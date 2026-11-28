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
      last_verification_note: "Contains coordinator-supplied execution observations and authoring-session corrections. Revised files have not yet been executed by the coordinator."
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
      - "prompt commit trace"
      - "traceability evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Evidence — AID-2026-327

## 1. Purpose

This record distinguishes three different measurements that must not be conflated:

1. Prompt-file digest agreement.
2. Implementation-commit reachability from the selected comparison base.
3. Strict end-to-end traceability, which additionally requires an immutable prompt pin proving the prompt bytes used at execution time.

A matching prompt file at the current audited commit is not, by itself, evidence that those bytes were the prompt used when implementation began.

## 2. Coordinator observations

The coordinator applied the previous checker and test bodies to a clean worktree:

- Worktree: `C:\tmp\apply327`
- Base: `origin/main`
- HEAD: `cc5d22b9126e00e3f93ffe71282554309908bc89`
- Environment: Windows, CPython 3.12, `PYTHONUTF8=1`

The previous test module failed when invoked with:

`python -m unittest scripts.ci.test_check_prompt_commit_trace -v`

The failure was an import error caused by importing `check_prompt_commit_trace` as a top-level module rather than through `scripts.ci`.

The same test file passed when invoked directly:

`python scripts/ci/test_check_prompt_commit_trace.py -v`

The previous checker did not accept `--commit` or `--base`, did not emit `PRIMARY` or `MATRIX` rows, and resolved repository-root-relative `prompt_file` values relative to the manifest directory. This caused false missing-file findings.

The previous checker also treated lifecycle and implementation-SHA evidence too loosely for the supplied cohort rules.

## 3. Supplied historical 138-row cohort

The supplied cohort contains 138 work items and is classified by the tuple:

`(declared_vs_actual, impl_sha_reach)`

The supplied group counts are:

| Digest classification | Implementation reach | Count |
|---|---|---:|
| MATCH | A | 3 |
| MATCH | N | 5 |
| MATCH | X | 12 |
| MATCH | - | 47 |
| MISMATCH | - | 1 |
| NOFILE | A | 1 |
| NOFILE | - | 2 |
| - | - | 67 |
| **Total** | | **138** |

The three `(MATCH, A)` rows are:

- `AID-2026-047`
- `AID-2026-059`
- `AID-2026-061`

Thus the historical cohort's digest-match and implementation-ancestor intersection is:

`3 / 138 = 2.17%`

The prompt digest match rate is:

`67 / 138 = 48.55%`

These are historical cohort measurements supplied to the authoring session. They are not the strict `TRACEABLE` count emitted by the immutable-pin checker.

## 4. Strict traceability interpretation

The three `(MATCH, A)` rows do not have a verified immutable execution-time prompt pin in the supplied coordinator evidence.

For these rows, a digest match against the current prompt file can establish `HEAD_MATCH`. It cannot establish `PINNED_OK`.

The strict checker therefore must not promote those three rows to `TRACEABLE`.

The expected strict result for the historical intersection is consequently:

- Historical digest-match plus ancestor intersection: 3/138.
- Strict immutable-pin `TRACEABLE` contribution from those three rows: 0/3.

The checker audit population is also distinct from the 138-row historical cohort. The coordinator's previous run enumerated 142 manifests in the selected Git tree. The revised checker audits the full manifest population in the selected commit tree; it does not silently discard four manifests to force the output to equal the historical cohort size.

## 5. Lifecycle handling

An implementation commit must not be counted for work items whose implementation lifecycle is:

- `NOT_STARTED`
- `DISPATCHED`
- `NOT_APPLICABLE`

A stale SHA in one of these records is reported as `commit_unexpected_for_lifecycle`; it is not treated as an implementation commit and cannot establish reachability.

An absent or pending implementation SHA is incomplete evidence, not proof of a failed commit ancestry check.

## 6. Revised execution commands

Test suite, direct invocation:

`python scripts/ci/test_check_prompt_commit_trace.py -v`

Test suite, unittest module invocation:

`python -m unittest scripts.ci.test_check_prompt_commit_trace -v`

Strict checker audit, pinned to the coordinator's supplied worktree HEAD:

`python scripts/ci/check_prompt_commit_trace.py --root . --commit cc5d22b9126e00e3f93ffe71282554309908bc89 --base cc5d22b9126e00e3f93ffe71282554309908bc89 --audit-only`

Expected audit population: all AID manifests present in that commit tree. The coordinator previously observed 142 manifests at this commit.

Expected strict `TRACEABLE` count: 0, based on the supplied absence of immutable prompt pins for the three historical `(MATCH, A)` rows. The revised command must be run to verify the complete current distribution.

## 7. Verification status and limitations

`verification_status` is `Unverified`.

No revised checker execution, revised test execution, PR creation, merge, or Owner acceptance is claimed by this record.

The coordinator must supply the actual exit codes and output from the revised commands before any verification status is changed.
