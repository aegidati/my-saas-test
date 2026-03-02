# ADR-013 — API Versioning & Backward Compatibility Strategy

- Status: Accepted  
- Date: 2026-02-26  
- Authors: Architecture Team  
- Supersedes: N/A  
- Related ADRs:
  - ADR-002 — Database Engine Strategy
  - ADR-003 — JWT Signing & Key Rotation Strategy
  - ADR-005 — API Rate Limiting Strategy
  - ADR-010 — Data Governance & Retention Policy
  - ADR-015 — Error & Exception Handling Strategy (future)
  - ADR-016 — Testing Strategy (future)

---

## 1. Context

The system exposes multiple HTTP APIs consumed by:

- Web frontend (React)
- Mobile applications (React Native)
- Potential third-party clients (partners, integrations)
- Internal tools and job/external workers

We need a clear strategy for:

- How API versions are defined and exposed
- How breaking changes are introduced and managed over time
- How clients can safely upgrade without regressions
- How long older versions are supported
- How all of this interacts with:
  - Mobile store release cycles (slow updates)
  - Multi-tenant model
  - Observability, logging, and auditing
  - Rate limiting and security controls

The architecture snapshot already states that:

- URL-based versioning is expected (`/api/v1/...`)
- Breaking changes require explicit versioning
- Mobile compatibility must be preserved

However, these rules were not yet formalized as an ADR,
and there was no explicit policy for deprecation, stability guarantees,
and test/observability requirements.

---

## 2. Decision

We adopt a **URL-based, major-versioned API strategy**
with strict backward compatibility guarantees **within a major version**.

### 2.1 Versioning Scheme

- All public API endpoints MUST be exposed under a versioned URL prefix:

  - `/api/v1/...`
  - `/api/v2/...`
  - etc.

- The version identifier (`v1`, `v2`, ...) represents the **major version**.
- There is **no minor version** in the URL.
  - Minor and patch-level changes are managed internally (docs, changelog, semantic versioning of the backend),
    but are not reflected in the URL.

### 2.2 Backward Compatibility Rules

- **Within a major version (e.g. v1)**:
  - Changes MUST be **backward compatible** for existing clients.
  - Allowed changes include:
    - Adding new fields to response payloads (without changing existing semantics)
    - Adding new optional request parameters
    - Adding new optional headers
    - Adding new endpoints
  - Disallowed changes:
    - Removing or renaming existing fields
    - Changing field types or formats in a breaking way
    - Changing HTTP method of an existing endpoint
    - Changing semantics of business behavior in a way that breaks existing clients
    - Changing error contract in a breaking way (to be detailed in ADR-015)

- **Breaking changes** MUST only be introduced by:
  - Creating a new major version prefix (e.g. `/api/v2/...`)
  - Maintaining the previous major version for a deprecation period

### 2.3 Version Pinning Policy

- Clients (web, mobile, external) MUST **explicitly target a single major version** of the API.
- The backend MUST NOT perform implicit "version negotiation" based on headers or user-agent:
  - Version is determined solely by the URL prefix.
- The frontend web application is expected to:
  - Use a single API major version at any given release.
- Mobile applications:
  - MUST pin to a specific major version (e.g. `/api/v1/...`).
  - The server MUST maintain that version stable for a defined support window
    to accommodate slow updates from app stores.

### 2.4 Deprecation Policy

- When introducing a new major version (e.g. v2):
  - v1 MUST remain available for a **deprecation period** (to be defined per environment, e.g. 6–12 months).
  - Deprecation MUST be communicated via:
    - API documentation
    - Release notes
    - Optional HTTP headers (e.g. `Deprecation`, `Sunset`) on deprecated endpoints.

- During the deprecation window:
  - No new features SHOULD be added to the deprecated version.
  - Only security fixes and critical bug fixes are allowed.

- After the deprecation period:
  - The old version MAY be disabled, returning:
    - A clear error response indicating that the version is no longer supported.
    - A link or reference to documentation for the supported version(s).

### 2.5 Internal vs External APIs

We distinguish between:

- **Public API**:
  - Used by web/mobile clients and potential external integrators.
  - MUST follow strict versioning and deprecation rules defined in this ADR.
  - MUST be documented and treated as a contract.

- **Internal API** (admin, internal tools, experimental):
  - MAY reside under a separate namespace, e.g. `/internal/` or `/admin/`.
  - MAY have more relaxed versioning rules, but:
    - MUST NOT be exposed to untrusted clients.
    - MUST be clearly marked as internal in the code and documentation.
  - Internal APIs SHOULD still consider stability, but are allowed to evolve faster.

### 2.6 Relation with Multi-Tenancy (ADR-001)

- API versioning is **orthogonal** to tenant isolation:
  - Tenant context is enforced within each version.
  - No cross-tenant leakage is allowed in any version.
- Changes to tenant-related behavior between versions (e.g. new limits, new fields)
  MUST still respect the tenant isolation rules.

### 2.7 Error Contract and Observability

- Error response structure MUST be version-aware:
  - Within a major version, the error contract MUST remain backward compatible.
  - Breaking changes to error shape or semantics require a new major version.
- Logs and traces MUST record:
  - API version (e.g. `api_version: "v1"`) as a structured field.
  - This enables:
    - Per-version observability
    - Gradual rollout monitoring
    - Impact analysis during migrations

Details of the error model and error codes will be formalized in ADR-015.

### 2.8 Testing & CI Requirements

- For every major version, we MUST maintain:
  - A regression test suite that covers critical endpoints.
  - Contract tests (where applicable) to ensure backward compatibility.
- CI MUST:
  - Validate that changes to an API version do not break existing tests for that version.
  - Validate that adding a new version does not implicitly change behavior of previous versions.

Details of testing policy will be expanded in ADR-016.

---

## 3. Alternatives Considered

### 3.1 Header-based Versioning (e.g. `Accept: application/vnd.app.v1+json`)

**Pros:**

- URL remains clean and stable.
- Version negotiation can be technically more flexible.

**Cons:**

- More complex for clients to implement and debug.
- Harder to inspect and filter in logs and monitoring tools.
- Less explicit in browser/dev tools, complicating support and debugging.
- Not aligned with the initial project direction (URL-based versioning).

**Decision:** Rejected in favor of explicit URL-based versioning.

---

### 3.2 No Versioning (Always Latest)

**Pros:**

- Simpler code and URLs initially.
- No version management overhead at the start.

**Cons:**

- Every change risks breaking existing clients.
- No safe evolution path for mobile apps (store/update lag).
- No controlled deprecation model.
- Not acceptable for a multi-tenant SaaS with long-lived clients.

**Decision:** Rejected as incompatible with long-term maintainability.

---

### 3.3 Query Parameter Versioning (e.g. `/api/resource?version=1`)

**Pros:**

- Minimal change to URL structure.
- Easy to experiment.

**Cons:**

- Parameter may be accidentally omitted or altered.
- Harder to enforce at routing level.
- More error-prone and less explicit than path-based versioning.
- Not a common best practice for long-lived public APIs.

**Decision:** Rejected in favor of path-based major versioning.

---

## 4. Consequences

### 4.1 Positive Consequences

- Clear contract with clients:
  - URL clearly indicates the major version.
  - Breaking changes are isolated per version.
- Safe evolution path:
  - We can add new versions while keeping old ones stable during deprecation.
- Better observability:
  - Logs and metrics can be aggregated by API version.
- Better support for mobile clients:
  - Mobile apps can rely on a stable API version for a defined time.
- Governance alignment:
  - ADR-013 provides a solid foundation for ADR-015 (Error Strategy) and ADR-016 (Testing Strategy).

### 4.2 Negative Consequences / Trade-offs

- Code complexity:
  - Multiple versions may coexist in the codebase.
  - Careful routing and structure are required to avoid duplication and divergence.
- Maintenance cost:
  - Old versions must be supported for the duration of their deprecation window.
- Documentation overhead:
  - API docs must be maintained per version.
  - Deprecation statuses must be clearly communicated.

### 4.3 Required Follow-up Actions

- Define and document:
  - The default deprecation window (e.g. 12 months for public APIs).
  - Version-specific support policy per environment (dev/staging/prod).
- Implement:
  - A version-aware routing strategy in the backend.
  - Logging/tracing fields for `api_version`.
- Align:
  - Testing strategy (ADR-016) to ensure version-specific regression coverage.
  - Error contract (ADR-015) with version-aware semantics.

---

## 5. Implementation Notes

- All new API endpoints MUST be introduced under `/api/v1/...` (or the current major version).
- When a breaking change is required:
  - Propose a dedicated STEP for introducing `/api/v2/...`.
  - Ensure regression tests are in place for `/api/v1/...`.
- The STEP Responsibility Matrix MUST:
  - Assign API versioning enforcement to the appropriate STEP(s).
- The Operational Prompt Sequence MUST:
  - Reference ADR-013 when planning or reviewing API-related STEPs.