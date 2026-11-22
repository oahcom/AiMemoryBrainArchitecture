//! Greedy marginal-coverage candidate selection.
//!
//! Hard constraints are evaluated before ranking. Excluded candidates never
//! consume budget and never participate in utility calculations.
//!
//! Assumptions based on the existing crate API:
//! - ContextBudget is constructed through its public fields.
//! - ContextBudget::validate() is its existing budget validation method.
//! - ContextCandidate::entry_id is the stable candidate identifier.
//! - SufficiencyDimension does not currently implement Ord, so this module
//!   supplies a deterministic ordering without changing its definition.

use crate::{ContextBudget, ContextCandidate, SufficiencyDimension};
use std::cmp::Ordering;
use std::collections::{BTreeSet, HashSet};

/// An uncertainty classification used by the selection utility function.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum UncertaintyLevel {
    None,
    Low,
    Medium,
    High,
}

/// A candidate and its utility inputs.
pub struct RankedCandidate<'a> {
    pub candidate: &'a ContextCandidate,
    pub covers: BTreeSet<SufficiencyDimension>,
    pub content_fingerprint: u64,
    pub rendered_bytes: u64,
    pub uncertainty: UncertaintyLevel,
}

/// Hard constraints that must all pass before ranking.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct HardConstraints {
    pub authorized: bool,
    pub not_forgotten: bool,
    pub temporally_valid: bool,
    pub environment_matches: bool,
    pub required_evidence_present: bool,
}

impl HardConstraints {
    fn first_violation(self) -> Option<&'static str> {
        if !self.authorized {
            Some("authorization")
        } else if !self.not_forgotten {
            Some("forget")
        } else if !self.temporally_valid {
            Some("temporal_validity")
        } else if !self.environment_matches {
            Some("environment_match")
        } else if !self.required_evidence_present {
            Some("required_evidence")
        } else {
            None
        }
    }
}

/// Explicit utility weights. Positive penalties reduce candidate scores.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SelectionWeights {
    pub marginal_coverage: i64,
    pub redundancy_penalty: i64,
    pub byte_cost_penalty_per_kib: i64,
    pub uncertainty_penalty: [i64; 3],
}

/// Result of a deterministic greedy selection.
pub struct SelectionOutcome<'a> {
    pub excluded: Vec<(&'a ContextCandidate, &'static str)>,
    pub selected: Vec<&'a ContextCandidate>,
    pub marginal_scores: Vec<i64>,
    pub uncovered_mandatory: Vec<SufficiencyDimension>,
}

/// Provide a stable total order for sufficiency dimensions.
///
/// Known variants follow their declaration order. Unknown dimensions are
/// ordered lexicographically by their contained value.
impl PartialOrd for SufficiencyDimension {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for SufficiencyDimension {
    fn cmp(&self, other: &Self) -> Ordering {
        fn rank(value: &SufficiencyDimension) -> u8 {
            match value {
                SufficiencyDimension::SemanticCoverage => 0,
                SufficiencyDimension::EntityCoverage => 1,
                SufficiencyDimension::RelationCoverage => 2,
                SufficiencyDimension::EnvironmentCoverage => 3,
                SufficiencyDimension::TemporalValidity => 4,
                SufficiencyDimension::EvidenceCoverage => 5,
                SufficiencyDimension::RiskCoverage => 6,
                SufficiencyDimension::UncertaintyCoverage => 7,
                SufficiencyDimension::FreshnessCompleteness => 8,
                SufficiencyDimension::NonRedundancy => 9,
                SufficiencyDimension::Unknown(_) => 10,
            }
        }

        match rank(self).cmp(&rank(other)) {
            Ordering::Equal => match (self, other) {
                (Self::Unknown(left), Self::Unknown(right)) => left.cmp(right),
                _ => Ordering::Equal,
            },
            ordering => ordering,
        }
    }
}

fn uncertainty_penalty(level: UncertaintyLevel, weights: &SelectionWeights) -> i64 {
    match level {
        UncertaintyLevel::None => 0,
        UncertaintyLevel::Low => weights.uncertainty_penalty[0],
        UncertaintyLevel::Medium => weights.uncertainty_penalty[1],
        UncertaintyLevel::High => weights.uncertainty_penalty[2],
    }
}

fn to_i64_saturating(value: usize) -> i64 {
    i64::try_from(value).unwrap_or(i64::MAX)
}

fn score_candidate(
    candidate: &RankedCandidate<'_>,
    covered: &BTreeSet<SufficiencyDimension>,
    selected_fingerprints: &[u64],
    weights: &SelectionWeights,
) -> i64 {
    let new_dimensions = candidate
        .covers
        .iter()
        .filter(|dimension| !covered.contains(*dimension))
        .count();

    let redundancy_count = selected_fingerprints
        .iter()
        .filter(|fingerprint| **fingerprint == candidate.content_fingerprint)
        .count();

    let kibibytes = candidate.rendered_bytes / 1024;

    let byte_units = i64::try_from(kibibytes).unwrap_or(i64::MAX);

    let coverage_score = weights
        .marginal_coverage
        .saturating_mul(to_i64_saturating(new_dimensions));

    let redundancy_cost = weights
        .redundancy_penalty
        .saturating_mul(to_i64_saturating(redundancy_count));

    let byte_cost = weights.byte_cost_penalty_per_kib.saturating_mul(byte_units);

    coverage_score
        .saturating_sub(redundancy_cost)
        .saturating_sub(byte_cost)
        .saturating_sub(uncertainty_penalty(candidate.uncertainty, weights))
}

/// Select candidates by greedy marginal utility.
///
/// Processing order:
/// 1. Evaluate every candidate's hard constraints.
/// 2. Rank only candidates that pass every hard constraint.
/// 3. Select the highest positive marginal score.
/// 4. Skip candidates that exceed the remaining budget and continue trying.
/// 5. Stop when no candidates remain or the best score is non-positive.
///
/// Input order breaks score ties deterministically.
pub fn select_candidates<'a>(
    candidates: &'a [RankedCandidate<'a>],
    constraints: &dyn Fn(&'a ContextCandidate) -> HardConstraints,
    weights: &SelectionWeights,
    budget: &ContextBudget,
    mandatory: &BTreeSet<SufficiencyDimension>,
) -> SelectionOutcome<'a> {
    let mut excluded = Vec::new();
    let mut eligible = Vec::new();

    // Phase 1: hard constraints. This phase is independent of budget.
    for (index, ranked) in candidates.iter().enumerate() {
        if let Some(reason) = constraints(ranked.candidate).first_violation() {
            excluded.push((ranked.candidate, reason));
        } else {
            eligible.push(index);
        }
    }

    let mut selected = Vec::new();
    let mut marginal_scores = Vec::new();
    let mut covered = BTreeSet::new();
    let mut selected_fingerprints = Vec::new();

    // Invalid budgets cannot admit candidates.
    if budget.validate().is_err() {
        return SelectionOutcome {
            excluded,
            selected,
            marginal_scores,
            uncovered_mandatory: mandatory.iter().cloned().collect(),
        };
    }

    let mut attempted = HashSet::new();
    let mut used_bytes = 0u64;

    loop {
        let mut best: Option<(usize, i64)> = None;

        // Scan in original input order. Strictly greater scores replace the
        // current best, preserving the first candidate on ties.
        for &index in &eligible {
            if attempted.contains(&index) {
                continue;
            }

            let ranked = &candidates[index];
            let score = score_candidate(ranked, &covered, &selected_fingerprints, weights);

            match best {
                None => best = Some((index, score)),
                Some((_, best_score)) if score > best_score => {
                    best = Some((index, score));
                }
                _ => {}
            }
        }

        let Some((best_index, best_score)) = best else {
            break;
        };

        // Never add zero- or negative-utility candidates.
        if best_score <= 0 {
            break;
        }

        attempted.insert(best_index);

        let ranked = &candidates[best_index];

        // Check both independent budget dimensions before accepting.
        let next_bytes = used_bytes.checked_add(ranked.rendered_bytes);

        let exceeds_budget = selected.len() >= budget.max_entries
            || next_bytes.is_none_or(|bytes| bytes > budget.max_rendered_bytes as u64);

        if exceeds_budget {
            // A smaller remaining candidate may still fit.
            continue;
        }

        used_bytes = next_bytes.unwrap();

        selected.push(ranked.candidate);
        marginal_scores.push(best_score);

        for dimension in &ranked.covers {
            covered.insert(dimension.clone());
        }

        selected_fingerprints.push(ranked.content_fingerprint);
    }

    let uncovered_mandatory = mandatory
        .iter()
        .filter(|dimension| !covered.contains(*dimension))
        .cloned()
        .collect();

    SelectionOutcome {
        excluded,
        selected,
        marginal_scores,
        uncovered_mandatory,
    }
}
