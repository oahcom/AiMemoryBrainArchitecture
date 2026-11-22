//! Authorization decision and attestor references.
//!
//! The references are validated candidates, not proof of authority. Durable
//! record validation belongs to the compiler-side AdmissionStore.

use crate::{
    is_rfc3339_utc, is_sha256_hex, DomainError, IssuerId, OpaqueId, I_DEV_BASELINE_ISSUER,
};

/// The decision kinds admitted by the I authorization contract.
///
/// Serde's default enum representation preserves the required PascalCase
/// wire values: "Approved", "Denied", and "Conditional".
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub enum AuthorizationDecisionKind {
    Approved,
    Denied,
    Conditional,
}

/// The immutable data carried by an issued authorization decision.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationDecisionData {
    pub decision_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
    pub decision_kind: AuthorizationDecisionKind,
}

/// The immutable data carried by an issued attestation.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AttestorData {
    pub attestation_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum AuthorizationDecisionRefState {
    Absent,
    Pending,
    Issued(AuthorizationDecisionData),
}

/// An authorization decision reference.
///
/// `Absent` is the only state rejected by `FactRevision::validate`.
/// `Pending` is a legacy placeholder and `Issued` is a validated candidate;
/// neither state by itself establishes durable authority.
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

    /// Legacy placeholder. This is not proof of an issued decision.
    pub const fn pending_i() -> Self {
        Self {
            state: AuthorizationDecisionRefState::Pending,
        }
    }

    /// Construct an issued candidate after validating its fields.
    ///
    /// This does not establish authority; the matching durable I record is
    /// required by the compiler-side validator.
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

    pub const fn is_issued(&self) -> bool {
        matches!(self.state, AuthorizationDecisionRefState::Issued(_))
    }

    pub fn data(&self) -> Option<&AuthorizationDecisionData> {
        match &self.state {
            AuthorizationDecisionRefState::Absent | AuthorizationDecisionRefState::Pending => None,
            AuthorizationDecisionRefState::Issued(data) => Some(data),
        }
    }
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
            "the absent or legacy pending authorization value, or an issued authorization decision object",
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
            "pending_i" => Ok(AuthorizationDecisionRef::pending_i()),
            _ => Err(E::unknown_variant(value, &["absent", "pending_i"])),
        }
    }

    fn visit_string<E: serde::de::Error>(self, value: String) -> Result<Self::Value, E> {
        self.visit_str(&value)
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

#[derive(Clone, Debug, Eq, PartialEq)]
enum AttestorRefState {
    Pending,
    Issued(AttestorData),
}

/// An attestor reference.
///
/// Pending is a placeholder, not proof of an attestation. An issued candidate
/// still requires a matching durable I record to validate.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AttestorRef {
    state: AttestorRefState,
}

impl AttestorRef {
    /// Legacy placeholder. This is not proof of an issued attestation.
    pub const fn pending_i() -> Self {
        Self {
            state: AttestorRefState::Pending,
        }
    }

    /// Construct an issued candidate after validating its fields.
    pub fn from_issued_data(data: AttestorData) -> Result<Self, DomainError> {
        validate_attestor_data(&data)?;
        Ok(Self {
            state: AttestorRefState::Issued(data),
        })
    }

    pub const fn is_pending(&self) -> bool {
        matches!(self.state, AttestorRefState::Pending)
    }

    pub const fn is_issued(&self) -> bool {
        matches!(self.state, AttestorRefState::Issued(_))
    }

    pub fn data(&self) -> Option<&AttestorData> {
        match &self.state {
            AttestorRefState::Pending => None,
            AttestorRefState::Issued(data) => Some(data),
        }
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
        formatter.write_str("the legacy attestor unit value or an issued attestor object")
    }

    fn visit_unit<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(AttestorRef::pending_i())
    }

    fn visit_none<E: serde::de::Error>(self) -> Result<Self::Value, E> {
        Ok(AttestorRef::pending_i())
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

/// Validate the fields carried by an authorization decision candidate.
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

/// Validate the fields carried by an attestor candidate.
fn validate_attestor_data(data: &AttestorData) -> Result<(), DomainError> {
    if data.attestation_id.as_str().trim().is_empty() {
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

#[cfg(test)]
mod tests {
    use super::*;

    fn sample_decision_data() -> AuthorizationDecisionData {
        AuthorizationDecisionData {
            decision_id: OpaqueId::new("decision-1").unwrap(),
            issuer: IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap(),
            subject_digest: OpaqueId::new("a".repeat(64)).unwrap(),
            issued_at: "2026-01-01T00:00:00Z".into(),
            decision_kind: AuthorizationDecisionKind::Approved,
        }
    }

    fn sample_attestor_data() -> AttestorData {
        AttestorData {
            attestation_id: OpaqueId::new("attestation-1").unwrap(),
            issuer: IssuerId::new(I_DEV_BASELINE_ISSUER).unwrap(),
            subject_digest: OpaqueId::new("b".repeat(64)).unwrap(),
            issued_at: "2026-01-01T00:00:00Z".into(),
        }
    }

    #[test]
    fn authorization_decision_wire_states_are_compatible_and_strict() {
        let absent = AuthorizationDecisionRef::absent();
        assert_eq!(serde_json::to_string(&absent).unwrap(), "\"absent\"");
        assert!(
            serde_json::from_str::<AuthorizationDecisionRef>("\"absent\"")
                .unwrap()
                .is_absent()
        );

        let pending = AuthorizationDecisionRef::pending_i();
        assert_eq!(serde_json::to_string(&pending).unwrap(), "null");
        assert!(serde_json::from_str::<AuthorizationDecisionRef>("null")
            .unwrap()
            .is_pending());
        assert!(
            serde_json::from_str::<AuthorizationDecisionRef>("\"pending_i\"")
                .unwrap()
                .is_pending()
        );

        let issued = AuthorizationDecisionRef::from_issued_data(sample_decision_data()).unwrap();
        let wire = serde_json::to_value(&issued).unwrap();
        assert_eq!(wire["decision_id"], "decision-1");
        assert_eq!(wire["issuer"], I_DEV_BASELINE_ISSUER);
        assert_eq!(wire["decision_kind"], "Approved");
        assert_eq!(
            serde_json::from_value::<AuthorizationDecisionRef>(wire).unwrap(),
            issued
        );

        assert!(serde_json::from_str::<AuthorizationDecisionRef>(
            r#"{"decision_id":"decision-1","issuer":"i-owner-proxy/dev-baseline-v1","subject_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","issued_at":"2026-01-01T00:00:00Z","decision_kind":"Unknown"}"#
        )
        .is_err());

        assert!(serde_json::from_str::<AuthorizationDecisionRef>(
            r#"{"decision_id":"decision-1","issuer":"i-owner-proxy/dev-baseline-v1","subject_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","issued_at":"2026-01-01T00:00:00Z","decision_kind":"Approved","extra":true}"#
        )
        .is_err());
    }

    #[test]
    fn attestor_wire_states_are_null_or_strict_issued_object() {
        let pending = AttestorRef::pending_i();
        assert_eq!(serde_json::to_string(&pending).unwrap(), "null");
        assert!(serde_json::from_str::<AttestorRef>("null")
            .unwrap()
            .is_pending());

        let issued = AttestorRef::from_issued_data(sample_attestor_data()).unwrap();
        let wire = serde_json::to_value(&issued).unwrap();
        assert_eq!(wire["attestation_id"], "attestation-1");
        assert_eq!(serde_json::from_value::<AttestorRef>(wire).unwrap(), issued);

        assert!(serde_json::from_str::<AttestorRef>(
            r#"{"attestation_id":"attestation-1","issuer":"i-owner-proxy/dev-baseline-v1","subject_digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}"#
        )
        .is_err());
    }

    #[test]
    fn issued_candidates_reject_invalid_fields() {
        let mut decision = sample_decision_data();
        decision.issuer = IssuerId::new("untrusted-issuer").unwrap();
        assert_eq!(
            AuthorizationDecisionRef::from_issued_data(decision),
            Err(DomainError::InvalidCanonicalCommitField("issuer"))
        );

        let mut attestor = sample_attestor_data();
        attestor.subject_digest = OpaqueId::new("not-a-digest").unwrap();
        assert_eq!(
            AttestorRef::from_issued_data(attestor),
            Err(DomainError::InvalidCanonicalCommitField("subject_digest"))
        );
    }
}
