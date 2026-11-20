# AID-2026-014 — R3 修正状态

## 1. 权威来源

Work Item：AID-2026-014

Tracking Issue：#265

ADR 载体：#43，comment 7034237663

处置：CORR-APPLY-DISP-01

修正状态：APPLIED_PENDING_INDEPENDENT_REVIEW

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
| R1 Claim 身份 | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |
| R2 Attestor 授权 | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |
| R3 共享 Fact Forget | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |
| R4 Fact/Claim 同步 | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |
| R5 端到端发布 | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |
| R5 Storage §8.8 | NOT_APPLIED_PENDING_LOCATE | PENDING |
| PASS 治理同步 | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |

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

## 8. 应用证据

应用基线 HEAD：94cbb4dbffae9935373935f699ea74a7daee983b

应用执行：L0 登记通道（CORR-APPLY-DISP-01，finalize 6b002288），落点为 43 服务器 main 树。

下表所有 HEAD 与 Blob 均来自实际应用与回读过程返回值；不使用源会话自报 HEAD 作为应用证据。

| 文件 | 组 | Commit SHA | Blob SHA | UTC |
|---|---|---|---|---|
| docs/en/02-domain-model/domain-model-overview.md | R1 §2.4 | d575ebc254ac | 47327d8a0f26 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R1 §2.4 | d575ebc254ac | 03843f8e1d98 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R1 §2.4 | d575ebc254ac | 47327d8a0f26 | 2026-11-20T19:53:40+08:00 |
| docs/en/09-security-governance/security-governance-guide.md | R2 §12 | 9420435f8eb7 | 60b2283fdf44 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/09-security-governance/security-governance-guide.md | R2 §12 | 9420435f8eb7 | 9fee318f2def | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | R2/R4 §3.15 | 74a531814cb2 | ec4a27099b29 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R2/R4 §3.15 | 74a531814cb2 | 0b2aa1c35553 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R2/R4 §3.15 | 74a531814cb2 | ec4a27099b29 | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | R3 §8.1 | 0e8ce367de8d | 364ce11587bc | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R3 §8.1 | 0e8ce367de8d | 28695a53a26a | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R3 §8.1 | 0e8ce367de8d | 364ce11587bc | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | R4 §1/§4/§11/§12 | 1cd36650f1d3 | 46fbdcacbe8a | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R4 §1/§4/§11/§12 | 1cd36650f1d3 | d80d0515f9e0 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R4 §1/§4/§11/§12 | 1cd36650f1d3 | 46fbdcacbe8a | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/phase-1-domain-model-freeze.md | R4 phase-1-freeze | 5429eff46d76 | 80a159515717 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md | R4 phase-1-freeze | 5429eff46d76 | acf12e265b52 | 2026-11-20T19:53:40+08:00 |
| docs/en/00-governance/architecture-invariants.md | R4 arch-invariants | 088de92867fc | 4213ab67dc8a | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/00-governance/architecture-invariants.md | R4 arch-invariants | 088de92867fc | 909be080e7f5 | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/core-entities.md | R4 core-entities | 08630cf875d6 | 58fd178a7b46 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/core-entities.md | R4 core-entities | 08630cf875d6 | 998213221432 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/core-entities.md | R4 core-entities | 08630cf875d6 | 06a914699813 | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/relationships-and-provenance.md | R4 relationships | 7873b5768f65 | cbacc2344310 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/relationships-and-provenance.md | R4 relationships | 7873b5768f65 | 684cb6b15242 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/relationships-and-provenance.md | R4 relationships | 7873b5768f65 | a674e21756cd | 2026-11-20T19:53:40+08:00 |
| docs/en/03-memory-brain/memory-versioning.md | R5 memory-versioning | e8078af592ea | d6694ba1409b | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/03-memory-brain/memory-versioning.md | R5 memory-versioning | e8078af592ea | dc652751d8c0 | 2026-11-20T19:53:40+08:00 |
| docs/en/04-memory-compiler/extraction-and-normalization.md | R5 extraction §19.1 | 5bf757863cd0 | 8d408328ed0d | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | R5 extraction §19.1 | 5bf757863cd0 | 6d67d73c5cca | 2026-11-20T19:53:41+08:00 |
| docs/en/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | R5 G addendum | bcf127f07078 | 28ab2832d5f2 | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | R5 G addendum | bcf127f07078 | d651005e5a87 | 2026-11-20T19:53:41+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | PASS §13+CH | 961d2191bba6 | 443b35b288fc | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | PASS §13+CH | 961d2191bba6 | 736fc5865c54 | 2026-11-20T19:53:41+08:00 |
| 02-domain-model/domain-model-overview.md | PASS §13+CH | 961d2191bba6 | 443b35b288fc | 2026-11-20T19:53:41+08:00 |
| docs/en/00-governance/aid-2026-014-r3-correction-status.md | PASS status files | 1d9e2bd18771 | 8ad07e794f05 | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md | PASS status files | 1d9e2bd18771 | d6d7e00e03f9 | 2026-11-20T19:53:41+08:00 |

本轮未应用项（已隔离，无仓库写入）：

- G 根级 §13.3 直接整合：ANCHOR_MISMATCH（定稿第七节 6. G 载体状态；同步债务 SD-06）。根级文件 06-memory-context/context-versioning.md，Blob 05c0739d0c22576a1fd5affc7d73c078c89049b1，保持不变。新建 EN/ZH 配对补充文件不宣称根级 §13.3 已完成替换。
- Storage ADR §8.8：NOT_APPLIED_PENDING_LOCATE（定稿第八节；同步债务 SD-08）。真实可写 ADR 载体未定位；未创建替代 ADR，未向无关文档插入。

本应用证据段由应用证据提交本身加入；该提交 SHA 与状态文件终态 Blob 由 L0 应用报告及 raw 回读登记。
