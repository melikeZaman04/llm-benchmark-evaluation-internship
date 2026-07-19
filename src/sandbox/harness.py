"""
Container İÇİNDE çalışan test koşucusu (harness).

Host tarafındaki executor, /work altına iki dosya bırakır:
  - solution.py : değerlendirilecek Python kodu (referans çözüm ya da model çıktısı)
  - tests.json  : {"fonksiyon_adi": str,
                   "test_cases": [{"girdi": [...], "beklenen": ...}],
                   "karsilastirma": {"mod": "tam|yaklasik|sirasiz", "tol": float}}

Bu betik solution.py'yi güvenli biçimde yükler, her test case'i çalıştırır
ve sonucu TEK bir JSON satırı olarak stdout'a yazar. Böylece host tarafı
çıktıyı deterministik olarak ayrıştırır. Hiçbir yargı (pass/fail) LLM'e
bırakılmaz; burada her şey saf koddur.

ÖNEMLİ: Değerlendirilen kodun ürettiği stdout (ör. `print`) baskılanır ve
yalnızca harness'in ürettiği tek JSON satırı gerçek stdout'a yazılır. Aksi
halde (a) modelin print'leri host'un JSON ayrıştırmasını bozar, (b) sınırsız
çıktı host belleğini şişirebilir. Baskılama bu iki açığı kaynağında kapatır.
"""

import contextlib
import importlib.util
import json
import os
import sys
import traceback

# Gerçek stdout'u sakla; harness'in JSON'u YALNIZCA buraya yazılır.
_GERCEK_STDOUT = sys.stdout


def _cikti(obj: dict) -> None:
    """Harness sonucunu (yalnız harness'e ait) gerçek stdout'a tek satır yazar."""
    print(json.dumps(obj), file=_GERCEK_STDOUT)


def _yukle(dosya_yolu: str):
    """solution.py'yi bir modül olarak yükler; syntax/import hatalarını yakalar."""
    spec = importlib.util.spec_from_file_location("solution", dosya_yolu)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _karsilastir(uretilen, beklenen, mod: str, tol: float) -> bool:
    """
    Beklenen çıktı ile üretileni verilen moda göre karşılaştırır.
      - tam      : birebir eşitlik (varsayılan)
      - yaklasik : sayısal, |a-b| <= tol (float problemleri için)
      - sirasiz  : sıra önemsiz (liste/çokküme olarak karşılaştır)
    Uygun olmayan tip gelirse güvenli tarafta kalıp tam eşitliğe düşer.
    """
    if mod == "yaklasik":
        try:
            return abs(uretilen - beklenen) <= tol
        except TypeError:
            return uretilen == beklenen
    if mod == "sirasiz":
        try:
            return sorted(uretilen) == sorted(beklenen)
        except TypeError:
            return uretilen == beklenen
    return uretilen == beklenen


def main() -> None:
    with open("/work/tests.json", encoding="utf-8") as f:
        payload = json.load(f)

    fonksiyon_adi = payload["fonksiyon_adi"]
    test_cases = payload["test_cases"]
    kars = payload.get("karsilastirma") or {}
    mod = kars.get("mod", "tam")
    tol = float(kars.get("tol", 1e-9))

    # Değerlendirilen kodun tüm stdout'u devnull'a; sadece harness JSON'u çıkar.
    devnull = open(os.devnull, "w")

    # 1) Kodu yükle — syntax veya import zamanı hataları burada ayrışır.
    try:
        with contextlib.redirect_stdout(devnull):
            modul = _yukle("/work/solution.py")
    except SyntaxError as e:
        _cikti({"hata_tipi": "syntax", "detay": str(e),
                "gecen": 0, "toplam": len(test_cases), "sonuclar": []})
        return
    except Exception as e:  # noqa: BLE001 - import sırasında her şey olabilir
        _cikti({"hata_tipi": "runtime_import", "detay": repr(e),
                "gecen": 0, "toplam": len(test_cases), "sonuclar": []})
        return

    # 2) Beklenen fonksiyon tanımlı mı?
    fonksiyon = getattr(modul, fonksiyon_adi, None)
    if not callable(fonksiyon):
        _cikti({"hata_tipi": "eksik_fonksiyon", "detay": fonksiyon_adi,
                "gecen": 0, "toplam": len(test_cases), "sonuclar": []})
        return

    # 3) Her test case'i çalıştır (kodun stdout'u baskılı).
    sonuclar = []
    for tc in test_cases:
        girdi = tc["girdi"]
        beklenen = tc["beklenen"]
        try:
            with contextlib.redirect_stdout(devnull):
                uretilen = fonksiyon(*girdi)
            dogru = _karsilastir(uretilen, beklenen, mod, tol)
            sonuclar.append({
                "ok": dogru,
                "uretilen": uretilen if _serilestirilebilir(uretilen) else str(uretilen),
                "hata_tipi": None if dogru else "mantik",
            })
        except Exception as e:  # noqa: BLE001
            sonuclar.append({"ok": False, "hata_tipi": "runtime", "detay": repr(e)})

    gecen = sum(1 for s in sonuclar if s["ok"])
    _cikti({"hata_tipi": None, "gecen": gecen,
            "toplam": len(test_cases), "sonuclar": sonuclar})


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
        _cikti({"hata_tipi": "harness_hatasi", "detay": repr(e),
                "iz": traceback.format_exc()[:800],
                "gecen": 0, "toplam": 0, "sonuclar": []})
        sys.exit(0)
