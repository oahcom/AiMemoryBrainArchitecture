# Memory Context Architecture

**Status:** DECIDED boundaries; CANDIDATE internal model; OPEN cross-module wire details  
**Owner:** Session G — Memory Context Manager  
**Baseline:** A/B/C and Phase-1 integration review, 2026-11-16

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
