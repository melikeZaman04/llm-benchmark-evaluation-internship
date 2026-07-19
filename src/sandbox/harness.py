"""
Container İÇİNDE çalışan test koşucusu (harness).

Host tarafındaki executor, /work altına iki dosya bırakır:
  - solution.py : değerlendirilecek Python kodu (referans çözüm ya da model çıktısı)
  - tests.json  : {"fonksiyon_adi": str, "test_cases": [{"girdi": [...], "beklenen": ...}]}

Bu betik solution.py'yi güvenli biçimde yükler, her test case'i çalıştırır
ve sonucu TEK bir JSON satırı olarak stdout'a yazar. Böylece host tarafı
çıktıyı deterministik olarak ayrıştırır. Hiçbir yargı (pass/fail) LLM'e
bırakılmaz; burada her şey saf koddur.
"""

import importlib.util
import json
import sys
import traceback


def _yukle(dosya_yolu: str):
    """solution.py'yi bir modül olarak yükler; syntax/import hatalarını yakalar."""
    spec = importlib.util.spec_from_file_location("solution", dosya_yolu)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def main() -> None:
    with open("/work/tests.json", encoding="utf-8") as f:
        payload = json.load(f)

    fonksiyon_adi = payload["fonksiyon_adi"]
    test_cases = payload["test_cases"]

    # 1) Kodu yükle — syntax veya import zamanı hataları burada ayrışır.
    try:
        modul = _yukle("/work/solution.py")
    except SyntaxError as e:
        print(json.dumps({"hata_tipi": "syntax", "detay": str(e),
                          "gecen": 0, "toplam": len(test_cases), "sonuclar": []}))
        return
    except Exception as e:  # noqa: BLE001 - import sırasında her şey olabilir
        print(json.dumps({"hata_tipi": "runtime_import", "detay": repr(e),
                          "gecen": 0, "toplam": len(test_cases), "sonuclar": []}))
        return

    # 2) Beklenen fonksiyon tanımlı mı?
    fonksiyon = getattr(modul, fonksiyon_adi, None)
    if not callable(fonksiyon):
        print(json.dumps({"hata_tipi": "eksik_fonksiyon", "detay": fonksiyon_adi,
                          "gecen": 0, "toplam": len(test_cases), "sonuclar": []}))
        return

    # 3) Her test case'i çalıştır.
    sonuclar = []
    for tc in test_cases:
        girdi = tc["girdi"]
        beklenen = tc["beklenen"]
        try:
            uretilen = fonksiyon(*girdi)
            dogru = (uretilen == beklenen)
            sonuclar.append({
                "ok": dogru,
                "uretilen": uretilen if _serilestirilebilir(uretilen) else str(uretilen),
                "hata_tipi": None if dogru else "mantik",
            })
        except Exception as e:  # noqa: BLE001
            sonuclar.append({"ok": False, "hata_tipi": "runtime", "detay": repr(e)})

    gecen = sum(1 for s in sonuclar if s["ok"])
    print(json.dumps({"hata_tipi": None, "gecen": gecen,
                      "toplam": len(test_cases), "sonuclar": sonuclar}))


def _serilestirilebilir(deger) -> bool:
    try:
        json.dumps(deger)
        return True
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # son güvenlik ağı: harness asla sessizce ölmesin
        print(json.dumps({"hata_tipi": "harness_hatasi", "detay": repr(e),
                          "iz": traceback.format_exc()[:800],
                          "gecen": 0, "toplam": 0, "sonuclar": []}))
        sys.exit(0)
