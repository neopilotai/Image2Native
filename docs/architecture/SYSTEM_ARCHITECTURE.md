# System Architecture

## 1. Overview

Image2Native is divided into a host-independent compiler core, platform-specific packaging/runtime backends, native launchers and optional lifecycle services.

```text
                USER / CI / LOCAL TOOL
                         |
              CLI / native launcher / API
                         |
               Compiler orchestration
                         |
     +-------------------v--------------------+
     |          HOST-INDEPENDENT CORE         |
     |                                        |
     | OCI resolver -> fetcher -> digest/cache|
     | layer engine -> rootfs -> inspector   |
     | NIR compiler -> compatibility analyzer|
     | artifact linker -> SBOM/provenance     |
     +-------------------+--------------------+
                         |
                  Backend plan + I2N
                         |
       +-----------------+------------------+
       |                 |                  |
    Linux host       macOS host         Windows host
    OCI runtime      Virtualization     WSL2 / future HCS
    namespaces       Linux guest        Linux guest / Windows
    cgroups/seccomp  guest agent        native container path
```

## 2. Boundaries

### Input boundary
The resolver accepts registry references and local OCI layouts. It owns protocol concerns. The compiler records immutable content identity and never treats a tag as final source identity.

### Content boundary
Blob bytes are keyed by digest. The cache is an optimization, not a source of truth. Cache metadata must be reconstructible from verified content.

### Filesystem boundary
Layer application produces a logical rootfs model. Host extraction is merely an implementation detail; it must not let host filesystem semantics corrupt source Linux metadata.

### IR boundary
NIR is the stable contract between compiler stages and backends. Platform SDK types must never appear in NIR.

### Backend boundary
Each backend reports capabilities and prerequisites. Backend selection follows analysis and policy evaluation; no backend silently drops unsupported requirements.

### Artifact boundary
I2N is immutable build output. Credentials, runtime secrets, logs, user files and mutable app data are stored separately.

## 3. Component ownership

| Component | Owns | Must not own |
|---|---|---|
| Resolver | reference parsing, auth challenge, manifest resolution | rootfs extraction |
| Fetcher | blob transfer, retry, cancellation | platform execution |
| Cache | verified immutable blobs | source tag truth |
| Layer engine | compressed layer parsing and changesets | host process launch |
| RootFS | path tree and metadata semantics | registry protocol |
| Inspector | static image/config analysis | arbitrary code execution |
| NIR compiler | canonical app model | platform framework calls |
| Analyzer | requirements and target compatibility | silent overrides |
| Linker | artifact layout/digests/metadata | secrets and mutable state |
| Runtime manager | install/lifecycle state | registry auth |
| Backend | host-specific integration | OCI parsing |

## 4. Build, install and run responsibilities

**Build:** resolve and verify source; reconstruct filesystem; normalize config; analyze compatibility; select backend profile; create I2N; generate SBOM/provenance; optionally sign.

**Install:** verify signature and policy; stage immutable payload; allocate writable state; register app metadata; provision a guest/runtime only with required consent.

**Run:** preflight backend; start guest/runtime; attach payload; apply port/mount policy; start workload; report logs, health and exit state.

## 5. State model

```text
UNRESOLVED -> RESOLVED -> FETCHED -> VERIFIED
 -> ROOTFS_READY -> NIR_READY -> ANALYZED -> PLANNED
 -> LINKED -> SIGNED -> INSTALLED -> STARTING -> RUNNING
 -> STOPPING -> STOPPED / FAILED
 -> UPDATED / ROLLED_BACK / UNINSTALLED
```

Build state and runtime state are separate. Launching an application must not mutate its signed build artifact. Guest state and application process state must be independently observable.

## 6. Identifiers

- `ImageReference`: user-supplied name/tag/digest.
- `ResolvedImage`: selected immutable manifest descriptor and platform.
- `BlobDigest`: digest algorithm and value.
- `RootFsId`: digest of ordered layer inputs and normalized rootfs semantics.
- `NirId`: digest of canonical NIR plus schema version.
- `ArtifactId`: digest of canonical manifest and payload graph.
- `InstallId`: local installation identity.
- `InstanceId`: one execution instance.

Never conflate application name, content digest, installation ID or process ID.

## 7. Extensibility

New input adapters produce the same resolved-image model. New backends implement shared capability and lifecycle contracts. Output package formats consume the linker model rather than reimplementing OCI parsing. Source compilers generate a separate source-build record and native binary payload.

## 8. Failure and recovery

Stages should be restartable from verified checkpoints. Incomplete downloads are never promoted to verified cache objects. Layer application and artifact writing use temporary outputs and atomic commit where supported. Runtime recovery distinguishes app process failure, guest failure, host prerequisite failure and artifact corruption.
