//! SQLite adapter for durable Phase 1 Event acceptance receipts.
//! The payload extension persists raw payload bytes with a SHA-256 digest verified
//! on append and re-verified on ordered reads. Payload custody is implemented by
//! the exported `payload` module; digest-format policy remains a candidate seam.

pub mod payload;
pub use payload::{PayloadEventStoreExt, StoredEvent};

use memory_domain::{scopes_intersect, OpaqueId, ScopeRef};
use memory_event_store::{
    AcceptedReceipt, EventEnvelope, EventStore, EventStoreError, ProcessingState,
};
use rusqlite::{params, Connection, OptionalExtension, TransactionBehavior};
use std::path::Path;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

/// Switch to WAL while tolerating transient contention during concurrent opens.
fn enable_wal(connection: &Connection) -> rusqlite::Result<()> {
    use rusqlite::{Error, ErrorCode};

    let deadline = std::time::Instant::now() + Duration::from_secs(5);
    let mut delay = Duration::from_millis(10);

    loop {
        match connection.execute_batch("PRAGMA journal_mode = WAL;") {
            Ok(()) => return Ok(()),
            Err(Error::SqliteFailure(error, _))
                if matches!(
                    error.code,
                    ErrorCode::DatabaseBusy | ErrorCode::DatabaseLocked
                ) && std::time::Instant::now() < deadline =>
            {
                std::thread::sleep(delay);
                delay = (delay * 2).min(Duration::from_millis(100));
            }
            Err(error) => return Err(error),
        }
    }
}

pub struct SqliteEventStore {
    connection: Connection,
}

/// A pending compile intent read from the durable compile outbox.
///
/// This is a read-only snapshot. Reading does not consume, delete, or mark the
/// intent. Callers may read the same intent again after compilation fails.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PendingCompileIntent {
    pub outbox_row: i64,
    pub event_row: i64,
    pub intent_kind: String,
    pub created_at: String,
}

impl SqliteEventStore {
    pub fn open(path: impl AsRef<Path>) -> Result<Self, EventStoreError> {
        let connection =
            Connection::open(path).map_err(|_| EventStoreError::TransactionUnavailable)?;
        connection
            .busy_timeout(Duration::from_secs(5))
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        enable_wal(&connection).map_err(|_| EventStoreError::TransactionUnavailable)?;
        connection
            .execute_batch(
                "PRAGMA synchronous = FULL;
             PRAGMA foreign_keys = ON;
             PRAGMA busy_timeout = 5000;",
            )
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    pub fn in_memory() -> Result<Self, EventStoreError> {
        let connection =
            Connection::open_in_memory().map_err(|_| EventStoreError::TransactionUnavailable)?;
        connection
            .busy_timeout(Duration::from_secs(5))
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        connection
            .execute_batch(
                "PRAGMA synchronous = FULL;
             PRAGMA foreign_keys = ON;
             PRAGMA busy_timeout = 5000;",
            )
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    fn initialize(&self) -> Result<(), EventStoreError> {
        self.connection.execute_batch(
            "BEGIN IMMEDIATE;
             CREATE TABLE IF NOT EXISTS accepted_events (
                event_row INTEGER PRIMARY KEY AUTOINCREMENT,
                producer_actor_ref TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                payload_digest TEXT NOT NULL,
                scope_json TEXT NOT NULL,
                envelope_json TEXT NOT NULL,
                accepted_at TEXT NOT NULL,
                processing_state_json TEXT NOT NULL,
                UNIQUE(producer_actor_ref, idempotency_key)
            );
            CREATE TABLE IF NOT EXISTS event_payloads (
                event_row INTEGER PRIMARY KEY REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
                payload_bytes BLOB NOT NULL,
                verified_digest TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS compile_outbox (
                outbox_row INTEGER PRIMARY KEY AUTOINCREMENT,
                event_row INTEGER NOT NULL UNIQUE REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
                intent_kind TEXT NOT NULL CHECK (intent_kind = 'compile'),
                created_at TEXT NOT NULL
            );
            INSERT OR IGNORE INTO compile_outbox (event_row, intent_kind, created_at)
                SELECT event_row, 'compile', accepted_at FROM accepted_events;
            COMMIT;"
        ).map_err(|_| EventStoreError::TransactionUnavailable)
    }

    fn encode<T: serde::Serialize>(value: &T) -> Result<String, EventStoreError> {
        serde_json::to_string(value).map_err(|_| EventStoreError::InvalidEnvelope)
    }

    fn decode<T: serde::de::DeserializeOwned>(value: &str) -> Result<T, EventStoreError> {
        serde_json::from_str(value).map_err(|_| EventStoreError::TransactionUnavailable)
    }

    fn validate_scope(scope: &[ScopeRef]) -> Result<(), EventStoreError> {
        if scope.is_empty() || scope.iter().any(|s| s.validate().is_err()) {
            return Err(EventStoreError::ScopeMismatch);
        }
        Ok(())
    }

    fn validate_envelope(
        envelope: &EventEnvelope,
        scope: &[ScopeRef],
    ) -> Result<(), EventStoreError> {
        Self::validate_scope(scope)?;
        if envelope.event_kind.is_empty()
            || envelope.source_type.is_empty()
            || envelope.payload_ref.is_empty()
            || envelope.payload_digest.is_empty()
            || envelope.idempotency_key.is_empty()
            || envelope.retention_class.is_empty()
            || envelope.scope_refs.is_empty()
            || envelope.scope_refs.iter().any(|s| s.validate().is_err())
        {
            return Err(EventStoreError::InvalidEnvelope);
        }
        if !scopes_intersect(&envelope.scope_refs, scope) {
            return Err(EventStoreError::ScopeMismatch);
        }
        Ok(())
    }

    fn scope_allowed(scope_json: &str, requested: &[ScopeRef]) -> Result<(), EventStoreError> {
        Self::validate_scope(requested)?;
        let stored: Vec<ScopeRef> = Self::decode(scope_json)?;
        if scopes_intersect(&stored, requested) {
            Ok(())
        } else {
            Err(EventStoreError::ScopeMismatch)
        }
    }

    fn row_id(event_id: &OpaqueId) -> Result<i64, EventStoreError> {
        event_id
            .as_str()
            .strip_prefix("event:")
            .and_then(|value| value.parse::<i64>().ok())
            .filter(|value| *value > 0)
            .ok_or(EventStoreError::NotFoundOrNotVisible)
    }

    fn receipt(
        row_id: i64,
        accepted_at: String,
        payload_digest: String,
        state_json: &str,
    ) -> Result<AcceptedReceipt, EventStoreError> {
        let processing_state = Self::decode(state_json)?;
        Ok(AcceptedReceipt {
            event_id: OpaqueId::new(format!("event:{row_id}"))
                .map_err(|_| EventStoreError::TransactionUnavailable)?,
            receipt_id: OpaqueId::new(format!("receipt:{row_id}"))
                .map_err(|_| EventStoreError::TransactionUnavailable)?,
            accepted_at,
            payload_digest,
            processing_state,
        })
    }

    fn now() -> String {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_nanos()
            .to_string()
    }

    /// Returns every pending compile intent in deterministic acceptance order.
    ///
    /// This is a read-only snapshot. Reading does not consume, delete, or mark
    /// any intent. Callers may read the same intent again after compilation
    /// fails.
    pub fn pending_compile_intents(&self) -> Result<Vec<PendingCompileIntent>, EventStoreError> {
        let mut statement = self
            .connection
            .prepare(
                "SELECT outbox_row, event_row, intent_kind, created_at
                 FROM compile_outbox
                 ORDER BY created_at ASC, outbox_row ASC",
            )
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let rows = statement
            .query_map([], |row| {
                Ok(PendingCompileIntent {
                    outbox_row: row.get(0)?,
                    event_row: row.get(1)?,
                    intent_kind: row.get(2)?,
                    created_at: row.get(3)?,
                })
            })
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        rows.collect::<rusqlite::Result<Vec<PendingCompileIntent>>>()
            .map_err(|_| EventStoreError::TransactionUnavailable)
    }
}

impl EventStore for SqliteEventStore {
    fn accept(
        &mut self,
        envelope: EventEnvelope,
        scope: &[ScopeRef],
    ) -> Result<AcceptedReceipt, EventStoreError> {
        Self::validate_envelope(&envelope, scope)?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let existing = tx
            .query_row(
                "SELECT event_row, payload_digest, scope_json, accepted_at, processing_state_json
             FROM accepted_events WHERE producer_actor_ref = ?1 AND idempotency_key = ?2",
                params![
                    envelope.producer_actor_ref.as_str(),
                    envelope.idempotency_key
                ],
                |row| {
                    Ok((
                        row.get::<_, i64>(0)?,
                        row.get::<_, String>(1)?,
                        row.get::<_, String>(2)?,
                        row.get::<_, String>(3)?,
                        row.get::<_, String>(4)?,
                    ))
                },
            )
            .optional()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        if let Some((row_id, digest, scope_json, accepted_at, state_json)) = existing {
            Self::scope_allowed(&scope_json, scope)?;
            if digest != envelope.payload_digest {
                return Err(EventStoreError::IdempotencyConflict);
            }
            let receipt = Self::receipt(row_id, accepted_at, digest, &state_json)?;
            tx.commit()
                .map_err(|_| EventStoreError::TransactionUnavailable)?;
            return Ok(receipt);
        }

        let accepted_at = Self::now();
        let state_json = Self::encode(&ProcessingState::Pending)?;
        let scope_json = Self::encode(&envelope.scope_refs)?;
        let envelope_json = Self::encode(&envelope)?;
        tx.execute(
            "INSERT INTO accepted_events
             (producer_actor_ref, idempotency_key, payload_digest, scope_json, envelope_json, accepted_at, processing_state_json)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            params![
                envelope.producer_actor_ref.as_str(),
                envelope.idempotency_key,
                envelope.payload_digest,
                scope_json,
                envelope_json,
                accepted_at,
                state_json
            ],
        ).map_err(|_| EventStoreError::TransactionUnavailable)?;
        let row_id = tx.last_insert_rowid();
        tx.execute(
            "INSERT INTO compile_outbox (event_row, intent_kind, created_at)
             VALUES (?1, 'compile', ?2)",
            params![row_id, accepted_at],
        )
        .map_err(|_| EventStoreError::TransactionUnavailable)?;
        let receipt = Self::receipt(row_id, accepted_at, envelope.payload_digest, &state_json)?;
        tx.commit()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        Ok(receipt)
    }

    fn status(
        &self,
        event_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<Option<AcceptedReceipt>, EventStoreError> {
        Self::validate_scope(scope)?;
        let row_id = Self::row_id(event_id)?;
        let row = self
            .connection
            .query_row(
                "SELECT payload_digest, scope_json, accepted_at, processing_state_json
             FROM accepted_events WHERE event_row = ?1",
                params![row_id],
                |row| {
                    Ok((
                        row.get::<_, String>(0)?,
                        row.get::<_, String>(1)?,
                        row.get::<_, String>(2)?,
                        row.get::<_, String>(3)?,
                    ))
                },
            )
            .optional()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        match row {
            None => Ok(None),
            Some((digest, scope_json, accepted_at, state_json)) => {
                Self::scope_allowed(&scope_json, scope)?;
                Ok(Some(Self::receipt(
                    row_id,
                    accepted_at,
                    digest,
                    &state_json,
                )?))
            }
        }
    }

    // Receipt replay is deliberately not queue execution: it returns the original
    // acceptance identity/time/state. No worker or processing queue is implemented here.
    fn replay(
        &mut self,
        event_id: &OpaqueId,
        scope: &[ScopeRef],
    ) -> Result<AcceptedReceipt, EventStoreError> {
        self.status(event_id, scope)?
            .ok_or(EventStoreError::NotFoundOrNotVisible)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::ScopeKind;
    use memory_event_store::EventClassification;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }
    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("scope-1"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-1".into(),
        }
    }
    fn envelope(key: &str, digest: &str) -> EventEnvelope {
        EventEnvelope {
            event_kind: "observation".into(),
            source_type: "test".into(),
            source_id: id("source-1"),
            producer_actor_ref: id("actor-1"),
            scope_refs: vec![scope()],
            event_time: None,
            payload_ref: "payload://source-1".into(),
            payload_digest: digest.into(),
            classification: EventClassification::Observed,
            idempotency_key: key.into(),
            retention_class: "default".into(),
            correlation_id: id("correlation-1"),
        }
    }

    fn path() -> std::path::PathBuf {
        let nonce = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        std::env::temp_dir().join(format!("event-store-{}-{nonce}.sqlite", std::process::id()))
    }
    fn cleanup(path: &Path) {
        let _ = std::fs::remove_file(path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }

    #[test]
    fn pending_compile_intents_is_empty_on_a_fresh_store() {
        let store = SqliteEventStore::in_memory().unwrap();

        assert!(store.pending_compile_intents().unwrap().is_empty());
    }

    #[test]
    fn pending_compile_intents_returns_accepted_events_in_insertion_order() {
        let mut store = SqliteEventStore::in_memory().unwrap();

        let first = store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();
        let second = store
            .accept(envelope("op-2", "digest-2"), &[scope()])
            .unwrap();

        let intents = store.pending_compile_intents().unwrap();
        assert_eq!(intents.len(), 2);

        let first_row = SqliteEventStore::row_id(&first.event_id).unwrap();
        let second_row = SqliteEventStore::row_id(&second.event_id).unwrap();
        assert_eq!(intents[0].event_row, first_row);
        assert_eq!(intents[1].event_row, second_row);
        assert_eq!(intents[0].intent_kind, "compile");
        assert_eq!(intents[1].intent_kind, "compile");
        assert!(intents[0].outbox_row < intents[1].outbox_row);
    }

    #[test]
    fn pending_compile_intents_is_idempotent_and_does_not_consume() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();
        store
            .accept(envelope("op-2", "digest-2"), &[scope()])
            .unwrap();

        let first_read = store.pending_compile_intents().unwrap();
        let count_before: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM compile_outbox", [], |row| row.get(0))
            .unwrap();
        let second_read = store.pending_compile_intents().unwrap();
        let count_after: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM compile_outbox", [], |row| row.get(0))
            .unwrap();

        assert_eq!(first_read, second_read);
        assert_eq!(count_before, count_after);
        assert_eq!(count_after, 2);
    }

    #[test]
    fn pending_compile_intent_created_at_matches_the_acceptance_time() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let receipt = store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();

        let intents = store.pending_compile_intents().unwrap();
        assert_eq!(intents.len(), 1);
        assert_eq!(intents[0].created_at, receipt.accepted_at);
    }

    #[test]
    fn acceptance_persists_across_reopen_and_receipt_replay_is_stable() {
        let path = path();
        let first = {
            let mut store = SqliteEventStore::open(&path).unwrap();
            store
                .accept(envelope("op-1", "digest-1"), &[scope()])
                .unwrap()
        };
        let mut reopened = SqliteEventStore::open(&path).unwrap();
        assert_eq!(
            reopened.status(&first.event_id, &[scope()]).unwrap(),
            Some(first.clone())
        );
        assert_eq!(reopened.replay(&first.event_id, &[scope()]).unwrap(), first);
        let outbox_count: i64 = reopened
            .connection
            .query_row("SELECT COUNT(*) FROM compile_outbox", [], |row| row.get(0))
            .unwrap();
        assert_eq!(outbox_count, 1);
        cleanup(&path);
    }

    #[test]
    fn startup_backfills_compile_intent_for_preexisting_accepted_events() {
        let path = path();
        {
            let legacy = Connection::open(&path).unwrap();
            legacy
                .execute_batch(
                    "CREATE TABLE accepted_events (
                    event_row INTEGER PRIMARY KEY AUTOINCREMENT,
                    producer_actor_ref TEXT NOT NULL,
                    idempotency_key TEXT NOT NULL,
                    payload_digest TEXT NOT NULL,
                    scope_json TEXT NOT NULL,
                    envelope_json TEXT NOT NULL,
                    accepted_at TEXT NOT NULL,
                    processing_state_json TEXT NOT NULL,
                    UNIQUE(producer_actor_ref, idempotency_key)
                );
                INSERT INTO accepted_events
                    (event_row, producer_actor_ref, idempotency_key, payload_digest,
                     scope_json, envelope_json, accepted_at, processing_state_json)
                VALUES (1, 'actor-legacy', 'legacy-op', 'legacy-digest',
                        '[]', '{}', '12345', '\"Pending\"');",
                )
                .unwrap();
        }

        let store = SqliteEventStore::open(&path).unwrap();
        let outbox_count: i64 = store
            .connection
            .query_row(
                "SELECT COUNT(*) FROM compile_outbox WHERE event_row = 1",
                [],
                |row| row.get(0),
            )
            .unwrap();
        assert_eq!(outbox_count, 1);
        cleanup(&path);
    }

    #[test]
    fn same_producer_key_and_digest_replay_original_receipt() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let first = store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();
        let retry = store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();
        assert_eq!(retry, first);
        assert_eq!(retry.processing_state, ProcessingState::Pending);
        let outbox_count: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM compile_outbox", [], |row| row.get(0))
            .unwrap();
        assert_eq!(outbox_count, 1);
    }

    #[test]
    fn same_producer_key_with_different_digest_conflicts() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();
        assert_eq!(
            store.accept(envelope("op-1", "different-digest"), &[scope()]),
            Err(EventStoreError::IdempotencyConflict)
        );
    }

    #[test]
    fn status_and_replay_enforce_scope() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let receipt = store
            .accept(envelope("op-1", "digest-1"), &[scope()])
            .unwrap();
        let other = ScopeRef {
            scope_id: id("scope-2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-2".into(),
        };
        assert_eq!(
            store.status(&receipt.event_id, std::slice::from_ref(&other)),
            Err(EventStoreError::ScopeMismatch)
        );
        assert_eq!(
            store.replay(&receipt.event_id, &[other]),
            Err(EventStoreError::ScopeMismatch)
        );
    }

    #[test]
    fn empty_scope_and_missing_payload_identity_are_rejected() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        assert_eq!(
            store.accept(envelope("op-1", "digest-1"), &[]),
            Err(EventStoreError::ScopeMismatch)
        );
        let mut invalid = envelope("op-1", "digest-1");
        invalid.payload_digest.clear();
        assert_eq!(
            store.accept(invalid, &[scope()]),
            Err(EventStoreError::InvalidEnvelope)
        );
    }
}

/// Durable ForgetFence restore gate.
pub mod forget_fence;
