# ADR-016 — Testing Strategy & Test Pyramid

- Status: Accepted
- Date: 2026-02-26
- Authors: Architecture Team
- Related ADRs:
  - ADR-001 — Multi-Tenancy Isolation Strategy
  - ADR-002 — Database Engine Strategy
  - ADR-003 — JWT Signing & Key Rotation Strategy
  - ADR-013 — API Versioning & Backward Compatibility Strategy
  - ADR-015 — Error & Exception Handling Strategy
  - ADR-009 — Horizontal Scaling & Load Balancing Strategy

---

## 1. Context

The system is a multi-tenant SaaS platform with:

- Versioned APIs
- Structured error contracts
- Strict layering discipline
- Horizontal scaling constraints
- Security-sensitive authentication logic

Without a formal testing strategy:

- Backward compatibility may break silently.
- Multi-tenant isolation may regress.
- Error contract stability cannot be guaranteed.
- Refactoring becomes dangerous.
- CI/CD cannot enforce architectural integrity.

This ADR defines the official testing strategy,
coverage model, and enforcement rules.

---

## 2. Decision

We adopt a **Test Pyramid strategy**
with strict separation between:

- Unit tests
- Integration tests
- API contract tests
- End-to-end tests (minimal but strategic)

The system MUST prioritize:

- Fast deterministic unit tests.
- Explicit multi-tenant validation.
- Backward compatibility enforcement per API version.
- Error contract stability.

---

## 3. Test Pyramid Model

### 3.1 Unit Tests (Foundation Layer)

Scope:
- Domain layer logic
- Pure application services
- Validation functions
- Stateless utilities

Requirements:
- No database dependency.
- No external network calls.
- No framework-specific logic when possible.
- High coverage expected (critical business logic > 90%).

Unit tests MUST validate:
- Business rules.
- Edge cases.
- Error raising behavior.
- Deterministic outputs.

---

### 3.2 Integration Tests

Scope:
- Application + infrastructure interaction.
- Database persistence.
- Repository layer.
- Transaction behavior.
- Background job execution.

Requirements:
- Use a real test database.
- Isolate tenant contexts.
- Validate migrations consistency.

Integration tests MUST validate:
- Multi-tenant isolation enforcement.
- Repository behavior.
- Database constraints.
- Transaction rollbacks.
- Failure scenarios.

---

### 3.3 API Contract Tests

Scope:
- HTTP endpoints.
- Request/response schema.
- Error contract (ADR-015).
- Versioning rules (ADR-013).

Requirements:
- Validate JSON schema structure.
- Validate mandatory fields.
- Validate error codes stability.
- Validate HTTP status mapping.

Contract tests MUST ensure:
- Backward compatibility within a major version.
- No breaking change without version bump.
- Error response format compliance.

Removing or altering response fields within a version
without updating the major version is forbidden.

---

### 3.4 End-to-End (E2E) Tests

Scope:
- Critical user flows.
- Authentication.
- Tenant-specific flows.
- Rate limiting and authorization.

E2E tests MUST:
- Be minimal.
- Cover only business-critical paths.
- Avoid duplicating unit test logic.
- Validate real-world integration across layers.

E2E tests are slower and must remain limited in number.

---

## 4. Multi-Tenancy Testing Requirements (ADR-001 Alignment)

All relevant test layers MUST include tenant isolation validation.

Tests MUST verify:

- Data created under tenant A is not accessible to tenant B.
- Queries always include tenant context.
- No cross-tenant leakage in API responses.
- Error responses do not expose tenant identifiers.

Multi-tenant isolation regressions are P1 issues.

---

## 5. API Versioning Testing Requirements (ADR-013 Alignment)

For each API major version:

- A dedicated regression test suite MUST exist.
- Contract tests MUST lock response schema.
- Removing fields within the same version is forbidden.
- Introducing breaking changes requires:
  - New version namespace.
  - New test suite for that version.

Backward compatibility is enforced by tests, not documentation alone.

---

## 6. Error Contract Testing (ADR-015 Alignment)

Tests MUST verify:

- Error JSON structure.
- Mandatory fields presence.
- Stable error codes.
- No sensitive information leakage.
- Proper HTTP status code mapping.

Changing error format without version bump is forbidden.

---

## 7. Horizontal Scaling & Statelessness Testing (ADR-009 Alignment)

Tests MUST ensure:

- No reliance on in-memory state across requests.
- No file-based local persistence.
- No server-side session coupling.
- Background jobs are idempotent when required.

Integration tests SHOULD simulate multiple requests
to detect state leakage.

---

## 8. Coverage Policy

Coverage expectations:

- Domain layer: High (> 90% recommended).
- Application layer: High (> 85% recommended).
- Infrastructure layer: Moderate but meaningful.
- API layer: Contract tests required for all public endpoints.

Coverage percentage is not sufficient alone.
Quality and critical path validation take precedence.

---

## 9. CI Enforcement

Continuous Integration MUST:

- Run all unit tests.
- Run integration tests.
- Run API contract tests.
- Fail on regression.
- Fail on unhandled exceptions.
- Fail on multi-tenant isolation violations.

CI SHOULD:

- Enforce coverage thresholds.
- Prevent merging if contract tests fail.
- Prevent merging if backward compatibility is broken.

---

## 10. Test Data Policy

Test data MUST:

- Be deterministic.
- Avoid production data.
- Avoid hardcoded secrets.
- Explicitly assign tenant context.
- Clean up after execution.

Factories or fixtures SHOULD be used.

---

## 11. Forbidden Testing Anti-Patterns

The following are forbidden:

- Relying solely on manual testing.
- Testing only via E2E tests.
- Skipping contract tests for new endpoints.
- Disabling tests to pass CI.
- Writing tests that depend on execution order.
- Using production databases in tests.

---

## 12. Consequences

### Positive

- Safe refactoring.
- Enforced backward compatibility.
- Multi-tenant safety.
- Reduced regression risk.
- Predictable evolution of APIs.

### Trade-offs

- Increased development time.
- CI runtime cost.
- Maintenance overhead for versioned API tests.

These trade-offs are accepted to ensure architectural stability.

---

## 13. Implementation Notes

- Use a clear test directory structure aligned with layers.
- Separate test categories (unit, integration, contract).
- Introduce version-aware test folders for API versions.
- Use fixtures for tenant setup.
- Centralize error contract validation utilities.
- Integrate coverage checks into CI.

All new features MUST include appropriate tests
before being considered complete.