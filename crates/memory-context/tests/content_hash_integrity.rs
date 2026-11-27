use memory_context::{
    content_hash_for, snapshot_hash, ContextEntryVersion, ContextError, ContextTier, EntryState,
};
use memory_domain::OpaqueId;

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

    assert!(matches!(
        value.validate(),
        Err(ContextError::ContentHashMismatch { .. })
    ));
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
