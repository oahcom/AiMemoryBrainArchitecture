# 验收矩阵——逻辑验收与物理验收分离（Issue #25 / #43）

- 工件 ID：ACCEPTANCE-LOGIC-PHYSICAL-001
- 版本：1.0.0
- 状态：PROPOSED / WAITING REVIEW
- 范围：为 Issue #25（D/E/I/Storage 原子 Producer Admission 与派生可见性）及 Issue #43（全系统架构收敛）补充统一验收治理。
- 关联契约与工作：RFC-IDE-001 v1.0.0（Draft PR #251）；可调用接口候选（PR #252）；A 架构实时源增量审查（PR #188）。
- 本工件不取代上述交付物，不批准任何 Owner 的领域语义，不选择物理拓扑，不授权实现，也不关闭任一 Issue。

## 1. 总原则

**逻辑验收与物理验收是两个独立门禁，必须分别记录。** 逻辑模型、文档评审、Schema 校验或参考模型 CI 通过，都不能证明已部署 Adapter、数据库、事务域、恢复流程或生产环境满足契约。

每项主张必须标注证据类别：
- DESIGN：仅提案/文档评审。
- OWNER-APPROVED：责任权威方明确批准，并固定精确工件版本。
- LOGICAL-TESTED：确定性模型/单元/属性测试；注明模型边界。
- PHYSICAL-TESTED：针对真实技术与配置的测试（SQLite 声称持久化/并发/崩溃能力时，必须使用真实文件数据库）。
- INTEGRATION-TESTED：使用实际 Adapter 与权威边界的跨模块测试。
- OPERATIONALLY-VERIFIED：目标环境中的部署、监控、备份/恢复、故障切换与运维证据。

不同证据类别不可互相替代。更高类别的测试也不能追溯性地批准其他 Owner 的领域语义。

## 2. 统一验收矩阵

| 门禁 | 验收对象 | 必需权威方/决策 Owner | 最低证据 | 不能证明什么 |
|---|---|---|---|---|
| L0 — 源基线 | 精确当前源文件与依赖版本 | A 协调；每个工件 Owner 确认自己的源 | Branch、Commit、路径、Blob SHA、回读时间、替代/时效状态 | 语义正确或已批准 |
| L1 — 逻辑契约 | Producer 身份、Scope、Key 命名空间、Digest/重放、Receipt 语义；领域类型与不变量 | Producer/领域身份权威（若治理分配则由 B 负责规范领域身份）；I 负责安全/Scope 授权；Event Store Owner 负责事件语义；A 仅做协调 | 按章节明确决策；中英一致；精确版本；列明未决候选 | 物理唯一性、授权强制执行、事务原子性 |
| L1 幂等入口 | RFC-IDE-001 v1.0.0 | Domain/Producer Identity 权威 + I/Scope Security 权威；Event Store Owner 确认消费义务 | 评审 PR #251；各权威记录 ACCEPT / ACCEPT_WITH_CONDITIONS / NEEDS_REVISION / REJECT；TTL 与清理仍为 CANDIDATE，直到策略决议 | SQLite Adapter 已经符合契约 |
| L2 — 逻辑组合 | 端到端状态机、线性化顺序、竞争结果、UNKNOWN 行为 | A 负责集成结论；D、E、I、Storage 分别决定自己负责的状态/操作语义 | 确定性参考模型测试：双向竞争顺序、崩溃切点、ACK 丢失、重复/重放、租约过期、撤权与依赖替换 | 真实 DB 隔离、持久性、崩溃恢复 |
| L3 — 协议契约 | 名义类型、Wire 字段、规范化、签名、版本与错误映射 | H 负责协议/Wire 决策；I 负责信任/安全策略；生产者/消费者 Owner 确认边界 | 精确 Schema/版本、正反向向量、签名与降级测试、独立 Owner 评审 | 运行时强制执行或持久提交 |
| P0 — 物理拓扑 | Producer Admission、Fence、授权、依赖注册及可见性的真实串行化/事务 Owner 与一致性域 | Storage/Consistency Owner 决定存储拓扑；D/I/E 负责各自权威侧 Participant 行为；A 不得代替选择 | 已选拓扑、权威边界、事务/Participant 协议、部署假设及 Owner 批准 | 仅凭拓扑图证明正确性 |
| P1 — 物理原子性 | Event/Receipt 与隐藏 Participant/可见性提交边界 | Storage 实现 Owner 负责 DB 原子性；Event Store Owner 负责 Event+Receipt 事务；D/I 负责 Participant 接受与终态证明 | 真实文件 DB/真实 Adapter 测试；事务回滚；唯一性/CAS；持久化配置；独立连接并发；无部分可见状态 | 故障切换/恢复正确性 |
| P2 — 物理恢复 | 崩溃、重启、故障切换、恢复、UNKNOWN 协调、陈旧副本与脑裂防护 | Storage/Consistency Owner 负责恢复底座；D/I 负责自身持久账本与当前性证明；运维负责操作流程 | 每个持久边界故障注入；重启/协调；备份恢复与故障切换演练；精确 CI Run ID 和环境配置 | 没有目标环境运维证据时的生产就绪 |
| P3 — 集成一致性 | D→E→I→Storage→F/G 消费者使用精确已提交工件与权威证明 | 每个生产者/消费者 Owner 签署自己的契约；A 记录跨 Owner 集成结论 | 真实 Adapter 间测试；替换/重放/跨 Scope 测试；受保护边界的当前授权/Fence 检查；完整依赖集 | 不能从 A 报告推断独立 Owner 批准 |
| P4 — 运行验收 | 生产部署、监控、保留、密钥生命周期、备份、事件响应 | 指定运维/服务 Owner；适用时由 I/安全/隐私/法务权威批准 | Runbook、SLO/告警、恢复证据、保留/法律保全策略、安全批准、部署签署 | 逻辑阻塞仍存在时的架构冻结 |
| F — 冻结结论 | 架构就绪度 | A 发布建议；各权威保留本领域否决权；项目治理权威批准项目级冻结 | G1–G8 证据账本；所有 P0/P1 风险已证明或明确列为阻塞；双语一致性 | 未经单独授权的部署权限 |

## 3. Owner 决策权与验证责任

| Owner | 决策权（仅限所属领域） | 逻辑验收责任 | 物理/一致性责任 |
|---|---|---|---|
| A — Integration | 仅负责跨模块组合与集成结论；不能批准 B–I 或 Storage 语义 | 维护源/证据账本、依赖图、矛盾、跨 Owner 验收矩阵；发布集成结论 | 协调端到端一致性证据；不得替其他 Owner 自我认证物理系统 |
| B — Domain Model | 规范领域对象与名义身份语义；若项目治理分配，则包含规范 ProducerIdentity 类型 | 批准类型化身份相等、领域引用与规范对象语义 | 提供序列化往返和领域不变量测试；不批准存储持久性 |
| C — Agent / Inference | 推理边界、请求/Agent 身份及 C 自有遥测语义 | 批准 C 自有输入/输出与信任边界 | 验证 C 范围内真实 Adapter/Provider 边界与证据采集 |
| D — Memory Brain | Canonical Memory 权威、ProducerWork Admission、ForgetFence、Lineage 与 D 终态化 | 批准 D Participant 生命周期、Admission/Fence 语义与 D 状态转换 | 使用实际实现证明 D 持久账本、Fence/当前性检查、竞争及恢复行为 |
| E — Memory Compiler | Compiler 入口、Staging、Lineage、依赖完整性与发布编排 | 批准 E Queue/Lease/Run/Derivation 与私有 Staging 语义 | 证明先注册后工作、依赖注册、陈旧租约、重试及发布集成 |
| F — Memory Runtime | Retrieval/Index/Cache 消费及最终抑制 | 批准 F 消费规则：只消费精确已提交/已发布工件，并检查当前授权/Fence | 使用真实 Store 测试索引/重建/回填/重放与披露抑制 |
| G — Memory Context | Context 版本、交付/移除及 Applied 证据 | 批准 G 自有 Context/Delivery/Applied 状态语义 | 证明 G 边界内真实交付/移除/协调及证据持久性 |
| H — BMCP Protocol | Wire Schema、名义 Wire 类型、规范编码、版本协商与协议错误词汇 | 批准协议契约与互操作向量 | 执行跨实现序列化/签名/互操作测试；不拥有 I 的信任策略 |
| I — Security Governance | Principal/Permission/Scope/PolicyDomain、撤权、密钥信任、保留与安全策略 | 批准授权语义、当前性与受保护边界要求 | 证明真实 Issuer/Key/Policy/Registry/PermissionEpoch 强制执行、撤权竞争、历史验证与审计证据 |
| Storage / Consistency | 物理事务拓扑、数据库一致性域、持久 Participant 账本、可见性串行化与恢复底座 | 确认逻辑协议可物理实现；不得重新定义 D/I/E 语义 | 负责真实 DB/Adapter 事务、持久性、崩溃、故障切换、恢复、脑裂及物理一致性证据 |
| Event Store / SQLite Adapter | Event Store 边界内的事件追加与 Receipt 存储契约 | 确认 RFC-IDE-001 与 Event/Receipt 逻辑原子性要求 | 证明文件型 SQLite 事务原子性、持久唯一性/CAS、重启重放/冲突及清理安全 |

Owner 边界不得根据职称或分支名称推断。如果项目治理尚未正式指定权威方，该行必须标记为 **AUTHORITY UNCONFIRMED / BLOCKING** 并取得明确指定。协调者、实现者或评审者不得代替其他权威签署。

## 4. Issue #25 的具体应用

验收链必须拆成独立证明：

1. **L1 契约：** D 的 Admission/Fence/Lineage 语义；E 的 register-before-queue/lease/run 与完整依赖语义；I 的当前授权和终态证明；Storage 的可见性 Participant 语义。RFC-IDE-001 v1.0.0 是 ProducerIdentity/Scope/Key 幂等入口契约。PR #251 是评审入口；PR #252 消费它，不能替代对它的批准。
2. **L2 组合：** 保持当前提出的崩溃安全顺序：Storage 先持久化隐藏 Participant → D 的 PublicationParticipantRef 绑定该 Participant → I 消费单次 CommitAuthorizationReceipt → Storage 最终可见性提交校验当前 D Fence/Participant 与精确 I 终态证明 → 仅在 COMMITTED_VISIBLE 或已证明 NO_PUBLICATION 后 D/I 才关闭。UNKNOWN 必须保持工件私有且 Barrier 开启。
3. **P0/P1：** Storage Owner 必须选择并批准物理串行化/事务拓扑。证明可见性不会越过 D Fence 安装或 I 撤权，并且 Participant、授权证明和可见性 Receipt 不可被替换。
4. **P2/P3：** 使用真实 Adapter 测试每个持久边界前后崩溃、ACK 丢失、相同/不同 Digest 重试、Scope 隔离、独立连接竞争、重启、故障切换/恢复及完整依赖集。
5. **退出条件：** 在精确 Owner 决策与物理/集成证据入账前，Issue #25 保持 OPEN。PR #252 的文档门禁成功仅是文档证据，不是实现一致性。

## 5. Issue #43 的具体应用

对 A–I 与 Storage 的每条关键路径采用相同分层：
- G1：精确实时源版本与时效性；
- G2：权威方/消费者验收矩阵，不推断批准；
- G3：无矛盾的端到端逻辑模型，或明确标记阻塞冲突；
- G4：P0/P1 竞争、崩溃、恢复、身份与信任证明；
- G5：技术/拓扑可行性具备责任决策与可复现证据；
- G6：中英双语一致；
- G7：A 集成结论与独立 Owner 决策并存；
- G8：明确 READY / READY WITH ENUMERATED BLOCKERS / NOT READY。

本矩阵不能关闭 Issue #43，也不能替代完整 G1–G8 报告。PR #188 的有限实时源增量审查不是完整验收报告。只要关键物理拓扑、信任、Forget/Restore 和独立 Owner 证据仍未证明，就必须维持 NOT READY。

## 6. 当前证据账本与时效说明

| 项目 | 当前已知状态 | 分类/用途 |
|---|---|---|
| RFC-IDE-001 PR #251 | Draft/Open；HEAD de0dfd157769aac67f28437a918fd1cbc0899f24；双语门禁 Run 44264890385 SUCCESS | 仅文档 CI；L1 评审入口，不是 Owner 批准 |
| 可调用接口 PR #252 | Draft/Open；HEAD f34d89d56a607eb2e321b41c73824f8765fe12d2；GOV-DOC-001 Run 44271607842 SUCCESS | 逻辑接口/文档候选；不是 Schema 冻结或物理一致性 |
| A 实时源增量 PR #188 | Issue #43 记录了 Draft、源 Commit/报告版本；该工作流明确未运行 | 有限集成审查；不是完整 G1–G8 |
| PR #248/#249/#250 | 刷新交接信息称为 Open 且 mergeable=clean | 使用前仍须刷新精确 Head、评审与检查；mergeable 不等于验收 |
| Issue #25 | Open；最新 Issue 活动包含 PR #252 文档门禁成功；Owner 决策与物理拓扑仍开放 | D/E/I/Storage 主验收线 |
| Issue #43 | Open；最近引用的 A 报告仍是明确不完整的有限增量 | 全系统收敛与冻结门禁 |

OPEN、mergeable、文档 CI 绿色或参考模型测试通过，都不是决策或物理验收。后续作出结论前，必须刷新精确 PR Head、精确 Head CI Run ID、Review 状态与 Owner 分支 Head。用户提供的刷新事实先作为交接输入，除非独立刷新，否则不冒充本轮实测。

## 7. 必需决策记录格式

每项 Owner 决策必须包括：
- 决策：ACCEPT / ACCEPT_WITH_CONDITIONS / NEEDS_REVISION / REJECT / CANDIDATE_NO_APPROVAL；
- 精确工件 Branch、Commit、Path、Blob SHA 与版本；
- 接受/拒绝的章节和字段，以及规范替换文本；
- 阻塞与非阻塞发现；
- 测试及证据类别、精确 Commit SHA 与 CI Run ID（或明确写明未运行）；
- 声称物理能力时的环境/配置与故障覆盖；
- 需要确认的下游消费者；
- 批准者身份及其决策权证据。

没有回复、文件存在、PR 可合并，或另一个 Owner 的角色模拟，都不构成验收。

## 8. 后续行动与退出条件

1. 取得 B/领域身份与 I/Scope 安全方对 RFC-IDE-001 的明确评审；TTL 与回收在策略证据形成前保持 CANDIDATE。
2. 取得 D、E、I、Storage 对 Issue #25 Phase 3.8 精确源版本的逐节决策；H 评审 Wire 名义类型与规范化。
3. 要求 Storage 发布已选择的物理拓扑，以及可复现的真实 Adapter 事务/恢复证据。
4. 要求 D/I/E 在每个受保护边界提供物理 Participant 与当前性证据。
5. 对齐 F/G 消费者及真实索引/Context 交付行为。
6. 将精确证据输入 Issue #43 G1–G8；A 发布集成结论，但不替代 Owner 批准。

在上述条件满足前，两个 Issue 均保持 OPEN；架构冻结与生产激活均 NOT AUTHORIZED。
