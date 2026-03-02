# ADR-011 — Event-Driven Architecture Strategy

## Status
Proposed

---

## Context

The platform is a multi-tenant SaaS system with:

- Strict tenant isolation
- PostgreSQL as source of truth
- Redis-backed caching
- Centralized rate limiting
- Background jobs (Celery + Redis)
- Immutable audit logging
- Feature flags
- Horizontal scaling
- Data governance and retention policies

As the system grows, synchronous request/response patterns become insufficient for:

- Cross-bounded-context communication
- Decoupled domain workflows
- Integrations with external systems
- Reactive UX features (notifications, updates)
- Analytics and reporting pipelines

We need a strategy for:

- Emitting domain events
- Handling application/integration events
- Ensuring reliability and idempotency
- Preserving tenant isolation
- Avoiding tight coupling between services/modules

An Event-Driven Architecture (EDA) strategy is required.

---

## Decision

We adopt a **layered Event-Driven Architecture** based on:

1. **Domain Events** — raised inside the Domain layer.
2. **Application Events** — orchestrated in the Application layer.
3. **Integration Events** — used for external systems and cross-service communication.

Initial implementation uses:

- PostgreSQL Outbox pattern for persistence of integration events.
- Celery + Redis for event dispatch and asynchronous handling.

Future-ready path:

- Ability to introduce a dedicated message broker (e.g., Kafka) without breaking domain contracts.

Database remains the source of truth.

---

## Event Types & Responsibilities

### 1. Domain Events

Examples:

- `UserRegistered`
- `TenantCreated`
- `SubscriptionUpgraded`
- `InvoicePaid`

Characteristics:

- Defined in Domain layer.
- Represent business facts.
- Pure data structures (no infrastructure concerns).
- Raised by domain entities/aggregates.

Domain events must not know:

- Celery
- Redis
- Message brokers
- HTTP

---

### 2. Application Events

Examples:

- `SendWelcomeEmail`
- `RecalculateTenantQuota`
- `GenerateInvoicePdf`
- `SyncTenantToExternalCrm`

Characteristics:

- Defined in Application layer.
- Orchestrate side effects triggered by Domain Events.
- Map domain events to concrete workflows.
- May enqueue background jobs (ADR-006).

---

### 3. Integration Events

Examples:

- `TenantSyncedToExternalCrm`
- `PaymentReceivedFromProvider`
- `WebhookDelivered`

Characteristics:

- Used for communication with external systems.
- Persisted via Outbox pattern.
- Dispatched asynchronously.
- May have versioned schemas.

Integration events must be tenant-aware and idempotent.

---

## Architectural Placement

### Domain Layer

- Defines Domain Event types.
- Raises events as part of domain operations.
- No knowledge of event bus implementation.

---

### Application Layer

- Subscribes to Domain Events (within same process boundary).
- Translates Domain Events into Application/Integration Events.
- Orchestrates workflows and background jobs.

---

### Infrastructure Layer

- Implements event bus abstraction.
- Handles:
  - Outbox persistence
  - Celery task dispatch
  - External message broker integration (future)
- Provides adapters for:
  - Publishing events
  - Consuming events

---

### Interface Layer

- May expose events via:
  - Webhooks
  - SSE / WebSocket gateways (future)
- Must not contain event logic beyond forwarding.

---

## Multi-Tenancy Rules

Event-driven flows must strictly preserve tenant isolation.

Rules:

1. Every event payload must include `tenant_id` (except purely system-level events).
2. Event handlers must reconstruct explicit Tenant Context.
3. No cross-tenant events allowed.
4. Cache keys used in handlers must include `tenant_id`.
5. Outbox entries must be indexed by `tenant_id`.

Tenant isolation is mandatory, even at event layer.

---

## Reliability Strategy

To avoid lost events and broken workflows:

- Use Outbox pattern for Integration Events:
  - Events are stored in DB within same transaction as domain changes.
  - A background job (ADR-006) reads the outbox and dispatches events.
- Ensure at-least-once delivery.
- Enforce idempotent event handlers.

Idempotency techniques:

- Idempotency keys.
- Handler-level deduplication.
- Safe reprocessing.

---

## Ordering & Consistency

Invariants:

- Domain operations and event persistence must be atomic.
- Events must not be emitted for failed transactions.
- Ordering is guaranteed per aggregate/tenant only where required.

For critical workflows:

- Handlers must not assume global ordering.
- Where strict ordering is needed, design explicit domain constraints.

---

## Event Schema & Versioning

Event contracts must be:

- Explicit
- Versioned
- Backward-compatible when possible

Strategy:

- Include `event_type`, `version`, `occurred_at` fields.
- Avoid breaking changes:
  - Additive changes preferred.
  - For breaking changes, introduce new event type or version.

Consumers must tolerate unknown optional fields.

---

## Observability & Monitoring

We must monitor:

- Event publishing failures
- Outbox backlog size
- Handler error rate
- Event processing latency
- Redelivery/retry counts

Alerts required for:

- Outbox congestion
- Persistent handler failures
- Significant retry storms

Audit logging (ADR-008) may record:

- Critical event emission
- Integration failures
- Manual replays

---

## Security Constraints

- Event payloads must not contain secrets.
- No JWTs or raw tokens in events.
- Sensitive fields must be minimized and, if needed, sanitized.
- Access to event logs/outbox is restricted to privileged roles.

---

## Initial Implementation Strategy

Phase 1 — Internal EDA:

- Introduce Domain Event types.
- Implement in-process dispatch inside Application layer.
- Use Celery for async Application Event handling where needed.

Phase 2 — Integration Events:

- Implement Outbox table in PostgreSQL.
- Implement dispatcher worker using Celery.
- Add robust logging, metrics, and retries.

Phase 3 — External Broker (Optional):

- Introduce message broker (e.g., Kafka) as transport for Integration Events.
- Keep domain and application layers unchanged.
- Migrate Infrastructure adapters only.

---

## Consequences

### Positive

- Decoupled modules and workflows.
- Easier integration with external systems.
- Better scalability for complex workflows.
- Clear separation between domain facts and side effects.
- Foundation for real-time features and analytics.

### Negative

- Increased architectural complexity.
- Harder debugging (async flows).
- Need for strong observability and monitoring.
- Potential risk of eventual consistency surprises.

---

## Architectural Invariants Compliance

This ADR must respect:

1. Tenant isolation is mandatory.
2. Database remains source of truth.
3. Background jobs (ADR-006) are preferred for async work.
4. No cross-layer shortcuts (Domain unaware of infrastructure).
5. Structured logging and audit logging (ADR-008) preserved.
6. Caching and rate limiting strategies (ADR-004, ADR-005) remain valid.

---

## Final Decision Statement

The system adopts a layered Event-Driven Architecture based on domain, application, and integration events, implemented initially via PostgreSQL Outbox + Celery/Redis, with strict tenant isolation, idempotent handlers, and full observability, while remaining future-ready for dedicated message brokers.