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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-007/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-28"
      last_verification_note: "The coordinating operator reports the recorded local gate measurements. CI results must be checked against the PR check-runs."
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
    canonical_scope: "Execution evidence for work item AID-2026-007 (session identity ratchet)."
    canonical_scope_id: "ai-development/aid-2026-007-execution-evidence"
    canonical_scope_keywords:
      - "AID-2026-007"
      - "execution evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-007 execution evidence

## Repository and commits

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Target branch: `main`
- Working branch: `feat/2026-11-27-session-identity-ratchet`
- Base commit SHA: `3d9b32bef6775974117ea0ab925179acf43c6ecb`

The branch contains these three implementation and documentation commits, rebased onto `origin/main`:

1. `2c0cd76ff` feat(gov): add a session-identity ratchet with a shrink-only baseline (AID-PENDING)
2. `9585ba80b` feat(gov): require an explicit git-verified bootstrap for the session-identity baseline (AID-PENDING)
3. `0749562c9` docs(gov): align the session-identity design with the git-verified bootstrap (AID-PENDING)

The work-item registration is recorded in a fourth commit:

4. The work-item registration commit that introduces these files; its SHA is recorded in the pull request, because a commit cannot contain its own hash.

## Changed implementation and governance files

- `scripts/ci/check_session_identity.py` — session identity checker, baseline validation, shrink-only update behavior, and explicit Git-verified bootstrap.
- `scripts/ci/test_check_session_identity.py` — automated tests for checker behavior, baseline handling, and bootstrap constraints.
- `scripts/ci/baselines/session-identity.txt` — the 74-entry frozen session identity baseline.
- `.github/workflows/session-identity-ratchet.yml` — CI workflow for the session identity ratchet check.
- `14-ai-development/design/session-identity-ratchet.md` — design and operational rules for the ratchet, baseline ownership, bootstrap, and acceptance boundary.
- `14-ai-development/PR-GOVERNANCE-001.md` — governance record for the added check context and its non-required status.

## Local gate results

The coordinating operator reports the following local measurements.

1. Command: `python scripts/ci/check_session_identity.py`

   Output:
   `SESSION IDENTITY: 74 violations, 74 baselined, 0 new`

   Exit code: `0`

2. Command: `python -m unittest scripts.ci.test_check_session_identity`

   Output:
   `Ran 27 tests`
   `OK`

   Exit code: `0`

3. Command: `python scripts/check_document_management.py --require-changed origin/main`

   Output: no output line was supplied; exit code: `0`.

4. Command: `python scripts/ci/check_manifest_parse.py`

   Output:
   `Manifest parse: 137 manifests found, 137 parsed, 0 failed.`

   Exit code: `0`

These are local results reported by the coordinating operator. They are not claims about remote CI.

## Baseline and shrink-only rule

The baseline contains 74 violation identities observed in the target branch tree. It freezes existing inventory rather than declaring the historical records valid or authentic.

After initial bootstrap, the baseline may only shrink. A finding that disappears is removed. A finding newly introduced relative to the baseline must be fixed; it must not be added to the baseline to make the check pass. Stale baseline entries are rejected during normal checking.

## Git-verified bootstrap conditions

Initial baseline creation requires an explicit `--bootstrap-baseline --base-ref REF` invocation. Bootstrap must satisfy all of the following conditions:

- The repository must not be shallow.
- The target `REF` must resolve to a Git commit and be verifiable against the current branch history.
- The target `REF` tree must not already contain the baseline file.
- Baseline contents must be generated from the work-items tree in the target `REF` tree, not from the current working tree.
- Current-tree violations must be a subset of the violation identities found in the target `REF` tree. Any current violation absent from the target tree causes bootstrap to be refused.

Ordinary checking and ordinary `--write-baseline` do not create a missing baseline. A missing baseline causes both operations to exit with code `2`.

## GitHub check context

`Session identity ratchet` is an added GitHub check context. It is not configured as required. The required check contexts remain 16.

## Issue scope

This PR does not reference any Issue.

## Prompt measurement placeholders

The `executed_prompt_sha256` and `executed_prompt_bytes` values in the manifest and session evidence are placeholders before coordination-side finalization. After `prompt-v1.md` is written from the registration prompt's exact original bytes, the coordinating operator must mechanically replace these placeholders using the actual file bytes: `executed_prompt_sha256` becomes the 64-character hexadecimal SHA-256 digest, and `executed_prompt_bytes` becomes the integer byte count. The prompt snapshot itself is written by the coordinating operator from the original prompt message.

## CI verification boundary

After the registration commit, CI results must be verified from the PR check-runs. No remote CI result is claimed by the local measurements recorded above.
