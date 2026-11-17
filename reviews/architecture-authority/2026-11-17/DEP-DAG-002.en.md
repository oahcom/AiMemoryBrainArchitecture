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

## Updated B→A closure sequence

**Wave B — exact protocol bundle:** H updates the 1.2.14 mapping to the current D crosswalk; C re-reviews that successor mapping; H reviews current I P0; I refreshes its anchor review; H records C acceptance and current CI; Storage publishes v3.3.0 or equivalent binding the exact current C/H/D/I/Storage Blobs and run/commit/job; C/H/D/I review that identical manifest; A re-reads the successor manifest and source heads. No protocol freeze before this chain closes.

**Wave A — Option A L1/L2:** Storage proposes an ADR successor addressing A-01/A-06 doc clarity; D makes an exact decision on the Storage ADR and shared-anchor contract; D/Storage define the shared transaction executor/UoW and row-write authorization boundary; D maps EffectPermit to all fence-sensitive lifecycle transitions; constrain each v1 atomic operation to one BrainAuthorityRef; I/Storage define COMMIT_WON replay/revocation/crash semantics; Storage/I define an independent restore anti-rollback witness; D/I/Storage/H clarify COC/JF-10 proof ordering without cross-log atomicity. A re-reviews exact successor Blobs. L1 closes only after A-01/A-03 and D acceptance; L2 requires A-04/A-05 composition; L3 requires executed deterministic concurrency/reference-model/fault evidence; L4 remains physical deployment.

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


## Source freshness / assessed baseline

This assessment's source-evidence baseline is pinned to main commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. At publication, the observed main HEAD is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` (a later revert commit); this later HEAD is not silently substituted for the assessed baseline. Before any Gate closure or freeze decision, refresh every cited Owner artifact and repeat the delta review against that HEAD. The Storage L1 topology source is separately pinned to Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`, branch `session-storage-consistency-forget-atomicity-2026-11-16`; §8 selects Option A for L1, while L4 physical conformance remains OPEN.


## Current main HEAD / 当前 Main HEAD

Current main HEAD observed for this publication: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`. Earlier `6470f25...` / `b372b62...` values are historical snapshots, not current main. A full source-by-source delta audit against current main is not complete; G1 remains PARTIAL and Gate/freeze restrictions remain in force.
