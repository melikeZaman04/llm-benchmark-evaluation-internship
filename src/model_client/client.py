"""
Yerel model istemcisi — Ollama / LM Studio (OpenAI-uyumlu endpoint).

Ollama (varsayılan http://localhost:11434/v1) ve LM Studio (varsayılan
http://localhost:1234/v1) aynı OpenAI-uyumlu Chat Completions arayüzünü
sunar. Bu yüzden tek bir istemci sınıfı her ikisiyle de çalışır; yalnızca
`base_url` (ve model adı) değişir.

Bu modül benchmark'ın DEĞERLENDİRİLEN öznesine dokunur. Model çıktısına
asla "doğru/yanlış" yargısı vermez — o karar Sandbox + Oracle'a aittir.
Buradaki tek iş, deterministik ve tekrar edilebilir biçimde ham metin almaktır.
"""

from __future__ import annotations

import json
import os

import requests

# Sağlayıcı hazır ayarları (preset). Ortam değişkenleriyle ezilebilir.
OLLAMA_BASE_URL = "http://localhost:11434/v1"
LM_STUDIO_BASE_URL = "http://localhost:1234/v1"


class ModelBaglantiHatasi(RuntimeError):
    """Yerel model sunucusuna ulaşılamadığında ya da hatalı yanıt geldiğinde."""


class ModelIstemcisi:
    """
    OpenAI-uyumlu bir Chat Completions endpoint'ine konuşan sade istemci.

    Örnek:
        istemci = ModelIstemcisi.ollama(model="gemma2:2b")
        sonuc = istemci.uret("Merhaba de.")
        print(sonuc["metin"])
    """

    def __init__(
        self,
        model: str,
        base_url: str = OLLAMA_BASE_URL,
        api_key: str = "yerel",
        timeout_sn: int = 120,
        temperature: float = 0.0,
        max_tokens: int | None = 1024,
    ) -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_sn = timeout_sn
        self.temperature = temperature
        self.max_tokens = max_tokens

    # --- Sağlayıcıya özel kısayollar -------------------------------------
    @classmethod
    def ollama(cls, model: str | None = None, **kwargs) -> "ModelIstemcisi":
        """Ollama için istemci. Model adı env `TRC_MODEL` ile de verilebilir."""
        base_url = os.environ.get("TRC_MODEL_BASE_URL", OLLAMA_BASE_URL)
        model = model or os.environ.get("TRC_MODEL", "gemma2:2b")
        return cls(model=model, base_url=base_url, **kwargs)

    @classmethod
    def lm_studio(cls, model: str | None = None, **kwargs) -> "ModelIstemcisi":
        """LM Studio için istemci."""
        base_url = os.environ.get("TRC_MODEL_BASE_URL", LM_STUDIO_BASE_URL)
        model = model or os.environ.get("TRC_MODEL", "local-model")
        return cls(model=model, base_url=base_url, **kwargs)

    # --- Ana çağrı --------------------------------------------------------
    def uret(self, prompt: str, sistem: str | None = None) -> dict:
        """
        Modelden tek seferlik bir yanıt üretir.

        Dönüş (dict):
          {
            "metin": str,          # modelin ürettiği ham metin
            "model": str,          # yanıtı üreten model adı
            "kullanim": dict|None, # token kullanımı (varsa)
            "bitis_nedeni": str|None,
          }

        Hata: bağlantı/timeout/geçersiz yanıt durumunda ModelBaglantiHatasi.
        """
        mesajlar = []
        if sistem:
            mesajlar.append({"role": "system", "content": sistem})
        mesajlar.append({"role": "user", "content": prompt})

        govde = {
            "model": self.model,
            "messages": mesajlar,
            "temperature": self.temperature,
            "stream": False,
        }
        if self.max_tokens is not None:
            govde["max_tokens"] = self.max_tokens

        url = f"{self.base_url}/chat/completions"
        try:
            yanit = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(govde),
                timeout=self.timeout_sn,
            )
        except requests.exceptions.ConnectionError as e:
            raise ModelBaglantiHatasi(
                f"Model sunucusuna ulaşılamadı ({url}). "
                "Ollama için `ollama serve`, LM Studio için yerel sunucunun "
                "açık olduğundan emin ol."
            ) from e
        except requests.exceptions.Timeout as e:
            raise ModelBaglantiHatasi(
                f"Model {self.timeout_sn} sn içinde yanıt vermedi ({url})."
            ) from e

        if yanit.status_code != 200:
            raise ModelBaglantiHatasi(
                f"Model sunucusu HTTP {yanit.status_code} döndü: "
                f"{yanit.text[:300]}"
            )

        try:
            veri = yanit.json()
            secim = veri["choices"][0]
            metin = secim["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
            raise ModelBaglantiHatasi(
                f"Model yanıtı beklenen biçimde değil: {yanit.text[:300]}"
            ) from e

        return {
            "metin": metin,
            "model": veri.get("model", self.model),
            "kullanim": veri.get("usage"),
            "bitis_nedeni": secim.get("finish_reason"),
        }

    def erisilebilir_mi(self) -> bool:
        """Sunucu ayakta mı? Model listesi ucunu yoklar (hızlı sağlık kontrolü)."""
        try:
            yanit = requests.get(f"{self.base_url}/models", timeout=5)
            return yanit.status_code == 200
        except requests.exceptions.RequestException:
            return False


if __name__ == "__main__":
    # Hızlı duman testi: sunucu + model varsa kısa bir yanıt alır,
    # yoksa kurulum yönergesini yazar (asla exception fırlatmaz).
    istemci = ModelIstemcisi.ollama()
    print(f"Sunucu: {istemci.base_url}  |  Model: {istemci.model}")
    if not istemci.erisilebilir_mi():
        print("Sunucuya ulaşılamadı. `ollama serve` çalışıyor mu?")
        raise SystemExit(0)
    try:
        sonuc = istemci.uret("Yalnızca 'merhaba' yaz.")
        print("Yanıt:", sonuc["metin"][:200])
        print("Kullanım:", sonuc["kullanim"])
    except ModelBaglantiHatasi as e:
        print("Hata:", e)
        print("İpucu: `ollama pull gemma2:2b` ile küçük bir model indir.")
