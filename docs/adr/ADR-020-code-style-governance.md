# ADR-020 — Code Style & Formatting Governance

- Status: Accepted
- Date: 2026-02-26
- Authors: Architecture Team
- Related ADRs:
  - ADR-016 — Testing Strategy
  - ADR-017 — Dependency Management Strategy

---

## 1. Context

Code style inconsistency leads to:

- Review friction
- Merge conflicts
- Reduced maintainability

---

## 2. Decision

We adopt:

Backend:
- Black (formatter)
- isort (import sorting)
- flake8 (linting)
- mypy (static typing)

Frontend:
- Prettier
- ESLint

Formatting MUST be automated.

---

## 3. CI Enforcement

CI MUST fail if:

- Formatting rules are violated.
- Linting errors exist.
- Static typing errors exist.

---

## 4. Forbidden Practices

- Manual formatting overrides.
- Ignoring lint errors without justification.
- Committing code that fails static checks.

---

## 5. Consequences

Positive:
- Consistent codebase.
- Faster reviews.
- Reduced technical debt.

Trade-offs:
- Slight setup overhead.