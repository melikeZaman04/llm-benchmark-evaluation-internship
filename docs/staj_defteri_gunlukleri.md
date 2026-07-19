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
