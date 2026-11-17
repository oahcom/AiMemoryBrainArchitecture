# ARCH-CONVERGENCE-001 — Contract Dependency Map
# ARCH-CONVERGENCE-001 — 契约依赖关系图

- Status: **DRAFT / NON-NORMATIVE**
- Baseline: `main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- Companion: `ARCH-CONVERGENCE-001-SOURCE-OF-TRUTH.md`

## 1. Purpose / 目的

This map records dependencies between existing Owner authorities. It does not move authority, create a new global coordinator, or approve unresolved interfaces.

本图记录现有 Owner 权威之间的依赖，不转移权威、不创建新的全局协调器，也不批准未解决的接口。

## 2. Authority map / 权威映射

| Authority / capability | Primary owner indicated by inspected sources | Depends on | Must not be delegated to |
|---|---|---|---|
| Domain meaning, identity, Fact/Claim semantics | B | Governance decision for Fact/Claim; D/E/F/G consumer mappings | Storage engine, extraction model, search product |
| Canonical Memory identity/version/commit/lifecycle | D with Storage physical realization | B domain references; Storage transaction; I commit authorization; E admission/publication | External memory product, workflow ACK |
| Evidence / Provenance semantics | Brain-owned Evidence authority (B/D/E contract split requires exact owner mapping) | E ingestion/lineage; D canonical refs; source integrity | Product episode IDs, model confidence |
| Ingestion acceptance and compilation | E | I identity/scope/auth; D producer admission; Storage durable work; B neutral candidate semantics | Provider ACK, queue delivery |
| Derived registration/publication | E producer; D canonical admission/fence; Storage atomic visibility | D fence/producer barrier; I policy; Storage same serialization domain | Search index, graph projection |
| Retrieval/activation and derived read path | F | D canonical visibility/version; I authorization; D ForgetFence; F index watermarks | Vector filter, cache hit, product RBAC |
| Context version/delivery/Applied decision | G | F candidate input; I authorization; D Forget; C Provider Outcome; H authenticated evidence; Storage/COC recovery | H transport ACK, workflow completion, search hit |
| Agent/provider dispatch and inference boundary | C | I authorization; G exact request binding; H wire/evidence; D Forget currentness | Agent runtime, provider receipt alone |
| BMCP wire and Adapter evidence transport | H | C/G/I/D/Storage exact schema mapping and identity semantics | MCP as substitute for BMCP or Brain authorization |
| Principal, policy, revocation, PermissionEpoch, global Forget policy | I | Authenticated issuer/workload identity; D canonical fence; all registered producers/recipients | PDP product as authority, Agent permissions |
| Canonical transaction substrate, visibility, COC/JF-10 and restore | Storage / Consistency | D row/semantic ownership; I pre-commit proof; E producer state; C/H/G evidence joins | Async outbox alone, process mutex, detached coordinator ACK |

## 3. Dependency edges / 依赖边

| Edge | Contract dependency | Evidence observed | Unresolved acceptance |
|---|---|---|---|
| B → D | Domain identities and Fact/Claim shape constrain canonical schema | B ADR-001 and D Canonical Store both mark Fact/Claim ADR-BLOCKED | Governance decision and D consumer acceptance |
| B → E | Compiler must emit candidate-neutral propositions until canonical model approved | E uses candidate/neutral proposal boundary | Exact candidate envelope and version contract |
| D ↔ Storage | Canonical fence/admission and final visibility must share a linearizable ordering mechanism | Storage L1 Option A selected; L4 engine/deployment OPEN | Exact D/Storage row ownership, schema, transaction and recovery proof |
| D → E | E producer registration/publication must be admitted and fenced by D | D producer admission and E derived registration contracts exist on branches | Current exact APIs and atomic commit evidence |
| I → D/E/F/G/H/Storage | Authorization, revocation, Forget governance and target inventory constrain all protected operations | I PermissionEpoch and global inventory contracts | Complete producer/recipient inventory and consumer conformance |
| D/I → F | Candidate retrieval and cache/index return must respect current Forget and permission state | F suppression/invalidation contracts; D/I fence/epoch definitions | Exact final-read linearization and rebuild/restore tests |
| F/I/D → G | Context may only include authorized, visible canonical references | G Applied contract requires own ContextVersion and D/I predicates | Exact read-to-context race and current-use checks |
| C ↔ H | Provider outcome and authenticated wire envelope require lossless identity and outcome mapping | C schema 1.0.1, H schema 1.2.15 and mapping reviews | H/C tree-currentness, exact field mapping and Owner acceptance |
| C/H/I/D/Storage → G | Full Applied requires exact provider request, authenticated evidence, authorization, Forget and applicable COC/Storage terminal evidence | G Phase 3.8.22 draft lists all evidence joins | C/H/G/I/D/Storage exact-version acceptance and physical test |
| Storage ↔ COC | JF-10 requires durable prepared participant and recovery evidence; COC is not silently folded into SQL | Storage branch contains JF-10 probes and COC design | Production topology and crash/failover/restore proof |

## 4. End-to-end dependency chain / 端到端依赖链

```text
Authenticated Principal / Workload (I)
        |
        v
Ingress identity + Scope + idempotency (E / I / B)
        |
        v
Durable acceptance / work record (E + Storage)
        |
        v
Candidate compilation + Evidence / Provenance (E; B semantics)
        |
        v
D producer admission + ForgetFence + canonical commit
        |                          |
        |                          +--> Storage atomic visibility / outbox
        v
Derived projection publication (F) -- never canonical truth
        |
        v
Retrieval candidate set (F)
        |
        +--> current canonical visibility/version (D / Storage)
        +--> current authorization / PermissionEpoch (I)
        +--> current ForgetFence / suppression (D / I)
        v
Versioned Context assembly (G)
        |
        +--> exact final request + Provider outcome (C)
        +--> authenticated Adapter / BMCP evidence (H)
        +--> COC / JF-10 / restore evidence (Storage)
        v
G-owned durable Applied decision
```

This is a dependency outline, not an approved state machine. Each edge requires a pinned contract version and an explicit consumer acceptance record.

这是依赖轮廓，不是已批准状态机。每条边都需要精确合同版本和明确的消费者接受记录。

## 5. Critical ordering namespaces / 关键顺序命名空间

The following values are not interchangeable and must never be numerically compared across namespaces:

| Namespace | Authority | Purpose |
|---|---|---|
| CanonicalCommitCursor | D | Canonical commit order |
| ForgetFenceGeneration | D | Canonical suppression generation |
| ProducerRegistrationHighWater / WorkItemBarrier | D | Per-Forget admitted producer work |
| PermissionEpoch | I | Authorization policy/revocation freshness |
| ProducerDomainInventoryEpoch | I | Closed-world producer/recipient inventory |
| IndexWatermark | F | Per-index/channel projection progress |
| ContextVersion | G | Context aggregate version |
| DeliveryAttempt / Applied identity | G | Delivery and Applied idempotency |
| AdapterCapabilityEpoch | H | Adapter capability snapshot |
| COC epoch/index / Prepared GID | COC / Storage | Durable coordination and participant recovery |

A consumer must invoke the issuing authority's validation operation. Numeric equality or ordering across different namespaces is invalid.

## 6. Unowned or multiply-described state / 未归属或重复描述状态

1. **Evidence / Provenance ownership:** the high-level matrix calls Evidence a primary capability, while B defines semantic references and E performs ingestion/binding. The exact record authority and write API need a single explicit owner statement.
2. **Canonical lifecycle:** D's Canonical Store owns lifecycle event persistence; B owns lifecycle semantics. The exact transition evaluator/authorization boundary must be pinned.
3. **Canonical transaction:** D owns semantic commit; Storage supplies physical serialization and visibility. Exact schema/row ownership is not fully published in main.
4. **Forget terminality:** D owns canonical suppression; I owns global completion/physical erasure policy. No single ACK may collapse local suppression, asynchronous cleanup and global physical erasure.
5. **Applied evidence:** G owns Applied decision; C owns provider handoff; H owns transport evidence; I/D/Storage supply authorization, Forget and transaction proofs. No upstream participant may write G's Applied state.
6. **Durable work:** E owns compiler attempts and queues; Storage owns durable persistence; D owns canonical admission. The common work ledger schema/transaction contract is not frozen.

## 7. Dependency order for convergence / 收敛依赖顺序

- A — freeze source provenance and resolve exact current Owner heads.
- B and C — resolve domain/transaction prerequisites and Forget/authorization/recovery contracts in parallel, with shared identity/epoch review.
- D — resolve runtime request/application evidence using only accepted B/C interfaces.
- E — choose minimum topology and implementation sequence after transaction, security and Applied contracts are stable.
- Final — cross-review all dependencies, adversarial scenarios and unresolved Owner approvals.

## 8. Non-decision / 非决议

This map does not approve any ADR, physical database, schema version, Owner contract, or implementation. A logical dependency does not imply a separate process, service, crate, database, broker or coordinator.
