# Implementation Readiness Assessment

**Generated:** 2026-11-20  
**Git commit:** f42f10a  
**Git branch:** main  

This document provides a comprehensive feature matrix, technical blockers, missing contracts, and implementation status for the Image2Native project.

## Feature Matrix

### Workspace Foundation

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Workspace structure | IMPLEMENTED | 34 packages in Cargo.toml | None |
| Rust toolchain | PARTIAL | Rust 1.100.0 available; CI not verified | I2N-0101 |
| Error model | PARTIAL | Diagnostic struct in i2n-diagnostics | I2N-0202 |
| Boundary enforcement | VERIFIED | project/boundaries.json, automation passes | None |
| Baseline verification | VERIFIED | project/baseline.json, automation passes | None |
| CI pipeline | IMPLEMENTED | .github/workflows/ci.yml | I2N-0101 |
| Repository automation | VERIFIED | scripts/i2n.py passes all checks | None |

### Domain Models

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Target platform types | IMPLEMENTED | TargetPlatform, OperatingSystem, Architecture | None |
| Digest types | IMPLEMENTED | Digest struct with parsing | None |
| Image reference parsing | MISSING | Not implemented | I2N-0201 |
| Platform identity fixtures | MISSING | No test fixtures | I2N-0201 |
| Digest validation | PARTIAL | Basic parsing; no cryptographic verification | I2N-0201, I2N-digest |

### OCI Resolver

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| OCI reference parser | MISSING | Not implemented | I2N-0301 |
| Descriptor models | MISSING | Not implemented | I2N-0301 |
| Manifest validation | MISSING | Not implemented | I2N-0301 |
| Index validation | MISSING | Not implemented | I2N-0301 |
| Config validation | MISSING | Not implemented | I2N-0301 |
| Media type constraints | MISSING | Not implemented | I2N-0301 |
| Test fixtures | MISSING | No fixtures | I2N-0301 |

### Registry Client

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| OCI Distribution API | MISSING | Not implemented | I2N-0302 |
| TLS support | MISSING | Not implemented | I2N-0302 |
| Registry auth | MISSING | Not implemented | I2N-0302 |
| Credential provider | MISSING | Not implemented | I2N-0302 |
| Manifest platform selection | MISSING | Not implemented | I2N-0302 |
| Retry logic | MISSING | Not implemented | I2N-0302 |
| Secret redaction | MISSING | Not implemented | I2N-0202 |

### Image Fetching

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Blob fetching | MISSING | Not implemented | I2N-0303 |
| Size verification | MISSING | Not implemented | I2N-0303 |
| Digest verification | MISSING | Not implemented | I2N-0303, I2N-digest |
| Bounded downloads | MISSING | Not implemented | I2N-0303 |
| Cancellation | MISSING | Not implemented | I2N-0303 |
| Resumable downloads | MISSING | Not implemented | I2N-0303 |
| Streaming | MISSING | Not implemented | I2N-0303 |

### Content Cache

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Content-addressed storage | MISSING | Not implemented | I2N-0401 |
| Atomic writes | MISSING | Not implemented | I2N-0401 |
| Concurrent writer safety | MISSING | Not implemented | I2N-0401 |
| Prune command | MISSING | Not implemented | I2N-0401 |
| Verify command | MISSING | Not implemented | I2N-0401 |
| Offline mode | MISSING | Not implemented | I2N-0401 |
| Eviction policy | MISSING | Not implemented | I2N-0401 |

### Layer Engine

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Layer decoder | MISSING | Not implemented | I2N-0501 |
| Compression formats | MISSING | Not implemented | I2N-0501 |
| Path traversal protection | MISSING | Not implemented | I2N-0501 |
| Symlink handling | MISSING | Not implemented | I2N-0501 |
| Hardlink handling | MISSING | Not implemented | I2N-0501 |
| Whiteout semantics | MISSING | Not implemented | I2N-0501 |
| Quotas | MISSING | Not implemented | I2N-0501 |
| Fuzz targets | MISSING | Not implemented | I2N-0501 |

### Archive Unpacking

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Safe unpacking | MISSING | Not implemented | I2N-0501 |
| Path normalization | MISSING | Not implemented | I2N-0501 |
| Metadata preservation | MISSING | Not implemented | I2N-0501 |
| xattrs support | MISSING | Not implemented | I2N-0501 |
| Decompression limits | MISSING | Not implemented | I2N-0501 |

### RootFS Compiler

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Logical rootfs model | MISSING | Not implemented | I2N-0601 |
| Layer ordering | MISSING | Not implemented | I2N-0601 |
| Mode preservation | MISSING | Not implemented | I2N-0601 |
| Ownership preservation | MISSING | Not implemented | I2N-0601 |
| Link preservation | MISSING | Not implemented | I2N-0601 |
| Provenance tracking | MISSING | Not implemented | I2N-0601 |
| Golden fixtures | MISSING | No fixtures | I2N-0601 |

### Filesystem Abstractions

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Path tree model | MISSING | Not implemented | None |
| Metadata normalization | MISSING | Not implemented | None |
| Cross-platform handling | MISSING | Not implemented | None |
| Case sensitivity | MISSING | Not implemented | None |

### Image Inspector

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Config inspection | MISSING | Not implemented | I2N-0701 |
| Entrypoint normalization | MISSING | Not implemented | I2N-0701 |
| Command normalization | MISSING | Not implemented | I2N-0701 |
| Environment handling | MISSING | Not implemented | I2N-0701 |
| User normalization | MISSING | Not implemented | I2N-0701 |
| Port extraction | MISSING | Not implemented | I2N-0701 |
| Volume detection | MISSING | Not implemented | I2N-0701 |
| Unknown field handling | MISSING | Not implemented | I2N-0701 |

### NIR (Native Image Representation)

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| NIR v0.1 schema | DRAFT | schemas/nir-v0.1.schema.json | I2N-0701 |
| ImageIdentity type | IMPLEMENTED | i2n-ir/src/lib.rs | Full NIR pending |
| ProcessSpec type | IMPLEMENTED | i2n-ir/src/lib.rs | Full NIR pending |
| NativeImage type | IMPLEMENTED | i2n-ir/src/lib.rs | Full NIR pending |
| Serialization | MISSING | Not implemented | I2N-0701 |
| Validation | MISSING | Not implemented | I2N-0701 |
| Canonicalization | MISSING | Not implemented | I2N-0701 |
| Golden fixtures | MISSING | No fixtures | I2N-0701 |
| Versioning | MISSING | Not implemented | I2N-0701 |

### Compatibility Analyzer

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| OS analysis | MISSING | Not implemented | I2N-0801 |
| Architecture analysis | MISSING | Not implemented | I2N-0801 |
| ABI detection | MISSING | Not implemented | I2N-0801 |
| Kernel requirements | MISSING | Not implemented | I2N-0801 |
| Privilege detection | MISSING | Not implemented | I2N-0801 |
| Capability analysis | MISSING | Not implemented | I2N-0801 |
| Device analysis | MISSING | Not implemented | I2N-0801 |
| Mount analysis | MISSING | Not implemented | I2N-0801 |
| Network analysis | MISSING | Not implemented | I2N-0801 |
| Finding codes | MISSING | Not implemented | I2N-0801 |
| Backend selection | MISSING | Not implemented | I2N-0801 |
| Policy engine | MISSING | Not implemented | I2N-0801 |

### Compiler Orchestration

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Stage contracts | MISSING | Not implemented | I2N-0901 |
| Execution planning | MISSING | Not implemented | I2N-0901 |
| Graph orchestration | MISSING | Not implemented | I2N-0901 |
| Checkpointing | MISSING | Not implemented | I2N-0901 |
| Cancellation | MISSING | Not implemented | I2N-0901 |
| Resource limits | MISSING | Not implemented | I2N-0901 |
| Progress reporting | MISSING | Not implemented | I2N-0901 |

### Linux Backend

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| OCI runtime integration | MISSING | Not implemented | I2N-0901 |
| Runtime selection | MISSING | Not implemented | Decision needed (runc vs youki) |
| Namespace support | MISSING | Not implemented | I2N-0901 |
| Cgroup support | MISSING | Not implemented | I2N-0901 |
| Seccomp support | MISSING | Not implemented | I2N-0901 |
| Capability restriction | MISSING | Not implemented | I2N-0901 |
| Rootless execution | MISSING | Not implemented | I2N-0901 |
| Filesystem mounting | MISSING | Not implemented | I2N-0901 |
| Device passthrough | MISSING | Not implemented | I2N-0901 |
| Network setup | MISSING | Not implemented | I2N-0901 |
| Lifecycle management | MISSING | Not implemented | I2N-0901 |

### macOS Backend

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Virtualization.framework | MISSING | Not implemented | I2N-1401 |
| Linux guest boot | MISSING | Not implemented | I2N-1401, I2N-1301 |
| Guest agent | MISSING | Not implemented | I2N-1401, I2N-1301 |
| Virtio devices | MISSING | Not implemented | I2N-1401 |
| .app packaging | MISSING | Not implemented | I2N-1401 |
| Code signing | MISSING | Not implemented | I2N-1401 |
| Entitlements | MISSING | Not implemented | I2N-1401 |
| Networking | MISSING | Not implemented | I2N-1401 |
| Shared storage | MISSING | Not implemented | I2N-1401 |

### Windows Backend

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| WSL2 integration | MISSING | Not implemented | I2N-1501, I2N-1301 |
| Guest provisioning | MISSING | Not implemented | I2N-1501 |
| Guest lifecycle | MISSING | Not implemented | I2N-1501 |
| Port forwarding | MISSING | Not implemented | I2N-1501 |
| Windows installer | MISSING | Not implemented | I2N-1501 |
| Native launcher | MISSING | Not implemented | I2N-1501 |
| HCS backend | MISSING | Not implemented | I2N-1701 (future) |
| Windows container support | MISSING | Not implemented | I2N-1701 (future) |

### Artifact System

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| I2N artifact schema | DRAFT | schemas/i2n-artifact-v1.schema.json | I2N-1001 |
| Manifest format | MISSING | Not implemented | I2N-1001 |
| Payload graph | MISSING | Not implemented | I2N-1001 |
| Reader/writer | MISSING | Not implemented | I2N-1001 |
| Digest verification | MISSING | Not implemented | I2N-1001 |
| Signature verification | MISSING | Not implemented | I2N-1001 |
| Installation | MISSING | Not implemented | I2N-1001 |
| Uninstallation | MISSING | Not implemented | I2N-1001 |
| Update support | MISSING | Not implemented | I2N-1001 |
| Rollback support | MISSING | Not implemented | I2N-1001 |

### Archive Format

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Deterministic archive | MISSING | Not implemented | None |
| Extraction | MISSING | Not implemented | None |
| Compression | MISSING | Not implemented | None |
| Integrity check | MISSING | Not implemented | None |

### SBOM

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| SPDX generation | MISSING | Not implemented | I2N-1101 |
| SPDX validation | MISSING | Not implemented | I2N-1101 |
| Scope definition | MISSING | Not implemented | I2N-1101 |
| Component inventory | MISSING | Not implemented | I2N-1101 |

### Signing

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Signature generation | MISSING | Not implemented | I2N-1101 |
| Signature verification | MISSING | Not implemented | I2N-1101 |
| Cosign compatibility | MISSING | Not implemented | Decision needed |
| Key management | MISSING | Not implemented | I2N-1101 |
| Trust policy | MISSING | Not implemented | I2N-1101 |

### Provenance

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Build provenance | MISSING | Not implemented | I2N-1101 |
| Source binding | MISSING | Not implemented | I2N-1101 |
| Toolchain identity | MISSING | Not implemented | I2N-1101 |
| Attestations | MISSING | Not implemented | I2N-1101 |

### Runtime Manager

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Lifecycle semantics | MISSING | Not implemented | None |
| Runtime plans | MISSING | Not implemented | None |
| Instance management | MISSING | Not implemented | None |
| State tracking | MISSING | Not implemented | None |

### Process Supervisor

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Process supervision | MISSING | Not implemented | None |
| VM supervision | MISSING | Not implemented | None |
| Event handling | MISSING | Not implemented | None |
| Instance state | MISSING | Not implemented | None |

### Networking

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Port mapping | MISSING | Not implemented | None |
| Network policy | MISSING | Not implemented | None |
| Host/guest channels | MISSING | Not implemented | None |

### Storage

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Writable overlays | MISSING | Not implemented | None |
| Volume management | MISSING | Not implemented | None |
| State persistence | MISSING | Not implemented | None |

### Security

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Policy evaluation | MISSING | Not implemented | None |
| Security boundaries | MISSING | Not implemented | None |
| Privilege checks | MISSING | Not implemented | None |

### Platform Contract

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| ExecutionKind enum | IMPLEMENTED | i2n-platform/src/lib.rs | None |
| BackendCapabilities | IMPLEMENTED | i2n-platform/src/lib.rs | None |
| PlatformBackend trait | IMPLEMENTED | i2n-platform/src/lib.rs | None |
| Capability detection | MISSING | Not implemented | None |
| Backend registration | MISSING | Not implemented | None |

### CLI

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Command parsing | PARTIAL | Basic commands implemented | Full CLI pending |
| Argument parsing | MISSING | Not implemented | I2N-1001 |
| Error handling | PARTIAL | Basic error messages | I2N-0202 |
| Progress output | MISSING | Not implemented | I2N-0901 |
| Configuration | MISSING | Not implemented | I2N-config |
| Doctor command | PARTIAL | Placeholder only | Full implementation pending |
| Compile command | MISSING | Reports not implemented | I2N-0901 |

### Launcher

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Native launcher | MISSING | Placeholder only | I2N-1001 |
| Artifact verification | MISSING | Not implemented | I2N-1001 |
| Runtime execution | MISSING | Not implemented | I2N-0901 |
| Lifecycle management | MISSING | Not implemented | I2N-1001 |

### Daemon

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Daemon service | MISSING | Placeholder only | Not prioritized |
| IPC protocol | MISSING | Not implemented | Not prioritized |
| Background tasks | MISSING | Not implemented | Not prioritized |

### Testing Infrastructure

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| Unit test harness | PLACEHOLDER | tests/unit/ empty | None |
| Integration test harness | PLACEHOLDER | tests/integration/ empty | None |
| Compatibility test harness | PLACEHOLDER | tests/compatibility/ empty | None |
| Security test harness | PLACEHOLDER | tests/security/ empty | None |
| Golden test fixtures | PLACEHOLDER | tests/golden/ empty | None |
| Test fixtures | PLACEHOLDER | tests/fixtures/ empty | None |
| Python automation | IMPLEMENTED | tests/python/test_repo_automation.py | None |

### CI

| Feature | Status | Evidence | Blockers |
|---------|--------|----------|----------|
| CI workflow | IMPLEMENTED | .github/workflows/ci.yml | I2N-0101 |
| fmt check | IMPLEMENTED | In CI | I2N-0101 |
| clippy check | IMPLEMENTED | In CI | I2N-0101 |
| test check | IMPLEMENTED | In CI | I2N-0101 |
| Repository automation | IMPLEMENTED | In CI | None |

## Technical Blockers

### Prerequisites

1. **I2N-0101: Rust toolchain verification**
   - Required: Rust stable, rustfmt, Clippy must pass on Linux, macOS, Windows CI
   - Current: Tools available but CI not yet verified
   - Impact: Blocks all Rust implementation verification
   - Estimated effort: S

2. **I2N-0201: Domain model completion**
   - Required: Target triples, digest validation, image references with fixtures
   - Current: Basic types implemented; missing reference parsing and fixtures
   - Impact: Blocks OCI ingestion (I2N-0301)
   - Estimated effort: M

3. **I2N-0202: Diagnostics framework**
   - Required: Stable error codes, retryability, secret redaction
   - Current: Basic Diagnostic struct; missing codes and redaction
   - Impact: Blocks all error handling consistency
   - Estimated effort: M

### Missing Decisions

1. **External dependency selection**
   - HTTP client: reqwest vs hyper vs ureq
   - Digest library: sha2 vs rust-crypto vs custom
   - Compression: flate2 vs libz-sys
   - OCI parsing: oci-distribution vs custom
   - Impact: Blocks OCI ingestion, layer engine
   - Estimated effort: S (decision) + M (integration)

2. **OCI runtime selection**
   - Options: runc vs youki vs crun
   - Impact: Blocks Linux backend integration
   - Estimated effort: S (decision) + L (integration)

3. **Immutable rootfs format**
   - Options: SquashFS vs EROFS vs custom
   - Impact: Blocks artifact format, runtime execution
   - Estimated effort: M (decision + implementation)

4. **Guest kernel version**
   - Options: Which kernel version, init system, guest OS
   - Impact: Blocks macOS/Windows Linux guest backends
   - Estimated effort: L (decision + build system)

5. **Signing scheme**
   - Options: Cosign vs Sigstore-compatible custom
   - Impact: Blocks artifact signing, trust verification
   - Estimated effort: M (decision + implementation)

### Architectural Gaps

1. **Zero dependency edges**
   - Current: Most crates have no dependencies
   - Required: Dependency graph must be populated as implementation progresses
   - Impact: No integration between crates
   - Estimated effort: Ongoing with each crate

2. **No test fixtures**
   - Current: All test directories are empty
   - Required: Golden fixtures, adversarial fixtures, integration tests
   - Impact: No verification of correctness
   - Estimated effort: L across all subsystems

3. **No external dependencies**
   - Current: Cargo.lock contains only workspace members
   - Required: Third-party crates for HTTP, crypto, compression, etc.
   - Impact: Cannot implement real functionality
   - Estimated effort: S (decision) + M (integration)

## Missing Contracts

### Missing Interfaces

1. **Fetcher contract**
   - Needs: Bounded transfer trait, cancellation token, progress callback
   - Owner: i2n-fetcher
   - Status: Not defined

2. **Cache contract**
   - Needs: Atomic storage trait, eviction policy interface
   - Owner: i2n-cache
   - Status: Not defined

3. **Layer decoder contract**
   - Needs: Decoder trait, compression codec registry
   - Owner: i2n-layer
   - Status: Not defined

4. **RootFS builder contract**
   - Needs: Builder trait, layer application semantics
   - Owner: i2n-rootfs
   - Status: Not defined

5. **Inspector contract**
   - Needs: Image inspection trait, config normalization
   - Owner: i2n-inspector
   - Status: Not defined

6. **Analyzer contract**
   - Needs: Compatibility analysis trait, finding interface
   - Owner: i2n-analyzer
   - Status: Not defined

7. **Compiler contract**
   - Needs: Stage trait, orchestration interface
   - Owner: i2n-compiler
   - Status: Not defined

8. **Artifact contract**
   - Needs: Reader/writer traits, manifest interface
   - Owner: i2n-artifact
   - Status: Not defined

9. **Runtime contract**
   - Needs: Lifecycle trait, instance management
   - Owner: i2n-runtime
   - Status: Not defined

## Missing Tests

### Unit Tests

- No unit tests exist in any crate
- Only i2n-model has basic tests (TargetPlatform, Digest parsing)
- Test coverage: < 1%

### Integration Tests

- No integration tests exist
- Test harnesses are empty directories
- No end-to-end verification

### Security Tests

- No security tests exist
- No adversarial input fixtures
- No fuzzing targets

### Golden Tests

- No golden fixtures exist
- No output verification

## Build and Validation Status

### Cargo Commands

```bash
cargo build --workspace          # Status: Not yet validated
cargo test --workspace           # Status: No tests to run
cargo clippy --workspace         # Status: Not yet validated
cargo fmt --all                  # Status: Not yet validated
```

### Repository Automation

```bash
python3 scripts/i2n.py status              # Status: PASS
python3 scripts/i2n.py inventory --check   # Status: PASS
python3 scripts/i2n.py checklist --write   # Status: PASS
python3 scripts/i2n.py baseline verify     # Status: PASS
python3 scripts/i2n.py validate            # Status: PASS
```

**Validation results:**
- Workspace packages: 34 present, 0 missing
- Repository components: 9 present, 0 missing
- Boundary violations: 0
- Task graph issues: 0
- Baseline control files: unchanged

### CI Pipeline

**File:** .github/workflows/ci.yml

**Status:** Workflow exists but Rust checks may not pass without toolchain verification (I2N-0101)

## Recommended Implementation Sequence

### Phase 1: Foundation (Estimated: S)

1. **I2N-0101: Rust toolchain verification**
   - Verify cargo fmt, cargo test, cargo clippy pass on CI
   - Add missing toolchain pins if needed
   - Estimated: S

2. **I2N-0202: Diagnostics framework**
   - Define stable error codes
   - Implement secret redaction
   - Add retryability flags
   - Estimated: M

### Phase 2: Domain (Estimated: M)

3. **I2N-0201: Domain model completion**
   - Add image reference parsing
   - Add digest validation (cryptographic)
   - Create golden and invalid fixtures
   - Estimated: M

### Phase 3: OCI Ingestion (Estimated: L)

4. **I2N-0301: OCI models**
   - Implement OCI reference parser
   - Implement descriptor models
   - Implement manifest/index/config validation
   - Add positive and negative fixtures
   - Estimated: M

5. **External dependency decisions**
   - Select HTTP client
   - Select digest library
   - Select compression library
   - Estimated: S

6. **I2N-0302: Registry client**
   - Implement OCI Distribution API
   - Implement TLS support
   - Implement credential provider
   - Implement secret redaction
   - Estimated: L

7. **I2N-0303: Fetcher**
   - Implement bounded blob transfer
   - Implement size/digest verification
   - Implement cancellation
   - Estimated: M

8. **I2N-0401: Cache**
   - Implement content-addressed storage
   - Implement atomic writes
   - Implement concurrent writer safety
   - Estimated: M

### Phase 4: Filesystem (Estimated: L)

9. **I2N-0501: Layer engine**
   - Implement layer decoder
   - Implement compression formats
   - Implement path traversal protection
   - Implement whiteout semantics
   - Add adversarial fixtures
   - Estimated: L

10. **I2N-0601: RootFS**
    - Implement logical rootfs model
    - Implement layer ordering
    - Implement metadata preservation
    - Create golden fixtures
    - Estimated: L

### Phase 5: NIR and Analysis (Estimated: L)

11. **I2N-0701: Inspector and NIR**
    - Implement image inspector
    - Complete NIR v0.1 implementation
    - Implement serialization/validation
    - Create golden fixtures
    - Estimated: L

12. **I2N-0801: Analyzer**
    - Implement compatibility analysis
    - Implement backend selection
    - Implement policy engine
    - Estimated: L

### Phase 6: Linux Backend (Estimated: XL)

13. **Runtime decision**
    - Select OCI runtime (runc vs youki)
    - Estimated: S

14. **I2N-0901: Linux backend**
    - Integrate OCI runtime
    - Implement namespaces/cgroups/seccomp
    - Implement rootless execution
    - Estimated: XL

15. **I2N-1001: Artifact and launcher**
    - Implement I2N artifact format
    - Implement Linux launcher
    - Implement install/run/uninstall
    - Estimated: L

### Phase 7: Trust (Estimated: M)

16. **Signing decision**
    - Select Cosign vs custom
    - Estimated: S

17. **I2N-1101: SBOM, provenance, signing**
    - Implement SPDX generation
    - Implement build provenance
    - Implement signing/verification
    - Estimated: M

### Phase 8: Desktop Platforms (Estimated: XL)

18. **I2N-1301: Guest build system**
    - Build pinned Linux guest
    - Implement guest agent
    - Estimated: XL

19. **I2N-1401: macOS backend**
    - Implement Virtualization.framework
    - Implement .app packaging
    - Estimated: XL

20. **I2N-1501: Windows backend**
    - Implement WSL2 integration
    - Implement Windows launcher
    - Estimated: XL

## Complexity Estimates

- **S:** Small (1-2 days, isolated changes)
- **M:** Medium (3-7 days, moderate complexity)
- **L:** Large (1-3 weeks, complex integration)
- **XL:** Extra Large (1-2 months, platform-specific work)

## Risk Assessment

### High Risk

1. **Archive extraction vulnerability** (Critical)
   - Impact: Security breach
   - Mitigation: Logical rootfs, quotas, fuzzing, hardened parser
   - Status: Not mitigated yet

2. **Container escape/overprivilege** (Critical)
   - Impact: Security breach
   - Mitigation: Mature runtime, rootless, least privilege, security review
   - Status: Not mitigated yet

3. **Incorrect layer merge** (High)
   - Impact: Incorrect application behavior
   - Mitigation: OCI conformance, golden whiteout tests
   - Status: Not mitigated yet

### Medium Risk

4. **macOS entitlement/distribution** (High)
   - Impact: Cannot ship on macOS
   - Mitigation: Early signed prototype, channel validation
   - Status: Not mitigated yet

5. **WSL2 variability** (High)
   - Impact: Windows compatibility issues
   - Mitigation: Doctor, supported matrix, managed guest
   - Status: Not mitigated yet

6. **Guest kernel compromise** (High)
   - Impact: Security breach
   - Mitigation: Pin, sign, attest, patch guest components
   - Status: Not mitigated yet

7. **Cross-architecture mismatch** (High)
   - Impact: Application fails to run
   - Mitigation: Explicit emulation policy; never infer success
   - Status: Not mitigated yet

### Low Risk

8. **Source toolchain complexity** (High)
   - Impact: Source compilation delays
   - Mitigation: Independent milestone, support matrix
   - Status: Deferred to Phase 18

## Acceptance Criteria Summary

For a feature to be marked **IMPLEMENTED** or **VERIFIED**, it must have:

1. **Functional code:** Actual implementation, not just interfaces
2. **Tests:** Unit tests, integration tests where applicable
3. **Documentation:** Public API documented
4. **Evidence:** Test results, benchmarks, or verification output
5. **No blockers:** All prerequisites satisfied
6. **Boundary compliance:** Dependencies within allowed groups
7. **CI passing:** All CI checks pass

## Conclusion

**Implementation readiness:**

- **Ready to implement immediately:** I2N-0101, I2N-0202, I2N-0201
- **Blocked by dependencies:** All other tasks
- **Critical path:** Foundation → Domain → OCI → Filesystem → NIR → Analysis → Linux Backend → Artifact → Trust
- **Estimated time to first working artifact:** Phase 1-6 (S + M + L + L + L + L = ~3-4 months)
- **Estimated time to full Linux support:** Phase 1-7 (~4-5 months)
- **Estimated time to desktop support:** Phase 1-8 (~6-8 months)

**Next step:** See docs/engineering/IMPLEMENTATION-START.md for the first concrete implementation task.
