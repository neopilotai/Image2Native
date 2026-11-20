# Implementation Process

Every implementation cycle follows this order:

1. **Inventory:** identify the owning crate, current dependencies, public contracts and existing tests.
2. **Boundary review:** validate that the proposed change respects `project/boundaries.json`.
3. **Baseline:** capture current test/behavior evidence before changing implementation.
4. **Plan:** create/update a task with acceptance criteria and dependencies.
5. **Implement:** change only the owning boundary; keep interfaces narrow.
6. **Test:** unit, integration, negative, fuzz/security and platform tests as appropriate.
7. **Automate:** regenerate reports and verify TODO/dependency/documentation links.
8. **Review:** inspect diff, public API, error behavior, compatibility claims and licensing.
9. **Close:** attach evidence and mark task done only after the acceptance criteria pass.

## Mandatory inventory questions

- What input and output contracts are owned here?
- Which crate is the source of truth for each type?
- Which dependencies are allowed and why?
- What platform-specific behavior is isolated behind a trait?
- What assumptions are unverified?
- What is deliberately out of scope?
- What tests prove correct behavior and safe failure?
