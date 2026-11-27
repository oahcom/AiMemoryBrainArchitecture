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
      last_verification_note: "Every figure below was produced by a command run in this branch's worktree on 2026-11-27 against origin/main 756e1e25. The before/after row text is quoted with control characters escaped, and the byte, pipe, and row counts were measured rather than eyeballed."
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
      - "index-table-integrity"
      - "document-management"
      - "gate-visibility"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-265 Evidence — the split AID-2026-190 row in the work-item INDEX

**Attribution:** user-authorized operator (delegated by account owner)
**Date:** 2026-11-27
**Issue:** none — this is a pre-existing defect on `main` with no tracking issue yet
**Base observed at implementation start:** f64a3f8bd004135e9873aeafc40e50ef10e10a9c (`origin/main`; the defect was also re-confirmed on the earlier bases `b4c1b11d`, `f20fff10`, `7fc4ddab`, `cbdaf783`, `a7cf5256` and `756e1e25`, before main advanced each time)

## The defect

`14-ai-development/work-items/INDEX.md` renders the `AID-2026-190` row as two
physical lines. The first ends with a literal backslash; the second begins with
`erification_status`. The `v` of `verification_status` is missing, so the row
carries seven pipe separators on the first line and three on the second instead
of ten on one line, and the table cell reads `erification_status`.

Before, with control characters escaped (the row is quoted from the first
character; the interior is elided at `…` only for width):

```
L1: | [AID-2026-190](AID-2026-190/manifest.yaml) | … no historical table cell,
    no blob, no \                       <- line ends here, 7 pipes total
L2: erification_status\ value, no checker, workflow or registry change | …
    #1212 remains OPEN |                <- 3 pipes total
```

After:

```
| [AID-2026-190](AID-2026-190/manifest.yaml) | … no historical table cell,
  no blob, no \verification_status\ value, no checker, workflow or registry
  change | … #1212 remains OPEN |        <- one line, 10 pipes
```

The change is exactly: delete the line break and restore the missing `v`. The
repair alone leaves the file's byte length unchanged (one byte removed, one byte
added); the growth shown in the measurements comes from this work item's own row.

## Re-run on the current main (second pass)

The first attempt (`6c511ad2`, PR #1418) was branched from `46dac1b1`. Main then
advanced to `cbdaf783` and further to `7fc4ddab`, and GitHub reported the pull
request as `mergeable_state=dirty` with no check run on its head. Replaying
`6c511ad2` by cherry-pick onto `cbdaf783` produced a wrong result: the three-way
merge re-inserted the neighbouring `AID-2026-191` and `AID-2026-199` rows as
stale `DRAFT` duplicates instead of joining the `AID-2026-190` pair, leaving
three duplicate work-item rows in the table. That replay was discarded
(`git reset --hard origin/main`) and the repair was redone by hand — join the
pair, restore the missing `v`, append this work item's row — then rebased onto
`7fc4ddab`. The final tree carries exactly one row per AID and no duplicated
neighbour.

## Where it came from

| Step | Commit | State of the row |
|---|---|---|
| Row added | `a38a2c3e` (docs(gov): append reproducible corrections … AID-2026-190) | Broken on arrival: the break is stored as `\` + `0x0B` (vertical tab) + `erification_status\` |
| Row reaches this branch's PR base | `987d2602` | Break is already a real LF; `0x0B` count 0; `lf-split` 1 |
| Current `main` | `a7cf5256` (also checked at `756e1e25`) | Unchanged: still two lines, one line starting with `erification`, 7 + 3 pipes |
| PR #1325 | `671032f3` → merged `3daebd2c` | INDEX.md diff is `+1` line (the AID-2026-191 row); the broken pair is preserved verbatim, not introduced |

`a38a2c3e` is an ancestor of `origin/main` (`git merge-base --is-ancestor a38a2c3e
origin/main` exits 0), and the pair is present in the `987d2602` and `756e1e25`
blobs. The defect is therefore pre-existing on `main`, not introduced by PR #1325
or by this branch.

## Why no required context reports it

| Gate | Behaviour over the broken pair |
|---|---|
| `Repository hygiene` (`scripts/ci/check_repository_hygiene.py`) | exit 0, `violations=0`; measured twice over the pair: over `main`'s own merge commit `a7cf5256` (`--base c2b346de --head a7cf5256`, break present) and over branch head `fe16a378` in CI (run 45940862448) |
| `GOV-DOC-002 metadata checks` | exit 0; it inspects the front-matter block, not table geometry |
| `Traceability` (`check_traceability.py --index-only`) | `PASS … 0 errors` with the pair present |
| Bilingual gate | not applicable to table geometry |

A broken table row is therefore invisible to every required context. That is the
reason this work item exists as a repair rather than as a gate change: the same
defect can be introduced again without anything turning red.

## Measurements

Measured on `origin/main` = `f64a3f8b` against this branch's final tree.

| Measurement | Before | After |
|---|---|---|
| Pipe separators on the `AID-2026-190` row | 7 + 3 across two lines, 7 cells, not ending in a pipe | 10 on one line, 9 cells, ending in a pipe |
| `verification_status` present as a complete word | no (`erification_status`) | yes |
| Lines beginning with `erification` | 1 (the continuation line) | 0 |
| Standalone truncated token (`erification_status` not preceded by `v`) | 1 | 0 |
| Control characters outside TAB/LF/CR (whole file) | none (`0x0B` count 0, CR count 0) | none |
| Table lines (lines beginning with a pipe character) | 205 | 206 (this work item's own row added; the joined continuation line was never a table line, so the repair alone does not change the count) |
| File bytes | 217086 | 217839 |
| File LF count | 325 | 325 (one line removed by the join, one added by this work item's row) |

## Same class of defect found while measuring, deliberately not repaired

| Row | Line | Pipe separators | Shape |
|---|---|---|---|
| `AID-2026-071` | 94 | 9 | 8 cells, does not end in a pipe |
| `P2-T2-MEMORY-SCHEMA` | 277 | 7 | 7 cells in a 9-column table |

Both are pre-existing and out of scope here: repairing them would widen a
single-purpose change and collide with concurrent INDEX edits. They are recorded
so the class stays visible.

## Suggested coverage (not implemented here)

No gate reads table geometry, so a one-line check inside the existing
`GOV-DOC-002` job would close the class: for every table block in
`14-ai-development/work-items/INDEX.md`, assert that each row has the same pipe
count as its header, ends with a pipe, and that the file contains no control
characters other than TAB/LF/CR. That is a checker and workflow decision with its
own blast radius; this work item records the proposal and changes nothing in
`scripts/` or `.github/workflows/`.


## Verification commands

```
python scripts/check_traceability.py --index-only
python scripts/check_document_management.py
python scripts/ci/check_repository_hygiene.py --base f64a3f8bd004135e9873aeafc40e50ef10e10a9c --head <head>
python scripts/ci/check_work_item_uniqueness.py --base f64a3f8bd004135e9873aeafc40e50ef10e10a9c --head <head>
BASE_SHA=f64a3f8bd004135e9873aeafc40e50ef10e10a9c HEAD_SHA=<head> python scripts/check_bilingual_docs.py
```

Raw output is summarised in `session-evidence.md`. No merge, squash, force-push
or issue closure is performed by this work item; the branch is rebased onto the
current `main` rather than merged with it.

## Boundaries

Only `14-ai-development/work-items/INDEX.md` and this work item's own directory
are changed. No checker, workflow, registry, branch protection, or required
context is modified; the repair does not add a gate for the class of defect it
repairs.
