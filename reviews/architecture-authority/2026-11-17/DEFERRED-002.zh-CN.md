# 延后能力登记册 — DEFERRED-002

- 版本：1.0.0；基线 `6470f25ca23b8d35c06f60be2326867066418d18`。
- 延后不代表豁免核心正确性、授权、一致性、Forget 或强制 Gate 要求。

| ID | 延后能力 | Owner | 风险 | 是否阻塞 | 允许范围 | 禁止范围 | 关闭标准/证据 | 期限/Gate |
|---|---|---|---|---|---|---|---|---|
| DEF-01 | Vector/ANN 检索与向量 DB 选型 | F | Medium | 对安全首期切片非阻塞 | Synthetic Data 基准、Recall/Precision 评估、资源测量 | 生产服务、权威 Ranking、Vector Index 充当 Canonical | 标注评估集；质量/延迟/资源报告；Delete/Rebuild/Forget 测试；F 建议及所需 ADR | P2 准入前 |
| DEF-02 | Reranking 和多阶段检索 | F | Medium | 非阻塞 | Synthetic/非敏感 Fixture 离线实验 | 生产依赖或绕过 Permission/Fence 前置过滤 | 相对基线的量化提升和延迟预算；授权负向测试 | P2 准入前 |
| DEF-03 | Entity Resolution 与自动 Identity Merge | B/D | High | 自动合并阻塞；人工研究允许 | 候选 Ontology/算法比较 | 自动 Canonical Merge 或身份变更 | B 身份语义、冲突策略、可逆合并证明和消费者采用 | 身份敏感实现前 |
| DEF-04 | 高级 Consolidation/Conflict-resolution 智能能力 | B/D/E | High | Canonical 自动裁决阻塞 | 离线候选评估 | 将不确定 Claim 自动提升为 Canonical Truth | B 语义、Provenance、不确定性/冲突策略、修正和回滚证据 | P2 生产能力前 |
| DEF-05 | 多种 Vector/Graph/Search Backend | F | Medium | 非阻塞 | 对比基准 | 无实测需求却引入多后端生产复杂度 | 工作负载支撑的 ADR 和运维预算 | P2 前 |
| DEF-06 | 分布式服务拆分、多地域和自动扩缩容 | Engineering/Storage | High | 生产规模化声明阻塞 | 拓扑研究和负载模型 | 过早微服务、多地域写入或规模化声明 | 实测负载、已选拓扑、故障域和 DR 证明 | P3 前 |
| DEF-07 | Multi-PolicyDomain Atomicity | I + Storage | Critical | BLOCKED；不接受 | 仅限单 Domain 设计 | 跨 Domain 事务或暗示原子性 | 新 I/Storage 规范设计、安全策略、物理拓扑和独立符合性 | 未来单独架构决策 |
| DEF-08 | 跨 BrainAuthority 原子 Publication/Forget 事务 | D + Storage + I | Critical | v1 中 BLOCKED | 拆分为每个 BrainAuthority 独立操作；只有每个 Authority 都有终态证明且 Inventory 完整后才允许全局完成 | 一个操作跨多个 BrainAuthorityRef；根据全局协调器推断跨 Authority 原子性 | 后继规范 ADR，明确范围/协调器、顺序、部分完成、Restore/Recovery 和独立物理符合性 | 未来单独架构决策；任何多 Authority 能力前 |

## 有条件接受的非阻塞条件

**COND-NB-01 — 延后 Vector/ANN 生产能力**

- 问题：在未测量基线检索价值前，生产 Vector Retrieval 会增加 Index Lifecycle、Embedding Version、Stale State、删除/重建及运维状态。
- 证据：X PR #49 将跨模块状态/恢复复杂度评为高，并列出 Vector/ANN 可延后；F/D/P PR #46 建议先 Structured + Lexical。
- 风险：Medium；对首期安全切片非阻塞。
- 允许：仅 Synthetic Benchmark 和标注评估框架。
- 禁止：生产服务、Canonical Authority、绕过 Permission/Forget 前置过滤。
- Owner：F。
- 关闭标准：标注 Corpus；可复现 Recall/Precision 与延迟/资源报告；Delete/Rebuild/Forget 负向测试；F 明确建议。
- 截止：P2 准入前。
- 验证证据：精确 Dataset/Benchmark Commit、命令、结果、负向测试轨迹及独立回读。
- 风险接受依据：延期避免未经测量的状态/运维负担，不削弱核心记忆正确性。
- 风险接受权威：A，仅限能力延期范围；检索设计权仍属于 F。
- 升级规则：若 Vector Retrieval 被提升为 P0/P1 依赖，或在关闭前提议生产使用，立即停止该工作并提交 A + F 复审。
- 相关 Gate：P2 能力 Gate；技术选型对应 G5。

其他所有开放的 Critical 正确性/安全/权威事项均为 DEFERRED 或 BLOCKED，不得视为已接受的残余风险。
