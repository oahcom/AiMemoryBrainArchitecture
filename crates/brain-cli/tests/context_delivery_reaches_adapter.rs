use serde_json::Value;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::atomic::{AtomicU64, Ordering};

const COMPILER_BLOCKED_NOTICE: &str = "compiler stage blocked: publication not authorized; \
     blocking flag: canonical_commit_confirmed; false flags: [canonical_commit_confirmed, \
     publication_participant_admitted, protected_visibility_authorized]";

const DELIVERY_PREFIX: &str = "delivery applied: session=brain-cli-session version=";

static NEXT_TEST_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_TEST_ID.fetch_add(1, Ordering::Relaxed);

        let path = std::env::temp_dir().join(format!(
            "brain-cli-context-delivery-{}-{id}",
            std::process::id()
        ));

        fs::create_dir_all(&path).expect("create test directory");

        Self { path }
    }

    fn output_path(&self) -> PathBuf {
        self.path.join("context.json")
    }

    fn sidecar_path(output_path: &Path) -> PathBuf {
        let mut name = output_path.as_os_str().to_os_string();
        name.push(".compiler-status");
        PathBuf::from(name)
    }

    fn fixture_path() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("fixtures")
            .join("event.json")
    }
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

#[test]
fn context_snapshot_reaches_agent_adapter_and_preserves_compiler_contract() {
    let directory = TestDirectory::new();
    let output_path = directory.output_path();

    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(&output_path)
        .output()
        .expect("execute brain binary");

    let stderr = String::from_utf8_lossy(&output.stderr);

    // 1. Delivery must not make the CLI fail.
    assert_eq!(
        output.status.code(),
        Some(0),
        "brain compile must exit successfully:\n{stderr}"
    );

    // 2. Read the exact ContextSnapshot produced by the CLI.
    let snapshot_bytes = fs::read(&output_path).expect("ContextSnapshot output must exist");

    let snapshot: Value =
        serde_json::from_slice(&snapshot_bytes).expect("valid ContextSnapshot JSON");

    let snapshot_version = snapshot["context_version"]
        .as_u64()
        .expect("context_version must be an unsigned integer");

    // 3. Exactly one successful delivery line must be emitted.
    let delivery_lines: Vec<&str> = stderr
        .lines()
        .filter(|line| line.starts_with(DELIVERY_PREFIX))
        .collect();

    assert_eq!(
        delivery_lines.len(),
        1,
        "expected exactly one delivery success line:\n{stderr}"
    );

    let delivered_version: u64 = delivery_lines[0]
        .strip_prefix(DELIVERY_PREFIX)
        .expect("delivery line must have the expected prefix")
        .parse()
        .expect("delivery version must be an unsigned integer");

    // 4. The adapter must have applied the same snapshot version.
    assert_eq!(
        delivered_version, snapshot_version,
        "adapter applied version must match ContextSnapshot.context_version"
    );

    // 5. Compiler Blocked notice must remain exactly once.
    assert_eq!(
        stderr
            .lines()
            .filter(|line| *line == COMPILER_BLOCKED_NOTICE)
            .count(),
        1,
        "compiler Blocked notice must appear exactly once:\n{stderr}"
    );

    // 6. Delivery must not contaminate the compiler-only sidecar.
    let sidecar_path = TestDirectory::sidecar_path(&output_path);

    let sidecar = fs::read_to_string(&sidecar_path).expect("compiler status sidecar must exist");

    assert_eq!(
        sidecar,
        format!("{COMPILER_BLOCKED_NOTICE}\n"),
        "compiler sidecar must retain its exact original contents"
    );
}
