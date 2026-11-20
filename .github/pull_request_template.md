## Summary

<!-- What changed and why? -->

## Work items

- [ ] Linked work item(s): `I2N-____`

## Boundary and baseline

- [ ] Change is within the declared owning boundary.
- [ ] Dependency edges are allowed by `project/boundaries.json`.
- [ ] No protected baseline contract was changed unintentionally.

## Validation

- [ ] `python3 scripts/i2n.py all --write`
- [ ] `python3 scripts/i2n.py validate`
- [ ] `cargo fmt --all -- --check`
- [ ] `cargo clippy --workspace --all-targets -- -D warnings`
- [ ] `cargo test --workspace`
- [ ] Relevant platform/security tests

## Evidence and docs

- [ ] Acceptance evidence added to `project/work-items.json` when closing work.
- [ ] Specs, compatibility notes and error behavior updated.
- [ ] Generated TODO/inventory/baseline reports are current.
