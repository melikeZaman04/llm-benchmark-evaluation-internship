"""
Birim testleri — Docker/model GEREKTİRMEZ, saf mantığı doğrular.

Kapsam: kod ayıklama, prompt üretimi, pass@k tahmincisi, harness karşılaştırma
modları, çoktan-seçmeli prompt üretimi. Bir test aracının kendi çekirdeğinin
testli olması, "güvenilir cetvel" iddiasının olmazsa olmazıdır.
"""

import pytest

from model_client.code_task import kod_ayikla, kod_prompt_olustur
from run_matrix import pass_at_k
import sandbox.harness as harness
import prompt_builder


# --- Kod ayıklama --------------------------------------------------------
def test_kod_ayikla_fenced_python():
    metin = "Elbette:\n```python\ndef f(x):\n    return x + 1\n```\nbitti"
    kod = kod_ayikla(metin)
    assert "def f(x)" in kod and "return x + 1" in kod


def test_kod_ayikla_def_iceren_blogu_tercih_eder():
    metin = "```\nprint('gurultu')\n```\n```python\ndef g():\n    return 2\n```"
    assert "def g" in kod_ayikla(metin)


def test_kod_ayikla_bloksuz_duz_kod():
    assert "def f" in kod_ayikla("def f(x):\n    return x")


# --- Prompt üretimi (TR/EN) ----------------------------------------------
def test_prompt_tr_ve_en_dogru_metni_kullanir():
    g = {"prompt_tr": "TR_METNI", "prompt_en": "EN_TEXT",
         "fonksiyon_imzasi": "def f() -> int:"}
    assert "TR_METNI" in kod_prompt_olustur(g, "tr")
    assert "EN_TEXT" in kod_prompt_olustur(g, "en")
    assert "def f() -> int:" in kod_prompt_olustur(g, "tr")


def test_prompt_gecersiz_dil_hata_verir():
    g = {"prompt_tr": "x", "prompt_en": "y", "fonksiyon_imzasi": "def f():"}
    with pytest.raises(ValueError):
        kod_prompt_olustur(g, "de")


# --- pass@k tahmincisi ---------------------------------------------------
def test_pass_at_k_bilinen_degerler():
    assert pass_at_k(5, 2, 1) == pytest.approx(0.4)
    assert pass_at_k(5, 2, 5) == pytest.approx(1.0)
    assert pass_at_k(5, 0, 3) == pytest.approx(0.0)
    assert pass_at_k(5, 5, 1) == pytest.approx(1.0)
    assert pass_at_k(10, 1, 5) == pytest.approx(0.5)


def test_pass_at_k_k_ustu_n_kirpar():
    # k > n verilse bile hata vermez, k=n gibi davranır
    assert pass_at_k(3, 1, 10) == pytest.approx(1.0)


# --- Harness karşılaştırma modları ---------------------------------------
def test_karsilastir_tam():
    assert harness._karsilastir(3, 3, "tam", 1e-9)
    assert not harness._karsilastir(3, 4, "tam", 1e-9)


def test_karsilastir_yaklasik_float():
    assert harness._karsilastir(0.3333333, 1 / 3, "yaklasik", 1e-4)
    assert not harness._karsilastir(0.34, 1 / 3, "yaklasik", 1e-4)


def test_karsilastir_sirasiz():
    assert harness._karsilastir([3, 2, 1], [1, 2, 3], "sirasiz", 1e-9)
    assert not harness._karsilastir([3, 2, 1], [1, 2, 3], "tam", 1e-9)


# --- Çoktan-seçmeli prompt (faz 1 track) ---------------------------------
def test_mc_prompt_secenekleri_icerir():
    q = {"id": "q", "question": "Soru?",
         "choices": {"A": "a", "B": "b", "C": "c", "D": "d"}}
    p = prompt_builder.build_prompt(q)
    assert "A)" in p and "D)" in p


def test_mc_prompt_eksik_secenek_hata_verir():
    q = {"id": "q", "question": "Soru?", "choices": {"A": "a", "B": "b"}}
    with pytest.raises(ValueError):
        prompt_builder.build_prompt(q)
