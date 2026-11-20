# AID-2026-014 — R3 修正状态

## 1. 权威来源

Work Item：AID-2026-014

Tracking Issue：#265

ADR 载体：#43，comment 7034237663

处置：CORR-APPLY-DISP-01

修正状态：PROPOSED_FOR_APPLICATION

## 2. 决策状态

OWNER DECISION = DECIDED FOR CONVERGENCE

B OPTION A = DECIDED FOR CONVERGENCE

D OPTION A = DECIDED FOR CONVERGENCE

R3 审查处置 = REQUEST CHANGES（最严格原则优先）

FORMAL ACCEPTANCE = PENDING

SCHEMA FREEZE = NOT APPROVED

IMPLEMENTATION CONFORMANCE = NOT ESTABLISHED

DDL = NOT APPROVED

PUBLIC API = NOT APPROVED

H WIRE = NOT APPROVED

生产 ATTESTATION 密钥 = NOT APPROVED

TRUST ROOT = NOT APPROVED

密码学 PROFILE = NOT APPROVED

STORAGE L4 = OPEN / NOT APPROVED

TEST EXECUTION = SUSPENDED

## 3. 各项修正状态

| 要求 | 应用状态 | 独立复审 |
|---|---|---|
| R1 Claim 身份 | PROPOSED_FOR_APPLICATION | PENDING |
| R2 Attestor 授权 | PROPOSED_FOR_APPLICATION | PENDING |
| R3 共享 Fact Forget | PROPOSED_FOR_APPLICATION | PENDING |
| R4 Fact/Claim 同步 | PROPOSED_FOR_APPLICATION | PENDING |
| R5 端到端发布 | PROPOSED_FOR_APPLICATION | PENDING |
| R5 Storage §8.8 | NOT_APPLIED_PENDING_LOCATE | PENDING |
| PASS 治理同步 | PROPOSED_FOR_APPLICATION | PENDING |

## 4. 应用证据要求

每个已应用目标 MUST 记录：

1. 应用前精确仓库 Commit HEAD。
2. 精确目标路径。
3. 原始 Blob SHA。
4. 精确修改前内容。
5. 修改后 Blob SHA。
6. 修改后 Commit HEAD。
7. 实际行数变化和 Diff 统计。
8. EN/ZH 一致性证据。
9. 独立复审引用。

应用记录 MUST 使用实际应用和回读过程返回的 HEAD 与 Blob。

不得使用源会话自报 HEAD 作为应用证据。

## 5. 独立复审程序

独立复审者 MUST 检查：

1. 精确应用后的 R1 Blob。
2. 精确应用后的 R2 Blob。
3. 精确应用后的 R3 Blob。
4. 精确应用后的 R4 Blob 及交叉同步消费者。
5. 精确应用后的 R5 D/E/G Blob。
6. Storage §8.8 载体和 Blob（如已定位）。
7. EN/ZH 语义一致性。
8. R5 七列表格。
9. R5 可逆顺序标记。
10. PASS 治理和证据分离。

每项 R1–R5 都必须获得明确 PASS 或 REQUEST CHANGES 结论。

不得仅凭作者声明将任何事项标记为 CLOSED。

## 6. 测试执行门禁

R1–R5 全部通过独立复审之前，测试执行 MUST 保持挂起。

规范文件存在不代表测试 PASS。

测试用例已经编写不代表测试 PASS。

空 CI 记录、缺失 Workflow 执行或不可获取的执行输出均不代表测试 PASS。

审查 PASS 不等于 Formal Acceptance。

修正已经应用，也不代表已经独立复审；必须回读精确 Commit HEAD 和 Blob 内容后才能进行独立复审。

## 7. 最终批准边界

Formal Acceptance 继续保持 PENDING。

Schema Freeze 继续保持 NOT APPROVED。

Implementation Conformance 继续保持 NOT ESTABLISHED。

本修正状态记录不授予任何生产授权。
