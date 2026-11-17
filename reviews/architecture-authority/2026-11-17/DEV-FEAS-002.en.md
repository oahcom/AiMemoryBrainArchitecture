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
| Storage/Consistency | BLOCKED for production topology; prototype feasible | XL | Storage | Selected physical topology, persistent COC, same-XID recovery, failover/restore proof |
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

## Five engineering prerequisites

1. Project authority names canonical runtime repository, accountable engineering lead, maintainers, build/CI and contract-to-code traceability (Issue #7).
2. B closes normative identity/Fact-Claim/temporal semantics; consumers bind exact version.
3. I and external authorities close security/governance decisions and signed closed-world producer/recipient/backup inventory.
4. D/E/I/Storage agree on exact admission → dependency registration → fence → final visibility semantics and prove both race orders and crash windows.
5. Storage selects and proves actual DB/COC topology; C/G/H close final-request and Applied/provider outcome contracts.

## Bounded engineering work

May proceed only in an isolated, non-production spike scope: synthetic fixtures, Rust workspace/toolchain exploration, typed ports with no frozen domain semantics, storage engine comparison, disposable PostgreSQL capability tests, deterministic model/fault harness scaffolding, FTS/vector quality benchmarks on synthetic data, resource inventory and documentation automation. Every spike must have an owner, exact input version, reproducible command, evidence artifact and explicit non-claim.

No production data, canonical visibility, security policy implementation, provider side effect, schema freeze or production deployment is authorized by this assessment.

See DEP-DAG-002, PRIORITY-002, READINESS-002 and GATE-002.
