# Definition of Done (DoD) Template

## Purpose

This document defines the mandatory completion criteria for any:

- Operational STEP (e.g., STEP-01, STEP-02)
- New feature
- Refactor
- Infrastructure change
- Architectural extension

No change is considered complete until this checklist is satisfied.

Authority hierarchy: ADR > Definition of Done > Prompt Governance Convention > Operations > Architecture > Operational prompts > Snapshots.

---

# 1. Governance Requirements

## 1.1 Planner Phase Completed
- [ ] Planner Agent produced structured plan.
- [ ] Plan referenced relevant ADRs.
- [ ] Non-goals clearly defined.
- [ ] Reviewer checklist included.

## 1.2 Implementer Phase Completed
- [ ] Changes implemented strictly according to plan.
- [ ] Scope not expanded beyond plan.
- [ ] Summary of modified files provided.

## 1.3 Reviewer Phase Completed
- [ ] Reviewer Agent executed.
- [ ] Structured compliance report produced.
- [ ] All P1 issues resolved.
- [ ] No open architectural violations remain.

---

# 2. ADR Compliance

All relevant ADRs must be marked compliant.

## Mandatory ADR Checks

### ADR-001 — Multi-Tenancy Isolation
- [ ] No cross-tenant data exposure.
- [ ] No global mutable tenant state.
- [ ] tenant_id enforced where required.

### ADR-002 — Database Strategy
- [ ] ORM used correctly.
- [ ] No engine-specific leakage outside infrastructure.
- [ ] Any bootstrap exceptions documented.

### ADR-009 — Horizontal Scaling
- [ ] No reliance on in-memory sessions.
- [ ] No process-level business state.
- [ ] Stateless discipline preserved.

### ADR-014 — Secret Management
- [ ] No hardcoded secrets.
- [ ] No fallback insecure secrets.
- [ ] Production requires environment-based secrets.
- [ ] No sensitive data logged.

---

## Conditional ADR Checks (if applicable)

### ADR-003 — JWT
- [ ] RS256 used.
- [ ] Key rotation supported.
- [ ] No key exposure.

### ADR-006 — Background Jobs
- [ ] Idempotent jobs.
- [ ] Proper retry strategy.
- [ ] No business logic in workers.

### ADR-011 — Event-Driven Architecture
- [ ] Domain events correctly defined.
- [ ] No cross-layer leakage.
- [ ] Outbox pattern respected (if applicable).

### ADR-012 — Distributed Tracing
- [ ] request_id propagated.
- [ ] tenant_id included in logs/trace (if applicable).

---

# 3. Layer Discipline Verification

- [ ] Domain does NOT import Django/infrastructure.
- [ ] Infrastructure does NOT import interfaces.
- [ ] Interfaces contain no business logic.
- [ ] No circular dependencies.
- [ ] Application layer orchestrates correctly.

---

# 4. Security & Configuration

- [ ] No credentials committed.
- [ ] No secret values in settings.
- [ ] Environment variables required where appropriate.
- [ ] Secure defaults enforced.
- [ ] Fail-fast for missing production secrets.

---

# 5. Documentation & Alignment

- [ ] STEP document updated (if applicable).
- [ ] ADR references accurate.
- [ ] Any exception to ADR documented.
- [ ] Prompt operational files aligned.
- [ ] Naming consistent with repository structure.

---
# 6. Automated & Manual Validation

For every significant STEP (or feature), it is RECOMMENDED to run both
static type checking and linting as part of the validation process.

- [ ] `python backend/manage.py check` passes.
- [ ] Tests pass (if present).
- [ ] No runtime errors on startup.
- [ ] CI (if configured) passes.
- [ ] No new warnings introduced that indicate regressions.

### 6.1 Static Type Checking (mypy)

- [ ] `mypy` has been executed on the relevant Python packages (e.g. `backend/`).
- [ ] No new mypy errors have been introduced by this STEP.
- [ ] Any remaining mypy warnings are either:
  - known and documented, or
  - explicitly out of scope for this STEP.

Recommended command:

---

# 7. Scope Control

- [ ] No hidden features added.
- [ ] No unrelated refactors introduced.
- [ ] No silent architectural changes.
- [ ] All changes traceable to plan.

---

# 8. Final Approval State

One of the following must be explicitly declared:

- [ ] ✅ Done — Fully compliant
- [ ] ⚠️ Done with documented non-blocking P2 improvements
- [ ] ❌ Not Done — Blocking violations remain

The state must be documented in the STEP file or PR description.

---

# Definition of Done Declaration Block

To be appended at the end of a STEP document:

---

## Definition of Done — Status

Overall Status: <✅ Done / ⚠️ Done with P2 / ❌ Not Done>

Reviewer Confirmation:
- ADR compliance: <status>
- Layer discipline: <status>
- Security compliance: <status>

Remaining Improvements (if any):
- <List P2 items>

Approved by:
- Planner Agent
- Implementer Agent
- Reviewer Agent

---

# Enforcement Clause

If any P1 issue is discovered after marking Done:

1. Reopen cycle.
2. Re-run Reviewer.
3. Apply fixes via Implementer.
4. Revalidate DoD.

---

### ADR-021 Enforcement

If this is the first business feature in a generated project,
Reviewer must confirm:

- STEP-FEAT-00 has been completed.
- ADR-021 compliance is satisfied.
- No business feature started before technical validation.

---

Done status may be revoked if violations are found.