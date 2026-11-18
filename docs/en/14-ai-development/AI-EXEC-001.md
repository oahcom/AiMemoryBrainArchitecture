# AI-EXEC-001 — AI Development Process Execution Rules

- **Document ID:** AI-EXEC-001
- **Version:** 1.1
- **Status:** ADOPTED — v1.0 adopted via PR #230 (merge commit `53aae842c390eac6d54f937af6cd2744dbe8d09d`); v1.1 adopted via PR #256 (merge commit `48a556491506d25e78be47957276bf3821797a0a`), both merged 2026-11-18; this header records both adoption events.
- **Owner:** Integration Owner
- **Tracking:** Issue #218 · Work Item [AID-2026-002](../../../14-ai-development/work-items/AID-2026-002/manifest.yaml) · Revision Work Item [AID-2026-003](../../../14-ai-development/work-items/AID-2026-003/manifest.yaml)
- **Upstream standards:** [AI-STD-001](../../../14-ai-development/ai-development-standard.md), [AI-PROC-001](../../../14-ai-development/iteration-lifecycle.md), [PR-GOVERNANCE-001](../../../14-ai-development/PR-GOVERNANCE-001.md) (ADOPTED), [AI-PROMPT-STD-001](../../../14-ai-development/prompt-authoring-standard.md), GOV-DOC-001
- **Source file:** `14-ai-development/AI-EXEC-001.md`
- **Source commit:** `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856` (coordinator-supplied)
- **Source blob SHA:** `372a290359f9e9de2bd81d7901beb2f084e6e3a4` (coordinator-supplied)
- **Translation status:** English counterpart; source-aligned pair. Chinese source remains authoritative for this batch.

> **Purpose and positioning:** This document does not establish a new governance system. It is an execution rulebook that makes the project's existing process (AI-STD-001 / AI-PROC-001 / PR-GOVERNANCE-001) **actually operate**. There is no script-based enforcement — PR-GOVERNANCE-001 §7 explicitly states that "templates/labels/comments/AI self-review must not be misrepresented as hard gates." These rules are consistent with that principle and add only operating discipline.
> **This document does not amend** any provision in a higher-level document. Where a conflict exists, the higher-level document prevails; this document only supplements "how to run it, what evidence to leave, and how long closure may take."

**English summary.** Execution rules that operationalize the existing governance stack — no parallel institution, no script enforcement. Adds: (1) a Stage 0–8 run table binding each lifecycle stage to its Work Item state and evidence; (2) tracking carriers per AI-STD-001 §13 (Issue / PR / AID+manifest / INDEX / Closeout); (3) PR discipline = PR-GOVERNANCE-001 five dispositions + exact-Head gate + flow quotas (open PR ≤ 10, weekly integration window — running discipline, violations logged as findings, never hard-blocked); (4) review & exception rules (NR-001 independent session for R2/R3, explicit exception recording, ≤ 2/iteration); (5) a **daily governance window** (≤ 20 min, AI-STD-001 §11 loop materialized) as the only feedback→rules re-entry point; (6) a five-point Definition of Done for closing the ecosystem loop. The three inter-standard conflicts are resolved by the binding Owner ruling **AI-EXEC-UNIFICATION-RULING-001** (2026-11-18): 15-item prompt structure, VERIFIED lifecycle vocabulary, and mandatory SHA-256 with NOT_VERIFIED treated only as an evidence limitation. **v1.1 adds** (observation-report gaps ①③⑤⑥): a session kickoff loading obligation (ADOPTED ≠ wired-in), the finding minimum registration line (ID + severity + feedback destination), an independent-review acquisition bridge (source order + timeout → recorded exception), and an interop clause for later governance documents (declare SUPERSEDE/COMPLEMENT/PARALLEL).

---

## 1. General Principles: Three Operating Principles That Make the Rules Effective

1. **Rules must take effect before they are enforced:** Most higher-level documents are currently PROPOSED. Following the **owner-directed adoption** model demonstrated by PR-GOVERNANCE-001 (Issue #130 comment #6962523529 + PR #144 merge record), convert them to **ADOPTED** in batches. Provisions that have not taken effect must not be used as gate criteria (AI-STD-001 §12, "Initial Governance Status," expressly permits this).
2. **Evidence accompanies the output:** NOT RUN ≠ PASS (the original AI-STD-001 DoD wording); evidence must point to the exact Head/commit (PR-GOVERNANCE-001 §4 exact-Head gate).
3. **Defects must flow back:** Findings go into an Issue/Closeout; **rule-related problems** (prompt/process/contract defects) are handled in the **daily governance window** (the daily operationalization of the AI-STD-001 §11 feedback loop).
4. **ADOPTED ≠ loaded — loading is mandatory at kickoff** (added in v1.1): Changing a standard to ADOPTED resolves its "effective" status; it does not ensure that it has "entered the execution path." At kickoff, every substantive session (development/review/governance) **must explicitly load** §§2–5 of this rulebook and §§2–3 of [AI-EXEC-002](AI-EXEC-002.md), and declare `LOADED: AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1` (or the actual versions) on the first line of the kickoff record. Where direct evidence proves that the rules were not loaded, mark `RULES-NOT-LOADED` and record a finding. Where only the LOADED declaration/record is missing, mark `RULES-LOAD-NOT-RECORDED` and register only an evidence gap; do not infer actual non-loading or retrospectively determine a violation from that absence alone.

## 2. Iteration Lifecycle = AI-PROC-001 Stages 0–8 (Run Table)

No new stages are introduced. This section specifies only what must be left behind to make each stage "run":

| Stage (AI-PROC-001) | Work Item state (AI-STD-001 §4.1) | Gate | Requirements of this rulebook |
|---|---|---|---|
| 0 Intake & registration | PROPOSED | G0 | **Load AI-EXEC-001/002 and declare `LOADED` (§1.4)**; reuse or create an Issue; create `AID-YYYY-NNN` + `manifest.yaml`; record Sponsor/Owner |
| 1 Impact & dependency | ANALYZED | G1 | Write the impact graph, dependency/contract status (DECIDED/CANDIDATE/OPEN/TO_VALIDATE), and acceptance criteria into the Issue |
| 2 Prompt drafting | PROMPT_READY | G1 | Store the prompt and freeze its version (AI-EXEC-002 §§2–3); A drafts, Owner approves |
| 3 Readiness gate | READY | G1 | All DoR conditions satisfied (AI-STD-001 §7); if an upstream contract is OPEN, choose one of three paths: resolve the contract first / do only an isolated slice / BLOCKED |
| 4 AI implementation | IN_PROGRESS → IMPLEMENTED | G2 | Branch `ai/<work-item-id>/<owner>-<short-topic>` (AI-STD-001 §6); make the smallest coherent change; update the Issue/PR as work proceeds |
| 5 Automated verification | VERIFIED | G3 | Check evidence against the exact Head; explicitly state the reason for `NOT RUN`; add concurrency/fault/security tests for R2/R3 |
| 6 Independent AI review | REVIEWED | G4 | Independent NR-001 ChatGPT session + finding system (AI-EXEC-002 §5) |
| 7 Cross-owner integration | INTEGRATION_READY | G5 | Each Owner approves only their own contract boundary; A reconciles conflicts and updates the Contract Registry; distinguish five levels (local approval / bilateral contract / multi-module / implementation evidence / system conformance) |
| 8 Acceptance & merge | ACCEPTED → MERGED → CLOSED | G6 (G7 release readiness counted separately) | Five-state PR disposition (§5); 8-item Closeout + INDEX row; read back the merge SHA after merge |

- State progression **must not skip states** (original AI-STD-001 §4.1): Implemented ≠ Verified ≠ Reviewed ≠ Accepted ≠ Merged.
- `BLOCKED`: a dependency/decision/permission is unavailable; record the blocking owner and exit conditions. `REJECTED`: the approach is invalid; preserve the prompt and review records rather than erasing evidence of failure (§4.2).

## 3. Work Classes and Risk Levels (Directly Reuse AI-STD-001 §4; Do Not Redefine)

- Work classes: `ARCH / IMPL / TEST / SEC / MIG / PERF / DOC / OPS`; every Work Item must declare one.
- Risk levels: `R0` editorial change / `R1` bounded-impact implementation or documentation / `R2` cross-module contracts, persistence, protocols, concurrency, compatibility / `R3` security boundaries, authorization, Forget/deletion, data integrity, recovery, migration, release-critical work.
- R2/R3 require explicit impact analysis + named reviewers. R3 requires independent security/domain-expert review + reproducible test evidence before acceptance.
- Bilingual gate (AI-STD-001 §7.1 / GOV-DOC-001): for tasks that affect architectural meaning, update Chinese and English documents in the same change set. Reviewers record PASS/FAIL for meaning/identifiers/status/examples/links. Missing or materially inconsistent content = BLOCKED/NOT DONE, or a time-bounded STALE exception registered under GOV-DOC-001 §5 (reason/temporary authoritative version/Owner/due date/tracking Issue).

## 4. Tracking Mechanism (AI-STD-001 §13 + Current PR-GOVERNANCE-001 Carriers)

| Carrier | Content carried | Rules |
|------|---------|------|
| **GitHub Issue** | Requirements, defects (findings), decisions, blockers | Prefer reusing an existing Issue (decision Issues such as #41/#130; work Issues according to the AID's owning Issue); every substantive session must belong to an Issue/PR; defects = findings recorded as BLOCKER/P0–P3 in an Issue comment or Closeout |
| **GitHub PR** | Integration unit | PR-GOVERNANCE-001 §3 admission and merge organization: search existing carriers first; open a new PR only for an independently reviewable unit; prohibit duplicates or splitting merely to inflate records |
| **Work Item** | `AID-YYYY-NNN` + `work-items/AID-YYYY-NNN/manifest.yaml` | Create before substantive work begins; registration rules are in [INDEX.md](../../../14-ai-development/work-items/INDEX.md) (unique number, create directory and manifest first, link prompt version and hash, update at major gates and closeout, do not delete rejected/blocked records) |
| **INDEX.md** | One session-level delivery record per line | AI-STD-001 §13 assigns maintenance to the Integration Owner; mark missing evidence `NOT RECORDED` and never fabricate it |
| **Closeout** | Issue/PR comment | AI-STD-001 §13 eight items ∪ PR-GOVERNANCE-001 §2 nine items ∪ §7.1 bilingual gate result (AI-EXEC-002 §6 template) |

**Minimum finding registration line (added in v1.1, response to gap ⑤):** Any finding (whether from review, self-check, retrospective, or observation) must contain all three elements to count as "registered":

1. **ID:** `F-n` (sequence within a PR) or `DEF-YYYYMMDD-nn` (across PRs);
2. **Severity:** `BLOCKER / P0 / P1 / P2 / P3` (AI-STD-001 §9);
3. **Feedback destination:** closure condition + feedback landing point (`Issue #N` / `RW-YYYYMMDD` / `Closeout item k`).

Missing any element = not registered (free-form text comments do not count as findings). All three elements provide the minimum interface through which the feedback flow can be measured — the smallest interface for loop ⑥→⑦ of the seven-loop model.

**No script-based restrictions and no labels masquerading as gates** (PR-GOVERNANCE-001 §7): labels/templates are conveniences for search and writing. The actual constraints are the record obligations above, review disposition, and Owner authority.

## 5. PR Discipline (= Execution Interpretation of Current PR-GOVERNANCE-001 Provisions)

1. **Five-state disposition** (original §6): `MERGE / HOLD / REMEDIATE / SUPERSEDED / REJECT` — every merge decision must select one of the five and state the missing items or rationale.
2. **Exact-Head gate** (§4): all checks and approvals must target the current Head SHA; when Head changes, refresh the evidence. Checks against an old Head, green checks from another PR, and verbal local assertions do not count; missing/pending/skipped/failed = NOT PASS.
3. **Flow-liquidity operating discipline** (operational layer, not platform enforcement): open PR ≤ 10, **clear before opening**; consolidate merges and backlog reduction into one integration window each week (consistent with PR-GOVERNANCE "merge upon verification": merge promptly when MERGE conditions are met; do not hold work merely to accumulate review rounds). Violations do not block platform actions, but must be recorded as findings in the retrospective.
4. **PRs targeting a non-main base branch** retain their target branch and dependency chain; do not unilaterally retarget them to main. Create a separate integration PR for mainline release (§3).
5. After merging, **read back the target branch** and record the actual merge commit SHA (§6).

## 6. Review and Exceptions (NR-001 + PR-GOVERNANCE-001 §5)

| Scenario | Requirement |
|------|------|
| R0/R1 low-risk documentation | Distinguish author and reviewer; one person may cover multiple review dimensions (AI-STD-001 §3.2) |
| R2 | Independent ChatGPT session review (NR-001) + explicit approval from affected Owners for their contract boundaries |
| R3 | Independent review + **security/domain-expert review** + reproducible test evidence + explicit approval by the Acceptance Authority |
| Involving security/identity/authorization/Forget/lifecycle/persistence/recovery/cross-Owner contracts | Reviewers must be independent of both the author and implementation session (PR-GOVERNANCE §5) |

**Exceptions and escalation (owner-directed exception):**

- Exceptions are only for time-sensitive handling that triggers escalation, maintains HOLD, or advances REMEDIATE/REJECT. They must not waive required evidence, treat NOT RUN as PASS, or replace mandatory review conditions at any risk level.
- The Issue/Closeout must record request time, reason for unavailability, escalation target, current HOLD status, next review time, and disposition decision; count exceptions according to the rules.
- Exceptions are limited to ≤ 2 per iteration. Exceeding the limit for 2 consecutive iterations triggers a rule revision through the daily governance window. This quota is an additional operating discipline introduced by this rulebook.

**Independent-review acquisition and non-waivable R3 gate (revised in v1.1):**

1. **Source order:** First request an independent ChatGPT review session. R3 must additionally obtain independent security/domain-expert review and reproducible test evidence. A ChatGPT session review cannot replace R3 expert review.
2. **24-hour escalation:** If the required review resources have not been obtained within 24 hours after the request, escalate to the accountable Owner and maintain HOLD. This deadline triggers escalation only; it creates no waiver, acceptance, or merge authority.
3. **Disposition within 3 working days:** If the required evidence is still unavailable, the Owner must record and choose to continue HOLD, REMEDIATE, or REJECT. Timeout, resource unavailability, or an exception record must not be used to downgrade merge/acceptance requirements.
4. **R3 hard gate:** Independent security/domain-expert review and reproducible test evidence are both prerequisites to R3 acceptance and MERGE and **cannot be waived**. If either is missing, the work must remain BLOCKED/HOLD until the evidence is obtained; retrospective review cannot retroactively deem an earlier acceptance or merge compliant.
5. **Closure on evidence recovery:** After the evidence is obtained, record the expert's identity/domain, review conclusion, exact test commit and result in the original PR/Issue, then have an independent Owner session perform exact-Head re-verification.

## 7. Daily Governance Window (Daily Operationalization of AI-STD-001 §11 — Critical to Closing the Loop)

**Once daily, at a fixed time, ≤ 20 minutes**, decoupled from iteration boundaries. This is the only entry point for "feedback flow reconnecting to the rule flow":

1. **Inputs:** rule-related findings from the day (prompt/process/contract defects) + improvement items from the most recent iteration retrospective (AI-PROC-001 §4 metric checklist output).
2. **Actions** (following the seven steps in AI-STD-001 §11): stop/isolate unsafe parts → open finding/change request → designate authoritative Owner → record decision (rationale/alternatives/consequences) → increment prompt version → update dependent tasks and compatibility tests → resume execution after approval.
3. **Outputs:** the revision PR is **merged and effective on the same day** (Owner has final say); document header `Status` is flipped (PROPOSED→ADOPTED/ACTIVE); affected prompts receive a new version.
4. **Feedback registration:** the corresponding finding/Issue comment states "feedback to RW-YYYYMMDD / PR #N"; items that cannot be scheduled that day roll over to the next day, and the daily backlog is cleared.

## 8. Iteration Retrospective (Continue to Follow AI-PROC-001 §4; Close Through the Daily Window)

At the end of each iteration, spend 30 minutes recording the metrics in its checklist: lead time / active time, prompt clarification and revision count, findings by severity, escaped defects after merge, new tests and NOT RUN items, rework caused by stale dependencies, cross-Owner contract conflicts, and documentation drift. Produce no more than 3 improvement items and bring them to the next day's daily governance window.

## 9. Closed-Loop Acceptance (Criteria for Determining That G0–G7 Actually Operate)

The "ecosystem loop" is achieved when all 5 conditions are met, after which the project enters the strengthening phase:

1. **Rules effective:** core upstream documents (AI-STD-001, AI-PROC-001, AI-PROMPT-STD-001, etc.) have been changed to ADOPTED through owner-directed adoption, with inspectable records (following the PR-GOVERNANCE-001 / Issue #130 model).
2. **Verification runs end to end:** two consecutive iterations complete Stages 0–8, with Work Item states progressing without skips to CLOSED (or BLOCKED with exit conditions recorded).
3. **Traceability test:** sample 3 merged PRs and verify the complete chain is inspectable — `AID / manifest → Prompt ID+version+commit SHA → Issue → PR Head → test evidence → review findings → Closeout → INDEX row`.
4. **Evidence integrity:** zero conflation of NOT RUN with PASS; zero `NOT_RECORDED` for Prompt provenance (ID+version+commit SHA) in new records; all same-author reviews disclosed.
5. **Flow health:** open PR ≤ 10 with no PR stalled for more than 7 days; PRs meeting MERGE conditions are not left pending; no more than 2 exceptions per iteration.

## 10. Attachment of Later Governance Documents (Added in v1.1, Response to Gap ③)

When adding any governance/evidence/process document (e.g. PR enforcement or merge evidence standards):

1. **The PR body must declare the relationship:** choose one of `SUPERSEDE / COMPLEMENT / PARALLEL` and explain the rationale, affected provisions, and boundaries. Failure to declare = a finding (P2, routed to the daily governance window).
2. **Adjudication gate before merge:** the attachment relationship for every governance/evidence/process-document PR must be adjudicated in writing before MERGE by the project Owner or an explicitly authorized governance decision-maker. Record the adjudicator, relationship, rationale, boundaries, and review deadline. The daily governance window organizes adjudication and records evidence, but the window itself does not automatically constitute approval.
3. **Handling without adjudication:** if adjudication is missing, unresolved, or authority is unclear, the PR must remain HOLD; it must not MERGE. Timeout permits only escalation, continued HOLD, REMEDIATE, or REJECT; it must not be treated as implied approval.
4. **Special threshold for PARALLEL:** PARALLEL must explicitly record the approver (project Owner or named delegate), why attachment is not possible, parallel boundaries/non-duplicated scope, dual-track risk controls, and review deadline. If any element is missing, adjudication is incomplete and the PR remains HOLD.
5. **SUPERSEDE** must rewrite the superseded provisions in the same PR; **COMPLEMENT** must explain the boundaries that remain governed by AI-EXEC.

---

## Appendix A: Current-State Gaps → Corresponding Actions in This Rulebook (All Within Existing Document Mechanisms)

| Current-state evidence (repository evidence) | Corresponding action | Location |
|---|---|---|
| 6 standards remained PROPOSED and never took effect | Convert them to ADOPTED in batches through owner-directed adoption (replicate the PR-GOVERNANCE-001 model) | §1 |
| Prompt hash `NOT RECORDED` was widespread | Prompt ID + version + commit SHA triplet; SHA-256 may be NOT_VERIFIED, but fabrication is prohibited | AI-EXEC-002 §2 |
| Only 2 Work Items registered for 142 PRs | Create AID + manifest before substantive work; search existing carriers first during PR admission | §4, PR-GOVERNANCE §3 |
| 0 independent reviews; exceptions became routine | NR-001 independent sessions + finding system + explicit exception counting | §6 |
| PR backlog (76 open/72 draft) | Limit of 10, clear before opening + weekly integration window + five-state disposition and timely MERGE | §5 |
| Test NOT RUN conflated with PASS | Explicit three-valued reporting + exact-Head evidence + execution of original DoD wording | §2 Stage 5, AI-EXEC-002 §4 |
| Two prompt libraries coexisted | Record the actual library and version used; consolidate as a strengthening item | AI-EXEC-002 §1 |

## Appendix B: Relationship Between This Rulebook and Higher-Level Documents

- This document **does not modify** any provision definition in AI-STD-001 / AI-PROC-001 / PR-GOVERNANCE-001 / AI-PROMPT-STD-001.
- Where conflicts exist, higher-level documents prevail; this document only supplements "how to run it, what evidence to leave, and how long closure may take."
- The Owner issued a binding ruling on the three conflicts among the higher-level standards on 2026-11-18. See [AI-EXEC-UNIFICATION-RULING-001](../../../14-ai-development/AI-EXEC-UNIFICATION-RULING-001.md): prompts are unified to 15 items; the verification stage uses VERIFIED (TESTED is used only to describe test evidence); SHA-256 must be recorded, and NOT_VERIFIED indicates only an evidence limitation, not a waiver. Through the SUPERSEDE relationship, this ruling replaces the previous deferred and temporary execution interpretations; all other provisions of the upstream standards remain unchanged.
- Revisions to this rulebook itself follow the daily governance window in §7.
