//! Full pipeline end-to-end: store write -> compile -> context build -> file
//! adapter -> read back from a freshly opened adapter.
//!
//! The other E2E tests stop at one boundary (store -> context, or
//! context -> adapter). This one runs the whole chain once, and proves the
//! delivered snapshot survives adapter re-open by comparing it byte-for-byte
//! with the snapshot that was built.
//!
//! Lives in `brain-cli` rather than `memory-context` because only this crate
//! depends on the store, the context builder, and the delivery adapter at once.

use agent_integration::{
    ApplyOutcome, ContextDeliveryAdapter, DeliveryPayload, FileContextDeliveryAdapter,
};
use memory_context::{
    build_context, select_within_budget, ContextBudget, ContextCandidate, ContextIdentity,
    ContextSnapshot, ContextTier,
};
use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef,
};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, RevisionWrite};
use std::fs;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};

const SESSION_ID: &str = "session-pipeline-001";
const TIMESTAMP: &str = "2026-11-22T00:00:00Z";

static NEXT_ID: AtomicU64 = AtomicU64::new(0);

struct TestDirectory {
    path: PathBuf,
}

impl TestDirectory {
    fn new() -> Self {
        let id = NEXT_ID.fetch_add(1, Ordering::Relaxed);
        let path = std::env::temp_dir().join(format!(
            "brain-cli-full-pipeline-{}-{id}",
            std::process::id()
        ));
        fs::create_dir_all(&path).expect("create test directory");
        Self { path }
    }

    fn store_path(&self) -> PathBuf {
        self.path.join("memory.sqlite")
    }

    fn delivery_root(&self) -> PathBuf {
        self.path.join("delivered")
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
        scope_id: id("scope-user-pipeline"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:pipeline".into(),
    }
}

fn identity() -> ContextIdentity {
    ContextIdentity {
        context_id: id("context-pipeline"),
        scope_refs: vec![scope()],
        agent_id: id("agent-pipeline"),
        agent_instance_id: id("agent-instance-pipeline"),
        session_id: id(SESSION_ID),
        task_id: Some(id("task-pipeline")),
        environment_id: None,
        purpose: "full-pipeline-e2e".into(),
        schema_version: "1".into(),
    }
}

fn budget() -> ContextBudget {
    ContextBudget {
        max_entries: 8,
        max_rendered_bytes: 4096,
    }
}

/// Persist one Memory plus its first revision through the real store.
fn seed(store: &mut MemoryStore<SqliteMemoryStorage>, scope_refs: &[ScopeRef], n: u32) -> OpaqueId {
    let memory_id = id(&format!("memory-{n}"));

    store
        .create_memory(
            Memory {
                memory_id: memory_id.clone(),
                memory_kind: "semantic".into(),
                scope_refs: scope_refs.to_vec(),
                current_version_id: None,
                // Context planning admits Active and Consolidated memories.
                lifecycle_state: MemoryLifecycle::Active,
                retention_class: "default".into(),
                sensitivity: "normal".into(),
                created_at: TIMESTAMP.into(),
                updated_at: TIMESTAMP.into(),
            },
            scope_refs,
        )
        .expect("persist memory through MemoryStore");

    let source_id = id(&format!("source-{n}"));
    store
        .write_revision(
            RevisionWrite {
                memory_id: memory_id.clone(),
                expected_current_version: None,
                revision: MemoryVersion {
                    memory_version_id: id(&format!("memory-version-{n}")),
                    memory_id: memory_id.clone(),
                    version_number: 1,
                    parent_version_id: None,
                    created_at: TIMESTAMP.into(),
                    author_kind: "integration-test".into(),
                    change_reason: "full pipeline fixture".into(),
                    claims: vec![Claim {
                        claim_id: id(&format!("claim-{n}")),
                        subject_ref: id("project-pipeline"),
                        predicate: format!("fact_{n}"),
                        object_value: format!("value_{n}"),
                        polarity: "positive".into(),
                        epistemic_status: EpistemicStatus::Reported,
                        confidence: Some("high".into()),
                        temporal_ref: None,
                        asserted_at: TIMESTAMP.into(),
                        scope_refs: scope_refs.to_vec(),
                        qualifiers: vec!["integration-test".into()],
                        evidence_refs: vec![source_id.clone()],
                    }],
                    entity_refs: vec![],
                    relation_refs: vec![],
                    source_refs: vec![source_id],
                    provenance_refs: vec![],
                    content_digest: format!("sha256:pipeline-{n}"),
                    schema_version: "1".into(),
                },
                idempotency_key: format!("idempotency-pipeline-{n}"),
                request_digest: format!("sha256:request-pipeline-{n}"),
            },
            scope_refs,
        )
        .expect("commit first revision through MemoryStore");

    memory_id
}

/// Read the current revision back out of the store and turn it into a context
/// candidate, exactly as the compiler read path does.
fn candidate_from_store(
    store: &MemoryStore<SqliteMemoryStorage>,
    memory_id: &OpaqueId,
    scope_refs: &[ScopeRef],
) -> ContextCandidate {
    let current = store
        .read_current(memory_id, scope_refs)
        .expect("read current revision")
        .expect("committed current revision must exist");
    let claim = current
        .claims
        .first()
        .expect("stored revision carries a Claim");

    ContextCandidate {
        entry_id: claim.claim_id.clone(),
        memory_id: current.memory_id.clone(),
        memory_version_id: current.memory_version_id.clone(),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: claim.scope_refs.clone(),
        tier: ContextTier::P0,
        priority: 0,
        activation_reason: "persisted memory selected by full-pipeline E2E".into(),
        rendered_content: format!("{} {}", claim.predicate, claim.object_value),
        source_refs: current.source_refs.clone(),
        evidence_refs: claim.evidence_refs.clone(),
        epistemic_qualifiers: claim.qualifiers.clone(),
        content_hash: current.content_digest.clone(),
    }
}

fn candidates_from_store(
    store: &MemoryStore<SqliteMemoryStorage>,
    memory_ids: &[OpaqueId],
    scope_refs: &[ScopeRef],
) -> Vec<ContextCandidate> {
    memory_ids
        .iter()
        .map(|memory_id| candidate_from_store(store, memory_id, scope_refs))
        .collect()
}

#[test]
fn store_write_to_context_to_file_adapter_survives_reopen() {
    let directory = TestDirectory::new();
    let scope_refs = vec![scope()];
    let mut store = MemoryStore::new(
        SqliteMemoryStorage::open(directory.store_path()).expect("open real SQLite store"),
    );

    let memory_ids: Vec<OpaqueId> = (1..=3).map(|n| seed(&mut store, &scope_refs, n)).collect();

    // Compile: persisted revisions become context candidates.
    let candidates = candidates_from_store(&store, &memory_ids, &scope_refs);
    assert_eq!(candidates.len(), 3);

    let selection =
        select_within_budget(&identity(), &budget(), candidates).expect("select within budget");
    assert_eq!(
        selection.selected.len(),
        3,
        "budget admits every persisted memory"
    );

    let snapshot = build_context(identity(), 1, budget(), selection.selected)
        .expect("build context from persisted revisions");
    assert_eq!(snapshot.entries.len(), 3);
    assert_eq!(
        snapshot
            .entries
            .iter()
            .map(|entry| entry.memory_version_id.as_str().to_owned())
            .collect::<Vec<_>>(),
        vec![
            "memory-version-1".to_owned(),
            "memory-version-2".to_owned(),
            "memory-version-3".to_owned()
        ],
        "every entry carries the version id the store committed"
    );

    // Deliver through the file-backed adapter.
    let delivery_root = directory.delivery_root();
    let mut adapter =
        FileContextDeliveryAdapter::open(&delivery_root).expect("open file delivery adapter");
    let payload = DeliveryPayload::from_snapshot(&snapshot).expect("payload from snapshot");

    assert_eq!(
        adapter
            .apply(SESSION_ID, payload)
            .expect("apply delivery to file adapter"),
        ApplyOutcome::Applied
    );
    assert_eq!(
        adapter
            .applied_snapshot(SESSION_ID)
            .map(DeliveryPayload::version),
        Some(snapshot.context_version)
    );
    drop(adapter);

    // A brand-new adapter instance must recover the delivery from disk.
    let mut reopened =
        FileContextDeliveryAdapter::open(&delivery_root).expect("reopen file delivery adapter");
    let applied = reopened
        .applied_snapshot(SESSION_ID)
        .expect("reopened adapter must read the applied snapshot");

    assert_eq!(
        applied.version(),
        snapshot.context_version,
        "delivered version must survive adapter re-open"
    );

    let restored: ContextSnapshot =
        serde_json::from_str(applied.content()).expect("delivered content is a ContextSnapshot");
    assert_eq!(
        restored, snapshot,
        "the read-back snapshot must equal the snapshot that was built"
    );
    assert_eq!(
        reopened.reconnect(SESSION_ID).expect("reconnect session"),
        Some(snapshot.context_version),
        "reconnect reports the last applied version"
    );
    assert!(
        delivery_root.join(format!("{SESSION_ID}.json")).is_file(),
        "each session must persist one record under the delivery root"
    );
}

#[test]
fn forgetting_a_memory_drops_it_from_the_rebuilt_snapshot() {
    let directory = TestDirectory::new();
    let scope_refs = vec![scope()];
    let mut store = MemoryStore::new(
        SqliteMemoryStorage::open(directory.store_path()).expect("open real SQLite store"),
    );

    let memory_ids: Vec<OpaqueId> = (1..=3).map(|n| seed(&mut store, &scope_refs, n)).collect();

    let before = build_context(
        identity(),
        1,
        budget(),
        candidates_from_store(&store, &memory_ids, &scope_refs),
    )
    .expect("build initial snapshot");
    assert_eq!(before.entries.len(), 3);

    let forgotten = memory_ids[1].as_str().to_owned();
    store
        .forget_memory(&memory_ids[1], "sha256:forget-reason", &scope_refs)
        .expect("forget one memory");

    assert!(
        store
            .read_current(&memory_ids[1], &scope_refs)
            .expect("read after forget")
            .is_none(),
        "a forgotten memory is unobservable through reads"
    );

    let survivors: Vec<OpaqueId> = memory_ids
        .iter()
        .filter(|memory_id| memory_id.as_str() != forgotten)
        .cloned()
        .collect();

    let after = build_context(
        identity(),
        2,
        budget(),
        candidates_from_store(&store, &survivors, &scope_refs),
    )
    .expect("rebuild snapshot after forget");

    assert_eq!(after.entries.len(), 2);
    assert!(
        after
            .entries
            .iter()
            .all(|entry| entry.memory_id.as_str() != forgotten),
        "the forgotten memory must not appear in the rebuilt snapshot"
    );
}
