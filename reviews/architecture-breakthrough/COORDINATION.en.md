# Architecture Breakthrough — Coordination Record

**Status:** Four isolated research branches created; this is a coordination entry, not an architecture decision.  
**Shared baseline:** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb` (2026-11-18)  
**Master tracking:** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## Workstreams

| ID | Research area | Branch | Current status |
|---|---|---|---|
| A | Forget Protocol Formal Verification | `research/breakthrough-a-forget-model-checking-2026-11-18` | Isolated branch created; model/source verification pending |
| B | Memory Operating System | `research/breakthrough-b-memory-operating-system-2026-11-18` | Isolated branch created; baseline analysis/prototype pending |
| C | Memory IR / Compiler | `research/breakthrough-c-memory-ir-compiler-2026-11-18` | Isolated branch created; baseline analysis/prototype pending |
| 0 | Principal Coordination | `research/breakthrough-0-coordination-2026-11-18` | This coordination record |

## Shared rules

- Each workstream independently reads exact current sources and records branch HEAD, path, and Blob SHA.
- Add reports, models, synthetic data, and prototypes only on the corresponding research branch.
- Do not modify main, Owner branches, existing PRs, the body of Issue #43, or authority contracts.
- No merge, deployment, or production Runtime implementation.
- Chinese/English peers must be in the same change set and semantically aligned.
- Classify findings as DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED.
- Simulating another Owner role is not independent Owner approval; a passing model is not physical production validation.

## Initial system-problem map

1. Forget safety: composition across Owner boundaries for Admission, Dependency Registration, Publication, Visibility, and Restore lacks sufficient proof.
2. Runtime complexity: Retrieval, Activation, Context Budget, and Eviction may duplicate decisions and state synchronization.
3. Formation complexity: intermediate representation, type boundaries, provenance, and incremental evolution from Raw Experience to Canonical Memory need validation.

These are research hypotheses/problem mappings, not a complete review of current normative specifications.

## Consolidation gates

Before a workstream submits conclusions, it must provide:
- exact source ledger and evidence levels;
- reproducible models/experiments/commands;
- counterexamples or negative results;
- itemized comparison against the existing architecture;
- safety, complexity, performance, migration, and operational impact;
- unresolved questions assigned to the correct authority;
- Chinese/English semantic parity checks.

## Principal coordination question

The final comparison must determine which mechanisms should reuse mature products, which domain invariants require custom ownership, which modules can be merged or lowered, which candidates should be rejected, and whether the minimum safe architecture becomes easier to implement. All recommendations remain candidates absent formal approval.
