//! Real Store -> SQLite -> Context integration test.
//!
//! This exercises the public Rust module boundary with a real in-memory SQLite
//! database. The rendered context text is derived from the persisted Claim;
//! MemoryVersion intentionally has no standalone `content` field.

use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextError, ContextIdentity, ContextTier,
};
use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeRef,
};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, RevisionWrite};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifiers are non-empty")
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-user-e2e"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:e2e".into(),
    }
}

fn context_identity(scope: ScopeRef) -> ContextIdentity {
    ContextIdentity {
        context_id: id("context-e2e"),
        scope_refs: vec![scope],
        agent_id: id("agent-e2e"),
        agent_instance_id: id("agent-instance-e2e"),
        session_id: id("session-e2e"),
        task_id: Some(id("task-e2e")),
        environment_id: None,
        purpose: "store-to-context-e2e".into(),
        schema_version: "1".into(),
    }
}

#[test]
fn sqlite_store_read_current_builds_context_from_persisted_revision() {
    let scope = scope();
    let scope_refs = vec![scope.clone()];
    let memory_id = id("memory-e2e");
    let version_id = id("memory-version-e2e");
    let source_id = id("source-e2e");

    let memory = Memory {
        memory_id: memory_id.clone(),
        memory_kind: "semantic".into(),
        scope_refs: scope_refs.clone(),
        current_version_id: None,
        // Context planning admits Active and Consolidated memories.
        lifecycle_state: MemoryLifecycle::Active,
        retention_class: "default".into(),
        sensitivity: "normal".into(),
        created_at: "2026-11-21T00:00:00Z".into(),
        updated_at: "2026-11-21T00:00:00Z".into(),
    };

    let claim = Claim {
        claim_id: id("claim-e2e"),
        subject_ref: id("project-e2e"),
        predicate: "project_status".into(),
        object_value: "ready".into(),
        polarity: "positive".into(),
        epistemic_status: EpistemicStatus::Reported,
        confidence: Some("high".into()),
        temporal_ref: None,
        asserted_at: "2026-11-21T00:00:00Z".into(),
        scope_refs: scope_refs.clone(),
        qualifiers: vec!["integration-test".into()],
        evidence_refs: vec![source_id.clone()],
    };

    let written_version = MemoryVersion {
        memory_version_id: version_id.clone(),
        memory_id: memory_id.clone(),
        version_number: 1,
        parent_version_id: None,
        created_at: "2026-11-21T00:00:00Z".into(),
        author_kind: "integration-test".into(),
        change_reason: "initial E2E fixture".into(),
        claims: vec![claim],
        entity_refs: vec![],
        relation_refs: vec![],
        source_refs: vec![source_id],
        provenance_refs: vec![],
        content_digest: "sha256:e2e-memory-content".into(),
        schema_version: "1".into(),
    };

    let sqlite = SqliteMemoryStorage::in_memory().expect("open real in-memory SQLite");
    let mut store = MemoryStore::new(sqlite);

    store
        .create_memory(memory, &scope_refs)
        .expect("persist memory through MemoryStore");

    let receipt = store
        .write_revision(
            RevisionWrite {
                memory_id: memory_id.clone(),
                expected_current_version: None,
                revision: written_version.clone(),
                idempotency_key: "idempotency-e2e-1".into(),
                request_digest: "sha256:e2e-request".into(),
            },
            &scope_refs,
        )
        .expect("commit first revision through MemoryStore");

    assert_eq!(receipt.resulting_version_id, version_id);

    let read_back = store
        .read_current(&memory_id, &scope_refs)
        .expect("read current revision")
        .expect("committed current revision must exist");

    // Verify the real SQLite round-trip, including identity, scope and claims.
    assert_eq!(read_back, written_version);
    assert_eq!(read_back.memory_version_id, version_id);
    assert_eq!(read_back.memory_id, memory_id);
    assert_eq!(read_back.claims[0].scope_refs, scope_refs);

    // Context text is derived from the actual persisted Claim, not a mock.
    let claim = &read_back.claims[0];
    let rendered_content = format!("{} {}", claim.predicate, claim.object_value);
    let candidate = ContextCandidate {
        entry_id: id("context-entry-e2e"),
        memory_id: read_back.memory_id.clone(),
        memory_version_id: read_back.memory_version_id.clone(),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: claim.scope_refs.clone(),
        tier: ContextTier::P0,
        priority: 100,
        activation_reason: "persisted memory selected by E2E test".into(),
        rendered_content,
        source_refs: read_back.source_refs.clone(),
        evidence_refs: claim.evidence_refs.clone(),
        epistemic_qualifiers: vec![format!("{:?}", claim.epistemic_status)],
        content_hash: read_back.content_digest.clone(),
    };

    let identity = context_identity(scope);
    let snapshot = build_context(
        identity.clone(),
        1,
        ContextBudget {
            max_entries: 4,
            max_rendered_bytes: 128,
        },
        vec![candidate.clone()],
    )
    .expect("build context from persisted revision");

    assert_eq!(snapshot.entries.len(), 1);
    assert_eq!(snapshot.entries[0].memory_id, memory_id);
    assert_eq!(snapshot.entries[0].memory_version_id, version_id);
    assert_eq!(snapshot.entries[0].rendered_content, "project_status ready");
    assert_eq!(snapshot.identity.scope_refs, scope_refs);

    // A zero budget is a contract error, not a panic or silent empty result.
    let error = build_context(
        identity,
        1,
        ContextBudget {
            max_entries: 0,
            max_rendered_bytes: 128,
        },
        vec![candidate],
    )
    .expect_err("zero-entry budget must be rejected");
    assert_eq!(error, ContextError::InvalidBudget);
}
