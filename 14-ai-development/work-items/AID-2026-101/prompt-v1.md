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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-26"
      last_verification_note: "Every count and SHA in this prompt was measured in the session that executed it: the three defects re-verified on main c6b7d987 after two identifier collisions forced renumbering, the PR facts fetched from the API, and the digest substitution that reproduced the superseded value exactly. None is copied from a pull request body."
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

# AID-2026-101-PROMPT v1 — Refresh three stale registry cells and one false prompt digest

## User dispatch

Repository: `oahcom/AiMemoryBrainArchitecture`.
Base: `main` at `ef988da3` (observed 2026-11-26).
Task: correct three registry defects measured in this session, and register the correction
so that `INDEX.md`'s own refresh rule is satisfied rather than bypassed.

## The rule this work item exists to obey

`14-ai-development/work-items/INDEX.md` states, above the table:

> every `Status`, `Review` and `Acceptance` cell that names a carrier PR MUST be refreshed
> when that carrier merges or closes; a stale cell is a defect in this registry, not a
> historical record. ... no cell is rewritten without an authorization that names it.

The second clause is the reason this work item exists. The correction cannot be made by a
commit that has no record behind it; the record is this manifest, and it itemises the prior
value of every cell it changes.

## Authorized scope

- `14-ai-development/work-items/INDEX.md` — three rows only: `AID-2026-047`,
  `AID-2026-072`, `AID-2026-076`, plus the row for this work item.
- `14-ai-development/work-items/AID-2026-047/manifest.yaml` — the `prompt_sha256` field.
- `14-ai-development/work-items/AID-2026-072/manifest.yaml` — the lifecycle fields that
  assert the carrier is still open.
- `14-ai-development/work-items/AID-2026-076/manifest.yaml` — the `implementation` block.
- `14-ai-development/work-items/AID-2026-101/` — this work item's own files.

## Explicitly out of scope

- No Rust source file. No crate. No test in a crate.
- No new checker and no new workflow step. The absence of a freshness gate is recorded as a
  finding below, not repaired here: wiring one is a different authorization and a different
  work item, and a correction that quietly grows a gate is not a correction.
- No other INDEX row. The measurement that selected these three rows is written into the
  manifest so that the selection can be re-run and disputed.

## Acceptance

A1. `prompt_sha256` in `AID-2026-047/manifest.yaml` equals the SHA-256 of the committed
    `prompt-v1.md`, and the superseded value is recorded rather than overwritten.
A2. `AID-2026-076`'s `implementation` block names PR #1155, its merge commit and that the
    carrier merged, and no field still says the carrier is open.
A3. `AID-2026-072`'s record distinguishes two facts that are both true: the PR it was
    dispatched under closed **without merging**, and a different PR merged the same work.
A4. Each corrected INDEX cell states which outcome occurred; none describes a closed-unmerged
    carrier as merged.
A5. `scripts/check_traceability.py --index-only` and `scripts/ci/check_repository_hygiene.py`
    both exit 0, and the hygiene manifest-consistency counter still reports `violations=0`.
A6. The prior value of every changed cell is itemised in the manifest, so the diff is not the
    only place history survives.
