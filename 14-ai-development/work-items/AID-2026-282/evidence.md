# AID-2026-282 — Implementation Evidence

## 1. Scope and source baseline

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Owning issue: [#1268](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1268)
- Branch: `fix/2026-11-27-aid282-symlink-false-pass`
- Commit: `e0c8a5ec`
- Base branch: `main`
- Base commit: `6f597e2dd8b6e879bf7539aa16b88a39504d9c49`
- The target test file was verified to have zero content differences between
  the previously referenced `a588cd99` and the actual base `6f597e2d`.
- Diff: `1 file changed, 48 insertions(+), 30 deletions(-)`
- Only changed implementation file:
  `scripts/test_check_document_management.py`

The production checker `scripts/check_document_management.py` was not modified.

## 2. Defect evidence — pre-change source

The following are the exact pre-change source locations at base
`6f597e2dd8b6e879bf7539aa16b88a39504d9c49`.

### T36 — directory symlink

Source lines 2870–2875:

```python
        try:
            link.symlink_to(Path(outside), target_is_directory=True)
        except (OSError, NotImplementedError):
            record("T36 directory symlink is rejected as a governed root", True,
                   "  (symlinks unavailable on this platform; skipped)")
            return
```

The unavailable operation was recorded as a passing result. The `return`
also terminated `run_symlink_boundary()`, suppressing all later cases in
that function, including T37 and the T41/T42 cases.

### T41 — symlinked governed file

Source lines 2903–2908:

```python
            try:
                target.symlink_to(victim)
            except (OSError, NotImplementedError):
                record("T41 symlinked governed file is rejected", True,
                       "  (symlinks unavailable; skipped)")
                return
```

The unavailable operation was recorded as a pass, and the `return` suppressed
subsequent cases in the function.

### T42 — governed file through symlinked parent

Source lines 2925–2930:

```python
        try:
            parent.symlink_to(victim_dir, target_is_directory=True)
        except (OSError, NotImplementedError):
            record("T42 governed file reached through a symlinked parent is rejected",
                   True, "  (symlinks unavailable; skipped)")
            return
```

The unavailable operation was recorded as a pass, and the `return` suppressed
subsequent cases in the function.

These three sites contradicted the existing `skip()` contract: a case that
could not execute must not append `True` to `RESULTS`.

## 3. Repair summary — four bounded replacements

| Replacement | OLD behavior | NEW behavior |
|---|---|---|
| 1. `ALLOWED_SKIPS` | Only T68c had a registered skip reason. | Register T36, T37, T41 and T42, each with the exact reason `symlink creation is unavailable on this platform`. |
| 2. T36/T37 | T36 recorded `True` on symlink failure and returned, suppressing later cases. | T36 uses `skip()`. T37 runs only when T36's link exists; otherwise T37 receives its own registered `skip()`. No early return. |
| 3. T41 | A failed `symlink_to()` recorded `True` and returned. | Track whether all required links were created. Run the assertion only when setup succeeds; otherwise call the registered `skip()`. |
| 4. T42 | A failed parent-link creation recorded `True` and returned. | Call `skip()` on setup failure; otherwise execute the existing assertion in the `else` branch. |

### Replacement 1 — registered skip boundary

OLD:

```python
ALLOWED_SKIPS = {
    "T68c a real 0o000 directory is reported by path (integration)":
        "running as root: mode bits cannot deny access",
}
```

NEW: retain T68c and add exact entries for T36, T37, T41 and T42. All four
new entries use the reason:

```python
"symlink creation is unavailable on this platform"
```

### Replacement 2 — T36/T37 dependency

OLD: one `except` branch called `record(..., True, ...)` and returned; T37
was then unconditionally below the setup block.

NEW mechanism:

```python
link_created = True
try:
    link.symlink_to(Path(outside), target_is_directory=True)
except (OSError, NotImplementedError):
    link_created = False
    skip("T36 directory symlink is rejected as a governed root",
         "symlink creation is unavailable on this platform")

if link_created:
    # Run the T36 assertion and the T37 governed_files assertion.
    ...
else:
    skip("T37 governed_files does not descend into a symlinked root",
         "symlink creation is unavailable on this platform")
```

### Replacement 3 — T41

OLD: failed setup called `record(..., True, ...)` and returned from the
entire function.

NEW mechanism:

```python
links_created = True
for rel in gate.GOVERNED_FILES:
    ...
    except (OSError, NotImplementedError):
        links_created = False
        break

if links_created:
    # Run the existing T41 assertion.
    ...
else:
    skip("T41 symlinked governed file is rejected",
         "symlink creation is unavailable on this platform")
```

### Replacement 4 — T42

OLD: failed setup called `record(..., True, ...)` and returned from the
entire function.

NEW mechanism:

```python
except (OSError, NotImplementedError):
    skip("T42 governed file reached through a symlinked parent is rejected",
         "symlink creation is unavailable on this platform")
else:
    # Run the existing T42 assertion.
    ...
```

## 4. Verification evidence

All figures below are the execution party's reported measurements for this
branch and commit. No unmeasured counterfactual totals are asserted.

| Environment | Relevant output | Exit code |
|---|---|---:|
| Symlink creation available (local and CI-equivalent semantics) | `371/371 passed` | 0 |
| Symlink creation available (skip accounting) | `1 skipped, 1 registered of 5 allowed` | 0 |
| Symlink creation unavailable; `Path.symlink_to` injected to raise `OSError(1314, ...)` | `367/367 passed` | 0 |
| Symlink creation unavailable (skip accounting) | `5 skipped, 5 registered of 5 allowed` | 0 |
| Line-ending check | `1765 files, 0 violations` | 0 |

The unavailable-symlink run produced four new skip entries:
T36, T37, T41 and T42. T68c remained the existing fifth registered skip.

The injection script was kept outside the repository at:

`C:\tmp\opencode\inject_symlink.py`

No formal test case was added for the injection harness, and no injection
script or other harness residue was left in the repository.

## 5. Reverse evidence — T36 failure does not suppress T37 or later cases

The new T36/T37 control flow has two explicit branches:

```python
if link_created:
    ...
else:
    skip("T37 governed_files does not descend into a symlinked root",
         "symlink creation is unavailable on this platform")
```

The T36 exception branch calls `skip()` and sets `link_created = False`;
it does not return.

Consequently, T37 is independently recorded as skipped when its required
directory symlink cannot be created. Control then continues after the
T36/T37 block, allowing T41, T42 and the remaining cases in
`run_symlink_boundary()` to execute or record their own skip outcomes.

The injected-failure measurement corroborates this mechanism: all four
affected cases appear as skips, and the run exits 0 with all five skips
registered.

## 6. Count invariance

The symlink-available result remains `371/371 passed` before and after the
patch because the successful setup path still executes the same existing
T36, T37, T41 and T42 assertions through `record()`.

The patch changes only the unavailable-setup branches:

- When symlink creation succeeds, the original assertion records remain
  executed and counted.
- When symlink creation fails, the affected case is now a skip and is not
  appended to `RESULTS`.
- T37 receives its own skip when T36's setup prerequisite cannot be created.
- The removed early returns no longer suppress independent later cases.

Thus the CI-equivalent successful path retains its original 371 recorded
results. The injected-failure path correctly reports 367 executed results
and five registered skips rather than treating unavailable cases as passes
or silently dropping later cases.

## 7. Explicit non-scope

This change does not touch `scripts/check_document_management.py`.

This change does not touch the AID-2026-079 manifest's historical `318/319`
numbers. That metric reconciliation is owned by issue #1269.

No claim is made that this patch updates or resolves AID-2026-079's
acceptance measurements.

## 8. Prompt and session provenance

- Issue reference: #1268
- Implementing session: `chatgpt-session-ops`
- Account identifier: `acct3`
- Session ID: `6b090a3d-57a0-83ec-9060-eca41f4e6178`
- Prompt ID: `AID-2026-282-PROMPT`

| Prompt version | File | UTF-8 bytes | SHA-256 | Purpose |
|---|---|---:|---|---|
| v1 | `prompt-1268.md` | 5456 | `ebb1233cc7b133b836d2aff9512b295f3dbfd98e298b8b6d3659c379f66bd4e9` | Implementation patch |
| v2 | `prompt-1268-r2.md` | 3151 | `ccf0cd7bf14eee1b411480a746d34e6fb9261a17f166d00f27b3a97a766f74b6` | Anchor-based replacements after the unappliable hunk |
| v3 | `prompt-1268-r3.md` | 4315 | `631437902fbe2d5cd95a2f70a945e78646d3573791777862e66973b90e3be211` | Delivery record requirements and evidence |

The byte counts are UTF-8 raw file byte counts in decimal bytes.
The SHA-256 values identify the actual delivered prompt files.
