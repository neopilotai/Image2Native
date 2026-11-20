# ADR 0002: Use a Versioned Native Image Representation

- **Status:** Accepted as proposed baseline
- **Date:** 2026-11-20

## Context

OCI metadata and layers need to be translated into several backends. Direct translation from OCI parser types to native platform APIs would couple core compilation to both input schemas and host SDKs.

## Decision

Introduce a canonical, versioned NIR between filesystem reconstruction/inspection and backend planning/linking. NIR preserves source facts and records derived findings separately. It does not replace OCI standards.

## Consequences

- NIR requires schema governance, canonicalization and migration tests.
- Unknown required features fail closed.
- Platform SDK handles remain outside NIR.
- The same NIR can be re-analyzed as backend capabilities evolve.

## Alternatives

Direct OCI-to-platform translation was rejected due to tight coupling. Using raw OCI config as the IR was rejected because it does not capture rootfs identity, compiler findings or target execution plans.
