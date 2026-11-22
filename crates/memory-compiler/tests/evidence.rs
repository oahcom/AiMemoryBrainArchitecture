//! MC-03 Evidence Manager acceptance tests.
//!
//! Tests target the registry contract and domain validation boundary.
//! Each test asserts an externally observable behavior that must fail if the
//! corresponding invariant is removed or reverted.

use memory_compiler::evidence::{
    AttachmentDecision, EvidenceEntry, EvidenceRegistry, EvidenceRejection, RegistrationOutcome,
};
use memory_domain::{
    ActorRef, DomainError, EventRef, Evidence, EvidenceAvailability, EvidenceExtension,
    EvidenceKind, EvidenceRef, EvidenceRole, EvidenceSourceRef, OpaqueId, ScopeKind, ScopeRef,
};

// ---------------------------------------------------------------------------
// Fixtures

fn oid(value: &str) -> OpaqueId {
    OpaqueId::new(value).expect("valid id")
}

fn scope(id: &str) -> ScopeRef {
    ScopeRef {
        scope_id: oid(id),
        scope_kind: ScopeKind::User,
        namespace_key: format!("ns-{id}"),
    }
}

fn entry(
    id: &str,
    role: EvidenceRole,
    availability: EvidenceAvailability,
    scopes: Vec<ScopeRef>,
) -> EvidenceEntry {
    EvidenceEntry {
        evidence: Evidence {
            evidence_id: oid(id),
            source_ref: oid(&format!("source-{id}")),
            recorded_at: "2026-01-01T00:00:00Z".into(),
            scope_refs: scopes,
            role,
        },
        extension: EvidenceExtension {
            evidence_ref: EvidenceRef::new(id).expect("valid evidence ref"),
            kind: EvidenceKind::Document,
            source_ref: EvidenceSourceRef::Event(
                EventRef::new(format!("src-{id}")).expect("valid event ref"),
            ),
            locator: Some("page=1".into()),
            observed_at: None,
            collector: ActorRef {
                actor_id: oid("collector-1"),
            },
            integrity_digest: Some("a".repeat(64)),
            source_reliability_ref: None,
            availability,
        },
    }
}

fn available(id: &str) -> EvidenceEntry {
    entry(
        id,
        EvidenceRole::Supports,
        EvidenceAvailability::Available,
        vec![scope("user-1")],
    )
}

fn register(registry: &mut EvidenceRegistry, entry: EvidenceEntry) -> RegistrationOutcome {
    registry.register_evidence(entry.evidence, entry.extension)
}

// ---------------------------------------------------------------------------
// Domain Evidence validation

#[test]
fn evidence_rejects_blank_recorded_at() {
    let mut record = available("ev-1");
    record.evidence.recorded_at = "   ".into();

    assert_eq!(
        record.evidence.validate(),
        Err(DomainError::EmptyRequiredField("recorded_at")),
        "recorded_at is required and whitespace is not a value"
    );
}

#[test]
fn evidence_rejects_empty_scope_refs() {
    let mut record = available("ev-1");
    record.evidence.scope_refs.clear();

    assert_eq!(
        record.evidence.validate(),
        Err(DomainError::EmptyRequiredField("scope_refs")),
        "Evidence must carry its authoritative scope set"
    );
}

#[test]
fn evidence_rejects_invalid_scope_ref() {
    let mut record = available("ev-1");
    record.evidence.scope_refs[0].namespace_key.clear();

    assert_eq!(
        record.evidence.validate(),
        Err(DomainError::EmptyRequiredField("namespace_key")),
        "each Evidence scope reference must validate"
    );
}

#[test]
fn evidence_extension_accepts_absent_integrity_digest() {
    let mut record = available("ev-1");
    record.extension.integrity_digest = None;

    assert_eq!(
        record.extension.validate(),
        Ok(()),
        "integrity_digest is nullable in the domain contract"
    );
}

#[test]
fn evidence_extension_rejects_blank_present_integrity_digest() {
    let mut record = available("ev-1");
    record.extension.integrity_digest = Some("   ".into());

    assert_eq!(
        record.extension.validate(),
        Err(DomainError::EmptyRequiredField("integrity_digest")),
        "a present digest must not be blank"
    );
}

#[test]
fn evidence_and_extension_must_have_the_same_identity() {
    let mut record = available("ev-1");
    record.extension.evidence_ref = EvidenceRef::new("ev-other").unwrap();

    assert_eq!(
        record.evidence.validate_against(&record.extension),
        Err(DomainError::InvalidParent),
        "the extension must refer to the Evidence identity it extends"
    );
}

#[test]
fn registry_rejects_evidence_extension_identity_mismatch() {
    let mut registry = EvidenceRegistry::new();
    let mut record = available("ev-1");
    record.extension.evidence_ref = EvidenceRef::new("ev-other").unwrap();

    assert_eq!(
        register(&mut registry, record),
        RegistrationOutcome::Rejected(EvidenceRejection::InvalidRecord(DomainError::InvalidParent)),
        "invalid pairs must not enter the registry"
    );
    assert_eq!(registry.evidence_count(), 0);
}

// ---------------------------------------------------------------------------
// Registration identity and idempotency

#[test]
fn registering_the_same_evidence_twice_is_idempotent() {
    let mut registry = EvidenceRegistry::new();
    let record = available("ev-1");

    assert_eq!(
        register(&mut registry, record.clone()),
        RegistrationOutcome::Registered
    );
    assert_eq!(
        register(&mut registry, record),
        RegistrationOutcome::AlreadyPresent,
        "same identity and same content must be idempotent"
    );
    assert_eq!(registry.evidence_count(), 1);
}

#[test]
fn same_identity_with_different_content_is_refused_not_overwritten() {
    let mut registry = EvidenceRegistry::new();
    assert_eq!(
        register(&mut registry, available("ev-1")),
        RegistrationOutcome::Registered
    );

    let mut conflicting = available("ev-1");
    conflicting.extension.integrity_digest = Some("c".repeat(64));

    assert_eq!(
        register(&mut registry, conflicting),
        RegistrationOutcome::Rejected(EvidenceRejection::IdentityConflict {
            evidence_id: oid("ev-1"),
        }),
        "different content under the same identity is a conflict"
    );

    let stored = registry
        .get_evidence(&oid("ev-1"))
        .expect("original registration remains present");
    assert_eq!(
        stored.extension.integrity_digest,
        Some("a".repeat(64)),
        "the first registration must survive: no silent overwrite"
    );
}

#[test]
fn registry_uses_evidence_id_as_its_lookup_identity() {
    let mut registry = EvidenceRegistry::new();
    register(&mut registry, available("ev-1"));

    assert!(registry.contains_evidence(&oid("ev-1")));
    assert!(!registry.contains_evidence(&oid("ghost")));
    assert_eq!(
        registry
            .get_evidence(&oid("ev-1"))
            .unwrap()
            .evidence
            .evidence_id,
        oid("ev-1")
    );
}

// ---------------------------------------------------------------------------
// Availability and attachment decisions

#[test]
fn unavailable_evidence_defers_attachment_with_its_reason() {
    let mut registry = EvidenceRegistry::new();
    register(
        &mut registry,
        entry(
            "ev-1",
            EvidenceRole::Supports,
            EvidenceAvailability::Unavailable,
            vec![scope("user-1")],
        ),
    );

    match registry.attachment_decision(&oid("ev-1")) {
        AttachmentDecision::Defer { reason } => assert!(
            reason.contains("unavailable"),
            "the blocking state must survive: {reason}"
        ),
        other => panic!("unavailable evidence must not attach, got {other:?}"),
    }
}

#[test]
fn forgotten_evidence_defers_attachment_with_its_reason() {
    let mut registry = EvidenceRegistry::new();
    register(
        &mut registry,
        entry(
            "ev-1",
            EvidenceRole::Supports,
            EvidenceAvailability::Forgotten,
            vec![scope("user-1")],
        ),
    );

    match registry.attachment_decision(&oid("ev-1")) {
        AttachmentDecision::Defer { reason } => assert!(
            reason.contains("forgotten"),
            "the blocking state must survive: {reason}"
        ),
        other => panic!("forgotten evidence must not attach, got {other:?}"),
    }
}

#[test]
fn restricted_evidence_defers_attachment_with_its_reason() {
    let mut registry = EvidenceRegistry::new();
    register(
        &mut registry,
        entry(
            "ev-1",
            EvidenceRole::Supports,
            EvidenceAvailability::Restricted,
            vec![scope("user-1")],
        ),
    );

    match registry.attachment_decision(&oid("ev-1")) {
        AttachmentDecision::Defer { reason } => assert!(
            reason.contains("restricted"),
            "the blocking state must survive: {reason}"
        ),
        other => panic!("restricted evidence must not attach, got {other:?}"),
    }
}

#[test]
fn available_evidence_attaches() {
    let mut registry = EvidenceRegistry::new();
    register(&mut registry, available("ev-1"));

    assert_eq!(
        registry.attachment_decision(&oid("ev-1")),
        AttachmentDecision::Attach
    );
}

#[test]
fn unknown_evidence_is_not_silently_attached() {
    let registry = EvidenceRegistry::new();

    assert_eq!(
        registry.attachment_decision(&oid("ghost")),
        AttachmentDecision::UnknownEvidence {
            evidence_id: oid("ghost"),
        },
        "absent evidence is unknown, not available"
    );
}

// ---------------------------------------------------------------------------
// Scope ownership

#[test]
fn evidence_scope_is_validated_on_the_domain_record() {
    let mut registry = EvidenceRegistry::new();
    let mut record = available("ev-1");
    record.evidence.scope_refs.clear();

    assert_eq!(
        register(&mut registry, record),
        RegistrationOutcome::Rejected(EvidenceRejection::InvalidRecord(
            DomainError::EmptyRequiredField("scope_refs")
        )),
        "scope validation belongs to Evidence, not an independent registry filter"
    );
    assert_eq!(registry.evidence_count(), 0);
}
