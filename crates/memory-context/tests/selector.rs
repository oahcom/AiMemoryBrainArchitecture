use memory_context::{
    select_candidates, ContextBudget, ContextCandidate, ContextTier, HardConstraints,
    RankedCandidate, SelectionWeights, SufficiencyDimension, UncertaintyLevel,
};
use memory_domain::{MemoryLifecycle, OpaqueId, ScopeKind, ScopeRef};
use std::collections::BTreeSet;

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn candidate(name: &str) -> ContextCandidate {
    ContextCandidate {
        entry_id: id(name),
        memory_id: id(&format!("memory-{name}")),
        memory_version_id: id(&format!("version-{name}")),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: vec![ScopeRef {
            scope_id: id("scope"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:selector-test".into(),
        }],
        tier: ContextTier::P1,
        priority: 1,
        activation_reason: "selector test".into(),
        rendered_content: format!("content-{name}"),
        source_refs: vec![id(&format!("source-{name}"))],
        evidence_refs: vec![],
        epistemic_qualifiers: vec![],
        content_hash: format!("hash-{name}"),
    }
}

fn dimensions(values: &[SufficiencyDimension]) -> BTreeSet<SufficiencyDimension> {
    values.iter().cloned().collect()
}

fn ranked<'a>(
    candidate: &'a ContextCandidate,
    covers: &[SufficiencyDimension],
    fingerprint: u64,
    bytes: u64,
    uncertainty: UncertaintyLevel,
) -> RankedCandidate<'a> {
    RankedCandidate {
        candidate,
        covers: dimensions(covers),
        content_fingerprint: fingerprint,
        rendered_bytes: bytes,
        uncertainty,
    }
}

fn weights() -> SelectionWeights {
    SelectionWeights {
        marginal_coverage: 10,
        redundancy_penalty: 0,
        byte_cost_penalty_per_kib: 0,
        uncertainty_penalty: [0, 0, 0],
    }
}

fn budget(entries: usize, bytes: usize) -> ContextBudget {
    ContextBudget {
        max_entries: entries,
        max_rendered_bytes: bytes,
    }
}

fn all_constraints(_: &ContextCandidate) -> HardConstraints {
    HardConstraints {
        authorized: true,
        not_forgotten: true,
        temporally_valid: true,
        environment_matches: true,
        required_evidence_present: true,
    }
}

fn mandatory(values: &[SufficiencyDimension]) -> BTreeSet<SufficiencyDimension> {
    dimensions(values)
}

#[test]
fn hard_constraint_violation_excludes_candidate_before_ranking() {
    let forbidden = candidate("forbidden");
    let allowed = candidate("allowed");

    let candidates = vec![
        ranked(
            &forbidden,
            &[
                SufficiencyDimension::SemanticCoverage,
                SufficiencyDimension::EntityCoverage,
                SufficiencyDimension::RelationCoverage,
            ],
            1,
            1,
            UncertaintyLevel::None,
        ),
        ranked(
            &allowed,
            &[SufficiencyDimension::SemanticCoverage],
            2,
            1,
            UncertaintyLevel::None,
        ),
    ];

    let constraints = |c: &ContextCandidate| HardConstraints {
        authorized: c.entry_id != id("forbidden"),
        ..all_constraints(c)
    };

    let result = select_candidates(
        &candidates,
        &constraints,
        &weights(),
        &budget(2, 100),
        &BTreeSet::new(),
    );

    assert_eq!(result.excluded.len(), 1);
    assert_eq!(result.excluded[0].0.entry_id, id("forbidden"));
    assert_eq!(result.excluded[0].1, "authorization");
    assert_eq!(result.selected.len(), 1);
    assert_eq!(result.selected[0].entry_id, id("allowed"));
}

#[test]
fn each_hard_constraint_is_reported_by_its_own_name() {
    let candidates_owned: Vec<_> = ["auth", "forget", "temporal", "environment", "evidence"]
        .iter()
        .map(|name| candidate(name))
        .collect();

    let candidates: Vec<_> = candidates_owned
        .iter()
        .map(|c| ranked(c, &[], 0, 1, UncertaintyLevel::None))
        .collect();

    let constraints = |c: &ContextCandidate| {
        let name = &c.entry_id;
        HardConstraints {
            authorized: name != &id("auth"),
            not_forgotten: name != &id("forget"),
            temporally_valid: name != &id("temporal"),
            environment_matches: name != &id("environment"),
            required_evidence_present: name != &id("evidence"),
        }
    };

    let result = select_candidates(
        &candidates,
        &constraints,
        &weights(),
        &budget(10, 100),
        &BTreeSet::new(),
    );

    let names: Vec<_> = result.excluded.iter().map(|item| item.1).collect();

    assert_eq!(
        names,
        vec![
            "authorization",
            "forget",
            "temporal_validity",
            "environment_match",
            "required_evidence",
        ]
    );
    assert!(result.selected.is_empty());
}

#[test]
fn excluded_candidates_consume_no_budget() {
    let excluded: Vec<_> = (0..5)
        .map(|index| candidate(&format!("excluded-{index}")))
        .collect();

    let allowed = candidate("allowed");

    let mut candidates: Vec<_> = excluded
        .iter()
        .map(|c| ranked(c, &[], 1, 1000, UncertaintyLevel::None))
        .collect();

    candidates.push(ranked(
        &allowed,
        &[SufficiencyDimension::SemanticCoverage],
        2,
        5,
        UncertaintyLevel::None,
    ));

    let constraints = |c: &ContextCandidate| HardConstraints {
        authorized: c.entry_id == id("allowed"),
        ..all_constraints(c)
    };

    let result = select_candidates(
        &candidates,
        &constraints,
        &weights(),
        &budget(1, 5),
        &BTreeSet::new(),
    );

    assert_eq!(result.excluded.len(), 5);
    assert_eq!(result.selected.len(), 1);
    assert_eq!(result.selected[0].entry_id, id("allowed"));
}

#[test]
fn first_selection_scores_all_covered_dimensions() {
    let a = candidate("a");

    let candidates = vec![ranked(
        &a,
        &[
            SufficiencyDimension::SemanticCoverage,
            SufficiencyDimension::EntityCoverage,
            SufficiencyDimension::RelationCoverage,
        ],
        1,
        1,
        UncertaintyLevel::None,
    )];

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(1, 100),
        &BTreeSet::new(),
    );

    assert_eq!(result.selected.len(), 1);
    // Only one candidate is available, so the greedy selection is unambiguous.
    // All three covered dimensions contribute 10 points each.
    assert_eq!(result.marginal_scores, vec![30]);
}

#[test]
fn subsequent_selection_scores_only_new_dimensions() {
    let a = candidate("a");
    let b = candidate("b");

    let candidates = vec![
        ranked(
            &a,
            &[
                SufficiencyDimension::SemanticCoverage,
                SufficiencyDimension::EntityCoverage,
            ],
            1,
            1,
            UncertaintyLevel::None,
        ),
        ranked(
            &b,
            &[
                SufficiencyDimension::SemanticCoverage,
                SufficiencyDimension::TemporalValidity,
            ],
            2,
            1,
            UncertaintyLevel::None,
        ),
    ];

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(2, 100),
        &BTreeSet::new(),
    );

    // Both candidates initially score 20. Input order breaks the tie, selecting a.
    // After a is selected, b contributes only its previously uncovered
    // TemporalValidity dimension, worth 10 points.
    assert_eq!(result.selected.len(), 2);
    assert_eq!(result.marginal_scores, vec![20, 10]);
    assert_eq!(result.selected[0].entry_id, id("a"));
    assert_eq!(result.selected[1].entry_id, id("b"));
}

#[test]
fn redundancy_is_penalized() {
    let a = candidate("a");
    let b = candidate("b");

    let candidates = vec![
        ranked(
            &a,
            &[SufficiencyDimension::SemanticCoverage],
            42,
            1,
            UncertaintyLevel::None,
        ),
        ranked(
            &b,
            &[SufficiencyDimension::EntityCoverage],
            42,
            1,
            UncertaintyLevel::None,
        ),
    ];

    let mut w = weights();
    w.redundancy_penalty = 3;

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &w,
        &budget(2, 100),
        &BTreeSet::new(),
    );

    assert_eq!(result.marginal_scores, vec![10, 7]);
}

#[test]
fn byte_cost_is_penalized_per_kib() {
    let a = candidate("a");

    let candidates = vec![ranked(
        &a,
        &[
            SufficiencyDimension::SemanticCoverage,
            SufficiencyDimension::EntityCoverage,
        ],
        1,
        2048,
        UncertaintyLevel::None,
    )];

    let mut w = weights();
    w.byte_cost_penalty_per_kib = 4;

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &w,
        &budget(1, 4096),
        &BTreeSet::new(),
    );

    // 2 KiB * 4 penalty = 8; coverage = 20.
    assert_eq!(result.marginal_scores, vec![12]);
}

#[test]
fn uncertainty_is_penalized_by_level() {
    let levels = [
        UncertaintyLevel::None,
        UncertaintyLevel::Low,
        UncertaintyLevel::Medium,
        UncertaintyLevel::High,
    ];

    let mut w = weights();
    w.uncertainty_penalty = [1, 2, 3];

    let mut scores = Vec::new();

    for (index, level) in levels.into_iter().enumerate() {
        let c = candidate(&format!("uncertainty-{index}"));

        let candidates = vec![ranked(
            &c,
            &[SufficiencyDimension::SemanticCoverage],
            index as u64,
            1,
            level,
        )];

        let result = select_candidates(
            &candidates,
            &all_constraints,
            &w,
            &budget(1, 100),
            &BTreeSet::new(),
        );

        scores.push(result.marginal_scores[0]);
    }

    assert_eq!(scores, vec![10, 9, 8, 7]);
}

#[test]
fn selection_stops_when_best_marginal_score_is_not_positive() {
    let a = candidate("a");
    let b = candidate("b");

    let candidates = vec![
        ranked(
            &a,
            &[SufficiencyDimension::SemanticCoverage],
            1,
            1,
            UncertaintyLevel::None,
        ),
        ranked(
            &b,
            &[SufficiencyDimension::SemanticCoverage],
            2,
            1,
            UncertaintyLevel::None,
        ),
    ];

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(10, 100),
        &BTreeSet::new(),
    );

    assert_eq!(result.selected.len(), 1);
    assert_eq!(result.selected[0].entry_id, id("a"));
    assert_eq!(result.marginal_scores, vec![10]);
}

#[test]
fn candidate_exceeding_budget_is_skipped_but_smaller_one_is_tried() {
    let large = candidate("large");
    let small = candidate("small");

    let candidates = vec![
        ranked(
            &large,
            &[
                SufficiencyDimension::SemanticCoverage,
                SufficiencyDimension::EntityCoverage,
            ],
            1,
            100,
            UncertaintyLevel::None,
        ),
        ranked(
            &small,
            &[SufficiencyDimension::SemanticCoverage],
            2,
            5,
            UncertaintyLevel::None,
        ),
    ];

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(2, 10),
        &BTreeSet::new(),
    );

    assert_eq!(result.selected.len(), 1);
    assert_eq!(result.selected[0].entry_id, id("small"));
    assert_eq!(result.marginal_scores, vec![10]);
}

#[test]
fn uncovered_mandatory_lists_missing_dimensions_in_order() {
    let a = candidate("a");

    let candidates = vec![ranked(
        &a,
        &[SufficiencyDimension::EntityCoverage],
        1,
        1,
        UncertaintyLevel::None,
    )];

    let required = mandatory(&[
        SufficiencyDimension::TemporalValidity,
        SufficiencyDimension::EvidenceCoverage,
        SufficiencyDimension::SemanticCoverage,
        SufficiencyDimension::EntityCoverage,
    ]);

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(2, 100),
        &required,
    );

    assert_eq!(
        result.uncovered_mandatory,
        vec![
            SufficiencyDimension::SemanticCoverage,
            SufficiencyDimension::TemporalValidity,
            SufficiencyDimension::EvidenceCoverage,
        ]
    );
}

#[test]
fn selection_is_deterministic_across_repeated_calls() {
    let owned: Vec<_> = (0..5)
        .map(|index| candidate(&format!("candidate-{index}")))
        .collect();

    let candidates: Vec<_> = owned
        .iter()
        .enumerate()
        .map(|(index, c)| {
            ranked(
                c,
                &[
                    SufficiencyDimension::SemanticCoverage,
                    SufficiencyDimension::EntityCoverage,
                ],
                index as u64,
                1,
                UncertaintyLevel::None,
            )
        })
        .collect();

    let required = BTreeSet::new();

    let first = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(3, 100),
        &required,
    );

    let expected: Vec<_> = first.selected.iter().map(|c| c.entry_id.clone()).collect();

    for _ in 0..5 {
        let result = select_candidates(
            &candidates,
            &all_constraints,
            &weights(),
            &budget(3, 100),
            &required,
        );

        let actual: Vec<_> = result.selected.iter().map(|c| c.entry_id.clone()).collect();

        assert_eq!(actual, expected);
        assert_eq!(result.marginal_scores, first.marginal_scores);
    }
}

#[test]
fn all_mandatory_covered_yields_empty_uncovered_list() {
    let a = candidate("a");

    let required = mandatory(&[
        SufficiencyDimension::SemanticCoverage,
        SufficiencyDimension::EntityCoverage,
    ]);

    let candidates = vec![ranked(
        &a,
        &[
            SufficiencyDimension::SemanticCoverage,
            SufficiencyDimension::EntityCoverage,
        ],
        1,
        1,
        UncertaintyLevel::None,
    )];

    let result = select_candidates(
        &candidates,
        &all_constraints,
        &weights(),
        &budget(2, 100),
        &required,
    );

    assert!(result.uncovered_mandatory.is_empty());
    assert_eq!(result.selected.len(), 1);
}
