//! End-to-end Forget path: MemoryStore -> SqliteMemoryStorage.
//!
//! This closes the GAP-06 finding quoted in
//! `crates/memory-context/tests/e2e_negative_paths.rs`:
//!
//! > The exact missing boundary call is a public
//! > `MemoryStore::forget_memory(memory_id, scope)` (or an explicitly named
//! > lifecycle-transition API) whose successful result makes subsequent
//! > `read_current`/Context construction exclude the forgotten memory. Do not
//! > simulate this by mutating a ContextCandidate: that would not test Store's
//! > forget path.
//!
//! Everything here goes through the real SQLite adapter, not a fake.

use memory_domain::{Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef};
use memory_storage::StorageError;
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{ForgetWrite, MemoryStore, MemoryStoreError, RevisionWrite};

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

fn memory(memory_id: &str, scope_ref: &ScopeRef) -> Memory {
    Memory {
        memory_id: id(memory_id),
        memory_kind: "semantic".into(),
        scope_refs: vec![scope_ref.clone()],
        current_version_id: None,
        lifecycle_state: MemoryLifecycle::Active,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "now".into(),
        updated_at: "now".into(),
    }
}

fn revision(memory_id: &str, version_id: &str, n: u64, parent: Option<&str>) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id(memory_id),
        version_number: n,
        parent_version_id: parent.map(id),
        created_at: "now".into(),
        author_kind: "test".into(),
        change_reason: "forget-e2e".into(),
        claims: vec![],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![],
        provenance_refs: vec![],
        content_digest: format!("digest-{version_id}"),
        schema_version: "1".into(),
    }
}

fn forget(key: &str, digest: &str) -> ForgetWrite {
    ForgetWrite {
        memory_id: id("m1"),
        reason: "user request".into(),
        idempotency_key: key.into(),
        request_digest: digest.into(),
    }
}

#[test]
fn forgotten_memory_is_denied_on_read_and_publication() {
    let scope_ref = scope("s1");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store.create_memory(memory("m1", &scope_ref), std::slice::from_ref(&scope_ref)).unwrap();
    store
        .write_revision(
            RevisionWrite {
                memory_id: id("m1"),
                expected_current_version: None,
                revision: revision("m1", "v1", 1, None),
                idempotency_key: "write-1".into(),
                request_digest: "digest-v1".into(),
            },
            std::slice::from_ref(&scope_ref),
        )
        .unwrap();
    assert_eq!(
        store.read_current(&id("m1"), std::slice::from_ref(&scope_ref)).unwrap().unwrap().memory_version_id,
        id("v1")
    );

    let receipt = store.forget_memory(forget("forget-1", "digest-forget-1"), std::slice::from_ref(&scope_ref)).unwrap();
    assert_eq!(receipt.memory_id, id("m1"));

    // Read suppression, including the historical revision (anti-resurrection).
    assert_eq!(store.read_current(&id("m1"), std::slice::from_ref(&scope_ref)).unwrap(), None);
    assert_eq!(store.read_revision(&id("m1"), &id("v1"), std::slice::from_ref(&scope_ref)).unwrap(), None);

    // New publications are suppressed too, and fail closed with the same error a
    // missing Memory produces so the fence leaks no existence signal.
    let blocked = store.write_revision(
        RevisionWrite {
            memory_id: id("m1"),
            expected_current_version: Some(id("v1")),
            revision: revision("m1", "v2", 2, Some("v1")),
            idempotency_key: "write-2".into(),
            request_digest: "digest-v2".into(),
        },
        std::slice::from_ref(&scope_ref),
    );
    assert_eq!(blocked, Err(MemoryStoreError::Storage(StorageError::NotFoundOrNotVisible)));
}

#[test]
fn repeated_forget_is_idempotent_across_keys() {
    let scope_ref = scope("s1");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store.create_memory(memory("m1", &scope_ref), std::slice::from_ref(&scope_ref)).unwrap();

    let first = store.forget_memory(forget("forget-1", "digest-a"), std::slice::from_ref(&scope_ref)).unwrap();
    let replay = store.forget_memory(forget("forget-1", "digest-a"), std::slice::from_ref(&scope_ref)).unwrap();
    assert_eq!(replay, first, "same key + same digest must replay the receipt");

    let other_key = store.forget_memory(forget("forget-2", "digest-b"), std::slice::from_ref(&scope_ref)).unwrap();
    assert_eq!(other_key.fence_generation, first.fence_generation, "a new key must not allocate a new generation");

    assert_eq!(
        store.forget_memory(forget("forget-1", "digest-different"), std::slice::from_ref(&scope_ref)),
        Err(MemoryStoreError::Storage(StorageError::IdempotencyConflict)),
    );
}

#[test]
fn forget_does_not_affect_a_sibling_memory_in_the_same_scope() {
    let scope_ref = scope("s1");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    for memory_id in ["m1", "m2"] {
        store.create_memory(memory(memory_id, &scope_ref), std::slice::from_ref(&scope_ref)).unwrap();
        store
            .write_revision(
                RevisionWrite {
                    memory_id: id(memory_id),
                    expected_current_version: None,
                    revision: revision(memory_id, &format!("{memory_id}-v1"), 1, None),
                    idempotency_key: format!("write-{memory_id}"),
                    request_digest: format!("digest-{memory_id}"),
                },
                std::slice::from_ref(&scope_ref),
            )
            .unwrap();
    }

    store.forget_memory(forget("forget-1", "digest-forget-1"), std::slice::from_ref(&scope_ref)).unwrap();

    // The fence is memory-granular: a namespace-level fence would have wiped m2.
    assert_eq!(store.read_current(&id("m1"), std::slice::from_ref(&scope_ref)).unwrap(), None);
    assert!(store.read_current(&id("m2"), std::slice::from_ref(&scope_ref)).unwrap().is_some());
}

#[test]
fn forget_of_an_unknown_memory_fails_closed() {
    let scope_ref = scope("s1");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    assert_eq!(
        store.forget_memory(forget("forget-1", "digest-forget-1"), std::slice::from_ref(&scope_ref)),
        Err(MemoryStoreError::Storage(StorageError::NotFoundOrNotVisible)),
    );
}
