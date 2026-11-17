# 架构与实现依赖 DAG — DEP-DAG-002

- 版本：1.0.0；基线 `6470f25ca23b8d35c06f60be2326867066418d18`（历史评估快照，非当前 Main）。
- 权威：A 负责集成；领域语义仍由表中 Owner 自己决定。

## 架构决策 DAG

```text
项目权威：运行时仓库 + 具名工程责任人
  ├─ B：Canonical Identity / Fact-Claim / Temporal 语义
  ├─ I + 外部权威：安全策略 / Trust / Inventory / Revocation
  ├─ D/E：Canonical Lifecycle / Admission / Lineage / Cursor 合同
  ├─ C/G/H：Final Request / Provider Outcome / Applied 语义
  └─ Storage + D + I：物理序列化 / Visibility / Recovery 拓扑
        ↓
精确版本消费者接受 + 跨 Owner 冲突解决
        ↓
A 集成裁决（不替代 Owner 批准）
        ↓
有界 Implementation Entry 决策
```

## 实现依赖 DAG

```text
P0-01 运行时仓库、具名负责人、可复现构建
  ↓
P0-02 B Identity/Domain 语义 + I Policy/Inventory 前置条件
  ↓
P0-03 L1 Option A 逻辑配置已选定；证明 L4 物理 DB/Adapter 与 COC 拓扑
  ↓
P0-04 D/E/I/Storage Admission + Lineage + Fence + Visibility 合同
  ↓
P0-05 Durable Ingress/Outbox + Canonical Commit/Cursor/Recovery
  ↓
P0-06 授权后的 Structured/Lexical Retrieval + Forget-safe 投影
  ↓
P0-07 Context Version/Delivery + C/G/H Final Request 和 Applied
  ↓
P0-08 集成 Race/Crash/Replay/Failover/Restore 符合性
  ↓
独立的部署与生产验收
```

这是对声明和受保护执行的硬依赖顺序，不禁止并行准备。

## 验证依赖 DAG

```text
精确源版本与 Owner 权威证据
  → 语义/合同一致性
  → Model/Schema 负向测试
  → 组件测试
  → 跨 Owner 合同测试
  → Race/Crash/ACK-loss/Replay/Failover/Restore 测试
  → 独立证据审查
  → 对应 Gate 验收
  → 生产运维授权
```

## 更新后的 B→A 关闭顺序

**Wave B — 精确协议 Bundle：** H 将 1.2.14 Mapping 更新为当前 D Crosswalk；C 复审该后继 Mapping；H 复审当前 I P0；I 刷新 Anchor Review；H 记录 C 接受和当前 CI；Storage 发布 v3.3.0 或等效版本，绑定当前 C/H/D/I/Storage 精确 Blob 与 Run/Commit/Job；C/H/D/I 复审同一 Manifest；A 回读后继 Manifest 和源分支。该链未关闭前不得协议冻结。

**Wave A — Option A L1/L2：** Storage 提交解决 A-01/A-06 文档清晰度的 ADR 后继版本；D 对 Storage ADR 和共享 Anchor 合同作精确决议；D/Storage 定义共享 Transaction Executor/UoW 和行写授权边界；D 将 EffectPermit 映射到所有 Fence-sensitive 生命周期转换；v1 每个原子操作限制为一个 BrainAuthorityRef；I/Storage 定义 COMMIT_WON 重放/撤销/崩溃语义；Storage/I 定义独立 Restore Anti-rollback Witness；D/I/Storage/H 澄清 COC/JF-10 证明顺序且不宣称跨 Log 原子性。A 对精确后继 Blob 复审。只有 A-01/A-02/A-03 规范化且 D 对 Storage ADR 精确接受后 L1 才能关闭；L2 要求 A-04/A-05 组合；L3 要求实际执行确定性并发/参考模型/故障证据；L4 仍是物理部署。

## 关键路径与并行工作

关键路径：指定实现权威 → 关闭 B/I 及其他 Owner 语义 → 完成已选定 Storage Option A 与 COC 拓扑的 L4 物理实现 → 证明 D/E/I/Storage Publication/Forget 边界 → 证明 Durable Canonical 纵向切片 → 安全 Retrieval/Context → Applied → Recovery/Restore 符合性。

可并行的有界工作：Synthetic Data Retrieval 基准；DB/COC 候选比较；故障测试框架脚手架；不冻结候选 Schema 的 Validator；双语一致性和精确版本自动化；硬件/工作负载盘点；可观测性/Runbook 草案。这些工作不解除依赖 Gate。

## 依赖规则

- B 语义必须先于依赖它的 Schema/Type Freeze。
- I Policy 必须先于受保护授权、撤销和 Global Forget 声明。
- D/E/I/Storage 原子可见性必须先于 Canonical Publication 实现和生产读写。
- C/G/H 精确 Final Request 语义必须先于 Applied 实现。
- Storage 拓扑和 JF-10 物理证明必须先于生产一致性声明。
- 技术 ADR 必须跟随 Owner 合同和可复现实验，不能反过来。

参见 SYS-RISK-002、DEV-FEAS-002、PRIORITY-002 和 GATE-002。


## 当前 Main HEAD

本次发布独立观察到的当前 Main HEAD 为 `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`。此前的 `6470f25...` / `b372b62...` 均为历史评估快照，不是当前 Main。本套文件尚未完成针对当前 Main 的逐来源完整差异审计；G1 仍为 PARTIAL，所有 Gate/冻结限制继续有效。
