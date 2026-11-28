# AID-2026-348 — Evidence

## Purpose

This work item records the historical adjudication of manifest blob-pin baseline diagnostics and the later scratch-rebase state of PR #1531.

It does not resolve the pending historical diagnostics, close the two defect records, change checker behavior, or claim that the latest scratch rebase has passed all gates.

## Frozen task input

- Source: `am-258-final-files.md`
- Bytes: `18702`
- SHA-256: `f03e73c62d880b419b1f98a0a8bf36942fe0d0703b987cf268f8c16b1e34f5bf`
- Snapshot: `14-ai-development/work-items/AID-2026-348/prompt-v1.md`

The byte count and digest are coordinator-supplied facts and must be checked against the copied snapshot before merge.

## Historical adjudication anchor

- Commit: `daa935f7a7ecc808f1775be8cf153cf715961b08`
- Original record commit: `4de0e74e5bcf3d0696353236295de37d86f9c721`
- Original record commit parent: `daa935f7a7ecc808f1775be8cf153cf715961b08`

The historical disposition was:

| Disposition | Count |
|---|---:|
| Superseded by current manifest values | 11 |
| Duplicate old-format entries | 2 |
| Transferred to standalone defect records | 6 |
| Retained in pending historical review ledger | 18 |
| Active ratchet findings at that historical snapshot | 4 |

These figures describe the historical snapshot only. They must not be rewritten to describe a later main state.

## Four-file package

1. `scripts/ci/baselines/manifest-blob-pins.txt`
2. `scripts/ci/baselines/pending-historical-diagnostics.md`
3. `scripts/ci/defects/DEFECT-1-frontmatter-blob-sha.md`
4. `scripts/ci/defects/DEFECT-2-nested-gate-a-reconstruction.md`

The two defect records remain open. The pending ledger retains 18 diagnostics as pending historical review, not as fixed or resolved.

## PR #1531 history

- PR: #1531
- Original PR head: `71fc753843c2b7684fd6cf50323ff04cd20f1ca0`
- Original PR base at the reported rebase stage: `4bed709ca`
- Latest scratch base: `f0843a8f38a420883921cfda96b515204967f885`
- Scratch rebase commit: `43bde81a60bfe86e96e2f4b9d00c323cee6c5ca1`
- Scratch branch: `scratch/rebase-1531`
- Scratch worktree: `D:\code\wt-scratch-1531`

The scratch commit is not pushed. The remote PR head remains `71fc753843c2b7684fd6cf50323ff04cd20f1ca0`.

## Scratch validation

### Ratchet

- Baseline ref: `f0843a8f38a420883921cfda96b515204967f885`
- Base: 2
- Candidate: 2
- Added: 0
- Removed: 0
- Current: 3
- Regressions: 1
- Remaining fixed: 0

The sole reported regression is the upstream ledger `INCOMPLETE` finding because the ledger's recorded repin commit `6045af65...` is not an ancestor of the target `f0843a8...`.

The ratchet therefore fails. This PR must not describe the scratch validation as green.

### Repository new-file admission

- New paths checked: 3
- Result: PASS
- Exit: 0

### Line endings

- Files inspected: 2113
- Binary files skipped: 0
- Violations: 0
- Exit: 0

These are coordinator-local scratch results, not CI results.

## Current status

- PR #1531 remains open.
- Its remote head remains `71fc753843c2b7684fd6cf50323ff04cd20f1ca0`.
- Its remote body remains unchanged until the new evidence files are added to the PR head.
- Scratch commit `43bde81a60bfe86e96e2f4b9d00c323cee6c5ca1` is not pushed.
- The ratchet remains red due to the upstream ledger `INCOMPLETE` finding.
- No CI success, independent review, Owner acceptance, or merge is asserted.
