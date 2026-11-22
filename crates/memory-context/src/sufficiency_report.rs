//! Domain model for Context sufficiency reporting.
//!
//! `SufficiencyDimension` and `ContextTier` are reused from the parent
//! `memory-context` crate to avoid introducing duplicate domain concepts.
//!
//! Watermarks are stored as a vector because a single maximum watermark
//! cannot represent independent progress or gaps across multiple partitions.
//!
//! Blocked and deferred references distinguish visible identities from
//! redacted references. The public API does not expose the total number of
//! hidden references when their count is not disclosable.
//! There is deliberately no total-count accessor, not even a crate-private one:
//! a `pub(crate)` method would make the "hidden count" a lie told to the reader
//! rather than a property of the type.
//!
//! This module carries the four §9.4 fields that `observability.rs` does not
//! model: canonical commit/fence references and the PermissionEpoch decision,
//! the budget vector alongside its measured usage, compacted source membership
//! with validation/digest profiles, and blocked/deferred references. It is a
//! data carrier, not a second projection: it recomputes nothing, and
//! `observability.rs` remains the place where a report is built from engine
//! outputs. See `context-budget-and-sufficiency.md` §9.4.

use std::collections::BTreeMap;

use crate::budget::{BudgetUsage, BudgetVector};
use crate::{CanonicalWatermark, ContextTier, SufficiencyDimension};

/// Completeness of one reported index/partition.
///
/// `Complete` and `Partial` are per-partition verdicts; `Unknown` means the
/// partition was not reported at all, which §9.1 requires to be distinguishable
/// from "reported and complete".
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum PartitionCompleteness {
    Complete,
    Partial { gaps: Vec<String> },
    Unknown { reason: String },
}

/// One partition's watermark plus its completeness verdict.
///
/// The watermark is `main`'s `CanonicalWatermark`; this type adds only the
/// gap verdict that §9.1 asks for and that `CanonicalWatermark` has no field for.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct PartitionState {
    pub watermark: CanonicalWatermark,
    pub completeness: PartitionCompleteness,
}

/// References whose identities or counts may have disclosure restrictions.
///
/// Public methods expose only authorized visible references and explicitly
/// disclosed counts. A hidden count is represented by `None`.
#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct BlockedRefs {
    visible: Vec<String>,
    redacted_count: Option<usize>,
}

impl BlockedRefs {
    /// Creates an empty reference collection.
    pub fn new() -> Self {
        Self::default()
    }

    /// Records a reference whose identity is authorized for disclosure.
    pub fn record_visible(&mut self, reference: String) {
        self.visible.push(reference);
    }

    /// Records hidden references without disclosing their count.
    ///
    /// Repeated calls preserve the undisclosed state.
    pub fn record_redacted(&mut self) {
        self.redacted_count = None;
    }

    /// Records a count when count disclosure is explicitly authorized.
    ///
    /// A previously undisclosed count cannot be recovered by adding a
    /// disclosed count later.
    pub fn record_redacted_count(&mut self, count: usize) {
        self.redacted_count = match self.redacted_count {
            Some(previous) => previous.checked_add(count),
            None if self.visible.is_empty() => Some(count),
            None => None,
        };
    }

    /// Returns only references whose identities may be disclosed.
    pub fn visible(&self) -> &[String] {
        &self.visible
    }

    /// Returns whether any references have been redacted.
    pub fn has_redactions(&self) -> bool {
        self.redacted_count.is_none() || self.redacted_count.is_some_and(|count| count > 0)
    }

    /// Returns the count only when disclosure is authorized.
    pub fn disclosed_count(&self) -> Option<usize> {
        self.redacted_count
    }
}

/// Why a requirement was omitted from the resulting Context.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum OmissionReason {
    OverBudget,
    HardConstraintFailed { constraint: String },
    UnknownCurrentness,
    ExplicitlyExcluded,
}

/// One explicitly recorded requirement omission.
///
/// Fields are private so callers cannot construct an omission with an
/// incorrectly disabled protection marker.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SafeOmission {
    requirement_id: String,
    dimension: SufficiencyDimension,
    tier: ContextTier,
    reason: OmissionReason,
    protected: bool,
}

impl SafeOmission {
    /// Constructs an omission and derives its protection status.
    ///
    /// P0 requirements and risk, uncertainty, evidence/provenance dimensions
    /// are always protected.
    pub fn new(
        requirement_id: String,
        dimension: SufficiencyDimension,
        tier: ContextTier,
        reason: OmissionReason,
    ) -> Self {
        let protected = tier == ContextTier::P0
            || matches!(
                dimension,
                SufficiencyDimension::RiskCoverage
                    | SufficiencyDimension::UncertaintyCoverage
                    | SufficiencyDimension::EvidenceCoverage
            );

        Self {
            requirement_id,
            dimension,
            tier,
            reason,
            protected,
        }
    }

    pub fn requirement_id(&self) -> &str {
        &self.requirement_id
    }

    pub fn dimension(&self) -> &SufficiencyDimension {
        &self.dimension
    }

    pub fn tier(&self) -> ContextTier {
        self.tier
    }

    pub fn reason(&self) -> &OmissionReason {
        &self.reason
    }

    pub fn is_protected(&self) -> bool {
        self.protected
    }
}

/// Explicitly recorded safe omissions.
#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct SafeOmissions {
    omissions: Vec<SafeOmission>,
}

impl SafeOmissions {
    pub fn new() -> Self {
        Self::default()
    }

    /// Records an omission, preserving its constructor-derived protection.
    pub fn record(&mut self, omission: SafeOmission) {
        self.omissions.push(omission);
    }

    pub fn all(&self) -> &[SafeOmission] {
        &self.omissions
    }

    pub fn protected(&self) -> impl Iterator<Item = &SafeOmission> {
        self.omissions.iter().filter(|omission| omission.protected)
    }

    pub fn protected_count(&self) -> usize {
        self.protected().count()
    }
}

/// Coverage statistics for one sufficiency dimension.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct DimensionCoverage {
    pub dimension: SufficiencyDimension,
    pub required: usize,
    pub covered: usize,
    pub omitted_requirement_ids: Vec<String>,
}

/// Aggregate sufficiency report for a Context version.
///
/// This type is a domain model only. It does not collect metrics, establish
/// authorization, or independently validate canonical commit/fence references.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SufficiencyReport {
    /// Exact Context version represented by this report.
    pub context_version: u64,
    /// Version of the requirement profile used for assessment.
    pub requirement_profile_version: String,
    dimension_coverage: BTreeMap<String, DimensionCoverage>,
    watermarks: Vec<PartitionState>,
    pub canonical_commit_ref: Option<String>,
    pub forget_fence_ref: Option<String>,
    pub permission_epoch: Option<u64>,
    /// Limits the planner was asked to respect. `None` means no vector was supplied.
    pub budget: Option<BudgetVector>,
    /// Measured utilization. `None` means nothing was measured, which is not zero.
    pub budget_usage: Option<BudgetUsage>,
    /// Tokenizer/model identity under which `budget_usage.tokens` was measured.
    ///
    /// `None` means no measurement was collected. It does not mean "no tokenizer".
    pub token_estimate_profile: Option<String>,
    /// Measured rendered size, when collected.
    pub rendered_bytes: Option<usize>,
    /// Measured entry count, when collected.
    pub entries: Option<usize>,
    pub compacted_sources: Vec<String>,
    pub validation_profile: Option<String>,
    pub digest_profile: Option<String>,
    pub blocked: BlockedRefs,
    pub deferred: BlockedRefs,
    omissions: SafeOmissions,
    currentness_established: bool,
}

impl SufficiencyReport {
    /// Creates a report in a fail-closed initial state.
    pub fn new(context_version: u64, requirement_profile_version: String) -> Self {
        Self {
            context_version,
            requirement_profile_version,
            dimension_coverage: BTreeMap::new(),
            watermarks: Vec::new(),
            canonical_commit_ref: None,
            forget_fence_ref: None,
            permission_epoch: None,
            budget: None,
            budget_usage: None,
            token_estimate_profile: None,
            rendered_bytes: None,
            entries: None,
            compacted_sources: Vec::new(),
            validation_profile: None,
            digest_profile: None,
            blocked: BlockedRefs::new(),
            deferred: BlockedRefs::new(),
            omissions: SafeOmissions::new(),
            currentness_established: false,
        }
    }

    /// Records or replaces coverage for a dimension.
    pub fn record_dimension_coverage(&mut self, coverage: DimensionCoverage) {
        let key = format!("{:?}", coverage.dimension);
        self.dimension_coverage.insert(key, coverage);
    }

    /// Appends one partition's watermark and completeness verdict.
    pub fn record_watermark(&mut self, state: PartitionState) {
        self.watermarks.push(state);
    }

    /// Records an explicit omission.
    pub fn record_omission(&mut self, omission: SafeOmission) {
        self.omissions.record(omission);
    }

    /// Marks currentness as unestablished.
    pub fn mark_currentness_unestablished(&mut self) {
        self.currentness_established = false;
    }

    /// Marks currentness as established by the report producer.
    ///
    /// This is an assertion by the caller, not an authorization check.
    pub fn mark_currentness_established(&mut self) {
        self.currentness_established = true;
    }

    pub fn context_version(&self) -> u64 {
        self.context_version
    }

    pub fn requirement_profile_version(&self) -> &str {
        &self.requirement_profile_version
    }

    /// Looks up coverage by its existing sufficiency dimension.
    pub fn dimension_coverage(
        &self,
        dimension: &SufficiencyDimension,
    ) -> Option<&DimensionCoverage> {
        self.dimension_coverage.get(&format!("{dimension:?}"))
    }

    /// Returns every reported partition state.
    pub fn watermarks(&self) -> &[PartitionState] {
        &self.watermarks
    }

    /// Returns the completeness of one source/partition pair.
    ///
    /// An unreported partition is Unknown, not Complete: omission is not
    /// proof that the partition contains no relevant data.
    pub fn completeness_of(&self, source: &str, partition: &str) -> PartitionCompleteness {
        self.watermarks
            .iter()
            .find(|state| {
                state.watermark.source == source && state.watermark.partition == partition
            })
            .map(|state| state.completeness.clone())
            .unwrap_or_else(|| PartitionCompleteness::Unknown {
                reason: format!("partition not reported: {source}/{partition}"),
            })
    }

    pub fn omissions(&self) -> &SafeOmissions {
        &self.omissions
    }

    /// Returns whether every reported dimension and index is complete.
    ///
    /// This is deliberately fail-closed: currentness must be established,
    /// every reported dimension must meet its required count, every reported
    /// reported partition must have an explicit Complete verdict.
    ///
    /// An empty dimension or watermark collection is not treated as evidence
    /// of complete coverage.
    pub fn is_complete(&self) -> bool {
        if !self.currentness_established
            || self.dimension_coverage.is_empty()
            || self.watermarks.is_empty()
        {
            return false;
        }

        if self.dimension_coverage.values().any(|coverage| {
            coverage.covered < coverage.required || !coverage.omitted_requirement_ids.is_empty()
        }) {
            return false;
        }

        self.watermarks
            .iter()
            .all(|state| state.completeness == PartitionCompleteness::Complete)
            && self.omissions.all().is_empty()
    }
}

// FINDING: BlockedRefs provides an API-level disclosure boundary, not a
// complete type-system security boundary. The representation cannot accurately
// accumulate hidden references after an undisclosed count has been recorded;
// it intentionally remains None.
//
// FINDING: `SufficiencyReport::is_complete()` can only assess dimensions and
// watermarks that were recorded. It cannot prove that all required dimensions
// or partitions were enumerated. A requirement-profile schema or expected
// dimension/index inventory is needed for that stronger guarantee.
//
// FINDING: Canonical commit/fence references, PermissionEpoch, compacted
// membership and validation/digest profiles are represented as data fields,
// but this model does not validate their canonicality, authorization or
// freshness. Collection and validation belong to the owning pipeline.
