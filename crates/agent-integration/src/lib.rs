//! Deterministic Agent Integration reference model.
//!
//! This crate does not perform model inference, network transport, persistence,
//! BMCP negotiation, or production telemetry.

use memory_context::{validate_snapshot, ContextError, ContextSnapshot};
use std::collections::BTreeMap;

/// Capability tier demonstrated by an adapter.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum CapabilityTier {
    /// Full inference-context boundary.
    Tier1,
    /// Middleware-controlled request paths.
    Tier2,
    /// Scoped events and explicit Active Recall.
    Tier3,
}

/// Concrete adapter operation subject to tier enforcement.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AdapterOperation {
    SubmitScopedTelemetry,
    RequestActiveRecall,
    InsertMiddlewareMemorySlot,
    AttestMiddlewareApplication,
    ObserveFullInferenceBoundary,
    ApplyFullBoundaryMemory,
    AttestFullBoundaryApplication,
    ReconcileSnapshotAndDelta,
}

impl AdapterOperation {
    /// Minimum capability tier required to perform this operation.
    pub const fn required_tier(self) -> CapabilityTier {
        match self {
            Self::SubmitScopedTelemetry | Self::RequestActiveRecall => CapabilityTier::Tier3,
            Self::InsertMiddlewareMemorySlot | Self::AttestMiddlewareApplication => {
                CapabilityTier::Tier2
            }
            Self::ObserveFullInferenceBoundary
            | Self::ApplyFullBoundaryMemory
            | Self::AttestFullBoundaryApplication
            | Self::ReconcileSnapshotAndDelta => CapabilityTier::Tier1,
        }
    }
}

/// A region in an assembled inference request.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ContextRegion {
    SystemInstructions,
    DeveloperInstructions,
    UserInput,
    AgentSafetyPolicy,
    ToolSchemasAndAuthorization,
    AgentWorkingState,
    BrainManagedMemory,
}

/// Typed, machine-matchable rejection reasons.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AdapterError {
    TierInsufficient {
        required: CapabilityTier,
        actual: CapabilityTier,
    },
    ProtectedRegionMutation(ContextRegion),
    RequestAlreadyFrozen,
    /// The caller attempted delivery while this session was disconnected.
    SessionDisconnected {
        session_id: String,
    },
    /// The supplied snapshot is not the exact next version for this session.
    VersionMismatch {
        expected: u64,
        received: u64,
    },
    /// A received version skips one or more required context versions.
    VersionGap {
        current: u64,
        received: u64,
    },
    /// A Brain-side snapshot failed canonical validation before delivery.
    InvalidSnapshot {
        reason: String,
    },
    /// The current version cannot be incremented without wrapping.
    VersionExhausted,
    /// The requested delivery-state transition is not permitted by the contract.
    IllegalStateTransition {
        from: DeliveryState,
        to: DeliveryState,
    },
    /// `Applied` was requested without an Applied attestation.
    AppliedRequiresAttestation,
    /// The attestation's target version is not this delivery's target version.
    AppliedVersionMismatch {
        expected: u64,
        received: u64,
    },
    EmptyIdentity {
        field: &'static str,
    },
    ProtectedRegionLeak {
        marker: &'static str,
    },
    BudgetExceeded {
        limit: usize,
        actual: usize,
    },
    NotFrozen,
    InvalidRegionDigest,
}

/// Check whether an adapter tier is sufficient for an operation.
pub fn authorize(actual: CapabilityTier, operation: AdapterOperation) -> Result<(), AdapterError> {
    let required = operation.required_tier();
    // Tier1 is strongest: the derived ordering is Tier1 < Tier2 < Tier3.
    if actual <= required {
        Ok(())
    } else {
        Err(AdapterError::TierInsufficient { required, actual })
    }
}

macro_rules! identity_type {
    ($name:ident, $field:literal) => {
        #[derive(Clone, Debug, Eq, PartialEq, Hash)]
        pub struct $name(String);

        impl $name {
            pub fn new(value: impl Into<String>) -> Result<Self, AdapterError> {
                let value = value.into();
                if value.trim().is_empty() {
                    return Err(AdapterError::EmptyIdentity { field: $field });
                }
                Ok(Self(value))
            }

            pub fn as_str(&self) -> &str {
                &self.0
            }
        }
    };
}

identity_type!(ContextId, "context_id");
identity_type!(ContextSessionId, "context_session_id");
identity_type!(AdapterId, "adapter_id");
identity_type!(AdapterInstanceId, "adapter_instance_id");
identity_type!(AgentInstanceId, "agent_instance_id");
identity_type!(BoundaryId, "boundary_id");
identity_type!(InferenceRequestId, "inference_request_id");
identity_type!(DeliveryId, "delivery_id");
identity_type!(RegionDigest, "region_digest");

/// Evidence stages are intentionally nominally separate observations.
///
/// No conversion is provided between stages: Received does not imply Accepted,
/// and Accepted does not imply Applied. A later protocol layer must establish
/// each stage with its own evidence.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EvidenceStage {
    Received,
    Accepted,
    Applied,
}

/// The request assembly state is either mutable or backed by frozen evidence.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AssemblyState {
    Open { staged_version: u64 },
    Frozen(FrozenRequest),
}

/// Immutable evidence produced when a request is frozen.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct FrozenRequest {
    pub request_id: InferenceRequestId,
    pub boundary_id: BoundaryId,
    pub region_version: u64,
    pub region_digest: RegionDigest,
}

/// Single-use request assembler. Its mutable state is private.
#[derive(Clone, Debug)]
pub struct RequestAssembler {
    boundary_id: BoundaryId,
    request_id: InferenceRequestId,
    state: AssemblyState,
    staged_region: Option<ManagedRegion>,
}

impl RequestAssembler {
    pub fn new(boundary_id: BoundaryId, request_id: InferenceRequestId) -> Self {
        Self {
            boundary_id,
            request_id,
            state: AssemblyState::Open { staged_version: 0 },
            staged_region: None,
        }
    }

    /// Stage a materialized region. A frozen assembler rejects further writes.
    pub fn stage(&mut self, region: &ManagedRegion) -> Result<(), AdapterError> {
        if matches!(self.state, AssemblyState::Frozen(_)) {
            return Err(AdapterError::RequestAlreadyFrozen);
        }
        validate_region_digest(&region.digest)?;
        self.staged_region = Some(region.clone());
        self.state = AssemblyState::Open {
            staged_version: region.context_version,
        };
        Ok(())
    }

    /// Consume this assembler and produce its single frozen request.
    pub fn freeze(self) -> Result<FrozenRequest, AdapterError> {
        match self.state {
            AssemblyState::Frozen(frozen) => Ok(frozen),
            AssemblyState::Open { .. } => {
                let region = self.staged_region.ok_or(AdapterError::NotFrozen)?;
                validate_region_digest(&region.digest)?;
                Ok(FrozenRequest {
                    request_id: self.request_id,
                    boundary_id: self.boundary_id,
                    region_version: region.context_version,
                    region_digest: region.digest,
                })
            }
        }
    }

    pub fn state(&self) -> &AssemblyState {
        &self.state
    }
}

/// Materialization limits. Neither limit permits truncation.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Budget {
    pub max_rendered_bytes: usize,
    pub max_entries: usize,
}

/// A Brain-managed context region materialized from a context snapshot.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ManagedRegion {
    pub context_id: ContextId,
    pub context_version: u64,
    pub rendered_bytes: usize,
    pub entry_count: usize,
    pub digest: RegionDigest,
}

fn validate_region_digest(digest: &RegionDigest) -> Result<(), AdapterError> {
    let value = digest.as_str();
    if value.len() != 16
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(AdapterError::InvalidRegionDigest);
    }
    Ok(())
}

/// Materialize a complete managed region from a snapshot.
///
/// The region digest is an internal FNV-1a fingerprint. It is independent of
/// memory-context's content_hash algorithm and is not a cross-authority proof.
pub fn materialize_managed_region(
    snapshot: &ContextSnapshot,
    budget: &Budget,
) -> Result<ManagedRegion, AdapterError> {
    let rendered_bytes = snapshot.rendered_bytes;
    let entry_count = snapshot.entries.len();

    if rendered_bytes > budget.max_rendered_bytes {
        return Err(AdapterError::BudgetExceeded {
            limit: budget.max_rendered_bytes,
            actual: rendered_bytes,
        });
    }
    if entry_count > budget.max_entries {
        return Err(AdapterError::BudgetExceeded {
            limit: budget.max_entries,
            actual: entry_count,
        });
    }

    // ContextIdentity exposes its stable context identifier as an OpaqueId.
    let context_id = ContextId::new(snapshot.identity.context_id.as_str())?;
    let digest = calculate_region_digest(snapshot, context_id.as_str());

    Ok(ManagedRegion {
        context_id,
        context_version: snapshot.context_version,
        rendered_bytes,
        entry_count,
        digest: RegionDigest::new(digest)?,
    })
}

fn calculate_region_digest(snapshot: &ContextSnapshot, context_id: &str) -> String {
    let mut canonical = format!(
        "{}\u{1f}{}\u{1f}{}\u{1f}{}",
        context_id,
        snapshot.context_version,
        snapshot.rendered_bytes,
        snapshot.entries.len()
    );

    canonical.push('\u{1e}');
    for (index, entry) in snapshot.entries.iter().enumerate() {
        if index > 0 {
            canonical.push('\u{1e}');
        }
        canonical.push_str(entry.entry_id.as_str());
        canonical.push('\u{1f}');
        canonical.push_str(entry.memory_id.as_str());
        canonical.push('\u{1f}');
        canonical.push_str(entry.memory_version_id.as_str());
        canonical.push('\u{1f}');
        canonical.push_str(&entry.content_hash);
        canonical.push('\u{1f}');
        canonical.push_str(&entry.rendered_bytes.to_string());
    }

    let mut hash = 0xcbf29ce484222325u64;
    for byte in canonical.as_bytes() {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    format!("{:016x}", hash)
}

/// Assert that content intended for the managed-memory region contains no
/// markers belonging to protected request regions.
pub fn assert_region_isolation(region: ContextRegion, content: &str) -> Result<(), AdapterError> {
    if region != ContextRegion::BrainManagedMemory {
        return Err(AdapterError::ProtectedRegionMutation(region));
    }

    const PROTECTED_MARKERS: [&str; 6] = [
        "<|system|>",
        "<|developer|>",
        "<|safety|>",
        "<|tools|>",
        "<|user|>",
        "<|working_state|>",
    ];

    for marker in PROTECTED_MARKERS {
        if content.contains(marker) {
            return Err(AdapterError::ProtectedRegionLeak { marker });
        }
    }
    Ok(())
}

/// Validate a proposed write to the inference request's context.
///
/// Only the Brain-managed memory region is writable. Once the request has
/// frozen evidence, even that region is immutable.
pub fn validate_context_write(
    region: ContextRegion,
    state: &AssemblyState,
) -> Result<(), AdapterError> {
    if region != ContextRegion::BrainManagedMemory {
        return Err(AdapterError::ProtectedRegionMutation(region));
    }
    if matches!(state, AssemblyState::Frozen(_)) {
        return Err(AdapterError::RequestAlreadyFrozen);
    }
    Ok(())
}

/// Apply deterministic permission and boundary checks before a full-boundary
/// memory write. This does not mutate a real Agent request or runtime.
pub fn validate_full_boundary_apply(
    tier: CapabilityTier,
    region: ContextRegion,
    state: &AssemblyState,
) -> Result<(), AdapterError> {
    authorize(tier, AdapterOperation::ApplyFullBoundaryMemory)?;

    validate_context_write(region, state)
}

/// An immutable, versioned payload delivered to one Agent session.
///
/// This adapter-boundary payload is deliberately distinct from
/// `memory_context::ContextSnapshot`, which is the Brain-side build artifact
/// containing context identity, entries, and rendered-byte accounting.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DeliveryPayload {
    version: u64,
    content: String,
}

impl DeliveryPayload {
    /// Build an adapter payload only from a validated Brain context snapshot.
    pub fn from_snapshot(snapshot: &ContextSnapshot) -> Result<Self, AdapterError> {
        validate_snapshot(snapshot).map_err(|error: ContextError| {
            AdapterError::InvalidSnapshot {
                reason: format!("{error:?}"),
            }
        })?;
        let content = snapshot
            .serialize()
            .map_err(|error| AdapterError::InvalidSnapshot {
                reason: format!("{error:?}"),
            })?;
        Ok(Self {
            version: snapshot.context_version,
            content,
        })
    }

    pub fn version(&self) -> u64 {
        self.version
    }
    pub fn content(&self) -> &str {
        &self.content
    }

    /// Test-only fixture constructor; production code must use `from_snapshot`.
    #[cfg(test)]
    fn new_for_test(version: u64, content: impl Into<String>) -> Self {
        Self {
            version,
            content: content.into(),
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ApplyOutcome {
    Applied,
    AlreadyApplied,
}

/// Delivery lifecycle states (inference-boundary-model.md §5).
///
/// `Delivered` is not `Received`; `Received` is not `Accepted`; `Accepted` is
/// not `Applied`. Each transition requires its own evidence.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum DeliveryState {
    Delivered,
    Received,
    Accepted,
    Applied,
    Rejected,
    Expired,
    Superseded,
}

impl DeliveryState {
    /// Terminal states cannot transition anywhere (§8).
    pub const fn is_terminal(self) -> bool {
        matches!(
            self,
            Self::Applied | Self::Rejected | Self::Expired | Self::Superseded
        )
    }

    /// Whether `self -> next` is a legal transition per §5/§8.
    ///
    /// Notably `Delivered -> Applied` and `Received -> Applied` are false: an
    /// update must be received *and* accepted before it can be applied.
    pub const fn can_transition_to(self, next: Self) -> bool {
        use DeliveryState::{
            Accepted, Applied, Delivered, Expired, Received, Rejected, Superseded,
        };
        matches!(
            (self, next),
            (Delivered, Received)
                | (Received, Accepted)
                | (Received, Rejected)
                | (Accepted, Applied)
                | (Accepted, Rejected)
                | (Delivered, Expired)
                | (Received, Expired)
                | (Accepted, Expired)
                | (Delivered, Superseded)
                | (Received, Superseded)
                | (Accepted, Superseded)
        )
    }
}

/// Applied attestation (§6): proof that the Adapter materialized the exact
/// target version in the managed region at an inference boundary.
///
/// This is an Adapter assertion, not provider-side proof, and it does not prove
/// model attention, comprehension, or compliance.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AppliedAttestation {
    pub context_id: String,
    pub context_session_id: String,
    pub target_context_version: u64,
    pub adapter_id: String,
    pub adapter_instance_id: String,
    pub agent_instance_id: String,
    pub boundary_id: String,
    pub inference_request_id: Option<String>,
    /// ISO-8601 timestamp; kept as a string because this crate has no deps.
    pub applied_at: String,
}

/// One delivery's lifecycle record: current state plus optional attestation.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DeliveryRecord {
    target_context_version: u64,
    state: DeliveryState,
    attestation: Option<AppliedAttestation>,
}

impl DeliveryRecord {
    /// A newly transported delivery starts at `Delivered` for `target_context_version`.
    pub fn new(target_context_version: u64) -> Self {
        Self {
            target_context_version,
            state: DeliveryState::Delivered,
            attestation: None,
        }
    }

    pub fn state(&self) -> DeliveryState {
        self.state
    }

    pub fn target_context_version(&self) -> u64 {
        self.target_context_version
    }

    pub fn attestation(&self) -> Option<&AppliedAttestation> {
        self.attestation.as_ref()
    }

    pub fn set_attestation(&mut self, attestation: AppliedAttestation) {
        self.attestation = Some(attestation);
    }

    /// Advance the delivery state, enforcing §5.
    ///
    /// `Applied` additionally requires an attestation whose
    /// `target_context_version` equals this delivery's target version: receipt,
    /// parsing, queueing, or caching never substitutes for materialization.
    pub fn transition(&mut self, next: DeliveryState) -> Result<(), AdapterError> {
        if !self.state.can_transition_to(next) {
            return Err(AdapterError::IllegalStateTransition {
                from: self.state,
                to: next,
            });
        }

        if next == DeliveryState::Applied {
            let attestation = self
                .attestation
                .as_ref()
                .ok_or(AdapterError::AppliedRequiresAttestation)?;
            if attestation.target_context_version != self.target_context_version {
                return Err(AdapterError::AppliedVersionMismatch {
                    expected: self.target_context_version,
                    received: attestation.target_context_version,
                });
            }
        }
        self.state = next;
        Ok(())
    }
}

/// Session-scoped delivery contract.
///
/// Versions begin at 1 for a new or cleared session. Every accepted apply must
/// be the exact successor of the last successfully applied snapshot. A clear
/// removes the applied snapshot and resets that sequence. Reconnect reports
/// only the last successfully applied version.
pub trait ContextDeliveryAdapter {
    fn apply(
        &mut self,
        session_id: &str,
        snapshot: DeliveryPayload,
    ) -> Result<ApplyOutcome, AdapterError>;

    fn clear(&mut self, session_id: &str) -> Result<(), AdapterError>;

    fn disconnect(&mut self, session_id: &str) -> Result<(), AdapterError>;

    fn reconnect(&mut self, session_id: &str) -> Result<Option<u64>, AdapterError>;

    /// Read the payload currently recorded as applied for this session.
    fn applied_snapshot(&self, session_id: &str) -> Option<&DeliveryPayload>;
}

#[derive(Debug)]
struct SessionState {
    applied: Option<DeliveryPayload>,
    connected: bool,
}

impl Default for SessionState {
    fn default() -> Self {
        Self {
            applied: None,
            connected: true,
        }
    }
}

/// In-memory adapter implementation for deterministic tests and local use.
///
/// It deliberately has no transport, runtime binding, or durable storage.
#[derive(Default)]
pub struct InMemoryContextDeliveryAdapter {
    sessions: BTreeMap<String, SessionState>,
}

impl ContextDeliveryAdapter for InMemoryContextDeliveryAdapter {
    fn apply(
        &mut self,
        session_id: &str,
        snapshot: DeliveryPayload,
    ) -> Result<ApplyOutcome, AdapterError> {
        let state = self.sessions.entry(session_id.to_owned()).or_default();
        if !state.connected {
            return Err(AdapterError::SessionDisconnected {
                session_id: session_id.to_owned(),
            });
        }

        if let Some(applied) = state.applied.as_ref() {
            if snapshot.version == applied.version && snapshot == *applied {
                return Ok(ApplyOutcome::AlreadyApplied);
            }
        }
        let current = state.applied.as_ref().map_or(0, |applied| applied.version);
        let expected = current
            .checked_add(1)
            .ok_or(AdapterError::VersionExhausted)?;
        if snapshot.version > expected {
            return Err(AdapterError::VersionGap {
                current,
                received: snapshot.version,
            });
        }
        if snapshot.version != expected {
            return Err(AdapterError::VersionMismatch {
                expected,
                received: snapshot.version,
            });
        }
        state.applied = Some(snapshot);
        Ok(ApplyOutcome::Applied)
    }

    fn clear(&mut self, session_id: &str) -> Result<(), AdapterError> {
        let state = self.sessions.entry(session_id.to_owned()).or_default();
        state.applied = None;
        Ok(())
    }

    fn disconnect(&mut self, session_id: &str) -> Result<(), AdapterError> {
        let state = self.sessions.entry(session_id.to_owned()).or_default();
        state.connected = false;
        Ok(())
    }

    fn reconnect(&mut self, session_id: &str) -> Result<Option<u64>, AdapterError> {
        let state = self.sessions.entry(session_id.to_owned()).or_default();
        state.connected = true;
        Ok(state.applied.as_ref().map(|snapshot| snapshot.version))
    }

    fn applied_snapshot(&self, session_id: &str) -> Option<&DeliveryPayload> {
        self.sessions.get(session_id)?.applied.as_ref()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_context::{ContextEntry, ContextIdentity};
    use memory_domain::{OpaqueId, ScopeKind, ScopeRef};

    fn opaque(value: &str) -> OpaqueId {
        OpaqueId::new(value).expect("fixture id is nonempty")
    }

    fn snapshot_with_entries(contents: &[(&str, &str, &str, &str, usize)]) -> ContextSnapshot {
        let entries = contents
            .iter()
            .map(
                |(entry_id, memory_id, version_id, content_hash, rendered_bytes)| ContextEntry {
                    entry_id: opaque(entry_id),
                    memory_id: opaque(memory_id),
                    memory_version_id: opaque(version_id),
                    tier: memory_context::ContextTier::P1,
                    priority: 1,
                    activation_reason: "test".into(),
                    rendered_content: "x".into(),
                    source_refs: vec![opaque("source")],
                    evidence_refs: vec![],
                    epistemic_qualifiers: vec![],
                    content_hash: (*content_hash).into(),
                    rendered_bytes: *rendered_bytes,
                },
            )
            .collect::<Vec<_>>();

        let rendered_bytes = entries.iter().map(|entry| entry.rendered_bytes).sum();
        ContextSnapshot {
            identity: ContextIdentity {
                context_id: opaque("context-1"),
                scope_refs: vec![ScopeRef {
                    scope_id: opaque("scope-1"),
                    scope_kind: ScopeKind::User,
                    namespace_key: "user:scope-1".into(),
                }],
                agent_id: opaque("agent-1"),
                agent_instance_id: opaque("agent-instance-1"),
                session_id: opaque("session-1"),
                task_id: None,
                environment_id: None,
                purpose: "agent-integration-test".into(),
                schema_version: "1".into(),
            },
            context_version: 7,
            entries,
            tombstones: vec![],
            operation_records: vec![],
            rendered_bytes,
        }
    }

    fn one_entry_snapshot() -> ContextSnapshot {
        snapshot_with_entries(&[("entry-1", "memory-1", "version-1", "hash-a", 1)])
    }

    fn budget() -> Budget {
        Budget {
            max_rendered_bytes: 1024,
            max_entries: 16,
        }
    }

    fn open_state() -> AssemblyState {
        AssemblyState::Open { staged_version: 0 }
    }

    fn frozen_state() -> AssemblyState {
        let mut assembler = RequestAssembler::new(
            BoundaryId::new("boundary-1").expect("valid fixture id"),
            InferenceRequestId::new("request-1").expect("valid fixture id"),
        );
        let region = materialize_managed_region(&one_entry_snapshot(), &budget())
            .expect("fixture fits budget");
        assembler.stage(&region).expect("stage succeeds");
        AssemblyState::Frozen(assembler.freeze().expect("staged request freezes"))
    }

    fn test_snapshot(version: u64, content: &str) -> ContextSnapshot {
        use memory_context::{
            build_context, ContextBudget, ContextCandidate, ContextIdentity, ContextTier,
        };
        use memory_domain::{MemoryLifecycle, OpaqueId, ScopeKind, ScopeRef};
        let id = |value: &str| OpaqueId::new(value).unwrap();
        let scope = ScopeRef {
            scope_id: id("scope"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:test".into(),
        };
        let identity = ContextIdentity {
            context_id: id("context"),
            scope_refs: vec![scope.clone()],
            agent_id: id("agent"),
            agent_instance_id: id("instance"),
            session_id: id("session"),
            task_id: None,
            environment_id: None,
            purpose: "adapter test".into(),
            schema_version: "1".into(),
        };
        let candidate = ContextCandidate {
            entry_id: id("entry"),
            memory_id: id("memory"),
            memory_version_id: id("memory-version"),
            memory_lifecycle: MemoryLifecycle::Active,
            scope_refs: vec![scope],
            tier: ContextTier::P0,
            priority: 0,
            activation_reason: "test fixture".into(),
            rendered_content: content.into(),
            source_refs: vec![id("source")],
            evidence_refs: vec![],
            epistemic_qualifiers: vec![],
            content_hash: "test-hash".into(),
        };
        build_context(
            identity,
            version,
            ContextBudget {
                max_entries: 8,
                max_rendered_bytes: 4096,
            },
            vec![candidate],
        )
        .unwrap()
    }

    #[test]
    fn from_snapshot_validates_and_serializes_the_canonical_snapshot() {
        let snapshot = test_snapshot(1, "canonical");
        let payload = DeliveryPayload::from_snapshot(&snapshot).unwrap();
        assert_eq!(payload.version(), snapshot.context_version);
        assert_eq!(payload.content(), snapshot.serialize().unwrap());
        let mut invalid = snapshot;
        invalid.rendered_bytes += 1;
        assert!(matches!(
            DeliveryPayload::from_snapshot(&invalid),
            Err(AdapterError::InvalidSnapshot { .. })
        ));
    }

    #[test]
    fn reapplying_identical_snapshot_returns_already_applied_without_mutation() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        let payload = DeliveryPayload::from_snapshot(&test_snapshot(1, "same")).unwrap();
        assert_eq!(
            adapter.apply("session-a", payload.clone()),
            Ok(ApplyOutcome::Applied)
        );
        let before = adapter.applied_snapshot("session-a").unwrap().clone();
        assert_eq!(
            adapter.apply("session-a", payload),
            Ok(ApplyOutcome::AlreadyApplied)
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&before));
        assert_eq!(
            adapter.apply("session-a", DeliveryPayload::new_for_test(1, "different")),
            Err(AdapterError::VersionMismatch {
                expected: 2,
                received: 1
            })
        );
    }

    #[test]
    fn skipped_context_version_returns_version_gap_without_mutation() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "first"))
            .unwrap();
        let before = adapter.applied_snapshot("session-a").unwrap().clone();
        assert_eq!(
            adapter.apply("session-a", DeliveryPayload::new_for_test(3, "third")),
            Err(AdapterError::VersionGap {
                current: 1,
                received: 3
            })
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&before));
    }

    #[test]
    fn disconnect_preserves_last_applied_snapshot_but_rejects_new_apply() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "committed"))
            .unwrap();
        let before = adapter.applied_snapshot("session-a").unwrap().clone();
        adapter.disconnect("session-a").unwrap();
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&before));
        assert_eq!(
            adapter.apply("session-a", DeliveryPayload::new_for_test(2, "blocked")),
            Err(AdapterError::SessionDisconnected {
                session_id: "session-a".into()
            })
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&before));
    }

    #[test]
    fn legal_tier_three_telemetry_call_is_allowed() {
        assert_eq!(
            authorize(
                CapabilityTier::Tier3,
                AdapterOperation::SubmitScopedTelemetry
            ),
            Ok(())
        );
    }

    #[test]
    fn insufficient_tier_is_rejected_with_typed_error() {
        assert_eq!(
            authorize(
                CapabilityTier::Tier3,
                AdapterOperation::ObserveFullInferenceBoundary
            ),
            Err(AdapterError::TierInsufficient {
                required: CapabilityTier::Tier1,
                actual: CapabilityTier::Tier3,
            })
        );
    }

    #[test]
    fn protected_instruction_region_write_is_rejected() {
        assert_eq!(
            validate_full_boundary_apply(
                CapabilityTier::Tier1,
                ContextRegion::DeveloperInstructions,
                &open_state(),
            ),
            Err(AdapterError::ProtectedRegionMutation(
                ContextRegion::DeveloperInstructions
            ))
        );
    }

    #[test]
    fn frozen_inference_request_write_is_rejected() {
        assert_eq!(
            validate_full_boundary_apply(
                CapabilityTier::Tier1,
                ContextRegion::BrainManagedMemory,
                &frozen_state(),
            ),
            Err(AdapterError::RequestAlreadyFrozen)
        );
    }

    #[test]
    fn authorize_complete_three_tier_by_eight_operation_matrix() {
        let operations = [
            AdapterOperation::SubmitScopedTelemetry,
            AdapterOperation::RequestActiveRecall,
            AdapterOperation::InsertMiddlewareMemorySlot,
            AdapterOperation::AttestMiddlewareApplication,
            AdapterOperation::ObserveFullInferenceBoundary,
            AdapterOperation::ApplyFullBoundaryMemory,
            AdapterOperation::AttestFullBoundaryApplication,
            AdapterOperation::ReconcileSnapshotAndDelta,
        ];
        let tiers = [
            CapabilityTier::Tier1,
            CapabilityTier::Tier2,
            CapabilityTier::Tier3,
        ];
        for operation in operations {
            for actual in tiers {
                let expected = if actual <= operation.required_tier() {
                    Ok(())
                } else {
                    Err(AdapterError::TierInsufficient {
                        required: operation.required_tier(),
                        actual,
                    })
                };
                assert_eq!(authorize(actual, operation), expected);
            }
        }
    }

    #[test]
    fn open_state_allows_managed_memory_write() {
        assert_eq!(
            validate_context_write(ContextRegion::BrainManagedMemory, &open_state()),
            Ok(())
        );
    }

    #[test]
    fn frozen_state_rejects_managed_memory_write() {
        assert_eq!(
            validate_context_write(ContextRegion::BrainManagedMemory, &frozen_state()),
            Err(AdapterError::RequestAlreadyFrozen)
        );
    }

    #[test]
    fn assembler_stage_rejects_frozen_state() {
        let mut assembler = RequestAssembler::new(
            BoundaryId::new("boundary").expect("valid id"),
            InferenceRequestId::new("request").expect("valid id"),
        );
        let region =
            materialize_managed_region(&one_entry_snapshot(), &budget()).expect("fixture fits");
        assembler.stage(&region).expect("first stage succeeds");
        let frozen = assembler.clone().freeze().expect("clone freezes");
        assembler.state = AssemblyState::Frozen(frozen);
        assert_eq!(
            assembler.stage(&region),
            Err(AdapterError::RequestAlreadyFrozen)
        );
    }

    #[test]
    fn assembler_cannot_freeze_without_a_staged_region() {
        let assembler = RequestAssembler::new(
            BoundaryId::new("boundary").expect("valid id"),
            InferenceRequestId::new("request").expect("valid id"),
        );
        assert_eq!(assembler.freeze(), Err(AdapterError::NotFrozen));
    }

    #[test]
    fn assembler_freeze_preserves_request_and_region_evidence() {
        let mut assembler = RequestAssembler::new(
            BoundaryId::new("boundary").expect("valid id"),
            InferenceRequestId::new("request").expect("valid id"),
        );
        let region =
            materialize_managed_region(&one_entry_snapshot(), &budget()).expect("fixture fits");
        assembler.stage(&region).expect("stage succeeds");
        let frozen = assembler.freeze().expect("freeze succeeds");
        assert_eq!(frozen.request_id.as_str(), "request");
        assert_eq!(frozen.boundary_id.as_str(), "boundary");
        assert_eq!(frozen.region_version, region.context_version);
        assert_eq!(frozen.region_digest, region.digest);
    }

    #[test]
    fn all_nine_identity_types_reject_empty_and_whitespace_values() {
        macro_rules! rejects {
            ($type:ident, $field:literal) => {
                assert_eq!(
                    $type::new(""),
                    Err(AdapterError::EmptyIdentity { field: $field })
                );
                assert_eq!(
                    $type::new(" \t\n "),
                    Err(AdapterError::EmptyIdentity { field: $field })
                );
            };
        }
        rejects!(ContextId, "context_id");
        rejects!(ContextSessionId, "context_session_id");
        rejects!(AdapterId, "adapter_id");
        rejects!(AdapterInstanceId, "adapter_instance_id");
        rejects!(AgentInstanceId, "agent_instance_id");
        rejects!(BoundaryId, "boundary_id");
        rejects!(InferenceRequestId, "inference_request_id");
        rejects!(DeliveryId, "delivery_id");
        rejects!(RegionDigest, "region_digest");
    }

    #[test]
    fn all_nine_identity_types_preserve_nonempty_values() {
        assert_eq!(ContextId::new("ctx").expect("valid").as_str(), "ctx");
        assert_eq!(
            ContextSessionId::new("session").expect("valid").as_str(),
            "session"
        );
        assert_eq!(
            AdapterId::new("adapter").expect("valid").as_str(),
            "adapter"
        );
        assert_eq!(
            AdapterInstanceId::new("adapter-instance")
                .expect("valid")
                .as_str(),
            "adapter-instance"
        );
        assert_eq!(
            AgentInstanceId::new("agent-instance")
                .expect("valid")
                .as_str(),
            "agent-instance"
        );
        assert_eq!(
            BoundaryId::new("boundary").expect("valid").as_str(),
            "boundary"
        );
        assert_eq!(
            InferenceRequestId::new("request").expect("valid").as_str(),
            "request"
        );
        assert_eq!(
            DeliveryId::new("delivery").expect("valid").as_str(),
            "delivery"
        );
        assert_eq!(
            RegionDigest::new("digest").expect("valid").as_str(),
            "digest"
        );
    }

    #[test]
    fn materialization_aligns_snapshot_version_bytes_entries_and_digest() {
        let snapshot = one_entry_snapshot();
        let region = materialize_managed_region(&snapshot, &budget()).expect("fits");
        assert_eq!(region.context_id.as_str(), "context-1");
        assert_eq!(region.context_version, snapshot.context_version);
        assert_eq!(region.rendered_bytes, snapshot.rendered_bytes);
        assert_eq!(region.entry_count, snapshot.entries.len());
        assert_eq!(region.digest.as_str().len(), 16);
        assert!(region
            .digest
            .as_str()
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte)));
    }

    #[test]
    fn materialization_rejects_byte_budget_without_truncating_actual() {
        let snapshot = one_entry_snapshot();
        let actual = snapshot.rendered_bytes;
        let too_small = Budget {
            max_rendered_bytes: actual.saturating_sub(1),
            max_entries: 10,
        };
        assert_eq!(
            materialize_managed_region(&snapshot, &too_small),
            Err(AdapterError::BudgetExceeded {
                limit: actual.saturating_sub(1),
                actual,
            })
        );
    }

    #[test]
    fn materialization_rejects_entry_budget() {
        let snapshot = one_entry_snapshot();
        assert_eq!(
            materialize_managed_region(
                &snapshot,
                &Budget {
                    max_rendered_bytes: 1024,
                    max_entries: 0,
                }
            ),
            Err(AdapterError::BudgetExceeded {
                limit: 0,
                actual: 1,
            })
        );
    }

    #[test]
    fn materialization_accepts_empty_snapshot() {
        let snapshot = snapshot_with_entries(&[]);
        let region = materialize_managed_region(&snapshot, &budget()).expect("empty fits");
        assert_eq!(region.rendered_bytes, 0);
        assert_eq!(region.entry_count, 0);
        assert_eq!(region.context_version, snapshot.context_version);
    }

    #[test]
    fn managed_region_accepts_clean_content() {
        assert_eq!(
            assert_region_isolation(ContextRegion::BrainManagedMemory, "remembered facts"),
            Ok(())
        );
    }

    #[test]
    fn managed_region_rejects_system_marker_leak() {
        assert_eq!(
            assert_region_isolation(
                ContextRegion::BrainManagedMemory,
                "text <|system|> protected"
            ),
            Err(AdapterError::ProtectedRegionLeak {
                marker: "<|system|>",
            })
        );
    }

    #[test]
    fn all_six_protected_regions_reject_writes() {
        let protected = [
            ContextRegion::SystemInstructions,
            ContextRegion::DeveloperInstructions,
            ContextRegion::AgentSafetyPolicy,
            ContextRegion::ToolSchemasAndAuthorization,
            ContextRegion::UserInput,
            ContextRegion::AgentWorkingState,
        ];
        for region in protected {
            assert_eq!(
                assert_region_isolation(region, "content"),
                Err(AdapterError::ProtectedRegionMutation(region))
            );
        }
    }

    #[test]
    fn repeated_materialization_has_deterministic_digest() {
        let snapshot = one_entry_snapshot();
        let first = materialize_managed_region(&snapshot, &budget()).expect("first");
        let second = materialize_managed_region(&snapshot, &budget()).expect("second");
        assert_eq!(first.digest, second.digest);
    }

    #[test]
    fn changing_entry_content_hash_changes_digest() {
        let first_snapshot = one_entry_snapshot();
        let mut second_snapshot = first_snapshot.clone();
        second_snapshot.entries[0].content_hash = "hash-b".into();

        let first = materialize_managed_region(&first_snapshot, &budget()).expect("first");
        let second = materialize_managed_region(&second_snapshot, &budget()).expect("second");
        assert_ne!(first.digest, second.digest);
    }

    #[test]
    fn metadata_equal_but_content_hash_different_changes_digest() {
        let first_snapshot = one_entry_snapshot();
        let mut second_snapshot = first_snapshot.clone();
        second_snapshot.entries[0].content_hash = "different-content-hash".into();

        assert_eq!(
            first_snapshot.context_version,
            second_snapshot.context_version
        );
        assert_eq!(
            first_snapshot.rendered_bytes,
            second_snapshot.rendered_bytes
        );
        assert_eq!(first_snapshot.entries.len(), second_snapshot.entries.len());
        assert_eq!(
            first_snapshot.entries[0].entry_id,
            second_snapshot.entries[0].entry_id
        );

        let first = materialize_managed_region(&first_snapshot, &budget()).expect("first");
        let second = materialize_managed_region(&second_snapshot, &budget()).expect("second");
        assert_ne!(first.digest, second.digest);
    }

    #[test]
    fn digest_is_order_sensitive_for_identical_entries_in_different_order() {
        // Entry order is deliberately significant: the digest commits to the
        // exact snapshot sequence, not merely to an unordered set of entries.
        let first_snapshot = snapshot_with_entries(&[
            ("entry-a", "memory-a", "version-a", "hash-a", 1),
            ("entry-b", "memory-b", "version-b", "hash-b", 1),
        ]);
        let second_snapshot = snapshot_with_entries(&[
            ("entry-b", "memory-b", "version-b", "hash-b", 1),
            ("entry-a", "memory-a", "version-a", "hash-a", 1),
        ]);
        let first = materialize_managed_region(&first_snapshot, &budget()).expect("first");
        let second = materialize_managed_region(&second_snapshot, &budget()).expect("second");
        assert_ne!(first.digest, second.digest);
    }

    #[test]
    fn evidence_stages_are_distinct_observations() {
        assert_ne!(EvidenceStage::Received, EvidenceStage::Accepted);
        assert_ne!(EvidenceStage::Accepted, EvidenceStage::Applied);
        assert_ne!(EvidenceStage::Received, EvidenceStage::Applied);
        // No From conversion exists: stages cannot be promoted by conversion.
    }

    #[test]
    fn full_boundary_apply_accepts_open_managed_region_at_tier_one() {
        assert_eq!(
            validate_full_boundary_apply(
                CapabilityTier::Tier1,
                ContextRegion::BrainManagedMemory,
                &open_state(),
            ),
            Ok(())
        );
    }

    #[test]
    fn full_boundary_apply_rejects_frozen_managed_region_at_tier_one() {
        assert_eq!(
            validate_full_boundary_apply(
                CapabilityTier::Tier1,
                ContextRegion::BrainManagedMemory,
                &frozen_state(),
            ),
            Err(AdapterError::RequestAlreadyFrozen)
        );
    }

    #[test]
    fn full_boundary_apply_rejects_developer_region_when_open() {
        assert_eq!(
            validate_full_boundary_apply(
                CapabilityTier::Tier1,
                ContextRegion::DeveloperInstructions,
                &open_state(),
            ),
            Err(AdapterError::ProtectedRegionMutation(
                ContextRegion::DeveloperInstructions
            ))
        );
    }

    #[test]
    fn malformed_region_digest_is_rejected_during_staging() {
        let mut assembler = RequestAssembler::new(
            BoundaryId::new("boundary").expect("valid"),
            InferenceRequestId::new("request").expect("valid"),
        );
        let mut region =
            materialize_managed_region(&one_entry_snapshot(), &budget()).expect("fits");
        region.digest = RegionDigest::new("NOT-A-VALID-DIGEST").expect("nonempty identity");
        assert_eq!(
            assembler.stage(&region),
            Err(AdapterError::InvalidRegionDigest)
        );
    }

    #[test]
    fn applying_a_valid_successor_updates_the_applied_version() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "first"))
            .unwrap();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(2, "second"))
            .unwrap();

        let applied = adapter.applied_snapshot("session-a").unwrap();
        assert_eq!(applied.version(), 2);
        assert_eq!(applied.content(), "second");
    }

    #[test]
    fn stale_or_skipped_versions_return_typed_error_without_mutation() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "accepted"))
            .unwrap();

        assert_eq!(
            adapter.apply("session-a", DeliveryPayload::new_for_test(1, "stale")),
            Err(AdapterError::VersionMismatch {
                expected: 2,
                received: 1
            })
        );
        assert_eq!(
            adapter.apply("session-a", DeliveryPayload::new_for_test(3, "skipped")),
            Err(AdapterError::VersionGap {
                current: 1,
                received: 3
            })
        );
        assert_eq!(adapter.applied_snapshot("session-a").unwrap().version, 1);
        assert_eq!(
            adapter.applied_snapshot("session-a").unwrap().content,
            "accepted"
        );
    }

    #[test]
    fn clear_resets_the_session_so_apply_starts_from_empty() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "old-1"))
            .unwrap();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(2, "old-2"))
            .unwrap();

        adapter.clear("session-a").unwrap();
        assert!(adapter.applied_snapshot("session-a").is_none());

        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "fresh"))
            .unwrap();
        let applied = adapter.applied_snapshot("session-a").unwrap();
        assert_eq!(applied.version, 1);
        assert_eq!(applied.content, "fresh");
    }

    #[test]
    fn reconnect_reports_last_applied_version_not_a_rejected_attempt() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter
            .apply("session-a", DeliveryPayload::new_for_test(1, "committed"))
            .unwrap();
        adapter.disconnect("session-a").unwrap();

        assert_eq!(
            adapter.apply(
                "session-a",
                DeliveryPayload::new_for_test(2, "not-delivered")
            ),
            Err(AdapterError::SessionDisconnected {
                session_id: "session-a".into()
            })
        );
        assert_eq!(adapter.reconnect("session-a"), Ok(Some(1)));
        assert_eq!(adapter.applied_snapshot("session-a").unwrap().version, 1);
    }
}
