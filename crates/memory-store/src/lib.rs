//! Minimal Phase 1 Memory Store facade.
//! 仅负责领域校验、Scope 边界与 Storage Port 编排；不拥有持久化实现。

use memory_domain::{Memory, MemoryVersion, OpaqueId, ScopeRef};
use memory_storage::{CommitReceipt, CommitRequest, ForgetReceipt, ForgetRequest, MemoryStorage, StorageError};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MemoryStoreError {
    InvalidDomain(memory_domain::DomainError),
    Storage(StorageError),
    MemoryIdentityMismatch,
}

impl From<StorageError> for MemoryStoreError {
    fn from(value: StorageError) -> Self { Self::Storage(value) }
}

pub type MemoryRevision = MemoryVersion;

pub struct RevisionWrite {
    pub memory_id: OpaqueId,
    pub expected_current_version: Option<OpaqueId>,
    pub revision: MemoryRevision,
    pub idempotency_key: String,
    pub request_digest: String,
}

pub struct ForgetWrite {
    pub memory_id: OpaqueId,
    pub reason: String,
    pub idempotency_key: String,
    pub request_digest: String,
}

pub struct MemoryStore<S: MemoryStorage> {
    storage: S,
}

impl<S: MemoryStorage> MemoryStore<S> {
    pub fn new(storage: S) -> Self { Self { storage } }

    pub fn into_storage(self) -> S { self.storage }

    pub fn create_memory(
        &mut self,
        memory: Memory,
        scope: &[ScopeRef],
    ) -> Result<(), MemoryStoreError> {
        memory.validate().map_err(MemoryStoreError::InvalidDomain)?;
        validate_scope(scope)?;
        self.storage.create_memory(memory, scope)?;
        Ok(())
    }

    pub fn read_current(
        &self,
        memory_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryRevision>, MemoryStoreError> {
        validate_scope(scope)?;
        Ok(self.storage.read_current(memory_id, scope)?)
    }

    pub fn read_revision(
        &self,
        memory_id: &OpaqueId,
        revision_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryRevision>, MemoryStoreError> {
        validate_scope(scope)?;
        Ok(self.storage.read_version(memory_id, revision_id, scope)?)
    }

    pub fn write_revision(
        &mut self,
        write: RevisionWrite,
        scope: &[ScopeRef],
    ) -> Result<CommitReceipt, MemoryStoreError> {
        validate_scope(scope)?;
        write.revision.validate().map_err(MemoryStoreError::InvalidDomain)?;
        if write.memory_id != write.revision.memory_id {
            return Err(MemoryStoreError::MemoryIdentityMismatch);
        }
        Ok(self.storage.commit_version(
            CommitRequest {
                memory_id: write.memory_id,
                expected_current_version: write.expected_current_version,
                new_version: write.revision,
                idempotency_key: write.idempotency_key,
                request_digest: write.request_digest,
            },
            scope,
        )?)
    }

    pub fn resolve_idempotency(
        &self,
        key: &str,
        request_digest: &str,
        scope: &[ScopeRef],
    ) -> Result<Option<CommitReceipt>, MemoryStoreError> {
        validate_scope(scope)?;
        Ok(self.storage.resolve_idempotency(key, request_digest, scope)?)
    }

    /// Suppress one Memory for all future reads and publications.
    ///
    /// Afterwards `read_current`/`read_revision` return `Ok(None)` and
    /// `write_revision` fails with `NotFoundOrNotVisible`. The Memory's
    /// `lifecycle_state` is intentionally left untouched: a fence is a storage
    /// suppression, not a lifecycle transition, and the two are separate layers.
    ///
    /// Note this makes Forget unobservable — "forgotten" and "never existed" look
    /// identical to callers. That is deliberate fail-closed behaviour; the
    /// identity-bearing read API is where an explicit result belongs.
    pub fn forget_memory(
        &mut self,
        write: ForgetWrite,
        scope: &[ScopeRef],
    ) -> Result<ForgetReceipt, MemoryStoreError> {
        validate_scope(scope)?;
        let reason = memory_storage::ForgetReason::new(write.reason)?;
        Ok(self.storage.forget_memory(
            ForgetRequest {
                memory_id: write.memory_id,
                reason,
                idempotency_key: write.idempotency_key,
                request_digest: write.request_digest,
            },
            scope,
        )?)
    }
}

fn validate_scope(scope: &[ScopeRef]) -> Result<(), MemoryStoreError> {
    if scope.is_empty() {
        return Err(MemoryStoreError::InvalidDomain(
            memory_domain::DomainError::EmptyRequiredField("scope"),
        ));
    }
    scope.iter()
        .try_for_each(ScopeRef::validate)
        .map_err(MemoryStoreError::InvalidDomain)
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{scope_set_contains_all, scopes_intersect};
    use memory_storage::{PrepareRequest, PreparedCommitReceipt};
    use memory_domain::{MemoryLifecycle, ScopeKind};
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
        fences: BTreeMap<String, u64>,
    }

    impl MemoryStorage for FakeStorage {
        fn create_memory(&mut self, memory: Memory, scope: &[ScopeRef]) -> Result<(), StorageError> {
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            self.memories.insert(memory.memory_id.as_str().into(), memory);
            Ok(())
        }

        fn read_current(&self, memory_id: &OpaqueId, scope: &[ScopeRef]) -> Result<Option<MemoryVersion>, StorageError> {
            let Some(memory) = self.memories.get(memory_id.as_str()) else { return Ok(None) };
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.fences.contains_key(memory_id.as_str()) { return Ok(None); }
            Ok(memory.current_version_id.as_ref().and_then(|id| self.versions.get(id.as_str()).cloned()))
        }

        fn read_version(&self, memory_id: &OpaqueId, version_id: &OpaqueId, scope: &[ScopeRef]) -> Result<Option<MemoryVersion>, StorageError> {
            let Some(memory) = self.memories.get(memory_id.as_str()) else { return Ok(None) };
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            let hidden = self
                .prepared
                .values()
                .any(|p| p.request.new_version.memory_version_id == *version_id && p.published.is_none());
            if hidden {
                return Ok(None);
            }
            if self.fences.contains_key(memory_id.as_str()) { return Ok(None); }
            Ok(self.versions.get(version_id.as_str()).filter(|v| &v.memory_id == memory_id).cloned())
        }

        fn commit_version(&mut self, request: CommitRequest, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError> {
            let memory = self.memories.get_mut(request.memory_id.as_str()).ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if self.fences.contains_key(request.memory_id.as_str()) {
                return Err(StorageError::NotFoundOrNotVisible);
            }
            if request.memory_id != request.new_version.memory_id {
                return Err(StorageError::InvalidReference);
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
                let current = self.versions.get(parent.as_str()).ok_or(StorageError::StaleVersion)?;
                request.new_version.validate_successor(current).map_err(|_| StorageError::StaleVersion)?;
            }
            let receipt = CommitReceipt {
                memory_id: request.memory_id.clone(),
                resulting_version_id: request.new_version.memory_version_id.clone(),
                commit_sequence: CommitReceiptSequence::next(&self.receipts),
                idempotency_key: request.idempotency_key.clone(),
            };
            memory.current_version_id = Some(request.new_version.memory_version_id.clone());
            self.versions.insert(request.new_version.memory_version_id.as_str().into(), request.new_version);
            self.receipts.insert(request.idempotency_key, FakeReceiptRecord {
                receipt: receipt.clone(),
                request_digest: request.request_digest,
                memory_id: request.memory_id.as_str().into(),
            });
            Ok(receipt)
        }

        fn prepare_version(&mut self, request: PrepareRequest, scope: &[ScopeRef]) -> Result<PreparedCommitReceipt, StorageError> {
            if request.memory_id != request.new_version.memory_id {
                return Err(StorageError::InvalidReference);
            }
            request.new_version.validate().map_err(|_| StorageError::InvalidSchema)?;
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
                let current = self.versions.get(parent.as_str()).ok_or(StorageError::StaleVersion)?;
                request.new_version.validate_successor(current).map_err(|_| StorageError::StaleVersion)?;
            } else if request.new_version.version_number != 1 || request.new_version.parent_version_id.is_some() {
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
                FakePreparedRecord { request, receipt: receipt.clone(), published: None },
            );
            Ok(receipt)
        }

        fn publish_prepared(&mut self, publication_id: &str, expected_current_version: Option<OpaqueId>, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError> {
            let record = self
                .prepared
                .get(publication_id)
                .cloned()
                .ok_or(StorageError::NotFoundOrNotVisible)?;
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
                let current = self.versions.get(parent.as_str()).ok_or(StorageError::StaleVersion)?;
                request.new_version.validate_successor(current).map_err(|_| StorageError::StaleVersion)?;
            } else if request.new_version.version_number != 1 || request.new_version.parent_version_id.is_some() {
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

        fn list_changes(&self, _after: Option<memory_storage::CommitSequence>, _scope: &[ScopeRef], _limit: usize) -> Result<memory_storage::ChangePage, StorageError> {
            Ok(memory_storage::ChangePage { records: vec![], next_cursor: None })
        }

        fn resolve_idempotency(&self, key: &str, digest: &str, scope: &[ScopeRef]) -> Result<Option<CommitReceipt>, StorageError> {
            let Some(record) = self.receipts.get(key) else { return Ok(None) };
            let memory = self.memories.get(&record.memory_id).ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            if record.request_digest != digest {
                return Err(StorageError::IdempotencyConflict);
            }
            Ok(Some(record.receipt.clone()))
        }

        fn forget_memory(&mut self, request: memory_storage::ForgetRequest, scope: &[ScopeRef]) -> Result<memory_storage::ForgetReceipt, StorageError> {
            let memory = self.memories.get(request.memory_id.as_str()).ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            let generation = match self.fences.get(request.memory_id.as_str()) {
                Some(existing) => *existing,
                None => {
                    let next = self.fences.values().copied().max().unwrap_or(0) + 1;
                    self.fences.insert(request.memory_id.as_str().into(), next);
                    next
                }
            };
            Ok(memory_storage::ForgetReceipt {
                memory_id: request.memory_id,
                fence_generation: memory_storage::FenceGeneration(generation),
                idempotency_key: request.idempotency_key,
            })
        }
    }

    struct CommitReceiptSequence;
    impl CommitReceiptSequence {
        fn next(receipts: &BTreeMap<String, FakeReceiptRecord>) -> memory_storage::CommitSequence {
            memory_storage::CommitSequence(receipts.len() as u64 + 1)
        }
    }

    fn id(value: &str) -> OpaqueId { OpaqueId::new(value).unwrap() }
    fn scope() -> ScopeRef {
        ScopeRef { scope_id: id("s1"), scope_kind: ScopeKind::User, namespace_key: "test".into() }
    }
    fn memory() -> Memory {
        Memory {
            memory_id: id("m1"), memory_kind: "semantic".into(), scope_refs: vec![scope()],
            current_version_id: None, lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(), sensitivity: "normal".into(),
            created_at: "now".into(), updated_at: "now".into(),
        }
    }
    fn revision(idv: &str, n: u64, parent: Option<&str>) -> MemoryRevision {
        MemoryRevision {
            memory_version_id: id(idv), memory_id: id("m1"), version_number: n,
            parent_version_id: parent.map(id), created_at: "now".into(),
            author_kind: "test".into(), change_reason: "test".into(),
            claims: vec![], entity_refs: vec![], relation_refs: vec![], source_refs: vec![],
            provenance_refs: vec![], content_digest: format!("digest-{idv}"), schema_version: "1".into(),
        }
    }

    #[test]
    fn create_and_read_are_scope_checked() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        let other = ScopeRef { scope_id: id("s2"), scope_kind: ScopeKind::User, namespace_key: "other".into() };
        assert!(matches!(store.read_current(&id("m1"), &[other]), Err(MemoryStoreError::Storage(StorageError::ScopeMismatch))));
    }

    #[test]
    fn stale_revision_and_identity_mismatch_fail_before_storage() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        let bad = RevisionWrite {
            memory_id: id("other"), expected_current_version: None, revision: revision("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "digest-1".into(),
        };
        assert_eq!(store.write_revision(bad, &[scope()]), Err(MemoryStoreError::MemoryIdentityMismatch));
    }

    #[test]
    fn idempotent_write_can_be_resolved() {
        let mut store = MemoryStore::new(FakeStorage::default());
        store.create_memory(memory(), &[scope()]).unwrap();
        let write = RevisionWrite {
            memory_id: id("m1"), expected_current_version: None, revision: revision("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "digest-1".into(),
        };
        let first = store.write_revision(write, &[scope()]).unwrap();
        let resolved = store.resolve_idempotency("op1", "digest-1", &[scope()]).unwrap();
        assert_eq!(resolved, Some(first.clone()));
        assert_eq!(
            store.resolve_idempotency("op1", "wrong-digest", &[scope()]),
            Err(MemoryStoreError::Storage(StorageError::IdempotencyConflict)),
        );
        let other = ScopeRef { scope_id: id("s2"), scope_kind: ScopeKind::User, namespace_key: "other".into() };
        assert_eq!(
            store.resolve_idempotency("op1", "digest-1", &[other]),
            Err(MemoryStoreError::Storage(StorageError::ScopeMismatch)),
        );
        let conflicting_replay = RevisionWrite {
            memory_id: id("m1"), expected_current_version: None, revision: revision("v2", 2, None),
            idempotency_key: "op1".into(), request_digest: "different-digest".into(),
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
            memory_id: id("m1"), expected_current_version: None, revision: revision("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "digest-1".into(),
        };
        store.write_revision(first, &[scope()]).unwrap();
        let stale = RevisionWrite {
            memory_id: id("m1"), expected_current_version: None, revision: revision("v2", 2, None),
            idempotency_key: "op2".into(), request_digest: "digest-2".into(),
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

        let prepared = storage.prepare_version(
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
        ).unwrap();

        assert_eq!(prepared.prepared_version_id, id("fake-prepared-v1"));

        assert!(
            storage.read_current(&id("m1"), &[scope()]).unwrap().is_none(),
            "FakeStorage prepare must not advance the current pointer"
        );

        assert!(
            storage.read_version(
                &id("m1"),
                &id("fake-prepared-v1"),
                &[scope()],
            ).unwrap().is_none(),
            "FakeStorage must hide a prepared but unpublished version"
        );

        let receipt = storage.publish_prepared(
            "fake-prepare-publication",
            None,
            &[scope()],
        ).unwrap();

        assert_eq!(receipt.resulting_version_id, id("fake-prepared-v1"));
        assert_eq!(
            storage.read_current(&id("m1"), &[scope()])
                .unwrap().unwrap().memory_version_id,
            id("fake-prepared-v1")
        );
        assert!(
            storage.read_version(
                &id("m1"),
                &id("fake-prepared-v1"),
                &[scope()],
            ).unwrap().is_some(),
            "published version must become readable"
        );
    }

    #[test]
    fn fake_publish_is_idempotent() {
        let mut storage = FakeStorage::default();
        storage.create_memory(memory(), &[scope()]).unwrap();

        storage.prepare_version(
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
        ).unwrap();

        let first = storage.publish_prepared(
            "fake-replay-publication",
            None,
            &[scope()],
        ).unwrap();

        let replay = storage.publish_prepared(
            "fake-replay-publication",
            None,
            &[scope()],
        ).unwrap();

        assert_eq!(first, replay);
        assert_eq!(first.commit_sequence, memory_storage::CommitSequence(1));

        let stored_receipt = storage.receipts.get("fake-replay-op").unwrap();
        assert_eq!(stored_receipt.receipt, first);

        let current = storage.read_current(&id("m1"), &[scope()])
            .unwrap().unwrap();
        assert_eq!(current.memory_version_id, id("fake-replay-v1"));
    }
}
