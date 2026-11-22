use bmcp_server::{handle_request_body, RequestOutcome};
use serde_json::Value;

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

fn response_json(body: &str) -> Value {
    serde_json::from_str(body)
        .unwrap_or_else(|error| panic!("response is not valid JSON ({error}): {body}"))
}

fn tool_result_json(body: &str) -> Value {
    let response = response_json(body);

    assert!(
        response.get("error").is_none(),
        "expected a tool result, got a JSON-RPC error: {response}"
    );

    assert_eq!(
        response["result"]["content"][0]["type"], "text",
        "tool result must contain a text content block: {response}"
    );

    assert!(
        response["result"]["isError"].is_boolean(),
        "result.isError must be a JSON boolean: {response}"
    );

    response
}

fn tool_payload(response: &Value) -> Value {
    let text = response["result"]["content"][0]["text"]
        .as_str()
        .expect("content[0].text must be a string");

    serde_json::from_str(text)
        .unwrap_or_else(|error| panic!("tool text is not valid inner JSON ({error}): {text:?}"))
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
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(response["result"]["isError"], false);
    assert_eq!(payload["valid"], true);

    let digest = payload["digest"]
        .as_str()
        .expect("valid validate payload must contain a string digest");

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
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(
        response["result"]["isError"], false,
        "ordinary validate failure must not be a tool execution error: {response}"
    );
    assert_eq!(payload["valid"], false);
    assert!(
        payload["error"]
            .as_str()
            .is_some_and(|error| error.contains("DuplicateKey")),
        "duplicate-key validation result must describe DuplicateKey: {payload}"
    );
}

#[test]
fn validate_tool_rejects_missing_field() {
    let missing = VALID_EVIDENCE.replace(r#""audience":"audience","#, "");

    let body = responded(&tool_call(
        4,
        "validate_applied_delivery_evidence",
        &missing,
    ));
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(
        response["result"]["isError"], false,
        "ordinary validate failure must not be a tool execution error: {response}"
    );
    assert_eq!(payload["valid"], false);
    assert!(
        payload["error"]
            .as_str()
            .is_some_and(|error| !error.is_empty()),
        "missing-field validation result must contain an error description: {payload}"
    );
}

#[test]
fn digest_tool_returns_hex64() {
    let body = responded(&tool_call(
        5,
        "digest_applied_delivery_evidence",
        VALID_EVIDENCE,
    ));
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(response["result"]["isError"], false);

    let digest = payload["digest"]
        .as_str()
        .expect("valid digest payload must contain a string digest");

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
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(
        response["result"]["isError"], true,
        "invalid digest evidence must be a tool execution error: {response}"
    );
    assert_eq!(payload["valid"], false);
    assert!(
        payload["error"]
            .as_str()
            .is_some_and(|error| !error.is_empty()),
        "invalid digest payload must contain an error description: {payload}"
    );
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
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(response["result"]["isError"], false);
    assert_eq!(payload["valid"], true);

    let digest = payload["digest"]
        .as_str()
        .expect("text payload must contain a string digest");

    assert!(
        is_hex64(digest),
        "text payload digest is not a 64-character hex string: {payload}"
    );
}

#[test]
fn invalid_evidence_yields_tool_error_not_protocol_error() {
    let body = responded(&tool_call(
        10,
        "digest_applied_delivery_evidence",
        r#"{"schema_artifact_revision":"1.0.0"}"#,
    ));
    let response = tool_result_json(&body);
    let payload = tool_payload(&response);

    assert_eq!(response["result"]["isError"], true);
    assert_eq!(payload["valid"], false);
    assert!(
        payload["error"]
            .as_str()
            .is_some_and(|error| !error.is_empty()),
        "tool error payload must contain a non-empty error description: {payload}"
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

#[test]
fn structural_protocol_error_cases_remain_json_rpc_errors() {
    let malformed_requests = [
        r#"{"jsonrpc":"2.0","id":21,"method":"tools/call"}"#,
        r#"{"jsonrpc":"2.0","id":22,"method":"tools/call","params":{}}"#,
        r#"{"jsonrpc":"2.0","id":23,"method":"tools/call","params":{"name":"digest_applied_delivery_evidence","arguments":{}}}"#,
        r#"{"jsonrpc":"2.0","id":24,"method":"tools/call","params":{"name":7,"arguments":{"evidence":{}}}}"#,
    ];

    for request in malformed_requests {
        let response = response_json(&responded(request));

        assert_eq!(response["error"]["code"], -32602);
        assert!(response.get("result").is_none());
    }

    let unknown_tool = response_json(&responded(&tool_call(25, "no_such_tool", VALID_EVIDENCE)));
    assert_eq!(unknown_tool["error"]["code"], -32602);
    assert!(unknown_tool.get("result").is_none());

    let unknown_method = response_json(&responded(
        r#"{"jsonrpc":"2.0","id":26,"method":"no/such/method"}"#,
    ));
    assert_eq!(unknown_method["error"]["code"], -32601);
    assert!(unknown_method.get("result").is_none());
}
