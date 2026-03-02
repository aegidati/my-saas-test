# Testing Strategy

---

## 1. Purpose

This document defines the testing strategy for the system.

It specifies:

- Test levels and responsibilities
- How tests map to the layered architecture (Domain, Application, Infrastructure, Interfaces)
- How to test multi-tenancy, security, and configuration
- How web and mobile clients are tested
- Expectations for coverage, automation, and CI integration
- Prohibited testing patterns

This document complements:

- ARCHITECTURE.md  
- backend-structure.md  
- multi-tenancy.md  
- database-abstraction.md  
- authentication.md  
- authorization.md  
- security-model.md  
- configuration.md  
- ci-cd.md (for pipeline integration)

In case of conflict, ADRs prevail.

---

## 2. Testing Goals

The testing strategy aims to:

- Validate that the system behaves correctly under expected and unexpected conditions
- Prevent regressions when evolving the system
- Ensure tenant isolation and security rules are correctly enforced
- Provide fast feedback to developers
- Support safe refactoring
- Enable continuous delivery

Tests must be:

- Deterministic
- Repeatable
- Automated where possible
- Maintainable and readable

---

## 3. Test Levels

The system uses multiple test levels:

1. Unit tests
2. Integration tests
3. API / Contract tests
4. End-to-end (E2E) tests
5. Performance and load tests (where needed)
6. Security and negative tests

Each level has a distinct purpose and scope.

---

## 4. Layer-to-Test Mapping

The layered architecture maps to tests as follows:

- Domain → unit tests
- Application → integration / service tests
- Infrastructure → integration tests with real/test dependencies
- Interfaces (API) → API and contract tests
- Frontend (Web and Mobile) → unit/component, integration, and E2E tests

Tests should be located under backend/tests, frontend/web/tests, and frontend/mobile/tests (or equivalent paths).

---

## 5. Domain Layer Testing (Backend)

Scope:

- Domain entities
- Value objects
- Domain services
- Invariants and business rules

Characteristics:

- Pure unit tests
- No database
- No Django
- No external services

Expectations:

- High coverage for critical domain logic
- Tests focus on behavior and invariants, not implementation details
- Edge cases and invalid states must be explicitly tested

---

## 6. Application Layer Testing (Backend)

Scope:

- Use cases
- Application services
- Orchestration logic
- Authorization checks at application level

Characteristics:

- Integration-style tests (but still primarily in-process)
- May use fake or in-memory implementations of repositories
- No reliance on external systems unless necessary

Expectations:

- Verify that use cases:
  - Enforce authorization
  - Enforce tenant rules
  - Coordinate domain and infrastructure contracts correctly
- Verify failure paths (unauthorized, invalid input, missing resources)

---

## 7. Infrastructure Layer Testing (Backend)

Scope:

- Repository implementations
- Database interactions
- Multi-tenant routing and scoping
- External service integrations (email, payment, etc.)

Characteristics:

- Integration tests using:
  - Real or test database
  - Test doubles for external services or sandbox environments
- Tests must validate actual persistence behavior

Expectations:

- Repository tests must:
  - Enforce tenant filters
  - Enforce constraints from database-abstraction.md
- External integration tests must:
  - Validate error handling
  - Avoid hitting production services

---

## 8. Interfaces / API Testing (Backend)

Scope:

- HTTP endpoints (REST/GraphQL)
- Request/response mapping
- Authentication integration
- Basic authorization validation at boundary
- Error handling format

Characteristics:

- API tests using HTTP-level clients (Django test client, DRF API client, etc.)
- Validate:
  - Status codes
  - Response schemas
  - Error payloads
  - Authentication/authorization behavior

Expectations:

- No business rules are re-tested here in detail (already covered by Domain/Application).
- Focus on:
  - Endpoint contracts
  - Correct use of HTTP semantics
  - Correct mapping of exceptions to error responses

---

## 9. Frontend Web Testing (React)

Scope:

- Components
- Hooks and state management
- API client behavior
- Routing
- Critical flows (login, logout, multi-tenant navigation)

Test types:

- Unit tests:
  - Components and hooks in isolation
- Integration tests:
  - Components with state and API mocking
- E2E tests (together with backend, where applicable):
  - Browser-based tests for critical journeys

Expectations:

- Minimal reliance on implementation details (DOM structure may change).
- Focus on user-visible behavior.
- Security-sensitive flows (auth, logout, error display) must be covered.

---

## 10. Frontend Mobile Testing (React Native)

Scope:

- Screens and navigators
- Hooks and state management
- API client behavior
- Authentication flows and secure storage interactions

Test types:

- Unit tests:
  - Components, hooks, and pure logic
- Integration tests:
  - Screens with mocked navigation and APIs
- E2E tests (device or emulator-based), where applicable:
  - Critical flows (login, logout, tenant switch, main user flows)

Expectations:

- Tests must not depend on production services.
- Security-related logic (token storage, error handling) must be tested.
- Deep linking / OAuth callback handling should be covered where implemented.

---

## 11. Multi-Tenancy Testing

Multi-tenancy must be explicitly tested at multiple levels:

- Domain:
  - Tenant-specific business rules (if applicable)
- Application:
  - Enforcement of tenant restrictions
- Infrastructure:
  - Repository filters and DB routing
- Interfaces / API:
  - Request with tenant context vs mismatched tenant claims

Test cases must include:

- Valid tenant access
- Cross-tenant access attempts (must be denied)
- Missing tenant context
- Incorrect tenant in JWT vs resolved tenant

Multi-tenant bugs are considered critical.

---

## 12. Authentication and Authorization Testing

Authentication tests:

- Valid login (web and mobile)
- Invalid credentials
- Expired tokens
- Tampered tokens
- Token refresh flow (if implemented)
- Logout behavior

Authorization tests:

- Allowed actions for roles and policies
- Forbidden actions (negative tests)
- Tenant-scoped roles and permissions
- API responses for unauthorized vs unauthenticated requests

Authorization must be tested at Application level and validated at API level.

---

## 13. Configuration and Security Testing

Configuration testing:

- Startup fails when mandatory configuration is missing or invalid
- Environment-specific settings behave as expected
- Misconfiguration scenarios are handled safely

Security testing:

- Negative tests for:
  - Access without authentication
  - Access with invalid token
  - Access to resources in another tenant
- Tests for:
  - Input validation
  - Output encoding (for critical paths)
  - Protection of sensitive data in responses

Automated security scanning (SAST/DAST) may be integrated via CI as defined in ci-cd.md.

---

## 14. Test Data Management

Guidelines:

- Test data must be deterministic and controlled.
- Fixtures or factory libraries may be used.
- Multi-tenant tests must use:
  - Multiple tenants with clear separation
  - Users assigned to specific tenants and roles
- Sensitive real-world data must never be used in tests.

Test data sets must be:

- Small enough for fast execution
- Representative enough to cover typical and edge cases

---

## 15. Performance and Load Testing

Performance and load tests are recommended for:

- Critical endpoints (e.g., heavily used APIs)
- Multi-tenant scenarios under load
- Operations with significant database impact

Guidelines:

- Run in non-production environments.
- Use synthetic data.
- Monitor:
  - Response times
  - Error rates
  - Resource utilization

Performance regressions must be treated as serious issues.

---

## 16. CI Integration

Test execution must be integrated into CI pipelines (see ci-cd.md).

Guidelines:

- Unit tests must run on every change.
- Integration and API tests should run on main branches and before releases.
- E2E tests may run on a schedule or pre-release environment.
- Pipelines must fail if critical tests fail.

Fast feedback is preferred; tests may be split into stages (smoke vs full suite).

---

## 17. Coverage Expectations

Coverage must focus on critical logic, not arbitrary percentages.

Guidelines:

- Domain and Application layers: high coverage for business rules.
- Infrastructure: coverage for data access and multi-tenant constraints.
- Interfaces: coverage for critical endpoints and error handling.

Coverage thresholds may be defined in ADR or CI configuration.

---

## 18. Prohibited Testing Patterns

The following are strictly discouraged or forbidden:

- Tests that depend on order or shared mutable state.
- Tests that depend on external, unstable services (without isolation).
- Usage of production credentials or production data in tests.
- Tests that rely on sleep-based timing instead of proper synchronization.
- Tests that replicate implementation instead of validating behavior.
- Tests that bypass authentication/authorization for convenience.

Any required exception must be justified and documented.

---

## 19. Evolution Strategy

The testing strategy may evolve as:

- New features and domains are added
- New testing tools are introduced
- CI/CD capabilities are extended

Changes that significantly alter:

- Supported test levels
- Critical coverage areas
- How multi-tenancy or security are tested

Must be documented and, when appropriate, captured in ADRs.

The goal is to continuously improve test quality while keeping feedback fast and reliable.