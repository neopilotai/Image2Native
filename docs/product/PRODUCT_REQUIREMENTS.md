# Product Requirements

## 1. Product definition

Image2Native transforms OCI image inputs into target-specific, verifiable application artifacts. It is not a universal Linux binary translator and does not aim to replace every container development tool.

## 2. Primary users

- **Application developer:** packages an existing image into an installable application without requiring end users to install Docker Engine.
- **Tool vendor:** needs native launchers, stable updates, app identity, logs, service lifecycle and a predictable support matrix.
- **Platform engineer:** needs offline inspection, digest pinning, reproducible packaging, SBOM/provenance and policy checks.
- **Enterprise administrator:** needs signed artifacts, trusted publisher policy, managed installation, vulnerability metadata and auditable runtime configuration.

## 3. Core user journeys

1. `analyze image:tag --target host` resolves and inspects an image without executing it.
2. `compile image@sha256:... --target linux-x86_64` creates an immutable I2N artifact.
3. `verify artifact` validates digests and the configured signature policy.
4. `install artifact` registers it without silently installing privileged services.
5. `run app` starts it using the declared backend.
6. `doctor` reports missing kernel, runtime, virtualization, signing or filesystem prerequisites.
7. `update` applies a signed update while preserving state according to policy.

## 4. Functional requirements

### Image acquisition
- Accept registry references, immutable digests, OCI image layouts and supported Docker archives.
- Resolve tags to immutable descriptors and record both the original reference and resolved digest.
- Support image indexes and explicit platform selection.
- Support registry authentication without logging secrets.
- Verify descriptor size and digest for downloaded blobs.
- Bound concurrency, retries, memory, disk and response sizes.

### Filesystem compilation
- Apply layers in descriptor order and implement OCI whiteout semantics.
- Preserve supported file types, modes, ownership, timestamps, symlinks, hardlinks and extended metadata.
- Record metadata that cannot be represented by a particular backend.
- Prevent traversal, link escape and unsafe host device creation.

### Image configuration
- Preserve entrypoint, command, environment, user, working directory, stop signal, health check, exposed ports, volume declarations and relevant annotations.
- Distinguish image defaults from user overrides.
- Never execute image-defined shell commands during compilation.

### Analysis
- Report source OS/architecture, target OS/architecture, ABI assumptions and backend.
- Identify unsupported features and host prerequisites.
- Use `supported`, `supported-with-warnings`, `unsupported`, `requires-explicit-policy` and `unknown` statuses.
- Attach evidence, confidence and remediation to findings.

### Packaging and runtime
- Create versioned, target-specific I2N artifacts.
- Include source digest, NIR, execution plan, payload digests, runtime references, SBOM and provenance.
- Verify artifact integrity and configured signature policy.
- Install, launch, stop, restart, inspect status, retrieve logs, update, rollback and uninstall.
- Keep immutable payload separate from writable state.
- Require explicit permission for host mounts, devices, privileged modes and network exposure.

## 5. Non-functional requirements

- **Correctness:** OCI descriptors and filesystem changesets follow pinned spec versions.
- **Security:** untrusted input is validated at parser, extraction, artifact and runtime boundaries.
- **Portability:** core crates build on supported Rust hosts; native bridge code is isolated.
- **Reproducibility:** build records identify immutable inputs and tool versions.
- **Observability:** structured logs and stable diagnostics identify stage and cause.
- **Performance:** caching and concurrency avoid repeated work without compromising determinism.
- **Accessibility:** human output plus machine-readable JSON.

## 6. Support status vocabulary

- `supported`: tested on named OS version, architecture and backend.
- `supported-with-warnings`: tested, with documented constraints.
- `experimental`: implementation exists without stable support guarantee.
- `unsupported`: known required feature cannot be provided.
- `not-tested`: no validated result; never display as supported.

## 7. MVP acceptance criteria

A pinned OCI image can be resolved without Docker Engine, verified, reconstructed into a correct logical rootfs, lowered to NIR, analyzed, packaged into I2N and run on a supported Linux host using a mature OCI runtime. Tests cover whiteouts, metadata, entrypoint, environment and common failure cases.

## 8. Product guardrails

- Do not call a Linux workload running in a guest “native-compiled”.
- Do not promise universal OCI image compatibility.
- Do not enable privileged execution silently.
- Do not bundle third-party components without license and redistribution review.
- Do not require a proprietary registry or cloud control plane for local use.
- Do not make the optional daemon a prerequisite for the core CLI.
