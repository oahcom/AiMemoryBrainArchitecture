//! Deterministic Agent Integration reference model.
//!
//! This crate does not perform model inference, network transport, persistence,
//! BMCP negotiation, or production telemetry.

use std::collections::BTreeMap;

pub use memory_context::ContextSnapshot;
use memory_context::{validate_snapshot, ContextError};

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
    /// The supplied canonical memory-context snapshot failed validation.
    InvalidSnapshot(ContextError),
    /// The caller attempted delivery while this session was disconnected.
    SessionDisconnected {
        session_id: String,
    },
    /// The supplied snapshot is not the exact next context version.
    VersionMismatch {
        expected: u64,
        received: u64,
    },
    /// The current context version cannot be incremented without wrapping.
    VersionExhausted,
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
pub fn validate_full_boundary_apply(
    tier: CapabilityTier,
    region: ContextRegion,
    request_frozen: bool,
) -> Result<(), AdapterError> {
    authorize(tier, AdapterOperation::ApplyFullBoundaryMemory)?;
    validate_context_write(region, request_frozen)
}

/// Session-scoped delivery contract.
///
/// The payload is the canonical `memory_context::ContextSnapshot`; this crate
/// does not define a parallel snapshot representation. Versions come directly
/// from `context_version`, begin at 1 for a new or cleared session, and must
/// advance by exactly one after each accepted apply.
pub trait ContextDeliveryAdapter {
    fn apply(&mut self, session_id: &str, snapshot: ContextSnapshot) -> Result<(), AdapterError>;

    fn clear(&mut self, session_id: &str) -> Result<(), AdapterError>;

    fn disconnect(&mut self, session_id: &str) -> Result<(), AdapterError>;

    fn reconnect(&mut self, session_id: &str) -> Result<Option<u64>, AdapterError>;

    /// Read the exact canonical snapshot currently recorded as applied.
    fn applied_snapshot(&self, session_id: &str) -> Option<&ContextSnapshot>;
}

#[derive(Debug)]
struct SessionState {
    applied: Option<ContextSnapshot>,
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
    fn apply(&mut self, session_id: &str, snapshot: ContextSnapshot) -> Result<(), AdapterError> {
        if self
            .sessions
            .get(session_id)
            .is_some_and(|state| !state.connected)
        {
            return Err(AdapterError::SessionDisconnected {
                session_id: session_id.to_owned(),
            });
        }

        validate_snapshot(&snapshot).map_err(AdapterError::InvalidSnapshot)?;

        let expected = match self.sessions.get(session_id).and_then(|state| state.applied.as_ref()) {
            Some(applied) => applied
                .context_version
                .checked_add(1)
                .ok_or(AdapterError::VersionExhausted)?,
            None => 1,
        };
        if snapshot.context_version != expected {
            return Err(AdapterError::VersionMismatch {
                expected,
                received: snapshot.context_version,
            });
        }

        self.sessions
            .entry(session_id.to_owned())
            .or_default()
            .applied = Some(snapshot);
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
        Ok(state
            .applied
            .as_ref()
            .map(|snapshot| snapshot.context_version))
    }

    fn applied_snapshot(&self, session_id: &str) -> Option<&ContextSnapshot> {
        self.sessions.get(session_id)?.applied.as_ref()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_context::{build_context, ContextBudget, ContextIdentity};
    use memory_domain::{OpaqueId, ScopeKind, ScopeRef};

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn build_snapshot(context_version: u64) -> ContextSnapshot {
        build_context(
            ContextIdentity {
                context_id: id("context-a"),
                scope_refs: vec![ScopeRef {
                    scope_id: id("scope-a"),
                    scope_kind: ScopeKind::User,
                    namespace_key: "user:scope-a".into(),
                }],
                agent_id: id("agent-a"),
                agent_instance_id: id("agent-instance-a"),
                session_id: id("canonical-session-a"),
                task_id: None,
                environment_id: None,
                purpose: "inference-context".into(),
                schema_version: "1".into(),
            },
            context_version,
            ContextBudget {
                max_entries: 8,
                max_rendered_bytes: 4096,
            },
            Vec::new(),
        )
        .unwrap()
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
        adapter.apply("session-a", build_snapshot(1)).unwrap();
        adapter.apply("session-a", build_snapshot(2)).unwrap();

        let applied = adapter.applied_snapshot("session-a").unwrap();
        assert_eq!(applied.context_version, 2);
        assert_eq!(applied, &build_snapshot(2));
    }

    #[test]
    fn stale_or_skipped_versions_return_typed_error_without_mutation() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        let accepted = build_snapshot(1);
        adapter.apply("session-a", accepted.clone()).unwrap();

        assert_eq!(
            adapter.apply("session-a", build_snapshot(1)),
            Err(AdapterError::VersionMismatch {
                expected: 2,
                received: 1
            })
        );
        assert_eq!(
            adapter.apply("session-a", build_snapshot(3)),
            Err(AdapterError::VersionMismatch {
                expected: 2,
                received: 3
            })
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&accepted));
    }

    #[test]
    fn clear_resets_the_session_so_apply_starts_from_empty() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        adapter.apply("session-a", build_snapshot(1)).unwrap();
        adapter.apply("session-a", build_snapshot(2)).unwrap();

        adapter.clear("session-a").unwrap();
        assert!(adapter.applied_snapshot("session-a").is_none());

        let fresh = build_snapshot(1);
        adapter.apply("session-a", fresh.clone()).unwrap();
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&fresh));
    }

    #[test]
    fn reconnect_reports_last_applied_version_not_a_rejected_attempt() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        let committed = build_snapshot(1);
        adapter.apply("session-a", committed.clone()).unwrap();
        adapter.disconnect("session-a").unwrap();

        assert_eq!(
            adapter.apply("session-a", build_snapshot(2)),
            Err(AdapterError::SessionDisconnected {
                session_id: "session-a".into()
            })
        );
        assert_eq!(adapter.reconnect("session-a"), Ok(Some(1)));
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&committed));
    }

    #[test]
    fn build_context_apply_and_readback_preserve_the_exact_canonical_snapshot() {
        let built = build_snapshot(1);
        let mut adapter = InMemoryContextDeliveryAdapter::default();

        adapter.apply("session-a", built.clone()).unwrap();

        assert_eq!(adapter.applied_snapshot("session-a"), Some(&built));
        assert_eq!(
            adapter.applied_snapshot("session-a").unwrap().context_version,
            built.context_version
        );
    }

    #[test]
    fn invalid_snapshot_is_typed_refusal_and_does_not_change_applied_state() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        let accepted = build_snapshot(1);
        adapter.apply("session-a", accepted.clone()).unwrap();

        let mut invalid = build_snapshot(2);
        invalid.rendered_bytes = 1;
        assert_eq!(
            adapter.apply("session-a", invalid),
            Err(AdapterError::InvalidSnapshot(
                ContextError::SnapshotByteCountMismatch {
                    actual: 0,
                    recorded: 1
                }
            ))
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&accepted));
    }

    #[test]
    fn non_successor_context_version_reports_actual_versions_without_mutation() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        let accepted = build_snapshot(4);
        adapter.apply("session-a", build_snapshot(1)).unwrap();
        // Establish version 2 before checking the deliberately skipped version.
        adapter.apply("session-a", build_snapshot(2)).unwrap();
        let before = adapter.applied_snapshot("session-a").unwrap().clone();

        assert_eq!(
            adapter.apply("session-a", accepted),
            Err(AdapterError::VersionMismatch {
                expected: 3,
                received: 4
            })
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&before));
    }

    #[test]
    fn apply_after_disconnect_is_rejected_and_state_is_unchanged() {
        let mut adapter = InMemoryContextDeliveryAdapter::default();
        let accepted = build_snapshot(1);
        adapter.apply("session-a", accepted.clone()).unwrap();
        adapter.disconnect("session-a").unwrap();

        assert_eq!(
            adapter.apply("session-a", build_snapshot(2)),
            Err(AdapterError::SessionDisconnected {
                session_id: "session-a".into()
            })
        );
        assert_eq!(adapter.applied_snapshot("session-a"), Some(&accepted));
    }
}
