use memory_domain::{
    DomainError, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef,
};
use memory_storage::{MemoryStorage, StorageError};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, MemoryStoreError, RevisionWrite};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope(value: &str) -> ScopeRef {
    ScopeRef {
        scope_id: id(value),
        scope_kind: ScopeKind::User,
        namespace_key: "cross-crate-contract".into(),
    }
}

fn memory(memory_id: &str, scope_ref: ScopeRef) -> Memory {
    Memory {
        memory_id: id(memory_id),
        memory_kind: "semantic".into(),
        scope_refs: vec![scope_ref],
        current_version_id: None,
        lifecycle_state: MemoryLifecycle::Candidate,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "2026-11-21T00:00:00Z".into(),
        updated_at: "2026-11-21T00:00:00Z".into(),
    }
}

fn revision(
    memory_id: &str,
    version_id: &str,
    version_number: u64,
    parent_version_id: Option<&str>,
) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id(memory_id),
        version_number,
        parent_version_id: parent_version_id.map(id),
        created_at: "2026-11-21T00:01:00Z".into(),
        author_kind: "integration-test".into(),
        change_reason: "cross-crate contract".into(),
        claims: vec![],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![],
        provenance_refs: vec![],
        content_digest: format!("content-{version_id}"),
        schema_version: "1".into(),
    }
}

fn write(
    memory_id: &str,
    revision: MemoryVersion,
    expected_current_version: Option<&str>,
    idempotency_key: &str,
    request_digest: &str,
) -> RevisionWrite {
    RevisionWrite {
        memory_id: id(memory_id),
        expected_current_version: expected_current_version.map(id),
        revision,
        idempotency_key: idempotency_key.into(),
        request_digest: request_digest.into(),
    }
}

#[test]
fn c1_facade_trait_and_sqlite_round_trip_preserves_every_revision_field() {
    let scope_ref = scope("scope-c1");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-c1", scope_ref.clone()),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();

    let expected = revision("memory-c1", "version-c1", 1, None);
    store
        .write_revision(
            write("memory-c1", expected.clone(), None, "key-c1", "digest-c1"),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();

    let actual = store
        .read_current(&id("memory-c1"), std::slice::from_ref(&scope_ref))
        .unwrap()
        .unwrap();

    assert_eq!(actual, expected);
}

#[test]
fn c2_invalid_domain_memory_is_rejected_without_persisting_a_row() {
    let scope_ref = scope("scope-c2");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    let mut invalid = memory("memory-c2", scope_ref.clone());
    invalid.memory_kind.clear();

    assert_eq!(
        store.create_memory(invalid, std::slice::from_ref(&scope_ref)),
        Err(MemoryStoreError::InvalidDomain(
            DomainError::EmptyRequiredField("memory_kind")
        ))
    );
    assert_eq!(
        store.read_current(&id("memory-c2"), std::slice::from_ref(&scope_ref)),
        Ok(None)
    );
}

#[test]
fn c3_non_intersecting_scope_is_rejected_with_storage_scope_mismatch() {
    let scope_a = scope("scope-c3-a");
    let scope_b = scope("scope-c3-b");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-c3", scope_a.clone()),
            std::slice::from_ref(&scope_a),
        )
        .unwrap();

    assert_eq!(
        store.read_current(&id("memory-c3"), std::slice::from_ref(&scope_b)),
        Err(MemoryStoreError::Storage(StorageError::ScopeMismatch))
    );
}

#[test]
fn c4_stale_expected_version_returns_conflict_without_changing_current_revision() {
    let scope_ref = scope("scope-c4");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-c4", scope_ref.clone()),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();

    let first = revision("memory-c4", "version-c4-1", 1, None);
    store
        .write_revision(
            write("memory-c4", first.clone(), None, "key-c4-1", "digest-c4-1"),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();

    let stale = store.write_revision(
        write(
            "memory-c4",
            revision("memory-c4", "version-c4-2", 2, Some("version-c4-1")),
            Some("outdated-version"),
            "key-c4-2",
            "digest-c4-2",
        ),
        std::slice::from_ref(&scope_ref),
    );
    assert_eq!(
        stale,
        Err(MemoryStoreError::Storage(StorageError::StaleVersion))
    );
    assert_eq!(
        store
            .read_current(&id("memory-c4"), std::slice::from_ref(&scope_ref))
            .unwrap(),
        Some(first)
    );
}

#[test]
fn c5_idempotency_replay_does_not_add_a_revision_and_digest_conflict_is_rejected() {
    let scope_ref = scope("scope-c5");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-c5", scope_ref.clone()),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();

    let first_revision = revision("memory-c5", "version-c5-1", 1, None);
    let first_receipt = store
        .write_revision(
            write(
                "memory-c5",
                first_revision.clone(),
                None,
                "key-c5",
                "same-request-digest",
            ),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();

    let replay_receipt = store
        .write_revision(
            write(
                "memory-c5",
                first_revision,
                None,
                "key-c5",
                "same-request-digest",
            ),
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();
    assert_eq!(replay_receipt, first_receipt);

    let before_conflict = store
        .resolve_idempotency(
            "key-c5",
            "same-request-digest",
            std::slice::from_ref(&scope_ref),
        )
        .unwrap()
        .unwrap();
    assert_eq!(before_conflict, first_receipt);

    let conflict = store.write_revision(
        write(
            "memory-c5",
            revision("memory-c5", "version-c5-conflict", 1, None),
            None,
            "key-c5",
            "different-request-digest",
        ),
        std::slice::from_ref(&scope_ref),
    );
    assert_eq!(
        conflict,
        Err(MemoryStoreError::Storage(StorageError::IdempotencyConflict))
    );

    let current = store
        .read_current(&id("memory-c5"), std::slice::from_ref(&scope_ref))
        .unwrap()
        .unwrap();
    assert_eq!(current.memory_version_id, id("version-c5-1"));

    let storage = store.into_storage();
    let changes = storage
        .list_changes(None, std::slice::from_ref(&scope_ref), usize::MAX)
        .unwrap();
    assert_eq!(changes.records.len(), 1);
    assert_eq!(changes.records[0].version_id, id("version-c5-1"));
}

#[test]
fn c6_duplicate_memory_creation_preserves_the_storage_error_variant() {
    let scope_ref = scope("scope-c6");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    let item = memory("memory-c6", scope_ref.clone());

    store
        .create_memory(item.clone(), std::slice::from_ref(&scope_ref))
        .unwrap();

    assert_eq!(
        store.create_memory(item, std::slice::from_ref(&scope_ref)),
        Err(MemoryStoreError::Storage(StorageError::InvalidReference))
    );
}
