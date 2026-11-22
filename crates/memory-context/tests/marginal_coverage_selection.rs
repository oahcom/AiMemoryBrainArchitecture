use memory_context::{
    select_within_budget, ContextBudget, ContextCandidate, ContextIdentity, ContextTier,
    SelectionDropReason,
};
use memory_domain::{MemoryLifecycle, OpaqueId, ScopeKind, ScopeRef};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn scope() -> ScopeRef {
    ScopeRef {
        scope_id: id("scope-user-1"),
        scope_kind: ScopeKind::User,
        namespace_key: "user:1".into(),
    }
}

fn identity() -> ContextIdentity {
    ContextIdentity {
        context_id: id("ctx-1"),
        scope_refs: vec![scope()],
        agent_id: id("agent-1"),
        agent_instance_id: id("agent-instance-1"),
        session_id: id("session-1"),
        task_id: Some(id("task-1")),
        environment_id: None,
        purpose: "task-working-context".into(),
        schema_version: "1".into(),
    }
}

fn candidate(entry: &str, tier: ContextTier, sources: &[&str], content: &str) -> ContextCandidate {
    ContextCandidate {
        entry_id: id(entry),
        memory_id: id(&format!("memory-{entry}")),
        memory_version_id: id(&format!("version-{entry}")),
        memory_lifecycle: MemoryLifecycle::Active,
        scope_refs: vec![scope()],
        tier,
        priority: 10,
        activation_reason: "direct task relevance".into(),
        rendered_content: content.into(),
        source_refs: sources.iter().map(|source| id(source)).collect(),
        evidence_refs: vec![],
        epistemic_qualifiers: vec!["reported".into()],
        content_hash: format!("sha256:{entry}"),
    }
}

fn budget(entries: usize, bytes: usize) -> ContextBudget {
    ContextBudget {
        max_entries: entries,
        max_rendered_bytes: bytes,
    }
}

fn selected_ids(outcome: &memory_context::SelectionOutcome) -> Vec<String> {
    outcome
        .selected
        .iter()
        .map(|candidate| candidate.entry_id.as_str().to_owned())
        .collect()
}

fn dropped_reason(outcome: &memory_context::SelectionOutcome, entry: &str) -> SelectionDropReason {
    outcome
        .dropped
        .iter()
        .find(|dropped| dropped.candidate.entry_id.as_str() == entry)
        .unwrap()
        .reason
}

#[test]
fn empty_candidates_produce_empty_selection() {
    let outcome = select_within_budget(&identity(), &budget(4, 128), vec![]).unwrap();

    assert!(outcome.selected.is_empty());
    assert!(outcome.dropped.is_empty());

    assert_eq!(outcome.coverage.total_units, 0);
    assert_eq!(outcome.coverage.covered_units, 0);
    assert_eq!(outcome.coverage.uncovered_units, 0);

    assert_eq!(outcome.budget_usage.entries, 0);
    assert_eq!(outcome.budget_usage.rendered_bytes, 0);
}

#[test]
fn all_candidates_fit_and_have_deterministic_selection_order() {
    let candidates = vec![
        candidate("z-entry", ContextTier::P1, &["source-z"], "z"),
        candidate("b-entry", ContextTier::P0, &["source-b"], "bb"),
        candidate("a-entry", ContextTier::P0, &["source-a"], "aaa"),
    ];

    let outcome = select_within_budget(&identity(), &budget(8, 128), candidates).unwrap();

    // P0 is processed before P1.
    assert_eq!(
        selected_ids(&outcome),
        vec!["a-entry", "b-entry", "z-entry"]
    );

    assert!(outcome.dropped.is_empty());
    assert_eq!(outcome.budget_usage.entries, 3);
    assert_eq!(outcome.budget_usage.rendered_bytes, 6);
    assert_eq!(outcome.coverage.covered_units, 3);
    assert_eq!(outcome.coverage.uncovered_units, 0);
}

#[test]
fn half_entry_budget_selects_highest_marginal_coverage() {
    let candidates = vec![
        candidate("small", ContextTier::P0, &["s1"], "s"),
        candidate("large", ContextTier::P0, &["l1", "l2", "l3"], "l"),
        candidate("medium", ContextTier::P0, &["m1", "m2"], "m"),
        candidate(
            "lower-tier",
            ContextTier::P1,
            &["p1", "p2", "p3", "p4"],
            "p",
        ),
    ];

    let outcome = select_within_budget(&identity(), &budget(2, 128), candidates).unwrap();

    // P0 is a hard group. P1 cannot displace P0 even with more coverage.
    assert_eq!(selected_ids(&outcome), vec!["large", "medium"]);

    assert_eq!(
        dropped_reason(&outcome, "small"),
        SelectionDropReason::BudgetInsufficient
    );

    assert_eq!(
        dropped_reason(&outcome, "lower-tier"),
        SelectionDropReason::BudgetInsufficient
    );

    assert_eq!(outcome.budget_usage.entries, 2);
    assert_eq!(outcome.coverage.total_units, 10);
    assert_eq!(outcome.coverage.covered_units, 5);
    assert_eq!(outcome.coverage.uncovered_units, 5);
}

#[test]
fn serialization_is_identical_after_input_permutation() {
    let first = vec![
        candidate("c", ContextTier::P0, &["s1", "s2"], "ccc"),
        candidate("a", ContextTier::P0, &["s1"], "a"),
        candidate("b", ContextTier::P0, &["s3", "s4"], "bb"),
        candidate("d", ContextTier::P1, &["s5"], "dddd"),
    ];

    let second = vec![
        candidate("d", ContextTier::P1, &["s5"], "dddd"),
        candidate("b", ContextTier::P0, &["s3", "s4"], "bb"),
        candidate("a", ContextTier::P0, &["s1"], "a"),
        candidate("c", ContextTier::P0, &["s1", "s2"], "ccc"),
    ];

    let first_outcome = select_within_budget(&identity(), &budget(3, 128), first).unwrap();

    let second_outcome = select_within_budget(&identity(), &budget(3, 128), second).unwrap();

    let first_bytes = serde_json::to_vec(&first_outcome).unwrap();
    let second_bytes = serde_json::to_vec(&second_outcome).unwrap();

    assert_eq!(first_bytes, second_bytes);
}

#[test]
fn zero_marginal_gain_candidate_is_dropped() {
    let candidates = vec![
        candidate(
            "a-primary",
            ContextTier::P0,
            &["shared-source", "unique-source"],
            "primary",
        ),
        candidate(
            "b-duplicate",
            ContextTier::P0,
            &["shared-source"],
            "duplicate",
        ),
    ];

    let outcome = select_within_budget(&identity(), &budget(8, 128), candidates).unwrap();

    assert_eq!(selected_ids(&outcome), vec!["a-primary"]);

    assert_eq!(
        dropped_reason(&outcome, "b-duplicate"),
        SelectionDropReason::ZeroMarginalGain
    );

    assert_eq!(outcome.coverage.total_units, 2);
    assert_eq!(outcome.coverage.covered_units, 2);
}

#[test]
fn equal_marginal_gain_uses_entry_id_not_input_order() {
    let first = vec![
        candidate("z-entry", ContextTier::P0, &["source-z"], "z"),
        candidate("a-entry", ContextTier::P0, &["source-a"], "a"),
    ];

    let second = vec![
        candidate("a-entry", ContextTier::P0, &["source-a"], "a"),
        candidate("z-entry", ContextTier::P0, &["source-z"], "z"),
    ];

    let first_outcome = select_within_budget(&identity(), &budget(1, 128), first).unwrap();

    let second_outcome = select_within_budget(&identity(), &budget(1, 128), second).unwrap();

    assert_eq!(selected_ids(&first_outcome), vec!["a-entry"]);

    assert_eq!(selected_ids(&second_outcome), vec!["a-entry"]);

    assert_eq!(
        serde_json::to_vec(&first_outcome).unwrap(),
        serde_json::to_vec(&second_outcome).unwrap()
    );
}

#[test]
fn higher_tier_cannot_be_displaced_by_lower_tier() {
    let candidates = vec![
        candidate("p0", ContextTier::P0, &["source-p0"], "mandatory"),
        candidate(
            "p1",
            ContextTier::P1,
            &["s1", "s2", "s3", "s4", "s5"],
            "advisory",
        ),
    ];

    let outcome = select_within_budget(&identity(), &budget(1, 128), candidates).unwrap();

    assert_eq!(selected_ids(&outcome), vec!["p0"]);

    assert_eq!(
        dropped_reason(&outcome, "p1"),
        SelectionDropReason::BudgetInsufficient
    );
}

#[test]
fn byte_budget_rejection_does_not_prevent_smaller_candidate() {
    let candidates = vec![
        candidate(
            "large",
            ContextTier::P0,
            &["large-source-1", "large-source-2"],
            "this candidate is too large",
        ),
        candidate("small", ContextTier::P0, &["small-source"], "ok"),
    ];

    let outcome = select_within_budget(&identity(), &budget(4, 2), candidates).unwrap();

    assert_eq!(selected_ids(&outcome), vec!["small"]);

    assert_eq!(
        dropped_reason(&outcome, "large"),
        SelectionDropReason::BudgetInsufficient
    );

    assert_eq!(outcome.budget_usage.rendered_bytes, 2);
}
