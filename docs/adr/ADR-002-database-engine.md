# ADR-002: Database Engine Strategy

---

## Status

Accepted

---

## Context

The system is a multi-tenant SaaS platform with:

- Backend implemented in Python (Django)
- Repository-based database abstraction layer
- Row-level tenant isolation (see ADR-001)
- Requirement for long-term scalability
- Need for strong consistency guarantees
- Support for transactional operations
- Potential future need for read replicas and scaling strategies

The architecture also requires:

- Flexibility to evolve database engine in the future
- Clean separation between domain logic and persistence
- Compatibility with Django ORM
- Mature ecosystem and operational reliability

A primary database engine must be selected as the default engine.

---

## Decision

The system will adopt **PostgreSQL as the primary relational database engine**.

The architecture will remain:

- Database-engine abstracted at repository level
- ORM-based (Django ORM)
- Engine replacement-ready through abstraction layer

PostgreSQL is the officially supported engine for production environments.

---

## Rationale

### Advantages of PostgreSQL

- Strong ACID compliance
- Mature and battle-tested
- Excellent Django ORM compatibility
- Advanced indexing support
- JSON/JSONB support
- Strong multi-tenant row-level filtering capabilities
- Support for future features (partitioning, read replicas, extensions)
- Rich ecosystem and tooling

PostgreSQL aligns well with:

- Multi-tenant row-level strategy (ADR-001)
- Transactional domain operations
- Structured relational modeling
- Long-term scalability requirements

---

## Trade-offs

### Compared to MySQL

Pros over MySQL:

- Stronger JSON support
- More advanced indexing capabilities
- More predictable transactional behavior
- Better Django ecosystem support

Trade-off:

- Slightly steeper operational learning curve (acceptable)

---

### Compared to NoSQL (e.g., MongoDB)

Pros over NoSQL:

- Strong consistency
- Structured relational model
- Easier multi-tenant enforcement at row level
- Mature transactional semantics

Trade-off:

- Less flexible schema evolution (manageable through migrations)

NoSQL was rejected due to:

- Increased complexity in tenant isolation
- Weaker transactional guarantees for domain logic

---

## Alternatives Considered

### 1. MySQL

Rejected due to:

- Less advanced feature set for future scaling
- Less expressive JSON querying
- Slightly weaker ecosystem alignment with Django

---

### 2. SQLite (Production)

Rejected because:

- Not suitable for multi-tenant SaaS production scale
- Limited concurrency support
- Not horizontally scalable

SQLite may still be used for:

- Local development
- Lightweight test environments

---

### 3. Multi-Engine Support at Launch

Rejected because:

- Increases complexity prematurely
- Harder to test consistently
- Operational overhead without immediate benefit

Engine abstraction remains available, but only PostgreSQL is officially supported.

---

## Consequences

### Positive

- Clear operational standard
- Stable and scalable relational engine
- Strong ecosystem support
- Simplified DevOps pipeline
- Alignment with Django best practices

### Negative

- Lock-in risk if PostgreSQL-specific features are overused
- Requires disciplined abstraction to avoid tight coupling

---

## Implementation Notes

- Default Django configuration must target PostgreSQL.
- Migrations must be written in a PostgreSQL-compatible way.
- PostgreSQL-specific features may be used cautiously.
- Avoid vendor-specific extensions unless documented.
- Repository abstraction must prevent direct engine coupling.
- Connection pooling strategy must be defined in infrastructure.

Future enhancements may include:

- Read replicas
- Partitioning
- Connection pooling optimization
- Horizontal scaling strategies

---

## Compliance Requirements

If the database engine strategy changes:

- A new ADR must be created.
- Migration strategy must be defined.
- Data migration plan must be documented.
- Rollback strategy must be considered.

No silent engine replacement is allowed.

---

## Review Trigger

This ADR must be reviewed if:

- System scale significantly increases
- Multi-database or sharding strategy is introduced
- Regulatory requirements mandate isolation changes
- Migration to distributed SQL engines is considered

---

## Relationship to Other ADRs

- ADR-001: Multi-Tenancy Isolation Strategy
- Future ADRs may define:
  - Read replica strategy
  - Partitioning strategy
  - Connection pooling strategy
  - Caching layer introduction

Database strategy is foundational and must remain stable unless formally revised.