# AID-2026-290 — Prompt Snapshot

## Identity

- Work Item: AID-2026-290
- Repository: oahcom/AiMemoryBrainArchitecture
- Owning Issue: #1268
- Role: L1 coordinator + L2 implementation session
- Date: 2026-11-26

## Objective

Fix symlink boundary test accounting in:

scripts/test_check_document_management.py

## Required behavior

Four cases are affected:

- T36 directory symlink is rejected as a governed root
- T37 governed_files does not descend into a symlinked root
- T41 symlinked governed file is rejected
- T42 governed file reached through a symlinked parent is rejected

When symlink creation is unavailable:

1. Each case must call skip() exactly once.
2. Each case must not call record().
3. Each case must use the exact existing registered reason:
   symlink creation unavailable on this platform
4. No case may silently disappear.
5. T36 failure must not suppress T37, T41 or T42.
6. T41 failure must not suppress T42.

When symlink creation is available:

1. All four original assertions must execute.
2. Each case must produce exactly one record().
3. The normal test count must remain unchanged.

## Implementation constraints

- Reuse ALLOWED_SKIPS, skip(), RESULTS and RESULTS_BY_NAME.
- Do not modify the four existing skip registration names or reasons.
- Do not change check_document_management.py.
- Do not modify T68c.
- Do not modify Issue #1269.
- Do not introduce dependencies.
- Do not rewrite unrelated tests.

## Initial implementation regression

The first skip conversion called skip() but continued into record().
Real execution demonstrated that all four cases appeared in both
SKIPPED and RESULTS_BY_NAME.

The corrected implementation must use mutually exclusive
success/failure branches.

## Required verification

Normal path:

python scripts/test_check_document_management.py

Forced unavailable path:

python verify_symlink_unavailable.py

The forced path must establish:

- SKIPPED contains exactly T36, T37, T41, T42.
- UNEXPECTED_SKIPS is empty.
- None of those four names occurs in RESULTS_BY_NAME.
- No skipped case is counted as passed or failed.

Negative controls:

- A mismatched reason must produce UNEXPECTED_SKIPS.
- A mismatched name must produce UNEXPECTED_SKIPS.

## Evidence discipline

The initial implementation's real failure output must be retained
verbatim in evidence.md.

The corrected implementation must not be described as passing
until both verification commands have actually been executed.

Prompt hash and byte count are supplied by the mechanical
registration operator after saving the final prompt snapshot.
