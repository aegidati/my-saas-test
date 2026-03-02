# Database Abstraction Architecture

---

## 1. Purpose

This document defines the database abstraction model for the system.

It specifies:

- How the application remains database-engine agnostic
- How persistence responsibilities are layered
- How repositories and adapters are structured
- How multi-tenancy interacts with persistence
- Constraints and prohibited patterns

This document complements:

- `ARCHITECTURE.md`
- `multi-tenancy.md`
- Relevant ADRs (e.g., DB engine choices, multi-tenancy strategy)

In case of conflict, ADRs prevail.

---

## 2. Goals

The database abstraction layer is designed to:

- Allow changing the underlying database engine (e.g., PostgreSQL, MySQL, etc.)
- Isolate domain and application logic from persistence details
- Support multi-tenant isolation strategies
- Provide a consistent repository interface across engines
- Minimize vendor lock-in
- Support evolution through ADR-controlled changes

Database abstraction is an architectural concern, not a convenience wrapper.

---

## 3. Layering and Responsibilities

The persistence model adheres to the layered architecture:

- **Domain layer**
  - Defines domain entities and aggregates
  - Contains no direct persistence logic
  - Is unaware of database engines and ORMs

- **Application layer**
  - Coordinates use cases
  - Interacts with repository interfaces
  - Does not know about concrete database engines

- **Infrastructure layer**
  - Implements repository interfaces
  - Encapsulates ORM usage and database specifics
  - Applies multi-tenancy scoping logic in coordination with `multi-tenancy.md`

Infrastructure is the only layer allowed to interact with the database driver/ORM.

---

## 4. Repository Pattern

### 4.1 Repository Interfaces

For each aggregate or persistence boundary, a repository interface must be defined at the application or domain boundary (depending on the design).

Characteristics:

- Expresses operations in domain terms (e.g., `find_active_by_tenant`, `save`, `delete`)
- Does not expose ORM or DB-specific types
- Returns domain models or dedicated DTOs/value objects

Repository interfaces must be:

- Stable
- Vendor-agnostic
- Tenant-aware where required

---

### 4.2 Repository Implementations

Repository implementations reside in the Infrastructure layer.

Responsibilities:

- Map between domain entities and persistence models
- Use the configured ORM/driver (e.g., Django ORM)
- Enforce tenant scoping as required by `multi-tenancy.md`
- Optimize queries while preserving contracts of the interface

Implementations must not:

- Be referenced directly from Domain or Presentation
- Leak ORM types or query sets outside Infrastructure
- Bypass tenant scoping logic

---

## 5. Django ORM Integration

The default persistence adapter uses **Django ORM**.

Guidelines:

- Django models reside in the Infrastructure layer (or a clear boundary module that is infrastructure-oriented).
- Domain models and Django models may be separate types.
- Mapping between domain and ORM entities must be explicit (mapping functions or mappers).
- Direct use of Django models in domain or application logic is discouraged and should be treated as an anti-pattern.

ORM-related details (fields, indexes, migrations) belong to Infrastructure.

---

## 6. Engine Abstraction

The system must support multiple database engines over time.

Design requirements:

- Repository interfaces must not assume features unique to a specific engine (unless clearly documented in ADRs).
- Engine-specific implementations can exist per repository (e.g., `PostgresUserRepository`, `MySQLUserRepository`), but must conform to the same interface.
- Runtime or configuration decides which implementation is active, based on:
  - Global configuration
  - Tenant configuration (for multi-tenant setups)
  - Environment (e.g., dev/staging/production)

Any engine-specific behavior must be:

- Encapsulated in Infrastructure
- Documented in ADRs if it affects behavior or constraints

---

## 7. Multi-Tenancy and Persistence

Persistence must comply with the multi-tenancy model defined in `multi-tenancy.md`.

Requirements:

- All repository operations must be tenant-aware when dealing with tenant-scoped data.
- Tenant context must be provided from the Application layer into Infrastructure.
- No repository is allowed to operate on tenant data without an explicit tenant scope, unless explicitly marked as global/system-wide.

Depending on the isolation strategy (database-per-tenant, schema-per-tenant, row-level):

- Database selection may change per tenant.
- Schema selection may change per tenant.
- Row-level filters must always apply tenant predicates.

No query is allowed to bypass tenant scoping logic.

---

## 8. Transactions

Transactions are managed in the Infrastructure layer.

Guidelines:

- Application layer may define transactional boundaries (e.g., “this use case is atomic”), but the implementation is delegated to Infrastructure.
- Transaction APIs exposed to Application must not expose engine-specific constructs.
- Nested transactions and transaction propagation semantics must be defined and documented in ADRs or a dedicated transaction strategy document.

Transactions must:

- Be tenant-aware
- Avoid cross-tenant operations inside a single transaction unless explicitly designed and justified

---

## 9. Migrations

Schema migrations are part of the Infrastructure layer.

Guidelines:

- Use migration tooling compatible with Django ORM (e.g., Django migrations).
- Migrations must respect the multi-tenancy strategy (e.g., apply per tenant DB, per schema).
- Backwards compatibility and data migration strategies must be documented in relevant ADRs.

Domain and Application layers must not be responsible for schema evolution logic.

---

## 10. Performance and Query Design

Persistence must:

- Avoid N+1 query patterns
- Use appropriate indexing strategies (documented where necessary)
- Limit data transfer from DB to application
- Use pagination and batching where required
- Consider engine-specific capabilities via Infrastructure abstractions

Any engine-specific optimization must:

- Remain within repository implementations
- Not change the observable behavior of the repository interface
- Be covered by tests

---

## 11. Testing Strategy

Testing levels:

- **Unit tests (Domain)**:
  - Must not depend on the database.
  - Must use in-memory/stand-in implementations of repositories if needed.

- **Integration tests (Infrastructure)**:
  - Validate repository behavior against a real or test database.
  - Ensure tenant scoping is enforced.
  - Validate engine-specific implementations behave consistently.

- **End-to-end tests**:
  - Validate persistence behavior across layers (Presentation → Application → Infrastructure).

Test configuration must allow:

- Running against a default DB engine locally
- Optionally running against multiple engines in CI (if supported and documented)

---

## 12. Prohibited Patterns

The following patterns are explicitly forbidden:

- Direct database access from Presentation layer
- Direct database access from Domain layer
- ORM usage outside Infrastructure
- Hardcoded engine-specific SQL in Application or Domain
- Skipping repository abstractions for “quick fixes”
- Tenant-unaware queries in multi-tenant data paths
- Storing engine-specific constructs in domain state

Any necessary deviation must be justified and approved via ADR.

---

## 13. Evolution Strategy

Database abstraction must evolve in a controlled way.

Changes that require ADRs:

- Introduction of a new database engine
- Significant change in repository interface contracts
- Changes in transaction semantics
- Changes in multi-tenancy isolation models impacting persistence

Goals during evolution:

- Preserve domain and application stability
- Limit changes to Infrastructure where possible
- Avoid large-scale rewrites by keeping abstractions clean

Database abstraction is a core architectural mechanism and must remain stable and deliberate.