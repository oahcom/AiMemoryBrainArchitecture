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
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure in §10 was pulled from the GitHub REST API on 2026-11-23: reviews queried per PR across the 45 most recent merges; the required_pull_request_reviews key absent from branch protection; and all 18 workflows grepped for reviews/APPROVED/reviewDecision with no enforcement hit. Not quoted."
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
    source: "14-ai-development/governance-register/GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008.md"
---

# GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008

- Register ID: GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008
- Status: `OPEN` / `ACTIVE` / CONTINUOUS — 0 independent reviews across 45 merged PRs, no platform requirement, and this register's author is one of the 45 (see §10); now BLOCKED under PR-GOVERNANCE-001 §7, escalated to the repository administrator (Issue #134) per §11 / the gate's own implementation was merged with zero review
- Found at: 2026-11-21T07:10Z (data pulled 2026-11-21T07:20Z)
- Subject: repository `oahcom/AiMemoryBrainArchitecture`, PR #423 / Issue #420
- Prior registers: 005 (CI never executed), 006 (gate deadlock), 007 (self-reviewed merges)

## 1. Bottom line

PR #423 changed the bilingual gate's own implementation (`scripts/check_bilingual_docs.py` **+110 −3**, plus +40 in tests) and fixed a real defect (Issue #420: an exemption could be self-registered in the same commit that introduced the file).

It was merged, and:

- `reviews = 0` — **no review at all**, not even a self-review;
- all three check runs have `conclusion = failure` and `steps = 0` — the jobs never started;
- author = merger = `oahcom`;
- created 06:53:12Z → merged 06:59:08Z, a span of **5m56s**.

This is the **reverse** of the shape register 007 records. 007 records "`reviews=1` on the count, independence zero". #423 does not even have the form.

## 2. Facts

### 2.1 PR metadata

| Item | Value |
|---|---|
| PR | #423 `fix(governance): require independent bilingual exemption registration` |
| created | 2026-11-21T06:53:12Z |
| merged | 2026-11-21T06:59:08Z |
| span | 5m56s |
| author | `oahcom` |
| merger | `oahcom` |
| reviews | **0** |
| commits | 1 (`6d6c6ba57a`) |
| files | 2, `+150 −3` |
| merge commit | `360d88c99a47018ce78b870379be3ee43841a837` |
| head branch | `fix/issue-420-exemption-self-registration` |

### 2.2 What changed

```
6d6c6ba57a  scripts/check_bilingual_docs.py                        +110  -3
6d6c6ba57a  scripts/governance/evidence/test_gate_normative_roots.py +40  -0
```

It adds `check_embedded_registration_history()`, requiring every entry in `EMBEDDED_BILINGUAL_SOURCES` to be registered in a commit **later** than the one that created the file. Same-commit registrations are allowed only for three `SELF_REGISTERED_AT_CREATION` entries, pinned to their measured SHAs.

This is a **genuinely effective fix**. Issue #420's reproduction was: create `00-governance/new-spec.md` and, in the same commit, insert a self-invented reason into the exemption table — gate returns `EXIT=0`. After the fix that path is closed.

### 2.3 Commit identity

```
author    {'name': 'Ubuntu', 'email': 'ubuntu@localhost.localdomain', 'date': '2026-11-21T06:51:14Z'}
committer {'name': 'Ubuntu', 'email': 'ubuntu@localhost.localdomain', 'date': '2026-11-21T06:52:00Z'}
```

That is the **fifth** commit identity in this series. The first four: `oahcom`, `unknown <1491856051>`, `governance@localhost`, `oahcom <noreply@github.com>` (web commit).

### 2.4 Check runs

| name | status | conclusion | steps |
|---|---|---|---|
| GOV-DOC-001 structural checks | completed | **failure** | **0** |
| GOV-DOC-002 metadata checks | completed | **failure** | **0** |
| audit | completed | **failure** | **0** |

All three annotations read:

```
The job was not started because recent account payments have failed or your
spending limit needs to be increased. Please check the 'Billing & plans' settings
```

That is the `NOT_EXECUTED` shape register 005 records: `conclusion: failure` does not mean the tests failed, only that the job never started.

## 3. Why this is worse than 007

007 records reviews that are compliant on the count and empty on independence. It at least shows the executor knew a review requirement existed and was willing to go through the motion.

#423 does not go through the motion at all:

| Item | #418 (recorded in 007) | #423 (this register) |
|---|---|---|
| reviews | 1 (`COMMENTED`, the author) | **0** |
| review → merge | 12 seconds | no review to time |
| created → merge | — | 5m56s |
| what changed | exemption table, +5 lines | **gate implementation, +110 −3** |
| check state | not pulled | all three `steps=0` |

The fourth row is the important difference: **#418 changed data (an exemption list); #423 changed the criterion (the gate implementation).** The first decides whether one file may pass. The second decides the rule by which every PR is judged.

A zero-review PR changed the definition of compliance, and the first thing that definition judges afterwards is every PR that follows it.

## 4. The chain it closes

006 records the gate being unsatisfiable on main; #418 lifted it via F-1; #420 pointed out that F-1's path can be abused by self-registration; #423 closed the self-registration.

Four steps, each either a direct push or a zero/self-reviewed merge:

```
ae37a419  direct push, unpaired normative doc      → 006
#418      self-review, 12s, +5 exemption lines    → 006 §12
#420      records the self-registration defect    → this register §2.2
#423      zero review, 5m56s, +110 −3 gate change → this register
```

Each step has a defensible reason on its own: direct push to move fast, F-1 because the template is machine-consumed, the fix because the defect is real. **But no step had independent review, and in series they rewrote the judging rule.**

## 5. A question that has to be asked

`check_embedded_registration_history()` depends on `git log --diff-filter=A` and `git log -S`, i.e. full git history. And register 005's state is: **CI has never executed this script**.

So the new criterion was never verified by any automation at merge time. Its test, `test_gate_normative_roots.py` (+40 lines), was not executed either.

This is not inference. `steps=0` on all three check runs is the evidence.

## 6. Measured: how the new criterion behaves on real history

Running the upgraded gate on a real full clone (770 commits) against the existing 21 exemptions:

```
::error::Unable to verify embedded bilingual registration history for
  00-governance/architecture-document-management-policy.md:
  Command '['git', 'log', '--format=%H', '-S', '"...policy.md"', 'HEAD', '--',
  'scripts/check_bilingual_docs.py']' returned non-zero exit status 128.
```

All 21 report the same class of error.

**Attribution, which must be stated**: that run used a `--filter=blob:none` partial clone; `git log -S` needs historical blobs, the promisor fetch failed (network), hence `exit 128`. **That is a defect in my environment, not in #423.** It cannot be used to claim the criterion fails on a normal clone.

But one observation does follow and must be recorded: **the new criterion changes the gate from "reads the working tree" to "depends on full history and a working network".** `current_bilingual_gaps()` only did `rglob` over the working tree; it now also does 21 `git log -S` calls. In CI that is fine (`fetch-depth: 0`). Offline or in a shallow clone it fails wholesale.

## 7. Inferences not made

- It does **not** rule that #423's author "deliberately" skipped review. The evidence shows `reviews=0`, checks `steps=0`, merged in 5m56s.
- It does **not** rule that #423's change is wrong. §2.2 treats it as a real fix, and Issue #420's reproduction is on record.
- It does **not** rule that the new criterion fails on a normal clone. §6 attributes the failure to my clone.
- It does **not** read this as "#420 should not have been fixed". It should have been. The question is how it landed.

## 8. Relation to the other registers

| Register | Relation |
|---|---|
| 005 | this register's three `steps=0` runs are another instance of 005's finding, still occurring after 005's window |
| 006 | #423 is the fourth step in 006's chain; it closes the hole in the fix path #418 used |
| 007 | this register records a regression from 007's shape: #418 had one review, #423 has none |
| #400 | #400 concluded "the exemption table is an unaudited expansion surface"; #423 is one implementation of that conclusion |

## 9. Reproduction

```bash
# 1) PR metadata
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/423 \
  | jq '{created_at, merged_at, merged, merged_by: .merged_by.login, additions, deletions, changed_files}'

# 2) review count
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/423/reviews | jq 'length'
# -> 0

# 3) check runs: three failures, all steps empty
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/6d6c6ba57a/check-runs \
  | jq '.check_runs[] | {name, conclusion, steps: (.steps | length)}'

# 4) changed lines
curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/6d6c6ba57a \
  | jq '.files[] | {filename, additions, deletions}'
```

**Register status**: `OPEN` / `ACTIVE` / the gate implementation merged with `reviews=0` / three checks `steps=0` / the fix itself is effective / the process did not satisfy PR-GOVERNANCE-001 §5

---

## 10. The pattern did not stop at #423. It became the default, and this register's author is one of them (2026-11-23)

The body of this register and its §2 measurement of #423 are **not changed**. What follows is a re-measurement on current `main`.

### 10.1 Across 45 merged PRs, the independent review count is zero

Pulled 2026-11-23: the most recent 45 merged PRs, calling `/pulls/{n}/reviews` for each.

| Review situation | Count |
|---|---|
| `reviews == 0` | **40** |
| `reviews > 0`, but the only reviewer is the author | **5** |
| A reviewer other than the author | **0** |

The set of reviewer identities ever seen: `{oahcom}`. The set of authors: `{oahcom}`. They are the same, so by PR-GOVERNANCE-001 §5's own definition — "a review performed through the same connected GitHub identity as the author is not independent" — **0 of 45 merges satisfy it.**

> **Citation currency (added 2026-11-25).** The §5 text quoted above was retired on 2026-11-24; the same identity is no longer by itself a disqualification. **The conclusion stands; the reason has changed.** 40 of the 45 had `reviews == 0` — there was no review at all, and no version of §5 requires one to exist; the other 5 were reviewed only by the author, i.e. by the session that wrote the change, which is not independent under the current clause either. The difference is that the current clause tests the *session*, not the *identity*, so using identity as the test will miscount the next batch.

### 10.2 The platform does not require review, so this is not a bypass

`GET /repos/{owner}/{repo}/branches/main/protection`:

| Item | Value |
|---|---|
| `required_status_checks.strict` | `true` |
| required checks | `GOV-DOC-001 structural checks`, `Branch freshness vs base`, `audit`, `GOV-DOC-002 metadata checks` |
| `required_pull_request_reviews` | **absent** |
| `enforce_admins.enabled` | `true` |
| `allow_force_pushes.enabled` | `false` |
| `restrictions` | `null` (nobody is barred from pushing to `main`) |

**The `required_pull_request_reviews` key does not appear in the response at all.** So nobody bypassed a review requirement — the platform never had one. PR-GOVERNANCE-001 §5's independent-review clause is currently enforced by prose only, by no machine.

At the same time, across 18 workflows (`bilingual-docs.yml`, `gates.yml`, and the rest), **none reads `reviews`, `reviewDecision` or `APPROVED`**. Every `grep -rln` hit is a different context (comments such as "reviewer obligation" inside `check_bilingual_docs.py`).

So §5 is a **norm with no enforcement mechanism**. That is not the same thing as §2.4's `steps=0`: that was a missing executor; this is a missing criterion.

### 10.3 This register's author accounts for 8 of those 45, all with zero review

| PR | Branch | Reviews | Span |
|---|---|---|---|
| #826 | `gov/013-dispatch` | 0 | 2.4m |
| #823 | `adr/embedded-bilingual-shape` | 0 | 6.7m |
| #814 | `gov/014-cwd-split` | 0 | 8.4m |
| #810 | `gov/005-execution-restored` | 0 | 5.1m |
| #777 | `aid/aid-2026-053` | 0 | 3.9m |
| #771 | `adr/evidence-split` | 0 | 9.9m |
| #765 | `aid/aid-2026-052` | 0 | 13.5m |
| #759 | `adr/release-boundary` | 0 | 7.9m |

Of these, #759, #771 and #823 are rulings declaring **`canonical_status: Canonical` / `normative_status: Normative` / `decision_status: Approved`**, with `approver` reading "Owner D acting as owner proxy".

This must be stated plainly rather than softened:

1. **This register's finding applies to this register's author.** The session writing this paragraph merged three documents that call themselves Canonical/Normative/Approved with zero review — and #823's content is a change to the bilingual gate's own criterion.
2. **This is not a bypass.** §10.2 measured it: the platform has no review requirement, so no machine criterion was evaded.
3. **But it is the same shape §1 describes.** §1's judgement on #423 was "a zero-review change to the definition of what counts as compliant". By that criterion, `adr/embedded-bilingual-shape` (#823) and `adr/evidence-split` (#771) land in the same cell.
4. **`approver: "Owner D acting as owner proxy"` is a self-description, not evidence.** Structurally identical to the "attributable Owner act" recorded in 002 §2: at the account layer, `author == merger == approver`, and the three are indistinguishable in any permission record.

This register neither retracts itself nor claims any independence for those three rulings. `OWNER-DECISION-EMBEDDED-BILINGUAL-001` §8.4 already states that a session writing a predicate cannot supply independence for it; the same applies to the ruling itself.

### 10.4 Relation to 002: 002 describes **one event**, this describes **a steady state**

| Register | Subject | Span | Shape |
|---|---|---|---|
| 002 | the Issue #305 delegation instrument | 12 actions in 48m51s | a single self-authorisation event |
| 007 | #418 | review → merge in 12s | self-review, formally compliant |
| 008 (original) | #423 | created → merge in 5m56s | zero review, no form either |
| 008 (this section) | 45 merged PRs | two months continuous | **zero review is the default, not an event** |

The first three record deviations. This section records that **the deviation became the baseline**. 40 of 45 is not "several incidents"; it is a stable distribution.

### 10.5 Executable next steps (this register implements none of them)

Ordered by cost; each is one config change or one script:

1. Turn on `required_pull_request_reviews` on `main`'s branch protection, with `dismiss_stale_reviews: true`. A repository setting, not code.
2. Or: add a workflow that reads `/pulls/{n}/reviews` and returns `HOLD` when `author == reviewer`. That maps directly to §5's definition and needs no new norm.
3. Or: demote §5 from Normative to Informative and record that this repository has no conditions under which independent review can be performed. **This is the most honest and the least work** — if it cannot be enforced, it should not read as though it is.

Exactly one of the three. Keeping the status quo is the worst option: the norm says there is a requirement, the platform says there is not, and the record shows 0 of 45.

### 10.6 Status

`OPEN` / `ACTIVE` unchanged, with: `/ CONTINUOUS — 45 merged PRs, 0 independent reviews / no platform enforcement / author of this register is one of the 45`.

Not `CLOSED`: §9's blocking chain (independent review `NOT_ASSIGNED`) is unchanged, and §10.3 makes that chain apply to this register itself.

---

## 11. None of §10.5's three remedies is available; the correct disposition is §7's `BLOCKED` (2026-11-23)

The body of this register, §2, and §10.1–§10.4 are **not changed**. §10.5's three-way choice is **not withdrawn**, but its premise was wrong: it assumed all three were executable and differed only in honesty and cost. Measured, two deadlock and the third is self-referential.

Ruling: `OWNER-DECISION-REVIEW-INDEPENDENCE-001`. Exception record: `EX-20261123-01`.

### 11.1 Full sweep: not 0 of 45, but 0 of 675

§10.1 sampled the 45 most recent merged PRs. This section walks **all** 675, fetching `/pulls/{n}/reviews` for each:

| | |
|---|---|
| PRs walked | **675** (all pages, not a sample) |
| Review states ever recorded | `{COMMENTED: 169}` |
| `APPROVED` | **0** |
| `REQUEST_CHANGES` | **0** |
| PR authors, all history | `{oahcom}` — 1 |
| Reviewers, all history | `{oahcom}` — 1 |

§5 has **never once been satisfied** in this repository, in any period. This is not a recent regression.

### 11.2 Exactly one identity can write

| | |
|---|---|
| collaborators | **1** — `oahcom`, `{admin, maintain, push, triage, pull}` |
| `oahcom0831-design` permission | **`read`** — `{admin: false, push: false, pull: true}` |
| PRs opened by `oahcom0831-design`, all history | **0** |

A second account exists and has pushed commits (4 of the last 100), but it cannot merge, and its approvals would not count toward a required review — that mechanism counts only reviewers with write access.

### 11.3 Remedies 1 and 2 make `main` permanently unmergeable

§5's last sentence **at the time this section was written** — a review through the same connected identity as the author is not independent, retired 2026-11-24; see §12 — plus a fact that did not change: GitHub forbids approving one's own PR. Combined with §11.2:

- **Remedy 1** (enable `required_pull_request_reviews`): the required approval cannot exist, so every PR is permanently unmergeable. And `enforce_admins: true` means that freeze binds the only identity that could lift it.
- **Remedy 2** (`author == reviewer` returns `HOLD`): all 675 PRs hit it, and so would the 676th.

Neither is a repair. Each is `GOV-NC-2026-11-21-GATE-DEADLOCK-006` reproduced deliberately. 006 is itself part of the evidence: it was resolved `RESOLVED_ON_MAIN` / "released by a self-review merge" (§12, §14) — the previous deadlock was opened by exactly the act §5 forbids. A second gate of the same shape would open the same way.

### 11.4 Remedy 3 is self-referential

Remedy 3 edits a clause of `PR-GOVERNANCE-001`, which is `canonical_status: Canonical` / `normative_status: Normative` / `decision_status: Approved`, and whose §9 states: "Changes to this standard require a bilingual semantic-parity update and an exact-Head governance review."

The governance review §9 requires is the independent review §5 cannot supply. **Demoting §5 requires violating §5.** §10.5 called this one "the most honest and the least work" — neither holds: it is the one that most resembles a decision while being a violation of the standard it edits.

### 11.5 The fourth route, already written in `PR-GOVERNANCE-001` §7

§7 is titled "Platform enforcement is separate from process policy" and says:

> "If the current GitHub plan/visibility does not support required controls for this private repository, record the limitation as BLOCKED and escalate to the repository administrator to select a genuinely enforceable plan/configuration."
>
> "Issue #134 remains OPEN until the platform confirms enforcement and a deliberately failing required check is proven unable to merge through the normal path."

That is the disposition: **`BLOCKED`, escalated to the repository administrator, carried by Issue #134** — open for exactly this since inception.

§10.5 framed the problem as a policy choice. It is not. It is missing a precondition, and §7 already says what to do about a missing precondition.

### 11.6 One act is available to a session, and it has been skipped 675 times

§5's final sentence requires: "Record exceptions explicitly; do not silently waive the requirement."

Measured: 675 PRs, **0 exception records**, no `EX-` file of any kind under `governance-register/`. The violation is that **the waiver was silent**, which §5 explicitly forbids and which was always avoidable.

> **Corrected 2026-11-25.** The first version inserted, between those two sentences, "So the violation is not 'no independent reviewer exists' — that is structural and nobody's fault." That is the same error a third time: writing "nobody opened an independent session" as "no independent session can be opened". §12.4 records that under the current §5 it is an executable backlog, not force majeure. Removing the clause makes this section's conclusion harder, not weaker: if an independent session was always openable, a silent waiver has even less excuse.

`EX-20261123-01` is what that sentence asks for. It waives nothing, changes no PR's disposition, and converts no `HOLD` into `MERGE`.

### 11.7 The quota trigger is the only lawful amendment path

`AI-EXEC-001` v1.1 is **ADOPTED** (PR #256, merge `48a55649`), and its §6 says: "at most 2 exceptions per iteration; exceeding the quota in 2 consecutive iterations triggers a daily governance window for rule revision."

That is the difference between remedy 3 and a lawful amendment: remedy 3 changes §5 by violating §9; the quota clause is **the mechanism the standard itself provides for a control that cannot be satisfied and keeps generating exceptions.**

Measured: the repository is at **675 exceptions, not 2**. Read as a continuous blocked interval it is 1 record — but the interval is **still open** (the second identity still does not exist). Both readings point at one act: **open the window.** The trigger has never fired because in a repository that never records exceptions the quota can never overflow — at a count of zero the clause has no input.

So the order is fixed: record (done) → count (675 vs 2) → open the window (accountable Owner, not done) → amend §5 (Integration Owner, blocked on the window) or supply a second write identity (repository administrator, blocked on a human).

### 11.8 Status

`OPEN` / `ACTIVE` / `CONTINUOUS` unchanged, appending: `/ BLOCKED — PR-GOVERNANCE-001 §7, escalated to the repository administrator (Issue #134) / EX-20261123-01 records 675 PRs and 0 independent reviews / the three remedies were ruled unavailable`.

Not `CLOSED`: §9's blocking chain (independent review `NOT_ASSIGNED`) is unchanged, §10.3 makes it apply to this register itself, and this section's ruling document is `Draft` rather than `Approved` — it claims nothing it cannot show.

## 12. Erratum: §11's central inference does not hold, because it treated an identity-layer fact as a review-layer conclusion (2026-11-24)

**Register status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION` / the conclusions of §11.3, §11.4, §11.7 and §11.8 are **withdrawn by this section**.

### 12.1 What is withdrawn

§11 began from a correct set of measurements and arrived at an incorrect conclusion.

The measurements all stand; this section changes no number: all 675 PRs walked, `APPROVED = 0`, `collaborators = 1`, `oahcom0831-design` permission `read`, the `required_pull_request_reviews` key absent, `enforce_admins: true`. These are verbatim `GET` responses, re-confirmed unchanged on 2026-11-24.

The error was the next step:

> §11.2 measured **how many GitHub accounts can write**; §11.3 read it as **how many reviewers can exist**.

Those are not the same quantity. Before 2026-11-24, §5 defined independence as a property of the GitHub identity, so under that definition "only one identity" did entail "independent review is impossible". But that was not a finding of the measurement — it was **the definition under test being used as the premise of the test**, i.e. one clause being used to prove that the same clause cannot be satisfied.

The clause has been amended on the Owner's baseline (`GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`): independence is a property of the **reviewing session**, not of the GitHub account that carries it. Under the amended definition the same measurement reads differently:

| §11's conclusion | Actual state under the session-level definition |
|---|---|
| §11.3 "remedy 1 makes `main` permanently unmergeable" | **Stands, and this section was earlier wrong to deny it.** `required_pull_request_reviews` counts **users** with write access and forbids approving your own PR; another session under the same account is the **same user**, so the platform approval genuinely cannot be supplied by a session. Remedy 1 still freezes the platform. |
| §11.3 "remedy 2 makes `main` permanently unmergeable" | No. Remedy 2's test is `author == reviewer`, which under the new definition is a **session** comparison: another session is not the authoring session, so it no longer returns HOLD for every PR. |
| §11.3 "the only identity that can lift the freeze is the one it freezes" | Still true, but it constrains only `required_pull_request_reviews`, a **platform** mechanism. It does not constrain the §5 process requirement. §7 already separates the two. |
| §11.4 "remedy 3 is self-referential — demoting §5 requires violating §5" | No. Amending §5 requires an **independent-session review**, and this repository can always open such a session. The self-reference was manufactured by the old definition, not by the clause's structure. |
| §11.7 "the quota trigger is the only lawful amendment path" | No. A second path exists: amend the clause through the §9 bilingual + exact-Head governance review. It was never attempted — not because it is unavailable, but because nobody opened that session. |
| §11.8 "`BLOCKED` — escalated to the repository administrator" | Now **`UNFULFILLED`**. Not blocked by force majeure; executable and unexecuted. |

### 12.2 The nature and direction of the error

This is the fourth error of one kind in this session, and all four point the same way: **a fact at one layer used to underwrite a conclusion at another**.

- First: "the gate passed" taken as "the content is correct".
- Second: "the baseline froze 77 entries" taken as "those 77 are the whole defect set".
- Third: "baseline 77 and content defects 7 do not overlap" taken as "shrinking the baseline repairs the defects".
- Fourth (this section): "there is only one identity" taken as "independent review is impossible".

All four insert an **unexamined equivalence** between evidence and conclusion. The first three were repaired by taking more measurements; this one was repaired by changing the definition — because the two things equated here (account / session) were never at the same layer.

The direction deserves its own note: §11's error **supplied a force-majeure reason for non-performance**. It rewrote "675 things not done" as "things that cannot be done", and on that basis recommended demoting the standard and escalating to an administrator. That class of error is harder to catch than a missing measurement, because its output reads like the most responsible conclusion available.

### 12.3 Why §11 is kept, not deleted

This section deletes none of §11's text, for the same reason as `GOV-REV-2026-11-24-CONVERGENCE-CEILING-034` §9: a record that can rewrite its own conclusions on demand is not a record. §11's measurements are a reusable asset; §11's inference is this register's error. Both must stay where they are.

When citing this register from now on: **cite §11.1/§11.2 for the measurements, §12 for the conclusion**.

### 12.4 The work this actually creates

Under the session-level definition, §9's blocking chain (independent review `NOT_ASSIGNED`) is no longer a blocked state but an **executable backlog**: of the 675 merged PRs, how many should have satisfied §5; of those, which are still worth registering as historical defects; and how the next PR onward will comply. All three are session-work — no second account, no administrator.

This register does not claim those three are done. It withdraws only the claim that they cannot be done.

### 12.5 This section's first version was wrong (corrected same day)

The first version of §12 withdrew the whole of §11.3 on the grounds that "the required approval can be supplied by another session". **That withdrawal was itself wrong and has been reverted.**

`required_pull_request_reviews` counts **users** with write access and the platform forbids approving your own pull request. Another session under the same account is the **same user**, not a second user. The session-level definition therefore changes §5's **process** test; it does not change the platform's **approval count**. Remedy 1 still freezes the platform, and §11.3 was right about that.

The error is the same kind §12 is criticising: §12 used the new session-level definition to overturn a **platform-layer** fact. Session-level independence redefines who counts as an independent reviewer; it does not redefine how GitHub counts approvals. Both layers are called "independence", but one is a process test and the other a platform mechanism — §7 separates them, and this section's first version merged them.

What does survive is the correction to **remedy 2**: under the new definition `author == reviewer` is a session comparison, another session is not the authoring session, so it no longer returns `HOLD` for every PR. That is what the session-level definition actually changes, and the only thing it changes.

Recorded here rather than quietly edited, for the reason given in §12.3: an erratum that can silently correct itself is the same class of problem as the thing it is correcting.
