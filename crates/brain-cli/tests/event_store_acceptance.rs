use memory_event_store_sqlite::SqliteEventStore;
use serde_json::Value;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_ID.fetch_add(1, Ordering::Relaxed);
        let path = std::env::temp_dir().join(format!(
            "brain-event-store-test-{}-{id}",
            std::process::id()
        ));

        fs::create_dir_all(&path).expect("create test directory");
        Self { path }
    }

    fn fixture() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .join("fixtures")
            .join("event.json")
    }

    fn output(&self) -> PathBuf {
        self.path.join("context.json")
    }

    fn event_database(&self) -> PathBuf {
        self.path.join("event-store-idempotent.sqlite")
    }

    fn input_with_empty_scope(&self) -> PathBuf {
        let mut input: Value =
            serde_json::from_slice(&fs::read(Self::fixture()).expect("read fixture"))
                .expect("parse fixture");

        input["event"]["scope_refs"] = Value::Array(Vec::new());

        let path = self.path.join("empty-scope.json");
        fs::write(
            &path,
            serde_json::to_vec_pretty(&input).expect("serialize modified fixture"),
        )
        .expect("write modified fixture");

        path
    }
}

impl Drop for TestDirectory {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

fn execute(input: &Path, output: &Path, event_database: Option<&Path>) -> Output {
    let mut command = Command::new(env!("CARGO_BIN_EXE_brain"));

    command
        .arg("compile")
        .arg("--input")
        .arg(input)
        .arg("--out")
        .arg(output)
        .arg("--verbose");

    if let Some(database) = event_database {
        command.arg("--event-store").arg(database);
    }

    command.output().expect("spawn brain CLI")
}

/// The Owner ruling of 2026-11-22 made compile results deliberately ephemeral:
/// `run_compiler_stage` gets `storage_path` and `admission_path` from
/// `TemporaryDatabase`, which deletes both in `Drop`, so the only durable
/// artifact a compile leaves behind is the accepted event and its outbox row.
///
/// This test pins the part of that contract that is observable from outside the
/// binary. If someone adds a `--storage` flag or starts persisting a result, the
/// outbox count or the snapshot will move, and the change has to be argued for
/// instead of slipping in.
///
/// ponytail: this checks the outbox and the output, not the schema. A table
/// named something unexpected would pass. Checking `sqlite_master` would mean
/// adding `rusqlite` as a `brain-cli` dev-dependency to read a file this crate
/// does not otherwise open; when a durable result actually appears, that is the
/// moment to pay for it, not now.
#[test]
fn compile_leaves_no_durable_result_behind() {
    let directory = TestDirectory::new();
    let input = TestDirectory::fixture();
    let database = directory.event_database();
    let first = directory.output();
    let second = directory.path.join("context-second.json");

    assert_success(&execute(&input, &first, Some(&database)));

    let store = SqliteEventStore::open(&database).expect("open event store");
    let intents_after_first = store
        .pending_compile_intents()
        .expect("read pending compile intents");
    drop(store);

    assert_success(&execute(&input, &second, Some(&database)));

    let store = SqliteEventStore::open(&database).expect("open event store");
    let intents_after_second = store
        .pending_compile_intents()
        .expect("read pending compile intents");
    drop(store);

    // A second compile must not enqueue a second intent. `compile_outbox.event_row`
    // is UNIQUE, so a growing count would mean someone added a second row per
    // attempt, which is the first half of "a compile result became durable".
    assert_eq!(
        intents_after_first.len(),
        1,
        "one accepted event must produce exactly one compile intent"
    );
    assert_eq!(
        intents_after_second.len(),
        1,
        "a re-run must re-read the same intent, not enqueue another"
    );

    // And both runs must agree. They can only agree if neither wrote a result
    // the other one read.
    assert_eq!(
        fs::read(&first).expect("read first snapshot"),
        fs::read(&second).expect("read second snapshot"),
        "two runs of the same event must produce the same snapshot"
    );
}

fn receipt_id(stderr: &str) -> String {
    stderr
        .lines()
        .find_map(|line| line.strip_prefix("accepted receipt: "))
        .expect("accepted receipt must appear in verbose stderr")
        .trim()
        .to_owned()
}

fn assert_success(output: &Output) {
    assert_eq!(
        output.status.code(),
        Some(0),
        "CLI should succeed:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );
}

fn assert_snapshot(output_path: &Path) {
    let bytes = fs::read(output_path).expect("read context snapshot");
    let snapshot: Value = serde_json::from_slice(&bytes).expect("parse context snapshot");

    assert_eq!(snapshot["identity"]["context_id"], "context-demo-001");

    assert_eq!(snapshot["entries"].as_array().map(Vec::len), Some(1));

    let rendered = snapshot["entries"][0]["rendered_content"]
        .as_str()
        .expect("rendered_content must be a string");

    assert!(
        rendered.contains("uses"),
        "rendered Claim must retain its predicate: {rendered}"
    );

    assert!(
        rendered.contains("a governed memory context"),
        "rendered Claim must retain its object: {rendered}"
    );

    let mut sidecar = output_path.as_os_str().to_os_string();
    sidecar.push(".compiler-status");
    let sidecar = PathBuf::from(sidecar);

    let status = fs::read_to_string(sidecar).expect("read compiler sidecar");

    assert!(
        status.starts_with("compiler stage blocked:"),
        "publication must remain blocked:\n{status}"
    );
}

#[test]
fn normal_input_is_accepted_and_receipt_is_visible_without_changing_snapshot() {
    let directory = TestDirectory::new();
    let output_path = directory.output();

    let result = execute(&TestDirectory::fixture(), &output_path, None);

    assert_success(&result);

    let stderr = String::from_utf8_lossy(&result.stderr);
    assert!(
        stderr.contains("accepted receipt: receipt:"),
        "verbose output must contain the durable receipt:\n{stderr}"
    );

    assert_snapshot(&output_path);
}

#[test]
fn repeated_processes_reuse_receipt_and_create_only_one_compile_intent() {
    let directory = TestDirectory::new();
    let database = directory.event_database();
    let input = TestDirectory::fixture();

    let first_output = directory.path.join("first-context.json");
    let second_output = directory.path.join("second-context.json");

    // First independent CLI process.
    let first = execute(&input, &first_output, Some(&database));
    assert_success(&first);

    // Second independent CLI process, using the same persistent EventStore.
    let second = execute(&input, &second_output, Some(&database));
    assert_success(&second);

    let first_stderr = String::from_utf8_lossy(&first.stderr);
    let second_stderr = String::from_utf8_lossy(&second.stderr);

    let first_receipt = receipt_id(&first_stderr);
    let second_receipt = receipt_id(&second_stderr);

    assert_eq!(
        first_receipt, second_receipt,
        "idempotent acceptance must return the original receipt"
    );

    let store = SqliteEventStore::open(&database).expect("reopen persistent EventStore");

    let intents = store
        .pending_compile_intents()
        .expect("read compile outbox");

    assert_eq!(
        intents.len(),
        1,
        "idempotent acceptance must not create a second outbox row"
    );

    assert_snapshot(&first_output);
    assert_snapshot(&second_output);
}

#[test]
fn empty_scope_is_rejected_before_any_output_is_written() {
    let directory = TestDirectory::new();
    let input = directory.input_with_empty_scope();
    let output_path = directory.output();

    let result = execute(&input, &output_path, None);

    assert_ne!(
        result.status.code(),
        Some(0),
        "empty scope must fail acceptance"
    );

    let stderr = String::from_utf8_lossy(&result.stderr);

    assert!(
        stderr.contains("event-store accept failed:"),
        "stderr must identify the EventStore rejection:\n{stderr}"
    );

    assert!(
        stderr.contains("ScopeMismatch"),
        "empty scope should be rejected by EventStore scope validation:\n{stderr}"
    );

    assert!(
        !output_path.exists(),
        "failed acceptance must not write a ContextSnapshot"
    );
}
