# ADR-004: Caching Strategy

---

## Status

Accepted

---

## Context

The system is a multi-tenant SaaS platform with:

- Django backend
- React web frontend
- React Native mobile app
- PostgreSQL as primary database (see ADR-002)
- Row-level tenant isolation (see ADR-001)

Performance and scalability requirements:

- Minimize database load for frequently accessed data
- Reduce latency for read-heavy operations
- Support future scale-out scenarios
- Preserve strict tenant isolation

Caching can significantly improve performance but introduces:

- Consistency challenges
- Potential multi-tenant data leakage if misused
- Additional operational complexity

A clear caching strategy is required to avoid unsafe or inconsistent usage.

---

## Decision

The system will adopt a **Centralized Multi-Tenant-Aware Caching Strategy using Redis** as the primary cache store.

Key decisions:

1. **Cache Backend**
   - Use Redis as shared cache backend for all backend instances.
   - No in-process or local-only caches for tenant-scoped data in the first iteration.

2. **Cache Scope**
   - Primary use: backend caching (Django + application-level caching).
   - Frontend (web/mobile) may use local in-memory/cache mechanisms for UI only, not as source of truth.

3. **Multi-Tenant Safety**
   - All tenant-scoped cache keys must include `tenant_id` as part of the key namespace.
   - No cross-tenant shared cache entries unless explicitly designed and documented.

4. **Cache Usage Level**
   - Caching logic will reside in:
     - Infrastructure layer for repository-level caching
     - Application layer for use-case-level caching where appropriate
   - Domain layer remains cache-agnostic.

---

## Rationale

### Why Redis?

Advantages:

- In-memory speed with persistence options
- Mature ecosystem and client support
- Good integration with Django
- Suitable for shared, multi-instance environments
- Supports advanced features (TTL, eviction policies, pub/sub) for future use

Compared to in-memory per-process caches:

- Centralization avoids inconsistency across instances
- Better for horizontal scaling

---

### Why Backend-Centric Caching?

- Backend has full knowledge of:
  - Tenant context
  - Authorization rules
  - Data consistency needs

- Frontend local caches (web/mobile):
  - Are allowed only for UX optimization (short-lived, per session/app)
  - Must never be treated as authoritative
  - Must always tolerate stale data and validate with backend when needed

Backend-centric caching simplifies:

- Consistency management
- Multi-tenant safety
- Operational observability

---

## Cache Types and Use Cases

### 1. Read-through Cache (Recommended)

Pattern:

- On read:
  - Check cache.
  - If miss → load from DB → populate cache → return.
- On write:
  - Write to DB.
  - Invalidate or update relevant cache keys.

Use cases:

- Frequently accessed reference data
- Configuration lookups
- Read-heavy, low-churn resources

---

### 2. Explicit Application-Level Cache

Pattern:

- Application service decides which results to cache.
- Keys are carefully constructed, including:
  - Tenant ID
  - Parameters
  - Version identifiers (if necessary)

Use cases:

- Computed aggregates
- Derived views
- Expensive read-only calculations

---

### 3. Prohibited Uses

- Caching security-sensitive decisions (e.g., authZ) without careful TTL and invalidation strategy.
- Caching data that changes very frequently unless carefully analyzed.
- Caching write operations.

---

## Multi-Tenancy Constraints

To preserve tenant isolation:

- All tenant-scoped cache keys must include tenant identifier, e.g.:

  - `tenant:{tenant_id}:user:{user_id}`
  - `tenant:{tenant_id}:settings`
  - `tenant:{tenant_id}:resource:{resource_id}`

- Shared (global) cache keys are allowed only for:
  - Public, non-tenant-specific data
  - Static configuration that is truly global

Forbidden:

- Reusing cache keys across tenants
- Deriving cache keys from user input without validation
- Using ambiguous keys that do not encode tenant context where needed

---

## Consistency and Invalidation

### Invalidation Rules

- On write operations that affect cached resources:
  - Invalidate corresponding cache entries.
- On bulk changes (e.g., tenant-level operations):
  - Use predictable key patterns to invalidate groups (e.g., prefixes) where supported.

General approach:

- Prefer **cache-as-optimization** (source of truth is always DB).
- Accept small eventual-consistency windows where appropriate.
- Do not rely on cache-only data for critical invariants.

---

### TTL (Time To Live)

- TTL must be defined per use-case.
- Recommended:
  - Short TTL for data that may change frequently.
  - Longer TTL for reference/configuration data.
- No “infinite TTL” without explicit justification.

TTL policy must balance:

- Freshness
- Performance
- Operational complexity

---

## Security Considerations

- Cache must never store:
  - Passwords
  - Raw tokens (JWT, refresh tokens)
  - Secrets

- When necessary to cache security-related info (e.g., rate limiting counters):
  - Use anonymized or non-sensitive identifiers.
  - Avoid storing raw PII.

Cache access:

- Must require authentication and authorization at infrastructure level.
- Must be restricted to backend services.

---

## Operational Considerations

- Redis must be:
  - Monitored (memory usage, connection count, eviction stats).
  - Configured with appropriate eviction policy.
  - Deployed in a highly available configuration for production.

- Logs and metrics must track:
  - Cache hit rate
  - Cache miss rate
  - Error rate for cache operations

Cache failure requirements:

- System must remain functional (degraded performance, not broken).
- Backend logic must handle cache unavailability gracefully.

---

## Alternatives Considered

### 1. Pure In-Process Caching (Per Instance)

Rejected because:

- Inconsistent view across multiple backend instances
- Hard to manage in horizontal scaling
- Not resilient to process restarts

---

### 2. No Caching Initially

Rejected because:

- Scalability and performance would be limited.
- Would lead to ad-hoc, ungoverned caching in future.

A controlled caching strategy is preferable from the outset.

---

### 3. Tenant-Per-Redis-Instance

Rejected as initial strategy due to:

- Operational complexity (many Redis instances)
- Higher infrastructure cost
- Coordination difficulty

May be reconsidered for very large tenants via future ADR.

---

## Implementation Notes

- Use Django’s cache framework with Redis backend where appropriate.
- For application-level caching:
  - Wrap repository or service calls in dedicated cache helpers.
- Use clear key namespaces, e.g.:
  - `app:{env}:{tenant_id}:{resource_type}:{id}`

- Instrument caching with observability:
  - Add metrics for hit/miss.
  - Add structured logs when useful for debugging.

---

## Compliance Requirements

Any change to caching strategy that involves:

- New cache backend
- Different tenant isolation mechanism
- Caching of security-sensitive data
- Introduction of write-through or write-behind caches

Must be documented in a new ADR and reviewed.

---

## Review Trigger

This ADR must be reviewed if:

- Cache usage becomes a major performance bottleneck.
- Read/write patterns change significantly.
- Per-tenant performance isolation becomes critical.
- Multi-region deployments are introduced.

---

## Relationship to Other ADRs

- ADR-001: Multi-Tenancy Isolation Strategy
- ADR-002: Database Engine Strategy
- ADR-003: JWT Signing & Key Rotation Strategy

Caching must always respect:

- Tenant isolation (ADR-001)
- Source-of-truth semantics (DB remains authoritative)
- Security constraints defined in the security model.