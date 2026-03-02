# STEP-05 — Repository & Service Pattern Foundation

## 1. Purpose

This STEP formalizes the **application-layer architecture** by introducing:

- A clear Repository pattern abstraction.
- A clear Application Service layer.
- Explicit separation between:
  - Domain
  - Application
  - Infrastructure
  - Interfaces (API)

The goal is to prevent:

- Business logic leaking into views/controllers.
- Direct ORM usage from higher layers.
- Tight coupling between infrastructure and domain logic.

This STEP applies and operationalizes existing architectural constraints for repository and service layering.

No new business features are implemented here.

---

## 2. Scope

### 2.1 In Scope

Backend architecture only:

- Definition of repository interfaces (in domain or application layer).
- Implementation of repositories in infrastructure layer.
- Definition of Application Services (use-case layer).
- Clear dependency direction enforcement.
- Example vertical slice demonstrating correct usage pattern.

### 2.2 Out of Scope

- New business features.
- Frontend changes.
- Tenant onboarding flows.
- Advanced authorization logic (RBAC comes later).
- CI/CD changes.
- Observability enhancements beyond what already exists.

---

## 3. Architectural Context

This STEP MUST comply with:

- ADR-001 — Multi-Tenancy Isolation Strategy  
  (Repositories must enforce tenant boundaries.)

- ADR-002 — Database Engine Strategy  
  (Repositories abstract ORM usage; DB remains source of truth.)

- ADR-015 — Error & Exception Handling Strategy  
  (Application services raise domain/application errors, not raw framework exceptions.)

- ADR-016 — Testing Strategy & Test Pyramid  
  (Repositories and services must be testable in isolation.)

- ADR-017 — Dependency & Package Management Strategy  
  (Clear dependency direction: domain ← application ← infrastructure ← interfaces.)

- ADR-018 — Migration & Schema Evolution Policy  
  (Repositories must not bypass migration discipline.)

- ADR-020 — Code Style & Formatting Governance  
  (mypy, flake8 must remain clean.)

This STEP builds on:

- STEP-02 — Infrastructure Baseline
- STEP-03 — Authentication Skeleton
- STEP-04 — Multi-Tenant Infrastructure Layer

---

## 4. Layer Responsibilities (Applied from ADRs and Architecture)

Layer contracts are applied here as defined in ADRs and architecture documents.

### 4.1 Domain Layer

- Contains:
  - Entities
  - Value objects
  - Pure business rules
- Must NOT:
  - Import Django ORM
  - Import infrastructure modules
  - Import request/response objects

### 4.2 Application Layer

- Contains:
  - Use-case services
  - Orchestrates domain entities and repositories
  - Handles transaction boundaries (if required)
- Must:
  - Depend on repository interfaces
- Must NOT:
  - Import ORM models directly
  - Contain framework-specific code

### 4.3 Infrastructure Layer

- Contains:
  - ORM models
  - Repository implementations
  - External service adapters
- Must:
  - Implement repository interfaces defined above
- Must NOT:
  - Contain business orchestration logic

### 4.4 Interfaces Layer

- Contains:
  - API endpoints
  - Request parsing
  - Response formatting
- Must:
  - Call application services
- Must NOT:
  - Contain business logic
  - Access ORM directly

---

## 5. Execution Requirements

### 5.1 Planner Agent Responsibilities

The Planner MUST:

1. Analyze current project structure.
2. Identify whether:
   - Repository abstractions exist.
   - Services are already partially implemented.
3. Define a clean repository interface structure:

   - Example:
     - `UserRepository`
     - `TenantRepository`
     - `TenantScopedRepository` (already from STEP-04)

4. Define application service structure:

   - Example:
     - `GetCurrentUserService`
     - `CreateTenantService` (as placeholder, not full feature)

5. Propose one **example vertical slice**:

   Interfaces → Application Service → Repository → ORM Model

6. Ensure:
   - No circular dependencies.
   - Proper dependency direction.

The Planner MUST NOT:

- Introduce full business features.
- Modify tenant resolution logic.
- Implement authorization policies.

---

### 5.2 Implementer Responsibilities

The Implementer MUST:

- Define repository interfaces in:
  - `application/` or `domain/` (depending on chosen pattern).
- Implement repository concrete classes in:
  - `infrastructure/`.

Example structure:

- `application/repositories/user_repository.py` (interface)
- `infrastructure/repositories/django_user_repository.py` (implementation)

- Ensure repositories:
  - Enforce tenant_id where applicable.
  - Do not expose raw ORM objects outside infrastructure.

- Implement at least one example Application Service:

  Example:
  - `GetCurrentUserService`
    - Receives `user_id`
    - Uses `UserRepository`
    - Returns domain entity or DTO

- Ensure interfaces layer (API):

  - Calls Application Service.
  - Converts result into response format.
  - Does NOT call ORM directly.

The Implementer MUST:

- Remove any direct ORM usage in views (if present).
- Ensure all data access flows through repositories.

---

### 5.3 Reviewer Responsibilities

The Reviewer MUST verify:

- No direct ORM imports in:
  - `interfaces/`
  - `application/`
  - `domain/`

- Repository interfaces are:
  - Located outside infrastructure.
  - Cleanly abstracted.

- Infrastructure implementations:
  - Depend on ORM.
  - Implement only the defined interfaces.

- Application services:
  - Orchestrate logic.
  - Do not depend on framework objects (e.g., HttpRequest).

- Dependency direction is respected:

  domain ← application ← infrastructure ← interfaces

- No circular imports exist.

- Tenant-aware repositories enforce tenant isolation (from STEP-04).

If any layering violation is detected, STEP-05 MUST be rejected.

---

## 6. Concrete Work Items (Checklist)

### 6.1 Repository Interfaces

- [ ] Define repository interfaces:
  - [ ] UserRepository
  - [ ] TenantRepository
  - [ ] Any other foundational repository needed
- [ ] Ensure interfaces:
  - [ ] Do not import ORM models.

### 6.2 Repository Implementations

- [ ] Implement concrete repositories in infrastructure.
- [ ] Ensure:
  - [ ] All queries are tenant-aware (if applicable).
  - [ ] No cross-tenant queries exist.

### 6.3 Application Services

- [ ] Create at least one example service:
  - [ ] Demonstrates full vertical slice.
- [ ] Ensure:
  - [ ] Services depend only on interfaces.
  - [ ] Services return domain entities or DTOs.

### 6.4 Interfaces Layer Cleanup

- [ ] Ensure API endpoints:
  - [ ] Call services.
  - [ ] Do not access ORM.
  - [ ] Do not contain business rules.

---

## 7. Validation & Testing

### 7.1 Structural Validation

- [ ] Run `mypy` to ensure:
  - [ ] No circular type issues.
  - [ ] Clean typing across layers.
- [ ] Run `flake8`.

### 7.2 Behavioral Validation

- [ ] Confirm:
  - [ ] `/auth/me` (from STEP-03) now calls an Application Service instead of ORM directly.
- [ ] Confirm:
  - [ ] Tenant-based queries go through TenantScopedRepository.

---

## 8. Definition of Done — STEP-05

STEP-05 is complete only when:

1. **Repository Pattern Established**
   - [ ] Repository interfaces defined outside infrastructure.
   - [ ] Concrete implementations exist in infrastructure.
   - [ ] No direct ORM access from upper layers.

2. **Application Service Layer Established**
   - [ ] At least one real service implemented.
   - [ ] Interfaces call services, not ORM.

3. **Layering Discipline**
   - [ ] No circular dependencies.
   - [ ] Proper dependency direction respected.
   - [ ] Tenant-aware repositories enforce isolation.

4. **Static Checks**
   - [ ] `mypy` passes.
   - [ ] `flake8` passes.

5. **ADR Compliance**
   - [ ] Complies with ADR-001, 002, 015, 016, 017, 018, 020.
   - [ ] No premature business logic introduced.

Only when all conditions are met and confirmed by the Reviewer can STEP-05 be marked as DONE.