use std::process::ExitCode;

use i2n_model::TargetPlatform;

const HELP: &str = concat!(
    "Image2Native — OCI image-to-application compiler (scaffold)\n\n",
    "USAGE:\n  image2native <COMMAND>\n\n",
    "COMMANDS:\n",
    "  version      Show version\n",
    "  targets      List target triples\n",
    "  doctor       Show host/tooling status\n",
    "  compile      Reserved; compiler implementation is pending\n",
    "  help         Show this help\n",
);

fn main() -> ExitCode {
    let mut args = std::env::args().skip(1);

    match args.next().as_deref() {
        Some("--version") | Some("version") => {
            println!("image2native {} (scaffold)", env!("CARGO_PKG_VERSION"));
            ExitCode::SUCCESS
        }
        Some("targets") => {
            let targets = [
                "linux-x86_64",
                "linux-aarch64",
                "macos-x86_64",
                "macos-aarch64",
                "windows-x86_64",
                "windows-aarch64",
            ];
            for target in targets {
                match target.parse::<TargetPlatform>() {
                    Ok(parsed) => println!("{parsed}"),
                    Err(error) => {
                        eprintln!("internal target table error: {error}");
                        return ExitCode::FAILURE;
                    }
                }
            }
            ExitCode::SUCCESS
        }
        Some("doctor") => {
            println!("Image2Native environment doctor");
            println!("Host OS: {}", std::env::consts::OS);
            println!("Host architecture: {}", std::env::consts::ARCH);
            println!("Compiler pipeline: not implemented");
            println!("Platform backends: scaffold only");
            println!("Next step: install the Rust toolchain and run `make check`.");
            ExitCode::SUCCESS
        }
        Some("compile") => {
            eprintln!("compile is not implemented yet; see TODO.md and docs/roadmap/ROADMAP.md");
            ExitCode::from(2)
        }
        Some("help") | None => {
            println!("{HELP}");
            ExitCode::SUCCESS
        }
        Some(other) => {
            eprintln!("unknown command `{other}`; run `image2native help`");
            ExitCode::from(2)
        }
    }
}
