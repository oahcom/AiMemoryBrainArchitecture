# Owner I U-011 — 授权、撤权、PermissionEpoch 与治理证据契约

- Work Item：AID-2026-001
- 派工来源：relay-011；指令来源：本 ChatGPT 会话中的用户指令；提供时间：2026-11-18 22:35 +08:00
- Conversation ID：UNAVAILABLE_TO_EXECUTING_SESSION（执行环境不可见，未伪造）
- 角色提示词：CHATGPT-OWNER-I-001 v2.0；`14-ai-development/prompts/owners/I/owner-session-v2.md`；源 Blob：`abf8551e37580f1e18a8f956ba453d88918a87b2`；源 commit：`6b5db2918cffc2281deb22fd9858a37dbaeec726`；提示词 SHA-256：NOT_VERIFIED
- 全局规则：AI-EXEC-001 v1.0 ADOPTED；AI-EXEC-002 v1.0 ADOPTED
- 基线：`remediation/aid-2026-001-forget-contract-closure-2026-11-18` @ `eb6aa17c9cefb51434234cdb0f5503197416b9bf`（派工事实包提供，且与 Issue #41 的 U-010 评论交叉印证；任何后续写入前必须重新核验）
- 任务类/风险级：ARCH / SEC / DOC；R3
- 状态：I 侧契约候选；不声称 Owner I 正式批准；D/I 同 SHA 批准尚未取得
- 语言状态：本文件为完整中文对应稿；英文工作稿路径为 `owner-i-r3-governance-rules-u011-v1.md`；双语语义一致性仍须独立审查
- 回流：既有 Issue #41；未新建 Issue/PR

## 1. 权责与不变量

1. I 负责安全主体、经过认证的行为主体/委托关系、授权决策、PermissionEpoch、撤权排序、隐私/保留/Legal Hold 策略、全局必需目标策略、治理评估以及例外批准与证据。
2. D 独占负责 Memory 的规范生命周期、Forgotten 的含义与触发点、ForgetOperation 阶段语义以及 D 领域完成状态。本契约不重新定义这些事项。
3. 本契约将 D 侧 U-010 决议作为接口前提：成功且持久化的 `SuppressionCommitted` 是 D 领域转入 `Forgotten` 的唯一触发条件；I 授权是提交前置条件，而不是提交后的治理完成条件。提交之后发生的失败、撤权或未知状态，均不得使 Memory 复活，也不得降低或移除 fence。
4. 只有 Storage 有权批准并证明持久化序列化、原子提交和可见性。Executors 只能证明各自能力边界内负责的目标动作。I 不得代替 Storage 或 Executors 批准其边界。
5. `Forgotten`、`DDomainCompletion`、`GovernanceAssessment`、每个 `PerTargetResult`、例外处置以及 `PhysicalErasureEvidence` 是相互独立的类型化事实。不得用一个布尔值或标签将其合并表达为“所有地方均已删除”。
6. 本文件是候选契约工件，不是已采纳的生产策略、实现、测试结果、Owner I 正式批准、D/I 同 SHA 批准、Storage 批准、验收或激活。

## 2. 认证授权决策与授权回执

### 2.1 决策信封

授权决策必须是可验证、不可变的决策信封，至少包含：

- `decision_id`：全局唯一且不可复用的标识符；
- `issuer_id` 及签发者密钥/版本：受信任且经 I 授权的决策签发者；
- `subject_principal_id`：经过认证的请求主体；
- `actor_principal_id`：通过委托行事时的实际有效行为主体；
- `delegation_chain`：有序且可验证的委托引用及约束；仅在直接权限适用时才允许为空；
- `action`：明确的操作，例如 `FORGET`；
- `resource_scope`：稳定的目标/资源标识符以及明确的范围边界；
- `purpose`：与该请求绑定的声明用途；
- `policy_id`、`policy_version` 以及策略评估上下文/修订版本；
- `permission_epoch`：由 I 针对该授权主体/策略域签发的单调递增 epoch；
- `decision`：`ALLOW` 或 `DENY`；不允许隐式放行；
- `not_before`、`expires_at` 和 `issued_at`；
- `request_hash`：规范化请求字段的摘要，包含操作、主体/委托、范围、用途及适用前置条件；
- `audience`：预期接收该授权的服务/操作/提交边界；
- `nonce` 或具备等效防重放能力的标识符；
- `provenance` 以及密码学完整性/真实性材料。

该信封必须由受信任且经 I 授权的签发者签名，或通过其他可信机制完成认证。调用方提供的布尔值、未签名载荷、日志行、UI 状态、Executor 确认，或仅仅持有 decision ID，均不构成授权回执。验证必须确认签发者可信性、签名/完整性、audience、请求绑定、有效时间窗口、nonce/重放状态、委托约束和策略版本。

### 2.2 授权回执

与提交绑定的授权回执，是经过验证的决策，加上验证结果和提交尝试绑定信息。它必须包含：

- 完整的决策信封引用及其不可变摘要；
- 验证结果以及验证者身份/版本；
- 精确的 `operation_id`、request hash、行为主体、操作、目标范围和用途；
- 适用的 PermissionEpoch 和策略修订版本；
- 提交尝试/事务标识，以及序列化点检查结果；
- 来自可信时间源的决策时间和验证时间；
- 唯一回执 ID，以及受完整性保护的来源信息。

回执仅对其精确的 audience、operation、request hash、scope、purpose、policy context、epoch 和有效时间区间有效。它不得转移到其他操作或更宽的范围。任何实质性请求变更都必须重新生成决策和回执。

## 3. PermissionEpoch 与撤权竞态协议

### 3.1 Epoch 语义

1. I 针对每个已定义的授权主体/策略域维护单调递增的 PermissionEpoch。Epoch 值绝不得复用或递减。
2. 任何影响授权的变更（撤权、撤销委托、权限降低、主体停用、使既有授权失效的策略变更）都必须在 I 授权权威系统中原子地推进相关 epoch。
3. 只有在序列化检查时，某决策的 epoch 与每个适用授权域的权威当前 epoch 相等，该决策才是当前有效的。“签发时间很近”、缓存新鲜度、队列顺序或此前成功的预检都不能替代该检查。
4. Epoch 比较必须针对权威的、具备线性一致性或等效 fencing 保证的当前值来源执行。如果无法读取或证明当前 epoch，则结果为 UNKNOWN，操作必须在提交前 fail closed。
5. 如果请求依赖多个主体/委托/策略，其回执必须绑定完整的 epoch 向量，而不是选择其中一个方便的 epoch。任一不匹配都会使回执失效。

### 3.2 提交序列化点的胜出规则

授权与撤权必须在持久化 suppression 提交边界共享一个确定性的序列化顺序。规则如下：

- **COMMIT_WON**：提交事务验证认证回执、当前 epoch 向量、策略修订版本、范围和有效期，并在撤权 epoch 推进生效之前，于某个序列化点原子记录 suppression/fence。Storage 必须证明该先后顺序及持久化原子性。Memory 按 D 的定义，在该次成功提交时进入 Forgotten。之后发生的撤权不得回滚提交、移除 fence 或使 Memory 复活。
- **REVOCATION_WON**：撤权/epoch 推进先完成序列化。提交时的 epoch 比较检测到不匹配并拒绝授权。不得报告 suppression 提交成功，也不得声称发生 Forgotten 转换。如果策略允许重试，则必须重新取得授权决策。
- **UNKNOWN**：系统无法证明哪个事件先完成序列化，无法确立权威 epoch/当前策略，或无法证明持久化事务结果。在提交尚未确认之前，必须 fail closed，不得声称成功；重试前必须先核对事务状态。如果之后证明持久化的 `SuppressionCommitted` 已成功，则必须适用 D 的 Forgotten 终态规则，不得撤销。

提交前的授权预检仅供参考。权威检查必须在建立 suppression 提交的事务内部重复执行，或与该事务原子耦合。禁止在 epoch 验证与提交之间存在检查时点/使用时点（TOCTOU）间隙。具体机制（事务性 compare-and-swap、序列化锁、fenced epoch token 或等效机制）由 Storage 和承担实现责任的 Owner 决定；I 规定安全属性，不规定 Storage 的内部实现机制。

### 3.3 失败与重放

签名/签发者无效、audience 错误、request hash 不匹配、范围扩大、回执过期/尚未生效、委托已撤销、epoch 过期、策略修订版本不匹配、nonce 重放、权威 epoch 不可用或排序结果 UNKNOWN，均必须在提交前 fail closed。重试必须具备幂等性，并绑定同一 operation/request 身份；请求发生变化时必须取得新决策。事务结果不明确时，必须在重试破坏性操作之前，根据持久化提交证据完成核对。

## 4. I authorization precondition for SuppressionCommitted / SuppressionCommitted 时 I 侧治理授权前置条件

只有在提交序列化点验证以下全部条件后，I 对 D 所有提交的授权前置条件才算满足：

1. 决策信封真实有效，且由当前仍受信任的 I 授权签发者签发。
2. 经过认证的请求主体、有效行为主体及委托链均有效，并有权执行该精确操作。
3. 操作、operation、目标范围、用途和规范化 request hash 完全匹配。
4. 决策为 `ALLOW`，处于有效时间区间内，并且 audience 指向执行提交的服务/操作。
5. 每个适用的 PermissionEpoch 均等于权威当前 epoch；不存在先行序列化的相关撤权或策略失效事件。
6. 适用的策略版本/修订版本是当前版本，且允许所请求的操作。
7. 不存在禁止该操作或所请求范围的适用 Legal Hold 或强制保留规则。如果 hold/保留规则要求延期或拒绝，I 必须返回相应结果，不得静默覆盖。
8. 回执具备防重放能力，且未被用于其他操作或不兼容的提交尝试。
9. 提交时的验证者能够提供受完整性保护的证据，证明上述检查及其与提交序列化的关系。

该清单仅定义 I 的安全授权门禁。它**不**要求 D 在执行 `SuppressionCommitted` 转换前，必须完成所有下游清理、所有跨系统目标动作、所有保留期限或物理擦除。这些事项应按照适用策略和类型化治理评估分别判断。如果某项具体法律/保留规则禁止 suppression 本身，则必须在提交前拒绝或延期授权；不得将其表述为 Forgotten 的提交后延迟条件。

## 5. Retention 与 Legal Hold 例外

### 5.1 默认规则与批准权

在适用法律、约束性策略或有效 hold 禁止删除或 suppression 受影响数据时，Retention/Legal Hold 默认采取拒绝/延期。只有明确指定的 I 策略权威主体可以批准法律和策略允许的、范围严格受限的例外。请求方、Executors、D、Storage 或自动化工作流均不得自行批准 I 例外。如果适用法律不允许例外，任何 I 批准都不能创造这种许可。

### 5.2 必需的例外记录

每项例外决策都必须具有不可变记录，至少包含：

- `exception_id`、决策 ID 和状态（`PENDING`、`APPROVED`、`DENIED`、`EXPIRED`、`REVOKED`、`SUPERSEDED`）；
- 具名的批准 I 权威主体、经过认证的主体身份、角色/权限依据及委托证据；
- 受影响的操作、精确目标 ID、数据类别、系统/区域和范围边界；
- Legal Hold 标识符或保留策略标识符/版本、司法辖区及所引用的依据（受法律特权控制）；
- 明确理由、必要性/比例性论证以及考虑过的替代方案；
- 精确允许的操作和禁止的操作；
- 残留数据/暴露情况说明、访问限制及补偿性控制；
- 证据引用、来源信息、完整性元数据及决策时间；
- 生效时间、到期时间、下次复核日期和负责的策略 Owner；
- 重新评估触发条件，包括 hold 解除/变更、策略变更、范围/目标变更、证据到期、恢复、访问控制变更或例外到期；
- 到期/撤销后的处置方式及必需的后续动作。

例外必须遵循最小权限原则，针对特定目标、绑定特定用途并设置明确时限。禁止一揽子、无限期、隐式或追溯性例外。实质性范围变更必须形成新决策。例外到期不得静默续期。

### 5.3 效力边界

已批准的 retention/legal-hold 例外：

- 不改变 D 的 Forgotten 状态，也不撤销已提交的 suppression；
- 不授权对已 suppression 内容进行普通访问、检索、派生、交付、重放或恢复；
- 不证明 Executor 成功、目标清理完成或物理擦除完成；
- 不得将任何 `PerTargetResult` 设置为 `Succeeded`；
- 本身不构成全局 `GovernanceAssessment.Compliant`；
- 只有在每项必需策略条件和补偿性控制均有证据支持时，才可以支持一个单独类型化的 `CompliantWithException` 评估；
- 如果法律/策略依据不允许例外，或必需控制/证据缺失，则必须产生 `Deferred` 或 `NonCompliant`。

Legal Hold 可能要求保留特定证据。此类证据必须隔离保存、实施访问控制、限制用途、保护完整性，并且只在授权期限内保留。不得在证据中包含不必要的 Forgotten 内容；优先使用证据引用和最少必要元数据。

## 6. 跨系统必需目标策略接口

### 6.1 I 策略与 D/Executor 发现职责

I 负责全局策略，声明针对特定数据类别、司法辖区、操作和策略修订版本，哪些目标类别及义务属于必需项。D 负责其领域依赖/清单契约及领域发现语义。每个 Executor 负责其系统边界内的发现和能力报告。I 不规定内部发现算法，也不得在没有证据时声称某 Executor 已发现其本地全部目标。

策略接口必须定义：

- 策略 ID/版本/修订版本及生效区间；
- 适用的数据类别、司法辖区、操作类型以及主体/用途条件；
- 必需目标类别及义务（suppression、拒绝访问、派生数据清理、副本/备份处理、接收方证据、恢复 fencing 等）；
- 条件适用规则以及带理由的明确排除项；
- 每种目标类别所需的证据类型、新鲜度窗口、来源信息及可接受的终态结果；
- 不支持的能力如何处理，以及升级责任 Owner；
- 清单修订/封存要求及失效触发条件；
- 例外资格及所需权威批准/证据。

### 6.2 清单修订与封存

每次评估必须绑定到一个不可变的清单修订版本，至少包含清单 ID、修订版本、发现来源/Owner、发现时间、范围、策略修订版本、目标身份/类别、能力状态、排除项和完整性摘要。D/Executors 提供其负责的清单事实；I 根据 I 策略评估覆盖情况。

只有在负责发现的 Owner 证明该修订版本所声明的发现流程已完成、所有已知来源均已查询、未解决的发现错误均已记录、所有排除项均已明确时，清单才可视为已封存以供评估。“已封存”表示某次评估的输入已固定，并不证明不存在任何尚未发现的目标。

未知、未登记、新发现、不受支持或无法解释的必需目标类别，都必须阻止评估结果成为 `Compliant`。新增目标或新的清单修订版本会使先前评估失效，并要求重新评估。策略修订版本变化、新的数据类别/司法辖区事实、恢复事件、证据到期或相关权限/hold 变更，也会触发重新评估。

I 可以定义必需覆盖范围，并依据策略接受或拒绝证据；I **不得**捏造目标发现事实，也不得将目标动作标记为成功。如果无法证明完整性，评估结果必须是 `Pending`、`Deferred` 或 `NonCompliant`，绝不能是 `Compliant`。

## 7. 治理评估及例外/结果类型

以下均为相互独立的类型，**不得相互强制转换或混同**：

- `PerTargetResult`（Executor 所有）：`NotStarted`、`InProgress`、`Succeeded`、`Failed`、`Unknown`、`Unsupported`、`NotEvidenced`。
- `ExceptionDecision`（I 所有）：`Pending`、`Approved`、`Denied`、`Expired`、`Revoked`、`Superseded`，并带有不可变例外引用。
- `GovernanceAssessment`（I 所有）：`Pending`、`Compliant`、`NonCompliant`、`Deferred`、`CompliantWithException`。
- `DDomainCompletion`（D 所有）和 `MemoryLifecycle`（D 所有）继续遵循 D 的定义；I 只消费其类型化引用。

规则：

1. `ExceptionApproved` 不是 `PerTargetResult`，绝不得存储、展示、聚合或映射为 `Succeeded`。
2. 已批准例外记录的是对某项残余义务的策略处置，不是目标动作已经发生的证据。
3. 只有在每项例外均有效、适用、处于授权范围内、未到期、经独立批准且有必需控制/证据支持，同时其他每项必需目标/义务均满足策略时，才允许 `CompliantWithException`。
4. 任何必需目标处于待处理、失败、未知、不受支持或缺少证据状态，都会阻止 `Compliant`；不得将局部成功聚合成全局合规。
5. 治理评估必须引用其所评估的精确清单修订版本、策略修订版本、授权回执、目标证据集和例外决策。
6. 清单/策略变更、例外到期/撤销、新 Legal Hold、证据到期、恢复，或授权/目标范围的任何实质变更，都会使评估失效。
7. `Compliant` 或 `CompliantWithException` 均不得改写 D 的 `Forgotten` 或 D 领域完成状态；如果缺少目标级证据，也都不能证明物理擦除。

## 8. 必需一致性测试用例

以下仅为测试规格；没有任何用例被声称已经执行。

| 测试 ID | 场景 | 必需断言 |
|---|---|---|
| I-U011-T01 | 伪造/未知签发者或签名无效 | 拒绝授权；不得提交 |
| I-U011-T02 | audience、operation、request hash、purpose 或 scope 不匹配 | 拒绝回执；不得提交 |
| I-U011-T03 | 回执已过期/尚未生效或 nonce 已重放 | fail closed；不得提交 |
| I-U011-T04 | 当前 PermissionEpoch 与回执 epoch 不同 | 拒绝过期回执 |
| I-U011-T05 | 撤权 epoch 先于提交完成序列化 | REVOCATION_WON；不得提交 |
| I-U011-T06 | 提交先于后续撤权完成序列化 | COMMIT_WON；Forgotten 持久保持终态；不得复活 |
| I-U011-T07 | 无法证明序列化顺序/当前 epoch | UNKNOWN；提交前 fail closed 并核对 |
| I-U011-T08 | 竞态期间委托被撤销或收窄 | epoch/当前性检查拒绝过期委托 |
| I-U011-T09 | Legal Hold/强制保留禁止该操作 | 拒绝/延期；除非法律/策略允许，否则不得例外 |
| I-U011-T10 | 例外缺少批准者、范围、依据、期限或控制 | 例外无效；不得形成 CompliantWithException 评估 |
| I-U011-T11 | 例外已批准但目标动作未执行 | 目标仍非成功；不得虚报 Succeeded |
| I-U011-T12 | 必需目标未知/不受支持/未登记 | GovernanceAssessment 不得为 Compliant |
| I-U011-T13 | 评估后出现新目标/清单或策略修订版本 | 先前评估失效；必须重新评估 |
| I-U011-T14 | 例外到期/撤销或 hold 变更 | 重新评估；不得静默续期 |
| I-U011-T15 | 所有目标证据齐全但缺少 D 领域完成状态 | I 评估不得宣告 D 已完成 |
| I-U011-T16 | D 已提交 Forgotten，但清理仍待处理 | Forgotten 保持终态；GovernanceAssessment 依情况独立保持待处理/不合规 |

测试执行必须提供可复现的测试框架、fixture、命令、输出、环境以及精确被测 commit SHA。当前状态：NOT RUN / NOT EVIDENCED。

## 9. Finding 处置

| Finding | 严重级 | U-011 的 I 侧处置 | 回流去向 |
|---|---|---|---|
| I-U009-001 | P1 | 已规定回执信封、验证、PermissionEpoch 向量及 COMMIT_WON / REVOCATION_WON / UNKNOWN 排序；实现、H/transport 绑定和竞态测试仍未完成 | Issue #41 |
| I-U009-002 | P1 | 接受 D 侧已澄清的触发语义：I 仅定义 §4 的提交时安全授权前置条件；精确 joined D/I 契约及同 SHA 批准仍未完成 | Issue #41 |
| I-U009-003 | P1 | 已规定类型化保留/Legal Hold 例外权威、记录结构、效力边界及拒绝/延期规则；法律策略验证和实现仍未完成 | Issue #41 |
| I-U009-004 | P2 | 已规定 I 全局必需目标策略接口、清单修订/封存和失效规则；D/Executor 发现与证据仍由各自 Owner 负责 | Issue #41 |
| I-U009-005 | P2 | 已将 ExceptionDecision 与 PerTargetResult 分离；ExceptionApproved 不得映射为 Succeeded；已规定 GovernanceAssessment 规则 | Issue #41 |
| I-U011-006 | P2 | 执行上下文无法取得派工 Conversation ID；保留 relay-011 和用户提供的时间，不伪造标识 | Issue #41 |

以上均为作者侧候选处置，不构成 Finding 关闭声明。每项 Finding 在满足客观关闭条件前，均保持 `OPEN_PENDING_INDEPENDENT_REVIEW_AND_REQUIRED_OWNER_EVIDENCE`。

## 10. 批准与剩余门禁

- 本文件是供整合进 D/I joined contract 的 I 侧候选契约。
- AI-EXEC-002 §5 禁止将 AI 角色扮演视为 Owner 批准。因此，本会话不会仅因以 Owner I 角色撰写文件就声称取得 Owner I 正式批准。承担责任的 Owner I 权威主体必须通过项目认可的批准机制，对本文件的精确 Artifact/Blob 或最终 joined contract 的精确内容 SHA 作出批准。
- Owner D 必须批准完全相同的 joined 双语内容 SHA。分别批准不同文件、不同 commit、摘要或不同哈希，不构成同 SHA 批准。
- Storage 必须独立批准并提供持久化序列化/原子性/可见性证据。本契约不规定，也不批准 Storage 内部实现。
- H/transport 及其他受影响 Owner 必须在各自职责边界内确认主体、audience、委托、目标/范围及证据绑定。
- 独立集成/安全审查、双语语义一致性审查以及可复现的 R3 运行时/竞态/故障注入测试，仍为 PENDING / NOT RUN。
- D-R3-D-003 继续保持双边门禁。AID-2026-001 继续保持 `BLOCKED_PENDING_R3_EVIDENCE`。
- 本文件不授权生产激活、验收、合并到 main 或宣称实现完成。

## 11. 双语语义一致性

本英文工作稿具有单独维护的完整中文对应稿：`14-ai-development/work-items/AID-2026-001/owner-i-r3-governance-rules-u011-v1.zh-CN.md`。作者侧翻译已完成。针对上一版精确双语文件对的独立语义审查（EN Blob `241f1ac4c63758bb791eb9b7d94bdfaf70eda66d`；ZH Blob `ba8f2b0569c834cc384dce0c01b5d918c10a3d0b`；审查基线 `5a24134200f55d6f559a452d509b8dbcd9753719`）已完成，结论为 **FAIL**，发现 `I-U012-001` 和 `I-U012-002`（均为 P2，已回流至 Issue #41）。这两项发现正在本次双语变更集中整改；在针对整改后精确 Head 的新一轮独立审查完成前，均保持 OPEN。不得将双语对等标记为 PASS，也不得将这两份文件单独视为已批准的 joined contract。最终 joined contract 必须在同一个冻结变更集中纳入两种语言的相同规则，并依据 GOV-DOC-001 进行审查。

## 12. 明确不作出的声明

本文件不声称已经实现生产授权服务、epoch 存储、事务协议、例外工作流、清单发现、目标执行、Storage 原子性或审计流水线。没有执行 R3 测试。没有声称取得 Owner I 正式批准或 D/I 同 SHA 批准。本文件本身不关闭任何 Finding。

---

## 双语对应关系与维护约束

- 英文工作稿：`owner-i-r3-governance-rules-u011-v1.md`
- 本中文对应稿：`owner-i-r3-governance-rules-u011-v1.zh-CN.md`
- 两份文件属于同一 AID-2026-001 / U-011 规则版本。
- 任一语言版本发生规范性变更时，另一语言版本必须在同一变更集中同步更新。
- 任何状态值、字段名、Finding ID、测试 ID、权限边界、否定性约束和强制性要求均须保持一致；代码标识符不翻译、不改名。
- 翻译完成不等于独立语义审查通过；双语 PASS 必须由独立审查给出并绑定精确 Head。
- 两份文件均为候选契约，不因翻译完成而自动成为 ADOPTED 生产规范。
