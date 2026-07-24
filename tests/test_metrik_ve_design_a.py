"""
Birim testleri — Gün 15/16 sertleştirmesi. Docker/model GEREKTİRMEZ.

Kapsam üç yeni yetenek:
  1) Bootstrap güven aralığı (metrik_ozet.bootstrap_ci) — istatistiksel motorun
     çekirdeği; determinizm, sıralama, sinyal-var/yok davranışı.
  2) Design A dil-başına tanımlayıcılar — EN koşumu İngilizce imza/ad kullanır,
     _en yoksa TR'ye düşer (prompt üretimi + harness fonksiyon adı seçimi).
  3) Veri seti DEĞİŞMEZİ — hiçbir prompt, imzasında bulunmayan bir tanımlayıcıyı
     backtick'lememeli. Bir kez düzeltilen "sızıntı yok" özelliğini kalıcı
     regresyon sigortasına çevirir (boyut değil, bozulma denetimi).
"""

import re

import pytest

import hata_taksonomisi
import metrik_ozet
import run_task
import task_io
from model_client.code_task import kod_prompt_olustur


# --- 1) Bootstrap güven aralığı ------------------------------------------
def _tax(ornek):
    """Eşleştirilmiş (en, tr) örnekten ortalama farkı — Türkçe vergisi istatistiği."""
    return (sum(e for e, _ in ornek) / len(ornek)
            - sum(t for _, t in ornek) / len(ornek))


def test_bootstrap_deterministik_seed():
    veri = [(1.0, 0.0), (1.0, 0.5), (0.5, 0.0), (1.0, 1.0), (0.0, 0.5)]
    a = metrik_ozet.bootstrap_ci(veri, _tax, seed=42)
    b = metrik_ozet.bootstrap_ci(veri, _tax, seed=42)
    assert a == b  # sabit seed => tekrarlanabilir aralık


def test_bootstrap_alt_ust_sirali():
    veri = [(1.0, 0.0), (0.8, 0.3), (0.6, 0.6), (0.9, 0.2)]
    lo, hi = metrik_ozet.bootstrap_ci(veri, _tax)
    assert lo <= hi


def test_bootstrap_guclu_sinyal_sifiri_dislar():
    # Her birimde en, tr'den 0.5 büyük => vergi kesinlikle pozitif, CI sıfırı dışlar.
    veri = [(1.0, 0.5)] * 12
    lo, hi = metrik_ozet.bootstrap_ci(veri, _tax)
    assert lo > 0.0


def test_bootstrap_sinyalsiz_sifiri_icerir():
    # Simetrik: yarısı en, yarısı tr lehine => ortalama 0, CI sıfırı içermeli.
    veri = [(1.0, 0.0), (0.0, 1.0)] * 6
    lo, hi = metrik_ozet.bootstrap_ci(veri, _tax)
    assert lo < 0.0 < hi


def test_bootstrap_sabit_istatistik_daralir():
    veri = [(0.7, 0.7)] * 8  # her örnekte tax=0
    lo, hi = metrik_ozet.bootstrap_ci(veri, _tax)
    assert lo == pytest.approx(0.0) and hi == pytest.approx(0.0)


def test_bootstrap_tek_birim_nan():
    import math
    lo, hi = metrik_ozet.bootstrap_ci([(1.0, 0.0)], _tax)
    assert math.isnan(lo) and math.isnan(hi)


# --- 2) Design A: dil-başına tanımlayıcılar ------------------------------
def _gorev_en():
    return {
        "prompt_tr": "TR problem", "prompt_en": "EN problem",
        "fonksiyon_imzasi": "def max_urun(fiyatlar: list, butce: int) -> int:",
        "fonksiyon_adi": "max_urun",
        "fonksiyon_imzasi_en": "def max_products(prices: list, budget: int) -> int:",
        "fonksiyon_adi_en": "max_products",
    }


def test_en_prompt_ingilizce_imzayi_kullanir():
    p = kod_prompt_olustur(_gorev_en(), "en")
    assert "def max_products(" in p
    assert "def max_urun(" not in p  # Türkçe imza EN koşumda sızmamalı


def test_tr_prompt_turkce_imzayi_kullanir():
    p = kod_prompt_olustur(_gorev_en(), "tr")
    assert "def max_urun(" in p
    assert "def max_products(" not in p


def test_en_imza_yoksa_turkceye_duser():
    g = {"prompt_tr": "x", "prompt_en": "y",
         "fonksiyon_imzasi": "def f(a: int) -> int:", "fonksiyon_adi": "f"}
    assert "def f(a: int) -> int:" in kod_prompt_olustur(g, "en")


def test_harness_en_kosumda_ingilizce_fonksiyon_adini_cagirir(monkeypatch):
    """gorevi_calistir, EN'de fonksiyon_adi_en'i sandbox'a geçirmeli."""
    yakalanan = {}

    def sahte_cozum(gorev, istemci, dil="tr"):
        return {"kod": "def x(): pass", "kullanim": None}

    def sahte_sandbox(kod, fonksiyon_adi, test_cases, karsilastirma=None):
        yakalanan["ad"] = fonksiyon_adi
        return {"gecti": True, "gecen": 1, "toplam": 1, "hata_tipi": None}

    monkeypatch.setattr(run_task, "modelden_cozum_al", sahte_cozum)
    monkeypatch.setattr(run_task, "sandboxta_calistir", sahte_sandbox)

    class SahteIstemci:
        model = "test"

    g = dict(_gorev_en(), id="trc_x", test_cases=[{"girdi": [], "beklenen": 1}])
    run_task.gorevi_calistir(g, SahteIstemci(), dil="en")
    assert yakalanan["ad"] == "max_products"
    run_task.gorevi_calistir(g, SahteIstemci(), dil="tr")
    assert yakalanan["ad"] == "max_urun"


def test_harness_en_adi_yoksa_turkceye_duser(monkeypatch):
    yakalanan = {}
    monkeypatch.setattr(run_task, "modelden_cozum_al",
                        lambda g, i, dil="tr": {"kod": "", "kullanim": None})
    monkeypatch.setattr(run_task, "sandboxta_calistir",
                        lambda kod, fonksiyon_adi, test_cases, karsilastirma=None:
                        yakalanan.update(ad=fonksiyon_adi) or
                        {"gecti": True, "gecen": 1, "toplam": 1, "hata_tipi": None})

    class SahteIstemci:
        model = "test"

    g = {"id": "t", "prompt_tr": "x", "prompt_en": "y",
         "fonksiyon_imzasi": "def f() -> int:", "fonksiyon_adi": "f",
         "test_cases": [{"girdi": [], "beklenen": 1}]}
    run_task.gorevi_calistir(g, SahteIstemci(), dil="en")
    assert yakalanan["ad"] == "f"  # _en yoksa TR ada düşer


# --- 2b) Şema kapısı: _en tutarlılığı ------------------------------------
def _temel_gorev():
    return {"id": "trc_001", "variant_type": "canonical", "canonical_id": "trc_001",
            "prompt_tr": "a", "prompt_en": "b",
            "fonksiyon_imzasi": "def f(x: int) -> int:", "fonksiyon_adi": "f",
            "referans_cozum": "def f(x):\n    return x", "kategori": "diziler",
            "zorluk": "kolay", "test_cases": [{"girdi": [1], "beklenen": 1}]}


def test_sema_en_tutarli_gorev_temiz():
    g = dict(_temel_gorev(), fonksiyon_imzasi_en="def g(y: int) -> int:",
             fonksiyon_adi_en="g")
    assert task_io.metadatayi_dogrula(g) == []


def test_sema_en_alani_eksikse_hata():
    g = dict(_temel_gorev(), fonksiyon_imzasi_en="def g(y: int) -> int:")  # ad yok
    hatalar = task_io.metadatayi_dogrula(g)
    assert any("birlikte bulunmalı" in h for h in hatalar)


def test_sema_en_ad_imzada_yoksa_hata():
    g = dict(_temel_gorev(), fonksiyon_imzasi_en="def g(y: int) -> int:",
             fonksiyon_adi_en="baska_ad")
    hatalar = task_io.metadatayi_dogrula(g)
    assert any("içermiyor" in h for h in hatalar)


def test_sema_en_alanlari_yoksa_geriye_uyumlu():
    assert task_io.metadatayi_dogrula(_temel_gorev()) == []


# --- 2c) Tanımlayıcı kapısı (Design A ortak gate — üreteçler de kullanır) ----
def _gorev_backtickli(ptr, pen):
    return {"id": "trc_x", "prompt_tr": ptr, "prompt_en": pen,
            "fonksiyon_imzasi": "def max_urun(fiyatlar: list, butce: int) -> int:",
            "fonksiyon_adi": "max_urun",
            "fonksiyon_imzasi_en": "def max_products(prices: list, budget: int) -> int:",
            "fonksiyon_adi_en": "max_products"}


def test_tanimlayici_kapisi_temiz():
    g = _gorev_backtickli("`butce` lira ver", "spend `budget`")
    assert task_io.tanimlayici_kapisi(g) == []


def test_tanimlayici_kapisi_en_sizinti_yakalar():
    # EN prompt Türkçe tanımlayıcı backtick'liyor -> yakalanmalı
    g = _gorev_backtickli("`butce` lira ver", "spend `butce`")
    hatalar = task_io.tanimlayici_kapisi(g)
    assert any("EN prompt `butce`" in h for h in hatalar)


def test_tanimlayici_kapisi_tr_sizinti_yakalar():
    # TR prompt İngilizce tanımlayıcı backtick'liyor -> yakalanmalı
    g = _gorev_backtickli("`budget` lira ver", "spend `budget`")
    hatalar = task_io.tanimlayici_kapisi(g)
    assert any("TR prompt `budget`" in h for h in hatalar)


def test_tanimlayici_kapisi_en_yoksa_tr_ye_duser():
    g = {"id": "t", "prompt_tr": "`x` ver", "prompt_en": "give `x`",
         "fonksiyon_imzasi": "def f(x: int) -> int:", "fonksiyon_adi": "f"}
    assert task_io.tanimlayici_kapisi(g) == []  # _en yok -> EN de TR imzaya bakar


# --- 3) Veri seti değişmezi: backtick tanımlayıcı sızıntısı yok ----------
def _imza_parametreleri(imza: str):
    return set(re.findall(r"[(,]\s*([A-Za-z_]\w*)\s*:", imza))


def _dataset():
    return [(g["id"], g) for g in task_io.gorevleri_yukle()]


@pytest.mark.parametrize("gid,gorev", _dataset(),
                         ids=lambda d: d if isinstance(d, str) else "")
def test_prompt_backtickleri_imzasiyla_uyumlu(gid, gorev):
    """TR/EN prompt'ta backtick'lenen her tanımlayıcı ilgili dilin imzasında olmalı.

    Bu, Design A'nın 'EN tamamen İngilizce, TR tamamen Türkçe' özelliğini kalıcı
    olarak kilitler: gelecekte biri prompt'a yabancı bir değişken adı sokarsa test
    kırılır. (Değerler/kod parçaları değil, yalın tanımlayıcı token'lar denetlenir.)
    """
    tr_ad = _imza_parametreleri(gorev["fonksiyon_imzasi"]) | {gorev["fonksiyon_adi"]}
    en_imza = gorev.get("fonksiyon_imzasi_en", gorev["fonksiyon_imzasi"])
    en_ad = _imza_parametreleri(en_imza) | {gorev.get("fonksiyon_adi_en",
                                                       gorev["fonksiyon_adi"])}
    for tok in re.findall(r"`([A-Za-z_]\w*)`", gorev["prompt_tr"]):
        assert tok in tr_ad, f"{gid}: TR prompt '{tok}' backtick'liyor ama TR imzada yok"
    for tok in re.findall(r"`([A-Za-z_]\w*)`", gorev["prompt_en"]):
        assert tok in en_ad, f"{gid}: EN prompt '{tok}' backtick'liyor ama EN imzada yok"


# --- 4) Hata taksonomisi sınıflandırıcısı --------------------------------
def test_taksonomi_gecen_ornek():
    assert hata_taksonomisi.sinifla({"gecti": True, "hata_tipi": None}) == "gecti"


def test_taksonomi_sert_hata_korunur():
    assert hata_taksonomisi.sinifla(
        {"gecti": False, "hata_tipi": "syntax"}) == "syntax"
    assert hata_taksonomisi.sinifla(
        {"gecti": False, "hata_tipi": "eksik_fonksiyon"}) == "eksik_fonksiyon"


def test_taksonomi_null_hata_yanlis_mantik_olur():
    # Kör noktanın kalbi: kod çalıştı ama testleri geçemedi (hata_tipi=null).
    assert hata_taksonomisi.sinifla(
        {"gecti": False, "hata_tipi": None}) == "yanlis_mantik"


def test_taksonomi_sert_olmayan_etiket_mantiga_duser():
    # Cell-düzeyi hata_tipi bilinmeyen/yumuşak bir değerse yanlış_mantık sayılır.
    assert hata_taksonomisi.sinifla(
        {"gecti": False, "hata_tipi": "mantik"}) == "yanlis_mantik"
