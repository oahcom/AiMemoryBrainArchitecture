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

**Status**: `OPEN` / `NOT_REMEDIATED` / **scale 53** / **nature escalated from "process slip" to "deliberate choice under a known rule, rationalised in writing"**; round three adds: **continues across parallel identities, and now includes a commit identity that cannot be attributed to any account**
