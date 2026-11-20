# Security Policy

Image2Native processes untrusted OCI images and executable workloads. Treat image input, archive metadata, registry responses, guest images and application artifacts as hostile until verified.

## Reporting

Do not open public issues for exploitable vulnerabilities. Until a private security contact is configured, repository maintainers must add a private reporting channel before publishing production binaries. The project is not yet production-ready.

## Security invariants

- Verify OCI manifest and blob digests before use.
- Bound downloads, decompression, file counts, path depth and extracted size.
- Reject unsafe paths, escaping symlinks and invalid whiteout behavior.
- Do not silently grant privileges or host mounts.
- Keep secrets out of image layers, artifacts, logs and diagnostics.
- Use isolated execution backends and least-privilege defaults.
- Verify artifact signatures and update provenance according to policy.
