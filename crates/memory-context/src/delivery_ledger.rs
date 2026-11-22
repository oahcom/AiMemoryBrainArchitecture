//! Delivery attempt ledger: attempt identity, retries, ACK separation,
//! late acknowledgements and supersession.
//!
//! Two design documents meet here:
//!
//! * `context-manager.md` §4 — T2 delivery attempt is *separate* from the T1
//!   Context commit, retries retain the logical Delivery id, and a timeout is
//!   Unknown rather than Applied.
//! * `context-versioning.md` §9 — Prepared → Delivered → Applied with Rejected,
//!   Expired and Superseded alternatives, where a late Applied for a superseded
//!   version is historical evidence and cannot roll the desired head backward.
//! * `phase-3.7…md` §4 — attempts are immutable, a retry creates a *new*
//!   attempt, and queue insertion, dispatch and transport ACK are separate
//!   stages: delivered does not mean materialized and materialized does not mean
//!   applied.
//!
//! The ledger models exactly that: an append-only list of attempts per delivery,
//! one explicit head per delivery, and a typed result for every operation that
//! could otherwise be mistaken for progress.

use crate::{ContextError, DeliveryIntent, OpaqueId};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Identity of one immutable delivery attempt.
#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd, Serialize, Deserialize)]
pub struct DeliveryAttemptId(String);

impl DeliveryAttemptId {
    /// Build an attempt id. Empty identifiers are rejected.
    pub fn new(value: impl Into<String>) -> Result<Self, ContextError> {
        let value = value.into();
        if value.trim().is_empty() {
            return Err(ContextError::EmptyField("delivery_attempt_id"));
        }
        Ok(Self(value))
    }

    /// The identifier as a string slice.
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// The exact authorization/fence/capability boundary an attempt was opened under.
///
/// A retry must revalidate these; the ledger records them so a caller can prove
/// which boundary produced a given attempt instead of assuming the current one.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DeliveryBoundary {
    pub adapter_id: OpaqueId,
    pub session_id: OpaqueId,
    pub permission_epoch: u64,
    pub forget_fence_cursor: u64,
    pub capability_epoch: String,
}

impl DeliveryBoundary {
    fn validate(&self) -> Result<(), ContextError> {
        if self.permission_epoch == 0 {
            return Err(ContextError::InvalidVersion);
        }
        if self.capability_epoch.trim().is_empty() {
            return Err(ContextError::EmptyField("capability_epoch"));
        }
        Ok(())
    }
}

/// What one attempt targets.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DeliveryAttemptDescriptor {
    pub delivery_id: OpaqueId,
    pub context_id: OpaqueId,
    pub target_context_version: u64,
    pub boundary: DeliveryBoundary,
}

impl DeliveryAttemptDescriptor {
    fn validate(&self) -> Result<(), ContextError> {
        if self.target_context_version == 0 {
            return Err(ContextError::InvalidVersion);
        }
        self.boundary.validate()
    }
}

/// The stage an attempt has reached.
///
/// `UnknownOutcome` exists because a timeout is neither a rejection nor an
/// application; collapsing it into either would be a correctness bug.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum DeliveryAttemptState {
    /// Package materialized and authorized, not confirmed sent.
    Prepared,
    /// Handed to the transport, no receipt yet.
    Dispatched,
    /// Transport or receiver receipt only. Does not mean materialized or applied.
    TransportAcknowledged,
    /// Timeout, lost ACK or otherwise unobservable result.
    UnknownOutcome { reason: String },
    /// The Adapter refused the payload or validation failed.
    Rejected { reason: String },
    /// TTL elapsed before a valid application.
    Expired,
    /// A newer target replaced this attempt before it was applied.
    Superseded,
}

impl DeliveryAttemptState {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::Prepared => "prepared",
            Self::Dispatched => "dispatched",
            Self::TransportAcknowledged => "transport_acknowledged",
            Self::UnknownOutcome { .. } => "unknown_outcome",
            Self::Rejected { .. } => "rejected",
            Self::Expired => "expired",
            Self::Superseded => "superseded",
        }
    }

    /// `true` when no further transition may occur.
    pub fn is_terminal(&self) -> bool {
        matches!(
            self,
            Self::Rejected { .. } | Self::Expired | Self::Superseded
        )
    }
}

/// Explicit proof that the Adapter materialized an exact Context version.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct AppliedProof {
    pub applied_context_version: u64,
    /// Adapter-side digest attesting the applied region.
    pub digest: String,
}

/// One immutable attempt record.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DeliveryAttempt {
    pub attempt_id: DeliveryAttemptId,
    /// 1-based retry ordinal within one delivery.
    pub ordinal: u32,
    pub descriptor: DeliveryAttemptDescriptor,
    pub state: DeliveryAttemptState,
    pub applied: Option<AppliedProof>,
    /// Every state the attempt passed through, in order.
    pub history: Vec<DeliveryAttemptState>,
    /// Transport receipts, including receipts that arrived too late to matter.
    pub transport_receipts: Vec<String>,
}

impl DeliveryAttempt {
    /// `true` when an explicit Applied proof exists for this attempt.
    pub fn is_applied(&self) -> bool {
        self.applied.is_some()
    }
}

/// Which head an acknowledgement was correlated against.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum LateAckDisposition {
    /// The acknowledgement belongs to the current attempt.
    Current,
    /// The acknowledgement is historical evidence only.
    Historical { superseded_by_ordinal: u32 },
}

impl LateAckDisposition {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::Current => "current",
            Self::Historical { .. } => "historical",
        }
    }
}

/// Where an Applied proof landed relative to the desired head.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum AppliedDisposition {
    /// The proof applies to the current target.
    Current,
    /// The proof is historical: the desired head has moved on.
    Historical { head_target_context_version: u64 },
}

impl AppliedDisposition {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::Current => "current",
            Self::Historical { .. } => "historical",
        }
    }
}

/// The desired head of one delivery.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
struct DeliveryHead {
    ordinal: u32,
    target_context_version: u64,
}

/// Append-only attempt ledger with one explicit head per delivery.
#[derive(Clone, Debug, Default, Eq, PartialEq, Serialize, Deserialize)]
pub struct DeliveryAttemptLedger {
    attempts: Vec<DeliveryAttempt>,
    heads: HashMap<OpaqueId, DeliveryHead>,
}

impl DeliveryAttemptLedger {
    /// An empty ledger.
    pub fn new() -> Self {
        Self::default()
    }

    /// Open a new attempt for a delivery.
    ///
    /// A retry always appends a new attempt with the next ordinal; existing
    /// attempts are never rewritten or merged.
    ///
    /// # Errors
    ///
    /// Rejects a malformed descriptor, and rejects a target version lower than the
    /// current head so a stale plan cannot rewind the desired head.
    pub fn open_attempt(
        &mut self,
        descriptor: DeliveryAttemptDescriptor,
    ) -> Result<DeliveryAttemptId, ContextError> {
        descriptor.validate()?;
        let previous = self.heads.get(&descriptor.delivery_id).cloned();
        if let Some(head) = &previous {
            if descriptor.target_context_version < head.target_context_version {
                return Err(ContextError::ContextVersionRegression {
                    current: head.target_context_version,
                    requested: descriptor.target_context_version,
                });
            }
        }
        let ordinal = previous.as_ref().map_or(1, |head| head.ordinal + 1);
        let attempt_id = DeliveryAttemptId::new(format!(
            "{}:attempt:{ordinal}",
            descriptor.delivery_id.as_str()
        ))?;
        if self
            .attempts
            .iter()
            .any(|attempt| attempt.attempt_id == attempt_id)
        {
            return Err(ContextError::DeliveryAttemptConflict(
                "duplicate_attempt_id",
            ));
        }
        self.attempts.push(DeliveryAttempt {
            attempt_id: attempt_id.clone(),
            ordinal,
            descriptor: descriptor.clone(),
            state: DeliveryAttemptState::Prepared,
            applied: None,
            history: vec![DeliveryAttemptState::Prepared],
            transport_receipts: Vec::new(),
        });
        self.heads.insert(
            descriptor.delivery_id,
            DeliveryHead {
                ordinal,
                target_context_version: descriptor.target_context_version,
            },
        );
        Ok(attempt_id)
    }

    /// Open an attempt directly from a prepared delivery intent.
    pub fn open_attempt_for_intent(
        &mut self,
        intent: &DeliveryIntent,
        boundary: DeliveryBoundary,
    ) -> Result<DeliveryAttemptId, ContextError> {
        self.open_attempt(DeliveryAttemptDescriptor {
            delivery_id: intent.delivery_id.clone(),
            context_id: intent.context_id.clone(),
            target_context_version: intent.target_context_version,
            boundary,
        })
    }

    /// Move a Prepared attempt to Dispatched. Queue insertion and dispatch are
    /// separate from transport acknowledgement by design.
    pub fn dispatch(&mut self, attempt_id: &DeliveryAttemptId) -> Result<(), ContextError> {
        let attempt = self.attempt_mut(attempt_id)?;
        move_to(attempt, DeliveryAttemptState::Dispatched)
    }

    /// Record a transport/receiver receipt for the current attempt.
    ///
    /// The state becomes `TransportAcknowledged`, which deliberately does *not*
    /// mean materialized or applied.
    pub fn record_transport_ack(
        &mut self,
        attempt_id: &DeliveryAttemptId,
        receipt: &str,
    ) -> Result<(), ContextError> {
        if receipt.trim().is_empty() {
            return Err(ContextError::EmptyField("transport_receipt"));
        }
        let attempt = self.attempt_mut(attempt_id)?;
        attempt.transport_receipts.push(receipt.to_owned());
        move_to(attempt, DeliveryAttemptState::TransportAcknowledged)
    }

    /// Correlate an acknowledgement against the current head, recording a late
    /// receipt as historical evidence instead of progress.
    pub fn acknowledge_late(
        &mut self,
        attempt_id: &DeliveryAttemptId,
        receipt: &str,
    ) -> Result<LateAckDisposition, ContextError> {
        if receipt.trim().is_empty() {
            return Err(ContextError::EmptyField("transport_receipt"));
        }
        let (delivery_id, ordinal) = self.attempt_key(attempt_id)?;
        let head_ordinal = self
            .heads
            .get(&delivery_id)
            .map(|head| head.ordinal)
            .ok_or_else(|| ContextError::DeliveryAttemptNotFound(attempt_id.as_str().to_owned()))?;
        let attempt = self.attempt_mut(attempt_id)?;
        attempt.transport_receipts.push(receipt.to_owned());
        if head_ordinal > ordinal {
            return Ok(LateAckDisposition::Historical {
                superseded_by_ordinal: head_ordinal,
            });
        }
        move_to(attempt, DeliveryAttemptState::TransportAcknowledged)?;
        Ok(LateAckDisposition::Current)
    }

    /// Record that the outcome is unobservable. A timeout is Unknown, full stop.
    pub fn record_unknown_outcome(
        &mut self,
        attempt_id: &DeliveryAttemptId,
        reason: &str,
    ) -> Result<(), ContextError> {
        if reason.trim().is_empty() {
            return Err(ContextError::EmptyField("reason"));
        }
        let attempt = self.attempt_mut(attempt_id)?;
        move_to(
            attempt,
            DeliveryAttemptState::UnknownOutcome {
                reason: reason.to_owned(),
            },
        )
    }

    /// Record that the Adapter rejected the payload.
    pub fn record_rejected(
        &mut self,
        attempt_id: &DeliveryAttemptId,
        reason: &str,
    ) -> Result<(), ContextError> {
        if reason.trim().is_empty() {
            return Err(ContextError::EmptyField("reason"));
        }
        let attempt = self.attempt_mut(attempt_id)?;
        move_to(
            attempt,
            DeliveryAttemptState::Rejected {
                reason: reason.to_owned(),
            },
        )
    }

    /// Record that the attempt expired before a valid application.
    pub fn record_expired(&mut self, attempt_id: &DeliveryAttemptId) -> Result<(), ContextError> {
        let attempt = self.attempt_mut(attempt_id)?;
        move_to(attempt, DeliveryAttemptState::Expired)
    }

    /// Record an explicit Applied proof.
    ///
    /// # Errors
    ///
    /// Requires the `TransportAcknowledged` stage, an exact version match between
    /// the proof and the attempt target, a non-empty digest, and no earlier proof.
    pub fn record_applied(
        &mut self,
        attempt_id: &DeliveryAttemptId,
        proof: AppliedProof,
    ) -> Result<AppliedDisposition, ContextError> {
        if proof.digest.trim().is_empty() {
            return Err(ContextError::EmptyField("applied_digest"));
        }
        let (delivery_id, ordinal) = self.attempt_key(attempt_id)?;
        {
            let attempt = self
                .attempts
                .iter()
                .find(|attempt| &attempt.attempt_id == attempt_id)
                .ok_or_else(|| {
                    ContextError::DeliveryAttemptNotFound(attempt_id.as_str().to_owned())
                })?;
            if proof.applied_context_version != attempt.descriptor.target_context_version {
                return Err(ContextError::DeliveryAttemptConflict(
                    "applied_proof_targets_a_different_context_version",
                ));
            }
            if attempt.applied.is_some() {
                return Err(ContextError::DeliveryAttemptConflict(
                    "applied_proof_already_recorded",
                ));
            }
            if attempt.state != DeliveryAttemptState::TransportAcknowledged {
                return Err(ContextError::InvalidDeliveryTransition {
                    from: attempt.state.label(),
                    to: "applied",
                });
            }
        }
        let head =
            self.heads.get(&delivery_id).cloned().ok_or_else(|| {
                ContextError::DeliveryAttemptNotFound(attempt_id.as_str().to_owned())
            })?;
        let attempt = self.attempt_mut(attempt_id)?;
        attempt.applied = Some(proof);
        if head.ordinal > ordinal {
            return Ok(AppliedDisposition::Historical {
                head_target_context_version: head.target_context_version,
            });
        }
        Ok(AppliedDisposition::Current)
    }

    /// The delivery and retry ordinal one attempt belongs to.
    fn attempt_key(&self, attempt_id: &DeliveryAttemptId) -> Result<(OpaqueId, u32), ContextError> {
        self.attempts
            .iter()
            .find(|attempt| &attempt.attempt_id == attempt_id)
            .map(|attempt| (attempt.descriptor.delivery_id.clone(), attempt.ordinal))
            .ok_or_else(|| ContextError::DeliveryAttemptNotFound(attempt_id.as_str().to_owned()))
    }

    /// Supersede every attempt of a delivery that has not been applied, then move
    /// the desired head to the new target version.
    ///
    /// # Errors
    ///
    /// Rejects a target version that does not advance the head.
    pub fn supersede_delivery(
        &mut self,
        delivery_id: &OpaqueId,
        new_target_context_version: u64,
    ) -> Result<Vec<DeliveryAttemptId>, ContextError> {
        if new_target_context_version == 0 {
            return Err(ContextError::InvalidVersion);
        }
        let head = self.heads.get(delivery_id).cloned().ok_or_else(|| {
            ContextError::DeliveryAttemptNotFound(delivery_id.as_str().to_owned())
        })?;
        if new_target_context_version <= head.target_context_version {
            return Err(ContextError::ContextVersionRegression {
                current: head.target_context_version,
                requested: new_target_context_version,
            });
        }
        let mut superseded = Vec::new();
        for attempt in &mut self.attempts {
            if attempt.descriptor.delivery_id != *delivery_id
                || attempt.applied.is_some()
                || attempt.state.is_terminal()
            {
                continue;
            }
            attempt.state = DeliveryAttemptState::Superseded;
            attempt.history.push(DeliveryAttemptState::Superseded);
            superseded.push(attempt.attempt_id.clone());
        }
        self.heads.insert(
            delivery_id.clone(),
            DeliveryHead {
                ordinal: head.ordinal,
                target_context_version: new_target_context_version,
            },
        );
        Ok(superseded)
    }

    /// Look up one attempt.
    pub fn attempt(&self, attempt_id: &DeliveryAttemptId) -> Option<&DeliveryAttempt> {
        self.attempts
            .iter()
            .find(|attempt| &attempt.attempt_id == attempt_id)
    }

    /// Every attempt of a delivery, in ordinal order.
    pub fn attempts_for(&self, delivery_id: &OpaqueId) -> Vec<&DeliveryAttempt> {
        let mut attempts: Vec<&DeliveryAttempt> = self
            .attempts
            .iter()
            .filter(|attempt| &attempt.descriptor.delivery_id == delivery_id)
            .collect();
        attempts.sort_by_key(|attempt| attempt.ordinal);
        attempts
    }

    /// The current attempt of a delivery.
    pub fn head_attempt(&self, delivery_id: &OpaqueId) -> Option<&DeliveryAttempt> {
        let head = self.heads.get(delivery_id)?;
        self.attempts.iter().find(|attempt| {
            &attempt.descriptor.delivery_id == delivery_id && attempt.ordinal == head.ordinal
        })
    }

    /// The desired head target version of a delivery.
    pub fn head_target_version(&self, delivery_id: &OpaqueId) -> Option<u64> {
        self.heads
            .get(delivery_id)
            .map(|head| head.target_context_version)
    }

    /// Highest provably applied version of a delivery, if any.
    pub fn applied_high_water(&self, delivery_id: &OpaqueId) -> Option<u64> {
        self.attempts
            .iter()
            .filter(|attempt| &attempt.descriptor.delivery_id == delivery_id)
            .filter_map(|attempt| {
                attempt
                    .applied
                    .as_ref()
                    .map(|proof| proof.applied_context_version)
            })
            .max()
    }

    /// Number of attempts whose outcome is explicitly Unknown.
    pub fn unknown_outcome_count(&self) -> usize {
        self.attempts
            .iter()
            .filter(|attempt| matches!(attempt.state, DeliveryAttemptState::UnknownOutcome { .. }))
            .count()
    }

    /// Total number of attempts recorded.
    pub fn total_attempts(&self) -> usize {
        self.attempts.len()
    }

    fn attempt_mut(
        &mut self,
        attempt_id: &DeliveryAttemptId,
    ) -> Result<&mut DeliveryAttempt, ContextError> {
        self.attempts
            .iter_mut()
            .find(|attempt| &attempt.attempt_id == attempt_id)
            .ok_or_else(|| ContextError::DeliveryAttemptNotFound(attempt_id.as_str().to_owned()))
    }
}

/// The only legal forward edges of the attempt machine.
fn move_to(attempt: &mut DeliveryAttempt, next: DeliveryAttemptState) -> Result<(), ContextError> {
    let allowed = matches!(
        (&attempt.state, &next),
        (
            DeliveryAttemptState::Prepared,
            DeliveryAttemptState::Dispatched
        ) | (
            DeliveryAttemptState::Dispatched,
            DeliveryAttemptState::TransportAcknowledged
        ) | (
            DeliveryAttemptState::Dispatched,
            DeliveryAttemptState::UnknownOutcome { .. }
        ) | (
            DeliveryAttemptState::TransportAcknowledged,
            DeliveryAttemptState::UnknownOutcome { .. }
        ) | (
            DeliveryAttemptState::Prepared,
            DeliveryAttemptState::Rejected { .. }
        ) | (
            DeliveryAttemptState::Dispatched,
            DeliveryAttemptState::Rejected { .. }
        ) | (
            DeliveryAttemptState::TransportAcknowledged,
            DeliveryAttemptState::Rejected { .. }
        ) | (
            DeliveryAttemptState::Prepared,
            DeliveryAttemptState::Expired
        ) | (
            DeliveryAttemptState::Dispatched,
            DeliveryAttemptState::Expired
        ) | (
            DeliveryAttemptState::UnknownOutcome { .. },
            DeliveryAttemptState::Expired
        )
    );
    if !allowed {
        return Err(ContextError::InvalidDeliveryTransition {
            from: attempt.state.label(),
            to: next.label(),
        });
    }
    attempt.state = next.clone();
    attempt.history.push(next);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn boundary() -> DeliveryBoundary {
        DeliveryBoundary {
            adapter_id: id("adapter"),
            session_id: id("session"),
            permission_epoch: 7,
            forget_fence_cursor: 3,
            capability_epoch: "cap-1".into(),
        }
    }

    fn descriptor(delivery: &str, version: u64) -> DeliveryAttemptDescriptor {
        DeliveryAttemptDescriptor {
            delivery_id: id(delivery),
            context_id: id("context"),
            target_context_version: version,
            boundary: boundary(),
        }
    }

    #[test]
    fn a_retry_appends_a_new_attempt_and_never_rewrites_the_previous_one() {
        let mut ledger = DeliveryAttemptLedger::new();
        let first = ledger.open_attempt(descriptor("delivery", 1)).unwrap();
        let second = ledger.open_attempt(descriptor("delivery", 1)).unwrap();
        assert_eq!(first.as_str(), "delivery:attempt:1");
        assert_eq!(second.as_str(), "delivery:attempt:2");
        assert_eq!(ledger.total_attempts(), 2);
        assert_eq!(ledger.attempts_for(&id("delivery")).len(), 2);
        // The first attempt is still Prepared: a retry is not progress on it.
        assert_eq!(
            ledger.attempt(&first).unwrap().state,
            DeliveryAttemptState::Prepared
        );
        assert_eq!(ledger.head_attempt(&id("delivery")).unwrap().ordinal, 2);
    }

    #[test]
    fn a_stale_target_cannot_rewind_the_desired_head() {
        let mut ledger = DeliveryAttemptLedger::new();
        ledger.open_attempt(descriptor("delivery", 5)).unwrap();
        assert_eq!(
            ledger.open_attempt(descriptor("delivery", 4)),
            Err(ContextError::ContextVersionRegression {
                current: 5,
                requested: 4,
            })
        );
    }

    #[test]
    fn transport_acknowledgement_is_not_application() {
        let mut ledger = DeliveryAttemptLedger::new();
        let attempt = ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        ledger.dispatch(&attempt).unwrap();
        ledger.record_transport_ack(&attempt, "receipt-1").unwrap();
        let record = ledger.attempt(&attempt).unwrap();
        assert_eq!(record.state, DeliveryAttemptState::TransportAcknowledged);
        assert!(!record.is_applied());
        assert_eq!(
            record.history,
            vec![
                DeliveryAttemptState::Prepared,
                DeliveryAttemptState::Dispatched,
                DeliveryAttemptState::TransportAcknowledged,
            ]
        );
    }

    #[test]
    fn a_timeout_is_unknown_not_rejected_and_not_applied() {
        let mut ledger = DeliveryAttemptLedger::new();
        let attempt = ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        ledger.dispatch(&attempt).unwrap();
        ledger
            .record_unknown_outcome(&attempt, "ack timeout")
            .unwrap();
        assert_eq!(ledger.unknown_outcome_count(), 1);
        assert!(!ledger.attempt(&attempt).unwrap().is_applied());
        assert_eq!(
            ledger.attempt(&attempt).unwrap().state.label(),
            "unknown_outcome"
        );
    }

    #[test]
    fn an_applied_proof_must_match_the_attempt_target_and_arrive_once() {
        let mut ledger = DeliveryAttemptLedger::new();
        let attempt = ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        ledger.dispatch(&attempt).unwrap();
        ledger.record_transport_ack(&attempt, "receipt-1").unwrap();
        // Wrong version is a conflict, not a silent accept.
        assert_eq!(
            ledger.record_applied(
                &attempt,
                AppliedProof {
                    applied_context_version: 3,
                    digest: "digest".into(),
                },
            ),
            Err(ContextError::DeliveryAttemptConflict(
                "applied_proof_targets_a_different_context_version"
            ))
        );
        assert_eq!(
            ledger
                .record_applied(
                    &attempt,
                    AppliedProof {
                        applied_context_version: 2,
                        digest: "digest".into(),
                    },
                )
                .unwrap(),
            AppliedDisposition::Current
        );
        // A second proof for the same attempt is refused.
        assert_eq!(
            ledger.record_applied(
                &attempt,
                AppliedProof {
                    applied_context_version: 2,
                    digest: "digest-2".into(),
                },
            ),
            Err(ContextError::DeliveryAttemptConflict(
                "applied_proof_already_recorded"
            ))
        );
        assert_eq!(ledger.applied_high_water(&id("delivery")), Some(2));
    }

    #[test]
    fn applied_before_transport_acknowledgement_is_an_illegal_transition() {
        let mut ledger = DeliveryAttemptLedger::new();
        let attempt = ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        assert_eq!(
            ledger.record_applied(
                &attempt,
                AppliedProof {
                    applied_context_version: 2,
                    digest: "digest".into(),
                },
            ),
            Err(ContextError::InvalidDeliveryTransition {
                from: "prepared",
                to: "applied",
            })
        );
    }

    #[test]
    fn a_late_acknowledgement_for_a_superseded_attempt_is_historical_evidence() {
        let mut ledger = DeliveryAttemptLedger::new();
        let first = ledger.open_attempt(descriptor("delivery", 1)).unwrap();
        ledger.dispatch(&first).unwrap();
        // A newer target supersedes the unapplied attempt.
        let superseded = ledger.supersede_delivery(&id("delivery"), 2).unwrap();
        assert_eq!(superseded, vec![first.clone()]);
        assert_eq!(ledger.head_target_version(&id("delivery")), Some(2));

        let second = ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        assert_eq!(
            ledger.acknowledge_late(&first, "late-receipt").unwrap(),
            LateAckDisposition::Historical {
                superseded_by_ordinal: 2,
            }
        );
        // The late receipt is recorded as evidence but does not revive the attempt.
        assert_eq!(
            ledger.attempt(&first).unwrap().state,
            DeliveryAttemptState::Superseded
        );
        assert!(ledger
            .attempt(&first)
            .unwrap()
            .transport_receipts
            .contains(&"late-receipt".to_owned()));
        // A current acknowledgement is still current.
        ledger.dispatch(&second).unwrap();
        assert_eq!(
            ledger.acknowledge_late(&second, "on-time").unwrap(),
            LateAckDisposition::Current
        );
    }

    #[test]
    fn an_applied_proof_for_an_attempt_behind_the_head_is_historical() {
        let mut ledger = DeliveryAttemptLedger::new();
        let first = ledger.open_attempt(descriptor("delivery", 1)).unwrap();
        ledger.dispatch(&first).unwrap();
        ledger.record_transport_ack(&first, "receipt").unwrap();
        // A retry moves the head to ordinal 2 while the first attempt is still
        // acknowledged-but-unapplied, which is exactly the late-proof window.
        ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        assert_eq!(
            ledger
                .record_applied(
                    &first,
                    AppliedProof {
                        applied_context_version: 1,
                        digest: "digest".into(),
                    },
                )
                .unwrap(),
            AppliedDisposition::Historical {
                head_target_context_version: 2,
            }
        );
        // The proof is kept as evidence but does not move the desired head.
        assert_eq!(ledger.applied_high_water(&id("delivery")), Some(1));
        assert_eq!(ledger.head_target_version(&id("delivery")), Some(2));
    }

    #[test]
    fn a_superseded_attempt_refuses_an_applied_proof_outright() {
        let mut ledger = DeliveryAttemptLedger::new();
        let first = ledger.open_attempt(descriptor("delivery", 1)).unwrap();
        ledger.dispatch(&first).unwrap();
        ledger.record_transport_ack(&first, "receipt").unwrap();
        ledger.supersede_delivery(&id("delivery"), 2).unwrap();
        // Supersession is terminal, so the proof is an illegal transition rather
        // than a historical record.
        assert!(matches!(
            ledger.record_applied(
                &first,
                AppliedProof {
                    applied_context_version: 1,
                    digest: "digest".into(),
                },
            ),
            Err(ContextError::InvalidDeliveryTransition { .. })
        ));
    }

    #[test]
    fn supersession_requires_a_strictly_advancing_target() {
        let mut ledger = DeliveryAttemptLedger::new();
        ledger.open_attempt(descriptor("delivery", 2)).unwrap();
        assert_eq!(
            ledger.supersede_delivery(&id("delivery"), 2),
            Err(ContextError::ContextVersionRegression {
                current: 2,
                requested: 2,
            })
        );
    }

    #[test]
    fn an_attempt_id_and_boundary_must_be_non_empty_and_non_zero() {
        assert_eq!(
            DeliveryAttemptId::new("  "),
            Err(ContextError::EmptyField("delivery_attempt_id"))
        );
        let mut invalid = descriptor("delivery", 1);
        invalid.boundary.permission_epoch = 0;
        assert_eq!(
            DeliveryAttemptLedger::new().open_attempt(invalid),
            Err(ContextError::InvalidVersion)
        );
    }
}
