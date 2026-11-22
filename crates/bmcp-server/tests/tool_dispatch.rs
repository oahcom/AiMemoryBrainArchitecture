use bmcp_server::{handle_request_body, RequestOutcome};

/// A semantically valid `AppliedDeliveryEvidence` record, taken from
/// `bmcp-protocol`'s `valid_value()` fixture with `payload_digest` filled in.
const VALID_EVIDENCE: &str = concat!(
    r#"{"schema_artifact_revision":"1.0.0","#,
    r#""message_type":"APPLIED_DELIVERY_EVIDENCE_RECORDED","#,
    r#""issuer_ref":"issuer","sender_authority_ref":"authority","#,
    r#""sender_subject_ref":"subject","audience":"audience","#,
    r#""message_id":"message","message_nonce":"nonce","#,
    r#""signing_sequence_namespace_ref":"namespace","signing_record_sequence":"1","#,
    r#""signature_profile_id":"profile","key_id_ref":"key","key_version":"1","#,
    r#""adapter_instance_ref":"adapter-instance","runtime_session_ref":"runtime-session","#,
    r#""delivery_id":"delivery","delivery_attempt_id":"attempt","#,
    r#""inference_request_id":"inference","final_request_boundary_id":"boundary","#,
    r#""adapter_capability_epoch":"1","evidence_kind":"APPLIED_CONTEXT_OBSERVED","#,
    r#""evidence_tier":"TIER_2","adapter_ref":"adapter","runtime_instance_ref":"runtime","#,
    r#""context_id":"context","context_version":"v1","materialized_context_version":"v1","#,
    r#""final_request_boundary_type":"final","managed_region_id":"region","#,
    r#""managed_region_revision":"1","#,
    r#""managed_region_inventory_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","#,
    r#""managed_region_coverage":"PARTIAL","#,
    r#""managed_region_digest":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","#,
    r#""digest_profile":"p0","evidence_issuer_ref":"evidence-issuer","#,
    r#""evidence_schema_version":"1.0.0","submission_observed_at":"2026-01-01T12:30:45Z","#,
    r#""correlation_ref":"correlation","causation_ref":"causation","audit_ref":"audit","#,
    r#""c_submit_outcome_ref":"submit","c_outcome_record_ref":"record","#,
    r#""c_outcome_record_sequence":"2","#,
    r#""c_outcome_payload_digest":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","#,
    r#""payload_digest":"1554fe033d057e297281fee1f748b70cd20d2e2bdee7e92d52621bfe7d79a478","#,
    r#""signature":"signature","integrity_proof_ref":"proof"}"#
);

fn is_hex64(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}

fn responded(body: &str) -> String {
    match handle_request_body(body.as_bytes()) {
        RequestOutcome::Responded { body } => body,
        other => panic!("expected Responded, got: {other:?}"),
    }
}

fn tool_call(id: u64, tool: &str, evidence: &str) -> String {
    format!(
        r#"{{"jsonrpc":"2.0","id":{id},"method":"tools/call","params":{{"name":"{tool}","arguments":{{"evidence":{evidence}}}}}}}"#
    )
}

#[test]
fn tools_list_exposes_validate_and_digest() {
    let body = responded(r#"{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}"#);

    assert!(body.contains("\"name\":\"validate_applied_delivery_evidence\""));
    assert!(body.contains("\"name\":\"digest_applied_delivery_evidence\""));
    assert!(body.contains("\"inputSchema\":{\"type\":\"object\",\"properties\":{\"evidence\":{\"type\":\"object\"}},\"required\":[\"evidence\"]}"));
    assert_eq!(
        body.matches("\"name\":\"").count(),
        2,
        "tools/list should describe exactly two tools: {body}"
    );
}

#[test]
fn validate_tool_accepts_valid_evidence() {
    let body = responded(&tool_call(
        2,
        "validate_applied_delivery_evidence",
        VALID_EVIDENCE,
    ));

    assert!(
        body.contains(r#"\"valid\":true"#),
        "successful validate payload must be present in the escaped text block: {body}"
    );

    let digest = body
        .split(r#"\"digest\":\""#)
        .nth(1)
        .and_then(|rest| rest.split(r#"\""#).next())
        .unwrap_or_else(|| panic!("no digest in response: {body}"));

    assert!(is_hex64(digest), "digest is not 64 hex chars: {digest}");
}

#[test]
fn validate_tool_rejects_duplicate_key() {
    let duplicated = VALID_EVIDENCE.replace(
        r#""issuer_ref":"issuer""#,
        r#""issuer_ref":"issuer","issuer_ref":"issuer""#,
    );
    assert_ne!(duplicated, VALID_EVIDENCE, "fixture edit did not apply");

    let body = responded(&tool_call(
        3,
        "validate_applied_delivery_evidence",
        &duplicated,
    ));

    assert!(
        body.contains("\"isError\":true"),
        "invalid evidence must be a tool error: {body}"
    );
    assert!(body.contains("DuplicateKey"), "unexpected error: {body}");
}

#[test]
fn validate_tool_rejects_missing_field() {
    let missing = VALID_EVIDENCE.replace(r#""audience":"audience","#, "");

    let body = responded(&tool_call(
        4,
        "validate_applied_delivery_evidence",
        &missing,
    ));

    assert!(
        body.contains("\"isError\":true"),
        "invalid evidence must be a tool error: {body}"
    );
}

#[test]
fn digest_tool_returns_hex64() {
    let body = responded(&tool_call(
        5,
        "digest_applied_delivery_evidence",
        VALID_EVIDENCE,
    ));

    let digest = body
        .split(r#"\"digest\":\""#)
        .nth(1)
        .and_then(|rest| rest.split(r#"\""#).next())
        .unwrap_or_else(|| panic!("no digest in response: {body}"));

    assert!(is_hex64(digest), "digest is not 64 hex chars: {digest}");
    assert_eq!(
        digest, "1554fe033d057e297281fee1f748b70cd20d2e2bdee7e92d52621bfe7d79a478",
        "digest must be the p0 digest of the fixture"
    );
}

#[test]
fn digest_tool_rejects_invalid_evidence() {
    let body = responded(&tool_call(
        6,
        "digest_applied_delivery_evidence",
        r#"{"schema_artifact_revision":"1.0.0"}"#,
    ));

    assert!(
        body.contains("\"isError\":true"),
        "invalid evidence is a tool error, not a protocol error: {body}"
    );
    assert!(
        !body.contains("\"code\":-32602"),
        "tool business failure must not be -32602: {body}"
    );
    assert!(body.contains("\"id\":6"), "unexpected body: {body}");
}

#[test]
fn unknown_tool_is_invalid_params() {
    let body = responded(&tool_call(7, "no_such_tool", VALID_EVIDENCE));

    assert!(body.contains("\"code\":-32602"), "unexpected body: {body}");
    assert!(body.contains("unknown tool"), "unexpected body: {body}");
    assert!(body.contains("\"id\":7"), "unexpected body: {body}");
}

#[test]
fn initialize_advertises_tools_capability() {
    let body = responded(r#"{"jsonrpc":"2.0","id":8,"method":"initialize","params":{}}"#);

    assert!(
        body.contains("\"capabilities\":{\"tools\":{\"listChanged\":false}}"),
        "tools capability must not be an empty object: {body}"
    );
}

#[test]
fn call_tool_result_has_text_content_block() {
    let body = responded(&tool_call(
        9,
        "validate_applied_delivery_evidence",
        VALID_EVIDENCE,
    ));

    assert!(
        body.contains(r#""content":[{"type":"text","text":"{\"valid\":true,\"digest\":\""#),
        "missing MCP text content block or expected payload: {body}"
    );
    assert!(
        body.contains(r#""isError":false"#),
        "successful tool result must have isError=false: {body}"
    );

    let digest = body
        .split(r#""text":"{\"valid\":true,\"digest\":\""#)
        .nth(1)
        .and_then(|rest| rest.split(r#"\"}"#).next())
        .unwrap_or_else(|| panic!("could not extract JSON payload from text content: {body}"));

    assert!(
        is_hex64(digest),
        "text payload digest is not a 64-character hex string: {body}"
    );
    assert!(
        body.contains(r#"\"}"#),
        "text content does not terminate as the expected JSON object string: {body}"
    );
}

#[test]
fn invalid_evidence_yields_tool_error_not_protocol_error() {
    let body = responded(&tool_call(
        10,
        "digest_applied_delivery_evidence",
        r#"{"schema_artifact_revision":"1.0.0"}"#,
    ));

    assert!(
        !body.contains(r#","error":{"code""#),
        "business failure must not be returned as a JSON-RPC protocol error: {body}"
    );
    assert!(
        body.contains(r#""isError":true"#),
        "invalid evidence must set result.isError=true: {body}"
    );
    assert!(
        body.contains(r#""content":[{"type":"text","text":""#),
        "business failure must include a text content block: {body}"
    );

    let text = body
        .split(r#""text":""#)
        .nth(1)
        .and_then(|rest| rest.split(r#""}],"isError""#).next())
        .unwrap_or_else(|| panic!("could not extract tool error text: {body}"));

    assert!(
        !text.is_empty(),
        "tool error text must not be empty: {body}"
    );
}

#[test]
fn malformed_call_params_remain_protocol_errors() {
    let requests = [
        r#"{"jsonrpc":"2.0","id":11,"method":"tools/call"}"#,
        r#"{"jsonrpc":"2.0","id":12,"method":"tools/call","params":{}}"#,
        r#"{"jsonrpc":"2.0","id":13,"method":"tools/call","params":{"name":"digest_applied_delivery_evidence","arguments":{}}}"#,
    ];

    for request in requests {
        let body = responded(request);

        assert!(
            body.contains(r#""code":-32602"#),
            "malformed tools/call params must return -32602: {body}"
        );
        assert!(
            !body.contains(r#""result""#),
            "protocol error must not contain a result field: {body}"
        );
    }
}

#[test]
fn unknown_tool_name_remains_protocol_error() {
    let body = responded(&tool_call(14, "no_such_tool", VALID_EVIDENCE));

    assert!(
        body.contains(r#""code":-32602"#),
        "unknown tool name must return -32602: {body}"
    );
    assert!(
        !body.contains(r#""result""#),
        "unknown tool protocol error must not contain a result field: {body}"
    );
}
