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
| `required_status_checks.strict` | same | `true`, 12 contexts (read 2026-11-24; re-read `2026-11-25T02:52Z` as 16, the four additions being `Session Evidence`, its two self-test contexts and `rust-workspace-test`) |
| Rulesets | `GET /rulesets` | `[]` |
| Collaborators | `GET /collaborators` | `oahcom` only (`push: true`) |
| `oahcom0831-design` permission | `GET /collaborators/oahcom0831-design/permission` | `read` |

Three consequences, stated as measurement rather than inference:

1. **No approval requirement exists**, so a zero-review merge is not blocked by the platform; it can only be recorded afterwards.
2. **A `read`-permission account cannot submit a formal Approved review**, so even with `required_pull_request_reviews` enabled, no second identity could satisfy it.
3. **`enforce_admins: true`** means any added restriction also binds the only write-capable account. Enabling the approval requirement before a second write-capable identity exists would freeze `main` in a state it cannot lift by itself.

Together these explain why "the file says it is forbidden" never became "the system prevents it".

### 7.1 Full-history census: 556 merges carry no review object at all

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

**What this establishes.** Not "seven merges skipped review". Not "enforcement recently failed". The finding is two numbers: of 662 merged PRs, **556 carry no review object at all** — not "no approval", but the review-submission path never walked even once — and the other 106 carry 170 objects, all `COMMENTED`. Review existed in form 106 times, and in 556 merges it did not exist in any form.

**`APPROVED = 0` is not a finding on the same level, and this record moves it out of the headline.** `GET /collaborators` returns `["oahcom"]`: exactly one collaborator. `GET /pulls?state=closed`, every page, returns 795 closed PRs, and `user.login` is `oahcom` for all of them (795 / 795). GitHub does not permit an account to approve a pull request it authored, so the number of `APPROVED` objects is not "currently zero" — it is **necessarily zero under this account topology, for every PR, forever, regardless of anyone's conduct**. Leading with it is reporting that a coin landed heads when the coin has one side: the number is true and carries no information.

D1's classification therefore changes. Not `ENFORCEMENT FAILURE` — that names a conduct defect and implies a fix in behaviour — but **`REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION`**, which names a specification defect and implies a fix in the rule. The earlier wording is preserved verbatim in `AID-2026-055`'s `status_history`, so the correction is auditable rather than overwritten. What independence can be expressed here is set out in §7.2.

> **This too was later split (2026-11-25, `AID-2026-055`).** As a *single* status, `REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION` welded the requirement to the formulation it replaced, and a reader taking it at face value concluded that independence itself was impossible here. What is impossible is the account-level form; the session-level form has always been available and was simply never recorded. What is recorded now is the two-part reading, in `current_status_parts` (`D1-a` = satisfiable, not satisfied; `D1-b` = necessarily zero, and not the requirement), while `current_status` itself is left verbatim with #1059's annotation scoping it to the account layer — because a record that edits its own claim is not a record. The paragraph above stands as written, because it is the record of that correction, not a statement about the present.

**What this does not establish.** It does not show that nobody ever reviewed the code, and it does not identify any person's intent. A `COMMENTED` review object is real review activity; what it is not is the record D1 requires. The finding is about the record, and about a control plane that was never configured to produce that record (`required_pull_request_reviews` is absent, §7).



**Why the count "seven" is not used here.** Earlier drafts of this record counted a subset of post-freeze merges. A subset count invites the reading that the problem is bounded and recent. The census is neither bounded nor recent, so it is the figure that governs.

### 7.2 The third endpoint: the conversation thread, and why "zero review" is itself inaccurate

§7.1 measured `pulls/{n}/reviews`. That is one of three endpoints, and it is the only one whose *approval* verdict is necessarily zero under this account topology. It is not empty: it carries 170 `COMMENTED` objects. What is necessarily zero is `APPROVED`, because the platform forbids self-approval. The three measure different things, and mixing them returns a constant that looks like evidence:

| Endpoint | Measures | Does not contain |
|---|---|---|
| `GET /pulls/{n}/reviews` | Formal review submissions (`APPROVE` / `REQUEST_CHANGES` / `COMMENT`) | Anything said in the conversation thread |
| `GET /pulls/{n}/comments` | Inline diff comments | The conversation thread, formal reviews |
| `GET /issues/{n}/comments` | The conversation thread (the PR discussion in time order) | Formal review state, inline comments |

`#966` establishes that the distinction is not pedantry. `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5 lists the two zeros from `pulls/946/reviews` and `pulls/946/comments` side by side, where they read as mutual corroboration while actually being one absence counted twice. The same PR's `issues/946/comments` returns `1` record, `created_at` `2026-11-24T15:36:10Z`, 90 minutes after the merge at `14:05:56Z`, first line `## Owner review — approved. The arithmetic reconciles, and the mutation is a genuine bound`.

**Third-endpoint measurement over the whole history.** Same enumeration as §7.1, read at `2026-11-25T00:36Z`:

| Quantity | Value |
|---|---|
| Closed PRs enumerated | 795 |
| Merged PRs (`merged_at` non-null) | 681 |
| All conversation comments in the repository (`GET /issues/comments`, every page) | 4577 |
| Authors of those comments | `{oahcom: 4577}` |
| Merged PRs with at least one conversation comment | 406 |
| Of those, with a comment **before** the merge | 317 |
| Of those, with a comment **after** the merge | 232 |
| Formal review objects (the §7.1 endpoint, extended to all 681 merged PRs) | 170, all `COMMENTED`, all authored by `oahcom` |
| Formal review objects in state `APPROVED` | **0** |

**So one sentence in §7.1 needs correcting, and D1's conclusion does not change.** (That classification was itself split into D1-a / D1-b on 2026-11-25; see the annotation in §7.1. "Does not change" here means D1 still stands and is not waived.) §7.1 measures only the formal-review endpoint, which invites the stronger reading "nobody ever looked", and that reading is false: 406 merged PRs have conversation comments, 317 of them before the merge. The accurate state is also the harder one to argue away:

> Review activity exists, and written review exists: 406 merged PRs carry a conversation comment, 317 of them written before the merge. But all 4,577 comments and all 170 review objects were written by one account, that account authored all 795 closed PRs, and GitHub does not permit it to approve its own pull requests.

So the question is not "did anyone review", and not "was the reviewer good enough". It is this: **defining independence as "a second GitHub account appears" is a specification defect that cannot be satisfied under this topology.**

That is not lowering the standard. It is moving the standard to the dimension this repository can express. `#935` already supplied the answer: **independence is a property of the reviewing session, not of the GitHub account.** D1 must therefore be restated in a form GitHub can express — a required status check, produced by a check run, asserting a non-authoring reviewing session. A status check needs no second account, and that is exactly how `#704` turned doctests into a gate and how `#965` is turning session evidence into one.

The converse must be stated as well: **`required_pull_request_reviews` can never be satisfied here, and must not be added.** Turning it on does not make `main` safer; it makes the next merge attempt impossible, because it requires an object this account topology cannot produce. §7 records it as absent — that is a statement of fact, not a repair instruction, and a later session that reads it as one will freeze the repository.

**This does not retract the refusal finding in §3.** A ratifying approval written 90 minutes after the merge ratifies a merge that already happened; it is not a permission for it, and it neither mitigates nor aggravates the existing refusal. The two are recorded side by side in `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5.

**This does not change the frozen basis in §7.1.** The historical count in `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 keeps its original value; this section widens the observed dimension, not the statistical base.

---

## 8. Related records

- `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3.5 — the merge-form record for the same event.
- `OWNER-DECISION-REVIEW-INDEPENDENCE-001` — the policy basis for D1, with the full 690-PR measurement.
- `#966` — the Owner ruling on `GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031` §3: the three endpoints measure different things, and a post-merge review in the conversation thread must be recorded separately from a formal review. §7.2 is the result of applying it.
- `EX-20261123-01` — the only registered exception record.
- `AID-2026-057` — the work item whose implementation merged, including the AC8/AC9 acceptance evidence.
