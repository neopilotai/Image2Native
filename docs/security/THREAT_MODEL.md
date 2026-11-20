# Threat Model

**Method:** assets, actors, attack surfaces, abuse cases, mitigations and residual risk. This model must evolve with implementation.

## 1. Assets

Registry credentials; host files/user data; host kernel and runtime; guest kernel and agent; source image bytes/digests; I2N artifacts/signatures/provenance; runtime secrets and app state; update trust roots and installed app identity.

## 2. Threat actors

Malicious image publisher; compromised registry/network intermediary; compromised dependency in an image; local unprivileged user attempting cross-user access; malicious workload; compromised builder/release signer; attacker replacing or downgrading an update.

## 3. Attack surface and controls

| Surface | Abuse case | Mitigation | Residual risk |
|---|---|---|---|
| Registry metadata | oversized/deep manifest or malicious media type | parser limits, allowlist, typed validation | parser defects remain possible |
| Blob download | substitution or truncation | streaming hash, expected size, atomic cache promotion | hash implementation risk |
| Layer archive | path traversal/link escape | logical root, link policy, fuzzing | filesystem semantic edge cases |
| Decompression | resource exhaustion | expanded-size/time/file quotas | configured quota exhaustion |
| NIR parser | crafted schema data | size/depth limits, schema validation, fuzzing | parser defects |
| Artifact reader | path traversal/payload swap | digest graph, safe extraction, signature check | signer/key compromise |
| Linux runtime | escape/overprivilege | mature runtime, rootless, namespaces, caps, seccomp, LSM, patching | shared-kernel attack surface |
| Guest integration | malicious guest agent/VM escape | signed guest, narrow channels, host API review, patching | hypervisor/framework defects |
| Host mounts | workload reads/modifies host data | explicit narrow grants, read-only default | authorized paths remain exposed |
| Network | unexpected service exposure | loopback default, explicit forwarding, firewall policy | host-specific networking differences |
| Secrets | secrets copied into artifacts/logs | sensitivity labels, redaction, runtime injection | secret may already exist in an image layer |
| Update | tampered/downgrade package | signature policy, monotonic version policy, staged update | signer compromise/revocation delay |
| Build supply chain | compromised compiler/toolchain | pinned dependencies, isolated builder, provenance, signed release | upstream compromise |

## 4. Assumptions

- Host OS/kernel/hypervisor is not already compromised.
- Cryptographic libraries and hash/signature primitives are correctly implemented.
- User consent for mounts and network exposure is enforced.
- Registry popularity does not establish trust.
- Content digest proves identity, not safety or publisher identity.

## 5. High-risk decisions

**Host extraction:** writing untrusted archive entries directly into host filesystem is high risk. Prefer a logical filesystem and constrained staging area.

**Privileged helpers:** rootless is default. A helper requires a separate ADR, security review and narrowly scoped API.

**Guest agent:** authenticate peer identity, version the protocol, validate every message, restrict operations and never expose arbitrary host command execution.

**Artifact trust:** protect signing keys from build workers and verify release outputs independently.

## 6. Security testing

Fuzz registry/image config parsers, archive decoder, whiteout engine, NIR parser, I2N reader and guest-agent protocol. Test path/link permutations, quotas, digest mismatch, wrong media types, privilege profiles, host mount restrictions, guest messages, signature mismatch, revoked identity and downgrade. Complete an independent security review before 1.0.

## 7. Incident response

Before public release, publish a security contact and coordinated disclosure process. Define severity, supported versions, patch process, artifact revocation, guest runtime update policy and notification. Maintain a playbook for compromised signing identities and vulnerable guest kernels.
