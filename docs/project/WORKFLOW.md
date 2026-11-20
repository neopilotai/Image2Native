# Implementation Workflow and Automated Project Control

## Source-of-truth files

| Concern | Source of truth | Generated view |
|---|---|---|
| Tasks/checklist | `project/work-items.json` | `TODO.md`, `reports/checklist.md` |
| Crate boundaries | `project/boundaries.json` | `reports/boundary-inventory.md/.json` |
| Structural baseline | `project/baseline.json` | `reports/baseline.md` |
| Overall state | the three sources above | `reports/project-status.md` |

Do not hand-edit generated outputs. Edit source JSON, run `python3 scripts/i2n.py all --write`, then commit all generated report changes.

## Standard developer loop

```bash
# 1. See current work and boundary state
python3 scripts/i2n.py status

# 2. Select a task and inspect its boundary
python3 scripts/i2n.py checklist
python3 scripts/i2n.py inventory

# 3. Implement in the owning crate; add tests and evidence

# 4. Refresh generated outputs
python3 scripts/i2n.py all --write

# 5. Validate structure, links, task graph and dependency rules
python3 scripts/i2n.py validate

# 6. Run Rust checks
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

## Task state machine

`todo → in_progress → done` is the normal flow. Use `blocked` when a dependency, decision or external prerequisite prevents progress. A task cannot be `done` without evidence. Tasks may carry `depends_on` IDs; a task cannot close while a dependency is not done.

## Definition of done

A task is done only when:

- implementation is in its owning boundary;
- public contracts and error behavior are documented;
- positive, negative and relevant adversarial tests pass;
- resource limits and cancellation are addressed where relevant;
- generated inventory and TODO views are current;
- compatibility and security claims are supported by test evidence;
- the required acceptance evidence is recorded in `project/work-items.json`.

## Baseline discipline

The initial baseline is the checked-in structural contract, not a performance benchmark. It protects exact workspace membership, non-Cargo component membership, required files and hashes of key governance/CI control files. Use `baseline verify` during normal work. Use `baseline capture --write` only when an intentional architecture or control-file change is reviewed and accepted. The capture command refuses to bless invalid tasks or dependency boundaries. Do not refresh a baseline to hide an accidental regression.

## CI behavior

Pull requests run Python repository checks, Rust formatting, Clippy and workspace tests on supported CI hosts. CI is expected to fail on stale generated files, unknown workspace crates, undeclared dependency edges, invalid task dependencies or broken local documentation links.
