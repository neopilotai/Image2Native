# Image2Native Codebase Index

**Generated:** 2026-11-20  
**Git commit:** f42f10a  
**Git branch:** main  
**Workspace packages:** 34  
**Source files:** 180  
**Indexed packages:** 34  

This index provides a complete, evidence-based inventory of the Image2Native repository. It is the authoritative reference for autonomous coding agents working on this codebase.

## Repository Overview

Image2Native is a Rust-first OCI image-to-application compiler and packaging system for Linux, macOS, and Windows. The repository is currently in **Phase 0/1 scaffold** status: architecture contracts, workspace/package boundaries, baseline inventory automation, and TODO tracking are complete. The compiler pipeline and platform runtime are **not implemented yet**.

### Current Status

- **Maturity:** foundation-scaffold
- **Compiler implemented:** false
- **OCI ingestion implemented:** false
- **RootFS compiler implemented:** false
- **Platform backends implemented:** false
- **Automation implemented:** true

### Git Working Tree Status

- Branch: main (origin/main)
- Uncommitted changes: README.md (modified), docs/index.md (modified), flycheck artifacts (modified)
- Deleted files: DOCS-MANIFEST.json, DOCUMENTATION-CHECKLIST.md, FILE-MANIFEST.json (no longer part of current structure)

### Toolchain

- **Rust:** 1.100.0 (0ef1bc386 2026-11-09)
- **Cargo:** 1.100.0 (3acc79c0c 2026-11-05)
- **Python:** 3.11.2
- **Git:** 2.56.1
- **Minimum Rust version:** 1.85 (defined in workspace)

## Complete Workspace Catalog

### Package Inventory

The workspace contains 34 packages organized into domain, foundation, OCI ingestion, filesystem, analysis, compiler, artifact, runtime, platform, and security groups.

| Package | Path | Kind | Group | Owner | Status | Library Target | Binary Targets |
|---------|------|------|-------|-------|--------|----------------|----------------|
| i2n-model | crates/i2n-model | library | domain | domain | PARTIAL | i2n_model | - |
| i2n-diagnostics | crates/i2n-diagnostics | library | foundation | foundation | PARTIAL | i2n_diagnostics | - |
| i2n-config | crates/i2n-config | library | foundation | foundation | SCAFFOLDED | i2n_config | - |
| i2n-protocol | crates/i2n-protocol | library | foundation | foundation | SCAFFOLDED | i2n_protocol | - |
| i2n-digest | crates/i2n-digest | library | content | content | SCAFFOLDED | i2n_digest | - |
| i2n-oci | crates/i2n-oci | library | oci | oci | SCAFFOLDED | i2n_oci | - |
| i2n-registry | crates/i2n-registry | library | oci | oci | SCAFFOLDED | i2n_registry | - |
| i2n-fetcher | crates/i2n-fetcher | library | content | content | SCAFFOLDED | i2n_fetcher | - |
| i2n-cache | crates/i2n-cache | library | content | content | SCAFFOLDED | i2n_cache | - |
| i2n-layer | crates/i2n-layer | library | filesystem | filesystem | SCAFFOLDED | i2n_layer | - |
| i2n-unpack | crates/i2n-unpack | library | filesystem | filesystem | SCAFFOLDED | i2n_unpack | - |
| i2n-rootfs | crates/i2n-rootfs | library | filesystem | filesystem | SCAFFOLDED | i2n_rootfs | - |
| i2n-filesystem | crates/i2n-filesystem | library | filesystem | filesystem | SCAFFOLDED | i2n_filesystem | - |
| i2n-inspector | crates/i2n-inspector | library | analysis | analysis | SCAFFOLDED | i2n_inspector | - |
| i2n-ir | crates/i2n-ir | library | contracts | contracts | PARTIAL | i2n_ir | - |
| i2n-analyzer | crates/i2n-analyzer | library | analysis | analysis | SCAFFOLDED | i2n_analyzer | - |
| i2n-compiler | crates/i2n-compiler | library | compiler | compiler | SCAFFOLDED | i2n_compiler | - |
| i2n-artifact | crates/i2n-artifact | library | artifact | artifact | SCAFFOLDED | i2n_artifact | - |
| i2n-archive | crates/i2n-archive | library | artifact | artifact | SCAFFOLDED | i2n_archive | - |
| i2n-sbom | crates/i2n-sbom | library | trust | trust | SCAFFOLDED | i2n_sbom | - |
| i2n-signing | crates/i2n-signing | library | trust | trust | SCAFFOLDED | i2n_signing | - |
| i2n-provenance | crates/i2n-provenance | library | trust | trust | SCAFFOLDED | i2n_provenance | - |
| i2n-platform | crates/i2n-platform | library | platform-contract | platform-contract | PARTIAL | i2n_platform | - |
| i2n-runtime | crates/i2n-runtime | library | runtime | runtime | SCAFFOLDED | i2n_runtime | - |
| i2n-supervisor | crates/i2n-supervisor | library | runtime | runtime | SCAFFOLDED | i2n_supervisor | - |
| i2n-network | crates/i2n-network | library | runtime | runtime | SCAFFOLDED | i2n_network | - |
| i2n-storage | crates/i2n-storage | library | runtime | runtime | SCAFFOLDED | i2n_storage | - |
| i2n-security | crates/i2n-security | library | security | security | SCAFFOLDED | i2n_security | - |
| i2n-platform-linux | crates/i2n-platform-linux | library | platform-linux | platform-linux | SCAFFOLDED | i2n_platform_linux | - |
| i2n-platform-macos | crates/i2n-platform-macos | library | platform-macos | platform-macos | SCAFFOLDED | i2n_platform_macos | - |
| i2n-platform-windows | crates/i2n-platform-windows | library | platform-windows | platform-windows | SCAFFOLDED | i2n_platform_windows | - |
| image2native-cli | apps/image2native-cli | application | app | application | PARTIAL | - | image2native-cli |
| image2native-launcher | apps/image2native-launcher | application | app | application | SCAFFOLDED | - | image2native-launcher |
| image2native-daemon | apps/image2native-daemon | application | app | application | SCAFFOLDED | - | image2native-daemon |

### Status Definitions

- **IMPLEMENTED:** Functional code and supporting evidence exist
- **PARTIAL:** Some implementation exists (core types with basic functionality)
- **SCAFFOLDED:** Structure or interfaces exist, but implementation is incomplete
- **MISSING:** No relevant implementation found
- **BLOCKED:** A prerequisite or decision prevents progress

## Directory Ownership

### Cargo Workspace Structure

```
Image2Native/
├── crates/           # 31 library crates
│   ├── i2n-model/    # Domain types (partial)
│   ├── i2n-diagnostics/ # Diagnostics (partial)
│   ├── i2n-ir/       # NIR contract (partial)
│   ├── i2n-platform/ # Platform traits (partial)
│   └── [27 other scaffolded crates]
├── apps/             # 3 application binaries
│   ├── image2native-cli/   # CLI (partial)
│   ├── image2native-launcher/ # Launcher (scaffold)
│   └── image2native-daemon/  # Daemon (scaffold)
├── platform/         # Platform-specific native bridges (placeholders)
│   ├── linux/        # Linux bridge code (empty)
│   ├── macos/        # macOS bridge code (empty)
│   └── windows/      # Windows bridge code (empty)
├── guest/            # Linux guest runtime (placeholder)
├── schemas/          # JSON schemas for contracts
├── tests/            # Test harnesses (empty directories)
├── docs/             # Documentation
├── project/          # Governance data
└── scripts/          # Repository automation
```

### Non-Cargo Repository Components

| Component ID | Kind | Owner | Path | Status |
|--------------|------|-------|------|--------|
| platform-linux-bridge | native-bridge | platform-linux | platform/linux | PLACEHOLDER |
| platform-macos-bridge | native-bridge | platform-macos | platform/macos | PLACEHOLDER |
| platform-windows-bridge | native-bridge | platform-windows | platform/windows | PLACEHOLDER |
| linux-guest-runtime | guest-runtime | guest-runtime | guest | PLACEHOLDER |
| project-governance | governance-data | foundation | project | IMPLEMENTED |
| project-automation | automation | foundation | scripts | IMPLEMENTED |
| contract-schemas | schemas | contracts | schemas | IMPLEMENTED |
| quality-harness | test-harness | quality | tests | PLACEHOLDER |
| documentation | documentation | docs | docs | IMPLEMENTED |

## Package Responsibilities

### Domain and Foundation

**i2n-model** (domain) - <ref_file file="/workspaces/Image2Native/crates/i2n-model/src/lib.rs" />
- Owns stable IDs, platform types, digests, image references
- **Implemented:** TargetPlatform (os/arch), Digest (algorithm:encoded), ParseTargetError
- **Tests:** Target parsing, digest validation present
- **Public API:** OperatingSystem, Architecture, TargetPlatform, Digest

**i2n-diagnostics** (foundation) - <ref_file file="/workspaces/Image2Native/crates/i2n-diagnostics/src/lib.rs" />
- Owns structured diagnostics, stage identifiers, safe error metadata
- **Implemented:** Stage enum (Resolve, Fetch, Decode, Rootfs, Normalize, Analyze, Plan, Link, Verify, Run), Diagnostic struct
- **Public API:** Stage, Diagnostic (with code, stage, message, retryable, remediation)

**i2n-config** (foundation) - SCAFFOLDED
- Owns validated compiler and runtime configuration
- **Implementation:** Status marker only

**i2n-protocol** (foundation) - SCAFFOLDED
- Owns versioned host/guest and daemon IPC message contracts
- **Implementation:** Status marker only

### Content and OCI

**i2n-digest** (content) - SCAFFOLDED
- Owns content digest parsing and verification primitives
- **Implementation:** Status marker only

**i2n-oci** (oci) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-oci/src/lib.rs" />
- Owns OCI image/index/manifest/config models and parsing
- **Implementation:** Status marker only

**i2n-registry** (oci) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-registry/src/lib.rs" />
- Owns OCI Distribution API, registry auth, manifest resolution
- **Implementation:** Status marker only

**i2n-fetcher** (content) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-fetcher/src/lib.rs" />
- Owns bounded blob transfer, retries, cancellation
- **Implementation:** Status marker only

**i2n-cache** (content) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-cache/src/lib.rs" />
- Owns verified content-addressed cache storage and pruning
- **Implementation:** Status marker only

### Filesystem

**i2n-layer** (filesystem) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-layer/src/lib.rs" />
- Owns layer decoding and changeset/whiteout semantics
- **Implementation:** Status marker only

**i2n-unpack** (filesystem) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-unpack/src/lib.rs" />
- Owns safe archive and layer unpacking policies
- **Implementation:** Status marker only

**i2n-rootfs** (filesystem) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-rootfs/src/lib.rs" />
- Owns logical root filesystem reconstruction
- **Implementation:** Status marker only

**i2n-filesystem** (filesystem) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-filesystem/src/lib.rs" />
- Owns filesystem abstractions and metadata normalization
- **Implementation:** Status marker only

### Analysis and Contracts

**i2n-inspector** (analysis) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-inspector/src/lib.rs" />
- Owns static image/process/dependency inspection
- **Implementation:** Status marker only

**i2n-ir** (contracts) - PARTIAL - <ref_file file="/workspaces/Image2Native/crates/i2n-ir/src/lib.rs" />
- Owns the versioned Native Image Representation (NIR)
- **Implemented:** ImageIdentity (source_reference, manifest_digest), ProcessSpec (entrypoint, arguments, working_directory, user), NativeImage (identity, source_platform, requested_target, process)
- **Public API:** ImageIdentity, ProcessSpec, NativeImage
- **Status:** Draft types only; NIR v0.1 schema exists at <ref_file file="/workspaces/Image2Native/schemas/nir-v0.1.schema.json" />

**i2n-analyzer** (analysis) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-analyzer/src/lib.rs" />
- Owns compatibility, policy and target capability analysis
- **Implementation:** Status marker only

### Compiler and Artifact

**i2n-compiler** (compiler) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-compiler/src/lib.rs" />
- Owns compile graph orchestration, stage contracts, execution planning
- **Implementation:** Status marker only

**i2n-artifact** (artifact) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-artifact/src/lib.rs" />
- Owns I2N bundle manifest, payload graph, reader/writer
- **Implementation:** Status marker only
- **Schema:** I2N artifact v1 schema at <ref_file file="/workspaces/Image2Native/schemas/i2n-artifact-v1.schema.json" />

**i2n-archive** (artifact) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-archive/src/lib.rs" />
- Owns deterministic artifact archive and extraction
- **Implementation:** Status marker only

### Trust and Security

**i2n-sbom** (trust) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-sbom/src/lib.rs" />
- Owns SPDX SBOM generation and validation
- **Implementation:** Status marker only

**i2n-signing** (trust) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-signing/src/lib.rs" />
- Owns artifact signature and verification adapters
- **Implementation:** Status marker only

**i2n-provenance** (trust) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-provenance/src/lib.rs" />
- Owns source/build provenance and attestations
- **Implementation:** Status marker only

**i2n-security** (security) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-security/src/lib.rs" />
- Owns policy evaluation and security boundary helpers
- **Implementation:** Status marker only

### Platform and Runtime

**i2n-platform** (platform-contract) - PARTIAL - <ref_file file="/workspaces/Image2Native/crates/i2n-platform/src/lib.rs" />
- Owns platform backend traits and capability contracts
- **Implemented:** ExecutionKind (NativeLinux, LinuxVirtualMachine, WindowsContainer), BackendCapabilities, PlatformBackend trait
- **Public API:** ExecutionKind, BackendCapabilities, PlatformBackend

**i2n-runtime** (runtime) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-runtime/src/lib.rs" />
- Owns application lifecycle semantics and runtime plans
- **Implementation:** Status marker only

**i2n-supervisor** (runtime) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-supervisor/src/lib.rs" />
- Owns process/VM supervision, events, instance state
- **Implementation:** Status marker only

**i2n-network** (runtime) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-network/src/lib.rs" />
- Owns host/guest networking policy and port mapping
- **Implementation:** Status marker only

**i2n-storage** (runtime) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-storage/src/lib.rs" />
- Owns application state, volumes, writable overlays
- **Implementation:** Status marker only

**i2n-platform-linux** (platform-linux) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-platform-linux/src/lib.rs" />
- Owns Linux native runtime adapter and Linux-specific integration
- **Implementation:** Status marker only

**i2n-platform-macos** (platform-macos) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-platform-macos/src/lib.rs" />
- Owns Apple Virtualization.framework adapter and native bridge
- **Implementation:** Status marker only

**i2n-platform-windows** (platform-windows) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/crates/i2n-platform-windows/src/lib.rs" />
- Owns WSL2/HCS adapter and Windows native bridge
- **Implementation:** Status marker only

### Applications

**image2native-cli** (application) - PARTIAL - <ref_file file="/workspaces/Image2Native/apps/image2native-cli/src/main.rs" />
- Command-line interface and user-facing orchestration
- **Implemented:** Basic CLI with version, targets, doctor, help commands
- **Dependencies:** i2n-model, i2n-diagnostics
- **Status:** Functional scaffold only; compile command reports not implemented

**image2native-launcher** (application) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/apps/image2native-launcher/src/main.rs" />
- Native per-platform application launcher
- **Implementation:** Placeholder main only

**image2native-daemon** (application) - SCAFFOLDED - <ref_file file="/workspaces/Image2Native/apps/image2native-daemon/src/main.rs" />
- Optional local service; never required by core CLI
- **Implementation:** Placeholder main only

## Public API Inventory

### Domain Types (i2n-model)

**OperatingSystem** enum
- Variants: Linux, Macos, Windows
- File: crates/i2n-model/src/lib.rs:7-11

**Architecture** enum
- Variants: X86_64, Aarch64
- File: crates/i2n-model/src/lib.rs:14-17

**TargetPlatform** struct
- Fields: os: OperatingSystem, architecture: Architecture
- Implements: FromStr, Display
- File: crates/i2n-model/src/lib.rs:20-23

**Digest** struct
- Fields: algorithm: String, encoded: String
- Implements: FromStr
- File: crates/i2n-model/src/lib.rs:91-94

**ParseTargetError** struct
- Implements: Display, Error
- File: crates/i2n-model/src/lib.rs:26-34

### Diagnostics (i2n-diagnostics)

**Stage** enum
- Variants: Resolve, Fetch, Decode, Rootfs, Normalize, Analyze, Plan, Link, Verify, Run
- File: crates/i2n-diagnostics/src/lib.rs:6-17

**Diagnostic** struct
- Fields: code: &'static str, stage: Stage, message: String, retryable: bool, remediation: Option<String>
- Methods: new(), with_remediation()
- Implements: Display, Error
- File: crates/i2n-diagnostics/src/lib.rs:20-26

### NIR Contract (i2n-ir)

**ImageIdentity** struct
- Fields: source_reference: String, manifest_digest: Digest
- File: crates/i2n-ir/src/lib.rs:6-9

**ProcessSpec** struct
- Fields: entrypoint: Vec<String>, arguments: Vec<String>, working_directory: Option<String>, user: Option<String>
- Implements: Default
- File: crates/i2n-ir/src/lib.rs:12-17

**NativeImage** struct
- Fields: identity: ImageIdentity, source_platform: String, requested_target: TargetPlatform, process: ProcessSpec
- File: crates/i2n-ir/src/lib.rs:20-24

### Platform Contract (i2n-platform)

**ExecutionKind** enum
- Variants: NativeLinux, LinuxVirtualMachine, WindowsContainer
- File: crates/i2n-platform/src/lib.rs:4-8

**BackendCapabilities** struct
- Fields: backend_id: &'static str, execution_kind: ExecutionKind, supports_linux_images: bool, supports_windows_images: bool
- File: crates/i2n-platform/src/lib.rs:11-16

**PlatformBackend** trait
- Method: capabilities() -> BackendCapabilities
- File: crates/i2n-platform/src/lib.rs:19-21

## Dependency Architecture

### Current Dependency Graph

The workspace currently has **zero internal dependency edges**. All crates except the following have no declared dependencies:

- **i2n-ir** depends on: i2n-model
- **i2n-platform-linux** depends on: i2n-diagnostics, i2n-model, i2n-platform
- **i2n-platform-macos** depends on: i2n-diagnostics, i2n-model, i2n-platform
- **i2n-platform-windows** depends on: i2n-diagnostics, i2n-model, i2n-platform
- **i2n-security** depends on: i2n-diagnostics, i2n-model, i2n-provenance, i2n-sbom, i2n-signing
- **image2native-cli** depends on: i2n-diagnostics, i2n-model

### Allowed Dependency Groups (from boundaries.json)

Permitted dependency directions by group:

- **domain:** No dependencies allowed (leaf)
- **foundation:** May depend on domain
- **content:** May depend on domain, foundation
- **oci:** May depend on domain, foundation
- **filesystem:** May depend on domain, foundation, content
- **analysis:** May depend on domain, foundation, oci, filesystem
- **contracts:** May depend on domain, foundation
- **compiler:** May depend on domain, foundation, oci, content, filesystem, analysis, contracts, artifact
- **artifact:** May depend on domain, foundation, contracts, content
- **trust:** May depend on domain, foundation, contracts
- **platform-contract:** May depend on domain, foundation
- **runtime:** May depend on domain, foundation, platform-contract, artifact
- **security:** May depend on domain, foundation, trust
- **platform-linux:** May depend on domain, foundation, platform-contract, runtime
- **platform-macos:** May depend on domain, foundation, platform-contract, runtime
- **platform-windows:** May depend on domain, foundation, platform-contract, runtime
- **app:** May depend on all groups except app

### Dependency Violations

**Current violations:** 0

## Compiler Pipeline Status

### Architectural Pipeline

The documented compiler pipeline (from <ref_file file="/workspaces/Image2Native/docs/architecture/COMPILER_PIPELINE.md" />):

```
Image Reference
       |
       v
OCI Resolver
       |
       v
Registry Client
       |
       v
Fetcher -> Digest Verification -> Content Cache
       |
       v
Layer Decoder -> Safe Layer Applier -> Logical RootFS
       |
       v
Image Inspector -> NIR Compiler
       |
       v
Compatibility Analyzer + Policy Engine
       |
       v
Explicit Backend Execution Plan
       |
       v
Artifact Linker
       |
       v
Verify / Install / Run
```

### Stage Implementation Status

| Stage | Owner Crate | Status | Evidence |
|-------|-------------|--------|----------|
| Resolve | i2n-oci, i2n-registry | SCAFFOLDED | Status markers only |
| Fetch | i2n-fetcher | SCAFFOLDED | Status marker only |
| Digest Verification | i2n-digest | SCAFFOLDED | Status marker only |
| Content Cache | i2n-cache | SCAFFOLDED | Status marker only |
| Layer Decode | i2n-layer | SCAFFOLDED | Status marker only |
| Layer Applier | i2n-unpack | SCAFFOLDED | Status marker only |
| RootFS Reconstruction | i2n-rootfs | SCAFFOLDED | Status marker only |
| Image Inspector | i2n-inspector | SCAFFOLDED | Status marker only |
| NIR Compiler | i2n-ir | PARTIAL | Draft types exist |
| Compatibility Analyzer | i2n-analyzer | SCAFFOLDED | Status marker only |
| Backend Planner | i2n-compiler | SCAFFOLDED | Status marker only |
| Artifact Linker | i2n-artifact | SCAFFOLDED | Status marker only |
| Runtime Manager | i2n-runtime | SCAFFOLDED | Status marker only |

### Platform Support Status

| Platform | Backend Crate | Implementation | Integration |
|----------|---------------|----------------|-------------|
| Linux (native) | i2n-platform-linux | SCAFFOLDED | platform/linux/ empty |
| macOS (guest) | i2n-platform-macos | SCAFFOLDED | platform/macos/ empty |
| Windows (WSL2) | i2n-platform-windows | SCAFFOLDED | platform/windows/ empty |
| Windows (HCS) | i2n-platform-windows | SCAFFOLDED | Not planned for v1 |

## Runtime Execution Flow

### Current CLI Execution

**Entry point:** apps/image2native-cli/src/main.rs

**Commands:**
- `version` / `--version`: Show version (implemented)
- `targets`: List supported target triples (implemented, uses i2n-model)
- `doctor`: Show host/tooling status (implemented, placeholder)
- `compile`: Reserved (reports not implemented)
- `help`: Show help (implemented)

**No actual compiler execution path exists.** The CLI is a functional scaffold that validates toolchain and parses targets, but does not execute the compiler pipeline.

### Intended Execution Flow (when implemented)

```
CLI parse
  |
  v
Command dispatch
  |
  v
Image Resolver (i2n-oci, i2n-registry)
  |
  v
Fetcher (i2n-fetcher) -> Cache (i2n-cache)
  |
  v
Layer Engine (i2n-layer, i2n-unpack)
  |
  v
RootFS Compiler (i2n-rootfs)
  |
  v
Inspector (i2n-inspector) -> NIR (i2n-ir)
  |
  v
Analyzer (i2n-analyzer)
  |
  v
Compiler (i2n-compiler) -> Backend Selection
  |
  v
Artifact Builder (i2n-artifact)
  |
  v
Output (I2N bundle)
```

## Testing and Build Instructions

### Build Commands

```bash
# Check formatting
cargo fmt --all -- --check

# Run tests
cargo test --workspace

# Run linter
cargo clippy --workspace --all-targets -- -D warnings

# Run repository automation
python3 scripts/i2n.py status
python3 scripts/i2n.py validate
python3 scripts/i2n.py all --write
```

### Make Targets

- `make status`: Show project status
- `make inventory`: Generate boundary inventory
- `make todo`: Generate TODO.md
- `make baseline-check`: Verify baseline
- `make check`: Run all checks

### Test Infrastructure

**Directories:**
- tests/unit/ - Unit tests (empty)
- tests/integration/ - Integration tests (empty)
- tests/fixtures/ - Test fixtures (empty)
- tests/golden/ - Golden test outputs (empty)
- tests/security/ - Security tests (empty)
- tests/compatibility/ - Compatibility tests (empty)
- tests/python/ - Python automation tests (has test_repo_automation.py)

**Status:** Test harness exists but contains no tests yet.

## Existing Implementation

### What Works

1. **Workspace foundation**: Complete workspace with 34 packages, proper dependency direction enforcement
2. **Domain types**: TargetPlatform and Digest parsing with tests
3. **Diagnostics**: Stage identifiers and Diagnostic struct
4. **NIR draft**: Basic NIR types (ImageIdentity, ProcessSpec, NativeImage)
5. **Platform contract**: ExecutionKind, BackendCapabilities, PlatformBackend trait
6. **CLI scaffold**: Functional CLI with version, targets, doctor commands
7. **Repository automation**: Python scripts for TODO, boundary, baseline management
8. **Documentation**: Complete architecture docs, specs, ADRs
9. **CI**: GitHub Actions workflow for fmt, clippy, tests
10. **Schema definitions**: NIR v0.1, I2N artifact v1, work-items, boundaries schemas

### What Is Partial

1. **i2n-model**: Basic platform types and digest parsing; missing image reference parsing, more sophisticated platform detection
2. **i2n-diagnostics**: Basic diagnostic struct; missing error codes, retryability logic, secret redaction
3. **i2n-ir**: Draft NIR types; missing full NIR v0.1 specification implementation, serialization, validation
4. **i2n-platform**: Basic trait contract; missing capability detection, backend registration
5. **image2native-cli**: Basic commands only; missing compile command implementation, argument parsing, error handling

### What Is Only Scaffolded

All other crates (27) have only status markers indicating scaffold status. No functional implementation exists for:
- OCI ingestion (i2n-oci, i2n-registry, i2n-fetcher, i2n-cache)
- Filesystem (i2n-layer, i2n-unpack, i2n-rootfs, i2n-filesystem)
- Analysis (i2n-inspector, i2n-analyzer)
- Compiler (i2n-compiler)
- Artifact (i2n-artifact, i2n-archive)
- Trust (i2n-sbom, i2n-signing, i2n-provenance)
- Runtime (i2n-runtime, i2n-supervisor, i2n-network, i2n-storage)
- Security (i2n-security)
- Platform backends (i2n-platform-linux, i2n-platform-macos, i2n-platform-windows)
- Applications (image2native-launcher, image2native-daemon)

## Missing Implementation

### Critical Path

The following compiler subsystems have **no implementation**:

1. **OCI reference parsing** (i2n-oci)
2. **Registry client** (i2n-registry)
3. **Blob fetching** (i2n-fetcher)
4. **Content cache** (i2n-cache)
5. **Layer decoder** (i2n-layer)
6. **Archive unpacking** (i2n-unpack)
7. **RootFS reconstruction** (i2n-rootfs)
8. **Filesystem abstractions** (i2n-filesystem)
9. **Image inspector** (i2n-inspector)
10. **Compatibility analyzer** (i2n-analyzer)
11. **Compiler orchestration** (i2n-compiler)
12. **Artifact format** (i2n-artifact)
13. **Linux OCI runtime integration** (i2n-platform-linux)
14. **macOS Virtualization integration** (i2n-platform-macos)
15. **Windows WSL2 integration** (i2n-platform-windows)

### Supporting Components

Also missing:
- Digest verification (i2n-digest)
- Configuration (i2n-config)
- Protocol contracts (i2n-protocol)
- Archive handling (i2n-archive)
- SBOM generation (i2n-sbom)
- Signing (i2n-signing)
- Provenance (i2n-provenance)
- Runtime lifecycle (i2n-runtime)
- Process supervision (i2n-supervisor)
- Networking (i2n-network)
- Storage (i2n-storage)
- Security policy (i2n-security)
- Native launcher (image2native-launcher)
- Daemon (image2native-daemon)

## Critical Architectural Boundaries

### Non-Negotiable Rules (from BLUEPRINT.md)

1. OCI image and distribution specifications define the image input contract
2. Docker Engine must not be required for normal image ingestion, compilation, inspection, or packaged execution
3. Core crates must not depend on macOS or Windows SDKs
4. NIR separates source image semantics from backend-specific execution
5. Unknown required features and unsupported requirements fail closed
6. Tags are mutable names; output artifacts pin resolved immutable digests
7. Images and archives are untrusted input
8. Rootless and least-privilege execution is preferred; no implicit privilege escalation
9. NIR and I2N are versioned, tested contracts
10. A native launcher must not be described as a natively compiled Linux workload

### Dependency Direction Rules

- Core crates must not depend on concrete platform implementation crates
- Platform-specific native APIs remain inside platform/<os> and i2n-platform-<os>
- Application crates are composition roots and are never dependencies of core crates
- Only explicitly allowed dependency groups may be referenced by a workspace crate
- Local path dependencies must resolve to declared workspace members

### Current Boundary Compliance

**Status:** PASS

- Workspace packages: 34 (matches baseline)
- Repository components: 9 (matches baseline)
- Boundary violations: 0
- Dependency edge violations: 0
- Task graph issues: 0

## Source References and Line Numbers

### Key Files by Subsystem

**Domain:**
- crates/i2n-model/src/lib.rs (146 lines)

**Diagnostics:**
- crates/i2n-diagnostics/src/lib.rs (51 lines)

**NIR:**
- crates/i2n-ir/src/lib.rs (25 lines)
- schemas/nir-v0.1.schema.json

**Platform:**
- crates/i2n-platform/src/lib.rs (21 lines)
- crates/i2n-platform-linux/src/lib.rs (10 lines)
- crates/i2n-platform-macos/src/lib.rs (9 lines)
- crates/i2n-platform-windows/src/lib.rs (9 lines)

**CLI:**
- apps/image2native-cli/src/main.rs (66 lines)

**Governance:**
- project/boundaries.json (634 lines)
- project/work-items.json (530 lines)
- project/baseline.json

**Automation:**
- scripts/i2n.py (534 lines)

**Documentation:**
- docs/architecture/SYSTEM_ARCHITECTURE.md (108 lines)
- docs/architecture/COMPILER_PIPELINE.md (75 lines)
- docs/architecture/NIR_SPEC.md (99 lines)
- docs/architecture/BACKEND_CONTRACT.md
- docs/architecture/ARTIFACT_FORMAT.md
- WHITEPAPER.md (105 lines)
- BLUEPRINT.md (219 lines)

## Platform Support

### Linux

**Status:** SCAFFOLDED
- Backend crate: i2n-platform-linux
- Native bridge: platform/linux/ (empty)
- Planned: OCI runtime integration (runc or youki), namespaces, cgroups, seccomp, capabilities, rootless execution

### macOS

**Status:** SCAFFOLDED
- Backend crate: i2n-platform-macos
- Native bridge: platform/macos/ (empty)
- Planned: Apple Virtualization.framework, Linux guest, Virtio devices, .app packaging, signing

### Windows

**Status:** SCAFFOLDED
- Backend crate: i2n-platform-windows
- Native bridge: platform/windows/ (empty)
- Planned: WSL2 for Linux images, future HCS for Windows-native images

## Technical Blockers

### Prerequisites

1. **Rust toolchain verification (I2N-0101):** Rust stable, rustfmt, and Clippy must pass on Linux, macOS, and Windows CI
2. **Domain model completion (I2N-0201):** Target triples, digest validation, image references with fixtures
3. **Diagnostics framework (I2N-0202):** Stable error codes, retryability, secret redaction

### Missing Decisions

1. **External dependencies:** No third-party crates are used yet; decisions needed for HTTP clients, digest libraries, compression, OCI parsing
2. **Runtime selection:** Decision needed on which OCI runtime to integrate (runc vs youki)
3. **Immutable rootfs format:** Decision needed on SquashFS vs EROFS for immutable rootfs
4. **Guest kernel version:** Decision needed for pinned Linux guest kernel and init system
5. **Signing scheme:** Decision needed on Cosign vs other Sigstore-compatible approach

### Architectural Gaps

1. **No dependency edges:** Most crates have no dependencies; dependency graph needs to be populated as implementation progresses
2. **No test fixtures:** All test directories are empty
3. **No integration:** No integration between crates exists yet
4. **No external dependencies:** Cargo.lock contains only workspace members

## How to Navigate This Codebase

### For Autonomous Agents

1. **Start here:** AGENTS.md (this file's parent) - navigation guide
2. **Read next:** docs/engineering/CODEBASE-INDEX.md (this file) - complete repository inventory
3. **Reference boundaries:** project/boundaries.json - dependency rules and ownership
4. **Check tasks:** project/work-items.json - structured TODO list
5. **Verify changes:** python3 scripts/i2n.py validate - boundary and baseline verification
6. **Implementation readiness:** docs/engineering/IMPLEMENTATION-READINESS.md - feature matrix and blockers
7. **First task:** docs/engineering/IMPLEMENTATION-START.md - concrete starting point

### Dependency Lookup

To find allowed dependencies for a crate:
1. Look up the crate in project/boundaries.json
2. Check "allowed_dependency_groups" field
3. Reference the group definitions in the same file
4. Verify actual Cargo.toml dependencies match the allowlist

### Boundary Verification

To verify boundary compliance:
1. Run `python3 scripts/i2n.py inventory --check`
2. Check reports/boundary-inventory.md for violations
3. Review the "Dependency edges" section for forbidden edges
4. Ensure no core crate depends on platform implementations

### Task Tracking

To track implementation progress:
1. Edit project/work-items.json
2. Run `python3 scripts/i2n.py checklist --write` to update TODO.md
3. Mark tasks "done" only when acceptance criteria are met
4. Record evidence paths in the "evidence" field

## Protected Files

The following files are protected by the baseline and require explicit review before modification:

**Control files:**
- Cargo.toml
- Cargo.lock
- project/boundaries.json
- schemas/boundaries.schema.json
- scripts/i2n.py
- .github/workflows/ci.yml

**Protected documentation:**
- All docs/**/*.md files
- README.md
- WHITEPAPER.md
- BLUEPRINT.md
- TODO.md
- CHANGELOG.md
- CONTRIBUTING.md
- SECURITY.md

**Governance data:**
- project/project.json
- project/work-items.json
- project/baseline.json
- schemas/work-items.schema.json
- schemas/nir-v0.1.schema.json
- schemas/i2n-artifact-v1.schema.json

**Automation:**
- scripts/install_hooks.py
- tests/python/test_repo_automation.py

To refresh the baseline after structural changes: `python3 scripts/i2n.py baseline capture --write`

## Repository Automation

### Available Commands

```bash
python3 scripts/i2n.py status              # Show project status
python3 scripts/i2n.py inventory --check   # Check boundary compliance
python3 scripts/i2n.py checklist --write   # Generate TODO.md
python3 scripts/i2n.py baseline verify     # Verify baseline
python3 scripts/i2n.py validate            # Run all validations
python3 scripts/i2n.py all --write         # Regenerate all reports
```

### Validation Results

**Current status:** All validations pass
- Workspace packages: 34 present, 0 missing
- Repository components: 9 present, 0 missing
- Boundary violations: 0
- Task graph issues: 0
- Baseline control files: unchanged

## Build and Validation Status

### Cargo Commands

```bash
cargo build --workspace          # Build all packages
cargo test --workspace           # Run all tests
cargo clippy --workspace         # Lint all code
cargo fmt --all                  # Format all code
```

**Status:** Not yet validated (Rust toolchain installation pending per I2N-0101)

### CI Pipeline

**File:** .github/workflows/ci.yml

**Steps:**
1. Checkout repository
2. Run repository automation (python3 scripts/i2n.py validate)
3. Run cargo fmt --all -- --check
4. Run cargo clippy --workspace --all-targets -- -D warnings
5. Run cargo test --workspace

**Status:** CI workflow exists but Rust checks may not pass without toolchain verification

## Implementation Readiness Summary

### Ready to Implement

The following components have minimal prerequisites and can begin implementation:

1. **i2n-diagnostics** (I2N-0202): Structured error codes and redaction
2. **i2n-digest** (post I2N-0201): Digest verification primitives
3. **i2n-oci** (I2N-0301): OCI reference and descriptor parsing
4. **i2n-registry** (I2N-0302): OCI Distribution client
5. **i2n-fetcher** (I2N-0303): Bounded blob fetching

### Blocked

The following components require prerequisites:

1. **i2n-cache** (I2N-0401): Blocked by i2n-fetcher
2. **i2n-layer** (I2N-0501): Blocked by i2n-fetcher
3. **i2n-unpack** (I2N-0501): Blocked by i2n-fetcher
4. **i2n-rootfs** (I2N-0601): Blocked by i2n-layer
5. **i2n-inspector** (I2N-0701): Blocked by i2n-rootfs
6. **i2n-analyzer** (I2N-0801): Blocked by i2n-inspector
7. **i2n-compiler** (I2N-0901): Blocked by i2n-analyzer
8. **Platform backends** (I2N-0901+): Blocked by i2n-analyzer
9. **Artifact system** (I2N-1001+): Blocked by platform backends

### First Implementation Task

See docs/engineering/IMPLEMENTATION-START.md for the first concrete, implementation-ready task with exact source locations, prerequisites, test plan, and acceptance criteria.

---

**Index generation timestamp:** 2026-11-20  
**Git commit:** f42f10a  
**Index schema version:** 1.0  
**Next review:** After any structural changes to workspace or boundaries
