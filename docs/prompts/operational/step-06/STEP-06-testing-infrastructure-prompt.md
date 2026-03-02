# STEP-06 — Testing Infrastructure & Quality Gates
## Operational Prompt for Planner Agent

This document is a controlled operational prompt.

It MUST be used with the Planner Agent.

The Planner MUST:

- Respect all ADRs (001–020).
- Respect the Agentic Workflow Playbook.
- Respect Definition of Done — STEP-06.
- Enforce test pyramid discipline.
- Introduce quality gates without weakening architecture.

This STEP formalizes backend testing and static quality enforcement.

---

## 1. Mandatory Context to Read

Before generating the plan, you MUST read:

- docs/operations/step-06/STEP-06-testing-infrastructure.md
- docs/operations/step-05/STEP-05-repository-service-foundation.md
- docs/operations/step-04/STEP-04-multi-tenant-infrastructure.md
- docs/operations/step-03/STEP-03-authentication-skeleton.md
- docs/operations/step-02/STEP-02-infrastructure-baseline.md
- docs/adr/ (ADR-001 through ADR-020)
- docs/operations/AGENTIC-WORKFLOW-PLAYBOOK.md
- docs/operations/STEP-RESPONSIBILITY-MATRIX.md
- docs/governance/DEFINITION-OF-DONE-TEMPLATE.md

If any required file is missing, stop and report it.

---

## 2. Objective

Plan the execution of STEP-06.

Goals:

- Configure pytest and pytest-django.
- Define test directory structure.
- Configure isolated test database.
- Introduce unit, integration, and minimal system tests.
- Introduce quality gates:
  - mypy
  - flake8
  - Optional coverage threshold.
- Ensure tenant isolation and authentication are explicitly tested.

This STEP MUST NOT:

- Introduce new business features.
- Modify core architecture to simplify testing.
- Disable failing tests instead of fixing root causes.

---

## 3. Required Output Structure

Your output MUST include:

### 3.1 Current State Assessment

- Inspect current test setup (if any).
- Inspect presence of pytest.
- Inspect static tooling configuration.
- Identify gaps in coverage for:
  - JWT utilities.
  - Tenant isolation.
  - Repository enforcement.
  - Application services.

### 3.2 Testing Infrastructure Plan

Provide a structured plan covering:

- pytest configuration:
  - pytest.ini
  - DJANGO_SETTINGS_MODULE for tests
  - Test DB configuration
- Directory structure:
  - tests/unit/
  - tests/integration/
  - tests/system/
- Fixtures design:
  - Tenant fixture
  - User fixture
  - JWT fixture
- Static checks:
  - mypy execution strategy
  - flake8 enforcement
  - Optional coverage configuration

### 3.3 Test Pyramid Mapping

Explain how tests are distributed across:

- Unit tests (majority)
- Integration tests
- Minimal system tests

Clarify boundaries between categories.

### 3.4 ADR Compliance & Risk Analysis

Explicitly explain compliance with:

- ADR-016 (Test pyramid discipline).
- ADR-001 (Tenant isolation verification).
- ADR-003 (JWT validation tests).
- ADR-015 (Error contract validation).
- ADR-020 (Static quality gates).

Identify risks such as:

- Hidden cross-tenant access not tested.
- Tests accidentally using dev DB.
- Static analysis ignored.

### 3.5 Validation Plan

Explain how Definition of Done — STEP-06 will be validated:

- Successful pytest run.
- Static checks pass.
- Coverage report generated.
- Explicit tenant isolation test.

---

## 4. Constraints

- Test database MUST be isolated from dev/prod DB.
- No global state shortcuts for testing.
- No disabling mypy/flake8 to “make things pass”.
- No weakening of tenant enforcement for test convenience.
- Maintain strict layering discipline in tests.

---

## 5. Implementer Handoff (Mandatory)

Provide:

- Ordered implementation steps.
- pytest configuration details.
- Example minimal test cases for:
  - JWT validation.
  - Tenant isolation.
  - `/auth/me` endpoint.
- Static check execution instructions.
- Reminder to:
  - Run pytest.
  - Run mypy.
  - Run flake8.
  - Confirm isolation behavior.

---

## 6. Invocation Pattern

Invoke as:

@planner Plan docs/prompts/operational/step-06/STEP-06-testing-infrastructure-prompt.md