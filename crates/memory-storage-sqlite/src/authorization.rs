use crate::SqliteMemoryStorage;
use memory_domain::{
    AuthorizationDecisionData, AuthorizationDecisionKind, AuthorizationDecisionRef,
    AuthorizationOperation, AuthorizationSubjectV1, IssuerId, OpaqueId,
    PrincipalRef, I_DEV_BASELINE_ISSUER,
};
use memory_storage::{
    AuthorizationAuthority, AuthorizationReceipt, AuthorizationTransaction,
    StorageError,
};
use rusqlite::{params, Connection, OptionalExtension};
use sha2::{Digest, Sha256};

pub const DEV_BASELINE_BRAIN_CLI_PRINCIPAL: &str = "workload:brain-cli";

/// Authorization decisions and the current policy epoch share the protected
/// storage database. The initial epoch is 1; zero is never a valid epoch.
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

pub fn initialize(connection: &Connection) -> Result<(), StorageError> {
    connection
        .execute_batch(AUTHORIZATION_SCHEMA)
        .map_err(|_| StorageError::TransactionUnavailable)
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

    let digest = Sha256::digest(&bytes);
    Ok(digest.iter().map(|byte| format!("{byte:02x}")).collect())
}

/// Convert a Unix timestamp to an RFC3339 UTC timestamp without introducing
/// a date/time dependency.
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

    let hour = day_seconds / 3_600;
    let minute = (day_seconds % 3_600) / 60;
    let second = day_seconds % 60;

    format!(
        "{year:04}-{month:02}-{day:02}T{hour:02}:{minute:02}:{second:02}.{:09}Z",
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
    let configured = configured_principal()?;

    if subject.principal_ref != configured {
        return Err(StorageError::PermissionDenied);
    }

    if subject.scopes.is_empty() {
        return Err(StorageError::InvalidSchema);
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
    let epoch = current_epoch(connection)?;

    if expected.epoch != epoch {
        return Err(StorageError::PermissionDenied);
    }

    let row = connection
        .query_row(
            "SELECT issuer, subject_digest, issued_at, decision_kind,
                    principal_ref, operation, target_kind, target_id, epoch
             FROM authorization_decisions
             WHERE decision_id = ?1",
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

/// Crate-private identity token for the SQLite connection participating in
/// the current transaction.
///
/// This token owns only the connection address as an identity value. It does
/// not dereference the address or extend the connection lifetime. The
/// TxAuthority that performs validation separately holds the actual
/// connection borrow for the duration of the validation call.
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

/// Authority adapter whose validation reads through the exact connection
/// borrowed by the caller's SQLite transaction.
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

impl AuthorizationAuthority for SqliteMemoryStorage {
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
