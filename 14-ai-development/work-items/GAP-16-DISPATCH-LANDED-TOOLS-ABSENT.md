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
      last_verification_note: "Every figure in §2 was measured at main 021f5a3f in this session, and each is given with the command that produced it. The three figures GAP-15 recorded at fb37a44b are reproduced and their expiry is explained in §3 rather than quietly overwritten."
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

# GAP-16 — the dispatch landed; the tool that would consume it did not

**Status:** open · **Severity:** Tier 2 (blocks no gate; blocks every consumer) · **Owner:** H (binding, already ruled), delivery session (implementation)
**Measured at:** `021f5a3f` · **Supersedes the BMCP figures in:** `GAP-15` §4 · **Implements:** `OWNER-DECISION-BMCP-MCP-DISPATCH-001`

---

## 1. Why this file exists

`GAP-15` recorded, at `fb37a44b`, that 19 of the 22 BMCP message types had no Rust recognition, and that 2 public parsers existed. Those figures were correct at that commit. They are no longer correct, and the reason is not a mistake in the measurement — it is that `main` is not a line.

`fb37a44b` and `6007782b` are both ancestors of `main` and neither is an ancestor of the other; their merge base is `b47bd97c`. Measuring at `fb37a44b` therefore cannot see `6007782b`, and a reader who takes a stale figure for a current one will dispatch work that is already merged. That is the failure `GAP-15` was written to prevent, so this file prevents it again rather than letting the correction live in a PR description.

## 2. Measured state at `021f5a3f`

| element | value | command |
|---|---|---|
| unique `message_type` in `08-bmcp-protocol/schemas/` | 22 | `python 08-bmcp-protocol/scripts/check_protocol_index.py` → `PASS` |
| `parse_dispatch` exists | yes | `grep -c 'pub fn parse_dispatch' crates/bmcp-protocol/src/lib.rs` → `1` |
| match arms inside `parse_dispatch` | 22 | one per type, enumerated below |
| arms backed by complete semantic validation | 1 | `APPLIED_DELIVERY_EVIDENCE_RECORDED` |
| arms backed by a message-specific structural parser | 1 | `Storage.PreparedParticipantReceipt` |
| arms that recognise only the root discriminator | **20** | the rest, all wrapped in `StructurallyUnvalidatedMessage` |
| MCP tools exposed | 2 | `validate_applied_delivery_evidence`, `digest_applied_delivery_evidence` |
| `validate_bmcp_message` in `bmcp-server` | **absent** | `grep -c` → `0` |
| call sites of `parse_dispatch` outside its own tests | **0** | see §4 |

So the shape has changed in a way that matters. The parsers are no longer missing — the *dispatch* is present and covers all 22 types. What is missing is the **tool** that would let a caller reach it, and the **validation** that 20 of those 22 arms explicitly do not perform.

## 3. What the 20 arms do and do not claim

`DispatchValidationState` names three mutually exclusive states, and the code is honest about which arm is in which:

| state | meaning | arms |
|---|---|---|
| `SemanticallyValidated` | passed the complete message-specific semantic validator | 1 |
| `StructurallyParsed` | passed a message-specific structural parser; full semantics not established | 1 |
| `RootDiscriminatorOnly` | only `message_type` was recognised | 20 |

`StructurallyUnvalidatedMessage` carries `message_type: &'static str` and `value: serde_json::Value` — the complete root object, deliberately preserved without applying any field allowlist. The doc comment on the struct says so, and the doc comment on `parse_dispatch` says so twice.

This is the correct design for an unfrozen wire mapping: it makes the un-validated state **representable** instead of pretending. But it also means that "22 types dispatch" must never be read as "22 types validate". A tool that returned `{"valid":true}` for all 22 would be a lie about 20 of them, and that is exactly what `OWNER-DECISION-BMCP-MCP-DISPATCH-001` §3.2 forbids.

## 4. The consumer gap, measured

`parse_dispatch` is `pub`. Nothing in the workspace calls it. `bmcp-server` exposes two tools, both hardwired to `APPLIED_DELIVERY_EVIDENCE_RECORDED` via `parse_and_validate`, and reaches no dispatch path at all.

This is the same shape `GAP-15` §4 described — a parser with no consumer — one layer up. The owner ruling removed the *contract* objection (what the tool is called, what it returns, what it must never return). It did not remove the *implementation* gap, and §6 of that ruling says so explicitly.

## 5. What is genuinely left

| item | blocked by | who can close it |
|---|---|---|
| `validate_bmcp_message` tool, dispatching on `message_type` | nothing; the binding is ruled | a delivery session, against §6 of the ruling |
| schema validation for the 20 `RootDiscriminatorOnly` arms | a JSON Schema engine, absent from `bmcp-protocol/Cargo.toml` | a delivery session, but see §6 |
| transport framing, session, handshake, ACK, replay | `DEPENDENCY_NOT_FROZEN` | H, and only after C/H mapping is accepted |
| C/H `COutcomeRecord` mapping (`C-CON-017`, `C-CON-019`) | `NOT ACCEPTED` | C and H jointly; not a single-owner decision |
| `Published` disposition | external issuers (COC quorum, Storage signature, I terminal) | nobody in this repository; see `D-OWNER-DECISION-PARTICIPANT-ADMISSION-001` and `D-OWNER-DECISION-PROTECTED-VISIBILITY-001` |

## 6. Why the 20 arms should not be schema-validated yet

`bmcp-protocol/Cargo.toml` carries no `jsonschema` dependency, and the reason is not an oversight. Adding one would make each of the 20 arms' conformance criterion *the schema file's current text* — the very text `TECH-REALITY-001-C/README.md:70` records as not frozen. A parser validated against an unfrozen schema is a bet, and it is a bet that looks like progress because the tests pass.

The one arm that *is* fully validated, `APPLIED_DELIVERY_EVIDENCE_RECORDED`, is validated by hand-written Rust (`validate::from_strict_value`), not by a schema engine. That is the pattern the repository has chosen for the one message whose contract is settled.

So the honest sequence is: ship the dispatch tool (§6 of the ruling), keep the 20 arms labelled `RootDiscriminatorOnly`, and let the freeze decision — not an implementation session — decide when the other 19 become schema-validated.

## 7. Acceptance criteria for the dispatch tool

Unchanged from `OWNER-DECISION-BMCP-MCP-DISPATCH-001` §6, restated here so this file can be closed without cross-reading:

1. `tools/list` returns a third tool named exactly `validate_bmcp_message`.
2. Every type whose arm is `SemanticallyValidated` or `StructurallyParsed` returns `{"valid":true,...}` for a conforming instance.
3. Every type whose arm is `RootDiscriminatorOnly` returns `{"valid":true,"validation_state":"root_discriminator_only",...}` — **not** an unqualified `true`, because the tool must not claim more than the arm established.
4. A message whose `message_type` is absent, non-string, or unknown returns `isError: true`, `valid:false`, and never `-32601`.
5. The two existing tools behave byte-identically to `021f5a3f`.
6. `digest` is offered for no new type.
7. No `#[ignore]`, `todo!()` or `unimplemented!()` is introduced.

Criterion 3 is the one this file adds to the ruling, and it is the one that matters: it makes the tool report the validation state it actually reached, instead of flattening three states into a boolean. The ruling's §3.2 envelope said `{"valid":true,"message_type":"<as received>"}` for the success case, written before `DispatchValidationState` existed in its current form; the three-state enum is the better carrier and the ruling's intent is preserved by reporting it.
