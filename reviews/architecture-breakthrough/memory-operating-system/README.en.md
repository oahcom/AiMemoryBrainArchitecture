# Memory Operating System Architecture Research

**Status:** Baseline pinned; design and experiments not yet completed.  
**Baseline:** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb` (2026-11-18)  
**Tracking:** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## Core question

Do Retrieval, Activation, Context Assembly, Budget, Eviction, Working Set, and Scheduling duplicate decisions about which memories should be selected or retained under task and resource constraints? Could a unified Memory Resource Manager reduce complexity while preserving domain boundaries and hard safety constraints?

This is not a renaming exercise that transplants Linux terminology into Memory Brain. Compare architecture complexity, provability, and real operational cost.

## Current constraints

- Memory Runtime remains in architecture-definition/feasibility research; this work does not authorize Runtime implementation.
- Forget, Permission, Authority, Provenance, and Freshness constraints must not be weakened into ranking scores.
- No Issue #43 decision or Owner authority changes as a result of this research.
- This branch does not modify F/G or any other Owner-authoritative contract.

## Baseline inspection

Read exact current F Retrieval, G Runtime, B Domain Model, C Agent Integration, and relevant Context, Activation, Budget, Eviction, Storage/Index/Cache documents and tests. Record branch HEAD, path, Blob SHA, status, and read timestamp for each critical source.

## Architecture alternatives

- A: retain separate Retrieval / Activation / Context / Budget responsibilities.
- B: unify resource decisions while preserving domain responsibilities and module interfaces.
- C: adopt a more comprehensive Memory OS kernel for request scheduling, residency, budget, and eviction.

Compare complexity, correctness, latency, throughput, resource efficiency, explainability, concurrency fairness, starvation, recovery, operational cost, and migration cost.

## Mechanisms to investigate

Working Set, Page Cache, Page Fault, Memory Pressure, LRU/LFU/ARC, CPU Scheduling, Cgroups, NUMA, and Kubernetes Resource Requests/Limits. For every mapping, state applicability conditions, failure boundaries, and whether the concept truly matches Memory semantics.

## Prototype experiment

Use deterministic synthetic data to compare:
1. Top-K Retrieval;
2. Retrieval + Reranking + Budget;
3. Unified Resource Manager.

Report at least Recall, Precision, Token Efficiency, Context Redundancy, Latency, Task Coverage, Budget Utilization, Starvation, and Fairness. Publish data generation, parameters, commands, and raw results. Synthetic data supports claims only within the tested setup.

## Safety invariants

The resource manager may optimize only within an authorized candidate set. Forget suppression, Permission, Authority, Scope, and Provenance are hard filters, never utility-score tradeoffs. The manager cannot create Canonical Memory or change lifecycle authority.

## Acceptance and deliverables

Deliver a current complexity map, OS-mechanism mapping, three-way architecture matrix, candidate request/decision contract, runnable prototype, benchmark results, migration/risk analysis, and bilingual report. Classify conclusions as DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED, and explicitly decide whether a formal architecture change is justified.
