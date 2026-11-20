# Native Image Representation (NIR)

**Status:** proposed project schema, version 0.1. NIR is not an OCI standard.

## 1. Purpose and design requirements

NIR is the versioned, host-independent boundary between OCI ingestion and target-specific backends. It preserves image semantics while recording derived analysis separately.

Requirements:
- Canonical serialization and deterministic identity.
- Explicit schema version and required/optional feature lists.
- Immutable source identity and source provenance.
- Separate source facts, compiler findings and user overrides.
- Preservation of unknown optional annotations where safe.
- Rejection of unknown required features.
- Explicit Linux versus Windows source platform.
- No embedded credentials, runtime secrets or mutable state.

## 2. Proposed top-level structure

```json
{
  "schemaVersion": "0.1.0",
  "requiredFeatures": ["oci.image-config.v1", "rootfs.layers.v1"],
  "optionalFeatures": ["image.healthcheck.v1"],
  "identity": {
    "sourceReference": "registry.example/app@sha256:...",
    "manifestDigest": "sha256:...",
    "configDigest": "sha256:...",
    "rootfsDigest": "sha256:..."
  },
  "platform": {"os": "linux", "architecture": "arm64", "variant": null, "abi": "unknown"},
  "filesystem": {"root": "payload/rootfs", "layers": [], "metadataPolicy": "preserve-supported"},
  "process": {
    "entrypoint": ["/entrypoint.sh"], "args": ["serve"],
    "workingDirectory": "/", "user": {"kind": "image-default"}, "environment": []
  },
  "runtimeRequirements": {"kernelFeatures": [], "capabilities": [], "devices": [], "mounts": [], "privileged": false},
  "network": {"exposedPorts": []},
  "resources": {}, "metadata": {"labels": {}, "annotations": {}},
  "provenance": {"compilerVersion": "0.1.0"}
}
```

Illustrative only. Production schema must define exact types, required fields, bounds, enums and extension behavior.

## 3. Core Rust type sketch

```rust
pub struct NativeImage {
    pub schema_version: SchemaVersion,
    pub required_features: Vec<FeatureId>,
    pub optional_features: Vec<FeatureId>,
    pub identity: ImageIdentity,
    pub platform: SourcePlatform,
    pub filesystem: RootFsDescriptor,
    pub process: ProcessSpec,
    pub runtime: RuntimeRequirements,
    pub network: NetworkSpec,
    pub resources: ResourceRequirements,
    pub metadata: ImageMetadata,
    pub provenance: BuildProvenance,
}
```

These are API sketches, not drop-in compiled Rust code. Use validated newtypes for digests, normalized paths, platform identifiers, ports and user IDs.

## 4. Identity

`sourceReference` is informational and may contain a mutable tag. `manifestDigest` is the immutable selected image manifest. `configDigest` identifies image configuration. `rootfsDigest` is project-defined and must declare algorithm/version for normalized ordered filesystem input. Preserve layer source digest, media type, size, ordinal and diff ID where available.

## 5. Process and environment semantics

Preserve entrypoint and command separately as source facts. Store effective argv as a derived value with provenance. Environment entries should include key, value source, optional value and sensitivity. Do not capture build secrets. Inject runtime secrets through separately authorized secret references, never as literal values embedded into NIR or artifact metadata.

Represent process identity as image default, numeric UID/GID, name resolution, or explicit runtime override. Never map an unresolved non-root identity to root silently.

## 6. Filesystem semantics

Entries carry normalized image path, type, mode, owner, timestamps, link target, content digest/payload reference, supported xattrs/capabilities and source-layer provenance. Distinguish present, absent, defaulted and unrepresentable metadata. Do not flatten hardlinks when it changes observable semantics without recording a finding.

## 7. Runtime requirements and findings

Use structured requirements for privileged execution, capabilities, mount propagation, devices, shared memory, host networking, cgroup controllers, kernel modules, syscall needs and special filesystem mounts. Every requirement has source and confidence.

A compatibility finding includes stable code, severity, status, message, evidence, confidence, field path, target/backend, remediation and `blocksPackaging` / `blocksExecution` flags. Findings are generated separately from source facts so NIR can be re-analyzed.

## 8. Canonicalization and hashing

- UTF-8 textual representation.
- Path normalization independent of host filesystem.
- Canonical ordering for maps; preserve semantic array order (layers, argv, args).
- Define null versus omitted behavior.
- Hash canonical bytes with named algorithm and domain separation including NIR major version.
- Never claim a digest is stable when it hashes non-canonical serializer output.

## 9. Evolution

Patch: no wire change. Minor: optional fields/features. Major: breaking structure or semantics. Unknown required features cause rejection; unknown optional extensions are preserved where possible. Each supported major version requires migration logic and golden fixtures.
