# R — 全系统架构风险评估与根本风险登记册

- Review ID：SYS-RISK-001；日期：2026-11-17
- 仓库：oahcom/AiMemoryBrainArchitecture
- main 基线：b372b62c640a2b656e54b6db62a4ee67d7d8c001
- 审查分支：review/session-1-system-wide-risk-2026-11-17
- 状态：**NOT READY FOR ARCHITECTURE FREEZE；候选评估稿，等待独立复审**
- 本文件为中文稿；同目录英文稿为语义对等版本。

## 1. 执行结论

**总体结论：NOT READY（不具备架构冻结条件）。**

项目已形成合理的逻辑分工：Canonical Memory 与派生索引/Context 分离；D 管理 Canonical Memory、Lineage 与 ForgetFence；I 管理身份、授权、撤权和 Global Forget 治理；C 管理 Provider 副作用事实；H 管理协议/Wire；Storage 管理持久化、事务、可见性与恢复。但责任被写明不代表这些边界在竞争、崩溃、恢复和重试时可组合。

根本问题不是缺少模块文档，而是：
1. 核心领域语义仍有 ADR-BLOCKED，canonical identity 和下游契约不能冻结。
2. 最终可见性与 ForgetFence 的共同线性化基础尚未选定。
3. 发布、遗忘、恢复跨越多个独立权威，缺少完整端到端竞争/崩溃证明。
4. Applied、Provider Outcome、Owner Admission、Storage Outcome、COC Recovery Evidence 是不同事实，尚未形成无歧义的精确版本绑定完成证明。
5. Owner 候选持续演进，版本清单和消费者采用关系必须持续重新验证。
6. 治理与候选协议复杂度已显著增长；若无可执行参考模型、明确决策权和冻结门禁，治理本身可能吞噬工程能力。

**评级依据：** Critical 表示可能直接破坏核心正确性不变量或阻止架构冻结；High 表示造成跨模块行为不确定、重大返工或生产 Gate 无法通过；Medium 表示主要影响演进/运维/成本且可在明确门禁下延后；Low 表示隔离明确、近期影响受控。本轮不把“尚无生产实现”本身视为架构缺陷。

## 2. 审查基线与精确证据

### 2.1 Owner 分支 HEAD 快照

| Owner | 分支 | 本轮读取 HEAD |
|---|---|---|
| main | main | b372b62c640a2b656e54b6db62a4ee67d7d8c001 |
| B | session-b-domain-model-phase3 | 0df144ae25c2039c9934395fc88b2d17080eb119 |
| C | session-c-agent-integration-2026-11-16 | f3251081c49e697fe4739a252e27f59e2ecd0a8f |
| D | session-d-memory-brain-2026-11-16 | 97e68fbd225bdf0ac71860c01077481afc162d50 |
| E | session-e-memory-compiler-2026-11-16 | fdb4f67a83083d995930b88f93975b5ee36080f3 |
| F | session-f-memory-runtime | 8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3 |
| G | session-g-memory-context | f9ca0ddc36e17f74041506f17039f0202d13042e |
| H | session-h-bmcp-protocol | f809be092a6c04db7982cc1bdbdd9c88787a4286 |
| I | session-i-security-governance-2026-11-16 | 28df608b075e619563c6367a8a1c171185c1faaf |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 17be31915b06d98d7f822e6e5270b8cde39eb0bb |

这些是本轮读取到的分支快照，不代表已合并到 main，也不代表 Owner 已接受其他 Owner 的精确版本。分支后续变化将使相关证据需要刷新。

### 2.2 关键源文件

| 主题 | 精确源（分支 HEAD / Path / Blob SHA） | 已验证状态 |
|---|---|---|
| Fact/Claim | B / 0df144ae25c2039c9934395fc88b2d17080eb119 / 02-domain-model/ADR-001-fact-claim-semantics.md / a1024938ff5baba069cf128c69496a44e143330c | VERIFIED：ADR-BLOCKED；无正式决策主体、批准人和决议时间 |
| D Publication | D / 97e68fbd225bdf0ac71860c01077481afc162d50 / 03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md / 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 | VERIFIED：D-role proposal；Owner approval/API/conformance OPEN |
| E Orchestration | E / fdb4f67a83083d995930b88f93975b5ee36080f3 / 04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md / 475fee41e5eea527af4edefbfe88c58c86967d0a | VERIFIED：跨 Owner API、批准和符合性 OPEN |
| F Lifecycle/Restore | F / 8d5ef89ce9b1ff1471ffd1a03fe4f289addb0af3 / 05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md / 29e9504c75d737c2dd200ebc3306eda555f0b0ac | VERIFIED：本地语义提案；跨 Owner 接口/实现未验证 |
| G Context/Applied | G / f9ca0ddc36e17f74041506f17039f0202d13042e / 06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md / c1de241ec69834377d9b0e24aa4770a809796d4b | VERIFIED：本地提案；C/G/H 交付和跨 Owner 接口 OPEN |
| H Unified 1.2.13 | H / f809be092a6c04db7982cc1bdbdd9c88787a4286 / 08-bmcp-protocol/phase-3.8.9-h-exact-mapping-unified-1.2.13-c-submit-outcome-1.0.1.md / 32bf9b0fd42abe8b58749b858b1d5c9aef39c5fd | VERIFIED：候选映射；exact CI rerun required；not frozen |
| I P0 Allowlist | I / 28df608b075e619563c6367a8a1c171185c1faaf / 09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md / 5c0e2049513d391dfc118f4f629a5ec95de456d6 | VERIFIED：P0 投影候选；生产 Profile/信任根/密钥运维未批准 |
| Storage Topology ADR | Storage / 17be31915b06d98d7f822e6e5270b8cde39eb0bb / reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md / 1ef47d4e5711c7db73a24d249adf1992be1f6aa4 | VERIFIED：ADR-BLOCKED；无部署拓扑选定 |
| Storage v3.2.5 Manifest | Storage / 同上 / reviews/storage-consistency/phase-3.6.15-storage-v3.2.5-protocol-bundle-exact-version-manifest.md / bea90697e7a61d43bed00543d636a5cdf40cf5ca | VERIFIED：successor bundle published；not jointly accepted/not frozen |
| Storage Visibility | Storage / 同上 / reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md / 175ee7b1349cfdb79a19898b311a88391ed88010 | VERIFIED：逻辑事务提案；物理拓扑和实现证明 OPEN |

**状态词汇：**
- VERIFIED：精确文件/证据已读取或文件明确记载该状态；不代表机制正确性已证明。
- PARTIALLY VERIFIED：有局部候选、CI 或模型证据，但缺端到端覆盖、Owner 批准或真实拓扑绑定。
- NOT PROVEN：主张的性质没有充分可复核证明。
- BLOCKED：明确 ADR、Owner 决策或 Gate 前置条件未满足。

## 3. System-wide Risk Register

概率为 High/Medium/Low，评级理由写在括号中；严重度与风险等级分开评估。

| ID / 风险 | 描述、根因、影响组件与失败后果 | 概率 / 严重度 / 等级 | 触发条件 | 缓解、所需决策、责任 Owner | 验证证据、残余风险、Blocking Gate |
|---|---|---|---|---|---|
| R-01 领域语义与 Canonical Identity 未闭环 | B Fact/Claim ADR 未决；Identity、Scope、Actor/Principal、Environment 类型若未统一，D/E/F/G/H 会对同一对象产生不同解释，导致错误合并、授权、保留/遗忘或错误 Schema。影响 B/D/E/F/G/H/I。 | High（ADR 明确阻塞且消费者等待）/ Critical / **Critical** | 冻结 canonical Fact/Claim Schema、API、索引或跨模块引用前 | B 提交选项与消费者映射；正式治理主体作出 Fact/Claim 决议；B/I/H/D 固定名义类型、身份来源、Scope 代数和 unknown 规则。Owner：B + Architecture Governance；I/H/D 审查消费者影响。 | B Blob a1024938…143330c 明确无批准主体/决议。关闭：正式 ADR、命名批准人、下游映射和反例测试。残余：新类型迁移。Gate：G2/G3 BLOCKED。 |
| R-02 ForgetFence 与最终可见性没有共同序列化基础 | D Fence/Lineage 与 Storage Visibility Commit 若无共同原子事务域或等价线性化协调器，check-then-write 竞态会导致遗忘后重新发布、未授权内容可见或 Barrier 错误关闭。影响 D/Storage/E/F/G/I。 | High（Storage ADR 明确无拓扑）/ Critical / **Critical** | 并发发布与 Forget、故障切换、跨服务写入、恢复 | 选择可证明拓扑：每个 Canonical Authority 一个 Serializable Transaction Domain，或具备线性化与持久参与者账本的协调器；明确 D 行边界、Storage 最终提交点、I Proof 验证点。Owner：Storage（物理机制）+ D（Fence）+ I（授权）。 | Storage ADR Blob 1ef47d…f6aa4 为 ADR-BLOCKED；Visibility Blob 175ee7…8010 仅逻辑提案。关闭：拓扑 ADR、双序列竞态、崩溃/丢 ACK/Failover 验证。残余：部署故障域。Gate：G3/G4/G5 BLOCKED。 |
| R-03 Forget/Revocation/Restore 反复活缺少端到端证明 | Forget 完成依赖 Producer、Attempt、Derivative、Queue、Retry、DLQ、Outbox、Index、Context、Adapter、Backup/Restore 的闭世界清点。任一延迟工作或旧快照遗漏，都可能在完成后重新暴露数据。影响 D/I/E/F/G/H/C/Storage/COC。 | High（多份 Owner 文档仍将端到端接口/证明标 OPEN）/ Critical / **Critical** | Forget 与派生、重试、离线 Adapter、索引重建、恢复或回滚并发 | D 定义 FenceGeneration、ProducerWork/Lineage/Barrier 终态；I 定义全局清点与残留策略；E/F/G/H/C/Storage 提供成员和当前性证据。任何 UNKNOWN、inventory gap、stale high-water 都阻止完成和恢复服务。Owner：D + I；执行 Owner 各自维护账本。 | D Blob 17e538…55ac78、F Blob 29e950…f0b0ac、G Blob c1de24…796d4b 均为 proposal/OPEN。关闭：Forget-vs-publish/replay/restore/offline reconnect/late derivative 矩阵和恢复后反复活负测。残余：第三方副本/法律保留。Gate：G4 BLOCKED。 |
| R-04 跨 Owner 发布状态机与 COC/JF-10 组合未证明 | Prepare→Admission→Authorization→Visibility→Closeout 可描述，但 Participant 身份、持久顺序、COC Recovery Cutoff、JF-10 Prepared Participant 是不同协议域。误把它们视为一个协调器，或用单方 ACK 推导终态，会导致重复提交、孤儿参与者、错误 Abort 或永不关闭。影响 D/E/H/I/Storage/COC/A。 | High（合同标 proposal、exact review/conformance OPEN）/ Critical / **Critical** | Prepare 后崩溃、D Admission 丢 ACK、I 决策/撤权竞争、Storage 提交响应丢失、COC 恢复期间新请求 | 固定各协议 authority、稳定 Participant/GID、tuple digest、单次消费证明、终态与 UNKNOWN 规则。COC 只记录顺序/参与者证据，不替代 I/D/C 决策；JF-10 独立。Owner：Storage/I/D/H；E/A 集成。 | D/E/Storage 当前 Blob 如上；Storage v3.2.5 清单未联合接受。关闭：同一 exact bundle 的双序列、崩溃点、丢 ACK、重复/变更 digest、恢复截断及恢复期间新请求测试。残余：协调服务运维故障。Gate：G3/G4 BLOCKED。 |
| R-05 Applied 与 Provider Outcome 证据语义可能混淆 | G Applied 只证明特定 Context/请求谓词；C Provider Outcome 证明 Provider 副作用；H 运输/验证协议证据。Transport ACK、Adapter ACK、Provider 拒绝标签、模型实际使用 Context 并非同一事实。缺证或版本错配被解释为成功，会造成虚假审计和重复副作用。影响 C/G/H/I/D/Storage。 | Medium-High（边界已定义但最新映射 Candidate、exact CI 未重跑）/ Critical / **High** | 请求重试、重定向/Failover、晚到 ACK、旧 ContextVersion、Provider 可能已收到但结果未知 | 冻结 CSubmitOutcome 1.0.1 ↔ H Unified 1.2.13 exact mapping、C sequence namespace、签名投影与 Owner Outcome 解引用；Applied 保持 G 自身谓词。UNKNOWN/IN_DOUBT 不得变成功或安全重试。Owner：C（Provider Truth）、G（Applied）、H（Wire）、I（信任）。 | H Blob 32bf9b…c5fd 明确 Candidate/exact CI rerun required/not frozen；G Blob c1de24…796d4b 标接口 OPEN。关闭：当前 HEAD exact-schema CI、跨 Owner 负向语义向量、最终发送边界 conformance。残余：Provider 不可观测副作用。Gate：G2/G4 BLOCKED。 |
| R-06 身份、授权、Scope 与密码学边界未闭环 | Principal/Actor/Workload/Environment/PolicyDomain、PermissionEpoch、KeyStatus、Issuer/Audience、anti-rollback 必须独立验证。缓存 ALLOW、历史签名、错误 audience 或跨域计数器比较可能越权。Multi-PolicyDomain 原子性不能从单域 PermissionEpoch 推导。影响 I/B/H/C/D/F/G/Storage。 | Medium-High（P0 投影改进，但生产信任根/密钥治理及多域决策开放）/ Critical / **High** | 密钥轮换/撤销、PolicyDomain 并发、旧快照恢复、跨 Scope 查询、签名字段变化 | I 保持唯一授权/撤权权威；逐消息族固定签名投影、issuer/audience/profile/key status；各域高水位仅本域比较。跨域原子语义另立 ADR，不拼接本地 Epoch。Owner：I；H/C/D/B 为消费者。 | I Blob 5c0e204…d456d6 明确生产 Profile、Key custody、外部 anti-rollback 和完整 P0 vectors 仍开放。关闭：精确 P0 双实现、负向篡改矩阵、撤权/恢复测试、PolicyDomain ADR。残余：供应链/密钥运维。Gate：G4/G5 BLOCKED。 |
| R-07 精确版本与证据新鲜度漂移 | Owner 分支演进；任一 Schema、Validator、Manifest、Consumer Mapping Blob 改变，旧接受/CI 不再证明新组合。路径/分支名不能代替 Blob pin；角色模拟不等于独立 Owner 批准。影响 A–I/Storage/CI。 | High（本轮观察到 successor bundle 和 exact rerun 缺口）/ High / **High** | Owner 修改 Schema、签名投影、错误码、状态机或 Manifest，消费者仍用旧 pin | 自动化证据账本：branch HEAD、commit、path、Blob、consumer pin、批准人、test run/head SHA、supersedes；Blob 改变自动使受影响审查失效。Owner：A 维护集成账本，各 Owner 签署自身规范。 | C/H/I/Storage 精确源显示多个候选版本；H 要求 exact CI rerun。关闭：完整消费者矩阵、批准来源、当前 HEAD 读回、双语 parity。残余：并行更新短暂窗口。Gate：G1/G2 BLOCKED。 |
| R-08 Cursor/Revision/Receipt/Manifest 跨域混用 | 各 Owner 序号、epoch、watermark、generation、cursor 属于不同权威域。合并为 scalar high-water、跨域比较数字或把缺失记录解释为无副作用，会在恢复时丢撤权/Forget/Provider 结果。影响 B/C/D/E/F/G/H/I/COC/Storage。 | Medium-High（F/G/I/H 明确独立水位，系统证明未闭合）/ Critical / **High** | PITR、快照回滚、日志部分缺失、跨域恢复批次、索引缺口、KeyStatus 不可用 | 每个水位绑定 issuer/domain/epoch/digest/continuity proof；恢复采用合取 Manifest，逐域核验；禁止跨域数值比较；gap/truncation/unknown 保持 quarantine。Owner：各 Owner 管本域账本；Storage/COC 管物理/顺序证据；A 集成。 | F Blob 29e950…f0b0ac 明确 IndexWatermark 为 partition-local、零命中不是删除证明；I Blob 5c0e…d456d6 要求独立 anti-rollback。关闭：恢复依赖 DAG、rollback/partial-prefix 对抗测试、逐域证明完整性。残余：外部锚点不可用导致停服。Gate：G4/G5 BLOCKED。 |
| R-09 治理复杂度可能超过工程收益 | 多 Owner、多版本、receipts/manifests/proofs、多层 Gate 持续增加协调成本。若没有可运行参考模型、决策期限和弃用策略，团队可能维护治理工件而非交付可验证系统；实现出现重复状态机和运维不透明。影响全系统；主要责任 A + Architecture Governance。 | Medium-High（候选协议、角色模拟审查、exact pin 快速增长）/ High / **High** | 同语义多协议表达、每次修订都需大量人工映射、无决策期限、Gate 依赖链无限延长 | 每个新 proof/field 说明独立失效模式、不可替代性和最小消费者集合；建立可运行状态机/故障模型；Candidate 设置到期日、冻结条件、弃用策略。保留必要权威分离，不为简化而合并语义。Owner：A + Architecture Governance；各 Owner 管复杂度预算。 | Issue #43 范围与协议证明显示治理工作量大，但无工时/吞吐数据。本风险 PARTIALLY VERIFIED，不宣称净收益已为负。关闭：工程估算、关键路径模型、最小端到端切片、复杂度/收益审查。残余：需求变化。Gate：G5/G8。 |
| R-10 生产部署与灾难恢复可运行性未形成方案 | 技术蓝图仍 Candidate；Storage 未选 DB/Coordinator/故障域/RPO/RTO/KMS/HSM/备份/on-call/SLO。逻辑协议若无法映射可操作持久化与恢复架构，系统无法安全上线或恢复。影响 Storage/I/A/所有运行模块。 | Medium（设计阶段可延后，生产前不可缺）/ Critical / **High** | 工程/部署评审、服务边界确定、区域或数据库故障 | 保持架构阶段与工程阶段分离；工程前指定 Canonical Authority、事务域、Coordinator、故障域、备份恢复、密钥责任；定义 RPO/RTO/SLO、演练、Runbook、生产 Gate。Owner：Storage + I + 指定 Engineering/Operations Owner；A 集成。 | Storage ADR Blob 1ef47d…f6aa4 的 T1–T8 均 OPEN；Issue #43 称 TAB-001 Candidate。关闭：批准技术蓝图/拓扑 ADR/恢复演练/运维责任签署。残余：云/供应商区域故障。Gate：G5/G8 BLOCKED。 |

## 4. 根本性排序

1. **R-01 领域语义与身份基础**：无稳定身份和语义，无法定义持久化、授权、索引正确性。
2. **R-02 ForgetFence 与 Visibility 共同线性化**：决定写入与遗忘能否同时正确。
3. **R-03 Forget/Revocation/Restore 反复活**：决定遗忘是否真实、可证明且可安全恢复。
4. **R-04 跨 Owner 发布与恢复状态机**：决定多模块能否形成单一事务语义。
5. **R-06 身份与授权信任边界**：决定受保护数据能否由正确主体在正确目的/环境访问。
6. **R-05 Applied 与 Provider Outcome**：决定外部副作用和 Context 交付能否被证明。
7. **R-08 跨域 Cursor/Manifest/Recovery**：决定恢复不会复活撤销或丢失已提交事实。
8. **R-07 版本与证据新鲜度**：决定 PASS 是否对应当前架构。
9. **R-10 生产可运行性**：决定逻辑保证能否在真实拓扑维持。
10. **R-09 治理复杂度**：决定工程组织能否持续交付，而非被协议负担吞噬。

## 5. 核心问题 A–I 的正式回答

**A. 最根本的十项风险：** R-01 至 R-10；它们构成语义、线性化、遗忘、跨 Owner 事务、信任、证据、恢复、版本、部署和治理依赖链。

**B. 哪些使系统正确性无法成立：** R-01/R-02/R-03/R-04 是直接根风险；R-06/R-08 会破坏安全和恢复正确性。未关闭前不能声称系统正确性已证明。

**C. 未闭环决策：** Fact/Claim ADR；D/Storage 最终可见性拓扑；D/I/E/Storage Publication 参与者/终态组合；CSubmitOutcome 1.0.1 与 H Unified 1.2.13 冻结映射和 exact CI；I 生产密码学 Profile/信任根/密钥生命周期/anti-rollback；Multi-PolicyDomain 原子性；Global Forget 闭世界清点和残留策略；技术蓝图/部署拓扑/RPO/RTO/SLO/运维责任。

**D. 集成时放大：** R-02/R-03/R-04/R-05/R-06/R-08。局部 UNKNOWN、receipt、watermark 或终态被下游过度解释，会形成组合错误。

**E. 现在不处理会重大返工：** R-01/R-02/R-04/R-05/R-06/R-08，影响核心 Schema、事务边界、错误模型、重试、索引/Context 版本、审计和恢复协议。

**F. 直接阻止未来生产：** R-02/R-03/R-04/R-06/R-08/R-10，尤其拓扑未选、Forget/Restore 未证明、授权/anti-rollback 和运维恢复方案未闭环。

**G. 看似安全但缺少证明：**
- UNKNOWN 保持私有，若未强制覆盖 Read Path、Cache、Index、Object URL、Adapter 和 Restore 路径，只是策略声明。
- Pointer + Receipt + Outbox 原子提交，若未绑定真实事务域、读取路径和崩溃恢复，不能证明可见性原子性。
- Signature + allowlist，若没有当前 KeyStatus、Issuer/Audience、撤销和 anti-rollback，不能证明授权仍有效。
- RecoveryJoin/Manifest，若无完整 Owner Ledger、Prefix Continuity 和独立高水位核验，不能证明恢复闭包。
- Applied 若未绑定精确请求、ContextVersion、Provider Outcome 和当前授权，不能证明实际行为。

**H. 多模块分别正确但组合错误：**
1. D Fence 与 Storage Visibility 各自正确，但无共同线性化点会产生 Forget/Publish 竞态。
2. I PermissionEpoch 与 D FenceGeneration 各自正确，但不能跨域数值比较或互相替代。
3. H Wire ACK 不等于 G Context Applied。
4. C Provider Outcome 不等于 G Applied。
5. COC Recovery Cutoff 不等于 JF-10 Participant Bridge；COC 不是 JF-10 Coordinator，也不能签发 I/D 决议。
6. F IndexWatermark 不是 D Producer high-water，也不是 Forget 完成证明。

**I. 治理复杂度是否可能超过工程收益：** 存在风险，但尚未证明已出现净负收益。身份、签名投影、Manifest、Participant Receipt、Owner Gate 和精确 pin 增加正确性成本，也增加验证/运维成本。必须通过可运行参考模型、端到端切片、工程估算和故障覆盖证明收益；不能为简化而删除必要权威边界，也不能无预算增长协议复杂度。

## 6. 风险依赖关系

~~~mermaid
flowchart TD
 R1[R-01 Domain semantics / identity]
 R2[R-02 Shared serialization / visibility]
 R6[R-06 Identity and authorization]
 R4[R-04 Cross-owner publication state machine]
 R3[R-03 Forget / revocation / restore]
 R5[R-05 Applied / Provider Outcome]
 R8[R-08 Cursor / manifest / recovery]
 R7[R-07 Exact-version freshness]
 R10[R-10 Production operability]
 R9[R-09 Governance complexity]
 R1 --> R2
 R1 --> R4
 R1 --> R6
 R2 --> R3
 R2 --> R4
 R6 --> R3
 R6 --> R4
 R4 --> R5
 R3 --> R8
 R4 --> R8
 R7 --> R4
 R7 --> R5
 R8 --> R10
 R2 --> R10
 R9 -. amplifies .-> R7
 R9 -. amplifies .-> R4
~~~

R-01 是下游类型/引用/授权语义前置；R-02/R-06 是发布遗忘竞态和授权 Gate 前置；R-03/R-04 决定可审计终态；R-05 证明 Agent/Provider 边界外部结果；R-08 把各权威持久状态带入恢复；R-10 决定逻辑保证能否在真实拓扑维持；R-07 横向影响证据有效性；R-09 放大证据治理成本与集成延迟。

## 7. 未决架构决策

| ID | 决策 | 权威 Owner | 当前状态 | 权限边界 |
|---|---|---|---|---|
| UAD-01 | Fact/Claim canonical semantics、身份与修订模型 | Architecture Governance；B 提案 | ADR-BLOCKED | R 不替 B/治理主体选项 |
| UAD-02 | D Fence 与 Storage Visibility 共同序列化拓扑 | D + Storage；I 审查授权提交点 | ADR-BLOCKED | R 不定义 D Fence 或替 Storage 选 DB |
| UAD-03 | JF-10 Prepared Participant 精确绑定与终态 | I + Storage；H 管 Wire | OPEN / exact review | COC 不能成为 JF-10 Coordinator |
| UAD-04 | Global Forget inventory、外部副本/备份与完成策略 | I（治理）+ D（Lineage/Fence） | OPEN / BLOCKED | R 不批准外部删除/法律保留策略 |
| UAD-05 | CSubmitOutcome 1.0.1 ↔ H Unified 1.2.13 冻结映射 | C + H；I 审查信任字段 | C/H Candidate | H 不定义 Provider Truth |
| UAD-06 | Applied 谓词与 C/H/I/D 证据组合 | G（Applied）+ C（Provider）+ H（Wire） | OPEN / NOT PROVEN | G 不声称模型理解或使用 Context |
| UAD-07 | Multi-PolicyDomain 跨域原子性 | I + Architecture Governance | BLOCKED / 未证明 | 不拼接本地 PermissionEpoch 为全局计数器 |
| UAD-08 | 生产密码学 Profile、密钥生命周期、anti-rollback 锚点 | I + Security/Operations | Candidate / OPEN | 候选投影不等于生产批准 |
| UAD-09 | Canonical Authority、DB/Coordinator、故障域和恢复目标 | Storage + 指定 Engineering/Operations | ADR-BLOCKED / Candidate | 逻辑事务提案不等于部署拓扑 |
| UAD-10 | 跨 Owner 精确版本与证据失效策略 | A + 全体 Owner | OPEN | A 管集成证据，不替 Owner 签语义接受 |

## 8. Critical / High 风险关闭标准

| 风险 | 最低关闭条件 |
|---|---|
| R-01 | 正式领域 ADR；决策权威/批准人/时间/理由齐全；所有消费者精确映射；身份/Scope/unknown 反例通过 |
| R-02 | 批准的序列化拓扑；Fence-first 与 Publication-first 双序列模型；所有崩溃点、丢 ACK、Failover、恢复回滚保持唯一终态或 UNKNOWN |
| R-03 | Producer/Attempt/Derivative/Retry/DLQ/Outbox/Index/Context/Adapter/Backup 全量清点；Forget-vs-every-effect 竞争；恢复后反复活负测；I 明确接受残留例外 |
| R-04 | D/E/I/Storage/COC/JF-10 状态机分离；Participant identity/digest 一致；exact bundle race/crash/replay 测试；各权威独立接受 |
| R-05 | 冻结 C/H exact schema mapping；明确 G Applied 谓词；Provider send/unknown/retry/late-ACK 测试；ACK 不推导 Applied/no-handoff |
| R-06 | 每类消息精确签名投影；双实现 canonicalization 一致；KeyStatus/revocation/issuer/audience/anti-rollback 负测；Multi-PolicyDomain ADR |
| R-07 | 自动可追溯账本包含 Owner HEAD/Blob pins/consumer matrix/Owner acceptance/exact CI head；Blob 变化触发重新审查 |
| R-08 | 各域独立 cursor/high-water/epoch；合取 Recovery Manifest 验证；截断/回滚/缺失/陈旧副本隔离；禁止跨域数值比较 |
| R-09 | 工程成本收益评估；可运行参考模型；最小端到端切片；证明每个 Gate/proof 对应独立风险、无重复权威 |
| R-10 | 批准拓扑/技术蓝图；RPO/RTO/SLO、备份、密钥、故障域、on-call 和恢复演练；工程/运维负责人签署 |

## 9. Root-first 整改建议

**P0 — 系统成立条件**
1. B 与 Architecture Governance 关闭 Fact/Claim ADR；之前不冻结共享 canonical Fact/Claim Schema。
2. D/Storage/I 关闭最终 Visibility 线性化拓扑 ADR，明确 D Fence、I Commit Authorization、Storage 原子提交边界。
3. D/I 定义 Forget/Revocation 闭世界终态；E/F/G/H/C/Storage 分别提供完整 Producer/Derivative/Recipient/Restore 账本。
4. A 组织精确协议包审查，分离 COC 与 JF-10，不将角色模拟写成独立 Owner 批准。

**P1 — 正确性与集成证明**
5. 用同一精确版本构建 Publication、Forget、Restore、Applied/Provider Outcome 参考模型。
6. 每个状态机测试双序列竞争、每个持久边界前后崩溃、丢 ACK、重复请求、变更 digest、旧租约、旧快照和 UNKNOWN。
7. 固定各 authority-local cursor、epoch、watermark、receipt、manifest 的类型与比较规则。
8. 完成 C/H 1.0.1/1.2.13 exact mapping 和 I 签名投影、KeyStatus、anti-rollback 闭环。

**P2 — 工程可运行性**
9. 评估 Modular Monolith/单一权威事务域，不预设微服务；用代表性负载和故障模型验证资源、索引、缓存、恢复策略。
10. 工程前指定 Canonical Authority、Storage topology、Coordinator、DB adapter、备份、密钥、RPO/RTO/SLO 和运维责任。

**P3 — 治理成本**
11. 每个新增 Schema/Proof/Manifest 都审查“独立失效模式—权威—消费者—测试—成本”。
12. Candidate 设到期日、决策人和升级路径，避免候选变成事实。
13. 保持双语语义对等，但不以翻译完整替代架构证明。

## 10. Gate 评估

| Gate | 本轮判断 | 依据 |
|---|---|---|
| G1 精确来源/新鲜度 | PARTIALLY VERIFIED | 已读取多个 Owner HEAD 和关键 Blob；未建立自动化全量消费者矩阵 |
| G2 Owner 权威/消费者接受 | BLOCKED | 多项仍为 role proposal/candidate；独立 Owner 接受不完整 |
| G3 端到端状态/因果一致性 | BLOCKED | Publication、Forget、COC/JF-10 组合缺完整证明 |
| G4 P0/P1 竞争/崩溃/恢复/信任 | NOT PROVEN / BLOCKED | 有测试规格和局部 CI，非当前 exact bundle 的端到端证明 |
| G5 技术拓扑/可运维性 | BLOCKED | Storage topology ADR-BLOCKED；TAB-001 Candidate |
| G6 中英文语义一致性 | PARTIALLY VERIFIED | 本次创建双语对应稿；未声称完成全仓双语审计 |
| G7 A 集成裁决/Owner 决策 | BLOCKED | R 报告不是 A 决策或 Owner 签署 |
| G8 架构冻结建议 | **NOT READY** | Critical 风险未关闭 |

## 11. 结论与限制

本报告基于 2026-11-17 读取的 GitHub 分支快照和精确 Blob。它不声称已证明所有实现必然失败；它指出当前设计证据尚未证明关键正确性不变量能够跨 Owner、跨故障和跨恢复路径成立。

- R-01 至 R-04：Critical，架构冻结前必须关闭。
- R-05 至 R-08、R-10：High，进入相关冻结/生产阶段前满足关闭 Gate。
- R-09：High，以工程成本与可运行参考模型验证，不凭直觉裁决。
- Owner 决策仍归各自权威；本报告只提出风险、证据与关闭条件。
- 不合并分支、不关闭 Issue、不释放 Gate、不授权实现或生产激活。

**Disposition: NOT READY FOR ARCHITECTURE FREEZE.**
