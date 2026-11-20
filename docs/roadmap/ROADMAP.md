# Product and Engineering Roadmap

**Planning baseline:** 20 November 2026. No calendar estimates are assigned; phases close on acceptance evidence.

## Release milestones

- **0.1:** compiler foundation and Linux prototype.
- **0.2:** Linux application artifact and lifecycle.
- **0.3:** macOS Linux-guest packaging.
- **0.4:** Windows WSL2 Linux-guest packaging.
- **0.5:** production trust, installer, update and rollback hardening.
- **1.0:** stable support for the explicitly tested platform matrix.
- **1.x:** Windows-native images, source compilation and ecosystem expansion.

## Phase plan

### Phase 0 — Product and contract freeze
Repository map, product requirements, threat model, NIR/I2N drafts and ADR process. **Exit:** architecture reviewed; unsupported behavior documented.

### Phase 1 — Rust workspace and CI
Workspace, toolchain pin, errors, tracing, lint, fixture harness and CI. **Exit:** clean build and tests on supported development hosts.

### Phase 2 — OCI domain model
Reference parser, descriptors, manifest, index and config validation. **Exit:** golden and invalid fixtures pass.

### Phase 3 — Registry ingestion
OCI Distribution client, auth provider, OCI layout/archive import, blob streaming and digest verification. **Exit:** pull pinned image without Docker Engine.

### Phase 4 — Content-addressed cache
Atomic blob store, metadata index, concurrency control, verify/prune and offline mode. **Exit:** partial downloads cannot be treated as verified objects.

### Phase 5 — Layer decode and safe extraction
Compression codecs, path/link policy, quotas, fuzz harness. **Exit:** adversarial archive fixtures pass.

### Phase 6 — RootFS reconstruction
Layer ordering, whiteouts, ownership, permissions and rootfs identity. **Exit:** golden filesystem fixtures match OCI semantics.

### Phase 7 — Image config and NIR 0.1
Normalize process config and emit canonical NIR. **Exit:** golden schema fixtures pass; unknown required features rejected; secrets excluded by policy.

### Phase 8 — Compatibility analyzer
Inspect binary format, architecture, ABI evidence, kernel/runtime needs and policy. **Exit:** unknown findings are never silently marked compatible.

### Phase 9 — Linux runtime adapter
Generate OCI runtime bundle; integrate mature runtime; rootless preflight, start/stop/log/status. **Exit:** supported images run without Docker Engine under documented security profile.

### Phase 10 — I2N artifact and Linux launcher
Manifest, payload graph, bundle reader/writer, install/run/uninstall. **Exit:** copied artifact runs on clean supported Linux host.

### Phase 11 — SBOM, provenance and signatures
SPDX output/import, provenance and signing/verification integration. **Exit:** tampered or untrusted artifacts fail configured policy.

### Phase 12 — Linux 0.2 hardening
Updates, rollback, state retention, benchmarks, fuzzing and support matrix. **Exit:** Linux lifecycle and security gates pass.

### Phase 13 — Guest build pipeline
Pinned minimal Linux kernel/userspace, init and guest agent; reproducible guest image build. **Exit:** signed guest and authenticated agent protocol.

### Phase 14 — macOS Virtualization backend
Native bridge, VM lifecycle, Virtio devices, guest-agent control and `.app` package. **Exit:** real supported Intel/Apple Silicon hosts run a Linux OCI fixture; signing/entitlement constraints are validated.

### Phase 15 — Windows WSL2 backend
Windows launcher, managed guest provisioning, guest agent, networking and installer. **Exit:** supported Windows builds run and manage Linux image fixture.

### Phase 16 — Update trust hardening
Separate app and guest updates, delta chunks, trust rotation and rollback controls. **Exit:** interrupted/tampered update cannot replace last-good version.

### Phase 17 — Windows-native images
HCS adapter and Windows image semantics. **Exit:** independent conformance and E2E suite passes on named Windows hosts.

### Phase 18 — Source-to-native compiler
Source/build context and Rust/Go/C/C++ toolchains. **Exit:** genuine ELF/Mach-O/PE output is produced and executed for documented project/target combinations.

### Phase 19 — Compose application groups
Supported service graph, dependencies, ports and persistent state. **Exit:** unsupported keys are reported, never ignored.

### Phase 20 — GUI, enterprise and ecosystem
Optional GUI, policy packs, private artifact registry, remote cache and extension API. **Exit:** stable public contract and security ownership.

## Critical path

Phases 0–12 deliver the first useful Linux product. Phases 13–15 add desktop Linux-image workflows. Phase 17 is separate because Windows-native containers are not Linux containers. Phase 18 is separate because source compilation has different inputs and reproducibility requirements.

## Parallel work

- OCI schemas and registry prototype can proceed in parallel after domain types are agreed.
- Security harness and documentation proceed alongside ingestion.
- macOS/Windows feasibility spikes can begin after contract drafts but must not block the Linux vertical slice.
- Stable guest protocol follows the NIR/backend contract.

## Stop/go criteria

Pause expansion if layer semantics, digest verification, archive safety, rootless execution or artifact trust are not correct. Do not add GUI, Compose or toolchains to compensate for a weak compiler core.
