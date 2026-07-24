# TR-CodeEval Veri Seti Datasheet

> Gebru vd. "Datasheets for Datasets" yapısına göre. Amaç: kökeni, kapsamı,
> amaçlanan kullanımı ve **limitleri** dürüstçe belgelemek — bir benchmark'ın
> bilimsel güvenilirliğinin olmazsa olmazı. Sürüm: **v1 (62 görev)**, 2026-07-24.

## 1. Motivasyon
- **Neden?** Küçük yerel LLM'lerin (0.5–3B) elemanter Python kodlama yeteneğini
  ölçmek ve **Türkçe'de sorulunca performansın düşüp düşmediğini** ("Türkçe
  vergisi") + **ezber-direncini** kontrollü biçimde ölçmek.
- **Kim için?** Model seçimi/karşılaştırması yapan uygulayıcılar; Türkçe NLP/kod
  değerlendirmesi araştırması.
- **Boşluk:** Standart kod benchmark'ları (HumanEval, MBPP) İngilizce ve
  kontaminasyon riski taşır; Türkçe muhakeme vergisini ve ezberi ayrıştıran
  kontrollü, özgün, çift-dilli bir set yoktu.

## 2. Bileşim
- **62 görev** = 20 kanonik + 20 parametric_story (sığ gizleme) + 22 story_mutation
  (derin gizleme). **20/20 tam aile.**
- 6 kategori (diziler, string, matematik, mantık, özyineleme, sayma); zorluk 12
  kolay + 8 orta (**henüz zor yok** — bkz. limitler).
- Her görev: `prompt_tr`, `prompt_en`, `fonksiyon_imzasi(_en)`, `fonksiyon_adi(_en)`,
  `referans_cozum` (oracle için, TR), `test_cases` (~6), `karsilastirma` modu.
- Her örnek/hücre: pass@1/@k, örnek başına token, hata_tipi.

## 3. Toplama süreci
- **Özgün yazım** — hiçbir görev internetten/mevcut benchmark'lardan alınmadı
  (kontaminasyon güvenliği).
- Kanonik görevler elle tasarlandı; varyantlar **ajan fabrikasıyla** üretildi
  (Mutator: senaryo değişimi; Translator: çift-dilli kurulum), her varyant
  oracle + kalite kapılarından geçmeden kabul edilmedi.
- Tanımlayıcılar Design A ile dil-başına (EN tamamen İngilizce, TR tamamen Türkçe).

## 4. Ön-işleme / etiketleme
- **Doğruluk etiketi LLM'e bırakılmaz** — deterministik sandbox + oracle karar verir.
- Kalite kapıları: oracle guardrail, anlam-denetimi (ajan+insan), uzunluk kapısı,
  tanımlayıcı invariant (regresyon testli), değişmezler. 249 birim testi.

## 5. Amaçlanan kullanım
- **Uygun:** küçük LLM'lerin TR/EN kodlama karşılaştırması, Türkçe vergisi ve iki
  seviyeli ezber ölçümü; ölçüm anında ajan çağrılmaz (deterministik).
- **Uygun DEĞİL:** model **eğitimi** (bir benchmark eğitime sızarsa geçersizleşir);
  büyük/API modellere ya da ileri algoritmalara doğrudan genelleme (kapsam dışı).

## 6. Dağıtım ve bakım
- Git deposu; sürümler etiketle dondurulur, **dondurulmuş sürüm düzenlenmez**.
- Sonuçlar dataset-sürümü + koşum-config alıntılar. Büyütme `veri_seti_blueprint.md`
  sözleşmesine göre (v2 ~50, v3 ~120 kanonik).

## 7. Bilinen limitler (açık ve kayıtlı)
1. **n=20 kanonik** — HumanEval'in (164) altında; manşetler geniş CI'lara yaslanır.
2. **Zor tier yok** — 0 zor görev; güçlü modellerde (coder:3b 0.85) tavan etkisi.
3. **Yalnız 7 küçük yerel model** ölçüldü — büyük/API modellere genellenmeyebilir.
4. **Görev başına ~6 test** — HumanEval+'ın dersi: daha çok test yanlış-ama-geçen
   kodu daha iyi yakalar.
5. **Türkçe tanımlayıcı adlandırması yazarın tercihi** (özellikle mutasyonlarda) —
   ana-dil doğallık gözden geçirmesi sertleştirir.
6. **Anlam-denetimi tam mekanik değil** — ölçekte insan-gözü darboğazı.
7. **Yerel çıkarım 4GB VRAM'de bit-tekrarlanabilir değil** — greedy'de bile küçük
   sapma; bu yüzden tekrar + CI ile raporlanır.

## 8. Sürüm geçmişi
| Sürüm | Tarih | İçerik |
|---|---|---|
| v1 | 2026-07-24 | 62 görev (20 kanonik + 42 varyant), Design A tanımlayıcılar, ilk tam matris (868 hücre, n=5) |
