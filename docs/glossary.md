# Glossary

| Term | Meaning |
|---|---|
| ABI | Application Binary Interface: binary conventions between applications and OS/runtime. |
| Artifact | A compiled, packaged and verifiable Image2Native output. |
| Backend | Host-specific implementation for packaging, installing and executing an application. |
| Blob | Content-addressed byte sequence referenced by an OCI descriptor. |
| Content digest | Cryptographic identity of bytes, represented as algorithm plus digest. |
| Guest | Linux or Windows operating environment running inside a VM or managed subsystem. |
| Host | User's underlying macOS, Linux or Windows operating system. |
| I2N | Image2Native's proposed application artifact bundle format. |
| Image index | OCI object that points to platform-specific manifests. |
| Layer | Ordered filesystem changeset in an OCI image. |
| NIR | Native Image Representation; proposed target-independent compiler IR. |
| OCI | Open Container Initiative. |
| RootFS | Logical root filesystem reconstructed from image layers. |
| Runtime | Component responsible for creating/managing workload process, container or guest. |
| Native launcher | Host-OS executable that verifies, starts and manages a packaged application. |
| Native compilation | Building source for a target OS/architecture ABI to produce a target-native binary. |
| Compatibility packaging | Packaging original workload bytes with a compatible guest/runtime. |
| WSL2 | Windows Subsystem for Linux version 2, which runs a Linux kernel in a lightweight managed VM. |
| Virtio | Standard virtual device interface for guest devices such as storage and networking. |
| Whiteout | OCI layer marker that indicates deletion of a path in lower layers. |
