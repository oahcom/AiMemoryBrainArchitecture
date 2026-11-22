//! `--delivery-root` must be honored by a persistent adapter.
//!
//! Case B at the time of writing: `FileContextDeliveryAdapter` lives in a
//! parallel task and is not on `main` yet. So `--delivery-root` is accepted,
//! warned about on stderr, and the run still succeeds on the in-memory
//! adapter. When the file adapter lands, the second test below flips to
//! asserting persisted files and cross-process applied state.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

const WARNING: &str =
    "warning: --delivery-root ignored, no persistent adapter available in this build";

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
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

fn compile(delivery_root: &Path, output_path: &Path) -> Output {
    Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(output_path)
        .arg("--delivery-root")
        .arg(delivery_root)
        .output()
        .expect("execute brain binary")
}

#[test]
fn delivery_root_is_accepted_and_delivery_still_succeeds() {
    let directory = TestDirectory::new();
    let delivery_root = directory.delivery_root();

    let output = compile(&delivery_root, &directory.output_path("context.json"));
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert_eq!(
        output.status.code(),
        Some(0),
        "--delivery-root must not fail the run:\n{stderr}"
    );
    assert!(
        stderr.contains(WARNING),
        "case B must warn that --delivery-root is ignored:\n{stderr}"
    );
    assert!(
        stderr.contains("delivery applied: session=brain-cli-session version="),
        "delivery must still be applied:\n{stderr}"
    );
}

#[test]
fn delivery_root_is_reported_once_per_run() {
    let directory = TestDirectory::new();

    let first = compile(&directory.delivery_root(), &directory.output_path("a.json"));
    let second = compile(&directory.delivery_root(), &directory.output_path("b.json"));

    for output in [&first, &second] {
        let stderr = String::from_utf8_lossy(&output.stderr);
        assert_eq!(output.status.code(), Some(0), "run must succeed:\n{stderr}");
        assert_eq!(
            stderr.lines().filter(|line| *line == WARNING).count(),
            1,
            "warning must appear exactly once:\n{stderr}"
        );
    }
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
