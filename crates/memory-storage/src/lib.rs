//! Backend-neutral storage contract for the Phase 1 canonical memory model.
//! 仅定义 Storage Port；不包含 SQLite、网络或具体持久化实现。

use memory_domain::{Memory, MemoryVersion, OpaqueId, ScopeRef};

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum StorageError {
    NotFoundOrNotVisible,
    StaleVersion,
    IdempotencyConflict,
    InvalidReference,
    ScopeMismatch,
    PermissionDenied,
    InvalidSchema,
    ProvenanceIncomplete,
    ContentDigestMismatch,
    HistoryUnavailable,
    TransactionUnavailable,
    PublicationStateConflict,
    Forgotten,
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

#[derive(
    serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd,
)]
pub struct CommitSequence(pub u64);

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
    fn read_current(
        &self,
        memory_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryVersion>, StorageError>;
    /// Returns the `Memory` aggregate (lifecycle, retention, sensitivity) rather than a
    /// `MemoryVersion`. Visibility semantics are identical to `read_current`: absent or
    /// forgotten yields `Ok(None)`, non-intersecting scope yields `ScopeMismatch`.
    fn read_memory(
        &self,
        memory_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<Memory>, StorageError>;
    fn read_version(
        &self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryVersion>, StorageError>;
    fn commit_version(
        &mut self,
        request: CommitRequest,
        scope: &[ScopeRef],
    ) -> Result<CommitReceipt, StorageError>;
    /// Stage a version as hidden: it must not become current and must not be
    /// readable through `read_version` until `publish_prepared` authorizes it.
    fn prepare_version(
        &mut self,
        request: PrepareRequest,
        scope: &[ScopeRef],
    ) -> Result<PreparedCommitReceipt, StorageError>;
    /// Authorize a prepared version: allocate the canonical sequence, advance the
    /// current pointer and append the change record, all in one transaction.
    fn publish_prepared(
        &mut self,
        publication_id: &str,
        expected_current_version: Option<OpaqueId>,
        scope: &[ScopeRef],
    ) -> Result<CommitReceipt, StorageError>;
    /// Permanently hide a memory and all of its versions.
    /// Repeated calls return the original fence sequence.
    fn forget_memory(
        &mut self,
        memory_id: &OpaqueId,
        reason_digest: &str,
        scope: &[ScopeRef],
    ) -> Result<i64, StorageError>;

    /// Permanently hide one version. Other versions of the memory remain visible.
    fn forget_version(
        &mut self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        reason_digest: &str,
        scope: &[ScopeRef],
    ) -> Result<i64, StorageError>;

    fn list_changes(
        &self,
        after: Option<CommitSequence>,
        scope: &[ScopeRef],
        limit: usize,
    ) -> Result<ChangePage, StorageError>;
    fn resolve_idempotency(
        &self,
        idempotency_key: &str,
        request_digest: &str,
        scope: &[ScopeRef],
    ) -> Result<Option<CommitReceipt>, StorageError>;
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{MemoryLifecycle, OpaqueId};
    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    #[test]
    fn commit_request_keeps_expected_version_and_idempotency_together() {
        let request = CommitRequest {
            memory_id: id("memory"),
            expected_current_version: Some(id("v1")),
            new_version: MemoryVersion {
                memory_version_id: id("v2"),
                memory_id: id("memory"),
                version_number: 2,
                parent_version_id: Some(id("v1")),
                created_at: "now".into(),
                author_kind: "test".into(),
                change_reason: "update".into(),
                claims: vec![],
                entity_refs: vec![],
                relation_refs: vec![],
                source_refs: vec![],
                provenance_refs: vec![],
                content_digest: "digest-v2".into(),
                schema_version: "1".into(),
            },
            idempotency_key: "op-1".into(),
            request_digest: "digest-1".into(),
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
        let page = ChangePage {
            records: vec![ChangeRecord {
                commit_sequence: CommitSequence(7),
                memory_id: id("memory"),
                version_id: id("v7"),
            }],
            next_cursor: Some(CommitSequence(7)),
        };
        assert_eq!(page.next_cursor, Some(CommitSequence(7)));
    }
}
