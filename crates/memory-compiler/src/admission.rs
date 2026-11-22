//! Durable producer admission primitives for the Memory Compiler.
//!
//! This crate implements the E-side lifecycle and a local SQLite admission
//! ledger. It does not claim to be the D-authoritative producer ledger or to
//! provide a cross-service D/Storage visibility transaction.

use memory_domain::{
    is_rfc3339_utc, is_sha256_hex, AttestorData, AttestorRef, AuthorizationDecisionData,
    AuthorizationDecisionKind, AuthorizationDecisionRef, CanonicalCommitData, CanonicalCommitRef,
    IssuerId, OpaqueId, ScopeRef, DEV_BASELINE_ISSUER, I_DEV_BASELINE_ISSUER,
};
use rusqlite::{params, Connection, OptionalExtension, Transaction, TransactionBehavior};
use serde::{de::DeserializeOwned, Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    path::Path,
    time::{Duration, SystemTime, UNIX_EPOCH},
};

/// E-side lifecycle state defined by compiler admission specification §2.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum WorkState {
    Received,
    Validating,
    Accepted,
    DRegistrationPending,
    Registered,
    Queued,
    Leased,
    Running,
    CandidatePrivate,
    StagedPrivate,
    DependencyRegistrationPending,
    DependencyRegistered,
    PreparedHidden,
    PublicationGatePending,
    Published,
    RetryQueued,
    DlqParked,
    SuppressedQuarantined,
    Rejected,
    Cancelled,
    UnknownReconciliation,
    Terminal,
}

/// D barrier interpretation for each E lifecycle state, per §3.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum BarrierMeaning {
    NoAdmissionImplied,
    RegistrationOutcomeMustBeResolved,
    DurableRegistrationOpen,
    DurableRegistrationOpenLeaseTelemetry,
    DurableRegistrationOpenExecutionTelemetry,
    DurableRegistrationOpenPrivateStaging,
    DependencyInventoryMustBeComplete,
    DependenciesDurableArtifactHidden,
    PublicationDecisionPendingArtifactHidden,
    PublicationReceiptDurable,
    NonTerminalReplayRemainsPossible,
    SuppressedNoPublicationEvidenceRequired,
    TerminalEvidenceRequiresDValidation,
    OutcomeUnknownFailClosed,
}

/// Errors returned by state, registration and publication operations.
#[derive(Debug)]
pub enum AdmissionError {
    Sqlite(rusqlite::Error),
    Serialization(serde_json::Error),
    InvalidInput(&'static str),
    InvalidTransition {
        from: WorkState,
        to: WorkState,
    },
    IdempotencyConflict,
    ProducerAlreadyRegistered,
    ProducerNotRegistered {
        producer_id: String,
    },
    NotFound,
    DependencySetIncomplete,
    StaleFence {
        expected: u64,
        actual: u64,
    },
    StaleProtocol {
        expected: u64,
        actual: u64,
    },
    ReceiptMismatch,
    /// Canonical commit validation could not establish authority. §4.2 of
    /// `D-OWNER-DECISION-CANONICAL-COMMIT-001`: a missing or unreadable record
    /// is an authority failure, never `Ok(false)`.
    CanonicalCommit(CanonicalCommitValidationError),
    /// Authorization decision validation could not establish a matching
    /// durable I record.
    AuthorizationDecision(AuthorizationDecisionValidationError),
}

impl std::fmt::Display for AdmissionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Sqlite(e) => write!(f, "admission SQLite error: {e}"),
            Self::Serialization(e) => write!(f, "admission serialization error: {e}"),
            Self::InvalidInput(s) => write!(f, "invalid admission input: {s}"),
            Self::InvalidTransition { from, to } => {
                write!(f, "illegal work transition: {from:?} -> {to:?}")
            }
            Self::IdempotencyConflict => {
                write!(f, "idempotency key reused with a different digest")
            }
            Self::ProducerAlreadyRegistered => write!(f, "producer is already registered"),
            Self::ProducerNotRegistered { producer_id } => {
                write!(f, "producer is not registered: {producer_id}")
            }
            Self::NotFound => write!(f, "admission receipt or work item not found"),
            Self::DependencySetIncomplete => write!(f, "dependency registration set is incomplete"),
            Self::StaleFence { expected, actual } => write!(
                f,
                "stale fence generation: observed {expected}, current {actual}"
            ),
            Self::StaleProtocol { expected, actual } => write!(
                f,
                "stale admission protocol sequence: observed {expected}, current {actual}"
            ),
            Self::ReceiptMismatch => write!(
                f,
                "dependency receipt set does not match the registered artifact"
            ),
            Self::CanonicalCommit(e) => write!(f, "canonical commit not established: {e}"),
            Self::AuthorizationDecision(e) => {
                write!(f, "authorization decision not established: {e}")
            }
        }
    }
}
impl std::error::Error for AdmissionError {}
impl From<rusqlite::Error> for AdmissionError {
    fn from(value: rusqlite::Error) -> Self {
        Self::Sqlite(value)
    }
}
impl From<serde_json::Error> for AdmissionError {
    fn from(value: serde_json::Error) -> Self {
        Self::Serialization(value)
    }
}

/// Producer work registration request, carrying the minimum §4.1 identity,
/// lineage, scope, cursor, authorization and idempotency evidence.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ProducerRegistrationRequest {
    pub producer_work_item_id: OpaqueId,
    pub producer_class: String,
    pub producer_identity: OpaqueId,
    pub source_refs: Vec<OpaqueId>,
    pub source_lineage_digest: String,
    pub scope_refs: Vec<ScopeRef>,
    pub operation_id: OpaqueId,
    pub correlation_id: OpaqueId,
    pub causation_id: Option<OpaqueId>,
    /// Caller-supplied cursor, persisted without validation. Its presence is not
    /// evidence that a canonical commit was confirmed (D6.3).
    pub admission_canonical_commit_cursor: Option<OpaqueId>,
    /// The reference the cursor selects. Only an issued reference can validate,
    /// and only against the durable `canonical_commits` row. Rows written before
    /// this field existed decode as `pending_d()`, which never validates (§6).
    #[serde(default = "pending_canonical_commit_ref")]
    pub canonical_commit_ref: CanonicalCommitRef,
    pub observed_fence_cursor: OpaqueId,
    pub permission_epoch: OpaqueId,
    pub request_digest: String,
    pub producer_schema_version: String,
}

/// Durable local receipt corresponding to §4.1.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ProducerRegistrationReceipt {
    pub receipt_id: OpaqueId,
    pub producer_work_item_id: OpaqueId,
    pub request_digest: String,
    pub ledger_sequence: u64,
    pub disposition: RegistrationDisposition,
}

/// Admission disposition stored in the producer receipt.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum RegistrationDisposition {
    Accepted,
    Rejected,
}

/// One dependency edge request for a derived artifact, per §4.2.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DependencyRegistrationRequest {
    pub dependency_registration_id: OpaqueId,
    pub artifact_ref: OpaqueId,
    pub artifact_version: OpaqueId,
    pub producer_work_item_id: OpaqueId,
    pub derivation_run_id: OpaqueId,
    pub source_ref: OpaqueId,
    pub source_version: Option<OpaqueId>,
    pub provenance_ref: OpaqueId,
    pub scope_refs: Vec<ScopeRef>,
    pub lineage_digest: String,
    pub required_dependency_count: u32,
    pub request_digest: String,
}

/// Durable local receipt for one dependency edge, per §4.2.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DependencyRegistrationReceipt {
    pub receipt_id: OpaqueId,
    pub dependency_registration_id: OpaqueId,
    pub artifact_ref: OpaqueId,
    pub artifact_version: OpaqueId,
    pub request_digest: String,
}

/// Final gate request, per §4.3. The protocol sequence and fence generation
/// are separate typed observations; neither is a PermissionEpoch.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct PublicationGateRequest {
    pub publication_operation_id: OpaqueId,
    pub artifact_ref: OpaqueId,
    pub artifact_version: OpaqueId,
    pub producer_work_item_id: OpaqueId,
    pub derivation_run_id: OpaqueId,
    pub attempt_id: OpaqueId,
    pub lease_id: OpaqueId,
    pub dependency_receipt_ids: Vec<OpaqueId>,
    pub permission_epoch: OpaqueId,
    pub observed_fence_generation: u64,
    pub observed_protocol_sequence: u64,
    pub scope_refs: Vec<ScopeRef>,
    pub request_digest: String,
}

/// Why a canonical commit could not be established (§4.2 of
/// `D-OWNER-DECISION-CANONICAL-COMMIT-001`).
///
/// Every variant maps to `Err` at the validator boundary. `Ok(false)` is
/// reserved for exactly one case: a readable record whose subject digest does
/// not equal the expected one.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum CanonicalCommitValidationError {
    /// The reference is `pending_d()`; it carries no commit evidence.
    PendingReference,
    /// The cursor is a lookup selector and must name the reference's commit.
    CursorMismatch,
    /// No durable `canonical_commits` row exists for the commit id.
    RecordMissing,
    /// The stored row exists but is not a well-formed record.
    RecordMalformed,
    /// A stored field differs from the reference it is supposed to back.
    RecordMismatch(&'static str),
    /// The issuer is not the dev-baseline trust anchor.
    UnsupportedIssuer,
    /// The database could not be read.
    ReadFailed,
}

impl std::fmt::Display for CanonicalCommitValidationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::PendingReference => write!(f, "reference is pending"),
            Self::CursorMismatch => write!(f, "cursor does not select the reference's commit"),
            Self::RecordMissing => write!(f, "no durable canonical commit record"),
            Self::RecordMalformed => write!(f, "canonical commit record is malformed"),
            Self::RecordMismatch(field) => {
                write!(f, "canonical commit record disagrees on {field}")
            }
            Self::UnsupportedIssuer => write!(f, "issuer is not on the dev-baseline allowlist"),
            Self::ReadFailed => write!(f, "canonical commit record is unreadable"),
        }
    }
}

impl std::error::Error for CanonicalCommitValidationError {}

/// Why a durable authorization decision could not be validated.
///
/// Missing and unreadable records are errors, never `Ok(false)`.
/// `Ok(false)` is reserved exclusively for a matching record whose
/// subject digest differs from the expected digest.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AuthorizationDecisionValidationError {
    /// The reference does not carry issued decision data.
    PendingReference,
    /// No durable authorization decision row exists.
    RecordMissing,
    /// The stored row is not a well-formed record.
    RecordMalformed,
    /// A stored field differs from the issued reference.
    RecordMismatch(&'static str),
    /// The issuer is not the I dev-baseline trust anchor.
    UnsupportedIssuer,
    /// The database could not be read.
    ReadFailed,
}

impl std::fmt::Display for AuthorizationDecisionValidationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::PendingReference => write!(f, "reference is pending"),
            Self::RecordMissing => {
                write!(f, "no durable authorization decision record")
            }
            Self::RecordMalformed => {
                write!(f, "authorization decision record is malformed")
            }
            Self::RecordMismatch(field) => {
                write!(f, "authorization decision record disagrees on {field}")
            }
            Self::UnsupportedIssuer => {
                write!(f, "issuer is not on the I dev-baseline allowlist")
            }
            Self::ReadFailed => {
                write!(f, "authorization decision record is unreadable")
            }
        }
    }
}

impl std::error::Error for AuthorizationDecisionValidationError {}

/// Why an attestor could not be established from its durable I-side record.
///
/// A subject digest mismatch is an authority error here, not a boolean
/// disposition: unlike an authorization decision, an attestation has no
/// `Ok(false)` outcome.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AttestorValidationError {
    /// The reference does not carry issued attestation data.
    PendingReference,
    /// No durable attestation row exists.
    RecordMissing,
    /// The stored row is not a well-formed record.
    RecordMalformed,
    /// A stored field differs from the issued reference, or from the expected
    /// subject digest.
    RecordMismatch(&'static str),
    /// The issuer is not the I dev-baseline trust anchor.
    UnsupportedIssuer,
    /// The database could not be read.
    ReadFailed,
}

impl std::fmt::Display for AttestorValidationError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::PendingReference => write!(f, "attestor reference is pending"),
            Self::RecordMissing => write!(f, "no durable attestation record"),
            Self::RecordMalformed => write!(f, "attestation record is malformed"),
            Self::RecordMismatch(field) => {
                write!(f, "attestation record disagrees on {field}")
            }
            Self::UnsupportedIssuer => {
                write!(
                    f,
                    "attestation issuer is not on the I dev-baseline allowlist"
                )
            }
            Self::ReadFailed => write!(f, "attestation record is unreadable"),
        }
    }
}

impl std::error::Error for AttestorValidationError {}

/// Durable publication decision bound to the exact artifact, dependencies,
/// fence generation and permission epoch, per §4.3.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct PublicationReceipt {
    pub receipt_id: OpaqueId,
    pub publication_operation_id: OpaqueId,
    pub artifact_ref: OpaqueId,
    pub artifact_version: OpaqueId,
    pub producer_work_item_id: OpaqueId,
    pub dependency_receipt_ids: Vec<OpaqueId>,
    pub fence_generation: u64,
    pub permission_epoch: OpaqueId,
    pub protocol_sequence: u64,
    pub visible: bool,
}

/// Result of a local fence-installation compare-and-swap, used to make the
/// local serialization boundary explicit in tests.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FenceInstallReceipt {
    pub fence_generation: u64,
    pub protocol_sequence: u64,
}

/// Local SQLite-backed producer admission ledger.
pub struct AdmissionStore {
    connection: Connection,
}

impl AdmissionStore {
    /// Open a durable WAL-backed admission database, as required by §4.1–§4.3.
    pub fn open(path: impl AsRef<Path>) -> Result<Self, AdmissionError> {
        let connection = Connection::open(path)?;
        connection.busy_timeout(Duration::from_secs(5))?;
        connection.execute_batch("PRAGMA journal_mode=WAL; PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;")?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    /// Open an in-memory admission database for isolated conformance tests (§4.1–§4.3).
    pub fn in_memory() -> Result<Self, AdmissionError> {
        let connection = Connection::open_in_memory()?;
        connection.busy_timeout(Duration::from_secs(5))?;
        connection.execute_batch(
            "PRAGMA synchronous=FULL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;",
        )?;
        let store = Self { connection };
        store.initialize()?;
        Ok(store)
    }

    fn initialize(&self) -> Result<(), AdmissionError> {
        self.connection.execute_batch(
            "CREATE TABLE IF NOT EXISTS admission_meta (
                singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                fence_generation INTEGER NOT NULL CHECK(fence_generation>=0),
                protocol_sequence INTEGER NOT NULL CHECK(protocol_sequence>=0)
             );
             INSERT OR IGNORE INTO admission_meta(singleton,fence_generation,protocol_sequence) VALUES(1,0,0);
             CREATE TABLE IF NOT EXISTS producer_registry (
                producer_id TEXT PRIMARY KEY,
                registered_at TEXT NOT NULL,
                registry_digest TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS producer_work (
                ledger_sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                work_item_id TEXT NOT NULL UNIQUE,
                request_digest TEXT NOT NULL,
                request_json TEXT NOT NULL,
                receipt_json TEXT NOT NULL,
                state_json TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS dependency_edges (
                ledger_sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                dependency_id TEXT NOT NULL UNIQUE,
                artifact_ref TEXT NOT NULL,
                artifact_version TEXT NOT NULL,
                work_item_id TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                request_json TEXT NOT NULL,
                receipt_json TEXT NOT NULL
             );
             CREATE INDEX IF NOT EXISTS dependency_artifact_idx
                ON dependency_edges(artifact_ref,artifact_version);
             CREATE TABLE IF NOT EXISTS publication_receipts (
                publication_id TEXT PRIMARY KEY,
                artifact_ref TEXT NOT NULL,
                artifact_version TEXT NOT NULL,
                request_digest TEXT NOT NULL,
                receipt_json TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS canonical_commits (
                commit_id       TEXT PRIMARY KEY NOT NULL,
                issuer_id       TEXT NOT NULL,
                subject_digest  TEXT NOT NULL,
                issued_at       TEXT NOT NULL,
                signature       TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS authorization_decisions (
                decision_id      TEXT PRIMARY KEY NOT NULL,
                issuer_id        TEXT NOT NULL,
                subject_digest   TEXT NOT NULL,
                issued_at        TEXT NOT NULL,
                decision_kind    TEXT NOT NULL,
                signature        TEXT NOT NULL
             );
             CREATE TABLE IF NOT EXISTS i_attestations (
                attestation_id   TEXT PRIMARY KEY NOT NULL,
                issuer_id        TEXT NOT NULL,
                subject_digest   TEXT NOT NULL,
                issued_at        TEXT NOT NULL,
                signature        TEXT NOT NULL
             );"
        )?;
        Ok(())
    }

    /// Resolve the E-state to D barrier meaning defined by §3.
    pub fn barrier_meaning(state: WorkState) -> BarrierMeaning {
        match state {
            WorkState::Received | WorkState::Validating | WorkState::Accepted => {
                BarrierMeaning::NoAdmissionImplied
            }
            WorkState::DRegistrationPending | WorkState::UnknownReconciliation => {
                BarrierMeaning::OutcomeUnknownFailClosed
            }
            WorkState::Registered | WorkState::Queued => BarrierMeaning::DurableRegistrationOpen,
            WorkState::Leased => BarrierMeaning::DurableRegistrationOpenLeaseTelemetry,
            WorkState::Running | WorkState::CandidatePrivate => {
                BarrierMeaning::DurableRegistrationOpenExecutionTelemetry
            }
            WorkState::StagedPrivate => BarrierMeaning::DurableRegistrationOpenPrivateStaging,
            WorkState::DependencyRegistrationPending => {
                BarrierMeaning::DependencyInventoryMustBeComplete
            }
            WorkState::DependencyRegistered => BarrierMeaning::DependenciesDurableArtifactHidden,
            WorkState::PreparedHidden => BarrierMeaning::DependenciesDurableArtifactHidden,
            WorkState::PublicationGatePending => {
                BarrierMeaning::PublicationDecisionPendingArtifactHidden
            }
            WorkState::Published => BarrierMeaning::PublicationReceiptDurable,
            WorkState::RetryQueued | WorkState::DlqParked => {
                BarrierMeaning::NonTerminalReplayRemainsPossible
            }
            WorkState::SuppressedQuarantined => {
                BarrierMeaning::SuppressedNoPublicationEvidenceRequired
            }
            WorkState::Rejected | WorkState::Cancelled | WorkState::Terminal => {
                BarrierMeaning::TerminalEvidenceRequiresDValidation
            }
        }
    }

    /// Return the complete legal transition relation defined by §2.
    pub fn legal_transition(from: WorkState, to: WorkState) -> bool {
        use WorkState::*;
        matches!(
            (from, to),
            (Received, Validating)
                | (Validating, Accepted)
                | (Validating, Rejected)
                | (Accepted, DRegistrationPending)
                | (Accepted, Cancelled)
                | (Accepted, SuppressedQuarantined)
                | (DRegistrationPending, Registered)
                | (DRegistrationPending, UnknownReconciliation)
                | (UnknownReconciliation, Registered)
                | (UnknownReconciliation, DRegistrationPending)
                | (Registered, Queued)
                | (Queued, Leased)
                | (Leased, Running)
                | (Running, CandidatePrivate)
                | (Running, RetryQueued)
                | (Running, SuppressedQuarantined)
                | (CandidatePrivate, StagedPrivate)
                | (CandidatePrivate, RetryQueued)
                | (CandidatePrivate, SuppressedQuarantined)
                | (StagedPrivate, DependencyRegistrationPending)
                | (StagedPrivate, RetryQueued)
                | (StagedPrivate, SuppressedQuarantined)
                | (DependencyRegistrationPending, DependencyRegistered)
                | (DependencyRegistrationPending, RetryQueued)
                | (DependencyRegistrationPending, UnknownReconciliation)
                | (DependencyRegistered, PreparedHidden)
                | (PreparedHidden, PublicationGatePending)
                | (PublicationGatePending, Published)
                | (PublicationGatePending, SuppressedQuarantined)
                | (RetryQueued, Queued)
                | (RetryQueued, DlqParked)
                | (DlqParked, RetryQueued)
                | (SuppressedQuarantined, Terminal)
                | (Published, Terminal)
                | (Rejected, Terminal)
                | (Cancelled, Terminal)
                | (Leased, Cancelled)
                | (Leased, SuppressedQuarantined)
                | (Queued, Cancelled)
                | (Queued, SuppressedQuarantined)
                | (Running, Cancelled)
                | (StagedPrivate, Cancelled)
        )
    }

    /// Persist a legal lifecycle transition, rejecting all edges outside §2.
    pub fn transition_work_state(
        &mut self,
        work_item_id: &OpaqueId,
        next: WorkState,
    ) -> Result<(), AdmissionError> {
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let state_json: String = tx
            .query_row(
                "SELECT state_json FROM producer_work WHERE work_item_id=?1",
                [work_item_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        let current: WorkState = decode(&state_json)?;
        if !Self::legal_transition(current, next) {
            return Err(AdmissionError::InvalidTransition {
                from: current,
                to: next,
            });
        }
        tx.execute(
            "UPDATE producer_work SET state_json=?1 WHERE work_item_id=?2",
            params![encode(&next)?, work_item_id.as_str()],
        )?;
        tx.commit()?;
        Ok(())
    }

    /// Register a producer identity independently from admitting any work item.
    /// Repeated registration is an explicit error, even when the digest matches.
    /// This is a local registry operation: callers must restrict access to this
    /// method to trusted bootstrap/configuration code; it does not authenticate identities.
    pub fn register_producer(
        &mut self,
        producer_id: &OpaqueId,
        registry_digest: &str,
    ) -> Result<(), AdmissionError> {
        if registry_digest.trim().is_empty() {
            return Err(AdmissionError::InvalidInput("producer registry digest"));
        }
        let registered_at = timestamp_unix_nanos().to_string();
        match self.connection.execute(
            "INSERT INTO producer_registry(producer_id,registered_at,registry_digest) VALUES(?1,?2,?3)",
            params![producer_id.as_str(), registered_at, registry_digest],
        ) {
            Ok(_) => Ok(()),
            Err(rusqlite::Error::SqliteFailure(error, _))
                if error.code == rusqlite::ErrorCode::ConstraintViolation =>
            {
                Err(AdmissionError::ProducerAlreadyRegistered)
            }
            Err(error) => Err(AdmissionError::Sqlite(error)),
        }
    }

    /// Whether a producer identity has an independent registry row.
    pub fn is_producer_registered(&self, producer_id: &OpaqueId) -> Result<bool, AdmissionError> {
        self.connection
            .query_row(
                "SELECT EXISTS(SELECT 1 FROM producer_registry WHERE producer_id=?1)",
                [producer_id.as_str()],
                |row| row.get(0),
            )
            .map_err(AdmissionError::from)
    }

    /// Register one logical ProducerWorkItem idempotently, as required by §4.1.
    pub fn register_producer_work(
        &mut self,
        request: ProducerRegistrationRequest,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let producer_registered: bool = tx.query_row(
            "SELECT EXISTS(SELECT 1 FROM producer_registry WHERE producer_id=?1)",
            [request.producer_identity.as_str()],
            |row| row.get(0),
        )?;
        if !producer_registered {
            return Err(AdmissionError::ProducerNotRegistered {
                producer_id: request.producer_identity.as_str().to_owned(),
            });
        }
        validate_producer_request(&request)?;
        if let Some((digest, receipt_json)) = tx
            .query_row(
                "SELECT request_digest,receipt_json FROM producer_work WHERE work_item_id=?1",
                [request.producer_work_item_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
            )
            .optional()?
        {
            if digest != request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            let receipt = decode(&receipt_json)?;
            tx.commit()?;
            return Ok(receipt);
        }
        let request_json = encode(&request)?;
        tx.execute(
            "INSERT INTO producer_work(work_item_id,request_digest,request_json,receipt_json,state_json) VALUES(?1,?2,?3,'',?4)",
            params![request.producer_work_item_id.as_str(), request.request_digest, request_json, encode(&WorkState::Accepted)?]
        )?;
        let sequence = tx.last_insert_rowid() as u64;
        let receipt = ProducerRegistrationReceipt {
            receipt_id: OpaqueId::new(format!("producer-registration:{sequence}"))
                .map_err(|_| AdmissionError::InvalidInput("receipt id"))?,
            producer_work_item_id: request.producer_work_item_id.clone(),
            request_digest: request.request_digest.clone(),
            ledger_sequence: sequence,
            disposition: RegistrationDisposition::Accepted,
        };
        tx.execute(
            "UPDATE producer_work SET receipt_json=?1 WHERE work_item_id=?2",
            params![encode(&receipt)?, request.producer_work_item_id.as_str()],
        )?;
        tx.commit()?;
        Ok(receipt)
    }

    /// Look up the durable ProducerRegistrationReceipt by ProducerWorkItemId (§4.1).
    pub fn producer_receipt(
        &self,
        work_item_id: &OpaqueId,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        let value: String = self
            .connection
            .query_row(
                "SELECT receipt_json FROM producer_work WHERE work_item_id=?1",
                [work_item_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        decode(&value)
    }

    /// Read the request paired with a local producer receipt. This proves only
    /// that a row exists in this local ledger; it is not external registry
    /// authorization and must not be represented as such.
    pub fn producer_request(
        &self,
        work_item_id: &OpaqueId,
    ) -> Result<ProducerRegistrationRequest, AdmissionError> {
        let value: String = self
            .connection
            .query_row(
                "SELECT request_json FROM producer_work WHERE work_item_id=?1",
                [work_item_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        decode(&value)
    }

    /// Return persisted dependency requests and receipts for the exact artifact.
    /// A foreign producer work item is rejected rather than silently included.
    pub fn dependency_entries_for(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
        work_item_id: &OpaqueId,
    ) -> Result<Vec<(DependencyRegistrationRequest, DependencyRegistrationReceipt)>, AdmissionError>
    {
        let mut statement = self.connection.prepare(
            "SELECT request_json,receipt_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2"
        )?;
        let rows = statement.query_map(
            params![artifact_ref.as_str(), artifact_version.as_str()],
            |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
        )?;
        let mut entries = Vec::new();
        for row in rows {
            let (request_json, receipt_json) = row?;
            let request: DependencyRegistrationRequest = decode(&request_json)?;
            let receipt: DependencyRegistrationReceipt = decode(&receipt_json)?;
            if &request.producer_work_item_id != work_item_id {
                return Err(AdmissionError::ReceiptMismatch);
            }
            entries.push((request, receipt));
        }
        Ok(entries)
    }

    /// Count publication receipts for a focused compiler-wiring assertion.
    pub fn publication_receipt_count(&self) -> Result<u64, AdmissionError> {
        let count: i64 =
            self.connection
                .query_row("SELECT COUNT(*) FROM publication_receipts", [], |row| {
                    row.get(0)
                })?;
        Ok(count as u64)
    }

    #[cfg(test)]
    pub(crate) fn block_publication_receipt_writes(&self) -> Result<(), AdmissionError> {
        self.connection.execute_batch(
            "CREATE TRIGGER reject_compiler_publication BEFORE INSERT ON publication_receipts
             BEGIN SELECT RAISE(FAIL, 'injected publication receipt write failure'); END;",
        )?;
        Ok(())
    }

    /// Count producer ledger rows, exposing the idempotency invariant for §4.1 tests.
    pub fn producer_ledger_count(&self) -> Result<u64, AdmissionError> {
        let count: i64 =
            self.connection
                .query_row("SELECT COUNT(*) FROM producer_work", [], |row| row.get(0))?;
        Ok(count as u64)
    }

    /// Register one artifact dependency edge idempotently; incomplete sets remain hidden (§4.2).
    pub fn register_dependency(
        &mut self,
        request: DependencyRegistrationRequest,
    ) -> Result<DependencyRegistrationReceipt, AdmissionError> {
        validate_dependency_request(&request)?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        if let Some((digest, receipt_json)) = tx
            .query_row(
                "SELECT request_digest,receipt_json FROM dependency_edges WHERE dependency_id=?1",
                [request.dependency_registration_id.as_str()],
                |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?)),
            )
            .optional()?
        {
            if digest != request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            let receipt = decode(&receipt_json)?;
            tx.commit()?;
            return Ok(receipt);
        }
        let work_exists: bool = tx.query_row(
            "SELECT EXISTS(SELECT 1 FROM producer_work WHERE work_item_id=?1)",
            [request.producer_work_item_id.as_str()],
            |row| row.get(0),
        )?;
        if !work_exists {
            return Err(AdmissionError::NotFound);
        }
        let receipt_id = format!(
            "dependency-registration:{}",
            request.dependency_registration_id.as_str()
        );
        let receipt = DependencyRegistrationReceipt {
            receipt_id: OpaqueId::new(receipt_id)
                .map_err(|_| AdmissionError::InvalidInput("dependency receipt id"))?,
            dependency_registration_id: request.dependency_registration_id.clone(),
            artifact_ref: request.artifact_ref.clone(),
            artifact_version: request.artifact_version.clone(),
            request_digest: request.request_digest.clone(),
        };
        tx.execute(
            "INSERT INTO dependency_edges(dependency_id,artifact_ref,artifact_version,work_item_id,request_digest,request_json,receipt_json) VALUES(?1,?2,?3,?4,?5,?6,?7)",
            params![request.dependency_registration_id.as_str(), request.artifact_ref.as_str(), request.artifact_version.as_str(), request.producer_work_item_id.as_str(), request.request_digest, encode(&request)?, encode(&receipt)?]
        )?;
        tx.commit()?;
        Ok(receipt)
    }

    /// Return whether all declared dependency edges exist; never treats a partial set as visible (§4.2).
    pub fn dependencies_complete(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        let mut statement = self.connection.prepare(
            "SELECT request_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2"
        )?;
        let rows = statement.query_map(
            params![artifact_ref.as_str(), artifact_version.as_str()],
            |row| row.get::<_, String>(0),
        )?;
        let mut required = None;
        let mut count = 0_u32;
        for row in rows {
            let request: DependencyRegistrationRequest = decode(&row?)?;
            if let Some(expected) = required {
                if expected != request.required_dependency_count {
                    return Err(AdmissionError::InvalidInput(
                        "inconsistent dependency count",
                    ));
                }
            } else {
                required = Some(request.required_dependency_count);
            }
            count += 1;
        }
        Ok(required.map(|n| count >= n).unwrap_or(false))
    }

    /// Read the current local fence generation and protocol sequence (§4.3).
    pub fn observe_fence(&self) -> Result<FenceInstallReceipt, AdmissionError> {
        self.connection
            .query_row(
                "SELECT fence_generation,protocol_sequence FROM admission_meta WHERE singleton=1",
                [],
                |row| {
                    Ok(FenceInstallReceipt {
                        fence_generation: row.get::<_, i64>(0)? as u64,
                        protocol_sequence: row.get::<_, i64>(1)? as u64,
                    })
                },
            )
            .map_err(AdmissionError::from)
    }

    /// Install a fence only if the observed protocol sequence is current (§4.3).
    pub fn install_fence(
        &mut self,
        expected_protocol_sequence: u64,
    ) -> Result<FenceInstallReceipt, AdmissionError> {
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let current = read_meta(&tx)?;
        if current.protocol_sequence != expected_protocol_sequence {
            return Err(AdmissionError::StaleProtocol {
                expected: expected_protocol_sequence,
                actual: current.protocol_sequence,
            });
        }
        let next = FenceInstallReceipt {
            fence_generation: current.fence_generation + 1,
            protocol_sequence: current.protocol_sequence + 1,
        };
        tx.execute(
            "UPDATE admission_meta SET fence_generation=?1,protocol_sequence=?2 WHERE singleton=1",
            params![next.fence_generation as i64, next.protocol_sequence as i64],
        )?;
        tx.commit()?;
        Ok(next)
    }

    /// Execute the final gate in the same SQLite serialization domain as fence installation (§4.3).
    ///
    /// This local implementation atomically persists the publication decision and
    /// consumes the observed protocol sequence. It is not a D service API and does
    /// not establish a cross-service Storage visibility transaction.
    ///
    /// Validation order is deliberate: the fence generation is checked before the
    /// protocol sequence, so a concurrent fence installation always surfaces as
    /// `StaleFence` rather than `StaleProtocol`. Callers must not depend on which
    /// counter moved to distinguish the two races; both mean "re-observe and retry".
    pub fn final_publication_gate(
        &mut self,
        request: PublicationGateRequest,
    ) -> Result<PublicationReceipt, AdmissionError> {
        validate_publication_request(&request)?;
        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        if let Some((digest, receipt_json)) = tx.query_row(
            "SELECT request_digest,receipt_json FROM publication_receipts WHERE publication_id=?1",
            [request.publication_operation_id.as_str()],
            |row| Ok((row.get::<_, String>(0)?, row.get::<_, String>(1)?))
        ).optional()? {
            if digest != request.request_digest { return Err(AdmissionError::IdempotencyConflict); }
            let receipt = decode(&receipt_json)?;
            tx.commit()?;
            return Ok(receipt);
        }
        let meta = read_meta(&tx)?;
        if meta.fence_generation != request.observed_fence_generation {
            return Err(AdmissionError::StaleFence {
                expected: request.observed_fence_generation,
                actual: meta.fence_generation,
            });
        }
        if meta.protocol_sequence != request.observed_protocol_sequence {
            return Err(AdmissionError::StaleProtocol {
                expected: request.observed_protocol_sequence,
                actual: meta.protocol_sequence,
            });
        }
        let work_exists: bool = tx.query_row(
            "SELECT EXISTS(SELECT 1 FROM producer_work WHERE work_item_id=?1)",
            [request.producer_work_item_id.as_str()],
            |row| row.get(0),
        )?;
        if !work_exists {
            return Err(AdmissionError::NotFound);
        }

        let mut statement = tx.prepare(
            "SELECT receipt_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2"
        )?;
        let rows = statement.query_map(
            params![
                request.artifact_ref.as_str(),
                request.artifact_version.as_str()
            ],
            |row| row.get::<_, String>(0),
        )?;
        let mut stored_ids = Vec::new();
        for row in rows {
            let receipt: DependencyRegistrationReceipt = decode(&row?)?;
            stored_ids.push(receipt.receipt_id);
        }
        drop(statement);
        if !Self::dependencies_complete_tx(&tx, &request.artifact_ref, &request.artifact_version)? {
            return Err(AdmissionError::DependencySetIncomplete);
        }
        let mut provided = request.dependency_receipt_ids.clone();
        stored_ids.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        provided.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        if stored_ids != provided {
            return Err(AdmissionError::ReceiptMismatch);
        }

        let next_sequence = meta.protocol_sequence + 1;
        let receipt = PublicationReceipt {
            receipt_id: OpaqueId::new(format!(
                "publication:{}",
                request.publication_operation_id.as_str()
            ))
            .map_err(|_| AdmissionError::InvalidInput("publication receipt id"))?,
            publication_operation_id: request.publication_operation_id.clone(),
            artifact_ref: request.artifact_ref.clone(),
            artifact_version: request.artifact_version.clone(),
            producer_work_item_id: request.producer_work_item_id.clone(),
            dependency_receipt_ids: provided,
            fence_generation: meta.fence_generation,
            permission_epoch: request.permission_epoch.clone(),
            protocol_sequence: next_sequence,
            visible: true,
        };
        tx.execute("INSERT INTO publication_receipts(publication_id,artifact_ref,artifact_version,request_digest,receipt_json) VALUES(?1,?2,?3,?4,?5)",
            params![request.publication_operation_id.as_str(), request.artifact_ref.as_str(), request.artifact_version.as_str(), request.request_digest, encode(&receipt)?])?;
        tx.execute(
            "UPDATE admission_meta SET protocol_sequence=?1 WHERE singleton=1",
            [next_sequence as i64],
        )?;
        tx.commit()?;
        Ok(receipt)
    }

    fn dependencies_complete_tx(
        tx: &Transaction<'_>,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        let mut statement = tx.prepare("SELECT request_json FROM dependency_edges WHERE artifact_ref=?1 AND artifact_version=?2")?;
        let rows = statement.query_map(
            params![artifact_ref.as_str(), artifact_version.as_str()],
            |row| row.get::<_, String>(0),
        )?;
        let mut required = None;
        let mut count = 0_u32;
        for row in rows {
            let request: DependencyRegistrationRequest = decode(&row?)?;
            if let Some(expected) = required {
                if expected != request.required_dependency_count {
                    return Err(AdmissionError::InvalidInput(
                        "inconsistent dependency count",
                    ));
                }
            } else {
                required = Some(request.required_dependency_count);
            }
            count += 1;
        }
        Ok(required.map(|n| count >= n).unwrap_or(false))
    }

    /// Report whether an artifact has a committed local publication receipt (§4.2–§4.3).
    pub fn is_artifact_visible(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        let count: i64 = self.connection.query_row(
            "SELECT COUNT(*) FROM publication_receipts WHERE artifact_ref=?1 AND artifact_version=?2",
            params![artifact_ref.as_str(), artifact_version.as_str()], |row| row.get(0)
        )?;
        Ok(count > 0)
    }

    /// Count dependency ledger rows for idempotency and partial-registration checks (§4.2).
    pub fn dependency_ledger_count(&self) -> Result<u64, AdmissionError> {
        let count: i64 =
            self.connection
                .query_row("SELECT COUNT(*) FROM dependency_edges", [], |row| {
                    row.get(0)
                })?;
        Ok(count as u64)
    }

    /// Retrieve the committed PublicationReceipt by PublicationOperationId (§4.3).
    pub fn publication_receipt(
        &self,
        operation_id: &OpaqueId,
    ) -> Result<PublicationReceipt, AdmissionError> {
        let value: String = self
            .connection
            .query_row(
                "SELECT receipt_json FROM publication_receipts WHERE publication_id=?1",
                [operation_id.as_str()],
                |row| row.get(0),
            )
            .optional()?
            .ok_or(AdmissionError::NotFound)?;
        decode(&value)
    }

    /// Compute a stable SHA-256 digest for a serializable request payload (§4.1–§4.3).
    pub fn request_digest<T: Serialize>(request: &T) -> Result<String, AdmissionError> {
        let bytes = serde_json::to_vec(request)?;
        Ok(format!("{:x}", Sha256::digest(bytes)))
    }

    /// Insert one immutable `canonical_commits` row and return the reference that
    /// names it (`D-OWNER-DECISION-CANONICAL-COMMIT-001` §3).
    ///
    /// The row is written before the reference escapes, in a single transaction
    /// with `synchronous=FULL`, so a returned reference always names a committed
    /// row. A byte-identical replay is idempotent; the same `commit_id` with any
    /// differing field is an integrity conflict. There is no update or delete.
    ///
    /// Dev baseline only: `signature` is the empty string (see §7). This is the
    /// issuer's write path, not the compiler's; the publication authority never
    /// calls it.
    pub fn issue_canonical_commit(
        &mut self,
        commit_id: &OpaqueId,
        issuer: &IssuerId,
        subject_digest: &OpaqueId,
        issued_at: &str,
    ) -> Result<CanonicalCommitRef, AdmissionError> {
        if issuer.as_str() != DEV_BASELINE_ISSUER {
            return Err(AdmissionError::InvalidInput(
                "issuer is not on the dev-baseline allowlist",
            ));
        }
        if !is_sha256_hex(subject_digest.as_str()) || !is_rfc3339_utc(issued_at) {
            return Err(AdmissionError::InvalidInput(
                "subject digest or issued_at is not in canonical form",
            ));
        }
        let data = CanonicalCommitData {
            commit_id: commit_id.clone(),
            issuer: issuer.clone(),
            subject_digest: subject_digest.clone(),
            issued_at: issued_at.to_owned(),
        };
        let reference = CanonicalCommitRef::from_issued_data(data)
            .map_err(|_| AdmissionError::InvalidInput("canonical commit fields"))?;

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;
        let inserted = tx.execute(
            "INSERT INTO canonical_commits(commit_id,issuer_id,subject_digest,issued_at,signature)
             VALUES(?1,?2,?3,?4,'')",
            params![
                commit_id.as_str(),
                issuer.as_str(),
                subject_digest.as_str(),
                issued_at
            ],
        );
        match inserted {
            Ok(_) => {}
            Err(rusqlite::Error::SqliteFailure(ref code, _))
                if code.code == rusqlite::ErrorCode::ConstraintViolation =>
            {
                // A duplicate primary key is either an idempotent replay or an
                // integrity conflict; only byte-identical fields are a replay.
                let stored = read_canonical_commit(&tx, commit_id)?;
                let identical = stored.issuer_id == issuer.as_str()
                    && stored.subject_digest == subject_digest.as_str()
                    && stored.issued_at == issued_at;
                if !identical {
                    return Err(AdmissionError::IdempotencyConflict);
                }
            }
            Err(error) => return Err(AdmissionError::Sqlite(error)),
        }
        tx.commit()?;
        Ok(reference)
    }

    /// Record-backed, three-outcome canonical commit validation (§4).
    ///
    /// `Ok(true)` — issued reference, cursor equal to its `commit_id`, a readable
    /// row whose commit id, issuer, digest and timestamp match the reference, an
    /// allowlisted issuer, and a stored digest equal to
    /// `expected_subject_digest`.
    ///
    /// `Ok(false)` — the row exists and is readable and every reference field
    /// matches it, but the stored subject digest differs from the expected one.
    ///
    /// `Err(..)` — everything else, including a missing row. A missing record is
    /// never `Ok(false)`: authority failures stay errors
    /// (`memory-compiler/src/lib.rs`, publication gate contract).
    pub fn validate_canonical_commit(
        &self,
        cursor: &OpaqueId,
        reference: &CanonicalCommitRef,
        expected_subject_digest: &OpaqueId,
    ) -> Result<bool, CanonicalCommitValidationError> {
        let data = reference
            .data()
            .ok_or(CanonicalCommitValidationError::PendingReference)?;
        if cursor != &data.commit_id {
            return Err(CanonicalCommitValidationError::CursorMismatch);
        }

        let stored =
            read_canonical_commit(&self.connection, &data.commit_id).map_err(
                |error| match error {
                    rusqlite::Error::QueryReturnedNoRows => {
                        CanonicalCommitValidationError::RecordMissing
                    }
                    _ => CanonicalCommitValidationError::ReadFailed,
                },
            )?;

        // Shape first: a corrupt row is malformed whatever the reference repeats,
        // and a non-allowlisted issuer is never trustworthy. `from_issued_data`
        // pins the reference's issuer to the allowlist, so this also covers an
        // issuer disagreement.
        if stored.issuer_id != DEV_BASELINE_ISSUER {
            return Err(CanonicalCommitValidationError::UnsupportedIssuer);
        }
        if !is_sha256_hex(&stored.subject_digest) || !is_rfc3339_utc(&stored.issued_at) {
            return Err(CanonicalCommitValidationError::RecordMalformed);
        }
        if stored.subject_digest != data.subject_digest.as_str() {
            return Err(CanonicalCommitValidationError::RecordMismatch(
                "subject_digest",
            ));
        }
        if stored.issued_at != data.issued_at {
            return Err(CanonicalCommitValidationError::RecordMismatch("issued_at"));
        }

        Ok(stored.subject_digest == expected_subject_digest.as_str())
    }

    /// Insert one immutable authorization decision and return its
    /// content-bearing reference.
    ///
    /// The durable row is committed before the reference escapes.
    /// Byte-identical replay is idempotent; conflicting reuse of the
    /// decision ID is rejected.
    ///
    /// Dev baseline only: signature is the empty string.
    pub fn issue_authorization_decision(
        &mut self,
        decision_id: &OpaqueId,
        issuer: &IssuerId,
        subject_digest: &OpaqueId,
        issued_at: &str,
        decision_kind: AuthorizationDecisionKind,
    ) -> Result<AuthorizationDecisionRef, AdmissionError> {
        if issuer.as_str() != I_DEV_BASELINE_ISSUER {
            return Err(AdmissionError::InvalidInput(
                "issuer is not on the I dev-baseline allowlist",
            ));
        }

        if !is_sha256_hex(subject_digest.as_str()) || !is_rfc3339_utc(issued_at) {
            return Err(AdmissionError::InvalidInput(
                "subject digest or issued_at is not in canonical form",
            ));
        }

        let data = AuthorizationDecisionData {
            decision_id: decision_id.clone(),
            issuer: issuer.clone(),
            subject_digest: subject_digest.clone(),
            issued_at: issued_at.to_owned(),
            decision_kind,
        };

        let reference = AuthorizationDecisionRef::from_issued_data(data)
            .map_err(|_| AdmissionError::InvalidInput("authorization decision fields"))?;

        let kind = authorization_decision_kind_str(decision_kind);

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;

        let inserted = tx.execute(
            "INSERT INTO authorization_decisions(
                decision_id,issuer_id,subject_digest,issued_at,decision_kind,signature
             )
             VALUES(?1,?2,?3,?4,?5,'')",
            params![
                decision_id.as_str(),
                issuer.as_str(),
                subject_digest.as_str(),
                issued_at,
                kind,
            ],
        );

        match inserted {
            Ok(_) => {}
            Err(rusqlite::Error::SqliteFailure(ref code, _))
                if code.code == rusqlite::ErrorCode::ConstraintViolation =>
            {
                let stored = read_authorization_decision(&tx, decision_id)?;

                let identical = stored.issuer_id == issuer.as_str()
                    && stored.subject_digest == subject_digest.as_str()
                    && stored.issued_at == issued_at
                    && stored.decision_kind == kind;

                if !identical {
                    return Err(AdmissionError::IdempotencyConflict);
                }
            }
            Err(error) => return Err(AdmissionError::Sqlite(error)),
        }

        tx.commit()?;
        Ok(reference)
    }

    /// Record-backed authorization decision validation.
    ///
    /// Ok(true): all reference fields match the readable durable record,
    /// the issuer is allowlisted, and the digest matches the expected digest.
    ///
    /// Ok(false): all reference fields match the readable durable record,
    /// but the stored digest differs from the expected digest.
    ///
    /// Err(..): every other case, including a missing or unreadable row.
    ///
    /// Decision kind is deliberately not an authorization policy check.
    /// A valid Denied or Conditional decision is still a valid recorded
    /// decision.
    pub fn validate_authorization_decision(
        &self,
        reference: &AuthorizationDecisionRef,
        expected_subject_digest: &OpaqueId,
    ) -> Result<bool, AuthorizationDecisionValidationError> {
        let data = reference
            .data()
            .ok_or(AuthorizationDecisionValidationError::PendingReference)?;

        let stored =
            read_authorization_decision(&self.connection, &data.decision_id).map_err(|error| {
                match error {
                    rusqlite::Error::QueryReturnedNoRows => {
                        AuthorizationDecisionValidationError::RecordMissing
                    }
                    _ => AuthorizationDecisionValidationError::ReadFailed,
                }
            })?;

        let stored_kind = validate_stored_authorization_decision(&stored)?;

        if stored.issuer_id != data.issuer.as_str() {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "issuer",
            ));
        }

        if stored.subject_digest != data.subject_digest.as_str() {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "subject_digest",
            ));
        }

        if stored.issued_at != data.issued_at {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "issued_at",
            ));
        }

        if stored_kind != data.decision_kind {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "decision_kind",
            ));
        }

        Ok(stored.subject_digest == expected_subject_digest.as_str())
    }

    /// Read the recorded decision kind.
    ///
    /// This is a record-reading operation, not an authorization check: it does
    /// not decide whether the kind permits a transition, and Denied and
    /// Conditional are valid stored kinds. It does verify that the durable row
    /// is the one this reference names, so a caller cannot read a kind that is
    /// not backed by the reference it holds.
    pub fn authorization_decision_kind(
        &self,
        reference: &AuthorizationDecisionRef,
    ) -> Result<AuthorizationDecisionKind, AuthorizationDecisionValidationError> {
        let data = reference
            .data()
            .ok_or(AuthorizationDecisionValidationError::PendingReference)?;

        let stored =
            read_authorization_decision(&self.connection, &data.decision_id).map_err(|error| {
                match error {
                    rusqlite::Error::QueryReturnedNoRows => {
                        AuthorizationDecisionValidationError::RecordMissing
                    }
                    _ => AuthorizationDecisionValidationError::ReadFailed,
                }
            })?;

        let stored_kind = validate_stored_authorization_decision(&stored)?;

        if stored.issuer_id != data.issuer.as_str() {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "issuer",
            ));
        }

        if stored.subject_digest != data.subject_digest.as_str() {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "subject_digest",
            ));
        }

        if stored.issued_at != data.issued_at {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "issued_at",
            ));
        }

        if stored_kind != data.decision_kind {
            return Err(AuthorizationDecisionValidationError::RecordMismatch(
                "decision_kind",
            ));
        }

        Ok(stored_kind)
    }

    /// Insert one immutable attestation record and return its content-bearing
    /// reference.
    ///
    /// A duplicate ID is idempotent only when every stored column is identical.
    /// The reference escapes only after the transaction commits.
    ///
    /// Dev baseline only: the signature is the empty string.
    pub fn issue_attestation(
        &mut self,
        attestation_id: &OpaqueId,
        issuer: &IssuerId,
        subject_digest: &OpaqueId,
        issued_at: &str,
    ) -> Result<AttestorRef, AdmissionError> {
        if issuer.as_str() != I_DEV_BASELINE_ISSUER {
            return Err(AdmissionError::InvalidInput(
                "attestor issuer is not on the I dev-baseline allowlist",
            ));
        }

        if !is_sha256_hex(subject_digest.as_str()) || !is_rfc3339_utc(issued_at) {
            return Err(AdmissionError::InvalidInput(
                "attestor subject digest or issued_at is not in canonical form",
            ));
        }

        let reference = AttestorRef::from_issued_data(AttestorData {
            attestation_id: attestation_id.clone(),
            issuer: issuer.clone(),
            subject_digest: subject_digest.clone(),
            issued_at: issued_at.to_owned(),
        })
        .map_err(|_| AdmissionError::InvalidInput("attestor fields"))?;

        let tx = self
            .connection
            .transaction_with_behavior(TransactionBehavior::Immediate)?;

        let inserted = tx.execute(
            "INSERT INTO i_attestations(
                attestation_id,issuer_id,subject_digest,issued_at,signature
             )
             VALUES(?1,?2,?3,?4,'')",
            params![
                attestation_id.as_str(),
                issuer.as_str(),
                subject_digest.as_str(),
                issued_at,
            ],
        );

        match inserted {
            Ok(_) => {}
            Err(rusqlite::Error::SqliteFailure(ref code, _))
                if code.code == rusqlite::ErrorCode::ConstraintViolation =>
            {
                let stored = read_attestation(&tx, attestation_id)?;
                let identical = stored.issuer_id == issuer.as_str()
                    && stored.subject_digest == subject_digest.as_str()
                    && stored.issued_at == issued_at
                    && stored.signature.is_empty();

                if !identical {
                    return Err(AdmissionError::IdempotencyConflict);
                }
            }
            Err(error) => return Err(AdmissionError::Sqlite(error)),
        }

        tx.commit()?;
        Ok(reference)
    }

    /// Validate an issued attestor against its durable row and the expected
    /// subject digest.
    ///
    /// A subject mismatch is an authority error, never a successful validation:
    /// unlike an authorization decision, an attestation has no boolean
    /// disposition to return.
    pub fn validate_attestor(
        &self,
        reference: &AttestorRef,
        expected_subject_digest: &OpaqueId,
    ) -> Result<(), AttestorValidationError> {
        let data = reference
            .data()
            .ok_or(AttestorValidationError::PendingReference)?;

        let stored =
            read_attestation(&self.connection, &data.attestation_id).map_err(
                |error| match error {
                    rusqlite::Error::QueryReturnedNoRows => AttestorValidationError::RecordMissing,
                    _ => AttestorValidationError::ReadFailed,
                },
            )?;

        // Authority first, then stored-row shape, then reference equality.
        if stored.issuer_id != I_DEV_BASELINE_ISSUER {
            return Err(AttestorValidationError::UnsupportedIssuer);
        }

        if !is_sha256_hex(&stored.subject_digest)
            || !is_rfc3339_utc(&stored.issued_at)
            || !stored.signature.is_empty()
        {
            return Err(AttestorValidationError::RecordMalformed);
        }

        if stored.issuer_id != data.issuer.as_str() {
            return Err(AttestorValidationError::RecordMismatch("issuer"));
        }

        if stored.subject_digest != data.subject_digest.as_str() {
            return Err(AttestorValidationError::RecordMismatch("subject_digest"));
        }

        if stored.issued_at != data.issued_at {
            return Err(AttestorValidationError::RecordMismatch("issued_at"));
        }

        if stored.subject_digest != expected_subject_digest.as_str() {
            return Err(AttestorValidationError::RecordMismatch(
                "expected_subject_digest",
            ));
        }

        Ok(())
    }
}

/// One decoded authorization_decisions row.
struct StoredAuthorizationDecision {
    issuer_id: String,
    subject_digest: String,
    issued_at: String,
    decision_kind: String,
}

/// Reads an authorization decision by primary key.
///
/// QueryReturnedNoRows is preserved so the caller can distinguish
/// a missing record from an unreadable database.
fn read_authorization_decision(
    connection: &Connection,
    decision_id: &OpaqueId,
) -> Result<StoredAuthorizationDecision, rusqlite::Error> {
    connection.query_row(
        "SELECT issuer_id,subject_digest,issued_at,decision_kind
         FROM authorization_decisions
         WHERE decision_id=?1",
        [decision_id.as_str()],
        |row| {
            Ok(StoredAuthorizationDecision {
                issuer_id: row.get(0)?,
                subject_digest: row.get(1)?,
                issued_at: row.get(2)?,
                decision_kind: row.get(3)?,
            })
        },
    )
}

/// Checks a stored authorization decision row for authority and shape, then
/// decodes its kind.
///
/// Shared by the reference validator and the kind accessor so both reject the
/// same rows. Authority is checked before shape: an untrusted issuer is reported
/// as such even if its row is also malformed.
fn validate_stored_authorization_decision(
    stored: &StoredAuthorizationDecision,
) -> Result<AuthorizationDecisionKind, AuthorizationDecisionValidationError> {
    if stored.issuer_id != I_DEV_BASELINE_ISSUER {
        return Err(AuthorizationDecisionValidationError::UnsupportedIssuer);
    }

    if !is_sha256_hex(&stored.subject_digest)
        || !is_rfc3339_utc(&stored.issued_at)
        || !matches!(
            stored.decision_kind.as_str(),
            "Approved" | "Denied" | "Conditional"
        )
    {
        return Err(AuthorizationDecisionValidationError::RecordMalformed);
    }

    parse_authorization_decision_kind(&stored.decision_kind)
        .ok_or(AuthorizationDecisionValidationError::RecordMalformed)
}

/// One decoded i_attestations row.
struct StoredAttestation {
    issuer_id: String,
    subject_digest: String,
    issued_at: String,
    signature: String,
}

/// Reads an attestation by primary key.
///
/// QueryReturnedNoRows is preserved so the caller can distinguish
/// a missing record from an unreadable database.
fn read_attestation(
    connection: &Connection,
    attestation_id: &OpaqueId,
) -> Result<StoredAttestation, rusqlite::Error> {
    connection.query_row(
        "SELECT issuer_id,subject_digest,issued_at,signature
         FROM i_attestations
         WHERE attestation_id=?1",
        [attestation_id.as_str()],
        |row| {
            Ok(StoredAttestation {
                issuer_id: row.get(0)?,
                subject_digest: row.get(1)?,
                issued_at: row.get(2)?,
                signature: row.get(3)?,
            })
        },
    )
}

fn authorization_decision_kind_str(kind: AuthorizationDecisionKind) -> &'static str {
    match kind {
        AuthorizationDecisionKind::Approved => "Approved",
        AuthorizationDecisionKind::Denied => "Denied",
        AuthorizationDecisionKind::Conditional => "Conditional",
    }
}

fn parse_authorization_decision_kind(value: &str) -> Option<AuthorizationDecisionKind> {
    match value {
        "Approved" => Some(AuthorizationDecisionKind::Approved),
        "Denied" => Some(AuthorizationDecisionKind::Denied),
        "Conditional" => Some(AuthorizationDecisionKind::Conditional),
        _ => None,
    }
}
/// One decoded `canonical_commits` row.
struct StoredCanonicalCommit {
    issuer_id: String,
    subject_digest: String,
    issued_at: String,
}

/// Reads a row by primary key. `QueryReturnedNoRows` is preserved so the caller
/// can distinguish a missing record from an unreadable one.
fn read_canonical_commit(
    connection: &Connection,
    commit_id: &OpaqueId,
) -> Result<StoredCanonicalCommit, rusqlite::Error> {
    connection.query_row(
        "SELECT issuer_id,subject_digest,issued_at FROM canonical_commits WHERE commit_id=?1",
        [commit_id.as_str()],
        |row| {
            Ok(StoredCanonicalCommit {
                issuer_id: row.get(0)?,
                subject_digest: row.get(1)?,
                issued_at: row.get(2)?,
            })
        },
    )
}

fn read_meta(tx: &Transaction<'_>) -> Result<FenceInstallReceipt, AdmissionError> {
    tx.query_row(
        "SELECT fence_generation,protocol_sequence FROM admission_meta WHERE singleton=1",
        [],
        |row| {
            Ok(FenceInstallReceipt {
                fence_generation: row.get::<_, i64>(0)? as u64,
                protocol_sequence: row.get::<_, i64>(1)? as u64,
            })
        },
    )
    .map_err(AdmissionError::from)
}

fn encode<T: Serialize>(value: &T) -> Result<String, AdmissionError> {
    Ok(serde_json::to_string(value)?)
}

/// §6 migration: a persisted request written before the reference existed
/// decodes as the legacy pending marker, which never validates.
fn pending_canonical_commit_ref() -> CanonicalCommitRef {
    CanonicalCommitRef::pending_d()
}
fn decode<T: DeserializeOwned>(value: &str) -> Result<T, AdmissionError> {
    Ok(serde_json::from_str(value)?)
}

fn validate_producer_request(r: &ProducerRegistrationRequest) -> Result<(), AdmissionError> {
    if r.producer_class.trim().is_empty()
        || r.producer_identity.as_str().trim().is_empty()
        || r.source_refs.is_empty()
        || r.source_lineage_digest.trim().is_empty()
        || r.scope_refs.is_empty()
        || r.scope_refs.iter().any(|s| s.validate().is_err())
        || r.request_digest.trim().is_empty()
        || r.producer_schema_version.trim().is_empty()
    {
        return Err(AdmissionError::InvalidInput(
            "producer registration required fields",
        ));
    }
    Ok(())
}
fn validate_dependency_request(r: &DependencyRegistrationRequest) -> Result<(), AdmissionError> {
    if r.lineage_digest.trim().is_empty()
        || r.request_digest.trim().is_empty()
        || r.required_dependency_count == 0
        || r.scope_refs.is_empty()
        || r.scope_refs.iter().any(|s| s.validate().is_err())
    {
        return Err(AdmissionError::InvalidInput(
            "dependency registration required fields",
        ));
    }
    Ok(())
}
fn validate_publication_request(r: &PublicationGateRequest) -> Result<(), AdmissionError> {
    if r.dependency_receipt_ids.is_empty()
        || r.request_digest.trim().is_empty()
        || r.scope_refs.is_empty()
        || r.scope_refs.iter().any(|s| s.validate().is_err())
    {
        return Err(AdmissionError::InvalidInput(
            "publication gate required fields",
        ));
    }
    Ok(())
}

/// Current UTC wall-clock timestamp helper retained for future durable evidence (§4.1–§4.3).
pub fn timestamp_unix_nanos() -> u128 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos()
}

/// The dev-baseline issuer's clock, formatted as RFC 3339 UTC.
///
/// Validation checks syntax and equality only; it never decides freshness, so a
/// small civil-date conversion is enough and no time-zone database is involved.
pub fn rfc3339_utc_now() -> String {
    let seconds = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    let days = (seconds / 86_400) as i64;
    let of_day = seconds % 86_400;
    // Howard Hinnant's civil_from_days: shift the epoch to 0000-03-01.
    let z = days + 719_468;
    let era = z.div_euclid(146_097);
    let doe = z.rem_euclid(146_097);
    let yoe = (doe - doe / 1460 + doe / 36_524 - doe / 146_096) / 365;
    let doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    let mp = (5 * doy + 2) / 153;
    let day = doy - (153 * mp + 2) / 5 + 1;
    let month = if mp < 10 { mp + 3 } else { mp - 9 };
    let year = yoe + era * 400 + i64::from(month <= 2);
    format!(
        "{year:04}-{month:02}-{day:02}T{:02}:{:02}:{:02}Z",
        of_day / 3600,
        (of_day % 3600) / 60,
        of_day % 60
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::ScopeKind;
    use std::sync::{Arc, Barrier};
    use std::thread;

    fn id(s: &str) -> OpaqueId {
        OpaqueId::new(s).unwrap()
    }
    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("scope-1"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-1".into(),
        }
    }
    fn register_work(
        db: &mut AdmissionStore,
        request: ProducerRegistrationRequest,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        let producer_id = request.producer_identity.clone();
        if !db.is_producer_registered(&producer_id)? {
            db.register_producer(&producer_id, "test-registry-digest")?;
        }
        db.register_producer_work(request)
    }

    fn producer() -> ProducerRegistrationRequest {
        ProducerRegistrationRequest {
            producer_work_item_id: id("work-1"),
            producer_class: "compiler".into(),
            producer_identity: id("producer-identity"),
            source_refs: vec![id("event-1")],
            source_lineage_digest: "lineage-1".into(),
            scope_refs: vec![scope()],
            operation_id: id("operation-1"),
            correlation_id: id("correlation-1"),
            causation_id: Some(id("cause-1")),
            admission_canonical_commit_cursor: None,
            canonical_commit_ref: CanonicalCommitRef::pending_d(),
            observed_fence_cursor: id("fence-observation-0"),
            permission_epoch: id("permission-epoch-1"),
            request_digest: "request-digest-1".into(),
            producer_schema_version: "v1".into(),
        }
    }
    fn dependency(edge: &str, source: &str) -> DependencyRegistrationRequest {
        DependencyRegistrationRequest {
            dependency_registration_id: id(edge),
            artifact_ref: id("artifact-1"),
            artifact_version: id("artifact-version-1"),
            producer_work_item_id: id("work-1"),
            derivation_run_id: id("run-1"),
            source_ref: id(source),
            source_version: None,
            provenance_ref: id("provenance-1"),
            scope_refs: vec![scope()],
            lineage_digest: "lineage-1".into(),
            required_dependency_count: 2,
            request_digest: format!("digest-{edge}"),
        }
    }
    fn gate(observation: FenceInstallReceipt, receipts: Vec<OpaqueId>) -> PublicationGateRequest {
        PublicationGateRequest {
            publication_operation_id: id("publication-op-1"),
            artifact_ref: id("artifact-1"),
            artifact_version: id("artifact-version-1"),
            producer_work_item_id: id("work-1"),
            derivation_run_id: id("run-1"),
            attempt_id: id("attempt-1"),
            lease_id: id("lease-1"),
            dependency_receipt_ids: receipts,
            permission_epoch: id("permission-epoch-2"),
            observed_fence_generation: observation.fence_generation,
            observed_protocol_sequence: observation.protocol_sequence,
            scope_refs: vec![scope()],
            request_digest: "publication-digest-1".into(),
        }
    }

    #[test]
    fn producer_work_rejects_unregistered_producer_as_configuration_error() {
        let mut db = AdmissionStore::in_memory().unwrap();
        let request = producer();
        let producer_id = request.producer_identity.clone();
        assert!(matches!(
            db.register_producer_work(request),
            Err(AdmissionError::ProducerNotRegistered { producer_id: found })
                if found == producer_id.as_str()
        ));
        assert_eq!(db.producer_ledger_count().unwrap(), 0);
    }

    #[test]
    fn producer_registry_rejects_duplicate_registration() {
        let mut db = AdmissionStore::in_memory().unwrap();
        let producer_id = id("producer-identity");
        db.register_producer(&producer_id, "registry-digest-1")
            .unwrap();
        assert!(matches!(
            db.register_producer(&producer_id, "registry-digest-1"),
            Err(AdmissionError::ProducerAlreadyRegistered)
        ));
    }

    #[test]
    fn one_registered_producer_can_admit_multiple_distinct_work_items() {
        let mut db = AdmissionStore::in_memory().unwrap();
        let producer_id = id("producer-identity");
        db.register_producer(&producer_id, "registry-digest-1")
            .unwrap();

        let first = db.register_producer_work(producer()).unwrap();
        let mut second_request = producer();
        second_request.producer_work_item_id = id("work-2");
        second_request.request_digest = "request-digest-2".into();
        let second = db.register_producer_work(second_request).unwrap();

        assert_ne!(first.producer_work_item_id, second.producer_work_item_id);
        assert_eq!(db.producer_ledger_count().unwrap(), 2);
    }

    #[test]
    fn producer_registration_is_idempotent_and_conflicting_digest_does_not_add_rows() {
        let mut db = AdmissionStore::in_memory().unwrap();
        let first = register_work(&mut db, producer()).unwrap();
        let retry = register_work(&mut db, producer()).unwrap();
        assert_eq!(first.receipt_id, retry.receipt_id);
        assert_eq!(db.producer_ledger_count().unwrap(), 1);
        let mut conflict = producer();
        conflict.request_digest = "different-digest".into();
        assert!(matches!(
            register_work(&mut db, conflict),
            Err(AdmissionError::IdempotencyConflict)
        ));
        assert_eq!(db.producer_ledger_count().unwrap(), 1);
    }

    #[test]
    fn producer_receipt_lookup_and_not_found_are_distinct() {
        let mut db = AdmissionStore::in_memory().unwrap();
        let receipt = register_work(&mut db, producer()).unwrap();
        assert_eq!(db.producer_receipt(&id("work-1")).unwrap(), receipt);
        assert!(matches!(
            db.producer_receipt(&id("missing")),
            Err(AdmissionError::NotFound)
        ));
    }

    #[test]
    fn partial_dependencies_remain_hidden_until_all_edges_are_registered() {
        let mut db = AdmissionStore::in_memory().unwrap();
        register_work(&mut db, producer()).unwrap();
        let first = db
            .register_dependency(dependency("dep-1", "source-1"))
            .unwrap();
        let replay = db
            .register_dependency(dependency("dep-1", "source-1"))
            .unwrap();
        assert_eq!(first.receipt_id, replay.receipt_id);
        assert_eq!(db.dependency_ledger_count().unwrap(), 1);
        let mut conflict = dependency("dep-1", "source-1");
        conflict.request_digest = "changed-digest".into();
        assert!(matches!(
            db.register_dependency(conflict),
            Err(AdmissionError::IdempotencyConflict)
        ));
        assert_eq!(db.dependency_ledger_count().unwrap(), 1);
        assert!(!db
            .is_artifact_visible(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
        assert!(!db
            .dependencies_complete(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
        let obs = db.observe_fence().unwrap();
        assert!(matches!(
            db.final_publication_gate(gate(obs, vec![first.receipt_id.clone()])),
            Err(AdmissionError::DependencySetIncomplete)
        ));
        let second = db
            .register_dependency(dependency("dep-2", "source-2"))
            .unwrap();
        assert!(db
            .dependencies_complete(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
        assert!(!db
            .is_artifact_visible(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
        assert!(db
            .final_publication_gate(gate(obs, vec![first.receipt_id, second.receipt_id]))
            .is_ok());
        assert!(db
            .is_artifact_visible(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
    }

    #[test]
    fn final_gate_receipt_binds_observed_fence_and_permission_epoch() {
        let mut db = AdmissionStore::in_memory().unwrap();
        register_work(&mut db, producer()).unwrap();
        let first = db
            .register_dependency(dependency("dep-1", "source-1"))
            .unwrap();
        let second = db
            .register_dependency(dependency("dep-2", "source-2"))
            .unwrap();
        let observed = db.observe_fence().unwrap();
        let request = gate(observed, vec![first.receipt_id, second.receipt_id]);
        let receipt = db.final_publication_gate(request.clone()).unwrap();
        assert_eq!(db.final_publication_gate(request).unwrap(), receipt);
        assert!(db
            .is_artifact_visible(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
        assert_eq!(receipt.fence_generation, observed.fence_generation);
        assert_eq!(receipt.permission_epoch, id("permission-epoch-2"));
        assert!(receipt.visible);
    }

    #[test]
    fn illegal_transition_accept_to_published_is_rejected() {
        assert!(!AdmissionStore::legal_transition(
            WorkState::Accepted,
            WorkState::Published
        ));
        let mut db = AdmissionStore::in_memory().unwrap();
        register_work(&mut db, producer()).unwrap();
        assert!(matches!(
            db.transition_work_state(&id("work-1"), WorkState::Published),
            Err(AdmissionError::InvalidTransition {
                from: WorkState::Accepted,
                to: WorkState::Published
            })
        ));
    }

    #[test]
    fn alternative_exit_transitions_are_accepted_and_persisted() {
        // Each case starts from a fresh registered work item, follows the legal
        // path to the source state, then verifies both acceptance and durable state.
        let cases: [(&[WorkState], WorkState, WorkState); 5] = [
            (&[], WorkState::Accepted, WorkState::Cancelled),
            (&[], WorkState::Accepted, WorkState::SuppressedQuarantined),
            (
                &[
                    WorkState::DRegistrationPending,
                    WorkState::Registered,
                    WorkState::Queued,
                ],
                WorkState::Queued,
                WorkState::SuppressedQuarantined,
            ),
            (
                &[
                    WorkState::DRegistrationPending,
                    WorkState::Registered,
                    WorkState::Queued,
                    WorkState::Leased,
                ],
                WorkState::Leased,
                WorkState::SuppressedQuarantined,
            ),
            (
                &[
                    WorkState::DRegistrationPending,
                    WorkState::Registered,
                    WorkState::Queued,
                    WorkState::Leased,
                    WorkState::Running,
                    WorkState::CandidatePrivate,
                    WorkState::StagedPrivate,
                    WorkState::DependencyRegistrationPending,
                ],
                WorkState::DependencyRegistrationPending,
                WorkState::RetryQueued,
            ),
        ];

        for (index, (path, expected_from, target)) in cases.into_iter().enumerate() {
            let mut db = AdmissionStore::in_memory().unwrap();
            let mut request = producer();
            request.producer_work_item_id = id(&format!("work-alt-exit-{index}"));
            request.request_digest = format!("request-alt-exit-{index}");
            register_work(&mut db, request).unwrap();

            for state in path {
                db.transition_work_state(&id(&format!("work-alt-exit-{index}")), *state)
                    .unwrap();
            }
            let work_item_id = id(&format!("work-alt-exit-{index}"));
            let before_json: String = db
                .connection
                .query_row(
                    "SELECT state_json FROM producer_work WHERE work_item_id=?1",
                    [work_item_id.as_str()],
                    |row| row.get(0),
                )
                .unwrap();
            assert_eq!(decode::<WorkState>(&before_json).unwrap(), expected_from);

            db.transition_work_state(&work_item_id, target).unwrap();

            let after_json: String = db
                .connection
                .query_row(
                    "SELECT state_json FROM producer_work WHERE work_item_id=?1",
                    [work_item_id.as_str()],
                    |row| row.get(0),
                )
                .unwrap();
            assert_eq!(decode::<WorkState>(&after_json).unwrap(), target);
        }
    }

    #[test]
    fn gate_reports_stale_protocol_when_fence_generation_matches() {
        let mut db = AdmissionStore::in_memory().unwrap();
        register_work(&mut db, producer()).unwrap();
        let first = db
            .register_dependency(dependency("dep-1", "source-1"))
            .unwrap();
        let second = db
            .register_dependency(dependency("dep-2", "source-2"))
            .unwrap();

        let observed = db.observe_fence().unwrap();
        let installed = db.install_fence(observed.protocol_sequence).unwrap();
        assert_eq!(installed.fence_generation, observed.fence_generation + 1);
        assert_eq!(installed.protocol_sequence, observed.protocol_sequence + 1);

        let mut request = gate(observed, vec![first.receipt_id, second.receipt_id]);
        request.observed_fence_generation = installed.fence_generation;
        // Keep the old protocol sequence while observing the new fence generation:
        // fence validation passes, then protocol-sequence validation must fail.
        assert!(matches!(
            db.final_publication_gate(request),
            Err(AdmissionError::StaleProtocol {
                expected,
                actual
            }) if expected == observed.protocol_sequence
                && actual == installed.protocol_sequence
        ));
    }

    #[test]
    fn fence_and_gate_compete_on_one_protocol_sequence_exactly_one_wins() {
        let path =
            std::env::temp_dir().join(format!("admission-race-{}.sqlite", std::process::id()));
        let _ = std::fs::remove_file(&path);
        let mut setup = AdmissionStore::open(&path).unwrap();
        register_work(&mut setup, producer()).unwrap();
        let first = setup
            .register_dependency(dependency("dep-1", "source-1"))
            .unwrap();
        let second = setup
            .register_dependency(dependency("dep-2", "source-2"))
            .unwrap();
        let observed = setup.observe_fence().unwrap();
        drop(setup);

        let barrier = Arc::new(Barrier::new(3));
        let gate_barrier = barrier.clone();
        let gate_path = path.clone();
        let gate_receipts = vec![first.receipt_id, second.receipt_id];
        let gate_thread = thread::spawn(move || {
            let mut db = AdmissionStore::open(&gate_path).unwrap();
            gate_barrier.wait();
            db.final_publication_gate(gate(observed, gate_receipts))
        });
        let fence_barrier = barrier.clone();
        let fence_path = path.clone();
        let fence_thread = thread::spawn(move || {
            let mut db = AdmissionStore::open(&fence_path).unwrap();
            fence_barrier.wait();
            db.install_fence(observed.protocol_sequence)
        });
        barrier.wait();
        let gate_result = gate_thread.join().unwrap();
        let fence_result = fence_thread.join().unwrap();
        assert_ne!(
            gate_result.is_ok(),
            fence_result.is_ok(),
            "same observed protocol sequence must have one CAS winner"
        );
        let after = AdmissionStore::open(&path)
            .unwrap()
            .observe_fence()
            .unwrap();
        assert_eq!(after.protocol_sequence, observed.protocol_sequence + 1);
        if let Ok(receipt) = gate_result {
            assert_eq!(receipt.protocol_sequence, observed.protocol_sequence + 1);
            assert_eq!(receipt.fence_generation, observed.fence_generation);
            assert!(matches!(
                fence_result,
                Err(AdmissionError::StaleProtocol { .. })
            ));
        } else {
            assert_eq!(after.fence_generation, observed.fence_generation + 1);
            // Fence installation advances both counters. The gate validates the fence
            // generation first, so a winning fence produces StaleFence; StaleProtocol
            // is possible only when the fence generation is unchanged.
            assert!(
                matches!(
                    &gate_result,
                    Err(AdmissionError::StaleFence { .. })
                        | Err(AdmissionError::StaleProtocol { .. })
                ),
                "unexpected gate race result: {gate_result:?}"
            );
        }
        let _ = std::fs::remove_file(&path);
        let _ = std::fs::remove_file(path.with_extension("sqlite-wal"));
        let _ = std::fs::remove_file(path.with_extension("sqlite-shm"));
    }

    // ---- canonical commit record and validator (§3, §4, §8 criterion 7) ----

    fn issued_store() -> (AdmissionStore, OpaqueId, CanonicalCommitRef, OpaqueId) {
        let mut db = AdmissionStore::in_memory().unwrap();
        let commit_id = id("commit-1");
        let subject = OpaqueId::new("b".repeat(64)).unwrap();
        let reference = db
            .issue_canonical_commit(
                &commit_id,
                &IssuerId::new(DEV_BASELINE_ISSUER).unwrap(),
                &subject,
                "2026-11-22T00:00:00Z",
            )
            .unwrap();
        (db, commit_id, reference, subject)
    }

    #[test]
    fn validator_confirms_a_matching_record() {
        let (db, cursor, reference, subject) = issued_store();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Ok(true)
        );
    }

    #[test]
    fn validator_reports_false_for_a_subject_digest_mismatch() {
        let (db, cursor, reference, _) = issued_store();
        let other = OpaqueId::new("c".repeat(64)).unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &other),
            Ok(false),
            "a readable, matching record with a different subject is a content mismatch"
        );
    }

    #[test]
    fn validator_reports_a_missing_record_as_an_error_not_false() {
        let (db, cursor, reference, subject) = issued_store();
        let absent = id("commit-never-issued");
        let forged = CanonicalCommitRef::from_issued_data(CanonicalCommitData {
            commit_id: absent.clone(),
            issuer: IssuerId::new(DEV_BASELINE_ISSUER).unwrap(),
            subject_digest: subject.clone(),
            issued_at: "2026-11-22T00:00:00Z".into(),
        })
        .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&absent, &forged, &subject),
            Err(CanonicalCommitValidationError::RecordMissing)
        );
        // The issued row still validates; the forged one did not disturb it.
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Ok(true)
        );
    }

    #[test]
    fn validator_rejects_a_pending_reference() {
        let (db, cursor, _, subject) = issued_store();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &CanonicalCommitRef::pending_d(), &subject),
            Err(CanonicalCommitValidationError::PendingReference)
        );
    }

    #[test]
    fn validator_rejects_a_cursor_that_does_not_select_the_reference() {
        let (db, _, reference, subject) = issued_store();
        assert_eq!(
            db.validate_canonical_commit(&id("commit-other"), &reference, &subject),
            Err(CanonicalCommitValidationError::CursorMismatch)
        );
    }

    #[test]
    fn validator_rejects_an_issuer_mismatch_as_an_authority_failure() {
        let (db, cursor, reference, subject) = issued_store();
        db.connection
            .execute(
                "UPDATE canonical_commits SET issuer_id='someone-else' WHERE commit_id=?1",
                [cursor.as_str()],
            )
            .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Err(CanonicalCommitValidationError::UnsupportedIssuer)
        );
    }

    #[test]
    fn issuance_refuses_an_issuer_outside_the_allowlist() {
        let mut db = AdmissionStore::in_memory().unwrap();
        assert!(matches!(
            db.issue_canonical_commit(
                &id("commit-rogue"),
                &IssuerId::new("someone-else").unwrap(),
                &OpaqueId::new("d".repeat(64)).unwrap(),
                "2026-11-22T00:00:00Z"
            ),
            Err(AdmissionError::InvalidInput(_))
        ));
        // Nothing was written.
        assert_eq!(
            db.validate_canonical_commit(
                &id("commit-rogue"),
                &CanonicalCommitRef::pending_d(),
                &OpaqueId::new("d".repeat(64)).unwrap()
            ),
            Err(CanonicalCommitValidationError::PendingReference)
        );
    }

    #[test]
    fn validator_rejects_a_record_that_disagrees_with_the_reference() {
        let (db, cursor, reference, subject) = issued_store();
        db.connection
            .execute(
                "UPDATE canonical_commits SET subject_digest=?2 WHERE commit_id=?1",
                params![cursor.as_str(), "9".repeat(64)],
            )
            .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Err(CanonicalCommitValidationError::RecordMismatch(
                "subject_digest"
            ))
        );

        let (db, cursor, reference, subject) = issued_store();
        db.connection
            .execute(
                "UPDATE canonical_commits SET issued_at='2026-11-23T00:00:00Z' WHERE commit_id=?1",
                [cursor.as_str()],
            )
            .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Err(CanonicalCommitValidationError::RecordMismatch("issued_at"))
        );
    }

    #[test]
    fn validator_rejects_a_malformed_record() {
        let (db, cursor, reference, subject) = issued_store();
        db.connection
            .execute(
                "UPDATE canonical_commits SET subject_digest='not-a-digest' WHERE commit_id=?1",
                [cursor.as_str()],
            )
            .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Err(CanonicalCommitValidationError::RecordMalformed)
        );

        let (db, cursor, reference, subject) = issued_store();
        db.connection
            .execute(
                "UPDATE canonical_commits SET issued_at='yesterday' WHERE commit_id=?1",
                [cursor.as_str()],
            )
            .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Err(CanonicalCommitValidationError::RecordMalformed)
        );
    }

    #[test]
    fn validator_reports_an_unreadable_database_as_an_error() {
        let (db, cursor, reference, subject) = issued_store();
        db.connection
            .execute_batch("DROP TABLE canonical_commits;")
            .unwrap();
        assert_eq!(
            db.validate_canonical_commit(&cursor, &reference, &subject),
            Err(CanonicalCommitValidationError::ReadFailed)
        );
    }

    #[test]
    fn issuance_is_idempotent_only_for_byte_identical_rows() {
        let mut db = AdmissionStore::in_memory().unwrap();
        let commit_id = id("commit-1");
        let issuer = IssuerId::new(DEV_BASELINE_ISSUER).unwrap();
        let subject = OpaqueId::new("e".repeat(64)).unwrap();
        let first = db
            .issue_canonical_commit(&commit_id, &issuer, &subject, "2026-11-22T00:00:00Z")
            .unwrap();
        let replay = db
            .issue_canonical_commit(&commit_id, &issuer, &subject, "2026-11-22T00:00:00Z")
            .unwrap();
        assert_eq!(first, replay);
        assert!(matches!(
            db.issue_canonical_commit(&commit_id, &issuer, &subject, "2026-11-23T00:00:00Z"),
            Err(AdmissionError::IdempotencyConflict)
        ));
    }

    // ---- authorization decision record and validator ----

    fn issued_authorization_store(
        kind: AuthorizationDecisionKind,
    ) -> (AdmissionStore, AuthorizationDecisionRef, OpaqueId) {
        let mut db = AdmissionStore::in_memory().unwrap();

        let decision_id = id("authorization-decision-1");
        let subject = OpaqueId::new("a".repeat(64)).unwrap();

        let reference = db
            .issue_authorization_decision(
                &decision_id,
                &IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap(),
                &subject,
                "2026-11-22T00:00:00Z",
                kind,
            )
            .unwrap();

        (db, reference, subject)
    }

    #[test]
    fn authorization_validator_accepts_approved_decision() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Ok(true)
        );
    }

    #[test]
    fn authorization_validator_accepts_denied_decision() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Denied);

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Ok(true)
        );
    }

    #[test]
    fn authorization_validator_accepts_conditional_decision() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Conditional);

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Ok(true)
        );
    }

    #[test]
    fn authorization_validator_reports_missing_record_as_error() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        let mut data = reference.data().unwrap().clone();
        data.decision_id = id("authorization-decision-never-issued");

        let missing = AuthorizationDecisionRef::from_issued_data(data).unwrap();

        assert_eq!(
            db.validate_authorization_decision(&missing, &subject),
            Err(AuthorizationDecisionValidationError::RecordMissing)
        );
    }

    #[test]
    fn authorization_validator_rejects_unsupported_issuer() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        let decision_id = reference.data().unwrap().decision_id.clone();

        db.connection
            .execute(
                "UPDATE authorization_decisions
                 SET issuer_id='someone-else'
                 WHERE decision_id=?1",
                [decision_id.as_str()],
            )
            .unwrap();

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Err(AuthorizationDecisionValidationError::UnsupportedIssuer)
        );
    }

    #[test]
    fn authorization_validator_rejects_subject_digest_reference_mismatch() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        let decision_id = reference.data().unwrap().decision_id.clone();

        db.connection
            .execute(
                "UPDATE authorization_decisions
                 SET subject_digest=?2
                 WHERE decision_id=?1",
                params![decision_id.as_str(), "9".repeat(64)],
            )
            .unwrap();

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Err(AuthorizationDecisionValidationError::RecordMismatch(
                "subject_digest"
            ))
        );
    }

    #[test]
    fn authorization_validator_rejects_issued_at_reference_mismatch() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        let decision_id = reference.data().unwrap().decision_id.clone();

        db.connection
            .execute(
                "UPDATE authorization_decisions
                 SET issued_at='2026-11-23T00:00:00Z'
                 WHERE decision_id=?1",
                [decision_id.as_str()],
            )
            .unwrap();

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Err(AuthorizationDecisionValidationError::RecordMismatch(
                "issued_at"
            ))
        );
    }

    #[test]
    fn authorization_validator_rejects_decision_kind_reference_mismatch() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        let decision_id = reference.data().unwrap().decision_id.clone();

        db.connection
            .execute(
                "UPDATE authorization_decisions
                 SET decision_kind='Denied'
                 WHERE decision_id=?1",
                [decision_id.as_str()],
            )
            .unwrap();

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Err(AuthorizationDecisionValidationError::RecordMismatch(
                "decision_kind"
            ))
        );
    }

    #[test]
    fn authorization_validator_reports_dropped_table_as_read_failed() {
        let (db, reference, subject) =
            issued_authorization_store(AuthorizationDecisionKind::Approved);

        db.connection
            .execute_batch("DROP TABLE authorization_decisions;")
            .unwrap();

        assert_eq!(
            db.validate_authorization_decision(&reference, &subject),
            Err(AuthorizationDecisionValidationError::ReadFailed)
        );
    }

    #[test]
    fn authorization_decision_kind_returns_denied_without_rejecting_it() {
        let (db, reference, _) = issued_authorization_store(AuthorizationDecisionKind::Denied);

        assert_eq!(
            db.authorization_decision_kind(&reference),
            Ok(AuthorizationDecisionKind::Denied)
        );
    }

    #[test]
    fn authorization_validator_returns_false_only_for_expected_digest_mismatch() {
        let (db, reference, _) = issued_authorization_store(AuthorizationDecisionKind::Approved);

        let other = OpaqueId::new("c".repeat(64)).unwrap();

        assert_eq!(
            db.validate_authorization_decision(&reference, &other),
            Ok(false)
        );
    }

    #[test]
    fn authorization_issuance_is_idempotent_only_for_identical_rows() {
        let mut db = AdmissionStore::in_memory().unwrap();

        let decision_id = id("authorization-decision-replay");
        let issuer = IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap();
        let subject = OpaqueId::new("d".repeat(64)).unwrap();

        let first = db
            .issue_authorization_decision(
                &decision_id,
                &issuer,
                &subject,
                "2026-11-22T00:00:00Z",
                AuthorizationDecisionKind::Approved,
            )
            .unwrap();

        let replay = db
            .issue_authorization_decision(
                &decision_id,
                &issuer,
                &subject,
                "2026-11-22T00:00:00Z",
                AuthorizationDecisionKind::Approved,
            )
            .unwrap();

        assert_eq!(first, replay);

        assert!(matches!(
            db.issue_authorization_decision(
                &decision_id,
                &issuer,
                &subject,
                "2026-11-22T00:00:00Z",
                AuthorizationDecisionKind::Denied,
            ),
            Err(AdmissionError::IdempotencyConflict)
        ));
    }

    #[test]
    fn a_request_row_written_before_the_reference_existed_decodes_as_pending() {
        // §6: the field is additive and defaults to the legacy marker, which
        // never validates. The stored JSON below is the pre-change shape.
        let legacy = r#"{
            "producer_work_item_id":"work-1","producer_class":"compiler",
            "producer_identity":"producer-identity","source_refs":["event-1"],
            "source_lineage_digest":"lineage-1",
            "scope_refs":[{"scope_id":"scope-1","scope_kind":"User","namespace_key":"user:scope-1"}],
            "operation_id":"operation-1","correlation_id":"correlation-1","causation_id":null,
            "admission_canonical_commit_cursor":"cursor-1",
            "observed_fence_cursor":"fence-observation-0","permission_epoch":"permission-epoch-1",
            "request_digest":"request-digest-1","producer_schema_version":"v1"
        }"#;
        let request: ProducerRegistrationRequest = decode(legacy).unwrap();
        assert!(request.canonical_commit_ref.is_pending());
    }
}
