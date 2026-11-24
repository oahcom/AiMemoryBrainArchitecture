//! `brain compile --store` must write a memory database a *different process*
//! can open (#860).
//!
//! `compile` was the only verb that wrote a memory and it deleted that memory's
//! database on exit, so `forget` — which requires a database that already holds
//! committed memory — had no CLI producer at all. The only way to make a
//! database `forget` could operate on was to call the library from a test.
//!
//! Three properties, each asserted against real processes:
//!
//! 1. `compile_store_is_opened_by_a_separate_forget_process` — process A writes
//!    a caller-chosen path; process B (`brain forget`) reads memory from it, and
//!    the test process reads the compiled Claim's own text back out of the file.
//! 2. `compile_without_store_leaves_no_database_behind` — the default stays
//!    process-scoped, so the flag did not turn every run into a leak.
//! 3. `a_failed_compile_leaves_no_readable_store_of_its_own` — a run that fails
//!    before storage is opened creates no file at all; a run that fails after
//!    opening an existing store adds nothing observable to it.

use memory_domain::{Memory, MemoryVersion, OpaqueId, ScopeKind, ScopeRef};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::MemoryStore;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output, Stdio};
use std::sync::atomic::{AtomicU64, Ordering};

/// Identifiers come from `crates/brain-cli/fixtures/event.json`. The Claim text
/// asserted below is that fixture's payload, so a store that only *exists* is
/// not enough — its content must be the compiled one.
const MEMORY_ID: &str = "memory-demo-001";
const VERSION_ID: &str = "memory-version-demo-001";
const CLAIM_PREDICATE: &str = "uses";
const CLAIM_OBJECT: &str = "a governed memory context";

static NEXT_TEST_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_TEST_ID.fetch_add(1, Ordering::Relaxed);
        let path = std::env::temp_dir().join(format!(
            "brain-cli-compile-store-{}-{id}",
            std::process::id()
        ));
        fs::create_dir_all(&path).expect("create test directory");
        Self { path }
    }

    fn store_path(&self) -> PathBuf {
        self.path.join("memory.sqlite")
    }

    fn output_path(&self) -> PathBuf {
        self.path.join("context.json")
    }

    /// The fixture's own scope, serialized in the shape `brain forget --scope`
    /// reads: a JSON array of ScopeRef.
    fn scope_path(&self) -> PathBuf {
        let path = self.path.join("scope.json");
        fs::write(
            &path,
            serde_json::to_vec(&vec![scope()]).expect("serialize scope"),
        )
        .expect("write scope fixture");
        path
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

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifiers are non-empty")
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-demo"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:demo".into(),
    }
}

fn compile(directory: &TestDirectory, store: Option<&Path>) -> Output {
    let mut command = Command::new(env!("CARGO_BIN_EXE_brain"));
    command
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(directory.output_path());
    if let Some(path) = store {
        command.arg("--store").arg(path);
    }
    command.output().expect("execute brain compile")
}

fn forget(store: &Path, scope_path: &Path) -> Output {
    Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("forget")
        .arg("--store")
        .arg(store)
        .arg("--scope")
        .arg(scope_path)
        .arg("--forget")
        .arg(MEMORY_ID)
        .arg("--forget-reason")
        .arg("sha256:compile-store-test")
        .output()
        .expect("execute brain forget")
}

fn read_revision(store_path: &Path) -> Option<MemoryVersion> {
    let store = MemoryStore::new(SqliteMemoryStorage::open(store_path).expect("open store"));
    store
        .read_revision(&id(MEMORY_ID), &id(VERSION_ID), &[scope()])
        .expect("read revision succeeds")
}

fn read_memory(store_path: &Path) -> Option<Memory> {
    let store = MemoryStore::new(SqliteMemoryStorage::open(store_path).expect("open store"));
    store
        .read_memory(&id(MEMORY_ID), &[scope()])
        .expect("read memory succeeds")
}

/// The acceptance condition for #860, in three real processes: this test's own
/// process only observes; the two actors are `brain` invocations.
#[test]
fn compile_store_is_opened_by_a_separate_forget_process() {
    let directory = TestDirectory::new();
    let store_path = directory.store_path();

    // Process 1: compile, naming the path it wants the memory to live at.
    let compile_output = compile(&directory, Some(&store_path));
    assert_eq!(
        compile_output.status.code(),
        Some(0),
        "compile --store must exit 0:\n{}",
        String::from_utf8_lossy(&compile_output.stderr)
    );
    assert!(
        store_path.is_file(),
        "compile --store must leave the memory database at the caller-chosen path {}",
        store_path.display()
    );

    // The content, read out of that file: a database that exists but holds no
    // compiled Claim would satisfy `Path::is_file` and prove nothing.
    let compiled = read_revision(&store_path).unwrap_or_else(|| {
        panic!(
            "the store at {} must contain the compiled revision {VERSION_ID}",
            store_path.display()
        )
    });
    let claim = compiled
        .claims
        .first()
        .expect("the compiled revision must carry the fixture Claim");
    assert_eq!(claim.predicate, CLAIM_PREDICATE);
    assert_eq!(claim.object_value, CLAIM_OBJECT);

    // Process 2: a separate invocation forgets through the same path. This is
    // the verb that had no CLI producer: it exits 0 only if the file still
    // exists and already holds this memory.
    let scope_path = directory.scope_path();
    assert!(
        store_path.is_file(),
        "the store must still exist between the two invocations"
    );
    let forget_output = forget(&store_path, &scope_path);
    let stdout = String::from_utf8_lossy(&forget_output.stdout);
    assert_eq!(
        forget_output.status.code(),
        Some(0),
        "a second process must be able to forget what the first compiled:\n{}",
        String::from_utf8_lossy(&forget_output.stderr)
    );
    assert!(
        stdout.contains("forget applied: target=Memory memory=memory-demo-001 fence_sequence="),
        "the second process must confirm the memory it read:\n{stdout}"
    );

    // And the fence the second process wrote governs the compiled memory: the
    // read gate now hides it, which is only possible because both processes
    // touched the same database.
    assert_eq!(
        read_revision(&store_path),
        None,
        "a forgotten compiled memory must read as None through the same gate"
    );
    assert_eq!(read_memory(&store_path), None);
}

/// The flag must not turn every run into a leak: without `--store`, the
/// database keeps its process-scoped default and is removed on exit.
#[test]
fn compile_without_store_leaves_no_database_behind() {
    let directory = TestDirectory::new();

    // `TemporaryDatabase::new("storage")` names its file after the *child's*
    // pid, so the pid is captured before waiting and the path is checked for
    // absence both before and after. A leftover from an earlier process that
    // reused this pid would make the before-check fail rather than let the
    // after-check pass for the wrong reason.
    let child = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(TestDirectory::fixture_path())
        .arg("--out")
        .arg(directory.output_path())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .expect("spawn brain compile");
    let pid = child.id();
    let base = std::env::temp_dir().join(format!("brain-cli-storage-{pid}.sqlite"));
    assert!(
        !base.exists(),
        "the default database path {} must not pre-exist this run, else the \
         cleanup assertion below could pass for the wrong reason",
        base.display()
    );
    let output = child.wait_with_output().expect("wait for brain compile");

    assert_eq!(
        output.status.code(),
        Some(0),
        "compile without --store must still succeed:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );

    assert!(
        !base.exists(),
        "the default memory database must be removed when the process exits, but {} survived",
        base.display()
    );
    for extension in ["sqlite-wal", "sqlite-shm"] {
        let sidecar = base.with_extension(extension);
        assert!(
            !sidecar.exists(),
            "the default run must not leave {} behind",
            sidecar.display()
        );
    }
}

/// A failed compile must not leave a store that a later process reads as a
/// valid memory database of its own.
///
/// Two failure points, two post-conditions:
/// - before storage is opened: no file is created at all (asserted as absent);
/// - after an existing store is opened: the file keeps exactly the content the
///   earlier run committed and gains nothing from the failed run, so a later
///   reader sees the same single revision rather than an empty workspace.
#[test]
fn a_failed_compile_leaves_no_readable_store_of_its_own() {
    let directory = TestDirectory::new();

    // Failure point 1: the input cannot be read, so storage is never opened.
    let unopened = directory.path.join("never-opened.sqlite");
    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(directory.path.join("absent-input.json"))
        .arg("--out")
        .arg(directory.output_path())
        .arg("--store")
        .arg(&unopened)
        .output()
        .expect("execute brain compile");
    assert_eq!(
        output.status.code(),
        Some(1),
        "an unreadable input must exit non-zero"
    );
    assert!(
        !unopened.exists(),
        "a compile that never reached storage must not create the --store file {}",
        unopened.display()
    );

    // Failure point 2: the store exists and already holds this memory, so the
    // second compile fails at create_memory rather than at open.
    let store_path = directory.store_path();
    let first = compile(&directory, Some(&store_path));
    assert_eq!(
        first.status.code(),
        Some(0),
        "the first compile must succeed:\n{}",
        String::from_utf8_lossy(&first.stderr)
    );
    let second = compile(&directory, Some(&store_path));
    assert_eq!(
        second.status.code(),
        Some(1),
        "re-compiling the same memory into the same store must fail"
    );
    assert!(
        String::from_utf8_lossy(&second.stderr).contains("create_memory failed"),
        "the failure must be the duplicate memory, not a storage error:\n{}",
        String::from_utf8_lossy(&second.stderr)
    );

    // The post-condition: the file still describes the first run's memory and
    // nothing else. An empty-but-valid database would read as `None` here.
    let survived = read_revision(&store_path)
        .expect("the store must still hold the revision the successful compile committed");
    assert_eq!(
        survived
            .claims
            .first()
            .map(|claim| claim.object_value.as_str()),
        Some(CLAIM_OBJECT),
        "the surviving revision must be the compiled one, not a blank row"
    );
    assert!(
        read_memory(&store_path).is_some(),
        "the memory metadata the successful compile wrote must survive the failed run"
    );
}
