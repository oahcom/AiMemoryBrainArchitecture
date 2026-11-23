//! Privacy-safe report projections over the budget/sufficiency and delivery
//! computations.
//!
//! Two coverage rows are served here, and they need different shapes:
//!
//! * `context-budget-and-sufficiency.md` §8–§9.4 asks for utilization,
//!   per-dimension coverage and omissions, exclusion counts, the exact
//!   ContextVersion, the per-partition watermark vector and an outcome
//!   correlation. `BudgetSufficiencyReport` carries that.
//! * `context-manager.md` §7, §9 asks that Context, Entry and Delivery
//!   lifecycles stay separate axes and that delivery states be countable
//!   without putting high-cardinality identifiers into metric labels.
//!   `DeliveryLifecycleReport` carries tallies only.
//!
//! Both builders are projections. They never re-run selection, never
//! re-evaluate sufficiency and never copy rendered content. Where a spec
//! section names an identifier, the report carries a stable digest or
//! nothing:
//!
//! * the requirement profile is reduced to a SHA-256 digest;
//! * requirement ids and the `Unknown { reason }` text are dropped, because
//!   both are caller-supplied and may embed memory or scope identifiers;
//! * an excluded candidate contributes a reason label and a count, never an
//!   id — which is also what §9.4 asks for ("blocked/deferred refs without
//!   leaking unauthorized existence or counts");
//! * a caller-supplied `SufficiencyDimension::Unknown(name)` is redacted to
//!   a single label instead of echoing the name;
//! * index/partition watermarks are carried as-is: they name infrastructure
//!   partitions, not memory content or user identity, and §9.1 requires the
//!   per-partition vector rather than one collapsed maximum.

use crate::{
    sha256_hex, BlockedRefs, BudgetUsage, BudgetVector, CanonicalWatermark, ContextBudget,
    ContextCandidate, DeliveryId, DeliveryLifecycle, DeliveryState, SelectionBudgetUsage,
    SufficiencyAssessment, SufficiencyDimension, SufficiencyOutcome, SufficiencyReport,
};
use std::collections::{BTreeMap, HashSet};

/// Payload-free classification of a sufficiency outcome.
///
/// The requirement lists carried by `SufficiencyOutcome` hold caller-supplied
/// requirement ids, so only the classification crosses into the report.
#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub enum SufficiencyOutcomeKind {
    Sufficient,
    Conditional,
    Insufficient,
    Unknown,
}

impl From<&SufficiencyOutcome> for SufficiencyOutcomeKind {
    fn from(outcome: &SufficiencyOutcome) -> Self {
        match outcome {
            SufficiencyOutcome::Sufficient => Self::Sufficient,
            SufficiencyOutcome::Conditional { .. } => Self::Conditional,
            SufficiencyOutcome::Insufficient { .. } => Self::Insufficient,
            SufficiencyOutcome::Unknown { .. } => Self::Unknown,
        }
    }
}

/// The budget dimensions this crate can actually measure, as used and limited.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BudgetUtilization {
    pub entries_used: usize,
    pub entries_limit: usize,
    pub rendered_bytes_used: usize,
    pub rendered_bytes_limit: usize,
}

/// How many candidates were excluded for one hard constraint.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ExclusionCount {
    /// The first violated constraint, as named by the selector.
    pub constraint: &'static str,
    pub count: usize,
}

/// How many requirements of one dimension the assessment left unmet.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DimensionOmission {
    /// Stable dimension label. Caller-supplied unknown dimensions are
    /// redacted to `"unknown_dimension"` rather than echoed.
    pub dimension: String,
    /// Whether the omission was mandatory (drives Insufficient) or advisory
    /// (drives Conditional).
    pub mandatory: bool,
    pub count: usize,
}

/// Budget and sufficiency observability report (`context-budget-and-sufficiency.md`
/// §8–§9.4).
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct BudgetSufficiencyReport {
    /// Exact ContextVersion the report describes.
    pub context_version: u64,
    /// SHA-256 of the requirement-profile version, never the raw profile.
    pub requirement_profile_digest: String,
    pub outcome: SufficiencyOutcomeKind,
    pub evaluated_requirements: usize,
    pub utilization: BudgetUtilization,
    /// Number of excluded candidates. Equal to the sum of `exclusions`.
    pub excluded_total: usize,
    /// One entry per distinct unmet hard constraint, ordered by name.
    pub exclusions: Vec<ExclusionCount>,
    /// One entry per dimension with unmet requirements, ordered by
    /// (dimension label, mandatory).
    pub omissions: Vec<DimensionOmission>,
    /// Per-index/per-partition watermarks, in the caller's order.
    pub watermarks: Vec<CanonicalWatermark>,

    /// §9.4 item 4: canonical commit/fence references and the PermissionEpoch
    /// decision. `None` means the domain report did not carry it.
    pub canonical_commit_ref: Option<String>,
    pub forget_fence_ref: Option<String>,
    pub permission_epoch: Option<u64>,

    /// §9.4 item 5: the budget vector alongside measured usage.
    ///
    /// `None` means no vector was supplied / nothing was measured. That is not
    /// zero, so neither field may be folded into a default.
    pub budget: Option<BudgetVector>,
    pub budget_usage: Option<BudgetUsage>,
    pub token_estimate_profile: Option<String>,
    pub rendered_bytes: Option<usize>,
    pub entries: Option<usize>,

    /// §9.4 item 6: compacted source membership and the profiles used to
    /// validate and digest it.
    pub compacted_sources: Vec<String>,
    pub validation_profile: Option<String>,
    pub digest_profile: Option<String>,

    /// §9.4 item 7: disclosure-controlled references.
    ///
    /// Carried as the domain type rather than flattened into a list plus a
    /// count, so the "no undisclosed total" guarantee stays a property of the
    /// type instead of a rule this module promises to follow.
    pub blocked: BlockedRefs,
    pub deferred: BlockedRefs,

    /// False means the optional/empty fields above cannot be read as
    /// established negatives.
    pub sufficiency_currentness_established: bool,
}

/// Project the selection and sufficiency results into a report.
///
/// Every input is data the engine already produced: `usage` and `excluded`
/// come from the selector, `assessment` from `assess_sufficiency`. Nothing is
/// recomputed, so the report cannot disagree with the decision it describes.
pub fn build_budget_sufficiency_report(
    sufficiency: &SufficiencyReport,
    budget: &ContextBudget,
    usage: &SelectionBudgetUsage,
    excluded: &[(&ContextCandidate, &'static str)],
    assessment: &SufficiencyAssessment,
    watermarks: &[CanonicalWatermark],
) -> BudgetSufficiencyReport {
    let mut by_constraint: BTreeMap<&'static str, usize> = BTreeMap::new();
    for (_, constraint) in excluded {
        *by_constraint.entry(*constraint).or_insert(0) += 1;
    }
    let exclusions = by_constraint
        .into_iter()
        .map(|(constraint, count)| ExclusionCount { constraint, count })
        .collect();

    let mut by_dimension: BTreeMap<(String, bool), usize> = BTreeMap::new();
    let unmet = match &assessment.outcome {
        SufficiencyOutcome::Insufficient { unmet_mandatory } => {
            Some((unmet_mandatory.as_slice(), true))
        }
        SufficiencyOutcome::Conditional { unmet_advisory } => {
            Some((unmet_advisory.as_slice(), false))
        }
        SufficiencyOutcome::Sufficient | SufficiencyOutcome::Unknown { .. } => None,
    };
    if let Some((requirements, mandatory)) = unmet {
        for requirement in requirements {
            *by_dimension
                .entry((dimension_label(&requirement.dimension), mandatory))
                .or_insert(0) += 1;
        }
    }
    let omissions = by_dimension
        .into_iter()
        .map(|((dimension, mandatory), count)| DimensionOmission {
            dimension,
            mandatory,
            count,
        })
        .collect();

    BudgetSufficiencyReport {
        context_version: sufficiency.context_version(),
        requirement_profile_digest: format!(
            "sha256:{}",
            sha256_hex(sufficiency.requirement_profile_version().as_bytes())
        ),
        outcome: SufficiencyOutcomeKind::from(&assessment.outcome),
        evaluated_requirements: assessment.evaluated_requirements,
        utilization: BudgetUtilization {
            entries_used: usage.entries,
            entries_limit: budget.max_entries,
            rendered_bytes_used: usage.rendered_bytes,
            rendered_bytes_limit: budget.max_rendered_bytes,
        },
        excluded_total: excluded.len(),
        exclusions,
        omissions,
        watermarks: watermarks.to_vec(),

        canonical_commit_ref: sufficiency.canonical_commit_ref.clone(),
        forget_fence_ref: sufficiency.forget_fence_ref.clone(),
        permission_epoch: sufficiency.permission_epoch,

        budget: sufficiency.budget.clone(),
        budget_usage: sufficiency.budget_usage.clone(),
        token_estimate_profile: sufficiency.token_estimate_profile.clone(),
        rendered_bytes: sufficiency.rendered_bytes,
        entries: sufficiency.entries,

        compacted_sources: sufficiency.compacted_sources.clone(),
        validation_profile: sufficiency.validation_profile.clone(),
        digest_profile: sufficiency.digest_profile.clone(),

        blocked: sufficiency.blocked.clone(),
        deferred: sufficiency.deferred.clone(),

        sufficiency_currentness_established: sufficiency.currentness_established(),
    }
}

/// Stable, privacy-safe label for a dimension.
fn dimension_label(dimension: &SufficiencyDimension) -> String {
    match dimension {
        // The payload is caller-supplied text and may name a memory or scope.
        SufficiencyDimension::Unknown(_) => "unknown_dimension".into(),
        known => known.label(),
    }
}

/// Delivery-side tallies for `context-manager.md` §7, §9.
///
/// The three lifecycles are separate axes: a delivery may be `Acknowledged`
/// while the desired Context head has moved on, and a Context may be Active
/// while one delivery is abandoned. This report therefore holds delivery
/// state only — no context version, no entry state, and no identifiers.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DeliveryLifecycleReport {
    pub pending: usize,
    pub delivered: usize,
    pub acknowledged: usize,
    pub superseded: usize,
    pub abandoned: usize,
    /// Observed ids with no lifecycle record. §9 calls these unknown
    /// deliveries; they are never folded into a known state.
    pub unknown_deliveries: usize,
    /// Sum of late-ACK counts, the delivery-side stale-ack signal.
    pub late_acks: u64,
}

/// Tally delivery states for `observed`, counting each distinct id once.
pub fn summarize_delivery_lifecycle(
    lifecycle: &DeliveryLifecycle,
    observed: &[DeliveryId],
) -> DeliveryLifecycleReport {
    let mut report = DeliveryLifecycleReport {
        pending: 0,
        delivered: 0,
        acknowledged: 0,
        superseded: 0,
        abandoned: 0,
        unknown_deliveries: 0,
        late_acks: 0,
    };

    let mut seen = HashSet::new();
    for delivery in observed {
        if !seen.insert(delivery) {
            continue;
        }
        match lifecycle.state(delivery) {
            Some(DeliveryState::Pending) => report.pending += 1,
            Some(DeliveryState::Delivered) => report.delivered += 1,
            Some(DeliveryState::Acknowledged) => report.acknowledged += 1,
            Some(DeliveryState::Superseded) => report.superseded += 1,
            Some(DeliveryState::Abandoned) => report.abandoned += 1,
            None => report.unknown_deliveries += 1,
        }
        if let Some(record) = lifecycle.record(delivery) {
            report.late_acks += record.late_ack_count();
        }
    }

    report
}
