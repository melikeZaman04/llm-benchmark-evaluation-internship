"""
Birim testleri — agent_factory (Düzlem 1: Yaratıcı Ajan Fabrikası).

Docker GEREKTİRMEZ, `claude` CLI GEREKTİRMEZ (subprocess mock'lanır) — hızlı,
ücretsiz, CI'da güvenle koşar. Gerçek `claude` çağrısını ve oracle guardrail
entegrasyonunu test etmez; onun için bkz. test_agent_factory_integration.py
(opsiyonel, gerçek CLI + gerçek maliyet gerektirir).
"""

import json
import subprocess

import pytest

from agent_factory.client import ajan_cagir, AjanCagriHatasi
from agent_factory.mutator import _gorev_metni_olustur, varyant_uret
import agent_factory.mutator as mutator_modul
from agent_factory.translator import promptlari_cevir
import agent_factory.translator as translator_modul
import agent_factory.parametric as parametric_modul


def _sahte_calisan(stdout: str = "", returncode: int = 0, stderr: str = ""):
    """subprocess.run çağrısını taklit eden bir tamamlanmış-süreç nesnesi üretir."""
    def _calistir(*args, **kwargs):
        return subprocess.CompletedProcess(args=args, returncode=returncode,
                                            stdout=stdout, stderr=stderr)
    return _calistir


SEMA = {"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]}


# --- ajan_cagir: başarı yolu ----------------------------------------------
def test_ajan_cagir_basarili_yapilandirilmis_veri_doner(monkeypatch):
    zarf = json.dumps({
        "is_error": False,
        "structured_output": {"x": "deger"},
        "total_cost_usd": 0.05,
        "usage": {"cache_read_input_tokens": 100, "cache_creation_input_tokens": 0},
        "duration_ms": 1234,
    })
    monkeypatch.setattr(subprocess, "run", _sahte_calisan(stdout=zarf))
    sonuc = ajan_cagir("persona", "gorev metni", SEMA)
    assert sonuc["veri"] == {"x": "deger"}
    assert sonuc["maliyet_usd"] == 0.05
    assert sonuc["onbellek_okuma_tok"] == 100


# --- ajan_cagir: hata yolları ----------------------------------------------
def test_ajan_cagir_is_error_true_hata_firlatir(monkeypatch):
    zarf = json.dumps({"is_error": True, "result": "bir sorun oldu"})
    monkeypatch.setattr(subprocess, "run", _sahte_calisan(stdout=zarf))
    with pytest.raises(AjanCagriHatasi, match="is_error"):
        ajan_cagir("persona", "gorev", SEMA)


def test_ajan_cagir_yapilandirilmis_veri_eksikse_hata_firlatir(monkeypatch):
    zarf = json.dumps({"is_error": False, "result": "duz metin, sema uymadi"})
    monkeypatch.setattr(subprocess, "run", _sahte_calisan(stdout=zarf))
    with pytest.raises(AjanCagriHatasi, match="structured_output"):
        ajan_cagir("persona", "gorev", SEMA)


def test_ajan_cagir_gecersiz_json_hata_firlatir(monkeypatch):
    monkeypatch.setattr(subprocess, "run", _sahte_calisan(stdout="bu json degil"))
    with pytest.raises(AjanCagriHatasi, match="JSON değil"):
        ajan_cagir("persona", "gorev", SEMA)


def test_ajan_cagir_sifir_disi_donus_kodu_hata_firlatir(monkeypatch):
    monkeypatch.setattr(subprocess, "run",
                         _sahte_calisan(returncode=1, stderr="komut basarisiz"))
    with pytest.raises(AjanCagriHatasi, match="komut basarisiz"):
        ajan_cagir("persona", "gorev", SEMA)


def test_ajan_cagir_zaman_asimi_hata_firlatir(monkeypatch):
    def _zaman_asimi(*a, **k):
        raise subprocess.TimeoutExpired(cmd="claude", timeout=120)
    monkeypatch.setattr(subprocess, "run", _zaman_asimi)
    with pytest.raises(AjanCagriHatasi, match="zaman aşımı"):
        ajan_cagir("persona", "gorev", SEMA)


def test_ajan_cagir_claude_kurulu_degilse_hata_firlatir(monkeypatch):
    def _bulunamadi(*a, **k):
        raise FileNotFoundError()
    monkeypatch.setattr(subprocess, "run", _bulunamadi)
    with pytest.raises(AjanCagriHatasi, match="bulunamadı"):
        ajan_cagir("persona", "gorev", SEMA)


# --- Mutator: görev metni üretimi (saf fonksiyon) --------------------------
def test_gorev_metni_tum_alanlari_icerir():
    kanonik = {
        "id": "trc_999", "prompt_tr": "TR_METIN", "prompt_en": "EN_TEXT",
        "fonksiyon_imzasi": "def f(x: int) -> int:", "fonksiyon_adi": "f",
        "referans_cozum": "def f(x):\n    return x\n",
        "sablon": {"nesne": ["a", "b"]},
    }
    metin = _gorev_metni_olustur(kanonik)
    assert "trc_999" in metin and "TR_METIN" in metin and "EN_TEXT" in metin
    assert "def f(x):" in metin and '"nesne"' in metin


# --- Mutator: varyant birleştirme + guardrail entegrasyonu (mock'lu) ------
def test_varyant_uret_basarili_gorev_birlestirir(monkeypatch):
    kanonik = {
        "id": "trc_001", "kategori": "diziler", "zorluk": "kolay",
        "prompt_tr": "eski_tr", "prompt_en": "eski_en",
        "fonksiyon_imzasi": "def eski(x):", "fonksiyon_adi": "eski",
        "referans_cozum": "def eski(x):\n    return x\n",
        "test_cases": [{"girdi": [1], "beklenen": 1}],
    }
    uretilen_veri = {
        "prompt_tr": "yeni_tr", "prompt_en": "yeni_en",
        "fonksiyon_imzasi": "def yeni(x):", "fonksiyon_adi": "yeni",
        "referans_cozum": "def yeni(x):\n    return x",  # kasıtlı: sonda \n yok
    }
    monkeypatch.setattr(mutator_modul, "ajan_cagir",
                         lambda *a, **k: {"veri": uretilen_veri, "maliyet_usd": 0.01})
    monkeypatch.setattr(mutator_modul, "gorevi_dogrula",
                         lambda gorev: {"gecerli": True, "gecen": 1, "toplam": 1,
                                        "hata_tipi": None})

    sonuc = varyant_uret(kanonik, "trc_100")

    assert sonuc["id"] == "trc_100"
    assert sonuc["ebeveyn"] == "trc_001"
    assert sonuc["kaynak"] == "mutasyon"
    assert sonuc["kategori"] == "diziler"          # kanonikten kopyalandı
    assert sonuc["test_cases"] == kanonik["test_cases"]  # DEĞİŞTİRİLMEDEN kopyalandı
    assert sonuc["fonksiyon_adi"] == "yeni"         # Mutator'dan geldi
    assert sonuc["referans_cozum"].endswith("\n")   # sondaki \n normalize edildi
    assert sonuc["_maliyet_usd"] == 0.01


def test_varyant_uret_guardrail_reddederse_hata_firlatir(monkeypatch):
    kanonik = {
        "id": "trc_001", "kategori": "diziler", "zorluk": "kolay",
        "prompt_tr": "t", "prompt_en": "e",
        "fonksiyon_imzasi": "def f(x):", "fonksiyon_adi": "f",
        "referans_cozum": "def f(x):\n    return x\n",
        "test_cases": [{"girdi": [1], "beklenen": 1}],
    }
    uretilen_veri = {
        "prompt_tr": "t2", "prompt_en": "e2",
        "fonksiyon_imzasi": "def f2(x):", "fonksiyon_adi": "f2",
        "referans_cozum": "def f2(x):\n    return x + 1\n",  # bozuk mantık
    }
    monkeypatch.setattr(mutator_modul, "ajan_cagir",
                         lambda *a, **k: {"veri": uretilen_veri, "maliyet_usd": 0.01})
    monkeypatch.setattr(mutator_modul, "gorevi_dogrula",
                         lambda gorev: {"gecerli": False, "gecen": 0, "toplam": 1,
                                        "hata_tipi": "mantik"})

    with pytest.raises(AjanCagriHatasi, match="Guardrail reddetti"):
        varyant_uret(kanonik, "trc_100")


def test_translator_kod_alanlarini_aynen_korur(monkeypatch):
    gorev = {"prompt_tr": "eski tr", "prompt_en": "old en",
             "fonksiyon_imzasi": "def f(x):", "fonksiyon_adi": "f",
             "referans_cozum": "def f(x):\n    return x\n",
             "test_cases": [{"girdi": [1], "beklenen": 1}]}
    monkeypatch.setattr(translator_modul, "ajan_cagir",
                        lambda *a, **k: {"veri": {"prompt_tr": "yeni tr", "prompt_en": "new en"},
                                        "maliyet_usd": 0.01})
    sonuc = promptlari_cevir(gorev)
    assert sonuc["prompt_tr"] == "yeni tr"
    assert sonuc["prompt_en"] == "new en"
    assert sonuc["referans_cozum"] == gorev["referans_cozum"]
    assert sonuc["test_cases"] == gorev["test_cases"]


def _parametrik_kanonik():
    return {"id": "trc_001", "kategori": "diziler", "zorluk": "kolay",
            "kaynak": "ozgun", "canonical_id": "trc_001",
            "variant_type": "canonical",
            "prompt_tr": "Bir markette ürünlerin fiyatları verilir.",
            "prompt_en": "In a market, product prices are given.",
            "fonksiyon_imzasi": "def f(x: list[int]) -> int:",
            "fonksiyon_adi": "f",
            "referans_cozum": "def f(x):\n    return x\n",
            "test_cases": [{"girdi": [1], "beklenen": 1}],
            "sablon": {"market": ["market", "kütüphane"],
                       "urun": ["ürün", "kitap"]}}


def _sahte_cevirici(tr: str, en: str):
    """Translator yerine geçen sahte: yalnızca prompt alanlarını değiştirir."""
    def cevir(gorev, yonerge=None):
        sonuc = dict(gorev)
        sonuc.update(prompt_tr=tr, prompt_en=en, _maliyet_usd=0.01)
        return sonuc
    return cevir


def test_parametrik_varyant_kodu_ve_testleri_korur(monkeypatch):
    kanonik = _parametrik_kanonik()
    monkeypatch.setattr(parametric_modul, "gorevi_dogrula",
                        lambda _: {"gecerli": True, "gecen": 1, "toplam": 1})

    sonuc = parametric_modul.varyantlari_uret(
        kanonik, ["trc_100"],
        cevirici=_sahte_cevirici("Bir kütüphanede kitapların sayfa sayıları verilir.",
                                 "In a library, book page counts are given."))

    varyant = sonuc[0]
    assert varyant["id"] == "trc_100"
    assert varyant["variant_type"] == "parametric_story"
    assert varyant["ebeveyn"] == "trc_001"
    assert varyant["canonical_id"] == "trc_001"
    # Kod ve testler ebeveynden byte-byte kopyalanır.
    assert varyant["referans_cozum"] == kanonik["referans_cozum"]
    assert varyant["test_cases"] == kanonik["test_cases"]
    assert varyant["fonksiyon_imzasi"] == kanonik["fonksiyon_imzasi"]
    # sablon varyanta TAŞINMAZ (varyanttan varyant türetilmesin).
    assert "sablon" not in varyant


def test_parametrik_iki_dili_birlikte_gunceller(monkeypatch):
    """B1 regresyonu: prompt_en güncellenmezse TR/EN paritesi kırılır."""
    kanonik = _parametrik_kanonik()
    monkeypatch.setattr(parametric_modul, "gorevi_dogrula",
                        lambda _: {"gecerli": True, "gecen": 1, "toplam": 1})

    sonuc = parametric_modul.varyantlari_uret(
        kanonik, ["trc_100"],
        cevirici=_sahte_cevirici("yeni TR metni", "new EN text"))

    assert sonuc[0]["prompt_tr"] != kanonik["prompt_tr"]
    assert sonuc[0]["prompt_en"] != kanonik["prompt_en"]


def test_parametrik_yonerge_sablon_esleşmelerini_icerir():
    sablon = {"market": ["market", "kütüphane"], "urun": ["ürün", "kitap"]}
    yonerge = parametric_modul._yonerge_olustur(
        sablon, {"market": "kütüphane", "urun": "kitap"})
    assert '"market" yerine "kütüphane"' in yonerge
    assert '"ürün" yerine "kitap"' in yonerge


def test_parametrik_kod_alanina_dokunulursa_reddedilir(monkeypatch):
    """Değişmezlik kapısı: çevirici kod alanını bozarsa varyant reddedilir."""
    kanonik = _parametrik_kanonik()
    monkeypatch.setattr(parametric_modul, "gorevi_dogrula",
                        lambda _: {"gecerli": True, "gecen": 1, "toplam": 1})

    def bozuk_cevirici(gorev, yonerge=None):
        sonuc = dict(gorev)
        sonuc.update(prompt_tr="yeni", prompt_en="new",
                     referans_cozum="def f(x):\n    return x + 1\n")
        return sonuc

    with pytest.raises(AjanCagriHatasi, match="kod alanlarına dokundu"):
        parametric_modul.varyantlari_uret(kanonik, ["trc_100"],
                                          cevirici=bozuk_cevirici)


def test_parametrik_guardrail_reddederse_hata_firlatir(monkeypatch):
    kanonik = _parametrik_kanonik()
    monkeypatch.setattr(parametric_modul, "gorevi_dogrula",
                        lambda _: {"gecerli": False, "gecen": 0, "toplam": 1})

    with pytest.raises(AjanCagriHatasi, match="guardrail reddetti"):
        parametric_modul.varyantlari_uret(
            kanonik, ["trc_100"],
            cevirici=_sahte_cevirici("yeni TR", "new EN"))


def test_parametrik_asiri_uzun_metin_reddedilir(monkeypatch):
    """Uzunluk confound'u: varyant metni ebeveyninin katları olamaz."""
    kanonik = _parametrik_kanonik()
    monkeypatch.setattr(parametric_modul, "gorevi_dogrula",
                        lambda _: {"gecerli": True, "gecen": 1, "toplam": 1})
    cok_uzun = "Bir kitapçıda kitapların fiyatları verilir. " * 20

    with pytest.raises(AjanCagriHatasi, match="aşırı uzun"):
        parametric_modul.varyantlari_uret(
            kanonik, ["trc_100"],
            cevirici=_sahte_cevirici(cok_uzun, cok_uzun))


def test_kombinasyon_sayisi_kanonigi_haric_tutar():
    # 2x2 sablon -> 4 kombinasyon, biri kanoniğin kendisi -> 3 varyant
    assert parametric_modul.kombinasyon_sayisi(_parametrik_kanonik()) == 3
    assert parametric_modul.kombinasyon_sayisi({"sablon": {}}) == 0
