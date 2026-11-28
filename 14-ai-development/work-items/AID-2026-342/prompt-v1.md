# AID-2026-342 — Resolve non-blob source-revision references in bilingual memory-brain guide mirrors

## Authorization and execution boundary

Repository: `oahcom/AiMemoryBrainArchitecture`

Work Item: `AID-2026-342`

Branch: `fix/2026-11-28-aid342-nonblob-guide-pointers`

Base branch: `main`

Base commit: `3da2e32cf`

Date: 2026-11-28

This task is authorized as a bounded documentation-management and CI-baseline repair. Implement only the scope below. Do not modify unrelated source pointers, document pairs, or historical provenance.

## Established facts

1. The affected files are:
   - `docs/en/03-memory-brain/memory-brain-guide.md`
   - `docs/zh-CN/03-memory-brain/memory-brain-guide.md`

2. Neither mirror currently has front matter. Both are therefore unclassified. Their line 6 source-revision records refer to the D-branch session `session-d-memory-brain-2026-11-16`, and the source-revision pointer scanner reports two `NON_BLOB_REFERENCE` findings.

3. The scanner is `scripts/check_source_revision_pointers.py`. Its relevant rules are:
   - A source-revision record must contain a 40-character Git blob SHA.
   - Revision records are paired in document order with the corresponding `- Source: [..](link)` records.
   - The file resolved from each Source link must have the same blob SHA as the paired revision record.

4. The adjudicated canonical source is:
   - Path: `03-memory-brain/memory-brain-overview.md`
   - Blob SHA: `b991f61e412d5cf21824e3ca43b315c3af5f0b4b`

5. The two mirrors must receive GOV-DOC-002-compliant `document_metadata` when modified.

6. DM-12 requires each mirror's `bilingual_counterpart.source` to point to a classified root-level canonical document. No root-level `03-memory-brain/memory-brain-guide.md` currently exists. This task must create that root-level canonical document.

7. The new root-level canonical document must:
   - Use the English mirror body as its document body.
   - Have `canonical_status: Canonical`.
   - Have `source: null`.
   - Declare its `en` and `zh-CN` counterparts as the two mirror paths.
   - Include the required `document_metadata`.

8. The two mirrors must:
   - Include the required `document_metadata`.
   - Set `bilingual_counterpart.source` to the new root-level canonical document.
   - Point to each other as bilingual counterparts.
   - Retain their respective language identity and mirror content.
   - Replace the D-branch session source-revision record with the adjudicated 40-character blob SHA, while preserving the scanner's ordered pairing with the relevant Source link.

9. `scripts/ci/baselines/source-revision-pointers.txt` currently holds the only two remaining entries, both `NON_BLOB_REFERENCE` records for these mirrors. The ratchet rules forbid keeping a baseline with nothing left in it, so this repair deletes the file and retires the wrapped gate to a hard gate in `.github/workflows/repository-hygiene.yml`.

## Required changes

1. Create the root-level canonical document:
   `03-memory-brain/memory-brain-guide.md`

2. Use the English mirror's current body as the canonical document body. Add the required front matter and metadata. Do not silently rewrite or expand the technical content.

3. Add GOV-DOC-002-compliant `document_metadata` to both mirrors. Establish the complete DM-12 relationship:
   - Canonical document: `canonical_status: Canonical`, `source: null`, and `en` / `zh-CN` references to the two mirrors.
   - English mirror: `bilingual_counterpart.source` points to the canonical document and its counterpart points to the Chinese mirror.
   - Chinese mirror: `bilingual_counterpart.source` points to the canonical document and its counterpart points to the English mirror.

4. Correct the source-revision record in each mirror to:
   `b991f61e412d5cf21824e3ca43b315c3af5f0b4b`
   The SHA identifies the adjudicated canonical source `03-memory-brain/memory-brain-overview.md`. Preserve the scanner's required order and pairing with each document's Source link. Do not point the revision record at the new memory-brain-guide canonical document; the adjudicated source for this revision record is the overview document.

5. Delete `scripts/ci/baselines/source-revision-pointers.txt` and replace the ratchet step in `.github/workflows/repository-hygiene.yml` with a direct hard gate (`python3 scripts/check_source_revision_pointers.py`). The baseline exists only for the two entries repaired here; an empty baseline is the exemption the ratchet rules forbid.

6. Update the AID-2026-342 work-item records:
   - `manifest.yaml`
   - `prompt-v1.md`
   - `session-evidence.md`
   - `evidence.md`

## Validation requirements

Run the following checks on the completed worktree and record their actual output and exit status:

1. `python scripts/check_source_revision_pointers.py`
   - Expected repaired state: no `NON_BLOB_REFERENCE` findings for either mirror and `BAD=0`.

2. `python scripts/check_document_management.py`
   - Expected repaired state: no DM-01 or DM-12 errors for the canonical document and its two mirrors.
   - Record any unrelated INCOMPLETE classification count separately; do not misrepresent an overall INCOMPLETE exit as a successful complete classification run.

3. `python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json`
   - Expected: `Legacy ratchet new regressions: 0`, exit code 0.

Do not claim any validation passed until its actual output and exit status have been observed. Preserve the distinction between:
- previously observed baseline results,
- expected post-repair results,
- and actual post-repair execution results.

## Acceptance criteria

- The root-level canonical document exists and is classified.
- Both mirrors are classified and have valid DM-12 references to the canonical document and to each other.
- Both mirror source-revision records use the adjudicated 40-character blob SHA and remain correctly paired with their Source links.
- The two repaired findings no longer exist, the pointer baseline file is deleted, and the pointer check runs as a hard gate.
- The pointer scanner reports `BAD=0`.
- The document-management checker reports no DM-01/DM-12 errors for the three-document relationship group.
- The manifest-schema ratchet reports zero new regressions.

Do not claim that the task is complete until the acceptance criteria are supported by recorded results.
