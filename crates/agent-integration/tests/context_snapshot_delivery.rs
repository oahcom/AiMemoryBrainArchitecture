use agent_integration::{
    AdapterError, ApplyOutcome, ContextDeliveryAdapter, DeliveryPayload,
    InMemoryContextDeliveryAdapter,
};

use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextSnapshot, ContextTier,
};

use memory_domain::{MemoryLifecycle, OpaqueId, ScopeKind, ScopeRef};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-1"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:context-delivery-test".into(),
    }
}

fn identity() -> ContextIdentity {
    ContextIdentity {
        context_id: id("context-1"),
        scope_refs: vec![scope()],
        agent_id: id("agent-1"),
        agent_instance_id: id("agent-instance-1"),
        session_id: id("sess"),
        task_id: None,
        environment_id: None,
        purpose: "context snapshot delivery test".into(),
        schema_version: "1".into(),
    }
}

fn candidate() -> ContextCandidate {
    ContextCandidate {
        entry_id: id("entry-1"),
        memory_id: id("memory-123"),
        memory_version_id: id("memory-version-1"),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: vec![scope()],
        tier: ContextTier::P0,
        priority: 100,
        activation_reason: "integration test fixture".into(),
        rendered_content: "This is the canonical memory content.".into(),
        source_refs: vec![id("source-1")],
        evidence_refs: vec![id("evidence-1")],
        epistemic_qualifiers: vec![],
        content_hash: "sha256:test-content-hash".into(),
    }
}

fn budget() -> ContextBudget {
    ContextBudget {
        max_entries: 8,
        max_rendered_bytes: 4096,
    }
}

#[test]
fn context_snapshot_serialization_is_delivered_and_observable() {
    // Preserve the original candidate memory ID so that the test verifies
    // the actual ID survives both context construction and JSON delivery.
    let candidate = candidate();
    let expected_memory_id = candidate.memory_id.clone();

    let s1 = build_context(identity(), 1, budget(), vec![candidate]).unwrap();

    // Verify the builder preserves candidate.memory_id in ContextEntry.
    assert_eq!(s1.entries.len(), 1);
    assert_eq!(s1.entries[0].memory_id, expected_memory_id);

    let mut adapter = InMemoryContextDeliveryAdapter::default();

    let outcome = adapter.apply("sess", DeliveryPayload::from_snapshot(&s1).unwrap());

    assert_eq!(outcome, Ok(ApplyOutcome::Applied));

    // A1: An applied snapshot exists and is observable.
    assert!(adapter.applied_snapshot("sess").is_some());

    let applied = adapter
        .applied_snapshot("sess")
        .expect("applied snapshot must exist");

    // A2: The delivered version equals the original context version.
    assert_eq!(applied.version(), s1.context_version);

    // A3: The delivered content exactly matches the original
    // canonical serialization, including every byte.
    let original_content = s1.serialize().unwrap();

    assert_eq!(applied.content().as_bytes(), original_content.as_bytes());

    // A4: The delivered content can be deserialized into a
    // ContextSnapshot and retains the original memory ID.
    let decoded: ContextSnapshot = serde_json::from_str(applied.content()).unwrap();

    assert_eq!(decoded.entries.len(), 1);

    assert_eq!(decoded.entries[0].memory_id, expected_memory_id);

    // Also verify that deserialization preserves the context version.
    assert_eq!(decoded.context_version, s1.context_version);
}

#[test]
fn rejected_delivery_leaves_applied_state_untouched() {
    // Build two valid snapshots with consecutive versions.
    // Both use the same identity and candidate; only context_version differs.
    let s1 = build_context(identity(), 1, budget(), vec![candidate()]).unwrap();

    let s2 = build_context(identity(), 2, budget(), vec![candidate()]).unwrap();

    let mut adapter = InMemoryContextDeliveryAdapter::default();

    // First delivery must apply successfully.
    assert_eq!(
        adapter.apply("sess", DeliveryPayload::from_snapshot(&s1).unwrap(),),
        Ok(ApplyOutcome::Applied)
    );

    // Second delivery must apply successfully as the exact successor.
    assert_eq!(
        adapter.apply("sess", DeliveryPayload::from_snapshot(&s2).unwrap(),),
        Ok(ApplyOutcome::Applied)
    );

    // Record the applied content before attempting the stale delivery.
    // This is necessary to prove that failure does not overwrite content.
    let content_before = adapter
        .applied_snapshot("sess")
        .expect("version 2 must be applied")
        .content()
        .to_owned();

    // A5: Reapplying the valid but outdated version 1 snapshot
    // must return the exact VersionMismatch error.
    match adapter.apply("sess", DeliveryPayload::from_snapshot(&s1).unwrap()) {
        Err(AdapterError::VersionMismatch {
            expected: 3,
            received: 1,
        }) => {}
        other => panic!("expected VersionMismatch {{ expected: 3, received: 1 }}, got {other:?}"),
    }

    // A6: The failed delivery must not modify the previously
    // applied snapshot, either in version or in content.
    let applied_after = adapter
        .applied_snapshot("sess")
        .expect("previously applied snapshot must remain present");

    assert_eq!(
        applied_after.version(),
        2,
        "failed delivery must not change the applied version"
    );

    assert_eq!(
        applied_after.content(),
        content_before,
        "failed delivery must not overwrite the applied content"
    );
}
