# Error Handling Architecture

---

## 1. Purpose

This document defines the error handling strategy of the system.

It specifies:

- How errors are classified
- Where errors are raised
- How errors propagate across layers
- How errors are mapped to HTTP responses
- How errors are logged
- How errors interact with multi-tenancy and security
- Client-facing error format

This document complements:

- ARCHITECTURE.md  
- backend-structure.md  
- authentication.md  
- authorization.md  
- security-model.md  
- logging.md  
- testing-strategy.md  

In case of conflict, ADRs prevail.

---

## 2. Error Handling Goals

The error handling strategy must:

- Provide consistent and predictable error responses
- Avoid leaking sensitive information
- Clearly distinguish between technical and business errors
- Preserve tenant isolation
- Support observability and diagnostics
- Remain testable and deterministic

Error handling is part of system reliability and security.

---

## 3. Error Categories

Errors are classified into the following categories:

### 3.1 Domain Errors

Origin:

- Domain layer

Examples:

- Invalid state transition
- Business rule violation
- Invariant failure

Characteristics:

- Deterministic
- Predictable
- Part of expected behavior

These errors represent valid but rejected operations.

---

### 3.2 Application Errors

Origin:

- Application layer

Examples:

- Resource not found
- Unauthorized action
- Invalid use case input

These errors reflect invalid usage of the system.

---

### 3.3 Infrastructure Errors

Origin:

- Database
- External APIs
- Network failures
- Third-party services

Characteristics:

- May be transient
- May require retries
- May require fallback strategies

---

### 3.4 System Errors

Origin:

- Unexpected exceptions
- Programming errors
- Misconfiguration

Characteristics:

- Unintended failures
- Should be logged and monitored
- Should not expose internal details

---

## 4. Layer Responsibilities

### 4.1 Domain Layer

- Raise explicit domain exceptions for business rule violations.
- Avoid generic exceptions.
- Do not format HTTP responses.
- Do not log sensitive data.

Domain errors must be meaningful and structured.

---

### 4.2 Application Layer

- Catch domain errors where necessary.
- Raise application-specific exceptions (e.g., NotFound, Forbidden).
- Enforce authorization-related failures explicitly.
- Avoid swallowing exceptions silently.

Application layer must not convert errors into HTTP responses.

---

### 4.3 Infrastructure Layer

- Wrap low-level exceptions into meaningful infrastructure exceptions.
- Avoid leaking database or external service details.
- Log technical failures appropriately.
- Do not propagate raw driver errors upward.

Infrastructure errors must be sanitized before leaving the layer.

---

### 4.4 Interfaces / API Layer

- Catch application and infrastructure exceptions.
- Map exceptions to HTTP status codes.
- Return standardized error payload.
- Never expose stack traces in production.

Interfaces are responsible for translating exceptions to protocol-level responses.

---

## 5. Standard Error Response Format (API)

All API errors must follow a consistent structure.

Example JSON structure:

{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found.",
    "details": null,
    "request_id": "optional-correlation-id"
  }
}

Rules:

- code → stable machine-readable identifier
- message → human-readable, non-sensitive message
- details → optional structured details (safe only)
- request_id → correlation identifier (if available)

No internal stack trace or implementation detail must appear in responses.

---

## 6. HTTP Status Code Mapping

Recommended mappings:

- 400 → Validation errors
- 401 → Unauthenticated
- 403 → Unauthorized (forbidden)
- 404 → Resource not found
- 409 → Conflict
- 422 → Semantic validation failure
- 429 → Rate limit exceeded
- 500 → Internal server error
- 503 → Service unavailable (external dependency failure)

Status codes must be consistent across endpoints.

---

## 7. Multi-Tenancy and Errors

Error handling must respect tenant isolation.

Rules:

- Never reveal whether a resource exists in another tenant.
- Avoid different messages that could reveal cross-tenant data.
- Unauthorized cross-tenant access must behave as:
  - 404 (if hiding existence)
  - or 403 (if existence is acceptable to disclose)

Choice must be consistent and documented.

Tenant context must be included in internal logs (not client response).

---

## 8. Authentication and Authorization Errors

Authentication failures:

- Return 401.
- Use generic message (e.g., "Invalid credentials").
- Do not reveal whether user exists.

Authorization failures:

- Return 403.
- Avoid exposing rule logic.
- Avoid indicating existence of restricted resource unless policy allows.

Token validation failures:

- Expired token → 401.
- Invalid signature → 401.
- Tenant mismatch → 403 or 401 (consistent policy required).

---

## 9. Logging and Error Visibility

When errors occur:

- Log at appropriate level:
  - Domain/application error → WARNING (if expected)
  - Infrastructure failure → ERROR
  - Unexpected exception → ERROR or CRITICAL
- Include:
  - request_id
  - tenant_id (if applicable)
  - user_id (if authenticated)
- Do not log:
  - passwords
  - tokens
  - secrets
  - sensitive personal data

Detailed logging rules are defined in logging.md.

---

## 10. Frontend Error Handling (Web)

Web client must:

- Interpret HTTP status codes correctly.
- Display user-friendly messages.
- Avoid exposing backend error codes directly to end users.
- Handle:
  - 401 → redirect to login
  - 403 → show forbidden page or message
  - 5xx → show generic error message

Frontend must not assume success if HTTP status indicates failure.

---

## 11. Mobile Error Handling

Mobile client must:

- Handle token expiration gracefully.
- Trigger refresh flow when appropriate.
- Handle offline/network failures explicitly.
- Avoid exposing raw backend error payloads to end users.

User-facing messages must be safe and generic.

---

## 12. Retry Strategy

Retries may be applied only to:

- Transient infrastructure errors
- Temporary network failures
- 503 responses

Retries must:

- Be bounded (no infinite loops)
- Use exponential backoff
- Avoid duplicating non-idempotent operations without safeguards

Retry logic must not be implemented blindly.

---

## 13. Exception Design Guidelines

Custom exception classes should:

- Be explicit
- Represent meaningful error categories
- Avoid overuse of generic exceptions
- Be documented

Avoid:

- Catch-all exceptions without rethrowing or logging
- Silent failures
- Mixing business and technical exception types

---

## 14. Testing Error Handling

Tests must validate:

- Correct exception raising at domain level
- Correct mapping to HTTP status codes
- Correct error payload structure
- Negative tests for unauthorized access
- Cross-tenant access denial behavior
- Infrastructure failure behavior

Error paths must be explicitly tested, not assumed.

---

## 15. Prohibited Patterns

The following are forbidden:

- Returning raw stack traces to clients
- Logging secrets or tokens in error logs
- Using generic 500 for known business errors
- Swallowing exceptions silently
- Exposing database or framework error messages
- Inconsistent error response formats across endpoints

Any deviation requires ADR approval.

---

## 16. Evolution Strategy

Error handling model changes require ADR if they involve:

- Changing API error format
- Introducing new error categorization model
- Changing HTTP mapping rules
- Introducing global exception handling middleware that alters behavior

Error handling must remain:

- Consistent
- Secure
- Predictable
- Observable

It is a core reliability and security mechanism of the system.