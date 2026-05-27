# Bills24 — Implementation Plan (Start Fresh)

This plan describes how to start the Bills24 project from scratch, from local setup through CI and production deployment. Follow the numbered phases in order; each phase has commands and verification steps.

## High-level Steps

1. Prepare environment and repo
2. Install dependencies and pin versions
3. Add Docker and local development services
4. Configure database & secrets
5. Implement core features (MVP)
6. Add tests, linting, and CI
7. Prepare production deployment
8. Observability, security hardening, and launch

## Phase 0 — Preconditions

- Host/source: Git repository (GitHub recommended).
- Local tools: Git, Docker & Docker Compose, Python 3.10+ (or project's requirement), pip, virtualenv.
- Cloud target: Heroku/GCP/AWS/Render/Platform.sh or container registry + Kubernetes.

## Phase 1 — Repository & Branching

- Initialize a new repo (or use existing). Create main branches: `main`, `develop`.
- Add `.gitignore`, `LICENSE`, `README.md`.
- Add `ARCHITECTURE.md` and this `IMPLEMENTATION_PLAN.md` to repo.

Commands

```bash
git init
git remote add origin <remote-url>
git checkout -b develop
```

## Phase 2 — Python Environment & Dependencies

- Create virtualenv and install pinned dependencies in `requirements.txt`.
- Recommended core requirements: `Django`, `djangorestframework`, `gunicorn`, `psycopg2-binary`, `python-dotenv`, `whitenoise`, `django-environ` (or `dj-database-url`).
- Create a `requirements.txt` and `requirements-dev.txt` (pytest, black, isort, flake8).

Commands

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Phase 3 — Project Scaffolding

- Create Django project skeleton (or reuse current structure): `manage.py`, project package (here `backend/`).
- Create apps: `accounts`, `Bill` under `apps/`.
- Configure `settings/` split: `base.py`, `development.py`, `production.py`.
- Set up `templates/`, `static/`, `media/` folders.

Key files to add/verify

- `settings/base.py` — core settings
- `settings/development.py` — local DB (sqlite), debug True
- `settings/production.py` — read env vars, secure flags

## Phase 4 — Database & Migrations

- Local dev: SQLite is fine.
- Production: provision PostgreSQL; use `DATABASE_URL` env var.
- Create initial migrations and apply locally.

Commands

```bash
python manage.py makemigrations
python manage.py migrate
```

Verification

- Run `python manage.py runserver` and visit `http://127.0.0.1:8000/`.

## Phase 5 — Docker (local parity)

- Create `Dockerfile` for app and `docker-compose.yml` with services:
  - `web` (Django/Gunicorn)
  - `db` (Postgres)
  - `redis` (optional for caching/email tasks)

Minimal `docker-compose.yml` example (excerpt)

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: bills24
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - db-data:/var/lib/postgresql/data
  web:
    build: .
    command: gunicorn backend.wsgi:application --bind 0.0.0.0:8000
    ports:
      - '8000:8000'
    env_file: .env
    depends_on:
      - db
volumes:
  db-data:
```

## Phase 6 — Implement MVP Features

Core features and file locations (suggested):

- Authentication: `apps/accounts/` (models, forms, API views, serializers)
- Billing models & logic: `apps/Bill/models.py`, `apps/Bill/api/` (serializers, views)
- Email templates: `templates/emails/` (welcome, password reset, billing notifications)
- API endpoints: project `api/` and app `api/` modules
- Frontend templates for simple UI in `templates/`

MVP user stories

- Users can sign up, log in, reset password
- Users can create/read/update/delete bills
- System sends email notifications for new bills

## Phase 7 — Tests, Linting, Formatting

- Add `pytest` with `pytest-django` or use Django's `manage.py test`.
- Add `flake8`, `black`, `isort`, and pre-commit hooks.

Commands

```bash
pip install -r requirements-dev.txt
pytest
black .
flake8
```

## Phase 8 — Continuous Integration

- Add GitHub Actions workflow to run tests, linters, and build Docker image on PRs to `develop`.
- Example checks: `python -m pip install -r requirements-dev.txt`, run `pytest`, `flake8`, `black --check`.

## Phase 9 — Secrets & Configuration

- Use `.env` (local) and real env vars in CI/production.
- Required env vars: `SECRET_KEY`, `DATABASE_URL`, `EMAIL_HOST`, `EMAIL_USER`, `EMAIL_PASSWORD`, `ALLOWED_HOSTS`.
- Add `.env.example` to repo documenting required vars.

## Phase 10 — Production Deployment

- Choose platform (Heroku/Render/Azure/GCP/AWS).
- Build process: container image + managed Postgres + SECRET config.
- Configure static files (WhiteNoise or external CDN) and media storage (S3).
- Run migrations on deploy and ensure workers (Celery) if background tasks needed.

Commands (Heroku example)

```bash
heroku create bills24-app
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY='<value>'
git push heroku main
heroku run python manage.py migrate
```

## Phase 11 — Observability and Security

- Add Sentry DSN for error tracking.
- Enable HTTPS, HSTS, secure cookies, and Content Security Policy.
- Review dependencies for vulnerabilities.

## Phase 12 — Post-launch

- Monitor errors and performance, iterate on features from backlog.
- Add automated backups for database.

## Project Milestones (Suggested)

- Milestone 1 (Week 1): Repo setup, environment, Docker, base settings, migrations
- Milestone 2 (Week 2): Auth, basic Bill models, CRUD endpoints, templates
- Milestone 3 (Week 3): Email notifications, tests, CI
- Milestone 4 (Week 4): Production deployment, monitoring, security hardening

## Backlog / Nice-to-have

- Celery + Redis for background tasks
- Admin UX improvements and audit logs
- Role-based access control
- Rate limiting and API throttling

---

If you want, I can now:

- Add `docker-compose.yml` and a `Dockerfile` to this repo.
- Add a sample GitHub Actions workflow file in `.github/workflows/ci.yml`.
- Create `.env.example` and `requirements-dev.txt`.

Created: IMPLEMENTATION_PLAN.md
