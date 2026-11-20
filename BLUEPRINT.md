# Image2Native Engineering Blueprint

**Version:** 0.1 · **Status:** proposed implementation baseline · **Planning date:** 20 November 2026

## 1. Mission

Implement a Rust-first compiler and packaging system that accepts Docker/OCI images and produces verified, target-specific application artifacts for Linux, macOS and Windows. First deliver a complete Linux vertical slice. Then reuse NIR and the artifact contract for macOS and Windows Linux-guest backends. Native source compilation is a separate subsystem and milestone.

## 2. Non-negotiable architecture rules

1. OCI image and distribution specifications define the image input contract.
2. Docker Engine must not be required for normal image ingestion, compilation, inspection or packaged execution.
3. Core crates must not depend on macOS or Windows SDKs.
4. NIR separates source image semantics from backend-specific execution.
5. Unknown required features and unsupported requirements fail closed.
6. Tags are mutable names; output artifacts pin resolved immutable digests.
7. Images and archives are untrusted input.
8. Rootless and least-privilege execution is preferred; no implicit privilege escalation.
9. NIR and I2N are versioned, tested contracts.
10. A native launcher must not be described as a natively compiled Linux workload.

## 3. Architecture and ownership

```text
Image reference / OCI archive
          |
          v
 OCI resolver + registry client
          |
          v
 Fetcher -> digest verification -> content cache
          |
          v
 Layer decoder -> safe layer applier -> logical RootFS
          |
          v
 Image inspector -> NIR compiler
          |
          v
 Compatibility analyzer + policy engine
          |
          v
 Explicit backend execution plan
       /             |             \
   Linux           macOS          Windows
   host OCI        Linux VM       WSL2 Linux VM
   runtime         via Virtual.   / future HCS
       \             |             /
        \            |            /
            I2N artifact linker
                    |
          verify / install / run
```

### Crate groups

**Domain and contracts:** `i2n-model`, `i2n-config`, `i2n-ir`, `i2n-protocol` (only if daemon/IPC exists).

**OCI acquisition:** `i2n-oci`, `i2n-registry`, `i2n-fetcher`, `i2n-digest`, `i2n-cache`.

**Image compiler:** `i2n-layer`, `i2n-rootfs`, `i2n-inspector`, `i2n-analyzer`, `i2n-compiler`.

**Artifact and trust:** `i2n-artifact`, `i2n-archive`, `i2n-sbom`, `i2n-provenance`, `i2n-signing`.

**Runtime and platforms:** `i2n-runtime`, `i2n-supervisor`, `i2n-platform`, `i2n-platform-linux`, `i2n-platform-macos`, `i2n-platform-windows`, `i2n-network`, `i2n-storage`, `i2n-security`.

**Apps:** `image2native-cli`, `image2native-launcher`, optional `image2native-daemon`.

## 4. Dependency direction

```text
i2n-model
  ├── i2n-oci -> i2n-registry -> i2n-fetcher -> i2n-cache
  ├── i2n-layer -> i2n-rootfs
  ├── i2n-inspector -> i2n-ir -> i2n-analyzer
  ├── i2n-artifact -> i2n-signing / i2n-sbom / i2n-provenance
  └── i2n-platform (shared traits)

OCI + RootFS + Inspector + NIR
              |
         i2n-compiler
              |
       compatibility plan
              |
       artifact linker
              |
       platform backends
              |
          CLI / launcher
```

No core crate depends on a concrete platform implementation. Platform crates may depend on shared traits and their own native bridge. Avoid cyclic dependencies and broad `common` crates.

## 5. Compiler stage contracts

| Stage | Input | Output | Owner | Key failure |
|---|---|---|---|---|
| Resolve | reference + target | selected manifest graph | OCI/registry | auth, missing tag, no platform |
| Fetch | descriptors | verified blobs | fetcher/cache | digest or size mismatch |
| Decode | compressed layer | ordered entries | layer | corrupt archive/unsupported codec |
| Apply | layer entries | logical rootfs | rootfs | invalid whiteout/path/link |
| Normalize | image config + rootfs | NIR | inspector/IR | invalid config/ambiguous process |
| Analyze | NIR + target + policy | compatibility report | analyzer | unsupported ABI/kernel need |
| Plan | report + user choice | execution plan | compiler | no eligible backend |
| Link | NIR + plan + payload | I2N bundle | artifact | manifest/payload failure |
| Verify | artifact | verified artifact | artifact/signing | digest/signature failure |
| Run | artifact + options | instance handle | backend/runtime | prerequisite/runtime failure |

Each stage must expose typed inputs/outputs, cancellation, resource limits, structured diagnostics and tests. Verified stage outputs should be checkpointable.

## 6. Proposed technical choices

| Concern | Choice | Guardrail |
|---|---|---|
| Language | Rust | Native bridges isolated behind small interfaces |
| Image format | OCI Image | Pin spec release/media-type behavior |
| Distribution | OCI Distribution | Credential isolation and digest checks |
| Linux execution | integrate runc or evaluate youki | Do not implement isolation runtime from scratch |
| macOS | Virtualization.framework | Test entitlement and distribution early |
| Windows Linux | WSL2 first | Explicit managed guest and preflight |
| Windows-native images | HCS later | Separate backend and semantics |
| SBOM | SPDX | Pin schema version and define scope |
| Signing | Sigstore/Cosign-compatible | Reuse proven signing/attestation ecosystem |
| Immutable rootfs | evaluate SquashFS/EROFS | Verify metadata/kernel support and benchmark |

## 7. Twenty-one implementation phases

Phase 0 — **Product and contract freeze:** workspace map, requirements, threat model, NIR/I2N drafts, ADR process. Exit: architecture reviewed.

Phase 1 — **Rust workspace and CI:** toolchain, error model, tracing, lint, test fixtures, architecture checks. Exit: clean builds and tests.

Phase 2 — **OCI domain model:** reference parser, descriptors, manifest/index/config validation. Exit: golden and invalid fixtures pass.

Phase 3 — **Registry ingestion:** OCI Distribution pull, auth provider, local layout import, blob streaming and digest verification. Exit: pull pinned images without Docker Engine.

Phase 4 — **Content-addressed cache:** atomic blob store, metadata index, prune/verify/offline. Exit: no partial object can be treated as verified.

Phase 5 — **Layer decoder and safe extraction:** codecs, path/link rules, decompression quotas, fuzz harness. Exit: adversarial archive fixtures pass.

Phase 6 — **RootFS reconstruction:** layer ordering, whiteouts, permissions and provenance. Exit: golden rootfs matches expected semantics.

Phase 7 — **Image config and NIR 0.1:** process config, environment sensitivity, canonicalization. Exit: NIR fixtures and unknown-required-feature rejection pass.

Phase 8 — **Compatibility analyzer:** architecture, ABI evidence, kernel/runtime requirements, policy findings. Exit: no unknown property is silently marked supported.

Phase 9 — **Linux runtime adapter:** OCI runtime bundle, rootless preflight, namespaces, cgroups, capabilities, seccomp and lifecycle. Exit: representative applications run without Docker Engine.

Phase 10 — **I2N artifact and Linux launcher:** manifest, payload graph, reader/writer, install/run/uninstall. Exit: copied artifact runs on clean supported Linux host.

Phase 11 — **SBOM, provenance, signatures:** SPDX output, build records, Cosign-compatible signing/verification. Exit: tampered or untrusted artifacts fail policy.

Phase 12 — **Linux 0.2 hardening:** updates, rollback, state retention, performance and security. Exit: production-like lifecycle passes.

Phase 13 — **Guest build system:** pinned Linux kernel, minimal init, guest agent, reproducible guest images. Exit: signed guest and authenticated agent handshake.

Phase 14 — **macOS backend:** native bridge, VM lifecycle, Virtio devices, `.app` packaging and signing. Exit: end-to-end run on real Apple Silicon and Intel hosts within stated support range.

Phase 15 — **Windows WSL2 backend:** native launcher, managed guest provisioning, agent, networking and installer. Exit: end-to-end run on supported Windows builds.

Phase 16 — **Update trust hardening:** split app and guest updates, delta chunks, trust rotation, rollback protection. Exit: interrupted or malicious update never replaces last-good artifact.

Phase 17 — **Windows-native image backend:** HCS adapter and Windows image semantics. Exit: own conformance/E2E suite on named Windows hosts.

Phase 18 — **Source-to-native compiler:** source context and Rust/Go/C/C++ toolchains. Exit: actual native outputs are built and validated for documented target sets.

Phase 19 — **Compose application groups:** service graph, dependencies, ports and state for an explicit supported subset. Exit: unsupported keys are reported rather than ignored.

Phase 20 — **GUI, enterprise and ecosystem:** optional GUI, policy packs, private artifact registry, remote cache and extension API. Exit: stable APIs and security ownership.

## 8. Critical path and parallel work

Phases 0–12 deliver the first useful Linux product. Phases 13–15 add desktop Linux-image workflows. Phase 17 is distinct because Windows-native containers are not Linux containers. Phase 18 is distinct because source compilation has different input and reproducibility requirements.

A macOS/Windows feasibility spike may begin in parallel after contract drafts, but must not block the Linux vertical slice. Security tests and docs should be maintained from Phase 0, not deferred.

## 9. Definition of done

A feature is complete only when requirements, failure cases, unit/adversarial tests, structured diagnostics, security review, platform integration tests, documentation and release notes are present. Cross-compilation alone is not evidence of runtime support.

## 10. Main risks

| Risk | Severity | Mitigation |
|---|---|---|
| Users expect binary translation | High | Separate packaging/source compilation modes everywhere |
| Incorrect layer merge | High | OCI conformance and golden whiteout tests |
| Archive extraction vulnerability | Critical | Logical rootfs, quotas, fuzzing, hardened parser |
| Container escape/overprivilege | Critical | Mature runtime, rootless, least privilege, security review |
| macOS entitlement/distribution | High | Early signed prototype and channel validation |
| WSL2 variability | High | `doctor`, supported matrix, managed guest |
| Guest kernel compromise | High | Pin, sign, attest and patch guest components |
| Cross-architecture mismatch | High | Explicit emulation policy; never infer success |
| Source toolchain complexity | High | Independent milestone and support matrix |

## 11. First milestone issue breakdown

- Create Rust workspace, pinned toolchain and CI.
- Define digest/platform/path newtypes and structured errors.
- Implement OCI reference and descriptor parsing.
- Add test registry/local OCI fixture.
- Implement resolver, registry auth and blob fetcher.
- Implement verified content cache.
- Build safe layer entry parser and whiteout engine.
- Generate rootfs golden fixtures.
- Normalize image config and emit NIR.
- Build compatibility report and JSON output.

## 12. Release gates

- [ ] No Docker Engine dependency for ingestion or core compile.
- [ ] Immutable source digest recorded and verified.
- [ ] Safe extraction and whiteout semantics tested.
- [ ] NIR and I2N schemas are versioned.
- [ ] Backend strategy visible and correct.
- [ ] No silent privilege escalation or dropped runtime requirement.
- [ ] Guest/runtime components pinned and verified.
- [ ] Artifact digest, signature, SBOM and provenance checks pass.
- [ ] Install/update/rollback/uninstall tested.
- [ ] Licenses and redistribution notices reviewed.
- [ ] Support matrix reflects actual evidence.
