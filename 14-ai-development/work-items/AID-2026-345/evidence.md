# AID-2026-345 Evidence — Manifest Pin Ledger Rebase Correction

## Defect

The `Repository hygiene (hard gate)` check on `main` at:

`f0843a8f38a420883921cfda96b515204967f885`

reported an incomplete manifest pin ledger. Both existing ledger records in `scripts/ci/manifest-pin-ledger.md` referred to:

`6045af65fcc2e89d1895e09ed666af4d737203bf`

That commit is not an ancestor of the current `main` history. It exists only in the branch history preceding squash integration. The checker cannot establish the required ancestry proof for either record.

## Captured CI output

The reported output was:

```text
main=f0843a8f38a420883921cfda96b515204967f885 manifests=167 pins=296 ok=294 mismatch=0 path_missing=2 incomplete=1 unbound=0
PATH_MISSING path=14-ai-development/work-items/AID-2026-261/prompt-v1.md; declared=0000000000000000000000000000000000000000000000000000000000000000
PATH_MISSING path=14-ai-development/work-items/AID-2026-261/prompt-v1.md; declared=0
INCOMPLETE ledger=scripts/ci/manifest-pin-ledger.md: ledger repin commit 6045af65fcc2e89d1895e09ed666af4d737203bf is not an ancestor of target f0843a8f38a420883921cfda96b515204967f885
INCOMPLETE: at least one requested scan could not be completed
##[error]Process completed with exit code 2.
```

The two `PATH_MISSING` entries are the existing intentional AID-2026-261 sentinels. They are not the cause of the incomplete ledger result.

## Relevant checker behavior

The relevant checker is:

`scripts/ci/check_manifest_blob_pins.py`

Its ledger validation establishes, for each record:

1. The manifest, field, and path identify one declared pin.
2. `previous_pin` equals the declaration in the first parent of `repin_commit`.
3. `new_pin` equals the declaration in `repin_commit`.
4. `repin_commit` is a full lowercase commit SHA and an ancestor of the target.
5. The recorded history is continuous and the target pin equals the latest `new_pin`.
6. The recorded transition corresponds to an actual first-parent manifest pin change after the baseline anchor.

The checker distinguishes violations from incomplete evidence. An unresolvable or non-ancestral repin commit is an `INCOMPLETE` condition.

## Authorized replacement anchor

The replacement anchor is:

`2ab66153dbcdd8a8f2d68d234914751a748a8f74`

It is the squash commit from PR #1512 and is a single-parent commit.

The following facts were measured for this candidate:

| Check | Measured result |
|---|---|
| First parent of `2ab66153` | `6c6f8cfe8` |
| AID-2026-101 value at first parent | `4470` |
| AID-2026-102 value at first parent | `4470` |
| AID-2026-101 value at `2ab66153` | `4412` |
| AID-2026-102 value at `2ab66153` | `4412` |
| `2ab66153` is an ancestor of itself | Yes |
| First-parent diff contains both manifest transitions | Yes |

The candidate therefore satisfies the recorded `previous_pin`, `new_pin`, ancestry, continuity, and actual-transition requirements for both rows.

## Reproduction command

The checker can be run against the specified target commit with:

```text
python scripts/ci/check_manifest_blob_pins.py --commit f0843a8f38a420883921cfda96b515204967f885
```

The captured CI output above is the pre-correction result. No post-correction execution result is claimed in this evidence file.

## Expected post-correction classification

After changing only the two `repin_commit` cells to the squash commit, the expected classification is:

- `mismatch=0`
- `path_missing=2`
- `incomplete=0`

The two `PATH_MISSING` lines must remain byte-for-byte equal to the two entries already present in:

`scripts/ci/baselines/manifest-blob-pins.txt`

The candidate checker is expected to return exit code `1` for the two intentional path-missing violations. The workflow's existing ratchet compares the observed violation lines against the committed baseline. The expected outcome is that the exact two existing sentinel lines remain accounted for and no new violation is introduced.

This expected result is an acceptance criterion, not a claim that the corrected tree has already been tested.

## Scope and non-claims

This evidence concerns only the invalid historical commit reference in the two existing ledger rows.

It does not authorize or claim:

- Changes to either manifest pin value.
- Changes to the two ledger records' manifest, field, path, `previous_pin`, or `new_pin`.
- Changes to `scripts/ci/baselines/manifest-blob-pins.txt`.
- Changes to checker logic or workflow behavior.
- Changes to AID-2026-261 or any other work item.
- Successful post-change CI, merge, or Owner acceptance.

---
