#!/usr/bin/env python3
"""Kalite kapısı pipeline driver'ı — bir görevi TÜM kapılardan geçirir.

Blueprint (§5) sözleşmesini tek çağrıda uygular:
  kanonik : oracle + şema + tanımlayıcı-invariant (Design A backtick tutarlılığı)
  varyant : yukarıdakiler + uzunluk kapısı + değişmezler  (--ebeveyn ile)

Geçmeyen görev veri setine ALINMAZ. `gecir()` saftır (test edilebilir); CLI
dosya(lar)ı doğrular ve sıfır-dışı kod döner (CI'de kullanılabilir).
"""
from __future__ import annotations

import re
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import task_io  # noqa: E402
from oracle.task_validator import gorevi_dogrula  # noqa: E402


def _parametreler(imza: str):
    return set(re.findall(r"[(,]\s*([A-Za-z_]\w*)\s*:", imza))


def backtick_kapisi(gorev: dict) -> list[str]:
    """Prompt backtick'leri ilgili DİLİN imzasıyla eşleşmeli (Design A)."""
    hatalar = []
    tr = _parametreler(gorev["fonksiyon_imzasi"]) | {gorev["fonksiyon_adi"]}
    en_imza = gorev.get("fonksiyon_imzasi_en", gorev["fonksiyon_imzasi"])
    en = _parametreler(en_imza) | {gorev.get("fonksiyon_adi_en", gorev["fonksiyon_adi"])}
    for t in re.findall(r"`([A-Za-z_]\w*)`", gorev.get("prompt_tr", "")):
        if t not in tr:
            hatalar.append(f"TR backtick `{t}` TR imzada yok")
    for t in re.findall(r"`([A-Za-z_]\w*)`", gorev.get("prompt_en", "")):
        if t not in en:
            hatalar.append(f"EN backtick `{t}` EN imzada yok")
    return hatalar


def gecir(gorev: dict, ebeveyn: dict | None = None) -> dict:
    """Görevi tüm kapılardan geçirir; kapı adı -> hata listesi döner (boş = geçti)."""
    rapor = {
        "sema": task_io.metadatayi_dogrula(gorev),
        "tanimlayici": backtick_kapisi(gorev),
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
