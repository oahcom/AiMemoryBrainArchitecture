# Memory Context Architecture

**Status:** DECIDED boundaries; CANDIDATE internal model; OPEN cross-module wire details  
**Owner:** Session G — Memory Context Manager  
**Baseline:** A/B/C and Phase-1 integration review, 2026-11-16

Requirement IDs `CA-01`..`CA-02` are stable references for the 2 MUST
occurrences in this document. They are labels only; the normative text is
unchanged. Other documents SHOULD cite `CA-nn` rather than a section number,
because section numbers drift.

## 1. Purpose and authority

Memory Context is the Brain-owned, scoped, versioned working view of selected Canonical Memory assets for a particular Agent execution context. It is a managed memory region, not a prompt, not the complete Memory Store, and not the Agent's private working state.

The Brain is authoritative for Context membership, ordering, qualification, expiry, budget policy and version history. The Adapter is authoritative only for what it actually materialized at a particular inference boundary and the evidence it can attest to. The Agent remains authoritative for reasoning, planning, action selection, tool execution and safety policy.

## 2. Three-layer architecture

| Layer | Authority | Contents | Mutation |
|---|---|---|---|
| Canonical Memory | Brain canonical domain (D) | Immutable Memory versions, Claims, Entities, Relations, Evidence/Provenance, lifecycle and permission metadata | Governed canonical operations only |
| Memory Context | Brain Context Manager (G) | Scoped entries referencing authorized canonical versions or governed renderings; ordering, activation rationale, validity, budget and version history | G-owned Change Sets |
| Applied Context | Adapter attestation, coordinated by G/H | Delivery and target Context Version installed in managed region at a specific inference boundary, with coverage/evidence | Adapter applies; Brain records attestation |

A Context Entry is a reference/presentation, not a second canonical authority. Materialized content is a bounded projection. Its hash and source references support audit; they do not grant permission to dereference canonical sources.

## 3. Context identity and Scope

A Context binds to resolved, immutable identity references:
- tenant/user or owning principal scope;
- project/workspace scope where applicable;
- agent_id and agent_instance_id;
- session_id and task_id when applicable;
- environment_id whenever any selected memory or task semantics depend on a world, save, simulation, tenant or workspace;
- resolved Scope reference, authorization/policy epoch and Context purpose/profile.

Environment identity is mandatory for environment-dependent Context. Missing, ambiguous or reused environment identity fails closed. A new task does not silently inherit another task's Context; inheritance must be explicit and authorized.

The generic Scope and principal binding schema belongs to B/I/H. G stores resolved opaque references and rechecks authorization at read, plan, mutation, delivery, replay and reconciliation. Agent-supplied Scope claims are hints, never authority.

## 4. Priority tiers

| Tier | Meaning | Inclusion rule |
|---|---|---|
| P0 Core Context | Stable, high-importance task/environment facts, identity anchors and invariants | Authorized, currently valid, strongly supported entries; never Agent policy or system instructions |
| P1 Task Context | Directly task-relevant memories, active entities, recent outcomes and task state | High semantic/temporal relevance with adequate evidence |
| P2 Extended Context | Useful relations, history, alternatives, conflicts and broader entity coverage | Include when coverage gain justifies cost |
| P3 Deferred Context | Eligible but currently omitted/expensive/low-priority references | Deferred references, not materialized in current region |

Tiers are prioritization, not trust or instruction authority. P0 cannot override authorization, retraction, expiry or Agent policy.

## 5. Logical components

- **Context Planner:** turns authorized task/telemetry and Runtime recommendations into a desired candidate plan with coverage requirements.
- **Memory Activator collaboration:** G consumes activation candidates/reasons; F owns retrieval, activation ranking, completeness and uncertainty. G revalidates candidates and may defer or request more.
- **Context Editor:** validates and stages semantic edits.
- **Versioning/Committer:** serializes Change Sets, checks Base Version, enforces idempotency, creates immutable versions and deltas.
- **Context Reconciler:** detects source/policy/delivery drift and creates compensating changes or blocks use.
- **Budget Manager:** estimates token/byte/count and latency cost, evaluates coverage and compression.
- **Delivery Coordinator:** produces Snapshot/Delta delivery intents and coordinates H acknowledgements; it does not implement BMCP transport.

These are logical modules in the initial modular monolith, not mandatory services or Rust crates.

## 6. Safety invariants

1. Context carries structured memory data with source refs, provenance, trust, epistemic/lifecycle status, validity and classification.
2. Memory never becomes System/Developer instruction, user input, tool definition, tool authorization or Agent security policy.
3. Action suggestions in memory are descriptive data; they never cause Brain or Adapter to execute actions.
4. Protected prompt regions are outside the managed region and immutable to G.
5. Scope filtering and permission checks precede candidate materialization and repeat before delivery/application.
6. Context Remove only removes a Context reference. Forget is a separate governed operation invalidating all relevant Context projections and delivery paths.
7. Delivery is not application; application is not model attention, understanding, recall or behavioral use.

## 7. Independent state machines

### Context Lifecycle
Provisioning → Active ↔ Stale → ReconcileRequired → Active; terminal states are Blocked, Expired and Closed.

- **Provisioning:** scope and initial snapshot being established.
- **Active:** desired Context is valid for known revisions and policy epoch.
- **Stale:** a source, index, policy or delivery watermark is behind.
- **ReconcileRequired:** a concrete trigger/gap requires a reconcile run.
- **Blocked:** permission, Forget, scope or integrity issue prevents use.
- **Expired:** Context TTL ended.
- **Closed:** explicitly ended; no reactivation through ordinary edits.

### Context Delivery Lifecycle
Prepared → Delivered → Applied; alternative terminal states: Rejected, Expired, Superseded. This is per Delivery ID and does not determine Context Lifecycle.

### Context Entry Lifecycle
Candidate → Active → Deferred, Expired, Invalidated or Removed. Invalidated entries cannot silently resurrect; a valid successor requires a new entry or explicit replacement. Removed is membership removal, not canonical deletion.

No single status field may conflate these three lifecycles.

## 8. Forget and revocation

On Forget/revocation, G first installs a deny tombstone keyed by canonical memory identity and affected Scope; invalidates matching entries across Contexts; blocks pending Change Sets/Snapshots containing the target; invalidates Context caches; and asks H to clear/quarantine Adapter managed regions. This logical block precedes physical cleanup.

Track per Adapter/session: pending, confirmed, failed or unknown. Offline adapters remain unknown/pending and must reauthenticate, re-resolve Scope, fetch current Forget/revocation epochs, discard stale local state, apply a safe replacement Snapshot/clear set and attest before reuse.

Confirmed means the Adapter attests that its managed region/cache no longer exposes the target under its declared capability. It does not prove physical deletion from external model/provider internals or erase tokens already processed by a prior inference.

## 9. Cross-module contract

| Partner | G consumes | G provides |
|---|---|---|
| D — Canonical Brain | Memory ID/version, lifecycle, epistemic status, Entity/Relation/Claim refs, Scope/Permission | No canonical mutation; scoped usage and invalidation references |
| E — Compiler | Canonical Change Events, revision/retraction/Forget, provenance/evidence refs | Context invalidation triggers/correlation refs |
| F — Runtime | Scoped candidates, activation recommendations, completeness, uncertainty, freshness/watermark | Coverage profile and accepted/deferred/rejected candidate feedback |
| H — BMCP/Adapter | Capability, delivery receipt, Applied proof, session/request/boundary IDs | Snapshot, Delta, desired version, revocation/clear request |
| I — Governance | Authorization/revocation, classification, Forget policy | Scope use, data classification, cleanup targets and audit events |

## 10. Decision register and acceptance

- **DECIDED:** Brain owns desired Context semantics/version authority; Adapter executes at a future inference boundary.
- **DECIDED:** Context is not full prompt, full Store or Agent Working State; P0–P3 are not instruction tiers.
- **CANDIDATE:** stable Context ID per exact Scope tuple and purpose; immutable generation sequence.
- **TO_VALIDATE:** tokenization/rendering cost and tier-specific sufficiency thresholds.
- **OPEN:** generic Scope/permission schema (B/I); wire/proof fields (H/C); canonical Forget completion criteria (I).

Acceptance: negative tests prove no cross-user/Agent/instance/task/environment mixing; missing environment identity rejects environment-dependent entries; every entry resolves only through current authorization; Context edits cannot mutate canonical memory; prompt regions and tool permissions remain protected; Forget blocks active and pending delivery paths before the next inference boundary.


## 11. Phase 3.5 cross-module contract alignment

**Status:** G-owned Context semantics are DECIDED where stated below; D/E/F/H/I execution interfaces remain owner-controlled and are not frozen by this document.

### 11.1 Typed identity, scope and epoch separation

G stores resolved typed references, not caller-supplied labels or credentials. The trusted binding chain is established by I/H and typed-reference semantics by B. ActorRef and ScopeRef identify attribution/applicability; neither is a credential, grant or PolicyDecision. Payload principal, actor, producer, Agent, Adapter, session, task or environment fields are claims and must be compared with authenticated bindings.

A Context's isolation key includes the required ownership and applicability dimensions: Principal/tenant, project, Agent, Agent Instance, Session, Task and Environment. The exact required subset is declared by operation class. EnvironmentRef is mandatory whenever Context semantics or any entry are environment-dependent. Missing, ambiguous, retired or mismatched EnvironmentRef blocks use; display names never substitute. Inheritance across task/session/environment requires an explicit authorized relation and creates a separately resolved Context identity or versioned inheritance decision.

The following are distinct opaque typed namespaces. **CA-01** — G and consumers MUST NOT numerically compare, cast, increment or substitute them:

| Type | Owner | G use |
|---|---|---|
| PermissionEpoch | I | Current authorization/revocation validity |
| ForgetFenceCursor / ForgetFenceGeneration | D | Canonical suppression of a Memory identity and its lineage |
| ProducerRegistrationSequence / HighWater | D | Admission/barrier accounting for G producer work |
| CanonicalCommitCursor | D | Canonical commit ordering and reconciliation watermark |
| ProducerDomainInventoryEpoch / TargetInventorySeal / TargetId | I | Global producer/recipient inventory and target-specific evidence |
| IndexWatermark | F, per index and partition | Retrieval freshness/completeness only |
| ContextVersion | G, per Context | Desired managed-region state |
| CapabilityEpoch | H, per Adapter instance | Capability/proof profile used for a delivery/application |
| DeliveryId / DeliveryAttemptId | G | Logical delivery and one execution attempt |
| InferenceRequestId / FinalRequestBoundaryId | C/H | Exact final inference submission correlation |

A scalar applied_version is only a convenience projection. Application history is per Adapter Instance, Runtime Session, Context Session, Delivery and Inference Request.

### 11.2 G as a registered derivative producer

D's current semantic contract includes G Context membership/materializations, ChangeSets, Snapshots, Deltas and Delivery Intents in the derivative-producer inventory. **CA-02** — G MUST register its producer class and every derivative-capable work item with D before queueing, leasing, dereferencing protected canonical source payload, executing a rebuild/replay or making an artifact visible.

The G work record binds a stable ProducerWorkItemId, ProducerClass/registry version, normalized request digest, exact source Memory/MemoryVersion and transitive lineage refs, ScopeRefs, Context ID, intended artifact class, observed D ForgetFenceCursor, current I PermissionEpoch/authorization decision, and correlation/causation. Retries and lease replacement retain ProducerWorkItemId and digest; AttemptId/LeaseId identify attempts. A new derivation run is explicitly linked and re-admitted; it cannot acquire new publication rights by changing artifact ID.

For every ContextVersion snapshot, compacted projection, Snapshot/Delta package or delivery artifact that can expose canonical content, G registers complete dependency lineage with D before visibility. It then uses D's semantic final publication gate, which rechecks the latest applicable fence and current I authorization at the visibility linearization point. A prior fence read or a local check-then-publish is insufficient. If D/Storage cannot provide the callable, atomic/recoverable gate, G keeps the staged artifact private/quarantined and does not advance a visible head or create a sendable delivery. These are semantic requirements, not a claim that the current branches already expose a production API or shared transaction.

### 11.3 I inventory and target evidence boundary

I owns ProducerDomainInventoryEpoch, TargetInventorySeal, TargetId, required action, per-target state, PolicyException and global completion. D's ProducerRegistrationHighWater is a separate per-Forget work barrier. G does not mint I TargetIds, seal the global inventory, decide NotApplicable, approve exceptions or declare global Forget complete.

G supplies evidence only for its declared surfaces: Context membership/materialization, immutable snapshots, deltas, ChangeSets, delivery intents and G-owned caches/queues. Each G evidence item binds ForgetOperationId, I TargetId and inventory seal when supplied, exact ScopeRef coverage, D ForgetFenceCursor, relevant I PermissionEpoch/decision, Context/Version/ChangeSet/Delivery/attempt references, target action/postcondition, capability or schema profile where applicable, timestamp, authenticated G producer identity, integrity/audit reference and unresolved gaps. A G acknowledgement can confirm only the exact G-owned target/action slice accepted by I; it cannot imply H Adapter clearing, F cache/index cleanup, backup erasure or global completion.

### 11.4 Applied and Forget evidence are separate

H's transport receipt, local materialization, final immutable request submission and execution-start evidence are distinct stages. G accepts Delivery Applied only when C's Full Applied predicates are satisfied and H's attestation binds the exact Context ID/Version, Delivery ID/attempt, authenticated Adapter/Agent/runtime/session, Scope/Environment, CapabilityEpoch, current PermissionEpoch, applicable D ForgetFence, Managed Region inventory and exact final InferenceRequestId/FinalRequestBoundaryId evidence. Missing, stale, partial or unverifiable evidence remains Partial, Bypassed or Unknown; it is not Full Applied. Tier 2/3 and paths without final-request visibility cannot claim Tier 1 Full Applied.

Applied Attestation is not a Forget ACK. H's SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED and QUEUED_DELIVERY_CANCELLED are distinct action-specific Adapter observations. G records them as evidence for the matching target/session only; I evaluates whether they satisfy the sealed target requirement.

### 11.5 Cross-module acceptance gates

- G never emits a Context candidate from an untrusted or unresolved scope.
- No derivative-capable G work executes without D registration and current I authorization.
- No G artifact becomes visible/sendable without complete D dependency registration and final fence/permission publication gate.
- Every F candidate is revalidated by G against D canonical identity/version/lifecycle and current I permission/fence; F completeness is a per-partition vector, not a scalar maximum.
- Forget/revocation tombstones block old Context snapshots, deltas, pending ChangeSets and deliveries before cleanup; historical immutable versions are audit-only.
- Offline Adapter state remains Pending/Unknown; reconnect must authenticate, refresh I PermissionEpoch and D fence, reconcile G target/delivery state and discard stale materialization before reuse.
- No G status asserts physical erasure or model comprehension/use.
