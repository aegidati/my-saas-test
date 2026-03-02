# ADR-018 — Database Migration & Schema Evolution Policy

- Status: Accepted
- Date: 2026-02-26
- Authors: Architecture Team
- Related ADRs:
  - ADR-001 — Multi-Tenancy Isolation Strategy
  - ADR-002 — Database Engine Strategy
  - ADR-009 — Horizontal Scaling Strategy

---

## 1. Context

The system uses PostgreSQL as primary production engine.

Schema evolution must support:

- Multi-tenant isolation.
- Zero-downtime deployments.
- Backward compatibility with running services.
- Audit and rollback safety.

---

## 2. Decision

We adopt:

- Forward-only migration discipline.
- Backward-compatible schema evolution.
- Zero-downtime strategy.
- Strict migration review process.

---

## 3. Migration Rules

- Migrations MUST be version-controlled.
- Manual production DB edits are forbidden.
- Destructive operations require staged rollout.

Breaking change pattern:

1. Add new column (nullable).
2. Deploy code supporting both versions.
3. Backfill data.
4. Remove old column in later release.

---

## 4. Multi-Tenant Requirements

All new tables MUST include:

- tenant_id
- Proper indexing for tenant isolation.

Cross-tenant joins are forbidden.

---

## 5. Rollback Policy

- Schema rollbacks are discouraged.
- Roll-forward strategy preferred.
- Production migrations must be tested in staging.

---

## 6. Zero-Downtime Requirements

- No long blocking locks.
- Avoid heavy ALTER TABLE operations.
- Prefer additive changes.

---

## 7. Consequences

Positive:
- Safe production evolution.
- Tenant-safe schema changes.

Trade-offs:
- Slower destructive changes.
- More planning required.