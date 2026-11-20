//! Native Image Representation (NIR) v0.1 draft types.

use i2n_model::{Digest, TargetPlatform};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ImageIdentity {
    pub source_reference: String,
    pub manifest_digest: Digest,
}

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct ProcessSpec {
    pub entrypoint: Vec<String>,
    pub arguments: Vec<String>,
    pub working_directory: Option<String>,
    pub user: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NativeImage {
    pub identity: ImageIdentity,
    pub source_platform: String,
    pub requested_target: TargetPlatform,
    pub process: ProcessSpec,
}
