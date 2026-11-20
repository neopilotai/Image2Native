# Agent Instructions for Image2Native

This file provides navigation and operating guidance for autonomous coding agents working on the Image2Native repository.

## Quick Start

1. **Read this file first** to understand how to navigate the codebase
2. **Read the codebase index** at `docs/engineering/CODEBASE-INDEX.md` for a complete repository overview
3. **Check implementation readiness** at `docs/engineering/IMPLEMENTATION-READINESS.md` for feature status and blockers
4. **Identify your task** from `docs/engineering/IMPLEMENTATION-START.md` or `project/work-items.json`
5. **Verify boundaries** before making changes using `python3 scripts/i2n.py validate`

## Documentation Navigation

### Essential Reading Order

1. **AGENTS.md** (this file) - Navigation guide
2. **docs/engineering/CODEBASE-INDEX.md** - Complete repository inventory and architecture
3. **docs/engineering/IMPLEMENTATION-READINESS.md** - Feature matrix and technical blockers
4. **docs/engineering/IMPLEMENTATION-START.md** - First concrete implementation task
5. **project/boundaries.json** - Dependency rules and ownership
6. **project/work-items.json** - Structured TODO list

### Reference Documentation

- **Architecture:** `docs/architecture/SYSTEM_ARCHITECTURE.md`, `docs/architecture/COMPILER_PIPELINE.md`
- **NIR Specification:** `docs/architecture/NIR_SPEC.md`
- **Platform Support:** `docs/platforms/PLATFORM_SUPPORT.md`
- **Security:** `docs/security/SECURITY_MODEL.md`, `docs/security/THREAT_MODEL.md`
- **Product Requirements:** `docs/product/PRODUCT_REQUIREMENTS.md`
- **Roadmap:** `docs/roadmap/ROADMAP.md`

## Package Ownership

### How to Find Package Responsibility

1. Look up the crate in `project/boundaries.json`
2. Check the `responsibility` field for the package's purpose
3. Check the `owner` field for the owning team
4. Check the `allowed_dependency_groups` field for permitted dependencies

### Dependency Lookup

To find allowed dependencies for a crate:

```bash
# Method 1: Read boundaries.json directly
grep -A 10 '"package": "i2n-oci"' project/boundaries.json

# Method 2: Use repository automation
python3 scripts/i2n.py inventory --check
```

The `allowed_dependency_groups` field lists which package groups this crate may depend on. Never add a dependency outside these groups without explicit architectural review.

## Boundary Verification

### Before Making Changes

Always run boundary verification before adding dependencies:

```bash
python3 scripts/i2n.py validate
```

This checks:
- Workspace membership compliance
- Dependency direction rules
- Boundary allowlist compliance
- Task graph consistency

### After Making Changes

Run the full validation suite:

```bash
# Regenerate reports
python3 scripts/i2n.py all --write

# Verify everything
python3 scripts/i2n.py validate

# Run Rust checks
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

## How to Validate Changes

### Step 1: Update Work Items

If your work corresponds to a task in `project/work-items.json`:

1. Find the task ID (e.g., I2N-0201)
2. Update the `status` field when appropriate
3. Add evidence paths to the `evidence` array when complete
4. Only mark `done` when all acceptance criteria are met with evidence

### Step 2: Regenerate Reports

```bash
python3 scripts/i2n.py all --write
```

This updates:
- `TODO.md` from `project/work-items.json`
- `reports/boundary-inventory.md`
- `reports/checklist.md`
- `reports/project-status.md`

### Step 3: Run Rust Checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
```

### Step 4: Verify Baseline

```bash
python3 scripts/i2n.py baseline verify
```

If baseline control files have changed (after structural changes), refresh explicitly:

```bash
python3 scripts/i2n.py baseline capture --write
```

## How to Update Implementation Tasks

### Adding a New Task

1. Add an entry to `project/work-items.json` following the schema in `schemas/work-items.schema.json`
2. Include all required fields: id, title, phase, priority, status, owner, scope, boundary, depends_on, acceptance_criteria, evidence
3. Set appropriate dependencies in `depends_on`
4. Run `python3 scripts/i2n.py checklist --write` to update TODO.md

### Updating Task Status

1. Find the task in `project/work-items.json`
2. Update `status` to `in_progress` when starting work
3. Update `status` to `done` only when all acceptance criteria are met
4. Add evidence paths to the `evidence` array
5. Run `python3 scripts/i2n.py checklist --write`

### Task Dependencies

Tasks must not be marked `done` if their dependencies are not `done`. The automation will detect and report this violation.

## Protected Files

### Control Files (Require Explicit Review)

- `Cargo.toml` - Workspace configuration
- `Cargo.lock` - Dependency lock file
- `project/boundaries.json` - Dependency rules
- `schemas/boundaries.schema.json` - Boundaries schema
- `scripts/i2n.py` - Repository automation
- `.github/workflows/ci.yml` - CI pipeline

### Protected Documentation

- All `docs/**/*.md` files
- `README.md`
- `WHITEPAPER.md`
- `BLUEPRINT.md`
- `TODO.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `SECURITY.md`

### Governance Data

- `project/project.json`
- `project/work-items.json`
- `project/baseline.json`
- `schemas/*.json`

To refresh the baseline after structural changes, run:

```bash
python3 scripts/i2n.py baseline capture --write
```

## How to Record Architectural Decisions

### Documentation Decisions

For decisions that affect architecture or boundaries:

1. Document in an ADR (Architecture Decision Record) in `docs/adr/`
2. Follow the existing ADR format (see `docs/adr/0001-oci-as-input-contract.md`)
3. Reference the ADR in relevant code comments
4. Update affected documentation if needed

### Implementation Decisions

For implementation-level decisions (e.g., library selection):

1. Document in the relevant crate's README.md
2. Record the decision rationale
3. Note alternatives considered and rejected
4. Update `project/work-items.json` evidence if the decision completes a task

## Common Workflows

### Implementing a New Crate Feature

1. Read the crate's README.md for purpose and scope
2. Check `project/boundaries.json` for allowed dependencies
3. Review existing implementation status in `docs/engineering/CODEBASE-INDEX.md`
4. Check acceptance criteria in `project/work-items.json`
5. Implement the feature
6. Add unit tests
7. Run `cargo fmt`, `cargo clippy`, `cargo test`
8. Update crate README.md if public API changed
9. Update `project/work-items.json` with evidence
10. Run `python3 scripts/i2n.py all --write`
11. Run `python3 scripts/i2n.py validate`

### Adding a Dependency

1. Check `project/boundaries.json` for the crate's `allowed_dependency_groups`
2. Verify the dependency's group is in the allowlist
3. Add the dependency to the crate's `Cargo.toml`
4. If the dependency is external, add it to `allowed_external_dependencies` in boundaries.json
5. Run `python3 scripts/i2n.py inventory --check` to verify
6. Run `cargo build` to test
7. Update the crate's README.md if needed

### Creating a New Crate

1. Add the crate to `Cargo.toml` workspace members
2. Create the crate directory with `Cargo.toml` and `src/lib.rs`
3. Add an entry to `project/boundaries.json` with group, owner, responsibility, and allowed dependencies
4. Add the crate to `project/baseline.json` required packages
5. Run `python3 scripts/i2n.py all --write`
6. Run `python3 scripts/i2n.py baseline capture --write` (structural change)
7. Commit the changes

## Troubleshooting

### Boundary Violations

If `python3 scripts/i2n.py validate` reports boundary violations:

1. Check the violation message for the specific dependency edge
2. Review `project/boundaries.json` for the crate's `allowed_dependency_groups`
3. Either remove the dependency or request an architectural review to update boundaries
4. Never suppress boundary violations

### Baseline Mismatches

If `python3 scripts/i2n.py baseline verify` reports changes:

1. Review the changed files listed
2. If changes are intentional (structural modifications), run `python3 scripts/i2n.py baseline capture --write`
3. If changes are unintentional, revert the files
4. Never automatically refresh the baseline without review

### Task Graph Issues

If the automation reports task graph issues:

1. Check for circular dependencies in `depends_on` fields
2. Ensure done tasks have evidence in the `evidence` array
3. Ensure blocked tasks have valid dependency IDs
4. Fix the issues in `project/work-items.json`
5. Run `python3 scripts/i2n.py checklist --write`

## Repository Automation Commands

```bash
# Show project status
python3 scripts/i2n.py status

# Check boundary compliance
python3 scripts/i2n.py inventory --check

# Generate/update TODO.md
python3 scripts/i2n.py checklist --write

# Verify baseline
python3 scripts/i2n.py baseline verify

# Refresh baseline (after structural changes)
python3 scripts/i2n.py baseline capture --write

# Run all validations
python3 scripts/i2n.py validate

# Regenerate all reports
python3 scripts/i2n.py all --write
```

## Make Targets

```bash
make status          # Show project status
make inventory       # Generate boundary inventory
make todo            # Generate TODO.md
make baseline-check  # Verify baseline
make check           # Run all checks
```

## Engineering Index Files

The following files in `docs/engineering/` provide machine-readable and detailed information:

- **CODEBASE-INDEX.md** - Complete repository overview, package inventory, API index
- **package-catalog.json** - Machine-readable package catalog with metadata
- **dependency-graph.mmd** - Mermaid visualization of dependency graph
- **IMPLEMENTATION-READINESS.md** - Feature matrix, technical blockers, missing contracts
- **IMPLEMENTATION-START.md** - First concrete implementation task with details
- **index-metadata.json** - Index generation metadata and statistics

## Key Architectural Rules

1. **OCI specs define input contract** - Do not deviate from OCI standards
2. **No Docker Engine dependency** - Must work without Docker Engine for ingestion
3. **Core crates no platform SDKs** - Platform-specific code stays in platform crates
4. **NIR is the boundary** - NIR separates image semantics from backend execution
5. **Fail closed on unknown** - Unknown required features must be rejected
6. **Pin digests, not tags** - Output artifacts must use immutable digests
7. **Untrusted input** - Treat all images and archives as hostile
8. **Least privilege** - Prefer rootless execution; no implicit privilege escalation
9. **Versioned contracts** - NIR and I2N must be versioned and tested
10. **Launcher ≠ native compilation** - Native launcher does not mean natively compiled Linux workload

## Contact and Support

For questions about:
- **Architecture decisions:** Review ADRs in `docs/adr/`
- **Boundary violations:** Check `project/boundaries.json` and this file
- **Task dependencies:** Check `project/work-items.json`
- **Build issues:** Run `cargo doctor` and check rust-toolchain.toml
- **Automation issues:** Check `scripts/i2n.py` and run with `--help`

## Index Freshness

This index was generated on 2026-11-20 (commit f42f10a). To regenerate the engineering index after significant implementation progress:

1. Update implementation status in all relevant crates
2. Re-run repository automation to gather current state
3. Update `docs/engineering/CODEBASE-INDEX.md` with current implementation
4. Update `docs/engineering/package-catalog.json` with current package data
5. Update `docs/engineering/dependency-graph.mmd` with current dependencies
6. Update `docs/engineering/IMPLEMENTATION-READINESS.md` with current feature matrix
7. Update `docs/engineering/IMPLEMENTATION-START.md` with next ready task
8. Update `docs/engineering/index-metadata.json` with current metadata
9. Verify all generated files and cross-references

---

**Remember:** The repository is in Phase 0/1 scaffold. Most crates are scaffolded with only status markers. Implementation follows the sequence in `docs/engineering/IMPLEMENTATION-READINESS.md`. Start with I2N-0202 (diagnostics) as documented in `docs/engineering/IMPLEMENTATION-START.md`.
