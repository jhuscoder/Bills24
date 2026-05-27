#!/usr/bin/env bash
set -e

# Wait for database to be ready (simple loop)
if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database to be ready..."
  # try connecting via psql if available, otherwise just sleep a bit
  COUNT=0
  until python - <<PY
import sys
import os
import django
from urllib.parse import urlparse
try:
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        sys.exit(0)
    # simple check: try opening a socket to host:port
    url = urlparse(db_url)
    host, port = url.hostname, url.port or 5432
    import socket
    s = socket.socket()
    s.settimeout(1)
    s.connect((host, port))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
  do_sleep=$?
  if [ $do_sleep -ne 0 ]; then
    COUNT=$((COUNT+1))
    if [ $COUNT -gt 30 ]; then
      echo "Database did not become available in time" >&2
      exit 1
    fi
    sleep 1
  else
    break
  fi
  done
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser if environment variables are set (optional)
if [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --noinput || true
fi

exec "$@"
