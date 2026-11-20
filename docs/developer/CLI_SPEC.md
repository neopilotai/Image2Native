# CLI Specification

**Command:** `image2native` · **Optional alias:** `i2n`

## 1. UX principles

- Human-readable output by default; `--format json` for automation.
- Stable error codes, stage and remediation.
- Explicit `--target` for cross-platform packaging.
- `--backend auto` may select only an analyzed, policy-approved backend and must show why.
- Never silently elevate privileges or broaden filesystem/network access.
- `--help` and `--version` work offline.

## 2. Proposed command tree

```text
image2native
├── analyze <IMAGE>
├── compile <IMAGE>
├── build <CONTEXT>               # future source/Dockerfile feature
├── inspect <ARTIFACT|IMAGE>
├── verify <ARTIFACT>
├── install <ARTIFACT>
├── run <ARTIFACT|APP-ID>
├── stop <APP-ID|INSTANCE-ID>
├── status [APP-ID|INSTANCE-ID]
├── logs <APP-ID|INSTANCE-ID>
├── update <APP-ID> <ARTIFACT>
├── rollback <APP-ID>
├── uninstall <APP-ID>
├── doctor
├── cache {info,prune,verify}
├── sign <ARTIFACT>
└── publish <ARTIFACT>           # optional registry support
```

## 3. Common options

- `--target <os>-<arch>`
- `--backend <auto|native|apple-virtualization|wsl2|hcs>`
- `--output <PATH>`
- `--format <bundle|app|dmg|pkg|exe|msi|elf|archive>` (backend dependent)
- `--platform <os/arch[/variant]>`
- `--offline`, `--cache-dir <PATH>`, `--rootless`, `--reproducible`
- `--verify-source-signature`, `--require-signature`
- `--generate-sbom <spdx-json>`, `--provenance`
- `--format json`, `--quiet`, `--verbose`

Do not accept arbitrary shell command strings when argv arrays can be used. Validate path and option combinations before work begins.

## 4. Command behavior

**analyze:** resolve/inspect image, calculate compatibility and display backend plan; never execute the image.

**compile:** run the pipeline and require an output path. Resolve tags once and store selected immutable digest. Explain when reproducibility is not achievable.

**inspect:** display artifact identity, source, target, backend, payload, security and runtime metadata without running it.

**verify:** check all referenced digests and configured trust policy; do not install or execute.

**install:** verify first, stage atomically, register application and allocate separate writable state. No automatic privileged integration.

**run:** preflight policy/backend, start runtime or guest, launch workload and stream output. Separate application exit status from backend failure.

**doctor:** report OS/architecture, kernel/runtime versions, virtualization availability, prerequisites, storage and supported backend capabilities.

## 5. Workflow examples

Linux:

```bash
image2native analyze nginx:alpine --target linux-x86_64
image2native compile nginx:alpine \
  --target linux-x86_64 \
  --output ./dist/nginx.i2n \
  --generate-sbom spdx-json \
  --provenance
image2native verify ./dist/nginx.i2n
image2native install ./dist/nginx.i2n
image2native run org.example.nginx
image2native status org.example.nginx
image2native logs org.example.nginx
```

macOS Linux guest:

```bash
image2native compile nginx:alpine \
  --target macos-arm64 \
  --backend apple-virtualization \
  --format app \
  --output ./dist/Nginx.app
```

Windows Linux guest (PowerShell):

```powershell
image2native compile nginx:alpine `
  --target windows-x86_64 `
  --backend wsl2 `
  --output .\dist\nginx.exe
```

These examples describe proposed UX, not a currently available executable.

## 6. Proposed exit-code classes

| Code | Meaning |
|---:|---|
| 0 | Success |
| 2 | CLI argument/usage error |
| 10 | Image resolution/authentication failure |
| 11 | Digest/integrity failure |
| 12 | Malformed or unsupported image |
| 20 | Compatibility blocked |
| 21 | Host prerequisite missing |
| 30 | Artifact/signature verification failure |
| 40 | Backend/runtime failure |
| 50 | Application process returned non-zero, where distinguishable |

Lock exact values only after tests. Machine-readable errors should include `code`, `stage`, `message`, `details` and `remediation`.
