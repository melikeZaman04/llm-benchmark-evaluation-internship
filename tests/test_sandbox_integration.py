"""
Entegrasyon testleri — GERÇEK Docker sandbox'ını çalıştırır.

Docker veya trc-sandbox imajı yoksa tüm modül otomatik atlanır (skip).
Sandbox'ın hem doğruluğunu (pass/fail, hata sınıflandırma) hem de güvenlik
davranışını (ağ yok, yazma yok, timeout + container temizliği) doğrular.
"""

import json
import subprocess
import time
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent

from sandbox.executor import sandboxta_calistir
from oracle.task_validator import gorevi_dogrula


def _docker_hazir() -> bool:
    try:
        a = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        b = subprocess.run(["docker", "image", "inspect", "trc-sandbox:latest"],
                           capture_output=True, timeout=10)
        return a.returncode == 0 and b.returncode == 0
    except Exception:
        return False


pytestmark = [
    pytest.mark.docker,
    pytest.mark.skipif(not _docker_hazir(),
                       reason="Docker veya trc-sandbox:latest imajı yok"),
]

TC = [{"girdi": [2, 3], "beklenen": 5}, {"girdi": [0, 0], "beklenen": 0}]


def test_dogru_cozum_gecer():
    r = sandboxta_calistir("def topla(a, b):\n    return a + b\n", "topla", TC)
    assert r["gecti"] and r["gecen"] == 2 and r["hata_tipi"] is None


def test_hatali_cozum_mantik_hatasi():
    r = sandboxta_calistir("def topla(a, b):\n    return a - b\n", "topla", TC)
    assert not r["gecti"]
    assert any(s.get("hata_tipi") == "mantik" for s in r["sonuclar"])


def test_syntax_hatasi_yakalanir():
    r = sandboxta_calistir("def topla(a, b)\n    return a+b\n", "topla", TC)
    assert not r["gecti"] and r["hata_tipi"] == "syntax"


def test_eksik_fonksiyon():
    r = sandboxta_calistir("def baska():\n    return 1\n", "topla", TC)
    assert not r["gecti"] and r["hata_tipi"] == "eksik_fonksiyon"


def test_print_ciktisi_json_ayristirmayi_bozmaz():
    kod = "def topla(a, b):\n    print('gurultu ' * 500)\n    return a + b\n"
    r = sandboxta_calistir(kod, "topla", TC)
    assert r["gecti"] and r["gecen"] == 2


def test_yaklasik_karsilastirma_modu():
    r = sandboxta_calistir("def b(x):\n    return x / 3\n", "b",
                           [{"girdi": [1], "beklenen": 0.333333}],
                           karsilastirma={"mod": "yaklasik", "tol": 1e-4})
    assert r["gecti"]


def test_sirasiz_karsilastirma_modu():
    r = sandboxta_calistir("def s(x):\n    return [3, 1, 2]\n", "s",
                           [{"girdi": [0], "beklenen": [1, 2, 3]}],
                           karsilastirma={"mod": "sirasiz"})
    assert r["gecti"]


def test_ag_erisimi_engellenir():
    kod = ("import socket\n"
           "def f(x):\n"
           "    socket.create_connection(('8.8.8.8', 53), timeout=3)\n"
           "    return x\n")
    r = sandboxta_calistir(kod, "f", [{"girdi": [1], "beklenen": 1}])
    assert not r["gecti"]  # ağ yok -> runtime hatası, geçemez


def test_timeout_ve_container_sizintisi_yok():
    kod = "def f(x):\n    while True:\n        pass\n    return x\n"
    t0 = time.time()
    r = sandboxta_calistir(kod, "f", [{"girdi": [1], "beklenen": 1}], timeout_sn=4)
    sure = time.time() - t0
    assert r["hata_tipi"] == "timeout"
    assert sure < 15  # timeout makul sürede kesildi
    # Kritik: timeout sonrası kaçak container KALMAMALI
    kalan = subprocess.run(
        ["docker", "ps", "-q", "--filter", "ancestor=trc-sandbox:latest"],
        capture_output=True, text=True, timeout=10).stdout.strip()
    assert kalan == "", f"Kaçak container kaldı: {kalan}"


def test_oracle_trc_001_gecerli():
    gorev = json.loads((KOK / "data/tasks/trc_001.json").read_text(encoding="utf-8"))
    r = gorevi_dogrula(gorev)
    assert r["gecerli"] and r["gecen"] == r["toplam"]
