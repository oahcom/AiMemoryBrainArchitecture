# AID-2026-255 — Negative Fixture Evidence

## Captured test output

The implementing session's regression-test output is captured in `negative-fixtures.log`.

```text
Ran 9 tests ... OK
```

Command:

```text
python scripts/ci/test_check_manifest_blob_pins.py -v
```

Observed result: 9 tests, all `ok`; exit code 0.

## What the nine tests establish

1. **Main-equivalent 12-item mismatch fixture** — a fixture containing the complete authorized set produces exactly 12 checker failure items when all 12 declared blob IDs mismatch their referenced fixture blobs.
2. **Out-of-scope prompt digest ignored** — a mismatching `prompt_sha256` declaration does not create an additional checker finding.
3. **Out-of-scope path-only entry ignored** — a `scope.changes[].path` entry without a digest is not treated as a blob pin and does not create a finding.
4. **Authorized one-byte mutation detected** — changing one byte in a referenced file changes its Git blob ID and causes the corresponding authorized identity to fail.
5. **Deleted referenced path detected** — removing an authorized referenced file produces a missing-path finding for that identity.
6. **Clean fixture succeeds** — when all 12 declared blob IDs match the referenced Git blobs, the checker exits 0.
7. **Missing required manifest fails closed** — removing a required manifest produces exit code 2 and the missing-manifest diagnostic.
8. **Authorization table is exact** — the test asserts that the checker authorization table contains exactly the 12 authorized identities, with no additions.
9. **Single missing path is isolated** — a missing referenced path affects its own authorized identity and does not generate failures for the other correctly pinned identities.

## Captured artifact

`negative-fixtures.log` is the captured output artifact for the regression run. The observed summary is `Ran 9 tests ... OK`, with exit code 0. The detailed test log is retained in the work-item directory.
