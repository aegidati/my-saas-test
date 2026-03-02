# ADR-007 — Feature Flag & Runtime Configuration Strategy

## Status
Proposed

---

## Context

The platform is a multi-tenant SaaS system with strict architectural invariants:

- Tenant isolation is mandatory.
- Layer separation must be preserved.
- No business logic in presentation layer.
- Database remains source of truth.
- No cross-layer shortcuts allowed.

As the platform evolves, we require controlled rollout mechanisms for:

- Gradual feature releases
- A/B testing
- Tenant-specific feature enablement
- Beta features
- Emergency feature kill-switch
- Operational toggles (e.g., temporary disable background job types)

Hardcoding feature toggles or using environment-based switches is insufficient because:

- We need tenant-scoped enablement
- We require runtime toggling without redeployment
- We must avoid configuration drift
- We must preserve auditability

A structured Feature Flag strategy is required.

---

## Decision

We adopt a centralized, database-backed Feature Flag system with tenant-aware evaluation and strict architectural placement.

The system will:

- Store feature flags in the database
- Support global flags
- Support tenant-scoped overrides
- Support percentage rollout (future-ready)
- Be evaluated server-side only
- Expose controlled evaluation results to frontend

No feature logic will live in frontend.

---

## Architectural Placement

Feature Flag components are distributed as follows:

### Domain Layer

Contains:

- FeatureFlag entity
- Evaluation rules (pure logic)
- No infrastructure dependencies

Domain must not import ORM or cache libraries.

---

### Application Layer

Responsible for:

- Flag evaluation orchestration
- Resolving tenant-specific overrides
- Applying rollout rules
- Providing flag evaluation service

---

### Infrastructure Layer

Contains:

- Repository implementation (Django ORM)
- Optional Redis caching
- Storage adapter

---

### Interface Layer

- API endpoints may expose flag states to frontend
- Frontend consumes evaluated flags only
- Frontend must not implement evaluation logic

---

## Multi-Tenancy Rules

Feature flags must respect tenant isolation.

Rules:

1. Global flags may exist.
2. Tenant overrides must include `tenant_id`.
3. Flag evaluation requires explicit tenant context.
4. No cross-tenant reads allowed.
5. Cache keys must include `tenant_id`.

Tenant isolation applies even to configuration data.

---

## Flag Types

### 1. Global Boolean Flags

Simple on/off flags affecting entire platform.

Example:
- enable_new_dashboard

---

### 2. Tenant-Scoped Flags

Override global behavior for specific tenants.

Example:
- enable_advanced_reporting for tenant X only

---

### 3. Operational Flags

Used for:
- Kill switches
- Emergency disable
- Operational throttling

These must be restricted to admin roles.

---

### 4. Percentage Rollout (Future Extension)

Support gradual rollout based on:

- Tenant ID hashing
- User ID hashing
- Deterministic evaluation

Not mandatory in initial implementation but architecture must allow it.

---

## Evaluation Strategy

Evaluation rules:

1. Check tenant override first.
2. If not present, fallback to global flag.
3. If no flag exists, default to disabled.

Evaluation must be:

- Deterministic
- Fast
- Cacheable
- Idempotent

---

## Caching Strategy

Feature flags may be cached in Redis.

Rules:

- Cache key must include:
  - flag_name
  - tenant_id
- TTL must be defined.
- Cache invalidation must occur on flag update.

Database remains source of truth.

---

## Security Constraints

- Only authorized admin roles may modify flags.
- All flag changes must be audit logged.
- No sensitive data in flag payload.
- No secrets stored in flags.

---

## Observability Requirements

We must monitor:

- Flag evaluation count
- Cache hit/miss ratio
- Flag update frequency

Audit log must record:

- Who changed the flag
- Old value
- New value
- Timestamp
- Tenant scope (if applicable)

---

## Deployment & Runtime Behavior

Feature flags must:

- Not require redeployment
- Be modifiable at runtime
- Be versionable
- Be migration-safe

Migrations must include schema evolution for feature flags.

---

## Consequences

### Positive

- Safe feature rollout
- Tenant-specific enablement
- Emergency kill-switch capability
- Reduced deployment risk
- Controlled experimentation

### Negative

- Increased system complexity
- Risk of flag sprawl
- Potential logic branching explosion
- Requires strong governance discipline

---

## Architectural Invariants Compliance

This ADR must respect:

1. Tenant isolation is mandatory.
2. Database remains source of truth.
3. No business logic in frontend.
4. No cross-layer shortcuts.
5. All changes must be audit logged.

---

## Final Decision Statement

The system adopts a database-backed, tenant-aware, server-side evaluated Feature Flag strategy with strict architectural layering, observability, and auditability.