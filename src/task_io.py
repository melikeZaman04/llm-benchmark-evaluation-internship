"""
Görev dosyalarının okunması, yazılması ve ŞEMA değişmezlerinin doğrulanması.

Neden ayrı bir modül? Üç ayrı yer (run_mutator, run_parametric, testler) aynı
iki soruyu soruyor: "bu görev dosyası nasıl yazılır?" ve "bu görev nesnesi
şemaya uygun mu?". Tek kaynakta toplanmazsa veri seti büyüdükçe her biri
kendi kopyasıyla ayrışır.

İki tasarım kararı:

1. `gorev_yaz` biçimi ELLE OKUNABİLİR tutar. Düz `json.dumps(indent=2)` her
   test case'i 10+ satıra yayar (`trc_001` 30 -> 97 satır); bu, veri setini
   git diff'inde ve elle düzenlemede okunamaz hale getirir. Buradaki
   serileştirici, satıra sığan yapıları (bir test case, bir sablon listesi)
   TEK SATIRDA tutar; yalnızca sığmayanları açar.

2. `metadatayi_dogrula` Docker GEREKTİRMEZ. Oracle (task_validator) görevin
   KODUNU çalıştırarak doğrular; buradaki kontrol ise görevin KİMLİK ve AİLE
   alanlarını doğrular (id biçimi, canonical_id/ebeveyn tutarlılığı, boş
   prompt yok). İkisi farklı şeylere bakar ve birbirinin yerine geçmez.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

GOREVLER_DIZINI = Path(__file__).resolve().parent.parent / "data" / "tasks"

ID_DESENI = re.compile(r"trc_\d{3,}")

#: Veri setinde kabul edilen varyant eksenleri. Yeni bir eksen eklendiğinde
#: BURAYA eklenir; testler bu kümeyi okur, kendi kopyalarını tutmaz.
VARYANT_TIPLERI = frozenset({
    "canonical",         # elle yazılmış kanonik görev
    "story_mutation",    # Mutator ajanı: aynı algoritma, yeni senaryo
    "parametric_story",  # sablon kombinasyonu: aynı algoritma, sablon senaryosu
})

#: Bir varyantın ebeveyninden ASLA sapmaması gereken alanlar. Varyant üretimi
#: yalnızca metni (prompt) değiştirir; bunlar byte-byte kopyalanır.
DEGISMEZ_ALANLAR = ("fonksiyon_imzasi", "fonksiyon_adi", "referans_cozum",
                    "test_cases", "karsilastirma")

#: Ebeveyni ile AYNI imzayı taşıyan (parametric_story) varyantlar için ek
#: değişmezler: dil-başına tanımlayıcılar da byte-byte kopyalanmalı. Yalnız
#: _en alanları mevcutsa denetlenir (parametric.py, story_mutation hariç).
DEGISMEZ_ALANLAR_EN = ("fonksiyon_imzasi_en", "fonksiyon_adi_en")

#: Dosyaya yazarken kullanılan sabit alan sırası. Üreteçler alanları farklı
#: sırayla ekleyebilir (ör. `id` en sona düşebilir); veri seti yayınlanacak
#: bir eser olduğu için dosyalar TEK ve öngörülebilir bir sırada yazılır.
#: Listede olmayan alanlar sonuna, kendi aralarında alfabetik eklenir.
ALAN_SIRASI = ("id", "kategori", "zorluk", "kaynak", "ebeveyn", "canonical_id",
               "variant_type", "prompt_tr", "prompt_en", "fonksiyon_imzasi",
               "fonksiyon_adi", "fonksiyon_imzasi_en", "fonksiyon_adi_en",
               "referans_cozum", "test_cases", "karsilastirma", "sablon")


# --- Serileştirme ---------------------------------------------------------
def _bicimle(deger, girinti: int, genislik: int) -> str:
    """Satıra sığan yapıları tek satırda, sığmayanları girintili yazar."""
    duz = json.dumps(deger, ensure_ascii=False)
    if not isinstance(deger, (dict, list)) or len(duz) + girinti <= genislik:
        return duz

    ic_girinti = girinti + 2
    bosluk = " " * ic_girinti
    if isinstance(deger, list):
        ogeler = [bosluk + _bicimle(o, ic_girinti, genislik) for o in deger]
        acilis, kapanis = "[", "]"
    else:
        ogeler = [
            f"{bosluk}{json.dumps(anahtar, ensure_ascii=False)}: "
            f"{_bicimle(alt, ic_girinti, genislik)}"
            for anahtar, alt in deger.items()
        ]
        acilis, kapanis = "{", "}"
    return acilis + "\n" + ",\n".join(ogeler) + "\n" + " " * girinti + kapanis


def alanlari_sirala(gorev: dict) -> dict:
    """Görev alanlarını ALAN_SIRASI'na göre yeniden dizer."""
    bilinen = [a for a in ALAN_SIRASI if a in gorev]
    kalan = sorted(a for a in gorev if a not in ALAN_SIRASI)
    return {a: gorev[a] for a in bilinen + kalan}


def gorev_metni(gorev: dict, genislik: int = 100) -> str:
    """Bir görev nesnesini okunabilir, alanları sıralı JSON metnine çevirir."""
    return _bicimle(alanlari_sirala(gorev), 0, genislik) + "\n"


def gorev_yaz(gorev: dict, yol: Path | str | None = None) -> Path:
    """Görevi diske yazar; `_` ile başlayan iç alanlar (ör. `_maliyet_usd`) atılır."""
    temiz = {a: d for a, d in gorev.items() if not a.startswith("_")}
    hedef = Path(yol) if yol else GOREVLER_DIZINI / f"{temiz['id']}.json"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(gorev_metni(temiz), encoding="utf-8")
    return hedef


def gorev_oku(yol: Path | str) -> dict:
    return json.loads(Path(yol).read_text(encoding="utf-8"))


def gorevleri_yukle(dizin: Path | str | None = None) -> list[dict]:
    """Veri setindeki tüm görevleri id sırasıyla yükler."""
    kok = Path(dizin) if dizin else GOREVLER_DIZINI
    return [gorev_oku(yol) for yol in sorted(kok.glob("trc_*.json"))]


def sonraki_id_uretici(dizin: Path | str | None = None):
    """Veri setini tarar, çakışmayan id'leri artan sırada üretir."""
    kok = Path(dizin) if dizin else GOREVLER_DIZINI
    en_buyuk = 0
    for yol in kok.glob("trc_*.json"):
        if ID_DESENI.fullmatch(yol.stem):
            en_buyuk = max(en_buyuk, int(yol.stem.split("_")[1]))
    while True:
        en_buyuk += 1
        yield f"trc_{en_buyuk:03d}"


# --- Şema doğrulaması (Docker gerektirmez) --------------------------------
def metadatayi_dogrula(gorev: dict) -> list[str]:
    """Görevin kimlik/aile alanlarını denetler; hata mesajları listesi döner."""
    hatalar: list[str] = []
    gorev_id = gorev.get("id", "<id yok>")

    if not ID_DESENI.fullmatch(str(gorev.get("id", ""))):
        hatalar.append(f"{gorev_id}: id 'trc_NNN' biçiminde değil")

    tip = gorev.get("variant_type")
    if tip not in VARYANT_TIPLERI:
        hatalar.append(
            f"{gorev_id}: variant_type={tip!r} tanınmıyor "
            f"(beklenen: {sorted(VARYANT_TIPLERI)})"
        )

    kanonik_id = gorev.get("canonical_id")
    if not kanonik_id:
        hatalar.append(f"{gorev_id}: canonical_id yok")
    elif tip == "canonical":
        if kanonik_id != gorev.get("id"):
            hatalar.append(f"{gorev_id}: kanonik görevde canonical_id kendi id'si olmalı")
        if gorev.get("ebeveyn"):
            hatalar.append(f"{gorev_id}: kanonik görevin ebeveyni olamaz")
    elif tip in VARYANT_TIPLERI:
        if not gorev.get("ebeveyn"):
            hatalar.append(f"{gorev_id}: varyantın ebeveyn alanı yok")
        if kanonik_id == gorev.get("id"):
            hatalar.append(f"{gorev_id}: varyant kendi kendisinin kanoniği olamaz")

    for alan in ("prompt_tr", "prompt_en", "fonksiyon_imzasi", "fonksiyon_adi",
                 "referans_cozum", "kategori", "zorluk"):
        if not str(gorev.get(alan, "")).strip():
            hatalar.append(f"{gorev_id}: {alan} boş veya yok")

    if not gorev.get("test_cases"):
        hatalar.append(f"{gorev_id}: test_cases boş")

    ad, cozum = gorev.get("fonksiyon_adi"), gorev.get("referans_cozum", "")
    if ad and f"def {ad}" not in cozum:
        hatalar.append(f"{gorev_id}: referans_cozum 'def {ad}' tanımını içermiyor")

    # Dil-başına tanımlayıcılar (Design A): _en alanları varsa ikisi de bulunmalı
    # ve fonksiyon_adi_en, fonksiyon_imzasi_en içinde 'def <ad>' olarak geçmeli.
    imza_en = gorev.get("fonksiyon_imzasi_en")
    ad_en = gorev.get("fonksiyon_adi_en")
    if imza_en or ad_en:
        if not (imza_en and ad_en):
            hatalar.append(f"{gorev_id}: fonksiyon_imzasi_en ve fonksiyon_adi_en "
                           "birlikte bulunmalı (biri eksik)")
        elif f"def {ad_en}" not in imza_en:
            hatalar.append(f"{gorev_id}: fonksiyon_imzasi_en 'def {ad_en}' içermiyor")

    return hatalar


def _imza_parametreleri(imza: str) -> set:
    return set(re.findall(r"[(,]\s*([A-Za-z_]\w*)\s*:", imza or ""))


def tanimlayici_kapisi(gorev: dict) -> list[str]:
    """Design A: prompt backtick'leri İLGİLİ DİLİN imzasıyla eşleşmeli.

    prompt_tr yalnız Türkçe imzadaki (fonksiyon_imzasi/adi) tanımlayıcıları,
    prompt_en yalnız İngilizce imzadaki (fonksiyon_imzasi_en/adi_en; yoksa
    TR'ye düşer) tanımlayıcıları backtick'leyebilir. EN sütununa Türkçe
    tanımlayıcı sızması (ya da tersi) bu kapıda yakalanır.
    """
    gid = gorev.get("id", "<id yok>")
    tr = _imza_parametreleri(gorev.get("fonksiyon_imzasi")) | {gorev.get("fonksiyon_adi")}
    en_imza = gorev.get("fonksiyon_imzasi_en") or gorev.get("fonksiyon_imzasi")
    en = _imza_parametreleri(en_imza) | {gorev.get("fonksiyon_adi_en") or gorev.get("fonksiyon_adi")}
    hatalar = []
    for t in re.findall(r"`([A-Za-z_]\w*)`", gorev.get("prompt_tr", "")):
        if t not in tr:
            hatalar.append(f"{gid}: TR prompt `{t}` TR imzada yok")
    for t in re.findall(r"`([A-Za-z_]\w*)`", gorev.get("prompt_en", "")):
        if t not in en:
            hatalar.append(f"{gid}: EN prompt `{t}` EN imzada yok")
    return hatalar


def uzunluk_kapisi(ebeveyn: dict, varyant: dict,
                   ust_kat: float = 3.0, taban_pay: int = 250) -> list[str]:
    """
    Varyant promptunun ebeveyninden aşırı uzamadığını denetler.

    Neden ÖLÇÜM için gerekli: ezber farkı `acc(kanonik) − acc(varyant)` olarak
    hesaplanır. Varyant metni özgününden belirgin uzunsa, gözlenen düşüşün
    kaynağı belirsizleşir — ezberin kırılması mı, yoksa yalnızca daha uzun ve
    daha yoğun bir metni işlemenin zorluğu mu? İkisi ayrışmazsa metrik
    yorumlanamaz. Bu kapı, o confound'u veri setine hiç sokmadan keser.

    Üst sınır bilinçli olarak gevşektir (3x): amaç zengin senaryoyu engellemek
    değil, uç örnekleri (ör. bir cümlelik problemi bir paragrafa çeviren) veri
    setine sessizce girmekten alıkoymaktır.

    Neden SAF ORAN yetmez: bir senaryo kurmanın kabaca SABİT bir karakter
    maliyeti vardır (kim, nerede, neyi ölçüyor). Ebeveyn çok kısaysa (ör.
    trc_014 faktöriyel promptu 105 karakter) herhangi bir gerçek senaryo
    kaçınılmaz olarak 3 katını aşar; saf oran, kısa ebeveynli görevlerde
    parametrik ekseni tümden imkânsız kılardı. Bu yüzden sınır
    `max(oran, ebeveyn + taban_pay)` olarak alınır: kısa metinlere senaryo
    kurmaya yetecek sabit bir pay tanınır, uzun metinlerde oran devreye girer.
    """
    hatalar: list[str] = []
    for alan in ("prompt_tr", "prompt_en"):
        ebeveyn_uzunluk = len(ebeveyn.get(alan, ""))
        varyant_uzunluk = len(varyant.get(alan, ""))
        if not ebeveyn_uzunluk:
            continue
        sinir = max(ebeveyn_uzunluk * ust_kat, ebeveyn_uzunluk + taban_pay)
        if varyant_uzunluk > sinir:
            hatalar.append(
                f"{varyant.get('id', '<id yok>')}: {alan} {varyant_uzunluk} karakter, "
                f"ebeveyninin {varyant_uzunluk / ebeveyn_uzunluk:.1f} katı "
                f"(sınır {sinir:.0f} karakter)"
            )
    return hatalar


def degismezleri_dogrula(ebeveyn: dict, varyant: dict) -> list[str]:
    """
    Varyantın kod/test alanlarının ebeveyninden sapmadığını denetler.

    YALNIZCA `parametric_story` için geçerlidir: parametrik varyantta sadece
    prompt metinleri değişir, kod byte-byte kopyalanır. `story_mutation`
    varyantları için KULLANILMAZ — Mutator tanım gereği fonksiyon adını,
    imzayı ve referans çözümü yeniden adlandırır; oradaki güvence oracle'ın
    kodu gerçekten çalıştırmasıdır.
    """
    return [
        f"{varyant.get('id', '<id yok>')}: {alan} ebeveyninden ({ebeveyn.get('id')}) sapmış"
        for alan in DEGISMEZ_ALANLAR
        if ebeveyn.get(alan) != varyant.get(alan)
    ]
