# Contributing

## Change process

1. Read `docs/project/WORKFLOW.md` and the relevant boundary ownership entry.
2. Select or create a work item in `project/work-items.json` before implementation.
3. Keep changes within the owning crate and allowed dependency direction.
4. Add unit, integration, negative and security tests appropriate to the change.
5. Update the relevant specification and acceptance evidence.
6. Run `python3 scripts/i2n.py all --write` and `python3 scripts/i2n.py validate`.
7. Run `cargo fmt --all -- --check`, `cargo clippy --workspace --all-targets -- -D warnings`, and `cargo test --workspace` when Rust is installed.
8. Include generated report changes in the pull request when inventory or status changes.

## Work item rules

- Every change links to one or more IDs from `project/work-items.json`.
- Mark an item `done` only when all acceptance criteria have evidence.
- Record blockers explicitly; do not mark blocked work as done.
- Keep tasks small enough to review and assign to one owning boundary.

## Dependency rules

- Domain and contract crates must not depend on platform SDKs or app crates.
- Compiler core must not depend on concrete OS backends.
- Platform implementations depend inward on contracts/domain types.
- CLI and app crates depend on public interfaces, not private backend internals.
- Do not add a generic `common` crate; put types in the owning domain crate.

## Pull request checklist

See `.github/pull_request_template.md`. All generated project reports must be current.
