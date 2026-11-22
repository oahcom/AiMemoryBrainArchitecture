//! Cross-language parity: the server's `tools/call` verdicts must agree with the
//! Python reference validator in `08-bmcp-protocol/validators/` on the same bytes.
//!
//! Both sides receive the fixture file verbatim. Rust sees it through
//! `handle_request_body`; Python sees it through
//! `validate_applied_delivery_evidence`, with every owner-authority callback
//! stubbed to `True` and a C record that satisfies the H/C join. What is being
//! compared is therefore envelope-level semantics plus the p0 digest, not the
//! injected trust decisions (Rust does not implement those at all).
//!
//! The Python run is skipped when `python3` or `jsonschema` is unavailable, so a
//! machine without the reference toolchain never turns this red.

use std::path::Path;
use std::process::Command;

use bmcp_server::{handle_request_body, RequestOutcome};
use serde_json::Value;

const VALIDATE_TOOL: &str = "validate_applied_delivery_evidence";
const DIGEST_TOOL: &str = "digest_applied_delivery_evidence";

/// The digest of `valid.json`, pinned so a silent change to either
/// canonicalization shows up as a fixture mismatch rather than a green run.
const VALID_DIGEST: &str = "ba322195c7852a553fec298ab249b0ede8afd129eb21ff8fb6fa1c591287aa39";

const PYTHON_SCRIPT: &str = r#"
import json, sys
root, fixture = sys.argv[1], sys.argv[2]
sys.path.insert(0, root + "/08-bmcp-protocol/validators")
import applied_delivery_evidence_validator as v

raw = open(fixture, "rb").read()
# One immutable C record that satisfies the H/C join for the fixture's
# c_submit_outcome_ref / c_outcome_* fields.
record = {
    "issuer_authority_ref": "authority",
    "sequence_namespace_ref": "namespace",
    "record_ref": "record",
    "record_sequence": "2",
    "payload_digest": "c" * 64,
    "FinalRequestBoundaryRef": "boundary",
}
checks = v.AppliedDeliveryChecks(
    verify_profile_registration=lambda envelope: True,
    verify_key_status=lambda envelope: True,
    verify_signature=lambda envelope, p0: True,
    verify_protected_identity_binding=lambda envelope: True,
    verify_c_final_boundary=lambda envelope: True,
    verify_g_delivery_binding=lambda envelope: True,
    verify_capability_epoch=lambda envelope: True,
    commit_observation=lambda envelope, digest: v.DurableObservationDecision("NEW"),
    verify_current_i_replay_authorization=lambda envelope, ref: True,
    verify_current_d_forget_fence=lambda envelope, ref: True,
    resolve_c_submit_outcome=lambda ref: record,
    verify_c_submit_outcome_record=lambda resolved: True,
)
result = v.validate_applied_delivery_evidence(raw, v.SCHEMA, checks)
status = result["status"]
print(json.dumps({
    "valid": status.startswith("VALID"),
    "status": status,
    "digest": result.get("h_p0_digest"),
}, separators=(",", ":")))
"#;

fn fixture_path(name: &str) -> String {
    format!("{}/tests/fixtures/{name}", env!("CARGO_MANIFEST_DIR"))
}

fn repo_root() -> &'static str {
    concat!(env!("CARGO_MANIFEST_DIR"), "/../..")
}

fn read_fixture(name: &str) -> String {
    let path = fixture_path(name);
    std::fs::read_to_string(&path).unwrap_or_else(|error| panic!("cannot read {path}: {error}"))
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

fn parse_json(body: &str) -> Value {
    serde_json::from_str(body)
        .unwrap_or_else(|error| panic!("response is not valid JSON ({error}): {body}"))
}

fn tool_payload(body: &str) -> (Value, Value) {
    let response = parse_json(body);

    assert!(
        response.get("error").is_none(),
        "tools/call unexpectedly returned a JSON-RPC error: {response}"
    );
    assert_eq!(
        response["result"]["content"][0]["type"], "text",
        "CallToolResult must contain a text content block: {response}"
    );
    assert!(
        response["result"]["isError"].is_boolean(),
        "CallToolResult.isError must be a boolean: {response}"
    );

    let text = response["result"]["content"][0]["text"]
        .as_str()
        .expect("CallToolResult text content must be a string");
    let payload = parse_json(text);

    (response, payload)
}

/// Returns the verdict and digest the server reports for a fixture.
fn rust_verdict(name: &str) -> (bool, Option<String>) {
    let body = responded(&tool_call(1, VALIDATE_TOOL, &read_fixture(name)));
    let (response, payload) = tool_payload(&body);

    assert_eq!(
        response["result"]["isError"], false,
        "validate semantic outcomes must not be tool execution errors: {response}"
    );

    let valid = payload["valid"]
        .as_bool()
        .expect("validate payload must contain a boolean `valid` field");
    let digest = payload["digest"].as_str().map(str::to_owned);

    if !valid {
        assert!(
            payload["error"]
                .as_str()
                .is_some_and(|error| !error.is_empty()),
            "invalid validate result must describe the validation failure: {payload}"
        );
    }

    (valid, digest)
}

struct PythonVerdict {
    valid: bool,
    status: String,
    digest: Option<String>,
}

fn python_verdict(name: &str) -> Option<PythonVerdict> {
    let probe = Command::new("python3").arg("--version").output();
    if probe.is_err() {
        eprintln!("skipping: python3 unavailable");
        return None;
    }

    let available = Command::new("python3")
        .args(["-c", "import jsonschema"])
        .output()
        .map(|output| output.status.success())
        .unwrap_or(false);
    if !available {
        eprintln!("skipping: python3 lacks jsonschema (reference validator dependency)");
        return None;
    }

    let path = fixture_path(name);
    assert!(
        Path::new(&path).exists(),
        "fixture is missing from the checkout: {path}"
    );

    let output = Command::new("python3")
        .arg("-c")
        .arg(PYTHON_SCRIPT)
        .arg(repo_root())
        .arg(&path)
        .output()
        .unwrap_or_else(|error| panic!("failed to spawn python3: {error}"));

    assert!(
        output.status.success(),
        "python reference validator failed on {name}:\n{}",
        String::from_utf8_lossy(&output.stderr)
    );

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stdout = stdout.trim();
    let result = parse_json(stdout);
    eprintln!("python reference validator said: {result}");

    Some(PythonVerdict {
        valid: result["valid"]
            .as_bool()
            .expect("python validator output must contain boolean `valid`"),
        status: result["status"].as_str().unwrap_or_default().to_owned(),
        digest: result["digest"].as_str().map(str::to_owned),
    })
}

#[test]
fn valid_fixture_agrees_with_python_and_pins_digest() {
    let (valid, digest) = rust_verdict("valid.json");
    assert!(valid, "the server must accept valid.json");
    assert_eq!(
        digest.as_deref(),
        Some(VALID_DIGEST),
        "server digest drifted from the pinned p0 digest"
    );

    // The digest tool must agree with the validate tool on the same bytes.
    let digest_body = responded(&tool_call(2, DIGEST_TOOL, &read_fixture("valid.json")));
    let (digest_response, digest_payload) = tool_payload(&digest_body);

    assert_eq!(digest_response["result"]["isError"], false);
    assert_eq!(
        digest_payload["digest"].as_str(),
        Some(VALID_DIGEST),
        "digest tool and validate tool disagree: {digest_body}"
    );

    let Some(python) = python_verdict("valid.json") else {
        return;
    };

    assert!(
        python.valid,
        "python reference validator rejected valid.json: {}",
        python.status
    );
    assert_eq!(
        python.digest.as_deref(),
        Some(VALID_DIGEST),
        "python and rust disagree on the p0 digest (python status {})",
        python.status
    );
}

#[test]
fn missing_field_fixture_is_rejected_by_both_sides() {
    let (valid, _) = rust_verdict("invalid_missing_field.json");
    assert!(!valid, "the server must reject invalid_missing_field.json");

    let Some(python) = python_verdict("invalid_missing_field.json") else {
        return;
    };
    assert!(
        !python.valid,
        "python reference validator accepted a record missing `audience`: {}",
        python.status
    );
}

#[test]
fn duplicate_key_fixture_is_rejected_by_both_sides() {
    let (valid, _) = rust_verdict("invalid_duplicate_key.json");
    assert!(!valid, "the server must reject invalid_duplicate_key.json");

    let Some(python) = python_verdict("invalid_duplicate_key.json") else {
        return;
    };
    assert!(
        !python.valid,
        "python reference validator accepted a duplicate `issuer_ref`: {}",
        python.status
    );
}

#[test]
fn invalid_fixtures_never_expose_a_digest() {
    for name in ["invalid_missing_field.json", "invalid_duplicate_key.json"] {
        let body = responded(&tool_call(3, VALIDATE_TOOL, &read_fixture(name)));
        let (response, payload) = tool_payload(&body);

        assert_eq!(response["result"]["isError"], false);
        assert_eq!(payload["valid"], false);
        assert!(
            payload.get("digest").is_none(),
            "a rejected record must not report a digest ({name}): {payload}"
        );
        assert!(
            payload["error"]
                .as_str()
                .is_some_and(|error| !error.is_empty()),
            "a rejected record must include its validation error ({name}): {payload}"
        );
    }
}
