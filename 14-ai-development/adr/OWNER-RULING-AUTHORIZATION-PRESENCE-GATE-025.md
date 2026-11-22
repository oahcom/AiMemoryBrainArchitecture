---
document_metadata:
  domain: domain-model
  role: decision-record

  lifecycle:
    approval:
      decision_status: Approved
      approver: "Project Owner delegate under standing instruction (Issue #564, comment 7074302216)"
      decision_date: "2026-11-22"
      approved_version:
        scheme: git
        value: "c90365442fe29c67f015dee6533a026ea585abc0"
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "Issue #640 (GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024)"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-22"
      last_verification_note: "All measurements re-run against main @ 46e2d243fc and against #634's own base 85504756b8 via git blob SHA, not contents?ref=."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Canonical
    canonical_scope: "Owner ruling: Placeholder satisfies the FactRevision presence gate; the propagated authority Err that dm2_06 must assert comes from the AdmissionStore validator, not from FactRevision::validate()."
    canonical_scope_id: domain-model/authorization-presence-gate-ruling
    canonical_scope_keywords:
      - authorization-presence-gate
      - placeholder
      - dm2-06
      - admission-store-validator
      - canonical-commit-ref-regression
    canonical_conflict_status: None
    normative_status: Normative
---

# OWNER RULING 025 — `Placeholder` satisfies the presence gate; #634 is rejected on regression, #623 is rejected on scope

**Status:** Decided — binding
**Area:** memory-domain / memory-compiler / governance
**Measured at:** `main @ 46e2d243fc`, `2026-11-22T15:40Z`
**Subject:** the contradiction registered in `GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024` (PR #640)
**Supersedes:** nothing. **Amends:** `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §4.3 and closure criteria 11–12, by interpretation only.

---

## 1. The ruling in one paragraph

`Placeholder` satisfies the presence gate. `FactRevision::validate()` MUST reject `Absent` and MUST NOT reject `Placeholder`. `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §4.3 does not require otherwise: it requires `dm2_06` to assert a propagated authority `Err`, and that error is produced by the `AdmissionStore`-backed validator of §4.1, not by `FactRevision::validate()`. `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D3 is correct as written. Neither open PR may merge as written: #634 on a measurable regression, #623 on crate-boundary scope.

This ruling does not overturn a decision. It resolves a misreading, and it resolves it with the authority document's own text.

## 2. Why this is a reading and not a choice

`GAP-...-024` §4 says the choice "should not be made by the session that wrote one of the two competing patches", and correctly declines. I wrote `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001`. So I cannot rule on the merits of my own instrument. What I can do is read the *other* instrument, which is not mine, and which settles the question by itself.

`I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §3.3, in full:

> The validator is **not** a `FactRevision::validate()` responsibility. Domain validation may validate candidate field syntax and reject Pending, but only the compiler's AdmissionStore-backed validator can establish durable existence and authority. Structural validation must not claim a candidate reference is issued.

§4.3, in full:

> `dm2_06_missing_authorization_ref_blocks_fact_publication` must exercise the **Pending reference** path and assert a propagated authority `Err`, not `Ok(false)`. The field is required and non-optional; there is no `None` state. An issued candidate with no durable row is also Err.

Closure criterion 12, in full:

> E MUST delete the `#[ignore]` on `dm2_06_...` and replace `unimplemented!()` with a real assertion that missing/pending authorization is rejected with **the propagated authority Err**.

Criterion 11, in full:

> `FactRevision::validate()` does not claim a pending placeholder is issued authority; durable authority is established only by AdmissionStore validation.

Read together, these say three things, none of them ambiguous:

1. The rejection of a pending reference is the **AdmissionStore validator's** job (§3.3, §4.1, §4.3).
2. `FactRevision::validate()`'s only obligation is to **not claim** that a placeholder is issued authority (criterion 11).
3. The `Err` that `dm2_06` asserts must be the **propagated authority** error, i.e. the one §4.1 returns (criterion 12).

`FactRevision::validate()` returning `Err` is not the propagated authority error. It is a *second, earlier, unrelated* error of the same shape. Asserting it satisfies the letter of "assert an `Err`" while destroying the distinction §4.3 exists to protect — and §3.3 forbids it in the same document, in the sentence immediately before the validator is introduced.

So the two authorities do not contradict. #623 misread #595. `GAP-...-024` §3 states the contradiction as "does a pending placeholder satisfy the presence gate? #595 never says" — that is true of the *question as posed*, and false of the *answer needed*: §595 does not need to say, because it puts the rejection somewhere else entirely, and says so twice.

## 3. Why #634 must not merge, measured

Independent of the reading above, #634 carries a regression. Verified by blob SHA, not by `contents?ref=` (which the #612 audit found can return stale bodies).

At #634's **own base** `85504756b8`:

| fact | value |
|---|---|
| `mod canonical_commit;` present | **True** |
| `pub use canonical_commit::*;` present | **True** |
| `pub struct CanonicalCommitRef(())` present | **False** |
| `dm2_15` test present | **True** |

At #634's head `d55f4996ca`, blob `643f3028213f15c9e19714f1cccd86d22e03a02b`:

| fact | value |
|---|---|
| `mod canonical_commit;` present | **False** |
| `pub use canonical_commit::*;` present | **False** |
| `pub struct CanonicalCommitRef(())` present | **True** |
| `dm2_15` test present | **False** |

`CanonicalCommitRef` is the subject of `D-OWNER-DECISION-CANONICAL-COMMIT-001`. On `main` it is a content-bearing type with private `Pending | Issued` state at `crates/memory-domain/src/canonical_commit.rs:59`. #634 replaces it with a unit struct and stops compiling the module. `dm2_15_legacy_pending_canonical_commit_keeps_its_unit_representation` — the regression test that pins the legacy `null` wire form, cited to that decision's §5 and §8 criterion 3 — is deleted.

That is not a difference of opinion about authorization. It reverts a merged decision about canonical commit, in a PR about `dm2_06`, and it deletes the test that would have caught it. #634 cannot merge as written regardless of who is right about D3.

## 4. Why #623 must not merge, measured

#623 is a faithful implementation of what it thought #595 said, and it does three things the contract puts elsewhere or forbids:

**4.1 The gate is in the wrong crate.** §3.3 and §4.1 place `validate_authorization_decision` in `memory-compiler`, behind `AdmissionStore`, because only a durable row can establish authority. #623 touches only `crates/memory-domain/`:

```
crates/memory-domain/src/canonical_commit.rs   +3  -14
crates/memory-domain/src/lib.rs              +501  -40
crates/memory-domain/tests/phase2_acceptance.rs +21 -4
```

`memory-domain`'s `Cargo.toml` has exactly one dependency, `serde`. It cannot host an `AdmissionStore`-backed validator, and #623 does not try. So criterion 6 (`authorization_decisions` table), criterion 8 (record-backed outcomes), and criterion 12 (the propagated authority `Err`) are all unimplemented, while `dm2_06`'s `#[ignore]` is deleted. That closes the item without doing the work the item exists to force.

**4.2 It makes the required constructor unusable.** §2.2 keeps `pending_i()` as the only public constructor until I ships `from_issued_data`. #623's `validate()` rejects `is_pending()` at `lib.rs:1340`, and `new()` calls `validate()`. So every `FactRevision::initial(.., pending_i(), ..)` call site constructs a value that fails immediately. #623's own diff confirms it: the fixtures had to switch to a new `issued_authorization(..)` helper. The contract's own §2.2 says `pending_i()` is "legacy/uncommitted marker; never authorization evidence" — not "structurally invalid". Making it invalid is a larger change than the PR admits and is not what §4.3 asks for.

**4.3 It asserts the wrong error.** #623's `dm2_06` asserts:

```rust
Err(DomainError::EmptyRequiredField("authorization_decision_ref"))
```

with a comment: *"ponytail: reuses EmptyRequiredField to avoid a new variant this round."* §4.3 requires the **propagated authority `Err`**, and criterion 11 requires `validate()` to not claim issued authority. A reused `EmptyRequiredField` is neither: it says "the field is empty", which is false — the field holds `Pending`. The test passes while asserting a proposition the contract does not make.

## 5. What E must implement

The work is not in `memory-domain`. It is in `memory-compiler`, and `dm2_06` stays `#[ignore]`d until it exists. Concretely:

1. **`crates/memory-compiler/src/admission.rs`** — add the two tables of §3.1 (`authorization_decisions`, `i_attestations`), append-only, idempotent on byte-identical replay, error on same-ID-different-field.
2. **Same file** — `validate_authorization_decision(&self, reference, expected_subject_digest) -> Result<bool, _>` and `authorization_decision_kind(..)`, exactly as §4.1 signs them. Three outcomes per §4.2; **missing row is always `Err`, never `Ok(false)`**.
3. **`crates/memory-domain`** — `AuthorizationDecisionRef` gains `Pending | Issued(data)` with the five fields of §2.1, private state, and Serde preserving the legacy `null` form (criterion 4). No authority logic.
4. **`dm2_06`** — un-ignore only when step 2 exists, and assert the **`Err` from `validate_authorization_decision`**, not from `FactRevision::validate()`. It is an integration test in `memory-compiler`, or it takes the store as a fixture.
5. **`FactRevision::validate()`** — rejects `Absent` (per D3 / criterion 11), accepts `Placeholder`, and never claims `Issued` is verified.

Steps 1–2 are the whole of the missing work. Step 3 is #623 minus its `validate()` check and minus its fixture rewrite.

## 6. Amendments this ruling makes, in the record

- `I-OWNER-DECISION-AUTHORIZATION-DECISION-001` §4.3 and criteria 11–12 are **clarified, not changed**: "propagated authority `Err`" means the §4.1 validator's error. A future editor should not need this ruling to read that sentence correctly, so the clarification belongs in that document as a one-line note, in a documentation PR, not in code.
- `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` D3 stands. Its scope note already defers publication-time rejection of `Placeholder` to `B-P2-XO-01`, which is consistent with this ruling and needs no edit.
- `GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024` (PR #640) should merge: its measurement is correct and its refusal to rule was the right call. Its §4 "specificity" reading is superseded by §2 above, which does not rely on specificity.

## 7. What this ruling does not decide

- Whether `Placeholder` should eventually be rejected at publication. That is `B-P2-XO-01`, still `PENDING CROSS-OWNER DECISION`, and this ruling deliberately leaves it open.
- The authenticity of any `Issued` value. Same owner, same reason.
- The `CanonicalCommitRef` regression's cause. #634 may have branched from a tree where it was still a unit struct; the cause is a rebase problem, and the fix is a rebase, not a decision.

## 8. Authority

Issued under the standing instruction to act as any owner when a ruling is required and no human will supply one, and under the one constraint that binds it: **no code is written by the ruling session.** Everything above is measurement of merged text plus an interpretation of one document's own sentences. Steps 1–5 are a work order for the implementing session, not an implementation.
