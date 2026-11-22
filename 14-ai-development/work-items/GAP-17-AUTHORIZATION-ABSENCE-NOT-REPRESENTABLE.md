# GAP-17 — missing authorization is not representable, and two DECIDED contracts disagree on how to make it so

**Status:** Open · **Severity:** Tier 2 (blocks the last `#[ignore]` in the workspace; no live exploit) · **Owner:** I (decision), E (implementation)
**Measured at:** `origin/main @ 709914f5`, `2026-11-22`
**Related:** `dm2_06`, ADR `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`, `I-OWNER-DECISION-AUTHORIZATION-DECISION-001`, GAP-14, `B-P2-XO-01`

## 1. What is actually blocked

`crates/memory-domain/tests/phase2_acceptance.rs:606`, `dm2_06_missing_authorization_ref_blocks_fact_publication`,
is the last `#[ignore]` in the workspace. It has never had a body — it is `unimplemented!()`.

The requirement it must satisfy is `02-domain-model/phase-2-domain-extension.md:241`:

> DM2-06: missing or invalid I authorization reference prevents Fact publication (after I decision is frozen).

The obstruction is type-level, and it is exact:

| fact | measurement |
|---|---|
| `AuthorizationDecisionRef` is a unit struct with no state | `lib.rs:531` `pub struct AuthorizationDecisionRef(());` |
| its only public constructor always yields a present value | `lib.rs:532-536` `pub const fn pending_i() -> Self { Self(()) }` |
| `FactRevision::initial` takes authorization as a required, non-`Option` parameter | `lib.rs:837` `authorization_decision_ref: AuthorizationDecisionRef,` |
| `successor` does the same | `lib.rs:873` |
| `validate()` does not inspect the field at all | `lib.rs:961-1012` — no reference to `authorization_decision_ref` |
| `memory-domain` cannot reach the compiler-side validator | `memory-domain/Cargo.toml` has no `memory-compiler` dependency; `memory-compiler` depends on `memory-domain`, not the reverse |

There is therefore **no value of `AuthorizationDecisionRef` that means "absent"**, and no constructor
path to `FactRevision` that omits it. A test cannot express the precondition of DM2-06, so it cannot
assert the conclusion. This is not a missing assertion; it is a missing state.

## 2. The two DECIDED contracts disagree

Both documents are on `main` and both are marked DECIDED. They specify incompatible repairs.

### 2.1 `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` (ADR, committed `986c42bc`, 13:41 +0800)

- **D2:** `FactRevision` gains a three-state authorization field: `Absent` / `Placeholder` / `Issued(..)`.
- **D5:** `initial` keeps the required-argument constructor **and gains one that takes no authorization**.
- **D6:** the presence gate is a **domain invariant**: `validate()` must reject `Absent` when
  `outcome == FactOutcome::Attested`.

Under this contract, `dm2_06` is expressible inside `memory-domain`, needs nothing from I, and needs
nothing from `memory-compiler`.

### 2.2 `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` (committed `c9a6394d`, 12:54 +0800)

- **§2.2:** `AuthorizationDecisionRef` gains `Pending` / `Issued(AuthorizationDecisionData)`.
  There is **no `Absent` state**.
- **§3.3:** "The validator is **not** a `FactRevision::validate()` responsibility. Domain validation may
  validate candidate field syntax and reject Pending, but only the compiler's AdmissionStore-backed
  validator can establish durable existence and authority."
- **§4.3:** "`dm2_06` must exercise the **Pending reference** path and assert a propagated authority `Err`,
  not `Ok(false)`. **The field is required and non-optional; there is no `None` state.**"
- **§6 closure item 12:** E must delete the `#[ignore]` and assert the propagated authority `Err`.

Under this contract, `dm2_06`'s assertion lives in the **compiler's** AdmissionStore validator. The test
at `phase2_acceptance.rs:606` is in `memory-domain`, which has no dependency on `memory-compiler`.
The path §4.3 names is **unreachable from where the test lives**.

### 2.3 Why this is a real conflict, not a wording difference

| question | ADR-001 | I-001 |
|---|---|---|
| can absence be represented? | yes, `Absent` | no, "there is no `None` state" |
| who rejects it? | `FactRevision::validate()` (domain) | `AdmissionStore` validator (compiler) |
| what does `dm2_06` assert? | `validate()` returns `Err` | a propagated authority `Err` from the compiler |
| is `pending_i()` rejected by `validate()`? | no — `Placeholder` passes the presence gate | yes — "reject Pending" |

The two cannot both be implemented. They disagree on the state set, on the enforcement layer, and on
what the test asserts.

## 3. What this document does not do

It does not choose between them. Both are DECIDED, both are owner-authored, and choosing would
substitute this measurement for a decision that is I's to make. It records the conflict and the two
exact repairs so the next reader does not have to rediscover that a "DECIDED" contract and a
"DECIDED" ADR contradict each other.

It also does not implement either. The `#[ignore]` stays, with a reason that now names both repairs.

## 4. Unblocking, stated as two alternatives

**(1) ADR-001 path.** `FactRevision::initial` gains an `Option<AuthorizationDecisionRef>` overload (or a
second constructor that takes none); `validate()` returns a named error for `None` +
`FactOutcome::Attested`. The test constructs a fact with absent authorization and asserts that error.
Scope: `memory-domain` only. `dm2_06` becomes a real assertion.

**(2) I-001 path.** `AuthorizationDecisionRef` gains `Pending` / `Issued`; the AdmissionStore validator
is implemented in `memory-compiler`; `dm2_06` moves out of `memory-domain` into a compiler-side
integration test that can reach the validator, and asserts the propagated `Err`. Scope:
`memory-domain` + `memory-compiler` + a new test location. The test at `phase2_acceptance.rs:606`
cannot hold the assertion under this contract.

Either way, one of the two documents must be amended so the repository has one answer.

## 5. Interaction with GAP-14

`fact_with_placeholder_attestor_validates_today` (`lib.rs:2196`) pins that a placeholder passes
`validate()` today. GAP-14's repair (reject placeholders in `validate()`) would flip it. The ADR path
above keeps it passing for `Placeholder` and only rejects `Absent`; the I-001 path rejects `Pending`
in domain validation and therefore **contradicts** that Round 4 test. The three documents cannot be
reconciled without one of them changing.

## 6. Closure criteria

1. Exactly one of the two repairs is implemented.
2. `dm2_06` has a real body and is no longer `#[ignore]`.
3. `cargo test --workspace --all-targets -- --list --ignored` is empty.
4. The losing document is amended to point at the winning one, so no future reader finds two
   DECIDED answers to one question.
