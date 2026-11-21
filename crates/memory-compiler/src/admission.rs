//! Durable producer admission primitives for the Memory Compiler.
//!
//! This module defines the E-side lifecycle and admission-store port, with a
//! pure-Rust in-memory implementation for conformance tests. The optional
//! SQLite adapter is local only, not the D-authoritative ledger or a
//! cross-service D/Storage visibility transaction.

use memory_domain::{OpaqueId, ScopeRef};
#[cfg(feature = "sqlite")]
use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    time::{SystemTime, UNIX_EPOCH},
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
    #[cfg(feature = "sqlite")]
    Sqlite(rusqlite::Error),
    Serialization(serde_json::Error),
    InvalidInput(&'static str),
    InvalidTransition {
        from: WorkState,
        to: WorkState,
    },
    IdempotencyConflict,
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
}

impl std::fmt::Display for AdmissionError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            #[cfg(feature = "sqlite")]
            Self::Sqlite(e) => write!(f, "admission SQLite error: {e}"),
            Self::Serialization(e) => write!(f, "admission serialization error: {e}"),
            Self::InvalidInput(s) => write!(f, "invalid admission input: {s}"),
            Self::InvalidTransition { from, to } => {
                write!(f, "illegal work transition: {from:?} -> {to:?}")
            }
            Self::IdempotencyConflict => {
                write!(f, "idempotency key reused with a different digest")
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
        }
    }
}
impl std::error::Error for AdmissionError {}
#[cfg(feature = "sqlite")]
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
    pub admission_canonical_commit_cursor: Option<OpaqueId>,
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
#[derive(Clone, Copy, Debug, Eq, PartialEq, Default)]
pub struct FenceInstallReceipt {
    pub fence_generation: u64,
    pub protocol_sequence: u64,
}

/// Storage port for producer admission semantics. Implementations own their
/// transaction/serialization strategy; callers depend only on these operations.
pub trait AdmissionStore {
    fn transition_work_state(
        &mut self,
        work_item_id: &OpaqueId,
        next: WorkState,
    ) -> Result<(), AdmissionError>;
    fn register_producer_work(
        &mut self,
        request: ProducerRegistrationRequest,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError>;
    fn producer_receipt(
        &self,
        work_item_id: &OpaqueId,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError>;
    fn producer_ledger_count(&self) -> Result<u64, AdmissionError>;
    fn register_dependency(
        &mut self,
        request: DependencyRegistrationRequest,
    ) -> Result<DependencyRegistrationReceipt, AdmissionError>;
    fn dependencies_complete(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError>;
    fn observe_fence(&self) -> Result<FenceInstallReceipt, AdmissionError>;
    fn install_fence(
        &mut self,
        expected_protocol_sequence: u64,
    ) -> Result<FenceInstallReceipt, AdmissionError>;
    fn final_publication_gate(
        &mut self,
        request: PublicationGateRequest,
    ) -> Result<PublicationReceipt, AdmissionError>;
    fn is_artifact_visible(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError>;
    fn dependency_ledger_count(&self) -> Result<u64, AdmissionError>;
    fn publication_receipt(
        &self,
        operation_id: &OpaqueId,
    ) -> Result<PublicationReceipt, AdmissionError>;
    fn work_state(&self, work_item_id: &OpaqueId) -> Result<WorkState, AdmissionError>;
}

#[cfg(feature = "sqlite")]
pub mod sqlite;
#[cfg(feature = "sqlite")]
pub use sqlite::SqliteAdmissionStore;

/// Pure-Rust store used to exercise admission invariants without SQLite or a C toolchain.
#[derive(Default)]
pub struct MemoryAdmissionStore {
    producers: BTreeMap<String, ProducerRecord>,
    dependencies: BTreeMap<String, DependencyRecord>,
    publications: BTreeMap<String, (String, PublicationReceipt)>,
    fence: FenceInstallReceipt,
}
struct ProducerRecord {
    digest: String,
    receipt: ProducerRegistrationReceipt,
    state: WorkState,
}
struct DependencyRecord {
    request: DependencyRegistrationRequest,
    receipt: DependencyRegistrationReceipt,
}

impl MemoryAdmissionStore {
    pub fn new() -> Self {
        Self::default()
    }
}

impl AdmissionStore for MemoryAdmissionStore {
    fn transition_work_state(
        &mut self,
        work_item_id: &OpaqueId,
        next: WorkState,
    ) -> Result<(), AdmissionError> {
        let record = self
            .producers
            .get_mut(work_item_id.as_str())
            .ok_or(AdmissionError::NotFound)?;
        if !legal_transition(record.state, next) {
            return Err(AdmissionError::InvalidTransition {
                from: record.state,
                to: next,
            });
        }
        record.state = next;
        Ok(())
    }

    fn register_producer_work(
        &mut self,
        request: ProducerRegistrationRequest,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        validate_producer_request(&request)?;
        let key = request.producer_work_item_id.as_str().to_owned();
        if let Some(existing) = self.producers.get(&key) {
            if existing.digest != request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            return Ok(existing.receipt.clone());
        }
        let sequence = self.producers.len() as u64 + 1;
        let receipt = ProducerRegistrationReceipt {
            receipt_id: OpaqueId::new(format!("producer-registration:{sequence}"))
                .map_err(|_| AdmissionError::InvalidInput("receipt id"))?,
            producer_work_item_id: request.producer_work_item_id,
            request_digest: request.request_digest.clone(),
            ledger_sequence: sequence,
            disposition: RegistrationDisposition::Accepted,
        };
        self.producers.insert(
            key,
            ProducerRecord {
                digest: request.request_digest,
                receipt: receipt.clone(),
                state: WorkState::Accepted,
            },
        );
        Ok(receipt)
    }

    fn producer_receipt(
        &self,
        work_item_id: &OpaqueId,
    ) -> Result<ProducerRegistrationReceipt, AdmissionError> {
        self.producers
            .get(work_item_id.as_str())
            .map(|r| r.receipt.clone())
            .ok_or(AdmissionError::NotFound)
    }

    fn producer_ledger_count(&self) -> Result<u64, AdmissionError> {
        Ok(self.producers.len() as u64)
    }

    fn register_dependency(
        &mut self,
        request: DependencyRegistrationRequest,
    ) -> Result<DependencyRegistrationReceipt, AdmissionError> {
        validate_dependency_request(&request)?;
        let key = request.dependency_registration_id.as_str().to_owned();
        if let Some(existing) = self.dependencies.get(&key) {
            if existing.request.request_digest != request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            return Ok(existing.receipt.clone());
        }
        if !self
            .producers
            .contains_key(request.producer_work_item_id.as_str())
        {
            return Err(AdmissionError::NotFound);
        }
        let receipt = DependencyRegistrationReceipt {
            receipt_id: OpaqueId::new(format!(
                "dependency-registration:{}",
                request.dependency_registration_id.as_str()
            ))
            .map_err(|_| AdmissionError::InvalidInput("dependency receipt id"))?,
            dependency_registration_id: request.dependency_registration_id.clone(),
            artifact_ref: request.artifact_ref.clone(),
            artifact_version: request.artifact_version.clone(),
            request_digest: request.request_digest.clone(),
        };
        self.dependencies.insert(
            key,
            DependencyRecord {
                request,
                receipt: receipt.clone(),
            },
        );
        Ok(receipt)
    }

    fn dependencies_complete(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        dependencies_complete(
            self.dependencies
                .values()
                .filter(|edge| {
                    edge.request.artifact_ref == *artifact_ref
                        && edge.request.artifact_version == *artifact_version
                })
                .map(|edge| &edge.request),
        )
    }

    fn observe_fence(&self) -> Result<FenceInstallReceipt, AdmissionError> {
        Ok(self.fence)
    }

    fn install_fence(
        &mut self,
        expected_protocol_sequence: u64,
    ) -> Result<FenceInstallReceipt, AdmissionError> {
        if self.fence.protocol_sequence != expected_protocol_sequence {
            return Err(AdmissionError::StaleProtocol {
                expected: expected_protocol_sequence,
                actual: self.fence.protocol_sequence,
            });
        }
        self.fence.fence_generation += 1;
        self.fence.protocol_sequence += 1;
        Ok(self.fence)
    }

    fn final_publication_gate(
        &mut self,
        request: PublicationGateRequest,
    ) -> Result<PublicationReceipt, AdmissionError> {
        validate_publication_request(&request)?;
        let key = request.publication_operation_id.as_str().to_owned();
        if let Some((digest, receipt)) = self.publications.get(&key) {
            if digest != &request.request_digest {
                return Err(AdmissionError::IdempotencyConflict);
            }
            return Ok(receipt.clone());
        }
        if self.fence.fence_generation != request.observed_fence_generation {
            return Err(AdmissionError::StaleFence {
                expected: request.observed_fence_generation,
                actual: self.fence.fence_generation,
            });
        }
        if self.fence.protocol_sequence != request.observed_protocol_sequence {
            return Err(AdmissionError::StaleProtocol {
                expected: request.observed_protocol_sequence,
                actual: self.fence.protocol_sequence,
            });
        }
        if !self
            .producers
            .contains_key(request.producer_work_item_id.as_str())
        {
            return Err(AdmissionError::NotFound);
        }
        let matching: Vec<&DependencyRecord> = self
            .dependencies
            .values()
            .filter(|edge| {
                edge.request.artifact_ref == request.artifact_ref
                    && edge.request.artifact_version == request.artifact_version
            })
            .collect();
        let requests = matching.iter().map(|edge| &edge.request);
        if !dependencies_complete(requests)? {
            return Err(AdmissionError::DependencySetIncomplete);
        }
        let mut stored_ids: Vec<OpaqueId> = matching
            .iter()
            .map(|edge| edge.receipt.receipt_id.clone())
            .collect();
        let mut provided = request.dependency_receipt_ids.clone();
        stored_ids.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        provided.sort_by(|a, b| a.as_str().cmp(b.as_str()));
        if stored_ids != provided {
            return Err(AdmissionError::ReceiptMismatch);
        }
        let next_sequence = self.fence.protocol_sequence + 1;
        let receipt = PublicationReceipt {
            receipt_id: OpaqueId::new(format!(
                "publication:{}",
                request.publication_operation_id.as_str()
            ))
            .map_err(|_| AdmissionError::InvalidInput("publication receipt id"))?,
            publication_operation_id: request.publication_operation_id,
            artifact_ref: request.artifact_ref,
            artifact_version: request.artifact_version,
            producer_work_item_id: request.producer_work_item_id,
            dependency_receipt_ids: provided,
            fence_generation: self.fence.fence_generation,
            permission_epoch: request.permission_epoch,
            protocol_sequence: next_sequence,
            visible: true,
        };
        self.publications
            .insert(key, (request.request_digest, receipt.clone()));
        self.fence.protocol_sequence = next_sequence;
        Ok(receipt)
    }

    fn is_artifact_visible(
        &self,
        artifact_ref: &OpaqueId,
        artifact_version: &OpaqueId,
    ) -> Result<bool, AdmissionError> {
        Ok(self.publications.values().any(|(_, receipt)| {
            receipt.artifact_ref == *artifact_ref && receipt.artifact_version == *artifact_version
        }))
    }

    fn dependency_ledger_count(&self) -> Result<u64, AdmissionError> {
        Ok(self.dependencies.len() as u64)
    }

    fn publication_receipt(
        &self,
        operation_id: &OpaqueId,
    ) -> Result<PublicationReceipt, AdmissionError> {
        self.publications
            .get(operation_id.as_str())
            .map(|(_, receipt)| receipt.clone())
            .ok_or(AdmissionError::NotFound)
    }

    fn work_state(&self, work_item_id: &OpaqueId) -> Result<WorkState, AdmissionError> {
        self.producers
            .get(work_item_id.as_str())
            .map(|r| r.state)
            .ok_or(AdmissionError::NotFound)
    }
}

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
        WorkState::DependencyRegistered | WorkState::PreparedHidden => {
            BarrierMeaning::DependenciesDurableArtifactHidden
        }
        WorkState::PublicationGatePending => {
            BarrierMeaning::PublicationDecisionPendingArtifactHidden
        }
        WorkState::Published => BarrierMeaning::PublicationReceiptDurable,
        WorkState::RetryQueued | WorkState::DlqParked => {
            BarrierMeaning::NonTerminalReplayRemainsPossible
        }
        WorkState::SuppressedQuarantined => BarrierMeaning::SuppressedNoPublicationEvidenceRequired,
        WorkState::Rejected | WorkState::Cancelled | WorkState::Terminal => {
            BarrierMeaning::TerminalEvidenceRequiresDValidation
        }
    }
}

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

fn dependencies_complete<'a>(
    requests: impl Iterator<Item = &'a DependencyRegistrationRequest>,
) -> Result<bool, AdmissionError> {
    let mut required = None;
    let mut count = 0_u32;
    for request in requests {
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

pub fn request_digest<T: Serialize>(request: &T) -> Result<String, AdmissionError> {
    let bytes = serde_json::to_vec(request)?;
    Ok(format!("{:x}", Sha256::digest(bytes)))
}

#[cfg(feature = "sqlite")]
fn encode<T: Serialize>(value: &T) -> Result<String, AdmissionError> {
    Ok(serde_json::to_string(value)?)
}
#[cfg(feature = "sqlite")]
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

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::ScopeKind;

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
    fn producer_registration_is_idempotent_and_conflicting_digest_does_not_add_rows() {
        let mut db = MemoryAdmissionStore::new();
        let first = db.register_producer_work(producer()).unwrap();
        let retry = db.register_producer_work(producer()).unwrap();
        assert_eq!(first.receipt_id, retry.receipt_id);
        assert_eq!(db.producer_ledger_count().unwrap(), 1);
        let mut conflict = producer();
        conflict.request_digest = "different-digest".into();
        assert!(matches!(
            db.register_producer_work(conflict),
            Err(AdmissionError::IdempotencyConflict)
        ));
        assert_eq!(db.producer_ledger_count().unwrap(), 1);
    }

    #[test]
    fn producer_receipt_lookup_and_not_found_are_distinct() {
        let mut db = MemoryAdmissionStore::new();
        let receipt = db.register_producer_work(producer()).unwrap();
        assert_eq!(db.producer_receipt(&id("work-1")).unwrap(), receipt);
        assert!(matches!(
            db.producer_receipt(&id("missing")),
            Err(AdmissionError::NotFound)
        ));
    }

    #[test]
    fn partial_dependencies_remain_hidden_until_all_edges_are_registered() {
        let mut db = MemoryAdmissionStore::new();
        db.register_producer_work(producer()).unwrap();
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
        assert!(matches!(
            db.final_publication_gate(gate(obs, vec![first.receipt_id, second.receipt_id])),
            Ok(_)
        ));
        assert!(db
            .is_artifact_visible(&id("artifact-1"), &id("artifact-version-1"))
            .unwrap());
    }

    #[test]
    fn final_gate_receipt_binds_observed_fence_and_permission_epoch() {
        let mut db = MemoryAdmissionStore::new();
        db.register_producer_work(producer()).unwrap();
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
        assert!(!legal_transition(WorkState::Accepted, WorkState::Published));
        let mut db = MemoryAdmissionStore::new();
        db.register_producer_work(producer()).unwrap();
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
            let mut db = MemoryAdmissionStore::new();
            let mut request = producer();
            request.producer_work_item_id = id(&format!("work-alt-exit-{index}"));
            request.request_digest = format!("request-alt-exit-{index}");
            db.register_producer_work(request).unwrap();

            for state in path {
                db.transition_work_state(&id(&format!("work-alt-exit-{index}")), *state)
                    .unwrap();
            }
            let work_item_id = id(&format!("work-alt-exit-{index}"));
            assert_eq!(db.work_state(&work_item_id).unwrap(), expected_from);

            db.transition_work_state(&work_item_id, target).unwrap();

            assert_eq!(db.work_state(&work_item_id).unwrap(), target);
        }
    }

    #[test]
    fn gate_reports_stale_protocol_when_fence_generation_matches() {
        let mut db = MemoryAdmissionStore::new();
        db.register_producer_work(producer()).unwrap();
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
}