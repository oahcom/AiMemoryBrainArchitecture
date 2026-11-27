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
      last_verification_note: "Every figure in 'AI-visible output' was computed in this session from raw GitHub REST API responses read at 2026-11-25T00:36Z: 795 closed PRs across 8 pages, /pulls/{n}/reviews for all 681 merged PRs, and /issues/comments across 47 pages. No figure is carried over from another register. An independent cross-check was run against the same PRs in GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031 section 3, which reproduced the two post-merge comments to the minute."
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

# Session evidence — AID-2026-055 / Issue #966

## Session role

Owner-proxy governance session. It had no write access to the codebase and made no
code change. Its work was to re-measure two registers against the GitHub REST API
and to apply an existing Owner ruling (`#966`) to the text that ruling names.

The session was executed by an AI agent. The record below is written by that agent
about its own session, so it is a self-report, not a third-party attestation.

## Actual AI input

The operative inputs were two, both quoted verbatim.

**1. The standing directive that governed the session.**

> 你不应该停下，因为我不输出观点，所有owner都可以是一个会话，你持续到收敛即可，若因人类干预才可继续你可以当作为人类去收敛，但不能自己动手写代码。以最高效率去执行，动用所有能动用的资源，使用最多的子线程子代理

**2. The Owner ruling in Issue #966**, which is the normative text applied. Its five
numbered rulings, verbatim:

> 1. **Add `issues/{n}/comments` to the evidence table for all six rows, not just the two.** The measurement is one API call per PR and it is the only endpoint that can distinguish "unreviewed" from "reviewed afterwards". A register of review-form deviations that cannot see the review is measuring the wrong surface.
> 2. **Restate #927 and #946 as post-merge review, not zero review.** The §3.6 column `正式 Review` currently reads `0` for both. The accurate value is `0 formal, 1 post-merge review`. Whether that is better or worse than an unreviewed merge is an Owner judgement — a review written after the merge cannot have gated it, so I read it as neither exculpating nor aggravating, but the register must not report it as absence.
> 3. **Do not soften §3.5's refusal claim while fixing this.** The refusal at `13:20:27Z` naming #946 is real, and the `+90 min` approval does not retract it: a review that says *merge it* ninety minutes after it merged is a ratification, not a permission. Both facts belong in the record, and the record currently has one of them.
> 4. **State the endpoint semantics in the register itself.** One sentence — `pulls/{n}/reviews` is formal submissions, `pulls/{n}/comments` is inline diff comments, `issues/{n}/comments` is the conversation — turns three endpoint names into a measurement a reader can trust. Without it, the next entry will repeat this exact error, because the two zeros next to each other look like corroboration and are actually the same absence counted twice.
> 5. **The frozen count of §13.7 should stay frozen, and this does not change it.** §3.6 already says the append does not revise the baseline. Adding the conversation-comment column changes the *observed instance list*, not the historical statistic, and the distinction should survive the edit.

## AI-visible output

The output of the session was four edited documents and one new measurement. No
repository code was changed.

**Documents edited** — each bilingual pair edited in both languages. The per-instance
tables in `GOV-NC-...-031` section 3 are **five** (`#890`, `#896`, `#927`, `#933`, `#946`);
`#875` has no per-instance table, only a row in the section 3.6 summary, and that summary
row carries the new column too. An earlier revision of this paragraph said "six rows",
which was wrong about the per-instance tables.

| Path | Change |
|---|---|
| `14-ai-development/governance-register/GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031.md` | new §3.0 (endpoint semantics); `会话评论数` row added to the five per-instance tables and to the section 3.6 summary row; §3.3 and §3.5 restated as `0` formal / `1` post-merge; §3.6 gains a `会话线程` column |
| `14-ai-development/governance-register/GOV-NC-2026-11-24-MERGE-FORM-DEVIATION-031.en.md` | the same four changes in English |
| `14-ai-development/governance-register/POST-DENIAL-UNAUTHORISED-MERGE-001.md` | new §7.2 (third-endpoint census); §8 gains the `#966` reference |
| `14-ai-development/governance-register/POST-DENIAL-UNAUTHORISED-MERGE-001.en.md` | the same two changes in English |

**Measurement performed.** Three endpoints were read, and the population figures were
computed from the raw responses rather than taken from another register:

| Quantity | Value | How obtained |
|---|---|---|
| Closed PRs enumerated | 795 | `GET /pulls?state=closed&per_page=100`, every page |
| Merged PRs | 681 | `merged_at` non-null in the same enumeration |
| Formal review objects | 170, all `COMMENTED`, all `oahcom` | `GET /pulls/{n}/reviews` for all 681 merged PRs, 0 failures |
| Objects in state `APPROVED` | 0 | counted from the same responses |
| Conversation comments repository-wide | 4577 | `GET /issues/comments?sort=created&direction=desc`, pages 1–47, last page returned 77 |
| Authors of those comments | `{oahcom: 4577}` | counted from the same responses |
| Merged PRs with ≥1 conversation comment | 406 | joined on `issue_url` against `merged_at` |
| Merged PRs with a comment before the merge | 317 | same join, `created_at < merged_at` |
| Merged PRs with a comment after the merge | 232 | same join, `created_at >= merged_at` |

All reads were taken at `2026-11-25T00:36Z`.

**Two corrections were made to the session's own prior work.**

First: §7.1 of `POST-DENIAL-UNAUTHORISED-MERGE-001` had concluded `APPROVED = 0` from the
`pulls/{n}/reviews` endpoint alone. The figure is correct and unchanged, but it is arithmetic
rather than a finding. `GET /collaborators` returns exactly one account, that account authored
all 795 closed PRs, and GitHub forbids an account from approving its own PR, so `APPROVED` cannot
be anything but zero here. §7.1 now leads with 556 of 662 merged PRs carrying no review object at
all, which is a real absence and is not forced by the platform, and it moves `APPROVED = 0` out of
the headline position.

Second: D1's status changed from `REQUIRED, UNSATISFIED; ENFORCEMENT FAILURE` to
`REQUIRED BUT UNSATISFIABLE BY CONSTRUCTION`, with the previous wording preserved in
`AID-2026-055` `status_history` rather than overwritten. That status was itself qualified on 2026-11-25: #1059 annotated it in place as
scoped to the account layer, and `AID-2026-055` records the two parts separately in
`current_status_parts` (`D1-a` satisfiable, not satisfied; `D1-b` necessarily zero, and not
the requirement), because as a single unqualified string it made the requirement look
impossible when only the superseded account-level form is. §7.2 now states that the defect is in the
specification — defining independence as the appearance of a second GitHub account — and that the
expressible form is a required status check asserting a non-authoring reviewing session. Adding
`required_pull_request_reviews` is recorded as forbidden, because it can never be satisfied here
and would make every merge impossible.

## What this record does not contain

- No session transcript identifier. `session_reference_status` is `NOT_RECORDED`
  because the session's raw transcript was not committed to this repository; only
  this summarising document was.
- No claim that the prompt snapshot was frozen before the session ran.
  `executed_prompt_provenance` is `NOT_VERIFIED`: the digest pins the recorded bytes
  of `prompt-v1.md`, nothing more.
- No attribution of any GitHub account to a natural person.
