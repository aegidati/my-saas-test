# STEP Responsibility Matrix

## 1. Purpose

This document defines responsibility boundaries between operational STEPs.

It prevents:

- Scope overlap
- Cross-STEP validation conflicts
- Reviewer ambiguity
- Architectural drift

Each STEP MUST respect its defined scope.
Cross-STEP validation is a governance violation.

---

## 2. STEP Scope Matrix

| STEP     | Primary Responsibility | Explicit Exclusions | Related ADRs |
|-----------|-----------------------|--------------------|--------------|
| STEP-00 | Local development environment baseline | Repository structure, Django bootstrap, backend code validation | ADR-002 (baseline awareness), ADR-014 |
| STEP-01 | Monorepo structure and Django bootstrap | Feature logic, auth, caching, rate limiting | ADR-001, ADR-002, ADR-009, ADR-014 |
| STEP-02 | Infrastructure baseline (DB wiring, settings discipline) | Business logic, feature endpoints | ADR-002, ADR-009, ADR-014 |
| STEP-03 | Authentication core implementation | Authorization logic, feature flags | ADR-003 |
| STEP-04 | Multi-tenant infrastructure layer | Tenant onboarding flows, billing/quotas, frontend/mobile integration | ADR-001, ADR-002, ADR-010 |
| STEP-05 | Repository & service pattern foundation | New business features, tenant onboarding flows, CI/CD changes | ADR-001, ADR-002, ADR-017 |
| STEP-06 | Testing infrastructure & quality gates | Frontend tests, E2E browser tests, performance/load testing | ADR-016, ADR-001, ADR-003, ADR-015, ADR-020 |
| STEP-07 | Background job processing | API feature logic | ADR-006 |
| STEP-08 | Feature flag system | Business logic refactoring | ADR-007 |
| STEP-09 | Audit logging & compliance | Domain logic changes | ADR-008 |
| STEP-10 | Scaling validation & stateless discipline | Feature changes | ADR-009 |
| STEP-11 | Data governance & retention enforcement | Infrastructure redesign | ADR-010 |
| STEP-12 | Event-driven integration layer | Domain rewrites | ADR-011 |
| STEP-13 | Distributed tracing integration | Feature refactor | ADR-012 |
| STEP-14 | Advanced secret management hardening | Feature logic | ADR-014 |

This table may evolve as the architecture matures.

---

## 3. Responsibility Principles

### 3.1 Single Responsibility per STEP

Each STEP MUST:

- Have a single dominant architectural objective.
- Avoid introducing unrelated concerns.
- Avoid anticipating future STEPs prematurely.

---

### 3.2 Cross-STEP Isolation

A STEP MUST NOT:

- Validate responsibilities of a future STEP.
- Introduce logic owned by another STEP.
- Modify ADR documents unless explicitly required.

Violations are P1 governance issues.

---

### 3.3 ADR Alignment

Each STEP MUST:

- Explicitly state which ADRs are involved.
- Explicitly state which ADRs are not yet applicable.
- Avoid implicit architectural decisions.

If a STEP introduces a new structural decision,
a new ADR is required.

---

## 4. Reviewer Enforcement Rule

The Reviewer Agent MUST:

- Validate only the responsibilities defined for the current STEP.
- Ignore missing components belonging to future STEPs.
- Flag scope creep as P1.
- Flag incomplete scope fulfillment as P1.

---

## 5. Evolution Rule

When a new STEP is introduced:

- It MUST be added to this matrix.
- It MUST declare its related ADR coverage.
- It MUST define its own Definition of Done.

A STEP not registered in this matrix is considered unofficial.