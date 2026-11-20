# ADR 0001: OCI as the Primary Image Input Contract

- **Status:** Accepted as proposed baseline
- **Date:** 2026-11-20

## Context

The compiler needs interoperable registry and local image inputs. A proprietary image format would fragment the ecosystem and duplicate existing standards.

## Decision

Use the OCI Image Specification and OCI Distribution Specification as primary input contracts. Support Docker-compatible media types where required for interoperability, with explicit normalization and tests. Store resolved immutable descriptor digests in build records and artifacts.

## Consequences

- Track specification versions and accepted media types.
- Support multi-platform image indexes.
- Implement OCI layer/whiteout semantics.
- Normalize alternative inputs into one resolved-image model.
- I2N remains a separate project-owned artifact format.

## Alternatives

Docker CLI shell-out only was rejected because Docker Engine/CLI must not be a core dependency. A proprietary image format was rejected because it would reduce interoperability.
