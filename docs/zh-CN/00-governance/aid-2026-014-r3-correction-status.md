# AID-2026-014 — R3 修正状态

## 1. 权威来源

Work Item：AID-2026-014

Tracking Issue：#265

ADR 载体：#43，comment 7034237663

处置：CORR-APPLY-DISP-01

修正状态：APPLIED

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
TEST EXECUTION 派发门禁 = UNLOCKED-WITH-CONDITIONS（仅限 REQ-04 第⑤步派发规格）

## 3. 各项修正状态

| 要求 | 应用状态 | 独立复审 |
|---|---|---|
| R1 Claim 身份 | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R2 Attestor 授权 | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R3 共享 Fact Forget | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R4 Fact/Claim 同步 | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R5 端到端发布 | APPLIED | PASS (M19: 7050001430; M20: 7050002020; M27: 7057332489; M28: 7057332846) |
| R5 Storage §8.8 | APPLIED | PASS (M22: 7056912025; M27: 7057332489; M28: 7057332846) |
| R5 Admission 阶段关系 | APPLIED | PASS (M25: 7057203158; M26: 7057203517; M27: 7057332489; M28: 7057332846) |
| PASS 治理同步 | APPLIED | PASS (M19: 7050001430; M20: 7050002020; M27: 7057332489; M28: 7057332846) |

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

回读经由提交 fc17542d（main）及 AID-2026-014 载体审计；本轮之后变更的
三个 Blob 见本节末尾更正注。

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

- G 根级 §13.3 直接整合：已应用。根级文件 06-memory-context/context-versioning.md 已重建为根级规范来源（提交 2606978e，Blob 8503a171922a27aca469042164b2e14f5f525910）。补充文件 Blob 249fd8691707（EN）与 aed4f80857de（ZH）已并入该节，不再宣称独立竞合协议。§14.5 随后对齐为 §13.3 的下位约束（提交 fc17542d，Blob dbce95485d02c8b25bfa2c13596c32d0d57b341d）。此前对 Blob 05c0739d... 的开放态读取已被取代。
- Storage ADR §8.8：已应用。载体分支 session-storage-consistency-forget-atomicity-2026-11-16，路径 reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md。应用提交 9f63874ecf2c4d8292435c8c10d0b7b4fe9c620f；Blob bb544ba2f346bdc130d524bd5c7310d86f367988 -> edd81e2ba21c752fc88fa5e1c3cf2f2cca8cf603（27834 -> 29945 字节，274 -> 333 行）。第 8 节现自 8.1 连续至 8.8。8.8 双语正文取自 Issue #265 评论 7037252404 的 Owner 文本，按 ADR 既有双语惯例逐字应用。既有 L1 决策与 Storage L4 OPEN 边界均保留；8.8 不选择新拓扑。NOT_APPLIED_PENDING_LOCATE 撤回：先前的递归树检索仅覆盖 main，而 prompt 钉定的载体位于 Storage Owner 分支。F-265-STORAGE-01 / SD-08 以此记录关闭。跨分支规范性共存登记为后续事项，不构成本次应用的阻断。

本应用证据段由应用证据提交本身加入；该提交 SHA 与状态文件终态 Blob 由 L0 应用报告及 raw 回读登记。

## 9. 更正注 —— R5 应用轮次后的回读

上文第 8 节写于三个 Blob 变更之前。本注为回读结果，按第 4 节「应用记录必须携带实际 HEAD 与
Blob 值」的要求取代相应行。

| 目标 | 被取代值 | 当前值 | 提交 | 说明 |
|---|---|---|---|---|
| 06-memory-context/context-versioning.md | 05c0739d0c22 | dbce95485d02 | fc17542d | §13.3 重建为根级规范来源（2606978e，8503a171），随后 §14.5 对齐为 §13.3 的下位约束。该根级文件仅英文；此前与此后均无同路径中文对应文件。 |
| docs/en/00-governance/aid-2026-014-r3-correction-status.md | 8ad07e794f05 | d9b3a9141c71 | 8b9cb119 | 状态表翻转为 FIX_APPLIED_AWAITING_REREVIEW / APPLIED_PENDING_INDEPENDENT_REVIEW。 |
| docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md | d6d7e00e03f9 | 706c4da352e5 | 8b9cb119 | 经 25c61283 恢复至配对位置；927eadcb 曾将其单独重命名至 docs/governance/archive/，孤立的归档副本已移除。 |

Storage §8.8 **不在**本仓库 `main` 树中。其已应用状态位于载体分支
`session-storage-consistency-forget-atomicity-2026-11-16`，提交 `9f63874e`，Blob `edd81e2ba21c`。
该分支即 Storage owner 分支，其 Tip `281fd1ed` 与 L1 topology Blob `bb544ba2` 由
AID-2026-014-PROMPT v1 钉定。在该分支上应用是正确处置；将 ADR 复制进 `main` 会产生第二个规范副本，
故未执行。

后续开放事项（不构成 R5 阻断）：跨分支规范性共存尚无 Owner 裁决。在裁决作出前，该 ADR 在其自身分支上
具权威性，且不得镜像。

R3 复审处置、正式验收、Schema 冻结与实现一致性均不因本注改变。七行独立复审状态仍全部为 `PENDING`。

### 9.1 R1 与 R4 修正轮的钉定回读

回读基线 HEAD：`dd4ecf167c4af4ccb911f18dcfca2ca849f0b650`。下表所有 Blob 均读自该确切提交，而非漂移中的分支头。此举是有意的：
在撰写本注期间，`main` 已从 `92459e0f` 经 `1733c3bf` 推进到 `dd4ecf16`，其中
`memory-versioning.md` 在该窗口内被改动了两次。不指明基线的回读不构成证据，故此处以钉定提交
满足第 4 节要求。

| 组 | 本轮改动内容 |
|---|---|
| R1/R4 | 确认 Canonical Claim identity 语义为 DECIDED；从领域模型 Overview 与 phase-1 Freeze 中删除过期的 `OPEN` 条款（6 条，EN/ZH/根级）。 |
| R1 消费者 | 下游文本对齐至已决的 Claim identity 语义。 |
| R4/R5 消费者 | Extraction 区分 Claim identity、Fact 专属建模与物理 Schema 三者。 |
| G | 确立第 13.3 节为根级规范来源；第 14.5 节作为其从属约束对齐。 |

| 目标 | 组 | 本轮回读所取代的值 | 基线 HEAD 处 Blob | 产生该 Blob 的提交 |
|---|---|---|---|---|
| docs/en/02-domain-model/domain-model-overview.md | R1/R4 | 46fbdcacbe8a | 5b86fe23ab7c670b4ae13331b56572aee35f5d00 | bc114263 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R1/R4 | d80d0515f9e0 | 03129ded6e9532048240aea3a18414370cbcb73d | bc114263 |
| 02-domain-model/domain-model-overview.md | R1/R4 | 46fbdcacbe8a | 5b86fe23ab7c670b4ae13331b56572aee35f5d00 | 778d1bee |
| docs/en/02-domain-model/phase-1-domain-model-freeze.md | R4 | 80a159515717 | 1a18c6b8424c939dd90986527a24807c8f74d552 | bc114263 |
| docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md | R4 | acf12e265b52 | 408a606c44fcf271f265508bc9d3029f8fc889cb | bc114263 |
| 02-domain-model/phase-1-domain-model-freeze.md | R4 | 第 8 节未登记 | d1102a0adf32e3f7b3eb9091758823f990a2a37c | ae5a886f |
| docs/en/03-memory-brain/memory-versioning.md | R1 消费者 | d6694ba1409b | 7e63b9b397c3bdff1567dab421f658af86ee1a48 | 5ed9669d |
| docs/zh-CN/03-memory-brain/memory-versioning.md | R1 消费者 | dc652751d8c0 | 89d9eb4786615cc43f7098b206c1ccd446536fa2 | 9c94b3c4 |
| docs/en/04-memory-compiler/extraction-and-normalization.md | R4/R5 消费者 | 8d408328ed0d | 10c46fd79c53c54a77f8bd2c91107a4b2aeaabda | 39553c25 |
| docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | R4/R5 消费者 | 6d67d73c5cca | cec9cf3185659b8d9ba1dd916674f71dd4fce808 | 39553c25 |
| docs/en/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | G | 28ab2832d5f2 | 190bd11d8226d6e6e3c97ad37b700d43b8b70720 | ae5a886f |
| docs/zh-CN/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | G | d651005e5a87 | 47d9fe9b7387c843f09f519519b14e998a1a65c7 | ae5a886f |
| 06-memory-context/context-versioning.md | G 根级 | 05c0739d0c22 (§8 bullet) | 847c9578b4404c1a034fe62ee9bbffa598f7ab2e | ae5a886f |

有两行需说明。根级 `02-domain-model/phase-1-domain-model-freeze.md` 在第 8 节中并无登记，
故无可援引的被取代值；`第 8 节未登记` 为字面陈述，非占位符。根级
`06-memory-context/context-versioning.md` 在第 8 节中不是表格行，而出现在「本轮未应用」条目
之内，故其被取代值附 `（§8 条目）` 限定。

R4 的闭合是实质性的，非文字性的。`10c46fd7` 拆开了此前被混为一谈的三个问题：canonical
Claim identity 语义为 `DECIDED FOR CONVERGENCE` 且由 D 治理；Fact 专属建模与 Fact 批准在
INT-P0-01 下仍为 `OPEN`；物理 Schema 与 DDL 仍为 `NOT APPROVED`。`ADR-BLOCKED` 已不再描述
Claim identity mapping。此前独立复审在此点上的结论读自 `2717fadb`，该版本已被取代。

此前版本的 §3 曾使用两个状态值：`FIX_APPLIED_AWAITING_REREVIEW` 与
`APPLIED_PENDING_INDEPENDENT_REVIEW`。在当时，二者表示同一确定性等级，并非两个档次：应用已完成、
独立复审尚未完成，仅产生该应用的轮次不同。二者属于历史状态值，不再描述当前 §3。
当前 §3 各行记录为 `APPLIED`，并同时记录独立复审结果。

上表不含两个状态文件自身，因为本小节即随它们一同提交：其提交前 Blob 为 `db3e9f394c61c247ae9dde51c92d190f194ee11a`（EN）与
`87c00ade741ebc0837c2f6903b820741f2887e4a`（ZH），由新增本小节的提交取代。

### 9.2 Admission 阶段关系轮次回读

回读基线 HEAD：`da378340b0c7adb0ad3c1f128878bc96804c78d9`。两个提交闭合了独立复审提出的最后一项实质问题。

| 目标 | 提交 | 修改前 Blob | 修改后 Blob | 大小 |
|---|---|---|---|---|
| docs/en/04-memory-compiler/extraction-and-normalization.md | da378340 | 10c46fd79c53 | 03c8a6f32113d54cac097c792b896a4ec3f873b1 | 18070 -> 20841 B |
| docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | da378340 | cec9cf318565 | ac484c860b9b8eb9da19801acd9a985f2a8b4b3a | 17662 -> 20233 B |
| reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md（载体分支） | a5a13d63 | edd81e2ba21c | 8d4ac845f409c2cb64831c850219fdb84a113cf0 | 29945 -> 32954 B |

缺口在于两个准入名称从未相遇。Extraction 只写 `Producer Admission`，位置在 D canonical commit
之前；Storage ADR §8.8 只写 `PublicationParticipant Admission`，位置在 D canonical commit 与
Storage 将准确 publication tuple 持久化为 `PREPARED_HIDDEN` 之后。在当时的文件状态下，同名动作
带有两个互相矛盾的位置，且没有任何文字说明它们是不同的动作。

所落文本裁定二者为两个不同的有序阶段，既非别名，也非可互换的决定。Producer Admission 在依赖
集合登记和规范提交之前准入准确的 Producer/ProducerWork 身份。PublicationParticipant Admission
在规范提交与 PREPARED_HIDDEN 持久化之后，准入绑定对应 StorageVisibilityParticipantRef 与
publication tuple digest 的准确 PublicationParticipant。前者的成功明确不等于后者的成功。二者
均须与各自的 participant 记录构成不可分操作，均针对同一权威排序锚点串行化。在 Producer
Admission 与依赖集合登记阶段建立的 dependency closure，在发布时不得被创建、替换、缩减或独立
重新定义。

Extraction 以新增 §19.2 承载，插入在该文件既有 `#### Storage 边界` 小节之前。该小节原有的两句
边界声明未改动，§19.2 未重复陈述它们。ADR 以 §8.8 内部澄清承载，位置在七步顺序之后、
per-BrainAuthorityRef 序列化锚点声明之前。七步顺序、锚点、L1 决策与 L4 OPEN 边界均未触及。

两处插入均声明这是 implementation-conformance gate，而非尚未解决的规范排序选择，故本次修正不
重新打开任何已 DECIDED FOR CONVERGENCE 的内容。

R3 处置、正式验收、Schema 冻结与实现一致性均不变。

### 9.3 修正轮的独立复审处置

复审方：独立会话 `6b00a00c-3ad0-83ee-bda0-f6dcdef2fbd9`（只读，未写仓库，未由复审方发布评论）。
2026-11-21 返回裁决：对仍被阻断的三项判 `PASS`，取代此前就该三项作出的 `REQUEST CHANGES`。

复审方读取的是文件本身，而非 L0 摘要。其所引 Blob 经事后核对与仓库一致：

```
docs/en/04-memory-compiler/extraction-and-normalization.md   03c8a6f32113d54cac097c792b896a4ec3f873b1
docs/zh-CN/04-memory-compiler/extraction-and-normalization.md   ac484c860b9b8eb9da19801acd9a985f2a8b4b3a
reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md（载体分支）   8d4ac845f409c2cb64831c850219fdb84a113cf0   32954 B
```

| 受审项 | 此前 | 现 | 复审方自述的核查内容 |
|---|---|---|---|
| R5 Admission 阶段关系 | REQUEST CHANGES | PASS | 两个不同的有序阶段；`MUST NOT be treated as aliases`；第一阶段成功明确不等于第二阶段成功；两者同处一个排序锚点；依赖闭包在 Producer Admission 建立，发布时不得缩减。 |
| R4 Claim identity / Fact modeling | REQUEST CHANGES | PASS | 重读了当前 Blob，而非沿用旧的 `2717fadb` 结论。`OPEN` 现仅界定 Fact 专属建模与 Fact 批准。未发现把未决项重新包装为已闭合。 |
| Application evidence §9.1 + §9.2 | REQUEST CHANGES | PASS | 修正记录连续：目标、修改前后 Blob、提交、大小、原因齐备。复审时全部复审状态仍为 `PENDING`，未预支复审结论。 |
| Storage §8.8 对齐 | PASS | PASS | 七步顺序未被改写；§8.8 澄清仅声明其之前存在独立的 Producer Admission。 |
| 双语同步 | PASS | PASS | EN/ZH 承载相同规范内容。 |

`PASS` 不代表什么，由复审方明示并在此保留：

- 不代表正式验收。`FORMAL ACCEPTANCE = PENDING` 不变。
- 不代表 Schema 冻结。`SCHEMA FREEZE = NOT APPROVED` 不变。
- 不代表实现一致性。`IMPLEMENTATION CONFORMANCE = NOT ESTABLISHED` 不变，且 `DDL`、
  `PUBLIC API`、`H WIRE`、`PRODUCTION ATTESTATION KEYS`、`TRUST ROOT`、
  `CRYPTOGRAPHIC PROFILE` 均仍为 `NOT APPROVED`，`STORAGE L4` 仍为 `OPEN`。
- 不重新打开任何 `DECIDED FOR CONVERGENCE`。

复审方主动保留一项实现门禁：必须由并发交错测试证明，在依赖闭包尚未完整进入 participant
barrier 时，Forget Fence 不得完成处置。这属于实现一致性验证，不是尚未解决的排序选择，且不能
由文本存在本身满足。

`R1`、`R2`、`R3`、`R5 端到端发布`、`PASS 治理同步` 本轮未被重新裁定，仍保持 `PENDING`。故整体
处置范围窄于本轮的 `PASS`：三行发生变更，五行未变，验收门禁完全未动。
### 9.4 第二轮独立复审 —— 要求修改

复审方：独立会话 `6b0112a2-7b64-83ee-a29b-da285ff8d589`（只读，未写仓库，未由复审方发布评论）。
2026-11-21 返回裁决。回读钉定：`8dc92c3debde36929d34808bead0a62ffc4f64fa`。十二个 Blob 均读自该确切提交。

这不是 §9.3 的重跑。§9.3 覆盖当时被阻断的三项；本轮覆盖 §9.3 留在 `PENDING` 的四项。本节取代
§9.3 末段以及 §9 中「七行仍全部为 PENDING」一句：二者描述的是本裁决之前的状态，当前状态以 §3
为准。

复审方核对过的 Blob 身份，全部 MATCH：
```
docs/en/09-security-governance/security-governance-guide.md        60b2283fdf44d116fa59fe84eaab217b435fbe70  15171 B
docs/zh-CN/09-security-governance/security-governance-guide.md     9fee318f2def690b3db9386d938df790292fb05f  13359 B
docs/en/03-memory-brain/memory-versioning.md                       7e63b9b397c3bdff1567dab421f658af86ee1a48  33424 B
docs/zh-CN/03-memory-brain/memory-versioning.md                    89d9eb4786615cc43f7098b206c1ccd446536fa2  31768 B
docs/en/02-domain-model/domain-model-overview.md                   5b86fe23ab7c670b4ae13331b56572aee35f5d00  26974 B
docs/en/04-memory-compiler/extraction-and-normalization.md         03c8a6f32113d54cac097c792b896a4ec3f873b1  20841 B
docs/zh-CN/04-memory-compiler/extraction-and-normalization.md      ac484c860b9b8eb9da19801acd9a985f2a8b4b3a  20233 B
docs/en/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md   190bd11d8226d6e6e3c97ad37b700d43b8b70720  2822 B
docs/zh-CN/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md   47d9fe9b7387c843f09f519519b14e998a1a65c7  2626 B
06-memory-context/context-versioning.md                            847c9578b4404c1a034fe62ee9bbffa598f7ab2e  32435 B
docs/en/00-governance/aid-2026-014-r3-correction-status.md         0047e6fc83b50eb561ebfc5f7b5440448435d79a  22544 B
docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md      4b41c177f1707be1b24334df60ca85c95974c612  21054 B
```

| 项目 | 裁决 | 阻断编号 |
|---|---|---|
| R2 Attestor 授权 | REQUEST CHANGES | R2-01 |
| R3 共享 Fact Forget | REQUEST CHANGES | R3-01 |
| R5 端到端发布 | REQUEST CHANGES | R5-01、R5-02 |
| PASS 治理同步 | PASS | — |
| R4 Fact/Claim 同步 | PASS，继承 | 未重新裁定 |
| R5 Storage §8.8 | PASS，继承 | 未重新裁定 |
| R5 Admission 阶段关系 | PASS，继承 | 未重新裁定 |

**R2-01 —— 授权决定未绑定唯一 Attestation 操作。** I/D 分工本身通过：§1 将全局身份与授权策略、
Delegation、Revocation 归 I；§12.1 明确 I 是 Attestor 授权的唯一治理决策权威，禁止 D 自行判断授权
资格或重新解释决定，D 只做验证。撤销侧也是充分的：§12.3 要求 PrincipalRef、精确 ScopeRef、
Method 与不可变 Version、有效期与授权 Epoch、撤销身份与 currentness、Delegation 的显式
`ALLOWED`/`PROHIBITED`、不可变 `AuthorizationDecisionRef` 以及策略 Provenance；§12.4 缺失即 fail
closed；§12.5 禁止静默改写历史。缺口在单次用途绑定。§12.2 在 FactRevision 上保存授权决定引用，但
§12.3 的字段清单未要求绑定唯一的 `AttestationOperationRef`、精确目标 `FactRef`/`FactRevisionRef`、
该次操作的精确 `ClaimRevisionRef` 集合、精确 `EvidenceRef` 集合，也未要求一次性消费或防重放状态。
§12.6 的 D 验证清单同样从不要求验证「该决定绑定于当前唯一 Attestation 操作」。由此产生的重放解读是
具体的：一个决定被第二个 FactRevision 引用时，满足现有全部显式 Scope、Method 与有效期检查，当前
文本没有任何一句禁止；而且两个 FactRevision 各自持有引用，并不能证明该决定只用过一次。修正只要求
语义契约，不要求批准 Schema、DDL 或 Public API。

**R3-01 —— 六分量矩阵缺少 Forget 终态映射。** 共享闭包规则通过。`§8.1` 要求 Forget 作用于完整依赖
闭包：精确 Claim/Fact Revision 引用、Evidence 及其独立治理与来源 Payload、可重构 Provenance、派生
MemoryVersion 与 ContextVersion、Index 与 Cache 的清理及读路径抑制、Snapshot/Staging 纳入依赖清单、
Replay/Retry/Recovery 的历史读取检查、Export 的授权与 Forget 检查、Backup 保留副本、Restore 在查询
或投递前重新检查。其三条约束是实质部分：共享 Fact 不得让多个 ClaimRevision 共享同一 Forget 处置；
剩余合法内容无法安全隔离时必须抑制整个受影响 FactRevision；依赖集合未知或不完整时不得宣告 Forget
完成。§19.1 也未留下合法的「先发布、后登记」路径：第 3 步先持久化完整直接与传递依赖集合，第 5 步
才允许规范提交，第 7 步才允许 E 发布。缺的是另一件产物：I Security Guide §7 定义了四种操作终态
——`Completed`、`CompletedWithPolicyException`、`Failed`、`Cancelled`——而 §16.1 没有把四种终态映射
到六个分量上。复审方点出四个当前矩阵答不出的问题：`Cancelled` 是否允许已提交的 Canonical Revision
保留；`Failed` 在 E 发布已发生而 Storage Visibility 未发生时如何终结；`CompletedWithPolicyException`
是否允许 G ContextVersion 提交，还是只允许隐藏态；哪些终态必须完成全部六个分量，哪些可以以抑制
处置结束。当前行为只能从「已声明的完成/抑制策略」推断，无法由矩阵逐项核验。这只要求一张终态 ×
分量处置表，不要求为每种故障复制一份矩阵。

**R5-01 —— 第二阶段 Fence-first 的结果未定义。** 一个原有 T17 未覆盖的竞争窗口：Producer Admission
成功且 participant 记录已持久化；依赖登记与规范提交成功；E 发布已产生对象，Storage 已将准确 tuple
持久化为 `PREPARED_HIDDEN`；随后 Forget Fence 与 PublicationParticipant Admission 竞争，Fence 先
线性化，第二阶段准入无法成功。§19.2 已确定排序锚点、第二阶段成功与 participant 记录的不可分性、
不得越过未解决已准入 participant barrier、不得替换 participant 身份。但它没有说明已经存在的对象
如何终结，留了五个问题：已提交的 Canonical Revision 是否永久不可公开；已存在的 E Publication 如何
处理；`PREPARED_HIDDEN` tuple 必须取消、隔离，还是保留为待处置态；第一阶段的 participant 处置如何
关联到一个从未成功准入的 PublicationParticipant；以及如何证明该隐藏 tuple 不会经恢复、重试或另一条
发布路径重新可见。

**R5-02 —— 六分量矩阵仍只有一个 `Admission` 列。** §16.1 仍写作
`D Fence → Admission → D Canonical Commit → E Publication → Storage Visibility → G Context Commit`，
而 §19.2 现已定义两个准入。Fence 在 Producer Admission 之前、两个准入之间、或在
PublicationParticipant Admission 成功之后线性化，三者留下的持久记录、可见性状态与最终处置各不相同，
而 T17/T18 只命名了第一种时序。

本裁决不做什么，由复审方明示并在此保留：

- 不重新打开 `DECIDED FOR CONVERGENCE` 的发布顺序、两准入区分、R4 三层拆分，或已应用的 Storage
  §8.8 位置。
- 不指控生产数据泄漏。R3 的发现针对规范可核验性；复审方明确记录目前没有已知的「已发布但未登记
  依赖」生产实例。
- 不改变任何验收门禁。§2 逐行未变。
- 不授权测试。`TEST EXECUTION = SUSPENDED` 维持，复审方给出的是前置条件而非执行许可。

复审方还回读了载体分支上的 Storage ADR §8.8 Blob（`8d4ac845f409c2cb64831c850219fdb84a113cf0`），
陈述其七步顺序与两个 Admission 定义和 Extraction §19.2 一致，但未重新裁定 ADR 正文。

交给本轮修正的 SYNC 事项（EN 与 ZH 同步，不只改英文）：

| 编号 | 目标 | 改动 |
|---|---|---|
| SYNC-01 | Security Guide §12.3 | 绑定唯一 Attestation 操作及其目标；禁止跨操作重放 |
| SYNC-02 | Security Guide §12.6 | 要求 D 验证操作身份、目标集合与消费状态 |
| SYNC-03 | Domain Model §8.1 | 保留闭包规则；增加其与 Forget 终态的对应关系 |
| SYNC-04 | Memory Versioning §16.1 | 增加 Forget 终态 × 六分量处置矩阵 |
| SYNC-05 | Extraction §19.1 / §19.2 | 补全第二阶段 Fence-first 与 Participant-first 处置 |
| SYNC-06 | Memory Versioning §16.1 | 区分 Producer Admission 与 PublicationParticipant Admission |
| SYNC-07 | G §13.3 | 明确第二阶段被拒绝时的不发布与恢复约束 |

复审方给出的测试前置条件，须先满足后才谈是否解除挂起：R2 的唯一操作绑定与跨 FactRevision 复用拒绝
测试；R3 的多 ClaimRevision 共享 Fact Forget、Evidence 与 Provenance 独立依赖、Export/Backup/Restore
路径、四种终态在六分量上的处置、依赖登记不完整时阻断提交；R5 的 `T17-P`、`T18-P`、`T17-PUB`、
`T18-PUB`、两准入并发交错、Fence 与 `PREPARED_HIDDEN` 竞争、崩溃、Lost ACK、重试与恢复、不得出现
重复可见的 Revision/Publication/ContextVersion、Fence 不得在 participant barrier 未解决时完成。准入
成功与 participant 持久记录必须在两个阶段分别成立，不能只验证第一阶段。

§3 的「应用状态」列保持原样：上一轮的应用仍在树中。变化的是「独立复审」列，这也是四行变更、验收
门禁一行未动的原因。

### 9.5 七项 SYNC 事项的应用

回读基线 HEAD：`836dc1055547f1dd9fba2081a5280ef22cbb94c5`。下表所有 Blob 均读自该确切提交。

七项事项分三次提交应用，随后发现一处缺陷并在第四次提交中移除。下表记录的是仓库当前持有的值，
不是某次更早提交持有的值。

| 目标 | 事项 | 变更前 Blob | 变更后 Blob | 大小 | 提交 |
|---|---|---|---|---|---|
| `docs/en/09-security-governance/security-governance-guide.md` | R2 / SYNC-01+02 | `60b2283fdf44` | `061c5847b3df` | 15171 -> 20714 B | `782c4c8d` |
| `docs/zh-CN/09-security-governance/security-governance-guide.md` | R2 / SYNC-01+02 | `9fee318f2def` | `372d27c79dc7` | 13359 -> 18224 B | `782c4c8d` |
| `docs/en/03-memory-brain/memory-versioning.md` | R3+R5 / SYNC-04+06 | `7e63b9b397c3` | `84aabc25bb07` | 33424 -> 48474 B | `9eca5eda` |
| `docs/zh-CN/03-memory-brain/memory-versioning.md` | R3+R5 / SYNC-04+06 | `89d9eb478661` | `aa2fc775c786` | 31768 -> 44569 B | `9eca5eda` |
| `docs/en/02-domain-model/domain-model-overview.md` | R3 / SYNC-03 | `5b86fe23ab7c` | `1a1a10b24d68` | 26974 -> 28507 B | `9eca5eda` |
| `docs/zh-CN/02-domain-model/domain-model-overview.md` | R3 / SYNC-03 | `03129ded6e95` | `8ef976789af6` | 24417 -> 25636 B | `9eca5eda` |
| `docs/en/04-memory-compiler/extraction-and-normalization.md` | R5 / SYNC-05 | `c87860706313` | `e6aad4b7504f` | 22484 -> 26256 B | `d36c27c9` |
| `docs/zh-CN/04-memory-compiler/extraction-and-normalization.md` | R5 / SYNC-05 | `9657949af482` | `8dd0b5b29ecd` | 21781 -> 25185 B | `d36c27c9` |
| `06-memory-context/context-versioning.md` | R5 / SYNC-07 | `847c9578b440` | `ce952ba3eca3` | 32435 -> 34566 B | `d36c27c9` |

**SYNC-01 与 SYNC-02 —— 授权决定现为单次使用。** `§12.3` 在原有七项之后新增三个编号字段：
绑定唯一 `AttestationOperationRef` 并指明该操作所针对的确切 `FactRef`/`FactRevisionRef`；
绑定确切的 `ClaimRevisionRef`、`EvidenceRef` 集合，以及在 Provenance 构成被证明输入时绑定确切的
`ProvenanceRef` 集合，并明确禁止未指定、事后扩张、替换或隐式解析的集合；以及一次性消费与防重放
状态，用于区分未使用与已被其唯一绑定操作消费的决定，一旦消费，该决定 MUST NOT 再授权另一操作、
FactRevision、目标、ClaimRevision 集合或 Evidence 集合。`§12.6` 新增对应的 D 验证职责：验证
`AuthorizationDecisionRef` 绑定于当前唯一操作、验证确切目标与确切输入集合、验证消费状态。结尾段
明确整组要求是语义契约与实现一致性边界，不是 Schema、DDL 或 Public API 的批准。

**SYNC-03 —— 闭包规则现与终态对接。** `§8.1` 原有闭包规则全部未改，新增其与 Forget 终态的对应
关系：依赖闭包不完整时不得声明任何终态；`Failed` 与 `Cancelled` 必须处置每一个已登记依赖，而不只
是发起对象。共享 Fact、整体抑制受影响 FactRevision、闭包未知即阻断这三条规则未动。

**SYNC-04 与 SYNC-06 —— 矩阵现命名两个准入并映射四种终态。** `§16.1` 不再写 `Admission`。七个
逻辑分量为 `D Fence`、`Producer Admission`、`D Canonical Commit`、`E Publication`、
`PublicationParticipant Admission`、`Storage Visibility`、`G Context Commit`，并明确两个准入
MUST 保持区分，MUST NOT 互为别名或可互换操作。九步执行顺序将 Producer Admission 置于第 2 步、
PublicationParticipant Admission 置于第 7 步，即第 6 步 `PREPARED_HIDDEN` 持久化之后。新增的
`Forget 终态 × 分量处置` 矩阵为七个分量在 `Completed`、`CompletedWithPolicyException`、
`Failed`、`Cancelled` 四种终态下分别给出处置，并给出每种终态最后允许可见的分量、已提交规范
Revision 的处置、已存在 E Artifact 的处置、`PREPARED_HIDDEN` tuple 的处置、所需审计证据以及
UNKNOWN 禁令。四条分类规则使四种终态互斥，其中包括：存在权威取消结果时 MUST NOT 声明 `Failed`；
执行失败 MUST NOT 被改写为 `Cancelled`。

**既有场景矩阵保留原有行。** 仅其 `Admission` 列名改为 `Producer Admission`。
`Fence before Admission (T17)`、`Fence after Admission (T18)`、崩溃、Lost ACK、重试与可见性后
崩溃各行含义未变。另设 `Second-stage Admission race matrix`，新增 `T17-P`、`T18-P`、`T17-PUB`
与 `T18-PUB`，并明确其不重新解释、也不替换第一阶段场景。

**SYNC-05 —— 第二阶段被拒绝现有终态处置。** Extraction `§19.2` 在现有正文与 `#### Storage
boundary` 之间新增 `T17-PUB`/`T18-PUB` 块，该边界的原两句声明未改动。该块逐条闭合五个开放问题：
已提交规范 Revision 保持已提交但永久不可公开，对同一被拒绝操作的重试不构成独立授权；已存在的
E Publication 撤销公开可见性或被隔离，且不得作为成功可见效果重放；`PREPARED_HIDDEN` tuple 取消
或隔离并具可审计终态结果，未解决的 tuple 不得视为已取消或可发布；第一阶段 Producer participant
获得可审计的抑制处置，且必须绑定确切的被拒绝 `PublicationParticipant` identity、其
`StorageVisibilityParticipantRef` 与确切 tuple identity，泛化的操作级抑制明确不满足要求；
恢复、重试与替代发布路径在作任何可见性推进前都必须验证已证明的第二阶段准入与独立授权的可见性
结果，证据缺失、冲突或 UNKNOWN 一律失效关闭。该块明确不改变 `§19.1` 的十步顺序，也不改变
`§19.2` 的六步顺序。

**SYNC-07 —— G 在第二阶段缺失时拒绝。** `06-memory-context/context-versioning.md` `§13.3` 在
`#### 4. T18 — Participant-first` 末尾新增一块：第二阶段准入未成功时 MUST NOT 提交或发布对应
`ContextVersion`；第一阶段成功不构成第二阶段成功的证据；已提交且引用了未获第二阶段准入的发布
对象的 `ContextVersion` 按 `§16.1` 终态处置；恢复与重放在每次读取时重新评估，历史提交不赋予
永久可见性；发布 identity、各参与方、闭包与终态 Forget 处置必须全程保留。
`#### 5. G protected commit requirements` 与 `#### 6. Historical visibility` 未改动。

**一处引入后又移除的缺陷。** R2 交付中每语言夹带了三行 HTML 注释，那是作者写给自己的落文指令，
不是规范正文：`§12.3` 与 `§12.6` 内各有一行 `insert after`，`§12.6` 末尾另有一行 `append`。它们
随 `782c4c8d` 一同进入仓库。提交 `836dc105` 移除这三行注释及其后随的空行，段落间距因此不变；
编号、D 的十二项验证职责与语义契约段逐字节相同。之所以记录，是因为只显示最终 Blob 的应用记录会
掩盖仓库曾短暂携带非规范标记这一事实。

清理完成后，九个目标全部在 `836dc1055547f1dd9fba2081a5280ef22cbb94c5` 处重新回读，均不含 HTML 注释。

R3 复审处置仍为 `REQUEST CHANGES`：三个阻断项已应用但尚未复审。`TEST EXECUTION = SUSPENDED`
维持。验收门禁未变：`§2` 在四次提交之间逐字节相同。

### 9.6 第三轮独立复审及其两项阻断的闭合

复审方：独立会话 `6b012e23-5ff0-83ee-95e1-1bea41ad85cf`（只读，未写仓库，未由复审方发布评论）。
2026-11-21 返回裁决。回读钉定：`7d2233a5bee2369fbb6358374ec5c2f049de88df`。

七项中五项通过：R2-01 单次用途绑定、R3-01 终态映射、R5-01 第二阶段收敛、双语一致性、
应用记录审计。两项阻断保留，均由 `3b452dbe` 闭合。

| 审查项 | 裁定 | 阻断编号 |
|---|---|---|
| R2-01 授权单次用途绑定 | PASS | — |
| R3-01 Forget 终态映射 | PASS | — |
| R5-02 两准入阶段 | REQUEST CHANGES | R5-02-01 |
| R5-01 第二阶段收敛 | PASS | — |
| SYNC-07 G 侧约束 | REQUEST CHANGES | SYNC-07-01 |
| 双语一致性 | PASS | — |
| 应用记录真实性（9.5） | PASS | — |

**R5-02-01 —— 第二阶段准入缺少不可分条款。** `§16.1` 原已要求成功的 Producer Admission 与精确
准入 Producer 参与者的持久记录构成不可分割的操作。第二阶段准入写明了它绑定哪个身份、禁止缩小
闭包，却从未禁止「第二阶段准入已成功、而其确切 participant 记录尚未持久」这一状态。Fence 因此
可能观察到准入而未观察到记录。修正补上对称要求：成功的 `PublicationParticipant` Admission 与
确切的已准入 `PublicationParticipant` identity、其 `StorageVisibilityParticipantRef`、以及绑定于
已提交发布身份的确切发布元组的持久记录，构成不可分割的操作；该中间状态 MUST NOT 存在；Forget
Fence MUST NOT 在观察到成功的第二阶段准入时，未能同时观察到该次确切准入对应的完整持久
participant 记录。

**SYNC-07-01 —— G 指向了错误的矩阵。** `§13.3` 原文称已提交的 `ContextVersion` 按
`six-component` 保护性发布失败矩阵取得终态处置。该名称指的仍是为保持 T17/T18 行义而保留的旧场景
矩阵，不是新增的终态处置产物。修正把该句重新指向 Forget 终态 × 分量处置矩阵，写明其维度（四种
终态 × 七个逻辑分量），并把 `G Context Commit` 的处置与适用终态绑定：`Failed` 与 `Cancelled` 下
MUST NOT 提交；`CompletedWithPolicyException` 下仅在例外获得具名批准且全部前置条件满足时才可提交；
`Completed` 下须满足完整完成要求。原有「不得仅因规范提交曾成功就保留或暴露为成功可见发布」这一
禁令保留。

`six-component` 一词在文件中仍恰好保留一处，位于 `§13.3` 既有的那句「六分量矩阵对由受保护
Claim/Fact 内容派生的 G `ContextVersion` 提交具有规范约束力」。该句在本轮之前是正确的，现在仍然
正确：旧表确实有六个分量列。错的只是新增块里的引用。

| 目标 | 变更前 Blob | 变更后 Blob | 大小 |
|---|---|---|---|
| `docs/en/03-memory-brain/memory-versioning.md` | `84aabc25bb07` | `4efbd26db958` | 48474 -> 49348 B |
| `docs/zh-CN/03-memory-brain/memory-versioning.md` | `aa2fc775c786` | `5ff17ab6cb56` | 44569 -> 45301 B |
| `06-memory-context/context-versioning.md` | `ce952ba3eca3` | `1bfe7f1891e1` | 34566 -> 35100 B |

复审方自身输出的一处不一致，此处如实记录而非抹平：其开头的汇总表把 R5-02 标为 `PASS`，而其正文
裁定为 `REQUEST CHANGES` 并给出阻断编号 R5-02-01，最终处置亦为 `REQUEST CHANGES`。以正文为准。
若采信汇总表那一行，就会把同一份复审在三个段落后亲手打开的缺口重新关上。

复审方明确确认的事项，以及它没有做的事：

- 独立比较修正前后的 Blob，陈述 `#### 5. G protected commit requirements` 与
  `#### 6. Historical visibility` 逐字节未变，新增 G 块未改写这两个既有规范段落。
- 独立核对 `§9.5` 的九个变更前 Blob 与九个变更后 Blob 全部 MATCH，并独立回读 `782c4c8d` 与
  `836dc105` 确认注释数为三后归零。
- 逐行复核 T17/T18，而非采信列名重命名，陈述仅 `Admission` 列名改变、行内容未变。
- 未重新打开任何 `DECIDED FOR CONVERGENCE` 决定。
- 不构成 `FORMAL ACCEPTANCE`，不确立 `IMPLEMENTATION CONFORMANT`，不解除
  `TEST EXECUTION = SUSPENDED`。

本轮之后 R3 复审处置仍为 `REQUEST CHANGES`：两项已应用但尚未复审。`§2` 在本轮五次提交之间逐行
未变。

### 9.7 第四轮独立复审 —— 两项闭合均 PASS

复审方：独立会话 `6b0133e2-3ce0-83ee-aa0c-8a994b9ea682`（只读，未写仓库，未由复审方发布评论）。
2026-11-21 返回裁决。回读钉定：`2fab32dea01310eb50f74aded3fa06e261e8e356`。

五项全部 `PASS`：R5-02-01、SYNC-07-01、未引入新缺陷、新增 `§16.1` 段的双语等价性、
`§9.6` 记录。复审方明确陈述其逐行核对了终态矩阵 `G Context Commit` 列与新增 G 段的对应关系，
确认四种处置一致，而非仅采信指向关系。

它同时裁定了 `§9.6` 以散文方式论证的那一点：旧场景矩阵确实只有六个分量列，因此残留的
`six-component` 一句正确，不构成阻断。

它确认 `3b452dbe` 的 diff 仅改动三个目标文件，九步执行顺序、既有 T17/T18 各行，以及
Schema / DDL / Public API / 线格式的排除条款均未被动。

复审方明示并在此保留的边界：未重新打开任何 `DECIDED FOR CONVERGENCE` 决定；不授予
`FORMAL ACCEPTANCE`；不确立 `IMPLEMENTATION CONFORMANT`；不授权测试执行，
`TEST EXECUTION = SUSPENDED` 维持。

### 9.8 R1 尚无独立复审，而这是唯一剩下的事

`§3` 中仅有一行仍为 `PENDING`：R1 Claim 身份。其余各行或为 `PASS`，或已有应用修正且其阻断项
现已闭合。R1 的应用记录在 `§9.1`，其消费者文本从未被质疑——但「未被质疑」不等于 `PASS`，
而第 5 节要求独立复审者核对已应用的 Blob。因此处置不能凭其余七行的成绩直接转为 `PASS`。

R1 的目标文件，在上述钉定处回读：

```
docs/en/02-domain-model/domain-model-overview.md  1a1a10b24d68dbc2de20cbe4cd6419a7ca037bed  28507 B
docs/zh-CN/02-domain-model/domain-model-overview.md  8ef976789af64afc5e02e8dbdeb2b5f7e1f3df58  25636 B
02-domain-model/domain-model-overview.md  5b86fe23ab7c670b4ae13331b56572aee35f5d00  26974 B
docs/en/02-domain-model/phase-1-domain-model-freeze.md  1a18c6b8424c939dd90986527a24807c8f74d552  5946 B
docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md  408a606c44fcf271f265508bc9d3029f8fc889cb  5553 B
02-domain-model/phase-1-domain-model-freeze.md  d1102a0adf32e3f7b3eb9091758823f990a2a37c  10457 B
docs/en/03-memory-brain/memory-versioning.md  4efbd26db9586f6fcf1897f42ffba287d625b903  49348 B
docs/zh-CN/03-memory-brain/memory-versioning.md  5ff17ab6cb561407806fe63e1b5aa18f399cbed1  45301 B
docs/en/04-memory-compiler/extraction-and-normalization.md  e6aad4b7504fa61fd0feb8b1da7aa8801103bc60  26256 B
docs/zh-CN/04-memory-compiler/extraction-and-normalization.md  8dd0b5b29ecd37ceac6750c4ad8fa07c1c46cb4c  25185 B
```

注意第三行。`02-domain-model/domain-model-overview.md` 与 `docs/en`、`docs/zh-CN` 并列存在于
仓库根级，且其 Blob 仍为 `5b86fe23ab7c`——即 R1 修正前的值。`docs/en` 副本已推进到
`1a1a10b24d68`。根级副本究竟是合法的第三份权威副本、过期镜像，还是冗余，是 `§9.1` 记录但
未裁定的问题：该节已指出根级 freeze 文件在 `§8` 中根本没有行，根级 `context-versioning.md`
仅以「本轮未应用」条目出现。同样的疑问现在也落在根级 domain-model Overview 上。

此处作为开放问题陈述，不作为发现。裁定哪些副本具有权威性需要 Owner 决定，不属于应用轮次
可自行决定的范围。

### 9.9 谓词等价修正轮的合并后回读

本节记录 REREVIEW-8 所审查的第七轮谓词等价修正完成合并后的回读结果。

本节仅记录仓库状态及内容身份。REREVIEW-8 = PASS 不构成 FORMAL ACCEPTANCE，也不建立实现符合性。

#### 9.9.1 精确修正提交 HEAD

| 目标 | 已复审的修正 HEAD | 修正内容 |
|---|---|---|
| PR #410 — Extraction EN | `a685aa9d868b56afb0a335a691d1e758d1fff05a` | `TRUE if and only if` |
| PR #411 — Storage ADR EN | `79a4d7df475c03ccb318712ccef6e6d78fedebba` | `TRUE if and only if` |

两个修正提交均只替换原有英文定义中的谓词连接词。中文定义此前已经使用「当且仅当」。

#### 9.9.2 精确合并目标

| 目标分支 | 合并提交 |
|---|---|
| `main` — PR #410 | `f1a6028d8192` |
| Storage 独立载体分支 — PR #411 | `356e2f051def` |

这两个目标属于不同 Git 历史，不得将其表述为一个共同的原子 Git 快照。

Extraction 文件从指定的 `main` 合并结果读取。Storage ADR 从其独立载体分支的合并结果读取。

#### 9.9.3 合并后 Blob 回读

下表 Blob 值钉定于 R7 合并结果（`main` `f1a6028d`）。它们是历史回读值，
不描述当前 `main` HEAD——该分支此后已被后续治理轮次推进。

| 规范载体 | 路径 | Blob SHA | 大小 |
|---|---|---|---:|
| Extraction EN | `docs/en/04-memory-compiler/extraction-and-normalization.md` | `c87860706313` | 22,484 bytes |
| Extraction ZH | `docs/zh-CN/04-memory-compiler/extraction-and-normalization.md` | `9657949af482` | 21,781 bytes |
| Storage ADR（EN/ZH） | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `62ae6e878657` | 35,544 bytes |

合并后回读确认的完整 Blob 标识如下：

- Extraction EN：`c87860706313`
- Extraction ZH：`9657949af482`
- Storage ADR：`62ae6e878657`

#### 9.9.4 谓词等价回读

四处规范定义分别为：

1. Extraction EN §19.2。
2. Extraction ZH §19.2。
3. Storage ADR EN §8.8。
4. Storage ADR ZH §8.8。

回读确认以下要素对应一致：

| 谓词要素 | 英文 | 中文 |
|---|---|---|
| 谓词身份 | `DependencyClosurePersisted(P)` | `DependencyClosurePersisted(P)` |
| 逻辑连接词 | `if and only if` | `当且仅当` |
| 依赖集合 | 完整直接及传递依赖集合 | 完整 direct 和 transitive 集合 |
| 完整性 | `COMPLETE` | `COMPLETE` |
| Digest | 与准确依赖集合匹配 | 与准确依赖集合匹配 |
| 确认方式 | Authoritative read-after-commit | 权威 read-after-commit |

英文和中文定义表达相同的必要且充分条件。

Participant barrier 只有在该谓词为 TRUE 时才 MUST 被判定为 resolved 或完成。

#### 9.9.5 复审及治理处置

```text
REREVIEW-8 = PASS

FOUR-WAY PREDICATE CONSISTENCY = PASS
LOGICAL EQUIVALENCE = PASS
SCOPE VIOLATION = NONE
REGRESSION = NONE
RESIDUAL REVIEW BLOCKER = NONE

R1-R5 = PASS / NOT REOPENED

FORMAL ACCEPTANCE = PENDING
IMPLEMENTATION CONFORMANCE = NOT ESTABLISHED

TEST EXECUTION = SUSPENDED
TEST EXECUTION DISPATCH GATE = UNLOCKED-WITH-CONDITIONS
UNLOCKED SCOPE = REQ-04 STEP 5 DISPATCH SPEC ONLY
```

PASS 是独立复审判定，不是正式接受决定。

本次回读不证明底层存储实现已经提供原子性、事务隔离、依赖登记持久化或任何其他实现属性。

本节不批准 Schema、DDL、公共 API、H Wire、生产密钥、Trust Root、Crypto Profile 或 Storage L4。

本节记录的是规范回读完成，不是实现测试完成。
