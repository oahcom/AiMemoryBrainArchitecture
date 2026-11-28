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
- Base commit SHA: `3da2e32cf0475a5d7645862a4a288988f69f09cc`

The branch contains these three implementation and documentation commits, rebased onto `origin/main` and identified here by their commit titles rather than SHA values:

1. `feat(gov): add a session-identity ratchet with a shrink-only baseline (AID-PENDING)`
2. `feat(gov): require an explicit git-verified bootstrap for the session-identity baseline (AID-PENDING)`
3. `docs(gov): align the session-identity design with the git-verified bootstrap`

The work-item registration is recorded in a fourth commit, identified by title:

4. `work-item(AID-2026-007): register the session-identity ratchet`

The fifth commit records the refreshed baseline evidence and work-item metadata after the target tree changed. Its title is `docs(gov): refresh session-identity baseline evidence and work-item record`.

Commit SHA values are intentionally not embedded in this work-item record. Rebase rewrites commit SHAs; embedding them before the branch is pushed would preserve references to Git objects that no longer exist after a subsequent rebase. The GitHub pull request's commit list is the authoritative source for the current commit SHAs.

## Changed implementation and governance files

- `scripts/ci/check_session_identity.py` — session identity checker, baseline validation, shrink-only update behavior, and explicit Git-verified bootstrap.
- `scripts/ci/test_check_session_identity.py` — automated tests for checker behavior, baseline handling, and bootstrap constraints.
- `scripts/ci/baselines/session-identity.txt` — the frozen session identity baseline.
- `.github/workflows/session-identity-ratchet.yml` — CI workflow for the session identity ratchet check.
- `14-ai-development/design/session-identity-ratchet.md` — design and operational rules for the ratchet, baseline ownership, bootstrap, and acceptance boundary.
- `14-ai-development/PR-GOVERNANCE-001.md` — governance record for the added check context and its non-required status.

## Local gate results

The coordinating operator reports the following local measurements.

1. Command: `python scripts/ci/check_session_identity.py`

   Output:
   `SESSION IDENTITY: PASS (0 new violations; existing violations baselined)`

   Exit code: `0`

2. Command: `python -m unittest scripts.ci.test_check_session_identity`

   Output:
   `Ran 27 tests`
   `OK`

   Exit code: `0`

3. Command: `python scripts/check_document_management.py --require-changed origin/main`

   Output:
   `PASS (incremental): no GOV-DOC-002 violations; 815 classified, 370 unclassified`

   Exit code: `0`

4. Command: `python scripts/ci/check_manifest_parse.py`

   Output:
   `Manifest parse: PASS (0 failed).`

   Exit code: `0`

5. Command: `python scripts/check_traceability.py --index-only`

   Output:
   `PASS TRACEABILITY: 0 requirements / 0 errors.`

   Exit code: `0`

6. Command: `python scripts/ci/check_work_item_uniqueness.py --base origin/main --head HEAD`

   Output:
   `WORK-ITEM UNIQUENESS: PASS (violations=0 deletions=0)`

   Exit code: `0`

   The reported tree hashes are intentionally omitted: `base_tree` and `candidate_tree` are determined by the final base and candidate commits, so their values are not prefilled before the final commit is established.

These are local results reported by the coordinating operator. They are not claims about remote CI.

## Baseline and shrink-only rule

The baseline freezes the existing violation identities observed in the target branch tree. It records the existing inventory rather than declaring the historical records valid or authentic.

After initial bootstrap, the baseline may only shrink. A finding that disappears is removed. A finding newly introduced relative to the baseline must be fixed; it must not be added to the baseline to make the check pass. Stale baseline entries are rejected during normal checking.

The baseline was regenerated by the checker after the target tree changed. After the previous bootstrap, `origin/main` advanced to `3da2e32cf0475a5d7645862a4a288988f69f09cc` and incorporated additional work items whose manifests themselves carried existing violations. The previous baseline no longer matched the updated target tree; the checker refused to continue with the inconsistent baseline and required regeneration from that tree. Earlier baseline sizes are historical states and are not the current baseline.

The coordinating operator regenerated the baseline with the following command and observed output:

`python scripts/ci/check_session_identity.py --bootstrap-baseline --base-ref origin/main` → `SESSION IDENTITY BASELINE: bootstrapped 84 entries from 3da2e32cf0475a5d7645862a4a288988f69f09cc`

This was a tool-generated refresh from the target Git tree, not a manual edit.

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

