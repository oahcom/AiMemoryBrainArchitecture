#![recursion_limit = "512"]

pub mod evidence {
    use serde::Serialize;

    #[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize)]
    pub enum EvidenceKind {
        #[serde(rename = "FINAL_REQUEST_SUBMITTED")]
        FinalRequestSubmitted,
        #[serde(rename = "APPLIED_CONTEXT_OBSERVED")]
        AppliedContextObserved,
        #[serde(rename = "EXECUTION_STARTED")]
        ExecutionStarted,
        #[serde(rename = "RECONCILIATION_OBSERVED")]
        ReconciliationObserved,
    }

    #[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize)]
    pub enum EvidenceTier {
        #[serde(rename = "TIER_1")]
        Tier1,
        #[serde(rename = "TIER_2")]
        Tier2,
        #[serde(rename = "TIER_3")]
        Tier3,
    }

    #[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize)]
    pub enum ManagedRegionCoverage {
        #[serde(rename = "COMPLETE")]
        Complete,
        #[serde(rename = "PARTIAL")]
        Partial,
        #[serde(rename = "BYPASSED")]
        Bypassed,
        #[serde(rename = "UNKNOWN")]
        Unknown,
    }

    /// 只能经由 `validate::from_strict_value` 构造。
    ///
    /// 刻意**不派生** `Deserialize`：所有拒绝语义（未知字段、枚举、const、
    /// hex64、十进制、RFC3339、两条 if/then）都在 `from_strict_value` 里。
    /// 若派生 `Deserialize`，任何人 `serde_json::from_str::<AppliedDeliveryEvidence>`
    /// 就能绕过全部校验，得到一份结构合法但语义非法的证据。
    #[derive(Clone, Debug, Eq, PartialEq, Serialize)]
    pub struct AppliedDeliveryEvidence {
        pub(super) schema_artifact_revision: String,
        pub(super) message_type: String,
        pub(super) issuer_ref: String,
        pub(super) sender_authority_ref: String,
        pub(super) sender_subject_ref: String,
        pub(super) audience: String,
        pub(super) message_id: String,
        pub(super) message_nonce: String,
        pub(super) signing_sequence_namespace_ref: String,
        pub(super) signing_record_sequence: String,
        pub(super) signature_profile_id: String,
        pub(super) key_id_ref: String,
        pub(super) key_version: String,
        pub(super) adapter_instance_ref: String,
        pub(super) runtime_session_ref: String,
        pub(super) delivery_id: String,
        pub(super) delivery_attempt_id: String,
        pub(super) inference_request_id: String,
        pub(super) final_request_boundary_id: String,
        pub(super) adapter_capability_epoch: String,
        pub(super) evidence_kind: EvidenceKind,
        pub(super) evidence_tier: EvidenceTier,
        pub(super) adapter_ref: String,
        pub(super) runtime_instance_ref: String,
        pub(super) context_id: String,
        pub(super) context_version: String,
        pub(super) materialized_context_version: String,
        pub(super) final_request_boundary_type: String,
        pub(super) managed_region_id: String,
        pub(super) managed_region_revision: String,
        pub(super) managed_region_inventory_digest: String,
        pub(super) managed_region_coverage: ManagedRegionCoverage,
        pub(super) managed_region_digest: String,
        pub(super) digest_profile: String,
        pub(super) evidence_issuer_ref: String,
        pub(super) evidence_schema_version: String,
        pub(super) submission_observed_at: String,
        #[serde(skip_serializing_if = "Option::is_none", default)]
        pub(super) submission_monotonic_sequence: Option<String>,
        pub(super) correlation_ref: String,
        pub(super) causation_ref: String,
        pub(super) audit_ref: String,
        pub(super) c_submit_outcome_ref: String,
        pub(super) c_outcome_record_ref: String,
        pub(super) c_outcome_record_sequence: String,
        pub(super) c_outcome_payload_digest: String,
        pub(super) payload_digest: String,
        pub(super) signature: String,
        pub(super) integrity_proof_ref: String,
    }

    impl AppliedDeliveryEvidence {
        pub fn schema_artifact_revision(&self) -> &str {
            &self.schema_artifact_revision
        }
        pub fn message_type(&self) -> &str {
            &self.message_type
        }
        pub fn issuer_ref(&self) -> &str {
            &self.issuer_ref
        }
        pub fn sender_authority_ref(&self) -> &str {
            &self.sender_authority_ref
        }
        pub fn sender_subject_ref(&self) -> &str {
            &self.sender_subject_ref
        }
        pub fn audience(&self) -> &str {
            &self.audience
        }
        pub fn message_id(&self) -> &str {
            &self.message_id
        }
        pub fn message_nonce(&self) -> &str {
            &self.message_nonce
        }
        pub fn signing_sequence_namespace_ref(&self) -> &str {
            &self.signing_sequence_namespace_ref
        }
        pub fn signing_record_sequence(&self) -> &str {
            &self.signing_record_sequence
        }
        pub fn signature_profile_id(&self) -> &str {
            &self.signature_profile_id
        }
        pub fn key_id_ref(&self) -> &str {
            &self.key_id_ref
        }
        pub fn key_version(&self) -> &str {
            &self.key_version
        }
        pub fn adapter_instance_ref(&self) -> &str {
            &self.adapter_instance_ref
        }
        pub fn runtime_session_ref(&self) -> &str {
            &self.runtime_session_ref
        }
        pub fn delivery_id(&self) -> &str {
            &self.delivery_id
        }
        pub fn delivery_attempt_id(&self) -> &str {
            &self.delivery_attempt_id
        }
        pub fn inference_request_id(&self) -> &str {
            &self.inference_request_id
        }
        pub fn final_request_boundary_id(&self) -> &str {
            &self.final_request_boundary_id
        }
        pub fn adapter_capability_epoch(&self) -> &str {
            &self.adapter_capability_epoch
        }
        pub fn evidence_kind(&self) -> EvidenceKind {
            self.evidence_kind
        }
        pub fn evidence_tier(&self) -> EvidenceTier {
            self.evidence_tier
        }
        pub fn adapter_ref(&self) -> &str {
            &self.adapter_ref
        }
        pub fn runtime_instance_ref(&self) -> &str {
            &self.runtime_instance_ref
        }
        pub fn context_id(&self) -> &str {
            &self.context_id
        }
        pub fn context_version(&self) -> &str {
            &self.context_version
        }
        pub fn materialized_context_version(&self) -> &str {
            &self.materialized_context_version
        }
        pub fn final_request_boundary_type(&self) -> &str {
            &self.final_request_boundary_type
        }
        pub fn managed_region_id(&self) -> &str {
            &self.managed_region_id
        }
        pub fn managed_region_revision(&self) -> &str {
            &self.managed_region_revision
        }
        pub fn managed_region_inventory_digest(&self) -> &str {
            &self.managed_region_inventory_digest
        }
        pub fn managed_region_coverage(&self) -> ManagedRegionCoverage {
            self.managed_region_coverage
        }
        pub fn managed_region_digest(&self) -> &str {
            &self.managed_region_digest
        }
        pub fn digest_profile(&self) -> &str {
            &self.digest_profile
        }
        pub fn evidence_issuer_ref(&self) -> &str {
            &self.evidence_issuer_ref
        }
        pub fn evidence_schema_version(&self) -> &str {
            &self.evidence_schema_version
        }
        pub fn submission_observed_at(&self) -> &str {
            &self.submission_observed_at
        }
        pub fn submission_monotonic_sequence(&self) -> Option<&str> {
            self.submission_monotonic_sequence.as_deref()
        }
        pub fn correlation_ref(&self) -> &str {
            &self.correlation_ref
        }
        pub fn causation_ref(&self) -> &str {
            &self.causation_ref
        }
        pub fn audit_ref(&self) -> &str {
            &self.audit_ref
        }
        pub fn c_submit_outcome_ref(&self) -> &str {
            &self.c_submit_outcome_ref
        }
        pub fn c_outcome_record_ref(&self) -> &str {
            &self.c_outcome_record_ref
        }
        pub fn c_outcome_record_sequence(&self) -> &str {
            &self.c_outcome_record_sequence
        }
        pub fn c_outcome_payload_digest(&self) -> &str {
            &self.c_outcome_payload_digest
        }
        pub fn payload_digest(&self) -> &str {
            &self.payload_digest
        }
        pub fn signature(&self) -> &str {
            &self.signature
        }
        pub fn integrity_proof_ref(&self) -> &str {
            &self.integrity_proof_ref
        }
    }
}

pub mod strict_json {
    use serde_json::{Map, Number, Value};
    use std::collections::BTreeSet;

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub enum StrictJsonError {
        DuplicateKey { path: String, key: String },
        TrailingCharacters,
        UnexpectedEof,
        InvalidEscape,
        InvalidNumber,
        InvalidLiteral,
        DepthExceeded,
        InvalidUtf8,
    }

    struct Parser<'a> {
        input: &'a [u8],
        pos: usize,
    }

    impl<'a> Parser<'a> {
        fn peek(&self) -> Option<u8> {
            self.input.get(self.pos).copied()
        }

        fn whitespace(&mut self) {
            while matches!(self.peek(), Some(b' ' | b'\n' | b'\r' | b'\t')) {
                self.pos += 1;
            }
        }

        fn string(&mut self) -> Result<String, StrictJsonError> {
            if self.peek() != Some(b'"') {
                return Err(if self.peek().is_none() {
                    StrictJsonError::UnexpectedEof
                } else {
                    StrictJsonError::InvalidEscape
                });
            }

            let start = self.pos;
            self.pos += 1;
            let mut escaped = false;

            loop {
                let byte = self.peek().ok_or(StrictJsonError::UnexpectedEof)?;
                self.pos += 1;

                if escaped {
                    if !matches!(
                        byte,
                        b'"' | b'\\' | b'/' | b'b' | b'f' | b'n' | b'r' | b't' | b'u'
                    ) {
                        return Err(StrictJsonError::InvalidEscape);
                    }
                    if byte == b'u' {
                        for _ in 0..4 {
                            let hex = self.peek().ok_or(StrictJsonError::UnexpectedEof)?;
                            if !hex.is_ascii_hexdigit() {
                                return Err(StrictJsonError::InvalidEscape);
                            }
                            self.pos += 1;
                        }
                    }
                    escaped = false;
                    continue;
                }

                match byte {
                    b'\\' => escaped = true,
                    b'"' => break,
                    0x00..=0x1f => return Err(StrictJsonError::InvalidEscape),
                    _ => {}
                }
            }

            serde_json::from_slice::<String>(&self.input[start..self.pos])
                .map_err(|_| StrictJsonError::InvalidEscape)
        }

        fn number(&mut self) -> Result<Value, StrictJsonError> {
            let start = self.pos;

            if self.peek() == Some(b'-') {
                self.pos += 1;
            }

            match self.peek() {
                Some(b'0') => {
                    self.pos += 1;
                    if matches!(self.peek(), Some(b'0'..=b'9')) {
                        return Err(StrictJsonError::InvalidNumber);
                    }
                }
                Some(b'1'..=b'9') => {
                    self.pos += 1;
                    while matches!(self.peek(), Some(b'0'..=b'9')) {
                        self.pos += 1;
                    }
                }
                _ => return Err(StrictJsonError::InvalidNumber),
            }

            if self.peek() == Some(b'.') {
                self.pos += 1;
                let fraction_start = self.pos;
                while matches!(self.peek(), Some(b'0'..=b'9')) {
                    self.pos += 1;
                }
                if self.pos == fraction_start {
                    return Err(StrictJsonError::InvalidNumber);
                }
            }

            if matches!(self.peek(), Some(b'e' | b'E')) {
                self.pos += 1;
                if matches!(self.peek(), Some(b'+' | b'-')) {
                    self.pos += 1;
                }
                let exponent_start = self.pos;
                while matches!(self.peek(), Some(b'0'..=b'9')) {
                    self.pos += 1;
                }
                if self.pos == exponent_start {
                    return Err(StrictJsonError::InvalidNumber);
                }
            }

            let bytes = &self.input[start..self.pos];
            let text = std::str::from_utf8(bytes).map_err(|_| StrictJsonError::InvalidUtf8)?;
            let number = text
                .parse::<Number>()
                .map_err(|_| StrictJsonError::InvalidNumber)?;
            Ok(Value::Number(number))
        }

        fn literal(&mut self, expected: &[u8], value: Value) -> Result<Value, StrictJsonError> {
            let end = self.pos.saturating_add(expected.len());
            let actual = self
                .input
                .get(self.pos..end)
                .ok_or(StrictJsonError::UnexpectedEof)?;
            if actual != expected {
                return Err(StrictJsonError::InvalidLiteral);
            }
            self.pos = end;
            Ok(value)
        }

        fn value(&mut self, path: &str, depth: usize) -> Result<Value, StrictJsonError> {
            if depth > 128 {
                return Err(StrictJsonError::DepthExceeded);
            }
            self.whitespace();

            match self.peek() {
                Some(b'{') => self.object(path, depth + 1),
                Some(b'[') => self.array(path, depth + 1),
                Some(b'"') => self.string().map(Value::String),
                Some(b'-' | b'0'..=b'9') => self.number(),
                Some(b't') => self.literal(b"true", Value::Bool(true)),
                Some(b'f') => self.literal(b"false", Value::Bool(false)),
                Some(b'n') => self.literal(b"null", Value::Null),
                None => Err(StrictJsonError::UnexpectedEof),
                _ => Err(StrictJsonError::InvalidLiteral),
            }
        }

        fn object(&mut self, path: &str, depth: usize) -> Result<Value, StrictJsonError> {
            self.pos += 1;
            self.whitespace();
            let mut object = Map::new();
            let mut keys = BTreeSet::new();

            if self.peek() == Some(b'}') {
                self.pos += 1;
                return Ok(Value::Object(object));
            }

            loop {
                self.whitespace();
                if self.peek().is_none() {
                    return Err(StrictJsonError::UnexpectedEof);
                }
                let key = self.string()?;
                if !keys.insert(key.clone()) {
                    return Err(StrictJsonError::DuplicateKey {
                        path: path.to_owned(),
                        key,
                    });
                }

                self.whitespace();
                if self.peek() != Some(b':') {
                    return Err(if self.peek().is_none() {
                        StrictJsonError::UnexpectedEof
                    } else {
                        StrictJsonError::InvalidLiteral
                    });
                }
                self.pos += 1;

                let child_path = format!("{}.{}", path, key);
                let child = self.value(&child_path, depth)?;
                object.insert(key, child);

                self.whitespace();
                match self.peek() {
                    Some(b',') => self.pos += 1,
                    Some(b'}') => {
                        self.pos += 1;
                        break;
                    }
                    None => return Err(StrictJsonError::UnexpectedEof),
                    _ => return Err(StrictJsonError::InvalidLiteral),
                }
            }

            Ok(Value::Object(object))
        }

        fn array(&mut self, path: &str, depth: usize) -> Result<Value, StrictJsonError> {
            self.pos += 1;
            self.whitespace();
            let mut values = Vec::new();

            if self.peek() == Some(b']') {
                self.pos += 1;
                return Ok(Value::Array(values));
            }

            loop {
                let child_path = format!("{}[{}]", path, values.len());
                values.push(self.value(&child_path, depth)?);
                self.whitespace();

                match self.peek() {
                    Some(b',') => self.pos += 1,
                    Some(b']') => {
                        self.pos += 1;
                        break;
                    }
                    None => return Err(StrictJsonError::UnexpectedEof),
                    _ => return Err(StrictJsonError::InvalidLiteral),
                }
            }

            Ok(Value::Array(values))
        }
    }

    pub fn parse_strict(input: &[u8]) -> Result<Value, StrictJsonError> {
        std::str::from_utf8(input).map_err(|_| StrictJsonError::InvalidUtf8)?;
        let mut parser = Parser { input, pos: 0 };
        parser.whitespace();
        let value = parser.value("$", 0)?;
        parser.whitespace();

        if parser.pos != input.len() {
            return Err(StrictJsonError::TrailingCharacters);
        }
        Ok(value)
    }
}

pub mod validate {
    use crate::evidence::{
        AppliedDeliveryEvidence, EvidenceKind, EvidenceTier, ManagedRegionCoverage,
    };
    use serde_json::Value;
    use std::collections::BTreeSet;

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub enum EvidenceError {
        InvalidJson(crate::strict_json::StrictJsonError),
        MissingField(&'static str),
        UnknownField(String),
        WrongConst {
            field: &'static str,
            expected: &'static str,
            actual: String,
        },
        InvalidEnum {
            field: &'static str,
            value: String,
        },
        InvalidDecimal {
            field: &'static str,
            value: String,
        },
        InvalidHex64 {
            field: &'static str,
            value: String,
        },
        InvalidDateTime {
            field: &'static str,
            value: String,
        },
        OutOfRange {
            field: &'static str,
            value: u64,
            min: u64,
            max: u64,
        },
        InvalidInteger {
            field: &'static str,
            value: String,
        },
        InvalidDigitString {
            field: &'static str,
            value: String,
        },
        InvalidLsn {
            field: &'static str,
            value: String,
        },
        InvalidString {
            field: &'static str,
            value: String,
        },
        Tier1RequiresCompleteCoverage,
        FinalRequestRequiresMonotonicSequence,
        Tier1RequiresMaterializedVersionMatch {
            context_version: String,
            materialized: String,
        },
        PayloadDigestMismatch {
            declared: String,
            actual: String,
        },
    }

    const REQUIRED: &[&str] = &[
        "schema_artifact_revision",
        "message_type",
        "issuer_ref",
        "sender_authority_ref",
        "sender_subject_ref",
        "audience",
        "message_id",
        "message_nonce",
        "signing_sequence_namespace_ref",
        "signing_record_sequence",
        "signature_profile_id",
        "key_id_ref",
        "key_version",
        "adapter_instance_ref",
        "runtime_session_ref",
        "delivery_id",
        "delivery_attempt_id",
        "inference_request_id",
        "final_request_boundary_id",
        "adapter_capability_epoch",
        "evidence_kind",
        "evidence_tier",
        "adapter_ref",
        "runtime_instance_ref",
        "context_id",
        "context_version",
        "materialized_context_version",
        "final_request_boundary_type",
        "managed_region_id",
        "managed_region_revision",
        "managed_region_inventory_digest",
        "managed_region_coverage",
        "managed_region_digest",
        "digest_profile",
        "evidence_issuer_ref",
        "evidence_schema_version",
        "submission_observed_at",
        "correlation_ref",
        "causation_ref",
        "audit_ref",
        "c_submit_outcome_ref",
        "c_outcome_record_ref",
        "c_outcome_record_sequence",
        "c_outcome_payload_digest",
        "payload_digest",
        "signature",
        "integrity_proof_ref",
    ];

    pub(crate) const ALL_FIELDS: &[&str] = &[
        "schema_artifact_revision",
        "message_type",
        "issuer_ref",
        "sender_authority_ref",
        "sender_subject_ref",
        "audience",
        "message_id",
        "message_nonce",
        "signing_sequence_namespace_ref",
        "signing_record_sequence",
        "signature_profile_id",
        "key_id_ref",
        "key_version",
        "adapter_instance_ref",
        "runtime_session_ref",
        "delivery_id",
        "delivery_attempt_id",
        "inference_request_id",
        "final_request_boundary_id",
        "adapter_capability_epoch",
        "evidence_kind",
        "evidence_tier",
        "adapter_ref",
        "runtime_instance_ref",
        "context_id",
        "context_version",
        "materialized_context_version",
        "final_request_boundary_type",
        "managed_region_id",
        "managed_region_revision",
        "managed_region_inventory_digest",
        "managed_region_coverage",
        "managed_region_digest",
        "digest_profile",
        "evidence_issuer_ref",
        "evidence_schema_version",
        "submission_observed_at",
        "submission_monotonic_sequence",
        "correlation_ref",
        "causation_ref",
        "audit_ref",
        "c_submit_outcome_ref",
        "c_outcome_record_ref",
        "c_outcome_record_sequence",
        "c_outcome_payload_digest",
        "payload_digest",
        "signature",
        "integrity_proof_ref",
    ];

    fn decimal(value: &str) -> bool {
        !value.is_empty()
            && value.bytes().all(|b| b.is_ascii_digit())
            && (value == "0" || !value.starts_with('0'))
    }

    fn hex64(value: &str) -> bool {
        value.len() == 64
            && value
                .bytes()
                .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    }

    fn leap_year(year: u32) -> bool {
        year.is_multiple_of(4) && (!year.is_multiple_of(100) || year.is_multiple_of(400))
    }

    fn datetime(value: &str) -> bool {
        let bytes = value.as_bytes();
        if bytes.len() < 20 {
            return false;
        }
        if bytes.get(4) != Some(&b'-')
            || bytes.get(7) != Some(&b'-')
            || !matches!(bytes.get(10), Some(b'T' | b't'))
            || bytes.get(13) != Some(&b':')
            || bytes.get(16) != Some(&b':')
        {
            return false;
        }
        for range in [0..4, 5..7, 8..10, 11..13, 14..16, 17..19] {
            if !bytes[range].iter().all(u8::is_ascii_digit) {
                return false;
            }
        }

        let number = |a: usize, b: usize| -> u32 { value[a..b].parse::<u32>().unwrap_or(0) };
        let year = number(0, 4);
        let month = number(5, 7);
        let day = number(8, 10);
        let hour = number(11, 13);
        let minute = number(14, 16);
        let second = number(17, 19);

        if !(1..=12).contains(&month) || !(0..=23).contains(&hour) || minute > 59 || second > 60 {
            return false;
        }

        let days = match month {
            1 | 3 | 5 | 7 | 8 | 10 | 12 => 31,
            4 | 6 | 9 | 11 => 30,
            2 if leap_year(year) => 29,
            2 => 28,
            _ => return false,
        };
        if day == 0 || day > days {
            return false;
        }

        let mut index = 19;
        if bytes.get(index) == Some(&b'.') {
            index += 1;
            let start = index;
            while matches!(bytes.get(index), Some(b'0'..=b'9')) {
                index += 1;
            }
            if index == start {
                return false;
            }
        }

        match bytes.get(index) {
            Some(b'Z' | b'z') => index += 1,
            Some(b'+' | b'-') => {
                if bytes.len() < index + 6
                    || !bytes[index + 1..index + 3].iter().all(u8::is_ascii_digit)
                    || bytes[index + 3] != b':'
                    || !bytes[index + 4..index + 6].iter().all(u8::is_ascii_digit)
                {
                    return false;
                }
                let tz_hour = number(index + 1, index + 3);
                let tz_minute = number(index + 4, index + 6);
                if tz_hour > 23 || tz_minute > 59 {
                    return false;
                }
                index += 6;
            }
            _ => return false,
        }
        index == bytes.len()
    }

    fn string_field<'a>(value: &'a Value, field: &'static str) -> Result<&'a str, EvidenceError> {
        value
            .get(field)
            .and_then(Value::as_str)
            .filter(|s| !s.is_empty())
            .ok_or(EvidenceError::MissingField(field))
    }

    pub(super) fn from_strict_value(
        value: &Value,
    ) -> Result<AppliedDeliveryEvidence, EvidenceError> {
        let object = value
            .as_object()
            .ok_or(EvidenceError::MissingField("object"))?;

        for key in object.keys() {
            if !ALL_FIELDS.contains(&key.as_str()) {
                return Err(EvidenceError::UnknownField(key.clone()));
            }
        }

        macro_rules! required_string {
            ($field:ident) => {
                string_field(value, stringify!($field))?.to_owned()
            };
        }

        let evidence_kind = match string_field(value, "evidence_kind")? {
            "FINAL_REQUEST_SUBMITTED" => EvidenceKind::FinalRequestSubmitted,
            "APPLIED_CONTEXT_OBSERVED" => EvidenceKind::AppliedContextObserved,
            "EXECUTION_STARTED" => EvidenceKind::ExecutionStarted,
            "RECONCILIATION_OBSERVED" => EvidenceKind::ReconciliationObserved,
            other => {
                return Err(EvidenceError::InvalidEnum {
                    field: "evidence_kind",
                    value: other.to_owned(),
                })
            }
        };

        let evidence_tier = match string_field(value, "evidence_tier")? {
            "TIER_1" => EvidenceTier::Tier1,
            "TIER_2" => EvidenceTier::Tier2,
            "TIER_3" => EvidenceTier::Tier3,
            other => {
                return Err(EvidenceError::InvalidEnum {
                    field: "evidence_tier",
                    value: other.to_owned(),
                })
            }
        };

        let managed_region_coverage = match string_field(value, "managed_region_coverage")? {
            "COMPLETE" => ManagedRegionCoverage::Complete,
            "PARTIAL" => ManagedRegionCoverage::Partial,
            "BYPASSED" => ManagedRegionCoverage::Bypassed,
            "UNKNOWN" => ManagedRegionCoverage::Unknown,
            other => {
                return Err(EvidenceError::InvalidEnum {
                    field: "managed_region_coverage",
                    value: other.to_owned(),
                })
            }
        };

        let evidence = AppliedDeliveryEvidence {
            schema_artifact_revision: required_string!(schema_artifact_revision),
            message_type: required_string!(message_type),
            issuer_ref: required_string!(issuer_ref),
            sender_authority_ref: required_string!(sender_authority_ref),
            sender_subject_ref: required_string!(sender_subject_ref),
            audience: required_string!(audience),
            message_id: required_string!(message_id),
            message_nonce: required_string!(message_nonce),
            signing_sequence_namespace_ref: required_string!(signing_sequence_namespace_ref),
            signing_record_sequence: required_string!(signing_record_sequence),
            signature_profile_id: required_string!(signature_profile_id),
            key_id_ref: required_string!(key_id_ref),
            key_version: required_string!(key_version),
            adapter_instance_ref: required_string!(adapter_instance_ref),
            runtime_session_ref: required_string!(runtime_session_ref),
            delivery_id: required_string!(delivery_id),
            delivery_attempt_id: required_string!(delivery_attempt_id),
            inference_request_id: required_string!(inference_request_id),
            final_request_boundary_id: required_string!(final_request_boundary_id),
            adapter_capability_epoch: required_string!(adapter_capability_epoch),
            evidence_kind,
            evidence_tier,
            adapter_ref: required_string!(adapter_ref),
            runtime_instance_ref: required_string!(runtime_instance_ref),
            context_id: required_string!(context_id),
            context_version: required_string!(context_version),
            materialized_context_version: required_string!(materialized_context_version),
            final_request_boundary_type: required_string!(final_request_boundary_type),
            managed_region_id: required_string!(managed_region_id),
            managed_region_revision: required_string!(managed_region_revision),
            managed_region_inventory_digest: required_string!(managed_region_inventory_digest),
            managed_region_coverage,
            managed_region_digest: required_string!(managed_region_digest),
            digest_profile: required_string!(digest_profile),
            evidence_issuer_ref: required_string!(evidence_issuer_ref),
            evidence_schema_version: required_string!(evidence_schema_version),
            submission_observed_at: required_string!(submission_observed_at),
            submission_monotonic_sequence: match value.get("submission_monotonic_sequence") {
                None => None,
                Some(v) => Some(
                    v.as_str()
                        .filter(|s| !s.is_empty())
                        .ok_or(EvidenceError::MissingField("submission_monotonic_sequence"))?
                        .to_owned(),
                ),
            },
            correlation_ref: required_string!(correlation_ref),
            causation_ref: required_string!(causation_ref),
            audit_ref: required_string!(audit_ref),
            c_submit_outcome_ref: required_string!(c_submit_outcome_ref),
            c_outcome_record_ref: required_string!(c_outcome_record_ref),
            c_outcome_record_sequence: required_string!(c_outcome_record_sequence),
            c_outcome_payload_digest: required_string!(c_outcome_payload_digest),
            payload_digest: required_string!(payload_digest),
            signature: required_string!(signature),
            integrity_proof_ref: required_string!(integrity_proof_ref),
        };

        validate_evidence(&evidence)?;
        Ok(evidence)
    }

    pub(super) fn validate_evidence(
        evidence: &AppliedDeliveryEvidence,
    ) -> Result<(), EvidenceError> {
        let value = serde_json::to_value(evidence)
            .map_err(|_| EvidenceError::MissingField("serialization"))?;
        let object = value
            .as_object()
            .ok_or(EvidenceError::MissingField("object"))?;

        for field in REQUIRED {
            string_field(&value, field)?;
        }

        let consts = [
            ("schema_artifact_revision", "1.0.0"),
            ("message_type", "APPLIED_DELIVERY_EVIDENCE_RECORDED"),
        ];
        for (field, expected) in consts {
            let actual = string_field(&value, field)?.to_owned();
            if actual != expected {
                return Err(EvidenceError::WrongConst {
                    field,
                    expected,
                    actual,
                });
            }
        }

        for field in ["signing_record_sequence", "c_outcome_record_sequence"] {
            let actual = string_field(&value, field)?;
            if !decimal(actual) {
                return Err(EvidenceError::InvalidDecimal {
                    field,
                    value: actual.to_owned(),
                });
            }
        }

        if let Some(sequence) = evidence.submission_monotonic_sequence.as_deref() {
            if !decimal(sequence) {
                return Err(EvidenceError::InvalidDecimal {
                    field: "submission_monotonic_sequence",
                    value: sequence.to_owned(),
                });
            }
        }

        for field in [
            "managed_region_inventory_digest",
            "managed_region_digest",
            "c_outcome_payload_digest",
            "payload_digest",
        ] {
            let actual = string_field(&value, field)?;
            if !hex64(actual) {
                return Err(EvidenceError::InvalidHex64 {
                    field,
                    value: actual.to_owned(),
                });
            }
        }

        let observed = string_field(&value, "submission_observed_at")?;
        if !datetime(observed) {
            return Err(EvidenceError::InvalidDateTime {
                field: "submission_observed_at",
                value: observed.to_owned(),
            });
        }

        if evidence.evidence_tier == EvidenceTier::Tier1 {
            if evidence.managed_region_coverage != ManagedRegionCoverage::Complete {
                return Err(EvidenceError::Tier1RequiresCompleteCoverage);
            }
            if evidence.materialized_context_version != evidence.context_version {
                return Err(EvidenceError::Tier1RequiresMaterializedVersionMatch {
                    context_version: evidence.context_version.clone(),
                    materialized: evidence.materialized_context_version.clone(),
                });
            }
        }

        if evidence.evidence_kind == EvidenceKind::FinalRequestSubmitted
            && evidence.submission_monotonic_sequence.is_none()
        {
            return Err(EvidenceError::FinalRequestRequiresMonotonicSequence);
        }

        let actual_digest = crate::digest::p0_digest(evidence)?;
        if actual_digest != evidence.payload_digest {
            return Err(EvidenceError::PayloadDigestMismatch {
                declared: evidence.payload_digest.clone(),
                actual: actual_digest,
            });
        }

        let known: BTreeSet<&str> = ALL_FIELDS.iter().copied().collect();
        for key in object.keys() {
            if !known.contains(key.as_str()) {
                return Err(EvidenceError::UnknownField(key.clone()));
            }
        }

        Ok(())
    }

    // Storage.PreparedParticipantReceipt validation.
    //
    // These field lists deliberately remain separate from ALL_FIELDS:
    // AppliedDeliveryEvidence and PreparedParticipantReceipt are different
    // protocol messages with different schemas.

    const RECEIPT_FIELDS: &[&str] = &[
        "schema_id",
        "schema_version",
        "message_type",
        "message_id",
        "message_nonce",
        "signature_envelope",
        "payload",
    ];

    const ENVELOPE_FIELDS: &[&str] = &[
        "payload_type",
        "schema_version",
        "issuer_principal_ref",
        "subject_ref",
        "owner_authority_ref",
        "audience_ref",
        "target_environment_ref",
        "purpose",
        "key_id",
        "key_version",
        "algorithm_profile_ref",
        "canonicalization_profile_ref",
        "digest_profile_ref",
        "issued_at",
        "trust_status_evidence_ref",
        "payload_digest",
        "signature",
    ];

    const PAYLOAD_FIELDS: &[&str] = &[
        "prepared_participant_ref",
        "prepared_transaction_gid",
        "postgresql_native_xid",
        "canonical_authority_db_ref",
        "database_incarnation_ref",
        "postgresql_system_identifier",
        "postgresql_database_oid",
        "original_prepare_timeline",
        "original_prepare_lsn",
        "publication_operation_id",
        "request_digest",
        "participant_tuple_digest",
        "owner_boundary_ref",
        "causal_order_domain_ref",
        "policy_domain_ref",
        "coc_prepare_intent_position",
        "coc_prepare_intent_digest",
        "prepare_attempt_ref",
        "prepare_attempt_generation",
        "participant_ledger_ref",
        "participant_ledger_version",
        "prepared_state",
        "prepared_observation_source",
        "prepared_observed_at",
    ];

    const ENVELOPE_REQUIRED: &[&str] = ENVELOPE_FIELDS;

    const PAYLOAD_REQUIRED: &[&str] = &[
        "prepared_participant_ref",
        "prepared_transaction_gid",
        "postgresql_native_xid",
        "canonical_authority_db_ref",
        "database_incarnation_ref",
        "postgresql_system_identifier",
        "postgresql_database_oid",
        "original_prepare_timeline",
        "original_prepare_lsn",
        "publication_operation_id",
        "request_digest",
        "participant_tuple_digest",
        "owner_boundary_ref",
        "causal_order_domain_ref",
        "policy_domain_ref",
        "coc_prepare_intent_position",
        "coc_prepare_intent_digest",
        "prepare_attempt_ref",
        "prepare_attempt_generation",
        "participant_ledger_ref",
        "participant_ledger_version",
        "prepared_state",
        "prepared_observation_source",
        "prepared_observed_at",
    ];

    fn reject_unknown_fields(
        object: &serde_json::Map<String, Value>,
        allowed: &[&str],
    ) -> Result<(), EvidenceError> {
        for key in object.keys() {
            if !allowed.contains(&key.as_str()) {
                return Err(EvidenceError::UnknownField(key.clone()));
            }
        }
        Ok(())
    }

    fn require_fields(value: &Value, fields: &[&'static str]) -> Result<(), EvidenceError> {
        for field in fields {
            if value.get(field).is_none() {
                return Err(EvidenceError::MissingField(field));
            }
        }
        Ok(())
    }

    fn receipt_string<'a>(value: &'a Value, field: &'static str) -> Result<&'a str, EvidenceError> {
        value
            .get(field)
            .and_then(Value::as_str)
            .filter(|s| !s.is_empty())
            .ok_or(EvidenceError::MissingField(field))
    }

    fn digit_string(
        value: &str,
        field: &'static str,
        max_length: usize,
    ) -> Result<(), EvidenceError> {
        if value.is_empty()
            || value.len() > max_length
            || !value.bytes().all(|b| b.is_ascii_digit())
        {
            return Err(EvidenceError::InvalidDigitString {
                field,
                value: value.to_owned(),
            });
        }
        Ok(())
    }

    fn receipt_lsn(value: &str) -> bool {
        let bytes = value.as_bytes();

        (3..=32).contains(&bytes.len())
            && bytes.iter().filter(|&&b| b == b'/').count() == 1
            && bytes
                .iter()
                .all(|&b| b == b'/' || b.is_ascii_digit() || (b'A'..=b'F').contains(&b))
            && bytes.first() != Some(&b'/')
            && bytes.last() != Some(&b'/')
    }

    fn receipt_integer(
        value: &Value,
        field: &'static str,
        min: u64,
        max: u64,
    ) -> Result<u64, EvidenceError> {
        let number = value.get(field).and_then(Value::as_u64).ok_or_else(|| {
            EvidenceError::InvalidInteger {
                field,
                value: value
                    .get(field)
                    .map(Value::to_string)
                    .unwrap_or_else(|| "null".to_owned()),
            }
        })?;

        if number < min || number > max {
            return Err(EvidenceError::OutOfRange {
                field,
                value: number,
                min,
                max,
            });
        }

        Ok(number)
    }

    fn validate_opaque_ref(value: &Value, field: &'static str) -> Result<(), EvidenceError> {
        let actual = receipt_string(value, field)?;
        if actual.len() > 512 {
            return Err(EvidenceError::InvalidString {
                field,
                value: actual.to_owned(),
            });
        }
        Ok(())
    }

    fn validate_receipt_digest(value: &Value, field: &'static str) -> Result<(), EvidenceError> {
        let actual = receipt_string(value, field)?;
        if !hex64(actual) {
            return Err(EvidenceError::InvalidHex64 {
                field,
                value: actual.to_owned(),
            });
        }
        Ok(())
    }

    fn validate_receipt_datetime(value: &Value, field: &'static str) -> Result<(), EvidenceError> {
        let actual = receipt_string(value, field)?;
        if !datetime(actual) {
            return Err(EvidenceError::InvalidDateTime {
                field,
                value: actual.to_owned(),
            });
        }
        Ok(())
    }

    pub(super) fn validate_storage_receipt_value(value: &Value) -> Result<(), EvidenceError> {
        let root = value
            .as_object()
            .ok_or(EvidenceError::MissingField("object"))?;

        reject_unknown_fields(root, RECEIPT_FIELDS)?;
        require_fields(value, RECEIPT_FIELDS)?;

        let consts = [
            ("schema_id", "bmcp.storage-prepared-participant-proof"),
            ("schema_version", "1.0.0"),
            ("message_type", "Storage.PreparedParticipantReceipt"),
        ];

        for (field, expected) in consts {
            let actual = receipt_string(value, field)?;
            if actual != expected {
                return Err(EvidenceError::WrongConst {
                    field,
                    expected,
                    actual: actual.to_owned(),
                });
            }
        }

        for field in ["message_id", "message_nonce"] {
            validate_opaque_ref(value, field)?;
        }

        let envelope = value
            .get("signature_envelope")
            .ok_or(EvidenceError::MissingField("signature_envelope"))?;

        let envelope_object = envelope
            .as_object()
            .ok_or(EvidenceError::MissingField("signature_envelope"))?;

        reject_unknown_fields(envelope_object, ENVELOPE_FIELDS)?;
        require_fields(envelope, ENVELOPE_REQUIRED)?;

        let payload = value
            .get("payload")
            .ok_or(EvidenceError::MissingField("payload"))?;

        let payload_object = payload
            .as_object()
            .ok_or(EvidenceError::MissingField("payload"))?;

        // The payload is the union of commonPayload and
        // preparedReceiptPayload properties. This enforces
        // unevaluatedProperties: false after both schemas are applied.
        reject_unknown_fields(payload_object, PAYLOAD_FIELDS)?;
        require_fields(payload, PAYLOAD_REQUIRED)?;

        // Signature envelope consts and conditional binding.
        let envelope_schema_version = receipt_string(envelope, "schema_version")?;

        if envelope_schema_version != "1.0.0" {
            return Err(EvidenceError::WrongConst {
                field: "signature_envelope.schema_version",
                expected: "1.0.0",
                actual: envelope_schema_version.to_owned(),
            });
        }

        let payload_type = receipt_string(envelope, "payload_type")?;

        if ![
            "Storage.PreparedParticipantReceipt",
            "Storage.StorageResolutionProof",
        ]
        .contains(&payload_type)
        {
            return Err(EvidenceError::InvalidEnum {
                field: "signature_envelope.payload_type",
                value: payload_type.to_owned(),
            });
        }

        // JSON Schema if/then binding:
        // message_type == Storage.PreparedParticipantReceipt
        // implies signature_envelope.payload_type ==
        // Storage.PreparedParticipantReceipt.
        if payload_type != "Storage.PreparedParticipantReceipt" {
            return Err(EvidenceError::WrongConst {
                field: "signature_envelope.payload_type",
                expected: "Storage.PreparedParticipantReceipt",
                actual: payload_type.to_owned(),
            });
        }

        for field in [
            "issuer_principal_ref",
            "subject_ref",
            "owner_authority_ref",
            "audience_ref",
            "target_environment_ref",
            "key_id",
            "key_version",
            "algorithm_profile_ref",
            "canonicalization_profile_ref",
            "digest_profile_ref",
            "trust_status_evidence_ref",
        ] {
            validate_opaque_ref(envelope, field)?;
        }

        let purpose = receipt_string(envelope, "purpose")?;
        if purpose.len() > 128 {
            return Err(EvidenceError::InvalidString {
                field: "signature_envelope.purpose",
                value: purpose.to_owned(),
            });
        }

        validate_receipt_datetime(envelope, "issued_at")?;
        validate_receipt_digest(envelope, "payload_digest")?;

        let signature = receipt_string(envelope, "signature")?;
        if signature.len() > 16384
            || !signature
                .bytes()
                .all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-')
        {
            return Err(EvidenceError::InvalidString {
                field: "signature_envelope.signature",
                value: signature.to_owned(),
            });
        }

        // preparedReceiptPayload consts.
        for (field, expected) in [
            ("prepared_state", "PREPARED"),
            (
                "prepared_observation_source",
                "AUTHORITATIVE_WRITABLE_PRIMARY_READBACK",
            ),
        ] {
            let actual = receipt_string(payload, field)?;
            if actual != expected {
                return Err(EvidenceError::WrongConst {
                    field,
                    expected,
                    actual: actual.to_owned(),
                });
            }
        }

        for field in [
            "prepared_participant_ref",
            "canonical_authority_db_ref",
            "database_incarnation_ref",
            "publication_operation_id",
            "owner_boundary_ref",
            "causal_order_domain_ref",
            "policy_domain_ref",
            "coc_prepare_intent_position",
            "prepare_attempt_ref",
            "participant_ledger_ref",
        ] {
            validate_opaque_ref(payload, field)?;
        }

        let gid = receipt_string(payload, "prepared_transaction_gid")?;
        if gid.len() > 200
            || !gid
                .bytes()
                .all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-')
        {
            return Err(EvidenceError::InvalidString {
                field: "prepared_transaction_gid",
                value: gid.to_owned(),
            });
        }

        // Integer bounds.
        receipt_integer(payload, "postgresql_native_xid", 0, u32::MAX as u64)?;
        receipt_integer(payload, "original_prepare_timeline", 1, u32::MAX as u64)?;

        receipt_integer(
            payload,
            "prepare_attempt_generation",
            1,
            9_007_199_254_740_991,
        )?;

        receipt_integer(
            payload,
            "participant_ledger_version",
            1,
            9_007_199_254_740_991,
        )?;

        // These are digit strings, not canonical decimal numbers.
        // Leading zeroes are intentionally permitted.
        digit_string(
            receipt_string(payload, "postgresql_system_identifier")?,
            "postgresql_system_identifier",
            20,
        )?;

        digit_string(
            receipt_string(payload, "postgresql_database_oid")?,
            "postgresql_database_oid",
            10,
        )?;

        let lsn = receipt_string(payload, "original_prepare_lsn")?;
        if !receipt_lsn(lsn) {
            return Err(EvidenceError::InvalidLsn {
                field: "original_prepare_lsn",
                value: lsn.to_owned(),
            });
        }

        for field in [
            "request_digest",
            "participant_tuple_digest",
            "coc_prepare_intent_digest",
        ] {
            validate_receipt_digest(payload, field)?;
        }

        validate_receipt_datetime(payload, "prepared_observed_at")?;

        Ok(())
    }
}

pub mod storage_receipt {
    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct SignatureEnvelope {
        pub(super) payload_type: String,
        pub(super) schema_version: String,
        pub(super) issuer_principal_ref: String,
        pub(super) subject_ref: String,
        pub(super) owner_authority_ref: String,
        pub(super) audience_ref: String,
        pub(super) target_environment_ref: String,
        pub(super) purpose: String,
        pub(super) key_id: String,
        pub(super) key_version: String,
        pub(super) algorithm_profile_ref: String,
        pub(super) canonicalization_profile_ref: String,
        pub(super) digest_profile_ref: String,
        pub(super) issued_at: String,
        pub(super) trust_status_evidence_ref: String,
        pub(super) payload_digest: String,
        pub(super) signature: String,
    }

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct PreparedReceiptPayload {
        pub(super) prepared_participant_ref: String,
        pub(super) prepared_transaction_gid: String,
        pub(super) postgresql_native_xid: u32,
        pub(super) canonical_authority_db_ref: String,
        pub(super) database_incarnation_ref: String,
        pub(super) postgresql_system_identifier: String,
        pub(super) postgresql_database_oid: String,
        pub(super) original_prepare_timeline: u32,
        pub(super) original_prepare_lsn: String,
        pub(super) publication_operation_id: String,
        pub(super) request_digest: String,
        pub(super) participant_tuple_digest: String,
        pub(super) owner_boundary_ref: String,
        pub(super) causal_order_domain_ref: String,
        pub(super) policy_domain_ref: String,
        pub(super) coc_prepare_intent_position: String,
        pub(super) coc_prepare_intent_digest: String,
        pub(super) prepare_attempt_ref: String,
        pub(super) prepare_attempt_generation: u64,
        pub(super) participant_ledger_ref: String,
        pub(super) participant_ledger_version: u64,
        pub(super) prepared_state: String,
        pub(super) prepared_observation_source: String,
        pub(super) prepared_observed_at: String,
    }

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct PreparedParticipantReceipt {
        pub(super) schema_id: String,
        pub(super) schema_version: String,
        pub(super) message_type: String,
        pub(super) message_id: String,
        pub(super) message_nonce: String,
        pub(super) signature_envelope: SignatureEnvelope,
        pub(super) payload: PreparedReceiptPayload,
    }
}

pub mod digest {
    use crate::evidence::AppliedDeliveryEvidence;
    use crate::validate::EvidenceError;
    use serde_json::Value;
    use sha2::{Digest, Sha256};

    const EXCLUDED: &[&str] = &["payload_digest", "signature", "integrity_proof_ref"];

    pub fn p0_digest(evidence: &AppliedDeliveryEvidence) -> Result<String, EvidenceError> {
        let value = serde_json::to_value(evidence)
            .map_err(|_| EvidenceError::MissingField("serialization"))?;
        p0_digest_of_value(&value)
    }

    pub fn p0_digest_of_value(value: &Value) -> Result<String, EvidenceError> {
        let object = value
            .as_object()
            .ok_or(EvidenceError::MissingField("object"))?;

        for key in object.keys() {
            if !crate::validate::ALL_FIELDS.contains(&key.as_str()) {
                return Err(EvidenceError::UnknownField(key.clone()));
            }
        }

        let mut p0 = serde_json::Map::new();
        for (key, item) in object {
            if !EXCLUDED.contains(&key.as_str()) {
                p0.insert(key.clone(), item.clone());
            }
        }

        let canonical = serde_json::to_vec(&Value::Object(p0))
            .map_err(|_| EvidenceError::MissingField("canonicalization"))?;
        let hash = Sha256::digest(&canonical);
        let mut output = String::with_capacity(64);
        for byte in hash {
            use std::fmt::Write;
            let _ = write!(&mut output, "{:02x}", byte);
        }
        Ok(output)
    }
}

/// Parse untrusted wire bytes with duplicate-key rejection, then apply every
/// protocol semantic check before returning a typed evidence value.
pub fn parse_and_validate(
    raw: &[u8],
) -> Result<evidence::AppliedDeliveryEvidence, validate::EvidenceError> {
    let value = strict_json::parse_strict(raw).map_err(validate::EvidenceError::InvalidJson)?;
    validate::from_strict_value(&value)
}

/// Parse and validate a Storage.PreparedParticipantReceipt.
///
/// Duplicate JSON keys are rejected by strict_json before semantic validation.
pub fn parse_storage_receipt(
    raw: &[u8],
) -> Result<storage_receipt::PreparedParticipantReceipt, validate::EvidenceError> {
    let value = strict_json::parse_strict(raw).map_err(validate::EvidenceError::InvalidJson)?;

    validate::validate_storage_receipt_value(&value)?;

    use serde_json::Value;
    use storage_receipt::{PreparedParticipantReceipt, PreparedReceiptPayload, SignatureEnvelope};

    let envelope = &value["signature_envelope"];
    let payload = &value["payload"];

    let string =
        |object: &Value, field: &str| -> String { object[field].as_str().unwrap().to_owned() };

    let integer = |object: &Value, field: &str| -> u64 { object[field].as_u64().unwrap() };

    Ok(PreparedParticipantReceipt {
        schema_id: string(&value, "schema_id"),
        schema_version: string(&value, "schema_version"),
        message_type: string(&value, "message_type"),
        message_id: string(&value, "message_id"),
        message_nonce: string(&value, "message_nonce"),

        signature_envelope: SignatureEnvelope {
            payload_type: string(envelope, "payload_type"),
            schema_version: string(envelope, "schema_version"),
            issuer_principal_ref: string(envelope, "issuer_principal_ref"),
            subject_ref: string(envelope, "subject_ref"),
            owner_authority_ref: string(envelope, "owner_authority_ref"),
            audience_ref: string(envelope, "audience_ref"),
            target_environment_ref: string(envelope, "target_environment_ref"),
            purpose: string(envelope, "purpose"),
            key_id: string(envelope, "key_id"),
            key_version: string(envelope, "key_version"),
            algorithm_profile_ref: string(envelope, "algorithm_profile_ref"),
            canonicalization_profile_ref: string(envelope, "canonicalization_profile_ref"),
            digest_profile_ref: string(envelope, "digest_profile_ref"),
            issued_at: string(envelope, "issued_at"),
            trust_status_evidence_ref: string(envelope, "trust_status_evidence_ref"),
            payload_digest: string(envelope, "payload_digest"),
            signature: string(envelope, "signature"),
        },

        payload: PreparedReceiptPayload {
            prepared_participant_ref: string(payload, "prepared_participant_ref"),
            prepared_transaction_gid: string(payload, "prepared_transaction_gid"),
            postgresql_native_xid: integer(payload, "postgresql_native_xid") as u32,
            canonical_authority_db_ref: string(payload, "canonical_authority_db_ref"),
            database_incarnation_ref: string(payload, "database_incarnation_ref"),
            postgresql_system_identifier: string(payload, "postgresql_system_identifier"),
            postgresql_database_oid: string(payload, "postgresql_database_oid"),
            original_prepare_timeline: integer(payload, "original_prepare_timeline") as u32,
            original_prepare_lsn: string(payload, "original_prepare_lsn"),
            publication_operation_id: string(payload, "publication_operation_id"),
            request_digest: string(payload, "request_digest"),
            participant_tuple_digest: string(payload, "participant_tuple_digest"),
            owner_boundary_ref: string(payload, "owner_boundary_ref"),
            causal_order_domain_ref: string(payload, "causal_order_domain_ref"),
            policy_domain_ref: string(payload, "policy_domain_ref"),
            coc_prepare_intent_position: string(payload, "coc_prepare_intent_position"),
            coc_prepare_intent_digest: string(payload, "coc_prepare_intent_digest"),
            prepare_attempt_ref: string(payload, "prepare_attempt_ref"),
            prepare_attempt_generation: integer(payload, "prepare_attempt_generation"),
            participant_ledger_ref: string(payload, "participant_ledger_ref"),
            participant_ledger_version: integer(payload, "participant_ledger_version"),
            prepared_state: string(payload, "prepared_state"),
            prepared_observation_source: string(payload, "prepared_observation_source"),
            prepared_observed_at: string(payload, "prepared_observed_at"),
        },
    })
}

/// A message whose discriminator is known, but whose payload has not been
/// validated against its JSON Schema or any message-specific semantic rules.
///
/// The contained value is the complete root JSON object. Its fields are
/// deliberately preserved without applying the APPLIED_DELIVERY_EVIDENCE
/// field allowlist.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct StructurallyUnvalidatedMessage {
    pub message_type: &'static str,
    pub value: serde_json::Value,
}

/// The strongest validation capability established for a dispatched message.
///
/// The three states are mutually exclusive. `StructurallyParsed` means a
/// message-specific structural parser accepted the message; it does not claim
/// complete semantic validation.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DispatchValidationState {
    /// The message passed its complete message-specific semantic validator.
    SemanticallyValidated,

    /// The message passed its message-specific structural parser, but complete
    /// semantic validation is not established.
    StructurallyParsed,

    /// Only the root `message_type` discriminator was recognized.
    RootDiscriminatorOnly,
}

/// Result of dispatching a strictly parsed BMCP message.
///
/// `AppliedDeliveryEvidenceRecorded` is the only variant backed by complete
/// semantic validation. `StoragePreparedParticipantReceipt` is backed by its
/// message-specific structural parser. Every other variant is an explicitly
/// structurally-unvalidated value.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum DispatchMessage {
    AppliedDeliveryEvidenceRecorded(Box<evidence::AppliedDeliveryEvidence>),

    CocParticipantManifestStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    CocRecoveryCutoffBatchStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    CProviderOutcomeRecordedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    IJf10TerminalDecisionObservedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    Jf10BridgeReconciliationRecordedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    Jf10ITerminalDecisionObservedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    Jf10PreparedParticipantRegisteredStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    Jf10PrepareIntentRegisteredStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    Jf10StorageParticipantResolvedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    OwnerAdmissionEntryStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    OwnerAdmissionSnapshotAttestationStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    OwnerGateReleaseAttestationStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    OwnerLocalGateReleaseStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    OwnerLocalPendingGateStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    ParticipantSetReconciliationStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    RecoveryCutoffBatchStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    RecoveryEpochCompletedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    RecoveryJoinProofStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    StorageJf10ParticipantResolvedStructurallyUnvalidated(StructurallyUnvalidatedMessage),
    // Structural parser exists; complete semantic validation is not claimed.
    StoragePreparedParticipantReceipt(Box<storage_receipt::PreparedParticipantReceipt>),
    StorageStorageResolutionProofStructurallyUnvalidated(StructurallyUnvalidatedMessage),
}

impl DispatchMessage {
    /// Returns the schema-declared discriminator for this result.
    pub const fn message_type(&self) -> &'static str {
        match self {
            Self::AppliedDeliveryEvidenceRecorded(_) => "APPLIED_DELIVERY_EVIDENCE_RECORDED",
            Self::CocParticipantManifestStructurallyUnvalidated(_) => "COC_PARTICIPANT_MANIFEST",
            Self::CocRecoveryCutoffBatchStructurallyUnvalidated(_) => "COC_RECOVERY_CUTOFF_BATCH",
            Self::CProviderOutcomeRecordedStructurallyUnvalidated(_) => {
                "C_PROVIDER_OUTCOME_RECORDED"
            }
            Self::IJf10TerminalDecisionObservedStructurallyUnvalidated(_) => {
                "I_JF10_TERMINAL_DECISION_OBSERVED"
            }
            Self::Jf10BridgeReconciliationRecordedStructurallyUnvalidated(_) => {
                "JF10_BRIDGE_RECONCILIATION_RECORDED"
            }
            Self::Jf10ITerminalDecisionObservedStructurallyUnvalidated(_) => {
                "JF10_I_TERMINAL_DECISION_OBSERVED"
            }
            Self::Jf10PreparedParticipantRegisteredStructurallyUnvalidated(_) => {
                "JF10_PREPARED_PARTICIPANT_REGISTERED"
            }
            Self::Jf10PrepareIntentRegisteredStructurallyUnvalidated(_) => {
                "JF10_PREPARE_INTENT_REGISTERED"
            }
            Self::Jf10StorageParticipantResolvedStructurallyUnvalidated(_) => {
                "JF10_STORAGE_PARTICIPANT_RESOLVED"
            }
            Self::OwnerAdmissionEntryStructurallyUnvalidated(_) => "OWNER_ADMISSION_ENTRY",
            Self::OwnerAdmissionSnapshotAttestationStructurallyUnvalidated(_) => {
                "OWNER_ADMISSION_SNAPSHOT_ATTESTATION"
            }
            Self::OwnerGateReleaseAttestationStructurallyUnvalidated(_) => {
                "OWNER_GATE_RELEASE_ATTESTATION"
            }
            Self::OwnerLocalGateReleaseStructurallyUnvalidated(_) => "OWNER_LOCAL_GATE_RELEASE",
            Self::OwnerLocalPendingGateStructurallyUnvalidated(_) => "OWNER_LOCAL_PENDING_GATE",
            Self::ParticipantSetReconciliationStructurallyUnvalidated(_) => {
                "PARTICIPANT_SET_RECONCILIATION"
            }
            Self::RecoveryCutoffBatchStructurallyUnvalidated(_) => "RECOVERY_CUTOFF_BATCH",
            Self::RecoveryEpochCompletedStructurallyUnvalidated(_) => "RECOVERY_EPOCH_COMPLETED",
            Self::RecoveryJoinProofStructurallyUnvalidated(_) => "RECOVERY_JOIN_PROOF",
            Self::StorageJf10ParticipantResolvedStructurallyUnvalidated(_) => {
                "STORAGE_JF10_PARTICIPANT_RESOLVED"
            }
            Self::StoragePreparedParticipantReceipt(_) => "Storage.PreparedParticipantReceipt",
            Self::StorageStorageResolutionProofStructurallyUnvalidated(_) => {
                "Storage.StorageResolutionProof"
            }
        }
    }

    /// Reports the strongest validation capability established for this message.
    pub const fn validation_state(&self) -> DispatchValidationState {
        match self {
            Self::AppliedDeliveryEvidenceRecorded(_) => {
                DispatchValidationState::SemanticallyValidated
            }

            Self::StoragePreparedParticipantReceipt(_) => {
                DispatchValidationState::StructurallyParsed
            }

            _ => DispatchValidationState::RootDiscriminatorOnly,
        }
    }

    /// True only when the message has received no message-specific structural
    /// or semantic validation.
    pub const fn is_structurally_unvalidated(&self) -> bool {
        matches!(
            self.validation_state(),
            DispatchValidationState::RootDiscriminatorOnly
        )
    }
}

/// Errors produced while strictly parsing and dispatching a BMCP message.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum DispatchError {
    InvalidJson(strict_json::StrictJsonError),
    RootNotObject,
    MissingMessageType,
    MessageTypeNotString,
    UnknownMessageType(String),
    InvalidEvidence(validate::EvidenceError),
    InvalidStorageReceipt(validate::EvidenceError),
}

/// Strictly parse a root-level BMCP message and dispatch on its `message_type`.
///
/// The schema JSON Pointers identifying `oneOf` branches and `$defs` are
/// pointers into schema documents. They are not instance paths. The message
/// discriminator for the message types handled here is read from the root
/// instance object's `message_type` member.
///
/// APPLIED_DELIVERY_EVIDENCE_RECORDED continues through the existing strict
/// evidence validator. The other 21 known message types are parsed as strict
/// JSON and returned as explicitly structurally-unvalidated values.
///
/// In particular, non-evidence messages are not passed through
/// `validate::from_strict_value`, `validate::ALL_FIELDS`, or the P0 digest
/// allowlist. This preserves fields such as `envelope` without pretending
/// that they have been schema-validated.
pub fn parse_dispatch(raw: &[u8]) -> Result<DispatchMessage, DispatchError> {
    let value = strict_json::parse_strict(raw).map_err(DispatchError::InvalidJson)?;

    let object = value.as_object().ok_or(DispatchError::RootNotObject)?;

    let message_type = object
        .get("message_type")
        .ok_or(DispatchError::MissingMessageType)?
        .as_str()
        .ok_or(DispatchError::MessageTypeNotString)?;

    match message_type {
        "APPLIED_DELIVERY_EVIDENCE_RECORDED" => {
            let evidence =
                validate::from_strict_value(&value).map_err(DispatchError::InvalidEvidence)?;
            Ok(DispatchMessage::AppliedDeliveryEvidenceRecorded(Box::new(
                evidence,
            )))
        }

        "COC_PARTICIPANT_MANIFEST" => Ok(
            DispatchMessage::CocParticipantManifestStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "COC_PARTICIPANT_MANIFEST",
                    value,
                },
            ),
        ),
        "COC_RECOVERY_CUTOFF_BATCH" => Ok(
            DispatchMessage::CocRecoveryCutoffBatchStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "COC_RECOVERY_CUTOFF_BATCH",
                    value,
                },
            ),
        ),
        "C_PROVIDER_OUTCOME_RECORDED" => Ok(
            DispatchMessage::CProviderOutcomeRecordedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "C_PROVIDER_OUTCOME_RECORDED",
                    value,
                },
            ),
        ),
        "I_JF10_TERMINAL_DECISION_OBSERVED" => Ok(
            DispatchMessage::IJf10TerminalDecisionObservedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "I_JF10_TERMINAL_DECISION_OBSERVED",
                    value,
                },
            ),
        ),
        "JF10_BRIDGE_RECONCILIATION_RECORDED" => Ok(
            DispatchMessage::Jf10BridgeReconciliationRecordedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "JF10_BRIDGE_RECONCILIATION_RECORDED",
                    value,
                },
            ),
        ),
        "JF10_I_TERMINAL_DECISION_OBSERVED" => Ok(
            DispatchMessage::Jf10ITerminalDecisionObservedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "JF10_I_TERMINAL_DECISION_OBSERVED",
                    value,
                },
            ),
        ),
        "JF10_PREPARED_PARTICIPANT_REGISTERED" => Ok(
            DispatchMessage::Jf10PreparedParticipantRegisteredStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "JF10_PREPARED_PARTICIPANT_REGISTERED",
                    value,
                },
            ),
        ),
        "JF10_PREPARE_INTENT_REGISTERED" => Ok(
            DispatchMessage::Jf10PrepareIntentRegisteredStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "JF10_PREPARE_INTENT_REGISTERED",
                    value,
                },
            ),
        ),
        "JF10_STORAGE_PARTICIPANT_RESOLVED" => Ok(
            DispatchMessage::Jf10StorageParticipantResolvedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "JF10_STORAGE_PARTICIPANT_RESOLVED",
                    value,
                },
            ),
        ),
        "OWNER_ADMISSION_ENTRY" => Ok(DispatchMessage::OwnerAdmissionEntryStructurallyUnvalidated(
            StructurallyUnvalidatedMessage {
                message_type: "OWNER_ADMISSION_ENTRY",
                value,
            },
        )),
        "OWNER_ADMISSION_SNAPSHOT_ATTESTATION" => Ok(
            DispatchMessage::OwnerAdmissionSnapshotAttestationStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "OWNER_ADMISSION_SNAPSHOT_ATTESTATION",
                    value,
                },
            ),
        ),
        "OWNER_GATE_RELEASE_ATTESTATION" => Ok(
            DispatchMessage::OwnerGateReleaseAttestationStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "OWNER_GATE_RELEASE_ATTESTATION",
                    value,
                },
            ),
        ),
        "OWNER_LOCAL_GATE_RELEASE" => Ok(
            DispatchMessage::OwnerLocalGateReleaseStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "OWNER_LOCAL_GATE_RELEASE",
                    value,
                },
            ),
        ),
        "OWNER_LOCAL_PENDING_GATE" => Ok(
            DispatchMessage::OwnerLocalPendingGateStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "OWNER_LOCAL_PENDING_GATE",
                    value,
                },
            ),
        ),
        "PARTICIPANT_SET_RECONCILIATION" => Ok(
            DispatchMessage::ParticipantSetReconciliationStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "PARTICIPANT_SET_RECONCILIATION",
                    value,
                },
            ),
        ),
        "RECOVERY_CUTOFF_BATCH" => Ok(DispatchMessage::RecoveryCutoffBatchStructurallyUnvalidated(
            StructurallyUnvalidatedMessage {
                message_type: "RECOVERY_CUTOFF_BATCH",
                value,
            },
        )),
        "RECOVERY_EPOCH_COMPLETED" => Ok(
            DispatchMessage::RecoveryEpochCompletedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "RECOVERY_EPOCH_COMPLETED",
                    value,
                },
            ),
        ),
        "RECOVERY_JOIN_PROOF" => Ok(DispatchMessage::RecoveryJoinProofStructurallyUnvalidated(
            StructurallyUnvalidatedMessage {
                message_type: "RECOVERY_JOIN_PROOF",
                value,
            },
        )),
        "STORAGE_JF10_PARTICIPANT_RESOLVED" => Ok(
            DispatchMessage::StorageJf10ParticipantResolvedStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "STORAGE_JF10_PARTICIPANT_RESOLVED",
                    value,
                },
            ),
        ),
        "Storage.PreparedParticipantReceipt" => {
            let receipt =
                parse_storage_receipt(raw).map_err(DispatchError::InvalidStorageReceipt)?;

            Ok(DispatchMessage::StoragePreparedParticipantReceipt(
                Box::new(receipt),
            ))
        }
        "Storage.StorageResolutionProof" => Ok(
            DispatchMessage::StorageStorageResolutionProofStructurallyUnvalidated(
                StructurallyUnvalidatedMessage {
                    message_type: "Storage.StorageResolutionProof",
                    value,
                },
            ),
        ),

        other => Err(DispatchError::UnknownMessageType(other.to_owned())),
    }
}

#[cfg(test)]
mod dispatch_tests {
    use super::{parse_dispatch, DispatchError, DispatchMessage, DispatchValidationState};
    use crate::strict_json::StrictJsonError;
    use serde_json::json;

    fn raw_message(message_type: &str) -> Vec<u8> {
        serde_json::to_vec(&json!({
            "message_type": message_type,
            "envelope": {
                "preserved": true
            }
        }))
        .unwrap()
    }

    fn assert_unvalidated(raw: &[u8], expected_type: &str) {
        let message = parse_dispatch(raw).expect("dispatch should succeed");

        assert!(message.is_structurally_unvalidated());
        assert_eq!(
            message.validation_state(),
            DispatchValidationState::RootDiscriminatorOnly
        );
        assert_eq!(message.message_type(), expected_type);

        let preserved_value = match message {
            DispatchMessage::CocParticipantManifestStructurallyUnvalidated(value)
            | DispatchMessage::CocRecoveryCutoffBatchStructurallyUnvalidated(value)
            | DispatchMessage::CProviderOutcomeRecordedStructurallyUnvalidated(value)
            | DispatchMessage::IJf10TerminalDecisionObservedStructurallyUnvalidated(value)
            | DispatchMessage::Jf10BridgeReconciliationRecordedStructurallyUnvalidated(value)
            | DispatchMessage::Jf10ITerminalDecisionObservedStructurallyUnvalidated(value)
            | DispatchMessage::Jf10PreparedParticipantRegisteredStructurallyUnvalidated(value)
            | DispatchMessage::Jf10PrepareIntentRegisteredStructurallyUnvalidated(value)
            | DispatchMessage::Jf10StorageParticipantResolvedStructurallyUnvalidated(value)
            | DispatchMessage::OwnerAdmissionEntryStructurallyUnvalidated(value)
            | DispatchMessage::OwnerAdmissionSnapshotAttestationStructurallyUnvalidated(value)
            | DispatchMessage::OwnerGateReleaseAttestationStructurallyUnvalidated(value)
            | DispatchMessage::OwnerLocalGateReleaseStructurallyUnvalidated(value)
            | DispatchMessage::OwnerLocalPendingGateStructurallyUnvalidated(value)
            | DispatchMessage::ParticipantSetReconciliationStructurallyUnvalidated(value)
            | DispatchMessage::RecoveryCutoffBatchStructurallyUnvalidated(value)
            | DispatchMessage::RecoveryEpochCompletedStructurallyUnvalidated(value)
            | DispatchMessage::RecoveryJoinProofStructurallyUnvalidated(value)
            | DispatchMessage::StorageJf10ParticipantResolvedStructurallyUnvalidated(value)
            | DispatchMessage::StorageStorageResolutionProofStructurallyUnvalidated(value) => {
                value.value
            }
            DispatchMessage::AppliedDeliveryEvidenceRecorded(_)
            | DispatchMessage::StoragePreparedParticipantReceipt(_) => {
                panic!("expected root-discriminator-only message")
            }
        };

        assert_eq!(
            preserved_value["envelope"]["preserved"],
            serde_json::Value::Bool(true)
        );
    }

    #[test]
    fn dispatch_applied_delivery_evidence_uses_existing_validator() {
        let raw = br#"{"message_type":"APPLIED_DELIVERY_EVIDENCE_RECORDED"}"#;

        assert!(matches!(
            parse_dispatch(raw),
            Err(DispatchError::InvalidEvidence(_))
        ));
    }

    #[test]
    fn dispatch_coc_participant_manifest() {
        assert_unvalidated(
            &raw_message("COC_PARTICIPANT_MANIFEST"),
            "COC_PARTICIPANT_MANIFEST",
        );
    }

    #[test]
    fn dispatch_coc_recovery_cutoff_batch() {
        assert_unvalidated(
            &raw_message("COC_RECOVERY_CUTOFF_BATCH"),
            "COC_RECOVERY_CUTOFF_BATCH",
        );
    }

    #[test]
    fn dispatch_c_provider_outcome_recorded() {
        assert_unvalidated(
            &raw_message("C_PROVIDER_OUTCOME_RECORDED"),
            "C_PROVIDER_OUTCOME_RECORDED",
        );
    }

    #[test]
    fn dispatch_i_jf10_terminal_decision_observed() {
        assert_unvalidated(
            &raw_message("I_JF10_TERMINAL_DECISION_OBSERVED"),
            "I_JF10_TERMINAL_DECISION_OBSERVED",
        );
    }

    #[test]
    fn dispatch_jf10_bridge_reconciliation_recorded() {
        assert_unvalidated(
            &raw_message("JF10_BRIDGE_RECONCILIATION_RECORDED"),
            "JF10_BRIDGE_RECONCILIATION_RECORDED",
        );
    }

    #[test]
    fn dispatch_jf10_i_terminal_decision_observed() {
        assert_unvalidated(
            &raw_message("JF10_I_TERMINAL_DECISION_OBSERVED"),
            "JF10_I_TERMINAL_DECISION_OBSERVED",
        );
    }

    #[test]
    fn dispatch_jf10_prepared_participant_registered() {
        assert_unvalidated(
            &raw_message("JF10_PREPARED_PARTICIPANT_REGISTERED"),
            "JF10_PREPARED_PARTICIPANT_REGISTERED",
        );
    }

    #[test]
    fn dispatch_jf10_prepare_intent_registered() {
        assert_unvalidated(
            &raw_message("JF10_PREPARE_INTENT_REGISTERED"),
            "JF10_PREPARE_INTENT_REGISTERED",
        );
    }

    #[test]
    fn dispatch_jf10_storage_participant_resolved() {
        assert_unvalidated(
            &raw_message("JF10_STORAGE_PARTICIPANT_RESOLVED"),
            "JF10_STORAGE_PARTICIPANT_RESOLVED",
        );
    }

    #[test]
    fn dispatch_owner_admission_entry() {
        assert_unvalidated(
            &raw_message("OWNER_ADMISSION_ENTRY"),
            "OWNER_ADMISSION_ENTRY",
        );
    }

    #[test]
    fn dispatch_owner_admission_snapshot_attestation() {
        assert_unvalidated(
            &raw_message("OWNER_ADMISSION_SNAPSHOT_ATTESTATION"),
            "OWNER_ADMISSION_SNAPSHOT_ATTESTATION",
        );
    }

    #[test]
    fn dispatch_owner_gate_release_attestation() {
        assert_unvalidated(
            &raw_message("OWNER_GATE_RELEASE_ATTESTATION"),
            "OWNER_GATE_RELEASE_ATTESTATION",
        );
    }

    #[test]
    fn dispatch_owner_local_gate_release() {
        assert_unvalidated(
            &raw_message("OWNER_LOCAL_GATE_RELEASE"),
            "OWNER_LOCAL_GATE_RELEASE",
        );
    }

    #[test]
    fn dispatch_owner_local_pending_gate() {
        assert_unvalidated(
            &raw_message("OWNER_LOCAL_PENDING_GATE"),
            "OWNER_LOCAL_PENDING_GATE",
        );
    }

    #[test]
    fn dispatch_participant_set_reconciliation() {
        assert_unvalidated(
            &raw_message("PARTICIPANT_SET_RECONCILIATION"),
            "PARTICIPANT_SET_RECONCILIATION",
        );
    }

    #[test]
    fn dispatch_recovery_cutoff_batch() {
        assert_unvalidated(
            &raw_message("RECOVERY_CUTOFF_BATCH"),
            "RECOVERY_CUTOFF_BATCH",
        );
    }

    #[test]
    fn dispatch_recovery_epoch_completed() {
        assert_unvalidated(
            &raw_message("RECOVERY_EPOCH_COMPLETED"),
            "RECOVERY_EPOCH_COMPLETED",
        );
    }

    #[test]
    fn dispatch_recovery_join_proof() {
        assert_unvalidated(&raw_message("RECOVERY_JOIN_PROOF"), "RECOVERY_JOIN_PROOF");
    }

    #[test]
    fn dispatch_storage_jf10_participant_resolved() {
        assert_unvalidated(
            &raw_message("STORAGE_JF10_PARTICIPANT_RESOLVED"),
            "STORAGE_JF10_PARTICIPANT_RESOLVED",
        );
    }

    #[test]
    fn dispatch_storage_prepared_participant_receipt_uses_existing_parser() {
        let value = super::tests::valid_storage_receipt_value();
        let raw = serde_json::to_vec(&value).unwrap();

        let message = parse_dispatch(&raw).expect("valid storage receipt should dispatch");

        assert_eq!(message.message_type(), "Storage.PreparedParticipantReceipt");
        assert_eq!(
            message.validation_state(),
            DispatchValidationState::StructurallyParsed
        );
        assert!(!message.is_structurally_unvalidated());

        assert!(matches!(
            message,
            DispatchMessage::StoragePreparedParticipantReceipt(_)
        ));
    }

    #[test]
    fn dispatch_storage_prepared_participant_receipt_rejects_invalid_structure() {
        let raw = raw_message("Storage.PreparedParticipantReceipt");

        assert!(matches!(
            parse_dispatch(&raw),
            Err(DispatchError::InvalidStorageReceipt(_))
        ));
    }

    #[test]
    fn dispatch_storage_storage_resolution_proof() {
        assert_unvalidated(
            &raw_message("Storage.StorageResolutionProof"),
            "Storage.StorageResolutionProof",
        );
    }

    #[test]
    fn dispatch_rejects_unknown_message_type() {
        let raw = br#"{"message_type":"UNKNOWN_MESSAGE_TYPE"}"#;

        assert_eq!(
            parse_dispatch(raw),
            Err(DispatchError::UnknownMessageType(
                "UNKNOWN_MESSAGE_TYPE".to_owned()
            ))
        );
    }

    #[test]
    fn dispatch_rejects_missing_message_type() {
        let raw = br#"{"other":"value"}"#;

        assert_eq!(parse_dispatch(raw), Err(DispatchError::MissingMessageType));
    }

    #[test]
    fn dispatch_rejects_non_string_message_type() {
        let raw = br#"{"message_type":42}"#;

        assert_eq!(
            parse_dispatch(raw),
            Err(DispatchError::MessageTypeNotString)
        );
    }

    #[test]
    fn dispatch_rejects_non_object_root() {
        let raw = br#"[]"#;

        assert_eq!(parse_dispatch(raw), Err(DispatchError::RootNotObject));
    }

    #[test]
    fn dispatch_preserves_strict_duplicate_key_rejection() {
        let raw = br#"{"message_type":"COC_PARTICIPANT_MANIFEST","nested":{"x":1,"x":2}}"#;

        assert!(matches!(
            parse_dispatch(raw),
            Err(DispatchError::InvalidJson(
                StrictJsonError::DuplicateKey { key, .. }
            )) if key == "x"
        ));
    }

    #[test]
    fn dispatch_applied_delivery_evidence_is_not_structurally_unvalidated() {
        let value = super::tests::valid_value();
        let raw = serde_json::to_vec(&value).unwrap();

        let message = parse_dispatch(&raw).expect("valid evidence should dispatch");

        assert!(matches!(
            &message,
            DispatchMessage::AppliedDeliveryEvidenceRecorded(_)
        ));
        assert!(!message.is_structurally_unvalidated());
        assert_eq!(
            message.validation_state(),
            DispatchValidationState::SemanticallyValidated
        );
        assert_eq!(message.message_type(), "APPLIED_DELIVERY_EVIDENCE_RECORDED");
    }
}

#[cfg(test)]
mod tests {
    use super::digest::{p0_digest, p0_digest_of_value};
    use super::evidence::*;
    use super::parse_and_validate;
    use super::strict_json::{parse_strict, StrictJsonError};
    use super::validate::{from_strict_value, validate_evidence, EvidenceError};
    use serde_json::{json, Value};

    pub(super) fn valid_value() -> Value {
        let mut value = json!({
            "schema_artifact_revision":"1.0.0",
            "message_type":"APPLIED_DELIVERY_EVIDENCE_RECORDED",
            "issuer_ref":"issuer",
            "sender_authority_ref":"authority",
            "sender_subject_ref":"subject",
            "audience":"audience",
            "message_id":"message",
            "message_nonce":"nonce",
            "signing_sequence_namespace_ref":"namespace",
            "signing_record_sequence":"1",
            "signature_profile_id":"profile",
            "key_id_ref":"key",
            "key_version":"1",
            "adapter_instance_ref":"adapter-instance",
            "runtime_session_ref":"runtime-session",
            "delivery_id":"delivery",
            "delivery_attempt_id":"attempt",
            "inference_request_id":"inference",
            "final_request_boundary_id":"boundary",
            "adapter_capability_epoch":"1",
            "evidence_kind":"APPLIED_CONTEXT_OBSERVED",
            "evidence_tier":"TIER_2",
            "adapter_ref":"adapter",
            "runtime_instance_ref":"runtime",
            "context_id":"context",
            "context_version":"v1",
            "materialized_context_version":"v1",
            "final_request_boundary_type":"final",
            "managed_region_id":"region",
            "managed_region_revision":"1",
            "managed_region_inventory_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "managed_region_coverage":"PARTIAL",
            "managed_region_digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "digest_profile":"p0",
            "evidence_issuer_ref":"evidence-issuer",
            "evidence_schema_version":"1.0.0",
            "submission_observed_at":"2026-01-01T12:30:45Z",
            "correlation_ref":"correlation",
            "causation_ref":"causation",
            "audit_ref":"audit",
            "c_submit_outcome_ref":"submit",
            "c_outcome_record_ref":"record",
            "c_outcome_record_sequence":"2",
            "c_outcome_payload_digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
            "payload_digest":"0000000000000000000000000000000000000000000000000000000000000000",
            "signature":"signature",
            "integrity_proof_ref":"proof"
        });
        let digest = p0_digest_of_value(&value).unwrap();
        value["payload_digest"] = Value::String(digest);
        value
    }

    fn valid_evidence() -> AppliedDeliveryEvidence {
        from_strict_value(&valid_value()).unwrap()
    }

    #[test]
    fn strict_rejects_top_level_duplicate_key() {
        assert!(matches!(
            parse_strict(br#"{"a":1,"a":2}"#),
            Err(StrictJsonError::DuplicateKey { path, key })
                if path == "$" && key == "a"
        ));
    }

    #[test]
    fn strict_rejects_nested_duplicate_key() {
        assert!(matches!(
            parse_strict(br#"{"a":{"b":1,"b":2}}"#),
            Err(StrictJsonError::DuplicateKey { path, key })
                if path == "$.a" && key == "b"
        ));
    }

    #[test]
    fn strict_rejects_duplicate_in_array_object() {
        assert!(matches!(
            parse_strict(br#"{"a":[{"x":1,"x":2}]}"#),
            Err(StrictJsonError::DuplicateKey { path, key })
                if path == "$.a[0]" && key == "x"
        ));
    }

    #[test]
    fn strict_rejects_three_level_duplicate() {
        assert!(matches!(
            parse_strict(br#"{"a":{"b":[{"c":1,"c":2}]}}"#),
            Err(StrictJsonError::DuplicateKey { path, key })
                if path == "$.a.b[0]" && key == "c"
        ));
    }

    #[test]
    fn strict_rejects_trailing_content() {
        assert_eq!(
            parse_strict(br#"{"a":1} false"#),
            Err(StrictJsonError::TrailingCharacters)
        );
    }

    #[test]
    fn strict_rejects_unclosed_object() {
        assert_eq!(
            parse_strict(br#"{"a":1"#),
            Err(StrictJsonError::UnexpectedEof)
        );
    }

    #[test]
    fn strict_rejects_invalid_escape() {
        assert_eq!(
            parse_strict(br#"{"a":"\q"}"#),
            Err(StrictJsonError::InvalidEscape)
        );
    }

    #[test]
    fn strict_rejects_invalid_number() {
        assert_eq!(
            parse_strict(br#"{"a":01}"#),
            Err(StrictJsonError::InvalidNumber)
        );
    }

    #[test]
    fn strict_rejects_invalid_literal() {
        assert_eq!(parse_strict(b"tru"), Err(StrictJsonError::UnexpectedEof));
    }

    #[test]
    fn strict_rejects_depth_over_128() {
        let input = format!("{}0{}", "[".repeat(130), "]".repeat(130));
        assert_eq!(
            parse_strict(input.as_bytes()),
            Err(StrictJsonError::DepthExceeded)
        );
    }

    #[test]
    fn public_raw_entrypoint_rejects_duplicate_members() {
        let raw =
            br#"{"message_type":"APPLIED_DELIVERY_EVIDENCE_RECORDED","message_type":"ATTACKER"}"#;
        assert!(matches!(
            parse_and_validate(raw),
            Err(EvidenceError::InvalidJson(StrictJsonError::DuplicateKey { key, .. }))
                if key == "message_type"
        ));
    }

    #[test]
    fn public_raw_entrypoint_returns_only_validated_evidence() {
        let raw = serde_json::to_vec(&valid_value()).unwrap();
        let evidence = parse_and_validate(&raw).unwrap();
        assert_eq!(evidence.message_type, "APPLIED_DELIVERY_EVIDENCE_RECORDED");
    }

    #[test]
    fn strict_rejects_empty_input() {
        assert_eq!(parse_strict(b""), Err(StrictJsonError::UnexpectedEof));
    }

    #[test]
    fn strict_accepts_surrogate_pair() {
        assert_eq!(
            parse_strict(br#""\uD83D\uDE00""#),
            Ok(Value::String("😀".to_owned()))
        );
    }

    #[test]
    fn strict_accepts_nested_arrays() {
        assert_eq!(parse_strict(br#"[1,[2,[3]]]"#), Ok(json!([1, [2, [3]]])));
    }

    #[test]
    fn strict_accepts_null() {
        assert_eq!(parse_strict(b"null"), Ok(Value::Null));
    }

    #[test]
    fn strict_rejects_invalid_utf8() {
        assert_eq!(
            parse_strict(&[b'"', 0xff, b'"']),
            Err(StrictJsonError::InvalidUtf8)
        );
    }

    #[test]
    fn semantic_rejects_missing_required_field() {
        let mut value = valid_value();
        value.as_object_mut().unwrap().remove("issuer_ref");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::MissingField("issuer_ref"))
        );
    }

    #[test]
    fn semantic_rejects_missing_decimal_field() {
        let mut value = valid_value();
        value
            .as_object_mut()
            .unwrap()
            .remove("signing_record_sequence");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::MissingField("signing_record_sequence"))
        );
    }

    #[test]
    fn semantic_rejects_missing_hex_field() {
        let mut value = valid_value();
        value
            .as_object_mut()
            .unwrap()
            .remove("managed_region_digest");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::MissingField("managed_region_digest"))
        );
    }

    #[test]
    fn semantic_rejects_missing_datetime_field() {
        let mut value = valid_value();
        value
            .as_object_mut()
            .unwrap()
            .remove("submission_observed_at");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::MissingField("submission_observed_at"))
        );
    }

    #[test]
    fn semantic_rejects_unknown_field() {
        let mut value = valid_value();
        value["extra"] = json!("no");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::UnknownField("extra".into()))
        );
    }

    #[test]
    fn semantic_rejects_wrong_const() {
        let mut value = valid_value();
        value["message_type"] = json!("OTHER");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::WrongConst {
                field: "message_type",
                ..
            })
        ));
    }

    /// 后门回归测试：结构体不得带 `deny_unknown_fields` 之外的宽松入口。
    ///
    /// `AppliedDeliveryEvidence` 刻意不派生 `Deserialize`。这里验证的是它的
    /// **唯一**构造入口 `from_strict_value` 对多余字段零容忍——即使多余字段
    /// 的值完全合法、类型正确，也必须拒绝，而不是像 `#[serde(default)]`
    /// 那样静默忽略。
    #[test]
    fn evidence_construction_rejects_unknown_field_with_valid_value() {
        let mut value = valid_value();
        value["unknown_but_well_typed_field"] = json!("perfectly-valid-string");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::UnknownField(name)) if name == "unknown_but_well_typed_field"
        ));
    }

    /// 反序列化入口不存在：只有 `from_strict_value` 能产出该类型。
    ///
    /// 用 `Serialize` 往返证明序列化是可用的，同时证明往返**必须**经过
    /// `from_strict_value` 才能拿回值——不存在 `Deserialize` 捷径。
    #[test]
    fn applied_delivery_evidence_accessors_return_the_validated_values() {
        let evidence = valid_evidence();

        assert_eq!(evidence.schema_artifact_revision(), "1.0.0");
        assert_eq!(
            evidence.message_type(),
            "APPLIED_DELIVERY_EVIDENCE_RECORDED"
        );
        assert_eq!(evidence.issuer_ref(), "issuer");
        assert_eq!(evidence.sender_authority_ref(), "authority");
        assert_eq!(evidence.sender_subject_ref(), "subject");
        assert_eq!(evidence.audience(), "audience");
        assert_eq!(evidence.message_id(), "message");
        assert_eq!(evidence.message_nonce(), "nonce");
    }

    #[test]
    fn applied_delivery_evidence_optional_sequence_is_none_when_absent() {
        let mut value = valid_value();
        value
            .as_object_mut()
            .unwrap()
            .remove("submission_monotonic_sequence");

        let evidence = from_strict_value(&value).unwrap();
        assert_eq!(evidence.submission_monotonic_sequence(), None);
    }

    #[test]
    fn evidence_round_trip_must_go_through_strict_validation() {
        let evidence = valid_evidence();
        let value = serde_json::to_value(&evidence).expect("serialize");
        // 直接反序列化不存在（编译期保证），只能走严格入口。
        let again = from_strict_value(&value).expect("strict round trip");
        assert_eq!(again, evidence);
    }

    #[test]
    fn semantic_rejects_invalid_enum() {
        let mut value = valid_value();
        value["evidence_tier"] = json!("TIER_4");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::InvalidEnum {
                field: "evidence_tier",
                ..
            })
        ));
    }

    #[test]
    fn semantic_rejects_decimal_leading_zero() {
        let mut value = valid_value();
        value["signing_record_sequence"] = json!("01");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::InvalidDecimal {
                field: "signing_record_sequence",
                ..
            })
        ));
    }

    #[test]
    fn semantic_rejects_hex_wrong_length() {
        let mut value = valid_value();
        value["managed_region_digest"] = json!("abc");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::InvalidHex64 {
                field: "managed_region_digest",
                ..
            })
        ));
    }

    #[test]
    fn semantic_rejects_uppercase_hex() {
        let mut value = valid_value();
        value["managed_region_digest"] = json!("A".repeat(64));
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::InvalidHex64 {
                field: "managed_region_digest",
                ..
            })
        ));
    }

    #[test]
    fn semantic_rejects_invalid_datetime_structure() {
        let mut value = valid_value();
        value["submission_observed_at"] = json!("2026-99-99 12:30:45Z");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::InvalidDateTime { .. })
        ));
    }

    #[test]
    fn semantic_rejects_nonexistent_calendar_date() {
        let mut value = valid_value();
        value["submission_observed_at"] = json!("2024-02-30T00:00:00Z");
        let digest = p0_digest_of_value(&value).unwrap();
        value["payload_digest"] = json!(digest);
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::InvalidDateTime { .. })
        ));
    }

    #[test]
    fn semantic_accepts_rfc3339_lowercase_and_leap_second_forms() {
        for observed_at in ["2024-01-01t00:00:00z", "2016-12-31T23:59:60Z"] {
            let mut value = valid_value();
            value["submission_observed_at"] = json!(observed_at);
            let digest = p0_digest_of_value(&value).unwrap();
            value["payload_digest"] = json!(digest);
            assert!(from_strict_value(&value).is_ok(), "{observed_at}");
        }
    }

    #[test]
    fn semantic_rejects_tier1_partial_coverage() {
        let mut value = valid_value();
        value["evidence_tier"] = json!("TIER_1");
        value["managed_region_coverage"] = json!("PARTIAL");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::Tier1RequiresCompleteCoverage)
        );
    }

    #[test]
    fn semantic_rejects_final_request_without_monotonic_sequence() {
        let mut value = valid_value();
        value["evidence_kind"] = json!("FINAL_REQUEST_SUBMITTED");
        assert_eq!(
            from_strict_value(&value),
            Err(EvidenceError::FinalRequestRequiresMonotonicSequence)
        );
    }

    #[test]
    fn semantic_rejects_tier1_materialized_version_mismatch() {
        let mut value = valid_value();
        value["evidence_tier"] = json!("TIER_1");
        value["managed_region_coverage"] = json!("COMPLETE");
        value["materialized_context_version"] = json!("v2");
        assert!(matches!(
            from_strict_value(&value),
            Err(EvidenceError::Tier1RequiresMaterializedVersionMatch { .. })
        ));
    }

    #[test]
    fn semantic_accepts_valid_evidence() {
        assert!(from_strict_value(&valid_value()).is_ok());
    }

    #[test]
    fn semantic_rejects_payload_digest_mismatch() {
        let mut evidence = valid_evidence();
        evidence.payload_digest = "d".repeat(64);
        assert!(matches!(
            validate_evidence(&evidence),
            Err(EvidenceError::PayloadDigestMismatch { .. })
        ));
    }

    #[test]
    fn digest_is_deterministic() {
        let evidence = valid_evidence();
        assert_eq!(p0_digest(&evidence), p0_digest(&evidence));
    }

    #[test]
    fn digest_ignores_payload_digest() {
        let mut evidence = valid_evidence();
        let before = p0_digest(&evidence).unwrap();
        evidence.payload_digest = "d".repeat(64);
        assert_eq!(before, p0_digest(&evidence).unwrap());
    }

    #[test]
    fn digest_changes_when_an_included_field_changes() {
        let mut evidence = valid_evidence();
        let before = p0_digest(&evidence).unwrap();
        evidence.audience.push_str("-changed");
        assert_ne!(before, p0_digest(&evidence).unwrap());
    }

    #[test]
    fn digest_excludes_signature_and_integrity_proof() {
        let value = valid_value();
        let digest = p0_digest_of_value(&value).unwrap();
        let mut without_excluded = value.clone();
        without_excluded
            .as_object_mut()
            .unwrap()
            .remove("signature");
        without_excluded
            .as_object_mut()
            .unwrap()
            .remove("integrity_proof_ref");
        assert_eq!(digest, p0_digest_of_value(&without_excluded).unwrap());
    }

    #[test]
    fn digest_accepts_optional_sequence_when_present() {
        let mut value = valid_value();
        value["submission_monotonic_sequence"] = json!("0");
        value["evidence_kind"] = json!("FINAL_REQUEST_SUBMITTED");
        let digest = p0_digest_of_value(&value).unwrap();
        value["payload_digest"] = json!(digest);
        assert!(from_strict_value(&value).is_ok());
    }

    pub(super) fn valid_storage_receipt_value() -> Value {
        json!({
            "schema_id": "bmcp.storage-prepared-participant-proof",
            "schema_version": "1.0.0",
            "message_type": "Storage.PreparedParticipantReceipt",
            "message_id": "message-1",
            "message_nonce": "nonce-1",
            "signature_envelope": {
                "payload_type": "Storage.PreparedParticipantReceipt",
                "schema_version": "1.0.0",
                "issuer_principal_ref": "issuer",
                "subject_ref": "subject",
                "owner_authority_ref": "authority",
                "audience_ref": "audience",
                "target_environment_ref": "environment",
                "purpose": "prepared-receipt",
                "key_id": "key",
                "key_version": "1",
                "algorithm_profile_ref": "algorithm",
                "canonicalization_profile_ref": "canonicalization",
                "digest_profile_ref": "digest-profile",
                "issued_at": "2026-11-21T12:00:00Z",
                "trust_status_evidence_ref": "trust-evidence",
                "payload_digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "signature": "AbCd_123-"
            },
            "payload": {
                "prepared_participant_ref": "participant",
                "prepared_transaction_gid": "GID_123",
                "postgresql_native_xid": 0,
                "canonical_authority_db_ref": "authority-db",
                "database_incarnation_ref": "incarnation",
                "postgresql_system_identifier": "0123456789",
                "postgresql_database_oid": "00042",
                "original_prepare_timeline": 1,
                "original_prepare_lsn": "A/BC",
                "publication_operation_id": "operation",
                "request_digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "participant_tuple_digest": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                "owner_boundary_ref": "boundary",
                "causal_order_domain_ref": "causal-domain",
                "policy_domain_ref": "policy-domain",
                "coc_prepare_intent_position": "position",
                "coc_prepare_intent_digest": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
                "prepare_attempt_ref": "attempt",
                "prepare_attempt_generation": 1,
                "participant_ledger_ref": "ledger",
                "participant_ledger_version": 1,
                "prepared_state": "PREPARED",
                "prepared_observation_source": "AUTHORITATIVE_WRITABLE_PRIMARY_READBACK",
                "prepared_observed_at": "2026-11-21T12:00:00Z"
            }
        })
    }

    #[test]
    fn storage_receipt_accepts_leading_zero_system_identifier() {
        let value = valid_storage_receipt_value();
        assert_eq!(
            value["payload"]["postgresql_system_identifier"],
            "0123456789"
        );
        assert!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()).is_ok()
        );
    }

    #[test]
    fn storage_receipt_accepts_native_xid_zero() {
        let value = valid_storage_receipt_value();
        assert_eq!(value["payload"]["postgresql_native_xid"], 0);
        assert!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()).is_ok()
        );
    }

    #[test]
    fn storage_receipt_rejects_native_xid_above_u32() {
        let mut value = valid_storage_receipt_value();
        value["payload"]["postgresql_native_xid"] = json!(4294967296u64);

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::OutOfRange {
                field: "postgresql_native_xid",
                ..
            })
        ));
    }

    #[test]
    fn storage_receipt_rejects_zero_prepare_attempt_generation() {
        let mut value = valid_storage_receipt_value();
        value["payload"]["prepare_attempt_generation"] = json!(0);

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::OutOfRange {
                field: "prepare_attempt_generation",
                ..
            })
        ));
    }

    #[test]
    fn storage_receipt_rejects_lowercase_lsn() {
        let mut value = valid_storage_receipt_value();
        value["payload"]["original_prepare_lsn"] = json!("a/BC");

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::InvalidLsn {
                field: "original_prepare_lsn",
                ..
            })
        ));
    }

    #[test]
    fn storage_receipt_rejects_wrong_message_type_const() {
        let mut value = valid_storage_receipt_value();
        value["message_type"] = json!("Storage.OtherMessage");

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::WrongConst {
                field: "message_type",
                ..
            })
        ));
    }

    #[test]
    fn storage_receipt_rejects_unknown_root_field() {
        let mut value = valid_storage_receipt_value();
        value["unexpected"] = json!("value");

        assert!(matches!(
            super::parse_storage_receipt(
                serde_json::to_string(&value).unwrap().as_bytes()
            ),
            Err(EvidenceError::UnknownField(field))
                if field == "unexpected"
        ));
    }

    #[test]
    fn storage_receipt_rejects_missing_required_field() {
        let mut value = valid_storage_receipt_value();
        value["payload"]
            .as_object_mut()
            .unwrap()
            .remove("prepared_participant_ref");

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::MissingField("prepared_participant_ref"))
        ));
    }

    #[test]
    fn storage_receipt_rejects_payload_type_mismatch() {
        let mut value = valid_storage_receipt_value();
        value["signature_envelope"]["payload_type"] = json!("Storage.StorageResolutionProof");

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::WrongConst {
                field: "signature_envelope.payload_type",
                ..
            })
        ));
    }

    #[test]
    fn storage_receipt_rejects_non_hex_digest() {
        let mut value = valid_storage_receipt_value();
        value["payload"]["request_digest"] =
            json!("gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg");

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::InvalidHex64 {
                field: "request_digest",
                ..
            })
        ));
    }

    #[test]
    fn storage_receipt_rejects_unknown_nested_fields() {
        let mut value = valid_storage_receipt_value();
        value["payload"]["unexpected"] = json!("value");

        assert!(matches!(
            super::parse_storage_receipt(
                serde_json::to_string(&value).unwrap().as_bytes()
            ),
            Err(EvidenceError::UnknownField(field))
                if field == "unexpected"
        ));
    }

    #[test]
    fn storage_receipt_rejects_non_integer_xid() {
        let mut value = valid_storage_receipt_value();
        value["payload"]["postgresql_native_xid"] = json!(1.5);

        assert!(matches!(
            super::parse_storage_receipt(serde_json::to_string(&value).unwrap().as_bytes()),
            Err(EvidenceError::InvalidInteger {
                field: "postgresql_native_xid",
                ..
            })
        ));
    }
}
