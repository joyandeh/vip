FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir \
    -i https://mirror-pypi.runflare.com/simple/ \
    --trusted-host mirror-pypi.runflare.com \
    -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "vip_crypto.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
