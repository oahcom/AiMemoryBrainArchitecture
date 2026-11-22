use memory_event_store::{EventStore, ProcessingState};
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

fn receipt_id(stderr: &str) -> String {
    stderr
        .lines()
        .find_map(|line| line.strip_prefix("accepted receipt: "))
        .and_then(|value| value.split_whitespace().next())
        .expect("accepted receipt must appear in verbose stderr")
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
    let input = TestDirectory::fixture();
    let database = directory.event_database();

    let first_output = directory.path.join("first-context.json");
    let second_output = directory.path.join("second-context.json");

    // Process 1: accept the fixture event and persist its compile intent.
    let first = execute(&input, &first_output, Some(&database));
    assert_success(&first);

    let first_receipt = receipt_id(&String::from_utf8_lossy(&first.stderr));

    // Read the durable outbox state before the retry.
    let first_snapshot = {
        let store =
            SqliteEventStore::open(&database).expect("reopen EventStore after first process");
        store
            .pending_compile_intents()
            .expect("read compile outbox after first process")
    };

    assert_eq!(
        first_snapshot.len(),
        1,
        "first process must create exactly one compile intent"
    );

    // Process 2: retry the same fixture against the same persistent database.
    let second = execute(&input, &second_output, Some(&database));
    assert_success(&second);

    let second_receipt = receipt_id(&String::from_utf8_lossy(&second.stderr));

    // Reopen the database and read the outbox again after the retry.
    let store =
        SqliteEventStore::open(&database).expect("reopen persistent EventStore after retry");
    let second_snapshot = store
        .pending_compile_intents()
        .expect("read compile outbox after retry");

    assert_eq!(
        second_snapshot.len(),
        1,
        "retry must not create a duplicate compile intent"
    );

    // Receipt identity must be reused across independent processes.
    assert_eq!(first_receipt, second_receipt);

    let first_intent = &first_snapshot[0];
    let second_intent = &second_snapshot[0];

    // The accepted work must be a compile intent with the exact fixture payload.
    assert_eq!(first_intent.intent_kind, "compile");
    assert_eq!(
        first_intent.payload_bytes,
        b"The project uses a governed memory context."
    );

    // Acceptance is durable, but compilation has not been acknowledged.
    assert_eq!(
        first_intent.receipt.processing_state,
        ProcessingState::Pending
    );

    // Both persisted row identities must remain stable across the retry.
    assert_eq!(first_intent.outbox_row, second_intent.outbox_row);
    assert_eq!(first_intent.event_row, second_intent.event_row);

    // The receipt and payload must remain unchanged across the retry.
    assert_eq!(first_intent.receipt, second_intent.receipt);
    assert_eq!(first_intent.payload_bytes, second_intent.payload_bytes);

    // EventStore status must agree with the persisted receipt.
    let status = store
        .status(
            &second_intent.receipt.event_id,
            &second_intent.envelope.scope_refs,
        )
        .expect("read EventStore status for accepted event");

    assert_eq!(status, Some(second_intent.receipt.clone()));

    // Both processes must produce valid snapshots with an observable compiler block.
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
