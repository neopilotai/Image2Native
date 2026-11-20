# Contributing

## Workflow

1. Open/update an issue with problem statement and acceptance criteria.
2. Propose an ADR before changes to public schemas, backend contracts or trust boundaries.
3. Keep pull requests scoped to one subsystem where practical.
4. Add unit, integration and adversarial tests appropriate to the changed boundary.
5. Update docs, examples, compatibility matrix and release notes.
6. Run formatting, lint, tests and applicable platform checks.

## Rust guidelines

- Use newtypes for digests, normalized paths and platform IDs.
- Validate all untrusted values before use.
- Minimize unsafe code and document invariants.
- Use structured errors; do not panic on invalid input.
- Keep async work bounded and cancellation-aware.
- Avoid holding locks over long network or platform calls without a design reason.
- Redact credentials and secrets from diagnostics.

## Security-sensitive changes

Changes to archive extraction, image parsing, runtime privileges, host mounts, guest agent, signature verification, updates or native bridges require security review. Include abuse cases and threat-model updates in the PR.

## PR content

Describe intent, implementation, tests, affected platforms, security impact, compatibility impact, schema/ADR links and known limitations.

## Documentation language

Use precise terms: image packaging, native launcher, Linux guest, host-native executable and source compilation. Do not call guest-executed workloads “native compiled”. Mark unimplemented functionality as proposed or planned.
