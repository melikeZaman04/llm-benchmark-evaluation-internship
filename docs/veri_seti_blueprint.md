# TR-CodeEval Veri Seti Blueprint (Spesifikasyon Tablosu)

> **Niyet dokümanı** (üç-katman kaynağın "Niyet" katmanı; canlı durum GitHub board,
> gerçekleşen `staj_defteri_gunlukleri.md`). Veri seti büyütmesinin SÖZLEŞMESİ:
> yazımdan önce "kategori × zorluk × sayı" burada sabitlenir — "yaz sonra say" değil.

## 1. Ölçülen yapılar (construct validity)

Her kanonik görev, aşağıdaki üç yapıdan **en az birine** açıkça hizmet eder; dolgu
görev yoktur:

1. **Kodlama yeteneği** — modelin elemanter algoritmik problemi çözme gücü (pass@1/@k).
2. **Türkçe dil-sağlamlığı ("Türkçe vergisi")** — `acc(en) − acc(tr)`. Ölçüm bir
   FARK olduğundan varyansı yüksektir → aynı kesinlik için tek-doğruluk
   benchmark'ından daha çok göreve ihtiyaç duyar (bkz. §2).
3. **Ezber-direnci** — kanonik vs sığ (parametric_story) vs derin (story_mutation)
   varyant ailesi üzerinden metamorfik prob. Her kanonik görev **tam aile** taşımalı.

## 2. Boyut hedefi (güç-temelli, keyfi değil)

Boyut hedef kesinlikten geri hesaplanır. Mevcut veride ölçülen görev-farkı SD'si
(~0.32 ortalama) üzerinden %95 CI yarı-genişliği ≈ 1.96·SD/√n:

| Hedef CI yarı-genişliği | Gereken kanonik | Yorum |
|---|---|---|
| ±0.10 (v1, n=20) | 20 | geniş — çoğu vergi belirsiz |
| ±0.07 | ~80 | manşet iddiaları savunulabilir |
| ±0.05 | ~158 | yayın-kalitesi |

Sektör normu (HumanEval 164, MBPP-sanitized 427) ile bağımsız olarak **~150
kanonikte** buluşur. Aile çarpanı ×3 → 150 kanonik = ~450 değerlendirme birimi.

**Fazlı plan** (her sürüm dondurulur → doğrulanır → koşulur → sonra sonraki):

| Sürüm | Kanonik | Toplam birim | Kesinlik | Amaç |
|---|---|---|---|---|
| **v1 (mevcut)** | 20 | 62 | ±0.10 | Altyapı + MVP |
| **v2 (sıradaki)** | ~50 | ~150 | ±0.09 | Zor tier + pipeline ölçek kanıtı |
| **v3 (hedef)** | ~120 | ~360 | ±0.06 | Savunulabilir manşetler |

## 3. Zorluk merdiveni (TANIMLI — sadece etiket değil)

En acil boşluk: v1'de **0 zor görev** (12 kolay + 8 orta) → coder:3b 0.85'te tavan
etkisi. Zorluk şu ölçütlerle tanımlanır:

- **kolay:** tek geçiş/döngü, tek kavram, küçük girdi uzayı, aşikâr çözüm.
- **orta:** iki kavramın birleşimi, kenar durumları önemli, durum-makinesi ya da
  O(n log n).
- **zor:** birden çok kavram, aşikâr-olmayan algoritma (DP, dikkatli değişmez,
  ince off-by-one, kombinatorik), **güçlü modelleri ayırt eden** kenar durumlar.

**Hedef dağılım (v2, 50 kanonik):** %30 kolay (15) · %45 orta (23) · %25 zor (12).
Her kategori en az 1 kolay ve 1 zor içermeli (kategori-içi ayırt edicilik).

## 4. Spesifikasyon tablosu (kategori × zorluk — v2 hedefi)

| Kategori | Mevcut | v2 hedef | Δ ekle | Not (zor odak) |
|---|---|---|---|---|
| diziler | 3 | 9 | +6 | kayan pencere, iki-işaretçi |
| string | 3 | 8 | +5 | ayrıştırma, örüntü |
| matematik | 3 | 8 | +5 | modüler, sayı-teorik (şu an çok kolay) |
| mantik | 4 | 9 | +5 | durum-makinesi, kısıt |
| ozyineleme | 4 | 8 | +4 | DP, ağaç/geri-izleme |
| sayma | 3 | 8 | +5 | kombinatorik, O(n) vs O(n²) |
| **Toplam** | **20** | **50** | **+30** | |

Her yeni kanonik → 1 parametric_story + 1 story_mutation (aile bütünlüğü).

## 5. Değişmez kalite kapıları (her görev geçmeli)

1. **Oracle guardrail** — referans çözüm test_cases'i geçmeli (mekanik doğruluk).
2. **Anlam-denetimi** — TR/EN parite + Türkçe tutarlılık + senaryo-mantığı
   (ajan ilk-geçiş + noktasal insan gözü).
3. **Uzunluk kapısı** — varyant, ebeveynin `max(3×, +250 karakter)` sınırında
   (uzunluk confound'unu önler).
4. **Tanımlayıcı invariant (Design A)** — EN sütunu tamamen İngilizce, TR tamamen
   Türkçe; prompt backtick'leri ilgili dilin imzasıyla eşleşir (regresyon testli).
5. **Değişmezler** — parametric_story kod/test'i ebeveynle byte-byte aynı.

## 6. Kontaminasyon ve adalet ilkeleri

- **Özgün yazım — ASLA** internetten/HumanEval/LeetCode/MBPP'den kopya (modeller
  onlarla eğitilmiş; ezber kirliliği). Bu projenin ayırt edici değeri.
- Gizleme, var-olan-ve-doğrulanmış problemin yüzeyini değiştiren ajan fabrikasıyla
  yapılır (yeni problem icat edilmez).
- Confound kontrolü: tek değişken problem+tanımlayıcı dili; sistem promptu, imza,
  tanımlayıcılar dahil modele giden HER metin denetlenir.

## 7. Sürüm ve dondurma politikası

- Her sürüm (v1/v2/v3) git etiketi ile dondurulur; **dondurulmuş sürüm ASLA
  düzenlenmez** (tekrarlanabilirlik).
- Sonuçlar daima `dataset_sürümü + koşum_config (tekrar, sıcaklık, modeller)`
  alıntılar.
- Koşum sırasında dataset donuk kalır (yeni görev, koşum bittikten sonra).

## 8. Revizyon günlüğü

| Tarih | Değişiklik | Sebep |
|---|---|---|
| 2026-07-24 | Blueprint oluşturuldu; v2=50/v3=120 hedefi, zorluk merdiveni tanımlandı | Design A re-run sonrası; 16. gün öncesi kavramsal boşlukları kapatma |
