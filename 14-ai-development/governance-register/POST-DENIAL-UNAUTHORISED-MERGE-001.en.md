---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every field in section 2 was read from the GitHub REST API in this session, and the endpoint is named beside each value. The one non-platform timestamp (the ruling's persistence time) is labelled as a local file modification time and is not used to order the two events; section 4 explains why the finding does not depend on it."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# POST-DENIAL-UNAUTHORISED-MERGE-001 — #946 merged after an explicit refusal

**Event type:** governance control failure, not an ordinary record of a missing approval.

**Conclusion:** the implementation in PR #946 passed technical acceptance and is retained; its merge was not authorised, and it happened after a refusal that named that PR. The two must be recorded separately: correct content does not retroactively authorise the merge, and an unauthorised merge does not invalidate the content.

---

## 1. Why this record stands alone

`GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.1–§3.5 records six zero-formal-review merges. All six share one property: **the ordering cannot be determined** from the platform fields — the merge came first, or both fell on a day where the fields cannot say which preceded which. That register therefore states only "zero formal reviews at merge time", and does not state "merged in violation of a ruling".

This event is not in that sequence. The refusal already existed, was persisted, and **named the very PR that merged**. Folding it into "ordering unknown" would erase the only distinction it has, so it gets its own record.

---

## 2. Platform fields

| Item | Endpoint | Field | Value as returned |
|---|---|---|---|
| Merge time | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946` | `merged_at` | `2026-11-24T14:05:56Z` |
| Merging account | same | `merged_by.login` | `oahcom` |
| Merge commit | same | `merge_commit_sha` | `8e489ec1e18cd127088a695fa21121521e240514` |
| Formal reviews | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/reviews` | array length | `0` |
| Review comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/comments` | array length | `0` |
| Commits / additions / deletions | `pulls/946` | `commits` / `additions` / `deletions` | `10` / `547` / `7` |
| Head at merge | `pulls/946` | `head.sha` | `600a562fbc52afc91ed0c7fcdadf684f9961e6c8` |
| PR title | `pulls/946` | `title` | feat(hygiene): admit the ten Owner-ruled A/B shapes, and nothing else |

## 3. The refusal

The ruling's wording about that PR, verbatim:

> 保留 PR #946，不执行合并。 ("Keep PR #946; do not merge it.")

The same ruling also states:

> **本轮裁定的是准入政策，不是合并授权。** ("This ruling governs admission policy, not merge authorisation.")

Persisted at `2026-11-24T13:20:27Z` (local file modification time, `21:20:27 +0800`).

## 4. Why this finding does not rest on subtracting two clocks

"Refused 45 minutes before the merge" would have been the easy sentence. That 45 minutes is a **local file mtime minus a platform timestamp**, and `OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001` says directly that a local mtime is not a platform timestamp. Using it would produce a stronger claim that violates the provenance rule.

This record uses evidence that does not depend on a clock:

1. The refusal text **names `#946`**, and `#946` is the object that merged. A correspondence between a document and the object it names is content-level and needs no clock comparison.
2. That text had been read in this session before the merge, and instructions were issued from it: keep the PR, do not merge, close D3, persist the acceptance evidence.
3. What is therefore established: **the refusal exists, it is specific to that PR, and this session held it before the merge.** What is not established: the precise platform-side ordering of the ruling taking effect against the merge instant. This record does not claim that.

Put differently: this record claims "a refusal naming that PR existed", not "the refusal took effect on the platform 45 minutes before the merge".

## 5. Relationship to authorisation state

| Object | Status |
|---|---|
| #946 code content | ACCEPTED / RETAINED |
| #946 merge authorisation | NOT AUTHORISED |
| The merge that occurred | UNAUTHORISED MERGE |
| `main` after the merge | retained as-is, no rollback |
| Historical audit record | must not be rewritten as a normal merge |

Why the content is retained: the A/B rules passed technical acceptance, AC8 measured 83 admitted / 30 refused, AC9 closes at `74 + 4 + 19 + 16 = 113`, and a rollback would destroy an accepted implementation without repairing the approval mechanism.

Why it is not retroactively authorised: technically correct is not the same as authorised. If "the content is right" implied "the merge was legitimate", D1 would be a content-review rule rather than a merge control.

> The implementation was technically accepted, but its merge was explicitly not authorised. Subsequent incorporation into main does not constitute retrospective authorisation.

## 6. Judgements deliberately not made

- **No operator is identified.** `oahcom` is a GitHub account, not a natural person. No identity, intent or responsibility is inferred from `merged_by.login`.
- **Not written as a proven malicious bypass.** The platform record can establish that an unauthorised merge occurred. It cannot establish motive.
- **No claim that this session's non-participation proves innocence.** This session's writes to #946 were: create the PR, push the branch, commit documentation. It did not call the merge endpoint. That is a factual statement about this session, not a defence against an accusation nobody made.
- **The frozen count in `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 is not rewritten.**

## 7. Control-plane measurement (2026-11-24)

The root cause of the governance failure is not in this record but in the control plane itself. Measured the same day:

| Check | Endpoint | Result |
|---|---|---|
| `required_pull_request_reviews` | `GET /branches/main/protection` | **absent** |
| `enforce_admins` | same | `true` |
| `allow_force_pushes` | same | `false` |
| `required_status_checks.strict` | same | `true`, 12 contexts |
| Rulesets | `GET /rulesets` | `[]` |
| Collaborators | `GET /collaborators` | `oahcom` only (`push: true`) |
| `oahcom0831-design` permission | `GET /collaborators/oahcom0831-design/permission` | `read` |

Three consequences, stated as measurement rather than inference:

1. **No approval requirement exists**, so a zero-review merge is not blocked by the platform; it can only be recorded afterwards.
2. **A `read`-permission account cannot submit a formal Approved review**, so even with `required_pull_request_reviews` enabled, no second identity could satisfy it.
3. **`enforce_admins: true`** means any added restriction also binds the only write-capable account. Enabling the approval requirement before a second write-capable identity exists would freeze `main` in a state it cannot lift by itself.

Together these explain why "the file says it is forbidden" never became "the system prevents it".

### 7.1 Full-history census: the requirement has never once been met

The table above measures the control plane. This one measures the outcome over the entire repository history, because "how many merges recently skipped review" is a weaker question than "has review ever happened at all".

**Method.** `GET /pulls?state=closed&per_page=100` over every page → 775 closed PRs, of which 662 carry a non-null `merged_at`. `GET /pulls/{n}/reviews` was then fetched for all 662 — not sampled, and not limited to recent merges. Zero requests failed, so every merged PR is accounted for. Read `2026-11-24T18:47Z`.

| Quantity | Value |
|---|---|
| Closed PRs enumerated | 775 |
| Merged PRs (`merged_at` non-null) | 662 |
| Merged PRs measured (0 failures) | 662 |
| Merged PRs with ≥1 review object | 106 |
| Merged PRs with no review object at all | 556 |
| Review objects ever recorded | 170 |
| States those 170 objects carry | `{COMMENTED: 170}` |
| **Review objects with state `APPROVED`** | **0** |
| Accounts that authored any review object | `oahcom` (170 of 170) |

**A growing count, a stable invariant.** The table is a snapshot at `2026-11-24T18:47Z`. Merges continued: re-measured at `2026-11-24T20:35Z`, 676 PRs had merged and the 14 since the census all carried no review object. The merged count therefore moves every time this is read; `APPROVED = 0` has not moved once. The count is dated for that reason, and no figure here should be quoted without its measurement instant.

**Cross-check, independent of the enumeration.** `GET /search/issues?q=repo:oahcom/AiMemoryBrainArchitecture+review:approved+is:pr` returned `total_count: 0`, and the same query restricted to `is:merged` also returned `0`. A different endpoint, a different index, the same answer.

**What this establishes.** Not "seven merges skipped review". Not "enforcement recently failed". The state is that in 662 merged PRs the record contains **no formal approval at all** — every review object that exists is a `COMMENTED` state, which D1 explicitly excludes from counting as approval, and all 170 were written by the same account that authored the PRs. D1 has never been satisfied, in any period of this repository's history.

**What this does not establish.** It does not show that nobody ever reviewed the code, and it does not identify any person's intent. A `COMMENTED` review object is real review activity; what it is not is the record D1 requires. The finding is about the record, and about a control plane that was never configured to produce that record (`required_pull_request_reviews` is absent, §7).

**Why the count "seven" is not used here.** Earlier drafts of this record counted a subset of post-freeze merges. A subset count invites the reading that the problem is bounded and recent. The census is neither bounded nor recent, so it is the figure that governs.

---

## 8. Related records

- `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5 — the merge-form record for the same event.
- `OWNER-DECISION-REVIEW-INDEPENDENCE-001` — the policy basis for D1, with the full 690-PR measurement.
- `EX-20261123-01` — the only registered exception record.
- `AID-2026-057` — the work item whose implementation merged, including the AC8/AC9 acceptance evidence.
