use memory_domain::{Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef};
use memory_storage::{CommitRequest, CommitSequence, MemoryStorage, StorageError};
use memory_storage_sqlite::SqliteMemoryStorage;
use std::sync::{Arc, Barrier};
use std::thread;
use std::time::{SystemTime, UNIX_EPOCH};

fn id(value: &str) -> OpaqueId { OpaqueId::new(value).unwrap() }

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-1"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:scope-1".into(),
    }
}

fn memory() -> Memory {
    Memory {
        memory_id: id("memory-1"),
        memory_kind: "knowledge".into(),
        scope_refs: vec![scope()],
        current_version_id: None,
        lifecycle_state: MemoryLifecycle::Candidate,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "now".into(),
        updated_at: "now".into(),
    }
}

fn version(version_id: &str) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id("memory-1"),
        version_number: 1,
        parent_version_id: None,
        created_at: "now".into(),
        author_kind: "concurrency-test".into(),
        change_reason: "competing first commit".into(),
        claims: vec![],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![],
        provenance_refs: vec![],
        content_digest: format!("digest-{version_id}"),
        schema_version: "1".into(),
    }
}

fn temp_db_path() -> std::path::PathBuf {
    let nonce = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
    std::env::temp_dir().join(format!("memory-brain-writer-race-{}-{nonce}.sqlite", std::process::id()))
}

fn remove_db_files(path: &std::path::Path) {
    let _ = std::fs::remove_file(path);
    let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
    let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
}

#[test]
fn independent_connections_serialize_competing_first_commits() {
    let path = temp_db_path();
    {
        let mut setup = SqliteMemoryStorage::open(&path).unwrap();
        setup.create_memory(memory(), &[scope()]).unwrap();
    }

    let barrier = Arc::new(Barrier::new(2));
    let mut workers = Vec::new();
    for index in 0..2 {
        let worker_path = path.clone();
        let worker_barrier = Arc::clone(&barrier);
        workers.push(thread::spawn(move || {
            // Each worker owns an independently opened SQLite connection.
            let mut store = SqliteMemoryStorage::open(&worker_path).unwrap();
            let suffix = if index == 0 { "a" } else { "b" };
            worker_barrier.wait();
            store.commit_version(
                CommitRequest {
                    memory_id: id("memory-1"),
                    expected_current_version: None,
                    new_version: version(&format!("version-{suffix}")),
                    idempotency_key: format!("first-commit-{suffix}"),
                    request_digest: format!("request-{suffix}"),
                },
                &[scope()],
            )
        }));
    }

    let results: Vec<_> = workers.into_iter().map(|worker| worker.join().unwrap()).collect();
    assert_eq!(results.iter().filter(|result| result.is_ok()).count(), 1);
    assert_eq!(
        results.iter().filter(|result| **result == Err(StorageError::StaleVersion)).count(),
        1
    );

    let reopened = SqliteMemoryStorage::open(&path).unwrap();
    let current = reopened.read_current(&id("memory-1"), &[scope()]).unwrap().unwrap();
    assert_eq!(current.version_number, 1);
    let changes = reopened.list_changes(None, &[scope()], 10).unwrap();
    assert_eq!(changes.records.len(), 1);
    assert_eq!(changes.records[0].commit_sequence, CommitSequence(1));
    drop(reopened);
    remove_db_files(&path);
}
