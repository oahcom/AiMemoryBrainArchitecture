use memory_context::{
    BlockedRefs, BudgetUsage, ContextTier, DimensionCoverage, OmissionReason,
    PartitionCompleteness, PartitionState, SafeOmission, SafeOmissions, SufficiencyDimension,
    SufficiencyReport,
};

fn complete_report() -> SufficiencyReport {
    let mut report = SufficiencyReport::new(1, "profile-v1".to_string());

    report.record_dimension_coverage(DimensionCoverage {
        dimension: SufficiencyDimension::SemanticCoverage,
        required: 2,
        covered: 2,
        omitted_requirement_ids: Vec::new(),
    });

    report.record_watermark(PartitionState {
        watermark: memory_context::CanonicalWatermark {
            source: "semantic-index".to_string(),
            partition: "p0".to_string(),
            revision: 42,
        },
        completeness: PartitionCompleteness::Complete,
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
        report.completeness_of("semantic-index", "unknown-partition"),
        PartitionCompleteness::Unknown { .. }
    ));
}

#[test]
fn contiguous_gap_makes_report_incomplete() {
    let mut report = complete_report();

    report.record_watermark(PartitionState {
        watermark: memory_context::CanonicalWatermark {
            source: "gapped-index".to_string(),
            partition: "p0".to_string(),
            revision: 41,
        },
        completeness: PartitionCompleteness::Partial {
            gaps: vec!["p0".into()],
        },
    });

    assert!(!report.is_complete());
}

#[test]
fn multiple_partitions_preserve_individual_completeness() {
    let mut report = complete_report();

    report.record_watermark(PartitionState {
        watermark: memory_context::CanonicalWatermark {
            source: "shared-index".to_string(),
            partition: "p1".to_string(),
            revision: 40,
        },
        completeness: PartitionCompleteness::Partial {
            gaps: vec!["p1".into()],
        },
    });

    report.record_watermark(PartitionState {
        watermark: memory_context::CanonicalWatermark {
            source: "shared-index".to_string(),
            partition: "p2".to_string(),
            revision: 43,
        },
        completeness: PartitionCompleteness::Complete,
    });

    assert!(matches!(
        report.completeness_of("shared-index", "p1"),
        PartitionCompleteness::Partial { .. }
    ));
    assert_eq!(
        report.completeness_of("shared-index", "p2"),
        PartitionCompleteness::Complete
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

#[test]
fn the_domain_report_preserves_the_four_section_9_4_field_groups() {
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
    assert_eq!(
        report.token_estimate_profile.as_deref(),
        Some("cl100k_base")
    );
    assert_eq!(report.compacted_sources, vec!["context-v3".to_string()]);
    assert_eq!(report.validation_profile.as_deref(), Some("fidelity-v1"));
    assert_eq!(report.digest_profile.as_deref(), Some("sha256"));
    assert_eq!(report.blocked.visible(), ["memory:visible"]);
    assert!(report.blocked.has_redactions());
    assert_eq!(report.blocked.disclosed_count(), None);
}
