use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

const COMPILER_SKIP_NOTICE: &str =
    "compiler stage skipped: PublicationAuthority has no production implementation";

const EXPECTED_USAGE: &str =
    "brain: usage: brain compile --input <event.json> --out <context.json> [--verbose]";

static NEXT_TEST_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_TEST_ID.fetch_add(1, Ordering::Relaxed);

        let path = std::env::temp_dir().join(format!(
            "brain-cli-compiler-skip-{}-{id}",
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

fn execute_compile(verbose: bool, output_path: &Path) -> Output {
    let mut command = Command::new(env!("CARGO_BIN_EXE_brain"));

    command
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(output_path);

    if verbose {
        command.arg("--verbose");
    }

    command.output().expect("execute brain binary")
}

fn assert_success_and_skip_marker(output: &Output, output_path: &Path) {
    assert_eq!(
        output.status.code(),
        Some(0),
        "brain compile must preserve exit code 0; stderr:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert_eq!(
        stderr
            .lines()
            .filter(|line| *line == COMPILER_SKIP_NOTICE)
            .count(),
        1,
        "the skip notice must appear exactly once; stderr:\n{stderr}"
    );

    assert!(
        output_path.is_file(),
        "successful compile must produce the ContextSnapshot output"
    );

    let sidecar_path = TestDirectory::sidecar_path(output_path);

    assert!(
        sidecar_path.is_file(),
        "compiler status sidecar must exist at {}",
        sidecar_path.display()
    );

    let sidecar_content = fs::read_to_string(&sidecar_path).expect("read compiler status sidecar");

    assert_eq!(
        sidecar_content,
        format!("{COMPILER_SKIP_NOTICE}\n"),
        "sidecar must contain the exact compiler skip declaration"
    );

    // The sidecar must not change the existing ContextSnapshot JSON.
    // Verify that the produced snapshot remains valid JSON with an object root.
    let snapshot_bytes = fs::read(output_path).expect("read ContextSnapshot output");

    let snapshot: serde_json::Value =
        serde_json::from_slice(&snapshot_bytes).expect("deserialize ContextSnapshot JSON");

    assert!(
        snapshot.is_object(),
        "ContextSnapshot must retain its existing JSON object representation"
    );
}

#[test]
fn compile_without_verbose_reports_skip_and_records_sidecar() {
    let directory = TestDirectory::new();
    let output_path = directory.output_path();

    let output = execute_compile(false, &output_path);

    assert_success_and_skip_marker(&output, &output_path);
}

#[test]
fn compile_with_verbose_reports_skip_exactly_once_and_records_sidecar() {
    let directory = TestDirectory::new();
    let output_path = directory.output_path();

    let output = execute_compile(true, &output_path);

    assert_success_and_skip_marker(&output, &output_path);

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(
        stderr.contains("memory-domain: Event, Memory, Claim and MemoryVersion validated"),
        "verbose diagnostics must remain available:\n{stderr}"
    );

    assert!(
        stderr.contains("memory-compiler reference version:"),
        "compiler version diagnostics must remain available:\n{stderr}"
    );
}

#[test]
fn missing_input_preserves_existing_usage_error_and_exit_code() {
    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--out")
        .arg("unused-context.json")
        .output()
        .expect("execute brain binary");

    assert_eq!(
        output.status.code(),
        Some(1),
        "missing --input must preserve exit code 1"
    );

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(
        stderr.contains(EXPECTED_USAGE),
        "existing usage error message must remain unchanged:\n{stderr}"
    );
}

#[test]
fn missing_output_preserves_existing_usage_error_and_exit_code() {
    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .output()
        .expect("execute brain binary");

    assert_eq!(
        output.status.code(),
        Some(1),
        "missing --out must preserve exit code 1"
    );

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(
        stderr.contains(EXPECTED_USAGE),
        "existing usage error message must remain unchanged:\n{stderr}"
    );
}
