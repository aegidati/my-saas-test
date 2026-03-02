# Security Model

---

## 1. Purpose

This document defines the security model of the system.

It specifies:

- Security principles and threat model
- Responsibilities across layers
- Input and output validation rules
- Multi-tenant security constraints
- Secrets and configuration handling
- Logging and data protection rules
- Client-specific considerations (Web and Mobile)
- Prohibited patterns

This document complements:

- `ARCHITECTURE.md`
- `multi-tenancy.md`
- `authentication.md`
- `authorization.md`
- `database-abstraction.md`
- `backend-structure.md`
- Relevant ADRs and security reviews

In case of conflict, ADRs prevail.

---

## 2. Security Goals

The system must:

- Protect confidentiality, integrity, and availability of data
- Enforce strict tenant isolation
- Prevent unauthorized access
- Limit impact and blast radius of potential breaches
- Minimize attack surface on all clients (Web and Mobile)
- Support secure evolution over time

Security is a first-class architectural concern and must be considered in every change.

---

## 3. Threat Model (High-Level)

The system must consider threats including, but not limited to:

- Unauthorized access (broken authentication/authorization)
- Cross-tenant data leakage
- Data exposure via logs or errors
- Injection attacks (SQL, NoSQL, command, etc.)
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Man-in-the-middle (MITM) attacks
- Token theft and replay
- Compromised clients (web browser, mobile device)
- Misconfiguration and insecure defaults

Detailed threat modeling for specific features may be captured in ADRs or separate security assessments.

---

## 4. Security Responsibilities by Layer

### 4.1 Presentation Layer (Interfaces / API / Frontends)

Responsibilities:

- Enforce authentication at boundaries
- Validate basic request structure
- Avoid trusting client-provided data
- Avoid exposing sensitive data in responses
- Apply CSRF protection when cookies are used (web)
- Apply secure CORS configuration (web)

Must not:

- Contain business authorization logic beyond glue-level checks
- Rely on frontend-only security validation

---

### 4.2 Application Layer

Responsibilities:

- Enforce authorization policies
- Enforce multi-tenant access rules
- Coordinate security-sensitive workflows (e.g., password reset, account linking)
- Validate business-level invariants (e.g., ownership checks)

Must not:

- Bypass security checks based on assumptions (“it was checked before”)
- Trust data solely because it comes from internal layers

---

### 4.3 Domain Layer

Responsibilities:

- Enforce domain invariants important for security (e.g., immutable records, state transitions)
- Encapsulate rules that prevent invalid or dangerous states

Must not:

- Depend on infrastructure or framework security constructs

---

### 4.4 Infrastructure Layer

Responsibilities:

- Secure integration with databases and external services
- Implement secure storage and retrieval of data
- Configure TLS and secure endpoints (where applicable)
- Safely handle secrets and credentials
- Implement secure logging

Must not:

- Contain business authorization logic
- Introduce insecure defaults

---

## 5. Input Validation and Output Encoding

### 5.1 Input Validation

Rules:

- All external inputs (HTTP body, query params, headers, path params, environment variables) must be treated as untrusted.
- Validation must:
  - Enforce types, ranges, and formats
  - Reject unexpected fields when appropriate
  - Sanitize or reject dangerous content

Validation strategy:

- Basic syntactic validation at API boundary (interfaces)
- Semantic/business validation in Application and Domain layers

---

### 5.2 Output Encoding

Rules:

- Output sent to web clients must be properly encoded:
  - HTML encoding where relevant
  - JSON encoding via safe serializers
- Avoid embedding untrusted content in HTML without encoding.

Frontend must avoid:

- `dangerouslySetInnerHTML` in React without strict sanitization
- Direct insertion of user-controlled HTML

---

## 6. Multi-Tenancy Security

Multi-tenancy is a core part of the security model.

Rules:

- Tenant Context must be resolved per request.
- Tenant ID in JWT (if present) must match resolved tenant.
- Repository operations must always enforce tenant scoping.
- No cross-tenant joins or data-sharing unless explicitly designed and documented.
- Global or system-wide operations must be explicitly marked and carefully reviewed.

Any change affecting tenant isolation requires ADR and security review.

---

## 7. Authentication and Session Security

Authentication is defined in `authentication.md`. Security rules include:

- Only HTTPS is allowed for authenticated endpoints.
- JWT tokens must:
  - Be signed with strong algorithms.
  - Have appropriate expirations.
  - Be validated on every request.
- Refresh tokens must be:
  - Stored securely (HTTP-only cookies on web, secure storage on mobile).
  - Rotated and revocable if implemented.
- Logout and token revocation behavior must be clearly defined.

No long-lived access tokens without explicit ADR and mitigation measures.

---

## 8. Authorization Enforcement

Authorization is defined in `authorization.md`. Security rules include:

- No reliance on frontend-only checks.
- Authorization must be enforced in Application and/or Domain layers.
- Every security-sensitive operation must:
  - Check user identity.
  - Check tenant membership.
  - Check role/permissions/policies.

Missing authorization is considered a critical security bug.

---

## 9. Secrets and Configuration

Secrets (e.g., JWT keys, database credentials, OAuth client secrets) must:

- Never be hardcoded in source code.
- Be provided via secure configuration (environment variables, secret managers).
- Not be committed to version control.

Configuration principles:

- Use environment variables or a secure configuration provider.
- Configuration must be environment-specific (dev/staging/prod).
- Sensitive configuration values must not appear in logs or error messages.

Configuration rules are detailed in `configuration.md`.

---

## 10. Logging and Observability

Logging must:

- Include enough context to diagnose issues (user id, tenant id, request id where applicable).
- Avoid logging:
  - Passwords
  - Tokens
  - Secrets
  - Sensitive personal data

Security-sensitive events (login failures, suspicious behavior) should be:

- Logged in a privacy-conscious manner.
- Monitored for anomaly detection where possible.

Observability tools must respect tenant boundaries when displaying or aggregating data.

Detailed rules are defined in `logging.md` and `observability.md`.

---

## 11. Web Client Security (React)

Web-specific security:

- Do not store tokens in `localStorage` or `sessionStorage` unless explicitly justified; prefer:
  - Access token in memory.
  - Refresh token in HTTP-only cookies.
- Use secure cookies:
  - `HttpOnly`, `Secure`, `SameSite`.
- Apply CSRF protection when using cookies.
- Apply strict CORS policy:
  - Whitelist explicit origins.
  - Avoid `*` for credentials or sensitive endpoints.
- Mitigate XSS:
  - Avoid `dangerouslySetInnerHTML`.
  - Sanitize user-generated content.
  - Consider Content Security Policy (CSP) for additional protection.

The web client must never assume it can skip server-side checks.

---

## 12. Mobile Client Security (React Native)

Mobile-specific security:

- Store tokens in secure storage:
  - iOS Keychain.
  - Android Encrypted SharedPreferences/Keystore.
- Never hardcode secrets or client secrets in the app.
- Use secure communication:
  - Enforce HTTPS.
  - Consider certificate pinning for high-security scenarios.
- For social login:
  - Use system browser or custom tabs with OAuth + PKCE.
  - Use secure deep-link/callback handling.
  - The backend must be the only component that issues internal JWT.

Device compromise must be assumed as a realistic threat; minimize what a compromised device can expose.

---

## 13. Error Handling and Information Disclosure

Error responses must:

- Not expose stack traces to clients.
- Not disclose internal implementation details.
- Use generic messages for authentication/authorization failures (e.g., “invalid credentials”, “forbidden”).

Internally:

- Detailed error logs may be stored for diagnostics but must avoid sensitive data leakage.

Consistent error response format should be documented in `error-handling.md`.

---

## 14. Performance and Security Trade-offs

Security-related trade-offs (e.g., token lifetime, encryption, rate limiting) must:

- Be documented and justified.
- Consider user experience without compromising core security.
- Be revisited periodically.

Any relaxations in security controls must be justified via ADR and reviewed.

---

## 15. Testing and Verification

Security-related behavior must be tested via:

- Unit tests for security-critical code paths.
- Integration tests for authentication and authorization.
- Multi-tenant isolation tests.
- End-to-end tests for login, logout, and token refresh.
- Negative tests for access control (ensuring forbidden actions are blocked).

Where possible, automated tools (linters, SAST/DAST) should be integrated into CI/CD as defined in `ci-cd.md`.

---

## 16. Prohibited Patterns

The following are strictly forbidden:

- Storing secrets in source code or public repositories.
- Relying on frontend-only checks for security.
- Bypassing authentication/authorization for “internal” endpoints.
- Direct database access from Presentation layer.
- Use of plain HTTP for authenticated traffic.
- Logging tokens, passwords, or secrets.
- Global mutable state used for tenant context or identity.

Any required exception must be documented and approved via ADR.

---

## 17. Evolution Strategy

Security model changes require ADR when they involve:

- Changes to authentication mechanisms or token formats.
- Changes to multi-tenancy isolation strategy.
- Introduction of new external identity providers or SSO.
- Relaxation of security controls.
- Introduction of new cryptographic schemes.

Security must evolve deliberately, with careful review and validation. All contributors are responsible for respecting and maintaining the security model described in this document.