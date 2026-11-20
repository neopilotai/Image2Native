# Windows Backend

## 1. Role

The initial Windows backend launches Linux OCI workloads through WSL2. The native Windows `.exe` is the launcher and lifecycle manager; the workload remains a Linux process inside the Linux guest. A later HCS backend may run Windows-native container images with Windows container semantics.

## 2. WSL2 Linux workload path

The backend should detect Windows build and architecture, check WSL2 and virtualization prerequisites, inspect guest/kernel version, provision or import a dedicated Image2Native-managed Linux environment, authenticate guest-agent identity/version, attach immutable payload, start the workload, and manage state, logs, ports and lifecycle.

Do not assume an arbitrary user WSL distribution is available or safe to modify. Prefer an isolated product-managed environment with user consent and documented storage location.

## 3. Windows-native images

A Windows image must never be sent to the Linux WSL2 backend. A future Windows-native backend should use HCS or supported Windows container APIs and validate host build, base-image compatibility, isolation mode and architecture. This is a separate milestone, not an automatic property of the Windows launcher.

## 4. Launcher

The `.exe` should perform preflight, artifact verification, install discovery, guest provisioning/start, workload invocation, log/status display and clean shutdown. Production release requires code signing. Do not embed registry credentials or runtime secrets.

## 5. Filesystem and paths

Linux paths remain POSIX paths inside the guest. Windows host paths enter only through explicit mount grants. Define path normalization and case-sensitivity behavior. Prevent traversal across mounts and do not expose an entire drive by default.

## 6. Networking

Use a supported WSL2 networking model and document behavior by Windows release. Define explicit port forwarding and firewall rules. Do not expose services on all interfaces by default. Surface selected network mode and prerequisites through `doctor` and `inspect`.

## 7. Future HCS backend

HCS exposes host compute lifecycle APIs for VMs and containers. The future backend must implement Windows image configuration, filesystem, process, networking and isolation semantics; it is not a generic execution shortcut.

## 8. Acceptance tests

- WSL2 detection and missing-prerequisite diagnostics.
- Managed guest provisioning/import lifecycle.
- Guest-agent identity and version checks.
- Windows launcher starts/stops a Linux workload.
- State persists according to explicit policy.
- Port forwarding/firewall behavior tested.
- Host/guest path isolation tests pass.
- WSL shutdown/restart and host reboot recovery.
- Signed installer/uninstaller and data-retention policy.
- HCS backend separately passes Windows-image tests before being called supported.
