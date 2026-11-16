# Project Baseline — AiMemoryBrainArchitecture

- Baseline ID: PB-2026-11-16
- Version: 0.1.0
- Status: **PROPOSED — NOT APPROVED; NOT ACTIVE**
- Scope: whole-project product, logical architecture, domain semantics, security, engineering and quality constraints.
- Authority: Project Governance Authority is **GOVERNANCE-OPEN**. This file proposes a project baseline and cannot approve itself.
- Source baseline: `main` @ `8a6414158c9c056c1638222534e1993d1bbc99d2`; supporting module branches and artifact SHAs are recorded in §11.

## PB-01 Product Mission

AiMemoryBrainArchitecture specifies an independent, durable, reusable, model- and Agent-independent AI Memory Brain. It preserves, structures, governs, retrieves, activates and manages memory assets and managed memory context across Agents, models, sessions and execution environments.

Primary users are Agent/application builders and operators who require continuity, traceability, portability, scoped sharing and governed memory lifecycle; indirectly, end users whose authorized memory assets are managed by those systems.

Long-term value: memory remains an owned and governed asset even when an Agent, model vendor, prompt template, framework, runtime or deployment changes. Brain is authoritative for the memory assets and managed Memory Context it owns, not for the Agent's reasoning or actions.

## PB-02 Product Scope

The Brain product scope includes:
- durable event/memory intake and compilation into candidate memory assets;
- normalization, classification, organization, consolidation and conflict preservation;
- canonical memory identity, versioning, lifecycle, entity and relationship management;
- evidence, provenance, temporal and epistemic qualification;
- scoped retrieval, ranking, activation and freshness handling;
- Brain-owned Memory Context planning, mutation, versioning, reconciliation and delivery;
- explicit Forget, retention, revocation, audit, backup/restore and recovery governance;
- stable Agent integration and BMCP protocol/Adapter contracts;
- storage, indexing, cache, consistency, observability and conformance support.

The Brain owns only Memory Regions explicitly designated and authorized as Brain-managed. It does not gain authority over adjacent protected prompt or policy regions.

## PB-03 Non-Goals

The project does not build or own:
- a general-purpose Agent Runtime;
- Agent Planner, task decomposition or Agent Decision Engine;
- Agent autonomous decision making or action selection;
- browser, terminal, tool execution or environment actuation platform;
- multi-Agent workflow orchestration or planner;
- Agent safety policy, external-action authorization or model guardrail ownership;
- a proprietary, single-LLM memory plugin or framework-private state as the sole persistence authority.

External Agents retain planning, reasoning, tool choice/execution, workflow orchestration and action policy. Brain may expose memory evidence, recommendations and managed context, but does not decide or execute the Agent's external actions.

## PB-04 System Architecture

Logical architecture is three cooperating layers:
1. **Memory Brain (canonical authority):** canonical domain identity and semantics, durable canonical assets and revisions, entities/relations, lifecycle, epistemic qualification, evidence/provenance references, canonical Forget state.
2. **Memory Compiler (transformation):** durable event ingress, extraction, normalization, classification, evidence/lineage attachment, consolidation proposals and conflict handling. It proposes and publishes only through authorized canonical contracts; it is not canonical truth authority.
3. **Memory Runtime (serving and context control):** retrieval, candidate generation, ranking, activation recommendations, working sets and Memory Context operations/synchronization. Retrieval does not confer canonical write authority.

Cross-cutting logical capabilities:
- **Context Management:** Brain-owned managed Memory Region desired state, membership/order/budget, versioning, reconciliation, delivery and applied evidence. It is logically in Runtime, with its own authority boundary and protocol contracts.
- **Agent Integration:** telemetry intake and inference-boundary Adapter integration; it bridges but does not take over Agent reasoning/action authority.
- **BMCP:** model-/Agent-neutral protocol and compatibility surface; H owns wire/Adapter contracts subject to dependent owner decisions.
- **Security Governance:** cross-cutting identity, authorization, delegation, revocation, retention, Forget completion, external copies, backup/restore and audit policy.
- **Storage/Index/Consistency:** persistence and derived projections; indexes/caches are not canonical authority.

These are logical responsibilities, not a mandated microservice or crate decomposition. A–I module ownership is governed by the module Owner artifacts and their approved contracts, not reassigned by this proposal.

## PB-05 Memory Domain Baseline

The following are distinct conceptual categories; this baseline does not define or approve their final schema:
- Event != Memory != Fact.
- Fact != Claim.
- Evidence != Provenance.
- Canonical Memory != Memory Context.
- Memory Context != Applied Context.
- Confidence != Relevance.
- Scope != Permission.

An Event is an observed/received occurrence; Memory is a governed retained memory asset; Fact/Claim semantics remain subject to B's formal ADR and domain decision. Evidence is supporting material; Provenance records origin/derivation lineage. Canonical Memory is durable Brain-owned memory state; Memory Context is a selected, mutable, versioned presentation/working region. Applied Context is what an Adapter/inference boundary can attest was applied for a particular request. Confidence is epistemic support; relevance is task/context utility. Scope identifies a boundary/partition; Permission authorizes an operation.

**No schema freeze:** B owns domain model semantics. Fact/Claim ADR, typed reference semantics and dependent schema/wire fields remain OPEN/ADR-BLOCKED until their decision authority approves them. No statement here selects an option.

## PB-06 Context Management Baseline

For a Brain-managed Memory Region, the product must support Add, Update, Remove, Replace, Reorder, Expire, Compact, Reconcile, Versioning, Delivery and Applied Evidence.

These operations mutate the desired/managed Context state and/or its delivery state; they do not by themselves mutate or delete Canonical Memory. Context removal is not Forget. Applied evidence is scoped to a specific request, Adapter/instance, Context version and delivery/application evidence; it is not global proof that all downstream copies were cleared.

Brain may manage only its explicitly assigned region. It must not overwrite System Instructions, Developer Instructions, User Original Input, Agent Safety Policy or other protected regions. Exact region boundaries and Adapter attestation semantics remain subject to C/G/H/I owner contracts.

## PB-07 Agent Independence

Brain exposes stable, documented contracts independent of any one Agent framework, model vendor, model API, hidden reasoning format, prompt template or Agent-private state. Agent implementations may be replaced while authorized canonical memory assets remain portable and governed.

Adapters translate at the inference boundary. Framework-specific formats may be optional adapters, never the unique canonical representation or sole durable store. Agent owns planning, decisions and actions; Brain owns its memory assets and managed context. Failure or replacement of an Agent must not silently destroy Brain-owned memory.

## PB-08 Security & Governance Baseline

The project must define and enforce:
- authenticated identity distinct from payload identity assertions;
- Principal and actor/delegation semantics;
- Scope and Permission as separate concepts;
- least privilege, explicit delegation and revocation;
- untrusted-memory handling and provenance;
- Forget authority, suppression, cleanup and physical-erasure distinctions;
- retention, external recipient inventory, backup/restore and erasure obligations;
- tamper-evident auditability and evidence retention policy.

B owns typed domain-reference semantics; I owns security policy and governance; H owns transport/wire and Adapter behavior; each module enforces applicable checks at its own boundary. Payload self-identification is not authentication. A Scope label is not permission. Memory and derived content are data, never instruction authority. No module may self-authorize a global Forget exception or claim physical erasure without evidence and I-governed policy.

## PB-09 Engineering Baseline

- Rust is the proposed primary route for the core control plane and correctness-critical components; language/tooling choices remain subject to engineering decision and validation.
- Prefer a modular monolith and explicit module boundaries before premature microservice distribution.
- Persistence, transactional semantics, indexing and cache technologies require comparative evaluation and representative validation; no candidate is pre-approved here.
- Model inference may be independently deployed or externally provided; core memory semantics must not depend on a specific model.
- Local resource budgets require representative workload measurements on declared hardware, datasets and concurrency.
- Correctness, security and recoverability precede performance optimization.
- Critical state transitions, races, replay and failure paths require repeatable tests and evidence.
- Technology decisions must record alternatives, constraints, benchmark methodology, results and rollback implications.

## PB-10 Quality Baseline

| Quality attribute | Required evidence (not satisfied by prose alone) |
|---|---|
| Correctness | Domain invariant tests, state-transition tests, contract conformance |
| Consistency | Transaction/ordering tests, concurrent race tests, recovery consistency checks |
| Reliability | Fault injection, retry/replay and partial-failure tests |
| Security | Threat model, negative authorization tests, adversarial tests, security review |
| Recoverability | Backup/restore drills, crash recovery, replay and post-restore Forget checks |
| Auditability | Correlated immutable audit records, traceable actor/source/decision evidence |
| Maintainability | Module ownership, reviewability, change impact and migration tests |
| Portability | Cross-Agent/model adapter conformance and export/import validation |
| Performance | Reproducible latency/throughput/resource benchmarks against declared budgets |
| Privacy/retention | Retention enforcement, recipient inventory and erasure evidence |

Each acceptance claim must link to a test/evidence ID, artifact version, environment, result and approving authority. Not Run, missing or inconclusive evidence remains open.

## 11. Source and decision boundaries

Initial sources inspected:
- `main@8a6414158c9c056c1638222534e1993d1bbc99d2`: `README.md` (blob `dfb5bf8a91f4a3ba29b14d623fbd2083f0273508`); `01-system-architecture/system-overview.md` (blob `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256`); `component-map.md` (blob `ddb7a1571463cadce83d89f62b03526c4f9693e8`); `responsibility-matrix.md` (blob `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3`).
- `session-a-integration-2026-11-16`: `reviews/integration/contract-registry.md` (blob `b15a87e9e259de74df600defbdd449772b9b3daa`).
- `session-d-memory-brain-2026-11-16`: Forget contract (blob `1f0391bc49d007c44ec74165bd33d37412cc7990`); cursor semantics (blob `4688a0ca487bf4d853c7f0220408abe8d743d159`).
- `session-e-memory-compiler-2026-11-16`: producer admission/publication contract (blob `00e37ba56596e710513c8d0568acd79141d9101b`).
- `session-h-bmcp-protocol`: envelope/versioning (blob `5547ecd78d118bd63e571e5daad87194d9b694e4`).
- `session-i-security-governance-2026-11-16`: Principal/ActorRef contract (blob `03765efac4bb1153f303ce0030f9e277d602e81d`).
- Phase 2 and Phase 3 integration reports on main were read; see the compliance matrix and rollout for findings.

The above are exact file blob SHAs, not branch HEAD SHAs. Branch-head inventory is recorded only where a live comparison/commit reference was actually verified. Historical review SHAs are not represented as current HEAD.

## Change control

Any change to PB-01..PB-10 requires a change proposal, impact analysis against all module baselines and project redlines, owner consultation, version increment, registry entry and approval by the Project Governance Authority. Until that authority is named and approves this baseline, status remains PROPOSED and no downstream document may cite it as an ACTIVE mandate.
