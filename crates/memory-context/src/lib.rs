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
    /// Serialize the staged snapshot as JSON. Serialization does not publish it.
    pub fn serialize(&self) -> Result<String, ContextError> {
        serde_json::to_string(self).map_err(|error| ContextError::Serialization(error.to_string()))
    }
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

    #[test]
    fn build_sorts_by_tier_then_priority_then_entry_id() {
        let snapshot = build_context(
            identity(),
            7,
            budget(),
            vec![
                candidate("z", ContextTier::P1, 10, "one"),
                candidate("b", ContextTier::P0, 1, "two"),
                candidate("a", ContextTier::P1, 10, "three"),
            ],
        )
        .unwrap();

        let ids: Vec<_> = snapshot
            .entries
            .iter()
            .map(|entry| entry.entry_id.as_str())
            .collect();
        assert_eq!(ids, vec!["b", "a", "z"]);
    }

    #[test]
    fn rejects_cross_scope_candidates() {
        let mut candidate = candidate("a", ContextTier::P0, 1, "private");
        candidate.scope_refs[0].namespace_key = "user:other".into();
        assert_eq!(
            build_context(identity(), 1, budget(), vec![candidate]).unwrap_err(),
            ContextError::ScopeMismatch
        );
    }

    #[test]
    fn rejects_forgotten_and_superseded_lifecycle() {
        let mut candidate = candidate("a", ContextTier::P0, 1, "private");
        candidate.memory_lifecycle = MemoryLifecycle::Forgotten;
        assert_eq!(
            build_context(identity(), 1, budget(), vec![candidate]).unwrap_err(),
            ContextError::IneligibleLifecycle
        );
    }

    #[test]
    fn rejects_duplicate_membership_and_entry_ids() {
        let mut first = candidate("a", ContextTier::P0, 1, "one");
        let mut duplicate = first.clone();
        duplicate.entry_id = id("b");
        assert_eq!(
            build_context(identity(), 1, budget(), vec![first.clone(), duplicate]).unwrap_err(),
            ContextError::DuplicateMembership
        );

        first.memory_id = id("other-memory");
        let duplicate_id = first.clone();
        assert_eq!(
            build_context(identity(), 1, budget(), vec![first, duplicate_id]).unwrap_err(),
            ContextError::DuplicateEntry
        );
    }

    #[test]
    fn enforces_entry_and_byte_budgets_without_truncation() {
        let entry_limited = ContextBudget {
            max_entries: 1,
            max_rendered_bytes: 100,
        };
        assert!(matches!(
            build_context(
                identity(),
                1,
                entry_limited,
                vec![
                    candidate("a", ContextTier::P0, 1, "a"),
                    candidate("b", ContextTier::P1, 1, "b"),
                ],
            ),
            Err(ContextError::EntryBudgetExceeded { .. })
        ));

        let byte_limited = ContextBudget {
            max_entries: 2,
            max_rendered_bytes: 3,
        };
        assert!(matches!(
            build_context(
                identity(),
                1,
                byte_limited,
                vec![candidate("a", ContextTier::P0, 1, "four")]
            ),
            Err(ContextError::ByteBudgetExceeded { .. })
        ));
    }

    #[test]
    fn serializes_snapshot_and_prepares_non_sendable_delivery_intent() {
        let snapshot = build_context(
            identity(),
            3,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "memory text")],
        )
        .unwrap();
        let json = snapshot.serialize().unwrap();
        assert!(json.contains("\"context_version\":3"));
        let intent = prepare_delivery_intent(id("delivery-1"), &snapshot).unwrap();
        assert_eq!(
            intent.visibility,
            DeliveryVisibility::PrivatePendingPublicationGate
        );
        assert_eq!(intent.target_context_version, 3);
        assert!(intent.snapshot_json.contains("memory text"));
    }

    #[test]
    fn rejects_missing_lineage_and_empty_content() {
        let mut no_lineage = candidate("a", ContextTier::P0, 1, "text");
        no_lineage.source_refs.clear();
        assert_eq!(
            build_context(identity(), 1, budget(), vec![no_lineage]).unwrap_err(),
            ContextError::MissingLineage
        );

        let empty = candidate("b", ContextTier::P0, 1, " ");
        assert_eq!(
            build_context(identity(), 1, budget(), vec![empty]).unwrap_err(),
            ContextError::EmptyField("rendered_content")
        );
    }
}
