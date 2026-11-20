# Compiler Pipeline Specification

## 1. Stage contract

Every stage has typed input/output, versioned metadata, structured diagnostics, cancellation behavior, resource limits and tests. Do not pass raw unvalidated JSON or arbitrary host paths between stages.

## 2. Resolve OCI references

Accepted input forms: registry/repository tag, registry/repository digest, local OCI layout, and explicitly supported archive formats.

1. Parse and normalize the reference.
2. Establish TLS and handle registry authentication through a credential provider.
3. Request supported manifest/index media types.
4. Validate media type, descriptor digest and size.
5. If an image index is returned, select the platform using explicit target and documented matching rules.
6. Fetch selected manifest and image configuration descriptor.
7. Record requested reference, registry, manifest/config digests, source OS/architecture/variant and layer descriptors.

A floating tag must be resolved once and its immutable digest embedded in the artifact. Reproducible builds should accept or emit digest-pinned sources.

## 3. Fetch and cache

- Fetch by digest and expected size.
- Bound blob size, total download, concurrency and memory.
- Stream to temporary objects, hash while downloading, verify size and digest, then atomically publish.
- Redact authorization headers and bearer tokens from logs/errors.
- Retry transient network failures only; digest mismatch is a hard integrity failure.
- Make cache metadata disposable and rebuildable. Protect active build objects from eviction.

## 4. Layer decode and application

Use streaming decompression with limits for compressed size, expanded size, file count, nesting/metadata complexity and time. Apply layers in descriptor order and follow OCI layer whiteout semantics. Do not use an unguarded host `tar -xf` into a trusted directory.

Required protections:
- Normalize paths and reject absolute paths or traversal outside logical root.
- Define symlink and hardlink handling, including targets outside root.
- Correctly process whiteout and opaque-directory markers.
- Preserve directory metadata according to layer semantics.
- Define policy for device nodes, FIFOs, sockets, xattrs, capabilities and ownership.
- Detect conflicting entry types and duplicate paths.
- Enforce storage quota and fail atomically.

## 5. RootFS model

Use a deterministic logical path tree or equivalent. Support regular files, directories, symlinks, hardlinks, metadata, supported xattrs and source-layer provenance. Distinguish absent metadata from explicit zero/empty values. Host materialization is not the semantic model; this matters on Windows build hosts that cannot represent all Linux metadata or case-distinct paths.

## 6. Image configuration normalization

Preserve source fields and the provenance of defaults/overrides. Handle entrypoint and command combination according to image configuration semantics; shell form is not interchangeable with exec-form argv. Capture OS, architecture, variant, environment, cwd, user, entrypoint, command, stop signal, exposed ports, volume declarations, health check, labels and layer/diff IDs where available.

Do not execute image-defined commands during image compilation. Dockerfile `RUN` support is a separate build-context feature, not part of OCI image ingestion.

## 7. Static binary inspection

Inspect ELF headers, architecture, dynamic loader paths, shared library references, scripts and shebangs without executing unknown binaries. An ELF header does not prove kernel compatibility. Record `unknown` when evidence is insufficient.

## 8. NIR lowering

Generate canonical NIR from resolved identity, rootfs, configuration and static findings. Sort unordered metadata, normalize path representation and preserve ordered layers/argv. Preserve unknown optional annotations where safe; reject unknown required semantics.

## 9. Compatibility analysis

Evaluate OS family, binary format, architecture/variant, ABI and loader evidence, known kernel features, privileged mode, capabilities, namespaces, devices, mounts, shared memory, IPC, networking, cgroups, filesystem needs, host virtualization and source image type. Every finding contains stable code, severity, status, evidence, confidence, remediation and whether it blocks package or execution.

## 10. Backend plan

The versioned plan pins backend ID/version, guest/kernel identity if any, launcher type, payload reference, resource defaults, port rules, mount allowlist, security profile and required host capabilities. User overrides are recorded and validated.

## 11. Link and verify

The linker consumes NIR, backend plan and verified payload; it never fetches mutable tags or executes the workload. It writes the manifest and payload graph, verifies all outputs, then atomically publishes. Verification checks payload digests and signature policy without installing or executing.

## 12. Determinism

Use pinned source digests and tool versions, normalized metadata, stable archive ordering, controlled timestamps, deterministic compression settings, canonical manifests and recorded options. Separate deterministic payload identity from signature envelope/timestamp identity.
