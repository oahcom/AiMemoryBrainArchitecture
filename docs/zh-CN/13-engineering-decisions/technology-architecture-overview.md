# AI Memory Brain 技术架构总览

- 文档 ID：DOC-TEC-001
- 版本：1.0
- 对应英文：[Technology Architecture Overview](../../en/13-engineering-decisions/technology-architecture-overview.md)
- 依据：TAB-001 v0.1 与 TAR-AI-001 最终系统技术架构审查
- 状态：技术解释文档；候选方案不构成技术冻结

## 1. 技术架构要解决什么问题

逻辑架构说明系统由什么组成、谁负责什么；技术架构进一步回答：用什么技术承载职责、模块如何通信、哪些状态必须在同一事务中持久化、系统如何部署和恢复，以及如何在本地 CPU、RAM、SSD 和 12–16 GB VRAM 约束下运行。

技术选择必须服务于正确性、可恢复性和可维护性，而不是追逐技术名词。

## 2. 当前首期推荐形态

**模块化 Rust 单体 + 明确的内部接口 + 本地持久化 + 可选独立推理进程。**

- 逻辑模块保持清晰，但不急于拆成微服务。
- 正确性关键的状态变更尽量位于明确的事务边界内。
- 模型推理可独立进程运行，避免模型加载、GPU OOM 或推理卡顿阻塞可靠事件接收和恢复。
- Agent Adapter 可嵌入 Agent，也可通过 Sidecar 或本地 Gateway 接入。
- 索引和缓存是派生数据，不是权威记忆。

这是首期工程候选形态，不是生产部署批准。

## 3. 技术层次

| 技术层 | 职责 | 主要约束 |
|---|---|---|
| Agent Adapter / BMCP | 遥测接入、上下文交付、ACK、能力协商 | 身份认证、版本兼容、最终推理边界证据 |
| Ingress / Compiler | 可靠接收、提取、规范化、证据和派生物 | 幂等、重试、任务恢复、Forget 发布门 |
| Canonical Memory | 权威记忆、版本、生命周期 | 事务一致性、版本历史、遗忘屏障 |
| Runtime / Retrieval | 检索、排序、激活、工作集 | Scope 先过滤、索引水位、防复活 |
| Memory Context | 上下文规划、编辑、版本、投递 | CAS、Delivery 状态、Applied 证明 |
| Governance | 身份、权限、保留、Forget、审计 | 跨模块强制执行和可核验证据 |
| Storage / Index / Cache | 数据持久化、搜索索引、缓存 | 权威与派生分离、可恢复重建 |
| Inference Provider | Embedding、提取、重排、可选生成 | 资源隔离、模型可替换、预算控制 |

## 4. 主要候选技术与状态

| 领域 | 候选 | 当前状态 | 必须验证 |
|---|---|---|---|
| 核心语言 | Rust | 项目方向已确定 | Crate 边界、依赖治理、编译和集成成本 |
| 异步运行时 | Tokio | 推荐候选 | 有界任务、背压、CPU 密集任务隔离 |
| 事务数据库 | SQLite WAL / PostgreSQL | 未最终决策 | 同一负载下事务、并发、崩溃恢复和 Forget 原子性 |
| Blob 存储 | 内容寻址文件系统 | 推荐方向 | DB 与 Blob 一致性、孤儿清理、加密、备份恢复 |
| 全文检索 | FTS5 / Tantivy | 待比较 | 同语料索引成本、查询延迟、更新和重建 |
| 向量检索 | usearch / sqlite-vec 等 | OPEN | Recall、过滤、内存、更新删除和重建 |
| 缓存 | Moka / 无缓存 / Redis | 候选 | 失效、权限隔离、Forget 防复活和内存上限 |
| 任务执行 | Transactional Outbox + 有界 Tokio Worker | 首期候选 | Lease、重试、DLQ、Replay、幂等和崩溃恢复 |
| 模型推理 | ONNX Runtime、GGUF/llama.cpp 等 | 候选 | 目标硬件延迟、VRAM、量化、模型版本和回退 |
| 协议编码 | Serde、JSON/JCS、CBOR 等 | OPEN | 规范化字节、签名、跨语言兼容、严格解析 |
| 传输 | HTTP、Unix Socket、Named Pipe、gRPC | OPEN | 身份认证、重连、跨平台、延迟和可观测性 |
| 密钥管理 | OS Key Store、信封加密等 | OPEN | 密钥轮换、恢复、备份和密码学擦除 |

候选技术不会仅因为出现在 TAB-001 中就自动成为批准选型。

## 5. 为什么不能凭偏好确定数据库

数据库不仅保存记忆文本，还可能承载 Canonical Memory、版本、Event、Accepted Receipt、Idempotency、Producer Registration、Forget Fence、Dependency Registration、Outbox、恢复检查点、Context、Delivery 和治理记录。

SQLite WAL 的优点是本地部署简单、运维成本低；限制是单写者模型和并发写入压力。PostgreSQL 的事务并发和运维能力更强，但需要额外服务、备份和部署管理。

应使用同一套代表性负载和一致性测试比较，而不是凭偏好拍板。

## 6. 正确性优先的数据流

~~~text
Event + Idempotency + Accepted Receipt
                ↓
        Durable Compiler Work
                ↓
       Candidate / Derivative
                ↓
  D Authority + Storage Publish Gate
                ↓
       Canonical Commit + Cursor
                ↓
       Index / Runtime Visibility
~~~

遗忘与生产流程竞争时必须仍然安全：

~~~text
Producer Admission ─────┐
                        ├─ Shared linearization boundary
Forget Fence Install ───┘
                        ↓
Dependency Registration
                        ↓
Final Publication Gate
                        ↓
Visible or Suppressed
~~~

**“先读取 Fence，再单独写入派生物”不是原子操作。** 必须有明确事务或等价线性化机制，并通过并发竞争和崩溃注入测试。

## 7. 部署与资源预算原则

当前规划范围为 12–16 GB VRAM，但这不是已完成的容量测试。

- 持久化、治理和核心状态机必须能在没有 GPU 推理时运行。
- Embedding、Reranker 和生成模型应可独立启停、限流和降级。
- 分别测量模型权重、KV Cache、上下文长度、Batch、并发数和显存碎片。
- CPU、RAM、SSD IOPS、索引构建和恢复时间也必须纳入预算。
- 必须声明硬件、模型版本、量化方式、语料规模、并发和测量方法。

没有可复现数据时，只能标记为估算或待验证，不能称为实测性能。

## 8. 当前技术审查结论

TAR-AI-001 最终系统结论为 **BLOCKED**；TAB-001 仍是 CANDIDATE，未批准、未冻结。

关键阻塞：
1. Fact/Claim ADR 未批准，依赖它的 Schema 和接口不能冻结。
2. D/E/Storage 的 Producer Admission、Forget Fence、Dependency Registration 和 Publication 原子边界缺少应用级实现证明。
3. JF-10 / COC 的同 XID 恢复和真实参与者集成仍未闭合。
4. Global Forget 的全目标映射、确认和完成证据需要端到端闭合。
5. C/G/H 的最终推理请求 Applied 证明需要真实 Adapter 集成。
6. F 的索引、缓存和重建防复活需要运行时故障测试。
7. 真实负载、资源预算和 P95/P99 基准测试尚未完成。

## 9. 推荐验证顺序

1. 解决 Fact/Claim ADR。
2. 建立 D/E/Storage/COC/I 原子发布与恢复集成测试。
3. 闭合 Global Forget 目标清单和证据向量。
4. 实现并验证 C/G/H Applied 最终请求证明。
5. 验证 F 的真实索引、缓存和防复活。
6. 正确性契约稳定后，再比较数据库、全文索引、向量索引和推理后端。
7. 运行代表性负载和 12–16 GB VRAM 资源测试。

---
**English counterpart:** [Technology Architecture Overview](../../en/13-engineering-decisions/technology-architecture-overview.md)
