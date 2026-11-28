use crate::SqliteEventStore;
use memory_domain::{
    AuthorizationDecisionData, AuthorizationDecisionKind, AuthorizationDecisionRef,
    AuthorizationOperation, AuthorizationSubjectV1, AuthorizationTarget, IssuerId,
    OpaqueId, PrincipalRef, ScopeRef, I_DEV_BASELINE_ISSUER,
};
use memory_event_store::{EventEnvelope, EventStoreError};
use memory_storage::{
    AuthorizationAuthority, AuthorizationReceipt, AuthorizationTransaction,
    StorageError, ValidatedAuthorization,
};
use rusqlite::{params, Connection, OptionalExtension};
use sha2::{Digest, Sha256};

pub const DEV_BASELINE_BRAIN_CLI_PRINCIPAL: &str = "workload:brain-cli";

pub const AUTHORIZATION_SCHEMA: &str = r#"
CREATE TABLE IF NOT EXISTS authorization_policy (
    singleton_id INTEGER PRIMARY KEY CHECK (singleton_id = 1),
    policy_epoch INTEGER NOT NULL CHECK (policy_epoch > 0)
);
INSERT OR IGNORE INTO authorization_policy(singleton_id, policy_epoch)
VALUES (1, 1);

CREATE TABLE IF NOT EXISTS authorization_decisions (
    decision_id       TEXT PRIMARY KEY,
    issuer            TEXT NOT NULL,
    subject_digest    TEXT NOT NULL,
    issued_at         TEXT NOT NULL,
    decision_kind     TEXT NOT NULL CHECK (
        decision_kind IN ('Approved', 'Denied', 'Conditional')
    ),
    principal_ref     TEXT NOT NULL,
    operation         TEXT NOT NULL,
    target_kind       TEXT NOT NULL,
    target_id         TEXT NOT NULL,
    epoch             INTEGER NOT NULL CHECK (epoch > 0)
);

CREATE INDEX IF NOT EXISTS authorization_decisions_subject_idx
    ON authorization_decisions(subject_digest, decision_kind);
"#;

pub(super) fn initialize(connection: &Connection) -> Result<(), EventStoreError> {
    connection
        .execute_batch(AUTHORIZATION_SCHEMA)
        .map_err(|_| EventStoreError::TransactionUnavailable)
}

pub fn configured_principal() -> Result<PrincipalRef, StorageError> {
    let id = OpaqueId::new(DEV_BASELINE_BRAIN_CLI_PRINCIPAL)
        .map_err(|_| StorageError::InvalidSchema)?;
    Ok(PrincipalRef::new(id))
}

fn operation_literal(operation: AuthorizationOperation) -> &'static str {
    match operation {
        AuthorizationOperation::CreateMemory => "CreateMemory",
        AuthorizationOperation::ReadMemory => "ReadMemory",
        AuthorizationOperation::ReadVersion => "ReadVersion",
        AuthorizationOperation::CommitVersion => "CommitVersion",
        AuthorizationOperation::PrepareVersion => "PrepareVersion",
        AuthorizationOperation::PublishPrepared => "PublishPrepared",
        AuthorizationOperation::ReadPublicationState => "ReadPublicationState",
        AuthorizationOperation::ForgetMemory => "ForgetMemory",
        AuthorizationOperation::ForgetVersion => "ForgetVersion",
        AuthorizationOperation::ListChanges => "ListChanges",
        AuthorizationOperation::ResolveIdempotency => "ResolveIdempotency",
        AuthorizationOperation::AppendEvent => "AppendEvent",
        AuthorizationOperation::ReadEvent => "ReadEvent",
        AuthorizationOperation::PublishFact => "PublishFact",
        AuthorizationOperation::AttestFact => "AttestFact",
    }
}

fn decision_kind_literal(kind: AuthorizationDecisionKind) -> &'static str {
    match kind {
        AuthorizationDecisionKind::Approved => "Approved",
        AuthorizationDecisionKind::Denied => "Denied",
        AuthorizationDecisionKind::Conditional => "Conditional",
    }
}

fn parse_decision_kind(value: &str) -> Result<AuthorizationDecisionKind, StorageError> {
    match value {
        "Approved" => Ok(AuthorizationDecisionKind::Approved),
        "Denied" => Ok(AuthorizationDecisionKind::Denied),
        "Conditional" => Ok(AuthorizationDecisionKind::Conditional),
        _ => Err(StorageError::InvalidAuthorizationReceipt),
    }
}

fn subject_digest(subject: &AuthorizationSubjectV1) -> Result<String, StorageError> {
    let bytes = subject
        .as_bytes()
        .map_err(|_| StorageError::InvalidAuthorizationReceipt)?;
    Ok(hex_sha256(&bytes))
}

fn hex_sha256(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    let mut output = String::with_capacity(64);
    for byte in digest {
        use std::fmt::Write;
        let _ = write!(&mut output, "{byte:02x}");
    }
    output
}

fn issued_at_now() -> String {
    let duration = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap_or_default();
    let seconds = duration.as_secs() as i64;
    let days = seconds.div_euclid(86_400);
    let day_seconds = seconds.rem_euclid(86_400);

    let z = days + 719_468;
    let era = if z >= 0 { z } else { z - 146_096 } / 146_097;
    let doe = z - era * 146_097;
    let yoe = (doe - doe / 1_460 + doe / 36_524 - doe / 146_096) / 365;
    let mut year = yoe + era * 400;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = doy - (153 * mp + 2) / 5 + 1;
    let month = mp + if mp < 10 { 3 } else { -9 };
    year += if month <= 2 { 1 } else { 0 };

    format!(
        "{year:04}-{month:02}-{day:02}T{:02}:{:02}:{:02}.{:09}Z",
        day_seconds / 3_600,
        (day_seconds % 3_600) / 60,
        day_seconds % 60,
        duration.subsec_nanos()
    )
}

pub(super) fn current_epoch(connection: &Connection) -> Result<u64, StorageError> {
    let epoch: i64 = connection
        .query_row(
            "SELECT policy_epoch FROM authorization_policy WHERE singleton_id = 1",
            [],
            |row| row.get(0),
        )
        .map_err(|_| StorageError::TransactionUnavailable)?;
    u64::try_from(epoch).map_err(|_| StorageError::InvalidAuthorizationReceipt)
}

fn issue_on_connection(
    connection: &Connection,
    subject: &AuthorizationSubjectV1,
    decision_id: &OpaqueId,
) -> Result<AuthorizationReceipt, StorageError> {
    if subject.principal_ref != configured_principal()? || subject.scopes.is_empty() {
        return Err(StorageError::PermissionDenied);
    }
    if subject.epoch != current_epoch(connection)? {
        return Err(StorageError::PermissionDenied);
    }

    let digest = subject_digest(subject)?;
    let issued_at = issued_at_now();
    let issuer = IssuerId::new(I_DEV_BASELINE_ISSUER)
        .map_err(|_| StorageError::InvalidSchema)?;

    connection
        .execute(
            "INSERT INTO authorization_decisions (
                decision_id, issuer, subject_digest, issued_at, decision_kind,
                principal_ref, operation, target_kind, target_id, epoch
             ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10)",
            params![
                decision_id.as_str(),
                issuer.as_str(),
                digest,
                issued_at,
                decision_kind_literal(AuthorizationDecisionKind::Approved),
                subject.principal_ref.as_str(),
                operation_literal(subject.operation),
                subject.target.target_kind,
                subject.target.target_id,
                i64::try_from(subject.epoch)
                    .map_err(|_| StorageError::InvalidAuthorizationReceipt)?,
            ],
        )
        .map_err(|_| StorageError::InvalidAuthorizationReceipt)?;

    let decision = AuthorizationDecisionRef::from_issued_data(
        AuthorizationDecisionData {
            decision_id: decision_id.clone(),
            issuer,
            subject_digest: OpaqueId::new(subject_digest(subject)?)
                .map_err(|_| StorageError::InvalidSchema)?,
            issued_at,
            decision_kind: AuthorizationDecisionKind::Approved,
        },
    )
    .map_err(|_| StorageError::InvalidAuthorizationReceipt)?;

    Ok(AuthorizationReceipt {
        decision,
        subject: subject.clone(),
    })
}

fn validate_on_connection(
    connection: &Connection,
    receipt: &AuthorizationReceipt,
    expected: &AuthorizationSubjectV1,
) -> Result<(), StorageError> {
    if &receipt.subject != expected {
        return Err(StorageError::InvalidAuthorizationReceipt);
    }
    let data = receipt
        .decision
        .data()
        .ok_or(StorageError::InvalidAuthorizationReceipt)?;

    if data.decision_kind != AuthorizationDecisionKind::Approved {
        return Err(StorageError::PermissionDenied);
    }

    let expected_digest = subject_digest(expected)?;
    if expected.epoch != current_epoch(connection)? {
        return Err(StorageError::PermissionDenied);
    }

    let row = connection
        .query_row(
            "SELECT issuer, subject_digest, issued_at, decision_kind,
                    principal_ref, operation, target_kind, target_id, epoch
             FROM authorization_decisions WHERE decision_id = ?1",
            params![data.decision_id.as_str()],
            |row| {
                Ok((
                    row.get::<_, String>(0)?,
                    row.get::<_, String>(1)?,
                    row.get::<_, String>(2)?,
                    row.get::<_, String>(3)?,
                    row.get::<_, String>(4)?,
                    row.get::<_, String>(5)?,
                    row.get::<_, String>(6)?,
                    row.get::<_, String>(7)?,
                    row.get::<_, i64>(8)?,
                ))
            },
        )
        .optional()
        .map_err(|_| StorageError::TransactionUnavailable)?
        .ok_or(StorageError::InvalidAuthorizationReceipt)?;

    let kind = parse_decision_kind(&row.3)?;
    if row.0 != I_DEV_BASELINE_ISSUER
        || row.1 != expected_digest
        || row.2 != data.issued_at
        || kind != AuthorizationDecisionKind::Approved
        || data.issuer.as_str() != I_DEV_BASELINE_ISSUER
        || data.subject_digest.as_str() != expected_digest
        || row.4 != expected.principal_ref.as_str()
        || row.5 != operation_literal(expected.operation)
        || row.6 != expected.target.target_kind
        || row.7 != expected.target.target_id
        || row.8 < 1
        || row.8 as u64 != expected.epoch
    {
        return Err(StorageError::InvalidAuthorizationReceipt);
    }
    Ok(())
}

/// A versioned, fixed-order, length-prefixed encoding. The producer and
/// source fields are caller declarations: this binds the declaration, but
/// does not authenticate either identity.
fn push_field(output: &mut Vec<u8>, value: &[u8]) {
    output.extend_from_slice(&(value.len() as u64).to_be_bytes());
    output.extend_from_slice(value);
}

fn classification_literal(value: &memory_event_store::EventClassification) -> &'static str {
    use memory_event_store::EventClassification::*;
    match value {
        Observed => "Observed",
        Reported => "Reported",
        Planned => "Planned",
        Predicted => "Predicted",
        Attempted => "Attempted",
        Outcome => "Outcome",
        Administrative => "Administrative",
        Unknown => "Unknown",
    }
}

pub(super) fn envelope_digest(envelope: &EventEnvelope) -> Result<String, EventStoreError> {
    let event_time = serde_json::to_vec(&envelope.event_time)
        .map_err(|_| EventStoreError::InvalidEnvelope)?;
    let mut scopes = envelope
        .scope_refs
        .iter()
        .map(|scope| {
            let mut encoded = Vec::new();
            push_field(&mut encoded, scope.scope_id.as_str().as_bytes());
            push_field(&mut encoded, format!("{:?}", scope.scope_kind).as_bytes());
            push_field(&mut encoded, scope.namespace_key.as_bytes());
            encoded
        })
        .collect::<Vec<_>>();
    scopes.sort();
    scopes.dedup();

    let mut bytes = Vec::new();
    push_field(&mut bytes, b"event-append-v1");
    push_field(&mut bytes, envelope.event_kind.as_bytes());
    push_field(&mut bytes, envelope.source_type.as_bytes());
    push_field(&mut bytes, envelope.source_id.as_str().as_bytes());
    push_field(&mut bytes, envelope.producer_actor_ref.as_str().as_bytes());
    push_field(&mut bytes, &(scopes.len() as u64).to_be_bytes());
    for scope in scopes {
        push_field(&mut bytes, &scope);
    }
    push_field(&mut bytes, &event_time);
    push_field(&mut bytes, envelope.payload_ref.as_bytes());
    push_field(&mut bytes, envelope.payload_digest.as_bytes());
    push_field(&mut bytes, classification_literal(&envelope.classification).as_bytes());
    push_field(&mut bytes, envelope.idempotency_key.as_bytes());
    push_field(&mut bytes, envelope.retention_class.as_bytes());
    push_field(&mut bytes, envelope.correlation_id.as_str().as_bytes());
    Ok(format!("sha256:{}", hex_sha256(&bytes)))
}

pub(super) fn append_target(
    envelope: &EventEnvelope,
) -> Result<AuthorizationTarget, EventStoreError> {
    let digest = envelope_digest(envelope)?;
    AuthorizationTarget::new("event-append-v1", digest)
        .map_err(|_| EventStoreError::InvalidEnvelope)
}

pub(super) fn append_payload_target(
    envelope: &EventEnvelope,
    actual_payload_digest: &str,
) -> Result<AuthorizationTarget, EventStoreError> {
    let envelope_hash = envelope_digest(envelope)?;
    let mut bytes = Vec::new();
    push_field(&mut bytes, b"event-append-payload-v1");
    push_field(&mut bytes, envelope_hash.as_bytes());
    push_field(&mut bytes, actual_payload_digest.as_bytes());
    AuthorizationTarget::new(
        "event-append-payload-v1",
        format!("sha256:{}", hex_sha256(&bytes)),
    )
    .map_err(|_| EventStoreError::InvalidEnvelope)
}

pub(super) fn read_target(
    resource: &str,
) -> Result<AuthorizationTarget, EventStoreError> {
    let mut bytes = Vec::new();
    push_field(&mut bytes, b"event-read-v1");
    push_field(&mut bytes, resource.as_bytes());
    AuthorizationTarget::new(
        "event-read-v1",
        format!("sha256:{}", hex_sha256(&bytes)),
    )
    .map_err(|_| EventStoreError::InvalidEnvelope)
}

pub(super) fn expected_subject(
    cap: &ValidatedAuthorization,
    operation: AuthorizationOperation,
    target: AuthorizationTarget,
) -> Result<AuthorizationSubjectV1, EventStoreError> {
    AuthorizationSubjectV1::new(
        cap.subject().principal_ref.clone(),
        operation,
        cap.subject().scopes.clone(),
        target,
        cap.subject().epoch,
    )
    .map_err(|_| EventStoreError::PermissionDenied)
}

pub(super) fn validate_scopes_exact(
    envelope_scopes: &[ScopeRef],
    authorized_scopes: &[ScopeRef],
) -> Result<(), EventStoreError> {
    fn canonical(scopes: &[ScopeRef]) -> Vec<Vec<u8>> {
        let mut values = scopes
            .iter()
            .map(|scope| {
                let mut bytes = Vec::new();
                push_field(&mut bytes, scope.scope_id.as_str().as_bytes());
                push_field(&mut bytes, format!("{:?}", scope.scope_kind).as_bytes());
                push_field(&mut bytes, scope.namespace_key.as_bytes());
                bytes
            })
            .collect::<Vec<_>>();
        values.sort();
        values.dedup();
        values
    }

    if envelope_scopes.is_empty()
        || authorized_scopes.is_empty()
        || envelope_scopes.iter().any(|scope| scope.validate().is_err())
        || authorized_scopes.iter().any(|scope| scope.validate().is_err())
        || canonical(envelope_scopes) != canonical(authorized_scopes)
    {
        return Err(EventStoreError::PermissionDenied);
    }
    Ok(())
}

pub(super) fn map_authorization_error(_: StorageError) -> EventStoreError {
    EventStoreError::PermissionDenied
}

pub(super) struct SqliteTransactionToken {
    connection_identity: usize,
}

impl SqliteTransactionToken {
    pub(super) fn for_connection(connection: &Connection) -> Self {
        Self {
            connection_identity: connection as *const Connection as usize,
        }
    }

    fn matches(&self, connection: &Connection) -> bool {
        self.connection_identity == connection as *const Connection as usize
    }
}

impl AuthorizationTransaction for SqliteTransactionToken {
    fn as_any(&self) -> &dyn std::any::Any {
        self
    }
}

pub(super) struct TxAuthority<'a> {
    pub(super) connection: &'a Connection,
}

impl AuthorizationAuthority for TxAuthority<'_> {
    fn issue(
        &self,
        subject: &AuthorizationSubjectV1,
        decision_id: &OpaqueId,
    ) -> Result<AuthorizationReceipt, StorageError> {
        issue_on_connection(self.connection, subject, decision_id)
    }

    fn validate(
        &self,
        receipt: &AuthorizationReceipt,
        expected: &AuthorizationSubjectV1,
    ) -> Result<(), StorageError> {
        validate_on_connection(self.connection, receipt, expected)
    }

    fn validate_in_transaction(
        &self,
        transaction: &dyn AuthorizationTransaction,
        receipt: &AuthorizationReceipt,
        expected: &AuthorizationSubjectV1,
    ) -> Result<(), StorageError> {
        let token = transaction
            .as_any()
            .downcast_ref::<SqliteTransactionToken>()
            .ok_or(StorageError::InvalidAuthorizationReceipt)?;
        if !token.matches(self.connection) {
            return Err(StorageError::InvalidAuthorizationReceipt);
        }
        validate_on_connection(self.connection, receipt, expected)
    }
}

impl AuthorizationAuthority for SqliteEventStore {
    fn issue(
        &self,
        subject: &AuthorizationSubjectV1,
        decision_id: &OpaqueId,
    ) -> Result<AuthorizationReceipt, StorageError> {
        issue_on_connection(&self.connection, subject, decision_id)
    }

    fn validate(
        &self,
        receipt: &AuthorizationReceipt,
        expected: &AuthorizationSubjectV1,
    ) -> Result<(), StorageError> {
        validate_on_connection(&self.connection, receipt, expected)
    }

    fn validate_in_transaction(
        &self,
        transaction: &dyn AuthorizationTransaction,
        receipt: &AuthorizationReceipt,
        expected: &AuthorizationSubjectV1,
    ) -> Result<(), StorageError> {
        TxAuthority {
            connection: &self.connection,
        }
        .validate_in_transaction(transaction, receipt, expected)
    }
}

pub(super) fn validate_cap_in_transaction(
    connection: &Connection,
    transaction: &dyn AuthorizationTransaction,
    cap: &ValidatedAuthorization,
    expected: &AuthorizationSubjectV1,
) -> Result<(), EventStoreError> {
    TxAuthority { connection }
        .validate_in_transaction(transaction, cap.receipt(), expected)
        .map_err(map_authorization_error)
}
