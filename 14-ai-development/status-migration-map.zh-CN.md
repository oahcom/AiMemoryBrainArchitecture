# AI-STD-001 状态迁移映射（简体中文）

**工作项：** P1-T2 — 流程治理改进  
**来源：** AI-STD-001 §4.1 中真实存在的 12 个规范状态  
**目标：** 六个操作阶段；源状态作为不可变证据保留。

| 精确源状态 | 目标阶段 | 必须独立保留的证据 |
|---|---|---|
| PROPOSED、ANALYZED、PROMPT_READY | INTAKE（受理） | 发起人/Owner、影响分析、冻结提示词身份/版本/哈希及基线 |
| READY | READY（就绪） | 依赖/契约及明确的 Owner 就绪确认 |
| IN_PROGRESS、IMPLEMENTED | ACTIVE（执行中） | 分支/进度、Commit、变更文件清单和自检 |
| VERIFIED、REVIEWED、INTEGRATION_READY | VALIDATION（验证） | 准确测试证据、独立评审报告/发现处置、集成兼容证据 |
| ACCEPTED | ACCEPTANCE（接受） | 获授权主体的明确接受决定 |
| MERGED、CLOSED | COMPLETE（完成） | 合并目标/SHA，以及独立结项/索引证据 |

## 不丢失与安全规则

1. 在 source_status 中精确保留原始状态字符串，包括后缀。兼容迁移期间原 status 字段保持不变。
2. lifecycle.phase 仅表示分组。lifecycle.gates 分别记录 verified、independent_review、integration、owner_acceptance、merge、closeout。阶段不代表门禁通过。
3. VERIFIED、REVIEWED、INTEGRATION_READY、ACCEPTED、MERGED、CLOSED 仍是不同检查点。
4. BLOCKED 和 REJECTED 是正交标记，不是阶段。保留原因、责任方、已知时间及解决/处置证据，不得推断标记。
5. 架构决策生命周期/状态独立管理，不在本范围内。包括 Owner G Charter 在内的 Owner 角色定义不变。
6. 未知、缺失、有歧义或带无法识别注释的状态 fail closed，保持不变。
7. 迁移必须增量、幂等、默认 dry-run、先备份且可回滚。备份逐字节复制；回滚恢复原始字节。
8. 不得推断缺失的评审、接受、集成、合并或结项证据；缺失证据保留为 NOT RECORDED。

## 六个阶段

- INTAKE：提议、分析和提示词准备。
- READY：执行前置条件满足。
- ACTIVE：实现进行中或已提交。
- VALIDATION：验证、独立评审和集成就绪检查点。
- ACCEPTANCE：获授权主体作出的接受决定。
- COMPLETE：合并和结项检查点。

迁移工具新增 lifecycle.phase、lifecycle.source_status、lifecycle.gates、lifecycle.markers，不删除或改写历史证据。原 status 保持不变，直至另行授权完成消费者盘点和字段切换。
