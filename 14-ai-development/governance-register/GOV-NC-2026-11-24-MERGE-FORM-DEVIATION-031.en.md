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
      last_verification_note: "Every SHA, parent count, timestamp and API response body in this record was read from the GitHub REST API or from git in this session. No figure is carried over from another register. The record states one limit explicitly: the evidence cannot establish why the merged commit's shape differs from the requested merge_method."
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
# GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031 — PR #875 landed as a squash while a merge commit was requested

**Status**: `OPEN` / `RECORDED`
**Defect class**: Governance Conformance — insufficient verification of the merge result
**Severity**: Low (no content deviation; the commit-graph shape differs from the request)
**Measured at**: `main = a8c367d`
**Related**: `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.4. The historical correction in §13.4 is not the subject of this record and is left exactly as it stands.

---

## 0. In one sentence

PR #875 landed with the approved content, but the form it landed in does not match the merge method I requested — and I did not confirm the actual commit shape before issuing the merge request. **This is an operational verification defect, not a content defect.** This record does not revoke the content; it leaves the form deviation behind as an auditable fact.

---

## 1. Deviation statement (Owner-supplied wording, verbatim in the original)

The ruling of record is written in Chinese in the counterpart file. Its content, rendered:

> The request specified `merge_method=merge`, but the merge commit finally observed has the single-parent squash shape. That commit already existed on main before the merge API request; the API request then returned the same SHA. The request and the final commit shape are inconsistent, and the causal relation between the request and the creation of the commit cannot be established from the available evidence. The operator did not confirm the actual commit shape before issuing the request, which is insufficient verification of the merge result.

Three boundaries attach to that wording and must not be relaxed when it is cited later:

1. **It does not claim GitHub ignored `merge_method`.** All three merge methods are enabled on the repository (`allow_merge_commit: true`, `allow_squash_merge: true`, `allow_rebase_merge: true`). The API had no stated reason to override the request, but there is also no evidence that it did.
2. **It does not claim the PUT created the commit.** The SHA the request returned was already the tip of `main` before the request was sent.
3. **It does not guess at another actor that triggered the merge.** Every relevant event is attributed to `oahcom` in the API. A distinction the API cannot make is recorded as a distinction that cannot be made.

---

## 2. Measured evidence

### 2.1 Request parameters

```
PUT /repos/oahcom/AiMemoryBrainArchitecture/pulls/875/merge
{"merge_method":"merge","sha":"c10ebdc4663bca289d64826883f4723664180d52"}
```

### 2.2 API responses

```
attempt 1: 422  "11 of 11 required status checks are expected."
attempt 2: 422  "Head branch was modified. Review and try the merge again."
attempt 3: 200  {"merged": true, "sha": "a8c367def34e5a3082ab777a7afedf7e82f38aa0",
                 "message": "Pull Request successfully merged"}
```

### 2.3 Shape of the landed commit

```
git rev-list --parents -n 1 a8c367d
a8c367def34e5a3082ab777a7afedf7e82f38aa0 8dada462b53ba6fd24e5775dcc761fc3528288c2
                                       ^ single parent -> squash, not a two-parent merge commit

subject: docs(register): record the #707 review-source correction in §13.4
```

### 2.4 Timing that matters (raw `issues/875/timeline` and `pulls/875` output)

| Time (UTC) | Event | Actor | Object |
|---|---|---|---|
| 2026-11-24T04:36:28Z | `head_ref_force_pushed` | oahcom | my rebase, `cfe0e7d -> 340167c` |
| 2026-11-24T04:43:58Z | `head_ref_force_pushed` | oahcom | my rebase, `c1d5381 -> 340167c` line |
| — | `committed` | — | `340167c` |
| — | `committed` | — | `4b64dcb` (GitHub Update branch, not created by me) |
| — | `committed` | — | `c10ebdc` (GitHub Update branch, not created by me) |
| 2026-11-24T04:54:07Z | `merged` | oahcom | `a8c367d` |
| 2026-11-24T04:54:07Z | `closed` | oahcom | — |

`a8c367d` was already the tip of `main` before I issued the third PUT. That is the direct basis for the finding that the causal relation cannot be established.

### 2.5 Content unaffected

| Check | Result |
|---|---|
| `GOV-NC-…-003.md` sha256 at `main` | `2cd88b58b29c9080be52c41f49db99aa7544fa76bcb0cafff25adca188a9a1d1` |
| `GOV-NC-…-003.en.md` sha256 at `main` | `ca43112043a3944bb9e3f39b1323ddd39c9a2c823c756a8636222053854b77c7` |
| `diff 8dada46..a8c367d` | `53 0` / `53 0`, no deletions |
| The same sha256 pair at approval time (`c1d5381`, `340167c`, `4b64dcb`, `c10ebdc`) | identical at every head |

Conclusion: the content is byte-identical to what was approved. The deviation exists only between the commit-graph shape and the requested form.

---

## 3. Follow-on record of the zero-formal-review instance

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/875/reviews` -> `[]`.

Per the Owner's ruling:

> Post-freeze observed instances: PR #875 — 2026-11-24 — 0 formal reviews.

**The frozen historical count in `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 must not be rewritten or extended.** The frozen count represents the historical observation range it originally defined; adding later instances to that number would change the statistical basis and the historical baseline. This record appends one line after it and leaves the original number untouched.

### 3.0 Three endpoints, three different things

Every table in this section asks the same question: was this merge reviewed. Asking the wrong endpoint returns a constant that looks like evidence, so what each endpoint measures is stated first:

| Endpoint | Measures | Does not contain |
|---|---|---|
| `GET /pulls/{n}/reviews` | **Formal review submissions** — the `APPROVE` / `REQUEST_CHANGES` / `COMMENT` actions that occupy the "Files changed" review pane | Anything said in the conversation thread |
| `GET /pulls/{n}/comments` | **Inline diff comments** — comments attached to a line of the patch | The conversation thread, formal review state |
| `GET /issues/{n}/comments` | **The conversation thread** — the PR discussion, in time order | Formal review state, inline comments |

Two zeros side by side read as mutual corroboration, and can be the same absence counted twice — which is what `#966` shows happened here. The six instances below are therefore measured on all three endpoints, and formal reviews are recorded separately from reviews written in the conversation thread instead of being merged into a single `0`.

### 3.1 Follow-on instance (two): PR #890

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890/reviews` -> `[]`.

> Post-freeze observed instances: PR #890 — 2026-11-24 — 0 formal reviews.

Verified evidence, read item by item when this entry was added. No figure is carried over from another register:

| Item | Endpoint | Field | Value as returned |
|---|---|---|---|
| Formal reviews | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890/reviews` | array length | `0` records |
| Conversation comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/890/comments` | array length | `0` records |
| Merge time | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/890` | `merged_at` | `2026-11-24T05:39:10Z` |
| Merging account | same record | `merged_by.login` | `oahcom` |
| Merge commit | same record | `merge_commit_sha` | `0f32d46c34cb086e52de38fa49b33ca8a3bf5cd3` |
| Inline review comments | same record | `review_comments` | `0` |
| Commits / additions / deletions | same record | `commits` / `additions` / `deletions` | `1` / `306` / `0` |
| Title | same record | `title` | `docs(register): record the #875 merge-form deviation` |

The two timestamps are labelled by source and are not interchanged:

| Event | Time | Source of the time |
|---|---|---|
| This session ruled that no merge authorisation was granted | no later than `2026-11-24T05:36:33Z` (`13:36:33 +0800`) | Local modification time of the file holding the ruling text. **This is not** a platform-issued timestamp. It is used only to establish ordering inside this session, and it is not used as evidence about the merge itself. |
| #890 merged | `2026-11-24T05:39:10Z` | GitHub REST API `merged_at` |

The two are at most 2 minutes 37 seconds apart. The times are used to establish order only. The time of one event is not used to prove that another event did or did not happen.

What this record states: **#890 was merged after this session had explicitly withheld merge authorisation, and it was merged with zero formal reviews.** This is a documented governance-control failure, not merely an unenforced policy.

What this record does not state: no attribution of `merged_by: oahcom` to a particular natural person. That field identifies a GitHub account, not necessarily the person operating it.

### 3.2 Follow-on instance (three): PR #896

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896/reviews` -> `[]`.

> Post-freeze observed instances: PR #896 — 2026-11-24 — 0 formal reviews.

| Item | Endpoint | Field | Value as returned |
|---|---|---|---|
| Formal reviews | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896/reviews` | array length | `0` records |
| Conversation comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/896/comments` | array length | `0` records |
| Merge time | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896` | `merged_at` | `2026-11-24T06:51:52Z` |
| Merging account | same record | `merged_by.login` | `oahcom` |
| Merge commit | same record | `merge_commit_sha` | `84bbe9241aef748b406a969da321e7d3fcda2dc1` |
| Commits / additions / deletions | same record | `commits` / `additions` / `deletions` | `1` / `335` / `1` |
| Head at merge | same record | `head.sha` | `5585d95ffd5705fe7a636f475b295162737585e9` |

**This subsection records one measurable state. It records no causation and no attribution.**

- Established: at merge time the formal-review record for this PR was `0` records.
  `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/896/reviews` returned `[]`.

**Two things that must be kept apart: event time and the time a rule took effect.** An earlier draft
of this subsection said "the D1 requirement therefore did not exist at that moment". That was wrong
and has been corrected. The accurate statement is:

> PR #896 was merged at `2026-11-24T06:51:52Z` and the formal-review API returned `[]`. The merge
> precedes the persistence of the Round 22 ruling that withheld merge authorisation for #896, so it
> cannot be treated as a violation of that Round 22 ruling. But the D1 formal-review requirement was
> issued in Round 20; this zero-review merge is still inconsistent with that pre-existing requirement.
> The available evidence does not support further attribution to a specific operator.

That is: **D1 was already in force before the merge, so the requirement did exist at merge time — it
was simply not satisfied.** It cannot be said that the requirement did not exist then. Nor can the
merge be back-dated into a violation of the Round 22 withholding, whose text had not yet been
persisted. Both time boundaries are preserved.

- Not established: the ordering of this merge against any ruling. The text of the ruling on #896 was persisted in this session at `2026-11-24T06:53:07Z` (`14:53:07 +0800`; again a local file modification time, not a platform timestamp), which is about 75 seconds after the merge at `2026-11-24T06:51:52Z`.

This subsection therefore does **not** say "merged in violation of a ruling". Writing an event of unknown order as an out-of-order event would contradict `OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001` directly. It records one fact only: **after D1 had been established, another merge occurred with zero formal reviews at merge time.** Whether this merge constituted a violation of a specific ruling is a question that requires the platform-side event sequence, and this record does not answer it.

### 3.3 Follow-on instance (four): PR #927

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927/reviews` -> `[]`.

> Post-freeze observed instances: PR #927 — 2026-11-24 — 0 formal reviews.

| Item | Endpoint | Field | Value as returned |
|---|---|---|---|
| Formal reviews | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927/reviews` | array length | `0` records |
| Conversation comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/927/comments` | array length | `1` records |
| Merge time | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/927` | `merged_at` | `2026-11-24T10:38:00Z` |
| Merging account | same record | `merged_by.login` | `oahcom` |
| Merge commit | same record | `merge_commit_sha` | `b3a65e54b0b0380430cc4cf8b187d3e0c9edb7a3` |
| Commits / additions / deletions | same record | `commits` / `additions` / `deletions` | `2` / `462` / `0` |
| Head at merge | same record | `head.sha` | `5e0a93d6301a7b04b1ee5e1a3031ece1068c1dfa` |

The same boundary applies as in §3.2: D1 was in force before this merge, so the formal-review
requirement existed at merge time and was not satisfied. This record does not infer an operator from
it, and does not turn "this session granted no merge authorisation" into "someone violated an
authorisation". This session's handling of that PR was: request a content review, and do not call the
merge endpoint.

**The conversation thread holds one review, written after the merge.** `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/927/comments` -> `1` record, `created_at` `2026-11-24T11:16:18Z`, 38 minutes after `merged_at` `10:38:00Z`. Its first line is `## Ruling 86 — #927's classification reconciles exactly; the manifest is sound and should merge`.

The accurate statement for this instance is therefore not "zero review" but **`0` formal reviews, `1` post-merge review**. Both instants come from the same API (`issues/{n}/comments.created_at` and `pulls/{n}.merged_at`), so the `+38` needs no local clock and the prohibition in `OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001` does not reach it. The review was written after the merge; it did not, and could not, gate it.

### 3.4 Follow-on instance (five): PR #933

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/933/reviews` -> `[]`.

> Post-freeze observed instances: PR #933 — 2026-11-24 — 0 formal reviews.

| Item | Endpoint | Field | Value as returned |
|---|---|---|---|
| Formal reviews | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/933/reviews` | array length | `0` records |
| Conversation comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/933/comments` | array length | `0` records |
| Merge time | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/933` | `merged_at` | `2026-11-24T11:34:23Z` |
| Merging account | same record | `merged_by.login` | `oahcom` |
| Merge commit | same record | `merge_commit_sha` | `3235db07f23cb272da7460147e2f80413e68e555` |
| Commits / additions / deletions | same record | `commits` / `additions` / `deletions` | `2` / `143` / `1` |
| Head at merge | same record | `head.sha` | `4f4669fb7a81a09a15c6d91e590d9832e4d615bf` |

The same boundary applies as in §3.2. No operator is inferred.

### 3.5 Follow-on instance (six): PR #946 — an explicit refusal existed at merge time

The first five instances share one property: **the ordering is unknown**. The merge happened first, or
happened on a day where the platform fields cannot establish which came first. This one is different,
and so it gets its own subsection rather than a row in the previous table.

`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/reviews` -> `[]`.

> Post-freeze observed instances: PR #946 — 2026-11-24 — 0 formal reviews.

| Item | Endpoint | Field | Value as returned |
|---|---|---|---|
| Formal reviews | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/reviews` | array length | `0` records |
| Review comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946/comments` | array length | `0` records |
| Conversation comments | `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/946/comments` | array length | `1` records |
| Merge time | `GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/946` | `merged_at` | `2026-11-24T14:05:56Z` |
| Merging account | same record | `merged_by.login` | `oahcom` |
| Merge commit | same record | `merge_commit_sha` | `8e489ec1e18cd127088a695fa21121521e240514` |
| Commits / additions / deletions | same record | `commits` / `additions` / `deletions` | `10` / `547` / `7` |
| Head at merge | same record | `head.sha` | `600a562fbc52afc91ed0c7fcdadf684f9961e6c8` |

**Why this is not the same category as the previous five.** The text of the ruling that withheld merge
authorisation was persisted at `2026-11-24T13:20:27Z` (`21:20:27 +0800`; a local file modification
time, not a platform timestamp), roughly 45 minutes before the merge at `14:05:56Z`. So this is not
"merged before the ruling". It is: **the ruling existed, was on disk, said not to merge, and the merge
happened anyway.**

Two kinds of time have to be kept apart here, or the record ends up making a stronger claim instead of
a more accurate one:

| Time | Source | Value | What it can establish |
|---|---|---|---|
| Ruling persisted | local file mtime | `2026-11-24T13:20:27Z` | this session still held the text afterwards; not a platform timestamp |
| Merge | `pulls/946.merged_at` | `2026-11-24T14:05:56Z` | the merge instant GitHub recorded |

A local file mtime is not a platform timestamp (see `OWNER-DECISION-EVENT-TIMESTAMP-PROVENANCE-001`),
so that table alone cannot prove the ruling took effect before the merge on the platform side. But this
subsection does not rest on the difference between two timestamps. It rests on a content-level
correspondence: **the ruling names the very PR that was merged**, and that text had been read in this
session before the merge, with instructions issued from it: `保留 PR #946，不执行合并。` ("Keep PR #946;
do not merge it.") That correspondence does not depend on a clock.

This session's handling of #946: create the PR, push the branch, commit documentation — and **do not
call the merge endpoint**. `oahcom` is recorded only as a GitHub account. As with the previous five,
this record does not judge who triggered the merge.

**Ninety minutes after the merge, one approval appears in the same PR's conversation thread.** `GET /repos/oahcom/AiMemoryBrainArchitecture/issues/946/comments` -> `1` record, `created_at` `2026-11-24T15:36:10Z`, 90 minutes after the merge at `14:05:56Z`. Its first line is `## Owner review — approved. The arithmetic reconciles, and the mutation is a genuine bound`.

That approval is not in `pulls/946/reviews`: it is not a formal review submission but a comment in the conversation thread. Both instants are platform timestamps, so the `+90` minutes needs no local clock.

**It does not retract this subsection's refusal finding; the two stand side by side.** An "approved / Merge it" written ninety minutes after the merge is a **ratification** of a merge that had already happened, not a **permission** for it — it did not, and could not, gate the merge. This subsection therefore records two facts, not one:

1. An explicit refusal already existed at merge time (above; establishable from content).
2. A ratifying approval appeared 90 minutes after the merge (this paragraph; establishable from platform timestamps).

Writing the second as a mitigation of the first would quietly convert "the merge happened after an explicit refusal" into "somebody approved it later". The second neither mitigates nor aggravates; it only makes "zero review" an inaccurate description. The accurate one is: **`0` formal reviews, `1` post-merge ratification.**

### 3.6 Sequence summary (the frozen §13.7 count is not rewritten)

| # | PR | Merge time (UTC) | Formal reviews | Conversation | Difference from the preceding |
|---|---|---|---:|---|---|
| one | #875 | `2026-11-24T04:54:07Z` | 0 | 0 | form deviation, content approved |
| two | #890 | `2026-11-24T05:39:10Z` | 0 | 0 | ordering unknown |
| three | #896 | `2026-11-24T06:51:52Z` | 0 | 0 | ordering unknown (ruling 75 s after merge) |
| four | #927 | `2026-11-24T10:38:00Z` | 0 | 1 (merge +38 min) | ordering unknown |
| five | #933 | `2026-11-24T11:34:23Z` | 0 | 0 | ordering unknown |
| six | #946 | `2026-11-24T14:05:56Z` | 0 | 1 (merge +90 min) | **an explicit refusal already existed** |

The frozen count in `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` §13.7 keeps its original value and is
not changed by appending to this table. This table is a follow-on observation list, not a revision of
the original statistical scope. The added Conversation column does not change it either: that column widens the **dimensions of the observed instance list**, not the base of the historical statistic.

---

## 4. Judgements deliberately not made

- No judgement about who triggered the merge, or whether more than one actor was involved.
- No judgement about whether GitHub should have produced a merge commit.
- The squash shape is not itself treated as a governance defect. A single-parent commit reduces traceability, but the content matches the approval; recording it as a content defect would be a different false statement.
- No claim that this record constitutes a re-approval of #875, and no change to any existing approval state.
- No retroactive exception is requested for this deviation.

---

## 5. Actionable lesson (exactly one)

After a merge request returns success, verify **the landed commit's parent count and subject**, not only the HTTP status and `merged: true`. That check was not performed here, so "the merge succeeded" was read as "the merge succeeded in the requested form". Those are not the same claim. The lesson applies to any merge issued with an explicit `merge_method`.
