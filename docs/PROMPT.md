# Prompts for Building Bills24

This file contains staged prompt templates you can use to instruct the assistant to build the project from scratch. Replace placeholders like `<project-name>`, `<hosting>`, `<field:type>`, `<email-provider>`, and `<remote-url>` before using.

---

## 1. Project brief
Use case: Give the assistant the overall goal and constraints.

Prompt:

```
I want to build a Django project named Bills24: user auth, CRUD for bills, email notifications, REST API, PostgreSQL in production, Docker deployments to <hosting>. Budget: MVP in 2 weeks. List the high-level architecture, milestones, and required files.
```

---

## 2. Repository & branch strategy
Use case: Seed repo layout and branch plan.

Prompt:

```
Initialize a Git repo for Bills24 with branches 'main' and 'develop', .gitignore, LICENSE, README, and a suggested directory structure (manage.py, backend/, apps/, api/, templates/, public/). Show exact files to create.
```

---

## 3. Environment & dependencies
Use case: Pick Python/Django versions and pin packages.

Prompt:

```
Create a requirements.txt and requirements-dev.txt for Django 4.x, djangorestframework, drf-spectacular, gunicorn, psycopg2-binary, whitenoise, django-environ, pytest, black, flake8. Explain why each is included and provide pinned versions.
```

---

## 4. Django scaffold
Use case: Create project and core settings split.

Prompt:

```
Scaffold a Django project named 'backend' with settings split into base, development, production. Show the content for `backend/settings/base.py`, `development.py`, and `production.py` using environment variables for secrets.
```

---

## 5. App skeletons
Use case: Create app boilerplate for `accounts` and `Bill`.

Prompt:

```
Create two apps under `apps/`: `accounts` and `Bill`. For each add `models.py`, `views.py`, `api/serializers.py`, `api/urls.py`, `tests.py`, and admin registration. Provide minimal code examples and URL includes.
```

---

## 6. User model & auth
Use case: Implement custom user and JWT auth.

Prompt:

```
Implement a Django custom user model (email as username) in `apps/accounts/models.py`. Add registration/login endpoints using djoser + simplejwt. Provide serializers and example requests.
```

---

## 7. Billing models & APIs
Use case: Define domain models and REST endpoints.

Prompt:

```
Design `Bill` model with fields: user(FK), title(str), amount(decimal), due_date(date), paid(bool). Create serializers, viewsets, and router entries to support list/create/retrieve/update/delete with permissions so only owner can modify.
```

---

## 8. Migrations & DB
Use case: Create migrations and local/production DB config.

Prompt:

```
Add migration steps and show `DATABASES` config for development (sqlite) and production (Postgres via DATABASE_URL). Provide commands to run migrations locally and in Docker.
```

---

## 9. Email templates & sending
Use case: Transactional emails (welcome, reset, billing).

Prompt:

```
Add email templates under `templates/emails/` for welcome and bill notification. Configure Django SMTP settings using env vars and example send function to queue/send emails.
```

---

## 10. Frontend templates (optional)
Use case: Add simple server-rendered pages.

Prompt:

```
Create basic templates: `base.html`, `bills/list.html`, `accounts/login.html`. Provide minimal views and URL entries to render them.
```

---

## 11. Testing
Use case: Add unit and API tests + test runner config.

Prompt:

```
Create pytest tests for user registration, bill CRUD, and email sending. Add `pytest.ini` and sample test cases demonstrating DB fixtures and API client usage.
```

---

## 12. CI pipeline
Use case: Set up GitHub Actions for lint/test/build.

Prompt:

```
Produce a `.github/workflows/ci.yml` that installs deps, runs `black --check`, `isort --check`, `flake8`, migrations, and `pytest`. Include matrix or caching recommendations.
```

---

## 13. Docker & local parity
Use case: Containerize app and compose for Postgres.

Prompt:

```
Create a multi-stage `Dockerfile`, `docker-compose.yml` with services `web` and `db` (postgres), and an `entrypoint.sh` that waits for DB, migrates, and collects static. Include `.dockerignore`.
```

---

## 14. Deployment config
Use case: Produce Procfile / k8s or hosting-specific steps.

Prompt:

```
Provide deployment steps for Heroku and a container registry (Docker Hub / GCR). Add a `Procfile` and example Kubernetes deployment manifest for a minimal rollout (Deployment + Service + Secret).
```

---

## 15. Observability & security
Use case: Add Sentry, logging, and security best practices.

Prompt:

```
Add Sentry integration, structured logging (JSON console), and production security settings (HSTS, secure cookies, SSL redirect). Provide required env vars and example config in `production.py`.
```

---

## 16. Docs & README
Use case: Generate project docs and developer onboarding.

Prompt:

```
Produce a README with quickstart (Docker + local), contributor guide, and links to `ARCHITECTURE.md`, `IMPLEMENTATION_PLAN.md`, and `DEPLOYMENT.md`. Generate `ARCHITECTURE.md` and `IMPLEMENTATION_PLAN.md` if missing.
```

---

## 17. Code review / PR automation
Use case: Add pre-commit and PR checklist.

Prompt:

```
Add a `.pre-commit-config.yaml` that runs black, isort, flake8. Provide a PR checklist for testing, security, and docs required before merge.
```

---

## 18. Iterative feature prompts (examples)
Use case: When building features incrementally.

Example - Add endpoint:

```
Add an endpoint to mark a bill as paid: POST /api/bills/<id>/pay/ that sets `paid=True` and sends a confirmation email. Provide serializer, view, url, and tests.
```

Example - Refactor:

```
Refactor `apps/Bill/views.py` to remove duplicated query logic and add a service layer `apps/Bill/services.py`. Show before/after code and tests.
```

---

## 19. Troubleshooting
Use case: Debugging errors or failing tests.

Prompt:

```
I ran `pytest` and got this error: <paste trace>. Inspect the related files (`apps/Bill/models.py`, `apps/Bill/serializers.py`) and propose a fix with a minimal patch.
```

---

## 20. Release & maintenance
Use case: Prepare release notes and changelog.

Prompt:

```
Draft release notes for v0.1.0 summarizing features, migrations, and breaking changes. Provide `CHANGELOG.md` entry and git tag command.
```

---

## 21. Automation meta-prompt
Use case: Continue building with ordered steps.

Prompt:

```
Continue the implementation: create file X, then run tests, then open a PR. Provide each step and stop after running tests so I can review.
```

---

If you want, I can now run any of these prompts to scaffold files in the repo. Which prompt should I execute first?