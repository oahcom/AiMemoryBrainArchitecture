# Phase 1 Memory Store Facade

状态：Phase 1 编排边界 DECIDED；Storage 后端仍保持可替换。

## 目的
提供最小应用层 Facade，将已冻结 Domain Model 与后端无关的 MemoryStorage Port 组合起来。

## 职责
- 在进入 Storage 前校验 Memory / MemoryVersion 领域不变量；
- 每个操作都要求已解析 Scope；
- 保持 Memory identity 与不可变 MemoryVersion/revision 语义；
- 在提交前拒绝 memory_id 与 revision.memory_id 不一致；
- 将 CAS、幂等和可见性约束委托给 MemoryStorage；
- 提供 current/revision 读取与幂等解析，但不拥有持久化。

## 非职责
不定义 SQLite DDL、分布式共识、Physical Forget、Permission Policy、索引、Embedding、LLM 或部署拓扑。

## Revision 边界
Phase 1 将 MemoryVersion 作为规范不可变 revision 表示。MemoryRevision 只是 API alias，不产生第二个持久化对象。

## Scope 边界
每个 Facade 操作都要求非空 resolved Scope。Scope 兼容不等于 Permission 授权。

## 幂等写入边界
Revision write 同时携带 expected-current-version、Idempotency Key 和 Request Digest。身份不一致必须在进入 Storage 前拒绝；重放/冲突语义由 Storage Port 负责。

## 验收
Create/Read 必须有有效 Scope；revision identity mismatch 必须在后端调用前失败；stale transition 必须被拒绝；相同 Key + Digest 可以解析到原 Receipt；不同 Scope 不得隐式可见；Facade 不得引入后端特定依赖。

## 下一单元
待该最小 Facade 稳定后，再继续更高层 Memory Store 行为和应用集成；不引入 Vector/Graph/LLM 依赖。
