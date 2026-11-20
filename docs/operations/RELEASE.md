# Release Engineering

## 1. Principles

A release is a signed, verifiable set of binaries, guest components, schemas, documentation and provenance. Builds should be reproducible where practical, and signing must be separated from untrusted build steps.

## 2. Channels

- `nightly`: development artifacts, not trusted by default.
- `preview`: candidate builds with explicit warnings.
- `stable`: all compatibility/security gates pass.
- `lts`: only after maintenance capacity and support policy exist.

## 3. Versioning

Use semantic versioning for CLI and libraries. NIR and I2N version independently. Guest kernel and agent versions are pinned in manifests. Every stable release states exact tested OS/build matrix and runtime versions.

## 4. Release pipeline

1. Checkout protected release commit.
2. Build on isolated CI workers for each target.
3. Pin toolchains, dependencies and guest inputs.
4. Run unit, integration, conformance, security and E2E tests.
5. Generate SBOM and provenance.
6. Verify all payload digests.
7. Sign artifacts from a protected signing environment.
8. Verify signatures independently.
9. Publish checksums, signatures, attestations and compatibility notes.
10. Test install and rollback from published artifacts.

## 5. macOS

Validate virtualization entitlement, code signing, hardened runtime, notarization and package behavior for each distribution channel. A development build does not establish public distribution readiness.

## 6. Windows

Sign executables and installers. Validate WSL2 prerequisites and supported Windows builds. Document optional elevation or Windows feature changes. Do not silently modify system settings.

## 7. Linux

Publish per-architecture binaries/packages. Document runtime requirements and rootless behavior. Do not infer distribution compatibility from Rust target compilation alone.

## 8. Guest components

Track guest kernel/agent source commit, build configuration, digest, signature and compatibility metadata. Support staged updates and rollback, but enforce policy against rollback to vulnerable versions.

## 9. Vulnerability response

Maintain supported-version policy, CVE triage, security release notes and artifact revocation. For compromised signing identity, publish deny/revocation policy and reissue affected artifacts. For guest kernel/runtime defects, define urgency, update path and user-visible status.

## 10. Release checklist

- [ ] Protected release tag and source commit.
- [ ] Pinned toolchain and dependencies.
- [ ] Tests on every declared stable target.
- [ ] Artifact hashes match manifests.
- [ ] SBOM and provenance generated.
- [ ] Signatures verify under release trust policy.
- [ ] Guest components signed and pinned.
- [ ] Install/update/uninstall tested.
- [ ] Compatibility documentation is accurate.
- [ ] Third-party licenses and notices reviewed.
- [ ] Rollback and incident procedures exercised.
