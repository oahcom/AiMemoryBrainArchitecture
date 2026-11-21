//! Minimal Phase 1 Memory Store facade.
//! 仅负责领域校验、Scope 边界与 Storage Port 编排；不拥有持久化实现。

use memory_domain::{Memory, MemoryVersion, OpaqueId, ScopeRef};
use memory_storage::{CommitReceipt, CommitRequest, MemoryStorage, StorageError};

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
    use memory_domain::scopes_intersect;
    use memory_domain::{MemoryLifecycle, ScopeKind};
    use std::collections::BTreeMap;

    #[derive(Clone)]
    struct FakeReceiptRecord {
        receipt: CommitReceipt,
        request_digest: String,
        memory_id: String,
    }

    #[derive(Default)]
    struct FakeStorage {
        memories: BTreeMap<String, Memory>,
        versions: BTreeMap<String, MemoryVersion>,
        receipts: BTreeMap<String, FakeReceiptRecord>,
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
            Ok(memory.current_version_id.as_ref().and_then(|id| self.versions.get(id.as_str()).cloned()))
        }

        fn read_version(&self, memory_id: &OpaqueId, version_id: &OpaqueId, scope: &[ScopeRef]) -> Result<Option<MemoryVersion>, StorageError> {
            let Some(memory) = self.memories.get(memory_id.as_str()) else { return Ok(None) };
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
            }
            Ok(self.versions.get(version_id.as_str()).filter(|v| &v.memory_id == memory_id).cloned())
        }

        fn commit_version(&mut self, request: CommitRequest, scope: &[ScopeRef]) -> Result<CommitReceipt, StorageError> {
            let memory = self.memories.get_mut(request.memory_id.as_str()).ok_or(StorageError::NotFoundOrNotVisible)?;
            if !scopes_intersect(&memory.scope_refs, scope) {
                return Err(StorageError::ScopeMismatch);
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
}
