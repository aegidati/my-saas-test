# ADR-001: Multi-Tenancy Isolation Strategy

---

## Status

Accepted

---

## Context

The system is designed as a multi-tenant SaaS platform.

Key architectural requirements:

- Strict tenant isolation
- Horizontal scalability
- Future database engine flexibility
- Operational simplicity
- Clear separation between tenant-scoped and global data
- Compatibility with Django ORM
- Support for evolving scale over time

The multi-tenancy model directly impacts:

- Database abstraction
- Repository design
- Authentication and authorization
- Logging and observability
- Testing strategy
- CI/CD behavior

A clear and explicit multi-tenancy isolation strategy must be defined early to prevent architectural drift.

---

## Decision

The system will adopt a **Row-Level Isolation Strategy with Explicit Tenant Context Enforcement**.

### Core principles:

1. Each tenant-scoped table includes a `tenant_id` field.
2. All repository operations require explicit tenant context.
3. Tenant scoping is enforced in the Infrastructure layer.
4. Tenant resolution occurs at request boundary (middleware/API layer).
5. Cross-tenant queries are forbidden unless explicitly defined.
6. No implicit global tenant state is allowed.

This approach is chosen as the initial strategy.

---

## Rationale

### Advantages

- Operational simplicity (single database instance possible).
- Easier to scale initially.
- Compatible with Django ORM without heavy customization.
- Lower infrastructure overhead compared to DB-per-tenant.
- Simplifies CI/CD and migrations.
- Simplifies observability and metrics aggregation.

### Trade-offs

- Requires strict discipline to avoid cross-tenant leaks.
- All queries must enforce tenant filtering.
- Larger shared tables over time.

The risk of cross-tenant access is mitigated through:

- Repository abstraction
- Tenant Context enforcement
- Automated testing
- Explicit architectural rules

---

## Alternatives Considered

### 1. Database-per-Tenant

Pros:
- Strong physical isolation
- Reduced cross-tenant risk

Cons:
- Operational complexity
- Complex migrations
- Higher infrastructure cost
- Harder horizontal scaling

Rejected due to operational overhead at current system stage.

---

### 2. Schema-per-Tenant

Pros:
- Logical isolation
- Reduced cross-tenant risk

Cons:
- Migration complexity
- Tooling friction
- Harder local development setup

Rejected for simplicity and early-stage scalability reasons.

---

### 3. Hybrid Model

Pros:
- Flexibility at scale

Cons:
- Increased complexity
- Harder mental model

Deferred for future consideration.

---

## Consequences

### Positive

- Clear repository design requirements
- Strong alignment with layered architecture
- Predictable behavior
- Easier onboarding
- Lower initial infrastructure cost

### Negative

- Requires rigorous code discipline
- Tenant filtering must never be bypassed
- Performance tuning may be required at scale

---

## Implementation Notes

- All tenant-scoped models must include `tenant_id`.
- Repository interfaces must require tenant context where applicable.
- Tests must explicitly validate cross-tenant protection.
- Logging must include `tenant_id`.
- Observability metrics may include tenant dimension internally.
- API must validate tenant claim consistency.

---

## Compliance Requirements

Any change to multi-tenancy strategy must:

- Create a new ADR
- Explain migration strategy
- Define backward compatibility plan
- Be reviewed before implementation

Multi-tenancy violations are considered critical defects.

---

## Review Date

To be reviewed when:

- System reaches significant scale
- Enterprise isolation requirements change
- Migration to multi-database architecture is considered