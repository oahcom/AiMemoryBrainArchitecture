use memory_compiler::admission::{
    DependencyRegistrationRequest, FenceInstallReceipt, ProducerRegistrationRequest,
    PublicationGateRequest, SqliteAdmissionStore, WorkState,
};
use memory_domain::{OpaqueId, ScopeKind, ScopeRef};
use std::{
    sync::{Arc, Barrier},
    thread,
};

fn id(s: &str) -> OpaqueId {
    OpaqueId::new(s).unwrap()
}
fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-1"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:scope-1".into(),
    }
}
fn producer() -> ProducerRegistrationRequest {
    ProducerRegistrationRequest {
        producer_work_item_id: id("work-1"),
        producer_class: "compiler".into(),
        producer_identity: id("producer-identity"),
        source_refs: vec![id("event-1")],
        source_lineage_digest: "lineage-1".into(),
        scope_refs: vec![scope()],
        operation_id: id("operation-1"),
        correlation_id: id("correlation-1"),
        causation_id: Some(id("cause-1")),
        admission_canonical_commit_cursor: None,
        observed_fence_cursor: id("fence-observation-0"),
        permission_epoch: id("permission-epoch-1"),
        request_digest: "request-digest-1".into(),
        producer_schema_version: "v1".into(),
    }
}
fn dependency(edge: &str, source: &str) -> DependencyRegistrationRequest {
    DependencyRegistrationRequest {
        dependency_registration_id: id(edge),
        artifact_ref: id("artifact-1"),
        artifact_version: id("artifact-version-1"),
        producer_work_item_id: id("work-1"),
        derivation_run_id: id("run-1"),
        source_ref: id(source),
        source_version: None,
        provenance_ref: id("provenance-1"),
        scope_refs: vec![scope()],
        lineage_digest: "lineage-1".into(),
        required_dependency_count: 2,
        request_digest: format!("digest-{edge}"),
    }
}
fn gate(observation: FenceInstallReceipt, receipts: Vec<OpaqueId>) -> PublicationGateRequest {
    PublicationGateRequest {
        publication_operation_id: id("publication-op-1"),
        artifact_ref: id("artifact-1"),
        artifact_version: id("artifact-version-1"),
        producer_work_item_id: id("work-1"),
        derivation_run_id: id("run-1"),
        attempt_id: id("attempt-1"),
        lease_id: id("lease-1"),
        dependency_receipt_ids: receipts,
        permission_epoch: id("permission-epoch-2"),
        observed_fence_generation: observation.fence_generation,
        observed_protocol_sequence: observation.protocol_sequence,
        scope_refs: vec![scope()],
        request_digest: "publication-digest-1".into(),
    }
}

#[test]
#[ignore = "SQLite cross-connection transaction/locking integration; run explicitly with --features sqlite on a host with SQLite build/link support"]
fn sqlite_fence_and_publication_gate_compete_on_one_protocol_sequence() {
    let path = std::env::temp_dir().join(format!("admission-race-{}.sqlite", std::process::id()));
    let _ = std::fs::remove_file(&path);
    let mut setup = SqliteAdmissionStore::open(&path).unwrap();
    setup.register_producer_work(producer()).unwrap();
    assert!(SqliteAdmissionStore::legal_transition(
        WorkState::Accepted,
        WorkState::DRegistrationPending
    ));
    setup
        .transition_work_state(&id("work-1"), WorkState::DRegistrationPending)
        .unwrap();
    let first = setup
        .register_dependency(dependency("dep-1", "source-1"))
        .unwrap();
    let second = setup
        .register_dependency(dependency("dep-2", "source-2"))
        .unwrap();
    let observed = setup.observe_fence().unwrap();
    drop(setup);

    let barrier = Arc::new(Barrier::new(3));
    let gate_barrier = barrier.clone();
    let gate_path = path.clone();
    let gate_receipts = vec![first.receipt_id, second.receipt_id];
    let gate_thread = thread::spawn(move || {
        let mut db = SqliteAdmissionStore::open(&gate_path).unwrap();
        gate_barrier.wait();
        db.final_publication_gate(gate(observed, gate_receipts))
    });
    let fence_barrier = barrier.clone();
    let fence_path = path.clone();
    let fence_thread = thread::spawn(move || {
        let mut db = SqliteAdmissionStore::open(&fence_path).unwrap();
        fence_barrier.wait();
        db.install_fence(observed.protocol_sequence)
    });
    barrier.wait();
    let gate_result = gate_thread.join().unwrap();
    let fence_result = fence_thread.join().unwrap();
    assert_ne!(
        gate_result.is_ok(),
        fence_result.is_ok(),
        "same observed protocol sequence must have one CAS winner"
    );
    let after = SqliteAdmissionStore::open(&path)
        .unwrap()
        .observe_fence()
        .unwrap();
    assert_eq!(after.protocol_sequence, observed.protocol_sequence + 1);
    if let Ok(receipt) = gate_result {
        assert_eq!(receipt.protocol_sequence, observed.protocol_sequence + 1);
        assert_eq!(receipt.fence_generation, observed.fence_generation);
        assert!(matches!(
            fence_result,
            Err(memory_compiler::admission::AdmissionError::StaleProtocol { .. })
        ));
    } else {
        assert_eq!(after.fence_generation, observed.fence_generation + 1);
        assert!(matches!(
            &gate_result,
            Err(memory_compiler::admission::AdmissionError::StaleFence { .. })
                | Err(memory_compiler::admission::AdmissionError::StaleProtocol { .. })
        ));
    }
    let _ = std::fs::remove_file(&path);
    let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
    let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
}