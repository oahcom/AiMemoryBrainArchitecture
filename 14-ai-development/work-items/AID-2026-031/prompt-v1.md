---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_ASSIGNED
      decision_date: "2026-11-28"
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-031/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-28"
      last_verification_note: "This is the initial registration prompt snapshot; execution and verification remain coordinator responsibilities."
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
    canonical_scope_keywords:
      - "AID-2026-031"
      - "session identity"
      - "governance registration"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-031 — Initial work package

## Objective

Correct the single new session-identity ratchet violation in `AID-2026-297` and register this work item with complete governance documentation.

## Repository and baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`
- Base commit: `f0843a8f38a420883921cfda96b515204967f885`
- Working date: `2026-11-28`
- Tracking issue: #1534, "AID-2026-328: Remove human label from NOT_RECORDED session sentinel"

## A. Correct AID-2026-297

The current manifest contains:

`implementing_ai_session: MIGRATION-POLICY`

with:

`session_reference_status: RECORDED`

The session-identity checker does not accept this human label as a supported session identifier.

Change the pair to:

`implementing_ai_session: NOT_RECORDED`

`session_reference_status: NOT_RECORDED`

Do not invent a UUID or `conv_` identifier.

Preserve the existing prompt snapshot path, SHA-256, byte count, provenance, issue references, and session evidence reference.

Do not rewrite `AID-2026-297/session-evidence.md`. It is a historical record of the declaration made in that evidence document, not the current authoritative manifest field pair.

Do not alter any other AID-2026-297 claim, evidence, test result, implementation detail, or lifecycle state.

Do not touch AID-2026-341.

## B. Register AID-2026-031

Create:

1. `14-ai-development/work-items/AID-2026-031/manifest.yaml`
2. `14-ai-development/work-items/AID-2026-031/evidence.md`
3. `14-ai-development/work-items/AID-2026-031/session-evidence.md`
4. `14-ai-development/work-items/AID-2026-031/prompt-v1.md`
5. One final row in `14-ai-development/work-items/INDEX.md`

Use the following registration facts:

- Work item ID: `AID-2026-031`
- Status: `DISPATCHED`
- ID status: `PROVISIONAL`
- Date: `2026-11-28`
- Base commit: `f0843a8f38a420883921cfda96b515204967f885`
- Owner and sponsor: `USER-PRINCIPAL-DELEGATED`
- Tracking issue: `#1534`
- Prompt snapshot: `14-ai-development/work-items/AID-2026-031/prompt-v1.md`
- Session status: `RECORDED`
- Session identifier: `{{CONV_ID}}`
- Prompt SHA-256: `{{PROMPT_SHA256}}`
- Prompt byte length: `{{PROMPT_BYTES}}`
- Prompt provenance: `NOT_VERIFIED`

Use the exact `{{CONV_ID}}`, `{{PROMPT_SHA256}}`, and `{{PROMPT_BYTES}}` placeholders. The coordinator substitutes their actual values mechanically.

The manifest's `prompt_sha256` and `session_evidence[0].executed_prompt_sha256` must both use `{{PROMPT_SHA256}}`.

The manifest's `session_evidence[0].executed_prompt_bytes` must use `{{PROMPT_BYTES}}`.

Do not invent `prompt_file_blob_sha`; omit it or leave it null.

Set `prompt_commit_trace_initial_registration: true`.

Use the required `document_metadata` block on every new Markdown file. Keep approval `Draft` and evidence verification `Unverified`.

## C. INDEX registration

Append one row to the end of the table in `14-ai-development/work-items/INDEX.md`.

Use nine columns:

`Work Item ID | Title | Owner | Class/Risk | Status | Prompt | Implementation | Review | Acceptance`

The row must:

- Link `[AID-2026-031](AID-2026-031/manifest.yaml)`.
- Identify the prompt as `AID-2026-031-PROMPT` v1.
- Include the prompt digest placeholder `{{PROMPT_SHA256}}`.
- State `Review: NOT_ASSIGNED`.
- State `Acceptance: PENDING`.

## D. Verification

The coordinator must execute the repository's required governance and CI gates after writing the files.

The supplied ratchet evidence is:

- Last green run: `46109215468`, head `3b4bc0039`.
- First red run: `46109393978`, head `6c6f8cfe8`.
- Current red run: `46109588406`, head `f0843a8f3`.

The original checker output was:

`SESSION IDENTITY: 92 violations, 91 baselined, 1 new`

The expected post-correction output is:

`SESSION IDENTITY: 91 violations, 91 baselined, 0 new`

Do not claim that the expected result has been achieved until the coordinator actually runs the checker.

The supplied gate list includes:

- Session-identity ratchet validation.
- Changed-document management validation using `scripts/check_document_management.py --require-changed origin/main`.
- Traceability index validation using `scripts/check_traceability.py --index-only`.
- Repository-required manifest/schema validation.
- Repository-required prompt-commit-trace validation.

The coordinator records the exact commands and results. Do not fabricate gate results.

## E. PR requirements

The coordinator creates the PR after committing and pushing.

The PR body must contain, in order:

1. What changed, including every changed file.
2. Attribution and scope: the AID-2026-297 edit changes one field pair solely for "correcting an unverifiable identity declaration" (修正一条不可核实的身份声明), not a content rewrite. No AID-2026-297 claim, evidence, test result, or lifecycle state is altered.
3. The verbatim ratchet violation and historical run IDs, plus the expected post-correction result.
4. The actual gate results, inserted by the coordinator.
5. Explicit non-claims: no CI success, merge, independent review, or Owner acceptance asserted at authoring time.

## F. Execution boundary

This authoring session supplies the content and placeholders.

The coordinator performs mechanical file writing, gate execution, commit, push, and PR creation.

Do not report those coordinator operations as completed until evidence is supplied.
