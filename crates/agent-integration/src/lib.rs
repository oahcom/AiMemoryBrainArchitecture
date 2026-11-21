//! Deterministic Agent Integration reference model.
//!
//! This crate does not perform model inference, network transport, persistence,
//! BMCP negotiation, or production telemetry.

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
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AdapterError {
    TierInsufficient {
        required: CapabilityTier,
        actual: CapabilityTier,
    },
    ProtectedRegionMutation(ContextRegion),
    RequestAlreadyFrozen,
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
}
