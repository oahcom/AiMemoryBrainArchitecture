#![cfg(feature = "sqlite")]

use memory_compiler::{AcceptedEvent, Identity, IngestionStage};
use memory_domain::{OpaqueId, ScopeKind, ScopeRef};
use memory_event_store::{EventClassification, EventEnvelope};
use memory_event_store_sqlite::{PayloadEventStoreExt, SqliteEventStore};
use sha2::{Digest, Sha256};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("test identifier should be valid")
}

#[test]
fn sqlite_event_store_receipt_digest_is_accepted_by_compiler_ingestion() {
    let payload = "payload accepted by SQLite Event Store";
    let scope = ScopeRef {
        scope_id: id("scope-1"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:scope-1".to_owned(),
    };
    let digest = format!("sha256:{:x}", Sha256::digest(payload.as_bytes()));
    let envelope = EventEnvelope {
        event_kind: "observation".to_owned(),
        source_type: "integration-test".to_owned(),
        source_id: id("source-1"),
        producer_actor_ref: id("producer-1"),
        scope_refs: vec![scope.clone()],
        event_time: None,
        payload_ref: "payload://integration-test/1".to_owned(),
        payload_digest: digest,
        classification: EventClassification::Observed,
        idempotency_key: "compiler-digest-compat-1".to_owned(),
        retention_class: "test".to_owned(),
        correlation_id: id("correlation-1"),
    };

    let mut store = SqliteEventStore::in_memory().expect("SQLite Event Store should initialize");
    let receipt = store
        .accept_with_payload(envelope, payload.as_bytes(), &[scope])
        .expect("Event Store should accept the payload and return its digest");

    let accepted = AcceptedEvent {
        event_id: Identity::new(receipt.event_id.as_str()).expect("event ID should be valid"),
        receipt_id: Identity::new(receipt.receipt_id.as_str()).expect("receipt ID should be valid"),
        payload_digest: receipt.payload_digest.clone(),
        payload: payload.to_owned(),
        compile_intent_durable: true,
    };

    let ingested = IngestionStage::run(accepted, 1)
        .expect("Compiler must accept the exact digest emitted by Event Store");
    assert_eq!(ingested.payload_digest, receipt.payload_digest);
    assert_eq!(ingested.provenance.payload_digest_algorithm, "sha256");
    assert_eq!(ingested.provenance.canonicalization_version, "raw-v1");
}
