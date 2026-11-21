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

        assert!(scopes_intersect(std::slice::from_ref(&canonical), std::slice::from_ref(&canonical)));
        assert!(!scopes_intersect(std::slice::from_ref(&canonical), &[other_namespace]));
        assert!(!scopes_intersect(&[canonical], &[other_kind]));
    }

}
