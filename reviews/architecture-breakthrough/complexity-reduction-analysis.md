# Complexity Reduction Analysis

- Baseline: `main@28fb37e21fa4ba2b871f7816fe669128618c063e`
- Status: evidence-backed hypotheses; no measured complexity reduction claimed

## 1. What complexity is essential

The following are not candidates for consolidation merely because they look repetitive:

- D ForgetFenceGeneration, I PermissionEpoch, E ProducerRegistrationHighWater, D CanonicalCommitCursor, F IndexWatermark, G ContextVersion and H AdapterCapabilityEpoch are distinct authority-local orders.
- Canonical Memory, Memory Context and Applied Context have different owners and evidence meanings.
- Logical suppression, derivative cleanup and physical erasure are different promises.
- Accepted, Compiled, CanonicalCommitted, Indexed, Delivered and Applied are different milestones.
- Producer work identity must survive retries and lease changes; attempt/lease identity must not become admission authority.

Merging these distinctions would reduce visible vocabulary but increase semantic ambiguity and race risk.

## 2. Candidate complexity to remove

### C-01 — Duplicate resource accounting across F/G
F has per-request candidate/evidence/latency budgets and Working Set byte/entry limits. G has Context token/byte budgets, ordering, expiry and sufficiency. These are not identical budgets, but may be accounted separately without a common reservation mechanism.

**Candidate reduction:** one resource ledger and hierarchical reservation API. F still chooses retrieval/activation; G still chooses Context membership and version. Resource Manager reports capacity and enforces limits, not semantic decisions.

Evidence to collect: number of budget structures, repeated conversion logic, over-reservation, token waste, memory peaks and inconsistent limit outcomes.

### C-02 — Unstable compiler stage contracts
E's stages exchange candidate objects, evidence/provenance records, conflict proposals and canonical write requests. Without a stable IR, each new stage/model/schema version may add conversion logic and lose metadata.

**Candidate reduction:** typed Memory IR with schema digest and provenance envelope. Existing stage responsibilities remain; only the boundary representation changes.

Evidence: count of DTOs/adapters, lossy conversions, duplicate parsing, migration complexity and reproducibility.

### C-03 — Forget proof fragmented across documents
D/E/I/Storage/F/G/H define related races and acknowledgements in their own language. This is partly necessary because authority is distributed, but the cross-owner composition needs one machine-checkable protocol model and one canonical race/crash matrix.

**Candidate reduction:** shared formal model and generated scenario IDs/trace references. Do not centralize domain authority or force every owner to duplicate all state fields.

Evidence: repeated invariant statements, incompatible transition descriptions, exact bundle drift, missing adoption rows, review cycles caused by contract ambiguity.

### C-04 — Protocol and recovery layering
COC log, Prepared XID, local owner gates, single-use receipts, recovery cutoff manifests and Adapter ACK evidence can be individually justified. The unresolved question is whether all layers are needed for the selected v1 physical topology.

**Candidate reduction:** do not reopen the Storage L1 ADR, which selects Option A: one SERIALIZABLE transaction domain and per-BrainAuthorityRef serialization anchor. Reduce complexity by validating whether the actual DB/adapter can satisfy that selected topology with the smallest schema and transition set. Option B (separate services/coordinator) is only a successor-ADR path if Option A cannot meet L4; it is not a parallel v1 option. COC and I sequencer remain independent authorities.

Evidence: number of independently durable state stores, cross-store reconciliation paths, recovery procedures, operational roles, fault cases and p95 write latency.

### C-05 — Retrieval index proliferation
Lexical, vector, temporal, graph and structured channels may each be justified by distinct query needs. But multiple engines and copies multiply consistency and Forget invalidation paths.

**Candidate reduction:** start with PostgreSQL structured + Tantivy lexical and defer Qdrant until vector recall/latency evidence demands it. This is a candidate deployment profile, not a semantic decision.

Evidence: recall@k, nDCG, latency, index freshness, storage footprint, filtered-query cost, rebuild duration and per-target Forget coverage.

## 3. Do not simplify by

- Replacing multiple typed cursors with one integer.
- Making one universal Memory object for Fact/Claim/Event/Entity/Procedure before B's ADR.
- Moving all resource decisions into G or all runtime logic into F.
- Treating Context Remove as canonical Forget.
- Treating tombstone as physical erasure.
- Treating queue deletion/lease expiry/DLQ as producer terminality.
- Letting LLM output directly update canonical state.
- Adding a new distributed coordinator before demonstrating a transaction boundary that needs one.

## 4. Measurement framework

Use the same workload and acceptance criteria for baseline and candidate:

| Category | Metrics |
|---|---|
| Structural | number of persisted state machines, schemas, adapters, services, queues, indexes, owner-owned interfaces |
| Coordination | cross-owner decisions per workflow, exact-version adoption checks, review round trips, unresolved dependency count |
| Correctness | counterexamples, invariant violations, stale visibility, unknown-to-success conversion, restore rollback |
| Runtime | p50/p95/p99 latency, CPU, RSS, disk IO, VRAM, queue age, cancellation delay |
| Retrieval | recall@k, nDCG, precision under Scope filters, index freshness, rebuild time |
| Compiler | deterministic replay rate, IR validation failure, provenance completeness, recompile fan-out |
| Context | token waste, truncation, sufficiency accuracy, stale Applied rate, reconcile duration |
| Operations | setup steps, components, backup/restore steps, failure domains, recovery time, operator actions |

No complexity-reduction percentage is claimed until baseline and candidate values exist.
