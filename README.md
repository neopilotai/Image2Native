# Image2Native

**OCI image-to-application compiler and packaging system for Linux, macOS and Windows.**

> Convert OCI images into verifiable, distributable application bundles with platform-native launchers and explicit execution backends.

**Repository status:** Phase 0/1 scaffold. This repository contains architecture contracts, workspace/package boundaries, baseline inventory automation and TODO tracking. The image compiler and platform runtime are not implemented yet.

## Important product boundary

A Linux OCI image is not automatically a native Mach-O or PE program. Linux images on macOS and Windows require a Linux guest/compatibility backend (planned: Apple Virtualization.framework and WSL2). The host `.app`/`.exe` is a native launcher; the Linux workload remains a Linux process in its guest. Genuine host-native machine code belongs to the separate source-compilation path.

## Quick start

Requirements: Python 3.11+ for repository automation; Rust stable with `rustfmt` and `clippy` for Rust build/test commands.

```bash
# Inspect current project status
python3 scripts/i2n.py status

# Regenerate inventory, TODO and reports
python3 scripts/i2n.py all --write

# Run repository checks (Rust checks run when Cargo is installed)
python3 scripts/i2n.py validate

# Rust checks
cargo fmt --all -- --check
cargo test --workspace
cargo clippy --workspace --all-targets -- -D warnings
```

Or use `make status`, `make inventory`, `make todo`, `make baseline-check`, and `make check`. Initialize a local Git repository with `git init -b main`; the archive intentionally excludes `.git` metadata.

## Automation as the source of truth

- `project/work-items.json`: structured checklist/TODO source of truth.
- `project/boundaries.json`: crate ownership and dependency boundary inventory.
- `project/baseline.json`: initial repository contract and structural baseline.
- `reports/`: generated, reviewable Markdown/JSON inventories.
- `TODO.md`: generated developer-facing task list; edit `project/work-items.json`, not this file.

Run `python3 scripts/i2n.py all --write` after changing the structured project data.

## Documentation

- [White Paper](WHITEPAPER.md)
- [Engineering Blueprint](BLUEPRINT.md)
- [Documentation Index](docs/index.md)
- [Product Requirements](docs/product/PRODUCT_REQUIREMENTS.md)
- [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Compiler Pipeline](docs/architecture/COMPILER_PIPELINE.md)
- [NIR Specification](docs/architecture/NIR_SPEC.md)
- [Backend Contract](docs/architecture/BACKEND_CONTRACT.md)
- [I2N Artifact Format](docs/architecture/ARTIFACT_FORMAT.md)
- [Platform Support](docs/platforms/PLATFORM_SUPPORT.md)
- [Security Model](docs/security/SECURITY_MODEL.md) · [Threat Model](docs/security/THREAT_MODEL.md)
- [CLI Specification](docs/developer/CLI_SPEC.md) · [Repository Layout](docs/developer/REPOSITORY_LAYOUT.md)
- [Implementation Workflow](docs/project/WORKFLOW.md) · [Boundary Inventory](docs/project/BOUNDARIES.md) · [Baseline](docs/project/BASELINE.md)
- [Roadmap](docs/roadmap/ROADMAP.md) · [ADRs](docs/adr/)

## First vertical slice

OCI resolve → digest verify → layer decode → RootFS reconstruction → NIR → compatibility report → Linux OCI runtime bundle → I2N artifact → launch.

## Scope boundaries

In scope: OCI ingestion, content verification, filesystem reconstruction, compatibility analysis, Linux execution, macOS/Windows Linux-guest packaging, signed artifacts, SBOM/provenance and optional source compilation.

Out of first release: generic binary translation, kernel emulation, guaranteed support for all container images, Docker Desktop parity, automatic privileged execution, full Compose support, Kubernetes orchestration and GUI-first delivery.

## License

License selection is an explicit pre-release task. Do not redistribute this scaffold as a licensed product until `LICENSE` and third-party notice policy are approved.
