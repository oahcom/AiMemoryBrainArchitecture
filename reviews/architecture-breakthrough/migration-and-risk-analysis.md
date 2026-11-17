# Migration and Risk Analysis

- Status: candidate migration path; no production/runtime changes authorized
- Research branch: `research/architecture-breakthrough-session-0-2026-11-18`

## 1. Migration principles

1. Research artifacts remain isolated from Owner source specifications.
2. No semantic change is made by introducing an internal IR or resource ledger.
3. Shadow mode precedes authority transfer or data migration.
4. Every candidate must preserve stable IDs, provenance, Scope, PermissionEpoch, ForgetFence and all typed cursors.
5. Rollback must return to the previous reader/writer path without restoring stale authorization or Forget state.
6. Unknown outcomes remain unknown; no migration step may infer success from missing data.
7. All schema/version transitions need explicit compatibility and replay tests.

## 2. Phased plan

### Phase 0 — Isolated research (current)
- Add bilingual research reports and source pins only.
- No Owner specs, schemas, ADRs, Runtime code or deployment changes.
- Output: reviewable candidate PR.

### Phase 1 — Forget reference model
- Model only one authority, target lineage, two producers, one derivative and one visibility boundary.
- Add registration/fence race, dependency gap, lost ACK, stale lease, DLQ replay and restore rollback actions.
- Run TLC with finite bounds; save tool version, config, output and counterexample traces.
- Expand only after the minimal model is stable.
- Exit: safety invariants hold for declared bounds, or counterexamples are assigned to D/E/I/Storage.

### Phase 2 — Resource Manager prototype
- Implement a test-only resource ledger in a separate prototype branch or harness.
- Feed deterministic replay of actual F/G request traces.
- Compare split budgets with hierarchical reservations.
- No change to F/G interfaces until measurements show clear benefit.
- Exit: measurable improvement without worse Forget/revocation latency, fairness or context sufficiency.

### Phase 3 — Memory IR shadow pipeline
- Serialize current compiler stage outputs into an IR envelope in parallel; do not make it canonical.
- Validate type, source span/digest, provenance, Scope and schema version.
- Replay same fixture set with identical inputs and compare outputs.
- Exit: deterministic pass outputs and no lineage loss; explicit migration plan for version evolution.

### Phase 4 — Owner review and ADR proposals
- Present only measured findings to accountable Owners.
- Draft candidate ADRs separately if required.
- Obtain formal Owner approvals and cross-consumer adoption before changing normative specs.
- Runtime implementation requires separate project authorization and an accountable implementation repository/owner.

## 3. Risk register

| ID | Risk | Severity | Mitigation / gate |
|---|---|---|---|
| R1 | Bounded model misses longer or unbounded trace | High | Explicit bounds, inductive proof where feasible, adversarial implementation tests |
| R2 | Formal model encodes wrong owner semantics | Critical | Owner source mapping, independent review, no role simulation as approval |
| R3 | PostgreSQL transaction boundary excludes COC/Adapter/vector index | Critical | Draw exact physical transaction boundary; unknown external effects remain out-of-transaction |
| R4 | Resource manager becomes new central authority | High | Restrict to capacity/admission; F/G keep semantic owners |
| R5 | Token budget conflated with RAM budget | High | Typed dimensions and separate semantic sufficiency |
| R6 | Eviction removes non-rebuildable or authoritative data | Critical | Evict only disposable projections; canonical store never evictable |
| R7 | IR freezes unresolved Fact/Claim schema | Critical | Provisional type envelope; B ADR remains blocking |
| R8 | IR transformation loses evidence/provenance or Scope | Critical | Mandatory source digest/span, Scope, evidence roles and lineage validation |
| R9 | Model extraction nondeterminism breaks replay | High | Record model/prompt/policy versions and output digest; treat extraction as Activity result |
| R10 | Recompilation creates duplicate or resurrected derivatives | Critical | Stable lineage identity, new DerivationRunId, D registration and current fence gate |
| R11 | Product adoption increases operational burden | Medium/High | Local-first profile, component count and recovery runbook review |
| R12 | Research branch becomes de facto architecture | High | Labels, status vocabulary, no merges into main without approval, explicit non-normative banners |

## 4. Rollback conditions

- Any candidate causes a Forget/Permission stale-read or resurrection counterexample.
- Resource manager cannot release reservations after worker crash or leaks across principal/scope.
- A budget change causes unacceptable sufficiency loss or interactive starvation.
- IR shadow output differs without an explainable, versioned transformation.
- Recompile cannot reproduce source/provenance lineage.
- New service adds more operational steps than the problem it removes.
- Candidate requires changing an Owner authority contract without explicit approval.

## 5. Acceptance evidence

For each phase retain:
- exact branch/commit/blob and tool versions;
- workload fixture digest;
- command and configuration;
- raw output and counterexample traces;
- baseline and candidate metrics;
- known omissions and confidence limits;
- independent review and Owner acceptance record.
