# TR-CodeEval güvenli çalıştırma ortamı (sandbox temel imajı).
# Amaç: model tarafından üretilen kodu ana sisteme zarar vermeden,
# root olmayan bir kullanıcı olarak, izole biçimde çalıştırmak.
FROM python:3.11-slim

# Root olmayan kullanıcı: container içinde ayrıcalıksız çalışırız.
RUN useradd -m -u 1000 sandbox

WORKDIR /work
USER sandbox

# Varsayılan komut host tarafından ('python /work/harness.py') ezilir.
CMD ["python", "/work/harness.py"]
