# Frontend Mobile Architecture (React Native)

---

## 1. Purpose

This document defines the architecture of the Mobile frontend application built with React Native.

It specifies:

- Project structure and layering
- Responsibilities of each layer
- Integration with backend API
- Authentication and authorization handling
- Multi-tenancy handling in the mobile client
- State management strategy
- Error handling and observability integration
- Security constraints specific to mobile devices

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

The Mobile frontend must:

- Provide a secure and consistent user experience on iOS and Android
- Respect backend architectural boundaries
- Correctly handle authentication and authorization states
- Support multi-tenant behavior in a mobile context
- Handle offline/poor connectivity scenarios gracefully
- Remain modular, testable, and maintainable
- Integrate with CI/CD and observability practices

As with Web, the mobile app is a **presentation layer**, not a domain layer.

---

## 3. High-Level Structure

The mobile frontend resides under:

frontend/mobile/

Recommended structure:

frontend/mobile/  
├── src/  
│   ├── app/  
│   ├── navigation/  
│   ├── screens/  
│   ├── components/  
│   ├── hooks/  
│   ├── services/  
│   ├── state/  
│   ├── utils/  
│   └── config/  
├── android/  
├── ios/  
├── tests/  
└── package.json  

The structure must reflect separation of concerns and navigation-centric design.

---

## 4. Layer Responsibilities

### 4.1 App Layer (`app/`)

Responsibilities:

- Application bootstrap
- Registration of navigation container
- Global providers (auth, tenant, theme, state)
- Global error boundaries

Must not contain:

- Backend business logic
- Direct API calls
- Authorization rules beyond basic wiring

---

### 4.2 Navigation Layer (`navigation/`)

Responsibilities:

- Stack/tab navigation definitions
- Navigation flows (auth flow, main app flow)
- Deep link and OAuth callback handling (if used)
- Guarded navigation patterns (e.g., redirect to login if unauthenticated)

Navigation must:

- Respect authentication state
- Reset stacks on logout or tenant switch to avoid data leakage
- Avoid embedding business logic in navigation definitions

---

### 4.3 Screens Layer (`screens/`)

Responsibilities:

- Screen-level components
- Composition of feature UIs
- Interaction with hooks and services
- Mapping user interactions to actions

Screens must not:

- Contain complex business logic
- Perform direct network calls
- Store tokens or secrets

---

### 4.4 Components Layer (`components/`)

Responsibilities:

- Reusable UI components (buttons, lists, forms, etc.)
- Presentational logic only
- Styling/layout for mobile

Constraints:

- No direct API calls
- No authentication logic
- No multi-tenant logic

Components should be reusable and pure.

---

### 4.5 Hooks Layer (`hooks/`)

Responsibilities:

- Reusable UI logic (e.g., useForm, usePaginatedList)
- Encapsulation of interaction patterns
- Orchestration with services and state

Hooks may:

- Call services layer
- Use global or screen-level state

Hooks must not:

- Implement business domain rules
- Store sensitive data in persistent storage

---

### 4.6 Services Layer (`services/`)

Responsibilities:

- Encapsulate HTTP/API client logic
- Format requests and parse responses
- Attach authentication headers
- Handle token refresh logic (in coordination with auth state)
- Apply base URL and API versioning rules

Constraints:

- Must not contain domain logic
- Must not store tokens directly (tokens come from secure storage / auth state)
- Must strictly follow authentication.md and api-versioning.md

All network calls must go through services.

---

### 4.7 State Layer (`state/`)

Responsibilities:

- Global state management (auth, tenant, user profile)
- Persistent state synchronization with secure storage (for tokens)
- UI-level global state (e.g., theme) if needed

Requirements:

- Strategy must be explicit (Context, Zustand, Redux, etc.)
- Must be predictable and serializable (where possible)
- Must support reset on logout or tenant change

State layer must not:

- Replace backend as source of truth
- Store sensitive data in insecure locations

---

### 4.8 Config Layer (`config/`)

Responsibilities:

- Environment-specific config (API base URL, environment name)
- Public-safe settings only
- Build-time / runtime config binding

Must not:

- Contain secrets
- Contain OAuth client secrets

---

## 5. Authentication Handling (Mobile)

Authentication must follow mobile-specific security rules:

- Access and refresh tokens must be stored in **secure storage**:
  - iOS Keychain
  - Android Encrypted SharedPreferences/Keystore
- No tokens in AsyncStorage for long-term persistence.
- On app startup:
  - Load tokens from secure storage.
  - Initialize auth state.
  - Verify token validity when appropriate.

Flow:

1. User authenticates (credentials or social login).
2. Backend returns JWT (access token, refresh token if applicable).
3. App stores tokens in secure storage through auth state layer.
4. Services layer:
   - Reads tokens from auth state (not from storage directly).
   - Attaches Authorization headers.
5. On token expiration:
   - Attempt refresh (if supported).
   - If refresh fails, logout user and clear secure storage.

The app must:

- Clear tokens from secure storage on logout.
- Reset navigation stacks to avoid residual access.

---

## 6. Social Authentication (Mobile)

For social login:

- Use system browser or custom tabs (not embedded WebView, when possible).
- Use OAuth + PKCE for secure flows.
- Use platform deep links or universal/app links for callbacks (e.g., myapp://auth/callback).

Flow:

1. App opens authorization URL in secure browser context.
2. User authenticates with provider.
3. Provider redirects to app's deep link.
4. App receives authorization code.
5. App sends code to backend.
6. Backend validates provider and issues internal JWT.
7. App stores tokens securely.

The mobile app must:

- Never store OAuth client secrets.
- Never trust provider token directly for API access (backend must issue JWT).

---

## 7. Authorization Handling (Mobile)

Mobile app authorization responsibilities:

- Adapt UI based on roles/permissions (e.g., hide protected actions).
- Avoid exposing actions the user is not allowed to perform.

However:

- Authorization enforcement resides in backend.
- The mobile app must always handle 403 responses by:
  - Showing appropriate feedback.
  - Optionally adjusting UI if consistent.

UI-level checks are convenience, not security.

---

## 8. Multi-Tenancy Handling

Mobile app must support multi-tenant behavior:

- Tenant context may be derived from:
  - User selection
  - JWT claims
  - Configured tenant for the app instance (if applicable)

The app must:

- Store tenant context in global state.
- Scope data in memory and cache per tenant.
- Reset tenant-scoped state when:
  - Tenant is changed
  - User logs out

Forbidden:

- Mixing data from multiple tenants in the same UI without clear separation.
- Reusing cached data across tenants.

If tenant is part of API path, services layer must construct URLs accordingly.

---

## 9. API Integration

All API requests must:

- Use services layer (no direct fetch/axios in screens/components).
- Respect API versioning conventions.
- Include authentication headers when required.
- Handle network errors and timeouts gracefully.

The app must be resilient to:

- Intermittent connectivity
- Timeouts
- Backend errors

Due to mobile context, error handling must be explicit and user-friendly.

---

## 10. Offline and Connectivity Considerations

Mobile apps must account for:

- No connectivity
- Flaky networks
- Background/foreground transitions

Recommended patterns:

- Detect connectivity status.
- Show user-friendly errors when offline.
- Optionally cache data (per tenant, per user) with clear invalidation rules.
- Avoid infinite spinners on network failure.

Caching must:

- Never cache sensitive data in plain text.
- Respect tenant separation.

---

## 11. Error Handling (Mobile)

Error handling must:

- Map HTTP status codes to:
  - Authentication errors (401)
  - Authorization errors (403)
  - Not found (404)
  - Validation errors (4xx)
  - Server errors (5xx)
- Show clear, non-technical user messages.
- Avoid exposing raw backend error structures directly.

Global error boundary:

- Should catch unexpected runtime exceptions.
- Provide fallback UI.
- Log error details through observability integration (without sensitive data).

---

## 12. Observability Integration

Mobile observability should include:

- Crash reporting
- Error logging (non-sensitive)
- Network error tracking
- Performance metrics for key flows

Rules:

- Never log tokens or secrets.
- Avoid logging full request/response payloads.
- Respect privacy and platform policies.

Telemetry should be:

- Sampled when appropriate.
- Configurable per environment (e.g., more verbose in dev).

---

## 13. Security Considerations (Mobile)

Specific mobile security rules:

- No secrets in app bundle (JS or native).
- No hardcoded credentials.
- Use HTTPS only.
- Consider certificate pinning if required by security posture.
- Protect sensitive screens from screenshots or task switchers if needed (OS-specific features).

Device compromise must be considered possible; minimize damage:

- Keep tokens short-lived.
- Use refresh logic securely.
- Clear sensitive state on logout or app delete.

---

## 14. Performance Considerations

Mobile performance must:

- Avoid heavy computations on UI thread.
- Use appropriate list virtualization for long lists.
- Minimize unnecessary re-renders.
- Manage memory usage carefully.

Network performance must:

- Avoid redundant requests.
- Use caching when safe.
- Batch or debounce calls where reasonable.

Performance optimizations must not break correctness or security.

---

## 15. Testing Strategy (Mobile)

Recommended tests:

- Unit tests:
  - Components
  - Hooks
  - Pure functions
- Integration tests:
  - Screens with navigation and mocked services
- Authentication tests:
  - Login flow
  - Token refresh handling
  - Logout behavior
- Multi-tenant tests:
  - Tenant switching
  - Tenant-scoped data separation

E2E tests (if used):

- Execute on emulators/devices
- Cover critical flows:
  - Login
  - Main user journeys
  - Logout and tenant switch

Tests must not depend on production backend or production secrets.

---

## 16. Prohibited Patterns

Forbidden patterns:

- Storing tokens in AsyncStorage or other insecure stores for long term.
- Embedding secrets or private keys in the app.
- Calling backend APIs directly from components/screens.
- Implementing business logic that belongs to backend.
- Mixing tenant data in shared state.
- Ignoring 401/403 responses from backend.
- Logging sensitive data in debug logs.

Any necessary exception requires explicit review and documentation.

---

## 17. Evolution Strategy

Mobile architecture may evolve when:

- State management approach changes.
- Navigation structure changes.
- Offline behavior becomes more complex.
- New native capabilities are integrated.

Changes affecting:

- Authentication and token handling
- Multi-tenancy behavior
- API compatibility
- Secure storage strategy

Must be carefully reviewed and documented.

The mobile app must remain a secure, tenant-aware, and well-structured presentation layer aligned with the overall SaaS architecture.