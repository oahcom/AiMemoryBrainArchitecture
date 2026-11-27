# AID-2026-255 — Exact-Head Verification

## Commit identity

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Base branch: `main`
- Base SHA: `242cf101c8b79007ad2fb8d9c89681224577188d`
- Head SHA: `f1319b32ad23a050f9f6092f10cb26e6478676cc`
- Head short SHA: `f1319b32`
- Working branch name: PENDING — not supplied in the captured evidence.

All command results below are reported for head `f1319b32`.

## Commands and observed results

| Command | Observed output / result | Exit |
|---|---|---:|
| `python scripts/ci/check_manifest_blob_pins.py` | 12 `::error::` lines | 1 |
| `python scripts/ci/gate_ratchet.py --baseline scripts/ci/baselines/manifest-blob-pins.txt --format paths --command "python scripts/ci/check_manifest_blob_pins.py"` | `baseline=12 current=12 regressions=0 fixed=0`; `ratchet: PASS - failure set matches the baseline exactly.` | 0 |
| `python scripts/ci/test_check_manifest_blob_pins.py -v` | 9 tests, all `ok` | 0 |
| `python scripts/ci/check_manifest_parse.py` | `115 manifests found, 115 parsed, 0 failed` | 0 |
| `python scripts/ci/check_repository_hygiene.py --base 242cf101 --head f1319b32` | `directories=125 linked=125`; `violations=0`; new-file admission passed | 0 |
| `python scripts/check_traceability.py` | `00-governance/requirements-registry.yaml` absent; the same file is absent on `main` (pre-existing condition) | 1 |

The checker command's exit 1 is the expected measured result: it emits the 12 currently mismatching authorized pins. The ratchet command confirms that the current failure set matches the unchanged 12-entry baseline exactly.

Captured run artifacts in the work-item directory:

- `negative-mismatch.log`
- `negative-fixtures.log`
- `regression-gates.log`
- `blob-rehash-ledger.tsv`

## Review and CI disposition

**CI: PENDING — 0 check runs recorded on this head at the time of writing.**

GitHub check runs have not been recorded for head `f1319b32ad23a050f9f6092f10cb26e6478676cc`. CI is not claimed green. The API quota is reported exhausted; no retry time or completion time is asserted here.

**Independent review: PENDING.**

No run ID, reviewer identity or acceptance is claimed.
