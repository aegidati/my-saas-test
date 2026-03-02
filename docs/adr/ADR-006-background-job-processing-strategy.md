# ADR-006 — Background Job Processing Strategy

## Status
Proposed

---

## Context

The platform is a multi-tenant SaaS system with strict architectural layering and tenant isolation invariants.

As the system evolves, we require asynchronous processing for:

- Email dispatching
- Webhook delivery
- Report generation
- CSV imports
- Scheduled cleanup tasks
- Token pruning
- Audit aggregation
- Integration with external systems
- Event-driven workflows

Synchronous execution inside the request/response lifecycle would:

- Increase API latency
- Reduce scalability
- Risk timeout failures
- Break UX expectations

A centralized, scalable, and tenant-safe background job processing mechanism is required.

---

## Decision

We adopt a centralized background job processing architecture based on:

- Celery as task queue framework
- Redis as broker
- Redis as result backend (initially)
- Dedicated worker containers
- Optional Celery Beat for scheduled tasks

Workers are deployed independently from web containers.

---

## Architectural Placement

The background job system must respect strict layered architecture:

- Domain Layer  
  Contains pure business logic.  
  Must not depend on Celery or infrastructure concerns.

- Application Layer  
  Responsible for orchestrating job creation and coordination.

- Infrastructure Layer  
  Contains Celery adapters and task definitions.

- Interface Layer  
  API endpoints enqueue jobs but do not execute business logic directly.

Domain logic must never import Celery.

---

## Multi-Tenancy Enforcement

Tenant isolation is a critical architectural invariant.

Rules:

1. Every job payload must include `tenant_id`.
2. Worker must reconstruct explicit Tenant Context.
3. No job may access data without tenant scope.
4. Cache keys used in jobs must include `tenant_id`.
5. Retries must not violate tenant isolation.

Failure to include tenant context is considered a critical defect.

---

## Job Categories

### 1. Fire-and-forget
- Email sending
- Webhook dispatch
- Non-critical async logging

### 2. Long-running tasks
- CSV imports
- Report generation
- Aggregation jobs

### 3. Scheduled tasks
- Cleanup routines
- Expired token pruning
- Retention enforcement
- Audit compaction

---

## Idempotency Strategy

All background jobs must be idempotent.

Requirements:

- Safe retry execution
- Use of idempotency keys where applicable
- Exponential backoff retry strategy
- Maximum retry limit
- No duplicate side-effects

Future extension may introduce a dead-letter queue.

---

## Failure Handling

Failures are categorized as:

- Retryable (network, temporary external failure)
- Non-retryable (validation errors, invariant violations)

Each failure must:

- Produce structured JSON logs
- Include `tenant_id`
- Include `job_id`
- Include `request_id` if available

Silent failures are forbidden.

---

## Observability Requirements

Mandatory monitoring:

- Job execution duration
- Retry count
- Failure rate
- Queue length
- Worker health

Alerts required for:

- Retry storms
- Queue congestion
- Worker crashes

All dashboards must remain tenant-safe.

---

## Scaling Strategy

System must support horizontal scaling:

- Multiple worker replicas
- Separate queues:
  - default
  - heavy
  - scheduled
- Independent scaling of:
  - Web layer
  - Worker layer

Future evolution may introduce autoscaling based on queue length.

---

## Security Constraints

- No secrets embedded in tasks
- No tokens logged
- No sensitive payload exposure in logs
- Input validation before enqueue
- Redis access must be secured

---

## Deployment Model

Monorepo compliant structure:

backend/
  celery_app.py
  tasks/
  worker_entrypoint.py

Docker services:

- Web container
- Worker container
- Beat container (optional)

CI/CD must:

- Execute background job tests
- Support safe rollout
- Allow rollback strategy

---

## Consequences

### Positive

- Decoupling of API and heavy operations
- Improved UX
- Independent scalability
- Resilience via retries
- Foundation for event-driven architecture

### Negative

- Increased operational complexity
- Redis becomes critical dependency
- Monitoring becomes mandatory
- Risk of tenant leakage if improperly implemented

---

## Architectural Invariants Compliance

This ADR must respect:

1. Tenant isolation is mandatory.
2. Database remains source of truth.
3. No cross-layer shortcuts.
4. Structured logging required.
5. Observability discipline enforced.

---

## Final Decision Statement

The system adopts a Redis-backed Celery-based background job processing architecture with strict tenant isolation, idempotency enforcement, and full observability integration.