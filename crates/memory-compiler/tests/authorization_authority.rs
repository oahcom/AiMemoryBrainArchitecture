use memory_compiler::admission::{AdmissionStore, AuthorizationDecisionValidationError};
use memory_domain::{
    AuthorizationDecisionKind, AuthorizationDecisionRef, IssuerId, OpaqueId, I_DEV_BASELINE_ISSUER,
};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn issued_authorization_store(
    kind: AuthorizationDecisionKind,
) -> (AdmissionStore, AuthorizationDecisionRef, OpaqueId) {
    let mut db = AdmissionStore::in_memory().unwrap();

    let decision_id = id("authorization-decision-integration");
    let issuer = IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap();
    let subject = OpaqueId::new("a".repeat(64)).unwrap();

    let reference = db
        .issue_authorization_decision(
            &decision_id,
            &issuer,
            &subject,
            "2026-11-22T00:00:00Z",
            kind,
        )
        .unwrap();

    (db, reference, subject)
}

#[test]
fn pending_reference_propagates_authority_validation_error() {
    let db = AdmissionStore::in_memory().unwrap();
    let pending = AuthorizationDecisionRef::pending_i();
    let subject = OpaqueId::new("a".repeat(64)).unwrap();

    assert_eq!(
        db.validate_authorization_decision(&pending, &subject),
        Err(AuthorizationDecisionValidationError::PendingReference)
    );
}

#[test]
fn issued_reference_without_durable_row_propagates_record_missing() {
    let db = AdmissionStore::in_memory().unwrap();
    let missing = AuthorizationDecisionRef::issued(id("authorization-never-issued"));
    let subject = OpaqueId::new("a".repeat(64)).unwrap();

    assert_eq!(
        db.validate_authorization_decision(&missing, &subject),
        Err(AuthorizationDecisionValidationError::RecordMissing)
    );
}

#[test]
fn durable_approved_decision_validates_and_reports_approved_kind() {
    let (db, reference, subject) = issued_authorization_store(AuthorizationDecisionKind::Approved);

    assert_eq!(
        db.validate_authorization_decision(&reference, &subject),
        Ok(true)
    );

    assert_eq!(
        db.authorization_decision_kind(&reference),
        Ok(AuthorizationDecisionKind::Approved)
    );
}

#[test]
fn durable_denied_decision_is_validly_recorded_but_is_not_approved() {
    let (db, reference, subject) = issued_authorization_store(AuthorizationDecisionKind::Denied);

    assert_eq!(
        db.validate_authorization_decision(&reference, &subject),
        Ok(true)
    );

    let kind = db.authorization_decision_kind(&reference).unwrap();

    assert_eq!(kind, AuthorizationDecisionKind::Denied);
    assert_ne!(kind, AuthorizationDecisionKind::Approved);
}

#[test]
fn matching_reference_with_different_expected_digest_returns_false() {
    let (db, reference, _) = issued_authorization_store(AuthorizationDecisionKind::Approved);

    let other_subject = OpaqueId::new("b".repeat(64)).unwrap();

    assert_eq!(
        db.validate_authorization_decision(&reference, &other_subject),
        Ok(false)
    );
}
