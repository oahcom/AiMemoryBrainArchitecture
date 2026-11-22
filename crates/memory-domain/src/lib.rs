//! Phase 1 canonical memory domain types.
//! 领域层保持纯 Rust、无存储/网络/LLM 依赖。

use std::collections::BTreeMap;

mod claim_identity;
mod claim_revision_registry;
pub use claim_identity::*;
pub use claim_revision_registry::*;

mod relation_registry;
pub use relation_registry::*;

mod provenance_graph;
pub use provenance_graph::*;

#[derive(
    serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd,
)]
pub struct OpaqueId(String);

impl OpaqueId {
    pub fn new(value: impl Into<String>) -> Result<Self, DomainError> {
        let value = value.into();
        if value.is_empty() {
            return Err(DomainError::EmptyId);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum DomainError {
    EmptyId,
    EmptyRequiredField(&'static str),
    InvalidVersionNumber,
    InvalidParent,
    StaleVersion,
    CrossScopeReference,
    MissingOutcomeEvidence,
    ConflictingIdempotencyPayload,
    MissingClaimRevision,
    MissingFactEvidence,
    MissingFactProvenance,
    MissingRevisionReason,
    MissingIdentityLineage,
    /// §3.6: a derived record must name its lineage or say why it cannot.
    /// A cross-field invariant, not a missing required field — the parent list
    /// is legitimately allowed to be empty when a reason is given.
    IncompleteProvenanceLineage,
    InvalidRelationEndpoint,
    UnregisteredRelationType,
    DuplicateRelationType,
    InvalidMergeState,
    DuplicateClaimRevisionRef,
    UnknownClaimRevision,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ScopeRef {
    pub scope_id: OpaqueId,
    pub scope_kind: ScopeKind,
    pub namespace_key: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum ScopeKind {
    User,
    Project,
    Agent,
    AgentInstance,
    Task,
    Session,
    Environment,
    System,
}

impl ScopeRef {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.namespace_key.is_empty() {
            return Err(DomainError::EmptyRequiredField("namespace_key"));
        }
        Ok(())
    }
}

impl Event {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.event_kind.is_empty() {
            return Err(DomainError::EmptyRequiredField("event_kind"));
        }
        if self.payload_ref.is_empty() {
            return Err(DomainError::EmptyRequiredField("payload_ref"));
        }
        if self.classification.is_empty() {
            return Err(DomainError::EmptyRequiredField("classification"));
        }
        if self.schema_version.is_empty() {
            return Err(DomainError::EmptyRequiredField("schema_version"));
        }
        if self.retention_class.is_empty() {
            return Err(DomainError::EmptyRequiredField("retention_class"));
        }
        if self.scope_refs.is_empty() {
            return Err(DomainError::EmptyRequiredField("scope_refs"));
        }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }
}

impl Claim {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.predicate.is_empty() {
            return Err(DomainError::EmptyRequiredField("predicate"));
        }
        if self.object_value.is_empty() {
            return Err(DomainError::EmptyRequiredField("object_value"));
        }
        if self.polarity.is_empty() {
            return Err(DomainError::EmptyRequiredField("polarity"));
        }
        if self.asserted_at.is_empty() {
            return Err(DomainError::EmptyRequiredField("asserted_at"));
        }
        if self.scope_refs.is_empty() {
            return Err(DomainError::EmptyRequiredField("scope_refs"));
        }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }
}

impl Memory {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.memory_kind.is_empty() {
            return Err(DomainError::EmptyRequiredField("memory_kind"));
        }
        if self.retention_class.is_empty() {
            return Err(DomainError::EmptyRequiredField("retention_class"));
        }
        if self.sensitivity.is_empty() {
            return Err(DomainError::EmptyRequiredField("sensitivity"));
        }
        if self.created_at.is_empty() {
            return Err(DomainError::EmptyRequiredField("created_at"));
        }
        if self.updated_at.is_empty() {
            return Err(DomainError::EmptyRequiredField("updated_at"));
        }
        if self.scope_refs.is_empty() {
            return Err(DomainError::EmptyRequiredField("scope_refs"));
        }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }
}

impl MemoryVersion {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.version_number == 0 {
            return Err(DomainError::InvalidVersionNumber);
        }
        if self.created_at.is_empty() {
            return Err(DomainError::EmptyRequiredField("created_at"));
        }
        if self.author_kind.is_empty() {
            return Err(DomainError::EmptyRequiredField("author_kind"));
        }
        if self.change_reason.is_empty() {
            return Err(DomainError::EmptyRequiredField("change_reason"));
        }
        if self.content_digest.is_empty() {
            return Err(DomainError::EmptyRequiredField("content_digest"));
        }
        if self.schema_version.is_empty() {
            return Err(DomainError::EmptyRequiredField("schema_version"));
        }
        self.claims.iter().try_for_each(Claim::validate)?;
        Ok(())
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ActorRef {
    pub actor_id: OpaqueId,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum TimeValue {
    Instant(String),
    Interval { start: String, end: String },
    Unknown,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct TemporalRef {
    pub occurred_at: TimeValue,
    pub valid_time: TimeValue,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Event {
    pub event_id: OpaqueId,
    pub event_kind: String,
    pub source_id: OpaqueId,
    pub recorded_at: String,
    pub scope_refs: Vec<ScopeRef>,
    pub occurred_at: Option<TimeValue>,
    pub idempotency_key: Option<String>,
    pub payload_ref: String,
    pub classification: String,
    pub schema_version: String,
    pub retention_class: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Claim {
    pub claim_id: OpaqueId,
    pub subject_ref: OpaqueId,
    pub predicate: String,
    pub object_value: String,
    pub polarity: String,
    pub epistemic_status: EpistemicStatus,
    pub confidence: Option<String>,
    pub temporal_ref: Option<TemporalRef>,
    pub asserted_at: String,
    pub scope_refs: Vec<ScopeRef>,
    pub qualifiers: Vec<String>,
    pub evidence_refs: Vec<OpaqueId>,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EpistemicStatus {
    Observed,
    Reported,
    Inferred,
    Verified,
    Disputed,
    Retracted,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Entity {
    pub entity_id: OpaqueId,
    pub entity_type: String,
    pub canonical_label: String,
    pub scope_refs: Vec<ScopeRef>,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Relation {
    pub relation_id: OpaqueId,
    pub relation_type: String,
    pub subject_ref: OpaqueId,
    pub object_ref: OpaqueId,
    pub scope_refs: Vec<ScopeRef>,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Evidence {
    pub evidence_id: OpaqueId,
    pub source_ref: OpaqueId,
    pub recorded_at: String,
    pub scope_refs: Vec<ScopeRef>,
    pub role: EvidenceRole,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EvidenceRole {
    Supports,
    Refutes,
    Qualifies,
    ContextOnly,
}

impl Evidence {
    /// §3.5 / §8: every Evidence has one stable identity, one typed source
    /// reference, at least one ScopeRef and a recorded-at value.
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.evidence_id.as_str().is_empty() {
            return Err(DomainError::EmptyId);
        }
        if self.source_ref.as_str().is_empty() {
            return Err(DomainError::EmptyId);
        }
        if self.recorded_at.trim().is_empty() {
            return Err(DomainError::EmptyRequiredField("recorded_at"));
        }
        if self.scope_refs.is_empty() {
            return Err(DomainError::EmptyRequiredField("scope_refs"));
        }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }

    /// The domain enforcement point for the Evidence/extension pair.
    ///
    /// The two records model one identity in two halves, so a pair whose
    /// identities disagree would let one object claim to be two Evidence
    /// records. `InvalidParent` is reused rather than adding a variant that
    /// only this check would ever construct.
    pub fn validate_against(&self, extension: &EvidenceExtension) -> Result<(), DomainError> {
        self.validate()?;
        extension.validate()?;
        if self.evidence_id.as_str() != extension.evidence_ref.as_str() {
            return Err(DomainError::InvalidParent);
        }
        Ok(())
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Provenance {
    pub provenance_id: OpaqueId,
    pub source_refs: Vec<OpaqueId>,
    pub derivation_kind: String,
    pub actor_ref: ActorRef,
    pub created_at: String,
    pub source_version_refs: Vec<OpaqueId>,
    pub parent_provenance_refs: Vec<ProvenanceRef>,
    pub unavailable_reason: Option<String>,
    pub method_version: Option<String>,
}

impl Provenance {
    /// A derived record must either name its lineage or say why it cannot.
    ///
    /// `source_version_refs` is positional over `source_refs`: when present it
    /// must be complete, because a partial list cannot identify "the exact
    /// version of each versioned source" (phase-2-domain-extension.md §3.6).
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.provenance_id.as_str().is_empty() {
            return Err(DomainError::EmptyId);
        }
        for (field, value) in [
            ("derivation_kind", &self.derivation_kind),
            ("created_at", &self.created_at),
        ] {
            if value.is_empty() {
                return Err(DomainError::EmptyRequiredField(field));
            }
        }
        if self.source_refs.is_empty() {
            return Err(DomainError::EmptyRequiredField("source_refs"));
        }
        // An explicitly supplied reason must contain meaningful text.
        if self
            .unavailable_reason
            .as_deref()
            .is_some_and(|reason| reason.trim().is_empty())
        {
            return Err(DomainError::EmptyRequiredField("unavailable_reason"));
        }
        // Either lineage or an explicit explanation of its absence is mandatory.
        if self.parent_provenance_refs.is_empty() && self.unavailable_reason.is_none() {
            return Err(DomainError::IncompleteProvenanceLineage);
        }
        if !self.source_version_refs.is_empty()
            && self.source_version_refs.len() != self.source_refs.len()
        {
            return Err(DomainError::InvalidVersionNumber);
        }
        Ok(())
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct MemorySource {
    pub memory_source_id: OpaqueId,
    pub source_ref: OpaqueId,
    pub source_role: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct MemoryVersion {
    pub memory_version_id: OpaqueId,
    pub memory_id: OpaqueId,
    pub version_number: u64,
    pub parent_version_id: Option<OpaqueId>,
    pub created_at: String,
    pub author_kind: String,
    pub change_reason: String,
    pub claims: Vec<Claim>,
    pub entity_refs: Vec<OpaqueId>,
    pub relation_refs: Vec<OpaqueId>,
    pub source_refs: Vec<OpaqueId>,
    pub provenance_refs: Vec<OpaqueId>,
    pub content_digest: String,
    pub schema_version: String,
}

impl MemoryVersion {
    pub fn validate_successor(&self, current: &MemoryVersion) -> Result<(), DomainError> {
        if self.memory_id != current.memory_id {
            return Err(DomainError::InvalidParent);
        }
        if self.version_number != current.version_number + 1 {
            return Err(DomainError::InvalidVersionNumber);
        }
        if self.parent_version_id.as_ref() != Some(&current.memory_version_id) {
            return Err(DomainError::InvalidParent);
        }
        Ok(())
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Memory {
    pub memory_id: OpaqueId,
    pub memory_kind: String,
    pub scope_refs: Vec<ScopeRef>,
    pub current_version_id: Option<OpaqueId>,
    pub lifecycle_state: MemoryLifecycle,
    pub retention_class: String,
    pub sensitivity: String,
    pub created_at: String,
    pub updated_at: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum MemoryLifecycle {
    Candidate,
    Consolidated,
    Active,
    Superseded,
    Archived,
    Forgotten,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ContextEntry {
    pub entry_id: OpaqueId,
    pub context_id: OpaqueId,
    pub memory_version_id: OpaqueId,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct MemoryContext {
    pub context_id: OpaqueId,
    pub scope_refs: Vec<ScopeRef>,
    pub context_version: u64,
    pub entries: Vec<ContextEntry>,
}

impl MemoryContext {
    pub fn remove_entry(&mut self, entry_id: &OpaqueId) -> bool {
        let before = self.entries.len();
        self.entries.retain(|entry| &entry.entry_id != entry_id);
        before != self.entries.len()
    }
}

pub fn scopes_intersect(left: &[ScopeRef], right: &[ScopeRef]) -> bool {
    left.iter().any(|l| right.iter().any(|r| l == r))
}

/// Returns true only when every required ScopeRef is present by full canonical identity.
pub fn scope_set_contains_all(container: &[ScopeRef], required: &[ScopeRef]) -> bool {
    required
        .iter()
        .all(|item| container.iter().any(|candidate| candidate == item))
}

pub fn validate_cross_scope_reference(
    source_scopes: &[ScopeRef],
    target_scopes: &[ScopeRef],
    explicitly_shared: bool,
) -> Result<(), DomainError> {
    if explicitly_shared || scopes_intersect(source_scopes, target_scopes) {
        Ok(())
    } else {
        Err(DomainError::CrossScopeReference)
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct IdempotencyRecord {
    pub key: String,
    pub payload_digest: String,
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Default)]
pub struct IdempotencyIndex {
    records: BTreeMap<String, String>,
}

impl IdempotencyIndex {
    pub fn accept(&mut self, key: &str, payload_digest: &str) -> Result<bool, DomainError> {
        match self.records.get(key) {
            None => {
                self.records
                    .insert(key.to_owned(), payload_digest.to_owned());
                Ok(true)
            }
            Some(existing) if existing == payload_digest => Ok(false),
            Some(_) => Err(DomainError::ConflictingIdempotencyPayload),
        }
    }
}

pub fn validate_outcome_claim(
    classification: &str,
    evidence_refs: &[OpaqueId],
) -> Result<(), DomainError> {
    if matches!(classification, "planned" | "predicted" | "attempted") && evidence_refs.is_empty() {
        return Err(DomainError::MissingOutcomeEvidence);
    }
    Ok(())
}

#[doc = r#"Claim and Fact references are intentionally incompatible.
```compile_fail
use memory_domain::{ClaimRef, FactRef};
let claim: ClaimRef = FactRef::new("f").unwrap();
```"#]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct ClaimRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct ClaimRevisionRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct FactRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct FactRevisionRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct EvidenceRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct ProvenanceRef(OpaqueId);
macro_rules! ref_ctor { ($($t:ty),*) => {$(
impl $t {
 pub fn new(v: impl Into<String>) -> Result<Self, DomainError> { Ok(Self(OpaqueId::new(v)?)) }
 pub fn as_str(&self)->&str { self.0.as_str() }
 pub fn validate(&self)->Result<(), DomainError> {
  if self.0.as_str().is_empty() { Err(DomainError::EmptyId) } else { Ok(()) }
 }
}
)*};}
ref_ctor!(
    ClaimRef,
    ClaimRevisionRef,
    FactRef,
    FactRevisionRef,
    EvidenceRef,
    ProvenanceRef
);

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct EntityRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct EventRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct ExternalSourceRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct MemoryRef(OpaqueId);
ref_ctor!(EntityRef, EventRef, ExternalSourceRef, MemoryRef);

/// NOT DEFINED: awaiting I. Placeholder only; security identity semantics are not inferred.
/// `pending_i()` is public and any caller can create this placeholder. It is not proof of
/// an attestor identity. This known temporary construction window closes only when I
/// defines the contract and the placeholder is replaced by a validated, non-forgeable ref.
#[doc = r#"The tuple field is private; external callers cannot forge the placeholder directly.
```compile_fail
use memory_domain::{AttestorRef, AuthorizationDecisionRef};
let _ = AttestorRef(());
let _ = AuthorizationDecisionRef(());
let _ = AuthorizationDecisionRef::new("");
```"#]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AttestorRef(());
impl AttestorRef {
    pub const fn pending_i() -> Self {
        Self(())
    }
}
/// NOT DEFINED: awaiting I. Required placeholder; this is not an authorization grant.
/// `pending_i()` is public and any caller can create this placeholder. Validation cannot
/// establish that it is an I-issued authorization decision; see FactRevision::validate.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionRef(());
impl AuthorizationDecisionRef {
    pub const fn pending_i() -> Self {
        Self(())
    }
}
/// NOT DEFINED: awaiting D. Required placeholder with no invented commit semantics.
/// `pending_d()` is public and any caller can create this placeholder. It has no
/// canonical-commit meaning until D freezes that contract.
#[doc = r#"The tuple field is private; external callers cannot forge the placeholder directly.
```compile_fail
use memory_domain::CanonicalCommitRef;
let _ = CanonicalCommitRef(());
```"#]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitRef(());
impl CanonicalCommitRef {
    pub const fn pending_d() -> Self {
        Self(())
    }
}

#[doc = r#"Immutable revision fields are private; corrections append successors.
```compile_fail
use memory_domain::{ClaimRevision, ClaimRef, ClaimRevisionRef, EpistemicStatus, TimeValue};
let mut r=ClaimRevision::initial(ClaimRevisionRef::new("r").unwrap(),ClaimRef::new("c").unwrap(),"s".into(),"p".into(),"o".into(),"+".into(),vec![],EpistemicStatus::Observed,TimeValue::Unknown,vec![],vec![],"t".into(),"initial".into(),vec![ScopeRef { scope_id: OpaqueId::new("s").unwrap(), scope_kind: ScopeKind::User, namespace_key: "user:s".into() }]).unwrap();
r.predicate=String::from("mutated");
```"#]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ClaimRevision {
    revision_ref: ClaimRevisionRef,
    claim_ref: ClaimRef,
    parent_revision_ref: Option<ClaimRevisionRef>,
    subject: String,
    predicate: String,
    object: String,
    polarity: String,
    qualifiers: Vec<String>,
    epistemic_status: EpistemicStatus,
    valid_time: TimeValue,
    evidence_refs: Vec<EvidenceRef>,
    provenance_refs: Vec<ProvenanceRef>,
    asserted_at: String,
    revision_reason: String,
    scope_refs: Vec<ScopeRef>,
}
impl ClaimRevision {
    #[allow(clippy::too_many_arguments)]
    pub fn initial(
        revision_ref: ClaimRevisionRef,
        claim_ref: ClaimRef,
        subject: String,
        predicate: String,
        object: String,
        polarity: String,
        qualifiers: Vec<String>,
        epistemic_status: EpistemicStatus,
        valid_time: TimeValue,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        asserted_at: String,
        revision_reason: String,
        scope_refs: Vec<ScopeRef>,
    ) -> Result<Self, DomainError> {
        Self::new(
            revision_ref,
            claim_ref,
            None,
            subject,
            predicate,
            object,
            polarity,
            qualifiers,
            epistemic_status,
            valid_time,
            evidence_refs,
            provenance_refs,
            asserted_at,
            revision_reason,
            scope_refs,
        )
    }
    #[allow(clippy::too_many_arguments)]
    pub fn successor(
        revision_ref: ClaimRevisionRef,
        claim_ref: ClaimRef,
        parent: &ClaimRevision,
        subject: String,
        predicate: String,
        object: String,
        polarity: String,
        qualifiers: Vec<String>,
        epistemic_status: EpistemicStatus,
        valid_time: TimeValue,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        asserted_at: String,
        revision_reason: String,
        scope_refs: Vec<ScopeRef>,
    ) -> Result<Self, DomainError> {
        Self::new(
            revision_ref,
            claim_ref,
            Some(parent),
            subject,
            predicate,
            object,
            polarity,
            qualifiers,
            epistemic_status,
            valid_time,
            evidence_refs,
            provenance_refs,
            asserted_at,
            revision_reason,
            scope_refs,
        )
    }
    #[allow(clippy::too_many_arguments)]
    fn new(
        revision_ref: ClaimRevisionRef,
        claim_ref: ClaimRef,
        parent: Option<&ClaimRevision>,
        subject: String,
        predicate: String,
        object: String,
        polarity: String,
        qualifiers: Vec<String>,
        epistemic_status: EpistemicStatus,
        valid_time: TimeValue,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        asserted_at: String,
        revision_reason: String,
        scope_refs: Vec<ScopeRef>,
    ) -> Result<Self, DomainError> {
        let parent_revision_ref = parent.map(|p| p.revision_ref.clone());
        if let Some(p) = parent {
            if p.claim_ref != claim_ref {
                return Err(DomainError::InvalidParent);
            }
        }
        let value = Self {
            revision_ref,
            claim_ref,
            parent_revision_ref,
            subject,
            predicate,
            object,
            polarity,
            qualifiers,
            epistemic_status,
            valid_time,
            evidence_refs,
            provenance_refs,
            asserted_at,
            revision_reason,
            scope_refs,
        };
        value.validate()?;
        Ok(value)
    }
    /// Re-check a deserialized revision against its resolved parent. Serde can
    /// materialize private fields without invoking constructors, so repository
    /// loaders must call this after resolving the parent reference.
    pub fn validate_parent(&self, parent: Option<&ClaimRevision>) -> Result<(), DomainError> {
        match (&self.parent_revision_ref, parent) {
            (None, None) => Ok(()),
            (Some(expected), Some(actual))
                if expected == &actual.revision_ref && self.claim_ref == actual.claim_ref =>
            {
                Ok(())
            }
            _ => Err(DomainError::InvalidParent),
        }
    }
    pub fn validate(&self) -> Result<(), DomainError> {
        for (field, value) in [
            ("subject", &self.subject),
            ("predicate", &self.predicate),
            ("object", &self.object),
            ("polarity", &self.polarity),
            ("asserted_at", &self.asserted_at),
            ("revision_reason", &self.revision_reason),
        ] {
            if value.is_empty() {
                return Err(DomainError::EmptyRequiredField(field));
            }
        }
        self.claim_ref.validate()?;
        self.revision_ref.validate()?;
        if self.scope_refs.is_empty() {
            return Err(DomainError::EmptyRequiredField("scope_refs"));
        }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)?;
        self.evidence_refs
            .iter()
            .try_for_each(EvidenceRef::validate)?;
        self.provenance_refs
            .iter()
            .try_for_each(ProvenanceRef::validate)?;
        Ok(())
    }
    pub fn revision_ref(&self) -> &ClaimRevisionRef {
        &self.revision_ref
    }
    pub fn claim_ref(&self) -> &ClaimRef {
        &self.claim_ref
    }
    pub fn parent_revision_ref(&self) -> Option<&ClaimRevisionRef> {
        self.parent_revision_ref.as_ref()
    }
    pub fn predicate(&self) -> &str {
        &self.predicate
    }
    pub fn subject(&self) -> &str {
        &self.subject
    }
    pub fn object(&self) -> &str {
        &self.object
    }
    pub fn polarity(&self) -> &str {
        &self.polarity
    }
    pub fn qualifiers(&self) -> &[String] {
        &self.qualifiers
    }
    pub fn epistemic_status(&self) -> &EpistemicStatus {
        &self.epistemic_status
    }
    pub fn valid_time(&self) -> &TimeValue {
        &self.valid_time
    }
    pub fn scope_refs(&self) -> &[ScopeRef] {
        &self.scope_refs
    }
    pub fn evidence_refs(&self) -> &[EvidenceRef] {
        &self.evidence_refs
    }
    pub fn provenance_refs(&self) -> &[ProvenanceRef] {
        &self.provenance_refs
    }
}

#[doc = "Confidence or Verified status alone cannot create a Fact; an attested initial revision is required.\n```compile_fail\nuse memory_domain::{Fact, FactRef, EpistemicStatus};\nlet _ = Fact::new(FactRef::new(\"f\").unwrap(), EpistemicStatus::Verified);\n```"]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Fact {
    fact_ref: FactRef,
    initial_revision: Box<FactRevision>,
}
impl Fact {
    pub fn new(fact_ref: FactRef, initial_revision: FactRevision) -> Result<Self, DomainError> {
        if initial_revision.fact_ref != fact_ref || initial_revision.parent_revision_ref.is_some() {
            return Err(DomainError::InvalidParent);
        }
        Ok(Self {
            fact_ref,
            initial_revision: Box::new(initial_revision),
        })
    }
    pub fn fact_ref(&self) -> &FactRef {
        &self.fact_ref
    }
    pub fn initial_revision(&self) -> &FactRevision {
        &self.initial_revision
    }
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum FactOutcome {
    Attested,
    Corrected,
    Revoked,
    Withdrawn,
}
/// A FactRevision pins one or more exact ClaimRevisionRef values.
/// This Vec is required by domain-model-overview.md §8.1, item 3 (Shared Fact visibility):
/// "A FactRevision linked to multiple ClaimRevisions may remain visible only if every disclosed dependency is independently authorized and not suppressed by an applicable Forget decision."
/// The multi-Claim dependency contract requires a set; validate() rejects an empty set.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct FactRevision {
    fact_ref: FactRef,
    revision_ref: FactRevisionRef,
    parent_revision_ref: Option<FactRevisionRef>,
    claim_revision_refs: Vec<ClaimRevisionRef>,
    evidence_refs: Vec<EvidenceRef>,
    provenance_refs: Vec<ProvenanceRef>,
    scope_ref: ScopeRef,
    attestor_ref: AttestorRef,
    authorization_decision_ref: AuthorizationDecisionRef,
    attestation_method_id: String,
    attestation_method_version: String,
    outcome: FactOutcome,
    rationale: String,
    canonical_commit_ref: CanonicalCommitRef,
    correction_or_revocation_reason: Option<String>,
}
impl FactRevision {
    #[allow(clippy::too_many_arguments)]
    pub fn initial(
        fact_ref: FactRef,
        revision_ref: FactRevisionRef,
        claim_revision_refs: Vec<ClaimRevisionRef>,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        scope_ref: ScopeRef,
        attestor_ref: AttestorRef,
        authorization_decision_ref: AuthorizationDecisionRef,
        attestation_method_id: String,
        attestation_method_version: String,
        outcome: FactOutcome,
        rationale: String,
        canonical_commit_ref: CanonicalCommitRef,
        correction_or_revocation_reason: Option<String>,
    ) -> Result<Self, DomainError> {
        Self::new(
            fact_ref,
            revision_ref,
            None,
            claim_revision_refs,
            evidence_refs,
            provenance_refs,
            scope_ref,
            attestor_ref,
            authorization_decision_ref,
            attestation_method_id,
            attestation_method_version,
            outcome,
            rationale,
            canonical_commit_ref,
            correction_or_revocation_reason,
        )
    }
    #[allow(clippy::too_many_arguments)]
    pub fn successor(
        fact_ref: FactRef,
        revision_ref: FactRevisionRef,
        parent: &FactRevision,
        claim_revision_refs: Vec<ClaimRevisionRef>,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        scope_ref: ScopeRef,
        attestor_ref: AttestorRef,
        authorization_decision_ref: AuthorizationDecisionRef,
        attestation_method_id: String,
        attestation_method_version: String,
        outcome: FactOutcome,
        rationale: String,
        canonical_commit_ref: CanonicalCommitRef,
        correction_or_revocation_reason: Option<String>,
    ) -> Result<Self, DomainError> {
        Self::new(
            fact_ref,
            revision_ref,
            Some(parent),
            claim_revision_refs,
            evidence_refs,
            provenance_refs,
            scope_ref,
            attestor_ref,
            authorization_decision_ref,
            attestation_method_id,
            attestation_method_version,
            outcome,
            rationale,
            canonical_commit_ref,
            correction_or_revocation_reason,
        )
    }
    #[allow(clippy::too_many_arguments)]
    fn new(
        fact_ref: FactRef,
        revision_ref: FactRevisionRef,
        parent: Option<&FactRevision>,
        claim_revision_refs: Vec<ClaimRevisionRef>,
        evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>,
        scope_ref: ScopeRef,
        attestor_ref: AttestorRef,
        authorization_decision_ref: AuthorizationDecisionRef,
        attestation_method_id: String,
        attestation_method_version: String,
        outcome: FactOutcome,
        rationale: String,
        canonical_commit_ref: CanonicalCommitRef,
        correction_or_revocation_reason: Option<String>,
    ) -> Result<Self, DomainError> {
        let parent_revision_ref = parent.map(|p| p.revision_ref.clone());
        if let Some(p) = parent {
            if p.fact_ref != fact_ref {
                return Err(DomainError::InvalidParent);
            }
        }
        let value = Self {
            fact_ref,
            revision_ref,
            parent_revision_ref,
            claim_revision_refs,
            evidence_refs,
            provenance_refs,
            scope_ref,
            attestor_ref,
            authorization_decision_ref,
            attestation_method_id,
            attestation_method_version,
            outcome,
            rationale,
            canonical_commit_ref,
            correction_or_revocation_reason,
        };
        value.validate()?;
        Ok(value)
    }
    /// Re-check a deserialized FactRevision against its resolved parent.
    pub fn validate_parent(&self, parent: Option<&FactRevision>) -> Result<(), DomainError> {
        match (&self.parent_revision_ref, parent) {
            (None, None) => Ok(()),
            (Some(expected), Some(actual))
                if expected == &actual.revision_ref && self.fact_ref == actual.fact_ref =>
            {
                Ok(())
            }
            _ => Err(DomainError::InvalidParent),
        }
    }
    /// Structural validation cannot distinguish a real I-issued attestor/authorization
    /// reference from public pending_i() placeholders, nor a D-issued commit from
    /// pending_d(). A FactRevision using placeholders can therefore validate today.
    /// This known temporary construction window closes only after I and D freeze their
    /// contracts and the placeholders are replaced with validated, non-forgeable refs.
    /// Ok(()) here is not evidence of authorization or canonical acceptance.
    pub fn validate(&self) -> Result<(), DomainError> {
        self.fact_ref.validate()?;
        self.revision_ref.validate()?;
        if let Some(parent) = &self.parent_revision_ref {
            parent.validate()?;
        }
        if self.claim_revision_refs.is_empty() {
            return Err(DomainError::MissingClaimRevision);
        }
        if self.evidence_refs.is_empty() {
            return Err(DomainError::MissingFactEvidence);
        }
        if self.provenance_refs.is_empty() {
            return Err(DomainError::MissingFactProvenance);
        }
        self.claim_revision_refs
            .iter()
            .try_for_each(ClaimRevisionRef::validate)?;
        self.evidence_refs
            .iter()
            .try_for_each(EvidenceRef::validate)?;
        self.provenance_refs
            .iter()
            .try_for_each(ProvenanceRef::validate)?;
        self.scope_ref.validate()?;
        for (n, v) in [
            ("attestation_method_id", &self.attestation_method_id),
            (
                "attestation_method_version",
                &self.attestation_method_version,
            ),
            ("rationale", &self.rationale),
        ] {
            if v.is_empty() {
                return Err(DomainError::EmptyRequiredField(n));
            }
        }
        if (self.parent_revision_ref.is_some()
            || matches!(
                self.outcome,
                FactOutcome::Corrected | FactOutcome::Revoked | FactOutcome::Withdrawn
            ))
            && self
                .correction_or_revocation_reason
                .as_deref()
                .unwrap_or("")
                .is_empty()
        {
            return Err(DomainError::MissingRevisionReason);
        }
        Ok(())
    }
    pub fn fact_ref(&self) -> &FactRef {
        &self.fact_ref
    }
    pub fn revision_ref(&self) -> &FactRevisionRef {
        &self.revision_ref
    }
    pub fn claim_revision_refs(&self) -> &[ClaimRevisionRef] {
        &self.claim_revision_refs
    }
    pub fn evidence_refs(&self) -> &[EvidenceRef] {
        &self.evidence_refs
    }
    pub fn provenance_refs(&self) -> &[ProvenanceRef] {
        &self.provenance_refs
    }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EntityIdentityStatus {
    Provisional,
    Resolved,
    Merged,
    Split,
    Retired,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct EntityAlias {
    pub value: String,
    pub language: Option<String>,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ScopedExternalIdentifier {
    pub namespace: String,
    pub value: String,
    pub scope_ref: ScopeRef,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct EntityMergeLineage {
    pub predecessor_refs: Vec<EntityRef>,
    pub successor_ref: EntityRef,
    pub reason: String,
}
/// Sidecar keeps Phase 1 Entity struct literals source-compatible.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct EntityIdentityExtension {
    pub entity_ref: EntityRef,
    pub status: EntityIdentityStatus,
    pub aliases: Vec<EntityAlias>,
    pub external_identifiers: Vec<ScopedExternalIdentifier>,
    pub merge_lineage: Option<EntityMergeLineage>,
    pub split_successor_refs: Vec<EntityRef>,
}
impl EntityIdentityExtension {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.aliases.iter().any(|a| a.value.is_empty()) {
            return Err(DomainError::EmptyRequiredField("alias"));
        }
        if self
            .external_identifiers
            .iter()
            .any(|i| i.namespace.is_empty() || i.value.is_empty())
        {
            return Err(DomainError::EmptyRequiredField("external_identifier"));
        }
        if self.status == EntityIdentityStatus::Merged {
            let l = self
                .merge_lineage
                .as_ref()
                .ok_or(DomainError::MissingIdentityLineage)?;
            if l.successor_ref == self.entity_ref
                || !l.predecessor_refs.contains(&self.entity_ref)
                || l.reason.is_empty()
            {
                return Err(DomainError::MissingIdentityLineage);
            }
        }
        if self.status == EntityIdentityStatus::Split && self.split_successor_refs.is_empty() {
            return Err(DomainError::MissingIdentityLineage);
        }
        Ok(())
    }
    pub fn add_alias(&mut self, a: EntityAlias) -> Result<(), DomainError> {
        if a.value.is_empty() {
            return Err(DomainError::EmptyRequiredField("alias"));
        }
        self.aliases.push(a);
        Ok(())
    }
    /// Merge this predecessor identity into a distinct resolved successor.
    /// Historical identity remains intact; aliases and scoped external identifiers
    /// are copied to the successor before this identity records its redirect.
    pub fn merge_into(
        &mut self,
        successor: &mut EntityIdentityExtension,
        reason: &str,
    ) -> Result<(), DomainError> {
        if self.entity_ref == successor.entity_ref
            || self.status != EntityIdentityStatus::Resolved
            || successor.status != EntityIdentityStatus::Resolved
            || reason.is_empty()
            || self.merge_lineage.is_some()
            || successor.merge_lineage.is_some()
        {
            return Err(DomainError::InvalidMergeState);
        }
        self.validate()?;
        successor.validate()?;
        for alias in &self.aliases {
            if !successor.aliases.contains(alias) {
                successor.aliases.push(alias.clone());
            }
        }
        for identifier in &self.external_identifiers {
            if !successor.external_identifiers.contains(identifier) {
                successor.external_identifiers.push(identifier.clone());
            }
        }
        self.status = EntityIdentityStatus::Merged;
        self.merge_lineage = Some(EntityMergeLineage {
            predecessor_refs: vec![self.entity_ref.clone()],
            successor_ref: successor.entity_ref.clone(),
            reason: reason.to_owned(),
        });
        self.validate()?;
        successor.validate()
    }
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum RelationEndpoint {
    Entity(EntityRef),
    Claim(ClaimRef),
    Fact(FactRef),
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum RelationEndpointKind {
    Entity,
    Claim,
    Fact,
}
impl RelationEndpoint {
    pub fn kind(&self) -> RelationEndpointKind {
        match self {
            Self::Entity(_) => RelationEndpointKind::Entity,
            Self::Claim(_) => RelationEndpointKind::Claim,
            Self::Fact(_) => RelationEndpointKind::Fact,
        }
    }
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum RelationDirectionality {
    Directed,
    Undirected,
    Symmetric,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum RelationLifecycleState {
    Proposed,
    Active,
    Superseded,
    Retracted,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum ValidTimeRef {
    Unknown,
    Bounded(TimeValue),
    AllTime,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct RelationDefinition {
    pub relation_type: String,
    pub allowed_subject_kinds: Vec<RelationEndpointKind>,
    pub allowed_object_kinds: Vec<RelationEndpointKind>,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct RelationExtension {
    pub subject: RelationEndpoint,
    pub object: RelationEndpoint,
    pub directionality: RelationDirectionality,
    pub qualifiers: Vec<String>,
    pub valid_time: Option<ValidTimeRef>,
    pub epistemic_status: EpistemicStatus,
    pub evidence_refs: Vec<EvidenceRef>,
    pub lifecycle_state: RelationLifecycleState,
    pub scope_refs: Vec<ScopeRef>,
}
impl RelationExtension {
    /// Registry-dependent endpoint compatibility cannot be expressed in static Rust types.
    pub fn validate(&self, d: &RelationDefinition) -> Result<(), DomainError> {
        if !d.allowed_subject_kinds.contains(&self.subject.kind())
            || !d.allowed_object_kinds.contains(&self.object.kind())
        {
            return Err(DomainError::InvalidRelationEndpoint);
        }
        if d.relation_type.is_empty() {
            return Err(DomainError::EmptyRequiredField("relation_type"));
        }
        Ok(())
    }
    pub fn valid_time_or_unknown(&self) -> ValidTimeRef {
        self.valid_time.clone().unwrap_or(ValidTimeRef::Unknown)
    }
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EvidenceKind {
    Document,
    Message,
    Observation,
    Record,
    Dataset,
    Other(String),
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EvidenceSourceRef {
    Event(EventRef),
    Memory(MemoryRef),
    External(ExternalSourceRef),
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum EvidenceAvailability {
    Available,
    Restricted,
    Unavailable,
    Forgotten,
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct EvidenceExtension {
    pub evidence_ref: EvidenceRef,
    pub kind: EvidenceKind,
    pub source_ref: EvidenceSourceRef,
    pub locator: Option<String>,
    pub observed_at: Option<TimeValue>,
    pub collector: ActorRef,
    /// §8 `integrity_digest`: `String, nullable`. `None` means no digest is
    /// available; it is never a reason to fabricate one.
    pub integrity_digest: Option<String>,
    /// §8 `source_reliability_ref`: `OpaqueId, nullable` — a reference to a
    /// *separate* source assessment. It is not a score and says nothing about
    /// whether the evidence is true.
    pub source_reliability_ref: Option<OpaqueId>,
    pub availability: EvidenceAvailability,
}
impl EvidenceExtension {
    /// Scope is not validated here: §8 defines `scope_refs` as an `Evidence`
    /// field, so `Evidence::validate()` is its only authority.
    ///
    /// Every reference is re-validated even though the constructors reject
    /// empty values, because serde derives `Deserialize` for these types and
    /// bypasses the constructors: a payload can carry `""` straight into a
    /// field that no constructor would ever have produced.
    pub fn validate(&self) -> Result<(), DomainError> {
        self.evidence_ref.validate()?;

        match &self.source_ref {
            EvidenceSourceRef::Event(reference) => reference.validate()?,
            EvidenceSourceRef::Memory(reference) => reference.validate()?,
            EvidenceSourceRef::External(reference) => reference.validate()?,
        }

        if self.collector.actor_id.as_str().is_empty() {
            return Err(DomainError::EmptyId);
        }

        if self
            .source_reliability_ref
            .as_ref()
            .is_some_and(|reference| reference.as_str().is_empty())
        {
            return Err(DomainError::EmptyId);
        }

        if self
            .integrity_digest
            .as_deref()
            .is_some_and(|digest| digest.trim().is_empty())
        {
            return Err(DomainError::EmptyRequiredField("integrity_digest"));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn scope(value: &str) -> ScopeRef {
        ScopeRef {
            scope_id: id(value),
            scope_kind: ScopeKind::User,
            namespace_key: format!("user:{value}"),
        }
    }

    #[test]
    fn dm2_01_claim_revision_parent_must_belong_to_same_claim() {
        let ca = ClaimRef::new("ca").unwrap();
        let cb = ClaimRef::new("cb").unwrap();
        let parent = ClaimRevision::initial(
            ClaimRevisionRef::new("r1").unwrap(),
            ca.clone(),
            "s".into(),
            "p".into(),
            "o".into(),
            "+".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "t1".into(),
            "initial".into(),
            vec![scope("s")],
        )
        .unwrap();
        let bad = ClaimRevision::successor(
            ClaimRevisionRef::new("r2").unwrap(),
            cb,
            &parent,
            "s".into(),
            "p".into(),
            "o".into(),
            "+".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "t2".into(),
            "correction".into(),
            vec![scope("s")],
        );
        assert_eq!(bad.unwrap_err(), DomainError::InvalidParent);
    }
    #[test]
    fn dm2_02_claim_revision_is_append_only_and_immutable() {
        let first = ClaimRevision::initial(
            ClaimRevisionRef::new("r1").unwrap(),
            ClaimRef::new("c").unwrap(),
            "s".into(),
            "p".into(),
            "old".into(),
            "+".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "t1".into(),
            "initial".into(),
            vec![scope("s")],
        )
        .unwrap();
        let parent_bytes = serde_json::to_vec(&first).unwrap();
        let next = ClaimRevision::successor(
            ClaimRevisionRef::new("r2").unwrap(),
            first.claim_ref().clone(),
            &first,
            "s".into(),
            "p".into(),
            "new".into(),
            "+".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "t2".into(),
            "correction".into(),
            vec![scope("s")],
        )
        .unwrap();
        assert_eq!(next.parent_revision_ref(), Some(first.revision_ref()));
        assert_eq!(
            serde_json::to_vec(&first).unwrap(),
            parent_bytes,
            "appending a correction must leave every serialized parent field byte-identical"
        );
    }
    #[test]
    fn dm2_03_fact_refs_are_distinct_and_fact_pins_exact_claim_revision() {
        let pinned = ClaimRevisionRef::new("cr1").unwrap();
        let fact_ref = FactRef::new("f").unwrap();
        let evidence = EvidenceRef::new("e").unwrap();
        let provenance = ProvenanceRef::new("p").unwrap();
        let rev = FactRevision::initial(
            fact_ref.clone(),
            FactRevisionRef::new("fr1").unwrap(),
            vec![pinned.clone()],
            vec![evidence.clone()],
            vec![provenance.clone()],
            scope("s"),
            AttestorRef::pending_i(),
            AuthorizationDecisionRef::pending_i(),
            "method".into(),
            "v1".into(),
            FactOutcome::Attested,
            "reason".into(),
            CanonicalCommitRef::pending_d(),
            None,
        )
        .unwrap();
        let fact = Fact::new(fact_ref, rev).unwrap();
        let _head = ClaimRevisionRef::new("cr2").unwrap();
        assert_eq!(fact.initial_revision().claim_revision_refs(), &[pinned]);
        assert_eq!(fact.initial_revision().evidence_refs(), &[evidence]);
        assert_eq!(fact.initial_revision().provenance_refs(), &[provenance]);
    }
    #[test]
    fn dm2_09_fact_pinning_does_not_follow_claim_head_after_append() {
        let claim_ref = ClaimRef::new("claim").unwrap();
        let first = ClaimRevision::initial(
            ClaimRevisionRef::new("claim-r1").unwrap(),
            claim_ref.clone(),
            "subject".into(),
            "has_value".into(),
            "v1".into(),
            "+".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "t1".into(),
            "initial".into(),
            vec![scope("s")],
        )
        .unwrap();
        let first_bytes = serde_json::to_vec(&first).unwrap();
        let fact_ref = FactRef::new("fact").unwrap();
        let fact_revision = FactRevision::initial(
            fact_ref.clone(),
            FactRevisionRef::new("fact-r1").unwrap(),
            vec![first.revision_ref().clone()],
            vec![EvidenceRef::new("evidence").unwrap()],
            vec![ProvenanceRef::new("provenance").unwrap()],
            scope("s"),
            AttestorRef::pending_i(),
            AuthorizationDecisionRef::pending_i(),
            "review".into(),
            "1".into(),
            FactOutcome::Attested,
            "attested against claim-r1".into(),
            CanonicalCommitRef::pending_d(),
            None,
        )
        .unwrap();
        let fact = Fact::new(fact_ref, fact_revision).unwrap();

        let second = ClaimRevision::successor(
            ClaimRevisionRef::new("claim-r2").unwrap(),
            claim_ref,
            &first,
            "subject".into(),
            "has_value".into(),
            "v2".into(),
            "+".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "t2".into(),
            "correction".into(),
            vec![scope("s")],
        )
        .unwrap();
        let mut history = vec![first.clone()];
        history.push(second.clone());

        let pinned_ref = &fact.initial_revision().claim_revision_refs()[0];
        assert_eq!(pinned_ref, first.revision_ref());
        assert_eq!(second.parent_revision_ref(), Some(first.revision_ref()));
        let resolved = history
            .iter()
            .find(|revision| revision.revision_ref() == pinned_ref)
            .unwrap();
        assert_eq!(
            serde_json::to_vec(resolved).unwrap(),
            first_bytes,
            "Fact must resolve its exact pinned ClaimRevision, not the Claim head"
        );
        assert_ne!(history.last().unwrap().revision_ref(), pinned_ref);
    }

    #[test]
    fn dm2_04_fact_cannot_be_constructed_without_claim_evidence_provenance() {
        let r = FactRevision::initial(
            FactRef::new("f").unwrap(),
            FactRevisionRef::new("fr").unwrap(),
            vec![],
            vec![],
            vec![],
            scope("s"),
            AttestorRef::pending_i(),
            AuthorizationDecisionRef::pending_i(),
            "m".into(),
            "v1".into(),
            FactOutcome::Attested,
            "why".into(),
            CanonicalCommitRef::pending_d(),
            None,
        );
        assert_eq!(r.unwrap_err(), DomainError::MissingClaimRevision);
        let no_evidence = FactRevision::initial(
            FactRef::new("f").unwrap(),
            FactRevisionRef::new("fr2").unwrap(),
            vec![ClaimRevisionRef::new("cr").unwrap()],
            vec![],
            vec![ProvenanceRef::new("p").unwrap()],
            scope("s"),
            AttestorRef::pending_i(),
            AuthorizationDecisionRef::pending_i(),
            "m".into(),
            "v1".into(),
            FactOutcome::Attested,
            "why".into(),
            CanonicalCommitRef::pending_d(),
            None,
        );
        assert_eq!(no_evidence.unwrap_err(), DomainError::MissingFactEvidence);
        let no_provenance = FactRevision::initial(
            FactRef::new("f").unwrap(),
            FactRevisionRef::new("fr3").unwrap(),
            vec![ClaimRevisionRef::new("cr").unwrap()],
            vec![EvidenceRef::new("e").unwrap()],
            vec![],
            scope("s"),
            AttestorRef::pending_i(),
            AuthorizationDecisionRef::pending_i(),
            "m".into(),
            "v1".into(),
            FactOutcome::Attested,
            "why".into(),
            CanonicalCommitRef::pending_d(),
            None,
        );
        assert_eq!(
            no_provenance.unwrap_err(),
            DomainError::MissingFactProvenance
        );
    }
    #[test]
    fn dm2_05_entity_merge_requires_successor_lineage_but_alias_does_not() {
        let scope_ref = scope("s");
        let alias = EntityAlias {
            value: "legacy label".into(),
            language: Some("en".into()),
        };
        let external = ScopedExternalIdentifier {
            namespace: "registry".into(),
            value: "A-17".into(),
            scope_ref: scope_ref.clone(),
        };
        let mut a = EntityIdentityExtension {
            entity_ref: EntityRef::new("entity-a").unwrap(),
            status: EntityIdentityStatus::Resolved,
            aliases: vec![alias.clone()],
            external_identifiers: vec![external.clone()],
            merge_lineage: None,
            split_successor_refs: vec![],
        };
        let mut b = EntityIdentityExtension {
            entity_ref: EntityRef::new("entity-b").unwrap(),
            status: EntityIdentityStatus::Resolved,
            aliases: vec![EntityAlias {
                value: "canonical B".into(),
                language: None,
            }],
            external_identifiers: vec![],
            merge_lineage: None,
            split_successor_refs: vec![],
        };

        // A label-only alias addition is not an identity merge.
        a.add_alias(EntityAlias {
            value: "another alias".into(),
            language: None,
        })
        .unwrap();
        assert_eq!(a.status, EntityIdentityStatus::Resolved);

        a.merge_into(&mut b, "duplicate identity resolved").unwrap();
        assert_eq!(a.status, EntityIdentityStatus::Merged);
        let lineage = a.merge_lineage.as_ref().unwrap();
        assert_eq!(lineage.successor_ref, b.entity_ref);
        assert!(lineage.predecessor_refs.contains(&a.entity_ref));
        assert!(
            b.merge_lineage.is_none(),
            "successor B must not point back to A as its successor"
        );
        assert!(
            b.aliases.contains(&alias),
            "source aliases must remain reachable from merged identity B"
        );
        assert!(
            b.external_identifiers.contains(&external),
            "source external identifiers must be migrated to B"
        );
        assert!(a.validate().is_ok());
        assert!(b.validate().is_ok());

        let mut split = a.clone();
        split.status = EntityIdentityStatus::Split;
        split.merge_lineage = None;
        assert_eq!(split.validate(), Err(DomainError::MissingIdentityLineage));
        split.split_successor_refs = vec![EntityRef::new("entity-c").unwrap()];
        assert!(split.validate().is_ok());
    }
    #[test]
    fn dm2_06_relation_endpoint_kind_is_checked_against_definition() {
        let r = RelationExtension {
            subject: RelationEndpoint::Entity(EntityRef::new("e").unwrap()),
            object: RelationEndpoint::Claim(ClaimRef::new("c").unwrap()),
            directionality: RelationDirectionality::Directed,
            qualifiers: vec![],
            valid_time: None,
            epistemic_status: EpistemicStatus::Observed,
            evidence_refs: vec![],
            lifecycle_state: RelationLifecycleState::Proposed,
            scope_refs: vec![],
        };
        let d = RelationDefinition {
            relation_type: "owns".into(),
            allowed_subject_kinds: vec![RelationEndpointKind::Entity],
            allowed_object_kinds: vec![RelationEndpointKind::Entity],
        };
        assert_eq!(r.validate(&d), Err(DomainError::InvalidRelationEndpoint));
    }
    #[test]
    fn dm2_07_evidence_extension_requires_integrity_and_scope() {
        // §8 splits the two dimensions: digest lives on the extension (nullable),
        // scope lives on Evidence (required). Each half is checked on its own.
        let e = EvidenceExtension {
            evidence_ref: EvidenceRef::new("e").unwrap(),
            kind: EvidenceKind::Document,
            source_ref: EvidenceSourceRef::Event(EventRef::new("ev").unwrap()),
            locator: None,
            observed_at: None,
            collector: ActorRef {
                actor_id: id("collector"),
            },
            integrity_digest: Some("sha256:x".into()),
            source_reliability_ref: None,
            availability: EvidenceAvailability::Available,
        };
        assert!(e.validate().is_ok());

        // Nullable digest: absence is legal and must not be treated as a defect.
        let mut without_digest = e.clone();
        without_digest.integrity_digest = None;
        assert_eq!(without_digest.validate(), Ok(()));

        // Present but blank is not a digest.
        let mut blank = e.clone();
        blank.integrity_digest = Some(String::new());
        assert_eq!(
            blank.validate(),
            Err(DomainError::EmptyRequiredField("integrity_digest"))
        );

        let evidence = Evidence {
            evidence_id: id("e"),
            source_ref: id("ev"),
            recorded_at: "2026-01-01T00:00:00Z".into(),
            scope_refs: vec![scope("s")],
            role: EvidenceRole::Supports,
        };
        assert!(evidence.validate().is_ok());
        let no_scope = Evidence {
            scope_refs: vec![],
            ..evidence
        };
        assert_eq!(
            no_scope.validate(),
            Err(DomainError::EmptyRequiredField("scope_refs"))
        );
    }
    #[test]
    fn dm2_08_unknown_valid_time_is_not_timeless() {
        let r = RelationExtension {
            subject: RelationEndpoint::Entity(EntityRef::new("e").unwrap()),
            object: RelationEndpoint::Entity(EntityRef::new("e2").unwrap()),
            directionality: RelationDirectionality::Directed,
            qualifiers: vec![],
            valid_time: None,
            epistemic_status: EpistemicStatus::Observed,
            evidence_refs: vec![],
            lifecycle_state: RelationLifecycleState::Active,
            scope_refs: vec![],
        };
        assert_eq!(r.valid_time_or_unknown(), ValidTimeRef::Unknown);
        assert_ne!(r.valid_time_or_unknown(), ValidTimeRef::AllTime);
    }

    fn claim(value: &str, scope_refs: Vec<ScopeRef>) -> Claim {
        Claim {
            claim_id: id(value),
            subject_ref: id("subject"),
            predicate: "has_value".into(),
            object_value: value.into(),
            polarity: "affirm".into(),
            epistemic_status: EpistemicStatus::Observed,
            confidence: None,
            temporal_ref: None,
            asserted_at: "now".into(),
            scope_refs,
            qualifiers: vec![],
            evidence_refs: vec![id("evidence")],
        }
    }

    #[test]
    fn dm01_objects_are_independent_types() {
        let event = Event {
            event_id: id("event"),
            event_kind: "observation".into(),
            source_id: id("source"),
            recorded_at: "2026-01-01T00:00:00Z".into(),
            scope_refs: vec![scope("s1")],
            occurred_at: None,
            idempotency_key: None,
            payload_ref: "payload".into(),
            classification: "observed".into(),
            schema_version: "1".into(),
            retention_class: "default".into(),
        };
        let memory = Memory {
            memory_id: id("memory"),
            scope_refs: vec![scope("s1")],
            current_version_id: None,
            memory_kind: "knowledge".into(),
            lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        };
        assert_eq!(event.event_id.as_str(), "event");
        assert_eq!(memory.memory_id.as_str(), "memory");
    }

    #[test]
    fn dm02_version_is_immutable_and_successor_validates_parent() {
        let memory_id = id("memory");
        let first = MemoryVersion {
            memory_version_id: id("v1"),
            memory_id: memory_id.clone(),
            version_number: 1,
            parent_version_id: None,
            created_at: "2026-01-01T00:00:00Z".into(),
            author_kind: "test".into(),
            change_reason: "initial".into(),
            claims: vec![],
            entity_refs: vec![],
            relation_refs: vec![],
            source_refs: vec![],
            provenance_refs: vec![],
            content_digest: "digest-v1".into(),
            schema_version: "1".into(),
        };
        let second = MemoryVersion {
            memory_version_id: id("v2"),
            memory_id,
            version_number: 2,
            parent_version_id: Some(id("v1")),
            ..first.clone()
        };
        assert!(second.validate_successor(&first).is_ok());
        assert_eq!(first.version_number, 1);
    }

    #[test]
    fn dm03_stale_parent_is_rejected() {
        let current = MemoryVersion {
            memory_version_id: id("v2"),
            memory_id: id("memory"),
            version_number: 2,
            parent_version_id: Some(id("v1")),
            created_at: "now".into(),
            author_kind: "test".into(),
            change_reason: "update".into(),
            claims: vec![],
            entity_refs: vec![],
            relation_refs: vec![],
            source_refs: vec![],
            provenance_refs: vec![],
            content_digest: "digest".into(),
            schema_version: "1".into(),
        };
        let stale = MemoryVersion {
            memory_version_id: id("v3"),
            memory_id: id("memory"),
            version_number: 3,
            parent_version_id: Some(id("v1")),
            created_at: "now".into(),
            author_kind: "test".into(),
            change_reason: "update".into(),
            claims: vec![],
            entity_refs: vec![],
            relation_refs: vec![],
            source_refs: vec![],
            provenance_refs: vec![],
            content_digest: "digest".into(),
            schema_version: "1".into(),
        };
        assert_eq!(
            stale.validate_successor(&current),
            Err(DomainError::InvalidParent)
        );
    }

    #[test]
    fn dm04_claim_status_is_separate_from_memory_lifecycle() {
        let c = claim("claim", vec![scope("s1")]);
        let m = Memory {
            memory_id: id("memory"),
            scope_refs: vec![scope("s1")],
            memory_kind: "knowledge".into(),
            current_version_id: None,
            lifecycle_state: MemoryLifecycle::Active,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        };
        assert_eq!(c.epistemic_status, EpistemicStatus::Observed);
        assert_eq!(m.lifecycle_state, MemoryLifecycle::Active);
    }

    #[test]
    fn dm05_scope_isolation_requires_overlap_or_explicit_share() {
        let left = vec![scope("a")];
        let right = vec![scope("b")];
        assert_eq!(
            validate_cross_scope_reference(&left, &right, false),
            Err(DomainError::CrossScopeReference)
        );
        assert!(validate_cross_scope_reference(&left, &right, true).is_ok());
    }

    #[test]
    fn dm06_provenance_is_explicit() {
        let p = Provenance {
            provenance_id: id("p1"),
            source_refs: vec![id("source")],
            derivation_kind: "direct_capture".into(),
            actor_ref: ActorRef {
                actor_id: id("actor"),
            },
            created_at: "now".into(),
            source_version_refs: vec![],
            parent_provenance_refs: vec![],
            unavailable_reason: None,
            method_version: None,
        };
        assert_eq!(p.source_refs.len(), 1);
    }

    #[test]
    fn dm07_context_removal_does_not_mutate_memory() {
        let memory_version_id = id("v1");
        let mut context = MemoryContext {
            context_id: id("ctx"),
            scope_refs: vec![scope("s1")],
            context_version: 1,
            entries: vec![ContextEntry {
                entry_id: id("entry"),
                context_id: id("ctx"),
                memory_version_id: memory_version_id.clone(),
            }],
        };
        let memory = Memory {
            memory_id: id("memory"),
            scope_refs: vec![scope("s1")],
            memory_kind: "knowledge".into(),
            current_version_id: Some(memory_version_id),
            lifecycle_state: MemoryLifecycle::Active,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        };
        assert!(context.remove_entry(&id("entry")));
        assert!(context.entries.is_empty());
        assert!(memory.current_version_id.is_some());
    }

    #[test]
    fn dm08_validation_has_no_external_dependencies() {
        assert!(OpaqueId::new("ok").is_ok());
        assert_eq!(OpaqueId::new(""), Err(DomainError::EmptyId));
    }

    #[test]
    fn dm09_domain_types_do_not_require_storage_or_network() {
        let _: Memory = Memory {
            memory_id: id("memory"),
            memory_kind: "knowledge".into(),
            scope_refs: vec![scope("s1")],
            current_version_id: None,
            lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        };
    }

    #[test]
    fn dm08_required_domain_fields_are_enforced() {
        let valid_scope = scope("s1");
        assert!(valid_scope.validate().is_ok());

        let mut invalid_scope = valid_scope.clone();
        invalid_scope.namespace_key.clear();
        assert_eq!(
            invalid_scope.validate(),
            Err(DomainError::EmptyRequiredField("namespace_key"))
        );

        let mut event = Event {
            event_id: id("event"),
            event_kind: "observation".into(),
            source_id: id("source"),
            recorded_at: "now".into(),
            scope_refs: vec![scope("s1")],
            occurred_at: None,
            idempotency_key: None,
            payload_ref: "payload".into(),
            classification: "observed".into(),
            schema_version: "1".into(),
            retention_class: "default".into(),
        };
        assert!(event.validate().is_ok());
        event.classification.clear();
        assert_eq!(
            event.validate(),
            Err(DomainError::EmptyRequiredField("classification"))
        );

        let mut c = claim("claim", vec![scope("s1")]);
        assert!(c.validate().is_ok());
        c.asserted_at.clear();
        assert_eq!(
            c.validate(),
            Err(DomainError::EmptyRequiredField("asserted_at"))
        );
    }

    #[test]
    fn dm09_memory_and_version_required_fields_are_enforced() {
        let mut memory = Memory {
            memory_id: id("memory"),
            memory_kind: "knowledge".into(),
            scope_refs: vec![scope("s1")],
            current_version_id: None,
            lifecycle_state: MemoryLifecycle::Candidate,
            retention_class: "default".into(),
            sensitivity: "normal".into(),
            created_at: "now".into(),
            updated_at: "now".into(),
        };
        assert!(memory.validate().is_ok());
        memory.memory_kind.clear();
        assert_eq!(
            memory.validate(),
            Err(DomainError::EmptyRequiredField("memory_kind"))
        );

        let version = MemoryVersion {
            memory_version_id: id("v1"),
            memory_id: id("memory"),
            version_number: 1,
            parent_version_id: None,
            created_at: "now".into(),
            author_kind: "test".into(),
            change_reason: "initial".into(),
            claims: vec![],
            entity_refs: vec![],
            relation_refs: vec![],
            source_refs: vec![],
            provenance_refs: vec![],
            content_digest: "digest".into(),
            schema_version: "1".into(),
        };
        assert!(version.validate().is_ok());
    }

    #[test]
    fn dm10_idempotency_and_outcome_rules_are_deterministic() {
        let mut index = IdempotencyIndex::default();
        assert_eq!(index.accept("k", "digest"), Ok(true));
        assert_eq!(index.accept("k", "digest"), Ok(false));
        assert_eq!(
            index.accept("k", "other"),
            Err(DomainError::ConflictingIdempotencyPayload)
        );
        assert_eq!(
            validate_outcome_claim("planned", &[]),
            Err(DomainError::MissingOutcomeEvidence)
        );
        assert!(validate_outcome_claim("outcome", &[]).is_ok());
    }
    #[test]
    fn scope_identity_requires_id_kind_and_namespace_to_match() {
        let canonical = scope("same-id");
        let mut other_namespace = canonical.clone();
        other_namespace.namespace_key = "project:same-id".into();
        let mut other_kind = canonical.clone();
        other_kind.scope_kind = ScopeKind::Project;

        assert!(scopes_intersect(
            std::slice::from_ref(&canonical),
            std::slice::from_ref(&canonical)
        ));
        assert!(!scopes_intersect(
            std::slice::from_ref(&canonical),
            std::slice::from_ref(&other_namespace)
        ));
        assert!(!scopes_intersect(
            std::slice::from_ref(&canonical),
            std::slice::from_ref(&other_kind)
        ));
    }

    fn claim_revision_fixture() -> ClaimRevision {
        ClaimRevision::initial(
            ClaimRevisionRef::new("claim-revision-1").unwrap(),
            ClaimRef::new("claim-stable").unwrap(),
            "subject".into(),
            "predicate".into(),
            "object".into(),
            "affirm".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "2026-01-01T00:00:00Z".into(),
            "initial".into(),
            vec![scope("s1")],
        )
        .unwrap()
    }

    fn fact_revision_fixture() -> FactRevision {
        FactRevision::initial(
            FactRef::new("fact-1").unwrap(),
            FactRevisionRef::new("fact-revision-1").unwrap(),
            vec![ClaimRevisionRef::new("claim-revision-1").unwrap()],
            vec![EvidenceRef::new("evidence-1").unwrap()],
            vec![ProvenanceRef::new("provenance-1").unwrap()],
            scope("s1"),
            AttestorRef::pending_i(),
            AuthorizationDecisionRef::pending_i(),
            "independent_review".into(),
            "1.0".into(),
            FactOutcome::Attested,
            "reviewed exact claim revision".into(),
            CanonicalCommitRef::pending_d(),
            None,
        )
        .unwrap()
    }

    #[test]
    fn claim_ref_constructs_and_validates() {
        let value = ClaimRef::new("claim-stable").unwrap();
        assert_eq!(value.as_str(), "claim-stable");
        assert!(value.validate().is_ok());
    }

    #[test]
    fn claim_ref_rejects_empty_id() {
        assert_eq!(ClaimRef::new(""), Err(DomainError::EmptyId));
        let decoded: ClaimRef = serde_json::from_str("\"\"").unwrap();
        assert_eq!(decoded.validate(), Err(DomainError::EmptyId));
    }

    #[test]
    fn claim_revision_ref_constructs_and_validates() {
        let value = ClaimRevisionRef::new("claim-revision").unwrap();
        assert_eq!(value.as_str(), "claim-revision");
        assert!(value.validate().is_ok());
    }

    #[test]
    fn claim_revision_ref_rejects_empty_id() {
        assert_eq!(ClaimRevisionRef::new(""), Err(DomainError::EmptyId));
        let decoded: ClaimRevisionRef = serde_json::from_str("\"\"").unwrap();
        assert_eq!(decoded.validate(), Err(DomainError::EmptyId));
    }

    #[test]
    fn fact_ref_constructs_and_validates_independently() {
        let value = FactRef::new("fact-independent").unwrap();
        assert_eq!(value.as_str(), "fact-independent");
        assert!(value.validate().is_ok());
        assert_ne!(value.as_str(), "claim-independent");
    }

    #[test]
    fn fact_ref_rejects_empty_id() {
        assert_eq!(FactRef::new(""), Err(DomainError::EmptyId));
        let decoded: FactRef = serde_json::from_str("\"\"").unwrap();
        assert_eq!(decoded.validate(), Err(DomainError::EmptyId));
    }

    #[test]
    fn fact_revision_ref_constructs_and_validates_independently() {
        let value = FactRevisionRef::new("fact-revision-independent").unwrap();
        assert_eq!(value.as_str(), "fact-revision-independent");
        assert!(value.validate().is_ok());
        assert_ne!(value.as_str(), "claim-revision-independent");
    }

    #[test]
    fn fact_revision_ref_rejects_empty_id() {
        assert_eq!(FactRevisionRef::new(""), Err(DomainError::EmptyId));
        let decoded: FactRevisionRef = serde_json::from_str("\"\"").unwrap();
        assert_eq!(decoded.validate(), Err(DomainError::EmptyId));
    }

    #[test]
    fn claim_revision_constructs_and_preserves_stable_identity_across_revisions() {
        let first = claim_revision_fixture();
        let second = ClaimRevision::successor(
            ClaimRevisionRef::new("claim-revision-2").unwrap(),
            first.claim_ref().clone(),
            &first,
            "subject".into(),
            "predicate".into(),
            "corrected object".into(),
            "affirm".into(),
            vec![],
            EpistemicStatus::Observed,
            TimeValue::Unknown,
            vec![],
            vec![],
            "2026-01-02T00:00:00Z".into(),
            "correction".into(),
            vec![scope("s1")],
        )
        .unwrap();
        assert!(first.validate().is_ok());
        assert!(second.validate().is_ok());
        assert_eq!(first.claim_ref(), second.claim_ref());
        assert_ne!(first.revision_ref(), second.revision_ref());
        assert_eq!(second.parent_revision_ref(), Some(first.revision_ref()));
    }

    #[test]
    fn claim_revision_rejects_empty_scope_and_empty_reference() {
        let mut missing_scope = claim_revision_fixture();
        missing_scope.scope_refs.clear();
        assert_eq!(
            missing_scope.validate(),
            Err(DomainError::EmptyRequiredField("scope_refs"))
        );

        let mut empty_claim_reference = claim_revision_fixture();
        empty_claim_reference.claim_ref = serde_json::from_str("\"\"").unwrap();
        assert_eq!(empty_claim_reference.validate(), Err(DomainError::EmptyId));

        let mut empty_subject = claim_revision_fixture();
        empty_subject.subject.clear();
        assert_eq!(
            empty_subject.validate(),
            Err(DomainError::EmptyRequiredField("subject"))
        );

        let mut empty_evidence_ref = claim_revision_fixture();
        empty_evidence_ref.evidence_refs = vec![serde_json::from_str("\"\"").unwrap()];
        assert_eq!(empty_evidence_ref.validate(), Err(DomainError::EmptyId));
    }

    #[test]
    fn fact_revision_constructs_and_binds_exact_claim_revision_and_authorization() {
        let revision = fact_revision_fixture();
        assert!(revision.validate().is_ok());
        assert_eq!(
            revision.claim_revision_refs(),
            &[ClaimRevisionRef::new("claim-revision-1").unwrap()]
        );
        assert_eq!(
            revision.authorization_decision_ref,
            AuthorizationDecisionRef::pending_i()
        );
        assert_eq!(revision.fact_ref().as_str(), "fact-1");
    }

    #[test]
    fn fact_revision_rejects_missing_method_scope_and_empty_references() {
        let mut missing_method = fact_revision_fixture();
        missing_method.attestation_method_id.clear();
        assert_eq!(
            missing_method.validate(),
            Err(DomainError::EmptyRequiredField("attestation_method_id"))
        );

        let mut missing_method_version = fact_revision_fixture();
        missing_method_version.attestation_method_version.clear();
        assert_eq!(
            missing_method_version.validate(),
            Err(DomainError::EmptyRequiredField(
                "attestation_method_version"
            ))
        );

        let mut missing_scope = fact_revision_fixture();
        missing_scope.scope_ref.namespace_key.clear();
        assert_eq!(
            missing_scope.validate(),
            Err(DomainError::EmptyRequiredField("namespace_key"))
        );

        let mut empty_claim_reference = fact_revision_fixture();
        empty_claim_reference.claim_revision_refs = vec![serde_json::from_str("\"\"").unwrap()];
        assert_eq!(empty_claim_reference.validate(), Err(DomainError::EmptyId));

        // An empty authorization ID is no longer representable by this unit placeholder
        // (and there is no string constructor); the public pending value is covered separately.
        let mut missing_evidence = fact_revision_fixture();
        missing_evidence.evidence_refs.clear();
        assert_eq!(
            missing_evidence.validate(),
            Err(DomainError::MissingFactEvidence)
        );

        let mut missing_provenance = fact_revision_fixture();
        missing_provenance.provenance_refs.clear();
        assert_eq!(
            missing_provenance.validate(),
            Err(DomainError::MissingFactProvenance)
        );
    }

    #[test]
    fn fact_with_placeholder_attestor_validates_today() {
        let revision = fact_revision_fixture();
        assert_eq!(revision.attestor_ref, AttestorRef::pending_i());
        assert_eq!(
            revision.authorization_decision_ref,
            AuthorizationDecisionRef::pending_i()
        );
        assert_eq!(
            revision.canonical_commit_ref,
            CanonicalCommitRef::pending_d()
        );
        // Known temporary compromise: structural validation currently accepts the placeholders.
        assert!(revision.validate().is_ok());
    }

    #[test]
    fn all_macro_generated_refs_reject_empty_id() {
        // Exercise every type emitted by ref_ctor!, not only the four legacy refs.
        assert_eq!(ClaimRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(ClaimRevisionRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(FactRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(FactRevisionRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(EvidenceRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(ProvenanceRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(EntityRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(EventRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(ExternalSourceRef::new(""), Err(DomainError::EmptyId));
        assert_eq!(MemoryRef::new(""), Err(DomainError::EmptyId));
    }
}
