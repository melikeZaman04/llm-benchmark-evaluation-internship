"""
HOST tarafındaki güvenli çalıştırma modülü (Sandbox Executor).

İki-düzlemli mimaride bu modül DETERMİNİSTİK ORACLE'ın parçasıdır:
verilen kodu izole bir Docker container'ında çalıştırır ve gizli testlere
sokar. Kararı (pass/fail) LLM değil, gerçek kod yürütme sonucu verir.

Güvenlik önlemleri (model 'rm -rf' üretse bile ana sistem korunur):
  --network none      : internet/ağ erişimi yok
  --memory / --cpus   : bellek ve CPU limiti
  --pids-limit        : fork bombasına karşı süreç limiti
  --read-only         : kök dosya sistemi salt-okunur
  --tmpfs /tmp        : yalnızca küçük, geçici, container'a özel yazılabilir alan
  --user 1000:1000    : root olmayan kullanıcı
  -v ...:/work:ro      : kod salt-okunur bağlanır
  subprocess timeout  : sonsuz döngüye karşı duvar-saati sınırı
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

IMAJ = "trc-sandbox:latest"


def sandboxta_calistir(
    kod: str,
    fonksiyon_adi: str,
    test_cases: list[dict],
    timeout_sn: int = 10,
    bellek: str = "256m",
    cpu: str = "1.0",
) -> dict:
    """
    Bir kod parçasını izole Docker sandbox'ında verilen testlere karşı çalıştırır.

    Dönüş (dict):
      {
        "gecti": bool,          # tüm testler geçti mi?
        "hata_tipi": str|None,  # None | syntax | runtime | timeout | mantik | ...
        "gecen": int, "toplam": int,
        "sonuclar": [...],      # test bazında ayrıntı
      }
    """
    with tempfile.TemporaryDirectory() as gecici:
        d = Path(gecici)
        (d / "solution.py").write_text(kod, encoding="utf-8")
        (d / "tests.json").write_text(
            json.dumps({"fonksiyon_adi": fonksiyon_adi, "test_cases": test_cases}),
            encoding="utf-8",
        )
        # harness.py'yi de gecici klasore kopyala (container /work'u salt-okunur gorur)
        harness_kaynak = Path(__file__).parent / "harness.py"
        (d / "harness.py").write_text(harness_kaynak.read_text(encoding="utf-8"), encoding="utf-8")

        # Container içindeki root-olmayan kullanıcı (uid 1000) dosyaları okuyabilsin.
        # executor kim olarak çalışırsa çalışsın (normal kullanıcı ya da sudo/root),
        # dosyalar dünya-okunur olsun ki uid uyuşmazlığı izin hatası yaratmasın.
        os.chmod(d, 0o755)
        for ad in ("solution.py", "tests.json", "harness.py"):
            os.chmod(d / ad, 0o644)

        komut = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", bellek, "--memory-swap", bellek,
            "--cpus", cpu,
            "--pids-limit", "64",
            "--read-only",
            "--tmpfs", "/tmp:size=16m",
            "-e", "PYTHONDONTWRITEBYTECODE=1",
            "--user", "1000:1000",
            "-v", f"{d}:/work:ro",
            IMAJ,
            "python", "/work/harness.py",
        ]

        try:
            proc = subprocess.run(
                komut, capture_output=True, text=True, timeout=timeout_sn
            )
        except subprocess.TimeoutExpired:
            return {"gecti": False, "hata_tipi": "timeout",
                    "gecen": 0, "toplam": len(test_cases), "sonuclar": []}

        cikti = proc.stdout.strip()
        try:
            sonuc = json.loads(cikti)
        except json.JSONDecodeError:
            # harness beklenen JSON'u üretemedi (ör. container hatası)
            return {"gecti": False, "hata_tipi": "harness_hatasi",
                    "stderr": proc.stderr[:500], "stdout": cikti[:500],
                    "gecen": 0, "toplam": len(test_cases), "sonuclar": []}

        sonuc["gecti"] = (
            sonuc.get("hata_tipi") is None
            and sonuc.get("gecen") == sonuc.get("toplam")
            and sonuc.get("toplam", 0) > 0
        )
        return sonuc


# --- Self-test: Docker açılınca `python src/sandbox/executor.py` ile denenir ---
if __name__ == "__main__":
    test_cases = [
        {"girdi": [[10, 20, 30], 40], "beklenen": 2},
        {"girdi": [[5, 5, 5, 5], 12], "beklenen": 2},
        {"girdi": [[100], 50], "beklenen": 0},
        {"girdi": [[], 100], "beklenen": 0},
        {"girdi": [[1, 1, 1, 1, 1], 3], "beklenen": 3},
        # AYIRT EDİCİ test: sırasız liste. Sıralamayı unutan (hatalı) çözüm
        # önce pahalı 10'u alıp bütçeyi tüketir -> 1 döner (doğru cevap 3).
        # Bu test olmadan zayıf çözüm yakalanamıyordu (benchmark kalitesi dersi).
        {"girdi": [[10, 3, 3, 3], 10], "beklenen": 3},
    ]

    dogru_kod = (
        "def max_urun(fiyatlar, butce):\n"
        "    fiyatlar = sorted(fiyatlar)\n"
        "    sayac = 0\n"
        "    for f in fiyatlar:\n"
        "        if butce >= f:\n"
        "            butce -= f\n"
        "            sayac += 1\n"
        "        else:\n"
        "            break\n"
        "    return sayac\n"
    )

    hatali_kod = (  # sıralamayı unutmuş -> bazı testlerde yanlış (mantik hatası)
        "def max_urun(fiyatlar, butce):\n"
        "    sayac = 0\n"
        "    for f in fiyatlar:\n"
        "        if butce >= f:\n"
        "            butce -= f\n"
        "            sayac += 1\n"
        "    return sayac\n"
    )

    print(">>> DOĞRU çözüm:")
    print(json.dumps(sandboxta_calistir(dogru_kod, "max_urun", test_cases),
                     ensure_ascii=False, indent=2))
    print("\n>>> HATALI çözüm:")
    print(json.dumps(sandboxta_calistir(hatali_kod, "max_urun", test_cases),
                     ensure_ascii=False, indent=2))
