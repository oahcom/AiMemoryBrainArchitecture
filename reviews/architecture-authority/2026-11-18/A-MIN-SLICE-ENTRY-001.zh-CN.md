# 最小工程切片——准入契约与就绪度裁定

- 审查编号：**A-MIN-SLICE-ENTRY-001**
- 权威角色：A / 首席系统架构权威（集成提案）
- 状态：**提案 / 未获 Owner 批准 / 不构成实现授权**
- 基线：`main@e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- 分支：`review/a-minimum-slice-entry-contract-2026-11-18`
- 治理跟踪：Issue #43
- 运行时位置阻塞项：Issue #7（OPEN）
- 范围：仅定义准入条件与候选顺序；不修改实现、Schema、技术选型或 Owner 合同。

## 1. 决策

**当前不得启动生产级或受保护路径运行时垂直切片。** Issue #7 尚未确认规范运行时仓库和负责工程负责人；领域语义、授权、Forget、序列化及恢复义务仍未闭环。

因此，A 建议的第一项工程工作**不是运行时功能**，而是在相关 D/E/I/Storage Owner 精确固定并澄清合同之后，构建一个有界、仅使用合成数据的 Forget/发布安全可执行验证包。这只是候选推进顺序，不能替代 Owner 决策。

后续运行时垂直切片可以考虑最小单 Authority 的规范写入 → 持久化提交 → 权威读取链路，但必须包含 Forget/防复活和授权检查，不能退化成只验证 happy-path 的 CRUD 演示。除非经批准的产品需求证明不可或缺，否则 Provider/Applied Delivery 明确排除在首个切片之外。

## 2. 当前证据与阻塞项

当前 main 基线为 `e52594f181d2edb77448adcfed64a0fbdffaf3aa`。PR #93 记录了该提交与 main 的实时 compare 结果为 identical；从 `b3c666e...` 到该提交的 compare 显示 ahead 2、behind 0、文件变化 0。这是历史差异，不是已证明的文件树内容漂移。

| 证据 | 精确引用 | 集成含义 |
|---|---|---|
| 架构突破集成审查 | PR #93 Head `0f3ba5293add8d6147a4375796b04c8bc6ae75e1` | Forget 仍为 P0 / NOT READY；Resource Manager 和 Memory IR 仅为 Shadow 候选；没有证明架构优越性或可冻结 |
| Forget 有界模型 | PR #88 Head `bf35b32295d0d3f337c80c3dc406db0a41de6830` | 安全抽象在深度 10 内探索 606 个状态/深度对；五个弱化守卫变体产生反例。这是有界模型证据，不是生产证明 |
| Memory OS 研究 | PR #86 Head `3892916ce2379f807a0ddcd0039816f6e88ecee1` | Resource Manager 仍为候选/仅 Shadow；合成结果显示权衡，不证明普遍优越 |
| Memory IR 研究 | PR #85 Head `c5013d3585d54457f38bef37984645e2055ff7cf` | E 内部 Shadow Typed IR 仍为候选；不能决定 B 语义或替代 D Canonical Commit |
| H/C 分支完整性 | PR #90 Head `0dc8444d590cea19c9ac9bce14e8a6825d55ea01`；PR #91 Head `55c60a11aedef858d450e19391cb3fcdfabf1199` | A 记录了 H 文件树破坏性回归及 C/H 源对账风险。后续 C 审查 PR #92 报告分支已恢复；依赖任一快照前必须刷新精确实时分支/Blob Pin |
| 运行时实现权威 | Issue #7 OPEN | 可访问证据尚未确立规范运行时仓库、工程负责人/维护者、可复现 Build/CI 权威或部署/运维拓扑 |

### 不得混为一谈的阻塞事实

1. B Fact/Claim 仍为 ADR-BLOCKED；不得推断规范 Fact/Claim Schema 或 Identity。
2. I 治理/信任和封闭世界 Inventory 义务仍然阻塞。
3. D/E/I/Storage 的发布、Forget Barrier、可见性线性化、崩溃恢复和 Anti-Rollback 证据仍不完整。
4. Storage Option A 仅是已选择的 L1 逻辑方向；不能证明 L2/L3 竞态安全或 L4 物理符合性。
5. 对于不经过 Provider 的规范写入/读取切片，H/C Applied Evidence 和 Provider Integration 并非必需前置条件；不得借其未解决状态把 Applied 偷渡进首个切片。
6. PR #90/#91 与 PR #92 中 H 分支快照存在时间顺序不一致。未重新读取精确分支 HEAD、递归 Tree Inventory 和 Blob 前，本提案不接受任何 H 源版本。
7. 最近读取的 Issue #7 和评论中仍无项目权威答复。

## 3. 候选工作分解

### Stage 0——源与权威稳定化（强制，不写运行时代码）

- 每次审查前重新读取 main 和相关 Owner 分支 HEAD。
- 发布不可变 Source Manifest：仓库、分支、提交、路径、Blob SHA、决策状态、审查范围和替代关系。
- 在使用 H/C 工件前，解决 H/C Tree Integrity 事件与陈旧源差异。
- 获取 B 的明确领域决策；否则保留中性的 opaque candidate vocabulary。
- 获取 I 的精确治理/信任决策和 Inventory 闭环计划。
- 获取 D/E/Storage 对 Registration、Fencing、Visibility、事务所有权和 Recovery 的精确合同。
- 获取项目权威对 Issue #7 的答复。

**退出条件：** 候选切片所用的所有源均为当前、不可变，并由其责任 Owner 明确接受对应范围。A 报告或委派角色模拟不能替代 Owner 签署。

### Stage 1——Forget/发布安全证据（建议的首个可执行工作）

只有 Stage 0 提供精确合同输入后，才可准备有界的合成模型/符合性验证 Harness。至少覆盖：

- Forget Cutoff 前后的 Producer/Derived Work Admission；
- Register-before-visible 和 Participant Barrier；
- 可见性线性化点上的最终 Fence 与 Lineage 校验；
- 并发 Forget 操作及单调 High-water 行为；
- ACK 丢失、Retry、重复投递和幂等 Receipt Replay；
- 每个持久化边界上的 Worker 暂停/崩溃；
- Cache Refill、Index Rebuild、Stale Restore 和延迟发现 Participant；
- 未知权威状态、陈旧 Epoch/Generation、Participant 不可用时 Fail-closed；
- Quarantine / IN_DOUBT 保留，以及不得提前可见的恢复行为。

PR #88 的 606 个探索状态/深度对和变异反例只能作为起点。必须扩展状态空间并明确记录抽象缺口。不得把有界探索标记为穷尽证明或生产安全证明。

**退出条件：** 可复现模型/Harness、精确输入合同 Pin、不变量到测试的追踪关系、反例回归测试，以及 Owner 对模型与合同映射的审查。完成后不会自动获得生产部署授权。

### Stage 2——首个运行时垂直切片（有条件；当前未授权）

候选范围，须经 Owner 决策：

1. 一个明确限定的 BrainAuthority 和一个序列化域。
2. 在获批 B/I 语义下使用合成数据进行 Ingress/Admission。
3. 按已采纳 Storage 拓扑执行 D/E 负责的持久化 Registration 和 Canonical Commit。
4. Forget Barrier、最终 Visibility Gate 和防复活行为。
5. 一条权威读取路径，在读取时重新校验当前 Permission/Fence，且不能读取陈旧 Derivative/Cache。
6. 对每个状态转换提供确定性故障注入、恢复和 Evidence。

不在范围内：多 Authority 事务、生产数据、Provider Side Effect、外部 Delivery、Global Applied、分布式扩展、高级 Retrieval/Reranking、完整 Memory OS 和生产部署。

这个切片不是 CRUD 演示：只有证明持久化顺序和可见性后，写入才算接受；只有检查当前授权和 Forget 状态后，读取才算接受。

## 4. 依赖 DAG 与责任归属

```text
项目权威 / Issue #7
          |
          v
规范运行时仓库 + 负责工程 Owner
          |
          v
精确源 Manifest + 当前 Owner 决策
  |       |       |        |
  B       I       D/E      Storage
  |       |       |        |
  +-------+-------+--------+
                  |
                  v
        Forget / 发布合同
                  |
                  v
     合成模型 + 符合性验证 Harness
                  |
                  v
       Owner 审查后的安全证据
                  |
                  v
       A 的限定范围切片准入决策
                  |
                  v
       未来运行时垂直切片（另行批准）
```

| 工作 | 责任权威 | A 的职责 |
|---|---|---|
| Fact/Claim/领域 Identity | B | 检查跨模块兼容性；不决定 B 语义 |
| Permission、Trust、Inventory、治理 | I | 检查系统级闭环和证据 |
| Canonical Lifecycle、Commit 和 Forget 领域结果 | D | 检查集成和顺序；不改写 D 语义 |
| Derived Registration 和 Compilation | E | 检查发布依赖；不把 IR 变成 Canonical |
| 序列化、持久化和恢复 | Storage | 检查拓扑/物理证明边界 |
| 运行时仓库、Code Owner、CI 和运维 | 项目权威/工程领导 | 通过 Issue #7 要求证据；不臆造责任归属 |
| 系统切片准入和 Gate 裁定 | A（必要时与治理权威共同） | 证据完整后作限定范围决策 |

只有当切片跨越 Provider Request、External Delivery 或 Applied Evidence 边界时，C/G/H 才成为强制依赖。

## 5. 准入 Gate

以下条件必须全部满足；部分通过不构成实现授权。

| Gate | 所需证据 | 当前状态 |
|---|---|---|
| E0——运行时位置与责任人 | Issue #7 答复；规范仓库/分支；具名工程负责人/Code Owner；Build/Test/CI 和 Artifact SHA 来源；部署/运维拓扑 | **BLOCKED** |
| E1——领域语义 | B Fact/Claim ADR 和精确下游类型映射，或正式限定的中性词汇 | **BLOCKED** |
| E2——治理与授权 | I Policy/Trust 决策、Issuer/Key 生命周期、撤销、Inventory 和 Fail-closed 行为 | **BLOCKED** |
| E3——生命周期与发布 | D/E 精确 Admission、Registration、Fencing、Visibility 和 No-resurrection 合同 | **NOT PROVEN** |
| E4——持久化顺序与恢复 | Storage/D 精确 Option A 采纳、A-01..A-05 处置、适用于切片的 L2/L3 竞态证明与 L4 物理计划/证据 | **NOT PROVEN** |
| E5——Forget 安全 | 不变量映射至 Owner 合同和可执行故障测试；覆盖 Restore/Replica/Index/Cache | **NOT READY** |
| E6——测试隔离 | 仅合成数据、隔离环境、无生产凭据/数据/Provider Side Effect、可复现 Harness | **NOT ESTABLISHED** |
| E7——切片责任与验收 | 具名实现者/审查者/运维者；代码到合同追踪；退出和回滚授权 | **BLOCKED** |

## 6. 验收与停止标准

### Stage 1 验收

- 每个不变量都有具名 Owner 合同源，并至少有一个正向和反向测试。
- 所有反例可复现且有回归测试。
- 覆盖崩溃/Retry/Replay/Restore 和并发 Forget。
- 未知/陈旧权威状态必须 Fail-closed。
- 结果明确声明探索边界和未覆盖行为。
- A 与各相关 Owner 只接受各自负责的范围。

### 未来运行时切片验收

- 在规范运行时仓库中可复现 Build 和 CI。
- 每个范围内状态转换都有 Contract-to-Code-to-Test 追踪。
- 通过注入崩溃证明持久化状态和恢复行为。
- 定义的线性化点之后，没有读取路径可以暴露已 Forget 或未授权数据。
- 没有陈旧 Cache/Index/Replica/Restore 路径可以复活被抑制数据。
- 所有必要 Owner 对精确 Commit 和 Artifact Set 签署；A 另行给出限定范围集成裁定。
- 回滚/停止流程经过测试，且不会回滚 Forget 或 Authorization High-water 状态。

### 立即停止条件

任一源 Pin 变化、Owner 分支丢失权威文件、语义发生争议、必要 Participant 未知、权威状态不可用、恢复无法证明当前 High-water、测试要求使用生产数据/凭据，或未经明确批准尝试 Provider/外部副作用时，立即停止并退回相应权威 Owner。

## 7. 明确不授权事项

本文**不授权**：

- 在本架构仓库编写运行时代码；
- 在任何仓库开展受保护路径实现；
- 访问/写入生产或客户数据；
- Provider 调用、外部 Delivery 或副作用；
- Schema/技术冻结或采纳 Memory OS / IR 架构；
- Gate 通过、Issue 关闭、PR 合并、部署或生产激活。

在现有治理约束下，仅允许隔离文档工作和合成数据、合同中立的可行性准备。Issue #7 仍 OPEN，G3 仍 BLOCKED。

## 8. A 提议裁定

**DEFERRED / ARCHITECTURE_NOT_READY。** 将 Stage 0 设为强制前置。把 Stage 1 Forget/发布安全证据作为首个有界可执行工程工件的优先候选，但必须以精确 Owner 合同输入为前提。首个运行时垂直切片暂不选定，直至 B/I/D/E/Storage 和项目权威满足准入 Gate。

这是供审查的 A 提案，不是 Owner 决策。此 PR 保持 Draft 且不得合并。
