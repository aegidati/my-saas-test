# ADR-008 — Audit Logging & Compliance Strategy

## Status
Proposed

---

## Context

The platform is a multi-tenant SaaS system with strict architectural invariants:

- Tenant isolation is mandatory.
- Database is the source of truth.
- Structured logging is enforced.
- Background jobs are supported.
- Feature flags are runtime-configurable.
- Security and observability are first-class concerns.

As the system evolves toward enterprise-grade maturity, we must introduce:

- Immutable audit trails
- Tenant-scoped traceability
- Compliance readiness (GDPR-aware design)
- Administrative action tracking
- Security event recording
- Configuration change tracking
- Financial/critical action logging

Operational logs are insufficient because:

- They are not immutable.
- They are not compliance-grade.
- They are not query-optimized for investigations.
- They may be rotated or deleted.

A formal Audit Logging strategy is required.

---

## Decision

We adopt a centralized, database-backed, immutable Audit Log system with strict tenant isolation and compliance-ready design.

Audit logs are:

- Persisted in the database
- Append-only
- Immutable (no update/delete)
- Tenant-scoped
- Structured
- Queryable
- Retention-governed

Audit logs are not standard application logs.

---

## Architectural Placement

### Domain Layer

Contains:

- AuditEvent entity
- AuditEventType definitions
- No infrastructure dependency

Domain must not depend on ORM or logging framework.

---

### Application Layer

Responsible for:

- Emitting audit events
- Enforcing audit rules
- Attaching metadata (actor, tenant, timestamp)
- Guaranteeing critical operations produce audit entries

Audit emission must not be optional for critical operations.

---

### Infrastructure Layer

Contains:

- Django ORM implementation
- Database model
- Storage optimizations
- Optional asynchronous write support
- Retention enforcement jobs

---

### Interface Layer

- Admin APIs may query audit logs (role-restricted).
- No public API exposure.
- No direct modification endpoints.

---

## What Must Be Audited

Audit logging is mandatory for:

### 1. Authentication & Authorization

- Login attempts (success/failure)
- Token refresh
- Role assignment
- Role revocation
- Permission changes

---

### 2. Administrative Actions

- Feature flag changes
- Tenant configuration updates
- User creation/deletion
- Role changes
- Rate limit changes
- Secret rotation

---

### 3. Sensitive Business Actions

- Financial operations
- Subscription changes
- Critical data updates
- Data exports
- Bulk imports

---

### 4. Security Events

- Suspicious activity
- Rate limit violations
- Access denials
- Permission violations

---

## Multi-Tenancy Rules

Audit logs must strictly respect tenant isolation.

Rules:

1. Every audit event must include `tenant_id`.
2. System-level events may use a special `system` tenant.
3. No cross-tenant queries allowed.
4. Cache keys (if used) must include tenant scope.
5. Data partitioning strategy must consider tenant_id indexing.

Tenant isolation applies to audit access.

---

## Audit Event Structure

Each audit record must include:

- id (UUID)
- tenant_id
- actor_id (nullable for system)
- actor_type (user/system/service)
- event_type
- resource_type
- resource_id
- action
- previous_state (optional, sanitized)
- new_state (optional, sanitized)
- metadata (JSON)
- timestamp (UTC, immutable)
- request_id (if applicable)

No secrets or sensitive tokens stored.

---

## Immutability Enforcement

Audit records must be:

- Append-only
- Non-updatable
- Non-deletable (except retention purge jobs)
- Protected at ORM level
- Protected at DB constraint level (where possible)

Any modification attempt must be considered a critical violation.

---

## Performance Strategy

Audit writes must:

- Not block critical operations
- Be reliable

Strategy:

- Synchronous write for critical operations
- Optional async dispatch via background jobs (ADR-006)
- Indexed by:
  - tenant_id
  - timestamp
  - event_type

---

## Retention Policy

Retention rules:

- Default retention window configurable (e.g., 12–36 months)
- Tenant-specific override possible (future)
- Purge handled via scheduled job
- Purge events must themselves be audited

Retention must balance:

- Compliance requirements
- Storage cost
- Performance

---

## Observability & Monitoring

We must monitor:

- Audit write failures
- Audit event volume
- Retention purge metrics
- Suspicious event frequency

Alerts required for:

- Audit write failures
- Abnormal security event spikes

Audit pipeline failure must be considered critical.

---

## Security Constraints

- Only privileged roles may query audit logs.
- No modification endpoints.
- Export must be controlled and logged.
- Sensitive fields must be sanitized.
- No secret leakage in metadata.

---

## Compliance Considerations

Architecture must be:

- GDPR-aware (data subject access)
- Data minimization compliant
- Retention policy enforced
- Tamper-resistant

Future compliance extensions:

- SOC2 readiness
- ISO27001 alignment
- Immutable storage support (WORM)

---

## Consequences

### Positive

- Enterprise readiness
- Regulatory compliance support
- Security investigation capability
- Administrative accountability
- Safer production governance

### Negative

- Increased storage usage
- Additional performance overhead
- Governance discipline required
- Risk of over-auditing

---

## Architectural Invariants Compliance

This ADR must respect:

1. Tenant isolation is mandatory.
2. Database remains source of truth.
3. Structured logging discipline.
4. Background jobs integration allowed.
5. No cross-layer shortcuts.

---

## Final Decision Statement

The system adopts a centralized, append-only, tenant-aware audit logging strategy with compliance-ready retention, strict immutability enforcement, and full observability integration.