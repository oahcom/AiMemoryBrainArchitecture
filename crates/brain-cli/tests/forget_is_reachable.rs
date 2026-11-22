//! `brain forget` is the production caller the forget facade was missing.
//!
//! GAP-06 / GAP-11 both record that every caller of `MemoryStore::forget_*` used
//! to live inside `#[cfg(test)]`, so no executable path could forget anything.
//! These tests go through the binary: write a Memory with the real store API,
//! forget it through the CLI verb, and prove the read gate denies it afterwards.

use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef,
};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, RevisionWrite};
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_TEST_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_TEST_ID.fetch_add(1, Ordering::Relaxed);
        let path =
            std::env::temp_dir().join(format!("brain-cli-forget-{}-{id}", std::process::id()));
        fs::create_dir_all(&path).expect("create test directory");
        Self { path }
    }

    fn store_path(&self) -> PathBuf {
        self.path.join("memory.sqlite")
    }

    fn scope_path(&self) -> PathBuf {
        let path = self.path.join("scope.json");
        fs::write(
            &path,
            serde_json::to_vec(&vec![scope()]).expect("serialize scope"),
        )
        .expect("write scope fixture");
        path
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
        scope_id: id("scope-forget-cli"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:forget-cli".into(),
    }
}

fn memory(memory_id: &str, s: &ScopeRef) -> Memory {
    Memory {
        memory_id: id(memory_id),
        memory_kind: "semantic".into(),
        scope_refs: vec![s.clone()],
        current_version_id: None,
        lifecycle_state: MemoryLifecycle::Active,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "2026-11-22T00:00:00Z".into(),
        updated_at: "2026-11-22T00:00:00Z".into(),
    }
}

fn revision(memory_id: &str, version_id: &str, s: &ScopeRef) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id(memory_id),
        version_number: 1,
        parent_version_id: None,
        created_at: "2026-11-22T00:00:00Z".into(),
        author_kind: "forget-cli-test".into(),
        change_reason: "initial".into(),
        claims: vec![Claim {
            claim_id: id(&format!("claim-{version_id}")),
            subject_ref: id("subject-forget-cli"),
            predicate: "cli_state".into(),
            object_value: version_id.into(),
            polarity: "positive".into(),
            epistemic_status: EpistemicStatus::Reported,
            confidence: Some("high".into()),
            temporal_ref: None,
            asserted_at: "2026-11-22T00:00:00Z".into(),
            scope_refs: vec![s.clone()],
            qualifiers: vec![],
            evidence_refs: vec![id(&format!("source-{version_id}"))],
        }],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![id(&format!("source-{version_id}"))],
        provenance_refs: vec![],
        content_digest: format!("sha256:{version_id}"),
        schema_version: "1".into(),
    }
}

/// Seed one readable Memory through the same store API `brain compile` uses.
fn seed(store_path: &Path, memory_id: &str, version_id: &str) -> ScopeRef {
    let s = scope();
    let scope_slice = std::slice::from_ref(&s);
    let mut store = MemoryStore::new(SqliteMemoryStorage::open(store_path).expect("open store"));
    store
        .create_memory(memory(memory_id, &s), scope_slice)
        .expect("create memory");
    store
        .write_revision(
            RevisionWrite {
                memory_id: id(memory_id),
                expected_current_version: None,
                revision: revision(memory_id, version_id, &s),
                idempotency_key: format!("op-{version_id}"),
                request_digest: format!("request-{version_id}"),
            },
            scope_slice,
        )
        .expect("write revision");
    s
}

fn read_current(store_path: &Path, memory_id: &str, s: &ScopeRef) -> Option<MemoryVersion> {
    let store = MemoryStore::new(SqliteMemoryStorage::open(store_path).expect("open store"));
    store
        .read_current(&id(memory_id), std::slice::from_ref(s))
        .expect("read succeeds")
}

fn forget(directory: &TestDirectory, extra: &[&str]) -> Output {
    let mut command = Command::new(env!("CARGO_BIN_EXE_brain"));
    command
        .arg("forget")
        .arg("--store")
        .arg(directory.store_path())
        .arg("--scope")
        .arg(directory.scope_path());
    for argument in extra {
        command.arg(argument);
    }
    command.output().expect("execute brain forget")
}

#[test]
fn forget_verb_hides_the_memory_from_the_read_gate() {
    let directory = TestDirectory::new();
    let s = seed(
        &directory.store_path(),
        "memory-cli-forget",
        "version-cli-1",
    );

    let before = read_current(&directory.store_path(), "memory-cli-forget", &s);
    assert!(
        before.is_some(),
        "the memory must be readable before forget, else the test proves nothing"
    );

    let output = forget(
        &directory,
        &[
            "--forget",
            "memory-cli-forget",
            "--forget-reason",
            "sha256:cli-forget",
        ],
    );
    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);
    assert_eq!(
        output.status.code(),
        Some(0),
        "forget must exit 0:\n{stderr}"
    );
    assert!(
        stdout.contains("forget applied: target=Memory memory=memory-cli-forget fence_sequence="),
        "forget must confirm the affected target on stdout:\n{stdout}"
    );

    assert_eq!(
        read_current(&directory.store_path(), "memory-cli-forget", &s),
        None,
        "a forgotten memory must read as None through the same gate"
    );
}

#[test]
fn forget_version_verb_hides_only_that_version() {
    let directory = TestDirectory::new();
    let s = seed(
        &directory.store_path(),
        "memory-cli-version",
        "version-cli-only",
    );

    let output = forget(
        &directory,
        &[
            "--forget",
            "memory-cli-version",
            "--forget-version",
            "version-cli-only",
            "--forget-reason",
            "sha256:cli-forget-version",
        ],
    );
    assert_eq!(
        output.status.code(),
        Some(0),
        "forget --forget-version must exit 0:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(
        String::from_utf8_lossy(&output.stdout).contains("forget applied: target=Version"),
        "stdout must name the Version target:\n{}",
        String::from_utf8_lossy(&output.stdout)
    );

    let store = MemoryStore::new(SqliteMemoryStorage::open(directory.store_path()).expect("open"));
    let scope_slice = std::slice::from_ref(&s);
    assert_eq!(
        store
            .read_revision(
                &id("memory-cli-version"),
                &id("version-cli-only"),
                scope_slice
            )
            .expect("read succeeds"),
        None,
        "the fenced version must not be readable"
    );
}

#[test]
fn forget_verb_fails_nonzero_for_an_unknown_memory() {
    let directory = TestDirectory::new();
    seed(
        &directory.store_path(),
        "memory-cli-present",
        "version-cli-present",
    );

    let output = forget(
        &directory,
        &[
            "--forget",
            "memory-cli-absent",
            "--forget-reason",
            "sha256:cli-forget-missing",
        ],
    );

    assert_eq!(
        output.status.code(),
        Some(1),
        "an unknown memory id must exit non-zero"
    );
    assert!(
        String::from_utf8_lossy(&output.stderr).contains("forget_memory failed"),
        "stderr must report the failure:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(
        output.stdout.is_empty(),
        "a failed forget must not print a confirmation"
    );
}
