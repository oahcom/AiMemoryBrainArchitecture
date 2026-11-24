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
        - "Measured against the GitHub REST API at 2026-11-24T03:43:37Z: 690 PRs (582 merged) walked, review states ever recorded = {COMMENTED: 169}, APPROVED = 0; collaborators = 1; oahcom0831-design permission = read; required_status_checks = 11 contexts; Issue #134 open, state_reason reopened."
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every figure in §2 was read from the GitHub REST API at 2026-11-24T03:43:37Z over the complete PR history (690 records), not sampled, plus GET /branches/main/protection, GET /collaborators and GET /issues/134. The scope classification in §2.4 was computed by fetching each docs-only PR's changed files at its merge commit. No figure is carried over from another register. Every count below names the query that produces it and the date it was read, because this population moves under the document: the PR total rose from 685 to 690 and the required-context set from 10 to 11 within one working session, so every count is stated with the query and the instant it was read, and no argument below rests on any of them."
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
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/adr/OWNER-DECISION-REVIEW-INDEPENDENCE-001.md"
---

# OWNER-DECISION-REVIEW-INDEPENDENCE-001 — none of the three remedies is available

**DECIDED — 2026-11-23, owner-proxy session, as `Draft` and deliberately not as `Approved`.** §6 explains why this document does not claim the approval status its siblings claim.

Answers the choice `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §10.5 demanded: "only one of the three may be chosen".

**The answer is that no session can choose any of the three, and the two reasons are different.** One pair deadlocks the repository; the third is circular. Both are measured below. What emerges instead is a fourth disposition that needs no new mechanism, because `PR-GOVERNANCE-001` §7 already names it.

## 1. The question, and the measurement that reframes it

008 §10.5 listed:

1. Turn on `required_pull_request_reviews` on `main`.
2. Add a workflow that returns `HOLD` when `author == reviewer`.
3. Demote §5 from Normative to Informative and record that this repository has no conditions for independent review.

It assumed all three were executable and differed only in honesty and cost. Two facts make that assumption false. Both are new measurements, taken over the **entire** PR history rather than the last 45.

## 2. What the repository actually is

### 2.1 No approving review has ever existed

Walking every pull request and fetching `/pulls/{n}/reviews` for each. The population is `GET /search/issues?q=repo:oahcom/AiMemoryBrainArchitecture+is:pr` read at `2026-11-24T03:43:37Z` -> **690**. The walk visits every number from 1 to the highest existing; a number that is absent is an issue, not a gap in the walk:

| | |
|---|---|
| PRs walked | **690** (all pages, not a sample) |
| of which merged | **582** (`+is:merged`, same instant) |
| Distinct review states ever recorded | `{COMMENTED: 169}` |
| `APPROVED` reviews ever recorded | **0** |
| `REQUEST_CHANGES` reviews ever recorded | **0** |
| Distinct PR authors, all history | `{oahcom}` — **1** |
| Distinct reviewers, all history | `{oahcom}` — **1** |

008 §10.1 reported 0 of 45. The figure over all history is 0 of 690, and 0 of 582 merged. This is not a recent regression; it has never once happened. §5 has never been complied with in this repository, in any period.

### 2.2 Exactly one identity can write

| | |
|---|---|
| Collaborators | **1** — `oahcom`, `{admin, maintain, push, triage, pull}` |
| Repo owner | `oahcom`, type `User` |
| Commit authors in the last 100 commits (read `2026-11-24`; a rolling window) | `oahcom` 97, `gate` 1, `owner-proxy` 1, `verifier` 1 |
| Commits authored by `oahcom0831-design`, all history | **4** (author email `oahcom0831@gmail.com`; none among the last 100) |
| PRs opened by `oahcom0831-design`, all history | **0** |
| `oahcom0831-design` permission | **`read`** — `{admin: false, maintain: false, push: false, triage: false, pull: true}` |

A second GitHub account does exist and does push commits. It cannot merge, and its approvals would not satisfy a required-review protection, which counts only reviewers with write access.

### 2.3 There is no platform requirement for independent review, and never was

`GET /branches/main/protection` returns:

| Key | Value |
|---|---|
| `required_status_checks.strict` | `true`, **11 contexts** (read `2026-11-24T03:43:37Z`) |
| `required_pull_request_reviews` | **absent from the response entirely** |
| `required_conversation_resolution` | `{enabled: false}` |
| `required_signatures` | `{enabled: false}` |
| `enforce_admins` | `{enabled: true}` |
| `restrictions` | `null` |

### 2.4 §5's scope is real, so this is not a scope artifact

008 §10.5's remedy 3 would be cheap if §5 never applied. It applies. The window is a closed range of PR numbers rather than a count, so it does not move: **`#742`-`#856` inclusive**, 115 numbers of which **69** are merged pull requests on `2026-11-24`, the rest being issues or unmerged PRs. Each is classified by `GET /pulls/{n}/files` with precedence docs-only -> `.py` -> `.rs` -> other, where docs-only means every changed file ends in `.md`:

| Kind | Count |
|---|---|
| docs-only | **33** |
| touches `.py` | 17 |
| touches `.rs` | 6 |
| other | 13 |

And of the **33** docs-only merged PRs in that window, whose changed files were fetched at their merge commit, **18 touch at least one document declaring `canonical_status: Canonical` or `normative_status: Normative`** — `#842`, `#837`, `#822`, `#812`, `#811`, `#807`, `#804`, `#802`, `#801`, `#794`, `#790`, `#783`, `#771`, `#770`, `#761`, `#759`, `#749`, `#744`.

"Canonical persistence" and "cross-owner contracts" cover those 18 by their own wording. §5 is not being read too widely. It is being ignored.

## 3. Remedy 1 and remedy 2 both deadlock the repository

§5's last sentence: "A review performed through the same connected GitHub identity as the author is not independent." GitHub separately forbids approving one's own pull request.

Combine those with §2.2: the only identity that can approve is the only identity that authors, and it cannot approve its own work. So:

- **Remedy 1** would make every PR permanently unmergeable. The required approval cannot exist.
- **Remedy 2** would return `HOLD` on 100% of PRs, because `author == reviewer` is true of every PR in the walk and would be true of the next one.

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

008 §10.5 called remedy 3 "the most honest and the least work". It is neither. It is the one remedy that would look like a decision while being a violation of the standard it edits.

## 5. The fourth disposition, and the dated history of its carrier

`PR-GOVERNANCE-001` §7 is titled "Platform enforcement is separate from process policy" and contains the clause this situation needs:

> "If the current GitHub plan/visibility does not support required controls ... record the limitation as BLOCKED and escalate to the repository administrator to select a genuinely enforceable plan/configuration."
>
> "Issue #134 remains OPEN until the platform confirms enforcement and a deliberately failing required check is proven unable to merge through the normal path."

That is the disposition. Not one of the three. **`BLOCKED`, per §7, escalated to the repository administrator, with Issue #134 as the carrier.** The carrier has a dated history, and the dates are part of the evidence:

| Timestamp (UTC) | State of Issue #134 |
|---|---|
| `2026-11-19T17:28:27Z` | closed by `oahcom`, `state_reason: completed` |
| `2026-11-19T17:28:27Z` – `2026-11-24T03:04:21Z` | closed, for five days |
| `2026-11-24T03:04:21Z` | reopened by `oahcom` |
| `2026-11-24T03:08:45Z` (read) | `state: open`, `state_reason: reopened`, `closed_at: null` |

At the moment of that closure neither half of the issue's own exit condition was satisfied: the platform had not been shown to confirm enforcement, and no deliberately failing required check had been proven unable to merge through the normal path. The closure verdict was "REMEDIATED WITH DOCUMENTED PLATFORM ALTERNATIVE", premised on `protection` and `rulesets` returning `403` for a private repository on a free plan. That premise is now measurably false — `GET /repos/oahcom/AiMemoryBrainArchitecture` returns `private: false` and `GET /branches/main/protection` returns `200` — and the issue's own reopen comment records both. A `completed` issue is not a carrier, so during that five-day interval this disposition had none. This section states the interval instead of asserting that the issue had been open throughout, because it had not been.

What the reopened issue records is narrower than review independence, and the boundary is worth quoting. Its reopen comment establishes that required status checks *are* platform-enforced: `strict: true`, `enforce_admins: true`, eleven required contexts as read on `2026-11-24`, and a merge of this PR's own head at `4e689be053` refused with `405 "10 of 10 required status checks are expected."` It leaves open when the repository became public and by whose decision, which §7 forbids as a workaround absent an explicit security/privacy decision. It states in terms that review independence is not what it covers: `required_pull_request_reviews` is still absent, and that is "a different failure from this one". The missing piece — a second write-capable identity — is recorded here, not there.

The three remedies in 008 §10.5 were written as if the repository were choosing a policy. It is not. It is missing a precondition, and §7 already says what to do about a missing precondition: say BLOCKED, name the administrator, keep the tracking issue open.

One qualification, stated rather than implied. §7's clause is written for a *plan or visibility* limitation, and as of `2026-11-24` neither is the limitation: protection is readable and enforcing eleven required contexts. What is missing is a second write-capable identity, which is an authority fact rather than a configuration toggle. §7 is the nearest disposition the standard provides for a missing precondition, but here it is applied **by analogy**, and the analogy is named so that a later reader can reject it on the merits rather than discover it was assumed.

### 5.1 The rule-revision trigger is armed, and it is the one legitimate way to change §5

`AI-EXEC-001` v1.1 is **ADOPTED** (PR #256, merge `48a55649`), so its §6 quota clause binds:

> "At most 2 exceptions per iteration; exceeding the quota in 2 consecutive iterations triggers a daily governance window for rule revision. This quota is new operating discipline added by this clause."

This clause is the difference between remedy 3 and a lawful amendment. Remedy 3 edits §5 by disobeying §9. This clause edits it by **being the mechanism the standard itself provides for exactly this situation** — a control that cannot be satisfied generating repeated exceptions.

Measured: the repository is at **582 exceptions, not 2**. The figure is `GET /search/issues?q=repo:oahcom/AiMemoryBrainArchitecture+is:pr+is:merged` read at `2026-11-24T03:43:37Z` — one exception per merge that proceeded without the review §5 requires. If the quota is counted per distinct blocked PR, as RULING-06's counting rule directs, that is 582 in a single interval against a cap of 2. The over-quota condition has therefore been satisfied for far more than two consecutive iterations — the trigger is not merely reachable, it is long overdue and has never fired, because exceptions were never recorded and a quota cannot overflow on zero.

So the sequence is ordered, and each step is someone's:

| Step | Who | State |
|---|---|---|
| Record the exceptions | any session | **this ruling**, `EX-20261123-01` |
| Count them against the §6 quota | any session | done here: 582 vs 2 |
| Open the daily governance window | accountable Owner | **not done** |
| Amend §5 in that window | Integration Owner, per §9 | blocked on the window |
| Or supply a second write identity | repository administrator | blocked on a human |

Recording first is not bureaucracy. Until the count exists, the trigger has no input, and the standard has no lawful route to amend itself.

## 6. The one thing a session can actually do, and why this document is `Draft`

There is exactly one compliance act available to a session, and it is the one §5 asks for in its own last sentence: **"Record exceptions explicitly; do not silently waive the requirement."**

Measured: across 690 PRs there are **0** exception records. `14-ai-development/governance-register/` contains no `EX-` file of any kind. So the violation is not "no independent reviewer exists" — that is structural and nobody's fault. The violation is that **the waiver was silent**, which §5 explicitly forbids and which was always avoidable.

`AI-EXEC-INDEPENDENCE-RULING-001` already specifies the exception protocol in full (RULING-06, seventeen fields), and `AI-EXEC-001` §6 caps exceptions at two per iteration and forbids them from ever converting `HOLD` into `MERGE`. Both remain **PROPOSED**, not adopted. That ruling cannot be adopted by this session either: its own status path says "an author-identity COMMENT, AI role simulation, commit, merge, silence or this session's own ruling is not adoption."

Which is why this document is `Draft`. Every sibling `OWNER-DECISION-*.md` in this directory declares `decision_status: Approved` with `approver: "Owner D acting as owner proxy"`. `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` §10.3 recorded that this pattern is self-description rather than evidence, because at the account layer `author == merger == approver`. Adding a ninth such approval in a document whose subject is that pattern would make the register's finding false by being written. So this one claims nothing it cannot show.

## 7. What this rules, and what it refuses

**Ruled.**

1. 008 §10.5's choice is **not available to any session**. Remedies 1 and 2 require a second write-capable identity; remedy 3 requires the review it removes.
2. The correct disposition is `BLOCKED` under `PR-GOVERNANCE-001` §7, recorded against **Issue #134**. As read on `2026-11-24T03:08:45Z` that issue is `open` with `state_reason: reopened`; it had been `closed`/`completed` from `2026-11-19T17:28:27Z` until `2026-11-24T03:04:21Z`, so for those five days this disposition had no carrier. §5 records the interval rather than asserting the issue was open throughout.
3. The immediate, session-executable obligation is to **record the exception**, which has been skipped 582 times — once per merge without the required review. `EX-20261123-01` is created with this ruling and covers the interval retrospectively. Per RULING-06's counting rule — one record per distinct blocked Work Item plus one missing control, where a continuous blocked interval counts once — one record covers the interval, not 582 records.
4. §5 stays `Normative` **for now**. It is not demoted unilaterally, because its scope is real (§2.4) and removal by edit is not executable (§4). The lawful route is §5.1's quota trigger, which requires the count that `EX-20261123-01` supplies.

**Refused.**

- Not enabling `required_pull_request_reviews`. It would freeze `main` with no way to unfreeze it, and `enforce_admins: true` means the freeze would bind the only identity that could lift it.
- Not reclassifying `oahcom0831-design` from `read` to `write` to manufacture a second approver. Whether that account is a distinct accountable human is a fact about the world that this repository cannot establish, and a session that promoted it would be creating the appearance of independence it is forbidden to claim. That is the repository administrator's act, named in §5 above.
- Not adopting `AI-EXEC-INDEPENDENCE-RULING-001`, for the reason its own status path gives.
- No claim of independent review for this document, or for the eight that precede it.

## 8. Residual risk, stated plainly

Everything above is a measurement about the repository's past and present. None of it makes a future merge compliant. Until a second write-capable identity exists, or the Project Owner records an attributable adoption of the PROPOSED ruling, **every merge into `main` continues to be a §5 violation** — and the only improvement this document achieves is that the violation now has a record with a date on it, which is the difference between a silent waiver and a recorded one.

That difference is small. It is also the only difference available from inside the repository.
