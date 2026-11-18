# AID-2026-001 — Forget / Memory 生命周期联合契约提案 v2.1（简体中文）

**PROPOSED — 尚不具规范效力。** Owner D/I 尚未批准本修订或任何同 SHA 内容。本文件是互链 EN/ZH 双文件中的中文对应件，是冻结 v2 的增量整改层。请与[英文对应文件](forget-lifecycle-joined-contract-proposal-v2.1.en.md)及[不可变 v2 基线](forget-lifecycle-joined-contract-proposal-v2.md)共同阅读。v1、v2 原文件保持不变且可追溯。

- 工作项：AID-2026-001 / U-023 整改
- 基线 Head：99d3c95d3a82c5880be46385922efb39ab478874
- 来源 Blob：v1 96882570d44f6a3c6d60a30b1edb0e405bde5efc；v2 28ce1f735be6781b8de32a310d50e24cb457f01e；U-010 e12bc3beaf7327f7646fa090cb1fe2cda023cacf；U-011 EN c9daf61a538a175718e1bb492797cb2b5a51547a；U-011 ZH d03d26bbdc96ee9df7f532144d331a3a06be3866；执行边界 008b625bdb29ee65fe136f21c0e9be6396228e4b；R3 矩阵 0dac44f65a47541bf5dca90563c90ade6a5d4331；GOV-DOC-001 b51b054b9f1022133666542680df74dfe19de2fb。
- D 批准：未声明；I 批准：未声明；同 SHA 双边批准：未授予；Storage 批准：未声明。
- 测试：仅规格，尚未运行。

## 1. 纳入基线与不变量

本候选纳入 v2 §§1–5，包括 I 决策信封、绑定提交的回执、PermissionEpoch 向量、九项提交时检查、Legal Hold/例外记录、清单策略/封存、逐目标证据和类型化结果；并叠加下文的恢复要求及 Failed 守卫。本文件不代替 Owner D/I 作任何权责决定。

与 U-010 一致且保持不变的不变量：
1. 成功且持久化的 `SuppressionCommitted` 是规范 Memory 原子转为 `Forgotten` 的唯一触发条件。I 授权是强制提交前置条件，不是触发点。
2. Forgotten 后同一身份永不复活。失败、重试、撤权、未知结果、Restore 或策略变化均不得降低/移除 Fence 或恢复普通访问。
3. I 治理完成不是 Forgotten 的前置条件。D 完成、I 治理评估、逐目标结果、例外决策和物理擦除证据彼此独立。
4. `COMMIT_WON`、`REVOCATION_WON`、`UNKNOWN` 保持 v2/U-011 含义。提交未获证明前 UNKNOWN 必须 fail closed 并对账；已证明的持久化提交仍保持 Forgotten。
5. `ExceptionApproved ≠ Succeeded`。
6. `DomainCompletionEvaluated` 是规范标识；`CompletionEvaluated` 已废弃，不得持久化或作为 API/测试标识输出。
7. 在 Owner D 与 Owner I 批准同一精确内容 SHA 前，状态保持 PROPOSED。

## 2. 恢复 v1 规范要求

### 2.1 每个受保护阶段前重新授权

在**每一个**不可逆或其他受保护阶段前（不只是 SuppressionCommitted），执行方 MUST 重新验证（按适用情况）：认证 Principal/有效 Actor；Delegation；当前 I 决策和权威 PermissionEpoch 向量；精确 Operation/Request Hash/Target/Scope/Purpose；当前 Policy ID/Version/Revision；Retention 和 Legal Hold；当前 D Fence Generation；Target Owner/Capability Profile/Version/Action；必需证据的有效性和新鲜度。检查必须在该阶段自身的执行边界进行。缓存、排队或早期阶段授权不构成持续授权。任何事实被拒绝、过期、不可用、未知或不匹配时均 fail closed，不得执行受保护动作。恢复、Lease、策略/epoch/scope/target 变化、Restore 或证据失效后必须重新检查。这不使 I 治理完成成为 Forgotten 的前置条件。

### 2.2 请求幂等

幂等 Key 按认证 Principal、有效 Scope、Target 身份和 Operation 类型限定。规范 Request Hash 覆盖 Action、Target 集合、Purpose、策略上下文和前置条件。
- 相同 Key + 相同 Hash：复用相同稳定 `operation_id` 和当前结果，不创建第二个 Operation。
- 相同 Key + 不同 Hash：以 `IDEMPOTENCY_CONFLICT` 拒绝，不得修改或扩大原请求。
- 重试和 Inventory Revision 均保持 operation_id。实质变化的请求按幂等作用域建立不同请求/Operation。
- 重试不得弱化 Scope 或隐式扩大 Target 身份。

### 2.3 Checkpoint 与 Lease Fencing

Checkpoint 身份精确为 `operation_id + inventory_revision + target_id + stage + action_version`。每个 Attempt 具有唯一 `attempt_id`、Lease Owner 和单调递增的 `lease_fence`。只有当前 lease_fence 可提交 Checkpoint、证据或 Publication；陈旧 Worker MUST 被拒绝。同一 Checkpoint 的并发重试必须串行化，或针对 Checkpoint Version 使用 Compare-and-Swap。Lease 重新分配创建新 Attempt，不创建新 Operation。

### 2.4 重试分类与对账

MUST 对重试分类，禁止盲目重试。

| 类别 | 示例 | 必需行为 |
|---|---|---|
| 可重试 | 临时网络/服务故障、Rate Limit、Provider 临时故障、Lease 过期 | 使用相同 Operation/Checkpoint、新 attempt_id、当前 lease_fence，并重新执行每阶段检查。 |
| 重试前对账 | 结果未知的超时、可能提交后的超时、重复 ACK、部分批次、响应丢失、Backup 恢复、Inventory Revision 变化、副作用后 Receipt 前崩溃 | 先查询权威状态，对账副作用、提交、证据和 Checkpoint。非幂等物理动作结果未知时不得重复。 |
| 当前 Operation/策略下终止 | Target 身份无效、完整性故障无法对账、授权拒绝、具有约束力的 Legal Hold/Retention 禁止 | 不得盲目重试；记录原因。仅在允许时获取新决策或使用独立身份 Operation。失败不移除 Fence。 |

Unknown、缺少错误、Worker 启动、Dispatch 接受、Queue ACK 或 Transport ACK 均不等于成功。

### 2.5 完整 GovernanceAssessment.Compliant 判定

只有针对精确 Inventory Revision、Policy Revision、Authorization Receipt 和 Evidence Set，以下**全部**条件满足时，I 才 MAY 记录 `Compliant`：
1. 授权及适用策略决策均有效且为当前状态。
2. Inventory 已封存；无未知或未计入的必需 Target。
3. 每个必需 Target Action 均处于其 Target Class 接受且已验证的终态。
4. 所有强制访问/派生/交付/恢复边界均有效抑制。
5. 必需派生清理已验证。
6. 受控主副本和副本擦除要求已满足。
7. Backup 已到期，或每个残留均有单独批准且有边界的 Retention Exception；未到期必需 Backup 不得静默视为已擦除。
8. 外部接收方已提供必需可验证证据，或每个残留均有明确批准且有边界的例外。
9. Audit 证据完整、受完整性保护，且不包含禁止的 Forgotten 内容。
10. 无未解决 Legal Hold、Retention 冲突、不支持的必需 Target、失败动作或未知状态。
任一条件缺失均阻止 Compliant。pending/in_progress/failed/unknown/unsupported 的必需 Target 均阻止 Compliant；必须带原因记录 NonCompliant 或 Deferred。Inventory 扩展、策略变化、撤权、证据到期或 Restore 后必须重新评估。

### 2.6 CompletedWithPolicyException 与公开投影

`CompletedWithPolicyException` 仅为派生公开投影，当且仅当 D 独立记录 `DDomainCompletion=Completed` 且 I 独立记录 `GovernanceAssessment=CompliantWithException` 时才允许。它不是规范生命周期/Operation 状态。D 未 Completed 时，联合结果仍未完成。ExceptionApproved 永远不能把 PerTargetResult 改为 Succeeded。

API/UI MUST 分别公开 MemoryLifecycle、ForgetOperationPhase、DDomainCompletion、每个 PerTargetResult/target_state、GovernanceAssessment、ExceptionDecision 和 PhysicalErasureEvidence。不得把 SuppressionCommitted、Forgotten、CleanupInProgress、Acknowledged、部分成功、D 完成或 I 评估合并为“全域删除”/“Forget 完成”。须如实披露 pending/failed/unknown/unsupported/policy-retained 残留，但不得暴露已 Forgotten 内容。

### 2.7 Target 状态词表

`target_state` 值为：`pending`、`in_progress`、`suppressed`、`cleaned`、`erased`、`expired`、`quarantined`、`acknowledged`、`policy_retained`、`failed`、`unknown`。这些值互不等价，不能推导全局完成。至少保留 operation_id、inventory_revision、target_id、target_class（允许值：Canonical（规范对象）、derivative（派生对象）、index/cache（索引/缓存）、working-set（工作集）、context（上下文）、adapter-managed（适配器管理）、primary-storage（主存储）、replica（副本）、backup（备份）、external-recipient（外部接收方）、audit-copy（审计副本）或 policy-retained（策略保留））、owner_domain、required_action（允许值：suppress（抑制）、invalidate（失效）、delete（删除）、redact（遮蔽）、deidentify（去标识化）、erase（擦除）、expire（到期）、quarantine（隔离）、restore-fence（恢复围栏）、notify（通知）或 verify（验证））、capability/profile version（capability 词表：supported（支持）/ unsupported（不支持）/ conditional（有条件支持），并包含 capability-profile version）、target_state、D fence generation、授权/策略引用、不可变 evidence reference/kind、可信 observed_at、认证 verifier/method/version、attempt_id、lease_fence、稳定 result_code、适用的 exception reference/expiry 和来源 provenance/完整性。未知、不支持、离线、不可访问及未登记但必需的 Target MUST 保留在记录中。

## 3. G04-C — Failed 恢复与只追加事件历史

`Failed` 是**当前 Attempt** 的终态，不自动终止稳定 Operation。只有明确且可审计的恢复决策才允许恢复。v2 §2.2 转换表受以下限制：

| 起始 | 目标 | 强制守卫 |
|---|---|---|
| Failed | CleanupInProgress | 显式 RecoveryStarted Event；先对账既有副作用/Checkpoint；当前每阶段授权、策略、Capability、Fence 检查通过；创建新 attempt_id/当前 lease_fence。 |
| Failed | AuthorizationPending | 显式 ReauthorizationRequired Event；关闭先前 Attempt；建立新 Attempt 身份；新 I 决策验证前不得执行受保护动作。 |
| Failed | Blocked | 显式 BlockerRecorded Event，记录原因/Owner；保留历史；解除阻塞前不执行工作。 |
| Failed | DomainCompletionEvaluated | 仅限评估阶段失败、所有必需证据/Checkpoint 仍当前且完整、显式 ReconciliationCompleted Event 已记录对账，之后由 D 重新评估判定。不得绕过清理/授权；关闭先前 attempt，分配新的 attempt_id，并使用当前 lease_fence。 |
| Failed | Completed / Cancelled / SuppressionCommitted | 禁止直接转换。 |

每次恢复均追加不可变 Event，含认证 Actor、原因、失败 Event 因果引用、先前 Checkpoint、策略/授权证据及可信时间戳。提交后失败保持 Forgotten/Fence。SuppressionCommitted 后仍禁止 Cancelled。

同一幂等请求的重试、Attempt、Lease 变化和 Inventory Revision 均保持稳定 operation_id。每个 Attempt 使用唯一且永不复用的 attempt_id。每次转换均追加不可变 Event，至少含 event_id、operation_id、attempt_id、from/to phase、Actor/Service 及适用时认证 Principal、reason_code、correlation/causation ID、inventory_revision、Checkpoint 身份/版本、Lease Owner/Fence、授权/Receipt 和策略引用、Target/Scope 引用、可信 observed_at、有序 Event Sequence/Version 及完整性 provenance。不得改写/删除/覆盖旧 Failed Event、Checkpoint、Target Result 或 Receipt；更正须追加 superseding Event。提交结果不明时，重试前 MUST 对账持久化 SuppressionCommitted 证据。已证明提交则保持 Forgotten；UNKNOWN 必须 fail closed 并继续对账，不得破坏性 Replay。

## 4. 测试交叉映射 — 源 ID 一对一保留

以下均为规格，不是执行证据。每个 ID 均有独立条款、场景和断言。DFI 来源：R3 矩阵和 Owner Execution Boundary Contracts v1。

### 4.1 DFI-001…DFI-022

| ID | 条款 | 场景 | 必需断言 |
|---|---|---|---|
| DFI-001 | §§1–2 | 并发读取/派生与抑制线性化竞态。 | Fence/Tombstone 提交后，后续读取/派生/交付不得返回内容。 |
| DFI-002 | §§1,2,5 | Forgotten 但 Operation 仍 CleanupInProgress。 | Memory 保持终态；Operation 不得 Completed。 |
| DFI-003 | §2 | SuppressionCommitted 后 Cancel。 | 拒绝 Cancel；Fence 有效。 |
| DFI-004 | §§2,5,2.5 | 必需 Target 缺失/未知/不支持。 | 拒绝全局完成和 Compliant。 |
| DFI-005 | §2.7；v2 §4.4 | 外部 ACK 仅覆盖有限 Managed Region。 | ACK 不证明认证能力/覆盖范围之外的隐藏副本擦除。 |
| DFI-006 | §2.6；v2 §§4.2,5 | CompletedWithPolicyException 投影。 | 要求 D Completed 且 I CompliantWithException，并有边界的批准残留/控制/期限；例外不是目标成功。 |
| DFI-007 | §2.2 | 相同幂等 Key 配合相同/不同 Hash。 | 相同返回同一 Operation；Hash 变化时拒绝 IDEMPOTENCY_CONFLICT。 |
| DFI-008 | §2.3 | 并发重试与陈旧 Lease Worker。 | 只有当前 lease_fence 可提交 Checkpoint/证据。 |
| DFI-009 | §§2.4,3 | 副作用后、Receipt 前发生 Crash。 | 重试前对账；不得重复破坏性动作。 |
| DFI-010 | §§2.1,2.4 | Operation 中撤权或 Legal Hold 变化。 | 下一受保护阶段 fail closed，等待重新授权/评估。 |
| DFI-011 | v2 §4.3；§§2.5,2.7 | Inventory 封存后发现依赖/必需 Target。 | 追加新 Revision、保留旧版、使评估失效并重评。 |
| DFI-012 | §§1,2.7,3 | Forget 后 Backup Restore。 | 恢复数据可查询/交付前应用最新 Fence。 |
| DFI-013 | v2 §4.3；E §3；R3 矩阵 | Producer Admission/依赖登记与 Fence 竞态。 | 登记/发布先于 Fence 串行化，或 Fence 抑制暂存输出；不得有迟到派生项/清单遗漏。 |
| DFI-014 | §§2.3,2.4,3；E §3 | 陈旧 Lease/Replay/重复 Event 下的 Lease/DLQ/Recompile。 | 不得发布已 Forgotten 来源；强制当前 Fence/Lease。 |
| DFI-015 | §§2.1,2.7；F §4 | 在途 Recall/延迟 Cache Fill 与 Fence 竞态。 | 响应/Cache Fill 前重验；Fence 获胜后无陈旧响应。 |
| DFI-016 | §§1,2.7,3；F §4 | Index Rebuild 使用旧 Snapshot/陈旧 Worker。 | 使用规范状态/最新 Fence Watermark；不得复活。 |
| DFI-017 | §§2.1,2.7；G §5 | Forget/撤权后 Replay 离线 Snapshot/Delta。 | 对账当前 ContextVersion/PermissionEpoch/Fence；拒绝陈旧 Delta。 |
| DFI-018 | §§1,2.7；G §5 | Context Remove 与规范 Forget 混淆。 | Remove 仅改变成员；Forget 使映射投影/待处理 Delivery 失效。 |
| DFI-019 | §2.7；v2 §4.4；H §6 | ACK 类别/Capability Epoch 受限或降级。 | 仅报告当前支持范围/动作；不得升级为擦除/Full Applied。 |
| DFI-020 | §§1,2.7；C §7 | Telemetry/Inference 重新输出 Forgotten 来源或声称成功。 | Agent/模型声明无权威性；检查 Lineage/Fence，拒绝陈旧内容。 |
| DFI-021 | §§1,3；Storage §8 | 原子抑制提交附近 Crash/Failover。 | Tombstone/Fence/Operation/Publication Intent 恢复一致；不得暴露内容/丢失 Fence。 |
| DFI-022 | §§1,2.7,3；Storage §8 | 应用最新 Fence 前 Restore。 | 最新 Fence/后续 Forget 应用前副本保持 Quarantined；不得复活。 |

### 4.2 I-U011-T01…T16 — 精确保留原始含义

| ID | 条款 | 场景 | 必需断言 |
|---|---|---|---|
| I-U011-T01 | v2 §3.1 | 伪造/未知签发者或签名无效。 | 拒绝授权；不得提交。 |
| I-U011-T02 | v2 §§3.1–3.2 | Audience/Operation/Request Hash/Purpose/Scope 不匹配。 | 拒绝回执；不得提交。 |
| I-U011-T03 | v2 §§3.1–3.2 | 回执过期/尚未生效或 Nonce 重放。 | Fail closed；不得提交。 |
| I-U011-T04 | v2 §3.3 | 当前 PermissionEpoch 与回执 Epoch 不同。 | 拒绝陈旧回执。 |
| I-U011-T05 | v2 §3.3 | 撤权 Epoch 先序列化。 | REVOCATION_WON；不得提交。 |
| I-U011-T06 | v2 §3.3 | 提交先于后续撤权序列化。 | COMMIT_WON；持久化 Forgotten 终态；不得复活。 |
| I-U011-T07 | v2 §3.3 | 无法证明序列化/当前 Epoch。 | UNKNOWN；fail closed/对账；已证明提交仍保持 Forgotten。 |
| I-U011-T08 | v2 §§3.1,3.3 | 竞态期间 Delegation 被撤销/收窄。 | 当前性检查拒绝陈旧 Delegation。 |
| I-U011-T09 | v2 §§4.1–4.2 | Legal Hold/强制保留禁止动作。 | 拒绝/延期；不得未经授权例外。 |
| I-U011-T10 | v2 §4.2 | 例外缺少批准人/权限/范围/司法辖区/期限/控制。 | 例外无效；不得 CompliantWithException。 |
| I-U011-T11 | v2 §§2.7,5 | 例外批准但目标动作未执行。 | PerTargetResult 不得为 Succeeded。 |
| I-U011-T12 | §§2.5,2.7；v2 §§4.3,5 | 必需 Target 未知/不支持/未登记。 | GovernanceAssessment 不得 Compliant；Target 保留并标记未解决。 |
| I-U011-T13 | v2 §4.3 | 评估后出现新 Target/Inventory 或 Policy Revision。 | 先前评估失效；重新评估。 |
| I-U011-T14 | v2 §§4.2,5 | 例外到期/撤销或 Legal Hold 变化。 | 重新评估；不得静默续期。 |
| I-U011-T15 | §§2.5,2.6；v2 §5 | 所有 Target 证据齐全但 D 完成缺失。 | I MUST NOT 宣告 D 完成；不得生成 CompletedWithPolicyException 投影。 |
| I-U011-T16 | §§1,2.6；v2 §§1,5 | Forgotten 已提交但清理仍待处理。 | Forgotten 保持终态；治理评估独立保持 Pending/NonCompliant（视情况）。 |

## 5. G04-C 处置

**本候选的文档规格已整改。** §3 为此前含糊的 Failed 转换增加守卫，并规定 Operation/Attempt 身份、显式恢复 Event、对账及只追加历史。

**实现/故障注入门禁仍为 OPEN / NOT EVIDENCED。** 在可复现测试覆盖所有允许/禁止恢复转换、陈旧 Lease 拒绝、稳定 operation_id/新 attempt_id、事件历史不可变、模糊提交对账及提交后不复活前，不得称 G04-C 完全关闭。本文件不声称测试已执行。

## 6. 语义变更裁决登记

本次未有意删除任何 v1 语义要求；U023-REG-001 的八组要求均已恢复。本版本未单方提出 D/I 语义变更。若任一 Owner 认为恢复规则与其权责冲突，须登记为 **D/I EXPLICIT DECISION REQUIRED**；本执行方不决定、不豁免、不重新解释。双边决策前保留 v1 来源要求及 PROPOSED 状态。

## 7. Finding、批准与不作出的声明

- **U023-GOV-001 — P1 — Issue #41 — FIXED_PENDING_INDEPENDENT_REVIEW。** 同一 Commit 提供独立 EN/ZH 对应件、互链及完整的语言专属规范测试表。
- **U023-REG-001 — P1 — Issue #41 — FIXED_PENDING_INDEPENDENT_REVIEW。** §2 恢复全部八组 v1 要求；不主张删除语义。
- **U023-TEST-001 — P1 — Issue #41 — FIXED_PENDING_INDEPENDENT_REVIEW。** I-U011-T01…T16 一对一保留源含义；DFI-001…022 各有独立映射行。
- **G04-C — P1 — Issue #41 — SPECIFICATION_REMEDIATED; IMPLEMENTATION_EVIDENCE_OPEN。** 已规定恢复守卫/历史；故障注入证据仍待补。

回归自查：`SuppressionCommitted ⇒ Forgotten` 仍是唯一触发；原子进入后不可复活；I 授权是提交前置条件而非触发点；I 治理完成不是 Forgotten 前置条件；COMMIT_WON/REVOCATION_WON/UNKNOWN 保持；ExceptionApproved ≠ Succeeded；PROPOSED 保持。

不声称 Owner D/I 批准、Storage 批准/原子性证明、运行时实现、生产符合性、R3 执行、独立复审 PASS、D-R3-D-003 关闭、验收、合并 main 或生产激活。AID-2026-001 仍为 BLOCKED_PENDING_R3_EVIDENCE。
