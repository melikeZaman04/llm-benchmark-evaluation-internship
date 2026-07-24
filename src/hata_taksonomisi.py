#!/usr/bin/env python3
"""Gün 16: Hata taksonomisi — başarısızlıkların NEDEN olduğunu sınıflandırır.

Mekanik `hata_tipi` alanı yalnızca "sert" hataları (syntax, import, eksik
fonksiyon, timeout) etiketler; kod çalışıp testleri geçmediğinde (yanlış mantık)
alan null kalır ve cell-düzeyi `hata_tipleri` listesine HİÇ düşmez — bu, en
büyük başarısızlık türünü görünmez kılan bir kör noktadır. Bu modül örnek
düzeyinde sınıflandırır ve o kör noktayı kapatır:

  gecti           : test geçti
  yanlis_mantik   : kod çalıştı ama en az bir test yanlış (mantık hatası)
  eksik_fonksiyon : beklenen fonksiyon tanımlı değil (ör. yanlış ad)
  syntax          : sözdizimi hatası
  runtime_import  : yükleme/import anında çalışma hatası
  timeout         : sandbox zaman aşımı
  harness_hatasi  : koşucunun kendi hatası (nadir)

Girdi: results/*.ckpt.jsonl. Ajan çağrılmaz; salt okuma.
"""
import json
import argparse
from collections import Counter, defaultdict

SERT_TIPLER = {"syntax", "runtime_import", "eksik_fonksiyon", "timeout",
               "harness_hatasi"}


def sinifla(ornek: dict) -> str:
    """Bir örneği (cell içindeki tek koşum) tek bir başarısızlık sınıfına atar."""
    if ornek.get("gecti"):
        return "gecti"
    ht = ornek.get("hata_tipi")
    if ht in SERT_TIPLER:
        return ht
    # gecti=False ve sert tip yok => kod çalıştı ama testleri geçemedi.
    return "yanlis_mantik"


def hucreleri_yukle(yol):
    rows = []
    for l in open(yol, encoding="utf-8"):
        l = l.strip()
        if not l or '"_tip"' in l:
            continue
        rows.append(json.loads(l))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--girdi", default="results/gun15_buyuk_kosum.ckpt.jsonl")
    args = ap.parse_args()

    rows = hucreleri_yukle(args.girdi)
    ornekler = [(r, o) for r in rows for o in r.get("ornekler", [])]
    toplam = len(ornekler)
    modeller = sorted(set(r["model"] for r in rows))
    siniflar = ["gecti", "yanlis_mantik", "eksik_fonksiyon", "syntax",
                "runtime_import", "timeout", "harness_hatasi"]

    # --- Genel dağılım ---
    genel = Counter(sinifla(o) for _, o in ornekler)
    print("=" * 78)
    print(f"HATA TAKSONOMİSİ (n={toplam} örnek)  girdi={args.girdi}")
    print("=" * 78)
    for s in siniflar:
        if genel[s]:
            print(f"  {s:<16} {genel[s]:>5}  (%{genel[s]*100//toplam})")

    # --- MANŞET 5: Türkçe vergisi ne TÜR hatadan geliyor? ---
    dil_sinif = {"en": Counter(), "tr": Counter()}
    for r, o in ornekler:
        dil_sinif[r["dil"]][sinifla(o)] += 1
    print()
    print("=" * 78)
    print("MANŞET 5: Başarısızlık türü — TR vs EN (Türkçe vergisi hangi hatadan?)")
    print("=" * 78)
    print(f"{'sınıf':<16} {'en_hata':>8} {'tr_hata':>8} {'fark(tr-en)':>12}")
    print("-" * 78)
    for s in siniflar:
        if s == "gecti":
            continue
        e, t = dil_sinif["en"][s], dil_sinif["tr"][s]
        if e or t:
            print(f"{s:<16} {e:>8} {t:>8} {t-e:>+12}")
    ml_fark = dil_sinif["tr"]["yanlis_mantik"] - dil_sinif["en"]["yanlis_mantik"]
    sert_fark = sum(dil_sinif["tr"][s] - dil_sinif["en"][s] for s in SERT_TIPLER)
    print("-" * 78)
    print(f"  Türkçe fazladan başarısızlık: yanlış_mantık {ml_fark:+d}, "
          f"sert hatalar {sert_fark:+d}")
    if ml_fark > sert_fark:
        print("  => Türkçe vergisi ağırlıkla YANLIŞ-MANTIK vergisidir: kod çalışıyor,")
        print("     ama Türkçe'de daha sık mantıken yanlış (sözdizimi/çökme değil).")

    # --- Model başına başarısızlık profili (yalnız başarısızlar, % olarak) ---
    print()
    print("=" * 78)
    print("Model başına başarısızlık profili (başarısızların % dağılımı)")
    print("=" * 78)
    print(f"{'model':<20} {'başarısız':>9} {'mantık%':>8} {'eksik%':>7} "
          f"{'syntax%':>8} {'import%':>8}")
    print("-" * 78)
    for md in modeller:
        c = Counter(sinifla(o) for r, o in ornekler if r["model"] == md)
        bas = sum(v for k, v in c.items() if k != "gecti")
        if not bas:
            continue
        def pct(k):
            return f"{c[k]*100//bas}" if bas else "0"
        print(f"{md:<20} {bas:>9} {pct('yanlis_mantik'):>8} "
              f"{pct('eksik_fonksiyon'):>7} {pct('syntax'):>8} "
              f"{pct('runtime_import'):>8}")

    # --- Kategori başına yanlış-mantık yoğunluğu (hangi problem şekli zor?) ---
    kat = defaultdict(lambda: [0, 0])  # kategori -> [yanlis_mantik, toplam]
    for r, o in ornekler:
        k = r.get("kategori", "?")
        kat[k][1] += 1
        if sinifla(o) == "yanlis_mantik":
            kat[k][0] += 1
    print()
    print("=" * 78)
    print("Kategori başına yanlış-mantık oranı (problem şekli zorluğu)")
    print("=" * 78)
    print(f"{'kategori':<14} {'yanlış_mantık':>13} {'toplam':>7} {'oran':>7}")
    print("-" * 78)
    for k in sorted(kat, key=lambda x: -kat[x][0] / max(kat[x][1], 1)):
        m, tp = kat[k]
        print(f"{k:<14} {m:>13} {tp:>7} {m/tp:>7.2f}")


if __name__ == "__main__":
    main()
