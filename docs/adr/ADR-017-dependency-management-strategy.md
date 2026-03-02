# ADR-017 — Dependency & Package Management Strategy

- Status: Accepted
- Date: 2026-02-26
- Authors: Architecture Team
- Related ADRs:
  - ADR-002 — Database Engine Strategy
  - ADR-009 — Horizontal Scaling Strategy
  - ADR-014 — Advanced Secret Management Strategy
  - ADR-016 — Testing Strategy

---

## 1. Context

The system depends on multiple external libraries across:

- Backend (Django, Redis, PostgreSQL drivers, JWT libraries)
- Frontend (React ecosystem)
- Mobile (React Native ecosystem)

Without a formal dependency policy:

- Security vulnerabilities may remain unnoticed.
- Upgrades may introduce breaking changes.
- Transitive dependencies may drift.
- CI builds may become non-reproducible.

This ADR defines how dependencies are selected, versioned, updated, and secured.

---

## 2. Decision

We adopt:

- Explicit version pinning.
- Deterministic builds.
- Controlled upgrade cycles.
- Automated vulnerability scanning.
- Minimal dependency philosophy.

---

## 3. Version Pinning Policy

- All backend dependencies MUST be pinned to exact versions.
- No wildcard versions allowed (e.g., django>=4.0 is forbidden).
- Lock files MUST be committed to the repository.
- Transitive dependency resolution must be deterministic.

Frontend and mobile dependencies must also use lock files.

---

## 4. Upgrade Strategy

Dependency updates must follow:

- Minor & patch updates: Allowed after testing.
- Major updates: Require explicit review.
- Major updates that impact architecture MUST trigger an ADR review.

Upgrade workflow:

1. Update dependency in isolated branch.
2. Run full CI suite.
3. Validate backward compatibility.
4. Merge only if no regressions detected.

---

## 5. Security & Vulnerability Management

- CI MUST include vulnerability scanning.
- High severity vulnerabilities MUST be addressed immediately.
- Critical vulnerabilities are P1 issues.
- Unmaintained libraries must be replaced.

Secrets must never be embedded in dependencies or config files.

---

## 6. Forbidden Practices

- Installing unused dependencies.
- Adding dependencies without justification.
- Using experimental or unmaintained libraries.
- Relying on transitive dependencies implicitly.

---

## 7. Consequences

Positive:
- Deterministic builds.
- Reduced supply-chain risk.
- Stable CI pipeline.

Trade-offs:
- Slightly slower upgrade cycles.
- Additional governance overhead.

Accepted due to enterprise requirements.