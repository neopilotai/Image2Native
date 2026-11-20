# Platform Support Matrix

## 1. Support policy

Support is a tested statement, not an inference from Rust cross-compilation. Every stable support entry identifies host OS version, architecture, backend version, guest kernel/runtime version, workload source OS/architecture, limitations and test evidence.

## 2. Proposed target matrix

| Host | Workload | Backend | Design status |
|---|---|---|---|
| Linux x86_64 | Linux x86_64 | Host Linux OCI runtime | MVP target |
| Linux ARM64 | Linux ARM64 | Host Linux OCI runtime | Planned |
| macOS ARM64 | Linux ARM64 | Apple Virtualization + Linux guest | Planned |
| macOS x86_64 | Linux x86_64 | Apple Virtualization + Linux guest | Planned; validate supported host releases |
| Windows x86_64 | Linux x86_64 | WSL2 Linux guest | Planned |
| Windows ARM64 | Linux ARM64 | WSL2 Linux guest | Planned; validate each host/build combination |
| Windows x86_64 | Windows x86_64 | HCS / Windows containers | Future, separate backend |
| Windows ARM64 | Windows ARM64 | HCS / Windows containers | Future; compatibility validation required |
| macOS ARM64 | Linux x86_64 | VM + explicit CPU emulation | Experimental, not assumed |
| Linux x86_64 | Linux ARM64 | explicit QEMU/binfmt-style emulation | Experimental, not assumed |

These are proposed targets, not claims that every combination currently works. Unimplemented combinations must fail analysis rather than silently emulate or change backend.

## 3. Host execution principles

- Linux images require a compatible Linux kernel ABI; Linux host execution is the first-class route.
- macOS executes Linux workloads in a Linux guest via the host virtualization API.
- Windows executes Linux workloads in WSL2 or another supported Linux guest.
- Windows-native images require Windows container semantics and a separate backend.
- A native launcher does not change a workload's binary format or OS ABI.
- CPU architecture mismatch requires explicit emulation support and must be reported.

## 4. Support labels

`planned`, `experimental`, `supported`, `supported-with-warnings`, `unsupported`, `not-tested`. A `supported` claim requires integration evidence on named host releases.

## 5. Prerequisites to test

**Linux:** runtime version, user namespace/rootless support, cgroup v2/controllers, seccomp, mount/filesystem features and kernel support.

**macOS:** supported macOS release and architecture, Virtualization framework, entitlement/signing/distribution configuration, guest kernel and Virtio support, CPU/memory/storage.

**Windows:** Windows edition/build, WSL2 mode and kernel, virtualization features, host policy, filesystem/interoperability behavior, networking mode, and HCS availability for later backend.

## 6. Compatibility tests

For each stable cell test install, launch, stop/restart, logs, port forwarding, writable state, resource limits, update/rollback, uninstall, host reboot and tampered artifact. Test actual hosts or appropriate virtualized runners; cross-build success is not runtime proof.

## 7. Architecture/ABI policy

Track OCI architecture and variant, ELF machine and ABI evidence, guest kernel architecture, CPU features and emulation profile. For source compilation also record the target triple and toolchain support tier, then validate the resulting binary.
