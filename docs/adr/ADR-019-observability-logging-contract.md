# ADR-019 — Observability & Logging Contract

- Status: Accepted
- Date: 2026-02-26
- Authors: Architecture Team
- Related ADRs:
  - ADR-008 — Audit Logging Strategy
  - ADR-012 — Distributed Tracing Strategy
  - ADR-015 — Error Handling Strategy

---

## 1. Context

The system must provide:

- Structured logging
- Tenant-safe observability
- Version-aware monitoring
- Correlation across services

Without a contract, logs become inconsistent and unreliable.

---

## 2. Decision

All logs MUST be structured JSON.

Mandatory log fields:

- timestamp
- level
- message
- request_id
- tenant_id (if applicable)
- api_version (if applicable)
- error_code (if error)

---

## 3. Logging Levels

- DEBUG: Development only
- INFO: Business events
- WARNING: Recoverable anomalies
- ERROR: Application-level failures
- CRITICAL: System failures

---

## 4. Sensitive Data Policy

Logs MUST NOT contain:

- Secrets
- Passwords
- JWT tokens
- PII unless explicitly masked

---

## 5. Metrics & Tracing

Metrics MUST support:

- Per-tenant aggregation
- Per-version aggregation
- Error rate monitoring

Tracing MUST propagate request_id across services.

---

## 6. Consequences

Positive:
- Enterprise-grade observability.
- Faster incident resolution.

Trade-offs:
- Logging discipline required.