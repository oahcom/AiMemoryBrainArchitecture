//! Cross-crate negative-path E2E coverage for MemoryStore -> SQLite -> Context.
//!
//! Public-API finding (GAP-06 round 5, case 2): forgetting cannot currently be
//! exercised end-to-end. Neither MemoryStore nor MemoryStorage exposes a
//! forget/tombstone operation; SqliteMemoryStorage has no public equivalent.
//! The exact missing boundary call is a public
//! `MemoryStore::forget_memory(memory_id, scope)` (or an explicitly named
//! lifecycle-transition API) whose successful result makes subsequent
//! `read_current`/Context construction exclude the forgotten memory. Do not
//! simulate this by mutating a ContextCandidate: that would not test Store's
//! forget path.

use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextError, ContextIdentity, ContextTier,
};
use memory_event_store_sqlite::forget_fence::ForgetFence;
use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef,
};
use memory_storage::StorageError;
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, MemoryStoreError, RevisionWrite};
use std::path::{Path, PathBuf};
use std::time::{SystemTime, UNIX_EPOCH};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifiers are non-empty")
}

fn scope(value: &str) -> ScopeRef {
    ScopeRef {
        scope_id: id(&format!("scope-{value}")),
        scope_kind: ScopeKind::User,
        namespace_key: format!("user:{value}"),
    }
}

fn identity(scope: ScopeRef, suffix: &str) -> ContextIdentity {
    ContextIdentity {
        context_id: id(&format!("context-{suffix}")),
        scope_refs: vec![scope],
        agent_id: id("agent-negative-e2e"),
        agent_instance_id: id("agent-instance-negative-e2e"),
        session_id: id("session-negative-e2e"),
        task_id: None,
        environment_id: None,
        purpose: "negative-path-e2e".into(),
        schema_version: "1".into(),
    }
}

fn memory(memory_id: &str, scope: &ScopeRef, lifecycle: MemoryLifecycle) -> Memory {
    Memory {
        memory_id: id(memory_id),
        memory_kind: "semantic".into(),
        scope_refs: vec![scope.clone()],
        current_version_id: None,
        lifecycle_state: lifecycle,
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
    scope: &ScopeRef,
) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id(memory_id),
        version_number,
        parent_version_id: parent_version_id.map(id),
        created_at: "2026-11-21T00:00:00Z".into(),
        author_kind: "negative-e2e".into(),
        change_reason: format!("revision {version_number}"),
        claims: vec![Claim {
            claim_id: id(&format!("claim-{version_id}")),
            subject_ref: id("subject-negative-e2e"),
            predicate: "e2e_state".into(),
            object_value: version_id.into(),
            polarity: "positive".into(),
            epistemic_status: EpistemicStatus::Reported,
            confidence: Some("high".into()),
            temporal_ref: None,
            asserted_at: "2026-11-21T00:00:00Z".into(),
            scope_refs: vec![scope.clone()],
            qualifiers: vec!["negative-e2e".into()],
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
    scope: &ScopeRef,
) {
    store
        .write_revision(
            RevisionWrite {
                memory_id: id(memory_id),
                expected_current_version: expected_current_version.map(id),
                revision: revision(memory_id, version_id, version_number, parent_version_id, scope),
                idempotency_key: format!("op-{version_id}"),
                request_digest: format!("request-{version_id}"),
            },
            std::slice::from_ref(scope),
        )
        .expect("revision write");
}

fn candidate(
    memory_id: &str,
    version: &MemoryVersion,
    lifecycle: MemoryLifecycle,
    entry_id: &str,
) -> ContextCandidate {
    let claim = &version.claims[0];
    ContextCandidate {
        entry_id: id(entry_id),
        memory_id: version.memory_id.clone(),
        memory_version_id: version.memory_version_id.clone(),
        memory_lifecycle: lifecycle,
        scope_refs: claim.scope_refs.clone(),
        tier: ContextTier::P0,
        priority: 100,
        activation_reason: format!("E2E candidate for {memory_id}"),
        rendered_content: format!("{} {}", claim.predicate, claim.object_value),
        source_refs: version.source_refs.clone(),
        evidence_refs: claim.evidence_refs.clone(),
        epistemic_qualifiers: vec![format!("{:?}", claim.epistemic_status)],
        content_hash: version.content_digest.clone(),
    }
}

fn default_budget(max_entries: usize) -> ContextBudget {
    ContextBudget {
        max_entries,
        max_rendered_bytes: 4096,
    }
}

#[test]
fn foreign_scope_cannot_read_or_populate_context() {
    let scope_a = scope("a");
    let scope_b = scope("b");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-scope-a", &scope_a, MemoryLifecycle::Active),
            std::slice::from_ref(&scope_a),
        )
        .unwrap();
    write(
        &mut store,
        "memory-scope-a",
        "version-scope-a",
        1,
        None,
        None,
        &scope_a,
    );

    let denied = store.read_current(&id("memory-scope-a"), std::slice::from_ref(&scope_b));
    assert_eq!(
        denied,
        Err(MemoryStoreError::Storage(StorageError::ScopeMismatch))
    );

    // A denied Store read supplies no candidate; Context must remain empty.
    let snapshot = build_context(
        identity(scope_b, "foreign-scope"),
        1,
        default_budget(4),
        vec![],
    )
    .expect("empty context for a foreign scope");
    assert!(snapshot.is_empty());
}

/// Desired Store-level forget E2E. This remains ignored until the memory-store
/// contract can durably transition a Memory to a forgotten/tombstoned state and
/// ensure reads cannot return it as a context candidate.
#[test]
#[ignore = "unreachable: no public forget API; see GAP-06-FORGET-PATH-UNREACHABLE"]
fn forgotten_memory_is_excluded_from_context() {
    // Intended public flow once the boundary exists:
    // create + write -> MemoryStore::forget_memory(memory_id, scope)
    // -> read_current returns no eligible revision -> build_context is empty.
    // Do not emulate this by editing ContextCandidate.lifecycle.
}

/// Pins the CURRENT (defective) behaviour: a ForgetFence record does not
/// suppress reads through MemoryStore. This test is expected to FAIL the
/// moment forget is wired into the read gate. When it does, delete it and
/// un-ignore `forgotten_memory_is_excluded_from_context`.
#[test]
fn forget_api_absence_is_detectable() {
    let visible_scope = scope("fence-not-wired");
    let temp_db = TempDatabase::new();
    let sqlite = SqliteMemoryStorage::open(temp_db.path()).unwrap();
    let mut store = MemoryStore::new(sqlite);

    store
        .create_memory(
            memory("memory-fence-not-wired", &visible_scope, MemoryLifecycle::Active),
            std::slice::from_ref(&visible_scope),
        )
        .unwrap();
    write(
        &mut store,
        "memory-fence-not-wired",
        "version-fence-not-wired",
        1,
        None,
        None,
        &visible_scope,
    );

    // Use the same physical SQLite database: the fence is present and durable,
    // but today's MemoryStorage read implementation does not consult it.
    let fence = ForgetFence::open(temp_db.path()).unwrap();
    assert_eq!(
        fence
            .record_forget(&visible_scope.namespace_key, "sha256:round7-forget")
            .unwrap(),
        1
    );

    let still_readable = store
        .read_current(
            &id("memory-fence-not-wired"),
            std::slice::from_ref(&visible_scope),
        )
        .unwrap()
        .expect("current behavior: the unconnected fence does not block reads");
    assert_eq!(
        still_readable.memory_version_id,
        id("version-fence-not-wired")
    );

    drop(store.into_storage());
    drop(fence);
    drop(temp_db);
}

#[test]
fn candidate_lifecycle_is_refused_by_context_after_store_round_trip() {
    let visible_scope = scope("candidate");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-candidate", &visible_scope, MemoryLifecycle::Candidate),
            std::slice::from_ref(&visible_scope),
        )
        .unwrap();
    write(
        &mut store,
        "memory-candidate",
        "version-candidate",
        1,
        None,
        None,
        &visible_scope,
    );
    let read_back = store
        .read_current(&id("memory-candidate"), std::slice::from_ref(&visible_scope))
        .unwrap()
        .unwrap();
    let ineligible = candidate(
        "memory-candidate",
        &read_back,
        MemoryLifecycle::Candidate,
        "entry-candidate",
    );

    let error = build_context(
        identity(visible_scope, "candidate"),
        1,
        default_budget(4),
        vec![ineligible],
    )
    .expect_err("Candidate lifecycle must not become a ContextEntry");
    assert_eq!(error, ContextError::IneligibleLifecycle);
}

#[test]
fn mixed_scope_candidate_set_is_rejected_instead_of_filtered() {
    let scope_a = scope("mixed-a");
    let scope_b = scope("mixed-b");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());

    for (memory_id, version_id, item_scope) in [
        ("memory-mixed-a", "version-mixed-a", &scope_a),
        ("memory-mixed-b", "version-mixed-b", &scope_b),
    ] {
        store
            .create_memory(
                memory(memory_id, item_scope, MemoryLifecycle::Active),
                std::slice::from_ref(item_scope),
            )
            .unwrap();
        write(
            &mut store,
            memory_id,
            version_id,
            1,
            None,
            None,
            item_scope,
        );
    }

    let read_a = store
        .read_current(&id("memory-mixed-a"), std::slice::from_ref(&scope_a))
        .unwrap()
        .unwrap();
    let read_b = store
        .read_current(&id("memory-mixed-b"), std::slice::from_ref(&scope_b))
        .unwrap()
        .unwrap();
    let candidates = vec![
        candidate("memory-mixed-a", &read_a, MemoryLifecycle::Active, "entry-mixed-a"),
        candidate("memory-mixed-b", &read_b, MemoryLifecycle::Active, "entry-mixed-b"),
    ];

    let result = build_context(
        identity(scope_a, "mixed-scopes"),
        1,
        default_budget(4),
        candidates,
    );
    assert_eq!(result, Err(ContextError::ScopeMismatch));
}

#[test]
fn stale_revision_is_rejected_and_current_version_remains_n_plus_one() {
    let visible_scope = scope("stale");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    store
        .create_memory(
            memory("memory-stale", &visible_scope, MemoryLifecycle::Active),
            std::slice::from_ref(&visible_scope),
        )
        .unwrap();

    write(
        &mut store,
        "memory-stale",
        "version-stale-1",
        1,
        None,
        None,
        &visible_scope,
    );
    write(
        &mut store,
        "memory-stale",
        "version-stale-2",
        2,
        Some("version-stale-1"),
        Some("version-stale-1"),
        &visible_scope,
    );

    let stale = store.write_revision(
        RevisionWrite {
            memory_id: id("memory-stale"),
            expected_current_version: Some(id("version-stale-1")),
            revision: revision(
                "memory-stale",
                "version-stale-3-stale-parent",
                3,
                Some("version-stale-1"),
                &visible_scope,
            ),
            idempotency_key: "op-stale-parent".into(),
            request_digest: "request-stale-parent".into(),
        },
        std::slice::from_ref(&visible_scope),
    );
    assert_eq!(
        stale,
        Err(MemoryStoreError::Storage(StorageError::StaleVersion))
    );

    let current = store
        .read_current(&id("memory-stale"), std::slice::from_ref(&visible_scope))
        .unwrap()
        .unwrap();
    assert_eq!(current.memory_version_id, id("version-stale-2"));
    assert_eq!(current.version_number, 2);
}

#[test]
fn entry_budget_overflow_reports_actual_and_limit_after_store_reads() {
    let visible_scope = scope("budget");
    let mut store = MemoryStore::new(SqliteMemoryStorage::in_memory().unwrap());
    let mut candidates = Vec::new();

    for index in 1..=2 {
        let memory_id = format!("memory-budget-{index}");
        let version_id = format!("version-budget-{index}");
        store
            .create_memory(
                memory(&memory_id, &visible_scope, MemoryLifecycle::Active),
                std::slice::from_ref(&visible_scope),
            )
            .unwrap();
        write(
            &mut store,
            &memory_id,
            &version_id,
            1,
            None,
            None,
            &visible_scope,
        );
        let read_back = store
            .read_current(&id(&memory_id), std::slice::from_ref(&visible_scope))
            .unwrap()
            .unwrap();
        candidates.push(candidate(
            &memory_id,
            &read_back,
            MemoryLifecycle::Active,
            &format!("entry-budget-{index}"),
        ));
    }

    let error = build_context(
        identity(visible_scope, "budget"),
        1,
        default_budget(1),
        candidates,
    )
    .expect_err("two persisted candidates must exceed a one-entry budget");
    assert_eq!(
        error,
        ContextError::EntryBudgetExceeded {
            actual: 2,
            limit: 1,
        }
    );
}

#[test]
fn rejected_stale_write_remains_rejected_after_file_backed_restart() {
    let visible_scope = scope("stale-restart");
    let temp_db = TempDatabase::new();

    {
        let sqlite = SqliteMemoryStorage::open(temp_db.path()).unwrap();
        let mut store = MemoryStore::new(sqlite);
        store
            .create_memory(
                memory("memory-stale-restart", &visible_scope, MemoryLifecycle::Active),
                std::slice::from_ref(&visible_scope),
            )
            .unwrap();
        write(
            &mut store,
            "memory-stale-restart",
            "version-stale-restart-1",
            1,
            None,
            None,
            &visible_scope,
        );
        write(
            &mut store,
            "memory-stale-restart",
            "version-stale-restart-2",
            2,
            Some("version-stale-restart-1"),
            Some("version-stale-restart-1"),
            &visible_scope,
        );

        let rejected = store.write_revision(
            RevisionWrite {
                memory_id: id("memory-stale-restart"),
                expected_current_version: Some(id("version-stale-restart-1")),
                revision: revision(
                    "memory-stale-restart",
                    "version-stale-restart-3-stale-parent",
                    3,
                    Some("version-stale-restart-1"),
                    &visible_scope,
                ),
                idempotency_key: "op-stale-restart".into(),
                request_digest: "request-stale-restart".into(),
            },
            std::slice::from_ref(&visible_scope),
        );
        assert_eq!(
            rejected,
            Err(MemoryStoreError::Storage(StorageError::StaleVersion))
        );

        drop(store.into_storage());
    }

    let sqlite = SqliteMemoryStorage::open(temp_db.path()).unwrap();
    let store = MemoryStore::new(sqlite);
    let current = store
        .read_current(&id("memory-stale-restart"), std::slice::from_ref(&visible_scope))
        .unwrap()
        .unwrap();
    assert_eq!(current.memory_version_id, id("version-stale-restart-2"));
    assert_eq!(current.version_number, 2);

    drop(store.into_storage());
    drop(temp_db);
}

struct TempDatabase(PathBuf);

impl TempDatabase {
    fn new() -> Self {
        let nonce = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("system clock after Unix epoch")
            .as_nanos();
        let filename = format!(
            "ai-memory-gap06-negative-{}-{nonce}.sqlite",
            std::process::id()
        );
        Self(std::env::temp_dir().join(filename))
    }

    fn path(&self) -> &Path {
        &self.0
    }
}

impl Drop for TempDatabase {
    fn drop(&mut self) {
        let _ = std::fs::remove_file(&self.0);
        let wal = PathBuf::from(format!("{}-wal", self.0.display()));
        let shm = PathBuf::from(format!("{}-shm", self.0.display()));
        let _ = std::fs::remove_file(wal);
        let _ = std::fs::remove_file(shm);
    }
}

#[test]
fn file_backed_sqlite_survives_storage_handle_restart() {
    let visible_scope = scope("restart");
    let temp_db = TempDatabase::new();

    {
        let sqlite = SqliteMemoryStorage::open(temp_db.path()).unwrap();
        let mut store = MemoryStore::new(sqlite);
        store
            .create_memory(
                memory("memory-restart", &visible_scope, MemoryLifecycle::Active),
                std::slice::from_ref(&visible_scope),
            )
            .unwrap();
        write(
            &mut store,
            "memory-restart",
            "version-restart",
            1,
            None,
            None,
            &visible_scope,
        );

        // Explicitly drop the storage connection before reopening/unlinking.
        drop(store.into_storage());
    }

    let sqlite = SqliteMemoryStorage::open(temp_db.path()).unwrap();
    let store = MemoryStore::new(sqlite);
    let read_back = store
        .read_current(&id("memory-restart"), std::slice::from_ref(&visible_scope))
        .unwrap()
        .expect("file-backed revision must survive connection restart");
    let persisted_candidate = candidate(
        "memory-restart",
        &read_back,
        MemoryLifecycle::Active,
        "entry-restart",
    );
    let snapshot = build_context(
        identity(visible_scope, "restart"),
        1,
        default_budget(4),
        vec![persisted_candidate],
    )
    .expect("reopened persisted revision must build context");
    assert_eq!(snapshot.entries.len(), 1);
    assert_eq!(
        snapshot.entries[0].memory_version_id,
        id("version-restart")
    );

    drop(store.into_storage());
    drop(temp_db);
}
