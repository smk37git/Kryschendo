# ---- Stage 1: Builder ----
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: Runtime ----
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /install /usr/local
COPY . .

# Collect static files at build time (no database needed for this)
RUN SECRET_KEY=build-placeholder python manage.py collectstatic --noinput

# Writable tmp dir for gunicorn worker heartbeat files
RUN mkdir -p /tmp/gunicorn && chown app:app /tmp/gunicorn
ENV TMPDIR=/tmp/gunicorn

# Cloud Run sets PORT env var; default to 8080
ENV PORT=8080
USER app

# Run migrations and load data at startup, then start gunicorn.
# This ensures Cloud SQL is reachable (not available at build time).
CMD python manage.py migrate --noinput && \
    python manage.py load_testimonials && \
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:$PORT \
        --workers 2 \
        --threads 4 \
        --timeout 120
