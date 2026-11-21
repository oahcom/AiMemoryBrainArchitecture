---
document_metadata:
  domain: agent-integration
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "07-agent-integration/agent-integration-architecture-completion.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "权威英文源文件的中文镜像；不代表 Owner 裁决或 Runtime 验证。"
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
    canonical_scope: "Agent Integration: MCP northbound access and BMCP memory-control boundary"
    canonical_scope_id: "agent-integration/mcp-bmcp-architecture-boundary"
    canonical_scope_keywords:
      - agent-integration
      - MCP
      - BMCP
      - server-lifecycle
      - memory-context
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "07-agent-integration/agent-integration-architecture-completion.md"
    en: "docs/en/07-agent-integration/agent-integration-architecture-completion.md"
---

# Agent Integration 架构完成说明

- 文档 ID：AI-INT-ARCH-001 | 版本：0.1.0
- Owner：C — Agent Integration；跨 Owner 批准待定
- 状态：CANDIDATE / NOT FROZEN / NOT IMPLEMENTATION AUTHORITY
- 英文镜像：[Agent Integration Architecture Completion](../../en/07-agent-integration/agent-integration-architecture-completion.md)
- 中文权威源：[架构仓库源文件](../../../07-agent-integration/agent-integration-architecture-completion.md)

## 1. 目的与状态

本文完成 Agent、MCP、BMCP 之间的架构阶段接入说明，提出职责边界、调用链、依赖契约、生命周期、路由、安全和未来 Runtime 验收计划。本文不定义或修改 H 所有的 BMCP Wire 字段、Transport Envelope、ACK 家族或 Validator，也不授权 Runtime 实施。

状态词汇：DECIDED BASELINE 表示已有源文件或明确 Owner 指令支持；CANDIDATE 表示等待有权 Owner 裁决；DEPENDENCY_NOT_FROZEN 表示上游契约缺失、不完整或未获 Owner 接受；NOT RUN / NOT VERIFIED 表示没有可执行证据；PENDING_OWNER_DECISION 表示尚无有权 Owner 裁决证据。

Issue #7 保留控制性实现状态 IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE。其最新关闭评论说明该 Issue 因被取代而关闭，并非完成；本文不会把 Deferred/未授权状态转换为实施批准。

## 2. 总体架构与权威边界

### 2.1 逻辑拓扑

    外部 Agent
      -> Agent Host / MCP Client
      -> MCP Transport（由 Host 按 MCP 标准选择）
      -> Agent Integration Server（北向 MCP 入口）
         -> MCP Method / Tool / Resource 分发
         -> 身份上下文传递（遵循 I 授权语义）
         -> 校验、限额、追踪、错误映射
         -> BMCP Integration Boundary（内部类型化适配器边界）
            -> BMCP Transport + Wire Adapter（H 所有；尚未冻结）
            -> Memory Service 接口
               -> 已授权 Memory Retrieval（F/Runtime 服务）
               -> Memory Domain/Store 操作（D / Storage）
               -> Memory Context 规划（G）
                  -> D Publication/Dependency Gate + I Authorization
                  -> H Delivery/ACK Evidence 路径

该图表示逻辑依赖关系，不代表每个组件当前都已成为可调用服务。仓库已有 Memory Context 规划 Crate，但没有完整 Agent Integration Server、可调用的端到端 Memory Retrieval 服务，也没有冻结的 BMCP Runtime Transport。

### 2.2 MCP 与 BMCP 是不同层次

| 关注点 | MCP | BMCP |
|---|---|---|
| 关系 | Agent Host/Client 到 Tool/Resource Server | Agent Adapter/Runtime 到 Memory Brain |
| 目的 | 标准化工具和资源交互 | Brain 记忆控制语义：Telemetry、Recall/Context 交换、Delivery/Applied Evidence |
| 负责内容 | MCP Server 生命周期、方法、Tool/Resource 暴露、MCP 请求/响应与协议错误 | 记忆控制消息语义和版本化 BMCP 契约 |
| Transport | 按采用的 MCP 规范选择并实现 | H 所有的 BMCP Transport Binding；尚未冻结 |
| 权威性 | 本身不授予 Brain 数据访问权 | 不替代 I 授权、D 生命周期/Forget 或 G Context 权威 |
| 状态 | 建议的北向接入；Runtime 未实现 | 完整 Wire/Transport/ACK/Validator 映射为 DEPENDENCY_NOT_FROZEN |

**MCP Server 是接入层，不能替代 BMCP。** MCP Tool Call 可以映射为内部类型化操作，但它本身不是 BMCP 消息。MCP 成功不代表 BMCP 接受、交付、ACK 或 Applied。

只允许暴露后端契约和授权均已具备的操作。BMCP 映射冻结前，任何声称 BMCP Delivery 或 Applied 的操作都必须不可用，或明确返回依赖未就绪结果。不得发明占位 BMCP 消息格式。

### 2.3 权责归属

- Agent / Host：推理、规划、任务拆解、行动选择、工具调用、原生会话状态和 Agent 安全策略。
- Agent Integration（C）：Agent 兼容性、MCP 分发映射、请求关联、校验和响应映射；不拥有 H Wire 契约。
- MCP Server Runtime：Listener/进程生命周期和 MCP 协议处理；不拥有 Canonical Memory 语义。
- BMCP Protocol / Adapter（H）：Wire Schema、Transport Envelope、ACK 语义、Validator 和协议符合性。
- Memory Context（G）：期望 Context 成员、确定性排序/预算、Context 版本和私有 Delivery Intent。
- Memory Domain/Lifecycle（B/D/E/F/Storage）：各自权威范围内的规范身份、生命周期、检索/激活、生产和持久化。
- 身份与授权（I）：主体、策略决策、PermissionEpoch、信任和撤销语义。
- Forget/Lifecycle（D）：ForgetFence、Lineage 和生命周期 Gate。
- 系统集成（A）：跨模块集成和部署决策；不得代替其他 Owner 合成批准。

## 3. Agent 到 Memory 的调用链

逻辑调用链为 Agent Client -> MCP Client/Transport -> Agent Integration -> BMCP Integration Boundary -> Memory Services -> Memory Context / Memory Retrieval -> Response Mapping。跨 BMCP 的字段级映射在 H 发布并接受相关版本化契约前均为 DEPENDENCY_NOT_FROZEN。

| 节点 | Owner 与输入/输出 | 协议与数据所有权 | 安全边界 | 失败、重试和超时 |
|---|---|---|---|---|
| Agent Client | Agent/Host；任务意图 -> MCP Request | MCP Client Message；Agent 拥有任务/会话状态 | Host 验证 Server 身份并执行 Tool Consent；Agent 自报身份不是授权 | 可能越过副作用边界时 Timeout 表示未知；仅在后端支持幂等时用同一操作身份重试 |
| MCP Client/Transport | MCP Host/Runtime Transport；请求帧 -> MCP Envelope | 仅 MCP Transport，不是 BMCP Wire | Transport Identity 是 I 授权输入，不能替代 I | 分发前连接失败可重试；分发后重试前先对账；Timeout 不等于 Rollback |
| Agent Integration Server | C 边界/未来 Runtime；MCP Envelope -> 类型化命令 -> MCP Result/Error | MCP Method/Tool/Resource 和内部命令；拥有请求关联，不拥有 Memory Record | 数据访问前校验 Method、Schema、Size、Deadline、Caller Identity 和 Tool Allowlist | 限制并发；逐请求 Deadline；传播取消；隔离异常；不自动重试非幂等写入 |
| BMCP Integration Boundary | C 消费者适配器；H 协议权威；类型化命令 -> H 定义 BMCP 操作 -> 类型化结果 | 内部边界为候选；Wire/Version/ACK/Transport 归 H | 绑定已认证主体/Scope 和授权证据；拒绝不支持版本/能力；不推断字段/别名 | DEPENDENCY_NOT_FROZEN：H 契约固定前不得发送/重试；之后只用 H 定义的幂等/重放/对账语义 |
| Memory Services | 按操作归属 D/F/E/Storage；已授权请求 -> Domain Result 或 Durable Receipt | Owner 定义接口；通用 MCP/BMCP Payload 不会自行变成 Canonical | 受保护读写前执行 I 授权；可见性/修改前执行 D Lifecycle/Forget 检查 | Commit/ACK 未知时查询相同 Operation/Receipt；不得盲目第二次写入；保留 Owner/操作身份 |
| Memory Context / Retrieval | G 负责 Context 规划；F/Runtime 负责 Retrieval；Candidate + Identity/Budget -> 暂存 Snapshot，或 Scoped Query -> 合格 Memory | 当前 G Crate 构建确定性 Snapshot 和私有不可发送 Intent；不是 Retrieval Service | 校验 Scope、Lifecycle、Lineage、Evidence、Budget；Builder 本身不认证/授权，也不查询 D/I | Scope/Lifecycle/Lineage/Budget 无效则 Fail Closed；Context/Forget/Permission 过期时由 Owner 对账 |
| Response Mapping | C 边界/未来 Runtime；类型化结果 -> MCP Result/Error | MCP Response Envelope；保留后端状态/Evidence，不发明 BMCP 字段 | 脱敏 Secret 和不可访问引用；不泄露跨 Scope 资源存在性 | 区分非法 MCP、授权拒绝、依赖不可用、Domain 拒绝、未知 Timeout 和内部失败 |

### 3.1 重试与超时不变量

1. Timeout 不证明失败；Cancellation Request 不证明 Rollback。
2. ACK 缺失不证明远端操作未 Commit。
3. 可重试变更复用 Owner 定义的同一 Operation/Idempotency Identity，并在创建另一逻辑操作前对账。
4. 不得仅凭 MCP Request ID、HTTP Status、Transport Connection 或 Trace ID 声称 Exactly-Once。
5. Trace ID、MCP Request ID、BMCP Operation Identity、Provider Attempt Identity 和 Domain Record Identity 必须区分。
6. Runtime 建立绝对 Deadline 或剩余时间预算；下游可以缩短，不得延长。具体时长由部署/SLO 决定。
7. Cancellation 传播到可取消工作。不可取消或已 Commit 的工作必须对账并报告 Unknown/In-Progress，不能虚报 Rollback。

## 4. BMCP 接入依赖契约

### 4.1 H 所有的边界

H 拥有权威 BMCP Wire 和 Transport 契约：版本化 Message Schema/Family；Transport Envelope、连接/会话和 Reconnect；ACK 家族及 Receipt/Acceptance/Delivery/Applied 的精确定义；Validator 行为和负向向量；Replay、Duplicate、Ordering 和协议 Error 语义。

Agent Integration 可以定义消费者需求和内部类型化接口，但不得增加/重命名 H 字段、发明 URI 语义、等同相似字段，或把候选 Schema 当作冻结契约。

### 4.2 当前依赖状态

| 依赖 | 当前 main / GitHub 证据 | 裁定 |
|---|---|---|
| Agent Integration 逻辑边界 | C Overview、Capability Tiers、Inference Boundary 和 Telemetry 模型已存在 | 基线存在；本文补充候选 MCP 接入架构 |
| Applied Delivery Evidence | main 有 H Applied Delivery Evidence 1.0.0 Schema、Validator 和符合性测试；H 3.8.25/3.8.26 补充说明候选加固 | 仅为候选证据家族，不证明完整 BMCP 映射或生产信任 |
| 完整 Message Family 映射 | Issue #3 历史记录八家族 Causal-Order Wire 映射缺口；该 Issue 被关闭为 superseded，不是技术验收 | DEPENDENCY_NOT_FROZEN；刷新控制性后继工件并取得 H 决议 |
| H Transport Binding | 当前 main 源文件未发现已接受的完整 Agent Integration Transport Binding | DEPENDENCY_NOT_FROZEN |
| ACK/Replay/Reconnect | 有候选 Applied Evidence；H 补充文件仍将生产持久 Replay、真实 Adapter 集成和跨 Owner 接受列为开放事项 | DEPENDENCY_NOT_FROZEN |
| Validator/Trust | 有候选 Validator/Fixture；不能证明 H 生产 Trust Root、注册 Profile/Key 生命周期或持久 Replay | DEPENDENCY_NOT_FROZEN |
| MCP-to-BMCP 映射 | 当前 main 未发现获批映射规范 | 仅候选内部边界；不假设 Wire 转换规则 |

H 补充文件明确指出，真实 C Ledger/Signature 验证、生产 Trust Root、持久 Replay、Crash-Safe Reservation 和 Runtime Adapter 集成仍未完成。Issue #3 历史也指出 Applied Delivery Evidence 与 JF-10 Schema 不会自动满足独立的八家族 Causal-Order 映射。Issue #3 被关闭为 superseded，不会把这些缺口转为批准。

### 4.3 BMCP URI 与 Transport 语义

- Agent Integration 源文档没有将 bmcp:// 定义为完整 URI Scheme。Authority、Grammar、默认端口、Path 语义、Discovery、Authentication、TLS、Framing、Error Mapping 和 Client Implementation 均未定义。
- BMCP 是应用层记忆控制协议，不是 URI Scheme 或 Transport。
- 若 H 选择 HTTP，它是独立 Transport Binding/Adapter。HTTP Endpoint 本身不证明 BMCP 符合性。
- MCP Transport 独立选择。MCP Streamable HTTP Endpoint 不会自动成为 BMCP HTTP Endpoint。
- 客户端若要打开 bmcp://，需要映射到已指定 Transport 的 URI Scheme Adapter 和实际 Client Handler。目前不声称该 Adapter 已存在。
- 除非精确 curl 构建已证明支持已注册/自定义 bmcp Handler，否则普通 curl 不能声称验证 bmcp://。标准 HTTP curl 只验证 HTTP Endpoint。
- 未来测试必须使用选定 BMCP Client/Transport，针对 H 固定的 Schema/Validator，验证真实请求/ACK/Replay 语义。仅 HTTP 200 不够。

本文不冻结 Health Path、BMCP URI Response Body、Envelope 或 Transport Mapping。

## 5. 未来 Runtime Server 生命周期契约

本节是 Runtime 义务，不是实现声明。

| 阶段 | 必须行为 | 证据 |
|---|---|---|
| start | 校验配置；初始化 Handler/依赖；绑定 Listener；仅在 Bind 和必要启动检查成功后报告成功 | Bound Socket/Address、启动结果、依赖 Readiness 和日志 |
| 启动失败 | 对地址、权限、端口冲突、TLS/配置、Handler 或依赖故障提供明确类型化错误；释放部分资源 | 故障注入；无虚假 Ready |
| Request Dispatch | 接收支持的 MCP Method；建立 Request Context、Principal、Scope、Deadline、Trace；校验后调用 Service | Method Trace 和非法输入测试 |
| health | 分离进程 Liveness 与依赖/协议 Readiness；HTTP Liveness 仅证明进程/HTTP Handler 有响应 | 独立 Liveness/Readiness 测试；BMCP Readiness 需要 H 定义的协议探测 |
| 并发 | 限制 In-flight Request；隔离请求状态；实施 Principal/Resource 限额 | Load/Race 测试；无跨请求泄漏 |
| Timeout/Cancellation | 执行 Deadline；传播 Cancellation；区分取消请求与 Rollback | 确定性 Timeout/Cancellation Race Trace |
| Graceful Shutdown | 停止接收；在 Deadline 内 Drain；按明确策略取消/终止剩余工作；关闭 Listener/资源 | Drain 测试和 Listener/Port 释放检查 |
| 重复 Shutdown | 幂等，或返回稳定 Already-Closed；不得二次释放/Panic | 重复关闭测试 |
| Shutdown 后 | 拒绝新请求；暴露 Closed 状态；Listener 不再绑定 | 连接失败且 Socket 可重新绑定 |

### 5.1 Health 状态模型

未来 Runtime 必须区分 Process Liveness、MCP Readiness、Memory Dependency Readiness 和 BMCP Readiness。BMCP Readiness 需要按 H 定义的 Transport Negotiation 和 Protocol Probe，与固定版本完成交互。HTTP /health 200 可以仅表示 Process Liveness，不得被描述为 BMCP Readiness、授权成功、Memory Context Publication、ACK 或 Applied。

实际 Path 和 Response Schema 是 Runtime 决策，待仓库与部署授权后确定。不得硬编码成功响应。

## 6. 请求路由与错误契约

### 6.1 路由阶段

1. 解析 Transport Frame 和 MCP Envelope。
2. Brain 数据访问前拒绝畸形 Framing/JSON、不支持版本或非法 Method。
3. 从可信 Host/Transport Identity 解析已认证 Principal 和 Scope；不信任 Caller 自报 Principal/Tenant。
4. 使用 I 所有的策略语义授权 Tool/Resource 操作。
5. 校验 Tool Name、Resource URI、Argument Shape、Size、Deadline 和 Capability。
6. 映射为类型化内部命令；仅在 H 冻结对应 Family 后序列化 BMCP。
7. 调用所属 Memory Service，保留 D/I/G/Storage 结果身份和 Evidence。
8. 映射 MCP Result，不改变语义状态。

### 6.2 错误类别

| 失败 | 边界 | 必须行为 |
|---|---|---|
| Transport/MCP Envelope 畸形 | MCP Transport/Server | MCP/Transport 定义的 Invalid Request；不调用 Service |
| 未知 MCP Method | MCP Dispatcher | MCP 定义的 Method-Not-Found |
| 未知 Tool/Resource | MCP Dispatcher | 明确 Not-Found/Unsupported；不回退 |
| Tool Arguments 无效 | Agent Integration | 参数校验错误；无后端副作用 |
| Authentication/Authorization 拒绝 | I 边界 | 受保护访问前拒绝；脱敏 Denial |
| PermissionEpoch 变化 | I Currentness | 按 I 语义重新授权；不复用过期授权 |
| ForgetFence 冲突/Lineage 过期 | D Lifecycle | 抑制/拒绝受保护操作；不允许本地覆盖 |
| BMCP Version/Family 不支持 | H Protocol | 明确 Unsupported；不静默降级 |
| BMCP Validator 拒绝 | H Validator | 保留失败/Evidence；不得解释为成功 |
| BMCP ACK 缺失/发送后 Timeout | H Transport + Operation Ledger | 同一操作对账前保持 UNKNOWN/IN_DOUBT；不盲目重试 |
| Memory Service 不可用 | 所属 Service | Dependency Unavailable；只有语义证明安全时才可重试 |
| Internal Exception/Panic | Runtime | 隔离请求、脱敏、记录 Trace/安全错误类别；尽可能保持 Server 存活 |

非法 MCP Envelope 与合法 Tool Invocation 被 Domain Authorization 拒绝是不同类别。Domain Denial 不是非法 JSON-RPC。精确 Error Code 遵循采用的 MCP 版本和 H BMCP 定义；本文不发明 BMCP Error Code。

## 7. 安全与隔离契约

1. Agent、Agent Instance、User/Tenant/Workspace/Project、Session、Task、Environment 是不同类型化身份。Request Body 不能自报已认证身份。
2. I 拥有 PermissionDecision、PermissionEpoch、Trust 和 Revocation。Agent Integration 消费 I 权威决策/当前性，不自行签发、无限期缓存或本地重解释 Permission。
3. PermissionEpoch 变化使受保护操作的缓存授权失效。重新校验遵循 I 的 Ordering/Currentness；本地时间戳比较不能替代。
4. D 拥有 ForgetFence Token、Lineage 和 Ordering。受保护 Memory Candidate、Context Publication 和迟到结果遵守 D 当前 Fence；Agent/MCP Caller 不能通过重提请求绕过。
5. Scope 不等于 Permission。Retrieval 前解析并授权 Scope；测试跨 Tenant、跨 Agent、跨 Session 和 Confused Deputy。
6. Agent Telemetry、Memory Text、Resource Content、Tool Description 和 Annotation 都是不可信数据，不是指令。Memory 不得提升为 System/Developer 权限或授权 Tool。
7. 暴露 MCP Tool 不等于授权执行。Host Consent 和 I/Tool Host Policy 必须在真实执行边界授权 Invocation 和数据访问。
8. Principal、Scope、Deadline、Cancellation Token 和 Trace Context 是请求级状态。无明确并发安全契约时，不跨请求共享可变授权或 Memory 状态。
9. 默认不记录原始 Memory Content、Secret、Credential、Prompt Body 或私有推理。按 I 隐私/保留规则记录稳定引用和受限诊断。
10. 外部错误不得泄露 Secret、跨 Scope 资源存在性、Key Material、原始 Stack Trace 或 Trust Registry 细节。
11. Replay/Idempotency 只使用 Owner 定义的 Operation Identity 和 Replay 规则。MCP Request ID、Trace ID 不是 Idempotency Key。
12. 传播因果 Trace Link 并保持身份域区分。Authorization Reference 和 Validator Outcome 是证据，但 Trace Correlation 不是权威。

## 8. Memory Context 集成矩阵

### 8.1 PR #421 已核实结果

PR #421 已合并，不再是 Draft：

- PR：[ #421 feat(memory): implement Memory Context](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/421)
- Head Commit：0a4e84276fbcdb94f8efff33d881becc5be460a4
- Merge Commit：d381e7a1fc17bea1dd14be54e8dfd497e8ca2e83
- 本轮观察到的 main：bb49dc121c195d7fb2ffa0ffbb9d376186b802fc
- 修改文件：Cargo.toml；crates/memory-context/Cargo.toml；crates/memory-context/src/lib.rs。

合并的 Crate 提供确定性、具 Scope 约束的 Context Snapshot 规划和私有、不可发送的 DeliveryIntent。Builder 接收 ContextIdentity、ContextBudget 和已提供的 ContextCandidate。它校验 Scope Membership、Active/Consolidated Lifecycle、Lineage、重复 Entry/Membership 以及 Entry/Byte Budget，确定性排序并序列化暂存 Snapshot。

该 Crate 不认证、不授权、不查询 D/I、不执行 Memory Retrieval、不持久化权威 Context Version、不发布可见 Context Head、不发送 BMCP，也不产生 Applied ACK。DeliveryVisibility 只有 PrivatePendingPublicationGate。PR 正文说明 D Producer/Dependency/Final-Publication 和 I Authorization 接口尚未暴露。

### 8.2 依赖矩阵

| 需求 | Memory Context 当前提供 | 缺失契约 | 集成规则 |
|---|---|---|---|
| Context Identity/Scope | ContextIdentity 含 Context、Agent、Agent Instance、Session、可选 Task/Environment 和 ScopeRefs | 权威 Principal/Permission 绑定归 I | 身份字段不是认证/授权 |
| Candidate Memory | ContextCandidate 输入类型 | Crate 未暴露已授权 Candidate Retrieval API；需明确 Retrieval Owner/Service | 仅传入独立授权读取路径返回的 Candidate |
| Context Planning | build_context 提供确定性排序和 Lifecycle/Scope/Lineage/Budget 校验 | 跨 Owner Currentness 和权威持久化 | 结果仅为 Staged Snapshot |
| Delivery | 序列化 DeliveryIntent，固定 PrivatePendingPublicationGate | D Publication/Dependency/Final Gate、I Authorization、H BMCP Delivery/ACK | 不得发送或暴露为已交付 |
| Applied Result | 无 Applied Record/ACK | G Applied 权威及 H Evidence Mapping | 不得从 Snapshot、MCP 成功或 HTTP 200 推断 Applied |
| Retrieval Response | 本 Crate 无 Retrieval Endpoint | F/Runtime Retrieval Contract 和 I Authorization | Builder 不是 Memory Retrieval 实现 |

### 8.3 必需集成顺序

1. 从已授权 Retrieval Service 获取 Scoped Candidate；该 Service 应用 I Authorization 和 D Lifecycle/Forget 约束。
2. 使用 G API 构建 Staged Snapshot；保留 Context Identity、Version、Lineage 和 Budget 结果。
3. 通过权威接口取得 D Producer/Dependency Registration、Final Publication Gate 和 I Authorization。
4. 仅在 Gate 成功后依据 G/H 已接受契约准备可发送 Delivery Operation。
5. H 定义的 BMCP Transport 发送版本化 Delivery 并验证 ACK/Evidence。
6. G 使用精确 H/C Boundary Evidence 和 Currentness 规则记录权威 Context/Applied Result。
7. Agent Integration 映射回 MCP，不得把 Receipt/Acceptance 提升为 Applied。

当前 Workspace 不具备步骤 3–6 的完整可调用路径。这是架构依赖，不是现有功能声明。

## 9. 未来 Runtime 验收计划

**以下全部 NOT RUN。** 这是验收要求，不是测试结果。BMCP 用例等待 H 发布并由相关 Owner 接受精确契约版本后才能执行。

| ID | 场景 | Agent Integration 职责 | H 职责 | 联合/外部依赖 | 证据/状态 |
|---|---|---|---|---|---|
| RT-01 | Server Startup | 校验配置、绑定 Listener、注册 MCP Dispatch；Bind 前不报告成功 | N/A | Runtime 环境 | Bound Socket/Startup Trace；NOT RUN |
| RT-02 | 端口绑定失败 | 明确启动错误；释放部分资源 | N/A | OS/Network | Failure Log、无虚假 Ready；NOT RUN |
| RT-03 | Health Check | 区分 Liveness、MCP Readiness、Dependency Readiness | Transport 冻结后定义 BMCP Probe | Runtime + H | HTTP Liveness 不等于 BMCP PASS；NOT RUN |
| RT-04 | MCP Initialize/Request | 实现采用版本的 MCP 方法生命周期 | N/A | MCP Conformance Suite | 有效 Transcript；NOT RUN |
| RT-05 | BMCP Request Forwarding | 映射类型化命令，不发明字段 | 定义 Family/Schema/Transport/Validator | C/H Mapping | 精确 H Version Request；BLOCKED / DEPENDENCY_NOT_FROZEN |
| RT-06 | BMCP ACK | 保留 ACK 状态和同一 Operation 关联 | 定义 ACK Family/Semantics/Ordering/Replay | G/D/Storage 对账 | 正/负/Replay Vector；BLOCKED |
| RT-07 | BMCP Validator | 调用固定 Validator；拒绝非法 Payload | 拥有 Validator 和规范错误 | H + Consumer Review | Schema/Validator 负向向量；BLOCKED |
| RT-08 | 并发请求 | 限制并发并隔离 Request Context | 如适用，定义 Transport/Session 并发 | I Scope Isolation | Race/Load Test；NOT RUN |
| RT-09 | Timeout | 执行 Deadline；结果不确定时返回 Unknown | 定义 Transport Timeout/ACK 语义 | Operation Ledger | 同一 Operation 对账；NOT RUN |
| RT-10 | Cancellation | 传播取消；不声称 Rollback | 如有协议级取消，定义语义 | D/Storage/Provider 副作用 Owner | Cancel-vs-Complete Trace；NOT RUN |
| RT-11 | Graceful Shutdown | 停止接收、Drain/Cancel、关闭 Listener/释放端口 | N/A | Runtime | Drain 和 Port-Rebind 证明；NOT RUN |
| RT-12 | Authorization Denied | 受保护访问前拒绝并脱敏 | 仅按 H 定义承载 Identity Evidence | I Policy | Denial Decision/No-Read 证明；NOT RUN |
| RT-13 | PermissionEpoch 变化 | 使缓存授权失效并重检 | 仅按 H 定义绑定协议 Evidence | I Currentness | Stale-Epoch Rejection；NOT RUN |
| RT-14 | ForgetFence 冲突 | 停止/抑制受保护使用 | 仅按 H 定义承载 D Fence Evidence | D Fence/Lineage；G Currentness | Fence Race/Stale Suppression；NOT RUN |
| RT-15 | 非法协议请求 | 拒绝畸形 MCP Envelope；不路由 Memory | 拒绝非法 BMCP Schema/Version | MCP + H | 分离负向测试；NOT RUN |
| RT-16 | 不支持的协议版本 | 在正确层报告不支持 | 定义 BMCP Negotiation/Fallback | H + Runtime | 不静默降级；BMCP BLOCKED |
| RT-17 | 未知 Method/Tool/Resource | MCP Method-Not-Found/明确失败 | 除非映射 BMCP Operation | MCP Runtime | 协议正确的负向响应；NOT RUN |
| RT-18 | 跨 Tenant/Confused Deputy | 执行请求级 Principal/Scope 隔离 | 保留已认证 Identity Binding | I 与 Adapter Security | 对抗性隔离测试；NOT RUN |
| RT-19 | Context Publication | 不发送私有 DeliveryIntent | 定义 Delivery Envelope/ACK | G + D + I + H | 发送前 Gate Evidence；BLOCKED |
| RT-20 | Applied 真实性 | 不将 Receipt/MCP Success 映射为 Applied | 校验 H Evidence Family | C/G/H 与 I Trust | Final-Boundary/Applied Join；BLOCKED |

### 9.1 验收 Gate

- Gate A — MCP Runtime：在获授权 Runtime 仓库通过 Startup、Dispatch、Health、Concurrency、Timeout、Cancellation、Shutdown 和 MCP Conformance。
- Gate B — BMCP Contract：H 发布版本化 Schema、Transport、ACK、Validator、Error、Replay、Reconnect；记录 H Owner 决议和消费者映射。
- Gate C — Security/Lifecycle：I 批准 Identity/PermissionEpoch/Trust；D 批准 ForgetFence/Lineage；负向测试证明 Fail Closed。
- Gate D — Memory Context End-to-End：已授权 Retrieval、G Planning、D/I Publication Gate、H Delivery/ACK 和 G Applied Evidence 使用精确身份与持久对账完成关联。
- 不得因存在设计文档就把任何 Gate 标为 PASS。可复现证据产生前 Runtime/BMCP Gate 均为 NOT RUN 或 BLOCKED。

## 10. Owner 裁决请求

以下请求仅请求对应权威范围内的决策，不代表代 H、D、I、G 或 A 签署。

### DECISION_REQUEST_ID: AI-INT-DR-001

- MODULE: Agent Integration
- ISSUE_OR_ADR: 现有 Agent Integration 基线；08-bmcp-protocol 下 H/BMCP 源文件；Issue #3 历史记录已关闭为 superseded，不代表技术验收。
- DECISION_REQUIRED: H 明确并批准 Agent Integration 消费者可实施所依据的 BMCP Message Family、Transport、ACK、Validator、Replay、Reconnect 精确版本。
- CURRENT_FACTS: 当前 main 有 Applied Delivery Evidence 1.0.0 候选家族和加固补充；完整跨 Owner Wire Mapping 和生产 Trust 尚未建立。
- DEPENDENCY_ON_H: 权威依赖；H 发布精确版本/Blob Pin 和 Wire/Transport/ACK/Validator 决策。
- DEPENDENCY_ON_D: ForgetFence 和 Lineage 字段/排序归 D；H 字段不得重新定义。
- DEPENDENCY_ON_I: 已认证身份、Trust Profile 和 PermissionEpoch 归 I；H 不授予授权。
- MCP_BMCP_BOUNDARY: MCP Dispatch 映射到类型化内部操作；仅通过 H 固定契约序列化 BMCP。
- OPTIONS: A 等待完整 H 契约；B 仅实现不声称 BMCP 行为的 MCP 操作；C 发明临时 BMCP Payload。拒绝 C。
- RECOMMENDED_OPTION: BMCP 依赖操作采用 A；仅明确受限的 MCP Health/Capability Endpoint 可采用 B。
- RUNTIME_IMPLEMENTATION_IMPACT: H 冻结前不得实现 BMCP Sender、URI Handler、ACK Parser 或 Validator 集成。
- REQUIRED_AUTHORITY: H Owner；C 消费者接受；涉及各自绑定的 D/I/G Owner。
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: 当前 main H Addenda 3.8.25/3.8.26；Issue #3 历史八家族缺口记录；PR #428 仍是 Open Draft 候选。
- FOLLOW_UP_ACTIONS: H 发布精确 Pin；C 记录消费者映射；相关 Owner 接受各自绑定。

### DECISION_REQUEST_ID: AI-INT-DR-002

- MODULE: Agent Integration
- ISSUE_OR_ADR: I Authorization Contract 与 D ForgetFence/Currentness Contract；Issue #7 工程入口交接。
- DECISION_REQUIRED: I 与 D 明确 Read、Delivery、Publication 和 Late-Result 边界所消费的可调用授权/当前性接口及必需 Evidence。
- CURRENT_FACTS: Agent Integration 需要 PermissionEpoch 重新验证和 ForgetFence/Lineage 执行；当前 Memory Context Builder 不调用 I 或 D。
- DEPENDENCY_ON_H: H 只能按 H 规范承载引用/Evidence，不能定义 I/D 权威决策。
- DEPENDENCY_ON_D: D 决定 Fence Token、Lineage、Ordering 和受保护 Lifecycle Gate。
- DEPENDENCY_ON_I: I 决定 Principal、PermissionDecision、PermissionEpoch、Trust、Revocation 和 Currentness。
- MCP_BMCP_BOUNDARY: 已认证身份从 MCP Host/Transport 传递到内部命令；BMCP 仅通过 H 接受的表达方式绑定。
- OPTIONS: A 接口发布后使用 I/D 精确接口；B 接口存在前阻断受保护操作；C 本地合成 Epoch/Fence 语义。拒绝 C。
- RECOMMENDED_OPTION: A 有证据前采用 B。
- RUNTIME_IMPLEMENTATION_IMPACT: 不得仅凭 Caller 自报身份、缓存 Permission 或本地 Fence 近似值执行受保护 Retrieval/Send/Publication。
- REQUIRED_AUTHORITY: I Owner 与 D Owner 独立裁决；C/H/G 消费者分别审查自己的绑定。
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: Agent Integration Security Boundary；PR #421 合并代码/正文；D/I 权威声明。
- FOLLOW_UP_ACTIONS: I/D 发布精确接口和 Test Vector；Runtime Entry Plan 固定引用，不改变语义。

### DECISION_REQUEST_ID: AI-INT-DR-003

- MODULE: Agent Integration
- ISSUE_OR_ADR: Runtime Implementation Entry / Issue #7。
- DECISION_REQUIRED: Owner 与 Engineering Leadership 授权 Canonical Runtime Repository/Branch、Maintainer、Build/CI、Deployment Topology 和 MCP/BMCP Transport 实施位置。
- CURRENT_FACTS: Issue #7 保留 IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE，且关闭为 superseded 而非 completed。当前仓库是架构定义范围。
- DEPENDENCY_ON_H: BMCP Runtime 实施前，H 必须提供冻结的 BMCP Transport/Protocol Contract。
- DEPENDENCY_ON_D: 受保护写入/Publication 需要 D Callable Lifecycle/Forget Interface 和运维责任。
- DEPENDENCY_ON_I: 需要 I Callable Identity/Authorization Interface 和 Trust/Key 操作。
- MCP_BMCP_BOUNDARY: MCP Server 是北向 Agent Tool Interface；BMCP 是独立南向 Memory-Control Protocol。
- OPTIONS: A 指定现有 Canonical Runtime Repository；B 明确授权独立 Runtime Repository；C 在本仓库添加 Placeholder Runtime Code。拒绝 C。
- RECOMMENDED_OPTION: Engineering Authority 明确选择 A 或 B；保持本仓库架构职责边界。
- RUNTIME_IMPLEMENTATION_IMPACT: 本仓库不创建 Runtime Server、Listener、bmcp:// Handler 或生产激活。
- REQUIRED_AUTHORITY: Project Owner 与 Engineering Leadership；A 协调 Traceability。
- OWNER_DECISION: PENDING_OWNER_DECISION
- EVIDENCE: Issue #7 最新 Superseding Closeout；当前 main Inventory 和 README 范围。
- FOLLOW_UP_ACTIONS: Owner 指定 Repository/Branch 和 Engineering Owner；Engineering Lead 提供 Build/Test/Deployment 与 Artifact Provenance 计划。

## 11. 工程阶段交接清单

Runtime 入口保持 Pending，直到记录：

1. H 批准的 BMCP Message Family、Wire、Transport、ACK、Validator、Error、Replay、Reconnect 契约和精确版本/Blob Pin。
2. 明确 MCP Version/Transport 与 MCP-to-Internal-Command 映射；不混淆 MCP/BMCP。
3. I 批准的 Identity、PermissionDecision、PermissionEpoch、Trust、Revocation 和 Key Lifecycle Interface。
4. D 批准的 ForgetFence、Lineage、Ordering 和 Publication/Lifecycle Gate Interface。
5. G 批准的 Context Identity/Version/Applied 消费者绑定和 H Evidence Mapping。
6. Canonical Runtime Repository/Branch、责任 Maintainer、写入权限和明确实施授权。
7. Build System、固定依赖、CI Workflow、可复现测试命令和 Artifact/Build SHA 来源。
8. Test/Service Topology、Secret/Key Custody、Logging/Retention、Monitoring、On-call、Rollback 和 Deployment Authorization。
9. 将 Runtime Acceptance Matrix 转为可执行测试，含 Owner 专属 Fixture 和确定性 Evidence。
10. 独立跨 Owner 评审和 Owner 批准；不得将提案状态误认为生产就绪。

## 12. 来源清单与可追溯性

已核实的 current-main 源文件：

- 07-agent-integration/agent-integration-overview.md
- 07-agent-integration/adapter-capability-tiers.md
- 07-agent-integration/inference-boundary-model.md
- 07-agent-integration/telemetry-model.md
- 08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md
- 08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md
- 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json
- 08-bmcp-protocol/validators/applied_delivery_evidence_validator.py
- 08-bmcp-protocol/tests/conformance/applied_delivery_evidence/test_applied_delivery_evidence.py
- 06-memory-context/README.md
- crates/memory-context/Cargo.toml
- crates/memory-context/src/lib.rs
- 00-governance/architecture-document-management-policy.md
- 00-governance/bilingual-documentation-policy.md

相关 GitHub 记录：

- [Issue #7 — 工程入口；关闭为 superseded，但保留 Deferred 决定](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7)
- [Issue #3 — 历史 C/G/H Wire 决策；关闭为 superseded，不代表技术验收](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/3)
- [PR #421 — Memory Context，已合并](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/421)
- [PR #428 — BMCP 架构契约，Open Draft](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/428)；仅为评审候选，尚未合并，不视为 H 批准或 BMCP 契约冻结。
- [Issue #381 — Delegated Grant Adapter Isolation 后续任务，已关闭](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/381)
- [Issue #348 — REQ-08 互操作提案，已关闭](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/348)

本文为 Informative/Candidate，不取代 C 源架构、H BMCP 契约、G Context 权威、D 生命周期、I 授权或 Issue #7 状态。

## 13. 最终架构状态

- MCP/BMCP 概念边界：已形成候选定义；等待 Owner 确认。
- Agent-to-Memory 调用链和职责：已文档化；部分上游接口仍不可用。
- H BMCP 契约：DEPENDENCY_NOT_FROZEN。
- Memory Context：基础能力已合并；Publication/Delivery/Applied 链路不可用。
- Server 生命周期和路由：已提出契约；Runtime 未实现。
- 安全依赖：保留 I/D 权威；可调用集成未验证。
- Runtime 验收：仅有计划；全部测试 NOT RUN。
- Issue #7：IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE。
- 生产激活：本文不授权生产激活。
