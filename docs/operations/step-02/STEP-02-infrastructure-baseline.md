# STEP-02 — Infrastructure Baseline (Backend Runtime & Settings)

## 1. Purpose

This STEP establishes the **minimum backend runtime infrastructure** required to run the system in a consistent, secure, and testable way, without introducing any business logic.

Goals:

- Create a robust Django backend runtime baseline.
- Configure environment-specific settings (dev/prod) aligned with ADRs.
- Prepare database connectivity (PostgreSQL in prod, SQLite allowed only for local/dev where documented).
- Set up minimal logging and health checking.
- Ensure the backend can run locally and is ready for future CI integration.

No business features (domains, use cases) are introduced in this STEP.

---

## 2. Scope

### 2.1 In Scope

- Backend infrastructure only, specifically under:

  - `backend/`
  - `backend/backend_core/` (or equivalent Django project root)
  - `backend/backend_core/settings/`
  - `backend/backend_core/urls.py`
  - `backend/backend_core/asgi.py`
  - `backend/backend_core/wsgi.py`
  - `manage.py`

- Environment-specific settings:

  - `base.py`
  - `dev.py`
  - `prod.py`

- Database configuration:

  - PostgreSQL for production (ADR-002)
  - SQLite only for local development if explicitly documented

- Minimal health-check endpoint (e.g., `/health/`), without business logic.

- Minimal logging configuration (backend side) consistent with ADRs.

### 2.2 Out of Scope

- Frontend (web/mobile).
- Business/domain models and application services.
- Multi-tenant domain logic (handled in STEP-04).
- Authentication features (handled in STEP-03).
- CI/CD pipelines (handled in a further STEP).
- Observability stack (beyond minimal logging and health check; full stack in STEP-07).

---

## 3. Architectural Context

This STEP must comply with:

- ADR-001 — Multi-Tenancy Isolation Strategy  
  (Design must not violate future tenant isolation; no global tenant state introduced.)

- ADR-002 — Database Engine Strategy  
  (PostgreSQL as primary production engine; SQLite only as documented bootstrap exception.)

- ADR-003 — JWT Signing & Key Rotation Strategy  
  (Even if auth is not implemented yet, settings must not conflict with JWT usage later.)

- ADR-014 — Advanced Secret Management Strategy  
  (SECRET_KEY and other secrets from environment, no hardcoded secrets.)

- ADR-015 — Error & Exception Handling Strategy  
  (Global error handler will come later, but no behavior should conflict with the error contract.)

- ADR-016 — Testing Strategy & Test Pyramid  
  (Settings and database configuration must be test-friendly.)

- ADR-017 — Dependency & Package Management Strategy  
  (Dependencies pinned and minimal; no unnecessary libraries introduced.)

- ADR-018 — Migration & Schema Evolution Policy  
  (Database configuration must be compatible with forward-only migrations.)

- ADR-019 — Observability & Logging Contract  
  (Logging configuration must be ready to emit structured logs later.)

- ADR-020 — Code Style & Formatting Governance  
  (Respect black/flake8/mypy decisions already in place.)

---

## 4. Execution Requirements

### 4.1 Planner Agent Responsibilities

The Planner Agent MUST:

1. Analyze the current backend structure created in STEP-01.
2. Identify what is already present in:
   - `backend/backend_core/settings/`
   - `backend/backend_core/urls.py`
   - `backend/backend_core/asgi.py`
   - `backend/backend_core/wsgi.py`
   - `manage.py`
3. Define a plan to:
   - Ensure a clean separation of settings: `base.py`, `dev.py`, `prod.py`.
   - Configure PostgreSQL for production, SQLite only for dev/local when acceptable.
   - Introduce environment variables usage for:
     - `SECRET_KEY`
     - Database connection for production
   - Add a minimal `/health/` endpoint under `interfaces`/`api` layer, without business logic.
   - Ensure logging configuration is present in `base.py` or a dedicated logging settings module, compatible with ADR-019.
4. Explicitly reference:
   - How this STEP prepares for STEP-03 (Authentication Skeleton).
   - How this STEP avoids violating multi-tenancy (ADR-001) and testing requirements (ADR-016).
5. Produce a step-by-step plan that the Implementer can follow without refactoring other layers (domain/application).

The Planner MUST NOT:

- Introduce domain models.
- Introduce authentication logic.
- Change repository structure in ways that conflict with STEP-01.

---

### 4.2 Implementer Agent Responsibilities

The Implementer Agent (or the human developer) MUST:

- Apply the plan while respecting:
  - Layered architecture:
    - No business logic in settings or health check.
  - Separation of environments:
    - `dev.py` for local development.
    - `prod.py` for production, with fail-fast if env vars are missing.
- Ensure that:
  - No secrets are hardcoded.
  - Environment variables are used for production DB and SECRET_KEY.
- Implement a minimal health check endpoint in the interfaces layer, e.g.:

  - `/health/` returning a simple JSON such as `{ "status": "ok" }`.
  - No dependency on database or external services (pure process-liveness check).

- Ensure that all changes respect ADRs and facilitate future STEPs (STEP-03, STEP-04, STEP-06).

The Implementer MUST NOT:

- Add any domain-specific endpoints.
- Tie the health check to tenant context.
- Implement authentication or authorization in this STEP.

---

### 4.3 Reviewer Agent Responsibilities

The Reviewer Agent MUST:

- Verify compliance with:
  - This STEP definition.
  - All related ADRs (001, 002, 014, 016, 017, 018, 019, 020).
- Confirm that:
  - Settings are split and correctly wired:
    - `DJANGO_SETTINGS_MODULE` points to `backend_core.settings.dev` or `prod` as appropriate.
  - Production config:
    - Uses PostgreSQL only.
    - SECRET_KEY comes from env with fail-fast behavior.
  - Development config:
    - May use SQLite for convenience, if explicitly documented as a non-production-only behavior.
  - No secrets are logged or hardcoded.
  - Logging is at least minimally configured and does not contradict ADR-019.
  - A `/health/` endpoint exists and:
    - Lives in the appropriate interfaces/API layer.
    - Does not contain business logic.
- Verify that:
  - No domain/application/infrastructure logic has been introduced beyond minimal infrastructure wiring.
  - Layering invariants from the snapshot are preserved.

If any violation is detected (e.g., hardcoded secrets, production using SQLite, health check in the wrong layer), STEP-02 MUST be rejected.

---

## 5. Concrete Work Items (Checklist)

This checklist is a guide for Planner/Implementer/Reviewer.

### 5.1 Settings

- [ ] Ensure `backend/backend_core/settings/base.py` exists and contains:
  - [ ] Core Django settings (INSTALLED_APPS, MIDDLEWARE, TEMPLATES, etc.).
  - [ ] Logging configuration scaffold (even if minimal).
- [ ] Ensure `backend/backend_core/settings/dev.py`:
  - [ ] Imports from `base.py`.
  - [ ] Uses SQLite or a simple DB suitable for local dev.
  - [ ] Handles SECRET_KEY safely (runtime-generated or from env, but never static hardcoded).
- [ ] Ensure `backend/backend_core/settings/prod.py`:
  - [ ] Imports from `base.py`.
  - [ ] Uses PostgreSQL via env-based configuration.
  - [ ] Fails fast if REQUIRED env vars are missing (SECRET_KEY, DB connection params).
  - [ ] Disables debug and other dev-only behaviors.

### 5.2 Environment Integration

- [ ] Provide documentation (in `docs/` or in this STEP) on:
  - [ ] How to set `DJANGO_SETTINGS_MODULE` for dev and prod.
  - [ ] Which env variables are required in prod.
  - [ ] Example `.env.example` file (may be postponed to a later STEP if already planned).

### 5.3 Health Check Endpoint

- [ ] Add a minimal `/health/` endpoint:
  - [ ] Implemented in interfaces layer (`interfaces/api` or similar).
  - [ ] Registered in `backend_core/urls.py` under a path like `/health/`.
  - [ ] Returns static JSON and HTTP 200 if the process is up.
  - [ ] Contains no domain logic, no DB access, no tenant access.

### 5.4 Logging

- [ ] Ensure logging configuration in settings:
  - [ ] No secrets logged.
  - [ ] Error-level logs are enabled.
  - [ ] Structure ready to evolve into JSON/structured logging later (ADR-019).

---

## 6. Validation & Testing

The system SHOULD be validated as follows:

### 6.1 Local Run

- [ ] With dev settings:
  - [ ] Run `python manage.py runserver` using dev settings.
  - [ ] Call `/health/` and verify response `{"status": "ok"}` (or equivalent).
  - [ ] Check logs to ensure no secrets or sensitive data are printed.

### 6.2 Basic Migrations

- [ ] Run `python manage.py migrate` using dev settings to ensure DB wiring works.

### 6.3 Static Checks

- [ ] Ensure `mypy` and `flake8` still pass after changes.
- [ ] No new violations introduced by STEP-02.

---

## 7. Definition of Done — STEP-02

STEP-02 is complete only when ALL the following conditions are satisfied:

1. **Settings & Environments**
   - [ ] `base.py`, `dev.py`, `prod.py` exist and are wired correctly.
   - [ ] Production configuration uses PostgreSQL and env-based secrets ONLY.
   - [ ] Development configuration may use SQLite, documented as local/non-prod-only.

2. **Secrets & Security**
   - [ ] No hardcoded SECRET_KEY exists anywhere in settings.
   - [ ] Production fails fast if SECRET_KEY or DB env vars are missing.
   - [ ] No secrets are written to logs.

3. **Health Check**
   - [ ] `/health/` endpoint exists in interfaces layer.
   - [ ] It is reachable and returns a simple JSON indicating the app is up.
   - [ ] It does not depend on DB/tenants/auth.

4. **Logging**
   - [ ] Logging is configured at least to a minimal, consistent baseline.
   - [ ] No contradictions with ADR-019 (e.g., no sensitive info logged).

5. **Layering & ADR Compliance**
   - [ ] No domain/application logic added in this STEP.
   - [ ] All changes align with ADR-001, 002, 014, 016, 017, 018, 019, 020.
   - [ ] `mypy` and `flake8` pass without new violations introduced by STEP-02.

6. **Scope Integrity**
   - [ ] Only infrastructure and settings were touched.
   - [ ] No business features were introduced.
   - [ ] No structural decisions contradict existing ADRs.

Only when all items above are verified by the Reviewer, STEP-02 can be considered DONE.