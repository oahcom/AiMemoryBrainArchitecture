# 安全、身份与治理架构指南

- 文档 ID：DOC-SEC-001
- 版本：1.0
- Owner：I — Security, Identity & Governance
- 源规范：I Owner 分支中的安全/身份总览、授权及 Forget/Retention 策略
- 对应英文：[Security, Identity & Governance Architecture Guide](../../en/09-security-governance/security-governance-guide.md)
- 状态：CANDIDATE 全局治理契约；不是生产安全认证

## 1. 安全是端到端属性

安全不能由单个 Query Filter、Cache Key、Tombstone 或 Adapter ACK 证明。它依赖认证身份、明确 Scope、策略决策、信任边界上的重新授权、撤销传播、Forget 屏障和可核验证据。

I 拥有全局身份/授权策略、Delegation 和 Revocation、Retention、Audit Governance、备份/外部副本策略、全局 Forget 完成策略和物理擦除要求。D/E/F/G/H/C 仍负责各自边界的本地执行机制和证据。

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
- ForgetFence 是 D 的规范抑制代数，不等于 PermissionEpoch。

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
| I | 发起/批准授权、目标清单策略、完成条件、例外、Legal Hold、Retention、备份/外部副本规则、审计和擦除证据 |
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

全局结果必须是逐目标证据向量，而不是单一 Boolean。它必须区分抑制、派生物清理、受控存储擦除、备份过期、外部接收方 ACK 和批准的残留例外。UNKNOWN、FAILED 或 UNSUPPORTED 目标不能静默算作成功。

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


## 11. Forget 联合契约对齐提案——待 D/I 批准

双语联合契约提案记录于 `14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v1.md`。在 D 与 I 对同一版本/SHA 明确批准前，本节仅为提案，不取代本 CANDIDATE 治理指南。

拟由 I 决定的事项：
- 当前授权、Delegation/Revocation、数据主体及 Scope 资格、Purpose、Consent、Retention 和 Legal Hold 策略；
- 全局目标清单策略、强制目标类别、清单封存和重新评估触发条件；
- 全局完成聚合、批准的残留例外、审计完整性和真实状态对外呈现。

D 继续拥有规范 Memory 生命周期、ForgetOperation 和 ForgetFence 语义。I 不重新定义 `Forgotten` 或规范线性化事件。D 不授予授权、不豁免 Retention/Legal Hold，也不得单方面声明全局完成。E/F/G/H/C/Storage/外部接收方只提供各自能力范围内的执行证据。

Operation Phase 与 Memory Lifecycle 相互独立。持久化的 `SuppressionCommitted` 事件可以使 Memory 进入终态 `Forgotten`，而清理仍异步进行。`Completed` 要求所有强制目标均有已验证的终态证据。未知、失败、不支持或未纳入清单的强制目标均阻止 `Completed`。`CompletedWithPolicyException` 必须有 I 的明确批准、有边界的残留、补偿控制、责任人及到期/复核时间；它不是物理擦除证明。

**状态：** PROPOSED / 待 D-I 批准 / R3 测试未执行。
