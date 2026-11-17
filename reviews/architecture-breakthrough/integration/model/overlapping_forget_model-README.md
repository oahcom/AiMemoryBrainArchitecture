# ABR-INTEGRATION-006 — Overlapping Forget Micro-Model / 重叠 Forget 微型模型

## Purpose / 目的

This separate bounded model addresses M-03 from the single-operation Forget model audit. It represents two overlapping Forget operations with distinct operation generations, partially overlapping target sets (`{a, shared}` and `{shared, b}`), operation-scoped terminal evidence, independent barriers and receipts, and late target discovery.

该模型只证明两个抽象 Forget 操作在有限状态下的基本单调性与隔离性质；不是完整多租户 Forget 协议，也不是物理并发/恢复证明。

## Reproduction / 复现

```bash
python3 overlapping_forget_model.py
python -m unittest -v test_overlapping_forget_model.py
```

Python standard library only.

## Bounded result / 有界结果

- Safe graph: **2,425 state/depth pairs**, max depth 12, no modeled invariant violation.
- Five weakened-guard mutants produce shortest counterexamples:
  - duplicate/reused operation generation;
  - one operation closes the other operation's barrier;
  - shared-target evidence is reused across operation identity;
  - late target discovery fails to reopen its operation;
  - one receipt incorrectly closes the other operation's barrier.
- Tests cover both installation orders, independent closure, shared target identity scoping and late discovery.

## Explicit assumptions / 明确假设

1. One D-local durable generation counter allocates a strictly increasing generation to each new operation/successor snapshot.
2. Each operation has its own immutable target set snapshot and independent terminal evidence namespace.
3. A shared target is independently evidenced under each operation identity; an op2 receipt cannot satisfy op1.
4. Late target discovery creates a successor generation for only the affected operation, reopens its barrier and makes its prior receipt non-current; it does not rewrite the other operation's barrier.
5. Operation receipts are current only for the generation they name.

## Not modeled / 未建模

More than two operations; arbitrary concurrent event interleavings beyond this finite action graph; real producer/recipient/backup inventories; cross-scope authorization; multiple workers/leases; Storage prepared participants, WAL/MVCC/2PC; crashes at every durable boundary; I Global Forget typed evidence and CompletedWithPolicyException; physical erasure and restore.

This model partially addresses M-03 only. It does not close M-04/M-05, JF-10, I Global Forget completion, or any production gate.
