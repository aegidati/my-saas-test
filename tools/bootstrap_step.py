#!/usr/bin/env python
"""
Bootstrap script for creating new STEP operational and prompt files.

Usage:
    python tools/bootstrap_step.py 02 "Infrastructure Baseline"

This will generate:
    docs/operations/step-02/STEP-02-infrastructure-baseline.md
    docs/prompts/operational/step-02/STEP-02-infrastructure-baseline-prompt.md
"""

import sys
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def slugify(name: str) -> str:
    """Convert STEP name to a filesystem-friendly slug."""
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "step"


def make_step_number(raw: str) -> str:
    """Normalize step number to zero-padded 2-digit string."""
    try:
        n = int(raw)
    except ValueError:
        raise SystemExit(f"Invalid STEP number '{raw}'. Must be an integer.")
    if n < 0:
        raise SystemExit("STEP number must be non-negative.")
    return f"{n:02d}"


def build_operations_content(step_num: str, step_name: str, slug: str) -> str:
    step_id = f"STEP-{step_num}"
    title = f"{step_id} — {step_name}"
    return f"""# {title}

## 1. Purpose

This document defines the operational contract for {step_id}.

It specifies:

- The goal and scope of this STEP.
- The responsibilities and constraints.
- The validation requirements.
- The STEP-specific Definition of Done.

This STEP MUST be executed under the Agentic Workflow governance
(Planner → Implementer → Reviewer) and MUST NOT violate existing ADRs.

---

## 2. Scope

### 2.1 In Scope

- TODO: describe what this STEP is responsible for.

### 2.2 Out of Scope

- TODO: explicitly list what this STEP must NOT do.
- Any responsibility owned by other STEPs MUST be listed here.

---

## 3. Architectural Context

This STEP MUST be consistent with:

- ADR-001..ADR-014 (where applicable).
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md

You MUST explicitly list which ADRs are relevant for this STEP:

- TODO: e.g. ADR-002, ADR-009, ADR-014

Any new structural decision introduced by this STEP
MUST be covered by a new ADR.

---

## 4. Execution Requirements

The Planner Agent SHOULD produce a plan that includes:

- A clear sequence of operations for this STEP.
- Any required changes to the codebase or docs.
- Validation steps (commands, checks).
- Explicit references to relevant ADRs and governance docs.

The Implementer Agent SHOULD:

- Follow the approved plan.
- Keep changes strictly within the STEP scope.
- Avoid scope creep into responsibilities of other STEPs.
- Produce a DoD self-assessment at the end.

---

## 5. Constraints

During this STEP, the following constraints MUST be respected:

- No violation of existing ADRs.
- No bypass of architectural layering.
- No introduction of secrets in the codebase.
- No cross-STEP responsibilities.

If any constraint conflicts with the required changes,
a new ADR MUST be proposed before proceeding.

---

## 6. Validation

Validation MUST include:

- TODO: list validation commands and checks for this STEP.
  - For example:
    - python -m mypy backend
    - python -m flake8 backend
    - python backend/manage.py check

- Manual review of:
  - Architectural alignment
  - Security implications
  - Multi-tenancy impact
  - Observability hooks (if relevant)

Validation for this STEP MUST NOT include checks
belonging to future or previous STEPs, as defined in
docs/operations/STEP-RESPONSIBILITY-MATRIX.md.

---

## 7. Definition of Done — {step_id}

{step_id} is considered complete when ALL the following conditions are met.

### 7.1 STEP-Specific Outcomes

- TODO: list the concrete outcomes that must exist after this STEP.
  - e.g. directory structure, configuration files, interfaces, etc.

### 7.2 Technical Validation

- All validation commands defined in Section 6 succeed.
- No new P1 issues have been introduced by this STEP.
- Any remaining warnings are documented and classified as P2 (non-blocking).

### 7.3 Governance Alignment

- No ADR violations have been detected.
- No architectural layering violations exist.
- No secrets are committed to the repository.
- No responsibilities of other STEPs have been taken over.

### 7.4 Documentation

- This document ({step_id}-{slug}.md) is up to date.
- Relevant sections of:
  - STEP-RESPONSIBILITY-MATRIX.md
  - OPERATIONAL-PROMPT-SEQUENCE.md
have been updated, if needed.

{step_id} MUST NOT be marked as DONE
until all the above conditions are satisfied.
"""


def build_prompt_content(step_num: str, step_name: str, slug: str) -> str:
    step_id = f"STEP-{step_num}"
    title = f"{step_id} — {step_name}"
    operations_path = f"docs/operations/step-{step_num}/{step_id}-{slug}.md"
    return f"""# {title} (Operational Prompt)

## Agent: Planner

This document is a self-contained operational prompt
for the Planner Agent.

When invoked, you MUST:

1. Read all required context files.
2. Produce a structured execution plan for {step_id}.
3. Respect the Prompt Governance Convention.
4. NOT modify code directly.
5. Prepare a clear handoff for the Implementer Agent.

---

## 1. Required Context (MANDATORY READ)

Before generating the plan, you MUST read:

- {operations_path}
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md

If any file is missing, explicitly state it
and stop the plan generation.

---

## 2. Objective

Plan the execution of {step_id} — {step_name}, ensuring:

- Scope is strictly aligned with the STEP document.
- No responsibilities of other STEPs are taken.
- All relevant ADRs are considered.
- Validation and Definition of Done are explicitly addressed.

---

## 3. Plan Structure Requirements

Your output MUST be structured as follows:

### 3.1 Context Summary

- Brief summary of what {step_id} is supposed to achieve.
- List of relevant ADRs and governance docs.

### 3.2 Execution Phases

- Phase 1: Analysis / Preparation
- Phase 2: Implementation actions
- Phase 3: Validation actions
- Phase 4: Documentation updates (if any)

Each phase MUST contain:

- Ordered steps.
- Files to touch.
- Commands to run (if any).
- Expected outcomes.

### 3.3 Validation Plan

- List all validation commands required.
- Map them to the Definition of Done items.
- Explicitly mention success criteria.

### 3.4 Risks & Open Questions

- List potential risks.
- List assumptions.
- List open questions (if any).

---

## 4. Constraints

You MUST:

- Keep the plan within the STEP scope.
- Avoid proposing changes to ADRs unless explicitly required.
- Avoid cross-layer shortcuts or anti-patterns.
- Avoid introducing secrets or environment-specific hacks.

If a requested change conflicts with governance,
highlight the conflict and propose a compliant alternative.

---

## 5. Implementer Handoff

At the end of the plan, provide a concise
Implementer Handoff section:

- Short description of {step_id} goal.
- Bullet list of implementation steps.
- Bullet list of validation commands.
- Reference to the Definition of Done section in the STEP document.

---

## 6. Invocation Pattern

This prompt is intended to be invoked as:

@planner Plan docs/prompts/operational/step-{step_num}/{step_id}-{slug}-prompt.md

It MUST work without additional instructions.
"""


def main(argv: list[str]) -> None:
    if len(argv) < 3:
        print("Usage: python tools/bootstrap_step.py <STEP_NUMBER> \"STEP Name\"")
        sys.exit(1)

    raw_step = argv[1]
    step_name = " ".join(argv[2:]).strip()
    step_num = make_step_number(raw_step)
    slug = slugify(step_name)

    operations_dir = REPO_ROOT / "docs" / "operations" / f"step-{step_num}"
    prompts_dir = REPO_ROOT / "docs" / "prompts" / "operational" / f"step-{step_num}"

    operations_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    operations_file = operations_dir / f"STEP-{step_num}-{slug}.md"
    prompt_file = prompts_dir / f"STEP-{step_num}-{slug}-prompt.md"

    if operations_file.exists():
        print(f"[WARN] Operations file already exists: {operations_file}")
    else:
        operations_content = build_operations_content(step_num, step_name, slug)
        operations_file.write_text(operations_content, encoding="utf-8")
        print(f"[OK] Created operations file: {operations_file}")

    if prompt_file.exists():
        print(f"[WARN] Prompt file already exists: {prompt_file}")
    else:
        prompt_content = build_prompt_content(step_num, step_name, slug)
        prompt_file.write_text(prompt_content, encoding="utf-8")
        print(f"[OK] Created prompt file: {prompt_file}")


if __name__ == "__main__":
    main(sys.argv)