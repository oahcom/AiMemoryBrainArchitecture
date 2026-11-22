---
document_metadata:
  domain: domain-model
  role: work-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner delegate under standing instruction"
      decision_date: "2026-11-22"
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "Every line number and signature re-read from main @ c9036544; the template table is a file:line index into shipped code."
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

# GAP-18 — The authorization validator: a work order with a template already in the tree

**Status:** Open — ready to implement
**Area:** memory-compiler / memory-domain
**Measured at:** `main @ c9036544`, `2026-11-22T16:10Z`
**Authority:** `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025`, `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.1, §4.1, §4.2
**Supersedes:** the work-order section of `GAP-16` only where that document speaks about authorization; it does not.

---

## 1. Why this document exists

Two PRs (#623, #634) tried to close `dm2_06` by editing `crates/memory-domain/`. Neither can, because the thing `dm2_06` needs does not exist and cannot exist there: a durable row.

The contract says where it goes. §3.3:

> Tables, insert/read operations and record-backed validators belong in `memory-compiler` behind `AdmissionStore`, matching D's layering.

`crates/memory-domain/Cargo.toml` has exactly one dependency:

```toml
[dependencies]
serde = { version = "1", features = ["derive"] }
```

No `rusqlite`, no `AdmissionStore`, no connection. The work is not a rewrite of an existing type. It is a new validator in a different crate, and it is a **near-exact copy of one that already ships**.

## 2. The template is already in the tree

`D-OWNER-DECISION-CANONICAL-COMMIT-001` froze the same shape for canonical commits, and it is implemented and tested. Authorization is the same problem with a different allowlist and one extra column.

| concern | canonical commit (exists) | authorization (to add) |
|---|---|---|
| table | `canonical_commits` — `admission.rs:367` | `authorization_decisions` |
| writer | `issue_canonical_commit` — `admission.rs:996` | `issue_authorization_decision` |
| validator | `validate_canonical_commit` — `admission.rs:1069` | `validate_authorization_decision` |
| error enum | `CanonicalCommitValidationError` — `admission.rs:240` | `AuthorizationDecisionValidationError` |
| row reader | `read_canonical_commit` — `admission.rs:1128` | `read_authorization_decision` |
| issuer const | `DEV_BASELINE_ISSUER` — `canonical_commit.rs:15` | `I_DEV_BASELINE_ISSUER` |
| domain ref | `CanonicalCommitRef` — `canonical_commit.rs:59` | `AuthorizationDecisionRef` |
| validation helper | `validate_canonical_commit_data` — `canonical_commit.rs:172` | `validate_authorization_decision_data` |

Every row is a copy with substitutions. That is the whole work order.

## 3. Step 1 — the two tables

`crates/memory-compiler/src/admission.rs`, in the schema-init block that already creates `canonical_commits` at `:367`. §3.1 gives the DDL verbatim; do not invent column names:

```sql
CREATE TABLE IF NOT EXISTS authorization_decisions (
    decision_id      TEXT PRIMARY KEY NOT NULL,
    issuer_id        TEXT NOT NULL,
    subject_digest   TEXT NOT NULL,
    issued_at        TEXT NOT NULL,
    decision_kind    TEXT NOT NULL,
    signature        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS i_attestations (
    attestation_id   TEXT PRIMARY KEY NOT NULL,
    issuer_id        TEXT NOT NULL,
    subject_digest   TEXT NOT NULL,
    issued_at        TEXT NOT NULL,
    signature        TEXT NOT NULL
);
```

The only structural difference from `canonical_commits` is `decision_kind`. Separate primary-key namespaces are the contract's requirement (§3.1, last line) — they prevent an attestation id being mistaken for a decision id, which is why they are two tables and not one with a discriminator column.

`i_attestations` is needed by criterion 6 and criterion 9. It is not needed by `dm2_06`. If the tranche must be split, do `authorization_decisions` first and leave `i_attestations` for the attestor PR — but then criterion 6 is partially met and the PR body should say so.

## 4. Step 2 — the validator

Sign it exactly as §4.1 does. Do not change the signature to suit the implementation.

```rust
pub fn validate_authorization_decision(
    &self,
    reference: &AuthorizationDecisionRef,
    expected_subject_digest: &OpaqueId,
) -> Result<bool, AuthorizationDecisionValidationError>;

pub fn authorization_decision_kind(
    &self,
    reference: &AuthorizationDecisionRef,
) -> Result<AuthorizationDecisionKind, AuthorizationDecisionValidationError>;
```

The body is `validate_canonical_commit` at `:1069` with four changes:

1. `reference.data()` returning `None` is `Err(PendingReference)`. There is no cursor parameter — §4.1's signature has none, unlike the canonical version.
2. The issuer check compares against `I_DEV_BASELINE_ISSUER` (`i-owner-proxy/dev-baseline-v1`), not `DEV_BASELINE_ISSUER`.
3. After the digest and timestamp comparisons, compare `stored.decision_kind` against the reference's. A mismatch is `Err(RecordMismatch("decision_kind"))`.
4. Return `Ok(stored.subject_digest == expected_subject_digest.as_str())`.

The three outcomes of §4.2 fall out of the existing structure with no extra code, and that is the point of copying it:

- `Ok(true)` — row readable, every field matches, issuer allowlisted, stored digest **equals** expected.
- `Ok(false)` — row readable, every field matches, stored digest **differs** from expected. Exactly one case.
- `Err(..)` — everything else. **A missing row is `RecordMissing`, never `Ok(false)`.** §4.2 states this twice; it is the whole reason the validator exists rather than a boolean check.

`authorization_decision_kind` reads the same row and returns the stored kind. §4.1 is explicit that it "is not itself an authority check", and that publication may proceed only when validation returned `Ok(true)` **and** the kind is `Approved`. Keep those two calls separate at the call site; do not fold the `Approved` test into `validate_authorization_decision`, because a valid `Denied` record must still return `Ok(true)` — it is a recorded decision, and conflating it with missing authority is the defect §4.3 warns about.

## 5. Step 3 — the domain reference

`crates/memory-domain/src/lib.rs`. `AuthorizationDecisionRef` is currently `struct AuthorizationDecisionRef(());` at `:531` with one constructor, `pending_i()`.

Give it the shape §2.2 froze, which is the same shape `CanonicalCommitRef` already has at `canonical_commit.rs:59`:

```rust
enum AuthorizationDecisionRefState { Pending, Issued(AuthorizationDecisionData) }
pub struct AuthorizationDecisionRef { state: AuthorizationDecisionRefState }
```

with `pending_i()` → `Pending`, `from_issued_data(data)` → validated `Issued`, `is_pending()`, `data()`. Serde must keep the legacy form: `Pending` serializes to `null` and deserializes from `null`, and a malformed issued object fails closed rather than degrading to `Pending`. `CanonicalCommitRef`'s implementation at `canonical_commit.rs:59-200` is the reference; copy it.

`IssuerId` must be defined **once at the crate root** and re-exported, per §2.2: "D's `IssuerId` and I's `IssuerId` are the same Rust type, defined once in `memory-domain` and shared across owner contracts; do not create an I-specific duplicate." #623 got this part right — `canonical_commit.rs` had its own `IssuerId` and #623 replaced it with `pub use crate::IssuerId;`. Keep that.

Add `I_DEV_BASELINE_ISSUER = "i-owner-proxy/dev-baseline-v1"` next to `DEV_BASELINE_ISSUER`, and `AuthorizationDecisionKind { Approved, Denied, Conditional }` (§2.1).

**Do not add any authority check to `FactRevision::validate()`.** It rejects `Absent` (per D3) and accepts `Placeholder`; that is the whole of its obligation under criterion 11.

## 6. Step 4 — `dm2_06`, last

Keep the `#[ignore]` until step 2 exists. Then replace it with a test that constructs a `Pending` reference, calls `validate_authorization_decision`, and asserts:

```rust
Err(AuthorizationDecisionValidationError::PendingReference)
```

not `Ok(false)`, and not an error from `FactRevision::validate()`. §4.3: "must exercise the **Pending reference** path and assert a propagated authority `Err`".

Because the validator is on `AdmissionStore`, this is naturally an integration test in `crates/memory-compiler/tests/`, not a unit test in `memory-domain`. If it stays in `phase2_acceptance.rs`, that file needs a `memory-compiler` dev-dependency, which would make the domain crate's tests depend on the compiler — the direction §3.3 exists to prevent. Put it in the compiler.

Criterion 8 wants nine more cases (valid Approved/Denied/Conditional, missing row, issuer mismatch, metadata mismatch, digest mismatch, malformed row, read failure). They are all one-liners against the same validator; the `canonical_commits` tests at `admission.rs:1671` are the pattern.

## 7. What not to do

- **Do not** put the validator in `memory-domain`. It has no `rusqlite` and must not gain one; §3.3 is explicit that the domain crate "remains SQLite-independent".
- **Do not** reject `Placeholder` in `FactRevision::validate()`. That is #623's defect; `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` rules it out and `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.3 forbids it.
- **Do not** touch `canonical_commit.rs` or `CanonicalCommitRef`. That is #634's defect and it is unrelated to this work.
- **Do not** add a fourth state. Two states on the reference (`Pending | Issued`) and three on the fact field (`Absent | Placeholder | Issued`) are enough; the contradiction was never "too few states".
- **Do not** un-ignore `dm2_06` before the validator exists. That closes the item without doing the work, which is what both open PRs do.

## 8. Definition of done

- `cargo test -p memory-compiler` passes, including the nine criterion-8 cases.
- `cargo test -p memory-domain` passes with **no** `#[ignore]` remaining and `dm2_15` still present.
- `dm2_06` asserts `Err(PendingReference)` from the store validator.
- `FactRevision::validate()` rejects `Absent`, accepts `Placeholder`, and its test says why in one line.
- `git diff --stat` touches `memory-compiler/src/admission.rs`, `memory-domain/src/lib.rs`, `memory-domain/src/canonical_commit.rs` (only to re-export `IssuerId`, if not already), and tests. It does **not** delete `mod canonical_commit;` and does not delete any test.
