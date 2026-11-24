---
document_metadata:
  domain: ai-development
  role: normative-standard
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
      last_verified_date: "2026-11-24"
      last_verification_note: "This file has no front-matter approval record. Its body header states v1.2 PENDING ADOPTION, with v1.1 adopted via PR #256 merge 48a556491506d25e78be47957276bf3821797a0a and v1.0 via PR #230 merge 53aae842c390eac6d54f937af6cd2744dbe8d09d. Those adoption events are recorded here as prose evidence only; this metadata does not assert them as a machine-verifiable approval binding."
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
    normative_status: Normative
  bilingual_counterpart:
    source: "14-ai-development/AI-EXEC-002.md"
    en: null
    zh-CN: null
---
# AI-EXEC-002 — AI Prompt Execution Rules
# AI Development Prompt Execution Details

- **Document ID:** AI-EXEC-002
- **Version:** 1.2
- **Status:** v1.2 PENDING ADOPTION (to be registered upon merge of this change set to `main`, per the effectiveness clause of AI-EXEC-UNIFICATION-RULING-001 §5). Previous versions: v1.1 ADOPTED via PR #256 (merge commit `48a556491506d25e78be47957276bf3821797a0a`, 2026-11-18); v1.0 ADOPTED via PR #230 (merge commit `53aae842c390eac6d54f937af6cd2744dbe8d09d`, 2026-11-18). v1.2 changes: F-006 anchor revision (structure = seven sections per AI-STD-001 §5.1; the 15/12 items reclassified as content obligations mapped per AI-PROMPT-STD-001 §4).
- **Owner:** Integration Owner
- **Tracking:** Issue #218 · Work Item [AID-2026-002](../../../14-ai-development/work-items/AID-2026-002/manifest.yaml) · Revision Work Item [AID-2026-003](../../../14-ai-development/work-items/AID-2026-003/manifest.yaml)
- **Upstream standards:** [AI-STD-001](../../../14-ai-development/ai-development-standard.md) §5/§13, [AI-PROMPT-STD-001](../../../14-ai-development/prompt-authoring-standard.md), [CHATGPT-GLOBAL-001](../../../14-ai-development/prompts/global/chatgpt-session-contract-v1.md), [AI-PROC-001](../../../14-ai-development/iteration-lifecycle.md) Stages 2/6, GLB-DOC-001 (policy GOV-DOC-001)
- **Source document:** `14-ai-development/AI-EXEC-002.md`
- **Source commit:** `1f97c3fae65828266a0c3cb1d1e8d4e6cb330856` (coordinator-supplied)
- **Source blob SHA:** `ebb7f1ee9a084864c454711d271499cfbf8d386f` (coordinator-supplied)
- **Translation status:** English counterpart; source-aligned translation. Source document remains authoritative for this batch.

> **Positioning**: This document does not establish a new standard. It provides execution details that make the project's existing prompt system actually work. No scripts are mandated; constraints rely on self-declaration in prompt text and traceability in Issues/PRs/Closeouts.

**English summary.** Every execution prompt MUST use the seven structural sections defined by AI-STD-001 §5.1 (post-#269 canonical structure). The 12 items in AI-PROMPT-STD-001 §4 and AI-STD-001's former items 13–15 remain mandatory **content obligations** and MUST be mapped into those seven sections per the mapping rule in AI-PROMPT-STD-001 §4; they are not separate headings. Six/seven-item focus subsets never waive content obligations. VERIFIED is the canonical lifecycle status; TESTED is evidence wording only. SHA-256 is mandatory for exact prompt bytes; NOT_VERIFIED records an evidence limitation and never waives the gate. T1/T2/T3 provenance, grandfather distinctions, traceability, review, finding fields, bilingual exceptions and Closeout remain governed by this document.

---

## 1. Scope and Prompt Library (following AI-STD-001 §5)

- **Execution channels**: Ordinary ChatGPT conversations + the project's verified GitHub connected app. The ten non-negotiable constraints in CHATGPT-GLOBAL-001 remain in force verbatim (no API Keys / Codex / third-party models / local relays; GitHub artifacts are the persistent source of truth, not chat history).
- **Prompt library** (canonical location is repository-root `prompts/`, per AI-STD-001 §5):
  - Required reading for every session: `prompts/global-project-developer.md` + `prompts/global-bilingual-documentation.md` + the relevant Owner prompt (`prompts/A/`–`prompts/I/`).
  - Review sessions must also read: `prompts/global-architecture-reviewer.md`.
  - The current `14-ai-development/prompts/` library (CHATGPT-GLOBAL-001, `owners/A/owner-session-v1.md`, etc.) **continues to be used**; every session must state in its evidence which library and version it actually used. Unifying the two libraries is a future hardening item.
- **Three session types**: Development sessions (Owners A–I), review sessions (independent ChatGPT conversations, NR-001), and governance sessions (daily governance window; see [AI-EXEC-001](AI-EXEC-001.md) §7).

## 2. Required Pre-Start Fields (Eliminate "Prompt hash: NOT RECORDED")

Before work starts, record the following in the Work Item's Issue/PR (= AI-STD-001 §13 start record + AI-PROC-001 §8 intake checklist):

1. **Work Item ID**: `AID-YYYY-NNN` (registration rules in [INDEX.md](../../../14-ai-development/work-items/INDEX.md)), with `work-items/AID-YYYY-NNN/manifest.yaml` already created;
2. **Prompt identifier**: Prompt ID + version (e.g. `AID-2026-002-PROMPT v1`) + provenance anchor (apply the **three T1/T2/T3 tiers** below);
3. **Baseline**: target branch, base SHA, dependency SHA(s) (source Pin — a branch name is not a stable baseline; AI-PROMPT-STD-001 Step 2);
4. **Scope / non-goals, task class** (ARCH/IMPL/TEST/SEC/MIG/PERF/DOC/OPS), **risk level** (R0–R3), and **acceptance criteria**.

**Three prompt-provenance tiers (added in v1.1; remedy for gap ②)** — the former triple assumed that a prompt must be a repository file and did not cover chat-instruction sessions. Select the tier according to the actual form:

| Tier | Applicability | Minimum traceable provenance anchor |
|---|---|---|
| **T1 Repository file** | The prompt is stored as a repository file (e.g. `work-items/AID-*/prompt-vN.md`) | **Prompt ID + version + prompt-file commit SHA triple**; record SHA-256 if available (calculate over the exact committed bytes, UTF-8 without normalization, and record path/byte count/digest/Blob SHA/commit SHA per AI-PROMPT-STD-001 §5); if it cannot be calculated/verified, record **NOT_VERIFIED** |
| **T2 In-session instruction** | Chat-instruction: instructions are provided in the conversation and have no repository file | **Prompt ID + version + full instruction snapshot** — at start, store the full text of the instructions actually executed in an Issue/PR comment (or archive it as `prompt-vN.md`); provenance anchor = **permanent comment URL + creation timestamp** (archiving upgrades it to T1) |
| **T3 Hybrid** | Repository file + in-session supplemental instructions | Use the **actual instruction set executed**: record both the file triple and the supplemental snapshot (using T2 method) |

- **No fabrication; an empty NOT RECORDED is prohibited** (all tiers);
- An executed prompt version is immutable; if an in-session clarification/supplement materially changes the instructions, create a new version first (new T1 file version / new T2 snapshot), then continue (AI-PROMPT-STD-001 §5);
- **Grandfather clause**: sessions started before v1.1 takes effect are retrospectively governed by the v1.0 approach; **no backdating, fabrication, or retroactive penalties**. Record `RULES-NOT-LOADED` only when direct evidence proves the rules were not loaded; when only a LOADED declaration/record is missing, record `RULES-LOAD-NOT-RECORDED`, which indicates an evidence gap only and must not be used to infer that the rules were actually not loaded or to find a historical violation.

> **Adjudicated (2026-11-18)**: Prompt provenance and hashing uniformly follow RULING-03 of `AI-EXEC-UNIFICATION-RULING-001`. SHA-256 of the exact prompt bytes is mandatory; `NOT_VERIFIED` is only an honest statement of an evidence limitation and is not an exemption. Work must not enter `PROMPT_READY` unless prompt-integrity requirements are met.

## 3. Mandatory Prompt Structure (seven structural sections + twelve/fifteen content-obligation mapping; no separate structure is created)

> **Structural authority**: the structural sections are the seven sections of AI-STD-001 §5.1; content obligations follow the mapping rule of AI-PROMPT-STD-001 §4 — the twelve items MUST be mapped into the seven sections per §4. The 12 items + additions below are a **content-obligation inventory** (not separate headings); after mapping, the seven sections are the only structural layer.
>
> **All-risk-level baseline obligation (F-02)**: substantive execution prompts of **every risk level (R0–R3) and every task class** MUST retain the complete **15 content obligations** (the 12 items + former items 13–15), all mapped into the seven sections. R0/R1 and R2/R3 do not change the base mandatory applicability of the 15 obligations; the six/seven-item focus subsets denote review emphasis only. Scheduled-prompt add-ons remain additional requirements.

Every execution prompt must contain its 12 content obligations (mapped into the seven sections per AI-PROMPT-STD-001 §4; together with former items 13–15 they form the complete 15 content obligations, applicable to every risk level):

1. Identity (Work Item ID, Issue, prompt ID/version/hash, Owner, session role)
2. Objective (goal and observable result)
3. Baseline (repository, branch, base SHA, source path/blob SHA, dependencies)
4. Authority (decisions owned, permitted/prohibited actions, approver)
5. Scope (in-scope files/modules and explicit non-goals)
6. State of knowledge (separate DECIDED / CANDIDATE / OPEN / TO_VALIDATE)
7. Required steps (inspect → plan → change → verify → report)
8. Acceptance criteria (numbered, objective, independently checkable)
9. Verification (commands, fixtures, environment, expected/actual results)
10. Git workflow (branch, commit, PR target, review handoff, no-merge rule)
11. Stop/escalation (stop conditions and escalation target)
12. Evidence and final report schema (evidence and final-report format)

**Tiered review emphasis (not a content-obligation exemption)**:
- **All execution prompts, across all risk levels and task classes**, must retain the complete 12 content obligations above (mapped into the seven sections); no remaining content obligations may be deleted, merged, or omitted because a prompt is R0/R1, DOC, or a code session.
- **R0/R1 documentation-session focus subset**: items 1, 2, 5, 8, 11, and 12 require particular specificity; these are review emphases, not a six-item replacement template.
- **Code-session focus subset**: for task classes `IMPL/TEST/SEC/MIG/PERF`, items 1, 2, 3, 5, 8, 9, and 12 require particular specificity; the other five items must still remain in the prompt. Regardless of task class, R2/R3 require the complete 12 content obligations plus applicable additional risk/bilingual requirements.
- **R2/R3 (any task class)**: the full 15 content obligations are required (mapped into the seven sections), along with applicable additional risk/bilingual requirements; this is consistent with the content obligations for R0/R1 and does not create a difference in which R2/R3 alone are exempt from.
- Scheduled prompts must additionally follow the add-ons in AI-PROMPT-STD-001 §4 (Owner key, automation ID, frequency, time zone, idempotency, per-run limit, no-task behavior, permission preflight).

> **Adjudicated (2026-11-18; 2026-11-19 F-006 anchor revision)**: The sole complete mandatory **structure** is the seven sections of AI-STD-001 §5.1, as specified in RULING-01 (revised) of `AI-EXEC-UNIFICATION-RULING-001`. The 12 items of AI-PROMPT-STD-001 §4 and the former items 13–15 are mandatory **content obligations** and MUST be mapped into the seven sections per §4; the six/seven-item focus subsets do not constitute deletion or exemption. Precedence: structure follows AI-STD-001 §5.1; content-obligation mapping follows AI-PROMPT-STD-001 §4.

Prompt approval continues to follow its Step 6 (A drafts cross-Owner tasks; the accountable Owner approves domain semantics; A must not draft and approve their own task). **Prompt approval ≠ implementation approval ≠ merge approval.**

## 4. Execution Traceability (AI-PROC-001 Stage 4 + PR-GOVERNANCE-001 §2)

- Record important decisions, commits, changed paths, test results, blockers, and handoffs **as they happen** in the Issue/PR; do not accumulate them until closeout.
- The sole canonical status vocabulary is the eight states in **CHATGPT-GLOBAL-001 session workflow, item 7**: `PROPOSED / IMPLEMENTED / VERIFIED / REVIEWED / ACCEPTED / MERGED / BLOCKED / NOT RUN`. `VERIFIED` is the only verification-stage status; `TESTED` describes test evidence only and is not a lifecycle status. Historical `TESTED` is mapped as evidence wording and is not automatically equivalent to `VERIFIED`. See RULING-02 of `AI-EXEC-UNIFICATION-RULING-001`.
- Explicitly state the three-valued test status: `RUN/PASS`, `RUN/FAIL`, `NOT RUN` (+ reason). **NOT RUN must never be reported as PASS** (verbatim AI-STD-001 DoD).
- Test evidence must point to the **exact commit**; tests against another commit are not evidence until the differences are proven irrelevant and recorded (AI-PROC-001 Stage 5).

## 5. Review Session Rules (Operationalization of NR-001)

1. **Independent review = a new ChatGPT conversation**, reviewing frozen inputs read from GitHub (approved prompt version, task record and acceptance criteria, base/implementation SHA, diff, test evidence, contract documents); the reviewer must read `prompts/global-architecture-reviewer.md`.
2. Reviewers must not merely repeat the author's report; they must actively seek counterexamples, missing negative cases, race windows, scope leakage, stale-state behavior, and compatibility breaks (AI-PROC-001 Stage 6).
3. **Finding classification**: project severity levels are `BLOCKER / P0 / P1 / P2 / P3`; **dispositions** are `PASS / CONDITIONAL PASS / FAIL / NOT REVIEWABLE`. Every finding must include ID, evidence, owner, severity, status, and closure condition; CONDITIONAL PASS must list limitations and must not be treated as full acceptance (AI-STD-001 §9). **Minimum registration threshold (v1.1, aligned with [AI-EXEC-001](AI-EXEC-001.md) §4)**: ID + severity + **feedback destination** (closure condition + feedback landing point: Issue #N / RW-YYYYMMDD / Closeout item k); if any of these three is missing, the finding is not registered. This enables the feedback flow to consume it.
4. **Red lines (verbatim PR-GOVERNANCE-001 §5, as amended 2026-11-24)**: `COMMENT` is a technical comment, not `APPROVE`; independence is a property of the **reviewing session**, not of the GitHub account that carries it — a review performed by a session that did not author the change is independent even when it reports through the same connected identity; AI role-play inside the authoring session is neither independent review nor Owner approval; exceptions must be explicitly recorded and never silently waived.
5. **Disclosure obligation (NR-001)**: the review record must state: "An independent ChatGPT conversation provides context/conversation isolation only; it is not model/statistical independence and must not be called multi-model consensus." R3 still requires independent security/domain-expert review + reproducible test evidence.

## 6. Closeout — Evidence Exit for a Session

At session end (whether completed or blocked), publish a Closeout comment in the Issue/PR (= the eight items in AI-STD-001 §13 ∪ the nine items in PR-GOVERNANCE-001 §2 ∪ the bilingual-gate result in AI-STD-001 §7.1):

1. Session/prompt identifier: Prompt ID, version, SHA-256 or NOT_VERIFIED, prompt-file commit SHA, role, accountable Owner;
2. Work Item ID + owning Issue + related PR links (prefer reusing existing tracking artifacts, PR-GOVERNANCE-001 §3);
3. Repository, branch, base SHA, final Head SHA, changed paths;
4. Actual work and decisions, each marked `PROPOSED / ACCEPTED / REJECTED / UNRESOLVED / OPEN / BLOCKED` + decision authority;
5. Verification commands, environment, exact test SHA, results and links; **list every required check not run and the reason**;
6. Independent-review and integration status; disclose same-author/delegated-role simulation and never present it as independent approval;
7. Dependencies, blockers, risks, next Owner, and objective closure conditions; even blocked/no-change work must publish a `BLOCKED` / `NO_CHANGE` Closeout;
8. Merge status: record target branch, merge commit SHA, and post-merge read-back verification only if actually merged — **never infer that a PR was merged from its closure**;
9. Bilingual-gate result (GOV-DOC-001: both paths, source version, parity-dimension PASS/FAIL, reviewer, or the required STALE-exception registration elements).

Then add one **session-level delivery record** line to [INDEX.md](../../../14-ai-development/work-items/INDEX.md) (mark missing evidence `NOT RECORDED`, never fabricate it; blocked/no-change work remains visible and must state resolver and exit condition).

## 7. Prohibited Actions (AI-PROMPT-STD-001 §7 + CHATGPT-GLOBAL-001)

- Self-drafting and self-approving; acting as one's own independent reviewer; presenting a role-play panel as independent approval;
- Using a floating branch name/"latest" instead of a SHA; combining multiple Work Items in one prompt;
- Claiming that unrun tests, missing approvals, or unverified deployment behavior are complete;
- Changing prompt instructions during execution without review; fabricating NOT RECORDED evidence;
- Using API Keys, Codex, third-party/local models, Desktop Commander, or local relays;
- Allowing scheduled tasks to merge/publish/perform destructive operations by default, or repeatedly reopening completed/rejected work.

## 8. Revisions

Prompt additions/changes go through the **daily governance window** ([AI-EXEC-001](AI-EXEC-001.md) §7, i.e. daily operationalization of the feedback loop in AI-STD-001 §11): issue a new version (Prompt ID + version number + new commit SHA); old versions remain immutable and retrievable.

---

## Appendix A: Copy/Paste Templates for Development Session Start / Closeout

```markdown
### Start Record (write to Issue/PR)
- LOADED: AI-EXEC-001 v__ + AI-EXEC-002 v__ (loaded-rules declaration in §1.4; missing declaration only = RULES-LOAD-NOT-RECORDED; only direct evidence of non-loading = RULES-NOT-LOADED)
- Work Item: AID-YYYY-____ (manifest.yaml: created/not created)
- Owning Issue: #____   Related PR: #____
- Role: Owner __ (Accountable Owner: __)
- Prompt: <Prompt ID> v<version> [T1|T2|T3]
  - T1: @ <prompt-file commit SHA> (SHA-256: ____ or NOT_VERIFIED)
  - T2: instruction snapshot → <permanent Issue/PR comment URL> @ <timestamp>
  - T3: both
- Base: <branch> @ <base SHA>   Deps: <SHA list>
- Class/Risk: ARCH|IMPL|TEST|SEC|MIG|PERF|DOC|OPS / R0|R1|R2|R3
- Scope / Non-goals: ____
- Acceptance: 1) ____ 2) ____
- Bilingual: □ synchronized in the same change set  □ STALE exception (reason/temporarily authoritative version/Owner/deadline/tracking Issue, GOV-DOC-001 §5)

### Closeout (publish to Issue/PR at session end, then add one INDEX.md line)
1. Session/Prompt: <Prompt ID> v__ [T1|T2|T3] @ __ (hash: ____/NOT_VERIFIED; T2: snapshot link __) Role: __
2. Work Item AID-____ / Issue #____ / PR #____
3. Branch __ / base __ / Head __ / changed: ____
4. Work & decisions: ____(PROPOSED/ACCEPTED/REJECTED/UNRESOLVED/OPEN/BLOCKED + authority)
5. Verification: <command> @ <test SHA> → RUN/PASS | RUN/FAIL | NOT RUN(__); unrun checks: ____
6. Review: <independent-session review / same-author disclosure> Verdict: PASS | CONDITIONAL PASS | FAIL | NOT REVIEWABLE
   (NR-001 disclosure: conversation isolation ≠ model independence)
7. Risks/blockers/next Owner/exit condition: ____
8. Merge: not merged | merged to __ @ __ (read-back: __)
9. Bilingual (GOV-DOC-001): paths __ / parity PASS|FAIL|STALE exception (deadline __ / tracking __) / reviewer __
```

## Appendix B: Review Session Output Template (Finding System)

```markdown
### [REVIEW] PR #____ / AID-____ (independent ChatGPT session; inputs frozen)
Verdict: PASS | CONDITIONAL PASS | FAIL | NOT REVIEWABLE
Findings:
- F-1 [P0] <symptom + evidence (file:line / commit)> — owner __ — closure condition __ — feedback __ (Issue #N / RW-YYYYMMDD / Closeout item k)
- F-2 [P2] ... — feedback __
Checks: scope consistency / honest test status (NOT RUN ≠ PASS) / traceable provenance (Prompt+version+commit SHA) / bilingual parity (GOV-DOC-001)
Disclosure: This review is an independent ChatGPT conversation providing context isolation, not model/statistical independence (NR-001).
```
