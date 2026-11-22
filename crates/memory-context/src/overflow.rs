//! Overflow degradation planning.
//!
//! `context-budget-and-sufficiency.md` §6–§7 require a specific degradation
//! order when a plan exceeds budget, and forbid the silent drop of protected
//! tiers, risk, uncertainty or provenance:
//!
//! 1. recompute estimates under the target rendering profile;
//! 2. remove redundant entries and move low marginal value to the deferred tier;
//! 3. compact eligible groups with fidelity validation;
//! 4. reduce optional relation/evidence expansion while retaining required refs;
//! 5. ask the retrieval side for narrower candidates;
//! 6. if hard requirements still exceed budget, report Insufficient with the
//!    exact gaps.
//!
//! This module is a *planner*: it returns the ordered list of degradations a
//! caller must execute, together with the exact size the deterministic steps
//! would produce. It never mutates the snapshot and it never proposes removing a
//! P0 entry. Steps whose result depends on a compactor or on the retrieval side
//! are proposed but excluded from the predicted size, and that exclusion is
//! documented rather than guessed.

use crate::budget_vector::{BudgetUsage, ContextBudgetVector};
use crate::{
    validate_snapshot, ContextEntry, ContextError, ContextSnapshot, ContextTier, OpaqueId,
};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashSet};

/// One ordered degradation the caller must execute.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum OverflowStep {
    /// §7.1 — re-derive every estimate with the target rendering profile.
    RecomputeEstimates { tokenizer_profile: String },
    /// §7.2 — drop a duplicate that carries no coverage the survivor lacks.
    DemoteRedundantDuplicate {
        entry_id: OpaqueId,
        covered_by: OpaqueId,
    },
    /// §7.2 — move low marginal value entries out of the managed region.
    MoveToDeferredTier { entry_ids: Vec<OpaqueId> },
    /// §7.3 — compact a group that shares provenance. The resulting size depends
    /// on the compactor and is therefore not part of the predicted size.
    CompactEligibleGroup { source_entry_ids: Vec<OpaqueId> },
    /// §7.4 — drop optional expansion entries (P3) while keeping required refs.
    ReduceOptionalExpansion { entry_ids: Vec<OpaqueId> },
    /// §7.5 — ask the retrieval side for narrower candidates.
    RequestNarrowerCandidates { overage: Vec<String> },
    /// §7.6 — hard requirements still do not fit: report Insufficient.
    ReportInsufficient { gaps: Vec<String> },
}

impl OverflowStep {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::RecomputeEstimates { .. } => "recompute_estimates",
            Self::DemoteRedundantDuplicate { .. } => "demote_redundant_duplicate",
            Self::MoveToDeferredTier { .. } => "move_to_deferred_tier",
            Self::CompactEligibleGroup { .. } => "compact_eligible_group",
            Self::ReduceOptionalExpansion { .. } => "reduce_optional_expansion",
            Self::RequestNarrowerCandidates { .. } => "request_narrower_candidates",
            Self::ReportInsufficient { .. } => "report_insufficient",
        }
    }
}

/// The verdict of one overflow round.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum OverflowPlan {
    /// The plan already fits; no degradation is required.
    WithinBudget { usage: BudgetUsage },
    /// Deterministic degradations bring the plan inside the vector budget.
    Degraded {
        steps: Vec<OverflowStep>,
        resulting_entries: usize,
        resulting_bytes: usize,
        deferred_entry_ids: Vec<OpaqueId>,
        usage: BudgetUsage,
    },
    /// Protected content cannot fit; the caller must report Insufficient.
    Blocked {
        steps: Vec<OverflowStep>,
        /// Exact overage, expressed against the remaining protected entries.
        gaps: Vec<String>,
        usage: BudgetUsage,
    },
}

impl OverflowPlan {
    /// The ordered steps this plan asks the caller to execute.
    pub fn steps(&self) -> &[OverflowStep] {
        match self {
            Self::WithinBudget { .. } => &[],
            Self::Degraded { steps, .. } | Self::Blocked { steps, .. } => steps,
        }
    }

    /// `true` when no degradation was necessary.
    pub fn is_within_budget(&self) -> bool {
        matches!(self, Self::WithinBudget { .. })
    }

    /// `true` when protected content cannot fit and Insufficient must be reported.
    pub fn is_blocked(&self) -> bool {
        matches!(self, Self::Blocked { .. })
    }
}

/// Build the ordered degradation plan for one snapshot under one budget vector.
///
/// # Errors
///
/// Returns a snapshot integrity error when the inputs are internally
/// inconsistent, and [`ContextError::BudgetVector`] when the budget itself is
/// malformed.
pub fn plan_overflow(
    snapshot: &ContextSnapshot,
    budget: &ContextBudgetVector,
) -> Result<OverflowPlan, ContextError> {
    validate_snapshot(snapshot)?;
    budget.validate().map_err(ContextError::BudgetVector)?;
    let mut working: Vec<ContextEntry> = snapshot.entries.clone();
    if budget.check_entries(&working).is_ok() {
        return Ok(OverflowPlan::WithinBudget {
            usage: budget.usage_for_entries(&working),
        });
    }

    let mut steps: Vec<OverflowStep> = Vec::new();
    let mut deferred_entry_ids: Vec<OpaqueId> = Vec::new();

    // §7.1 — estimates are always the first thing to re-derive.
    steps.push(OverflowStep::RecomputeEstimates {
        tokenizer_profile: budget
            .token_budget
            .as_ref()
            .and_then(|token_budget| token_budget.tokenizer_profile.clone())
            .unwrap_or_else(|| "unknown-profile-conservative-upper-bound".into()),
    });

    // §7.2a — duplicate content carries no marginal coverage. P0 is exempt.
    for (entry_id, covered_by) in redundant_duplicates(&working) {
        if let Some(index) = working.iter().position(|entry| entry.entry_id == entry_id) {
            working.remove(index);
            deferred_entry_ids.push(entry_id.clone());
            steps.push(OverflowStep::DemoteRedundantDuplicate {
                entry_id,
                covered_by,
            });
        }
    }
    if budget.check_entries(&working).is_ok() {
        return Ok(degraded(steps, working, deferred_entry_ids, budget));
    }

    // §7.3 — compaction is proposed, but its output size belongs to the compactor.
    for group in compaction_groups(&working) {
        steps.push(OverflowStep::CompactEligibleGroup {
            source_entry_ids: group,
        });
    }

    // §7.2b — move the lowest marginal value out of the managed region.
    let mut demoted: Vec<OpaqueId> = Vec::new();
    for entry_id in deferrable_order(&working) {
        if budget.check_entries(&working).is_ok() {
            break;
        }
        if let Some(index) = working.iter().position(|entry| entry.entry_id == entry_id) {
            working.remove(index);
            deferred_entry_ids.push(entry_id.clone());
            demoted.push(entry_id);
        }
    }
    if !demoted.is_empty() {
        steps.push(OverflowStep::MoveToDeferredTier { entry_ids: demoted });
    }
    if budget.check_entries(&working).is_ok() {
        return Ok(degraded(steps, working, deferred_entry_ids, budget));
    }

    // §7.4 — optional expansion (P3) is the remainder that was never mandatory.
    let optional: Vec<OpaqueId> = working
        .iter()
        .filter(|entry| entry.tier == ContextTier::P3)
        .map(|entry| entry.entry_id.clone())
        .collect();
    if !optional.is_empty() {
        working.retain(|entry| entry.tier != ContextTier::P3);
        deferred_entry_ids.extend(optional.iter().cloned());
        steps.push(OverflowStep::ReduceOptionalExpansion {
            entry_ids: optional,
        });
    }
    if budget.check_entries(&working).is_ok() {
        return Ok(degraded(steps, working, deferred_entry_ids, budget));
    }

    // §7.5–§7.6 — protected content does not fit. Report the exact gap.
    let usage = budget.usage_for_entries(&working);
    let gaps = limit_gaps(&usage, budget);
    steps.push(OverflowStep::RequestNarrowerCandidates {
        overage: gaps.clone(),
    });
    steps.push(OverflowStep::ReportInsufficient { gaps: gaps.clone() });
    Ok(OverflowPlan::Blocked { steps, gaps, usage })
}

fn degraded(
    steps: Vec<OverflowStep>,
    working: Vec<ContextEntry>,
    deferred_entry_ids: Vec<OpaqueId>,
    budget: &ContextBudgetVector,
) -> OverflowPlan {
    let usage = budget.usage_for_entries(&working);
    OverflowPlan::Degraded {
        steps,
        resulting_entries: usage.entries,
        resulting_bytes: usage.rendered_bytes,
        deferred_entry_ids,
        usage,
    }
}

/// Exact overage strings for a set that cannot fit.
fn limit_gaps(usage: &BudgetUsage, budget: &ContextBudgetVector) -> Vec<String> {
    let mut gaps = Vec::new();
    if usage.entries > budget.max_entries {
        gaps.push(format!(
            "entry_count {} > {}",
            usage.entries, budget.max_entries
        ));
    }
    if usage.rendered_bytes > budget.max_rendered_bytes {
        gaps.push(format!(
            "rendered_bytes {} > {}",
            usage.rendered_bytes, budget.max_rendered_bytes
        ));
    }
    if let (Some(limit), Some(estimate)) = (&budget.token_budget, &usage.estimated_tokens) {
        if estimate.tokens > limit.max_estimated_tokens {
            gaps.push(format!(
                "estimated_tokens {} > {}",
                estimate.tokens, limit.max_estimated_tokens
            ));
        }
    }
    if let Some(limit) = budget.max_distinct_canonical_refs {
        if usage.distinct_canonical_refs > limit {
            gaps.push(format!(
                "distinct_canonical_refs {} > {limit}",
                usage.distinct_canonical_refs
            ));
        }
    }
    if let Some(limit) = budget.max_relation_fanout {
        if usage.relation_fanout > limit {
            gaps.push(format!(
                "relation_fanout {} > {limit}",
                usage.relation_fanout
            ));
        }
    }
    if gaps.is_empty() {
        // A saturated region can also fail a tier floor rather than a size limit.
        for reserve in &budget.tier_reserves {
            let held = usage.entries_in(reserve.tier);
            if held < reserve.reserved_entries {
                gaps.push(format!(
                    "protected_tier {:?} {} < {}",
                    reserve.tier, held, reserve.reserved_entries
                ));
            }
        }
    }
    gaps
}

/// Duplicate-content entries that can be dropped, as `(dropped, survivor)`.
///
/// Only P1–P3 entries are candidates: P0 is protected, so a P0 duplicate is
/// reported by the caller as a planning defect instead of being dropped here.
fn redundant_duplicates(entries: &[ContextEntry]) -> Vec<(OpaqueId, OpaqueId)> {
    let mut groups: BTreeMap<&str, Vec<&ContextEntry>> = BTreeMap::new();
    for entry in entries {
        if entry.tier == ContextTier::P0 {
            continue;
        }
        groups
            .entry(entry.content_hash.as_str())
            .or_default()
            .push(entry);
    }
    let mut drops = Vec::new();
    for members in groups.values() {
        if members.len() < 2 {
            continue;
        }
        let mut ranked = members.clone();
        ranked.sort_by(|left, right| {
            left.tier
                .cmp(&right.tier)
                .then_with(|| right.priority.cmp(&left.priority))
                .then_with(|| left.entry_id.cmp(&right.entry_id))
        });
        let survivor = ranked[0].entry_id.clone();
        for member in &ranked[1..] {
            drops.push((member.entry_id.clone(), survivor.clone()));
        }
    }
    drops
}

/// Groups that share an identical provenance signature and may be compacted.
///
/// A single-entry group has nothing to compact, and a group containing P0 content
/// is not proposed because compaction loss on protected material is not
/// recoverable by the caller.
fn compaction_groups(entries: &[ContextEntry]) -> Vec<Vec<OpaqueId>> {
    let mut groups: BTreeMap<Vec<&str>, Vec<&ContextEntry>> = BTreeMap::new();
    for entry in entries {
        if entry.tier == ContextTier::P0 {
            continue;
        }
        let mut signature: Vec<&str> = entry
            .source_refs
            .iter()
            .map(|reference| reference.as_str())
            .collect();
        signature.sort_unstable();
        groups.entry(signature).or_default().push(entry);
    }
    let mut out = Vec::new();
    for members in groups.values() {
        if members.len() < 2 {
            continue;
        }
        let mut source_entry_ids: Vec<OpaqueId> =
            members.iter().map(|entry| entry.entry_id.clone()).collect();
        source_entry_ids.sort();
        out.push(source_entry_ids);
    }
    out
}

/// Non-protected entries in the order they should leave the managed region:
/// P2 before P1, lowest priority first, then ascending entry id.
fn deferrable_order(entries: &[ContextEntry]) -> Vec<OpaqueId> {
    let mut candidates: Vec<&ContextEntry> = entries
        .iter()
        .filter(|entry| entry.tier == ContextTier::P2 || entry.tier == ContextTier::P1)
        .collect();
    candidates.sort_by(|left, right| {
        right
            .tier
            .cmp(&left.tier)
            .then_with(|| left.priority.cmp(&right.priority))
            .then_with(|| left.entry_id.cmp(&right.entry_id))
    });
    let mut seen: HashSet<OpaqueId> = HashSet::new();
    candidates
        .into_iter()
        .filter(|entry| seen.insert(entry.entry_id.clone()))
        .map(|entry| entry.entry_id.clone())
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{ContextIdentity, ContextSnapshot};
    use memory_domain::{ScopeKind, ScopeRef};

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn identity() -> ContextIdentity {
        ContextIdentity {
            context_id: id("context"),
            scope_refs: vec![ScopeRef {
                scope_id: id("scope"),
                scope_kind: ScopeKind::User,
                namespace_key: "user:overflow-test".into(),
            }],
            agent_id: id("agent"),
            agent_instance_id: id("instance"),
            session_id: id("session"),
            task_id: Some(id("task")),
            environment_id: None,
            purpose: "overflow test".into(),
            schema_version: "1".into(),
        }
    }

    fn entry(
        name: &str,
        tier: ContextTier,
        priority: i32,
        content: &str,
        hash: &str,
    ) -> ContextEntry {
        ContextEntry {
            entry_id: id(name),
            memory_id: id(&format!("memory-{name}")),
            memory_version_id: id(&format!("version-{name}")),
            tier,
            priority,
            activation_reason: "overflow test".into(),
            rendered_content: content.into(),
            source_refs: vec![id(&format!("source-{name}"))],
            evidence_refs: vec![],
            epistemic_qualifiers: vec!["reported".into()],
            content_hash: hash.into(),
            rendered_bytes: content.len(),
            compacted_from: Vec::new(),
        }
    }

    fn snapshot(entries: Vec<ContextEntry>) -> ContextSnapshot {
        let rendered_bytes = entries.iter().map(|entry| entry.rendered_bytes).sum();
        ContextSnapshot {
            identity: identity(),
            context_version: 1,
            entries,
            tombstones: vec![],
            operation_records: vec![],
            rendered_bytes,
        }
    }

    #[test]
    fn a_plan_that_already_fits_requires_no_degradation() {
        let plan = plan_overflow(
            &snapshot(vec![entry("a", ContextTier::P0, 5, "aa", "h-a")]),
            &ContextBudgetVector::two_dimensional(4, 64),
        )
        .unwrap();
        assert!(plan.is_within_budget());
        assert!(plan.steps().is_empty());
    }

    #[test]
    fn a_redundant_duplicate_is_demoted_before_anything_protected_is_touched() {
        // Two P1 entries with the same content hash, plus one P0 anchor. The
        // byte budget only fits two entries, so the duplicate must go first.
        let plan = plan_overflow(
            &snapshot(vec![
                entry("anchor", ContextTier::P0, 9, "keep", "h-anchor"),
                entry("dup-a", ContextTier::P1, 5, "same", "h-dup"),
                entry("dup-b", ContextTier::P1, 3, "same", "h-dup"),
            ]),
            &ContextBudgetVector::two_dimensional(2, 12),
        )
        .unwrap();
        let steps = plan.steps();
        assert_eq!(steps[0].label(), "recompute_estimates");
        assert_eq!(steps[1].label(), "demote_redundant_duplicate");
        // The lower-priority duplicate is the one dropped, and it is recorded.
        match &steps[1] {
            OverflowStep::DemoteRedundantDuplicate {
                entry_id,
                covered_by,
            } => {
                assert_eq!(entry_id, &id("dup-b"));
                assert_eq!(covered_by, &id("dup-a"));
            }
            other => panic!("expected a duplicate demotion, got {other:?}"),
        }
        match plan {
            OverflowPlan::Degraded {
                resulting_entries,
                deferred_entry_ids,
                ..
            } => {
                assert_eq!(resulting_entries, 2);
                assert_eq!(deferred_entry_ids, vec![id("dup-b")]);
            }
            other => panic!("expected a degraded plan, got {other:?}"),
        }
    }

    #[test]
    fn protected_content_that_cannot_fit_is_blocked_with_exact_gaps() {
        let plan = plan_overflow(
            &snapshot(vec![entry(
                "anchor",
                ContextTier::P0,
                9,
                "protected content",
                "h",
            )]),
            &ContextBudgetVector::two_dimensional(4, 4),
        )
        .unwrap();
        assert!(plan.is_blocked());
        match plan {
            OverflowPlan::Blocked { gaps, steps, .. } => {
                assert_eq!(gaps, vec!["rendered_bytes 17 > 4".to_owned()]);
                // Narrower candidates are requested before Insufficient is reported.
                assert_eq!(
                    steps[steps.len() - 2].label(),
                    "request_narrower_candidates"
                );
                assert_eq!(steps[steps.len() - 1].label(), "report_insufficient");
            }
            other => panic!("expected a blocked plan, got {other:?}"),
        }
    }

    #[test]
    fn a_low_marginal_p1_entry_is_demoted_before_optional_expansion_is_touched() {
        let plan = plan_overflow(
            &snapshot(vec![
                entry("anchor", ContextTier::P0, 9, "a", "h1"),
                entry("mid", ContextTier::P1, 9, "b", "h2"),
                entry("extra", ContextTier::P3, 1, "c", "h3"),
            ]),
            &ContextBudgetVector::two_dimensional(3, 2),
        )
        .unwrap();
        // Entry count fits; only the byte dimension is over, and demotion has a
        // P1 candidate, so §7.2 runs before §7.4.
        assert!(matches!(
            plan,
            OverflowPlan::Degraded {
                resulting_entries: 2,
                ..
            }
        ));
        assert!(plan
            .steps()
            .iter()
            .any(|step| step.label() == "move_to_deferred_tier"));
        assert!(!plan
            .steps()
            .iter()
            .any(|step| step.label() == "reduce_optional_expansion"));
    }

    #[test]
    fn optional_p3_expansion_is_reduced_when_no_p1_or_p2_entry_can_be_demoted() {
        // Only protected P0 plus optional P3: §7.2 has nothing to demote, so the
        // optional expansion is the step that closes the gap.
        let plan = plan_overflow(
            &snapshot(vec![
                entry("anchor", ContextTier::P0, 9, "a", "h1"),
                entry("extra", ContextTier::P3, 1, "c", "h3"),
            ]),
            &ContextBudgetVector::two_dimensional(2, 1),
        )
        .unwrap();
        match &plan {
            OverflowPlan::Degraded {
                resulting_entries,
                deferred_entry_ids,
                ..
            } => {
                assert_eq!(*resulting_entries, 1);
                assert_eq!(deferred_entry_ids, &vec![id("extra")]);
            }
            other => panic!("expected a degraded plan, got {other:?}"),
        }
        assert!(plan
            .steps()
            .iter()
            .any(|step| step.label() == "reduce_optional_expansion"));
    }
}
