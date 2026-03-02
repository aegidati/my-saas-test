# Use Case


.github/prompts/feature-planning.prompt.md
.github/prompts/feature-implementation.prompt.md
.github/prompts/feature-review.prompt.md

## How to complex

“Use the standard Feature Implementation prompt for Features012”


---

## How to compact

Phase: [Planning/Implementation/Review]  
Feature: #file:/docs/features/FeaturesXXX.md  
Objective: [1 sentence]  
Layers: Touch [..] / Do NOT touch [..]  
Constraints: Respect ADRs, no new deps, no architecture changes  
Success: Architecture safe, secure, tested

---




**Planning Phase**

## CONTEXT

Phase: Planning

Feature File:
- #file:/docs/features/Features012-UserRegistration.md

Architecture References:
- #file:/docs/adr/ADR-003-user-module.md
- #file:/docs/architecture/domain-layer.md

Constraints:
- No new dependencies
- No architectural changes
- Maintain backward compatibility

---

## OBJECTIVE

Produce a complete implementation plan for user registration.

---

## SCOPE

Included:
- Domain logic
- Application use case
- Persistence integration

Excluded:
- UI implementation

---

## LAYER EXPECTATION

The change must affect:
- Domain
- Application
- Infrastructure

The change must NOT affect:
- Presentation

---

## SUCCESS CRITERIA

- Layer separation respected
- Validation rules defined
- Testing strategy defined


**Implementation Phase**

## CONTEXT

Phase: Implementation

Feature File:
- #file:/docs/features/Features012-UserRegistration.md

Approved Plan:
[Paste planner output here]

Constraints:
- No new dependencies
- Do not modify public interfaces

---

## OBJECTIVE

Implement the user registration feature strictly following the approved plan.

---

## LAYER EXPECTATION

The change must affect:
- Domain
- Application
- Infrastructure

The change must NOT affect:
- Presentation

---

## SUCCESS CRITERIA

- Tests added
- Validation enforced
- No architecture violations


**Review Phase**

## CONTEXT

Phase: Review

Feature File:
- #file:/docs/features/Features012-UserRegistration.md

Files:
- #file:/src/domain/user/User.ts
- #file:/src/application/RegisterUserUseCase.ts
- #file:/src/infrastructure/UserRepository.ts

---

## OBJECTIVE

Perform strict architectural and security review.

---

## SUCCESS CRITERIA

- No layer violations
- No security gaps
- No N+1 queries