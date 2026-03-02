# STEP-03 — Authentication Skeleton (JWT Infrastructure, No Business Logic)

## 1. Purpose

This STEP introduces the **authentication infrastructure skeleton** without implementing full business flows.

Goals:

- Prepare the backend to issue and validate JWTs according to ADR-003.
- Introduce the minimal user/account model necessary for authentication infrastructure.
- Add middleware/hooks to extract authenticated user context from incoming requests.
- Ensure secrets, keys, and token handling adhere to security and secret management ADRs.
- Avoid any domain-specific or application-specific auth flows (e.g., password reset, signup forms, OAuth integrations).

This STEP focuses on setting up the **technical backbone** for authentication,
not on delivering a complete login/registration UX.

---

## 2. Scope

### 2.1 In Scope

Backend authentication infrastructure only, specifically:

- User/account model definition (aligned with Django’s auth system or a custom user model).
- JWT issuing and validation utilities.
- Authentication middleware/hooks to:
  - Parse Authorization headers.
  - Validate JWT signatures.
  - Attach an authenticated user principal to the request context.
- Basic “whoami”/`/auth/me` endpoint (read-only) for smoke-testing auth wiring.
- Integration with settings:
  - Public/private key loading.
  - Token lifetimes.
  - Algorithm choice (RS256) as per ADR-003.

### 2.2 Out of Scope

- Complex authentication flows:
  - Password reset.
  - Email confirmation.
  - Multi-factor authentication.
  - Social login/OAuth 2.0 flows (can be future STEPs).
- Full registration and onboarding flows (will be defined in feature STEPs).
- Authorization & RBAC rules (covered by other STEPs).
- UI changes in frontend/mobile.
- Tenant provisioning/assignment flows (handled in STEP-04 and feature STEPs).

---

## 3. Architectural Context

This STEP MUST comply with:

- ADR-001 — Multi-Tenancy Isolation Strategy  
  (Auth context must consider tenant boundaries in future STEPs; this STEP must not violate that.)

- ADR-003 — JWT Signing & Key Rotation Strategy  
  (JWTs MUST be RS256-signed, with `kid` in header, and support key rotation.)

- ADR-013 — API Versioning & Backward Compatibility Strategy  
  (Auth endpoints MUST live under `/api/v1/` and respect versioned contract patterns.)

- ADR-014 — Advanced Secret Management Strategy  
  (Private keys, public keys, and other sensitive auth settings MUST come from secure env/config, not hardcoded.)

- ADR-015 — Error & Exception Handling Strategy  
  (Auth errors MUST use the canonical error format and appropriate HTTP status codes.)

- ADR-016 — Testing Strategy & Test Pyramid  
  (Unit and integration tests for auth utilities and middleware MUST be introduced.)

- ADR-019 — Observability & Logging Contract  
  (Auth-related events MUST log safely without exposing secrets or entire token contents.)

- ADR-020 — Code Style & Formatting Governance  
  (mypy, flake8, black, etc. MUST remain clean after changes.)

This STEP prepares the ground for future:

- Tenant-aware auth (STEP-04).
- Role-based access control.
- Feature-level authentication requirements.

---

## 4. Execution Requirements

### 4.1 Planner Agent Responsibilities

The Planner Agent MUST:

1. Inspect current backend code to identify:
   - Existing user model (if present).
   - Any existing auth-related settings or utilities.
   - Any preliminary JWT or security-related code.

2. Produce a plan to:
   - Define or confirm the canonical User model location (e.g., `infrastructure` or a dedicated auth app).
   - Introduce a JWT utility module:
     - Token issuing (access token, optionally refresh token skeleton).
     - Token validation (signature, expiry, claims).
   - Configure key loading:
     - RS256 private key from env or file path.
     - RS256 public key(s) from env or file path(s).
     - `kid` selection and rotation-friendly design.
   - Add authentication middleware / request decorator to:
     - Parse Authorization bearer token.
     - Validate token.
     - Attach authenticated principal (user id, tenant id if known later) to request context.

3. Specify minimal endpoints:
   - `GET /api/v1/auth/me/` to return authenticated user basic info (e.g. id, email), purely for wiring verification.

4. Reference how this STEP:
   - Respects ADR-003, ADR-014, ADR-015, ADR-016.
   - Does not yet introduce full tenant or RBAC logic (these come later).

The Planner MUST NOT:

- Design full signup/login UX.
- Introduce multi-tenant logic beyond basic compatibility.
- Introduce business-specific behavior (e.g., subscription status, roles) in this STEP.

---

### 4.2 Implementer Agent Responsibilities

The Implementer Agent (or human developer) MUST:

- Implement or configure a **User model**:

  - Either:
    - Confirm and use Django’s built-in `User` (if suitable), or
    - Introduce a custom user model as per Django best practices.
  - Ensure compatibility with future tenant and RBAC logic.

- Implement a **JWT utility module**, e.g.:

  - `infrastructure/auth/jwt_utils.py` (or similar, respecting layering rules).
  - Functions to:
    - Issue access tokens with required claims (sub, exp, iat, iss, etc.).
    - Validate tokens (signature, expiry, issuer).

- Integrate **key management**:

  - Private key(s) loaded from env or secure file path.
  - Public key(s) for verification.
  - `kid` assigned to tokens and used to select verification key.
  - No keys hardcoded in code.

- Add **auth middleware / dependency** in interfaces layer:

  - Parse the `Authorization: Bearer <token>` header.
  - Validate token and resolve user identity.
  - Attach user context to request (e.g., `request.user` or equivalent).

- Implement a minimal `GET /api/v1/auth/me/` endpoint:

  - Returns basic authenticated user info:
    - id
    - email/username
  - Returns an appropriate error (401/403) if no valid token is provided.

The Implementer MUST:

- Use the error contract defined in ADR-015 for auth-related errors.
- Ensure no secret data (e.g., private key, raw token contents) are logged.

The Implementer MUST NOT:

- Implement full login/registration UI flows.
- Implement tenant assignment logic (belongs to later STEPs).
- Implement role-based authorization (another STEP).

---

### 4.3 Reviewer Agent Responsibilities

The Reviewer Agent MUST:

- Verify that:

  - JWT implementation uses RS256, not HS256 or others, as mandated by ADR-003.
  - Keys are NOT hardcoded:
    - Loaded from env or external secure configuration.
  - `kid` is present in JWT headers and used for verification.
  - `auth/me` endpoint:
    - Resides under `/api/v1/` and is versioned.
    - Returns appropriate error responses using ADR-015 format when unauthorized/unauthenticated.

- Confirm layering discipline:

  - JWT utilities do NOT depend on interfaces layer.
  - Middleware/endpoints do NOT contain business logic beyond auth wiring.
  - No tenant or RBAC rules implemented prematurely.

- Check error & logging constraints:

  - No token contents, private keys, or secrets are logged.
  - Error responses do NOT leak internal details.

- Check testing status:

  - Unit tests exist for JWT issuing and validation functions.
  - At least one integration test verifies:
    - A valid token can access `/auth/me/`.
    - An invalid/expired token is rejected with the correct error.

If any violation of ADR-003, ADR-014, ADR-015, or ADR-016 is found, STEP-03 MUST be rejected.

---

## 5. Concrete Work Items (Checklist)

This checklist is a guide for Planner/Implementer/Reviewer.

### 5.1 User Model & Auth App

- [ ] Confirm or create a dedicated auth module/app (e.g., `infrastructure/auth/` or `backend/auth_app/`).
- [ ] Define the canonical User model:
  - [ ] Either reuse Django default User or define a custom model.
  - [ ] Ensure future extension for tenant id and roles is possible.

### 5.2 JWT Utilities

- [ ] Create a JWT utility module:
  - [ ] Function to issue access tokens:
    - [ ] RS256 signing.
    - [ ] `kid` in header.
    - [ ] Standard claims (sub, exp, iat, iss).
  - [ ] Function to validate tokens:
    - [ ] Signature verification.
    - [ ] Expiry validation.
    - [ ] Issuer validation (if configured).

- [ ] Load keys via configuration:
  - [ ] Private key path or content from env.
  - [ ] Public keys from env/path(s).
  - [ ] No hardcoded key strings.

### 5.3 Middleware / Request Context

- [ ] Implement middleware (or equivalent mechanism) to:
  - [ ] Parse Authorization bearer token.
  - [ ] Validate token via JWT utilities.
  - [ ] Resolve user identity.
  - [ ] Attach user context to the request object.

- [ ] Ensure unauthenticated requests are handled gracefully with proper errors.

### 5.4 `/auth/me` Endpoint

- [ ] Add `GET /api/v1/auth/me/` endpoint:
  - [ ] Returns authenticated user’s basic data.
  - [ ] Uses the auth middleware to obtain the user context.
  - [ ] Returns 401/403 + proper error JSON when no/invalid token is provided.

### 5.5 Testing

- [ ] Unit tests:
  - [ ] For token issuing.
  - [ ] For token validation.
- [ ] Integration tests:
  - [ ] Valid token → `/auth/me` returns 200 and user info.
  - [ ] Invalid/expired token → `/auth/me` returns 401/403 with ADR-015 error format.

---

## 6. Validation & Testing

### 6.1 Local Validation

- [ ] Run dev server with STEP-02 settings.
- [ ] Manually obtain a JWT (via test utility or CLI).
- [ ] Call `/api/v1/auth/me/`:
  - [ ] With valid token → expect user info.
  - [ ] Without token or invalid token → expect proper error.

### 6.2 Static & Security Checks

- [ ] Run `mypy` and `flake8` to ensure:
  - [ ] No new type/lint errors introduced.
- [ ] Verify:
  - [ ] No secrets or raw tokens are printed in logs.
  - [ ] No hardcoded keys in repository.

---

## 7. Definition of Done — STEP-03

STEP-03 is complete only when ALL the following are true:

1. **JWT Infrastructure**
   - [ ] RS256 JWT issuing and validation utilities are implemented.
   - [ ] Keys are loaded from secure configuration (env/files), not hardcoded.
   - [ ] `kid` is present and used for verification.

2. **User Context**
   - [ ] A User model is defined/confirmed for the project.
   - [ ] Middleware or equivalent mechanism attaches authenticated user context to requests.

3. **Auth Endpoint**
   - [ ] `GET /api/v1/auth/me/` exists and:
     - [ ] Returns basic user info when authenticated.
     - [ ] Returns proper ADR-015-style errors when unauthenticated/unauthorized.

4. **Security & Secrets**
   - [ ] No private key or secret is hardcoded in code or settings.
   - [ ] No sensitive token/key details are logged.

5. **Testing**
   - [ ] Unit tests exist for JWT utilities.
   - [ ] Integration test(s) cover `/auth/me` for valid and invalid tokens.
   - [ ] `mypy` and `flake8` pass without new violations.

6. **ADR Compliance**
   - [ ] Implementation is compliant with ADR-001, 003, 013, 014, 015, 016, 019, 020.
   - [ ] No business-domain auth flows have been prematurely implemented.

Only when all of the above are verified by the Reviewer, STEP-03 can be considered DONE.