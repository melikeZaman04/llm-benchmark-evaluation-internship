"""
Yerel model istemcisi paketi.

İki-düzlemli mimaride bu paket, DÜZLEM 2'nin (deterministik oracle) değil,
**TEST EDİLEN ÖZNE**'nin arayüzüdür: yerel bir dil modelinden kod çıktısı
almak için kullanılır. Ollama ve LM Studio'nun ikisi de OpenAI-uyumlu bir
endpoint (/v1/chat/completions) sunduğu için tek bir istemci her ikisiyle
de çalışır — yalnızca `base_url` değişir.
"""

from .client import ModelIstemcisi, ModelBaglantiHatasi
from .code_task import kod_prompt_olustur, kod_ayikla, modelden_cozum_al

__all__ = [
    "ModelIstemcisi",
    "ModelBaglantiHatasi",
    "kod_prompt_olustur",
    "kod_ayikla",
    "modelden_cozum_al",
]
