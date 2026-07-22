"""
Genel Claude Code CLI çağırıcı — Düzlem 1'in (Yaratıcı Ajan Fabrikası) ortak
alt katmanı.

Mutator, (ileride) Translator, Test-Öneri ve Failure-Classifier ajanlarının
HEPSİ bu tek fonksiyonu kullanır: persona (sistem promptu) + görev-özel metin
-> JSON şemasına zorlanmış yapılandırılmış çıktı. Ham `anthropic` API paketi
yerine kurulu Claude Code CLI'nin headless (`-p`) modu kullanılır — ayrı bir
ANTHROPIC_API_KEY gerektirmez, mevcut Claude Code girişini (abonelik) kullanır.

Önkoşul: `claude` komutu PATH'te olmalı ve giriş yapılmış olmalı
(bkz. docs/staj_defteri_gunlukleri.md, Gün 13 girişi — kurulum notları).

Maliyet notu: `--system-prompt` her çağrıda AYNI persona metniyle verilirse,
Anthropic'in prompt önbelleklemesi ilk çağrıdan sonrakileri belirgin biçimde
ucuzlatır (pilotta ~4 kat). Bu yüzden persona metni ajan modüllerinde SABİT
tutulur, görev-özel içerik ayrı (stdin) gönderilir.
"""

from __future__ import annotations

import json
import subprocess


class AjanCagriHatasi(Exception):
    """
    claude CLI çağrısı başarısız olduğunda veya guardrail reddettiğinde fırlatılır.

    `maliyet_usd`: reddedilen bir üretimin ajan çağrısı ZATEN yapılmıştır ve
    para harcanmıştır. Bu alan o maliyeti taşır ki çağıran, toplam harcamayı
    yalnızca başarılı varyantlar üzerinden sayıp olduğundan düşük raporlamasın.
    """

    def __init__(self, mesaj: str, maliyet_usd: float | None = None):
        super().__init__(mesaj)
        self.maliyet_usd = maliyet_usd


def ajan_cagir(persona: str, gorev_metni: str, json_semasi: dict,
                zaman_asimi_sn: int = 120) -> dict:
    """
    Claude Code CLI'yi headless modda çağırır, yapılandırılmış JSON döner.

    persona: sistem promptu (--system-prompt) — ajanın kim olduğunu, neyi
             yapıp neyi yapamayacağını tanımlar. Çağrılar arasında SABİT
             tutulmalı (önbellek verimliliği için).
    gorev_metni: kullanıcı promptu (stdin) — görev-özel veri.
    json_semasi: beklenen çıktının JSON Schema'sı (--json-schema).

    Dönüş: {"veri": <şemaya uyan dict>, "maliyet_usd": float|None,
            "onbellek_okuma_tok": int|None, "onbellek_yazma_tok": int|None,
            "sure_ms": int|None}
    """
    komut = [
        "claude", "-p",
        "--system-prompt", persona,
        "--output-format", "json",
        "--json-schema", json.dumps(json_semasi),
    ]
    try:
        sonuc = subprocess.run(
            komut, input=gorev_metni, capture_output=True, text=True,
            timeout=zaman_asimi_sn,
        )
    except subprocess.TimeoutExpired as e:
        raise AjanCagriHatasi(
            f"claude CLI zaman aşımına uğradı ({zaman_asimi_sn}s)"
        ) from e
    except FileNotFoundError as e:
        raise AjanCagriHatasi(
            "claude komutu bulunamadı — Claude Code CLI kurulu mu, PATH'te mi?"
        ) from e

    if sonuc.returncode != 0:
        raise AjanCagriHatasi(f"claude CLI hata döndü: {sonuc.stderr.strip()}")

    try:
        zarf = json.loads(sonuc.stdout)
    except json.JSONDecodeError as e:
        raise AjanCagriHatasi(
            f"claude CLI çıktısı JSON değil: {sonuc.stdout[:300]!r}"
        ) from e

    if zarf.get("is_error"):
        raise AjanCagriHatasi(f"claude CLI is_error=true: {zarf.get('result')}")

    yapilandirilmis = zarf.get("structured_output")
    if yapilandirilmis is None:
        raise AjanCagriHatasi(
            f"structured_output alanı yok (şema zorlaması başarısız olmuş "
            f"olabilir): {str(zarf.get('result'))[:300]!r}"
        )

    kullanim = zarf.get("usage", {}) or {}
    return {
        "veri": yapilandirilmis,
        "maliyet_usd": zarf.get("total_cost_usd"),
        "onbellek_okuma_tok": kullanim.get("cache_read_input_tokens"),
        "onbellek_yazma_tok": kullanim.get("cache_creation_input_tokens"),
        "sure_ms": zarf.get("duration_ms"),
    }
