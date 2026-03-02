# Authorization Architecture

---

## 1. Purpose

This document defines the authorization architecture of the system.

It specifies:

- The authorization model (RBAC / policy-based)
- Tenant-scoped authorization rules
- Where authorization logic resides
- How authorization integrates with authentication and multi-tenancy
- Enforcement boundaries across layers
- Prohibited patterns

This document complements:

- `ARCHITECTURE.md`
- `multi-tenancy.md`
- `authentication.md`
- `backend-structure.md`
- Relevant ADRs

In case of conflict, ADRs prevail.

---

## 2. Authorization Goals

The authorization system must:

- Enforce strict tenant isolation
- Prevent cross-tenant access by design
- Centralize permission logic
- Avoid duplication of authorization checks
- Be testable and deterministic
- Remain independent from UI implementation
- Avoid embedding authorization logic inside infrastructure

Authorization is a domain-level concern, not a frontend concern.

---

## 3. Authorization Model

The system uses a layered authorization model composed of:

- Role-Based Access Control (RBAC)
- Optional Policy-Based rules (when necessary)

### 3.1 Role-Based Access Control (RBAC)

Users are assigned roles within a tenant.

Examples:

- Tenant Admin
- Manager
- Member
- Viewer

Characteristics:

- Roles are tenant-scoped
- A user may have different roles across tenants
- Roles define allowed actions

Roles must be stored and validated in a tenant-aware manner.

---

### 3.2 Policy-Based Authorization

In addition to roles, complex business rules may require policies.

Examples:

- A user can modify a resource only if they created it.
- A user can access billing only if subscription is active.
- A user can perform an action only within a specific time window.

Policies:

- Are implemented in Application or Domain layer
- Are explicit and testable
- Must not be hidden inside controllers

---

## 4. Authorization and Multi-Tenancy

Authorization must integrate strictly with multi-tenancy.

Rules:

- Every authorization decision must be tenant-aware.
- A user cannot access resources outside their tenant.
- JWT tenant claim must match resolved tenant.
- Role lookup must be performed within tenant scope.
- Cross-tenant roles are forbidden unless explicitly defined via ADR.

Tenant context must always be provided to authorization logic.

---

## 5. Layer Responsibilities

### 5.1 Domain Layer

May contain:

- Domain policies
- Invariant enforcement rules
- Role definitions (as domain concepts)

Must not:

- Depend on infrastructure
- Access database directly

---

### 5.2 Application Layer

Primary enforcement location for authorization.

Responsibilities:

- Check permissions before executing use cases
- Invoke domain policies
- Enforce role checks
- Throw explicit authorization exceptions

Application services must never assume authorization has already been performed elsewhere.

---

### 5.3 Infrastructure Layer

Responsibilities:

- Provide role/permission repository implementations
- Provide identity resolution adapters
- Provide technical enforcement glue (e.g., permission decorators)

Must not:

- Contain business authorization rules
- Decide role semantics

---

### 5.4 Interfaces / API Layer

Responsibilities:

- Authenticate user
- Pass identity and tenant context to application
- Optionally perform preliminary permission checks
- Translate authorization exceptions to HTTP 403 responses

Must not:

- Embed business authorization logic
- Hardcode permission rules

---

## 6. Authorization Flow

Typical request flow:

1. Request arrives at API.
2. Authentication validates JWT.
3. Tenant is resolved.
4. Application service is invoked with:
   - User identity
   - Tenant context
5. Application service performs:
   - Role check
   - Policy evaluation
6. If authorized → proceed.
7. If not authorized → raise explicit authorization exception.

Authorization must fail explicitly and early.

---

## 7. Role and Permission Design

### 7.1 Role Definition

Roles must:

- Be explicit
- Be versioned or evolvable
- Be documented
- Be tenant-scoped

Role definitions should not be hardcoded across multiple files.

---

### 7.2 Permission Granularity

Permissions may be:

- Action-based (create_user, delete_invoice)
- Resource-based (edit_own_profile)
- Context-based (manage_tenant_settings)

Granularity must balance:

- Security
- Maintainability
- Simplicity

Overly complex permission matrices must be avoided.

---

## 8. Authorization Exceptions

Unauthorized access must:

- Raise explicit domain/application exception
- Be mapped to HTTP 403
- Avoid leaking sensitive details
- Not reveal internal system structure

Error responses must be consistent across API.

---

## 9. Testing Requirements

Authorization must be validated through:

- Unit tests for domain policies
- Integration tests for application services
- Multi-tenant isolation tests
- Negative tests (ensure forbidden access is rejected)

Authorization tests must explicitly verify cross-tenant protection.

---

## 10. Prohibited Patterns

The following are strictly forbidden:

- Authorization logic in frontend only
- Authorization checks only in API controllers
- Hardcoded role checks scattered across files
- Bypassing authorization for “internal” endpoints
- Mixing authentication and authorization logic
- Cross-tenant access without explicit rule

Any deviation requires ADR approval.

---

## 11. Evolution Strategy

Authorization model changes require ADR if they involve:

- Introducing new role hierarchy model
- Changing permission semantics
- Introducing cross-tenant roles
- Switching from RBAC to a different model
- Introducing external policy engines

Authorization must evolve deliberately and under architectural governance.

It is a foundational security boundary and must remain consistent, centralized, and testable.