//! SQLite implementation of the Phase 1 MemoryStorage port.
//! 这是第一个具体持久化适配器；事务边界仍严格受 Storage Trait 约束。

use memory_domain::{scopes_intersect, Memory, MemoryVersion, OpaqueId, ScopeRef};
use memory_storage::{ChangePage, ChangeRecord, CommitReceipt, CommitRequest, CommitSequence, MemoryStorage, StorageError};
use rusqlite::{params, Connection, OptionalExtension, TransactionBehavior};

pub struct SqliteMemoryStorage {
    connection: Connection,
}

impl SqliteMemoryStorage {
    pub fn open(path: impl AsRef<std::path::Path>) -> Result<Self, StorageError> {
        let connection = Connection::open(path).map_err(|_| StorageError::TransactionUnavailable)?;
        connection
            .busy_timeout(std::time::Duration::from_secs(5))
            .map_err(|_| StorageError::TransactionUnavailable)?;
        connection
            .pragma_update(None, "journal_mode", "WAL")
            .map_err(|_| StorageError::TransactionUnavailable)?;
        connection
            .pragma_update(None, "synchronous", "FULL")
            .map_err(|_| StorageError::TransactionUnavailable)?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    pub fn in_memory() -> Result<Self, StorageError> {
        let connection = Connection::open_in_memory().map_err(|_| StorageError::TransactionUnavailable)?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    fn initialize(&self) -> Result<(), StorageError> {
        self.connection
            .execute_batch(
                "PRAGMA foreign_keys = ON;
                 CREATE TABLE IF NOT EXISTS memories (
                   memory_id TEXT PRIMARY KEY,
                   scope_json TEXT NOT NULL,
                   current_version_id TEXT,
                   memory_json TEXT NOT NULL
                 );
                 CREATE TABLE IF NOT EXISTS versions (
                   version_id TEXT PRIMARY KEY,
                   memory_id TEXT NOT NULL REFERENCES memories(memory_id),
                   version_number INTEGER NOT NULL,
                   parent_version_id TEXT,
                   scope_json TEXT NOT NULL,
                   version_json TEXT NOT NULL,
                   commit_sequence INTEGER NOT NULL UNIQUE
                 );
                 CREATE TABLE IF NOT EXISTS idempotency (
                   idempotency_key TEXT PRIMARY KEY,
                   memory_id TEXT NOT NULL REFERENCES memories(memory_id),
                   request_digest TEXT NOT NULL,
                   receipt_json TEXT NOT NULL
                 );
                 CREATE INDEX IF NOT EXISTS versions_memory_idx
                   ON versions(memory_id, version_number);
                 CREATE TABLE IF NOT EXISTS commit_log (
                   commit_sequence INTEGER PRIMARY KEY,
                   memory_id TEXT NOT NULL REFERENCES memories(memory_id),
                   version_id TEXT NOT NULL UNIQUE REFERENCES versions(version_id)
                 );",
            )
            .map_err(|_| StorageError::TransactionUnavailable)
    }

    fn encode<T: serde::Serialize>(value: &T) -> Result<String, StorageError> {
        serde_json::to_string(value).map_err(|_| StorageError::InvalidSchema)
    }

    fn decode<T: serde::de::DeserializeOwned>(value: &str) -> Result<T, StorageError> {
        serde_json::from_str(value).map_err(|_| StorageError::InvalidSchema)
    }

    fn scope_allowed(stored_json: &str, requested: &[ScopeRef]) -> Result<(), StorageError> {
        let stored: Vec<ScopeRef> = Self::decode(stored_json)?;
        if scopes_intersect(&stored, requested) {
            Ok(())
        } else {
            Err(StorageError::ScopeMismatch)
        }
    }

    fn read_version_row(
        &self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryVersion>, StorageError> {
        let row = self
            .connection
            .query_row(
                "SELECT v.scope_json, v.version_json
                 FROM versions v
                 WHERE v.memory_id = ?1 AND v.version_id = ?2",
                params![memory_id.as_str(), version_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?;
        match row {
            Some((scope_json, version_json)) => {
                Self::scope_allowed(&scope_json, scope)?;
                Ok(Some(Self::decode(&version_json)?))
            }
            None => Ok(None),
        }
    }

}

impl MemoryStorage for SqliteMemoryStorage {
    fn create_memory(&mut self, memory: Memory, scope: &[ScopeRef]) -> Result<(), StorageError> {
        Self::scope_allowed(&Self::encode(&memory.scope_refs)?, scope)?;
        let scope_json = Self::encode(&memory.scope_refs)?;
        let memory_json = Self::encode(&memory)?;
        self.connection
            .execute(
                "INSERT INTO memories(memory_id, scope_json, current_version_id, memory_json)
                 VALUES (?1, ?2, ?3, ?4)",
                params![
                    memory.memory_id.as_str(),
                    scope_json,
                    memory.current_version_id.as_ref().map(OpaqueId::as_str),
                    memory_json
                ],
            )
            .map_err(|_| StorageError::InvalidReference)?;
        Ok(())
    }

    fn read_current(
        &self,
        memory_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryVersion>, StorageError> {
        let row = self
            .connection
            .query_row(
                "SELECT scope_json, current_version_id FROM memories WHERE memory_id = ?1",
                params![memory_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, Option<String>>(1)?)),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?;
        let Some((scope_json, current)) = row else { return Ok(None) };
        Self::scope_allowed(&scope_json, scope)?;
        let Some(current) = current else { return Ok(None) };
        let version_id = OpaqueId::new(current).map_err(|_| StorageError::InvalidSchema)?;
        self.read_version_row(memory_id, &version_id, scope)
    }

    fn read_version(
        &self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryVersion>, StorageError> {
        self.read_version_row(memory_id, version_id, scope)
    }

    fn commit_version(
        &mut self,
        request: CommitRequest,
        scope: &[ScopeRef],
    ) -> Result<CommitReceipt, StorageError> {
        if request.memory_id != request.new_version.memory_id {
            return Err(StorageError::InvalidReference);
        }

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| StorageError::TransactionUnavailable)?;

        let memory_row = tx
            .query_row(
                "SELECT scope_json, current_version_id FROM memories WHERE memory_id = ?1",
                params![request.memory_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, Option<String>>(1)?)),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?
            .ok_or(StorageError::NotFoundOrNotVisible)?;

        Self::scope_allowed(&memory_row.0, scope)?;

        if let Some((stored_memory_id, stored_digest, receipt_json)) = tx
            .query_row(
                "SELECT memory_id, request_digest, receipt_json FROM idempotency WHERE idempotency_key = ?1",
                params![request.idempotency_key.as_str()],
                |row| Ok((
                    row.get::<_, String>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                )),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?
        {
            // Idempotency keys are globally unique in this adapter. A retry may
            // replay only the receipt for the same memory and identical payload.
            if stored_memory_id == request.memory_id.as_str()
                && stored_digest == request.request_digest
            {
                return Self::decode(&receipt_json);
            }
            return Err(StorageError::IdempotencyConflict);
        }

        let current_id = memory_row.1.as_deref();
        if current_id != request.expected_current_version.as_ref().map(OpaqueId::as_str) {
            return Err(StorageError::StaleVersion);
        }

        if let Some(current_id) = current_id {
            let current_json: String = tx
                .query_row(
                    "SELECT version_json FROM versions WHERE version_id = ?1",
                    params![current_id],
                    |row| row.get(0),
                )
                .map_err(|_| StorageError::TransactionUnavailable)?;
            let current: MemoryVersion = Self::decode(&current_json)?;
            request
                .new_version
                .validate_successor(&current)
                .map_err(|_| StorageError::StaleVersion)?;
        } else if request.new_version.version_number != 1 || request.new_version.parent_version_id.is_some() {
            return Err(StorageError::StaleVersion);
        }

        let scope_json = memory_row.0.clone();
        let version_json = Self::encode(&request.new_version)?;
        let next_sequence: i64 = tx
            .query_row("SELECT COALESCE(MAX(commit_sequence), 0) + 1 FROM commit_log", [], |row| row.get(0))
            .map_err(|_| StorageError::TransactionUnavailable)?;

        tx.execute(
            "INSERT INTO versions(version_id, memory_id, version_number, parent_version_id, scope_json, version_json, commit_sequence)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            params![
                request.new_version.memory_version_id.as_str(),
                request.memory_id.as_str(),
                request.new_version.version_number as i64,
                request.new_version.parent_version_id.as_ref().map(OpaqueId::as_str),
                scope_json,
                version_json,
                next_sequence
            ],
        )
        .map_err(|_| StorageError::InvalidReference)?;

        let mut updated_memory: Memory = Self::decode(
            &tx.query_row(
                "SELECT memory_json FROM memories WHERE memory_id = ?1",
                params![request.memory_id.as_str()],
                |row| row.get::<_, String>(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?,
        )?;
        updated_memory.current_version_id = Some(request.new_version.memory_version_id.clone());
        let memory_json = Self::encode(&updated_memory)?;

        tx.execute(
            "UPDATE memories SET current_version_id = ?1, memory_json = ?2 WHERE memory_id = ?3",
            params![
                request.new_version.memory_version_id.as_str(),
                memory_json,
                request.memory_id.as_str()
            ],
        )
        .map_err(|_| StorageError::TransactionUnavailable)?;

        tx.execute(
            "INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (?1, ?2, ?3)",
            params![next_sequence, request.memory_id.as_str(), request.new_version.memory_version_id.as_str()],
        )
        .map_err(|_| StorageError::TransactionUnavailable)?;

        let receipt = CommitReceipt {
            memory_id: request.memory_id.clone(),
            resulting_version_id: request.new_version.memory_version_id.clone(),
            commit_sequence: CommitSequence(next_sequence as u64),
            idempotency_key: request.idempotency_key.clone(),
        };
        let receipt_json = Self::encode(&receipt)?;
        tx.execute(
            "INSERT INTO idempotency(idempotency_key, memory_id, request_digest, receipt_json) VALUES (?1, ?2, ?3, ?4)",
            params![request.idempotency_key, request.memory_id.as_str(), request.request_digest, receipt_json],
        )
        .map_err(|_| StorageError::IdempotencyConflict)?;

        tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
        Ok(receipt)
    }

    fn list_changes(
        &self,
        after: Option<CommitSequence>,
        scope: &[ScopeRef],
        limit: usize,
    ) -> Result<ChangePage, StorageError> {
        if limit == 0 {
            return Ok(ChangePage { records: vec![], next_cursor: after });
        }
        let start = after.map(|c| c.0 as i64).unwrap_or(0);
        let mut stmt = self.connection
            .prepare(
                "SELECT c.commit_sequence, c.memory_id, c.version_id, m.scope_json
                 FROM commit_log c JOIN memories m ON m.memory_id = c.memory_id
                 WHERE c.commit_sequence > ?1 ORDER BY c.commit_sequence ASC LIMIT ?2",
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        let rows = stmt
            .query_map(params![start, (limit + 1) as i64], |row| {
                Ok((
                    row.get::<_, i64>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                ))
            })
            .map_err(|_| StorageError::TransactionUnavailable)?;

        let mut records = Vec::new();
        for row in rows {
            let (sequence, memory_id, version_id, scope_json) = row.map_err(|_| StorageError::TransactionUnavailable)?;
            if Self::scope_allowed(&scope_json, scope).is_ok() {
                records.push(ChangeRecord {
                    commit_sequence: CommitSequence(sequence as u64),
                    memory_id: OpaqueId::new(memory_id).map_err(|_| StorageError::InvalidSchema)?,
                    version_id: OpaqueId::new(version_id).map_err(|_| StorageError::InvalidSchema)?,
                });
                if records.len() == limit {
                    break;
                }
            }
        }
        let next_cursor = records.last().map(|r| r.commit_sequence);
        Ok(ChangePage { records, next_cursor })
    }

    fn resolve_idempotency(
        &self,
        idempotency_key: &str,
        request_digest: &str,
        scope: &[ScopeRef],
    ) -> Result<Option<CommitReceipt>, StorageError> {
        let row = self
            .connection
            .query_row(
                "SELECT i.request_digest, i.receipt_json, m.scope_json
                 FROM idempotency i
                 JOIN memories m ON m.memory_id = i.memory_id
                 WHERE i.idempotency_key = ?1",
                params![idempotency_key],
                |row| Ok((
                    row.get::<_, String>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                )),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?;
        match row {
            None => Ok(None),
            Some((stored_digest, receipt_json, scope_json)) => {
                Self::scope_allowed(&scope_json, scope)?;
                if stored_digest == request_digest {
                    Ok(Some(Self::decode(&receipt_json)?))
                } else {
                    Err(StorageError::IdempotencyConflict)
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{MemoryLifecycle, ScopeKind};

    fn id(value: &str) -> OpaqueId { OpaqueId::new(value).unwrap() }
    fn scope() -> ScopeRef { ScopeRef { scope_id: id("s1"), scope_kind: ScopeKind::User, namespace_key: "user:s1".into() } }
    fn memory() -> Memory {
        Memory {
            memory_id: id("m1"), memory_kind: "knowledge".into(), scope_refs: vec![scope()],
            current_version_id: None, lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(), sensitivity: "normal".into(),
            created_at: "now".into(), updated_at: "now".into(),
        }
    }
    fn version(idv: &str, n: u64, parent: Option<&str>) -> MemoryVersion {
        MemoryVersion {
            memory_version_id: id(idv), memory_id: id("m1"), version_number: n,
            parent_version_id: parent.map(id), created_at: "now".into(),
            author_kind: "test".into(), change_reason: "test".into(),
            claims: vec![], entity_refs: vec![], relation_refs: vec![], source_refs: vec![],
            provenance_refs: vec![], content_digest: format!("digest-{idv}"), schema_version: "1".into(),
        }
    }

    #[test]
    fn sqlite_round_trip_and_idempotency_are_atomic() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        let receipt = store.commit_version(CommitRequest {
            memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "d1".into(),
        }, &[scope()]).unwrap();
        assert_eq!(receipt.commit_sequence, CommitSequence(1));
        assert_eq!(store.read_current(&id("m1"), &[scope()]).unwrap().unwrap().version_number, 1);
        assert_eq!(store.resolve_idempotency("op1", "d1", &[scope()]).unwrap(), Some(receipt.clone()));
        assert_eq!(store.commit_version(CommitRequest {
            memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "d1".into(),
        }, &[scope()]).unwrap(), receipt);
    }

    #[test]
    fn sqlite_rejects_create_outside_requested_scope() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let other = ScopeRef { scope_id: id("s2"), scope_kind: ScopeKind::User, namespace_key: "user:s2".into() };
        assert_eq!(store.create_memory(memory(), &[other]), Err(StorageError::ScopeMismatch));
    }

    #[test]
    fn sqlite_does_not_replay_idempotency_receipt_before_scope_check() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        store.commit_version(CommitRequest {
            memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "d1".into(),
        }, &[scope()]).unwrap();
        let other = ScopeRef { scope_id: id("s2"), scope_kind: ScopeKind::User, namespace_key: "user:s2".into() };
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
                idempotency_key: "op1".into(), request_digest: "d1".into(),
            }, &[other]),
            Err(StorageError::ScopeMismatch)
        );
    }

    #[test]
    fn sqlite_does_not_replay_idempotency_key_across_memories() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        let mut second_memory = memory();
        second_memory.memory_id = id("m2");
        store.create_memory(second_memory, &[scope()]).unwrap();

        store.commit_version(CommitRequest {
            memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
            idempotency_key: "shared-op".into(), request_digest: "same-digest".into(),
        }, &[scope()]).unwrap();

        let mut second_version = version("v2", 1, None);
        second_version.memory_id = id("m2");
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m2"), expected_current_version: None, new_version: second_version,
                idempotency_key: "shared-op".into(), request_digest: "same-digest".into(),
            }, &[scope()]),
            Err(StorageError::IdempotencyConflict)
        );
    }

    #[test]
    fn sqlite_rejects_stale_expected_version() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        store.commit_version(CommitRequest {
            memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
            idempotency_key: "op1".into(), request_digest: "d1".into(),
        }, &[scope()]).unwrap();
        let result = store.commit_version(CommitRequest {
            memory_id: id("m1"), expected_current_version: Some(id("wrong")), new_version: version("v2", 2, Some("wrong")),
            idempotency_key: "op2".into(), request_digest: "d2".into(),
        }, &[scope()]);
        assert_eq!(result, Err(StorageError::StaleVersion));
    }


    #[test]
    fn file_database_uses_wal_and_full_synchronous_mode() {
        let path = std::env::temp_dir().join(format!("memory-brain-wal-{}.sqlite", std::process::id()));
        let _ = std::fs::remove_file(&path);
        let store = SqliteMemoryStorage::open(&path).unwrap();
        let journal_mode: String = store.connection
            .pragma_query_value(None, "journal_mode", |row| row.get(0)).unwrap();
        let synchronous: i64 = store.connection
            .pragma_query_value(None, "synchronous", |row| row.get(0)).unwrap();
        assert_eq!(journal_mode.to_ascii_lowercase(), "wal");
        assert_eq!(synchronous, 2, "FULL synchronous mode must be active");
        drop(store);
        let _ = std::fs::remove_file(&path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }

    #[test]
    fn committed_state_and_receipt_survive_connection_restart() {
        let path = std::env::temp_dir().join(format!("memory-brain-restart-{}.sqlite", std::process::id()));
        let _ = std::fs::remove_file(&path);
        let receipt = {
            let mut store = SqliteMemoryStorage::open(&path).unwrap();
            store.create_memory(memory(), &[scope()]).unwrap();
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: version("v1", 1, None),
                idempotency_key: "restart-op".into(),
                request_digest: "restart-digest".into(),
            }, &[scope()]).unwrap()
        };
        {
            let store = SqliteMemoryStorage::open(&path).unwrap();
            assert_eq!(store.read_current(&id("m1"), &[scope()]).unwrap().unwrap().memory_version_id, id("v1"));
            assert_eq!(store.resolve_idempotency("restart-op", "restart-digest", &[scope()]).unwrap(), Some(receipt));
            let changes = store.list_changes(None, &[scope()], 10).unwrap();
            assert_eq!(changes.records.len(), 1);
            assert_eq!(changes.records[0].commit_sequence, CommitSequence(1));
        }
        let _ = std::fs::remove_file(&path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }

    // 子进程测试入口：父测试在事务尚未提交时终止该进程，验证 WAL 恢复不会暴露半成品。
    #[test]
    fn crash_writer_child() {
        if std::env::var_os("SQLITE_CRASH_CHILD").is_none() {
            return;
        }
        let path = std::env::var_os("SQLITE_CRASH_PATH").unwrap();
        let store = SqliteMemoryStorage::open(path).unwrap();
        let tx = store.connection.unchecked_transaction().unwrap();
        tx.execute(
            "UPDATE memories SET current_version_id = 'uncommitted-version' WHERE memory_id = 'm1'",
            [],
        ).unwrap();
        std::process::abort();
    }

    #[test]
    fn process_crash_during_open_transaction_recovers_committed_state_only() {
        let path = std::env::temp_dir().join(format!("memory-brain-crash-{}.sqlite", std::process::id()));
        let _ = std::fs::remove_file(&path);
        {
            let mut store = SqliteMemoryStorage::open(&path).unwrap();
            store.create_memory(memory(), &[scope()]).unwrap();
        }

        let status = std::process::Command::new(std::env::current_exe().unwrap())
            .arg("--exact")
            .arg("tests::crash_writer_child")
            .arg("--nocapture")
            .env("SQLITE_CRASH_CHILD", "1")
            .env("SQLITE_CRASH_PATH", &path)
            .status()
            .unwrap();
        assert!(!status.success(), "crash child must terminate before commit");

        let recovered = SqliteMemoryStorage::open(&path).unwrap();
        assert_eq!(recovered.read_current(&id("m1"), &[scope()]).unwrap(), None);
        let pointer: Option<String> = recovered.connection.query_row(
            "SELECT current_version_id FROM memories WHERE memory_id = 'm1'",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(pointer, None, "uncommitted pointer update must be rolled back");

        drop(recovered);
        let _ = std::fs::remove_file(&path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }
}
