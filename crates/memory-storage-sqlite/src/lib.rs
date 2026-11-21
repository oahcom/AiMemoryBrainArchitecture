//! SQLite implementation of the Phase 1 MemoryStorage port.
//! 这是第一个具体持久化适配器；事务边界仍严格受 Storage Trait 约束。

use memory_domain::{scope_set_contains_all, scopes_intersect, Memory, MemoryVersion, OpaqueId, ScopeRef};
use memory_storage::{
    ChangePage, ChangeRecord, CommitReceipt, CommitRequest, CommitSequence, FenceGeneration,
    ForgetReceipt, ForgetRequest, MemoryStorage, PrepareRequest, PreparedCommitReceipt,
    StorageError,
};
use rusqlite::{params, Connection, OptionalExtension, TransactionBehavior};
use std::time::Duration;

/// Switch to WAL while tolerating transient contention during concurrent opens.
fn enable_wal(connection: &Connection) -> rusqlite::Result<()> {
    use rusqlite::{Error, ErrorCode};

    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    let mut delay = Duration::from_millis(10);

    loop {
        match connection.execute_batch("PRAGMA journal_mode = WAL;") {
            Ok(()) => return Ok(()),
            Err(Error::SqliteFailure(error, _))
                if matches!(error.code, ErrorCode::DatabaseBusy | ErrorCode::DatabaseLocked)
                    && std::time::Instant::now() < deadline =>
            {
                std::thread::sleep(delay);
                delay = (delay * 2).min(Duration::from_millis(100));
            }
            Err(error) => return Err(error),
        }
    }
}


pub struct SqliteMemoryStorage {
    connection: Connection,
}

impl SqliteMemoryStorage {
    pub fn open(path: impl AsRef<std::path::Path>) -> Result<Self, StorageError> {
        let connection = Connection::open(path).map_err(|_| StorageError::TransactionUnavailable)?;
        connection.busy_timeout(Duration::from_secs(5)).map_err(|_| StorageError::TransactionUnavailable)?;
        enable_wal(&connection).map_err(|_| StorageError::TransactionUnavailable)?;
        connection.execute_batch(
            "PRAGMA synchronous = FULL;
             PRAGMA foreign_keys = ON;
             PRAGMA busy_timeout = 5000;"
        ).map_err(|_| StorageError::TransactionUnavailable)?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    pub fn in_memory() -> Result<Self, StorageError> {
        let connection = Connection::open_in_memory().map_err(|_| StorageError::TransactionUnavailable)?;
        connection.busy_timeout(Duration::from_secs(5)).map_err(|_| StorageError::TransactionUnavailable)?;
        connection.execute_batch(
            "PRAGMA synchronous = FULL;
             PRAGMA foreign_keys = ON;
             PRAGMA busy_timeout = 5000;"
        ).map_err(|_| StorageError::TransactionUnavailable)?;
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
                 );
                 CREATE TABLE IF NOT EXISTS publication_preparations (
                   version_id TEXT PRIMARY KEY REFERENCES versions(version_id),
                   memory_id TEXT NOT NULL REFERENCES memories(memory_id),
                   publication_id TEXT NOT NULL UNIQUE,
                   generation INTEGER NOT NULL CHECK(generation >= 0),
                   request_digest TEXT NOT NULL,
                   idempotency_key TEXT NOT NULL UNIQUE,
                   expected_current_version TEXT,
                   state TEXT NOT NULL CHECK (
                     state IN ('PreparedHidden', 'Published', 'Suppressed')
                   ),
                   commit_sequence INTEGER
                 );
                 CREATE INDEX IF NOT EXISTS publication_preparations_memory_idx
                   ON publication_preparations(memory_id, state);
                 -- Memory-granularity Forget fence. Deliberately keyed by
                 -- memory_id, not namespace_key: a namespace fence would forget
                 -- every Memory belonging to that scope.
                 CREATE TABLE IF NOT EXISTS forget_fence (
                   memory_id TEXT PRIMARY KEY REFERENCES memories(memory_id),
                   fence_generation INTEGER NOT NULL UNIQUE,
                   reason TEXT NOT NULL,
                   recorded_at TEXT NOT NULL
                 );
                 -- Separate from `idempotency` because that table's receipt_json
                 -- is decoded as CommitReceipt in two places; mixing types would
                 -- fail at decode.
                 CREATE TABLE IF NOT EXISTS forget_idempotency (
                   idempotency_key TEXT PRIMARY KEY,
                   memory_id TEXT NOT NULL REFERENCES memories(memory_id),
                   request_digest TEXT NOT NULL,
                   receipt_json TEXT NOT NULL
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

    fn validate_scope_set(scope: &[ScopeRef]) -> Result<(), StorageError> {
        if scope.is_empty() {
            return Err(StorageError::InvalidSchema);
        }
        scope.iter()
            .try_for_each(|item| item.validate().map_err(|_| StorageError::InvalidSchema))
    }

    fn scope_allowed(stored_json: &str, requested: &[ScopeRef]) -> Result<(), StorageError> {
        Self::validate_scope_set(requested)?;
        let stored: Vec<ScopeRef> = Self::decode(stored_json)?;
        Self::validate_scope_set(&stored)?;
        if scopes_intersect(&stored, requested) {
            Ok(())
        } else {
            Err(StorageError::ScopeMismatch)
        }
    }

    /// Fail-closed fence probe. A forgotten Memory is indistinguishable from a
    /// missing one at this boundary, so callers see `Ok(None)` /
    /// `NotFoundOrNotVisible` rather than a third, existence-revealing response.
    fn is_fenced(&self, memory_id: &OpaqueId) -> Result<bool, StorageError> {
        let fenced: Option<i64> = self
            .connection
            .query_row(
                "SELECT 1 FROM forget_fence WHERE memory_id = ?1",
                params![memory_id.as_str()],
                |row| row.get(0),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?;
        Ok(fenced.is_some())
    }

    fn read_version_row(
        &self,
        memory_id: &OpaqueId,
        version_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<MemoryVersion>, StorageError> {
        if self.is_fenced(memory_id)? {
            return Ok(None);
        }
        let row = self
            .connection
            .query_row(
                "SELECT v.scope_json, v.version_json
                 FROM versions v
                 LEFT JOIN publication_preparations p ON p.version_id = v.version_id
                 WHERE v.memory_id = ?1 AND v.version_id = ?2
                   AND (p.version_id IS NULL OR p.state = 'Published')",
                params![memory_id.as_str(), version_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?;
        match row {
            Some((scope_json, version_json)) => {
                Self::scope_allowed(&scope_json, scope)?;
                let stored_scopes: Vec<ScopeRef> = Self::decode(&scope_json)?;
                let mut version: MemoryVersion = Self::decode(&version_json)?;
                version.validate().map_err(|_| StorageError::InvalidSchema)?;
                if version.claims.iter().any(|claim| !scope_set_contains_all(&stored_scopes, &claim.scope_refs)) {
                    return Err(StorageError::InvalidSchema);
                }
                // A Claim is an indivisible disclosure unit: if any of its ScopeRefs
                // is outside the caller-visible set, hide the entire Claim rather
                // than returning a partial or existence-revealing projection.
                version.claims.retain(|claim| scope_set_contains_all(scope, &claim.scope_refs));
                Ok(Some(version))
            }
            None => Ok(None),
        }
    }

}

impl MemoryStorage for SqliteMemoryStorage {
    fn create_memory(&mut self, memory: Memory, scope: &[ScopeRef]) -> Result<(), StorageError> {
        Self::validate_scope_set(scope)?;
        memory.validate().map_err(|_| StorageError::InvalidSchema)?;
        if memory.current_version_id.is_some() {
            // Creation cannot point at a version that this operation does not persist.
            return Err(StorageError::InvalidReference);
        }
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
        Self::validate_scope_set(scope)?;
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
        if self.is_fenced(memory_id)? {
            return Ok(None);
        }
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
        Self::validate_scope_set(scope)?;
        self.read_version_row(memory_id, version_id, scope)
    }

    fn commit_version(
        &mut self,
        request: CommitRequest,
        scope: &[ScopeRef],
    ) -> Result<CommitReceipt, StorageError> {
        Self::validate_scope_set(scope)?;
        if request.memory_id != request.new_version.memory_id {
            return Err(StorageError::InvalidReference);
        }
        request.new_version.validate().map_err(|_| StorageError::InvalidSchema)?;
        if request.idempotency_key.is_empty() || request.request_digest.is_empty() {
            return Err(StorageError::InvalidSchema);
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

        // A fenced Memory must not accept new publications. Fail closed with the
        // same error a missing Memory produces, so the fence stays unobservable.
        let fenced: Option<i64> = tx
            .query_row(
                "SELECT 1 FROM forget_fence WHERE memory_id = ?1",
                params![request.memory_id.as_str()],
                |row| row.get(0),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if fenced.is_some() {
            return Err(StorageError::NotFoundOrNotVisible);
        }

        let memory_scopes: Vec<ScopeRef> = Self::decode(&memory_row.0)?;
        if request.new_version.claims.iter().any(|claim| {
            !scope_set_contains_all(&memory_scopes, &claim.scope_refs)
                || !scope_set_contains_all(scope, &claim.scope_refs)
        }) {
            return Err(StorageError::ScopeMismatch);
        }

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

    fn prepare_version(
        &mut self,
        request: PrepareRequest,
        scope: &[ScopeRef],
    ) -> Result<PreparedCommitReceipt, StorageError> {
        Self::validate_scope_set(scope)?;
        if request.memory_id != request.new_version.memory_id {
            return Err(StorageError::InvalidReference);
        }
        request.new_version.validate().map_err(|_| StorageError::InvalidSchema)?;
        if request.idempotency_key.is_empty()
            || request.request_digest.is_empty()
            || request.publication_id.is_empty()
            || request.generation > i64::MAX as u64
        {
            return Err(StorageError::InvalidSchema);
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
        let memory_scopes: Vec<ScopeRef> = Self::decode(&memory_row.0)?;
        if request.new_version.claims.iter().any(|claim| {
            !scope_set_contains_all(&memory_scopes, &claim.scope_refs)
                || !scope_set_contains_all(scope, &claim.scope_refs)
        }) {
            return Err(StorageError::ScopeMismatch);
        }

        // Replay of an identical preparation returns the original receipt.
        if let Some((stored_memory, stored_digest, stored_publication, stored_generation)) = tx
            .query_row(
                "SELECT memory_id, request_digest, publication_id, generation
                 FROM publication_preparations WHERE idempotency_key = ?1",
                params![request.idempotency_key.as_str()],
                |row| Ok((
                    row.get::<_, String>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, i64>(3)?,
                )),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?
        {
            if stored_memory != request.memory_id.as_str()
                || stored_digest != request.request_digest
                || stored_publication != request.publication_id
                || stored_generation != request.generation as i64
            {
                return Err(StorageError::IdempotencyConflict);
            }
            let version_id: String = tx
                .query_row(
                    "SELECT version_id FROM publication_preparations WHERE idempotency_key = ?1",
                    params![request.idempotency_key.as_str()],
                    |row| row.get(0),
                )
                .map_err(|_| StorageError::TransactionUnavailable)?;
            tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
            return Ok(PreparedCommitReceipt {
                memory_id: request.memory_id,
                prepared_version_id: OpaqueId::new(version_id).map_err(|_| StorageError::InvalidSchema)?,
                publication_id: request.publication_id,
                generation: request.generation,
                idempotency_key: request.idempotency_key,
            });
        }

        // The legacy commit path owns its own idempotency namespace; refuse a key
        // that it already consumed so a single key can never mean two commits.
        let legacy_key_used: bool = tx
            .query_row(
                "SELECT EXISTS(SELECT 1 FROM idempotency WHERE idempotency_key = ?1)",
                params![request.idempotency_key.as_str()],
                |row| row.get(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if legacy_key_used {
            return Err(StorageError::IdempotencyConflict);
        }

        let publication_exists: bool = tx
            .query_row(
                "SELECT EXISTS(SELECT 1 FROM publication_preparations WHERE publication_id = ?1)",
                params![request.publication_id.as_str()],
                |row| row.get(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if publication_exists {
            return Err(StorageError::PublicationStateConflict);
        }

        let current_id = memory_row.1.as_deref();
        if current_id != request.expected_current_version.as_ref().map(OpaqueId::as_str) {
            return Err(StorageError::StaleVersion);
        }

        if let Some(current_id) = current_id {
            if request.new_version.parent_version_id.as_ref().map(OpaqueId::as_str) != Some(current_id) {
                return Err(StorageError::StaleVersion);
            }
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

        // Hidden versions take strictly-decreasing negative sequences so the
        // existing NOT NULL UNIQUE constraint holds without touching the
        // canonical positive sequence, which is allocated from commit_log only.
        let min_negative: Option<i64> = tx
            .query_row(
                "SELECT MIN(commit_sequence) FROM versions WHERE commit_sequence < 0",
                [],
                |row| row.get(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        let reserved_sequence = min_negative
            .unwrap_or(0)
            .checked_sub(1)
            .ok_or(StorageError::TransactionUnavailable)?;

        let scope_json = memory_row.0;
        let version_json = Self::encode(&request.new_version)?;
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
                reserved_sequence
            ],
        )
        .map_err(|_| StorageError::InvalidReference)?;

        tx.execute(
            "INSERT INTO publication_preparations(version_id, memory_id, publication_id, generation,
                request_digest, idempotency_key, expected_current_version, state, commit_sequence)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, 'PreparedHidden', NULL)",
            params![
                request.new_version.memory_version_id.as_str(),
                request.memory_id.as_str(),
                request.publication_id.as_str(),
                request.generation as i64,
                request.request_digest.as_str(),
                request.idempotency_key.as_str(),
                request.expected_current_version.as_ref().map(OpaqueId::as_str),
            ],
        )
        .map_err(|_| StorageError::PublicationStateConflict)?;

        tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
        Ok(PreparedCommitReceipt {
            memory_id: request.memory_id,
            prepared_version_id: request.new_version.memory_version_id,
            publication_id: request.publication_id,
            generation: request.generation,
            idempotency_key: request.idempotency_key,
        })
    }

    fn publish_prepared(
        &mut self,
        publication_id: &str,
        expected_current_version: Option<OpaqueId>,
        scope: &[ScopeRef],
    ) -> Result<CommitReceipt, StorageError> {
        Self::validate_scope_set(scope)?;
        if publication_id.is_empty() {
            return Err(StorageError::InvalidSchema);
        }

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| StorageError::TransactionUnavailable)?;

        let row = tx
            .query_row(
                "SELECT p.memory_id, p.version_id, p.idempotency_key, p.request_digest,
                        p.expected_current_version, p.state, p.commit_sequence,
                        m.scope_json, m.current_version_id, m.memory_json, v.version_json
                 FROM publication_preparations p
                 JOIN memories m ON m.memory_id = p.memory_id
                 JOIN versions v ON v.version_id = p.version_id
                 WHERE p.publication_id = ?1",
                params![publication_id],
                |row| Ok((
                    row.get::<_, String>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                    row.get::<_, Option<String>>(4)?,
                    row.get::<_, String>(5)?,
                    row.get::<_, Option<i64>>(6)?,
                    row.get::<_, String>(7)?,
                    row.get::<_, Option<String>>(8)?,
                    row.get::<_, String>(9)?,
                    row.get::<_, String>(10)?,
                )),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?
            .ok_or(StorageError::NotFoundOrNotVisible)?;

        let (memory_id_text, version_id_text, idempotency_key, request_digest, stored_expected, state, stored_sequence, scope_json, current_id, memory_json, version_json) = row;

        Self::scope_allowed(&scope_json, scope)?;
        let memory_id = OpaqueId::new(memory_id_text).map_err(|_| StorageError::InvalidSchema)?;
        let version_id = OpaqueId::new(version_id_text.clone()).map_err(|_| StorageError::InvalidSchema)?;

        // Replay of a published preparation restores the original receipt and
        // never allocates a second sequence.
        if state == "Published" {
            let sequence = stored_sequence
                .filter(|value| *value > 0)
                .ok_or(StorageError::PublicationStateConflict)?;
            let receipt = CommitReceipt {
                memory_id,
                resulting_version_id: version_id,
                commit_sequence: CommitSequence(sequence as u64),
                idempotency_key,
            };
            tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
            return Ok(receipt);
        }
        if state != "PreparedHidden" {
            return Err(StorageError::PublicationStateConflict);
        }

        if current_id.as_deref() != stored_expected.as_deref()
            || current_id.as_deref() != expected_current_version.as_ref().map(OpaqueId::as_str)
        {
            return Err(StorageError::StaleVersion);
        }

        let memory_scopes: Vec<ScopeRef> = Self::decode(&scope_json)?;
        let version: MemoryVersion = Self::decode(&version_json)?;
        version.validate().map_err(|_| StorageError::InvalidSchema)?;
        if version.claims.iter().any(|claim| {
            !scope_set_contains_all(&memory_scopes, &claim.scope_refs)
                || !scope_set_contains_all(scope, &claim.scope_refs)
        }) {
            return Err(StorageError::ScopeMismatch);
        }

        // Re-validate the parent at publish time; the prepare-time check alone
        // cannot vouch for a pointer that may have moved since.
        if let Some(current_id) = current_id.as_deref() {
            if version.parent_version_id.as_ref().map(OpaqueId::as_str) != Some(current_id) {
                return Err(StorageError::StaleVersion);
            }
            let current_json: String = tx
                .query_row(
                    "SELECT version_json FROM versions WHERE version_id = ?1",
                    params![current_id],
                    |row| row.get(0),
                )
                .map_err(|_| StorageError::TransactionUnavailable)?;
            let current: MemoryVersion = Self::decode(&current_json)?;
            version.validate_successor(&current).map_err(|_| StorageError::StaleVersion)?;
        } else if version.version_number != 1 || version.parent_version_id.is_some() {
            return Err(StorageError::StaleVersion);
        }

        let key_exists: bool = tx
            .query_row(
                "SELECT EXISTS(SELECT 1 FROM idempotency WHERE idempotency_key = ?1)",
                params![idempotency_key.as_str()],
                |row| row.get(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if key_exists {
            return Err(StorageError::IdempotencyConflict);
        }

        let next_sequence: i64 = tx
            .query_row(
                "SELECT COALESCE(MAX(commit_sequence), 0) + 1 FROM commit_log",
                [],
                |row| row.get(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if next_sequence <= 0 {
            return Err(StorageError::TransactionUnavailable);
        }

        let changed = tx
            .execute(
                "UPDATE versions SET commit_sequence = ?1 WHERE version_id = ?2 AND commit_sequence < 0",
                params![next_sequence, version_id_text.as_str()],
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if changed != 1 {
            return Err(StorageError::PublicationStateConflict);
        }

        let mut updated_memory: Memory = Self::decode(&memory_json)?;
        updated_memory.current_version_id = Some(version_id.clone());
        let updated_memory_json = Self::encode(&updated_memory)?;
        tx.execute(
            "UPDATE memories SET current_version_id = ?1, memory_json = ?2 WHERE memory_id = ?3",
            params![version_id.as_str(), updated_memory_json, memory_id.as_str()],
        )
        .map_err(|_| StorageError::TransactionUnavailable)?;

        tx.execute(
            "INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (?1, ?2, ?3)",
            params![next_sequence, memory_id.as_str(), version_id.as_str()],
        )
        .map_err(|_| StorageError::TransactionUnavailable)?;

        let receipt = CommitReceipt {
            memory_id: memory_id.clone(),
            resulting_version_id: version_id.clone(),
            commit_sequence: CommitSequence(next_sequence as u64),
            idempotency_key: idempotency_key.clone(),
        };
        let receipt_json = Self::encode(&receipt)?;
        tx.execute(
            "INSERT INTO idempotency(idempotency_key, memory_id, request_digest, receipt_json) VALUES (?1, ?2, ?3, ?4)",
            params![idempotency_key.as_str(), memory_id.as_str(), request_digest.as_str(), receipt_json],
        )
        .map_err(|_| StorageError::IdempotencyConflict)?;

        let changed = tx
            .execute(
                "UPDATE publication_preparations SET state = 'Published', commit_sequence = ?1
                 WHERE publication_id = ?2 AND state = 'PreparedHidden'",
                params![next_sequence, publication_id],
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        if changed != 1 {
            return Err(StorageError::PublicationStateConflict);
        }

        tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
        Ok(receipt)
    }

    fn list_changes(
        &self,
        after: Option<CommitSequence>,
        scope: &[ScopeRef],
        limit: usize,
    ) -> Result<ChangePage, StorageError> {
        Self::validate_scope_set(scope)?;
        if limit == 0 {
            return Ok(ChangePage { records: vec![], next_cursor: after });
        }
        let start = after.map(|c| c.0 as i64).unwrap_or(0);
        let mut stmt = self.connection
            .prepare(
                "SELECT c.commit_sequence, c.memory_id, c.version_id, m.scope_json
                 FROM commit_log c JOIN memories m ON m.memory_id = c.memory_id
                 WHERE c.commit_sequence > ?1 ORDER BY c.commit_sequence ASC",
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        let rows = stmt
            .query_map(params![start], |row| {
                Ok((
                    row.get::<_, i64>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                ))
            })
            .map_err(|_| StorageError::TransactionUnavailable)?;

        // Apply the page limit to authorized records, not raw commit-log rows.
        // Read until one extra visible record is found so the cursor never
        // advances past an item that belongs on the next page.
        let mut records = Vec::new();
        for row in rows {
            let (sequence, memory_id, version_id, scope_json) =
                row.map_err(|_| StorageError::TransactionUnavailable)?;
            match Self::scope_allowed(&scope_json, scope) {
                Ok(()) => {
                    records.push(ChangeRecord {
                        commit_sequence: CommitSequence(sequence as u64),
                        memory_id: OpaqueId::new(memory_id).map_err(|_| StorageError::InvalidSchema)?,
                        version_id: OpaqueId::new(version_id).map_err(|_| StorageError::InvalidSchema)?,
                    });
                    if records.len() > limit {
                        break;
                    }
                }
                Err(StorageError::ScopeMismatch) => continue,
                Err(error) => return Err(error),
            }
        }
        if records.len() > limit {
            records.pop();
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
        Self::validate_scope_set(scope)?;
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

    fn forget_memory(
        &mut self,
        request: ForgetRequest,
        scope: &[ScopeRef],
    ) -> Result<ForgetReceipt, StorageError> {
        Self::validate_scope_set(scope)?;
        if request.idempotency_key.is_empty() || request.request_digest.is_empty() {
            return Err(StorageError::InvalidSchema);
        }
        if request.reason.as_str().trim().is_empty() {
            return Err(StorageError::InvalidSchema);
        }

        // IMMEDIATE so the generation read and the fence insert cannot interleave:
        // two concurrent forgets would otherwise both read the same MAX and
        // collide on the UNIQUE constraint, surfacing as a storage error rather
        // than a clean idempotent replay.
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| StorageError::TransactionUnavailable)?;

        let scope_json: String = tx
            .query_row(
                "SELECT scope_json FROM memories WHERE memory_id = ?1",
                params![request.memory_id.as_str()],
                |row| row.get(0),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?
            .ok_or(StorageError::NotFoundOrNotVisible)?;
        Self::scope_allowed(&scope_json, scope)?;

        if let Some((stored_memory_id, stored_digest, receipt_json)) = tx
            .query_row(
                "SELECT memory_id, request_digest, receipt_json FROM forget_idempotency WHERE idempotency_key = ?1",
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
            if stored_memory_id == request.memory_id.as_str() && stored_digest == request.request_digest {
                let receipt: ForgetReceipt = Self::decode(&receipt_json)?;
                tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
                return Ok(receipt);
            }
            return Err(StorageError::IdempotencyConflict);
        }

        // Repeated Forget under a fresh key is idempotent: replay the existing
        // generation instead of allocating another one.
        if let Some(existing) = tx
            .query_row(
                "SELECT fence_generation FROM forget_fence WHERE memory_id = ?1",
                params![request.memory_id.as_str()],
                |row| row.get::<_, i64>(0),
            )
            .optional()
            .map_err(|_| StorageError::TransactionUnavailable)?
        {
            let receipt = ForgetReceipt {
                memory_id: request.memory_id.clone(),
                fence_generation: FenceGeneration(existing as u64),
                idempotency_key: request.idempotency_key.clone(),
            };
            tx.execute(
                "INSERT INTO forget_idempotency(idempotency_key, memory_id, request_digest, receipt_json)
                 VALUES (?1, ?2, ?3, ?4)",
                params![
                    request.idempotency_key.as_str(),
                    request.memory_id.as_str(),
                    request.request_digest.as_str(),
                    Self::encode(&receipt)?
                ],
            )
            .map_err(|_| StorageError::IdempotencyConflict)?;
            tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
            return Ok(receipt);
        }

        let next: i64 = tx
            .query_row(
                "SELECT COALESCE(MAX(fence_generation), 0) + 1 FROM forget_fence",
                [],
                |row| row.get(0),
            )
            .map_err(|_| StorageError::TransactionUnavailable)?;
        let recorded_at = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_nanos()
            .to_string();
        tx.execute(
            "INSERT INTO forget_fence(memory_id, fence_generation, reason, recorded_at)
             VALUES (?1, ?2, ?3, ?4)",
            params![
                request.memory_id.as_str(),
                next,
                request.reason.as_str(),
                recorded_at
            ],
        )
        .map_err(|_| StorageError::TransactionUnavailable)?;

        let receipt = ForgetReceipt {
            memory_id: request.memory_id.clone(),
            fence_generation: FenceGeneration(next as u64),
            idempotency_key: request.idempotency_key.clone(),
        };
        tx.execute(
            "INSERT INTO forget_idempotency(idempotency_key, memory_id, request_digest, receipt_json)
             VALUES (?1, ?2, ?3, ?4)",
            params![
                request.idempotency_key.as_str(),
                request.memory_id.as_str(),
                request.request_digest.as_str(),
                Self::encode(&receipt)?
            ],
        )
        .map_err(|_| StorageError::IdempotencyConflict)?;

        tx.commit().map_err(|_| StorageError::TransactionUnavailable)?;
        Ok(receipt)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::{Claim, EpistemicStatus, MemoryLifecycle, ScopeKind};

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

    fn claim_in_scope(claim_id: &str, claim_scope: ScopeRef) -> Claim {
        Claim {
            claim_id: id(claim_id),
            subject_ref: id("subject"),
            predicate: "has_value".into(),
            object_value: "value".into(),
            polarity: "affirm".into(),
            epistemic_status: EpistemicStatus::Observed,
            confidence: None,
            temporal_ref: None,
            asserted_at: "now".into(),
            scope_refs: vec![claim_scope],
            qualifiers: vec![],
            evidence_refs: vec![],
        }
    }


    fn temp_db_path(label: &str) -> std::path::PathBuf {
        let nonce = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos();
        std::env::temp_dir().join(format!("memory-brain-{label}-{}-{nonce}.sqlite", std::process::id()))
    }

    fn remove_db_files(path: &std::path::Path) {
        let _ = std::fs::remove_file(path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }

    #[test]
    fn sqlite_committed_state_survives_close_and_reopen() {
        let path = temp_db_path("reopen");
        let receipt = {
            let mut store = SqliteMemoryStorage::open(&path).unwrap();
            store.create_memory(memory(), &[scope()]).unwrap();
            store.commit_version(CommitRequest {
                memory_id: id("m1"), expected_current_version: None, new_version: version("v1", 1, None),
                idempotency_key: "restart-op".into(), request_digest: "restart-digest".into(),
            }, &[scope()]).unwrap()
        };

        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert_eq!(reopened.read_current(&id("m1"), &[scope()]).unwrap().unwrap().memory_version_id, id("v1"));
        assert_eq!(reopened.resolve_idempotency("restart-op", "restart-digest", &[scope()]).unwrap(), Some(receipt));
        let changes = reopened.list_changes(None, &[scope()], 10).unwrap();
        assert_eq!(changes.records.len(), 1);
        assert_eq!(changes.records[0].commit_sequence, CommitSequence(1));
        drop(reopened);
        remove_db_files(&path);
    }

    // Invoked only by the parent test in a separate process. process::exit bypasses
    // Rust destructors, leaving SQLite to recover an uncommitted WAL transaction.
    #[test]
    fn abrupt_exit_worker() {
        let Ok(path) = std::env::var("MEMORY_SQLITE_CRASH_WORKER_PATH") else { return; };
        let mut store = SqliteMemoryStorage::open(path).unwrap();
        let tx = store.connection.transaction_with_behavior(TransactionBehavior::Immediate).unwrap();

        let mut updated_memory = memory();
        updated_memory.current_version_id = Some(id("v-crash"));
        let scope_json = SqliteMemoryStorage::encode(&vec![scope()]).unwrap();
        let version_json = SqliteMemoryStorage::encode(&version("v-crash", 1, None)).unwrap();
        tx.execute(
            "INSERT INTO versions(version_id, memory_id, version_number, parent_version_id, scope_json, version_json, commit_sequence)
             VALUES ('v-crash', 'm1', 1, NULL, ?1, ?2, 1)",
            params![scope_json, version_json],
        ).unwrap();
        tx.execute(
            "UPDATE memories SET current_version_id = 'v-crash', memory_json = ?1 WHERE memory_id = 'm1'",
            params![SqliteMemoryStorage::encode(&updated_memory).unwrap()],
        ).unwrap();
        tx.execute("INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (1, 'm1', 'v-crash')", []).unwrap();
        let receipt = CommitReceipt {
            memory_id: id("m1"), resulting_version_id: id("v-crash"),
            commit_sequence: CommitSequence(1), idempotency_key: "crash-op".into(),
        };
        tx.execute(
            "INSERT INTO idempotency(idempotency_key, memory_id, request_digest, receipt_json)
             VALUES ('crash-op', 'm1', 'crash-digest', ?1)",
            params![SqliteMemoryStorage::encode(&receipt).unwrap()],
        ).unwrap();

        // Deliberately terminate with the transaction still uncommitted.
        std::process::exit(86);
    }

    #[test]
    fn abrupt_process_exit_rolls_back_entire_uncommitted_commit() {
        let path = temp_db_path("crash");
        {
            let store = SqliteMemoryStorage::open(&path).unwrap();
            let mut store = store;
            store.create_memory(memory(), &[scope()]).unwrap();
        }

        let status = std::process::Command::new(std::env::current_exe().unwrap())
            .args(["--exact", "tests::abrupt_exit_worker", "--nocapture"])
            .env("MEMORY_SQLITE_CRASH_WORKER_PATH", &path)
            .status().unwrap();
        assert_eq!(status.code(), Some(86));

        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert!(reopened.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert_eq!(reopened.read_version(&id("m1"), &id("v-crash"), &[scope()]).unwrap(), None);
        assert_eq!(reopened.resolve_idempotency("crash-op", "crash-digest", &[scope()]).unwrap(), None);
        assert!(reopened.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
        drop(reopened);
        remove_db_files(&path);
    }


    #[test]
    fn independent_connections_serialize_competing_compare_and_swap_writers() {
        use std::sync::{Arc, Barrier};
        use std::thread;

        let path = temp_db_path("cas-race");
        {
            let mut setup = SqliteMemoryStorage::open(&path).unwrap();
            setup.create_memory(memory(), &[scope()]).unwrap();
        }
        let first_store = SqliteMemoryStorage::open(&path).unwrap();
        let second_store = SqliteMemoryStorage::open(&path).unwrap();
        let barrier = Arc::new(Barrier::new(2));

        let first_barrier = barrier.clone();
        let first = thread::spawn(move || {
            let mut store = first_store;
            first_barrier.wait();
            store.commit_version(CommitRequest {
                memory_id: id("m1"), expected_current_version: None,
                new_version: version("v-race-a", 1, None),
                idempotency_key: "race-a".into(), request_digest: "race-a-digest".into(),
            }, &[scope()])
        });

        let second_barrier = barrier.clone();
        let second = thread::spawn(move || {
            let mut store = second_store;
            second_barrier.wait();
            store.commit_version(CommitRequest {
                memory_id: id("m1"), expected_current_version: None,
                new_version: version("v-race-b", 1, None),
                idempotency_key: "race-b".into(), request_digest: "race-b-digest".into(),
            }, &[scope()])
        });

        let first_result = first.join().unwrap();
        let second_result = second.join().unwrap();
        let successes = usize::from(first_result.is_ok()) + usize::from(second_result.is_ok());
        assert_eq!(successes, 1, "exactly one CAS writer may commit");
        let loser = match first_result {
            Err(error) => error,
            Ok(_) => second_result.unwrap_err(),
        };
        assert_eq!(loser, StorageError::StaleVersion);

        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        let current = reopened.read_current(&id("m1"), &[scope()]).unwrap().unwrap();
        assert!(current.memory_version_id == id("v-race-a") || current.memory_version_id == id("v-race-b"));
        let changes = reopened.list_changes(None, &[scope()], 10).unwrap();
        assert_eq!(changes.records.len(), 1);
        drop(reopened);
        remove_db_files(&path);
    }

    #[test]
    fn concurrent_identical_idempotency_requests_replay_one_durable_receipt() {
        use std::sync::{Arc, Barrier};
        use std::thread;

        let path = temp_db_path("idempotency-race");
        {
            let mut setup = SqliteMemoryStorage::open(&path).unwrap();
            setup.create_memory(memory(), &[scope()]).unwrap();
        }
        let first_store = SqliteMemoryStorage::open(&path).unwrap();
        let second_store = SqliteMemoryStorage::open(&path).unwrap();
        let barrier = Arc::new(Barrier::new(2));

        let first_barrier = barrier.clone();
        let first = thread::spawn(move || {
            let mut store = first_store;
            first_barrier.wait();
            store.commit_version(CommitRequest {
                memory_id: id("m1"), expected_current_version: None,
                new_version: version("v-idempotent-race", 1, None),
                idempotency_key: "same-race-key".into(), request_digest: "same-race-digest".into(),
            }, &[scope()])
        });

        let second_barrier = barrier.clone();
        let second = thread::spawn(move || {
            let mut store = second_store;
            second_barrier.wait();
            store.commit_version(CommitRequest {
                memory_id: id("m1"), expected_current_version: None,
                new_version: version("v-idempotent-race", 1, None),
                idempotency_key: "same-race-key".into(), request_digest: "same-race-digest".into(),
            }, &[scope()])
        });

        let first_receipt = first.join().unwrap().unwrap();
        let second_receipt = second.join().unwrap().unwrap();
        assert_eq!(first_receipt, second_receipt);
        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert_eq!(reopened.resolve_idempotency("same-race-key", "same-race-digest", &[scope()]).unwrap(), Some(first_receipt));
        assert_eq!(reopened.list_changes(None, &[scope()], 10).unwrap().records.len(), 1);
        drop(reopened);
        remove_db_files(&path);
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
    fn sqlite_change_pages_filter_scope_before_applying_limit() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let visible_scope = scope();
        let hidden_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };

        for (memory_id, version_id, item_scope) in [
            ("m1", "v1", visible_scope.clone()),
            ("m2", "v2", hidden_scope.clone()),
            ("m3", "v3", hidden_scope),
            ("m4", "v4", visible_scope.clone()),
        ] {
            let mut item = memory();
            item.memory_id = id(memory_id);
            item.scope_refs = vec![item_scope.clone()];
            store.create_memory(item, std::slice::from_ref(&item_scope)).unwrap();

            let mut item_version = version(version_id, 1, None);
            item_version.memory_id = id(memory_id);
            store.commit_version(CommitRequest {
                memory_id: id(memory_id),
                expected_current_version: None,
                new_version: item_version,
                idempotency_key: format!("op-{memory_id}"),
                request_digest: format!("digest-{memory_id}"),
            }, &[item_scope]).unwrap();
        }

        let first = store.list_changes(None, std::slice::from_ref(&visible_scope), 1).unwrap();
        assert_eq!(first.records.len(), 1);
        assert_eq!(first.records[0].memory_id, id("m1"));
        assert_eq!(first.next_cursor, Some(CommitSequence(1)));

        let second = store.list_changes(first.next_cursor, std::slice::from_ref(&visible_scope), 1).unwrap();
        assert_eq!(second.records.len(), 1);
        assert_eq!(second.records[0].memory_id, id("m4"));
        assert_eq!(second.next_cursor, Some(CommitSequence(4)));

        let end = store.list_changes(second.next_cursor, &[visible_scope], 1).unwrap();
        assert!(end.records.is_empty());
        assert_eq!(end.next_cursor, None);
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
    fn file_db_nested_savepoint_rollback_preserves_outer_work() {
        let path = temp_db_path("nested-savepoint");
        let mut store = SqliteMemoryStorage::open(&path).unwrap();
        store.connection.execute_batch(
            "CREATE TABLE rollback_probe (value INTEGER PRIMARY KEY);"
        ).unwrap();

        let mut outer = store.connection
            .transaction_with_behavior(TransactionBehavior::Immediate).unwrap();
        outer.execute("INSERT INTO rollback_probe(value) VALUES (1)", []).unwrap();

        {
            let mut middle = outer.savepoint().unwrap();
            middle.execute("INSERT INTO rollback_probe(value) VALUES (2)", []).unwrap();
            {
                let mut inner = middle.savepoint().unwrap();
                inner.execute("INSERT INTO rollback_probe(value) VALUES (3)", []).unwrap();
                inner.rollback().unwrap();
            }
            middle.commit().unwrap();
        }
        outer.commit().unwrap();

        let values: Vec<i64> = {
            let mut stmt = store.connection
                .prepare("SELECT value FROM rollback_probe ORDER BY value").unwrap();
            stmt.query_map([], |row| row.get(0)).unwrap()
                .collect::<Result<Vec<_>, _>>().unwrap()
        };
        assert_eq!(values, vec![1, 2]);
        drop(store);
        remove_db_files(&path);
    }

    #[test]
    fn file_db_busy_timeout_bounds_wait_for_long_immediate_transaction() {
        use std::thread;

        let path = temp_db_path("busy-timeout");
        let mut blocker = SqliteMemoryStorage::open(&path).unwrap();
        blocker.create_memory(memory(), &[scope()]).unwrap();
        let mut contender = SqliteMemoryStorage::open(&path).unwrap();
        contender.connection.busy_timeout(Duration::from_millis(100)).unwrap();

        let held = blocker.connection
            .transaction_with_behavior(TransactionBehavior::Immediate).unwrap();
        // BEGIN IMMEDIATE acquires the write reservation even without a row update.
        thread::sleep(Duration::from_millis(150));

        let request = CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v-busy", 1, None),
            idempotency_key: "busy-op".into(),
            request_digest: "busy-digest".into(),
        };
        let started = std::time::Instant::now();
        let blocked = contender.commit_version(request.clone(), &[scope()]);
        let elapsed = started.elapsed();
        assert_eq!(blocked, Err(StorageError::TransactionUnavailable));
        assert!(elapsed >= Duration::from_millis(80), "busy timeout returned too early: {elapsed:?}");
        assert!(elapsed < Duration::from_secs(2), "busy timeout did not bound lock wait: {elapsed:?}");

        held.rollback().unwrap();
        let receipt = contender.commit_version(request, &[scope()]).unwrap();
        assert_eq!(receipt.resulting_version_id, id("v-busy"));

        drop(contender);
        drop(blocker);
        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert_eq!(reopened.read_current(&id("m1"), &[scope()]).unwrap().unwrap().memory_version_id, id("v-busy"));
        drop(reopened);
        remove_db_files(&path);
    }

    #[test]
    fn file_db_interrupted_commit_keeps_version_pointer_log_and_idempotency_consistent() {
        let path = temp_db_path("interrupted-write");
        let mut store = SqliteMemoryStorage::open(&path).unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        store.connection.execute_batch(
            "CREATE TRIGGER interrupt_commit_log
             BEFORE INSERT ON commit_log
             BEGIN SELECT RAISE(ABORT, 'injected write interruption'); END;"
        ).unwrap();

        let result = store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v-interrupted", 1, None),
            idempotency_key: "interrupted-op".into(),
            request_digest: "interrupted-digest".into(),
        }, &[scope()]);
        assert_eq!(result, Err(StorageError::TransactionUnavailable));

        drop(store);
        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert!(reopened.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert_eq!(reopened.read_version(&id("m1"), &id("v-interrupted"), &[scope()]).unwrap(), None);
        assert_eq!(reopened.resolve_idempotency("interrupted-op", "interrupted-digest", &[scope()]).unwrap(), None);
        assert!(reopened.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
        drop(reopened);
        remove_db_files(&path);
    }

    #[test]
    fn file_db_unwinding_worker_releases_open_transaction_without_partial_state() {
        let path = temp_db_path("abnormal-release");
        {
            let mut setup = SqliteMemoryStorage::open(&path).unwrap();
            setup.create_memory(memory(), &[scope()]).unwrap();
        }

        let worker_path = path.clone();
        let worker = std::thread::spawn(move || {
            let mut store = SqliteMemoryStorage::open(&worker_path).unwrap();
            let tx = store.connection
                .transaction_with_behavior(TransactionBehavior::Immediate).unwrap();
            let scope_json = SqliteMemoryStorage::encode(&vec![scope()]).unwrap();
            let version_json = SqliteMemoryStorage::encode(&version("v-unwind", 1, None)).unwrap();
            tx.execute(
                "INSERT INTO versions(version_id, memory_id, version_number, parent_version_id, scope_json, version_json, commit_sequence)
                 VALUES ('v-unwind', 'm1', 1, NULL, ?1, ?2, 1)",
                params![scope_json, version_json],
            ).unwrap();
            tx.execute(
                "UPDATE memories SET current_version_id = 'v-unwind' WHERE memory_id = 'm1'",
                [],
            ).unwrap();
            tx.execute(
                "INSERT INTO commit_log(commit_sequence, memory_id, version_id) VALUES (1, 'm1', 'v-unwind')",
                [],
            ).unwrap();
            panic!("simulate worker panic while connection owns an uncommitted transaction");
        });
        assert!(worker.join().is_err());

        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert!(reopened.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert_eq!(reopened.read_version(&id("m1"), &id("v-unwind"), &[scope()]).unwrap(), None);
        assert!(reopened.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
        drop(reopened);
        remove_db_files(&path);
    }

    #[test]
    fn sqlite_rejects_invalid_memory_and_orphan_initial_version_pointer() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();

        let mut invalid_memory = memory();
        invalid_memory.memory_kind.clear();
        assert_eq!(
            store.create_memory(invalid_memory, &[scope()]),
            Err(StorageError::InvalidSchema)
        );
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());

        let mut orphan_pointer = memory();
        orphan_pointer.current_version_id = Some(id("v-orphan"));
        assert_eq!(
            store.create_memory(orphan_pointer, &[scope()]),
            Err(StorageError::InvalidReference)
        );
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
    }

    #[test]
    fn sqlite_rejects_invalid_version_fields_before_writing_any_commit_state() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        let mut missing_digest = version("v-invalid-digest", 1, None);
        missing_digest.content_digest.clear();
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: missing_digest,
                idempotency_key: "invalid-digest-op".into(),
                request_digest: "invalid-digest".into(),
            }, &[scope()]),
            Err(StorageError::InvalidSchema)
        );

        let mut missing_created_at = version("v-invalid-time", 1, None);
        missing_created_at.created_at.clear();
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: missing_created_at,
                idempotency_key: "invalid-time-op".into(),
                request_digest: "invalid-time".into(),
            }, &[scope()]),
            Err(StorageError::InvalidSchema)
        );

        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert_eq!(store.read_version(&id("m1"), &id("v-invalid-digest"), &[scope()]).unwrap(), None);
        assert_eq!(store.resolve_idempotency("invalid-digest-op", "invalid-digest", &[scope()]).unwrap(), None);
        assert!(store.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
    }

    #[test]
    fn sqlite_rejects_empty_idempotency_key_or_request_digest() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: version("v-empty-key", 1, None),
                idempotency_key: String::new(),
                request_digest: "digest".into(),
            }, &[scope()]),
            Err(StorageError::InvalidSchema)
        );

        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: version("v-empty-digest", 1, None),
                idempotency_key: "empty-digest-op".into(),
                request_digest: String::new(),
            }, &[scope()]),
            Err(StorageError::InvalidSchema)
        );

        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert!(store.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
    }

    #[test]
    fn sqlite_scope_checks_cover_current_history_and_idempotency_receipt_reads() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v1", 1, None),
            idempotency_key: "scope-read-op".into(),
            request_digest: "scope-read-digest".into(),
        }, &[scope()]).unwrap();

        let other = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };
        assert_eq!(
            store.read_current(&id("m1"), std::slice::from_ref(&other)),
            Err(StorageError::ScopeMismatch)
        );
        assert_eq!(
            store.read_version(&id("m1"), &id("v1"), std::slice::from_ref(&other)),
            Err(StorageError::ScopeMismatch)
        );
        assert_eq!(
            store.resolve_idempotency("scope-read-op", "scope-read-digest", &[other]),
            Err(StorageError::ScopeMismatch)
        );
    }

    #[test]
    fn sqlite_idempotency_digest_mismatch_conflicts_for_commit_and_receipt_lookup() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v1", 1, None),
            idempotency_key: "digest-conflict".into(),
            request_digest: "digest-a".into(),
        }, &[scope()]).unwrap();

        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: version("v1", 1, None),
                idempotency_key: "digest-conflict".into(),
                request_digest: "digest-b".into(),
            }, &[scope()]),
            Err(StorageError::IdempotencyConflict)
        );
        assert_eq!(
            store.resolve_idempotency("digest-conflict", "digest-b", &[scope()]),
            Err(StorageError::IdempotencyConflict)
        );
        assert_eq!(store.list_changes(None, &[scope()], 10).unwrap().records.len(), 1);
    }

    #[test]
    fn independent_connections_serialize_conflicting_idempotency_payloads() {
        use std::sync::{Arc, Barrier};
        use std::thread;

        let path = temp_db_path("idempotency-conflict-race");
        {
            let mut setup = SqliteMemoryStorage::open(&path).unwrap();
            setup.create_memory(memory(), &[scope()]).unwrap();
        }
        let first_store = SqliteMemoryStorage::open(&path).unwrap();
        let second_store = SqliteMemoryStorage::open(&path).unwrap();
        let barrier = Arc::new(Barrier::new(2));

        let first_barrier = barrier.clone();
        let first = thread::spawn(move || {
            let mut store = first_store;
            first_barrier.wait();
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: version("v-conflict-a", 1, None),
                idempotency_key: "same-conflict-key".into(),
                request_digest: "payload-a".into(),
            }, &[scope()])
        });

        let second_barrier = barrier.clone();
        let second = thread::spawn(move || {
            let mut store = second_store;
            second_barrier.wait();
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version: version("v-conflict-b", 1, None),
                idempotency_key: "same-conflict-key".into(),
                request_digest: "payload-b".into(),
            }, &[scope()])
        });

        let first_result = first.join().unwrap();
        let second_result = second.join().unwrap();
        assert_eq!(
            usize::from(first_result.is_ok()) + usize::from(second_result.is_ok()),
            1,
            "only one payload may claim an idempotency key"
        );
        let first_won = first_result.is_ok();
        let winner_digest = if first_won { "payload-a" } else { "payload-b" };
        let loser = if first_won { second_result.unwrap_err() } else { first_result.unwrap_err() };
        assert_eq!(loser, StorageError::IdempotencyConflict);

        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        assert_eq!(reopened.list_changes(None, &[scope()], 10).unwrap().records.len(), 1);
        let receipt = reopened.resolve_idempotency(
            "same-conflict-key",
            winner_digest,
            &[scope()],
        ).unwrap();
        assert!(receipt.is_some());
        drop(reopened);
        remove_db_files(&path);
    }

    #[test]
    fn file_backed_connection_applies_required_sqlite_pragmas() {
        let path = temp_db_path("pragma-profile");
        let store = SqliteMemoryStorage::open(&path).unwrap();

        let journal_mode: String = store.connection.query_row(
            "PRAGMA journal_mode", [], |row| row.get(0)
        ).unwrap();
        let synchronous: i64 = store.connection.query_row(
            "PRAGMA synchronous", [], |row| row.get(0)
        ).unwrap();
        let foreign_keys: i64 = store.connection.query_row(
            "PRAGMA foreign_keys", [], |row| row.get(0)
        ).unwrap();
        let busy_timeout: i64 = store.connection.query_row(
            "PRAGMA busy_timeout", [], |row| row.get(0)
        ).unwrap();

        assert_eq!(journal_mode.to_ascii_lowercase(), "wal");
        assert_eq!(synchronous, 2, "SQLite FULL synchronous mode");
        assert_eq!(foreign_keys, 1);
        assert_eq!(busy_timeout, 5000);

        drop(store);
        remove_db_files(&path);
    }

    #[test]
    fn sqlite_filters_nested_claims_by_the_callers_scope() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let first_scope = scope();
        let second_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };

        let mut multi_scope_memory = memory();
        multi_scope_memory.scope_refs = vec![first_scope.clone(), second_scope.clone()];
        store.create_memory(
            multi_scope_memory,
            &[first_scope.clone(), second_scope.clone()],
        ).unwrap();

        let mut new_version = version("v-multi-scope", 1, None);
        new_version.claims = vec![claim_in_scope("claim-s2", second_scope.clone())];
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version,
            idempotency_key: "multi-scope-claim".into(),
            request_digest: "multi-scope-claim-digest".into(),
        }, &[first_scope.clone(), second_scope.clone()]).unwrap();

        let first_reader = store.read_current(&id("m1"), &[first_scope]).unwrap().unwrap();
        assert!(first_reader.claims.is_empty(), "scope s1 must not receive the s2-only Claim");

        let second_reader = store.read_current(&id("m1"), std::slice::from_ref(&second_scope)).unwrap().unwrap();
        assert_eq!(second_reader.claims.len(), 1);
        assert_eq!(second_reader.claims[0].claim_id, id("claim-s2"));

        let historical = store.read_version(
            &id("m1"),
            &id("v-multi-scope"),
            &[second_scope],
        ).unwrap().unwrap();
        assert_eq!(historical.claims.len(), 1);
    }

    #[test]
    fn sqlite_rejects_claims_outside_the_parent_memory_scope() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        let other_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };
        let mut new_version = version("v-cross-scope-claim", 1, None);
        new_version.claims = vec![claim_in_scope("claim-s2", other_scope)];
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version,
                idempotency_key: "cross-scope-claim".into(),
                request_digest: "cross-scope-claim-digest".into(),
            }, &[scope()]),
            Err(StorageError::ScopeMismatch)
        );
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert!(store.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
    }

    #[test]
    fn sqlite_rejects_mixed_parent_and_foreign_claim_scopes_before_commit() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        let other_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };
        let mut mixed_claim = claim_in_scope("claim-mixed", scope());
        mixed_claim.scope_refs.push(other_scope);
        let mut new_version = version("v-mixed-scope", 1, None);
        new_version.claims = vec![mixed_claim];

        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version,
                idempotency_key: "mixed-scope-op".into(),
                request_digest: "mixed-scope-digest".into(),
            }, &[scope()]),
            Err(StorageError::ScopeMismatch)
        );
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert_eq!(store.read_version(&id("m1"), &id("v-mixed-scope"), &[scope()]).unwrap(), None);
        assert_eq!(store.resolve_idempotency("mixed-scope-op", "mixed-scope-digest", &[scope()]).unwrap(), None);
        assert!(store.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
    }

    #[test]
    fn sqlite_rejects_persisted_claim_with_mixed_parent_and_foreign_scopes() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        let mut new_version = version("v-persisted-mixed-scope", 1, None);
        new_version.claims = vec![claim_in_scope("claim-persisted-mixed", scope())];
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version,
            idempotency_key: "persisted-mixed-op".into(),
            request_digest: "persisted-mixed-digest".into(),
        }, &[scope()]).unwrap();

        let other_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };
        let version_json: String = store.connection.query_row(
            "SELECT version_json FROM versions WHERE version_id = 'v-persisted-mixed-scope'",
            [],
            |row| row.get(0),
        ).unwrap();
        let mut persisted: MemoryVersion = SqliteMemoryStorage::decode(&version_json).unwrap();
        persisted.claims[0].scope_refs.push(other_scope);
        let corrupted = SqliteMemoryStorage::encode(&persisted).unwrap();
        store.connection.execute(
            "UPDATE versions SET version_json = ?1 WHERE version_id = 'v-persisted-mixed-scope'",
            params![corrupted],
        ).unwrap();

        assert_eq!(
            store.read_current(&id("m1"), &[scope()]),
            Err(StorageError::InvalidSchema)
        );
    }

    #[test]
    fn sqlite_rejects_malformed_nested_claims_before_commit() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        let mut malformed = claim_in_scope("claim-invalid", scope());
        malformed.predicate.clear();
        let mut new_version = version("v-invalid-claim", 1, None);
        new_version.claims = vec![malformed];
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version,
                idempotency_key: "invalid-claim".into(),
                request_digest: "invalid-claim-digest".into(),
            }, &[scope()]),
            Err(StorageError::InvalidSchema)
        );
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
    }

    #[test]
    fn sqlite_storage_entry_points_reject_empty_and_malformed_scope_sets() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let empty: Vec<ScopeRef> = vec![];
        let malformed = ScopeRef {
            scope_id: id("s1"),
            scope_kind: ScopeKind::User,
            namespace_key: String::new(),
        };

        assert_eq!(store.create_memory(memory(), &empty), Err(StorageError::InvalidSchema));
        assert_eq!(store.create_memory(memory(), std::slice::from_ref(&malformed)), Err(StorageError::InvalidSchema));
        assert_eq!(store.read_current(&id("missing"), &empty), Err(StorageError::InvalidSchema));
        assert_eq!(store.read_version(&id("missing"), &id("missing-v"), std::slice::from_ref(&malformed)), Err(StorageError::InvalidSchema));
        assert_eq!(store.commit_version(CommitRequest {
            memory_id: id("missing"),
            expected_current_version: None,
            new_version: version("missing-v", 1, None),
            idempotency_key: "scope-validation".into(),
            request_digest: "scope-validation".into(),
        }, &empty), Err(StorageError::InvalidSchema));
        assert_eq!(store.list_changes(None, &empty, 0), Err(StorageError::InvalidSchema));
        assert_eq!(store.resolve_idempotency("missing", "digest", &[malformed]), Err(StorageError::InvalidSchema));
    }

    #[test]
    fn sqlite_change_listing_surfaces_corrupt_scope_metadata_instead_of_silently_skipping_it() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v1", 1, None),
            idempotency_key: "corrupt-scope-op".into(),
            request_digest: "corrupt-scope-digest".into(),
        }, &[scope()]).unwrap();

        store.connection.execute(
            "UPDATE memories SET scope_json = 'not-json' WHERE memory_id = 'm1'",
            [],
        ).unwrap();

        assert_eq!(
            store.list_changes(None, &[scope()], 10),
            Err(StorageError::InvalidSchema)
        );
    }

    // Worker mode for the parent test below. Each invocation is a separate OS process
    // with its own SQLite Connection; the gate synchronizes the competing CAS start.
    #[test]
    fn multi_process_cas_worker() {
        let (Ok(path), Ok(gate), Ok(result_path), Ok(version_id)) = (
            std::env::var("MEMORY_SQLITE_MP_CAS_PATH"),
            std::env::var("MEMORY_SQLITE_MP_CAS_GATE"),
            std::env::var("MEMORY_SQLITE_MP_CAS_RESULT"),
            std::env::var("MEMORY_SQLITE_MP_CAS_VERSION"),
        ) else {
            return;
        };

        let mut store = SqliteMemoryStorage::open(path).unwrap();
        let deadline = std::time::Instant::now() + Duration::from_secs(10);
        while !std::path::Path::new(&gate).exists() {
            assert!(std::time::Instant::now() < deadline, "timed out waiting for multiprocess CAS gate");
            std::thread::sleep(Duration::from_millis(5));
        }

        let result = store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version(&version_id, 1, None),
            idempotency_key: format!("mp-{version_id}"),
            request_digest: format!("mp-digest-{version_id}"),
        }, &[scope()]);
        let outcome = match result {
            Ok(_) => "success",
            Err(StorageError::StaleVersion) => "stale",
            Err(other) => panic!("unexpected multiprocess CAS result: {other:?}"),
        };
        std::fs::write(result_path, outcome).unwrap();
    }

    #[test]
    fn separate_processes_serialize_competing_file_backed_cas_writers() {
        let path = temp_db_path("multiprocess-cas");
        let gate = path.with_extension("go");
        let first_result = path.with_extension("first-result");
        let second_result = path.with_extension("second-result");
        {
            let mut setup = SqliteMemoryStorage::open(&path).unwrap();
            setup.create_memory(memory(), &[scope()]).unwrap();
        }

        let executable = std::env::current_exe().unwrap();
        let spawn_worker = |version_id: &str, result_path: &std::path::Path| {
            std::process::Command::new(&executable)
                .args(["--exact", "tests::multi_process_cas_worker", "--nocapture"])
                .env("MEMORY_SQLITE_MP_CAS_PATH", &path)
                .env("MEMORY_SQLITE_MP_CAS_GATE", &gate)
                .env("MEMORY_SQLITE_MP_CAS_RESULT", result_path)
                .env("MEMORY_SQLITE_MP_CAS_VERSION", version_id)
                .spawn()
                .unwrap()
        };
        let mut first = spawn_worker("v-mp-a", &first_result);
        let mut second = spawn_worker("v-mp-b", &second_result);
        std::fs::write(&gate, "go").unwrap();

        assert!(first.wait().unwrap().success());
        assert!(second.wait().unwrap().success());
        let outcomes = [
            std::fs::read_to_string(&first_result).unwrap(),
            std::fs::read_to_string(&second_result).unwrap(),
        ];
        assert_eq!(outcomes.iter().filter(|value| value.as_str() == "success").count(), 1);
        assert_eq!(outcomes.iter().filter(|value| value.as_str() == "stale").count(), 1);

        let reopened = SqliteMemoryStorage::open(&path).unwrap();
        let current = reopened.read_current(&id("m1"), &[scope()]).unwrap().unwrap();
        assert!(current.memory_version_id == id("v-mp-a") || current.memory_version_id == id("v-mp-b"));
        assert_eq!(reopened.list_changes(None, &[scope()], 10).unwrap().records.len(), 1);
        drop(reopened);

        remove_db_files(&path);
        let _ = std::fs::remove_file(gate);
        let _ = std::fs::remove_file(first_result);
        let _ = std::fs::remove_file(second_result);
    }


    #[test]
    fn sqlite_denies_fresh_cross_scope_write_without_persisting_any_commit_state() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();
        let foreign_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };

        let result = store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v-denied-cross-scope", 1, None),
            idempotency_key: "fresh-foreign-write".into(),
            request_digest: "fresh-foreign-write-digest".into(),
        }, &[foreign_scope]);
        assert_eq!(result, Err(StorageError::ScopeMismatch));

        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
        assert_eq!(
            store.read_version(&id("m1"), &id("v-denied-cross-scope"), &[scope()]).unwrap(),
            None
        );
        assert_eq!(
            store.resolve_idempotency("fresh-foreign-write", "fresh-foreign-write-digest", &[scope()]).unwrap(),
            None
        );
        assert!(store.list_changes(None, &[scope()], 10).unwrap().records.is_empty());
    }

    #[test]
    fn sqlite_change_pages_with_limit_two_preserve_order_without_skips_or_duplicates() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let visible_scope = scope();
        let hidden_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };

        for (memory_id, version_id, item_scope) in [
            ("m1", "v1", visible_scope.clone()),
            ("m2", "v2", hidden_scope.clone()),
            ("m3", "v3", hidden_scope.clone()),
            ("m4", "v4", visible_scope.clone()),
            ("m5", "v5", visible_scope.clone()),
            ("m6", "v6", hidden_scope),
            ("m7", "v7", visible_scope.clone()),
        ] {
            let mut item = memory();
            item.memory_id = id(memory_id);
            item.scope_refs = vec![item_scope.clone()];
            store.create_memory(item, std::slice::from_ref(&item_scope)).unwrap();

            let mut item_version = version(version_id, 1, None);
            item_version.memory_id = id(memory_id);
            store.commit_version(CommitRequest {
                memory_id: id(memory_id),
                expected_current_version: None,
                new_version: item_version,
                idempotency_key: format!("page-two-{memory_id}"),
                request_digest: format!("page-two-digest-{memory_id}"),
            }, &[item_scope]).unwrap();
        }

        let first = store.list_changes(None, std::slice::from_ref(&visible_scope), 2).unwrap();
        assert_eq!(
            first.records.iter().map(|record| record.memory_id.clone()).collect::<Vec<_>>(),
            vec![id("m1"), id("m4")]
        );
        assert_eq!(first.next_cursor, Some(CommitSequence(4)));

        let second = store.list_changes(first.next_cursor, std::slice::from_ref(&visible_scope), 2).unwrap();
        assert_eq!(
            second.records.iter().map(|record| record.memory_id.clone()).collect::<Vec<_>>(),
            vec![id("m5"), id("m7")]
        );
        assert_eq!(second.next_cursor, Some(CommitSequence(7)));

        let end = store.list_changes(second.next_cursor, &[visible_scope], 2).unwrap();
        assert!(end.records.is_empty());
        assert_eq!(end.next_cursor, None);
    }

    #[test]
    fn sqlite_rejects_claim_scope_outside_callers_scope_even_when_parent_contains_it() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let first_scope = scope();
        let second_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };
        let mut multi_scope_memory = memory();
        multi_scope_memory.scope_refs = vec![first_scope.clone(), second_scope.clone()];
        store.create_memory(
            multi_scope_memory,
            &[first_scope.clone(), second_scope.clone()],
        ).unwrap();

        let mut new_version = version("v-unauthorized-claim-scope", 1, None);
        new_version.claims = vec![claim_in_scope("claim-s2", second_scope)];
        assert_eq!(
            store.commit_version(CommitRequest {
                memory_id: id("m1"),
                expected_current_version: None,
                new_version,
                idempotency_key: "unauthorized-claim-scope".into(),
                request_digest: "unauthorized-claim-scope-digest".into(),
            }, std::slice::from_ref(&first_scope)),
            Err(StorageError::ScopeMismatch)
        );
        assert!(store.read_current(&id("m1"), std::slice::from_ref(&first_scope)).unwrap().is_none());
        assert_eq!(
            store.resolve_idempotency("unauthorized-claim-scope", "unauthorized-claim-scope-digest", std::slice::from_ref(&first_scope)).unwrap(),
            None
        );
        assert!(store.list_changes(None, &[first_scope], 10).unwrap().records.is_empty());
    }

    #[test]
    fn sqlite_hides_entire_multiscope_claim_from_partial_scope_reader() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        let first_scope = scope();
        let second_scope = ScopeRef {
            scope_id: id("s2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:s2".into(),
        };
        let mut multi_scope_memory = memory();
        multi_scope_memory.scope_refs = vec![first_scope.clone(), second_scope.clone()];
        store.create_memory(
            multi_scope_memory,
            &[first_scope.clone(), second_scope.clone()],
        ).unwrap();

        let mut new_version = version("v-multiscope-claim", 1, None);
        let mut multi_scope_claim = claim_in_scope("claim-both", first_scope.clone());
        multi_scope_claim.scope_refs.push(second_scope.clone());
        new_version.claims = vec![multi_scope_claim];
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version,
            idempotency_key: "multiscope-claim".into(),
            request_digest: "multiscope-claim-digest".into(),
        }, &[first_scope.clone(), second_scope.clone()]).unwrap();

        let partial_reader = store.read_current(&id("m1"), std::slice::from_ref(&first_scope)).unwrap().unwrap();
        assert!(partial_reader.claims.is_empty(), "partial scope access must not disclose a partial Claim");
        let full_reader = store.read_current(&id("m1"), &[first_scope, second_scope]).unwrap().unwrap();
        assert_eq!(full_reader.claims.len(), 1);
        assert_eq!(full_reader.claims[0].claim_id, id("claim-both"));
    }


    #[test]
    fn sqlite_prepare_keeps_current_version_unchanged() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        let prepared = store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v1-prepared", 1, None),
            idempotency_key: "t1-op".into(),
            request_digest: "t1-digest".into(),
            publication_id: "t1-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        assert_eq!(prepared.prepared_version_id, id("v1-prepared"));
        assert!(
            store.read_current(&id("m1"), &[scope()]).unwrap().is_none(),
            "prepare must not advance the current-version pointer"
        );

        let current_id: Option<String> = store.connection.query_row(
            "SELECT current_version_id FROM memories WHERE memory_id = 'm1'",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(current_id, None);
    }

    #[test]
    fn sqlite_prepare_hides_version_from_read_version() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v2-hidden", 1, None),
            idempotency_key: "t2-op".into(),
            request_digest: "t2-digest".into(),
            publication_id: "t2-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        assert_eq!(
            store.read_version(&id("m1"), &id("v2-hidden"), &[scope()]).unwrap(),
            None,
            "PreparedHidden versions must not be disclosed by read_version"
        );
    }

    #[test]
    fn sqlite_read_version_keeps_legacy_versions_visible() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v3-legacy", 1, None),
            idempotency_key: "t3-legacy-op".into(),
            request_digest: "t3-legacy-digest".into(),
        }, &[scope()]).unwrap();

        let preparation_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM publication_preparations
             WHERE version_id = 'v3-legacy'",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(preparation_count, 0);

        let visible = store.read_version(
            &id("m1"),
            &id("v3-legacy"),
            &[scope()],
        ).unwrap();

        assert_eq!(
            visible.unwrap().memory_version_id,
            id("v3-legacy"),
            "legacy versions without a preparation row must remain readable"
        );
    }

    #[test]
    fn sqlite_prepare_does_not_add_change_log_entries() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v4-hidden", 1, None),
            idempotency_key: "t4-op".into(),
            request_digest: "t4-digest".into(),
            publication_id: "t4-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        let changes = store.list_changes(None, &[scope()], 10).unwrap();
        assert!(
            changes.records.is_empty(),
            "a prepared version must not appear in the public change log"
        );

        let log_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM commit_log WHERE version_id = 'v4-hidden'",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(log_count, 0);
    }

    #[test]
    fn sqlite_publish_makes_prepared_version_current_and_readable() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v5-publish", 1, None),
            idempotency_key: "t5-op".into(),
            request_digest: "t5-digest".into(),
            publication_id: "t5-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        let receipt = store.publish_prepared(
            "t5-publication",
            None,
            &[scope()],
        ).unwrap();

        assert_eq!(receipt.memory_id, id("m1"));
        assert_eq!(receipt.resulting_version_id, id("v5-publish"));
        assert_eq!(receipt.commit_sequence, CommitSequence(1));

        assert_eq!(
            store.read_current(&id("m1"), &[scope()])
                .unwrap().unwrap().memory_version_id,
            id("v5-publish")
        );
        assert_eq!(
            store.read_version(&id("m1"), &id("v5-publish"), &[scope()])
                .unwrap().unwrap().memory_version_id,
            id("v5-publish")
        );

        let state: String = store.connection.query_row(
            "SELECT state FROM publication_preparations
             WHERE publication_id = 't5-publication'",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(state, "Published");
    }

    #[test]
    fn sqlite_publish_allocates_sequence_only_at_publish_time() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        // 先提交一个正式版本，确保 MAX 不只是空表的 NULL。
        let first = store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v6-base", 1, None),
            idempotency_key: "t6-base-op".into(),
            request_digest: "t6-base-digest".into(),
        }, &[scope()]).unwrap();
        assert_eq!(first.commit_sequence, CommitSequence(1));

        let max_before: i64 = store.connection.query_row(
            "SELECT COALESCE(MAX(commit_sequence), 0) FROM commit_log",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(max_before, 1);

        // 两次 prepare 均不得推进正式 commit_log 序列。
        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: Some(id("v6-base")),
            new_version: version("v6-prepared-a", 2, Some("v6-base")),
            idempotency_key: "t6-a-op".into(),
            request_digest: "t6-a-digest".into(),
            publication_id: "t6-a-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: Some(id("v6-base")),
            new_version: version("v6-prepared-b", 2, Some("v6-base")),
            idempotency_key: "t6-b-op".into(),
            request_digest: "t6-b-digest".into(),
            publication_id: "t6-b-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        let max_after_prepare: i64 = store.connection.query_row(
            "SELECT COALESCE(MAX(commit_sequence), 0) FROM commit_log",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(
            max_after_prepare,
            max_before,
            "prepare must not consume a formal commit_log sequence"
        );

        let published = store.publish_prepared(
            "t6-a-publication",
            Some(id("v6-base")),
            &[scope()],
        ).unwrap();

        assert_eq!(published.commit_sequence, CommitSequence(2));

        let max_after_publish: i64 = store.connection.query_row(
            "SELECT COALESCE(MAX(commit_sequence), 0) FROM commit_log",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(max_after_publish, 2);
    }

    #[test]
    fn sqlite_prepare_replay_returns_same_receipt() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        let request = PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v7-replay", 1, None),
            idempotency_key: "t7-op".into(),
            request_digest: "t7-digest".into(),
            publication_id: "t7-publication".into(),
            generation: 7,
        };

        let first = store.prepare_version(request.clone(), &[scope()]).unwrap();
        let replay = store.prepare_version(request, &[scope()]).unwrap();

        assert_eq!(first, replay);

        let versions: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM versions WHERE version_id = 'v7-replay'",
            [],
            |row| row.get(0),
        ).unwrap();
        let preparations: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM publication_preparations
             WHERE publication_id = 't7-publication'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(versions, 1);
        assert_eq!(preparations, 1);
        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());
    }

    #[test]
    fn sqlite_prepare_rejects_idempotency_digest_conflict() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v8-original", 1, None),
            idempotency_key: "t8-shared-op".into(),
            request_digest: "t8-original-digest".into(),
            publication_id: "t8-original-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        let result = store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v8-conflict", 1, None),
            idempotency_key: "t8-shared-op".into(),
            request_digest: "t8-different-digest".into(),
            publication_id: "t8-conflict-publication".into(),
            generation: 1,
        }, &[scope()]);

        assert_eq!(result, Err(StorageError::IdempotencyConflict));

        let version_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM versions WHERE version_id IN
             ('v8-original', 'v8-conflict')",
            [],
            |row| row.get(0),
        ).unwrap();
        let preparation_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM publication_preparations
             WHERE idempotency_key = 't8-shared-op'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(version_count, 1);
        assert_eq!(preparation_count, 1);
    }

    #[test]
    fn sqlite_publish_replay_returns_original_receipt() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v9-publish-replay", 1, None),
            idempotency_key: "t9-op".into(),
            request_digest: "t9-digest".into(),
            publication_id: "t9-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        let first = store.publish_prepared("t9-publication", None, &[scope()]).unwrap();
        let replay = store.publish_prepared("t9-publication", None, &[scope()]).unwrap();

        assert_eq!(first, replay);

        let log_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM commit_log
             WHERE version_id = 'v9-publish-replay'",
            [],
            |row| row.get(0),
        ).unwrap();
        let idempotency_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM idempotency WHERE idempotency_key = 't9-op'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(log_count, 1, "replay must not insert a second commit_log row");
        assert_eq!(idempotency_count, 1);
        assert_eq!(first.commit_sequence, CommitSequence(1));
    }

    #[test]
    fn sqlite_publish_rejects_stale_parent_without_partial_commit() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v10-base", 1, None),
            idempotency_key: "t10-base-op".into(),
            request_digest: "t10-base-digest".into(),
        }, &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: Some(id("v10-base")),
            new_version: version("v10-prepared", 2, Some("v10-base")),
            idempotency_key: "t10-prepared-op".into(),
            request_digest: "t10-prepared-digest".into(),
            publication_id: "t10-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        // 兼容路径先提交另一条 successor，令 prepared parent 变旧。
        store.commit_version(CommitRequest {
            memory_id: id("m1"),
            expected_current_version: Some(id("v10-base")),
            new_version: version("v10-competitor", 2, Some("v10-base")),
            idempotency_key: "t10-competitor-op".into(),
            request_digest: "t10-competitor-digest".into(),
        }, &[scope()]).unwrap();

        let result = store.publish_prepared(
            "t10-publication",
            Some(id("v10-base")),
            &[scope()],
        );
        assert_eq!(result, Err(StorageError::StaleVersion));

        assert_eq!(
            store.read_current(&id("m1"), &[scope()])
                .unwrap().unwrap().memory_version_id,
            id("v10-competitor")
        );
        assert_eq!(
            store.read_version(&id("m1"), &id("v10-prepared"), &[scope()])
                .unwrap(),
            None,
            "failed publication must leave the prepared version hidden"
        );

        let prepared_log_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM commit_log WHERE version_id = 'v10-prepared'",
            [],
            |row| row.get(0),
        ).unwrap();
        let prepared_state: String = store.connection.query_row(
            "SELECT state FROM publication_preparations
             WHERE publication_id = 't10-publication'",
            [],
            |row| row.get(0),
        ).unwrap();

        assert_eq!(prepared_log_count, 0);
        assert_eq!(prepared_state, "PreparedHidden");

        let total_log_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM commit_log",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(total_log_count, 2);
    }

    #[test]
    fn sqlite_multiple_preparations_reserve_unique_negative_sequences() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v11-a", 1, None),
            idempotency_key: "t11-a-op".into(),
            request_digest: "t11-a-digest".into(),
            publication_id: "t11-a-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v11-b", 1, None),
            idempotency_key: "t11-b-op".into(),
            request_digest: "t11-b-digest".into(),
            publication_id: "t11-b-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        let mut stmt = store.connection.prepare(
            "SELECT commit_sequence FROM versions
             WHERE version_id IN ('v11-a', 'v11-b')
             ORDER BY version_id",
        ).unwrap();

        let values: Vec<i64> = stmt.query_map([], |row| row.get(0))
            .unwrap()
            .collect::<Result<Vec<_>, _>>()
            .unwrap();

        assert_eq!(values.len(), 2);
        assert!(values.iter().all(|value| *value < 0));
        assert_ne!(
            values[0],
            values[1],
            "each prepared version must reserve a distinct negative commit_sequence"
        );

        let log_max: i64 = store.connection.query_row(
            "SELECT COALESCE(MAX(commit_sequence), 0) FROM commit_log",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(log_max, 0, "hidden preparations must not enter commit_log");
    }

    #[test]
    fn sqlite_publish_rejects_duplicate_publication_and_suppressed_state() {
        let mut store = SqliteMemoryStorage::in_memory().unwrap();
        store.create_memory(memory(), &[scope()]).unwrap();

        store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v12-original", 1, None),
            idempotency_key: "t12-original-op".into(),
            request_digest: "t12-original-digest".into(),
            publication_id: "t12-shared-publication".into(),
            generation: 1,
        }, &[scope()]).unwrap();

        // publication_id 是唯一键，第二个 preparation 必须被拒绝。
        let duplicate_publication = store.prepare_version(PrepareRequest {
            memory_id: id("m1"),
            expected_current_version: None,
            new_version: version("v12-duplicate", 1, None),
            idempotency_key: "t12-duplicate-op".into(),
            request_digest: "t12-duplicate-digest".into(),
            publication_id: "t12-shared-publication".into(),
            generation: 2,
        }, &[scope()]);

        assert_eq!(
            duplicate_publication,
            Err(StorageError::PublicationStateConflict)
        );

        // 当前没有 suppress API；测试直接将 preparation 状态置为 Suppressed。
        let changed = store.connection.execute(
            "UPDATE publication_preparations
             SET state = 'Suppressed'
             WHERE publication_id = 't12-shared-publication'",
            [],
        ).unwrap();
        assert_eq!(changed, 1);

        assert_eq!(
            store.read_version(&id("m1"), &id("v12-original"), &[scope()])
                .unwrap(),
            None,
            "Suppressed versions must remain hidden"
        );

        assert_eq!(
            store.publish_prepared(
                "t12-shared-publication",
                None,
                &[scope()],
            ),
            Err(StorageError::PublicationStateConflict),
            "Suppressed preparations must not be publishable"
        );

        assert!(store.read_current(&id("m1"), &[scope()]).unwrap().is_none());

        let log_count: i64 = store.connection.query_row(
            "SELECT COUNT(*) FROM commit_log WHERE version_id = 'v12-original'",
            [],
            |row| row.get(0),
        ).unwrap();
        assert_eq!(log_count, 0);
    }
}
