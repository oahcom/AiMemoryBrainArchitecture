//! Payload custody extension for the SQLite Event Store.
//! Payload digests use sha256:<lowercase-hex>; the actual bytes are hashed
//! before the transaction is allowed to write any business row.

use crate::authorization;
use crate::SqliteEventStore;
use memory_domain::{scopes_intersect, AuthorizationOperation, OpaqueId, ScopeRef};
use memory_event_store::{
    AcceptedReceipt, EventEnvelope, EventStoreError, ProcessingState,
};
use memory_storage::{AuthorizationTransaction, ValidatedAuthorization};
use rusqlite::{params, OptionalExtension, TransactionBehavior};
use sha2::{Digest, Sha256};

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StoredEvent {
    pub sequence: i64,
    pub envelope: EventEnvelope,
    pub payload_bytes: Vec<u8>,
    pub receipt: AcceptedReceipt,
}

pub trait PayloadEventStoreExt {
    fn accept_with_payload(
        &mut self,
        envelope: EventEnvelope,
        payload_bytes: &[u8],
        cap: &ValidatedAuthorization,
    ) -> Result<AcceptedReceipt, EventStoreError>;

    fn read_after(
        &mut self,
        after_sequence: i64,
        cap: &ValidatedAuthorization,
        limit: usize,
    ) -> Result<Vec<StoredEvent>, EventStoreError>;
}

pub(super) fn digest(payload: &[u8]) -> String {
    let hash = Sha256::digest(payload);
    let mut encoded = String::with_capacity(71);
    encoded.push_str("sha256:");
    for byte in hash {
        use std::fmt::Write;
        let _ = write!(&mut encoded, "{byte:02x}");
    }
    encoded
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
            .any(|item| item.validate().is_err())
    {
        return Err(EventStoreError::InvalidEnvelope);
    }
    Ok(())
}

fn check_scope(scope_json: &str, requested: &[ScopeRef]) -> Result<(), EventStoreError> {
    validate_scope(requested)?;
    let stored: Vec<ScopeRef> = decode(scope_json)?;
    if stored.is_empty() || stored.iter().any(|item| item.validate().is_err()) {
        return Err(EventStoreError::TransactionUnavailable);
    }
    if scopes_intersect(&stored, requested) {
        Ok(())
    } else {
        Err(EventStoreError::ScopeMismatch)
    }
}

fn receipt(
    row_id: i64,
    accepted_at: String,
    payload_digest: String,
    state_json: &str,
) -> Result<AcceptedReceipt, EventStoreError> {
    let processing_state = decode(state_json)?;
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

impl PayloadEventStoreExt for SqliteEventStore {
    fn accept_with_payload(
        &mut self,
        envelope: EventEnvelope,
        payload_bytes: &[u8],
        cap: &ValidatedAuthorization,
    ) -> Result<AcceptedReceipt, EventStoreError> {
        validate_envelope(&envelope)?;

        let actual_digest = digest(payload_bytes);
        if envelope.payload_digest != actual_digest {
            return Err(EventStoreError::PayloadIntegrityMismatch);
        }

        authorization::validate_scopes_exact(
            &envelope.scope_refs,
            &cap.subject().scopes,
        )?;

        let target = authorization::append_payload_target(&envelope, &actual_digest)?;
        let expected = authorization::expected_subject(
            cap,
            AuthorizationOperation::AppendEvent,
            target,
        )?;

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let token = authorization::SqliteTransactionToken::for_connection(&tx);
        authorization::validate_cap_in_transaction(
            &tx,
            &token,
            cap,
            &expected,
        )?;

        // Authorization and epoch revalidation complete before the first
        // accepted_events, event_payloads, or compile_outbox write.
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
            check_scope(&scope_json, &cap.subject().scopes)?;
            if stored_digest != actual_digest {
                return Err(EventStoreError::IdempotencyConflict);
            }

            let stored_bytes = tx
                .query_row(
                    "SELECT payload_bytes FROM event_payloads WHERE event_row = ?1",
                    params![row_id],
                    |row| row.get::<_, Vec<u8>>(0),
                )
                .optional()
                .map_err(|_| EventStoreError::TransactionUnavailable)?;

            match stored_bytes {
                Some(bytes) if bytes != payload_bytes => {
                    return Err(EventStoreError::PayloadIntegrityMismatch);
                }
                Some(_) => {}
                None => {
                    tx.execute(
                        "INSERT INTO event_payloads
                         (event_row, payload_bytes, verified_digest)
                         VALUES (?1, ?2, ?3)",
                        params![row_id, payload_bytes, actual_digest],
                    )
                    .map_err(|_| EventStoreError::TransactionUnavailable)?;
                }
            }

            let original = receipt(row_id, accepted_at, stored_digest, &state_json)?;
            tx.commit()
                .map_err(|_| EventStoreError::TransactionUnavailable)?;
            return Ok(original);
        }

        let accepted_at = SqliteEventStore::now();
        let state_json = encode(&ProcessingState::Pending)?;
        let scope_json = encode(&envelope.scope_refs)?;
        let envelope_json = encode(&envelope)?;

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
            "INSERT INTO event_payloads
             (event_row, payload_bytes, verified_digest)
             VALUES (?1, ?2, ?3)",
            params![row_id, payload_bytes, actual_digest],
        )
        .map_err(|_| EventStoreError::TransactionUnavailable)?;

        tx.execute(
            "INSERT INTO compile_outbox (event_row, intent_kind, created_at)
             VALUES (?1, 'compile', ?2)",
            params![row_id, accepted_at],
        )
        .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let accepted = receipt(row_id, accepted_at, actual_digest, &state_json)?;
        tx.commit()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        Ok(accepted)
    }

    fn read_after(
        &mut self,
        after_sequence: i64,
        cap: &ValidatedAuthorization,
        limit: usize,
    ) -> Result<Vec<StoredEvent>, EventStoreError> {
        validate_scope(&cap.subject().scopes)?;
        if limit == 0 || after_sequence < 0 {
            return Err(EventStoreError::InvalidEnvelope);
        }

        let resource = format!("after:{after_sequence}:limit:{limit}");
        let target = authorization::read_target(&resource)?;
        let expected = authorization::expected_subject(
            cap,
            AuthorizationOperation::ReadEvent,
            target,
        )?;

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let token = authorization::SqliteTransactionToken::for_connection(&tx);
        authorization::validate_cap_in_transaction(
            &tx,
            &token,
            cap,
            &expected,
        )?;

        let mut statement = tx
            .prepare(
                "SELECT e.event_row, e.payload_digest, e.scope_json, e.envelope_json,
                        e.accepted_at, e.processing_state_json,
                        p.payload_bytes, p.verified_digest
                 FROM accepted_events e
                 INNER JOIN event_payloads p ON p.event_row = e.event_row
                 WHERE e.event_row > ?1
                 ORDER BY e.event_row ASC",
            )
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let rows = statement
            .query_map(params![after_sequence], |row| {
                Ok((
                    row.get::<_, i64>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                    row.get::<_, String>(4)?,
                    row.get::<_, String>(5)?,
                    row.get::<_, Vec<u8>>(6)?,
                    row.get::<_, String>(7)?,
                ))
            })
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        let mut events = Vec::new();
        for row in rows {
            let (
                sequence,
                declared_digest,
                scope_json,
                envelope_json,
                accepted_at,
                state_json,
                payload_bytes,
                verified_digest,
            ) = row.map_err(|_| EventStoreError::TransactionUnavailable)?;

            match check_scope(&scope_json, &cap.subject().scopes) {
                Ok(()) => {}
                Err(EventStoreError::ScopeMismatch) => continue,
                Err(error) => return Err(error),
            }

            let envelope: EventEnvelope = decode(&envelope_json)?;
            let actual_digest = digest(&payload_bytes);
            if declared_digest != actual_digest
                || verified_digest != actual_digest
                || envelope.payload_digest != actual_digest
            {
                return Err(EventStoreError::PayloadIntegrityMismatch);
            }

            let accepted = receipt(sequence, accepted_at, declared_digest, &state_json)?;
            events.push(StoredEvent {
                sequence,
                envelope,
                payload_bytes,
                receipt: accepted,
            });

            if events.len() == limit {
                break;
            }
        }

        drop(statement);
        tx.commit()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        Ok(events)
    }
}
