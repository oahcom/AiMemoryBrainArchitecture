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
      last_verification_note: "The branch-protection payload quoted here was read on 2026-11-25 before the #1033 merge at 02:45:19Z, and returned 15 required contexts; the 16 is the later reading at 02:52Z, recorded in the manifest. The merge timestamp, the ReadyForReviewEvent and the ruling timestamp were read from the pull request timeline at 2026-11-25T02:20Z. The claim that no code path requires a REVIEWER role was checked by reading MANIFEST_FIELDS and the role validation in scripts/governance/session_evidence/validate.py."
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

# Session evidence — the correction pass on the #1013 record

## Session role

CORRECTOR. This session did not write the record and did not write the code. It
read a `REQUEST CHANGES` ruling left on a pull request that merged without
answering it, checked each of that ruling's claims against the merged bytes, and
applied the ruling's own prescribed fixes.

## Actual AI input

The standing instruction, verbatim:

> 「你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动力的资源，使用最多的子线程子代理」

The ruling being applied, verbatim (comment `IC_kwDOVwHcdc8AAAABqioyZw` on
PR #1013, `2026-11-25T01:42:19Z`):

> `REQUEST CHANGES`。三项必须先解决：
> - **B4**（manifest 同时禁止并认证同一次 branch-protection 写入）——这是唯一一条会让后续实现按错误方向落地的；
> - **B3**（`remediation` 与 `constraints` 互斥）——它使 D1 有两个验收口径；
> - **B1**（两侧语言断言不同的事实）。
> **B2** 与 **B1/B3** 同源，一起改。**M1** 是独立的一段删除，恢复或在中英两侧同时声明删除。
> 我不改这份 PR 的任何字节：`#966` 的 ruling 该由落地它的会话改，我只报我实测到的矛盾。

No other normative instruction was supplied for this pass. Where the ruling
named a defect but not its replacement wording, the wording here follows the
criterion the ruling itself adopts (`#935`: independence is a property of the
reviewing session, not of the account).

## AI-visible output

| Ruling item | What the merged bytes said | What this pass did |
|---|---|---|
| B1 | zh: `唯一一个结构性恒为空的那个`; en: `only one structurally guaranteed to be near-empty` | both sides now state the same decidable fact: the endpoint is not empty (170 `COMMENTED`), what is necessarily zero is `APPROVED` |
| B2 | `ruling` required a non-authoring *session*; `current_status_components[0]` required a formal `Approved` review from a non-author *human* | `components[0]` restated at session level; the retired form is described as the thing measured as necessarily zero, not as the requirement |
| B3 | `remediation` prescribed a check-run attestation; three `constraints` demanded a second designated human with a GitHub account mapping | the three constraints restated at session level, with the self-review boundary preserved |
| B4 | deliverable 1, AC1 and `branch_protection_write` all required `required_pull_request_reviews >= 1`, which `remediation` forbids | all three rewritten to the session-attestation check; the withdrawn deliverable is quoted verbatim with its withdrawal recorded, not deleted |
| M1 | the English side lost the "why the count *seven* is not used" paragraph that the Chinese side keeps | restored from base `6c2b3ee` |
| item 1 | `11 contexts` in four places | now states 11 at registration, 12 at `2026-11-24`, 15 when read earlier on `2026-11-25`, and names the three additions. The count became 16 with the `#1033` merge at `2026-11-25T02:45:19Z` and was re-read as 16 at `02:52Z`; `rust-workspace-test` is the fourth addition. This record keeps the 15 it measured before that merge; the manifest and `POST-DENIAL` §7 carry the 16 |
| item 2 | `POST-DENIAL` §7 said 12, AC3 said 11, `GOV-031` §2.2 quotes `11 of 11` | the §2.2 quote is a verbatim platform response and stays; a note now says so and points at the re-read |
| item 3 | `prompt_status: RECORDED_NOT_FROZEN` next to `prompt_provenance_note: "Frozen from …"` | note now begins "Recorded from" |
| item 4 | the evidence table claimed rows added to "all six instances"; there are five per-instance tables | corrected to five plus the section 3.6 summary row, with the earlier wording named as wrong |

Measurement performed for this pass (`GET /branches/main/protection`, read
earlier on `2026-11-25` and quoted at the time as `02:45Z`):
15 required contexts, `strict: true`, `enforce_admins: true`,
`allow_force_pushes: false`, `allow_deletions: false`,
`required_pull_request_reviews` absent. The count became 16 with the `#1033`
merge at `2026-11-25T02:45:19Z`, re-read as 16 at `02:52Z`; this record keeps the
15 it measured before that merge, and the manifest carries the 16.

## What this record does not contain

- No claim that the `REQUEST CHANGES` was answered before the merge. It was not:
  the ruling is at `01:42:19Z`, the head did not change in response to it, and
  the merge is at `01:55:16Z`.
- No claim about why the merge proceeded. This session has no visibility into the
  session that merged it.
- No new instance row, no change to any frozen count, and no edit to §13.7.
