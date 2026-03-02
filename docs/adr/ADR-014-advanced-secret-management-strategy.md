# ADR-014 — Advanced Secret Management Strategy

## Status
Proposed

---

## Context

The platform handles:

- JWT signing keys (RS256)
- Database credentials
- Redis credentials
- External API keys
- Webhook secrets
- Encryption keys

Hardcoded secrets or environment-only secrets are insufficient because:

- Horizontal scaling increases exposure surface.
- CI/CD pipelines may leak secrets.
- Logs may accidentally expose sensitive data.
- Key rotation must be supported.

A formal secret management strategy is required.

---

## Decision

We adopt a centralized secret management approach based on:

- External secret storage system (Vault / Cloud Secret Manager).
- Runtime injection into containers.
- No secrets committed to repository.
- Key rotation support.
- Separation between:
  - Application secrets
  - Infrastructure secrets
  - JWT signing keys

---

## Secret Categories

### 1. Application Secrets

- API keys
- Webhook secrets
- Encryption keys

Stored in external secret manager.

---

### 2. Infrastructure Secrets

- DB credentials
- Redis credentials

Injected via secure runtime configuration.

---

### 3. Cryptographic Keys

- JWT private keys
- Encryption master keys

Must support:

- Versioning
- Rotation
- `kid` header usage (ADR-003 compliant)

Old keys retained temporarily for token validation.

---

## Architectural Placement

### Domain Layer

- Must not handle secrets directly.
- Only receives validated inputs.

---

### Application Layer

- Uses injected secrets.
- Never stores secrets in DB.
- Never logs secrets.

---

### Infrastructure Layer

- Responsible for secret retrieval.
- Provides secure configuration injection.
- Implements key rotation logic.

---

## Secret Injection Strategy

At runtime:

- Secrets loaded via:
  - Environment variables injected by secret manager.
  - Mounted secret files.
- No plaintext secrets in repository.
- No secrets in Docker images.

---

## Logging & Observability

Rules:

- Never log secrets.
- Never log full tokens.
- Mask sensitive headers.
- Mask credentials in error logs.

Audit log (ADR-008) must record:

- Key rotation events.
- Secret update events.
- Access to secret configuration.

---

## Key Rotation Strategy

For JWT (RS256):

- Maintain key registry with `kid`.
- Allow multiple active public keys.
- Deprecate old keys gradually.
- Rotate without downtime.

For other secrets:

- Versioned secret entries.
- Update via rolling deployment.

---

## Multi-Tenancy Considerations

- Secrets are global infrastructure-level unless explicitly tenant-specific.
- Tenant-specific secrets (future extension):
  - Stored separately.
  - Encrypted at rest.
  - Strictly scoped by tenant_id.

No cross-tenant secret access.

---

## Security Constraints

- No secrets stored in DB in plaintext.
- Encryption at rest where applicable.
- Principle of least privilege.
- Access to secret manager restricted.
- Secrets never exposed in tracing (ADR-012).

---

## Compliance Considerations

Secret management must support:

- SOC2
- ISO27001
- Secure key lifecycle management
- Auditability of secret access

---

## Consequences

### Positive

- Reduced breach surface.
- Rotation without downtime.
- Enterprise-grade security posture.
- Clear separation of concerns.

### Negative

- Additional infrastructure complexity.
- Requires secure secret manager integration.
- Requires strict operational discipline.

---

## Architectural Invariants Compliance

This ADR must respect:

1. No secrets in frontend.
2. JWT must use RS256 (ADR-003).
3. Structured logging discipline.
4. No cross-layer shortcuts.
5. Tenant isolation preserved.

---

## Final Decision Statement

The system adopts a centralized, externally managed, rotation-capable secret management strategy with strict separation of cryptographic keys, infrastructure credentials, and application secrets to ensure enterprise-grade security and compliance readiness.