# Build, Test and Quality Strategy

## 1. Development prerequisites

Pin minimum Rust version in `rust-toolchain.toml` after the first workspace build. Platform work requires Xcode/SDK tools for macOS bridge code, Windows SDK and WSL features for Windows integration, and Linux runtime/kernel dependencies for backend tests.

## 2. Local checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo build --workspace
```

CI should additionally run schema validation, markdown/link checks, license audit, dependency vulnerability audit and architecture dependency tests.

## 3. Test layers

- **Unit:** reference parsing, descriptor validation, digests, path normalization, whiteouts, NIR canonicalization, compatibility rules, manifest validation and lifecycle state machine.
- **Golden:** pinned OCI fixtures produce expected descriptor graph, rootfs tree, metadata, canonical NIR and compatibility report.
- **Conformance:** test behaviors against pinned OCI image/distribution/runtime specification versions.
- **Integration:** local registry, OCI layout, selected runtime, artifact install/verify/update, guest-agent channel.
- **End-to-end:** compile and execute representative images on real Linux/macOS/Windows targets. Cross-compilation alone does not establish runtime support.
- **Security:** fuzz parser/extractor; test hostile archives, oversized metadata, corrupt digest, symlink escape, signature failure, privilege policy and malformed guest messages.
- **Performance:** record download throughput, cache hit ratio, decompression rate, peak memory, rootfs build, artifact size, startup and guest boot latency, and update bytes.

## 4. Fixture catalogue

- Minimal BusyBox/Alpine-style image: process, argv and filesystem.
- Nginx-style server: long-running process, ports and signal handling.
- Node.js and Python: interpreters and dynamic dependencies.
- Redis/PostgreSQL-style service: persistence and shared memory.
- Debian/Ubuntu-style base: broader userspace diversity.
- Malformed fixtures: bad descriptor, invalid layer, whiteout edge case, traversal and digest mismatch.

Pin every fixture digest. Never use a floating tag as a golden test input.

## 5. CI matrix

| Runner | Coverage |
|---|---|
| Linux x86_64 | Core, tests and Linux runtime |
| Linux ARM64 | Architecture and runtime |
| macOS ARM64 | Virtualization integration |
| macOS x86_64 | Intel Mac backend, where supported |
| Windows x86_64 | WSL2 and launcher |
| Windows ARM64 | ARM64 launcher/guest, when supported |
| Cross-target jobs | Compile launchers for declared Rust targets |
| Security jobs | Fuzz smoke tests, dependency audit, static analysis |
| Reproducibility job | Compare payload roots from clean rebuilds |

## 6. Quality gates

No unexplained warning suppression; no unsafe block without localized safety comment and tests; no unbounded untrusted allocation; no panic on malformed input; no secrets in logs; no platform SDK dependency in domain crates; no release without artifact verification and backend compatibility evidence.

## 7. Benchmark method

Record host model, CPU architecture, OS/kernel, storage, memory, tool versions, image digest, cache state, concurrency and signing inclusion. Report cold and warm cache separately. Do not compare different security profiles as equivalent.
