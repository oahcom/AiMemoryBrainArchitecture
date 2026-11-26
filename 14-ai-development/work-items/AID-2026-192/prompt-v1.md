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
        - "14-ai-development/work-items/AID-2026-192/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Structured snapshot of the dispatched task, assembled after the fact; the verbatim dispatching message was not captured, which is why the manifest records prompt_status: NOT_RECORDED."
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
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Prompt snapshot v1 — AID-2026-192

**Status: structured task snapshot, not a verbatim transcript.** `prompt_status: NOT_RECORDED`.
The dispatching session's message was not preserved byte for byte. What follows is the task
content the implementing session acted on, written from the dispatch after the fact.

## Task

Repair one governance record and two work items in `D:\code\wt-counts` on branch
`fix/2026-11-27-stale-counts-and-claims`, without changing any historical verdict.

1. `docs/governance/documentation-gaps.md:51` (GAP-03) said 26 architecture documents under
   `docs/` and 196 Markdown files under `reviews/`. The authoritative value for the first is 27
   and the measured value for the second is 198. Replace both with the correct values and
   annotate the same line `(verified 2026-11-27 against <tree SHA>)`.
2. `14-ai-development/work-items/AID-2026-111/evidence.md`: the §1 combined row reads
   0 / 36 / 52 while the three set rows above it sum to 0 / 34 / 54. Do **not** edit the
   combined row. Append a `## Correction` section that lists each judgment row, shows the
   summation, says which of the two totals the rows support, and states the correct total.
3. `14-ai-development/work-items/AID-2026-112/evidence.md`: AID-2026-111 records the
   memory-context group's exit code, failed count and test-binary count as `NOT_RECORDED`;
   AID-2026-112 records them as `0`, `0` and `11`, plus a stdout SHA-256, with no new capture
   cited. Do **not** change its conclusions. Append a `## Provenance correction` section that
   says what AID-2026-111 records, that no new collection is referenced, and marks the three
   fields `INHERITED_ASSUMPTION`.
4. The canonical, EN and ZH-CN copies must stay structurally consistent, and so must the
   three AID-2026-112 copies.

## Constraints stated at dispatch

- Do not change any historical verdict value: PASS / PARTIAL_EVIDENCE / UNCHANGED stay as
  recorded.
- Do not change any blob pin, and do not re-run any test.
- Do not work outside `D:\code\wt-counts`.
- Registration set: manifest, evidence, prompt snapshot, session evidence, EN and ZH-CN
  mirrors, one `INDEX.md` row.
- PR body must carry `Related issue(s)`, `AI-assisted work: YES` and a `Session evidence
  reference(s)` path that resolves in the head tree.
- Merge only on 16/16 required contexts at the exact head, behind = 0, `merge_method: merge`,
  then verify every changed blob against `origin/main`.

## Measured values supplied with the dispatch

- Authoritative architecture-document count under `docs/`: **27** (registry backlog claim).
- Measured `reviews/**/*.md`: **198**.
- AID-2026-111: 72 Gate A cells + 8 SC + 8 HIR = 88 verdict rows; recorded combined row
  0/36/52; the dispatch described the row inventory as "95 rows", which the body does not
  reproduce.
