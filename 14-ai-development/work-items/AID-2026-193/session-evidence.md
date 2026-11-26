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
        - "14-ai-development/work-items/AID-2026-193/evidence.md"
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
      - "front-matter"
      - "bilingual-mirror"
      - "dm-12"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---
# AID-2026-193 session evidence

## Session role / use case

Implementation session. A delegated coding agent working inside the worktree
`D:\code\wt-corpus-a` on branch `fix/2026-11-27-mirror-frontmatter-a` executed
the assigned unit: add GOV-DOC-002 front-matter to the mirror documents of four
directories that carry none, without editing body prose. Use case: clear a
classification backlog the governance policy counts as unreviewed content, while
keeping the DM-01..DM-14 gate green.

## Actual AI input

The dispatch, verbatim in substance (full scope snapshot in `prompt-v1.md`):

- read `fix-brief-common.md` and `unit-corpus-a.md`, execute end to end, do not
  ask questions;
- work only in `D:\code\wt-corpus-a` on `fix/2026-11-27-mirror-frontmatter-a`;
- insert front-matter only, prove `git diff --numstat` deleted lines = 0;
- `domain` from the directory, `role` by content, `canonical_status:
  Non-Canonical`, `normative_status` inherited from the canonical, and when the
  canonical has no front-matter use `Informative` and say why;
- orphans get nothing and are listed;
- record pre/post blob and added bytes per file;
- run `check_document_management.py` incrementally and over the whole tree and
  record governed / classified / unclassified;
- do not change any body text, any other directory, or the canonical side; do
  not create files.

The agent then read the repository itself rather than assuming: the schema
(`00-governance/architecture-document-metadata.schema.yaml`), the gate
(`scripts/check_document_management.py`), the bilingual gate, the two CI
workflows that run them, `.gitattributes`, and `defects-corpus.md`.

## AI-visible output

Recorded, with the numbers the agent measured:

1. The unit is not executable as dispatched. DM-12 requires a mirror's source to
   be an already classified governed document; 170/170 classified mirrors have a
   classified source, and a probe on `docs/en/02-domain-model/core-entities.md`
   at the base commit produced `FAIL: 3 error(s)` with the three DM-12 messages
   quoted in `evidence.md` section 3. Classifying mirrors alone is a red gate.
2. Therefore 63 files were classified instead of 42: the 21 canonical roots and
   their 42 mirrors. `git diff --numstat` total: 63 files, 2473 added lines, 16
   deleted lines, the 16 being the `Source revision` / `源版本` pins of the eight
   pairs that pin their canonical blob (DEF-corpus-08 requires the pin to move
   with the blob).
3. GOV-DOC-002: governed 942 -> 942, classified 496 -> 559, unclassified 446 ->
   383; incremental verdict `PASS (incremental): no GOV-DOC-002 violations`;
   whole tree `INCOMPLETE` with `no rule violations`.
4. Bilingual gate: `77 frozen, 0 new gaps`, `PASS (63 changed paths inspected)`.
   Pointer gate: `STALE=8` before and after, no new stale pin.
5. Nine rels (18 files) are orphan mirrors and were left unclassified, matching
   `defects-corpus.md` section 5.

What the agent did not do: no body prose edited, no file created or deleted in
the corpus, no authority claimed (`canonical_status: Non-Canonical` everywhere,
no `canonical_scope_id`), no approval recorded, no checker, schema, baseline,
workflow or required context changed, no Issue closed.
