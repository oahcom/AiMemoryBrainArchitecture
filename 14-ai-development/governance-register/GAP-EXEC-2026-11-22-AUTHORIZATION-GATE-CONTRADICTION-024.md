---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: docs/zh-CN/14-ai-development/governance-register/GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024.md
---

# GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024 — Authorization gate contradiction between PR #623 and PR #634

**Status:** RESOLVED — historical conflict record. This document records a contradiction that existed at a past measurement point and the Owner ruling that closed it. It is not an open question list and it decides nothing on its own authority.

- **Measurement point:** `main` = `f34d96a92975bb4e42e8b3121e345963ea4b7ab2`
- **Registration:** recorded in PR #640 before `2026-11-22T07:30:33Z`; the Owner ruling followed approximately eight minutes later.
- **Author identity:** written by a coordinating session acting as scribe for this record. That session is **not** an independent reviewer of #623 or #634, and is **not** the accountable owner of either change.
- **Resolution:**
  - Issue #347, comment `7075955802`, `2026-11-22T07:30:33Z`
  - Issue #595, comment `7076098820`, `2026-11-22T07:45:02Z` (formal Owner scope amendment)
- **Superseded framing:** the earlier text of this register presented three questions "that only the Owner can answer" and explicitly declined to adjudicate them. Those questions have been answered; §3 records the answer, §5 records what remains outside this record.

---

## 1. What this record is

This is a **historical conflict record**. It preserves, for audit purposes, the exact shape of a semantic contradiction that two open pull requests introduced into the same contract, together with the ruling that resolved it and the consequences that followed from that ruling.

It is retained rather than deleted because the contradiction was invisible to tooling: both pull requests merged cleanly against their respective bases, and neither CI nor any merge conflict surfaced the disagreement. A future reader who finds #623 and #634 in history, or who re-derives the same three-state authorization model, needs the record of why the two positions were not both admissible and which one the Owner selected.

This document is Informative and Non-Canonical. The binding text is the Owner ruling cited above and in §3; where this record and the ruling differ, the ruling controls.

## 2. The conflict as it stood

Both pull requests changed the semantics of a single field, `FactRevision::authorization_decision_ref`, and asserted mutually exclusive invariants about it.

| Aspect | PR #623 | PR #634 |
| --- | --- | --- |
| Opened | `2026-11-22T06:30:31Z` | `2026-11-22T06:59:28Z` |
| Base commit at registration | `87f54bb4` | `85504756` |
| Size at registration (files / lines) | 2 files, +522 / −44 | 2 files, +214 / −64 |
| Field type of `authorization_decision_ref` | presence-layer rejection: a pending reference is treated as inadmissible, and `Placeholder` does not survive `FactRevision::validate()` | three-state presence gate: `Absent` / `Placeholder` / `Issued`, with `Placeholder` passing `FactRevision::validate()` |
| `dm2_06` assertion | `Pending` → `Err` | `Absent` and `Placeholder` behaviour asserted at the presence layer |
| Cites | earlier I decision, §4.3 and §6.4 | `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4 |

The figures above are the values **at registration time**, which is the moment this record describes. Both pull requests have since been rebased and both are still open, so their current bases and sizes differ from these cells; the live values are not restated here, because a record of a past conflict must not silently track moving inputs. Re-read the pull requests for current values.

The frontmatter carries `verification_status: Unverified` because the ruling text has not been re-verified against a later revision of either cited decision.

### 2.1 Retained quotation — the earlier I decision

Two fragments of the earlier I decision are load-bearing for this conflict, because #623 cited them:

- §4.3: `dm2_06` must test `Pending` → `Err`.
- §6.4: structured `FactRevision::validate()` rejects pending evidence.

These fragments are reproduced as they were carried into the conflict. The surrounding text of the earlier I decision is **not** reproduced here in full; it is retained by reference, and its operative reading is now governed by `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4 as described in §3.

### 2.2 Excerpt carried from the conflict — #623's presence-layer predicate

```rust
// Verbatim from PR #623's `FactRevision::validate()`, as carried in the
// superseded register.
if self.authorization_decision_ref.is_pending() {
    // ponytail: reuses EmptyRequiredField to avoid a new variant this round;
    // rename when the variant set is next revised.
    return Err(DomainError::EmptyRequiredField("authorization_decision_ref"));
}
```

The predicate is quoted only to show the mechanism by which #623 collapsed "not yet issued" into "not admissible". It is not normative and it is not an endorsement.

### 2.3 Why this was not a merge conflict

1. The two pull requests touched different regions of the same contract, so git merged both without a textual conflict.
2. The disagreement was semantic, not textual: it concerned which invariant the field is supposed to uphold, not which lines survive.
3. Both branches could therefore merge green, in either order, and still leave the repository with two mutually exclusive readings of one field.
4. No CI job, linter, or review bot in the current pipeline compares invariants across open pull requests, so nothing surfaced the contradiction automatically. It was found by reading the two diffs against each other.

## 3. The ruling

The Owner ruling is recorded at Issue #347 comment `7075955802` (`2026-11-22T07:30:33Z`) and restated as a formal scope amendment at Issue #595 comment `7076098820` (`2026-11-22T07:45:02Z`). The operative points, quoted:

> The later `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` (§§3–4) is the **controlling refinement** of the earlier I decision's use of `dm2_06`.

Two questions were being conflated and must be separated:

1. **Existence (domain invariant).** `FactRevision.authorization_decision_state` distinguishes `Absent` / `Placeholder` / `Issued`. `FactRevision::validate()` rejects `Absent` only when `outcome == Attested`; `Placeholder` passes.
2. **Authenticity and durable authority (I validator).** `AuthorizationDecisionRef::Pending` is not authority. The AdmissionStore-backed `validate_authorization_decision()` must return `Err` for Pending, for a missing row, for a malformed row, and for a mismatched reference; `validate_attestor()` must independently reject pending, missing, or corrupt attestor evidence. Only a matching durable record with `decision_kind == Approved` satisfies the unconditional authorization requirement.

Consequences of the ruling, quoted or closely paraphrased from the same two comments:

- The earlier I decision's §4.3 requirement — `dm2_06` must test `Pending` → `Err` — is **retained**, but **reassigned** to a separate I validator test, for example `authorization_validator_rejects_pending_reference` or `validate_authorization_decision_rejects_pending_reference`. It is no longer part of `dm2_06`'s semantics.
- The §6.4 statement is **narrowed**: pending evidence is rejected by the I publication-authority validator before a successful publication, not by the presence-only `FactRevision::validate()`.
- `#634 must preserve the three-state presence gate and dm2_06 absent/placeholder assertions.`
- `#623 must not make FactRevision::validate() reject Placeholder.`
- No fourth state is introduced. The state set remains `Absent` / `Placeholder` / `Issued`.
- The ruling does not grant production cryptographic authority. The dev-baseline `i-owner-proxy/dev-baseline-v1` remains the logical trust anchor; production signing and key custody remain OUT-OF-SCOPE.

In one line: **presence is a three-state question answered by the domain type; authority is a durability question answered by the validator.** #623 answered the second question at the first question's layer; #634 kept the layers separate. The Owner kept the separation.

## 4. What changed in consequence

- **PR #634** is required to preserve the three-state presence gate and the `dm2_06` absent/placeholder assertions. Its presence layer stands as written.
- **PR #623** must not make `FactRevision::validate()` reject `Placeholder`. Its presence-layer rejection of pending references is not admissible as a domain invariant; the rejection it wants belongs in the I validator.
- **New test obligation:** a dedicated I validator test must assert `Pending` → `Err` (naming examples in §3). This is the surviving home of the earlier I decision §4.3 requirement.
- **`dm2_06`** no longer carries the pending-rejection semantics. It asserts presence behaviour only: `Absent` under a non-`Attested` outcome, and `Placeholder` passing validation.
- **This register** is reclassified from an open question list to a resolved historical record (this document).

## 5. What this record does not decide

- It does **not** decide whether #623 or #634 may be merged, in what order, or under what review conditions. Merge disposition is the Owner's, and is not recorded here.
- It does **not** constitute an independent review of either pull request. The session that produced this record is the coordinating session; see §6.
- It does **not** grant production cryptographic authority, and it does not alter the OUT-OF-SCOPE status of production signing and key custody.
- It does **not** re-open the ruling. If a future change contradicts `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` §§3–4, the correct action is a new Owner decision, not an edit to this record.
- It does **not** assert the **current** open dates, sizes, or base commits of #623 and #634. The cells in §2 are the values at registration time; both branches have since been rebased.

## 6. Authority and independence disclosure

This record is written by a coordinating session. Disclosure obligations that apply, and that this record states rather than argues around:

- **Owner role may be held by the same session.** Per #305 §2 (delegation instrument `7042461592`), the Owner role is not bound to a distinct session; a session that wrote a change may also make an Owner disposition on it.
- **But that disposition may not be presented as independent review.** Per #305 §4, a representative must not be the sole reviewer of their own implementation and must not characterise that review as independent. This is a **disclosure obligation, not a merge prohibition**: where independence cannot be established, the correct action is to record `INDEPENDENCE_UNVERIFIABLE` and continue, not to halt.
- **This record's author therefore claims no independence.** The author is not the accountable owner of #623 or #634, and does not assert independent review of either. Where the ruling above is quoted, it is quoted as the Owner's text, not as the author's judgement.
- **Prompt-pair independence is unverified.** The governance baseline requires independence to be established by **different sessions and different prompts**. A difference in GitHub author is not sufficient evidence of either. The paired session identifiers and the prompt version or hash for the sessions that produced #623 and #634 are **not recorded** in this document, and the earlier claim that the two pull requests were written by two different sessions is withdrawn as unsupported. Status: `INDEPENDENCE_UNVERIFIABLE` — prompt-pair independence not verified.
- **What would close it:** recording, for each of #623 and #634, the session identifier and the prompt version or hash, so that session distinctness and prompt distinctness can be checked rather than assumed.

---

Documentation only. No source code is changed by this record.
