// Delivery attempt identity, retry history, and ACK classification.
//
// Note: `ContextAcknowledgements::ack` (in `lib.rs`) classifies late ACKs
// along the context version axis. This module classifies them along the
// delivery attempt axis. They are orthogonal: a delivery can be acked
// correctly while its context version is stale, and vice versa.

use std::collections::{HashMap, HashSet};

use super::ContextError;

/// 一次投递尝试的身份。构造即校验，不可伪造。
#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct DeliveryAttemptId(String);

impl DeliveryAttemptId {
    pub fn new(raw: impl Into<String>) -> Result<Self, ContextError> {
        let raw = raw.into();

        if raw.trim().is_empty() {
            return Err(ContextError::EmptyField("delivery_attempt_id"));
        }

        Ok(Self(raw))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// delivery 身份（与 attempt 区分）。
#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct DeliveryId(String);

impl DeliveryId {
    pub fn new(raw: impl Into<String>) -> Result<Self, ContextError> {
        let raw = raw.into();

        if raw.trim().is_empty() {
            return Err(ContextError::EmptyField("delivery_id"));
        }

        Ok(Self(raw))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

/// 一次尝试的记录。
///
/// 所有字段私有，只能通过 first 或 retry 构造。
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DeliveryAttempt {
    delivery: DeliveryId,
    attempt: DeliveryAttemptId,
    attempt_number: u32,
    previous: Option<DeliveryAttemptId>,
}

impl DeliveryAttempt {
    /// 第一次尝试：attempt_number = 1，previous = None。
    pub fn first(delivery: DeliveryId, attempt: DeliveryAttemptId) -> Self {
        Self {
            delivery,
            attempt,
            attempt_number: 1,
            previous: None,
        }
    }

    /// 重试：继承 previous 的 delivery 身份，
    /// attempt_number 增加 1，previous 指向上一 attempt。
    pub fn retry(
        previous: &DeliveryAttempt,
        attempt: DeliveryAttemptId,
    ) -> Result<Self, ContextError> {
        let attempt_number = previous
            .attempt_number
            .checked_add(1)
            .ok_or(ContextError::SequenceOverflow)?;

        Ok(Self {
            delivery: previous.delivery.clone(),
            attempt,
            attempt_number,
            previous: Some(previous.attempt.clone()),
        })
    }

    pub fn delivery_id(&self) -> &DeliveryId {
        &self.delivery
    }

    pub fn attempt_id(&self) -> &DeliveryAttemptId {
        &self.attempt
    }

    pub fn attempt_number(&self) -> u32 {
        self.attempt_number
    }

    pub fn previous_attempt_id(&self) -> Option<&DeliveryAttemptId> {
        self.previous.as_ref()
    }
}

/// ACK 只针对 delivery。
///
/// acknowledged_attempt 是 ACK 报文携带的观察记录，
/// 不是 ACK 的目标身份。
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DeliveryAck {
    delivery: DeliveryId,
    acknowledged_attempt: DeliveryAttemptId,
}

impl DeliveryAck {
    pub fn new(delivery: DeliveryId, acknowledged_attempt: DeliveryAttemptId) -> Self {
        Self {
            delivery,
            acknowledged_attempt,
        }
    }

    pub fn delivery_id(&self) -> &DeliveryId {
        &self.delivery
    }

    /// ACK 携带的 attempt 观察记录，不是 ACK 目标。
    pub fn acknowledged_attempt_id(&self) -> &DeliveryAttemptId {
        &self.acknowledged_attempt
    }
}

/// ACK 归属判定结果。
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AckDisposition {
    /// ACK 对应的正是当前活跃 attempt。
    Current,

    /// ACK 对应的不是当前 attempt，包括已被取代或未知的 attempt。
    Late,

    /// delivery 不存在。
    UnknownDelivery,
}

/// attempt 台账。
///
/// attempts 按记录顺序保存。
/// attempt_ids 在整个 ledger 范围内全局唯一。
#[derive(Clone, Debug, Default)]
pub struct DeliveryLedger {
    attempts: HashMap<DeliveryId, Vec<DeliveryAttempt>>,
    attempt_ids: HashSet<DeliveryAttemptId>,
}

impl DeliveryLedger {
    pub fn new() -> Self {
        Self::default()
    }

    /// 记录一次尝试。
    ///
    /// 首次尝试必须是 attempt_number = 1 且 previous = None。
    ///
    /// 后续尝试必须：
    /// - 属于同一个 delivery；
    /// - previous 指向当前最新 attempt；
    /// - attempt_number 恰好递增 1。
    ///
    /// attempt ID 在整个 ledger 内不得重复。
    pub fn record(&mut self, attempt: DeliveryAttempt) -> Result<(), ContextError> {
        if self.attempt_ids.contains(&attempt.attempt) {
            return Err(ContextError::DuplicateOperationId);
        }

        match self.attempts.get(&attempt.delivery) {
            None => {
                if attempt.attempt_number != 1 || attempt.previous.is_some() {
                    return Err(ContextError::ContextMismatch);
                }
            }
            Some(history) => {
                let current = history.last().ok_or(ContextError::ContextMismatch)?;

                let expected_number = current
                    .attempt_number
                    .checked_add(1)
                    .ok_or(ContextError::SequenceOverflow)?;

                if attempt.attempt_number != expected_number
                    || attempt.previous.as_ref() != Some(&current.attempt)
                {
                    return Err(ContextError::ContextMismatch);
                }
            }
        }

        self.attempt_ids.insert(attempt.attempt.clone());

        self.attempts
            .entry(attempt.delivery.clone())
            .or_default()
            .push(attempt);

        Ok(())
    }

    /// 某个 delivery 的当前（最新）attempt。
    pub fn current_attempt(&self, delivery: &DeliveryId) -> Option<&DeliveryAttempt> {
        self.attempts
            .get(delivery)
            .and_then(|history| history.last())
    }

    /// 某个 delivery 的全部 attempt，按 attempt_number 升序。
    pub fn attempts_for(&self, delivery: &DeliveryId) -> Vec<&DeliveryAttempt> {
        self.attempts
            .get(delivery)
            .map(|history| history.iter().collect())
            .unwrap_or_default()
    }

    /// 某个 delivery 的尝试次数。
    pub fn attempt_count(&self, delivery: &DeliveryId) -> usize {
        self.attempts.get(delivery).map_or(0, Vec::len)
    }

    /// 判定一条 ACK 是 Current / Late / UnknownDelivery。
    ///
    /// 判定依据：
    /// 1. delivery 不存在：UnknownDelivery。
    /// 2. ACK 携带的 attempt ID 等于当前 attempt ID：Current。
    /// 3. 其他情况：Late。
    ///
    /// 即使 ACK 携带的 attempt 从未被 ledger 记录，
    /// 只要 delivery 存在且该 attempt 不是当前 attempt，
    /// 仍然返回 Late。
    pub fn classify_ack(&self, ack: &DeliveryAck) -> AckDisposition {
        let Some(current) = self.current_attempt(&ack.delivery) else {
            return AckDisposition::UnknownDelivery;
        };

        if current.attempt_id() == ack.acknowledged_attempt_id() {
            AckDisposition::Current
        } else {
            AckDisposition::Late
        }
    }
}
