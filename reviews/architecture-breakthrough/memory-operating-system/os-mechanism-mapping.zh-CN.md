# 操作系统机制映射——适用条件与失效边界

状态：仅为候选类比。Brain 管理的是知识投影与任务上下文，不是物理内存页或进程地址空间。

| OS 机制 | 可借鉴之处 | Brain 必须如何调整 | 失效边界 |
|---|---|---|---|
| Virtual Memory / Page Table | 区分规范后备资产与任务局部物化；按需解析引用 | Canonical Memory 是后备权威；F Working Set 与 G Context 是不同投影 | Memory 是语义知识，不是固定大小页；Page Fault 不能定义相关性或真实性 |
| Page Cache | 缓存可丢弃读取结果，在压力下回收并从权威源重新获取 | 缓存精确不可变版本引用与授权/Fence Epoch；Cache Miss 不影响正确性 | Linux Page Cache 不理解 Permission、Forget、Provenance 或 Epistemic Status |
| Page Fault | 对缺失的合格资产发起显式按需读取 | 转化为有界 Recall Miss/Deferred Expansion，返回 Deadline 与 Completeness | 不能把每个未纳入记忆都变成同步昂贵检索 |
| Working Set | 限制任务局部热点集合 | 每个 Runtime Session/Task 有界引用/物化；G Context 仍是独立受管理推理区 | OS Working Set 是局部性近似；语义重要性和跨任务复用不同 |
| Memory Pressure / Reclaim | 触发安全降级并回收可丢弃状态 | 优先清 F Cache；减少可选 Graph/Evidence 工作；延后后台刷新；不能静默丢弃 G 必要覆盖 | 不能回收 Canonical State、Forget Evidence 或受保护 Context 要求 |
| LRU/LFU/ARC | Cache Replacement 候选启发式 | 仅用于可丢弃 Cache；考虑频率衰减、最近性和扫描抵抗 | 不能用于 Context 成员决策；低频记忆可能极重要 |
| CPU Scheduling / WFQ | 公平份额、Reservation、Aging、有界 Queue、Deadline | 按 Principal/Task 分配 Retrieval 与 Context Planning 资源 | 重要性/紧迫性不能绕过 Permission、Forget、Quota 或其他任务保障 |
| cgroups | 硬上限与压力隔离 | 按 Principal/Task 限制 CPU、Memory、Fan-out、Token 和 Latency | cgroups 不执行语义 Token Sufficiency 或 Context Coverage |
| NUMA | 消费者附近的热点数据局部性 | 仅在 Profile 证明收益后做进程/索引局部性优化 | 本地单机部署通常未必受 NUMA 限制 |
| Cache Hierarchy | 区分持久源、索引、Runtime Cache、Task Context、Adapter Materialization | 每层明确 Owner、重建和失效规则 | 这些不是单一缓存层级：G Context 是版本化语义产物，不是 L2 Cache |
| Kubernetes Requests/Limits | 按声明需求 Admission、最低保障、限制过度使用 | Request/Reservation/Limit/Deadline 合同和邻居隔离 | K8s Scheduler 是节点放置，不是记忆选择算法 |

## 推荐映射

1. **Residency 是视图，不是新的规范生命周期。** 只表示本地投影状态（未驻留、已缓存、在 Working Set、已暂存 Context、已由 Adapter 应用），并保留 Owner 专属 Epoch 与证据。禁止存储全局“记忆已驻留”的真值。
2. **Page Fault 转化为有界 Recall。** 返回候选引用、Freshness/Completeness，可延后或部分返回。
3. **Reclaim 必须按类别处理。** F 可淘汰可丢弃 Cache/Working Set 物化；G 只能通过自己的版本化 ChangeSet 延后或移除 Context Entry。二者都不能删除 Canonical Memory。
4. **Memory Pressure 采用降级阶梯。** 停止推测性刷新 → 取消低优先级工作 → 回收 F Cache → 减少可选扩展 → 请求 G 压缩/延后可选 Entry → 若必要覆盖仍超预算则返回 Insufficient。
5. **按 Request/Task 使用 Weighted Fair Scheduling。** 为每个活动 Principal/Task 保留最低额度；在安全边界借用未使用容量；对排队请求做 Aging；隔离后台任务。
6. **硬门禁位于调度器之外。** Authentication、Scope、I PermissionEpoch、D ForgetFence、Canonical Lifecycle/Version、Provenance Access 和 Classification 必须先行。

## 重要的反向映射

- 不要把 Forget 映射为 Page Eviction。Forget 是具有 Lineage、Inventory 和 Evidence 语义的权威生命周期/撤销操作。
- 不要把 Archive/Retention 映射为 Swap。持久保留和合规删除不是缓存层级。
- 不要把 Context P0–P3 映射为 OS 进程优先级。它们是纳入优先级，不是权限。
- 不要把“最近访问”映射为“重要”。低频紧急指引或偏好可能比热门 trivia 更重要。
- 不要用全局 LRU 决定用户应该记住什么。
- 不要从 Cache Residency 或 Index Partition 推断 Permission。

## 参考资料

- Linux MM concepts：https://docs.kernel.org/admin-guide/mm/concepts.html
- Linux cgroup v2：https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
- Linux VM/NUMA reclaim：https://docs.kernel.org/admin-guide/sysctl/vm.html
- Redis eviction：https://redis.io/docs/latest/develop/reference/eviction/
- Kubernetes resource requests/limits：https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
