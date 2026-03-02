# ADR INDEX

## Purpose

This document provides a structured overview of all Architectural Decision Records (ADR) defined in the system.

Each ADR is authoritative only in its own document located in the `/adr` folder.

This index:

- Provides thematic grouping
- Helps developers quickly navigate architectural decisions
- Prevents decision duplication
- Supports documentation alignment
- Enables snapshot verification

---

## ADR Authority Rule

If any conflict arises between documents:

ADR documents always prevail over:

- Architecture documents
- Operations / STEP documents
- Prompts
- Snapshot
- Playbook

This index does not override ADR content.
It only organizes and summarizes them.

---

# Core System Architecture

- **ADR-001 — Multi-Tenancy Isolation Strategy**  
  Defines tenant isolation model, row-level separation, and invariants.

- **ADR-002 — Database Engine Strategy**  
  Defines primary database engine and abstraction rules.

- **ADR-003 — JWT Signing and Key Rotation Strategy**  
  Defines authentication token strategy and cryptographic rules.

- **ADR-013 — API Versioning & Backward Compatibility Strategy**
  Defines versioning model and backward compatibility rules.

- **ADR-004 — Caching Strategy**  
  Defines Redis usage and cache authority rules.

- **ADR-005 — API Rate Limiting Strategy**  
  Defines centralized rate limiting and tenant-aware enforcement.

- **ADR-021 — Project Initialization & Validation Policy**
  Defines mandatory validation (STEP-FEAT-00) before starting business features in generated projects.

---

# Scalability & Runtime Behavior

- **ADR-006 — Background Job Processing Strategy**  
  Defines async processing and worker separation.

- **ADR-007 — Feature Flag & Runtime Configuration Strategy**  
  Defines feature toggling and runtime configuration control.

- **ADR-009 — Horizontal Scaling & Load Balancing Strategy**  
  Defines stateless service rules and scaling model.

- **ADR-011 — Event-Driven Architecture Strategy**  
  Defines internal event patterns and decoupling model.

- **ADR-012 — Distributed Tracing Strategy**  
  Defines observability tracing boundaries.

---

# Data Governance & Compliance

- **ADR-008 — Audit Logging & Compliance Strategy**  
  Defines audit logging scope and immutability principles.

- **ADR-010 — Data Governance & Retention Policy**  
  Defines retention rules and lifecycle constraints.

- **ADR-018 — Database Migration & Schema Evolution Policy**  
  Defines version-controlled schema changes.

---

# Security & Governance

- **ADR-014 — Advanced Secret Management Strategy**  
  Defines secret handling and environment segregation.

- **ADR-015 — Error & Exception Handling Strategy (API Error Contract)**  
  Defines error layering and exposure rules.

- **ADR-019 — Observability & Logging Contract**  
  Defines structured logging requirements.

- **ADR-020 — Code Style & Formatting Governance**  
  Defines static analysis and formatting enforcement.

- **ADR-017 — Dependency & Package Management Strategy**  
  Defines dependency constraints and update discipline.

---

# Testing & Quality

- **ADR-016 — Testing Strategy & Test Pyramid**  
  Defines testing pyramid and validation principles.

---

# Coverage Summary

The ADR set covers:

- Multi-tenancy
- Security
- Authentication
- Database
- Caching
- Rate limiting
- Background jobs
- Event-driven patterns
- Observability
- Scaling
- Data governance
- Migration
- Testing
- Dependency control
- Code style governance

Architectural coverage is complete for foundational SaaS architecture.

---

# Maintenance Rules

When introducing a new architectural rule:

1. A new ADR must be created.
2. This ADR-INDEX must be updated.
3. Snapshot must reflect the new ADR.
4. Architecture documents must reference it.

This ensures decision traceability and prevents drift.