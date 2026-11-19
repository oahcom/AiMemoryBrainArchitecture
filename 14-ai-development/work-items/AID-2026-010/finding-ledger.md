# AID-2026-010 — Finding Ledger（唯一权威状态台账）

> **本文件是 AID-2026-010 的唯一权威 Finding 状态台账。**
> Issue #43 评论是历史裁决与证据锚点，不单独决定当前状态；与本台账冲突时，须核查最新裁决及精确提交证据后修订本台账。
> 原始审查报告 `../../issue-alignment-2026-11-19/l2-05b-integration-review.md` 是 F-43-01…05 的原始定义来源，不因本文件存在而改变，也不复制其文本充当原始证据。

- 建立依据：A Integration 裁定（A 会话 `6aff38f6-ac34-83e8-b116-53d4e87b22a5`，R29，选项 A）
- 建立时间：2026-11-20
- 状态语义：`OPEN`（未解决或缺证据）/ `BLOCKED`（有明确阻断项）/ `REMEDIATION ACCEPTED`（技术整改被接受，账本关闭条件未全部满足）/ `CLOSED`（关闭条件全部满足，证据已持久化并可回读）
- **`REMEDIATION ACCEPTED` 不得自动等同于 `CLOSED`。**

---

## F-43-01/F1 — D/H ForgetFence 高水位格式与语义映射（双高水位六条件操作级证明）

| 字段 | 内容 |
|---|---|
| ID | F-43-01/F1 |
| 历史 ID / 别名 | F-43-01（子项 F1） |
| 原始锚点 | `14-ai-development/issue-alignment-2026-11-19/l2-05b-integration-review.md` §F-43-01（L171）；Issue #43 裁决评论 `7015532739`（R22）、`7015683598`+`7015684625`（D-001/D-002） |
| 问题定义 | D-002 双高水位语义已 ACCEPT，但六条件替代证明尚未在操作级落地（`verify_owner_snapshot` 真实 D 权威证据、exact equality、linearization、Receipt）。 |
| 状态 | BLOCKED |
| 责任 Owner | D Owner |
| 回流去向 | D Owner 双高水位六条件操作级证明 → A 集成复审 |
| 关闭条件 | 六条件逐条操作级证据（真实 D 权威回调、非 `lambda: True` 占位），含 exact equality 与 linearization 证明、Receipt 样例，经 A 独立复核接受 |
| 最新裁决 / 证据 | `D-OWNER-2026-11-19-002`（ACCEPT，六条件定义）；`D-OWNER-2026-11-19-003`（D-002 规范证明包 ACCEPT，Blob `4c8672a68e4339e40b5d8cb98eb073af8c98c1a5`）；A R32 裁定规范论证达设计交付要求但**操作级实现验收未达到**；D Owner Runtime 核验确认五操作 NOT IMPLEMENTED、真实 Receipt 不存在、十场景 NOT RUN；A R33 裁定不授权 A1 空仓初始化、不授权 B2 Adapter 承载、不新建 Runtime repo，F1 实现级工作 **BLOCKED（等待产品/平台架构责任方指定工程载体及 Canonical Authority/权威持久化边界）**；D Owner `D-OWNER-2026-11-19-006` 明确 F1 仍 OPEN for implementation evidence，未改变 A 的 BLOCKED 管理状态 |
| 范围限制 | 语义 ACCEPT ≠ 操作级证明完成；文档六条件论证 ≠ 真实 D 权威状态满足六条件；参考模型 ≠ 生产权威 |

## F-43-01/F2 — H 组合验证器 D Snapshot 八字段与长度约束对齐

| 字段 | 内容 |
|---|---|
| ID | F-43-01/F2 |
| 历史 ID / 别名 | F-43-01（子项 F2） |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-01（L171）；Issue #43 评论 `7016478902`（R23-H）、`7016850797`（R24-H）、`7017186199`（R25-H） |
| 问题定义 | 组合验证器 D allowlist 5 字段 vs Schema 1.2.17 八字段不一致，且长度约束（1–512）在 legacy opt-in 路径可绕过。 |
| 状态 | CLOSED |
| 责任 Owner | H Owner |
| 回流去向 | A 集成复审（R26 已裁定） |
| 关闭条件 | 八字段对齐 + 六字段长度约束在 legacy/normal 双路径生效 + 独立重跑测试 |
| 最新裁决 / 证据 | R26 裁定 CLOSED（A-OWNER-ALIGNMENT-001-R26）；Commit `19a839332c390440163c2d9c68e50dd652d4d6c4`，源 Blob `7dd48ecb31ced6c2d6041cce33b9686056705742`，测试 Blob `f4126e2034d71bc90bae5fefab89c826c3f1ccfa`；L0 本地独立重跑 22/22 PASS |
| 范围限制 | 仅限 TEST-profile 组合验证器 D Snapshot 范围；不代表 1.2.17 整体对齐或生产验证 |

## F-43-01/F3 — H 独立接受 D/H 映射

| 字段 | 内容 |
|---|---|
| ID | F-43-01/F3 |
| 历史 ID / 别名 | F-43-01（子项 F3） |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-01（L171）；Issue #43 评论 `7015532739` 等 |
| 问题定义 | H 尚未独立接受 D/H 双向映射（D/H authoritative query interface 未闭合）。 |
| 状态 | CLOSED |
| 责任 Owner | D Owner / H Owner |
| 回流去向 | D/H 联合映射接受 → A 集成复审 |
| 关闭条件 | D/H 双方对同一映射 Blob 的独立接受证据 + authoritative query interface 定义与核验 |
| 最新裁决 / 证据 | A R32 授权 H 对 D 1.3.1 Blob `12b71e770f4e977c7f147694a644066bc2ce11b9` 独立映射审查；H `H-OWNER-2026-11-19-001` 对精确 H mapping Blob `e60bdd4cbfef79850596001f01cb56e622b7d79d` 作 `ACCEPT WITH EXPLICIT LIMITATIONS`（H HEAD `940963af09fe25ffb862b69ac5f272050cf000f2`，#43 `7021523060`，补充 `7021543287`）；D `D-OWNER-2026-11-19-006` 对同一精确 H mapping Blob 独立作 `ACCEPT WITH EXPLICIT LIMITATIONS`（#43 `7021721864`）；A R35 接受双 Owner 对同一精确映射 Blob 的规范层决定。D `D-OWNER-2026-11-19-007` 对 `D-AUTH-QUERY-1.0` 作 `ACCEPT`（Commit `4c5183abdc74583a3a6b8f9722d7ff2ef54ca89a` / Blob `da69b84090f45c7b6d786766eac6ec2dec9c6dee`；#43 `7021914182`）。A 独立按精确 commit 回读契约，Blob SHA 匹配；逐项核验八字段 nominal type/authority/namespace/Receipt binding、五类独立 decimal/range、D 14 元组与 H Snapshot/attestation 绑定、请求关联与响应认证、C1–C6 evidence payload/coverage/digest/Receipt 绑定、currentness/revocation、Ed25519/RFC 8785/key lifecycle、`D-Ledger-Consistency-Proof-v1`，覆盖 R35 所列 authoritative query interface 规范缺口。**A 裁定 F3 CLOSED（仅规范定义与核验范围）**：关闭条件“D/H 对同一映射 Blob 独立接受 + authoritative query interface 定义与核验”已满足。明确排除：endpoint/transport、真实 Receipt、生产密钥/签名、实际 ledger proof、C6 真实序列化与事件覆盖 trace、Runtime 测试及 CI 均未验证/未运行；不构成 operational conformance 或生产授权。上述实现级证据继续由 F1 的 BLOCKED/操作级验收及相关生产 Gate 跟踪，不得因 F3 CLOSED 而推定满足。 |
| 范围限制 | H 的 F3 独立接受不替代 F1 实现验收；D 1.3.1 ACCEPT ≠ H 接受 |

## F-43-02 — D 契约 1.3.0 权威采纳

| 字段 | 内容 |
|---|---|
| ID | F-43-02 |
| 历史 ID / 别名 | — |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-02（L203）；Issue #43 评论 `7015681927`+`7015682819`（D-001/D-002） |
| 问题定义 | D 1.3.0 契约在 main 与 D Owner 分支不一致；Unicode 数据版本未固定，§5 双高水位证明规则不符。 |
| 状态 | REMEDIATION ACCEPTED |
| 责任 Owner | D Owner |
| 回流去向 | D successor 契约正式落文 + Unicode 版本固定 → D 1.3.0 采纳裁决；实现绑定（UCD 工件 lock manifest / validator 版本校验）作为独立实现验收工作跟踪 |
| 关闭条件 | D successor 契约落文、Unicode 数据版本固定、D Owner 采纳决定（DECIDED → ACCEPTED）——规范层三条件已满足；剩余：main 基线同步 + Unicode 实现绑定验证 |
| 最新裁决 / 证据 | `D-OWNER-2026-11-19-001`：采纳 = **BLOCKED**，H 消费 = **NOT AUTHORIZED**；`D-OWNER-2026-11-19-003`：1.3.1 successor ACCEPT；A R32 裁定两个规范阻塞点（§5 双语规则 + Unicode 15.1.0 版本固定）解除，`BLOCKED → REMEDIATION ACCEPTED`，不直接 CLOSED（main 未同步 + UCD 工件/validator 绑定未实现未验证）。证据：Commit `7c74c23`→`b03e31c7`，1.3.1 Blob `12b71e770f4e977c7f147694a644066bc2ce11b9`，D-002 证明包 Blob `4c8672a68e4339e40b5d8cb98eb073af8c98c1a5`，#43 `7020911000` |
| 范围限制 | 不得把 H 修复进展解释为 D 1.3.0 采纳；不得把规范版本固定解释为实现符合；后续不得把原始两个规范阻塞点重复派给 D Owner |

## F-43-03 — H 独立可复核测试证据

| 字段 | 内容 |
|---|---|
| ID | F-43-03 |
| 历史 ID / 别名 | — |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-03（L215） |
| 问题定义 | H 测试证据不是当前 H HEAD 的精确验证；缺独立可复核完整测试日志（含 CI）。 |
| 状态 | OPEN |
| 责任 Owner | H Owner |
| 回流去向 | H HEAD 精确测试证据（本地 + CI）→ A 独立复核 |
| 关闭条件 | 对最终 HEAD 的完整测试日志（命令、环境、PASS/FAIL/SKIP 明细），且 CI 有测试级输出（runner 空 steps 不算） |
| 最新裁决 / 证据 | R28：CI 仍 NOT VERIFIED（Run `44599661184` / Job `135827292056` steps=[]）；H Owner 诊断评论 `7022079646`：Run `44612473889` / Job `135878277940`，HEAD `345bb3be537d018be80040cd2f00425bb80aac2c`，`runner_id=0`、`steps=[]`；同 workflow 及跨 workflow 对照亦报告相同 runner allocation signature，表明该次失败发生在 runner 分配阶段而非测试步骤。L0 对旧 HEAD 的本地报告为 `423 PASS / 2 FAIL / 1 ERROR / 22 SKIP`，但原始完整日志未附且 `Ran 426` 与分类合计 448 不一致，故不采纳为独立验证计数。A 检视旧 HEAD 测试源码 Blob `b25a9478796138f2d388971d20412407d787e5c7`，确认 512 字符有效值测试错误覆盖两个仅允许 `0..2^63-1` 的 typed high-water 字段，构成测试设计缺陷。H 随后在既有分支 `session-h-bmcp-protocol` 提交 `1d5296e0effa7c6466c9e7aef9f071827ff8aa1c`（`Fix 1.2.17 bounded-field regression test partition`）；A 精确回读该 commit，确认该分支 ref 与 commit `identical`（ahead/behind 0），唯一变更文件为 `08-bmcp-protocol/tests/conformance/recovery_cutoff/test_owner_snapshot_semantics_1_2_17.py`，测试 Blob `40694238e01139c764f03a9ba3cbfabfeb28d318`；validator `08-bmcp-protocol/runtime_reference/owner_snapshot_semantics_1_2_17.py` Blob `f572ef31c270f9fee8bb7dd84ad7d1b548650aa9` 未变。新测试将 512/513 字符边界限制在四个非 typed 字段，并为两个 typed 字段测试 `0`、`9223372036854775807` VALID 及 `9223372036854775808` INVALID；A 接受该测试设计缺陷整改。L0 报告在 Windows/Python 3.12.3/jsonschema 4.26.0 下完整套件 `Ran 426`，分类为 `403 PASS / 0 FAIL / 1 ERROR / 22 SKIP`，ERROR 为缺少 `rfc8785`；并报告聚焦模块 `Ran 13` / `OK`。这些计数和输出目前仅为提交的 L0 报告，未附完整原始 stdout/stderr，A 未在本地复跑，故不作为独立可复核完整测试证据。A 查询该 commit 的 PR-triggered workflow runs 返回空列表；尚无该 HEAD 的 CI 测试级输出，且此前 runner allocation failure（`runner_id=0`、`steps=[]`）未被证明恢复。**裁定：测试设计缺陷整改 ACCEPTED；F-43-03 整体仍 OPEN。** 关闭仍要求最终 HEAD 的完整原始测试日志（命令、环境、依赖版本、PASS/FAIL/ERROR/SKIP 明细及 skip reasons，计数与 `Ran N` 一致）以及 CI 对同一 HEAD 的实际测试级输出；空 runner/空 steps、workflow 未触发或仅本地 `0 FAIL` 均不满足 CI 条件。

R39：H/L0 本轮补报完整套件结果：Windows/Git Bash、Python 3.12.3、pip 24.0、jsonschema 4.26.0、Node 22.22.2、npm 10.9.7；报告已安装 `rfc8785==0.1.4` 与 `canonicalize@2.1.0`。命令为 `python -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p "test_*.py" -v`；报告 `Ran 432 tests in 0.707s; OK (skipped=22)`，逐行分类 `410 PASS / 0 FAIL / 0 ERROR / 22 SKIP`，exit code 0；skip 均为 `test_unified_manifest_1_2_10.UnionSemanticsTests` 的 1.2.10 legacy semantics superseded 说明；聚焦模块报告 `Ran 13` / `OK`。H 声明原始日志位于其本机路径 `state/h-f43-03-complete-test-log.txt`、72,653 bytes。**证据分类：OWNER-REPORTED / NOT INDEPENDENTLY READ**；该本机路径文件未作为当前对话附件、可访问 Library 文件或仓库 artifact 提供，A 无法读取原始 stdout/stderr，也无法独立核验逐行计数、安装输出或 skip 明细。精确 HEAD 仍为 `1d5296e0effa7c6466c9e7aef9f071827ff8aa1c`；A 对该 HEAD 的 workflow-run 查询返回空列表。此前 CI runner allocation failure（`runner_id=0`、`steps=[]`）仍无恢复证据。**裁定：测试设计缺陷整改 ACCEPTED；本地完整套件结果作为 H/L0 报告登记，但测试证据层尚未达到 A 独立验收；F-43-03 整体维持 OPEN。** 当前 ledger 关闭条件要求最终 HEAD 的可复核完整测试日志及 CI 测试级输出；不得在未取得授权的情况下将外部 CI 阻塞自动豁免。
| 范围限制 | 本地 PASS 不等于 CI PASS |

## F-43-04 — #25 Phase 3.8.1 Addendum Blob 漂移

| 字段 | 内容 |
|---|---|
| ID | F-43-04 |
| 历史 ID / 别名 | — |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-04（L229）；#25 Pin 更新证据 |
| 问题定义 | #25 中 A Phase 3.8.1 Addendum Blob 已漂移。 |
| 状态 | CLOSED |
| 责任 Owner | A Integration |
| 回流去向 | #25 Pin 更新（R20 已完成） |
| 关闭条件 | #25 Pin 更新为精确 Blob 并回读一致 |
| 最新裁决 / 证据 | R20 裁定 CLOSED |
| 范围限制 | — |

## F-43-05 — AID-2026-010 登记状态不一致

| 字段 | 内容 |
|---|---|
| ID | F-43-05 |
| 历史 ID / 别名 | — |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-05（L239） |
| 问题定义 | AID-2026-010 登记状态不一致。 |
| 状态 | CLOSED |
| 责任 Owner | 按原始报告记录的 Owner（具体责任人不得推测） |
| 回流去向 | R18 裁决 |
| 关闭条件 | 登记状态与 R18 基线一致 |
| 最新裁决 / 证据 | R18 裁定 CLOSED |
| 范围限制 | — |

## F-43-06A — Storage/COC JoinProof 双持久化与恢复协议

| 字段 | 内容 |
|---|---|
| ID | F-43-06A |
| 历史 ID / 别名 | `F-43-06`（历史别名，不得继续作主键） |
| 原始锚点 | Issue #43 comment `7013501942`；交叉引用 #25 comment `7013493546` |
| 问题定义 | Storage-persisted + COC-committed JoinProof 缺少规范性双持久化写序、canonical-copy 规则与崩溃恢复协议。 |
| 状态 | OPEN / BLOCKED |
| 责任 Owner | Storage Owner |
| 回流去向 | Storage Owner 裁决 → #25 owner-decision 载体 + 本台账 |
| 关闭条件 | Storage durable write + signed receipt → COC quorum append binding exact ref/digest → 双向回读 → 才 owner release；重试用同一 immutable identity |
| 最新裁决 / 证据 | #43 `7013501942`（F-43-06 P1 OPEN/BLOCKED 原始登记） |
| 范围限制 | 架构可行性 finding，非实现验证 |

## F-43-06B — BIH Registry §9 currentness / status-scope reconciliation

| 字段 | 内容 |
|---|---|
| ID | F-43-06B |
| 历史 ID / 别名 | `F-43-06`（历史别名，不得继续作主键） |
| 原始锚点 | Issue #43 comment `7016815868` |
| 问题定义 | BIH identity baseline currentness / status-scope 未完成对账。 |
| 状态 | OPEN |
| 责任 Owner | BIH Registry Owner |
| 回流去向 | BIH Registry Owner 裁决 → A 集成复审 |
| 关闭条件 | §9 currentness 与 status-scope reconciliation 的权威证据（按该评论定义的关闭条件） |
| 最新裁决 / 证据 | #43 `7016815868`（F-43-06 P2 OPEN 原始登记） |
| 范围限制 | — |

## F-43-07 — ParticipantRef 映射（PublicationParticipantRef / StorageVisibilityParticipantRef ↔ COC ParticipantIntentRef）

| 字段 | 内容 |
|---|---|
| ID | F-43-07 |
| 历史 ID / 别名 | — |
| 原始锚点 | Issue #43 comment `7013501942`（与 F-43-06A 同评论登记，子项 F-43-07）；交叉引用 #25 comment `7013493546` |
| 问题定义 | D PublicationParticipantRef / StorageVisibilityParticipantRef 未显式映射到（也未规范性排除于）COC ParticipantIntentRef。 |
| 状态 | OPEN / BLOCKED |
| 责任 Owner | D Owner / Storage Owner / H Owner |
| 回流去向 | D/Storage/H 选定记账边界并定义 exact identity binding + ordering + recovery（或定义独立权威恢复枚举）→ A 集成复审 |
| 关闭条件 | 映射或规范性排除的契约文本 + identity binding/ordering/recovery 定义 + 三方独立接受 |
| 最新裁决 / 证据 | #43 `7013501942`（F-43-07 P1 OPEN/BLOCKED 原始登记）；R28 裁定保留原 ID 与含义 |
| 范围限制 | 架构可行性 finding，非实现验证；编号治理不改变其技术含义 |

## F-43-08 — Finding ID 冲突纠正

| 字段 | 内容 |
|---|---|
| ID | F-43-08 |
| 历史 ID / 别名 | — |
| 原始锚点 | Issue #43 comment `7018553089` |
| 问题定义 | `F-43-06` 被两个不同 finding 复用（`7013501942` Storage/COC JoinProof、`7016815868` BIH Registry §9），后续又曾被 D 长度修复借用为 task label，稳定 ID 不唯一。 |
| 状态 | CLOSED |
| 责任 Owner | A Integration |
| 回流去向 | 本台账（编号映射持久化）→ Issue #43 映射评论 → A 精确回读 |
| 关闭条件 | 已满足：本台账按 Blob SHA 精确回读；06A/06B 拆分且保留原始锚点；#43 映射评论 `7020472247` 的 comment ID 与正文核对一致；F-43-07 保留原义、I/C 漂移独立编号为 F-43-10；未发现 ID 冲突残留 |
| 最新裁决 / 证据 | R29 编号映射 + R30 独立精确回读裁决 CLOSED；Commit `6bee14688dcb11b5117699ecdb32abc3698efd9a` / Blob `475fe6d665d12a2c4911cc7677707c68f9ed0b61`；#43 comment `7020472247`；映射与锚点核验通过 |
| 范围限制 | 纯可追溯性纠正，不改变任何技术 finding 或 Owner 决定 |

## F-43-09 — H 1.2.17 独立 Owner Snapshot D 六字段长度约束

| 字段 | 内容 |
|---|---|
| ID | F-43-09 |
| 历史 ID / 别名 | `F-43-06`（R27 task label，仅历史别名） |
| 原始锚点 | Issue #43 comment `7019182732`、#25 comment `7019181900`（H 交付回填）；R27 裁定 |
| 问题定义 | `owner_snapshot_semantics_1_2_17.py` 未执行 Schema 1.2.17 的 `minLength:1 / maxLength:512`，513 字符 D 字段被 Schema 拒却通过验证器。 |
| 状态 | CLOSED |
| 责任 Owner | H Owner |
| 回流去向 | H 独立 D Snapshot 六字段长度约束证据 → A 独立复审（R27 已通过）→ 本台账登记关闭 |
| 关闭条件 | 已满足：六字段 0/1/512/513 全矩阵 + callback 前置 + 独立重跑测试证据持久化回读；R30 裁定 CLOSED |
| 最新裁决 / 证据 | R27 技术整改 ACCEPT + R30 账本关闭裁决；Commit `8ff8c83f0bac59cc834e40e73f8b8f520d8fafb5` + `dd3cacde4af541205d2dc1e50f8a196666ea3a7b`；源 Blob `d9dc43ff0136751aba20cffa4db3f280d16edc67`，测试 Blob `d535ddcc24f57ab38aceb350853a424490f870cc`；L0 本地 9/9 PASS + 全矩阵复现 |
| 范围限制 | TEST-profile；本地测试 ≠ CI PASS；不构成生产授权 |

## F-43-10 — 组合验证器版本字段集隔离（1.2.9 vs 1.2.17）

| 字段 | 内容 |
|---|---|
| ID | F-43-10 |
| 历史 ID / 别名 | 曾暂记 F-43-07（R26 PROPOSED 期），现独立编号 |
| 原始锚点 | Issue #43 comment `7019972155`、#25 comment `7019971478`（H 范围声明回填）；R28 裁定 |
| 问题定义 | 组合验证器默认按 1.2.9 I5/C3 字段集运行，与 Schema 1.2.17 I6/D8/C5 不一致；旧混合测试路径不能证明完整 1.2.17 组合兼容。 |
| 状态 | CLOSED |
| 责任 Owner | H Owner |
| 回流去向 | H 版本隔离修复证据 → A 独立复审（R28 已接受）→ 本台账登记关闭 |
| 关闭条件 | 已满足：显式 `schema_artifact_revision` 版本选择 + I/C 新旧字段集回归测试 + 范围声明持久化回读；R30 裁定 CLOSED |
| 最新裁决 / 证据 | R28 技术整改 ACCEPT + R30 账本关闭裁决；Commit `a04d4010152577cab2f27b4c1359e955ea91e447`→`de5d7b63ff8555a9bbd58f9dd64d4c28fbc7e5cc`；源 Blob `6eee88221c7488542240cdaf326ffdeb0cc2419a`，测试 Blob `ea38ae2aa97a75c62ed857bfd16e3b8d27ba72f1`，范围声明 Blob `66a6dfa627ff6a6c382aca84258de347b0048ab5`；L0 本地 7/7 PASS + 版本矩阵复现；CI NOT VERIFIED |
| 范围限制 | TEST-profile 版本字段集隔离；不代表生产入口验证完成；本地测试 ≠ CI PASS |

---

## 编号映射（历史 → 当前）

| 历史称呼 | 当前 ID | 说明 |
|---|---|---|
| F-43-06（Storage/COC JoinProof） | **F-43-06A** | 保留锚点 `7013501942` |
| F-43-06（BIH Registry §9） | **F-43-06B** | 保留锚点 `7016815868` |
| F-43-06（R27 task label，D 长度约束） | **F-43-09** | 仅历史别名，不再作主键 |
| F-43-07 | **F-43-07** | 含义不变（ParticipantRef 映射） |
| F-43-07（R26 PROPOSED 期 I/C 字段集） | **F-43-10** | 与历史 F-43-07 无关，独立编号 |
| F-43-08 | **F-43-08** | 编号冲突纠正，待回读关闭 |

## 待补项（TBD）

- 无。F-43-07 原始锚点已核实为 #43 comment `7013501942`（与 F-43-06A 同评论登记），非虚构。
