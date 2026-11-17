# Architecture and Implementation Dependency DAG — DEP-DAG-002

- Version: 1.0.0; baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Authority: A integration; Owner-specific semantics remain with named Owners.

## Architecture decision DAG

```text
Project authority: runtime repo + accountable engineering owner
  ├─ B: canonical identity / Fact-Claim / temporal semantics
  ├─ I + external authorities: security policy / trust / inventory / revocation
  ├─ D/E: canonical lifecycle / admission / lineage / cursor contracts
  ├─ C/G/H: final request / provider outcome / Applied semantics
  └─ Storage + D + I: physical serialization / visibility / recovery topology
        ↓
Exact-version consumer acceptance + cross-owner conflict resolution
        ↓
A integration disposition (does not replace Owner approvals)
        ↓
Bounded implementation-entry decision
```

## Implementation dependency DAG

```text
P0-01 implementation repository, accountable lead, reproducible build
  ↓
P0-02 B identity/domain semantics + I policy/inventory prerequisites
  ↓
P0-03 L1 Option A logical profile selected; prove L4 physical DB/adapter and COC topology
  ↓
P0-04 D/E/I/Storage admission + lineage + fence + visibility contract
  ↓
P0-05 durable ingress/outbox + canonical commit/cursor/recovery
  ↓
P0-06 authorized structured/lexical retrieval + Forget-safe projections
  ↓
P0-07 Context version/delivery + C/G/H final request and Applied
  ↓
P0-08 integrated race/crash/replay/failover/restore conformance
  ↓
separate deployment and production acceptance
```

This is a hard dependency order for claims and protected execution, not a ban on parallel preparation.

## Verification dependency DAG

```text
Exact source pins and Owner authority evidence
  → semantic/contract consistency
  → model/schema negative tests
  → component tests
  → cross-owner contract tests
  → race/crash/ACK-loss/replay/failover/restore tests
  → independent evidence review
  → Gate-specific acceptance
  → production operational authorization
```

## Critical path and parallelism

Critical path: designate implementation authority → close B/I and other Owner-owned semantics → complete L4 physical realization of selected Storage Option A and COC topology → prove D/E/I/Storage publication/Forget boundary → prove durable canonical vertical slice → safe retrieval/context → Applied → recovery/restore conformance.

Parallel bounded work: synthetic-data retrieval benchmarks; DB/COC candidate comparison; fault-harness scaffolding; schema validators that do not freeze candidate schemas; bilingual parity and exact-pin automation; hardware/workload inventory; observability/runbook drafts. These do not release dependent gates.

## Dependency rules

- B semantics precede dependent schema/type freeze.
- I policy precedes protected authorization, revocation and Global Forget claims.
- D/E/I/Storage atomic visibility precedes canonical publication implementation and production read/write.
- C/G/H exact final-request semantics precede Applied implementation.
- Storage topology and JF-10 physical proof precede production consistency claims.
- Technology ADRs follow Owner contracts and reproducible experiments, not the reverse.

See SYS-RISK-002, DEV-FEAS-002, PRIORITY-002 and GATE-002.
