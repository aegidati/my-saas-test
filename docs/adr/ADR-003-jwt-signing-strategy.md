# ADR-003: JWT Signing and Key Rotation Strategy

---

## Status

Accepted

---

## Context

The system uses JWT-based authentication (see authentication.md).

Requirements:

- Stateless authentication
- Support for Web and Mobile clients
- Support for social login integration
- Strong security guarantees
- Protection against token forgery
- Controlled token lifetime
- Ability to rotate signing keys without system downtime
- Support for future scaling (multiple backend instances)

Security posture requires:

- Clear signing algorithm strategy
- Secure key storage
- Key rotation policy
- Backward compatibility during rotation

JWT signing strategy is security-critical and must be formally defined.

---

## Decision

The system will adopt the following JWT signing and key management strategy:

### 1. Signing Algorithm

- Use **RS256 (RSA with SHA-256)** for signing access and refresh tokens.
- Avoid symmetric algorithms (e.g., HS256) in production.

### 2. Key Management

- Private signing keys stored securely in:
  - Environment-managed secret store (e.g., Vault, cloud secret manager)
  - Never in source code
- Public keys exposed through a controlled mechanism if needed (e.g., JWKS endpoint for internal services)

### 3. Key Rotation

- Support multiple active public keys simultaneously.
- Include `kid` (Key ID) in JWT header.
- Allow validation of tokens signed with previous key during rotation window.
- Maintain a defined key rotation schedule.

### 4. Token Lifetime

- Access tokens: short-lived (e.g., 5–15 minutes).
- Refresh tokens: longer-lived but revocable.

---

## Rationale

### Why RS256 Instead of HS256?

Advantages:

- Asymmetric signing separates signing and verification responsibilities.
- Backend instances can verify tokens without access to private key.
- Safer in distributed environments.
- Supports secure future microservice expansion.

HS256 was rejected because:

- Requires sharing secret across services.
- Higher risk if secret leaks.
- Harder to isolate signing authority.

---

## Key Rotation Strategy

### Rotation Requirements

- New key generated securely.
- New tokens signed with new key.
- Old key retained for verification during grace period.
- Old key removed after expiration window.

### Rotation Process

1. Generate new RSA key pair.
2. Store new private key in secure secret store.
3. Publish new public key.
4. Start signing tokens with new key (`kid` updated).
5. Continue validating tokens signed with old key.
6. After grace period, remove old key.

Rotation must be:

- Logged
- Auditable
- Performed without downtime

---

## Consequences

### Positive

- Strong security posture
- Safe distributed validation
- Secure microservice readiness
- Safe key compromise mitigation via rotation
- Clear separation of signing authority

### Negative

- Slightly higher implementation complexity
- Requires proper secret management infrastructure

Security benefit outweighs complexity.

---

## Implementation Notes

- JWT header must include `kid`.
- Backend must maintain active key registry.
- Validation logic must:
  - Select public key by `kid`
  - Reject tokens signed with unknown keys
- Token verification must check:
  - Signature validity
  - Expiration (`exp`)
  - Issuer (`iss`)
  - Audience (`aud`)
  - Tenant claim consistency

Private keys must:

- Never be committed
- Never be logged
- Never be included in container images

---

## Refresh Token Considerations

Refresh tokens must:

- Be stored securely (see authentication.md)
- Be revocable (optional: store token IDs server-side)
- Not be self-contained if revocation is required

Optional improvement:

- Store refresh token identifiers in database to enable forced revocation.

---

## Compliance Requirements

If signing algorithm changes:

- Create new ADR.
- Document migration plan.
- Ensure backward compatibility.

If key management strategy changes:

- Document new secret storage mechanism.
- Update CI/CD and environment provisioning.

JWT signing strategy must not be altered without architectural review.

---

## Review Trigger

This ADR must be reviewed if:

- Microservices architecture is introduced
- External identity provider replaces internal JWT
- Compliance requirements change
- Hardware security module (HSM) is introduced
- Token introspection model is adopted

---

## Relationship to Other ADRs

- ADR-001 — Multi-Tenancy Isolation Strategy
- ADR-002 — Database Engine Strategy
- authentication.md
- security-model.md

JWT signing is foundational to system security and must remain stable and controlled.