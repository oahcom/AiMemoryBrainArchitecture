//! Canonical commit reference, issued data and subject encoding.
//!
//! Contract: `D-OWNER-DECISION-CANONICAL-COMMIT-001` §2. The reference is
//! content-bearing, but a reference is only a *candidate*: it establishes no
//! authority on its own. Only the durable `canonical_commits` row owned by the
//! compiler's `AdmissionStore` can make a candidate validate.
//!
//! Dev-baseline scope: the issuer allowlist contains exactly one literal and no
//! cryptography is performed. See §7 of the decision for the production
//! replacement path.

use crate::{DomainError, OpaqueId};

/// The single issuer identity admitted by the dev baseline (§2.2).
pub const DEV_BASELINE_ISSUER: &str = "d-owner-proxy/dev-baseline-v1";

/// Version tag of the subject encoding (§2.1). Changing the encoding requires a
/// new tag; the tag is part of the digested bytes.
pub const CANONICAL_COMMIT_SUBJECT_VERSION: &str = "CanonicalCommitSubjectV1";

/// Issuer identity. Validated by the `OpaqueId` convention, not by an allowlist:
/// whether an issuer is trusted is decided when a record is validated (§4.2).
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct IssuerId(OpaqueId);

impl IssuerId {
    pub fn new(value: impl Into<String>) -> Result<Self, DomainError> {
        Ok(Self(OpaqueId::new(value)?))
    }

    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

/// The content a committed reference carries (§2.1).
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitData {
    pub commit_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum CanonicalCommitRefState {
    Pending,
    Issued(CanonicalCommitData),
}

/// A canonical commit reference: either the legacy pending placeholder or an
/// issued candidate.
///
/// The state is private so no struct literal can fabricate an issued reference,
/// and the only public constructor for issued data is [`Self::from_issued_data`],
/// which validates the fields but confers no authority. §4.2 requires the
/// matching durable record for validation.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitRef {
    state: CanonicalCommitRefState,
}

impl CanonicalCommitRef {
    /// Explicit legacy/uncommitted marker. This is never commit evidence.
    pub const fn pending_d() -> Self {
        Self {
            state: CanonicalCommitRefState::Pending,
        }
    }

    /// Construct a candidate reference after validating its fields.
    ///
    /// This does not issue a commit or establish authority; the matching durable
    /// `canonical_commits` row is required by the validator.
    pub fn from_issued_data(data: CanonicalCommitData) -> Result<Self, DomainError> {
        validate_commit_data(&data)?;
        Ok(Self {
            state: CanonicalCommitRefState::Issued(data),
        })
    }

    pub fn is_pending(&self) -> bool {
        matches!(self.state, CanonicalCommitRefState::Pending)
    }

    pub fn data(&self) -> Option<&CanonicalCommitData> {
        match &self.state {
            CanonicalCommitRefState::Pending => None,
            CanonicalCommitRefState::Issued(data) => Some(data),
        }
    }
}

/// §2.3: `Pending` keeps the legacy unit/null representation of the old
/// `CanonicalCommitRef(())` newtype; `Issued` is a named object with exactly the
/// four issued fields. Malformed issued data is a deserialization error, never a
/// silent downgrade to `Pending`.
impl serde::Serialize for CanonicalCommitRef {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        match &self.state {
            CanonicalCommitRefState::Pending => {
                serializer.serialize_unit_struct("CanonicalCommitRef")
            }
            CanonicalCommitRefState::Issued(data) => {
                use serde::ser::SerializeStruct;
                let mut object = serializer.serialize_struct("CanonicalCommitRef", 4)?;
                object.serialize_field("commit_id", &data.commit_id)?;
                object.serialize_field("issuer", &data.issuer)?;
                object.serialize_field("subject_digest", &data.subject_digest)?;
                object.serialize_field("issued_at", &data.issued_at)?;
                object.end()
            }
        }
    }
}

#[derive(serde::Deserialize)]
#[serde(deny_unknown_fields)]
struct IssuedWire {
    commit_id: OpaqueId,
    issuer: String,
    subject_digest: OpaqueId,
    issued_at: String,
}

struct CanonicalCommitRefVisitor;

impl<'de> serde::de::Visitor<'de> for CanonicalCommitRefVisitor {
    type Value = CanonicalCommitRef;

    fn expecting(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str("the legacy canonical commit unit value or an issued commit object")
    }

    fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(CanonicalCommitRef::pending_d())
    }

    fn visit_none<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(CanonicalCommitRef::pending_d())
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, map: A) -> Result<Self::Value, A::Error> {
        use serde::de::Error;
        let wire: IssuedWire =
            serde::Deserialize::deserialize(serde::de::value::MapAccessDeserializer::new(map))?;
        let data = CanonicalCommitData {
            commit_id: wire.commit_id,
            issuer: IssuerId::new(wire.issuer)
                .map_err(|error| Error::custom(format!("invalid issuer: {error:?}")))?,
            subject_digest: wire.subject_digest,
            issued_at: wire.issued_at,
        };
        CanonicalCommitRef::from_issued_data(data)
            .map_err(|error| Error::custom(format!("invalid issued canonical commit: {error:?}")))
    }
}

impl<'de> serde::Deserialize<'de> for CanonicalCommitRef {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(CanonicalCommitRefVisitor)
    }
}

/// §2.2 field validation. Rejects empty IDs, an issuer outside the dev-baseline
/// allowlist, a digest that is not exactly 64 lowercase hex characters, and a
/// timestamp that is not RFC 3339 UTC.
fn validate_commit_data(data: &CanonicalCommitData) -> Result<(), DomainError> {
    if data.commit_id.as_str().trim().is_empty() {
        return Err(DomainError::EmptyId);
    }
    if data.issuer.as_str() != DEV_BASELINE_ISSUER {
        return Err(DomainError::InvalidCanonicalCommitField("issuer"));
    }
    if !is_sha256_hex(data.subject_digest.as_str()) {
        return Err(DomainError::InvalidCanonicalCommitField("subject_digest"));
    }
    if !is_rfc3339_utc(&data.issued_at) {
        return Err(DomainError::InvalidCanonicalCommitField("issued_at"));
    }
    Ok(())
}

/// Exactly 64 lowercase hexadecimal characters.
pub fn is_sha256_hex(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
}

/// Strict `YYYY-MM-DDTHH:MM:SS[.fraction]Z` check, no clock and no offsets.
///
/// The dev baseline issues UTC `Z` timestamps only; a numeric offset is not
/// accepted because validation must not depend on a time-zone database.
pub fn is_rfc3339_utc(value: &str) -> bool {
    let bytes = value.as_bytes();
    if bytes.len() < 20 {
        return false;
    }
    if bytes[4] != b'-'
        || bytes[7] != b'-'
        || bytes[10] != b'T'
        || bytes[13] != b':'
        || bytes[16] != b':'
    {
        return false;
    }
    if *bytes.last().unwrap_or(&0) != b'Z' {
        return false;
    }
    let digits = |range: std::ops::Range<usize>| -> Option<u32> {
        let slice = value.get(range)?;
        if !slice.bytes().all(|b| b.is_ascii_digit()) {
            return None;
        }
        slice.parse().ok()
    };
    let (Some(year), Some(month), Some(day), Some(hour), Some(minute), Some(second)) = (
        digits(0..4),
        digits(5..7),
        digits(8..10),
        digits(11..13),
        digits(14..16),
        digits(17..19),
    ) else {
        return false;
    };
    let fraction_ok = if bytes.len() == 20 {
        true
    } else {
        // `SS.<1+ digits>Z`
        bytes[19] == b'.'
            && bytes.len() >= 22
            && bytes[20..bytes.len() - 1]
                .iter()
                .all(|b| b.is_ascii_digit())
    };
    fraction_ok
        && (1..=12).contains(&month)
        && day >= 1
        && day <= days_in_month(year, month)
        && hour <= 23
        && minute <= 59
        && second <= 60
}

fn days_in_month(year: u32, month: u32) -> u32 {
    match month {
        1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
        4 | 6 | 9 | 11 => 30,
        2 if year.is_multiple_of(4) && !year.is_multiple_of(100) || year.is_multiple_of(400) => 29,
        2 => 28,
        _ => 0,
    }
}

/// Deterministic, length-prefixed encoding of the immutable subject being
/// committed (§2.1).
///
/// One implementation is shared by issuance and validation. Every field is
/// preceded by its `u64` big-endian byte length, so no concatenation is
/// ambiguous, and the field order is fixed by this function. JSON object key
/// order is deliberately not used.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CanonicalCommitSubjectV1 {
    encoded: Vec<u8>,
}

impl CanonicalCommitSubjectV1 {
    pub fn from_parts(
        subject_kind: &str,
        subject_id: &str,
        revision_id: &str,
        payload: &[u8],
    ) -> Result<Self, DomainError> {
        if subject_kind.is_empty() || subject_id.is_empty() || revision_id.is_empty() {
            return Err(DomainError::EmptyRequiredField("canonical_commit_subject"));
        }
        let mut encoded = Vec::new();
        for field in [
            CANONICAL_COMMIT_SUBJECT_VERSION.as_bytes(),
            subject_kind.as_bytes(),
            subject_id.as_bytes(),
            revision_id.as_bytes(),
        ] {
            push_field(&mut encoded, field);
        }
        push_field(&mut encoded, payload);
        Ok(Self { encoded })
    }

    /// The exact bytes to digest.
    pub fn as_bytes(&self) -> &[u8] {
        &self.encoded
    }
}

fn push_field(out: &mut Vec<u8>, field: &[u8]) {
    out.extend_from_slice(&(field.len() as u64).to_be_bytes());
    out.extend_from_slice(field);
}

#[cfg(test)]
mod tests {
    use super::*;

    fn digest() -> OpaqueId {
        OpaqueId::new("a".repeat(64)).unwrap()
    }

    fn data() -> CanonicalCommitData {
        CanonicalCommitData {
            commit_id: OpaqueId::new("commit-1").unwrap(),
            issuer: IssuerId::new(DEV_BASELINE_ISSUER).unwrap(),
            subject_digest: digest(),
            issued_at: "2026-11-22T00:00:00Z".into(),
        }
    }

    #[test]
    fn pending_keeps_the_legacy_unit_json_representation() {
        assert_eq!(
            serde_json::to_string(&CanonicalCommitRef::pending_d()).unwrap(),
            "null"
        );
        let decoded: CanonicalCommitRef = serde_json::from_str("null").unwrap();
        assert!(decoded.is_pending());
        assert_eq!(decoded, CanonicalCommitRef::pending_d());
    }

    #[test]
    fn issued_round_trips_through_its_named_object_form() {
        let issued = CanonicalCommitRef::from_issued_data(data()).unwrap();
        let json = serde_json::to_string(&issued).unwrap();
        assert_eq!(
            json,
            format!(
                r#"{{"commit_id":"commit-1","issuer":"{DEV_BASELINE_ISSUER}","subject_digest":"{}","issued_at":"2026-11-22T00:00:00Z"}}"#,
                "a".repeat(64)
            )
        );
        let decoded: CanonicalCommitRef = serde_json::from_str(&json).unwrap();
        assert_eq!(decoded, issued);
        assert!(!decoded.is_pending());
    }

    #[test]
    fn malformed_issued_objects_fail_closed() {
        let base = format!(
            r#"{{"commit_id":"commit-1","issuer":"{DEV_BASELINE_ISSUER}","subject_digest":"{}","issued_at":"2026-11-22T00:00:00Z"}}"#,
            "a".repeat(64)
        );
        for malformed in [
            base.replace(r#""commit-1""#, r#""""#),
            base.replace(DEV_BASELINE_ISSUER, "someone-else"),
            base.replace(&"a".repeat(64), &"A".repeat(64)),
            base.replace("2026-11-22T00:00:00Z", "2026-11-22"),
            base.replace(r#","issued_at""#, r#","extra":"x","issued_at""#),
            base.replace(
                r#""issued_at":"2026-11-22T00:00:00Z""#,
                r#""issued_at":"2026-11-22T00:00:00Z","issued_at":"2026-11-22T00:00:00Z""#,
            ),
            r#"{"commit_id":"commit-1"}"#.to_owned(),
        ] {
            assert!(
                serde_json::from_str::<CanonicalCommitRef>(&malformed).is_err(),
                "must reject {malformed}"
            );
        }
    }

    #[test]
    fn issued_data_validation_rejects_bad_fields() {
        let mut bad = data();
        bad.subject_digest = OpaqueId::new("not-a-digest").unwrap();
        assert_eq!(
            CanonicalCommitRef::from_issued_data(bad).unwrap_err(),
            DomainError::InvalidCanonicalCommitField("subject_digest")
        );

        let mut bad = data();
        bad.issued_at = "2026-13-01T00:00:00Z".into();
        assert_eq!(
            CanonicalCommitRef::from_issued_data(bad).unwrap_err(),
            DomainError::InvalidCanonicalCommitField("issued_at")
        );

        let mut bad = data();
        bad.issuer = IssuerId::new("someone-else").unwrap();
        assert_eq!(
            CanonicalCommitRef::from_issued_data(bad).unwrap_err(),
            DomainError::InvalidCanonicalCommitField("issuer")
        );
    }

    #[test]
    fn subject_encoding_is_length_prefixed_and_field_order_fixed() {
        let first = CanonicalCommitSubjectV1::from_parts("fact", "s1", "r1", b"payload").unwrap();
        let again = CanonicalCommitSubjectV1::from_parts("fact", "s1", "r1", b"payload").unwrap();
        assert_eq!(first, again);

        // Concatenation ambiguity is impossible: shifting a byte between
        // adjacent fields changes the bytes.
        let shifted = CanonicalCommitSubjectV1::from_parts("fact", "s1r", "1", b"payload").unwrap();
        assert_ne!(first.as_bytes(), shifted.as_bytes());

        // The version tag leads the encoding.
        assert!(first
            .as_bytes()
            .starts_with(&(CANONICAL_COMMIT_SUBJECT_VERSION.len() as u64).to_be_bytes()));
    }

    #[test]
    fn timestamp_check_accepts_utc_and_rejects_offsets() {
        assert!(is_rfc3339_utc("2026-11-22T00:00:00Z"));
        assert!(is_rfc3339_utc("2024-02-29T23:59:60.123Z"));
        assert!(!is_rfc3339_utc("2023-02-29T00:00:00Z"));
        assert!(!is_rfc3339_utc("2026-11-22T00:00:00+00:00"));
        assert!(!is_rfc3339_utc("2026-11-22T24:00:00Z"));
        assert!(!is_rfc3339_utc("2026-11-22T00:00:00.Z"));
    }
}
