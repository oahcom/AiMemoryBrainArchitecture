# ABR-INTEGRATION-003 — Cross-owner Forget model / 跨 Owner Forget 模型

## Purpose / 目的

A bounded Python explicit-state model extending the earlier one-object Forget abstraction with selected current Owner contract boundaries:
- D ProducerWork registration, Fence generation/high-water, barrier and final visibility gate;
- E work/attempt/lease, DLQ/retry and durable dependency registration;
- I PermissionEpoch, COMMIT_WON / REVOCATION_WON / UNKNOWN and held revocation;
- Storage visibility outcome and restore high-water;
- F cache/read disclosure boundary;
- I inventory completeness and D barrier reopening;
- durable Forget receipt and lost-ACK retry.

这是有限状态的研究模型，不是 TLA+/TLC 无界证明、Owner 合同替代品、数据库实现或生产安全认证。

## Reproduction / 复现

From this directory:

```bash
python3 forget_cross_owner_model.py
python3 -m unittest -v test_forget_cross_owner_model.py
```

The model uses only the Python standard library.\n\nRepository CI: [run 44140051181](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44140051181) — **SUCCESS** at integration-branch commit `c6c6e136f3d1c1b24448e28b754bfe083fe1a0f8`; both the model command and unittest regression suite completed successfully (14 tests). Earlier run 44136327645 is retained as historical evidence.

## Bounded result / 有界结果

- Safe transition graph: **28,383 state/depth pairs**, maximum depth 14; no modeled invariant violation.
- 13 weakened-guard mutants produce shortest counterexamples (see script output).
- Manual serial-order assertions cover I COMMIT_WON-before-revocation, revocation-before-commit, Fence-before-visibility, visibility-before-Fence, UNKNOWN participant handling and lost-ACK receipt replay.
- Cache negative control: a stale cache fill by itself is not an external disclosure if the final read gate still checks current Fence/Permission. A stale read after Fence/revocation is a violation. Cache-fill freshness remains a separate F contract requirement.

## Explicit assumptions / 明确假设

1. D Fence generation and producer registration are authority-local and monotonic; registration and Fence installation share one linearizable ordering domain.
2. E retries reuse the same logical work identity; attempts/leases are distinct execution identities. DLQ and lease expiry are nonterminal.
3. D dependency registration is complete and durable before the final publication gate.
4. I PermissionEpoch is compared only within the I namespace. It is never numerically compared with D Fence generation, Storage cursor or G ContextVersion.
5. I COMMIT_WON holds applicable revocation until the exact Storage participant reaches a terminal outcome. UNKNOWN remains open.
6. D final visibility gate rechecks the current Fence and dependency registration; an I receipt alone does not authorize visibility.
7. Restore release is blocked for a stale snapshot and succeeds only after replaying the current D-local Fence high-water. Real I/COC/Storage high-waters are separate and are not collapsed into one counter.
8. Lost ACK changes caller knowledge only; same operation key + normalized request digest resolves to the original durable receipt.

## Not modeled / 未建模

Multiple objects, scopes, tenants and overlapping Forget targets; arbitrary dependency DAGs; multiple concurrent producers/workers and independent storage replicas; actual MVCC/WAL/2PC/prepared-XID behavior; split brain, failover, PITR and pg_rewind; complete Producer/Recipient/Backup/External-copy inventory; cryptographic signing, key rotation and trust registry; full F/G/H Adapter and Context implementations; actual COC/G Applied persistence; physical erasure and operational deployment.

The `core_barrier_ready` predicate is deliberately not named or treated as I's `Global Forget Completed`. The model does not infer terminality from a missing Worker run; it accepts an abstract external no-publication proof input whose concrete D/E/Storage contract remains unresolved. A separate two-operation model is still required for overlapping Forget requests; this model remains single-operation.\n\nThe state count is bounded by this abstraction and depth. A PASS means only that no invariant violation was found in this finite model under the assumptions above. It does not establish that the Owner contracts or production topology implement those assumptions.
