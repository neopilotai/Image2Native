//! Platform backend contracts. Implementations live in separate platform crates.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExecutionKind {
    NativeLinux,
    LinuxVirtualMachine,
    WindowsContainer,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BackendCapabilities {
    pub backend_id: &'static str,
    pub execution_kind: ExecutionKind,
    pub supports_linux_images: bool,
    pub supports_windows_images: bool,
}

/// This contract intentionally contains no operating-system handles.
pub trait PlatformBackend {
    fn capabilities(&self) -> BackendCapabilities;
}
