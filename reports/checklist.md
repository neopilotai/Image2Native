# Checklist Report

- Total: **26**
- Done: **4**
- In progress: **1**
- Blocked: **0**
- Open: **21**

| ID | Phase | Priority | Status | Owner | Boundary | Task |
|---|---:|---|---|---|---|---|
| I2N-0001 | 0 | P0 | done | docs | `documentation` | Import and index product documentation |
| I2N-0002 | 1 | P0 | done | foundation | `workspace` | Create Rust workspace and crate scaffold |
| I2N-0003 | 1 | P0 | done | foundation | `project-automation` | Implement automated TODO, boundary and baseline control |
| I2N-0004 | 1 | P0 | done | foundation | `ci` | Add cross-platform CI and contributor workflow |
| I2N-0101 | 1 | P0 | todo | foundation | `workspace` | Install and verify supported Rust toolchain in maintainer environments |
| I2N-0201 | 2 | P0 | in_progress | domain | `i2n-model` | Finalize domain IDs, digest and target platform model |
| I2N-0202 | 2 | P1 | todo | foundation | `i2n-diagnostics` | Define structured diagnostic codes and error policy |
| I2N-0301 | 3 | P0 | todo | oci | `i2n-oci` | Implement OCI image reference and descriptor parsing |
| I2N-0302 | 3 | P0 | todo | registry | `i2n-registry` | Implement OCI Distribution registry client |
| I2N-0303 | 3 | P0 | todo | content | `i2n-fetcher` | Implement bounded blob fetching and digest verification |
| I2N-0401 | 4 | P1 | todo | content | `i2n-cache` | Build atomic content-addressed layer cache |
| I2N-0501 | 5 | P0 | todo | filesystem | `i2n-layer/i2n-unpack` | Implement safe OCI layer decode and extraction |
| I2N-0601 | 6 | P0 | todo | filesystem | `i2n-rootfs` | Reconstruct logical RootFS with OCI layer semantics |
| I2N-0701 | 7 | P0 | todo | contracts | `i2n-inspector/i2n-ir` | Implement image config inspector and NIR v0.1 |
| I2N-0801 | 8 | P0 | todo | analysis | `i2n-analyzer` | Build compatibility analyzer and explicit backend planner |
| I2N-0901 | 9 | P0 | todo | linux | `i2n-platform-linux` | Integrate Linux OCI runtime backend |
| I2N-1001 | 10 | P0 | todo | artifact | `i2n-artifact/i2n-platform-linux` | Implement I2N artifact format and Linux launcher |
| I2N-1101 | 11 | P1 | todo | trust | `i2n-sbom/i2n-signing/i2n-provenance` | Add SBOM, provenance and artifact signing |
| I2N-1201 | 12 | P0 | todo | linux | `runtime/security` | Harden Linux install, update, rollback and runtime security |
| I2N-1301 | 13 | P1 | todo | guest | `guest/agent` | Build minimal Linux guest and authenticated guest agent |
| I2N-1401 | 14 | P1 | todo | macos | `i2n-platform-macos` | Implement macOS Virtualization backend and app packaging |
| I2N-1501 | 15 | P1 | todo | windows | `i2n-platform-windows` | Implement Windows WSL2 backend and launcher |
| I2N-1701 | 17 | P2 | todo | windows | `i2n-platform-windows` | Add Windows-native OCI image backend through HCS |
| I2N-1801 | 18 | P2 | todo | toolchains | `source-toolchains` | Add source-to-native compilation mode |
| I2N-1901 | 19 | P2 | todo | compiler | `i2n-compiler/i2n-runtime` | Add supported Docker Compose application groups |
| I2N-2001 | 20 | P1 | todo | release | `release-engineering` | Prepare 1.0 support matrix, release and operations readiness |
