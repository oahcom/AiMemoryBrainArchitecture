//! I-side attestation references.
//!
//! `AttestorRef` on `lib.rs` is a unit placeholder: `AttestorRef(())` carries no
//! id, no issuer and no digest, so it cannot be compared against a durable
//! `i_attestations` row. That is sufficient for the presence gate — `dm2_06`
//! only asks whether an attestor ref exists — but it leaves the attestor half of
//! GAP-18 unimplementable, because a validator with nothing to compare is a
//! lookup, not a validation.
//!
//! This module adds the content carrier, mirroring `AuthorizationDecisionRef`
//! deliberately: same three states, same constructor split, same rules. §3.1 of
//! `GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER` gives the two tables the same
//! shape, so the two reference types should not diverge either.
//!
//! What is *not* shared is the issuer. `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER`
//! §5 says "Do not reuse `DEV_BASELINE_ISSUER` for decisions … that separation is
//! the point." The same reasoning runs the other way: an attestation is issued by
//! the attestor, not by the decision authority, so it has its own allowlist
//! constant. One shared string would let a single compromised issuer mint both
//! kinds of record, which is what two primary-key namespaces exist to prevent.

use crate::canonical_commit::{is_rfc3339_utc, is_sha256_hex};
use crate::{DomainError, IssuerId, OpaqueId};

/// The single I-side attestor identity admitted by the dev baseline.
///
/// Deliberately distinct from [`crate::I_DEV_BASELINE_ISSUER`]. The two tables
/// have separate primary-key namespaces so an attestation id cannot be mistaken
/// for a decision id; separate issuer strings close the same gap one layer up,
/// where the namespace alone cannot.
pub const I_DEV_BASELINE_ATTESTOR: &str = "i-attestor-proxy/dev-baseline-v1";

/// The content an issued attestation carries.
///
/// `signature` appears in the DDL but not here: nothing produces or checks one in
/// the dev baseline, and `authorization_decisions` already stores `''` in the same
/// column. A field nothing validates would suggest coverage that does not exist.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AttestorData {
    pub attestation_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}

/// Attestor presence and issued content.
///
/// Three states for the same reason `AuthorizationDecisionRef` has three: absence
/// has to be representable before presence can mean anything. `PendingI` satisfies
/// the presence gate and proves nothing; `Issued` carries the fields a durable row
/// can be compared against, and establishes nothing by itself.
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum IssuedAttestorRef {
    /// No attestor reference was recorded.
    Absent,
    /// The known unvalidated placeholder: a value exists, nothing is proven.
    PendingI,
    /// A caller-claimed I-issued attestation carrying its contract fields.
    /// Authenticity is not asserted; that is the attestor contract's question.
    Issued(AttestorData),
}

impl IssuedAttestorRef {
    /// Explicit absence.
    pub const fn absent() -> Self {
        Self::Absent
    }

    /// Legacy placeholder. Public, and therefore never proof of an attestation.
    pub const fn pending_i() -> Self {
        Self::PendingI
    }

    /// Construct a candidate from complete issued data. Confers no authority.
    ///
    /// Validation happens in [`AttestorData::validate`], not here, so a caller can
    /// build a reference for comparison against a stored row without first
    /// satisfying the writer's rules. `issue_attestation` is the writer; it
    /// validates before insert.
    pub fn from_issued_data(data: AttestorData) -> Self {
        Self::Issued(data)
    }

    pub const fn is_absent(&self) -> bool {
        matches!(self, Self::Absent)
    }

    pub const fn is_pending(&self) -> bool {
        matches!(self, Self::PendingI)
    }

    pub const fn is_issued(&self) -> bool {
        matches!(self, Self::Issued(_))
    }

    /// The issued content, if this reference carries any.
    pub fn data(&self) -> Option<&AttestorData> {
        match self {
            Self::Absent | Self::PendingI => None,
            Self::Issued(data) => Some(data),
        }
    }
}

impl AttestorData {
    /// The four rules a row must satisfy before it can back a reference.
    ///
    /// Mirrors `issue_authorization_decision`'s checks exactly, so a row one path
    /// accepts and the other rejects cannot exist.
    pub fn validate(&self) -> Result<(), DomainError> {
        if self.attestation_id.as_str().trim().is_empty() {
            return Err(DomainError::EmptyId);
        }
        if self.issuer.as_str() != I_DEV_BASELINE_ATTESTOR {
            return Err(DomainError::InvalidCanonicalCommitField("issuer"));
        }
        if !is_sha256_hex(self.subject_digest.as_str()) {
            return Err(DomainError::InvalidCanonicalCommitField("subject_digest"));
        }
        if !is_rfc3339_utc(&self.issued_at) {
            return Err(DomainError::InvalidCanonicalCommitField("issued_at"));
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sample() -> AttestorData {
        AttestorData {
            attestation_id: OpaqueId::new("attestation-1").unwrap(),
            issuer: IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap(),
            subject_digest: OpaqueId::new("a".repeat(64)).unwrap(),
            issued_at: "2026-01-01T00:00:00Z".into(),
        }
    }

    #[test]
    fn well_formed_data_validates() {
        sample().validate().expect("sample is well formed");
    }

    #[test]
    fn the_decision_issuer_is_refused() {
        let mut data = sample();
        data.issuer = IssuerId::new(crate::I_DEV_BASELINE_ISSUER).unwrap();
        assert_eq!(
            data.validate().unwrap_err(),
            DomainError::InvalidCanonicalCommitField("issuer")
        );
    }

    #[test]
    fn a_short_subject_digest_is_refused() {
        let mut data = sample();
        data.subject_digest = OpaqueId::new("abc").unwrap();
        assert_eq!(
            data.validate().unwrap_err(),
            DomainError::InvalidCanonicalCommitField("subject_digest")
        );
    }

    #[test]
    fn a_non_utc_timestamp_is_refused() {
        let mut data = sample();
        data.issued_at = "2026-01-01 00:00:00".into();
        assert_eq!(
            data.validate().unwrap_err(),
            DomainError::InvalidCanonicalCommitField("issued_at")
        );
    }

    #[test]
    fn the_three_states_are_distinguishable() {
        assert!(IssuedAttestorRef::absent().is_absent());
        assert!(IssuedAttestorRef::pending_i().is_pending());
        assert!(IssuedAttestorRef::from_issued_data(sample()).is_issued());
        assert!(IssuedAttestorRef::pending_i().data().is_none());
        assert!(IssuedAttestorRef::from_issued_data(sample())
            .data()
            .is_some());
    }

    #[test]
    fn an_issued_reference_round_trips_through_json() {
        let reference = IssuedAttestorRef::from_issued_data(sample());
        let encoded = serde_json::to_string(&reference).unwrap();
        let decoded: IssuedAttestorRef = serde_json::from_str(&encoded).unwrap();
        assert_eq!(decoded, reference);
    }

    #[test]
    fn a_placeholder_round_trips_without_gaining_content() {
        let decoded: IssuedAttestorRef =
            serde_json::from_str(&serde_json::to_string(&IssuedAttestorRef::pending_i()).unwrap())
                .unwrap();
        assert!(decoded.is_pending());
        assert!(decoded.data().is_none());
    }
}
