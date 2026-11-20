# Security Model

## 1. Objectives

1. Protect the host from malicious image metadata and layer content.
2. Prevent credentials and secrets leaking into logs or artifacts.
3. Verify immutable objects before use.
4. Run workloads with least privilege.
5. Make isolation boundaries and host integrations visible.
6. Authenticate updates and prevent unsafe downgrade.
7. Preserve an auditable source-image-to-installed-app chain.

## 2. Trust domains

- **Untrusted source:** registry metadata, image config, layers, labels, entrypoint and application binaries.
- **Compiler host:** parsers, decompressor, cache, staging filesystem, CLI and launcher.
- **Build output:** NIR, execution plan, I2N manifest, payload and SBOM.
- **Runtime host:** kernel, container runtime, VM framework, WSL2/HCS, guest kernel and guest agent.
- **Workload:** application code/data, still untrusted after packaging.
- **Trust infrastructure:** signers, trust roots, attestations and update metadata.

Each boundary needs explicit validation and policy.

## 3. Input security

- Require TLS for registry traffic.
- Use credential helpers or OS secret storage; do not write raw credentials into project config by default.
- Redact tokens/auth headers from traces and errors.
- Validate media types, sizes, descriptor digests and object counts.
- Bound response sizes, JSON depth, concurrency and total resource use.
- Reject unsupported compression/archive formats rather than guessing.

## 4. Archive and filesystem security

Use safe extraction into a logical rootfs. Normalize rooted paths, reject traversal, define symlink/hardlink handling, prevent link escapes, implement whiteouts, cap expanded size and file count, avoid host device-node creation and stage changes atomically. Preserve logical metadata even where host materialization is not possible. Fuzz parsers and extractors.

## 5. Runtime security

### Linux
- Rootless by default where supported.
- Separate namespaces and use cgroups for resources.
- Drop capabilities; add only policy-approved minimums.
- Apply seccomp and available LSM policy.
- Read-only rootfs with explicit writable state.
- Restrict host mounts, devices and networking.
- Avoid privileged mode and host namespace sharing by default.

Seccomp filters system calls and reduces exposed kernel surface; it is not a complete sandbox by itself. Runtime and host kernel remain part of the trusted computing base.

### macOS and Windows
Run Linux workloads in a Linux guest. Treat host/guest file sharing, port forwarding, guest-agent channels and runtime downloads as privileged interfaces. Authenticate and version the guest-agent protocol, minimize guest services and pin guest kernel versions.

## 6. Secrets

Image environment variables may accidentally contain secrets. Offer detection warnings and redaction policy but do not claim complete detection. Runtime secrets enter through explicit secret references or OS secret stores. Never bake them into NIR, manifests, SBOMs, logs or immutable artifacts.

## 7. Signing and provenance

- Always verify content digests.
- Verify source signatures when policy requires them.
- Sign I2N output in release workflows.
- Generate provenance binding input digest, compiler version, target, build options and builder identity.
- Generate/import SBOM with explicit scope and coverage limitations.
- Verify guest kernel, agent and runtime components independently.
- Support trust-root rotation and revocation.

A signature authenticates a signer under a trust policy; it does not prove an application is benign. A digest proves byte identity, not publisher trust.

## 8. Update security

Updates are digest-pinned and signed. Stage and verify a complete new artifact before switching active versions. Preserve a last-known-good version. Enforce minimum security versions. Application rollback must not undo trust revocations or security policy.

## 9. Privacy

No mandatory telemetry in the core compiler. Any opt-in telemetry must disclose fields, retention and destination, exclude secrets and private environment data, and be disableable. Do not embed host usernames, home paths or machine identifiers in artifacts unless explicitly requested and reviewed.

## 10. Stable release gates

Archive fuzzing, static analysis, dependency audit, signature verification, artifact tamper tests, privilege-boundary review, platform integration review and a vulnerability reporting process are required before 1.0.
