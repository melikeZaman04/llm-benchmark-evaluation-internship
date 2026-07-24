# Staj Defteri Günlükleri

## 1. Gün - Proje Yapısının Oluşturulması

Bugün LLM benchmark değerlendirme projesinin temel yapısı oluşturuldu. Projenin amacı, büyük dil modellerinin benchmark veri setleri ve değerlendirme metrikleri üzerinden nasıl ölçüldüğünü öğrenmek olarak belirlendi. Bu kapsamda sıfırdan büyük bir model eğitmek yerine, küçük ve yönetilebilir örnekler üzerinden değerlendirme mantığını anlamaya odaklanılmasına karar verildi.

GitHub üzerinde proje takibi için Kanban tabanlı bir Project board kullanılması konuşuldu. Ayrıca docs, notebooks, src, data ve results klasörlerinden oluşan temel repository yapısı hazırlandı. README dosyasında projenin amacı, kapsamı, kapsam dışı konuları, kullanılacak araçlar ve 20 iş günlük ilerleme mantığı açıklandı.

Gün sonunda README.md, requirements.txt ve staj defteri günlüklerini tutmak için docs/staj_defteri_gunlukleri.md dosyası oluşturuldu.

### Bugün Öğrenilenler

* LLM benchmark değerlendirme projesinin amacı netleştirildi.
* Proje klasör yapısının düzenli olmasının deneylerin takip edilebilirliği için önemli olduğu görüldü.
* Staj sürecinde her gün somut bir çıktı üretmenin proje takibini kolaylaştıracağı öğrenildi.

### Oluşturulan Çıktılar

* README.md
* requirements.txt
* docs/staj_defteri_gunlukleri.md
* docs/
* notebooks/
* src/
* data/
* results/
* results/figures/

### Bir Sonraki Adım

Bir sonraki gün LLM, benchmark ve değerlendirme kavramları araştırılarak docs/01_llm_benchmark_giris.md dosyası hazırlanacaktır.

## 2. Gün - LLM, Benchmark ve Değerlendirme Kavramlarının İncelenmesi

Bugün LLM, benchmark, benchmark veri seti ve model değerlendirme süreci gibi temel kavramlar incelendi. Büyük dil modellerinin yalnızca çıktı üretmek için değil, aynı zamanda doğru, tutarlı ve ölçülebilir cevaplar üretip üretmediğini anlamak için de değerlendirilmesi gerektiği görüldü.

Benchmark kavramının, farklı modelleri aynı koşullar altında karşılaştırmak için kullanılan standart bir test yapısı olduğu açıklandı. Ayrıca benchmark veri seti ile normal veri seti arasındaki fark ele alındı. Benchmark veri setlerinin model başarımını ölçmek için soru, beklenen cevap, görev türü ve değerlendirme bilgisi gibi alanlar içerebileceği öğrenildi.

Gün sonunda `docs/01_llm_benchmark_giris.md` dosyası hazırlandı. Bu dosya, ilerleyen günlerde yapılacak veri seti hazırlama ve metrik hesaplama çalışmalarına kavramsal temel oluşturacaktır.

### Bugün Öğrenilenler

* LLM kavramının model değerlendirme açısından nasıl ele alınacağı öğrenildi.
* Benchmarkların modelleri karşılaştırmak için standart test yapısı sunduğu görüldü.
* Benchmark veri setlerinin doğru cevap ve değerlendirme formatı içermesinin önemli olduğu anlaşıldı.
* Küçük örneklerle başlamanın proje kapsamı için daha uygun olduğu belirlendi.

### Oluşturulan Çıktılar

* docs/01_llm_benchmark_giris.md

### Bir Sonraki Adım

Bir sonraki gün yaygın LLM benchmark veri setleri araştırılarak `docs/02_benchmark_veri_setleri.md` dosyası hazırlanacaktır.

## 3. Gün - Yaygın LLM Benchmark Veri Setlerinin İncelenmesi

Bugün yaygın LLM benchmark veri setleri incelendi. MMLU, GSM8K, ARC, HellaSwag, TruthfulQA, HumanEval, SQuAD, GLUE ve SuperGLUE gibi benchmarkların hangi görevleri ölçtüğü araştırıldı. Her veri setinin cevap formatı ve yaygın değerlendirme metriği karşılaştırmalı olarak ele alındı.

Çalışmada özellikle çoktan seçmeli soru cevaplama, matematiksel akıl yürütme, fen bilgisi, sağduyu çıkarımı, doğruluk, kod üretme ve okuduğunu anlama gibi farklı benchmark türleri incelendi. Ayrıca Türkçe LLM değerlendirmesi için TR-MMLU, Cetvel ve TurkBench gibi örnek benchmark çalışmaları not edildi.

Gün sonunda `docs/02_benchmark_veri_setleri.md` dosyası hazırlandı. Bu dosya, ilerleyen günlerde hangi benchmark türünün proje için daha uygun olacağını belirlemeye yardımcı olacaktır.

### Bugün Öğrenilenler

* LLM benchmarklarının tek tip olmadığı, farklı becerileri ölçtüğü öğrenildi.
* Çoktan seçmeli benchmarklarda accuracy metriğinin sık kullanıldığı görüldü.
* Serbest metin, kod üretimi ve okuduğunu anlama görevlerinde değerlendirmenin daha karmaşık olabileceği anlaşıldı.
* Türkçe benchmarkların, Türkçenin dil yapısı ve kültürel bağlamı nedeniyle ayrıca önemli olduğu görüldü.

### Oluşturulan Çıktılar

* docs/02_benchmark_veri_setleri.md

### Bir Sonraki Adım

Bir sonraki gün LLM değerlendirme metrikleri incelenerek `docs/03_degerlendirme_metrikleri.md` dosyası hazırlanacaktır.

## 4. Gün - Değerlendirme Metriklerinin İncelenmesi

Bugün Day 04 çalışmasına başlamadan önce Day 03 çıktıları kontrol edildi. `docs/02_benchmark_veri_setleri.md` dosyasının istenen başlıklarla oluşturulduğu görüldü. Ancak staj defteri günlüklerinde 2. ve 3. gün kayıtlarının eksik olduğu fark edildi. Bu eksik tamamlanarak staj defterine geçmiş günlerin özetleri eklendi.

Daha sonra LLM benchmark değerlendirmelerinde kullanılan temel metrikler incelendi. Accuracy, Exact Match, precision, recall, F1, BLEU, ROUGE, pass@k ve format compliance metriklerinin hangi görevlerde kullanıldığı açıklandı. Ayrıca insan değerlendirmesi ve LLM-as-a-Judge yaklaşımının hangi durumlarda gerekli olabileceği değerlendirildi.

Gün sonunda `docs/03_degerlendirme_metrikleri.md` dosyası hazırlandı. Bu dosya, ilerleyen günlerde küçük bir Türkçe soru-cevap veri seti üzerinde accuracy ve format uyumu gibi metriklerin hesaplanması için temel oluşturacaktır.

### Bugün Öğrenilenler

* Her benchmark türü için aynı metriğin uygun olmadığı öğrenildi.
* Çoktan seçmeli ve kısa cevaplı görevlerde accuracy ve exact match metriklerinin kullanışlı olduğu görüldü.
* Serbest metin cevaplarda otomatik değerlendirmenin daha zor olduğu anlaşıldı.
* Format uyumunun LLM değerlendirmelerinde doğruluk kadar önemli olabileceği görüldü.
* Bu proje için başlangıçta accuracy, exact match ve format compliance metriklerinin uygun olduğu belirlendi.

### Oluşturulan Çıktılar

* docs/03_degerlendirme_metrikleri.md
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün küçük ve yönetilebilir bir Türkçe benchmark veri seti taslağı hazırlanarak değerlendirme sürecinin uygulama kısmına geçilecektir.

## 5. Gün - İlk Küçük Çoktan Seçmeli Veri Setinin Hazırlanması

Bugün Day 05 kapsamında küçük ve yönetilebilir bir Türkçe çoktan seçmeli benchmark veri seti hazırlanıp doğrulandı. Day 04'te incelenen accuracy, exact match ve format compliance metriklerine uygun olacak şekilde, modelden yalnızca A, B, C veya D seçeneklerinden birini üretmesi beklenen bir veri yapısı tercih edildi.

Veri seti `data/sample_questions.json` dosyasında oluşturuldu. Dosyada genel bilgi, matematik, mantık, fen ve Türkçe kategorilerinden toplam 12 soru yer aldı. Her soruda soru metni, `choices` alanı içinde A, B, C ve D seçenekleri, `answer` alanında beklenen cevap harfi, kategori ve zorluk bilgisi bulunacak şekilde düzenli bir JSON yapısı kullanıldı.

Bu çalışma sırasında herhangi bir model çalıştırılmadı ve metrik hesaplanmadı. Amaç, Day 06'da tasarlanacak prompt formatı için hazır ve küçük bir benchmark girdisi oluşturmaktı.

### Bugün Öğrenilenler

* Çoktan seçmeli benchmark verisinin düzenli alanlara sahip olması gerektiği görüldü.
* Beklenen cevabın standart bir `answer` alanında A, B, C veya D harfi olarak tutulmasının ileride değerlendirmeyi kolaylaştıracağı anlaşıldı.
* Format compliance ölçümü için modelden istenecek cevap biçiminin veri seti tasarımında da net olması gerektiği öğrenildi.
* Küçük veri setlerinde kategori ve seçenek dağılımının kontrol edilmesinin önemli olduğu görüldü.

### Oluşturulan Çıktılar

* data/sample_questions.json
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün bu veri setindeki sorular için modelden yalnızca tek bir seçenek harfi almayı hedefleyen prompt formatı tasarlanacaktır.

## 6. Gün - Prompt Formatının Tasarlanması

Bugün LLM benchmark değerlendirme projesinde kullanılacak prompt formatı tasarlandı. Önceki gün hazırlanan küçük çoktan seçmeli veri setindeki soruların modele nasıl sunulacağı incelendi. Bu kapsamda modelden yalnızca A, B, C veya D seçenek harfiyle cevap alınmasını hedefleyen sade bir prompt yapısı oluşturuldu.

Prompt formatında soru metni, dört seçenek ve modelden beklenen çıktı biçimi açıkça belirtildi. Modelin uzun açıklama üretmesini engellemek için prompt içinde yalnızca seçenek harfi istenmesine dikkat edildi. Bu yapı ilerleyen günlerde model cevaplarının daha kolay normalize edilmesini ve format compliance ölçümünün daha düzenli yapılmasını sağlayacaktır.

`src/prompt_builder.py` dosyasında tek bir soru nesnesini prompt metnine dönüştüren `build_prompt` fonksiyonu hazırlandı. Ayrıca birden fazla soru için prompt üretmeye uygun `build_prompts` fonksiyonu eklendi. Soru nesnesinin gerekli alanlara sahip olup olmadığını kontrol etmek için `validate_question_item` fonksiyonu kullanıldı. Bu sayede ilerleyen aşamalarda veri setindeki tüm sorular için standart promptlar üretilebilecektir.

Bu gün herhangi bir model çalıştırılmadı, model çıktısı alınmadı ve metrik hesaplanmadı. Çalışma yalnızca değerlendirme deneylerinde kullanılacak prompt formatının hazırlanması amacıyla tamamlandı.

### Bugün Öğrenilenler

* Prompt formatının model çıktısını doğrudan etkileyebileceği öğrenildi.
* Çoktan seçmeli görevlerde modelden yalnızca seçenek harfi istemenin değerlendirmeyi kolaylaştıracağı görüldü.
* Standart prompt yapısının deneylerin tekrar edilebilirliği için önemli olduğu anlaşıldı.
* Format compliance ölçümü için promptun açık ve sınırlayıcı olması gerektiği öğrenildi.
* Prompt oluşturma işleminin ayrı bir Python dosyasında tutulmasının proje düzenini artıracağı görüldü.

### Oluşturulan Çıktılar

* src/prompt_builder.py
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün modelden cevap alma sürecinin temel yapısı planlanacaktır. `src/run_model.py` dosyası hazırlanacak ve model çıktılarının nasıl kaydedileceği belirlenecektir. Gerçek deneylere geçmeden önce bu yapı küçük örnekler üzerinden kontrollü şekilde ilerletilecektir.

## 7. Gün - Docker Sandbox ve Referans-Çözüm Oracle'ının Kurulması

Bugün projenin iki-düzlemli mimarisindeki "Deterministik Oracle" katmanının çekirdeği kuruldu. Amaç, değerlendirilecek kodun (referans çözüm ya da ileride model çıktısı) ana sisteme zarar veremeyecek şekilde izole bir Docker container'ında çalıştırılıp gizli testlere sokulmasıdır. Bu sayede geçti/kaldı kararı bir LLM'e değil, gerçek kod yürütmesine bırakılır.

`src/sandbox/` altında güvenli çalıştırma altyapısı hazırlandı. `Dockerfile` root olmayan bir kullanıcıyla çalışan sade bir Python 3.11 imajı tanımlar. Container içinde çalışan `harness.py`, kodu bir modül olarak yükleyip her test case'ini çalıştırır ve sonucu tek bir JSON satırı olarak döndürür; syntax, import, eksik fonksiyon, runtime ve mantık hatalarını ayrı ayrı sınıflar. Host tarafındaki `executor.py`, kodu geçici bir klasöre yazıp Docker'ı sertleştirme bayraklarıyla çağırır ve çıktıyı deterministik biçimde ayrıştırır.

Güvenlik önlemleri gerçek saldırı senaryolarıyla sınandı: ağ erişimi (`--network none`) engellendi, kök dosya sistemine yazma (`--read-only`) reddedildi, sonsuz döngü duvar-saati `timeout` ile kesildi ve fork bombası `--pids-limit` ile durduruldu. Host dosya sisteminin dokunulmadan kaldığı doğrulandı.

`src/oracle/task_validator.py` ile guardrail'in temeli kuruldu: bir görevin geçerli sayılması için kendi referans çözümünün kendi testlerini Sandbox'ta eksiksiz geçmesi gerekir. İlk kanonik görev `data/tasks/trc_001.json` (bütçeyle maksimum ürün) bu doğrulamadan 6/6 ile geçti. Ayrıca projenin genel yönünü açıklayan `docs/proje_yon_raporu.md` eklendi.

### Bugün Öğrenilenler

* Değerlendirme kararının deterministik olması için pass/fail yargısının koda bırakılması gerektiği pekişti.
* Güvenli sandbox tasarımında ağ, dosya sistemi, süreç ve süre limitlerinin birlikte ele alınması gerektiği görüldü.
* Bir görevin veri setine alınmadan önce referans çözümüyle doğrulanmasının benchmark güvenilirliği için kritik olduğu anlaşıldı.
* Ayırt edici (sırasız liste gibi) test case'lerin, zayıf çözümleri yakalamak için benchmark kalitesini artırdığı görüldü.

### Oluşturulan Çıktılar

* src/sandbox/Dockerfile
* src/sandbox/harness.py
* src/sandbox/executor.py
* src/sandbox/README.md
* src/oracle/task_validator.py
* data/tasks/trc_001.json
* docs/proje_yon_raporu.md
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün yerel model istemcisi (Ollama / LM Studio, OpenAI-uyumlu endpoint) hazırlanacak ve tek bir görev için modelden kod alınıp Sandbox'tan geçirileceği uçtan-uca dikey dilim denenecektir.

## 8. Gün - Yerel Model İstemcisinin Hazırlanması

Bugün, benchmark'ın değerlendirdiği yerel dil modellerinden kod çıktısı almak için bir istemci katmanı hazırlandı. Yol haritasındaki 3. adıma karşılık gelen bu iş, iki-düzlemli mimarinin "test edilen özne" tarafına dokunur; üretilen kod güvenilmez kabul edilir ve doğru/yanlış kararı önceki günlerde kurulan Sandbox + Oracle'a bırakılır.

Ollama ve LM Studio'nun ikisinin de OpenAI-uyumlu `/v1/chat/completions` arayüzü sunduğu gözlemlendi; bu yüzden her ikisiyle de çalışan tek bir `ModelIstemcisi` sınıfı yazıldı. Sağlayıcı yalnızca `base_url` ile ayrışıyor: Ollama için `localhost:11434/v1`, LM Studio için `localhost:1234/v1`. Model adı ve endpoint `TRC_MODEL` / `TRC_MODEL_BASE_URL` ortam değişkenleriyle de verilebiliyor. İstemci; bağlantı hatası, timeout, HTTP hata kodu ve beklenmeyen yanıt biçimi durumlarını açık Türkçe mesajlarla `ModelBaglantiHatasi` olarak yükseltiyor.

`code_task.py` içinde görev ile model arasındaki köprü kuruldu. `kod_prompt_olustur` bir görevi (trc_*.json) modele verilecek kod-üretim prompt'una çeviriyor ve TR/EN dili seçilebiliyor; bu, ilerideki "Türkçe muhakeme vergisi" ölçümünün temelini oluşturuyor. `kod_ayikla` ise modelin çoğu zaman markdown kod bloğu ve açıklama içeren ham yanıtından yalnızca çalıştırılabilir Python fonksiyonunu güvenilir biçimde çıkarıyor (`def` içeren ilk blok tercih ediliyor). `modelden_cozum_al` bu adımları tek çağrıda birleştirip Sandbox'a verilmeye hazır kodu döndürüyor.

Model gerektirmeyen kısımlar (prompt üretimi ve kod ayıklama) çevrimdışı doğrulandı. Ollama servisi ayağa kaldırıldı; henüz bir model indirilmediği için istemci beklendiği gibi net bir "model not found" mesajı verdi. Bu, gerçek uçtan-uca çalıştırmadan önce küçük bir modelin (ör. `gemma2:2b`) indirilmesi gerektiğini gösterdi.

### Bugün Öğrenilenler

* Ollama ve LM Studio'nun ortak OpenAI-uyumlu arayüz sayesinde tek bir istemciyle soyutlanabildiği görüldü.
* Model çıktısının ham metin olduğu ve prompt/kod ayıklamanın deterministik biçimde ayrı tutulmasının değerlendirmeyi kolaylaştırdığı anlaşıldı.
* Aynı görevin TR ve EN sorulabilmesinin dil-vergisi metriği için tasarıma baştan yerleştirilmesi gerektiği pekişti.
* Yerel model istemcisinde bağlantı/timeout/hata durumlarının açık mesajlarla ele alınmasının hata ayıklamayı kolaylaştırdığı görüldü.

### Oluşturulan Çıktılar

* src/model_client/client.py
* src/model_client/code_task.py
* src/model_client/README.md
* src/model_client/__init__.py
* Güncellenmiş requirements.txt (requests)
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün küçük bir model (ör. `gemma2:2b`) indirilip uçtan-uca dikey dilim tamamlanacaktır: tek bir görev modele sorulacak, dönen kod Sandbox'ta gizli testlere karşı çalıştırılacak ve pass/fail sonucu alınacaktır (yol haritası 4. adım).

## 9. Gün - Uçtan-Uca Dikey Dilim ve Tekrarlanabilirlik

Bugün yol haritasının 4. adımı olan uçtan-uca dikey dilim tamamlandı: tek bir görev `görev → prompt → yerel model → kod → Sandbox → pass/fail` zincirinin tamamından geçirildi. `src/run_task.py` bu akışı tek komutla çalıştırıyor ve `--model`, `--dil` (tr/en), `--saglayici` bayraklarını destekliyor. Böylece iki-düzlemli mimari küçük ölçekte fiilen kanıtlandı: model (test edilen özne) kodu üretti, doğru/yanlış kararını ise yalnızca deterministik Sandbox verdi.

4 GB VRAM'e uygun küçük modeller indirildi (`qwen2.5` ailesi 0.5B/1.5B/3B, ayrıca `llama3.2:3b`, `gemma2:2b`). İlk kanonik görev trc_001, üç Qwen boyutu ile hem Türkçe hem İngilizce koşuldu. Boru hattının doğru çalıştığı net biçimde görüldü; örneğin qwen2.5:3b Türkçe koşumda sözdizimi hatalı kod üretti ve Sandbox bunu deterministik olarak `syntax` hatasıyla yakaladı (0/6).

Koşumlar sırasında önemli bir metodolojik sorun keşfedildi: `temperature=0` olmasına rağmen aynı model+dil ikilisi koşumdan koşuma farklı sonuç verebiliyordu (bir denemede 6/6, diğerinde 5/6). Bunun nedeni Ollama'nın seed sabitlenmediğinde tam tekrarlanabilir olmamasıdır. Bir benchmark için pass@1'in anlamlı olması koşumun deterministik olmasına bağlı olduğundan, model istemcisine sabit `seed` (varsayılan 0) parametresi eklendi. Sabit seed + temperature=0 ile aynı tarama iki kez çalıştırıldığında sonuçların birebir aynı olduğu doğrulandı.

Sabit seed altında dürüst sonuç şu oldu: küçük modeller trc_001'i deterministik olarak tam geçemedi (en iyi 5/6). Bu aslında olumlu bir bulgudur; görevdeki ayırt edici test case ([10, 3, 3, 3] bütçe 10 → 3) sıralama yapmayan zayıf çözümleri yakalayarak benchmark'ın ayrıştırıcı olduğunu gösterdi. Ayrıca "Türkçe muhakeme vergisi"nin ilk işareti de belirdi: aynı modeller İngilizce'de Türkçe'ye göre daha yüksek puan aldı. Koşum kanıtı `results/gun09_dikey_dilim.json` dosyasına kaydedildi.

### Bugün Öğrenilenler

* Uçtan-uca dikey dilimin, mimarinin tamamını küçük ölçekte doğrulayan en değerli erken adım olduğu görüldü.
* Ollama'nın temperature=0'da bile seed olmadan tam tekrarlanabilir olmadığı; benchmark için sabit seed'in şart olduğu öğrenildi.
* Ayırt edici test case'lerin, zayıf çözümleri deterministik biçimde eleyerek benchmark kalitesini belirlediği pekişti.
* Aynı görevin TR/EN koşulabilmesinin, dil vergisi sinyalini daha ilk koşumda görünür kıldığı gözlendi.

### Oluşturulan Çıktılar

* src/run_task.py
* results/gun09_dikey_dilim.json
* Güncellenmiş src/model_client/client.py (sabit seed)
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün (Gün 10) koşum çok-modelli ve çok-dilli hale getirilecek; sonuçlar `results/` altında yapılandırılmış bir şemada (model × dil × görev) toplanacak ve metrik motorunun (Gün 15) girdisi hazırlanacaktır.

## 10. Gün - Çoklu-Model Koşum Matrisi ve Determinizm Gerçeği

Bugün koşum çok-modelli ve çok-dilli hale getirildi. `src/run_matrix.py`, bir görev kümesini (görev × model × dil) matrisi olarak koşup sonuçları hem JSON hem CSV biçiminde `results/` altına kaydediyor. Beş yerel model (`qwen2.5` 0.5B/1.5B/3B, `llama3.2:3b`, `gemma2:2b`) trc_001 üzerinde TR ve EN dillerinde koşuldu.

Gün 9'da sabit seed + temperature=0 ile ardışık iki koşumun birebir aynı çıktığını gözlemlemiştik. Bugün bu bulgu daha geniş koşulda sınandı ve dürüstçe rafine edildi: sabit seed **yalnızca koşullar birebir aynıyken** determinizm sağlıyor. Beş model art arda koşulup VRAM'de takas edildiğinde (4 GB VRAM'de kısmi GPU offload + kayan-nokta işlemlerinin sırasının değişmesi), aynı hücre koşumdan koşuma ±1 test oynayabiliyor. Yani yerel çıkarım bu donanımda **bit-tekrarlanabilir değil**; pass@1 tek başına gürültülü bir ölçüdür.

Bu gerçeğe verilen yanıt olarak runner'a `--tekrar K` eklendi: her hücre K kez örnekleniyor ve tüm örnekler saklanıyor. Kayıt her hücre için `gecti_sayisi/K`, geçen-test aralığı (min–max) ve bir `kararli` bayrağı (K örnek birbirinin aynı mı?) tutuyor. Bu, gürültüyü gizlemek yerine şeffaf biçimde kaydediyor ve Gün 15'te hesaplanacak pass@k metriğinin ham girdisini oluşturuyor. K=3 ile koşulan matriste 10 hücrenin 3'ü kararsız çıktı — pass@1'e güvenmemek gerektiğinin somut kanıtı.

Metodolojik gürültünün ötesinde, projenin ana araştırma sinyali güçlü biçimde belirdi. **Türkçe muhakeme vergisi** her modelde görünür: İngilizce geçme oranı Türkçe'den yüksek ya da eşit. En çarpıcı örnek gemma2:2b — İngilizce'de 3/3 kararlı biçimde geçerken Türkçe'de 0/3. gemma2:2b bu görevde en güçlü ve en kararlı model oldu; llama3.2:3b ise her iki dilde de yetersiz/çok kısa kod üretti. Sonuçlar `results/gun10_matris.json` ve `results/gun10_matris.csv` dosyalarına yazıldı.

### Bugün Öğrenilenler

* Yerel çıkarımın düşük VRAM'de sabit seed'le bile bit-tekrarlanabilir olmadığı, dolayısıyla pass@1 yerine çok-örnekli pass@k'ye ihtiyaç duyulduğu görüldü.
* Ölçüm gürültüsünü gizlemek yerine (kararlılık bayrağıyla) şeffaf kaydetmenin bilimsel dürüstlük açısından doğru yaklaşım olduğu pekişti.
* Türkçe vergisinin küçük modellerde çok belirgin olduğu (gemma2:2b: EN 3/3, TR 0/3) somut veriyle doğrulandı.
* Yapılandırılmış JSON + düz CSV çıktının, ileride metrik motoru ve dashboard için ortak bir sözleşme oluşturduğu görüldü.

### Oluşturulan Çıktılar

* src/run_matrix.py
* results/gun10_matris.json
* results/gun10_matris.csv
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bir Sonraki Adım

Bir sonraki gün (Gün 11) veri seti büyütülmeye başlanacak: dizi/string/matematik kategorilerinde 8–10 yeni kanonik görev yazılıp her biri Oracle ile doğrulanacak; böylece matris tek görevden çıkıp anlamlı bir kapsama ulaşacaktır.

## Ara Çalışma - Mühendislik Sağlamlaştırması (Jüri Eleştirileri)

Gün 11'e geçmeden önce, projeye sert bir öz-değerlendirme (seçici jüri bakışı) uygulandı ve tespit edilen mühendislik açıkları kapatıldı. Bu ara çalışma yeni bir gün numarası açmaz; plandaki tampon mantığına yaslanır ve kalan günlerin değerini artırır.

Kapatılan açıklar:

* **Güvenlik/doğruluk — sandbox stdout açığı:** Değerlendirilen kod `print` yaparsa host'un JSON ayrıştırması bozuluyordu ve çıktı host belleğine sınırsız akıyordu. Harness artık kodun tüm stdout'unu baskılıyor; yalnızca kendi tek JSON satırını gerçek stdout'a yazıyor. Host ayrıca yalnızca son satırı ayrıştırıyor.
* **Güvenlik sertleştirmesi:** Container'a `--cap-drop ALL` ve `--security-opt no-new-privileges` eklendi (yetenek düşürme + setuid ile yetki yükseltmeyi engelleme).
* **Doğruluk — karşılaştırma modları:** Harness artık tam eşitliğin yanında `yaklasik` (float toleransı) ve `sirasiz` (sıra önemsiz) modlarını destekliyor; görev şemasına `karsilastirma` alanı eklendi. Bu, yazılabilecek görev tiplerini genişletir.
* **Metodoloji — pass@k düzeltmesi:** Önceki "K örnek = pass@k" çerçevesi hatalıydı; `temperature=0`'da örnekler yalnız donanım gürültüsüyle oynar. Artık gerçek pass@k için `--sicaklik>0` örnekleme (her örneğe farklı seed) ve yansız pass@k tahmincisi var. `sicaklik=0` ise açıkça "kararlılık" ölçümü olarak konumlandırıldı; ikisi karıştırılmıyor.
* **Test altyapısı:** Bir test aracının kendi testi yoktu. `tests/` altında pytest paketi kuruldu (12 birim + 10 Docker entegrasyon = 22 test, hepsi geçiyor). GitHub Actions CI eklendi (imajı derleyip tüm testleri koşuyor).
* **Tekrarlanabilir ortam:** Bağımlılıklar pinlenmemişti ve `pandas` listede olmasına rağmen kurulu değildi. İzole `.venv` kuruldu; `requirements.txt` çekirdek+test için sadeleştirildi; analiz/görselleştirme bağımlılıkları `requirements-analiz.txt`'e ayrıldı.
* **README kimlik krizi:** README eski (çoktan-seçmeli) projeyi anlatıyordu. Gerçek mimariyi (iki-düzlem, sandbox, kod-değerlendirme, determinizm uyarısı) yansıtacak biçimde baştan yazıldı; çoktan-seçmeli track'i açıkça "Faz 1 öğrenme arşivi" olarak konumlandırıldı.

### Bugün Öğrenilenler

* Bir test aracının kendi testlerinin ve CI'sının olmasının, "güvenilir cetvel" iddiasının olmazsa olmazı olduğu pekişti.
* Güvenlik sandbox'ında en sinsi açığın (stdout taşması) doğruluk hatasıyla iç içe olabildiği görüldü.
* pass@k gibi metriklerin ancak doğru örnekleme koşulunda (sıcaklık>0) anlamlı olduğu, metodolojik terimlerin gevşek kullanılmaması gerektiği anlaşıldı.
* Tekrarlanabilirliği vaaz eden bir projenin kendi ortamının da pinlenmiş ve izole olması gerektiği pekişti.

### Oluşturulan Çıktılar

* Güncellenmiş src/sandbox/harness.py, src/sandbox/executor.py (sertleştirme, karşılaştırma modları)
* Güncellenmiş src/run_matrix.py (gerçek pass@k), src/run_task.py, src/oracle/task_validator.py
* tests/ (conftest, test_unit, test_sandbox_integration), pytest.ini
* .github/workflows/tests.yml (CI)
* Yeniden yazılan README.md, requirements.txt, yeni requirements-analiz.txt

### Bir Sonraki Adım

Sağlam zemin hazır. Gün 11'de veri seti büyütmeye güvenle geçilebilir; yeni görevler artık testli oracle, karşılaştırma modları ve tekrarlanabilir ortam üzerine oturacaktır.

## 11. Gün - Veri Seti Büyütme I: Sekiz Kanonik Görev ve Guardrail Kanıtı

Bugün benchmark tek görevlik iskeleden çıkıp anlamlı bir kapsama ulaştı. Veri setine sekiz yeni kanonik görev eklendi ve toplam dokuz göreve (`trc_001`–`trc_009`) çıkıldı. Görevler üç kategoriye dengeli dağıtıldı: **diziler** (max_ürün, ikinci en büyük, benzersiz elemanlar), **string** (palindrom, anagram, Türkçe sesli harf sayımı) ve **matematik** (asallık, basamak toplamı, ortalama). Her görev; Türkçe ve İngilizce prompt, fonksiyon imzası, referans çözüm, altı test case (kenar durumlar dahil: boş liste, boş metin, tek eleman) ve ileride Mutator ajanının kullanacağı bir `sablon` alanı içeriyor.

Görevler bilinçli olarak sandbox'ın üç karşılaştırma modunu da gerçek veriyle sınayacak şekilde seçildi: çoğu görev `tam` eşitlik kullanırken, `benzersizler` (trc_007) sıranın önemsiz olduğu `sirasiz` modunu, `ortalama` (trc_009) ise float toleranslı `yaklasik` modunu kullanıyor. Böylece ara çalışmada eklenen karşılaştırma altyapısı soyut bir yetenek olmaktan çıkıp fiilen kullanılan bir sözleşmeye dönüştü. `sesli_sayisi` (trc_008) görevi ayrıca Türkçe karakterlerin (ı, ö, ü) sandbox'a UTF-8 olarak sorunsuz taşındığını doğruladı.

Günün asıl disiplini **guardrail**'di: hiçbir görev, kendi referans çözümü kendi test case'lerini sandbox'ta EKSİKSİZ geçmeden veri setine kabul edilmedi. Dokuz görevin tamamı oracle'dan 6/6 ile geçti. Bu, iki-düzlemli mimarinin temel ilkesinin (LLM asla değil, yalnızca deterministik oracle "geçerli"liğe karar verir) elle yazılan görevlere de uygulandığı ilk andı. Bu ilkeyi kalıcı kılmak için, önceden yalnızca trc_001'i sınayan pytest testi tüm `data/tasks/*.json` üzerinde parametrik bir teste dönüştürüldü; artık veri seti her büyüdüğünde guardrail otomatik olarak sınanıyor. Test paketi 22'den 30'a çıktı, hepsi geçiyor.

### Bugün Öğrenilenler

* Bir benchmark'ın "kapsam"ının, kategori çeşitliliği (dizi/string/matematik) ve kenar durum titizliğiyle (boş girdi, tek eleman) ölçüldüğü; birkaç görevin çokluktan değil çeşitlilikten değer kazandığı görüldü.
* Karşılaştırma modlarının (tam/sirasiz/yaklasik) ancak onları kullanan gerçek görevlerle birlikte "tamamlanmış" sayılabileceği; altyapının kullanımla doğrulandığı pekişti.
* Guardrail'in soyut bir ilke değil, çalıştırılabilir ve testle korunan bir kapı olduğu somutlaştı: geçmeyen görev veri setine giremez, ve bu kural artık CI'da yaşıyor.
* Türkçe'ye özgü karakterlerin uçtan uca (JSON → host → container → karşılaştırma) doğru aktığının erkenden doğrulanmasının, ileriki Türkçe-vergisi ölçümleri için zemini güvenceye aldığı görüldü.

### Oluşturulan Çıktılar

* data/tasks/trc_002.json … trc_009.json (8 yeni kanonik görev)
* Güncellenmiş tests/test_sandbox_integration.py (parametrik guardrail regresyon testi)
* Güncellenmiş docs/staj_defteri_gunlukleri.md, docs/20_gunluk_plani.md

### Bir Sonraki Adım

Gün 12'de veri seti mantık/özyineleme/sayma kategorileriyle ~20 göreve büyütülecek; ardından Gün 13'te Mutator ajanı (Claude API) bu kanonik görevlerden oracle-onaylı parametrik varyantlar üretmeye başlayacak. Bugün eklenen `sablon` alanları bu varyant üretiminin girdisi olacak.

## Ara Bulgu - Türkçe/İngilizce Karşılaştırmasında Confound (Kullanıcı Tespiti)

Gün 11'in canlı demolarını kullanıcının kendi terminalinde koşup yorumlarken, kullanıcı önemli bir metodolojik itiraz yaptı: "İngilizce" koşumda bile fonksiyon adı ve parametre adları (`ikinci_en_buyuk`, `sayilar`) Türkçe kalıyor — bu, "Türkçe muhakeme vergisi" iddiasını (acc(en) − acc(tr)) bulandırmıyor mu?

Kod okunarak iki ayrı sorun tespit edildi:

1. **Tanımlayıcı isimleri (identifier) paylaşılıyor** — `fonksiyon_imzasi`/`fonksiyon_adi` görev şemasında tek alan; TR ve EN koşumlarına aynı Türkçe isim gidiyor. Bu bilinçli bir tasarım tercihi olarak bırakıldı (bkz. karar aşağıda).
2. **Daha ciddi olan, gerçek bir hata:** `src/model_client/code_task.py` içinde sistem promptu `dil` parametresinden bağımsız olarak HER ZAMAN Türkçe'ydi (`SISTEM_TR`). Yani "İngilizce" koşumda bile modele Türkçe talimat veriliyordu — kodun kendi docstring'inin vaat ettiği "tek değişken problem dili" iddiasıyla doğrudan çelişen, kontrolsüz bir confound'du.

Kullanıcıyla birlikte kapsam kararlaştırıldı: sistem promptu düzeltilecek (açık hata), tanımlayıcı isimleri ise BİLİNÇLİ sabit olarak bırakılacak (kapsamlı çözüm — her göreve ayrı `fonksiyon_imzasi_en` eklemek — ileri bir güne ertelendi). `SISTEM_EN` eklendi; `modelden_cozum_al` artık `dil`e göre doğru sistem promptunu seçiyor. Karar koda yorum olarak da işlendi ki gelecekte biri "neden tanımlayıcılar hâlâ Türkçe?" diye sorduğunda cevap kodun içinde dursun.

### Bugün Öğrenilenler

* Bir benchmark'ın "iki dilde aynı görevi sorma" iddiasının, yalnızca görünür prompt metnini değil, modele giden HER metni (sistem promptu dahil) kapsaması gerektiği görüldü — gizli/sabit kalan bir kanal bile confound olabilir.
* Kullanıcının kod yazmadan, yalnızca çıktıyı okuyarak deneysel tasarım hatası bulabilmesi, sistemin "kara kutu" değil "anlaşılır" olmasının değerini gösterdi.
* Tam temizlik (tanımlayıcıları da ayırmak) ile hızlı düzeltme (yalnız sistem promptu) arasındaki ayrımın açıkça karara bağlanıp kayıt altına alınmasının, ileride "neden böyle bırakıldı?" sorusuna hazır cevap ürettiği görüldü.

### Oluşturulan Çıktılar

* Güncellenmiş src/model_client/code_task.py (`SISTEM_EN` eklendi, dil'e göre seçim)
* Güncellenmiş docs/staj_defteri_gunlukleri.md

### Bilinen Sınırlılık (açıkça kayıtlı)

Tanımlayıcı isimleri (fonksiyon/parametre adları) hâlâ TR/EN koşumları arasında paylaşılıyor ve her zaman Türkçe. Ölçülen "Türkçe vergisi" bu yüzden şu an saf "problem cümlesi dili" etkisidir + sabit bir Türkçe-tanımlayıcı zemini üzerine oturur; tanımlayıcı dilinin ayrı bir etkisi (varsa) şimdilik ölçülmüyor. İleri bir günde `fonksiyon_imzasi_en` eklenirse bu ayrıştırılabilir.

## 12. Gün - Veri Seti Büyütme II: Kalan Üç Kategori ve 20'ye Tamamlama

Gün 11'de kategori kapsamı 3/6'da (diziler, string, matematik) kalmıştı; bugün kalan üç kategori — **mantık**, **özyineleme**, **sayma** — eklenerek veri seti proje yön raporunun §5'inde hedeflenen **20 kanonik göreve** tamamlandı (`trc_010`–`trc_020`, 11 yeni görev). Dağılım artık dengeli: diziler 3, string 3, matematik 3, mantık 4, özyineleme 4, sayma 3.

Kategori seçimlerinde bilinçli çeşitlilik gözetildi: **mantık** (dengeli parantez kontrolü, kesin-artan liste, üçgen eşitsizliği, FizzBuzz) durum-makinesi/koşul mantığını; **özyineleme** (faktöriyel, Fibonacci, iç içe liste toplamı, Öklid EBOB) doğası gereği özyinelemeli problemleri — özellikle iç içe liste toplamı, keyfi derinlikte iç içe geçmiş girdilerle modelin gerçekten özyinelemeli düşünüp düşünmediğini zorluyor; **sayma** (kelime sayısı, hedefe eşit ikili sayısı, en uzun ardışık dizi) O(n²) kombinatorik sayım ile O(n) taramayı ayırt eden problemleri kapsıyor.

Guardrail disiplini aynen sürdürüldü: 11 yeni görevin tamamı oracle'dan 6/6 ile geçti (toplamda 20/20). Kenar durumları elle hesaplanıp doğrulandı — ör. `hedefe_esit_ciftler` görevinde `[0,0,0,0]` listesinde hedef 0 için C(4,2)=6 ikili beklendiği gibi çıktı; `ic_ice_liste_toplami` görevinde `[[[[]]]]` gibi tamamen boş iç içe yapılar 0 döndürdü. Guardrail regresyon testi otomatik olarak genişledi (parametrik test her yeni dosyayı kendiliğinden yakalıyor); pytest paketi 30'dan **41'e** çıktı, hepsi geçiyor.

### Bugün Öğrenilenler

* Kategori tasarımının rastgele değil, farklı **problem şekillerini** (durum-makinesi mantığı, özyineleme, kombinatorik sayım) temsil edecek şekilde kasıtlı seçildiği; bunun ileride hata taksonomisinin (Gün 16) anlamlı kırılımlar üretebilmesi için zemin oluşturduğu görüldü.
* Parametrik guardrail testinin (Gün 11'de eklenen) tam olarak amaçlandığı gibi çalıştığı doğrulandı: 11 yeni dosya eklendiğinde hiçbir ek kod yazmadan otomatik olarak test kapsamına girdi.
* "Özyineleme" kategorisinin, sandbox'ın yalnızca girdi/çıktı eşitliğine baktığını (modelin *nasıl* çözdüğünü değil) hatırlattığı; iç içe liste gibi problemlerin özyinelemeyi doğal olarak teşvik etmesi, katı bir "özyinelemeli kod yazmalısın" zorlaması olmadan da anlamlı bir kategori ayrımı sağlıyor.

### Oluşturulan Çıktılar

* data/tasks/trc_010.json … trc_020.json (11 yeni kanonik görev; mantık×4, özyineleme×4, sayma×3)
* Güncellenmiş docs/staj_defteri_gunlukleri.md, docs/20_gunluk_plani.md

### Bir Sonraki Adım

Veri seti hedeflenen ~20 kanonik göreve ulaştı; §5'teki 6 kategorinin tamamı dolu. Gün 13'te Mutator ajanı (Claude API) devreye girecek: her görevin `sablon` alanı kullanılarak parametrik varyantlar üretilecek ve her varyant oracle guardrail'inden geçmeden veri setine kabul edilmeyecek. Bu, Düzlem 1'in (yaratıcı ajan fabrikası) projede ilk kez fiilen çalışacağı gün olacak.

## 13. Gün - Mutator Ajanı: Düzlem 1'in İlk Fiili Çalışması

Bugün, projenin en hassas mimari eşiği geçildi: Düzlem 1 (Yaratıcı Ajan Fabrikası) ilk kez fiilen çalıştı. Koda geçmeden önce uzun bir tasarım/iletişim süreci yürütüldü — persona metni, kapsam sınırları ve üretim mimarisi kod yazılmadan netleştirildi.

**Kapsam kararı.** Mutator'ın işi baştan **dar** tutuldu: var olan, zaten oracle-doğrulanmış bir kanonik görevin YALNIZCA senaryosunu (bağlamını) değiştirmek — algoritmayı değil. "Parametrik varyant" (sayısal örnekleme) ekseni bilinçli olarak Mutator'ın kapsamı DIŞINDA bırakıldı; bu saf mekanik bir iş olduğu için ileride saf kodla (Claude'suz) yapılacak. Kullanıcının kritik bir itirazı ("agent'lar profesyonelce kurgulanmış soru üretmekte zorlanır, internetten mi almalıyız?") bu noktada netleştirici oldu: cevap, sorunun kendisinde saklıydı — internetten soru almak **kirlilik/ezber riski** taşır (proje_yon_raporu §5), ve Mutator'ın işi zaten yeni problem icat etmek değil, var olan-ve-doğrulanmış bir problemin yüzeyini değiştirmek olduğu için "profesyonellik" riski düşük.

**Persona tasarımı ve pilot doğrulama (koddan önce).** Persona; rol, sabit kalması gereken alanlar (mantık, test_cases), değiştirilebilecek alanlar (senaryo, isimler) ve "oracle neyi yakalar neyi yakalayamaz" ayrımı etrafında kuruldu — en kritik uyarı: oracle yalnızca KOD davranışını kontrol eder, senaryonun anlam tutarlılığını (ör. "ödünç alma" + "bütçe" çelişkisi) ASLA yakalayamaz; bu tamamen persona'nın sorumluluğu. Bu persona, koda geçmeden önce bu oturumun `Agent` aracıyla **7 kez** pilot test edildi — en riskli senaryolar dahil (özyinelemeli fonksiyonda kendi-kendini-çağırma satırının doğru yeniden adlandırılması, 3-parametreli skaler fonksiyonlar, çok ince `sablon`'la kendi başına senaryo kurma, aynı görevde farklı sablon kombinasyonları). 7/7 pilot, oracle'dan 6/6 geçti ve kod-düzeyinde satır satır karşılaştırmada hiçbir mantık sapması bulunmadı. 4 pilot varyant kaliteli bulunup doğrudan veri setine eklendi (`trc_021`-`trc_024`).

**Üretim mimarisi kararı: Claude Code CLI (API anahtarsız).** Ham Anthropic API ile ayrı bir `ANTHROPIC_API_KEY` kurmak yerine, kurulu Claude Code CLI'nin headless (`-p`) modu + `--system-prompt` + `--json-schema` kullanılarak, kullanıcının mevcut Claude Code (Max) girişini kullanan bir script mimarisi kuruldu. Bu karara varmadan önce iki gerçek mühendislik/hesap sorusu araştırıldı ve kaynaklı biçimde cevaplandı: (1) CLI kullanımı aynı hesabın diğer cihazlardaki kullanımıyla AYNI paylaşımlı kotaya giriyor mu (evet — hesap bazlı, cihaz bazlı değil, ama "bir insan bir abonelik" ilkesiyle izinli); (2) gösterilen `total_cost_usd` gerçekten faturalandırılıyor mu (hayır — Max planda bu yalnızca yerel bir TAHMİN, gerçek ödeme değil, tüketilen şey dolar değil kota). npm global kurulumda izin hatası (`EACCES`) çıktı, npm prefix'i kullanıcı dizinine taşınarak (sudo'suz) çözüldü; ardından güvenlik nedeniyle engellenen `postinstall` betiği elle çalıştırılarak native ikili indirildi.

**Maliyet optimizasyonu — ölçülerek keşfedildi.** Persona'yı `--system-prompt` ile ayırmadan (hepsi tek stdin metni) ilk çağrı $0.22'ye mal oldu; `--system-prompt` ile ayırınca $0.16'ya düştü; AYNI persona ile ikinci bir çağrıda Anthropic'in prompt önbelleklemesi devreye girdi ve maliyet $0.043'e indi (~4 kat). Bu, toplu üretimde yalnızca ilk çağrının pahalı olacağını, sonrakilerin önbellekten yararlanacağını gösterdi — tahminle değil, ölçülerek doğrulandı.

**Kalıcı kod.** `src/agent_factory/client.py` (genel, yeniden kullanılabilir `ajan_cagir()` — Mutator/Translator/Test-Öneri/Failure-Classifier'ın HEPSİ bunu kullanacak), `src/agent_factory/mutator.py` (persona + varyant birleştirme + guardrail çağrısı), `src/run_mutator.py` (CLI, otomatik id atama). Script gerçek görevlerle uçtan uca test edildi (tekli ve TOPLU üretim — toplu üretimde ilk yazımda bir ID-çakışma hatası fark edilip düzeltildi: id üretici her döngüde diskten değil, bellekte artan biçimde çalışmalıydı). 3 ek üretim (`trc_025`-`trc_027`) veri setine eklendi. Toplam veri seti: **27 görev** (20 kanonik + 7 mutasyon).

**Test altyapısı.** `tests/test_agent_factory.py` — `subprocess.run` mock'lanarak Docker/CLI GEREKTİRMEYEN 10 birim testi (başarı yolu, is_error, şema-uyumsuzluğu, JSON-olmayan çıktı, sıfır-dışı dönüş kodu, zaman aşımı, CLI-bulunamadı, görev-metni biçimlendirme, varyant birleştirme, guardrail-red senaryosu). Pytest paketi 48'den **58'e** çıktı, hepsi geçiyor.

### Bugün Öğrenilenler

* Kod yazmadan önce persona'yı gerçek pilot denemelerle (bu oturumun kendi agent aracıyla) doğrulamanın, kalıcı script'e büyük bir güvenle geçmeyi sağladığı görüldü — "önce kanıtla, sonra kalıcılaştır" sırası işe yaradı.
* "İnternetten soru almalı mıyız" sorusunun cevabının, projenin kendi kirlilik-güvenliği ilkesinde (§5) zaten yazılı olduğu; kullanıcının bu itirazı sorması, mimarinin doğru gerekçelerle savunulabilir olduğunu sınamış oldu.
* Bir CLI aracının gösterdiği `cost_usd` rakamının HER ZAMAN gerçek bir ödeme anlamına gelmediği, abonelik/API ayrımının dikkatle açıklanması gerektiği — teknik kesinlik burada mali kafa karışıklığını önledi.
* Prompt önbellekleme faydasının varsayılmak yerine ÖLÇÜLEREK doğrulanmasının (üç art arda çağrı, üç farklı maliyet) hem mühendislik hem metodolojik disiplin açısından doğru olduğu.
* Guardrail'in, isim-değiştirme gibi "düşük risk" görünen bir işlemde bile GERÇEK iş yaptığı: özyinelemeli çağrıyı yeniden adlandırmayı unutma gibi bir hata, oracle tarafından anında yakalanırdı (yakalanmadı çünkü doğru yapıldı, ama mekanizma orada, hazır bekliyordu).

### Oluşturulan Çıktılar

* src/agent_factory/ (client.py, mutator.py, __init__.py)
* src/run_mutator.py
* tests/test_agent_factory.py (10 yeni birim testi)
* data/tasks/trc_021.json … trc_027.json (7 mutasyon varyantı)
* .gitignore (.env kalıcı olarak dışlandı — henüz kullanılmasa da)
* Güncellenmiş README.md, docs/staj_defteri_gunlukleri.md, docs/20_gunluk_plani.md
* Kurulu ve giriş yapılmış Claude Code CLI (~/.npm-global altında, sudo'suz)

### Bir Sonraki Adım

Gün 14: Hikaye mutasyonunun tamamlayıcısı olan TR↔EN Translator ajanı + varyant ailesi otomasyonu. `agent_factory/client.py`'nin genel `ajan_cagir()` fonksiyonu sayesinde Translator, Mutator'ın altyapısını doğrudan yeniden kullanabilecek — yalnızca yeni bir persona ve şema yazmak yeterli olacak.

## Gün 14 Çalışma Kararı — Veri Seti Ölçeği ve Branch Düzeni

Gün 14 çalışmaları `gun14-translator` branch'inde sürdürülecek. Mevcut 27 görev
(20 kanonik + 7 hikâye mutasyonu) ölçüm altyapısını doğrulamak için yeterli bir
MVP zemini sağlıyor; ancak nihai benchmark için yeterli değildir. Veri seti
kesinlikle büyük ölçekte artırılacaktır. Kısa vadeli hedef, metrik motoru
çalıştıktan sonra kanonik görevleri ve her kanonik görev için dengeli varyant
ailesini kontrollü biçimde çoğaltmaktır. Uzun vadeli hedef proje yön raporunda
belirtilen yaklaşık 150–200 değerlendirme birimidir.

İzlenecek sıra: Translator sözleşmesi ve aile metadatası → Gün 15 metrik motoru
→ küçük doğrulama büyütmesi → oracle ile toplu veri üretimi → model matrisi ve
istatistiksel raporlama. Böylece veri sayısını artırırken görev kalitesini,
kategori dengesini ve Türkçe/İngilizce karşılaştırılabilirliğini koruyacağız.

## 14. Gün - Translator Ajanı, Dereceli Gizleme Tasarımı ve Veri Setinin Yeniden Kurulması

Bugün veri seti 27'den **62 göreve** çıktı, ama asıl iş sayı değil: varyantların NE ölçtüğünün netleşmesiydi.

**Bulunan hata — sessizce metriği bozan bir tasarım.** Günün başında parametrik üreteç, `sablon` kelimelerini `prompt_tr` içinde düz regex ile değiştiriyordu. İki kusuru vardı ve ikisi de veri setini fark edilmeden bozuyordu. Birincisi: `prompt_en` hiç güncellenmiyordu, yani varyantta Türkçe "kütüphane" sorulurken İngilizce hâlâ "market" soruluyordu — projenin manşet metriği `acc(en) − acc(tr)` iki dilde AYNI problemin sorulmasına dayanır, bu haliyle metrik anlamsızlaşıyordu. İkincisi: Türkçe ek uyumu yapılamıyordu; kodun yorumu "markette → kütüphanede olur" diyordu ama kod eki olduğu gibi yapıştırıp "kütüphanete" üretiyordu. Test paketi zaten kırmızıydı ve tam bu satırı gösteriyordu. Türkçe bir benchmark'ın bozuk Türkçe üretmesi, ölçtüğü şeyi doğrudan kirletir.

**Çözüm — ikameyi metin düzeyinden ajan düzeyine taşımak.** Regex tamamen kaldırıldı. Artık sablon seçimi bir DEĞİŞİM YÖNERGESİ'ne çevrilip Translator ajanına veriliyor; ajan iki dili birlikte, sıfırdan kuruyor. Böylece ek uyumu ve TR/EN paritesi tek hamlede çözülüyor. Nondeterminizm itirazına dürüst cevap: veri seti üretim anında BİR KEZ üretilip git'e commit edilerek donduruluyor; ölçüm (`run_matrix`) sırasında hiçbir ajan çağrılmıyor, dolayısıyla benchmark'ın kendisi deterministik kalıyor.

**Tasarım kararı — dereceli gizleme.** Gün içinde iki varyant ekseninin birbirinin alternatifi olmadığı, farklı DERİNLİKTE iki kirlilik probu olduğu netleşti: `parametric_story` yalnız hikâyeyi değiştirir, fonksiyon adı ve imza aynı kalır (sığ gizleme); `story_mutation` hikâyeyle birlikte fonksiyon adını, imzayı ve değişken adlarını da değiştirir (derin gizleme). Bir model yalnız derin seviyede düşüyorsa ezber kod yüzeyine tutunmuştur; her ikisinde düşüyorsa hikâyeye. Tek bir "ezber farkı" sayısı bu ayrımı yapamaz. Veri seti buna göre TASARLANDI: 20 kanonik × (1 parametrik + 1 mutasyon), 20/20 aile tam. Ezber metriğinin örneklemi n=5 aileden n=20 aileye çıktı.

**Kalite kapıları — biri gerçek, biri itiraf.** Parametrik eksende oracle'ın neredeyse TAUTOLOJİ olduğu açıkça kabul edildi: kod ve test_cases hiç değişmediği için oracle tanım gereği geçer. Gerçek mekanik güvence olarak `degismezleri_dogrula` (kod/test alanları byte-byte aynı mı) eklendi; oracle regresyon sigortası olarak yerinde bırakıldı ve sınırı kod yorumuna yazıldı. Prompt metninin ANLAM doğruluğunu hiçbir mekanik kapı denetleyemez — bu, insan gözden geçirmesi gerektiren bir yüzey olarak dürüstçe kaydedildi.

**Uzunluk confound'u — ölçerek bulundu.** İlk düzeltmeden sonra üretilen faktöriyel varyantı güzeldi ama ebeveyninin 5.1 katı uzunluktaydı. Bu ciddi bir sorun: `acc(kanonik) − acc(varyant)` düşüşünün ezberin kırılmasından mı yoksa metnin uzamasından mı geldiği ayırt edilemez hale gelirdi. Hem persona'ya uzunluk kısıtı eklendi hem `uzunluk_kapisi` mekanik kapısı yazıldı. Kapı ilk kalibrasyonunda (saf 3x oranı) kısa ebeveynli görevlerde parametrik ekseni tümden imkânsız kılıyordu — bir senaryo kurmanın kabaca SABİT bir karakter maliyeti var, oran bunu görmüyor. `max(3x, ebeveyn + 250 karakter)` olarak yeniden kalibre edildi. Mevcut 62 görevde tek ihlal kalmadı; oranlar 1.0–2.5x arasında.

**Testler büyümeyi engelliyordu.** Veri seti testinde `len(gorevler) == 27` sabiti vardı: veri setini büyütmeyi ana hedef edinmiş bir projede, her yeni görevde kırılan bir test. Testler BOYUT yerine DEĞİŞMEZ doğrular hale getirildi (parametrik şema doğrulaması, aile bütünlüğü, kod değişmezliği) — artık her yeni görev otomatik kapsama giriyor.

**Ortak altyapı.** `src/task_io.py` yazıldı: okunabilir JSON serileştirme, sabit alan sırası, Docker'sız şema doğrulaması, id üreteci. Sebep somuttu — bir önceki gün görev dosyaları düz `json.dumps(indent=2)` ile yeniden yazılmış ve `trc_001` 30 satırdan 97 satıra şişmişti; veri seti diff'i 1443 satırdı. Yeni serileştiriciyle diff 99 satıra indi ve dosyalar elle okunabilir hale döndü.

**Koşum matrisine kontrol noktası.** ~868 hücrelik tam matris saatler sürüyor; ortada bir çökme tüm emeği götürürdü. Her hücre tamamlanır tamamlanmaz JSONL kontrol noktasına yazılıyor, `--devam` ile kaldığı yerden sürüyor. Farklı `--tekrar`/`--sicaklik` ile devam etmek hücreleri karıştıracağı için imza uyuşmazlığında koşum sessizce devam etmiyor, duruyor.

### Bugün Öğrenilenler

* Bir ajanın ürettiği metnin "doğru" olması ile "ölçüm için kullanılabilir" olmasının farklı şeyler olduğu: uzunluk confound'u, tek tek bakıldığında kusursuz görünen varyantlarda gizliydi ve ancak ebeveyniyle ORANLANARAK görünür oldu.
* Yönergenin nasıl yazıldığının çıktının bilimsel değerini belirlediği: `"sayı" yerine "adım" kullan` yönergesi "n adım miktarının faktöriyeli" gibi değersiz bir metin üretti; aynı tohum "somut senaryo kur" çerçevesiyle verildiğinde koreografın dans adımlarını kaç farklı sırayla dizebileceği problemine dönüştü — algoritma aynı, gizleme gerçek.
* Guardrail'in ne yakalayabildiğini abartmamanın, yakalayamadığını açıkça yazmanın mühendislik dürüstlüğü olduğu: parametrik eksende oracle bir şey ispatlamıyor, `degismezleri_dogrula` ispatlıyor.
* Testin projenin hedefiyle çelişebileceği: sabit sayı bekleyen bir test, büyümesi gereken bir veri setinde kusurdur.
* En iyi varyantın, problemin adını hiç anmayanı olduğu — `trc_044`'te EBOB, "iki tahtayı artık bırakmadan eşit parçalara bölmek" senaryosuna dönüştü ve "EBOB" kelimesi metinde hiç geçmiyor; model problemi çıkarmak zorunda.

### Oluşturulan Çıktılar

* src/task_io.py (serileştirme, alan sırası, şema doğrulaması, id üreteci, uzunluk/değişmezlik kapıları)
* src/agent_factory/translator.py (iki modlu: uyumlama + yönergeli senaryo değişimi)
* src/agent_factory/parametric.py (regex'siz, üç kapılı parametrik üreteç)
* src/run_parametric.py (`--kuru` plan modu dahil)
* src/run_matrix.py: kontrol noktası + `--devam`
* data/tasks/trc_028.json … trc_062.json (20 parametrik + 15 mutasyon varyantı)
* Pytest 61 → 168 test; 62/62 görev oracle'dan 6/6

### Bir Sonraki Adım

Gün 15: **Büyük koşum** ve metrik motoru. Veri seti artık iki benchmark'ı da (saf kodlama yeteneği + Türkçe vergisi) ve iki seviyeli ezber farkını gerçek veriyle hesaplayacak olgunlukta. Ölçüm borcu projenin kalan en büyük açığı: bugüne kadarki tüm `results/*` dosyaları hâlâ tek görev üzerinde koşulmuş durumda.

## 15. Gün — Büyük Koşum ve Metrik Motoru (ölçüm borcu kapandı)

Bugün ilk kez **tam matris gerçek veriyle koşuldu**: 62 görev × 7 model × 2 dil × 3 tekrar = **868 hücre**, `sıcaklık=0.4` (gerçek pass@k). Bugüne kadarki tüm sonuçlar tek görev üzerindeydi; projenin en büyük açığı olan ölçüm borcu kapandı.

**Koşum bir kez çöktü, kontrol noktası kurtardı — ama sessizce değil.** Koşum, Ollama servisi durduğunda yarıda kaldı. Kaldığı yerden sürdürülürken kontrol noktası dosyasının (`gun15_buyuk_kosum.ckpt.jsonl`) son satırının tamamen NUL byte'lardan oluştuğu görüldü — temiz olmayan kapanışın klasik izi (tampon uzatılmış ama veri flush edilmemiş). Yükleyici bu bozuk satırda `JSONDecodeError` ile durdu; bu aslında iyi bir davranış — sessizce yutup eksik veriyle devam etmedi. Bozuk satır temizlenip (76 sağlam hücre korundu) `--devam` ile sürdürüldü; imza (`tekrar=3, sıcaklık=0.4`) uyuştuğu için hücreler karışmadan tamamlandı. Bütünlük doğrulaması: 868/868 hücre, 0 eksik kombinasyon, 0 koşulamamış hücre, dil dengesi 434/434.

**Metrik motoru — dört manşet, hepsi kayıtlı veriden, ajan çağırmadan.** `src/metrik_ozet.py` yazıldı; ölçüm anında hiçbir ajan çağrılmadan yalnız kontrol noktası + görev metadatası okunuyor:

* **Kodlama yeteneği (acc_en):** qwen2.5:3b 0.933, coder:3b/llama3.2:3b 0.883. Genel pass@1'de coder:3b lider (0.858).
* **Türkçe vergisi (acc_en − acc_tr):** llama3.2:3b'de en ağır (+0.300 — İngilizce'de güçlü, Türkçe'de çöküyor); kod'a-özel coder:3b'de neredeyse yok (+0.017). Bulgu: koda-özel eğitim Türkçe vergisini baskılıyor.
* **İki-seviyeli ezber farkı (n=20 tam aile):** Tasarım hipotezi doğrulandı — **derin gizleme** (ad/imza/değişken değişir) neredeyse her modelde **sığ gizlemeden** (yalnız hikâye) daha büyük düşüş yaratıyor. Modeller yüzeysel kod ezberine tutunuyor. En dirençli coder:3b (derin Δ yalnız +0.064); en kırılgan qwen2.5:1.5b (+0.193).
* **Token vergisi (kanonik, ort. completion token, tr/en oranı):** coder:1.5b Türkçe'de **3.77×**, gemma2:2b 2.88× daha fazla token harcıyor; qwen2.5:3b ve llama3.2:3b ~1.0 (eşit). Aynı doğruluk farklı hesap maliyetiyle geliyor — bu ancak ölçülünce görünür.

### Bugün Öğrenilenler

* Uzun koşumlarda kontrol noktasının değeri, ancak bir çökme yaşandığında somutlaşıyor: 868 hücrelik matris saatler sürüyor, ortadaki bir çökme `--devam` olmadan tüm emeği götürürdü.
* Bozuk veride "sessizce devam etme, dur" davranışının doğru mühendislik olduğu: NUL-byte'lı satırda yükleyicinin durması, eksik/yanlış metrik üretmekten iyidir.
* Koda-özel eğitimin iki ayrı ekseni birden iyileştirdiği: coder:3b hem en yüksek doğruluğa hem en düşük Türkçe vergisine hem en düşük ezber kırılganlığına sahip — ama token vergisi hâlâ 1.53×.
* Doğruluğun tek başına yeterli olmadığı: iki model aynı pass@1'i tutturup biri 3× daha fazla token harcayabiliyor; token vergisi olmadan bu maliyet görünmez kalırdı.
* pass@k − pass@1 kazancının model boyutuyla ters orantılı olduğu: küçük modeller (0.5b +0.185, 1.5b +0.164) arada bir doğruyu buluyor ama kararlı üretemiyor; coder/büyük modeller (+0.05) zaten kararlı. Tek örnekle (pass@1) ölçmek küçük modelleri olduğundan zayıf, k örnekle ölçmek gücünü örnekleme bütçesine bağımlı gösterirdi — ikisini birlikte raporlamak şart.

### Oluşturulan Çıktılar

* results/gun15_buyuk_kosum.json + .csv + .ckpt.jsonl (868 hücrelik tam matris)
* src/metrik_ozet.py (manşetler: kodlama yeteneği, Türkçe vergisi, pass@1↔pass@k örnekleme kazancı, iki-seviyeli ezber farkı, token vergisi — planın Gün 15 listesi tam karşılandı)
* Pytest 168/168 geçiyor (değişmedi — metrik motoru saf okuma, mevcut kapıları bozmadı)

### Bir Sonraki Adım

Gün 16: **Hata taksonomisi (Failure-Classifier) + ölçek trendi.** Büyük koşum artık her hücrede `hata_tipleri` ve örnek çıktıları saklıyor; başarısızlıkların NEDEN olduğu (sözdizimi, yanlış mantık, Türkçe yanlış-anlama, zaman aşımı) sınıflandırılacak ve 0.5→3B ölçek eğrisi figürleri çıkarılacak.

## Gün 16 Hazırlık — Endişe Kapatma: CI + Design A + Taksonomi/Figürler + Veri Seti v2

Bu oturum "16. güne geçmeden önce tüm eksik bilgileri kapatalım" hedefiyle başladı. Gün 15 sonrası kıdemli bir gözden geçirme dört endişe çıkardı ve dördü de kapatıldı; ayrıca Gün 16 içeriğinin (taksonomi + figürler) çekirdeği kuruldu ve veri seti blueprint-hedefli 50 kanonik göreve çıkarıldı. Çalışma `gun16-hazirlik` dalında iki düzenli commit + PR #21 olarak kalıcılaştırıldı.

**Endişe 1 — istatistiksel güç (bootstrap CI).** Metrik motoru saf nokta-tahmin üretiyordu; "+0.017 vs +0.300" gibi farkların gürültüden ayrışıp ayrışmadığı bilinmiyordu. `metrik_ozet.py`'ye görev/aile düzeyinde (sabit seed, tekrarlanabilir) bootstrap %95 GA eklendi. İlk koşuda gemma2:2b'nin defterde "sağlam" yazılı +0.150 vergisinin CI'sının sıfırı içerdiği görüldü — bir overclaim CI tarafından anında yakalandı. Tasarım hipotezinin TAM testi (derin−sığ fark-farkı CI'sı) da eklendi.

**Endişe 2 — anlam kapısı.** Donmuş 62 görevde bir denetim ajanı çalıştırıldı: 62/62 okundu, 59 temiz; TR/EN parite, Türkçe dilbilgisi ve senaryo-mantığı hepsi geçti. Bulunan 3 küçük imza-uyumsuzluğunun aslında Design A confound'unun belirtisi olduğu anlaşıldı ve ayrı değil, geçişin parçası olarak düzeltildi.

**Endişe 3 — tanımlayıcı confound (Design A).** En kritik boşluk: "İngilizce" koşumda bile fonksiyon/parametre adları Türkçe kalıyordu (`max_urun`, `fiyatlar`, `butce`), yani "Türkçe vergisi" manşeti sabit bir Türkçe-tanımlayıcı zemini üzerine oturuyordu. Kullanıcı onayıyla **Design A** seçildi: EN sütunu TAMAMEN İngilizce, TR TAMAMEN Türkçe (ekolojik olarak geçerli uçtan-uca vergi). `code_task`/`run_task` dil-duyarlı yapıldı (`fonksiyon_imzasi_en`/`fonksiyon_adi_en`, TR'ye güvenli fallback); 62 göreve EN tanımlayıcı eklendi ve 43 EN prompt'ta sızan Türkçe backtick düzeltildi (her iki dilde 0 sızıntı). Kritik ince nokta: imzayı değiştirmek EN prompt'lardaki backtick'leri bozuyordu — konumsal TR↔EN parametre eşlemesiyle toplu düzeltildi ve bu "0-sızıntı" özelliği kalıcı regresyon-testine çevrildi. Şema kapısı EN-tutarlılığı da denetliyor.

**Design A re-run — temiz manşetler.** Genişletilmiş kablolamayla tam matris n=3→5 ile yeniden koşuldu (868 hücre, 0 eksik). Confound temizliği vergiyi ŞİŞİRMEDİ, büyük ölçüde SABİT kaldı — bu, verginin bir tanımlayıcı-artefaktı değil GERÇEK olduğunun en güçlü kanıtı. coder:3b Türkçe vergisi tam **+0.00** [−0.05,+0.04]'e indi: koda-özel eğitim vergiyi yok ediyor (kusursuz kanıt); genel modeller (llama3.2:3b +0.27, qwen0.5b +0.24, gemma +0.22, qwen1.5b +0.15) gerçek vergiyi koruyor.

**Endişe 4 (bekleme operasyonları) — Gün 16 çekirdeği.** Matris koşarken, koşuma dokunmadan üç eksik kapatıldı: (a) yeni kodun test borcu (`test_metrik_ve_design_a.py`, 81 test); (b) **hata taksonomisi** (`hata_taksonomisi.py`) — mekanik `hata_tipi`'nin kör noktasını kapattı: başarısızlıkların çoğu "kod çalıştı ama yanlış" (yanlış-mantık) ve Türkçe vergisi bir **mantık vergisi** (+347 mantık vs +44 sert hata); (c) **figürler** (`figur_uret.py`, dataviz metoduyla 3 advisor-ready grafik: ölçek eğrisi, vergi+CI, taksonomi).

**Veri seti v2 — blueprint'ten 50 kanoniğe.** Genişletmenin sözleşmesi önce yazıldı: `veri_seti_blueprint.md` (güç-temelli boyut hedefi — kendi verimizden ±0.07→~80, ±0.05→~158 kanonik; sektör normu HumanEval 164 ile yakınsıyor) + `veri_seti_datasheet.md` (köken, kapsam, 7 açık limit). En büyük yapısal boşluk **zor tier'ın hiç olmaması**ydı (0 zor görev → coder:3b 0.85'te tavan etkisi). `run_kalite_kapisi.py` tüm kapıları (oracle+şema+Design-A+opsiyonel uzunluk/değişmez) zincirledi. 30 yeni özgün kanonik (trc_063-092) elle yazıldı — hepsi tüm kapılardan + anlam-denetiminden geçti. Sonuç blueprint hedefini birebir tutturdu: 20→50 kanonik, 15 kolay / 23 orta / 12 zor, 6 kategori dengeli (8-9). pytest 168→339.

### Bugün Öğrenilenler

* Bir confound'u temizlemenin bulguyu değiştirmemesinin, o bulgunun gerçekliğinin EN güçlü kanıtı olabileceği: Design A vergiyi şişirmedi, bu yüzden vergi artefakt değil.
* Güven aralığının değerinin ilk koşuda somutlaştığı: nokta-tahmin "sağlam" görünen bir farkın (gemma +0.150) aslında sıfırı içerdiğini yalnızca CI gösterebildi.
* Bir tasarım düzeltmesinin (EN imza) beklenmedik ikinci-düzey etki yaratabildiği (EN prompt backtick'leri bozuldu) — ve mekanik bir invariant testinin bunu kalıcı olarak kilitlediği.
* Mekanik hata-etiketinin bir kör noktası olduğu: başarısızlıkların %27'si "null" etiketliydi ama aslında en büyük tür olan yanlış-mantıktı; Türkçe vergisinin bir syntax değil MANTIK vergisi olduğu ancak bu ayrımla görüldü.
* Benchmark boyutunun bir "his" değil, hedef kesinlikten geri hesaplanan bir sayı olduğu; ve en saygın kod benchmark'ının (HumanEval 164) küçük olması — güvenilirliğin ham boyuttan çok yapı geçerliliği + kontaminasyon kontrolünden geldiği.
* Bir veri setini büyütürken "yaz sonra say" yerine "önce blueprint" disiplininin, dağılımı (zorluk, kategori) hedefe birebir oturtmayı sağladığı.

### Oluşturulan Çıktılar

* src/metrik_ozet.py (bootstrap CI + fark-farkı; not dinamikleştirildi)
* src/model_client/code_task.py, src/run_task.py, src/task_io.py (Design A dil-duyarlı + şema kapısı)
* data/tasks/trc_001-062 (EN tanımlayıcılar + backtick temizliği), trc_063-092 (30 yeni kanonik, zor tier)
* src/hata_taksonomisi.py, src/figur_uret.py, src/run_kalite_kapisi.py
* tests/test_metrik_ve_design_a.py (bootstrap, Design A, 0-sızıntı invariant, taksonomi — 168→339)
* results/gun16_designA.json + .csv + .ckpt.jsonl (868 hücre, n=5, temiz); results/figures/fig1-3.png
* docs/veri_seti_blueprint.md, docs/veri_seti_datasheet.md
* Dal `gun16-hazirlik`: 2 commit + PR #21

### Bir Sonraki Adım

Dalga-4: 30 yeni kanoniğe sığ (parametric_story) + derin (story_mutation) varyant aileleri (ajan fabrikası), v2'yi git etiketiyle dondurma ve genişletilmiş sette (~150 birim) büyük koşum — CI'lar ~±0.09'a daralacak.
