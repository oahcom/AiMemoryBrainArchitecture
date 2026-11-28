//! SQLite adapter for durable Phase 1 Event acceptance receipts.
//! Authorization decisions and policy epochs are revalidated on the exact
//! SQLite transaction connection before any Event, payload, or outbox write.

mod authorization;
pub mod payload;
pub use payload::{PayloadEventStoreExt, StoredEvent};

use authorization::{
    append_target, current_epoch, expected_subject, read_target,
    validate_cap_in_transaction, validate_scopes_exact,
};
use memory_domain::{
    AuthorizationOperation, AuthorizationSubjectV1, AuthorizationTarget, OpaqueId, ScopeRef,
};
use memory_event_store::{
    AcceptedReceipt, EventEnvelope, EventStore, EventStoreError, ProcessingState,
};
use memory_storage::{
    AuthorizationAuthority, StorageError, ValidatedAuthorization,
};
use rusqlite::{params, Connection, OptionalExtension, TransactionBehavior};
use std::path::Path;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

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

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PendingCompileIntent {
    outbox_row: i64,
    event_row: i64,
    intent_kind: String,
    created_at: String,
    receipt: AcceptedReceipt,
    envelope: EventEnvelope,
    payload_bytes: Vec<u8>,
}

impl PendingCompileIntent {
    pub fn outbox_row(&self) -> i64 {
        self.outbox_row
    }

    pub fn event_row(&self) -> i64 {
        self.event_row
    }

    pub fn intent_kind(&self) -> &str {
        &self.intent_kind
    }

    pub fn created_at(&self) -> &str {
        &self.created_at
    }

    pub fn receipt(&self) -> &AcceptedReceipt {
        &self.receipt
    }

    pub fn envelope(&self) -> &EventEnvelope {
        &self.envelope
    }

    pub fn payload_bytes(&self) -> Vec<u8> {
        self.payload_bytes.clone()
    }
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
        self.connection
            .execute_batch(
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
                    event_row INTEGER PRIMARY KEY
                        REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
                    payload_bytes BLOB NOT NULL,
                    verified_digest TEXT NOT NULL
                 );
                 CREATE TABLE IF NOT EXISTS compile_outbox (
                    outbox_row INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_row INTEGER NOT NULL UNIQUE
                        REFERENCES accepted_events(event_row) ON DELETE RESTRICT,
                    intent_kind TEXT NOT NULL CHECK (intent_kind = 'compile'),
                    created_at TEXT NOT NULL
                 );
                 INSERT OR IGNORE INTO compile_outbox
                    (event_row, intent_kind, created_at)
                    SELECT event_row, 'compile', accepted_at FROM accepted_events;",
            )
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        if let Err(error) = authorization::initialize(&self.connection) {
            let _ = self.connection.execute_batch("ROLLBACK;");
            return Err(error);
        }

        self.connection
            .execute_batch("COMMIT;")
            .map_err(|_| {
                let _ = self.connection.execute_batch("ROLLBACK;");
                EventStoreError::TransactionUnavailable
            })
    }

    fn encode<T: serde::Serialize>(value: &T) -> Result<String, EventStoreError> {
        serde_json::to_string(value).map_err(|_| EventStoreError::InvalidEnvelope)
    }

    fn decode<T: serde::de::DeserializeOwned>(value: &str) -> Result<T, EventStoreError> {
        serde_json::from_str(value).map_err(|_| EventStoreError::TransactionUnavailable)
    }

    fn validate_scope(scope: &[ScopeRef]) -> Result<(), EventStoreError> {
        if scope.is_empty() || scope.iter().any(|item| item.validate().is_err()) {
            return Err(EventStoreError::ScopeMismatch);
        }
        Ok(())
    }

    fn validate_envelope(envelope: &EventEnvelope) -> Result<(), EventStoreError> {
        if envelope.event_kind.is_empty()
            || envelope.source_type.is_empty()
            || envelope.payload_ref.is_empty()
            || envelope.payload_digest.is_empty()
            || envelope.idempotency_key.is_empty()
            || envelope.retention_class.is_empty()
            || envelope.scope_refs.is_empty()
            || envelope
                .scope_refs
                .iter()
                .any(|scope| scope.validate().is_err())
        {
            return Err(EventStoreError::InvalidEnvelope);
        }
        Ok(())
    }

    fn scope_allowed(scope_json: &str, requested: &[ScopeRef]) -> Result<(), EventStoreError> {
        Self::validate_scope(requested)?;
        let stored: Vec<ScopeRef> = Self::decode(scope_json)?;
        if stored.is_empty() || stored.iter().any(|scope| scope.validate().is_err()) {
            return Err(EventStoreError::TransactionUnavailable);
        }
        if memory_domain::scopes_intersect(&stored, requested) {
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

    /// Build the exact subject required by `accept`. The configured principal
    /// is a dev-baseline configuration label, not an authenticated identity.
    pub fn append_authorization_subject(
        &self,
        envelope: &EventEnvelope,
    ) -> Result<AuthorizationSubjectV1, EventStoreError> {
        Self::validate_envelope(envelope)?;
        let target = append_target(envelope)?;
        self.subject(
            AuthorizationOperation::AppendEvent,
            envelope.scope_refs.clone(),
            target,
        )
    }

    /// Build the exact subject required by `accept_with_payload`.
    pub fn append_payload_authorization_subject(
        &self,
        envelope: &EventEnvelope,
        payload_bytes: &[u8],
    ) -> Result<AuthorizationSubjectV1, EventStoreError> {
        Self::validate_envelope(envelope)?;
        let actual_digest = payload::digest(payload_bytes);
        if envelope.payload_digest != actual_digest {
            return Err(EventStoreError::PayloadIntegrityMismatch);
        }
        let target =
            authorization::append_payload_target(envelope, &actual_digest)?;
        self.subject(
            AuthorizationOperation::AppendEvent,
            envelope.scope_refs.clone(),
            target,
        )
    }

    /// Build the exact subject required by `status` and `replay`.
    pub fn read_event_authorization_subject(
        &self,
        event_id: &OpaqueId,
        scopes: Vec<ScopeRef>,
    ) -> Result<AuthorizationSubjectV1, EventStoreError> {
        let target = read_target(event_id.as_str())?;
        self.subject(AuthorizationOperation::ReadEvent, scopes, target)
    }

    /// Build the exact subject required by `read_after`.
    pub fn read_after_authorization_subject(
        &self,
        after_sequence: i64,
        limit: usize,
        scopes: Vec<ScopeRef>,
    ) -> Result<AuthorizationSubjectV1, EventStoreError> {
        if after_sequence < 0 || limit == 0 {
            return Err(EventStoreError::InvalidEnvelope);
        }
        let target = read_target(&format!("after:{after_sequence}:limit:{limit}"))?;
        self.subject(AuthorizationOperation::ReadEvent, scopes, target)
    }

    fn subject(
        &self,
        operation: AuthorizationOperation,
        scopes: Vec<ScopeRef>,
        target: AuthorizationTarget,
    ) -> Result<AuthorizationSubjectV1, EventStoreError> {
        let principal = authorization::configured_principal()
            .map_err(|_| EventStoreError::PermissionDenied)?;
        let epoch = current_epoch(&self.connection)
            .map_err(|_| EventStoreError::PermissionDenied)?;
        AuthorizationSubjectV1::new(principal, operation, scopes, target, epoch)
            .map_err(|_| EventStoreError::PermissionDenied)
    }

    /// Read-only snapshot of pending compile intents.
    ///
    /// This legacy worker-facing path is deliberately not used as an
    /// authorization substitute for EventStore read operations.
    pub fn pending_compile_intents(
        &self,
    ) -> Result<Vec<PendingCompileIntent>, EventStoreError> {
        let mut statement = self
            .connection
            .prepare(
                "SELECT o.outbox_row, o.event_row, o.intent_kind, o.created_at,
                        e.payload_digest, e.envelope_json, e.processing_state_json,
                        p.payload_bytes, p.verified_digest
                 FROM compile_outbox o
                 INNER JOIN accepted_events e ON e.event_row = o.event_row
                 INNER JOIN event_payloads p ON p.event_row = o.event_row
                 ORDER BY o.created_at ASC, o.outbox_row ASC",
            )
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let rows = statement
            .query_map([], |row| {
                Ok((
                    row.get::<_, i64>(0)?,
                    row.get::<_, i64>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                    row.get::<_, String>(4)?,
                    row.get::<_, String>(5)?,
                    row.get::<_, String>(6)?,
                    row.get::<_, Vec<u8>>(7)?,
                    row.get::<_, String>(8)?,
                ))
            })
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let mut intents = Vec::new();
        for row in rows {
            let (
                outbox_row,
                event_row,
                intent_kind,
                created_at,
                declared_digest,
                envelope_json,
                state_json,
                payload_bytes,
                verified_digest,
            ) = row.map_err(|_| EventStoreError::TransactionUnavailable)?;

            let envelope: EventEnvelope = Self::decode(&envelope_json)?;
            let actual_digest = payload::digest(&payload_bytes);
            if declared_digest != actual_digest
                || verified_digest != actual_digest
                || envelope.payload_digest != actual_digest
            {
                return Err(EventStoreError::PayloadIntegrityMismatch);
            }

            let receipt =
                Self::receipt(event_row, created_at.clone(), declared_digest, &state_json)?;
            intents.push(PendingCompileIntent {
                outbox_row,
                event_row,
                intent_kind,
                created_at,
                receipt,
                envelope,
                payload_bytes,
            });
        }
        Ok(intents)
    }
}

impl EventStore for SqliteEventStore {
    fn accept(
        &mut self,
        envelope: EventEnvelope,
        cap: &ValidatedAuthorization,
    ) -> Result<AcceptedReceipt, EventStoreError> {
        Self::validate_envelope(&envelope)?;
        validate_scopes_exact(&envelope.scope_refs, &cap.subject().scopes)?;

        let target = append_target(&envelope)?;
        let expected = expected_subject(
            cap,
            AuthorizationOperation::AppendEvent,
            target,
        )?;

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let token = authorization::SqliteTransactionToken::for_connection(&tx);
        validate_cap_in_transaction(&tx, &token, cap, &expected)?;

        // No accepted_events, event_payloads, or compile_outbox write occurs
        // before transaction-bound authorization and epoch validation.
        let existing = tx
            .query_row(
                "SELECT event_row, payload_digest, scope_json, accepted_at,
                        processing_state_json
                 FROM accepted_events
                 WHERE producer_actor_ref = ?1 AND idempotency_key = ?2",
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

        if let Some((row_id, stored_digest, scope_json, accepted_at, state_json)) = existing {
            Self::scope_allowed(&scope_json, &cap.subject().scopes)?;
            if stored_digest != envelope.payload_digest {
                return Err(EventStoreError::IdempotencyConflict);
            }
            let accepted = Self::receipt(row_id, accepted_at, stored_digest, &state_json)?;
            tx.commit()
                .map_err(|_| EventStoreError::TransactionUnavailable)?;
            return Ok(accepted);
        }

        let accepted_at = Self::now();
        let state_json = Self::encode(&ProcessingState::Pending)?;
        let scope_json = Self::encode(&envelope.scope_refs)?;
        let envelope_json = Self::encode(&envelope)?;

        tx.execute(
            "INSERT INTO accepted_events
             (producer_actor_ref, idempotency_key, payload_digest, scope_json,
              envelope_json, accepted_at, processing_state_json)
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
        )
        .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let row_id = tx.last_insert_rowid();
        tx.execute(
            "INSERT INTO compile_outbox (event_row, intent_kind, created_at)
             VALUES (?1, 'compile', ?2)",
            params![row_id, accepted_at],
        )
        .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let accepted =
            Self::receipt(row_id, accepted_at, envelope.payload_digest, &state_json)?;
        tx.commit()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        Ok(accepted)
    }

    fn status(
        &mut self,
        event_id: &OpaqueId,
        cap: &ValidatedAuthorization,
    ) -> Result<Option<AcceptedReceipt>, EventStoreError> {
        Self::validate_scope(&cap.subject().scopes)?;
        let row_id = Self::row_id(event_id)?;
        let target = read_target(event_id.as_str())?;
        let expected = expected_subject(
            cap,
            AuthorizationOperation::ReadEvent,
            target,
        )?;

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let token = authorization::SqliteTransactionToken::for_connection(&tx);
        validate_cap_in_transaction(&tx, &token, cap, &expected)?;

        let row = tx
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

        let result = match row {
            None => None,
            Some((digest, scope_json, accepted_at, state_json)) => {
                Self::scope_allowed(&scope_json, &cap.subject().scopes)?;
                Some(Self::receipt(row_id, accepted_at, digest, &state_json)?)
            }
        };

        tx.commit()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        Ok(result)
    }

    fn replay(
        &mut self,
        event_id: &OpaqueId,
        cap: &ValidatedAuthorization,
    ) -> Result<AcceptedReceipt, EventStoreError> {
        self.status(event_id, cap)?
            .ok_or(EventStoreError::NotFoundOrNotVisible)
    }
}
