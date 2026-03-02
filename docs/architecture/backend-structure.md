# Backend Structure

---

## 1. Purpose

This document defines the internal structure of the `backend/` directory and how the Django-based backend is organized according to the layered architecture defined in `ARCHITECTURE.md`.

It specifies:

- Directory layout
- Layer responsibilities
- Dependency rules
- Multi-tenancy integration points
- Database abstraction integration
- Authentication and authorization integration
- Testing structure
- Evolution rules

In case of conflict, ADRs prevail.

---

## 2. Architectural Principles

The backend must strictly follow a layered architecture:

- Domain
- Application
- Infrastructure
- Presentation (Interfaces / API)

Key principles:

- Domain is framework-agnostic.
- Infrastructure contains all Django and ORM logic.
- Interfaces contain HTTP entry points only.
- Application orchestrates use cases.
- Dependencies must point inward only.
- No circular dependencies.
- Multi-tenancy and database abstraction must not leak into Domain.

---

## 3. Backend Directory Structure

The backend resides under the `backend/` directory.

The logical structure is:

backend/  
├── manage.py  
├── pyproject.toml | requirements.txt  
├── backend_core/  
│   ├── settings/  
│   │   ├── base.py  
│   │   ├── dev.py  
│   │   └── prod.py  
│   ├── urls.py  
│   ├── asgi.py  
│   └── wsgi.py  
├── domain/  
│   ├── tenants/  
│   ├── users/  
│   └── ...  
├── application/  
│   ├── tenants/  
│   ├── users/  
│   └── ...  
├── infrastructure/  
│   ├── db/  
│   │   ├── models/  
│   │   ├── repositories/  
│   │   └── routers.py  
│   ├── auth/  
│   ├── integrations/  
│   └── middleware/  
├── interfaces/  
│   ├── api/  
│   │   ├── urls.py  
│   │   ├── views.py  
│   │   ├── serializers.py  
│   │   └── permissions.py  
│   └── cli/  
├── shared/  
└── tests/  
    ├── domain/  
    ├── application/  
    ├── infrastructure/  
    └── interfaces/  

The physical structure may evolve, but logical layer separation must remain intact.

---

## 4. Domain Layer (`backend/domain/`)

### Responsibilities

- Domain entities
- Value objects
- Aggregates
- Domain services
- Business rules
- Invariants
- Domain-level validation

### Constraints

- No Django imports
- No ORM usage
- No infrastructure imports
- No HTTP logic
- No persistence logic

The Domain layer must remain pure and testable without database or framework dependencies.

---

## 5. Application Layer (`backend/application/`)

### Responsibilities

- Use case orchestration
- Coordination between domain and repositories
- Transaction boundaries (conceptual)
- Input/Output DTOs or command/query models
- Enforcement of authorization rules (where applicable)

### Constraints

- May depend on Domain
- Must not depend on Django-specific APIs
- Must not implement persistence logic
- Must not handle HTTP requests directly

Application services coordinate the flow:

Interface → Application → Domain → Infrastructure

---

## 6. Infrastructure Layer (`backend/infrastructure/`)

### Responsibilities

- Django ORM models
- Repository implementations
- Database routing
- Multi-tenancy enforcement at persistence level
- JWT issuance and validation
- Social authentication integration
- External service integrations (email, payment, etc.)
- Middleware (e.g., tenant resolution)

### Constraints

- May depend on Domain and Application
- May depend on Django and third-party libraries
- Must not expose ORM models to Domain
- Must enforce tenant isolation rules

All database interactions must occur inside this layer.

---

## 7. Interfaces / Presentation Layer (`backend/interfaces/`)

### Responsibilities

- HTTP endpoints (Django views / DRF viewsets)
- Request validation
- Response serialization
- Mapping HTTP requests to application services
- Authentication enforcement glue

### Constraints

- Must not implement business rules
- Must not access ORM directly
- Must not perform complex authorization logic
- Must delegate to Application layer

Interfaces are adapters only.

---

## 8. Django Project Core (`backend/backend_core/`)

### Responsibilities

- Django settings configuration
- URL root configuration
- ASGI/WSGI setup
- Installed apps configuration
- Middleware registration
- Logging configuration
- Database configuration

### Constraints

- No business logic
- No domain rules
- Only wiring and configuration

---

## 9. Multi-Tenancy Integration

Multi-tenancy integration points:

- Tenant resolution occurs at request boundary (middleware or API layer).
- A Tenant Context object is created per request.
- Tenant Context is passed into Application services.
- Infrastructure repositories enforce tenant scoping.
- Database routers may select DB or schema per tenant.

Strict rules:

- No global mutable tenant state.
- No tenant filtering in frontend.
- No cross-tenant queries unless explicitly designed.

---

## 10. Database Abstraction Integration

Database abstraction is implemented in `infrastructure/db/`.

Rules:

- Repository interfaces are defined in Domain or Application.
- Repository implementations reside in Infrastructure.
- Django ORM models must not be used in Domain.
- Engine-specific logic must remain inside Infrastructure.
- Domain must remain database-engine agnostic.

---

## 11. Authentication and Authorization Integration

### Authentication

- Implemented in `infrastructure/auth/`
- JWT validation integrated at API boundary
- Tenant claim validated against resolved tenant
- Token logic must not leak into Domain

### Authorization

- Authorization rules enforced in Application or Domain
- Interfaces layer may call centralized authorization services
- Infrastructure must not contain business authorization logic

---

## 12. Shared Utilities (`backend/shared/`)

Optional module for:

- Pure utilities
- Reusable helpers
- Cross-layer safe abstractions

Constraints:

- Must not depend on Django
- Must not depend on Infrastructure or Interfaces
- Should remain lightweight

---

## 13. Testing Structure

Tests mirror architectural layers:

- tests/domain → pure unit tests
- tests/application → use case integration tests
- tests/infrastructure → DB integration tests
- tests/interfaces → API tests with authentication

Multi-tenant scenarios must be explicitly tested.

---

## 14. Dependency Rules

Allowed import directions:

- interfaces → application, domain
- application → domain
- infrastructure → application, domain
- domain → (no outward dependencies)

Forbidden:

- domain importing infrastructure
- domain importing Django
- interfaces directly accessing ORM
- circular dependencies across layers

These rules must be enforced in code review.

---

## 15. Evolution Strategy

Backend structure may evolve, but:

- Layer boundaries must remain intact.
- Structural refactoring impacting dependencies requires ADR.
- Domain purity must never be compromised.
- Multi-tenancy and database abstraction boundaries must remain stable.

The backend structure is foundational for:

- Testability
- Maintainability
- Multi-tenant safety
- Security consistency
- Long-term architectural integrity