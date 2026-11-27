---
document_metadata:
  domain: memory-compiler
  role: design-specification
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
      last_verification_note: "从 Owner 源分支逐字节恢复；Owner 接受仍待定。"
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
    canonical_status: Canonical
    canonical_scope: "E 域 Memory Compiler 记录 phase-3.6.2-jf10-cross-authority-recovery-protocol.md；规范归属位置待 Owner 接受后确定。"
    canonical_scope_id: "memory-compiler/e-phase-3-6-2-jf10-cross-authority-recovery-protocol"
    canonical_scope_keywords:
      - memory-compiler
      - e-domain
      - phase-3-6-2-jf10-cross-authority-recovery-protocol
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---




# 第 3.6.2 阶段 —— JF-10 跨权威提交恢复协议

- 状态：**DE-S 工程提案 / 候选（CANDIDATE）**
- 决策权限：D、E 与 Storage 可各自定义其所有者侧的消费与恢复行为；I 单独拥有策略域排序器与 `CommitAuthorizationReceipt` 语义。
- 批准：**需要 I 接受；本提案不暗示任何 I 批准。**
- 实现：**未实现（NOT IMPLEMENTED）**
- 一致性：**未运行（NOT RUN）**
- 结论：**在 I 接受该接口且协议通过崩溃/恢复测试之前，JF-10 P0 保持 OPEN。**

## 1. 问题与安全目标

JF-10 覆盖两个对调用方不可区分的失败窗口：
1. I 已把某个授权决策持久排序为 `COMMIT_WON`，随后 Storage 在 `VisibilityPointer` 与 `PublicationReceipt` 持久提交之前崩溃。
2. Storage 已提交可见性，但 I 的响应/确认或调用方的确认丢失。

超时、响应缺失、副本行不存在或进程重启，都不构成已提交或未提交的证据。协议必须在保证字节在 Storage 可见性事务提交之前保持私有的同时，保留 I 的撤销顺序与 D 的栅栏顺序。

## 2. 规范权限边界

- **I** 是签发方/主体/参与者授权、PermissionEpoch、撤销顺序与持久终态排序器结果的权威。
- **D** 是 ForgetFence、已捕获工作/屏障状态、依赖完整性与 D 侧发布谓词的权威。
- **E** 是生产者执行状态与冻结输出/血缘清单输入的权威；它不能声明制品已 Published。
- **Storage** 是持久 `VisibilityPointer`、`PublicationReceipt`、所有者提交游标与读者可见发布状态的权威。
- `VisibilityPointer` 仍是唯一的发布权威。暂存对象存在、outbox 投递、仅有 I 授权与 E 本地状态，都不使字节可见。

## 3. 稳定操作身份与不可变绑定

在联系 I 之前，Storage 必须在拥有可见性指针的同一个 Canonical Memory Authority 数据库中持久化所有者侧发布意图。该意图包含：
- 跨重试与恢复保持稳定的 `PublicationOperationId` / 幂等键；
- 覆盖完整不可变请求的规范 `RequestDigest`；
- `CommitAuthorizationReceipt` 引用或精确的 I 请求绑定；
- 策略域、PermissionEpoch、PrincipalRef、ActorRef、动作、ResourceRef、目的、受众、ScopeBindingSet 摘要、EnvironmentRef 与 DelegationChainRef；
- ForgetOperationId、栅栏代号/高水位、WorkItemId、AttemptId、LeaseEpoch、ProducerRef；
- DependencySetDigest、OutputManifestVersion/摘要、ProducerDomainInventoryEpoch 与（要求时的）InventorySealReceipt 摘要；
- 所有者权威、预期可见性操作与创建/决策元数据。

同操作 ID + 同摘要即为幂等重放。同操作 ID + 不同摘要为硬冲突，必须拒绝/审计。不得铸造新操作 ID 来规避未解决的结果。

## 4. 提交协议

### 阶段 A —— 所有者准备（不可见）

1. E 提交完整的冻结清单与依赖证据；D 校验当前栅栏/屏障谓词。
2. Storage 校验全部所有者本地谓词，并持久插入 `PublicationIntent(PREPARED_FOR_I)`，对操作 ID 与不可变请求摘要施加唯一约束。
3. 不写入 `VisibilityPointer`。制品字节留在私有暂存中。
4. 若准备确认丢失，Storage 通过其权威决策屏障以同一操作 ID 与摘要求解。在解决之前，结果为 `UNKNOWN`，而不是 `NOT_COMMITTED`。

### 阶段 B —— I 排序器决策（持久且按撤销排序）

5. Storage 使用同一操作 ID 与摘要，以及绑定到精确受保护操作元组的、一次性不可转让的 `CommitAuthorizationReceipt`，请求 I 决策。
6. I 必须在策略域内把该决策与撤销原子串行化，并持久记录一个终态结果：`COMMIT_WON`、`REVOCATION_WON` 或 `INDETERMINATE_ABORTED`。
7. I 必须提供按操作 ID + 摘要的权威、已认证查询。重复同一请求返回同一持久终态结果；不同摘要构成冲突。丢失的 I ACK 通过查询/重放解决，绝不通过创建新操作解决。
8. `COMMIT_WON` 仅是授权顺序结果；它本身不是发布，也不是读者可见。`REVOCATION_WON` 与 `INDETERMINATE_ABORTED` 禁止可见性。I 状态未知/不可用时，操作保持待定且私有。

### 阶段 C —— 所有者可见性提交（单个本地原子事务）

9. 在验证持久 I `COMMIT_WON` 结果与回执绑定之后，Storage 在实际所有者提交边界处重新检查 D 栅栏/屏障、WorkItem/Attempt/Lease 栅栏、依赖摘要、冻结清单版本/摘要、要求时的清单封存新鲜度，以及全部所有者本地不变量。
10. 在 Canonical Memory Authority 数据库的一个事务中，Storage 必须原子地：
   - 对精确的期望可见性代号与所有者提交游标做比较并设置（CAS）；
   - 写入/更新 `VisibilityPointer`；
   - 写入不可变 `PublicationReceipt`，包含 I 决策/回执引用、I 排序器位置、精确请求摘要、D 栅栏代号、清单/依赖摘要与所有者提交游标；
   - 把该操作记录为 `OWNER_COMMITTED`，并记录终态所有者结果；
   - 为该操作记录幂等回执消费；并且
   - 追加同一事务的 outbox 事件。
11. 指针、回执、结果与 outbox 要么全部提交，要么全部回滚。Outbox 投递仅为通知/对账，绝不是可见性权威。
12. 只有该事务提交之后，Storage 才可返回 `PUBLISHED`；E 随后可用持久 Storage 回执记录其终态 Published 状态。若 D 栅栏或任何所有者谓词胜出，Storage 记录不可见的终态拒绝/中止，且不发布任何指针。

## 5. 恢复与确认丢失规则

| 持久 I 结果 | 持久 Storage 结果 | 恢复动作 |
|---|---|---|
| `COMMIT_WON` | `OWNER_COMMITTED`，摘要与回执匹配 | 返回同一发布回执；不重新发布、不铸造新 ID |
| `COMMIT_WON` | 已准备意图，无所有者提交 | 在重检 D 栅栏与全部所有者谓词之后，以同一操作 ID/摘要重跑阶段 C |
| `REVOCATION_WON` | 无所有者提交 | 标记为拒绝/中止；字节保持私有；不得以新键重试 |
| `INDETERMINATE_ABORTED` | 无所有者提交 | 按 I 终态证据标记为中止/不可见；保留审计 |
| I 结果未知/不可用 | 无所有者提交 | 保持 `OUTCOME_UNKNOWN`；字节保持私有；仅以同一键查询/重放 |
| 任意 I 结果 | Storage 结果未知 | 使用 Storage 的权威决策屏障；不得从缺失行或陈旧副本推断 |
| Storage 称已提交，但 I 回执/绑定无法验证 | 任意 | 隔离/失败关闭；绝不基于 Storage 行单独暴露 |

恢复 worker 必须幂等且受栅栏约束。它们不得绕过当前 D 谓词、复用过期租约、变更冻结清单、接受已变更摘要，或把未知状态变为成功。恢复必须在服务读者之前，对账控制账本、I 终态决策与所有者提交游标。

## 6. 必需的 I 接口接受

I 必须在 I 拥有的制品中显式接受或替换以下语义：
1. 以稳定操作 ID + 请求摘要为键的持久终态决策；
2. 已认证的权威查询/重放，对同一绑定返回同一终态结果；
3. 同 ID 不同摘要的硬冲突；
4. 把 `COMMIT_WON` 作为排序器顺序事实不可撤销地保留，并提供足以支撑所有者崩溃恢复的、有文档记录的保留/恢复保证；
5. 一次性 `CommitAuthorizationReceipt`、其消费记录与终态排序器决策之间的精确关系；
6. I 在决策持久之前/之后崩溃、响应丢失、副本滞后、恢复与排序器故障切换时的定义行为；
7. 确认 `COMMIT_WON` 意味着授权相对撤销胜出，而不是 Storage 可见性已提交。

若 I 无法保证持久终态查询与前向恢复，本协议不充分；需要形式化规定的、带参与者恢复的持久分布式事务/2PC 协议。DE-S 不得静默用缓存、租约、陈旧 epoch 或本地 ALLOW 替代。

## 7. DE-S 接受与实现证据

- **D：** 确认栅栏/屏障状态被重新检查并与所有者可见性提交串行化的精确点；定义当 I 说 `COMMIT_WON` 但 D 栅栏在指针提交之前胜出时，所有者侧的终态处置。
- **E：** 持久化稳定操作 ID/摘要，并在匹配的 Storage `PublicationReceipt` 持久确认之前保持非终态；绝不单凭 I `COMMIT_WON` 报告 Published。
- **Storage：** 实现持久意图、唯一幂等约束、权威结果查询/屏障、原子指针+回执+outbox 事务、恢复 worker 与恢复对账。
- **全部：** 分别保留 I 授权顺序、D Forget 栅栏顺序与 Storage 可见性提交游标；不得合并其权威或水位。

## 8. 拟议的 JF-10 一致性用例（新提案；未执行）

| 用例 | 注入的失败/竞争 | 必需结果 |
|---|---|---|
| JF10-01 | I 记录 `COMMIT_WON`；Storage 在可见性事务之前崩溃 | 同键恢复仅在重检 D/所有者谓词之后完成；无重复指针/回执 |
| JF10-02 | 持久 `COMMIT_WON` 之后 I 决策响应丢失 | 查询返回同一决策；不产生新操作 ID |
| JF10-03 | Storage 事务提交指针+回执；调用方 ACK 丢失 | 同键查询返回完全相同的回执；恰好一次可见发布 |
| JF10-04 | I 撤销与排序器决策竞争 | 恰好一个持久 I 终态顺序；未胜出的授权不能发布 |
| JF10-05 | D ForgetFence 在 I `COMMIT_WON` 之后、所有者可见性提交之前安装 | D 栅栏谓词在所有者提交处胜出；无指针；终态不可见处置 |
| JF10-06 | 同操作 ID 以不同摘要重放 | 硬冲突；无可见性 |
| JF10-07 | 恢复期间 I 或 Storage 副本陈旧/不可用 | UNKNOWN/PENDING；无可见性，也不得出虚假的 NOT_COMMITTED |
| JF10-08 | I 决策之后、Storage 可见性提交之前发生恢复 | 对账 I 决策 + 所有者账本/游标；完成或保持阻塞，且不产生不安全可见性 |

每个已执行用例都必须保留构建 SHA、数据库/运行时版本、确定性夹具/种子、故障注入点、I 决策证据、Storage 事务/锁/CAS 轨迹、D 栅栏游标、PublicationReceipt ID/摘要、实际结果与独立评审人签核。本表规定测试；它不是测试已运行的证据。

## 9. 决策与不作声明

本文档是供 I 审阅的 DE-S 候选协议。它不关闭 JF-10、不批准 I 治理、不确立消费者接受、不选定具体数据库供应商、不证明实现，也不通过任何测试。在 I 接受所需排序器语义并存在可执行崩溃/恢复证据之前，JF-10 保持 **P0 OPEN**，最终发布在结果未知时保持失败关闭，且第 3.6 阶段无法通过最终门。


---

# 附录 —— 对照 I36-SR-02 owner-gate 排序的对账（JF-10 P0）

- 新增：2026-11-16
- 状态：**已识别实质性协议缺口 —— 需要 I 决策**
- 适用于上述候选协议；它不会静默替换或重新解释更早的阶段。

## A. 新确认的 I 要求

当前 I 拥有的联合信任策略（Blob `0cbf6bb7480db873790c454817593a9b1c5548ba`）§10.2 要求：

1. 每个策略域一个逻辑 I 权威与可线性化排序器；
2. 绑定到完整授权元组、操作 ID/摘要与所有者边界的单次使用 `CommitAuthorizationReceipt`；
3. 操作所有者的最终提交/披露门参与**同一按域提交排序协议**；
4. 所有者操作提交相对撤销的原子排序，产出 `COMMIT_WON`、`REVOCATION_WON` 或 `INDETERMINATE_ABORTED`。

该回执不是可转让许可或离线租约。I 的 §10.2 同时声明实现证据为 NOT VERIFIED。

## B. 当前 JF-10 候选的缺口

既有候选的阶段 B 把 I `COMMIT_WON` 作为授权顺序结果持久记录，随后阶段 C 独立提交 Storage 的 VisibilityPointer + PublicationReceipt 事务。

这种分阶段序列对幂等与前向恢复有用，但**候选尚未证明 Storage 的最终所有者提交参与同一 I 策略域排序协议**。先前的一次 I 决策随后由独立的 Storage 事务跟随，不能仅因 Storage 在其本地事务中存有回执 ID 与排序器位置，就被假定满足 I36-SR-02。

同样，一行本地单次使用回执消费记录，本身不能证明回执消费与所有者提交已相对 I 排序器中的并发撤销原子排序。

因此：
- JF-10 候选 v1 **尚未证明符合** I36-SR-02；
- 不主张既有阶段 B/阶段 C 拆分已被 I 接受；
- JF-10 仍为 P0 OPEN，且在结果未知/不确定时发布保持失败关闭。

## C. 协议冻结前需要 I Owner 决策

I 必须发布一项 I 拥有的规范协议决策，至少定义：

1. **排序参与者：** Storage 所有者门如何加入与撤销相同的按策略域排序器顺序。指明协议参与者与精确线性化点。
2. **回执语义：** `CommitAuthorizationReceipt` 是准备/授权令牌、提交顺序预留，还是其他原语；精确说明何时、由谁消费，以及消费如何绑定到终态所有者结果。
3. **原子结果：** 协议如何保证撤销与 Storage 可见性提交不能同时胜出，包括每个终态结果的精确含义。
4. **崩溃矩阵：** I 在记录顺序之前/之后崩溃、Storage 在本地持久提交之前/之后崩溃、任一响应丢失、参与者重启、副本滞后或故障切换/恢复时的行为。
5. **恢复权威：** 哪个权威回答全局操作结果的已认证查询，需要哪些持久记录，以及恢复如何在不铸造新操作 ID 的情况下继续。
6. **活性与安全性：** 协议使用排序器介导的参与者协议、带恢复的持久准备/提交、2PC 还是其他形式化机制。若分区期间无法推进，明确保留安全性并规定阻塞状态；不得暗示可用性。
7. **证据：** 必需的 I 排序器日志、Storage 事务证明、参与者恢复日志、回执消费证明与故障注入用例。

DE-S 不选择这一 I 拥有的跨权威排序机制，也不宣布 2PC 为强制。I 必须接受某个具体协议、以 I 拥有的规范设计修订，或阻塞并指明可问责所有者与缺失证明。

## D. 过渡期 DE-S 安全规则

在 I 发布并接受 owner-gate 参与协议之前：
- 单独的先前 `COMMIT_WON` 响应不足以作为使 Storage 数据可见的证据；
- 最终 Storage 门必须失败关闭，除非它能证明 I 批准的排序协议已针对精确操作 ID/摘要与所有者边界完成；
- 回执/结果缺失、陈旧、重放、不匹配或不确定，都使暂存数据保持私有；
- D ForgetFence 仍是独立的所有者本地排序检查；
- 不得铸造新操作 ID 以规避未知的先前结果。

## E. 状态

本附录是 DE-S 缺口报告与对 I 决策的正式请求，不是 I 政策修订或接受。原始候选为可追溯性而保留。**JF-10 P0 OPEN；I36-SR-02 运行时未核实；无跨权威原子性证明；无第 3.6 阶段最终门。**


# 附录 v2 —— 参与 Owner-Gate 的持久 2PC 协议（JF-10）

- 状态：**DE-S 修订架构提案 / 可供精确 I Owner 审阅；未被 I 接受；未实现；未测试**
- 取代：JF-10 候选 v1 中阶段 B/阶段 C 拆分的解释。更早的 I 回执绑定、不可变操作身份、权威查询、重放/冲突与终态结果要求继续有效。
- 这是 D/E/Storage 所有者侧提案。它不修订 I 政策，也不主张 I 批准。

## A. 决策

对受保护发布采用**与 I 策略域排序器集成的持久两阶段提交（2PC）参与者协议**。拒绝"独立的 I 授权决策 + 无关的 Storage 事务"。实际的 Storage 最终可见性门把精确的所有者操作（含持久的已准备 Storage 参与者）提交到与撤销相同的 I 排序协议中。

部署画像分两层：

1. 在一个 Canonical Memory Authority 内，D 的 Forget/生产者/依赖账本与 Storage 的发布/可见性记录共享同一个事务数据库与同一个按权威可串行化协调器。
2. 在 I 策略域与该所有者数据库之间，I 排序器是受保护最终所有者门操作的持久排序/2PC 协调器。Storage 数据库是可恢复的已准备参与者。不允许尽力而为的协调器或异步授权令牌。

这是为满足 I36-SR-02、同时保留 D 独立栅栏权威与 Storage 唯一可见性权威而提议的最小协议。它是协议选择，不是具体供应商/版本/部署的批准。

## B. 参与者与权限

| 参与者 | 权限与持久记录 | 必需角色 |
|---|---|---|
| I 策略域排序器/协调器 | CommitAuthorizationReceipt、PermissionEpoch、撤销顺序、持久事务决策与参与者/XID 登记册 | 把精确的所有者最终门操作相对撤销排序；记录 COMMIT/ABORT 决策；驱动参与者恢复 |
| Canonical Authority DB（D + Storage） | D ForgetFence、ProducerClass/WorkItem/Dependency 账本、Storage PublicationIntent、已准备 XID、VisibilityPointer、PublicationReceipt、所有者结果、回执消费记录与 outbox | 校验/锁定 D 与所有者谓词；准备精确可见性事务；仅按 I 的持久协调器决策提交/回滚 |
| E Compiler | WorkItem/Attempt/Lease 生命周期、冻结输出清单、暂存字节、血缘与发布请求 | 调用最终门；在权威 Storage 回执确认提交之前保持非终态 |
| D Forget 权威 | 规范 ForgetOperation、栅栏代号、按权威登记高水位、依赖/屏障证明 | 把栅栏安装相对已准备发布串行化；绝不把 I 授权视为栅栏覆盖 |
| I 清单登记册 | ProducerDomainInventoryEpoch、InventorySealReceipt 与全局目标目录 | 提供封闭世界生产者/接收方覆盖；与 D 工作高水位保持分离 |

## C. JF-10 v2 协议

### C1. 不可变操作身份

在任何 I 排序器调用之前，Storage 持久分配一个稳定 PublicationOperationId 与规范 RequestDigest。摘要绑定完整的不可变操作：精确制品/版本与载荷摘要；WorkItemId、AttemptId 与 LeaseEpoch；ProducerClass/ProducerIdentity 绑定；源与传递血缘；ScopeRefs；DependencySetDigest；冻结 OutputManifestVersion/摘要；D ForgetOperationId、适用栅栏代号与目标摘要；当前 I 清单 epoch/seal 引用；policy_domain_id、PermissionEpoch、PrincipalRef、ActorRef、动作、ResourceRef、目的、受众、ScopeBindingSet 摘要、EnvironmentRef、DelegationChainRef；精确 owner_boundary；以及 CommitAuthorizationReceipt/决策绑定。

同 ID + 同摘要即为同一操作的查询/重放。同 ID + 不同摘要或已变更的安全绑定元组为硬冲突。任何重试都不得铸造新 ID 以规避未知结果。

### C2. 阶段 0 —— 准备资格

E 必须在入队、租约、源解引用或执行之前拥有持久 D RegistrationReceipt。E 冻结其完整输出清单与血缘。D 确认依赖登记完整。Storage 确认适用的 I InventorySealReceipt 真实、新鲜，并绑定到 I 策略要求的精确清单 epoch/摘要。这些是前置条件，不是发布许可。

候选字节留在私有暂存中。对象存储列举、路径知识、带签名的暂存 URL、队列状态、outbox 投递与 E 本地状态都不能使制品可见。

### C3. 阶段 1 —— Storage 参与者准备与 D 栅栏串行化

实际的 Storage 最终门在 Canonical Authority DB 中开启可串行化事务，并准备精确的可见性事务。它必须：

1. 幂等解析 PublicationOperationId + RequestDigest。
2. 锁定按权威协调器以及所有受影响的 目标/血缘栅栏行、ProducerWork/Attempt/Lease 行、依赖集合与冻结清单版本、清单封存引用与期望 VisibilityPointer 代号。
3. 校验每个源祖先与目标的最新 D 栅栏；校验 WorkItem/Attempt/Lease 栅栏；校验完整不可变依赖/清单；校验当前 I 封存引用与全部所有者本地谓词。
4. 校验精确的 CommitAuthorizationReceipt 绑定，但不把回执本身解释为排序器决策。
5. 持久化已准备参与者/XID 与参与者摘要。数据库的已准备状态在进程重启与协调器不可用期间保留串行化锁。不暴露任何 VisibilityPointer 或 PublicationReceipt；字节保持私有。

D 的 InstallForgetFence、RegisterProducerWork 与 RegisterDerivedDependency 使用相同的按权威串行化行/键。若栅栏/登记/依赖事务先行胜出，准备看到该已提交状态，并要么拒绝，要么绑定该精确合格状态。若发布参与者先行准备，冲突的 D 操作在 I 解决提交或中止之前无法通过所持串行化锁。因此 D 栅栏与发布恰好一个顺序；锁超时或参与者不确定即 UNKNOWN，绝不是许可。

若所选数据库无法在崩溃/重启之间持久保留已准备状态与锁，则本协议在该数据库画像上不可实现，部署被阻塞；需要形式化等效的持久参与者协议。

### C4. 阶段 2 —— I 排序器为实际所有者最终门排序

Storage 把已准备参与者令牌、PublicationOperationId、RequestDigest、精确 owner_boundary、回执与参与者身份提交给 I 排序器的 **owner-final-gate 操作**。这不是独立的预检授权调用。

I 在策略域内把该精确操作相对撤销原子排序，并持久记录一个协调器决策：

- COMMIT：精确的所有者最终门操作被排序在冲突撤销之前。I 终态结果为 COMMIT_WON，包含排序器位置、回执/决策绑定、不可变摘要与持久 Storage 参与者/XID 身份。
- ABORT：撤销被排在前面，或该操作被拒绝。终态结果为 REVOCATION_WON 或 INDETERMINATE_ABORTED，按 I 的定义。不允许任何可见性。
- UNKNOWN/IN_DOUBT：尚未可恢复地确立终态决策。任何参与者都不得推断提交或中止；制品保持私有，受影响排序保持阻塞，等待协调器恢复。

I 不得为一个与已准备所有者参与者脱钩的独立授权检查记录 COMMIT_WON。协调器决策与参与者身份必须持久且可恢复。撤销不能通过假定中止而越过未解决的更早最终门操作；它必须取得协调器的持久决策或保持待定。这是对存疑事务"安全优先于可用性"的规则。

### C5. 阶段 3 —— 参与者完成与可见性

在持久 I COMMIT 之后，Storage 参与者恢复 worker 提交精确的已准备数据库事务。在该单个本地事务中，它原子写入 VisibilityPointer、不可变 PublicationReceipt、所有者终态结果、幂等回执消费证据与同一事务的 outbox 事件。它记录 I 协调器决策 ID/位置、回执 ID、RequestDigest、参与者/XID、D 栅栏代号、依赖与清单摘要、清单 epoch/seal、所有者提交游标与可见性代号。

只有在该参与者提交被权威回读之后，Storage 才可返回 PUBLISHED，E 才可把工作终结为 Published。仅 I COMMIT_WON 不是发布成功。

在持久 I ABORT 之后，参与者回滚；制品保持私有，且只有在参与者中止被持久确认之后，该操作才成为未发布。D 的锁/预留仅在参与者解决之后释放。Outbox 投递是至少一次的通知/对账，绝不是可见性权威。

### C6. D 栅栏交互

D 栅栏安装与 Storage 已准备参与者共享同一 Canonical Authority DB 串行化域与目标/血缘锁：

- 栅栏提交先于参与者准备：准备观测到栅栏，并拒绝/隔离该派生品。
- 参与者准备先行：D 栅栏安装被阻塞在已准备参与者之后。若 I 提交，Storage 先提交可见性，随后栅栏把该发布捕获/抑制为栅栏前工作。若 I 中止，Storage 回滚，栅栏随后可安装。
- 参与者/协调器状态未知：既不推断可见性，也不推断栅栏完成；操作保持未解决，且在存在冲突的已准备发布时，栅栏不能声称屏障已关闭。

这不是 I 对 D 的覆盖。它是共享的本地排序机制，用于防止栅栏在 D 检查与所有者可见性提交之间插入。

## D. 持久状态机

| 状态 | 权威 | 合法后继状态 | 禁止的捷径 |
|---|---|---|---|
| PRIVATE_STAGED | E/Storage | DEPENDENCIES_COMPLETE | 读者可见或 Published |
| DEPENDENCIES_COMPLETE | D/E | OWNER_PREPARED 或 REJECTED | 血缘不完整即发布 |
| OWNER_PREPARED | Storage DB 参与者 | I_ORDER_PENDING | 释放锁或暴露字节 |
| I_ORDER_PENDING | I 协调器 | I_COMMIT_DECIDED、I_ABORT_DECIDED 或 IN_DOUBT | 把超时当作中止/成功 |
| I_COMMIT_DECIDED | I 协调器 | 参与者提交后 OWNER_COMMITTED | 铸造另一 ID；在 DB 提交前报告 Published |
| I_ABORT_DECIDED | I 协调器 | 参与者回滚后 OWNER_ABORTED | 发布，或以已变更摘要重试 |
| IN_DOUBT | I + Storage 恢复 | 权威恢复后 I_COMMIT_DECIDED 或 I_ABORT_DECIDED | 释放锁、把撤销推进越过未知顺序，或暴露字节 |
| OWNER_COMMITTED | Storage | PUBLISHED 回执回读；E 可终结 | 重复可见性副作用 |
| OWNER_ABORTED | Storage | 全部输出解决后 REJECTED/SUPPRESSED | 以已变更摘要重开同一意图 |

COMMIT_WON 是 I 的排序/提交决策；PUBLISHED 是 Storage 参与者提交加精确 PublicationReceipt 回读。它们是不同状态。完整的跨权威操作只有在两者均有证据时才成功。

## E. 恢复与崩溃矩阵

| 失败点 | 必需持久状态 | 恢复 |
|---|---|---|
| 所有者准备提交之前 | 无已准备参与者；无可见性 | 以同一 ID/摘要重试；无回执即不准入 |
| 所有者准备之后、I 排序之前 | 已准备 XID 与锁；私有字节 | I 协调器解析/重放同一请求；不产生新 ID |
| I 排序请求/ACK 丢失 | I 协调器按 ID+摘要与 XID 查询 | 返回精确决策/位置或 UNKNOWN |
| I COMMIT 持久、Storage 参与者未提交 | 持久协调器 COMMIT + 可恢复已准备 XID | 前向提交精确 XID；读者在参与者提交前保持关闭 |
| I ABORT 持久、参与者未回滚 | 持久 ABORT + 已准备 XID | 回滚精确 XID；读者在中止确认前保持关闭 |
| Storage 参与者已提交、ACK 丢失 | VisibilityPointer + PublicationReceipt + 结果 + outbox 已原子提交 | 回读同一回执；无第二次发布 |
| I/Storage 重启或副本滞后 | 从权威持久状态恢复协调器日志与参与者 XID | 不得使用陈旧副本决策；在对账之前不提供服务 |
| 备份/恢复 | 恢复清单加协调器/参与者决策日志与 D 栅栏账本 | 隔离分区；在服务之前重放决策与当前栅栏 |
| 协调器不可用 / 分区 | 已准备参与者保持存疑并持锁 | 失败关闭；冲突的撤销/栅栏不能越过未知顺序；恢复协调器或保持阻塞 |
| 重复同键 | 原始摘要/决策 | 返回同一结果与排序器位置 |
| 已变更摘要/边界 | 原始不可变行 | 硬冲突并审计；不覆盖 |

不得从行缺失、超时、陈旧副本、ACK 缺失或进程死亡得出 NOT_COMMITTED 结论。否定结果需要权威持久 ABORT 决策与参与者回滚证明。

## F. Storage 与部署决策

- 选定的本地画像：每个 Canonical Memory Authority 一个事务数据库；D 与 Storage 的权威行共享可串行化事务与一个按权威协调器。
- 必需记录：持久工作账本；ProducerClass 登记册/版本；ProducerRegistrationHighWater；ForgetFence 与 BarrierSnapshotReceipt；依赖集合/清单；已准备参与者/XID；PublicationIntent；VisibilityPointer；PublicationReceipt；所有者结果；幂等/回执消费账本；事务性 outbox；恢复/对账检查点。
- CAS：在选定事务内用于代号/版本/租约检查；不是独立的跨记录原子性机制。
- Outbox：必须在同一 Storage 提交事务中，用于下游通知；绝不是可见性或完成证明。
- 对象存储：仅允许用于私有暂存的不可变字节；DB 的 VisibilityPointer 是唯一发布权威。
- 串行化协调器：未选定独立的尽力而为协调器服务。I 排序器是 I/Storage 受保护提交协议的持久协调器；本地 DB 协调器串行化 D/Storage 所有者状态。
- 2PC：被选为跨权威 JF-10 恢复机制。若 I 无法提供持久协调器决策与参与者恢复，或数据库无法保留已准备 XID/锁，则 JF-10 保持阻塞；不允许任何更弱的检查后写入替代。
- 具体引擎/版本、XA/已准备事务支持、隔离配置、复制/法定人数、故障切换与备份/恢复拓扑：未选定 / 未核实。需要 Storage 工程批准与可执行证据。

## G. 必需的 I Owner 决策（不作推定）

请 I 审阅这一精确的 v2 制品，并接受或修订：
1. owner-final-gate 操作即被排序的 I 操作，携带已准备 Storage 参与者/XID、不可变 PublicationOperationId/RequestDigest 与精确 owner_boundary。
2. I 的持久协调器决策可恢复，并控制参与者 COMMIT/ABORT；撤销不能越过存疑的更早门。
3. I 定义协调器日志保留、参与者登记、决策查询、恢复所有权、故障切换/恢复与多策略域全有或全无行为。
4. COMMIT_WON 不是读者可见的发布；Storage 必须提交并返回其 PublicationReceipt。
5. I 保留对清单 epoch/seal、PermissionEpoch、授权策略、例外与 Global Forget Completion 的唯一权威。DE-S 不激活也不批准这些策略。

在 I 接受该精确修订协议之前，JF-10 为 **P0 OPEN / 需要 I 审阅**，且最终受保护发布在跨权威状态未解决时保持失败关闭。

## H. 追加的一致性用例（全部未运行）

| ID | 必需场景 | 期望不变量 |
|---|---|---|
| JF10-01 | Storage 准备进入 I owner-gate 排序器时撤销竞争 | 恰好一个顺序；无独立预检决策 |
| JF10-02 | I COMMIT 决策持久，Storage 参与者在提交前崩溃 | 已准备 XID 被恢复并前向提交；提交前无可见性 |
| JF10-03 | I ABORT 决策持久，Storage 参与者在回滚前崩溃 | 已准备 XID 被恢复并回滚；无可见性 |
| JF10-04 | Storage 参与者已提交，响应/ACK 丢失 | 回读返回同一回执；无重复可见性 |
| JF10-05 | 协调器在持久决策之前/之后崩溃 | 恢复精确决策；未知保持锁定/私有 |
| JF10-06 | D 栅栏与已准备参与者竞争 | 栅栏先行则拒绝；参与者先行则阻塞栅栏直到提交/中止；无第三种顺序 |
| JF10-07 | 多策略域操作 | 全有或全无决策；无部分可见性 |
| JF10-08 | 备份/恢复丢失本地近期快照但协调器决策存活 | 在服务之前隔离并重放决策/栅栏 |
| JF10-I-09 | 回执消费后以同 ID/摘要重试 | 结果/位置完全相同；无第二次消费 |
| JF10-I-10 | 同 ID 但摘要或 owner_boundary 变更 | 硬冲突 |
| JF10-I-11 | I 副本滞后 / 查询不可用 | UNKNOWN；不得本地 ALLOW 或推断 NOT_COMMITTED |
| JF10-I-12 | 参与者准备未解决期间到达撤销 | 撤销不能越过未解决排序；恢复先解决提交/中止 |
| JF10-I-13 | I 排序器故障切换/恢复 | 终态决策与参与者 XID 保持单调且可恢复 |

## I. 不作声明与状态

这是供精确 I Owner 审阅的架构提案。它不是 I 批准、治理激活、具体 DB 部署、实现、测试结果、生产就绪决策或 Global Forget Completion。在可执行实现与故障注入环境存在之前，D36、E36-01..20、C01..C20 与 JF10-01..13 均为 NOT RUN。


## 第 3.6.2 阶段 —— 由 D/E/Storage 消费的 I Owner 处置

**处置来源：** I Owner，`09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md`，Blob `b7b0287cde3922434a560fca90051cc5b418d987`。

**状态更正：** I **接受** JF-10 v2 架构，适用于**单一 I 策略域并附有约束性澄清**。这取代了更早 §6 中"I 接受仍待定"的表述。它不关闭 JF-10 P0，不批准实现，也不批准治理。多策略域原子性仍为 **BLOCKED / 未接受**。

### A. 约束性单域契约

owner-final-gate 操作必须把下列内容绑定为一个不可变授权/参与者元组：

- 稳定 PublicationOperationId 与规范 RequestDigest；
- Storage VisibilityPointer 提交门的精确 owner_boundary；
- 持久 Storage 参与者身份、XID 与参与者摘要；
- CommitAuthorizationReceipt ID 与决策绑定；
- policy_domain_id、PermissionEpoch、PrincipalRef、ActorRef、动作、ResourceRef、目的、受众、ScopeBindingSet 摘要、EnvironmentRef 与 DelegationChainRef；
- 适用的 D ForgetOperationId/栅栏引用与精确 D 所有者谓词证据；
- 当生效 I 策略要求时，权威的 ProducerDomainInventoryEpoch 与 InventorySealReceipt 身份/摘要。

I 协调器 COMMIT 是这一精确参与者的授权/撤销排序记录。它不是发布。Storage 必须在持久 COMMIT 之后前向提交同一 XID，并且在本地可见性事务与匹配的 PublicationReceipt 持久回读之前不得发布。

### B. 回执消费与重放

I 的回执消费必须原子绑定到协调器事务记录、参与者 XID/摘要、操作 ID/摘要、所有者边界、决策 ID、策略域、PermissionEpoch 与排序器位置。同 ID/同摘要/同边界的重放返回同一持久状态。任何已变更的摘要、XID、边界或安全元组都是硬冲突。一个回执不能授权第二次所有者操作。

### C. 终态结果与存疑行为

- `COMMIT_WON`：持久协调器决策；Storage 前向提交精确参与者。不是可见性主张。
- `REVOCATION_WON`：持久的撤销优先结果；Storage 回滚并证明未发布。
- `INDETERMINATE_ABORTED`：持久的非成功终态结果；Storage 回滚。
- `UNKNOWN/IN_DOUBT`：非终态。保持字节私有、保留已准备参与者与必需锁，并阻塞冲突的撤销推进直到权威恢复。

不允许任何启发式提交/中止、基于超时的推断、陈旧副本决策或运维覆盖。I 的权威查询必须已认证且可线性化。协调器日志、参与者身份、回执消费与终态决策必须在故障切换/恢复中不丢失、不重复、不乱序、不反转。

### D. 明确的 D/E/Storage 所有者消费

- **D：** D 在 `forget-fence-operation-and-publication-gate.md` 中既有的第 3.6.2 阶段所有者接受，即 D 对栅栏/登记/屏障排序的处置。D 必须把存疑参与者保持在开启屏障之内；栅栏先行则拒绝准备；参与者先行则保留目标/血缘串行化直到解决。I COMMIT 绝不覆盖 D 栅栏语义。
- **E：** 在读取匹配的持久 Storage PublicationReceipt 之前，E 保持非终态。稳定 PublicationOperationId/RequestDigest 在重试/恢复中存续；AttemptId/LeaseEpoch 仅约束执行尝试，不能铸造新的逻辑发布。
- **Storage：** Storage 拥有已准备 XID 的持久性/恢复，以及原子的 VisibilityPointer + PublicationReceipt + 所有者结果 + 回执消费证据 + outbox 提交。它必须在选定数据库上证明同 XID 前向提交/回滚、锁保留、无启发式结果与恢复/故障切换行为。

这些是架构消费要求，不是实现证据。每个所有者必须为其自身边界提供运行时证据。

### E. 清单与多域限制

当策略要求 InventorySeal 时，I 必须在被排序的 owner-final-gate 操作内部校验当前权威 epoch、seal ID 与摘要。Storage 本地副本/锁不能确立新鲜度。在 I 的清单权威、签名方/验证方、epoch/seal 生命周期与一致性获得批准之前，缺失/陈旧/不可验证的封存证据保持 BLOCKED/UNKNOWN。

任何跨越一个以上 I 策略域的操作必须被拒绝或暂停为 BLOCKED/UNKNOWN。在 I 发布且各所有者消费规范的全局全有或全无协调器协议之前，禁止独立的按域 COMMIT_WON 决策与尽力而为聚合。

### F. 一致性与关闭状态

JF10-01..13 加上 I 追加的 协调器/参与者/回执/清单/栅栏 用例仍为 **SPECIFIED / NOT RUN**。必需证据包括协调器 PREPARE 与终态日志位置、参与者 XID 轨迹、回执消费证明、D 栅栏/屏障轨迹、Storage 原子事务证明、清单封存版本、数据库/运行时身份、确定性故障注入与独立所有者审阅。

**总体处置：** 单域架构在约束性澄清下被接受；多域被阻塞；JF-10 P0 OPEN；实现未核实；软件测试未运行；InventorySeal 与 Global Forget 治理 OPEN；Global Forget Completion 未被声明。
