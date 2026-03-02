# STEP-04 — Multi-Tenant Infrastructure Layer

## 1. Purpose

This STEP introduces the **multi-tenant infrastructure primitives** required to enforce tenant isolation across the system, without implementing tenant-specific business features.

Goals:

- Define a canonical `Tenant` model.
- Introduce tenant identification and resolution mechanisms.
- Ensure all tenant-scoped persistence goes through tenant-aware repositories.
- Prepare middleware and context handling so that future features can reliably access `tenant_id`.
- Enforce the architectural invariants from ADR-001 without leaking tenant logic into presentation or domain layers.

No business-specific tenant features (such as billing plans, quotas, or invitations) are included in this STEP.

---

## 2. Scope

### 2.1 In Scope

Backend multi-tenant infrastructure only, specifically:

- Tenant model (e.g., `Tenant` table/entity).
- Tenant context resolution:
  - From request (hostname, header, or explicit identifier).
  - From authenticated user (in future STEPs).
- Tenant-aware repository base classes.
- Middleware or infrastructure components that:
  - Resolve the current tenant for each request.
  - Make `tenant_id` available in application and domain layers (via context or parameters).
- Guardrails that **forbid cross-tenant access** at repository level.

### 2.2 Out of Scope

- Tenant onboarding flows (creation, invitations, approval).
- Tenant admin UIs and management APIs.
- Billing, subscription plans, quotas enforcement.
- Any UX-level behavior.
- Frontend and mobile integration (they will use the APIs once stabilized).
- Complete mapping between users and tenants (basic relation may be defined but not fully exploited in this STEP).

---

## 3. Architectural Context

This STEP MUST comply with:

- ADR-001 — Multi-Tenancy Isolation Strategy  
  (Row-level isolation, all tenant-scoped tables include `tenant_id`, no cross-tenant queries, no global tenant state.)

- ADR-002 — Database Engine Strategy  
  (Tenant model and indexes designed for PostgreSQL as primary engine.)

- ADR-003 — JWT Signing & Key Rotation Strategy  
  (Tokens may carry tenant context in future STEPs; nothing in this STEP may conflict with that.)

- ADR-010 — Data Governance & Retention Strategy  
  (Tenant data boundaries must support governance and retention constraints.)

- ADR-013 — API Versioning Strategy  
  (Any tenant-related endpoints must be versioned, if introduced as technical helpers.)

- ADR-015 — Error & Exception Handling Strategy  
  (Tenant resolution errors must use canonical error format.)

- ADR-016 — Testing Strategy  
  (Specific tests must validate tenant isolation and blocking of cross-tenant access.)

- ADR-018 — Migration & Schema Evolution Policy  
  (Tenant schema and tenant_id columns must follow additive evolution and indexing rules.)

- ADR-019 — Observability & Logging Contract  
  (Logs must include `tenant_id` when applicable without leaking cross-tenant information.)

- ADR-020 — Code Style & Formatting Governance  
  (mypy, flake8, formatting must stay clean.)

This STEP builds directly on top of:

- STEP-02 — Infrastructure Baseline (settings, DB, health check)
- STEP-03 — Authentication Skeleton (user and JWT infrastructure)

---

## 4. Execution Requirements

### 4.1 Planner Agent Responsibilities

The Planner Agent MUST:

1. Analyze current backend structure to identify:
   - Existing models, if any.
   - Any preliminary tenant fields or assumptions.
   - Where repositories and services will live (as defined by earlier architecture docs).

2. Design the **Tenant core model**:
   - Name (e.g., `Tenant`).
   - Key fields (`id`, `name`, `slug` or `code`, timestamps, status flags if needed).
   - Indexes for lookup by slug/subdomain (if applicable).

3. Define **tenant resolution strategy**:
   - Primary resolution mechanism (e.g., from subdomain, header, or explicit URL segment).
   - How it interacts with authenticated user context from STEP-03.
   - How to handle "no tenant" or "invalid tenant" scenarios:
     - Error codes.
     - Error responses following ADR-015.

4. Plan **tenant context propagation**:
   - Middleware or infrastructure components that:
     - Resolve tenant at request boundary.
     - Attach tenant context to request (e.g., `request.tenant` or context object).
   - Application and repository layers should **receive `tenant_id` explicitly** (no global state).

5. Plan **tenant-aware repository abstraction**:
   - Base repository class requiring `tenant_id` for tenant-scoped operations.
   - Guards against:
     - Omitting tenant filters.
     - Accessing data from multiple tenants in a single operation (unless explicitly allowed and justified).

The Planner MUST explicitly separate:

- Technical infrastructure introduced in this STEP.
- Business flows (to be handled later in feature STEPs).

---

### 4.2 Implementer Agent Responsibilities

The Implementer Agent (or human developer) MUST:

- Implement the **Tenant model**, with at least:

  - `id` (UUID or integer, aligned with system conventions).
  - `name` (human-readable).
  - `slug` or `code` (stable identifier for URLs/hostnames).
  - `created_at`, `updated_at`.
  - Any minimal status flags if needed (e.g., `is_active`).

- Implement **tenant resolution middleware**:

  - Read tenant identifier from the chosen mechanism (e.g., subdomain, header).
  - Load the matching Tenant record.
  - Attach it to request context (e.g., `request.tenant`).
  - Raise/return a proper error when:
    - Tenant not found.
    - Tenant inactive/blocked (if modeled).

- Implement **tenant context object or helper**:

  - A small abstraction (e.g., `TenantContext`) that holds:
    - `tenant_id`
    - Possibly `tenant_slug`
  - Ensures that application and repository layers **receive tenant context explicitly**.

- Implement **tenant-aware repository base class**, e.g.:

  - `TenantScopedRepository` with:
    - Methods that always include `tenant_id` or `TenantContext` as argument.
    - Enforcement that queries are filtered by tenant.
    - Helper methods for common CRUD operations in a tenant-safe way.

- Update **existing or skeleton repositories** (if any) to:

  - Require `tenant_id` for tenant-scoped data.
  - Enforce tenant filters in queries.

The Implementer MUST NOT:

- Implement tenant onboarding, invitations, or complex business logic.
- Introduce global variables storing the current tenant.
- Use singleton patterns or static state for tenant context.

---

### 4.3 Reviewer Agent Responsibilities

The Reviewer Agent MUST:

- Verify the **Tenant model**:

  - Is cleanly defined.
  - Has appropriate indexes.
  - Includes `tenant_id` semantics where needed for related models (if any are added in this STEP).

- Verify **tenant resolution**:

  - Middleware is the only place where tenant is resolved from the request.
  - Resulting tenant is attached to request context, not global state.
  - Errors are returned using ADR-015 error contract.

- Verify **repositories**:

  - Any tenant-scoped repository requires tenant context explicitly.
  - No direct ORM queries in higher layers bypassing tenant-aware repositories.
  - No queries that potentially aggregate across multiple tenants unless explicitly allowed and documented.

- Verify **ADR-001 compliance**:

  - No cross-tenant queries.
  - No global tenant state.
  - All tenant-scoped tables have `tenant_id` (if new models are introduced).

- Verify **tests**:

  - There are tests that:
    - Create multiple tenants.
    - Assign or simulate data belonging to different tenants.
    - Assert that tenant-scoped queries never leak data across tenants.

If any violation of ADR-001 or the invariants in the architectural snapshot is found, STEP-04 MUST be rejected.

---

## 5. Concrete Work Items (Checklist)

This checklist is a guide for Planner/Implementer/Reviewer.

### 5.1 Tenant Model

- [ ] Create `Tenant` model with:
  - [ ] `id` (UUID or int, system standard).
  - [ ] `name`.
  - [ ] `slug` or unique code for lookup.
  - [ ] `created_at` / `updated_at`.
  - [ ] Optional `is_active` or similar flag.
- [ ] Add database indexes on:
  - [ ] `slug` or unique code.
  - [ ] Any fields relevant to lookup strategy.

### 5.2 Tenant Resolution Middleware

- [ ] Implement middleware (e.g., `TenantResolutionMiddleware`) that:
  - [ ] Extracts tenant identifier from request (hostname, header, or path segment).
  - [ ] Looks up the corresponding `Tenant`.
  - [ ] Attaches tenant to `request` or context.
  - [ ] Handles missing/invalid tenant with ADR-015 compliant error.

- [ ] Ensure middleware runs **before** business logic but after core framework middleware as appropriate.

### 5.3 Tenant Context & Propagation

- [ ] Define a `TenantContext` or equivalent structure providing:
  - [ ] `tenant_id` as primary field.
  - [ ] Optional `tenant_slug` or display info.

- [ ] Ensure services and repositories receive `TenantContext` or `tenant_id` explicitly as argument.

### 5.4 Tenant-Aware Repository Base

- [ ] Create a base repository (e.g., `TenantScopedRepository`) that:
  - [ ] Requires `tenant_id` / `TenantContext` for all tenant-scoped methods.
  - [ ] Applies tenant filters to all queries.
  - [ ] Provides safe utilities for:
    - [ ] `list_for_tenant`
    - [ ] `get_for_tenant`
    - [ ] `create_for_tenant`
    - [ ] `update_for_tenant`
    - [ ] `delete_for_tenant`

- [ ] Update existing repositories (if any) that operate on tenant-scoped entities to inherit from this base class.

### 5.5 Testing

- [ ] Unit tests for:
  - [ ] Tenant model basic behavior.
  - [ ] Tenant resolution logic (given various inputs, resolves or errors out).
- [ ] Integration tests to ensure:
  - [ ] When two tenants exist, tenant-scoped operations do not leak data.
  - [ ] Repository queries always respect tenant filtering.

---

## 6. Validation & Testing

### 6.1 Local Validation

- [ ] Run migrations to create the `Tenant` table.
- [ ] Manually create two tenants.
- [ ] Exercise the application (via tests or simple endpoints) to:
  - [ ] Confirm that tenant-specific operations are correctly scoped.
  - [ ] Confirm that accessing data under tenant A does not reveal data from tenant B.

### 6.2 Static & Structural Checks

- [ ] Run `mypy` and `flake8`:
  - [ ] Ensure no new type/lint errors are introduced by tenant code.
- [ ] Check imports:
  - [ ] No circular dependencies between domain/application/infrastructure layers.
  - [ ] Tenant context is propagated via parameters, not global state.

---

## 7. Definition of Done — STEP-04

STEP-04 is complete only when ALL the following are true:

1. **Tenant Model**
   - [ ] `Tenant` entity exists with basic required fields.
   - [ ] Appropriate indexes and uniqueness constraints are in place.

2. **Tenant Resolution**
   - [ ] A clear tenant resolution strategy is implemented in middleware.
   - [ ] Invalid/missing tenant scenarios are handled with ADR-015-compliant errors.
   - [ ] No tenant is resolved via global or static variables.

3. **Tenant Context Propagation**
   - [ ] Application and repository layers receive `tenant_id` or `TenantContext` explicitly.
   - [ ] No direct ORM access from upper layers bypasses tenant filtering.

4. **Tenant-Aware Repositories**
   - [ ] A base `TenantScopedRepository` (or equivalent) exists.
   - [ ] All tenant-scoped data access goes through this abstraction.
   - [ ] Cross-tenant queries are not possible without explicit and justified exceptions.

5. **Testing**
   - [ ] There are tests that demonstrate:
     - [ ] Data from tenant A is not visible to tenant B.
     - [ ] Tenant resolution behaves correctly for valid and invalid inputs.
   - [ ] `mypy` and `flake8` pass without new violations.

6. **ADR Compliance**
   - [ ] Implementation complies with ADR-001, 002, 010, 013, 015, 016, 018, 019, 020.
   - [ ] No business logic related to tenants (onboarding, billing, etc.) is prematurely implemented in this STEP.

Only when all points above are verified by the Reviewer, STEP-04 can be considered DONE.