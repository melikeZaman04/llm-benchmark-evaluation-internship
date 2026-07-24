"""
Parametrik Varyant Üreteci — kanonik görevin `sablon` alanından hikâye ailesi.

Amaç, veri setinin EZBER-DAYANIKLILIĞI eksenini beslemek: aynı algoritmanın
farklı senaryolarda sorulması, modelin problemi gerçekten anlayıp anlamadığını
(yoksa ezberden mi geldiğini) ölçmeyi sağlar — `acc(orijinal) − acc(varyant)`.

Akış:

    sablon kombinasyonu          (market->kütüphane, ürün->kitap, ...)
            │
            ▼  DEĞİŞİM YÖNERGESİ olarak Translator ajanına verilir
    Translator                    temiz prompt_tr + eşleşen prompt_en
            │
            ▼  mekanik kapı 1
    degismezleri_dogrula          kod/test alanları byte-byte aynı mı?
            │
            ▼  mekanik kapı 2
    uzunluk_kapisi                metin ebeveyninden aşırı uzamış mı?
            │
            ▼  oracle kapısı
    gorevi_dogrula                referans çözüm testleri geçiyor mu?

Neden metin ikamesi (regex) YOK? İlk tasarımda sablon kelimeleri prompt_tr
içinde düz regex ile değiştiriliyordu. İki kusuru vardı ve ikisi de veri
setini sessizce bozuyordu:
  - prompt_en hiç değişmiyordu -> TR ve EN'de FARKLI problem soruluyordu,
    bu da `acc(en) − acc(tr)` metriğini anlamsız kılıyordu;
  - Türkçe ek uyumu yapılamıyordu -> "markette" ikamesi "kütüphanete"
    üretiyordu (doğrusu "kütüphanede").
Bu yüzden ikame işi metin düzeyinde değil, ajan düzeyinde yapılır: sablon
seçimi bir YÖNERGE'ye çevrilip Translator'a verilir, o da iki dili birlikte
yeniden kurar. Ayrıntı: agent_factory/translator.py.

Sınır — dürüstçe: `gorevi_dogrula` bu eksende TAUTOLOJİye yakındır; kod ve
test_cases hiç değişmediği için geçmesi beklenir. Gerçek mekanik güvence
`degismezleri_dogrula`dır (kodun kıpırdamadığını ispatlar). Oracle yine de
çağrılır, çünkü üreteç ileride yanlışlıkla kod alanına dokunacak biçimde
değiştirilirse bu regresyonu yakalayan ikinci settir. Prompt metninin ANLAM
doğruluğu hiçbiri tarafından denetlenemez; insan gözden geçirmesi gerekir.
"""

from __future__ import annotations

from itertools import product
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from agent_factory.client import AjanCagriHatasi  # noqa: E402
from agent_factory.translator import promptlari_cevir  # noqa: E402
from oracle.task_validator import gorevi_dogrula  # noqa: E402
from task_io import (degismezleri_dogrula, uzunluk_kapisi,  # noqa: E402
                     metadatayi_dogrula, tanimlayici_kapisi)


def _secenekler(sablon: dict) -> list[dict[str, str]]:
    """
    sablon'daki tüm kelime kombinasyonlarını üretir.

    Sıralama deterministiktir (anahtarlar sıralı, `product` sabit sırayla
    gezer) — aynı sablon her zaman aynı sırada aynı varyantları verir.
    İLK kombinasyon her anahtarın ilk değeridir; bu, kanonik görevin kendi
    senaryosudur ve `varyantlari_uret` tarafından atlanır.
    """
    anahtarlar = sorted(sablon)
    return [dict(zip(anahtarlar, degerler)) for degerler in product(
        *(sablon[anahtar] for anahtar in anahtarlar)
    )]


def _yonerge_olustur(sablon: dict, secimler: dict[str, str]) -> str:
    """
    Bir sablon kombinasyonunu Translator'ın anlayacağı yönergeye çevirir.

    Kelimeler TOHUM olarak sunulur, ikame listesi olarak değil. Erken bir
    sürümde yönerge '"X" yerine "Y" kullan' diyordu ve ajan bunu sözlük
    ikamesi gibi uyguluyordu: `sayı -> adım` tohumu "n adım miktarının
    faktöriyeli" gibi hikâyesi olmayan bir metin üretmişti. Böyle bir varyant
    ezber ölçümü için DEĞERSİZDİR — problemi gizlemez, yalnızca bir kelimeyi
    değiştirir. Bu yüzden yönerge artık senaryo kurmayı açıkça ister.
    """
    tohumlar = [
        f'- "{sablon[anahtar][0]}" yerine "{yeni}" temasını kullan'
        for anahtar, yeni in sorted(secimler.items())
        if yeni != sablon[anahtar][0]
    ]
    if not tohumlar:
        return ""
    return "\n".join(tohumlar) + (
        "\n\nBu kelimeler TOHUM'dur. Etraflarında somut, gerçekçi ve kendi "
        "içinde tutarlı YENİ bir senaryo kur; yalnızca kelimeleri değiştirip "
        "eski cümleyi bırakma."
    )


def kombinasyon_sayisi(kanonik: dict) -> int:
    """Bu kanonik görevden üretilebilecek varyant sayısı (kanonik hariç)."""
    sablon = kanonik.get("sablon") or {}
    return max(0, len(_secenekler(sablon)) - 1) if sablon else 0


def varyantlari_uret(kanonik: dict, idler: list[str],
                     cevirici=promptlari_cevir) -> list[dict]:
    """
    Kanonik görevden `sablon` kombinasyonlarıyla doğrulanmış varyantlar üretir.

    `idler` kadar varyant üretilir (kombinasyonlar yeterliyse). Herhangi bir
    varyant kapılardan geçemezse AjanCagriHatasi fırlatılır — çağıran bunu
    "reddedildi" olarak ele almalı, veri setine YAZMAMALIdır.
    """
    sablon = kanonik.get("sablon") or {}
    if not sablon:
        return []

    varyantlar = []
    for yeni_id, secimler in zip(idler, _secenekler(sablon)[1:]):
        yonerge = _yonerge_olustur(sablon, secimler)
        if not yonerge:
            continue

        taslak = {a: d for a, d in kanonik.items() if a not in ("sablon", "id")}
        taslak.update({
            "id": yeni_id,
            "kaynak": "parametrik",
            "ebeveyn": kanonik["id"],
            "canonical_id": kanonik.get("canonical_id", kanonik["id"]),
            "variant_type": "parametric_story",
        })

        varyant = cevirici(taslak, yonerge=yonerge)

        maliyet = varyant.get("_maliyet_usd")

        sapmalar = degismezleri_dogrula(kanonik, varyant)
        if sapmalar:
            raise AjanCagriHatasi(
                f"Parametrik varyant kod alanlarına dokundu ({yeni_id}): "
                + "; ".join(sapmalar), maliyet_usd=maliyet
            )

        asirilik = uzunluk_kapisi(kanonik, varyant)
        if asirilik:
            raise AjanCagriHatasi(
                f"Parametrik varyant aşırı uzun ({yeni_id}): " + "; ".join(asirilik),
                maliyet_usd=maliyet,
            )

        # Design-A: EN prompt İngilizce, TR prompt Türkçe tanımlayıcı kullanmalı.
        tanimlayici_hatalari = tanimlayici_kapisi(varyant) + metadatayi_dogrula(varyant)
        if tanimlayici_hatalari:
            raise AjanCagriHatasi(
                f"Parametrik varyant Design-A kapısına takıldı ({yeni_id}): "
                + "; ".join(tanimlayici_hatalari), maliyet_usd=maliyet,
            )

        dogrulama = gorevi_dogrula(varyant)
        if not dogrulama["gecerli"]:
            raise AjanCagriHatasi(
                f"Parametrik varyant guardrail reddetti ({yeni_id}): "
                f"{dogrulama['gecen']}/{dogrulama['toplam']}", maliyet_usd=maliyet
            )
        varyantlar.append(varyant)
    return varyantlar
