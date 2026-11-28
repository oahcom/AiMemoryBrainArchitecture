//! Backend-neutral storage contract for the Phase 1 canonical memory model.
//! 仅定义 Storage Port；不包含 SQLite、网络或具体持久化实现。

use memory_domain::{
    AuthorizationDecisionRef, AuthorizationOperation, AuthorizationSubjectV1,
    AuthorizationTarget, Claim, Memory, MemoryVersion, OpaqueId, ScopeRef,
};

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum StorageError {
    InvalidAuthorizationReceipt,
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

/// The persisted publication state of one version, mirroring the
/// `publication_preparations.state` constraint of the SQLite adapter.
#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, PartialEq)]
pub enum PublicationState {
    PreparedHidden,
    Published,
    Suppressed,
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

/// Candidate evidence returned by the authorization authority.
/// This is not itself a validated capability.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationReceipt {
    pub decision: AuthorizationDecisionRef,
    pub subject: AuthorizationSubjectV1,
}

/// Marker for a transaction context accepted by the authorization port.
/// Backend implementations must only accept contexts belonging to their
/// own transactional connection.
pub trait AuthorizationTransaction: std::any::Any {
    fn as_any(&self) -> &dyn std::any::Any;
}

/// Validated, process-local authorization capability.
///
/// Its fields are private and it deliberately does not implement Serialize
/// or Deserialize. The only constructor is authorize().
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ValidatedAuthorization {
    receipt: AuthorizationReceipt,
}

impl ValidatedAuthorization {
    pub fn subject(&self) -> &AuthorizationSubjectV1 {
        &self.receipt.subject
    }

    pub fn decision(&self) -> &AuthorizationDecisionRef {
        &self.receipt.decision
    }

    /// The validated receipt, for backends that must revalidate the durable
    /// decision inside their own transaction.
    pub fn receipt(&self) -> &AuthorizationReceipt {
        &self.receipt
    }
}

/// The one authority used by memory and event storage operations.
pub trait AuthorizationAuthority {
    fn issue(
        &self,
        subject: &AuthorizationSubjectV1,
        decision_id: &OpaqueId,
    ) -> Result<AuthorizationReceipt, StorageError>;

    fn validate(
        &self,
        receipt: &AuthorizationReceipt,
        expected: &AuthorizationSubjectV1,
    ) -> Result<(), StorageError>;

    fn validate_in_transaction(
        &self,
        transaction: &dyn AuthorizationTransaction,
        receipt: &AuthorizationReceipt,
        expected: &AuthorizationSubjectV1,
    ) -> Result<(), StorageError>;
}

/// The only capability construction entry point.
pub fn authorize(
    authority: &dyn AuthorizationAuthority,
    receipt: AuthorizationReceipt,
    expected: &AuthorizationSubjectV1,
) -> Result<ValidatedAuthorization, StorageError> {
    if &receipt.subject != expected {
        return Err(StorageError::InvalidAuthorizationReceipt);
    }

    authority.validate(&receipt, expected)?;

    Ok(ValidatedAuthorization { receipt })
}

/// A non-canonical metadata projection. It intentionally contains only
/// explicitly selected metadata and never exposes the canonical Memory.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ScopedMemoryProjection {
    pub memory_id: OpaqueId,
    pub memory_kind: String,
    pub lifecycle_state: memory_domain::MemoryLifecycle,
    pub retention_class: String,
    pub sensitivity: String,
    pub created_at: String,
    pub updated_at: String,
    /// Only scopes in both the stored memory and the caller's authorized
    /// projection scope may appear here.
    pub visible_scope_refs: Vec<ScopeRef>,
    pub authorized_scopes: Vec<ScopeRef>,
    pub policy_epoch: u64,
    pub projection_digest: String,
}

/// A non-canonical version projection. Aggregate reference collections
/// are deliberately absent until ClaimRevision membership is implemented.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ScopedMemoryVersionProjection {
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub canonical_content_digest: String,
    pub visible_claims: Vec<Claim>,
    pub authorized_scopes: Vec<ScopeRef>,
    pub policy_epoch: u64,
    pub projection_digest: String,
}

pub trait MemoryStorage {
    fn create_memory(
        &mut self,
        memory: Memory,
        cap: &ValidatedAuthorization,
    ) -> Result<(), StorageError>;

    fn read_current(
        &mut self,
        memory_id: &OpaqueId,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
    ) -> Result<Option<ScopedMemoryVersionProjection>, StorageError>;

    fn read_memory(
        &mut self,
        memory_id: &OpaqueId,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
    ) -> Result<Option<ScopedMemoryProjection>, StorageError>;

    fn read_version(
        &mut self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
    ) -> Result<Option<ScopedMemoryVersionProjection>, StorageError>;

    fn commit_version(
        &mut self,
        request: CommitRequest,
        cap: &ValidatedAuthorization,
    ) -> Result<CommitReceipt, StorageError>;

    fn prepare_version(
        &mut self,
        request: PrepareRequest,
        cap: &ValidatedAuthorization,
    ) -> Result<PreparedCommitReceipt, StorageError>;

    fn publish_prepared(
        &mut self,
        publication_id: &str,
        expected_current_version: Option<OpaqueId>,
        cap: &ValidatedAuthorization,
    ) -> Result<CommitReceipt, StorageError>;

    fn publication_state(
        &mut self,
        publication_id: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<Option<PublicationState>, StorageError>;

    fn forget_memory(
        &mut self,
        memory_id: &OpaqueId,
        reason_digest: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<i64, StorageError>;

    fn forget_version(
        &mut self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        reason_digest: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<i64, StorageError>;

    fn list_changes(
        &mut self,
        after: Option<CommitSequence>,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
        limit: usize,
    ) -> Result<ChangePage, StorageError>;

    fn resolve_idempotency(
        &mut self,
        idempotency_key: &str,
        request_digest: &str,
        cap: &ValidatedAuthorization,
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
