use serde_json::Value;
use std::fs;
use std::process::Command;
use std::sync::atomic::{AtomicU64, Ordering};

static NEXT_ID: AtomicU64 = AtomicU64::new(1);

#[test]
fn raw_event_to_persisted_memory_context_and_compiler_gate_is_observable() {
    let nonce = NEXT_ID.fetch_add(1, Ordering::Relaxed);
    let output_path = std::env::temp_dir().join(format!(
        "brain-e2e-full-chain-{}-{nonce}.json",
        std::process::id()
    ));
    let sidecar_path = std::path::PathBuf::from(format!(
        "{}.compiler-status",
        output_path.display()
    ));
    let fixture = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("fixtures")
        .join("event.json");

    let output = Command::new(env!("CARGO_BIN_EXE_brain"))
        .arg("compile")
        .arg("--input")
        .arg(&fixture)
        .arg("--out")
        .arg(&output_path)
        .arg("--verbose")
        .output()
        .expect("execute brain compile");

    assert_eq!(
        output.status.code(),
        Some(0),
        "CLI failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );

    let bytes = fs::read(&output_path).expect("read ContextSnapshot output");
    let snapshot: Value =
        serde_json::from_slice(&bytes).expect("output must be a serialized ContextSnapshot");

    assert_eq!(snapshot["identity"]["context_id"], "context-demo-001");
    assert_eq!(snapshot["context_version"], 1);
    assert_eq!(snapshot["entries"].as_array().expect("entries must be an array").len(), 1);
    assert_eq!(snapshot["entries"][0]["memory_id"], "memory-demo-001");
    assert_eq!(
        snapshot["entries"][0]["memory_version_id"],
        "memory-version-demo-001"
    );
    let rendered = snapshot["entries"][0]["rendered_content"]
        .as_str()
        .expect("entry content must be serialized as text");
    assert!(rendered.contains("uses"));
    assert!(rendered.contains("a governed memory context"));

    let sidecar =
        fs::read_to_string(&sidecar_path).expect("compiler status sidecar must be written");
    assert!(
        sidecar.starts_with("compiler stage blocked:"),
        "the production compiler gate must expose its typed Blocked disposition: {sidecar}"
    );

    let _ = fs::remove_file(&output_path);
    let _ = fs::remove_file(&sidecar_path);
}
