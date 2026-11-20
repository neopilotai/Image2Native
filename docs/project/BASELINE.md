# Repository Baseline and Change Control

## Baseline meaning

The baseline records the initial repository structure, exact workspace package/component inventory, protected architecture documents, automation entrypoints, selected SHA-256 hashes for governance control files and the project maturity declaration. It is not a claim that compiler functionality exists, and it is not a performance benchmark.

The control hashes cover the Cargo workspace/lockfile, dependency-boundary inventory/schema, repository automation and CI workflow. A change to one of these files fails `baseline verify` until it is reviewed and explicitly recaptured. Ordinary source and task progress are not locked by these hashes.

## Current declaration

- Product phase: foundation scaffold.
- Compiler pipeline: not implemented.
- OCI ingestion and filesystem reconstruction: not implemented.
- Linux/macOS/Windows execution backends: scaffold only.
- NIR and I2N artifact: draft specifications/contracts only.
- Automation: implemented for TODO validation, boundary inventory, baseline checks and generated reports.

## Commands

```bash
# Check current structure against approved baseline
python3 scripts/i2n.py baseline verify

# Capture a new baseline after an approved structural change
python3 scripts/i2n.py baseline capture --write

# Full validation
python3 scripts/i2n.py validate
```

A baseline refresh is a reviewed architecture operation. It must not be used to make a failed check pass without explaining the change in an ADR or pull request. Fix task and boundary violations before refreshing; the capture command refuses to snapshot an invalid inventory or task graph.
