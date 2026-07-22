"""
Mutator ajanını çalıştırıp kanonik görevlerden veri setine yeni mutasyon
varyantları ekler (yol haritası Gün 13). Her varyant, dosyaya yazılmadan
önce oracle guardrail'inden geçmek ZORUNDADIR — reddedilen varyant veri
setine hiç girmez, yalnızca ekrana yazdırılır.

Önkoşul: `claude` (Claude Code CLI) PATH'te ve giriş yapılmış olmalı.

Kullanım:
    python src/run_mutator.py --gorev data/tasks/trc_003.json --sayi 2
    python src/run_mutator.py --gorev data/tasks/trc_003.json data/tasks/trc_014.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_factory.client import AjanCagriHatasi  # noqa: E402
from agent_factory.mutator import varyant_uret  # noqa: E402
from task_io import GOREVLER_DIZINI, gorev_oku, gorev_yaz, sonraki_id_uretici  # noqa: E402


def main() -> int:
    ayristirici = argparse.ArgumentParser(description="Mutator ajanı ile varyant üretimi")
    ayristirici.add_argument("--gorev", nargs="+", required=True,
                              help="Kanonik görev JSON dosyalarının yolu")
    ayristirici.add_argument("--sayi", type=int, default=1,
                              help="Her kanonik görev için üretilecek varyant sayısı")
    args = ayristirici.parse_args()

    id_uretici = sonraki_id_uretici()
    toplam_uretilen = 0
    toplam_reddedilen = 0
    toplam_maliyet = 0.0

    for yol in args.gorev:
        kanonik = gorev_oku(yol)
        for _ in range(args.sayi):
            yeni_id = next(id_uretici)
            try:
                yeni_gorev = varyant_uret(kanonik, yeni_id)
            except AjanCagriHatasi as e:
                print(f"❌ REDDEDİLDİ  {kanonik['id']} -> denenen {yeni_id}: {e}")
                toplam_reddedilen += 1
                continue

            maliyet = yeni_gorev.pop("_maliyet_usd", None)
            gorev_yaz(yeni_gorev, GOREVLER_DIZINI / f"{yeni_id}.json")
            toplam_uretilen += 1
            if maliyet:
                toplam_maliyet += maliyet
            print(f"✅ {yeni_id}  <- {kanonik['id']}  ({yeni_gorev['fonksiyon_adi']})"
                  + (f"  (~${maliyet:.3f})" if maliyet else ""))

    print(f"\nToplam: {toplam_uretilen} üretildi, {toplam_reddedilen} reddedildi"
          f"  (~${toplam_maliyet:.3f})")
    return 0 if toplam_reddedilen == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
