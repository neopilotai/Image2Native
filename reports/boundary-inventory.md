# Generated Boundary Inventory

- Workspace members: **34**
- Packages indexed: **34**
- Local dependency edges: **41**

| Package | Kind | Group | Owner | Path | Responsibility |
|---|---|---|---|---|---|
| `i2n-analyzer` | library | analysis | analysis | `crates/i2n-analyzer` | Owns compatibility, policy and target capability analysis. |
| `i2n-archive` | library | artifact | artifact | `crates/i2n-archive` | Owns deterministic artifact archive and extraction. |
| `i2n-artifact` | library | artifact | artifact | `crates/i2n-artifact` | Owns I2N bundle manifest, payload graph and reader/writer. |
| `i2n-cache` | library | content | content | `crates/i2n-cache` | Owns verified content-addressed cache storage and pruning. |
| `i2n-compiler` | library | compiler | compiler | `crates/i2n-compiler` | Owns compile graph orchestration, stage contracts and execution planning. |
| `i2n-config` | library | foundation | foundation | `crates/i2n-config` | Owns validated compiler and runtime configuration. |
| `i2n-diagnostics` | library | foundation | foundation | `crates/i2n-diagnostics` | Owns structured diagnostics, stage identifiers and safe error metadata. |
| `i2n-digest` | library | content | content | `crates/i2n-digest` | Owns content digest parsing and verification primitives. |
| `i2n-fetcher` | library | content | content | `crates/i2n-fetcher` | Owns bounded blob transfer, retries and cancellation. |
| `i2n-filesystem` | library | filesystem | filesystem | `crates/i2n-filesystem` | Owns filesystem abstractions and metadata normalization. |
| `i2n-inspector` | library | analysis | analysis | `crates/i2n-inspector` | Owns static image/process/dependency inspection. |
| `i2n-ir` | library | contracts | contracts | `crates/i2n-ir` | Owns the versioned Native Image Representation (NIR). |
| `i2n-layer` | library | filesystem | filesystem | `crates/i2n-layer` | Owns layer decoding and changeset/whiteout semantics. |
| `i2n-model` | library | domain | domain | `crates/i2n-model` | Owns stable IDs, platform types, digests, image references and shared domain values. |
| `i2n-network` | library | runtime | runtime | `crates/i2n-network` | Owns host/guest networking policy and port mapping. |
| `i2n-oci` | library | oci | oci | `crates/i2n-oci` | Owns OCI image/index/manifest/config models and parsing. |
| `i2n-platform` | library | platform-contract | platform-contract | `crates/i2n-platform` | Owns platform backend traits and capability contracts. |
| `i2n-platform-linux` | library | platform-linux | platform-linux | `crates/i2n-platform-linux` | Owns Linux native runtime adapter and Linux-specific integration. |
| `i2n-platform-macos` | library | platform-macos | platform-macos | `crates/i2n-platform-macos` | Owns Apple Virtualization.framework adapter and native bridge. |
| `i2n-platform-windows` | library | platform-windows | platform-windows | `crates/i2n-platform-windows` | Owns WSL2/HCS adapter and Windows native bridge. |
| `i2n-protocol` | library | foundation | foundation | `crates/i2n-protocol` | Owns versioned host/guest and daemon IPC message contracts. |
| `i2n-provenance` | library | trust | trust | `crates/i2n-provenance` | Owns source/build provenance and attestations. |
| `i2n-registry` | library | oci | oci | `crates/i2n-registry` | Owns OCI Distribution API, registry auth and manifest resolution. |
| `i2n-rootfs` | library | filesystem | filesystem | `crates/i2n-rootfs` | Owns logical root filesystem reconstruction. |
| `i2n-runtime` | library | runtime | runtime | `crates/i2n-runtime` | Owns application lifecycle semantics and runtime plans. |
| `i2n-sbom` | library | trust | trust | `crates/i2n-sbom` | Owns SPDX SBOM generation and validation. |
| `i2n-security` | library | security | security | `crates/i2n-security` | Owns policy evaluation and security boundary helpers. |
| `i2n-signing` | library | trust | trust | `crates/i2n-signing` | Owns artifact signature and verification adapters. |
| `i2n-storage` | library | runtime | runtime | `crates/i2n-storage` | Owns application state, volumes and writable overlays. |
| `i2n-supervisor` | library | runtime | runtime | `crates/i2n-supervisor` | Owns process/VM supervision, events and instance state. |
| `i2n-unpack` | library | filesystem | filesystem | `crates/i2n-unpack` | Owns safe archive and layer unpacking policies. |
| `image2native-cli` | application | app | application | `apps/image2native-cli` | Command-line interface and user-facing orchestration. |
| `image2native-daemon` | application | app | application | `apps/image2native-daemon` | Optional local service; never required by the core CLI. |
| `image2native-launcher` | application | app | application | `apps/image2native-launcher` | Native per-platform application launcher. |

## Non-Cargo repository components

- Components inventoried: **9**

| Component | Kind | Owner | Path | Responsibility |
|---|---|---|---|---|
| `contract-schemas` | schemas | contracts | `schemas` | Versioned JSON schemas for NIR, I2N artifacts and project governance records. |
| `documentation` | documentation | docs | `docs` | Product, architecture, platform, security and implementation documentation. |
| `linux-guest-runtime` | guest-runtime | guest-runtime | `guest` | Pinned Linux kernel, minimal init, guest agent and host-guest protocol implementation. |
| `platform-linux-bridge` | native-bridge | platform-linux | `platform/linux` | Linux host syscalls and OCI runtime integration; must remain behind the platform backend contract. |
| `platform-macos-bridge` | native-bridge | platform-macos | `platform/macos` | Apple Virtualization.framework bridge and entitlement-sensitive code. |
| `platform-windows-bridge` | native-bridge | platform-windows | `platform/windows` | Windows WSL2, Win32 and HCS bridge code. |
| `project-automation` | automation | foundation | `scripts` | Deterministic repository checks, TODO rendering, inventory and baseline enforcement. |
| `project-governance` | governance-data | foundation | `project` | Machine-readable tasks, ownership boundaries, decisions and baseline source of truth. |
| `quality-harness` | test-harness | quality | `tests` | Unit, integration, compatibility, security, golden and fixture test suites. |

## Dependency edges

- `i2n-ir` → `i2n-model` (dependencies)
- `i2n-ir` → `i2n-diagnostics` (dependencies)
- `i2n-analyzer` → `i2n-model` (dependencies)
- `i2n-analyzer` → `i2n-diagnostics` (dependencies)
- `i2n-analyzer` → `i2n-ir` (dependencies)
- `i2n-compiler` → `i2n-model` (dependencies)
- `i2n-compiler` → `i2n-diagnostics` (dependencies)
- `i2n-compiler` → `i2n-oci` (dependencies)
- `i2n-compiler` → `i2n-layer` (dependencies)
- `i2n-compiler` → `i2n-rootfs` (dependencies)
- `i2n-compiler` → `i2n-inspector` (dependencies)
- `i2n-compiler` → `i2n-ir` (dependencies)
- `i2n-compiler` → `i2n-analyzer` (dependencies)
- `i2n-compiler` → `i2n-artifact` (dependencies)
- `i2n-artifact` → `i2n-model` (dependencies)
- `i2n-artifact` → `i2n-diagnostics` (dependencies)
- `i2n-artifact` → `i2n-ir` (dependencies)
- `i2n-artifact` → `i2n-digest` (dependencies)
- `i2n-runtime` → `i2n-model` (dependencies)
- `i2n-runtime` → `i2n-diagnostics` (dependencies)
- `i2n-runtime` → `i2n-platform` (dependencies)
- `i2n-runtime` → `i2n-artifact` (dependencies)
- `i2n-supervisor` → `i2n-model` (dependencies)
- `i2n-supervisor` → `i2n-diagnostics` (dependencies)
- `i2n-supervisor` → `i2n-runtime` (dependencies)
- `i2n-security` → `i2n-model` (dependencies)
- `i2n-security` → `i2n-diagnostics` (dependencies)
- `i2n-security` → `i2n-signing` (dependencies)
- `i2n-security` → `i2n-sbom` (dependencies)
- `i2n-security` → `i2n-provenance` (dependencies)
- `i2n-platform-linux` → `i2n-model` (dependencies)
- `i2n-platform-linux` → `i2n-diagnostics` (dependencies)
- `i2n-platform-linux` → `i2n-platform` (dependencies)
- `i2n-platform-macos` → `i2n-model` (dependencies)
- `i2n-platform-macos` → `i2n-diagnostics` (dependencies)
- `i2n-platform-macos` → `i2n-platform` (dependencies)
- `i2n-platform-windows` → `i2n-model` (dependencies)
- `i2n-platform-windows` → `i2n-diagnostics` (dependencies)
- `i2n-platform-windows` → `i2n-platform` (dependencies)
- `image2native-cli` → `i2n-model` (dependencies)
- `image2native-cli` → `i2n-diagnostics` (dependencies)

## Violations

No boundary violations detected.

> Generated by `python3 scripts/i2n.py inventory --write`. Source: `project/boundaries.json` and Cargo manifests.
