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
        - "14-ai-development/work-items/AID-2026-341/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured prompt snapshot; original dispatch payload bytes and digest are not independently available."
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
      - "AID-2026-341"
      - "prompt commit trace"
      - "checker evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Prompt snapshot — AID-2026-341

## Provenance

- Work item: `AID-2026-341`
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`
- Supplied worktree base: `cc5d22b9126e00e3f93ffe71282554309908bc89`
- Prompt provenance: `STRUCTURED_TASK_SNAPSHOT`
- Prompt status: `NOT_RECORDED`
- Prompt SHA-256: `NOT_VERIFIED`
- Prompt byte count: `NOT_VERIFIED`
- Recorded-snapshot pin: the manifest's `prompt_sha256` and
  `prompt_file_blob_sha` pin the bytes of this recorded snapshot only. They
  do not claim to reproduce the unrecorded original dispatch payload, whose
  digest and byte count remain `NOT_VERIFIED`.

This file is a structured snapshot of the task and coordinator corrections. It is not claimed to be a byte-for-byte archive of the original task payload.

## Goal

Repair the prompt-to-commit trace checker and its tests so that the checker reports prompt integrity, immutable prompt-pin verification, implementation reachability, and strict end-to-end traceability without conflating those facts.

Preserve the existing primary decision order and ratchet semantics.

## Required semantics

1. `NO_TRACE` takes precedence when the prompt digest or implementation commit is absent.
2. `DIGEST_UNPINNED` applies when a digest exists but no immutable prompt pin verifies execution-time bytes. A current-HEAD match is not an immutable pin.
3. `DIGEST_MISMATCH` applies when an immutable pin exists but fails digest verification.
4. `COMMIT_UNREACHABLE` applies when prompt evidence is pinned correctly but the implementation commit is not reachable from the selected target.
5. `TRACEABLE` requires both a verified immutable prompt pin and a reachable implementation commit.
6. `NOT_STARTED`, `DISPATCHED`, and `NOT_APPLICABLE` lifecycle states cannot contribute an implementation commit to reachability. A stale SHA in one of these states is a finding, not a usable implementation pin.
7. Prompt paths stored as repository-root-relative paths must be resolved from the repository root, not from the manifest's directory.
8. The checker must support `--root`, `--commit`, `--base`, `--json`, and a read-only `--audit-only` mode.
9. The audit must expose `PRIMARY`, `MATRIX`, and `FINDING` output.
10. Preserve the legacy ratchet findings `DIGEST_MISMATCH`, `REGRESSION`, and `NEW_FINDINGS`; each must retain a negative test.
11. Tests must be importable with `python -m unittest scripts.ci.test_check_prompt_commit_trace -v` and executable directly.
12. No test-success or CI-success claim may be written before coordinator execution.

## 138-row historical measurement

The supplied historical cohort contains 138 rows:

| Classification | Count |
|---|---:|
| `MATCH / A` | 3 |
| `MATCH / N` | 5 |
| `MATCH / X` | 12 |
| `MATCH / -` | 47 |
| `MISMATCH / -` | 1 |
| `NOFILE / A` | 1 |
| `NOFILE / -` | 2 |
| `- / -` | 67 |
| **Total** | **138** |

The prompt digest match rate is:

`67 / 138 = 48.55%`

The intersection of digest match and implementation ancestry is:

`3 / 138 = 2.17%`

The three rows in that intersection are:

- `AID-2026-047`
- `AID-2026-059`
- `AID-2026-061`

This 3/138 intersection is a historical cohort metric. It is not the strict `TRACEABLE` count: the supplied evidence does not establish immutable execution-time prompt pins for these three items.

## Strict repository audit population

The coordinator's prior run enumerated 142 manifests at:

`cc5d22b9126e00e3f93ffe71282554309908bc89`

The full repository audit and the 138-row historical cohort are different populations. The checker must audit all AID manifests in the selected Git tree and must not discard four records to force the audit population to 138.

The strict `TRACEABLE` contribution from the three historical `(MATCH, A)` rows is zero because `HEAD_MATCH` without an immutable prompt pin is not `PINNED_OK`.

The coordinator must verify the complete strict audit distribution by running:

`python scripts/ci/check_prompt_commit_trace.py --root . --commit cc5d22b9126e00e3f93ffe71282554309908bc89 --base cc5d22b9126e00e3f93ffe71282554309908bc89 --audit-only`

Expected population from the coordinator's previous tree enumeration: 142 manifests.

Expected strict `TRACEABLE` count: 0.

These are the expected audit population and strict count for coordinator verification, not a claim that the revised checker has already been run.

## Coordinator execution

Test command:

`python scripts/ci/test_check_prompt_commit_trace.py -v`

Module invocation:

`python -m unittest scripts.ci.test_check_prompt_commit_trace -v`

Audit command:

`python scripts/ci/check_prompt_commit_trace.py --root . --commit cc5d22b9126e00e3f93ffe71282554309908bc89 --base cc5d22b9126e00e3f93ffe71282554309908bc89 --audit-only`

Coordinator-local execution (EXECUTED_BY_COORDINATOR_NOT_IN_CI; not CI) against the rebase-after PR code commit d43851732: targeted unittest module — 14 tests, OK, exit 0; repository-wide discovery — 194 tests, FAILED (8 failures, 2 errors), exit 1; the same 10 test_work_item_uniqueness failures were reproduced on origin/main, an existing Windows python3 PATH issue; strict audit — 151 manifests, TRACEABLE=0, exit 0; traceability index — 0 requirements / 150 work items / 0 errors / 125 warnings, exit 0; manifest schema — 0 new violations, exit 0; document management — 1208 governed / 838 classified / 370 unclassified, exit 2, pre-existing and not introduced by this PR.
