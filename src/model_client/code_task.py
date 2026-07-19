"""
Kod görevi ↔ model köprüsü.

İki iş yapar:
  1) Bir TR-CodeEval görevini (trc_*.json) modele verilecek bir KOD ÜRETİM
     prompt'una çevirir (`kod_prompt_olustur`). TR/EN dili seçilebilir —
     böylece aynı görev iki dilde sorulup "Türkçe muhakeme vergisi" ölçülür.
  2) Modelin (çoğu zaman markdown kod bloğu içeren) ham yanıtından yalnızca
     çalıştırılabilir Python kodunu ayıklar (`kod_ayikla`).

Bu modül yalnızca metin biçimlendirir/ayıklar; hiçbir yargı (doğru/yanlış)
vermez. Üretilen kodun testleri geçip geçmediğine Sandbox + Oracle karar verir.
"""

from __future__ import annotations

import re

SISTEM_TR = (
    "Sen deneyimli bir Python programcısısın. Sana verilen problemi çözen "
    "tek bir Python fonksiyonu yaz. Yalnızca tek bir ```python kod bloğu "
    "döndür; açıklama, örnek kullanım veya test kodu ekleme. Fonksiyonun "
    "adı ve imzası istenenle birebir aynı olmalı."
)


def kod_prompt_olustur(gorev: dict, dil: str = "tr") -> str:
    """
    Bir görev nesnesini modele verilecek kod-üretim prompt'una çevirir.

    dil: "tr" -> prompt_tr, "en" -> prompt_en kullanılır.
    """
    if dil not in ("tr", "en"):
        raise ValueError("dil yalnızca 'tr' veya 'en' olabilir.")

    anahtar = "prompt_tr" if dil == "tr" else "prompt_en"
    if anahtar not in gorev:
        raise ValueError(f"Görevde '{anahtar}' alanı yok.")
    if "fonksiyon_imzasi" not in gorev:
        raise ValueError("Görevde 'fonksiyon_imzasi' alanı yok.")

    problem = gorev[anahtar].strip()
    imza = gorev["fonksiyon_imzasi"].strip()

    if dil == "tr":
        satirlar = [
            problem,
            "",
            "Aşağıdaki imzayı birebir kullanarak fonksiyonu tamamla:",
            "",
            "```python",
            imza,
            "    ...",
            "```",
            "",
            "Yalnızca tamamlanmış fonksiyonu tek bir ```python kod bloğu "
            "içinde ver.",
        ]
    else:
        satirlar = [
            problem,
            "",
            "Complete the function using exactly the following signature:",
            "",
            "```python",
            imza,
            "    ...",
            "```",
            "",
            "Return only the completed function inside a single ```python "
            "code block.",
        ]
    return "\n".join(satirlar)


# ```python ... ```  ya da  ``` ... ```  bloklarını yakalar.
_KOD_BLOK = re.compile(r"```(?:python|py)?\s*\n?(.*?)```", re.DOTALL | re.IGNORECASE)


def kod_ayikla(metin: str) -> str:
    """
    Model yanıtından çalıştırılabilir Python kodunu ayıklar.

    Öncelik sırası:
      1) İlk markdown kod bloğunun içeriği (en yaygın durum),
      2) Blok yoksa metnin kendisi (bazı modeller düz kod döndürür).
    Metin trimlenir; sondaki gereksiz boşluklar temizlenir.
    """
    if not isinstance(metin, str):
        raise ValueError("metin bir string olmalıdır.")

    bloklar = _KOD_BLOK.findall(metin)
    if bloklar:
        # `def` içeren ilk blok tercih edilir; yoksa ilk blok.
        for blok in bloklar:
            if "def " in blok:
                return blok.strip() + "\n"
        return bloklar[0].strip() + "\n"

    # Kod bloğu yok: düz metni kod kabul et (yalın kod döndüren modeller için).
    return metin.strip() + "\n"


def modelden_cozum_al(gorev: dict, istemci, dil: str = "tr") -> dict:
    """
    Uçtan uca tek adım: görev -> prompt -> model -> ayıklanmış kod.

    Dönüş (dict):
      {
        "id": str, "dil": str,
        "kod": str,          # sandbox'a verilebilecek ayıklanmış Python kodu
        "ham_yanit": str,    # modelin ham metni (hata ayıklama için)
        "kullanim": dict|None,
        "prompt": str,
      }
    Not: Bu fonksiyon kodu ÇALIŞTIRMAZ ve doğrulamaz; yalnızca üretir.
    """
    prompt = kod_prompt_olustur(gorev, dil=dil)
    sonuc = istemci.uret(prompt, sistem=SISTEM_TR)
    kod = kod_ayikla(sonuc["metin"])
    return {
        "id": gorev.get("id"),
        "dil": dil,
        "kod": kod,
        "ham_yanit": sonuc["metin"],
        "kullanim": sonuc.get("kullanim"),
        "prompt": prompt,
    }


if __name__ == "__main__":
    # Bağımsız test: prompt üretimi ve kod ayıklama (model gerektirmez).
    ornek_gorev = {
        "id": "trc_001",
        "prompt_tr": "Bir listedeki en büyük sayıyı döndüren fonksiyon yaz.",
        "prompt_en": "Write a function that returns the largest number in a list.",
        "fonksiyon_imzasi": "def en_buyuk(sayilar: list[int]) -> int:",
    }
    print("=== TR PROMPT ===")
    print(kod_prompt_olustur(ornek_gorev, dil="tr"))

    ornek_yanit = (
        "Elbette, işte çözüm:\n\n"
        "```python\n"
        "def en_buyuk(sayilar):\n"
        "    return max(sayilar)\n"
        "```\n"
        "Umarım yardımcı olur."
    )
    print("\n=== AYIKLANAN KOD ===")
    print(kod_ayikla(ornek_yanit))
