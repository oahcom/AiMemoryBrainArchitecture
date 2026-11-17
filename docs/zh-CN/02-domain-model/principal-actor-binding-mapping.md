# Principal / Actor 绑定与消费者兼容性矩阵

- **Owner：** Session B — Domain Model
- **状态：** CANDIDATE 跨模块映射；身份冻结仍为 OPEN（INT-P0-02 / INT-X-03）
- **源分支：** `session-b-domain-model-phase3`
- **精确源 Blob SHA：** `bbbef919e1e2ffe158cda8d9b2c5e718efaae969`
- **权威边界：** B 仅定义引用语义。I 负责 Principal/认证策略与信任 registry；H 负责传输绑定/Wire 格式；C 负责遥测字段语义；D/E 负责各自内部规范对象/编译操作。
- **对应文件状态：** 双语阅读对应文件；不改变源决策状态。
- **English companion:** [English](../../en/02-domain-model/principal-actor-binding-mapping.md)

## 1. Principal 到 Actor 的绑定链

`Issuer → validated credential/session → authenticated PrincipalRef → verifier-issued ActorRef → optional DelegationChainRef → operation-specific AgentRef / AdapterRef / ProducerRef + ScopeRef / EnvironmentRef → I PolicyDecision`

每一条箭头都是经过验证的绑定，不是字符串类型转换。

| 概念 | 含义 | Owner/权威 | 必须区分 |
|---|---|---|---|
| Issuer | 签发凭据/断言或签署委托的权威 | I trust registry | 未知/不可信 issuer 必须 fail closed；信任不传递 |
| Authenticated Principal | 经凭据/session 验证建立的安全主体 | I，在 H 边界验证 | PrincipalRef 不是 payload 身份声明 |
| ActorRef | 保留 Principal 及认证/委托来源的逐操作归因 | B 语义；I 断言；H 绑定 | 不是 credential、permission 或长期 bearer token |
| Delegation | 从 grantor 到 delegate 的有界签名授权链 | I 策略；B 类型化引用 | 不是身份转换；有效权限是所有约束的交集 |
| AgentRef | 逻辑 Agent 身份 | Agent registry；I 绑定 | 不是 Agent 实例、Principal 或 Adapter |
| AdapterRef | 已注册协议 Adapter/应用或实例 | H registry；I Principal 绑定 | 不是逻辑 Agent；capability/session epoch 独立 |
| ProducerRef | 获准产生声明事件/工作族的已注册来源/workload | I registry；C 断言；E ingress；D work admission | Payload producer_id 是声明，不是认证 |
| ScopeRef | 归属/适用领域 | B 语义；I/Governance registry/policy | 不是 permission 或 tenant wildcard |
| EnvironmentRef | 权威世界/存档/模拟/外部状态身份 | Environment registry；I 信任绑定 | 不是显示标签；environment version 独立 |
| PermissionDecision | 绑定 action/resource/scope/purpose/audience 的授权结果 | I | 不是 Ref，不能跨资源/scope/audience 转移 |

## 2. 绑定不变量

1. 解析 payload 身份声明前 MUST 完成认证。
2. H MUST 将 transport/session/workload 身份绑定到 I 已认证 Principal 及已注册 Adapter/Producer 身份；精确 Wire 字段仍归 H 所有。
3. C 遥测中的 `producer_id`、`agent_id`、`adapter_id`、`environment_id`（若存在）都是需要与可信绑定比较的声明，绝不是凭据。
4. E MUST 在 receipt、compile attempt、retry 和 proposal 中保留 verifier 签发的 ActorRef 及类型化 Scope/Environment 引用；MUST NOT 从模型输出或源文本创建身份。
5. D MUST 在规范对象 mutation/commit 边界校验 ActorRef 绑定和 Scope 兼容性；规范权威不意味着认证权威。
6. I MUST 在受保护边界重新评估当前 policy、delegation、revocation 和 PermissionEpoch。历史 ActorRef 不能证明当前权限。
7. 即使绑定到同一 Principal，Adapter 和 Producer 身份仍须独立注册、独立撤销。
8. Agent 只有通过显式、有界 delegation/assignment 才可代表 Principal 行动；Agent 标签相同不是证据。
9. EnvironmentRef 和 ScopeRef 必须来自权威 registry 或已认证 Adapter，不得从自由文本推断。
10. 任一必需绑定缺失、歧义、陈旧或不一致时，必须 fail closed。不得静默降级为通用字符串或匿名 actor。

## 3. 消费者兼容性矩阵

| 消费者 | 字段/逻辑输入 | 类型 | Issuer/权威 | 信任来源 | 校验边界 | 状态/未决项 |
|---|---|---|---|---|---|---|
| C Telemetry | `producer_id` | ProducerRef assertion | I Producer registry；C 定义字段 | 已认证 H session/workload + I registry | C ingress adapter/H binding；E 在 acceptance 时复查 | C 精确字段 schema/path 尚未独立取回；确认 requiredness 及 producer_id 是否 1:1 映射 ProducerRef |
| C Telemetry | `agent_id` | AgentRef assertion | Agent registry + I Principal binding | 已认证 workload/session 和已注册 Agent assignment | telemetry 接收前由 H/I 绑定；C 校验语义一致性 | OPEN：区分逻辑 Agent 与 Agent instance |
| C Telemetry | `adapter_id` | AdapterRef assertion | H Adapter registry + I Principal binding | 已认证 Adapter session/capability registry | H transport boundary | OPEN：C 字段可能缺省；绝不能当作 AgentRef |
| C Telemetry | `environment_id` / environment context | EnvironmentRef assertion + Environment ScopeRef | Environment registry / I trust binding | 已认证 Environment Adapter 或权威 registry 解析 | H/I 解析；E 校验 Event/Evidence Scope | OPEN：C 精确字段名及可信来源 |
| D Canonical Memory | `author_ref`、`ActorRef` | ActorRef | B 语义；I Principal/issuer；H authenticated binding | verifier 签发 auth context + delegation chain | D canonical write/commit boundary | D 核心模型使用 author_kind + author_ref；确保 author_kind 不替代类型化 ActorRef |
| D Canonical Memory | `scope_refs[]`、`environment_scope_id` | ScopeRef[]、EnvironmentRef/Environment ScopeRef | B 语义；I/Governance registry | 已解析 registry refs，不是调用方字符串 | D canonical validation 和 read/write boundary | D 必须保留类型和命名空间；环境绑定资产必须显式绑定 |
| D Forget admission | `requester_actor_ref`、`target_scope_refs` | ActorRef、ScopeRef[] | D operation schema + I policy | 已认证请求绑定和 I authorization receipt | D Forget request admission；I 控制权限和全局完成 | 不得从 ActorRef 推断全局权限 |
| E Compiler | `collector_ref`、`source_id`、`source_type` | 按字段语义为 ActorRef 或 ProducerRef；source_id 是类型化来源身份，不是认证 | B 语义；I Producer registry；H binding | 已认证 ProducerIdentity/ActorRef；source registry | E durable ingress/receipt 及每次 retry/replay | OPEN：保留 source origin 与 executing collector 的区别；不得混用 |
| E Compiler | `scope_refs[]`、`environment_scope_id` | ScopeRef[]、EnvironmentRef | B 语义；I/Governance registry | 可信 ingress metadata 和权威环境绑定 | E acceptance、compile、dereference、publication | 必须经 ExtractionIR 和 candidate proposal 保留，不得由模型生成内容替代 |
| E Compiler | `producer_ref`、`work_id`、`producer_class` | ProducerRef + 独立稳定 work identity | I producer registration；D per-work barrier | 已认证 ProducerRef + D durable registration receipt | E work admission/lease/retry 和最终 publication gate | I ProducerDomain inventory 与 D WorkItem registration/cursor 必须分开；两个 epoch 不同 |
| H BMCP | `source`、`recipient` | 按角色区分的 ProducerRef / AdapterRef / PrincipalRef assertion | I trust registry；H wire registry | 已认证 transport/session + H adapter registry | H envelope decode/authenticate/bind | 现有 H 将 source 称为逻辑 producer assertion，而非认证 |
| H BMCP | `scope_ref` | ScopeRef | B 语义类型；I/Governance 权威 registry | 已认证请求绑定和已解析 Scope registry | H decode/bind 后由 I 授权；消费者重新校验 | opaque owner-defined ref；Wire encoding OPEN |
| H BMCP | `permission_epoch` | PermissionEpoch（不是 Ref） | I | I 签发的 policy decision | H 原样传递；每个消费者检查当前性 | 不得转换为 ScopeRef、ActorRef 或通用 cursor |
| H BMCP | `forget_fence` | D ForgetFenceCursor/Generation（不是 Ref） | D | D canonical fence receipt；I policy binding | H 原样传递；D/I/消费者执行各自语义 | 不得与 PermissionEpoch 或 capability epoch 做数值比较 |
| I Governance | `authenticated_principal_ref` | PrincipalRef | I Principal registry、trusted Issuer | credential/session verification | H authentication boundary；I 解析并授权 | 在 B/H/Governance 联合批准前保持 Candidate |
| I Governance | `actor_ref` | ActorRef | B 语义类型；I auth assertion | H verifier-issued binding；issuer 和 auth context refs | I authorization decision 和最终操作边界 | 单独的 payload ActorRef 必须拒绝 |
| I Governance | `producer_identity_ref` | ProducerRef / I ProducerIdentity binding | I producer registry | 已认证 workload/session 和已注册 producer | I ingress/authorization；E acceptance | 与 D producer work registration 分离 |
| I Governance | `delegation_chain_ref`、`acting_for_ref` | DelegationChainRef、PrincipalRef | I delegation registry | 签名 grant chain + issuer trust + revocation state | I 在授权及最终 commit/disclosure 前校验 | Delegation 不转移所有权 |
| I Governance | `ownership_scope_ref`、`applicability_scope_refs[]`、`environment_scope_ref` | ScopeRef[] + EnvironmentRef | B 语义；I/Governance 和 Environment registry | 已认证绑定 + 权威 registry | I 解析 Scope/Environment | Scope 解析不是授权 |
| I Governance | `PolicyDecision.subject_ref`、`actor_ref` | PrincipalRef、ActorRef | I | 当前 policy engine 和已认证绑定 | I policy decision；消费者重新检查 epoch | Decision 绑定 action/resource/scope/audience/purpose |

## 4. Producer 与 Agent 身份区分

- **AgentRef** 回答涉及哪个逻辑 Agent。
- **PrincipalRef** 回答哪个安全主体完成了认证。
- **ActorRef** 回答本次操作归因于哪个已认证主体。
- **AdapterRef** 回答哪个已注册 Adapter 实例/应用负责传输或应用操作。
- **ProducerRef** 回答哪个已注册来源/workload 获准产生声明的事件/工作族。
- **EnvironmentRef** 回答观察/操作属于哪个权威外部状态域。
- **ScopeRef** 回答资源位于或受哪个归属/适用边界限定。

一次操作可以绑定上述全部身份，但它们仍是不同类型字段。一个 Principal 可以通过显式 registry 关系绑定 Agent、Adapter 和 Producer；这不意味着这些引用可以互换。

## 5. ADR 与审批门禁

- 在 B 类型化引用语义、I 安全断言、H 已认证传输绑定和 C telemetry mapping 完成协调前，INT-P0-02 / INT-X-03 保持 **OPEN**。
- H Wire 字段名和编码仍是 H 所有的候选项；本文不冻结它们。
- I 负责认证、授权、委托、撤销和 policy epoch。
- C 负责 telemetry schema 和 producer/event 语义。
- D 负责规范对象身份和 commit；E 负责 ingress/compile/producer-side enforcement。
- Architecture Governance 必须记录联合批准及证据，之后才能冻结公共 identity schema。

## 6. Phase 3.6 Principal / Actor 绑定闭环（CANDIDATE）

- **状态：** CANDIDATE 跨模块映射；INT-P0-02 / INT-X-03 仍为 OPEN。本节不批准 I policy，也不冻结 H Wire 字段。
- **基线：** B HEAD `66adf6bdcf5ec69a146fe75afe20ce3b85af8448`；此前 Blob `f20dc0cbd99b5eaf6451b5b8daf1af7c297102c6`。
- **权威：** B 定义类型语义。I 负责认证、信任、委托、授权、撤销和 PermissionEpoch。H 负责传输/session 绑定及 Wire 格式。C 负责 telemetry event 字段。D/E 负责规范对象和 compiler 边界校验。

### 6.1 Principal-to-Actor 基数与生命周期

- 一个 Principal 可以对应多个 ActorRef。ActorRef 是逐操作归因，不是第二个持久安全主体；不同操作、已认证 session、delegation context 或归因来源会产生不同的不可变 ActorRef。
- 一个 Principal 只有通过独立注册、已认证的绑定，才可关联多个逻辑 Agent、Adapter 或 Producer。这些引用仍是不同类型，且可有独立生命周期/撤销。
- 单个 ActorRef 标识一次操作的归因上下文。它 MUST 绑定已解析 PrincipalRef 和 IssuerRef，以及 verifier 所有的 AuthenticationContextRef；只有经过验证且与操作相关时，才包含可选 AgentRef、AdapterRef、ProducerRef 和 delegation refs。
- ActorRef 的历史生命周期不可变：不得重写或重新分配。但新操作能否使用它不是永久授权：I 必须重新检查 Principal、issuer、credential/session、delegation、revocation 和当前 authorization。
- 撤销 Principal、issuer、credential、Agent、Adapter、Producer 或 delegation 后，按 I policy 阻止新的受保护使用；但不改写历史归因。进行中的操作是否中止，取决于 I 批准的 revocation/linearization policy 及 D/E/H/C 边界；此项仍为 **CANDIDATE / I GOVERNANCE-BLOCKED**，不是由 B 决定。

### 6.2 Delegation 与 acting-for 语义

- Delegation 不是 PrincipalRef 到 ActorRef 的转换，不是所有权转移，也不是类型转换。
- 候选语义形态：经 verifier 解析的 ActorRef 可记录已认证 delegate PrincipalRef 和 `acting_for_ref` grantor/represented PrincipalRef，并关联类型化 DelegationChainRef 与 AuthenticationContextRef。
- 被委托的 actor 仍是已认证 delegate；被代表的 Principal 保持独立身份。ActorRef 记录两个角色，不得伪装成 delegate 已以 grantor 身份完成认证。
- 有效权限、合格 grantor/delegate、最大链深度、sub-delegation、audience、purpose、resource/action、Scope、expiry 和 parent revocation 都是 I 的策略决定。在 I36-GOV-02 中仍为 **GOVERNANCE-BLOCKED**；B 不授予这些权限。
- 没有当前有效且经 I 批准的 delegation/assignment 时，Agent 代表 Principal 行动应拒绝或判定为不确定。标签匹配或持有 AgentRef 不能证明 delegation。

### 6.3 Issuer 与跨 Issuer 处理

- IssuerRef 是签发权威的类型化身份，不是信任决定。
- Principal 身份以 IssuerRef 和声明的 tenant/security domain 为命名空间。不同 issuer 下相同 subject 字符串是不同身份，除非 I 批准显式 federation mapping。
- 信任不具传递性。来自未知、暂停、受损或不可信 issuer 的 credential/assertion 不能建立 Authenticated Principal。
- 跨 Issuer 身份链接、federation、密钥轮换/泄露和 trust-domain 准入仍为 **OPEN / I36-GOV-01 GOVERNANCE-BLOCKED**。B 仅要求显式 issuer-qualified 引用并拒绝基于字符串的别名。

### 6.4 撤销影响（领域语义与策略）

| 事件 | B 领域不变量 | I 策略依赖/状态 |
|---|---|---|
| Credential/key 轮换 | PrincipalRef 可保持稳定；credential/authentication context 是新的 | I 决定信任迁移；OPEN |
| Principal 或 Issuer 撤销 | 历史 ActorRef 保持不可变；不得推断新的可信绑定 | I 定义生效点及在途语义；GOVERNANCE-BLOCKED |
| Agent/Adapter/Producer 注册撤销 | 其引用仍是历史标识，但不得推断新的操作绑定 | I/H 定义注册和撤销；OPEN |
| Delegation 撤销/过期 | ActorRef 的历史 delegation provenance 保留；不能证明当前 delegated authority | I 定义链失效和 PermissionEpoch；GOVERNANCE-BLOCKED |
| Runtime session 过期/撤销 | RuntimeSessionRef 保留历史意义；不能续期或重放为当前 session | H/I 定义 session 权威和撤销；OPEN |
| Scope 关闭/撤销 | ScopeRef 仍是身份；新的访问/关联受 policy 控制 | I/Governance 决定操作和保留行为；OPEN |

### 6.5 必需校验顺序（逻辑顺序；策略仍由 I 负责）

1. 使用获批 verifier 对受保护 transport/session/workload 进行认证；取得受保护 issuer 和 credential/session 结果。
2. 通过 I trust/Principal registry 解析 IssuerRef 和 Authenticated PrincipalRef。
3. 从权威 registry 解析 AgentRef、AdapterRef、ProducerRef 和 RuntimeSessionRef，并绑定到已认证 Principal；不得信任 payload selectors。
4. 将 payload 身份声明与受保护绑定比较。任何不匹配、未知 issuer、缺少必需绑定或陈旧/已撤销 session 都必须拒绝或隔离；绝不优先相信 payload。
5. 只从 verifier 生成的操作上下文解析 ActorRef；校验其 Principal、Issuer、authentication-context 及任何 delegation chain。
6. 从权威 registry 解析 ScopeRef 和 EnvironmentRef；校验命名空间、kind、生命周期及操作兼容性。
7. 请求 I 对精确 Principal + Actor + action + resource + audience + purpose + 已解析 Scope/Environment 作当前授权；在所属最终 commit/disclosure 边界重新校验。

此顺序是候选跨模块协议顺序。精确 API 和 Wire 表示仍为 OPEN。

### 6.6 消费者字段映射——producer、wire 与 domain 绑定

Wire Field 列中的所有名称均为现有逻辑名称或候选映射。H 负责 Wire 命名/序列化；C 负责 telemetry 字段定义；本表不冻结任一方。

| 消费者 | Producer Field | Wire Field（候选/逻辑） | Domain Type | Issuer/Authority | Authentication Source | Validation Owner | Authorization Owner | OPEN Decision |
|---|---|---|---|---|---|---|---|---|
| C Telemetry | producer 声明的 producer identity | `producer_claim`、`producer_id` | ProducerRef assertion | I Producer registry | H 受保护 workload/session binding，由 I 解析 | H/I ingress；C 检查声明；E acceptance 时复查 | I | 精确必需字段、别名及 ProducerRef-to-ProducerIdentity 基数 |
| C Telemetry | 逻辑 Agent 和运行实例 | `agent_id`、`agent_instance_id` | AgentRef + 独立 instance identity | Agent/deployment registry；I Principal binding | H authenticated workload/session + assignment | H/I binding；C semantic validation | I | 精确 instance Ref 类型，以及两字段是否按 signal kind 必需 |
| C Telemetry | Adapter 应用/实例 | `adapter_id`、可选 `adapter_instance_ref` | AdapterRef + 独立 instance ref | H Adapter registry；I Adapter Principal | H authenticated Adapter channel/session | H；I 验证 Principal/revocation | I | C 字段是否存在及 canonical Adapter instance ref |
| C Telemetry | environment context | `environment_id` | EnvironmentRef assertion | Environment registry；I trust binding | 已认证 Environment Adapter 或可信 registry 解析 | H/I 解析；C 校验 signal requirement；E 检查 Scope | I | 精确可信环境来源及环境依赖 signal 的必需性 |
| C Telemetry | 操作归因 | `actor_ref` / ActorRef claim | ActorRef | B 语义类型；I auth assertions | H verifier-issued AuthenticationContextRef | H 生成；C/E/D 拒绝未验证 payload ActorRef | I | 精确受保护绑定证据及 ActorRef profile |
| C Telemetry | 归属/适用边界 | `scope_ref` / `scope_refs[]` | 带显式角色的 ScopeRef[] | B 语义；I/Governance registry | 受保护请求绑定 + 权威 registry | H/I 解析；C 检查 event 语义；E 校验 ingress | I | 单/多 Scope、角色及 C 精确字段名 |
| C Telemetry | runtime session | `session_id` | RuntimeSessionRef selector，不是 auth | H/I session authority | 受保护已认证 channel/session | H/I | I | C 序列化 opaque RuntimeSessionRef，还是仅用非权威 correlation selector |
| D Canonical Memory | author/attributor | `author_ref`、`created_by_actor_ref`、`author_actor_ref` | ActorRef | B 语义；I Principal/Issuer；H verifier | 受保护 auth context + 已验证操作绑定 | D canonical mutation/commit；I 提供 trust/policy result | I | D 字段别名合并和类型化 schema；`author_kind` 不能替代 ActorRef |
| D Canonical Memory | owner/applicability | `owner_scope_ref`、`scope_refs[]`、`applicability_scope_refs`、legacy `environment_scope_id` | 带角色的 ScopeRef[]；EnvironmentRef 独立 | B 语义；I/Governance Scope registry；Environment authority | 可信请求上下文 + registry 解析 | D canonical validation/read/write；I 校验 grant | I | 只能经 D 所有的 migration 退役无类型 `environment_scope_id`；不得隐式转换 |
| D Forget admission | requester 和 target | `requester_actor_ref`、`target_scope_refs` | ActorRef + ScopeRef[] | B 类型；I Principal/authorization | 受保护请求认证 | D admission 校验类型引用；I 决策 | I | 精确请求封套和 policy receipt 字段 |
| E Compiler ingress | event origin 与执行 collector | `producer_ref`、`producer_actor_ref`、`collector_ref`、`source_id`、`source_type` | ProducerRef；ActorRef；类型化 Source identity（不是 auth） | I Producer registry；source registry；B 类型语义 | H authenticated ProducerIdentity/session；verifier ActorRef | E durable ingress 及每次 retry/replay；I 解析 trust | I | 保留源头 ProducerRef 与 collector ActorRef；不得过载 source_id |
| E Compiler ingress | scope/environment context | `scope_refs[]`、`environment_scope_id`（legacy candidate） | ScopeRef[] + EnvironmentRef | B 语义；I/Governance + Environment registry | 可信 ingress metadata，不是模型输出 | E acceptance、compile、dereference、publication；D 重新检查 canonical commit | I | E 字段迁移为类型化 EnvironmentRef；角色/必需性 |
| E Compiler work | producer 与 work admission | `producer_ref`、`work_id`、`producer_class` | ProducerRef + 独立 WorkItem identity/class | I producer registration；D per-work barrier | 已认证 ProducerRef + D durable work-registration receipt | E admission/lease/retry/publication；D 校验 barrier | producer trust 由 I；work admission 由 D | I ProducerDomain inventory 与 D WorkItem registration/cursor 必须分离 |
| H BMCP envelope | source endpoint/producer | `source` | 按角色区分的 ProducerRef / PrincipalRef assertion | I trust registry；H endpoint registry | 受保护已认证 transport | H decode/authenticate/bind；I resolve | I | 候选 Wire role discriminator 和精确编码 |
| H BMCP envelope | recipient endpoint | `recipient` | 按角色区分的 AdapterRef / PrincipalRef assertion | H Adapter registry；I Principal registry | 已认证 channel + 已注册 recipient binding | H 和 I | I | 区分稳定 Adapter app、Adapter instance 和 Principal |
| H BMCP envelope | request scope | `scope_ref` | ScopeRef | B 语义类型；I/Governance registry | 受保护已认证请求 + registry 解析 | H bind；每个 consumer 重新校验 | I | 精确 Wire 表示和多 Scope 扩展 |
| H BMCP protected context | authenticated caller/session | 受保护的 `auth.issuer_ref`、`auth.principal_ref`、`auth.authentication_context_ref`、`runtime_session_ref` | IssuerRef + PrincipalRef + verifier context + RuntimeSessionRef | I trust/Principal；H/I session authority | 仅 transport verifier 输出；payload mirror 仍只是声明 | H 获取 protected context；I 验证 | I | Protected context API、RuntimeSessionRef issuer/expiry 和精确字段名 |
| H BMCP | policy token | `permission_epoch` | I PermissionEpoch（不是 Ref） | I | I policy authority | H 原样传输；consumer 重新校验 | I | Policy-domain/lease 契约仍为 I36-GOV-06 GOVERNANCE-BLOCKED |
| H BMCP | Forget token | `forget_fence` | D ForgetFenceRef/Generation（不是 Ref） | D | D canonical fence receipt | H 原样传输；consumer 校验 | 授权归 I；fence 归 D | 精确 Wire mapping；绝不与 PermissionEpoch 比较 |
| I Governance | authenticated subject | `authenticated_principal_ref` | PrincipalRef | I Principal registry + IssuerRef | H verifier 处验证 credential/session | I 解析 issuer/Principal 和 trust chain | I | I36-GOV-01 issuer 和 Principal policy GOVERNANCE-BLOCKED |
| I Governance | operation attribution | `actor_ref` | ActorRef | B 语义类型；I assertion policy | H verifier-issued auth context；可选 delegation proof | I 校验 binding 和 chain | I | I36-GOV-02 delegation policy GOVERNANCE-BLOCKED |
| I Governance | producer registration | `producer_identity_ref` | ProducerRef / I ProducerIdentity binding | I producer registry | 已认证 workload/session | I ingress；E acceptance；D 独立注册 work | I | ProducerRef registry 和 inventory 契约审批 |
| I Governance | delegation relationship | `delegation_chain_ref`、`acting_for_ref` | DelegationChainRef + PrincipalRef | I delegation authority | 已签名且经 issuer 验证的 grant chain | I 在授权和最终边界前校验 | I | Eligibility、depth、sub-delegation 和 revocation 仍 GOVERNANCE-BLOCKED |
| I Governance | resource boundaries | `ownership_scope_ref`、`applicability_scope_refs[]`、`environment_scope_ref` | ScopeRef[] + EnvironmentRef | B 类型语义；I/Governance 和 Environment registry | 已认证绑定 + registry | I 解析 Scope/Environment | I | 跨 Scope I36-GOV-03 和跨 Environment I36-GOV-04 GOVERNANCE-BLOCKED |

### 6.7 授权边界与不可替代性

- Authentication 回答：谁在可信 issuer 下出示了有效 credential/session。
- Reference resolution 回答：类型化引用指向哪个已注册领域身份。
- Authorization 回答：已认证 Principal 现在是否可对精确 resource、audience、purpose 和已解析 Scope/Environment 执行精确 action。
- D/E 的规范或 durable custody 不赋予认证或权限。
- H transport integrity 不建立授权或语义真实性。
- C telemetry authenticity 不会把报告提升为已验证 Fact/Claim。
- PermissionDecision 归 I 所有，绑定 action/resource/audience/purpose/scope 且不可转移。PermissionEpoch 是 I 所有的当前性 token，不是 reference，也不能与任何其他 epoch 互换。

### 6.8 OPEN 决定与证据要求

| ID | 决定 | Owner | 状态 |
|---|---|---|---|
| B36-OPEN-01 | 批准通用 IssuerRef/NamespaceRef 和 federation binding | I + B；Governance approval | OPEN / I36-GOV-01 GOVERNANCE-BLOCKED |
| B36-OPEN-02 | 批准 delegation grant 模型、actor acting-for 语义和撤销 | I；B 提供类型语义 | OPEN / I36-GOV-02 GOVERNANCE-BLOCKED |
| B36-OPEN-03 | 批准跨 Scope grant/inheritance/sharing 代数 | I + Governance；B 提供 Scope 语义 | OPEN / I36-GOV-03 GOVERNANCE-BLOCKED |
| B36-OPEN-04 | 批准跨 Environment bridge/federation policy | I + Environment owner | OPEN / I36-GOV-04 GOVERNANCE-BLOCKED |
| B36-OPEN-05 | 批准撤销生效点及在途操作行为 | I + 各边界 Owner | OPEN / I36-GOV-05 GOVERNANCE-BLOCKED |
| B36-OPEN-06 | 批准 PermissionEpoch policy-domain、传播和有界 lease 语义 | I | OPEN / I36-GOV-06 GOVERNANCE-BLOCKED |
| B36-OPEN-07 | 冻结 H Wire 名称/编码及受保护 authentication-context 暴露 | H，需 B/C/I acceptance | OPEN / CANDIDATE |
| B36-OPEN-08 | 确认 C telemetry 字段存在性/必需性和类型映射 | C，需 B/H/I | OPEN / CANDIDATE |
| B36-OPEN-09 | 确认 D/E canonical/compiler 字段别名和类型化 EnvironmentRef migration | D/E 与 B；I 校验 policy | OPEN / CANDIDATE |
| B36-OPEN-10 | 确认 runtime-session issuer、生命周期及跨实例绑定 | H/I | OPEN / CANDIDATE |

### 6.9 ADR-001 仍独立阻塞

本身份映射不决定 Fact/Claim 语义、规范对象身份或 attestation authority。

- ADR-001 状态仍为 **ADR-BLOCKED**。
- 本更新不批准任何 Fact/Claim schema、canonical ID、revision model、DDL、API 或 Wire 字段。
- E 继续输出中立的 CandidateProposition/ExtractionIR；D 不创建规范 Fact/Claim 对象。
- 任何 ClaimRef/ClaimRevisionRef 使用仍以正式 ADR 批准为前提。
- 身份/Scope 完成不能作为关闭 INT-P0-01 的证据。
