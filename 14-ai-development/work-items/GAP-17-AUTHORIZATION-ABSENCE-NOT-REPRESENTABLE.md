---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null

    evidence_verification:
      verification_status: Unverified

    usage_status: Active
    modification_status: Modified

  authority:
    canonical_status: Non-Canonical
    normative_status: Informative
    canonical_conflict_status: None
---

# GAP-17 — missing authorization is not representable: ruling recorded, implementation owed

**Status:** Open — contract resolved, implementation owed · **Severity:** Tier 2 (blocks the last `#[ignore]` in the workspace; no live exploit) · **Owner:** E (implementation); ruling by team-lead
**Measured at:** `origin/main @ 709914f5`, `2026-11-22`. Every count below names its commit; `main` advances during the day and a count without a commit is not reproducible.
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

## 2. The two DECIDED contracts, and what the ruling made of them

Both documents are on `main` and both are marked DECIDED. The four-dimension table in §2.3 is the
measurement that produced this gap. It stays as evidence. What follows it is the ruling: most of the
apparent conflict is two different gates at two different layers, and only two clauses genuinely collide.

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

### 2.3 The four-dimension measurement

| question | ADR-001 | I-001 |
|---|---|---|
| can absence be represented? | yes, `Absent` | no, "there is no `None` state" |
| who rejects it? | `FactRevision::validate()` (domain) | `AdmissionStore` validator (compiler) |
| what does `dm2_06` assert? | `validate()` returns `Err` | a propagated authority `Err` from the compiler |
| is `pending_i()` rejected by `validate()`? | no — `Placeholder` passes the presence gate | yes — "reject Pending" |

## 3. The ruling: what coexists, what is superseded

**Ruled by team-lead on 2026-11-22, after this gap was filed.** The ruling is recorded here rather than
left as an open question, because the question it answers is a coordination decision, not a measurement.

### 3.1 These coexist — they are two gates at two layers, not rivals

- **I-001 §3.3** puts the *authenticity* validator in `memory-compiler` behind `AdmissionStore`.
  **ADR-001 D6** puts the *presence* gate in domain `validate()`. "Was this authorization real?" and
  "was any authorization recorded at all?" are different questions, and ADR-001 §1 argues that
  separation explicitly. Both gates stand.
- **I-001 §4.2's** three outcomes (`Ok(true)` / `Ok(false)` for subject mismatch / `Err` for missing
  authority) stand unchanged. ADR-001 §5 deliberately leaves stricter publication-time rejection open.

Read this way, the third and fourth rows of §2.3 are not contradictions: they describe different gates.

### 3.2 These are superseded — ADR-001 governs, on two points only

1. **Type shape.** I-001 §2.2's two-state enum `{ Pending, Issued }` cannot express absence. **ADR-001 D2's
   three states govern.** ADR-001 is 47 minutes later and the type state is its explicit subject.
2. **What `dm2_06` asserts, and where.** I-001 §4.3 requires `dm2_06` to assert a compiler-layer
   propagated `Err`. **That requirement is not hard — it is unreachable.** The test sits at
   `crates/memory-domain/tests/phase2_acceptance.rs:605`, and `crates/memory-domain/Cargo.toml` does not
   depend on `memory-compiler`; the dependency direction is the reverse. A requirement that cannot exist
   where it is specified is a defect in the document, not an obligation on the implementer.
   **ADR-001 §4 governs:** `dm2_06` becomes two domain-layer assertions.

### 3.3 The residual obligation, stated plainly

I-001's compiler-layer **authenticity validator is still required.** It is not `dm2_06` and must never
be counted as `dm2_06`. It needs its **own** test at a location that can reach `memory-compiler`.
Closing `dm2_06` does not close it, and a green `dm2_06` is not evidence that it exists.

## 4. Resolution, and what remains owed

**`dm2_06` is blocked on implementation of ADR-001 D2/D6, not on an undecided contract.** The contract
question is closed by §3. What remains is code:

- `FactRevision` gains the three-state authorization field (D2).
- `FactRevision::initial` gains a constructor that takes no authorization, keeping the required-argument
  one (D5).
- `validate()` rejects `Absent` + `FactOutcome::Attested` with a named error (D6).
- `dm2_06` then becomes two assertions: absent + `Attested` is rejected; `Placeholder` still validates
  (ADR-001 §4 — the second assertion is what keeps the gate honest about checking presence, not authenticity).

Scope: `memory-domain` only. An implementation PR is in flight.

**Separately owed:** the compiler-layer authenticity validator from I-001 §3.3/§4.2, with its own test
that can reach `memory-compiler`. Tracked, not started, not `dm2_06`.

## 5. Interaction with GAP-14

`fact_with_placeholder_attestor_validates_today` (`lib.rs:2196`) pins that a placeholder passes
`validate()` today. GAP-14's repair (reject placeholders in `validate()`) would flip it. The ADR path
keeps it passing for `Placeholder` and rejects only `Absent`, so ADR-001 and GAP-14 are compatible as
written. The tension that remains is that ADR-001 §5 leaves "should `Placeholder` be rejected at
publication time" open — GAP-14 is one place that door could close.

## 6. Closure criteria

1. ADR-001 D2/D5/D6 are implemented in `memory-domain`.
2. `dm2_06` has a real body and is no longer `#[ignore]`.
3. `cargo test --workspace --all-targets -- --list --ignored` is empty.
4. I-001's compiler-layer authenticity validator has its own test, separate from `dm2_06`, at a location
   that can reach `memory-compiler`.

