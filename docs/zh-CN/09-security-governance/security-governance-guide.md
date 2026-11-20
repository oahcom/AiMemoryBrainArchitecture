# 安全、身份与治理架构指南

- 文档 ID：DOC-SEC-001
- 版本：1.0
- Owner：I — Security, Identity & Governance
- 源规范：I Owner 分支中的安全/身份总览、授权及 Forget/Retention 策略
- 对应英文：[Security, Identity & Governance Architecture Guide](../../en/09-security-governance/security-governance-guide.md)
- 状态：CANDIDATE 全局治理契约；不是生产安全认证

## 1. 安全是端到端属性

安全不能由单个 Query Filter、Cache Key、Tombstone 或 Adapter ACK 证明。它依赖认证身份、明确 Scope、策略决策、信任边界上的重新授权、撤销传播、Forget 屏障和可核验证据。

I 拥有全局身份/授权策略、Delegation 和 Revocation、Retention、Audit Governance、备份/外部副本策略、跨系统 Forget 治理评估策略、证据接受条件和物理擦除要求。D 单独拥有规范 Forget 生命周期语义及 D 领域完成判定条件。I 的跨系统治理评估不得重定义 D 的规范状态或宣告 D 领域操作完成。D/E/F/G/H/C 仍负责各自边界的本地执行机制和证据。

## 2. 三个治理平面

| 平面 | 目的 |
|---|---|
| Identity Plane | 确定谁/什么正在执行操作，以及哪个 Producer/Service 绑定到该 Actor |
| Decision Plane | 根据 Actor、Action、Resource、归属/适用 Scope、Delegation、Policy、Consent/Retention 和当前 Epoch 评估请求 |
| Enforcement/Evidence Plane | D/E/F/G/H 在各自边界执行；I 管理跨系统撤销、保留、审计和 Forget 完成 |

任何身份、Scope、Trust Level、Epoch 或授权结果，都不能仅因为它出现在 Payload 中就被信任。

## 3. Principal、ActorRef 和 ProducerIdentity

- Principal 是经过认证的安全主体：人类、Agent、Service、Workload、Adapter 或已登记的外部接收方。
- ActorRef 标识执行某项操作的 Principal，并保留其授权/委托链。
- ProducerIdentity 将生产者实例绑定到认证 Principal、Issuer、Credential、来源类型、允许的 Event Family、安全域以及撤销/凭据 Epoch。
- Issuer 是签发或证明 Credential/Delegation 的可信权威。
- Delegation 是 Delegate 代表 Grantor 行使的、有范围和期限的授权。
- ScopeRef 是领域命名空间/归属或适用范围引用，不等于 Permission。
- Permission 是策略下针对某个 Resource 的指定 Action 的允许/拒绝。
- PermissionEpoch 用于使过期授权决策和 Lease 失效。
- ForgetFence 是 D 的规范抑制代次，不等于 PermissionEpoch。

准确的类型引用语义和 Wire 字段仍需 B/I/H 联合批准。调用方自行构造的 ActorRef 不能证明身份认证；H 必须绑定认证 Transport Principal，I 定义信任策略。

## 4. Scope 和授权

请求必须根据 Action/Resource 类型，携带已解析的类型化 Scope Binding，例如 tenant、user、project、Agent、Agent instance、task、session 和 environment。

必需维度缺失时应拒绝或判为不确定，绝不能当作通配符。展示名称、模型名称、用户提供的 ID 和自由格式 Payload 声明都不是身份凭据。未明确授予的操作默认拒绝。

Permission 必须在事件接收、Canonical Read、Evidence/来源解引用、修改、生命周期转换、激活/Context 投递、导出/共享、Forget、审计以及异步 Worker 实际执行时检查。排队时曾经获得授权，不代表未来执行时授权仍然有效。

## 5. Forget 是跨系统流程

Forget 不是删除一行记录。治理模型将其分为三个阶段：

1. 即时逻辑抑制：通过持久化 Fence 阻止新的访问、派生、候选输出、Context 应用和恢复导致的内容复现。
2. 异步派生物清理：根据归属和能力，删除或使已登记的派生物、索引、缓存、Working Set、摘要、Embedding、导出和下游副本不可访问。
3. 物理擦除：根据批准的 Retention/Backup 计划和证据标准，从受控主存储和备份介质中不可恢复地移除内容及可恢复副本。

Suppressed 不等于 Cleaned。Cleaned 不一定意味着所有备份均已过期。外部 ACK 也不能证明供应商隐藏副本已擦除，除非存在覆盖该范围的可审计保证。

## 6. Forget 职责划分

| Owner | 职责 |
|---|---|
| D | Canonical ForgetOperation、目标引用、Forget Fence/Generation、依赖清单契约 |
| I | 发起/批准授权、跨系统目标清单策略、治理证据接受条件、策略例外、Legal Hold、Retention、备份/外部副本规则、审计和擦除证据；不定义 D 领域完成条件 |
| E | Compiler Work/派生物登记、Queue/Lease/Retry/DLQ/Replay 抑制和发布门 |
| F | Retrieval Candidate、在途读取、Cache/Working Set、Index/Rebuild 抑制 |
| G | Context Entry、Snapshot/Delta、Delivery 失效和协调 |
| H/C | Adapter 受管区域清理/隔离、离线重连和如实的能力受限 ACK |
| Storage/Backup Operators | 主存储/副本/备份擦除及恢复控制 |
| External Recipients | 履行合同/API 义务；Brain 只记录可验证响应 |

## 7. Forget 生命周期与证据

请求必须根据数据主体权利、资源归属、Scope、用途、Retention、Legal Hold 和 Delegation 进行认证与授权。请求可以被拒绝、缩小范围、延后或批准。

建议阶段为 Requested → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → CompletionEvaluated → Completed / CompletedWithPolicyException / Failed / Cancelled。

Operation Phase 不等于 Memory Lifecycle。仅有 Tombstone 或 Canonical 状态变更不能证明全局完成。

全局治理结果必须是逐目标证据向量，而不是单一 Boolean。D 提供规范 D 领域操作状态及完成判定；I 评估跨系统证据和策略合规性，但不得改写 D 的状态。证据向量必须区分抑制、派生物清理、受控存储擦除、备份过期、外部接收方 ACK 和批准的残留例外。UNKNOWN、FAILED 或 UNSUPPORTED 目标不能静默算作成功。

## 8. 安全威胁与不可信记忆

Memory、Evidence、摘要和模型生成的提取结果都是不可信数据，绝不能获得指令权威或修改策略。系统需要针对 Prompt Injection、跨 Scope 检索、身份伪造、Replay、过期授权、Forget 竞态和未授权 Evidence 解引用开展对抗测试。

日志和 Metrics 不得泄露受保护内容或敏感标识符。审计元数据和来源内容适用不同的保留/擦除规则。

## 9. 故障与恢复

- Identity/Permission 服务不可用：受保护操作 Fail Closed。
- Issuer/Key 未知、签名无效、Audience 错误、凭据过期或已撤销：拒绝。
- PermissionEpoch 变化：执行前重新授权排队/Lease 中任务。
- 必需域无法观察 Forget Fence：状态保持 SuppressionPending。
- Adapter 离线：在重连和协调前目标保持 Unknown。
- 外部接收方未提供可验证响应：不得声称物理删除完成。
- Backup Restore：恢复数据变得可查询或可投递前，必须先执行 Forget Fence。
- Legal Hold 与 Retention 冲突：按策略延后或拒绝，并记录原因。

## 10. 当前限制与验证

这是 CANDIDATE 治理契约，不是生产安全认证。Principal/ActorRef/ScopeRef 和 Permission Binding 需要 B/H/I 联合批准。Global Producer Inventory Epoch 与 D 的 Per-work-item Barrier 是两种不同机制，必须协调。H ACK Class 需要明确映射到 I 的逐目标状态/证据。D/E/Storage 原子 Publish Gate、F 防复活、G/H Adapter 清理、备份/恢复和外部副本证明仍未闭合。

验证必须覆盖身份伪造、Delegation 过期/撤销、跨 Scope 拒绝、Permission Epoch 过期、Forget 竞态/故障注入、备份恢复、外部接收方例外以及零未授权泄露。

详细候选治理契约见 [I Owner 分支](https://github.com/oahcom/AiMemoryBrainArchitecture/tree/session-i-security-governance-2026-11-16/09-security-governance)。


## 11. Forget 联合契约提案——待 D/I 批准

双语联合契约提案记录于 `14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v1.md`。相关的 [Owner D/I Forget 权责矩阵](../../../14-ai-development/work-items/AID-2026-001/owner-d-i-forget-authority-matrix.md) 同样是提案；在 D 与 I 对同一版本/SHA 明确批准前，两份文件都不具有规范效力。

D 拥有规范 Memory 生命周期、ForgetOperation/Fence 语义及 D 领域完成判定条件。I 拥有认证/授权、隐私/Retention/Legal Hold 策略、跨系统目标清单策略、证据接受标准和跨系统治理评估。I 不得改写 D 的规范状态或判定条件；D 不得豁免 I 的策略或声明跨系统治理合规。每个执行方只报告其能力范围内的动作和证据。

跨系统治理评估独立于 D 领域完成。只有 D 已独立记录 `Completed` 且 I 已记录 `CompliantWithException` 时，才可派生公开展示 `CompletedWithPolicyException`。未知、失败、不支持或未纳入清单的强制目标都会阻止 I 评估为 `Compliant`。Tombstone 或 ACK 均不能证明物理擦除。

**状态：** PROPOSED / 待 D-I 批准 / R3 测试未执行。

## 12. Attestor 授权契约

### 12.1 权限边界

I 是唯一负责判断 Attestor 是否有权执行指定 Attestation 操作的治理授权权威。

D MUST NOT 自行判断 Attestor 是否具有治理授权资格。

D 验证并持久化 I 提供的授权决定引用。D 不签发、不扩大、不重新解释 I 的授权。

### 12.2 Fact 与 FactRevision 绑定

每个 FactRevision MUST 绑定：

- 精确 FactRef 和 FactRevisionRef。
- 被 Attest 的精确 ClaimRevisionRef。
- 精确 EvidenceRef。
- 精确 ProvenanceRef。
- ScopeRef 及适用的可见性约束。
- 有效时间区间和记录/提交时间引用。
- Attestor Principal 身份。
- 授权决定引用。
- Attestation Method 标识和不可变 Version。
- Attestation 结果、理由及更正/撤销谱系。

FactRevision MUST NOT 自动跟随 Claim 的最新 Revision。

### 12.3 必需授权决定

每项授权决定 MUST 绑定：

1. Attestor Principal 身份：稳定且经过认证的 PrincipalRef，不得使用展示名称或自行声明的 ActorRef。
2. 授权 Scope：准确 ScopeRef 及允许的资源/动作边界。
3. Attestation Method/Version：精确注册的方法标识及不可变版本。
4. 有效期：生效时间、过期时间及适用授权 Epoch。
5. 撤销：撤销身份、生效顺序、当前性及在途 Attestation 处理。
6. Delegation：明确的 ALLOWED 或 PROHIBITED 决定。
7. 决策身份：不可变 AuthorizationDecisionRef 及对应 Policy/Version 引用。

授权决定还 MUST 保留签发权威和决策 Provenance。

Delegation 默认 NOT_ALLOWED。

每项授权决定 MUST 显式声明 ALLOWED 或 PROHIBITED。

如果 Delegation 为 ALLOWED，必须能够验证完整委托链、委托主体、被委托主体、授权主体、Scope、Method 限制、委托深度、有效期和撤销条件。

Attestor MUST NOT 从自身授权推导出 Delegation 权限。

### 12.4 Fail-closed 行为

授权缺失、歧义、过期、撤销或无法验证时 MUST fail closed。

只提供 Method 标识符而没有精确 Version 不充分。

改变 Method 或 Version 时 MUST NOT 静默扩大既有授权。

### 12.5 授权变化与历史 FactRevision

后续授权变化不得静默改写已提交的 FactRevision。

原始 Attestation 提交时的授权决定及其有效性，必须作为历史审计证据保留。

Attestor 授权被撤销或发生实质变化后，后续 Attestation 必须使用新的授权决定。

既有 FactRevision 必须根据适用撤销策略重新评估。

可以通过新的治理状态转换标记为受质疑、当前用途失效或被后继版本取代。

不得覆盖原始不可变内容。

原始授权决定与任何后续复核决定之间的关系 MUST 保持可追溯。

### 12.6 D 的验证与持久化责任

提交 FactRevision 前，D MUST：

1. 获取 I 的 AuthorizationDecisionRef。
2. 验证该引用可解析，并符合适用治理契约的真实性要求。
3. 验证 Attestor Principal 身份。
4. 验证 Scope 兼容性。
5. 验证精确 Method/Version 授权。
6. 验证相关评估时间处于授权有效期内。
7. 验证该时间点授权未被撤销。
8. 在 Delegation 明确 ALLOWED 时验证全部委托条件。
9. 将精确授权决定引用绑定至 FactRevision。
10. 在可审计提交记录中持久化决定引用和验证结果。

D MUST 保存精确 AuthorizationDecisionRef、Attestor Principal 引用、Method/Version、Scope、授权上下文、授权证据 Digest/引用、Commit Sequence 和 FactRevision 谱系。

授权证据缺失，或授权引用无法解析、验证时，D MUST 拒绝该 Attestation。

D 负责验证契约符合性和引用完整性，不替代 I 作出治理资格判断。

### 12.7 Method 正确性边界

Attestation Method 身份只能证明调用了哪个声明程序，不能证明该程序本身正确。

Confidence 是评估值，不是授权凭证，也不是创建 Fact 的机制。

Verified 是认知状态，不能代替 Attestor 授权。

本语义契约不批准生产密钥、Trust Root、密码学 Profile、公开授权 Schema、DDL 或公开 API。
