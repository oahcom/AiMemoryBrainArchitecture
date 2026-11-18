# AID-2026-002 Prompt v1 — Execution rules PR + related bug fixes

- Prompt ID: AID-2026-002-PROMPT
- Version: v1
- Status: EXECUTED (immutable — do not edit; clarification addenda get new versions)
- Work Item: AID-2026-002
- Owning Issue: #218
- Role: Implementing AI session (Integration Owner lane, class DOC / risk R1)
- Created: 2026-11-18

## 1. Identity
Implementing session for AID-2026-002 under CHATGPT-GLOBAL-001 constraints (ordinary ChatGPT conversation + validated connected GitHub app / git credentials; no API Key, Codex, third-party or local models, Desktop Commander, or local relay).

## 2. Objective
Land the AI-development execution rules as one reviewable PR on `oahcom/AiMemoryBrainArchitecture`, and fix the related documentation bugs found during the rules review. Observable outcome: branch `ai/AID-2026-002/IO-exec-rules` with (a) AI-EXEC-001 / AI-EXEC-002 / AI-EXEC-ROLLOUT-001 added under `14-ai-development/`, (b) literal-escape bugs fixed, (c) Work Item AID-2026-002 registered (manifest + prompt + INDEX rows), (d) tracking Issue #218 and a PR whose description satisfies PR-GOVERNANCE-001 §3.

## 3. Baseline
- Repo: oahcom/AiMemoryBrainArchitecture
- Base branch: main
- Base SHA: 282a82e58d8d9d1aa876621481df3184fbe5d284
- Dependencies: AI-STD-001, AI-PROC-001, PR-GOVERNANCE-001 (ADOPTED), AI-PROMPT-STD-001, CHATGPT-GLOBAL-001, NR-001 (governance-decision), GOV-DOC-001 policy

## 4. Authority
- Owner-directed content: execution rules derived from and subordinate to the upstream standards; no upstream clause is amended.
- Allowed: add new docs under 14-ai-development/ and work-items/AID-2026-002/, update INDEX.md and docs/translation-status.md registration rows, fix literal escape-sequence formatting bugs.
- Prohibited: changing normative semantics of upstream standards; fabricating evidence; merging to main; claiming independent review.

## 5. Scope / Non-goals
- In scope: the three rule/plan documents, escape-sequence bug fixes in ai-development-standard.md, docs/README.md, docs/translation-status.md, reviews/.../model/README.md, Work Item registration.
- Non-goals: resolving the three inter-standard conflicts (deferred to Issue #218 adoption); English full translation (registered as STALE exception, due 2026-12-02); platform enforcement (Issue #134); prompt-library unification; any code change.

## 6. State of knowledge
- DECIDED: PR-GOVERNANCE-001 ADOPTED (Issue #130 comment #6962523529, PR #144); NR-001 controls; G0–G7 gate names; AID + manifest + INDEX registration rules.
- CANDIDATE: AI-EXEC-001/002 rules themselves (PROPOSED until adoption recorded in Issue #218).
- OPEN: upstream conflicts (15-vs-12 structure; TESTED-vs-VERIFIED; SHA-256-vs-NOT_VERIFIED) — to be settled at adoption.
- TO_VALIDATE: none for this work item.

## 7. Required steps
inspect (repo conventions, INDEX/manifest formats, bug sites) → plan (branch, work item, file set) → change (bug-fix commit + rules commit) → verify (formatting checks, diff review, exact-Head evidence) → report (PR body + closeout + INDEX rows).

## 8. Acceptance criteria
1. Branch follows `ai/<work-item-id>/<owner>-<short-topic>`; two reviewable commits (bug fixes; rules + registration).
2. AI-EXEC-001/002/ROLLOUT-001 present with house headers (Document ID, Version, Status: PROPOSED, Owner, Tracking Issue #218, upstream links, translation-status note).
3. All literal backslash-n sequences in the four target prose files replaced with real newlines; shell-code escapes in ubuntu-self-hosted-runner-bootstrap.md untouched.
4. Work Item registered: manifest.yaml + prompt-v1.md (SHA-256 recorded) + INDEX.md work-item row + session row; docs/translation-status.md rows added for the three new docs with STALE exception registration.
5. PR opened against main stating deliverable/owner/scope/dependencies/why-new-PR per PR-GOVERNANCE-001 §3; verification records distinguish RUN/PASS from NOT RUN.

## 9. Verification
- `python` literal-escape scanner over the four files (expect zero prose occurrences after fix; before: 19 across 4 files).
- `git diff --check` for whitespace errors on both commits.
- Visual check of AI-STD-001 §5 items 14/15 and §7.1 rendering as separate lines.
- NO code tests (documentation-only change set): runtime/test suites NOT RUN.

## 10. Git workflow
Branch `ai/AID-2026-002/IO-exec-rules` off main@282a82e5. Conventional commits. PR to main. No self-merge; merge decision is owner's (five-disposition rule applies). Post-merge: read back and record merge SHA.

## 11. Stop / escalation
Stop on: any requirement to amend upstream normative clauses; credential/permission failure; unexpected conflicts with open PRs touching the same files. Escalate to: project owner via Issue #218.

## 12. Evidence and final report schema
Closeout per AI-EXEC-002 §6 (nine items incl. bilingual STALE registration); evidence recorded in PR body and INDEX session row; findings (if any) as BLOCKER/P0–P3 in Issue #218 or PR comments.
