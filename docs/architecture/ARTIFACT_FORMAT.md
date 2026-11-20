# I2N Application Artifact Format

**Status:** proposed private format v0.1. It is not an OCI image format or finalized interoperability standard.

## 1. Goals

I2N is a portable, inspectable package describing an application payload and the backend required to execute it. It should support directory bundles, installer wrappers, integrity verification, signatures, SBOM, provenance, delta updates and rollback.

## 2. Proposed directory layout

```text
sample.i2n/
├── manifest.json
├── nir/native-image.json
├── plan/execution-plan.json
├── payload/rootfs.squashfs
├── payload/chunks/                 # optional content-addressed chunks
├── runtime/references.json
├── launcher/{icon,metadata.json}
├── security/{sbom.spdx.json,provenance.json,signature.bundle}
└── resources/defaults.json
```

Only target-required components ship. Guest/runtime components may be included or fetched as separately signed, digest-pinned dependencies.

## 3. Manifest requirements

The manifest includes format/version, application identity/version, source reference and immutable manifest digest, NIR schema/digest, target OS/architecture, backend ID/version, source workload OS/architecture/ABI, execution-plan digest, payload paths/media types/sizes/digests, runtime/guest identities, default resource/network/mount/state policies, SBOM/provenance references and signature policy.

## 4. Example manifest

```json
{
  "format": "i2n",
  "formatVersion": "0.1.0",
  "application": {"id": "org.example.nginx", "name": "Nginx", "version": "1.0.0"},
  "source": {
    "reference": "docker.io/library/nginx:alpine",
    "manifestDigest": "sha256:REPLACE_WITH_VERIFIED_DIGEST",
    "os": "linux", "architecture": "arm64"
  },
  "target": {"os": "macos", "architecture": "arm64", "backend": "apple-virtualization"},
  "nir": {"path": "nir/native-image.json", "schemaVersion": "0.1.0", "digest": "sha256:REPLACE_WITH_DIGEST"},
  "executionPlan": {"path": "plan/execution-plan.json", "digest": "sha256:REPLACE_WITH_DIGEST"},
  "payload": [{
    "path": "payload/rootfs.squashfs",
    "mediaType": "application/vnd.image2native.rootfs.squashfs",
    "size": 0,
    "digest": "sha256:REPLACE_WITH_DIGEST"
  }],
  "runtime": {"guestProfile": "linux-minimal-v1", "kernelDigest": "sha256:REPLACE_WITH_PINNED_DIGEST"},
  "security": {"sbom": "security/sbom.spdx.json", "provenance": "security/provenance.json", "signaturePolicy": "required"}
}
```

`REPLACE...` values are placeholders. Production validation rejects placeholders and missing required digests.

## 5. Canonical digest model

Define canonical manifest serialization and a payload digest graph. The artifact root digest commits to the canonical manifest (excluding self-referential signature fields) and every referenced payload digest. Publish a formal digest specification before format 1.0.

## 6. Signatures and attestations

Reuse an established ecosystem such as Sigstore where appropriate; do not invent cryptographic primitives or a trust model. Signature material must cover artifact identity and payload graph. Provenance binds source digest, compiler version, target, options and builder identity. Signing authenticates a signer under a policy; it does not prove software safety.

## 7. Mutable state separation

Never embed registry credentials, secrets, logs, user files, database state or runtime caches in the immutable application payload. Mutable application data lives in a separate managed state directory/volume. Uninstall must follow an explicit retain/delete policy.

## 8. Filesystem and compression choice

Evaluate SquashFS and EROFS for Linux guest payloads based on metadata compatibility, guest kernel support, random access, read performance, compression and license obligations. The guest mounts Linux filesystems; the host need not mount them.

## 9. Delta updates

A delta references old and new artifact root digests. Each chunk is independently hashed. Stage the update, verify the whole resulting artifact, then atomically switch the active version. Keep the prior known-good version until health verification passes. Rollback must not reverse trust revocations or security policy.

## 10. Compatibility rules

- Unknown major version: reject.
- Unknown required feature: reject.
- Unknown optional metadata: preserve where safe.
- Missing payload or digest mismatch: reject.
- Required but absent/untrusted signature: reject.
- Unavailable backend: fail preflight or fetch an independently verified compatible runtime according to policy.
