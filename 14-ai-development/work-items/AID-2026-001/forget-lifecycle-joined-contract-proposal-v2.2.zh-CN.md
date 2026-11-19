# AID-2026-001 — Forget / Memory 生命周期联合契约提案 v2.2（简体中文）

**PROPOSED — 尚不具规范效力。** 本文件是在冻结 v2.1 双语层之上的 Storage/Backup 持久化边界增量完成层。不替换、修改、覆盖或削弱 v2.1。根据治理记录，v2.1 精确 Blob 仍是已批准的上游层；该批准不会自动延伸至 v2.2。D/I/Storage 对本 v2.2 精确 SHA 的批准：均未声明。本层不声称已取得同 SHA 批准。

请与 [v2.2 英文对应文件](forget-lifecycle-joined-contract-proposal-v2.2.en.md)、[冻结的 v2.1 英文层](forget-lifecycle-joined-contract-proposal-v2.1.en.md)及[冻结的 v2.1 中文层](forget-lifecycle-joined-contract-proposal-v2.1.zh-CN.md)共同阅读。v2.1 保持不可变。

- 工作项：AID-2026-001 / STOR-R3-001 整改
- 层级：v2.2 — v2.1 之上的持久化边界增量完成层
- 基线 Head：cc571886c7f5afb8f581740486f6f32ed5f2e61d
- 来源 Blob：v1 96882570d44f6a3c6d60a30b1edb0e405bde5efc；v2 28ce1f735be6781b8de32a310d50e24cb457f01e；v2.1 EN 7acd3e5095995c6b8c52b637d7d9978e96619c3a；v2.1 ZH 5c778a6e095d3087937da5edd0273cbfc744ec80；U-010 e12bc3beaf7327f7646fa090cb1fe2cda023cacf；Owner Execution Boundary Contracts v1 008b625bdb29ee65fe136f21c0e9be6396228e4b；R3 Contract Test Matrix 0dac44f65a47541bf5dca90563c90ade6a5d4331。
- 状态：PROPOSED — NOT NORMATIVE；实现/证据未验证；测试未运行。

## 1. 目的、范围与权责

本层针对 STOR-R3-001 / P1 / Issue #41，明确承载 U-010 D-R3-D-002 和《Owner Execution Boundary Contracts v1》§8 的 Storage/Backup 义务。本层是增量层；v2.1 仍为已批准的上游语义层。本文件未覆盖之处，继续适用 v2.1 及其源契约。本提案规定要求，不证明已有实现、原子性、备份完整性、恢复安全或测试执行。

Owner D 拥有规范生命周期与 ForgetFence 语义，并提供领域事件/证明。Owner I 拥有授权、策略、Retention/Legal Hold 及治理证据接受规则，并提供其类型化决策/引用。Storage/Backup 拥有并必须证明持久化排序、原子性、复制/故障切换、备份生命周期、恢复隔离及恢复可见性。本层不转移权责。

## 2. STOR-01 — 持久化语义提交元组的原子性

对于每个进入 SuppressionCommitted 的 Forget Operation，Storage MUST 在**单一、经 Storage 批准的持久化原子排序与可见性边界**内绑定以下六项；或采用经过明确审查、对外可观察保证等价的事务协议：

1. 规范 Memory 身份及预期当前 Lifecycle/Version，包括防止陈旧写入的并发/版本判定条件。
2. 终态 MemoryLifecycle=Forgotten 及其对应的不可变规范 LifecycleEvent。
3. 适用且单调递增的 ForgetFence generation 与 Tombstone，绑定规范身份并防止回滚/降低。
4. 稳定 ForgetOperation 身份、幂等身份/请求绑定，以及 Operation 阶段 SuppressionCommitted。
5. 足以使已提交抑制对下游执行/对账可观察的持久化 Outbox/Publication 记录；原子边界之外事后尽力发送的通知不充分。
6. I 授权决策和 D 抑制证明的不可变类型化引用和/或密码学摘要，并绑定同一 Operation、Memory 身份、Fence Generation 和 Commit。

六项共同构成一个语义元组，不是六次各自成功的独立写入。权威结果 MUST 是全有或全无。禁止在 Fence、Operation 状态、证明引用或持久化发布意图缺失时，部分可见地呈现 Forgotten。若只有 Fence/Outbox 记录而规范终态化未发生，也不得报告为已完成的抑制提交。

Storage MUST 记录所选 Transaction/Consensus/WAL 协议、原子性/持久性保证、排序点、隔离/可见性、崩溃恢复及幂等重试行为。若未采用单一物理数据库事务，则等价协议 MUST 经明确审查，并证明：(a) 完整元组具有唯一权威提交决策；(b) 在声明的故障模型内，进程/节点/可用区故障后仍能持久恢复；(c) 不存在对外可见的部分元组；(d) 客户端结果未知时可确定性对账，且不重复非幂等动作；(e) 发布意图与 Commit 耦合持久化，派发可安全重放。

Transaction/WAL Receipt MUST 标识 Transaction/Commit、Operation、规范 Memory 引用、Fence Generation、元组/证明引用及权威结果。普通成功响应、Queue ACK、Transport ACK 或独立写入的 Event 均不构成原子性证明。

除非 Storage 能提供可验证证据，证明完整六项元组已跨越经批准的持久化原子边界，否则 MUST NOT 声称 SuppressionCommitted。结果未知时标记 UNKNOWN，对读取/发布 fail closed，并针对权威持久化状态对账。不得从超时、进程完成、部分行集合或通知推断成功。语义触发点仍是成功持久化的 SuppressionCommitted；规范 MemoryLifecycle 在该点成为终态 Forgotten。I 授权是前置条件，不能替代 Storage Commit。D/I 治理完成与物理擦除仍是独立事实。

## 3. STOR-02 — 复制/故障切换期间 Fence 单调持久化

Storage MUST 在复制、故障切换、Leader 选举、副本提升、Restore 和灾难恢复期间，维护适用 ForgetFence Generation 的持久化单调高水位。

1. 每条权威写入/提升路径在成为权威或服务受保护读取前，MUST 与已提交高水位比较。
2. 若陈旧/滞后副本的 Fence Generation 低于最新已提交高水位，该副本 MUST NOT 成为权威。追平并完成对账前，必须保持非权威、受 Fence 约束或隔离状态。
3. 复制滞后 MUST NOT 降低、擦除、回滚已提交 Fence，也不得使 Fence 变成可选项。提升决策必须保留最大已提交 Generation，而不能只采用被提升副本本地观察值。
4. Generation 分配/提交 MUST 单调递增，并防止陈旧写入方或 Split-Brain 提交。冲突解决 MUST 永不选择较低 Generation。
5. Storage MUST 提供可验证的副本高水位观察记录，标识副本、观察到的 Generation、权威 Generation、观察时间和验证方法。观察缺失/不可用为 UNKNOWN，不是副本一致的证明。

任何流程均不得通过提升低于已提交 Fence 高水位的副本，恢复普通读取权威性。

## 4. STOR-03 — 抑制先行、可见性控制与读取 Fail Closed

抑制 MUST 在规范 Commit 边界生效，并先于异步物理擦除/去标识化。物理清理 Pending 不削弱抑制。

1. 每条读取、检索、派生、激活、交付、Index/Cache 服务及 Restore 可见性路径，在使受保护内容可观察前，MUST 查询权威当前 ForgetFence，或查询经明确批准且保证不会低于已提交高水位的等价机制。
2. 若服务路径无法查询/验证权威 Fence、无法确定新鲜度/高水位，或收到 UNKNOWN/超时/不一致状态，则 MUST 对受影响身份/Scope fail closed，或将该路径隔离出服务。MUST NOT 回退到陈旧本地副本/Cache，也不得假设 Fence 不存在。
3. 物理清理、副本收敛、备份到期或外部接收方工作仍 Pending 时，抑制必须持续有效。
4. Fence 前进时，Cache、Index、派生投影和 Publication Consumer MUST 丢弃/隔离陈旧内容。发布意图持久化不授权陈旧派发/重放；派发前必须重新检查当前 Fence。
5. SuppressionCommitted 不证明物理擦除。Storage 和各责任执行方必须使用逐副本证据分别报告物理擦除/去标识化。

## 5. STOR-04 — 备份集清单、保留与不确定状态

对于每个范围内 Backup Set，Storage/Backup MUST 维护持久化清单，至少标识：不可变 Backup Set ID 和 Snapshot/时间身份；覆盖范围（纳入或明确排除的系统、存储、区域、分片、副本、对象类别及时间/版本区间）；创建时间；到期时间；适用 Retention Policy/Version；适用加密/密钥、访问与 Restore 约束；Restore 顺序/依赖及必需 Fence/对账流程；清单完整性/来源、验证者和观察时间。

尚未达到经验证到期时间的 Backup **不属于已擦除**。除非策略和证据证明介质/对象已不可恢复，否则仅到期本身不构成逐副本擦除回执。任何 Retention Exception 仍须是可归属 I 决策，具有明确范围、控制和到期时间；本层不授予例外。

Backup Manifest 缺失、不可访问、不完整或无法认证时，其状态 MUST 记录为 UNKNOWN。清单缺失 MUST NOT 被解释为没有备份、没有副本、已到期或已擦除。若完成/合规声明依赖证明该覆盖范围，则未知备份覆盖阻止该声明。

## 6. STOR-05 — Restore 预检、隔离与对账

Restore 是潜在复活事件。在任何恢复副本、Snapshot、Replica 或派生状态变得可查询、可交付、可激活或以其他方式可见前，Storage/Backup MUST：

1. 将恢复目标/Snapshot 置于 quarantined、不可服务状态。任何必需 Manifest、Fence 状态或对账证据不可用时，隔离持续有效。
2. 获取并持久化应用最新权威 ForgetFence Generation/高水位，包括适用于恢复覆盖范围的全部 Tombstone。不得假定 Snapshot 内嵌 Fence 是最新的。
3. 枚举备份 Snapshot 时间点之后已提交的每个 Forget Operation，并逐项针对恢复覆盖范围对账：Operation 身份、规范 Memory 身份、Fence Generation、Commit 结果及受影响副本/目标。
4. 重新应用抑制/Tombstone，并使可能暴露已 Forgotten 身份的陈旧 Index、Cache、Projection、Publication Intent 或 Delivery 状态失效。
5. 使用负向 Query/Delivery 检查验证 Restore 后状态，并记录 Restore 预检/对账轨迹。
6. 仅在 Fence 应用和对账完成、证据持久化且责任 Storage/Backup 释放条件满足后，才可解除隔离。UNKNOWN、清单缺失、对账不完整或 Fence 服务不可用意味着继续隔离。

Restore MUST 使依赖已恢复覆盖范围的先前 D 完成/I 治理完成评估失效，直至对账完成且相关 Owner 重新评估。即使备份 Snapshot 早于 Forget Operation，Restore 也绝不得降低 Fence 或复活普通访问。

## 7. STOR-06 — 证据义务与状态

Storage/Backup 证据 MUST 只追加、完整性受保护、内容最小化，并可归属到精确 Operation、Fence Generation、目标/副本及执行版本。至少在适用时 MUST 包含：
- 证明六项元组原子持久化提交的 Transaction/WAL Commit Receipt；
- ForgetOperation 身份、幂等身份、Commit 结果和 Fence Generation；
- 相关副本及提升/故障切换边界上的副本高水位观察；
- 逐副本擦除/去标识化回执，含副本身份、动作、结果、验证者和可信观察时间；
- Backup Set Manifest、覆盖范围及经验证的到期/保留证明；
- Restore 预检及逐 Operation 对账轨迹，包括进入/解除隔离决策；
- Restore 后负向 Query 和 Delivery 测试证据。

每项证据 MUST 具有不可变引用/摘要、证据类别、Provenance、认证生产者/验证者、可信 observed_at、完整性保护，并绑定相关 Operation/Target/Fence。证据 MUST NOT 包含已 Forgotten 载荷，也不得成为未经授权保留的副本。

**证据状态：OPEN / NOT RUN / NOT PROVIDED。** 本规格不生成回执，也不声称已有事务证明、副本观察、擦除回执、备份清单、Restore 轨迹或负向测试结果。证据缺失为 UNKNOWN/NOT PROVIDED，不代表对应副本或风险不存在。

## 8. STOR-07 — 强制失败规则

以下规则保留《Owner Execution Boundary Contracts v1》§8：
- 无原子性证明：不得声称 SuppressionCommitted；结果保持 UNKNOWN/Blocked，直至权威对账完成，并 fail closed。
- 复制滞后：绝不降低/回滚 Fence；低于已提交高水位的副本不得成为服务权威。
- Restore：应用最新 Fence/高水位并对账所有 Snapshot 之后的 Forget Operation 前，Backup Restore 始终保持 Quarantined。
- 备份清单缺失：覆盖范围/状态标记 UNKNOWN，绝不标记 erased。
- Fence 查询不可用或陈旧：受影响读取/服务路径 fail closed 或隔离；不得使用陈旧回退路径。
- 元组部分提交或 Publication 失败：不得暴露部分成功；必须对权威事务和持久化 Outbox 意图对账。
- 提交后结果未知：不得盲目重放破坏性动作；先对账。已证明 Commit 始终保持 Forgotten，Fence 保持单调。

以上为强制失败约束，不是可自由裁量的建议。

## 9. 测试交叉引用与验证门禁

现有源测试 ID 仅作交叉引用；本层不复制、改名、改写或替代其场景/断言：
- DFI-021 — 原子抑制提交/故障切换：适用本层 §§2–3、§8；源 ID/原始断言仍以 R3 矩阵为准。
- DFI-022 — 最新 Fence 应用前 Backup Restore：适用本层 §§5–8；源 ID/原始断言仍以 R3 矩阵为准。
- DFI-012 — Forget 后 Backup Restore：适用本层 §6；源 ID/原始断言仍以 v2.1 交叉映射为准。

以上引用不构成执行证据。Storage/Backup 证据及可复现故障注入测试仍为 OPEN / NOT RUN。本文件不重新定义任何测试 ID。

## 10. Finding、批准与不作出的声明

- STOR-R3-001 — P1 — Issue #41 — SPECIFICATION_REMEDIATION_PROPOSED / PENDING_INDEPENDENT_REVIEW_AND_STORAGE_REASSESSMENT。§§2–8 明确规定六项原子提交元组、可执行 Storage/Backup 故障切换/读取/备份/恢复义务、失败规则及证据要求。
- 根据治理记录，v2.1 作为冻结的上游已批准层；本 Commit 不修改其文件或精确内容 SHA。
- D/I/Storage 对本 v2.2 精确内容 SHA 的批准：NOT CLAIMED。后续任何批准必须指向本层精确 SHA，并由相应权责方明确归属。
- 独立复审、Storage 重新审查、D/I 补充同 SHA 批准、集成审查、R3 可复现测试及故障注入证据均待完成。
- 不声称已有运行时实现、生产符合性、原子性证明、备份完整性、物理擦除、恢复安全、测试 PASS、Finding 关闭、合并或生产激活。

**AID-2026-001 总体状态继续为 BLOCKED_PENDING_R3_EVIDENCE。** 规格修复不等于批准、实现证据或测试证据。
