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
      last_verification_note: "Every line number re-read from main @ 2093e07a; the two shipped steps are verified against the blob of phase2_acceptance.rs (6135a8db30) and the current lib.rs, not against a commit message."
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

# GAP-18 (continued) — the authorization validator: what is left, exactly

**Status:** Open · **Supersedes nothing** · **Companion to:** `GAP-18-AUTHORIZATION-VALIDATOR-WORK-ORDER.md`
**Measured at:** `main` @ `2093e07ae2ef1edd44993853e87f998af155ff3a`
**Author:** owner delegate under standing instruction (Issue #564, comment 7074302216)

---

## 1. Why this document exists

`GAP-18` (`#653`, `456d4d55`) described a five-step work order and said the template was already in the tree. Two of those five steps have since shipped, by a commit that was not written against this work order:

`001248d452` — *feat(domain): let AuthorizationDecisionRef express absence, closing the last phase-2 ignore*

It modified two files:

| file | +/− | what it did |
|---|---|---|
| `crates/memory-domain/src/lib.rs` | +41 / −5 | replaced `pub struct AuthorizationDecisionRef(())` with a three-state enum |
| `crates/memory-domain/tests/phase2_acceptance.rs` | +54 / −2 | removed the last `#[ignore]` and wrote the real `dm2_06` |

That commit is correct. This document records **what it left**, so the remaining work is not re-derived and the shipped work is not redone. Three of the five steps remain, and none of them is in `memory-domain`.

I am writing this because the alternative is what happened twice already in this repository: a later session re-reads the work order, sees five steps, and implements step 3 a second time against a struct that is no longer a struct.

## 2. What shipped, verified rather than assumed

Read from `main` at `2093e07a`, blob `6135a8db30` for the test file and the current `lib.rs`:

**The type** (`crates/memory-domain/src/lib.rs:538`):

```rust
#[derive(serde::Serialize, serde::Deserialize, Clone, Debug, Eq, PartialEq)]
#[serde(rename_all = "snake_case")]
pub enum AuthorizationDecisionRef {
    /// No authorization decision was recorded. This is the only state that blocks publication.
    Absent,
    /// The known unvalidated placeholder: a value exists, nothing is proven.
    PendingI,
    /// A caller-claimed I-issued reference. Authenticity is not asserted; whether it is
    /// genuine is I's contract and `B-P2-XO-01`'s question.
    Issued(OpaqueId),
}
```

**The gate** (`:1008`), inside `FactRevision::validate`:

```rust
// Presence gate, not authenticity: `Absent` means nobody recorded a decision, which
// is exactly what DM2-06 says must not publish. `PendingI`/`Issued` pass because
// presence is all this gate can check; proving issuance is `B-P2-XO-01`.
if self.authorization_decision_ref.is_absent() {
    return Err(DomainError::MissingAuthorizationDecision);
}
```

This is `OWNER-RULING-025` implemented exactly: `Absent` blocks, `PendingI` and `Issued` pass presence. Step 3 and step 5 of the original work order are done.

**The test** (`crates/memory-domain/tests/phase2_acceptance.rs:608`), five assertions:

| # | assertion | ruling clause satisfied |
|---|---|---|
| 1 | `with_decision(absent())` → `Err(MissingAuthorizationDecision)` | §3.1 — absence blocks |
| 2 | `with_decision(pending_i()).unwrap()` then `validate().is_ok()` | §3.2 — placeholder satisfies presence |
| 3 | `with_decision(issued(..)).unwrap()` then `validate().is_ok()` | §3.2 — claimed issuance satisfies presence |
| 4 | wire form rewritten to `"absent"`, re-validated → same `Err` | §3.4 — a persisted revision cannot be edited into absence |
| 5 | `absent()` / `pending_i()` stay distinguishable after round-trip | §3.5 — a reader cannot mistake one for the other |

`grep -c '#\[ignore\]'` on that file returns `1`, and the single match is a comment on line 5 (`//! 纪律：当前类型系统无法表达的条目一律 ...`), not an attribute. **There are zero ignored tests in that file.** The PR body of `#659` claims `0 ignored` for `main`; for this file that is correct.

## 3. What remains: three steps, all in `memory-compiler`

`GAP-18` §3 established the correspondence. Here it is again with the line numbers as they stand at `2093e07a`, because the earlier document used the numbers from an older tree:

| concern | canonical commit (exists today) | authorization (to add) |
|---|---|---|
| table | `canonical_commits` — `admission.rs:367` | `authorization_decisions` |
| writer | `issue_canonical_commit` — `admission.rs:996` | `issue_authorization_decision` |
| validator | `validate_canonical_commit` — `admission.rs:1069` | `validate_authorization_decision` |
| error enum | `CanonicalCommitValidationError` — `admission.rs:240` | `AuthorizationDecisionValidationError` |
| row reader | `read_canonical_commit` — `admission.rs:1124` | `read_authorization_decision` |
| issuer const | `DEV_BASELINE_ISSUER` — `canonical_commit.rs:15` | `I_DEV_BASELINE_ISSUER` |

### Step 1 — the table

Append to the same `execute_batch` that already ends with `canonical_commits` (`admission.rs:367`–`374`), inside the same string, before the closing quote:

```sql
CREATE TABLE IF NOT EXISTS authorization_decisions (
   decision_id     TEXT PRIMARY KEY NOT NULL,
   issuer_id       TEXT NOT NULL,
   subject_digest  TEXT NOT NULL,
   issued_at       TEXT NOT NULL,
   signature       TEXT NOT NULL
);
```

Why the shape is identical to `canonical_commits` and not "similar": `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.1 specifies this DDL. A column added here that the decision does not name is a field the validator will not check, and an unchecked field in an authority table is a place a wrong value can live undisturbed. If the decision's DDL and this block ever diverge, the decision is right.

`signature` is written as `''` by the writer, exactly as `issue_canonical_commit:1027` does. It is present so the schema can carry a real signature later without a migration; nothing reads it today, and the validator must not pretend it verified anything.

### Step 2 — the writer and the validator

Copy `issue_canonical_commit` (`:996`) and `validate_canonical_commit` (`:1069`) and rename. Three things must change and everything else must not:

**(a) The issuer constant.** `I_DEV_BASELINE_ISSUER` is a different string from `DEV_BASELINE_ISSUER`. If the same constant is reused, an I-issued decision becomes indistinguishable from a D-issued commit at the storage layer, which is the confusion this whole line of work exists to remove. Define it next to `DEV_BASELINE_ISSUER` in `canonical_commit.rs`, or in a new `authorization.rs` beside it — but define it, do not alias it.

**(b) The cursor.** `validate_canonical_commit` takes `cursor: &OpaqueId` and rejects it at `:1078` when it does not equal `data.commit_id`. The decision's §4.1 signature has **no cursor parameter**:

```rust
pub fn validate_authorization_decision(
    &self,
    reference: &AuthorizationDecisionRef,
    expected_subject_digest: &OpaqueId,
) -> Result<bool, AuthorizationDecisionValidationError>;
```

Do not add one for symmetry. The cursor exists in the canonical-commit validator because a publication path selects a commit by cursor; no such selector exists for decisions, and inventing one creates a second way to name a decision that the decision document does not recognize. **This is the one place where copying the template is wrong**, and it is the place a mechanical copy gets wrong.

**(c) The reference's absence state.** `validate_canonical_commit:1075` starts with `reference.data().ok_or(PendingReference)?` because `CanonicalCommitRef` is a three-state struct with an `Option` payload. `AuthorizationDecisionRef` is an **enum** with three variants, and the mapping is:

| variant | validator outcome |
|---|---|
| `Absent` | `Err(..)` — absence is never a validation result, it is a failure to have a reference at all |
| `PendingI` | `Err(..)` — same reason; a placeholder carries no decision id |
| `Issued(id)` | look up `id` and proceed to the three-outcome logic |

A mechanical copy that writes `reference.data().ok_or(..)` will not compile, because there is no `data()`. That compile error is the good outcome. The bad outcome is a `match` that folds `Absent` and `PendingI` into one arm and returns `Ok(false)` for both, which would make "nobody authorized this" indistinguishable from "authorized, wrong subject" — and `Ok(false)` is a **success** shape.

### Step 3 — `dm2_06` gains its authority assertion

This is the step the contradiction in `#623` / `#634` was about, and `GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024` (`#640`) is the register entry. `OWNER-RULING-025` §5 and `I-OWNER-DECISION-...-001` §4.3 both require it.

The test as it stands at `phase2_acceptance.rs:608` proves presence. It does not prove that a **present but unbacked** reference is refused, because `memory-domain` cannot see the store: its `Cargo.toml` depends on `serde` and nothing else. So the assertion has to live where the store lives.

Add a new integration test under `crates/memory-compiler/tests/` — not in `phase2_acceptance.rs` — with this shape:

```rust
// A decision reference that claims issuance but has no durable row must be
// refused by the authority, and that refusal must be an Err, not Ok(false).
let reference = AuthorizationDecisionRef::issued(id("ad-never-issued"));
let outcome = store.validate_authorization_decision(&reference, &subject_digest);
assert!(
    matches!(outcome, Err(AuthorizationDecisionValidationError::RecordMissing)),
    "an unbacked issued reference must be an authority error, got {outcome:?}"
);
```

Three properties of that assertion are load-bearing and each corresponds to a mistake made in a real PR:

1. **`Err`, not `Ok(false)`.** `#623` asserted `Err(EmptyRequiredField)` — the wrong error, produced by the wrong layer, because it drove the gate through `FactRevision::validate()` where the only reachable failure was a field check. The decision document is explicit (§4.2): "a missing row is always `Err`".
2. **`RecordMissing`, not any `Err`.** An assertion that accepts any error passes when the validator is broken in a way that fails earlier — for example at `Absent` handling — and then the test is green and measures nothing.
3. **In `memory-compiler`, not `memory-domain`.** `#623` put the gate in `memory-domain` and had to rewrite the fixtures to avoid `pending_i()`, because `FactRevision::validate()` rejected `is_pending()` at the time. That rejection is gone (`:1008` now rejects only `is_absent()`), so the fixtures are safe again — but the store still is not reachable from `memory-domain`, and no amount of fixture rewriting changes that.

## 4. What not to do

Each item is a defect observed in a real PR on this repository, not a hypothetical.

- **Do not implement the validator in `memory-domain`.** Its `Cargo.toml` has one dependency (`serde`). Adding `rusqlite` to it inverts the layering the workspace is built on: the domain crate is the thing that must be testable without a database. `#623` is what this looks like when it is tried.
- **Do not make `FactRevision::validate()` reject `PendingI`.** `OWNER-RULING-025` exists because that reading was attempted. A `PendingI` that fails validation makes every `initial(.., pending_i(), ..)` call site fail at construction, which forces fixtures to be rewritten and hides the real gate behind a constructor error.
- **Do not fold `Absent` and `PendingI` into one validator arm returning `Ok(false)`.** See §3 step 2(c). `Ok(false)` means "the record exists and disagrees", which is a different fact.
- **Do not add a cursor parameter.** See §3 step 2(b).
- **Do not reuse `DEV_BASELINE_ISSUER`.** See §3 step 2(a).
- **Do not remove `dm2_06`'s presence assertions while adding the authority one.** `#634` did this as a rebase accident and lost `mod canonical_commit;`, `pub use canonical_commit::*;`, the content-bearing `CanonicalCommitRef`, and `dm2_15` along with it. The presence test and the authority test assert different things and both must exist.

## 5. Definition of done

- [ ] `authorization_decisions` table created in the same batch as `canonical_commits`, columns exactly as §3.1 of the decision.
- [ ] `issue_authorization_decision` with the idempotent-replay handling copied from `issue_canonical_commit:1035`–`1051`: duplicate primary key reads back and compares fields, byte-identical is a replay, anything else is `IdempotencyConflict`.
- [ ] `validate_authorization_decision(reference, expected_subject_digest)` — **two parameters**, matching §4.1.
- [ ] `AuthorizationDecisionValidationError` with at least `RecordMissing`, `RecordMalformed`, `RecordMismatch(&'static str)`, `UnsupportedIssuer`, `ReadFailed`, and one variant for the absent/placeholder case. `Display` implemented, following `:257`.
- [ ] A new test in `crates/memory-compiler/tests/` asserting `Err(RecordMissing)` for an unbacked `issued()` reference.
- [ ] A second test in the same file asserting `Ok(true)` after a real `issue_authorization_decision` call, and `Ok(false)` when `expected_subject_digest` differs — the three outcomes of §4.2, each reached by a path that can only reach it.
- [ ] `dm2_06` in `phase2_acceptance.rs` unchanged. It is correct.
- [ ] `cargo test --workspace --all-targets` reports zero ignored in `memory-domain`.

## 6. Why this is a work order and not a patch

I do not write code on this repository. That is the one constraint I hold without exception, and it is why this document specifies line numbers, exact SQL, exact signatures, and the three places a mechanical copy fails instead of producing the diff itself. Everything needed to write the diff is here; the diff is not.

The reason to prefer this over another round of discussion is in §2: the two steps that shipped were correct, and they shipped without this document. What was missing was not judgment but a record of what remained, and the cost of that absence is measurable — `#623` and `#634` both re-derived step 3, both got it wrong in different directions, and one of them lost four unrelated items to a rebase.
