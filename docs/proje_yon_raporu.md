# Proje Yön Raporu — TR-CodeEval: İki Düzlemli, Kirlilik-Dirençli Türkçe Kod Değerlendirme Takımı

## 1. Özet ve Vizyon
Bu proje, yerel açık-kaynak dil modellerinin (LLM) kod problemlerini
*gerçekten anlayıp anlamadığını* ölçen, yeniden kullanılabilir bir
**değerlendirme takımı (benchmark)** inşa eder. Katkı, model çalıştırmak
değil; herkesin (büyük donanımlılar dahil) kendi modelini geçirebileceği
**ölçü aletini** kurmaktır — tıpkı MMLU ve HumanEval'in yazarlarının en
güçlü donanıma değil, en iyi *cetvele* sahip olmasıyla tanınması gibi.

Var olan kod benchmark'larından üç eksende ayrışırız: **(1) Türkçe**,
**(2) ezber-dayanıklılığı** (mutasyon), **(3) çalıştırma-tabanlı**
gerçek doğrulama.

**İki benchmark, tek altyapı (Gün 13'te netleşen çerçeve):** Aynı koşum
matrisinden iki ayrı araştırma sorusu cevaplanır. **(A) Küçük modeller
kodlamada ne kadar başarılı?** — saf yetenek, model ölçeğiyle nasıl değişiyor;
bilinçli olarak İNGİLİZCE ölçülür (test edilen modellerin baskın eğitim
dili), böylece dil engelinden arındırılmış bir "saf kodlama yeteneği" sinyali
elde edilir. **(B) Türkçe muhakeme, kod üretimini ne kadar zorlaştırıyor?**
— `acc(en) − acc(tr)`; B'yi anlamlı yorumlamak, A'nın "temiz" tabanını
gerektirir. İkisi de `run_matrix.py`'nin tek bir koşumundan (her görev ×
model için hem `tr` hem `en`) çıkar; ek altyapı gerekmez, yalnızca ayrı
raporlanır. Ayrıntı: `README.md`.

## 2. Metodoloji: İki Düzlemli Değerlendirme Mimarisi
LLM tabanlı benchmark'ların kronik sorunu, "ölçümün deterministik
olmaması"dır — testleri veya skoru bir LLM üretirse, ground truth
belirsizleşir ve benchmark bilimsel olarak çöker. Bu riski kökten yok
etmek için süreci iki düzleme ayırıyoruz:

```
┌─────────────────────────────────────────────────────────┐
│  DÜZLEM 1 — YARATICI AJAN FABRİKASI (Claude API)         │
│  Yalnızca "yaratıcı" işlerden sorumlu; hakemlik yapamaz. │
│   • Mutator Ajanı     → hikaye/parametre varyantı üretir │
│   • Translator Ajanı  → TR↔EN paralel prompt üretir      │
│   • Test-Öneri Ajanı  → ADAY test girdileri önerir       │
│   • Failure-Classifier→ hata tipini sınıflar (taksonomi) │
└───────────────────────────┬─────────────────────────────┘
                            │ ÜRETİR (ham, güvenilmez)
                            ▼  [her çıktı doğrulama kapısından geçer]
┌─────────────────────────────────────────────────────────┐
│  DÜZLEM 2 — DETERMİNİSTİK ORACLE (saf kod · hakem)       │
│  Benchmark'ın hakemidir; LLM "tahmini" buraya karışamaz. │
│   • Referans-Çözüm Doğrulayıcı → varyantı/testi ONAYLAR  │
│   • Docker Sandbox Executor    → izole gerçek çalıştırma  │
│   • Metrik Motoru              → pass@k, vergiler (KOD)   │
└─────────────────────────────────────────────────────────┘
```

**Doğrulama Kapısı (guardrail):** Düzlem 1'in ürettiği hiçbir şeye
doğrudan güvenilmez. Bir varyant/test üretildiğinde, önce **referans
çözüm** o varyantın testlerinde Sandbox'ta çalıştırılır; geçerse
dondurulur, geçmezse atılır. Böylece LLM *ölçeği* sağlar (yüzlerce
varyant), doğruluğu ise deterministik oracle **garanti eder.**

**Neden Claude?** Fabrika ajanının hata yapması tüm benchmark'ın çöp
olması demektir. "Cetveli en iyi aletle yap, yerel modelleri o cetvelle
ölç" ayrımı akademik olarak kusursuzdur: cetveli inşa eden model
(Claude) ile test edilen özneler (yerel modeller) birbirinden ayrıdır —
bu, çıkar çatışmasını ve veri kirliliğini engeller.

## 3. Ölçtüğümüz Özgün Metrikler
- **Türkçe Muhakeme Vergisi:** `acc(en) − acc(tr)` — aynı problem
  Türkçe sorulunca başarı ne kadar düşüyor?
- **Ezber Farkı (contamination gap):** `acc(orijinal) − acc(mutasyon)` —
  yüksek fark, gerçek anlama değil ezber demektir.
- **Token Vergisi:** `tokens(tr) / tokens(en)` — Türkçe ~1.5–2 kat token
  harcar; maliyet ve latency etkisi grafiklenir.
- **pass@1, pass@k:** kodun gizli testleri geçme oranı.
- **Hata Taksonomisi:** syntax / runtime / timeout / mantık hatası /
  Türkçe prompt'u yanlış anlama — otomatik sınıflandırma.
- **Ölçek Trendi:** aynı ailenin farklı boyları (0.5B→7B) ile metriklerin
  eğrisi; büyük modeller hakkında dürüst çıkarım (bkz. §6).

## 4. Teknik Yığın
- **Sandbox:** Docker (`--network none`, `--memory`, `--cpus`,
  `--pids-limit`, `--read-only`, non-root, `timeout`).
- **Orkestrasyon:** Düz Python fonksiyon zinciri (`src/agent_factory/client.py`
  + görev-özel ajan modülleri). Gün 13'te LangGraph yeniden değerlendirildi ve
  ASKIYA ALINDI: gerçek ajan zinciri büyük ölçüde doğrusal (Görev → Mutator →
  Guardrail → [Translator]), grafik-tabanlı bir orkestrasyon kütüphanesinin
  sağladığı yetenekler (döngü, çok-yönlü koşullu yönlendirme, kalıcı state)
  şu an karşılığı olmayan bir bağımlılık olurdu. Gerçek çoklu-ajan döngüsel
  karmaşıklık doğarsa yeniden değerlendirilecek (bkz. 20_gunluk_plani.md
  Revizyon Günlüğü).
- **Fabrika ajanları:** Claude Code CLI (headless, `--system-prompt` +
  `--json-schema`) — kullanıcının mevcut Claude Code girişini (abonelik)
  kullanır, ayrı bir `ANTHROPIC_API_KEY` gerektirmez.
- **Test edilen özneler:** yerel modeller — Ollama + LM Studio (ikisi de
  OpenAI-uyumlu endpoint → tek istemci arayüzü).
- **Veri seti:** git ile sürümlenir, HuggingFace Datasets formatında
  yayınlanır (dataset card ile). [DVC opsiyonel.]

## 5. Benchmark Veri Seti Tasarımı
Her görev tek bir JSON nesnesidir; **modele giden** kısım (prompt +
fonksiyon imzası) ile **gizli** kısım (referans çözüm + test case'ler)
ayrıdır. Bir kanonik görevden üç eksende varyant ailesi türetilir:
1. **Parametrik örnekleme** (aynı mantık, farklı sayılar) → ezber testi.
2. **Hikaye mutasyonu** (aynı algoritma, farklı bağlam) → anlama testi.
3. **Dil** (TR↔EN, aynı test setiyle) → Türkçe vergisi.

Problemler kirlilik-güvenli kaynaktan gelir: ağırlıklı **özgün** yazım +
parametrik taze örnekler (HackerRank vb. kazınmaz). Hedef ölçek:
~30–40 kanonik görev × ~4–6 varyant ≈ 150–200 değerlendirme birimi.
Kategoriler: diziler, string, matematik, mantık, özyineleme, sayma.

## 6. Donanım Kısıtı ve Çözümü
Makine: i7-11800H, 15 GB RAM, RTX 3050 Ti **4 GB VRAM**. Bu, kurumsal
70B modelleri test etmeye yetmez; dolayısıyla "şu modeli kur" tarzı bir
tavsiye aracı kapsam dışıdır. Bunun yerine **ölçek trendi**: aynı ailenin
0.5B→7B boyları test edilip bir eğri çıkarılır ("Türkçe vergisi büyüdükçe
azalıyor ama sıfırlanmıyor"). Bu, laptopla üretilen ama büyük modeller
hakkında da söz söyleyen dürüst bir bulgudur.

## 7. İnşa Yol Haritası (staj günlerine oturur)
1. **Docker Sandbox** — elle yazılmış kodu izole çalıştır, geçti/kaldı dön.
2. **Test Oracle** — referans çözüm + `assert` tabanlı doğrulama.
3. **Model Client** — 1 yerel modelden (ör. gemma2:2b) kod al.
4. **Uçtan-uca dikey dilim** — 1 görev → model → sandbox → sonuç.
5. **Mutator ajanı** (Claude) — varyant üret + oracle ile doğrula.
6. **Metrik motoru** — taksonomi, vergiler, trend.
7. ~~LangGraph ile bileşenleri orkestre et~~ — askıya alındı (bkz. §4);
   düz Python zinciri yeterli.
8. **Dashboard (Gradio)** — canlı demo, en son ince kabuk.
9. **HuggingFace yayını** + dataset card.

## 8. Değer
- **Akademik:** Yeni bir benchmark inşa etmek, alanın en saygın katkı
  türüdür — skor tutmak değil, standardı kurmak. İki-düzlemli mimari,
  "LLM'e nerede güvenilir nerede güvenilmez" ayrımını göstererek
  metodolojik olgunluk sergiler.
- **Gerçek-dünya:** Türkçe + on-prem + çalıştırılabilir açık bir kod
  değerlendirme seti; benimsenme (adoption) yoluyla referans standardı
  olabilir.
