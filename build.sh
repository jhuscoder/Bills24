#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
python -m pip install --upgrade pip

pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files (requires WhiteNoise or similar)
python manage.py collectstatic --no-input

gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT