# ADR-015 — Error & Exception Handling Strategy (API Error Contract)

- Status: Accepted
- Date: 2026-02-26
- Authors: Architecture Team
- Related ADRs:
  - ADR-001 — Multi-Tenancy Isolation Strategy
  - ADR-003 — JWT Signing & Key Rotation Strategy
  - ADR-008 — Audit Logging & Compliance Strategy
  - ADR-013 — API Versioning & Backward Compatibility Strategy
  - ADR-016 — Testing Strategy (future)

---

## 1. Context

The system exposes versioned HTTP APIs consumed by:

- Web frontend
- Mobile applications
- Potential third-party clients
- Internal services and background workers

To ensure:

- Backward compatibility (ADR-013),
- Clear client behavior,
- Secure multi-tenant isolation (ADR-001),
- Proper logging and auditability (ADR-008),

we must define a stable and version-aware error contract.

Without a formal error strategy:

- Error formats may drift over time.
- Breaking changes may occur unintentionally.
- Sensitive internal details may leak.
- Clients may rely on undefined behavior.
- Observability and monitoring become inconsistent.

This ADR defines the canonical error response format,
error classification model, HTTP mapping rules,
and security constraints.

---

## 2. Decision

We adopt a structured, version-aware JSON error contract
with strict separation between:

- Domain errors
- Application errors
- Infrastructure errors
- System errors

Error response structure MUST remain backward compatible
within a major API version.

Breaking changes to the error format require
a new major API version (ADR-013).

---

## 3. Canonical Error Response Format

All API errors MUST return JSON in the following structure:

{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {},
    "request_id": "uuid",
    "timestamp": "ISO-8601",
    "api_version": "v1"
  }
}

---

### 3.1 Field Definitions

code (string, REQUIRED)
- Stable machine-readable identifier.
- Must not change within a major version.
- Serves as the canonical contract element for clients.

message (string, REQUIRED)
- Human-readable explanation.
- May evolve for clarity but must preserve semantic meaning.
- Must not contain sensitive information.

details (object, OPTIONAL)
- Structured additional metadata.
- Used primarily for validation errors.
- Must never contain secrets or internal stack traces.

request_id (string, REQUIRED)
- Correlation ID for tracing.
- Must match logging and tracing systems.

timestamp (string, REQUIRED)
- ISO-8601 UTC timestamp.

api_version (string, REQUIRED)
- Major version identifier (e.g., "v1").

---

## 4. Error Classification Model

Errors are categorized into four layers:

### 4.1 Domain Errors

Origin:
- Business logic violations.

Examples:
- INSUFFICIENT_BALANCE
- TENANT_NOT_ALLOWED
- RESOURCE_ALREADY_EXISTS

Typical HTTP mappings:
- 400 Bad Request
- 403 Forbidden
- 409 Conflict

Domain errors MUST:
- Be deterministic.
- Be safe for client exposure.
- Never leak internal implementation details.

---

### 4.2 Application Errors

Origin:
- Application orchestration layer.
- Input validation failures.
- State transition violations.

Examples:
- INVALID_INPUT
- MISSING_PARAMETER
- INVALID_STATE

Typical HTTP mappings:
- 400 Bad Request
- 422 Unprocessable Entity

Validation-related errors SHOULD include structured details.

---

### 4.3 Infrastructure Errors

Origin:
- Database connectivity issues.
- External API failures.
- Network timeouts.

Examples:
- DATABASE_UNAVAILABLE
- EXTERNAL_SERVICE_TIMEOUT

Typical HTTP mappings:
- 503 Service Unavailable
- 504 Gateway Timeout

Infrastructure errors MUST NOT expose:
- SQL statements
- Internal hostnames
- Stack traces

---

### 4.4 System Errors

Origin:
- Unexpected unhandled exceptions.

Example:
- INTERNAL_ERROR

Typical HTTP mapping:
- 500 Internal Server Error

System errors MUST:
- Return a generic client-safe message.
- Log full diagnostic details internally.
- Never expose stack traces in production.

---

## 5. HTTP Status Code Policy

- 2xx codes indicate success only.
- 4xx codes represent client-side issues.
- 5xx codes represent server-side failures.
- Non-standard HTTP status codes are forbidden.
- Status code semantics must align with RFC standards.

---

## 6. Backward Compatibility Rules (ADR-013 Alignment)

Within a major API version:

- The error JSON structure MUST remain stable.
- Existing error codes MUST NOT be renamed or removed.
- New error codes MAY be introduced.
- Changing error code semantics is considered breaking.

Breaking changes require:

- A new major API version.
- Parallel support during a defined deprecation window.

---

## 7. Multi-Tenancy Safety (ADR-001 Alignment)

Error responses MUST NOT:

- Reveal tenant identifiers.
- Indicate existence of resources across tenants.
- Leak cross-tenant information.

Example:

If a resource belongs to another tenant,
the response SHOULD return 404 NOT_FOUND
instead of exposing tenant mismatch details,
unless business rules explicitly require otherwise.

---

## 8. Security Constraints

The following MUST NEVER appear in production error responses:

- Stack traces
- Internal file paths
- SQL queries
- Secret values
- JWT payload contents
- Infrastructure topology
- Environment variables

Sensitive debugging information MUST remain in structured logs only.

---

## 9. Logging & Observability Alignment (ADR-008)

For every error response:

- request_id MUST be logged.
- error.code MUST be logged as structured field.
- api_version MUST be logged.
- Tenant context MUST be logged safely.

This enables:

- Version-specific monitoring
- Tenant-safe debugging
- Incident tracing
- Audit compliance

---

## 10. Testing Requirements (ADR-016 Alignment)

Test suites MUST verify:

- Error format schema stability.
- Presence of mandatory fields.
- Correct HTTP status mapping.
- No sensitive information leakage.
- Tenant isolation in error scenarios.

Contract tests SHOULD assert:

- Stable error codes across releases.
- Backward compatibility within a major version.

---

## 11. Alternatives Considered

### 11.1 Free-Form Error Responses

Rejected because:
- Unstable contract.
- Hard to test.
- Hard to version.
- Encourages drift.

---

### 11.2 Stack Trace Exposure in Non-Production

Allowed only in explicit development mode.
Never allowed in staging or production environments.

---

## 12. Consequences

### Positive Consequences

- Stable client-facing contract.
- Predictable mobile/web integration.
- Strong observability and audit capabilities.
- Reduced risk of accidental breaking changes.
- Clear mapping between business rules and HTTP responses.

### Trade-offs

- Requires disciplined error code management.
- Slight overhead in centralized exception handling.
- Requires version-aware thinking when evolving APIs.

---

## 13. Implementation Notes

- Implement a centralized exception handler layer.
- Maintain a centralized error code registry.
- Ensure error responses are generated consistently.
- Log internal details separately from client-safe messages.
- Include api_version in error responses and logs.

All future API-related STEPs MUST comply with this ADR.