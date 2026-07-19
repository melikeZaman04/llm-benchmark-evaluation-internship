"""
Çoklu-model / çoklu-dil koşum matrisi (yol haritası Gün 10).

Bir görev kümesini (data/tasks/*.json) birden çok model ve dille koşup
sonuçları YAPILANDIRILMIŞ biçimde kaydeder. Her satır tek bir
(görev × model × dil) birimidir. Bu çıktı, Gün 15 metrik motorunun
(pass@k, Türkçe vergisi, ezber farkı, token vergisi) doğrudan girdisidir.

Determinizm notu: sabit seed + temperature=0 kullanılsa bile, düşük VRAM'de
(model takası + kısmi GPU offload) yerel çıkarım BIT-tekrarlanabilir değildir;
pass@1 koşumdan koşuma ±1 test oynayabilir (Gün 10 bulgusu). Bu yüzden runner
her hücreyi (görev × model × dil) `--tekrar K` kez koşup TÜM örnekleri saklar.
Böylece gürültü şeffaf kaydedilir ve Gün 15'teki pass@k'nin ham girdisi oluşur.

Kullanım:
    python src/run_matrix.py                          # K=1
    python src/run_matrix.py --tekrar 3               # hücre başına 3 örnek
    python src/run_matrix.py --modeller qwen2.5:3b,gemma2:2b --diller tr,en
    python src/run_matrix.py --gorevler "data/tasks/*.json" --cikti results/matris.json
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from model_client import ModelIstemcisi, ModelBaglantiHatasi  # noqa: E402
from run_task import gorevi_calistir  # noqa: E402

VARSAYILAN_MODELLER = [
    "qwen2.5:0.5b", "qwen2.5:1.5b", "qwen2.5:3b", "llama3.2:3b", "gemma2:2b",
]
VARSAYILAN_DILLER = ["tr", "en"]


def _tokenlar(kullanim: dict | None) -> dict:
    """Token kullanımını sabit anahtarlara indirger (eksikse None)."""
    k = kullanim or {}
    return {
        "prompt": k.get("prompt_tokens"),
        "completion": k.get("completion_tokens"),
        "total": k.get("total_tokens"),
    }


def matris_kosu(gorevler: list[dict], modeller: list[str],
                diller: list[str], tekrar: int = 1) -> list[dict]:
    """
    Görev × model × dil matrisini koşar; her hücre `tekrar` kez örneklenir.
    Her kayıt, o hücrenin K örneğini ve özetini (gecti_sayisi/K, gecen aralığı)
    içerir — böylece yerel çıkarımın gürültüsü şeffaf saklanır.
    """
    kayitlar: list[dict] = []
    toplam = len(gorevler) * len(modeller) * len(diller)
    sayac = 0
    for model in modeller:
        istemci = ModelIstemcisi.ollama(model=model)
        erisim = istemci.erisilebilir_mi()
        for gorev in gorevler:
            for dil in diller:
                sayac += 1
                onek = f"[{sayac:>3}/{toplam}] {model:<14} {dil}  {gorev.get('id')}"
                if not erisim:
                    print(f"{onek} -> SUNUCU YOK")
                    kayitlar.append(_hata_kaydi(gorev, model, dil, "sunucu_yok", tekrar))
                    continue
                ornekler = []
                for _ in range(tekrar):
                    try:
                        r = gorevi_calistir(gorev, istemci, dil=dil)
                        ornekler.append({
                            "gecti": r["gecti"], "gecen": r["gecen"],
                            "toplam": r["toplam"], "hata_tipi": r["hata_tipi"],
                            "tokenlar": _tokenlar(r.get("kullanim")),
                        })
                    except ModelBaglantiHatasi as e:
                        print(f"{onek} -> HATA: {e}")
                        ornekler.append({"gecti": False, "gecen": 0,
                                         "toplam": len(gorev.get("test_cases", [])),
                                         "hata_tipi": "istemci_hatasi",
                                         "tokenlar": _tokenlar(None)})
                kayitlar.append(_hucre_kaydi(gorev, model, dil, ornekler))
                gecti_sayisi = sum(1 for o in ornekler if o["gecti"])
                gecenler = [o["gecen"] for o in ornekler]
                aralik = (f"{min(gecenler)}-{max(gecenler)}"
                          if min(gecenler) != max(gecenler) else str(gecenler[0]))
                print(f"{onek} -> geçen={aralik}/{ornekler[0]['toplam']}  "
                      f"pass {gecti_sayisi}/{tekrar}")
    return kayitlar


def _hucre_kaydi(gorev: dict, model: str, dil: str, ornekler: list[dict]) -> dict:
    """Bir hücrenin K örneğini özetleyip kayıt nesnesine çevirir."""
    gecenler = [o["gecen"] for o in ornekler]
    toklar = [o["tokenlar"]["completion"] for o in ornekler
              if o["tokenlar"]["completion"] is not None]
    return {
        "gorev": gorev.get("id"), "kategori": gorev.get("kategori"),
        "model": model, "dil": dil,
        "tekrar": len(ornekler),
        "gecti_sayisi": sum(1 for o in ornekler if o["gecti"]),
        "gecen_min": min(gecenler), "gecen_max": max(gecenler),
        "toplam": ornekler[0]["toplam"],
        "hata_tipleri": sorted({o["hata_tipi"] for o in ornekler if o["hata_tipi"]}),
        "ort_completion_tok": round(sum(toklar) / len(toklar)) if toklar else None,
        "kararli": min(gecenler) == max(gecenler),  # K örnek aynı mı?
        "ornekler": ornekler,
    }


def _hata_kaydi(gorev: dict, model: str, dil: str, hata: str, tekrar: int) -> dict:
    n = len(gorev.get("test_cases", []))
    ornekler = [{"gecti": False, "gecen": 0, "toplam": n, "hata_tipi": hata,
                 "tokenlar": _tokenlar(None)} for _ in range(tekrar)]
    return _hucre_kaydi(gorev, model, dil, ornekler)


def ozet_yazdir(kayitlar: list[dict]) -> None:
    """Model × dil bazında pass oranı, geçen-aralığı ve kararlılık özeti."""
    print("\n=== ÖZET (model × dil) ===")
    print(f"{'model':<14} {'dil':<3} {'pass':>6} {'geçen':>7} {'kararlı':>8} {'ort_tok':>8}")
    for k in sorted(kayitlar, key=lambda x: (x["model"], x["dil"])):
        aralik = (f"{k['gecen_min']}-{k['gecen_max']}"
                  if k["gecen_min"] != k["gecen_max"] else str(k["gecen_min"]))
        kararli = "evet" if k["kararli"] else "HAYIR"
        ort = k["ort_completion_tok"] if k["ort_completion_tok"] is not None else "-"
        print(f"{k['model']:<14} {k['dil']:<3} {k['gecti_sayisi']:>3}/{k['tekrar']:<2} "
              f"{aralik:>7} {kararli:>8} {ort:>8}")


def csv_yaz(kayitlar: list[dict], yol: Path) -> None:
    """Düz (flat) CSV — hücre başına bir satır (özet)."""
    with yol.open("w", newline="", encoding="utf-8") as f:
        yazici = csv.writer(f)
        yazici.writerow(["gorev", "kategori", "model", "dil", "tekrar",
                         "gecti_sayisi", "gecen_min", "gecen_max", "toplam",
                         "kararli", "hata_tipleri", "ort_completion_tok"])
        for k in kayitlar:
            yazici.writerow([k["gorev"], k["kategori"], k["model"], k["dil"],
                             k["tekrar"], k["gecti_sayisi"], k["gecen_min"],
                             k["gecen_max"], k["toplam"], k["kararli"],
                             ";".join(k["hata_tipleri"]), k["ort_completion_tok"]])


def main() -> int:
    a = argparse.ArgumentParser(description="TR-CodeEval koşum matrisi")
    a.add_argument("--gorevler", default="data/tasks/*.json")
    a.add_argument("--modeller", default=",".join(VARSAYILAN_MODELLER))
    a.add_argument("--diller", default=",".join(VARSAYILAN_DILLER))
    a.add_argument("--tekrar", type=int, default=1,
                   help="Hücre başına örnek sayısı (gürültü/pass@k için)")
    a.add_argument("--cikti", default="results/matris.json")
    args = a.parse_args()

    yollar = sorted(glob.glob(args.gorevler))
    if not yollar:
        print(f"Görev bulunamadı: {args.gorevler}")
        return 1
    gorevler = [json.loads(Path(y).read_text(encoding="utf-8")) for y in yollar]
    modeller = [m.strip() for m in args.modeller.split(",") if m.strip()]
    diller = [d.strip() for d in args.diller.split(",") if d.strip()]

    print(f"Görev: {len(gorevler)} | Model: {len(modeller)} | Dil: {len(diller)} "
          f"| Tekrar: {args.tekrar} "
          f"| Toplam koşum: {len(gorevler)*len(modeller)*len(diller)*args.tekrar}\n")

    kayitlar = matris_kosu(gorevler, modeller, diller, tekrar=args.tekrar)

    cikti = {
        "meta": {
            "tarih_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "seed": 0, "temperature": 0.0, "tekrar": args.tekrar,
            "modeller": modeller, "diller": diller,
            "gorev_sayisi": len(gorevler),
            "not": ("Yerel çıkarım düşük VRAM'de bit-tekrarlanabilir değil; "
                    "'kararli=false' hücreler K örnek arasında oynamıştır."),
        },
        "kayitlar": kayitlar,
    }
    json_yol = Path(args.cikti)
    json_yol.parent.mkdir(parents=True, exist_ok=True)
    json_yol.write_text(json.dumps(cikti, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    csv_yol = json_yol.with_suffix(".csv")
    csv_yaz(kayitlar, csv_yol)

    ozet_yazdir(kayitlar)
    print(f"\nKaydedildi: {json_yol}  ve  {csv_yol}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
