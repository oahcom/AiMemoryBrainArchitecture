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
}

/// Check whether an adapter tier is sufficient for an operation.
pub fn authorize(actual: CapabilityTier, operation: AdapterOperation) -> Result<(), AdapterError> {
    let required = operation.required_tier();
    if actual <= required {
        Ok(())
    } else {
        Err(AdapterError::TierInsufficient { required, actual })
    }
}

/// Validate a proposed write to the inference request's context.
///
/// Only the Brain-managed memory region is writable. Once the request is
/// frozen for submission, even that region is immutable.
pub fn validate_context_write(
    region: ContextRegion,
    request_frozen: bool,
) -> Result<(), AdapterError> {
    if region != ContextRegion::BrainManagedMemory {
        return Err(AdapterError::ProtectedRegionMutation(region));
    }
    if request_frozen {
        return Err(AdapterError::RequestAlreadyFrozen);
    }
    Ok(())
}

/// Apply the deterministic checks required before a full-boundary memory write.
///
/// This validates permission and boundary conditions only; it does not mutate
/// a real Agent request or invoke an inference runtime.
pub fn validate_full_boundary_apply(
    tier: CapabilityTier,
    region: ContextRegion,
    request_frozen: bool,
) -> Result<(), AdapterError> {
    authorize(tier, AdapterOperation::ApplyFullBoundaryMemory)?;
    validate_context_write(region, request_frozen)
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
                false,
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
                true,
            ),
            Err(AdapterError::RequestAlreadyFrozen)
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
