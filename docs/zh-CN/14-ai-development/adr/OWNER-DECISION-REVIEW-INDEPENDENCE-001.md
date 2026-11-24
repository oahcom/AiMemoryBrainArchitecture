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
        - "Measured against the GitHub REST API on 2026-11-23: 675 PRs walked, review states ever recorded = {COMMENTED: 169}, APPROVED = 0; collaborators = 1; oahcom0831-design permission = read."
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure in §2 was read from the GitHub REST API in this session over the complete PR history (675 records), not sampled, plus GET /branches/main/protection and GET /collaborators. The scope classification in §2.4 was computed by fetching each docs-only PR's files at its merge commit. No figure is carried over from another register."
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
    source: "14-ai-development/adr/OWNER-DECISION-REVIEW-INDEPENDENCE-001.md"
    en: "docs/en/14-ai-development/adr/OWNER-DECISION-REVIEW-INDEPENDENCE-001.md"
    zh-CN: null
---

# OWNER-DECISION-REVIEW-INDEPENDENCE-001 — none of the three remedies is available

**DECIDED — 2026-11-23, owner-proxy session, as `Draft` and deliberately not as `Approved`.** §6 explains why this document does not claim the approval status its siblings claim.

Answers the choice `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §10.5 demanded: "三者只能选一个" — one of three remedies must be chosen.

**The answer is that no session can choose any of the three, and the two reasons are different.** One pair deadlocks the repository; the third is circular. Both are measured below. What emerges instead is a fourth disposition that needs no new mechanism, because `PR-GOVERNANCE-001` §7 already names it.

## 1. The question, and the measurement that reframes it

008 §10.5 listed:

1. Turn on `required_pull_request_reviews` on `main`.
2. Add a workflow that returns `HOLD` when `author == reviewer`.
3. Demote §5 from Normative to Informative and record that this repository has no conditions for independent review.

It assumed all three were executable and differed only in honesty and cost. Two facts make that assumption false. Both are new measurements, taken over the **entire** PR history rather than the last 45.

## 2. What the repository actually is

### 2.1 No approving review has ever existed

Walking all 675 pull requests and fetching `/pulls/{n}/reviews` for each:

| | |
|---|---|
| PRs walked | **675** (all pages, not a sample) |
| Distinct review states ever recorded | `{COMMENTED: 169}` |
| `APPROVED` reviews ever recorded | **0** |
| `REQUEST_CHANGES` reviews ever recorded | **0** |
| Distinct PR authors, all history | `{oahcom}` — **1** |
| Distinct reviewers, all history | `{oahcom}` — **1** |

008 §10.1 reported 0 of 45. The figure over all history is 0 of 675. This is not a recent regression; it has never once happened. §5 has never been complied with in this repository, in any period.

### 2.2 Exactly one identity can write

| | |
|---|---|
| Collaborators | **1** — `oahcom`, `{admin, maintain, push, triage, pull}` |
| Repo owner | `oahcom`, type `User` |
| Commit authors in last 100 | `oahcom` 100, `oahcom0831-design` 4 |
| PRs opened by `oahcom0831-design`, all history | **0** |
| `oahcom0831-design` permission | **`read`** — `{admin: false, maintain: false, push: false, triage: false, pull: true}` |

A second GitHub account does exist and does push commits. It cannot merge, and its approvals would not satisfy a required-review protection, which counts only reviewers with write access.

### 2.3 There is no platform requirement, and never was

`GET /branches/main/protection` returns:

| Key | Value |
|---|---|
| `required_status_checks.strict` | `true`, 4 contexts |
| `required_pull_request_reviews` | **absent from the response entirely** |
| `required_conversation_resolution` | `{enabled: false}` |
| `required_signatures` | `{enabled: false}` |
| `enforce_admins` | `{enabled: true}` |
| `restrictions` | `null` |

### 2.4 §5's scope is real, so this is not a scope artifact

008 §10.5's remedy 3 would be cheap if §5 never applied. It applies. Classifying the 69 most recent merged PRs by content:

| Kind | Count |
|---|---|
| docs-only | **45** |
| touches `.py` | 13 |
| touches `.rs` | 9 |
| other | 2 |

And of the 46 docs-only merged PRs whose files were fetched at their merge commit, **26 touch at least one document declaring `canonical_status: Canonical` or `normative_status: Normative`** — `#837`, `#823`, `#822`, `#812`, `#811`, `#807`, `#804`, `#802`, `#801`, `#794`, `#790`, `#783`, `#777`, `#771`, `#770`, `#765`, `#761`, `#759`, `#750`, `#749`, `#744`, `#742`, `#740`, `#737`, `#733`, `#731`.

"Canonical persistence" and "cross-owner contracts" cover those 26 by their own wording. §5 is not being read too widely. It is being ignored.

## 3. Remedy 1 and remedy 2 both deadlock the repository

§5's last sentence: "A review performed through the same connected GitHub identity as the author is not independent." GitHub separately forbids approving one's own pull request.

Combine those with §2.2: the only identity that can approve is the only identity that authors, and it cannot approve its own work. So:

- **Remedy 1** would make every PR permanently unmergeable. The required approval cannot exist.
- **Remedy 2** would return `HOLD` on 100% of PRs, because `author == reviewer` is true of all 675 and would be true of the 676th.

Neither is a repair. Each is `GOV-NC-2026-11-21-GATE-DEADLOCK-006` reproduced deliberately: a gate that refuses every input on `main`. 006 is the precedent, and its own resolution is part of the evidence — it was resolved `RESOLVED_ON_MAIN` by a **self-review merge** (§14, §12), which is to say the previous deadlock was closed by an act that §5 forbids. Adding a second gate of the same shape would close the same way.

**So remedies 1 and 2 are not "expensive".** They are unavailable until a second write-capable identity exists, and creating one is an authority transfer to a human, not a configuration toggle.

## 4. Remedy 3 is circular, and its own change-control clause says so

Remedy 3 means editing a clause of `PR-GOVERNANCE-001`, which is:

```
canonical_status: Canonical
normative_status: Normative
decision_status: Approved
approver: Integration Owner
```

Its §9 states: "Changes to this standard require a bilingual semantic-parity update and an exact-Head governance review."

The governance review §9 requires is the independent review §5 cannot supply. **Demoting §5 requires disobeying §5.** The remedy is not merely awkward; it is unavailable through its own text.

008 §10.5 called remedy 3 "最诚实，也最省事". It is neither. It is the one remedy that would look like a decision while being a violation of the standard it edits.

## 5. The fourth disposition, which already exists

`PR-GOVERNANCE-001` §7 is titled "Platform enforcement is separate from process policy" and contains the clause this situation needs:

> "If the current GitHub plan/visibility does not support required controls ... record the limitation as BLOCKED and escalate to the repository administrator to select a genuinely enforceable plan/configuration."
>
> "Issue #134 remains OPEN until the platform confirms enforcement and a deliberately failing required check is proven unable to merge through the normal path."

That is the disposition. Not one of the three. **`BLOCKED`, per §7, escalated to the repository administrator, with Issue #134 as the carrier** — which is already open for exactly this and has been the whole time.

The three remedies in 008 §10.5 were written as if the repository were choosing a policy. It is not. It is missing a precondition, and §7 already says what to do about a missing precondition: say BLOCKED, name the administrator, keep the tracking issue open.

### 5.1 The rule-revision trigger is armed, and it is the one legitimate way to change §5

`AI-EXEC-001` v1.1 is **ADOPTED** (PR #256, merge `48a55649`), so its §6 quota clause binds:

> "每迭代例外 ≤ 2；连续 2 迭代超限 → 触发日度治理窗口做规则修订。该配额为本细则新增运行纪律。"
>
> ("At most 2 exceptions per iteration; exceeding the quota in 2 consecutive iterations triggers a daily governance window for rule revision.")

This clause is the difference between remedy 3 and a lawful amendment. Remedy 3 edits §5 by disobeying §9. This clause edits it by **being the mechanism the standard itself provides for exactly this situation** — a control that cannot be satisfied generating repeated exceptions.

Measured: the repository is at **675 exceptions, not 2**. If the quota is counted per distinct blocked PR, as RULING-06's counting rule directs, that is 675 in a single interval against a cap of 2. The over-quota condition has therefore been satisfied for far more than two consecutive iterations — the trigger is not merely reachable, it is long overdue and has never fired, because exceptions were never recorded and a quota cannot overflow on zero.

So the sequence is ordered, and each step is someone's:

| Step | Who | State |
|---|---|---|
| Record the exceptions | any session | **this ruling**, `EX-20261123-01` |
| Count them against the §6 quota | any session | done here: 675 vs 2 |
| Open the daily governance window | accountable Owner | **not done** |
| Amend §5 in that window | Integration Owner, per §9 | blocked on the window |
| Or supply a second write identity | repository administrator | blocked on a human |

Recording first is not bureaucracy. Until the count exists, the trigger has no input, and the standard has no lawful route to amend itself.

## 6. The one thing a session can actually do, and why this document is `Draft`

There is exactly one compliance act available to a session, and it is the one §5 asks for in its own last sentence: **"Record exceptions explicitly; do not silently waive the requirement."**

Measured: across 675 PRs there are **0** exception records. `14-ai-development/governance-register/` contains no `EX-` file of any kind. So the violation is not "no independent reviewer exists" — that is structural and nobody's fault. The violation is that **the waiver was silent**, which §5 explicitly forbids and which was always avoidable.

`AI-EXEC-INDEPENDENCE-RULING-001` already specifies the exception protocol in full (RULING-06, seventeen fields), and `AI-EXEC-001` §6 caps exceptions at two per iteration and forbids them from ever converting `HOLD` into `MERGE`. Both remain **PROPOSED**, not adopted. That ruling cannot be adopted by this session either: its own status path says "an author-identity COMMENT, AI role simulation, commit, merge, silence or this session's own ruling is not adoption."

Which is why this document is `Draft`. Every sibling `OWNER-DECISION-*.md` in this directory declares `decision_status: Approved` with `approver: "Owner D acting as owner proxy"`. `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §10.3 recorded that this pattern is self-description rather than evidence, because at the account layer `author == merger == approver`. Adding a ninth such approval in a document whose subject is that pattern would make the register's finding false by being written. So this one claims nothing it cannot show.

## 7. What this rules, and what it refuses

**Ruled.**

1. 008 §10.5's choice is **not available to any session**. Remedies 1 and 2 require a second write-capable identity; remedy 3 requires the review it removes.
2. The correct disposition is `BLOCKED` under `PR-GOVERNANCE-001` §7, recorded against **Issue #134**, which stays open.
3. The immediate, session-executable obligation is to **record the exception**, which has been skipped 675 times. `EX-20261123-01` is created with this ruling and covers the interval retrospectively. Per RULING-06's counting rule — one record per distinct blocked Work Item plus one missing control, where a continuous blocked interval counts once — one record covers the interval, not 675 records.
4. §5 stays `Normative` **for now**. It is not demoted unilaterally, because its scope is real (§2.4) and removal by edit is not executable (§4). The lawful route is §5.1's quota trigger, which requires the count that `EX-20261123-01` supplies.

**Refused.**

- Not enabling `required_pull_request_reviews`. It would freeze `main` with no way to unfreeze it, and `enforce_admins: true` means the freeze would bind the only identity that could lift it.
- Not reclassifying `oahcom0831-design` from `read` to `write` to manufacture a second approver. Whether that account is a distinct accountable human is a fact about the world that this repository cannot establish, and a session that promoted it would be creating the appearance of independence it is forbidden to claim. That is the repository administrator's act, named in §5 above.
- Not adopting `AI-EXEC-INDEPENDENCE-RULING-001`, for the reason its own status path gives.
- No claim of independent review for this document, or for the eight that precede it.

## 8. Residual risk, stated plainly

Everything above is a measurement about the repository's past and present. None of it makes a future merge compliant. Until a second write-capable identity exists, or the Project Owner records an attributable adoption of the PROPOSED ruling, **every merge into `main` continues to be a §5 violation** — and the only improvement this document achieves is that the violation now has a record with a date on it, which is the difference between a silent waiver and a recorded one.

That difference is small. It is also the only difference available from inside the repository.
