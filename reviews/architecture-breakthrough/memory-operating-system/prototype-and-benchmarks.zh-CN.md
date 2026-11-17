# 合成原型与基准测试

**状态：探索性合成实验；不是用户行为、生产负载或 Runtime 符合性证据。**

## 实验问题

共享资源分配器能否在资源竞争下改善公平性？与简单 Retrieval、Rerank+Budget 相比，会引入怎样的质量/延迟权衡？

## 复现条件

- Python 3.11+，仅标准库。
- 固定随机种子：20261118。
- 30 个独立任务；每个任务 24 个候选 Memory（共 720）。
- 每个任务有 4 个必需候选（共 120 个）。
- Candidate Token Cost 在 25–110 之间均匀采样。
- 全局 Context Token Budget：9,000；单任务上限：650。
- 4% 候选无权限；1.5% 候选已 Forget（独立生成）。
- 必需候选初始 Relevance 较高；干扰项存在重叠且可能获得高分。
- Rerank Score = 0.35 Relevance + 0.20 Authority + 0.15 Freshness + 0.15 Evidence + 0.15 Task Value。
- RM 先为每个任务预留相同底线（全局预算 / 30），再按当前归一化分配最低的任务轮转，单任务上限 650。
- 三种方法都在选择前执行相同硬资格过滤。

## 算法

1. **Direct Top-K：** 每个任务按 Relevance 取前 6，再按 Relevance 填充共享全局预算。
2. **Retrieval + Reranking + Budget：** 按 Rerank Score / Token Cost 全局排序，贪心填充相同预算。
3. **Unified RM：** 使用相同候选与 Rerank 集合，但增加任务级 Reservation Floor，并在任务上限内公平分配剩余预算。

## 指标定义

- Recall = 选中的必需候选 / 全部 120 个必需候选。
- Precision = 选中的必需候选 / 全部选中候选。
- Token Efficiency = 必需候选 Token / 全部选中 Token。
- Redundancy = 每个 Task-Topic Bucket 首个候选之后的额外候选数 / 已选数量。
- Task Coverage = 每个任务 4 个必需候选覆盖率的平均值。
- Starvation = 获得零个候选的任务数。
- Fairness = 各任务必需候选覆盖率的 Jain Index。
- Budget Utilization = 已用 Token / 9,000。
- Latency = 本地进程内运行 100 次的中位数；单线程 Python 微基准，不代表服务延迟。

## 结果

| 指标 | Direct Top-K | Rerank + Budget | Unified RM |
|---|---:|---:|---:|
| Recall | 0.5333 | **0.5417** | 0.5083 |
| Precision | **0.4741** | 0.2863 | 0.2699 |
| Token Efficiency | **0.4817** | 0.3244 | 0.2984 |
| Redundancy Rate | **0.2815** | 0.4097 | 0.4071 |
| 平均 Task Coverage | 0.5333 | **0.5417** | 0.5083 |
| 饥饿任务数 | 1 | 0 | **0** |
| Jain 公平度 | 0.8325 | 0.8141 | **0.8554** |
| Budget Utilization | 0.9997 | 0.9996 | 0.9973 |
| 选择延迟中位数（ms） | **0.099** | 0.127 | 0.324 |

## 结果解释

- RM 消除了饥饿并提高了该负载下的公平性，但没有提高 Recall、Precision、Token Efficiency 或减少冗余。
- 公平性提升来自为所有任务保留容量，包括候选价值较低的任务。这是有意的服务保障，不是免费的效率提升。
- Direct Top-K 的 Precision 和 Token Efficiency 最好，但有一个任务完全饥饿，任务间覆盖不均。
- Rerank+Budget 的总体 Recall/Task Coverage 最好，但 Jain 公平度最低。
- 本原型 RM 延迟约为 Direct Top-K 的 3.3 倍。这是小型 Python 算法原型的开销，不是生产性能估计。
- 实验仅支持条件性结论：当公平性是产品要求时，共享资源仲裁有价值；不能证明它普遍提升检索质量。

## 重跑命令

将原型保存为 `prototype.py`，运行：

```bash
python3 prototype.py
```

测试程序应打印固定随机种子、参数、全部九项指标和 100 次运行中位数。任何实现变化都必须保持相同 Seed/Parameter Manifest，或发布新的 Experiment ID。

## 有效性限制

没有模拟自然语言 Embedding、真实索引、模型 Tokenizer、用户偏好标签、真实任务轨迹、多进程竞争、I/O、CPU 饱和、GPU、网络、Cache Invalidation、Forget Race 或存储恢复。分数是合成标量。Latency 不包含 Retrieval Backend、Authorization RPC、Canonical Revalidation、序列化和推理 Provider。不得把结果描述为真实用户行为或生产容量证据。
