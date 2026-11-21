# Phase 2 领域扩展规格

- Work Item：GAP-05 / GAP-BASELINE-001
- Owner：B — Domain Model Architect
- 状态：PROPOSED — 仅规格；不代表实现、Schema 冻结或验收
- 基线：`1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9`
- 语言配对：本文与 `phase-2-domain-extension.md` 具有相同规范语义

## 1. 决策与范围

Phase 1 已实现为有明确边界的最小领域核心。Phase 2 有充分依据：Phase 1 领域文档和下游 G 契约要求不可变断言修订，以及比当前 Rust 模型更完整的规范指代对象和血缘语义。

这是对现有模型的**窄范围扩展**，不是替换 Phase 1，也不表示旧版领域总览中的所有概念都已获准立即实现。

Phase 2 范围：

1. 将 Claim 身份与不可变 ClaimRevision 状态分离。
2. 独立的 Fact / FactRevision Attestation 概念，但受 §8 的 D/I 边界决策约束。
3. 完整的领域级 Entity 身份和 Relation 类型化关联语义。
4. Evidence 记录及明确的 Claim/Relation Evidence 角色。
5. 显式 Provenance 血缘和类型化 MemorySource 关联。
6. 足以区分发生时间、记录时间和有效时间，且不虚构确定性的时间精度语义。

Phase 2 **不包括** Phase 3、运行时检索/排序、编译器提取、Context 规划/版本生命周期、BMCP Wire Schema、Storage DDL/事务机制、授权策略、密码学信任或物理 Forget 实现。

## 2. 基于证据的缺口评估

| 缺失或建模不足的概念 | 被何处需要 | Phase 1 现状 | Phase 2 处置 |
|---|---|---|---|
| ClaimRevision 与精确 ClaimRevisionRef | `domain-model-overview.md` §2.4；`06-memory-context/context-versioning.md` §§13.2–13.3 要求精确不可变 ClaimRevision 引用 | 当前 `Claim` 合并了命题和断言状态；没有独立 Revision 类型 | 纳入 |
| Fact 与 FactRevision | Domain Overview §3.15；G Context Versioning §13.3 要求精确 FactRevision 引用 | Rust 无对应类型 | 纳入，但设 D/I 决策门 |
| Entity 身份元数据和生命周期 | `core-entities.md` §6；relationships/provenance 与 lifecycle 文档 | `Entity` 仅有 ID、类型、标签和 Scope | 纳入，扩展 Entity |
| 类型化 Relation 语义 | `core-entities.md` §7；`relationships-and-provenance.md` §§2–3 | `Relation` 仅有字符串类型、不透明端点和 Scope | 纳入，扩展 Relation |
| Evidence 来源/定位/可用性及关联角色 | `core-entities.md` §8；relationships/provenance §4 | `Evidence` 有来源、记录时间、Scope 和角色；缺少 kind、locator、观察时间、采集者、完整性及可用性 | 纳入，扩展 Evidence |
| Provenance 派生图和 MemorySource | `core-entities.md` §9；relationships/provenance §5 | `Provenance` 是扁平记录；`MemorySource` 已存在但字段不足 | 纳入，扩展 |
| 时间精度与显式有效时间语义 | `epistemic-and-temporal-semantics.md` §§5–6 | `TimeValue` 仅为字符串 Instant/Interval/Unknown；没有精度、时区、确定性或原始时间表达 | 纳入，扩展 |
| Context identity、budget、ContextVersion、delivery 和 reconciliation | `06-memory-context/`；GAP-02 | G 所有；Phase 1 已有 `MemoryContext` 和 `ContextEntry` | 不属于 B 范围；由 G 负责 |
| Producer ledger namespace、ForgetFence currentness 和 watermarks | `08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md` | 无对应领域类型；属于 D/H/I 权威和 BMCP 协议事项 | 不属于 B 范围 |
| Permission、Attestor 授权、安全主体和 Trust Root | `scope-and-permission-model.md`；BMCP currentness 契约 | Phase 1 刻意将 Scope 与 Permission 分离 | 不属于 B 范围；安全决策由 I 负责 |

G 契约构成明确的下游依赖：引用 ClaimRevision 或 FactRevision 的 ContextVersion 必须固定精确不可变 Revision，不得跟随当前 Claim Head。这不会把 ContextVersion 语义的所有权转移给 B。

BMCP 契约中的 ProducerWork Registration Ledger Namespace 和 ForgetFence Currentness Proof 并非缺失的领域实体。它们是具有明确 D/H/I 所有权的协议/治理构造。B 不得为它们创建影子领域类型。

## 3. Phase 2 领域定义

### 3.1 Claim 身份与 ClaimRevision

**Claim** 是一个命题的稳定身份。它包含 ClaimRef 以及该命题所属的 Scope 身份。它本身不是可变的断言状态。

**ClaimRevision** 是某个 Claim 的一个不可变断言状态。它包含 ClaimRevisionRef、ClaimRef、可选的精确父 ClaimRevisionRef、命题字段（subject、predicate、object、polarity 和实质限定条件）、epistemic status、valid-time 引用、Evidence 引用、Provenance 引用、断言时间以及更正/修订原因。

**不变量（可测试）：**

- 每个 ClaimRevision 必须且只能引用一个已存在的 ClaimRef。
- 每个 ClaimRevisionRef 唯一标识一个不可变 Revision，且永不复用。
- 非初始 Revision 必须且只能有一个属于同一 ClaimRef 的父 Revision；初始 Revision 不得有父 Revision。
- Revision 被接受后不得原地修改；更正必须追加新 Revision。
- DOMAIN-MODEL-001 §2.4 的 CI-01 至 CI-08 将命题实质变化分类为 NEW_CLAIM，并要求显式血缘；CI-09 至 CI-13 将 Evidence/Provenance/状态/评估/编辑变化分类为 NEW_REVISION，并保留 ClaimRef。
- Scope 变化不得静默转移 ClaimRef；必须使用新的 ClaimRef 和显式血缘。
- 受治理身份分类存在歧义时必须拒绝自动分类；不得静默默认 NEW_REVISION。
- 下游引用（包括 G ContextVersion）只能解析精确 ClaimRevisionRef；不得用语义相似性或最新 Head 替代。

**与 Phase 1 的关系：** Claim 被细化而非移除。ClaimRevision 是新增类型。现有 Claim 中描述断言状态的字段迁移到 Revision 表示；稳定命题身份保留在 Claim 上。

### 3.2 Fact 与 FactRevision

**Fact** 是具有独立身份、受治理的 Attestation。它既不是高 Confidence 的 Claim，也不是 Verified Claim 的同义词。

**FactRevision** 是该 Attestation 的不可变修订。它绑定精确 FactRef 和 FactRevisionRef；精确 ClaimRevisionRef 集合；精确 EvidenceRef 和 ProvenanceRef 集合；ScopeRef；valid-time 与 recorded/commit-time 引用；Attestor 引用；精确 Attestation Method 标识/版本；I AuthorizationDecisionRef；结果、理由及更正/撤销血缘。

**不变量（可测试）：**

- FactRef、FactRevisionRef 与 ClaimRef、ClaimRevisionRef 相互独立。
- 每个 FactRevision 固定一个或多个精确 ClaimRevisionRef；不得跟随 Claim 当前 Head。
- 每个 FactRevision 固定精确 EvidenceRef、ProvenanceRef 和一个 Scope 身份。
- Confidence 单独存在以及 Verified 状态单独存在均不得创建 Fact。
- 更正、撤回或重新评估必须追加 FactRevision；不得覆盖历史 Revision。
- 缺少必需授权引用或授权引用未解析的 FactRevision，不具备被接受并规范发布的资格。
- 共享 Fact 不会授予对其关联 ClaimRevision、Evidence 或 Provenance 的访问权。

**与 Phase 1 的关系：** 两种类型均为新增，不替换 Claim 或 Evidence。

**PENDING CROSS-OWNER DECISION：** I 必须定义/批准 Attestor 主体身份、授权决定语义，以及授权引用的安全含义。D 必须确认 Fact/FactRevision 的规范提交、Revision 和 Forget/依赖语义。在两个决策绑定到同一精确契约版本之前，这些字段仅是语义占位引用；实现不得自行推断授权或规范接收结果。

### 3.3 Entity 身份

Entity 仍是具有身份的指代对象，并扩展 identity status、aliases、带 Scope 的外部标识符、身份 Evidence、当前身份/Profile 版本引用，以及 merge/split 血缘引用。

**不变量（可测试）：**

- EntityRef 是不透明、类型化、稳定且永不复用的标识符。
- 显示标签、别名、mention 文本或 embedding 相似性本身不能证明身份相同。
- 外部标识符必须命名空间化；唯一性只在声明的命名空间和适用 Scope 内评估。
- 指代对象发生变化不是标签更正：必须创建新 Entity 身份和显式血缘。
- Merge/split 必须保留源身份和可审计的重定向/引用迁移记录；不得静默重写历史引用。
- 合并后的 Entity 必须标识其后继；拆分必须标识结果身份及引用的受治理分配。
- Identity status 与 Memory lifecycle 相互独立。

**与 Phase 1 的关系：** 在语义层面扩展现有 Entity。本规格不强制新增独立 EntityVersion 类型；不可变身份/Profile Revision 的存储方式由 D/Storage 决定。

**PENDING CROSS-OWNER DECISION：** D 必须决定 Entity 身份变更和 merge/split 血缘如何提交，以及如何迁移规范引用而不重写不可变历史。

### 3.4 Relation

Relation 仍是类型化关联，并扩展为具有类型化端点、方向性、结构化限定条件、可选 valid time、epistemic status、Evidence 引用和 Relation lifecycle state。

**不变量（可测试）：**

- 两个端点都是类型化引用，且端点类型均被注册的 Relation 定义允许。
- Relation 类型、方向性、逆向/对称行为和唯一性必须依据带版本的词汇表校验。
- 共同出现或 embedding 相似性不能创建 Relation。
- 缺少 valid time 表示未指定/未知，不代表永恒有效。
- 跨 Scope Relation 引用必须有明确共享授权；Scope 兼容本身不授予权限。
- proposed、active、superseded、retracted 是不同 Relation 生命周期状态，不得与 MemoryLifecycle 或 Claim epistemic status 混用。
- 撤回/替代必须保留历史和原因；不得原地重写语义。

**与 Phase 1 的关系：** 在语义层面扩展现有 Relation。本规格不定义 Relation 词汇注册表或物理图表示。

**PENDING CROSS-OWNER DECISION：** D 必须确认 Relation 变更的规范持久化/版本及引用一致性。I 拥有跨 Scope 引用的授权语义。精确 Relation 词汇治理流程在 B 的领域范围内仍为 OPEN，本规格不予冻结。

### 3.5 Evidence

Evidence 仍是支持、反驳、限定或提供上下文的来源材料/观察。扩展字段包括 Evidence kind、类型化来源引用、可选 locator/content 引用、观察时间、采集者 ActorRef、完整性 Digest、来源可靠性引用和可用性状态。

**不变量（可测试）：**

- 每个 Evidence 具有一个稳定 EvidenceRef、一个类型化来源引用、至少一个 ScopeRef 和记录时间。
- Evidence 角色必须明确，且仅限 supports、refutes、qualifies 或 context-only。
- Evidence 不是 Confidence 分数，也不是 Provenance 记录。
- 仅有可变外部 URL 不构成持久保留的 Evidence。
- 来源 Payload 不可用/受限/已遗忘时必须显式表示；不得重建或伪造缺失内容。
- Evidence 可见性必须独立授权，且可以比关联 Memory 或 Claim 更窄。
- 新增 Evidence 不改变 Claim 身份；当断言的 Evidence 状态发生变化时，应创建 ClaimRevision。

**与 Phase 1 的关系：** 在语义层面扩展现有 Evidence。现有 EvidenceRole 变体仍然有效。

**PENDING CROSS-OWNER DECISION：** I 拥有受保护来源 Payload 的访问/授权及隐私分类。D 拥有规范保留和 Forget 依赖处理。B 不定义这两类策略。

### 3.6 Provenance 与 MemorySource

Provenance 是显式派生血缘记录。扩展字段包括 target 引用、类型化/带版本的 source edges、派生类型、method/component 版本引用、derived-at 时间、输入 Digest 引用、父 Provenance 引用，以及明确的 unavailable reason。

MemorySource 是 MemoryVersion/派生资产与一个来源之间的类型化关联，包含来源角色、可选 locator、Scope 和创建时间。

**不变量（可测试）：**

- 每个派生规范 Revision 必须具有至少一条完整血缘路径，或具有经其治理策略接受的显式 unavailable reason。
- 每条 source edge 必须标识来源对象；存在带版本来源时必须标识精确版本。
- Provenance 解释来源/派生过程；Evidence 提供支持材料，两者不可互换。
- Method/model 身份是过程元数据，不是正确性证明。
- 来源材料缺失时必须标记 unavailable，不得伪造。
- Provenance 历史只能追加；更正应增加血缘，不得重写旧 Provenance。
- MemorySource 不会将来源材料变成结果 Memory，也不隐含读取来源的权限。
- 具有共同祖先的重复派生物不能仅因重复就成为独立佐证 Evidence。

**与 Phase 1 的关系：** Provenance 和 MemorySource 均为扩展；MemorySource 已在 Rust 中存在，但建模不足。

**PENDING CROSS-OWNER DECISION：** D 必须确认 Provenance edge 和 MemorySource 引用的原子/可恢复提交及 Forget 依赖语义。E 拥有编译派生方法和输入 Digest 的生产语义；B 不定义 E 的流水线。

### 3.7 时间语义

扩展 TimeValue/TemporalRef，以保留精度、时区、确定性、来源表达，以及 Event Time、Recorded At、Valid Time 和（若由 D 采纳）规范提交/事务时间之间的区别。

**不变量（可测试）：**

- 未知时间必须显式表示，绝不能视为永恒有效。
- Event Time、Recorded At、Valid Time 和保留时间是不同维度，不得互相替代。
- 近似时间或来源报告时间必须保留来源表达及不确定性；规范化不得虚构精度。
- 适用区间语义时，Valid interval 使用声明的半开区间约定 [start, end)。
- 时间点断言必须具有时间点语义，不得扩展为虚构时长。
- 解析失败必须保留原始文本，并产生显式 unknown/un-normalized 值。
- 时间变化必须通过 Revision 表达；不得覆盖历史有效时间。

**与 Phase 1 的关系：** 扩展 TimeValue 和 TemporalRef；现有 Instant/Interval/Unknown 变体需要兼容映射。

**PENDING CROSS-OWNER DECISION：** D 必须决定规范提交/事务时间属于领域对象，还是仅属于规范存储元数据。F 拥有时间查询行为；本规格不定义检索语义。

## 4. Phase 2 排除项与 Owner 边界

本规格刻意不向 `memory-domain` 新增以下内容：

- G 所有的 ContextIdentity、ContextBudget、ContextVersion、ChangeSet、delivery intent、reconciliation 或 applied-delivery lifecycle。现有 MemoryContext/ContextEntry 保持为有界 Phase 1 领域引用；Context 行为由 G 负责。
- H 所有的 BMCP message、wire field、schema version、ProducerWork Registration Ledger namespace 和 delivery/fence proof 表示。
- D 所有的 Canonical Memory Authority、commit cursor、ForgetFence state machine、producer admission ledger、持久化事务协议和物理 Forget 语义。
- I 所有的 principal、认证身份、凭据、grant、permission policy、Attestor 授权、隐私和 trust-root 决策。
- E 所有的 compiler stage、extraction、inference、model/method 执行和派生记忆生产。
- F 所有的 retrieval、ranking、activation 和 temporal query 执行。

ScopeRef 仍是领域适用范围/命名空间引用，不是授权 Grant。OPEN 的 Scope composition algebra 不会被本扩展静默裁定。

## 5. 对 Phase 1 Rust 模型的迁移影响

基线 `crates/memory-domain/src/lib.rs` 为 679 行、13 个单元测试。本规格不修改该文件。未来获得授权的实现将影响以下现有声明/验证/测试：

| 现有代码区域 | 未来所需变更 |
|---|---|
| `Claim` 结构体与 `Claim::validate` | 将稳定命题身份与不可变 ClaimRevision 断言字段分离；增加 Revision parent 和精确引用校验 |
| `MemoryVersion.claims` 与 `MemoryVersion::validate` | 用精确不可变 ClaimRevision 引用/快照替换或版本化嵌入 Claim 快照表示；与 D 协调规范持久化 |
| `Entity` 结构体 | 增加 identity status、aliases、带 Scope 的外部标识符、identity Evidence 和 merge/split 血缘 |
| `Relation` 结构体 | 将非类型化端点 ID 替换为类型化引用；增加 directionality、qualifiers、valid time、epistemic/lifecycle state 和 Evidence 引用 |
| `Evidence` 与 `EvidenceRole` | 增加 kind、类型化来源、locator、观察/记录时间、collector、integrity 和 availability |
| `Provenance` 与 `MemorySource` | 增加类型化 target/source edges、派生 method/version、输入 Digest、parent lineage 和显式不可用状态 |
| `TimeValue` 与 `TemporalRef` | 增加 precision/timezone/certainty/source phrase 和显式 valid-time 表示，不与 recorded time 混淆 |
| `DomainError` | 增加类型化引用错误、Revision parent/identity 不匹配、Relation endpoint 无效、身份分类歧义和血缘不完整等确定性错误 |
| 构造器及现有 13 个测试 | 更新 fixtures 并增加不变量测试；保留 Phase 1 行为和回归覆盖 |

由于当前未授权实现，本规格不规定逐行补丁。迁移必须保留既有序列化数据，或使用明确版本化的转换。只有当命题身份和历史无歧义时，旧 Claim 记录才可映射为初始 ClaimRevision。存在歧义的记录必须隔离并交由受治理流程解决；不得自动合并或静默分配新身份。

## 6. Phase 2 必需测试清单

未来实现至少必须提供以下确定性测试：

- DM2-01：多个 Revision 之间 ClaimRef 稳定，ClaimRevisionRef 唯一。
- DM2-02：无效/不匹配的 Revision parent 被拒绝；已接受 Revision 不可变。
- DM2-03：所有 CI-01–CI-13 分类向量产生规定的 NEW_CLAIM/NEW_REVISION 结果。
- DM2-04：精确 ClaimRevisionRef 解析；禁止替换为当前 Head。
- DM2-05：Fact 与 Claim 身份不同；FactRevision 固定精确 ClaimRevision/Evidence/Provenance。
- DM2-06：缺失或无效的 I 授权引用阻止 Fact 发布（I 决策冻结之后）。
- DM2-07：Entity label/alias 不会合并身份；指代对象变化要求新身份和血缘。
- DM2-08：无效类型化 Relation endpoint 和未注册 Relation 类型被拒绝。
- DM2-09：Relation 的时间/Scope/lifecycle 维度保持独立。
- DM2-10：Evidence role、availability 和 source Scope 独立执行约束。
- DM2-11：Provenance source/version lineage 或显式 unavailable reason 为必需项。
- DM2-12：共同来源祖先不得被计为独立 Evidence。
- DM2-13：未知/近似时间不得升级为精确时间或永恒有效。
- DM2-14：Phase 1 序列化/迁移兼容性及全部 13 项 Phase 1 回归测试保持有效。

这些是未来实现的验收要求，不代表测试已经编写或运行。

## 7. 明确保留的未决事项

- Relation vocabulary registry 的治理及兼容/版本策略。
- 正式 Scope composition algebra。
- 模糊/近似时间的规范表示细节。
- Entity Profile Revision 是否需要一等 EntityVersion 类型。
- Provenance DAG 的环和压缩策略。
- 物理 Schema、DDL、序列化和公开 API。
- D 规范提交/Forget 集成。
- I 安全/Attestor 授权契约。
- H Wire 映射和 Schema。
- 实现及符合性状态。

## 8. 跨 Owner 决策登记表

| ID | 准确问题 | 责任 Owner | 退出条件 |
|---|---|---|---|
| B-P2-XO-01 | B 可以存储何种精确的领域侧 Attestor 引用？哪个 I 签发的 AuthorizationDecisionRef 能证明 Attestor 对该 Fact/Scope/Method 有授权？ | I（安全权威）、B（领域绑定） | I 发布/接受安全侧引用契约；B 与 I 对同一精确版本/SHA 达成一致；D 确认规范持久化引用处理 |
| B-P2-XO-02 | ClaimRevision/FactRevision 及其 Evidence/Provenance edge 适用何种规范提交、不可变 Revision、依赖登记和 Forget 语义？ | D，与 B 协作 | D 接受精确领域引用/提交边界及依赖/Forget 处理；B 记录双方认可的绑定，不修改 D 契约 |
| B-P2-XO-03 | Entity merge/split 身份血缘和历史类型化引用迁移如何提交，同时不重写不可变历史？ | D，与 B 协作 | D 确认规范提交/历史机制；B 仅冻结领域侧含义 |
| B-P2-XO-04 | Relation 跨 Scope 引用如何授权，策略决定如何绑定类型化端点？ | I，与 B 协作 | I 定义授权绑定；B 保留 Scope 语义，不定义 Grant |
| B-P2-XO-05 | 规范提交/事务时间属于领域时间对象，还是仅属于存储元数据？ | D，与 B 协作 | D 给出明确决定；B 据此调整 TemporalRef，不预设存储语义 |

以上五项均为 **PENDING CROSS-OWNER DECISION**。本规格不单方面决定安全、规范持久化、Forget 或 Wire 语义。

## 9. Phase 边界与状态

- Phase 1：有界核心已实现；本文不重新开启其已接受不变量。
- Phase 2：本文规格状态为 PROPOSED；未来实现须先解决所列跨 Owner 决策并获得单独授权。
- Phase 3：未评估，且不声称完成。

没有修改代码。本规格任务未运行测试。不声称自我批准或验收。

## 10. 参考资料

以下仓库资料均在基线 `1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9` 回读：

- `02-domain-model/domain-model-overview.md`
- `02-domain-model/core-entities.md`
- `02-domain-model/relationships-and-provenance.md`
- `02-domain-model/epistemic-and-temporal-semantics.md`
- `02-domain-model/lifecycle-model.md`
- `02-domain-model/scope-and-permission-model.md`
- `02-domain-model/phase-1-domain-model-freeze.md`
- `02-domain-model/phase-1-memory-store.md`
- `02-domain-model/phase-1-sqlite-adapter-contract.md`
- `02-domain-model/phase-1-storage-trait-contract.md`
- `crates/memory-domain/src/lib.rs`
- `06-memory-context/context-versioning.md`
- `06-memory-context/context-architecture.md`
- `08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md`
- `14-ai-development/work-items/GAP-BASELINE-001.md`
- `14-ai-development/prompts/owners/B/owner-session-v2.md`
- `14-ai-development/prompts/global/chatgpt-session-contract-v1.md`
