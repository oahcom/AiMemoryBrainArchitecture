---
document_metadata:
  domain: ai-development
  role: decision-record
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
      evidence_reference:
        - "Measured against the GitHub REST API on 2026-11-24: 690 PRs enumerated (`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all`, every page; `GET /search/issues?q=repo:oahcom/AiMemoryBrainArchitecture+is:pr` returned `total_count: 690` the same day) with `/pulls/{n}/reviews` fetched for each, review states ever recorded = {COMMENTED: 169}, APPROVED = 0; merged PRs = 581 (`is:pr+is:merged` `total_count: 581`, cross-checked as 581 non-null `merged_at` in the same enumeration); collaborators = 1; oahcom0831-design permission = read."
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure in §2 was re-read from the GitHub REST API on 2026-11-24 over the complete PR history (690 records), not sampled, plus GET /branches/main/protection and GET /collaborators. The scope classification in §2.4 was computed by fetching GET /pulls/{n}/files for the 69 merged PRs with the greatest merged_at, and the canonical/normative check by fetching each changed .md file at that PR's merge_commit_sha. Each figure states its query and read date. The figures this note attested for 2026-11-23 did not all survive re-measurement and have been replaced in §2.1, §2.3 and §2.4; the correction record is the event comment on PR #849."
    usage_status: Active
    modification_status: Modified
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
    source: "14-ai-development/adr/OWNER-DECISION-REVIEW-INDEPENDENCE-001.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/adr/OWNER-DECISION-REVIEW-INDEPENDENCE-001.md"
---

# OWNER-DECISION-REVIEW-INDEPENDENCE-001 — none of the three remedies is available

> **Added 2026-11-25 (citation currency).** The title's "none of the three remedies is available" rested on the premise that independent review requires a second GitHub account. That premise was amended on 2026-11-24 by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935): independence is a property of the reviewing session, not of the account that carries it. Of the conclusion the title states, only "remedy 1 is unavailable" (GitHub counts *users* and forbids self-approval) and "the fourth disposition: record the exception explicitly" survive; "none of the three is available" does not. See §9.

**DECIDED — 2026-11-23, owner-proxy session, as `Draft` and deliberately not as `Approved`.** §6 explains why this document does not claim the approval status its siblings claim.

Answers the choice `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §10.5 demanded: "only one of the three may be chosen".

**The answer is that no session can choose any of the three, and the two reasons are different.** One pair deadlocks the repository; the third is circular.[Added 2026-11-25: this sentence assumed independence requires a second GitHub account. "No session can choose any of the three" no longer holds — §5 was amended on 2026-11-24 by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935) to a per-session test, so remedy 3 is available and remedy 2 is available as a rule (§9.5). "One pair deadlocks the repository" survives only for remedy 1; "the third is circular" does not. The rest of the paragraph — a fourth disposition needing no new mechanism, because §5's last sentence already states it — is unchanged.] Both are measured below. What emerges instead is a fourth disposition that needs no new mechanism, because `PR-GOVERNANCE-001` §5 states it in its own last sentence.

## 1. The question, and the measurement that reframes it

008 §10.5 listed:

1. Turn on `required_pull_request_reviews` on `main`.
2. Add a workflow that returns `HOLD` when `author == reviewer`.
3. Demote §5 from Normative to Informative and record that this repository has no conditions for independent review.

It assumed all three were executable and differed only in honesty and cost. Two facts make that assumption false.[Added 2026-11-25: only one of the two facts still makes the assumption false. The second (the §9 review was unobtainable under the §5 definition then in force) lapsed when §5 was amended on 2026-11-24 by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935); the first (no second write-capable account, and the platform forbids self-approval) is unchanged. "All three were never executed" still holds; "all three were unexecutable" does not.] Both are new measurements, taken over the **entire** PR history rather than the last 45.

## 2. What the repository actually is

### 2.1 No approving review has ever existed

Walking all 690 pull requests (`GET /repos/oahcom/AiMemoryBrainArchitecture/pulls?state=all`, every page, read `2026-11-24`) and fetching `/pulls/{n}/reviews` for each:

| | |
|---|---|
| PRs walked | **690** (all pages, not a sample; `search/issues?q=…+is:pr` also returned `690`) |
| Distinct review states ever recorded | `{COMMENTED: 169}` |
| `APPROVED` reviews ever recorded | **0** |
| `REQUEST_CHANGES` reviews ever recorded | **0** |
| Distinct PR authors, all history | `{oahcom}` — **1** |
| Distinct reviewers, all history | `{oahcom}` — **1** |

008 §10.1 reported 0 of the 45 PRs it sampled. The figure over all history is 0 of 690. This is not a recent regression; it has never once happened. §5 has never been complied with in this repository, in any period.[Added 2026-11-25: `APPROVED = 0` is still a measurement of the approvals recorded on GitHub, and "not a recent regression" is unchanged. "§5 has never been complied with, in any period" can no longer be asserted directly from 2026-11-24: after §5 was amended by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935) to a session-level test, §9.2 states that #935's governance review was performed by a separate session; if that review satisfies §5's session test, at least one compliant instance exists. This document has not verified that, so the universal negative is marked unverified rather than resolved.]

### 2.2 Exactly one identity can write

| | |
|---|---|
| Collaborators | **1** — `oahcom`, `{admin, maintain, push, triage, pull}` |
| Repo owner | `oahcom`, type `User` |
| Commit authors in last 100 | `oahcom` 100, `oahcom0831-design` 4 |
| PRs opened by `oahcom0831-design`, all history | **0** |
| `oahcom0831-design` permission | **`read`** — `{admin: false, maintain: false, push: false, triage: false, pull: true}` |

A second GitHub account does exist and does push commits. It cannot merge, and its approvals would not satisfy a required-review protection, which counts only reviewers with write access.

### 2.3 There is no review requirement, and never was

`GET /branches/main/protection` returns:

| Key | Value |
|---|---|
| `required_status_checks.strict` | `true`, 11 contexts |
| `required_pull_request_reviews` | **absent from the response entirely** |
| `required_conversation_resolution` | `{enabled: false}` |
| `required_signatures` | `{enabled: false}` |
| `enforce_admins` | `{enabled: true}` |
| `restrictions` | `null` |

Read `2026-11-24` from `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` (`HTTP 200`). The eleven required contexts are `GOV-DOC-001 structural checks`, `Branch freshness vs base`, `audit`, `GOV-DOC-002 metadata checks`, `BMCP protocol index (hard gate)`, `BMCP conformance suite (hard gate)`, `Schema non-empty audit (hard gate)`, `Bilingual docs coverage (ratchet)`, `Rust clippy (hard gate)`, `Repository hygiene (hard gate)`, `Rust format (hard gate)`. `required_pull_request_reviews` is absent from that same payload.

### 2.4 §5's scope is real, so this is not a scope artifact

008 §10.5's remedy 3 would be cheap if §5 never applied. It applies. Classifying the 69 merged PRs with the greatest `merged_at` by content — `GET /pulls?state=all` (every page), then `GET /pulls/{n}/files` for each, read `2026-11-24`; docs-only means every changed file ends in `.md`:

| Kind | Count |
|---|---|
| docs-only | **33** |
| touches `.py` | 18 |
| touches `.rs` | 5 |
| other | 13 |

And of those **33** docs-only merged PRs, whose changed `.md` files were each fetched at that PR's `merge_commit_sha`, **17 touch at least one document declaring `canonical_status: Canonical` or `normative_status: Normative`** — `#749`, `#759`, `#761`, `#770`, `#771`, `#783`, `#790`, `#794`, `#801`, `#802`, `#804`, `#807`, `#811`, `#812`, `#822`, `#842`, `#849`.

The figures this paragraph replaces were internally impossible: the table reported 45 docs-only while the paragraph claimed to have fetched 46, and the paragraph then listed `#731`–`#744`, which are older than the 69th PR of the window it named. Table and paragraph had been measured over different windows. Both are re-derived above from one window, one query and one read date. One file could not be evaluated: `.github/pull_request_template.md` at `5283e98e` (PR `#757`) returned `404` at that commit, so `#757` is counted as not touching a canonical or normative document.

"Canonical persistence" and "cross-owner contracts" cover those 17 by their own wording. §5 is not being read too widely. It is being ignored.

## 3. Remedy 1 and remedy 2 both deadlock the repository

> **Partly withdrawn by §9 (2026-11-25).** Remedy 1 still deadlocks, for a reason the amendment did not touch: GitHub forbids approving your own PR and counts *users*, and there is one user. Remedy 2 no longer does — under §5 as amended, `author == reviewer` is a *session* comparison, and a second session is not the authoring session. What survives against remedy 2 is narrower and is a fact about the tool, not the clause: a GitHub workflow can only compare accounts, so it cannot observe the new test.

§5's last sentence: "A review performed through the same connected GitHub identity as the author is not independent." [Added 2026-11-25: this quotation is pre-2026-11-24 §5 text, retired by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935); the live §5 wording is "Independence is a property of the reviewing session, not of the GitHub account that carries it", and its last sentence is "Record exceptions explicitly; do not silently waive the requirement." The inference that follows therefore holds only for platform-enforced *required approval*; it no longer yields "independent review is impossible".] GitHub separately forbids approving one's own pull request.

Combine those with §2.2: the only identity that can approve is the only identity that authors, and it cannot approve its own work. So:

- **Remedy 1** would make every PR permanently unmergeable. The required approval cannot exist.
- **Remedy 2** would return `HOLD` on 100% of PRs, because `author == reviewer` is true of every pull request this repository has produced and would be true of the next one whatever its number.[Added 2026-11-25: this bullet does not hold. `author == reviewer` is a *session* comparison after 2026-11-24 (`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`, PR #935); a second session is not the authoring session, so this would not fire on 100% of PRs. What survives is narrower and is a fact about the tool, not the clause: a GitHub workflow can only compare accounts, so it cannot observe the session-level test.]

Neither is a repair. Each is `GOV-NC-2026-11-21-GATE-DEADLOCK-006` reproduced deliberately: a gate that refuses every input on `main`. 006 is the precedent, and its own resolution is part of the evidence — it was resolved `RESOLVED_ON_MAIN` by a **self-review merge** (§14, §12), which is to say the previous deadlock was closed by an act that §5 forbids. Adding a second gate of the same shape would close the same way.

**So remedies 1 and 2 are not "expensive".** They are unavailable until a second write-capable identity exists, and creating one is an authority transfer to a human, not a configuration toggle.[Added 2026-11-25: conclusion unchanged, ground changed — and only for remedy 1. Remedy 1 remains unavailable on platform grounds (GitHub counts *users*, forbids self-approval, `collaborators = 1`); remedy 2 no longer needs a second write-capable identity, because a separate session satisfies §5's session test (`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`, PR #935). "Creating a second identity is an authority transfer to a human, not a configuration toggle" still holds for remedy 1.]

The same protection payload quoted in §2.3 forecloses the §7 escape route as well: it reports 11 required contexts in force with `enforce_admins: true`, and no `required_pull_request_reviews`. Enforcement is present; independent approval is not. §7 describes a repository where the platform cannot enforce at all, which is not this one.

## 4. Remedy 3 is circular, and its own change-control clause says so

> **Withdrawn by §9 (2026-11-25).** The circularity was real only while independence required a second GitHub identity. Under the amended §5 the governance review §9 demands can be performed by a separate session, so remedy 3 was never structurally unavailable — and on 2026-11-24 it was *executed*: PR #935 amended §5 through this route. [Added 2026-11-25 (correcting this banner's last clause): "was *executed*" conflicts with §9.2, and §9.2 governs — PR #935 used the §9 route ("the route was used"); it did not carry out remedy 3 ("the remedy was not"): §5 is still Normative, and the demotion 008 §10.5 offered has still not been made. The amendment itself was made on 2026-11-24 under `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` / PR #935. The judgment that the circularity does not hold is unchanged; what changes is the distinction between "route used" and "remedy performed".]

Remedy 3 means editing a clause of `PR-GOVERNANCE-001`, which is:

```
canonical_status: Canonical
normative_status: Normative
decision_status: Approved
approver: Integration Owner
```

Its §9 states: "Changes to this standard require a bilingual semantic-parity update and an exact-Head governance review."

The governance review §9 requires is the independent review §5 cannot supply. **Demoting §5 requires disobeying §5.** The remedy is not merely awkward; it is unavailable through its own text.[Added 2026-11-25: these three sentences are withdrawn by §9.2 and are preserved here. §9's governance review can be performed by a session that did not author and did not implement the change, so §5 can satisfy §9; PR #935 amended §5 on 2026-11-24 by exactly that route under `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`. "Unavailable through its own text" does not hold. What still holds: §5 has not been demoted, and #935 amended the criterion without demoting §5.]

008 §10.5 called remedy 3 "the most honest and the least work". It is neither. It is the one remedy that would look like a decision while being a violation of the standard it edits.[Added 2026-11-25: this judgment rested on §4's circularity argument, which lapsed when §5 was amended on 2026-11-24 by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935): §9's governance review can be supplied by a separate session, so demoting §5 is not necessarily a violation of §5. "Would look like a decision while being a violation" still holds for an edit that has not obtained §9's review; it does not hold for one that has.]

## 5. The fourth disposition, which already exists

`PR-GOVERNANCE-001` §5 closes with the sentence this situation actually needs:

> "Record exceptions explicitly; do not silently waive the requirement."

That is the disposition. Not one of the three. **The exception is recorded, explicitly, as `EX-20261123-01`.** §5 demands a record, not a platform control, so a session can discharge it without depending on a repository setting and without a second identity existing.

**Why §7 is not available as the ground.** §7's disposition branch is conditioned twice — on "the current GitHub plan/visibility" not supporting required controls, and on that being so "for this private repository". Neither condition holds, measured `2026-11-24`:

| §7's premise | Measured `2026-11-24` |
|---|---|
| the repository is private | `GET /repos/oahcom/AiMemoryBrainArchitecture` → `private=false`, `visibility=public` |
| the plan/visibility cannot enforce required controls | `GET /branches/main/protection` → `200`; 11 required contexts; `strict: true`; `enforce_admins: true` |
| a stale or failing head can still merge | `PUT /pulls/849/merge` refused a green-but-behind head: `405 10 of 10 required status checks are expected` (message text as returned; the payload later lists eleven contexts) |

Platform enforcement exists here. A disposition naming an absent platform capability would be a false statement about this repository, so this document does not use one.

**The identity problem is separate, and §7 never addressed it.** Independent review is unsatisfiable at `collaborators = 1` with GitHub forbidding self-approval (§2.2, §3).[Added 2026-11-25: conclusion unchanged, ground changed, and the scope narrows to the platform-approval layer. GitHub counts *users* and forbids self-approval, so `collaborators = 1` makes *required approval* unobtainable — that platform fact is unchanged, and §5's amendment (`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`, PR #935) does not touch it. "Independent review itself is unsatisfiable" does not hold: §5 now defines independence at the session level, so another session can supply it without a second account.] That is a fact about who may write, not about what the plan or the visibility permits; changing either would not produce a second reviewer.

**What the merges were.** §5 forbids the *silence*, not the waiver. Every merge counted in §2.1 was a waiver that should have been recorded and was not. Recording it is what `EX-20261123-01` does, and the count it produces is what arms the `AI-EXEC-001` §6 rule-revision trigger (§5.1).

**What Issue #134 carries now, and what it did not.** #134 was closed `completed` at `2026-11-19T17:28:27Z`; its two remediation items were dispositioned `PLATFORM-LIMITED` on the ground that protection and rulesets both return `403` for a private repository on the free plan. That ground is false: `GET /repos/oahcom/AiMemoryBrainArchitecture` returns `private=false` / `visibility=public`, and `GET /branches/main/protection` returns `200` with 11 required contexts, `strict: true` and `enforce_admins: true`. Because the ground is false, #134 carries a `reopened` event at `2026-11-24T03:04:21Z`; before it, a `closed` event at `2026-11-19T17:28:27Z` with `state_reason: completed`. It now tracks a narrower question: whether the status-check enforcement and the change of repository visibility were authorized. Independent approval — `required_pull_request_reviews` is absent from that same payload — remains the subject of this record and not of #134. An earlier version of this paragraph asserted that the issue had been open continuously; it had in fact been closed for most of the interval.

### 5.1 The rule-revision trigger is armed, and it is the one legitimate way to change §5

> **Added 2026-11-25 (citation currency).** "The one legitimate way" has been overtaken by fact: §5 was amended on 2026-11-24 through §9's own exact-Head governance review path under `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935), without this quota trigger. The trigger remains a legitimate route, but not the only one; the ordering conclusion (record, then count, then amend) is unchanged. "Remedy 3 edits §5 by disobeying §9" in the same section also lapsed with §4's circularity argument: an edit that has obtained §9's review does not violate §9.

`AI-EXEC-001` v1.1 is **ADOPTED** (PR #256, merge `48a55649`), so its §6 quota clause binds:

> "At most 2 exceptions per iteration; exceeding the quota in 2 consecutive iterations triggers a daily governance window for rule revision. This quota is new operating discipline added by this clause."

This clause is the difference between remedy 3 and a lawful amendment. Remedy 3 edits §5 by disobeying §9. This clause edits it by **being the mechanism the standard itself provides for exactly this situation** — a control that cannot be satisfied generating repeated exceptions.

Measured: the repository is at **581 exceptions, not 2** — one for every PR merged into `main` without an independent approving review (`is:pr+is:merged` `total_count: 581`, read `2026-11-24`; the same enumeration shows 581 PRs with a non-null `merged_at`). If the quota is counted per distinct blocked PR, as RULING-06's counting rule directs, that is 581 in a single interval against a cap of 2. The over-quota condition has therefore been satisfied for far more than two consecutive iterations — the trigger is not merely reachable, it is long overdue and has never fired, because exceptions were never recorded and a quota cannot overflow on zero.

So the sequence is ordered, and each step is someone's:

| Step | Who | State |
|---|---|---|
| Record the exceptions | any session | **this ruling**, `EX-20261123-01` |
| Count them against the §6 quota | any session | done here: 581 vs 2 |
| Open the daily governance window | accountable Owner | **not done** |
| Amend §5 in that window | Integration Owner, per §9 | blocked on the window |
| Or supply a second write identity | repository administrator | blocked on a human |

Recording first is not bureaucracy. Until the count exists, the trigger has no input, and the standard has no lawful route to amend itself.

> **Added 2026-11-25 (citation currency).** The table's last row, "Or supply a second write identity", presents a second write-capable identity as a route to compliance. Since 2026-11-24 (`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`, PR #935) independence is decided by session rather than by account, so a second identity is no longer required for independent review; it remains required only for remedy 1 (platform-enforced required approval). The other rows are unchanged.

## 6. The one thing a session can actually do, and why this document is `Draft`

> **Partly withdrawn by §9 (2026-11-25).** The sentence "that is structural and nobody's fault" is the error §9 records: it turned "nobody opened an independent session" into "no independent session can be opened". The obligation to record the exception is unaffected and remains the one act a session can take.

There is exactly one compliance act available to a session, and it is the one §5 asks for in its own last sentence: **"Record exceptions explicitly; do not silently waive the requirement."**

Measured: across all 690 PRs the register held **0** exception records before this ruling. `14-ai-development/governance-register/` contained no `EX-` file of any kind; `EX-20261123-01`, added with this ruling, is the first. So the violation is not "no independent reviewer exists" — that is structural and nobody's fault. The violation is that **the waiver was silent**, which §5 explicitly forbids and which was always avoidable.

`AI-EXEC-INDEPENDENCE-RULING-001` already specifies the exception protocol in full (RULING-06, seventeen fields), and `AI-EXEC-001` §6 caps exceptions at two per iteration and forbids them from ever converting `HOLD` into `MERGE`. Both remain **PROPOSED**, not adopted. That ruling cannot be adopted by this session either: its own status path says "an author-identity COMMENT, AI role simulation, commit, merge, silence or this session's own ruling is not adoption."

Which is why this document is `Draft`. Every sibling `OWNER-DECISION-*.md` in this directory declares `decision_status: Approved` with `approver: "Owner D acting as owner proxy"`. `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §10.3 recorded that this pattern is self-description rather than evidence, because at the account layer `author == merger == approver`. Adding a ninth such approval in a document whose subject is that pattern would make the register's finding false by being written. So this one claims nothing it cannot show.

## 7. What this rules, and what it refuses

**Ruled.**

1. 008 §10.5's choice is **not available to any session**. Remedies 1 and 2 require a second write-capable identity; remedy 3 requires the review it removes.[Added 2026-11-25: this ruling item is withdrawn by §9.5; the original is retained. Its premise — that independence requires a second GitHub account — was amended on 2026-11-24 by `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036` (PR #935). After the amendment: remedy 1 is still unavailable (the platform counts *users* and forbids self-approval); remedy 2 is available as a rule and remedy 3 is available (§9.5). What does not change is that the choice belongs to the Owner.]
2. The correct disposition is a **recorded exception** under `PR-GOVERNANCE-001` §5, filed as `EX-20261123-01`. No platform-blocked status is claimed: §7's precondition — a plan or visibility that cannot enforce the controls — is false as measured on `2026-11-24`, so §7 is not available as a ground (§5). **Issue #134** stays open, tracking the narrower question §5 states: whether the status-check enforcement and the visibility change were authorized.
3. The immediate, session-executable obligation is to **record the exception**, which has been skipped on every one of the 581 merges. `EX-20261123-01` is created with this ruling and covers the interval retrospectively. Per RULING-06's counting rule — one record per distinct blocked Work Item plus one missing control, where a continuous blocked interval counts once — one record covers the interval, not 581 records.
4. §5 stays `Normative` **for now**. It is not demoted unilaterally, because its scope is real (§2.4) and removal by edit is not executable (§4). The lawful route is §5.1's quota trigger, which requires the count that `EX-20261123-01` supplies.

**Refused.**

- Not enabling `required_pull_request_reviews`. It would freeze `main` with no way to unfreeze it, and `enforce_admins: true` means the freeze would bind the only identity that could lift it.
- Not reclassifying `oahcom0831-design` from `read` to `write` to manufacture a second approver. Whether that account is a distinct accountable human is a fact about the world that this repository cannot establish, and a session that promoted it would be creating the appearance of independence it is forbidden to claim. That is the repository administrator's act, named in §5 above.
- Not adopting `AI-EXEC-INDEPENDENCE-RULING-001`, for the reason its own status path gives.
- No claim of independent review for this document, or for the eight that precede it.

## 8. Residual risk, stated plainly

> **Withdrawn by §9 (2026-11-25).** This paragraph required a second write-capable *identity* before any merge could be compliant. A second *session* supplies the independence element; the Owner-approval element still requires an accountable human and is unchanged.

Everything above is a measurement about the repository's past and present. None of it makes a future merge compliant. Until a second write-capable identity exists, or the Project Owner records an attributable adoption of the PROPOSED ruling, **every merge into `main` continues to be a §5 violation** — and the only improvement this document achieves is that the violation now has a record with a date on it, which is the difference between a silent waiver and a recorded one.

That difference is small. It is also the only difference available from inside the repository.

## 9. Erratum: one of the three remedies was available, and was used (2026-11-25)

> **Added 2026-11-25 (citation currency).** "Was used" in the title refers to §9's route being used, not to remedy 3 having been executed. On this section's own §9.2 distinction: PR #935 (`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`, 2026-11-24) amended the test for independence but did not demote §5 to Informative. This note corrects the title's wording only; it touches no count and no measurement.

`PR-GOVERNANCE-001` §5 was amended on 2026-11-24
(`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`, PR #935). Independence
is now a property of the **reviewing session**, not of the GitHub account that
carries it. This document's measurements were all taken before that and none of
them changes; what changes is what they support.

### 9.1 What is withdrawn

| Claim | Where | Status |
|---|---|---|
| "Remedy 3 is circular … demoting §5 requires disobeying §5" | §4, §7 ruling 1 | **False.** The §9 governance review is supplied by a separate session, so the route was open all along — #935 used it on 2026-11-24. Note what that did and did not do: it amended the criterion; it did not demote §5. See §9.2. |
| "Remedies 1 and 2 are unavailable until a second write-capable identity exists" | §3, §7 ruling 2 | **Half false.** Remedy 1 is unavailable — GitHub counts *users* and forbids self-approval, and that is a platform fact §5 does not touch. Remedy 2 as *specified in §1* is a workflow returning `HOLD` when `author == reviewer`; a workflow reads accounts, not sessions, so that mechanism still cannot distinguish the case it was meant to catch. The *rule* is now satisfiable; the *instrument* named here still is not. |
| "Every merge continues to be a §5 violation until a second write-capable identity exists" | §8 | **False.** A second session supplies the independence element. The Owner-approval element for §5-scope changes still requires an accountable human. |
| "That is structural and nobody's fault" | §6 | **False, and it was doing work** — see §9.3. |

### 9.2 Why §4 was wrong, specifically

§4 read: "The governance review §9 requires is the independent review §5 cannot
supply. Demoting §5 requires disobeying §5."

Both sentences were true under the definition then in force, and the second one
made the argument look airtight: the standard could not be amended without an
act the standard forbade. But it was a definition being used to prove that the
definition could not be changed. Once independence is a session property, §9's
review requirement is satisfiable by opening a session — no second account, no
administrator, no human.

That is not a hypothetical. PR #935 amended §5 on 2026-11-24 through exactly
this route: bilingual parity, exact-Head governance review, no second identity
involved. The *route* §4 declared closed was open **the next day** — this
document is `DECIDED — 2026-11-23`, and #935 merged 2026-11-24.

**Precision, because the distinction is the whole point.** Remedy 3 as 008 §10.5
worded it is *demote §5 from Normative to Informative*. #935 did not do that. It
**amended the criterion** and left §5 Normative. So what #935 proves is that the
§9 route is available — which is the proposition §4 denied — not that remedy 3
has been carried out. Calling the amendment "remedy 3 executed" would be the same
error one level up: a shared route taken for a shared act. As of this erratum,
§5 is still Normative, still in force, and the demotion 008 §10.5 offered is still
an unmade decision.

### 9.3 The error's direction, which is the useful part

§6 said the missing independent reviewer was "structural and nobody's fault",
and §8 closed by saying the only improvement possible from inside the repository
was a dated record. A day later the same route produced a governed amendment.
The claim was not falsified by a new fact about the world; it was falsified by
the repository doing what the document said could not be done.

This is the fourth instance in this session of one error shape: **a fact at one
layer read as a conclusion at another.**

- "the gate passed" read as "the content is correct";
- "the baseline froze 77 entries" read as "those 77 are the whole defect set";
- "the baseline and the content defects do not overlap" read as "shrinking the
  baseline repairs the defects";
- and here, "one GitHub account can write" read as "one review context can exist".

The first three were repaired by measuring again. This one needed no new
measurement: §2.2's numbers are all correct. It needed the distinction between
the account that **carries** a review and the session that **performs** it, which
the document had collapsed into a single word, "identity".

### 9.4 What still stands

Almost everything. Specifically:

- **§2's measurements**, unchanged and re-verifiable: 690 PRs walked,
  `APPROVED = 0`, `collaborators = 1`, `oahcom0831-design` read-only,
  `required_pull_request_reviews` absent, `enforce_admins: true`, 17 of 33
  docs-only PRs touching a Canonical or Normative document.
- **Remedy 1's deadlock.** The platform constraint is real and the amendment does
  not lift it. Anyone proposing remedy 1 should read this and expect `main` to
  freeze.
- **The obligation to record exceptions.** Unchanged, and now the only thing this
  document's §6 gets right. 675+ merges were silent waivers; §5 forbids the
  silence, not the waiver.
- **The refusal to claim independence for this document or its eight
  predecessors.** Unchanged for a new reason: they were written by a session, and
  a session cannot independently review itself.

### 9.5 What this creates

Not a decision. §7's ruling that "008 §10.5's choice is not available to any
session" is withdrawn. The accurate state is narrower than "two of the three are
available":

| Remedy | State after the amendment |
|---|---|
| 1 — enable `required_pull_request_reviews` | **Still unavailable.** GitHub counts *users*, forbids self-approval, and there is one user. |
| 2 — `HOLD` when `author == reviewer` | **Available as a rule, not as the named instrument.** A workflow reads accounts; the new test is per-session. It would need to be specified differently to mean what it says. |
| 3 — demote §5 | **Available.** §9's review requirement is satisfiable by a separate session, and #935 proved it by using that route. Not done: §5 is still Normative. |

Choosing among them is the Owner's, and this document declines to make that
choice on the Owner's behalf, which is the one thing in §7 that does not need
correcting.

What this document can say without exceeding its role: the reason it gave for
refusing to choose was that no choice existed. That reason is gone. The choice
exists, it is the Owner's, and it is now the only thing standing between the
repository and a compliant process.
