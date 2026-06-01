# syntax=docker/dockerfile:1

FROM python:3.13-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip --no-cache-dir \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt


FROM python:3.13-slim AS runtime

LABEL org.opencontainers.image.authors="Jackowski Maciej" \
      org.opencontainers.image.title="weather-app" \
      org.opencontainers.image.version="1.0.0"

ENV PORT=8080
ENV PYTHONUNBUFFERED=1

RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

COPY --from=builder /app/venv /app/venv
COPY app.py .
COPY templates/ templates/

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["/app/venv/bin/gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "app:app"]
