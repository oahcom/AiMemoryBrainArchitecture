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
        - "14-ai-development/work-items/AID-2026-265/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "The command output quoted here was produced in this branch's worktree on 2026-11-27; the record distinguishes what was executed locally from what was only read from the API."
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
      - "index-table-integrity"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-265 Session Evidence

**Session:** fix-1325-subagent, repurposed by the coordination layer to carry the
INDEX repair as a standalone pull request.
**Implementing AI session string:** `fix-1325-index-split-repair-2026-11-27`
(writer-chosen; no in-repo mechanism relates a session string to a process, so
this is a declaration and not a proof that a distinct context existed).
**Date:** 2026-11-27
**Base:** `f64a3f8bd004135e9873aeafc40e50ef10e10a9c` (`origin/main` at rebase time; the first attempt was
branched from `46dac1b1`, and main advanced five times — to `cbdaf783`, to
`7fc4ddab`, to `f20fff10`, to `b4c1b11d` and to `f64a3f8b` — before this head was
produced)

## What this session did

1. Re-read `origin/main:14-ai-development/work-items/INDEX.md` before acting.
   The `AID-2026-190` row was still two lines (`lf-split` 1) on every base
   checked — `a7cf5256`, `cbdaf783`, `7fc4ddab`, `f20fff10`, `b4c1b11d` and `f64a3f8b` — so the repair was still
   needed and the `ALREADY_FIXED_ON_MAIN` stop condition did not apply.
2. Checked `AID-2026-265` in three places before using it: the work-item tree on
   `origin/main` (`git ls-tree origin/main:14-ai-development/work-items`, no
   `AID-2026-265`), the ledger on `origin/aid-ledger` (`git grep AID-2026-265
   origin/aid-ledger -- aid-ledger.yaml`, no match), and remote branch names
   (`git ls-remote --heads origin`, no branch naming 265). The identifier was
   free.
3. Replayed the first attempt, `6c511ad2`, by cherry-pick onto `cbdaf783`. The
   three-way merge reported success but produced the wrong tree: it re-inserted
   the `AID-2026-191` and `AID-2026-199` rows as stale `DRAFT` duplicates and
   left the `AID-2026-190` pair unjoined. The replay was discarded
   (`git reset --hard origin/main`) and the repair redone by hand — delete the
   line break, restore the missing `v`, append this work item's row — then
   rebased onto `f64a3f8b`.
4. Registered this work item and inserted its INDEX row directly after the repaired
   `AID-2026-190` row — not at the tail — so a concurrent tail append on `main`
   cannot collide with it. The file's final state is its own self-check.
5. Ran the gates listed below against base `f64a3f8b` and recorded the results
   here.

## Prompt digest

`prompt-v1.md` is the executed input snapshot for this session:

```
sha256   c933d0173e736740afb6862c70ca51329cefd0d1a0a37f8d6d4734ceea3f747a
bytes    3242
```

The digest covers the complete file bytes, front matter included. Any later
amendment belongs in a separate artifact, not in these bytes.

## Executed commands and results

| Command | Result |
|---|---|
| `python scripts/check_traceability.py --index-only` | `PASS TRACEABILITY: 0 requirements / 131 work items / 0 errors / 118 warnings` (exit 0; the warnings are the pre-existing per-record T-04/T-05/T-06 advisories, including one for this work item's free-text `tracking_issue`) |
| `python scripts/check_document_management.py` | exit 2 `INCOMPLETE: no rule violations in 766 classified documents, but 370 governed documents are still unclassified` — the same adoption backlog the gate reports on `f64a3f8b` itself (1133 governed / 763 classified / 370 unclassified there; the +3 are this work item's own documents), and zero DM-01..DM-15 violations |
| `python scripts/ci/check_repository_hygiene.py --base f64a3f8bd004135e9873aeafc40e50ef10e10a9c --head <head>` | exit 0, `violations=0`, `manifests=131 in_scope=116`, `Repository new-file admission passed: 4 new path(s) checked`, index membership `directories=142 linked=142` |
| `python scripts/ci/check_work_item_uniqueness.py --base f64a3f8bd004135e9873aeafc40e50ef10e10a9c --head <head>` | `PASS ... introduced=1 occupied=0` (exit 0) |
| `BASE_SHA=f64a3f8bd004135e9873aeafc40e50ef10e10a9c HEAD_SHA=<head> python scripts/check_bilingual_docs.py` | `PASS (5 changed paths inspected)`, `bilingual baseline: 77 frozen, 0 new gaps` (exit 0) |

## Limits of this record

- `scripts/check_declared_check_contexts.py` cannot run in this environment: the
  local HTTPS egress terminates TLS with a private CA and the script verifies the
  chain, so it exits 2 `INCOMPLETE` before comparing anything. The `Existing gates`
  workflow covers it.
- CI conclusions for the new head are read from the REST API and recorded on the
  pull request; nothing here asserts a required context passed unless a check run
  reported it.
- No merge, squash, force-push, or issue closure was performed. The branch is
  rebased onto the current `main`, not merged with it.
