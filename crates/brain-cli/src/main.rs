use memory_compiler::admission::{
    AdmissionStore, DependencyRegistrationRequest, ProducerRegistrationRequest,
};
use memory_compiler::publication_authority::AdmissionPublicationAuthority;
use memory_compiler::{
    AcceptedEvent, ExtractionStage, Identity, IngestionStage, MemoryCompiler, NormalizationStage,
    ProducerWorkItemId, PublicationAuthority, PublicationDisposition, PublicationProof,
    StagingInput, WorkerLease, COMPILER_VERSION,
};
use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextTier,
};
use memory_domain::{Claim, Event, Memory, MemoryLifecycle, MemoryVersion, OpaqueId, ScopeRef};
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
    event_id: &'a OpaqueId,
    source_ref: &'a OpaqueId,
    payload: &'a str,
    scope: &'a [ScopeRef],
    source_version_id: &'a OpaqueId,
    derivative_version: MemoryVersion,
    publication_id: &'a str,
    storage_path: &'a Path,
    admission_path: &'a Path,
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

fn identifier(value: impl Into<String>) -> Result<OpaqueId, String> {
    OpaqueId::new(value).map_err(|error| format!("invalid identifier: {error:?}"))
}

/// Runs the compiler publication stage through the production adapter.
///
/// This seeds the local admission ledger and stages the derivative hidden, then
/// lets `MemoryCompiler::compile` decide. Publication itself is expected to be
/// refused: the adapter may not authorize what no issuer has authorized.
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
            admission_canonical_commit_cursor: Some(identifier(format!(
                "canonical-commit:{event_id}"
            ))?),
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

    let accepted = AcceptedEvent {
        event_id: Identity(event_id.to_owned()),
        receipt_id: Identity(format!("accepted:{event_id}")),
        payload_digest: format!("sha256:{}", sha256_hex(request.payload.as_bytes())),
        payload: request.payload.to_owned(),
        compile_intent_durable: true,
    };
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
        canonical_commit_confirmed: false,
    };
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
    let mut verbose = false;

    while let Some(argument) = args.next() {
        match argument.as_str() {
            "--input" => input_path = args.next(),
            "--out" => output_path = args.next(),
            "--verbose" => verbose = true,
            _ => return Err(format!("unknown argument: {argument}\n{}", usage())),
        }
    }

    let input_path = input_path.ok_or_else(usage)?;
    let output_path = output_path.ok_or_else(usage)?;
    let input_bytes = fs::read(&input_path)
        .map_err(|error| format!("cannot read input {}: {error}", input_path))?;
    let input: Input = serde_json::from_slice(&input_bytes)
        .map_err(|error| format!("invalid input JSON: {error}"))?;

    input
        .event
        .validate()
        .map_err(|error| format!("invalid event: {error:?}"))?;
    input
        .claim
        .validate()
        .map_err(|error| format!("invalid claim: {error:?}"))?;

    let idempotency_key = input
        .event
        .idempotency_key
        .as_ref()
        .filter(|key| !key.trim().is_empty())
        .ok_or_else(|| "event.idempotency_key is required".to_owned())?
        .clone();

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
        event_id: &input.event.event_id,
        source_ref: &input.event.source_id,
        payload: &input.payload,
        scope: &scope,
        source_version_id: &source_version_id,
        derivative_version,
        publication_id: &publication_id,
        storage_path: database.path(),
        admission_path: admission_database.path(),
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
