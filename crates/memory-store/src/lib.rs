//! Minimal Phase 1 Memory Store facade.
//! 仅负责领域输入校验与 Storage Port 编排；不拥有持久化实现或授权决策。

use memory_domain::{Memory, MemoryVersion, OpaqueId, ScopeRef};
use memory_storage::{
    CommitReceipt, CommitRequest, MemoryStorage, PrepareRequest, PreparedCommitReceipt,
    PublicationState, ScopedMemoryProjection, ScopedMemoryVersionProjection, StorageError,
    ValidatedAuthorization,
};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MemoryStoreError {
    InvalidDomain(memory_domain::DomainError),
    Storage(StorageError),
    MemoryIdentityMismatch,
}

impl From<StorageError> for MemoryStoreError {
    fn from(value: StorageError) -> Self {
        Self::Storage(value)
    }
}

pub type MemoryRevision = MemoryVersion;

pub struct RevisionWrite {
    pub memory_id: OpaqueId,
    pub expected_current_version: Option<OpaqueId>,
    pub revision: MemoryRevision,
    pub idempotency_key: String,
    pub request_digest: String,
}

pub struct MemoryStore<S: MemoryStorage> {
    storage: S,
}

impl<S: MemoryStorage> MemoryStore<S> {
    pub fn new(storage: S) -> Self {
        Self { storage }
    }

    pub fn into_storage(self) -> S {
        self.storage
    }

    pub fn create_memory(
        &mut self,
        memory: Memory,
        cap: &ValidatedAuthorization,
    ) -> Result<(), MemoryStoreError> {
        memory
            .validate()
            .map_err(MemoryStoreError::InvalidDomain)?;

        self.storage.create_memory(memory, cap)?;
        Ok(())
    }

    pub fn read_current(
        &mut self,
        memory_id: &OpaqueId,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
    ) -> Result<Option<ScopedMemoryVersionProjection>, MemoryStoreError> {
        validate_projection_scope(projection_scope)?;
        Ok(self
            .storage
            .read_current(memory_id, cap, projection_scope)?)
    }

    pub fn read_memory(
        &mut self,
        memory_id: &OpaqueId,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
    ) -> Result<Option<ScopedMemoryProjection>, MemoryStoreError> {
        validate_projection_scope(projection_scope)?;
        Ok(self
            .storage
            .read_memory(memory_id, cap, projection_scope)?)
    }

    pub fn read_revision(
        &mut self,
        memory_id: &OpaqueId,
        revision_id: &OpaqueId,
        cap: &ValidatedAuthorization,
        projection_scope: &[ScopeRef],
    ) -> Result<Option<ScopedMemoryVersionProjection>, MemoryStoreError> {
        validate_projection_scope(projection_scope)?;
        Ok(self
            .storage
            .read_version(memory_id, revision_id, cap, projection_scope)?)
    }

    pub fn write_revision(
        &mut self,
        write: RevisionWrite,
        cap: &ValidatedAuthorization,
    ) -> Result<CommitReceipt, MemoryStoreError> {
        write
            .revision
            .validate()
            .map_err(MemoryStoreError::InvalidDomain)?;

        if write.memory_id != write.revision.memory_id {
            return Err(MemoryStoreError::MemoryIdentityMismatch);
        }

        validate_required_string(&write.idempotency_key, "idempotency_key")?;
        validate_required_string(&write.request_digest, "request_digest")?;

        Ok(self.storage.commit_version(
            CommitRequest {
                memory_id: write.memory_id,
                expected_current_version: write.expected_current_version,
                new_version: write.revision,
                idempotency_key: write.idempotency_key,
                request_digest: write.request_digest,
            },
            cap,
        )?)
    }

    /// Stage a revision as hidden.
    ///
    /// The version becomes durable but is neither the current pointer nor
    /// readable through `read_revision` until `publish_prepared` authorizes it.
    /// `PrepareRequest` keeps together everything that must survive the staging
    /// window: the expected current version, the idempotency pair, and the
    /// publication identity addressed by `publish_prepared` and
    /// `publication_state`.
    pub fn prepare_version(
        &mut self,
        request: PrepareRequest,
        cap: &ValidatedAuthorization,
    ) -> Result<PreparedCommitReceipt, MemoryStoreError> {
        Ok(self.storage.prepare_version(request, cap)?)
    }

    /// Publish a prepared revision.
    ///
    /// `expected_current_version` is a concurrency fence, not a hint.
    /// Storage revalidates the captured parent and current pointer when
    /// publishing.
    pub fn publish_prepared(
        &mut self,
        publication_id: &str,
        expected_current_version: Option<OpaqueId>,
        cap: &ValidatedAuthorization,
    ) -> Result<CommitReceipt, MemoryStoreError> {
        validate_required_string(publication_id, "publication_id")?;

        Ok(self.storage.publish_prepared(
            publication_id,
            expected_current_version,
            cap,
        )?)
    }

    /// Return the persisted state of one publication.
    ///
    /// Visibility and authorization are determined by storage from the
    /// transactionally revalidated authorization capability.
    pub fn publication_state(
        &mut self,
        publication_id: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<Option<PublicationState>, MemoryStoreError> {
        validate_required_string(publication_id, "publication_id")?;
        Ok(self.storage.publication_state(publication_id, cap)?)
    }

    pub fn resolve_idempotency(
        &mut self,
        key: &str,
        request_digest: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<Option<CommitReceipt>, MemoryStoreError> {
        validate_required_string(key, "idempotency_key")?;
        validate_required_string(request_digest, "request_digest")?;

        Ok(self
            .storage
            .resolve_idempotency(key, request_digest, cap)?)
    }

    /// Permanently hide a Memory and all of its versions.
    ///
    /// `reason_digest` is an opaque digest, not free text. Repeating the call
    /// returns the original fence sequence.
    pub fn forget_memory(
        &mut self,
        memory_id: &OpaqueId,
        reason_digest: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<i64, MemoryStoreError> {
        validate_required_string(reason_digest, "reason_digest")?;

        Ok(self
            .storage
            .forget_memory(memory_id, reason_digest, cap)?)
    }

    /// Permanently hide one version of a Memory; other versions stay readable.
    pub fn forget_version(
        &mut self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        reason_digest: &str,
        cap: &ValidatedAuthorization,
    ) -> Result<i64, MemoryStoreError> {
        validate_required_string(reason_digest, "reason_digest")?;

        Ok(self
            .storage
            .forget_version(memory_id, version_id, reason_digest, cap)?)
    }
}

/// Validate only the shape of a requested projection scope.
///
/// This is deliberately not an authorization check. Storage must verify that
/// the capability is valid for the operation and target, and that every
/// requested projection scope is covered by the capability, inside its
/// transaction.
fn validate_projection_scope(
    projection_scope: &[ScopeRef],
) -> Result<(), MemoryStoreError> {
    if projection_scope.is_empty() {
        return Err(MemoryStoreError::InvalidDomain(
            memory_domain::DomainError::EmptyRequiredField("projection_scope"),
        ));
    }

    projection_scope
        .iter()
        .try_for_each(ScopeRef::validate)
        .map_err(MemoryStoreError::InvalidDomain)
}

fn validate_required_string(
    value: &str,
    field: &'static str,
) -> Result<(), MemoryStoreError> {
    if value.trim().is_empty() {
        return Err(MemoryStoreError::InvalidDomain(
            memory_domain::DomainError::EmptyRequiredField(field),
        ));
    }

    Ok(())
}


#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{scope_set_contains_all, scopes_intersect};
    use memory_domain::{MemoryLifecycle, ScopeKind};
    use memory_storage::{PrepareRequest, PreparedCommitReceipt, PublicationState};
    use std::collections::BTreeMap;

    #[derive(Clone)]
    struct FakeReceiptRecord {
        receipt: CommitReceipt,
        request_digest: String,
        memory_id: String,
    }

    #[derive(Clone)]
    struct FakePreparedRecord {
        request: PrepareRequest,
        receipt: PreparedCommitReceipt,
        published: Option<CommitReceipt>,
    }

    #[derive(Default)]
    struct FakeStorage {
        memories: BTreeMap<String, Memory>,
        versions: BTreeMap<String, MemoryVersion>,
        receipts: BTreeMap<String, FakeReceiptRecord>,
        prepared: BTreeMap<String, FakePreparedRecord>,
        fences: BTreeMap<(String, String), i64>,
        next_fence_sequence: i64,
    }

    impl FakeStorage {
        fn is_fenced(&self, kind: &str, id: &str) -> bool {
            self.fences.contains_key(&(kind.to_owned(), id.to_owned()))
        }

        fn ensure_not_forgotten(
            &self,
            memory_id: &OpaqueId,
            version_id: Option<&OpaqueId>,
            parent_id: Option<&OpaqueId>,
        ) -> Result<(), StorageError> {
            if self.is_fenced("Memory", memory_id.as_str())
                || version_id.is_some_and(|id| self.is_fenced("Version", id.as_str()))
                || parent_id.is_some_and(|id| self.is_fenced("Version", id.as_str()))
            {
                return Err(StorageError::Forgotten);
            }

            Ok(())
        }

        fn allocate_fence_sequence(&mut self) -> i64 {
            self.next_fence_sequence += 1;
            self.next_fence_sequence
        }
    }

    impl MemoryStorage for FakeStorage {
        fn create_memory(
            &mut self,
            memory: Memory,
            scope: &[ScopeRef],
        ) -> Result<(), StorageError> {
            if scope.is_empty() {
                return Err(StorageError::InvalidSchema);
            }
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.is_fenced("Memory", memory.memory_id.as_str()) {
                return Err(StorageError::Forgotten);
            }
            self.memories
                .insert(memory.memory_id.as_str().into(), memory);
            Ok(())
        }

        fn read_memory(
            &self,
            memory_id: &OpaqueId,
            scope: &[ScopeRef],
        ) -> Result<Option<Memory>, StorageError> {
            if scope.is_empty() {
                return Err(StorageError::InvalidSchema);
            }
            let Some(memory) = self.memories.get(memory_id.as_str()) else {
                return Ok(None);
            };
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.is_fenced("Memory", memory_id.as_str()) {
                return Ok(None);
            }
            Ok(Some(memory.clone()))
        }

        fn read_current(
            &self,
            memory_id: &OpaqueId,
            scope: &[ScopeRef],
        ) -> Result<Option<MemoryVersion>, StorageError> {
            if scope.is_empty() {
                return Err(StorageError::InvalidSchema);
            }
            let Some(memory) = self.memories.get(memory_id.as_str()) else {
                return Ok(None);
            };
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.is_fenced("Memory", memory_id.as_str()) {
                return Ok(None);
            }
            Ok(memory
                .current_version_id
                .as_ref()
                .and_then(|id| self.versions.get(id.as_str()).cloned()))
        }

        fn read_version(
            &self,
            memory_id: &OpaqueId,
            version_id: &OpaqueId,
            scope: &[ScopeRef],
        ) -> Result<Option<MemoryVersion>, StorageError> {
            let Some(memory) = self.memories.get(memory_id.as_str()) else {
                return Ok(None);
            };
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.is_fenced("Memory", memory_id.as_str()) {
                return Ok(None);
            }
            if self.is_fenced("Version", version_id.as_str()) {
                return Ok(None);
            }
            let hidden = self.prepared.values().any(|p| {
                p.request.new_version.memory_version_id == *version_id && p.published.is_none()
            });
            if hidden {
                return Ok(None);
            }
            Ok(self
                .versions
                .get(version_id.as_str())
                .filter(|v| &v.memory_id == memory_id)
                .cloned())
        }

        fn publication_state(
            &self,
            publication_id: &str,
            scope: &[ScopeRef],
        ) -> Result<Option<PublicationState>, StorageError> {
            if scope.is_empty() {
                return Err(StorageError::InvalidSchema);
            }
            let Some(record) = self.prepared.get(publication_id) else {
                return Ok(None);
            };
            let memory = self
                .memories
                .get(record.request.memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.is_fenced("Memory", record.request.memory_id.as_str())
                || self.is_fenced(
                    "Version",
                    record.request.new_version.memory_version_id.as_str(),
                )
            {
                return Ok(None);
            }
            Ok(Some(if record.published.is_some() {
                PublicationState::Published
            } else {
                PublicationState::PreparedHidden
            }))
        }

        fn commit_version(
            &mut self,
            request: CommitRequest,
            scope: &[ScopeRef],
        ) -> Result<CommitReceipt, StorageError> {
            let memory = self
                .memories
                .get_mut(request.memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if request.memory_id != request.new_version.memory_id {
                return Err(StorageError::InvalidReference);
            }
            if self
                .fences
                .contains_key(&("Memory".to_owned(), request.memory_id.as_str().to_owned()))
                || self.fences.contains_key(&(
                    "Version".to_owned(),
                    request.new_version.memory_version_id.as_str().to_owned(),
                ))
                || request
                    .new_version
                    .parent_version_id
                    .as_ref()
                    .is_some_and(|parent| {
                        self.fences
                            .contains_key(&("Version".to_owned(), parent.as_str().to_owned()))
                    })
            {
                return Err(StorageError::Forgotten);
            }
            if let Some(existing) = self.receipts.get(&request.idempotency_key) {
                if existing.memory_id == request.memory_id.as_str()
                    && existing.request_digest == request.request_digest
                {
                    return Ok(existing.receipt.clone());
                }
                return Err(StorageError::IdempotencyConflict);
            }
            if memory.current_version_id != request.expected_current_version {
                return Err(StorageError::StaleVersion);
            }
            if let Some(parent) = request.expected_current_version.as_ref() {
                let current = self
                    .versions
                    .get(parent.as_str())
                    .ok_or(StorageError::StaleVersion)?;
                request
                    .new_version
                    .validate_successor(current)
                    .map_err(|_| StorageError::StaleVersion)?;
            }
            let receipt = CommitReceipt {
                memory_id: request.memory_id.clone(),
                resulting_version_id: request.new_version.memory_version_id.clone(),
                commit_sequence: CommitReceiptSequence::next(&self.receipts),
                idempotency_key: request.idempotency_key.clone(),
            };
            memory.current_version_id = Some(request.new_version.memory_version_id.clone());
            self.versions.insert(
                request.new_version.memory_version_id.as_str().into(),
                request.new_version,
            );
            self.receipts.insert(
                request.idempotency_key,
                FakeReceiptRecord {
                    receipt: receipt.clone(),
                    request_digest: request.request_digest,
                    memory_id: request.memory_id.as_str().into(),
                },
            );
            Ok(receipt)
        }

        fn prepare_version(
            &mut self,
            request: PrepareRequest,
            scope: &[ScopeRef],
        ) -> Result<PreparedCommitReceipt, StorageError> {
            if request.memory_id != request.new_version.memory_id {
                return Err(StorageError::InvalidReference);
            }
            request
                .new_version
                .validate()
                .map_err(|_| StorageError::InvalidSchema)?;
            if request.idempotency_key.is_empty()
                || request.request_digest.is_empty()
                || request.publication_id.is_empty()
            {
                return Err(StorageError::InvalidSchema);
            }
            let memory = self
                .memories
                .get(request.memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if request.new_version.claims.iter().any(|claim| {
                !scope_set_contains_all(&memory.scope_refs, &claim.scope_refs)
                    || !scope_set_contains_all(scope, &claim.scope_refs)
            }) {
                return Err(StorageError::ScopeMismatch);
            }
            self.ensure_not_forgotten(
                &request.memory_id,
                Some(&request.new_version.memory_version_id),
                request.new_version.parent_version_id.as_ref(),
            )?;
            if let Some(existing) = self
                .prepared
                .values()
                .find(|p| p.request.idempotency_key == request.idempotency_key)
            {
                if existing.request.memory_id == request.memory_id
                    && existing.request.request_digest == request.request_digest
                    && existing.request.publication_id == request.publication_id
                    && existing.request.generation == request.generation
                {
                    return Ok(existing.receipt.clone());
                }
                return Err(StorageError::IdempotencyConflict);
            }
            if self.receipts.contains_key(&request.idempotency_key) {
                return Err(StorageError::IdempotencyConflict);
            }
            if self.prepared.contains_key(&request.publication_id) {
                return Err(StorageError::PublicationStateConflict);
            }
            if memory.current_version_id != request.expected_current_version {
                return Err(StorageError::StaleVersion);
            }
            if let Some(parent) = request.expected_current_version.as_ref() {
                if request.new_version.parent_version_id.as_ref() != Some(parent) {
                    return Err(StorageError::StaleVersion);
                }
                let current = self
                    .versions
                    .get(parent.as_str())
                    .ok_or(StorageError::StaleVersion)?;
                request
                    .new_version
                    .validate_successor(current)
                    .map_err(|_| StorageError::StaleVersion)?;
            } else if request.new_version.version_number != 1
                || request.new_version.parent_version_id.is_some()
            {
                return Err(StorageError::StaleVersion);
            }
            let receipt = PreparedCommitReceipt {
                memory_id: request.memory_id.clone(),
                prepared_version_id: request.new_version.memory_version_id.clone(),
                publication_id: request.publication_id.clone(),
                generation: request.generation,
                idempotency_key: request.idempotency_key.clone(),
            };
            self.versions.insert(
                request.new_version.memory_version_id.as_str().into(),
                request.new_version.clone(),
            );
            self.prepared.insert(
                request.publication_id.clone(),
                FakePreparedRecord {
                    request,
                    receipt: receipt.clone(),
                    published: None,
                },
            );
            Ok(receipt)
        }

        fn publish_prepared(
            &mut self,
            publication_id: &str,
            expected_current_version: Option<OpaqueId>,
            scope: &[ScopeRef],
        ) -> Result<CommitReceipt, StorageError> {
            let record = self
                .prepared
                .get(publication_id)
                .cloned()
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            self.ensure_not_forgotten(
                &record.request.memory_id,
                Some(&record.request.new_version.memory_version_id),
                record.request.new_version.parent_version_id.as_ref(),
            )?;
            if let Some(receipt) = record.published {
                return Ok(receipt);
            }
            let request = record.request;
            let memory = self
                .memories
                .get(request.memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if expected_current_version != request.expected_current_version
                || memory.current_version_id != request.expected_current_version
            {
                return Err(StorageError::StaleVersion);
            }
            if let Some(parent) = request.expected_current_version.as_ref() {
                if request.new_version.parent_version_id.as_ref() != Some(parent) {
                    return Err(StorageError::StaleVersion);
                }
                let current = self
                    .versions
                    .get(parent.as_str())
                    .ok_or(StorageError::StaleVersion)?;
                request
                    .new_version
                    .validate_successor(current)
                    .map_err(|_| StorageError::StaleVersion)?;
            } else if request.new_version.version_number != 1
                || request.new_version.parent_version_id.is_some()
            {
                return Err(StorageError::StaleVersion);
            }
            if self.receipts.contains_key(&request.idempotency_key) {
                return Err(StorageError::IdempotencyConflict);
            }
            let receipt = CommitReceipt {
                memory_id: request.memory_id.clone(),
                resulting_version_id: request.new_version.memory_version_id.clone(),
                commit_sequence: CommitReceiptSequence::next(&self.receipts),
                idempotency_key: request.idempotency_key.clone(),
            };
            let memory = self
                .memories
                .get_mut(request.memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            memory.current_version_id = Some(request.new_version.memory_version_id.clone());
            self.receipts.insert(
                request.idempotency_key.clone(),
                FakeReceiptRecord {
                    receipt: receipt.clone(),
                    request_digest: request.request_digest,
                    memory_id: request.memory_id.as_str().into(),
                },
            );
            if let Some(prepared) = self.prepared.get_mut(publication_id) {
                prepared.published = Some(receipt.clone());
            }
            Ok(receipt)
        }

        fn forget_memory(
            &mut self,
            memory_id: &OpaqueId,
            reason_digest: &str,
            scope: &[ScopeRef],
        ) -> Result<i64, StorageError> {
            if reason_digest.is_empty() || scope.is_empty() {
                return Err(StorageError::InvalidSchema);
            }

            let memory = self
                .memories
                .get(memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;

            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }

            if let Some(sequence) = self
                .fences
                .get(&("Memory".into(), memory_id.as_str().into()))
            {
                return Ok(*sequence);
            }

            let sequence = self.allocate_fence_sequence();

            self.fences
                .insert(("Memory".into(), memory_id.as_str().into()), sequence);

            let memory = self
                .memories
                .get_mut(memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;

            memory.lifecycle_state = MemoryLifecycle::Forgotten;

            Ok(sequence)
        }

        fn forget_version(
            &mut self,
            memory_id: &OpaqueId,
            version_id: &OpaqueId,
            reason_digest: &str,
            scope: &[ScopeRef],
        ) -> Result<i64, StorageError> {
            if reason_digest.is_empty() || scope.is_empty() {
                return Err(StorageError::InvalidSchema);
            }

            let memory = self
                .memories
                .get(memory_id.as_str())
                .ok_or(StorageError::NotFoundOrNotVisible)?;

            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }

            let version_exists = self
                .versions
                .get(version_id.as_str())
                .is_some_and(|version| version.memory_id == *memory_id);

            if !version_exists {
                return Err(StorageError::NotFoundOrNotVisible);
            }

            if let Some(sequence) = self
                .fences
                .get(&("Version".into(), version_id.as_str().into()))
            {
                return Ok(*sequence);
            }

            if self.is_fenced("Memory", memory_id.as_str()) {
                return Err(StorageError::Forgotten);
            }

            let sequence = self.allocate_fence_sequence();

            self.fences
                .insert(("Version".into(), version_id.as_str().into()), sequence);

            Ok(sequence)
        }

        fn list_changes(
            &self,
            _after: Option<memory_storage::CommitSequence>,
            _scope: &[ScopeRef],
            _limit: usize,
        ) -> Result<memory_storage::ChangePage, StorageError> {
            Ok(memory_storage::ChangePage {
                records: vec![],
                next_cursor: None,
            })
        }

        fn resolve_idempotency(
            &self,
            key: &str,
            digest: &str,
            scope: &[ScopeRef],
        ) -> Result<Option<CommitReceipt>, StorageError> {
            let Some(record) = self.receipts.get(key) else {
                return Ok(None);
            };
            let memory = self
                .memories
                .get(&record.memory_id)
                .ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.is_fenced("Memory", record.memory_id.as_str())
                || self.is_fenced("Version", record.receipt.resulting_version_id.as_str())
            {
                return Ok(None);
            }
            if record.request_digest != digest {
                return Err(StorageError::IdempotencyConflict);
            }
            Ok(Some(record.receipt.clone()))
        }
    }

    struct CommitReceiptSequence;
    impl CommitReceiptSequence {
        fn next(receipts: &BTreeMap<String, FakeReceiptRecord>) -> memory_storage::CommitSequence {
            memory_storage::CommitSequence(receipts.len() as u64 + 1)
        }
    }

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }
    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("s1"),
            scope_kind: ScopeKind::User,
            namespace_key: "test".into(),
        }
    }
    fn memory() -> Memory {
        Memory {
            memory_id: id("m1"),
            memory_kind: "semantic".into(),
            scope_refs: vec![scope()],
            current_version_id: None,
            lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        }
    }
    fn revision(idv: &str, n: u64, parent: Option<&str>) -> MemoryRevision {
        MemoryRevision {
            memory_version_id: id(idv),
            memory_id: id("m1"),
            version_number: n,
            parent_version_id: parent.map(id),
            created_at: "now".into(),
            author_kind: "test".into(),
            change_reason: "test".into(),
            claims: vec![],
            entity_refs: vec![],
            relation_refs: vec![],
            source_refs: vec![],
            provenance_refs: vec![],
            content_digest: format!("digest-{idv}"),
            schema_version: "1".into(),
        }
    }

    #[test]
    fn create_and_read_are_scope_checked() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        let other = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "other".into(),
        };
        assert!(matches!(
            store.read_current(&id("m1"), &[other]),
            Err(MemoryStoreError::Storage(StorageError::ScopeMismatch))
        ));
    }

    #[test]
    fn stale_revision_and_identity_mismatch_fail_before_storage() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        let bad = RevisionWrite {
            memory_id: id("other"),
            expected_current_version: None,
            revision: revision("v1", 1, None),
            idempotency_key: "op1".into(),
            request_digest: "digest-1".into(),
        };
        assert_eq!(
            store.write_revision(bad, &[scope()]),
            Err(MemoryStoreError::MemoryIdentityMismatch)
        );
    }

    #[test]
    fn idempotent_write_can_be_resolved() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        let write = RevisionWrite {
            memory_id: id("m1"),
            expected_current_version: None,
            revision: revision("v1", 1, None),
            idempotency_key: "op1".into(),
            request_digest: "digest-1".into(),
        };
        let first = store.write_revision(write, &[scope()]).unwrap();
        let resolved = store
            .resolve_idempotency("op1", "digest-1", &[scope()])
            .unwrap();
        assert_eq!(resolved, Some(first.clone()));
        assert_eq!(
            store.resolve_idempotency("op1", "wrong-digest", &[scope()]),
            Err(MemoryStoreError::Storage(StorageError::IdempotencyConflict)),
        );
        let other = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "other".into(),
        };
        assert_eq!(
            store.resolve_idempotency("op1", "digest-1", &[other]),
            Err(MemoryStoreError::Storage(StorageError::ScopeMismatch)),
        );
        let conflicting_replay = RevisionWrite {
            memory_id: id("m1"),
            expected_current_version: None,
            revision: revision("v2", 2, None),
            idempotency_key: "op1".into(),
            request_digest: "different-digest".into(),
        };
        assert_eq!(
            store.write_revision(conflicting_replay, &[scope()]),
            Err(MemoryStoreError::Storage(StorageError::IdempotencyConflict)),
        );
    }

    #[test]
    fn stale_revision_is_rejected_by_storage_port() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        let first = RevisionWrite {
            memory_id: id("m1"),
            expected_current_version: None,
            revision: revision("v1", 1, None),
            idempotency_key: "op1".into(),
            request_digest: "digest-1".into(),
        };
        store.write_revision(first, &[scope()]).unwrap();
        let stale = RevisionWrite {
            memory_id: id("m1"),
            expected_current_version: None,
            revision: revision("v2", 2, None),
            idempotency_key: "op2".into(),
            request_digest: "digest-2".into(),
        };
        assert_eq!(
            store.write_revision(stale, &[scope()]),
            Err(MemoryStoreError::Storage(StorageError::StaleVersion)),
        );
    }

    #[test]
    fn fake_prepare_does_not_advance_current_version() {
        let mut storage = FakeStorage::default();
        storage.create_memory(memory(), &[scope()]).unwrap();

        let prepared = storage
            .prepare_version(
                memory_storage::PrepareRequest {
                    memory_id: id("m1"),
                    expected_current_version: None,
                    new_version: revision("fake-prepared-v1", 1, None),
                    idempotency_key: "fake-prepare-op".into(),
                    request_digest: "fake-prepare-digest".into(),
                    publication_id: "fake-prepare-publication".into(),
                    generation: 1,
                },
                &[scope()],
            )
            .unwrap();

        assert_eq!(prepared.prepared_version_id, id("fake-prepared-v1"));

        assert!(
            storage
                .read_current(&id("m1"), &[scope()])
                .unwrap()
                .is_none(),
            "FakeStorage prepare must not advance the current pointer"
        );

        assert!(
            storage
                .read_version(&id("m1"), &id("fake-prepared-v1"), &[scope()],)
                .unwrap()
                .is_none(),
            "FakeStorage must hide a prepared but unpublished version"
        );

        let receipt = storage
            .publish_prepared("fake-prepare-publication", None, &[scope()])
            .unwrap();

        assert_eq!(receipt.resulting_version_id, id("fake-prepared-v1"));
        assert_eq!(
            storage
                .read_current(&id("m1"), &[scope()])
                .unwrap()
                .unwrap()
                .memory_version_id,
            id("fake-prepared-v1")
        );
        assert!(
            storage
                .read_version(&id("m1"), &id("fake-prepared-v1"), &[scope()],)
                .unwrap()
                .is_some(),
            "published version must become readable"
        );
    }

    #[test]
    fn fake_publish_is_idempotent() {
        let mut storage = FakeStorage::default();
        storage.create_memory(memory(), &[scope()]).unwrap();

        storage
            .prepare_version(
                memory_storage::PrepareRequest {
                    memory_id: id("m1"),
                    expected_current_version: None,
                    new_version: revision("fake-replay-v1", 1, None),
                    idempotency_key: "fake-replay-op".into(),
                    request_digest: "fake-replay-digest".into(),
                    publication_id: "fake-replay-publication".into(),
                    generation: 1,
                },
                &[scope()],
            )
            .unwrap();

        let first = storage
            .publish_prepared("fake-replay-publication", None, &[scope()])
            .unwrap();

        let replay = storage
            .publish_prepared("fake-replay-publication", None, &[scope()])
            .unwrap();

        assert_eq!(first, replay);
        assert_eq!(first.commit_sequence, memory_storage::CommitSequence(1));

        let stored_receipt = storage.receipts.get("fake-replay-op").unwrap();
        assert_eq!(stored_receipt.receipt, first);

        let current = storage
            .read_current(&id("m1"), &[scope()])
            .unwrap()
            .unwrap();
        assert_eq!(current.memory_version_id, id("fake-replay-v1"));
    }

    #[test]
    fn read_memory_round_trips_memory_and_current_version_pointer() {
        let mut store = MemoryStore::new(FakeStorage::default());
        let mut original = memory();
        original.lifecycle_state = MemoryLifecycle::Active;
        store.create_memory(original.clone(), &[scope()]).unwrap();
        store
            .write_revision(
                RevisionWrite {
                    memory_id: id("m1"),
                    expected_current_version: None,
                    revision: revision("v1", 1, None),
                    idempotency_key: "read-memory-round-trip".into(),
                    request_digest: "read-memory-round-trip".into(),
                },
                &[scope()],
            )
            .unwrap();

        let loaded = store.read_memory(&id("m1"), &[scope()]).unwrap().unwrap();
        assert_eq!(loaded.memory_id, original.memory_id);
        assert_eq!(loaded.lifecycle_state, MemoryLifecycle::Active);
        assert_eq!(loaded.current_version_id, Some(id("v1")));
    }

    #[test]
    fn read_memory_and_read_current_return_distinct_domain_objects() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        store
            .write_revision(
                RevisionWrite {
                    memory_id: id("m1"),
                    expected_current_version: None,
                    revision: revision("v1", 1, None),
                    idempotency_key: "distinct-read-apis".into(),
                    request_digest: "distinct-read-apis".into(),
                },
                &[scope()],
            )
            .unwrap();

        let loaded_memory = store.read_memory(&id("m1"), &[scope()]).unwrap().unwrap();
        let loaded_current = store.read_current(&id("m1"), &[scope()]).unwrap().unwrap();
        assert_eq!(loaded_memory.current_version_id, Some(id("v1")));
        assert_eq!(loaded_current.memory_version_id, id("v1"));
        assert_eq!(loaded_memory.memory_kind, "semantic");
        assert_eq!(loaded_current.version_number, 1);
    }

    #[test]
    fn read_memory_returns_none_for_missing_memory() {
        let store = MemoryStore::new(FakeStorage::default());
        assert_eq!(store.read_memory(&id("missing"), &[scope()]), Ok(None));
    }

    #[test]
    fn read_memory_scope_mismatch_matches_read_current() {
        let mut fake = FakeStorage::default();
        fake.create_memory(memory(), &[scope()]).unwrap();
        let other = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "other".into(),
        };
        assert_eq!(
            fake.read_memory(&id("m1"), std::slice::from_ref(&other)),
            Err(StorageError::ScopeMismatch)
        );
        assert_eq!(
            fake.read_current(&id("m1"), &[other]),
            Err(StorageError::ScopeMismatch)
        );
    }

    #[test]
    fn read_memory_empty_scope_matches_read_current() {
        let mut fake = FakeStorage::default();
        fake.create_memory(memory(), &[scope()]).unwrap();
        let empty: [ScopeRef; 0] = [];
        assert_eq!(
            fake.read_memory(&id("m1"), &empty),
            Err(StorageError::InvalidSchema)
        );
        assert_eq!(
            fake.read_current(&id("m1"), &empty),
            Err(StorageError::InvalidSchema)
        );
    }

    #[test]
    fn memory_store_reads_lifecycle_metadata_without_a_current_version() {
        let mut store = MemoryStore::new(FakeStorage::default());
        let mut item = memory();
        item.lifecycle_state = MemoryLifecycle::Archived;
        store.create_memory(item, &[scope()]).unwrap();

        let loaded = store.read_memory(&id("m1"), &[scope()]).unwrap().unwrap();
        assert_eq!(loaded.lifecycle_state, MemoryLifecycle::Archived);
        assert_eq!(loaded.current_version_id, None);
    }

    #[test]
    fn read_memory_hides_a_forgotten_memory_like_read_current_does() {
        let mut fake = FakeStorage::default();
        fake.create_memory(memory(), &[scope()]).unwrap();
        fake.forget_memory(&id("m1"), "forget-digest", &[scope()])
            .unwrap();

        assert_eq!(fake.read_memory(&id("m1"), &[scope()]), Ok(None));
        assert_eq!(fake.read_current(&id("m1"), &[scope()]), Ok(None));
    }

    #[test]
    fn fake_storage_matches_sqlite_scope_semantics() {
        use memory_storage_sqlite::SqliteMemoryStorage;

        let mut fake = FakeStorage::default();
        let mut sqlite = SqliteMemoryStorage::in_memory().unwrap();
        let stored = memory();
        fake.create_memory(stored.clone(), &[scope()]).unwrap();
        sqlite.create_memory(stored, &[scope()]).unwrap();

        let empty: [ScopeRef; 0] = [];
        assert_eq!(
            fake.read_memory(&id("m1"), &empty),
            Err(StorageError::InvalidSchema)
        );
        assert_eq!(
            sqlite.read_memory(&id("m1"), &empty),
            Err(StorageError::InvalidSchema)
        );
        assert_eq!(
            fake.read_memory(&id("missing"), &empty),
            Err(StorageError::InvalidSchema)
        );
        assert_eq!(
            sqlite.read_memory(&id("missing"), &empty),
            Err(StorageError::InvalidSchema)
        );

        let other = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "other".into(),
        };
        assert_eq!(
            fake.read_memory(&id("m1"), std::slice::from_ref(&other)),
            Err(StorageError::ScopeMismatch)
        );
        assert_eq!(
            sqlite.read_memory(&id("m1"), std::slice::from_ref(&other)),
            Err(StorageError::ScopeMismatch)
        );

        assert_eq!(fake.read_memory(&id("m1"), &[scope()]), Ok(Some(memory())));
        assert_eq!(
            sqlite.read_memory(&id("m1"), &[scope()]),
            Ok(Some(memory()))
        );

        let empty_fake = FakeStorage::default();
        let mut empty_sqlite = SqliteMemoryStorage::in_memory().unwrap();
        assert_eq!(
            empty_fake.read_current(&id("missing"), &empty),
            Err(StorageError::InvalidSchema)
        );
        assert_eq!(
            empty_sqlite.read_current(&id("missing"), &empty),
            Err(StorageError::InvalidSchema)
        );
        assert_eq!(
            empty_sqlite.create_memory(memory(), &empty),
            Err(StorageError::InvalidSchema)
        );
        let mut create_fake = FakeStorage::default();
        assert_eq!(
            create_fake.create_memory(memory(), &empty),
            Err(StorageError::InvalidSchema)
        );
    }

    #[test]
    fn sqlite_read_memory_hides_a_forgotten_memory() {
        use memory_storage_sqlite::SqliteMemoryStorage;

        let mut sqlite = SqliteMemoryStorage::in_memory().unwrap();
        sqlite.create_memory(memory(), &[scope()]).unwrap();
        sqlite
            .forget_memory(&id("m1"), "forget-digest", &[scope()])
            .unwrap();

        assert_eq!(sqlite.read_memory(&id("m1"), &[scope()]), Ok(None));
        assert_eq!(sqlite.read_current(&id("m1"), &[scope()]), Ok(None));
    }
}
