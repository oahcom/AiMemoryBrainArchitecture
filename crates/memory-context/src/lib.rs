//! Brain-owned, scoped Memory Context planning primitives.
//!
//! This crate deliberately stops before persistence and transport. A built
//! snapshot is a private staged artifact until the D producer/dependency
//! registration, I authorization and D final publication gate have succeeded.
//! Delivery intents created here are therefore non-sendable by construction.

use memory_domain::{scope_set_contains_all, DomainError, MemoryLifecycle, OpaqueId, ScopeRef};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextBudget {
    pub max_entries: usize,
    pub max_rendered_bytes: usize,
}

impl ContextBudget {
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.max_entries == 0 || self.max_rendered_bytes == 0 {
            return Err(ContextError::InvalidBudget);
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextIdentity {
    pub context_id: OpaqueId,
    pub scope_refs: Vec<ScopeRef>,
    pub agent_id: OpaqueId,
    pub agent_instance_id: OpaqueId,
    pub session_id: OpaqueId,
    pub task_id: Option<OpaqueId>,
    pub environment_id: Option<OpaqueId>,
    pub purpose: String,
    pub schema_version: String,
}

impl ContextIdentity {
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.scope_refs.is_empty() {
            return Err(ContextError::Domain(DomainError::EmptyRequiredField(
                "scope_refs",
            )));
        }
        for scope in &self.scope_refs {
            scope.validate().map_err(ContextError::Domain)?;
        }
        if self.purpose.trim().is_empty() {
            return Err(ContextError::EmptyField("purpose"));
        }
        if self.schema_version.trim().is_empty() {
            return Err(ContextError::EmptyField("schema_version"));
        }
        Ok(())
    }
}

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd, Serialize, Deserialize)]
pub enum ContextTier {
    P0,
    P1,
    P2,
    P3,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextCandidate {
    pub entry_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub memory_lifecycle: MemoryLifecycle,
    pub scope_refs: Vec<ScopeRef>,
    pub tier: ContextTier,
    pub priority: i32,
    pub activation_reason: String,
    pub rendered_content: String,
    pub source_refs: Vec<OpaqueId>,
    pub evidence_refs: Vec<OpaqueId>,
    pub epistemic_qualifiers: Vec<String>,
    pub content_hash: String,
}

impl ContextCandidate {
    fn validate_for(&self, identity: &ContextIdentity) -> Result<(), ContextError> {
        if self.memory_lifecycle != MemoryLifecycle::Active
            && self.memory_lifecycle != MemoryLifecycle::Consolidated
        {
            return Err(ContextError::IneligibleLifecycle);
        }
        if self.scope_refs.is_empty()
            || !scope_set_contains_all(&self.scope_refs, &identity.scope_refs)
        {
            return Err(ContextError::ScopeMismatch);
        }
        for scope in &self.scope_refs {
            scope.validate().map_err(ContextError::Domain)?;
        }
        if self.activation_reason.trim().is_empty() {
            return Err(ContextError::EmptyField("activation_reason"));
        }
        if self.rendered_content.trim().is_empty() {
            return Err(ContextError::EmptyField("rendered_content"));
        }
        if self.content_hash.trim().is_empty() {
            return Err(ContextError::EmptyField("content_hash"));
        }
        if self.source_refs.is_empty() {
            return Err(ContextError::MissingLineage);
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextEntry {
    pub entry_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub tier: ContextTier,
    pub priority: i32,
    pub activation_reason: String,
    pub rendered_content: String,
    pub source_refs: Vec<OpaqueId>,
    pub evidence_refs: Vec<OpaqueId>,
    pub epistemic_qualifiers: Vec<String>,
    pub content_hash: String,
    pub rendered_bytes: usize,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextSnapshot {
    pub identity: ContextIdentity,
    pub context_version: u64,
    pub entries: Vec<ContextEntry>,
    pub rendered_bytes: usize,
}

impl ContextSnapshot {
    /// Number of entries currently held by this snapshot.
    pub fn total_entries(&self) -> usize {
        self.entries.len()
    }

    /// Whether this snapshot contains no entries.
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    /// Serialize the staged snapshot as JSON. Serialization does not publish it.
    pub fn serialize(&self) -> Result<String, ContextError> {
        serde_json::to_string(self).map_err(|error| ContextError::Serialization(error.to_string()))
    }
}

/// Validates invariants that can be checked without the original build budget.
pub fn validate_snapshot(snapshot: &ContextSnapshot) -> Result<(), ContextError> {
    let Some(actual) = snapshot.entries.iter().try_fold(0usize, |total, entry| {
        total.checked_add(entry.rendered_bytes)
    }) else {
        return Err(ContextError::SnapshotByteCountMismatch {
            actual: usize::MAX,
            recorded: snapshot.rendered_bytes,
        });
    };
    if actual != snapshot.rendered_bytes {
        return Err(ContextError::SnapshotByteCountMismatch {
            actual,
            recorded: snapshot.rendered_bytes,
        });
    }
    if snapshot
        .entries
        .iter()
        .any(|entry| entry.rendered_content.trim().is_empty())
    {
        return Err(ContextError::EmptyField("rendered_content"));
    }
    Ok(())
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum DeliveryVisibility {
    PrivatePendingPublicationGate,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct DeliveryIntent {
    pub delivery_id: OpaqueId,
    pub context_id: OpaqueId,
    pub target_context_version: u64,
    pub snapshot_json: String,
    pub visibility: DeliveryVisibility,
}

/// Builds a deterministic private snapshot from candidates already returned by
/// an authorized canonical-memory read path. This function does not itself
/// authenticate, authorize, query D/I, or publish.
pub fn build_context(
    identity: ContextIdentity,
    context_version: u64,
    budget: ContextBudget,
    mut candidates: Vec<ContextCandidate>,
) -> Result<ContextSnapshot, ContextError> {
    identity.validate()?;
    budget.validate()?;
    if context_version == 0 {
        return Err(ContextError::InvalidVersion);
    }

    let mut seen_entries = HashSet::new();
    let mut seen_memberships = HashSet::new();
    for candidate in &candidates {
        candidate.validate_for(&identity)?;
        if !seen_entries.insert(candidate.entry_id.clone()) {
            return Err(ContextError::DuplicateEntry);
        }
        let membership = (
            candidate.memory_id.clone(),
            candidate.memory_version_id.clone(),
        );
        if !seen_memberships.insert(membership) {
            return Err(ContextError::DuplicateMembership);
        }
    }

    // Stable, deterministic ordering: tier, descending priority, then entry ID.
    candidates.sort_by(|left, right| {
        left.tier
            .cmp(&right.tier)
            .then_with(|| right.priority.cmp(&left.priority))
            .then_with(|| left.entry_id.cmp(&right.entry_id))
    });

    if candidates.len() > budget.max_entries {
        return Err(ContextError::EntryBudgetExceeded {
            actual: candidates.len(),
            limit: budget.max_entries,
        });
    }

    let mut rendered_bytes = 0usize;
    let mut entries = Vec::with_capacity(candidates.len());
    for candidate in candidates {
        let bytes = candidate.rendered_content.len();
        rendered_bytes =
            rendered_bytes
                .checked_add(bytes)
                .ok_or(ContextError::ByteBudgetExceeded {
                    actual: usize::MAX,
                    limit: budget.max_rendered_bytes,
                })?;
        if rendered_bytes > budget.max_rendered_bytes {
            return Err(ContextError::ByteBudgetExceeded {
                actual: rendered_bytes,
                limit: budget.max_rendered_bytes,
            });
        }
        entries.push(ContextEntry {
            entry_id: candidate.entry_id,
            memory_id: candidate.memory_id,
            memory_version_id: candidate.memory_version_id,
            tier: candidate.tier,
            priority: candidate.priority,
            activation_reason: candidate.activation_reason,
            rendered_content: candidate.rendered_content,
            source_refs: candidate.source_refs,
            evidence_refs: candidate.evidence_refs,
            epistemic_qualifiers: candidate.epistemic_qualifiers,
            content_hash: candidate.content_hash,
            rendered_bytes: bytes,
        });
    }

    // The byte total is accumulated from the same entry lengths above. Keep
    // this as a debug invariant: it detects internal drift without adding a
    // new runtime failure mode to this pure constructor.
    debug_assert_eq!(
        entries
            .iter()
            .map(|entry| entry.rendered_bytes)
            .sum::<usize>(),
        rendered_bytes
    );

    Ok(ContextSnapshot {
        identity,
        context_version,
        entries,
        rendered_bytes,
    })
}

/// Creates a private delivery intent. It is not a send authorization and cannot
/// transition to a sendable state without the external owner-controlled gate.
pub fn prepare_delivery_intent(
    delivery_id: OpaqueId,
    snapshot: &ContextSnapshot,
) -> Result<DeliveryIntent, ContextError> {
    Ok(DeliveryIntent {
        delivery_id,
        context_id: snapshot.identity.context_id.clone(),
        target_context_version: snapshot.context_version,
        snapshot_json: snapshot.serialize()?,
        visibility: DeliveryVisibility::PrivatePendingPublicationGate,
    })
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ContextError {
    Domain(DomainError),
    EmptyField(&'static str),
    InvalidBudget,
    InvalidVersion,
    IneligibleLifecycle,
    ScopeMismatch,
    MissingLineage,
    DuplicateEntry,
    DuplicateMembership,
    EntryBudgetExceeded { actual: usize, limit: usize },
    ByteBudgetExceeded { actual: usize, limit: usize },
    Serialization(String),
    SnapshotByteCountMismatch { actual: usize, recorded: usize },
}

impl std::fmt::Display for ContextError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for ContextError {}

#[cfg(test)]
mod tests {
    use super::*;
    use memory_domain::ScopeKind;

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

    fn candidate(entry: &str, tier: ContextTier, priority: i32, content: &str) -> ContextCandidate {
        ContextCandidate {
            entry_id: id(entry),
            memory_id: id(&format!("memory-{entry}")),
            memory_version_id: id(&format!("version-{entry}")),
            memory_lifecycle: MemoryLifecycle::Active,
            scope_refs: vec![scope()],
            tier,
            priority,
            activation_reason: "direct task relevance".into(),
            rendered_content: content.into(),
            source_refs: vec![id(&format!("source-{entry}"))],
            evidence_refs: vec![],
            epistemic_qualifiers: vec!["reported".into()],
            content_hash: format!("sha256:{entry}"),
        }
    }

    fn budget() -> ContextBudget {
        ContextBudget {
            max_entries: 8,
            max_rendered_bytes: 1024,
        }
    }

    fn ordered_ids(candidates: Vec<ContextCandidate>) -> Vec<String> {
        build_context(identity(), 1, budget(), candidates)
            .unwrap()
            .entries
            .iter()
            .map(|entry| entry.entry_id.as_str().to_owned())
            .collect()
    }

    // A1 — identical candidate batches produce identical ordered entries.
    #[test]
    fn build_context_order_is_deterministic_across_repeated_calls() {
        let candidates = vec![
            candidate("z", ContextTier::P1, 10, "one"),
            candidate("b", ContextTier::P0, 1, "two"),
            candidate("a", ContextTier::P1, 10, "three"),
        ];
        let first = build_context(identity(), 7, budget(), candidates.clone()).unwrap();
        let second = build_context(identity(), 7, budget(), candidates).unwrap();
        assert_eq!(first.entries, second.entries);
    }

    // A2 — each sort key is independently verified: tier, priority, entry ID.
    #[test]
    fn sorting_uses_tier_then_descending_priority_then_entry_id() {
        assert_eq!(
            ordered_ids(vec![
                candidate("z-tier", ContextTier::P1, 5, "a"),
                candidate("a-tier", ContextTier::P0, 5, "b"),
                candidate("m-tier", ContextTier::P2, 5, "c"),
            ]),
            vec!["a-tier", "z-tier", "m-tier"]
        );
        assert_eq!(
            ordered_ids(vec![
                candidate("a-priority", ContextTier::P1, 1, "a"),
                candidate("z-priority", ContextTier::P1, 9, "b"),
                candidate("m-priority", ContextTier::P1, 5, "c"),
            ]),
            vec!["z-priority", "m-priority", "a-priority"]
        );
        assert_eq!(
            ordered_ids(vec![
                candidate("z-entry", ContextTier::P1, 5, "a"),
                candidate("a-entry", ContextTier::P1, 5, "b"),
                candidate("m-entry", ContextTier::P1, 5, "c"),
            ]),
            vec!["a-entry", "m-entry", "z-entry"]
        );
    }

    // A3 — entry overflow reports the actual candidate count.
    #[test]
    fn entry_budget_error_reports_actual_candidate_count() {
        let result = build_context(
            identity(),
            1,
            ContextBudget {
                max_entries: 2,
                max_rendered_bytes: 100,
            },
            vec![
                candidate("a", ContextTier::P0, 1, "a"),
                candidate("b", ContextTier::P1, 1, "b"),
                candidate("c", ContextTier::P2, 1, "c"),
            ],
        );
        assert_eq!(
            result.unwrap_err(),
            ContextError::EntryBudgetExceeded {
                actual: 3,
                limit: 2
            }
        );
    }

    // A4 — byte overflow reports the real accumulated byte count.
    #[test]
    fn byte_budget_error_reports_accumulated_rendered_bytes() {
        let result = build_context(
            identity(),
            1,
            ContextBudget {
                max_entries: 3,
                max_rendered_bytes: 4,
            },
            vec![
                candidate("a", ContextTier::P0, 1, "ab"),
                candidate("b", ContextTier::P1, 1, "cde"),
            ],
        );
        assert_eq!(
            result.unwrap_err(),
            ContextError::ByteBudgetExceeded {
                actual: 5,
                limit: 4
            }
        );
    }

    // A5 — both budget limits accept exact equality.
    #[test]
    fn exact_entry_and_byte_budget_boundaries_succeed() {
        let snapshot = build_context(
            identity(),
            1,
            ContextBudget {
                max_entries: 2,
                max_rendered_bytes: 3,
            },
            vec![
                candidate("a", ContextTier::P0, 1, "a"),
                candidate("b", ContextTier::P1, 1, "bc"),
            ],
        )
        .unwrap();
        assert_eq!(snapshot.entries.len(), 2);
        assert_eq!(snapshot.rendered_bytes, 3);
    }

    // A6 — duplicate entry IDs are rejected even for different memories.
    #[test]
    fn duplicate_entry_ids_are_rejected() {
        let first = candidate("same", ContextTier::P0, 1, "one");
        let mut second = candidate("other", ContextTier::P1, 1, "two");
        second.entry_id = id("same");
        assert_eq!(
            build_context(identity(), 1, budget(), vec![first, second]).unwrap_err(),
            ContextError::DuplicateEntry
        );
    }

    // A7 — one memory/version membership cannot appear under two entry IDs.
    #[test]
    fn duplicate_memory_version_membership_is_rejected() {
        let first = candidate("a", ContextTier::P0, 1, "one");
        let mut second = first.clone();
        second.entry_id = id("b");
        assert_eq!(
            build_context(identity(), 1, budget(), vec![first, second]).unwrap_err(),
            ContextError::DuplicateMembership
        );
    }

    // A8 — every lifecycle other than Active and Consolidated is ineligible.
    #[test]
    fn non_active_non_consolidated_lifecycles_are_rejected() {
        for lifecycle in [
            MemoryLifecycle::Candidate,
            MemoryLifecycle::Superseded,
            MemoryLifecycle::Archived,
            MemoryLifecycle::Forgotten,
        ] {
            let mut item = candidate("a", ContextTier::P0, 1, "text");
            item.memory_lifecycle = lifecycle;
            assert_eq!(
                build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
                ContextError::IneligibleLifecycle
            );
        }
    }

    // A9 — candidates outside the identity scope are rejected.
    #[test]
    fn candidate_scope_must_be_contained_by_identity_scope() {
        let mut item = candidate("a", ContextTier::P0, 1, "private");
        item.scope_refs[0].namespace_key = "user:other".into();
        assert_eq!(
            build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
            ContextError::ScopeMismatch
        );
    }

    // A10 — empty identity scope, purpose, and schema version each fail validation.
    #[test]
    fn empty_identity_scope_purpose_and_schema_version_are_rejected() {
        let mut empty_scope = identity();
        empty_scope.scope_refs.clear();
        assert_eq!(
            build_context(empty_scope, 1, budget(), vec![]).unwrap_err(),
            ContextError::Domain(DomainError::EmptyRequiredField("scope_refs"))
        );

        let mut empty_purpose = identity();
        empty_purpose.purpose.clear();
        assert_eq!(
            build_context(empty_purpose, 1, budget(), vec![]).unwrap_err(),
            ContextError::EmptyField("purpose")
        );

        let mut empty_schema = identity();
        empty_schema.schema_version.clear();
        assert_eq!(
            build_context(empty_schema, 1, budget(), vec![]).unwrap_err(),
            ContextError::EmptyField("schema_version")
        );
    }

    // A11 — context version zero is invalid.
    #[test]
    fn zero_context_version_is_rejected() {
        assert_eq!(
            build_context(identity(), 0, budget(), vec![]).unwrap_err(),
            ContextError::InvalidVersion
        );
    }

    // A12 — either zero-valued budget field invalidates the budget.
    #[test]
    fn zero_entry_or_byte_budget_is_rejected() {
        for invalid_budget in [
            ContextBudget {
                max_entries: 0,
                max_rendered_bytes: 1,
            },
            ContextBudget {
                max_entries: 1,
                max_rendered_bytes: 0,
            },
        ] {
            assert_eq!(
                build_context(identity(), 1, invalid_budget, vec![]).unwrap_err(),
                ContextError::InvalidBudget
            );
        }
    }

    // A13 — delivery intent visibility is private and has no sendable variant.
    #[test]
    fn delivery_intent_visibility_is_always_private_pending_gate() {
        let snapshot = build_context(
            identity(),
            3,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "memory text")],
        )
        .unwrap();
        let intent = prepare_delivery_intent(id("delivery-1"), &snapshot).unwrap();
        assert_eq!(
            intent.visibility,
            DeliveryVisibility::PrivatePendingPublicationGate
        );
    }

    // A14 — delivery intent targets exactly the snapshot context version.
    #[test]
    fn delivery_intent_targets_snapshot_context_version() {
        let snapshot = build_context(identity(), 42, budget(), vec![]).unwrap();
        let intent = prepare_delivery_intent(id("delivery-1"), &snapshot).unwrap();
        assert_eq!(intent.target_context_version, snapshot.context_version);
    }

    // A15 — serialized delivery snapshot round-trips to an equivalent structure.
    #[test]
    fn delivery_intent_snapshot_json_round_trips_to_equivalent_snapshot() {
        let snapshot = build_context(
            identity(),
            3,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "memory text")],
        )
        .unwrap();
        let intent = prepare_delivery_intent(id("delivery-1"), &snapshot).unwrap();
        let decoded: ContextSnapshot = serde_json::from_str(&intent.snapshot_json).unwrap();
        assert_eq!(decoded, snapshot);
    }

    // B1 — snapshot entry-count and emptiness accessors reflect the entries.
    #[test]
    fn snapshot_accessors_report_entry_count_and_emptiness() {
        let empty = build_context(identity(), 1, budget(), vec![]).unwrap();
        assert_eq!(empty.total_entries(), 0);
        assert!(empty.is_empty());

        let populated = build_context(
            identity(),
            1,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "text")],
        )
        .unwrap();
        assert_eq!(populated.total_entries(), 1);
        assert!(!populated.is_empty());
    }

    // B2 — constructor output keeps the sum of entry byte counts self-consistent.
    #[test]
    fn build_context_rendered_byte_total_matches_entry_sum() {
        let snapshot = build_context(
            identity(),
            1,
            budget(),
            vec![
                candidate("a", ContextTier::P0, 1, "one"),
                candidate("b", ContextTier::P1, 1, "two!"),
            ],
        )
        .unwrap();
        assert_eq!(
            snapshot
                .entries
                .iter()
                .map(|entry| entry.rendered_bytes)
                .sum::<usize>(),
            snapshot.rendered_bytes
        );
    }

    // B3 — deserialized snapshots can be checked for byte totals and empty content.
    #[test]
    fn validate_snapshot_rejects_inconsistent_bytes_and_empty_entry_content() {
        let snapshot = build_context(
            identity(),
            1,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "text")],
        )
        .unwrap();

        let mut wrong_total = snapshot.clone();
        wrong_total.rendered_bytes += 1;
        assert_eq!(
            validate_snapshot(&wrong_total),
            Err(ContextError::SnapshotByteCountMismatch {
                actual: 4,
                recorded: 5
            })
        );

        let mut empty_content = snapshot;
        empty_content.entries[0].rendered_content.clear();
        assert_eq!(
            validate_snapshot(&empty_content),
            Err(ContextError::EmptyField("rendered_content"))
        );
    }
}

[executed on device: VM-0-9-ubuntu (d03d92fd-4b5d-4bc1-a701-985eb5de69cc)]