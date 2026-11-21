//! Backend-neutral durable Event Store contract.
//! 事件接收是持久化边界，不等于编译或 Canonical Memory Commit。

use memory_domain::{OpaqueId, ScopeRef, TimeValue};

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EventClassification {
    Observed,
    Reported,
    Planned,
    Predicted,
    Attempted,
    Outcome,
    Administrative,
    Unknown,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct EventEnvelope {
    pub event_kind: String,
    pub source_type: String,
    pub source_id: OpaqueId,
    pub producer_actor_ref: OpaqueId,
    pub scope_refs: Vec<ScopeRef>,
    pub event_time: Option<TimeValue>,
    pub payload_ref: String,
    pub payload_digest: String,
    pub classification: EventClassification,
    pub idempotency_key: String,
    pub retention_class: String,
    pub correlation_id: OpaqueId,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AcceptedReceipt {
    pub event_id: OpaqueId,
    pub receipt_id: OpaqueId,
    pub accepted_at: String,
    pub payload_digest: String,
    pub processing_state: ProcessingState,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum ProcessingState {
    Pending,
    Suppressed,
    Processing,
    Compiled,
    DeadLetter,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum EventStoreError {
    CapacityUnavailable,
    IdempotencyConflict,
    ScopeMismatch,
    PermissionDenied,
    InvalidEnvelope,
    PayloadIntegrityMismatch,
    NotFoundOrNotVisible,
    TransactionUnavailable,
}

pub trait EventStore {
    fn accept(
        &mut self,
        envelope: EventEnvelope,
        scope: &[ScopeRef],
    ) -> Result<AcceptedReceipt, EventStoreError>;

    fn status(
        &self,
        event_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<AcceptedReceipt>, EventStoreError>;

    fn replay(
        &mut self,
        event_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<AcceptedReceipt, EventStoreError>;
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{OpaqueId, ScopeKind};

    fn id(v: &str) -> OpaqueId {
        OpaqueId::new(v).unwrap()
    }
    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("s1"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s1".into(),
        }
    }

    #[test]
    fn accepted_receipt_is_not_a_compilation_receipt() {
        let receipt = AcceptedReceipt {
            event_id: id("e1"),
            receipt_id: id("r1"),
            accepted_at: "now".into(),
            payload_digest: "d1".into(),
            processing_state: ProcessingState::Pending,
        };
        assert_eq!(receipt.processing_state, ProcessingState::Pending);
    }

    #[test]
    fn envelope_requires_explicit_scope_and_idempotency_identity() {
        let envelope = EventEnvelope {
            event_kind: "observation".into(),
            source_type: "test".into(),
            source_id: id("source"),
            producer_actor_ref: id("actor"),
            scope_refs: vec![scope()],
            event_time: None,
            payload_ref: "payload".into(),
            payload_digest: "digest".into(),
            classification: EventClassification::Observed,
            idempotency_key: "op1".into(),
            retention_class: "default".into(),
            correlation_id: id("corr"),
        };
        assert_eq!(envelope.scope_refs.len(), 1);
        assert!(!envelope.idempotency_key.is_empty());
    }
}
