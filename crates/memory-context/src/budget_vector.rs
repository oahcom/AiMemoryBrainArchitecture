//! Vector budget accounting for the managed Context region.
//!
//! `context-budget-and-sufficiency.md` §1–§2 decides that budget is a *vector*,
//! not a single Top-K entry count. This module models the part of that vector
//! the crate can actually measure from its own snapshot schema:
//!
//! * Entry count, rendered bytes, distinct canonical refs and relation fan-out —
//!   exact over declared fields.
//! * Per-tier reserved capacity — exact, and only enforced when the region is
//!   actually saturated, so a reservation is a floor rather than a quota.
//! * Estimated tokens — **caller supplied**. This crate links no tokenizer, so
//!   the estimate belongs to the rendering layer; the planner consumes it and
//!   records whether it was exact or conservative. `None` means "not measured",
//!   never "fits".
//! * Transitive provenance depth, planning/commit/delivery latency and CPU cost —
//!   not carried by the snapshot schema and not measurable here, so they are
//!   reported as unmeasured instead of being filled with a plausible number.

use crate::{ContextBudget, ContextCandidate, ContextEntry, ContextTier};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

/// Entry capacity reserved for one prioritization tier.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct TierReserve {
    pub tier: ContextTier,
    pub reserved_entries: usize,
}

/// A token estimate produced by whoever owns the tokenizer/model profile.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct TokenEstimate {
    pub tokens: usize,
    /// Tokenizer or model profile the estimate was produced under.
    pub profile: String,
    /// `false` for a conservative upper bound rather than an exact count.
    pub exact: bool,
}

/// Token dimension of the budget vector.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct TokenBudget {
    pub max_estimated_tokens: usize,
    /// Declared profile the limit was calibrated against, if any.
    pub tokenizer_profile: Option<String>,
}

/// The multi-dimensional budget a Context plan must fit.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextBudgetVector {
    pub max_entries: usize,
    pub max_rendered_bytes: usize,
    #[serde(default)]
    pub token_budget: Option<TokenBudget>,
    #[serde(default)]
    pub max_distinct_canonical_refs: Option<usize>,
    #[serde(default)]
    pub max_relation_fanout: Option<usize>,
    #[serde(default)]
    pub tier_reserves: Vec<TierReserve>,
}

/// Measured consumption of one budget dimension.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct TierUsage {
    pub tier: ContextTier,
    pub entries: usize,
}

/// Measured usage of the budget vector for a concrete candidate or entry set.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct BudgetUsage {
    pub entries: usize,
    pub rendered_bytes: usize,
    pub distinct_canonical_refs: usize,
    pub relation_fanout: usize,
    pub entries_by_tier: Vec<TierUsage>,
    /// `None` when the producer of the estimate has not measured tokens.
    pub estimated_tokens: Option<TokenEstimate>,
    /// `None` when transitive lineage is not carried by the snapshot schema.
    pub provenance_depth: Option<usize>,
}

impl BudgetUsage {
    /// Entry count for one tier, or zero when the tier is absent.
    pub fn entries_in(&self, tier: ContextTier) -> usize {
        self.entries_by_tier
            .iter()
            .find(|usage| usage.tier == tier)
            .map_or(0, |usage| usage.entries)
    }
}

/// A single boundary a set crossed. The first violation is returned; the caller
/// can repair and re-check to discover the next one.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum BudgetVectorViolation {
    ZeroLimit(&'static str),
    DuplicateTierReserve(ContextTier),
    ReservedExceedsEntryLimit {
        reserved: usize,
        limit: usize,
    },
    EntryCount {
        actual: usize,
        limit: usize,
    },
    RenderedBytes {
        actual: usize,
        limit: usize,
    },
    EstimatedTokens {
        actual: usize,
        limit: usize,
    },
    DistinctCanonicalRefs {
        actual: usize,
        limit: usize,
    },
    RelationFanout {
        actual: usize,
        limit: usize,
    },
    /// The region is saturated and a tier fell below its reserved floor.
    ProtectedTierUnderflow {
        tier: ContextTier,
        entries: usize,
        reserved: usize,
    },
}

impl BudgetVectorViolation {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::ZeroLimit(_) => "zero_limit",
            Self::DuplicateTierReserve(_) => "duplicate_tier_reserve",
            Self::ReservedExceedsEntryLimit { .. } => "reserved_exceeds_entry_limit",
            Self::EntryCount { .. } => "entry_count",
            Self::RenderedBytes { .. } => "rendered_bytes",
            Self::EstimatedTokens { .. } => "estimated_tokens",
            Self::DistinctCanonicalRefs { .. } => "distinct_canonical_refs",
            Self::RelationFanout { .. } => "relation_fanout",
            Self::ProtectedTierUnderflow { .. } => "protected_tier_underflow",
        }
    }
}

impl std::fmt::Display for BudgetVectorViolation {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::ZeroLimit(field) => write!(formatter, "budget limit {field} must be non-zero"),
            Self::DuplicateTierReserve(tier) => {
                write!(formatter, "tier reserve declared twice for {tier:?}")
            }
            Self::ReservedExceedsEntryLimit { reserved, limit } => write!(
                formatter,
                "reserved entries {reserved} exceed the entry limit {limit}"
            ),
            Self::EntryCount { actual, limit } => {
                write!(formatter, "entry_count {actual} > {limit}")
            }
            Self::RenderedBytes { actual, limit } => {
                write!(formatter, "rendered_bytes {actual} > {limit}")
            }
            Self::EstimatedTokens { actual, limit } => {
                write!(formatter, "estimated_tokens {actual} > {limit}")
            }
            Self::DistinctCanonicalRefs { actual, limit } => {
                write!(formatter, "distinct_canonical_refs {actual} > {limit}")
            }
            Self::RelationFanout { actual, limit } => {
                write!(formatter, "relation_fanout {actual} > {limit}")
            }
            Self::ProtectedTierUnderflow {
                tier,
                entries,
                reserved,
            } => write!(
                formatter,
                "saturated region holds {entries} entries of {tier:?} below its reserve {reserved}"
            ),
        }
    }
}

/// One element of a measured set. Both `ContextCandidate` and `ContextEntry`
/// expose the same four plan-relevant fields.
pub(crate) struct UsageInput<'a> {
    pub tier: ContextTier,
    pub rendered_bytes: usize,
    pub memory_id: &'a crate::OpaqueId,
    pub memory_version_id: &'a crate::OpaqueId,
    pub source_refs: &'a [crate::OpaqueId],
    pub evidence_refs: &'a [crate::OpaqueId],
}

impl ContextBudgetVector {
    /// A vector with only the two dimensions the older planner enforced.
    pub fn two_dimensional(max_entries: usize, max_rendered_bytes: usize) -> Self {
        Self {
            max_entries,
            max_rendered_bytes,
            token_budget: None,
            max_distinct_canonical_refs: None,
            max_relation_fanout: None,
            tier_reserves: Vec::new(),
        }
    }

    /// Reserved entry capacity for one tier.
    pub fn tier_reserve(&self, tier: ContextTier) -> usize {
        self.tier_reserves
            .iter()
            .find(|reserve| reserve.tier == tier)
            .map_or(0, |reserve| reserve.reserved_entries)
    }

    /// The projection of this vector onto the legacy two-dimensional budget, so
    /// a plan validated here can still be handed to `build_context`.
    pub fn narrow(&self) -> ContextBudget {
        ContextBudget {
            max_entries: self.max_entries,
            max_rendered_bytes: self.max_rendered_bytes,
        }
    }

    /// Dimensions this vector constrains but cannot measure from a snapshot.
    pub fn unmeasured_dimensions(&self) -> Vec<&'static str> {
        vec![
            "transitive_provenance_depth",
            "planning_latency",
            "cpu_cost",
        ]
    }

    /// Validate the declared limits themselves.
    pub fn validate(&self) -> Result<(), BudgetVectorViolation> {
        if self.max_entries == 0 {
            return Err(BudgetVectorViolation::ZeroLimit("max_entries"));
        }
        if self.max_rendered_bytes == 0 {
            return Err(BudgetVectorViolation::ZeroLimit("max_rendered_bytes"));
        }
        if let Some(token_budget) = &self.token_budget {
            if token_budget.max_estimated_tokens == 0 {
                return Err(BudgetVectorViolation::ZeroLimit("max_estimated_tokens"));
            }
        }
        if let Some(limit) = self.max_distinct_canonical_refs {
            if limit == 0 {
                return Err(BudgetVectorViolation::ZeroLimit(
                    "max_distinct_canonical_refs",
                ));
            }
        }
        if let Some(limit) = self.max_relation_fanout {
            if limit == 0 {
                return Err(BudgetVectorViolation::ZeroLimit("max_relation_fanout"));
            }
        }
        let mut total_reserved = 0usize;
        for (index, reserve) in self.tier_reserves.iter().enumerate() {
            if self.tier_reserves[..index]
                .iter()
                .any(|previous| previous.tier == reserve.tier)
            {
                return Err(BudgetVectorViolation::DuplicateTierReserve(reserve.tier));
            }
            total_reserved += reserve.reserved_entries;
        }
        if total_reserved > self.max_entries {
            return Err(BudgetVectorViolation::ReservedExceedsEntryLimit {
                reserved: total_reserved,
                limit: self.max_entries,
            });
        }
        Ok(())
    }

    /// Measure a candidate set without asserting it fits.
    pub fn usage(&self, candidates: &[ContextCandidate]) -> BudgetUsage {
        usage_from(candidates.iter().map(|candidate| UsageInput {
            tier: candidate.tier,
            rendered_bytes: candidate.rendered_content.len(),
            memory_id: &candidate.memory_id,
            memory_version_id: &candidate.memory_version_id,
            source_refs: &candidate.source_refs,
            evidence_refs: &candidate.evidence_refs,
        }))
    }

    /// Measure a snapshot entry set without asserting it fits.
    pub fn usage_for_entries(&self, entries: &[ContextEntry]) -> BudgetUsage {
        usage_from(entries.iter().map(|entry| UsageInput {
            tier: entry.tier,
            rendered_bytes: entry.rendered_bytes,
            memory_id: &entry.memory_id,
            memory_version_id: &entry.memory_version_id,
            source_refs: &entry.source_refs,
            evidence_refs: &entry.evidence_refs,
        }))
    }

    /// Check a candidate set against every limit that is measurable without a
    /// caller-supplied token estimate.
    pub fn check(
        &self,
        candidates: &[ContextCandidate],
    ) -> Result<BudgetUsage, BudgetVectorViolation> {
        let usage = self.usage(candidates);
        self.verify(&usage)?;
        Ok(usage)
    }

    /// Check a snapshot entry set. See [`Self::check`].
    pub fn check_entries(
        &self,
        entries: &[ContextEntry],
    ) -> Result<BudgetUsage, BudgetVectorViolation> {
        let usage = self.usage_for_entries(entries);
        self.verify(&usage)?;
        Ok(usage)
    }

    /// Check a candidate set including the token dimension measured by the
    /// rendering layer. An inexact estimate is accepted as an upper bound.
    pub fn check_with_token_estimate(
        &self,
        candidates: &[ContextCandidate],
        estimate: &TokenEstimate,
    ) -> Result<BudgetUsage, BudgetVectorViolation> {
        let mut usage = self.usage(candidates);
        usage.estimated_tokens = Some(estimate.clone());
        self.verify(&usage)?;
        Ok(usage)
    }

    fn verify(&self, usage: &BudgetUsage) -> Result<(), BudgetVectorViolation> {
        self.validate()?;
        if usage.entries > self.max_entries {
            return Err(BudgetVectorViolation::EntryCount {
                actual: usage.entries,
                limit: self.max_entries,
            });
        }
        if usage.rendered_bytes > self.max_rendered_bytes {
            return Err(BudgetVectorViolation::RenderedBytes {
                actual: usage.rendered_bytes,
                limit: self.max_rendered_bytes,
            });
        }
        if let (Some(limit), Some(estimate)) = (&self.token_budget, &usage.estimated_tokens) {
            if estimate.tokens > limit.max_estimated_tokens {
                return Err(BudgetVectorViolation::EstimatedTokens {
                    actual: estimate.tokens,
                    limit: limit.max_estimated_tokens,
                });
            }
        }
        if let Some(limit) = self.max_distinct_canonical_refs {
            if usage.distinct_canonical_refs > limit {
                return Err(BudgetVectorViolation::DistinctCanonicalRefs {
                    actual: usage.distinct_canonical_refs,
                    limit,
                });
            }
        }
        if let Some(limit) = self.max_relation_fanout {
            if usage.relation_fanout > limit {
                return Err(BudgetVectorViolation::RelationFanout {
                    actual: usage.relation_fanout,
                    limit,
                });
            }
        }
        // A reservation is a floor for a saturated region, not a cap: it only
        // binds once the entry budget is actually exhausted.
        if usage.entries >= self.max_entries {
            for reserve in &self.tier_reserves {
                let held = usage.entries_in(reserve.tier);
                if held < reserve.reserved_entries {
                    return Err(BudgetVectorViolation::ProtectedTierUnderflow {
                        tier: reserve.tier,
                        entries: held,
                        reserved: reserve.reserved_entries,
                    });
                }
            }
        }
        Ok(())
    }
}

fn usage_from<'a, I>(items: I) -> BudgetUsage
where
    I: IntoIterator<Item = UsageInput<'a>>,
{
    let mut entries = 0usize;
    let mut rendered_bytes = 0usize;
    let mut canonical: HashSet<(&str, &str)> = HashSet::new();
    let mut relation_fanout = 0usize;
    let mut tier_counts: Vec<(ContextTier, usize)> = Vec::new();
    for item in items {
        entries += 1;
        rendered_bytes = rendered_bytes.saturating_add(item.rendered_bytes);
        canonical.insert((item.memory_id.as_str(), item.memory_version_id.as_str()));
        let mut fan: HashSet<&str> = HashSet::new();
        for reference in item.source_refs {
            fan.insert(reference.as_str());
        }
        for reference in item.evidence_refs {
            fan.insert(reference.as_str());
        }
        relation_fanout = relation_fanout.max(fan.len());
        match tier_counts.iter_mut().find(|(tier, _)| *tier == item.tier) {
            Some((_, count)) => *count += 1,
            None => tier_counts.push((item.tier, 1)),
        }
    }
    tier_counts.sort_by_key(|(tier, _)| *tier);
    BudgetUsage {
        entries,
        rendered_bytes,
        distinct_canonical_refs: canonical.len(),
        relation_fanout,
        entries_by_tier: tier_counts
            .into_iter()
            .map(|(tier, entries)| TierUsage { tier, entries })
            .collect(),
        estimated_tokens: None,
        provenance_depth: None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::OpaqueId;

    #[test]
    fn tier_reserve_binds_only_when_the_region_is_saturated() {
        let vector = ContextBudgetVector {
            max_entries: 2,
            max_rendered_bytes: 1024,
            token_budget: None,
            max_distinct_canonical_refs: None,
            max_relation_fanout: None,
            tier_reserves: vec![TierReserve {
                tier: ContextTier::P0,
                reserved_entries: 1,
            }],
        };
        // One P1 entry in a 2-entry region: not saturated, so the P0 floor does
        // not bind and a P0-less plan is still legal.
        let usage = BudgetUsage {
            entries: 1,
            rendered_bytes: 10,
            distinct_canonical_refs: 1,
            relation_fanout: 1,
            entries_by_tier: vec![TierUsage {
                tier: ContextTier::P1,
                entries: 1,
            }],
            estimated_tokens: None,
            provenance_depth: None,
        };
        assert_eq!(vector.verify(&usage), Ok(()));
        // Saturated and holding no P0 entry: the reservation becomes a floor.
        let saturated = BudgetUsage {
            entries: 2,
            entries_by_tier: vec![TierUsage {
                tier: ContextTier::P1,
                entries: 2,
            }],
            ..usage
        };
        assert_eq!(
            vector.verify(&saturated),
            Err(BudgetVectorViolation::ProtectedTierUnderflow {
                tier: ContextTier::P0,
                entries: 0,
                reserved: 1,
            })
        );
    }

    #[test]
    fn zero_limit_is_rejected_before_any_usage_is_measured() {
        let vector = ContextBudgetVector::two_dimensional(0, 1024);
        assert_eq!(
            vector.validate(),
            Err(BudgetVectorViolation::ZeroLimit("max_entries"))
        );
    }

    #[test]
    fn usage_counts_distinct_canonical_refs_and_max_fanout() {
        let memory_id = OpaqueId::new("m1").unwrap();
        let version_id = OpaqueId::new("v1").unwrap();
        let source_one = OpaqueId::new("s1").unwrap();
        let source_two = OpaqueId::new("s2").unwrap();
        let single = [source_one.clone()];
        let pair = [source_one, source_two];
        let usage = usage_from(vec![
            UsageInput {
                tier: ContextTier::P1,
                rendered_bytes: 3,
                memory_id: &memory_id,
                memory_version_id: &version_id,
                source_refs: &single,
                evidence_refs: &[],
            },
            UsageInput {
                tier: ContextTier::P1,
                rendered_bytes: 5,
                memory_id: &memory_id,
                memory_version_id: &version_id,
                source_refs: &pair,
                evidence_refs: &[],
            },
        ]);
        assert_eq!(usage.entries, 2);
        assert_eq!(usage.rendered_bytes, 8);
        // Both entries share one (memory, version) pair.
        assert_eq!(usage.distinct_canonical_refs, 1);
        assert_eq!(usage.relation_fanout, 2);
        assert_eq!(usage.entries_in(ContextTier::P1), 2);
        assert_eq!(usage.entries_in(ContextTier::P0), 0);
    }
}
