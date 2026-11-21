//! Deterministic Agent Integration reference model.
//!
//! This crate does not perform model inference, network transport, persistence,
//! BMCP negotiation, or production telemetry.

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
    SessionDisconnected { session_id: String },
    /// The supplied snapshot is not the exact next version for this session.
    VersionMismatch { expected: u64, received: u64 },
    /// The current version cannot be incremented without wrapping.
    VersionExhausted,
}

/// Check whether an adapter tier is sufficient for an operation.
pub fn authorize(
    actual: CapabilityTier,
    operation: AdapterOperation,
) -> Result<(), AdapterError> {
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

/// An immutable, versioned context payload delivered to one session.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ContextSnapshot {
    pub version: u64,
    pub content: String,
}

impl ContextSnapshot {
    pub fn new(version: u64, content: impl Into<String>) -> Self {
        Self { version, content: content.into() }
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
        snapshot: ContextSnapshot,
    ) -> Result<(), AdapterError>;

    fn clear(&mut self, session_id: &str) -> Result<(), AdapterError>;

    fn disconnect(&mut self, session_id: &str) -> Result<(), AdapterError>;

    fn reconnect(&mut self, session_id: &str) -> Result<Option<u64>, AdapterError>;

    /// Read the payload currently recorded as applied for this session.
    fn applied_snapshot(&self, session_id: &str) -> Option<&ContextSnapshot>;
}

#[derive(Debug)]
struct SessionState {
    applied: Option<ContextSnapshot>,
    connected: bool,
}

impl Default for SessionState {
    fn default() -> Self {
        Self { applied: None, connected: true }
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
        snapshot: ContextSnapshot,
    ) -> Result<(), AdapterError> {
        let state = self.sessions.entry(session_id.to_owned()).or_default();
        if !state.connected {
            return Err(AdapterError::SessionDisconnected {
                session_id: session_id.to_owned(),
            });
        }

        let expected = match state.applied.as_ref() {
            Some(applied) => applied.version.checked_add(1).ok_or(AdapterError::VersionExhausted)?,
            None => 1,
        };
        if snapshot.version != expected {
            return Err(AdapterError::VersionMismatch {
                expected,
                received: snapshot.version,
            });
        }

        state.applied = Some(snapshot);
        Ok(())
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

    fn applied_snapshot(&self, session_id: &str) -> Option<&ContextSnapshot> {
        self.sessions.get(session_id)?.applied.as_ref()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn legal_tier_three_telemetry_call_is_allowed() {
        assert_eq!(
            authorize(CapabilityTier::Tier3, AdapterOperation::SubmitScopedTelemetry),
            Ok(())
        );
    }

    #[test]
    fn insufficient_tier_is_rejected_with_typed_error() {
        assert_eq!(
            authorize(CapabilityTier::Tier3, AdapterOperation::ObserveFullInferenceBoundary),
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
        adapter.apply("session-a", ContextSnapshot::new(1, "first")).unwrap();
        adapter.apply("session-a", ContextSnapshot::new(2, "second")).unwrap();

        let applied = adapter.applied_snapshot("session-a").unwrap();
        assert_eq!(applied.version, 2);
        assert_eq!(applied.content, "second");
    }

    #[test]
    fn stale_or_skipped_versions_return_typed_error_without_mutation() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter.apply("session-a", ContextSnapshot::new(1, "accepted")).unwrap();

        assert_eq!(
            adapter.apply("session-a", ContextSnapshot::new(1, "stale")),
            Err(AdapterError::VersionMismatch { expected: 2, received: 1 })
        );
        assert_eq!(
            adapter.apply("session-a", ContextSnapshot::new(3, "skipped")),
            Err(AdapterError::VersionMismatch { expected: 2, received: 3 })
        );
        assert_eq!(adapter.applied_snapshot("session-a").unwrap().version, 1);
        assert_eq!(adapter.applied_snapshot("session-a").unwrap().content, "accepted");
    }

    #[test]
    fn clear_resets_the_session_so_apply_starts_from_empty() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter.apply("session-a", ContextSnapshot::new(1, "old-1")).unwrap();
        adapter.apply("session-a", ContextSnapshot::new(2, "old-2")).unwrap();

        adapter.clear("session-a").unwrap();
        assert!(adapter.applied_snapshot("session-a").is_none());

        adapter.apply("session-a", ContextSnapshot::new(1, "fresh")).unwrap();
        let applied = adapter.applied_snapshot("session-a").unwrap();
        assert_eq!(applied.version, 1);
        assert_eq!(applied.content, "fresh");
    }

    #[test]
    fn reconnect_reports_last_applied_version_not_a_rejected_attempt() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter.apply("session-a", ContextSnapshot::new(1, "committed")).unwrap();
        adapter.disconnect("session-a").unwrap();

        assert_eq!(
            adapter.apply("session-a", ContextSnapshot::new(2, "not-delivered")),
            Err(AdapterError::SessionDisconnected { session_id: "session-a".into() })
        );
        assert_eq!(adapter.reconnect("session-a"), Ok(Some(1)));
        assert_eq!(adapter.applied_snapshot("session-a").unwrap().version, 1);
    }
}
