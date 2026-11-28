---
document_metadata:
  domain: ai-development
  role: work-record
  steward: "user-authorized operator (delegated by account owner)"
  lifecycle:
    approval:
      decision_status: Draft
      approver: NOT_ASSIGNED
      decision_date: "2026-11-27"
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-327/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the supplied coordinator report and the revised authoring output. No claim is made that the revised output has been executed."
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
      - "AID-2026-327"
      - "session evidence"
      - "checker repair"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session role / use case

This session authors the checker, tests, and evidence corrections for AID-2026-327 in `oahcom/AiMemoryBrainArchitecture`.

The coordinator performs mechanical application and repository execution. This authoring session does not claim to have modified the coordinator's worktree, run the coordinator's commands, created a branch, opened a PR, or merged a commit.

Attribution:

`user-authorized operator (delegated by account owner)`

# Actual AI input

The session received the coordinator's ROUND 1 execution report for AID-2026-327.

The supplied worktree facts were:

- Worktree: `C:\tmp\apply327`
- HEAD: `cc5d22b9126e00e3f93ffe71282554309908bc89`
- Environment: Windows and CPython 3.12
- `PYTHONUTF8=1`

The report identified:

1. A `unittest` module import failure caused by a top-level sibling-module import.
2. A mismatch between the attempted `--commit` / `--base` invocation and the previous checker's actual CLI.
3. A missing `PRIMARY` / `MATRIX` output contract.
4. False missing-prompt-file findings because repository-root-relative paths were joined to the manifest directory.
5. A 142-manifest audit population, distinct from the supplied 138-row historical cohort.
6. Lifecycle cases where stale implementation SHAs must not be counted for `NOT_STARTED` or `DISPATCHED` work items.
7. Manifest schema rejection of `implementation.status: DISPATCHED`.
8. Document metadata rejection of `verification_status: Pending`.
9. The need for a PR body draft containing an explicit `TESTS:` line.

The coordinator also supplied the exact historical cohort counts and identified the three `(MATCH, A)` rows.

# AI-visible output

The AI-authored output in this revision consists of:

1. A complete replacement for `scripts/ci/check_prompt_commit_trace.py`.
2. A complete replacement for `scripts/ci/test_check_prompt_commit_trace.py`.
3. A corrected `14-ai-development/work-items/AID-2026-327/manifest.yaml`.
4. A corrected `14-ai-development/work-items/AID-2026-327/evidence.md`.
5. A corrected `14-ai-development/work-items/AID-2026-327/session-evidence.md`.
6. A corrected `14-ai-development/work-items/AID-2026-327/prompt-v1.md`.
7. One corrected registration row for `14-ai-development/work-items/INDEX.md`.
8. A complete PR body draft.

# Corrections made in the authored output

- The test module imports the checker through `scripts.ci.check_prompt_commit_trace`, allowing package-style unittest discovery.
- The checker accepts `--commit` and `--base` and provides an explicit `--audit-only` mode that does not require a baseline snapshot.
- Prompt paths are read as repository-root-relative paths from the selected Git tree.
- `PRIMARY` and `MATRIX` report rows are emitted for the strict audit.
- `TRACEABLE` continues to require a verified immutable prompt pin and a reachable implementation commit.
- A current-HEAD digest match is retained as `HEAD_MATCH`; it is not promoted to `PINNED_OK`.
- `NOT_STARTED`, `DISPATCHED`, and `NOT_APPLICABLE` lifecycle states cannot contribute an implementation commit to reachability.
- The historical 138-row cohort metric is kept separate from the full Git-tree manifest audit.
- Manifest implementation status uses the schema's allowed enumeration.
- Evidence-document verification metadata uses `Unverified`, not `Pending`.

# Execution boundary

The revised files have not yet been executed by the coordinator.

The following remain pending:

- Direct test-suite execution.
- `unittest` module execution.
- Strict audit execution against the supplied commit.
- Review of the resulting `PRIMARY`, `MATRIX`, and finding counts.
- PR creation and CI.
- Independent review and Owner acceptance.

No successful test run, successful CI run, PR number, merge SHA, or acceptance decision is asserted by this session record.
