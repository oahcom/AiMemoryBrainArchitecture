# Session G Review — Memory Context Manager 三方六维度独立架构审查报告

- 审查日期：2026-11-16
- Repository：`oahcom/AiMemoryBrainArchitecture`
- Branch：`main`
- 审查对象：Session G — Memory Context Manager
- 审查方式：三个专业视角的独立模拟 × 六个架构维度
- 审查类型：静态文档审查与跨模块契约审查；非代码审计、非运行测试
- 最终结论：**FAIL — Session G 核心设计文档未出现在本次审查所读取的 main 分支中，无法证明 Context Version、Change Set 原子性、Applied Proof 与 Forget/Reconciliation 契约成立。不得冻结 G 契约或据此放行实现。**
- 审查签署说明：三方是三个专业视角的独立模拟，不代表三名真实人员或三个独立模型签署。

> 本报告严格区分“文档缺失/证据不足”和“已证实的实现缺陷”。本次未执行真实 Adapter 测试、Rust 事务测试、并发压力测试、权限渗透测试、离线重连测试或 Forget 物理清理测试。不得将任何未执行测试描述为通过。

---

## 1. 审查范围和材料

### 1.1 本次实际读取的材料

| 类别 | 文件/路径 | 状态 | 用途 |
|---|---|---|---|
| 项目基线 | `README.md` | READ | 产品定位、边界、文档地图 |
| 路线图 | `ARCHITECTURE_ROADMAP.md` | READ | 子系统规格模板、阶段门禁 |
| 治理 | `00-governance/architecture-invariants.md` | READ | I-01 至 I-22 |
| 治理 | `00-governance/design-principles.md` | READ | P-01 至 P-16 |
| 治理 | `00-governance/terminology.md` | READ | Context、Entry、Applied Context、Forget 等术语 |
| 系统架构 | `01-system-architecture/system-overview.md` | READ | Brain/Runtime/Agent 边界、推理上下文边界 |
| 系统架构 | `01-system-architecture/component-map.md` | READ | MCM、Sync、Governance 等职责 |
| 系统架构 | `01-system-architecture/responsibility-matrix.md` | READ | Context 权威、Activation、Sync 主责 |
| 系统架构 | `01-system-architecture/component-interactions.md` | DIRECTORY ENTRY 已确认 | 交互关系基线 |
| 领域模型 | `02-domain-model/domain-model-overview.md` | READ | Memory/Memory Version/Context/Entry 语义 |
| 领域模型 | `02-domain-model/core-entities.md` | READ | 核心实体语义 |
| 领域模型 | `02-domain-model/scope-and-permission-model.md` | READ | Scope 与 Permission |
| 领域模型 | `02-domain-model/lifecycle-model.md` | READ | Canonical Lifecycle |
| 领域模型 | `02-domain-model/relationships-and-provenance.md` | READ | Provenance 与引用 |
| A/B/C 集成审查 | `reviews/integration/phase-1-abc-cross-document-integration-review.md` | READ | INT-P0、INT-P1、跨模块门禁 |
| D 专项审查 | `reviews/03-memory-brain/three-party-six-dimension-review.md` | READ | D 缺失材料状态及 D 相关风险 |
| F 专项审查 | `reviews/05-memory-runtime/three-party-six-dimension-review.md` | READ | F 缺失材料状态及 Runtime 风险 |
| H/Agent Integration 设计 | `07-agent-integration/agent-integration-overview.md` | READ | Adapter 与 Brain 边界 |
| H/Agent Integration 设计 | `07-agent-integration/adapter-capability-tiers.md` | READ | Adapter 能力层级、Applied 条件 |
| H/Agent Integration 设计 | `07-agent-integration/inference-boundary-model.md` | READ | Inference Boundary、Applied 证明 |
| C 专项审查 | `reviews/07-agent-integration/three-party-six-dimension-review.md` | READ | P1-06、P1-07、P2-05、P2-06 等 |

### 1.2 G 的核心设计材料：本次全部未取得

按任务书指定路径读取，以下文件均返回 GitHub 404：

| 指定文件 | 状态 |
|---|---|
| `06-memory-context/context-architecture.md` | MISSING |
| `06-memory-context/context-manager.md` | MISSING |
| `06-memory-context/context-edit-operations.md` | MISSING |
| `06-memory-context/context-versioning.md` | MISSING |
| `06-memory-context/context-reconciliation.md` | MISSING |
| `06-memory-context/context-budget-and-sufficiency.md` | MISSING |
| `06-memory-context/` 目录 | MISSING |

指定审查报告 `reviews/06-memory-context/three-party-six-dimension-review.md` 在本次检查时也不存在。当前仓库根目录可见的目录为 `00-governance/`、`01-system-architecture/`、`02-domain-model/`、`07-agent-integration/`、`reviews/`；未见 `03-memory-brain/`、`04-memory-compiler/`、`05-memory-runtime/`、`06-memory-context/`、`08-protocols/`。这与 D/F 专项审查报告所记录的缺失状态一致。

**证据边界：** 以上结论只代表本次读取到的 GitHub `main` 分支状态，不推断其他分支、未提交工作区或其他会话中的文档。任务书列出的 G 设计文档不能被视为已经提交或已经审查。

### 1.3 依赖材料状态

| 依赖 | 可见证据 | 本轮判断 |
|---|---|---|
| A 系统架构 | 系统架构文档、A 审查由集成报告引用 | 基线可读；完整专项报告未作为本轮重点展开 |
| B Domain Model | 六份领域模型文件、B 审查由集成报告引用 | 基础语义可读；部分跨模块结论依赖既有审查 |
| C Agent Integration / Adapter 边界 | 四份设计文件、C 审查报告 | 可读；C 明确将 G/H 的 Context 原子性与 Applied 证明留待定义 |
| D Memory Brain | D 专项审查报告可读，D 设计目录缺失 | Canonical Memory 实施契约未验证 |
| E Memory Compiler | 本次未发现 E 设计目录或 E 专项审查报告 | 未验证 |
| F Memory Runtime | F 专项审查报告可读，F 设计目录缺失 | Retrieval/Activation 输出契约未验证 |
| H BMCP / Adapter | Agent Integration 设计可读；`08-protocols/` 缺失 | 部分边界可读，BMCP 最终 wire contract 未验证 |
| I Security / Governance | 治理原则与 B Scope 模型可读；I 专项设计未见 | 撤权、Forget 执行、离线副本治理未验证 |

---

## 2. 总体结论

### 2.1 最终决议：FAIL

本次不能给 Session G 通过或有条件通过的设计审查结论，原因不是已证明 G 的某项实现必然错误，而是 **G 的核心设计交付物在审查基线中缺失**。任务书要求审查的六份核心文档均不可读取，导致以下关键事实无法被文档证据证明：

1. G 是否为每个 MemoryContext 持有唯一、单调、不可分叉的 Context Version 权威序列。
2. ContextChangeSet 是否绑定 Base Version、Target Version、幂等键、提交身份和原子操作集合。
3. Snapshot 是否定义完整替换语义，Delta 是否定义 all-or-nothing 应用语义。
4. 多操作 ChangeSet 在局部失败时是否回滚，是否存在部分状态可见。
5. Delivery ACK 是否能证明完整 managed region 已进入指定 Inference Request 的最终提交边界。
6. Forget/Revocation 是否能阻断旧 Context、Pending Delivery、离线 Adapter 和缓存中的内容。
7. Context Lifecycle、Delivery Lifecycle、ContextEntry Lifecycle 是否是三个独立状态机。
8. Rust 实现是否有可执行的 CAS/串行提交、事务边界、重试、重放和恢复模型。

因此，不能依据 README 或系统架构中的原则性描述，推断 G 已经完成这些契约。也不能依据 C 的 Adapter 设计，反向补写或替代 G 的内部权威模型。

### 2.2 可保留的总体架构基线

本次确认以下原则在现有基线中表达清晰，且应继续作为 G 的强制约束：

- Brain 是其管理的 Memory Context 的逻辑权威；Adapter 是执行者，不是记忆规则制定者。
- Canonical Memory、Memory Context、Applied Context 是不同层次。
- Context 不等于完整 Prompt，也不等于 Canonical Memory Store。
- Context Entry 引用 Canonical Memory Version，不拥有或修改 Canonical Memory。
- Context Remove 不等于 Forget。
- Context 变更在下一次 inference-context assembly boundary 生效，不假设修改正在进行的推理。
- System / Developer / User 原始区域及 Agent 安全策略不可由 Context Editor 覆盖。
- Memory 内容是数据，不获得指令层级、工具授权或行动策略权力。
- Adapter 的 ACK 不证明模型理解、注意或遵从内容。
- Context Version、Memory Version、Delivery ID、Inference Request ID 必须分离。
- Scope 与 Permission 分离，跨 Agent/Instance/Task/Environment 必须隔离。

这些是**基线原则通过**，不是 G 设计文档通过。

### 2.3 三方结论摘要

| 审查方 | 结论 | 核心理由 |
|---|---|---|
| 第一方：系统架构师 | FAIL / NOT REVIEWABLE | G 的组件职责、Context 权威边界、D/F/H/I 交接契约无 G 文档可核验 |
| 第二方：工程实现负责人 | FAIL / NOT REVIEWABLE | 无对象模型、事务、状态机、原子性和并发协议，无法推演完整实现路径 |
| 第三方：安全与可靠性审计者 | FAIL / NOT REVIEWABLE | 无 G 的 Scope 检查点、Forget 传播、撤权、离线副本与 Applied 证据契约 |

---

## 3. 三方独立审查结论

### 3.1 第一方：系统架构师

**结论：FAIL — 无法确认 G 是否真正拥有 Context 逻辑权威。**

现有系统架构基线将 MR-03 Memory Context Manager 定义为 Context 的规划、编辑、版本管理、预算和 Reconciliation 主责；MR-04 Context Synchronization Engine 负责 Snapshot/Delta 交付和 Adapter ACK 跟踪。责任矩阵也明确 MCM 拥有 Context Version Authority，Sync 只拥有 Delivery Tracking。

该划分在原则上正确，但本次缺少 G 设计文档，无法验证以下职责是否在内部组件之间被正确分配：

- Context Planner 是否只决定候选内容与原因，不自行写入权威版本。
- Activation Policy 是否只提出激活建议，不直接变更 Context。
- Context Editor 是否是唯一生成 ChangeSet 的受控入口。
- Versioning 是否是唯一分配 Context Version 的组件。
- Reconciler 是否修复投影/Adapter 状态，而不是创建第二条版本权威序列。
- Budget Manager 是否能触发受控编辑，但不能绕过版本事务。
- Coordinator 是否只是编排，不拥有第二个 Context Version。
- Adapter 是否只执行 Brain 签发的操作，不自行选择、合并或删改记忆。

**架构判断：** 保留 MR-03/MR-04 的所有权边界；在 G 文档提交前，禁止将此边界视为已经落实。

### 3.2 第二方：工程实现负责人

**结论：FAIL — 无法证明 ChangeSet 的原子性、幂等性和并发正确性。**

没有 G 的对象模型和事务章节，无法完成任务书要求的正常路径、失败路径和并发路径推演。尤其无法证明以下路径安全：

**正常路径应当能够证明：**

1. 收到带有来源、Scope、授权上下文和索引水位的 Retrieval/Activation Result。
2. Planner 产生计划，保留 activation_reason、source_refs 和 Memory Version。
3. Editor 基于当前 Context Version 准备 ChangeSet。
4. Versioning 校验 Base Version、权限/撤销 epoch 和幂等身份。
5. 事务性提交完整 ChangeSet，分配唯一 Target Version。
6. Sync 为提交版本建立唯一 Delivery ID，发送 Snapshot 或 Delta。
7. Adapter 在未来推理组装边界执行完整应用。
8. ACK 关联 Delivery ID、Context ID、Target Version、Capability Epoch 和 Inference Request ID。
9. Reconciler 对 ACK、超时、版本差异和未知状态作幂等处理。

**失败路径必须定义但目前无法核验：**

- CAS 冲突后旧 ChangeSet 不得部分落地。
- Commit 成功但响应丢失，重试不得重复生成新版本。
- Delta 多操作中任一操作失败时，目标版本不得部分可见。
- Snapshot 不完整、hash 不匹配或版本不兼容时，Adapter 不得报告 Full Applied。
- Delivery timeout 不等于失败，也不等于 Applied；必须进入查询/对账。
- 迟到 ACK 不得覆盖更高版本或已撤销状态。
- Adapter 重启后不得重复追加 Entry 或回退 Context Version。
- Reconciliation 重放必须幂等，且不可把历史旧 Delivery 变成当前状态。

**并发路径必须定义但目前无法核验：**

- 同一 Context 两个并发 ChangeSet 竞争同一 Base Version。
- 一个 ChangeSet 成功后，另一个基于旧 Base Version 的提交应被拒绝或重算。
- Context Remove 与 Memory Revision/Forget 同时发生时，不能恢复已失效引用。
- Revoke 与 Delivery/Apply 并发时，必须有确定的线性化检查点。
- 多个 Adapter Session 或多 Environment 不得共用版本序列，除非显式定义为同一个 Context Scope。

**工程判断：** 无法基于缺失文档认定 Rust 事务可行或不可行。不得声称完成了 Rust 状态机或数据库事务验证。

### 3.3 第三方：安全与可靠性审计者

**结论：FAIL — 关键安全与删除传播链没有可审查的 G 契约。**

基线已经要求 Scope/Permission 全链路检查、Forget 覆盖派生副本、Memory 不提升为指令权力。但 G 必须明确这些要求在 Context 管理层的检查时点、数据对象和失败状态。本次无法确认：

- Context 与 Entry 是否绑定 authenticated principal、user、agent、agent_instance、task、environment、context_session。
- Entry 对 memory_id/memory_version 的引用是否在读取、编辑、Delivery、Apply 前重新授权。
- Snapshot、Delta、Pending Delivery 和 Adapter Cache 是否都绑定 Scope 与 capability/revocation epoch。
- Forget 是否先阻断访问，再异步清理副本。
- Offline Adapter 是否在 reconnect 时必须先执行 revocation check 和 reconciliation，才能恢复 Context 使用。
- Applied/cleanup 是否区分 Brain 已提交、Adapter 已收到、Adapter 已应用、Adapter 已确认清理。
- 不可信 Memory 的 Trust、Epistemic Status、Provenance 是否保留到最终 managed region。
- Editor 是否只能修改 Brain-owned managed region，无法触及 System/Developer/User/Policy/Tool 权限区域。

**安全判断：** 不能把“Brain 已删除 Canonical Memory”推导为“所有 Context/Adapter 副本已清除”；不能把 Adapter 自报 ACK 推导为独立可信的最终请求证明。

---

## 4. 六维度逐项审查

### 维度一：架构与职责边界

| 检查项 | 状态 | 证据与理由 |
|---|---|---|
| Brain 是 Memory Context 逻辑权威 | PARTIAL | I-01、P-01 和系统架构明确原则；无 G 内部设计证明唯一权威写路径 |
| Adapter 是执行者而非规则制定者 | PASS（基线） | README、系统架构和 C 设计明确；G 侧执行契约未验证 |
| Canonical Memory / Memory Context / Applied Context 分离 | PASS（基线） | System Overview、Terminology、Domain Model 均有定义 |
| Context 不等于完整 Prompt | PASS（基线） | System Overview 的 managed region 与 inference boundary 原则 |
| Planner / Activator / Editor / Versioning / Reconciler / Budget Manager 职责 | NOT ASSESSABLE | G 文件缺失 |
| 唯一 Context Version Authority | PARTIAL | Component Map/Responsibility Matrix 声明 MCM 主责；无 G 版本写入与分配规范 |
| D/F/G/H 不产生多权威版本 | PARTIAL | A/B/C 集成原则可读；D/F/G/H 设计交付不齐 |
| 多 Agent/Task/Environment Context 独立 | PARTIAL | Scope 原则存在；G Context Scope/Session 身份字段缺失 |

**结论：** 架构方向有基线支持，但 G 具体职责分配未审查通过。

### 维度二：领域模型与数据契约

任务书要求的以下对象均无法从 G 设计文档核验：

- MemoryContext
- ContextEntry
- ContextChangeSet
- ContextOperation
- ContextDelivery
- AgentContextSession
- Context Snapshot
- Context Delta
- Applied Attestation
- Applied Coverage
- Inference Request Correlation

| 字段/语义 | 状态 | 必须满足的契约 |
|---|---|---|
| context_id | NOT ASSESSABLE | 稳定标识一个独立 Context |
| scope | NOT ASSESSABLE | 明确 namespace 与隔离边界，不等同 permission |
| agent_instance_id / task_id / environment_id | NOT ASSESSABLE | 防止实例、任务、环境串用 |
| context_version | NOT ASSESSABLE | G 唯一权威、不可变、单调序列 |
| applied_version | NOT ASSESSABLE | Adapter 在约定边界确认的版本，不替代 context_version |
| memory_id / memory_version | NOT ASSESSABLE | 引用 D 的不可变 Canonical Version，不与 Context Version 混用 |
| base_version / target_version | NOT ASSESSABLE | ChangeSet 的前置版本与提交目标 |
| idempotency_key | NOT ASSESSABLE | 同 key 同 payload 返回原结果；同 key 异 payload 明确冲突 |
| delivery_id | NOT ASSESSABLE | 每次逻辑交付的独立标识 |
| inference_request_id | NOT ASSESSABLE | 关联最终推理请求，不可与 delivery_id 互换 |
| capability_epoch | NOT ASSESSABLE | 与 Adapter 能力/撤销状态绑定 |
| activation_reason / source_refs | NOT ASSESSABLE | 可回答为何加入及来源 |
| content_hash | NOT ASSESSABLE | 明确 canonicalization、算法版本、隐私边界和用途 |

**必须保持的版本区分：**

- Memory Version：D 对 Canonical Memory 的版本。
- Context Version：G 对特定 Context 内容状态的唯一版本。
- Delivery ID：H/G 对一次投递实例的标识。
- Inference Request ID：Adapter/Inference Runtime 对一次最终请求的标识。

不得用一个 revision、sequence 或 status 字段兼任上述四者。

### 维度三：数据流与一致性

任务书定义的数据流：

`Retrieval Result → Context Planning → Change Set Preparation → Version Validation → Commit → Delivery → Adapter Application → Acknowledgement → Reconciliation`

本次没有 G 设计文件，因此每一阶段均不能做实现级 PASS 判断。

| 阶段 | 状态 | 必须具备的可验证条件 |
|---|---|---|
| Retrieval Result | PARTIAL | F 输出必须是候选而非 ContextEntry；带 Scope、Memory Version、来源与完整性水位 |
| Context Planning | NOT ASSESSABLE | Planner 记录选择/排除原因，不写权威版本 |
| ChangeSet Preparation | NOT ASSESSABLE | 生成不可变操作集合，绑定 Base Version、Scope、授权与幂等键 |
| Version Validation | NOT ASSESSABLE | CAS/串行提交；检查 Memory Revision、撤销 epoch、Base Version |
| Commit | NOT ASSESSABLE | 全部操作原子提交；分配单调 Target Version |
| Delivery | PARTIAL | C/H 有交付原则；G 的 Delivery/Version 绑定缺失 |
| Adapter Application | PARTIAL | C 定义 inference boundary；缺少 G 的原子 Snapshot/Delta 语义 |
| Acknowledgement | PARTIAL | C 指出 ACK 不足以证明最终请求完整性；G/H 统一契约缺失 |
| Reconciliation | NOT ASSESSABLE | timeout、迟到 ACK、版本跳跃、离线重连无 G 状态机证据 |

#### 三个独立状态机

| 状态机 | 必须独立拥有的状态 | 本次结论 |
|---|---|---|
| Context Lifecycle | Active / Suspended / RevocationBlocked / Closed 等 Context 管理状态（具体枚举需 G 定义） | NOT ASSESSABLE |
| Context Delivery Lifecycle | Prepared / Queued / Delivered / Applying / Applied / Partial / Rejected / Unknown / Expired 等交付状态（具体枚举需 G/H 定义） | NOT ASSESSABLE |
| ContextEntry Lifecycle | Proposed / Active / Stale / Removed / Revoked 等 Entry 状态（具体枚举需 G 定义） | NOT ASSESSABLE |

禁止将上述三个状态机压缩为一个 status 字段。尤其 Context Active 不意味着 Delivery Applied；Delivery Applied 不意味着每条 Entry 仍然有效；Entry Removed 不意味着 Canonical Memory Forgotten。

#### Snapshot / Delta 原子性

当前无 G 证据证明：
- Snapshot 是目标 Context 的完整替换，而不是局部追加。
- Delta 绑定 from_version/to_version，且只允许在精确 Base Version 上应用。
- 多操作 ChangeSet 是 all-or-nothing。
- 局部失败不产生可见的混合版本。
- 重复 Delivery 不会重复 Entry 或回退版本。
- 版本缺口时必须获取 Snapshot 或执行有界重放。
- Snapshot 与 Delta 具有可验证 hash/manifest，且 schema/capability 兼容性先行检查。

**维度结论：FAIL（核心设计材料缺失）。**

### 维度四：安全与治理

#### INT-P0-02 — Scope Isolation

状态：**PARTIAL / NOT VERIFIED**

已有基线：I-13、P-12、B 的 Scope/Permission Model，以及 A/B/C 集成审查要求 Scope 在候选生成前过滤并贯穿缓存、Context、异步任务和 Apply。

G 必须进一步证明：
- Context Scope 不能由 Agent 自报字符串直接建立授权。
- 每个 Entry 的 Canonical Memory 引用重新授权。
- Snapshot、Delta、Delivery、Cache 均绑定 scope/principal/agent_instance/task/environment 与权限/撤销 epoch。
- Agent Instance 或 Environment 改变时不得复用旧 Context。
- Delivery 与 Apply 前重新授权，拒绝或阻断旧权限内容。
- 日志和审计不泄露跨 Scope Memory 内容。

当前 G 文件缺失，不能认定该 P0 已关闭。

#### INT-P0-03 — Forget / Revocation

状态：**PARTIAL / NOT VERIFIED**

以下所有副本/阶段均没有 G 级传播证据：

| 位置 | 必须证明的行为 | 状态 |
|---|---|---|
| Active Context Entry | 立即阻断读取/使用，进入撤销状态 | NOT VERIFIED |
| Pending Change Set | 阻止提交或重基时剔除撤销内容 | NOT VERIFIED |
| Prepared Delivery | 取消或使其不可应用 | NOT VERIFIED |
| Delivered but not Applied | Apply 前重新检查授权/撤销 epoch | NOT VERIFIED |
| Applied Context | 阻断后续推理复用；按能力清理 | NOT VERIFIED |
| Snapshot | 撤销引用并阻止旧快照恢复使用 | NOT VERIFIED |
| Delta Log | 受控保留/重放，不得复活撤销内容 | NOT VERIFIED |
| Adapter Local Cache | 失效、清理、隔离或声明无法确认 | NOT VERIFIED |
| Offline Adapter | 离线期间不得继续使用已失效的授权内容；能力边界需明示 | NOT VERIFIED |
| Reconnect | 先撤销检查与 Reconciliation，后恢复 Context 使用 | NOT VERIFIED |

状态语义必须至少区分：
- Forget Requested
- Access Blocked
- Cleanup Pending
- Adapter Acknowledged
- Cleanup Confirmed
- Failed
- Unknown

Brain 删除 Canonical Memory 不能直接等价于所有 Adapter 本地副本物理删除。Adapter 无法提供可信清理证明时，必须保留 Unknown/Failed，而不是 Cleanup Confirmed。

#### INT-P0-04 — Prompt Injection

状态：**PARTIAL / NOT VERIFIED**

已有基线：I-12、P-11 和 C 的 managed region 原则，禁止覆盖 System/Developer/User 与 Agent 安全策略。

G 必须证明：
- Memory Trust、Epistemic Status、Provenance 和 Source Ref 不因 Context Rendering 丢失。
- Entry 的自然语言内容始终是数据，不可通过 Context Operation 变成强制指令。
- Context 操作不能改变 Tool Authorization、Agent Policy 或安全策略。
- 不可信内容的结构化标记不被宣称为模型层绝对安全边界。
- 伪造 system 标签、间接提示注入、跨 Scope 内容进入 Context 均进入对抗性测试。

**维度结论：FAIL（安全传播契约缺失，P0 门槛未证明）。**

### 维度五：性能与资源

由于 G 设计文件缺失，本轮无法核验实际预算算法、数据结构或复杂度分析。不得编造 Benchmark 或延迟数字。

| 检查项 | 状态 | 最低设计要求 |
|---|---|---|
| Entry 数量预算 | NOT ASSESSABLE | 限制数量并说明按何种 Scope/任务分配 |
| Token / Byte Budget | NOT ASSESSABLE | 区分模型 Token、传输 Byte、持久化大小 |
| Snapshot 构建成本 | NOT ASSESSABLE | 说明全量构建、压缩、hash 与并发读写成本 |
| Delta 传输成本 | NOT ASSESSABLE | 说明增量阈值、版本间距、回退 Snapshot 条件 |
| Reconciliation 成本 | NOT ASSESSABLE | 说明按 Context/Delivery 扫描、重试与限流 |
| 大量 Memory Revision | NOT ASSESSABLE | 识别 Stale Entry 并避免无界重算 |
| 高并发 Context 更新 | NOT ASSESSABLE | 串行化/CAS 冲突率、重试上限与公平性 |
| 多 Agent Session | NOT ASSESSABLE | 隔离索引、队列、缓存与预算 |
| Context Compact | NOT ASSESSABLE | 保留 Provenance、Evidence 展开引用与压缩版本身份 |
| Evidence 展开 | NOT ASSESSABLE | 按需访问并重新授权，不把证据全文无界注入 |
| Context Sufficiency | NOT ASSESSABLE | 多维覆盖与风险约束，不仅 Top-K/Token 数 |
| Applied 确认延迟 | NOT ASSESSABLE | 以实测定义，不给未经 Benchmark 的固定承诺 |

预算/充分性至少应评估：
- Semantic Coverage
- Entity Coverage
- Relation Coverage
- Environment Coverage
- Temporal Validity
- Evidence Coverage
- Risk Coverage
- Uncertainty Coverage
- Redundancy
- Compression Cost

Budget Manager 不得为了满足 Token 上限静默截断、移除安全关键项或让 Adapter 自行改变内容。压缩/Compact 若改变 Context 的语义内容，应通过受控 ChangeSet 形成新 Context Version，并保留来源引用。

**维度结论：FAIL / NOT ASSESSABLE。**

### 维度六：可演进性与可观测性

| 检查项 | 状态 | 最低要求 |
|---|---|---|
| Context Schema Version | NOT ASSESSABLE | 与 Context Version 分离 |
| Context Version | NOT ASSESSABLE | 唯一权威、单调、不可变 |
| ChangeSet Version | NOT ASSESSABLE | 定义操作语义/Schema 兼容 |
| Delivery Version | NOT ASSESSABLE | 关联 delivery_id，不与 Context Version 混同 |
| Adapter Capability Epoch | PARTIAL | C 提及能力协商；G/H 联合契约未闭合 |
| Snapshot / Delta 兼容 | NOT ASSESSABLE | 明确 schema、base/target、hash、能力要求 |
| Applied Attestation | PARTIAL | C 有原则；G 的证明字段与覆盖定义缺失 |
| Delivery Error | NOT ASSESSABLE | 明确可重试/不可重试/未知/部分失败 |
| Reconciliation Event | NOT ASSESSABLE | 可重放、可排序、可审计 |
| Audit Trail | PARTIAL | 治理原则存在；G 的事件链缺失 |
| Correlation Chain | PARTIAL | C 有多种 ID；G/H 端到端关系未闭合 |
| Context Update Metrics | NOT ASSESSABLE | 版本滞后、冲突、变更原因、预算拒绝 |
| Applied Coverage Metrics | NOT ASSESSABLE | Full/Partial/Bypassed/Unknown 等覆盖语义 |

系统必须能回答：
1. 为什么添加/移除一条 Entry？
2. 哪个 Canonical Memory Version 被引用？
3. 哪个 Context Version 被提交？
4. 哪个 ChangeSet 和 Delivery 执行了变更？
5. Adapter 收到的具体 Snapshot/Delta 是什么？
6. Adapter 实际应用了哪些操作？
7. 目标版本是否进入指定 Inference Request 的最终提交边界？
8. 若无法证明，为什么状态为 Partial/Unknown？

**维度结论：FAIL / NOT ASSESSABLE。**

---

## 5. 逐文件审查矩阵

| 文件 | 状态 | 结论/说明 |
|---|---|---|
| `README.md` | READ | 总体原则支持 Brain Context 权威；非 G 详细契约 |
| `ARCHITECTURE_ROADMAP.md` | READ | 要求完整子系统规格和可测试验收；G 未达到可见交付状态 |
| `00-governance/architecture-invariants.md` | READ | I-01、I-07 至 I-13、I-16 至 I-20 为 G 的强制约束 |
| `00-governance/design-principles.md` | READ | P-01、P-08 至 P-13、P-15 为 G 的强制约束 |
| `00-governance/terminology.md` | READ | Context/Entry/Applied Context/Forget 定义明确 |
| `01-system-architecture/system-overview.md` | READ | 定义三层 Context、inference boundary 和隔离原则 |
| `01-system-architecture/component-map.md` | READ | MR-03 为 Context 主责、MR-04 为同步主责 |
| `01-system-architecture/responsibility-matrix.md` | READ | 明确 MCM 管 Context Version，Sync 管 Delivery Tracking |
| `02-domain-model/domain-model-overview.md` | READ | Memory Version 与 Context Version 是不同语义对象 |
| `02-domain-model/core-entities.md` | READ | Context Entry 是引用/呈现，不是 Canonical Memory |
| `02-domain-model/scope-and-permission-model.md` | READ | 提供 Scope/Permission 基线；G 层执行点未核验 |
| `02-domain-model/lifecycle-model.md` | READ | Canonical Lifecycle 与 Context 生命周期不能混用 |
| `02-domain-model/relationships-and-provenance.md` | READ | 为来源引用提供基线；G 是否保留引用未验证 |
| `06-memory-context/context-architecture.md` | MISSING | 无法审查 |
| `06-memory-context/context-manager.md` | MISSING | 无法审查 |
| `06-memory-context/context-edit-operations.md` | MISSING | 无法审查 |
| `06-memory-context/context-versioning.md` | MISSING | 无法审查 |
| `06-memory-context/context-reconciliation.md` | MISSING | 无法审查 |
| `06-memory-context/context-budget-and-sufficiency.md` | MISSING | 无法审查 |
| `07-agent-integration/agent-integration-overview.md` | READ | Adapter 边界可读；不能替代 G 内部语义 |
| `07-agent-integration/adapter-capability-tiers.md` | READ | Tier/能力原则可读；Snapshot/Delta 原子性待 G/H |
| `07-agent-integration/inference-boundary-model.md` | READ | 最终请求边界原则可读；证明链待 G/H 收敛 |
| `08-protocols/*` | MISSING | BMCP wire contract 未验证 |
| `reviews/integration/phase-1-abc-cross-document-integration-review.md` | READ | INT-P0-02/03/04、INT-P1-01/05 等门禁已明确 |
| `reviews/06-memory-context/three-party-six-dimension-review.md` | MISSING | 本报告为首次创建 |

---

## 6. Context 三层模型审查

| 层次 | 语义 | 权威 | 本轮结论 |
|---|---|---|---|
| Canonical Memory | 持久化、可追溯的知识资产及其不可变 Memory Version | D / Canonical Memory Authority | 基线清楚；D 设计缺失 |
| Memory Context | 特定 Scope/Agent Instance/Task/Environment 的版本化记忆视图 | G / MCM | 基线声明清楚；G 设计缺失，唯一权威未被具体契约证明 |
| Applied Context | Adapter 在约定推理边界确认应用的 Context 版本/覆盖 | Adapter 执行，Brain 记录权威状态 | C 有原则；G/H 的 attestation 与最终请求证明缺失 |

必须防止以下错误：
- 将 Retrieval Result 直接视为 Context Entry。
- 将 Context Entry 当成 Canonical Memory 的复制所有权。
- 将 Applied Context 当成新的 Memory Version。
- 将 Adapter Cache 当成 Context 权威副本。
- 将完整 Prompt 或 System/Developer/User 原始区域纳入 MCM 的可编辑范围。

**结论：** 三层模型的概念定义通过基线检查；三层之间的版本与证明接口未通过 G 专项审查。

---

## 7. 三个独立状态机审查

### 7.1 Context Lifecycle

必须表达 Context 本身的创建、可用、暂停、撤销阻断、关闭/归档等生命周期。实际枚举由 G 决定，但必须与 Entry 和 Delivery 状态分离。

### 7.2 Context Delivery Lifecycle

必须表达单次交付从准备、排队、发送、接收、应用、拒绝、部分应用、超时未知、过期到对账修复的状态。Delivery 状态不得反向成为 Context Version 的权威。

### 7.3 ContextEntry Lifecycle

必须表达 Entry 被提议、激活、变陈旧、移除、撤销或被替换的状态。Entry Remove 不得隐式触发 Canonical Forget。

**审查结果：三个状态机全部 NOT ASSESSABLE。** G 文档缺失，无法确认它们是否独立建模。不得以单个 `status` 字段代替三个状态机。

---

## 8. Context Version / Change Set 审查

### 8.1 唯一权威

系统架构和责任矩阵声明 MCM 是 Context Version 的主责方。正确的权威规则应为：

- G 的 Context Versioning 是每个 context_id 的唯一版本分配者。
- Planner、Editor、Reconciler、Coordinator、Sync、Adapter 都不能各自生成权威版本。
- 每次成功提交产生一个不可变 Context Version。
- 同一 Context 的成功提交必须单调递增且可线性化排序。
- Adapter 的 applied_version 是执行观察，不是另一条权威版本序列。

### 8.2 ChangeSet 最低契约

每个 ChangeSet 至少应包含：
- change_set_id
- context_id 与 scope
- base_version
- target_version（提交前可为空，提交后固定）
- schema_version / operation_version
- ordered operations
- actor/principal 与授权依据
- idempotency_key
- reason / activation_reason
- source_refs
- expected content hash 或等效完整性信息
- capability/revocation epoch
- created_at / committed_at
- audit correlation

### 8.3 CAS / 串行提交

同一 Context 的并发变更必须使用 CAS 或等效串行化：
- 当前版本必须等于 ChangeSet.base_version。
- 不相等时拒绝旧 ChangeSet 或要求重新规划，不允许隐式套用到新版本。
- 成功提交时原子地产生一个新的 Target Version。
- Commit 成功但响应丢失时，幂等重试返回原提交结果，不得产生第二个版本。
- 两个并发 ChangeSet 不能都成功地从同一 Base Version 产生同一条线性序列的分叉头。

### 8.4 多操作 ChangeSet

一个 ChangeSet 有多个 Add/Remove/Replace 操作时，默认必须 all-or-nothing：
- 任一操作校验失败，整个 ChangeSet 不提交。
- 不允许部分操作已可见、部分操作仍待完成，却把整体标记为 Applied。
- 若业务确实需要部分接受，必须拆成独立 ChangeSet/Target Version，或明确设计可审计的分段事务；不得伪装成原子提交。

**审查结果：INT-P1-01 FAIL（G 关键设计缺失，跨模块契约未闭合）。**

---

## 9. Snapshot / Delta 原子性审查

### Snapshot 必须定义

- 对明确 context_id、scope、schema_version 和 target_version 的完整状态替换。
- manifest/entry count/hash 或等效完整性校验。
- 先构建并验证新快照，再原子切换当前 Adapter managed region。
- 失败时保留旧的完整状态，不能出现新旧 Entry 混合。
- Snapshot 不得覆盖 managed region 之外的 System/Developer/User/Policy/Tool 区域。

### Delta 必须定义

- from_version 与 to_version。
- 精确 base version 检查。
- 有序、可幂等的操作集合。
- 全部操作成功后才原子提交新版本。
- 任一操作失败时回滚或保持旧版本，并返回明确失败/Partial/Unknown。
- 版本跳跃时拒绝直接应用，触发 Snapshot 或有界 Delta 重放。
- 重复应用相同 delivery/change_set 不得重复添加或造成版本回退。

### 关键失败场景

| 场景 | 必须结果 |
|---|---|
| Snapshot 内容截断 | Reject/Unknown；不得 Applied |
| Snapshot hash 不匹配 | Reject；旧版本保持完整 |
| Delta Base Version 不匹配 | Conflict；不得部分应用 |
| 多操作中第 N 项失败 | 全部回滚或显式分段提交；不得 Full Applied |
| ACK 丢失 | 查询 Delivery 状态；不得盲目重放为新操作 |
| 迟到 ACK | 校验 Delivery、Context、Target Version、Capability Epoch |
| Adapter 重启 | 读取持久化 Applied 状态并对账，不重复追加 |
| Context Version 跳跃 | Snapshot repair 或确定性 replay |
| Forget 与旧 Snapshot 并发 | 撤销 epoch 阻断旧 Snapshot 安装 |

**审查结果：FAIL / NOT ASSESSABLE。**

---

## 10. Applied Proof 审查

C 的 `inference-boundary-model.md` 与 C 专项审查已明确：Applied 的必要条件不是 Adapter 在中间模板上完成插入，而是目标版本的完整 managed region 确实属于本次提交给 inference runtime 的最终请求上下文。不能观测最终请求的 Adapter 不得过度声明 Tier 1/Full Applied。

G/H 必须共同定义 Applied Attestation，至少关联：

- context_id
- context_version
- delivery_id
- change_set_id（适用时）
- agent_instance_id / context_session_id
- capability_epoch
- inference_request_id
- boundary_id 或等效最终提交点身份
- applied_coverage
- applied_content_hash / digest（若采用）
- applied_at
- adapter identity / attestation provenance
- authorization/revocation epoch
- status 与 reason

Coverage 不得只用一个含糊布尔值。至少要区分：
- Full
- Partial
- Bypassed
- Unknown
- Rejected（作为明确拒绝结果）

证明强度必须分层：
1. Adapter 收到包：Received。
2. Adapter 完成局部变更：Applied Partial 或内部应用结果。
3. Adapter 完整应用目标版本到 managed region：Adapter Applied。
4. 目标版本的完整 managed region 属于指定最终提交给 Inference Runtime 的请求：Boundary-Applied。
5. 模型理解、注意或遵从：**不属于 Applied Proof 的可证明范围。**

不能独立观测最终请求边界时，必须标记 Unknown/Partial 或使用较低能力等级，不得以 Adapter 自报 Applied 代替完整证明。

**审查结果：INT-P1-05 FAIL（C 已指出风险，G/H 最终契约缺失）。**

---

## 11. Forget / Revocation 传播审查

Forget 必须先阻断使用，再执行清理。G 的工作不是替代 I 的治理权威，而是确保 Context 管理域提供可执行、可追踪的撤销和清理状态。

建议的最低传播顺序：

1. 接收经授权的 Forget/Revocation Event，确认 scope 与目标 Memory Version。
2. 提升或读取撤销 epoch，立即阻断新 Context 引用与旧 Delivery 应用。
3. 将 Active Context Entries 标记为 revoked/stale 并禁止继续进入后续推理边界。
4. 取消/失效 Pending ChangeSet、Prepared Delivery 和 Delivered-but-not-Applied Delivery。
5. 对已 Applied Context 发出 Adapter 清理/替换请求；若无法确认物理清理，保留 Unknown。
6. 使 Snapshot/Delta/Cache/Working Set 的旧引用不可恢复使用。
7. Offline Adapter reconnect 时先执行认证、授权、撤销 epoch 检查与 Reconciliation，再允许恢复 Context。
8. 记录每个副本的阻断、清理请求、ACK、确认、失败和未知状态。
9. 只有达到治理定义的 Cleanup Confirmed 条件，才能宣称清理完成；不得将 Brain 侧提交视为外部物理删除证明。

### 状态区分

| 状态 | 含义 | 禁止的错误推断 |
|---|---|---|
| Forget Requested | 请求已登记 | 不代表访问已阻断 |
| Access Blocked | 系统已阻断进一步使用 | 不代表副本已清理 |
| Cleanup Pending | 清理正在进行 | 不代表 Adapter 已确认 |
| Adapter Acknowledged | Adapter 已回执清理/替换操作 | 不必然证明所有本地介质物理擦除 |
| Cleanup Confirmed | 达到明确定义的清理证明条件 | 仅能对声明范围作保证 |
| Failed | 清理明确失败 | 不得隐藏为成功 |
| Unknown | 无法证明结果 | 不得当作完成 |

**审查结果：INT-P0-03 PARTIAL / NOT VERIFIED；INT-P1-06 FAIL。**

---

## 12. P0/P1/P2/P3 问题清单

以下 Review ID 为本报告新增的 G 专项追踪 ID。它们不替代既有 INT-* ID。

### P0 — 阻断性安全门槛

#### G-SEC-P0-01 — Context Scope 与 Permission 检查链缺少 G 侧证明

- **Severity：** P0
- **File / Section：** `06-memory-context/*`（全部缺失）；关联 `02-domain-model/scope-and-permission-model.md`、`07-agent-integration/inference-boundary-model.md`
- **Evidence：** G 目录及六份核心设计文档在 main 分支不可读取；INT-P0-02 要求全链路 Scope 隔离。
- **Problem：** 无法证明 Context、Entry、Snapshot、Delta、Delivery、Cache 在候选读取、提交、Delivery、Apply、Reconnect 时持续绑定主体、Scope、Environment 与授权版本。
- **Impact：** 若实现仅在入口授权，可能发生跨用户/Agent/Task/Environment 混用或撤权后旧 Context 继续使用。
- **Required Correction：** G 定义 Context Scope 绑定、逐操作授权检查点、Memory 引用重授权、撤销 epoch 和缓存键隔离；I/H 提供权威授权/撤销契约。
- **Owner：** G + I；H、D、F 协作。
- **Dependency：** INT-P0-02、B DM-010、C P1-03/P1-07。
- **Acceptance Criteria：** 跨 Scope 负向测试覆盖候选、Entry、Snapshot、Delta、Delivery、Applied、Cache、Reconnect；未经授权结果为零；撤权后旧版本无法进入下一次推理边界。

#### G-SEC-P0-02 — Forget 无法证明传播至 Context 与 Adapter 管理副本

- **Severity：** P0
- **File / Section：** `06-memory-context/context-reconciliation.md`（缺失）；关联 D/E/H/I Forget 契约（未完整提交）
- **Evidence：** INT-P0-03 明确要求覆盖 Context Entry、Pending ChangeSet、Prepared/Delivered Delivery、Applied Context、Snapshot、Delta、Adapter Cache、Offline Adapter 和 Reconnect。
- **Problem：** 缺少 G 侧撤销阻断、清理状态、旧快照失效和离线重连流程。
- **Impact：** Forget 后旧 Context 或离线缓存可能继续被使用；系统可能错误宣称删除完成。
- **Required Correction：** 先 Access Block，再传播清理；定义撤销 epoch、Delivery 取消/失效、Adapter 清理 ACK、Unknown/Failed 与 Cleanup Confirmed。
- **Owner：** I 主责治理语义；G 主责 Context 传播；H 主责 Adapter/协议执行；D/E 提供 Memory/Compiler 变更事件。
- **Dependency：** INT-P0-03、INT-P1-06、B DM-011、C P1-07。
- **Acceptance Criteria：** 覆盖 Forget 与 Pending/Delivered/Applied/Offline/Reconnect 并发故障注入；未确认的副本不得显示 Cleanup Confirmed；撤销内容不能被旧 Snapshot/Delta 重放复活。

#### G-SEC-P0-03 — Memory 内容与受保护推理区域之间缺少 G Editor 的不可越权证明

- **Severity：** P0
- **File / Section：** `06-memory-context/context-edit-operations.md`（缺失）；关联 `07-agent-integration/inference-boundary-model.md`
- **Evidence：** I-12、P-11 和 INT-P0-04 要求 Memory 是数据，不获得 System/Developer 指令权力；G Editor 设计未提交。
- **Problem：** 无法证明 Add/Replace/Compact/Render 操作只能作用于 Brain-managed region，不能覆盖 System/Developer/User 原始区域或 Agent 安全策略。
- **Impact：** 若编辑接口边界不清，可能出现受保护区域覆盖、恶意 Memory 被提升为指令或工具权限被记忆内容影响。
- **Required Correction：** 明确 managed region 的不可变边界、类型化操作白名单、Trust/Provenance 保留规则；工具授权和 Agent Policy 始终由 Agent 侧拥有。
- **Owner：** G + H + I；Agent 安全策略由 Agent Owner 负责。
- **Dependency：** INT-P0-04、C P2-07。
- **Acceptance Criteria：** 对 System/Developer/User/Policy/Tool 区域的所有写入尝试均被拒绝；恶意 Memory、伪造 system 标签、间接注入和跨 Scope 样例不能改变权限或编辑边界。

### P1 — 核心契约阻断项

#### G-CTX-P1-01 — Context Version / ChangeSet 权威模型缺失

- **Severity：** P1
- **File / Section：** `06-memory-context/context-versioning.md`（缺失）
- **Evidence：** I-09、I-17；Component Map/Responsibility Matrix 将 MCM 指定为 Context Version 主责；INT-P1-01。
- **Problem：** 无法证明唯一版本分配者、Base/Target Version、不可变快照、CAS/串行提交和并发冲突语义。
- **Impact：** 多个组件可能创建竞争版本，产生分叉、丢失更新或历史状态不可重建。
- **Required Correction：** G 定义单一权威版本服务/模块、不可变版本记录、CAS、提交身份、幂等键和冲突重算流程。
- **Owner：** G。
- **Dependency：** INT-P1-01、C P2-05/P2-06、D Memory Version 契约。
- **Acceptance Criteria：** 并发同 Base Version 只能有一个线性化成功；版本严格单调；成功提交响应丢失后的重试返回原结果。

#### G-CTX-P1-02 — 多操作 ChangeSet 的原子性和局部失败语义缺失

- **Severity：** P1
- **File / Section：** `06-memory-context/context-edit-operations.md`、`context-versioning.md`（缺失）
- **Evidence：** C 审查 P2-05 明确要求 G 定义 Snapshot/Delta 原子性；I-16 要求幂等。
- **Problem：** 无法证明多个 Add/Remove/Replace 操作是否 all-or-nothing，以及局部失败时是否回滚。
- **Impact：** Context 可能暴露混合状态；Adapter 可能对部分应用错误报告 Full Applied。
- **Required Correction：** 默认 ChangeSet 原子提交；若采用分段事务，必须将各段变成独立可审计版本，不得以一个整体 Applied 掩盖部分成功。
- **Owner：** G + H。
- **Dependency：** INT-P1-01、INT-P1-05、C P2-05。
- **Acceptance Criteria：** 任一操作失败时无部分目标版本可见；重复应用不产生重复 Entry；所有 Partial/Rejected 状态都有明确 coverage。

#### G-CTX-P1-03 — Snapshot / Delta 的完整替换、版本连续性和修复协议缺失

- **Severity：** P1
- **File / Section：** `06-memory-context/context-reconciliation.md`（缺失）
- **Evidence：** C P2-05/P2-06；I-09、I-16、I-17。
- **Problem：** 无法确认 Snapshot 是完整替换，Delta 是否精确绑定 from/to version，以及版本跳跃、hash 不匹配和重复投递的处理。
- **Impact：** Adapter 可能将不完整状态当作目标版本，或重放旧 Delta 导致状态回退。
- **Required Correction：** 定义 Snapshot manifest、Delta base/target、hash、原子切换、幂等重放、版本缺口修复与兼容拒绝。
- **Owner：** G 主责语义；H 主责协议封装。
- **Dependency：** INT-P1-01、C P2-05/P2-06。
- **Acceptance Criteria：** 乱序、重复、缺失、损坏、版本跳跃测试均保持单一正确状态；必要时强制 Snapshot repair。

#### G-CTX-P1-04 — Applied Proof 缺少与最终 Inference Request 的强关联

- **Severity：** P1
- **File / Section：** `06-memory-context/context-reconciliation.md`（缺失）；`07-agent-integration/inference-boundary-model.md`
- **Evidence：** INT-P1-05；C 专项审查 P1-06 指出 Adapter 自报 Applied、可选 digest 和最终请求可见性仍不足。
- **Problem：** 无法证明 Context Version、Delivery ID、Capability Epoch、Inference Request ID 和最终提交边界的关联。
- **Impact：** 中间模板插入成功但最终请求覆盖/丢弃时，系统仍可能错误报告 Applied。
- **Required Correction：** 定义 Applied Attestation 与 Full/Partial/Bypassed/Unknown coverage；完整 managed region 必须可证明属于指定最终提交请求。
- **Owner：** G + H；C 负责 Adapter Tier conformance。
- **Dependency：** INT-P1-05、C P1-06。
- **Acceptance Criteria：** 每个 Full Applied 都能关联唯一 Inference Request 与最终 boundary evidence；无法观测最终提交点的 Adapter 不得报告 Full/Boundary Applied。

#### G-CTX-P1-05 — Forget / Retraction / Memory Revision 的 Context 引用失效契约缺失

- **Severity：** P1
- **File / Section：** `06-memory-context/context-reconciliation.md`、`context-architecture.md`（缺失）
- **Evidence：** INT-P0-03、INT-P1-06；B Domain Model 将 Memory Version 定义为不可变历史版本；D/E 设计未提交。
- **Problem：** 无法确认 Memory Revision、Retracted、Superseded、Deleted、Entity Merge/Split 如何使 ContextEntry 变 Stale、失效或重新解析。
- **Impact：** Context 可能长期引用旧 Memory Version，或在 Forget/Entity 变化后错误复活旧内容。
- **Required Correction：** G 消费 Canonical Memory Revision/Forget/Retraction 事件；对引用做版本校验与权限复核；保留历史引用但阻断不再允许使用的版本。
- **Owner：** D/E 定义事件；G 定义 Context 反应；I 定义 Forget/撤销语义。
- **Dependency：** INT-P0-03、INT-P1-06、B DM-002/DM-006/DM-007/DM-011。
- **Acceptance Criteria：** 修订/撤回/删除/合并拆分均能确定性识别 Stale Entry；撤销内容不会被重放重新激活。

#### G-CTX-P1-06 — Retrieval Result 与 Activation Recommendation 的输入信任/完整性门槛未定义

- **Severity：** P1
- **File / Section：** `06-memory-context/context-architecture.md`（缺失）；F 设计目录缺失
- **Evidence：** A/B/C 集成报告要求 Scope-before-candidate；F 专项审查报告标记 Runtime 设计缺失；INT-P0-02。
- **Problem：** 无法确认 G 是否验证 Retrieval Result 的 Scope、Memory Version、Index Watermark、Incomplete Result、activation_reason 和来源。
- **Impact：** 不完整或未授权候选可能进入权威 Context。
- **Required Correction：** F 输出必须带来源、版本、水位、完整性与建议原因；G 在规划/提交前验证授权与水位，必要时拒绝或标记不完整。
- **Owner：** F + G；I 提供授权契约。
- **Dependency：** INT-P0-02、INT-P1-01、C P1-03。
- **Acceptance Criteria：** 未授权候选永不进入 Context；低水位/不完整结果按策略拒绝或显式标记，不能伪装完整。

### P2 — 性能、观测和兼容性

#### G-OPS-P2-01 — Context Budget/Sufficiency 多维指标与压缩语义未验证
- **Severity：** P2
- **File / Section：** `06-memory-context/context-budget-and-sufficiency.md`（缺失）
- **Evidence：** C P2-10；任务书要求多维 Coverage。
- **Problem：** 无法确认预算是否仅以 Top-K/Token 衡量，或是否保留 Evidence、Temporal、Risk、Uncertainty 等覆盖。
- **Impact：** 可能压缩掉关键关系、风险或不确定性，导致上下文虽短但失真。
- **Required Correction：** 采用 Semantic/Entity/Relation/Environment/Temporal/Evidence/Risk/Uncertainty Coverage、Redundancy 与 Compression Cost；压缩形成可追溯新版本。
- **Owner：** G。
- **Dependency：** F Activation、D Provenance、H Adapter Token/Byte 限制。
- **Acceptance Criteria：** 提供代表性任务集、覆盖度评估和压缩前后可追溯测试；无 Benchmark 不承诺固定延迟或准确率。

#### G-OPS-P2-02 — Context Update / Reconciliation 指标与故障诊断链缺失
- **Severity：** P2
- **File / Section：** `06-memory-context/context-reconciliation.md`（缺失）
- **Evidence：** INT-P1-05；C P2-06/P2-12/P2-13。
- **Problem：** 无法回答版本滞后、Delivery Unknown、迟到 ACK、Partial Apply、重试和修复次数。
- **Impact：** 故障无法区分 Brain commit、transport、Adapter application 和 inference boundary 问题。
- **Required Correction：** 建立 context_id、context_version、change_set_id、delivery_id、inference_request_id 的 trace chain；控制 metric cardinality，敏感内容不进入普通日志。
- **Owner：** G + H + Observability。
- **Dependency：** INT-P1-05、C P2-06/P2-12。
- **Acceptance Criteria：** 给定任意 delivery_id 可追溯准备、提交、投递、ACK、Inference Request 和 reconciliation 结果；日志不暴露原始 Memory/Prompt/凭证。

#### G-OPS-P2-03 — Schema/Capability 演进兼容策略未验证
- **Severity：** P2
- **File / Section：** `06-memory-context/context-versioning.md`、`context-reconciliation.md`（缺失）
- **Evidence：** C P2-11；`08-protocols/` 不存在。
- **Problem：** 无法确认 Context Schema、ChangeSet、Snapshot/Delta 与 Adapter Capability Epoch 的兼容规则。
- **Impact：** 新旧 Adapter 可能误读字段或把未知操作静默忽略。
- **Required Correction：** 明确 major/minor、未知字段/操作、能力协商、弃用和升级失败行为。
- **Owner：** G + H。
- **Dependency：** INT-P1-01、C P2-11。
- **Acceptance Criteria：** 兼容矩阵覆盖旧 Brain/新 Adapter、新 Brain/旧 Adapter、未知必需操作和能力 epoch 变化。

#### G-OPS-P2-04 — Rust 状态机、事务与性质测试方案缺失
- **Severity：** P2
- **File / Section：** G 全部设计缺失；后续 Rust Engineering 文档
- **Evidence：** README/ARCHITECTURE_ROADMAP 要求实现前具备状态、事务、恢复与验收规范。
- **Problem：** 当前没有可验证的状态转换表、并发性质或故障注入矩阵。
- **Impact：** 未来实现可能出现状态分叉、重复应用、崩溃窗口和撤权竞态。
- **Required Correction：** G 提供状态机和事务契约；工程阶段补充 property-based tests 与 fault injection。
- **Owner：** G + Engineering + Testing。
- **Dependency：** G-CTX-P1-01 至 P1-05。
- **Acceptance Criteria：** 测试覆盖幂等、版本单调、原子性、scope 隔离、Forget 优先级、迟到 ACK、离线重连和恢复。

### P3 — 文档与维护优化

#### G-DOC-P3-01 — G 的文档索引、状态分类和跨模块引用未提交
- **Severity：** P3
- **File / Section：** `06-memory-context/*`（目录缺失）
- **Evidence：** README 文档地图列出 06，但当前 main 分支未见该目录。
- **Problem：** 缺少 G 文档自身的 DECIDED/CANDIDATE/TO_VALIDATE/OPEN 状态和接口索引。
- **Impact：** 后续会话难以定位权威定义，容易重复定义。
- **Required Correction：** 提交 G 规格、文档索引、决策状态和 INT-* 引用。
- **Owner：** G。
- **Dependency：** G 全部 P1 修复。
- **Acceptance Criteria：** 六份核心文档可读、互相链接、每项关键设计有 Owner/Dependency/Acceptance Criteria。

---

## 13. INT-* 状态矩阵

状态定义：PASS = 有足够文档证据满足；PARTIAL = 原则存在但执行契约未闭合；FAIL = 有明确冲突/缺失导致门槛不满足；NOT APPLICABLE = 不适用。本报告将“关键 G 文件缺失导致无法证明”记为 FAIL 或 PARTIAL，不把证据缺失误写成实现漏洞。

| ID | 状态 | 证据与判断 | Owner / 下一步 |
|---|---|---|---|
| INT-P0-02 | PARTIAL | B Scope 模型和系统原则存在；G 的 Context/Entry/Delivery/Cache 全链路授权未提交 | I 主责，G/H/D/F 协作 |
| INT-P0-03 | FAIL | G Forget/Reconciliation 文件缺失，无法证明 Context/Adapter 副本阻断与清理传播 | I + G + H；D/E 提供事件 |
| INT-P0-04 | PARTIAL | I-12/P-11 与 C 边界原则存在；G Editor 与 managed region 强制约束未验证 | I + G + H |
| INT-P1-01 | FAIL | G Context Version/ChangeSet 规格缺失 | G + H + C |
| INT-P1-02 | PARTIAL | B 定义 Memory Version/Claim 语义；G 引用和 Stale 处理未验证 | B/D + G |
| INT-P1-03 | PARTIAL | C 身份/Scope 问题已指出；G Context Scope 绑定缺失 | B/C/H/I + G |
| INT-P1-04 | NOT APPLICABLE（G 仅消费） | Accepted 耐久性由 E/H/Consistency 主责；G 应消费已接受且可信的输入，不拥有 Telemetry Accepted 事务 | E/H/I；G 定义输入门槛 |
| INT-P1-05 | FAIL | G Applied Attestation/Reconciliation 缺失；C 明确指出最终请求证明仍待 G/H | G + H + C |
| INT-P1-06 | FAIL | G Forget/Retraction/Stale 引用对账缺失；E/D/I 事件依赖也未齐 | D/E/G/I |
| A: AR-001 | PARTIAL | A/B/C 集成报告明确 Forget 全链路门槛；G 清理传播未验证 | I + G/H |
| A: AR-002 | PARTIAL | Memory Injection 残余风险已识别；G Editor/Context Render 防护未验证 | I + G/H |
| A: AR-003 | PARTIAL | Scope-before-candidate 基线存在；G Context/Cache 再授权未验证 | I + G/F |
| A: AR-005 | PARTIAL | Applied 必须关联请求边界原则已明确；G/H 完整证明缺失 | G/H/C |
| B: DM-002 | PARTIAL | B 定义 Memory Version；Context Version 独立权威由 G 负责但缺失 | B + G |
| B: DM-006 | PARTIAL | Provenance 语义存在；G 是否保留 source_refs/evidence 展开关系未验证 | B/D/E + G |
| B: DM-007 | PARTIAL | Lifecycle/引用语义有基线；G 对 Superseded/Retraction 反应未验证 | B/D + G |
| B: DM-010 | PARTIAL | Scope/Permission 模型存在；G 层每阶段授权未验证 | B + I + G |
| B: DM-011 | FAIL | Forget 依赖图和副本清理语义尚未闭合，G 侧缺失 | B + I + G/H |
| C: P1-03 | PARTIAL | C 指出身份/Scope 绑定缺口；G 的 Context Scope 不可核验 | C + H + I + G |
| C: P1-06 | FAIL | Applied 最终请求证明仍待 G/H，G 文件缺失 | G + H + C |
| C: P1-07 | PARTIAL | C 指出撤权/离线缓存问题；G Reconciliation 缺失 | I + H + G |
| C: P2-05 | FAIL | Snapshot/Delta 原子性明确要求 G 定义，G 文件缺失 | G + H |
| C: P2-06 | FAIL | Timeout/迟到 ACK 的查询和对账模型无 G 证据 | G + H |
| C: P2-07 | PARTIAL | Memory injection 原则存在，G 端结构化 managed region/Trust 保留未验证 | I + H + G |
| C: P2-10 | FAIL | Context budget/压缩语义由 G 主责但文档缺失 | G + H |
| C: P2-12 | PARTIAL | C 的 correlation 字段存在，G/H 端到端链缺失 | G + H + Observability |

---

## 14. 与 D/E/F/H/I 的接口冲突和依赖

### 对 D — Memory Brain

- ContextEntry 必须引用 Canonical Memory ID + Memory Version，不得复制或拥有 Canonical Memory。
- Memory Version 与 Context Version 分离。
- Memory Revision、Superseded、Retracted、Deleted、Entity Merge/Split 应产生可消费的失效/重解析信号。
- G 不得通过 Context Remove 修改 Canonical Memory Lifecycle。
- D 设计目录在本次 main 分支缺失，无法核验 D 的实际事件和引用契约。

### 对 E — Memory Compiler

- Canonical Memory Revision、Forget、Retraction、Provenance 更新需要通过可靠事件/变更流通知 G。
- Compiler Accepted 不等于 Canonical Memory 已形成，更不等于 Context 可引用。
- Evidence/Provenance/source_refs 必须可被 Context 保留和按权限展开。
- E 设计目录与 E 专项审查报告本次未见，全部标记未验证。

### 对 F — Memory Runtime

- Retrieval Result 是候选，不是 ContextEntry。
- Activation Recommendation 应包含 activation_reason、相关性/风险/时效信息。
- Incomplete Result、低 Index Watermark 或授权不完整不能伪装成完整候选。
- F 不得直接修改 G 的 Context Version。
- F 设计目录缺失；F 专项审查已记录审查受阻，故不能证明 Retrieval/Activation 输出契约成立。

### 对 H — BMCP / Adapter

- G 定义 Context 内部语义、Version、ChangeSet、Snapshot/Delta 原子性与 reconciliation 目标状态。
- H 定义 wire message、能力协商、传输重试和 Adapter 侧执行接口。
- Applied 必须关联 Delivery ID、Context Version、Capability Epoch、Inference Request ID 和最终 boundary。
- Adapter 应返回 Full/Partial/Rejected/Unknown 等可区分结果。
- Adapter 自报 Applied 不得被直接当作完整证明。
- 当前 Agent Integration 文档有原则；`08-protocols/` 缺失，BMCP 最终 wire contract 未验证。

### 对 I — Security / Governance

- I 拥有授权、撤销、Forget、保留和审计治理语义；G 消费这些决策并负责 Context 域的阻断与副本传播。
- Revoke/Forget 必须在提交、Delivery、Apply、Reconnect 阶段检查。
- Offline Adapter 未重新验证撤销 epoch 前，不得恢复旧 Context。
- 清理状态必须区分 Requested、Blocked、Pending、Acknowledged、Confirmed、Failed、Unknown。
- 本次未取得 I 的专项设计，不能假定治理执行闭环已成立。

### 接口冲突总判断

当前主要问题不是已证明 D/E/F/H/I 与 G 的设计发生具体字段冲突，而是 G、D、E、F、H、I 的契约缺失导致**无法证明不存在冲突**。不得把“架构原则一致”写成“跨模块接口已冻结”。

---

## 15. DECIDED / CANDIDATE / TO_VALIDATE / OPEN

### DECIDED（由现有治理/系统基线支持）

1. Brain 是其管理的 Memory Context 的逻辑权威。
2. Adapter 是执行者，不拥有 Brain 的记忆规则。
3. Canonical Memory、Memory Context、Applied Context 分层。
4. Context Remove 不等于 Forget。
5. Context 修改在未来 inference assembly boundary 生效。
6. 不覆盖 System/Developer/User 原始区域及 Agent 安全策略。
7. Memory 内容不获得指令权力或工具授权。
8. Context Version 与 Memory Version 分离。
9. Context Version 必须有唯一权威序列。
10. Adapter ACK 不证明模型理解或使用。

### CANDIDATE（建议 G 提交后评审，不在本轮视为已决策）

1. 每个 context_id 使用单一串行提交队列，或使用 CAS 乐观并发；可按负载验证后选择。
2. ChangeSet 默认 all-or-nothing。
3. Snapshot 作为完整替换恢复基线，Delta 作为连续版本间增量。
4. Delivery 与 Context Version 分开建模，Adapter Applied 状态作为投影/证明记录。
5. Applied Coverage 采用 Full/Partial/Bypassed/Unknown/Rejected 分类。
6. Forget/Revocation 先阻断，再异步清理，并保留无法物理确认的 Unknown。

### TO_VALIDATE

1. Context Snapshot/Delta 的最优阈值与构建成本。
2. 高并发 Context 的 CAS 冲突率与串行化吞吐。
3. Context Sufficiency 多维评分与 Agent 任务成功率之间的关系。
4. Compact 对 Evidence Coverage、Temporal Validity 和 Uncertainty Coverage 的影响。
5. Reconciliation 扫描成本、重试上限和离线 Adapter 恢复时间。
6. Applied Attestation 的 digest 规范化与隐私/可观测性折衷。
7. 代表性 Agent 工作负载上的 Token/Byte/Latency 预算。

### OPEN

1. Context Version 的持久化形式：不可变完整快照、事件日志投影或混合方案。
2. CAS 与 per-context serialization 的选型及冲突重算策略。
3. ChangeSet 的操作排序、冲突规则与可组合性。
4. Snapshot/Delta 的 schema compatibility 和跨 capability epoch 规则。
5. Adapter 最终请求边界证据的最小可信实现。
6. Offline Adapter 对 Forget 的最大可保证范围及超期失效策略。
7. 多 Agent/Task/Environment Context 的继承、共享与隔离规则。

---

## 16. 修复顺序、退出条件和审查局限

### 16.1 修复顺序

| 顺序 | 工作 | Owner | 依赖 |
|---|---|---|---|
| 0 | 提交 G 六份核心设计文件并补齐目录索引 | G | 无 |
| 1 | 冻结 Context Scope/Identity/Permission 与 Revocation 检查点 | G + I + H | INT-P0-02 |
| 2 | 冻结 Context Version / ChangeSet / CAS / Idempotency | G | INT-P1-01 |
| 3 | 冻结 Snapshot/Delta 原子应用和局部失败语义 | G + H | INT-P1-01、C P2-05 |
| 4 | 冻结 Applied Attestation 与最终 Inference Request 证明 | G + H + C | INT-P1-05 |
| 5 | 冻结 Forget/Retraction/Revision/Reconciliation 传播 | D + E + G + H + I | INT-P0-03、INT-P1-06 |
| 6 | 冻结三状态机、重放、迟到 ACK、未知状态处理 | G + H | 上述契约 |
| 7 | 完成 Budget/Sufficiency/Compact 和指标设计 | G + F + H | P2 |
| 8 | 建立性质测试、并发测试、故障注入和 Adapter conformance suite | G + H + I + Testing | 契约冻结后 |

### 16.2 G Review 退出条件

只有同时满足以下条件，才可将本次 FAIL 重新审查为 Conditional Pass/Pass：

- 六份 G 核心文档已提交，且相互引用一致。
- Context Version 有唯一权威分配者，Memory Version/Delivery ID/Inference Request ID 明确分离。
- ChangeSet 具备 Base Version、Target Version、幂等键、提交身份和原子操作语义。
- Snapshot/Delta 有完整替换、原子应用、局部失败、重复应用、版本跳跃和恢复语义。
- Context Lifecycle、Delivery Lifecycle、ContextEntry Lifecycle 三个状态机独立。
- Scope Isolation、Permission Revocation、Forget 传播覆盖 Context 与 Adapter 管理副本。
- Applied 关联最终 inference request boundary；无法证明的结果为 Partial/Unknown。
- D/E/F/H/I 能消费 G 的稳定契约，跨模块问题有 Owner 和 Acceptance Criteria。
- 不存在覆盖 System/Developer/User 或 Agent 安全策略的操作路径。
- 性能数字只在有可复现实测后提出。

### 16.3 审查局限

1. 本次审查基于 GitHub `main` 分支可读取内容；未检查其他分支或未提交工作区。
2. G 核心目录缺失，故本报告无法对 G 内部文档作逐段内容审查；文件缺失本身是审查阻断证据。
3. D/E/F 的设计材料并未完整出现在本次可见仓库中；D/F 专项审查报告记录其设计缺失，E 设计/审查材料未见。
4. H 的 Agent Integration 文档可读，但 BMCP `08-protocols/` 未见；不能把 Adapter 原则视为最终 wire contract。
5. I Security/Governance 设计未取得；治理原则不能替代可执行的撤权与清理协议。
6. 未运行 Rust 代码、数据库、Adapter 或 Inference Runtime。
7. 未执行真实并发、崩溃恢复、离线重连、Forget 物理清理、Prompt Injection 或性能测试。
8. 三方结论是专业视角模拟，不代表三名真实人员或三个模型的独立签署。

### 16.4 最终决议

**Session G：FAIL — Review Blocked by Missing Design Deliverables。**

本轮确认了正确的总体架构基线，但不能证明 Memory Brain 已经通过 G 实际拥有并管理一个具备唯一权威版本、原子变更、完整 Applied Proof 和 Forget/Reconciliation 能力的记忆上下文区域。

**不得将 G 标记为 Pass，不得冻结 Context Version / ChangeSet / Snapshot-Delta / Applied wire contract，不得据此直接进入实现。**

本报告只创建于 `reviews/06-memory-context/three-party-six-dimension-review.md`；未修改 README、路线图、治理、系统架构、领域模型、D/E/F/H/I 或其他审查文件。
