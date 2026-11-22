//! Durable-delivery checks: an applied snapshot must outlive the adapter that
//! applied it, which is what "survives the process" means at this boundary.

use agent_integration::{
    AdapterError, ApplyOutcome, ContextDeliveryAdapter, DeliveryPayload, FileContextDeliveryAdapter,
};
use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextSnapshot, ContextTier,
};
use memory_domain::{MemoryLifecycle, OpaqueId, ScopeKind, ScopeRef};
use std::path::{Path, PathBuf};

/// Removes the fixture root even when an assertion fails.
struct TempRoot(PathBuf);

impl TempRoot {
    fn new(label: &str) -> Self {
        let nanos = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let path = std::env::temp_dir().join(format!(
            "agent-integration-{label}-{}-{nanos}",
            std::process::id()
        ));
        Self(path)
    }

    fn path(&self) -> &Path {
        &self.0
    }
}

impl Drop for TempRoot {
    fn drop(&mut self) {
        let _ = std::fs::remove_dir_all(&self.0);
    }
}

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn snapshot(version: u64, content: &str) -> ContextSnapshot {
    let scope = ScopeRef {
        scope_id: id("scope-1"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:file-adapter-test".into(),
    };
    let identity = ContextIdentity {
        context_id: id("context-1"),
        scope_refs: vec![scope.clone()],
        agent_id: id("agent-1"),
        agent_instance_id: id("agent-instance-1"),
        session_id: id("sess"),
        task_id: None,
        environment_id: None,
        purpose: "file adapter persistence test".into(),
        schema_version: "1".into(),
    };
    let candidate = ContextCandidate {
        entry_id: id("entry-1"),
        memory_id: id("memory-123"),
        memory_version_id: id("memory-version-1"),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: vec![scope],
        tier: ContextTier::P0,
        priority: 100,
        activation_reason: "integration test fixture".into(),
        rendered_content: content.into(),
        source_refs: vec![id("source-1")],
        evidence_refs: vec![id("evidence-1")],
        epistemic_qualifiers: vec![],
        content_hash: "sha256:test-content-hash".into(),
    };
    build_context(
        identity,
        version,
        ContextBudget {
            max_entries: 8,
            max_rendered_bytes: 4096,
        },
        vec![candidate],
    )
    .unwrap()
}

fn payload(version: u64, content: &str) -> DeliveryPayload {
    DeliveryPayload::from_snapshot(&snapshot(version, content)).unwrap()
}

#[test]
fn applied_snapshot_is_visible_to_a_second_adapter_instance() {
    let root = TempRoot::new("persist");
    let first = payload(1, "first delivery");

    let mut adapter = FileContextDeliveryAdapter::open(root.path()).unwrap();
    assert_eq!(
        adapter.apply("sess", first.clone()),
        Ok(ApplyOutcome::Applied)
    );
    assert_eq!(adapter.applied_snapshot("sess"), Some(&first));
    drop(adapter);

    // A brand-new instance reading the same root must see the delivery, which
    // is the observable form of "the delivery outlived the process".
    let reopened = FileContextDeliveryAdapter::open(root.path()).unwrap();
    let restored = reopened
        .applied_snapshot("sess")
        .expect("delivery must survive reopening the adapter");
    assert_eq!(restored, &first);
    assert_eq!(restored.version(), 1);
    assert_eq!(restored.content(), first.content());

    // The restored version participates in sequencing, not just reads.
    let mut reopened = reopened;
    assert_eq!(
        reopened.apply("sess", payload(2, "second delivery")),
        Ok(ApplyOutcome::Applied)
    );
}

#[test]
fn already_applied_is_reported_across_instances() {
    let root = TempRoot::new("idempotent");
    let first = payload(1, "first delivery");

    let mut adapter = FileContextDeliveryAdapter::open(root.path()).unwrap();
    assert_eq!(
        adapter.apply("sess", first.clone()),
        Ok(ApplyOutcome::Applied)
    );
    drop(adapter);

    let mut reopened = FileContextDeliveryAdapter::open(root.path()).unwrap();
    assert_eq!(
        reopened.apply("sess", first),
        Ok(ApplyOutcome::AlreadyApplied)
    );
}

#[test]
fn clear_removes_the_applied_snapshot_durably() {
    let root = TempRoot::new("clear");
    let mut adapter = FileContextDeliveryAdapter::open(root.path()).unwrap();
    adapter.apply("sess", payload(1, "first delivery")).unwrap();
    assert!(adapter.applied_snapshot("sess").is_some());

    adapter.clear("sess").unwrap();
    assert_eq!(adapter.applied_snapshot("sess"), None);
    drop(adapter);

    let reopened = FileContextDeliveryAdapter::open(root.path()).unwrap();
    assert_eq!(reopened.applied_snapshot("sess"), None);

    // A cleared session restarts its version sequence at 1.
    let mut reopened = reopened;
    assert_eq!(
        reopened.apply("sess", payload(1, "after clear")),
        Ok(ApplyOutcome::Applied)
    );
}

#[test]
fn disconnect_and_reconnect_state_survives_reopening() {
    let root = TempRoot::new("connection");
    let first = payload(1, "first delivery");

    let mut adapter = FileContextDeliveryAdapter::open(root.path()).unwrap();
    adapter.apply("sess", first.clone()).unwrap();
    adapter.disconnect("sess").unwrap();
    assert_eq!(
        adapter.apply("sess", payload(2, "second delivery")),
        Err(AdapterError::SessionDisconnected {
            session_id: "sess".into()
        })
    );
    drop(adapter);

    let mut reopened = FileContextDeliveryAdapter::open(root.path()).unwrap();
    assert_eq!(
        reopened.apply("sess", payload(2, "second delivery")),
        Err(AdapterError::SessionDisconnected {
            session_id: "sess".into()
        })
    );

    // Reconnect reports the last applied version and restores the connection.
    assert_eq!(reopened.reconnect("sess"), Ok(Some(1)));
    assert_eq!(reopened.applied_snapshot("sess"), Some(&first));
    assert_eq!(
        reopened.apply("sess", payload(2, "second delivery")),
        Ok(ApplyOutcome::Applied)
    );
}

#[test]
fn reconnect_without_any_delivery_reports_nothing() {
    let root = TempRoot::new("reconnect-empty");
    let mut adapter = FileContextDeliveryAdapter::open(root.path()).unwrap();
    adapter.disconnect("sess").unwrap();
    drop(adapter);

    let mut reopened = FileContextDeliveryAdapter::open(root.path()).unwrap();
    assert_eq!(reopened.reconnect("sess"), Ok(None));
    assert_eq!(reopened.applied_snapshot("sess"), None);
}

#[test]
fn unsafe_session_ids_are_rejected() {
    let root = TempRoot::new("unsafe");
    let mut adapter = FileContextDeliveryAdapter::open(root.path()).unwrap();

    for session_id in [
        "../evil",
        "",
        "a/b",
        ".hidden",
        "a\\b",
        "sess\n1",
        "sess\u{7f}",
    ] {
        assert!(
            matches!(
                adapter.apply(session_id, payload(1, "first delivery")),
                Err(AdapterError::InvalidSessionId { .. })
            ),
            "apply must reject {session_id:?}"
        );
        assert!(matches!(
            adapter.clear(session_id),
            Err(AdapterError::InvalidSessionId { .. })
        ));
        assert!(matches!(
            adapter.disconnect(session_id),
            Err(AdapterError::InvalidSessionId { .. })
        ));
        assert!(matches!(
            adapter.reconnect(session_id),
            Err(AdapterError::InvalidSessionId { .. })
        ));
        assert_eq!(adapter.applied_snapshot(session_id), None);
    }

    // Nothing escaped the root: the only entries are the ones we opened.
    assert!(root.path().exists());
    assert_eq!(
        std::fs::read_dir(root.path()).unwrap().count(),
        0,
        "rejected session ids must not write anything"
    );
}
