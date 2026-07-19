# Yerel Model İstemcisi

İki-düzlemli mimaride **test edilen özne**'nin arayüzü. Yerel bir dil
modelinden (Ollama / LM Studio) bir görev için **kod** çıktısı alır. Bu
çıktı güvenilmezdir; doğru/yanlış kararını Sandbox + Oracle verir.

Ollama ve LM Studio'nun ikisi de OpenAI-uyumlu `/v1/chat/completions`
sunar; bu yüzden tek bir istemci (`ModelIstemcisi`) her ikisiyle çalışır —
yalnızca `base_url` değişir.

## Kurulum (bir kez)

```bash
pip install requests

# Ollama: servisi başlat ve küçük bir model indir (4 GB VRAM'e uygun)
ollama serve &
ollama pull gemma2:2b        # ~1.6 GB  (alternatif: qwen2.5:0.5b ~400 MB)
```

LM Studio kullanılıyorsa: uygulamada "Local Server"ı başlat
(varsayılan `http://localhost:1234/v1`).

## Doğrulama (self-test)

```bash
python src/model_client/code_task.py   # model GEREKTİRMEZ: prompt + ayıklama
python src/model_client/client.py      # sunucu/model varsa kısa yanıt alır
```

## Kullanım (koddan)

```python
from src.model_client import ModelIstemcisi, modelden_cozum_al

istemci = ModelIstemcisi.ollama(model="gemma2:2b")   # ya da .lm_studio(...)
sonuc = modelden_cozum_al(gorev, istemci, dil="tr")  # görev -> prompt -> kod
print(sonuc["kod"])   # Sandbox'a verilmeye hazır Python kodu
```

`sonuc` alanları: `kod`, `ham_yanit`, `kullanim` (token), `prompt`, `dil`, `id`.

## Yapılandırma (ortam değişkenleri)

- `TRC_MODEL` — model adı (varsayılan `gemma2:2b`).
- `TRC_MODEL_BASE_URL` — endpoint (varsayılan Ollama `http://localhost:11434/v1`).

## Not

Bu modül kodu **çalıştırmaz** ve doğrulamaz; yalnızca üretip ayıklar.
Sonraki adım (dikey dilim): `modelden_cozum_al` çıktısını
`sandboxta_calistir` ile testlere sokup pass/fail almak.
