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
        - "14-ai-development/work-items/AID-2026-256/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Measurements and edit inventory recorded from Git readback; no CI result or acceptance is asserted."
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
      - "registration-reconciliation"
      - "index-status"
      - "manifest-status"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
  steward: "user-authorized operator (delegated by account owner)"
---

# AID-2026-256 — registration reconciliation evidence

Scope: INDEX status-cell prefix and manifest top-level status only. Every other field untouched.

## INDEX rows changed (19)

| AID | merge PR | status cell (prefix …) |
|---|---|---|
| AID-2026-095 | #1264 | MERGED — id_status: PROVISIONAL; merge-time recheck/renumber required |
| AID-2026-098 | #1283 | MERGED — PR #1283; id_status: PROVISIONAL; AID-2026-097 reserved for E/F mirrors; recheck/ |
| AID-2026-099 | #1275 | MERGED — id_status: PROVISIONAL; merge-time recheck required |
| AID-2026-107 | #1290 | MERGED — PROVISIONAL; 72/72 checkpoints remain NOT EVIDENCED (0 UPGRADED, 72 UNCHANGED, 0  |
| AID-2026-110 | #1304 | MERGED — id_status: PROVISIONAL; canonical path restoration only; no Owner acceptance |
| AID-2026-112 | #1316 | MERGED — PROVISIONAL; 36 SC/HIR predicates: 27 PARTIAL_EVIDENCE, 9 UNCHANGED, 0 PASS; AID- |
| AID-2026-140 | #1324 | MERGED — id_status: PROVISIONAL; original source carrier PR #1314 merged; AID-140 reconcil |
| AID-2026-150 | #1320 | MERGED — `id_status: PROVISIONAL`; PR #1320; exactly three D normative roots restored; 29  |
| AID-2026-170 | #1328 | MERGED — PR #1328; id_status: PROVISIONAL; one pointer cell re-pinned in the EN and ZH-CN  |
| AID-2026-172 | #1327 | MERGED — PR #1327; id_status: PROVISIONAL; baseline-copy comparison inside the existing st |
| AID-2026-173 | #1330 | MERGED — PR #1330 — `id_status: PROVISIONAL`; 56 thresholds: 51 BLOCKING / 2 ADVISORY / 3  |
| AID-2026-189 | #1339 | MERGED - PR #1339; `id_status: PROVISIONAL`; fmt job loses the toolchain probe and the rus |
| AID-2026-190 | #1343 | MERGED — PR #1343; \id_status: PROVISIONAL\; six files gain one appended \## Correction (2 |
| AID-2026-191 | #1345 | MERGED - PR #1345; `id_status: PROVISIONAL`; unqualified invocation now exits 2 with `SKIP |
| AID-2026-193 | #1351 | MERGED — `id_status: PROVISIONAL`; 91 distinct path strings cited, 84 absent from the tree |
| AID-2026-197 | #1348 | MERGED - PR #1348; `id_status: PROVISIONAL`; `NON_BLOB_REFERENCE` now enters BAD (BAD 8 -> |
| AID-2026-199 | #1353 | MERGED - PR #1353; `id_status: PROVISIONAL`; `check_index_membership` raises the file's ex |
| AID-2026-210 | #1357 | MERGED - PR #1357; `id_status: PROVISIONAL`; 6 files gain a metadata block (46/45 insertio |
| AID-2026-240 | #1347 | MERGED — PR #1347; `id_status: PROVISIONAL`; seven carriers measured and given one declare |

## Manifests whose top-level status field was set to MERGED (13)

AID-2026-107, 112, 170, 172, 173, 189, 190, 191, 193, 197, 199, 210, 240.

Manifests with no top-level status field (6, deliberately untouched): AID-2026-095, 098, 099, 110, 140, 150.

## Verification

- python scripts/check_document_management.py --root . → INCOMPLETE: no rule violations in 654 classified documents, but 371 governed documents are still unclassified (the 371 backlog predates this change; exit 1 is the pre-existing INCOMPLETE state).
- git diff --stat → 14 files, 32 insertions / 32 deletions.
- Full before/after text is recoverable from the commit diff; no note text was deleted.
