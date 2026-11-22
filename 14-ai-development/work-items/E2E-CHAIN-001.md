# E2E-CHAIN-001 — End-to-end chain reachability measurement

**Status:** Measurement complete; one additive CLI E2E test proposed below, execution not locally verified  
**Repository:** `oahcom/AiMemoryBrainArchitecture`  
**Observed ref:** `main` (recursive Git tree `666d77da77d28926abdd2f6784d1e89e0be654b5`)  
**Scope:** 11 Rust workspace crates; no `src/` changes

**Method note:** files, manifest contents, and line numbers were inspected through the GitHub repository tree/file API. The shell commands below are reproducible verification commands, not commands executed in this session; `grep`, `cargo tree`, and `cargo test` were not run locally.

## Executive finding

The premise “there is no cross-crate integration test” is false on the observed `main`: there are 14 Rust integration-test files, including a five-crate positive Store→SQLite→Context chain (`memory-context/tests/e2e_store_to_context.rs`) and a seven-crate executable path through `brain-cli` and `memory-compiler`. However, the current CLI test only asserts that the output is JSON object-shaped, not that the expected persisted revision appears in the resulting snapshot. The test proposed in §1.4 closes that assertion gap.

The actual seven-crate path ends in a **Blocked** compiler publication disposition, not a Published derivative. It does not include durable EventStore acceptance, Agent integration delivery, or BMCP protocol encoding.

## 1.1 Dependency reachability matrix

Direction means “crate A declares a dependency on crate B”; this is a dependency graph, not a runtime call graph. The graph includes dependencies declared under both `[dependencies]` and `[dev-dependencies]`.

Legend:

- `D(P)` — direct production dependency (`[dependencies]`).
- `D(T)` — direct test-only dependency (`[dev-dependencies]`).
- `I2`, `I3` — shortest indirect path of 2 or 3 declared edges, all production edges.
- `I2T`, `I3T` — shortest indirect path includes at least one test-only edge; this is **not** a production-reachability claim.
- `×N` — no directed path exists in the declared manifest graph. The reason is absence of a dependency path, not an assumed type mismatch. For any such cell, reproduce with `cargo tree` as shown immediately after the matrix.

| crate A → crate B | agent-integration | bmcp-protocol | brain-cli | memory-compiler | memory-context | memory-domain | memory-event-store-sqlite | memory-event-store | memory-storage-sqlite | memory-storage | memory-store |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `agent-integration` | — | ×N | ×N | ×N | D(P) | D(P) | I2T | I3T | I2T | I2T | I2T |
| `bmcp-protocol` | ×N | — | ×N | ×N | ×N | ×N | ×N | ×N | ×N | ×N | ×N |
| `brain-cli` | ×N | ×N | — | D(P) | D(P) | D(P) | I2T | I2T | D(P) | D(P) | D(P) |
| `memory-compiler` | ×N | ×N | ×N | — | ×N | D(P) | D(T) | D(T) | D(T) | D(P) | ×N |
| `memory-context` | ×N | ×N | ×N | ×N | — | D(P) | D(T) | I2T | D(T) | D(T) | D(T) |
| `memory-domain` | ×N | ×N | ×N | ×N | ×N | — | ×N | ×N | ×N | ×N | ×N |
| `memory-event-store-sqlite` | ×N | ×N | ×N | ×N | ×N | D(P) | — | D(P) | ×N | ×N | ×N |
| `memory-event-store` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | — | ×N | ×N | ×N |
| `memory-storage-sqlite` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | ×N | — | D(P) | ×N |
| `memory-storage` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | ×N | ×N | — | ×N |
| `memory-store` | ×N | ×N | ×N | ×N | ×N | D(P) | ×N | ×N | D(T) | D(P) | — |

Manifest evidence (line numbers are 1-based):

- Workspace membership: `Cargo.toml:1-13` lists exactly these 11 crates.
- `agent-integration/Cargo.toml:8-11`: production deps are `memory-context` and `memory-domain`.
- `bmcp-protocol/Cargo.toml:8-11`: only external serde/serde_json/sha2; no workspace-crate dependency.
- `brain-cli/Cargo.toml:12-21`: direct production deps include domain, storage, storage-sqlite, store, context, compiler; no agent-integration, event-store, event-store-sqlite, or bmcp-protocol.
- `memory-compiler/Cargo.toml:8-23`: domain and storage are production deps; event-store, event-store-sqlite and storage-sqlite are dev-dependencies.
- `memory-context/Cargo.toml:8-17`: domain is the only production workspace dep; event-store-sqlite, store, storage and storage-sqlite are test-only deps.
- `memory-store/Cargo.toml:8-13`: domain and storage are production deps; storage-sqlite is test-only.
- `memory-event-store-sqlite/Cargo.toml:8-14`: domain and event-store are production deps.
- `memory-storage-sqlite/Cargo.toml:8-14`: domain and storage are production deps.
- `memory-storage/Cargo.toml:8-9` and `memory-event-store/Cargo.toml:8-9`: domain is their production dependency.

For any individual `×N` cell, substitute its row and column names into this command; a no-match is the expected evidence for that cell. Example (`agent-integration → bmcp-protocol`):

```sh
cargo tree -p agent-integration -e normal,dev --prefix none | grep -F "bmcp-protocol v"
# expected: no match (exit status 1)
```

The BMCP no-caller claim can be reproduced with `grep -RInE 'bmcp_protocol|bmcp-protocol' crates --exclude-dir=bmcp-protocol` (expected: no matches). The EventStore production-call absence can be checked with `grep -RInE 'EventStore|SqliteEventStore|memory_event_store' crates/brain-cli/src crates/memory-compiler/src` (expected: no matches). The direct edge inventory can also be reproduced with:

```sh
grep -nE '^(memory-[a-z-]+|agent-integration|bmcp-protocol)[[:space:]]*=' crates/*/Cargo.toml
```

For each `×N`, the absence of a path means no sequence of declared workspace dependency edges connects A to B. It does **not** imply a type mismatch. `I*T` entries are test-only reachability and must never be described as a production path.

## 1.2 Breakpoint inventory (ordered by estimated repair cost)

| Breakpoint | Location (file:line) | Broken nature | What repair requires | Existing carrier |
|---|---|---|---|---|
| BMCP has no workspace integration edge or caller | `crates/bmcp-protocol/Cargo.toml:8-11`; no references outside its own crate | **Zero dependency** | Choose and document the owning boundary; declare a dependency from that owner and add a real call/serialization path plus a cross-crate contract test. No existing caller is present to extend. | No identified carrier; BMCP crate's own `tests/p0_conformance.rs` is protocol-local only. |
| Durable EventStore acceptance is not wired into the CLI/compiler path | `crates/brain-cli/Cargo.toml:12-21`; `crates/memory-compiler/Cargo.toml:20-23`; `crates/brain-cli/src/main.rs:246-254` | **Zero production dependency** (compiler has test-only deps) | Add a production adapter seam that reads an actual `AcceptedReceipt`/payload from EventStore and feeds the compiler; preserve durable receipt, payload digest, scope and idempotency semantics. | Existing test carrier: `crates/memory-compiler/tests/event_store_digest_compat.rs` proves digest compatibility only; no production carrier currently. |
| EventStore-to-compiler identity boundary is nominally incompatible | `crates/memory-domain/src/lib.rs:8-24`; `crates/memory-event-store/src/lib.rs:35-43`; `crates/memory-compiler/src/lib.rs:39-48` | **Type incompatibility** | Add an explicit, validating conversion/adapter between `OpaqueId` and compiler `Identity(String)`; do not assume implicit conversion. Add tests for empty IDs and identity preservation. | Test-only compatibility carrier `crates/memory-compiler/tests/event_store_digest_compat.rs`; no production adapter. |
| Agent integration is not in the executable CLI delivery path | `crates/agent-integration/Cargo.toml:8-11`; `crates/brain-cli/Cargo.toml:12-21`; `crates/agent-integration/tests/context_snapshot_delivery.rs:38-60,63-108` | **Zero dependency** between CLI and agent-integration; existing agent tests have fixtures, not Store-derived snapshots | Add a deliberate application boundary that passes the produced `ContextSnapshot` into the Agent adapter and asserts the delivered payload/version. Keep inference-provider claims outside this boundary. | Existing carrier: `crates/agent-integration/tests/context_snapshot_delivery.rs`, but it constructs its own `ContextCandidate`; it is not connected to storage/CLI. |
| Context crate declares an unused EventStore-SQLite test dependency | `crates/memory-context/Cargo.toml:13-17`; `grep -RIn 'memory_event_store_sqlite' crates/memory-context/tests` | **Dependency exists but no call point** in the context integration tests | Either remove the unused dev-dependency or add a test that actually accepts/reads an event through it and documents the intended edge. This is lower cost and should not be confused with a production dependency. | Existing carrier: `crates/memory-context/tests/e2e_store_to_context.rs` covers Store/SQLite/Context, not EventStore. |

### Type-boundary evidence

`OpaqueId` is a private-field newtype with `new`/`as_str` (`memory-domain/src/lib.rs:8-24`). Compiler `Identity` is a separate public tuple newtype over `String` (`memory-compiler/src/lib.rs:39-48`). EventStore's `AcceptedReceipt` carries `OpaqueId` for `event_id` and `receipt_id` (`memory-event-store/src/lib.rs:35-43`). There is no implicit assignment compatibility; an explicit conversion must be authored. Reproduce the conversion search with:

```sh
grep -RInE 'impl[[:space:]]+From<.*(OpaqueId|Identity)|impl[[:space:]]+From<(OpaqueId|Identity)' crates/memory-domain crates/memory-compiler
```

### Important correction to earlier gap statements

On the observed `main`, `brain-cli` **does call** `MemoryCompiler::compile`: `crates/brain-cli/src/main.rs:246-254,280-290`. It constructs `AdmissionPublicationAuthority` and invokes `compile`; this is not the old “compiler skipped/no production caller” state described by the older GAP-07 work item. The production authority currently reports `canonical_commit_confirmed`, `publication_participant_admitted`, and `protected_visibility_authorized` as `false` (`crates/memory-compiler/src/publication_authority.rs:99-101`). Therefore the real CLI path reaches the gate and ends Blocked; it does not publish. Do not reuse the stale “compiler is not called” claim.

## 1.3 Existing integration-test coverage: all 14 Rust files

Count evidence:

```sh
ls crates/*/tests/*.rs
ls crates/*/tests/*.rs | wc -l
# 14
```

The list below counts workspace crates whose APIs/types are imported or whose executable is invoked, not third-party libraries.

| # | Integration-test file | Crates crossed | Edge actually exercised | What it cannot prove |
|---:|---|---:|---|---|
| 1 | `agent-integration/tests/context_snapshot_delivery.rs` | 3 (`agent-integration`, `memory-context`, `memory-domain`) | Fixture candidate → `build_context` → `DeliveryPayload::from_snapshot` → in-memory adapter | Does not create/read a Memory from SQLite; does not test EventStore, CLI, BMCP or real Agent runtime. |
| 2 | `agent-integration/tests/delivery_lifecycle.rs` | 1 | Delivery state transitions and attestation invariants inside Agent integration | Does not build a ContextSnapshot or cross any storage/protocol boundary. |
| 3 | `bmcp-protocol/tests/p0_conformance.rs` | 1 | BMCP digest and strict conformance vectors | Does not exchange a message with Agent integration or consume a real ContextSnapshot. |
| 4 | `brain-cli/tests/compiler_skip_is_visible.rs` | 7 (CLI plus domain, storage, storage-sqlite, store, context, compiler) | Executes the `brain compile` binary; asserts exit status, blocked notice/sidecar and JSON-object output | Despite the legacy filename, it does not assert the exact snapshot entry, memory ID/version, or prove EventStore acceptance, Agent delivery, BMCP encoding, or Published outcome. |
| 5 | `memory-compiler/tests/event_store_digest_compat.rs` | 4 (`memory-compiler`, `memory-domain`, `memory-event-store`, `memory-event-store-sqlite`) | SQLite EventStore receipt digest accepted by compiler ingestion | Does not make EventStore a production dependency of compiler/CLI; digest compatibility is not an end-to-end accepted-event pipeline. |
| 6 | `memory-context/tests/e2e_negative_paths.rs` | 5 (`memory-context`, `memory-domain`, `memory-storage`, `memory-storage-sqlite`, `memory-store`) | Store/SQLite/Context scope, lifecycle, forget, stale-write, budget and restart negative paths | Does not pass through EventStore, compiler, Agent integration or BMCP. |
| 7 | `memory-context/tests/e2e_store_to_context.rs` | 5 (`memory-context`, `memory-domain`, `memory-storage-sqlite`, `memory-store`, plus storage trait) | Real SQLite Store create/write/read → ContextSnapshot build from persisted Claim | Does not include raw EventStore acceptance, compiler, Agent delivery or BMCP. It is already a genuine five-crate positive E2E path. |
| 8 | `memory-domain/tests/phase2_acceptance.rs` | 1 | Domain claim/fact/relation/provenance acceptance rules | Does not cross any crate boundary or persist data. |
| 9 | `memory-event-store-sqlite/tests/forget_fence.rs` | 1 | ForgetFence restore/fail-closed/concurrency behavior with a hand-built schema | Does not enforce the MemoryStore read path or build Context. |
| 10 | `memory-event-store-sqlite/tests/forget_fence_real_schema.rs` | 3 (`memory-event-store-sqlite`, `memory-event-store`, `memory-domain`) | Fence restore against a database built by the actual EventStore schema | Does not cross into MemoryStorage/MemoryStore or Context; event rows are not canonical Memory revisions. |
| 11 | `memory-event-store-sqlite/tests/resilience.rs` | 3 (`memory-event-store-sqlite`, `memory-event-store`, `memory-domain`) | Payload custody, digest tamper detection, replay, concurrency, rollback and WAL recovery | Does not connect event acceptance to compiler ingestion or Context assembly. |
| 12 | `memory-store/tests/cross_crate_contract.rs` | 4 (`memory-store`, `memory-storage`, `memory-storage-sqlite`, `memory-domain`) | Store facade + trait + SQLite round-trip, scope, CAS, idempotency and duplicate create | Does not build Context or involve EventStore/compiler/Agent/BMCP. |
| 13 | `memory-store/tests/forget_e2e.rs` | 4 (`memory-store`, `memory-storage`, `memory-storage-sqlite`, `memory-domain`) | MemoryStore forget facade and version/sibling visibility semantics | Does not use the separate EventStore ForgetFence, Context, compiler or protocol. |
| 14 | `memory-store/tests/sqlite_integration.rs` | 4 (`memory-store`, `memory-storage`, `memory-storage-sqlite`, `memory-domain`) | Minimal SQLite MemoryStore path and facade identity validation | Does not build Context or exercise event acceptance/compiler/Agent/BMCP. |

The crucial distinction: a test named `e2e_*`, a green workspace, or a cross-crate import does not establish the full product chain. Each row above has an explicit boundary it does not cross.

## 1.4 One minimum credible E2E proposal

**Selected chain (seven workspace crates):**

`raw event JSON fixture → brain-cli → memory-domain validation → memory-storage-sqlite → memory-storage / memory-store → memory-context ContextSnapshot → memory-compiler publication gate → output snapshot + compiler-status sidecar`

Why this chain: it is the longest currently wired executable route that has an existing runnable binary and a checked-in fixture. It requires no `src/` changes and no new production dependency. `brain-cli/src/main.rs:304-479` parses and validates the input, creates and persists the Memory/revision, reads the persisted revision, derives a ContextCandidate, and builds the snapshot. `main.rs:246-290` runs the compiler through `AdmissionPublicationAuthority`; `main.rs:502-520` serializes the snapshot and emits the compiler disposition. The current integration test already invokes the binary (`compiler_skip_is_visible.rs:59-75,129-159`).

**Start:** the checked-in `crates/brain-cli/fixtures/event.json` raw event/payload/Memory/Claim/Context request.

**End / assertions:** a valid serialized `ContextSnapshot` whose `identity.context_id` is `context-demo-001`, whose first entry references `memory-demo-001` and `memory-version-demo-001`, and whose adjacent `.compiler-status` sidecar declares `compiler stage blocked:`. The Blocked result is expected under today's production authority: three proof flags have no authoritative issuer and remain false.

**Proves:** the executable's current JSON-input path validates domain values; creates and persists a Memory and revision in SQLite through MemoryStore; reads that persisted revision; derives a candidate from the stored Claim; builds and serializes a ContextSnapshot; invokes the compiler and preserves its typed Blocked outcome in a sidecar.

**Does not prove:** durable EventStore acceptance/receipt or payload custody; an EventStore-to-compiler conversion; compiler publication (the result is intentionally Blocked); Agent adapter delivery; BMCP serialization/signing/conformance; model inference or provider-side application. It is an E2E for the currently wired CLI→Context→Compiler-gate route, not an E2E for all 11 crates.

### Segment 2 — additive test

The existing `compiler_skip_is_visible.rs` test only checks that the snapshot JSON root is an object. The following additive test strengthens that assertion without touching `src/`. It is placed beside the existing CLI process test because the CLI is the only current production entry point that wires all seven crates.

File: `crates/brain-cli/tests/e2e_full_chain.rs`

```rust
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
```

**Execution status:** not run in this measurement session. The connected local terminal was unavailable due its monthly usage limit; GitHub file inspection confirms that the binary, fixture, `serde_json` dependency, and CLI process-test pattern already exist, but this session cannot truthfully claim `cargo test --workspace --offline` passed. Before treating the additive test as accepted, run:

```sh
cargo test --workspace --offline
ls crates/*/tests/*.rs | wc -l
# expected: all tests green; 15
```

No `src/` file was modified. No production dependency was added. If the additive test fails, retain the measurement and repair the test fixture/assertion only; do not alter implementation code under this work item.

## Finding for registration

- **Evidence:** `cargo tree -p brain-cli -e normal,dev` plus `crates/brain-cli/src/main.rs:418-479,502-520` reproduces the seven-crate Store→Context path; `crates/brain-cli/tests/compiler_skip_is_visible.rs:59-75,129-159` shows the existing process-level test only asserts an object-shaped JSON output; `crates/agent-integration/Cargo.toml:8-11` and `crates/bmcp-protocol/Cargo.toml:8-11` show their separate dependency boundaries.
- **Judgment:** the CLI→MemoryStore→ContextSnapshot→Compiler gate edge is connected, but the test oracle is too weak to prove persisted identity; EventStore acceptance, Agent delivery and BMCP remain disconnected from that executable chain. Compiler publication itself is reached but intentionally Blocked.
- **Next step:** Owner A adds/executes `crates/brain-cli/tests/e2e_full_chain.rs` and verifies exact snapshot identity plus the Blocked sidecar with `cargo test --workspace --offline`; Owner E/Owner D separately supplies authoritative issuers for the three false publication flags; the protocol/Agent owners must then define and test their own explicit adapter boundaries.

## Recommendation

If only one broken edge may be repaired first, connect durable EventStore acceptance to the CLI/compiler ingestion boundary: it removes the earliest semantic gap between a raw event and the currently executable Memory/Context/Compiler path, and gives later Agent/BMCP work a real accepted-event identity and payload to consume.
