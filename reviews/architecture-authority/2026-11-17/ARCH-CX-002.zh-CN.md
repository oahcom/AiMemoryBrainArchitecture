# 架构复杂度评估 — ARCH-CX-002

- 版本：1.0.0；基线：`main@8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`
- X 来源：PR #49，Commit `131f91743bd506517ee354d58c277501ca447929`，英文 Blob `c509120644d6f7c7223decf3f9f0ee33b0548bb7`，中文 Blob `981a376ddf283ace1e891795c813b17ac4aa3d8b`。
- A 裁决：复杂度可控性 **NOT PROVEN**。

## 五项最大复杂度瓶颈

1. Forget → Producer Admission → Dependency/Derivative Registration → Final Publication Gate。X 对该跨模块链的八个维度均评为 5/5。
2. Global Forget Completion 覆盖 Canonical、衍生物、索引、缓存、Context、Adapter、副本和备份；这些对象具有不同证明和终态语义。
3. Storage/Consistency 的事务、可见性、COC/JF-10 恢复与故障切换。Storage 模块八维均为 5/5；L1 Option A 已选定，但 L4 物理引擎/部署仍开放，因此置信度为 Low。
4. D/E/Storage 跨模块的 Durable Ingress、Outbox、Lease、Retry、Replay 和 Canonical Cursor 协调。
5. C/G/H 的 Applied/Provider Outcome 与 I/D 授权和 Fence 证据组合。

## 复杂度模型核验

X 使用八个序数维度：内部、依赖、状态、并发、恢复、验证、运维、认知；每项 1–5 分。分数适合定位热点，不是可相加的项目总分、工期估算或实测运行复杂度。最高分集中在 D、E、Storage 和跨模块 Forget/Publication。H/I 同样承担较高责任和证明负担；X 对未完整检查 Owner 源文件的项目降低置信度是合理的。

## 交叉核验与修正

- 必须保留不同证明对象：Accepted、Compiler Completion、Canonical Commit、Index Applied、Context Applied、Applied、Forget Completion、PublicationReceipt 和 Provider Outcome。
- 不得在没有量化需求时，为每个逻辑概念新增独立服务、数据库、队列、协议或版本边界。
- Local-first Rust Modular Monolith 是首期工程切片的优先候选部署形态。Storage 已另行选择 L1 Option A（每个 Canonical Memory Authority 一个 Serializable Transaction Domain）；实际 L4 Engine/Deployment 符合性仍开放。这不合并 Owner 权威。
- 每项跨模块操作必须指定一个 Operation ID、各状态权威、有限 Participant 集合、线性化点、可重试阶段、终态和恢复动作。
- 每个 Receipt/Manifest/Applied/Watermark 必须标明签发者、主体、Scope、Generation/Version、持久性、时效和明确的非声明。
- Derived Index/Cache 不能成为第二权威；陈旧状态必须可检测、可重建。
- 降低复杂度不得删除身份、授权、Durable Admission、Forget Fence、幂等性、审计、恢复或证明分离。

## 复杂度预算与验证阈值

在任何 P0/P1 不变量被称为已验证之前，必须有直接负向测试、每个持久化边界前后崩溃测试、Duplicate/Out-of-order/Retry/Partial Failure/Recovery 案例，以及跨 Owner 追踪关联。只有 Happy-path E2E 不足以通过。

## 简化裁决

**MUST PRESERVE：** 权威边界、Typed Identity/Scope、单调 Fence、幂等性、不同证明状态、恢复/还原、审计、Owner 本地因果位置。

**CAN SIMPLIFY：** 首期采用 Modular Monolith；若 Storage/D/I 批准并证明，可采用一个 Canonical SQL 权威事务域；统一 Operation Envelope；可重建投影；首期限制为一个 I PolicyDomain。

**CAN DEFER：** Vector/ANN、Reranking、图数据库后端扩张、多 Provider/Backend、Multi-PolicyDomain 原子性、分布式服务拆分和高级自动扩缩容。

**MUST NOT INTRODUCE：** 跨域 Cursor 比较、Cache/Index 充当权威、用通用 Success 替代不同终态、JF-10 启发式裁决、用进程 Mutex 代替持久原子性、无量化依据的微服务。

## Option A 与协议 Bundle 新增复杂度

Option A 减少了协调器扩张，但新增五项重要证明/维护义务：（1）共享 Transaction Executor 与 D/Storage 行写权威边界；（2）D EffectPermit 必须覆盖 Admission/Lease/Attempt/Retry/Replay/Source Read/Execution/Late Dependency/Terminalization；（3）v1 每个原子操作仅限一个 BrainAuthority；（4）I COMMIT_WON 不可变 Tuple 及 Crash/Revocation/Replay 语义；（5）独立 Anchor Checkpoint 和 DB-Incarnation Restore Anti-rollback Witness。PR #54 修订仍是提案，不是已采纳 Owner 合同。

H 1.2.14/CSubmitOutcome 1.0.1 协议候选也增加精确当前性联结复杂度。H Mapping、C Re-review、D Crosswalk、I P0 和 Storage Manifest 必须绑定同一组当前工件；v3.2.9 已过期，需要 v3.3.0 后继版本。

## 结论

系统复杂度高，复杂度可控性 **NOT PROVEN**。可以降低不必要的部署复杂度，但 P0 证明负担仍然很高。参见 SYS-RISK-002、DEV-FEAS-002、DEP-DAG-002 和 GATE-002。
