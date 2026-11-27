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
        - "14-ai-development/work-items/AID-2026-263/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Local command output is quoted verbatim. No CI run, merge, or platform-side branch-protection read is claimed; the REST quota was exhausted before a pull request could be created."
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
      - "session-evidence"
      - "merge-broker"
      - "work-item-uniqueness"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# Session Evidence — AID-2026-263

## Session role / use case

Implementation session for Issue #1341, Option (d) as selected in Issue #1331: a
serialized, merge-time work-item uniqueness gate. The session was dispatched as
"IMPL-B" by a coordinating session and executed on a Windows host with a local
git worktree; no GitHub write operation was performed by this session.

## Actual AI input

The dispatching instruction is reproduced verbatim in `prompt-v1.md`. In
substance it required: the broker workflow with the exact trigger, concurrency
group, permissions, re-enumeration, per-candidate re-read, merge-candidate
evaluation, and `sha=<head>` pinned merge; the eight acceptance rows quoted from
Issue #1341; `BROKER_SERIALIZATION_UNPROVEN` wherever the exclusivity boundary
cannot be enforced; and a hard prohibition on adding a required context,
declaring the broker a required check, merging, closing an Issue, or changing
branch protection.

## Facts established before authoring

1. `AID-2026-255`, `AID-2026-242` and `AID-2026-261` are all unavailable.
   `AID-2026-242` is on `main`; `AID-2026-261` exists only as an uncommitted
   `manifest.yaml` in another session's worktree whose branch head
   (`a7a252eb`) is the merge commit of PR #1364 and contains no AID-2026-261
   work. `AID-2026-255` was a mis-allocation by the dispatching session.
2. `AID-2026-263` is free: `git ls-tree -d origin/main 14-ai-development/work-items/`
   contains no `AID-2026-26*` entry.
3. **Issue #1341's checker half was already merged** while this branch was being
   prepared: AID-2026-279, `feat(ci): enforce merge-time work-item uniqueness`,
   commit `84790d36`, merged by PR #1372 as `386d8f57`. `main` therefore already
   carries `scripts/ci/check_work_item_uniqueness.py`,
   `scripts/ci/test_work_item_uniqueness.py`, and its wiring in the required
   GOV-DOC-002 job (`.github/workflows/document-management.yml` lines 32-46).
4. AID-2026-279's own evidence records the gap this work item fills: the
   `/protection` endpoint returned HTTP 403 to that session, so `strict` and
   `enforce_admins` are unasserted and "merge serialization through strict
   freshness remains unverified".

Consequence, recorded as `scope.deviation` in `manifest.yaml`: this session did
not write a second checker. The broker calls the merged one.

## AI-visible output

Authored on branch `work-item/aid-2026-262-merge-broker`:

- `.github/workflows/work-item-merge-broker.yml` — the serialized merge broker.
- `scripts/ci/test_work_item_merge_broker.py` — 11 tests: 7 structural
  assertions on the workflow text (no YAML dependency) and 4 composition tests
  that drive the merged checker through the two references the broker passes it.
- `14-ai-development/work-items/AID-2026-263/{manifest.yaml,evidence.md,prompt-v1.md,session-evidence.md}`
  and one `INDEX.md` row.

No existing file was deleted or rewritten, no workflow was modified, no required
context was added, and branch protection was not touched.

## Local command output

```
$ python scripts/ci/test_work_item_merge_broker.py
Ran 11 tests in 6.926s

OK
```

```
$ python scripts/ci/check_work_item_uniqueness.py --base HEAD --head HEAD
WORK-ITEM UNIQUENESS: PASS (base=386d8f57b02d8e3c511ff0e3980b9ce0af8b3028 candidate=386d8f57b02d8e3c511ff0e3980b9ce0af8b3028 introduced=0 occupied=0)
```

```
$ python scripts/ci/audit_runner_admission.py
GitHub-hosted runner policy: 29 job(s) audited, 0 violation(s)
```

```
$ python scripts/ci/check_test_reachability.py
Test reachability: 68 test files, 68 reachable, 0 unreachable
Gate wiring: 20 gate scripts, 3 unwired, 3 baselined
```

```
$ python scripts/check_traceability.py --index-only
PASS TRACEABILITY: 0 requirements / 115 work items / 0 errors / 108 warnings
```

```
$ python scripts/ci/check_repository_hygiene.py --base 386d8f57b02d8e3c511ff0e3980b9ce0af8b3028 --head <this commit>
Work-item index membership version=2026-11-27.2 directories=126 linked=126
Work-item manifest consistency version=2026-11-27.2 manifests=115 in_scope=101 excluded_by_record_type=5 unrecognized=9 violations=0
Repository new-file admission passed: 6 new path(s) checked.
```

```
$ python scripts/check_document_management.py --require-changed <base>
(exit 0; no AID-2026-263 finding)
```

## What this session did not do, and does not claim

- No CI run, required-context result, merge SHA, or post-merge blob digest.
- No live broker execution: the GitHub REST quota was exhausted (`GET
  /rate_limit` reported `remaining: 0`), so no pull request and no
  `merge-ready` run exists. The merge path in the workflow has never executed.
- No branch-protection or ruleset read on 2026-11-27. The dated 2026-11-25
  reading in `14-ai-development/PR-GOVERNANCE-001.md` is quoted as a document,
  not as a measurement.
- No independent review, and no Owner acceptance.
- AID-2026-279's own tests were not executed on this host: they invoke
  `python3`, which is a Microsoft Store stub here (exit 9009). This work item's
  tests use `sys.executable` for that reason, and the merged checker's behaviour
  is exercised here through the composition tests instead.
