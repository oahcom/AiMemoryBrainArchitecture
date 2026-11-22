---
document_metadata:
  domain: domain-model
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Re-read from main @ 550bb864ed: validate_authorization_decision at admission.rs:1276 has the two-parameter signature, Issued carries AuthorizationDecisionData at lib.rs:566, and memory-compiler/tests holds one file. Each claim is a blob read, not a commit message."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes:
        - 14-ai-development/work-items/GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER.md
      supersession_reason: "The superseded version said three steps remained; #662 shipped two of them within the hour, leaving one. Keeping the old text would make the record misleading on read, which is the defect it was written to prevent."
    modification_note: "Rewritten to reflect #662. Same file path so the two versions do not both appear in the work-items index."

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-18 (continued) — one step left, and it is not the one that was blocked

**Status:** Open — one step remains · **Companion to:** `GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER.md`
**Measured at:** `main` @ `550bb864ed`
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. Why this document was rewritten

The first version of this document, merged as `#663` (`0fda02e2c8`), said three steps remained. Two of them shipped in the two hours that followed, in `#662` (`f98a45995d`). Leaving the document as it was would make it an instance of exactly what it was written to prevent: a record that is correct when written and misleading when read.

So this is the same document with the completed work marked done and one step left. The one step left is the only one that was ever blocked, and it is still blocked for the same reason.

## 2. What has shipped, in the order it shipped

| commit | what it did | which of the five steps |
|---|---|---|
| `001248d452` | `AuthorizationDecisionRef` became `Absent \| PendingI \| Issued`; `dm2_06` lost its `#[ignore]` | 3 (domain type), 5 (validate rejects only `Absent`) |
| `f98a45995d` (`#662`) | `authorization_decisions` + `i_attestations` tables, `issue_authorization_decision`, `validate_authorization_decision`, `IssuerId` moved to crate root | 1 (table), 2 (writer + validator) |

Four of five steps are done. What remains is step 4: the assertion that a present-but-unbacked reference is refused by the authority.

## 3. Verified, not assumed

Read from `main` at `550bb864ed`, not from commit messages.

**The table and the validator exist** (`admission.rs:1276`):

```rust
pub fn validate_authorization_decision(
    &self,
    reference: &AuthorizationDecisionRef,
    expected_subject_digest: &OpaqueId,
) -> Result<bool, AuthorizationDecisionValidationError> {
    let data = reference
        .data()
        .ok_or(AuthorizationDecisionValidationError::PendingReference)?;
```

Two parameters, no cursor. That is `§4.1` exactly, and it is the one place I flagged in the previous version where a mechanical copy of `validate_canonical_commit` would have gone wrong. It did not go wrong.

**The type carries content now** (`lib.rs:566`):

```rust
Issued(AuthorizationDecisionData),
```

This is a change from what the earlier version of this document specified (`Issued(OpaqueId)`), and it is an improvement I did not ask for. §4.2 requires per-field comparison between reference and stored row; a bare id gives that comparison nothing to compare. `#662`'s message states the reason directly: "so §4.2's per-field comparison has an input."

**The old constructor was kept and made honest** (`lib.rs:585`):

```rust
pub fn issued(decision_id: OpaqueId) -> Self {
    Self::Issued(AuthorizationDecisionData {
        decision_id,
        issuer: IssuerId(OpaqueId::new("i-owner-proxy/dev-baseline-v1")...),
        subject_digest: OpaqueId::new("0".repeat(64))...,
        issued_at: "1970-01-01T00:00:00Z".to_owned(),
        decision_kind: AuthorizationDecisionKind::Conditional,
    })
}
```

The doc comment says what the sentinels are for: "deliberately NOT valid issued data — `validate_authorization_decision` will not match it against any row, and no row can be written from it."

That is the right shape. `dm2_06` calls `issued(id("ad-1"))` and asserts presence passes; it does not need real data to assert presence, and the sentinel guarantees the test cannot accidentally become an authority test that passes for the wrong reason. A constructor that silently filled plausible-looking fields would have made `dm2_06` assertion 3 meaningless.

## 4. The one step left

`crates/memory-compiler/tests/` contains exactly one file: `event_store_digest_compat.rs`. There is no authorization test. `dm2_06` proves presence and cannot prove authority, because `memory-domain` has one dependency and cannot see the store.

`#662`'s message says this explicitly: "the un-ignore belongs to the follow-up that can call it." That follow-up is this step.

### The assertion

New file `crates/memory-compiler/tests/authorization_authority.rs`:

```rust
// A reference that claims issuance but has no durable row must be refused by the
// authority, and the refusal must be Err, not Ok(false).
let reference = AuthorizationDecisionRef::issued(id("ad-never-issued"));
let outcome = store.validate_authorization_decision(&reference, &subject_digest);
assert!(
    matches!(outcome, Err(AuthorizationDecisionValidationError::RecordMissing)),
    "an unbacked issued reference must be an authority error, got {outcome:?}"
);
```

Three properties, each traceable to a defect that actually happened:

1. **`Err`, not `Ok(false)`.** `#623` asserted `Err(EmptyRequiredField)` — the wrong error from the wrong layer, because it drove the gate through `FactRevision::validate()` where the only reachable failure was a field check. §4.2: "a missing row is always `Err`".
2. **`RecordMissing` specifically.** An assertion accepting any `Err` passes when the validator fails earlier — at `PendingReference`, for instance — and then the test is green and measures nothing.
3. **In `memory-compiler`.** `#623` put it in `memory-domain` and rewrote the fixtures; the store was never reachable there. `#634` did it in the right crate but lost `mod canonical_commit;`, `pub use canonical_commit::*;`, the content-bearing `CanonicalCommitRef`, and `dm2_15` to a rebase.

### The other two outcomes, which the same file should cover

§4.2 has three outcomes and only `Err` is above. The other two need a real row, so they need `issue_authorization_decision`:

- `Ok(true)` — issue a decision, then validate the reference it returned against the same subject digest.
- `Ok(false)` — issue, then validate against a *different* subject digest. The row is readable and every reference field matches it, so this must be `Ok(false)` and not `Err`.

A test file with only the `Err` case would leave `Ok(false)` unreachable by any test, and `Ok(false)` is the one outcome where a bug makes a wrong thing look like a valid answer.

## 5. What not to do

- **Do not remove `dm2_06`'s presence assertions.** They assert something the authority test cannot: that `Absent` blocks at construction and `PendingI` does not. Both tests are needed.
- **Do not make `FactRevision::validate()` reject `PendingI`.** `OWNER-RULING-025` exists because that was attempted. It would fail every `initial(.., pending_i(), ..)` at construction.
- **Do not add a cursor parameter** to `validate_authorization_decision`. It has two, matching §4.1, and it is correct.
- **Do not fold `Absent` and `PendingI` into one arm returning `Ok(false)`.** `#662` maps both to `PendingReference` via `data()`; keep it.
- **Do not reuse `DEV_BASELINE_ISSUER` for decisions.** `#662` introduced a separate issuer and a separate primary-key namespace (`i_attestations`). That separation is the point.

## 6. Definition of done

- [ ] `crates/memory-compiler/tests/authorization_authority.rs` exists.
- [ ] `Err(RecordMissing)` for an unbacked `issued()` reference.
- [ ] `Ok(true)` after a real issue-then-validate round trip.
- [ ] `Ok(false)` when the expected subject digest differs from the stored one.
- [ ] `dm2_06` unchanged.
- [ ] `cargo test --workspace --all-targets` reports `ignored = 0`.

## 7. Why this is a work order and not a patch

I do not write code on this repository. That constraint has not moved, and it is why this document gives the exact assertion, the exact file path, and the three failure modes instead of the diff.

The reason to prefer it over silence is measurable in this repository's own history: `#623` and `#634` both re-derived this step, both got it wrong in different directions, and one lost four unrelated items to a rebase. A written target is cheaper than a third derivation.
