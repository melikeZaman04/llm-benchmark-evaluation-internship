# Yaygın LLM Benchmark Veri Setleri

Bu dokümanda yaygın kullanılan LLM benchmark veri setleri incelenmiştir. Amaç, veri setlerinin hangi görevleri ölçtüğünü, modellerden nasıl cevaplar beklediğini ve hangi metriklerle değerlendirildiğini genel olarak anlamaktır.

Bu aşamada herhangi bir model çalıştırılmamış, veri seti indirilmemiş ve metrik hesaplanmamıştır. Çalışma yalnızca araştırma ve dokümantasyon amacıyla hazırlanmıştır.

## 1. Benchmark Veri Seti Nedir?

Benchmark veri seti, modellerin belirli görevlerdeki başarısını ölçmek için hazırlanmış standart test verisidir. Bu veri setlerinde genellikle modele verilecek soru, komut veya metin ile beklenen doğru cevap birlikte bulunur.

LLM benchmark veri setleri farklı becerileri ölçebilir. Örneğin bazıları çoktan seçmeli genel bilgi sorularından oluşur, bazıları matematik problemi çözmeyi, bazıları kod üretmeyi, bazıları ise verilen metinden cevap bulmayı test eder.

Bir benchmark veri setinde şu bilgiler önemli olabilir:

* Görev türü
* Soru veya giriş metni
* Cevap seçenekleri ya da beklenen cevap
* Doğru cevap etiketi
* Değerlendirme metriği
* Konu veya zorluk kategorisi

Bu tür veri setleri sayesinde farklı modeller aynı sorular üzerinde test edilebilir. Böylece model sonuçları daha düzenli ve karşılaştırılabilir hale gelir.

## 2. LLM Benchmarklarını Karşılaştırma Tablosu

| Benchmark | Görev Tipi | Ölçtüğü Yetenek | Cevap Formatı | Yaygın Metrik | Bu Proje İçin Uygunluk |
|---|---|---|---|---|---|
| MMLU | Çoktan seçmeli soru cevaplama | Genel bilgi ve akademik alan bilgisi | A, B, C veya D seçeneği | Accuracy | Uygun örnek; bu projenin başlangıç formatına benzer |
| GSM8K | Matematik problemi çözme | Sayısal akıl yürütme | Çözüm adımları ve son sayısal cevap | Exact Match / Accuracy | Orta düzey; başlangıç için sadeleştirilmiş örnekleri kullanılabilir |
| ARC | Çoktan seçmeli fen soruları | Fen bilgisi ve akıl yürütme | A, B, C veya D seçeneği | Accuracy | Uygun örnek; küçük Türkçe fen sorularına uyarlanabilir |
| HellaSwag | Cümle / olay tamamlama | Sağduyu çıkarımı | En uygun devam seçeneği | Accuracy | Mantığı faydalı, ancak başlangıç için biraz daha yorum gerektirir |
| TruthfulQA | Doğruluk ve güvenilirlik değerlendirmesi | Yanıltıcı olmayan cevap verme | Kısa cevap veya çoktan seçmeli cevap | Truthfulness, informativeness, accuracy | Daha zor; serbest cevap değerlendirmesi gerektirebilir |
| HumanEval | Kod üretme | Programlama ve testlerden geçen kod yazma | Python fonksiyonu | pass@k | Başlangıç için uygun değil; kod çalıştırma ortamı gerektirir |
| SQuAD | Okuduğunu anlama | Metinden cevap çıkarma | Kısa metin cevabı | Exact Match, F1 | Faydalı ama bu projenin ilk aşamasından sonra ele alınabilir |
| GLUE | Doğal dil anlama | Sınıflandırma, benzerlik ve çıkarım | Göreve göre etiket veya skor | Accuracy, F1, correlation | Çok görevli olduğu için başlangıçta karmaşık |
| SuperGLUE | Zor doğal dil anlama | Daha zor çıkarım ve anlama görevleri | Göreve göre etiket veya kısa cevap | Accuracy, F1, Exact Match | Başlangıç için karmaşık |
| TR-MMLU | Türkçe çoktan seçmeli değerlendirme | Türkçe akademik ve genel bilgi | A, B, C veya D seçeneği | Accuracy | Türkçe benchmark fikri için uygun referans |
| Cetvel | Türkçe dil anlama ve üretim | Türkçe dil becerisi ve kültürel bilgi | Göreve göre değişir | Göreve göre değişir | Kapsamlı olduğu için başlangıçtan sonra incelenebilir |
| TurkBench | Türkçe LLM değerlendirmesi | Bilgi, akıl yürütme ve yönerge takibi | Göreve göre değişir | Göreve göre değişir | Türkçe değerlendirme için yararlı referans |

Tablodan görüldüğü gibi benchmarklar tek bir türden oluşmaz. Bazı benchmarklar kısa ve net cevaplar isterken, bazıları uzun açıklama, kod veya metinden çıkarılmış cevap bekler. Bu nedenle her benchmark için aynı değerlendirme yöntemi kullanılamaz.

Bu proje için ilk deney aşamasında çoktan seçmeli soru-cevap formatı tercih edilecektir. Çünkü modelden yalnızca A, B, C veya D seçenek harfi istenebilir ve accuracy metriğiyle değerlendirme daha kolay yapılabilir.

## 3. MMLU

MMLU, "Measuring Massive Multitask Language Understanding" ifadesinin kısaltmasıdır. Bu benchmark, dil modellerinin farklı akademik ve mesleki alanlardaki bilgisini ölçmek için hazırlanmıştır.

MMLU; matematik, tarih, hukuk, tıp, bilgisayar bilimi, felsefe ve benzeri çok sayıda alandan sorular içerir. Sorular çoktan seçmeli yapıdadır. Modelden genellikle A, B, C veya D seçeneklerinden doğru olanı seçmesi beklenir.

MMLU'nun ölçtüğü temel beceriler şunlardır:

* Genel bilgi
* Akademik alan bilgisi
* Çoktan seçmeli soru çözme
* Farklı konular arasında genelleme yapabilme

Cevap formatı basittir. Modelden yalnızca doğru seçeneği üretmesi istenebilir:

```text
Soru: ...
A) ...
B) ...
C) ...
D) ...

Beklenen cevap: B
```

MMLU'da yaygın metrik accuracy değeridir. Yani modelin doğru cevapladığı soru sayısı toplam soru sayısına bölünür.

Bu proje açısından MMLU doğrudan uygulanacak ilk benchmark olmak zorunda değildir. Ancak çoktan seçmeli değerlendirme mantığını anlamak için iyi bir örnektir. Çünkü cevap formatı nettir ve değerlendirme basit accuracy ile yapılabilir.

## 4. GSM8K

GSM8K, ilköğretim düzeyinde matematik problemlerinden oluşan bir benchmark veri setidir. Sorular genellikle kısa hikaye problemleri şeklindedir ve çözüm için birkaç aritmetik işlem yapmak gerekir.

GSM8K'nin amacı yalnızca modelin son sayıyı tahmin edip etmediğini ölçmek değildir. Aynı zamanda modelin problemi adım adım çözme becerisi de incelenebilir. Ancak otomatik değerlendirmede çoğu zaman son sayısal cevap beklenen cevapla karşılaştırılır.

Örnek cevap yapısı şu şekilde düşünülebilir:

```text
Soru:
Ali'nin 3 kalemi var. 2 kalem daha alırsa toplam kaç kalemi olur?

Beklenen cevap:
5
```

GSM8K'nin ölçtüğü temel beceriler şunlardır:

* Matematiksel akıl yürütme
* Çok adımlı problem çözme
* Sayısal cevap üretme
* Metindeki bilgiyi işleme

Yaygın değerlendirme metriği exact match veya accuracy olarak düşünülebilir. Modelin verdiği son cevap beklenen sayısal cevapla aynıysa doğru kabul edilir.

Bu proje için GSM8K'nin küçük bir benzeri ilerleyen günlerde hazırlanabilir. Ancak ilk aşamada gerçek GSM8K veri setini indirmek yerine, benzer mantıkta birkaç basit soru oluşturmak daha uygundur.

## 5. ARC

ARC, "AI2 Reasoning Challenge" ifadesinin kısaltmasıdır. Bu benchmark, özellikle fen bilgisi soruları üzerinden akıl yürütme becerisini ölçmek için hazırlanmıştır.

ARC veri seti, genellikle ilkokul ve ortaokul düzeyinde fen sorularından oluşur. Sorular çoktan seçmelidir. ARC'nin "Easy" ve "Challenge" olmak üzere iki farklı bölümü bulunur. Challenge bölümü, daha zor ve basit yöntemlerle çözülemeyen soruları içerir.

ARC'nin ölçtüğü temel beceriler şunlardır:

* Fen bilgisi
* Çoktan seçmeli soru çözme
* Bilgiye dayalı akıl yürütme
* Soru kökünü ve seçenekleri birlikte değerlendirme

Cevap formatı MMLU'ya benzer:

```text
Soru: ...
A) ...
B) ...
C) ...
D) ...

Beklenen cevap: C
```

Yaygın değerlendirme metriği accuracy değeridir. Modelin doğru seçeneği üretip üretmediği kontrol edilir.

Bu proje açısından ARC, çoktan seçmeli ve bilgiye dayalı değerlendirme için anlaşılır bir örnektir. Türkçe basit fen veya genel kültür soruları hazırlanarak ARC benzeri küçük bir yapı kurulabilir.

## 6. HellaSwag

HellaSwag, sağduyuya dayalı cümle veya olay tamamlama becerisini ölçen bir benchmarktır. Modele bir olay açıklaması verilir ve bu olayın en mantıklı devamını seçenekler arasından seçmesi beklenir.

Bu benchmarkın önemli tarafı, yanlış seçeneklerin insanlar için genellikle açıkça hatalı görünmesi, fakat modelleri yanıltabilecek şekilde hazırlanmış olmasıdır. Bu nedenle HellaSwag yalnızca kelime benzerliğiyle değil, anlam ve sağduyu ile cevaplamayı gerektirir.

HellaSwag'in ölçtüğü temel beceriler şunlardır:

* Sağduyu çıkarımı
* Olay akışını anlama
* Cümle tamamlama
* Yanıltıcı seçenekleri eleme

Örnek format şu şekilde düşünülebilir:

```text
Bağlam:
Bir kişi mutfağa girer ve bardağı suyla doldurur.

Seçenekler:
A) Bardağı masaya koyar.
B) Arabayı tamir eder.
C) Uyumak için yatağa gider.
D) Kitabı yakar.

Beklenen cevap: A
```

Yaygın metrik accuracy değeridir. Modelin en uygun devam seçeneğini seçmesi beklenir.

Bu proje için HellaSwag doğrudan uygulanması gereken ilk veri seti değildir. Ancak "anlam olarak en uygun cevap" seçme fikrini göstermesi bakımından önemlidir.

## 7. TruthfulQA

TruthfulQA, modellerin doğru ve yanıltıcı olmayan cevaplar verip vermediğini ölçmek için hazırlanmış bir benchmarktır. Bazı sorular, internette veya günlük hayatta sık karşılaşılan yanlış inanışlara dayanır. Modelin bu yanlış inanışları tekrar etmemesi beklenir.

TruthfulQA iki farklı şekilde kullanılabilir:

* Modelden kısa bir cevap üretmesi istenebilir.
* Modelden çoktan seçmeli seçenekler arasından doğru cevabı seçmesi istenebilir.

Bu benchmarkın ölçtüğü temel beceriler şunlardır:

* Gerçeğe uygun cevap verme
* Yaygın yanlış bilgileri tekrar etmeme
* Güvenilirlik
* Yanıltıcı sorulara karşı dikkatli olma

Üretim görevinde değerlendirme daha zordur. Çünkü modelin cevabı yalnızca kelime olarak değil, anlam olarak da doğru olmalıdır. Bu nedenle truthfulness ve informativeness gibi ölçütler kullanılır. Çoktan seçmeli sürümlerde ise accuracy daha kolay uygulanabilir.

Bu proje açısından TruthfulQA önemli bir örnektir, fakat başlangıç için biraz karmaşıktır. Çünkü serbest metin cevapların otomatik değerlendirilmesi, çoktan seçmeli sorulara göre daha zordur.

## 8. HumanEval

HumanEval, kod üretme becerisini ölçen bir benchmarktır. Modele genellikle bir Python fonksiyonunun açıklaması veya başlangıç kodu verilir. Modelden bu fonksiyonun doğru çalışan tamamlanmış halini üretmesi beklenir.

HumanEval'in ölçtüğü temel beceriler şunlardır:

* Kod yazma
* Fonksiyon tamamlama
* Problem çözme
* Testlerden geçebilen çıktı üretme

Örnek görev yapısı şu şekilde olabilir:

```python
def add_numbers(a, b):
    """
    İki sayıyı toplayan fonksiyonu tamamla.
    """
```

Modelden beklenen cevap, çalışan bir Python fonksiyonudur. Değerlendirme sırasında üretilen kod testlerle çalıştırılır. Eğer kod testleri geçerse doğru kabul edilir.

HumanEval'de yaygın metrik pass@k değeridir. Bu metrik, modelin ürettiği k farklı çözümden en az birinin testleri geçme olasılığını ölçer.

Bu proje için HumanEval başlangıç benchmarkı olarak uygun değildir. Çünkü kod çalıştırma, test ortamı hazırlama ve güvenli çalıştırma gibi ek konular gerektirir. Ancak ilerleyen aşamalarda kod üretme değerlendirmesi öğrenilmek istenirse incelenebilir.

## 9. SQuAD

SQuAD, "Stanford Question Answering Dataset" ifadesinin kısaltmasıdır. Okuduğunu anlama görevleri için hazırlanmış önemli bir benchmarktır.

SQuAD'da modele bir paragraf ve bu paragrafa bağlı bir soru verilir. Modelden cevabı paragraf içinden bulması beklenir. Bu nedenle SQuAD, serbest genel bilgi sorusundan farklıdır. Modelin dış bilgisinden çok, verilen metni anlayıp doğru cevap parçasını çıkarması önemlidir.

Örnek yapı şu şekilde olabilir:

```text
Paragraf:
Ankara, Türkiye'nin başkentidir.

Soru:
Türkiye'nin başkenti neresidir?

Beklenen cevap:
Ankara
```

SQuAD'ın ölçtüğü temel beceriler şunlardır:

* Okuduğunu anlama
* Paragraf içinden cevap çıkarma
* Kısa cevap üretme
* Metne bağlı kalma

SQuAD için yaygın metrikler Exact Match ve F1 değeridir. Exact Match, model cevabının beklenen cevapla tamamen aynı olup olmadığını ölçer. F1 ise model cevabı ile beklenen cevap arasındaki kelime örtüşmesini dikkate alır.

SQuAD 2.0 sürümünde cevaplanamayan sorular da bulunur. Bu sürümde modelin yalnızca cevap vermesi değil, gerektiğinde "bu sorunun cevabı verilen metinde yok" diyebilmesi de beklenir.

Bu proje için SQuAD mantığı oldukça faydalıdır. Çünkü küçük bir paragraf-soru-cevap veri seti oluşturmak mümkündür ve cevaplar basit metin karşılaştırmasıyla değerlendirilebilir.

## 10. GLUE ve SuperGLUE

GLUE, doğal dil anlama görevlerini bir araya getiren çok görevli bir benchmarktır. Tek bir soru türüne odaklanmak yerine, farklı dil anlama görevleri üzerinden modelleri karşılaştırmayı amaçlar.

GLUE içinde duygu analizi, cümle benzerliği, doğal dil çıkarımı ve metin sınıflandırma gibi görevler bulunur. Bu nedenle cevap formatı göreve göre değişir. Bazı görevlerde sınıf etiketi beklenirken, bazı görevlerde benzerlik skoru veya doğru/yanlış kararı beklenir.

GLUE'nun ölçtüğü temel beceriler şunlardır:

* Cümle sınıflandırma
* Cümleler arası anlam ilişkisi kurma
* Metin benzerliği ölçme
* Doğal dil çıkarımı

SuperGLUE ise GLUE'dan sonra daha zor bir benchmark olarak hazırlanmıştır. GLUE üzerinde modellerin performansı yükseldikçe, daha ayırt edici ve zor görevlerden oluşan yeni bir değerlendirme setine ihtiyaç duyulmuştur.

GLUE ve SuperGLUE'da kullanılan metrikler göreve göre değişir:

* Accuracy
* F1
* Pearson / Spearman korelasyonu
* Exact Match

Bu proje açısından GLUE ve SuperGLUE, çok görevli değerlendirme fikrini anlamak için önemlidir. Ancak başlangıçta bu kadar farklı görev tipini aynı anda ele almak yerine, tek bir görev türüyle başlamak daha uygundur.

## 11. Türkçe LLM Benchmark Örnekleri

LLM değerlendirme çalışmalarında İngilizce benchmarklar daha yaygın olsa da Türkçe için de yeni benchmark çalışmaları bulunmaktadır. Türkçe benchmarklar önemlidir çünkü Türkçenin eklemeli yapısı, kelime sırası, deyimleri ve kültürel bilgileri İngilizceden farklıdır.

Türkçe LLM benchmark örnekleri şunlardır:

* TR-MMLU: Türkçe MMLU benzeri bir benchmarktır. Türkçe eğitim sistemiyle ilişkili çoktan seçmeli sorular üzerinden modellerin Türkçe akademik ve kavramsal bilgisini ölçmeyi amaçlar.
* Cetvel: Türkçe dil anlama, dil üretimi ve kültürel bilgi görevlerini birlikte ele alan kapsamlı bir benchmark çalışmasıdır. Dil bilgisi düzeltme, makine çevirisi ve Türkçe odaklı soru cevaplama gibi görevleri içerir.
* TurkBench: Türkçe büyük dil modellerini bilgi, dil anlama, akıl yürütme, içerik denetimi, Türkçe dil bilgisi ve yönerge takibi gibi farklı başlıklarda değerlendirmeyi amaçlayan bir benchmarktır.

Bu örnekler, Türkçe LLM değerlendirmesinin yalnızca İngilizce veri setlerini çevirmekten ibaret olmadığını gösterir. Bir model Türkçe cevap üretebilse bile Türkçe dil bilgisi, kültürel bağlam ve yerel bilgi sorularında ayrıca test edilmelidir.

Bu proje başlangıç aşamasında olduğu için bu büyük Türkçe benchmarkların tamamını kullanmak yerine, Türkçe küçük bir soru-cevap veya çoktan seçmeli örnek veri seti hazırlamak daha uygulanabilir görünmektedir.

## 12. Bu Proje İçin Uygun Başlangıç Benchmark Türü

Bu proje öğrenme ve temel değerlendirme mantığını kavrama amacıyla yürütüldüğü için başlangıçta küçük, anlaşılır ve kolay değerlendirilebilir bir benchmark türü seçilmelidir.

Başlangıç için en uygun seçenekler şunlardır:

* Çoktan seçmeli soru-cevap benchmarkı
* Kısa cevaplı genel bilgi benchmarkı
* Küçük paragraf-soru-cevap benchmarkı

Bu üç seçenek içinde en pratik başlangıç türü çoktan seçmeli veya kısa cevaplı soru-cevap benchmarkıdır. Çünkü beklenen cevap nettir ve accuracy metriği kolayca hesaplanabilir.

Örneğin veri seti şu alanlardan oluşabilir:

```json
{
  "id": 1,
  "question": "Türkiye'nin başkenti neresidir?",
  "expected_answer": "Ankara",
  "category": "genel_bilgi"
}
```

Çoktan seçmeli format kullanılacaksa yapı şu şekilde olabilir:

```json
{
  "id": 1,
  "question": "Türkiye'nin başkenti neresidir?",
  "choices": ["İstanbul", "Ankara", "İzmir", "Bursa"],
  "expected_answer": "B",
  "category": "genel_bilgi"
}
```

Bu proje için başlangıçta önerilen yaklaşım şudur:

1. Küçük bir Türkçe soru-cevap veri seti hazırlanır.
2. Cevap formatı açıkça belirlenir.
3. Modelden yalnızca beklenen formatta cevap istenir.
4. Accuracy ve format uyumu gibi basit metriklerle değerlendirme yapılır.
5. Hatalar daha sonra manuel olarak incelenir.

Bu yaklaşım, MMLU ve ARC gibi çoktan seçmeli benchmarkların basit bir versiyonu olarak düşünülebilir. Böylece büyük ve karmaşık benchmark frameworklerine geçmeden önce temel değerlendirme akışı öğrenilmiş olur.

## 13. Kısa Özet

Bugün yaygın LLM benchmark veri setleri incelendi. MMLU'nun genel ve akademik bilgi ölçtüğü, GSM8K'nin matematiksel akıl yürütmeye odaklandığı, ARC'nin fen bilgisi soruları içerdiği ve HellaSwag'in sağduyu çıkarımını test ettiği görüldü.

TruthfulQA'nın modellerin yanıltıcı olmayan doğru cevaplar verip vermediğini ölçtüğü, HumanEval'in kod üretme becerisine odaklandığı, SQuAD'ın okuduğunu anlama için kullanıldığı, GLUE ve SuperGLUE'nun ise çok görevli doğal dil anlama benchmarkları olduğu açıklandı.

Ayrıca Türkçe LLM değerlendirmesi için TR-MMLU, Cetvel ve TurkBench gibi örnekler incelendi. Bu proje için başlangıçta büyük veri setleri indirmek yerine, küçük ve anlaşılır bir Türkçe soru-cevap veya çoktan seçmeli benchmark yapısının daha uygun olduğu sonucuna varıldı.

Bu doküman sonucunda `docs/02_benchmark_veri_setleri.md` dosyası oluşturulmuştur. Dosya, ilerleyen günlerde hazırlanacak örnek veri seti ve değerlendirme metrikleri çalışmaları için temel kaynak niteliğindedir.

## 14. İncelenen Kaynaklar

* MMLU: [Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)
* GSM8K: [Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)
* ARC: [Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge](https://arxiv.org/abs/1803.05457)
* HellaSwag: [HellaSwag: Can a Machine Really Finish Your Sentence?](https://arxiv.org/abs/1905.07830)
* TruthfulQA: [TruthfulQA: Measuring How Models Mimic Human Falsehoods](https://arxiv.org/abs/2109.07958)
* TruthfulQA GitHub: [sylinrl/TruthfulQA](https://github.com/sylinrl/TruthfulQA)
* HumanEval: [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
* HumanEval GitHub: [openai/human-eval](https://github.com/openai/human-eval)
* SQuAD: [SQuAD: 100,000+ Questions for Machine Comprehension of Text](https://arxiv.org/abs/1606.05250)
* SQuAD 2.0: [Know What You Don't Know: Unanswerable Questions for SQuAD](https://arxiv.org/abs/1806.03822)
* SQuAD resmi sayfası: [The Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/)
* GLUE: [GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding](https://arxiv.org/abs/1804.07461)
* SuperGLUE: [SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems](https://arxiv.org/abs/1905.00537)
* TR-MMLU: [Setting Standards in Turkish NLP: TR-MMLU for Large Language Model Evaluation](https://arxiv.org/abs/2501.00593)
* Cetvel: [A Unified Benchmark for Evaluating Language Understanding, Generation and Cultural Capacity of LLMs for Turkish](https://arxiv.org/abs/2508.16431)
* TurkBench: [A Benchmark for Evaluating Turkish Large Language Models](https://arxiv.org/abs/2601.07020)
