---
document_metadata:
  domain: memory-compiler
  role: design-specification
  steward: USER-PRINCIPAL-DELEGATED
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "从 Owner 源分支恢复；Owner 接受仍待定。"
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6-bih-identity-consumer-acceptance.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-bih-identity-consumer-acceptance"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-bih-identity-consumer-acceptance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# Phase 3.6 — BIH 身份信任消费者接受（DE-S Owner 侧）

- 状态：**已记录设计层接受；运行时一致性尚未验证**
- 权限边界：本记录接受命名的 DE-S 消费者边界所采用的 B/H 类型化身份与认证传输语义。它不批准 I 治理策略、不修改 I 的消费者登记册，也不声称实现或测试已完成。
- B 源文件：`02-domain-model/phase-3.6-typed-identity-trust-closure.md`，Blob `0a6b78a842e550b58533b797cdfcd2d954ed6826`，分支 `session-b-domain-model-phase3`。
- H 源文件：`08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md`，Blob `9845c97ac43d7888732afafe12e28850ec02add8`，分支 `session-h-bmcp-protocol`。
- I 源文件：`09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md`，Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`；I 补充文件 Blob `1f5d2e4aba7afa75c0696f3c8f025b0cb903e0ad`。
- 联合技术决策：BIH36-JD-01..17。I 治理批准仍为 GOVERNANCE-BLOCKED；I 自身登记册仍将此消费者列为 OPEN，直至 Owner 接受及证据经 I 流程记录。

## 1. 明确的设计接受

DE-S 消费者接受其边界适用的以下语义规则：

1. 类型化引用必须保留其判别类型、签发者/权威命名空间和安全域维度。禁止在 PrincipalRef、ActorRef、AgentRef、AdapterRef、ProducerRef、ScopeRef 或 EnvironmentRef 之间相互转换。
2. 载荷提供的身份只是一个不可信的声明/选择器。认证来自 H 的受保护验证器/传输上下文；I 负责解析签发者、Principal 和已注册工作负载绑定。调用方自行创建的 ActorRef 绝不是认证凭据。
3. ActorRef 是不可变、由验证器生成、针对单次操作的归因信息。它不是凭据、授权许可、可复用的 Principal 别名或 bearer token。
4. Scope 绑定必须显式标记角色，并通过权威登记册解析。ScopeRef 本身不授予权限。跨 Scope 访问需要显式且当前有效的授权。跨 Environment 访问默认拒绝；不得基于标签、坐标、租户或项目相似性进行回退匹配。
5. 每个受保护操作都必须绑定完整的适用授权元组：PrincipalRef、ActorRef、action、ResourceRef、purpose、audience、所有权/适用性 Scope 绑定、适用的 EnvironmentRef、DelegationChainRef、策略域和 PermissionEpoch，以及认证工作负载/会话上下文与 Owner 本地安全栅栏。
6. I 是 PermissionEpoch 的唯一逻辑权威。Epoch 是不透明值，只能在其策略域内比较。过期、有缺口、未知、不可比较或无法验证的 epoch 都会阻断操作。此基线禁止离线/过期授权租约，也禁止在没有在线当前性证明时使用缓存 ALLOW。
7. PermissionEpoch 与 D ForgetFence/ForgetFenceGeneration 属于彼此独立的命名空间，必须分别检查；二者不可相互替代。
8. 未知的安全关键字段、格式错误或重复引用、不支持的主版本、缺失的必需绑定、伪造/不匹配的身份声明以及结果不明确的情况，均必须 fail closed。不支持某项能力不等于成功，也不得静默降级。
9. 受保护的不可逆操作必须使用单次使用的 I `CommitAuthorizationReceipt`，并绑定策略域、PermissionEpoch、PrincipalRef、ActorRef、action、ResourceRef、purpose、audience、ScopeBindingSet 摘要、EnvironmentRef、DelegationChainRef、操作 ID、操作载荷摘要、Owner 边界和决策 ID。Owner 必须在最终提交门禁提交该回执，并记录回执/决策/排序器证据。
10. 撤销与 Owner 提交由 I 策略域排序器排序。`COMMIT_WON` 表示授权操作赢得了该排序，不代表 Owner 数据已经可见。`REVOCATION_WON` 会拒绝操作。`INDETERMINATE_ABORTED` 绝不算成功，必须进行 fail-closed 恢复。

## 2. 消费者字段映射与边界义务

| 必需字段/行为 | 已接受的语义 | DE-S 强制执行点 | 必需的负向行为 |
|---|---|---|---|
| PrincipalRef | 由 I 解析的已认证主体，不能由载荷自行认证 | D 规范变更准入；E 入口与发布 | 无法解析、已撤销或不匹配 => 拒绝/隔离 |
| ActorRef | 由 H/I 验证器生成的单次操作归因 | D 变更归因；E 工作与发布归因 | 调用方伪造、会话过期或不匹配 => 拒绝 |
| Producer/Adapter 身份 | 与 Principal 分别绑定的已注册工作负载/应用身份 | E 入口/工作准入；D 注册/工作准入；Storage 回执上下文 | 伪造、未注册或实例被替换 => 拒绝/隔离 |
| ScopeRef | 具有显式角色的权威类型化 Scope 身份 | D 目标/变更 Scope；E 源/工作/依赖 Scope | 缺失、歧义或隐式继承 => 拒绝 |
| EnvironmentRef | 权威 Environment 身份，而非展示标签 | 仅在操作配置文件要求时由 D/E 使用 | 登记册无法解析或跨域未经批准 => 拒绝 |
| 认证传输绑定 | 受保护的 H 验证器上下文，位于不可信载荷之外 | E 入口；D 仅通过认证内部边界接收可信操作上下文 | 载荷镜像不得覆盖验证器上下文 |
| PermissionEpoch | 当前 I 策略域 epoch | 受保护时由 E 入口检查；E 最终发布及 D 受保护变更边界必须检查 | 过期/有缺口/离线/未知 => 暂停/拒绝 |
| 撤销 | 由 I 排序器排序的撤销，在 Owner 不可逆边界重新检查 | D 规范提交；E 最终发布门禁 | 撤销胜出或状态不确定 => 中止/不产生可见性 |
| 拒绝伪造载荷身份 | 将声明与验证器及权威登记册绑定进行比较 | E 入口和 D 变更准入 | 不匹配 => 拒绝、审计、不回退 |
| 未知/不支持处理 | fail closed；不推断能力或证据 | 所有 DE-S 受保护边界 | 保持阻断/Unknown；绝不标记成功 |

## 3. 边界特定接受

### E — 生产者入口/编译器发布边界

E 接受将 BIH 语义用于认证生产者入口、工作执行和派生发布：

- 在入口处，根据受保护的 H 验证器上下文和 I 登记册解析已认证 Principal 与已注册 ProducerRef/AdapterRef；载荷中的生产者标识符仅是声明。
- 将每个已准入工作项绑定到已认证生产者/工作负载、ActorRef、必要时精确的 Scope/Environment 上下文、不可变工作身份和溯源信息。
- 在最终可见性线性化边界重新验证当前 I PermissionEpoch 和相关 D ForgetFence；上游 ALLOW 或入口时检查结果不能转移为发布能力。
- 向 E 最终发布门禁提交单次使用的 I `CommitAuthorizationReceipt`，并绑定精确操作 ID、载荷摘要和 E Owner 边界。最终门禁必须参与同一策略域内针对撤销的提交排序。
- E 不得把 `COMMIT_WON` 解释为 Storage 可见性证明。Storage 的持久化 VisibilityPointer + PublicationReceipt 事务仍然是可见性的权威。
- 将回执/决策/排序器证据与 E 工作/依赖/发布身份一同记录。响应丢失或排序器结果不确定时，必须沿用同一操作 ID/摘要恢复；E 不得通过生成新操作 ID 绕过未知结果。
- ProducerDomainInventoryEpoch / TargetInventorySeal 属于 I 所有的全局清单；E 的生产者注册和工作/依赖账本只是本地证据，不能替代全局 seal。

**E 设计处置：**接受其语义消费方式，但以 I 治理批准和实现证据为条件。**E 运行时一致性：尚未验证。**

### 4. Inventory Seal / Global Forget 依赖

E 将 I 的 `ProducerDomainInventoryEpoch` 和 `TargetInventorySeal` 视为全局清单权威，覆盖生产者类别、编译器工作器、队列、重试、DLQ、重放、暂存、派生制品、外部接收方和恢复路径。E 自身的生产者/工作注册不能证明全局成员完整性。未知生产者、迟到目标、无效 seal、epoch 变化、不支持的接收方或离线证据都会使操作保持 open/Unknown，并阻止闭世界完成声明。

### 5. 未完成的证据与门禁

- GOV-01..10 的 I 治理批准仍受阻；本接受不满足这些要求。
- 在 I 记录/认可这份确切 E Owner 工件之前，I 所有的消费者登记册仍为 OPEN。
- JF-10 跨权威恢复仍为 P0 OPEN，等待 I 对精确共享协议以及持久化查询/重放/回执消费保证作出处理。
- 本文不声称存在可执行的 E 入口/编译器/发布实现、集成测试命令、数据库事务证明或故障注入证据。
- 必需的后续验证：伪造生产者/Adapter 拒绝；签发者/Principal 不匹配；PermissionEpoch 过期/有缺口；撤销先于提交与提交先于撤销的排序；回执单次使用与摘要冲突；依赖/fence 竞态；Storage 可见性提交前后崩溃；ACK 丢失后的前向恢复；未知/不支持/离线路径不得发布。

**最终状态：**仅 E 设计层接受。不声称已获治理批准、运行时 PASS、JF-10 关闭或 Phase 3.6 Gate 通过。
