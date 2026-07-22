"""
Parametrik varyant üretimini çalıştırır: kanonik görevlerin `sablon`
kombinasyonlarından ezber-dayanıklılığı ekseni için varyant ailesi kurar.

Her varyant, dosyaya yazılmadan önce iki kapıdan geçmek ZORUNDADIR:
değişmezlik kapısı (kod/test alanları kıpırdamamış mı) ve oracle guardrail'i.
Reddedilen varyant veri setine hiç girmez, yalnızca ekrana yazdırılır.

Önkoşul: `claude` (Claude Code CLI) PATH'te ve giriş yapılmış olmalı; Docker
çalışır durumda olmalı (oracle sandbox'ı kullanır).

Kullanım:
    # ne üretileceğini göster, hiçbir şey çalıştırma
    python src/run_parametric.py --tumu --kuru

    # tek görevden 2 varyant
    python src/run_parametric.py --gorev data/tasks/trc_001.json --sayi 2

    # varyantı olmayan tüm kanonik görevlerden 1'er varyant
    python src/run_parametric.py --tumu --sayi 1
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agent_factory.client import AjanCagriHatasi  # noqa: E402
from agent_factory.parametric import kombinasyon_sayisi, varyantlari_uret  # noqa: E402
from task_io import (  # noqa: E402
    GOREVLER_DIZINI, gorev_oku, gorev_yaz, gorevleri_yukle, sonraki_id_uretici,
)


def _kanonikleri_sec(args) -> list[dict]:
    if args.gorev:
        return [gorev_oku(yol) for yol in args.gorev]
    return [g for g in gorevleri_yukle()
            if g.get("variant_type") == "canonical" and g.get("sablon")]


def main() -> int:
    a = argparse.ArgumentParser(description="Parametrik varyant üretimi")
    kaynak = a.add_mutually_exclusive_group(required=True)
    kaynak.add_argument("--gorev", nargs="+", help="Kanonik görev JSON yolları")
    kaynak.add_argument("--tumu", action="store_true",
                        help="sablon'u olan tüm kanonik görevler")
    a.add_argument("--sayi", type=int, default=1,
                   help="Her kanonik görev için üretilecek varyant sayısı")
    a.add_argument("--kuru", action="store_true",
                   help="Hiçbir şey üretme; yalnızca planı ve kapasiteyi yazdır")
    args = a.parse_args()

    kanonikler = _kanonikleri_sec(args)
    if not kanonikler:
        print("Uygun kanonik görev bulunamadı (sablon alanı olan var mı?).")
        return 1

    if args.kuru:
        print(f"{'gorev':<10} {'kategori':<12} {'kapasite':>8} {'planlanan':>10}")
        toplam = 0
        for k in kanonikler:
            kapasite = kombinasyon_sayisi(k)
            planlanan = min(kapasite, args.sayi)
            toplam += planlanan
            print(f"{k['id']:<10} {k['kategori']:<12} {kapasite:>8} {planlanan:>10}")
        print(f"\nToplam planlanan varyant: {toplam}  "
              f"(veri seti {len(gorevleri_yukle())} -> {len(gorevleri_yukle()) + toplam})")
        return 0

    id_uretici = sonraki_id_uretici()
    uretilen = reddedilen = 0
    toplam_maliyet = 0.0

    for kanonik in kanonikler:
        kapasite = kombinasyon_sayisi(kanonik)
        if not kapasite:
            print(f"⏭  {kanonik['id']}: sablon yok veya tek kombinasyon, atlandı")
            continue

        idler = [next(id_uretici) for _ in range(min(kapasite, args.sayi))]
        try:
            varyantlar = varyantlari_uret(kanonik, idler)
        except AjanCagriHatasi as e:
            # Reddedilen varyantın ajan çağrısı zaten yapıldı: harcanan para
            # toplama YİNE DE eklenir, yoksa maliyet olduğundan düşük görünür.
            toplam_maliyet += getattr(e, "maliyet_usd", None) or 0.0
            print(f"❌ REDDEDİLDİ  {kanonik['id']}: {e}")
            reddedilen += 1
            continue

        for varyant in varyantlar:
            maliyet = varyant.get("_maliyet_usd") or 0.0
            toplam_maliyet += maliyet
            gorev_yaz(varyant, GOREVLER_DIZINI / f"{varyant['id']}.json")
            uretilen += 1
            print(f"✅ {varyant['id']}  <- {kanonik['id']}"
                  + (f"  (~${maliyet:.3f})" if maliyet else ""))

    print(f"\nToplam: {uretilen} üretildi, {reddedilen} reddedildi"
          f"  (~${toplam_maliyet:.3f})")
    return 0 if reddedilen == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
