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

# Build static files and bake SQLite database into image
# Omit DATABASE_URL so settings.py default (BASE_DIR / db.sqlite3) is used
RUN SECRET_KEY=build-placeholder python manage.py collectstatic --noinput && \
    SECRET_KEY=build-placeholder python manage.py migrate --run-syncdb && \
    SECRET_KEY=build-placeholder python manage.py load_testimonials

# Make db writable by app user (for admin session writes, etc.)
RUN chown app:app /app/db.sqlite3

# Cloud Run sets PORT env var; default to 8080
ENV PORT=8080
USER app

CMD exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 120
