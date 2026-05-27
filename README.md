# Bills24

A Django-based billing and payments application.

## Overview

Bills24 is a monolithic Django application that provides user authentication, bill management, and email notifications. The repository contains app modules under `apps/`, a project backend under `backend/`, and API helpers in `api/`.

## Quick Start (Docker)

1. Copy the example environment file and edit values:

```bash
cp .env.example .env
# Edit .env to set SECRET_KEY and production-ready values
```

2. Start services with Docker Compose:

```bash
docker-compose up --build
```

3. Visit the app at http://localhost:8000

## Quick Start (Local - no Docker)

```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt -r requirements-extras.txt -r requirements-dev.txt
cp .env.example .env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

## Tests & Linters

Install dev requirements and run tests:

```bash
pip install -r requirements-dev.txt
pytest
black .
flake8
```

## Documentation

- Architecture overview: [ARCHITECTURE.md](ARCHITECTURE.md)
- Implementation plan: [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)
- Deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

More docs in `docs/`.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions, environment variables, and Docker/Heroku examples.

## Contributing

- Create a feature branch off `develop`.
- Run tests and linters locally before opening a PR.

## License

See [LICENSE](LICENSE)

---

Created: `README.md`
