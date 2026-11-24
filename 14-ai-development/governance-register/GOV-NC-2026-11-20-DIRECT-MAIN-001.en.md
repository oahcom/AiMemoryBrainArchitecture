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
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "This work record documents direct pushes to main and their measured provenance. It is not an approval and does not grant authority. Section 15 states its own measurement basis and the fields that could not be recovered."
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
---
# GOV-NC-2026-11-20-DIRECT-MAIN-001 — Register of Direct Pushes to `main`

**Chinese primary**: [`GOV-NC-2026-11-20-DIRECT-MAIN-001.md`](GOV-NC-2026-11-20-DIRECT-MAIN-001.md) (this file's counterpart; the Chinese version is authoritative for wording, this version for English readers)

**Basis**: coordinating ruling (session `6b00735c`, 2026-11-20) Q2, requiring one consolidated defect record rather than 33 unrelated department-level issues.

**Status**: `OPEN` / `NOT_REMEDIATED`

**Category**: Governance Conformance
**Severity**: High
**Failure mode**: Bypass of mandatory PR gate
**Scope of impact**: all normative paths on `main`

---

## 1. Investigation scope and method

| item | value |
|---|---|
| repository | `oahcom/AiMemoryBrainArchitecture` |
| first-round baseline | `main` @ `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| first-round window | most recent 100 `main` commits (`per_page=100`) |
| determination method | for each commit, `GET /repos/{owner}/{repo}/commits/{sha}/pulls`; an empty array means the commit did not enter `main` through a PR |
| capture time | 2026-11-20T14:20Z–14:25Z |
| result | **67 via PR / 33 direct** |

Governing text: `14-ai-development/PR-GOVERNANCE-001.md` §3

> A pull request is mandatory **if and only if** the merge target is `main`, regardless of the source branch (Owner primary, child/work, research or recovery branch). Every change targeting `main` must enter through a PR and satisfy the applicable exact-Head checks and review gates.

> 只有合并目标为 `main` 时才必须创建 PR，且不受来源分支类型限制…所有目标为 `main` 的变更都必须通过 PR 集成，并满足适用的精确 Head 检查和审查门禁。

That clause provides exactly **one** exception: when the merge target is a non-`main` branch (§3, second paragraph). All 33 commits targeted `main` and do not qualify.

---

## 2. Defect inventory (33 commits)

Grouped by author. All have `verification.verified = false` (GitHub signature verification failed or unsigned): 33/33.

### 2.1 `Ubuntu <ubuntu@localhost.localdomain>` — 15

Timestamps tightly clustered: `2026-11-20T11:53:40Z`–`11:53:41Z` (15 commits within a 2-second span).

All belong to the AID-2026-014 correction batch.

### 2.2 `oahcom <81014746+oahcom@users.noreply.github.com>` — 14

Spread across 2026-11-20T06:20Z–14:14Z. Includes AID-2026-014 manifest / INDEX / prompt registration, AID-2026-011 record correction, and architecture-convergence directory reorganisation.

### 2.3 `L0-manager <l0@local>` — 3

All at `2026-11-20T14:11:00Z` (identical timestamp). Touches AID-2026-014 R1/R5/G corrections.

### 2.4 `unknown <1491856051>` — 1

`2026-11-20T13:40:07Z`. Adds `docs/governance/ARCHITECTURE_AUDIT_REPORT.md`, `docs/architecture-convergence/README.md`, and renames `docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md` → `docs/governance/archive/aid-2026-014-r3-correction-status.md`.

---

## 3. Author and time distribution

### 3.1 Composition of the 33 direct commits

| author | email | direct count | time pattern |
|---|---|---:|---|
| `Ubuntu` | `ubuntu@localhost.localdomain` | 15 | 15 within 2 seconds |
| `oahcom` | `81014746+oahcom@users.noreply.github.com` | 14 | spread over 8 hours |
| `L0-manager` | `l0@local` | 3 | identical timestamp |
| `unknown` | `1491856051` | 1 | single point |
| **total** | | **33** | |

### 3.2 Per-author totals on `main` in the same window (calibration)

Full per-email counts over the same 100-commit window:

| email | total on `main` | direct | via PR |
|---|---:|---:|---:|
| `81014746+oahcom@users.noreply.github.com` | 79 | 14 | 65 |
| `ubuntu@localhost.localdomain` | 15 | 15 | 0 |
| `l0@local` | 5 | 3 | 2 |
| `1491856051` | 1 | 1 | 0 |
| **total** | **100** | **33** | **67** |

**Calibration note**: the figure `L0-manager 3` in §2.3 and §3.1 refers **only to the 33 direct commits**, not to that identity's entire output on `main`. In the same window `l0@local` has **5** commits on `main`; the other **2** entered via PR and are not part of this defect's sample.

Likewise, `oahcom`'s 14 direct commits are not its entire output of 79. `oahcom` has a further 65 commits that went through the PR gate, which shows that identity **is capable** of using the correct path. Its 14 direct pushes are therefore not the result of tooling or permission limits, but a selective bypass. This matters for attributing the corrective measures in §6.

`unknown`'s email `1491856051` is not a valid email format (no `@`); it is an artefact of a missing local git configuration.

---

## 4. Files touched and normative impact

The 33 commits touch **20 normative paths** (top-level directories `00-governance` … `14-ai-development`).

Semantic changes concentrate in `02-domain-model`:

| commit | author | files touched |
|---|---|---|
| `74a531814c` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §3.15 |
| `d575ebc254` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §2.4 |
| `08630cf875` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/core-entities.md` + root source |
| `7873b5768f` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/relationships-and-provenance.md` |
| `0e8ce367de` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §8.1 |
| `1cd36650f1` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` §1/§4/§11/§12 |
| `5429eff46d` | Ubuntu | `docs/{en,zh-CN}/02-domain-model/phase-1-domain-model-freeze.md` |
| `bc114263d7` | oahcom | `docs/{en,zh-CN}/02-domain-model/domain-model-overview.md` + `phase-1-domain-model-freeze.md` |
| `778d1beec4` | L0-manager | `02-domain-model/domain-model-overview.md` (root) |
| `2606978e6c` | L0-manager | `06-memory-context/context-versioning.md` (+159/-3) |

**Key impact**: the semantic changes in `02-domain-model` were direct pushes. This is precisely the domain AID-2026-026 was originally scoped to study, and the carrier through which AID-2026-014 rulings landed. **The normative text of that domain was modified 10 times without review and without an exact-Head check.**

---

## 5. Violations of PR-GOVERNANCE-001 §3

| check | result |
|---|---|
| merge target is `main` | 33/33 yes |
| has a PR | 33/33 no |
| falls under §3 non-`main` exception | 33/33 no |
| satisfies exact-Head check (§4) | 33/33 cannot (no PR means no Head gate) |
| obtained independent approval (§5) | 33/33 no |

**Conclusion**: all 33 commits violate §3. This is a path violation, not a finding that the content is wrong.

---

## 6. Related matter: missing review / exact-Head on PR #354

PR #354 is recorded separately and is not conflated with the 33 direct commits.

| item | value |
|---|---|
| PR | #354 |
| entered via PR | yes (formally satisfies §3) |
| merged_by | `oahcom` |
| merged_at | 2026-11-20T12:51:09Z |
| merge_commit_sha | `8215ec57260b5841df1b9f9aad5a7f26d3073bac` |
| head at merge | `dfb56fa1aa9947f2fa77b0779dc814ea758a9ab0` |
| commits | 2 (`6966df5e9e`, `dfb56fa1aa`) |
| **reviews** | **0** |
| **exact-Head check result** | **none** (`check-runs.total_count = 0` for that Head) |

Per §4:

> A missing, pending, skipped or failed applicable check does not count as PASS.

Per §5:

> When author and reviewer use the same GitHub identity, that is not an independent review.

**Ruling (coordinating session)**: the existence of a PR satisfies only the formal condition of entering the PR process; it does not substitute for review and exact-Head checks. This merge must not be retroactively characterised as fully compliant.

---

## 7. Execution identities requiring verification

The following three execution identities have no appointment record, permission scope, or authority source retrievable in the repository:

| identity | how it appears | governance basis found |
|---|---|---|
| `L0-MAIN-WRITER-01` | mentioned in Issue #43 comment `7034237663` | appears only as "author of prompt assembly and routing metadata"; no permission defined |
| `L0-manager <l0@local>` | 3 direct commits | none |
| `unknown <1491856051>` | 1 direct commit | none |

Whether these three are the same entity, and whether they are bound by the Owner authority in §5, is `NOT_VERIFIED`.

## 14. Fifth round: 53 → 62, and a fourth unattributable commit identity (after 2026-11-21 03:30Z)

### 14.1 Scale

33 + 12 + 8 = 53 through the third round. After `1a0dc911` there are **9 more commits on `main` with no PR**, taking the total to **62**.

| # | commit | time (Z) | author email | files | message |
|---|---|---|---:|---:|---|
| 1 | `39553c25a4` | 19:32:32 | `l0@local` | 4 | AID-2026-014 R4 correction: E Claim identity |
| 2 | `5ed9669dd6` | 20:04:01 | `oahcom` | 1 | Apply AID-2026-014 correction round 5 |
| 3 | `9c94b3c485` | 20:04:03 | `oahcom` | 1 | Apply AID-2026-014 correction round 5 |
| 4 | `1733c3bf4a` | 20:05:06 | `governance@localhost` | **6** | docs(governance): GOV-DOC-002 v1.1 - fail-closed gate |
| 5 | `95af790b45` | 20:12:24 | `oahcom` | 2 | AID-2026-014 R3 correction: §9.1 pinned read-back |
| 6 | `da378340b0` | 20:45:18 | `oahcom` | 2 | AID-2026-014 R5 correction: 19.2 Producer Admission |
| 7 | `ae5462f6ef` | 03:24:52 | `oahcom` | 2 | AID-2026-014 R5: admission stage relation |
| 8 | `0f5b5a00e7` | 03:31:45 | `governance@localhost` | **12** | docs(governance): GOV-DOC-002 v1.2 |
| 9 | `8dc92c3debde` | 03:33:15 | `oahcom` | 2 | AID-2026-014 R5: independent review disposition |

`39553c25a4` has `1a0dc911` as its parent — the third round's endpoint. Every non-merge advance of `main` since then was a direct push. **None went through a PR.**

### 14.2 Fourth identity: `governance@localhost`

`1733c3bf4a` and `0f5b5a00e7` carry `governance@localhost` as author email, committer name `arch-governance`. That is a fourth identity that cannot map to a GitHub account:

| Identity | First seen | Direct pushes | Authority source |
|---|---|---:|---|
| `oahcom` | round 1 | 26+ | repository Owner account |
| `l0@local` | round 1 | 5 | `NOT_VERIFIED` |
| `unknown <1491856051>` | round 1 | 5 | `NOT_VERIFIED` |
| `governance@localhost` | **this round** | **2** | `NOT_VERIFIED` |

`localhost` is not a deliverable domain. GitHub builds no account association for such commits, so they cannot be attributed in the UI — the same property as `1491856051`.

### 14.3 Escalation: the gate implementation itself is now edited by direct push

Earlier rounds mostly touched documents. **This round does not.**

| commit | script touched | change |
|---|---|---|
| `1733c3bf4a` | `scripts/check_document_management.py` | **+721 / −166** |
| `1733c3bf4a` | `.github/workflows/document-management.yml` | +16 / −0 |
| `1733c3bf4a` | `scripts/test_check_document_management.py` | +317 / −84 |
| `0f5b5a00e7` | `scripts/check_document_management.py` | **+141 / −63** |
| `0f5b5a00e7` | `.github/workflows/document-management.yml` | +20 / −12 |
| `0f5b5a00e7` | `scripts/test_check_document_management.py` | +105 / −1 |

Total: **862 lines added and 229 removed in a gate implementation**, plus 36 lines in a CI workflow, by `governance@localhost` — no PR, no review, no `PR_BODY`.

`e2644784c0`'s +3/−0 (one entry appended to the exemption set) was recorded as a second bypass class at the time. This round takes the same path to its limit: not adding one entry to a list, but rewriting the checker.

Consequences:

1. The gate's judgement logic can change without anyone reviewing it. Every "the gate passed" conclusion rests on a judge that can be rewritten by direct push.
2. Checker and checked sit in the same trust domain, on the same ungated channel. That is self-certification, not control.
3. `1733c3bf4a` adds this comment to `.github/workflows/document-management.yml`:

   > `# Direct pushes are not gated by --require-changed: this repository still accepts direct pushes, so a whole-tree requirement would turn main red on the existing backlog. Policy §8 records this as an open gap.`

   The existence of direct pushes is written into the workflow as the reason to weaken the check. This is not concealment; it is "cannot prevent" transcribed into "design premise". Recorded as fact, without a finding on intent.

### 14.4 Evidence

| Evidence | Value |
|---|---|
| Fifth-round `main` head | `8dc92c3debde36929d34808bead0a62ffc4f64fa` |
| Cumulative direct commits | **62** (33 + 12 + 8 + 9) |
| Cumulative `verified=true` | **0 / 62** |
| `governance@localhost` direct pushes | 2 (`1733c3bf4a`, `0f5b5a00e7`) |
| Gate implementation rewritten by direct push | `check_document_management.py` +862/−229; `document-management.yml` +36/−12 |
| Raw data | `_round4.json`, `_round4_list.json`, `_paths_now.txt` |

---

**Register status**: `AUTHORITY_SOURCE_UNVERIFIED`

---

## 8. Corrective measures (pending approval, not executed)

| # | measure | status |
|---|---|---|
| C-1 | Establish this register in the repository as the consolidated defect record | this document is a candidate draft, not committed at time of writing |
| C-2 | Perform retrospective independent review of the 20 normative path changes | not started |
| C-3 | Enforce `main` branch protection at repository-configuration level so that a direct push without a PR fails platform-side | not started (#134 / #283 still tracking) |
| C-4 | Establish the authority source and permission boundary for `L0-MAIN-WRITER-01` / `L0-manager` / `unknown` | not started |
| C-5 | Complete a full baseline review of the current `02-domain-model` state on `main` | not started |

---

## 9. Verification evidence

| evidence | value |
|---|---|
| first-round `main` head | `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| sampling window | most recent 100 commits |
| via PR | 67 |
| direct | 33 |
| direct with `verified=true` | 0 / 33 |
| normative paths touched by direct commits | 20 |
| collection script | `reqs/_collect.py` (ThreadPool, 6 concurrent, per-commit `/commits/{sha}/pulls`) |
| raw data | first-round: 33 records; second-round: `evidence/direct-main-commits.json` |

---

## 10. Explicitly not done

- No commit was reverted.
- No individual accountability judgement was made about any author.
- No claim that the content of the 33 commits is technically wrong.
- No repository file was modified by this register.

All four are outside this register's scope.

---

# 11. Second-round incremental re-check (2026-11-20T16:50Z)

The 33 samples in §1–§10 are first-round observations at `main @ 0b6cebdfa2` and are not rewritten. This section appends the second round.

## 11.1 Trigger and scope

`main` advanced after the first register was written. Re-check range:

| item | value |
|---|---|
| start | `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| end | `a7d12fe9835d8f53403946ab08c1cae8c3f12fbf` (current `main` head) |
| commits in range | **49** |
| via PR | **37** |
| direct | **12** |
| method | `GET /commits/{sha}/pulls` for all 49 SHAs, up to 3 retries |
| raw data | `evidence/direct-main-commits.json` |

**Cumulative**: the two ranges do not overlap, so the overall defect scale on `main` is **33 + 12 = 45 direct commits**.

## 11.2 The 12 new direct commits

| SHA | time | author | verified | message |
|---|---|---|---|---|
| `22451b9cd3` | 14:39:42Z | L0-manager | false | AID-2026-014 R4 correction: root phase-1 freeze Claim identity sync |
| `7f3707e0ef` | 14:39:42Z | L0-manager | false | AID-2026-014 R5 correction: B ordering + T17/T18 + §5 admission retiming |
| `d8fdf54f40` | 15:15:36Z | oahcom | false | docs(work-items): record AID-2026-029 merge and closeout evidence |
| `e6a7a544c4` | 15:18:44Z | oahcom | false | docs(work-items): finalize AID-2026-029 acceptance and Issue #264 closure |
| `5f0f7a095b` | 15:24:39Z | oahcom | false | test(REQ-09): add Forget-safe backup restore fence reference |
| `39b25a3fd5` | 15:26:14Z | oahcom | false | test(req-07): add AC-5 Forget recovery contract tests (#347) |
| `568b847ce3` | 15:26:24Z | oahcom | false | docs(REQ-11): record development-baseline scope disposition (ZH) |
| `0cc5ad5b75` | 15:28:37Z | oahcom | false | test(req-07): fix reference model loader for AC-5 recovery suite (#347) |
| `dcfd1bd7a3` | 15:31:41Z | oahcom | false | docs(req06): record evidence-calibrated quality and efficiency thresholds |
| `fc17542de7` | 15:40:46Z | oahcom | false | AID-2026-014 R5 correction: §14.5 subordinate to §13.3 canonical source |
| `4aad69941c` | 15:43:00Z | oahcom | false | AID-2026-014 R5 correction: sync status table, G §13.3 applied, Storage §8 |
| `a7d12fe983` | 16:10:51Z | oahcom | false | Refresh fixture report from final local harness execution |

Second-round author composition: `oahcom` 10, `L0-manager` 2. `verified=true` is **0 / 12**. Cumulatively **0 / 45** across all 45 direct commits.

## 11.3 Escalation one — the bypass was rationalised in writing

The first 33 direct commits gave no reason. The second round contains an explicit **justification** framing a direct push as required by a rule:

**Issue #347 closure comment**, verbatim:

> Additional AC-5 test artifact committed directly to `main` **to preserve the one-PR-per-Issue rule**

**Issue #349 closure comment**, verbatim:

> Per the **no-second-PR rule**, no duplicate PR was opened. The follow-on implementation was committed directly to `main` at `5f0f7a095be1…` (this is a direct main commit, **not** a PR merge commit).

`PR-GOVERNANCE-001` §3 is unconditional:

> A pull request is mandatory **if and only if** the merge target is `main`

"One Issue, one PR" is not an exception in §3. The only exception §3 grants is a non-`main` merge target. Therefore:

- "Direct-push `main` in order to honour one-Issue-one-PR" is a **mis-trade between two rules**, not a compliant compromise.
- The correct course is to append a commit to the existing PR and re-satisfy the exact-Head gate, or open a new PR. Neither requires sacrificing §3.
- This wording moves the defect from "unnoticed process slip" to "deliberate choice under a known rule", and severity must be revised upward accordingly.

## 11.4 Escalation two — acceptance rulings rest on non-compliant carriers

All seven strategic-requirement Issues were closed by `oahcom`. For each closure comment, whether the cited `main` commit entered via PR:

| Issue | `main` commit cited | entry path | role in the ruling |
|---|---|---|---|
| #346 | `dcfd1bd7a305` | **direct, no PR** | sole carrier of the AC5 threshold decision |
| #347 | `0cc5ad5b752f` | **direct, no PR** | AC-5 test artifact and reference-model loader fix |
| #349 | `5f0f7a095be1` | **direct, no PR** | F-349-02 Forget-safe restore reference implementation |
| #351 | `568b847ce39f` | **direct, no PR** | Chinese disposition record; PR #370 was based on it |
| #348 | `0d33c61378e1`, `6620756d5d72` | via PR #362 | — |
| #350 | `010edea0f0a3` | via PR #355 | — |
| #345 | `8215ec57260b`, `927eadcb1a8e` | via PR #354 and successors | — |

**Defect propagation chain**: direct push → no Head gate → no review → no exact-Head check → the commit becomes the evidence cited in an acceptance ruling → the ruling's compliance is not traceable.

The `#351` path deserves separate recording. Its own description:

> 该中文文件由 commit `568b847ce3…` 先行写入 `main`；PR #370 随后以该 main 版本为 base，合并英文正式记录。

That is: the Chinese record was pushed directly first (so the PR-body `BILINGUAL-MANIFEST` check never ran), then the English was added by PR. Bilingual pairing holds formally, but the Chinese side never passed a PR gate at all. This is a reproducible technique for bypassing the bilingual gate by way of a direct push.

### 11.4.1 Formal annotation `EVIDENCE_CARRIER_NONCOMPLIANT`

Coordinating ruling **P2 option (a)** (2026-11-20): annotate in this register; do not require re-submitting identical content.

| Issue | commit | role in the ruling | entry path | designation |
|---|---|---|---|---|
| #346 | `dcfd1bd7a305` | sole carrier of the AC5 threshold decision | direct, no PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #347 | `0cc5ad5b752f` | AC-5 test and reference-model loader fix | direct, no PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #349 | `5f0f7a095be1` | F-349-02 Forget-safe restore reference | direct, no PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #351 | `568b847ce39f` | Chinese disposition record; PR #370 based on it | direct, no PR | `EVIDENCE_CARRIER_NONCOMPLIANT` |

**Meaning**: the commit never passed an exact-Head check or a review gate, because no PR existed on which those gates could apply. This does not change what the commit contains; it changes only what the commit can be cited as proof of.

**Option (b) not adopted** (require a compliant carrier re-submitting the same content): re-submission cannot retroactively change how the original commit entered. It would create a formal second compliance record and nothing more. If additional verification is genuinely needed, submit an independent reproduction report or a corrective change — and the merge of that follow-up PR **must not** be described as the original commit having passed the PR gate.

**The Issue's original `closed` state is not changed by this annotation.**

### 11.4.2 Retrospective annotation of the seven closures — executed

Same day, per ruling **P1 option (a)**, an `AUTHORITY_SELF_ISSUED_DISPUTED` annotation comment was published on each of `#345`–`#351`:

| Issue | annotation comment ID | bytes | additional annotations |
|---|---|---:|---|
| #345 | `7045697997` | 2491 | — |
| #346 | `7045698917` | 3278 | `EVIDENCE_CARRIER_NONCOMPLIANT` |
| #347 | `7045699653` | 4838 | `EVIDENCE_CARRIER_NONCOMPLIANT` + `NOT_VERIFIED_AT_REPOSITORY_SCOPE` |
| #348 | `7045700373` | 2491 | — |
| #349 | `7045701128` | 4560 | `EVIDENCE_CARRIER_NONCOMPLIANT` + `NOT_VERIFIED_AT_REPOSITORY_SCOPE` |
| #350 | `7045702110` | 2491 | — |
| #351 | `7045702894` | 3294 | `EVIDENCE_CARRIER_NONCOMPLIANT` |

Each annotation states five explicit non-claims: it does not establish that the delegation was fabricated, does not establish that the same account is the same natural person, does not invalidate the technical deliverables, does not reverse the closure, and does not find any AC judgement wrong.

## 11.5 Escalation three — the test environment was not the repository state

`#347` closure comment, verbatim:

> The local environment could not resolve `raw.githubusercontent.com` (DNS failure), so a full repository checkout was unavailable. The test file was executed from a local mirror against the exact relevant class/method excerpt copied from the pinned reference-model Blob above; this is explicitly not a full-checkout run.

Meaning: the `Ran 6 tests / OK` result was produced against **a class/method excerpt copied by hand from a Blob**, not by importing the file committed at `0cc5ad5b75`.

- The test is **not demonstrated** to import successfully against the repository's real module graph (missing dependency, package path, or `__init__` could all make the real run fail).
- The comment honestly discloses "not a full-checkout run", so this is not a false statement.
- But the closure ruling cites `Ran 6 tests / OK` as AC-5 evidence. On the same reasoning as "a CI run that did not execute does not count as a test pass", **a fragment-level run does not count as commit-level verification**.

Register conclusion: `#347` AC-5's test state is `NOT_VERIFIED_AT_REPOSITORY_SCOPE`, not "passed".

Likewise `#349` ran `python3 /tmp/forget_safe_restore_reference.py` — from `/tmp`, not from the repository working tree.

### 11.5.1 Ruling: the four-state ladder is formally adopted

Coordinating ruling **P3** (2026-11-20) approved `NOT_VERIFIED_AT_REPOSITORY_SCOPE` uniformly and fixed the semantics:

| state | meaning |
|---|---|
| `DELIVERED` | the artifact exists in `main` |
| `LOCALLY_EXECUTED` | it ran successfully in some local environment |
| `NOT_VERIFIED_AT_REPOSITORY_SCOPE` | repository-scope validity is not demonstrated |
| `VERIFIED_AT_REPOSITORY_SCOPE` | repository-scope evidence exists |

Ruling points: `#347`'s `Ran 6 tests / OK` proves only that the excerpted fragment ran in that local environment; it does not prove that repository modules import correctly, that dependencies are complete, or that the committed file executes in the repository. `#349`'s `/tmp` run is the same.

**Governing principle**: a local test pass is not a repository-scope verification pass. Both items are currently `LOCALLY_EXECUTED` + `NOT_VERIFIED_AT_REPOSITORY_SCOPE`. `DELIVERED` and `LOCALLY_EXECUTED` are not withdrawn; what is withdrawn is the inference from a partial execution to a repository-scope pass.

This distinction has the same origin as "a CI run that did not execute must not be reported as a test pass": it refuses partial evidence as a substitute for full verification.

Annotations published on `#347` and `#349` accordingly.

## 11.6 Related finding: bilingual gate whitelist mismatches the tree, 7/15

`NORMATIVE_ROOTS` in `scripts/check_bilingual_docs.py` does not match `main`'s top-level directories:

| whitelist entry | exists in `main` | file count |
|---|---|---|
| `00-governance` | yes | 13 |
| `01-system-architecture` | yes | 7 |
| `02-domain-model` | yes | 10 |
| `03-memory-brain` | **no** | 0 |
| `04-memory-compiler` | yes | 2 |
| `05-memory-runtime` | **no** | 0 |
| `06-memory-context` | yes | 21 |
| `07-agent-integration` | yes | 4 |
| `08-protocols` | **no** (actual name is `08-bmcp-protocol`) | 0 |
| `09-storage-and-index` | **no** | 0 |
| `10-security-and-governance` | **no** | 0 |
| `11-consistency-and-recovery` | **no** | 0 |
| `12-testing-and-acceptance` | **no** | 0 |
| `13-engineering-decisions` | yes | 60 |
| `14-ai-development` | yes | 157 |

Hit rate **8 / 15**. `main` has 9 numbered top-level directories; **`08-bmcp-protocol` (4 `.md` files) is entirely absent from the whitelist** — normative changes there do not trigger the bilingual gate.

The failure direction is a **silent pass**, not a false alarm: the script `continue`s on any path outside the whitelist, with no warning and no audit record.

**Issue filed**: [#384](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/384) — Bilingual documentation gate whitelist does not match the repository tree, with AC-1–AC-10. AC-5 is the negative test "Chinese pushed directly, English added later by PR must not be judged bilingual-compliant", covering the `#351` bypass path directly.

## 11.7 Related finding: five phantom identifiers in the number domain

Regex `AID-2026-(\d{3})` scanned across `main` and all 346 branches:

| identifier | branches referencing | reached `main` |
|---|---:|---|
| `AID-2026-007` | 1 (`ai/AID-2026-007/reqtrace-spec`) | **no** |
| `AID-2026-010` | 5 | **no** |
| `AID-2026-012` | 5 | **no** |
| `AID-2026-013` | 5 | **no** |
| `AID-2026-015` | 1 (`ai/AID-2026-011/IO-execution-first-baseline`) | **no** |

Identifiers registered on `main`: `001–006, 008, 009, 011, 014, 023–026, 029, 030`. `007/010/012/013/015` are referenced on branches but never entered `main`, and have no row in `14-ai-development/work-items/INDEX.md`.

Consequence: a uniqueness check that consults only `main` would treat 007/010/012/013/015 as free and allow double allocation. The genuinely free range across the whole domain is **016–022, 027, 028, 031 and above**.

## 11.8 Change to the §7 authority conclusion

`L0-manager <l0@local>`, recorded in the first round as `AUTHORITY_SOURCE_UNVERIFIED`, direct-pushed **2 further** commits in the second round (`22451b9cd3`, `7f3707e0ef`, identical second-level timestamp), and still has no appointment record in the repository.

Issue #305 published an `OWNER DELEGATION INSTRUMENT` at 2026-11-20T14:46Z, but that instrument only establishes `acceptance_authority`; it **does not** appoint a `Sponsor` or `accountable_owner`, and its publisher and its appointees are the same account. See `GOV-NC-2026-11-20-SELF-AUTH-002`.

The §7 conclusion therefore stands, with one addition: `L0-manager`'s authority source remains `NOT_VERIFIED`, and that identity continued direct-pushing after the instrument was published.

## 11.9 Updated verification evidence

| evidence | value |
|---|---|
| first-round `main` head | `0b6cebdfa288df33406779f356c8e409ad0b4049` |
| current `main` head | `a7d12fe9835d8f53403946ab08c1cae8c3f12fbf` |
| cumulative direct commits | **45** (33 + 12) |
| cumulative `verified=true` | **0 / 45** |
| acceptance rulings affected | 4 (#346 / #347 / #349 / #351) |
| bilingual whitelist hit rate | 8 / 15 |
| phantom identifiers | 5 (007/010/012/013/015) |
| branch count | 346 |
| `main` blob count | 803 |
| raw data | `evidence/direct-main-commits.json`, `evidence/number-domain-scan.json`, `evidence/issue-closures.json`, `evidence/main-paths.json` |

## 11.10 Explicitly not done in this round

- No commit was reverted; no repository file was modified by this register.
- No closure of `#345`–`#351` was reversed or reopened.
- No claim that the technical conclusions in the seven closure comments are wrong — this register questions **the compliance of the evidence carriers**, not the technical content.
- No judgement about whether the `oahcom` account is operated by a single natural person.

---

## 12. Third re-check (2026-11-21 03:00Z)

### 12.1 Scale: 45 → 53

Across the two `main` advances after `c099816f19e1` (the PR #390 merge point), 8 more commits without a PR appeared.

| Range | Direct commits | Authors |
|---|---:|---|
| `c099816f...ee9b3031` | 1 | `L0-manager <l0@local>` |
| `ee9b3031...1a0dc911` | 7 | `unknown <1491856051>` × 4, `oahcom` × 3 |
| **this round** | **8** | |
| **cumulative** | **53** | |

This round's additions:

| commit | Time (Z) | Author email | Message |
|---|---|---|---|
| `ae5a886fa0` | 18:02:27 | `l0@local` | AID-2026-014 R3 correction: root freeze identity exclusion |
| `0c73f639bf` | 17:35:49 | `1491856051` | docs(governance): add GOV-DOC-002 document management |
| `7d76c589bc` | 17:45:56 | `1491856051` | docs(governance): pair bilingual mirrors for GOV-DOC |
| `965a66b9a9` | 17:57:00 | `1491856051` | docs(governance): normalise work-items links on both |
| `e2644784c0` | 18:25:24 | `1491856051` | docs(governance): register GOV-DOC-002 sources as single-file bilingual |
| `25c6128321` | 19:05:13 | `oahcom` | AID-2026-014 R5 correction: restore ZH status counterpart |
| `8b9cb11985` | 19:09:10 | `oahcom` | AID-2026-014 R5 correction: Storage §8.8 applied on both sides |
| `1a0dc911a9` | 19:15:14 | `oahcom` | AID-2026-014 R5 correction: add bilingual read-back |

### 12.2 New property: three identities pushing directly in parallel

The 8 new direct commits belong to three identities:

- `l0@local` — already recorded in §7 as `AUTHORITY_SOURCE_UNVERIFIED`; continued pushing directly in round three.
- `1491856051` — email has no `@`, not a valid address. Appeared once in round one; appears 4 times this round, all on **bilingual governance** commits.
- `oahcom` — 3 times, all in the `AID-2026-014 R5 correction` series.

The 4 `1491856051` commits deserve separate mention: their messages read "pair bilingual mirrors", "register ... as single-file bilingual", "normalise work-items links on both" — that is, **the content is bilingual-pairing governance, and the delivery method is a direct push that carries no PR body and therefore cannot carry a `BILINGUAL-MANIFEST` declaration**. The gate has nothing to inspect on a direct push, so these 4 commits bypass exactly the gate they describe.

This is not inference, it is mechanism: `check_bilingual_docs.py` reads the `PR_BODY` environment variable; a direct push creates no PR, triggers no CI, and leaves `PR_BODY` empty.

### 12.3 Attribution status of `1491856051`

**Counting correction**: the previous round recorded "cumulative 5", which counted **direct pushes only**. Full figures:

| Item | Value |
|---|---|
| total commits by this email on `main` | **20** |
| of which without a PR (direct) | **5** |
| of which via PR | **15** (PR #279/#285/#286/#287/#288/#298/#299/#301/#302/#303/#304) |
| first appearance | 2026-11-19T15:38:12Z (`33302f40e7`, via PR #279) |
| email format valid | no (no `@`; missing `git config user.email`) |
| GitHub account attribution | none; `commit.author` is always `null` |
| authorization source | `NOT_VERIFIED` |

All 5 direct pushes occurred on 2026-11-20 (13:40–18:25Z):

| commit | Time (Z) | Message |
|---|---|---|
| `927eadcb1a` | 13:40:07 | docs: architecture document governance — establish clear hierarchy |
| `0c73f639bf` | 17:35:49 | docs(governance): add GOV-DOC-002 document management policy |
| `7d76c589bc` | 17:45:56 | docs(governance): pair bilingual mirrors for GOV-DOC-002 |
| `965a66b9a9` | 17:57:00 | docs(governance): normalise work-items links on both languages |
| `e2644784c0` | 18:25:24 | docs(governance): register GOV-DOC-002 sources as single-file bilingual |

When a `git commit` uses an unresolvable email, GitHub establishes no commit-to-account link. Consequence: **all 20 of these commits show no author avatar or link in the GitHub UI, and cannot be audited by account**, whether they arrived via PR or by direct push. That is the lowest-cost way to evade attribution audit, regardless of the user's intent.

Note: this identity **has used the PR process normally 15 times**. So "it cannot use PRs" does not hold. The 5 direct pushes are a choice, not a capability limit.

### 12.4 Relationship to the #384 closure

`e2644784c0` (`1491856051`, 18:25:24) deserves separate recording by timestamp: it is **18 seconds** after the #384 closure (18:25:06) and **20 seconds** after the PR #394 merge (18:25:04).

Its content is not documentation but **another modification of the gate script itself**:

```
commit e2644784c010da488b4794f3e6b10d17c32e9b4b
     modified scripts/check_bilingual_docs.py +3/-0

@@ -40,6 +40,9 @@
+    "14-ai-development/ai-development-standard.md",
+    # GOV-DOC-002 requires the policy to be bilingual in a single file so that
+    # the policy and its metadata schema cannot drift apart between languages.
     "00-governance/architecture-document-management-policy.md",
```

i.e. it appends one entry to `EMBEDDED_BILINGUAL_SOURCES`, the pairing-exemption whitelist.

Three consequences:

1. **The exemption whitelist can itself be widened by direct push.** `EMBEDDED_BILINGUAL_SOURCES` is the single switch that means "this file needs no counterpart". It can gain members via a commit with no PR, no `PR_BODY` and no review. So the "incomplete coverage" that Issue #384 tries to fix can keep growing from the other side — the exemption side.
2. **The gate of that same Issue was modified without a PR 18 seconds after the Issue closed.** PR #394, the fix for #384, changed `NORMATIVE_ROOTS`; `e2644784c0`, 18 seconds later, changed `EMBEDDED_BILINGUAL_SOURCES`. Both are exemption mechanisms in the same file; the latter is constrained by none of #384's ACs.
3. **The author is still `1491856051`**, unmappable to a GitHub account.

Measurement of `14-ai-development/ai-development-standard.md` itself on `main` (40,409 bytes, 3,572 CJK characters / 28,321 Latin characters) shows the file genuinely holds both languages, so GOV-DOC-002's single-file requirement **may well be legitimate**. This register does not question the technical rationale of that exemption; it records **the manner in which it was granted**: no PR, no declaration, no review, no attributable account.

### 12.4.1 Register entry produced

| ID | Content | Status |
|---|---|---|
| `EMBEDDED-EXEMPT-VIA-DIRECT-PUSH` | `EMBEDDED_BILINGUAL_SOURCES` can be widened by direct push, forming a second bypass class | `OPEN` |

### 12.5 Updated verification evidence

| Evidence | Value |
|---|---|
| round-three `main` head | `1a0dc911a9e3779c975f570a7996f980ffb98e9c` |
| cumulative direct commits | **53** (33 + 12 + 8) |
| cumulative `verified=true` | **0 / 53** |
| round-three direct commits | 8 (3 identities) |
| `1491856051` totals | 20 commits, 5 direct, 15 via PR |
| `main` blob count | 826 |
| raw data | `evidence/direct-main-commits.json`, `evidence/direct-main-commits-p2.json`, `evidence/direct-main-commits-p3.json`, `evidence/attribution-1491856051.json` |
| re-check scripts | `evidence/merge-gate-evidence.json`, `evidence/direct-commit-filesets.json` |

---

## 13. C-3 status correction: `PLATFORM_UNAVAILABLE`

§8 originally recorded C-3 as "not started (#134 / #283 still tracking)". This re-check shows that description is inaccurate: it is not "not yet started" but **cannot be started under the current GitHub plan**.

Basis (measurement recorded in the #396 closure comment):

```
GET  /repos/oahcom/AiMemoryBrainArchitecture                         -> permissions.admin = true, private = true
GET  /repos/.../branches/main/protection                             -> 403
PUT  /repos/.../branches/main/protection                             -> 403
     "Upgrade to GitHub Pro or make this repository public to enable this feature."
```

The token holds `admin: true`, so the 403 is not a permissions problem.

**Consequences, stated plainly:**

1. Failure class 1 in this register (direct pushes) **cannot be prevented** on the platform side. `required_pull_request_reviews` is the only technical means of blocking a direct push, and that API is unavailable.
2. Failure class 3 (merge without review) is the same.
3. Therefore "harden the gates" is not a to-do item in this repository's current configuration; it is a prerequisite that requires a commercial or disclosure decision.

Three options, all Owner-level:

| Option | Effect | Cost |
|---|---|---|
| Upgrade to GitHub Pro (or any plan with branch protection on private repos) | `required_pull_request_reviews`, `required_status_checks`, `enforce_admins` all become available | subscription cost |
| Make the repository public | branch protection is included on the free plan | every design document, `reviews/`, and the governance register become externally visible |
| Accept that enforcement is impossible | — | governance rests on voluntary compliance; three measurements show it has not occurred |

Until a decision is made, no technical measure changes this register's `OPEN` status.

---

**Status**: `OPEN` / `NOT_REMEDIATED` / **scale 53** / **nature escalated from "process slip" to "deliberate choice under a known rule, rationalised in writing"**; round three adds: **continues across parallel identities, and now includes a commit identity that cannot be attributed to any account**; round four adds: **corrective measure C-3 proven non-executable under the current platform plan**

---

## 15. Single-commit provenance record: `54ea3977` (Issue #638)

**Record date**: 2026-11-24
**Owning Issue**: [#638](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/638) — "[REQ-03 P1] Recover direct-main authorization and provenance for commit 54ea3977"
**Carrier**: this PR. This section is the register's provenance entry for a single direct-push commit; it does not open a separate register file.
**Measurement baseline**: `main` @ `882ed439f639853d311348d67038bf9e4ef02d8e` (live API `main` head, 2026-11-24T10:24:16Z)

### 15.1 Why this section rather than a new register

Sections 1–14 record **scale and pattern** (45 → 53 → 62 direct pushes). This section records **one commit's recoverability boundary**, because #638 does not ask for "one more commit on the list" — it asks whether this commit's authorization can be proven at all.

The register already defines the determination method (§1: call `/commits/{sha}/pulls`; an empty array means direct push), but its census window closed at 2026-11-20T14:20Z. `54ea3977` was committed **two days later**, so it never entered any round of this register's count — that gap is itself a coverage defect, recorded in §15.8 as P-2.

### 15.2 Recoverable commit facts (all API-measured, none inferred)

| Field | Value | Source |
|---|---|---|
| commit SHA | `54ea39771af33c2e68d94515ca159cd74b18287f` | `GET /repos/{repo}/commits/{sha}` |
| parent SHA | `968a81db5ba83b767713e29655ad0af439f87e29` (single parent, not a merge) | same, `parents[].sha`; `git rev-list --parents -n1` |
| subject | `feat(bmcp): expose validate/digest as MCP tools instead of an empty capability set` | same, `commit.message` |
| author identity | `ChatGPT Automation <automation@users.noreply.github.com>` | same, `commit.author` |
| committer identity | `ChatGPT Automation <automation@users.noreply.github.com>` | same, `commit.committer` |
| signature | `verified: false`, `reason: unsigned` | same, `commit.verification` |
| author/committer time | `2026-11-22T13:48:07+08:00` = `2026-11-22T05:48:07Z` | same; `git log --format=%aI/%cI` |
| changed files | 3 files, `+344 / −12` | same, `files[]`, `stats` |
| ancestor of `main` | yes; `compare/main...54ea3977` → `status: behind`, `ahead_by 0`, `behind_by 343` | `GET /repos/{repo}/compare/main...54ea3977` |

Per file (from `files[]`):

| Path | Status | ±lines | blob SHA |
|---|---|---|---|
| `crates/bmcp-server/src/lib.rs` | modified | +172 / −8 | `8ce8593bcc1f24a509bb08bd81e7e799aa2425cf` |
| `crates/bmcp-server/tests/rt_scenarios.rs` | modified | +2 / −4 | `9c58364dea9012470346242f140f1e831af58366` |
| `crates/bmcp-server/tests/tool_dispatch.rs` | added | +170 / −0 | `111b89555243081b89755518b7df3013c7899c19` |

Position on the first-parent chain: entry 203 of `git rev-list --first-parent origin/main`, i.e. a linear direct push, not a merge.

### 15.3 Fields that cannot be recovered (each with its reason)

No inference. The following fields exist in no queryable carrier and are recorded as **unavailable**:

| Field | Status | Reason and search scope |
|---|---|---|
| producing ChatGPT session ID | **UNAVAILABLE** | No in-repo record; `grep -r` for this SHA over the whole tree returns **0 matches**. The #638 body supplies none |
| execution prompt version / hash | **UNAVAILABLE** | Same. No prompt file, no manifest, no Work Item link. Nothing under `14-ai-development/work-items/` references this SHA |
| Owner / delegation authorizing the direct write to `main` | **UNAVAILABLE** | The commit message carries no `Authorized by:` segment (contrast `DIRECT-PUSH-RATIFICATION-ffc44c31`, whose message does). No instrument, issue comment or ADR in the repository points at this write |
| authorization scope and validity window | **UNAVAILABLE** | No authorizing carrier exists, so neither scope nor start/end can be bounded |
| independent review (different session, different prompt) | **ABSENT** | See §15.4. Not "not found" — no review carrier exists |
| merge event / merger | **NOT APPLICABLE** | No PR, therefore no merge event. `pulls` is `[]`; there is no `merged_by` / `merged_at` |
| exact-Head checks at commit time | **NOT EXECUTED** | See §15.5 |

### 15.4 Review: absent, and not merely "not found yet"

| Retrieval path | Returned | Meaning |
|---|---|---|
| `GET /repos/{repo}/commits/{sha}/pulls` | `[]` | no PR carrier → no PR review, no review comment, no review state |
| `GET /repos/{repo}/commits/{sha}/comments` | `0` records | no commit-level comments |
| `GET /repos/{repo}/commits/{sha}/check-runs` | 3, all `failure` | see §15.5 |
| `GET /repos/{repo}/commits/{sha}/status` | `state: pending`, `total_count: 0` | no commit statuses |
| `GET /search/issues?q=repo:{repo} 54ea3977` | 4 hits: `#638` (issue), `#348` (issue), `#611` (PR, closed), `#264` (issue) | three only mention the SHA in prose; `#611` is a search match with no carrier relationship (its head is `d95cb4eb`, base `1effc423`, neither of which is this SHA) |
| `GET /search/issues?q=repo:{repo} "expose validate/digest as MCP tools"` | 3 hits: `#638`, `#732` (PR, closed), `#264` | `#732` is a gap-10 errata with head `eeff8507` and base `021f5a3f`, unrelated to this SHA |

Recording the exclusions matters too: `#611` (opened 2026-11-22T05:40:34Z, merged 06:17:12Z) and `#732` both appear in the search, but neither head nor base SHA contains `54ea3977`, and both report `reviews: 0`. **Neither** may be cited as a review carrier for this commit.

The only upstream carrier that mentions the defect in this commit is Issue **#617** (`bmcp-server: return MCP CallToolResult for tools/call`), which states:

> Main commit `54ea39771af33c2e68d94515ca159cd74b18287f` added `tools/list` and `tools/call` to `bmcp-server`. The current `tools/call` response shape is not compliant with the declared MCP protocol version `2024-11-05`.

**This is not a review of this commit.** It is a defect finding, filed after the commit, by `oahcom` (the same identity that wrote this record). Under `PR-GOVERNANCE-001` §5, "a review performed through the same connected GitHub identity as the author is not independent", and it does not satisfy #638's independence baseline of "different session plus different prompt". This record does not count it as a review.

### 15.5 Check state at commit time: `NOT_EXECUTED`

All three check runs are push-triggered and were created 1–2 minutes after the commit:

| check | conclusion | started (Z) | completed (Z) | job id | `runner_name` | `runner_id` | `steps` |
|---|---|---|---|---|---|---|---|
| `rust-workspace-test` | `failure` | 05:49:49 | 05:49:56 | `137112019738` | `""` | `0` | `0` |
| `audit` | `failure` | 05:49:49 | 05:49:51 | `137112019710` | `""` | `0` | `0` |
| `GOV-DOC-002 metadata checks` | `failure` | 05:49:49 | 05:49:51 | `137112019454` | `""` | `0` | `0` |

With `runner_name == ""`, `runner_id == 0` and `steps == []` all holding, the register's established rule (§3 here and `MERGE-AFTER-RULING-003` §2: `steps==0 && runner_name==""` → `NOT_EXECUTED`) applies: these three results are **not executed**, neither PASS nor substantive FAIL.

The accurate statement is therefore that the commit passed through **no executed check**; `failure` is only the surface value of "never started". This also shows Actions was not the producer of the commit — it merely attempted to check it afterwards, and did not start.

One timing fact, useful for bounding "was there a gate at the time": the tree at `54ea3977` does **not** contain `.github/workflows/gates.yml` (`git cat-file -e 54ea3977:.github/workflows/gates.yml` → ABSENT). That file first appears in `9f30610f` (`ci: wire the existing gates into CI and ratchet the two that are already red (#669)`, 2026-11-22T18:36:31+08:00), **4 h 48 min later**. Thirteen workflows existed at the time (`git ls-tree 54ea3977:.github/workflows/`).

### 15.6 Was the carrier exception authorized?

`PR-GOVERNANCE-001` §3 gives exactly one exception: when the merge target is a non-`main` branch. `54ea3977`'s target (its direct write target) is `main`, so it does **not** fall under that exception.

Does the standard contain any other clause that could authorize a direct write to `main`:

| Clause | Content | Applies here |
|---|---|---|
| §3 paragraph 2 | a non-`main` target needs no PR | No (target is `main`) |
| §7 | platform enforcement is separate from process policy | No (describes platform capability, authorizes no write) |
| Enforcement addendum §7 | emergency bypass must record authorizing actor, reason, exact SHA, skipped checks, risk acceptance, time window, and a mandatory post-event independent review | No (none recorded; and the clause only entered `main` with #750 on 2026-11-23, after this commit) |

**Conclusion**: the direct-push carrier for `54ea3977` has **no** discoverable authorization basis. This is not "the authorization exceeded its scope"; it is "no authorization record exists".

### 15.7 Disposition

```
PROVENANCE_UNRECOVERABLE — 54ea3977
  facts recoverable : sha, parent 968a81db, 3 paths (+344/-12), unsigned, no PR
  authorization     : not recorded anywhere; unrecoverable after the fact
  review            : absent (no PR carrier; #617 is a defect finding, not a review)
  carrier exception : not authorized under PR-GOVERNANCE-001 §3
  residual risk     : accepted, bounded to bmcp validate/digest MCP tool exposure
```

**Boundaries of this disposition**:

1. All four facts above are reproducible and unaffected by the missing authorization. **The content exists** and **the entry path was compliant** are two different claims; this record denies only the second.
2. No PR is invented, no reviewer is invented, and `#611` / `#732` / `#617` are not retroactively promoted to reviews. Any of those would make the record wider than the facts.
3. Residual risk is bounded by the change's content: the commit replaces an empty capability set with two read-only tools, `validate` and `digest`, removes no authorization check and adds no write path. The effect of an unauthorized version of this change is "a capability that returned nothing now returns something", not "a boundary moved". This bound follows the #638 ruling in comment `7125721934`, which this record re-checked and agrees with.
4. The `tools/call` response-shape defect is tracked separately by **#617**. **This section does not claim it is fixed**, and the provenance conclusion must not be read as a disposition of that defect.

### 15.8 Corrective actions (proposed here; none executed)

| # | Action | Status |
|---|---|---|
| P-1 | Turn §1's determination method from a one-off census into a continuous check: on `push` to `main`, call `/commits/{sha}/pulls` for each new commit, and emit a failing check or a record that must be archived when the array is empty | Not executed. Carried by #134. Note the policy text already exists on the `push` branch of `document-management.yml`, but that workflow does not check PR membership |
| P-2 | Replace this register's window ("most recent 100 commits @ `0b6cebdf`") with a re-runnable rolling window, so `54ea3977` and post-2026-11-20 direct pushes stop falling outside it | Not executed. Measured here: `grep -c 54ea3977` on this register was **0** before this revision |
| P-3 | Maintain a per-commit list for the synthetic identity `ChatGPT Automation`. Measured: **15** commits on `main`, of which **9** have `pulls == []`, **2** are merge commits (each carrying 1 PR) and **4** carry a PR | Partly done: §15.9 publishes that list, so `54ea3977` has a corresponding row |

### 15.9 All 15 commits by that synthetic identity (each API-measured)

Method: call `/commits/{sha}/pulls` per SHA; `parents` > 1 marks a merge commit. Captured 2026-11-24.

| # | commit | time (Z) | parents | associated PR | verdict |
|---|---|---|---|---|---|
| 1 | `7228c886` | 2026-11-21T09:56:40 | 1 | #463 | via PR |
| 2 | `46c4b677` | 2026-11-21T10:49:48 | 1 | #483 | via PR |
| 3 | `cdd76a56` | 2026-11-21T10:58:47 | 1 | #483 | via PR |
| 4 | `2651e226` | 2026-11-21T13:38:15 | 1 | `[]` | **direct** |
| 5 | `c553aeeb` | 2026-11-21T18:12:09 | 1 | #536 | via PR |
| 6 | `cf460ba4` | 2026-11-21T19:02:28 | 2 | #433 | merge commit |
| 7 | `6e9214dc` | 2026-11-22T02:34:56 | 1 | `[]` | **direct** |
| 8 | `87d503ba` | 2026-11-22T02:36:28 | 1 | `[]` | **direct** |
| 9 | `4eacb5b4` | 2026-11-22T04:24:56 | 1 | `[]` | **direct** |
| 10 | `d89fd5fa` | 2026-11-22T04:28:15 | 1 | `[]` | **direct** |
| 11 | `6897e53c` | 2026-11-22T05:12:19 | 1 | `[]` | **direct** |
| 12 | **`54ea3977`** | 2026-11-22T05:48:07 | 1 | `[]` | **direct — the subject of this record** |
| 13 | `71499e76` | 2026-11-22T06:05:18 | 1 | `[]` | **direct** |
| 14 | `001248d4` | 2026-11-22T07:17:31 | 1 | `[]` | **direct** |
| 15 | `8a4be6d2` | 2026-11-22T10:14:55 | 2 | #659 | merge commit |

**Totals for this identity: of 15 commits, 9 have no PR carrier, 2 are merge commits and 4 went via PR.** All 15 are `verified: false` (`reason: unsigned`).

The purpose of this table is to make the proportion visible, not to fold nine cases into one disposition: `54ea3977` is one of those 9, and the other 8 have **no** provenance record of their own. This register does not claim those 8 are covered by this section.

### 15.10 What this section deliberately does not decide

- **It does not determine** which natural person, session or tool stands behind `ChatGPT Automation`. That email resolves to a real GitHub user account `automation` (id `289953`, registered 2010-05-28); the account is public, but as a `users.noreply.github.com`-style commit identity it points at no collaborator of this repository. Measured `collaborators` for this repository is **1** (`oahcom`, `admin: true`), so even an existing account cannot write here. That fact and "who executed the commit" are separate questions; this section infers no executor from it.
- **It does not judge** whether the commit's technical content is correct or desirable. #617 tracks its defect; this section neither duplicates nor prejudges that.
- **It does not revert** the commit, rewrite history, or re-attribute it.
- **It does not read** `PROVENANCE_UNRECOVERABLE` as "authorization was granted and then lost". It has exactly one meaning: **this write does not produce an authorization record by design** — synthetic identity, unsigned, no PR — and those three together make after-the-fact recovery structurally infeasible, not merely under-attempted.
- **It does not extend** this section's conclusion to the other 8 direct pushes in §15.9.

### 15.11 Reproduction commands for this section

```bash
# commit metadata
git log -1 --format='%H%n%P%n%an <%ae>%n%cn <%ce>%n%aI%n%cI%n%G?' 54ea3977
git show --name-status --format='' 54ea3977

# containment
git merge-base --is-ancestor 54ea3977 origin/main && echo ancestor
git rev-list --first-parent origin/main | grep -n 54ea3977

# carrier
curl -s -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/54ea3977/pulls
# -> []

# were the checks executed
curl -s -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/commits/54ea3977/check-runs
# -> 3 check_runs, all conclusion=failure; job detail: runner_name="", runner_id=0, steps=[]

# is the SHA cited by any file in the tree
grep -rn 54ea3977 --include='*.md' --include='*.json' --include='*.yaml' .
# -> 0 matches

# did gates.yml exist at that commit
git cat-file -e 54ea3977:.github/workflows/gates.yml   # -> ABSENT
```

---

