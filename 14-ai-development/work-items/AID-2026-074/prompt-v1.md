---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: content-hash
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "The assignment this record reproduces is the one executed in session-a1084 against origin/main at 073ffe3e. It was written after the session rather than before it, so it is RECORDED_NOT_FROZEN and its provenance is NOT_VERIFIED; the measurement it points at is the session evidence file beside it."
    usage_status: Active
    modification_status: Unchanged
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-074 — Prompt v1

Work item: `AID-2026-074`
Issues: #1064, #1069
Class/Risk: GATE/CONFIG/TEST / R1
Prompt status: `RECORDED_NOT_FROZEN` — assembled after the session from the
assignment actually executed, so provenance is `NOT_VERIFIED`.

## Assignment as executed

Two issues, one change, because fixing either alone makes the other worse.

### #1069: the false conflict

`14-ai-development/work-items/INDEX.md` is a table with one row per work item,
and every registration appends a row. Two concurrent registrations therefore
conflict on text adjacency alone: both rows are wanted, nothing sorts the
table, and no cell in one row constrains a cell in the other.

Add one path-scoped union merge driver:

```
14-ai-development/work-items/INDEX.md merge=union
```

Only this path. `*.md merge=union` would be destructive for prose, where union
alternates both sides' paragraphs.

Before trusting the driver, confirm the table is a shape union can handle: one
row per work item, no multi-line cells, no wrapping. A table where a row spans
lines cannot be union-merged, because a union of half-rows parses as neither
side.

### #1064: the missing detector

A union driver keeps both sides' appended lines. That eliminates the false
conflict, and it also eliminates the last accidental detector of a duplicate
work-item ID: today a duplicate ID produces an add/add conflict on the
directory. So the driver must ship with an assertion that refuses a duplicate,
or the next collision merges cleanly as two rows claiming one number.

The assertion already exists. `scripts/check_traceability.py:730` reports
`T-04 duplicate INDEX entry {aid}`, and `:666-670` reports a `work_item_id`
that disagrees with its directory. Neither has ever run against the tree,
because `run_check` calls `parse_registry` first inside the same `try`, and
`00-governance/requirements-registry.yaml` does not exist. The registry is a
required input and its absence is correctly an error; the defect is that the
manifest half is unreachable behind it.

So: give the half that needs no registry an entry point of its own, and run it
in the job that is already a required context. Do not write a second detector.

### Explicitly not built

- No ID reservation service, no allocator, no registry of taken-but-unmerged
  IDs. #1064 rejects these and the rejection stands: they need coordination
  this repository does not have.
- No `next_id` cell in `INDEX.md`. That converts an append conflict into a
  same-cell conflict, raising the rate rather than lowering it.
- No generated table derived from directories. Correct in principle, a much
  larger change, and it requires the derivation to be order-stable and
  duplicate-aware first — the same prerequisites this change already pays.
- No renumbering of any existing work item.
- Nothing under `crates/`.

## Acceptance as executed

Measured, not asserted. The nine criteria are in `manifest.yaml`; the
measurements themselves are in `session-evidence-1064-1069.md`.

The load-bearing ones:

1. `--index-only` exits 0 on the unmodified tree, and the default invocation
   still exits 1 for the missing registry. Both forms run on the same tree.
2. A duplicate row exits 1 naming `T-04 duplicate INDEX entry`; reverting it
   exits 0.
3. `merge=union` merges two concurrent registrations at the same anchor with
   `rc=0` and keeps both rows.
4. The three shapes union does not resolve each end as one `AID` on two lines,
   so (2) refuses them. This is measured for all three, including the deletion
   shape, which is the one whose symptom is a resurrected row.
5. Mutating either half fails the suite: removing the `T-04 duplicate` call
   fails two tests, making `--index-only` a no-op fails four.

## What this does not fix

A collision between two sessions that have each written their files but not
merged is still invisible to everyone. Detecting that needs the open-PR list
and a `Work Item ID` field that something reads, which is #1042's subject.
This change catches the merged case — the one that actually happened three
times in one hour — and the residual is stated rather than closed.
