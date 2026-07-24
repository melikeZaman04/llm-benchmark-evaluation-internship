#!/usr/bin/env python3
"""Kalite kapısı pipeline driver'ı — bir görevi TÜM kapılardan geçirir.

Blueprint (§5) sözleşmesini tek çağrıda uygular:
  kanonik : oracle + şema + tanımlayıcı-invariant (Design A backtick tutarlılığı)
  varyant : yukarıdakiler + uzunluk kapısı + değişmezler  (--ebeveyn ile)

Geçmeyen görev veri setine ALINMAZ. `gecir()` saftır (test edilebilir); CLI
dosya(lar)ı doğrular ve sıfır-dışı kod döner (CI'de kullanılabilir).
"""
from __future__ import annotations

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import task_io  # noqa: E402
from oracle.task_validator import gorevi_dogrula  # noqa: E402


def gecir(gorev: dict, ebeveyn: dict | None = None) -> dict:
    """Görevi tüm kapılardan geçirir; kapı adı -> hata listesi döner (boş = geçti)."""
    rapor = {
        "sema": task_io.metadatayi_dogrula(gorev),
        "tanimlayici": task_io.tanimlayici_kapisi(gorev),
    }
    o = gorevi_dogrula(gorev)  # oracle: referans çözüm test_cases'i geçmeli (Docker)
    rapor["oracle"] = ([] if o["gecerli"]
                       else [f"{o['gecen']}/{o['toplam']} [{o['hata_tipi']}]"])
    if ebeveyn is not None:
        rapor["uzunluk"] = task_io.uzunluk_kapisi(ebeveyn, gorev)
        rapor["degismezler"] = task_io.degismezleri_dogrula(ebeveyn, gorev)
    return rapor


def temiz_mi(rapor: dict) -> bool:
    return all(not h for h in rapor.values())


def main() -> int:
    ap = argparse.ArgumentParser(description="Görev kalite kapısı")
    ap.add_argument("gorevler", nargs="+", help="Görev JSON yolları")
    ap.add_argument("--ebeveyn", help="Varyantlar için ebeveyn kanonik JSON yolu")
    args = ap.parse_args()
    ebeveyn = task_io.gorev_oku(args.ebeveyn) if args.ebeveyn else None

    tum_temiz = True
    for yol in args.gorevler:
        g = task_io.gorev_oku(yol)
        rapor = gecir(g, ebeveyn)
        ok = temiz_mi(rapor)
        tum_temiz = tum_temiz and ok
        print(f"{'✅' if ok else '❌'} {g.get('id', yol)}")
        for kapi, hatalar in rapor.items():
            for h in hatalar:
                print(f"     - {kapi}: {h}")
    return 0 if tum_temiz else 1


if __name__ == "__main__":
    raise SystemExit(main())
