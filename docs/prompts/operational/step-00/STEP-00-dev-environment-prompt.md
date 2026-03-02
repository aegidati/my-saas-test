# STEP-00 — Development Environment Setup (Operational Prompt)

## Agent: Planner

This document is a self-contained operational manifest.

When invoked by the Planner Agent, you MUST:

1. Read all required context files listed below.
2. Produce a structured execution plan.
3. NOT modify code.
4. Respect Prompt Governance Convention and Definition of Done.
5. Prepare a structured handoff for the Implementer.

---

# 1. Required Context (MANDATORY READ)

Before generating the plan, you MUST read:

- docs/operations/step-00/STEP-00-dev-environment.md
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md
- docs/prompts/governance/PROMPT-GOVERNANCE-CONVENTION.md
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md

If any file is missing, explicitly state it.

---

# 2. Objective

Establish a complete, reproducible local development environment according to STEP-00 specifications.

This includes:

- Python baseline validation
- Virtual environment creation
- Installation of required dev dependencies
- Static analysis configuration validation
- VS Code interpreter alignment
- Validation command execution
- Git ignore verification

This STEP does NOT include:

- Docker
- Cloud infrastructure
- CI/CD
- Production configuration

---

# 3. Execution Plan Requirements

You MUST structure the output as follows:

## 1. Environment Verification
- Validate Python version
- Validate Git
- Validate Node (optional future steps)

## 2. Virtual Environment Setup
- Create .venv
- Activate
- Upgrade pip

## 3. Dependency Installation
- Install django
- Install mypy
- Install flake8

## 4. Static Analysis Configuration
- Validate presence of mypy.ini
- Validate presence of .flake8
- Explain expected configuration alignment

## 5. VS Code Alignment
- Python interpreter selection
- Extension recommendations

## 6. Validation Commands
- python -m mypy backend
- python -m flake8 backend

## 7. Definition of Done Verification
Map results against DoD checklist for STEP-00.

---

# 4. Constraints

You MUST:

- Avoid modifying architectural files.
- Avoid introducing new dependencies.
- Avoid changing ADR files.
- Keep scope strictly aligned with STEP-00.

If a requested action conflicts with governance or DoD, highlight the issue and propose a compliant alternative.

---

# 5. Implementer Handoff Block

At the end of the plan, provide:

- Ordered actionable checklist
- Commands to execute
- Expected outputs
- Common failure cases and resolutions

This plan must be executable by a developer without ambiguity.

---

# Invocation Pattern

Invoke with:

@planner Plan docs/prompts/operational/step-00/STEP-00-dev-environment-prompt.md

This prompt must work without additional instructions.