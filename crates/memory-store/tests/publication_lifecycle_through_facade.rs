//! Publication lifecycle through the `MemoryStore` facade, against real SQLite.
//!
//! GAP-14-A: `prepare_version` / `publish_prepared` / `publication_state` used to
//! exist only on the storage trait (and on the test `FakeStorage`). These tests
//! drive the same three calls through `MemoryStore<SqliteMemoryStorage>`.

use std::path::PathBuf;

use memory_domain::{Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef};
use memory_storage::{PrepareRequest, PublicationState, StorageError};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, MemoryStoreError, RevisionWrite};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifiers are non-empty")
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-publication-facade"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:publication-facade".into(),
    }
}

fn memory() -> Memory {
    Memory {
        memory_id: id("m1"),
        memory_kind: "semantic".into(),
        scope_refs: vec![scope()],
        current_version_id: None,
        lifecycle_state: MemoryLifecycle::Active,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "2026-11-22T00:00:00Z".into(),
        updated_at: "2026-11-22T00:00:00Z".into(),
    }
}

fn revision(version_id: &str, version_number: u64, parent: Option<&str>) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id("m1"),
        version_number,
        parent_version_id: parent.map(id),
        created_at: "2026-11-22T00:00:00Z".into(),
        author_kind: "publication-facade".into(),
        change_reason: format!("revision {version_number}"),
        claims: vec![],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![],
        provenance_refs: vec![],
        content_digest: format!("sha256:{version_id}"),
        schema_version: "1".into(),
    }
}

fn prepare(version_id: &str, version_number: u64, parent: Option<&str>) -> PrepareRequest {
    PrepareRequest {
        memory_id: id("m1"),
        expected_current_version: parent.map(id),
        new_version: revision(version_id, version_number, parent),
        idempotency_key: format!("op-{version_id}"),
        request_digest: format!("digest-{version_id}"),
        publication_id: format!("pub-{version_id}"),
        generation: 1,
    }
}

/// A throwaway SQLite file: a real database on disk, removed with its sidecars.
struct TempDb {
    dir: PathBuf,
}

impl TempDb {
    fn new(label: &str) -> Self {
        let dir = std::env::temp_dir().join(format!(
            "memory-store-publication-{label}-{}",
            std::process::id()
        ));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).expect("temp dir is creatable");
        Self { dir }
    }

    fn store(&self) -> MemoryStore<SqliteMemoryStorage> {
        MemoryStore::new(SqliteMemoryStorage::open(self.dir.join("memory.sqlite")).expect("opens"))
    }
}

impl Drop for TempDb {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.dir);
    }
}

#[test]
fn prepare_stays_hidden_until_publish_through_the_facade() {
    let db = TempDb::new("prepare-publish");
    let mut store = db.store();
    store.create_memory(memory(), &[scope()]).unwrap();

    let receipt = store
        .prepare_version(prepare("v1", 1, None), &[scope()])
        .expect("prepare succeeds against real SQLite");
    assert_eq!(receipt.prepared_version_id, id("v1"));
    assert_eq!(receipt.publication_id, "pub-v1");

    // Staged but not readable: neither the pointer nor the version is visible.
    assert_eq!(
        store.publication_state("pub-v1", &[scope()]).unwrap(),
        Some(PublicationState::PreparedHidden)
    );
    assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
    assert!(store
        .read_revision(&id("m1"), &id("v1"), &[scope()])
        .unwrap()
        .is_none());

    let published = store
        .publish_prepared("pub-v1", None, &[scope()])
        .expect("publish succeeds");
    assert_eq!(published.resulting_version_id, id("v1"));

    assert_eq!(
        store.publication_state("pub-v1", &[scope()]).unwrap(),
        Some(PublicationState::Published)
    );
    let current = store
        .read_current(&id("m1"), &[scope()])
        .unwrap()
        .expect("published version becomes current");
    assert_eq!(current.memory_version_id, id("v1"));
    assert!(store
        .read_revision(&id("m1"), &id("v1"), &[scope()])
        .unwrap()
        .is_some());
}

#[test]
fn publish_rejects_a_stale_expected_current_version() {
    let db = TempDb::new("stale-fence");
    let mut store = db.store();
    store.create_memory(memory(), &[scope()]).unwrap();

    assert_eq!(
        store.publish_prepared("pub-absent", None, &[scope()]),
        Err(MemoryStoreError::Storage(
            StorageError::NotFoundOrNotVisible
        ))
    );

    store
        .prepare_version(prepare("v1", 1, None), &[scope()])
        .unwrap();
    store.publish_prepared("pub-v1", None, &[scope()]).unwrap();

    // Prepare a successor against v1, then let a competing commit advance the
    // pointer: the prepared publication is now stale.
    store
        .prepare_version(prepare("v2", 2, Some("v1")), &[scope()])
        .unwrap();
    store
        .write_revision(
            RevisionWrite {
                memory_id: id("m1"),
                expected_current_version: Some(id("v1")),
                revision: revision("v3", 2, Some("v1")),
                idempotency_key: "op-v3".into(),
                request_digest: "digest-v3".into(),
            },
            &[scope()],
        )
        .unwrap();

    assert_eq!(
        store.publish_prepared("pub-v2", Some(id("v1")), &[scope()]),
        Err(MemoryStoreError::Storage(StorageError::StaleVersion)),
        "a stale fence must be rejected, not silently accepted"
    );
    // A wrong-but-current fence is rejected too: it must match the prepared value.
    assert_eq!(
        store.publish_prepared("pub-v2", Some(id("v3")), &[scope()]),
        Err(MemoryStoreError::Storage(StorageError::StaleVersion))
    );
    assert_eq!(
        store.publication_state("pub-v2", &[scope()]).unwrap(),
        Some(PublicationState::PreparedHidden),
        "a rejected publish leaves the preparation hidden"
    );
    assert_eq!(
        store
            .read_current(&id("m1"), &[scope()])
            .unwrap()
            .unwrap()
            .memory_version_id,
        id("v3")
    );

    // Facade-level scope validation runs before the storage call.
    assert_eq!(
        store.publication_state("pub-v2", &[]),
        Err(MemoryStoreError::InvalidDomain(
            memory_domain::DomainError::EmptyRequiredField("scope")
        ))
    );
}
