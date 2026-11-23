---
document_metadata:
  domain: protocol
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every claim in §2 was measured at main 6212ec75 in this session: parse_dispatch has 22 match arms, 1 semantically validated, 1 structurally parsed, 20 root-discriminator-only, and validate_bmcp_message appears 0 times in crates/bmcp-server/src/lib.rs."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# TASK — add `validate_bmcp_message`, and do not let it lie

`main` is at `6212ec75`. Everything you need already exists; what is missing is one tool that
reaches it.

---

## 1. Hard constraints

**#0 — Do not write a JSON Schema validator, and do not add a `jsonschema` dependency.**
`crates/bmcp-protocol/Cargo.toml` has none, and `GAP-32` §6 explains why that is deliberate, not
an oversight. Adding one makes 20 message types conform to schema text that
`TECH-REALITY-001-C/README.md:70` records as **not frozen**. That work is unmergeable by
construction. If you find yourself reaching for a schema engine, stop and re-read this line.

**#1 — Do not claim more validation than the arm performed.** `DispatchValidationState` has three
values for a reason. A `RootDiscriminatorOnly` message is not a validated message and must not be
reported as one.

**#2 — Do not change the two existing tools.** `validate_applied_delivery_evidence` and
`digest_applied_delivery_evidence` must behave byte-identically to `6212ec75`.

**#3 — `lib.rs` may only be appended to** where the existing pattern is append-only. Never re-emit
a whole file.

**#4 — No `#[ignore]`, `todo!()`, `unimplemented!()`.** The workspace is at zero; keep it there.

**#5 — Report only commands you actually ran, with real output and real exit codes.** If you did
not run something, write `NOT RUN` and say why. Never fabricate output.

---

## 2. What is already there

`crates/bmcp-protocol/src/lib.rs`:

```rust
pub fn parse_dispatch(raw: &[u8]) -> Result<DispatchMessage, DispatchError>
```

22 match arms, one per message type:

| state | arms | backing |
|---|---|---|
| `SemanticallyValidated` | 1 — `APPLIED_DELIVERY_EVIDENCE_RECORDED` | `validate::from_strict_value` |
| `StructurallyParsed` | 1 — `Storage.PreparedParticipantReceipt` | its structural parser |
| `RootDiscriminatorOnly` | **20** | `StructurallyUnvalidatedMessage { message_type, value }` |

`StructurallyUnvalidatedMessage` carries the complete root object. Its doc comment says its fields
are "deliberately preserved without applying the APPLIED_DELIVERY_EVIDENCE field allowlist".

`parse_dispatch` is `pub` and **nothing in the workspace calls it.**

`crates/bmcp-server/src/lib.rs` exposes exactly two tools:

```rust
const VALIDATE_TOOL: &str = "validate_applied_delivery_evidence";
const DIGEST_TOOL: &str = "digest_applied_delivery_evidence";
```

Both are hardwired to one message type. `validate_bmcp_message` does not exist (`grep -c` → `0`).

---

## 3. The change

Add one tool, `validate_bmcp_message`, arguments `{"message": <object>}`, dispatching on the
`message_type` string inside that object. Wire it to `parse_dispatch`.

### 3.1 Result envelope

Read the validation state off the dispatched value, not off your own guess:

```json
{"valid": true, "message_type": "<as received>", "validation_state": "semantically_validated"}
{"valid": true, "message_type": "<as received>", "validation_state": "structurally_parsed"}
{"valid": true, "message_type": "<as received>", "validation_state": "root_discriminator_only"}
```

`validation_state` is **required** on every success. `root_discriminator_only` means exactly what
`DispatchValidationState` means by it: the discriminator was recognised and the JSON was strictly
parsed. It does not mean the payload conforms to its schema, and the field name must not be read as
if it did.

### 3.2 Failure envelope

| case | result |
|---|---|
| message is not valid JSON | `isError: true`, `{"valid":false,"message_type":null,"error":{...}}` |
| root is not an object | same, `message_type: null` |
| `message_type` missing | same, `message_type: null` |
| `message_type` not a string | same, `message_type: null` |
| `message_type` present but unknown | `isError: true`, `{"valid":false,"message_type":"<as received>","error":{...}}` |
| known type, body fails its validator | `isError: true`, `{"valid":false,"message_type":"<as received>","error":{...}}` |

**No case returns `-32601`.** The method exists; the message may not. That is the entire point of
`OWNER-DECISION-BMCP-MCP-DISPATCH-001` §3.1.

### 3.3 Why one tool and not 22

`message_type` is already the discriminator, and it already varies in shape —
`JF10_PREPARE_INTENT_REGISTERED` is SCREAMING_SNAKE, `Storage.PreparedParticipantReceipt` is
dot-Pascal. Any derivation rule for 22 tool names invents a second namespace beside the
authoritative one. Use the one in the message.

---

## 4. What not to do, and why each one is a trap

| tempting move | why it is wrong |
|---|---|
| add `jsonschema` and validate all 22 | the schemas are the unfrozen text (`GAP-32` §6) |
| return `{"valid":true}` without `validation_state` | flattens three states into a boolean; hides that 20 are unvalidated |
| return `{"valid":true}` for `root_discriminator_only` | claims schema conformance that was never established |
| add `digest_bmcp_message` for symmetry | `p0_digest` is defined for one type; 19 canonicalisation profiles do not exist |
| return `-32601` for unknown `message_type` | reports a message problem as a method problem |
| change `validate_applied_delivery_evidence` "while you are in there" | forbidden by constraint #2; its behaviour is the baseline others are compared against |

---

## 5. Acceptance criteria

The task is done when all of these hold and you have shown the command and its output for each:

1. `tools/list` returns a third tool named exactly `validate_bmcp_message`.
2. A conforming `APPLIED_DELIVERY_EVIDENCE_RECORDED` returns
   `validation_state: "semantically_validated"`.
3. A conforming `Storage.PreparedParticipantReceipt` returns
   `validation_state: "structurally_parsed"`.
4. **Each of the 20 remaining types**, given a message that strictly parses and carries a known
   `message_type`, returns `{"valid":true, "validation_state":"root_discriminator_only"}`. All 20
   are named in `GAP-32` §2 and in `parse_dispatch`'s match arms; a test that covers 19 of them and
   claims 20 is the specific failure this criterion exists to catch.
5. A message whose `message_type` is absent, non-string or unknown returns `isError: true`,
   `valid:false`, and never `-32601`.
6. A known type with a body that fails its own validator returns `isError: true`, `valid:false`.
7. The two pre-existing tools behave byte-identically to `6212ec75`; show the test that proves it.
8. `digest` is offered for no new type.
9. `grep -rn '^#\[ignore' --include=*.rs crates/` → 0 hits.
   `grep -rn 'todo!\|unimplemented!' --include=*.rs crates/` → 0 hits.
10. `cargo test --workspace --all-targets --no-fail-fast` → 0 failed, 0 ignored.

---

## 6. What this task deliberately does not settle

- **Transport framing, session, handshake, ACK, replay.** Still `DEPENDENCY_NOT_FROZEN`. This tool
  is an MCP tool; it freezes no bytes on any wire. RT-01..RT-09 stay blocked.
- **C/H `COutcomeRecord` mapping.** `C-CON-017` / `C-CON-019` stay `NOT ACCEPTED`. Unchanged.
- **Schema validation for the 20.** Still open, still blocked on the freeze. This task makes the
  state *reportable*; it does not make the state *better*, and it must not appear to.
- **`Published` disposition.** Unchanged; external issuers, per
  `D-OWNER-DECISION-PARTICIPANT-ADMISSION-001` and `D-OWNER-DECISION-PROTECTED-VISIBILITY-001`.

---

## 7. Provenance

Dispatched by the owner-proxy session that measured `GAP-32` at `6212ec75` and authored
`OWNER-DECISION-BMCP-MCP-DISPATCH-001` (#733, merged `9b95e8bb`). This prompt is a task
description, not a decision: the decision is already merged. If this prompt and the ruling
disagree, **the ruling wins** and the discrepancy is a finding to report, not a choice to make.
