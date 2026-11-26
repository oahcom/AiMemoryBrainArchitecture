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
        - "14-ai-development/work-items/AID-2026-200/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Records the dispatched task scope, not a full raw transcript; the session identifier and the verbatim model input stream were not captured."
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
# AID-2026-200 - executed prompt snapshot (scope, not a transcript)

Dispatch received by the implementation session: read
`.superpowers/sdd/2026-11-26-chatgpt-session-ops-skill/fix-brief-common.md` and
`unit-corpus-a.md`, then execute end to end in the worktree
`D:\code\wt-corpus-a` on branch `fix/2026-11-27-mirror-frontmatter-a`, without
asking questions.

The unit scope, verbatim in substance:

1. Enumerate both mirrors of `00-governance`, `01-system-architecture`,
   `02-domain-model`, `06-memory-context` and decide, file by file, whether the
   first line is `---`.
2. For every file without front-matter, insert the GOV-DOC-002 block at the top
   only; the body must not change, proved with `git diff --numstat` (added lines
   equal the front-matter line count, deleted lines are zero).
3. Fields: `domain` from the directory; `role` by content
   (`spec` / `index` / `review-record`); `canonical_status: Non-Canonical`;
   `normative_status` inherited from the canonical (when the canonical has no
   front-matter, use `Informative` and say why); `bilingual_counterpart` correct
   in all three directions.
4. Orphan mirrors (no canonical) get no front-matter and are listed as
   `ORPHAN_SKIPPED`.
5. Record, per file, the pre-insertion blob, the post-insertion blob and the
   bytes added.
6. Run `check_document_management.py` incrementally and over the whole tree and
   record governed / classified / unclassified.
7. Do not change any body text, any other directory, or the canonical side; do
   not create files.

The common brief additionally requires a work item under
`14-ai-development/work-items/AID-2026-200/` with `manifest.yaml`,
`evidence.md`, `prompt-v1.md` and `session-evidence.md`, bilingual copies of the
evidence, one row appended to `INDEX.md`, a PR body carrying the issue
reference, `AI-assisted work: YES` and a resolvable session-evidence path, and a
merge only after all sixteen required contexts report success.

Deviation recorded, not hidden: the "do not change the canonical side"
constraint cannot be satisfied together with DM-12, because DM-12 requires a
mirror's `bilingual_counterpart.source` to be an already classified governed
document. Evidence section 3 states the measurement and the resulting scope.
