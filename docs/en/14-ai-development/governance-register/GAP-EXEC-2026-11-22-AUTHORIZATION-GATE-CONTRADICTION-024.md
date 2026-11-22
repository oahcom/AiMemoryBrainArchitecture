# Two merges, one field, opposite assertions — the type-state decision was applied twice, incompatibly

**Status:** Open — needs an Owner ruling, not a patch
**Area:** memory-domain / governance
**Measured at:** `main @ 4a7624da86`, `2026-11-22T07:10Z`
**Related:** `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, `I-OWNER-DECISION-AUTHORIZATION-DECISION-001`, PR #623, PR #634, `dm2_06`

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

Both authorities are merged. Both are in the tree. Both PRs are open and `mergeable: true`. Only one of them can be right, and the two decisions do not say the same thing.

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

Under this rule `Placeholder` — the only state any caller can construct today — is rejected. That makes `dm2_06` pass, and it makes every other `FactRevision` construction path that uses `pending_i()` fail. Which is why #623 also had to rewrite the fixtures in `phase2_acceptance.rs` from `pending_i()` to a new `issued_authorization(..)` helper, and rewrite the unit test's assertion to `assert!(!revision.authorization_decision_ref.is_pending())`.

So #623 is not just a different implementation of the same decision. It is a **stricter gate** that rejects the placeholder, and it can only pass its own suite by first manufacturing issued references in test fixtures.

## 3. Why this is not a merge conflict

A merge conflict would be resolvable by reading both sides. This is not that:

- Git will report a conflict in `lib.rs` and in `phase2_acceptance.rs`, and the conflict markers will show two *coherent* alternatives.
- Resolving it by "take both" produces a struct with two authorization fields or a `validate()` that rejects `Absent` **and** `Placeholder`, i.e. a gate nothing can pass.
- Resolving it by "take theirs" silently discards one merged decision.
- Resolving it by "take mine" silently discards the other.

Neither PR is wrong on its own terms. #623 is a faithful implementation of #595, which froze a five-field `AuthorizationDecisionRef` with private `Pending | Issued` state and mandated custom Serde preserving the legacy unit/null form. #634 is a faithful implementation of the type-state decision, which froze a three-state field on `FactRevision` and required `Placeholder` to pass.

**The two decisions overlap on one question and answer it differently: does a pending placeholder satisfy the presence gate?** #595 never says. The type-state decision says yes, explicitly, and explains why. #623 assumed no.

## 4. Which one is actually binding

This is the part I can measure rather than argue, so I will only state what the documents say and stop.

- The type-state decision addresses the question directly, names `dm2_06` as its subject, and its §4 specifies the exact two assertions. It is the more specific instrument.
- #595 addresses the *shape of the reference*, and its own scope note says the durable-row validator is what makes a candidate valid. It does not rule on whether a `FactRevision` with a pending reference may validate structurally.

By specificity, the type-state decision governs the gate. But specificity is my reading, and this is precisely the kind of reading that should not be made by the session that wrote one of the two competing patches.

## 5. What must not happen

- **Do not merge both.** They cannot both be true.
- **Do not merge #623 as-is** without amending either it or D3, because it contradicts a merged decision while citing a different one.
- **Do not merge #634 as-is** without checking whether D3 itself was superseded by #595's later landing — #595 is the older decision but it landed in the same window, and "older" is not "superseded" here.
- **Do not let a third session "fix" this by adding a fourth state.** The defect is two incompatible answers, not too few states.

## 6. The three questions an Owner has to answer

1. **Does `Placeholder` satisfy the presence gate?** D3 says yes. #623 says no. One of them must yield, and the yielding one must be amended in the record, not just in code — otherwise the next session re-derives the same contradiction.
2. **If `Placeholder` is rejected (i.e. #623 wins), what happens to `FactRevision::initial`?** Every existing call site passes `pending_i()`. Under #623's rule they all construct values that immediately fail `validate()`, and `new()` calls `validate()`. So `initial` becomes unusable, which is a larger change than #623's diff admits — its own fixtures had to switch to `issued_authorization(..)` to keep compiling-and-passing.
3. **If `Placeholder` is accepted (i.e. #634 wins), what does #595's `from_issued_data` buy?** It buys authenticity, which the presence gate explicitly does not check. That is consistent — but it means #623's `is_pending()` check has no home in `FactRevision::validate()` and belongs somewhere else, or nowhere yet.

## 7. What this document does not do

It does not pick a winner, close either PR, or edit either decision. It records that two merged authorities were applied incompatibly within half an hour, by two sessions that each had grounds, and that the resolution is a ruling rather than a diff.

It also does not claim #634 is correct. I wrote it, which disqualifies me from ruling on it. The only thing I will assert is the measurement: the two patches cannot both be merged, and the contradiction is between the decisions, not between the implementations.
