---
document_metadata:
  steward: USER-PRINCIPAL-DELEGATED
  domain: repository-governance
  role: implementation-evidence
  lifecycle: active
  authority: supporting-evidence
---

# AID-2026-336 Implementation Evidence

## 1. Implementation identity

| Field | Recorded value |
|---|---|
| Work item | AID-2026-336 |
| Repository | `oahcom/AiMemoryBrainArchitecture` |
| Branch | `aid-2026-336` |
| Rebased base | `origin/main` at supplied abbreviated commit `daa935f7a` |
| Implementation commit | `d8512eee5` |
| Parent commit | `daa935f7a` |
| Merge status | `NOT_MERGED` |
| Acceptance status | `PENDING` |

The implementation commit is recorded using the abbreviated identifier supplied
with the measured implementation results. No full object ID is inferred here.

## 2. Changed implementation files

The implementation changed the following seven existing files:

1. `scripts/ci/check_manifest_blob_pins.py`
2. `scripts/ci/test_check_manifest_blob_pins.py`
3. `scripts/ci/baselines/manifest-blob-pins.txt`
4. `scripts/ci/assert_manifest_blob_pin_negative.py`
5. `scripts/ci/test_assert_manifest_blob_pin_negative.py`
6. `.github/workflows/repository-hygiene.yml`
7. `14-ai-development/work-items/AID-2026-100/manifest.yaml`

The checker was rebased onto the supplied `origin/main` baseline while retaining
the `blob_sha256` scan. The repository-hygiene ratchet filter was extended to
include the three semantic diagnostic prefixes:

- `HISTORICAL_REFERENCE_NOT_FOUND`
- `CURRENT_REFERENCE_MISMATCH`
- `REFERENCE_MODE_MISSING_OR_INVALID`

The AID-2026-100 migration adds
`reference_mode: historical` to `related_evidence[0]`. Its existing digest was
not rewritten.

## 3. Checker result at the implementation commit

Command:

```bash
python scripts/ci/check_manifest_blob_pins.py --commit HEAD
```

Measured result:

```text
rc=0
main=d8512eee59e8bfdfec5e280e4a3a01fc62c61074 manifests=161 pins=12 ok=12 mismatch=0 path_missing=0 incomplete=0 excluded=163 unbound=0
```

The measured `pins=12` consists of:

- 10 AID-336 in-scope pins under the historical/current Git-blob reference
  semantics;
- 2 bound `blob_sha256` declarations.

The `excluded=163` value is the checker's runtime exclusion counter. It is not
the same measure as the manifest-visible declaration inventory or the
prompt-metadata inventory documented in `pincount.md`.

## 4. Test results

### 4.1 Checker tests

Command:

```bash
python scripts/ci/test_check_manifest_blob_pins.py
```

Measured result:

```text
Ran 35 tests ... OK
```

### 4.2 Negative assertion tests

Command:

```bash
python scripts/ci/test_assert_manifest_blob_pin_negative.py
```

Measured result:

```text
7 tests ... OK
```

### 4.3 Combined base resolver and negative assertion tests

Command:

```bash
python -m unittest scripts/ci/test_resolve_manifest_blob_pin_base.py scripts/ci/test_assert_manifest_blob_pin_negative.py
```

Measured result:

```text
15 tests ... OK
```

## 5. Fixed negative fixture

Command:

```bash
python scripts/ci/assert_manifest_blob_pin_negative.py --commit 9a2063ae1fa5d905b3817cd4eddba065a06daa73
```

Measured result:

```text
NEGATIVE_ASSERTION_PASS
main=9a2063ae1fa5d905b3817cd4eddba065a06daa73 manifests=108 pins=14 ok=7 mismatch=1 path_missing=0 incomplete=0 excluded=146 unbound=4
```

The measured findings included:

- 4 `UNBOUND_BLOB_SHA256` findings;
- 1 `REFERENCE_MODE_MISSING_OR_INVALID` finding;
- 0 `MISMATCH ` findings;
- 0 `PATH_MISSING ` findings;
- 0 `INCOMPLETE ` findings.

The missing/invalid `reference_mode` is classified as a policy violation,
contributing to the violation result rather than making the scan incomplete.
The four unbound SHA-256 declarations remain explicit violations.

## 6. Manifest validation

### 6.1 Manifest parse checker

Command:

```bash
python scripts/ci/check_manifest_parse.py
```

Measured result:

```text
161/161 passed
```

### 6.2 Work-item manifest schema and legacy ratchet

Command:

```bash
python scripts/ci/check_work_item_manifest_schema.py --tree HEAD --baseline 14-ai-development/reports/work-item-manifest-ac4-baseline.json
```

Measured result:

```text
rc=0
Legacy ratchet new regressions: 0
```

These are local command results supplied from the implementation worktree. They
are not a claim that GitHub Actions or any remote CI workflow has run or passed.

## 7. AID-2026-100 migration observation

After the required mode migration, the measured AID-2026-100 in-scope result
was:

```text
pins=10 ok=10
```

The existing related-evidence digest remained unchanged. The migration supplies
the explicit historical interpretation required to verify that declaration.

## 8. Verification boundary

The evidence above records local execution against the rebased implementation
commit and the specified fixed negative fixture.

It does not establish:

- a successful GitHub Actions run;
- an independent exact-head review;
- a merge commit;
- Owner acceptance;
- work-item closure.

The current recorded states remain:

- Implementation: `IMPLEMENTED`
- Review: `NOT_STARTED`
- Merge: `NOT_MERGED`
- Acceptance: `PENDING`
