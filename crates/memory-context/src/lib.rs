//! Brain-owned, scoped Memory Context planning primitives.
//!
//! This crate deliberately stops before persistence and transport. A built
//! snapshot is a private staged artifact until the D producer/dependency
//! registration, I authorization and D final publication gate have succeeded.
//! Delivery intents created here are therefore non-sendable by construction.

use memory_domain::{scope_set_contains_all, DomainError, MemoryLifecycle, OpaqueId, ScopeRef};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashSet};

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextBudget {
    pub max_entries: usize,
    pub max_rendered_bytes: usize,
}

impl ContextBudget {
    /// Validates that both configured limits are non-zero.
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
    /// Validates required identity fields and scope references.
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

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct ChangeSet {
    pub from_version: u64,
    pub to_version: u64,
    pub added: Vec<OpaqueId>,
    pub removed: Vec<OpaqueId>,
    pub updated: Vec<OpaqueId>,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize, Deserialize)]
pub struct EntryExpiry {
    pub entry_id: OpaqueId,
    pub expires_at_unix: i64,
}

#[derive(Clone, Debug, Default, Eq, PartialEq, Serialize, Deserialize)]
pub struct ExpiryPolicy {
    pub entries: Vec<EntryExpiry>,
}

/// Kept outside ContextSnapshot so existing snapshot literals and wire shape stay stable.
#[derive(Clone, Debug, Default, Eq, PartialEq, Serialize, Deserialize)]
pub struct ContextAcknowledgements {
    pub acknowledged_versions: Vec<u64>,
}

impl ContextAcknowledgements {
    /// Records a consumed version; repeating the same acknowledgement is idempotent.
    pub fn ack(&mut self, version: u64, current_context_version: u64) -> Result<(), ContextError> {
        if version == 0 || version > current_context_version {
            return Err(ContextError::AcknowledgementVersionOutOfRange {
                version,
                current: current_context_version,
            });
        }
        if !self.acknowledged_versions.contains(&version) {
            self.acknowledged_versions.push(version);
            self.acknowledged_versions.sort_unstable();
        }
        Ok(())
    }
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

    /// Removes exactly one entry and advances the snapshot version once.
    pub fn remove_entry(&mut self, entry_id: &OpaqueId) -> Result<(), ContextError> {
        validate_snapshot(self)?;
        let index = self
            .entries
            .iter()
            .position(|entry| &entry.entry_id == entry_id)
            .ok_or(ContextError::EntryNotFound)?;
        let next_version = next_context_version(self.context_version)?;
        let mut next = self.clone();
        next.entries.remove(index);
        next.context_version = next_version;
        recalculate_rendered_bytes(&mut next)?;
        validate_snapshot(&next)?;
        *self = next;
        Ok(())
    }

    /// Replaces rendered content and priority, recalculating byte length and SHA-256.
    pub fn update_entry(
        &mut self,
        entry_id: &OpaqueId,
        rendered_content: String,
        priority: i32,
    ) -> Result<(), ContextError> {
        validate_snapshot(self)?;
        if rendered_content.trim().is_empty() {
            return Err(ContextError::EmptyField("rendered_content"));
        }
        let index = self
            .entries
            .iter()
            .position(|entry| &entry.entry_id == entry_id)
            .ok_or(ContextError::EntryNotFound)?;
        let next_version = next_context_version(self.context_version)?;
        let rendered_bytes = rendered_content.len();
        let content_hash = format!("sha256:{}", sha256_hex(rendered_content.as_bytes()));
        let mut next = self.clone();
        let entry = &mut next.entries[index];
        entry.rendered_content = rendered_content;
        entry.priority = priority;
        entry.rendered_bytes = rendered_bytes;
        entry.content_hash = content_hash;
        next.context_version = next_version;
        recalculate_rendered_bytes(&mut next)?;
        validate_snapshot(&next)?;
        *self = next;
        Ok(())
    }

    /// Removes entries whose explicit expiry timestamp is <= now_unix.
    /// The clock is always supplied by the caller; one batch advances once.
    pub fn expire(
        &mut self,
        now_unix: i64,
        policy: &ExpiryPolicy,
    ) -> Result<Vec<OpaqueId>, ContextError> {
        validate_snapshot(self)?;
        let mut expiries = BTreeMap::new();
        for condition in &policy.entries {
            if !self
                .entries
                .iter()
                .any(|entry| entry.entry_id == condition.entry_id)
            {
                return Err(ContextError::ExpiryEntryNotFound);
            }
            if expiries
                .insert(condition.entry_id.clone(), condition.expires_at_unix)
                .is_some()
            {
                return Err(ContextError::DuplicateExpiryPolicyEntry);
            }
        }
        let removed: Vec<OpaqueId> = self
            .entries
            .iter()
            .filter(|entry| {
                expiries
                    .get(&entry.entry_id)
                    .is_some_and(|expiry| *expiry <= now_unix)
            })
            .map(|entry| entry.entry_id.clone())
            .collect();
        if removed.is_empty() {
            return Ok(removed);
        }

        let next_version = next_context_version(self.context_version)?;
        let expired_ids: HashSet<OpaqueId> = removed.iter().cloned().collect();
        let mut next = self.clone();
        next.entries
            .retain(|entry| !expired_ids.contains(&entry.entry_id));
        next.context_version = next_version;
        recalculate_rendered_bytes(&mut next)?;
        validate_snapshot(&next)?;
        *self = next;
        Ok(removed)
    }
}

/// Computes a pure entry-level delta between two valid snapshots of one context.
pub fn delta(old: &ContextSnapshot, new: &ContextSnapshot) -> Result<ChangeSet, ContextError> {
    validate_snapshot(old)?;
    validate_snapshot(new)?;
    if old.identity != new.identity {
        return Err(ContextError::ContextIdentityMismatch);
    }
    if new.context_version < old.context_version {
        return Err(ContextError::ContextVersionRegression {
            from: old.context_version,
            to: new.context_version,
        });
    }
    if new.context_version == old.context_version && old.entries != new.entries {
        return Err(ContextError::VersionDidNotAdvance(old.context_version));
    }
    let old_entries = entries_by_id(old)?;
    let new_entries = entries_by_id(new)?;
    let added = new_entries
        .iter()
        .filter(|(id, _)| !old_entries.contains_key(*id))
        .map(|(id, _)| id.clone())
        .collect();
    let removed = old_entries
        .iter()
        .filter(|(id, _)| !new_entries.contains_key(*id))
        .map(|(id, _)| id.clone())
        .collect();
    let updated = new_entries
        .iter()
        .filter_map(|(id, new_entry)| match old_entries.get(id) {
            Some(old_entry) if *old_entry != *new_entry => Some(id.clone()),
            _ => None,
        })
        .collect();
    Ok(ChangeSet {
        from_version: old.context_version,
        to_version: new.context_version,
        added,
        removed,
        updated,
    })
}

fn entries_by_id(
    snapshot: &ContextSnapshot,
) -> Result<BTreeMap<OpaqueId, &ContextEntry>, ContextError> {
    let mut entries = BTreeMap::new();
    for entry in &snapshot.entries {
        if entries.insert(entry.entry_id.clone(), entry).is_some() {
            return Err(ContextError::DuplicateEntry);
        }
    }
    Ok(entries)
}

fn next_context_version(version: u64) -> Result<u64, ContextError> {
    version
        .checked_add(1)
        .ok_or(ContextError::ContextVersionOverflow)
}

fn recalculate_rendered_bytes(snapshot: &mut ContextSnapshot) -> Result<(), ContextError> {
    snapshot.rendered_bytes = snapshot
        .entries
        .iter()
        .try_fold(0usize, |sum, entry| sum.checked_add(entry.rendered_bytes))
        .ok_or(ContextError::RenderedByteCountOverflow)?;
    Ok(())
}

/// Dependency-free SHA-256 used to refresh the digest of edited rendered content.
fn sha256_hex(input: &[u8]) -> String {
    const K: [u32; 64] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4,
        0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,
        0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f,
        0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc,
        0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
        0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116,
        0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7,
        0xc67178f2,
    ];
    let mut msg = input.to_vec();
    let bit_len = (input.len() as u64).wrapping_mul(8);
    msg.push(0x80);
    while msg.len() % 64 != 56 {
        msg.push(0);
    }
    msg.extend_from_slice(&bit_len.to_be_bytes());
    let mut h = [
        0x6a09e667u32,
        0xbb67ae85,
        0x3c6ef372,
        0xa54ff53a,
        0x510e527f,
        0x9b05688c,
        0x1f83d9ab,
        0x5be0cd19,
    ];
    for chunk in msg.as_chunks::<64>().0 {
        let mut w = [0u32; 64];
        for (i, word) in w.iter_mut().take(16).enumerate() {
            let j = i * 4;
            *word = u32::from_be_bytes([chunk[j], chunk[j + 1], chunk[j + 2], chunk[j + 3]]);
        }
        for i in 16..64 {
            let x = w[i - 15];
            let y = w[i - 2];
            let s0 = x.rotate_right(7) ^ x.rotate_right(18) ^ (x >> 3);
            let s1 = y.rotate_right(17) ^ y.rotate_right(19) ^ (y >> 10);
            w[i] = w[i - 16]
                .wrapping_add(s0)
                .wrapping_add(w[i - 7])
                .wrapping_add(s1);
        }
        let [mut a, mut b, mut c, mut d, mut e, mut f, mut g, mut hh] = h;
        for i in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ (!e & g);
            let t1 = hh
                .wrapping_add(s1)
                .wrapping_add(ch)
                .wrapping_add(K[i])
                .wrapping_add(w[i]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = s0.wrapping_add(maj);
            hh = g;
            g = f;
            f = e;
            e = d.wrapping_add(t1);
            d = c;
            c = b;
            b = a;
            a = t1.wrapping_add(t2);
        }
        h[0] = h[0].wrapping_add(a);
        h[1] = h[1].wrapping_add(b);
        h[2] = h[2].wrapping_add(c);
        h[3] = h[3].wrapping_add(d);
        h[4] = h[4].wrapping_add(e);
        h[5] = h[5].wrapping_add(f);
        h[6] = h[6].wrapping_add(g);
        h[7] = h[7].wrapping_add(hh);
    }
    let mut out = String::with_capacity(64);
    for word in h {
        out.push_str(&format!("{word:08x}"));
    }
    out
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
    EntryNotFound,
    ContextVersionOverflow,
    RenderedByteCountOverflow,
    DuplicateExpiryPolicyEntry,
    ExpiryEntryNotFound,
    ContextIdentityMismatch,
    ContextVersionRegression { from: u64, to: u64 },
    VersionDidNotAdvance(u64),
    AcknowledgementVersionOutOfRange { version: u64, current: u64 },
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

    // A13 — delivery intent visibility remains private across distinct inputs.
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

    // Restores the original build_context input-lineage rejection assertion.
    #[test]
    fn build_context_rejects_candidates_without_lineage() {
        let mut item = candidate("missing-lineage", ContextTier::P0, 1, "valid content");
        item.source_refs.clear();

        assert_eq!(
            build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
            ContextError::MissingLineage
        );
    }

    // Restores the original build_context input-content rejection assertion.
    #[test]
    fn build_context_rejects_whitespace_only_rendered_content() {
        let item = candidate("empty-content", ContextTier::P0, 1, "   \n\t ");

        assert_eq!(
            build_context(identity(), 1, budget(), vec![item]).unwrap_err(),
            ContextError::EmptyField("rendered_content")
        );
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

    #[test]
    fn remove_entry_removes_and_advances_context_version() {
        let mut s = build_context(
            identity(),
            4,
            budget(),
            vec![
                candidate("remove-me", ContextTier::P0, 1, "four"),
                candidate("keep-me", ContextTier::P1, 1, "xyz"),
            ],
        )
        .unwrap();
        s.remove_entry(&id("remove-me")).unwrap();
        assert_eq!(s.context_version, 5);
        assert_eq!(s.total_entries(), 1);
        assert_eq!(s.entries[0].entry_id, id("keep-me"));
        assert_eq!(s.rendered_bytes, 3);
        validate_snapshot(&s).unwrap();
    }

    #[test]
    fn remove_entry_rejects_missing_id_without_mutation() {
        let mut s = build_context(
            identity(),
            4,
            budget(),
            vec![candidate("present", ContextTier::P0, 1, "text")],
        )
        .unwrap();
        let before = s.clone();
        assert_eq!(
            s.remove_entry(&id("absent")),
            Err(ContextError::EntryNotFound)
        );
        assert_eq!(s, before);
    }

    #[test]
    fn update_entry_recomputes_rendered_bytes_and_content_hash() {
        let mut s = build_context(
            identity(),
            8,
            budget(),
            vec![candidate("update-me", ContextTier::P0, 1, "old")],
        )
        .unwrap();
        s.update_entry(&id("update-me"), "abc".into(), 17).unwrap();
        let e = &s.entries[0];
        assert_eq!(s.context_version, 9);
        assert_eq!(e.priority, 17);
        assert_eq!(e.rendered_content, "abc");
        assert_eq!(e.rendered_bytes, 3);
        assert_eq!(
            e.content_hash,
            "sha256:ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
        assert_eq!(s.rendered_bytes, 3);
        validate_snapshot(&s).unwrap();
    }

    #[test]
    fn update_entry_rejects_empty_content_and_missing_id() {
        let mut s = build_context(
            identity(),
            8,
            budget(),
            vec![candidate("present", ContextTier::P0, 1, "text")],
        )
        .unwrap();
        let before = s.clone();
        assert_eq!(
            s.update_entry(&id("present"), "  \n ".into(), 2),
            Err(ContextError::EmptyField("rendered_content"))
        );
        assert_eq!(
            s.update_entry(&id("absent"), "replacement".into(), 2),
            Err(ContextError::EntryNotFound)
        );
        assert_eq!(s, before);
    }

    #[test]
    fn change_set_serialization_round_trips_all_fields() {
        let cs = ChangeSet {
            from_version: 2,
            to_version: 5,
            added: vec![id("added")],
            removed: vec![id("removed")],
            updated: vec![id("updated")],
        };
        let json = serde_json::to_string(&cs).unwrap();
        let decoded: ChangeSet = serde_json::from_str(&json).unwrap();
        assert_eq!(decoded, cs);
    }

    #[test]
    fn change_set_for_identical_snapshot_is_empty() {
        let s = build_context(identity(), 3, budget(), vec![]).unwrap();
        let cs = delta(&s, &s).unwrap();
        assert_eq!(cs.from_version, 3);
        assert_eq!(cs.to_version, 3);
        assert!(cs.added.is_empty() && cs.removed.is_empty() && cs.updated.is_empty());
    }

    #[test]
    fn delta_reports_added_removed_and_updated_entries() {
        let old = build_context(
            identity(),
            10,
            budget(),
            vec![
                candidate("update", ContextTier::P0, 1, "before"),
                candidate("remove", ContextTier::P1, 1, "gone"),
            ],
        )
        .unwrap();
        let new = build_context(
            identity(),
            12,
            budget(),
            vec![
                candidate("update", ContextTier::P0, 9, "after"),
                candidate("add", ContextTier::P2, 1, "new"),
            ],
        )
        .unwrap();
        let cs = delta(&old, &new).unwrap();
        assert_eq!(cs.from_version, 10);
        assert_eq!(cs.to_version, 12);
        assert_eq!(cs.added, vec![id("add")]);
        assert_eq!(cs.removed, vec![id("remove")]);
        assert_eq!(cs.updated, vec![id("update")]);
    }

    #[test]
    fn delta_rejects_mismatched_identity_and_non_monotonic_versions() {
        let old = build_context(
            identity(),
            10,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "before")],
        )
        .unwrap();
        let mut other = old.clone();
        other.identity.context_id = id("other-context");
        other.context_version = 11;
        assert_eq!(
            delta(&old, &other),
            Err(ContextError::ContextIdentityMismatch)
        );
        let mut regressed = old.clone();
        regressed.context_version = 9;
        assert_eq!(
            delta(&old, &regressed),
            Err(ContextError::ContextVersionRegression { from: 10, to: 9 })
        );
        let mut reused = old.clone();
        reused.entries[0].rendered_content = "changed".into();
        reused.entries[0].rendered_bytes = 7;
        reused.rendered_bytes = 7;
        assert_eq!(
            delta(&old, &reused),
            Err(ContextError::VersionDidNotAdvance(10))
        );
    }

    #[test]
    fn acknowledgement_is_idempotent_for_the_same_version() {
        let mut a = ContextAcknowledgements::default();
        a.ack(2, 4).unwrap();
        a.ack(2, 4).unwrap();
        a.ack(4, 4).unwrap();
        assert_eq!(a.acknowledged_versions, vec![2, 4]);
    }

    #[test]
    fn acknowledgement_rejects_out_of_range_versions() {
        let mut a = ContextAcknowledgements::default();
        assert_eq!(
            a.ack(0, 4),
            Err(ContextError::AcknowledgementVersionOutOfRange {
                version: 0,
                current: 4
            })
        );
        assert_eq!(
            a.ack(5, 4),
            Err(ContextError::AcknowledgementVersionOutOfRange {
                version: 5,
                current: 4
            })
        );
        assert!(a.acknowledged_versions.is_empty());
    }

    #[test]
    fn expire_removes_entries_at_expiry_boundary_and_advances_once() {
        let mut s = build_context(
            identity(),
            20,
            budget(),
            vec![
                candidate("first", ContextTier::P0, 1, "one"),
                candidate("second", ContextTier::P1, 1, "two"),
                candidate("keep", ContextTier::P2, 1, "keep"),
            ],
        )
        .unwrap();
        let policy = ExpiryPolicy {
            entries: vec![
                EntryExpiry {
                    entry_id: id("first"),
                    expires_at_unix: 100,
                },
                EntryExpiry {
                    entry_id: id("second"),
                    expires_at_unix: 101,
                },
            ],
        };
        let removed = s.expire(101, &policy).unwrap();
        assert_eq!(removed, vec![id("first"), id("second")]);
        assert_eq!(s.context_version, 21);
        assert_eq!(s.total_entries(), 1);
        assert_eq!(s.entries[0].entry_id, id("keep"));
        assert_eq!(s.rendered_bytes, 4);
        validate_snapshot(&s).unwrap();
    }

    #[test]
    fn expire_rejects_unknown_policy_entry_without_mutation() {
        let mut s = build_context(
            identity(),
            20,
            budget(),
            vec![candidate("present", ContextTier::P0, 1, "text")],
        )
        .unwrap();
        let before = s.clone();
        let p = ExpiryPolicy {
            entries: vec![EntryExpiry {
                entry_id: id("absent"),
                expires_at_unix: 1,
            }],
        };
        assert_eq!(s.expire(100, &p), Err(ContextError::ExpiryEntryNotFound));
        assert_eq!(s, before);
    }

    #[test]
    fn mutation_rejects_preexisting_snapshot_invariant_violation() {
        let mut s = build_context(
            identity(),
            1,
            budget(),
            vec![candidate("a", ContextTier::P0, 1, "text")],
        )
        .unwrap();
        s.rendered_bytes += 1;
        let before = s.clone();
        assert_eq!(
            s.remove_entry(&id("a")),
            Err(ContextError::SnapshotByteCountMismatch {
                actual: 4,
                recorded: 5
            })
        );
        assert_eq!(s, before);
    }

    #[test]
    fn expire_with_no_due_entries_does_not_advance_version() {
        let mut s = build_context(
            identity(),
            20,
            budget(),
            vec![candidate("keep", ContextTier::P0, 1, "text")],
        )
        .unwrap();
        let p = ExpiryPolicy {
            entries: vec![EntryExpiry {
                entry_id: id("keep"),
                expires_at_unix: 200,
            }],
        };
        assert!(s.expire(100, &p).unwrap().is_empty());
        assert_eq!(s.context_version, 20);
        assert_eq!(s.rendered_bytes, 4);
    }
}
