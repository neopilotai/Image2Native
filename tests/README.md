# Test Strategy

- `unit/`: domain, parsing, canonicalization and stage tests.
- `fixtures/`: pinned OCI layouts and hostile/adversarial archives.
- `integration/`: end-to-end compile and runtime flows.
- `compatibility/`: image × target × backend support matrix.
- `security/`: archive, registry, isolation, secrets and update tests.
- `golden/`: NIR, RootFS and artifact deterministic outputs.

Do not check in credentials or live mutable tags as golden inputs. Fixtures should be digest-pinned and license-reviewed.
