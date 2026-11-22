# TASK 360 — second repair: the module duplicates a type `main` already has

`main` has moved to `550bb864`. Two things changed under you:

1. `crates/memory-context/src/budget.rs` owns `BudgetVector` (limits) and
   `BudgetUsage` (measurements). You already migrated to them in round 359.
2. `crates/memory-context/src/observability.rs` landed (commit `79c54699`,
   "feat(context): add the budget and sufficiency observability report").
   It contains `build_budget_sufficiency_report` and `summarize_delivery_lifecycle`.

That second landing changes what your module is for, and it exposes one more
duplicated type. **This round is smaller than the last one. Do not redesign.**

---

## 1. Hard constraints

**#0 — `lib.rs` may only be APPENDED to.** Never re-emit it.
**#1 — Do not duplicate a type that already exists.** Round 359 failed here once
(`BudgetVector`); this round has one more instance of the same mistake.
**#2 — No `#[ignore]`, `todo!()`, `unimplemented!()`.** The workspace is at zero.
**#3 — Report only commands you ran, with their real output and real exit codes.**
You have no access to the repository, so write `NOT RUN` and say so. That is the
correct answer and it is what you did last round. Never fabricate output.

---

## 2. The defect: `IndexWatermark` duplicates `CanonicalWatermark`

`main` already defines, at `crates/memory-context/src/lib.rs:1762`:

```rust
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CanonicalWatermark {
    pub source: String,
    pub partition: String,
    pub revision: u64,
}
```

Your module defines:

```rust
pub struct IndexWatermark {
    pub index_id: String,
    pub watermark: u64,
    pub contiguous_gap: bool,
}
```

`index_id` is `source`+`partition` flattened; `watermark` is `revision`. The only
genuinely new information is `contiguous_gap` — and §9.1 requires that gap state
be recorded *alongside* the watermark vector, not welded into each watermark.

`observability.rs` already carries `Vec<CanonicalWatermark>` and its coverage-row
text says watermarks are "carried as-is". Two watermark types in one crate means
the report and the observability projection cannot exchange a watermark without
a conversion, and a future contributor has to guess which one is canonical.

### Required change

Delete `IndexWatermark`. Carry the vector as `CanonicalWatermark` and keep gap
state in its own parallel structure, because §9.1 says a partition is Complete,
Partial or Unknown — three states, not a bool:

```rust
use crate::CanonicalWatermark;

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
```

Then:

- `SufficiencyReport.watermarks: Vec<PartitionState>` (private field, as now).
- `record_watermark(&mut self, state: PartitionState)`.
- `watermarks(&self) -> &[PartitionState]`.
- `completeness_of(&self, source: &str, partition: &str) -> PartitionCompleteness`
  — match on both fields, since `source` alone may name several partitions.
  Keep the fail-closed rule: an unreported partition returns
  `Unknown { reason }`, never `Complete`.
- `is_complete()` — a partition is acceptable only when
  `completeness == Complete`. Drop the old `contiguous_gap` scan; the enum now
  carries that fact.
- `CompletenessOutcome` is superseded by `PartitionCompleteness`. Delete the old
  name rather than keeping an alias; two names for one concept is the same
  mistake in a different costume.

---

## 3. What this module is now for, and what it must NOT claim

Read `crates/memory-context/src/observability.rs` before you answer. It already
implements:

| §9.4 requirement | `observability.rs` |
|---|---|
| exact ContextVersion + requirement-profile version | yes (`context_version`, `requirement_profile_digest`) |
| per-dimension coverage and omissions | yes (`omissions`) |
| per-partition watermark vector | yes (`watermarks`) |
| canonical commit/fence refs + PermissionEpoch | **absent** |
| budget vector (token profile, bytes, entries, relation/provenance bounds, latency/CPU) | **absent** |
| compacted source membership + validation/digest profile | **absent** |
| blocked/deferred refs without leaking existence or counts | **absent** |

So your module is not a second observability report. It is the **carrier for the
four §9.4 fields the projection does not model**, and the projection can consume
it later. Do not add a `build_*` function that re-projects anything; do not
re-run selection or assessment; do not import from `observability.rs`.

State this in the module doc comment, in one short paragraph, so the next reader
does not think two reports compete:

```rust
//! This module carries the four §9.4 fields that `observability.rs` does not
//! model: canonical commit/fence references and the PermissionEpoch decision,
//! the budget vector alongside its measured usage, compacted source membership
//! with validation/digest profiles, and blocked/deferred references. It is a
//! data carrier, not a second projection: it recomputes nothing, and
//! `observability.rs` remains the place where a report is built from engine
//! outputs. See `context-budget-and-sufficiency.md` §9.4.
```

---

## 4. Test changes

Rewrite the three watermark tests for the new shape:

1. `unreported_index_is_unknown_not_complete` — call
   `completeness_of("semantic-index", "p0")` on a report that never recorded that
   partition; assert `PartitionCompleteness::Unknown { .. }`.
2. `contiguous_gap_makes_report_incomplete` — record a `PartitionState` whose
   `completeness` is `Partial { gaps: vec!["p0".into()] }`; assert
   `!report.is_complete()`.
3. `multiple_partitions_preserve_individual_completeness` — two partitions under
   the **same** `source` with different `partition` values, one Complete and one
   Partial. Assert `completeness_of` distinguishes them. This is the test that
   proves matching on `source` alone would have been wrong.

Add one test for the new reason this module exists:

```rust
#[test]
fn the_report_carries_the_four_fields_observability_does_not_model() {
    let mut report = complete_report();
    report.canonical_commit_ref = Some("commit-abc".to_string());
    report.forget_fence_ref = Some("fence-7".to_string());
    report.permission_epoch = Some(12);
    report.budget = Some(memory_context::BudgetVector {
        tokens: Some(4096),
        ..Default::default()
    });
    report.budget_usage = Some(memory_context::BudgetUsage {
        tokens: 1024,
        ..Default::default()
    });
    report.token_estimate_profile = Some("cl100k_base".to_string());
    report.compacted_sources.push("context-v3".to_string());
    report.validation_profile = Some("fidelity-v1".to_string());
    report.digest_profile = Some("sha256".to_string());
    report.blocked.record_visible("memory:visible".to_string());
    report.blocked.record_redacted();

    assert_eq!(report.canonical_commit_ref.as_deref(), Some("commit-abc"));
    assert_eq!(report.permission_epoch, Some(12));
    assert_eq!(report.budget_usage.as_ref().map(|u| u.tokens), Some(1024));
    assert_eq!(report.token_estimate_profile.as_deref(), Some("cl100k_base"));
    assert_eq!(report.compacted_sources, vec!["context-v3".to_string()]);
    assert_eq!(report.validation_profile.as_deref(), Some("fidelity-v1"));
    assert_eq!(report.digest_profile.as_deref(), Some("sha256"));
    assert_eq!(report.blocked.visible(), ["memory:visible"]);
    assert!(report.blocked.has_redactions());
    assert_eq!(report.blocked.disclosed_count(), None);
}
```

Update `complete_report()` to record a `PartitionState` with
`completeness: PartitionCompleteness::Complete`. The other 16 tests should be
untouched — say so if one is not.

---

## 5. Deliver

Unified diff hunks for exactly two files:
`crates/memory-context/src/sufficiency_report.rs` and
`crates/memory-context/tests/sufficiency_report.rs`. `lib.rs` needs only this
appended re-export list — but do **not** emit `lib.rs`:

```rust
pub mod sufficiency_report;

pub use sufficiency_report::{
    BlockedRefs, OmissionReason, PartitionCompleteness, PartitionState, SafeOmission,
    SafeOmissions, SufficiencyReport,
};
```

Then the verification block, with `NOT RUN` and a one-line reason for each
command you cannot execute.

Acceptance I will check on my side:

| Check | Required |
|---|---|
| `cargo build -p memory-context` | zero warnings |
| `cargo clippy -p memory-context --all-targets -- -D warnings` | exit 0 |
| `sufficiency_report` tests | 21 passed, 0 failed, 0 ignored |
| `budget_vector` tests | 10 passed (unchanged) |
| `observability` tests | 10 passed (unchanged) |
| `cargo fmt --all -- --check` | exit 0 |
| `IndexWatermark` / `CompletenessOutcome` | zero occurrences in the crate |

---

## 6. Source files as they are on disk right now

See the two fenced blocks at the end of this file. They are the current contents
of the two files you are changing, unmodified.


### FILE crates/memory-context/src/sufficiency_report.rs

```rust
//! Domain model for Context sufficiency reporting.
//!
//! `SufficiencyDimension` and `ContextTier` are reused from the parent
//! `memory-context` crate to avoid introducing duplicate domain concepts.
//!
//! `CompletenessOutcome` describes the completeness of an individual
//! index/partition watermark. It is distinct from `SufficiencyOutcome`,
//! which describes the overall assessment of a ContextSnapshot.
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

use std::collections::BTreeMap;

use crate::budget::{BudgetUsage, BudgetVector};
use crate::{ContextTier, SufficiencyDimension};

/// A watermark belonging to one index or partition.
///
/// `index_id` identifies the index/partition whose watermark is represented.
/// One report contains a vector of these entries, not a global maximum.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct IndexWatermark {
    pub index_id: String,
    pub watermark: u64,
    pub contiguous_gap: bool,
}

/// Completeness of an individual index or partition.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CompletenessOutcome {
    /// The reported index has no known contiguous gaps.
    Complete,
    /// Missing or lagging data is known.
    Partial { gaps: Vec<String> },
    /// Completeness cannot currently be established.
    Unknown { reason: String },
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
    watermarks: Vec<IndexWatermark>,
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

    /// Appends one index/partition watermark.
    pub fn record_watermark(&mut self, watermark: IndexWatermark) {
        self.watermarks.push(watermark);
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

    /// Returns every reported index/partition watermark.
    pub fn watermarks(&self) -> &[IndexWatermark] {
        &self.watermarks
    }

    /// Returns the completeness of one reported index/partition.
    ///
    /// An unreported index is Unknown, not Complete: omission is not proof
    /// that the index contains no relevant data.
    pub fn completeness_of(&self, index_id: &str) -> CompletenessOutcome {
        let matching: Vec<_> = self
            .watermarks
            .iter()
            .filter(|watermark| watermark.index_id == index_id)
            .collect();

        if matching.is_empty() {
            return CompletenessOutcome::Unknown {
                reason: format!("index not reported: {index_id}"),
            };
        }

        let gaps: Vec<String> = matching
            .iter()
            .filter(|watermark| watermark.contiguous_gap)
            .map(|watermark| watermark.index_id.clone())
            .collect();

        if gaps.is_empty() {
            CompletenessOutcome::Complete
        } else {
            CompletenessOutcome::Partial { gaps }
        }
    }

    pub fn omissions(&self) -> &SafeOmissions {
        &self.omissions
    }

    /// Returns whether every reported dimension and index is complete.
    ///
    /// This is deliberately fail-closed: currentness must be established,
    /// every reported dimension must meet its required count, every reported
    /// watermark must be gap-free, and every reported index must be complete.
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

        if self
            .watermarks
            .iter()
            .any(|watermark| watermark.contiguous_gap)
        {
            return false;
        }

        self.watermarks.iter().all(|watermark| {
            matches!(
                self.completeness_of(&watermark.index_id),
                CompletenessOutcome::Complete
            )
        }) && self.omissions.all().is_empty()
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
```

### FILE crates/memory-context/tests/sufficiency_report.rs

```rust
use memory_context::{
    BlockedRefs, BudgetUsage, CompletenessOutcome, ContextTier, DimensionCoverage, IndexWatermark,
    OmissionReason, SafeOmission, SafeOmissions, SufficiencyDimension, SufficiencyReport,
};

fn complete_report() -> SufficiencyReport {
    let mut report = SufficiencyReport::new(1, "profile-v1".to_string());

    report.record_dimension_coverage(DimensionCoverage {
        dimension: SufficiencyDimension::SemanticCoverage,
        required: 2,
        covered: 2,
        omitted_requirement_ids: Vec::new(),
    });

    report.record_watermark(IndexWatermark {
        index_id: "semantic-index".to_string(),
        watermark: 42,
        contiguous_gap: false,
    });

    report.mark_currentness_established();
    report
}

fn omission(
    requirement_id: &str,
    dimension: SufficiencyDimension,
    tier: ContextTier,
) -> SafeOmission {
    SafeOmission::new(
        requirement_id.to_string(),
        dimension,
        tier,
        OmissionReason::OverBudget,
    )
}

#[test]
fn new_report_starts_incomplete() {
    let report = SufficiencyReport::new(1, "profile-v1".to_string());
    assert!(!report.is_complete());
}

#[test]
fn fully_covered_current_report_is_complete() {
    let report = complete_report();
    assert!(report.is_complete());
}

#[test]
fn dimension_with_uncovered_requirements_is_incomplete() {
    let mut report = complete_report();

    report.record_dimension_coverage(DimensionCoverage {
        dimension: SufficiencyDimension::SemanticCoverage,
        required: 3,
        covered: 2,
        omitted_requirement_ids: Vec::new(),
    });

    assert!(!report.is_complete());
}

#[test]
fn unestablished_currentness_fails_closed() {
    let mut report = complete_report();
    report.mark_currentness_unestablished();
    assert!(!report.is_complete());
}

#[test]
fn unreported_index_is_unknown_not_complete() {
    let report = complete_report();

    assert!(matches!(
        report.completeness_of("unknown-index"),
        CompletenessOutcome::Unknown { .. }
    ));
}

#[test]
fn contiguous_gap_makes_report_incomplete() {
    let mut report = complete_report();

    report.record_watermark(IndexWatermark {
        index_id: "gapped-index".to_string(),
        watermark: 41,
        contiguous_gap: true,
    });

    assert!(!report.is_complete());
}

#[test]
fn multiple_partitions_preserve_individual_completeness() {
    let mut report = complete_report();

    report.record_watermark(IndexWatermark {
        index_id: "partition-b".to_string(),
        watermark: 40,
        contiguous_gap: true,
    });

    report.record_watermark(IndexWatermark {
        index_id: "partition-c".to_string(),
        watermark: 43,
        contiguous_gap: false,
    });

    assert!(matches!(
        report.completeness_of("partition-b"),
        CompletenessOutcome::Partial { .. }
    ));
    assert_eq!(
        report.completeness_of("partition-c"),
        CompletenessOutcome::Complete
    );
    assert!(!report.is_complete());
}

#[test]
fn unmeasured_budget_does_not_imply_incompleteness() {
    let mut report = complete_report();
    report.budget = None;
    report.budget_usage = None;

    assert!(report.is_complete());
}

#[test]
fn p0_omission_is_automatically_protected() {
    let omission = omission(
        "p0-requirement",
        SufficiencyDimension::SemanticCoverage,
        ContextTier::P0,
    );

    assert!(omission.is_protected());
}

#[test]
fn risk_dimension_is_protected_even_at_p3() {
    let omission = omission(
        "risk-requirement",
        SufficiencyDimension::RiskCoverage,
        ContextTier::P3,
    );

    assert!(omission.is_protected());
}

#[test]
fn ordinary_p3_semantic_omission_is_not_protected() {
    let omission = omission(
        "semantic-requirement",
        SufficiencyDimension::SemanticCoverage,
        ContextTier::P3,
    );

    assert!(!omission.is_protected());
}

#[test]
fn protected_count_counts_only_protected_omissions() {
    let mut omissions = SafeOmissions::new();

    omissions.record(omission(
        "p0",
        SufficiencyDimension::SemanticCoverage,
        ContextTier::P0,
    ));

    omissions.record(omission(
        "risk",
        SufficiencyDimension::RiskCoverage,
        ContextTier::P3,
    ));

    omissions.record(omission(
        "ordinary",
        SufficiencyDimension::SemanticCoverage,
        ContextTier::P3,
    ));

    assert_eq!(omissions.protected_count(), 2);
}

#[test]
fn redacted_refs_hide_undisclosed_count() {
    let mut refs = BlockedRefs::new();
    refs.record_redacted();

    assert!(refs.has_redactions());
    assert_eq!(refs.disclosed_count(), None);
    assert!(refs.visible().is_empty());
}

#[test]
fn redacted_count_is_disclosed_without_exposing_identities() {
    let mut refs = BlockedRefs::new();
    refs.record_redacted_count(5);

    assert_eq!(refs.disclosed_count(), Some(5));
    assert!(refs.visible().is_empty());
}

#[test]
fn visible_refs_are_separate_from_redacted_refs() {
    let mut refs = BlockedRefs::new();
    refs.record_visible("authorized-ref".to_string());
    refs.record_redacted();

    assert_eq!(refs.visible(), &["authorized-ref".to_string()]);
    assert_eq!(refs.disclosed_count(), None);
}

#[test]
fn omitted_requirement_ids_make_dimension_incomplete() {
    let mut report = complete_report();

    report.record_dimension_coverage(DimensionCoverage {
        dimension: SufficiencyDimension::SemanticCoverage,
        required: 2,
        covered: 2,
        omitted_requirement_ids: vec!["omitted-1".to_string()],
    });

    assert!(!report.is_complete());
}

#[test]
fn explicitly_recorded_omission_makes_report_incomplete() {
    let mut report = complete_report();

    report.record_omission(omission(
        "protected-p0",
        SufficiencyDimension::SemanticCoverage,
        ContextTier::P0,
    ));

    assert_eq!(report.omissions().protected_count(), 1);
    assert!(!report.is_complete());
}

#[test]
fn report_preserves_context_and_requirement_versions() {
    let report = SufficiencyReport::new(42, "requirements-v3".to_string());

    assert_eq!(report.context_version(), 42);
    assert_eq!(report.requirement_profile_version(), "requirements-v3");
}

#[test]
fn budget_fields_distinguish_unmeasured_from_zero() {
    let usage = BudgetUsage {
        tokens: 0,
        ..BudgetUsage::default()
    };
    let mut report = complete_report();
    report.budget_usage = Some(usage);
    report.rendered_bytes = Some(0);
    report.entries = None;

    assert_eq!(report.budget_usage.as_ref().map(|u| u.tokens), Some(0));
    assert_eq!(report.rendered_bytes, Some(0));
    assert_eq!(report.entries, None);
    assert!(report.is_complete());
}

#[test]
fn report_consumes_the_crate_budget_vector() {
    use memory_context::{BudgetUsage, BudgetVector};

    let limits = BudgetVector {
        tokens: Some(100),
        ..BudgetVector::default()
    };
    let usage = BudgetUsage {
        tokens: 120,
        ..BudgetUsage::default()
    };

    let mut report = complete_report();
    report.budget = Some(limits);
    report.budget_usage = Some(usage);

    let limits = report.budget.as_ref().expect("limits recorded");
    let usage = report.budget_usage.as_ref().expect("usage recorded");
    assert_eq!(limits.violations(usage).len(), 1);

    // The report's own completeness verdict is independent of overflow:
    // §9.4 asks for the budget to be *reported*, and §9.2 keeps admission
    // constraints separate from weighted budget pressure.
    assert!(report.is_complete());
}
```
