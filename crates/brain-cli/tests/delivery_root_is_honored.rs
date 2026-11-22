//! `--delivery-root` must be honored by a persistent adapter.
//!
//! A `--delivery-root <dir>` selects `FileContextDeliveryAdapter`, so each
//! session's applied snapshot lands in `<dir>/<session_id>.json` and survives
//! the process. The adapter reads the existing record on open, which makes a
//! repeat delivery of the same snapshot an `AlreadyApplied` no-op rather than
//! a version error.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

const IGNORED_WARNING: &str = "--delivery-root ignored";

static NEXT_TEST_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_TEST_ID.fetch_add(1, Ordering::Relaxed);
        let path = std::env::temp_dir().join(format!(
            "brain-cli-delivery-root-{}-{id}",
            std::process::id()
        ));
        fs::create_dir_all(&path).expect("create test directory");
        Self { path }
    }

    fn output_path(&self, name: &str) -> PathBuf {
        self.path.join(name)
    }

    fn delivery_root(&self) -> PathBuf {
        self.path.join("delivered")
    }

    fn fixture_path() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("fixtures")
            .join("event.json")
    }

    /// The fixture with `context.session_id` replaced, so each run is a
    /// distinct session and therefore a distinct record file.
    fn fixture_with_session(&self, session_id: &str, name: &str) -> PathBuf {
        let text = fs::read_to_string(Self::fixture_path()).expect("read fixture");
        let patched = text.replace(
            "\"session_id\": \"session-demo-001\"",
            &format!("\"session_id\": \"{session_id}\""),
        );
        assert!(
            patched.contains(session_id),
            "fixture must contain the session id to replace"
        );
        let path = self.output_path(name);
        fs::write(&path, patched).expect("write patched fixture");
        path
    }
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

fn compile(input: &Path, delivery_root: &Path, output_path: &Path) -> Output {
    Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(input)
        .arg("--out")
        .arg(output_path)
        .arg("--delivery-root")
        .arg(delivery_root)
        .output()
        .expect("execute brain binary")
}

fn record_names(delivery_root: &Path) -> Vec<String> {
    let mut names: Vec<String> = fs::read_dir(delivery_root)
        .expect("delivery root must exist")
        .map(|entry| entry.expect("read entry").file_name())
        .map(|name| name.to_string_lossy().into_owned())
        .collect();
    names.sort();
    names
}

#[test]
fn delivery_root_persists_one_record_per_session_across_processes() {
    let directory = TestDirectory::new();
    let delivery_root = directory.delivery_root();

    let first_input = directory.fixture_with_session("session-alpha", "alpha.json");
    let first = compile(
        &first_input,
        &delivery_root,
        &directory.output_path("alpha-context.json"),
    );
    let first_stderr = String::from_utf8_lossy(&first.stderr);
    assert_eq!(
        first.status.code(),
        Some(0),
        "first run must succeed:\n{first_stderr}"
    );
    assert!(
        first_stderr.contains("delivery applied: session=session-alpha version="),
        "first run must apply the delivery:\n{first_stderr}"
    );

    let second_input = directory.fixture_with_session("session-beta", "beta.json");
    let second = compile(
        &second_input,
        &delivery_root,
        &directory.output_path("beta-context.json"),
    );
    let second_stderr = String::from_utf8_lossy(&second.stderr);
    assert_eq!(
        second.status.code(),
        Some(0),
        "second run must succeed:\n{second_stderr}"
    );
    assert!(
        !second_stderr.contains(IGNORED_WARNING),
        "--delivery-root must not be ignored any more:\n{second_stderr}"
    );

    assert_eq!(
        record_names(&delivery_root),
        vec![
            "session-alpha.json".to_owned(),
            "session-beta.json".to_owned()
        ],
        "each session must persist its own record under --delivery-root"
    );
}

#[test]
fn same_session_redelivery_is_accepted() {
    let directory = TestDirectory::new();
    let delivery_root = directory.delivery_root();
    let input = directory.fixture_with_session("session-gamma", "gamma.json");

    let first = compile(
        &input,
        &delivery_root,
        &directory.output_path("gamma-context-1.json"),
    );
    assert_eq!(
        first.status.code(),
        Some(0),
        "first run must succeed:\n{}",
        String::from_utf8_lossy(&first.stderr)
    );

    // The file adapter reopens the applied record, so the identical snapshot
    // resolves to `ApplyOutcome::AlreadyApplied` and still reports success.
    let second = compile(
        &input,
        &delivery_root,
        &directory.output_path("gamma-context-2.json"),
    );
    let second_stderr = String::from_utf8_lossy(&second.stderr);

    assert_eq!(
        second.status.code(),
        Some(0),
        "redelivery must not fail the run:\n{second_stderr}"
    );
    assert!(
        second_stderr.contains("delivery applied: session=session-gamma version=1"),
        "redelivery must be reported as applied:\n{second_stderr}"
    );
    assert!(
        !second_stderr.contains("delivery failed"),
        "redelivery must not report a delivery failure:\n{second_stderr}"
    );
    assert_eq!(
        record_names(&delivery_root),
        vec!["session-gamma.json".to_owned()],
        "redelivery must not create a second record"
    );
}

#[test]
fn delivery_root_without_value_is_rejected() {
    let directory = TestDirectory::new();

    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(directory.output_path("context.json"))
        .arg("--delivery-root")
        .output()
        .expect("execute brain binary");

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert_eq!(output.status.code(), Some(1), "missing value must fail");
    assert!(
        stderr.contains("--delivery-root requires a path"),
        "error must name the missing value:\n{stderr}"
    );
}
