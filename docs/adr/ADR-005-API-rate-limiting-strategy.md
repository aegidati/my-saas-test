# ADR-005: API Rate Limiting Strategy

---

## Status

Accepted

---

## Context

The system is a multi-tenant SaaS platform with:

- JWT-based authentication (ADR-003)
- Multi-tenant row-level isolation (ADR-001)
- PostgreSQL as primary database (ADR-002)
- Redis-based caching layer (ADR-004)
- Public API consumed by:
  - Web client (React)
  - Mobile client (React Native)
  - Potential future third-party integrations

Requirements:

- Protect backend resources from abuse
- Prevent denial-of-service via excessive API calls
- Ensure fair usage across tenants
- Avoid a single tenant degrading performance for others
- Support horizontal scaling across backend instances

A clear and enforceable rate limiting strategy is required.

---

## Decision

The system will implement a **Centralized, Tenant-Aware Rate Limiting Strategy using Redis**.

Key decisions:

1. Rate limiting will be enforced at the API boundary (Interfaces layer).
2. Rate limits will be applied at multiple scopes:
   - Per user
   - Per tenant
   - Per IP (optional)
3. Redis will be used as the shared rate limiting store.
4. Rate limit violations will return HTTP 429.
5. Rate limiting must be environment-aware and configurable.

---

## Rationale

### Why Centralized (Redis-Based) Rate Limiting?

- Backend may run multiple instances.
- In-memory rate limiting per instance is inconsistent.
- Redis provides atomic counters and TTL support.
- Shared store ensures consistent enforcement across nodes.

---

### Why Multi-Level Rate Limiting?

Single-level rate limiting is insufficient in multi-tenant SaaS.

We must protect against:

- A single user spamming endpoints.
- A single tenant overwhelming shared resources.
- Anonymous IP abuse (if public endpoints exist).

Therefore, rate limits may apply at:

- User level (user_id)
- Tenant level (tenant_id)
- IP level (for unauthenticated requests)

---

## Rate Limiting Model

### 1. Authenticated Requests

For authenticated requests:

- Identify:
  - user_id
  - tenant_id
- Apply:
  - Per-user limit
  - Per-tenant aggregate limit

Example key patterns:

- `rate:user:{user_id}`
- `rate:tenant:{tenant_id}`

---

### 2. Unauthenticated Requests

For unauthenticated endpoints (e.g., login, password reset):

- Apply IP-based limit.
- Example key:
  - `rate:ip:{ip_address}`

Special care must be taken to avoid:

- Locking out legitimate users due to shared IPs (e.g., mobile networks).
- Excessively strict limits on login endpoints.

---

### 3. Limit Types

Initial strategy:

- Fixed window or sliding window using Redis atomic counters.
- Configurable limits such as:
  - X requests per minute per user
  - Y requests per minute per tenant
  - Z requests per minute per IP

Exact numbers are configuration-level, not hardcoded.

---

## HTTP Behavior

When rate limit is exceeded:

- Return HTTP 429 (Too Many Requests).
- Include headers:
  - `Retry-After`
  - Optional remaining limit indicators
- Response body must follow standard error format (see error-handling.md).

No sensitive internal details must be exposed.

---

## Multi-Tenancy Constraints

Rate limiting must:

- Respect tenant isolation.
- Prevent one tenant from degrading service for others.
- Avoid cross-tenant leakage of metrics or limits.

Tenant-level limits must:

- Be isolated per tenant.
- Not share counters across tenants.

Rate limiting keys must include tenant_id where applicable.

---

## Security Considerations

Rate limiting is a security control and must:

- Protect login endpoints against brute-force attacks.
- Protect sensitive endpoints (e.g., password reset).
- Avoid storing sensitive data in Redis.

Keys must not include:

- Raw tokens
- Passwords
- Sensitive PII

IP-based rate limiting must consider reverse proxies and trusted headers.

---

## Interaction with Caching (ADR-004)

Rate limiting may reuse Redis infrastructure but:

- Must use separate key namespaces.
- Must not interfere with application caching.
- Must not rely on cache TTL policies for correctness beyond rate windows.

Rate limiting and caching are logically separate concerns.

---

## Interaction with Authentication (ADR-003)

Rate limiting must:

- Use verified JWT claims for user_id and tenant_id.
- Not trust unverified request parameters.
- Apply stricter rules to authentication endpoints.

Rate limiting must not:

- Leak whether a user exists based on rate limit responses.

---

## Observability

Rate limiting must be observable via:

- Metrics:
  - Number of 429 responses
  - Per-tenant rate limit hits
  - Per-endpoint rate limit hits
- Logs:
  - Structured logs for rate limit violations
  - Include tenant_id and user_id when applicable

Alerts may be configured for:

- Sudden spikes in rate limit violations
- Suspicious behavior patterns

---

## Operational Considerations

Redis must:

- Be highly available in production.
- Support atomic increment operations.
- Be monitored for:
  - Memory usage
  - Key growth
  - Latency

If Redis is temporarily unavailable:

- Fail-open or fail-closed behavior must be defined.

Initial strategy:

- Prefer **fail-open** for availability (with logging),
- Unless endpoint is security-critical (e.g., login), where stricter behavior may apply.

This choice must be documented and consistent.

---

## Alternatives Considered

### 1. In-Process Rate Limiting

Rejected because:

- Inconsistent across multiple backend instances.
- Not suitable for horizontal scaling.

---

### 2. API Gateway-Level Rate Limiting Only

Considered but not sufficient because:

- Gateway-level limits may not understand tenant_id.
- Business-aware rate limits (per tenant) require application-level context.

Gateway-level limits may still be added as additional outer protection.

---

### 3. No Rate Limiting Initially

Rejected because:

- Exposes system to abuse.
- Contradicts security-model.md.
- Makes later introduction disruptive.

---

## Consequences

### Positive

- Protects system from abuse.
- Enforces fairness across tenants.
- Supports predictable scaling.
- Integrates naturally with Redis infrastructure.

### Negative

- Additional infrastructure complexity.
- Risk of misconfiguration affecting legitimate traffic.
- Requires monitoring and tuning.

Trade-off is acceptable for SaaS security and stability.

---

## Compliance Requirements

Any change to rate limiting strategy involving:

- New algorithm (e.g., token bucket vs sliding window)
- Different storage backend
- Per-tenant custom limits
- Gateway-only enforcement

Must be documented in a new ADR.

---

## Review Trigger

This ADR must be reviewed if:

- System scale increases significantly.
- Enterprise customers require custom rate tiers.
- Public API is exposed to third parties.
- Distributed multi-region deployment is introduced.

---

## Relationship to Other ADRs

- ADR-001: Multi-Tenancy Isolation Strategy
- ADR-003: JWT Signing & Key Rotation Strategy
- ADR-004: Caching Strategy

Rate limiting must always preserve:

- Tenant isolation
- Security boundaries
- Observability discipline
- Layered architecture enforcement