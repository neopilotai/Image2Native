# Linux Backend

## 1. Role

The Linux backend runs compatible Linux OCI workloads using the host Linux kernel and a mature OCI runtime. It is the first implementation target and reference for application lifecycle behavior.

## 2. Runtime integration

Evaluate `runc` and `youki` and select one using maintenance, compatibility, security and licensing review. Do not implement a new container-isolation runtime from scratch. The backend stages an OCI-compatible bundle and delegates create/start/kill/delete semantics to the selected runtime. Record runtime name, version and effective configuration in diagnostics.

## 3. NIR-to-runtime mapping

Map rootfs path/read-only mode; process argv/env/cwd/user/terminal; mounts; namespaces; cgroup resource limits; capabilities; `no_new_privs`; seccomp and LSM policy where available; hostname; and safe lifecycle configuration. Image metadata must never become an arbitrary host hook. Do not forward image-specified host hooks into the runtime.

## 4. Rootless-first

Prefer rootless execution. Preflight user namespaces, subordinate UID/GID mappings where necessary, mount capability and cgroup delegation. If a requirement cannot be met rootlessly, show the reason and fail or require a separately designed explicit privileged mode. Never silently retry with root.

A future privileged helper must be narrowly scoped, signed, auditable, versioned and reviewed as a separate security boundary. It is not part of the MVP.

## 5. Security profile

- Separate namespaces where supported and required.
- Drop all capabilities by default; add only documented minimums.
- Enable `no_new_privs` where compatible.
- Apply a restrictive seccomp profile and available LSM policy.
- Use cgroup controls for CPU, memory, process count and IO where available.
- Make rootfs read-only by default with explicitly managed writable state.
- Make host mounts opt-in and constrain sources/targets.
- Restrict devices and network exposure.

Seccomp filters system calls and reduces exposed kernel surface; it is not a complete sandbox by itself.

## 6. Storage

Use an immutable rootfs payload plus a separate writable layer/state volume. Evaluate OverlayFS for native execution and SquashFS/EROFS for immutable payloads. Validate metadata behavior and support on every named kernel/distribution. Do not assume rootless OverlayFS is available everywhere.

## 7. Networking

Initially support isolated networking with explicit port publishing. A host-network mode is explicit and policy-gated. Image-declared exposed ports are metadata, not permission to bind host interfaces. Prefer loopback host binding by default and report address/interface selection.

## 8. Lifecycle

Support start/stop/restart/status/logs/health. Capture exit code, signal, OOM/cgroup failure where available and runtime errors. Distinguish workload failure from runtime failure.

## 9. Acceptance tests

- Generated OCI bundle passes selected runtime validation.
- Minimal BusyBox/Alpine-style fixture runs with correct argv/env/cwd.
- Whiteout and symlink fixtures preserve expected filesystem.
- Rootless path passes on named supported kernels.
- Capability, seccomp and mount defaults are visible and verified.
- Unauthorized host mount is rejected.
- Resource constraints are enforced where supported.
- Start/stop/restart/logs and exit reporting are stable.
