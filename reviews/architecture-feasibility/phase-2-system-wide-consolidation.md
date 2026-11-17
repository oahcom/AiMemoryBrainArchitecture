# Phase 2 — System-wide Architecture Consolidation
# 第二阶段 — 全系统架构统一收敛审查

- Review ID: ARCH-CONSOL-001
- Repository: oahcom/AiMemoryBrainArchitecture
- Snapshot: 2026-11-17
- Review branch: review/arch-consol-001-system-wide-2026-11-17
- Authority: A / Principal Integration (role simulation authorized by the user; not an independent human Owner signature)
- Status: **PRELIMINARY INTEGRATION DISPOSITION — ARCHITECTURE FREEZE NOT READY**
- Normative languages: English and Chinese are peers.
- Tracking: Issue #43

## 1. Executive disposition / 总体裁决

**EN — NOT READY FOR ARCHITECTURE FREEZE.** The domain/authority decomposition remains coherent. B has reached semantic/source L1/L2 candidate alignment on H 1.2.14/C 1.0.1, but Storage v3.2.9 is stale against later C/D/I exact-review and H CI pin corrections; A has selected Option A as the v1 logical D/Storage topology, but its L1/L2 contract still needs clarifications for transaction execution authority, D effect-permit/lifecycle coverage, cross-BrainAuthority scope, I COMMIT_WON crash/revocation semantics and anchor restore continuity. The remaining freeze blockers are those Option A clarifications, incomplete distributed reference-model/COC/JF-10 evidence, Fact/Claim ADR, Full Applied and Global Forget composition.

**中文 — 暂不具备架构冻结条件。** 项目已经形成相当清晰且安全约束深入的领域架构。总体模块划分合理：Canonical Memory 与检索投影、任务 Context 分离；D 管理权威记忆和 ForgetFence 语义；I 管理授权与 Global Forget 策略；C 管理 Provider 副作用事实；H 管理 Wire 合同；Storage 管理物理持久化与可见性机制。但目前仍不能证明这些模块已经组成一套完整、无歧义的系统。主要冻结阻塞是 D/Storage 序列化拓扑未决、C/H/D/I 精确版本绑定漂移、发布/遗忘/恢复端到端参考模型证据不足，以及 Fact/Claim 和 Applied/Provider Outcome 合同仍有未闭环绑定。

This is an architecture review, not an implementation-readiness review. L4 production implementation, deployment, real provider adapters, HSM/KMS operations and performance benchmarks are later engineering acceptance work. They must not be used to disguise L1/L2/L3 architecture gaps, and their absence alone does not make a coherent architecture infeasible.

本审查判断架构可行性，不以“尚未实现”作为架构失败理由。L4 生产实现、部署、真实 Provider Adapter、HSM/KMS 运维和性能基准属于后续工程验收；不得用这些 L4 缺失掩盖 L1/L2/L3 架构问题，也不能仅因它们尚不存在就判定架构不可行。

## 2. System architecture / 总体架构

~~~mermaid
flowchart TB
  AG["Agent / LLM / Session"]
  C["C — Agent Integration / Provider Egress"]
  H["H — BMCP / Wire / Adapter Capability"]
  E["E — Ingress / Memory Compiler"]
  D["D — Canonical Memory / Lifecycle / ForgetFence"]
  F["F — Retrieval / Activation / Index / Cache"]
  G["G — Memory Context / Delivery / Applied"]
  B["B — Domain Model / Typed Semantics"]
  I["I — Identity / Authorization / Revocation / Global Forget"]
  S["Storage — Durable Transactions / Visibility / Recovery"]
  Q["COC — Quorum Log / Recovery Cutoff / Participant Registry"]
  A["A — Principal Integration / Architecture Governance"]
  AG <--> C
  C <--> H
  H <--> E
  E <--> D
  D <--> F
  F <--> G
  G <--> H
  H <--> C
  B -. "shared semantic contract" .-> E
  B -. "shared semantic contract" .-> D
  B -. "shared semantic contract" .-> F
  B -. "shared semantic contract" .-> G
  I -. "protected-boundary authorization" .-> C
  I -. "protected-boundary authorization" .-> D
  I -. "protected-boundary authorization" .-> E
  I -. "protected-boundary authorization" .-> F
  I -. "protected-boundary authorization" .-> G
  Q -. "quorum prefix / batch / manifest" .-> S
  S -. "durability / visibility / recovery" .-> D
  S -. "durability / visibility / recovery" .-> E
  S -. "durability / visibility / recovery" .-> F
  S -. "durability / visibility / recovery" .-> G
  A -. "integration / freeze governance" .-> B
  A -. "integration / freeze governance" .-> C
  A -. "integration / freeze governance" .-> D
  A -. "integration / freeze governance" .-> E
  A -. "integration / freeze governance" .-> F
  A -. "integration / freeze governance" .-> G
  A -. "integration / freeze governance" .-> H
  A -. "integration / freeze governance" .-> I
  A -. "integration / freeze governance" .-> S
~~~

The diagram is a logical responsibility view, not a deployment diagram. A–I do not imply one process, service, database or Rust crate per Owner. Storage is a cross-cutting physical consistency responsibility, not a second Memory Brain authority.

该图表达逻辑责任，不代表部署拓扑。A–I 不意味着每个 Owner 必须对应独立进程、服务、数据库或 Rust Crate。Storage 是横向物理一致性责任，不是第二个 Memory Brain 领域权威。

### 2.1 Authority map / 权威边界

| Role | Normative responsibility / 规范责任 | Must not claim / 不得越权 |
|---|---|---|
| A | System integration, cross-owner dependency and freeze decision / 系统集成、跨 Owner 依赖与冻结裁决 | Another Owner's semantic or terminal truth / 其他 Owner 的语义或终态事实 |
| B | Canonical domain meaning, identity and type semantics / 领域语义、身份与类型 | Persistence or runtime policy / 持久化或运行时策略 |
| C | Agent boundary, final provider send and immutable Provider Outcome / Agent 边界、最终 Provider 发送及 Provider Outcome | D/I/Storage truth or model execution success / D/I/Storage 权威或模型执行成功 |
| D | Canonical Memory, lifecycle, producer registry, lineage and ForgetFence / 权威记忆、生命周期、Producer Registry、Lineage、ForgetFence | I authorization or Storage physical commit / I 授权或 Storage 物理提交 |
| E | Durable ingress, extraction, compilation, provenance and staged output / 持久入口、抽取、编译、溯源与暂存输出 | Canonical truth, D admission or global completion / Canonical Truth、D 准入或全局完成 |
| F | Retrieval, ranking, activation, index/cache and Working Set / 检索、排序、激活、索引/缓存与 Working Set | Canonical truth, Forget completion or G Applied / 权威事实、遗忘完成或 G Applied |
| G | Desired Context, immutable ContextVersion, delivery and Context-side Applied / 目标 Context、不可变版本、交付与 Context 侧 Applied | Canonical Memory, provider outcome or external erasure / 权威记忆、Provider Outcome 或外部擦除 |
| H | BMCP schema, wire semantics, capability and authenticated transport evidence / BMCP Schema、Wire 语义、能力与认证传输证据 | Owner authority or business terminal truth / Owner 权威或业务终态事实 |
| I | Principal/workload trust, authorization, PolicyDomain, PermissionEpoch, revocation and Global Forget policy/completion / 身份信任、授权、PolicyDomain、PermissionEpoch、撤权及 Global Forget | D lineage/fence or Storage visibility / D Lineage/Fence 或 Storage 可见性 |
| COC | Quorum-committed causal-order prefix, Recovery Cutoff Batch/Manifest and participant registry / Quorum 因果顺序前缀、Recovery Cutoff Batch/Manifest 与 Participant Registry | Owner authorization, D fence, C provider truth or I release / Owner 授权、D Fence、C Provider Truth 或 I Release |
| Storage | Durable transaction, prepared participant, visibility pointer, outbox and physical recovery / 持久事务、Prepared Participant、可见性指针、Outbox 与物理恢复 | D/I/C semantic decisions or Global Forget completion / D/I/C 语义决议或 Global Forget 完成 |

### 2.2 Domain model / 领域模型

The B baseline correctly separates Event, Memory, Claim, Entity, Relation, Evidence, Provenance, MemoryVersion, MemorySource, MemoryContext, ContextEntry, AgentScope and EnvironmentScope. A Memory is a retained knowledge asset, not a guarantee that every contained Claim is true. Epistemic status, lifecycle, temporal qualification, confidence, relevance, trust and evidence strength are orthogonal dimensions.

B 的领域基线正确区分 Event、Memory、Claim、Entity、Relation、Evidence、Provenance、MemoryVersion、MemorySource、MemoryContext、ContextEntry、AgentScope 和 EnvironmentScope。Memory 是被保留的知识资产，不代表其中每个 Claim 都必然为真。认知状态、生命周期、时间限定、置信度、相关性、信任和证据强度是相互独立的维度。

The Fact/Claim ADR remains ADR-BLOCKED. Until B resolves it, no shared schema or wire field may silently assume a final Fact/Claim boundary. This is a semantic freeze blocker, not a reason to collapse Memory and Claim into one object.

Fact/Claim ADR 仍为 ADR-BLOCKED。在 B 正式解决之前，任何共享 Schema 或 Wire 字段都不得暗中假设 Fact/Claim 边界已经定案。这是语义冻结阻塞，不意味着应该把 Memory 与 Claim 合并成同一个对象。

## 3. End-to-end lifecycle / 端到端生命周期

### 3.1 Ingress and compilation / 输入与编译

1. Agent/Adapter submits source material through the authenticated C/H boundary.
2. E durably accepts the source and creates stable ingress/work identity.
3. Derivative-capable work must obtain D RegistrationReceipt before queue insertion, lease, protected source dereference or execution.
4. E freezes one immutable compiler input bundle per DerivationRun, preserving source versions, evidence, provenance, Scope and model/compiler/schema versions.
5. E writes candidate output to private staging and submits the complete direct/transitive dependency set to D.
6. E/D/Storage publication uses the candidate sequence: durable Storage PREPARED_HIDDEN participant → D PublicationParticipant admission → I single-use CommitAuthorization consumption → Storage final visibility commit validating D and I proofs → D/I closeout against the same authoritative Storage outcome.
7. UNKNOWN/IN_DOUBT remains private and keeps the relevant barriers open.

1. Agent/Adapter 经认证的 C/H 边界提交源材料。
2. E 持久化接收输入并建立稳定的入口/Work 身份。
3. 可产生派生物的工作必须先取得 D RegistrationReceipt，之后才能入队、取得租约、读取受保护源或执行。
4. E 为每个 DerivationRun 冻结不可变编译输入包，保留源版本、证据、溯源、Scope 及模型/编译器/Schema 版本。
5. E 将候选输出写入私有暂存区，并向 D 提交完整直接及传递依赖集合。
6. E/D/Storage 候选发布顺序为：Storage 持久化 PREPARED_HIDDEN Participant → D 准入 PublicationParticipant → I 单次消费 CommitAuthorization → Storage 在最终可见性提交点验证 D/I 证明 → D/I 根据同一权威 Storage Outcome 分别关闭。
7. UNKNOWN/IN_DOUBT 必须保持私有，并保持相关 Barrier 开启。

The logical sequence is coherent, including the correction that post-commit ITerminalProof cannot be required by the commit that creates the Storage outcome. Option A is now selected as the v1 logical serialization profile by ADR §8; the database engine/deployment remains unselected (L4), and A-01–A-05 remain architecture clarification gates. The protocol is not end-to-end or production verified.

COC and JF-10 must remain separate in the system model. COC is a quorum-committed causal-order log for recovery cutoffs and participant manifests; it records owner evidence but cannot issue owner decisions. JF-10 is a separately gated I/Storage prepared-participant bridge using the exact same prepared GID/participant identity for resolution. Storage v3.2.3 explicitly says prior COC acceptance does not approve automatic COC↔JF-10 composition, and COC does not become the JF-10 coordinator. Issue #10 currently records Gate A PARTIAL PASS after five PostgreSQL 18.7 capability CI classes; Gate B persistent COC and Gate C deterministic fault-injection remain BLOCKED. The CI results do not identify a project-designated Canonical Authority deployment or close JF-10.

COC 与 JF-10 必须在系统模型中保持分离。COC 是用于恢复截止点和 Participant Manifest 的 Quorum 因果顺序日志；它记录 Owner 证据，但不能签发 Owner 决议。JF-10 是单独设门的 I/Storage Prepared Participant 桥接协议，使用同一个精确 Prepared GID/Participant 身份进行解析。Storage v3.2.3 明确指出，既有 COC 接受不等于自动批准 COC↔JF-10 组合，COC 也不会成为 JF-10 Coordinator。Issue #10 当前记录 PostgreSQL 18.7 五类能力 CI 后 Gate A PARTIAL PASS；持久化 COC 的 Gate B 和确定性故障注入 Gate C 仍 BLOCKED。这些 CI 结果没有指定项目 Canonical Authority 的实际部署，也没有关闭 JF-10。

当前提案的逻辑顺序基本自洽，尤其已经修正了不能要求 Storage 提交前先获得提交后 ITerminalProof 的循环依赖。但它仍不是已经选定的物理序列化拓扑，也不是经过端到端验证的协议。

### 3.2 Recall, Context and inference / 召回、上下文与推理

- F returns candidate exact MemoryVersionRefs with provenance and completeness/currentness information; it does not establish canonical truth.
- D revalidates canonical lifecycle and lineage; I authorizes the exact principal, purpose, Scope, Environment and PolicyDomain.
- G decides Context membership and produces an immutable ContextVersion. F Working Set, E compiler input bundle and G ContextVersion are distinct objects.
- H transports the versioned delivery; transport ACK is not materialization or Applied.
- C owns the final provider transport boundary and immutable CSubmitOutcome. Every physical send, retry, redirect or failover must re-enter the final gate.
- G Applied is a request-bound Context-side fact; it must not imply that the model understood or followed the supplied context.

- F 返回带溯源和完整性/当前性信息的精确 MemoryVersionRef 候选，不负责建立 Canonical Truth。
- D 重新验证权威生命周期与 Lineage；I 针对精确主体、Purpose、Scope、Environment 和 PolicyDomain 授权。
- G 决定 Context 成员并生成不可变 ContextVersion。F Working Set、E 编译输入包和 G ContextVersion 是不同对象。
- H 传输带版本的 Delivery；Transport ACK 不等于 Materialized 或 Applied。
- C 拥有最终 Provider 传输边界和不可变 CSubmitOutcome。每次物理发送、重试、重定向或故障切换都必须重新进入最终 Gate。
- G Applied 是绑定具体请求的 Context 侧事实；不得声称模型理解或遵循了所提供的 Context。

### 3.3 Forget and restore / 遗忘与恢复

D owns per-Canonical-Memory producer admission, lineage, ForgetFence and barrier disposition. I owns authorization/revocation and Global Forget policy/completion. F/G/E must register derivative-capable work, preserve complete lineage, build privately, revalidate current D/I state before visibility or delivery, and quarantine restored queues/snapshots until reconciliation. Storage owns durable recovery evidence but cannot issue D/I/F/G/C release receipts.

D 管理每个 Canonical Memory 的 Producer 准入、Lineage、ForgetFence 和 Barrier 终态。I 管理授权/撤权与 Global Forget 策略/完成。E/F/G 必须登记可产生派生物的工作、保留完整 Lineage、私有构建，并在可见或交付前重新验证 D/I 当前状态；恢复的队列和快照必须隔离，直至完成协调。Storage 提供持久恢复证据，但不能签发 D/I/F/G/C 的 Gate Release。

## 4. What is already strong / 已有的架构优势

1. Canonical Memory is separated from index/cache projections and task Context.
2. Event acceptance, compiler completion, canonical commit, indexing, delivery and Applied are distinct evidence states.
3. D/I/C/Storage authority boundaries are explicit; downstream ACKs cannot synthesize another Owner's truth.
4. Producer admission-before-work, complete dependency registration, immutable retry identity and fail-closed UNKNOWN are consistently present in E/F/G and D proposals.
5. Context removal is not canonical Forget; logical suppression is not physical erasure.
6. H has a typed recovery evidence model with separate owner admission and owner entry identities, row digests, snapshots and membership proofs.
7. Rust modular monolith is a reasonable first deployment direction; microservices/Kubernetes/Kafka are not prematurely mandatory.

1. Canonical Memory 与索引/缓存投影、任务 Context 分离。
2. Event 接收、Compiler 完成、Canonical Commit、索引、交付和 Applied 是不同证据状态。
3. D/I/C/Storage 权威边界明确，下游 ACK 不能替代其他 Owner 的事实。
4. E/F/G 与 D 提案普遍采用先准入后执行、完整依赖登记、不可变重试身份及 UNKNOWN 失败关闭。
5. Context 移除不等于 Canonical Forget；逻辑抑制不等于物理擦除。
6. H 已建立类型化恢复证据模型，区分 Owner Admission 与 Owner Entry 身份、行摘要、快照和 Membership Proof。
7. Rust Modular Monolith 是合理的首期部署方向，不应过早强制微服务/Kubernetes/Kafka。

## 5. Freeze blockers / 架构冻结阻塞

| ID | Severity / Level | Finding / 发现 | Required closure / 必须闭环 |
|---|---|---|---|
| ARC-01 | P1 · L1/L2/L3 | Storage/D Option A is selected as the v1 logical profile, but the cross-owner transaction executor/write-authority boundary, complete D fence-sensitive lifecycle transition set, one-BrainAuthority operation scope, I COMMIT_WON crash/revocation rule and anchor restore checkpoint proof are not fully specified. / Storage/D Option A 已选为 v1 逻辑 Profile，但跨 Owner 事务执行者/写权边界、D Fence 敏感生命周期转换、单 BrainAuthority 操作范围、I COMMIT_WON 崩溃/撤销规则和 Anchor Restore Checkpoint Proof 尚未完整规范。 | Resolve A-01–A-05 in a successor ADR amendment; then execute L3 reference-model/race/fault vectors. DB engine/deployment remains L4. / 在后继 ADR 修订中解决 A-01 至 A-05，再执行 L3 参考模型/竞争/故障向量；DB Engine/部署仍属 L4。 |
| ARC-02 | P2 · L2 | Storage v3.3.0 now consolidates H 1.2.14/C 1.0.1, the exact 42-test H local path, and current C/H/D/I role reviews; semantic/source candidate alignment is conditionally aligned. / Storage v3.3.0 已整合 H 1.2.14/C 1.0.1、H 精确 42-test 本地路径及当前 C/H/D/I 角色审查；语义/源文件候选对齐已条件满足。 | A performs fresh exact review of v3.3.0 and Option A ADR; production authority adapters and L3/L4 gates remain open. / A 对 v3.3.0 和 Option A ADR 进行新精确审查；生产权威 Adapter 与 L3/L4 Gate 仍 OPEN。 |
| ARC-03 | P2 · L2 | CSubmitOutcome 1.0.1 is now the proposed immutable source for new records and is pinned by Storage v3.2.9; 1.0.0 remains historical. / CSubmitOutcome 1.0.1 已成为新记录候选不可变来源并由 Storage v3.2.9 精确绑定；1.0.0 保留为历史。 | Keep production C/I crypto profile registration, trust roots, key custody, historical verification and anti-rollback as independent I governance gates; do not infer production trust from local CI. / 生产 C/I Crypto Profile 注册、Trust Root、Key Custody、历史验证和 Anti-Rollback 仍是 I 独立治理 Gate，不得从本地 CI 推断生产信任。 |
| ARC-04 | P0 · L1/L3 | The D/E/Storage publication sequence is coherent as a proposal, but a complete integrated race/crash reference model is not evidenced by the exact current contract bundle. / D/E/Storage 发布顺序作为提案自洽，但当前精确合同包尚无完整集成竞争/崩溃参考模型证据。 | Model both D fence/admission orders, I revocation/consumption orders, Storage prepare/commit ACK loss, process crash at every durable boundary, stale lease, replay and conflicting terminal outcomes. / 建模 D Fence/Admission 两种顺序、I 撤权/消费顺序、Storage Prepare/Commit ACK 丢失、每个持久边界崩溃、过期 Lease、重放和冲突终态。 |
| ARC-05 | P1 · L1/L2/L3 | Multi-PolicyDomain atomicity is explicitly blocked; I PermissionEpoch is local to one PolicyDomain. Global Forget and cross-domain operations need an explicit supported scope. / Multi-PolicyDomain 原子性明确阻塞；I PermissionEpoch 仅属于单个 PolicyDomain。 | State single-domain guarantees and cross-domain limitations, or design a separate coordinator/partial-completion protocol with explicit semantics. / 明确单域保证与跨域限制，或设计独立协调/部分完成协议。 |
| ARC-06 | P1 · L2/L3 | C Provider Outcome, H wire validation and G Applied are not yet one exact frozen end-to-end contract. / C Provider Outcome、H Wire 验证和 G Applied 尚未形成一套精确冻结的端到端合同。 | Bind the final immutable inference request after all transformations; distinguish handoff, provider acceptance, execution, completion, delivery and Applied. / 绑定全部转换后的最终不可变推理请求；区分 Handoff、Provider Acceptance、Execution、Completion、Delivery 与 Applied。 |
| ARC-07 | P1 · L2 | B Fact/Claim ADR remains ADR-BLOCKED. / B Fact/Claim ADR 仍未解决。 | Resolve the domain decision before freezing dependent schemas or wire fields. / 冻结依赖 Schema/Wire 字段前先解决领域决议。 |
| ARC-08 | P1 · L3 | Full Forget/restore anti-resurrection proof across producer inventory, derivatives, backup, restore, index rebuild, cache and Adapter reconnect is not yet established as one traceable model. / Producer Inventory、派生物、备份、恢复、索引重建、缓存和 Adapter 重连之间的完整防复活证明尚未形成一个可追溯模型。 | Produce an end-to-end scope/lineage inventory and adversarial restore/replay traces; unknown coverage remains quarantined. / 建立端到端 Scope/Lineage 清单及对抗性恢复/重放轨迹；覆盖未知时必须隔离。 |
| ARC-09 | Governance | Role-simulated reviews are not independent Owner signatures or external governance approvals. / 角色模拟审查不等于独立 Owner 签署或外部治理批准。 | Record technical role simulation separately from Owner-authorized and external governance decisions. / 将技术角色模拟与 Owner 授权决议、外部治理批准分开记录。 |
| ARC-10 | P1 · L1/L2/L3 | COC recovery-cutoff consensus and the JF-10 prepared-participant bridge are distinct authorities; automatic composition is not approved. / COC 恢复截止点共识与 JF-10 Prepared Participant 桥接是不同权威；自动组合未获批准。 | Keep COC quorum prefix/batch/manifest, I terminal decision, D fence and Storage same-GID resolution separate; require fresh I/D/C/Storage/H exact bridge decisions and Gate B/C evidence. / 分离 COC Quorum 前缀/Batch/Manifest、I 终态决议、D Fence 与 Storage 同 GID 解析；要求 I/D/C/Storage/H 精确桥接决议及 Gate B/C 证据。 |

### 5.1 Technology compatibility note / 技术兼容性说明

TAB-001 is a candidate blueprint, not a technology freeze. Rust is the decided language direction; a modular monolith is recommended; SQLite WAL is only a conditional first prototype; PostgreSQL is a comparison candidate; FTS5/Tantivy/vector ANN and local/remote inference backends remain candidates.

TAB-001 是候选技术蓝图，不是技术冻结。Rust 是已决定的语言方向；Modular Monolith 是推荐方案；SQLite WAL 只是有条件的首期原型候选；PostgreSQL 是比较候选；FTS5/Tantivy/Vector ANN 和本地/远程推理后端仍是候选。

The SQLite prototype must not be represented as satisfying JF-10 prepared-participant or HA/recovery guarantees unless the exact design proves those capabilities. Storage ADR Option A requires one serializable transaction domain for D/Storage visibility; Option B requires a durable linearizable coordinator. PostgreSQL 18.7 capability CI is evidence for its pinned test profile only, not proof that the project has selected or deployed it.

除非精确设计证明能力，否则不得将 SQLite 原型描述为满足 JF-10 Prepared Participant 或 HA/恢复保证。Storage ADR 的 Option A 要求 D/Storage 可见性处于一个 Serializable Transaction Domain；Option B 要求持久化线性一致协调器。PostgreSQL 18.7 能力 CI 仅证明其固定测试 Profile，不代表项目已经选定或部署该数据库。

## 6. Feasibility matrix / 可行性矩阵

| Critical path | Current verdict | Reason / 原因 |
|---|---|---|
| Domain model B | CANDIDATE | Strong object separation; Fact/Claim ADR remains open. / 对象分离清晰；Fact/Claim ADR 未决。 |
| Ingress/compiler E | CANDIDATE | Durable ingress and D-before-work semantics are specified; integrated model evidence remains incomplete. / 持久入口与先 D 准入后执行已有规范；集成模型证据不足。 |
| Canonical Memory/Forget D | NOT PROVEN | D semantics are detailed; physical final visibility topology and integrated proof remain open. / D 语义深入；最终可见性拓扑与集成证明未闭环。 |
| Retrieval/runtime F | CANDIDATE | Candidate filtering, exact ref revalidation and derivative gating are specified; full anti-resurrection traces remain open. / 候选过滤、精确引用复核和派生物 Gate 已定义；防复活轨迹未闭环。 |
| Context/Applied G | NOT PROVEN | Context version boundary is clear; exact Full Applied C/G/H proof is not frozen. / Context 版本边界清晰；Full Applied 的 C/G/H 证明未冻结。 |
| Agent/provider C | CANDIDATE | Egress gate and immutable outcome semantics exist; schema/contract version alignment and provider conformance remain open. / Egress Gate 与不可变 Outcome 语义已定义；Schema/合同版本及 Provider 符合性未闭环。 |
| BMCP H | NOT PROVEN | 1.2.14/1.0.2/1.0.5 and C 1.0.1 candidate artifacts exist; Provider Outcome and integrated authority mappings are separate, and same-manifest C review remains open. / 1.2.12/1.0.2 结构工件存在；语义 Validator 与 C 映射落后。 |
| Security/governance I | CANDIDATE | Authority and fail-closed semantics are clear; crypto profile registration and governance approval remain open. / 权威与 Fail-closed 语义清晰；密码学配置注册和治理批准未完成。 |
| Storage/COC/JF-10 | BLOCKED | Option A is selected as L1 logical topology, conditionally accepted pending A-01–A-05; JF-10 P0, Gate A, persistent COC Gate B and fault-campaign Gate C remain open/blocked. / Option A 已选为 L1 逻辑拓扑，但 A-01 至 A-05 仍待澄清；JF-10 P0、Gate A、持久化 COC Gate B 和故障演练 Gate C 仍 OPEN/BLOCKED。 |
| System composition A | NOT READY | Exact-version joins, integrated reference traces and owner-authority decisions are incomplete. / 精确版本 Join、集成参考轨迹及 Owner 权威决议尚不完整。 |

## 7. Architecture-freeze gate / 架构冻结门槛

Freeze requires L1 + L2 + L3:

- L1: every critical mechanism has a feasible, explicit authority and linearization design.
- L2: exact Owner contracts, schemas, identifiers, evidence and consumer joins are consistent and accepted by affected authorities.
- L3: critical invariants have adversarial reference-model traces, negative cases and counterexample analysis.
- L4: implementation, deployment, real provider and performance acceptance are carried forward separately.

冻结要求 L1 + L2 + L3：

- L1：每个关键机制均有可行、明确的权威与线性化设计。
- L2：精确 Owner 合同、Schema、标识符、证据和消费者 Join 保持一致，并得到相关权威接受。
- L3：关键不变量具备对抗性参考模型轨迹、负例和反例分析。
- L4：实现、部署、真实 Provider 和性能验收另行纳入后续工程计划。

**Current recommendation: NOT READY.** Do not freeze the system architecture and do not begin product implementation on the assumption that the current proposals are already a complete proof. Continue with the ordered closure plan in Issue #43. This review does not claim production readiness, implementation PASS, Global Forget completion or physical erasure.

**当前建议：NOT READY。** 不冻结系统架构，也不应假定现有提案已经构成完整证明而启动产品实现。继续按照 Issue #43 的顺序闭环。本审查不宣称生产就绪、实现通过、Global Forget 完成或物理擦除完成。

## 8. Ordered next actions / 后续推进顺序

1. Storage + D + A: amend Option A with the exact transaction executor/owner-write boundary, D effect-permit and lifecycle transition coverage, per-BrainAuthority scope, I receipt race semantics and anchor restore continuity; keep DB engine selection at L4.
2. C + H + D + I + Storage: close same-manifest review of H 1.2.14 / RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 / CSubmitOutcome 1.0.1, including both H mapping artifacts.
3. D + E + I + Storage: build the integrated producer/fence/publication reference model with adversarial ordering and crash-window tests.
4. I + D + E + F + G + Storage: prove Global Forget inventory, restore/replay cutoff and anti-resurrection across all derivative classes.
5. C + G + H + I + D: close the final-request-bound Applied evidence chain and provider outcome semantics.
6. B: resolve Fact/Claim ADR and confirm no dependent schema uses unresolved semantics.
7. A: refresh all exact pins, complete bilingual parity review and issue a final L1/L2/L3 freeze disposition.

1. Storage + D + A：修订 Option A，明确事务执行者/Owner 写权、D EffectPermit/生命周期转换覆盖、per-BrainAuthority 范围、I Receipt 竞争语义及 Anchor 恢复连续性；DB Engine 选择仍属于 L4。
2. C + H + D + I + Storage：闭环 H 1.2.14 / RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 / CSubmitOutcome 1.0.1 的同一 Manifest 审查，必须包含两种 H Mapping。
3. D + E + I + Storage：建立集成 Producer/Fence/Publication 参考模型，覆盖对抗性顺序和崩溃窗口。
4. I + D + E + F + G + Storage：证明 Global Forget Inventory、Restore/Replay Cutoff 和所有派生物的防复活。
5. C + G + H + I + D：闭环最终请求绑定的 Applied 证据链及 Provider Outcome 语义。
6. B：解决 Fact/Claim ADR，并确认没有依赖未决语义的 Schema。
7. A：刷新全部精确 Pin，完成双语语义一致性复审，并给出最终 L1/L2/L3 冻结裁决。

## 9. Evidence references / 证据入口

- A Phase 1 reassessment: reviews/architecture-feasibility/phase-1-owner-reassessment.md, Blob 1ffb788c7e193b8777e8d849c1e3cc11ededc545.
- TAB-001: 13-engineering-decisions/technology-architecture-blueprint.md, Blob 7b6f2d139217dbe13ab3a3af31bfbff525f20e71.
- Storage/D topology ADR: Blob bb544ba2f346bdc130d524bd5c7310d86f367988.
- Storage v3.2.4 successor exact-version manifest: Blob 6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7.
- Current exact evidence ledger: phase-2-exact-evidence-ledger.md.
- Contradiction register: phase-2-contradiction-register.md.


## 12. Superseding protocol status — Storage v3.2.9 / 后继协议状态

The latest Owner branches supersede the earlier Phase 2 protocol observations. Current B baseline is Storage v3.2.9 exact manifest Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3.

- H Unified 1.2.14 / wire 1.3.0, RecoveryJoin 1.0.2, RecoveryCutoff 1.0.5 and CSubmitOutcome 1.0.1 are now bound in one candidate source bundle.
- C/H/D/I role reviews now bind the corrected H schema Blob 09fcd1fa29fe24255fbd87cae79dafb406594a59 and integrated H authority-join mapping 1cbe74eba69325510d6b1019d971661f965eabf8.
- H now has a full local H envelope + CSubmitOutcome 1.0.1 positive fixture and 32 passing test methods (26 H validator/fixture + 6 Python/Node crypto interoperability) on run 44069777296.
- The full-path local tests no longer mock H/C schema validation, local semantic predicates or C-P0 digest/preimage computation. The ten I/D/Storage authority callbacks remain test doubles; production trust and owner-authoritative proof adapters remain OPEN.
- Storage v3.2.9 records C/H/I/D role reviews but explicitly requires fresh A review. The earlier A review of v3.2.8 does not transfer.
- B is **CONDITIONALLY ALIGNED at L1/L2 candidate level**. This is not protocol freeze, independent human Owner approval, Gate B/C acceptance or production authorization.

中文：最新 Owner 分支已替代此前 Phase 2 协议观察。当前 B 基线为 Storage v3.2.9 精确 Manifest Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3。H 1.2.14、RecoveryJoin 1.0.2、RecoveryCutoff 1.0.5、CSubmitOutcome 1.0.1 已绑定为同一候选源包；C/H/D/I 角色审查已绑定修正后的 H Schema 和集成 Authority-Join Mapping；H 已有完整本地 H Envelope + CSubmitOutcome 正向 Fixture，32 项测试通过。本地 Schema/Semantic/Digest 路径不再 Mock，但十个 I/D/Storage Authority Callback 仍为 Test Double。生产信任和 Owner 权威 Proof Adapter 仍 OPEN。Storage v3.2.9 记录了 C/H/I/D 角色审查，但明确要求 A 新审查；A 对 v3.2.8 的旧审查不能继承。B 可在 L1/L2 候选层标记 CONDITIONALLY ALIGNED，但不代表协议冻结、独立人类 Owner 批准、Gate B/C 验收或生产授权。


## 13. Currentness correction after v3.2.9 / v3.2.9 后的当前性修正

The latest Owner branches advanced after Storage v3.2.9:
- C HEAD 81f1e81307315a31c3bbeae17eb801e8a4f47e10 corrected its H schema pin.
- D HEAD 7d01732521a8b9db202f10cde2c2547e50071d58 corrected its H schema pin.
- I HEAD a68bb3587fe88aa72398e2dc8d136f94cee9a63f corrected its H schema pin.
- H HEAD 362cc113cfb5b595a4002a6f6e980d19ae2d2d15 updated the CI pin to run 44069941327 / commit ba2c9341fee4eb9ca9e665c74bdd37b4675dd251 / job 133993324484.
- Storage HEAD 39a1e0429f6b4b08c6c437c8e3f5ace582a7315f still has v3.2.9 as latest manifest.

Storage v3.2.9 therefore no longer binds the latest C/D/I review Blobs and H CI run. The semantic/source candidate alignment remains, but B's exact-currentness gate is OPEN until Storage publishes a successor manifest, all Owners review that same exact Blob, and A reviews the successor. This is provenance/currentness drift, not a demonstrated schema regression.

中文：v3.2.9 发布后，C/D/I 修正了精确 Schema Pin，H 更新了 CI Run/Commit/Job，但 Storage 尚未刷新 Manifest。语义/源文件候选对齐仍成立，B 的精确当前性 Gate 重新 OPEN，直至 Storage 发布后继 Manifest、所有 Owner 审查同一 Blob、A 复审后继版本。该问题属于来源/当前性漂移，不是已证明的 Schema 回退。


## 14. B successor manifest reconciliation / B 后继 Manifest 谱系收敛

Storage has published v3.3.0, exact Blob c8407c9f10049d65426a3598ad20b6aa70f83c32. It explicitly supersedes v3.2.7, v3.2.8 and v3.2.9 for current candidate bundle binding and reconciles the divergent manifest lineage. It binds the 42-test H exact-head suite (run 44072037563, commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7, job 134000402978), H 1.2.14, C 1.0.1, RecoveryJoin 1.0.2, RecoveryCutoff 1.0.5, integrated H authority mapping and current C/D/I 42-test review Blobs.

**B disposition:** CONDITIONALLY ALIGNED at L1/L2 candidate level against v3.3.0. A must now review the exact v3.3.0 Blob and Option A topology ADR. Production callbacks remain test doubles; production C/I trust, D lineage/release, COC quorum, JF-10, same-GID recovery, Gate B/C, Global Forget and Full Applied remain open.

中文：Storage 已发布 v3.3.0，精确 Blob c8407c9f...，明确替代 v3.2.7/v3.2.8/v3.2.9 的当前候选 Bundle 绑定，解决 Manifest 谱系分叉。它绑定 H 42-test 精确 HEAD Suite、H 1.2.14、C 1.0.1、RecoveryJoin 1.0.2、RecoveryCutoff 1.0.5、H 集成 Authority Mapping 和当前 C/D/I 42-test Review Blob。**B 裁决：** L1/L2 候选层 CONDITIONALLY ALIGNED，基线为 v3.3.0；A 现在必须精确审查 v3.3.0 和 Option A 拓扑 ADR。生产 Callback 仍为 Test Double；生产 C/I Trust、D Lineage/Release、COC Quorum、JF-10、Same-GID Recovery、Gate B/C、Global Forget 和 Full Applied 仍 OPEN。
