# ADR-010 — Data Governance & Retention Policy

## Status
Proposed

---

## Context

The platform is a multi-tenant SaaS system with:

- Strict tenant isolation
- PostgreSQL as source of truth
- Redis-backed caching
- JWT authentication
- Background job processing
- Feature flag management
- Immutable audit logging
- Horizontal scalability
- Structured logging & observability

As the system evolves toward enterprise-grade maturity, we must define:

- Data ownership model
- Data classification
- Data retention rules
- Data minimization policies
- Tenant data isolation guarantees
- Right-to-access & right-to-erasure readiness (GDPR-aware design)
- Backup and purge governance alignment

Operational decisions must not be ad hoc.

A formal Data Governance and Retention strategy is required.

---

## Decision

We adopt a centralized Data Governance policy based on:

- Explicit data classification
- Defined retention windows per data category
- Controlled purge processes
- Tenant-aware retention enforcement
- Compliance-ready architecture
- Clear separation between operational logs and audit logs

Database remains the source of truth.

---

## Data Classification Model

All persisted data must fall into one of the following categories:

### 1. Core Business Data

Examples:

- Users
- Roles
- Tenant configuration
- Domain entities
- Subscription data

Characteristics:

- Long-term persistence
- Required for platform operation
- Retained while tenant is active

---

### 2. Sensitive Personal Data

Examples:

- Email addresses
- Identifiers
- Personal profile information

Characteristics:

- Subject to GDPR principles
- Must follow data minimization
- Must support erasure/anonymization (where applicable)

---

### 3. Audit Data

Defined in ADR-008.

Characteristics:

- Append-only
- Immutable
- Retention governed
- Not user-editable

---

### 4. Operational Logs

Examples:

- Application logs
- System logs
- Debug logs

Characteristics:

- Short-term retention
- Stored outside primary database
- Not compliance-grade

---

### 5. Derived or Temporary Data

Examples:

- Cache entries
- Temporary files
- Background job artifacts

Characteristics:

- Ephemeral
- TTL-governed
- Never source of truth

---

## Retention Policy

Retention must be category-driven.

### Core Business Data

- Retained while tenant is active.
- Upon tenant deletion:
  - Grace period (configurable).
  - Soft-delete period.
  - Permanent purge.

---

### Sensitive Personal Data

- Minimize storage.
- Support anonymization when legally required.
- No unnecessary duplication.
- No storage in logs.

---

### Audit Logs

- Retention window configurable (e.g., 12–36 months).
- Must align with compliance needs.
- Purge via scheduled background job.
- Purge itself must be audited.

---

### Operational Logs

- Short retention (e.g., 7–30 days).
- Managed at infrastructure level.
- No business data dependency.

---

## Tenant Deletion Workflow

Tenant deletion must follow controlled steps:

1. Mark tenant as `pending_deletion`.
2. Disable authentication.
3. Enforce grace period.
4. Execute background purge job.
5. Delete or anonymize dependent data.
6. Emit audit trail of deletion.
7. Finalize deletion.

No hard deletion without staged process.

---

## Data Minimization Principles

System must enforce:

- Store only necessary fields.
- Avoid redundant copies.
- No sensitive tokens persisted.
- No JWT storage.
- No plaintext secrets.
- Avoid logging personal data.

Frontend must not store sensitive data persistently.

---

## Backup Alignment

Backup strategy must:

- Respect retention policy.
- Avoid infinite retention.
- Allow restoration within compliance boundaries.
- Not reintroduce deleted tenants unintentionally.

Backup & disaster recovery will be formalized in future ADR.

---

## Multi-Tenancy Governance

All data governance policies must:

- Be tenant-scoped.
- Avoid cross-tenant exposure.
- Ensure tenant_id indexed.
- Ensure purge respects tenant boundaries.

No cross-tenant purge operations allowed.

---

## Anonymization vs Deletion

When required by regulation:

- Prefer anonymization if deletion breaks referential integrity.
- Use irreversible anonymization.
- Record anonymization in audit log.

Anonymization must:

- Remove personal identifiers.
- Preserve structural integrity where necessary.

---

## Observability & Monitoring

We must monitor:

- Data growth rate
- Audit table size
- Retention job success
- Purge failures
- Tenant deletion metrics

Alerts required for:

- Retention job failure
- Unexpected storage growth
- Purge job errors

---

## Security Constraints

Data governance must ensure:

- No sensitive fields logged.
- No secret persistence.
- No cross-tenant queries.
- Strict access control to personal data.
- Admin-level audit visibility only.

---

## Compliance Readiness

Architecture must be:

- GDPR-aware
- Data minimization compliant
- Retention-controlled
- Tamper-resistant (audit)
- Traceable

Future-ready for:

- SOC2
- ISO27001
- Data residency enforcement
- Legal hold support

---

## Consequences

### Positive

- Enterprise compliance readiness
- Predictable storage growth
- Controlled tenant deletion
- Legal defensibility
- Reduced data sprawl

### Negative

- Increased operational complexity
- Requires strict discipline
- Requires purge automation
- Additional monitoring required

---

## Architectural Invariants Compliance

This ADR must respect:

1. Tenant isolation is mandatory.
2. Database remains source of truth.
3. Audit logs are immutable.
4. No cross-layer shortcuts.
5. Structured logging discipline.

---

## Final Decision Statement

The system adopts a formal, tenant-aware data governance and retention policy based on explicit data classification, controlled retention windows, purge automation, and compliance-ready design to ensure long-term sustainability and regulatory alignment.