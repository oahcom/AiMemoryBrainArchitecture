# 成熟技术选型——候选矩阵

状态：仅为研究建议，不替代 TAB-001、Storage ADR 或 Owner 决策。

| 能力 | 候选产品 | 建议 | 边界/所需证据 |
|---|---|---|---|
| Canonical Transactional State | PostgreSQL | 可作为 Storage Transaction/Serialization Domain 的强候选，但必须服从当前 Storage ADR 并完成物理 L4 证明 | 验证 Serializable Transaction、COC Durability、Failover/Old-primary Fencing、Restore/PITR 和部署拓扑。PostgreSQL WAL 支持崩溃恢复，但不能单独证明跨 Owner Forget/COC 正确性。 |
| 本地单用户原型 | SQLite | 仅在 Storage Owner 认可语义适配时，用于隔离本地原型或单节点 MVP | WAL 支持一个 Writer 与并发 Reader，但 Writer 仍串行；测试 Lock、fsync/VFS、Backup 和 Crash Restore。不能假设 SQLite 满足跨进程/全局 JF-10 拓扑。 |
| Lexical/Full-text Index | Tantivy 或 SQLite FTS5 | 从最简单路径开始；若实测规模需要，Tantivy 是强 Rust 原生嵌入式候选 | Index 是派生且可重建的；执行 Scope-before-Candidate 和分区 Watermark。已采用 SQLite 时，FTS5 最简单。 |
| Vector ANN | Qdrant | 只有标注检索评估证明 Lexical/Structured 有明显缺口后再引入 | 验证严格 Scope Filter 下的预过滤保证、过期/删除 Payload 抑制、分区隔离、重建和 Forget Race。Qdrant 支持 Hybrid Query/Filter，但不是授权权威。 |
| 可丢弃 Cache | Redis / Valkey | 可选 Cache；不能作为 Canonical Memory 或唯一安全账本 | LRU/LFU 是近似 Cache 策略。Cache Key 必须绑定精确 Version/Scope/Epoch；每次 Hit 都重新验证 I/D。正确性关键元数据优先使用 No-eviction 或有界本地 Cache。 |
| Scheduler/Concurrency | Tokio 原语 + 小型进程内策略模块 | 优先采用有界 Channel、Semaphore、Cancellation、Task Group 等库原语 | Runtime Admission 是临时执行。只有证明需要持久长流程后，才考虑 Temporal/DBOS/Restate，不要给每次 Recall 引入 Durable Workflow。 |
| Resource Ledger | 现有事务存储 | 只有采用 RM 时才持久化 Reservation/Idempotency；否则使用本地有界计数 | 不能把 Authority Token、Forget Completion 或 Context Lifecycle 放在 Redis TTL 语义之下。 |

## 产品边界

- 直接采用成熟 Storage Engine、Text Index、Vector Search 和 Cache；不自研 B-tree、倒排索引、ANN 或 LRU 数据结构。
- Brain 自己掌握 Canonical Identity、Authorization Gate、Forget Fence、Provenance、Task Coverage/Sufficiency、Activation Rationale、Fairness Policy、Residency View 解释和可解释性。
- 任何技术选型都不能把派生 Index/Cache 变成 Canonical Authority。
- 对 Local-first Modular Monolith，不应在缺乏负载与运维证据时引入 Kubernetes 或分布式 Scheduler。

## 参考资料

- PostgreSQL WAL：https://www.postgresql.org/docs/18/runtime-config-wal.html
- SQLite WAL：https://www.sqlite.org/wal.html
- SQLite FTS5：https://www.sqlite.org/fts5.html
- Tantivy：https://docs.rs/tantivy/latest/tantivy/
- Qdrant Search：https://qdrant.tech/documentation/search/search/
- Redis Eviction：https://redis.io/docs/latest/develop/reference/eviction/
