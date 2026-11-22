use agent_integration::{
    ApplyOutcome, ContextDeliveryAdapter, DeliveryPayload, FileContextDeliveryAdapter,
    InMemoryContextDeliveryAdapter,
};
use memory_compiler::admission::{
    rfc3339_utc_now, AdmissionStore, DependencyRegistrationRequest, ProducerRegistrationRequest,
};
use memory_compiler::publication_authority::AdmissionPublicationAuthority;
use memory_compiler::{
    accepted_event_from, canonical_subject_digest, ExtractionStage, Identity, IngestionStage,
    MemoryCompiler, NormalizationStage, ProducerWorkItemId, PublicationAuthority,
    PublicationDisposition, PublicationProof, StagingInput, StagingStage, WorkerLease,
    COMPILER_VERSION,
};
use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextTier,
};
use memory_domain::{
    CanonicalCommitRef, Claim, Event, IssuerId, Memory, MemoryLifecycle, MemoryVersion, OpaqueId,
    ScopeRef, DEV_BASELINE_ISSUER,
};
use memory_event_store::{EventClassification, EventEnvelope};
use memory_event_store_sqlite::{PayloadEventStoreExt, SqliteEventStore};
use memory_storage::{MemoryStorage, PrepareRequest};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, RevisionWrite};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};

/// Generation used for the single compiler attempt this binary makes.
const COMPILER_GENERATION: u64 = 1;

#[derive(Deserialize)]
struct Input {
    event: Event,
    /// Raw source payload. The domain Event keeps its payload reference separately.
    payload: String,
    memory: MemoryInput,
    claim: Claim,
    context: ContextInput,
}

#[derive(Deserialize)]
struct MemoryInput {
    memory_id: OpaqueId,
    memory_version_id: OpaqueId,
    memory_kind: String,
    lifecycle_state: MemoryLifecycle,
    retention_class: String,
    sensitivity: String,
    created_at: String,
    updated_at: String,
    version_created_at: String,
    author_kind: String,
    change_reason: String,
    schema_version: String,
}

#[derive(Deserialize)]
struct ContextInput {
    context_id: OpaqueId,
    agent_id: OpaqueId,
    agent_instance_id: OpaqueId,
    session_id: OpaqueId,
    task_id: Option<OpaqueId>,
    environment_id: Option<OpaqueId>,
    purpose: String,
    schema_version: String,
}

struct TemporaryDatabase(PathBuf);

impl TemporaryDatabase {
    fn new(label: &str) -> Self {
        Self(std::env::temp_dir().join(format!("brain-cli-{label}-{}.sqlite", std::process::id())))
    }

    fn path(&self) -> &Path {
        &self.0
    }
}

impl Drop for TemporaryDatabase {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.0);
        let _ = fs::remove_file(self.0.with_extension("sqlite-wal"));
        let _ = fs::remove_file(self.0.with_extension("sqlite-shm"));
    }
}

fn main() {
    if let Err(error) = run() {
        eprintln!("brain: {error}");
        std::process::exit(1);
    }
}

/// Everything the compiler stage needs from the CLI input. The derivative is
/// staged hidden in storage before the gate runs, so the proof can report the
/// durable preparation state instead of guessing it.
struct CompilerStageRequest<'a> {
    /// The row read back out of `compile_outbox`. The compiler input is built
    /// from this and nothing else, so `compile_intent_durable` is a fact about
    /// the database rather than a flag the caller sets.
    intent: &'a memory_event_store_sqlite::PendingCompileIntent,
    event_id: &'a OpaqueId,
    source_ref: &'a OpaqueId,
    scope: &'a [ScopeRef],
    source_version_id: &'a OpaqueId,
    derivative_version: MemoryVersion,
    publication_id: &'a str,
    storage_path: &'a Path,
    admission_path: &'a Path,
    /// Issue a durable dev-baseline canonical commit record for this run's
    /// derivative. Off by default so the ordinary path keeps the legacy pending
    /// reference and the unchanged `blocked` disposition.
    issue_canonical_commit: bool,
}

struct CompilerStageOutcome {
    disposition: PublicationDisposition,
    proof: PublicationProof,
}

impl CompilerStageOutcome {
    /// A single line naming the disposition and, when publication is refused,
    /// the flag that caused it. Three flags have no authoritative issuer yet
    /// (OWNER-DECISION-PUBLICATION-RECORD-001 D3), so `Blocked` is the expected
    /// outcome of a real run.
    fn notice(&self) -> String {
        let false_flags = false_flags(&self.proof);
        let blocking = false_flags.first().copied().unwrap_or("none");
        match self.disposition {
            PublicationDisposition::Published => {
                "compiler stage published: all eight publication flags are true".to_owned()
            }
            PublicationDisposition::Blocked => format!(
                "compiler stage blocked: publication not authorized; blocking flag: {blocking}; false flags: [{}]",
                false_flags.join(", ")
            ),
            PublicationDisposition::Suppressed => format!(
                "compiler stage suppressed: publication not authorized; blocking flag: {blocking}; false flags: [{}]",
                false_flags.join(", ")
            ),
            PublicationDisposition::Failed => {
                "compiler stage failed: storage visibility advancement failed".to_owned()
            }
        }
    }
}

/// The eight proof flags in the order `PublicationGate` evaluates them, so the
/// first `false` entry is exactly the flag that produced the disposition.
fn false_flags(proof: &PublicationProof) -> Vec<&'static str> {
    [
        ("producer_admitted", proof.producer_admitted),
        (
            "dependency_closure_complete",
            proof.dependency_closure_complete,
        ),
        (
            "canonical_commit_confirmed",
            proof.canonical_commit_confirmed,
        ),
        ("storage_prepared_hidden", proof.storage_prepared_hidden),
        (
            "publication_participant_admitted",
            proof.publication_participant_admitted,
        ),
        (
            "protected_visibility_authorized",
            proof.protected_visibility_authorized,
        ),
    ]
    .into_iter()
    .filter(|(_, value)| !value)
    .map(|(name, _)| name)
    .collect()
}

fn event_classification(value: &str) -> EventClassification {
    match value.to_ascii_lowercase().as_str() {
        "observed" => EventClassification::Observed,
        "reported" => EventClassification::Reported,
        "planned" => EventClassification::Planned,
        "predicted" => EventClassification::Predicted,
        "attempted" => EventClassification::Attempted,
        "outcome" => EventClassification::Outcome,
        "administrative" => EventClassification::Administrative,
        _ => EventClassification::Unknown,
    }
}

fn identifier(value: impl Into<String>) -> Result<OpaqueId, String> {
    OpaqueId::new(value).map_err(|error| format!("invalid identifier: {error:?}"))
}

/// Runs the compiler publication stage through the production adapter.
///
/// This seeds the local admission ledger and stages the derivative hidden, then
/// lets `MemoryCompiler::compile` decide. Publication itself is expected to be
/// refused: the adapter may not authorize what no issuer has authorized.
///
/// Storage and admission are process-scoped. `storage_path` and `admission_path`
/// are supplied by the caller as `TemporaryDatabase` files, which are removed in
/// `Drop`, so every compile result in this binary is deliberately ephemeral. The
/// durable boundary here is event acceptance and outbox delivery, not the
/// compiler's output; persisting a compile result is outside this binary's
/// contract. An Owner ruling on 2026-11-22 settled this: no cursor table, no
/// `compiled_at` column, and no durable storage flags are required, and the
/// "who owns compile progress" question is not applicable to `brain-cli`.
///
/// `Blocked` is therefore the normal outcome, not an unfinished hook.
fn run_compiler_stage(request: CompilerStageRequest<'_>) -> Result<CompilerStageOutcome, String> {
    let event_id = request.event_id.as_str();
    let work_item_id = ProducerWorkItemId::new(identifier(format!("work:{event_id}"))?);
    let producer_identity = identifier("producer:brain-cli")?;

    let storage = {
        let mut storage = SqliteMemoryStorage::open(request.storage_path)
            .map_err(|error| format!("cannot open SQLite storage: {error:?}"))?;
        storage
            .prepare_version(
                PrepareRequest {
                    memory_id: request.derivative_version.memory_id.clone(),
                    expected_current_version: Some(request.source_version_id.clone()),
                    new_version: request.derivative_version,
                    idempotency_key: format!("prepare:{event_id}"),
                    request_digest: format!("prepare-digest:{event_id}"),
                    publication_id: request.publication_id.to_owned(),
                    generation: COMPILER_GENERATION,
                },
                request.scope,
            )
            .map_err(|error| format!("prepare_version failed: {error:?}"))?;
        storage
    };

    let mut admission = AdmissionStore::open(request.admission_path)
        .map_err(|error| format!("cannot open admission ledger: {error}"))?;
    // Built from the outbox row, not assembled here. Before this the CLI
    // computed its own digest and hard-coded `compile_intent_durable: true`,
    // which meant `IngestionStage::run`'s durable-intent guard could never fire
    // on the production path.
    let accepted = accepted_event_from(request.intent)
        .map_err(|error| format!("invalid pending compile intent: {error:?}"))?;
    let normalized = {
        let ingested = IngestionStage::run(accepted.clone(), COMPILER_GENERATION)
            .map_err(|error| format!("ingestion stage failed: {error:?}"))?;
        let extracted = ExtractionStage::run(ingested, COMPILER_GENERATION)
            .map_err(|error| format!("extraction stage failed: {error:?}"))?;
        NormalizationStage::run(extracted, COMPILER_GENERATION)
            .map_err(|error| format!("normalization stage failed: {error:?}"))?
    };
    let staging = StagingInput {
        normalized,
        derivative_id: Identity(format!("derivative:{event_id}")),
        publication_id: Identity(request.publication_id.to_owned()),
        // Admission booleans and dependency ids are derived from the durable
        // ledger inside `compile`; these placeholders are overwritten there.
        dependency_ids: Vec::new(),
        dependency_closure_complete: false,
        producer_admitted: false,
        canonical_commit_cursor_recorded: false,
    };
    // The dev-baseline issuer writes one durable record for exactly the
    // derivative this run stages. Staging is deterministic, so the preview below
    // produces the same provenance `compile` re-derives; the record commits
    // before the reference is handed to the request. Without the flag the run
    // carries the legacy pending reference, which never validates.
    let (cursor, reference) = if request.issue_canonical_commit {
        let preview = StagingStage::run(
            StagingInput {
                dependency_ids: vec![Identity(request.source_ref.as_str().to_owned())],
                dependency_closure_complete: true,
                producer_admitted: true,
                canonical_commit_cursor_recorded: true,
                ..staging.clone()
            },
            COMPILER_GENERATION,
        )
        .map_err(|error| format!("staging preview failed: {error:?}"))?;
        let subject = canonical_subject_digest(&preview.provenance)
            .map_err(|error| format!("cannot derive canonical subject digest: {error:?}"))?;
        let commit_id = identifier(format!("canonical-commit:{event_id}"))?;
        let issued = admission
            .issue_canonical_commit(
                &commit_id,
                &IssuerId::new(DEV_BASELINE_ISSUER)
                    .map_err(|error| format!("invalid issuer: {error:?}"))?,
                &subject,
                &rfc3339_utc_now(),
            )
            .map_err(|error| format!("issue_canonical_commit failed: {error}"))?;
        (commit_id, issued)
    } else {
        (
            identifier(format!("canonical-commit:{event_id}"))?,
            CanonicalCommitRef::pending_d(),
        )
    };

    admission
        .register_producer(&producer_identity, "brain-cli-registry-digest")
        .map_err(|error| format!("register_producer failed: {error}"))?;
    admission
        .register_producer_work(ProducerRegistrationRequest {
            producer_work_item_id: work_item_id.as_opaque_id().clone(),
            producer_class: "compiler".into(),
            producer_identity: producer_identity.clone(),
            source_refs: vec![request.source_ref.clone()],
            source_lineage_digest: format!("lineage:{event_id}"),
            scope_refs: request.scope.to_vec(),
            operation_id: identifier(format!("operation:{event_id}"))?,
            correlation_id: identifier(format!("correlation:{event_id}"))?,
            causation_id: None,
            admission_canonical_commit_cursor: Some(cursor),
            canonical_commit_ref: reference,
            observed_fence_cursor: identifier("fence:0")?,
            permission_epoch: identifier("permission-epoch:1")?,
            request_digest: format!("producer-request:{event_id}"),
            producer_schema_version: "1".into(),
        })
        .map_err(|error| format!("register_producer_work failed: {error}"))?;
    admission
        .register_dependency(DependencyRegistrationRequest {
            dependency_registration_id: identifier(format!("dependency:{event_id}"))?,
            artifact_ref: identifier(format!("derivative:{event_id}"))?,
            artifact_version: identifier(request.publication_id.to_owned())?,
            producer_work_item_id: work_item_id.as_opaque_id().clone(),
            derivation_run_id: identifier(format!("run:{event_id}"))?,
            source_ref: request.source_ref.clone(),
            source_version: None,
            provenance_ref: identifier(format!("provenance:{event_id}"))?,
            scope_refs: request.scope.to_vec(),
            lineage_digest: format!("lineage:{event_id}"),
            required_dependency_count: 1,
            request_digest: format!("dependency-request:{event_id}"),
        })
        .map_err(|error| format!("register_dependency failed: {error}"))?;

    // The adapter reads committed rows through its own handle; it never writes.
    let authority_admission = AdmissionStore::open(request.admission_path)
        .map_err(|error| format!("cannot open admission ledger: {error}"))?;
    let authority =
        AdmissionPublicationAuthority::new(authority_admission, &storage, work_item_id.clone());

    let lease = WorkerLease {
        operation_id: Identity(format!("operation:{event_id}")),
        worker_id: Identity("brain-cli-worker".into()),
        generation: COMPILER_GENERATION,
    };

    let mut compiler = MemoryCompiler {
        authority,
        admission,
    };
    let outcome = compiler
        .compile(
            accepted,
            staging,
            lease.clone(),
            COMPILER_GENERATION,
            &work_item_id,
        )
        .map_err(|error| format!("compiler stage failed: {error:?}"))?;
    let proof = compiler
        .authority
        .obtain_proof(&outcome.derivative, &lease)
        .map_err(|error| format!("publication proof unavailable: {error:?}"))?;

    Ok(CompilerStageOutcome {
        disposition: outcome.disposition,
        proof,
    })
}

/// Deliver a validated Brain context snapshot to the local Agent adapter.
///
/// Independent of compiler publication authorization: the adapter receives the
/// context snapshot, not the publication decision. The adapter is injected so
/// the caller owns its lifetime and persistence.
fn deliver_snapshot(
    adapter: &mut dyn ContextDeliveryAdapter,
    session_id: &str,
    snapshot: &memory_context::ContextSnapshot,
) -> Result<u64, String> {
    let payload = DeliveryPayload::from_snapshot(snapshot)
        .map_err(|error| format!("cannot construct delivery payload: {error:?}"))?;

    let expected_version = snapshot.context_version;

    match adapter
        .apply(session_id, payload)
        .map_err(|error| format!("adapter apply failed: {error:?}"))?
    {
        ApplyOutcome::Applied | ApplyOutcome::AlreadyApplied => {}
    }

    let applied = adapter
        .applied_snapshot(session_id)
        .ok_or_else(|| "adapter has no applied snapshot after apply".to_owned())?;

    if applied.version() != expected_version {
        return Err(format!(
            "adapter version mismatch: expected {expected_version}, got {}",
            applied.version()
        ));
    }

    Ok(applied.version())
}

/// Select the delivery adapter for this process.
///
/// A `--delivery-root` selects the file-backed adapter, so an applied delivery
/// survives the process; without one the run stays in memory.
fn delivery_adapter(
    delivery_root: Option<&Path>,
) -> Result<Box<dyn ContextDeliveryAdapter>, String> {
    match delivery_root {
        Some(root) => FileContextDeliveryAdapter::open(root)
            .map(|adapter| Box::new(adapter) as Box<dyn ContextDeliveryAdapter>)
            .map_err(|error| format!("cannot open delivery root {}: {error:?}", root.display())),
        None => Ok(Box::new(InMemoryContextDeliveryAdapter::default())),
    }
}

fn run() -> Result<(), String> {
    let mut args = std::env::args().skip(1);
    let Some(command) = args.next() else {
        return Err(usage());
    };
    if command != "compile" {
        return Err(usage());
    }

    let mut input_path = None;
    let mut output_path = None;
    let mut event_store_path: Option<PathBuf> = None;
    let mut delivery_root: Option<PathBuf> = None;
    let mut verbose = false;
    let mut issue_canonical_commit = false;

    while let Some(argument) = args.next() {
        match argument.as_str() {
            "--input" => input_path = args.next(),
            "--out" => output_path = args.next(),
            "--event-store" => {
                event_store_path = Some(
                    args.next()
                        .ok_or_else(|| "--event-store requires a path".to_owned())?
                        .into(),
                );
            }
            "--delivery-root" => {
                delivery_root = Some(
                    args.next()
                        .ok_or_else(|| "--delivery-root requires a path".to_owned())?
                        .into(),
                );
            }
            "--verbose" => verbose = true,
            // Dev-baseline issuance. Without it the run keeps the legacy pending
            // reference and the unchanged `blocked` disposition.
            "--canonical-commit" => issue_canonical_commit = true,
            _ => return Err(format!("unknown argument: {argument}\n{}", usage())),
        }
    }

    let input_path = input_path.ok_or_else(usage)?;
    let output_path = output_path.ok_or_else(usage)?;
    let input_bytes = fs::read(&input_path)
        .map_err(|error| format!("cannot read input {}: {error}", input_path))?;
    let input: Input = serde_json::from_slice(&input_bytes)
        .map_err(|error| format!("invalid input JSON: {error}"))?;

    // An empty scope must reach EventStore::accept so its own scope
    // validation rejects the attempted acceptance. For non-empty scopes,
    // retain the existing domain validation before persisting anything.
    if !input.event.scope_refs.is_empty() {
        input
            .event
            .validate()
            .map_err(|error| format!("invalid event: {error:?}"))?;
    }
    input
        .claim
        .validate()
        .map_err(|error| format!("invalid claim: {error:?}"))?;

    let idempotency_key = match input.event.idempotency_key.as_deref() {
        Some(key) if !key.trim().is_empty() => key.to_owned(),
        Some(_) => return Err("event.idempotency_key must not be empty".into()),
        None => {
            // A missing key falls back to the stable event identity. This is
            // safe for retries of the same event and does not merge different
            // event IDs under the fixed brain-cli producer identity.
            format!("brain-cli:{}", input.event.event_id.as_str())
        }
    };

    // The default database is process-scoped and cleaned up by RAII.
    // An explicitly supplied path belongs to the caller and is never deleted.
    let temporary_event_database = if event_store_path.is_none() {
        Some(TemporaryDatabase::new("event"))
    } else {
        None
    };

    let event_database_path = event_store_path
        .as_deref()
        .or_else(|| {
            temporary_event_database
                .as_ref()
                .map(TemporaryDatabase::path)
        })
        .expect("one EventStore database path must be selected");

    let mut event_store = SqliteEventStore::open(event_database_path)
        .map_err(|error| format!("cannot open EventStore SQLite database: {error:?}"))?;

    let envelope = EventEnvelope {
        event_kind: input.event.event_kind.clone(),

        // Event has no source_type field. The explicit producer adapter
        // identifies this ingress path rather than inventing source metadata.
        source_type: "brain-cli".into(),

        source_id: input.event.source_id.clone(),

        // Stable producer identity makes idempotency keys comparable across
        // independent CLI processes.
        producer_actor_ref: identifier("producer:brain-cli")?,

        scope_refs: input.event.scope_refs.clone(),
        event_time: input.event.occurred_at.clone(),
        payload_ref: input.event.payload_ref.clone(),
        payload_digest: format!("sha256:{}", sha256_hex(input.payload.as_bytes())),
        classification: event_classification(&input.event.classification),
        idempotency_key: idempotency_key.clone(),
        retention_class: input.event.retention_class.clone(),

        // Event has no correlation_id field. Deriving it from event identity
        // is deterministic, non-empty, and stable across retries.
        correlation_id: identifier(format!("correlation:{}", input.event.event_id.as_str()))?,
    };

    // EventStore is the durable acceptance boundary, not an authorization
    // authority. Its scope argument is the event's declared scope.
    // Payload custody, not bare acceptance: `pending_compile_intents` joins
    // `event_payloads`, so a bare `accept` leaves the outbox row unreachable
    // to the compile read path.
    let accepted_receipt = event_store
        .accept_with_payload(envelope, input.payload.as_bytes(), &input.event.scope_refs)
        .map_err(|error| format!("event-store accept failed: {error:?}"))?;

    // Read the accepted row back through the outbox join. Keeping the receipt
    // in memory would prove acceptance happened but say nothing about whether
    // the compile read path can see it, which is the path the compiler uses.
    let pending = event_store
        .pending_compile_intents()
        .map_err(|error| format!("cannot read compile outbox: {error:?}"))?;
    let pending_intent = pending
        .iter()
        .find(|intent| intent.receipt().receipt_id == accepted_receipt.receipt_id)
        .ok_or_else(|| {
            format!(
                "accepted receipt {} has no pending compile intent",
                accepted_receipt.receipt_id.as_str()
            )
        })?;

    if verbose {
        eprintln!(
            "accepted receipt: {} (outbox row {})",
            accepted_receipt.receipt_id.as_str(),
            pending_intent.outbox_row()
        );
    }

    // EventStore acceptance succeeded. Continue with the existing domain
    // validation and Memory/Version/Context pipeline.
    input
        .event
        .validate()
        .map_err(|error| format!("invalid event: {error:?}"))?;

    let content_digest = sha256_hex(input.payload.as_bytes());
    let scope = input.event.scope_refs.clone();
    let source_version_id = input.memory.memory_version_id.clone();
    let publication_id = format!("publication:{}", input.event.event_id.as_str());
    let derivative_version_id = format!("{}:derivative", source_version_id.as_str());
    let derivative_version = MemoryVersion {
        memory_version_id: OpaqueId::new(derivative_version_id.clone())
            .map_err(|error| format!("invalid derivative version id: {error:?}"))?,
        memory_id: input.memory.memory_id.clone(),
        version_number: 2,
        parent_version_id: Some(source_version_id.clone()),
        created_at: input.memory.version_created_at.clone(),
        author_kind: "compiler".into(),
        change_reason: "compiler derivative".into(),
        claims: vec![input.claim.clone()],
        entity_refs: Vec::new(),
        relation_refs: Vec::new(),
        source_refs: vec![input.event.source_id.clone()],
        provenance_refs: Vec::new(),
        content_digest: format!("{content_digest}:derivative"),
        schema_version: input.memory.schema_version.clone(),
    };
    derivative_version
        .validate()
        .map_err(|error| format!("invalid derivative version: {error:?}"))?;

    let memory = Memory {
        memory_id: input.memory.memory_id.clone(),
        memory_kind: input.memory.memory_kind,
        scope_refs: input.event.scope_refs.clone(),
        current_version_id: None,
        lifecycle_state: input.memory.lifecycle_state.clone(),
        retention_class: input.memory.retention_class,
        sensitivity: input.memory.sensitivity,
        created_at: input.memory.created_at,
        updated_at: input.memory.updated_at,
    };
    memory
        .validate()
        .map_err(|error| format!("invalid memory: {error:?}"))?;

    let revision = MemoryVersion {
        memory_version_id: input.memory.memory_version_id,
        memory_id: memory.memory_id.clone(),
        version_number: 1,
        parent_version_id: None,
        created_at: input.memory.version_created_at,
        author_kind: input.memory.author_kind,
        change_reason: input.memory.change_reason,
        claims: vec![input.claim],
        entity_refs: Vec::new(),
        relation_refs: Vec::new(),
        source_refs: vec![input.event.source_id.clone()],
        provenance_refs: Vec::new(),
        content_digest: content_digest.clone(),
        schema_version: input.memory.schema_version,
    };
    revision
        .validate()
        .map_err(|error| format!("invalid memory version: {error:?}"))?;

    let database = TemporaryDatabase::new("storage");
    let snapshot = {
        let sqlite = SqliteMemoryStorage::open(database.path())
            .map_err(|error| format!("cannot open SQLite storage: {error:?}"))?;
        let mut store = MemoryStore::new(sqlite);

        store
            .create_memory(memory.clone(), &input.event.scope_refs)
            .map_err(|error| format!("create_memory failed: {error:?}"))?;
        store
            .write_revision(
                RevisionWrite {
                    memory_id: memory.memory_id.clone(),
                    expected_current_version: None,
                    revision,
                    idempotency_key,
                    request_digest: content_digest,
                },
                &input.event.scope_refs,
            )
            .map_err(|error| format!("write_revision failed: {error:?}"))?;

        let current = store
            .read_current(&memory.memory_id, &input.event.scope_refs)
            .map_err(|error| format!("read_current failed: {error:?}"))?
            .ok_or_else(|| "read_current returned no revision".to_owned())?;
        let claim = current
            .claims
            .first()
            .ok_or_else(|| "stored revision contains no Claim".to_owned())?;
        let rendered_content = serde_json::to_string(claim)
            .map_err(|error| format!("cannot serialize Claim: {error}"))?;
        let candidate = ContextCandidate {
            entry_id: claim.claim_id.clone(),
            memory_id: current.memory_id.clone(),
            memory_version_id: current.memory_version_id.clone(),
            memory_lifecycle: memory.lifecycle_state.clone(),
            scope_refs: claim.scope_refs.clone(),
            tier: ContextTier::P0,
            priority: 0,
            activation_reason: format!("source event {}", input.event.event_id.as_str()),
            content_hash: sha256_hex(rendered_content.as_bytes()),
            rendered_content,
            source_refs: current.source_refs.clone(),
            evidence_refs: claim.evidence_refs.clone(),
            epistemic_qualifiers: claim.qualifiers.clone(),
        };
        let identity = ContextIdentity {
            context_id: input.context.context_id,
            scope_refs: input.event.scope_refs.clone(),
            agent_id: input.context.agent_id,
            agent_instance_id: input.context.agent_instance_id,
            session_id: input.context.session_id,
            task_id: input.context.task_id,
            environment_id: input.context.environment_id,
            purpose: input.context.purpose,
            schema_version: input.context.schema_version,
        };

        build_context(
            identity,
            1,
            ContextBudget {
                max_entries: 64,
                max_rendered_bytes: 1_048_576,
            },
            vec![candidate],
        )
        .map_err(|error| format!("build_context failed: {error:?}"))?
    };

    let admission_database = TemporaryDatabase::new("admission");
    let stage = run_compiler_stage(CompilerStageRequest {
        intent: pending_intent,
        event_id: &input.event.event_id,
        source_ref: &input.event.source_id,
        scope: &scope,
        source_version_id: &source_version_id,
        derivative_version,
        publication_id: &publication_id,
        storage_path: database.path(),
        admission_path: admission_database.path(),
        issue_canonical_commit,
    })?;
    let notice = stage.notice();

    let mut sidecar_name = std::ffi::OsString::from(&output_path);
    sidecar_name.push(".compiler-status");
    let sidecar_path = PathBuf::from(sidecar_name);
    let sidecar_content = format!("{notice}\n");

    let output = snapshot
        .serialize()
        .map_err(|error| format!("cannot serialize ContextSnapshot: {error:?}"))?;
    fs::write(&output_path, &output)
        .map_err(|error| format!("cannot write output {}: {error}", output_path))?;

    // Context delivery is independent of the compiler publication gate.
    // Delivery failures are observable but must not change CLI success.
    let session_id = snapshot.identity.session_id.as_str();
    let delivery = delivery_adapter(delivery_root.as_deref())
        .and_then(|mut adapter| deliver_snapshot(adapter.as_mut(), session_id, &snapshot));
    match delivery {
        Ok(version) => {
            eprintln!("delivery applied: session={session_id} version={version}");
        }
        Err(reason) => {
            eprintln!("delivery failed: {reason}");
        }
    }
    if let Err(error) = fs::write(&sidecar_path, sidecar_content.as_bytes()) {
        let _ = fs::remove_file(&output_path);
        return Err(format!(
            "cannot write compiler status {}: {error}",
            sidecar_path.display()
        ));
    }

    eprintln!("{notice}");

    if verbose {
        eprintln!("memory-domain: Event, Memory, Claim and MemoryVersion validated");
        eprintln!("memory-storage-sqlite: persisted revision to a temporary SQLite database");
        eprintln!("memory-store: create_memory -> write_revision -> read_current succeeded");
        eprintln!(
            "memory-context: build_context produced {} entr(y/ies)",
            snapshot.total_entries()
        );
        eprintln!("memory-compiler reference version: {COMPILER_VERSION}");
        eprintln!("output: {} ({} bytes)", output_path, output.len());
    }

    Ok(())
}

fn sha256_hex(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";
    let digest = Sha256::digest(bytes);
    let mut output = String::with_capacity(64);
    for byte in digest {
        output.push(HEX[(byte >> 4) as usize] as char);
        output.push(HEX[(byte & 0x0f) as usize] as char);
    }
    output
}

fn usage() -> String {
    "usage: brain compile --input <event.json> --out <context.json> [--verbose]".to_owned()
}

#[cfg(test)]
mod tests {
    use super::sha256_hex;

    #[test]
    fn sha256_output_is_stable() {
        assert_eq!(
            sha256_hex(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
    }
}
