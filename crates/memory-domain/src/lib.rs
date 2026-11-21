//! Phase 1 canonical memory domain types.
//! 领域层保持纯 Rust、无存储/网络/LLM 依赖。

use std::collections::BTreeMap;

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
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
    MissingClaimRevision, MissingFactEvidence, MissingFactProvenance, MissingRevisionReason,
    MissingIdentityLineage, InvalidRelationEndpoint,
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
        if self.event_kind.is_empty() { return Err(DomainError::EmptyRequiredField("event_kind")); }
        if self.payload_ref.is_empty() { return Err(DomainError::EmptyRequiredField("payload_ref")); }
        if self.classification.is_empty() { return Err(DomainError::EmptyRequiredField("classification")); }
        if self.schema_version.is_empty() { return Err(DomainError::EmptyRequiredField("schema_version")); }
        if self.retention_class.is_empty() { return Err(DomainError::EmptyRequiredField("retention_class")); }
        if self.scope_refs.is_empty() { return Err(DomainError::EmptyRequiredField("scope_refs")); }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }
}

impl Claim {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.predicate.is_empty() { return Err(DomainError::EmptyRequiredField("predicate")); }
        if self.object_value.is_empty() { return Err(DomainError::EmptyRequiredField("object_value")); }
        if self.polarity.is_empty() { return Err(DomainError::EmptyRequiredField("polarity")); }
        if self.asserted_at.is_empty() { return Err(DomainError::EmptyRequiredField("asserted_at")); }
        if self.scope_refs.is_empty() { return Err(DomainError::EmptyRequiredField("scope_refs")); }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }
}

impl Memory {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.memory_kind.is_empty() { return Err(DomainError::EmptyRequiredField("memory_kind")); }
        if self.retention_class.is_empty() { return Err(DomainError::EmptyRequiredField("retention_class")); }
        if self.sensitivity.is_empty() { return Err(DomainError::EmptyRequiredField("sensitivity")); }
        if self.created_at.is_empty() { return Err(DomainError::EmptyRequiredField("created_at")); }
        if self.updated_at.is_empty() { return Err(DomainError::EmptyRequiredField("updated_at")); }
        if self.scope_refs.is_empty() { return Err(DomainError::EmptyRequiredField("scope_refs")); }
        self.scope_refs.iter().try_for_each(ScopeRef::validate)
    }
}

impl MemoryVersion {
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.version_number == 0 { return Err(DomainError::InvalidVersionNumber); }
        if self.created_at.is_empty() { return Err(DomainError::EmptyRequiredField("created_at")); }
        if self.author_kind.is_empty() { return Err(DomainError::EmptyRequiredField("author_kind")); }
        if self.change_reason.is_empty() { return Err(DomainError::EmptyRequiredField("change_reason")); }
        if self.content_digest.is_empty() { return Err(DomainError::EmptyRequiredField("content_digest")); }
        if self.schema_version.is_empty() { return Err(DomainError::EmptyRequiredField("schema_version")); }
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

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Provenance {
    pub provenance_id: OpaqueId,
    pub source_refs: Vec<OpaqueId>,
    pub derivation_kind: String,
    pub actor_ref: ActorRef,
    pub created_at: String,
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
    required.iter().all(|item| container.iter().any(|candidate| candidate == item))
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
                self.records.insert(key.to_owned(), payload_digest.to_owned());
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


#[doc="Claim and Fact references are intentionally incompatible.
```compile_fail
use memory_domain::{ClaimRef, FactRef};
let claim: ClaimRef = FactRef::new("f").unwrap();
```"]
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
impl $t { pub fn new(v: impl Into<String>) -> Result<Self, DomainError> { Ok(Self(OpaqueId::new(v)?)) } pub fn as_str(&self)->&str { self.0.as_str() } }
)*};}
ref_ctor!(ClaimRef,ClaimRevisionRef,FactRef,FactRevisionRef,EvidenceRef,ProvenanceRef);


#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct EntityRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct EventRef(OpaqueId);
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, Hash, PartialEq)]
pub struct ExternalSourceRef(OpaqueId);
ref_ctor!(EntityRef, EventRef, ExternalSourceRef);

/// NOT DEFINED: awaiting I. Placeholder only; security identity semantics are not inferred.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AttestorRef { _pending_i: () }
impl AttestorRef { pub const fn pending_i() -> Self { Self { _pending_i: () } } }
/// NOT DEFINED: awaiting I. Required placeholder; this is not an authorization grant.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionRef { _pending_i: () }
impl AuthorizationDecisionRef { pub const fn pending_i() -> Self { Self { _pending_i: () } } }
/// NOT DEFINED: awaiting D. Required placeholder with no invented commit semantics.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitRef { _pending_d: () }
impl CanonicalCommitRef { pub const fn pending_d() -> Self { Self { _pending_d: () } } }

#[doc="Immutable revision fields are private; corrections append successors.
```compile_fail
use memory_domain::{ClaimRevision, ClaimRef, ClaimRevisionRef, EpistemicStatus, TimeValue};
let mut r=ClaimRevision::new(ClaimRevisionRef::new("r").unwrap(),ClaimRef::new("c").unwrap(),None,"s".into(),"p".into(),"o".into(),"+".into(),vec![],EpistemicStatus::Observed,TimeValue::Unknown,vec![],vec![],"t".into(),"initial".into()).unwrap();
r.predicate=String::from("mutated");
```"]
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct ClaimRevision {
    revision_ref: ClaimRevisionRef, claim_ref: ClaimRef, parent_revision_ref: Option<ClaimRevisionRef>,
    subject: String, predicate: String, object: String, polarity: String, qualifiers: Vec<String>,
    epistemic_status: EpistemicStatus, valid_time: TimeValue, evidence_refs: Vec<EvidenceRef>,
    provenance_refs: Vec<ProvenanceRef>, asserted_at: String, revision_reason: String,
}
impl ClaimRevision {
    #[allow(clippy::too_many_arguments)]
    pub fn new(revision_ref: ClaimRevisionRef, claim_ref: ClaimRef, parent: Option<&ClaimRevision>,
        subject: String, predicate: String, object: String, polarity: String, qualifiers: Vec<String>,
        epistemic_status: EpistemicStatus, valid_time: TimeValue, evidence_refs: Vec<EvidenceRef>,
        provenance_refs: Vec<ProvenanceRef>, asserted_at: String, revision_reason: String) -> Result<Self, DomainError> {
        let parent_revision_ref = parent.map(|p| p.revision_ref.clone());
        if let Some(p) = parent { if p.claim_ref != claim_ref { return Err(DomainError::InvalidParent); } }
        let value = Self { revision_ref, claim_ref, parent_revision_ref, subject, predicate, object, polarity,
            qualifiers, epistemic_status, valid_time, evidence_refs, provenance_refs, asserted_at, revision_reason };
        value.validate()?; Ok(value)
    }
    pub fn validate(&self) -> Result<(), DomainError> {
        for (field, value) in [("subject",&self.subject),("predicate",&self.predicate),("object",&self.object),
            ("polarity",&self.polarity),("asserted_at",&self.asserted_at),("revision_reason",&self.revision_reason)] {
            if value.is_empty() { return Err(DomainError::EmptyRequiredField(field)); }
        }
        Ok(())
    }
    pub fn revision_ref(&self)->&ClaimRevisionRef { &self.revision_ref }
    pub fn claim_ref(&self)->&ClaimRef { &self.claim_ref }
    pub fn parent_revision_ref(&self)->Option<&ClaimRevisionRef> { self.parent_revision_ref.as_ref() }
    pub fn predicate(&self)->&str { &self.predicate }
    pub fn evidence_refs(&self)->&[EvidenceRef] { &self.evidence_refs }
    pub fn provenance_refs(&self)->&[ProvenanceRef] { &self.provenance_refs }
}

#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct Fact { fact_ref: FactRef, initial_revision: Box<FactRevision> }
impl Fact {
    pub fn new(fact_ref: FactRef, initial_revision: FactRevision) -> Result<Self, DomainError> {
        if initial_revision.fact_ref != fact_ref || initial_revision.parent_revision_ref.is_some() {
            return Err(DomainError::InvalidParent);
        }
        Ok(Self { fact_ref, initial_revision: Box::new(initial_revision) })
    }
    pub fn fact_ref(&self)->&FactRef { &self.fact_ref }
    pub fn initial_revision(&self)->&FactRevision { &self.initial_revision }
}
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum FactOutcome { Attested, Corrected, Revoked, Withdrawn }
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct FactRevision {
    fact_ref: FactRef, revision_ref: FactRevisionRef, parent_revision_ref: Option<FactRevisionRef>,
    claim_revision_refs: Vec<ClaimRevisionRef>, evidence_refs: Vec<EvidenceRef>, provenance_refs: Vec<ProvenanceRef>,
    scope_ref: ScopeRef, attestor_ref: AttestorRef, authorization_decision_ref: AuthorizationDecisionRef,
    attestation_method_id: String, attestation_method_version: String, outcome: FactOutcome, rationale: String,
    canonical_commit_ref: CanonicalCommitRef, correction_or_revocation_reason: Option<String>,
}
impl FactRevision {
    #[allow(clippy::too_many_arguments)]
    pub fn new(fact_ref: FactRef, revision_ref: FactRevisionRef, parent_revision_ref: Option<FactRevisionRef>,
        claim_revision_refs: Vec<ClaimRevisionRef>, evidence_refs: Vec<EvidenceRef>, provenance_refs: Vec<ProvenanceRef>,
        scope_ref: ScopeRef, attestor_ref: AttestorRef, authorization_decision_ref: AuthorizationDecisionRef,
        attestation_method_id: String, attestation_method_version: String, outcome: FactOutcome, rationale: String,
        canonical_commit_ref: CanonicalCommitRef, correction_or_revocation_reason: Option<String>) -> Result<Self, DomainError> {
        let value=Self { fact_ref, revision_ref, parent_revision_ref, claim_revision_refs, evidence_refs, provenance_refs,
            scope_ref, attestor_ref, authorization_decision_ref, attestation_method_id, attestation_method_version,
            outcome, rationale, canonical_commit_ref, correction_or_revocation_reason };
        value.validate()?; Ok(value)
    }
    pub fn validate(&self)->Result<(),DomainError> {
        if self.claim_revision_refs.is_empty(){return Err(DomainError::MissingClaimRevision)}
        if self.evidence_refs.is_empty(){return Err(DomainError::MissingFactEvidence)}
        if self.provenance_refs.is_empty(){return Err(DomainError::MissingFactProvenance)}
        self.scope_ref.validate()?;
        for (n,v) in [("attestation_method_id",&self.attestation_method_id),("attestation_method_version",&self.attestation_method_version),("rationale",&self.rationale)] {
            if v.is_empty(){return Err(DomainError::EmptyRequiredField(n))}
        }
        if (self.parent_revision_ref.is_some() || matches!(self.outcome, FactOutcome::Corrected | FactOutcome::Revoked | FactOutcome::Withdrawn)) && self.correction_or_revocation_reason.as_deref().unwrap_or("").is_empty(){return Err(DomainError::MissingRevisionReason)}
        Ok(())
    }
    pub fn fact_ref(&self)->&FactRef { &self.fact_ref }
    pub fn revision_ref(&self)->&FactRevisionRef { &self.revision_ref }
    pub fn claim_revision_refs(&self)->&[ClaimRevisionRef] { &self.claim_revision_refs }
    pub fn evidence_refs(&self)->&[EvidenceRef] { &self.evidence_refs }
    pub fn provenance_refs(&self)->&[ProvenanceRef] { &self.provenance_refs }
}


#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum EntityIdentityStatus { Provisional, Resolved, Merged, Split, Retired }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct EntityAlias { pub value:String, pub language:Option<String> }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct ScopedExternalIdentifier { pub namespace:String, pub value:String, pub scope_ref:ScopeRef }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct EntityMergeLineage { pub predecessor_refs:Vec<EntityRef>, pub successor_ref:EntityRef, pub reason:String }
/// Sidecar keeps Phase 1 Entity struct literals source-compatible.
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct EntityIdentityExtension {
 pub entity_ref:EntityRef, pub status:EntityIdentityStatus, pub aliases:Vec<EntityAlias>,
 pub external_identifiers:Vec<ScopedExternalIdentifier>, pub merge_lineage:Option<EntityMergeLineage>,
 pub split_successor_refs:Vec<EntityRef>
}
impl EntityIdentityExtension {
 pub fn validate(&self)->Result<(),DomainError>{
  if self.aliases.iter().any(|a|a.value.is_empty()){return Err(DomainError::EmptyRequiredField("alias"))}
  if self.external_identifiers.iter().any(|i|i.namespace.is_empty()||i.value.is_empty()){return Err(DomainError::EmptyRequiredField("external_identifier"))}
  if self.status==EntityIdentityStatus::Merged {let l=self.merge_lineage.as_ref().ok_or(DomainError::MissingIdentityLineage)?;
   if l.successor_ref==self.entity_ref||l.predecessor_refs.is_empty()||l.reason.is_empty(){return Err(DomainError::MissingIdentityLineage)}}
  if self.status==EntityIdentityStatus::Split&&self.split_successor_refs.is_empty(){return Err(DomainError::MissingIdentityLineage)}
  Ok(())
 }
 pub fn add_alias(&mut self,a:EntityAlias)->Result<(),DomainError>{if a.value.is_empty(){return Err(DomainError::EmptyRequiredField("alias"))}self.aliases.push(a);Ok(())}
}
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum RelationEndpoint { Entity(EntityRef), Claim(ClaimRef), Fact(FactRef) }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum RelationEndpointKind { Entity, Claim, Fact }
impl RelationEndpoint { pub fn kind(&self)->RelationEndpointKind {match self{Self::Entity(_)=>RelationEndpointKind::Entity,Self::Claim(_)=>RelationEndpointKind::Claim,Self::Fact(_)=>RelationEndpointKind::Fact}} }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum RelationDirectionality { Directed, Undirected, Symmetric }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum RelationLifecycleState { Proposed, Active, Superseded, Retracted }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum ValidTimeRef { Unknown, Bounded(TimeValue), AllTime }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct RelationDefinition { pub relation_type:String, pub allowed_subject_kinds:Vec<RelationEndpointKind>, pub allowed_object_kinds:Vec<RelationEndpointKind> }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct RelationExtension {
 pub subject:RelationEndpoint, pub object:RelationEndpoint, pub directionality:RelationDirectionality,
 pub qualifiers:Vec<String>, pub valid_time:Option<ValidTimeRef>, pub epistemic_status:EpistemicStatus,
 pub evidence_refs:Vec<EvidenceRef>, pub lifecycle_state:RelationLifecycleState
}
impl RelationExtension {
 /// Registry-dependent endpoint compatibility cannot be expressed in static Rust types.
 pub fn validate(&self,d:&RelationDefinition)->Result<(),DomainError>{
  if !d.allowed_subject_kinds.contains(&self.subject.kind())||!d.allowed_object_kinds.contains(&self.object.kind()){return Err(DomainError::InvalidRelationEndpoint)}
  if d.relation_type.is_empty(){return Err(DomainError::EmptyRequiredField("relation_type"))} Ok(())
 }
 pub fn valid_time_or_unknown(&self)->ValidTimeRef{self.valid_time.clone().unwrap_or(ValidTimeRef::Unknown)}
}
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum EvidenceKind { Document, Message, Observation, Record, Dataset, Other(String) }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum EvidenceSourceRef { Event(EventRef), Memory(OpaqueId), External(ExternalSourceRef) }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub enum EvidenceAvailability { Available, Restricted, Unavailable, Forgotten }
#[derive(serde::Serialize,serde::Deserialize,Clone,Debug,Eq,PartialEq)]
pub struct EvidenceExtension {
 pub evidence_ref:EvidenceRef, pub kind:EvidenceKind, pub source_ref:EvidenceSourceRef, pub locator:Option<String>,
 pub observed_at:Option<TimeValue>, pub collector:ActorRef, pub integrity_digest:String,
 pub availability:EvidenceAvailability, pub scope_refs:Vec<ScopeRef>
}
impl EvidenceExtension { pub fn validate(&self)->Result<(),DomainError>{
 if self.integrity_digest.is_empty(){return Err(DomainError::EmptyRequiredField("integrity_digest"))}
 if self.scope_refs.is_empty(){return Err(DomainError::EmptyRequiredField("scope_refs"))}
 self.scope_refs.iter().try_for_each(ScopeRef::validate)
}}


    #[test]
    fn dm2_01_claim_revision_parent_must_belong_to_same_claim() {
        let ca=ClaimRef::new("ca").unwrap(); let cb=ClaimRef::new("cb").unwrap();
        let parent=ClaimRevision::new(ClaimRevisionRef::new("r1").unwrap(),ca.clone(),None,"s".into(),"p".into(),"o".into(),"+".into(),vec![],EpistemicStatus::Observed,TimeValue::Unknown,vec![],vec![],"t1".into(),"initial".into()).unwrap();
        let bad=ClaimRevision::new(ClaimRevisionRef::new("r2").unwrap(),cb,Some(&parent),"s".into(),"p".into(),"o".into(),"+".into(),vec![],EpistemicStatus::Observed,TimeValue::Unknown,vec![],vec![],"t2".into(),"correction".into()).unwrap();
        assert_eq!(bad.validate(),Err(DomainError::InvalidParent));
    }
    #[test]
    fn dm2_02_claim_revision_is_append_only_and_immutable() {
        let first=ClaimRevision::new(ClaimRevisionRef::new("r1").unwrap(),ClaimRef::new("c").unwrap(),None,"s".into(),"p".into(),"old".into(),"+".into(),vec![],EpistemicStatus::Observed,TimeValue::Unknown,vec![],vec![],"t1".into(),"initial".into()).unwrap();
        let next=ClaimRevision::new(ClaimRevisionRef::new("r2").unwrap(),first.claim_ref().clone(),Some(&first),"s".into(),"p".into(),"new".into(),"+".into(),vec![],EpistemicStatus::Observed,TimeValue::Unknown,vec![],vec![],"t2".into(),"correction".into()).unwrap();
        assert_eq!(first.predicate(),"p"); assert_eq!(next.parent_revision_ref(),Some(first.revision_ref()));
    }
    #[test]
    fn dm2_03_fact_refs_are_distinct_and_fact_pins_exact_claim_revision() {
        let pinned=ClaimRevisionRef::new("cr1").unwrap(); let fact_ref=FactRef::new("f").unwrap();
        let rev=FactRevision::new(fact_ref.clone(),FactRevisionRef::new("fr1").unwrap(),None,vec![pinned.clone()],vec![EvidenceRef::new("e").unwrap()],vec![ProvenanceRef::new("p").unwrap()],scope("s"),AttestorRef::pending_i(),AuthorizationDecisionRef::pending_i(),"method".into(),"v1".into(),FactOutcome::Attested,"reason".into(),CanonicalCommitRef::pending_d(),None).unwrap();
        let fact=Fact::new(fact_ref,rev).unwrap(); let _head=ClaimRevisionRef::new("cr2").unwrap(); assert_eq!(fact.initial_revision().claim_revision_refs(),&[pinned]);
    }
    #[test]
    fn dm2_04_fact_cannot_be_constructed_without_claim_evidence_provenance() {
        let r=FactRevision::new(FactRef::new("f").unwrap(),FactRevisionRef::new("fr").unwrap(),None,vec![],vec![],vec![],scope("s"),AttestorRef::pending_i(),AuthorizationDecisionRef::pending_i(),"m".into(),"v1".into(),FactOutcome::Attested,"why".into(),CanonicalCommitRef::pending_d(),None);
        assert_eq!(r.unwrap_err(),DomainError::MissingClaimRevision);
    }
    #[test]
    fn dm2_05_entity_merge_requires_successor_lineage_but_alias_does_not() {
        let mut e=EntityIdentityExtension{entity_ref:EntityRef::new("e1").unwrap(),status:EntityIdentityStatus::Resolved,aliases:vec![],external_identifiers:vec![],merge_lineage:None,split_successor_refs:vec![]};
        e.add_alias(EntityAlias{value:"label".into(),language:None}).unwrap(); assert!(e.validate().is_ok());
        e.status=EntityIdentityStatus::Merged; assert_eq!(e.validate(),Err(DomainError::MissingIdentityLineage));
        e.merge_lineage=Some(EntityMergeLineage{predecessor_refs:vec![EntityRef::new("e0").unwrap()],successor_ref:EntityRef::new("e2").unwrap(),reason:"resolved".into()}); assert!(e.validate().is_ok());
    }
    #[test]
    fn dm2_06_relation_endpoint_kind_is_checked_against_definition() {
        let r=RelationExtension{subject:RelationEndpoint::Entity(EntityRef::new("e").unwrap()),object:RelationEndpoint::Claim(ClaimRef::new("c").unwrap()),directionality:RelationDirectionality::Directed,qualifiers:vec![],valid_time:None,epistemic_status:EpistemicStatus::Observed,evidence_refs:vec![],lifecycle_state:RelationLifecycleState::Proposed};
        let d=RelationDefinition{relation_type:"owns".into(),allowed_subject_kinds:vec![RelationEndpointKind::Entity],allowed_object_kinds:vec![RelationEndpointKind::Entity]};
        assert_eq!(r.validate(&d),Err(DomainError::InvalidRelationEndpoint));
    }
    #[test]
    fn dm2_07_evidence_extension_requires_integrity_and_scope() {
        let e=EvidenceExtension{evidence_ref:EvidenceRef::new("e").unwrap(),kind:EvidenceKind::Document,source_ref:EvidenceSourceRef::Event(EventRef::new("ev").unwrap()),locator:None,observed_at:None,collector:ActorRef{actor_id:id("collector")},integrity_digest:"sha256:x".into(),availability:EvidenceAvailability::Available,scope_refs:vec![scope("s")]};
        assert!(e.validate().is_ok());
    }
    #[test]
    fn dm2_08_unknown_valid_time_is_not_timeless() {
        let r=RelationExtension{subject:RelationEndpoint::Entity(EntityRef::new("e").unwrap()),object:RelationEndpoint::Entity(EntityRef::new("e2").unwrap()),directionality:RelationDirectionality::Directed,qualifiers:vec![],valid_time:None,epistemic_status:EpistemicStatus::Observed,evidence_refs:vec![],lifecycle_state:RelationLifecycleState::Active};
        assert_eq!(r.valid_time_or_unknown(),ValidTimeRef::Unknown); assert_ne!(r.valid_time_or_unknown(),ValidTimeRef::AllTime);
    }

#[cfg(test)]
mod tests {
    use super::*;

    fn id(value: &str) -> OpaqueId {
        OpaqueId::new(value).unwrap()
    }

    fn scope(value: &str) -> ScopeRef {
        ScopeRef { scope_id: id(value), scope_kind: ScopeKind::User, namespace_key: format!("user:{value}") }
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
        assert_eq!(stale.validate_successor(&current), Err(DomainError::InvalidParent));
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
            actor_ref: ActorRef { actor_id: id("actor") },
            created_at: "now".into(),
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

        assert!(scopes_intersect(&[canonical.clone()], &[canonical.clone()]));
        assert!(!scopes_intersect(&[canonical.clone()], &[other_namespace]));
        assert!(!scopes_intersect(&[canonical], &[other_kind]));
    }

}
