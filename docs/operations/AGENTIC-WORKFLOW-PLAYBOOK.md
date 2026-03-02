# AGENTIC WORKFLOW PLAYBOOK

## 1. Purpose

This playbook defines how to use:

- Planner Agent  
- Implementer Agent  
- Reviewer Agent  
- Documentation Guardian Agent  

to evolve the system in a controlled, ADR-driven, enterprise-grade way.

It applies to:

- Foundational STEPs (step-00 to step-06)  
- Feature STEPs (STEP-FEAT-XX)  
- Documentation alignment activities  

---

## 2. Agents and Responsibilities

### 2.1 Planner Agent

**Role**  
Designs the execution plan for a given STEP or Feature.

**Inputs**

- ADR documents (/adr)
- Architecture documentation (/architecture)
- STEP operational documents (/operations)
- Governance documents (/governance)
- Prompt Governance Convention (/prompts/governance)

**Responsibilities**

- Read all mandatory context declared in the operational prompt.
- Produce:
  - Current state assessment
  - Detailed execution plan
  - ADR compliance mapping
  - Risk assessment
  - Validation plan (tests + static checks)
  - Clear implementer handoff
- Must NOT modify code or documentation.

---

### 2.2 Implementer Agent

**Role**  
Applies the approved plan to the codebase.

**Responsibilities**

- Follow the Planner plan exactly.
- Respect:
  - ADRs
  - Architecture layering
  - Definition of Done
  - Prompt Governance Convention
- Run:
  - pytest
  - mypy
  - flake8
- Provide:
  - Files modified
  - Summary of changes
  - Mapping plan → implementation
  - Definition of Done self-check
  - Static analysis results
- Must NOT introduce new architectural decisions.

---

### 2.3 Reviewer Agent

**Role**  
Performs architectural and technical validation.

**Responsibilities**

- Validate against:
  - ADRs
  - STEP document
  - Definition of Done
  - Prompt Governance Convention
- Check:
  - Tenant isolation
  - Layer discipline
  - Security & secrets
  - Logging & error handling
  - Tests and static checks
- Produce structured review:
  - Executive summary
  - ADR compliance
  - Security review
  - Layering review
  - Quality gate verification
  - Required fixes
- Has authority to reject a STEP.

---

### 2.4 Documentation Guardian Agent

**Role**  
Ensures documentation integrity and prevents semantic drift.

**Scope**

- /adr
- /architecture
- /operations
- /prompts
- /governance
- /snapshots
- README.md and guides

**Operational Modes**

1. Planning Mode  
   Plans documentation alignment without modifying files.

2. Refactor Mode  
   Applies approved documentation refactor plan.

3. Review Mode  
   Reviews documentation consistency and drift.

**Hard Constraints**

- Must NOT change ADR decisions.
- Must NOT introduce new architectural rules.
- Must NOT modify application code.
- Must preserve authority hierarchy.

---

## 3. Authority Hierarchy

From strongest to descriptive:

1. ADR documents  
2. Definition of Done  
3. Prompt Governance Convention  
4. STEP operational documents and operations playbooks  
5. Architecture documents  
6. Operational prompts  
7. Snapshots  

No document may override an ADR.

---

## ADR Index Usage

The document `docs/adr/ADR-INDEX.md` provides the structured overview of all architectural decisions.

Before starting any:

- New STEP
- Feature STEP
- Major refactor
- Documentation alignment

The Planner and Documentation Guardian must consult docs/adr/ADR-INDEX.md to ensure:

- No decision duplication
- No architectural rule redefinition
- No missing ADR reference
- Full coverage awareness

docs/adr/ADR-INDEX.md is mandatory reading for all architectural evolution work.

---

## 4. Standard STEP Execution Workflow

Example: STEP-03 — Authentication Skeleton

### Phase 1 — Planning

1. Select Planner Agent.
2. Invoke:

   Plan docs/prompts/operational/step-03/STEP-03-authentication-skeleton-prompt.md

3. Review the plan.
4. Approve before proceeding.

---

### Phase 2 — Implementation

1. Select Implementer Agent.
2. Invoke:

   Execute approved plan for STEP-03.

3. Verify:
   - pytest
   - mypy
   - flake8
4. Confirm Definition of Done compliance.

---

### Phase 3 — Review

1. Select Reviewer Agent.
2. Invoke review including:
   - Relevant STEP document
   - Relevant ADRs
   - Definition of Done
   - Prompt Governance Convention

3. Address any P1 issues before marking complete.

---

## 5. Documentation Governance Workflow

Documentation alignment must follow this controlled process.

### Phase 1 — Planning

Invoke:

@documentation-guardian Plan documentation alignment for <scope>

The output must include:

- Executive summary
- File-by-file findings
- Prioritized plan (P1, P2, P3)

No file modifications in this phase.

---

### Phase 2 — Refactor

Invoke:

@documentation-guardian Refactor documentation according to approved plan

Rules:

- Do not alter ADR meaning.
- Convert normative architecture text into references such as:
   “As defined in the relevant ADR…”
- Add missing “Related ADRs” sections.
- Normalize structure and formatting.

Must provide:

- Files modified
- Nature of changes
- Confirmation that no new decisions were introduced

---

### Phase 3 — Review

For the first business feature in a generated project, Reviewer must verify ADR-021 compliance.

Invoke:

@documentation-guardian Review documentation changes

The output must validate:

- ADR integrity
- Architecture alignment
- STEP consistency
- Snapshot accuracy
- Governance compliance

---

## 6. Feature Workflow (STEP-FEAT-XX)

Before starting any business feature (FEAT-01+), STEP-FEAT-00 must be completed in compliance with ADR-021.

For each feature:

1. Create:
   - STEP-FEAT-XX document in /operations
   - Operational prompt in /prompts/operational

2. Execute:
   - Planner → Implementer → Reviewer

3. Periodically run:
   - Documentation Guardian full alignment check

---

## 7. Quality Gates (Mandatory)

For every significant STEP:

- pytest must pass
- mypy must pass
- flake8 must pass
- ADR compliance must hold
- Layering must remain intact
- Tenant isolation must not be violated

No STEP is considered DONE without satisfying all of the above.

---

## 8. System Integrity Principle

The four agents together guarantee:

- Architectural stability
- Controlled evolution
- Documentation coherence
- Enterprise-grade governance
- Long-term scalability

This playbook is mandatory for all architectural and feature evolution work.