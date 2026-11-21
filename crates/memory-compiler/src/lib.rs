//! Memory Compiler reference pipeline.
//! Pure Rust. No database, network, model-provider or authorization implementation.
//! Production authority integrations are explicit traits and remain unimplemented.

pub mod admission;

use std::collections::BTreeSet;

pub const COMPILER_VERSION: &str = "0.1.0";

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
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AcceptedEvent {
    pub event_id: Identity,
    pub receipt_id: Identity,
    pub payload_digest: String,
    pub payload: String,
    pub compile_intent_durable: bool,
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

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PublicationDisposition {
    Published,
    Suppressed,
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
    pub fn run(
        event: AcceptedEvent,
        generation: u64,
    ) -> Result<IngestedEvent, CompilerError> {
        if event.receipt_id.0.is_empty() {
            return Err(CompilerError::MissingAcceptedReceipt);
        }
        if !event.compile_intent_durable {
            return Err(CompilerError::MissingCompileIntent);
        }
        if event.payload_digest.trim().is_empty() {
            return Err(CompilerError::InvalidPayloadDigest);
        }

        let provenance = Provenance {
            source_event_id: event.event_id.clone(),
            source_payload_digest: event.payload_digest.clone(),
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
            payload_digest: event.payload_digest,
            payload: event.payload,
            provenance,
        })
    }
}

/// Deterministic reference extractor. It does not invoke an LLM.
pub struct ExtractionStage;

impl ExtractionStage {
    pub fn run(
        input: IngestedEvent,
        generation: u64,
    ) -> Result<ExtractionIR, CompilerError> {
        let segments: Vec<String> = input.payload
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
    pub fn run(
        input: ExtractionIR,
        generation: u64,
    ) -> Result<NormalizedIR, CompilerError> {
        let values: Vec<String> = input.segments
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
    pub canonical_commit_confirmed: bool,
}

pub struct StagingStage;

impl StagingStage {
    pub fn run(
        input: StagingInput,
        generation: u64,
    ) -> Result<StagedDerivative, CompilerError> {
        if !input.producer_admitted {
            return Err(CompilerError::MissingProducerAdmission);
        }
        if !input.dependency_closure_complete || input.dependency_ids.is_empty() {
            return Err(CompilerError::IncompleteDependencyClosure);
        }
        if !input.canonical_commit_confirmed {
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
            return Err(CompilerError::StaleWorker);
        }

        if staged.visibility != Visibility::Hidden {
            return Err(CompilerError::InvalidPublicationProof);
        }

        let proof = authority.obtain_proof(&staged, lease)?;

        if proof.publication_id != staged.publication_id
            || proof.generation != lease.generation
        {
            return Err(CompilerError::InvalidPublicationProof);
        }

        if !proof.producer_admitted
            || !proof.dependency_closure_complete
            || !proof.canonical_commit_confirmed
            || !proof.storage_prepared_hidden
        {
            return Err(CompilerError::InvalidPublicationProof);
        }

        if !proof.publication_participant_admitted
            || !proof.protected_visibility_authorized
        {
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

/// Reference pipeline: five explicit typed stages.
/// External authorities remain injected through PublicationAuthority.
pub struct MemoryCompiler<A> {
    pub authority: A,
}

impl<A: PublicationAuthority> MemoryCompiler<A> {
    pub fn compile(
        &mut self,
        event: AcceptedEvent,
        staging: StagingInput,
        lease: WorkerLease,
        current_generation: u64,
    ) -> Result<PublishedDerivative, CompilerError> {
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

        PublicationGate::run(
            staged,
            &lease,
            current_generation,
            &mut self.authority,
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(s: &str) -> Identity {
        Identity::new(s).unwrap()
    }

    fn event() -> AcceptedEvent {
        AcceptedEvent {
            event_id: id("event-1"),
            receipt_id: id("receipt-1"),
            payload_digest: "sha256:source".into(),
            payload: "I plan to move to Tokyo. I tried to deploy.".into(),
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
            canonical_commit_confirmed: true,
        }
    }

    struct TestAuthority {
        publication_admitted: bool,
        visibility_authorized: bool,
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
    fn late_worker_cannot_publish() {
        let (_, _, normalized) = pipeline();
        let staged = StagingStage::run(staging_input(normalized), 1).unwrap();
        let mut authority = TestAuthority {
            publication_admitted: true,
            visibility_authorized: true,
        };
        assert_eq!(
            PublicationGate::run(staged, &lease(), 2, &mut authority),
            Err(CompilerError::StaleWorker)
        );
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
}