---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count and exit code in this prompt was measured in this session on branch req05/752-attestor rebased onto origin/main 3a859ac0. The mutation outputs are verbatim from the commands shown."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-094 — Close the unvalidated AttestorData deserialization boundary

## The gap, measured

`crates/memory-domain/src/authorization.rs` declares a public data carrier:

```rust
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
pub struct AttestorData {
    pub attestation_id: OpaqueId,
    pub issuer: IssuerId,
    pub subject_digest: OpaqueId,
    pub issued_at: String,
}
```

The `Deserialize` was derived. `validate_attestor_data` is a separate private
function that only `AttestorRef::from_issued_data` called. So
`serde_json::from_str::<AttestorData>(...)` produced a value with **any**
issuer — `someone-else`, the decision issuer, anything `IssuerId::new` accepts
— and nothing on the value said it was unvalidated. `AttestorRef` already had a
hand-written `Deserialize` (line 440) that routes through its visitor and calls
`from_issued_data`; the bare struct was the hole that bypassed it.

Measured before the change, at `origin/main` `3a859ac0` (the commit this
branch was measured on; it was rebased onto `ba5b26b3` before the pull request
opened, and the pre-fix decode is unchanged between the two because neither
touches `authorization.rs`):

```
serde_json::from_str::<AttestorData>(r#"{"attestation_id":"x","issuer":"someone-else",...}"#)
  -> Ok(AttestorData { issuer: IssuerId(OpaqueId("someone-else")), .. })
```

`AttestorData` is used in exactly two places outside its own module:
`AttestorRefState::Issued(AttestorData)` in the same file, and
`crates/memory-compiler/src/admission.rs` (import at the `use memory_domain`
block, construction at `issue_attestation`). The compiler constructs it by
**struct literal** and immediately hands it to `AttestorRef::from_issued_data`,
which validates. It never deserializes an `AttestorData`:

```
grep -rn "from_str::<AttestorData|from_slice::<AttestorData|from_value::<AttestorData" crates/
  (no matches)
```

## The two options, and the one chosen

The issue offered two:

1. Make `AttestorData` deserialization invoke the domain validator.
2. Make the unvalidated nature explicit and prevent callers treating bare
   deserialized data as validated.

**Option 1 was chosen.** The deciding measurement is that the only non-test
construction site (`admission.rs::issue_attestation`) builds the struct by
literal and validates through `from_issued_data`, and nothing in the workspace
deserializes an `AttestorData`. Option 1 therefore needs **no** parallel
unvalidated constructor and **no** new public API: the struct literal stays as
the unvalidated construction path (documented as such), and `Deserialize`
becomes the validated one.

Option 2 was rejected because the only way to make "unvalidated" a type-system
fact is a second newtype or a private field, which forces either a `pub`
accessor that reconstructs the hole or a parallel type threaded through
`AttestorRefState` and the compiler — the same hole with more code. The brief's
own test is exactly this: if option 1 forced a `pub` unvalidated back door it
would lose; it did not.

Consequence accepted and stated: the existing unit test
`attestor_data_rejects_empty_attestation_id` used
`serde_json::from_str::<OpaqueId>("\"\"")` to smuggle an empty id past the
derived `OpaqueId` deserializer so it could reach `validate_attestor_data`.
That path still works — it decodes an `OpaqueId`, not an `AttestorData` — so the
test is unchanged and still reachable. No test was deleted or made unreachable.

## What the change is

`AttestorData` loses its derived `Deserialize` and gains a hand-written one that
decodes through the existing `AttestorIssuedWire` helper (the same one
`AttestorRefVisitor` uses, so the wire form is identical) and calls
`validate_attestor_data` before returning. `Serialize` is untouched, so the
emitted flat four-field object is byte-identical. `AttestorRef`'s own
`Deserialize` and both of its wire forms (`null` → pending, flat object →
issued) are untouched.

The rule is enforced by the deserializer, not a doc comment: there is no way to
obtain an `AttestorData` from bytes that fails `validate_attestor_data`.

## Acceptance criteria

- AC1: `serde_json::from_str::<AttestorData>` with `issuer: "someone-else"`
  returns `Err` whose text is `invalid attestor data: InvalidCanonicalCommitField("issuer")`.
- AC2: the same with `attestation_id: ""` returns `Err` whose text is
  `invalid attestor data: EmptyId`.
- AC3: a valid `AttestorData` serializes to the flat four-field object and
  deserializes back to an equal value.
- AC4: `AttestorRef` still round-trips `null` → pending and flat object → issued,
  and a flat object with a bad issuer still fails to decode.
- AC5: removing the guard (turning the `validate_attestor_data` call into a
  no-op, or restoring the derived `Deserialize`) makes exactly AC1's and AC2's
  tests fail with an `assert_eq!` panic carrying the expected/actual pair, and
  no other test fails.

## Measured results

`cargo test --offline -p memory-domain`: 93 + 22 + 3 passed, 0 failed.

Mutation A — `validate_attestor_data(&data)` replaced with
`let _ = validate_attestor_data(&data);`:

```
assertion `left == right` failed
  left: Ok(AttestorData { attestation_id: OpaqueId("attestation-domain-test"), issuer: IssuerId(OpaqueId("someone-else")), ... })
 right: Err("invalid attestor data: InvalidCanonicalCommitField(\"issuer\")")
```

Mutation B — the hand-written `impl Deserialize` deleted and `serde::Deserialize`
restored to the derive: the same two tests fail with the same pair. Both are
recorded verbatim in `session-evidence-752.md`.
