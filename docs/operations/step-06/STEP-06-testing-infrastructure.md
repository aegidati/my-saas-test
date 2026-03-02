# STEP-06 — Testing Infrastructure & Quality Gates

## 1. Purpose

This STEP establishes the **testing infrastructure and quality gates** required to ensure:

- Architectural integrity.
- Tenant isolation guarantees.
- Authentication correctness.
- Layering discipline.
- Long-term maintainability.

It formalizes:

- Test structure.
- Test pyramid alignment.
- Test database configuration.
- Coverage requirements.
- Static analysis integration (mypy, flake8).

No new business features are introduced.

This STEP makes the system safe to evolve.

---

## 2. Scope

### 2.1 In Scope

Backend testing infrastructure only:

- pytest (or equivalent test runner) configuration.
- Test directory structure.
- Test database configuration.
- Unit tests.
- Integration tests.
- Multi-tenant isolation tests.
- Authentication tests.
- Static analysis enforcement (mypy, flake8).
- Coverage reporting.

### 2.2 Out of Scope

- Frontend testing (separate future STEP).
- E2E browser tests.
- CI/CD pipeline automation (may reference but not implement here).
- Performance testing.
- Load testing.

---

## 3. Architectural Context

This STEP MUST comply with:

- ADR-016 — Testing Strategy & Test Pyramid  
  (Unit > Integration > Minimal system tests.)

- ADR-001 — Multi-Tenancy Isolation Strategy  
  (Explicit tests must validate isolation.)

- ADR-003 — JWT Signing & Key Rotation Strategy  
  (Token validation must be tested.)

- ADR-015 — Error & Exception Handling Strategy  
  (Error format consistency must be tested.)

- ADR-020 — Code Style & Formatting Governance  
  (mypy + flake8 as quality gates.)

This STEP validates the correctness of:

- STEP-02 — Infrastructure Baseline
- STEP-03 — Authentication Skeleton
- STEP-04 — Multi-Tenant Infrastructure
- STEP-05 — Repository & Service Pattern

---

## 4. Testing Philosophy (Applied from ADR-016)

The project follows the **Test Pyramid**:

### 4.1 Unit Tests (Majority)

- Test:
  - Domain logic.
  - Repository logic (isolated).
  - JWT utilities.
  - Tenant resolution logic.
- Must:
  - Be fast.
  - Avoid network.
  - Avoid unnecessary DB usage.

### 4.2 Integration Tests (Moderate)

- Test:
  - API endpoints.
  - Middleware interactions.
  - DB + repository behavior.
- Must:
  - Use test database.
  - Validate tenant isolation.
  - Validate authentication flow.

### 4.3 System Tests (Minimal)

- Validate:
  - End-to-end path of:
    - Auth → Tenant resolution → Repository → Response.
- Should be minimal and targeted.

---

## 5. Execution Requirements

### 5.1 Planner Responsibilities

The Planner MUST:

1. Analyze current project structure.
2. Define test directory layout, for example:

   - `backend/tests/unit/`
   - `backend/tests/integration/`
   - `backend/tests/system/`

3. Define pytest configuration:

   - Test settings module.
   - Test database behavior.
   - Fixtures for:
     - Tenant creation.
     - User creation.
     - JWT generation.

4. Define mandatory test categories:

   - JWT issuing & validation tests.
   - Tenant isolation tests.
   - Repository contract tests.
   - Application service tests.
   - Error format tests.

5. Define static quality gates:

   - `mypy` must pass.
   - `flake8` must pass.
   - Optional: minimum coverage threshold (e.g., 80%).

The Planner MUST NOT:

- Introduce business feature tests.
- Add unnecessary complexity.

---

### 5.2 Implementer Responsibilities

The Implementer MUST:

- Install and configure pytest (if not already).
- Create test structure:

  - `tests/unit/`
  - `tests/integration/`
  - `tests/system/`

- Configure Django test settings:

  - Separate test database.
  - Ensure no production DB is touched.

- Implement required unit tests:

  - JWT utility:
    - Valid token generation.
    - Expired token detection.
    - Invalid signature detection.
  - Tenant resolution:
    - Valid tenant lookup.
    - Invalid tenant error.
  - Repository:
    - Enforces tenant filtering.

- Implement integration tests:

  - `/api/v1/auth/me`:
    - Valid token → 200.
    - Invalid token → 401.
  - Multi-tenant:
    - Data created under tenant A not visible under tenant B.

- Add static checks integration:

  - Provide scripts or instructions:
    - `mypy backend/`
    - `flake8 backend/`

- Optionally configure coverage:

  - `pytest --cov=backend`

The Implementer MUST NOT:

- Disable failing tests to “make them pass”.
- Bypass tenant filtering for convenience.
- Modify architecture to simplify testing in a way that breaks ADRs.

---

### 5.3 Reviewer Responsibilities

The Reviewer MUST verify:

- Test structure exists and is clean.
- Unit tests exist for:
  - JWT utilities.
  - Tenant resolution.
  - Repository enforcement.
- Integration tests exist for:
  - Auth endpoint.
  - Multi-tenant isolation.
- No direct DB usage in unit tests unless justified.
- Test database is properly isolated from dev/prod.
- Static checks:
  - `mypy` passes.
  - `flake8` passes.

- Coverage:
  - Coverage report exists (if enabled).
  - Core infrastructure modules are covered.

If tenant isolation is not explicitly tested, STEP-06 MUST be rejected.

---

## 6. Concrete Work Items (Checklist)

### 6.1 Pytest Configuration

- [ ] Install pytest and pytest-django.
- [ ] Create pytest.ini.
- [ ] Configure test settings module.
- [ ] Ensure test DB isolation.

### 6.2 Unit Tests

- [ ] JWT issue/validate tests.
- [ ] Expired token test.
- [ ] Invalid signature test.
- [ ] Tenant resolution valid/invalid test.
- [ ] Repository enforces tenant filter test.

### 6.3 Integration Tests

- [ ] `/auth/me` with valid token.
- [ ] `/auth/me` with invalid token.
- [ ] Multi-tenant isolation test.

### 6.4 Static Quality Gates

- [ ] `mypy backend/` passes.
- [ ] `flake8 backend/` passes.
- [ ] Optional: coverage ≥ agreed threshold.

---

## 7. Validation & Execution

### 7.1 Local Execution

- [ ] Run:

  - `pytest`
  - `pytest --cov=backend`
  - `mypy backend/`
  - `flake8 backend/`

- [ ] Confirm:
  - All tests pass.
  - No lint/type errors.
  - Coverage acceptable.

### 7.2 Isolation Validation

- [ ] Create two tenants in test.
- [ ] Insert data for both.
- [ ] Confirm no cross-tenant visibility.

---

## 8. Definition of Done — STEP-06

STEP-06 is complete only when:

1. **Test Infrastructure**
   - [ ] pytest configured.
   - [ ] Separate test DB configured.
   - [ ] Clear test directory structure exists.

2. **Unit Coverage**
   - [ ] JWT utilities fully tested.
   - [ ] Tenant resolution tested.
   - [ ] Repository tenant enforcement tested.

3. **Integration Coverage**
   - [ ] Auth endpoint tested.
   - [ ] Multi-tenant isolation tested.

4. **Static Quality Gates**
   - [ ] `mypy` passes.
   - [ ] `flake8` passes.
   - [ ] Optional coverage threshold met.

5. **Architectural Integrity**
   - [ ] No architecture violations introduced.
   - [ ] All prior STEPs remain compliant.

Only when all items are verified by the Reviewer can STEP-06 be marked as DONE.