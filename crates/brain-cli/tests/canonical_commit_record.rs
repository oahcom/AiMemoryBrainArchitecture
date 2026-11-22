use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

/// Without `--canonical-commit` the run keeps the legacy pending reference, so
/// `canonical_commit_confirmed` stays false and the gate blocks (GAP-12 §6.5).
const BLOCKED_NOTICE: &str = "compiler stage blocked: publication not authorized; \
     blocking flag: canonical_commit_confirmed; false flags: [canonical_commit_confirmed, \
     publication_participant_admitted, protected_visibility_authorized]";

/// With a durable dev-baseline record the validator confirms the commit, so that
/// flag drops out of the false list; the gate then suppresses because GAP-13
/// still has no issuer for the remaining two flags.
const SUPPRESSED_NOTICE: &str = "compiler stage suppressed: publication not authorized; \
     blocking flag: publication_participant_admitted; false flags: [\
     publication_participant_admitted, protected_visibility_authorized]";

static NEXT_TEST_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_TEST_ID.fetch_add(1, Ordering::Relaxed);
        let path = std::env::temp_dir().join(format!(
            "brain-cli-canonical-commit-{}-{id}",
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

fn execute_compile(output_path: &Path, issue_canonical_commit: bool) -> Output {
    let mut command = Command::new(env!("CARGO_BIN_EXE_brain"));
    command
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(output_path);
    if issue_canonical_commit {
        command.arg("--canonical-commit");
    }
    command.output().expect("execute brain binary")
}

fn assert_notice(output: &Output, output_path: &Path, expected: &str) {
    assert_eq!(
        output.status.code(),
        Some(0),
        "brain compile must exit 0; stderr:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert_eq!(
        stderr.lines().filter(|line| *line == expected).count(),
        1,
        "expected exactly one notice line; stderr:\n{stderr}"
    );
    let sidecar = fs::read_to_string(TestDirectory::sidecar_path(output_path))
        .expect("read compiler status sidecar");
    assert_eq!(sidecar, format!("{expected}\n"));
}

#[test]
fn pending_reference_still_blocks_publication() {
    let directory = TestDirectory::new();
    let output_path = directory.output_path();
    let output = execute_compile(&output_path, false);
    assert_notice(&output, &output_path, BLOCKED_NOTICE);
}

#[test]
fn an_issued_canonical_commit_record_confirms_the_commit_and_still_suppresses() {
    let directory = TestDirectory::new();
    let output_path = directory.output_path();
    let output = execute_compile(&output_path, true);
    assert_notice(&output, &output_path, SUPPRESSED_NOTICE);
}
