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
