---
document_metadata:
  domain: protocol
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Unverified
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-16 — BMCP is a single-message validator, not a protocol stack

**Status:** Open — 1 of 22 message types has a Rust parser; transport has no specification at all
**Area:** bmcp-protocol / 08-bmcp-protocol
**Measured at:** `main @ b47bd97cc40a80cd1f50674838fad04590f740b1`, `2026-11-22T05:15Z`
**Related:** GAP-13 (participant admission needs `JF10_*` messages), GAP-14-B, `protocol-index.md`, `B-P2-XO-01`

## 1. The claim being measured

The working baseline says *"BMCP 完整协议栈（60% 未实现）"*. That sentence is not measurable — 60% of what? This document replaces it with two counts and one absence.

## 2. What exists, counted

`crates/bmcp-protocol` is 1549 lines, one source file, three dependencies (`serde`, `serde_json`, `sha2`). It exposes exactly one public entry point:

```rust
// crates/bmcp-protocol/src/lib.rs:1033
pub fn parse_and_validate(
    raw: &[u8],
) -> Result<evidence::AppliedDeliveryEvidence, validate::EvidenceError>
```

That signature is the whole finding. It returns **one** type, named in the return position. There is no dispatch, no envelope, no `enum Message`, no registry.

### 2.1 Message type coverage: 1 of 22

```
$ python3 08-bmcp-protocol/scripts/check_protocol_index.py
schema_files=32
schemas_with_message_type=31
unique_message_types=22
index_rows=22
PASS
```

22 unique `message_type` values are declared across the schemas. The Rust parser handles one:

| | count |
|---|---:|
| unique `message_type` in schemas | 22 |
| parsed by `crates/bmcp-protocol` | **1** |
| index rows marked `IMPLEMENTED (artifact presence)` | 2 |
| index rows marked `PARTIAL` | 1 |
| index rows with schema + reference tests only | 19 |

The single Rust-parsed type is `APPLIED_DELIVERY_EVIDENCE_RECORDED`. The other 21 — including every `JF10_*` message GAP-13 depends on — exist as JSON Schema and, in some cases, reference Python, with no Rust parser.

### 2.1a The index's `IMPLEMENTED` does not mean what a reader assumes

Two rows are marked `IMPLEMENTED (artifact presence)`: `APPLIED_DELIVERY_EVIDENCE_RECORDED` and `RECOVERY_JOIN_PROOF`. Only the first has a Rust parser. Neither the second nor the one `PARTIAL` row (`C_PROVIDER_OUTCOME_RECORDED`) appears anywhere in `crates/`:

```
$ grep -rn "RECOVERY_JOIN_PROOF" crates/          # no output
$ grep -rn "C_PROVIDER_OUTCOME_RECORDED" crates/  # no output
```

"Artifact presence" means a Python validator and a test file exist. That is a real thing to record — but it is not a protocol implementation, and the word `IMPLEMENTED` in a status column will be read as one by anyone skimming. The index says so in its own preamble (*"not a production-conformance claim"*), which is honest; the column header still does the misleading. A status column that needs a disclaimer to be read correctly is a column that should be renamed.

### 2.2 It is not a dispatcher that happens to have one arm

This distinction matters, because "add the other 21 arms" would be a different task from "add a dispatcher". The current code hard-compares the type:

```rust
// crates/bmcp-protocol/src/lib.rs:892-903
let consts = [
    ("schema_artifact_revision", "1.0.0"),
    ("message_type", "APPLIED_DELIVERY_EVIDENCE_RECORDED"),
];
for (field, expected) in consts {
    let actual = string_field(&value, field)?.to_owned();
    if actual != expected {
        return Err(EvidenceError::WrongConst { field, expected, actual });
    }
}
```

An `APPLIED_ACK` message is not "unimplemented" — it is `WrongConst { field: "message_type", expected: "APPLIED_DELIVERY_EVIDENCE_RECORDED", actual: "APPLIED_ACK" }`. The parser has no concept of a message it does not already expect. Calling this "60% implemented" overstates it: a single-type parser is not 40% of a 22-type protocol, it is a different category of artifact.

## 3. What does not exist, and is not merely unwritten

`protocol-index.md:162` states its own scope:

> The checker is an index-consistency gate only. It does not validate the message semantics, transport, framing, session, handshake, production runtime, or C/D/I/Storage authority.

### 3.1 A server does exist, and it is not a BMCP server

`crates/bmcp-server` is a workspace member: 723 lines of `lib.rs`, a 67-line `main.rs`, and a 166-line `rt_scenarios.rs`. It binds a TCP listener, enforces a concurrency cap and a per-request deadline, and dispatches on a JSON-RPC `method` string:

```rust
// crates/bmcp-server/src/lib.rs:275-290
if method == "initialize" {
    RequestOutcome::Responded { body: format!("...protocolVersion\":\"2024-11-05\"...") }
} else {
    RequestOutcome::Responded { body: format!("...\"code\":-32601,\"message\":\"Method not found\"...") }
}
```

That is an **MCP transport skeleton**, not a BMCP one. It has exactly one implemented method (`initialize`) and returns `-32601 Method not found` for everything else.

It never calls the BMCP parser. The only reference to `bmcp_protocol` anywhere in `bmcp-server` is a dead formatter, and its own comment says so:

```rust
// crates/bmcp-server/src/lib.rs:718-723
// EvidenceError's Display/Error implementations are intentionally not assumed.
// This local formatter is available for a future evidence-validation call site.
#[allow(dead_code)]
fn describe(error: &bmcp_protocol::validate::EvidenceError) -> String {
    format!("{error:?}")
}
```

`#[allow(dead_code)]` plus "for a future call site" plus zero call sites is the whole state of the wire-to-parser route: **a listener exists, and no BMCP message type reaches a parser.** The 22 types have no route from wire to validation.

### 3.2 The transport decision is still unfrozen

Framing, session and handshake are not implemented and not specified — and that is an unfrozen decision, not a backlog item:

- `13-engineering-decisions/technology-research/TECH-REALITY-001-C/README.md:70` — *"H wire mapping remains NOT FROZEN."*
- `.../agent-integration-cross-owner-contract-matrix.md:18` — *"C/H wire mapping remains NOT FROZEN"*, with the H validator only calling an injected `verify_c_final_boundary` callback that **current tests stub to `True`**.
- `.../agent-integration-cross-owner-contract-matrix.md:85` — *"C/H mapping is therefore NOT ACCEPTED / NOT VERIFIED pending exact resolution and mismatch vectors."*
- `02-domain-model/phase-2-domain-extension.md:263` — *"H wire mapping and schema"* is listed under things the domain model explicitly does **not** decide.

The existing `bmcp-server` does not settle this. It chose JSON-RPC over TCP with newline framing, which is a reasonable local choice, but nothing records it as the BMCP wire mapping, and `protocol-index.md` still says framing and session are out of scope. A choice made in code without a decision behind it is exactly what the next section warns about.

So the honest decomposition of "60% unimplemented" is:

| component | state | blocked by |
|---|---|---|
| 21 message parsers | absent | nothing — transcription from existing schemas |
| envelope / dispatch | absent | nothing — a design choice, small |
| wire-to-parser route | **absent** | `bmcp-server`'s only `bmcp_protocol` reference is `#[allow(dead_code)]` |
| framing / session / handshake | absent | **H wire mapping, NOT FROZEN** |
| signature verification | absent | **C crypto profile + I trust registration, not deployed** |
| transport listener | **present** (JSON-RPC/TCP, 1 method) | — |

Two of six rows are ordinary work, one is a routing gap, two are blocked on decisions, one is done. That is a materially different picture from both "60% missing" and "the stack is there".

## 4. The one stub that must not be trusted

The H validator's `verify_c_final_boundary` is injected and stubbed to `True` in the current tests. That is a legitimate test seam — but it means **no test in the tree proves a boundary mismatch is rejected**. This is the same defect shape as `dm2_06`: a check whose negative case has never run, described in a way that reads as though it had.

It should be recorded as such before anyone counts the H validator as coverage. A stub returning `True` is not a verification; it is the absence of one, wearing a function signature.

## 5. What can be done without the decision, and what cannot

**Can, now:** add a `message_type` dispatch layer and parsers for the 21 schema-declared types. This is transcription against existing JSON Schema, needs no H decision, and would move the count from 1/22 to 22/22. Routing them from `bmcp-server` to the parser is a second, smaller step that also needs no decision — the listener already exists and already parses JSON.

**Cannot, now:** framing, session, handshake, and anything that assumes a settled wire mapping. All three require `H wire mapping` to freeze, and it is `NOT FROZEN` in every record that mentions it. The existing JSON-RPC/TCP choice is a local implementation decision, not a recorded one, so building on it is building on an undocumented premise.

**Should not, now:** build a dispatcher that pretends to be a protocol stack. A `parse_any()` returning a boxed enum, wired into `bmcp-server` with no framing or session contract, would let the baseline claim "BMCP 80% complete" while remaining exactly as unusable as it is today. That is the failure mode this document exists to prevent.

## 6. Revised statement for the baseline

Replace *"BMCP 完整协议栈（60% 未实现）"* with:

> BMCP has a schema layer (32 schemas, 22 message types, index-consistent) and a Rust validator for 1 of the 22. The index marks two rows `IMPLEMENTED`, but only one of those has a Rust parser; the other has a Python validator and a test file. A JSON-RPC/TCP listener exists in `crates/bmcp-server` with exactly one method (`initialize`) and no route to the parser at all — its only reference to `bmcp_protocol` is a `#[allow(dead_code)]` formatter awaiting "a future evidence-validation call site". Framing, session, handshake and signature verification are absent, and the first three are blocked on `H wire mapping`, which is recorded as `NOT FROZEN` in every engineering-decision record that mentions it. The largest available increment is 21 parsers, which is transcription, not design.

That sentence is checkable, and it tells the next person which half they can start on.

## 7. Closure criteria

1. `parse_and_validate` becomes `parse_message`, returning a dispatch enum, with one arm per schema-declared type — 22 arms, not 1.
2. A conformance test per message type, driven by the schema's own `const`, so the count cannot silently drift from the index.
3. `H wire mapping` frozen in a decision record, with an exact version/SHA — prerequisite for any transport work, not for the parsers.
4. `verify_c_final_boundary` gains a test that returns `False` and proves the rejection path, replacing the `True` stub as the only evidence.
