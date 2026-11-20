# macOS Backend

## 1. Role

The macOS backend packages a native macOS launcher and manages a minimal Linux guest for Linux OCI workloads. The guest supplies the Linux kernel ABI; the source image's application binaries remain Linux binaries.

## 2. Host integration

Use Apple's Virtualization framework behind a small native bridge. Rust owns compiler orchestration, bundle metadata, policy and lifecycle state. Swift or Objective-C may be used for framework APIs where it provides the most reliable integration. Keep native handles and callback lifetimes private to the platform crate.

Account for the virtualization entitlement, code signing, hardened runtime and distribution/notarization rules appropriate to the chosen distribution channel. A development build is not proof that the production-signed application can be distributed.

## 3. Guest contents

- Pinned Linux kernel and configuration.
- Minimal init and required guest userspace.
- Image2Native guest agent.
- Required filesystem/network support.
- Immutable application payload attachment.
- Separately managed writable application state.

Guest images should be reproducible, signed and updated independently from application payloads only when the compatibility contract permits it. Guest kernel and agent are part of the trust chain.

## 4. Boot and control sequence

1. Verify the application artifact and guest component signatures.
2. Validate host prerequisites and entitlement.
3. Allocate CPU, memory and storage within policy.
4. Configure Virtio storage, networking, serial diagnostics and narrow host/guest channels.
5. Boot guest and authenticate the guest agent.
6. Attach/mount immutable payload.
7. Apply runtime policy and start workload.
8. Stream logs and health state over a versioned channel.
9. Stop workload and guest according to lifecycle policy.

## 5. Filesystem integration

Do not share the whole host home directory by default. Use explicit grants and a narrow guest mount broker. Keep Linux rootfs semantics inside the guest. The guest mounts the Linux filesystem; macOS should not need to represent Linux owners, device nodes or special file types directly.

## 6. Networking

Use a controlled virtual NIC and explicit host port forwarding. Do not bind image ports to all host interfaces automatically. Prefer loopback-only exposure where possible and require explicit policy/consent for LAN access.

## 7. Architecture

Native ARM64 guest execution is the primary Apple Silicon path; x86_64 guest on Intel is a separate target. Running x86_64 images on Apple Silicon requires a separately designed and benchmarked emulation mode and must be declared as such. Never assume cross-architecture compatibility.

## 8. Packaging

A `.app` may contain launcher, resources, manifest and references to verified guest/runtime components. DMG or PKG can wrap the app. Downloaded runtime components must be digest-pinned and signature-verified. Application and guest updates are separate operations.

## 9. Resource management

Expose CPU and memory budgets, recover from sleep/reboot, and ensure crashes do not leak VM resources. Do not keep a guest running when no workload needs it unless the user enables service mode.

## 10. Acceptance tests

- Entitlement and prerequisite failures are actionable.
- Guest boots on named Intel and Apple Silicon hosts.
- Guest-agent handshake authenticates peer and version.
- Immutable payload and writable state are separated.
- Port forwarding follows loopback/LAN policy.
- Start/stop/restart works after sleep and host reboot.
- Signed `.app` distribution flow is validated.
- Guest update and rollback are verified.
