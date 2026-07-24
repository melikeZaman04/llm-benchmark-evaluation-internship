"""
Translator Ajanı — Düzlem 1'in ikinci ajanı: prompt metinlerini üretir.

İki modda çalışır, ikisi de AYNI persona ile (persona sabit kalmalı, yoksa
prompt önbelleklemesi bozulur — bkz. client.py maliyet notu):

1. **Uyumlama (yönergesiz).** Var olan prompt_tr/prompt_en çiftini alır, ikisinin
   BİREBİR aynı problemi anlattığından emin olur. Senaryoyu korur.
2. **Senaryo değişimi (yönergeli).** Bir kelime-eşleme yönergesi verilirse
   senaryoyu yeni bağlama taşır ve metni HER İKİ DİLDE de yeniden kurar.
   `parametric.py` bu modu kullanır.

Neden bu ajan parametrik varyantın da içinde? Çünkü parametrik varyantın iki
zor tarafı var ve ikisi de saf kodla güvenilir çözülmüyor:
  - **TR/EN paritesi.** Yalnızca Türkçe metni değiştirip İngilizceyi olduğu
    gibi bırakmak, `acc(en) − acc(tr)` metriğini sessizce çöpe çevirir: iki
    dilde FARKLI problem sorulmuş olur.
  - **Türkçe ek uyumu.** "market" -> "kütüphane" ikamesi "markette" ifadesini
    "kütüphanete" yapar; doğrusu "kütüphanede"dir. Ünsüz yumuşaması ve ünlü
    uyumunu düz metin ikamesiyle çözmek kırılgandır ve TÜRKÇE bir benchmark'ta
    bozuk Türkçe üretmek ölçülen şeyi doğrudan kirletir.

Determinizm notu: bu ajan veri setini ÜRETİM anında bir kez çalıştırır; üretilen
görevler git'e commit edilip DONDURULUR. Ölçüm (run_matrix) sırasında hiçbir
ajan çağrılmaz, dolayısıyla benchmark'ın kendisi deterministik kalır.

Sınır — dürüstçe: oracle bu ajanın çıktısını doğrulayamaz. Kod ve test_cases
değişmediği için oracle tanım gereği geçer; prompt metninin anlam doğruluğu
mekanik olarak denetlenemez, insan gözden geçirmesi gerektirir. Mekanik güvence
yalnızca `task_io.degismezleri_dogrula` ile kod/test alanlarının hiç
kıpırdamadığıdır.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent_factory.client import ajan_cagir, AjanCagriHatasi  # noqa: E402

PERSONA = """ROL:
Sen TR-CodeEval benchmark'ının Prompt Uyum Ajanısın (Translator). Tek işin bir programlama görevinin prompt_tr ve prompt_en alanlarını üretmek ve bu ikisinin BİREBİR AYNI problemi anlattığından emin olmaktır.

DOKUNAMAYACAKLARIN:
- Algoritma, sayılar, kısıtlar, sınır durumları, fonksiyon imzası, fonksiyon adı, test_cases. Bunlar sana yalnızca BAĞLAM olarak verilir; çıktında yer almazlar ve değişmezler.

TANIMLAYICI DİLİ (Design A — KESİN KURAL):
- prompt_tr içinde backtick'li tanımlayıcılar TÜRKÇE imzadaki (fonksiyon_imzasi / fonksiyon_adi) adlar olmalı; prompt_en içinde İNGİLİZCE imzadaki (fonksiyon_imzasi_en / fonksiyon_adi_en) adlar olmalı.
- Yani AYNI parametre Türkçe metinde Türkçe adıyla (ör. `butce`), İngilizce metinde İngilizce adıyla (ör. `budget`) backtick'lenir. Bir dilin tanımlayıcısını diğer dilin metnine ASLA taşıma. EN sütunu tamamen İngilizce, TR tamamen Türkçe olmalı.

DİL KALİTESİ (EN ÖNEMLİSİ):
- prompt_tr KUSURSUZ ve DOĞAL Türkçe olmalı. Ek uyumu (ünsüz yumuşaması, ünlü uyumu, kaynaştırma) mutlaka doğru olmalı: "kütüphanete" DEĞİL "kütüphanede"; "kitapı" DEĞİL "kitabı".
- prompt_en doğal İngilizce olmalı — kelimesi kelimesine çeviri değil, o dilde nasıl yazılırdı öyle.
- İki metin aynı bilgiyi, aynı kısıtları ve aynı sınır durumlarını içermeli. Birinde olup diğerinde olmayan bir ayrıntı KALMAMALI.

SENARYO DEĞİŞİMİ:
Sana açık bir "DEĞİŞİM YÖNERGESİ" verilirse: oradaki kelimeler bir TOHUM'dur, sözlük ikamesi DEĞİLDİR. O tohumun etrafında SOMUT ve gerçekçi bir senaryo kur — kim, nerede, neyi ölçüyor/sayıyor belli olsun — ve metni her iki dilde de sıfırdan, doğal biçimde yeniden yaz.
Tohum soyutsa ("sayı", "değer", "adım" gibi) onu MUTLAKA somut bir bağlama oturt. "n adım miktarı veriliyor, n adımın faktöriyelini döndür" gibi yapay, hikâyesi olmayan ifadeler ÜRETME — bu, kelimeyi değiştirip problemi olduğu gibi bırakmaktır ve benchmark açısından değersizdir.
Yeni senaryo kendi içinde anlamca tutarlı olmalı — parasal olmayan bir kısıtı (ağırlık, kapasite, süre) parasal bir çerçeveye zorlama; bağlama uygun yeni bir kısıt anlamı kur.
Problemin girdi-çıktı davranışı, sayıları ve sınır durumları AYNEN korunur; değişen YALNIZCA hikâyedir.

UZUNLUK (ÖLÇÜM İÇİN KRİTİK):
Yeni metin, sana verilen özgün metinle KABACA AYNI uzunlukta olmalı — en fazla iki katı. Senaryoyu bir-iki cümlede kur, gereksiz betimleme ve sahne kurgusu yapma. Bu bir estetik tercih değil ölçüm zorunluluğudur: varyant metni özgününden belirgin uzun olursa, başarı düşüşünün ezberin kırılmasından mı yoksa metnin uzamasından mı geldiği ayırt edilemez hale gelir.

Yönerge verilmezse: senaryoyu KORU, yalnızca iki dili birbiriyle tam uyumlu hale getir.

Yalnızca istenen JSON şemasına uyan çıktı döndür."""

JSON_SEMASI = {
    "type": "object",
    "properties": {
        "prompt_tr": {"type": "string"},
        "prompt_en": {"type": "string"},
    },
    "required": ["prompt_tr", "prompt_en"],
}


def _gorev_metni_olustur(gorev: dict, yonerge: str | None = None) -> str:
    parcalar = [
        f"prompt_tr: {gorev['prompt_tr']!r}",
        f"prompt_en: {gorev['prompt_en']!r}",
        f"fonksiyon_imzasi (TR tanımlayıcılar): {gorev['fonksiyon_imzasi']!r}",
        f"fonksiyon_adi (TR): {gorev['fonksiyon_adi']!r}",
        f"fonksiyon_imzasi_en (EN tanımlayıcılar): "
        f"{gorev.get('fonksiyon_imzasi_en', gorev['fonksiyon_imzasi'])!r}",
        f"fonksiyon_adi_en (EN): "
        f"{gorev.get('fonksiyon_adi_en', gorev['fonksiyon_adi'])!r}",
    ]
    if yonerge:
        parcalar.append(f"\nDEĞİŞİM YÖNERGESİ:\n{yonerge}")
        parcalar.append("\nYönergeyi uygulayarak iki prompt alanını yeniden üret.")
    else:
        parcalar.append("\nSenaryoyu koruyarak iki prompt alanını karşılıklı uyumla.")
    return "\n".join(parcalar)


def promptlari_cevir(gorev: dict, yonerge: str | None = None) -> dict:
    """
    Görevin prompt alanlarını üretir; diğer TÜM alanları aynen korur.

    yonerge: verilirse senaryo değişimi modu (bkz. modül docstring'i); None
             ise yalnızca TR/EN uyumlaması yapılır.
    """
    sonuc = ajan_cagir(PERSONA, _gorev_metni_olustur(gorev, yonerge), JSON_SEMASI)
    veri = sonuc["veri"]
    if not veri["prompt_tr"].strip() or not veri["prompt_en"].strip():
        raise AjanCagriHatasi("Translator boş prompt üretti")

    cevrilmis = dict(gorev)
    cevrilmis.update(prompt_tr=veri["prompt_tr"], prompt_en=veri["prompt_en"])
    cevrilmis["_maliyet_usd"] = sonuc.get("maliyet_usd")
    return cevrilmis
