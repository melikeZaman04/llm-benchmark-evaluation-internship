# LLM Benchmark Değerlendirme Projesi

## Projenin Amacı

Bu projede benchmark veri setleri ve değerlendirme metrikleri üzerinden LLM değerlendirme mantığı incelenecektir. İlk aşamada küçük ve yönetilebilir Türkçe örnekler kullanılacak, model cevaplarının nasıl standart promptlarla alınabileceği ve daha sonra nasıl değerlendirilebileceği öğrenilecektir.

Bu proje büyük ölçekli model eğitimi veya üretim sistemi kurma projesi değildir. Amaç, benchmark veri setleri ve değerlendirme metrikleri üzerinden LLM değerlendirme mantığını küçük ve yönetilebilir örneklerle öğrenmektir.

## Projenin Kapsamı

* LLM benchmark kavramını öğrenmek
* Yaygın benchmark veri setlerini incelemek
* Değerlendirme metriklerini anlamak
* Küçük bir çoktan seçmeli soru-cevap veri seti hazırlamak
* Prompt formatı ve değerlendirme akışını adım adım tasarlamak
* Model cevaplarını daha sonraki aşamalarda doğru cevaplarla karşılaştırmak
* Accuracy ve format compliance gibi temel metrikleri öğrenmek
* Hata analizi ve sonuç raporlama mantığını kavramak

## Kapsam Dışı Konular

* Büyük ölçekli model eğitimi yapılmayacak
* Üretim sistemi kurulmayacak
* Büyük GPU gerektiren deneyler yapılmayacak
* İlk aşamada karmaşık benchmark frameworkleri kullanılmayacak
* Büyük benchmark veri setleri indirilmeyecek
* Proje, öğrenme ve temel değerlendirme mantığını kavrama odaklı ilerleyecek

## 20 İş Günlük İlerleme Mantığı

Bu proje 20 iş gününe yayılmış şekilde ilerleyecektir. Her günün sonunda somut bir çıktı üretilecektir. Bu çıktı bazen bir Markdown dokümanı, bazen küçük bir Python dosyası, bazen veri dosyası, bazen sonuç tablosu, bazen de staj defterine yazılabilir günlük metni olacaktır.

İlk günlerde kavramsal hazırlık ve küçük veri seti oluşturma adımları yapılır. Sonraki günlerde prompt tasarımı, modelden cevap alma, metrik hesaplama, hata analizi ve sonuçların raporlanması adım adım ele alınır.

## Klasör Yapısı

```text
README.md
requirements.txt
docs/
  01_llm_benchmark_giris.md
  02_benchmark_veri_setleri.md
  03_degerlendirme_metrikleri.md
  staj_defteri_gunlukleri.md
notebooks/
src/
data/
  sample_questions.json
results/
  figures/
```

## Kullanılacak Araçlar

* Python
* Jupyter Notebook
* pandas
* scikit-learn
* matplotlib
* GitHub Issues
* GitHub Project Board

## Şu Ana Kadar Oluşturulan Çıktılar

* `docs/01_llm_benchmark_giris.md`: LLM, benchmark ve değerlendirme kavramlarına giriş
* `docs/02_benchmark_veri_setleri.md`: Yaygın LLM benchmark veri setlerinin karşılaştırılması
* `docs/03_degerlendirme_metrikleri.md`: LLM değerlendirme metriklerinin açıklanması
* `data/sample_questions.json`: İlk küçük çoktan seçmeli soru-cevap veri seti
* `src/prompt_builder.py`: Çoktan seçmeli soruları standart LLM prompt formatına dönüştürür
* `docs/staj_defteri_gunlukleri.md`: Günlük staj ilerleme notları

## Çalıştırma Notu

Bu aşamada proje ağırlıklı olarak dokümantasyon ve veri hazırlama odaklıdır. Henüz model çalıştırma, API çağrısı yapma, model çıktısı alma veya metrik hesaplama adımları tamamlanmış deney olarak ele alınmamıştır.

Day 06 aşamasına geçmeden önce repository içinde temel klasör yapısı, ilk üç dokümantasyon dosyası, staj defteri ve küçük çoktan seçmeli veri seti hazır olmalıdır.
