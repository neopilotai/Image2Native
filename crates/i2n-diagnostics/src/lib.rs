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
