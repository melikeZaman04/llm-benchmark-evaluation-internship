# Güvenli Kod Çalıştırma Altyapısı (Sandbox)

İki-düzlemli mimaride **Deterministik Oracle**'ın çekirdeği. Model/aday
kodu, ana sisteme zarar veremeyecek şekilde izole bir Docker container'ında
çalıştırıp gizli testlere sokar.

## Kurulum (bir kez)

```bash
# 1) Docker daemon'ı başlat ve kullanıcıyı gruba ekle (sudo gerekir)
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
#    -> ardından oturumu/terminali yeniden başlat (grup üyeliği için)

# 2) Sandbox temel imajını derle
docker build -t trc-sandbox:latest src/sandbox
```

## Doğrulama (self-test)

```bash
python src/sandbox/executor.py
```

Beklenen: DOĞRU çözüm 5/5 test geçer (`"gecti": true`), HATALI çözüm bazı
testlerde `mantik` hatasıyla kalır (`"gecti": false`).

## Kullanım (koddan)

```python
from src.sandbox import sandboxta_calistir

sonuc = sandboxta_calistir(kod, "fonksiyon_adi", test_cases)
# -> {"gecti": bool, "hata_tipi": ..., "gecen": int, "toplam": int, "sonuclar": [...]}
```

## Güvenlik önlemleri
`--network none`, `--memory`/`--cpus`/`--pids-limit`, `--read-only`,
`--tmpfs /tmp`, `--user 1000:1000`, salt-okunur kod bağlama, duvar-saati
`timeout`. (İleri sertleştirme — gVisor/microVM — kapsam dışı.)
