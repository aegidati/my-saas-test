# ADR-012 — Distributed Tracing Strategy

## Status
Proposed

---

## Context

The platform is a horizontally scalable, multi-tenant SaaS system with:

- Stateless web layer
- Background job processing
- Event-driven architecture
- Audit logging
- Centralized rate limiting
- Redis-backed caching
- Feature flag system

Asynchronous workflows, background jobs, and event-driven flows introduce:

- Multi-hop execution paths
- Cross-layer invocation chains
- Retry complexity
- Partial failures

Structured logs alone are insufficient to:

- Trace a request across services
- Correlate background jobs to originating requests
- Diagnose latency bottlenecks
- Debug distributed failures

A Distributed Tracing strategy is required.

---

## Decision

We adopt a request-correlated distributed tracing strategy based on:

- Global `request_id`
- Global `trace_id`
- Optional `span_id`
- OpenTelemetry-compatible design
- Structured JSON logging integration

Initial implementation:

- Correlation ID propagation across:
  - Web layer
  - Background jobs
  - Event handlers
- Trace metadata included in logs

Future-ready for:

- OpenTelemetry exporters
- Jaeger / Tempo / Datadog / similar systems

---

## Trace Model

### Request Scope

Each incoming HTTP request must generate or accept:

- `trace_id`
- `request_id`

If not provided by upstream:

- Generate new IDs at API gateway/web layer.

These IDs must:

- Be immutable for request lifetime.
- Be included in all logs.
- Be propagated to background jobs.

---

### Background Jobs

When enqueueing a job:

- Include `trace_id`
- Include `request_id` (if applicable)
- Include `tenant_id`

Worker must:

- Rehydrate tracing context.
- Continue trace.

No background job may run without trace metadata.

---

### Event-Driven Flows

When emitting integration events:

- Include `trace_id`
- Include event metadata
- Preserve correlation across boundaries

Event handlers must:

- Propagate trace context.
- Never drop correlation IDs.

---

## Architectural Placement

### Domain Layer

- Must not know about tracing.
- Remains pure.

---

### Application Layer

- Responsible for:
  - Passing tracing metadata.
  - Preserving correlation across workflows.
  - Attaching context to async tasks.

---

### Infrastructure Layer

- Implements tracing middleware.
- Injects trace IDs into logs.
- Integrates OpenTelemetry SDK (future).
- Exports spans (optional future phase).

---

## Observability Integration

Tracing must integrate with:

- Structured logs
- Metrics
- Background job monitoring
- Event outbox processing

We must be able to answer:

- Which request triggered this job?
- Which tenant experienced this failure?
- Which service caused latency?
- Where did retry loops occur?

---

## Multi-Tenancy Considerations

Tracing must include:

- `tenant_id` in structured log context.
- No cross-tenant trace leakage.
- No mixing of tenant context within spans.

Tenant context remains isolated.

---

## Security Constraints

- Trace payload must not include secrets.
- No PII embedded in spans.
- Tracing storage must respect retention policy (ADR-010).
- Trace data access restricted to privileged roles.

---

## Performance Constraints

Tracing must:

- Add minimal overhead.
- Avoid synchronous blocking.
- Avoid heavy span generation for trivial flows.

Sampling strategy (future-ready):

- Sample low-priority requests.
- Always trace:
  - Errors
  - Slow requests
  - Security-related operations.

---

## Consequences

### Positive

- Easier debugging of async flows.
- Correlated request-to-job tracking.
- Improved production diagnostics.
- Enterprise-grade observability.

### Negative

- Increased implementation complexity.
- Storage cost for trace data.
- Potential overhead if misconfigured.

---

## Architectural Invariants Compliance

This ADR must respect:

1. Tenant isolation is mandatory.
2. No business logic in tracing layer.
3. Structured logging discipline.
4. Database remains source of truth.
5. Background job integration preserved.

---

## Final Decision Statement

The system adopts a request-correlated distributed tracing strategy with trace propagation across web, background jobs, and event flows, designed for OpenTelemetry compatibility and strict tenant isolation.