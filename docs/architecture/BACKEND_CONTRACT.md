# Platform Backend Contract

## 1. Purpose

A backend converts NIR plus an execution plan into a target-specific package and provides install/run lifecycle operations. It does not resolve registries, parse image layers or invent semantics absent from the compiler model.

## 2. Backend descriptor

Every backend reports stable ID/version, host OS/architecture, supported source OS/architecture/ABI, runtime and guest versions, capabilities, limitations, privileges/entitlements/prerequisites and artifact formats.

## 3. Capability model

Use at least `supported`, `unsupported`, `conditional` and `unknown`. Unknown is never treated as supported. Capability families include CPU/emulation, OS/ABI, filesystem metadata, process/signal behavior, user mapping, networking, mount modes, devices, resource controls, guest lifecycle and security isolation.

## 4. Conceptual Rust interface

```rust
#[async_trait::async_trait]
pub trait PlatformBackend: Send + Sync {
    fn descriptor(&self) -> BackendDescriptor;
    async fn preflight(&self, plan: &ExecutionPlan, host: &HostDescriptor)
        -> Result<PreflightReport>;
    async fn package(&self, input: &BackendPackageInput, output: &ArtifactOutput)
        -> Result<BackendPackageResult>;
    async fn install(&self, artifact: &VerifiedArtifact, options: &InstallOptions)
        -> Result<InstallReceipt>;
    async fn start(&self, install: &InstallReceipt, options: &RunOptions)
        -> Result<InstanceHandle>;
    async fn stop(&self, instance: &InstanceHandle, mode: StopMode) -> Result<()>;
    async fn status(&self, instance: &InstanceHandle) -> Result<InstanceStatus>;
    async fn logs(&self, instance: &InstanceHandle, cursor: Option<LogCursor>)
        -> Result<LogPage>;
    async fn uninstall(&self, install: &InstallReceipt, policy: &UninstallPolicy)
        -> Result<()>;
}
```

Conceptual API only. Finalize lifetimes, async trait strategy and object safety when runtime orchestration is selected. Keep native SDK handles backend-private.

## 5. Execution plan

Pin backend ID/version, NIR digest, payload digest, guest/kernel identity, resource defaults, network policy, mount policy, security profile, required host features and compatibility findings. Signed plans are immutable. Runtime overrides are recorded separately and checked against policy.

## 6. Backend selection algorithm

1. Read source OS and architecture.
2. Read host OS and architecture.
3. Filter backends by supported source/host pair.
4. Check host prerequisites.
5. Evaluate workload requirements.
6. Apply security policy and user preference.
7. Return one backend with rationale, or fail with actionable findings.

Automatic fallback must never broaden privileges, expose host paths or weaken isolation without explicit user consent.

## 7. Lifecycle

`Absent -> Installed -> Starting -> Running -> Stopping -> Stopped`; failure enters `Failed` with cause and recoverability. Guest state and application process state must be separately observable.

## 8. Conformance suite

Every backend must pass common tests for verification, idempotent install, start/stop, crash reporting, logs, port policy, state retention, update/rollback, uninstall and tampered-artifact rejection. Platform tests cover entitlements, guest boot, VM lifecycle, service management and OS upgrade compatibility.
