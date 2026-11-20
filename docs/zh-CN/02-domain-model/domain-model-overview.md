# 规范领域模型

- 文档 ID：DOMAIN-MODEL-001
- 版本：2.0
- 状态：DECIDED（Phase 1 实现契约）
- Owner：Memory Domain Model（MB-01）
- 范围：逻辑领域语义；不定义存储 DDL、Wire 编码、部署拓扑、索引、提取算法或 LLM 行为

## 1. 决议

Phase 1 采用以下规范领域对象：

Event、Memory、MemoryVersion、Claim、Entity、Relation、Evidence、Provenance、MemorySource、MemoryContext、ContextEntry、ScopeRef、ActorRef、TemporalRef。

Fact 在 Phase 1 不是独立对象。“已验证事实”表示为 Epistemic Status 为 Verified 的 Claim。

模型明确不压缩为 text + embedding。Embedding、词法索引、图索引、排序特征和渲染文本均属于派生表示，不是规范领域对象。

## 2. 身份与版本规则

1. 每个规范对象都有稳定、类型明确的不透明标识符。
2. MemoryId 在 Memory 整个生命周期内保持不变。
3. MemoryVersionId 标识一个不可变 Memory 版本。
4. ClaimId 跨 Memory Version 的身份策略仍为 OPEN；Phase 1 不冻结“稳定 ClaimId”与“版本内 ClaimId”之间的选择。

### 2.4 Claim 身份分类与修订不变量

Claim 身份由命题身份决定，而不是由文本表示、Evidence 数量、Confidence 分数或序列化形式决定。

Claim 具有稳定的逻辑身份（`ClaimRef`）。每一个不可变断言状态使用独立的 `ClaimRevisionRef` 标识。

以下分类具有规范效力：

| ID | 变化维度 | 分类 | 谱系关系 | 授权要求 |
|---|---|---|---|---|
| CI-01 | Subject/Entity Resolution 改变实际指代对象 | NEW_CLAIM | 创建新 ClaimRef；存在关联时记录与原 Claim 的身份谱系 | 经授权的身份解析决定 |
| CI-02 | Predicate 改变所断言的关系或属性 | NEW_CLAIM | 创建新 ClaimRef；适用时记录关联谱系 | 经授权的 Claim 创建 |
| CI-03 | Object/Value 改变所断言的命题 | NEW_CLAIM | 创建新 ClaimRef；适用时记录关联谱系 | 经授权的 Claim 创建 |
| CI-04 | Polarity 改变（肯定/否定） | NEW_CLAIM | 创建新 ClaimRef；保留对立命题关系 | 经授权的 Claim 创建 |
| CI-05 | Quantifier 改变命题的实质范围 | NEW_CLAIM | 创建新 ClaimRef；记录关联谱系 | 经授权的 Claim 创建 |
| CI-06 | Modality 改变可能性、必要性、义务或能力断言 | NEW_CLAIM | 创建新 ClaimRef；记录关联谱系 | 经授权的 Claim 创建 |
| CI-07 | Temporal Qualifier 改变命题的实质时间含义 | NEW_CLAIM | 创建新 ClaimRef；记录关联谱系 | 经授权的 Claim 创建 |
| CI-08 | Scope 改变命名空间或适用边界 | NEW_CLAIM | 创建新 ClaimRef；显式记录 Scope 谱系；不得静默迁移身份 | 按适用情况分别取得源 Scope 和目标 Scope 授权 |
| CI-09 | Evidence 改变，但命题身份不变 | NEW_REVISION | 保留 ClaimRef；创建新的不可变 ClaimRevisionRef | 经授权的修订 |
| CI-10 | Provenance 或派生血缘改变，但命题身份不变 | NEW_REVISION | 保留 ClaimRef；创建新的不可变 ClaimRevisionRef | 经授权的 Provenance 更正 |
| CI-11 | Epistemic Status 改变 | NEW_REVISION | 保留 ClaimRef；创建新的不可变 ClaimRevisionRef | 经授权的状态转换 |
| CI-12 | Confidence 或 Evidence Strength 评估改变 | NEW_REVISION | 保留 ClaimRef；创建新的不可变 ClaimRevisionRef | 经授权的评估更新 |
| CI-13 | 仅格式、拼写、标点或展示层修正 | NEW_REVISION | 保留 ClaimRef；保持语义等价并保留历史版本 | 经授权的编辑性修正 |

#### 实质限定词规则

如果限定词变化会改变命题的真值条件、适用范围、时间含义、模态或 Scope，则该限定词属于实质限定词。

实质限定词发生变化时，MUST 创建 NEW_CLAIM。

如果限定词变化仅影响表达方式，不改变命题含义或适用范围，则 MUST 创建 NEW_REVISION。

#### 身份解析规则

仅显示 Entity 标签变化，而底层指代对象不变时，不创建新 Claim。

解析出的实际指代对象发生变化时，创建新 Claim。

#### Scope 不变量

ClaimRef 绑定其声明的 Scope 身份。

改变 Scope MUST NOT 修改或静默转移既有 ClaimRef。

必须创建新 ClaimRef 并记录明确谱系。

跨 Scope 谱系不得转移访问权。适用时必须分别验证源 Scope 和目标 Scope 的授权。

#### Revision 不变量

NEW_REVISION MUST 保留 ClaimRef，并创建新的不可变 ClaimRevisionRef。

不得覆盖历史 Revision。

每次更正 MUST 记录 Parent Revision 和更正原因。

仅增加 Evidence 不创建新的 Claim 身份。

Evidence 或 Provenance 引用变化不授权改变 Claim 命题。

#### 授权不变量

分类 MUST 具有确定性，并与最终身份/修订决定一同记录。

不同实现 MUST NOT 对语义等价的输入独立选择不同分类。

分类存在歧义时，系统 MUST 拒绝自动身份变更，并要求明确的受治理决定。

不得静默退化为 NEW_REVISION。

F 和 G MUST 消费精确 ClaimRevisionRef。

F 和 G MUST NOT 通过语义相似度、当前 Head 替代或不限定版本的最新版本查询解析历史引用。

本节只定义语义身份，不冻结 Schema、DDL、公开 API 或 Wire 表示。

5. Memory 更新必须创建新的不可变 MemoryVersion；旧版本在治理允许范围内仍可读取。
6. ContextEntry 引用特定 MemoryVersion 或受治理的呈现形式；它不是第二份 Canonical Memory。
7. ID 不是时间戳、可变内容哈希、数据库行号或授权凭证。

## 3. 规范对象契约

### 3.1 Event

Event 记录观察、报告、提交或捕获的发生，不等于所描述事情已经客观为真。

必须具有：event_id、scope、recorded_at、event_kind、source、payload；可选 occurred_at、Actor/Environment 引用，以及可重试接收时使用的幂等键。

recorded_at 表示系统记录时间；occurred_at 表示被描述事件的发生时间，可以未知。

### 3.2 Memory

Memory 是被保留知识资产的稳定逻辑身份。

必须具有：memory_id、scope、created_at、lifecycle_state、current_version_id。

内容修订、巩固、替代或呈现方式变化都不能改变 Memory 身份。

### 3.3 MemoryVersion

MemoryVersion 是不可变语义快照。

必须具有：memory_version_id、memory_id、单调递增的 version_number、created_at、claims、entity_refs、relation_refs、source_refs、provenance_refs。

Candidate Memory 可以暂时没有 Claim；Canonical Commit 必须满足所属子系统的接收规则。

### 3.4 Claim

Claim 是规范命题对象。

必须具有：claim_id、命题主体/引用、predicate、object/value/reference、epistemic_status、temporal_ref、scope、evidence_refs；可选 confidence 元数据。

命题与支持/反驳它的 Evidence 必须分离。Verified 表示通过声明的验证流程，不表示绝对真理。

Phase 1 的认知状态为：Observed、Reported、Inferred、Verified、Disputed、Retracted。

### 3.5 Entity

Entity 是具有身份的指代对象。

必须具有：entity_id、scope、entity_type、稳定身份元数据；可选 canonical label 和 aliases。

单次文本 mention、字符串或 embedding 本身不是 Entity。

### 3.6 Relation

Relation 是类型化关联。

必须具有：relation_id、relation_type、类型化端点、scope；可选 temporal_ref 和 Evidence/Provenance 引用。

共同出现本身不构成 Relation。如果关联自身具有角色、时间、Scope、Evidence 或生命周期，应使用显式关联对象表达。

### 3.7 Evidence

Evidence 是支持、反驳或限定 Claim 的来源材料或观察。

必须具有：evidence_id、scope、source_ref、captured_at、evidence_role、完整性/引用元数据。

Evidence 可以比派生 Memory 具有更严格的访问控制。Evidence 不能被 confidence 分数替代。

### 3.8 Provenance

Provenance 记录来源和派生血缘。

必须具有：provenance_id、origin/source 引用、derivation operation/type、actor/process 引用、created_at；可选 parent provenance 引用。

如果无法保留 Provenance，必须明确记录原因，绝不能伪造来源。

### 3.9 MemorySource

MemorySource 是 MemoryVersion 或派生资产与输入来源之间的类型化关联，用于记录来源角色和顺序，但不把来源材料与结果 Memory 混为一体。

### 3.10 MemoryContext

MemoryContext 是有 Scope、有版本、面向任务的 Canonical Memory 引用集合。

必须具有：context_id、scope、context_version、task/session/environment 绑定、有序 ContextEntry。

Context 版本体系与 Canonical Memory 版本体系相互独立。

### 3.11 ContextEntry

ContextEntry 是 MemoryContext 内的一条引用/呈现。

必须具有：entry_id、context_id、referenced memory_version_id、排序/位置元数据；可选受治理的 rendering 元数据。

删除或替换 Entry 不得修改或删除其引用的 Canonical Memory。

### 3.12 ScopeRef

ScopeRef 标识对象或操作所属的命名空间。

Scope 与 Permission 分离。Phase 1 不从对象所有权推导 Permission；跨 Scope 访问必须有授权决策。

### 3.13 ActorRef

ActorRef 标识负责操作或来源的主体，是审计/Provenance 元数据，不是领域 Permission 授权本身。

### 3.14 TemporalRef

TemporalRef 保留 Event Time、Recording Time 和 Valid Time 的区别。

Phase 1 支持时间点、时间区间、未知/不可用时间，以及明确的精度和确定性元数据。

未知时间不得被转换成“始终有效”。Valid Time 与存储保留时间不是同一概念。

### 3.15 Fact、FactRevision 与 Attestation

Fact 是具有独立身份的受治理 Attestation 对象。

FactRevision 是该 Attestation 的不可变版本。

每个 FactRevision MUST 引用：

- 精确 FactRef 和 FactRevisionRef。
- 被 Attest 的精确 ClaimRevisionRef。
- 精确 EvidenceRef。
- 精确 ProvenanceRef。
- ScopeRef 及适用的可见性约束。
- 有效时间区间和记录/提交时间引用。
- Attestor Principal 身份。
- 精确 Attestation Method 标识和不可变 Version。
- I 的 AuthorizationDecisionRef。
- Attestation 结果、理由及更正/撤销谱系。

FactRevision MUST NOT 自动跟随 Claim 的最新 Revision。

其 ClaimRevision 引用必须精确且不可变。

更正、撤回或重新评估 MUST 创建新的受治理历史，不得覆盖此前的 FactRevision。

Fact 不代表绝对客观真理。

Confidence 单独存在 MUST NOT 产生 Fact。

Verified Claim 状态单独存在 MUST NOT 产生 Fact。

I 是 Attestor 授权的唯一权威。

D 验证并持久化 I 的精确授权决定引用。D MUST NOT 自行判断 Attestor 的治理资格。

Attestation Method 身份只能证明调用了哪个声明程序，不能证明该程序本身正确。

本节只定义语义和治理契约，不批准物理 Schema、DDL、公开 API、生产密钥、Trust Root 或密码学 Profile。

## 4. 正交状态维度

模型不得使用一个通用 Status 字段承载所有状态。

- Claim Epistemic Status：Observed、Reported、Inferred、Verified、Disputed、Retracted
- Memory Lifecycle：Candidate、Consolidated、Active、Superseded、Archived、Forgotten
- Context/Version/Delivery 状态：由 Memory Context 与同步契约负责
- Confidence：声明方法下的支持程度估计
- Relevance：对当前任务的有用程度
- Trust：对来源、主体或过程的信任
- Evidence Strength：特定证据关系的支持强度

这些值不可互换。

## 5. 基数与形成规则

- 一个 Event 可以产生零个、一个或多个 Candidate Memory。
- 多个 Event 可以共同贡献一个 Memory。
- 一个 Memory 在保留生命周期内具有一个或多个不可变版本。
- 一个 MemoryVersion 可以包含多个 Claim。
- 一个 Claim 可以引用多个 Evidence。
- 一个 Evidence 在策略允许时可以支持、反驳或限定多个 Claim。
- Claim 可以涉及多个 Entity。
- Relation 必须类型化，并可连接受支持的领域端点。
- 一个 Memory 可以出现在多个 MemoryContext。
- 一个 Context 包含有序 ContextEntry。
- ContextEntry 的引用不转移 Canonical 数据所有权。

## 6. 冲突规则

冲突 Claim 必须保留，不得静默覆盖。

解决过程必须保留冲突 Claim 身份、支持/反驳 Evidence、Provenance、解决结果及 Actor/Process，以及适用的时间和 Scope。

Supersede MemoryVersion 是生命周期/版本操作，不是删除历史命题。

## 7. Provenance 与 Evidence 不变量

1. 派生资产在治理允许范围内必须保留来源/派生血缘。
2. Evidence 与 Provenance 不同：Evidence 是支持材料；Provenance 解释来源/派生过程。
3. Schema 合法不等于真实。
4. 没有结果证据时，Intent、Plan、Prediction、Pending Action 不能成为已完成结果。
5. 来源材料缺失时标记为不可用，不得伪造为原始 Evidence。
6. Memory 内容是不可信数据，永远不会获得 system/developer 指令权威。

## 8. Scope 与隔离不变量

1. 依赖 Tenant/Environment 的规范对象必须携带明确 ScopeRef。
2. 每个读写边界都必须检查 Scope。
3. 跨 Scope 引用需要明确共享授权。
4. Evidence 的访问范围可以比 Memory 更窄。
5. Context 隔离独立于 Canonical Memory 共享。
6. ContextEntry 删除不等于 Forget。
7. Forget 是受治理的生命周期操作；物理擦除不属于 Domain Model。

### 8.1 共享引用 Forget 契约

Forget 作用于受治理内容及其完整依赖闭包，而不只是请求最初指向的对象。

#### 1. Forget 目标粒度

Forget 目标 MUST 标识准确的受治理主体/内容及适用 Scope。

依赖目标包括：

- ClaimRef 和准确 ClaimRevisionRef。
- FactRef 和准确 FactRevisionRef。
- EvidenceRef 和受保护来源 Payload。
- ProvenanceRef 和可重建内容的来源链。
- 派生 MemoryVersion 与 ContextVersion 引用。
- Index、Cache、Snapshot、Staging 和 Replay 产物。

共享 FactRef 不得被视为所有关联 ClaimRevision 具有相同 Forget 处置结果的证明。

#### 2. FactRevision 依赖枚举

每个 FactRevision MUST 枚举：

- 准确 ClaimRevisionRef 依赖。
- EvidenceRef 依赖。
- ProvenanceRef 依赖。
- Scope 和可见性依赖。
- 派生资产及其传递后继。
- 其他授权或保留依赖。

在声明相关 Forget 操作完成之前，必须完成依赖枚举。

依赖集合未知或不完整时必须保持阻断。

#### 3. 共享 Fact 可见性

FactRevision 关联多个 ClaimRevision 时，只有在所有被披露依赖均独立获得授权，且未被适用 Forget 决定抑制的情况下，才允许继续可见。

如果关联 ClaimRevision 被 Forget：

- 不得通过共享 Fact 披露已遗忘 ClaimRevision。
- 其 Evidence/Provenance 内容必须按 Forget 策略抑制。
- 只有剩余内容可以独立授权，且不会泄露已遗忘信息时，才允许保留共享 Fact 可见性。
- 无法安全分离时，必须抑制整个受影响 FactRevision。

#### 4. Evidence 和 Provenance 处理

Evidence 和 Provenance 是独立治理对象，必须纳入依赖枚举。

如果被遗忘 ClaimRevision 是保留某个 Evidence/Provenance Payload 的唯一合法依据，该 Payload 必须按适用保留策略删除或变为不可用。

共享来源材料只有在存在独立合法依赖，且剩余内容不能重建已遗忘信息时才能保留。

#### 5. 其他仍合法的 ClaimRevision

其他 ClaimRevision 只有在以下条件全部满足时，才可以继续提供历史访问：

- 该 Revision 本身未被 Forget。
- 自身 Scope 和授权仍有效。
- Evidence 和 Provenance 依赖仍然合法。
- 不会通过共享引用、摘录、摘要或派生资产暴露已遗忘内容。

共享 Fact 对象不得导致无关的合法 ClaimRevision 被自动删除。

#### 6. 所有读取路径统一执行检查

所有读取路径 MUST 执行相同的当前授权和 Forget 检查，包括：

- FR-01：直接读取 Claim 和 ClaimRevision。
- FR-02：通过 Fact 和 FactRevision 读取 Claim。
- FR-03：通过 Evidence 追溯来源。
- FR-04：通过 Provenance 追溯来源链。
- FR-05：通过 F 的 Index、Cache 和 Retrieval Projection 读取。
- FR-06：读取 G 已有 ContextVersion 和历史 Snapshot。
- FR-07：历史版本查询、Replay、Retry 和 Recovery。
- Export：受授权的内容导出和共享。
- Backup：备份创建及保留副本。
- Restore：数据恢复和重建，以及恢复数据重新变得可查询或可投递之前的检查。

任何替代引用、Cache Key、旧版本、Replay Cursor、Export、Backup、Restore 流程或保留的对象 ID，都不得绕过授权和 Forget 决定。

#### 7. 物理清除与审计分离

以下三种状态必须明确区分：

1. 物理内容清除：按要求删除受治理 Payload 及可重建派生内容。
2. 审计保留：仅允许保留策略允许的、不可重建内容的元数据。
3. 历史引用不可用：旧标识符可以留在历史审计中，但解析时必须返回明确的不可用/已抑制结果。

标识符、Digest、谱系边或历史指针仍然存在，不构成内容披露授权。

Forget 抑制必须在返回内容之前执行，不能在成功读取之后才检查。

#### 8. 完成不变量

只有在所有必需依赖路径和替代读取路径均执行相同 Forget 决定后，才能认为声明范围内的 Forget 已完成。

所有必需依赖 MUST 具有已知且完成协调的处置结果。

任何必需依赖、Export 路径、Backup 副本、Restore 路径或读取路径仍未解决时，结果 MUST 保持未完成或未知状态。

MUST NOT 将其表示为成功 Forget。

#### 9. 测试覆盖契约

上述七个 FR 标识符是稳定测试标识符。

每项 FR 测试 MUST 标明目标、Fixture、适用 Forget 决定、预期抑制结果、实际结果及失败分类。

一个 FR 标识符的测试不得被当作另一个 FR 标识符已经通过的证据。

## 9. 变更与并发契约

Domain Validation 必须确定性、无副作用。

Canonical Memory 更新采用乐观并发：
- 调用方提供期望的当前版本；
- 成功更新恰好产生一个后继 MemoryVersion；
- 过期写入返回 Conflict；
- 并发提案不得静默覆盖。

MemoryVersion 提交后不可变。可变呈现属于 Context 或派生表示。

Canonical Commit 与所需 Provenance 可见性必须处于同一原子边界，或者由持久化/一致性层负责的可恢复 publication/outbox 机制保护。

## 10. Phase 1 验收标准

在不使用 Embedding 或 Graph DB 的情况下，必须证明：

1. Event、Memory、Claim、Entity、Relation、Evidence、Scope 可以独立创建/校验；
2. 一个 Event 可以产生多个 Candidate Memory；
3. 一个 Memory 可以包含多个 Claim；
4. Memory 身份跨不可变版本稳定；
5. Claim 跨 Memory Version 的身份策略继续保持 OPEN，不在 Phase 1 冻结；
6. 冲突 Claim 及其 Evidence 被保留；
7. 删除 ContextEntry 不会修改 Canonical Memory；
8. 无授权时跨 Scope 读写被拒绝；
9. 没有 Outcome Evidence 时拒绝把 Plan/Intent 提升为完成结果；
10. 校验错误和 Stale Write Conflict 是确定性的。

## 11. 本规范明确不决定的事项

以下事项不属于 Phase 1 语义冻结：
- 独立不可变 Fact 对象；
- 物理存储 Schema 与 SQL 布局；
- 精确序列化/Wire 格式；
- Embedding/Vector/Graph Index；
- Ranking 与 Retrieval 算法；
- Relation 扇出性能上限；
- Forget 的物理擦除机制；
- 模型辅助提取行为。

不得为了简化实现而把这些事项偷偷引入规范领域模型。

## 12. 决策闭合

| 决策 | 状态 |
|---|---|
| Event / Memory / Claim 相互独立 | DECIDED |
| Claim 是规范命题；Phase 1 不设独立 Fact | DECIDED |
| Memory 身份跨版本稳定 | DECIDED |
| Claim 跨 Memory Version 的身份策略 | OPEN |
| MemoryVersion 不可变 | DECIDED |
| Event / Recorded / Valid Time 分离 | DECIDED |
| 未知时间显式表示，绝不等于“始终有效” | DECIDED |
| Canonical Memory 与 Context 分离 | DECIDED |
| Scope 与 Permission 分离 | DECIDED |
| 冲突保留竞争 Claim 与 Evidence | DECIDED |
| 带自身语义的多对多关系使用显式关联对象 | DECIDED（语义规则） |
| 独立不可变 Fact 对象 | OPEN / 延后 |
| 时间不确定性的精确编码 | TO_VALIDATE |
| 物理存储表示 | OUT OF SCOPE |

本规范是 Phase 1 的领域语义唯一基准。后续 Rust 类型、数据库表或协议消息只能映射这些概念，不得重新定义其含义。
