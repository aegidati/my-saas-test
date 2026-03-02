# Agentic SaaS Platform

Enterprise-ready multi-tenant SaaS architecture built with:

- Backend: Django
- Web: React
- Mobile: React Native
- Monorepo structure
- ADR-driven governance
- Agent-based development workflow

---

# Architecture Philosophy

This project follows:

- Architecture First
- ADR-driven decision making
- Strict layer separation
- Multi-tenant isolation as invariant
- Static quality enforcement
- Agentic workflow (Planner / Implementer / Reviewer)

---

# Repository Structure

## Root

- backend/
- frontend/
- packages/
- docs/
- .github/

---

# Documentation Structure

All documentation is located in `/docs`.

docs/
├── architecture/     → Technical design (how the system works)
├── adr/              → Architectural Decision Records (normative)
├── operations/       → STEP execution documents
├── prompts/          → Governance and operational prompts
│   ├── governance/
│   └── operational/
├── governance/       → Definition of Done and process rules
├── guides/           → Developer guides
└── snapshots/        → Architectural memory snapshots

---

# Architectural Snapshot

Current architectural memory snapshot:

docs/snapshots/ARCHITECTURAL-DECISION-CONTEXT-SNAPSHOT.md

Use it to restore context in future sessions.

---

# How to Execute a STEP

1. Read the corresponding STEP document in:
   docs/operations/<step-folder>/

2. Invoke Planner:

   @planner Plan <path-to-operational-prompt.md>

3. Review and approve the plan.

4. Invoke Implementer.

5. Handoff to Reviewer:

   Review according to:
   - STEP Definition of Done
   - Relevant ADRs
   - Prompt Governance Convention

---

# Quality Gates

Before marking any STEP as DONE:

- mypy must pass
- flake8 must pass
- pytest must pass
- No ADR violations
- No layering violations

---

# Architectural Invariants

1. Tenant isolation is mandatory
2. No cross-layer shortcuts
3. No hardcoded secrets
4. No ORM in presentation layer
5. DB is source of truth
6. JWT must use RS256
7. Every structural change requires ADR

---

# Current Status

Foundational STEPs completed:

- STEP-00 to STEP-06

System is ready for feature development.