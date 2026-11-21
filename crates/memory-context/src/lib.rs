//! Brain-owned, scoped Memory Context planning primitives.
//!
//! This crate deliberately stops before persistence and transport.
//! Snapshots and change sets remain private staged artifacts until the
//! external authorization and publication gates have succeeded.

use memory_domain::{
    scope_set_contains_all, ActorRef, DomainError, MemoryLifecycle, OpaqueId, ScopeRef,
    TemporalRef, TimeValue,
};
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};

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

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum TombstoneKind {
    Removed,
    Replaced,
    Expired,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextTombstone {
    pub entry_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub operation_id: String,
    pub reason: String,
    pub kind: TombstoneKind,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ContextOperationKind {
    Update,
    Remove,
    Replace,
    Reorder,
    Expire,
    Reconcile,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextOperationRecord {
    pub operation_id: String,
    pub kind: ContextOperationKind,
    pub reason: String,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextSnapshot {
    pub identity: ContextIdentity,
    pub context_version: u64,
    pub entries: Vec<ContextEntry>,
    #[serde(default)]
    pub tombstones: Vec<ContextTombstone>,
    #[serde(default)]
    pub operation_records: Vec<ContextOperationRecord>,
    pub rendered_bytes: usize,
}

impl ContextSnapshot {
    pub fn total_entries(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn serialize(&self) -> Result<String, ContextError> {
        serde_json::to_string(self).map_err(|error| ContextError::Serialization(error.to_string()))
    }
}

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

/// A pure in-memory edit envelope. The source snapshot is never mutated.
#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ChangeSet {
    pub base_version: u64,
    pub operations: Vec<ChangeSetOperation>,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ChangeSetOperation {
    Update {
        operation_id: String,
        entry_id: OpaqueId,
        updated: ContextEntry,
        reason: String,
    },
    Remove {
        operation_id: String,
        entry_id: OpaqueId,
        reason: String,
    },
    Replace {
        operation_id: String,
        old_entry_id: Option<OpaqueId>,
        replacement: ContextEntry,
        reason: String,
    },
    Reorder {
        operation_id: String,
        entry_ids: Vec<OpaqueId>,
        reason: String,
    },
    Expire {
        operation_id: String,
        entry_id: OpaqueId,
        expires_at_context_version: u64,
        reason: String,
    },
    Reconcile {
        operation_id: String,
        desired_entries: Vec<ContextEntry>,
        reason: String,
    },
}

impl ChangeSetOperation {
    fn operation_id(&self) -> &str {
        match self {
            Self::Update { operation_id, .. }
            | Self::Remove { operation_id, .. }
            | Self::Replace { operation_id, .. }
            | Self::Reorder { operation_id, .. }
            | Self::Expire { operation_id, .. }
            | Self::Reconcile { operation_id, .. } => operation_id,
        }
    }
}

impl ChangeSet {
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.base_version == 0 || self.operations.is_empty() {
            return Err(ContextError::InvalidOperation);
        }
        let mut ids = HashSet::new();
        for operation in &self.operations {
            let id = operation.operation_id();
            if id.trim().is_empty() {
                return Err(ContextError::InvalidOperationId);
            }
            if !ids.insert(id) {
                return Err(ContextError::DuplicateOperationId);
            }
            match operation {
                ChangeSetOperation::Update {
                    updated, reason, ..
                }
                | ChangeSetOperation::Replace {
                    replacement: updated,
                    reason,
                    ..
                } => {
                    validate_edit_entry(updated)?;
                    if reason.trim().is_empty() {
                        return Err(ContextError::EmptyField("reason"));
                    }
                }
                ChangeSetOperation::Remove { reason, .. }
                | ChangeSetOperation::Expire { reason, .. }
                | ChangeSetOperation::Reconcile { reason, .. } => {
                    if reason.trim().is_empty() {
                        return Err(ContextError::EmptyField("reason"));
                    }
                }
                ChangeSetOperation::Reorder {
                    entry_ids, reason, ..
                } => {
                    if reason.trim().is_empty() {
                        return Err(ContextError::EmptyField("reason"));
                    }
                    if entry_ids.is_empty() {
                        return Err(ContextError::InvalidReorder);
                    }
                }
            }
            if let ChangeSetOperation::Expire {
                expires_at_context_version,
                ..
            } = operation
            {
                if *expires_at_context_version == 0 {
                    return Err(ContextError::InvalidVersion);
                }
            }
            if let ChangeSetOperation::Reconcile {
                desired_entries, ..
            } = operation
            {
                let mut desired_ids = HashSet::new();
                for entry in desired_entries {
                    validate_edit_entry(entry)?;
                    if !desired_ids.insert(entry.entry_id.clone()) {
                        return Err(ContextError::DuplicateEntry);
                    }
                }
            }
        }
        Ok(())
    }
}

fn validate_edit_entry(entry: &ContextEntry) -> Result<(), ContextError> {
    if entry.rendered_content.trim().is_empty() {
        return Err(ContextError::EmptyField("rendered_content"));
    }
    if entry.content_hash.trim().is_empty() {
        return Err(ContextError::EmptyField("content_hash"));
    }
    if entry.source_refs.is_empty() {
        return Err(ContextError::MissingLineage);
    }
    if entry.rendered_bytes != entry.rendered_content.len() {
        return Err(ContextError::EntryByteCountMismatch {
            actual: entry.rendered_content.len(),
            recorded: entry.rendered_bytes,
        });
    }
    Ok(())
}

/// Applies all operations against the declared base version. A failure drops
/// the staged clone and leaves the borrowed input snapshot untouched.
pub fn apply_change_set(
    snapshot: &ContextSnapshot,
    change_set: &ChangeSet,
    budget: &ContextBudget,
) -> Result<ContextSnapshot, ContextError> {
    if snapshot.context_version != change_set.base_version {
        return Err(ContextError::StaleBase {
            expected: change_set.base_version,
            actual: snapshot.context_version,
        });
    }
    change_set.validate()?;
    budget.validate()?;
    validate_snapshot(snapshot)?;
    let target_version = snapshot
        .context_version
        .checked_add(1)
        .ok_or(ContextError::SequenceOverflow)?;
    let mut staged = snapshot.clone();
    for operation in &change_set.operations {
        apply_change_operation(&mut staged, operation, target_version)?;
    }
    if staged.entries.len() > budget.max_entries {
        return Err(ContextError::EntryBudgetExceeded {
            actual: staged.entries.len(),
            limit: budget.max_entries,
        });
    }
    let rendered_bytes = staged
        .entries
        .iter()
        .try_fold(0usize, |sum, entry| sum.checked_add(entry.rendered_bytes))
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
    staged.context_version = target_version;
    staged.rendered_bytes = rendered_bytes;
    validate_snapshot(&staged)?;
    Ok(staged)
}

fn append_tombstone(
    snapshot: &mut ContextSnapshot,
    entry: &ContextEntry,
    operation_id: &str,
    reason: &str,
    kind: TombstoneKind,
) {
    snapshot.tombstones.push(ContextTombstone {
        entry_id: entry.entry_id.clone(),
        memory_id: entry.memory_id.clone(),
        memory_version_id: entry.memory_version_id.clone(),
        operation_id: operation_id.to_owned(),
        reason: reason.to_owned(),
        kind,
    });
}

fn apply_change_operation(
    snapshot: &mut ContextSnapshot,
    operation: &ChangeSetOperation,
    target_version: u64,
) -> Result<(), ContextError> {
    match operation {
        ChangeSetOperation::Update {
            entry_id, updated, ..
        } => {
            let Some(index) = snapshot
                .entries
                .iter()
                .position(|entry| &entry.entry_id == entry_id)
            else {
                return Err(ContextError::MissingEntry);
            };
            let current = &snapshot.entries[index];
            if updated.entry_id != current.entry_id
                || updated.memory_id != current.memory_id
                || updated.memory_version_id != current.memory_version_id
            {
                return Err(ContextError::ImmutableMemoryVersion);
            }
            snapshot.entries[index] = updated.clone();
        }
        ChangeSetOperation::Remove {
            operation_id,
            entry_id,
            reason,
        } => {
            let Some(index) = snapshot
                .entries
                .iter()
                .position(|entry| &entry.entry_id == entry_id)
            else {
                return Err(ContextError::MissingEntry);
            };
            let removed = snapshot.entries.remove(index);
            append_tombstone(
                snapshot,
                &removed,
                operation_id,
                reason,
                TombstoneKind::Removed,
            );
        }
        ChangeSetOperation::Replace {
            operation_id,
            old_entry_id,
            replacement,
            reason,
        } => {
            let position = match old_entry_id {
                Some(old_id) => {
                    let Some(index) = snapshot
                        .entries
                        .iter()
                        .position(|entry| &entry.entry_id == old_id)
                    else {
                        return Err(ContextError::MissingEntry);
                    };
                    Some(index)
                }
                None => None,
            };
            if snapshot.entries.iter().enumerate().any(|(index, entry)| {
                entry.entry_id == replacement.entry_id && Some(index) != position
            }) {
                return Err(ContextError::DuplicateEntry);
            }
            if !snapshot
                .entries
                .iter()
                .any(|entry| entry.entry_id == replacement.entry_id)
                && snapshot
                    .tombstones
                    .iter()
                    .any(|tombstone| tombstone.entry_id == replacement.entry_id)
            {
                return Err(ContextError::TombstonedEntry);
            }
            if let Some(index) = position {
                let old = snapshot.entries.remove(index);
                append_tombstone(
                    snapshot,
                    &old,
                    operation_id,
                    reason,
                    TombstoneKind::Replaced,
                );
                snapshot.entries.insert(index, replacement.clone());
            } else {
                snapshot.entries.push(replacement.clone());
            }
        }
        ChangeSetOperation::Reorder { entry_ids, .. } => {
            let current: HashSet<_> = snapshot
                .entries
                .iter()
                .map(|entry| entry.entry_id.clone())
                .collect();
            let requested: HashSet<_> = entry_ids.iter().cloned().collect();
            if entry_ids.len() != snapshot.entries.len()
                || requested.len() != entry_ids.len()
                || current != requested
            {
                return Err(ContextError::InvalidReorder);
            }
            let mut reordered = Vec::with_capacity(snapshot.entries.len());
            for id in entry_ids {
                let Some(index) = snapshot
                    .entries
                    .iter()
                    .position(|entry| &entry.entry_id == id)
                else {
                    return Err(ContextError::InvalidReorder);
                };
                reordered.push(snapshot.entries[index].clone());
            }
            snapshot.entries = reordered;
        }
        ChangeSetOperation::Expire {
            operation_id,
            entry_id,
            expires_at_context_version,
            reason,
        } => {
            if *expires_at_context_version > target_version {
                return Err(ContextError::ExpirationNotDue {
                    expires_at: *expires_at_context_version,
                    target_version,
                });
            }
            let Some(index) = snapshot
                .entries
                .iter()
                .position(|entry| &entry.entry_id == entry_id)
            else {
                return Err(ContextError::MissingEntry);
            };
            let expired = snapshot.entries.remove(index);
            append_tombstone(
                snapshot,
                &expired,
                operation_id,
                reason,
                TombstoneKind::Expired,
            );
        }
        ChangeSetOperation::Reconcile {
            operation_id,
            desired_entries,
            reason,
        } => {
            let expanded = reconcile_operations(snapshot, desired_entries, operation_id, reason)?;
            for child in &expanded {
                apply_change_operation(snapshot, child, target_version)?;
            }
        }
    }
    let (kind, reason) = match operation {
        ChangeSetOperation::Update { reason, .. } => (ContextOperationKind::Update, reason),
        ChangeSetOperation::Remove { reason, .. } => (ContextOperationKind::Remove, reason),
        ChangeSetOperation::Replace { reason, .. } => (ContextOperationKind::Replace, reason),
        ChangeSetOperation::Reorder { reason, .. } => (ContextOperationKind::Reorder, reason),
        ChangeSetOperation::Expire { reason, .. } => (ContextOperationKind::Expire, reason),
        ChangeSetOperation::Reconcile { reason, .. } => (ContextOperationKind::Reconcile, reason),
    };
    snapshot.operation_records.push(ContextOperationRecord {
        operation_id: operation.operation_id().to_owned(),
        kind,
        reason: reason.to_owned(),
    });
    Ok(())
}

/// Reconcile is compiled into Update, Remove, Replace and Reorder operations.
/// A tombstoned identity cannot silently re-enter the active membership set.
fn reconcile_operations(
    snapshot: &ContextSnapshot,
    desired_entries: &[ContextEntry],
    operation_id: &str,
    reason: &str,
) -> Result<Vec<ChangeSetOperation>, ContextError> {
    let mut desired_ids = HashSet::new();
    for entry in desired_entries {
        validate_edit_entry(entry)?;
        if !desired_ids.insert(entry.entry_id.clone()) {
            return Err(ContextError::DuplicateEntry);
        }
        if !snapshot
            .entries
            .iter()
            .any(|active| active.entry_id == entry.entry_id)
            && snapshot
                .tombstones
                .iter()
                .any(|tombstone| tombstone.entry_id == entry.entry_id)
        {
            return Err(ContextError::TombstonedEntry);
        }
    }
    let desired_by_id: HashMap<_, _> = desired_entries
        .iter()
        .map(|entry| (entry.entry_id.clone(), entry))
        .collect();
    let mut unmatched: Vec<_> = snapshot
        .entries
        .iter()
        .filter(|entry| !desired_ids.contains(&entry.entry_id))
        .map(|entry| entry.entry_id.clone())
        .collect();
    let mut operations = Vec::new();

    for current in &snapshot.entries {
        let Some(desired) = desired_by_id.get(&current.entry_id) else {
            continue;
        };
        if current == *desired {
            continue;
        }
        let index = operations.len();
        if current.memory_id != desired.memory_id
            || current.memory_version_id != desired.memory_version_id
        {
            operations.push(ChangeSetOperation::Replace {
                operation_id: format!("{}:replace:{}", operation_id, index),
                old_entry_id: Some(current.entry_id.clone()),
                replacement: (*desired).clone(),
                reason: reason.to_owned(),
            });
        } else {
            operations.push(ChangeSetOperation::Update {
                operation_id: format!("{}:update:{}", operation_id, index),
                entry_id: current.entry_id.clone(),
                updated: (*desired).clone(),
                reason: reason.to_owned(),
            });
        }
    }

    for desired in desired_entries {
        if snapshot
            .entries
            .iter()
            .any(|current| current.entry_id == desired.entry_id)
        {
            continue;
        }
        let old_entry_id = if unmatched.is_empty() {
            None
        } else {
            Some(unmatched.remove(0))
        };
        let index = operations.len();
        operations.push(ChangeSetOperation::Replace {
            operation_id: format!("{}:replace:{}", operation_id, index),
            old_entry_id,
            replacement: desired.clone(),
            reason: reason.to_owned(),
        });
    }
    for old_entry_id in unmatched {
        let index = operations.len();
        operations.push(ChangeSetOperation::Remove {
            operation_id: format!("{}:remove:{}", operation_id, index),
            entry_id: old_entry_id,
            reason: reason.to_owned(),
        });
    }
    if !desired_entries.is_empty() {
        operations.push(ChangeSetOperation::Reorder {
            operation_id: format!("{}:reorder", operation_id),
            entry_ids: desired_entries
                .iter()
                .map(|entry| entry.entry_id.clone())
                .collect(),
            reason: reason.to_owned(),
        });
    }
    Ok(operations)
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
        tombstones: Vec::new(),
        operation_records: Vec::new(),
        rendered_bytes,
    })
}

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
    EntryBudgetExceeded {
        actual: usize,
        limit: usize,
    },
    ByteBudgetExceeded {
        actual: usize,
        limit: usize,
    },
    Serialization(String),
    SnapshotByteCountMismatch {
        actual: usize,
        recorded: usize,
    },
    StaleBase {
        expected: u64,
        actual: u64,
    },
    MissingEntry,
    InvalidReorder,
    ImmutableMemoryVersion,
    TombstonedEntry,
    ExpirationNotDue {
        expires_at: u64,
        target_version: u64,
    },
    InvalidOperationId,
    InvalidContextVersionId,
    InvalidChangeSetId,
    InvalidEntryRevision,
    DuplicateEntryId,
    DuplicateOperationId,
    DuplicateWatermark,
    InvalidOperation,
    InvalidChangeSetStatus,
    BaseVersionMismatch,
    ContextMismatch,
    PolicyEpochStale {
        expected: u64,
        actual: u64,
    },
    SequenceOverflow,
    RollbackFromGenesis,
    NoOpRollback,
    SnapshotHashMismatch {
        declared: String,
        actual: String,
    },
    BudgetSummaryMismatch,
    IdempotencyConflict,
    IdempotencyResultMissing,
    ChangeSetNotPrepared,
    TargetVersionAlreadySet,
    VersionNotFound,
    VersionAlreadySuperseded,
    InvalidVersionLineage,
    EntryByteCountMismatch {
        actual: usize,
        recorded: usize,
    },
    PayloadHashMismatch {
        declared: String,
        actual: String,
    },
}

impl std::fmt::Display for ContextError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{self:?}")
    }
}

impl std::error::Error for ContextError {}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd, Serialize, Deserialize)]
pub struct ContextVersionId(String);

impl ContextVersionId {
    pub fn new(value: impl Into<String>) -> Result<Self, ContextError> {
        let value = value.into();
        if value.trim().is_empty() {
            return Err(ContextError::InvalidContextVersionId);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd, Serialize, Deserialize)]
pub struct ChangeSetId(String);

impl ChangeSetId {
    pub fn new(value: impl Into<String>) -> Result<Self, ContextError> {
        let value = value.into();
        if value.trim().is_empty() {
            return Err(ContextError::InvalidChangeSetId);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextHead {
    pub context_id: OpaqueId,
    pub version: Option<ContextVersionId>,
    pub sequence: u64,
}

impl ContextHead {
    pub fn validate(&self) -> Result<(), ContextError> {
        match (&self.version, self.sequence) {
            (None, 0) => Ok(()),
            (Some(version), sequence) if !version.as_str().is_empty() && sequence > 0 => Ok(()),
            _ => Err(ContextError::InvalidVersion),
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextBudgetSummary {
    pub entry_count: usize,
    pub rendered_bytes: usize,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct CanonicalWatermark {
    pub source: String,
    pub partition: String,
    pub revision: u64,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum EntryState {
    Active,
    Retracted,
    Superseded,
    Expired,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextEntryVersion {
    pub entry_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub memory_version_id: OpaqueId,
    pub revision: u64,
    pub state: EntryState,
    pub tier: ContextTier,
    pub priority: i32,
    pub activation_reason: String,
    pub rendered_content: String,
    pub source_refs: Vec<OpaqueId>,
    pub evidence_refs: Vec<OpaqueId>,
    pub epistemic_qualifiers: Vec<String>,
    pub content_hash: String,
    pub rendered_bytes: usize,
    pub valid_time: Option<TimeValue>,
    pub temporal_ref: Option<TemporalRef>,
}

impl ContextEntryVersion {
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.revision == 0 {
            return Err(ContextError::InvalidEntryRevision);
        }
        if self.rendered_content.trim().is_empty() {
            return Err(ContextError::EmptyField("rendered_content"));
        }
        if self.content_hash.trim().is_empty() {
            return Err(ContextError::EmptyField("content_hash"));
        }
        if self.rendered_bytes != self.rendered_content.len() {
            return Err(ContextError::EntryByteCountMismatch {
                actual: self.rendered_content.len(),
                recorded: self.rendered_bytes,
            });
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ContextOperation {
    AddEntry {
        operation_id: String,
        entry: ContextEntryVersion,
    },
    ReplaceEntry {
        operation_id: String,
        entry: ContextEntryVersion,
        expected_revision: u64,
    },
    RemoveEntry {
        operation_id: String,
        entry_id: OpaqueId,
        expected_revision: u64,
    },
    ReorderEntries {
        operation_id: String,
        entry_ids: Vec<OpaqueId>,
    },
}

impl ContextOperation {
    pub fn operation_id(&self) -> &str {
        match self {
            Self::AddEntry { operation_id, .. }
            | Self::ReplaceEntry { operation_id, .. }
            | Self::RemoveEntry { operation_id, .. }
            | Self::ReorderEntries { operation_id, .. } => operation_id,
        }
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub enum ChangeSetStatus {
    Prepared,
    Committed,
    Rejected,
    Superseded,
    Abandoned,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextChangeSet {
    pub change_set_id: ChangeSetId,
    pub context_id: OpaqueId,
    pub base_version: Option<ContextVersionId>,
    pub target_version: Option<ContextVersionId>,
    pub operations: Vec<ContextOperation>,
    pub reason: String,
    pub actor_ref: ActorRef,
    pub created_at: String,
    pub idempotency_key: String,
    pub payload_hash: String,
    pub policy_epoch: u64,
    pub status: ChangeSetStatus,
    pub correlation_id: Option<String>,
    pub causation_id: Option<String>,
    pub result_ref: Option<String>,
}

impl ContextChangeSet {
    pub fn compute_payload_hash(&self) -> Result<String, ContextError> {
        let payload = (
            &self.change_set_id,
            &self.context_id,
            &self.base_version,
            &self.target_version,
            &self.operations,
            &self.policy_epoch,
        );
        let bytes = serde_json::to_vec(&payload)
            .map_err(|error| ContextError::Serialization(error.to_string()))?;
        Ok(stable_digest(&bytes))
    }

    pub fn validate(&self) -> Result<(), ContextError> {
        if self.reason.trim().is_empty() {
            return Err(ContextError::EmptyField("reason"));
        }
        if self.created_at.trim().is_empty() {
            return Err(ContextError::EmptyField("created_at"));
        }
        if self.idempotency_key.trim().is_empty() {
            return Err(ContextError::EmptyField("idempotency_key"));
        }
        if self.payload_hash.trim().is_empty() {
            return Err(ContextError::EmptyField("payload_hash"));
        }
        if self.operations.is_empty() {
            return Err(ContextError::InvalidOperation);
        }
        if self.target_version.is_some() && self.status == ChangeSetStatus::Prepared {
            return Err(ContextError::TargetVersionAlreadySet);
        }
        let mut operation_ids = HashSet::new();
        for operation in &self.operations {
            if operation.operation_id().trim().is_empty() {
                return Err(ContextError::EmptyField("operation_id"));
            }
            if !operation_ids.insert(operation.operation_id()) {
                return Err(ContextError::DuplicateOperationId);
            }
            match operation {
                ContextOperation::AddEntry { entry, .. } => entry.validate()?,
                ContextOperation::ReplaceEntry { entry, .. } => entry.validate()?,
                ContextOperation::RemoveEntry {
                    expected_revision, ..
                } if *expected_revision == 0 => return Err(ContextError::InvalidEntryRevision),
                _ => {}
            }
        }
        let actual = self.compute_payload_hash()?;
        if actual != self.payload_hash {
            return Err(ContextError::PayloadHashMismatch {
                declared: self.payload_hash.clone(),
                actual,
            });
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextVersion {
    pub context_version_id: ContextVersionId,
    pub context_id: OpaqueId,
    pub sequence: u64,
    pub parent_version_id: Option<ContextVersionId>,
    pub snapshot_ref: String,
    pub snapshot_hash: String,
    pub schema_version: String,
    pub scope_fingerprint: String,
    pub canonical_watermarks: Vec<CanonicalWatermark>,
    pub policy_epoch: u64,
    pub committed_change_set_id: ChangeSetId,
    pub committed_at: String,
    pub actor_ref: ActorRef,
    pub reason: String,
    pub entry_count: usize,
    pub budget_summary: ContextBudgetSummary,
}

impl ContextVersion {
    pub fn validate(&self) -> Result<(), ContextError> {
        if self.sequence == 0 {
            return Err(ContextError::InvalidVersion);
        }
        for (field, value) in [
            ("snapshot_ref", self.snapshot_ref.as_str()),
            ("snapshot_hash", self.snapshot_hash.as_str()),
            ("schema_version", self.schema_version.as_str()),
            ("scope_fingerprint", self.scope_fingerprint.as_str()),
            ("committed_at", self.committed_at.as_str()),
            ("reason", self.reason.as_str()),
        ] {
            if value.trim().is_empty() {
                return Err(ContextError::EmptyField(field));
            }
        }
        if self.entry_count != self.budget_summary.entry_count {
            return Err(ContextError::BudgetSummaryMismatch);
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct VersionMetadata {
    pub context_version_id: ContextVersionId,
    pub schema_version: String,
    pub scope_fingerprint: String,
    pub canonical_watermarks: Vec<CanonicalWatermark>,
    pub policy_epoch: u64,
    pub snapshot_ref: String,
    pub snapshot_hash: String,
    pub budget_summary: ContextBudgetSummary,
    pub committed_at: String,
    pub actor_ref: ActorRef,
    pub reason: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CommitOutcome {
    Committed {
        version: ContextVersion,
        entries: Vec<ContextEntryVersion>,
    },
    Replayed {
        version: ContextVersion,
        entries: Vec<ContextEntryVersion>,
    },
}

#[derive(Clone, Debug, Default)]
pub struct IdempotencyLog {
    records: HashMap<(String, String), IdempotencyRecord>,
}

#[derive(Clone, Debug)]
struct IdempotencyRecord {
    payload_hash: String,
    version: ContextVersion,
    entries: Vec<ContextEntryVersion>,
}

impl IdempotencyLog {
    pub fn len(&self) -> usize {
        self.records.len()
    }

    pub fn is_empty(&self) -> bool {
        self.records.is_empty()
    }
}

pub fn commit_change_set(
    head: &ContextHead,
    change_set: ContextChangeSet,
    current_entries: &[ContextEntryVersion],
    idempotency: &mut IdempotencyLog,
    authorization_epoch: u64,
    metadata: VersionMetadata,
) -> Result<CommitOutcome, ContextError> {
    head.validate()?;
    change_set.validate()?;
    if change_set.status != ChangeSetStatus::Prepared {
        return Err(ContextError::ChangeSetNotPrepared);
    }
    if change_set.context_id != head.context_id {
        return Err(ContextError::ContextMismatch);
    }
    if change_set.base_version != head.version {
        return Err(ContextError::BaseVersionMismatch);
    }
    if metadata.policy_epoch != authorization_epoch
        || change_set.policy_epoch != authorization_epoch
    {
        return Err(ContextError::PolicyEpochStale {
            expected: authorization_epoch,
            actual: metadata.policy_epoch,
        });
    }

    let principal_scope = change_set.actor_ref.actor_id.as_str().to_owned();
    let idempotency_key = (principal_scope, change_set.idempotency_key.clone());
    if let Some(record) = idempotency.records.get(&idempotency_key) {
        if record.payload_hash != change_set.payload_hash {
            return Err(ContextError::IdempotencyConflict);
        }
        return Ok(CommitOutcome::Replayed {
            version: record.version.clone(),
            entries: record.entries.clone(),
        });
    }

    let sequence = head
        .sequence
        .checked_add(1)
        .ok_or(ContextError::SequenceOverflow)?;
    let mut staged = current_entries.to_vec();
    validate_unique_entries(&staged)?;
    apply_operations(&mut staged, &change_set.operations)?;
    validate_unique_entries(&staged)?;
    for entry in &staged {
        entry.validate()?;
    }

    let actual_snapshot_hash = snapshot_hash(&staged)?;
    if metadata.snapshot_hash != actual_snapshot_hash {
        return Err(ContextError::SnapshotHashMismatch {
            declared: metadata.snapshot_hash,
            actual: actual_snapshot_hash,
        });
    }

    let rendered_bytes = staged
        .iter()
        .try_fold(0usize, |sum, entry| sum.checked_add(entry.rendered_bytes))
        .ok_or(ContextError::BudgetSummaryMismatch)?;
    let actual_summary = ContextBudgetSummary {
        entry_count: staged.len(),
        rendered_bytes,
    };
    if metadata.budget_summary != actual_summary {
        return Err(ContextError::BudgetSummaryMismatch);
    }

    for (field, value) in [
        ("schema_version", metadata.schema_version.as_str()),
        ("scope_fingerprint", metadata.scope_fingerprint.as_str()),
        ("snapshot_ref", metadata.snapshot_ref.as_str()),
        ("committed_at", metadata.committed_at.as_str()),
        ("reason", metadata.reason.as_str()),
    ] {
        if value.trim().is_empty() {
            return Err(ContextError::EmptyField(field));
        }
    }
    validate_watermarks(&metadata.canonical_watermarks)?;

    let version = ContextVersion {
        context_version_id: metadata.context_version_id,
        context_id: head.context_id.clone(),
        sequence,
        parent_version_id: head.version.clone(),
        snapshot_ref: metadata.snapshot_ref,
        snapshot_hash: metadata.snapshot_hash,
        schema_version: metadata.schema_version,
        scope_fingerprint: metadata.scope_fingerprint,
        canonical_watermarks: metadata.canonical_watermarks,
        policy_epoch: metadata.policy_epoch,
        committed_change_set_id: change_set.change_set_id,
        committed_at: metadata.committed_at,
        actor_ref: metadata.actor_ref,
        reason: metadata.reason,
        entry_count: staged.len(),
        budget_summary: actual_summary,
    };
    version.validate()?;

    idempotency.records.insert(
        idempotency_key,
        IdempotencyRecord {
            payload_hash: change_set.payload_hash,
            version: version.clone(),
            entries: staged.clone(),
        },
    );

    Ok(CommitOutcome::Committed {
        version,
        entries: staged,
    })
}

fn validate_unique_entries(entries: &[ContextEntryVersion]) -> Result<(), ContextError> {
    let mut ids = HashSet::new();
    for entry in entries {
        if !ids.insert(entry.entry_id.clone()) {
            return Err(ContextError::DuplicateEntryId);
        }
    }
    Ok(())
}

fn validate_watermarks(watermarks: &[CanonicalWatermark]) -> Result<(), ContextError> {
    let mut seen = HashSet::new();
    for watermark in watermarks {
        if watermark.source.trim().is_empty() {
            return Err(ContextError::EmptyField("watermark.source"));
        }
        if watermark.partition.trim().is_empty() {
            return Err(ContextError::EmptyField("watermark.partition"));
        }
        if !seen.insert((watermark.source.clone(), watermark.partition.clone())) {
            return Err(ContextError::DuplicateWatermark);
        }
    }
    Ok(())
}

fn apply_operations(
    entries: &mut Vec<ContextEntryVersion>,
    operations: &[ContextOperation],
) -> Result<(), ContextError> {
    for operation in operations {
        match operation {
            ContextOperation::AddEntry { entry, .. } => {
                if entries
                    .iter()
                    .any(|existing| existing.entry_id == entry.entry_id)
                {
                    return Err(ContextError::DuplicateEntryId);
                }
                entries.push(entry.clone());
            }
            ContextOperation::ReplaceEntry {
                entry,
                expected_revision,
                ..
            } => {
                let Some(index) = entries
                    .iter()
                    .position(|existing| existing.entry_id == entry.entry_id)
                else {
                    return Err(ContextError::VersionNotFound);
                };
                if entries[index].revision != *expected_revision {
                    return Err(ContextError::InvalidEntryRevision);
                }
                entries[index] = entry.clone();
            }
            ContextOperation::RemoveEntry {
                entry_id,
                expected_revision,
                ..
            } => {
                let Some(index) = entries
                    .iter()
                    .position(|existing| &existing.entry_id == entry_id)
                else {
                    return Err(ContextError::VersionNotFound);
                };
                if entries[index].revision != *expected_revision {
                    return Err(ContextError::InvalidEntryRevision);
                }
                entries.remove(index);
            }
            ContextOperation::ReorderEntries { entry_ids, .. } => {
                if entry_ids.len() != entries.len() {
                    return Err(ContextError::InvalidOperation);
                }
                let mut reordered = Vec::with_capacity(entries.len());
                for id in entry_ids {
                    let Some(index) = entries.iter().position(|entry| &entry.entry_id == id) else {
                        return Err(ContextError::InvalidOperation);
                    };
                    if reordered
                        .iter()
                        .any(|entry: &ContextEntryVersion| &entry.entry_id == id)
                    {
                        return Err(ContextError::InvalidOperation);
                    }
                    reordered.push(entries[index].clone());
                }
                *entries = reordered;
            }
        }
    }
    Ok(())
}

pub fn snapshot_hash(entries: &[ContextEntryVersion]) -> Result<String, ContextError> {
    let mut canonical = entries.to_vec();
    canonical.sort_by(|left, right| left.entry_id.cmp(&right.entry_id));
    let bytes = serde_json::to_vec(&canonical)
        .map_err(|error| ContextError::Serialization(error.to_string()))?;
    Ok(stable_digest(&bytes))
}

fn stable_digest(bytes: &[u8]) -> String {
    let mut hash: u64 = 0xcbf29ce484222325;
    for byte in bytes {
        hash ^= u64::from(*byte);
        hash = hash.wrapping_mul(0x100000001b3);
    }
    format!("fnv1a64:{hash:016x}")
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RollbackPlanRequest {
    pub target: ContextVersionId,
    pub target_entries: Vec<ContextEntryVersion>,
    pub current_entries: Vec<ContextEntryVersion>,
    pub reason: String,
    pub actor: ActorRef,
    pub change_set_id: ChangeSetId,
    pub created_at: String,
    pub policy_epoch: u64,
}

pub fn plan_rollback(
    head: &ContextHead,
    request: RollbackPlanRequest,
) -> Result<ContextChangeSet, ContextError> {
    let target = &request.target;
    let target_entries = request.target_entries.as_slice();
    let current_entries = request.current_entries.as_slice();
    let reason = request.reason.as_str();
    let actor = request.actor;
    let change_set_id = request.change_set_id;
    let created_at = request.created_at;
    let policy_epoch = request.policy_epoch;

    head.validate()?;
    let base_version = head
        .version
        .clone()
        .ok_or(ContextError::RollbackFromGenesis)?;
    if reason.trim().is_empty() {
        return Err(ContextError::EmptyField("reason"));
    }
    if created_at.trim().is_empty() {
        return Err(ContextError::EmptyField("created_at"));
    }
    validate_unique_entries(target_entries)?;
    validate_unique_entries(current_entries)?;
    for entry in target_entries.iter().chain(current_entries.iter()) {
        entry.validate()?;
    }

    let mut operations = Vec::new();
    let mut current_by_id = HashMap::new();
    let mut target_by_id = HashMap::new();
    for entry in current_entries {
        current_by_id.insert(entry.entry_id.clone(), entry);
    }
    for entry in target_entries {
        target_by_id.insert(entry.entry_id.clone(), entry);
    }

    for current in current_entries {
        if !target_by_id.contains_key(&current.entry_id) {
            let index = operations.len();
            operations.push(ContextOperation::RemoveEntry {
                operation_id: format!("rollback:{}:{index}", change_set_id.as_str()),
                entry_id: current.entry_id.clone(),
                expected_revision: current.revision,
            });
        }
    }
    for target_entry in target_entries {
        match current_by_id.get(&target_entry.entry_id) {
            None => {
                let index = operations.len();
                operations.push(ContextOperation::AddEntry {
                    operation_id: format!("rollback:{}:{index}", change_set_id.as_str()),
                    entry: (*target_entry).clone(),
                });
            }
            Some(current) if *current != target_entry => {
                let index = operations.len();
                operations.push(ContextOperation::ReplaceEntry {
                    operation_id: format!("rollback:{}:{index}", change_set_id.as_str()),
                    entry: (*target_entry).clone(),
                    expected_revision: current.revision,
                });
            }
            Some(_) => {}
        }
    }

    if operations.is_empty() {
        return Err(ContextError::NoOpRollback);
    }

    let mut change_set = ContextChangeSet {
        change_set_id: change_set_id.clone(),
        context_id: head.context_id.clone(),
        base_version: Some(base_version),
        target_version: None,
        operations,
        reason: format!("rollback:{reason}"),
        actor_ref: actor,
        created_at,
        idempotency_key: format!("rollback:{}", change_set_id.as_str()),
        payload_hash: String::new(),
        policy_epoch,
        status: ChangeSetStatus::Prepared,
        correlation_id: Some(format!("rollback:{}", change_set_id.as_str())),
        causation_id: Some(target.as_str().to_owned()),
        result_ref: None,
    };
    change_set.payload_hash = change_set.compute_payload_hash()?;
    change_set.validate()?;
    Ok(change_set)
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct SupersedeOutcome {
    pub previous: ContextVersion,
    pub replacement: ContextVersion,
}

pub fn supersede_version(
    previous: &ContextVersion,
    new_version_id: ContextVersionId,
    committed_at: String,
    reason: String,
) -> Result<ContextVersion, ContextError> {
    if committed_at.trim().is_empty() {
        return Err(ContextError::EmptyField("committed_at"));
    }
    if reason.trim().is_empty() {
        return Err(ContextError::EmptyField("reason"));
    }
    let sequence = previous
        .sequence
        .checked_add(1)
        .ok_or(ContextError::SequenceOverflow)?;
    let replacement = ContextVersion {
        context_version_id: new_version_id,
        context_id: previous.context_id.clone(),
        sequence,
        parent_version_id: Some(previous.context_version_id.clone()),
        snapshot_ref: previous.snapshot_ref.clone(),
        snapshot_hash: previous.snapshot_hash.clone(),
        schema_version: previous.schema_version.clone(),
        scope_fingerprint: previous.scope_fingerprint.clone(),
        canonical_watermarks: previous.canonical_watermarks.clone(),
        policy_epoch: previous.policy_epoch,
        committed_change_set_id: previous.committed_change_set_id.clone(),
        committed_at,
        actor_ref: previous.actor_ref.clone(),
        reason,
        entry_count: previous.entry_count,
        budget_summary: previous.budget_summary.clone(),
    };
    replacement.validate()?;
    Ok(replacement)
}

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

    #[test]
    fn candidate_scope_must_be_contained_by_identity_scope() {
        let mut item = candidate("a", ContextTier::P0, 1, "private");
        item.scope_refs[0].namespace_key = "user:other".into();
        assert_eq!(
            build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
            ContextError::ScopeMismatch
        );
    }

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

    #[test]
    fn zero_context_version_is_rejected() {
        assert_eq!(
            build_context(identity(), 0, budget(), vec![]).unwrap_err(),
            ContextError::InvalidVersion
        );
    }

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

    #[test]
    fn delivery_intent_visibility_is_always_private_pending_gate() {
        let configurations = vec![
            (
                3,
                ContextBudget {
                    max_entries: 1,
                    max_rendered_bytes: 32,
                },
                vec![candidate("a", ContextTier::P0, 1, "memory text")],
            ),
            (
                17,
                ContextBudget {
                    max_entries: 2,
                    max_rendered_bytes: 128,
                },
                vec![
                    candidate("b", ContextTier::P2, 3, "second"),
                    candidate("c", ContextTier::P1, 8, "third"),
                ],
            ),
            (
                99,
                ContextBudget {
                    max_entries: 4,
                    max_rendered_bytes: 512,
                },
                vec![
                    candidate("d", ContextTier::P3, 1, "fourth"),
                    candidate("e", ContextTier::P0, 9, "fifth"),
                    candidate("f", ContextTier::P2, 4, "sixth"),
                ],
            ),
        ];

        for (context_version, context_budget, candidates) in configurations {
            let snapshot =
                build_context(identity(), context_version, context_budget, candidates).unwrap();
            let intent =
                prepare_delivery_intent(id(&format!("delivery-{context_version}")), &snapshot)
                    .unwrap();
            assert_eq!(
                intent.visibility,
                DeliveryVisibility::PrivatePendingPublicationGate
            );
        }
    }

    #[test]
    fn delivery_intent_targets_snapshot_context_version() {
        let snapshot = build_context(identity(), 42, budget(), vec![]).unwrap();
        let intent = prepare_delivery_intent(id("delivery-1"), &snapshot).unwrap();
        assert_eq!(intent.target_context_version, snapshot.context_version);
    }

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

    #[test]
    fn build_context_rejects_candidates_without_lineage() {
        let mut item = candidate("missing-lineage", ContextTier::P0, 1, "valid content");
        item.source_refs.clear();

        assert_eq!(
            build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
            ContextError::MissingLineage
        );
    }

    #[test]
    fn build_context_rejects_whitespace_only_rendered_content() {
        let item = candidate("empty-content", ContextTier::P0, 1, "   \n\t ");

        assert_eq!(
            build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
            ContextError::EmptyField("rendered_content")
        );
    }

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

#[cfg(test)]
mod version_tests {
    use super::*;

    fn oid(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn actor() -> ActorRef {
        ActorRef {
            actor_id: oid("actor-1"),
        }
    }

    fn version_id(value: &str) -> ContextVersionId {
        ContextVersionId::new(value).unwrap()
    }

    fn changeset_id(value: &str) -> ChangeSetId {
        ChangeSetId::new(value).unwrap()
    }

    fn entry(value: &str, content: &str, revision: u64) -> ContextEntryVersion {
        ContextEntryVersion {
            entry_id: oid(value),
            memory_id: oid(&format!("memory-{value}")),
            memory_version_id: oid(&format!("memory-version-{value}")),
            revision,
            state: EntryState::Active,
            tier: ContextTier::P1,
            priority: 10,
            activation_reason: "test".into(),
            rendered_content: content.into(),
            source_refs: vec![oid("source")],
            evidence_refs: vec![],
            epistemic_qualifiers: vec![],
            content_hash: format!("hash-{value}-{revision}"),
            rendered_bytes: content.len(),
            valid_time: Some(TimeValue::Unknown),
            temporal_ref: None,
        }
    }

    fn head() -> ContextHead {
        ContextHead {
            context_id: oid("ctx"),
            version: Some(version_id("v1")),
            sequence: 1,
        }
    }

    fn rollback(
        target_entries: &[ContextEntryVersion],
        current_entries: &[ContextEntryVersion],
    ) -> Result<ContextChangeSet, ContextError> {
        rollback_with_reason(target_entries, current_entries, "restore")
    }

    fn rollback_with_reason(
        target_entries: &[ContextEntryVersion],
        current_entries: &[ContextEntryVersion],
        reason: &str,
    ) -> Result<ContextChangeSet, ContextError> {
        plan_rollback(
            &head(),
            RollbackPlanRequest {
                target: version_id("v0"),
                target_entries: target_entries.to_vec(),
                current_entries: current_entries.to_vec(),
                reason: reason.to_owned(),
                actor: actor(),
                change_set_id: changeset_id("rollback-1"),
                created_at: "2026-01-01T00:00:00Z".into(),
                policy_epoch: 7,
            },
        )
    }

    fn metadata(entries: &[ContextEntryVersion]) -> VersionMetadata {
        VersionMetadata {
            context_version_id: version_id("v2"),
            schema_version: "1".into(),
            scope_fingerprint: "scope-fp".into(),
            canonical_watermarks: vec![],
            policy_epoch: 7,
            snapshot_ref: "snapshot://v2".into(),
            snapshot_hash: snapshot_hash(entries).unwrap(),
            budget_summary: ContextBudgetSummary {
                entry_count: entries.len(),
                rendered_bytes: entries.iter().map(|item| item.rendered_bytes).sum(),
            },
            committed_at: "2026-01-01T00:00:01Z".into(),
            actor_ref: actor(),
            reason: "commit".into(),
        }
    }

    fn prepared_change_set(operations: Vec<ContextOperation>) -> ContextChangeSet {
        let mut value = ContextChangeSet {
            change_set_id: changeset_id("cs-1"),
            context_id: oid("ctx"),
            base_version: Some(version_id("v1")),
            target_version: None,
            operations,
            reason: "test".into(),
            actor_ref: actor(),
            created_at: "2026-01-01T00:00:00Z".into(),
            idempotency_key: "key-1".into(),
            payload_hash: String::new(),
            policy_epoch: 7,
            status: ChangeSetStatus::Prepared,
            correlation_id: None,
            causation_id: None,
            result_ref: None,
        };
        value.payload_hash = value.compute_payload_hash().unwrap();
        value
    }

    #[test]
    fn context_version_id_rejects_empty() {
        assert_eq!(
            ContextVersionId::new(" "),
            Err(ContextError::InvalidContextVersionId)
        );
    }

    #[test]
    fn change_set_id_rejects_empty() {
        assert_eq!(ChangeSetId::new(""), Err(ContextError::InvalidChangeSetId));
    }

    #[test]
    fn context_head_rejects_genesis_with_nonzero_sequence() {
        let value = ContextHead {
            context_id: oid("ctx"),
            version: None,
            sequence: 1,
        };
        assert_eq!(value.validate(), Err(ContextError::InvalidVersion));
    }

    #[test]
    fn context_head_rejects_version_with_zero_sequence() {
        let value = ContextHead {
            context_id: oid("ctx"),
            version: Some(version_id("v1")),
            sequence: 0,
        };
        assert_eq!(value.validate(), Err(ContextError::InvalidVersion));
    }

    #[test]
    fn entry_version_rejects_zero_revision() {
        let mut value = entry("a", "content", 1);
        value.revision = 0;
        assert_eq!(value.validate(), Err(ContextError::InvalidEntryRevision));
    }

    #[test]
    fn entry_version_rejects_rendered_byte_mismatch() {
        let mut value = entry("a", "content", 1);
        value.rendered_bytes = 1;
        assert_eq!(
            value.validate(),
            Err(ContextError::EntryByteCountMismatch {
                actual: 7,
                recorded: 1
            })
        );
    }

    #[test]
    fn change_set_rejects_duplicate_operation_ids() {
        let value = prepared_change_set(vec![
            ContextOperation::AddEntry {
                operation_id: "same".into(),
                entry: entry("a", "a", 1),
            },
            ContextOperation::AddEntry {
                operation_id: "same".into(),
                entry: entry("b", "b", 1),
            },
        ]);
        assert_eq!(value.validate(), Err(ContextError::DuplicateOperationId));
    }

    #[test]
    fn change_set_rejects_empty_operations() {
        let value = prepared_change_set(vec![]);
        assert_eq!(value.validate(), Err(ContextError::InvalidOperation));
    }

    #[test]
    fn change_set_rejects_precomputed_target_version_when_prepared() {
        let mut value = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        value.target_version = Some(version_id("v2"));
        value.payload_hash = value.compute_payload_hash().unwrap();
        assert_eq!(value.validate(), Err(ContextError::TargetVersionAlreadySet));
    }

    #[test]
    fn change_set_rejects_payload_hash_mismatch() {
        let mut value = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        value.payload_hash = "tampered".into();
        assert!(matches!(
            value.validate(),
            Err(ContextError::PayloadHashMismatch { .. })
        ));
    }

    #[test]
    fn rollback_from_genesis_is_rejected() {
        let genesis = ContextHead {
            context_id: oid("ctx"),
            version: None,
            sequence: 0,
        };
        assert_eq!(
            plan_rollback(
                &genesis,
                RollbackPlanRequest {
                    target: version_id("v0"),
                    target_entries: vec![entry("a", "a", 1)],
                    current_entries: vec![],
                    reason: "restore".into(),
                    actor: actor(),
                    change_set_id: changeset_id("cs"),
                    created_at: "time".into(),
                    policy_epoch: 1,
                }
            ),
            Err(ContextError::RollbackFromGenesis)
        );
    }

    #[test]
    fn rollback_rejects_empty_reason() {
        assert_eq!(
            rollback_with_reason(&[entry("a", "a", 1)], &[], ""),
            Err(ContextError::EmptyField("reason"))
        );
    }

    #[test]
    fn rollback_rejects_empty_created_at() {
        assert_eq!(
            plan_rollback(
                &head(),
                RollbackPlanRequest {
                    target: version_id("v0"),
                    target_entries: vec![entry("a", "a", 1)],
                    current_entries: vec![],
                    reason: "restore".into(),
                    actor: actor(),
                    change_set_id: changeset_id("cs"),
                    created_at: String::new(),
                    policy_epoch: 1,
                }
            ),
            Err(ContextError::EmptyField("created_at"))
        );
    }

    #[test]
    fn rollback_rejects_duplicate_target_entry_ids() {
        let duplicate = vec![entry("a", "one", 1), entry("a", "two", 2)];
        assert_eq!(
            rollback(&duplicate, &[]),
            Err(ContextError::DuplicateEntryId)
        );
    }

    #[test]
    fn rollback_rejects_noop_diff() {
        let same = entry("a", "same", 1);
        assert_eq!(
            rollback(std::slice::from_ref(&same), std::slice::from_ref(&same)),
            Err(ContextError::NoOpRollback)
        );
    }

    #[test]
    fn rollback_sets_all_declared_change_set_fields() {
        let target = vec![entry("a", "target", 1)];
        let current = vec![entry("a", "current", 2), entry("b", "remove", 1)];
        let value = rollback(&target, &current).unwrap();
        assert_eq!(value.change_set_id, changeset_id("rollback-1"));
        assert_eq!(value.context_id, head().context_id);
        assert_eq!(value.base_version, Some(version_id("v1")));
        assert_eq!(value.target_version, None);
        assert_eq!(value.reason, "rollback:restore");
        assert_eq!(value.created_at, "2026-01-01T00:00:00Z");
        assert_eq!(value.idempotency_key, "rollback:rollback-1");
        assert_eq!(value.policy_epoch, 7);
        assert_eq!(value.status, ChangeSetStatus::Prepared);
        assert_eq!(value.correlation_id.as_deref(), Some("rollback:rollback-1"));
        assert_eq!(value.causation_id.as_deref(), Some("v0"));
        assert_eq!(value.result_ref, None);
        assert_eq!(value.operations.len(), 2);
    }

    #[test]
    fn rollback_adds_missing_target_entry() {
        let target = vec![entry("new", "new", 1)];
        let value = rollback(&target, &[]).unwrap();
        assert!(matches!(
            value.operations.as_slice(),
            [ContextOperation::AddEntry { entry: added, .. }] if added.entry_id == oid("new")
        ));
    }

    #[test]
    fn rollback_removes_entries_absent_from_target() {
        let current = vec![entry("old", "old", 3)];
        let value = rollback(&[], &current).unwrap();
        assert!(matches!(
            value.operations.as_slice(),
            [ContextOperation::RemoveEntry { entry_id, expected_revision: 3, .. }]
                if entry_id == &oid("old")
        ));
    }

    #[test]
    fn rollback_replaces_changed_entry_with_target_revision() {
        let target = vec![entry("a", "target", 1)];
        let current = vec![entry("a", "current", 2)];
        let value = rollback(&target, &current).unwrap();
        assert!(matches!(
            value.operations.as_slice(),
            [ContextOperation::ReplaceEntry {
                entry,
                expected_revision: 2,
                ..
            }] if entry.rendered_content == "target"
        ));
    }

    #[test]
    fn rollback_operation_ids_are_deterministic() {
        let target = vec![entry("a", "new-a", 1), entry("b", "new-b", 1)];
        let first = rollback(&target, &[]).unwrap();
        let second = rollback(&target, &[]).unwrap();
        assert_eq!(
            first
                .operations
                .iter()
                .map(ContextOperation::operation_id)
                .collect::<Vec<_>>(),
            second
                .operations
                .iter()
                .map(ContextOperation::operation_id)
                .collect::<Vec<_>>()
        );
    }

    #[test]
    fn commit_rejects_stale_policy_epoch() {
        let change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        let mut metadata = metadata(&[entry("a", "a", 1)]);
        metadata.policy_epoch = 6;
        assert!(matches!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata
            ),
            Err(ContextError::PolicyEpochStale { .. })
        ));
    }

    #[test]
    fn commit_rejects_wrong_base_version() {
        let mut change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        change_set.base_version = Some(version_id("stale"));
        change_set.payload_hash = change_set.compute_payload_hash().unwrap();
        assert_eq!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata(&[entry("a", "a", 1)])
            ),
            Err(ContextError::BaseVersionMismatch)
        );
    }

    #[test]
    fn commit_rejects_context_mismatch() {
        let mut change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        change_set.context_id = oid("other");
        change_set.payload_hash = change_set.compute_payload_hash().unwrap();
        assert_eq!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata(&[entry("a", "a", 1)])
            ),
            Err(ContextError::ContextMismatch)
        );
    }

    #[test]
    fn commit_rejects_snapshot_hash_mismatch() {
        let change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        let mut metadata = metadata(&[entry("a", "a", 1)]);
        metadata.snapshot_hash = "wrong".into();
        assert!(matches!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata
            ),
            Err(ContextError::SnapshotHashMismatch { .. })
        ));
    }

    #[test]
    fn commit_rejects_budget_summary_mismatch() {
        let change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: entry("a", "a", 1),
        }]);
        let mut metadata = metadata(&[entry("a", "a", 1)]);
        metadata.budget_summary.entry_count = 99;
        assert_eq!(
            commit_change_set(
                &head(),
                change_set,
                &[],
                &mut IdempotencyLog::default(),
                7,
                metadata
            ),
            Err(ContextError::BudgetSummaryMismatch)
        );
    }

    #[test]
    fn commit_returns_version_with_caller_metadata_and_computed_sequence() {
        let added = entry("a", "a", 1);
        let change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: added.clone(),
        }]);
        let outcome = commit_change_set(
            &head(),
            change_set,
            &[],
            &mut IdempotencyLog::default(),
            7,
            metadata(&[added]),
        )
        .unwrap();
        let CommitOutcome::Committed { version, entries } = outcome else {
            panic!("expected a first commit");
        };
        assert_eq!(version.context_version_id, version_id("v2"));
        assert_eq!(version.context_id, oid("ctx"));
        assert_eq!(version.sequence, 2);
        assert_eq!(version.parent_version_id, Some(version_id("v1")));
        assert_eq!(version.policy_epoch, 7);
        assert_eq!(version.entry_count, 1);
        assert_eq!(entries.len(), 1);
    }

    #[test]
    fn commit_is_idempotently_replayed_for_same_principal_and_key() {
        let added = entry("a", "a", 1);
        let change_set = prepared_change_set(vec![ContextOperation::AddEntry {
            operation_id: "add".into(),
            entry: added.clone(),
        }]);
        let mut log = IdempotencyLog::default();
        let first = commit_change_set(
            &head(),
            change_set.clone(),
            &[],
            &mut log,
            7,
            metadata(std::slice::from_ref(&added)),
        )
        .unwrap();
        let second =
            commit_change_set(&head(), change_set, &[], &mut log, 7, metadata(&[added])).unwrap();
        assert!(matches!(first, CommitOutcome::Committed { .. }));
        assert!(matches!(second, CommitOutcome::Replayed { .. }));
        assert_eq!(log.len(), 1);
    }

    #[test]
    fn supersede_version_increments_sequence_and_preserves_other_fields() {
        let previous = ContextVersion {
            context_version_id: version_id("v1"),
            context_id: oid("ctx"),
            sequence: 1,
            parent_version_id: None,
            snapshot_ref: "snapshot".into(),
            snapshot_hash: "hash".into(),
            schema_version: "1".into(),
            scope_fingerprint: "scope".into(),
            canonical_watermarks: vec![],
            policy_epoch: 4,
            committed_change_set_id: changeset_id("cs"),
            committed_at: "old-time".into(),
            actor_ref: actor(),
            reason: "old-reason".into(),
            entry_count: 0,
            budget_summary: ContextBudgetSummary {
                entry_count: 0,
                rendered_bytes: 0,
            },
        };
        let next = supersede_version(
            &previous,
            version_id("v2"),
            "new-time".into(),
            "superseded".into(),
        )
        .unwrap();
        assert_eq!(next.sequence, 2);
        assert_eq!(next.parent_version_id, Some(version_id("v1")));
        assert_eq!(next.snapshot_hash, previous.snapshot_hash);
        assert_eq!(next.committed_at, "new-time");
        assert_eq!(next.reason, "superseded");
    }

    #[test]
    fn supersede_version_rejects_sequence_overflow() {
        let previous = ContextVersion {
            context_version_id: version_id("v-max"),
            context_id: oid("ctx"),
            sequence: u64::MAX,
            parent_version_id: None,
            snapshot_ref: "snapshot".into(),
            snapshot_hash: "hash".into(),
            schema_version: "1".into(),
            scope_fingerprint: "scope".into(),
            canonical_watermarks: vec![],
            policy_epoch: 1,
            committed_change_set_id: changeset_id("cs"),
            committed_at: "time".into(),
            actor_ref: actor(),
            reason: "reason".into(),
            entry_count: 0,
            budget_summary: ContextBudgetSummary {
                entry_count: 0,
                rendered_bytes: 0,
            },
        };
        assert_eq!(
            supersede_version(
                &previous,
                version_id("v-next"),
                "time".into(),
                "reason".into()
            ),
            Err(ContextError::SequenceOverflow)
        );
    }

    #[test]
    fn snapshot_hash_is_independent_of_entry_order() {
        let first = vec![entry("a", "a", 1), entry("b", "b", 1)];
        let second = vec![entry("b", "b", 1), entry("a", "a", 1)];
        assert_eq!(snapshot_hash(&first), snapshot_hash(&second));
    }
}

#[cfg(test)]
mod changeset_tests {
    use super::*;
    use memory_domain::ScopeKind;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn scope() -> ScopeRef {
        ScopeRef {
            scope_id: id("scope"),
            scope_kind: ScopeKind::User,
            namespace_key: "user:test".into(),
        }
    }

    fn snapshot(values: &[(&str, &str)]) -> ContextSnapshot {
        let identity = ContextIdentity {
            context_id: id("ctx"),
            scope_refs: vec![scope()],
            agent_id: id("agent"),
            agent_instance_id: id("instance"),
            session_id: id("session"),
            task_id: None,
            environment_id: None,
            purpose: "test".into(),
            schema_version: "1".into(),
        };
        let candidates = values
            .iter()
            .map(|(entry, content)| ContextCandidate {
                entry_id: id(entry),
                memory_id: id(&format!("memory-{entry}")),
                memory_version_id: id(&format!("version-{entry}")),
                memory_lifecycle: MemoryLifecycle::Active,
                scope_refs: vec![scope()],
                tier: ContextTier::P1,
                priority: 10,
                activation_reason: "test".into(),
                rendered_content: (*content).into(),
                source_refs: vec![id("source")],
                evidence_refs: vec![],
                epistemic_qualifiers: vec![],
                content_hash: format!("hash-{entry}"),
            })
            .collect();
        build_context(
            identity,
            1,
            ContextBudget {
                max_entries: 8,
                max_rendered_bytes: 1024,
            },
            candidates,
        )
        .unwrap()
    }

    fn budget(max_entries: usize, max_rendered_bytes: usize) -> ContextBudget {
        ContextBudget {
            max_entries,
            max_rendered_bytes,
        }
    }

    fn set(operations: Vec<ChangeSetOperation>) -> ChangeSet {
        ChangeSet {
            base_version: 1,
            operations,
        }
    }

    fn updated(entry: &ContextEntry, content: &str) -> ContextEntry {
        let mut value = entry.clone();
        value.rendered_content = content.into();
        value.rendered_bytes = content.len();
        value.content_hash = format!("updated:{content}");
        value
    }

    #[test]
    fn change_set_rejects_duplicate_operation_ids() {
        let change_set = set(vec![
            ChangeSetOperation::Remove {
                operation_id: "same".into(),
                entry_id: id("a"),
                reason: "first".into(),
            },
            ChangeSetOperation::Remove {
                operation_id: "same".into(),
                entry_id: id("b"),
                reason: "second".into(),
            },
        ]);
        assert_eq!(
            change_set.validate(),
            Err(ContextError::DuplicateOperationId)
        );
    }

    #[test]
    fn stale_base_is_rejected_without_changing_snapshot() {
        let base = snapshot(&[("a", "a")]);
        let mut stale = set(vec![ChangeSetOperation::Remove {
            operation_id: "remove-a".into(),
            entry_id: id("a"),
            reason: "no longer needed".into(),
        }]);
        stale.base_version = 2;
        assert_eq!(
            apply_change_set(&base, &stale, &budget(8, 1024)),
            Err(ContextError::StaleBase {
                expected: 2,
                actual: 1
            })
        );
        assert_eq!(base.entries[0].entry_id, id("a"));
        assert!(base.tombstones.is_empty());
    }

    #[test]
    fn any_failing_operation_discards_the_entire_staged_set() {
        let base = snapshot(&[("a", "before")]);
        let original = base.clone();
        let after_first = updated(&base.entries[0], "after");
        let after_second = updated(&after_first, "after again");
        let change_set = set(vec![
            ChangeSetOperation::Update {
                operation_id: "update-a-1".into(),
                entry_id: id("a"),
                updated: after_first,
                reason: "first valid staged edit".into(),
            },
            ChangeSetOperation::Update {
                operation_id: "update-a-2".into(),
                entry_id: id("a"),
                updated: after_second,
                reason: "second valid staged edit".into(),
            },
            ChangeSetOperation::Remove {
                operation_id: "remove-missing".into(),
                entry_id: id("missing"),
                reason: "third operation is invalid".into(),
            },
        ]);
        assert_eq!(
            apply_change_set(&base, &change_set, &budget(8, 1024)),
            Err(ContextError::MissingEntry)
        );
        assert_eq!(base, original);
    }

    #[test]
    fn remove_tombstone_is_visible_to_later_reconcile() {
        let base = snapshot(&[("a", "keep")]);
        let old_entry = base.entries[0].clone();
        let removed = apply_change_set(
            &base,
            &set(vec![ChangeSetOperation::Remove {
                operation_id: "remove-a".into(),
                entry_id: id("a"),
                reason: "membership removed, not forgotten".into(),
            }]),
            &budget(8, 1024),
        )
        .unwrap();
        assert_eq!(removed.tombstones.len(), 1);
        assert_eq!(removed.tombstones[0].operation_id, "remove-a");
        assert_eq!(
            removed.tombstones[0].reason,
            "membership removed, not forgotten"
        );
        let reconcile = ChangeSet {
            base_version: removed.context_version,
            operations: vec![ChangeSetOperation::Reconcile {
                operation_id: "reconcile".into(),
                desired_entries: vec![old_entry.clone()],
                reason: "desired state supplied".into(),
            }],
        };
        assert_eq!(
            apply_change_set(&removed, &reconcile, &budget(8, 1024)),
            Err(ContextError::TombstonedEntry)
        );
        let direct_replace = ChangeSet {
            base_version: removed.context_version,
            operations: vec![ChangeSetOperation::Replace {
                operation_id: "attempt-resurrection".into(),
                old_entry_id: None,
                replacement: old_entry,
                reason: "must not bypass tombstone".into(),
            }],
        };
        assert_eq!(
            apply_change_set(&removed, &direct_replace, &budget(8, 1024)),
            Err(ContextError::TombstonedEntry)
        );
    }

    #[test]
    fn reorder_rejects_non_permutation() {
        let base = snapshot(&[("a", "a"), ("b", "b")]);
        let change_set = set(vec![ChangeSetOperation::Reorder {
            operation_id: "reorder".into(),
            entry_ids: vec![id("a"), id("new")],
            reason: "invalid permutation".into(),
        }]);
        assert_eq!(
            apply_change_set(&base, &change_set, &budget(8, 1024)),
            Err(ContextError::InvalidReorder)
        );
        assert_eq!(base.entries[1].entry_id, id("b"));
    }

    #[test]
    fn replace_tombstones_old_membership_in_the_same_result() {
        let base = snapshot(&[("old", "old content")]);
        let replacement = snapshot(&[("new", "new content")]).entries.remove(0);
        let result = apply_change_set(
            &base,
            &set(vec![ChangeSetOperation::Replace {
                operation_id: "replace-old".into(),
                old_entry_id: Some(id("old")),
                replacement,
                reason: "superseded membership".into(),
            }]),
            &budget(8, 1024),
        )
        .unwrap();
        assert_eq!(result.entries.len(), 1);
        assert_eq!(result.entries[0].entry_id, id("new"));
        assert_eq!(result.tombstones.len(), 1);
        assert_eq!(result.tombstones[0].entry_id, id("old"));
        assert_eq!(result.tombstones[0].operation_id, "replace-old");
        assert_eq!(result.tombstones[0].kind, TombstoneKind::Replaced);
        assert_eq!(result.operation_records[0].operation_id, "replace-old");
        assert_eq!(result.operation_records[0].reason, "superseded membership");
    }

    #[test]
    fn update_preserves_memory_version_and_rejects_version_changes() {
        let base = snapshot(&[("a", "before")]);
        let memory_version_id = base.entries[0].memory_version_id.clone();
        let result = apply_change_set(
            &base,
            &set(vec![ChangeSetOperation::Update {
                operation_id: "update-a".into(),
                entry_id: id("a"),
                updated: updated(&base.entries[0], "after"),
                reason: "render-only update".into(),
            }]),
            &budget(8, 1024),
        )
        .unwrap();
        assert_eq!(result.entries[0].rendered_content, "after");
        assert_eq!(result.entries[0].memory_version_id, memory_version_id);
        assert_eq!(
            result.operation_records[0].kind,
            ContextOperationKind::Update
        );
        assert_eq!(result.operation_records[0].reason, "render-only update");

        let mut invalid = updated(&base.entries[0], "changed version");
        invalid.memory_version_id = id("different-version");
        assert_eq!(
            apply_change_set(
                &base,
                &set(vec![ChangeSetOperation::Update {
                    operation_id: "illegal-update".into(),
                    entry_id: id("a"),
                    updated: invalid,
                    reason: "must not mutate canonical version".into(),
                }]),
                &budget(8, 1024),
            ),
            Err(ContextError::ImmutableMemoryVersion)
        );
    }

    #[test]
    fn rendered_byte_budget_is_revalidated_after_update() {
        let base = snapshot(&[("a", "a")]);
        let change_set = set(vec![ChangeSetOperation::Update {
            operation_id: "grow-content".into(),
            entry_id: id("a"),
            updated: updated(&base.entries[0], "12345"),
            reason: "larger rendering".into(),
        }]);
        assert_eq!(
            apply_change_set(&base, &change_set, &budget(8, 4)),
            Err(ContextError::ByteBudgetExceeded {
                actual: 5,
                limit: 4
            })
        );
        assert_eq!(base.entries[0].rendered_content, "a");
    }

    #[test]
    fn expire_uses_target_version_and_preserves_expiration_tombstone() {
        let base = snapshot(&[("a", "expires")]);
        let not_due = set(vec![ChangeSetOperation::Expire {
            operation_id: "expire-a".into(),
            entry_id: id("a"),
            expires_at_context_version: 3,
            reason: "version deadline".into(),
        }]);
        assert_eq!(
            apply_change_set(&base, &not_due, &budget(8, 1024)),
            Err(ContextError::ExpirationNotDue {
                expires_at: 3,
                target_version: 2
            })
        );
        let due = set(vec![ChangeSetOperation::Expire {
            operation_id: "expire-a".into(),
            entry_id: id("a"),
            expires_at_context_version: 2,
            reason: "version deadline".into(),
        }]);
        let result = apply_change_set(&base, &due, &budget(8, 1024)).unwrap();
        assert!(result.entries.is_empty());
        assert_eq!(result.tombstones[0].kind, TombstoneKind::Expired);
        assert_eq!(result.operation_records[0].operation_id, "expire-a");
    }

    #[test]
    fn reconcile_materializes_new_desired_membership_through_replace() {
        let base = snapshot(&[("a", "existing")]);
        let desired = snapshot(&[("a", "existing"), ("b", "new")]).entries;
        let result = apply_change_set(
            &base,
            &set(vec![ChangeSetOperation::Reconcile {
                operation_id: "reconcile-add".into(),
                desired_entries: desired.clone(),
                reason: "desired set includes a new membership".into(),
            }]),
            &budget(8, 1024),
        )
        .unwrap();
        assert_eq!(result.entries, desired);
        assert!(result.tombstones.is_empty());
        assert!(result.operation_records.iter().any(|record| {
            record.kind == ContextOperationKind::Replace
                && record.operation_id == "reconcile-add:replace:0"
        }));
    }

    #[test]
    fn reconcile_emits_updates_replacements_and_a_valid_final_order() {
        let base = snapshot(&[("a", "old-a"), ("b", "remove-b")]);
        let desired_a = updated(&base.entries[0], "new-a");
        let desired_c = snapshot(&[("c", "new-c")]).entries.remove(0);
        let desired = vec![desired_c, desired_a];
        let result = apply_change_set(
            &base,
            &set(vec![ChangeSetOperation::Reconcile {
                operation_id: "reconcile".into(),
                desired_entries: desired.clone(),
                reason: "authoritative desired membership".into(),
            }]),
            &budget(8, 1024),
        )
        .unwrap();
        assert_eq!(result.entries, desired);
        assert_eq!(result.tombstones.len(), 1);
        assert_eq!(result.tombstones[0].entry_id, id("b"));
        assert!(result.operation_records.iter().any(|record| {
            record.kind == ContextOperationKind::Reconcile && record.operation_id == "reconcile"
        }));
    }
}
