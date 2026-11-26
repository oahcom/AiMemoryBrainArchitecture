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
        - "14-ai-development/work-items/AID-2026-190/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task and what the implementing session did with it; the session identifier and the verbatim model input stream were not captured."
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
      - "documentation-gaps"
      - "work-item-arithmetic"
      - "provenance"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# Session Evidence — AID-2026-190

## Session role / use case

Documentation repair worker. The assistant was dispatched to fix three statements in the
governance record and two evidence work items without changing any historical verdict: a stale
pair of counts in `documentation-gaps` GAP-03, an addition error in the AID-2026-111 combined
row, and three execution fields in AID-2026-112 that the earlier record marks `NOT_RECORDED`.

## Actual AI input

The dispatching session supplied two brief files, in this order:

- a common brief: work only inside `D:\code\wt-counts` on branch
  `fix/2026-11-27-stale-counts-and-claims`; take a free AID number after checking occupancy;
  write the work-item set (`manifest.yaml`, `evidence.md`, `prompt-v1.md`,
  `session-evidence.md`, EN and ZH-CN mirrors, one INDEX row); use block-style YAML because an
  inline `{}` makes the metadata parser raise `ParseError`; PR body must carry
  `Related issue(s)`, `AI-assisted work: YES` and a `Session evidence reference(s)` path that
  resolves in the head tree; merge only with 16/16 required contexts green at the exact head,
  behind = 0, `merge_method: merge`, then verify blobs against `origin/main`;
- a unit brief naming the three defects, the authoritative 27 and measured 198, the two
  candidate totals 36/52 and 34/54, and the prohibition list: do not change historical
  verdicts (PASS / PARTIAL_EVIDENCE / UNCHANGED stay), do not change any blob, do not re-run
  any test, and append correction sections rather than rewriting the recorded values.

The model serving this unit was `opencode-go/deepseek-v4.1-flash`, the fallback the common
brief names because the free 9router pool was returning 429. That is recorded because it
changes which model produced the text, not what was asked for.

## What the session did

1. Read both briefs, then measured instead of trusting them: `docs/**/*.md` minus
   `docs/en`, `docs/zh-CN` and the individually governed gap record is **27**; `reviews/**/*.md`
   is **198**; the AID-2026-111 body holds **88** verdict-bearing rows (72 + 8 + 8), not the
   95 the brief described, and those rows tally to 23/49, 6/2, 5/3 → 0/34/54.
2. Corrected GAP-03 in place (26 → 27, 196 → 198) with the `(verified 2026-11-27 against tree
   4326669c…)` annotation, and checked that `docs/governance/` has no EN or ZH-CN mirror to
   sync — it is not a `NORMATIVE_ROOT`, and the changed row is English-only.
3. Appended `## Correction` to the three AID-2026-111 copies before the session-evidence
   sections, leaving the §1 table and the 0/36/52 combined row untouched, and listing all 88
   verdicts (a 9-checkpoint × 8-flow table plus the 8 SC and 8 HIR rows individually).
4. Appended `## Provenance correction` to the three AID-2026-112 copies at the end, leaving the
   §8 table, the 552 title and every verdict untouched, and marking Exit code, Failed count and
   Test binaries `INHERITED_ASSUMPTION` with the unsourced stdout hash noted separately.
5. Took `AID-2026-190` after confirming the INDEX maximum was 189 (merged) and that no pull
   request title, head branch or work-item directory carried 190; wrote this registration set
   and one INDEX row.
6. Ran the repository's own gates locally: metadata parse `True` on all seven edited files,
   line endings 1629 files / 0 violations, document management `INCOMPLETE` with **zero rule
   violations** (the documented backlog state, not a finding).

## AI-visible output

The assistant reported, and the head of this branch confirms:

- `docs/governance/documentation-gaps.md` GAP-03 now reads 27 architecture documents under
  `docs/` and 198 Markdown files under `reviews/`, with the tree SHA `4326669c…` and the
  counting rule inline; the registry's `documents: 27` was not edited because it was already
  correct;
- AID-2026-111 carries `## Correction` in canonical, EN and ZH-CN: the §1 combined row still
  reads 0 / 36 / 52, and the appended section shows 23 + 6 + 5 = 34 and 49 + 2 + 3 = 54,
  concludes 0 / 34 / 54 = 88 rows, and notes that the record's own `AI-visible output` section
  already states 34 / 54;
- AID-2026-112 carries `## Provenance correction` in all three copies: AID-2026-111 §2.3 at the
  same HEAD records exit code, failed count and test-binary count as `NOT_RECORDED`, no new
  capture is cited anywhere in AID-2026-112 for them, and the three fields are graded
  `INHERITED_ASSUMPTION`; 552 = 99 + 276 + 177 is retained as a sum of three passed counts;
- no verdict, no blob pin, no registry value, no checker, no workflow and no required context
  changed; nothing under `scripts/`, `tests/` or `.github/` was touched, and no test was run.

## Attribution and independence

- Attribution: user-authorized operator, delegated by the account owner.
- Independent review: NOT_ASSIGNED. No APPROVE, acceptance or natural-person signature is
  represented by this file or by the PR.
- The session that wrote these files is the session that describes them; that is disclosure,
  not independence.
