//! Candidate-set selection that maximizes marginal coverage under vector
//! constraints.
//!
//! `context-budget-and-sufficiency.md` §5 (CANDIDATE) asks for a selection that
//! maximizes weighted requirement coverage / marginal utility while penalizing
//! redundancy and token/byte cost, with authorization, lifecycle, temporal
//! validity, environment match and required evidence treated as hard constraints
//! *before* ranking (§9.2).
//!
//! The optimizer therefore runs in three phases:
//!
//! 1. **Hard constraints.** Every candidate is validated against the identity
//!    (lifecycle, scope, lineage, non-empty rendering) before it is ranked. A
//!    candidate that fails is a typed error, not a low score.
//! 2. **Mandatory anchors.** P0 candidates are protected: they are admitted
//!    first and the plan fails if the protected set alone cannot fit, because
//!    §9.4 forbids silently dropping protected P0 content.
//! 3. **Greedy marginal-coverage ranking.** Each remaining candidate is scored by
//!    the weight of coverage keys no already-selected candidate covers, divided
//!    by its rendered-byte cost. Zero marginal gain is redundancy (§3 dimension
//!    10) and is deferred with a reason instead of consuming budget.
//!
//! Ties are broken deterministically (larger gain, then tier, then descending
//! priority, then entry id) so repeated planning of the same input returns the
//! same membership.

use crate::budget_vector::{BudgetUsage, BudgetVectorViolation, ContextBudgetVector};
use crate::{ContextCandidate, ContextError, ContextIdentity, ContextTier, OpaqueId};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

/// One weighted coverage key the task requires.
///
/// `weight` is a relative integer weight rather than a probability: the
/// optimizer only needs ordering, and integer weights keep the result exactly
/// reproducible. `mandatory` keys that end up uncovered are reported, never
/// silently satisfied by substituting a cheaper entry.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CoverageWeight {
    pub coverage_key: String,
    pub weight: u32,
    pub mandatory: bool,
}

/// The coverage keys one candidate can contribute.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CandidateCoverage {
    pub entry_id: OpaqueId,
    pub coverage_keys: Vec<String>,
}

/// Coverage declaration supplied by the planner for one selection round.
#[derive(Clone, Debug, Eq, PartialEq, Default, Serialize, Deserialize)]
pub struct CoverageRequest {
    pub weights: Vec<CoverageWeight>,
    pub coverage: Vec<CandidateCoverage>,
}

/// Why one round of the greedy ranking admitted a candidate.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct SelectedCandidate {
    pub entry_id: OpaqueId,
    pub tier: ContextTier,
    pub priority: i32,
    /// Sum of the weights of the keys this candidate covered first.
    pub marginal_gain: u32,
    /// Rendered bytes the candidate costs.
    pub marginal_cost_bytes: usize,
    pub cumulative_entries: usize,
    pub cumulative_bytes: usize,
    /// `true` when the candidate was admitted as a protected P0 anchor.
    pub mandatory_anchor: bool,
}

/// Why a candidate did not enter the selected set.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum DeferredReason {
    /// Every key it covers is already covered: a paraphrase, not coverage.
    ZeroMarginalCoverage,
    /// Same canonical membership as an already-selected candidate.
    DuplicateMembership,
    EntryBudget,
    ByteBudget,
    TokenBudget,
    CanonicalRefBudget,
    RelationFanoutBudget,
    ProtectedTierUnderflow,
    InvalidBudget,
}

impl DeferredReason {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::ZeroMarginalCoverage => "zero_marginal_coverage",
            Self::DuplicateMembership => "duplicate_membership",
            Self::EntryBudget => "entry_budget",
            Self::ByteBudget => "byte_budget",
            Self::TokenBudget => "token_budget",
            Self::CanonicalRefBudget => "canonical_ref_budget",
            Self::RelationFanoutBudget => "relation_fanout_budget",
            Self::ProtectedTierUnderflow => "protected_tier_underflow",
            Self::InvalidBudget => "invalid_budget",
        }
    }

    /// `true` when the deferral was caused by a capacity limit.
    pub fn is_budget_limited(&self) -> bool {
        !matches!(self, Self::ZeroMarginalCoverage | Self::DuplicateMembership)
    }
}

/// One deferred candidate and the reason it lost.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DeferredCandidate {
    pub entry_id: OpaqueId,
    pub reason: DeferredReason,
}

impl From<&BudgetVectorViolation> for DeferredReason {
    fn from(violation: &BudgetVectorViolation) -> Self {
        match violation {
            BudgetVectorViolation::EntryCount { .. } => Self::EntryBudget,
            BudgetVectorViolation::RenderedBytes { .. } => Self::ByteBudget,
            BudgetVectorViolation::EstimatedTokens { .. } => Self::TokenBudget,
            BudgetVectorViolation::DistinctCanonicalRefs { .. } => Self::CanonicalRefBudget,
            BudgetVectorViolation::RelationFanout { .. } => Self::RelationFanoutBudget,
            BudgetVectorViolation::ProtectedTierUnderflow { .. } => Self::ProtectedTierUnderflow,
            BudgetVectorViolation::ZeroLimit(_)
            | BudgetVectorViolation::DuplicateTierReserve(_)
            | BudgetVectorViolation::ReservedExceedsEntryLimit { .. } => Self::InvalidBudget,
        }
    }
}

/// The outcome of one optimization round: membership plus the evidence for it.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CandidateSelection {
    /// Selected candidates in ranking order.
    pub selected: Vec<ContextCandidate>,
    /// Per-candidate marginal contribution, in the order candidates were admitted.
    pub order: Vec<SelectedCandidate>,
    /// Candidates excluded from the managed region, with typed reasons.
    pub deferred: Vec<DeferredCandidate>,
    /// Coverage keys the selection actually covers.
    pub covered_keys: Vec<String>,
    /// Mandatory keys no candidate could cover. An empty plan is reported, not hidden.
    pub uncovered_mandatory: Vec<String>,
    /// Measured usage of the selected set.
    pub usage: BudgetUsage,
}

impl CandidateSelection {
    /// `true` when at least one candidate was excluded by a capacity limit.
    pub fn is_budget_limited(&self) -> bool {
        self.deferred
            .iter()
            .any(|candidate| candidate.reason.is_budget_limited())
    }

    /// The selected membership in the deterministic order `build_context` expects.
    pub fn into_candidates(self) -> Vec<ContextCandidate> {
        let mut candidates = self.selected;
        sort_for_plan(&mut candidates);
        candidates
    }
}

fn sort_for_plan(candidates: &mut [ContextCandidate]) {
    candidates.sort_by(|left, right| {
        left.tier
            .cmp(&right.tier)
            .then_with(|| right.priority.cmp(&left.priority))
            .then_with(|| left.entry_id.cmp(&right.entry_id))
    });
}

/// Select the candidate set with the highest marginal weighted coverage that
/// fits the budget vector.
///
/// # Errors
///
/// Returns [`ContextError::IneligibleLifecycle`], [`ContextError::ScopeMismatch`],
/// [`ContextError::MissingLineage`] and the other admission errors when a
/// candidate violates a hard constraint, [`ContextError::InvalidCoverageRequest`]
/// when the coverage declaration is malformed, and
/// [`ContextError::BudgetVector`] when the protected P0 anchors alone cannot fit.
pub fn select_coverage_optimal_candidates(
    identity: &ContextIdentity,
    budget: &ContextBudgetVector,
    request: &CoverageRequest,
    candidates: Vec<ContextCandidate>,
) -> Result<CandidateSelection, ContextError> {
    identity.validate()?;
    budget.validate().map_err(ContextError::BudgetVector)?;
    let weights = coverage_weights(request)?;
    let coverage = coverage_index(request)?;

    // Phase 1 — hard constraints precede ranking.
    for candidate in &candidates {
        candidate.validate_for(identity)?;
    }
    let mut ordered = candidates;
    sort_for_plan(&mut ordered);

    let mut selected: Vec<ContextCandidate> = Vec::new();
    let mut order: Vec<SelectedCandidate> = Vec::new();
    let mut deferred: Vec<DeferredCandidate> = Vec::new();
    let mut covered: HashSet<String> = HashSet::new();
    let mut memberships: HashSet<(OpaqueId, OpaqueId)> = HashSet::new();

    // Phase 2 — protected P0 anchors are admitted before any ranking.
    let (anchors, mut remaining): (Vec<ContextCandidate>, Vec<ContextCandidate>) = ordered
        .into_iter()
        .partition(|candidate| candidate.tier == ContextTier::P0);
    for anchor in anchors {
        let membership = (anchor.memory_id.clone(), anchor.memory_version_id.clone());
        if !memberships.insert(membership) {
            return Err(ContextError::DuplicateMembership);
        }
        let gain = marginal_gain(&anchor, &coverage, &weights, &covered);
        for key in covered_by(&anchor, &coverage) {
            if weights.contains_key(&key) {
                covered.insert(key);
            }
        }
        let bytes = anchor.rendered_content.len();
        selected.push(anchor.clone());
        order.push(SelectedCandidate {
            entry_id: anchor.entry_id,
            tier: anchor.tier,
            priority: anchor.priority,
            marginal_gain: gain,
            marginal_cost_bytes: bytes,
            cumulative_entries: selected.len(),
            cumulative_bytes: selected
                .iter()
                .map(|candidate| candidate.rendered_content.len())
                .sum(),
            mandatory_anchor: true,
        });
    }
    // A protected set that does not fit is a hard failure, never a silent drop.
    budget
        .check(&selected)
        .map_err(ContextError::BudgetVector)?;

    // Phase 3 — greedy marginal coverage under vector constraints.
    loop {
        let mut best: Option<(usize, u32, usize)> = None;
        for (index, candidate) in remaining.iter().enumerate() {
            let gain = marginal_gain(candidate, &coverage, &weights, &covered);
            if gain == 0 {
                continue;
            }
            let cost = candidate.rendered_content.len().max(1);
            best = match best {
                None => Some((index, gain, cost)),
                Some((best_index, best_gain, best_cost)) => {
                    let challenger = u128::from(gain) * best_cost as u128;
                    let incumbent = u128::from(best_gain) * cost as u128;
                    let wins = challenger > incumbent
                        || (challenger == incumbent
                            && tie_break(candidate, &remaining[best_index]));
                    if wins {
                        Some((index, gain, cost))
                    } else {
                        Some((best_index, best_gain, best_cost))
                    }
                }
            };
        }
        let Some((index, gain, cost)) = best else {
            break;
        };
        let candidate = remaining.remove(index);
        let membership = (
            candidate.memory_id.clone(),
            candidate.memory_version_id.clone(),
        );
        if !memberships.insert(membership) {
            deferred.push(DeferredCandidate {
                entry_id: candidate.entry_id,
                reason: DeferredReason::DuplicateMembership,
            });
            continue;
        }
        let mut tentative = selected.clone();
        tentative.push(candidate.clone());
        match budget.check(&tentative) {
            Ok(_) => {
                for key in covered_by(&candidate, &coverage) {
                    if weights.contains_key(&key) {
                        covered.insert(key);
                    }
                }
                selected.push(candidate.clone());
                order.push(SelectedCandidate {
                    entry_id: candidate.entry_id,
                    tier: candidate.tier,
                    priority: candidate.priority,
                    marginal_gain: gain,
                    marginal_cost_bytes: cost,
                    cumulative_entries: selected.len(),
                    cumulative_bytes: tentative
                        .iter()
                        .map(|selected| selected.rendered_content.len())
                        .sum(),
                    mandatory_anchor: false,
                });
            }
            Err(violation) => deferred.push(DeferredCandidate {
                entry_id: candidate.entry_id,
                reason: DeferredReason::from(&violation),
            }),
        }
    }

    // Anything left over covers nothing new; say so rather than hiding it.
    for candidate in remaining {
        deferred.push(DeferredCandidate {
            entry_id: candidate.entry_id,
            reason: DeferredReason::ZeroMarginalCoverage,
        });
    }

    let mut covered_keys: Vec<String> = covered.into_iter().collect();
    covered_keys.sort();
    let mut uncovered_mandatory: Vec<String> = weights
        .iter()
        .filter(|(key, weight)| weight.mandatory && !covered_keys.contains(key))
        .map(|(key, _)| key.clone())
        .collect();
    uncovered_mandatory.sort();

    let usage = budget.usage(&selected);
    Ok(CandidateSelection {
        selected,
        order,
        deferred,
        covered_keys,
        uncovered_mandatory,
        usage,
    })
}

fn tie_break(challenger: &ContextCandidate, incumbent: &ContextCandidate) -> bool {
    challenger
        .tier
        .cmp(&incumbent.tier)
        .then_with(|| incumbent.priority.cmp(&challenger.priority))
        .then_with(|| challenger.entry_id.cmp(&incumbent.entry_id))
        .is_lt()
}

fn marginal_gain(
    candidate: &ContextCandidate,
    coverage: &HashMap<OpaqueId, Vec<String>>,
    weights: &HashMap<String, CoverageWeight>,
    covered: &HashSet<String>,
) -> u32 {
    let mut keys: Vec<&String> = coverage
        .get(&candidate.entry_id)
        .map(|keys| keys.iter().collect())
        .unwrap_or_default();
    keys.sort();
    keys.dedup();
    let mut gain = 0u32;
    for key in keys {
        if covered.contains(key) {
            continue;
        }
        if let Some(weight) = weights.get(key) {
            gain = gain.saturating_add(weight.weight);
        }
    }
    gain
}

fn covered_by(
    candidate: &ContextCandidate,
    coverage: &HashMap<OpaqueId, Vec<String>>,
) -> Vec<String> {
    coverage
        .get(&candidate.entry_id)
        .cloned()
        .unwrap_or_default()
}

fn coverage_weights(
    request: &CoverageRequest,
) -> Result<HashMap<String, CoverageWeight>, ContextError> {
    let mut weights = HashMap::new();
    for weight in &request.weights {
        let key = weight.coverage_key.trim();
        if key.is_empty() {
            return Err(ContextError::InvalidCoverageRequest(
                "coverage_key must not be empty".into(),
            ));
        }
        if weights.contains_key(key) {
            return Err(ContextError::InvalidCoverageRequest(format!(
                "coverage_key declared twice: {key}"
            )));
        }
        weights.insert(key.to_owned(), weight.clone());
    }
    Ok(weights)
}

fn coverage_index(
    request: &CoverageRequest,
) -> Result<HashMap<OpaqueId, Vec<String>>, ContextError> {
    let mut index: HashMap<OpaqueId, Vec<String>> = HashMap::new();
    for declaration in &request.coverage {
        if index.contains_key(&declaration.entry_id) {
            return Err(ContextError::InvalidCoverageRequest(format!(
                "coverage declared twice for entry {}",
                declaration.entry_id.as_str()
            )));
        }
        index.insert(
            declaration.entry_id.clone(),
            declaration.coverage_keys.clone(),
        );
    }
    Ok(index)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::ContextCandidate;
    use memory_domain::{MemoryLifecycle, ScopeKind, ScopeRef};

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("scope"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:optimizer-test".into(),
        }
    }

    fn identity() -> ContextIdentity {
        ContextIdentity {
            context_id: id("context"),
            scope_refs: vec![scope()],
            agent_id: id("agent"),
            agent_instance_id: id("instance"),
            session_id: id("session"),
            task_id: Some(id("task")),
            environment_id: None,
            purpose: "optimizer test".into(),
            schema_version: "1".into(),
        }
    }

    fn candidate(entry: &str, tier: ContextTier, content: &str) -> ContextCandidate {
        ContextCandidate {
            entry_id: id(entry),
            memory_id: id(&format!("memory-{entry}")),
            memory_version_id: id(&format!("version-{entry}")),
            memory_lifecycle: MemoryLifecycle::Active,
            scope_refs: vec![scope()],
            tier,
            priority: 5,
            activation_reason: "optimizer test".into(),
            rendered_content: content.into(),
            source_refs: vec![id(&format!("source-{entry}"))],
            evidence_refs: vec![],
            epistemic_qualifiers: vec!["reported".into()],
            content_hash: format!("sha256:{entry}"),
        }
    }

    fn weight(key: &str, value: u32, mandatory: bool) -> CoverageWeight {
        CoverageWeight {
            coverage_key: key.into(),
            weight: value,
            mandatory,
        }
    }

    fn coverage(entry: &str, keys: &[&str]) -> CandidateCoverage {
        CandidateCoverage {
            entry_id: id(entry),
            coverage_keys: keys.iter().map(|key| (*key).to_owned()).collect(),
        }
    }

    #[test]
    fn selection_ranks_by_marginal_coverage_per_byte() {
        let request = CoverageRequest {
            weights: vec![weight("k1", 10, true), weight("k2", 1, false)],
            coverage: vec![coverage("wide", &["k1"]), coverage("narrow", &["k2"])],
        };
        // Both fit, but `narrow` has the better gain-per-byte (1/1 vs 10/20),
        // so it is ranked first even though `wide` covers the mandatory key.
        let selection = select_coverage_optimal_candidates(
            &identity(),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &request,
            vec![
                candidate("wide", ContextTier::P1, "a much longer rendering"),
                candidate("narrow", ContextTier::P1, "x"),
            ],
        )
        .unwrap();
        assert_eq!(selection.selected.len(), 2);
        assert_eq!(selection.order[0].entry_id, id("narrow"));
        assert_eq!(selection.order[0].marginal_gain, 1);
        assert_eq!(selection.order[1].entry_id, id("wide"));
        assert_eq!(selection.order[1].marginal_gain, 10);
        assert!(selection.uncovered_mandatory.is_empty());
    }

    #[test]
    fn a_redundant_candidate_is_deferred_with_zero_marginal_coverage() {
        let request = CoverageRequest {
            weights: vec![weight("k1", 10, false)],
            coverage: vec![
                coverage("first", &["k1"]),
                // Same key: a paraphrase, not extra coverage.
                coverage("second", &["k1"]),
            ],
        };
        let selection = select_coverage_optimal_candidates(
            &identity(),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &request,
            vec![
                candidate("first", ContextTier::P1, "one"),
                candidate("second", ContextTier::P1, "two"),
            ],
        )
        .unwrap();
        assert_eq!(selection.selected.len(), 1);
        assert_eq!(selection.deferred.len(), 1);
        assert_eq!(
            selection.deferred[0].reason,
            DeferredReason::ZeroMarginalCoverage
        );
        assert!(!selection.deferred[0].reason.is_budget_limited());
    }

    #[test]
    fn protected_p0_anchors_are_admitted_before_ranking_and_fail_hard_when_they_cannot_fit() {
        let request = CoverageRequest {
            weights: vec![weight("k1", 10, false)],
            coverage: vec![coverage("anchor", &["k1"])],
        };
        let oversized = select_coverage_optimal_candidates(
            &identity(),
            &ContextBudgetVector::two_dimensional(1, 4),
            &request,
            vec![candidate("anchor", ContextTier::P0, "way over four bytes")],
        );
        // A protected anchor that does not fit is an error, never a silent drop.
        assert!(matches!(
            oversized,
            Err(ContextError::BudgetVector(
                BudgetVectorViolation::RenderedBytes { .. }
            ))
        ));
        let fits = select_coverage_optimal_candidates(
            &identity(),
            &ContextBudgetVector::two_dimensional(1, 4),
            &request,
            vec![candidate("anchor", ContextTier::P0, "ok")],
        )
        .unwrap();
        assert!(fits.order[0].mandatory_anchor);
    }

    #[test]
    fn duplicate_membership_is_deferred_and_an_uncoverable_mandatory_key_is_reported() {
        let request = CoverageRequest {
            weights: vec![
                weight("k1", 10, false),
                weight("k2", 10, false),
                weight("never", 5, true),
            ],
            // The twin covers a *different* key, so it has positive marginal
            // gain and reaches the membership check instead of being filtered
            // out as zero-gain redundancy.
            coverage: vec![coverage("first", &["k1"]), coverage("second", &["k2"])],
        };
        let mut twin = candidate("second", ContextTier::P1, "two");
        // Same canonical membership as `first`: not a new fact.
        twin.memory_id = id("memory-first");
        twin.memory_version_id = id("version-first");
        let selection = select_coverage_optimal_candidates(
            &identity(),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &request,
            vec![candidate("first", ContextTier::P1, "one"), twin],
        )
        .unwrap();
        assert_eq!(
            selection.deferred[0].reason,
            DeferredReason::DuplicateMembership
        );
        assert_eq!(selection.uncovered_mandatory, vec!["never".to_owned()]);
    }

    #[test]
    fn a_candidate_violating_a_hard_constraint_is_an_error_not_a_low_score() {
        let mut ineligible = candidate("bad", ContextTier::P1, "content");
        ineligible.memory_lifecycle = MemoryLifecycle::Forgotten;
        let request = CoverageRequest {
            weights: vec![weight("k1", 1, false)],
            coverage: vec![coverage("bad", &["k1"])],
        };
        assert_eq!(
            select_coverage_optimal_candidates(
                &identity(),
                &ContextBudgetVector::two_dimensional(8, 1024),
                &request,
                vec![ineligible],
            ),
            Err(ContextError::IneligibleLifecycle)
        );
    }
}
