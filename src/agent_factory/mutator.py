"""
Mutator Ajanı — Düzlem 1'in (Yaratıcı Ajan Fabrikası) ilk fiili ajanı.

Zaten oracle-doğrulanmış bir kanonik görevi YENİ bir senaryoya (bağlama)
uyarlar — algoritmayı DEĞİL. Ürettiği HER varyant, veri setine yazılmadan
önce mutlaka oracle guardrail'inden (oracle.task_validator.gorevi_dogrula)
geçmek zorundadır; geçemeyen varyant reddedilir ve veri setine hiç girmez.

Persona ve akış, 2026-07-20/21 pilot testleriyle doğrulandı: 7/7 başarılı
deneme (özyinelemeli fonksiyonlar, çok-parametreli fonksiyonlar, ince/kalın
sablon'lar, farklı sablon kombinasyonları dahil). Detay için
docs/staj_defteri_gunlukleri.md.

Tasarım kararı: test_cases Mutator'a HİÇ gösterilmez — kanonik görevden
DEĞİŞTİRİLMEDEN kopyalanır. Böylece Mutator'ın "yanlışlıkla bir sayıyı
değiştirme" riski sıfırdır; tek riski isimlendirme sırasında mantığı
bozmaktır, ve bunu oracle guardrail'i doğrudan test eder.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent_factory.client import ajan_cagir, AjanCagriHatasi  # noqa: E402
from oracle.task_validator import gorevi_dogrula  # noqa: E402
from task_io import metadatayi_dogrula, tanimlayici_kapisi  # noqa: E402

PERSONA = """ROL:
Sen TR-CodeEval benchmark'ının Hikaye Mutasyon Ajanısın (Mutator). Tek işin: sana verilen ZATEN DOĞRULANMIŞ bir programlama görevini, YENİ bir senaryoya (bağlama) uyarlamak — algoritmayı değil.

Sana bir kanonik görevin şu alanları verilecek: prompt_tr, prompt_en, fonksiyon_imzasi (Türkçe tanımlayıcılar), fonksiyon_adi (Türkçe), fonksiyon_imzasi_en (İngilizce tanımlayıcılar), fonksiyon_adi_en (İngilizce), referans_cozum, sablon (varsa).

YAPABİLECEKLERİN:
- Tutarlı, tek bir yeni senaryo yaz (prompt_tr, prompt_en) — sablon'dan kelime seçerek veya kendi uygun bir bağlam kurarak.
- Fonksiyon adını ve parametre adlarını yeni senaryoya uyarla — HEM Türkçe (fonksiyon_imzasi, fonksiyon_adi) HEM İngilizce (fonksiyon_imzasi_en, fonksiyon_adi_en) sürümünü üret.
- referans_cozum'u YENİ Türkçe isimlerle (fonksiyon_adi / fonksiyon_imzasi'ndaki) yeniden yaz.

TANIMLAYICI DİLİ (Design A — KESİN KURAL):
- İki paralel imza üret: fonksiyon_imzasi TÜRKÇE tanımlayıcılar taşır (ör. `en_fazla_kitap(sayfa_sayilari, kapasite)`), fonksiyon_imzasi_en aynı yapının İNGİLİZCE gizlenmiş karşılığıdır (ör. `max_books(page_counts, capacity)`). Parametre SIRASI ve tipleri iki imzada birebir aynı olmalı.
- prompt_tr içindeki backtick'li tanımlayıcılar TÜRKÇE (fonksiyon_imzasi'ndaki) adlar; prompt_en içindekiler İNGİLİZCE (fonksiyon_imzasi_en'deki) adlar olmalı. EN metni tamamen İngilizce, TR tamamen Türkçe.
- referans_cozum YALNIZCA Türkçe adı (fonksiyon_adi) kullanır; fonksiyon_adi_en yalnız İngilizce prompt ve ölçüm içindir, çözümde geçmez.

KESİN KURAL — SAF İSİM DEĞİŞİMİ:
referans_cozum'u yeniden yazarken tek yaptığın şey İSİM DEĞİŞTİRMEK olmalı. Kontrol akışı, işlem sırası, operatörler, karşılaştırmalar BİREBİR AYNI kalmalı. Özyinelemeli bir fonksiyonsa, fonksiyonun kendi içinde kendini çağırdığı satırı da yeni Türkçe adla güncellemen ŞART.

DOKUNAMAYACAKLARIN:
- test_cases'e hiç erişimin yok, onları görmeyeceksin bile.

TUTARLILIK (EN ÖNEMLİSİ):
Yeni senaryo anlamca kendi içinde tutarlı olmalı. Parasal olmayan bir kısıtı (ağırlık, kapasite, zaman) parasal bir çerçeveye (bütçe, satın alma) zorlama — mantığa uygun yeni bir kısıt anlamı kur ve bunu hem metinde hem isimlerde tutarlı tut.

Yalnızca istenen JSON şemasına uyan çıktı döndür."""

JSON_SEMASI = {
    "type": "object",
    "properties": {
        "prompt_tr": {"type": "string"},
        "prompt_en": {"type": "string"},
        "fonksiyon_imzasi": {"type": "string"},
        "fonksiyon_adi": {"type": "string"},
        "fonksiyon_imzasi_en": {"type": "string"},
        "fonksiyon_adi_en": {"type": "string"},
        "referans_cozum": {"type": "string"},
    },
    "required": ["prompt_tr", "prompt_en", "fonksiyon_imzasi", "fonksiyon_adi",
                 "fonksiyon_imzasi_en", "fonksiyon_adi_en", "referans_cozum"],
}


def _gorev_metni_olustur(kanonik: dict) -> str:
    sablon = kanonik.get("sablon", {})
    return (
        f"KANONİK GÖREV ({kanonik['id']}):\n"
        f"prompt_tr: {kanonik['prompt_tr']!r}\n"
        f"prompt_en: {kanonik['prompt_en']!r}\n"
        f"fonksiyon_imzasi: {kanonik['fonksiyon_imzasi']!r}\n"
        f"fonksiyon_adi: {kanonik['fonksiyon_adi']!r}\n"
        f"fonksiyon_imzasi_en: "
        f"{kanonik.get('fonksiyon_imzasi_en', kanonik['fonksiyon_imzasi'])!r}\n"
        f"fonksiyon_adi_en: "
        f"{kanonik.get('fonksiyon_adi_en', kanonik['fonksiyon_adi'])!r}\n"
        f"referans_cozum:\n```python\n{kanonik['referans_cozum']}```\n"
        f"sablon: {json.dumps(sablon, ensure_ascii=False)}\n"
    )


def varyant_uret(kanonik: dict, yeni_id: str) -> dict:
    """
    Bir kanonik görevden TEK bir mutasyon varyantı üretir ve guardrail'den
    geçirir.

    Başarılıysa tam görev sözlüğünü (`_maliyet_usd` iç alanıyla birlikte)
    döner. Ajan çağrısı başarısız olursa VEYA üretilen varyant oracle
    guardrail'inden geçemezse AjanCagriHatasi fırlatır — çağıran bunu
    "reddedildi" olarak ele almalı, veri setine YAZMAMALI.
    """
    gorev_metni = _gorev_metni_olustur(kanonik)
    sonuc = ajan_cagir(PERSONA, gorev_metni, JSON_SEMASI)
    uretilen = sonuc["veri"]

    yeni_gorev = {
        "id": yeni_id,
        "kategori": kanonik["kategori"],
        "zorluk": kanonik["zorluk"],
        "kaynak": "mutasyon",
        "ebeveyn": kanonik["id"],
        "canonical_id": kanonik.get("canonical_id", kanonik["id"]),
        "variant_type": "story_mutation",
        "prompt_tr": uretilen["prompt_tr"],
        "prompt_en": uretilen["prompt_en"],
        "fonksiyon_imzasi": uretilen["fonksiyon_imzasi"],
        "fonksiyon_adi": uretilen["fonksiyon_adi"],
        "fonksiyon_imzasi_en": uretilen["fonksiyon_imzasi_en"],
        "fonksiyon_adi_en": uretilen["fonksiyon_adi_en"],
        "referans_cozum": uretilen["referans_cozum"].rstrip("\n") + "\n",
        "test_cases": kanonik["test_cases"],
    }
    if kanonik.get("karsilastirma"):
        yeni_gorev["karsilastirma"] = kanonik["karsilastirma"]

    # Design-A kapısı (oracle'dan önce, ucuz mekanik denetim): şema + EN
    # tutarlılığı + prompt backtick'lerinin doğru dilde olması.
    sema_hatalari = metadatayi_dogrula(yeni_gorev) + tanimlayici_kapisi(yeni_gorev)
    if sema_hatalari:
        raise AjanCagriHatasi(
            f"Design-A kapısı reddetti ({yeni_id} <- {kanonik['id']}): "
            + "; ".join(sema_hatalari)
        )

    dogrulama = gorevi_dogrula(yeni_gorev)
    if not dogrulama["gecerli"]:
        raise AjanCagriHatasi(
            f"Guardrail reddetti ({yeni_id} <- {kanonik['id']}): "
            f"{dogrulama['gecen']}/{dogrulama['toplam']} test, "
            f"hata={dogrulama['hata_tipi']}"
        )

    yeni_gorev["_maliyet_usd"] = sonuc["maliyet_usd"]
    return yeni_gorev
