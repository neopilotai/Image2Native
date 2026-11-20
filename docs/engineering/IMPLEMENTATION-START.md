# Implementation Start: First Implementation-Ready Task

**Generated:** 2026-11-20  
**Git commit:** f42f10a  
**Git branch:** main  

This document identifies the first concrete, implementation-ready task for Image2Native.

## First Implementation Task

### Task ID: I2N-0202

**Name:** Define structured diagnostic codes and error policy

**Current Status:** todo

**Priority:** P1

**Phase:** 2

**Owner:** foundation

**Boundary:** i2n-diagnostics

## Objective

Implement a structured diagnostic system with stable error codes, stage identifiers, retryability flags, secret redaction, and remediation hints. This is a foundational component that all other compiler stages will depend on for consistent error reporting.

## Existing Code

**File:** crates/i2n-diagnostics/src/lib.rs (51 lines)

**Current implementation:**
```rust
//! Structured diagnostics shared across compiler stages.

use core::fmt;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Stage {
    Resolve,
    Fetch,
    Decode,
    Rootfs,
    Normalize,
    Analyze,
    Plan,
    Link,
    Verify,
    Run,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    pub code: &'static str,
    pub stage: Stage,
    pub message: String,
    pub retryable: bool,
    pub remediation: Option<String>,
}

impl Diagnostic {
    pub fn new(code: &'static str, stage: Stage, message: impl Into<String>) -> Self {
        Self {
            code,
            stage,
            message: message.into(),
            retryable: false,
            remediation: None,
        }
    }

    pub fn with_remediation(mut self, remediation: impl Into<String>) -> Self {
        self.remediation = Some(remediation.into());
        self
    }
}

impl fmt::Display for Diagnostic {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {}", self.code, self.message)
    }
}

impl std::error::Error for Diagnostic {}
```

**Status:** Basic Stage enum and Diagnostic struct exist, but missing:
- Stable error code definitions
- Code validation
- Secret redaction logic
- Structured error categories
- Context/field path tracking
- Confidence levels
- Error conversion helpers

## Required Changes

### 1. Define Error Code Registry

**File:** crates/i2n-diagnostics/src/lib.rs

**Add:**
```rust
/// Error code registry. All codes must be stable and documented.
/// Format: <STAGE>_<CATEGORY>_<SPECIFIC>
/// Example: RESOLVE_AUTH_FAILED, FETCH_DIGEST_MISMATCH
pub mod codes {
    // Resolve stage errors
    pub const RESOLVE_INVALID_REFERENCE: &str = "RESOLVE_INVALID_REFERENCE";
    pub const RESOLVE_AUTH_FAILED: &str = "RESOLVE_AUTH_FAILED";
    pub const RESOLVE_NO_PLATFORM: &str = "RESOLVE_NO_PLATFORM";
    pub const RESOLVE_REGISTRY_UNAVAILABLE: &str = "RESOLVE_REGISTRY_UNAVAILABLE";

    // Fetch stage errors
    pub const FETCH_DIGEST_MISMATCH: &str = "FETCH_DIGEST_MISMATCH";
    pub const FETCH_SIZE_MISMATCH: &str = "FETCH_SIZE_MISMATCH";
    pub const FETCH_NETWORK_ERROR: &str = "FETCH_NETWORK_ERROR";
    pub const FETCH_CANCELLED: &str = "FETCH_CANCELLED";

    // Decode stage errors
    pub const DECODE_UNSUPPORTED_CODEC: &str = "DECODE_UNSUPPORTED_CODEC";
    pub const DECODE_CORRUPT_ARCHIVE: &str = "DECODE_CORRUPT_ARCHIVE";
    pub const DECODE_QUOTA_EXCEEDED: &str = "DECODE_QUOTA_EXCEEDED";

    // RootFS stage errors
    pub const ROOTFS_PATH_TRAVERSAL: &str = "ROOTFS_PATH_TRAVERSAL";
    pub const ROOTFS_INVALID_WHITEOUT: &str = "ROOTFS_INVALID_WHITEOUT";
    pub const ROOTFS_CONFLICTING_ENTRY: &str = "ROOTFS_CONFLICTING_ENTRY";

    // Normalize stage errors
    pub const NORMALIZE_INVALID_CONFIG: &str = "NORMALIZE_INVALID_CONFIG";
    pub const NORMALIZE_UNKNOWN_REQUIRED: &str = "NORMALIZE_UNKNOWN_REQUIRED";

    // Analyze stage errors
    pub const ANALYZE_UNSUPPORTED_ABI: &str = "ANALYZE_UNSUPPORTED_ABI";
    pub const ANALYZE_KERNEL_REQUIREMENT: &str = "ANALYZE_KERNEL_REQUIREMENT";
    pub const ANALYZE_PRIVILEGE_REQUIRED: &str = "ANALYZE_PRIVILEGE_REQUIRED";

    // Plan stage errors
    pub const PLAN_NO_ELIGIBLE_BACKEND: &str = "PLAN_NO_ELIGIBLE_BACKEND";
    pub const PLAN_UNSUPPORTED_REQUIREMENT: &str = "PLAN_UNSUPPORTED_REQUIREMENT";

    // Link stage errors
    pub const LINK_MANIFEST_FAILURE: &str = "LINK_MANIFEST_FAILURE";
    pub const LINK_PAYLOAD_FAILURE: &str = "LINK_PAYLOAD_FAILURE";

    // Verify stage errors
    pub const VERIFY_SIGNATURE_FAILED: &str = "VERIFY_SIGNATURE_FAILED";
    pub const VERIFY_DIGEST_FAILED: &str = "VERIFY_DIGEST_FAILED";

    // Run stage errors
    pub const RUN_PREREQUISITE_FAILED: &str = "RUN_PREREQUISITE_FAILED";
    pub const RUN_BACKEND_FAILED: &str = "RUN_BACKEND_FAILED";
}
```

### 2. Enhance Diagnostic Struct

**File:** crates/i2n-diagnostics/src/lib.rs

**Replace existing Diagnostic struct with:**
```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Diagnostic {
    /// Stable error code from the codes module
    pub code: &'static str,
    /// Compiler stage where the error occurred
    pub stage: Stage,
    /// Human-readable error message (secrets redacted)
    pub message: String,
    /// Whether the operation can be retried
    pub retryable: bool,
    /// Suggested remediation steps
    pub remediation: Option<String>,
    /// Field path or context for structured errors
    pub context: Option<String>,
    /// Confidence in the diagnosis (low/medium/high)
    pub confidence: Confidence,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Confidence {
    Low,
    Medium,
    High,
}
```

### 3. Add Secret Redaction

**File:** crates/i2n-diagnostics/src/lib.rs

**Add:**
```rust
/// Redact sensitive values from error messages.
/// Replaces common secret patterns with [REDACTED].
pub fn redact_secrets(message: impl AsRef<str>) -> String {
    let msg = message.as_ref();
    let redacted = msg
        // Redact bearer tokens
        .replace(|c: char| c.is_ascii_uppercase() && c.is_ascii_alphabetic(), |c: &str| {
            if msg.contains("bearer") || msg.contains("token") || msg.contains("secret") {
                "[REDACTED]"
            } else {
                c
            }
        })
        // Redact potential credential-like patterns
        .replace(|s: &str| {
            s.chars().all(|c| c.is_ascii_hexdigit() || c == '-' || c == '_') && s.len() >= 32
        }, "[REDACTED]");
    
    redacted.to_string()
}

/// Safe message constructor that redacts secrets.
pub fn safe_message(code: &'static str, stage: Stage, message: impl AsRef<str>) -> String {
    format!("{} [{}]: {}", code, stage, redact_secrets(message))
}
```

### 4. Add Error Builder

**File:** crates/i2n-diagnostics/src/lib.rs

**Add:**
```rust
impl Diagnostic {
    /// Create a new diagnostic with automatic secret redaction.
    pub fn builder(code: &'static str, stage: Stage) -> DiagnosticBuilder {
        DiagnosticBuilder {
            code,
            stage,
            message: String::new(),
            retryable: false,
            remediation: None,
            context: None,
            confidence: Confidence::High,
        }
    }
}

pub struct DiagnosticBuilder {
    code: &'static str,
    stage: Stage,
    message: String,
    retryable: bool,
    remediation: Option<String>,
    context: Option<String>,
    confidence: Confidence,
}

impl DiagnosticBuilder {
    pub fn message(mut self, message: impl AsRef<str>) -> Self {
        self.message = redact_secrets(message);
        self
    }

    pub fn retryable(mut self, retryable: bool) -> Self {
        self.retryable = retryable;
        self
    }

    pub fn remediation(mut self, remediation: impl Into<String>) -> Self {
        self.remediation = Some(remediation.into());
        self
    }

    pub fn context(mut self, context: impl Into<String>) -> Self {
        self.context = Some(context.into());
        self
    }

    pub fn confidence(mut self, confidence: Confidence) -> Self {
        self.confidence = confidence;
        self
    }

    pub fn build(self) -> Diagnostic {
        Diagnostic {
            code: self.code,
            stage: self.stage,
            message: self.message,
            retryable: self.retryable,
            remediation: self.remediation,
            context: self.context,
            confidence: self.confidence,
        }
    }
}
```

### 5. Add Tests

**File:** crates/i2n-diagnostics/src/lib.rs

**Add test module:**
```rust
#[cfg(test)]
mod tests {
    use super::*;
    use crate::codes::*;

    #[test]
    fn diagnostic_builder_creates_valid_diagnostic() {
        let diag = Diagnostic::builder(FETCH_DIGEST_MISMATCH, Stage::Fetch)
            .message("Digest abc123 does not match expected def456")
            .retryable(false)
            .remediation("Verify the image digest and try again")
            .context("blob:sha256:abc123")
            .confidence(Confidence::High)
            .build();

        assert_eq!(diag.code, FETCH_DIGEST_MISMATCH);
        assert_eq!(diag.stage, Stage::Fetch);
        assert!(!diag.retryable);
        assert_eq!(diag.remediation, Some("Verify the image digest and try again".to_string()));
        assert_eq!(diag.context, Some("blob:sha256:abc123".to_string()));
    }

    #[test]
    fn redact_secrets_removes_bearer_tokens() {
        let msg = "Authentication failed: bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9";
        let redacted = redact_secrets(msg);
        assert!(redacted.contains("[REDACTED]"));
        assert!(!redacted.contains("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"));
    }

    #[test]
    fn redact_secrets_preserves_safe_messages() {
        let msg = "File not found: /tmp/image.tar";
        let redacted = redact_secrets(msg);
        assert_eq!(redacted, msg);
    }

    #[test]
    fn all_codes_are_well_formed() {
        // Ensure all codes follow pattern: STAGE_CATEGORY_SPECIFIC
        let codes = [
            RESOLVE_INVALID_REFERENCE,
            RESOLVE_AUTH_FAILED,
            FETCH_DIGEST_MISMATCH,
            DECODE_UNSUPPORTED_CODEC,
            ROOTFS_PATH_TRAVERSAL,
            NORMALIZE_INVALID_CONFIG,
            ANALYZE_UNSUPPORTED_ABI,
            PLAN_NO_ELIGIBLE_BACKEND,
            LINK_MANIFEST_FAILURE,
            VERIFY_SIGNATURE_FAILED,
            RUN_PREREQUISITE_FAILED,
        ];

        for code in codes {
            let parts: Vec<&str> = code.split('_').collect();
            assert!(parts.len() >= 2, "Code {} must have at least 2 parts", code);
            assert!(parts[0].chars().all(|c| c.is_ascii_uppercase()), "Code {} must be uppercase", code);
        }
    }
}
```

### 6. Update README

**File:** crates/i2n-diagnostics/README.md

**Update with:**
```markdown
# i2n-diagnostics

Structured diagnostics shared across compiler stages.

## Purpose

Provides stable error codes, stage identifiers, retryability flags, secret redaction, and remediation hints for consistent error reporting across all compiler stages.

## Public API

- `Stage` enum: Compiler stage identifiers
- `Diagnostic` struct: Error information with code, stage, message, retryability, remediation, context, confidence
- `codes` module: Stable error code registry
- `redact_secrets()`: Secret redaction utility
- `DiagnosticBuilder`: Fluent API for constructing diagnostics

## Usage

```rust
use i2n_diagnostics::{Diagnostic, Stage, codes::FETCH_DIGEST_MISMATCH, Confidence};

let diag = Diagnostic::builder(FETCH_DIGEST_MISMATCH, Stage::Fetch)
    .message("Digest does not match")
    .retryable(false)
    .remediation("Verify the image digest")
    .confidence(Confidence::High)
    .build();
```

## Error Code Format

Error codes follow the pattern: `<STAGE>_<CATEGORY>_<SPECIFIC>`

Examples:
- `RESOLVE_AUTH_FAILED`: Resolve stage, authentication failure
- `FETCH_DIGEST_MISMATCH`: Fetch stage, digest verification failure
- `ROOTFS_PATH_TRAVERSAL`: RootFS stage, path traversal attempt

## Secret Redaction

All error messages are automatically redacted to prevent secrets from appearing in logs. The `redact_secrets()` function replaces:
- Bearer tokens
- API keys
- Long hex strings that may be credentials

## Status

PARTIAL: Basic Stage and Diagnostic exist. Error codes, secret redaction, and builder pattern are pending implementation.
```

## Dependencies

**Prerequisite task IDs:**
- I2N-0002: Create Rust workspace and crate scaffold (DONE)

**Allowed dependency groups:**
- None (foundation crate with no dependencies per boundaries.json)

**Actual dependencies:**
- None (currently no dependencies in Cargo.toml)

## Public API Impact

**Changes:**
- Add `codes` module with stable error code constants
- Enhance `Diagnostic` struct with `context` and `confidence` fields
- Add `Confidence` enum
- Add `redact_secrets()` function
- Add `DiagnosticBuilder` type
- Add `safe_message()` function

**Breaking changes:** None (additive only)

**Dependent crates:** None currently, but will be used by all compiler stages as they are implemented.

## Boundary Impact

**Boundary:** i2n-diagnostics (foundation group)

**Allowed dependency groups:** None (foundation crate is a leaf)

**Impact:** No dependency changes required. This crate remains a leaf in the dependency graph.

## Testing Requirements

### Unit Tests

1. **Error code validation:** Test that all codes follow the STAGE_CATEGORY_SPECIFIC pattern
2. **Secret redaction:** Test that bearer tokens, API keys, and credential-like strings are redacted
3. **Safe message preservation:** Test that safe messages are not modified
4. **Diagnostic builder:** Test fluent API constructs valid diagnostics
5. **Display formatting:** Test that Diagnostic displays correctly
6. **Error conversion:** Test that Diagnostic implements std::error::Error correctly

### Negative Tests

1. **Invalid code format:** Test that malformed codes are rejected (if validation is added)
2. **Empty messages:** Test behavior with empty message strings
3. **Remediation without message:** Test behavior when remediation is provided but message is empty

### Integration Tests

None required for this task (no dependencies on other crates).

## Acceptance Criteria

1. ✅ Error code registry with at least 30 stable codes covering all stages
2. ✅ All codes follow STAGE_CATEGORY_SPECIFIC pattern
3. ✅ Secret redaction function removes bearer tokens and credential-like strings
4. ✅ Safe messages are preserved without modification
5. ✅ DiagnosticBuilder provides fluent API for constructing diagnostics
6. ✅ Diagnostic struct includes context and confidence fields
7. ✅ Unit tests achieve >90% coverage
8. ✅ cargo clippy passes with -D warnings
9. ✅ cargo fmt passes with --check
10. ✅ README.md updated with usage examples
11. ✅ Evidence recorded in project/work-items.json

## Risks

### Low Risk

1. **Secret redaction over-redaction:** May redact legitimate error messages
   - **Mitigation:** Conservative redaction patterns; add allowlist for safe patterns
   - **Fallback:** Manual review of redacted messages in tests

2. **Code registry bloat:** Too many codes may become unmanageable
   - **Mitigation:** Start with essential codes; add as needed
   - **Fallback:** Group codes by stage in documentation

## Estimated Complexity

**S (Small)** - 1-2 days

**Justification:**
- Isolated crate with no dependencies
- Well-defined scope (error codes, redaction, builder)
- No integration with other crates required
- Pure logic with clear test cases

## Ready to Implement

**YES**

This task is ready to implement because:
1. ✅ All prerequisites satisfied (I2N-0002 is done)
2. ✅ No dependency on other crates
3. ✅ Clear acceptance criteria
4. ✅ Isolated scope (foundation leaf crate)
5. ✅ Test strategy is straightforward
6. ✅ No architectural decisions required
7. ✅ No external dependencies needed

## Next Steps After This Task

After completing I2N-0202, the next implementation-ready task is:

**I2N-0201: Finalize domain IDs, digest and target platform model**
- Depends on: I2N-0002 (done)
- Status: in_progress (basic types exist, need completion)
- Complexity: M

## How to Verify Completion

1. Run unit tests: `cargo test -p i2n-diagnostics`
2. Run clippy: `cargo clippy -p i2n-diagnostics -- -D warnings`
3. Run fmt check: `cargo fmt -p i2n-diagnostics -- --check`
4. Update project/work-items.json:
   ```json
   {
     "id": "I2N-0202",
     "status": "done",
     "evidence": [
       "crates/i2n-diagnostics/src/lib.rs",
       "crates/i2n-diagnostics/README.md"
     ]
   }
   ```
5. Regenerate TODO.md: `python3 scripts/i2n.py checklist --write`
6. Run validation: `python3 scripts/i2n.py validate`

## Evidence Collection

After implementation, record evidence in project/work-items.json:

```json
{
  "id": "I2N-0202",
  "evidence": [
    "crates/i2n-diagnostics/src/lib.rs",
    "crates/i2n-diagnostics/README.md",
    "tests/unit/diagnostics_test.rs"  // if tests are in separate file
  ]
}
```

---

**Ready to start implementation.** No blockers, no dependencies, clear acceptance criteria.
