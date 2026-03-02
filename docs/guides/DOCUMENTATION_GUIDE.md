# Documentation Overview Guide

---

## 1. Purpose

This document provides a concise overview of every architectural and governance document in the project.

It explains:

- What each document covers
- Why it exists
- When developers should consult it
- How documents relate to each other

This guide serves as a navigation map for the entire documentation system.

---

# CORE ARCHITECTURE DOCUMENTS

---

## ARCHITECTURE.md

**What it covers:**  
High-level overview of the entire system.

**Purpose:**  
Defines the global structure of the SaaS platform, including:

- Monorepo organization
- Backend (Django)
- Web (React)
- Mobile (React Native)
- Packages layer
- Multi-tenancy foundation
- Architectural philosophy

**When to read:**  
First document every developer must read.

---

## backend-structure.md

**What it covers:**  
Backend layering and folder structure.

**Purpose:**  
Defines:

- Domain layer responsibilities
- Application layer responsibilities
- Infrastructure layer responsibilities
- Interfaces/API layer responsibilities
- Dependency rules
- Multi-tenancy integration points

**When to read:**  
Before modifying or adding backend logic.

---

## frontend-web.md

**What it covers:**  
Architecture of the React web application.

**Purpose:**  
Defines:

- Folder structure
- Services layer
- State management
- Auth handling
- Tenant handling
- UI responsibility boundaries

**When to read:**  
Before implementing or refactoring web features.

---

## frontend-mobile.md

**What it covers:**  
Architecture of the React Native mobile application.

**Purpose:**  
Defines:

- Secure token storage
- Navigation structure
- API integration
- Multi-tenant behavior
- Offline considerations
- Mobile security constraints

**When to read:**  
Before implementing mobile features.

---

## packages.md

**What it covers:**  
Reusable backend modules inside the monorepo.

**Purpose:**  
Defines:

- What belongs in packages
- Dependency constraints
- Public API discipline
- Versioning strategy
- Testing requirements

**When to read:**  
Before adding shared utilities or cross-cutting modules.

---

# MULTI-TENANCY & DATA

---

## multi-tenancy.md

**What it covers:**  
Tenant isolation model.

**Purpose:**  
Defines:

- Tenant resolution
- Tenant context propagation
- Isolation strategies
- Cross-tenant restrictions
- Security rules for tenant separation

**When to read:**  
Before implementing any feature that accesses tenant-scoped data.

---

## database-abstraction.md

**What it covers:**  
Database architecture and repository pattern.

**Purpose:**  
Defines:

- Repository interfaces
- ORM isolation
- Engine-agnostic design
- Transaction boundaries
- Multi-tenant database behavior

**When to read:**  
Before modifying persistence logic.

---

# SECURITY & IDENTITY

---

## authentication.md

**What it covers:**  
JWT-based authentication model.

**Purpose:**  
Defines:

- Token lifecycle
- Web vs Mobile token handling
- Social login flow
- Refresh strategy
- Security constraints

**When to read:**  
Before modifying login, tokens, or identity flows.

---

## authorization.md

**What it covers:**  
Role-based and policy-based authorization.

**Purpose:**  
Defines:

- RBAC model
- Policy evaluation
- Tenant-scoped roles
- Where authorization must occur
- Prohibited patterns

**When to read:**  
Before implementing permission checks.

---

## security-model.md

**What it covers:**  
Global security posture.

**Purpose:**  
Defines:

- Threat model
- Secure coding principles
- Input validation rules
- Secret management
- Logging restrictions
- Web vs Mobile security differences

**When to read:**  
Before making security-sensitive changes.

---

# OPERATIONAL DISCIPLINE

---

## configuration.md

**What it covers:**  
Environment and configuration strategy.

**Purpose:**  
Defines:

- Environment separation
- Secret injection
- Tenant-specific config
- Feature flags
- Startup validation rules

**When to read:**  
Before adding new environment variables or config logic.

---

## testing-strategy.md

**What it covers:**  
Testing model across layers.

**Purpose:**  
Defines:

- Unit vs integration vs API vs E2E tests
- Multi-tenant test requirements
- Security testing expectations
- Coverage guidelines

**When to read:**  
Before writing or refactoring tests.

---

## error-handling.md

**What it covers:**  
Error classification and API response structure.

**Purpose:**  
Defines:

- Domain vs application vs infrastructure errors
- HTTP mapping rules
- Standard error payload
- Security-safe error exposure

**When to read:**  
Before modifying exception handling or API responses.

---

## api-versioning.md

**What it covers:**  
API evolution strategy.

**Purpose:**  
Defines:

- URL-based versioning
- Breaking change rules
- Deprecation policy
- Mobile compatibility considerations

**When to read:**  
Before changing API contracts.

---

## logging.md

**What it covers:**  
Structured logging rules.

**Purpose:**  
Defines:

- Log levels
- Structured log format
- Tenant-aware logging
- Sensitive data restrictions
- Request correlation rules

**When to read:**  
Before adding logs or modifying logging behavior.

---

## observability.md

**What it covers:**  
Metrics, tracing, monitoring, and alerting.

**Purpose:**  
Defines:

- Metrics types
- SLO/SLI
- Tenant-safe dashboards
- Alerting strategy
- Post-deploy monitoring

**When to read:**  
When adding monitoring or diagnosing incidents.

---

## ci-cd.md

**What it covers:**  
Continuous Integration and Delivery.

**Purpose:**  
Defines:

- Monorepo pipeline structure
- Quality gates
- Deployment flow
- Environment promotion
- Security scanning
- Rollback strategy

**When to read:**  
Before modifying pipeline or deployment process.

---

# GOVERNANCE

---

## Developer Onboarding Guide

**What it covers:**  
How to work within the architecture.

**Purpose:**  
Defines:

- How to navigate docs
- How to implement features
- How to use AI safely
- Architectural discipline expectations
- Definition of Done

**When to read:**  
Mandatory reading for every new contributor.

---

# DOCUMENTATION HIERARCHY SUMMARY

1. ARCHITECTURE.md → System overview  
2. Layer-specific docs → Backend, Web, Mobile, Packages  
3. Cross-cutting docs → Security, Config, Logging, CI/CD  
4. Governance docs → Onboarding and workflow discipline  

All documents together define:

- Structural boundaries
- Security constraints
- Operational discipline
- Long-term scalability

---

# Final Note

This documentation system is designed to:

- Prevent architectural drift
- Protect tenant isolation
- Enforce security boundaries
- Maintain clean layering
- Enable safe scaling of the SaaS platform

Every contributor must treat documentation as authoritative.

Architecture precedes code.