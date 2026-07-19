# 20 Günlük Staj Planı — TR-CodeEval

Bu belge, projenin 20 iş gününe bölünmüş yol haritasıdır. Her gün **tek ve
somut bir çıktı** üretir; günler birbirine **girdi → çıktı** zinciriyle
bağlıdır. Yol haritasının teknik gerekçesi için bkz. `proje_yon_raporu.md`.

> **Bu bir kılavuzdur, sözleşme değildir.** Gün numaraları hedeftir, kilit
> değil. Aşağıdaki *Esneklik İlkesi* bölümü, plan değiştiğinde kaosa
> düşmeden nasıl ilerleyeceğimizi tanımlar.

---

## Esneklik İlkesi — Plan Değişince Ne Yaparız?

Günlük işlerde sapma **normaldir**. Bunu üç katmanlı bir "hakikat kaynağı"
düzeniyle yönetiriz; böylece plan esner ama iz kaybolmaz:

| Katman | Dosya / Yer | Neyi tutar | Ne zaman güncellenir |
|--------|-------------|------------|----------------------|
| **Niyet** | `docs/20_gunluk_plani.md` (bu dosya) | Çerçeve + bağımlılıklar | Plan değişince + *Revizyon Günlüğü*'ne satır |
| **Canlı durum** | GitHub Board (Projects #3) | Kart hangi kolonda, kim, kapsam | Her gün, iş ilerledikçe |
| **Gerçekleşen** | `docs/staj_defteri_gunlukleri.md` | O gün *fiilen* ne yapıldı | Her günün sonunda |

**Çelişki olursa esas alınan: Gerçekleşen (defter).** Plan geleceğe dair
bir tahmindir; defter olana dair kayıttır.

### Kaydırma Kuralları (sapmayı disipline eden 4 kural)

1. **Fazlar sabit, gün-içi dağılım esnek.** Beş faz (aşağıda) bloklardır.
   Bir iş taşarsa önce **faz içinde** kaydırılır; faz sınırı korunur.
2. **Taşma faz sınırını aşarsa: gün ekleme, kapsamı küçült.** Ör. "20 kanonik
   görev" hedefi 15'e iner; toplam gün sayısı 20'de kalır. (Tampon: Gün 20.)
3. **Yalnızca aşağı-akışı güncelle.** Bağımlılık tablosu sayesinde bir gün
   değişince *hangi sonraki günlerin* etkilendiği görünür; yalnız onlar
   revize edilir.
4. **Her değişiklik iz bırakır.** *Revizyon Günlüğü*'ne `tarih — değişiklik —
   sebep` satırı eklenir. Git zaten dosyayı versiyonlar; board kartı taşınır.

Bu düzende plana %100 uymak *gerekmez*; **plandan sapmayı kayıt altına
almak** yeterlidir. Kayıtlı sapma, plansızlık değil, olgun proje yönetimidir.

---

## Fazlar (bloklar)

| Faz | Günler | Tema | Durum |
|-----|--------|------|-------|
| **F1 — Temel & Kavram** | 1–6 | Yapı, kavramlar, veri seti, prompt | ✅ Bitti |
| **F2 — Deterministik Çekirdek & Dikey Dilim** | 7–10 | Sandbox, Oracle, model istemcisi, uçtan-uca | 🔄 Sürüyor |
| **F3 — Veri Seti & Yaratıcı Ajanlar** | 11–14 | Kanonik görevler, Mutator/Translator (Claude) | ⏳ |
| **F4 — Metrik & Orkestrasyon** | 15–17 | Vergiler, taksonomi, trend, LangGraph | ⏳ |
| **F5 — Yayın & Kapanış** | 18–20 | Dashboard, HuggingFace, rapor | ⏳ |

---

## Günlük Plan (girdi → çıktı zinciriyle)

Her satır: **Girdi** (hangi önceki günün çıktısına dayanır) ve **Çıktı**
(hangi sonraki güne besler). Bu, planın "birbirine bağlı" iskeletidir.

### F1 — Temel & Kavram (✅ 1–6)

| Gün | İş | Girdi | Çıktı | Durum |
|-----|-----|-------|-------|-------|
| 1 | Proje yapısı + README | — | Repo iskeleti | ✅ |
| 2 | LLM/benchmark kavramları | G1 | `01_..giris.md` | ✅ |
| 3 | Benchmark veri setleri | G2 | `02_..veri_setleri.md` | ✅ |
| 4 | Değerlendirme metrikleri | G3 | `03_..metrikleri.md` | ✅ |
| 5 | Çoktan-seçmeli veri seti | G4 | `sample_questions.json` | ✅ |
| 6 | Prompt formatı | G5 | `prompt_builder.py` | ✅ |

### F2 — Deterministik Çekirdek & Dikey Dilim (7–10)

| Gün | İş | Girdi | Çıktı | Durum |
|-----|-----|-------|-------|-------|
| 7 | Docker Sandbox + Oracle | G1 (yapı) | `sandbox/`, `oracle/`, `trc_001` | ✅ |
| 8 | Yerel model istemcisi (Ollama/LM Studio) | G6 (prompt) | `model_client/` | ✅ |
| 9 | **Uçtan-uca dikey dilim** (görev→model→sandbox→sonuç) | G7+G8 | `run_task.py` çalışır | ✅ |
| 10 | Çoklu model + TR/EN koşumu; sonuçları `results/`'a yaz | G9 | `results/*.json` şeması | ✅ |

### F3 — Veri Seti & Yaratıcı Ajanlar (11–14)

| Gün | İş | Girdi | Çıktı | Durum |
|-----|-----|-------|-------|-------|
| 11 | Veri seti büyütme I: 8–10 kanonik görev (dizi/string/matematik) + oracle doğrulama | G7 (oracle) | `data/tasks/*` genişler | ⏳ |
| 12 | Veri seti büyütme II: 10–12 görev daha (mantık/özyineleme/sayma), ~20 kanonik | G11 | ~20 doğrulanmış görev | ⏳ |
| 13 | **Mutator ajanı** (Claude API): parametrik varyant + oracle guardrail | G12 + G7 | `oracle/` onaylı varyantlar | ⏳ |
| 14 | Hikaye mutasyonu + TR↔EN Translator ajanı; varyant ailesi otomasyonu | G13 | Varyant ailesi üretici | ⏳ |

### F4 — Metrik & Orkestrasyon (15–17)

| Gün | İş | Girdi | Çıktı | Durum |
|-----|-----|-------|-------|-------|
| 15 | **Metrik motoru**: pass@1/pass@k, Türkçe vergisi, ezber farkı, token vergisi | G10 + G14 | `metrics/` modülü | ⏳ |
| 16 | Hata taksonomisi (Failure-Classifier) + ölçek trendi (0.5→3B eğrisi) | G15 | Taksonomi + trend figürleri | ⏳ |
| 17 | **LangGraph** orkestrasyon: bileşenleri oracle-korumalı state ile bağla | G13+G15 | Uçtan-uca akış grafiği | ⏳ |

### F5 — Yayın & Kapanış (18–20)

| Gün | İş | Girdi | Çıktı | Durum |
|-----|-----|-------|-------|-------|
| 18 | **Gradio dashboard**: canlı demo + metrik grafikleri | G16 | `dashboard/` | ⏳ |
| 19 | **HuggingFace** Datasets yayını + dataset card | G12+G16 | Yayınlanmış veri seti | ⏳ |
| 20 | Kapanış + **tampon**: rapor/README güncelleme, sınırlılıklar, sunum | Tümü | Final rapor | ⏳ |

---

## Bağımlılık Haritası (kritik zincir)

```
G7 (Sandbox+Oracle) ─┬─> G9 (dikey dilim) ─> G10 (çoklu koşum) ─> G15 (metrik)
G8 (model istemci) ──┘                                              │
G11→G12 (veri seti) ─> G13 (mutator) ─> G14 (varyant) ─────────────┤
                                                                    ├─> G16 (taksonomi/trend)
                                        G15 + G13 ─> G17 (LangGraph) │
G16 ─> G18 (dashboard)                                              │
G12 + G16 ─> G19 (HF yayını) ─> G20 (kapanış) <─────────────────────┘
```

**En kritik düğüm:** G7 (Sandbox+Oracle) — her doğrulama buradan geçer.
Kayarsa tüm alt-akış kayar; bu yüzden erkene (Gün 7) çekildi ve tamamlandı.

---

## Revizyon Günlüğü

Plandaki her sapma buraya `tarih — değişiklik — sebep` olarak işlenir.

- **2026-07-20 — v1.0** — İlk 20 günlük plan oluşturuldu. Gün 1–8 tamamlanmış
  durumda; Gün 9 (dikey dilim) başladı. Yol haritası §7 ile hizalı.
- **2026-07-20 — v1.1** — Gün 9 tamamlandı (✅). Kapsam eki: koşum sırasında
  Ollama'nın seed'siz tam tekrarlanabilir olmadığı görülünce model istemcisine
  sabit `seed` eklendi (pass@1 determinizmi). Sebep: benchmark için ölçümün
  tekrarlanabilir olması şart. Aşağı-akış etkilenmedi; Gün 10 başladı (🔄).
- **2026-07-20 — v1.2** — Gün 10 tamamlandı (✅). Bulgu: sabit seed düşük
  VRAM'de bit-determinizmi garanti etmiyor (model takası + GPU offload). Yanıt:
  matris runner'a `--tekrar K` çok-örnekleme eklendi; pass@1 yerine çok-örnekli
  ölçüm esas alınacak. Bu, Gün 15 (pass@k) tasarımını netleştirir — aşağı-akış
  güçlenir, gün sayısı değişmez.
- **2026-07-20 — v1.3** — Gün 11 öncesi sağlamlaştırma arası (yeni gün açmaz).
  Seçici jüri öz-değerlendirmesiyle mühendislik açıkları kapatıldı: sandbox
  stdout açığı + `--cap-drop ALL`/`no-new-privileges`, harness karşılaştırma
  modları, gerçek pass@k (`--sicaklik>0`), pytest paketi + CI, izole `.venv` +
  pinli bağımlılıklar, README yeniden yazımı. Sebep: veri setini büyütmeden önce
  zeminin testli ve tekrarlanabilir olması. Aşağı-akış güçlendi; süre değişmedi.
