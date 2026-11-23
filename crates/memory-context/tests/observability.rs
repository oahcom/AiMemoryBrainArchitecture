//! Property tests for the observability report projections.

use memory_context::{
    build_budget_sufficiency_report, summarize_delivery_lifecycle, BudgetSufficiencyReport,
    BudgetUsage, BudgetVector, CanonicalWatermark, ContextBudget, ContextCandidate, ContextTier,
    DeliveryAck, DeliveryAttempt, DeliveryAttemptId, DeliveryId, DeliveryLifecycle,
    SelectionBudgetUsage, SufficiencyAssessment, SufficiencyDimension, SufficiencyOutcome,
    SufficiencyOutcomeKind, SufficiencyReport, SufficiencyRequirement,
};
use memory_domain::{MemoryLifecycle, OpaqueId, ScopeKind, ScopeRef};

const SECRET: &str = "SECRET-MEMORY-CONTENT-do-not-leak";

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn candidate(name: &str, content: &str) -> ContextCandidate {
    ContextCandidate {
        entry_id: id(name),
        memory_id: id(&format!("memory-{name}")),
        memory_version_id: id(&format!("version-{name}")),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: vec![ScopeRef {
            scope_id: id("scope"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:obs-test".into(),
        }],
        tier: ContextTier::P1,
        priority: 1,
        activation_reason: "observability test".into(),
        rendered_content: content.into(),
        source_refs: vec![id(&format!("source-{name}"))],
        evidence_refs: vec![],
        epistemic_qualifiers: vec![],
        content_hash: format!("hash-{name}"),
    }
}

fn budget() -> ContextBudget {
    ContextBudget {
        max_entries: 8,
        max_rendered_bytes: 4096,
    }
}

fn usage() -> SelectionBudgetUsage {
    SelectionBudgetUsage {
        entries: 2,
        rendered_bytes: 40,
    }
}

fn requirement(dimension: SufficiencyDimension, mandatory: bool) -> SufficiencyRequirement {
    SufficiencyRequirement {
        requirement_id: format!("{SECRET}-requirement"),
        dimension,
        threshold: 3,
        mandatory,
    }
}

fn sufficiency() -> SufficiencyReport {
    let mut report = SufficiencyReport::new(7, format!("profile-{SECRET}"));
    report.mark_currentness_established();
    report
}

fn report_with_sufficiency(
    sufficiency: &SufficiencyReport,
    excluded: &[(&ContextCandidate, &'static str)],
    assessment: &SufficiencyAssessment,
) -> BudgetSufficiencyReport {
    build_budget_sufficiency_report(
        sufficiency,
        &budget(),
        &usage(),
        excluded,
        assessment,
        &[CanonicalWatermark {
            source: "canonical".into(),
            partition: "p0".into(),
            revision: 11,
        }],
    )
}

fn report(
    excluded: &[(&ContextCandidate, &'static str)],
    assessment: &SufficiencyAssessment,
) -> BudgetSufficiencyReport {
    report_with_sufficiency(&sufficiency(), excluded, assessment)
}

fn sufficient() -> SufficiencyAssessment {
    SufficiencyAssessment {
        outcome: SufficiencyOutcome::Sufficient,
        evaluated_requirements: 2,
    }
}

#[test]
fn exclusion_counts_sum_to_the_number_of_excluded_candidates() {
    let denied = candidate("denied", "a");
    let forgotten = candidate("forgotten", "b");
    let stale = candidate("stale", "c");

    let excluded = vec![
        (&denied, "authorization"),
        (&forgotten, "forget"),
        (&stale, "authorization"),
    ];

    let report = report(&excluded, &sufficient());

    assert_eq!(report.excluded_total, 3);
    assert_eq!(
        report.exclusions.iter().map(|e| e.count).sum::<usize>(),
        report.excluded_total,
        "no candidate may be double-counted or silently dropped"
    );
}

#[test]
fn each_distinct_unmet_constraint_is_its_own_key_with_its_own_count() {
    let denied_a = candidate("denied-a", "a");
    let denied_b = candidate("denied-b", "b");
    let stale = candidate("stale", "c");

    let excluded = vec![
        (&denied_a, "authorization"),
        (&denied_b, "authorization"),
        (&stale, "temporal_validity"),
    ];

    let report = report(&excluded, &sufficient());

    assert_eq!(report.exclusions.len(), 2);
    assert_eq!(report.exclusions[0].constraint, "authorization");
    assert_eq!(report.exclusions[0].count, 2);
    assert_eq!(report.exclusions[1].constraint, "temporal_validity");
    assert_eq!(report.exclusions[1].count, 1);
}

#[test]
fn an_all_admitted_run_reports_zero_exclusions_and_no_omissions() {
    let report = report(&[], &sufficient());

    assert_eq!(report.excluded_total, 0);
    assert!(report.exclusions.is_empty(), "empty is not an error");
    assert!(report.omissions.is_empty());
    assert_eq!(report.outcome, SufficiencyOutcomeKind::Sufficient);
}

#[test]
fn the_report_carries_no_memory_content_requirement_ids_or_unknown_dimension_names() {
    let excluded_candidate = candidate("leaky", SECRET);
    let excluded = vec![(&excluded_candidate, "authorization")];
    let assessment = SufficiencyAssessment {
        outcome: SufficiencyOutcome::Insufficient {
            unmet_mandatory: vec![
                requirement(SufficiencyDimension::SemanticCoverage, true),
                requirement(SufficiencyDimension::Unknown(SECRET.into()), true),
            ],
        },
        evaluated_requirements: 2,
    };

    let report = report(&excluded, &assessment);
    let debug = format!("{report:?}");

    assert!(!debug.contains(SECRET), "report leaked raw data: {debug}");
    assert!(!debug.contains("leaky"), "report leaked a candidate id");
    assert_eq!(report.omissions.len(), 2);
    assert_eq!(report.omissions[0].dimension, "semantic_coverage");
    assert_eq!(report.omissions[1].dimension, "unknown_dimension");
    assert!(report.requirement_profile_digest.starts_with("sha256:"));
    assert!(!report.requirement_profile_digest.contains(SECRET));
}

#[test]
fn the_report_is_identical_across_two_runs_over_the_same_inputs() {
    let denied = candidate("denied", "a");
    let forgotten = candidate("forgotten", "b");
    let stale = candidate("stale", "c");
    let excluded = vec![
        (&stale, "temporal_validity"),
        (&denied, "authorization"),
        (&forgotten, "forget"),
        (&denied, "authorization"),
    ];
    let assessment = SufficiencyAssessment {
        outcome: SufficiencyOutcome::Conditional {
            unmet_advisory: vec![
                requirement(SufficiencyDimension::RiskCoverage, false),
                requirement(SufficiencyDimension::EvidenceCoverage, false),
                requirement(SufficiencyDimension::RiskCoverage, false),
            ],
        },
        evaluated_requirements: 3,
    };

    let first = report(&excluded, &assessment);
    let second = report(&excluded, &assessment);

    assert_eq!(first, second);
    assert_eq!(
        format!("{first:?}"),
        format!("{second:?}"),
        "debug ordering must be stable too"
    );
}

#[test]
fn advisory_omissions_are_labelled_conditional_and_counted_per_dimension() {
    let assessment = SufficiencyAssessment {
        outcome: SufficiencyOutcome::Conditional {
            unmet_advisory: vec![
                requirement(SufficiencyDimension::RiskCoverage, false),
                requirement(SufficiencyDimension::RiskCoverage, false),
                requirement(SufficiencyDimension::UncertaintyCoverage, false),
            ],
        },
        evaluated_requirements: 3,
    };

    let report = report(&[], &assessment);

    assert_eq!(report.outcome, SufficiencyOutcomeKind::Conditional);
    assert_eq!(report.omissions.len(), 2);
    assert_eq!(report.omissions[0].dimension, "risk_coverage");
    assert_eq!(report.omissions[0].count, 2);
    assert!(report.omissions.iter().all(|o| !o.mandatory));
}

#[test]
fn budget_utilization_reports_used_and_limit_per_measured_dimension() {
    let report = report(&[], &sufficient());

    assert_eq!(report.utilization.entries_used, 2);
    assert_eq!(report.utilization.entries_limit, 8);
    assert_eq!(report.utilization.rendered_bytes_used, 40);
    assert_eq!(report.utilization.rendered_bytes_limit, 4096);
    assert_eq!(report.context_version, 7);
    assert_eq!(report.watermarks.len(), 1);
    assert_eq!(report.watermarks[0].revision, 11);
}

// ---- delivery lifecycle observability (context-manager.md §7, §9) ----

fn delivery(name: &str) -> DeliveryId {
    DeliveryId::new(name).unwrap()
}

fn attempt(name: &str) -> DeliveryAttempt {
    DeliveryAttempt::first(
        delivery(name),
        DeliveryAttemptId::new(format!("a-{name}")).unwrap(),
    )
}

#[test]
fn delivery_states_are_tallied_on_separate_axes_and_never_folded_together() {
    // max_attempts is high on purpose: `record_attempt` only appends to the
    // ledger and abandons on exhaustion — it does not reach `Delivered`. This
    // test is about tallying the five states separately, so each state is
    // reached through its own real transition.
    let mut lifecycle = DeliveryLifecycle::new(8).unwrap();

    let pending = delivery("pending");
    let delivered = delivery("delivered");
    let acknowledged = delivery("acknowledged");

    lifecycle.enqueue(pending.clone()).unwrap();

    lifecycle.enqueue(delivered.clone()).unwrap();
    lifecycle.record_attempt(attempt("delivered")).unwrap();
    lifecycle.mark_delivered(&delivered).unwrap();

    lifecycle.enqueue(acknowledged.clone()).unwrap();
    lifecycle.record_attempt(attempt("acknowledged")).unwrap();
    lifecycle.mark_delivered(&acknowledged).unwrap();
    lifecycle
        .consume_ack(&DeliveryAck::new(
            acknowledged.clone(),
            DeliveryAttemptId::new("a-acknowledged").unwrap(),
        ))
        .unwrap();

    let report = summarize_delivery_lifecycle(
        &lifecycle,
        &[pending, delivered, acknowledged.clone(), acknowledged],
    );

    assert_eq!(report.pending, 1);
    assert_eq!(report.delivered, 1);
    assert_eq!(report.acknowledged, 1, "a repeated observation counts once");
    assert_eq!(report.superseded, 0);
    assert_eq!(report.abandoned, 0);
    assert_eq!(report.unknown_deliveries, 0);
}

#[test]
fn an_observed_delivery_without_a_record_is_reported_unknown_not_guessed() {
    let lifecycle = DeliveryLifecycle::new(2).unwrap();

    let report = summarize_delivery_lifecycle(&lifecycle, &[delivery("never-enqueued")]);

    assert_eq!(report.unknown_deliveries, 1);
    assert_eq!(
        report.pending
            + report.delivered
            + report.acknowledged
            + report.superseded
            + report.abandoned,
        0,
        "unknown must not be folded into a known state"
    );
}

#[test]
fn the_delivery_report_carries_counts_only_and_no_delivery_identifiers() {
    let mut lifecycle = DeliveryLifecycle::new(2).unwrap();
    let secret_delivery = delivery(SECRET);
    lifecycle.enqueue(secret_delivery.clone()).unwrap();

    let report = summarize_delivery_lifecycle(&lifecycle, &[secret_delivery]);
    let debug = format!("{report:?}");

    assert_eq!(report.pending, 1);
    assert!(
        !debug.contains(SECRET),
        "report leaked a delivery id: {debug}"
    );
}

#[test]
fn the_report_carries_all_four_section_9_4_field_groups() {
    let mut sufficiency = sufficiency();
    sufficiency.canonical_commit_ref = Some("commit-abc".into());
    sufficiency.forget_fence_ref = Some("fence-7".into());
    sufficiency.permission_epoch = Some(12);
    sufficiency.budget = Some(BudgetVector {
        tokens: Some(4096),
        relation_fan_out: Some(32),
        provenance_depth: Some(8),
        latency_micros: Some(1000),
        cpu_micros: Some(500),
        tier_entries: vec![(ContextTier::P1, 4)],
    });
    sufficiency.budget_usage = Some(BudgetUsage {
        tokens: 1024,
        relation_fan_out: 8,
        provenance_depth: 3,
        latency_micros: 200,
        cpu_micros: 100,
        tier_entries: vec![(ContextTier::P1, 2)],
    });
    sufficiency.token_estimate_profile = Some("cl100k_base".into());
    sufficiency.rendered_bytes = Some(2048);
    sufficiency.entries = Some(4);
    sufficiency.compacted_sources = vec!["context-v3".into(), "context-v4".into()];
    sufficiency.validation_profile = Some("fidelity-v1".into());
    sufficiency.digest_profile = Some("sha256".into());
    sufficiency.blocked.record_visible("memory:visible".into());
    sufficiency.blocked.record_redacted();
    sufficiency.deferred.record_visible("source:visible".into());
    sufficiency.deferred.record_redacted();

    let report = report_with_sufficiency(&sufficiency, &[], &sufficient());

    assert_eq!(report.canonical_commit_ref.as_deref(), Some("commit-abc"));
    assert_eq!(report.forget_fence_ref.as_deref(), Some("fence-7"));
    assert_eq!(report.permission_epoch, Some(12));
    assert_eq!(report.budget.as_ref().unwrap().tokens, Some(4096));
    assert_eq!(report.budget_usage.as_ref().unwrap().tokens, 1024);
    assert_eq!(
        report.token_estimate_profile.as_deref(),
        Some("cl100k_base")
    );
    assert_eq!(report.rendered_bytes, Some(2048));
    assert_eq!(report.entries, Some(4));
    assert_eq!(
        report.compacted_sources,
        vec!["context-v3".to_string(), "context-v4".to_string()]
    );
    assert_eq!(report.validation_profile.as_deref(), Some("fidelity-v1"));
    assert_eq!(report.digest_profile.as_deref(), Some("sha256"));
    assert_eq!(report.blocked.visible(), ["memory:visible"]);
    assert_eq!(report.deferred.visible(), ["source:visible"]);
    assert!(report.blocked.has_redactions());
    assert!(report.deferred.has_redactions());
    assert!(report.sufficiency_currentness_established);
}

#[test]
fn blocked_and_deferred_never_disclose_unauthorized_counts() {
    let mut sufficiency = sufficiency();
    sufficiency
        .blocked
        .record_visible("authorized-blocked".into());
    sufficiency.blocked.record_redacted();
    sufficiency
        .deferred
        .record_visible("authorized-deferred".into());
    sufficiency.deferred.record_redacted();

    let report = report_with_sufficiency(&sufficiency, &[], &sufficient());

    assert_eq!(report.blocked.visible(), ["authorized-blocked"]);
    assert_eq!(report.deferred.visible(), ["authorized-deferred"]);
    assert_eq!(report.blocked.disclosed_count(), None);
    assert_eq!(report.deferred.disclosed_count(), None);
    assert!(report.blocked.has_redactions());
    assert!(report.deferred.has_redactions());

    // The type has no total-count accessor to leak through; the only count it
    // can report is the disclosed one, and that stays None above.
    let debug = format!("{report:?}");
    assert!(!debug.contains(SECRET));
}

#[test]
fn budget_usage_none_is_distinct_from_measured_zero() {
    let mut unmeasured = sufficiency();
    unmeasured.budget_usage = None;
    let unmeasured_report = report_with_sufficiency(&unmeasured, &[], &sufficient());

    let mut measured_zero = sufficiency();
    measured_zero.budget_usage = Some(BudgetUsage::default());
    let zero_report = report_with_sufficiency(&measured_zero, &[], &sufficient());

    assert_eq!(unmeasured_report.budget_usage, None);
    assert_eq!(zero_report.budget_usage, Some(BudgetUsage::default()));
    assert_ne!(
        unmeasured_report.budget_usage, zero_report.budget_usage,
        "not measured must not collapse into measured zero"
    );
}

#[test]
fn unestablished_currentness_is_not_reported_as_established_absence() {
    let sufficiency = SufficiencyReport::new(7, format!("profile-{SECRET}"));

    let report = report_with_sufficiency(&sufficiency, &[], &sufficient());

    assert!(!report.sufficiency_currentness_established);
    assert!(report.compacted_sources.is_empty());
    assert_eq!(report.budget_usage, None);
}
