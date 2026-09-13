FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev libjpeg-dev zlib1g-dev procps \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Fix logs permission (most important)
RUN mkdir -p /code/logs \
    && touch /code/logs/django_errors.log \
    && chmod -R 777 /code/logs     # Temporary broad permission for testing

EXPOSE 8000