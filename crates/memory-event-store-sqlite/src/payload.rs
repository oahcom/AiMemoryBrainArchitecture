//! Payload custody extension for the SQLite Event Store.
//! Digest format selected for this CANDIDATE adapter seam: sha256:<lowercase-hex>.
//! Algorithm/version and canonical payload boundary remain TO_VALIDATE against the
//! Event Store payload-integrity contract. This is not an Owner decision.
//!
//! Idempotency lookup retains the pre-existing (producer_actor_ref, idempotency_key)
//! key pending RFC-IDE-001 / identity-owner closure. TO_VALIDATE:
//! exact ProducerIdentity + Scope + IdempotencyKey namespace.

use crate::SqliteEventStore;
use memory_domain::{scopes_intersect, OpaqueId, ScopeRef};
use memory_event_store::{AcceptedReceipt, EventEnvelope, EventStoreError, ProcessingState};
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
        scope: &[ScopeRef],
    ) -> Result<AcceptedReceipt, EventStoreError>;
    fn read_after(
        &self,
        after_sequence: i64,
        limit: usize,
        scope: &[ScopeRef],
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
fn validate_envelope(envelope: &EventEnvelope, scope: &[ScopeRef]) -> Result<(), EventStoreError> {
    validate_scope(scope)?;
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
    if !scopes_intersect(&envelope.scope_refs, scope) {
        return Err(EventStoreError::ScopeMismatch);
    }
    Ok(())
}
fn check_scope(scope_json: &str, requested: &[ScopeRef]) -> Result<(), EventStoreError> {
    validate_scope(requested)?;
    let stored: Vec<ScopeRef> = decode(scope_json)?;
    // Persisted metadata is untrusted input. Corruption must not collapse
    // into ScopeMismatch because read_after intentionally skips that variant.
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
        scope: &[ScopeRef],
    ) -> Result<AcceptedReceipt, EventStoreError> {
        validate_envelope(&envelope, scope)?;
        let actual_digest = digest(payload_bytes);
        if envelope.payload_digest != actual_digest {
            return Err(EventStoreError::PayloadIntegrityMismatch);
        }
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(|_| EventStoreError::TransactionUnavailable)?;

        // TO_VALIDATE: preserve the existing namespace until the identity Owner freezes
        // ProducerIdentity + Scope + IdempotencyKey and canonical equality.
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

        if let Some((row_id, stored_digest, scope_json, accepted_at, state_json)) = existing {
            check_scope(&scope_json, scope)?;
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
                    return Err(EventStoreError::PayloadIntegrityMismatch)
                }
                Some(_) => {}
                None => {
                    tx.execute(
                        "INSERT INTO event_payloads (event_row, payload_bytes, verified_digest) VALUES (?1, ?2, ?3)",
                        params![row_id, payload_bytes, actual_digest],
                    ).map_err(|_| EventStoreError::TransactionUnavailable)?;
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
             (producer_actor_ref, idempotency_key, payload_digest, scope_json, envelope_json, accepted_at, processing_state_json)
             VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7)",
            params![envelope.producer_actor_ref.as_str(), envelope.idempotency_key, envelope.payload_digest,
                    scope_json, envelope_json, accepted_at, state_json],
        ).map_err(|_| EventStoreError::TransactionUnavailable)?;
        let row_id = tx.last_insert_rowid();
        tx.execute(
            "INSERT INTO event_payloads (event_row, payload_bytes, verified_digest) VALUES (?1, ?2, ?3)",
            params![row_id, payload_bytes, actual_digest],
        ).map_err(|_| EventStoreError::TransactionUnavailable)?;
        tx.execute(
            "INSERT INTO compile_outbox (event_row, intent_kind, created_at) VALUES (?1, 'compile', ?2)",
            params![row_id, accepted_at],
        ).map_err(|_| EventStoreError::TransactionUnavailable)?;
        let accepted = receipt(row_id, accepted_at, actual_digest, &state_json)?;
        tx.commit()
            .map_err(|_| EventStoreError::TransactionUnavailable)?;
        Ok(accepted)
    }

    fn read_after(
        &self,
        after_sequence: i64,
        limit: usize,
        scope: &[ScopeRef],
    ) -> Result<Vec<StoredEvent>, EventStoreError> {
        validate_scope(scope)?;
        if limit == 0 {
            return Err(EventStoreError::InvalidEnvelope);
        }
        let mut statement = self
            .connection
            .prepare(
                "SELECT e.event_row, e.payload_digest, e.scope_json, e.envelope_json,
                    e.accepted_at, e.processing_state_json, p.payload_bytes, p.verified_digest
             FROM accepted_events e INNER JOIN event_payloads p ON p.event_row = e.event_row
             WHERE e.event_row > ?1 ORDER BY e.event_row ASC",
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
            match check_scope(&scope_json, scope) {
                Ok(()) => {}
                // A valid but non-intersecting Scope is invisible, not a page error.
                // Decode/validation failures remain fail-closed.
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
            // limit counts visible events; the last returned sequence is the next cursor.
            if events.len() == limit {
                break;
            }
        }
        Ok(events)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::ScopeKind;
    use memory_event_store::EventClassification;
    use std::time::{SystemTime, UNIX_EPOCH};

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
    fn envelope(key: &str, payload: &[u8]) -> EventEnvelope {
        EventEnvelope {
            event_kind: "observation".into(),
            source_type: "test".into(),
            source_id: id("source-1"),
            producer_actor_ref: id("actor-1"),
            scope_refs: vec![scope()],
            event_time: None,
            payload_ref: "payload://source-1".into(),
            payload_digest: digest(payload),
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
        std::env::temp_dir().join(format!(
            "event-payload-{}-{nonce}.sqlite",
            std::process::id()
        ))
    }
    fn cleanup(path: &std::path::Path) {
        let _ = std::fs::remove_file(path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }

    #[test]
    fn payload_append_receipt_and_ordered_read_survive_reopen() {
        let path = path();
        let (first, second) = {
            let mut store = SqliteEventStore::open(&path).unwrap();
            let first = store
                .accept_with_payload(envelope("k1", b"first"), b"first", &[scope()])
                .unwrap();
            let second = store
                .accept_with_payload(envelope("k2", b"second"), b"second", &[scope()])
                .unwrap();
            (first, second)
        };
        let store = SqliteEventStore::open(&path).unwrap();
        let rows = store.read_after(0, 10, &[scope()]).unwrap();
        assert_eq!(rows.len(), 2);
        assert!(rows[0].sequence < rows[1].sequence);
        assert_eq!(rows[0].payload_bytes, b"first");
        assert_eq!(rows[1].payload_bytes, b"second");
        assert_eq!(rows[0].receipt, first);
        assert_eq!(rows[1].receipt, second);
        cleanup(&path);
    }

    #[test]
    fn payload_digest_mismatch_is_rejected_before_append() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let mut event = envelope("k1", b"actual");
        event.payload_digest = digest(b"declared-other");
        assert_eq!(
            store.accept_with_payload(event, b"actual", &[scope()]),
            Err(EventStoreError::PayloadIntegrityMismatch)
        );
        let count: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM accepted_events", [], |r| r.get(0))
            .unwrap();
        assert_eq!(count, 0);
    }

    #[test]
    fn read_after_skips_non_intersecting_scopes_and_limits_visible_rows() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let scope_a = scope();
        let scope_b = ScopeRef {
            scope_id: id("scope-2"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-2".into(),
        };
        let mut a = envelope("scope-a-1", b"a1");
        a.scope_refs = vec![scope_a.clone()];
        let mut b1 = envelope("scope-b-1", b"b1");
        b1.scope_refs = vec![scope_b.clone()];
        let mut b2 = envelope("scope-b-2", b"b2");
        b2.scope_refs = vec![scope_b.clone()];

        store.accept_with_payload(a, b"a1", &[scope_a]).unwrap();
        let hidden_only = store
            .read_after(0, 1, std::slice::from_ref(&scope_b))
            .unwrap();
        assert!(hidden_only.is_empty());

        let visible1 = store
            .accept_with_payload(b1, b"b1", std::slice::from_ref(&scope_b))
            .unwrap();
        let visible2 = store
            .accept_with_payload(b2, b"b2", std::slice::from_ref(&scope_b))
            .unwrap();
        let page1 = store
            .read_after(0, 1, std::slice::from_ref(&scope_b))
            .unwrap();
        assert_eq!(page1.len(), 1);
        assert_eq!(page1[0].receipt, visible1);
        let page2 = store.read_after(page1[0].sequence, 1, &[scope_b]).unwrap();
        assert_eq!(page2.len(), 1);
        assert_eq!(page2[0].receipt, visible2);
    }

    #[test]
    fn read_after_fails_closed_on_empty_persisted_scope_list() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        store
            .accept_with_payload(
                envelope("corrupt-empty", b"payload"),
                b"payload",
                &[scope()],
            )
            .unwrap();
        store
            .connection
            .execute("UPDATE accepted_events SET scope_json = '[]'", [])
            .unwrap();

        assert_eq!(
            store.read_after(0, 10, &[scope()]),
            Err(EventStoreError::TransactionUnavailable),
        );
    }

    #[test]
    fn read_after_fails_closed_on_invalid_persisted_scope_ref() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        store
            .accept_with_payload(
                envelope("corrupt-invalid", b"payload"),
                b"payload",
                &[scope()],
            )
            .unwrap();
        let mut invalid = scope();
        invalid.namespace_key.clear();
        let encoded = encode(&vec![invalid]).unwrap();
        store
            .connection
            .execute(
                "UPDATE accepted_events SET scope_json = ?1",
                params![encoded],
            )
            .unwrap();

        assert_eq!(
            store.read_after(0, 10, &[scope()]),
            Err(EventStoreError::TransactionUnavailable),
        );
    }

    #[test]
    fn read_after_paginates_interleaved_scope_rows_by_visible_limit() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let scope_a = scope();
        let scope_b = ScopeRef {
            scope_id: id("scope-b"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-b".into(),
        };
        let rows = [
            ("a1", b"a1".as_slice(), scope_a.clone()),
            ("b1", b"b1".as_slice(), scope_b.clone()),
            ("a2", b"a2".as_slice(), scope_a.clone()),
            ("b2", b"b2".as_slice(), scope_b.clone()),
        ];
        let mut expected = Vec::new();
        for (key, bytes, event_scope) in rows {
            let mut event = envelope(key, bytes);
            event.scope_refs = vec![event_scope.clone()];
            let receipt = store
                .accept_with_payload(event, bytes, &[event_scope])
                .unwrap();
            expected.push(receipt);
        }

        let first_a = store
            .read_after(0, 1, std::slice::from_ref(&scope_a))
            .unwrap();
        assert_eq!(first_a.len(), 1);
        assert_eq!(first_a[0].receipt, expected[0]);
        let second_a = store
            .read_after(first_a[0].sequence, 1, std::slice::from_ref(&scope_a))
            .unwrap();
        assert_eq!(second_a.len(), 1);
        assert_eq!(second_a[0].receipt, expected[2]);
        assert!(store
            .read_after(second_a[0].sequence, 1, &[scope_a])
            .unwrap()
            .is_empty());

        let first_b = store
            .read_after(0, 1, std::slice::from_ref(&scope_b))
            .unwrap();
        assert_eq!(first_b.len(), 1);
        assert_eq!(first_b[0].receipt, expected[1]);
        let second_b = store
            .read_after(first_b[0].sequence, 1, std::slice::from_ref(&scope_b))
            .unwrap();
        assert_eq!(second_b.len(), 1);
        assert_eq!(second_b[0].receipt, expected[3]);
        assert!(store
            .read_after(second_b[0].sequence, 1, &[scope_b])
            .unwrap()
            .is_empty());
    }

    #[test]
    fn duplicate_payload_append_returns_original_receipt_without_duplicate_rows() {
        let mut store = SqliteEventStore::in_memory().unwrap();
        let first = store
            .accept_with_payload(envelope("k1", b"same"), b"same", &[scope()])
            .unwrap();
        let retry = store
            .accept_with_payload(envelope("k1", b"same"), b"same", &[scope()])
            .unwrap();
        assert_eq!(retry, first);
        let count: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM accepted_events", [], |r| r.get(0))
            .unwrap();
        let payload_count: i64 = store
            .connection
            .query_row("SELECT COUNT(*) FROM event_payloads", [], |r| r.get(0))
            .unwrap();
        assert_eq!((count, payload_count), (1, 1));
    }
}
