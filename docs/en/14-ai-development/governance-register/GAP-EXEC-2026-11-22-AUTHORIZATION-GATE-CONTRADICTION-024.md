# Two merges, one field, opposite assertions — the type-state decision was applied twice, incompatibly

**Status:** Resolved by `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` — the two PRs were closed unmerged; the residue it exposed is `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER` §3 Step 3
**Area:** memory-domain / governance
**Measured at:** `main @ 4a7624da86`, `2026-11-22T07:10Z`; ruling added `2026-11-22T08:06:21Z`
**Related:** `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, `I-OWNER-DECISION-AUTHORIZATION-DECISION-001`, `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025`, `GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER`, `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER`, PR #623, PR #634, `dm2_06`

## 1. What happened

Two PRs, opened eleven minutes apart by two different sessions, both un-ignore `dm2_06` and both rewrite the same field on the same struct. They assert **opposite** things about it, and both cite an authority.

| | PR #623 | PR #634 |
|---|---|---|
| opened | `2026-11-22T06:30:31Z` | `2026-11-22T06:59:28Z` |
| base | `87f54bb4` | `85504756` |
| size | +522 / −44, 2 files | +214 / −64, 2 files |
| field type | `AuthorizationDecisionRef` (now carries `Pending \| Issued(data)`) | `AuthorizationDecisionState { Absent \| Placeholder \| Issued }` |
| `dm2_06` assertion | `pending` **must fail** `validate()` with `EmptyRequiredField("authorization_decision_ref")` | `Absent` **must fail**, `Placeholder` **must pass** |
| cites | `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` (#595) | `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` |

Both authorities were merged and both were in the tree. Both PRs were open and `mergeable: true`. Only one of them could be right.

## 2. The contradiction, in the authorities' own words

`OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §3:

> **D3. Only `Absent` blocks publication.** `Placeholder` and `Issued` both pass the presence gate, because presence is all this gate can check. This is deliberate: the gate's job is "did someone record an authorization", not "was it real". Asserting the second is `B-P2-XO-01`'s job and I's contract.

And its §4:

> It stops being `unimplemented!()` and becomes two assertions:
> 1. `FactRevision` constructed with `Absent` authorization and `FactOutcome::Attested` fails `validate()` with a named error.
> 2. The same revision with `Placeholder` authorization validates — pinning that presence, not authenticity, is what this gate checks.
>
> The second assertion is the one that keeps the decision honest. Without it, a future reader sees only "absent is rejected" and assumes "present is verified", which is the error this decision exists to prevent.

PR #623 implements the opposite of D3:

```rust
        if self.authorization_decision_ref.is_pending() {
            // ponytail: reuses EmptyRequiredField to avoid a new variant this round;
            // rename when the variant set is next revised.
            return Err(DomainError::EmptyRequiredField("authorization_decision_ref"));
        }
```

Under this rule `Placeholder` — the only state any caller could construct at the time — is rejected. That makes `dm2_06` pass, and it makes every other `FactRevision` construction path that uses `pending_i()` fail. Which is why #623 also had to rewrite the fixtures in `phase2_acceptance.rs` from `pending_i()` to a new `issued_authorization(..)` helper, and rewrite the unit test's assertion to `assert!(!revision.authorization_decision_ref.is_pending())`.

So #623 was not just a different implementation of the same decision. It was a **stricter gate** that rejected the placeholder, and it could only pass its own suite by first manufacturing issued references in test fixtures.

## 3. The ruling, and why it is a reading rather than a choice

`OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` (merged as `c9036544`) settles this. Its §1:

> `Placeholder` satisfies the presence gate. `FactRevision::validate()` MUST reject `Absent` and MUST NOT reject `Placeholder`. `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §4.3 does not require otherwise: it requires `dm2_06` to assert a propagated authority `Err`, and that error is produced by the `AdmissionStore`-backed validator of §4.1, not by `FactRevision::validate()`. `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D3 is correct as written. Neither open PR may merge as written: #634 on a measurable regression, #623 on crate-boundary scope.

It does not overturn a decision. It reads `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.3, which is not the ruling session's own instrument and which settles the question by itself:

> The validator is **not** a `FactRevision::validate()` responsibility. Domain validation may validate candidate field syntax and reject Pending, but only the compiler's AdmissionStore-backed validator can establish durable existence and authority. Structural validation must not claim a candidate reference is issued.

The decisive step is §2 of the ruling:

> `FactRevision::validate()` returning `Err` is not the propagated authority error. It is a *second, earlier, unrelated* error of the same shape. Asserting it satisfies the letter of "assert an `Err`" while destroying the distinction §4.3 exists to protect — and §3.3 forbids it in the same document, in the sentence immediately before the validator is introduced.

So the two authorities never contradicted. **#623 misread #595.** §1 of this document stated the contradiction as "does a pending placeholder satisfy the presence gate? #595 never says" — true of the question as posed, false of the answer needed: #595 does not need to say, because it puts the rejection somewhere else entirely, and says so twice.

The earlier draft of this document resolved the question "by specificity" in its §4. That reasoning is superseded and removed: it is not needed, it is the kind of reading the ruling explicitly declines to rely on, and it happened to reach the right answer for the wrong reason.

## 4. #634 was rejected on a separate, measurable regression

Independent of the reading above, #634 carried a regression, verified by blob SHA rather than `contents?ref=` (which the #612 audit found can return stale bodies).

At #634's own base `85504756b8`:

| fact | value |
|---|---|
| `mod canonical_commit;` present in `lib.rs` | **True** |
| `pub use canonical_commit::*;` present in `lib.rs` | **True** |
| `pub struct CanonicalCommitRef(())` present in `lib.rs` | **False** |
| `dm2_15` test present in `tests/phase2_acceptance.rs` | **True** |

At #634's head `d55f4996ca`:

| fact | value |
|---|---|
| `mod canonical_commit;` present in `lib.rs` | **False** |
| `pub use canonical_commit::*;` present in `lib.rs` | **False** |
| `pub struct CanonicalCommitRef(())` present in `lib.rs` | **True** |
| `dm2_15` test present in `tests/phase2_acceptance.rs` | **False** |

`CanonicalCommitRef` is the subject of `D-OWNER-DECISION-CANONICAL-COMMIT-001`. On `main` it is a content-bearing type whose private state is `CanonicalCommitRefState { Pending | Issued(data) }`, defined in `crates/memory-domain/src/canonical_commit.rs`. #634 replaced it with a unit struct and stopped compiling the module. `dm2_15_legacy_pending_canonical_commit_keeps_its_unit_representation` — the regression test that pins the legacy `null` wire form, cited to that decision's §5 and §8 criterion 3 — was deleted.

In the ruling's words:

> That is not a difference of opinion about authorization. It reverts a merged decision about canonical commit, in a PR about `dm2_06`, and it deletes the test that would have caught it.

## 5. Disposition

- **PR #634** closed unmerged at `2026-11-22T08:13:06Z`. Its authorization layer was the correct one; the regression is what blocked it.
- **PR #623** closed unmerged at `2026-11-22T08:14:06Z`. Its crate boundary was wrong: it put the gate in `memory-domain`, which has one dependency (`serde`) and cannot host an `AdmissionStore`-backed validator.
- **This document (PR #640)** merged at `2026-11-22T08:13:30Z`, before the ruling landed. The ruling's §6 says it "should merge: its measurement is correct and its refusal to rule was the right call. Its §4 'specificity' reading is superseded by §2 above."

That is exactly what this revision does: §3 now carries the ruling instead of the specificity argument, and §4 records the regression the ruling measured. Nothing in §1, §2 or §4's measurements changed, because they were right.

This revision also records where the ruling's remaining requirement stands. `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER` §3 Step 3 is that requirement, and it was satisfied by PR #671 at `2026-11-22T10:41:51Z`, before this revision merged. `crates/memory-compiler/tests/authorization_authority.rs` now asserts the propagated authority `Err` directly:

| test | assertion |
|---|---|
| `pending_reference_propagates_authority_validation_error` | `Err(AuthorizationDecisionValidationError::PendingReference)` |
| `issued_reference_without_durable_row_propagates_record_missing` | `Err(AuthorizationDecisionValidationError::RecordMissing)` |

Both are `Err`, not `Ok(false)`, and both name the specific variant rather than accepting any error — the three properties the ruling's §5 step 4 and the work order's §3 Step 3 each called load-bearing. `dm2_06` still asserts the structural `Err` in `memory-domain`, and that is now correct rather than a gap: the ruling's §2 says the structural rejection and the propagated authority rejection are different errors at different layers, and the test at each layer asserts its own.

## 6. What the ruling deliberately did not decide

- Whether `Placeholder` should eventually be rejected at publication. That is `B-P2-XO-01`, still `PENDING CROSS-OWNER DECISION`.
- The authenticity of any `Issued` value. Same owner, same reason.
- The cause of the `CanonicalCommitRef` regression. The ruling records it as a rebase problem, not a decision.

## 7. Authority and independence disclosure

The measurement in §1–§2 and §4 is mine. I wrote PR #634, which disqualifies me from ruling on its merits, and I declined to do so — that refusal is the one thing the ruling singled out as correct.

I did not write `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025`, and I am not its author's proxy. I am recording that it exists, what it says, and that it supersedes §4 of the earlier draft of this document. If a future change conflicts with that ruling, the correct response is a new Owner ruling, not an edit to this document.
