use crate::{is_rfc3339_utc, is_sha256_hex, DomainError, IssuerId, OpaqueId};

/// I-owner-proxy dev-baseline trust anchor
/// (`I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §2.2).
pub const I_DEV_BASELINE_ISSUER: &str = "i-owner-proxy/dev-baseline-v1";

/// Deliberately distinct from [`I_DEV_BASELINE_ISSUER`]. The two tables have
/// separate primary-key namespaces so an attestation id cannot be mistaken for
/// a decision id; separate issuer strings close the same gap one layer up,
/// where the namespace alone cannot.
pub const I_DEV_BASELINE_ATTESTOR: &str = "i-attestor-proxy/dev-baseline-v1";

const fn issuer_str_eq(left: &str, right: &str) -> bool {
    let left = left.as_bytes();
    let right = right.as_bytes();

    if left.len() != right.len() {
        return false;
    }

    let mut i = 0;
    while i < left.len() {
        if left[i] != right[i] {
            return false;
        }
        i += 1;
    }

    true
}

const fn issuer_has_prefix(value: &str, prefix: &str) -> bool {
    let value = value.as_bytes();
    let prefix = prefix.as_bytes();

    if prefix.len() > value.len() {
        return false;
    }

    let mut i = 0;
    while i < prefix.len() {
        if value[i] != prefix[i] {
            return false;
        }
        i += 1;
    }

    true
}

const _: () = {
    assert!(
        !issuer_str_eq(I_DEV_BASELINE_ISSUER, I_DEV_BASELINE_ATTESTOR),
        "I decision and attestor issuer identifiers must be distinct"
    );

    assert!(
        issuer_has_prefix(I_DEV_BASELINE_ISSUER, "i-owner-proxy/"),
        "I decision issuer must use the i-owner-proxy/ prefix"
    );

    assert!(
        issuer_has_prefix(I_DEV_BASELINE_ATTESTOR, "i-attestor-proxy/"),
        "I attestor issuer must use the i-attestor-proxy/ prefix"
    );

    assert!(
        !issuer_has_prefix(I_DEV_BASELINE_ISSUER, "i-attestor-proxy/"),
        "I decision issuer must not use the attestor issuer prefix"
    );

    assert!(
        !issuer_has_prefix(I_DEV_BASELINE_ATTESTOR, "i-owner-proxy/"),
        "I attestor issuer must not use the decision issuer prefix"
    );
};

// ---------------------------------------------------------------------------
// Authorization decision
// ---------------------------------------------------------------------------

/// Terminal disposition of a recorded authorization decision (§2.1).
///
/// Serialized as `Approved` / `Denied` / `Conditional`, matching the durable
/// `decision_kind` column literal required by §3.1.
#[derive(serde::Serialize, serde::Deserialize, Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorizationDecisionKind {
    Approved,
    Denied,
    Conditional,
}

/// The content an issued authorization decision carries (§2.1).
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionData {
    pub decision_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
    pub decision_kind: AuthorizationDecisionKind,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum AuthorizationDecisionRefState {
    Absent,
    Pending,
    Issued(AuthorizationDecisionData),
}

/// Authorization decision presence and issued content.
///
/// Three states: `Absent` blocks publication, `Pending` satisfies the presence
/// gate, `Issued` carries the five fields §4.2 compares against a durable row.
/// No state independently establishes authority.
///
/// The wire form is fixed by §2.4 and is not derivable: `Absent` is the string
/// `"absent"`, `Pending` is the legacy unit value (JSON `null`), and `Issued` is
/// a flat five-field object. A derived enum would emit `"pending_i"` and wrap
/// issued content in `{"issued": ..}`, both of which break Phase 1.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionRef {
    state: AuthorizationDecisionRefState,
}

impl AuthorizationDecisionRef {
    /// Explicit absence. `FactRevision::validate` rejects a fact carrying this.
    pub const fn absent() -> Self {
        Self {
            state: AuthorizationDecisionRefState::Absent,
        }
    }

    /// Legacy placeholder. Public, and therefore never proof of an I-issued
    /// decision.
    pub const fn pending_i() -> Self {
        Self {
            state: AuthorizationDecisionRefState::Pending,
        }
    }

    /// A claimed I-issued reference when only an id is at hand.
    ///
    /// The remaining fields are explicit sentinels: a zero digest, the epoch, and
    /// `Conditional` (the weakest kind). This is deliberately NOT valid issued
    /// data — `validate_authorization_decision` will not match it against any row,
    /// and no row can be written from it. Use `from_issued_data` for real content.
    pub fn issued(decision_id: OpaqueId) -> Self {
        Self {
            state: AuthorizationDecisionRefState::Issued(AuthorizationDecisionData {
                decision_id,
                issuer: IssuerId::new(I_DEV_BASELINE_ISSUER)
                    .expect("the dev-baseline issuer literal is a valid opaque id"),
                subject_digest: OpaqueId::new("0".repeat(64))
                    .expect("64 lowercase hexadecimal zeroes are a valid opaque id"),
                issued_at: "1970-01-01T00:00:00Z".to_owned(),
                decision_kind: AuthorizationDecisionKind::Conditional,
            }),
        }
    }

    /// Construct a candidate from complete issued data. Confers no authority.
    pub fn from_issued_data(data: AuthorizationDecisionData) -> Result<Self, DomainError> {
        validate_authorization_decision_data(&data)?;
        Ok(Self {
            state: AuthorizationDecisionRefState::Issued(data),
        })
    }

    pub const fn is_absent(&self) -> bool {
        matches!(self.state, AuthorizationDecisionRefState::Absent)
    }

    pub const fn is_pending(&self) -> bool {
        matches!(self.state, AuthorizationDecisionRefState::Pending)
    }

    /// The issued content, if this reference carries any.
    pub fn data(&self) -> Option<&AuthorizationDecisionData> {
        match &self.state {
            AuthorizationDecisionRefState::Absent | AuthorizationDecisionRefState::Pending => None,
            AuthorizationDecisionRefState::Issued(data) => Some(data),
        }
    }
}

fn validate_authorization_decision_data(
    data: &AuthorizationDecisionData,
) -> Result<(), DomainError> {
    if data.decision_id.as_str().trim().is_empty() {
        return Err(DomainError::EmptyId);
    }
    if data.issuer.as_str() != I_DEV_BASELINE_ISSUER {
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

impl serde::Serialize for AuthorizationDecisionRef {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        match &self.state {
            AuthorizationDecisionRefState::Absent => serializer.serialize_str("absent"),
            AuthorizationDecisionRefState::Pending => {
                serializer.serialize_unit_struct("AuthorizationDecisionRef")
            }
            AuthorizationDecisionRefState::Issued(data) => {
                use serde::ser::SerializeStruct;

                let mut object = serializer.serialize_struct("AuthorizationDecisionRef", 5)?;
                object.serialize_field("decision_id", &data.decision_id)?;
                object.serialize_field("issuer", &data.issuer)?;
                object.serialize_field("subject_digest", &data.subject_digest)?;
                object.serialize_field("issued_at", &data.issued_at)?;
                object.serialize_field("decision_kind", &data.decision_kind)?;
                object.end()
            }
        }
    }
}

#[derive(serde::Deserialize)]
#[serde(deny_unknown_fields)]
struct AuthorizationDecisionIssuedWire {
    decision_id: OpaqueId,
    issuer: String,
    subject_digest: OpaqueId,
    issued_at: String,
    decision_kind: AuthorizationDecisionKind,
}

struct AuthorizationDecisionRefVisitor;

impl<'de> serde::de::Visitor<'de> for AuthorizationDecisionRefVisitor {
    type Value = AuthorizationDecisionRef;

    fn expecting(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(
            "the absent marker, the legacy pending unit/string value, or a flat issued \
             authorization decision object",
        )
    }

    fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(AuthorizationDecisionRef::pending_i())
    }

    fn visit_none<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(AuthorizationDecisionRef::pending_i())
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match value {
            "absent" => Ok(AuthorizationDecisionRef::absent()),
            // Read-compat with values written by the previous derived enum. New
            // writes always emit the unit form above (§2.4).
            "pending_i" => Ok(AuthorizationDecisionRef::pending_i()),
            _ => Err(E::custom("unknown authorization decision reference marker")),
        }
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, map: A) -> Result<Self::Value, A::Error> {
        use serde::de::Error;

        let wire: AuthorizationDecisionIssuedWire =
            serde::Deserialize::deserialize(serde::de::value::MapAccessDeserializer::new(map))?;

        let data = AuthorizationDecisionData {
            decision_id: wire.decision_id,
            issuer: IssuerId::new(wire.issuer)
                .map_err(|error| Error::custom(format!("invalid issuer: {error:?}")))?,
            subject_digest: wire.subject_digest,
            issued_at: wire.issued_at,
            decision_kind: wire.decision_kind,
        };

        AuthorizationDecisionRef::from_issued_data(data).map_err(|error| {
            Error::custom(format!("invalid issued authorization decision: {error:?}"))
        })
    }
}

impl<'de> serde::Deserialize<'de> for AuthorizationDecisionRef {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(AuthorizationDecisionRefVisitor)
    }
}

// ---------------------------------------------------------------------------
// Attestor
// ---------------------------------------------------------------------------

/// The content an issued attestation carries (§2.3).
///
/// Distinct from `AuthorizationDecisionData` on purpose: an attestation answers
/// "who attested this subject", an authorization decision answers "what did I
/// decide about this subject". Neither substitutes for the other.
///
/// Construction by struct literal is unvalidated — that is what
/// [`AttestorRef::from_issued_data`] is for. **Deserialization is validated**:
/// `Deserialize` routes through [`validate_attestor_data`], so a value decoded
/// from bytes cannot carry an unsupported issuer, an empty id, a non-hex digest
/// or a non-RFC-3339 timestamp. There is deliberately no unvalidated decode path.
#[derive(serde::Serialize, Clone, Debug, Eq, PartialEq)]
pub struct AttestorData {
    pub attestation_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum AttestorRefState {
    Pending,
    Issued(AttestorData),
}

/// An attestor reference is a candidate only. Authority comes from the matching
/// durable `i_attestations` row, never from this value.
///
/// Wire form per §2.4: `Pending` is the legacy unit value (JSON `null`),
/// `Issued` is a flat four-field object.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AttestorRef {
    state: AttestorRefState,
}

impl AttestorRef {
    pub const fn pending_i() -> Self {
        Self {
            state: AttestorRefState::Pending,
        }
    }

    /// Construct a candidate from complete attestation data. Confers no authority.
    pub fn from_issued_data(data: AttestorData) -> Result<Self, DomainError> {
        validate_attestor_data(&data)?;
        Ok(Self {
            state: AttestorRefState::Issued(data),
        })
    }

    pub const fn is_pending(&self) -> bool {
        matches!(self.state, AttestorRefState::Pending)
    }

    /// The issued content, if this reference carries any.
    pub fn data(&self) -> Option<&AttestorData> {
        match &self.state {
            AttestorRefState::Pending => None,
            AttestorRefState::Issued(data) => Some(data),
        }
    }
}

fn validate_attestor_data(data: &AttestorData) -> Result<(), DomainError> {
    if data.attestation_id.as_str().trim().is_empty() {
        return Err(DomainError::EmptyId);
    }
    if data.issuer.as_str() != I_DEV_BASELINE_ATTESTOR {
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

impl<'de> serde::Deserialize<'de> for AttestorData {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        use serde::de::Error;

        let wire = AttestorIssuedWire::deserialize(deserializer)?;
        let data = AttestorData {
            attestation_id: wire.attestation_id,
            issuer: IssuerId::new(wire.issuer)
                .map_err(|error| Error::custom(format!("invalid issuer: {error:?}")))?,
            subject_digest: wire.subject_digest,
            issued_at: wire.issued_at,
        };

        validate_attestor_data(&data)
            .map_err(|error| Error::custom(format!("invalid attestor data: {error:?}")))?;
        Ok(data)
    }
}

impl serde::Serialize for AttestorRef {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        match &self.state {
            AttestorRefState::Pending => serializer.serialize_unit_struct("AttestorRef"),
            AttestorRefState::Issued(data) => {
                use serde::ser::SerializeStruct;

                let mut object = serializer.serialize_struct("AttestorRef", 4)?;
                object.serialize_field("attestation_id", &data.attestation_id)?;
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
struct AttestorIssuedWire {
    attestation_id: OpaqueId,
    issuer: String,
    subject_digest: OpaqueId,
    issued_at: String,
}

struct AttestorRefVisitor;

impl<'de> serde::de::Visitor<'de> for AttestorRefVisitor {
    type Value = AttestorRef;

    fn expecting(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str("the legacy attestor unit value or a flat issued attestor object")
    }

    fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(AttestorRef::pending_i())
    }

    fn visit_none<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(AttestorRef::pending_i())
    }

    fn visit_str<E: serde::de::Error>(self, value: &str) -> Result<Self::Value, E> {
        match value {
            "pending_i" => Ok(AttestorRef::pending_i()),
            _ => Err(E::custom("unknown attestor reference marker")),
        }
    }

    fn visit_map<A: serde::de::MapAccess<'de>>(self, map: A) -> Result<Self::Value, A::Error> {
        use serde::de::Error;

        let wire: AttestorIssuedWire =
            serde::Deserialize::deserialize(serde::de::value::MapAccessDeserializer::new(map))?;

        let data = AttestorData {
            attestation_id: wire.attestation_id,
            issuer: IssuerId::new(wire.issuer)
                .map_err(|error| Error::custom(format!("invalid issuer: {error:?}")))?,
            subject_digest: wire.subject_digest,
            issued_at: wire.issued_at,
        };

        AttestorRef::from_issued_data(data)
            .map_err(|error| Error::custom(format!("invalid issued attestor: {error:?}")))
    }
}

impl<'de> serde::Deserialize<'de> for AttestorRef {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(AttestorRefVisitor)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn valid_attestor_data() -> AttestorData {
        AttestorData {
            attestation_id: OpaqueId::new("attestation-domain-test").unwrap(),
            issuer: IssuerId::new(I_DEV_BASELINE_ATTESTOR).unwrap(),
            subject_digest: OpaqueId::new("a".repeat(64)).unwrap(),
            issued_at: "2026-11-22T00:00:00Z".to_owned(),
        }
    }

    #[test]
    fn attestor_data_accepts_valid_issued_data() {
        assert!(validate_attestor_data(&valid_attestor_data()).is_ok());
    }

    #[test]
    fn attestor_data_rejects_empty_attestation_id() {
        // OpaqueId's derived Deserialize does not validate, so decoding an empty
        // string lets this reach the validator instead of failing earlier.
        let mut data = valid_attestor_data();
        data.attestation_id = serde_json::from_str("\"\"").unwrap();

        assert_eq!(validate_attestor_data(&data), Err(DomainError::EmptyId));
    }

    #[test]
    fn attestor_data_rejects_unsupported_issuer() {
        let mut data = valid_attestor_data();
        data.issuer = IssuerId::new("someone-else").unwrap();

        assert_eq!(
            validate_attestor_data(&data),
            Err(DomainError::InvalidCanonicalCommitField("issuer"))
        );
    }

    #[test]
    fn the_decision_issuer_is_refused() {
        let mut data = valid_attestor_data();
        data.issuer = IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap();
        assert_eq!(
            validate_attestor_data(&data).unwrap_err(),
            DomainError::InvalidCanonicalCommitField("issuer")
        );
    }

    #[test]
    fn attestor_data_rejects_non_hex_subject_digest() {
        let mut data = valid_attestor_data();
        data.subject_digest = OpaqueId::new("not-a-digest").unwrap();

        assert_eq!(
            validate_attestor_data(&data),
            Err(DomainError::InvalidCanonicalCommitField("subject_digest"))
        );
    }

    #[test]
    fn attestor_data_rejects_non_rfc3339_issued_at() {
        let mut data = valid_attestor_data();
        data.issued_at = "yesterday".to_owned();

        assert_eq!(
            validate_attestor_data(&data),
            Err(DomainError::InvalidCanonicalCommitField("issued_at"))
        );
    }

    /// A bare `AttestorData` decoded from bytes must not carry an issuer the
    /// validator would refuse. Before the hand-written `Deserialize` this
    /// returned `Ok` and the caller had no way to tell.
    #[test]
    fn attestor_data_deserialize_rejects_unsupported_issuer() {
        let json = format!(
            r#"{{"attestation_id":"attestation-domain-test","issuer":"someone-else","subject_digest":"{}","issued_at":"2026-11-22T00:00:00Z"}}"#,
            "a".repeat(64)
        );

        assert_eq!(
            serde_json::from_str::<AttestorData>(&json).map_err(|error| error.to_string()),
            Err("invalid attestor data: InvalidCanonicalCommitField(\"issuer\")".to_owned())
        );
    }

    #[test]
    fn attestor_data_deserialize_rejects_empty_attestation_id() {
        let json = format!(
            r#"{{"attestation_id":"","issuer":"{I_DEV_BASELINE_ATTESTOR}","subject_digest":"{}","issued_at":"2026-11-22T00:00:00Z"}}"#,
            "a".repeat(64)
        );

        assert_eq!(
            serde_json::from_str::<AttestorData>(&json).map_err(|error| error.to_string()),
            Err("invalid attestor data: EmptyId".to_owned())
        );
    }

    #[test]
    fn attestor_data_valid_value_round_trips_through_json() {
        let data = valid_attestor_data();
        let wire = serde_json::to_string(&data).unwrap();

        assert_eq!(
            wire,
            format!(
                r#"{{"attestation_id":"attestation-domain-test","issuer":"{I_DEV_BASELINE_ATTESTOR}","subject_digest":"{}","issued_at":"2026-11-22T00:00:00Z"}}"#,
                "a".repeat(64)
            )
        );
        assert_eq!(serde_json::from_str::<AttestorData>(&wire).unwrap(), data);
    }

    #[test]
    fn attestor_ref_keeps_both_wire_forms() {
        // Pending stays the legacy unit value (§2.4): JSON `null`.
        let pending_wire = serde_json::to_string(&AttestorRef::pending_i()).unwrap();
        assert_eq!(pending_wire, "null");
        assert!(serde_json::from_str::<AttestorRef>("null")
            .unwrap()
            .is_pending());

        // Issued stays a flat four-field object, and decoding it still validates.
        let issued = AttestorRef::from_issued_data(valid_attestor_data()).unwrap();
        let issued_wire = serde_json::to_string(&issued).unwrap();
        assert!(
            issued_wire.starts_with("{\"attestation_id\""),
            "got {issued_wire}"
        );
        assert_eq!(
            serde_json::from_str::<AttestorRef>(&issued_wire).unwrap(),
            issued
        );

        let bad_issuer = format!(
            r#"{{"attestation_id":"a","issuer":"someone-else","subject_digest":"{}","issued_at":"2026-11-22T00:00:00Z"}}"#,
            "a".repeat(64)
        );
        assert!(serde_json::from_str::<AttestorRef>(&bad_issuer).is_err());
    }

    #[test]
    fn attestor_ref_distinguishes_pending_from_issued() {
        let pending = AttestorRef::pending_i();
        assert!(pending.is_pending());
        assert!(pending.data().is_none());

        let issued = AttestorRef::from_issued_data(valid_attestor_data()).unwrap();
        assert!(!issued.is_pending());
        assert_eq!(
            issued.data().unwrap().attestation_id.as_str(),
            "attestation-domain-test"
        );
    }

    #[test]
    fn attestor_ref_issued_round_trips_through_json() {
        let issued = AttestorRef::from_issued_data(valid_attestor_data()).unwrap();
        let wire = serde_json::to_string(&issued).unwrap();

        // Flat four-field object, not a tagged enum variant (§2.4).
        assert!(wire.starts_with("{\"attestation_id\""), "got {wire}");
        assert_eq!(serde_json::from_str::<AttestorRef>(&wire).unwrap(), issued);
    }

    #[test]
    fn authorization_decision_kind_serde_uses_canonical_pascal_case() {
        let cases = [
            (AuthorizationDecisionKind::Approved, "\"Approved\""),
            (AuthorizationDecisionKind::Denied, "\"Denied\""),
            (AuthorizationDecisionKind::Conditional, "\"Conditional\""),
        ];

        for (kind, expected_json) in cases {
            let serialized = serde_json::to_string(&kind).unwrap();

            assert_eq!(
                serialized, expected_json,
                "Serde must serialize the canonical decision-kind literal"
            );
        }
    }

    #[test]
    fn authorization_decision_kind_serde_rejects_lowercase_values() {
        for legacy_json in [r#""approved""#, r#""denied""#, r#""conditional""#] {
            let result = serde_json::from_str::<AuthorizationDecisionKind>(legacy_json);

            assert!(
                result.is_err(),
                "Serde must reject legacy lowercase value {legacy_json}"
            );
        }
    }
}
