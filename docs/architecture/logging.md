# Logging Architecture

---

## 1. Purpose

This document defines the logging strategy of the system.

It specifies:

- Logging goals and principles
- Log levels and categorization
- Structured logging requirements
- Multi-tenant logging rules
- Security and privacy constraints
- Log correlation and traceability
- Backend and frontend logging responsibilities
- Integration with observability and CI/CD

This document complements:

- ARCHITECTURE.md  
- backend-structure.md  
- security-model.md  
- error-handling.md  
- multi-tenancy.md  
- observability.md  
- ci-cd.md  

In case of conflict, ADRs prevail.

---

## 2. Logging Goals

The logging system must:

- Provide actionable operational visibility
- Support debugging and incident investigation
- Support security monitoring
- Maintain tenant isolation
- Avoid leaking sensitive data
- Be structured and machine-readable
- Integrate with centralized log aggregation systems

Logging must balance observability and security.

---

## 3. Logging Principles

Logging must be:

- Structured (prefer JSON format)
- Context-aware
- Minimal but sufficient
- Environment-sensitive
- Secure by default

Logs must never:

- Contain secrets
- Contain tokens
- Contain passwords
- Contain sensitive personal data unless strictly necessary and compliant

---

## 4. Log Levels

Standard log levels must be used consistently:

- DEBUG → Detailed diagnostic information (development only)
- INFO → Normal system operations
- WARNING → Expected but abnormal situations
- ERROR → Operational failures requiring attention
- CRITICAL → Severe failures requiring immediate attention

Log levels must not be misused.

---

## 5. Structured Logging

All backend logs must use structured format (preferably JSON).

Each log entry should include:

- timestamp
- level
- service name
- environment (dev/staging/prod)
- request_id (if applicable)
- tenant_id (if applicable)
- user_id (if authenticated)
- message
- error_code (if applicable)

Structured logs enable:

- Searchability
- Aggregation
- Filtering
- Automated alerting

---

## 6. Multi-Tenancy Logging Rules

Multi-tenant systems require careful logging.

Rules:

- Every request log must include tenant_id where applicable.
- Logs must not mix tenant data implicitly.
- No cross-tenant identifiers must be exposed.
- Logging must not reveal data from other tenants.
- Internal logs may include tenant_id for traceability.

Tenant_id must not be shown in client-facing responses.

---

## 7. Authentication and Authorization Logging

Authentication events must log:

- Successful login (INFO)
- Failed login (WARNING)
- Token validation failures (WARNING)
- Suspicious authentication attempts (ERROR)

Authorization failures:

- Log at WARNING level.
- Include:
  - user_id
  - tenant_id
  - attempted action
- Avoid revealing sensitive resource details.

Sensitive security events should be traceable but privacy-conscious.

---

## 8. Error Logging

Errors must:

- Be logged at ERROR or CRITICAL level.
- Include correlation identifiers.
- Avoid logging sensitive input data.
- Include sanitized error information.

Stack traces:

- Allowed in development.
- Restricted or sanitized in production.
- Must never be returned to clients.

Error handling details are defined in error-handling.md.

---

## 9. Request Logging

Each HTTP request should log:

- request_id
- method
- path (without sensitive query data)
- status code
- response time
- tenant_id (if applicable)
- user_id (if authenticated)

Sensitive headers and bodies must not be logged.

Request logging must:

- Avoid logging entire request bodies unless necessary.
- Avoid logging large payloads.

---

## 10. Infrastructure Logging

Infrastructure components (DB, integrations) must:

- Log connection failures.
- Log timeouts.
- Log external API failures.
- Avoid logging raw payloads containing sensitive information.

Retries must log:

- Attempt count
- Final outcome
- Correlation identifiers

Infrastructure logs must not expose credentials.

---

## 11. Frontend Logging (Web)

Frontend logging must:

- Avoid logging sensitive data.
- Avoid logging tokens.
- Log only non-sensitive client errors.
- Be environment-aware (debug logs disabled in production).

Client-side logs may include:

- UI errors
- Failed API calls (status code only)
- Unexpected state transitions

Frontend logs must not replace backend logging.

---

## 12. Mobile Logging

Mobile logging must:

- Avoid logging tokens or secrets.
- Avoid logging full API payloads.
- Be minimal in production builds.
- Be useful for debugging crash reports.

Crash reporting tools may be used, but:

- Must not expose sensitive data.
- Must comply with privacy requirements.

---

## 13. Log Storage and Aggregation

Logs should be:

- Emitted to stdout in containerized environments.
- Collected by centralized log systems (e.g., ELK, Cloud logging).
- Retained according to retention policy.

Retention policy must:

- Define duration per environment.
- Comply with regulatory requirements.
- Avoid indefinite storage of sensitive logs.

---

## 14. Correlation and Traceability

Each request must have:

- A unique request_id.
- Propagation of request_id across layers.

For distributed systems:

- Trace identifiers should be propagated to external services.
- Correlation IDs should be included in logs.

Correlation enables:

- End-to-end debugging
- Incident reconstruction
- Performance tracing

---

## 15. Logging and Performance

Logging must:

- Avoid excessive verbosity in production.
- Avoid blocking operations.
- Avoid large synchronous I/O operations.
- Use asynchronous logging where possible.

Logging should not significantly degrade performance.

---

## 16. Compliance and Privacy

Logging must comply with:

- Data protection regulations (e.g., GDPR if applicable).
- Privacy best practices.

Rules:

- Do not log personal data unnecessarily.
- Mask partially sensitive fields where needed.
- Ensure logs are protected with proper access control.

Access to logs must be restricted to authorized personnel.

---

## 17. Testing Logging

Logging behavior must be tested for:

- Proper inclusion of tenant_id and request_id.
- Absence of sensitive fields in logs.
- Correct log level usage for major scenarios.
- Proper error logging behavior.

Tests must ensure that:

- No secrets are logged.
- Logging does not leak cross-tenant data.

---

## 18. Prohibited Patterns

The following are strictly forbidden:

- Logging JWT tokens or passwords.
- Logging full request bodies with sensitive data.
- Logging raw database queries with parameters.
- Using print statements in production code.
- Swallowing errors without logging.
- Logging at DEBUG level in production.

Any exception requires ADR approval.

---

## 19. Evolution Strategy

Logging strategy may evolve if:

- Observability tooling changes.
- Structured logging format changes.
- Compliance requirements evolve.
- Distributed tracing is introduced.

Changes that affect:

- Log format
- Correlation strategy
- Sensitive data policy

Must be documented and reviewed.

Logging is foundational to observability, security, and operational reliability.