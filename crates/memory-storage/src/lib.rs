//! Backend-neutral storage contract for the Phase 1 canonical memory model.
//! 仅定义 Storage Port；不包含 SQLite、网络或具体持久化实现。

use memory_domain::{Memory, MemoryVersion, OpaqueId, ScopeRef};

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum StorageError {
    NotFoundOrNotVisible, StaleVersion, IdempotencyConflict, InvalidReference,
    ScopeMismatch, PermissionDenied, InvalidSchema, ProvenanceIncomplete,
    ContentDigestMismatch, HistoryUnavailable, TransactionUnavailable,
    PublicationStateConflict,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct CommitRequest {
    pub memory_id: OpaqueId,
    pub expected_current_version: Option<OpaqueId>,
    pub new_version: MemoryVersion,
    pub idempotency_key: String,
    pub request_digest: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct CommitReceipt {
    pub memory_id: OpaqueId,
    pub resulting_version_id: OpaqueId,
    pub commit_sequence: CommitSequence,
    pub idempotency_key: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct PrepareRequest {
    pub memory_id: OpaqueId,
    pub expected_current_version: Option<OpaqueId>,
    pub new_version: MemoryVersion,
    pub idempotency_key: String,
    pub request_digest: String,
    pub publication_id: String,
    pub generation: u64,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct PreparedCommitReceipt {
    pub memory_id: OpaqueId,
    pub prepared_version_id: OpaqueId,
    pub publication_id: String,
    pub generation: u64,
    pub idempotency_key: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct CommitSequence(pub u64);

/// Monotonic Forget fence generation.
///
/// Deliberately a separate type from [`CommitSequence`]: the fence is ordered in
/// the audit stream, not in the version commit log. Reusing `commit_log` for
/// fence installation would punch a hole in the contiguous `list_changes`
/// sequence, so the two counters must never be merged.
#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct FenceGeneration(pub u64);

/// Caller-supplied Forget justification.
///
/// The spec requires an operation record to carry a reason, but defines no
/// reason vocabulary, so this stays an opaque non-empty string rather than an
/// invented enum of legal categories.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ForgetReason(String);

impl ForgetReason {
    pub fn new(value: impl Into<String>) -> Result<Self, StorageError> {
        let value = value.into();
        if value.trim().is_empty() {
            return Err(StorageError::InvalidSchema);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ForgetRequest {
    pub memory_id: OpaqueId,
    pub reason: ForgetReason,
    pub idempotency_key: String,
    pub request_digest: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ForgetReceipt {
    pub memory_id: OpaqueId,
    pub fence_generation: FenceGeneration,
    pub idempotency_key: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ChangeRecord {
    pub commit_sequence: CommitSequence,
    pub memory_id: OpaqueId,
    pub version_id: OpaqueId,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ChangePage {
    pub records: Vec<ChangeRecord>,
    pub next_cursor: Option<CommitSequence>,
}

pub trait MemoryStorage {
    fn create_memory(&mut self, memory: Memory, scope: &[ScopeRef]) -> Result<(), StorageError>;
    fn read_current(&self, memory_id: &OpaqueId, scope: &[ScopeRef]) -> Result<Option<MemoryVersion>, StorageError>;
    fn read_version(&self, memory_id: &OpaqueId, version_id: &OpaqueId, scope: &[ScopeRef]) -> Result<Option<MemoryVersion>, StorageError>;
    fn commit_version(&mut self, request: CommitRequest, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError>;
    /// Stage a version as hidden: it must not become current and must not be
    /// readable through `read_version` until `publish_prepared` authorizes it.
    fn prepare_version(&mut self, request: PrepareRequest, scope: &[ScopeRef]) -> Result<PreparedCommitReceipt, StorageError>;
    /// Authorize a prepared version: allocate the canonical sequence, advance the
    /// current pointer and append the change record, all in one transaction.
    fn publish_prepared(&mut self, publication_id: &str, expected_current_version: Option<OpaqueId>, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError>;
    fn list_changes(&self, after: Option<CommitSequence>, scope: &[ScopeRef], limit: usize) -> Result<ChangePage, StorageError>;
    fn resolve_idempotency(&self, idempotency_key: &str, request_digest: &str, scope: &[ScopeRef]) -> Result<Option<CommitReceipt>, StorageError>;

    /// Suppress one Memory by installing a durable, monotonically ordered fence.
    ///
    /// # Suppression, not erasure
    ///
    /// This operation makes the Memory unreadable and unpublishable; it does not
    /// claim to physically remove the payload. Physical erasure is a separate,
    /// asynchronous retention concern that this port cannot prove and therefore
    /// must not report. The `removes payload` vs `makes unavailable` tension in
    /// the spec is resolved in favour of `makes unavailable` at this layer.
    ///
    /// # Idempotency
    ///
    /// Same key + same digest replays the original [`ForgetReceipt`] without
    /// allocating a new generation. Same key + different digest is
    /// [`StorageError::IdempotencyConflict`]. A *different* key forgetting an
    /// already-forgotten Memory is also a success returning the existing
    /// generation: repeated Forget is idempotent, and
    /// `ALREADY_FORGOTTEN` belongs to the lifecycle-transition layer, which this
    /// port deliberately does not implement.
    ///
    /// # Fail-closed observability
    ///
    /// Once fenced, [`MemoryStorage::read_current`] and
    /// [`MemoryStorage::read_version`] return `Ok(None)` and
    /// [`MemoryStorage::commit_version`] returns
    /// [`StorageError::NotFoundOrNotVisible`]. This makes Forget *unobservable*:
    /// a caller cannot distinguish "forgotten" from "never existed". That is a
    /// deliberate trade: a distinguishable third response would leak existence,
    /// and this port carries no `ActorRef`, so it cannot do the
    /// authorization-dependent disclosure the spec describes. The future
    /// identity-bearing read API is where an explicit `forgotten` result belongs.
    ///
    /// # Known gap: change feed
    ///
    /// [`MemoryStorage::list_changes`] is unchanged, so a forgotten Memory still
    /// appears in change pages. Any downstream projection that trusts the change
    /// feed will keep materialising content that reads now deny. Closing this
    /// requires a `ChangeKind::{Version, Forgotten}` discriminator on
    /// [`ChangePage`], which is a separate work item.
    fn forget_memory(&mut self, request: ForgetRequest, scope: &[ScopeRef]) -> Result<ForgetReceipt, StorageError>;
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{MemoryLifecycle, OpaqueId};
    fn id(value: &str) -> OpaqueId { OpaqueId::new(value).unwrap() }

    #[test]
    fn commit_request_keeps_expected_version_and_idempotency_together() {
        let request = CommitRequest {
            memory_id: id("memory"), expected_current_version: Some(id("v1")),
            new_version: MemoryVersion {
                memory_version_id: id("v2"), memory_id: id("memory"), version_number: 2,
                parent_version_id: Some(id("v1")), created_at: "now".into(),
                author_kind: "test".into(), change_reason: "update".into(),
                claims: vec![], entity_refs: vec![], relation_refs: vec![], source_refs: vec![],
                provenance_refs: vec![], content_digest: "digest-v2".into(), schema_version: "1".into(),
            }, idempotency_key: "op-1".into(), request_digest: "digest-1".into(),
        };
        assert_eq!(request.memory_id.as_str(), "memory");
        assert_eq!(request.expected_current_version.unwrap().as_str(), "v1");
    }

    #[test]
    fn commit_sequence_is_orderable_but_not_a_domain_identifier() {
        assert!(CommitSequence(1) < CommitSequence(2));
        let _ = MemoryLifecycle::Candidate;
    }

    #[test]
    fn change_page_can_stop_at_a_contiguous_cursor() {
        let page = ChangePage { records: vec![ChangeRecord { commit_sequence: CommitSequence(7), memory_id: id("memory"), version_id: id("v7") }], next_cursor: Some(CommitSequence(7)) };
        assert_eq!(page.next_cursor, Some(CommitSequence(7)));
    }

    #[test]
    fn forget_reason_rejects_blank_justification() {
        assert_eq!(ForgetReason::new("  "), Err(StorageError::InvalidSchema));
        assert_eq!(ForgetReason::new("user request").unwrap().as_str(), "user request");
    }

    #[test]
    fn fence_generation_orders_independently_of_commit_sequence() {
        assert!(FenceGeneration(1) < FenceGeneration(2));
        assert_eq!(FenceGeneration(9), FenceGeneration(9));
    }
}
