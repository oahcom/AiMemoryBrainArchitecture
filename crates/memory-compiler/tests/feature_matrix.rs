//! The five pure pipeline stages must be usable with no admission ledger.
//!
//! `memory-compiler`'s `default` feature pulls `rusqlite` with `bundled`, which
//! needs a C compiler. The stages themselves never touch the ledger, so this
//! file drives all five of them end to end under `--no-default-features` and
//! proves the C-free build exposes a working pipeline rather than an empty
//! shell. The sqlite-only orchestrator is covered in the crate's own tests.

use memory_compiler::{
    AcceptedEvent, CompilerError, ExtractionStage, Identity, IngestionStage, NormalizationStage,
    PublicationAuthority, PublicationDisposition, PublicationGate, PublicationProof, StagingInput,
    StagingStage, Visibility, WorkerLease,
};

fn id(value: &str) -> Identity {
    Identity::new(value).expect("test identities are non-empty")
}

fn lease(generation: u64) -> WorkerLease {
    WorkerLease {
        operation_id: id("op-1"),
        worker_id: id("worker-1"),
        generation,
    }
}

fn proof(staged: &memory_compiler::StagedDerivative, lease: &WorkerLease) -> PublicationProof {
    PublicationProof {
        publication_id: staged.publication_id.clone(),
        generation: lease.generation,
        producer_admitted: true,
        dependency_closure_complete: true,
        canonical_commit_confirmed: true,
        storage_prepared_hidden: true,
        publication_participant_admitted: true,
        protected_visibility_authorized: true,
    }
}

/// A caller-provided authority: exactly what the trait doc warns is not
/// production evidence, and exactly what a C-free build must still accept.
struct StubAuthority;

impl PublicationAuthority for StubAuthority {
    fn obtain_proof(
        &mut self,
        staged: &memory_compiler::StagedDerivative,
        lease: &WorkerLease,
    ) -> Result<PublicationProof, CompilerError> {
        Ok(proof(staged, lease))
    }
}

fn accepted_event() -> AcceptedEvent {
    AcceptedEvent {
        event_id: id("event-1"),
        receipt_id: id("receipt-1"),
        payload_digest: "sha256:6c6885d7d1b77faf059ec91410374c984456b0dff2dcdb268f63b50cff0c25f0"
            .into(),
        payload: "First sentence. Second sentence! Third one?".into(),
        compile_intent_durable: true,
    }
}

fn staging_input(normalized: memory_compiler::NormalizedIR) -> StagingInput {
    StagingInput {
        normalized,
        derivative_id: id("derivative-1"),
        publication_id: id("publication-1"),
        dependency_ids: vec![id("dependency-1")],
        dependency_closure_complete: true,
        producer_admitted: true,
        canonical_commit_cursor_recorded: true,
    }
}

#[test]
fn all_five_stages_run_end_to_end_without_an_admission_ledger() {
    let generation = 1;

    let ingested = IngestionStage::run(accepted_event(), generation).expect("ingest");
    let extracted = ExtractionStage::run(ingested, generation).expect("extract");
    let normalized = NormalizationStage::run(extracted, generation).expect("normalize");
    let staged = StagingStage::run(staging_input(normalized), generation).expect("stage");

    // Staging leaves the derivative hidden: nothing is visible before the gate.
    assert_eq!(staged.visibility, Visibility::Hidden);

    let published =
        PublicationGate::run(staged, &lease(generation), generation, &mut StubAuthority)
            .expect("publish");

    assert_eq!(published.disposition, PublicationDisposition::Published);
    assert_eq!(published.derivative.visibility, Visibility::Visible);
}

#[test]
fn a_stale_generation_is_suppressed_and_never_reaches_visible() {
    let generation = 1;

    let ingested = IngestionStage::run(accepted_event(), generation).unwrap();
    let extracted = ExtractionStage::run(ingested, generation).unwrap();
    let normalized = NormalizationStage::run(extracted, generation).unwrap();
    let staged = StagingStage::run(staging_input(normalized), generation).unwrap();

    // The lease belongs to an older generation than the caller's current one.
    let published = PublicationGate::run(
        staged,
        &lease(generation),
        generation + 1,
        &mut StubAuthority,
    )
    .unwrap();

    assert_eq!(published.disposition, PublicationDisposition::Suppressed);
    assert_ne!(published.derivative.visibility, Visibility::Visible);
}

#[test]
fn a_missing_dependency_closure_is_rejected_before_staging() {
    let generation = 1;

    let ingested = IngestionStage::run(accepted_event(), generation).unwrap();
    let extracted = ExtractionStage::run(ingested, generation).unwrap();
    let normalized = NormalizationStage::run(extracted, generation).unwrap();

    let mut input = staging_input(normalized);
    input.dependency_closure_complete = false;

    assert_eq!(
        StagingStage::run(input, generation),
        Err(CompilerError::IncompleteDependencyClosure)
    );
}

#[test]
fn a_non_durable_compile_intent_is_rejected_at_ingestion() {
    let mut event = accepted_event();
    event.compile_intent_durable = false;

    assert_eq!(
        IngestionStage::run(event, 1),
        Err(CompilerError::MissingCompileIntent)
    );
}
