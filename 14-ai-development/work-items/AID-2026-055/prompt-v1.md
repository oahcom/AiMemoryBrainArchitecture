---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure in §1 was read from the GitHub REST API at main a8c367d in this session: the protection object, both reviews endpoints, the #875 merge record, and the repository merge-method flags. No figure is carried over from another document."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-055 — require formal review on main, and prove it by being refused

**Work item:** `AID-2026-055`
**Class / risk:** `GATE/CONFIG/TEST` / `R2`
**Status:** `DISPATCHED`
**Measured at:** `main = a8c367d`

---

## 1. Why this exists, in measurements

Read from the API, not inferred:

```
GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection
  required_pull_request_reviews  : null          <- absent
  required_status_checks.strict  : true
  required_status_checks.contexts: 11
  enforce_admins.enabled         : true
  allow_force_pushes.enabled     : false

GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/707/reviews  -> []
GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/875/reviews  -> []
```

Eleven required contexts, all green on #875, and the merge went through with zero
formal reviews. The check list is not a substitute for review, and this repository
demonstrates that twice in two days.

The distinction the record must keep: `reviews -> []` is an absence of formal review
records. `review_comments = 0` is an absence of inline review comments. They are
different endpoints and different claims. #875 had both zero; that is a coincidence,
not a definition.

## 2. The four decisions this work item implements

Issued by the Owner in round 20. These are rulings, not options.

| ID | Question | Ruling |
|---|---|---|
| D1 | Formal review required? | **Yes** — at least one `Approved` review from an account that is not the PR author. **Current status: REQUIRED, UNSATISFIED; ENFORCEMENT FAILURE** — see §3. |
| D2 | Code Owner review required? | **Yes**, scoped to CODEOWNERS-covered paths; must be verified as actually required, not merely that the file exists |
| D3 | Admins may bypass? | **No** — `enforce_admins.enabled` must be true and verified by read-back |
| D4 | How to verify? | Read the rule back from the API **and** run a zero-review negative test that GitHub refuses. Do not merge a non-compliant PR to test. |

## 3. The blocking finding, stated first

**F3 — no second accountable person is established.**

> D1 is a mandatory policy requirement, but is currently unsatisfiable because no second
> accountable human approver has been established. This is not a waiver, an optional
> recommendation, or evidence that review is unnecessary.
>
> D1 是强制政策要求，但由于目前尚未建立第二名问责人，现阶段无法满足。这不是豁免，不是可选建议，
> 也不表示审查没有必要。

The basis, measured: every action in this repository is attributed to one account, `oahcom` —
authoring, merging, and both zero-review merges; no record appoints a second maintainer,
independent reviewer or integration reviewer; and `pulls/875/reviews` and `pulls/890/reviews`
both return `[]`. This records that no second accountable person is established **for the
governance system to rely on**. It does not assert that no such person exists anywhere.

The implementer must not resolve this by:

- counting the author's own review as the independent approval;
- creating a second identity so the first can approve the second;
- lowering D1 to "review recommended";
- treating a ChatGPT review, a GitHub Actions identity, or any automated actor as the second human.

**The only legitimate path out of this state** is formally designating another real human
accountable person and recording their identity, duties, approval authority, and the mapping
to their GitHub account — after which it must also be verified that the person is not the PR
author and has authority to carry the approval.

Until then, AC1 can be configured and AC5 can be satisfied by a refusal — which is worth
having, because a refusal is the proof the requirement is live. AC4 cannot be satisfied by a
real approver.

## 4. Change order, because the order is load-bearing

Enabling required review with no available second approver makes `main` unmergeable,
including the PR that would fix it. Therefore:

1. Record the revert path **before** writing the setting.
2. Write the complete protection object, not a partial one. A PUT that omits
   `required_status_checks` replaces the object and silently drops all 11 contexts. AC3
   exists to catch exactly that.
3. Read the object back and diff it field by field against the "before" values in §1.
4. Run the negative test last, and confirm nothing merged.

## 5. Acceptance criteria

| ID | Criterion |
|---|---|
| AC1 | `GET /branches/main/protection` shows `required_pull_request_reviews.required_approving_review_count >= 1`, recorded with the raw response body |
| AC2 | Same response shows `dismiss_stale_reviews = true` and `enforce_admins.enabled = true`; a field the platform does not expose is recorded as not exposed, never as passing |
| AC3 | Required-check contexts still number 11 and `strict` is still true |
| AC4 | Either a CODEOWNERS-covered path is refused without Code Owner approval, or D2 is recorded `NOT_VERIFIABLE` with the reason — never reported as satisfied |
| AC5 | The negative test records a platform refusal verbatim: request, status, body, PR head SHA, required-check state. A client-side pre-check does not satisfy this |
| AC6 | No review is fabricated; the record names the account used and why it legitimately cannot self-approve |
| AC7 | The frozen zero-review count in `MERGE-AFTER-RULING-003` §13.7 is unchanged, verified by diff against `a8c367d` |

## 6. What this work item does not do

- It does not close Risk 2. Risk 2 closes only when the rule is configured, the API state is
  verified, and the negative test is refused. All three.
- It does not address direct pushes to `main`. `enforce_admins` governs the PR path; a direct
  push is a different vector and stays **OPEN** after this change.
- It does not change the required-check list, the frozen count, or any ownership mapping
  beyond what makes D2 testable.

## 7. Evidence to hand the implementer

The "before" object in §1 is the baseline for the required before/after table. It is stated
as raw values so the implementer can reproduce it rather than trust the conclusion. Both
zero-review instances are cited by endpoint, so either can be re-read at any time and will
still return the same thing: the record is a snapshot of a past observation, and past
observations do not expire.
