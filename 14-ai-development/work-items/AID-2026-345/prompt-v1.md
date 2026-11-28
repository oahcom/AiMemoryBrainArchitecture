# AID-2026-345 — Correct the manifest pin ledger rebase anchor

## Task

Repair the `Repository hygiene (hard gate)` failure on `main` caused by the two existing records in `scripts/ci/manifest-pin-ledger.md` referring to a repin commit that is not an ancestor of the current `main` history.

Repository: `oahcom/AiMemoryBrainArchitecture`

Authorized base commit:

`f0843a8f38a420883921cfda96b515204967f885`

Tracking issue: `#1350`

## Observed defect

The two existing ledger records for AID-2026-101 and AID-2026-102 use:

`6045af65fcc2e89d1895e09ed666af4d737203bf`

That commit exists only in the pre-squash branch history and is not an ancestor of the current `main` target. The manifest pin checker therefore reports an `INCOMPLETE` ledger condition.

The authorized replacement anchor is:

`2ab66153dbcdd8a8f2d68d234914751a748a8f74`

This is the single-parent squash commit from PR #1512. Its first parent contains the two original `4470` declarations, and the squash commit contains the corresponding `4412` declarations.

## Required changes

1. In `scripts/ci/manifest-pin-ledger.md`, change only the `repin_commit` cell in each of the two existing records:
   - AID-2026-101: replace `6045af65fcc2e89d1895e09ed666af4d737203bf` with `2ab66153dbcdd8a8f2d68d234914751a748a8f74`.
   - AID-2026-102: make the same replacement.
2. Preserve every other existing table cell exactly.
3. Append a short `## Rebase correction` section explaining why the ledger anchor now identifies the squash commit on `main` rather than the pre-squash branch commit. State that this corrects the historical commit reference without changing the meaning of either recorded pin transition.
4. Add the AID-2026-345 work-item records and append one row to `14-ai-development/work-items/INDEX.md`.
5. Do not modify the manifest blob-pin checker, the baseline, any other work-item manifest, or any other work-item directory.

## Authorization boundary

This is a narrow correction to the Git commit identity used to prove two already-recorded transitions. It does not authorize changing either transition's manifest, field, path, `previous_pin`, or `new_pin`.

The two records must continue to mean:

- AID-2026-101: `4470` → `4412`
- AID-2026-102: `4470` → `4412`

The replacement commit must prove both transitions through its first-parent diff. Do not add a new ledger record, remove a record, reorder records, or change the baseline.

## Acceptance criteria

The correction is acceptable only if all of the following hold:

1. Both ledger rows name `2ab66153dbcdd8a8f2d68d234914751a748a8f74`.
2. The replacement commit's first parent has `4470` for both declared paths.
3. The replacement commit has `4412` for both declared paths.
4. The replacement commit is an ancestor of the target `main` commit.
5. Each row still identifies exactly one manifest pin.
6. The target tree's two pin values equal the corresponding latest `new_pin` values.
7. The two intentional AID-2026-261 `PATH_MISSING` sentinel lines remain unchanged in `scripts/ci/baselines/manifest-blob-pins.txt`.
8. The candidate checker result has `mismatch=0`, `path_missing=2`, and `incomplete=0`; the two `PATH_MISSING` lines match the existing baseline exactly, so the ratchet does not introduce a new failure.
9. The existing `Repository hygiene (hard gate)` succeeds on the resulting PR head.
10. The diff contains only the six authorized files: the ledger, the four AID-2026-345 work-item files, and the work-item index.

No acceptance or merge is claimed by this task snapshot.

---
