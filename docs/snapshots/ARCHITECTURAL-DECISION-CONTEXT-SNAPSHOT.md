# ARCHITECTURAL DECISION CONTEXT SNAPSHOT

## Purpose

This file is a compact architectural memory snapshot.

It is designed to:

- Re-establish architectural context in future sessions.
- Prevent drift from accepted decisions.
- Provide continuity when resuming work.

It does not replace ADRs, governance, operations, or architecture documents.

---

## Authority Reminder

When conflicts exist, apply the documented hierarchy used across repository governance:

1. ADR documents
2. Definition of Done
3. Prompt Governance Convention
4. STEP operational documents and operations playbooks
5. Architecture documents
6. Operational prompts
7. Snapshots

---

## System Overview

Current documented platform context:

- Fullstack SaaS platform
- Multi-tenant
- Monorepo
- Backend: Django
- Web: React
- Mobile: React Native

Layered architecture:

- Domain
- Application
- Infrastructure
- Interfaces

---

## ADR Coverage (Defined ADRs)

The system currently defines the following Architectural Decision Records (ADR-001…ADR-021).

Each ADR’s **status** (Proposed, Accepted, Superseded, etc.) is defined only in its own ADR document under `docs/adr` and that is the authoritative source for its current state.

This snapshot lists the ADRs for orientation and coverage only, without redefining their status.

- ADR-001 — Multi-Tenancy Isolation Strategy
- ADR-002 — Database Engine Strategy
- ADR-003 — JWT Signing & Key Rotation Strategy
- ADR-004 — Caching Strategy
- ADR-005 — API Rate Limiting Strategy
- ADR-006 — Background Job Processing Strategy
- ADR-007 — Feature Flag & Runtime Configuration Strategy
- ADR-008 — Audit Logging & Compliance Strategy
- ADR-009 — Horizontal Scaling & Load Balancing Strategy
- ADR-010 — Data Governance & Retention Policy
- ADR-011 — Event-Driven Architecture Strategy
- ADR-012 — Distributed Tracing Strategy
- ADR-013 — API Versioning & Backward Compatibility Strategy
- ADR-014 — Advanced Secret Management Strategy
- ADR-015 — Error & Exception Handling Strategy
- ADR-016 — Testing Strategy
- ADR-017 — Dependency & Package Management Strategy
- ADR-018 — Migration & Schema Evolution Policy
- ADR-019 — Observability & Logging Contract
- ADR-020 — Code Style & Formatting Governance
- ADR-021 — Project Initialization & Validation Policy

---

## ADR Index Reference

The complete structured overview of all ADR documents is available in:

docs/adr/ADR-INDEX.md

This index must always reflect the full set of ADR-001…ADR-021 (and any future ADRs).

Snapshot must remain aligned with docs/adr/ADR-INDEX.md at all times.

---

## Documented STEP State

Current operational STEP documents present in repository:

- STEP-00 — Development Environment Baseline
- STEP-01 — Monorepo Bootstrap
- STEP-01A — Documentation Alignment
- STEP-02 — Infrastructure Baseline
- STEP-03 — Authentication Skeleton
- STEP-04 — Multi-Tenant Infrastructure Layer
- STEP-05 — Repository & Service Pattern Foundation
- STEP-06 — Testing Infrastructure & Quality Gates

Scope ownership and exclusions are defined by STEP documents and STEP-RESPONSIBILITY-MATRIX.

---

## Architectural Invariants (Derived from ADRs)

1. Tenant isolation is mandatory.
2. Database remains the source of truth.
3. Cross-layer shortcuts are not allowed.
4. Secrets must not be hardcoded.
5. Structural changes require ADR governance.

---

## Resume Guidance

To resume architecture work in a new session:

1. Load this snapshot.
2. Load relevant ADRs and STEP document.
3. Continue from the next planned operational step or approved feature step.