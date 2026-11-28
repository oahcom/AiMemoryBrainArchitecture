# Evidence — AID-2026-342

## 1. Baseline and affected findings

The supplied pre-change repository state is based on `main` commit `3da2e32cf`.

Affected documents:

- `docs/en/03-memory-brain/memory-brain-guide.md`
- `docs/zh-CN/03-memory-brain/memory-brain-guide.md`

Both files have no front matter. Each contains a source-revision record on line 6 that refers to D-branch session `session-d-memory-brain-2026-11-16`, rather than a 40-character blob SHA.

The two scanner findings are:

```text
NON_BLOB_REFERENCE: docs/en/03-memory-brain/memory-brain-guide.md:6
  Source revision references D branch session-d-memory-brain-2026-11-16

NON_BLOB_REFERENCE: docs/zh-CN/03-memory-brain/memory-brain-guide.md:6
  Source revision references D branch session-d-memory-brain-2026-11-16
```

The exact original scanner stdout was not included in the supplied task facts. The entries above identify the two reported findings by type, path, line, and referenced D-branch session.

## 2. Adjudicated source and required pointer value

The adjudicated source is:

- Path: `03-memory-brain/memory-brain-overview.md`
- Blob SHA: `b991f61e412d5cf21824e3ca43b315c3af5f0b4b`

Each mirror's source-revision record must use this 40-character SHA and remain paired, in document order, with its corresponding `- Source: [..](link)` record. The linked file's resolved blob must equal the recorded SHA.

The D-branch session remains historical provenance. It is not the current source-revision pointer target.

## 3. Canonical document and DM-12 relationship closure

The required root-level canonical document is:

`03-memory-brain/memory-brain-guide.md`

Its required relationship metadata is:

- `canonical_status: Canonical`
- `source: null`
- `en` points to `docs/en/03-memory-brain/memory-brain-guide.md`
- `zh-CN` points to `docs/zh-CN/03-memory-brain/memory-brain-guide.md`

The canonical document uses the English mirror body. Both mirrors receive GOV-DOC-002-compliant `document_metadata`; each mirror's `bilingual_counterpart.source` points to the root-level canonical document, and each mirror points to the other language mirror.

This establishes the intended DM-12 canonical/mirror relationship group. Closure is to be confirmed by the actual document-management checker output after the edits.

## 4. Baseline ratchet change

`scripts/ci/baselines/source-revision-pointers.txt` held exactly two entries, both the `NON_BLOB_REFERENCE` records repaired here. Because a baseline with nothing left in it is the exemption the ratchet rules forbid, the file is deleted and the ratchet step in `.github/workflows/repository-hygiene.yml` becomes a direct hard gate: `python3 scripts/check_source_revision_pointers.py`. No other entry existed to preserve.

## 5. Previously observed local validation state

The following results were supplied for the pre-change state at `3da2e32cf`:

| Check | Observed result | Interpretation |
|---|---|---|
| `python scripts/check_source_revision_pointers.py` | `POINTERS=52 ACCURATE=28 STALE=0 BAD=2` | The two known findings remain in the pre-change state. |
| `python scripts/check_document_management.py` | Exit 2, `INCOMPLETE` | 368 documents remain unclassified; this was reported as the same state as the existing baseline. |
| Manifest schema ratchet | `new regressions: 0` | The pre-change manifest schema state introduces no new regressions. |

These are pre-change observations. They are not post-repair validation results.

## 6. Post-repair validation commands and expected results

Run the following commands on the completed worktree and record their actual stdout and exit codes.

### Source revision pointer scanner

Command:

```powershell
python scripts/check_source_revision_pointers.py
```

Expected repaired result:

- Neither memory-brain-guide mirror produces a `NON_BLOB_REFERENCE` finding.
- `BAD=0`.

The scanner's `POINTERS` and `ACCURATE` totals must be copied from the actual run rather than predicted here.

### Document management checker

Command:

```powershell
python scripts/check_document_management.py
```

Expected repaired result:

- No DM-01 or DM-12 errors for the root canonical document and its two mirrors.
- Any remaining unrelated `INCOMPLETE` classification count is reported separately.
- An overall exit code of 2 caused by unrelated unclassified documents must not be described as a fully successful classification run.

### Work Item manifest schema ratchet

Command:

```powershell
python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json
```

Expected result:

```text
Legacy ratchet new regressions: 0
```

Expected exit code: `0`.

## 7. Post-repair result record

All commands were run on the repaired worktree in Windows PowerShell with `PYTHONUTF8=1`.

### Source revision pointer scanner

```text
POINTERS=54
ACCURATE=30
STALE=0
UNRESOLVED=0
DEREFERENCED=24
BAD_DEREFERENCE=0
NON_BLOB_REFERENCE=0
BAD=0
```

Exit code: `0`

The two new accurate pointers are the corrected memory-brain-guide records; the previously repaired 28 remain accurate and no STALE, UNRESOLVED or NON_BLOB_REFERENCE finding is left.

### Document management checker

```text
GOV-DOC-002: 1213 governed documents, 845 classified, 368 unclassified
DM-15 steward adoption baseline: 543 classified document(s) missing steward
DM-10 out-of-scope stale bindings: 0
```

Exit code: `2` (INCOMPLETE: 368 unrelated unclassified documents). No `DM-01`, `DM-07`, `DM-10`, `DM-12` or `DM-15` error line was emitted for the canonical document or either mirror.

### Work Item manifest schema ratchet

```text
Legacy ratchet new regressions: 0
```

Exit code: `0`

## 8. Acceptance status

The pre-change evidence establishes two reported `NON_BLOB_REFERENCE` findings and the current adjudicated source SHA. It does not establish that the repair has been applied.

AID-2026-342 remains in progress until:

1. The root-level canonical document and both classified mirrors have the required DM-12 relationships.
2. Both source-revision records resolve to the adjudicated blob SHA through their corresponding Source links.
3. Exactly the two repaired findings have been removed from the source-revision baseline, with unrelated entries preserved.
4. The pointer scanner reports `BAD=0`.
5. The document-management checker reports no DM-01/DM-12 errors for the three-document group.
6. The manifest-schema ratchet reports zero new regressions with exit code 0.
