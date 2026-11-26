---
document_metadata:
  domain: protocol
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Owner H acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open."
      decision_date: "2026-11-23"
      approved_version:
        scheme: content-hash
        value: "b121682f2084fe89346d254288de4f8202311ff4b18a2744a407aaff2fb0d137"
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Issue #751 comment 7097692424 — owner ruling that the five DECIDED records must agree with their own bodies"
        - "14-ai-development/adr/OWNER-DECISION-BMCP-MCP-DISPATCH-001.md — the DECIDED line in this document names the decider and the date"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every code reference in §2 was read at main 0527ecf6 in this session; the 22-message-type count is reproduced by 08-bmcp-protocol/scripts/check_protocol_index.py (PASS) at the same commit. Re-checked at 0dc8f5a2: the three intervening commits touch only .github/workflows/branch-freshness.yml, scripts/ci/check_branch_freshness.py, scripts/ci/test_check_branch_freshness.py and crates/memory-compiler/src/admission.rs, none of which is a BMCP path, so no §2 figure moves."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: the BMCP-to-MCP tool binding is exactly one dispatch tool, selected by the message's own message_type field; no per-type tool names and no digest extension."
    canonical_scope_id: protocol/bmcp-mcp-dispatch-binding
    canonical_scope_keywords:
      - bmcp-mcp-binding
      - validate-bmcp-message
      - message-type-dispatch
      - transport-not-frozen
    canonical_conflict_status: None
    normative_status: Normative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# OWNER-DECISION-BMCP-MCP-DISPATCH-001 — freeze the tool binding, not the wire

**Status:** DECIDED (owner-proxy decision, 2026-11-23)
**Decided by:** Owner H acting as owner proxy, under the standing instruction that a blocking decision with no human available is to be taken and recorded rather than left open. Same mechanism as `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` and `D-OWNER-DECISION-CANONICAL-COMMIT-001`.
**Effect:** gives the 19 unparsed BMCP message types a consumer. Does **not** freeze transport framing, session, handshake, ACK, or the C/H COutcomeRecord mapping.
**Scope:** the binding between a BMCP message and an MCP tool call. Nothing else.

---

## 1. The gap this decides, stated narrowly

`07-agent-integration/agent-integration-architecture-completion.md:168` records:

> H transport binding | No accepted complete Agent Integration transport binding identified in Owner-controlled baseline source set | DEPENDENCY_NOT_FROZEN

and `:169` records ACK/replay/reconnect as equally open. Read literally, that blocks every downstream step, and it is why RT-01..RT-09 are all NOT RUN.

But there is already a running binding in the tree, and it is narrower than "transport". `crates/bmcp-server/src/lib.rs` implements MCP methods `initialize`, `tools/list` and `tools/call`, and exposes exactly two tools, both hardwired to one message type:

- `validate_applied_delivery_evidence`
- `digest_applied_delivery_evidence`

Both call `bmcp_protocol::parse_and_validate`. There is no second consumer of any parser. `describe()` is also live, not dead: it is defined at `lib.rs:938`, and `invalid_evidence_result()` calls it at `lib.rs:419` to render an `EvidenceError` into the `error` string of a `{"valid":false,"error":"…"}` payload. It carries no `#[allow(dead_code)]`, and nothing else in the crate does either.

So the open question worth deciding is not framing. It is: **when a message of any other type arrives, what is it called and what comes back.** That is a naming and dispatch question, and it is small.

## 2. Measured state at `0527ecf6`

| element | value | how measured |
|---|---|---|
| unique `message_type` in `08-bmcp-protocol/schemas/` | 22 | `check_protocol_index.py` → `PASS` |
| recognised anywhere in `crates/` | 3 | `git grep -l <TYPE> -- crates/` |
| public parsers in `bmcp-protocol` | 2 (`parse_and_validate`, `parse_storage_receipt`) | `grep -rn '^pub fn parse_'` |
| message types with no Rust recognition | 19 | enumerated in `GAP-15` §4 |
| MCP server tools | 2, both for `APPLIED_DELIVERY_EVIDENCE_RECORDED` | `tools_catalog()` |
| MCP methods implemented | 3 | `handle_request_body_with_deadline` |

Two parsers, one exported tool type. The parsers exist and have nowhere to go; the tools exist and serve one type. The binding is missing, not the parsing.

## 3. Decision

**H freezes exactly one additional MCP tool, `validate_bmcp_message`, whose arguments are `{"message": <object>}` and whose dispatch key is the `message_type` string carried inside that object. No per-type tool names are frozen. No digest tool is added for any type besides `APPLIED_DELIVERY_EVIDENCE_RECORDED`.**

### 3.1 Why one dispatch tool and not 19 named tools

Nineteen generated names would each need a deterministic derivation from a `message_type` that already varies in shape — `JF10_PREPARE_INTENT_REGISTERED` is SCREAMING_SNAKE, `Storage.PreparedParticipantReceipt` is dot-and-PascalCase. Any naming rule would be a second, invented namespace sitting beside the authoritative one, and the authoritative one is already in the message.

Dispatching on `message_type` uses the schema's own discriminator. It also fails closed in the right place: an unrecognised type is a *message* problem, not a *method* problem, and must not be reported as `-32601`.

### 3.2 Result envelope

| case | result |
|---|---|
| type parses and validates | `{"valid":true,"message_type":"<as received>"}` |
| type is known, body invalid | `isError: true`, `{"valid":false,"message_type":"<as received>","error":{...}}` |
| `message_type` absent or not a string | `isError: true`, `{"valid":false,"message_type":null,"error":{...}}` |
| `message_type` syntactically present but unknown | `isError: true`, `{"valid":false,"message_type":"<as received>","error":{...}}` |

No case returns `-32601`. The method exists; the message may not.

### 3.3 What this deliberately does not do

- **Does not extend `digest`.** `bmcp_protocol::digest::p0_digest` is defined for `AppliedDeliveryEvidence`. Extending it to 19 types would require a canonicalisation profile per type, and none exists. Inventing 19 canonicalisations to make a tool symmetrical is exactly the failure mode this repository keeps recording. Digest stays one type, and that asymmetry is recorded as open rather than papered over.
- **Does not touch framing, session or handshake.** Unchanged. This decision freezes no bytes on the wire; it freezes which tool answers a message.
- **Does not accept the C/H COutcomeRecord mapping.** `C-CON-017`/`C-CON-019` stay exactly as open as they are. `APPLIED_DELIVERY_EVIDENCE_RECORDED` keeps its existing two tools and its existing semantics.
- **Does not implement anything.** See §5.

## 4. Why deciding this does not violate the no-invention rule

`GAP-10` §1.5 says Agent Integration "cannot be implemented ahead of those without inventing contracts". That is a rule against implementing before deciding, not against deciding.

What makes this decision lawful is that it invents nothing: the tool surface, the method set, the parser call, the discriminator and the error shape are all already present in `bmcp-server` and in the schemas. The decision names an existing possibility and forbids the nineteen alternatives a reasonable implementer might otherwise pick — which is the actual function of an owner ruling.

The one thing it does choose is *one tool instead of nineteen*, and §3.1 gives the reason rather than the preference.

## 5. What remains, and who it belongs to

- **19 parsers.** Transcription against the 22 schemas. This decision removes the objection that they would have no consumer; it does not write them. Dispatchable to a delivery session with acceptance criteria, not by the owner.
- **Transport framing, session, handshake, ACK, replay.** Still `DEPENDENCY_NOT_FROZEN`. Unchanged by this decision, and still blocking RT-01..RT-09 for the parts that need them.
- **C/H COutcomeRecord mapping.** Still `NOT ACCEPTED`. Unchanged.
- **`describe()`.** Not dead code and not waiting on the 19 parsers: `invalid_evidence_result()` already calls it on the error path, rendering an `EvidenceError` into the `error` field of a `valid:false` payload. Landing the 19 parsers widens its coverage, not its first call site. This decision does not change its behaviour or its output format.

## 6. Acceptance criteria for whoever implements this

The decision is implemented when all of the following hold, and none is satisfied by this document:

1. `tools/list` returns a third tool named exactly `validate_bmcp_message`.
2. Each of the 19 currently unrecognised types, given a schema-valid instance, returns `{"valid":true,...}` from that tool.
3. An instance that fails its own schema returns `isError: true` with `valid:false`, and never `-32601` and never `Ok` with `valid:true`.
4. A message whose `message_type` is absent, non-string, or unknown returns `isError: true` with `valid:false`.
5. `validate_applied_delivery_evidence` and `digest_applied_delivery_evidence` behave byte-identically to `0527ecf6` — this decision may not change them.
6. `digest` is offered for no new type.
7. No `#[ignore]`, `todo!()` or `unimplemented!()` is introduced.

## 7. Independence

Written by the same session that measured §2. This is an owner-proxy decision, not an independent review, and the repository's prohibition on self-authorization means it does not by itself authorize merge of the implementation. Recorded here so a later reader can tell which kind of document this is.
