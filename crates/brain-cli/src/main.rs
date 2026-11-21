use memory_compiler::COMPILER_VERSION;
use memory_context::{
    build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextTier,
};
use memory_domain::{Claim, Event, Memory, MemoryLifecycle, MemoryVersion, OpaqueId};
use memory_storage_sqlite::SqliteMemoryStorage;
use memory_store::{MemoryStore, RevisionWrite};
use serde::Deserialize;
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};

const COMPILER_SKIP_NOTICE: &str =
    "compiler stage skipped: PublicationAuthority has no production implementation";

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
    fn new() -> Self {
        Self(std::env::temp_dir().join(format!(
            "brain-cli-{}.sqlite",
            std::process::id()
        )))
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

    input.event.validate().map_err(|error| format!("invalid event: {error:?}"))?;
    input.claim.validate().map_err(|error| format!("invalid claim: {error:?}"))?;

    let idempotency_key = input
        .event
        .idempotency_key
        .as_ref()
        .filter(|key| !key.trim().is_empty())
        .ok_or_else(|| "event.idempotency_key is required".to_owned())?
        .clone();

    let content_digest = sha256_hex(input.payload.as_bytes());
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
    memory.validate().map_err(|error| format!("invalid memory: {error:?}"))?;

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

    let database = TemporaryDatabase::new();
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

    let mut sidecar_name = std::ffi::OsString::from(&output_path);
    sidecar_name.push(".compiler-status");
    let sidecar_path = PathBuf::from(sidecar_name);
    let sidecar_content = format!("{COMPILER_SKIP_NOTICE}\n");

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

    eprintln!("{COMPILER_SKIP_NOTICE}");

    if verbose {
        eprintln!("memory-domain: Event, Memory, Claim and MemoryVersion validated");
        eprintln!("memory-storage-sqlite: persisted revision to a temporary SQLite database");
        eprintln!("memory-store: create_memory -> write_revision -> read_current succeeded");
        eprintln!("memory-context: build_context produced {} entr(y/ies)", snapshot.total_entries());
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
