# Minimum Engineering Slice — Entry Contract and Readiness Decision

- Review ID: **A-MIN-SLICE-ENTRY-001**
- Authority: A / Principal System Architecture Authority (integration proposal)
- Status: **PROPOSED / NOT OWNER-APPROVED / NOT IMPLEMENTATION AUTHORIZATION**
- Baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Branch: `review/a-minimum-slice-entry-contract-2026-11-18`
- Governing tracker: Issue #43
- Runtime-location blocker: Issue #7 (OPEN)
- Scope: entry criteria and candidate sequencing only; no implementation, schema, technology or Owner contract changes.

## 1. Decision

**Do not start a production or protected-path runtime vertical slice yet.** The canonical runtime repository and accountable engineering owner have not been identified in Issue #7, and the architecture still has unresolved domain, authorization, Forget, serialization and recovery obligations.

The first engineering work item recommended by A is therefore **not a runtime feature**. It is a bounded, synthetic-only executable safety/conformance package for the Forget/publication lifecycle, derived only after the relevant D/E/I/Storage Owners pin and clarify their exact contracts. This is a candidate sequencing recommendation, not a substitute for those Owner decisions.

A later runtime vertical slice may be a minimal single-authority canonical write → durable commit → authoritative read path, with Forget/no-resurrection and authorization checks included. It must not be reduced to a happy-path CRUD demo. Provider/Applied delivery is explicitly excluded from this first slice unless an approved product requirement proves it indispensable.

## 2. Current evidence and blockers

Current main is anchored at `e52594f181d2edb77448adcfed64a0fbdffaf3aa`. PR #93 independently records a live compare of that commit with main as identical; the compare from `b3c666e...` reports two commits ahead and zero file changes. This is a history difference, not evidence of tree-content drift.

| Evidence | Exact reference | Integration meaning |
|---|---|---|
| Architecture-breakthrough integration | PR #93 head `0f3ba5293add8d6147a4375796b04c8bc6ae75e1` | Forget remains P0 / NOT READY; Resource Manager and Memory IR remain shadow-only candidates; no architecture superiority or freeze proven |
| Forget bounded model | PR #88 head `bf35b32295d0d3f337c80c3dc406db0a41de6830` | Safe abstraction explored 606 state/depth pairs through depth 10; five weakened-guard mutants yielded counterexamples. This is bounded model evidence, not production proof |
| Memory OS research | PR #86 head `3892916ce2379f807a0ddcd0039816f6e88ecee1` | Resource Manager remains candidate/shadow-only; synthetic results show trade-offs, not universal improvement |
| Memory IR research | PR #85 head `c5013d3585d54457f38bef37984645e2055ff7cf` | Shadow Typed IR inside E remains candidate; it cannot decide B semantics or replace D Canonical Commit |
| H/C branch integrity | PR #90 head `0dc8444d590cea19c9ac9bce14e8a6825d55ea01`; PR #91 head `55c60a11aedef858d450e19391cb3fcdfabf1199` | A recorded a destructive H-tree regression and C/H source reconciliation risk. Later C review PR #92 reports restored branch snapshots; exact live branch/Blob pins must be refreshed before relying on either snapshot |
| Runtime implementation authority | Issue #7 OPEN | No canonical runtime repo, engineering lead/maintainers, reproducible build/CI authority or deployment/operator map established in the accessible evidence |

### Blocking facts that must not be collapsed

1. B Fact/Claim remains ADR-BLOCKED; no canonical Fact/Claim schema or identity may be inferred.
2. I governance/trust and closed-world inventory obligations remain blocking.
3. D/E/I/Storage publication, Forget barrier, visibility linearization, crash recovery and anti-rollback evidence remain incomplete.
4. Storage Option A is a selected L1 logical direction only; it does not prove L2/L3 race safety or L4 physical conformance.
5. H/C Applied evidence and provider integration are not prerequisites for a provider-free canonical write/read slice; their unresolved state must not be used to smuggle Applied into the first slice.
6. H branch snapshots in PR #90/#91 and PR #92 are inconsistent in chronology. No H source is accepted here without a fresh exact branch HEAD, recursive tree inventory and Blob readback.
7. Issue #7 has no project-authority answer in the latest fetched issue/comments.

## 3. Candidate work decomposition

### Stage 0 — source and authority stabilization (mandatory, no runtime code)

- Re-read main and all relevant Owner branch heads immediately before each review.
- Publish an immutable source manifest: repository, branch, commit, path, Blob SHA, decision status, reviewer scope and supersession relation.
- Resolve the H/C tree-integrity incident and stale-source discrepancies before consuming H/C artifacts.
- Obtain B's explicit domain decision or preserve neutral opaque candidate vocabulary.
- Obtain I's exact governance/trust decision and inventory closure plan.
- Obtain D/E/Storage exact contracts for registration, fencing, visibility, transaction ownership and recovery.
- Obtain the project-authority response to Issue #7.

**Exit:** all sources used by the proposed slice are current, immutable and explicitly accepted by their accountable Owners for the stated scope. A report or delegated role simulation is not an Owner signature.

### Stage 1 — Forget/publication safety evidence (recommended first executable work)

A bounded synthetic model/conformance harness may be prepared only after Stage 0 supplies exact contract inputs. It must cover at least:

- producer/derived-work admission before and after Forget cutoff;
- registration-before-visible and the participant barrier;
- final Fence and lineage validation at the visibility linearization point;
- concurrent Forget operations and monotonic high-water behavior;
- lost acknowledgement, retry, duplicate delivery and idempotent receipt replay;
- worker pause/crash at every durable boundary;
- cache refill, index rebuild, stale restore and delayed participant discovery;
- unknown authority state, stale epoch/generation and unavailable participant fail-closed behavior;
- quarantine/IN_DOUBT retention and recovery without premature visibility.

The PR #88 model's 606 explored state/depth pairs and mutant counterexamples are a starting point only. Expand the state space and explicitly document abstraction gaps. Do not label bounded exploration exhaustive or production-safe.

**Exit:** reproducible model/harness, exact input contract pins, invariant-to-test traceability, counterexample regression tests, and Owner review of the model-to-contract mapping. No production deployment follows automatically.

### Stage 2 — first runtime vertical slice (conditional; not authorized now)

Candidate scope, subject to Owner decisions:

1. One explicitly scoped BrainAuthority and one serialization domain.
2. Synthetic-only ingress/admission under the approved B/I semantics.
3. D/E-owned durable registration and canonical commit under the adopted Storage topology.
4. Forget barrier, final visibility gate and no-resurrection behavior.
5. One authoritative read path that revalidates current Permission/Fence and cannot read stale derivative/cache state.
6. Deterministic fault injection, recovery and evidence emission for each state transition.

Out of scope: multi-authority transactions, production data, provider side effects, external delivery, global Applied, distributed scaling, advanced retrieval/reranking, full Memory OS, and production deployment.

The slice is not a CRUD demo: a write is not accepted until durable ordering and visibility are proven; a read is not accepted until current authorization and Forget state are checked.

## 4. Dependency DAG and ownership

```text
Project authority / Issue #7
          |
          v
Canonical runtime repo + accountable engineering owners
          |
          v
Exact source manifest + current Owner decisions
  |       |       |        |
  B       I       D/E      Storage
  |       |       |        |
  +-------+-------+--------+
                  |
                  v
        Forget / publication contract
                  |
                  v
     Synthetic model + conformance harness
                  |
                  v
       Owner-reviewed safety evidence
                  |
                  v
       A scoped slice-entry decision
                  |
                  v
     Runtime vertical slice (future approval)
```

| Work | Accountable authority | A's role |
|---|---|---|
| Fact/Claim/domain identity | B | Check cross-module compatibility; do not decide B semantics |
| Permission, trust, inventory, governance | I | Check system-level closure and evidence |
| Canonical lifecycle, commit and Forget domain result | D | Check integration and ordering; do not rewrite D semantics |
| Derived registration and compilation | E | Check publication dependencies; do not make IR canonical |
| Serialization, durability and recovery | Storage | Check topology/physical proof boundary |
| Runtime repository, code owners, CI and operations | Project authority / engineering leadership | Require evidence through Issue #7; do not invent ownership |
| System slice entry and Gate disposition | A with governance authority as applicable | Issue a scoped decision only after evidence is complete |

C/G/H become mandatory only if the chosen slice crosses provider request, external delivery or Applied evidence boundaries.

## 5. Entry gates

All are conjunctive; a partial pass does not authorize implementation.

| Gate | Required evidence | Current state |
|---|---|---|
| E0 — Runtime location and accountable owner | Issue #7 answer; canonical repo/branch; named engineering owner/code owners; build/test/CI and artifact SHA source; deployment/operator map | **BLOCKED** |
| E1 — Domain semantics | B Fact/Claim ADR and exact downstream type mapping, or formally scoped neutral vocabulary | **BLOCKED** |
| E2 — Governance and authorization | I policy/trust decisions, issuer/key lifecycle, revocation, inventory and fail-closed behavior | **BLOCKED** |
| E3 — Lifecycle and publication | D/E exact admission, registration, fencing, visibility and no-resurrection contracts | **NOT PROVEN** |
| E4 — Durable ordering and recovery | Storage/D exact Option A adoption, A-01..A-05 disposition, L2/L3 race proofs and L4 physical plan/evidence appropriate to the slice | **NOT PROVEN** |
| E5 — Forget safety | Invariants mapped to Owner contracts and executable fault tests; restore/replica/index/cache behavior addressed | **NOT READY** |
| E6 — Test isolation | Synthetic-only data, isolated environment, no production credentials/data/provider side effects, reproducible harness | **NOT ESTABLISHED** |
| E7 — Slice ownership and acceptance | Named implementer/reviewer/operator; code-to-contract traceability; exit and rollback authority | **BLOCKED** |

## 6. Acceptance and stop criteria

### Stage 1 acceptance

- Every invariant has a named Owner contract source and at least one positive and negative test.
- All counterexamples are reproducible and regression-tested.
- Crash/retry/replay/restore and concurrent Forget cases are included.
- Unknown/stale authority state fails closed.
- Results state explored bounds and excluded behaviors.
- A and each relevant Owner explicitly accept only their own scope.

### Future runtime-slice acceptance

- Reproducible build and CI on the canonical runtime repository.
- Contract-to-code-to-test traceability for every in-scope transition.
- Durable state and recovery behavior demonstrated under injected crashes.
- No read path can expose forgotten or unauthorized data after the defined linearization point.
- No stale cache/index/replica/restore path can resurrect suppressed data.
- All required Owners sign the exact commit and artifact set; A issues a separate scoped integration decision.
- Rollback/stop procedure is tested and does not roll back Forget or authorization high-water state.

### Immediate stop conditions

Stop and return to the owning authority if any source pin changes, an Owner branch loses authoritative files, semantics are disputed, a required participant is unknown, authority state is unavailable, recovery cannot prove current high-water state, a test requires production data/credentials, or any provider/external side effect is attempted outside explicit approval.

## 7. Explicit non-authorizations

This document does **not** authorize:

- runtime code in this architecture repository;
- protected-path implementation in any repository;
- production or customer data access/write;
- provider calls, external delivery or side effects;
- schema/technology freeze or architecture adoption of Memory OS / IR;
- Gate passage, Issue closure, PR merge, deployment or production activation.

Only isolated documentation and synthetic, contract-neutral feasibility preparation remain permissible under the existing governance constraints. Issue #7 remains OPEN and G3 remains BLOCKED.

## 8. A proposed disposition

**DEFERRED / ARCHITECTURE_NOT_READY.** Adopt Stage 0 as mandatory. Prioritize Stage 1 Forget/publication safety evidence as the first bounded executable engineering artifact, conditional on exact Owner contract inputs. Keep the first runtime vertical slice unselected until B/I/D/E/Storage and project authority satisfy the entry gates.

This is an A proposal for review, not an Owner decision. Keep this PR Draft and unmerged.
