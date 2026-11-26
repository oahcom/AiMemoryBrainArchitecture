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
        - "14-ai-development/work-items/AID-2026-190/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task and what the implementing session did with it; the platform session identifier and the verbatim model stream were not captured."
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
      - "gov-doc-002"
      - "frontmatter"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Session Evidence — AID-2026-190

## Session role / use case

Documentation-metadata worker. The assistant was dispatched as a subagent to read two briefs and
execute one unit end to end: add GOV-DOC-002 metadata to the unclassified `docs/en` and `docs/zh-CN`
mirrors of `07-agent-integration`, `08-bmcp-protocol` and `13-engineering-decisions`, without
touching the 58 frozen bilingual gaps and without moving the 77-entry baseline.

## Actual AI input

The dispatching session supplied, in this order:

- a task message naming two files to read (`fix-brief-common.md`, `unit-corpus-b.md`), the fixed
  work tree `D:\code\wt-corpus-b` and branch `fix/2026-11-27-mirror-frontmatter-b`, and the explicit
  instruction "only work inside it", "do not ask questions";
- the unit rule that the 58 frozen `13-engineering-decisions` gaps must not be closed, only
  frontmatter may be added, and that `check_bilingual_docs.py` must show `77 frozen` unchanged
  before and after;
- the common brief: work-item layout (`manifest.yaml`, `evidence.md`, `prompt-v1.md`,
  `session-evidence.md`, one `evidence.md` under each language mirror, one `INDEX.md` row), the
  manifest fields, block-style YAML (inline `{}` is refused by `_scalar()`), the PR body shape with
  `Session evidence reference(s)` as a full head-tree path, merge discipline (16 contexts, behind 0,
  `merge` method, blob verification), and the prohibition list (no branch-protection edit, no Issue
  close, no required-context deletion, no fabricated SHA or gate output, no bypass of a red gate).

Both briefs are preserved verbatim in `prompt-v1.md`, with its byte count and SHA-256 in the
manifest. The platform session identifier was not available to the worker, so it is recorded as
`NOT_RECORDED` rather than invented.

The model serving this unit was `opencode-go/deepseek-v4.1-flash`; the brief records that the
primary upstream (`9router`, two models) was returning 429, and asks that the substitution be
stated in the report.

## AI-visible output

1. **Enumeration.** 22 unclassified mirrors in the three directories (5 + 5 in
   `07-agent-integration`, 3 + 3 in `08-bmcp-protocol`, 3 + 3 in `13-engineering-decisions`),
   cross-checked against `scripts/bilingual-baseline.txt` (77 entries, 58 of them under
   `13-engineering-decisions`).
2. **Classification of two complete groups (6 files).** `07-agent-integration/inference-boundary-model.md`
   and `07-agent-integration/telemetry-model.md` each received a metadata block, and their
   `docs/en` and `docs/zh-CN` mirrors received a block naming the root as `source`. Every block
   parses (`read_metadata(...) is not None` → `True` on all six files).
3. **Measured refusals, not assumptions.** Two probes were run and reverted in the same session:
   - an orphan mirror with `source` set → `DM-12 ... does not exist` and `DM-12 ... is not a
     classified governed document` (4 errors), which is why 16 files are reported as
     `ORPHAN_SKIPPED`;
   - a frozen `13-engineering-decisions` source with a metadata block → `check_bilingual_docs.py`
     FAILs with `requires all counterparts changed in this PR`, which is why the 58 stay `0/58`.
4. **Gate evidence.** Whole-tree `check_document_management.py` 496 → 502 classified with 0 rule
   violations and 446 → 440 unclassified; `07-agent-integration` 6/8 → 8/8; `docs` 173/343 →
   177/343; ratchet `baseline=77 current=77 regressions=0 fixed=0` before and after; incremental
   gate PASS on the exact head.
5. **This registration set.** `manifest.yaml`, `evidence.md` (root plus EN and ZH-CN mirrors),
   `prompt-v1.md`, this file, and one `INDEX.md` row.

Nothing in the output claims that the 22-file defect is closed or that the English and Chinese
mirror text is semantically equivalent.
