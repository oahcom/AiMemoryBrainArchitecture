//! Budget and sufficiency observability.
//!
//! `context-budget-and-sufficiency.md` §8 and §9.4 require a sufficiency report
//! that names the exact Context version, the requirement-profile version,
//! per-dimension coverage and omissions, the watermark vector and completeness
//! gaps, the budget vector, compacted source membership and blocked refs — while
//! `context-manager.md` §9 forbids putting high-cardinality identifiers into
//! metric labels.
//!
//! This module therefore produces two different projections of the same report:
//!
//! * [`SufficiencyReport`] — the full artifact, which belongs in a trace or an
//!   audit record and therefore *does* carry the Context identity;
//! * [`SufficiencyReport::metric_labels`] — a low-cardinality projection with
//!   buckets and counts only, which is what a metric backend may index.
//!
//! §9.4 also says a Context must not be published when currentness or
//! completeness cannot be established. That rule is executable as
//! [`SufficiencyReport::is_publishable`].

use crate::budget_vector::{BudgetUsage, ContextBudgetVector};
use crate::{
    assess_sufficiency, sufficiency_measure, CanonicalWatermark, ContextEntry, ContextError,
    ContextSnapshot, SufficiencyAssessment, SufficiencyDimension, SufficiencyOutcome,
    SufficiencyRequirement,
};
use serde::{Deserialize, Serialize};

/// Whether a dimension was measurable for this snapshot.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum CoverageStatus {
    /// Measured and at or above the declared threshold.
    Satisfied { measured: usize, threshold: usize },
    /// Measured and below the declared threshold.
    Unmet { measured: usize, threshold: usize },
    /// The snapshot does not carry structured evidence for this dimension.
    Unknown { reason: String },
}

impl CoverageStatus {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::Satisfied { .. } => "satisfied",
            Self::Unmet { .. } => "unmet",
            Self::Unknown { .. } => "unknown",
        }
    }
}

/// Per-dimension coverage detail.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DimensionCoverage {
    pub requirement_id: String,
    pub dimension: SufficiencyDimension,
    pub mandatory: bool,
    pub status: CoverageStatus,
}

/// How much of the budget vector the region consumed, in per-mille so the value
/// stays exact and comparable without floating point.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct BudgetUtilization {
    pub entries: usize,
    pub max_entries: usize,
    pub entries_permille: u32,
    pub rendered_bytes: usize,
    pub max_rendered_bytes: usize,
    pub bytes_permille: u32,
    pub distinct_canonical_refs: usize,
    pub relation_fanout: usize,
    /// Dimensions the budget constrains but this crate cannot measure.
    pub unmeasured_dimensions: Vec<String>,
}

impl BudgetUtilization {
    /// Build the utilization projection of one measured usage.
    pub fn new(usage: &BudgetUsage, budget: &ContextBudgetVector) -> Self {
        Self {
            entries: usage.entries,
            max_entries: budget.max_entries,
            entries_permille: permille(usage.entries, budget.max_entries),
            rendered_bytes: usage.rendered_bytes,
            max_rendered_bytes: budget.max_rendered_bytes,
            bytes_permille: permille(usage.rendered_bytes, budget.max_rendered_bytes),
            distinct_canonical_refs: usage.distinct_canonical_refs,
            relation_fanout: usage.relation_fanout,
            unmeasured_dimensions: budget
                .unmeasured_dimensions()
                .into_iter()
                .map(str::to_owned)
                .collect(),
        }
    }
}

fn permille(actual: usize, limit: usize) -> u32 {
    if limit == 0 {
        return 0;
    }
    let saturated = actual.min(limit);
    u32::try_from(saturated.saturating_mul(1000) / limit).unwrap_or(1000)
}

/// Blocked-reference reporting that cannot leak unauthorized existence or counts.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum BlockedRefReport {
    /// The caller is authorized for the scope, so the count is reportable.
    Visible { count: usize },
    /// The caller is not authorized, so neither existence nor count is disclosed.
    Redacted,
}

impl BlockedRefReport {
    /// Stable machine label, safe to attach to a metric.
    pub fn label(&self) -> &'static str {
        match self {
            Self::Visible { .. } => "visible",
            Self::Redacted => "redacted",
        }
    }
}

/// Caller-supplied context for one sufficiency report.
#[derive(Clone, Debug, Eq, PartialEq, Default, Serialize, Deserialize)]
pub struct SufficiencyReportInput {
    pub requirements: Vec<SufficiencyRequirement>,
    pub requirement_profile_version: String,
    /// Present only when a canonical commit reference was actually established.
    pub canonical_commit_ref: Option<String>,
    /// Present only when the authorization authority returned a current decision.
    pub permission_epoch_decision: Option<String>,
    pub index_watermarks: Vec<CanonicalWatermark>,
    pub completeness_gaps: Vec<String>,
    /// Number of refs the caller may not see, and whether it may see that count.
    pub blocked_ref_count: Option<usize>,
    pub blocked_refs_authorized: bool,
}

/// The full sufficiency/budget report artifact.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct SufficiencyReport {
    pub context_id: crate::OpaqueId,
    pub context_version: u64,
    pub requirement_profile_version: String,
    pub assessment: SufficiencyAssessment,
    pub dimensions: Vec<DimensionCoverage>,
    pub covered_dimensions: usize,
    pub unknown_dimensions: usize,
    pub unmet_requirement_ids: Vec<String>,
    pub budget: BudgetUtilization,
    pub canonical_commit_ref: Option<String>,
    pub permission_epoch_decision: Option<String>,
    pub index_watermarks: Vec<CanonicalWatermark>,
    pub completeness_gaps: Vec<String>,
    pub compacted_source_membership: Vec<crate::OpaqueId>,
    pub blocked_refs: BlockedRefReport,
}

impl SufficiencyReport {
    /// The overall outcome of the sufficiency assessment.
    pub fn outcome(&self) -> &SufficiencyOutcome {
        &self.assessment.outcome
    }

    /// `true` when every currentness precondition was established and the
    /// outcome does not claim an unmeasured dimension.
    ///
    /// §9.4: if D/I currentness or F completeness cannot be established, do not
    /// publish a Context that implies complete coverage.
    pub fn is_publishable(&self) -> bool {
        if matches!(self.outcome(), SufficiencyOutcome::Unknown { .. }) {
            return false;
        }
        if self.unknown_dimensions > 0
            || !self.completeness_gaps.is_empty()
            || self.permission_epoch_decision.is_none()
            || self.canonical_commit_ref.is_none()
        {
            return false;
        }
        true
    }

    /// High-cardinality subject for a trace span. Deliberately separate from
    /// [`Self::metric_labels`].
    pub fn trace_subject(&self) -> String {
        format!(
            "context={} version={}",
            self.context_id.as_str(),
            self.context_version
        )
    }

    /// Low-cardinality metric labels: no Context id, no version, no ref id.
    pub fn metric_labels(&self) -> Vec<(String, String)> {
        let mut labels = vec![
            (
                "outcome".to_owned(),
                outcome_label(self.outcome()).to_owned(),
            ),
            (
                "coverage".to_owned(),
                coverage_bucket(self.budget.bytes_permille),
            ),
            (
                "entries_bucket".to_owned(),
                count_bucket(self.budget.entries).to_owned(),
            ),
            (
                "unmet_requirements".to_owned(),
                count_bucket(self.unmet_requirement_ids.len()).to_owned(),
            ),
            (
                "unknown_dimensions".to_owned(),
                count_bucket(self.unknown_dimensions).to_owned(),
            ),
            (
                "completeness".to_owned(),
                if self.completeness_gaps.is_empty() {
                    "complete".to_owned()
                } else {
                    "gapped".to_owned()
                },
            ),
            (
                "permission_decision".to_owned(),
                if self.permission_epoch_decision.is_some() {
                    "current".to_owned()
                } else {
                    "absent".to_owned()
                },
            ),
            (
                "blocked_refs".to_owned(),
                self.blocked_refs.label().to_owned(),
            ),
        ];
        labels.sort();
        labels
    }
}

fn outcome_label(outcome: &SufficiencyOutcome) -> &'static str {
    match outcome {
        SufficiencyOutcome::Sufficient => "sufficient",
        SufficiencyOutcome::Conditional { .. } => "conditional",
        SufficiencyOutcome::Insufficient { .. } => "insufficient",
        SufficiencyOutcome::Unknown { .. } => "unknown",
    }
}

fn coverage_bucket(permille: u32) -> String {
    match permille {
        0..=250 => "0-25".into(),
        251..=500 => "25-50".into(),
        501..=750 => "50-75".into(),
        751..=999 => "75-100".into(),
        _ => "100+".into(),
    }
}

fn count_bucket(count: usize) -> &'static str {
    match count {
        0 => "0",
        1 => "1",
        2..=4 => "2-4",
        5..=9 => "5-9",
        _ => "10+",
    }
}

/// Build the sufficiency/budget report for one snapshot.
///
/// # Errors
///
/// Returns a snapshot integrity error when the snapshot cannot be validated, and
/// [`ContextError::BudgetVector`] when the budget vector is malformed.
pub fn build_sufficiency_report(
    snapshot: &ContextSnapshot,
    budget: &ContextBudgetVector,
    input: &SufficiencyReportInput,
) -> Result<SufficiencyReport, ContextError> {
    crate::validate_snapshot(snapshot)?;
    budget.validate().map_err(ContextError::BudgetVector)?;
    if input.requirement_profile_version.trim().is_empty() {
        return Err(ContextError::EmptyField("requirement_profile_version"));
    }
    let usage = budget.usage_for_entries(&snapshot.entries);
    let assessment = assess_sufficiency(snapshot, &input.requirements);
    let dimensions: Vec<DimensionCoverage> = input
        .requirements
        .iter()
        .map(|requirement| DimensionCoverage {
            requirement_id: requirement.requirement_id.clone(),
            dimension: requirement.dimension.clone(),
            mandatory: requirement.mandatory,
            status: dimension_status(snapshot, requirement),
        })
        .collect();
    let covered_dimensions = dimensions
        .iter()
        .filter(|dimension| matches!(dimension.status, CoverageStatus::Satisfied { .. }))
        .count();
    let unknown_dimensions = dimensions
        .iter()
        .filter(|dimension| matches!(dimension.status, CoverageStatus::Unknown { .. }))
        .count();
    let mut unmet_requirement_ids: Vec<String> = dimensions
        .iter()
        .filter(|dimension| matches!(dimension.status, CoverageStatus::Unmet { .. }))
        .map(|dimension| dimension.requirement_id.clone())
        .collect();
    unmet_requirement_ids.sort();

    let compacted_source_membership = compacted_membership(&snapshot.entries);
    let blocked_refs = match (input.blocked_refs_authorized, input.blocked_ref_count) {
        (true, Some(count)) => BlockedRefReport::Visible { count },
        _ => BlockedRefReport::Redacted,
    };

    Ok(SufficiencyReport {
        context_id: snapshot.identity.context_id.clone(),
        context_version: snapshot.context_version,
        requirement_profile_version: input.requirement_profile_version.clone(),
        assessment,
        dimensions,
        covered_dimensions,
        unknown_dimensions,
        unmet_requirement_ids,
        budget: BudgetUtilization::new(&usage, budget),
        canonical_commit_ref: input.canonical_commit_ref.clone(),
        permission_epoch_decision: input.permission_epoch_decision.clone(),
        index_watermarks: input.index_watermarks.clone(),
        completeness_gaps: input.completeness_gaps.clone(),
        compacted_source_membership,
        blocked_refs,
    })
}

fn dimension_status(
    snapshot: &ContextSnapshot,
    requirement: &SufficiencyRequirement,
) -> CoverageStatus {
    match sufficiency_measure(snapshot, &requirement.dimension) {
        Ok(measured) if measured >= requirement.threshold => CoverageStatus::Satisfied {
            measured,
            threshold: requirement.threshold,
        },
        Ok(measured) => CoverageStatus::Unmet {
            measured,
            threshold: requirement.threshold,
        },
        Err(reason) => CoverageStatus::Unknown { reason },
    }
}

/// Every entry id that has become part of a compacted group, sorted and deduped.
fn compacted_membership(entries: &[ContextEntry]) -> Vec<crate::OpaqueId> {
    let mut membership: Vec<crate::OpaqueId> = entries
        .iter()
        .flat_map(|entry| entry.compacted_from.iter().cloned())
        .collect();
    membership.sort();
    membership.dedup();
    membership
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{ContextIdentity, ContextTier};
    use memory_domain::{ScopeKind, ScopeRef};

    fn id(value: &str) -> crate::OpaqueId {
        crate::OpaqueId::new(value).unwrap()
    }

    fn identity(with_environment: bool) -> ContextIdentity {
        ContextIdentity {
            context_id: id("context"),
            scope_refs: vec![ScopeRef {
                scope_id: id("scope"),
                scope_kind: ScopeKind::User,
                namespace_key: "user:report-test".into(),
            }],
            agent_id: id("agent"),
            agent_instance_id: id("instance"),
            session_id: id("session"),
            task_id: Some(id("task")),
            environment_id: with_environment.then(|| id("environment")),
            purpose: "report test".into(),
            schema_version: "1".into(),
        }
    }

    fn entry(name: &str, evidence: &[&str], compacted_from: &[&str]) -> ContextEntry {
        let content = format!("content-{name}");
        ContextEntry {
            entry_id: id(name),
            memory_id: id(&format!("memory-{name}")),
            memory_version_id: id(&format!("version-{name}")),
            tier: ContextTier::P1,
            priority: 5,
            activation_reason: "report test".into(),
            source_refs: vec![id(&format!("source-{name}"))],
            evidence_refs: evidence.iter().map(|value| id(value)).collect(),
            epistemic_qualifiers: vec!["reported".into()],
            content_hash: format!("sha256:{name}"),
            rendered_bytes: content.len(),
            rendered_content: content,
            compacted_from: compacted_from.iter().map(|value| id(value)).collect(),
        }
    }

    fn snapshot(with_environment: bool, entries: Vec<ContextEntry>) -> ContextSnapshot {
        let rendered_bytes = entries.iter().map(|entry| entry.rendered_bytes).sum();
        ContextSnapshot {
            identity: identity(with_environment),
            context_version: 3,
            entries,
            tombstones: vec![],
            operation_records: vec![],
            rendered_bytes,
        }
    }

    fn requirement(
        requirement_id: &str,
        dimension: SufficiencyDimension,
        threshold: usize,
    ) -> SufficiencyRequirement {
        SufficiencyRequirement {
            requirement_id: requirement_id.into(),
            dimension,
            threshold,
            mandatory: true,
        }
    }

    fn input() -> SufficiencyReportInput {
        SufficiencyReportInput {
            requirements: vec![requirement(
                "evidence-primary",
                SufficiencyDimension::EvidenceCoverage,
                1,
            )],
            requirement_profile_version: "profile-1".into(),
            canonical_commit_ref: Some("commit-1".into()),
            permission_epoch_decision: Some("current".into()),
            index_watermarks: vec![],
            completeness_gaps: vec![],
            blocked_ref_count: Some(4),
            blocked_refs_authorized: true,
        }
    }

    #[test]
    fn a_report_is_publishable_only_when_every_currentness_precondition_holds() {
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &input(),
        )
        .unwrap();
        assert_eq!(report.outcome(), &SufficiencyOutcome::Sufficient);
        assert!(report.is_publishable());

        // A completeness gap blocks publication even though the outcome is
        // still Sufficient for the declared requirement.
        let mut gapped = input();
        gapped.completeness_gaps = vec!["partition 7 not caught up".into()];
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &gapped,
        )
        .unwrap();
        assert!(!report.is_publishable());

        // An absent permission decision blocks publication too.
        let mut unauthorized = input();
        unauthorized.permission_epoch_decision = None;
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &unauthorized,
        )
        .unwrap();
        assert!(!report.is_publishable());
    }

    #[test]
    fn an_unmeasurable_dimension_is_unknown_and_blocks_publication() {
        let mut declared = input();
        declared.requirements.push(requirement(
            "semantic",
            SufficiencyDimension::SemanticCoverage,
            1,
        ));
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &declared,
        )
        .unwrap();
        // Unknown outranks the met evidence requirement and is never downgraded.
        assert!(matches!(
            report.outcome(),
            SufficiencyOutcome::Unknown { .. }
        ));
        assert_eq!(report.unknown_dimensions, 1);
        assert_eq!(report.covered_dimensions, 1);
        assert!(!report.is_publishable());
    }

    #[test]
    fn an_unmet_mandatory_requirement_is_named_in_the_report() {
        let mut declared = input();
        declared.requirements = vec![requirement(
            "evidence-two",
            SufficiencyDimension::EvidenceCoverage,
            2,
        )];
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &declared,
        )
        .unwrap();
        assert_eq!(
            report.unmet_requirement_ids,
            vec!["evidence-two".to_owned()]
        );
        assert!(matches!(
            report.outcome(),
            SufficiencyOutcome::Insufficient { .. }
        ));
    }

    #[test]
    fn compacted_source_membership_is_reported_and_deduped() {
        let report = build_sufficiency_report(
            &snapshot(
                false,
                vec![
                    entry(
                        "group-1",
                        &["evidence-1"],
                        &["source-entry-a", "source-entry-b"],
                    ),
                    entry("group-2", &[], &["source-entry-b"]),
                ],
            ),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &input(),
        )
        .unwrap();
        assert_eq!(
            report.compacted_source_membership,
            vec![id("source-entry-a"), id("source-entry-b")]
        );
    }

    #[test]
    fn metric_labels_carry_no_context_identity_or_ref_ids() {
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &input(),
        )
        .unwrap();
        let labels = report.metric_labels();
        let keys: Vec<&str> = labels.iter().map(|(key, _)| key.as_str()).collect();
        assert_eq!(
            keys,
            vec![
                "blocked_refs",
                "completeness",
                "coverage",
                "entries_bucket",
                "outcome",
                "permission_decision",
                "unknown_dimensions",
                "unmet_requirements",
            ]
        );
        // The trace subject, by contrast, does carry the identity.
        assert_eq!(report.trace_subject(), "context=context version=3");
        let joined = format!("{labels:?}");
        assert!(!joined.contains("evidence-1"));
        assert!(!joined.contains("context"));
    }

    #[test]
    fn an_unauthorized_caller_cannot_learn_the_blocked_ref_count() {
        let mut hidden = input();
        hidden.blocked_refs_authorized = false;
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &hidden,
        )
        .unwrap();
        assert_eq!(report.blocked_refs, BlockedRefReport::Redacted);
        assert_eq!(report.blocked_refs.label(), "redacted");

        let visible = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(8, 1024),
            &input(),
        )
        .unwrap();
        assert_eq!(visible.blocked_refs, BlockedRefReport::Visible { count: 4 });
    }

    #[test]
    fn budget_utilization_is_reported_in_per_mille_and_marks_unmeasured_dimensions() {
        let report = build_sufficiency_report(
            &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
            &ContextBudgetVector::two_dimensional(4, 400),
            &input(),
        )
        .unwrap();
        assert_eq!(report.budget.entries, 1);
        assert_eq!(report.budget.max_entries, 4);
        assert_eq!(report.budget.entries_permille, 250);
        assert!(report
            .budget
            .unmeasured_dimensions
            .contains(&"planning_latency".to_owned()));
    }

    #[test]
    fn an_empty_requirement_profile_version_is_rejected() {
        let mut invalid = input();
        invalid.requirement_profile_version = "  ".into();
        assert!(matches!(
            build_sufficiency_report(
                &snapshot(false, vec![entry("a", &["evidence-1"], &[])]),
                &ContextBudgetVector::two_dimensional(8, 1024),
                &invalid,
            ),
            Err(ContextError::EmptyField("requirement_profile_version"))
        ));
    }
}
