use memory_context::{
    commit_change_set, content_hash_for, snapshot_hash, ChangeSet, ChangeSetId, ChangeSetOperation,
    ChangeSetStatus, ContextBudgetSummary, ContextChangeSet, ContextEntry, ContextEntryVersion,
    ContextError, ContextHead, ContextOperation, ContextTier, ContextVersionId, EntryState,
    IdempotencyLog, VersionMetadata,
};
use memory_domain::{ActorRef, OpaqueId};

fn entry(content: &str) -> ContextEntryVersion {
    ContextEntryVersion {
        entry_id: OpaqueId::new("entry-test").unwrap(),
        memory_id: OpaqueId::new("memory-test").unwrap(),
        memory_version_id: OpaqueId::new("version-test").unwrap(),
        revision: 1,
        state: EntryState::Active,
        tier: ContextTier::P1,
        priority: 10,
        activation_reason: "test".into(),
        rendered_content: content.into(),
        source_refs: vec![OpaqueId::new("source-test").unwrap()],
        evidence_refs: vec![],
        epistemic_qualifiers: vec![],
        content_hash: content_hash_for(content),
        rendered_bytes: content.len(),
        valid_time: None,
        temporal_ref: None,
    }
}

#[test]
fn commit_rejects_entry_with_wrong_content_hash() {
    let mut value = entry("A");
    value.content_hash = content_hash_for("B");

    let head = ContextHead {
        context_id: OpaqueId::new("ctx-test").unwrap(),
        version: Some(ContextVersionId::new("v1").unwrap()),
        sequence: 1,
    };

    let mut change_set = ContextChangeSet {
        change_set_id: ChangeSetId::new("cs-test").unwrap(),
        context_id: head.context_id.clone(),
        base_version: head.version.clone(),
        target_version: None,
        operations: vec![ContextOperation::AddEntry {
            operation_id: "add-entry".into(),
            entry: value,
        }],
        reason: "test".into(),
        actor_ref: ActorRef {
            actor_id: OpaqueId::new("actor-test").unwrap(),
        },
        created_at: "2026-01-01T00:00:00Z".into(),
        idempotency_key: "key-test".into(),
        payload_hash: String::new(),
        policy_epoch: 7,
        status: ChangeSetStatus::Prepared,
        correlation_id: None,
        causation_id: None,
        result_ref: None,
    };
    change_set.payload_hash = change_set.compute_payload_hash().unwrap();

    let metadata = VersionMetadata {
        context_version_id: ContextVersionId::new("v2").unwrap(),
        schema_version: "1".into(),
        scope_fingerprint: "scope-fp".into(),
        canonical_watermarks: vec![],
        policy_epoch: 7,
        snapshot_ref: "snapshot://v2".into(),
        snapshot_hash: snapshot_hash(&[]).unwrap(),
        budget_summary: ContextBudgetSummary {
            entry_count: 0,
            rendered_bytes: 0,
        },
        committed_at: "2026-01-01T00:00:01Z".into(),
        actor_ref: ActorRef {
            actor_id: OpaqueId::new("actor-test").unwrap(),
        },
        reason: "test".into(),
    };

    let mut idempotency = IdempotencyLog::default();

    assert!(matches!(
        commit_change_set(&head, change_set, &[], &mut idempotency, 7, metadata,),
        Err(ContextError::ContentHashMismatch { .. })
    ));

    assert!(idempotency.is_empty());
}

#[test]
fn validate_rejects_stale_hash_after_content_edit() {
    let mut value = entry("original");
    value.rendered_content = "modified".into();
    value.rendered_bytes = value.rendered_content.len();

    assert!(matches!(
        value.validate(),
        Err(ContextError::ContentHashMismatch { .. })
    ));
}

#[test]
fn validate_rejects_empty_content_hash() {
    let mut value = entry("content");
    value.content_hash.clear();

    assert!(matches!(
        value.validate(),
        Err(ContextError::EmptyField("content_hash"))
    ));
}

#[test]
fn change_set_validate_rejects_edit_entry_with_wrong_content_hash() {
    let updated = ContextEntry {
        entry_id: OpaqueId::new("entry-edit-test").unwrap(),
        memory_id: OpaqueId::new("memory-edit-test").unwrap(),
        memory_version_id: OpaqueId::new("version-edit-test").unwrap(),
        tier: ContextTier::P1,
        priority: 10,
        activation_reason: "test".into(),
        rendered_content: "actual rendered content".into(),
        source_refs: vec![OpaqueId::new("source-edit-test").unwrap()],
        evidence_refs: vec![],
        epistemic_qualifiers: vec![],
        content_hash: content_hash_for("different rendered content"),
        rendered_bytes: "actual rendered content".len(),
    };

    let change_set = ChangeSet {
        base_version: 1,
        operations: vec![ChangeSetOperation::Update {
            operation_id: "update-entry".into(),
            entry_id: updated.entry_id.clone(),
            updated,
            reason: "test edit".into(),
        }],
    };

    assert!(matches!(
        change_set.validate(),
        Err(ContextError::ContentHashMismatch { .. })
    ));
}

#[test]
fn content_hash_is_sha256_prefixed_and_deterministic() {
    let first = content_hash_for("deterministic content");
    let second = content_hash_for("deterministic content");

    assert_eq!(first, second);
    assert!(first.starts_with("sha256:"));
    assert_eq!(first.len(), 71);
}

#[test]
fn content_hash_covers_exact_utf8_bytes() {
    let content = "中文内容 🧠🌏";
    let value = entry(content);

    assert_eq!(value.rendered_bytes, content.len());
    assert_eq!(value.content_hash, content_hash_for(content));
    assert_ne!(value.content_hash, content_hash_for("中文内容"));

    assert_ne!(content_hash_for("a "), content_hash_for("a"));
    assert_ne!(content_hash_for(" a"), content_hash_for("a"));
}

#[test]
fn content_hash_does_not_normalize_unicode() {
    let nfc = "é";
    let nfd = "e\u{0301}";

    assert_ne!(nfc, nfd);
    assert_ne!(content_hash_for(nfc), content_hash_for(nfd));
}

#[test]
fn snapshot_hash_changes_when_entry_content_hash_changes() {
    let original = entry("snapshot content");
    let mut modified = original.clone();
    modified.content_hash = content_hash_for("different content");

    assert_ne!(
        snapshot_hash(&[original]).unwrap(),
        snapshot_hash(&[modified]).unwrap()
    );
}
