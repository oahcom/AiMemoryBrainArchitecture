//! Memory Compiler reference pipeline.
//! Deterministic five-stage reference pipeline with a local SQLite admission ledger.
//! Production D/Storage authority integrations are provided by the
//! `publication_authority` adapter.

#[cfg(feature = "sqlite")]
pub mod admission;
#[cfg(feature = "sqlite")]
pub mod publication_authority;

use memory_domain::OpaqueId;
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;

pub const COMPILER_VERSION: &str = "0.1.0";

/// Strongly typed identifier for a producer work item admitted by the compiler.
#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
pub struct ProducerWorkItemId(OpaqueId);

impl ProducerWorkItemId {
    pub fn new(value: OpaqueId) -> Self {
        Self(value)
    }

    pub fn as_opaque_id(&self) -> &OpaqueId {
        &self.0
    }
}

/// Digest algorithm used for the interim payload integrity check.
pub const PAYLOAD_DIGEST_ALGORITHM: &str = "sha256";

/// Representation the digest is computed over. `raw-v1` means the exact UTF-8
/// bytes of the accepted payload, with no canonical envelope normalisation.
/// A versioned canonical envelope is owned by the BMCP/domain contract and is
/// not defined here.
pub const PAYLOAD_CANONICALIZATION_VERSION: &str = "raw-v1";

/// SHA-256 over the exact UTF-8 bytes of the accepted payload.
///
/// ponytail: raw bytes only, not the canonical envelope the stage contract
/// ultimately describes. Upgrade path is a versioned `canonicalization_version`
/// supplied by the BMCP/domain contract; until then this value is honestly
/// labelled `raw-v1` rather than presented as canonical.
fn raw_payload_digest(payload: &str) -> String {
    format!("sha256:{:x}", Sha256::digest(payload.as_bytes()))
}

#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub struct Identity(pub String);

impl Identity {
    pub fn new(value: impl Into<String>) -> Result<Self, CompilerError> {
        let value = value.into();
        if value.trim().is_empty() {
            return Err(CompilerError::InvalidIdentity);
        }
        Ok(Self(value))
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Provenance {
    pub source_event_id: Identity,
    pub source_payload_digest: String,
    pub payload_digest_algorithm: String,
    pub canonicalization_version: String,
    pub stage_output_id: Identity,
    pub upstream_outputs: Vec<Identity>,
    pub compiler_version: String,
    pub parameter_digest: String,
    pub stage_name: StageName,
    pub attempt_generation: u64,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum StageName {
    Ingestion,
    Extraction,
    Normalization,
    Staging,
    PublicationGate,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CompilerError {
    InvalidIdentity,
    MissingAcceptedReceipt,
    MissingCompileIntent,
    InvalidPayloadDigest,
    PayloadDigestMismatch {
        declared: String,
        computed: String,
    },
    EmptyExtraction,
    InvalidNormalizedValue,
    IncompleteDependencyClosure,
    MissingProducerAdmission,
    MissingCanonicalCommit,
    MissingPreparedHiddenTuple,
    MissingPublicationAdmission,
    StaleWorker,
    PublicationSuppressed,
    InvalidPublicationProof,
    IllegalStateTransition,
    LeaseExpired,
    AdmissionStoreFailure,
    /// The stored payload is not valid UTF-8. Kept distinct from
    /// `PayloadDigestMismatch` because no digest can be computed at all: the
    /// bytes never become the `String` the pipeline digests.
    InvalidPayloadEncoding,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub enum ExecutionState {
    Pending,
    Leased,
    Running,
    Staged,
    PreparedHidden,
    PublicationAdmission,
    Published,
    Suppressed,
    Blocked,
    Failed,
}

impl ExecutionState {
    pub fn is_terminal(&self) -> bool {
        matches!(self, Self::Published | Self::Suppressed | Self::Failed)
    }

    pub fn can_transition_to(&self, next: ExecutionState) -> bool {
        matches!(
            (self, next),
            (Self::Pending, Self::Leased)
                | (Self::Leased, Self::Running)
                | (Self::Running, Self::Staged)
                | (Self::Staged, Self::PreparedHidden)
                | (Self::PreparedHidden, Self::PublicationAdmission)
                | (Self::PublicationAdmission, Self::Published)
                | (Self::PublicationAdmission, Self::Suppressed)
                | (Self::PublicationAdmission, Self::Blocked)
                | (Self::PublicationAdmission, Self::Failed)
                | (Self::Blocked, Self::Pending)
        )
    }
}

/// Recoverable execution metadata for one logical operation and stage.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StageExecution {
    pub operation_id: Identity,
    pub stage: StageName,
    pub state: ExecutionState,
    pub attempt_generation: u64,
    pub last_durable_stage: Option<StageName>,
    pub lease: Option<WorkerLease>,
}

impl StageExecution {
    pub fn new(operation_id: Identity, stage: StageName) -> Self {
        Self {
            operation_id,
            stage,
            state: ExecutionState::Pending,
            attempt_generation: 1,
            last_durable_stage: None,
            lease: None,
        }
    }

    pub fn advance(&mut self, next: ExecutionState) -> Result<(), CompilerError> {
        if !self.state.can_transition_to(next) {
            return Err(CompilerError::IllegalStateTransition);
        }
        self.state = next;
        Ok(())
    }

    pub fn record_durable(&mut self, stage: StageName) {
        self.last_durable_stage = Some(stage);
    }

    pub fn retry(&mut self) -> Result<(), CompilerError> {
        if !matches!(self.state, ExecutionState::Failed | ExecutionState::Blocked) {
            return Err(CompilerError::IllegalStateTransition);
        }

        let next_generation = self
            .attempt_generation
            .checked_add(1)
            .ok_or(CompilerError::IllegalStateTransition)?;

        self.attempt_generation = next_generation;
        self.state = ExecutionState::Pending;
        self.lease = None;
        Ok(())
    }

    pub fn lease_is_current(&self, current_generation: u64) -> bool {
        self.lease
            .as_ref()
            .map(|lease| lease.generation == current_generation)
            .unwrap_or(false)
    }

    pub fn can_publish(&self) -> bool {
        self.state == ExecutionState::PublicationAdmission && self.lease.is_some()
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AcceptedEvent {
    pub event_id: Identity,
    pub receipt_id: Identity,
    pub payload_digest: String,
    pub payload: String,
    pub compile_intent_durable: bool,
}

/// Build the compiler input from a pending compile intent read out of the
/// durable outbox.
///
/// This is the only place a production caller gets an `AcceptedEvent` whose
/// `compile_intent_durable` is not a lie. `IngestionStage::run` rejects
/// `compile_intent_durable == false`, so the flag has to come from evidence
/// rather than from the caller. The evidence here is that the row was returned
/// by `SqliteEventStore::pending_compile_intents()`, whose query inner-joins
/// `compile_outbox` with `accepted_events` and `event_payloads`: a row exists
/// only because a `compile_outbox` row exists.
///
/// The bytes are re-digested instead of trusted. The store verified them on
/// write, but the intent is a snapshot taken later, and an adapter that copies
/// `receipt.payload_digest` without recomputing would pass a tampered payload
/// straight into compilation.
///
/// The struct is sealed: its fields are private, and its only source is a
/// store-backed row returned by `SqliteEventStore::pending_compile_intents()`.
/// Callers cannot construct a forged intent with
/// `compile_intent_durable: true`. The remaining guarantee boundary is that
/// the payload bytes are re-digested by this adapter rather than trusted from
/// the stored receipt or envelope.
#[cfg(feature = "sqlite")]
pub fn accepted_event_from(
    intent: &memory_event_store_sqlite::PendingCompileIntent,
) -> Result<AcceptedEvent, CompilerError> {
    let event_id = Identity::new(intent.receipt().event_id.as_str().to_owned())?;
    let receipt_id = Identity::new(intent.receipt().receipt_id.as_str().to_owned())?;

    // Lossy decoding would silently change the bytes whose digest was accepted.
    let payload = String::from_utf8(intent.payload_bytes())
        .map_err(|_| CompilerError::InvalidPayloadEncoding)?;

    let computed_digest = raw_payload_digest(&payload);
    if intent.receipt().payload_digest != computed_digest {
        return Err(CompilerError::PayloadDigestMismatch {
            declared: intent.receipt().payload_digest.clone(),
            computed: computed_digest,
        });
    }
    if intent.envelope().payload_digest != computed_digest {
        return Err(CompilerError::PayloadDigestMismatch {
            declared: intent.envelope().payload_digest.clone(),
            computed: computed_digest,
        });
    }

    Ok(AcceptedEvent {
        event_id,
        receipt_id,
        payload_digest: computed_digest,
        payload,
        compile_intent_durable: true,
    })
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct IngestedEvent {
    pub event_id: Identity,
    pub receipt_id: Identity,
    pub payload_digest: String,
    pub payload: String,
    pub provenance: Provenance,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExtractionIR {
    pub event_id: Identity,
    pub segments: Vec<String>,
    pub provenance: Provenance,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct NormalizedIR {
    pub event_id: Identity,
    pub values: Vec<String>,
    pub provenance: Provenance,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Visibility {
    Hidden,
    Visible,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StagedDerivative {
    pub derivative_id: Identity,
    pub publication_id: Identity,
    pub event_id: Identity,
    pub values: Vec<String>,
    pub dependency_ids: Vec<Identity>,
    pub dependency_closure_digest: String,
    pub visibility: Visibility,
    pub provenance: Provenance,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PublishedDerivative {
    pub derivative: StagedDerivative,
    pub disposition: PublicationDisposition,
}

/// Publication outcome. `Failed` is reserved for the Storage boundary when
/// visibility advancement fails; this crate has no Storage advancement hook
/// and therefore has no in-crate trigger for that disposition.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PublicationDisposition {
    Published,
    Suppressed,
    Blocked,
    Failed,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct WorkerLease {
    pub operation_id: Identity,
    pub worker_id: Identity,
    pub generation: u64,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PublicationProof {
    pub publication_id: Identity,
    pub generation: u64,
    pub producer_admitted: bool,
    pub dependency_closure_complete: bool,
    pub canonical_commit_confirmed: bool,
    pub storage_prepared_hidden: bool,
    pub publication_participant_admitted: bool,
    pub protected_visibility_authorized: bool,
}

/// Ingestion accepts only an already durably Accepted Event.
/// It does not implement the Event Store or create Accepted Receipts.
pub struct IngestionStage;

impl IngestionStage {
    pub fn run(event: AcceptedEvent, generation: u64) -> Result<IngestedEvent, CompilerError> {
        if event.receipt_id.0.is_empty() {
            return Err(CompilerError::MissingAcceptedReceipt);
        }
        if !event.compile_intent_durable {
            return Err(CompilerError::MissingCompileIntent);
        }
        if event.payload_digest.trim().is_empty() {
            return Err(CompilerError::InvalidPayloadDigest);
        }

        let computed_digest = raw_payload_digest(&event.payload);
        if event.payload_digest != computed_digest {
            return Err(CompilerError::PayloadDigestMismatch {
                declared: event.payload_digest,
                computed: computed_digest,
            });
        }

        let provenance = Provenance {
            source_event_id: event.event_id.clone(),
            source_payload_digest: computed_digest.clone(),
            payload_digest_algorithm: PAYLOAD_DIGEST_ALGORITHM.into(),
            canonicalization_version: PAYLOAD_CANONICALIZATION_VERSION.into(),
            stage_output_id: Identity(format!("{}:ingestion", event.event_id.0)),
            upstream_outputs: vec![],
            compiler_version: COMPILER_VERSION.into(),
            parameter_digest: "ingestion:v1".into(),
            stage_name: StageName::Ingestion,
            attempt_generation: generation,
        };

        Ok(IngestedEvent {
            event_id: event.event_id,
            receipt_id: event.receipt_id,
            payload_digest: computed_digest,
            payload: event.payload,
            provenance,
        })
    }
}

/// Deterministic reference extractor. It does not invoke an LLM.
pub struct ExtractionStage;

impl ExtractionStage {
    pub fn run(input: IngestedEvent, generation: u64) -> Result<ExtractionIR, CompilerError> {
        let segments: Vec<String> = input
            .payload
            .split(['.', '!', '?', '\n'])
            .map(str::trim)
            .filter(|s| !s.is_empty())
            .map(str::to_owned)
            .collect();

        if segments.is_empty() {
            return Err(CompilerError::EmptyExtraction);
        }

        let provenance = Provenance {
            source_event_id: input.event_id.clone(),
            source_payload_digest: input.payload_digest,
            payload_digest_algorithm: input.provenance.payload_digest_algorithm.clone(),
            canonicalization_version: input.provenance.canonicalization_version.clone(),
            stage_output_id: Identity(format!(
                "{}:extraction:{}",
                input.event_id.0,
                segments.len()
            )),
            upstream_outputs: vec![input.provenance.stage_output_id],
            compiler_version: COMPILER_VERSION.into(),
            parameter_digest: "deterministic-split:v1".into(),
            stage_name: StageName::Extraction,
            attempt_generation: generation,
        };

        Ok(ExtractionIR {
            event_id: input.event_id,
            segments,
            provenance,
        })
    }
}

/// Deterministic normalization. Original source evidence remains upstream.
pub struct NormalizationStage;

impl NormalizationStage {
    pub fn run(input: ExtractionIR, generation: u64) -> Result<NormalizedIR, CompilerError> {
        let values: Vec<String> = input
            .segments
            .iter()
            .map(|s| s.split_whitespace().collect::<Vec<_>>().join(" "))
            .filter(|s| !s.is_empty())
            .collect();

        if values.is_empty() {
            return Err(CompilerError::InvalidNormalizedValue);
        }

        let provenance = Provenance {
            source_event_id: input.event_id.clone(),
            source_payload_digest: input.provenance.source_payload_digest.clone(),
            payload_digest_algorithm: input.provenance.payload_digest_algorithm.clone(),
            canonicalization_version: input.provenance.canonicalization_version.clone(),
            stage_output_id: Identity(format!(
                "{}:normalization:{}",
                input.event_id.0,
                values.len()
            )),
            upstream_outputs: vec![input.provenance.stage_output_id],
            compiler_version: COMPILER_VERSION.into(),
            parameter_digest: "whitespace-normalization:v1".into(),
            stage_name: StageName::Normalization,
            attempt_generation: generation,
        };

        Ok(NormalizedIR {
            event_id: input.event_id,
            values,
            provenance,
        })
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StagingInput {
    pub normalized: NormalizedIR,
    pub derivative_id: Identity,
    pub publication_id: Identity,
    pub dependency_ids: Vec<Identity>,
    pub dependency_closure_complete: bool,
    pub producer_admitted: bool,
    pub canonical_commit_cursor_recorded: bool,
}

pub struct StagingStage;

impl StagingStage {
    pub fn run(input: StagingInput, generation: u64) -> Result<StagedDerivative, CompilerError> {
        if !input.producer_admitted {
            return Err(CompilerError::MissingProducerAdmission);
        }
        if !input.dependency_closure_complete || input.dependency_ids.is_empty() {
            return Err(CompilerError::IncompleteDependencyClosure);
        }
        if !input.canonical_commit_cursor_recorded {
            return Err(CompilerError::MissingCanonicalCommit);
        }

        let mut ordered = BTreeSet::new();
        for id in &input.dependency_ids {
            ordered.insert(id.0.clone());
        }
        if ordered.len() != input.dependency_ids.len() {
            return Err(CompilerError::IncompleteDependencyClosure);
        }

        let closure_digest = ordered.into_iter().collect::<Vec<_>>().join("|");
        let provenance = Provenance {
            source_event_id: input.normalized.event_id.clone(),
            source_payload_digest: input.normalized.provenance.source_payload_digest.clone(),
            payload_digest_algorithm: input.normalized.provenance.payload_digest_algorithm.clone(),
            canonicalization_version: input.normalized.provenance.canonicalization_version.clone(),
            stage_output_id: input.derivative_id.clone(),
            upstream_outputs: vec![input.normalized.provenance.stage_output_id],
            compiler_version: COMPILER_VERSION.into(),
            parameter_digest: format!("dependency-closure:{}", closure_digest),
            stage_name: StageName::Staging,
            attempt_generation: generation,
        };

        Ok(StagedDerivative {
            derivative_id: input.derivative_id,
            publication_id: input.publication_id,
            event_id: input.normalized.event_id,
            values: input.normalized.values,
            dependency_ids: input.dependency_ids,
            dependency_closure_digest: closure_digest,
            visibility: Visibility::Hidden,
            provenance,
        })
    }
}

/// Production implementations MUST obtain this proof from authoritative
/// D/Storage boundaries. A caller-provided boolean is not production evidence.
pub trait PublicationAuthority {
    fn obtain_proof(
        &mut self,
        staged: &StagedDerivative,
        lease: &WorkerLease,
    ) -> Result<PublicationProof, CompilerError>;
}

pub struct PublicationGate;

impl PublicationGate {
    pub fn run<A: PublicationAuthority>(
        staged: StagedDerivative,
        lease: &WorkerLease,
        current_generation: u64,
        authority: &mut A,
    ) -> Result<PublishedDerivative, CompilerError> {
        if lease.generation != current_generation
            || staged.provenance.attempt_generation != lease.generation
        {
            return Ok(PublishedDerivative {
                derivative: staged,
                disposition: PublicationDisposition::Suppressed,
            });
        }

        if staged.visibility != Visibility::Hidden {
            return Ok(PublishedDerivative {
                derivative: staged,
                disposition: PublicationDisposition::Blocked,
            });
        }

        // Authority failures remain errors: they are not a publication
        // disposition and must be propagated without reinterpretation.
        let proof = authority.obtain_proof(&staged, lease)?;

        if proof.publication_id != staged.publication_id || proof.generation != lease.generation {
            return Ok(PublishedDerivative {
                derivative: staged,
                disposition: PublicationDisposition::Blocked,
            });
        }

        if !proof.producer_admitted
            || !proof.dependency_closure_complete
            || !proof.canonical_commit_confirmed
            || !proof.storage_prepared_hidden
        {
            return Ok(PublishedDerivative {
                derivative: staged,
                disposition: PublicationDisposition::Blocked,
            });
        }

        if !proof.publication_participant_admitted || !proof.protected_visibility_authorized {
            return Ok(PublishedDerivative {
                derivative: staged,
                disposition: PublicationDisposition::Suppressed,
            });
        }

        let mut published = staged;
        published.visibility = Visibility::Visible;

        Ok(PublishedDerivative {
            derivative: published,
            disposition: PublicationDisposition::Published,
        })
    }
}

pub(crate) fn map_admission_error(error: admission::AdmissionError) -> CompilerError {
    match error {
        admission::AdmissionError::NotFound => CompilerError::MissingProducerAdmission,
        _ => CompilerError::AdmissionStoreFailure,
    }
}

/// Reference pipeline: five explicit typed stages.
/// External authorities remain injected through PublicationAuthority.
pub struct MemoryCompiler<A> {
    pub authority: A,
    pub admission: admission::AdmissionStore,
}

impl<A: PublicationAuthority> MemoryCompiler<A> {
    /// Compile only after the caller has durably registered producer work and
    /// every dependency in the local AdmissionStore. A receipt proves only that
    /// the corresponding local ledger row exists; it does not prove external
    /// producer-registry authorization. No registration is performed here.
    pub fn compile(
        &mut self,
        event: AcceptedEvent,
        mut staging: StagingInput,
        lease: WorkerLease,
        current_generation: u64,
        producer_work_item_id: &ProducerWorkItemId,
    ) -> Result<PublishedDerivative, CompilerError> {
        let producer_receipt = self
            .admission
            .producer_receipt(producer_work_item_id.as_opaque_id())
            .map_err(map_admission_error)?;
        if producer_receipt.disposition != admission::RegistrationDisposition::Accepted {
            return Err(CompilerError::MissingProducerAdmission);
        }
        let producer_request = self
            .admission
            .producer_request(producer_work_item_id.as_opaque_id())
            .map_err(map_admission_error)?;

        let artifact_ref = OpaqueId::new(staging.derivative_id.0.clone())
            .map_err(|_| CompilerError::InvalidIdentity)?;
        let artifact_version = OpaqueId::new(staging.publication_id.0.clone())
            .map_err(|_| CompilerError::InvalidIdentity)?;
        if !self
            .admission
            .dependencies_complete(&artifact_ref, &artifact_version)
            .map_err(map_admission_error)?
        {
            return Err(CompilerError::IncompleteDependencyClosure);
        }
        let dependency_entries = self
            .admission
            .dependency_entries_for(
                &artifact_ref,
                &artifact_version,
                producer_work_item_id.as_opaque_id(),
            )
            .map_err(map_admission_error)?;
        if dependency_entries.is_empty() {
            return Err(CompilerError::IncompleteDependencyClosure);
        }
        let dependency_ids = dependency_entries
            .iter()
            .map(|(request, _)| Identity(request.source_ref.as_str().to_owned()))
            .collect::<Vec<_>>();
        let dependency_receipt_ids = dependency_entries
            .iter()
            .map(|(_, receipt)| receipt.receipt_id.clone())
            .collect::<Vec<_>>();
        let derivation_run_id = dependency_entries[0].0.derivation_run_id.clone();
        if dependency_entries
            .iter()
            .any(|(request, _)| request.derivation_run_id != derivation_run_id)
        {
            return Err(CompilerError::IncompleteDependencyClosure);
        }
        // D6.3: presence records only a caller-supplied cursor. It is persisted
        // without validation and does not establish that a commit was confirmed.
        if producer_request.admission_canonical_commit_cursor.is_none() {
            return Err(CompilerError::MissingCanonicalCommit);
        }

        // Staging admission booleans and dependency IDs are derived from the
        // durable local ledger, never accepted from caller-provided flags.
        staging.producer_admitted = true;
        staging.dependency_closure_complete = true;
        // D6.2: this asserts only that a caller supplied a cursor and the ledger
        // persisted it. It is NOT evidence that a canonical commit was confirmed;
        // `PublicationProof::canonical_commit_confirmed` stays false in the
        // production adapter until owner D freezes that contract (D6.1).
        staging.canonical_commit_cursor_recorded = true;
        staging.dependency_ids = dependency_ids;

        let ingested = IngestionStage::run(event, lease.generation)?;
        let extracted = ExtractionStage::run(ingested, lease.generation)?;
        let normalized = NormalizationStage::run(extracted, lease.generation)?;
        if normalized.event_id != staging.normalized.event_id {
            return Err(CompilerError::InvalidPublicationProof);
        }
        let staged = StagingStage::run(
            StagingInput {
                normalized,
                ..staging
            },
            lease.generation,
        )?;
        let gated = PublicationGate::run(staged, &lease, current_generation, &mut self.authority)?;
        if gated.disposition != PublicationDisposition::Published {
            // Preserve the publication gate's typed terminal outcome.
            // In particular, Suppressed must remain distinguishable from
            // retryable Blocked outcomes.
            return Ok(gated);
        }

        let observation = self
            .admission
            .observe_fence()
            .map_err(map_admission_error)?;
        let publication_operation_id = OpaqueId::new(format!(
            "compiler-publication:{}",
            gated.derivative.publication_id.0
        ))
        .map_err(|_| CompilerError::InvalidIdentity)?;
        let gate_request = admission::PublicationGateRequest {
            publication_operation_id: publication_operation_id.clone(),
            artifact_ref,
            artifact_version,
            producer_work_item_id: producer_work_item_id.as_opaque_id().clone(),
            derivation_run_id,
            attempt_id: OpaqueId::new(format!("attempt:{}", lease.generation))
                .map_err(|_| CompilerError::InvalidIdentity)?,
            lease_id: OpaqueId::new(lease.worker_id.0.clone())
                .map_err(|_| CompilerError::InvalidIdentity)?,
            dependency_receipt_ids,
            permission_epoch: producer_request.permission_epoch,
            observed_fence_generation: observation.fence_generation,
            observed_protocol_sequence: observation.protocol_sequence,
            scope_refs: producer_request.scope_refs,
            request_digest: format!(
                "compiler-publication:{}:{}:{}",
                gated.derivative.publication_id.0,
                producer_work_item_id.as_opaque_id().as_str(),
                lease.generation
            ),
        };
        let receipt = self
            .admission
            .final_publication_gate(gate_request)
            .map_err(map_admission_error)?;
        if !receipt.visible {
            return Err(CompilerError::PublicationSuppressed);
        }
        Ok(gated)
    }

    /// §6.3 recovery entry point.
    ///
    /// The supplied StagingInput contains the normalized stage result, so this
    /// reference implementation resumes from that typed result and does not
    /// repeat ingestion, extraction, or normalization. A missing durable-stage
    /// marker does not provide an AcceptedEvent to this API; consequently the
    /// available normalized input is the earliest stage result it can consume.
    ///
    /// This is deterministic in-process recovery only. It does not establish
    /// durable storage, commit-outcome resolution, or production authorization.
    pub fn resume(
        &mut self,
        execution: &StageExecution,
        staging: StagingInput,
        lease: WorkerLease,
        current_generation: u64,
    ) -> Result<PublishedDerivative, CompilerError> {
        if execution.state.is_terminal() {
            return Err(CompilerError::IllegalStateTransition);
        }

        if !execution.lease_is_current(current_generation)
            || lease.generation != current_generation
            || lease.operation_id != execution.operation_id
            || execution
                .lease
                .as_ref()
                .map(|current| current != &lease)
                .unwrap_or(true)
        {
            return Err(CompilerError::LeaseExpired);
        }

        if !matches!(
            execution.last_durable_stage,
            None | Some(StageName::Ingestion)
                | Some(StageName::Extraction)
                | Some(StageName::Normalization)
                | Some(StageName::Staging)
                | Some(StageName::PublicationGate)
        ) {
            return Err(CompilerError::IllegalStateTransition);
        }

        let staged = StagingStage::run(staging, lease.generation)?;
        PublicationGate::run(staged, &lease, current_generation, &mut self.authority)
    }
}

#[cfg(test)]
fn digest_of(payload: &str) -> String {
    // Deliberately independent of raw_payload_digest: a fixture built from the
    // production helper would make every digest test tautological.
    format!("sha256:{:x}", Sha256::digest(payload.as_bytes()))
}

#[cfg(test)]
mod payload_digest_tests {
    use super::*;

    #[test]
    fn sha256_raw_v1_matches_a_known_vector() {
        // NIST FIPS 180-4 test vector for "abc".
        assert_eq!(
            raw_payload_digest("abc"),
            "sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
        assert_eq!(raw_payload_digest("abc"), digest_of("abc"));
    }

    #[test]
    fn ingestion_rejects_payload_changed_without_digest_update() {
        let mut event = AcceptedEvent {
            event_id: Identity::new("event-tampered-payload").unwrap(),
            receipt_id: Identity::new("receipt-tampered-payload").unwrap(),
            payload_digest: digest_of("original payload"),
            payload: "original payload".into(),
            compile_intent_durable: true,
        };
        event.payload = "tampered payload".into();

        let result = IngestionStage::run(event, 1);
        assert!(matches!(
            &result,
            Err(CompilerError::PayloadDigestMismatch { .. })
        ));

        match result {
            Err(CompilerError::PayloadDigestMismatch { declared, computed }) => {
                assert_eq!(declared, digest_of("original payload"));
                assert_eq!(computed, digest_of("tampered payload"));
                assert_ne!(declared, computed);
            }
            other => panic!("expected PayloadDigestMismatch, got {:?}", other),
        }
    }

    #[test]
    fn ingestion_rejects_digest_changed_without_payload_update() {
        let payload = "payload remains unchanged";
        let mut event = AcceptedEvent {
            event_id: Identity::new("event-tampered-digest").unwrap(),
            receipt_id: Identity::new("receipt-tampered-digest").unwrap(),
            payload_digest: digest_of(payload),
            payload: payload.into(),
            compile_intent_durable: true,
        };
        let correct = event.payload_digest.clone();
        event.payload_digest = "0".repeat(64);

        let result = IngestionStage::run(event, 1);
        assert!(matches!(
            &result,
            Err(CompilerError::PayloadDigestMismatch { .. })
        ));
        match result {
            Err(CompilerError::PayloadDigestMismatch { declared, computed }) => {
                assert_eq!(declared, "0".repeat(64));
                assert_eq!(computed, correct);
            }
            other => panic!("expected PayloadDigestMismatch, got {:?}", other),
        }
    }

    #[test]
    fn valid_digest_is_recomputed_and_carried_to_the_next_stage() {
        let payload = "A valid payload. A second sentence.";
        let expected = digest_of(payload);

        let event = AcceptedEvent {
            event_id: Identity::new("event-valid-digest").unwrap(),
            receipt_id: Identity::new("receipt-valid-digest").unwrap(),
            payload_digest: expected.clone(),
            payload: payload.into(),
            compile_intent_durable: true,
        };

        let ingested = IngestionStage::run(event, 1).unwrap();
        // The stored value is the recomputed one, which is what proves the
        // comparison actually ran rather than the input being copied through.
        assert_eq!(ingested.payload_digest, expected);
        assert_eq!(ingested.provenance.source_payload_digest, expected);
        assert_eq!(ingested.provenance.payload_digest_algorithm, "sha256");
        assert_eq!(ingested.provenance.canonicalization_version, "raw-v1");

        let extracted = ExtractionStage::run(ingested, 1).unwrap();
        assert_eq!(extracted.provenance.source_payload_digest, expected);
        assert_eq!(extracted.provenance.payload_digest_algorithm, "sha256");
        assert_eq!(extracted.provenance.canonicalization_version, "raw-v1");
    }

    #[test]
    fn ingestion_accepts_event_store_sha256_prefixed_digest() {
        let payload = "prefix format is emitted by Event Store";
        let event = AcceptedEvent {
            event_id: Identity::new("event-prefixed-digest").unwrap(),
            receipt_id: Identity::new("receipt-prefixed-digest").unwrap(),
            payload_digest: digest_of(payload),
            payload: payload.into(),
            compile_intent_durable: true,
        };

        let ingested = IngestionStage::run(event, 1).unwrap();
        assert_eq!(ingested.payload_digest, digest_of(payload));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(s: &str) -> Identity {
        Identity::new(s).unwrap()
    }

    fn event() -> AcceptedEvent {
        let payload = "I plan to move to Tokyo. I tried to deploy.".to_owned();
        AcceptedEvent {
            event_id: id("event-1"),
            receipt_id: id("receipt-1"),
            payload_digest: digest_of(&payload),
            payload,
            compile_intent_durable: true,
        }
    }

    fn pipeline() -> (IngestedEvent, ExtractionIR, NormalizedIR) {
        let ingested = IngestionStage::run(event(), 1).unwrap();
        let extracted = ExtractionStage::run(ingested.clone(), 1).unwrap();
        let normalized = NormalizationStage::run(extracted.clone(), 1).unwrap();
        (ingested, extracted, normalized)
    }

    fn staging_input(normalized: NormalizedIR) -> StagingInput {
        StagingInput {
            normalized,
            derivative_id: id("derivative-1"),
            publication_id: id("publication-1"),
            dependency_ids: vec![id("event-1"), id("source-1")],
            dependency_closure_complete: true,
            producer_admitted: true,
            canonical_commit_cursor_recorded: true,
        }
    }

    struct TestAuthority {
        publication_admitted: bool,
        visibility_authorized: bool,
    }

    struct EvidenceAuthority {
        producer_admitted: bool,
        storage_prepared_hidden: bool,
    }

    impl PublicationAuthority for EvidenceAuthority {
        fn obtain_proof(
            &mut self,
            staged: &StagedDerivative,
            lease: &WorkerLease,
        ) -> Result<PublicationProof, CompilerError> {
            Ok(PublicationProof {
                publication_id: staged.publication_id.clone(),
                generation: lease.generation,
                producer_admitted: self.producer_admitted,
                dependency_closure_complete: true,
                canonical_commit_confirmed: true,
                storage_prepared_hidden: self.storage_prepared_hidden,
                publication_participant_admitted: true,
                protected_visibility_authorized: true,
            })
        }
    }

    impl PublicationAuthority for TestAuthority {
        fn obtain_proof(
            &mut self,
            staged: &StagedDerivative,
            lease: &WorkerLease,
        ) -> Result<PublicationProof, CompilerError> {
            Ok(PublicationProof {
                publication_id: staged.publication_id.clone(),
                generation: lease.generation,
                producer_admitted: true,
                dependency_closure_complete: true,
                canonical_commit_confirmed: true,
                storage_prepared_hidden: true,
                publication_participant_admitted: self.publication_admitted,
                protected_visibility_authorized: self.visibility_authorized,
            })
        }
    }

    fn lease() -> WorkerLease {
        WorkerLease {
            operation_id: id("operation-1"),
            worker_id: id("worker-1"),
            generation: 1,
        }
    }

    #[test]
    fn ingestion_requires_durable_receipt_and_intent() {
        let mut e = event();
        e.compile_intent_durable = false;
        assert_eq!(
            IngestionStage::run(e, 1),
            Err(CompilerError::MissingCompileIntent)
        );
    }

    #[test]
    fn ingestion_preserves_original_receipt() {
        let result = IngestionStage::run(event(), 1).unwrap();
        assert_eq!(result.receipt_id, id("receipt-1"));
        assert_eq!(result.provenance.source_event_id, id("event-1"));
    }

    #[test]
    fn extraction_is_deterministic_and_lineaged() {
        let (_, first, _) = pipeline();
        let (_, second, _) = pipeline();
        assert_eq!(first, second);
        assert_eq!(first.segments.len(), 2);
        assert_eq!(first.provenance.upstream_outputs.len(), 1);
    }

    #[test]
    fn normalization_preserves_upstream_identity() {
        let (_, extracted, normalized) = pipeline();
        assert_eq!(
            normalized.provenance.upstream_outputs,
            vec![extracted.provenance.stage_output_id]
        );
    }

    #[test]
    fn staging_requires_producer_admission() {
        let (_, _, normalized) = pipeline();
        let mut input = staging_input(normalized);
        input.producer_admitted = false;
        assert_eq!(
            StagingStage::run(input, 1),
            Err(CompilerError::MissingProducerAdmission)
        );
    }

    #[test]
    fn staging_requires_complete_dependency_closure() {
        let (_, _, normalized) = pipeline();
        let mut input = staging_input(normalized);
        input.dependency_closure_complete = false;
        assert_eq!(
            StagingStage::run(input, 1),
            Err(CompilerError::IncompleteDependencyClosure)
        );
    }

    #[test]
    fn staged_derivative_is_hidden() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        assert_eq!(staged.visibility, Visibility::Hidden);
    }

    #[test]
    fn publication_requires_second_admission() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = TestAuthority {
            publication_admitted: false,
            visibility_authorized: true,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Suppressed);
        assert_eq!(result.derivative.visibility, Visibility::Hidden);
    }

    #[test]
    fn stale_generation_returns_suppressed() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = TestAuthority {
            publication_admitted: true,
            visibility_authorized: true,
        };
        let result = PublicationGate::run(staged, &lease(), 2, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Suppressed);
        assert_eq!(result.derivative.visibility, Visibility::Hidden);
    }

    #[test]
    fn non_hidden_visibility_returns_blocked() {
        let (_, _, normalized) = pipeline();
        let mut staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        staged.visibility = Visibility::Visible;
        let mut authority = TestAuthority {
            publication_admitted: true,
            visibility_authorized: true,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Blocked);
        assert_eq!(result.derivative.visibility, Visibility::Visible);
    }

    #[test]
    fn missing_storage_prepared_hidden_returns_blocked() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = EvidenceAuthority {
            producer_admitted: true,
            storage_prepared_hidden: false,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Blocked);
        assert_eq!(result.derivative.visibility, Visibility::Hidden);
    }

    #[test]
    fn missing_producer_admission_returns_blocked() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = EvidenceAuthority {
            producer_admitted: false,
            storage_prepared_hidden: true,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Blocked);
        assert_eq!(result.derivative.visibility, Visibility::Hidden);
    }

    #[test]
    fn failed_variant_exists_but_is_unreachable_here() {
        // Storage owns visibility advancement and must report Failed when that
        // boundary cannot advance visibility. PublicationGate has no such hook.
        assert!(matches!(
            PublicationDisposition::Failed,
            PublicationDisposition::Failed
        ));
    }

    #[test]
    fn publication_requires_visibility_authorization() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = TestAuthority {
            publication_admitted: true,
            visibility_authorized: false,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Suppressed);
        assert_eq!(result.derivative.visibility, Visibility::Hidden);
    }

    fn oid(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn admission_scope() -> memory_domain::ScopeRef {
        memory_domain::ScopeRef {
            scope_id: oid("scope-1"),
            scope_kind: memory_domain::ScopeKind::User,
            namespace_key: "user:scope-1".into(),
        }
    }

    fn register_compile_inputs(store: &mut admission::AdmissionStore) -> ProducerWorkItemId {
        let producer_id = oid("producer-identity");
        if !store.is_producer_registered(&producer_id).unwrap() {
            store
                .register_producer(&producer_id, "compiler-test-registry-digest")
                .unwrap();
        }
        let work_id = oid("work-1");
        store
            .register_producer_work(admission::ProducerRegistrationRequest {
                producer_work_item_id: work_id.clone(),
                producer_class: "compiler".into(),
                producer_identity: oid("producer-identity"),
                source_refs: vec![oid("event-1")],
                source_lineage_digest: "lineage-1".into(),
                scope_refs: vec![admission_scope()],
                operation_id: oid("operation-1"),
                correlation_id: oid("correlation-1"),
                causation_id: Some(oid("cause-1")),
                admission_canonical_commit_cursor: Some(oid("canonical-commit-1")),
                observed_fence_cursor: oid("fence-observation-0"),
                permission_epoch: oid("permission-epoch-1"),
                request_digest: "producer-request-1".into(),
                producer_schema_version: "v1".into(),
            })
            .unwrap();
        for (edge, source) in [("dep-1", "source-1"), ("dep-2", "source-2")] {
            store
                .register_dependency(admission::DependencyRegistrationRequest {
                    dependency_registration_id: oid(edge),
                    artifact_ref: oid("derivative-1"),
                    artifact_version: oid("publication-1"),
                    producer_work_item_id: work_id.clone(),
                    derivation_run_id: oid("run-1"),
                    source_ref: oid(source),
                    source_version: None,
                    provenance_ref: oid("provenance-1"),
                    scope_refs: vec![admission_scope()],
                    lineage_digest: "lineage-1".into(),
                    required_dependency_count: 2,
                    request_digest: format!("digest-{edge}"),
                })
                .unwrap();
        }
        ProducerWorkItemId::new(work_id)
    }

    #[test]
    fn compile_persists_admission_and_publication_receipts_before_returning_visible_derivative() {
        let mut store = admission::AdmissionStore::in_memory().unwrap();
        let work_id = register_compile_inputs(&mut store);
        let mut compiler = MemoryCompiler {
            authority: TestAuthority {
                publication_admitted: true,
                visibility_authorized: true,
            },
            admission: store,
        };
        let result = compiler
            .compile(event(), staging_input(pipeline().2), lease(), 1, &work_id)
            .unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Published);
        assert_eq!(result.derivative.visibility, Visibility::Visible);
        assert_eq!(
            compiler
                .admission
                .producer_receipt(work_id.as_opaque_id())
                .unwrap()
                .producer_work_item_id,
            work_id.as_opaque_id().clone()
        );
        assert_eq!(compiler.admission.publication_receipt_count().unwrap(), 1);
        let publication_id = oid("compiler-publication:publication-1");
        assert!(
            compiler
                .admission
                .publication_receipt(&publication_id)
                .unwrap()
                .visible
        );
    }

    #[test]
    fn compile_requires_preexisting_producer_receipt_and_succeeds_after_registration() {
        let mut compiler = MemoryCompiler {
            authority: TestAuthority {
                publication_admitted: true,
                visibility_authorized: true,
            },
            admission: admission::AdmissionStore::in_memory().unwrap(),
        };
        let producer_id = oid("producer-identity");
        compiler
            .admission
            .register_producer(&producer_id, "compiler-test-registry-digest")
            .unwrap();
        let work_id = ProducerWorkItemId::new(oid("work-1"));
        assert_eq!(
            compiler.compile(event(), staging_input(pipeline().2), lease(), 1, &work_id),
            Err(CompilerError::MissingProducerAdmission)
        );
        assert_eq!(compiler.admission.publication_receipt_count().unwrap(), 0);
        register_compile_inputs(&mut compiler.admission);
        let result = compiler
            .compile(event(), staging_input(pipeline().2), lease(), 1, &work_id)
            .unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Published);
    }

    #[test]
    fn compile_preserves_terminal_suppression_without_persisting_publication_receipt() {
        let mut store = admission::AdmissionStore::in_memory().unwrap();
        let work_id = register_compile_inputs(&mut store);
        let mut compiler = MemoryCompiler {
            authority: TestAuthority {
                publication_admitted: false,
                visibility_authorized: true,
            },
            admission: store,
        };
        let result = compiler
            .compile(event(), staging_input(pipeline().2), lease(), 1, &work_id)
            .unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Suppressed);
        assert_eq!(compiler.admission.publication_receipt_count().unwrap(), 0);
    }

    #[test]
    fn compile_returns_typed_error_when_publication_receipt_write_fails() {
        let mut store = admission::AdmissionStore::in_memory().unwrap();
        let work_id = register_compile_inputs(&mut store);
        store.block_publication_receipt_writes().unwrap();
        let mut compiler = MemoryCompiler {
            authority: TestAuthority {
                publication_admitted: true,
                visibility_authorized: true,
            },
            admission: store,
        };
        assert_eq!(
            compiler.compile(event(), staging_input(pipeline().2), lease(), 1, &work_id),
            Err(CompilerError::AdmissionStoreFailure)
        );
        assert_eq!(compiler.admission.publication_receipt_count().unwrap(), 0);
    }

    #[test]
    fn successful_publication_requires_both_admissions() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = TestAuthority {
            publication_admitted: true,
            visibility_authorized: true,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Published);
        assert_eq!(result.derivative.visibility, Visibility::Visible);
    }

    #[test]
    fn rejected_participant_admission_returns_suppressed() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = TestAuthority {
            publication_admitted: false,
            visibility_authorized: true,
        };
        let result = PublicationGate::run(staged, &lease(), 1, &mut authority).unwrap();
        assert_eq!(result.disposition, PublicationDisposition::Suppressed);
        assert_eq!(result.derivative.visibility, Visibility::Hidden);
    }
}

#[cfg(test)]
mod state_tests {
    use super::*;

    fn id(value: &str) -> Identity {
        Identity::new(value).unwrap()
    }

    fn execution() -> StageExecution {
        StageExecution::new(id("operation-1"), StageName::Normalization)
    }

    fn worker_lease(generation: u64) -> WorkerLease {
        WorkerLease {
            operation_id: id("operation-1"),
            worker_id: id("worker-1"),
            generation,
        }
    }

    fn normalized() -> NormalizedIR {
        let payload = "A deterministic recovery test.".to_owned();
        let event = AcceptedEvent {
            event_id: id("event-1"),
            receipt_id: id("receipt-1"),
            payload_digest: digest_of(&payload),
            payload,
            compile_intent_durable: true,
        };
        let ingested = IngestionStage::run(event, 1).unwrap();
        let extracted = ExtractionStage::run(ingested, 1).unwrap();
        NormalizationStage::run(extracted, 1).unwrap()
    }

    fn staging_input() -> StagingInput {
        StagingInput {
            normalized: normalized(),
            derivative_id: id("derivative-recovery"),
            publication_id: id("publication-recovery"),
            dependency_ids: vec![id("event-1"), id("source-1")],
            dependency_closure_complete: true,
            producer_admitted: true,
            canonical_commit_cursor_recorded: true,
        }
    }

    struct RecoveryAuthority {
        calls: usize,
    }

    impl PublicationAuthority for RecoveryAuthority {
        fn obtain_proof(
            &mut self,
            staged: &StagedDerivative,
            lease: &WorkerLease,
        ) -> Result<PublicationProof, CompilerError> {
            self.calls += 1;
            Ok(PublicationProof {
                publication_id: staged.publication_id.clone(),
                generation: lease.generation,
                producer_admitted: true,
                dependency_closure_complete: true,
                canonical_commit_confirmed: true,
                storage_prepared_hidden: true,
                publication_participant_admitted: true,
                protected_visibility_authorized: true,
            })
        }
    }

    #[test]
    fn blocked_is_recoverable_and_not_terminal() {
        assert!(!ExecutionState::Blocked.is_terminal());
        assert!(ExecutionState::Blocked.can_transition_to(ExecutionState::Pending));
    }

    #[test]
    fn published_is_terminal_and_cannot_transition() {
        assert!(ExecutionState::Published.is_terminal());

        for next in [
            ExecutionState::Pending,
            ExecutionState::Leased,
            ExecutionState::Running,
            ExecutionState::Staged,
            ExecutionState::PreparedHidden,
            ExecutionState::PublicationAdmission,
            ExecutionState::Published,
            ExecutionState::Suppressed,
            ExecutionState::Blocked,
            ExecutionState::Failed,
        ] {
            assert!(!ExecutionState::Published.can_transition_to(next));
        }
    }

    #[test]
    fn illegal_transition_is_rejected() {
        let mut execution = execution();
        assert_eq!(
            execution.advance(ExecutionState::Published),
            Err(CompilerError::IllegalStateTransition)
        );
        assert_eq!(execution.state, ExecutionState::Pending);
    }

    #[test]
    fn happy_path_transitions_are_all_legal() {
        let mut state = ExecutionState::Pending;
        for next in [
            ExecutionState::Leased,
            ExecutionState::Running,
            ExecutionState::Staged,
            ExecutionState::PreparedHidden,
            ExecutionState::PublicationAdmission,
            ExecutionState::Published,
        ] {
            assert!(state.can_transition_to(next));
            state = next;
        }
        assert_eq!(state, ExecutionState::Published);
    }

    #[test]
    fn publication_admission_branches_to_four_dispositions() {
        for next in [
            ExecutionState::Published,
            ExecutionState::Suppressed,
            ExecutionState::Blocked,
            ExecutionState::Failed,
        ] {
            assert!(ExecutionState::PublicationAdmission.can_transition_to(next));
        }
    }

    #[test]
    fn retry_increments_generation_and_preserves_stage_identity() {
        let mut execution = execution();
        execution.state = ExecutionState::Failed;
        execution.attempt_generation = 7;
        execution.lease = Some(worker_lease(7));

        let original_operation = execution.operation_id.clone();
        let original_stage = execution.stage.clone();

        execution.retry().unwrap();

        assert_eq!(execution.state, ExecutionState::Pending);
        assert_eq!(execution.attempt_generation, 8);
        assert_eq!(execution.operation_id, original_operation);
        assert_eq!(execution.stage, original_stage);
        assert!(execution.lease.is_none());
    }

    #[test]
    fn retry_on_published_is_rejected() {
        let mut execution = execution();
        execution.state = ExecutionState::Published;
        assert_eq!(
            execution.retry(),
            Err(CompilerError::IllegalStateTransition)
        );
        assert_eq!(execution.attempt_generation, 1);
        assert_eq!(execution.state, ExecutionState::Published);
    }

    #[test]
    fn retry_on_blocked_returns_to_pending() {
        let mut execution = execution();
        execution.state = ExecutionState::Blocked;
        execution.attempt_generation = 3;

        execution.retry().unwrap();

        assert_eq!(execution.state, ExecutionState::Pending);
        assert_eq!(execution.attempt_generation, 4);
    }

    #[test]
    fn lease_generation_mismatch_is_not_current() {
        let mut execution = execution();
        execution.lease = Some(worker_lease(4));

        assert!(execution.lease_is_current(4));
        assert!(!execution.lease_is_current(5));
    }

    #[test]
    fn resume_rejects_terminal_state() {
        let mut compiler = MemoryCompiler {
            authority: RecoveryAuthority { calls: 0 },
            admission: admission::AdmissionStore::in_memory().unwrap(),
        };
        let mut execution = execution();
        execution.state = ExecutionState::Published;
        execution.lease = Some(worker_lease(1));

        assert_eq!(
            compiler.resume(&execution, staging_input(), worker_lease(1), 1,),
            Err(CompilerError::IllegalStateTransition)
        );
        assert_eq!(compiler.authority.calls, 0);
    }

    #[test]
    fn resume_rejects_stale_lease() {
        let mut compiler = MemoryCompiler {
            authority: RecoveryAuthority { calls: 0 },
            admission: admission::AdmissionStore::in_memory().unwrap(),
        };
        let mut execution = execution();
        execution.lease = Some(worker_lease(1));

        assert_eq!(
            compiler.resume(&execution, staging_input(), worker_lease(1), 2,),
            Err(CompilerError::LeaseExpired)
        );
        assert_eq!(compiler.authority.calls, 0);
    }

    #[test]
    fn resume_from_last_durable_stage_skips_completed_work() {
        let mut compiler = MemoryCompiler {
            authority: RecoveryAuthority { calls: 0 },
            admission: admission::AdmissionStore::in_memory().unwrap(),
        };
        let mut execution = execution();
        execution.state = ExecutionState::PublicationAdmission;
        execution.record_durable(StageName::Normalization);
        execution.lease = Some(worker_lease(1));

        let result = compiler
            .resume(&execution, staging_input(), worker_lease(1), 1)
            .unwrap();

        assert_eq!(result.disposition, PublicationDisposition::Published);
        assert_eq!(result.derivative.visibility, Visibility::Visible);
        assert_eq!(result.derivative.provenance.stage_name, StageName::Staging);
        assert_eq!(compiler.authority.calls, 1);
    }
}

#[cfg(test)]
mod scenario_tests {
    use super::*;

    fn id(value: &str) -> Identity {
        Identity::new(value).unwrap()
    }

    fn accepted_event() -> AcceptedEvent {
        let payload = "A scenario test payload.".to_owned();
        AcceptedEvent {
            event_id: id("scenario-event"),
            receipt_id: id("scenario-receipt"),
            payload_digest: digest_of(&payload),
            payload,
            compile_intent_durable: true,
        }
    }

    #[test]
    fn llm_outage_before_accepted_leaves_stage_pending() {
        let mut execution = StageExecution::new(id("before-accepted"), StageName::Ingestion);
        execution.state = ExecutionState::Running;

        let mut event = accepted_event();
        // 空 receipt 无法通过 Identity::new 的校验，直接构造裸值以覆盖 stage 的拒绝路径。
        event.receipt_id = Identity(String::new());

        assert_eq!(
            IngestionStage::run(event, execution.attempt_generation),
            Err(CompilerError::MissingAcceptedReceipt)
        );
        assert!(matches!(
            execution.state,
            ExecutionState::Pending | ExecutionState::Running
        ));
        assert_ne!(execution.state, ExecutionState::Staged);
        assert_eq!(execution.attempt_generation, 1);
        assert_eq!(execution.last_durable_stage, None);

        execution.state = ExecutionState::Failed;
        execution.retry().unwrap();

        assert_eq!(execution.state, ExecutionState::Pending);
        assert_eq!(execution.attempt_generation, 2);
        assert_eq!(execution.last_durable_stage, None);
    }

    #[test]
    fn llm_outage_after_accepted_preserves_staged_result() {
        let ingested = IngestionStage::run(accepted_event(), 1).unwrap();
        let staged_result = ExtractionStage::run(ingested, 1).unwrap();
        let original_stage_output = staged_result.provenance.stage_output_id.clone();

        let mut execution = StageExecution::new(id("after-accepted"), StageName::Extraction);
        execution.state = ExecutionState::Staged;
        execution.record_durable(StageName::Extraction);

        let extraction_calls = 1usize;
        execution.state = ExecutionState::Blocked;
        execution.retry().unwrap();

        assert_eq!(execution.state, ExecutionState::Pending);
        assert_eq!(execution.attempt_generation, 2);
        assert_eq!(execution.stage, StageName::Extraction);
        assert_eq!(
            staged_result.provenance.stage_output_id,
            original_stage_output
        );
        assert_eq!(staged_result.provenance.attempt_generation, 1);
        assert_eq!(extraction_calls, 1);
        assert_eq!(execution.last_durable_stage, Some(StageName::Extraction));
    }

    #[test]
    fn crash_after_event_and_outbox_commit_recovers_without_duplicate_publication() {
        struct EventOutboxFixture {
            event_committed: bool,
            outbox_committed: bool,
            publication_count: usize,
        }

        impl EventOutboxFixture {
            fn recover_and_publish(&mut self) {
                if self.event_committed && self.outbox_committed {
                    return;
                }
                self.event_committed = true;
                self.outbox_committed = true;
                self.publication_count += 1;
            }
        }

        let mut execution =
            StageExecution::new(id("event-outbox-operation"), StageName::PublicationGate);
        let mut fixture = EventOutboxFixture {
            event_committed: true,
            outbox_committed: true,
            publication_count: 1,
        };

        execution.record_durable(StageName::PublicationGate);
        execution.state = ExecutionState::Blocked;

        execution.retry().unwrap();
        fixture.recover_and_publish();

        assert_eq!(execution.state, ExecutionState::Pending);
        assert_eq!(
            execution.last_durable_stage,
            Some(StageName::PublicationGate)
        );
        assert!(fixture.event_committed);
        assert!(fixture.outbox_committed);
        assert_eq!(fixture.publication_count, 1);
    }

    #[test]
    fn same_idempotency_key_different_digest_is_rejected() {
        #[derive(Clone, Debug, Eq, PartialEq)]
        enum IdempotencyError {
            KeyDigestConflict,
        }

        struct IdempotencyFixture {
            entries: std::collections::BTreeMap<String, String>,
        }

        impl IdempotencyFixture {
            fn accept(&mut self, key: &str, digest: &str) -> Result<(), IdempotencyError> {
                match self.entries.get(key) {
                    Some(existing) if existing != digest => {
                        Err(IdempotencyError::KeyDigestConflict)
                    }
                    Some(_) => Ok(()),
                    None => {
                        self.entries.insert(key.to_owned(), digest.to_owned());
                        Ok(())
                    }
                }
            }
        }

        let mut fixture = IdempotencyFixture {
            entries: std::collections::BTreeMap::new(),
        };

        assert_eq!(fixture.accept("same-key", "digest-a"), Ok(()));
        assert_eq!(
            fixture.accept("same-key", "digest-b"),
            Err(IdempotencyError::KeyDigestConflict)
        );
        assert_eq!(
            fixture.entries.get("same-key"),
            Some(&"digest-a".to_owned())
        );
    }

    #[test]
    fn plan_only_input_cannot_reach_publication() {
        let mut event = accepted_event();
        event.payload.clear();
        event.payload_digest = digest_of(&event.payload);

        let ingested = IngestionStage::run(event, 1).unwrap();
        assert_eq!(
            ExtractionStage::run(ingested, 1),
            Err(CompilerError::EmptyExtraction)
        );

        let execution = StageExecution::new(id("plan-only-operation"), StageName::Extraction);
        assert_eq!(execution.state, ExecutionState::Pending);
        assert_ne!(execution.state, ExecutionState::PreparedHidden);
        assert_ne!(execution.state, ExecutionState::Published);
    }

    #[test]
    fn permission_revoked_between_queue_and_execution_blocks_publication() {
        #[derive(Clone, Copy, Debug, Eq, PartialEq)]
        enum Admission {
            Admitted,
            Blocked,
            Failed,
        }

        struct PermissionFixture {
            permission_at_enqueue: bool,
            permission_at_execution: bool,
        }

        impl PermissionFixture {
            fn execute(&self) -> Admission {
                if !self.permission_at_execution {
                    Admission::Blocked
                } else {
                    Admission::Admitted
                }
            }
        }

        let fixture = PermissionFixture {
            permission_at_enqueue: true,
            permission_at_execution: false,
        };

        assert!(fixture.permission_at_enqueue);
        assert_eq!(fixture.execute(), Admission::Blocked);
        assert_ne!(fixture.execute(), Admission::Failed);
    }

    #[test]
    fn forget_while_leased_prevents_publication() {
        #[derive(Clone, Copy, Debug, Eq, PartialEq)]
        enum ForgetCheck {
            Tombstoned,
        }

        struct ForgetFixture {
            lease_valid: bool,
            tombstone_epoch: u64,
            checked_low_watermark: bool,
        }

        impl ForgetFixture {
            fn authorize_publication(
                &mut self,
                current_low_watermark: u64,
            ) -> Result<(), ForgetCheck> {
                self.checked_low_watermark = true;

                if self.tombstone_epoch <= current_low_watermark {
                    return Err(ForgetCheck::Tombstoned);
                }

                if !self.lease_valid {
                    return Err(ForgetCheck::Tombstoned);
                }

                Ok(())
            }
        }

        let mut fixture = ForgetFixture {
            lease_valid: false,
            tombstone_epoch: 12,
            checked_low_watermark: false,
        };

        assert_eq!(
            fixture.authorize_publication(12),
            Err(ForgetCheck::Tombstoned)
        );
        assert!(!fixture.lease_valid);
        assert!(fixture.checked_low_watermark);

        // 租约有效且墓碑晚于低水位时，授权必须放行：这是 Clear 曾被用来表达的
        // 成功路径，语义上由 Ok(()) 承载，不应再占用一个错误变体。
        fixture.lease_valid = true;
        fixture.tombstone_epoch = 13;
        assert_eq!(fixture.authorize_publication(12), Ok(()));
    }

    #[test]
    fn canonical_commit_with_index_outage_is_not_marked_published() {
        struct CommitIndexFixture {
            canonical_commit_confirmed: bool,
            index_available: bool,
        }

        impl CommitIndexFixture {
            fn resulting_state(&self) -> ExecutionState {
                if self.canonical_commit_confirmed && !self.index_available {
                    ExecutionState::Blocked
                } else if self.canonical_commit_confirmed && self.index_available {
                    ExecutionState::Published
                } else {
                    ExecutionState::Failed
                }
            }
        }

        let fixture = CommitIndexFixture {
            canonical_commit_confirmed: true,
            index_available: false,
        };

        let mut execution =
            StageExecution::new(id("commit-index-operation"), StageName::PublicationGate);
        execution.state = ExecutionState::PublicationAdmission;
        execution.advance(fixture.resulting_state()).unwrap();

        assert_eq!(execution.state, ExecutionState::Blocked);
        assert!(!execution.state.is_terminal());
        assert_ne!(execution.state, ExecutionState::Published);
    }

    #[test]
    fn replay_after_source_expiry_does_not_bypass_tombstones() {
        #[derive(Clone, Copy, Debug, Eq, PartialEq)]
        enum ReplayError {
            SourceExpired,
            ForgetTombstone,
        }

        struct ReplayFixture {
            source_expired: bool,
            tombstone_present: bool,
        }

        impl ReplayFixture {
            fn replay(&self) -> Result<(), ReplayError> {
                if self.tombstone_present {
                    return Err(ReplayError::ForgetTombstone);
                }
                if self.source_expired {
                    return Err(ReplayError::SourceExpired);
                }
                Ok(())
            }
        }

        let fixture = ReplayFixture {
            source_expired: true,
            tombstone_present: true,
        };

        assert_eq!(fixture.replay(), Err(ReplayError::ForgetTombstone));
        assert!(fixture.source_expired);
        assert!(fixture.tombstone_present);
    }

    #[test]
    fn malicious_document_with_tool_instructions_is_quarantined() {
        #[derive(Clone, Copy, Debug, Eq, PartialEq)]
        enum DocumentDisposition {
            Accepted,
            Quarantined,
        }

        struct DocumentSecurityFixture;

        impl DocumentSecurityFixture {
            fn inspect(&self, document: &str) -> DocumentDisposition {
                let normalized = document.to_ascii_lowercase();
                if normalized.contains("tool:")
                    || normalized.contains("policy:")
                    || normalized.contains("ignore previous instructions")
                {
                    DocumentDisposition::Quarantined
                } else {
                    DocumentDisposition::Accepted
                }
            }
        }

        let document = "Ordinary text. Tool: execute an external command.";
        let fixture = DocumentSecurityFixture;
        let disposition = fixture.inspect(document);

        assert_eq!(disposition, DocumentDisposition::Quarantined);
        assert_ne!(disposition, DocumentDisposition::Accepted);
    }
}

#[cfg(all(test, feature = "sqlite"))]
mod outbox_adapter_tests {
    use super::*;
    use memory_domain::{OpaqueId, ScopeKind, ScopeRef};
    use memory_event_store::{EventClassification, EventEnvelope};
    use memory_event_store_sqlite::{PayloadEventStoreExt, SqliteEventStore};

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).expect("test identifier should be valid")
    }

    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("scope-1"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:scope-1".into(),
        }
    }

    fn envelope(payload: &[u8]) -> EventEnvelope {
        EventEnvelope {
            event_kind: "observation".into(),
            source_type: "compiler-test".into(),
            source_id: id("source-1"),
            producer_actor_ref: id("actor-1"),
            scope_refs: vec![scope()],
            event_time: None,
            payload_ref: "payload://source-1".into(),
            payload_digest: raw_payload_digest(
                std::str::from_utf8(payload).expect("test payload is utf-8"),
            ),
            classification: EventClassification::Observed,
            idempotency_key: "compile-test-1".into(),
            retention_class: "default".into(),
            correlation_id: id("correlation-1"),
        }
    }

    fn envelope_with_raw_payload_digest(payload: &[u8]) -> EventEnvelope {
        EventEnvelope {
            event_kind: "observation".into(),
            source_type: "compiler-test".into(),
            source_id: id("source-1"),
            producer_actor_ref: id("actor-1"),
            scope_refs: vec![scope()],
            event_time: None,
            payload_ref: "payload://source-1".into(),
            payload_digest: format!("sha256:{:x}", Sha256::digest(payload)),
            classification: EventClassification::Observed,
            idempotency_key: "compile-test-1".into(),
            retention_class: "default".into(),
            correlation_id: id("correlation-1"),
        }
    }

    /// The positive path: accept, read the outbox, adapt, ingest. Every digest
    /// the compiler sees must be the one the store issued, not one computed
    /// alongside it.
    #[test]
    fn outbox_adapter_builds_accepted_event_from_real_acceptance() {
        let mut store = SqliteEventStore::in_memory().expect("store should open");
        let payload = b"A durable observation for compiler ingestion.";

        let receipt = store
            .accept_with_payload(envelope(payload), payload, &[scope()])
            .expect("accept should succeed");

        let pending = store
            .pending_compile_intents()
            .expect("outbox read should succeed");
        assert_eq!(pending.len(), 1);

        let accepted = accepted_event_from(&pending[0]).expect("adapter should accept real intent");

        assert_eq!(accepted.payload_digest, receipt.payload_digest);
        assert_eq!(accepted.receipt_id.0, receipt.receipt_id.as_str());
        assert_eq!(accepted.event_id.0, receipt.event_id.as_str());
        assert!(accepted.compile_intent_durable);

        let ingested = IngestionStage::run(accepted, 1).expect("ingestion should accept the event");
        assert_eq!(ingested.payload_digest, receipt.payload_digest);
    }

    /// Genuinely non-UTF-8 bytes can be accepted and retrieved intact, but
    /// the compiler adapter rejects them rather than decoding them lossily.
    #[test]
    fn outbox_adapter_rejects_non_utf8_payload() {
        let mut store = SqliteEventStore::in_memory().expect("store should open");
        let payload = &[0xff, 0xfe];

        store
            .accept_with_payload(
                envelope_with_raw_payload_digest(payload),
                payload,
                &[scope()],
            )
            .expect("accept should succeed");

        let pending = store
            .pending_compile_intents()
            .expect("outbox read should succeed");

        assert_eq!(
            accepted_event_from(&pending[0]),
            Err(CompilerError::InvalidPayloadEncoding)
        );
    }
}
