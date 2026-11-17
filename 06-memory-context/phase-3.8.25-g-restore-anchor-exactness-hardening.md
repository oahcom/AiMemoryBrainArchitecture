# Phase 3.8.25 — G Restore Anchor Exactness Hardening
# Phase 3.8.25 — G Restore Anchor 精确匹配加固

- Date: 2026-11-18
- G code commit tested: `8afe821689b8a7b5c2069aef0f45fd0e89c72f87`
- Test source Blob: `4978622b1767019fb254763d4c5c44db46521f83`
- Workflow: [G Applied Persistence Reference Model #44188581729](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44188581729)
- Job: `g-applied-reference-model` — SUCCESS
- Log: `Ran 16 tests in 0.215s`, `OK`

## 1. Defect found

The previous SQLite reference model fenced a restored snapshot only when its epoch or ledger high-water was **less than** the trusted external anchor. A snapshot with a numerically greater epoch or high-water was therefore accepted as current if owner-currentness booleans were true.

That is unsafe: a snapshot ahead of the trusted anchor may be an unanchored fork, a stale/misconfigured external anchor, or a rollback-manipulated image. Numeric superiority alone does not prove a committed, authenticated prefix.

## 2. Correction

The reference model now requires exact equality of snapshot restore epoch and ledger high-water with the trusted external anchor before clearing the restore fence. Any mismatch in either direction remains FENCED. A production protocol may advance the anchor only through a separately authenticated contiguous-prefix/checkpoint proof, then repeat exact reconciliation.

Two negative tests were added:
- `test_15_snapshot_epoch_ahead_of_trusted_anchor_keeps_restore_fenced`
- `test_16_snapshot_highwater_ahead_of_trusted_anchor_keeps_restore_fenced`

Both prove that an apparently newer snapshot cannot re-enable serving without an authenticated anchor advance.

The bilingual G Phase 3.8.22 contract now states the same rule: EN Blob `a8efd1aa9696783035e157131fa9751666a4182d`; zh-CN Blob `dd3791aa50c5fb24e93f9ab5cee50d3b5c02706e`.

## 3. Verification

The workflow ran on exact code commit `8afe821689b8a7b5c2069aef0f45fd0e89c72f87`; both new negative tests passed and the full reference suite is **16/16 PASS**.

## 4. Scope

This closes a defect in the bounded SQLite reference model and tightens the G normative restore rule. It does not prove a production external monotonic anchor, signed checkpoint verification, real COC/owner ledger prefix continuity, PostgreSQL/Storage restore behavior, multi-replica recovery or production G persistence. G remains REFERENCE MODEL ONLY; production Full Applied is not proven.
