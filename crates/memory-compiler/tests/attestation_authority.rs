//! Durable attestation validation, exercised against a real SQLite store.
//!
//! The decision side already has this file's counterpart
//! (`authorization_authority.rs`). This one exists because `i_attestations` had a
//! table and no reader: every assertion below fails on `main` with
//! `issue_attestation` not existing, which is the point — the table being present
//! was never evidence that the attestor half of GAP-18 was implemented.

use memory_compiler::admission::{AdmissionStore, AttestationValidationError};
use memory_domain::{
    AttestorData, IssuedAttestorRef, IssuerId, OpaqueId, I_DEV_BASELINE_ATTESTOR,
    I_DEV_BASELINE_ISSUER,
};

fn id(value: &str) -> OpaqueId {
    OpaqueId::new(value).unwrap()
}

fn digest() -> OpaqueId {
    OpaqueId::new("a".repeat(64)).unwrap()
}

fn issued_store() -> (AdmissionStore, IssuedAttestorRef, OpaqueId) {
    let mut db = AdmissionStore::in_memory().unwrap();

    let attestation_id = id("attestation-integration");
    let issuer = IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap();
    let subject = digest();

    let reference = db
        .issue_attestation(&attestation_id, &issuer, &subject, "2026-11-22T00:00:00Z")
        .unwrap();

    (db, reference, subject)
}

#[test]
fn a_pending_reference_is_not_a_validation_failure_of_authority() {
    // A placeholder must be refused before any row is consulted, so the caller
    // cannot mistake "no attestation claimed" for "attestation rejected".
    let db = AdmissionStore::in_memory().unwrap();
    let pending = IssuedAttestorRef::pending_i();

    assert_eq!(
        db.validate_attestation(&pending, &digest()),
        Err(AttestationValidationError::PendingReference)
    );
}

#[test]
fn an_absent_reference_is_refused_the_same_way_as_pending() {
    // `Absent` and `PendingI` both carry no data. `#662` maps both to
    // `PendingReference` on the decision side; this pins the same choice here so
    // the two paths do not drift.
    let db = AdmissionStore::in_memory().unwrap();

    assert_eq!(
        db.validate_attestation(&IssuedAttestorRef::absent(), &digest()),
        Err(AttestationValidationError::PendingReference)
    );
}

#[test]
fn an_issued_reference_without_a_durable_row_is_record_missing_not_false() {
    // The whole reason this returns an enum rather than a bool. An unbacked
    // reference is an error, never a negative answer.
    let db = AdmissionStore::in_memory().unwrap();
    let unbacked = IssuedAttestorRef::from_issued_data(AttestorData {
        attestation_id: id("never-written"),
        issuer: IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap(),
        subject_digest: digest(),
        issued_at: "2026-11-22T00:00:00Z".into(),
    });

    assert_eq!(
        db.validate_attestation(&unbacked, &digest()),
        Err(AttestationValidationError::RecordMissing)
    );
}

#[test]
fn issue_then_validate_against_the_same_digest_is_true() {
    let (db, reference, subject) = issued_store();

    assert_eq!(db.validate_attestation(&reference, &subject), Ok(true));
}

#[test]
fn issue_then_validate_against_a_different_digest_is_false_not_err() {
    // The row is readable and every reference field matches it, so the answer is
    // a negative decision, not a missing record. If this collapsed into `Err`,
    // a caller could not tell "attestation exists but does not cover this
    // subject" from "no attestation was ever issued".
    let (db, reference, _) = issued_store();
    let other = OpaqueId::new("b".repeat(64)).unwrap();

    assert_eq!(db.validate_attestation(&reference, &other), Ok(false));
}

#[test]
fn the_decision_issuer_cannot_mint_an_attestation() {
    // `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER` §5: the separation of issuer
    // namespaces is the point. If this were accepted, one compromised issuer
    // string would cover both tables.
    let mut db = AdmissionStore::in_memory().unwrap();
    let decision_issuer = IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap();

    let result = db.issue_attestation(
        &id("attestation-wrong-issuer"),
        &decision_issuer,
        &digest(),
        "2026-11-22T00:00:00Z",
    );

    assert!(
        result.is_err(),
        "decision issuer must not issue attestations"
    );
}

#[test]
fn a_malformed_digest_is_refused_at_issuance() {
    let mut db = AdmissionStore::in_memory().unwrap();
    let issuer = IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap();

    let result = db.issue_attestation(
        &id("attestation-short-digest"),
        &issuer,
        &id("abc"),
        "2026-11-22T00:00:00Z",
    );

    assert!(result.is_err(), "a short digest is not canonical");
}

#[test]
fn a_non_utc_timestamp_is_refused_at_issuance() {
    let mut db = AdmissionStore::in_memory().unwrap();
    let issuer = IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap();

    let result = db.issue_attestation(
        &id("attestation-bad-time"),
        &issuer,
        &digest(),
        "2026-11-22 00:00:00",
    );

    assert!(result.is_err(), "a non-UTC timestamp is not canonical");
}

#[test]
fn an_identical_replay_succeeds() {
    let mut db = AdmissionStore::in_memory().unwrap();
    let attestation_id = id("attestation-replay");
    let issuer = IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap();
    let subject = digest();

    let first = db
        .issue_attestation(&attestation_id, &issuer, &subject, "2026-11-22T00:00:00Z")
        .unwrap();
    let second = db
        .issue_attestation(&attestation_id, &issuer, &subject, "2026-11-22T00:00:00Z")
        .unwrap();

    assert_eq!(first, second);
    assert_eq!(db.validate_attestation(&second, &subject), Ok(true));
}

#[test]
fn a_differing_replay_is_an_idempotency_conflict() {
    // A retry must not silently overwrite a recorded attestation. Same primary
    // key with different content is a conflict, matching the decision writer.
    let mut db = AdmissionStore::in_memory().unwrap();
    let attestation_id = id("attestation-conflict");
    let issuer = IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap();
    let subject = digest();

    db.issue_attestation(&attestation_id, &issuer, &subject, "2026-11-22T00:00:00Z")
        .unwrap();

    let conflicting = db.issue_attestation(
        &attestation_id,
        &issuer,
        &OpaqueId::new("c".repeat(64)).unwrap(),
        "2026-11-22T00:00:00Z",
    );

    assert!(conflicting.is_err(), "a differing replay must be refused");
}

#[test]
fn an_attestation_id_and_a_decision_id_are_separate_namespaces() {
    // §3.1 keeps two tables precisely so an attestation id cannot be mistaken for
    // a decision id. Same string, both tables, no collision.
    let mut db = AdmissionStore::in_memory().unwrap();
    let shared = id("same-id-both-tables");
    let attestor = IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap();
    let decision_issuer = IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap();
    let subject = digest();

    let attestation = db
        .issue_attestation(&shared, &attestor, &subject, "2026-11-22T00:00:00Z")
        .unwrap();
    let decision = db
        .issue_authorization_decision(
            &shared,
            &decision_issuer,
            &subject,
            "2026-11-22T00:00:00Z",
            memory_domain::AuthorizationDecisionKind::Approved,
        )
        .unwrap();

    assert_eq!(db.validate_attestation(&attestation, &subject), Ok(true));
    assert_eq!(
        db.validate_authorization_decision(&decision, &subject),
        Ok(true)
    );
}
