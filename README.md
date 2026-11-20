# Image2Native

**An OCI image-to-application compiler and packaging system for macOS, Linux, and Windows.**

> Turn container images into verified, distributable application bundles with native host launchers and explicit execution backends.

**Status:** proposed architecture and documentation baseline. The software, CLI, IR and artifact format described here are not yet implemented. Examples are design targets, not claims of working functionality.

## Product definition

Image2Native resolves OCI images, verifies their content, reconstructs their layered filesystem and process metadata, lowers the result into a canonical Native Image Representation (NIR), analyzes host compatibility, then packages the workload with an appropriate platform launcher and execution backend.

## Important technical distinction

Image2Native is not a universal Linux-to-Mach-O/PE binary translator. A standard Linux container image contains Linux executables and expects Linux kernel behavior. General execution of Linux images on macOS and Windows therefore requires a Linux guest environment (proposed: Apple's Virtualization framework on macOS and WSL2 on Windows). The host-native `.app` or `.exe` is a launcher and lifecycle manager; the original Linux workload remains a Linux process in the guest.

The project has two separate modes:

1. **Image packaging:** accepts an existing OCI/Docker image and packages its application filesystem and configuration for a compatible backend.
2. **Source compilation:** accepts source/build inputs and invokes target toolchains to produce actual target-native binaries where source code and dependencies support that target. This is not generic binary translation.

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
- [Linux](docs/platforms/LINUX.md) · [macOS](docs/platforms/MACOS.md) · [Windows](docs/platforms/WINDOWS.md)
- [Security Model](docs/security/SECURITY_MODEL.md) · [Threat Model](docs/security/THREAT_MODEL.md)
- [CLI](docs/developer/CLI_SPEC.md) · [Repository Layout](docs/developer/REPOSITORY_LAYOUT.md) · [Build and Test](docs/developer/BUILD_AND_TEST.md)
- [Release Engineering](docs/operations/RELEASE.md) · [Roadmap](docs/roadmap/ROADMAP.md)
- [ADRs](docs/adr/) · [References](docs/references.md) · [Glossary](docs/glossary.md)

## Proposed repository layout

```text
image2native/
├── Cargo.toml / Cargo.lock / rust-toolchain.toml
├── README.md / WHITEPAPER.md / BLUEPRINT.md
├── apps/
│   ├── image2native-cli/
│   ├── image2native-launcher/
│   └── image2native-daemon/          # optional; never required for core CLI
├── crates/
│   ├── i2n-model/                    # shared domain types
│   ├── i2n-oci/                      # OCI image/index/config parsing
│   ├── i2n-registry/                 # OCI Distribution client
│   ├── i2n-fetcher/                  # blob transfer and retries
│   ├── i2n-digest/                   # digest parsing and verification
│   ├── i2n-cache/                    # content-addressed cache
│   ├── i2n-layer/                    # layer decode/application
│   ├── i2n-rootfs/                   # logical filesystem model
│   ├── i2n-inspector/                # static image inspection
│   ├── i2n-ir/                       # NIR schema and validation
│   ├── i2n-analyzer/                 # compatibility and policy analysis
│   ├── i2n-compiler/                 # pipeline orchestration
│   ├── i2n-artifact/                 # I2N bundle reader/writer
│   ├── i2n-sbom/ / i2n-signing/ / i2n-provenance/
│   ├── i2n-runtime/ / i2n-supervisor/
│   ├── i2n-platform/                 # backend contracts
│   ├── i2n-platform-linux/
│   ├── i2n-platform-macos/
│   ├── i2n-platform-windows/
│   ├── i2n-security/ / i2n-diagnostics/
│   └── i2n-network/ / i2n-storage/
├── platform/{linux,macos,windows}/   # thin native bridges
├── guest/{agent,init,kernel,rootfs}/
├── schemas/ tests/ docs/ scripts/
```

## First implementation target

Deliver a complete Linux vertical slice before building desktop virtualization backends: OCI resolve → verify → layer reconstruction → NIR → compatibility report → Linux runtime bundle → I2N artifact → launch. This validates the compiler core before adding host-specific VM integrations.

## Scope boundaries

**In scope:** OCI ingestion; multi-architecture selection; rootfs reconstruction; compatibility analysis; native launchers; Linux execution; macOS and Windows Linux-guest execution; integrity/signing/SBOM; updates; optional source compilation.

**Not in the first release:** generic binary translation; kernel emulation; guaranteed support for all images; Docker Desktop parity; automatic privileged execution; full Compose support; GUI-first product; Kubernetes orchestration.
