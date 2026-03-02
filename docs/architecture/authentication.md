# Authentication Architecture

---

## 1. Purpose

This document defines the authentication architecture of the system.

It specifies:

- The JWT-based authentication model
- Social authentication integration
- Multi-tenant authentication behavior
- Token lifecycle management
- Client-specific security considerations (Web vs Mobile)
- Security boundaries and constraints

This document complements:

- `ARCHITECTURE.md`
- `multi-tenancy.md`
- `database-abstraction.md`
- `authorization.md`
- Relevant ADRs

In case of conflict, ADRs prevail.

---

## 2. Authentication Goals

The authentication system must:

- Provide secure, stateless authentication using JWT
- Support OAuth-based social login providers
- Integrate with the multi-tenant architecture
- Minimize attack surface on both web and mobile clients
- Support scalable distributed deployments
- Prevent cross-tenant access by design

Authentication is a critical security boundary of the system.

---

## 3. Authentication Model Overview

The system uses a stateless JWT-based authentication model.

High-level flow:

1. User authenticates via:
   - Credentials (if supported), or
   - Social login provider (OAuth)
2. Backend validates identity.
3. Backend issues a signed JWT (access token).
4. Client stores token securely.
5. Client sends token with each authenticated request.
6. Backend validates token and resolves user + tenant context.

Authentication is enforced at the Presentation boundary (API layer).

---

## 4. JWT Strategy

### 4.1 Token Characteristics

JWTs must:

- Be cryptographically signed (algorithm defined via ADR)
- Include:
  - `sub` (user identifier)
  - `exp` (expiration)
  - `iat` (issued at)
  - `iss` (issuer)
  - `aud` (audience, if applicable)
  - `tenant_id` (if tenant-scoped)
- Contain minimal necessary claims only

Tokens must be:

- Short-lived (access tokens)
- Rotatable

Refresh token strategy must be defined in ADR.

---

### 4.2 Token Validation

Each authenticated request must:

- Validate signature
- Validate expiration
- Validate issuer and audience
- Extract user identity
- Extract tenant context
- Verify tenant membership

Invalid tokens must result in immediate rejection.

---

## 5. Multi-Tenant Authentication

Authentication must integrate with the multi-tenancy model.

Rules:

- JWT must include tenant identifier when operating in tenant scope.
- Backend must verify that:
  - User belongs to tenant.
  - Tenant in token matches resolved tenant (e.g., subdomain).
- Cross-tenant token reuse must be impossible.

Mismatch between resolved tenant and token tenant claim must result in rejection.

---

## 6. Token Lifecycle

### 6.1 Access Tokens

- Short-lived
- Stateless
- Used for API access
- Included in Authorization header (`Bearer <token>`)

### 6.2 Refresh Tokens

If implemented:

- Must be securely stored (client-dependent)
- Must be rotatable
- Must be revocable
- Must be bound to user and tenant

Refresh rotation and revocation strategy must be documented in ADR.

---

## 7. Web Client (React) vs Mobile Client (React Native)

Although the backend model is unified, client-side security measures differ.

---

## 8. Web Client (React)

### 8.1 Token Storage (Web)

Recommended approach:

- Access token:
  - Stored in memory only (not persisted in localStorage)
- Refresh token:
  - Stored in HTTP-only, Secure cookie
  - `SameSite` set to `Lax` or `Strict`
  - Not accessible via JavaScript

Avoid:

- Storing tokens in `localStorage`
- Storing tokens in `sessionStorage`
- Exposing tokens to client-side scripts unnecessarily

### 8.2 CSRF Protection

If cookies are used:

- Implement CSRF protection strategy
- Use `SameSite` cookies
- Optionally use anti-CSRF tokens

### 8.3 XSS Protection

Web application must:

- Avoid injecting untrusted HTML
- Sanitize user input
- Avoid storing tokens in JavaScript-accessible storage
- Consider Content Security Policy (CSP)

---

## 9. Mobile Client (React Native)

Mobile applications have different constraints and threat models.

### 9.1 Token Storage (Mobile)

Access and refresh tokens must be stored in secure platform storage:

- iOS: Keychain
- Android: Encrypted SharedPreferences / Keystore

Avoid:

- AsyncStorage for sensitive tokens
- Hardcoding secrets in the application

Tokens may be loaded into memory for API calls but must persist only in secure storage.

---

### 9.2 Device Security Considerations

Mobile security must consider:

- Device compromise
- Reverse engineering
- Man-in-the-middle attacks

Recommended protections:

- Enforce HTTPS
- Consider certificate pinning (if high-security context)
- Avoid embedding OAuth client secrets in the mobile app

---

## 10. Social Authentication (OAuth)

The system supports OAuth-based providers (e.g., Google, GitHub).

Social provider tokens must never be treated as internal authentication tokens.

Backend must:

1. Validate provider-issued tokens or authorization codes.
2. Map external identity to internal user.
3. Issue internal JWT.

---

### 10.1 Social Login – Web

Web flow:

1. Redirect user to provider authorization endpoint.
2. Provider authenticates user.
3. Provider redirects back to backend callback endpoint.
4. Backend validates authorization code.
5. Backend issues JWT (access + refresh if applicable).
6. Tokens handled via cookie or response mechanism.

Web must ensure:

- Secure redirect URIs
- State parameter validation
- CSRF protection in OAuth flow

---

### 10.2 Social Login – Mobile

Mobile flow should use:

- System browser or custom tabs
- OAuth with PKCE
- Deep linking back into the app

Recommended flow:

1. App opens provider authorization in system browser.
2. User authenticates.
3. Provider redirects to custom scheme (e.g., `myapp://auth/callback`).
4. App sends authorization code to backend.
5. Backend validates and issues JWT.

Mobile app must never:

- Embed OAuth client secret
- Trust provider tokens directly
- Handle token signing locally

---

## 11. Logout Strategy

Logout must:

- Invalidate refresh tokens (if used)
- Optionally blacklist access tokens if necessary
- Remove client-side tokens securely

Stateless logout limitations must be documented.

---

## 12. Rate Limiting and Abuse Protection

Authentication endpoints must implement:

- Rate limiting
- Brute-force protection
- IP throttling
- Suspicious activity monitoring

These protections apply to:

- Login endpoints
- Refresh endpoints
- Social login callbacks

---

## 13. Error Handling

Authentication errors must:

- Avoid leaking sensitive details
- Not reveal whether a user exists (where applicable)
- Use consistent response structure
- Avoid exposing internal stack traces

---

## 14. Testing Requirements

Authentication must be validated via:

- Unit tests for token generation and validation
- Integration tests for login flows
- Tests for tenant-scoped authentication
- Social login integration tests
- Security tests for invalid/expired tokens

Both Web and Mobile flows must be covered.

---

## 15. Prohibited Patterns

The following are strictly forbidden:

- Storing JWT in localStorage (web) without explicit security evaluation
- Storing tokens in insecure mobile storage
- Hardcoding secrets in frontend/mobile apps
- Trusting social provider tokens for internal authorization
- Skipping tenant validation during authentication
- Bypassing authentication in Presentation layer

Any deviation requires ADR approval.

---

## 16. Evolution Strategy

Changes requiring ADR:

- Changing signing algorithm
- Introducing SSO or external identity providers
- Changing token structure
- Introducing refresh token rotation
- Modifying tenant-scoped authentication logic

Authentication architecture must evolve deliberately and under architectural governance.