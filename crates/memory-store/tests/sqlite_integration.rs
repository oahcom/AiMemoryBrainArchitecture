use memory_domain::{Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef};
use memory_storage::StorageError;
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, MemoryStoreError, RevisionWrite};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope(idv: &str) -> ScopeRef {
    ScopeRef {
        scope_id: id(idv),
        scope_kind: ScopeKind::User,
        namespace_key: "test".into(),
    }
}

fn memory() -> Memory {
    Memory {
        memory_id: id("m1"),
        memory_kind: "semantic".into(),
        scope_refs: vec![scope("s1")],
        current_version_id: None,
        lifecycle_state: MemoryLifecycle::Candidate,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "now".into(),
        updated_at: "now".into(),
    }
}

fn revision(idv: &str, n: u64, parent: Option<&str>) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(idv),
        memory_id: id("m1"),
        version_number: n,
        parent_version_id: parent.map(id),
        created_at: "now".into(),
        author_kind: "test".into(),
        change_reason: "integration".into(),
        claims: vec![],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![],
        provenance_refs: vec![],
        content_digest: format!("digest-{idv}"),
        schema_version: "1".into(),
    }
}

#[test]
fn sqlite_is_a_minimal_runnable_memory_store_path() {
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store.create_memory(memory(), &[scope("s1")]).unwrap();

    let first = store
        .write_revision(
            RevisionWrite {
                memory_id: id("m1"),
                expected_current_version: None,
                revision: revision("v1", 1, None),
                idempotency_key: "op1".into(),
                request_digest: "digest-1".into(),
            },
            &[scope("s1")],
        )
        .unwrap();

    let current = store
        .read_current(&id("m1"), &[scope("s1")])
        .unwrap()
        .unwrap();
    assert_eq!(current.memory_version_id, id("v1"));

    let replay = store
        .write_revision(
            RevisionWrite {
                memory_id: id("m1"),
                expected_current_version: Some(id("v1")),
                revision: revision("v2", 2, Some("v1")),
                idempotency_key: "op1".into(),
                request_digest: "digest-1".into(),
            },
            &[scope("s1")],
        )
        .unwrap();
    assert_eq!(replay, first);

    let other = scope("s2");
    assert_eq!(
        store.read_current(&id("m1"), &[other]),
        Err(MemoryStoreError::Storage(StorageError::ScopeMismatch))
    );
}

#[test]
fn sqlite_rejects_revision_identity_mismatch_at_facade_boundary() {
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store.create_memory(memory(), &[scope("s1")]).unwrap();
    let result = store.write_revision(
        RevisionWrite {
            memory_id: id("other"),
            expected_current_version: None,
            revision: revision("v1", 1, None),
            idempotency_key: "op1".into(),
            request_digest: "digest-1".into(),
        },
        &[scope("s1")],
    );
    assert_eq!(result, Err(MemoryStoreError::MemoryIdentityMismatch));
}
