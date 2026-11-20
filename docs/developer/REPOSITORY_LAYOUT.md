# Repository Layout and Module Boundaries

## 1. Workspace policy

Use a Cargo workspace with one toolchain policy and centralized dependency versions where practical. Keep crate APIs small; default to `pub(crate)`. Do not create an oversized `common` crate that becomes an unowned dependency sink.

## 2. Ownership

**Domain/contracts:** `i2n-model` owns IDs, digests, platform types, structured diagnostics and shared errors. It remains light and has no registry, runtime or OS SDK dependency.

**OCI/content:** `i2n-oci` owns image-spec models/parsing; `i2n-registry` owns Distribution protocol; `i2n-fetcher` owns bounded transfer; `i2n-digest` owns digest operations; `i2n-cache` owns verified content-addressed storage.

**Filesystem/compiler:** `i2n-layer` owns layer decoding and changeset semantics; `i2n-rootfs` owns logical filesystem; `i2n-inspector` owns static inspection; `i2n-ir` owns NIR; `i2n-analyzer` owns compatibility; `i2n-compiler` orchestrates the graph.

**Artifact/trust:** `i2n-artifact` owns I2N manifest and payload graph; `i2n-sbom` handles SBOM; `i2n-provenance` handles build records; `i2n-signing` adapts signing/verification.

**Runtime/platform:** `i2n-platform` owns shared traits/capabilities. Platform crates own native API bridges. `i2n-runtime` owns lifecycle semantics; `i2n-supervisor` owns instance state/events. Native handles never leak into domain types.

## 3. Dependency rules

- Domain crates do not depend on app crates.
- Core compiler crates do not depend on platform SDKs.
- Platform crates may depend on shared traits/model/runtime and their private bridge.
- CLI depends on public service interfaces, not backend internals.
- Guest-agent protocol is versioned and independently testable.
- Docker CLI shell-out is never the only ingestion route.

Enforce boundaries with architecture tests or dependency graph checks.

## 4. Error model

Use structured errors with stable code, stage, retryability, source chain, safe user-facing message and remediation. Do not include secret headers, environment values or private host paths in errors. Preserve causes in redacted debug logs.

## 5. Feature flags

Use feature flags only when they materially affect build/distribution. Never let flags silently change security behavior. A backend not compiled into a binary must be reported unavailable, not selected dynamically.

## 6. Native bridge strategy

Keep Swift/Objective-C and Win32/HCS/WSL bridge code in `platform/macos` and `platform/windows`. Use a narrow C ABI or generated bindings where appropriate. Document ownership, callback, threading and cancellation rules. Convert native errors into structured Rust errors.

## 7. Naming

- Crates: `i2n-*`.
- CLI: `image2native`.
- App IDs: reverse-domain style where publisher identity exists.
- Backend IDs: `linux-oci`, `apple-virtualization`, `windows-wsl2`, `windows-hcs`.
- Schemas: kebab-case and explicit major version where necessary.
