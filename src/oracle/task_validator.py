"""
Oracle — Referans-Çözüm Doğrulayıcı.

İki-düzlemli mimarinin GUARDRAIL'inin temelidir: bir görevin (Task)
geçerli olması için, kendi `referans_cozum`'unun kendi `test_cases`'ini
Sandbox'ta EKSİKSİZ geçmesi gerekir. Bu doğrulama;
  - elle yazılan görevlerin tutarlılığını (imza/testler/çözüm uyumlu mu?),
  - ileride Mutator ajanının ürettiği varyantların bozulmadığını
kontrol etmek için kullanılır. Geçmeyen görev/varyant veri setine ALINMAZ.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# src/ dizinini yola ekle ki 'sandbox' paketini import edebilelim.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sandbox.executor import sandboxta_calistir  # noqa: E402


def gorevi_dogrula(gorev: dict) -> dict:
    """Bir görev nesnesini referans çözümüyle Sandbox'ta doğrular."""
    sonuc = sandboxta_calistir(
        kod=gorev["referans_cozum"],
        fonksiyon_adi=gorev["fonksiyon_adi"],
        test_cases=gorev["test_cases"],
        karsilastirma=gorev.get("karsilastirma"),
    )
    return {
        "id": gorev.get("id"),
        "gecerli": bool(sonuc["gecti"]),
        "gecen": sonuc["gecen"],
        "toplam": sonuc["toplam"],
        "hata_tipi": sonuc.get("hata_tipi"),
        "detay": sonuc,
    }


def dosyadan_dogrula(yol: str) -> dict:
    """Bir görev JSON dosyasını yükleyip doğrular."""
    gorev = json.loads(Path(yol).read_text(encoding="utf-8"))
    return gorevi_dogrula(gorev)


if __name__ == "__main__":
    import glob

    hedefler = sys.argv[1:] or sorted(glob.glob("data/tasks/*.json"))
    if not hedefler:
        print("Doğrulanacak görev bulunamadı (data/tasks/*.json).")
        sys.exit(1)

    tum_gecerli = True
    for yol in hedefler:
        r = dosyadan_dogrula(yol)
        isaret = "✅" if r["gecerli"] else "❌"
        ek = "" if r["gecerli"] else f"  [hata: {r['hata_tipi']}]"
        print(f"{isaret} {r['id']:<10} {r['gecen']}/{r['toplam']}  ({yol}){ek}")
        tum_gecerli = tum_gecerli and r["gecerli"]

    print("\nTüm görevler geçerli ✅" if tum_gecerli else "\nBazı görevler GEÇERSİZ ❌")
    sys.exit(0 if tum_gecerli else 1)
