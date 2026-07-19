# TR-CodeEval — Türkçe, Çalıştırma-Tabanlı, Kirlilik-Dirençli Kod Değerlendirme Takımı

Yerel açık-kaynak dil modellerinin kod problemlerini *gerçekten anlayıp
anlamadığını* ölçen, yeniden kullanılabilir bir **değerlendirme takımı
(benchmark)**. Katkı bir model çalıştırmak değil; herkesin kendi modelini
geçirebileceği **ölçü aletini** kurmaktır.

Var olan kod benchmark'larından üç eksende ayrışır: **(1) Türkçe**,
**(2) ezber-dayanıklılığı** (mutasyon), **(3) çalıştırma-tabanlı** gerçek
doğrulama. Ayrıntılı gerekçe: [`docs/proje_yon_raporu.md`](docs/proje_yon_raporu.md).

> **Durum (Gün 10/20):** Deterministik çekirdek (Docker sandbox + oracle),
> yerel model istemcisi ve çok-modelli koşum matrisi çalışıyor ve testli.
> Veri seti henüz küçük (büyütme Gün 11-12). İlerleme:
> [`docs/20_gunluk_plani.md`](docs/20_gunluk_plani.md).

## Mimari — İki Düzlem

```
DÜZLEM 1 — Yaratıcı Ajan Fabrikası (Claude API)   [yol haritası: Gün 13-14]
  varyant/test/çeviri üretir · güvenilmez · her çıktı doğrulama kapısından geçer
        │
        ▼
DÜZLEM 2 — Deterministik Oracle (saf kod · hakem)  [KURULU]
  • Docker Sandbox Executor  → izole gerçek çalıştırma   (src/sandbox)
  • Referans-Çözüm Doğrulayıcı → görevi/varyantı ONAYLAR (src/oracle)
  • Metrik Motoru → pass@k, vergiler                     [Gün 15]
```

Karar (pass/fail) hiçbir zaman bir LLM'e bırakılmaz; yalnızca gerçek kod
yürütmesi verir. Model çıktısı **test edilen özne**dir, hakem değil.

## Kurulum

```bash
# 1) İzole, tekrarlanabilir Python ortamı
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Sandbox temel imajını derle (bir kez)
docker build -t trc-sandbox:latest src/sandbox

# 3) Yerel model sunucusu (test edilen özneler) — Ollama örneği
ollama serve &
ollama pull qwen2.5:1.5b        # 4 GB VRAM'e uygun küçük modeller
```

## Kullanım

```bash
# Sandbox + oracle self-test (model gerektirmez)
python src/sandbox/executor.py
python src/oracle/task_validator.py

# Tek görev, uçtan uca: görev -> model -> sandbox -> pass/fail
python src/run_task.py --model qwen2.5:1.5b --dil tr

# Çoklu-model matris. Greedy (kararlılık) ya da örnekleme (gerçek pass@k):
python src/run_matrix.py --tekrar 3                       # sicaklik=0: kararlılık
python src/run_matrix.py --tekrar 5 --sicaklik 0.4        # gerçek pass@k

# Testler (birim + Docker entegrasyon)
python -m pytest -v
```

## Ölçülen Metrikler (ve dürüst uyarılar)

- **Türkçe muhakeme vergisi:** `acc(en) − acc(tr)`.
- **Ezber farkı:** `acc(orijinal) − acc(mutasyon)` — [Gün 13 sonrası].
- **Token vergisi:** `tokens(tr) / tokens(en)`.
- **pass@1, pass@k:** kodun gizli testleri geçme oranı.

> **Determinizm uyarısı:** Düşük VRAM'de yerel çıkarım, sabit seed +
> `temperature=0` ile bile bit-tekrarlanabilir DEĞİLDİR (model takası +
> kısmi GPU offload). Bu yüzden `run_matrix` her hücreyi K kez örnekler;
> `sicaklik=0`'da anlamlı olan **kararlılık**tır, `sicaklik>0`'da **pass@k**.
> İkisi karıştırılmaz. Küçük veri setinde tek bir sonucu kesin bir bulgu
> gibi sunmaktan kaçınılır.

## Proje Yapısı

```
src/
  sandbox/      Docker sandbox: Dockerfile, harness (container-içi), executor (host)
  oracle/       Referans-çözüm doğrulayıcı (guardrail)
  model_client/ Ollama/LM Studio istemcisi + kod prompt/ayıklama
  run_task.py   Tek görev dikey dilim
  run_matrix.py Çoklu-model × dil koşum matrisi (JSON + CSV)
  prompt_builder.py   [Faz 1 arşivi — aşağıya bakınız]
data/tasks/     Kanonik kod görevleri (trc_*.json)
tests/          Birim + Docker entegrasyon testleri (pytest)
docs/           Yön raporu, 20 günlük plan, staj defteri
results/        Koşum çıktıları (JSON/CSV)
```

## İki Track Hakkında (kimlik notu)

Bu depo iki iz taşır:

1. **Kod-değerlendirme (asıl proje).** Yukarıda anlatılan her şey.
   `data/tasks/`, `src/sandbox|oracle|model_client`, `run_task`, `run_matrix`.
2. **Çoktan-seçmeli (Faz 1 öğrenme arşivi).** `data/sample_questions.json` ve
   `src/prompt_builder.py`, stajın ilk günlerinde (Gün 5-6) değerlendirme
   mantığını öğrenmek için yazıldı. Asıl kod-değerlendirme hattı bunları
   kullanmaz; öğrenme kaydı olarak korunur, silinmez.

## Donanım Notu

Geliştirme makinesi 4 GB VRAM'lidir; kurumsal büyük modeller test edilmez.
Bunun yerine aynı ailenin farklı boyları (0.5B→3B) ile **ölçek trendi**
çıkarılır — laptopla üretilen ama büyük modeller hakkında da söz söyleyen
dürüst bir yaklaşım.
