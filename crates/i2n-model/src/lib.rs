//! Shared, platform-independent Image2Native domain types.

use core::fmt;
use core::str::FromStr;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum OperatingSystem {
    Linux,
    Macos,
    Windows,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Architecture {
    X86_64,
    Aarch64,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct TargetPlatform {
    pub os: OperatingSystem,
    pub architecture: Architecture,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParseTargetError(pub String);

impl fmt::Display for ParseTargetError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for ParseTargetError {}

impl FromStr for TargetPlatform {
    type Err = ParseTargetError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let (os_name, architecture_name) = match value.split_once('-') {
            Some(parts) => parts,
            None => {
                return Err(ParseTargetError(
                    "target must have the form <os>-<architecture>".to_owned(),
                ));
            }
        };

        let os = match os_name {
            "linux" => OperatingSystem::Linux,
            "macos" => OperatingSystem::Macos,
            "windows" => OperatingSystem::Windows,
            _ => {
                return Err(ParseTargetError(format!("unsupported operating system `{os_name}`")));
            }
        };

        let architecture = match architecture_name {
            "x86_64" | "x64" => Architecture::X86_64,
            "aarch64" | "arm64" => Architecture::Aarch64,
            _ => {
                return Err(ParseTargetError(format!(
                    "unsupported architecture `{architecture_name}`"
                )));
            }
        };

        Ok(Self { os, architecture })
    }
}

impl fmt::Display for TargetPlatform {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let os = match self.os {
            OperatingSystem::Linux => "linux",
            OperatingSystem::Macos => "macos",
            OperatingSystem::Windows => "windows",
        };
        let architecture = match self.architecture {
            Architecture::X86_64 => "x86_64",
            Architecture::Aarch64 => "aarch64",
        };

        write!(f, "{os}-{architecture}")
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Digest {
    pub algorithm: String,
    pub encoded: String,
}

impl FromStr for Digest {
    type Err = ParseTargetError;

    fn from_str(value: &str) -> Result<Self, Self::Err> {
        let (algorithm, encoded) = match value.split_once(':') {
            Some(parts) => parts,
            None => {
                return Err(ParseTargetError(
                    "digest must have the form algorithm:encoded".to_owned(),
                ));
            }
        };

        let is_hex = encoded.bytes().all(|byte| byte.is_ascii_hexdigit());
        if algorithm.is_empty() || encoded.is_empty() || !is_hex {
            return Err(ParseTargetError(
                "digest must contain an algorithm and hexadecimal value".to_owned(),
            ));
        }

        Ok(Self {
            algorithm: algorithm.to_owned(),
            encoded: encoded.to_ascii_lowercase(),
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_supported_targets() {
        let target = "macos-arm64".parse::<TargetPlatform>().unwrap();
        assert_eq!(target.os, OperatingSystem::Macos);
        assert_eq!(target.architecture, Architecture::Aarch64);
        assert_eq!(target.to_string(), "macos-aarch64");
    }

    #[test]
    fn rejects_unknown_target() {
        assert!("plan9-quantum".parse::<TargetPlatform>().is_err());
    }

    #[test]
    fn parses_sha256_digest_shape() {
        let digest = "sha256:abcdef".parse::<Digest>().unwrap();
        assert_eq!(digest.algorithm, "sha256");
        assert_eq!(digest.encoded, "abcdef");
    }
}
