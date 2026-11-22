//! In-memory delivery lifecycle state machine and ACK consumer.
//!
//! `AckDisposition` in `delivery_ledger` is a pure classification:
//! it answers whether an ACK targets the current attempt without changing state.
//! `AckOutcome` is the result of consuming an ACK: it reports the outcome
//! of the state transition and records accepted, duplicate, and late ACKs.
//!
//! Supersession policy:
//! - An Acknowledged delivery cannot be superseded.
//! - A Superseded delivery cannot be superseded again.
//! - An Abandoned delivery cannot be superseded.
//! - The replacement delivery must already be enqueued.
//!
//! A delivery cannot be marked Delivered without a recorded attempt.
//! `max_attempts` is the maximum number of attempts a delivery may record,
//! and the first attempt counts toward it. Recording the attempt that reaches
//! the limit moves the delivery to Abandoned and returns Ok; there is no
//! separate grace attempt.
//!
//! Duplicate ACKs are idempotently accepted as Duplicate. They do not
//! change the lifecycle state, but increment the total ACK counter.
//!
//! Late ACKs for superseded deliveries are retained in the record.
//! Late ACKs targeting an obsolete attempt of a non-superseded delivery
//! are also retained and reported as StaleAttempt.

use std::collections::HashMap;

use super::{
    AckDisposition, ContextError, DeliveryAck, DeliveryAttempt, DeliveryAttemptId, DeliveryId,
    DeliveryLedger,
};

/// Delivery lifecycle state.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DeliveryState {
    /// Enqueued but not yet delivered.
    Pending,
    /// An attempt has been delivered and is awaiting acknowledgement.
    Delivered,
    /// Successfully acknowledged. Terminal.
    Acknowledged,
    /// Replaced by a newer delivery. Terminal.
    Superseded,
    /// Retry budget exhausted. Terminal.
    Abandoned,
}

impl DeliveryState {
    pub fn is_terminal(&self) -> bool {
        matches!(
            self,
            Self::Acknowledged | Self::Superseded | Self::Abandoned
        )
    }
}

/// Complete in-memory lifecycle record for one delivery.
#[derive(Clone, Debug)]
pub struct DeliveryRecord {
    state: DeliveryState,
    current_attempt: Option<DeliveryAttempt>,
    ack_count: u64,
    late_ack_count: u64,
    superseded_by: Option<DeliveryId>,
}

impl DeliveryRecord {
    fn new() -> Self {
        Self {
            state: DeliveryState::Pending,
            current_attempt: None,
            ack_count: 0,
            late_ack_count: 0,
            superseded_by: None,
        }
    }

    pub fn state(&self) -> &DeliveryState {
        &self.state
    }

    pub fn current_attempt(&self) -> Option<&DeliveryAttempt> {
        self.current_attempt.as_ref()
    }

    /// Total number of ACK messages consumed for this delivery.
    pub fn ack_count(&self) -> u64 {
        self.ack_count
    }

    /// Number of ACK messages classified as late.
    pub fn late_ack_count(&self) -> u64 {
        self.late_ack_count
    }

    pub fn superseded_by(&self) -> Option<&DeliveryId> {
        self.superseded_by.as_ref()
    }
}

/// Result of consuming an ACK.
///
/// Unlike `AckDisposition`, this type describes the outcome of an
/// operation that may mutate the lifecycle record.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum AckOutcome {
    /// ACK accepted; delivery transitioned to Acknowledged.
    Accepted,
    /// Duplicate ACK; the original acknowledgement remains authoritative.
    Duplicate,
    /// ACK received for a superseded delivery.
    Late { superseded_by: DeliveryId },
    /// ACK references a delivery absent from the attempt ledger.
    UnknownDelivery,
    /// ACK references an obsolete attempt of a delivery not superseded.
    StaleAttempt,
}

/// In-memory delivery lifecycle and ACK consumer.
#[derive(Clone, Debug)]
pub struct DeliveryLifecycle {
    max_attempts: u32,
    ledger: DeliveryLedger,
    records: HashMap<DeliveryId, DeliveryRecord>,
}

impl DeliveryLifecycle {
    /// Create a lifecycle manager with a positive maximum attempt count.
    pub fn new(max_attempts: u32) -> Result<Self, ContextError> {
        if max_attempts == 0 {
            return Err(ContextError::InvalidBudget);
        }

        Ok(Self {
            max_attempts,
            ledger: DeliveryLedger::new(),
            records: HashMap::new(),
        })
    }

    /// Enqueue a new delivery.
    pub fn enqueue(&mut self, delivery: DeliveryId) -> Result<(), ContextError> {
        if self.records.contains_key(&delivery) {
            return Err(ContextError::DuplicateOperationId);
        }

        self.records.insert(delivery, DeliveryRecord::new());
        Ok(())
    }

    /// Record an attempt and enforce the attempt budget.
    ///
    /// The ledger validates attempt identity, sequence, and lineage.
    /// The attempt that reaches the configured budget is still recorded,
    /// then the delivery transitions to Abandoned.
    pub fn record_attempt(&mut self, attempt: DeliveryAttempt) -> Result<(), ContextError> {
        let delivery = attempt.delivery_id().clone();

        let record = self
            .records
            .get(&delivery)
            .ok_or(ContextError::MissingEntry)?;

        if record.state.is_terminal() {
            return Err(ContextError::IneligibleLifecycle);
        }

        let next_count = self
            .ledger
            .attempt_count(&delivery)
            .checked_add(1)
            .ok_or(ContextError::SequenceOverflow)?;

        self.ledger.record(attempt.clone())?;

        let record = self
            .records
            .get_mut(&delivery)
            .ok_or(ContextError::MissingEntry)?;

        record.current_attempt = Some(attempt);

        if next_count >= self.max_attempts as usize {
            record.state = DeliveryState::Abandoned;
        }

        Ok(())
    }

    /// Mark a delivery as delivered.
    ///
    /// At least one attempt must have been recorded.
    pub fn mark_delivered(&mut self, delivery: &DeliveryId) -> Result<(), ContextError> {
        let record = self
            .records
            .get_mut(delivery)
            .ok_or(ContextError::MissingEntry)?;

        if record.state.is_terminal() {
            return Err(ContextError::IneligibleLifecycle);
        }

        if record.current_attempt.is_none() {
            return Err(ContextError::IneligibleLifecycle);
        }

        record.state = DeliveryState::Delivered;
        Ok(())
    }

    /// Consume an ACK, updating lifecycle state and recording its outcome.
    ///
    /// Unknown deliveries are normal protocol observations and return
    /// `Ok(AckOutcome::UnknownDelivery)`.
    ///
    /// ACKs for superseded deliveries are counted, never silently discarded.
    /// ACKs for abandoned deliveries are rejected without changing the record.
    pub fn consume_ack(&mut self, ack: &DeliveryAck) -> Result<AckOutcome, ContextError> {
        let delivery = ack.delivery_id();

        let Some(record) = self.records.get(delivery) else {
            return Ok(AckOutcome::UnknownDelivery);
        };

        if record.state == DeliveryState::Acknowledged {
            let record = self
                .records
                .get_mut(delivery)
                .ok_or(ContextError::MissingEntry)?;

            record.ack_count = record
                .ack_count
                .checked_add(1)
                .ok_or(ContextError::SequenceOverflow)?;

            return Ok(AckOutcome::Duplicate);
        }

        if record.state == DeliveryState::Superseded {
            let superseded_by = record
                .superseded_by
                .clone()
                .ok_or(ContextError::ContextMismatch)?;

            let record = self
                .records
                .get_mut(delivery)
                .ok_or(ContextError::MissingEntry)?;

            record.ack_count = record
                .ack_count
                .checked_add(1)
                .ok_or(ContextError::SequenceOverflow)?;

            record.late_ack_count = record
                .late_ack_count
                .checked_add(1)
                .ok_or(ContextError::SequenceOverflow)?;

            return Ok(AckOutcome::Late { superseded_by });
        }

        if record.state == DeliveryState::Abandoned {
            return Err(ContextError::IneligibleLifecycle);
        }

        match self.ledger.classify_ack(ack) {
            AckDisposition::UnknownDelivery => Ok(AckOutcome::UnknownDelivery),

            AckDisposition::Late => {
                let record = self
                    .records
                    .get_mut(delivery)
                    .ok_or(ContextError::MissingEntry)?;

                record.ack_count = record
                    .ack_count
                    .checked_add(1)
                    .ok_or(ContextError::SequenceOverflow)?;

                record.late_ack_count = record
                    .late_ack_count
                    .checked_add(1)
                    .ok_or(ContextError::SequenceOverflow)?;

                Ok(AckOutcome::StaleAttempt)
            }

            AckDisposition::Current => {
                let record = self
                    .records
                    .get_mut(delivery)
                    .ok_or(ContextError::MissingEntry)?;

                if record.state != DeliveryState::Delivered {
                    return Err(ContextError::IneligibleLifecycle);
                }

                record.ack_count = record
                    .ack_count
                    .checked_add(1)
                    .ok_or(ContextError::SequenceOverflow)?;

                record.state = DeliveryState::Acknowledged;

                Ok(AckOutcome::Accepted)
            }
        }
    }

    /// Supersede an existing delivery with an already-enqueued replacement.
    ///
    /// Acknowledged, Superseded, and Abandoned deliveries cannot be superseded.
    /// The replacement must exist and must not be the old delivery itself.
    pub fn supersede(&mut self, old: &DeliveryId, by: DeliveryId) -> Result<(), ContextError> {
        if old == &by {
            return Err(ContextError::ContextMismatch);
        }

        if !self.records.contains_key(&by) {
            return Err(ContextError::MissingEntry);
        }

        let old_record = self
            .records
            .get_mut(old)
            .ok_or(ContextError::MissingEntry)?;

        if old_record.state.is_terminal() {
            return Err(ContextError::IneligibleLifecycle);
        }

        old_record.state = DeliveryState::Superseded;
        old_record.superseded_by = Some(by);

        Ok(())
    }

    /// Return a delivery's current state.
    pub fn state(&self, delivery: &DeliveryId) -> Option<&DeliveryState> {
        self.records.get(delivery).map(|record| &record.state)
    }

    /// Return a delivery's complete lifecycle record.
    pub fn record(&self, delivery: &DeliveryId) -> Option<&DeliveryRecord> {
        self.records.get(delivery)
    }

    /// Whether another attempt may be recorded.
    pub fn can_retry(&self, delivery: &DeliveryId) -> bool {
        let Some(record) = self.records.get(delivery) else {
            return false;
        };

        !record.state.is_terminal()
            && self.ledger.attempt_count(delivery) < self.max_attempts as usize
    }

    /// Return the configured maximum number of attempts.
    pub fn max_attempts(&self) -> u32 {
        self.max_attempts
    }

    /// Return the attempt ledger.
    pub fn ledger(&self) -> &DeliveryLedger {
        &self.ledger
    }

    /// Return the current attempt identity, if present.
    pub fn current_attempt_id(&self, delivery: &DeliveryId) -> Option<&DeliveryAttemptId> {
        self.records
            .get(delivery)
            .and_then(|record| record.current_attempt.as_ref())
            .map(DeliveryAttempt::attempt_id)
    }
}
