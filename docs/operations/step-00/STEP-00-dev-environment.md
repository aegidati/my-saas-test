# STEP-00 — Development Environment Baseline

## 1. Purpose

This STEP establishes a standardized development environment for this repository.

Its goals are:

- Ensure every developer works with the same baseline toolchain.
- Guarantee that Planner / Implementer / Reviewer workflows are reproducible.
- Make the Definition of Done (DoD) validation section executable.
- Align local development with architectural governance and ADR constraints.

This STEP focuses strictly on the local development environment.

It does NOT include:

- Cloud infrastructure
- CI/CD configuration
- Production deployments
- Database provisioning in staging/production

---

## 2. Scope

In scope:

- Python installation and configuration
- Virtual environment setup
- Backend development dependencies
- Static analysis tooling (mypy, flake8)
- VS Code workspace configuration
- GitHub Copilot & Agents readiness

Out of scope:

- Docker production setup
- Cloud provider configuration
- CI/CD pipelines
- External managed services

---

## 3. Prerequisites

Each developer MUST have installed:

- Git
- VS Code
- Python 3.11.x (recommended baseline)
- Node.js LTS (for future frontend STEPs)

Verification commands:

    git --version
    python --version
    node --version
    npm --version

Python MUST be version 3.11 or later.

---

## 4. Repository Setup

All commands below are executed from the repository root.

### 4.1 Create the Virtual Environment

    python -m venv .venv

### 4.2 Activate the Virtual Environment

Windows (PowerShell):

    .\.venv\Scripts\activate

Linux/macOS:

    source .venv/bin/activate

The shell prompt SHOULD show `(.venv)` when active.

### 4.3 Upgrade pip

    python -m pip install --upgrade pip

### 4.4 Install Backend Development Dependencies

Minimum required packages:

    python -m pip install django mypy flake8

Future STEPs will extend this dependency set.

---

## 5. VS Code Configuration

### 5.1 Select Python Interpreter

In VS Code:

1. Open Command Palette (Ctrl + Shift + P)
2. Select: "Python: Select Interpreter"
3. Choose the interpreter inside `.venv`

Windows:
    .venv\Scripts\python.exe

Linux/macOS:
    .venv/bin/python

This ensures:

- Extensions use the correct Python
- Linting and type-checking use the correct environment
- Django commands run inside the virtualenv

### 5.2 Recommended Extensions

Developers SHOULD install:

- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- GitHub Copilot
- GitHub Copilot Chat
- YAML
- Docker (optional)
- EditorConfig (optional)

---

## 6. Static Analysis Configuration

The repository MUST include in its root:

- `mypy.ini`
- `.flake8`

### 6.1 mypy Configuration Requirements

`mypy.ini` SHOULD:

- Enable strict_optional
- Enable check_untyped_defs
- Ignore missing imports for third-party libraries
- Disable the `import-untyped` error code to reduce Django noise
- Optionally specialize behavior for internal packages:
  - backend_core
  - domain
  - application
  - infrastructure
  - interfaces

### 6.2 flake8 Configuration Requirements

`.flake8` SHOULD:

- Set max-line-length (e.g., 100)
- Exclude common directories:
  - .git
  - __pycache__
  - .venv
  - dist
  - build
  - migrations
- Optionally ignore E203 and W503

---

## 7. Git Configuration

Developers MUST ensure global Git identity is configured:

    git config --global user.name
    git config --global user.email

If not set:

    git config --global user.name "Your Name"
    git config --global user.email "your@email.com"

---

## 8. Git Ignore Baseline

The repository MUST ignore:

- `.venv/`
- `__pycache__/`
- `.mypy_cache/`
- `.pytest_cache/`
- `*.pyc`

`.venv` MUST NOT be committed.

---

## 9. GitHub Copilot & Agents

This repository relies on agent-based workflows.

The following directory MUST exist:

    .github/agents/

Required agents:

- planner.agent.md
- implementer.agent.md
- reviewer.agent.md

These agents MUST align with:

- ADRs
- Prompt Governance Convention
- Agentic Workflow Playbook
- Definition of Done Template

GitHub Copilot Chat MUST be enabled for this repository.

---

## 10. Validation Commands

After completing environment setup, the following commands MUST run successfully:

    python -m mypy backend
    python -m flake8 backend

After STEP-01 (Monorepo Bootstrap):

    python backend/manage.py check

For every significant STEP, it is RECOMMENDED to run:

    python -m mypy backend
    python -m flake8 backend

New errors introduced by a STEP SHOULD be treated as P1 issues for that STEP.

---

## 11. Definition of Done — STEP-00 (Development Environment Baseline)

STEP-00 is considered complete when ALL the following conditions are met.

This STEP concerns ONLY the local development environment.
It does NOT validate repository structure or application code.

---

### 11.1 System-Level Requirements

- Python 3.11+ is installed and accessible via the `python` command.
- `python --version` returns a valid compatible version.
- Git is installed and accessible via the `git` command.
- Node.js is installed (for future frontend STEPs), but not required for backend validation.

---

### 11.2 Virtual Environment

- A local virtual environment named `.venv` exists in the repository root.
- The virtual environment can be activated successfully.
- When activated, `which python` (or equivalent) points to `.venv`.
- `python -m pip install --upgrade pip` executes without errors.

---

### 11.3 Development Dependencies

Inside the activated virtual environment:

- `django` can be installed successfully.
- `mypy` can be installed successfully.
- `flake8` can be installed successfully.
- No installation errors remain unresolved.

At this stage, no requirement exists regarding Django project structure.

---

### 11.4 Static Analysis Tooling Availability

The following commands execute without crashing:

    python -m mypy --version
    python -m flake8 --version

The purpose of this STEP is only to verify tool availability,
not to validate repository code structure.

Validation of repository folders (e.g. backend/) belongs to STEP-01.

---

### 11.5 VS Code Alignment

- VS Code is configured to use the `.venv` interpreter.
- The Python extension recognizes the virtual environment.
- GitHub Copilot and GitHub Copilot Chat are installed and enabled.

---

### 11.6 Git Hygiene

- `.venv/` is present in `.gitignore`.
- No virtual environment files are staged for commit.
- Git identity (user.name and user.email) is configured globally.

---

### 11.7 Governance Alignment

- The directory `.github/agents/` exists.
- planner.agent.md, implementer.agent.md, and reviewer.agent.md are present.
- No architectural files (ADR, architecture, governance) were modified in this STEP.

STEP-00 MUST NOT:

- Create backend folder structure.
- Create Django project files.
- Introduce database configuration.
- Modify ADR documents.
- Introduce production configuration.

Those responsibilities belong to STEP-01 and subsequent STEPs.

---

### 11.8 Explicit Exclusions

The following items are explicitly OUT OF SCOPE for STEP-00 and MUST NOT be treated as review failures:

- Missing `backend/` directory
- Missing `manage.py`
- Failing `python backend/manage.py check`
- Running `mypy` or `flake8` against non-existent project folders
- Database connectivity checks
- Docker configuration
- CI/CD pipeline execution

---

### 11.9 Final Acceptance Condition

STEP-00 is officially marked DONE when:

- The environment is reproducible on a clean machine.
- A developer can clone the repository and reach a working virtualenv state.
- Tooling (pip, mypy, flake8) is available and executable.
- No P1 issues remain open regarding local environment setup.

Once these conditions are satisfied, the project may proceed to:

STEP-01 — Monorepo Bootstrap.