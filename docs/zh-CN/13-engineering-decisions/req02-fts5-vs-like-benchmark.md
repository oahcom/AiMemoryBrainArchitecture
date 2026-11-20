# REQ-02 证据：SQLite FTS5 与无索引 LIKE 扫描对比

- 证据 ID：REQ02-LEXICAL-BENCH-001
- 需求：REQ-02 / Issue #263
- 状态：**候选证据——不是技术决议**
- 基线：`main@927eadcb1a8ee94cf533491823373b5ce5f4e204`
- 蓝图输入：TAB-001 §4.3，Blob `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- 可执行脚本：[ `benchmarks/req02/fts5_vs_like.py`](../../../benchmarks/req02/fts5_vs_like.py)
- 实测结果：[ `benchmarks/req02/results-2026-11-20.json`](../../../benchmarks/req02/results-2026-11-20.json)

## 问题

对于首个本地词法检索路径，在同一数据集上，SQLite FTS5 与不建索引、使用 SQL `LIKE` 精确 token 扫描之间，实际查询路径性能差异是多少？

这是嵌入式全文索引与最简单无索引基线之间的窄范围比较；它不是与 Tantivy 或其他外部搜索产品的比较，也不决定产品是否正式采用 FTS5。

## 方法

脚本只使用 Python 标准库及其链接的 SQLite FTS5 实现。它创建临时 SQLite 数据库、确定性合成数据集、使用 `unicode61` tokenizer 的 FTS5 external-content 表，并在相同的补空格 token 文本上执行 LIKE 扫描。

复现命令：

```bash
python3 -m py_compile benchmarks/req02/fts5_vs_like.py
python3 benchmarks/req02/fts5_vs_like.py --output benchmarks/req02/results-2026-11-20.json
```

运行参数：12,000 条文档；500 个 token 词表；每条文档 40 个不重复 token；随机种子 `20261120`；100 个确定性查询；每条路径预热 25 次；每条路径计时 300 次。脚本在计时前核对全部 100 个查询的有序结果集是否完全一致。

## 本地真实结果

环境：Python 3.13.5；SQLite 3.46.1；Linux x86_64。

| 指标 | SQLite FTS5 | SQL LIKE 扫描 |
|---|---:|---:|
| P50 | 285.44 μs | 9,908.69 μs |
| P95 | 433.36 μs | 12,309.67 μs |
| P99 | 820.31 μs | 14,873.49 μs |
| 平均值 | 319.70 μs | 10,263.03 μs |
| 吞吐 | 3,127.95 queries/s | 97.44 queries/s |

- 结果集一致性：**100/100 个查询完全一致**。
- 平均延迟比（LIKE / FTS5）：**32.10×**。
- 查询计划：FTS5 显示 `SCAN docs_fts VIRTUAL TABLE INDEX 0:M1`；LIKE 显示 `SCAN docs`。

记录值来自一次真实执行，不是对生产负载的统计结论。在其他机器、缓存状态或系统负载下重跑会得到不同数值。

## 解读与限制

本次运行表明：对于本次精确 token 合成负载，SQLite FTS5 在返回相同结果集的同时，明显快于无索引全表扫描。该结果支持在 TAB-001 §4.3 中将 FTS5 保留为首个本地词法检索通道的优先候选。

本结果**不能**证明：
- Rust `memory-storage-sqlite` Adapter 或产品运行时的性能；
- 端到端检索质量、排序相关性、Scope/Permission 执行、Forget 抑制或授权安全；
- 写入/更新/删除吞吐、读写并发、崩溃恢复、索引重建成本、存储增长或运维维护成本；
- 相比 Tantivy 或其他成熟搜索引擎的优势；
- 已批准的技术选择、ADR 或 Owner 验收。

LIKE 基线有意选择为无索引对照，并非另一个成熟产品。若要在 FTS5 与 Tantivy 之间作正式选择，必须提供可执行的同等比较，统一 tokenizer、查询语义、结果集正确性、语料和负载。本证据必须保持 `CANDIDATE`。

## 出处与验证

- 提示词出处：当前 ChatGPT 对话中的 T2 用户指令；Prompt ID `REQ02-LEXICAL-BENCH-PROMPT` v1。当前接口不暴露会话 UUID/永久链接；原始聊天指令字节的 SHA-256 为 `NOT_VERIFIED`。未伪造来源标识。
- 脚本 SHA-256：`0b2aa5f306940cb3d7baa24f91b55924a012ee14c5eaa3ecdd102f40c5e01d22`。
- 实测结果 SHA-256：`56d057552d91155f3eb029773c985cc729f50f6bf70c2209c6462c45bc2f2b6d`。
- 本地验证：`python3 -m py_compile` 退出码 0；基准执行退出码 0；100/100 结果集一致性检查通过。
- 执行分类：`LOCAL_ONLY`；执行路径为 Python `sqlite3`，不是 Rust 原生执行，也不是 CI。
