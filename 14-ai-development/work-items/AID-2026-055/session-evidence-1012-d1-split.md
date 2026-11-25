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
      last_verified_date: "2026-11-25"
      last_verification_note: "Every branch-protection number quoted here was read from GET /branches/main/protection during 2026-11-25. The claim that D1's single status string could not be read as the requirement was checked by reading both sides of the manifest at d82734b6, not by trusting a pull request description. The constraint that this session must not reverse a merged decision was checked by reading #1059's merged bytes before editing."
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

# Session evidence — recording D1 as two parts, without reversing what already merged

## Session role

CORRECTOR. This session changed no code and issued no new policy. It applied
repairs that earlier records had already specified and that had not been
executed: the `REQUEST CHANGES` ruling on #1013, issue #1012's closing
condition 2, and — after a first attempt was itself reviewed — the findings of
three independent reviews of that attempt.

## Actual AI input

The standing instruction, verbatim:

> 「你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理」

The specifications being applied, verbatim:

> `REQUEST CHANGES`。三项必须先解决：**B4**（manifest 同时禁止并认证同一次
> branch-protection 写入）、**B3**（`remediation` 与 `constraints` 互斥）、
> **B1**（两侧语言断言不同的事实）。**B2** 与 **B1/B3** 同源，一起改。**M1**
> 是独立的一段删除，恢复或在中英两侧同时声明删除。修完后 head 变了请 ping，
> 我按同样方式（逐句读两侧正文，不按清单比对）重跑一遍。

> closing condition 2: D1's status must have two named parts with two statuses.

## AI-visible output

What follows is the correction, stated as what was wrong before it is stated as what was done.
The first version of this change was reviewed by three independent sessions; two returned
`REQUEST CHANGES` and one returned `APPROVE` with four minor findings, and the checks below
are the record of acting on them rather than of agreeing with them.

### What the first attempt got wrong

The first version of this change renamed `current_status` from
`REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION` to a two-part string. Three
independent reviewers then found that the change had introduced the same class
of defect it existed to remove, and one of them found something the change
could not have known: **#1059 had already merged a different repair to the same
field while this branch was open.** It kept the value verbatim and appended an
annotation scoping it to the account layer, on the stated ground that *a record
that edits its own claim is not a record*.

Renaming the field would have reversed a merged decision. That is the exact
conduct this repository has spent a week recording (POST-DENIAL-UNAUTHORISED-MERGE-001),
so this session did not do it. `current_status` now carries #1059's bytes
unchanged, comment and annotation included.

### What is recorded instead

| item | before | after |
|---|---|---|
| two-part reading of D1 | existed only as prose inside a Chinese annotation on `current_status`, so no field stated which part governs | `current_status_parts`: two entries, `D1-a` = `SATISFIABLE, NOT SATISFIED` (the requirement), `D1-b` = `NECESSARILY ZERO, AND NOT THE REQUIREMENT` (the retired account-level form). `current_status` is untouched |
| `current_status_wording` / `_zh` | described D1 as a single unsatisfiable requirement | describes the two parts, and states that `current_status` is left verbatim because #1059's annotation already scopes it, and that `current_status_parts` is what a reader needs instead |
| `status_history` | one entry, `REQUIRED BUT CURRENTLY UNSATISFIABLE`, whose `superseded_by` named `REQUIRED, UNSATISFIED; ENFORCEMENT FAILURE` — a status that existed only as `constraints[0]`, so the chain did not resolve inside the list | two entries, newest first, resolving to `current_status` at the end — inside the list for the first link, and as the annotated current value for the last: `CURRENTLY UNSATISFIABLE` → `ENFORCEMENT FAILURE` → `REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION`. Every `superseded_by` resolves inside the list |
| `constraints[0]` | a `status`/`superseded_by`/`reason`/`evidence` mapping at index 0 of a list whose other eight items are plain strings — a retired status presented as the first live constraint | withdrawn from `constraints` and recorded as the second `status_history` entry; `constraints` is homogeneous and its first item states the live obligation |
| acceptance criterion AC2 | required `dismiss_stale_reviews = true` | excludes it. `dismiss_stale_reviews` is a subfield of `required_pull_request_reviews`, which this work item's own remediation forbids adding and which is absent from the live payload; requiring it made AC2 unsatisfiable by the same construction that made AC1's original form unsatisfiable |
| deliverable 2 | required the same field | withdrawn, with the withdrawal and its reason recorded in place rather than deleted |
| `prompt-v1.md` | pinned by `prompt_file` and by three `executed_prompt_sha256` values, and still stating the older formulation at lines 68, 77, 95 and 97 — with nothing marking it as superseded | unchanged byte-for-byte, and superseded in the manifest: new `prompt_supersession` field quotes all four passages by line and names the operative fields; new `prompt_currency_note` tells an implementer which field governs. Rewriting the snapshot would re-pin four digests so that three sessions appeared to have executed text they never saw |
| 16 required contexts | `components[6]` dated the 16 to `02:45Z` while AC3, `verification.commands[0]`, F1, F6 and this evidence dated it to `02:52Z` | the 16 was declared by the #1033 commit `2570ba0` at `2026-11-25T02:45:18Z`, whose own message says an earlier stage-B PUT had set it; the 15 was read before it. `components[6]` now says `02:52Z` |
| §7 context row (both sides) | `12 contexts … re-read as 16, the extra three being Session Evidence and its two self-test contexts` — 12 + 3 = 15 against a stated 16 | names all four additions, `rust-workspace-test` included |
| §7.1 annotation, Chinese side | 「读者照字面读会得出……」 — a modal, where the English recorded what a reader concluded | 「有读者照字面接受，得出的结论是……」 — the same fact on both sides |
| §7.2 opening sentence | `D1's conclusion does not change` (both sides), with no pointer to the later restatement | carries the pointer to the split and defines what "does not change" means |
| INDEX row | `enable required_pull_request_reviews … complete-object PUT so the 11 required contexts survive` — an instruction to perform the write the same work item forbids, with a count that would have shrunk the list from 16 to 11 | the session-attestation check, `strict`/`enforce_admins` read-back, the CODEOWNERS-or-recorded-finding branch, and the refused-merge test; `required_pull_request_reviews` named only as forbidden |

### What this does not establish

It does not show that D1 is satisfied. No review by a non-authoring session has
been recorded; `D1-a` is `SATISFIABLE, NOT SATISFIED` and nothing in this change
moves it. It does not show that the session-attestation carrier asserts review:
the 16 required contexts include three `Session Evidence` contexts, and what
they attest is the *implementing* session, because `MANIFEST_FIELDS` begins with
`implementing_ai_session` and `role` is free text with no code path requiring a
reviewer role.

It also does not resolve the question this round raised and left open: whether a
work item's pinned prompt should be amended when the policy it states is
superseded, or annotated and left intact. This session chose annotation, on the
ground that the file is evidence of what was executed. A later round may rule
otherwise; if it does, four digests must move with it.

## What this record does not contain

No claim that the three reviews agreed. They did not: one returned `APPROVE`
with four minor findings, two returned `REQUEST CHANGES` on disjoint grounds.
No claim that the first attempt was sound; it was not, and two of its defects
were introduced by it. No claim that this pass is complete: the reviews that
found those defects have not yet re-read the bytes they are now looking at.
