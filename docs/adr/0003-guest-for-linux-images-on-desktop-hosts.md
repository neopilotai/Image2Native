# ADR 0003: Use a Linux Guest for General Linux Images on macOS and Windows

- **Status:** Accepted as proposed baseline
- **Date:** 2026-11-20

## Context

Linux images commonly contain ELF binaries and Linux userspace assumptions. macOS and Windows do not provide a general Linux kernel ABI. Translating arbitrary Linux binaries to host machine code is not a credible general-purpose product promise.

## Decision

The macOS backend uses Apple's Virtualization framework to manage a Linux guest. The initial Windows Linux-image backend uses WSL2. A native launcher manages the guest and workload but does not claim the workload itself is a native Mach-O or PE application. Cross-architecture execution requires an explicit, separately tested emulation backend.

## Consequences

- Guest kernel, init and agent are part of the trusted computing base.
- VM boot, storage, networking and host/guest channels require backend-specific work.
- Artifact manifests pin guest/backend versions.
- Support matrix distinguishes source OS from host OS.

## Alternatives

Generic binary translation was rejected as an unsupported promise. Requiring Docker Desktop was rejected because self-contained packaged runtime is a product goal. Converting every image to WASM was rejected because support is limited and may still involve emulation/translation.
