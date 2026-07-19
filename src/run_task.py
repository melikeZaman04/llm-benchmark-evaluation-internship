"""
Uçtan-uca dikey dilim (yol haritası 4. adım).

Tek bir görevi baştan sona geçirir:
    görev (JSON) → prompt → yerel model → kod → Sandbox → pass/fail

İki-düzlemli mimarinin tamamını küçük ölçekte doğrular: model (test edilen
özne) kodu üretir, karar (doğru/yanlış) yalnızca deterministik Sandbox'tan
gelir. Hiçbir yargı LLM'e bırakılmaz.

Kullanım:
    python src/run_task.py                         # varsayılan: trc_001, tr, gemma2:2b
    python src/run_task.py --model qwen2.5:3b --dil en
    python src/run_task.py --gorev data/tasks/trc_001.json --model llama3.2:3b
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# src/ dizinini yola ekle ki paketleri import edebilelim.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from model_client import ModelIstemcisi, ModelBaglantiHatasi, modelden_cozum_al  # noqa: E402
from sandbox.executor import sandboxta_calistir  # noqa: E402


def gorevi_calistir(gorev: dict, istemci: ModelIstemcisi, dil: str = "tr") -> dict:
    """Bir görevi model + sandbox üzerinden uçtan uca çalıştırır."""
    uretim = modelden_cozum_al(gorev, istemci, dil=dil)
    calisma = sandboxta_calistir(
        kod=uretim["kod"],
        fonksiyon_adi=gorev["fonksiyon_adi"],
        test_cases=gorev["test_cases"],
        karsilastirma=gorev.get("karsilastirma"),
    )
    return {
        "id": gorev.get("id"),
        "model": istemci.model,
        "dil": dil,
        "gecti": calisma["gecti"],
        "gecen": calisma["gecen"],
        "toplam": calisma["toplam"],
        "hata_tipi": calisma.get("hata_tipi"),
        "kod": uretim["kod"],
        "kullanim": uretim.get("kullanim"),
        "calisma": calisma,
    }


def main() -> int:
    ayrıştırıcı = argparse.ArgumentParser(description="TR-CodeEval dikey dilim")
    ayrıştırıcı.add_argument("--gorev", default="data/tasks/trc_001.json")
    ayrıştırıcı.add_argument("--model", default=None,
                            help="Ollama model adı (varsayılan env TRC_MODEL / gemma2:2b)")
    ayrıştırıcı.add_argument("--dil", default="tr", choices=["tr", "en"])
    ayrıştırıcı.add_argument("--saglayici", default="ollama",
                            choices=["ollama", "lm_studio"])
    args = ayrıştırıcı.parse_args()

    gorev = json.loads(Path(args.gorev).read_text(encoding="utf-8"))

    if args.saglayici == "ollama":
        istemci = ModelIstemcisi.ollama(model=args.model)
    else:
        istemci = ModelIstemcisi.lm_studio(model=args.model)

    print(f"Görev: {gorev.get('id')}  |  Model: {istemci.model}  |  Dil: {args.dil}")
    print(f"Sunucu: {istemci.base_url}\n")

    if not istemci.erisilebilir_mi():
        print("HATA: Model sunucusuna ulaşılamadı. `ollama serve` çalışıyor mu?")
        return 2

    try:
        sonuc = gorevi_calistir(gorev, istemci, dil=args.dil)
    except ModelBaglantiHatasi as e:
        print(f"HATA: {e}")
        return 2

    isaret = "✅ GEÇTI" if sonuc["gecti"] else "❌ KALDI"
    print("--- MODELİN ÜRETTİĞİ KOD ---")
    print(sonuc["kod"])
    print("--- SONUÇ ---")
    print(f"{isaret}   {sonuc['gecen']}/{sonuc['toplam']} test"
          + (f"   [hata: {sonuc['hata_tipi']}]" if not sonuc["gecti"] else ""))
    if sonuc.get("kullanim"):
        print(f"Token kullanımı: {sonuc['kullanim']}")
    return 0 if sonuc["gecti"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
