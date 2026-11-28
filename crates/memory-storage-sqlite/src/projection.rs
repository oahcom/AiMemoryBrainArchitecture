use memory_domain::{
    Claim, EpistemicStatus, Memory, MemoryLifecycle, MemoryVersion, ScopeKind, ScopeRef,
    TemporalRef, TimeValue,
};
use memory_storage::StorageError;
use sha2::{Digest, Sha256};

const CLAIM_PROJECTION_PREFIX: &[u8] = b"sqlite-claim-projection-v1";
const VERSION_PROJECTION_PREFIX: &[u8] = b"sqlite-version-projection-v1";
const MEMORY_PROJECTION_PREFIX: &[u8] = b"sqlite-memory-projection-v1";

fn push_u64(output: &mut Vec<u8>, value: u64) {
    output.extend_from_slice(&value.to_be_bytes());
}

fn push_bytes(output: &mut Vec<u8>, value: &[u8]) {
    push_u64(output, value.len() as u64);
    output.extend_from_slice(value);
}

fn push_str(output: &mut Vec<u8>, value: &str) {
    push_bytes(output, value.as_bytes());
}

fn push_scope_kind(output: &mut Vec<u8>, kind: &ScopeKind) {
    let literal = match kind {
        ScopeKind::User => "User",
        ScopeKind::Project => "Project",
        ScopeKind::Agent => "Agent",
        ScopeKind::AgentInstance => "AgentInstance",
        ScopeKind::Task => "Task",
        ScopeKind::Session => "Session",
        ScopeKind::Environment => "Environment",
        ScopeKind::System => "System",
    };
    push_str(output, literal);
}

fn scope_projection_bytes(scope: &ScopeRef) -> Vec<u8> {
    let mut output = Vec::new();
    push_str(&mut output, scope.scope_id.as_str());
    push_scope_kind(&mut output, &scope.scope_kind);
    push_str(&mut output, &scope.namespace_key);
    output
}

fn normalized_scope_bytes(scopes: &[ScopeRef]) -> Vec<Vec<u8>> {
    let mut encoded: Vec<Vec<u8>> = scopes.iter().map(scope_projection_bytes).collect();
    encoded.sort();
    encoded.dedup();
    encoded
}

fn push_scope_list(output: &mut Vec<u8>, scopes: &[ScopeRef]) {
    let encoded = normalized_scope_bytes(scopes);
    push_u64(output, encoded.len() as u64);
    for scope in encoded {
        push_bytes(output, &scope);
    }
}

fn epistemic_status_literal(status: &EpistemicStatus) -> &'static str {
    match status {
        EpistemicStatus::Observed => "Observed",
        EpistemicStatus::Reported => "Reported",
        EpistemicStatus::Inferred => "Inferred",
        EpistemicStatus::Verified => "Verified",
        EpistemicStatus::Disputed => "Disputed",
        EpistemicStatus::Retracted => "Retracted",
    }
}

fn push_time_value(output: &mut Vec<u8>, value: &TimeValue) {
    match value {
        TimeValue::Instant(value) => {
            output.push(0);
            push_str(output, value);
        }
        TimeValue::Interval { start, end } => {
            output.push(1);
            push_str(output, start);
            push_str(output, end);
        }
        TimeValue::Unknown => output.push(2),
    }
}

fn push_temporal_ref(output: &mut Vec<u8>, temporal: &TemporalRef) {
    push_time_value(output, &temporal.occurred_at);
    push_time_value(output, &temporal.valid_time);
}

fn push_string_list(output: &mut Vec<u8>, values: &[String]) {
    push_u64(output, values.len() as u64);
    for value in values {
        push_str(output, value);
    }
}

fn push_id_list(
    output: &mut Vec<u8>,
    values: &[memory_domain::OpaqueId],
) {
    push_u64(output, values.len() as u64);
    for value in values {
        push_str(output, value.as_str());
    }
}

/// Deterministic SQLite-local Claim projection encoding.
/// This is not the domain's canonical Claim encoding.
pub(crate) fn claim_projection_bytes(claim: &Claim) -> Vec<u8> {
    let mut output = Vec::new();
    push_bytes(&mut output, CLAIM_PROJECTION_PREFIX);

    push_str(&mut output, claim.claim_id.as_str());
    push_str(&mut output, claim.subject_ref.as_str());
    push_str(&mut output, &claim.predicate);
    push_str(&mut output, &claim.object_value);
    push_str(&mut output, &claim.polarity);
    push_str(
        &mut output,
        epistemic_status_literal(&claim.epistemic_status),
    );

    match &claim.confidence {
        None => output.push(0),
        Some(value) => {
            output.push(1);
            push_str(&mut output, value);
        }
    }

    match &claim.temporal_ref {
        None => output.push(0),
        Some(value) => {
            output.push(1);
            push_temporal_ref(&mut output, value);
        }
    }

    push_str(&mut output, &claim.asserted_at);
    push_scope_list(&mut output, &claim.scope_refs);
    push_string_list(&mut output, &claim.qualifiers);
    push_id_list(&mut output, &claim.evidence_refs);

    output
}

fn sha256_hex(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

/// Digest of the visible version projection, independent of the canonical
/// content digest's encoding.
pub(crate) fn version_projection_digest(
    version: &MemoryVersion,
    visible_claims: &[Claim],
    authorized_scopes: &[ScopeRef],
    policy_epoch: u64,
) -> String {
    let mut output = Vec::new();
    push_bytes(&mut output, VERSION_PROJECTION_PREFIX);
    push_str(&mut output, version.memory_id.as_str());
    push_str(&mut output, version.memory_version_id.as_str());
    push_str(&mut output, &version.content_digest);
    push_scope_list(&mut output, authorized_scopes);
    push_u64(&mut output, policy_epoch);
    push_u64(&mut output, visible_claims.len() as u64);

    for claim in visible_claims {
        let encoded = claim_projection_bytes(claim);
        push_bytes(&mut output, &encoded);
    }

    sha256_hex(&output)
}

fn memory_lifecycle_literal(state: &MemoryLifecycle) -> &'static str {
    match state {
        MemoryLifecycle::Candidate => "Candidate",
        MemoryLifecycle::Consolidated => "Consolidated",
        MemoryLifecycle::Active => "Active",
        MemoryLifecycle::Superseded => "Superseded",
        MemoryLifecycle::Archived => "Archived",
        MemoryLifecycle::Forgotten => "Forgotten",
    }
}

/// Digest of the explicitly whitelisted Memory metadata projection.
pub(crate) fn memory_projection_digest(
    memory: &Memory,
    visible_scope_refs: &[ScopeRef],
    authorized_scopes: &[ScopeRef],
    policy_epoch: u64,
) -> String {
    let mut output = Vec::new();
    push_bytes(&mut output, MEMORY_PROJECTION_PREFIX);

    push_str(&mut output, memory.memory_id.as_str());
    push_str(&mut output, &memory.memory_kind);
    push_str(
        &mut output,
        memory_lifecycle_literal(&memory.lifecycle_state),
    );
    push_str(&mut output, &memory.retention_class);
    push_str(&mut output, &memory.sensitivity);
    push_str(&mut output, &memory.created_at);
    push_str(&mut output, &memory.updated_at);

    push_scope_list(&mut output, visible_scope_refs);
    push_scope_list(&mut output, authorized_scopes);
    push_u64(&mut output, policy_epoch);

    sha256_hex(&output)
}

/// Retain only whole Claims whose complete scope set is authorized and lies
/// within the requested projection scope. The source order is preserved.
pub(crate) fn visible_claims(
    version: &MemoryVersion,
    authorized: &[ScopeRef],
    projection_scope: &[ScopeRef],
) -> Vec<Claim> {
    version
        .claims
        .iter()
        .filter(|claim| {
            !claim.scope_refs.is_empty()
                && claim.scope_refs.iter().all(|scope| {
                    authorized.contains(scope) && projection_scope.contains(scope)
                })
        })
        .cloned()
        .collect()
}

/// Return the stored/authorized/requested scope intersection. A request that
/// contains any unauthorized scope is rejected rather than silently narrowed.
pub(crate) fn projectable_scopes(
    stored: &[ScopeRef],
    authorized: &[ScopeRef],
    projection_scope: &[ScopeRef],
) -> Result<Vec<ScopeRef>, StorageError> {
    if projection_scope
        .iter()
        .any(|scope| !authorized.contains(scope))
    {
        return Err(StorageError::ScopeMismatch);
    }

    let mut result: Vec<ScopeRef> = stored
        .iter()
        .filter(|scope| {
            authorized.contains(scope) && projection_scope.contains(scope)
        })
        .cloned()
        .collect();

    result.sort_by_key(scope_projection_bytes);
    result.dedup();

    if result.is_empty() {
        return Err(StorageError::ScopeMismatch);
    }

    Ok(result)
}
