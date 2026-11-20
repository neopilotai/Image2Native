# References and Standards

**Reference check date:** 20 November 2026. Links point to upstream specifications or vendor documentation. Implementation must pin exact specification/tool versions rather than depend implicitly on moving `main`/`latest` branches.

## OCI standards

1. [OCI Image Specification](https://github.com/opencontainers/image-spec) — manifests, indexes, descriptors, image config, layers and image layouts.
2. [OCI Manifest](https://github.com/opencontainers/image-spec/blob/main/manifest.md) — content-addressable manifest and platform-specific image data.
3. [OCI Image Index](https://github.com/opencontainers/image-spec/blob/main/image-index.md) — platform-indexed manifests.
4. [OCI Image Layer](https://github.com/opencontainers/image-spec/blob/main/layer.md) — changesets and whiteout behavior.
5. [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec) — registry distribution API.
6. [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec) — runtime configuration and lifecycle contract.
7. [OCI Runtime Configuration](https://github.com/opencontainers/runtime-spec/blob/main/config.md) — process, rootfs and mounts.
8. [OCI Linux Runtime Configuration](https://github.com/opencontainers/runtime-spec/blob/main/config-linux.md) — namespaces, cgroups, capabilities and Linux-specific settings.

## Platform virtualization

9. [Apple Virtualization framework](https://developer.apple.com/documentation/virtualization) — manage Linux/macOS VMs on Apple Silicon and Intel Macs; Virtio devices and virtualization entitlement.
10. [Apple: Creating and Running a Linux Virtual Machine](https://developer.apple.com/documentation/virtualization/creating-and-running-a-linux-virtual-machine) — Linux guest setup.
11. [Microsoft: What is WSL](https://learn.microsoft.com/en-us/windows/wsl/about) — WSL2 Linux kernel in a lightweight utility VM.
12. [Microsoft: Comparing WSL versions](https://learn.microsoft.com/en-us/windows/wsl/wsl2-about) — WSL2 architecture.
13. [Microsoft Host Compute System](https://learn.microsoft.com/en-us/virtualization/api/hcs/overview) — lifecycle APIs for VMs and containers.

## Linux runtime and isolation

14. [Linux cgroup v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) — process grouping and resource controllers.
15. [Linux seccomp filter](https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html) — syscall filtering and its scope/limitations.
16. [SquashFS documentation](https://github.com/torvalds/linux/blob/master/Documentation/filesystems/squashfs.rst) — compressed read-only Linux filesystem.
17. [Firecracker getting started](https://github.com/firecracker-microvm/firecracker/blob/main/docs/getting-started.md) — KVM requirements; relevant only to an optional Linux microVM backend.

## Supply chain and build targets

18. [Sigstore Cosign: Signing containers](https://docs.sigstore.dev/cosign/signing/signing_with_containers/) — signing and attestation workflows.
19. [Sigstore Quickstart](https://docs.sigstore.dev/quickstart/quickstart-cosign/) — signing and verification examples.
20. [Rust platform support](https://doc.rust-lang.org/rustc/platform-support.html) — target triples and support tiers.
21. [SPDX](https://spdx.dev/) — software bill of materials specification and ecosystem.

## Notes

- Pin exact spec releases/commits and OS builds at implementation time.
- I2N and NIR are project-owned proposals; the references above do not define them.
- Cryptographic signing establishes signer identity over content under a trust policy; it does not prove the software is benign.
