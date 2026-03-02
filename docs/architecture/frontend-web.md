# Frontend Web Architecture (React)

---

## 1. Purpose

This document defines the architecture of the Web frontend application built with React.

It specifies:

- Project structure and layering
- Responsibilities of each layer
- Integration with backend API
- Authentication and authorization handling
- Multi-tenancy handling in the UI
- State management strategy
- Error handling and observability integration
- Security constraints

This document complements:

- ARCHITECTURE.md  
- authentication.md  
- authorization.md  
- api-versioning.md  
- error-handling.md  
- security-model.md  
- observability.md  
- configuration.md  

In case of conflict, ADRs prevail.

---

## 2. Goals

The Web frontend must:

- Provide a responsive and secure user interface
- Respect backend architectural boundaries
- Avoid embedding business logic that belongs to backend
- Correctly handle authentication and authorization states
- Support multi-tenant behavior
- Remain modular and testable
- Integrate with CI/CD and observability practices

Frontend is a presentation layer, not a domain layer.

---

## 3. High-Level Structure

The web frontend resides under:

frontend/web/

Recommended structure:

frontend/web/  
├── src/  
│   ├── app/  
│   ├── features/  
│   ├── components/  
│   ├── hooks/  
│   ├── services/  
│   ├── state/  
│   ├── routes/  
│   ├── utils/  
│   └── config/  
├── public/  
├── tests/  
└── package.json  

The structure must reflect separation of concerns.

---

## 4. Layer Responsibilities

### 4.1 App Layer (`app/`)

Responsibilities:

- Application bootstrap
- Router configuration
- Global providers (auth, theme, state)
- Error boundaries

Must not contain:

- Business logic
- API calls directly
- Authorization rules

---

### 4.2 Features Layer (`features/`)

Responsibilities:

- Feature-based modular structure
- Pages and containers per domain concept
- Local feature state
- UI orchestration

Features should group:

- Page components
- Feature-specific hooks
- Feature-specific UI components

Features must not:

- Duplicate shared logic
- Directly manipulate global configuration

---

### 4.3 Components Layer (`components/`)

Responsibilities:

- Reusable UI components
- Pure presentational logic
- Styling and layout

Constraints:

- Must not perform API calls
- Must not contain business rules
- Should remain reusable across features

---

### 4.4 Hooks Layer (`hooks/`)

Responsibilities:

- Encapsulate reusable UI logic
- Manage interaction logic
- Abstract API interaction patterns

Hooks may:

- Use services layer
- Use global state

Hooks must not:

- Contain business domain logic

---

### 4.5 Services Layer (`services/`)

Responsibilities:

- Encapsulate API calls
- Manage request formatting
- Handle response parsing
- Attach authentication headers
- Handle token refresh logic (if applicable)

Constraints:

- Must align with API versioning strategy
- Must not embed domain rules
- Must not bypass authentication logic

Services are thin adapters to backend APIs.

---

### 4.6 State Layer (`state/`)

Responsibilities:

- Global state management (if used)
- Authentication state
- Tenant context
- UI preferences

State management strategy must:

- Be explicit (e.g., Context API, Redux, Zustand, etc.)
- Avoid global mutable state patterns
- Remain predictable

Global state must not:

- Replace backend as source of truth
- Store sensitive data insecurely

---

### 4.7 Routing (`routes/`)

Responsibilities:

- Route definitions
- Protected route logic
- Lazy loading configuration

Protected routes must:

- Check authentication state
- Optionally check role-based access (UI-level only)

Authorization enforcement must still occur in backend.

---

## 5. Authentication Handling

Web authentication must:

- Follow rules in authentication.md
- Store access token in memory (preferred)
- Store refresh token in secure HTTP-only cookie
- Handle token expiration gracefully
- Trigger refresh flow automatically when needed

Frontend must not:

- Store tokens in localStorage (unless explicitly approved)
- Trust client-side authorization as final authority

401 responses must trigger:

- Logout or refresh logic
- Redirect to login when appropriate

---

## 6. Authorization Handling

Frontend authorization responsibilities:

- Conditionally render UI elements based on roles
- Hide or disable forbidden actions

Rules:

- UI-level checks are for user experience only.
- Backend remains the source of truth for authorization.
- Frontend must handle 403 responses gracefully.

Frontend must not assume that hidden UI equals secure behavior.

---

## 7. Multi-Tenancy Handling

Frontend must support multi-tenant behavior:

- Tenant context may be derived from:
  - Subdomain
  - Path
  - JWT claim
- Tenant context must be stored in global state.
- Tenant switching (if allowed) must:
  - Clear sensitive state
  - Reload relevant data

Frontend must never:

- Allow cross-tenant data mixing
- Cache tenant data without tenant scoping

Tenant identifier must not be manipulated manually in client logic.

---

## 8. API Integration

All API calls must:

- Go through the services layer
- Include versioned endpoints
- Include authentication headers
- Handle error responses consistently

API responses must be:

- Validated
- Safely parsed
- Handled according to error-handling.md

Frontend must not:

- Call backend endpoints directly from components
- Hardcode API URLs outside config layer

---

## 9. Configuration Handling

Frontend configuration must:

- Be environment-specific
- Include only non-sensitive values
- Be injected at build or runtime safely
- Not contain secrets

Configuration may include:

- API base URL
- Environment name
- Public feature flags

Secrets must never be included in frontend bundles.

---

## 10. Error Handling (Frontend)

Frontend must:

- Interpret HTTP status codes properly
- Display user-friendly error messages
- Avoid exposing raw backend error codes
- Handle:

  - 401 → redirect to login
  - 403 → show forbidden state
  - 404 → show not found page
  - 5xx → show generic error message

Error boundaries should catch unexpected UI crashes.

---

## 11. Observability Integration

Frontend must:

- Log client-side errors (non-sensitive)
- Track API failure rates
- Track performance metrics
- Avoid logging tokens or personal data

Telemetry must:

- Respect privacy rules
- Be environment-aware
- Support debugging without exposing sensitive information

---

## 12. Performance Considerations

Frontend must:

- Use lazy loading where appropriate
- Avoid unnecessary re-renders
- Avoid heavy global state updates
- Cache safely without mixing tenant data
- Avoid blocking operations

Performance optimizations must not compromise security or correctness.

---

## 13. Testing Strategy (Web)

Frontend tests must include:

- Unit tests for components and hooks
- Integration tests for feature flows
- API mocking tests
- Authentication flow tests
- Protected route behavior tests

Tests must validate:

- Correct handling of error responses
- Correct handling of tenant context
- Correct role-based UI rendering

Frontend tests must not depend on production backend.

---

## 14. Prohibited Patterns

The following are forbidden:

- Storing tokens in localStorage without approval
- Embedding secrets in frontend code
- Performing business logic in components
- Bypassing services layer for API calls
- Trusting frontend-only authorization
- Mixing tenant data in state
- Using global mutable variables for auth state

Any exception requires review and documentation.

---

## 15. Evolution Strategy

Frontend architecture may evolve when:

- State management strategy changes
- Routing model changes
- New rendering frameworks are adopted
- Micro-frontend architecture is introduced

Significant changes affecting:

- Authentication handling
- Multi-tenancy behavior
- API version compatibility

Must be reviewed and documented.

Frontend remains a presentation layer and must not absorb backend responsibilities.