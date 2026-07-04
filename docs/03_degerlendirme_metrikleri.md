# LLM Değerlendirme Metrikleri

Bu dokümanda LLM benchmark değerlendirmelerinde kullanılan temel metrikler incelenmiştir. Amaç, farklı görev türlerinde model çıktılarının nasıl ölçülebileceğini anlamaktır.

Bu aşamada herhangi bir model çalıştırılmamış, veri seti indirilmemiş ve gerçek metrik hesaplaması yapılmamıştır. Çalışma yalnızca araştırma ve dokümantasyon odaklıdır.

## 1. Değerlendirme Metriği Nedir?

Değerlendirme metriği, bir modelin verdiği cevabın ne kadar başarılı olduğunu sayısal veya kurallı bir şekilde ölçmek için kullanılan yöntemdir. LLM benchmark çalışmalarında metrikler, model cevabı ile beklenen cevap arasındaki ilişkiyi ölçmeye yarar.

Örneğin bir soru-cevap benchmarkında modelin doğru cevap verdiği soru sayısı ölçülebilir. Bir özetleme görevinde ise modelin ürettiği özet ile referans özet arasındaki kelime örtüşmesi incelenebilir. Kod üretme görevinde ise modelin ürettiği kodun testlerden geçip geçmediği kontrol edilebilir.

Metrik seçimi, değerlendirme görevinin türüne bağlıdır. Her görev için aynı metriği kullanmak doğru değildir.

## 2. LLM Değerlendirmesinde Metrikler Neden Önemlidir?

LLM çıktıları doğal dil şeklinde olduğu için değerlendirme her zaman kolay değildir. Bazı cevaplar tek kelime veya tek seçenek olabilirken, bazı cevaplar uzun açıklama, paragraf, kod veya matematik çözümü olabilir.

Metrikler şu nedenlerle önemlidir:

* Model başarısını sayısal olarak ifade etmeyi sağlar.
* Farklı modelleri aynı veri seti üzerinde karşılaştırmayı kolaylaştırır.
* Prompt değişikliklerinin sonuca etkisini göstermeye yardımcı olur.
* Modelin hangi görevlerde güçlü veya zayıf olduğunu anlamayı sağlar.
* Değerlendirme sonuçlarının raporlanmasını kolaylaştırır.

Ancak metrikler tek başına her zaman yeterli değildir. Özellikle serbest metin cevaplarda model anlam olarak doğru cevap verebilir ama beklenen cevapla kelime kelime aynı olmayabilir. Bu nedenle otomatik metriklerin yanında gerektiğinde manuel hata analizi de yapılmalıdır.

## 3. Accuracy

Accuracy, en temel değerlendirme metriklerinden biridir. Modelin doğru cevapladığı örnek sayısının toplam örnek sayısına oranını gösterir.

Formül şu şekilde ifade edilebilir:

```text
accuracy = doğru cevap sayısı / toplam örnek sayısı
```

Örneğin 10 soruluk bir benchmarkta model 8 soruya doğru cevap verdiyse:

```text
accuracy = 8 / 10 = 0.80
```

Bu durumda modelin accuracy değeri yüzde 80 olarak yorumlanabilir.

Accuracy özellikle şu görevlerde kullanışlıdır:

* Çoktan seçmeli soru cevaplama
* Doğru / yanlış sınıflandırma
* Etiket sınıflandırma
* Kısa ve net cevaplı benchmarklar

MMLU, ARC ve HellaSwag gibi çoktan seçmeli benchmarklarda accuracy yaygın olarak kullanılır. Bu proje için de başlangıçta en uygun metriklerden biridir.

Accuracy'nin sınırlı olduğu durumlar da vardır. Örneğin veri setinde sınıflar dengesizse, model çoğunluk sınıfını tahmin ederek yüksek accuracy alabilir. Ayrıca uzun serbest metin cevaplarda yalnızca doğru / yanlış kararı vermek yeterli olmayabilir.

## 4. Exact Match

Exact Match, model cevabının beklenen cevapla tamamen aynı olup olmadığını kontrol eder. Cevap birebir aynıysa doğru, farklıysa yanlış kabul edilir.

Örnek:

```text
Beklenen cevap: Ankara
Model cevabı: Ankara
Sonuç: Doğru
```

Farklı bir örnek:

```text
Beklenen cevap: Ankara
Model cevabı: Türkiye'nin başkenti Ankara'dır.
Sonuç: Strict exact match için yanlış
```

İkinci örnekte cevap anlam olarak doğrudur, fakat birebir aynı değildir. Bu nedenle exact match kullanılırken değerlendirme kuralının net belirlenmesi gerekir.

Exact Match iki şekilde ele alınabilir:

* Strict exact match: Cevap tamamen aynı olmalıdır.
* Normalize edilmiş exact match: Büyük/küçük harf, boşluk veya noktalama gibi küçük farklar temizlendikten sonra karşılaştırma yapılır.

Exact Match özellikle şu görevlerde kullanılır:

* Kısa cevaplı soru-cevap görevleri
* Sayısal cevap beklenen matematik soruları
* Metinden cevap çıkarma görevleri

Bu proje için kısa cevaplı sorularda normalize edilmiş exact match yaklaşımı kullanılabilir.

## 5. Precision, Recall ve F1-score

Precision, recall ve F1-score daha çok sınıflandırma ve bilgi çıkarımı görevlerinde kullanılan metriklerdir. Bu metrikler özellikle doğru pozitif, yanlış pozitif ve yanlış negatif kavramlarına dayanır.

Temel kavramlar:

* True Positive (TP): Modelin pozitif dediği ve gerçekten pozitif olan örnekler
* False Positive (FP): Modelin pozitif dediği ama gerçekte pozitif olmayan örnekler
* False Negative (FN): Modelin negatif dediği ama gerçekte pozitif olan örnekler

Precision, modelin pozitif olarak işaretlediği örneklerin ne kadarının gerçekten doğru olduğunu gösterir.

```text
precision = TP / (TP + FP)
```

Recall, gerçekte pozitif olan örneklerin ne kadarının model tarafından yakalandığını gösterir.

```text
recall = TP / (TP + FN)
```

F1-score ise precision ve recall değerlerinin dengeli bir ortalamasıdır.

```text
F1 = 2 * precision * recall / (precision + recall)
```

F1-score metriği, precision ve recall arasında denge kurmak istendiğinde kullanışlıdır. Özellikle sınıflar dengesiz olduğunda accuracy tek başına yeterli olmayabilir.

LLM değerlendirmesinde F1 şu durumlarda kullanılabilir:

* Metinden cevap çıkarma
* Varlık tanıma
* Bilgi çıkarımı
* Sınıflandırma görevleri

Bu proje başlangıcında F1-score doğrudan ilk metrik olmayabilir. Ancak ilerleyen günlerde metin tabanlı cevap karşılaştırması yapılırsa önemli hale gelebilir.

## 6. SQuAD Tarzı Exact Match ve F1

SQuAD gibi okuduğunu anlama benchmarklarında modele bir paragraf ve soru verilir. Modelden beklenen cevap genellikle paragraf içindeki kısa bir metin parçasıdır.

Bu tür görevlerde iki metrik sık kullanılır:

* Exact Match
* Token düzeyinde F1

Exact Match, model cevabının referans cevapla aynı olup olmadığını kontrol eder. Token düzeyinde F1 ise model cevabı ile beklenen cevap arasındaki kelime örtüşmesini dikkate alır.

Örnek:

```text
Beklenen cevap: Ankara
Model cevabı: Ankara şehri
```

Bu cevap strict exact match açısından yanlış olabilir. Ancak kelime örtüşmesi olduğu için F1 değeri tamamen sıfır olmayabilir.

Bu yaklaşım, serbest metin cevaplarda exact match'in fazla katı kaldığı durumlarda daha esnek bir değerlendirme sağlar.

## 7. BLEU

BLEU, özellikle makine çevirisi değerlendirmelerinde kullanılan otomatik bir metriktir. Modelin ürettiği metin ile referans metin arasındaki n-gram örtüşmesini ölçer.

N-gram, ardışık kelime grupları anlamına gelir. Örneğin "büyük dil modeli" ifadesinde:

* 1-gram: büyük, dil, modeli
* 2-gram: büyük dil, dil modeli
* 3-gram: büyük dil modeli

BLEU, model çevirisinin referans çeviriye ne kadar benzediğini ölçmeye çalışır. Değer yükseldikçe üretilen metnin referansa daha çok benzediği kabul edilir.

BLEU şu görevlerde kullanılabilir:

* Makine çevirisi
* Bazı kontrollü metin üretimi görevleri

Ancak BLEU'nun önemli sınırlılıkları vardır. Anlam olarak doğru ama farklı kelimelerle yazılmış bir cevap düşük BLEU alabilir. Bu nedenle açık uçlu LLM cevaplarını değerlendirmek için tek başına yeterli değildir.

Bu proje başlangıcında BLEU kullanılmayacaktır. Ancak metin üretimi veya çeviri değerlendirmesi yapılacaksa ileride incelenebilir.

## 8. ROUGE

ROUGE, özellikle otomatik özetleme değerlendirmelerinde kullanılan bir metrik ailesidir. Modelin ürettiği özet ile referans özet arasındaki kelime veya ifade örtüşmesini ölçer.

Yaygın ROUGE türleri şunlardır:

* ROUGE-1: Tek kelimelik örtüşmeleri ölçer.
* ROUGE-2: İki kelimelik ardışık örtüşmeleri ölçer.
* ROUGE-L: En uzun ortak alt diziye dayalı benzerliği ölçer.

ROUGE şu görevlerde kullanılabilir:

* Metin özetleme
* Uzun cevap karşılaştırma
* Referans metne bağlı üretim görevleri

ROUGE, özetleme görevleri için faydalıdır. Ancak yalnızca kelime örtüşmesine dayandığı için anlam benzerliğini her zaman doğru yansıtmayabilir. Model iyi bir özet üretse bile referans özetteki kelimeleri kullanmadıysa ROUGE düşük çıkabilir.

Bu proje başlangıcında özetleme görevi yapılmayacağı için ROUGE ilk uygulanacak metriklerden biri değildir.

## 9. Perplexity

Perplexity, bir dil modelinin verilen metni ne kadar iyi olasılıksal olarak tahmin ettiğini ölçen bir metriktir. Daha düşük perplexity değeri, modelin metni daha beklenen veya daha iyi tahmin edilebilir bulduğunu gösterebilir.

Perplexity daha çok dil modeli eğitimi ve dil modelleme kalitesini inceleme çalışmalarında kullanılır. Ancak LLM benchmark değerlendirmelerinde her zaman pratik bir metrik değildir. Çünkü birçok kapalı modelde token olasılıklarına erişilemeyebilir ve kullanıcıya verilen cevap kalitesi yalnızca perplexity ile açıklanamaz.

Perplexity şu durumlarda kullanılabilir:

* Dil modeli karşılaştırma
* Metin olasılığı inceleme
* Model eğitimi veya fine-tuning sürecini takip etme

Bu proje başlangıcında perplexity kullanılmayacaktır. Çünkü proje, modelin iç olasılık değerlerini incelemekten çok çoktan seçmeli cevap doğruluğu ve format uyumu üzerine kuruludur.

## 10. pass@k

pass@k, özellikle kod üretme benchmarklarında kullanılan bir metriktir. HumanEval gibi benchmarklarda modelden bir programlama problemini çözen kod üretmesi beklenir. Üretilen kod testlerden geçirilir.

pass@k, modelin ürettiği k farklı çözümden en az birinin doğru olma olasılığını ifade eder.

Örneğin:

```text
pass@1: Modelin ilk ürettiği çözüm testleri geçti mi?
pass@10: Modelin 10 farklı çözümünden en az biri testleri geçti mi?
```

Kod üretme görevlerinde model bazen ilk denemede yanlış, sonraki denemelerde doğru çözüm üretebilir. Bu nedenle pass@k, birden fazla örnekleme yapılan senaryolarda anlamlıdır.

Bu proje başlangıcında pass@k kullanılmayacaktır. Çünkü kod çalıştırma, test ortamı kurma ve güvenli sandbox kullanımı gibi ek konular gerektirir.

## 11. Format Uyumu (Format Compliance)

Format uyumu, modelin cevabının istenen çıktı formatına uyup uymadığını ölçer. LLM değerlendirmelerinde doğru bilgi kadar cevap formatı da önemlidir.

Örneğin modelden yalnızca seçenek harfi istenmiş olabilir:

```text
Beklenen format: A, B, C veya D
Model cevabı: B
Sonuç: Format uyumlu
```

Farklı bir örnek:

```text
Beklenen format: A, B, C veya D
Model cevabı: Doğru cevap B seçeneğidir çünkü...
Sonuç: Format uyumsuz
```

İkinci cevap bilgi olarak doğru olabilir, fakat beklenen format yalnızca tek harf olduğu için format uyumu açısından başarısız sayılabilir.

Format compliance şu şekilde hesaplanabilir:

```text
format compliance = formata uyan cevap sayısı / toplam cevap sayısı
```

Bu proje için format uyumu özellikle önemlidir. Çünkü küçük benchmarklarda modelden belirli bir cevap biçimi istenecek ve modelin bu biçime uyup uymadığı ayrıca ölçülecektir.

## 12. İnsan Değerlendirmesi ve LLM-as-a-Judge

Bazı LLM cevapları otomatik metriklerle kolay değerlendirilemez. Özellikle açık uçlu açıklamalar, yaratıcı metinler, uzun cevaplar veya yorum gerektiren görevlerde insan değerlendirmesi gerekebilir.

İnsan değerlendirmesinde cevaplar belirli ölçütlere göre incelenebilir:

* Doğruluk
* Açıklık
* Tutarlılık
* Eksiksizlik
* Zararsızlık
* Göreve uygunluk

LLM-as-a-Judge yaklaşımında ise başka bir dil modeli, üretilen cevapları değerlendirmek için kullanılır. Bu yöntem pratik olabilir ancak dikkatli kullanılmalıdır. Çünkü değerlendiren model de hata yapabilir, yanlı davranabilir veya değerlendirme ölçütlerini tutarsız uygulayabilir.

Bu proje başlangıcında insan değerlendirmesi yalnızca hata analizi ve yorumlama amacıyla kullanılabilir. LLM-as-a-Judge yöntemi ilk aşamada tercih edilmeyecektir.

## 13. Benchmark Türüne Göre Metrik Seçimi

Farklı benchmark türleri için uygun metrikler değişir. Aşağıdaki tablo genel bir karşılaştırma sunar.

| Görev Tipi | Örnek Benchmark | Uygun Metrikler |
|---|---|---|
| Çoktan seçmeli soru cevaplama | MMLU, ARC, HellaSwag | Accuracy, Format Compliance |
| Kısa cevaplı soru cevaplama | Basit QA veri seti | Exact Match, Accuracy |
| Okuduğunu anlama | SQuAD | Exact Match, F1-score |
| Matematik problemi | GSM8K | Exact Match, Accuracy |
| Sınıflandırma | GLUE görevleri | Accuracy, Precision, Recall, F1-score |
| Çeviri | Makine çevirisi benchmarkları | BLEU |
| Özetleme | Özetleme veri setleri | ROUGE |
| Kod üretme | HumanEval | pass@k |
| Dil modelleme | Dil modeli testleri | Perplexity |
| Açık uçlu cevap | TruthfulQA, sohbet değerlendirmeleri | İnsan değerlendirmesi, LLM-as-a-Judge |

Bu tablo, metrik seçiminin görevden bağımsız yapılamayacağını göstermektedir.

| Metrik | Kullanıldığı Görevler | Ne Ölçer? | Avantajı | Sınırlılığı | Bu Projede Kullanım Durumu |
|---|---|---|---|---|---|
| Accuracy | Çoktan seçmeli soru cevaplama, sınıflandırma | Doğru cevap oranını | Kolay hesaplanır ve yorumlanır | Dengesiz veri setlerinde yanıltıcı olabilir | İlk deneylerde kullanılacaktır |
| Format Compliance | Format kısıtı olan LLM cevapları | Cevabın istenen biçime uyup uymadığını | Prompt uyumunu ayrı ölçer | Bilginin doğru olup olmadığını tek başına göstermez | İlk deneylerde kullanılacaktır |
| Exact Match | Kısa cevaplı soru cevaplama | Cevabın beklenen cevapla birebir eşleşmesini | Net ve basittir | Anlamca doğru farklı ifadeleri yanlış sayabilir | Yardımcı metrik olarak incelenebilir |
| Precision | Sınıflandırma, bilgi çıkarımı | Pozitif tahminlerin ne kadarının doğru olduğunu | Yanlış pozitifleri görünür kılar | Tek başına kaçırılan doğru örnekleri göstermez | İlk aşamada kullanılmayacaktır |
| Recall | Sınıflandırma, bilgi çıkarımı | Gerçek pozitiflerin ne kadarının yakalandığını | Kaçırılan örnekleri gösterir | Yanlış pozitifleri tek başına yeterince açıklamaz | İlk aşamada kullanılmayacaktır |
| F1-score | Sınıflandırma, metinden cevap çıkarma | Precision ve recall dengesini | Dengesiz sınıflarda faydalıdır | Accuracy kadar sezgisel olmayabilir | İlk aşamada kullanılmayacaktır |
| BLEU | Çeviri | Referansla n-gram örtüşmesini | Çeviri için yaygın kullanılır | Anlam benzerliğini her zaman yakalayamaz | Kullanılmayacaktır |
| ROUGE | Özetleme | Referans özetle kelime örtüşmesini | Özetleme için yaygındır | Farklı ama doğru özetleri düşük puanlayabilir | Kullanılmayacaktır |
| Perplexity | Dil modelleme | Modelin metni olasılıksal tahmin başarısını | Model içi kaliteyi izlemeye yardım eder | Kapalı modellerde erişilemeyebilir | Kullanılmayacaktır |
| pass@k | Kod üretme | Üretilen çözümlerden en az birinin testleri geçmesini | Kod benchmarkları için uygundur | Kod çalıştırma ortamı gerektirir | Kullanılmayacaktır |

## 14. Bu Proje İçin Başlangıçta Kullanılacak Metrikler

Bu proje öğrenme amaçlı olduğu için ilk aşamada basit ve yorumlanabilir metriklerle başlanacaktır. Büyük ve karmaşık değerlendirme yöntemleri yerine, küçük Türkçe soru-cevap örnekleri üzerinde anlaşılır hesaplamalar yapılacaktır.

Bu projenin ilk deneylerinde Accuracy ve Format Compliance kullanılacaktır.

Başlangıç için en uygun metrikler şunlardır:

* Accuracy
* Format Compliance

Bu metrikler şu nedenlerle uygundur:

* Hesaplamaları kolaydır.
* Küçük veri setlerinde rahat yorumlanabilir.
* Çoktan seçmeli ve kısa cevaplı sorular için uygundur.
* Model cevaplarının hem doğruluğunu hem de format uyumunu ölçmeyi sağlar.

İlk uygulama aşamasında örnek bir sonuç tablosu şu alanları içerebilir:

```text
id
question
answer
model_answer
is_correct
format_ok
error_type
```

Bu yapı sayesinde hem otomatik metrik hesaplanabilir hem de daha sonra hata analizi yapılabilir.

## 15. Metriklerin Sınırlılıkları

Metrikler değerlendirme sürecini düzenli hale getirir, ancak her zaman model kalitesini tam olarak yansıtmaz.

Önemli sınırlılıklar şunlardır:

* Exact Match anlam olarak doğru ama farklı yazılmış cevapları yanlış sayabilir.
* Accuracy, dengesiz veri setlerinde yanıltıcı olabilir.
* BLEU ve ROUGE kelime örtüşmesine dayanır, anlam benzerliğini her zaman yakalayamaz.
* pass@k kod üretme dışındaki görevler için uygun değildir.
* İnsan değerlendirmesi daha esnek olsa da zaman alır ve öznel olabilir.
* LLM-as-a-Judge pratik olsa da değerlendiren modelin hatalarından etkilenebilir.

Bu nedenle değerlendirme sonuçları yorumlanırken yalnızca sayısal değere bakılmamalıdır. Hangi görevde, hangi veri setinde ve hangi cevap formatıyla ölçüm yapıldığı da belirtilmelidir.

## 16. Kısa Özet

Bugün LLM değerlendirme metrikleri incelendi. Accuracy, Exact Match, precision, recall, F1-score, BLEU, ROUGE, Perplexity, pass@k ve format compliance gibi metriklerin hangi durumlarda kullanıldığı açıklandı.

Çoktan seçmeli ve kısa cevaplı benchmarklarda accuracy ve exact match metriklerinin kullanışlı olduğu görüldü. Okuduğunu anlama görevlerinde F1, çeviri görevlerinde BLEU, özetleme görevlerinde ROUGE ve kod üretme görevlerinde pass@k metriklerinin öne çıktığı anlaşıldı.

Bu projenin ilk deneylerinde accuracy ve format compliance metriklerinin yeterli ve uygun olduğu sonucuna varıldı. İlerleyen günlerde küçük bir Türkçe soru-cevap veri seti hazırlanarak bu metriklerin pratikte nasıl hesaplanacağı uygulanacaktır.

## 17. İncelenen Kaynaklar

* scikit-learn: [Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html)
* scikit-learn: [accuracy_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
* scikit-learn: [precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)
* scikit-learn: [recall_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)
* scikit-learn: [f1_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)
* SQuAD: [The Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/)
* BLEU: [BLEU: a Method for Automatic Evaluation of Machine Translation](https://aclanthology.org/P02-1040/)
* ROUGE: [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)
* HumanEval: [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
* HumanEval GitHub: [openai/human-eval](https://github.com/openai/human-eval)
* GLUE: [GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding](https://arxiv.org/abs/1804.07461)
* LLM-as-a-Judge: [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)
