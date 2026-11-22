---
document_metadata:
  domain: protocol
  role: review-report

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Counted from the 22 message-type rows of 08-bmcp-protocol/protocol-index.md at main @ 0fda02e2c8, and from the four cited directories on disk. The two Rust entry points are read from crates/bmcp-protocol/src/lib.rs:1556 and :1566. Every count is reproducible by the command in section 3."
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

# GAP-22 — BMCP: 22 message types, 2 validators, and the number nobody had counted

**Status:** Open · **Area:** `08-bmcp-protocol/`, `crates/bmcp-protocol/`
**Measured at:** `main` @ `0fda02e2c8`, tarball unpacked locally
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. What this measures, and what it does not

`08-bmcp-protocol/protocol-index.md` is an honest document. It counts 22 unique `message_type` constraints across 32 schemas and it labels each one's status without inflating any of them. I am not correcting it.

What it does not do — because it is an index, not a gap analysis — is answer the question a reader actually has: **how much of this protocol can reject a malformed message today?** That is the question this document answers, with the counts the index already contains but does not total.

Two measurements, deliberately kept apart:

| question | answer | where |
|---|---|---|
| How many message types have a schema? | 22 of 22 | `protocol-index.md`, verified below |
| How many can reject a malformed message? | **2 of 22** have a dedicated validator; **13 of 22** have no validator at all | this document §3 |

## 2. The index is accurate — verified, not assumed

I checked the four directories the index cites, because a document that describes artifacts is only as good as their presence:

```
08-bmcp-protocol/schemas/            32 *.json
08-bmcp-protocol/validators/          6 *.py
08-bmcp-protocol/tests/conformance/   applied_delivery_evidence, provider_outcome, recovery_cutoff
08-bmcp-protocol/runtime_reference/   present
```

All four exist. The index's own header states its audited base as `2f8c00d835b04c75e71f1a6ba33e1e465445dec0`, which is older than the tree I measured; the counts still hold, so nothing in between invalidated them.

The index also does the thing that makes it trustworthy: it distinguishes `IMPLEMENTED (artifact presence)` from conformance, and says so in the status cell — "Not a production-conformance claim." An index that overclaimed here would have made this document unnecessary and wrong.

## 3. The distribution

From the 22 message-type rows of `protocol-index.md`, grouped by what the status column actually says:

| status | count | message types |
|---|---:|---|
| `IMPLEMENTED (artifact presence)` | 2 | `APPLIED_DELIVERY_EVIDENCE_RECORDED`, `RECOVERY_JOIN_PROOF` |
| `PARTIAL` | 1 | `C_PROVIDER_OUTCOME_RECORDED` |
| `SCHEMA + REFERENCE TESTS PRESENT` | 7 | `COC_RECOVERY_CUTOFF_BATCH`, `JF10_I_TERMINAL_DECISION_OBSERVED`, `OWNER_LOCAL_GATE_RELEASE`, `OWNER_LOCAL_PENDING_GATE`, `PARTICIPANT_SET_RECONCILIATION`, `RECOVERY_CUTOFF_BATCH`, `RECOVERY_EPOCH_COMPLETED` |
| `SCHEMA + LIMITED TEST REFERENCE` | 4 | `JF10_BRIDGE_RECONCILIATION_RECORDED`, `JF10_PREPARED_PARTICIPANT_REGISTERED`, `JF10_PREPARE_INTENT_REGISTERED`, `JF10_STORAGE_PARTICIPANT_RESOLVED` |
| `SCHEMA PRESENT` — no conformance verdict | 7 | `I_JF10_TERMINAL_DECISION_OBSERVED`, `OWNER_ADMISSION_ENTRY`, `OWNER_ADMISSION_SNAPSHOT_ATTESTATION`, `OWNER_GATE_RELEASE_ATTESTATION`, `STORAGE_JF10_PARTICIPANT_RESOLVED`, `Storage.PreparedParticipantReceipt`, `Storage.StorageResolutionProof` |
| `SCHEMA PRESENT` — no test located | 1 | `COC_PARTICIPANT_MANIFEST` |

Two things about that table are worth stating plainly:

**Seven message types have a schema and nothing else.** No validator, no test, no verdict. They are in the protocol, they are in the index, and nothing in this repository can say whether a message claiming one of those types is well-formed.

**"Reference tests present" is not validation.** Six validators exist in `08-bmcp-protocol/validators/`, and only two of them are message-type dispatchers:

```
applied_delivery_evidence_validator.py   -> no message_type constant (structural validator)
envelope_auth_validator.py               -> C_PROVIDER_OUTCOME_RECORDED
gateway_attestation_validator.py         -> C_PROVIDER_OUTCOME_RECORDED
provider_outcome_validator.py            -> C_PROVIDER_OUTCOME_RECORDED
provider_outcome_validator_1_2_15.py     -> C_PROVIDER_OUTCOME_RECORDED
recovery_join_validator.py               -> no message_type constant (structural validator)
```

Four of the six all serve one message type (`C_PROVIDER_OUTCOME_RECORDED`), which is the one the index marks `PARTIAL`. That is not a criticism of those four — the C-owned authority checks are external by design — but it means the validator count is not a coverage count, and reading `6 validators` as `6 message types covered` would be wrong by a factor of three.

## 4. The Rust side: 2 parsers for 22 types

`crates/bmcp-protocol/src/lib.rs` is 2,366 lines. It contains exactly two public parse entry points:

```rust
:1556   pub fn parse_and_validate(..)      -> APPLIED_DELIVERY_EVIDENCE_RECORDED
:1566   pub fn parse_storage_receipt(..)   -> Storage.PreparedParticipantReceipt
```

Both are single-const parsers: each rejects any `message_type` that is not its one literal. There is no dispatch table, so a third message type cannot be routed without writing a third function, and the caller must already know which type it holds before calling — which is the thing a protocol layer exists to avoid.

This is the 1-of-22 gap that has been reported verbally more than once. The measured form is: **22 declared message types, 2 Rust parsers, 0 routing layer.**

## 5. Why "22 parsers" is the wrong work item

The obvious reading of §4 is "write 20 more parsers." That is 20 near-identical functions, each with its own field list, and it is not what the gap is.

The gap is that **there is no wire-to-parser router**. A router is one function:

```rust
match envelope.message_type() {
    "APPLIED_DELIVERY_EVIDENCE_RECORDED" => parse_and_validate(input),
    "Storage.PreparedParticipantReceipt" => parse_storage_receipt(input),
    other => Err(UnknownMessageType(other)),
}
```

Writing that router first, with two arms, makes the shape of the remaining work visible and makes each subsequent parser a one-line addition. Writing 20 parsers first produces 20 functions with no caller and no shared envelope contract, and the second one written will invent a slightly different envelope check from the first.

The envelope contract is the second half of this. Eleven of the unified-family types share a `commonEnvelope` with 25 required fields. If each parser re-implements that check, the repository gets eleven chances to disagree with itself about what a valid envelope is. One shared envelope validator plus a type-specific payload validator is the shape that cannot drift.

## 6. Ordering, if this is to be worked

1. **The router, with the two existing parsers.** No new parsing. This proves the dispatch shape against code that already works, and it makes the `UnknownMessageType` case explicit instead of "the caller picked the wrong function."
2. **The shared envelope validator**, extracted from whichever of the two current parsers has the stricter check. Eleven types depend on it; getting it right once is the only way they agree.
3. **The seven `SCHEMA PRESENT` types**, in whatever order their consumers need. Each is one router arm and one payload validator. These are the highest value because they currently have no verdict at all.
4. **The four `SCHEMA + LIMITED TEST REFERENCE` types.** Their tests cover the message family, not the message; the gap is narrower than it looks and should not be worked before step 3.
5. **The seven `SCHEMA + REFERENCE TESTS PRESENT` types.** `runtime_reference/` code is explicitly not an authority source per the index. Working these before the seven above would produce validation against reference semantics, which the index already says is not conformance.

## 7. What this document does not claim

- **It does not claim the 22 are all needed.** Some may be retired. The index does not say, and neither does this document.
- **It does not claim the Python validators are the production path.** They validate artifacts; the Rust crate is the product. The two counts are separate on purpose.
- **It does not re-audit the schemas.** I counted what the index counts and grouped it. If the index is wrong about one row, this table is wrong about one row.
- **It does not say the protocol is 9% done.** Two of 22 is the count of types with a dedicated validator. Coverage of the *traffic* those types carry is a different number and nothing in the repository measures it.

## 8. The one-line summary

`protocol-index.md` says, correctly, that 22 message types exist. It does not say — and nobody had totalled — that 7 of them have a schema and no verdict, 11 more have tests that do not validate, and the Rust crate parses 2 of them with no router between the wire and the parser.
