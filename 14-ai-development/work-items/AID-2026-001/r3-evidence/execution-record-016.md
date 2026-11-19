# R3 Execution Record 016 (mainline integration measurement)

- Timestamp: 2026-11-19 23:13 (UTC+8)
- Executor: WorkBuddy coordinator
- Integration branch: `integration-aid-2026-001-r3-baseline`
- Pre-update branch Head: `fc179a5a0fb4f158a15df7ab3f98dec8a24d033f`
  (merge of `main` @ `4f82e3a48a35e9fd73e7920f0c6a559b77aaf0dc` into the
  previous PR Head `155dd1719c499f6234f58f0279420d3210880649`)
- Integration PR: https://github.com/oahcom/AiMemoryBrainArchitecture/pull/277
- Source dev branch: `remediation/aid-2026-001-forget-contract-closure-2026-11-18`

This record covers **mainline integration measurement only**. It does not
re-open, re-review or re-approve any Owner decision; the three Owner rulings
below are quoted as recorded, with the evidence they relied on.

## Blobs at this integration Head

| Artifact | Blob | LF bytes | Lines | sha256 (LF blob) |
|---|---|---|---|---|
| `reference-model/r3_contract_model.py` | `771c1fdc6f8a248a7121d165a0b035cebcc9880c` | 55,526 | 1,494 | `8324ec551749c2d50067967e4a445b26a6683008a4fa52e02da02a9976417a15` |
| `reference-model/test_r3_contract.py` | `22b8d81e7738fe66074f9973932a2dbe79fb52ae` | 91,930 | 2,450 | `26c72ceaa636606118ef94013b7515842d51b02b521c3cb0e6ef4303c72308af` |
| `reference-model/forget_model.py` (mainline, unchanged) | `cd623d67400c8870a729f79f88a4413f37bb335a` | — | — | — |
| `reference-model/test_forget_model.py` (mainline, unchanged) | `633e12db094b703b5f4a431950c3df369dababb0` | — | — | — |

### Measurement basis

`execution-record-013.md` and `execution-record-015.md` quote **57,020 B /
sha256 `35efab93…`** (model) and **94,380 B / sha256 `f326cafd…`** (test).
Those are the figures of the **CRLF-rendered Windows working copy**. This
record quotes the **canonical git blob** (LF) figures instead.

Both bases were recomputed and agree with what the earlier records state:

- CRLF rendering of blob `771c1fdc` → 57,020 B, sha256 `35efab9361f313bb556159818ef2fbb1a6380cbf48d12f8aead273c3c438a946` — matches record-013 / record-015 exactly.
- CRLF rendering of blob `22b8d81e` → 94,380 B, sha256 `f326cafd70c97a7cc0133ad2139d7508d83f493c710d80f534e01c25d68734ce` — matches record-015 exactly.

No earlier figure was fabricated; the two records simply did not label which
rendering they measured. This record labels it, and the Manifest
`dev_baseline_integration.measurement_basis` overlay now carries both sets.

## Test result at the integration Head

Command (identical to `.github/workflows/aid-2026-001-reference-model.yml`):

```
python -m unittest discover -s 14-ai-development/work-items/AID-2026-001/reference-model -v
```

```
Ran 103 tests in 0.007s

OK
```

103 = **79 R3 contract tests** (`test_r3_contract.py`) + **24 Forget model
tests** (`test_forget_model.py`).

The 24-test Forget figure comes from **mainline**, which is authoritative for
`forget_model.py` / `test_forget_model.py`. The source dev branch still carries
the older 14-test Forget model, so its own baseline is **93 tests OK
(79 + 14)** — as recorded in `execution-record-014.md` / `execution-record-015.md`.
Both numbers are correct for their respective trees; they are not in conflict.

## Repository gates re-run at the integration Head

| Gate | Command | Result |
|---|---|---|
| Reference-model unit tests | `python -m unittest discover -s .../reference-model -v` | **PASS** — 103 tests, 0 failed, 0 errors |
| Manifest strict YAML + required fields + referenced paths | repository CI parity script (duplicate-key-rejecting loader) | **PASS** |
| GOV-DOC-001 bilingual structural gate | `python3 scripts/check_bilingual_docs.py` (22 changed paths inspected) | **PASS** |

The bilingual gate is structural only. All changed paths sit under
`14-ai-development/`, which is not a `NORMATIVE_ROOT`, and no `docs/en/` or
`docs/zh-CN/` file was touched, so no paired-counterpart obligation was
triggered. The prompt-library sub-check also passed.

**Local parser version disclosure.** The CI workflow pins `PyYAML==6.0.2`; the
local re-run used `PyYAML 6.0.3` on CPython 3.12 (PyPI was unreachable from
this environment). 6.0.3 is a patch release over 6.0.2 and does not change the
duplicate-key-rejecting `UniqueKeyLoader` behaviour the gate depends on, but
the local run is therefore a *parity* check, not a byte-identical replay of
the CI image. The authoritative gate remains the CI run on the exact PR Head.

## What changed against the previous PR Head (`155dd17`)

1. **Merged current main** `4f82e3a` into the integration branch. The merge was
   clean — no conflicts, no manual resolution. `08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md`
   came in from main unchanged.
2. **Added `r3-evidence/execution-record-015.md`** (introduced on the source
   branch by `aee8780`), which the previous PR Head did not carry.
3. **Added `r3-evidence/execution-record-016.md`** (this file).
4. **Refreshed `manifest.yaml` `dev_baseline_integration`**: Storage decision
   `...-07` → `DEC-AID-2026-001-STOR-20261119-08`; code target `e5f1198` →
   `95347a5`; suite 93 → 103 (79 contract + 24 Forget model); records extended
   to 003–016; added `mainline_integration`, `mainline_append_only_edits` and
   `measurement_basis` blocks. All mainline manifest records above the overlay
   are preserved verbatim.
5. **Appended an R3 section to `reference-model/README.md`**, keeping the
   mainline Forget-model text verbatim. This file was previously listed under
   `excluded_from_integration`; it is now recorded under
   `mainline_append_only_edits`.
6. **Updated `INDEX.md`**: the AID-2026-001 row now cites Storage `...-08`,
   the 103-test figure and both blobs; a session-level delivery record
   `2026-11-19-AID-2026-001-R3-MAINLINE-INTEGRATION` was added. A stray
   trailing `)` in that row's Review cell was removed (typographic fix only).

No model, test, forget-model or mainline evidence file was modified.

## Three-owner decision ledger (as recorded)

| Owner | Decision | Target | Scope |
|---|---|---|---|
| D | `OD-D-FORGET-DELTA-20261119-009` — ACCEPT | `95347a5` | Forget lifecycle / atomic tuple / trigger gate |
| I | ACCEPT (no `Decision_ID` issued by the reviewer) | `95347a5` | F-OI-01…04, reference-model layer only |
| Storage | `DEC-AID-2026-001-STOR-20261119-08` — ACCEPT | `95347a5` | Atomic commit / persistence / recovery boundary |

Owner I reported `Test_Execution: NOT RUN` and did not expand the ruling to
AID-2026-001 acceptance. Storage reported `Reviewer: NOT RUN` and
`Unresolved_Findings: NONE`, and could not read `execution-record-015.md` at
`e5f1198` (404), so the 93-test figure remained a coordinator report for that
ruling. The 103-test figure in this record is a **coordinator** measurement at
the integration Head; no Owner re-ran the suite at that Head.

## Defect-return rounds — cap exceeded (registered)

The task instruction capped defect returns against the implementation session
at **2 rounds**, after which the item was to be recorded BLOCKED and
converged. **That cap was exceeded.** The implementation session required
roughly **8 return rounds** (U-053 → U-054/U-055 → U-056 → U-057/U-058 →
U-059 → U-060 → U-061 → U-062) before the model layer reached three-owner
ACCEPT.

Recorded explicitly rather than silently absorbed:

- The cap was exceeded in favour of convergence, under the standing user
  instruction to continue without waiting on a human.
- The extra rounds produced genuine reviewer findings (missing-credential
  bypass, incomplete snapshot, lost `FSTOR_17`, record-010 overstatement), so
  the extra rounds were not padding — but the instruction's cap was a
  governance control, and the deviation is disclosed here rather than
  presented as compliance.
- Two process defects surfaced during the extra rounds and are themselves
  registered: a concurrent write lost `test_FSTOR_17` while the record still
  claimed it existed, and `execution-record-010` shipped three prose claims
  that its own target commit did not support (`erratum-004`).

## Boundaries

Reference-model level only. No WAL, fsync, torn-write, power-loss, physical
crash-recovery or production verifier claim. DFI-013 (deterministic
interleaving, not concurrency linearisation) and DFI-021 (in-memory model, not
physical WAL durability) are retained. `TrustAllReceiptVerifier` is a test
double; the shipped default `RejectingReceiptVerifier` stays fail-closed.

Still **NOT RUN** and **NOT AUTHORIZED**: production activation, formal Owner
approval, architecture acceptance, production R3 evidence, real cryptographic
receipt signature verification, production issuer minting a fresh credential
per retry, and enforced production verifier.

PR #277 therefore remains **OPEN — NO AUTO-MERGE**: a fresh independent
exact-Head re-verification and an explicit Owner/governance approval are
required before merge. Per PR-GOVERNANCE-001 §4, any further push invalidates
the test figures in this record and requires a re-run.
