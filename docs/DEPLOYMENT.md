# Deployment Checklist — Bills24

This file lists steps and commands to deploy Bills24 to production using Docker or Heroku.

## Required environment variables

- `SECRET_KEY` — strong Django secret
- `PROJECT_ENVIRONMENT` — production
- `DEBUG` — False
- `ALLOWED_HOSTS` — comma-separated hosts
- `DATABASE_URL` or `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `AUTHENTICATION_KEY` — JWT signing key
- `NEXT_ROUTE` — allowed CORS origin
- Optional: `SENTRY_DSN`, `DJANGO_SUPERUSER_*`

## Docker (recommended)

1. Build image:

```bash
docker build -t bills24:latest .
```

2. Run as container (production-like):

```bash
docker run --env-file .env -p 8000:8000 bills24:latest
```

3. Use orchestration (Docker Compose, Kubernetes) and connect to managed Postgres.

## Heroku (quick)

1. Create app and provision Postgres addon.
2. Set env vars in Heroku config.
3. Push code to Heroku (Procfile is present):

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
```

## Common deployment steps

- Migrate database: `python manage.py migrate --noinput`
- Collect static: `python manage.py collectstatic --noinput`
- Create superuser (if needed): set `DJANGO_SUPERUSER_*` env vars and let entrypoint create it or run `createsuperuser` interactively.

## Security & Hardening

- Ensure `DEBUG=False` and `ALLOWED_HOSTS` set.
- Use HTTPS and set `SECURE_PROXY_SSL_HEADER`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and `SECURE_HSTS_SECONDS`.
- Rotate `SECRET_KEY` and other credentials regularly.

## Rollback & Backups

- Ensure automated DB backups (managed DB provider).
- Tag releases and use image tags for deploy/rollback.

---

Follow `ARCHITECTURE.md` and `IMPLEMENTATION_PLAN.md` for broader context.
