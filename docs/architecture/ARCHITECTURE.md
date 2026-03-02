# ARCHITECTURE.md

---

## 1. Purpose and Scope

This document provides a high-level architectural overview of the system.

It defines:

* The monorepo structure
* The multi-tenant SaaS model
* The core technology stack
* The database abstraction strategy
* The authentication model
* The architectural constraints

This document does NOT override Architecture Decision Records (ADRs) or detailed architecture documents.

Reference hierarchy for this document:

1. `/docs/adr/*.md`
2. `/docs/governance/DEFINITION-OF-DONE-TEMPLATE.md`
3. `/docs/prompts/governance/PROMPT-GOVERNANCE-CONVENTION.md`
4. `/docs/operations/*.md`
5. `/docs/architecture/*.md`

In case of conflict, follow the hierarchy above; ADRs prevail.

---

## 2. System Overview

The system is a multi-tenant SaaS full-stack application implemented as a single monorepo.

Core characteristics:

* Multi-tenant by design
* Backend implemented in Python / Django
* Web frontend implemented in React (JavaScript)
* Mobile frontend implemented in React Native
* Backend-only reusable modules under `/packages`
* Database abstraction layer allowing DB engine substitution
* Authentication based on JWT + social authentication providers

At this stage, the architecture defines the platform structure and constraints.
Business capabilities and feature modules will be defined separately.

---

## 3. Architectural Style

The system follows a strict layered architecture with separation of concerns.

### 3.1 Core Layers

#### Domain Layer

* Business rules
* Core invariants
* Domain models
* Pure logic independent of frameworks

#### Application Layer

* Use cases
* Orchestration logic
* Coordination between domain and infrastructure

#### Infrastructure Layer

* Persistence implementations
* External APIs
* Framework integrations (e.g., Django ORM)
* Technical adapters

#### Presentation Layer

* HTTP controllers / API endpoints
* Web UI (React)
* Mobile UI (React Native)
* Transport-level logic only

Strict rules:

* No business logic in Presentation.
* No direct database access from Presentation.
* No infrastructure leakage into Domain.
* No circular dependencies.
* Dependency direction must always point inward.

---

## 4. Monorepo Structure

```
/
├── backend/              # Django backend
│   ├── domain/           # Business rules and core logic
│   ├── application/      # Use cases and orchestration
│   ├── infrastructure/   # Persistence and adapters
│   └── interfaces/       # API endpoints
├── frontend/
│   ├── web/              # React web application
│   └── mobile/           # React Native mobile application
├── packages/             # Backend-only reusable modules
├── docs/
│   ├── adr/              # Architecture Decision Records
│   ├── architecture/     # Detailed architectural specs
│   └── features/         # Feature specifications
├── .github/              # CI/CD, AI governance, workflows
└── ARCHITECTURE.md       # This document
```

### 4.1 Backend

`/backend` contains the Django project and follows layered boundaries internally:

* `domain/`
* `application/`
* `infrastructure/`
* `interfaces/` (API layer)

Exact structure is defined in:
`/docs/architecture/backend-structure.md`

---

### 4.2 Frontend — Web

`/frontend/web` contains the React web client:

* Presentational components
* Routing
* API communication layer
* Tenant-aware UI behavior

No business rules must reside here.

Architecture details:
`/docs/architecture/frontend-web.md`

---

### 4.3 Frontend — Mobile

`/frontend/mobile` contains the React Native mobile application:

* Mobile navigation
* UI components
* Shared API client logic when possible

Architecture details:
`/docs/architecture/frontend-mobile.md`

---

### 4.4 Packages (Backend Only)

`/packages` contains reusable backend modules.

Constraints:

* No UI code.
* No dependency on frontend.
* Avoid hard coupling to Django where possible.
* Must respect layered architecture.

Design guidelines:
`/docs/architecture/packages.md`

---

## 5. Multi-Tenancy Architecture

The system is multi-tenant by design.

### 5.1 Core Principles

* Each request must resolve a Tenant Context.
* Tenant resolution occurs at the system boundary.
* Tenant context must be explicitly propagated.
* No global mutable tenant state.

### 5.2 Tenant Isolation

Tenant isolation strategies may include:

* Database-per-tenant
* Schema-per-tenant
* Row-level isolation
* Hybrid strategies

The chosen strategy is defined in:

* `/docs/adr/ADR-001-multi-tenancy.md`
* `/docs/architecture/multi-tenancy.md`

The architecture must allow strategy evolution through ADR without structural rewrite.

---

## 6. Database Abstraction Strategy

The system is designed to be database-engine agnostic.

### 6.1 Abstraction Model

* Standard persistence interfaces defined in application/infrastructure layers.
* Database-specific implementations provided per engine.
* Selection determined by:

  * Deployment configuration
  * Tenant configuration (if applicable)

Domain and application layers must never depend on a specific DB engine.

---

### 6.2 Django Integration

* Django ORM may serve as default adapter.
* ORM usage must be encapsulated within infrastructure.
* Domain logic must remain ORM-agnostic.
* Repository pattern or equivalent abstraction must isolate persistence.

Details:
`/docs/architecture/database-abstraction.md`

---

## 7. Authentication and Authorization

Authentication is based on:

* JWT tokens
* Social authentication providers (OAuth-based)

### 7.1 JWT

* Tokens issued by backend.
* Tokens may include tenant identifier in claims.
* Stateless authentication model preferred.

### 7.2 Social Authentication

* Integrated via backend services.
* Must integrate cleanly with JWT issuance.
* Must respect tenant boundaries.

Details:
`/docs/architecture/authentication.md`

Authorization:

* Enforced in application/domain layers.
* Must not rely solely on frontend logic.

Details:
`/docs/architecture/authorization.md`

---

## 8. Cross-Cutting Concerns

Cross-cutting concerns include:

* Logging
* Observability
* Configuration management
* Error handling
* API versioning
* Feature flags

Defined in:

* `/docs/architecture/logging.md`
* `/docs/architecture/observability.md`
* `/docs/architecture/configurations.md`
* `/docs/architecture/api-versioning.md`

All cross-cutting concerns must respect layered architecture and multi-tenant constraints.

---

## 9. Performance and Scalability Principles

The system must:

* Avoid N+1 queries
* Avoid blocking operations in async contexts
* Support horizontal scaling
* Avoid global mutable state
* Support tenant-based scaling strategies

Performance-sensitive decisions must be documented via ADR.

---

## 10. Testing Philosophy

Testing aligns with layering:

* Domain → unit tests
* Application → integration tests
* Infrastructure → integration tests
* Presentation → API/UI tests

Tests validate behavior, not implementation structure.

Testing strategy defined in:
`/docs/architecture/testing-strategy.md`

---

## 11. CI/CD and Monorepo Governance

CI/CD pipelines must:

* Support selective builds per directory (backend, web, mobile, packages)
* Run tests per affected module
* Enforce linting and static analysis
* Enforce architecture compliance where applicable

Defined in:
`/docs/architecture/ci-cd.md`

---

## 12. AI-Assisted Development Governance

This repository uses structured AI-assisted development.

References:

* `.github/copilot-instructions.md`
* `.github/agents/*.agent.md`

AI tools must:

* Respect documentation hierarchy.
* Respect layered boundaries.
* Not introduce new dependencies autonomously.
* Follow Planning → Implementation → Review workflow.

Architecture prevails over generated output.

---

## 13. Evolution Strategy

The system is designed for controlled evolution.

Architectural changes must:

* Be documented via ADR.
* Avoid cascading structural rewrites.
* Preserve layering and separation of concerns.

The monorepo structure and multi-tenant model are foundational and must remain stable unless redefined through ADR.
