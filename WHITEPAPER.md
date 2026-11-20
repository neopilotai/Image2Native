# Image2Native White Paper

**Version:** 0.1 · **Date:** 20 November 2026 · **Status:** proposed architecture

## Abstract

Container images are reliable units for building and distributing application filesystems and process metadata, but they are not automatically desktop applications or standalone native executables. Runtime behavior depends on a compatible operating-system kernel, ABI, filesystem, process model, networking, resource controls and lifecycle manager.

Image2Native proposes a Rust-first compiler and packaging system that transforms OCI images into verified, target-specific application bundles. It resolves and verifies image content, reconstructs layered filesystems, extracts runtime metadata, lowers the result into a canonical Native Image Representation (NIR), analyzes backend compatibility, and links the application payload with a native host launcher, runtime requirements, provenance, SBOM and signatures.

The design distinguishes native packaging from native machine-code compilation. A macOS `.app` or Windows `.exe` can be a native launcher while a Linux workload continues to run in a Linux guest. A separate source-to-native path can produce real ELF, Mach-O or PE executables only where source and dependencies support the target. This distinction is fundamental to credible compatibility guarantees.

## 1. Problem and opportunity

Developers routinely have OCI images that they want to distribute as applications. Their users may not want to install or operate a container engine. Vendors also need a verifiable chain from source image digest to installed application, with predictable upgrades, application state, logs and platform support. Existing container tools primarily build, run and manage containers; Image2Native focuses on the transformation and packaging boundary between an OCI image and an installable application.

The product should make this workflow predictable without hiding that Linux, macOS and Windows expose different kernel and application binary interfaces.

## 2. Product thesis

**An OCI image should be compilable into a verified application artifact whose execution strategy is explicit, inspectable and appropriate to the target host.**

The compiler preserves image intent, reports unsupported requirements before packaging, and never silently changes isolation or privilege. The artifact records immutable source identity, canonical IR, execution plan, backend identity, payload digests and trust metadata.

## 3. Two distinct compilation modes

### 3.1 Image packaging

For an existing image:

- Linux host: use the host Linux kernel and an OCI-compatible runtime, within supported kernel and security-policy constraints.
- macOS host: package a native launcher and manage a Linux guest using Apple's Virtualization framework.
- Windows host: package a native launcher and use WSL2 for Linux workloads. A separate future backend handles Windows-native container images.

The launcher is native to the host. The image's Linux executable is still a Linux binary.

### 3.2 Source-to-native compilation

When source code and supported toolchains are available, invoke the appropriate compiler for a target triple. Rust, Go and C/C++ are reasonable initial integrations. Python and Node.js bundling is generally runtime packaging unless a specific AOT pipeline is implemented. Do not promise translation of arbitrary proprietary binaries.

## 4. System design

The pipeline has seven major stages:

1. **Resolve:** parse references, authenticate to registries, resolve image indexes and select a platform manifest.
2. **Acquire:** fetch blobs by digest, verify size and digest, and populate a content-addressed cache.
3. **Reconstruct:** decode and apply ordered layers, including OCI whiteout and metadata semantics.
4. **Lower:** convert image configuration and rootfs identity into versioned NIR.
5. **Analyze:** inspect OS, architecture, ABI evidence, entrypoint, mounts, devices, kernel requirements and security policy.
6. **Backend and link:** select an explicit execution plan and package payload, launcher, runtime references and trust metadata.
7. **Verify and execute:** verify artifact integrity/signature, install, launch, supervise, update, roll back and uninstall.

## 5. Native Image Representation

NIR is the host-independent boundary between image ingestion and platform backends. It captures immutable source identity, platform, rootfs, file metadata, process arguments, environment policy, user, working directory, ports, mounts, devices, capabilities, resource requirements and provenance. Compiler findings are kept separate from source facts so the same NIR can be re-analyzed as backend capabilities evolve.

NIR is a project-owned IR, not a replacement for OCI standards.

## 6. Execution by platform

### Linux

Integrate an established OCI runtime rather than writing a new container isolation runtime. The backend translates NIR into an OCI runtime bundle and applies namespaces, cgroups, capability restrictions, read-only rootfs, explicit mounts and seccomp/LSM policy where supported. Rootless execution is the preferred path. Seccomp is syscall filtering, not a complete sandbox by itself.

### macOS

Use Apple's Virtualization framework to create and manage a minimal Linux VM. The guest contains a pinned Linux kernel, init, guest agent and supporting utilities. Virtio devices provide controlled storage/network/host-guest communication. The `.app` manages guest lifecycle, application process, logs and ports. Entitlements, signing, hardened runtime and distribution constraints must be validated for the intended distribution channel.

### Windows

Use WSL2 as the initial Linux guest backend. A native Windows launcher verifies the artifact and controls a product-managed guest. Windows-native images require a different execution model; a future HCS backend must implement Windows container semantics rather than sending Windows images into a Linux guest.

## 7. I2N bundle

I2N is a versioned, target-specific artifact format proposed by the project. It includes an application manifest, source digest, NIR, execution plan, payload graph, target/backend metadata, pinned runtime/guest references, SBOM, provenance and signature material. Mutable user data and runtime secrets remain outside the immutable artifact.

The first format should support a directory bundle; native installers and self-extracting variants can be wrappers over the same verified payload graph. Canonicalization and signing rules must be finalized before declaring I2N 1.0.

## 8. Security model

Treat every image, config, layer and application binary as untrusted. Validate media types, sizes and digests; bound network and decompression resources; use a logical rootfs model; prevent archive path and link escapes; keep credentials out of logs and artifacts; and verify signatures according to an explicit trust policy.

At runtime, use least privilege. On Linux prefer rootless execution, separate namespaces, resource limits, reduced capabilities and restrictive syscall filtering. On macOS and Windows, the Linux guest is the isolation boundary, but host/guest shared files, ports and agent channels still require strict policy. Sign artifacts and runtime components, produce provenance and an SBOM, and verify updates before activation.

A valid digest proves byte identity, not that the image is safe. A signature proves a trusted identity signed a specific object under a policy; it does not prove the software is benign.

## 9. Performance strategy

Prioritize content-addressed reuse, concurrent but bounded downloads, streaming decompression, correct parallelism across independent work, immutable compressed payloads, writable copy-on-write state, chunk-level updates and minimal guest boot. Benchmark cold and warm cache separately and publish test environments. Avoid unsupported speed claims.

## 10. Differentiation

Image2Native is not another container daemon. Its distinct value is a unified compiler pipeline, NIR, compatibility analysis, native launchers, explicit backend selection, signed application artifact, lifecycle/update model and optional source compiler.

## 11. Limits and non-goals

Not every OCI image is portable. Some images need privileged mode, kernel modules, host devices, particular kernel features, unusual mount propagation, host networking or unsupported architectures. These must be diagnosed or rejected. The first release does not promise generic binary translation, arbitrary kernel emulation, Docker Desktop feature parity, or unrestricted host integration.

## 12. Success criteria

The project is successful when it can resolve and verify a pinned image without Docker Engine; reconstruct the rootfs correctly; preserve process intent in NIR; report compatibility blockers; produce a deterministic I2N package; install and run it on a validated backend; support signed updates/rollback; and demonstrate the Linux, macOS and Windows paths with real platform tests.

## Conclusion

Image2Native should be built as a cross-platform application packaging compiler, not a universal binary translator. A standards-based OCI ingestion pipeline, canonical IR and explicit platform backends provide one developer workflow while respecting the real differences between operating systems.
