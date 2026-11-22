//! GAP-06: a forgotten memory must not reach the compiled Context.
//!
//! Drives the public boundary only: `MemoryStore<SqliteMemoryStorage>` for
//! persistence and forgetting, `read_current` for visibility, and
//! `build_context` for compilation. No test reaches into the fence table, and
//! no production symbol is stubbed.

use std::path::PathBuf;

use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextTier,
};
use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeKind, ScopeRef,
};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, RevisionWrite};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifiers are non-empty")
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-gap06"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:gap06".into(),
    }
}

fn identity(s: &ScopeRef) -> ContextIdentity {
    ContextIdentity {
        context_id: id("context-gap06"),
        scope_refs: vec![s.clone()],
        agent_id: id("agent-gap06"),
        agent_instance_id: id("agent-instance-gap06"),
        session_id: id("session-gap06"),
        task_id: None,
        environment_id: None,
        purpose: "gap06-forget-e2e".into(),
        schema_version: "1".into(),
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

fn revision(memory_id: &str, version_id: &str, object_value: &str, s: &ScopeRef) -> MemoryVersion {
    MemoryVersion {
        memory_version_id: id(version_id),
        memory_id: id(memory_id),
        version_number: 1,
        parent_version_id: None,
        created_at: "2026-11-22T00:00:00Z".into(),
        author_kind: "gap06-forget-e2e".into(),
        change_reason: "initial revision".into(),
        claims: vec![Claim {
            claim_id: id(&format!("claim-{version_id}")),
            subject_ref: id("subject-gap06"),
            predicate: "state".into(),
            object_value: object_value.into(),
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

fn seed(
    store: &mut MemoryStore<SqliteMemoryStorage>,
    memory_id: &str,
    version_id: &str,
    object_value: &str,
    s: &ScopeRef,
) {
    store
        .create_memory(memory(memory_id, s), std::slice::from_ref(s))
        .expect("create memory through MemoryStore");
    store
        .write_revision(
            RevisionWrite {
                memory_id: id(memory_id),
                expected_current_version: None,
                revision: revision(memory_id, version_id, object_value, s),
                idempotency_key: format!("op-{version_id}"),
                request_digest: format!("request-{version_id}"),
            },
            std::slice::from_ref(s),
        )
        .expect("commit revision through MemoryStore");
}

/// Compile a context from whatever the store still considers visible for
/// `memory_ids`. This is the same composition `brain-cli` performs: read the
/// current revision, project it into a candidate, then compile.
fn compile(
    store: &MemoryStore<SqliteMemoryStorage>,
    memory_ids: &[&str],
    s: &ScopeRef,
) -> memory_context::ContextSnapshot {
    let candidates: Vec<ContextCandidate> = memory_ids
        .iter()
        .filter_map(|memory_id| {
            let current = store
                .read_current(&id(memory_id), std::slice::from_ref(s))
                .expect("read_current succeeds")?;
            let claim = current.claims.first().expect("revision carries a claim");
            Some(ContextCandidate {
                entry_id: claim.claim_id.clone(),
                memory_id: current.memory_id.clone(),
                memory_version_id: current.memory_version_id.clone(),
                memory_lifecycle: MemoryLifecycle::Active,
                scope_refs: claim.scope_refs.clone(),
                tier: ContextTier::P0,
                priority: 100,
                activation_reason: "gap06 fixture".into(),
                rendered_content: format!("{} {}", claim.predicate, claim.object_value),
                source_refs: current.source_refs.clone(),
                evidence_refs: claim.evidence_refs.clone(),
                epistemic_qualifiers: vec![],
                content_hash: current.content_digest.clone(),
            })
        })
        .collect();

    build_context(
        identity(s),
        1,
        ContextBudget {
            max_entries: 16,
            max_rendered_bytes: 4096,
        },
        candidates,
    )
    .expect("build context from persisted revisions")
}

struct TempDb {
    dir: PathBuf,
}

impl TempDb {
    fn new(label: &str) -> Self {
        let dir = std::env::temp_dir().join(format!(
            "memory-context-forget-{label}-{}",
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
fn a_forgotten_memory_does_not_reach_the_compiled_context() {
    let db = TempDb::new("excludes-from-context");
    let s = scope();
    let scope_slice = std::slice::from_ref(&s);
    let mut store = db.store();

    seed(
        &mut store,
        "memory-forgotten",
        "version-forgotten",
        "secret",
        &s,
    );
    seed(
        &mut store,
        "memory-sibling",
        "version-sibling",
        "public",
        &s,
    );

    // Baseline: both memories are visible, so the context is non-empty.
    let before = compile(&store, &["memory-forgotten", "memory-sibling"], &s);
    assert_eq!(
        before.entries.len(),
        2,
        "baseline context admits both memories"
    );
    assert!(before
        .entries
        .iter()
        .any(|entry| entry.memory_id == id("memory-forgotten")));
    assert!(before
        .entries
        .iter()
        .any(|entry| entry.memory_id == id("memory-sibling")));

    store
        .forget_memory(&id("memory-forgotten"), "sha256:gap06-forget", scope_slice)
        .expect("forget one memory through the facade");

    // The forgotten memory no longer compiles into the context ...
    let after = compile(&store, &["memory-forgotten", "memory-sibling"], &s);
    assert_eq!(
        after.entries.len(),
        1,
        "only the sibling remains in context"
    );
    assert!(
        !after
            .entries
            .iter()
            .any(|entry| entry.memory_id == id("memory-forgotten")),
        "a forgotten memory must not reach the compiled context"
    );
    assert!(
        after
            .entries
            .iter()
            .any(|entry| entry.memory_id == id("memory-sibling")),
        "forgetting one memory must not evict its sibling"
    );
    assert!(
        !after
            .entries
            .iter()
            .any(|entry| entry.rendered_content.contains("secret")),
        "no rendered content may survive from the forgotten memory"
    );
}

#[test]
fn a_forgotten_memory_is_unreachable_through_read_current_and_read_revision() {
    let db = TempDb::new("unreachable-reads");
    let s = scope();
    let scope_slice = std::slice::from_ref(&s);
    let mut store = db.store();

    seed(
        &mut store,
        "memory-forgotten",
        "version-forgotten",
        "secret",
        &s,
    );

    // Reachable before the forget.
    assert!(store
        .read_current(&id("memory-forgotten"), scope_slice)
        .expect("read_current succeeds")
        .is_some());
    assert!(store
        .read_revision(
            &id("memory-forgotten"),
            &id("version-forgotten"),
            scope_slice
        )
        .expect("read_revision succeeds")
        .is_some());

    store
        .forget_memory(&id("memory-forgotten"), "sha256:gap06-forget", scope_slice)
        .expect("forget one memory through the facade");

    assert_eq!(
        store
            .read_current(&id("memory-forgotten"), scope_slice)
            .expect("read_current succeeds"),
        None,
        "a forgotten memory has no current revision"
    );
    assert_eq!(
        store
            .read_revision(
                &id("memory-forgotten"),
                &id("version-forgotten"),
                scope_slice
            )
            .expect("read_revision succeeds"),
        None,
        "a forgotten memory is not reachable by revision id"
    );
}
