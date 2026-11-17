# Development Feasibility Matrix — DEV-FEAS-002

- Version: 1.0.0; baseline: `main@b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Source: F/D/P PR #46, branch `review/session-3-engineering-planning-2026-11-17`, commit `8b9ff8efa92a88dacc8f97b5faba5918fe5d2edc`, EN Blob `081610b1734ec08dc7c35c75fae1cae3ca713be4`, ZH Blob `834dc39998342dc2f292fe1dfed411768b3ed156`.
- A verdict: **FEASIBLE_WITH_CONDITIONS in principle; current implementation entry BLOCKED**.

## Feasibility matrix

| Area | Verdict | Complexity | Accountable Owner | Key prerequisite |
|---|---|---:|---|---|
| B Domain | FEASIBLE_WITH_CONDITIONS | L | B | Fact/Claim, identity and temporal ADR; downstream adoption |
| D Canonical Brain | FEASIBLE_WITH_CONDITIONS | XL | D | Canonical authority, cursor, producer barrier, Forget fence and visibility contract |
| E Compiler | FEASIBLE_WITH_CONDITIONS | L–XL | E | Durable admission, register-before-queue, lineage and replay/recovery |
| F Runtime/Retrieval | FEASIBLE_WITH_CONDITIONS | M–L | F | Authoritative permission/fence prefilter; stale projection suppression |
| G Context | FEASIBLE_WITH_CONDITIONS | L–XL | G | Context versioning, delivery and Applied boundary |
| C Agent Integration | FEASIBLE_WITH_CONDITIONS | L–XL | C | Final request boundary, provider side-effect idempotency and UNKNOWN recovery |
| H BMCP | FEASIBLE_WITH_CONDITIONS | L | H | Exact schema, canonicalization, signature, crypto and interoperability decisions |
| I Security/Governance | BLOCKED for policy closure; mechanisms conditionally feasible | XL | I + external governance authorities | I36-GOV-01..10, InventorySeal, revocation and trust approvals |
| Storage/Consistency | BLOCKED for production topology; prototype feasible | XL | Storage | L1 Option A logical topology selected; actual DB engine/adapter, persistent COC, same-XID recovery, failover/restore proof remain open |
| Index/Cache | FEASIBLE_WITH_CONDITIONS | M–L | F + D + Storage | Derived-only authority, rebuild, stale suppression and Forget safety |
| End-to-end system | NOT PROVEN | XL | All Owners; A integrates | Exact owner contracts + physical P0 proof + conformance |

## Effort and confidence

F/D/P uses relative sizes (S/M/L/XL), not person-days. No reliable calendar or staffing estimate exists because engineering headcount, availability, target hardware, runtime repository and delivery ownership are not designated. Converting relative sizes into dates would be false precision.

## Key technical conclusions

- Rust local-first modular monolith is plausible and preferred as a candidate starting shape; it is not an approved technology/topology ADR.
- Structured SQL + lexical retrieval is a viable first read path after authorization and Forget suppression are enforced.
- PostgreSQL 18.7 evidence is a bounded engine-capability probe, not proof of selected production topology or integrated D/I/COC operation.
- Durable ingress/outbox, canonical cursor, Forget/publication, JF-10 recovery and Applied require separate evidence boundaries.
- Vector/ANN, reranking and graph-backend expansion are not prerequisites for a safe first vertical slice.

## Current B→A feasibility update

- B's canonical identity and entity inventory artifacts now exist on main but remain CANDIDATE; B1 is in progress and Fact/Claim remains ADR-BLOCKED. They improve the research basis but do not close domain semantics or permit schema freeze.
- H Unified 1.2.14 / wire 1.3.0 + CSubmitOutcome 1.0.1 are a coherent L1/L2 candidate. C accepts the exact H mapping; D accepts the H high-water/RecoveryJoin carrier; I has an anchor review. However, H's mapping status still says C review required, H/I/D exact pins are not all current in one bundle, and Storage v3.2.9 is stale. Protocol freeze remains blocked until Storage v3.3.0 or equivalent is reviewed by C/H/D/I and A.
- Storage Option A is the preferred v1 logical direction but only conditionally accepted; A-01..A-05 and exact D acceptance remain open. L2/L3/L4 are not closed.

## Five engineering prerequisites

1. Project authority names canonical runtime repository, accountable engineering lead, maintainers, build/CI and contract-to-code traceability (Issue #7).
2. B closes normative identity/Fact-Claim/temporal semantics; consumers bind exact version.
3. I and external authorities close security/governance decisions and signed closed-world producer/recipient/backup inventory.
4. D/E/I/Storage agree on exact admission → dependency registration → fence → final visibility semantics and prove both race orders and crash windows.
5. Storage completes L4 physical realization and proves the selected L1 Option A profile (actual DB/adapter, COC, same-XID recovery, failover/restore); C/G/H close final-request and Applied/provider outcome contracts.

## Bounded engineering work

May proceed only in an isolated, non-production spike scope: synthetic fixtures, Rust workspace/toolchain exploration, typed ports with no frozen domain semantics, storage engine comparison, disposable PostgreSQL capability tests, deterministic model/fault harness scaffolding, FTS/vector quality benchmarks on synthetic data, resource inventory and documentation automation. Every spike must have an owner, exact input version, reproducible command, evidence artifact and explicit non-claim.

No production data, canonical visibility, security policy implementation, provider side effect, schema freeze or production deployment is authorized by this assessment.

See DEP-DAG-002, PRIORITY-002, READINESS-002 and GATE-002.


## Source freshness / assessed baseline

This assessment's source-evidence baseline is pinned to main commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. At publication, the observed main HEAD is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f` (a later revert commit); this later HEAD is not silently substituted for the assessed baseline. Before any Gate closure or freeze decision, refresh every cited Owner artifact and repeat the delta review against that HEAD. The Storage L1 topology source is separately pinned to Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`, branch `session-storage-consistency-forget-atomicity-2026-11-16`; §8 selects Option A for L1, while L4 physical conformance remains OPEN.


## Current main HEAD / 当前 Main HEAD

Current main HEAD observed for this publication: `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`. Earlier `6470f25...` / `b372b62...` values are historical snapshots, not current main. A full source-by-source delta audit against current main is not complete; G1 remains PARTIAL and Gate/freeze restrictions remain in force.
