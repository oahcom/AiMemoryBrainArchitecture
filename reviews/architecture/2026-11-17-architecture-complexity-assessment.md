# Architecture Complexity Assessment
# X — Principal Architecture Complexity Assessment

- Assessment ID: X-ACA-2026-11-17
- Version: 1.0
- Status: **INDEPENDENT DESIGN-LEVEL ASSESSMENT — NOT AN OWNER APPROVAL, CONTRACT FREEZE OR IMPLEMENTATION SIGN-OFF**
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Main baseline: `b372b62c640a2b656e54b6db62a4ee67d7d8c001`
- Assessment branch: `review/architecture-complexity-assessment-2026-11-17`
- Date: 2026-11-17
- Role: X — Principal Architecture Complexity Assessment
- Language peer: [中文版本](2026-11-17-architecture-complexity-assessment-zh-CN.md)

## 1. Executive verdict

**Overall implementation, verification and long-term maintainability feasibility: NOT PROVEN.**

The architecture is not simply “large”. Its dominant cost is the composition of independently owned state machines and proof obligations across canonical memory, compiler admission/publication, retrieval/indexing, Context delivery, Adapter application, identity/authorization, Forget, Storage visibility, COC and restore.

The design contains necessary correctness costs: provenance, scope-first authorization, immutable versioning, typed causal positions, idempotent durable acceptance, Forget anti-resurrection, final inference-boundary evidence, and fail-closed recovery. These must not be removed to improve a score.

The primary complexity multiplier is that one business operation may cross several authorities, each with its own state, epoch, cursor, evidence, retry and recovery rules. A second multiplier is exact-version governance across many mutable Owner branches and chained protocol amendments. A third is that several crucial contracts are still candidates or open, so the eventual implementation may need to encode semantics that are not yet fully closed.

This assessment rates the *designed system and its required proof burden*, not code volume, delivery time or the quality of any individual Owner. Scores are ordinal risk indicators, not additive project totals.

### Decision summary

| Question | Assessment |
|---|---|
| Can the architecture be implemented as currently composed without further simplification? | NOT PROVEN |
| Is the logical modular-monolith direction viable? | CANDIDATE; strongly preferable to early microservices |
| Are correctness-critical complexity costs avoidable? | No; several are fundamental |
| Is there demonstrable over-engineering? | Some governance/versioning and protocol-surface proliferation risks; not enough evidence to label core safety invariants unnecessary |
| Is the current test burden bounded and executable end-to-end? | NOT PROVEN |
| Is operational topology settled? | No; Storage topology ADR is BLOCKED |
| Is a small team likely to sustain all current workstreams in parallel? | High risk without strict sequencing and a narrow first-release envelope |

## 2. Evidence baseline and limits

### 2.1 Live source pins

| Source | Branch / ref | Exact revision or Blob | Assessment use |
|---|---|---|---|
| Main | main | Commit `b372b62c640a2b656e54b6db62a4ee67d7d8c001` | Repository baseline and governance |
| D | `session-d-memory-brain-2026-11-16` | HEAD `97e68fbd225bdf0ac71860c01077481afc162d50`; Forget contract Blob `1f0391bc49d007c44ec74165bd33d37412cc7990`; cursor Blob `4688a0ca487bf4d853c7f0220408abe8d743d159` | Canonical authority, fence, cursor |
| E | `session-e-memory-compiler-2026-11-16` | HEAD `fdb4f67a83083d995930b88f93975b5ee36080f3`; Forget contract Blob `00e37ba56596e710513c8d0568acd79141d9101b`; Accepted contract Blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46` | Ingress, work lifecycle, publication |
| F | `session-f-memory-runtime` | HEAD `8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3`; Retrieval Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`; Forget addendum Blob `ce59252dbbdc5d10d016704797e9ba12d5a941bd` | Retrieval, index, cache, anti-resurrection |
| G | `session-g-memory-context` | HEAD `f9ca0ddc36e17f74041506f17039f0202d13042e`; version Blob `05c0739d0c22576a1fd5affc7d73c078c89049b1`; reconciliation Blob `87063aceebed1c30b7840045ada8e3f348732688` | Context state and reconciliation |
| H | `session-h-bmcp-protocol` | HEAD `6eb1816f3a17b68422f55848cc722c76b835d9a1`; Applied contract Blob `ed6b43a29aa368d772c701ffc83309a5aadf3c00`; delivery Blob `bf9732cc39d156853b507c3a3a4e573159978f49` | Protocol, Adapter and Applied |
| I | `session-i-security-governance-2026-11-16` | HEAD `3f29dbc4dffb99c16ab1d3197e2f5fb8207ebe2f`; inventory Blob `9100061fa986fb6676656169de3fcf9fc1c72664`; identity Blob `03765efac4bb1153f303ce0030f9e277d602e81d` | Identity, policy and Global Forget |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | HEAD `17be31915b06d98d7f822e6e5270b8cde39eb0bb`; topology ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`; visibility contract Blob `175ee7b1349cfdb79a19898b311a88391ed88010`; v3.2.5 binding manifest Blob `bea90697e7a61d43bed00543d636a5cdf40cf5ca` | Storage/COC/restore |
| C | `session-c-agent-integration-2026-11-16` | HEAD `9d4301b056fd72f683bdcfeceaa262f21e991051` | Agent boundary; current source package not fully re-read in this assessment |
| A | `session-a-integration-2026-11-16` | HEAD `d72dbac6e0f739cd00ac986176b78ec5cd385d88` | Integration and coordination; current source package not fully re-read in this assessment |
| PR #28 | `docs/bilingual-coverage-completion` | HEAD `365726ac4ac9f16c935eb4b23f88411b4ecc0fc4` | Pending bilingual migration scope and known gaps |

The Owner branch heads are live refs read during this assessment. Blob pins identify the exact individual source documents read. This is a bounded source sample, not a claim that every file on every Owner branch was reviewed.

### 2.2 Repository integration facts

- Main's recursive tree contains 82 files. Detailed D/E/F/G/H/I/Storage source packages are not all integrated into main; their existence on Owner branches must not be confused with main integration.
- PR #28 is Draft/Open and explicitly says it adds paired source-aligned documentation while leaving Owner source specifications unchanged. It also explicitly disclaims full 136-file semantic parity sign-off.
- PR #28 records C/G/H Applied freeze BLOCKED, I governance BLOCKED, Storage topology ADR-BLOCKED, and JF-10 P0 OPEN / NOT IMPLEMENTED / NOT RUN.
- The bilingual coverage register marks many detailed Owner specifications as NOT STARTED for translation. A reader guide is not a normative Owner contract.
- Main branch protection was observed disabled at assessment time. This is a governance/operational exposure, not a claim that source design semantics are wrong.
- Issue #43 is open and defines architecture consolidation/feasibility review boundaries. Its non-claims and authority rules are preserved here.

### 2.3 Evidence limitations

No production implementation, complete end-to-end conformance campaign, representative workload benchmark, production topology, or small-team delivery trial was verified. Several branch-local reviews identify themselves as static or simulated review lenses rather than independent external sign-offs. No score below should be interpreted as measured runtime complexity.

## 3. Scoring model

Eight dimensions are scored independently for each module and cross-module mechanism:

1. **I — Internal Complexity:** internal responsibilities, algorithms, object model and local rules.
2. **D — Dependency Complexity:** number and strength of external contracts required to behave correctly.
3. **S — State Complexity:** state objects, transitions, epochs, revisions and lifecycle combinations.
4. **C — Concurrency Complexity:** races, admission, ordering, locking, linearization and duplicate work.
5. **R — Recovery Complexity:** crash windows, replay, restore, reconciliation and unresolved outcomes.
6. **V — Verification Complexity:** tests, evidence, proof predicates and independent acceptance.
7. **O — Operational Complexity:** deployment, data services, backup, monitoring, failover and human operations.
8. **K — Cognitive Complexity:** cross-owner understanding, source pinning, documentation and change propagation.

Scale: 1 Low; 2 Moderate; 3 Significant; 4 High; 5 Extreme. A 5 means the design has an extreme burden or unresolved risk in that dimension; it does not mean the design is defective.

A score is accompanied by evidence, amplification factors, simplification opportunities, non-removable correctness constraints and confidence. Do not sum scores or compute an arithmetic “system complexity” total.

## 4. Module Complexity Matrix

Dimension order: **I / D / S / C / R / V / O / K**.

| Module / authority | Scores | Principal evidence and reason |
|---|---:|---|
| B — Domain Model | 4/4/5/3/3/4/2/5 | Distinct Event/Memory/Fact/Claim/Entity/Relation/Evidence semantics; temporal and epistemic status; typed ActorRef/ScopeRef dependencies. Fact/Claim remains ADR-BLOCKED, so identity/schema coupling is unresolved. |
| C — Agent Integration | 4/5/4/4/4/5/3/5 | Telemetry, Adapter identity, inference-boundary integration, provider outcome and actual final-request evidence. C/G/H Applied depends on three authorities and cannot be inferred from transport ACK. Confidence medium-low: current C branch source was not sampled in depth. |
| D — Canonical Memory | 5/5/5/5/5/5/4/5 | Canonical lifecycle, identity, aggregate revisions, global per-authority CanonicalCommitCursor, per-Memory lifecycle cursor, ForgetOperation/Fence, producer registry/high-water and dependency lineage. |
| E — Memory Compiler | 5/5/5/5/5/5/4/5 | Durable Accepted receipt, compile intent, work/attempt/lease identities, staged derivatives, dependency registration, publication gate, DLQ/replay and separate receipts. D/Storage atomic operation remains OPEN. |
| F — Memory Runtime | 5/5/5/5/5/5/4/5 | Structured/entity/full-text/vector/graph/temporal/provenance retrieval; scope-before-candidate; per-partition watermarks; final revalidation; cache/Working Set isolation and anti-resurrection. |
| G — Memory Context | 5/5/5/5/5/5/4/5 | Immutable ContextVersion, CAS/serialization, ChangeSet, delivery/session state, reconciliation triggers, stale/blocked states, per-consumer Applied history and Forget invalidation. |
| H — BMCP / Adapter | 5/5/5/5/5/5/4/5 | Versioned envelopes, identity binding, capability epochs, Snapshot/Delta, reconnect, delivery ACK taxonomy, cryptographic evidence and final-request Applied tiers. Multiple schema/recovery revisions increase compatibility and exact-pin burden. |
| I — Security & Governance | 5/5/5/5/5/5/5/5 | Principal/issuer/delegation, scope binding, PermissionEpoch, revocation sequencing, closed-world producer/recipient inventory, target seal, Global Forget proof, backup and physical-erasure exceptions. |
| Storage / Consistency / COC | 5/5/5/5/5/5/5/5 | Durable hidden participants, prepared-XID/GID identity, D/I/Storage gates, atomic visibility/outcome, COC prefix/batches/manifests, restore high-water and split-brain fencing. Physical topology ADR remains blocked. |
| A — Integration / Governance coordination | 4/5/4/4/4/5/3/5 | Exact-version source ledger, dependency graph, Owner acceptance, cross-document parity and conformance orchestration. High coordination cost; must not become a shadow owner of module semantics. |

**Confidence:** B/D/E/F/G/H/I/Storage = medium-high for the cited source samples; A/C = medium-low. These are architecture-design scores, not implementation measurements.

### Per-module score rationale and complexity controls

The vector below gives the dimension-by-dimension basis for each module score. The earlier matrix is the compact score view; this table records why each dimension received that level and what may or may not be simplified.

| Module | Dimension score basis (I; D; S; C; R; V; O; K) | Amplifiers | Simplifiable portion | Non-removable correctness constraints | Confidence |
|---|---|---|---|---|---|
| B | I4 distinct epistemic/domain concepts; D4 B references consumed across D/E/F/G/H/I; S5 Fact/Claim + temporal/epistemic/lifecycle semantics; C3 concurrent revision/identity binding; R3 provenance and historical correction; V4 ADR/schema dependency; O2 no separate runtime proven; K5 stable terminology and bilingual semantics | Fact/Claim ADR and typed-reference decisions remain open | Consolidate glossary and typed-reference registry; defer schema variants until ADR | Distinct source Event vs Claim/Fact, provenance, time and epistemic status | Medium |
| C | I4 telemetry/Adapter/final-request responsibilities; D5 C/G/H/I/Provider/Agent coupling; S4 request/session/capability/application states; C4 final-request race with revocation/Forget; R4 offline/reconnect/late outcome; V5 actual final request evidence; O3 adapter deployment/upgrade; K5 multiple owner proofs | Provider-specific outcomes and middleware visibility | Start with one Adapter and one declared capability profile | Never infer final request submission or model use from transport receipt | Medium-low |
| D | I5 canonical lifecycle/lineage/fence; D5 E/F/G/H/I/Storage/COC; S5 objects, revisions, cursor, fence, producer barriers; C5 registration-vs-fence and final publication; R5 barrier recovery and late derivative; V5 serial-order/crash/lineage proof; O4 authoritative DB and restore; K5 many typed authorities and owner handoffs | Closed-world producers and derivative descendants | One Canonical Authority; reduce producer classes for first slice | Canonical authority, fence monotonicity, register-before-visible, fail-closed unknown | Medium-high |
| E | I5 ingestion/compiler stages and immutable artifacts; D5 D/B/H/I/F/Storage; S5 receipt/work/attempt/lease/run/artifact/publication states; C5 retries and final gate vs Forget; R5 DLQ/replay/lost ACK; V5 per-stage and cross-owner proof; O4 durable queue/blob/DB coordination; K5 many receipt distinctions | Same work identity crosses queue, lease, replay and publication | One worker substrate; defer advanced extraction/consolidation modes | Durable Accepted, stable idempotency, no visible derivative before authoritative gate | Medium-high |
| F | I5 hybrid retrieval, ranking, graph and freshness; D5 D/I/E/G/H/index backends; S5 channel watermarks/cache/session/fence/permission; C5 revocation/Forget during query/rerank; R5 rebuild/replay/cache anti-resurrection; V5 per-channel isolation and stale-state tests; O4 index/cache lifecycle; K5 many channels and authorization checkpoints | Multiple retrieval channels each duplicate security/freshness checks | Structured + lexical first; no distributed cache | Scope-before-candidate, current authorization/fence at disclosure, index is not authority | Medium-high |
| G | I5 context planning, versioning, reconciliation; D5 C/D/E/F/H/I; S5 ContextVersion/ChangeSet/Delivery/Applied/consumer state; C5 CAS and concurrent edits/late ACK; R5 offline consumer and restore/reconciliation; V5 Applied predicate and per-session evidence; O4 delivery persistence and adapter operations; K5 several overlapping but distinct version axes | Per-consumer Applied history plus many reconciliation triggers | One Context type and one consumer profile initially | Immutable desired version, CAS/serialization, Applied distinct from delivery, stale entries blocked | Medium-high |
| H | I5 envelope, negotiation, ACK, attestation and recovery schemas; D5 C/G/I/D/Storage/COC; S5 protocol versions, capabilities, delivery, participant and recovery states; C5 retry/reconnect/order/commit gates; R5 unknown ACK, replay, recovery cutoff; V5 schema/parser/crypto/interop vectors; O4 key/adapter lifecycle; K5 exact schema and bundle pins | Schema family evolution and cryptographic trust coupling | Generate schemas/validators from canonical definitions; constrain first profile | Strict parsing, authenticated identity binding, no Full Applied below required evidence tier, typed opaque refs | Medium-high |
| I | I5 identity/trust/authorization/retention/global proof; D5 all producer, consumer, storage and external domains; S5 epochs, inventory seals, gates, exceptions, proof vectors; C5 authorization/revocation and inventory races; R5 backup/restore/recipient reconciliation; V5 trust/negative/global evidence; O5 key lifecycle, operators, backup and external recipients; K5 broad governance ownership | Closed-world inventory expands with every producer, recipient, backup and restore target | One PolicyDomain and finite target classes; defer external-recipient breadth | Authenticated issuer, least privilege, revocation, unknown blocks, global/physical completion evidence | Medium-high |
| Storage / COC | I5 prepared participant, atomic visibility, COC and restore protocol; D5 D/I/C/H/E/COC; S5 participant/XID/GID/prefix/batch/manifest/restore states; C5 serialization and same-XID resolution; R5 crash, ACK loss, quorum loss, failover/PITR; V5 physical DB and application-level fault campaign; O5 DB/COC/HA/backup/on-call; K5 multiple immutable protocol versions and exact bundle pins | Two-phase participant protocol, COC quorum and owner-local gates | One transaction domain; defer distributed coordinator until evidence demands it | Same participant identity, atomic visibility/outcome, UNKNOWN retains barriers, restore quarantine | Medium-high |
| A | I4 integration registry/sequence/conformance orchestration; D5 every Owner and exact branch; S4 source status and evidence lifecycle; C4 concurrent branch evolution and stale pins; R4 supersession/re-review after source changes; V5 independent owner evidence and parity; O3 governance controls; K5 global coordination | Source drift and coordination register staleness | One manifest and generated indexes; avoid duplicate normative summaries | Owner authority remains local; no inferred acceptance or stale source approval | Medium-low |

### Per-mechanism score rationale and controls

| Mechanism | Score basis (I; D; S; C; R; V; O; K) | Amplifier | Simplifiable portion | Must remain | Confidence |
|---|---|---|---|---|
| E/D/Storage publication | 5 operation stages; 5 three authority dependencies; 5 work/fence/participant/outcome states; 5 competing linearization; 5 crash/lost-ACK; 5 race proof; 4 one DB topology; 5 cross-owner semantics | Admission and visibility are separate durable authorities | Collapse physical serialization into one transaction domain if Owner-approved | Final gate rechecks current fence and I proof; no staged visibility | Medium-high |
| Global Forget | 5 inventory/proof algorithm; 5 six+ owners; 5 independent epochs and local ACKs; 5 new producer/recipient races; 5 offline/restore; 5 global evidence; 5 external backup/operator; 5 global reasoning | Inventory grows with every copy/consumer/restore path | Bound first-release inventory and policy domain | Unknown is not success; suppression/cleanup/erasure remain distinct | Medium-high |
| C/G/H Applied | 4 adapter assembly; 5 three owners plus I; 5 per-delivery/session/request state; 4 late ACK/revocation; 4 offline/reconnect; 5 actual final request proof; 3 one adapter ops; 5 proof semantics | Capability tiers can overstate what an adapter can observe | One adapter profile and narrow managed region | Full Applied only with exact final submission evidence | Medium |
| JF-10/COC | 5 distributed participant protocol; 5 C/D/I/H/Storage/COC; 5 participant/XID/prefix/gate; 5 serial order and quorum; 5 same-XID recovery; 5 deterministic fault campaign; 5 production ops; 5 exact bundle governance | Prepared DB transaction plus separate coordinator and owner ledgers | Defer COC deployment or constrain to one proven topology | No heuristic resolution; same-XID; UNKNOWN holds barriers | Medium-high |
| Typed positions | 4 type registry; 5 consumers; 5 distinct position semantics; 4 ordering mistakes; 5 replay/gap recovery; 5 type misuse tests; 3 runtime operations; 5 cognitive namespace load | Similar-looking integer/version fields invite accidental coercion | Central registry and code generation | Nominal type distinction and authority-owned comparison | Medium-high |
| Restore | 5 reconciliation protocol; 5 DB/COC/I/D/Storage/Owner; 5 epochs/prefix/participant/seal; 5 stale primary/rollback race; 5 partial restore; 5 negative evidence; 5 operators/DR; 5 evidence interpretation | Data plane can be restored without control plane | One restore topology and automated manifest verification | Start fenced; no serve until independent ledgers and owners release | Medium-high |
| Bilingual governance | 3 document process; 5 owners/branches; 4 source and translation states; 2 runtime races; 3 supersession/re-review; 5 semantic parity; 3 CI/review ops; 5 human cognitive load | Guides mistaken for normative source and stale Blob pins | One paired report/manifest; structural automation | Semantic parity, stable IDs, exact source revision and authority status | High |

Confidence describes confidence in the score based on the cited source sample, not confidence that the module is correct or implementation-ready.


### Module findings

- **Highest intrinsic state burden:** D, E, G, H and I. Their local state machines are individually large even before cross-module composition.
- **Highest concurrency/recovery burden:** D, E and Storage, followed by I and G. The critical races are not ordinary request concurrency; they determine whether forgotten or unauthorized data can become visible.
- **Highest cognitive burden:** I, H, Storage and A. Their evidence and protocol revisions require understanding multiple authority namespaces and exact-version dependencies.
- **Highest retrieval-specific burden:** F. Hybrid retrieval itself is not the only cost; authorization must precede candidate exposure and be rechecked through fusion, reranking, materialization and return.
- **Highest integration dependency:** C/G/H Applied and D/E/Storage publication. Neither is safely implemented by treating another module's ACK as proof.

## 5. Cross-module Complexity Matrix

Dimension order remains **I / D / S / C / R / V / O / K**.

| Cross-module mechanism | Scores | Why it exceeds a local module |
|---|---:|---|
| E admission × D Forget Fence × Storage visibility | 5/5/5/5/5/5/4/5 | Producer class/work registration, fence snapshot/high-water, dependency edge, hidden prepare, final fence recheck, visibility pointer and immutable outcome must share a defensible linearization model. |
| Global Forget D/E/F/G/H/I/Storage | 5/5/5/5/5/5/5/5 | I domain inventory/seal + D work-item barrier + local owner watermarks/ACKs + Adapter/offline state + backup/restore/external recipients; no local ACK proves global completion. |
| C/G/H final-request Applied | 4/5/5/4/4/5/3/5 | Exact ContextVersion, delivery attempt, Adapter capability, authenticated identity, scope, permission epoch, Forget fence, managed-region digest and actual submitted inference request must bind. |
| JF-10 / COC / Storage prepared participant | 5/5/5/5/5/5/5/5 | COC quorum prefix, immutable participant tuple, GID/native XID/DB incarnation, I terminal decision, same-XID resolution, owner outcomes and atomic visibility receipt; UNKNOWN holds barriers. |
| Typed causal positions and freshness vector | 4/5/5/4/5/5/3/5 | CanonicalCommitCursor, AggregateRevision, LifecycleEventCursor, IndexWatermark, ForgetFenceGeneration, PermissionEpoch, ContextVersion, AdapterCapabilityEpoch and producer high-water are non-interchangeable. |
| Restore / backup / split-brain recovery | 5/5/5/5/5/5/5/5 | Restore quarantine, WAL/timeline continuity, old-primary fencing, COC prefix, I/D ledgers, inventory seal, prepared participants and owner-local gate release must reconcile before serving. |
| Bilingual source and exact-version governance | 3/5/4/2/3/5/3/5 | Paired docs, stable identifiers, source branch/commit/Blob pins, supersession and independent Owner review. This is governance complexity rather than runtime complexity. |

### Cross-module assessment

The system's dominant complexity is **protocol composition**, not module count. A workflow is safe only when all relevant authorities agree on the same immutable operation/participant identity, exact scope, current epochs, causal cutoffs, terminal disposition and evidence. If one component advances while another is stale or unknown, the correct result is often to block, quarantine or reconcile—not to guess.

## 6. State-space Complexity Analysis

### 6.1 State axes that combine

At minimum, critical workflows combine the following independent state dimensions:

- Identity: issuer, Principal, ActorRef, producer/recipient instance and trust/key status.
- Scope: tenant/user/project/Agent/instance/task/session/environment and purpose.
- Canonical state: object identity, aggregate revision, lifecycle state and CanonicalCommitCursor.
- Compiler state: Accepted, Registered, Queued, Leased, Running, Staged, DependencyRegistered, Published, CanonicalCommitted, Retry, DeadLettered and Terminal.
- Forget state: operation, target inventory, fence generation, producer high-water, dependency coverage, suppression, cleanup and residual exception.
- Runtime state: index/channel/partition watermark, coverage/schema version, cache/Working Set generation and in-flight query/rerank.
- Context state: ContextVersion, ChangeSet, reconciliation state, delivery attempt and consumer/session applied version.
- Storage/COC state: private prepare, participant identity, prepared transaction, quorum prefix, I decision, Storage outcome, visibility pointer and restore gate.
- Time/failure state: crash point, lost ACK, duplicate delivery, stale lease, delayed event, offline recipient, replay, rollback and unknown outcome.

These axes are not all one global state machine. They are independent owner-local machines whose cross-product appears at integration boundaries. A numeric total of possible states cannot be responsibly calculated from current artifacts: the full finite state domains, legal transitions and equivalence reductions have not been closed. **Exact state-space cardinality: NOT PROVEN.**

### 6.2 Highest-risk combinations

1. Producer registration wins vs Forget fence wins, followed by a crash before dependency registration or publication.
2. Storage hidden prepare succeeds but ACK is lost; D admission and retry must resolve the same immutable participant.
3. I authorization/revocation changes between initial check and final visibility commit.
4. Index watermark is behind while canonical Forget fence has advanced; candidate must not leak through fusion, cache or graph expansion.
5. Context delivery is applied locally but final inference submission is not proven; no Full Applied.
6. Adapter is offline during Forget, later reconnects with stale queue/cache and attempts replay.
7. Restore rolls data back behind a control-ledger high-water or inventory seal; system must remain RESTORE_FENCED.
8. COC quorum is lost with unresolved prepared participants; UNKNOWN/IN_DOUBT must retain locks/barriers and cannot be resolved by TTL.

### 6.3 Correctness constraints that must remain

- Fail closed on unknown identity, permission, fence, lineage, cursor gap, participant outcome or restore proof.
- Never infer one authority's state from another authority's ACK.
- Never compare or coerce typed cursors/epochs across namespaces.
- Never expose staged data before final visibility commit.
- Never treat DLQ, lease expiry, timeout or missing ACK as terminal success.
- Never infer Applied from Delivered, materialization alone or Adapter capability declaration.
- Never claim global/physical Forget completion from canonical suppression or local cleanup.
- Never serve restored data until independent control ledgers and owner gates reconcile.

### 6.4 Simplification without weakening correctness

Use one authoritative owner per state machine; define one minimal immutable cross-module tuple; expose a small number of typed boundary operations; keep derived indexes and caches disposable; and centralize the physical linearization point for a bounded first deployment. Do not duplicate policy logic in each consumer. Consumers must enforce owner-issued decisions, not reimplement the authority's decision rules.

## 7. Complexity Hotspot Register

| ID | Hotspot / multiplier | Severity | Evidence / impact | Required action |
|---|---|---|---|---|
| XH-01 | D/E/Storage producer-fence-publication linearization | P0 | D semantics exist; E explicitly says atomic registration/final gate OPEN; Storage topology ADR has no selected option | Close exact operation, transaction boundary, retry/unknown semantics and race/crash proof before implementation |
| XH-02 | Global Forget closed-world inventory | P0 | I inventory epoch/seal differs from D per-work barrier; F/G/H/Storage/backup/external targets | Bound first release to one PolicyDomain and a declared finite producer/recipient set; unknown remains blocking |
| XH-03 | JF-10 + persistent COC + prepared-XID | P0 | Storage v3.2.5 manifest is published but not jointly accepted/frozen; topology ADR blocked; Gate A partial; Gate B/C implementation deferred/not run | Keep one-domain scope; do not activate distributed topology until exact-owner acceptance and engineering proof |
| XH-04 | Applied proof across C/G/H | P1 | Full Applied requires final request submission evidence and complete identity/scope/epoch/fence binding; H tiers 2/3 cannot emit Full | Choose one supported Adapter profile for first slice; otherwise report Delivered/Unknown, never Full Applied |
| XH-05 | Typed cursor/epoch proliferation | P1 | At least nine distinct namespaces in the source contracts | Maintain one registry and typed wrappers; prohibit generic integer/version fields and cross-domain arithmetic |
| XH-06 | Schema and exact-version churn | P1 | H has a sequence of unified COC/JF-10 schemas 1.2.0–1.2.13 and RecoveryCutoff 1.0.0–1.0.5 / RecoveryJoin 1.0.0–1.0.2; Storage v3.2.3 plus successor binding manifests | One canonical current-version manifest; retire stale pins explicitly; generate compatibility tests from schemas |
| XH-07 | Restore and rollback proof | P0 | Storage reference tests are logical models; production control-ledger, old-primary fencing, deployment and operational evidence remain separate | Keep restore quarantined until WAL, COC, I, D, inventory, participant and owner-release evidence reconcile |
| XH-08 | Retrieval channel × authorization × cache | P1 | F supports structured/entity/lexical/vector/graph/temporal/provenance paths; each has pre-exposure policy requirements | Start with structured + lexical; defer vector/graph expansion until corpus and scope-isolation tests justify it |
| XH-09 | Bilingual + Owner source integration drift | P1 | Main has guides but not all detailed Owner contracts; PR #28 is still Draft and does not claim full parity | Make source integration, translation parity and semantic approval explicit separate gates |
| XH-10 | Branch protection / review enforcement | P1 | Main branch API reported protection disabled | Project governance Owner to decide and verify protections; X records operational exposure only |

## 8. Complexity Budget and Thresholds

These thresholds are proposed control limits for architecture evolution; they do not rewrite Owner decisions.

### 8.1 Score thresholds

| Score | Meaning | Gate |
|---:|---|---|
| 1–2 | Low / bounded | Normal module review |
| 3 | Significant | Document owner, inputs/outputs and regression tests |
| 4 | High | Require explicit dependency map, failure model, acceptance evidence and named maintainer |
| 5 | Extreme | Must be justified as correctness-critical or explicitly approved as a bounded risk; no silent introduction; architecture gate required |

Additional controls:
- Any P0 cross-module mechanism with a 5 in concurrency, recovery or verification remains BLOCKED until its operation and proof obligations are closed.
- Any first-release component with 5 in operational complexity must be reduced to a single-node/single-authority bounded profile or explicitly deferred.
- A score reduction is accepted only when a mechanism is removed, consolidated or its proof surface demonstrably shrinks; renaming or hiding states does not reduce complexity.
- Do not use average scores. The maximum dimension and its evidence drive the gate.

### 8.2 First-release envelope (recommended)

| Area | Budget / limit | Deferred or excluded |
|---|---|---|
| Canonical authority | One Brain authority | Multi-authority global ordering |
| Security domain | One I PolicyDomain | Cross-PolicyDomain atomic Forget / publication |
| Runtime topology | Modular monolith; one process for correctness-critical state transitions | Microservices and cross-service distributed transactions |
| Storage serialization | One authoritative transaction domain per Canonical Memory authority | Option B distributed coordinator until separately justified; Option C check-then-write is rejected |
| Queue | One durable outbox/queue abstraction with bounded workers | Multiple queue products and independent replay fabrics |
| Retrieval | Structured + lexical first | Vector ANN, graph expansion and multiple independent index engines until benchmarked |
| Cache | Off initially or one bounded in-process disposable cache | Distributed cache and cross-node invalidation |
| Adapter | One declared Adapter capability profile | General multi-framework compatibility matrix in first slice |
| Forget inventory | Explicit finite producer/recipient classes; unknown blocks | Arbitrary plugin ecosystem and unbounded external recipients |
| Backup/restore | One declared backup/restore path with quarantine and owner-ledger reconciliation | Multi-region active-active and multi-policy-domain restore |
| Model inference | Separate optional resource boundary | Model inference as a prerequisite for durable acceptance or recovery |

This envelope does not choose SQLite or PostgreSQL as the final product topology. PostgreSQL 18.7 has bounded CI capability evidence; the Storage serialization topology ADR remains BLOCKED and the actual Canonical Authority deployment is not selected by that evidence.

### 8.3 Testing complexity budget

Tests must be organized around contracts and durable boundaries, not a single enormous end-to-end suite.

| Test layer | Required budget | Exit evidence |
|---|---|---|
| Domain/state-machine unit | Every owner-local transition, invariant, invalid transition and idempotent replay | Deterministic tests and state transition coverage |
| Module contract | Owner boundary inputs/outputs, authorization, version/cursor and error semantics | Consumer/provider contract suite |
| Concurrency | Both serial orders of every safety-critical race; stale lease/epoch and duplicate admission | Deterministic race harness with invariant assertions |
| Crash/recovery | Crash before/after every durable boundary; lost ACK; process restart; unknown outcome | Reproducible fault traces and same-identity reconciliation |
| Cross-module conformance | D/E/Storage, D/E/F/G/H/I Forget, C/G/H Applied, Storage/COC/JF-10 | Exact-version vector suite with owner-specific evidence |
| Restore/DR | Missing WAL/prefix, stale inventory, old-primary rejoin, partial restore, participant mismatch | Remain fenced/quarantined until complete proof |
| Security | Identity spoofing, scope confusion, revocation race, replay, key rotation/revocation, unauthorized existence leakage | Negative tests and auditable denials |
| Performance | Representative corpus, scope distribution, concurrency, model/resource profile | Reproducible benchmark; no assumed SLO |
| Regression | Every corrected P0/P1 becomes a permanent regression case | Versioned suite tied to contract IDs |

A test suite is not complete because reference-model tests pass. Logical model, database capability probe, deployed implementation conformance and production acceptance are separate evidence classes.

### 8.4 Operational complexity budget

First release should have one canonical database authority, one backup/restore runbook, one monitoring and audit pipeline, one accountable operational owner, bounded worker concurrency and explicit disk/queue/index limits. No production launch until RPO/RTO, failover fencing, restore rehearsal, backup integrity, alert ownership and recovery operator are evidenced.

### 8.5 Cognitive complexity budget

- One canonical glossary and one typed cursor/epoch registry.
- One authoritative current-source manifest per cross-module bundle.
- Each contract names one owner, consumers, source revision, status and exact acceptance evidence.
- Keep reader guides explicitly non-normative; link to owner source contracts.
- Avoid parallel duplicate summaries of the same normative state machine. Use generated indexes or concise consumer maps where possible.
- Any new state, epoch, cursor, receipt or protocol version must state which existing concept it cannot replace and why.

## 9. Simplification Recommendations

### MUST PRESERVE — correctness costs

1. Canonical Memory authority and immutable revision/provenance.
2. Scope-first authorization and current authorization recheck at protected boundaries.
3. Separate Accepted, Compiled, CanonicalCommitted, Indexed, Delivered and Applied evidence.
4. Typed cursor/epoch namespaces and authority ownership.
5. Durable idempotency, stable work identity and replay-safe state transitions.
6. Forget fence, closed-world producer inventory, dependency registration and anti-resurrection.
7. Final visibility linearization and fail-closed UNKNOWN/IN_DOUBT.
8. Adapter final-request proof boundary; no false Full Applied.
9. Restore quarantine, old-primary fencing and independent owner-ledger reconciliation.
10. Bilingual semantic parity and exact source pinning for normative contracts.

### CAN SIMPLIFY — preserve semantics, reduce mechanisms

1. Implement logical subsystems as Rust modules in one modular monolith; do not make each Owner a process, crate or deployable service by default.
2. Reuse one durable outbox/worker execution substrate for compiler and bounded background jobs, while retaining owner-specific state and authorization.
3. Keep a single canonical typed-ID/cursor/epoch registry; use nominal Rust newtypes and generated serialization rather than repeated bespoke wrappers.
4. Use one shared conformance harness with owner-specific adapters and fixtures; avoid each module inventing a separate fault harness.
5. Use one immutable cross-module operation tuple and digest profile wherever the same publication/participant identity is carried; do not re-encode identity independently at each hop.
6. Prefer canonical references over copied payloads in Working Sets, Context and caches.
7. Use one paired bilingual report with a stable manifest; avoid duplicated normative prose in multiple guides.

### CAN DEFER — not required to prove the first correctness slice

1. Vector ANN, graph retrieval and reranking until lexical/structured baselines are measured.
2. Distributed cache, multi-region active-active and multi-authority causal ordering.
3. Multi-PolicyDomain atomicity; it remains BLOCKED, not implicitly supported.
4. Broad adapter ecosystem and capability tiers beyond the first selected integration.
5. Sophisticated automatic memory consolidation and multi-model routing where deterministic/manual workflows can validate core contracts first.
6. Full production COC deployment until the single-authority publication/Forget contract and required physical topology are selected.
7. Advanced optimization, speculative prefetch and cache warming before correctness and workload baselines exist.

### REASSESS — do not silently decide here

1. Whether D and Storage can share one serializable transaction domain (Storage ADR Option A) or require a durable distributed coordinator (Option B). A is the preferred candidate only if real deployment proves it. Option C check-then-write is rejected.
2. Exact scope of the closed-world producer/recipient inventory for a first release.
3. Whether full Applied proof is in first-release scope or the first release truthfully stops at Delivered/Unknown.
4. Number of retrieval channels and index partitions justified by actual corpus/latency requirements.
5. The H schema/recovery versioning policy and whether all historical schema artifacts need to remain as active compatibility targets.
6. Operational acceptance scope, human on-call ownership and deployment boundary.

### MUST NOT INTRODUCE

1. Microservices per logical subsystem or per Owner without a measured isolation/scaling requirement.
2. A generic “version”, “sequence”, “epoch” or “cursor” field that erases authority/type boundaries.
3. A second independent source of truth for Context, Forget, authorization or publication state.
4. A local check-then-write substitute for the D/Storage linearization gate.
5. A cache/index/queue/Adapter ACK treated as canonical proof.
6. Multi-PolicyDomain or multi-region semantics before explicit design and fault proof.
7. New protocol state/receipt/version solely to paper over unclear ownership or stale source pins.

## 10. Small-team failure forecast

The most likely failure points for a small engineering team are:

1. **Trying to implement all owner packages at once.** Cross-owner contracts are not frozen and the team will encode guesses into interfaces.
2. **Implementing Forget as a background deletion job.** The hard part is producer admission and visibility linearization, not deleting rows.
3. **Treating receipts as interchangeable.** AcceptedReceipt, RegistrationReceipt, PublicationReceipt, IndexApplied, Adapter ACK and Global Forget evidence prove different facts.
4. **Building the whole retrieval stack immediately.** Vector/graph/cache complexity arrives before the corpus, quality and workload justify it.
5. **Testing only happy paths or reference models.** The important defects live in crash windows, duplicate/lost ACK, revocation races and restore rollback.
6. **Maintaining several moving source branches without a single current manifest.** Exact Blob pins and stale decisions will consume review capacity and create accidental contract drift.
7. **Underestimating operational work.** COC, prepared transactions, backups, restore fencing, key lifecycle, monitoring and human response are not incidental implementation details.
8. **Allowing AI sessions to expand architecture independently.** Without strict owner prompts, change manifests, source pins and review gates, documentation and protocol versions multiply faster than the team can validate them.

## 11. Architecture constraints arising from this assessment

These are X recommendations for governance consideration, not unilateral changes to Owner contracts:

- **X-AC-01:** First implementation slice SHOULD be a modular monolith with one Canonical Memory authority and one transaction serialization domain.
- **X-AC-02:** First release MUST declare exactly one I PolicyDomain unless a separately accepted multi-domain protocol exists.
- **X-AC-03:** Any P0 mechanism scored 5 for concurrency/recovery/verification MUST remain blocked until its operation contract and executable proof plan are accepted by its authorities.
- **X-AC-04:** No module may claim a cross-module terminal state from another module's transport or local ACK.
- **X-AC-05:** Typed cursors/epochs MUST remain nominally distinct in schema, code and tests.
- **X-AC-06:** First retrieval slice SHOULD use structured + lexical search; additional channels require measured quality/latency justification.
- **X-AC-07:** Full Applied MUST remain unavailable unless C/G/H final-request proof predicates are satisfied; otherwise report the narrower actual delivery state.
- **X-AC-08:** Restore MUST start fenced/quarantined and may serve only after current control-ledger and owner proof reconciliation.
- **X-AC-09:** Every new protocol version, state, epoch, cursor or receipt MUST identify the exact compatibility need and supersession path.
- **X-AC-10:** Complexity score changes MUST cite a removed/merged mechanism or reduced proof surface; no score-only optimization is accepted.

## 12. Prioritized simplification and closure sequence

| Priority | Work | Accountable authority | Why this order |
|---|---|---|---|
| P0-1 | Close D/E/Storage register-fence-dependency-final-publication operation and race semantics | D, E, Storage; A coordinates | Central safety/visibility path |
| P0-2 | Bound I producer/recipient inventory and single-PolicyDomain first-release scope | I with D/E/F/G/H/Storage | Makes Forget scope finite and testable |
| P0-3 | Select Storage serialization topology and define exact deployment boundary | Storage, D, I; A coordinates | No implementable atomicity without it |
| P0-4 | Close JF-10/COC same-participant, same-XID and restore gates or explicitly defer COC | Storage, A, I, D, C, H | Prevents accidental distributed deployment |
| P1-1 | Freeze typed cursor/epoch registry and consumer conformance | D authority; E/F/G/H/I consume | Stops semantic type drift |
| P1-2 | Decide C/G/H Applied first-slice scope and exact proof boundary | C, G, H, I | Avoids false application claims |
| P1-3 | Integrate exact Owner source manifests and bilingual detailed contracts | A + each Owner | Makes review and implementation baselines reproducible |
| P1-4 | Build shared contract/race/crash/restore test harness | A coordinates; each Owner supplies oracle | Reduces duplicated verification infrastructure |
| P2-1 | Benchmark retrieval channel additions and model resource needs | F, Engineering | Adds only justified channels |
| P2-2 | Validate production operations, backup/restore, monitoring and on-call | Storage, I, Engineering/operator | Needed before deployment, not before logical design closure |

## 13. Final answer

**Is the current architecture within an implementable, verifiable and maintainable range?**

**NOT PROVEN.**

The logical modular-monolith direction is a credible way to contain complexity. The current complete design, however, combines several extreme cross-module protocols and has not yet demonstrated an executable end-to-end proof path, a selected Storage topology, bounded operational ownership or sustainable small-team verification.

The architecture can become manageable only if the first release is deliberately narrow, the correctness-critical cross-module linearization and recovery contracts are closed before coding, and optional retrieval/distribution/automation capabilities are deferred. Reducing the number of modules or deleting correctness states is not an acceptable simplification.

---

## Appendix A — Source interpretation notes

- The main-branch absence of detailed Owner source files is an integration visibility fact, not a design-quality verdict on those Owner branches.
- Branch-local conditional passes and simulated review lenses are not independent approval.
- PostgreSQL 18.7 capability CI results are bounded engine/profile evidence; they do not select the production topology or prove the whole D/I/Storage/COC application path.
- Logical reference-model tests are not physical implementation or production recovery proof.
- PR #28's bilingual structural checks are not full semantic parity or architecture acceptance.
- No implementation effort estimate is derived from complexity scores.

## Appendix B — Key source links

- [Issue #43 — System-wide Architecture Consolidation & Feasibility Review](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)
- [PR #28 — Bilingual architecture coverage migration](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/28)
- [D — Forget Fence and Completion Contract](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-d-memory-brain-2026-11-16/03-memory-brain/forget-fence-and-completion-contract.md)
- [E — Forget Fence and Derived Registration](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-e-memory-compiler-2026-11-16/04-memory-compiler/forget-fence-and-derived-registration.md)
- [F — Runtime Forget Suppression](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-f-memory-runtime/05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md)
- [G — Context Versioning](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-g-memory-context/06-memory-context/context-versioning.md)
- [H — Adapter Applied Attestation](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-h-bmcp-protocol/08-bmcp-protocol/adapter-capability-and-applied-attestation.md)
- [I — Global Forget Inventory](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-i-security-governance-2026-11-16/09-security-governance/global-forget-target-inventory-and-completion-evidence.md)
- [Storage — Serialization Topology ADR](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-storage-consistency-forget-atomicity-2026-11-16/reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md)
- [Storage — v3.2.5 Exact-Version Binding Manifest](https://github.com/oahcom/AiMemoryBrainArchitecture/blob/session-storage-consistency-forget-atomicity-2026-11-16/reviews/storage-consistency/phase-3.6.15-storage-v3.2.5-protocol-bundle-exact-version-manifest.md)
