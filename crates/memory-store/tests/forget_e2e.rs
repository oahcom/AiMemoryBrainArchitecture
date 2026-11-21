//! Store-level forget E2E through the real SQLite adapter (no Context layer).

use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef,
};
use memory_storage::StorageError;
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, MemoryStoreError, RevisionWrite};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifiers are non-empty")
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-forget-e2e"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:forget-e2e".into(),
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

fn revision(
    memory_id: &str,
    version_id: &str,
    version_number: u64,
    parent_version_id: Option<&str>,
    s: &ScopeRef,
) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id(memory_id),
        version_number,
        parent_version_id: parent_version_id.map(id),
        created_at: "2026-11-22T00:00:00Z".into(),
        author_kind: "forget-e2e".into(),
        change_reason: format!("revision {version_number}"),
        claims: vec![Claim {
            claim_id: id(&format!("claim-{version_id}")),
            subject_ref: id("subject-forget-e2e"),
            predicate: "e2e_state".into(),
            object_value: version_id.into(),
            polarity: "positive".into(),
            epistemic_status: EpistemicStatus::Reported,
            confidence: Some("high".into()),
            temporal_ref: None,
            asserted_at: "2026-11-22T00:00:00Z".into(),
            scope_refs: vec![s.clone()],
            qualifiers: vec!["forget-e2e".into()],
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

fn write(
    store: &mut MemoryStore<SqliteMemoryStorage>,
    memory_id: &str,
    version_id: &str,
    version_number: u64,
    parent_version_id: Option<&str>,
    expected_current_version: Option<&str>,
    s: &ScopeRef,
) {
    store
        .write_revision(
            RevisionWrite {
                memory_id: id(memory_id),
                expected_current_version: expected_current_version.map(id),
                revision: revision(memory_id, version_id, version_number, parent_version_id, s),
                idempotency_key: format!("op-{version_id}"),
                request_digest: format!("request-{version_id}"),
            },
            std::slice::from_ref(s),
        )
        .expect("revision write");
}

#[test]
fn forget_memory_on_unknown_memory_fails_closed_at_storage() {
    let s = scope();
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());

    let result = store.forget_memory(
        &id("memory-missing"),
        "sha256:unknown",
        std::slice::from_ref(&s),
    );

    assert_eq!(
        result,
        Err(MemoryStoreError::Storage(
            StorageError::NotFoundOrNotVisible
        ))
    );
}

#[test]
fn forgetting_one_memory_leaves_its_sibling_in_the_same_scope_readable() {
    let s = scope();
    let scope_slice = std::slice::from_ref(&s);
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());

    for (memory_id, version_id) in [
        ("memory-forgotten", "version-forgotten"),
        ("memory-sibling", "version-sibling"),
    ] {
        store
            .create_memory(memory(memory_id, &s), scope_slice)
            .unwrap();
        write(&mut store, memory_id, version_id, 1, None, None, &s);
    }

    store
        .forget_memory(&id("memory-forgotten"), "sha256:forget-one", scope_slice)
        .expect("forget one memory");

    assert_eq!(
        store.read_current(&id("memory-forgotten"), scope_slice),
        Ok(None)
    );
    let sibling = store
        .read_current(&id("memory-sibling"), scope_slice)
        .expect("sibling read succeeds")
        .expect("sibling memory stays visible");
    assert_eq!(sibling.memory_version_id, id("version-sibling"));
    assert_eq!(
        store.read_revision(&id("memory-sibling"), &id("version-sibling"), scope_slice),
        Ok(Some(sibling))
    );
}

#[test]
fn forget_version_fences_only_that_version_and_the_sibling_version_stays_readable() {
    let s = scope();
    let scope_slice = std::slice::from_ref(&s);
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());

    store
        .create_memory(memory("memory-versions", &s), scope_slice)
        .unwrap();
    write(
        &mut store,
        "memory-versions",
        "version-1",
        1,
        None,
        None,
        &s,
    );
    write(
        &mut store,
        "memory-versions",
        "version-2",
        2,
        Some("version-1"),
        Some("version-1"),
        &s,
    );

    store
        .forget_version(
            &id("memory-versions"),
            &id("version-1"),
            "sha256:forget-version-1",
            scope_slice,
        )
        .expect("forget one version");

    // The fenced version is unreadable (read_version_row excludes Version fences).
    assert_eq!(
        store.read_revision(&id("memory-versions"), &id("version-1"), scope_slice),
        Ok(None)
    );

    // Actual main behavior: SQLite read_version_row filters only the memory fence
    // and the requested version's own fence. Parent lineage is consulted by
    // ensure_not_forgotten on WRITE paths only, so the sibling version-2 (whose
    // parent is the fenced version-1) REMAINS readable. Pin the real behavior.
    let sibling = store
        .read_revision(&id("memory-versions"), &id("version-2"), scope_slice)
        .expect("sibling version read succeeds")
        .expect("sibling version stays readable after its parent is fenced");
    assert_eq!(sibling.memory_version_id, id("version-2"));
    assert_eq!(sibling.parent_version_id, Some(id("version-1")));

    // The memory itself is not fenced by forget_version, so read_current still works.
    assert_eq!(
        store.read_current(&id("memory-versions"), scope_slice),
        Ok(Some(sibling))
    );
}
