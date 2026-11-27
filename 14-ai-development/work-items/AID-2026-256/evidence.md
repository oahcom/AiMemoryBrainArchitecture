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

## Post-merge backfill (2026-11-27)

- Carrier PR #1380 merged as `46dac1b1e198c8d88daff5a34faf759ecb075869` at 2026-11-27T05:27:58Z, from exact head `b1c0ab0e` with 17/17 required contexts SUCCESS and `mergeStateStatus=CLEAN`.
- This backfill changes exactly two fields: `implementation.status` DRAFT_PR to MERGED, and `implementation.merge_commit_sha` PENDING to the merge commit above. No other field, file or claim is changed.
- Readback on the base commit of this PR: the AID-2026-256 INDEX row exists exactly once; the 13 manifest top-level `status` fields and the 19 INDEX Status prefixes landed by #1380 all read back as MERGED.
- Residual, deliberately not rewritten here: `registration_status: CARRIER_PR_DRAFT` still names the registration-stage label of the carrier PR; `review.status: NOT_ASSIGNED` and `acceptance.status: NOT_GRANTED` remain, because a merged carrier is not an acceptance.

## Merge-fact correction batch (2026-11-27)

Seven manifests recorded a merge fact that contradicted GitHub. Each is corrected from `GET /pulls/<n>` (`merged=true`, `merge_commit_sha`, `merged_at`) and each keeps a `post_merge_correction` block holding the original value so nothing is silently overwritten.

| AID | field | original | corrected |
| --- | --- | --- | --- |
| AID-2026-079 | `implementation.status` / `merge_commit_sha` | `IMPLEMENTED_IN_BRANCH` / `NOT_MERGED` | `MERGED` / `6314a65bd8be48c1a4bb0768e9960c4c808110ab` (PR #1078) |
| AID-2026-082 | `implementation.status` / `merge_commit_sha` | `IN_PROGRESS` / `NOT_MERGED` | `MERGED` / `71548b7b9d8efae4ee605a0fb4c9d1d97236138c` (PR #1265) |
| AID-2026-250 | `implementation.status` / `merge_commit_sha` | `IN_PROGRESS` / `NOT_MERGED` | `MERGED` / `652aeaaea9cc77db959e6241f65184b4bf21c9c8` (PR #1388) |
| AID-2026-150 | `carrier.merge_commit_sha` | `PENDING` | `6ab36b3697a0994d8de449d2b9c344f23aac0fda` (PR #1320) |
| AID-2026-172 | `carrier.merge_commit_sha` | absent | `1e9341da603dec78377fed240f4d6dbabaa8838e` (PR #1327) |
| AID-2026-204 | `carrier.merge_commit_sha` | absent | `980e54d9b17af04eaaf754f160c3068eb0adc6fa` (PR #1354) |
| AID-2026-116 | `implementation.status` / `merge_commit_sha` | `PR_OPEN` / absent | `MERGED` / `a7cf5256e975ff25fd2f75b3b5051b16d8d77d36` (PR #1321) |

`AID-2026-059` was reported as having no merge SHA, but it records the same fact under `implementation_commit_sha`, which equals the merge commit `ebadbe843eb69e0e3e2db84b4956d9e8e635e5a8`. It is not edited: the key differs, the fact does not.

Top-level `status` is set to `MERGED` only where the key already existed. `AID-2026-150` has no top-level `status` and none is invented, consistent with the rule applied in #1380.
