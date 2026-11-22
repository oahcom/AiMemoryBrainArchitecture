//! Multi-dimensional context budget: a vector of independent limits.
//!
//! Spec: `06-memory-context/context-budget-and-sufficiency.md` §1–§2, §7, §9.4.
//!
//! The required-entry and rendered-byte limits stay on `ContextBudget`.
//! This module carries the remaining dimensions §2 names as part of the same
//! vector and that `context-implementation-coverage.md` records as absent:
//! token estimate, relation fan-out, provenance depth, planning/commit/delivery
//! latency, CPU/memory cost and per-tier reserved capacity.
//!
//! Every limit is independent and fails closed the way the entry/byte limits do:
//! `actual > limit` is an overflow, `actual == limit` fits. A limit of `None`
//! (or, for tiers, a tier that is not listed) means unbounded. `Some(0)` is a
//! genuinely exhausted budget, never a synonym for unbounded.

use crate::ContextTier;
use serde::{Deserialize, Serialize};

/// Limits of the budget vector, independent of entry count and rendered bytes.
#[derive(Clone, Debug, Default, Eq, PartialEq, Serialize, Deserialize)]
pub struct BudgetVector {
    /// Estimated tokens under the target tokenizer/model profile.
    pub tokens: Option<u64>,
    /// Maximum relation fan-out admitted by expansion.
    pub relation_fan_out: Option<u64>,
    /// Maximum provenance chain depth that may be followed or retained.
    pub provenance_depth: Option<u64>,
    /// Planning/commit/delivery latency allowance in microseconds.
    pub latency_micros: Option<u64>,
    /// CPU (and memory) cost allowance in microseconds.
    pub cpu_micros: Option<u64>,
    /// Reserved capacity per tier as `(tier, entries)`. Empty means unbounded;
    /// a tier that is not listed is unbounded even when others are capped.
    pub tier_entries: Vec<(ContextTier, u64)>,
}

/// Measured utilization against a `BudgetVector`.
#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct BudgetUsage {
    pub tokens: u64,
    pub relation_fan_out: u64,
    pub provenance_depth: u64,
    pub latency_micros: u64,
    pub cpu_micros: u64,
    /// Observed entry count per tier.
    pub tier_entries: Vec<(ContextTier, u64)>,
}

/// One overflow outcome per budget dimension, carrying what happened and why.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum BudgetVectorError {
    TokenBudgetExceeded {
        actual: u64,
        limit: u64,
    },
    FanOutBudgetExceeded {
        actual: u64,
        limit: u64,
    },
    ProvenanceDepthBudgetExceeded {
        actual: u64,
        limit: u64,
    },
    LatencyBudgetExceeded {
        actual: u64,
        limit: u64,
    },
    CpuBudgetExceeded {
        actual: u64,
        limit: u64,
    },
    TierReserveExceeded {
        tier: ContextTier,
        actual: u64,
        limit: u64,
    },
}

impl std::fmt::Display for BudgetVectorError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{self:?}")
    }
}

fn entries_in(tier: ContextTier, counts: &[(ContextTier, u64)]) -> u64 {
    counts
        .iter()
        .filter(|(observed, _)| *observed == tier)
        .map(|(_, count)| count)
        .sum()
}

impl BudgetVector {
    /// Every violated dimension in declaration order. Overflow in one dimension
    /// is reported even when another dimension also overflows.
    pub fn violations(&self, usage: &BudgetUsage) -> Vec<BudgetVectorError> {
        let mut violations = Vec::new();

        if let Some(limit) = self.tokens {
            if usage.tokens > limit {
                violations.push(BudgetVectorError::TokenBudgetExceeded {
                    actual: usage.tokens,
                    limit,
                });
            }
        }
        if let Some(limit) = self.relation_fan_out {
            if usage.relation_fan_out > limit {
                violations.push(BudgetVectorError::FanOutBudgetExceeded {
                    actual: usage.relation_fan_out,
                    limit,
                });
            }
        }
        if let Some(limit) = self.provenance_depth {
            if usage.provenance_depth > limit {
                violations.push(BudgetVectorError::ProvenanceDepthBudgetExceeded {
                    actual: usage.provenance_depth,
                    limit,
                });
            }
        }
        if let Some(limit) = self.latency_micros {
            if usage.latency_micros > limit {
                violations.push(BudgetVectorError::LatencyBudgetExceeded {
                    actual: usage.latency_micros,
                    limit,
                });
            }
        }
        if let Some(limit) = self.cpu_micros {
            if usage.cpu_micros > limit {
                violations.push(BudgetVectorError::CpuBudgetExceeded {
                    actual: usage.cpu_micros,
                    limit,
                });
            }
        }
        for (tier, limit) in &self.tier_entries {
            let actual = entries_in(*tier, &usage.tier_entries);
            if actual > *limit {
                violations.push(BudgetVectorError::TierReserveExceeded {
                    tier: *tier,
                    actual,
                    limit: *limit,
                });
            }
        }

        violations
    }

    /// Fail closed on the first violated dimension in declaration order.
    pub fn check(&self, usage: &BudgetUsage) -> Result<(), BudgetVectorError> {
        match self.violations(usage).into_iter().next() {
            Some(violation) => Err(violation),
            None => Ok(()),
        }
    }
}
