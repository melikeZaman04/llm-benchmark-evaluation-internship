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
import task_io


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


# --- Veri seti şeması ----------------------------------------------------
# NOT: Bu testler veri setinin BOYUTUNU değil, DEĞİŞMEZLERİNİ doğrular.
# Görev sayısına sabit bir beklenti yazmak (ör. `== 27`), veri setini
# büyütmeyi ana hedef edinmiş bir projede her eklemede kırılan bir test
# üretir — testler büyümeyi engellememeli, bozulmayı engellemeli.

def _veri_setindeki_gorevler():
    return [(g["id"], g) for g in task_io.gorevleri_yukle()]


@pytest.mark.parametrize("gorev_id,gorev", _veri_setindeki_gorevler(),
                         ids=lambda d: d if isinstance(d, str) else "")
def test_gorev_metadatasi_semaya_uyar(gorev_id, gorev):
    hatalar = task_io.metadatayi_dogrula(gorev)
    assert not hatalar, f"{gorev_id} şema ihlali: " + "; ".join(hatalar)


def test_varyantlarin_ebeveyni_veri_setinde_var():
    gorevler = {g["id"]: g for g in task_io.gorevleri_yukle()}
    for gorev in gorevler.values():
        if gorev["variant_type"] == "canonical":
            continue
        assert gorev["ebeveyn"] in gorevler, \
            f"{gorev['id']}: ebeveyn {gorev['ebeveyn']} veri setinde yok"
        assert gorevler[gorev["canonical_id"]]["variant_type"] == "canonical", \
            f"{gorev['id']}: canonical_id kanonik olmayan bir göreve işaret ediyor"


def test_parametrik_varyantlar_ebeveyninin_kodunu_aynen_tasir():
    """Parametrik eksende YALNIZCA metin değişir; kod/test byte-byte aynıdır."""
    gorevler = {g["id"]: g for g in task_io.gorevleri_yukle()}
    parametrikler = [g for g in gorevler.values()
                     if g["variant_type"] == "parametric_story"]
    for varyant in parametrikler:
        sapmalar = task_io.degismezleri_dogrula(gorevler[varyant["ebeveyn"]], varyant)
        assert not sapmalar, "; ".join(sapmalar)


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


# --- Koşum matrisi kontrol noktası ---------------------------------------
def test_kontrol_noktasi_tamamlanan_hucreleri_doner(tmp_path):
    import json as _json
    from run_matrix import kontrol_noktasi_yukle, _imza

    yol = tmp_path / "m.ckpt.jsonl"
    imza = _imza(tekrar=3, sicaklik=0.4)
    satirlar = [
        {"_tip": "imza", **imza},
        {"gorev": "trc_001", "model": "qwen2.5:3b", "dil": "tr", "gecti_sayisi": 2},
        {"gorev": "trc_001", "model": "qwen2.5:3b", "dil": "en", "gecti_sayisi": 3},
    ]
    yol.write_text("\n".join(_json.dumps(s) for s in satirlar) + "\n", encoding="utf-8")

    tamam = kontrol_noktasi_yukle(yol, imza)
    assert set(tamam) == {("trc_001", "qwen2.5:3b", "tr"),
                          ("trc_001", "qwen2.5:3b", "en")}
    assert tamam[("trc_001", "qwen2.5:3b", "tr")]["gecti_sayisi"] == 2


def test_kontrol_noktasi_yok_ise_bos_doner(tmp_path):
    from run_matrix import kontrol_noktasi_yukle, _imza
    assert kontrol_noktasi_yukle(tmp_path / "yok.jsonl", _imza(1, 0.0)) == {}


def test_kontrol_noktasi_imza_uyusmazsa_durdurur(tmp_path):
    """Farklı --tekrar/--sicaklik ile devam etmek hücreleri karıştırırdı."""
    import json as _json
    from run_matrix import kontrol_noktasi_yukle, _imza

    yol = tmp_path / "m.ckpt.jsonl"
    yol.write_text(_json.dumps({"_tip": "imza", **_imza(3, 0.4)}) + "\n",
                   encoding="utf-8")

    with pytest.raises(SystemExit, match="farklı ayarlarla"):
        kontrol_noktasi_yukle(yol, _imza(tekrar=5, sicaklik=0.4))
