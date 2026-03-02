# STEP 01 — Monorepo Bootstrap

## Objective

Initialize the monorepo structure aligned with:

- The layered architecture (Domain / Application / Infrastructure / Interfaces)
- Multi-tenancy and security invariants
- Prompt Governance Convention

This step focuses on **structure only**, not business logic.

---

## ADR-002 Bootstrap Exception (SQLite Scope)

For STEP-01 only, SQLite is allowed exclusively for local bootstrap and
lightweight local checks.

Constraints:

- PostgreSQL remains the only production database engine.
- Production settings must target PostgreSQL.
- No production deployment may rely on SQLite.
- No engine-specific logic may be introduced outside infrastructure.

---

## Related ADRs

This step MUST respect:

- ADR-001 — Multi-Tenancy Isolation Strategy
- ADR-002 — Database Engine Strategy
- ADR-009 — Horizontal Scaling & Load Balancing Strategy

And is preparatory for:

- ADR-006 — Background Job Processing Strategy
- ADR-011 — Event-Driven Architecture Strategy
- ADR-012 — Distributed Tracing Strategy
- ADR-014 — Advanced Secret Management Strategy

---

## Related Governance

This step MUST comply with:

- `PROMPT-GOVERNANCE-CONVENTION.md`

In particular:

- Prompts must explicitly list related ADRs.
- Authority follows the documented hierarchy: ADR > Definition of Done > Prompt Governance Convention > Operations > Architecture > Operational prompts > Snapshots.
- No cross-layer shortcuts.
- No secrets hardcoded.

---

## Target Monorepo Structure (High-Level)

At the end of this step, the repository MUST have at least:

```text
root/
│
├── backend/
│   ├── domain/
│   │   └── __init__.py
│   ├── application/
│   │   └── __init__.py
│   ├── infrastructure/
│   │   └── __init__.py
│   ├── interfaces/
│   │   └── __init__.py
│   ├── settings/
│   │   └── __init__.py
│   ├── manage.py
│   └── <django_project_root>/
│       └── __init__.py
│
├── frontend/
│   ├── web/
│   └── mobile/
│
├── packages/
│   ├── shared_kernel/
│   ├── event_bus/
│   └── utilities/
│
└── docs/
    ├── adr/
    ├── architecture/
    ├── operations/
    └── prompts/

---

## Definition of Done — STEP-01 (Monorepo Bootstrap)

STEP-01 is considered complete when ALL the following conditions are met.

This STEP is responsible for establishing the repository structure,
backend project bootstrap, and architectural layering discipline.

It builds on STEP-00 (environment baseline).

---

### 1. Repository Structure

The monorepo MUST contain the following top-level structure:

- backend/
- frontend/web/ (may be empty scaffold)
- frontend/mobile/ (may be empty scaffold)
- packages/
- docs/

The backend directory MUST contain a valid Django project root.

---

### 2. Django Project Bootstrap

Inside `backend/`:

- A Django project has been created.
- `manage.py` exists.
- `backend_core/` (or equivalent project module) exists.
- `settings/` package structure is defined (base.py, dev.py, prod.py or equivalent separation).
- `urls.py`, `asgi.py`, and `wsgi.py` exist.

The Django project MUST start successfully with:

    python backend/manage.py check

No critical errors are allowed.

Warnings may be accepted only if documented.

---

### 3. Architectural Layering

The backend MUST define explicit layered separation:

- domain/
- application/
- infrastructure/
- interfaces/

The following invariants MUST hold:

- Domain layer MUST NOT import Django or infrastructure.
- Application layer MUST NOT depend on presentation.
- Interfaces layer MUST NOT contain business logic.
- No circular dependencies between layers.

Violation of layering rules is a P1 issue.

---

### 4. Multi-Tenancy Alignment (ADR-001)

Even if no tenant logic is implemented yet:

- The structure MUST anticipate tenant isolation.
- No global state related to tenant context may be introduced.
- No cross-tenant assumptions may be hardcoded.

Tenant context implementation may come later,
but structural violations are not allowed.

---

### 5. Database Strategy Alignment (ADR-002)

- PostgreSQL MUST be the declared production target engine.
- SQLite MAY be used for bootstrap/development only if explicitly documented.
- No raw database engine assumptions may leak into domain logic.
- Migrations framework MUST be initialized and functional.

The database configuration MUST NOT:

- Hardcode production credentials.
- Contain secrets in source code.

---

### 6. Security & Secrets (ADR-014)

- No SECRET_KEY hardcoded in production settings.
- Production configuration MUST require environment variables (fail-fast).
- No secrets committed to the repository.
- .env files MUST be ignored by Git.

---

### 7. Statelessness & Scaling Discipline (ADR-009)

- No server-side session state introduced.
- No in-memory business state.
- No file-based persistent state.
- No local caching logic violating distributed scaling assumptions.

The backend must remain horizontally scalable by design.

---

### 8. Static Analysis & Linting Validation

With the virtualenv active, the following commands MUST execute successfully:

    python -m mypy backend
    python -m flake8 backend

New errors introduced in this STEP are P1 issues.

Tooling warnings must be justified or resolved.

---

### 9. Django Validation

The following command MUST succeed:

    python backend/manage.py check

Optional (recommended):

    python backend/manage.py make migrations --check

No unapplied migration inconsistencies should exist.

---

### 10. Governance Compliance

STEP-01 MUST NOT:

- Modify existing ADR documents without creating a new ADR.
- Introduce shortcuts across architectural layers.
- Bypass Prompt Governance Convention.
- Introduce production infrastructure configuration.

Any structural decision beyond bootstrap requires an ADR.

---

### 11. Documentation Alignment

The following documents MUST remain consistent:

- docs/operations/step-01/STEP-01-monorepo-bootstrap.md
- Architecture overview
- ADR-001 through ADR-014 (where applicable)

If deviations occur, documentation must be updated within this STEP.

---

### 12. Explicit Exclusions

The following are NOT required for STEP-01:

- Feature implementation
- Business logic implementation
- Authentication endpoints
- Authorization logic
- Background jobs
- Caching configuration
- Rate limiting logic
- Production CI/CD setup

Those belong to later STEPs.

---

### 13. Final Acceptance Condition

STEP-01 is officially marked DONE when:

- The monorepo structure exists and is coherent.
- The Django backend boots successfully.
- Layered architecture is enforced structurally.
- Static analysis passes without new errors.
- No P1 architectural violations remain open.
- No ADR violations are detected.

At this point, the repository is structurally ready for:

STEP-02 — Infrastructure Baseline or Core Feature Implementation.