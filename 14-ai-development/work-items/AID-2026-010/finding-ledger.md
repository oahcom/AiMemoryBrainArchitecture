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
| 状态 | CLOSED（限定于 UCD 15.1.0 工件锁定、版本绑定及完整一致性语料验证；不代表生产验收或运行时操作证明） |
| 责任 Owner | D Owner |
| 回流去向 | D successor 契约正式落文 + Unicode 版本固定 → D 1.3.0 采纳裁决；实现绑定（UCD 工件 lock manifest / validator 版本校验）作为独立实现验收工作跟踪 |
| 关闭条件 | D successor 契约落文、Unicode 数据版本固定、D Owner 采纳决定（DECIDED → ACCEPTED）——规范层三条件已满足；剩余：main 基线同步 + Unicode 实现绑定验证 |
| 最新裁决 / 证据 | `D-OWNER-2026-11-19-001`：采纳 = **BLOCKED**，H 消费 = **NOT AUTHORIZED**；`D-OWNER-2026-11-19-003`：1.3.1 successor ACCEPT；A R32 裁定 §5 双语规则与 Unicode 15.1.0 版本固定两个规范阻塞点解除，`BLOCKED → REMEDIATION ACCEPTED`，当时不直接 CLOSED（main 未同步 + UCD 工件/validator 绑定未实现未验证）。`AID-2026-026`：**NOT YET CLOSED**，唯一残余为 `normalizer.cargo_lock_sha256` 与实际 `Cargo.lock` 及锁定 normalizer 版本的绑定证明。`AID-2026-027`：**F-43-02 CLOSED**（限于本 finding 的 UCD 工件锁定、版本绑定及完整一致性语料验证范围；不构成生产验收）。证据：Commit `bb1420b34b1c26e4936fb3b86956e6cf658c2719`；实际 `Cargo.lock` SHA-256 `a697d9051dc486f9707b1f1dd20f135ca922628805dcecf46a9e41078f751f24`，锁定且解析依赖版本 `unicode-normalization 0.1.24` 一致；正向 `cargo test -j 2`：**28 passed / 4 ignored**；完整语料 `records_consumed=19074 / nfc_assertions=95370 / nfd_assertions=95370`；负向伪造 `cargo_lock_sha256` 并重算 payload digests 后，构建以 **exit 101** 失败，报告期望与实际 digest 不匹配。此前对 `Cargo.lock` 追加注释的负向测试因 Cargo 会规范化 lock 文件而未能证明校验行为，明确排除，不作为证据。 |
| 范围限制 | 不得把 H 修复进展解释为 D 1.3.0 采纳；不得把规范版本固定解释为实现符合；后续不得把原始两个规范阻塞点重复派给 D Owner |


R41（A-OWNER-INTEGRATION-R41-2026-11-19）：F-43-02 继续保持 REMEDIATION ACCEPTED，不转 CLOSED。A 核验 D successor `owner-snapshot-namespace-and-fence-currentness-contract-1.3.1.md` Blob `12b71e770f4e977c7f147694a644066bc2ce11b9`，其 §4 明确固定 Unicode 15.1.0、UCD 工件和 SHA-256 lock manifest、validator/build 的实际数据源版本核验及 fail-closed、完整 NormalizationTest.txt 与 D-specific vectors。派 D Owner 在既有授权 D 分支完成 UCD 工件 lock manifest、每项 SHA-256、validator/build version binding 与实际来源校验、fail-closed 行为及完整语料/向量测试，提交精确 commit/Blob/原始日志。main 同步：不得直接向 main 写入；当前冻结 ACTIVE，且沿用既有 PR-only / no-main-direct-write 边界。只允许利用已存在且覆盖该精确 successor 的 PR 完成审查/合并；未找到可确认覆盖该 Blob 的既有 open PR，禁止新建 PR。待冻结解除后再按正常 PR 流程同步 main。规范层已满足，main sync 与 Unicode implementation binding 均未完成，不得 CLOSED。

R42（A-OWNER-INTEGRATION-R42-2026-11-19）：F-43-02 裁定为 BLOCKED（实现目标未授权）。A 检查了可见仓库：`oahcom/AiMemoryBrain` 当前仍为空仓且无分支；`oahcom/ai-memory-adapter` 的 README 所示能力仅为通用 MemoryAdapter（store/query/inject_context/prune，SQLite+Qdrant），不是 D Unicode validator/build，也不含 D 五项权威操作；`AiMemoryBrainArchitecture` 是规范/测试参考仓，未找到可核验的获授权 D Unicode validator/build 载体。不得把上述任一仓库推定为目标。配额冻结 ACTIVE，禁止新建 repo/branch/PR/Issue；不得创建或初始化 Runtime/validator 载体。D Owner 当前仅可在既有 D 授权分支维护规范、测试设计/证据材料，不得在未获授权的仓库或分支写入 validator/build 实现。解阻条件：Product/Platform Architecture responsibility holder 指定现有工程仓库、分支、validator/build 路径、Canonical Authority Owner、数据源/构建边界，并明确 D Owner 写权限；之后 A 再核验目标及授权。Unicode 15.1.0 lock manifest、实际数据源版本绑定、fail-closed 和完整语料测试均未实施/未验证。

> **L0 时序说明（2026-11-20 测量，不构成裁定）**
>
> 本节只登记上述裁决与后续裁决的先后顺序，供阅读时定位，不判断何者生效；效力归属由 A 裁定。
>
> | 序 | 裁决 / 记录 | 时间（UTC） | 对 F-43-02 的表述 |
> |---:|---|---|---|
> | 1 | R41（commit `0ee679b`） | 2026-11-19T21:29Z | 保持 REMEDIATION ACCEPTED，不转 CLOSED |
> | 2 | R42（commit `29076ed`） | 2026-11-19T21:49Z | BLOCKED（实现目标未授权） |
> | 3 | AID-2026-026（#43 `7031825212`） | 2026-11-20T06:00Z | NOT YET CLOSED，残余为 lock 绑定证明 |
> | 4 | AID-2026-027（#43 `7032631742`） | 2026-11-20T06:49Z | CLOSED（限定范围） |
> | 5 | 本表状态行同步（commit `9263d0d`） | 2026-11-20T06:55Z | 状态行与证据行改为 CLOSED |
>
> 事实：R41、R42 早于 AID-2026-026 与 AID-2026-027 约 9 小时；本表「状态」行目前反映的是第 4、5 序记录。R41/R42 段落正文未标注已被后续记录取代，故本表内并存三种表述。
>
> 另：R42 的核心事实依据「`oahcom/AiMemoryBrain` 当前仍为空仓且无分支」在 2026-11-20T10:00Z 实测已不成立（该仓 `main` 已有 8 个提交、完整 validator 实现与 UCD 15.1.0 锁清单）。测量记录见 `f43-02-blocked-premise-falsified-l0-measurement.md`。L0 只陈述该事实，不据此改变本表任何状态。
## F-43-03 — H 独立可复核测试证据

| 字段 | 内容 |
|---|---|
| ID | F-43-03 |
| 历史 ID / 别名 | — |
| 原始锚点 | `l2-05b-integration-review.md` §F-43-03（L215） |
| 问题定义 | H 测试证据不是当前 H HEAD 的精确验证；缺独立可复核完整测试日志（含 CI）。 |
| 状态 | CLOSED |
| 责任 Owner | H Owner |
| 回流去向 | H HEAD 精确测试证据（本地 + CI）→ A 独立复核 |
| 关闭条件 | 最终测试源码 HEAD 的完整可复核测试日志（命令、环境、依赖、PASS/FAIL/ERROR/SKIP 明细与原因，计数一致）并经 A 独立回读；若 CI 因已确认的外部 runner 分配故障无测试步骤，A Integration Owner 可作开发基线范围内的明确 CI 豁免。CI 豁免不构成 CI PASS、生产授权或运行时 conformance。 |
| 最新裁决 / 证据 | R28：CI 仍 NOT VERIFIED（Run `44599661184` / Job `135827292056` steps=[]）；H Owner 诊断评论 `7022079646`：Run `44612473889` / Job `135878277940`，HEAD `345bb3be537d018be80040cd2f00425bb80aac2c`，`runner_id=0`、`steps=[]`；同 workflow 及跨 workflow 对照亦报告相同 runner allocation signature，表明该次失败发生在 runner 分配阶段而非测试步骤。L0 对旧 HEAD 的本地报告为 `423 PASS / 2 FAIL / 1 ERROR / 22 SKIP`，但原始完整日志未附且 `Ran 426` 与分类合计 448 不一致，故不采纳为独立验证计数。A 检视旧 HEAD 测试源码 Blob `b25a9478796138f2d388971d20412407d787e5c7`，确认 512 字符有效值测试错误覆盖两个仅允许 `0..2^63-1` 的 typed high-water 字段，构成测试设计缺陷。H 随后在既有分支 `session-h-bmcp-protocol` 提交 `1d5296e0effa7c6466c9e7aef9f071827ff8aa1c`（`Fix 1.2.17 bounded-field regression test partition`）；A 精确回读该 commit，确认该分支 ref 与 commit `identical`（ahead/behind 0），唯一变更文件为 `08-bmcp-protocol/tests/conformance/recovery_cutoff/test_owner_snapshot_semantics_1_2_17.py`，测试 Blob `40694238e01139c764f03a9ba3cbfabfeb28d318`；validator `08-bmcp-protocol/runtime_reference/owner_snapshot_semantics_1_2_17.py` Blob `f572ef31c270f9fee8bb7dd84ad7d1b548650aa9` 未变。新测试将 512/513 字符边界限制在四个非 typed 字段，并为两个 typed 字段测试 `0`、`9223372036854775807` VALID 及 `9223372036854775808` INVALID；A 接受该测试设计缺陷整改。L0 报告在 Windows/Python 3.12.3/jsonschema 4.26.0 下完整套件 `Ran 426`，分类为 `403 PASS / 0 FAIL / 1 ERROR / 22 SKIP`，ERROR 为缺少 `rfc8785`；并报告聚焦模块 `Ran 13` / `OK`。这些计数和输出目前仅为提交的 L0 报告，未附完整原始 stdout/stderr，A 未在本地复跑，故不作为独立可复核完整测试证据。A 查询该 commit 的 PR-triggered workflow runs 返回空列表；尚无该 HEAD 的 CI 测试级输出，且此前 runner allocation failure（`runner_id=0`、`steps=[]`）未被证明恢复。**裁定：测试设计缺陷整改 ACCEPTED；F-43-03 整体仍 OPEN。** 关闭仍要求最终 HEAD 的完整原始测试日志（命令、环境、依赖版本、PASS/FAIL/ERROR/SKIP 明细及 skip reasons，计数与 `Ran N` 一致）以及 CI 对同一 HEAD 的实际测试级输出；空 runner/空 steps、workflow 未触发或仅本地 `0 FAIL` 均不满足 CI 条件。

R39：H/L0 本轮补报完整套件结果：Windows/Git Bash、Python 3.12.3、pip 24.0、jsonschema 4.26.0、Node 22.22.2、npm 10.9.7；报告已安装 `rfc8785==0.1.4` 与 `canonicalize@2.1.0`。命令为 `python -m unittest discover -s 08-bmcp-protocol/tests/conformance/recovery_cutoff -p "test_*.py" -v`；报告 `Ran 432 tests in 0.707s; OK (skipped=22)`，逐行分类 `410 PASS / 0 FAIL / 0 ERROR / 22 SKIP`，exit code 0；skip 均为 `test_unified_manifest_1_2_10.UnionSemanticsTests` 的 1.2.10 legacy semantics superseded 说明；聚焦模块报告 `Ran 13` / `OK`。H 声明原始日志位于其本机路径 `state/h-f43-03-complete-test-log.txt`、72,653 bytes。**证据分类：OWNER-REPORTED / NOT INDEPENDENTLY READ**；该本机路径文件未作为当前对话附件、可访问 Library 文件或仓库 artifact 提供，A 无法读取原始 stdout/stderr，也无法独立核验逐行计数、安装输出或 skip 明细。精确 HEAD 仍为 `1d5296e0effa7c6466c9e7aef9f071827ff8aa1c`；A 对该 HEAD 的 workflow-run 查询返回空列表。此前 CI runner allocation failure（`runner_id=0`、`steps=[]`）仍无恢复证据。**裁定：测试设计缺陷整改 ACCEPTED；本地完整套件结果作为 H/L0 报告登记，但测试证据层尚未达到 A 独立验收；F-43-03 整体维持 OPEN。** 当前 ledger 关闭条件要求最终 HEAD 的可复核完整测试日志及 CI 测试级输出；不得在未取得授权的情况下将外部 CI 阻塞自动豁免。
| 范围限制 | 本地 PASS 不等于 CI PASS |


R40（A-OWNER-INTEGRATION-R40-2026-11-19）：A 按精确 commit `d4fb6f199a9546ab48bbba2c6b926c92f27e7fc3` 独立回读 H 既有分支 `session-h-bmcp-protocol`；分支 ref 与该 commit `identical`。原始日志 `08-bmcp-protocol/tests/conformance/recovery_cutoff/test-logs/2026-11-20-full-suite-python312.log` Blob `55b99d64260a73fa81dbcc667e2a276ce60736bd` 全文可访问，逐行计数 `410 ok / 22 skipped / 0 FAIL / 0 ERROR`，尾部 `Ran 432 tests in 0.707s; OK (skipped=22)`；22 项 skip 全部为 `test_unified_manifest_1_2_10.UnionSemanticsTests`，每项均有 legacy 1.2.10 superseded 原因。元数据 `2026-11-20-evidence-metadata.md` Blob `94cc1791357e821ea260bccbec3a235aac1c4ace` 记录 Windows/Git Bash、Python 3.12.3、pip 24.0、jsonschema 4.26.0、Node 22.22.2、npm 10.9.7、`rfc8785==0.1.4`、`canonicalize@2.1.0`、执行命令及 exit code 0。比较测试 HEAD `1d5296e0effa7c6466c9e7aef9f071827ff8aa1c` 与证据提交，唯一新增为上述日志和元数据文件，测试源码及 validator 未变。**测试证据层 ACCEPTED（独立回读，不等同 A 本地重跑）**。A Integration Owner 批准开发基线范围内一次有限 CI 豁免：此前 CI runner allocation failure（`runner_id=0`、`steps=[]`）属于外部基础设施阻塞；该 finding 的 CI 测试级输出要求由精确测试 HEAD 的完整本地原始日志及元数据替代。CI 状态仍为 `NOT VERIFIED`，不记为 CI PASS；CI 恢复后补跑作为后续补验，不再阻塞本 finding 关闭。此豁免仅适用于 F-43-03 开发基线测试证据，不授予生产发布、生产 conformance 或 Runtime 授权。**F-43-03 CLOSED**。

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
| 状态 | CLOSED |
| 责任 Owner | Storage Owner |
| 回流去向 | Storage Owner 裁决 → #25 owner-decision 载体 + 本台账 |
| 关闭条件 | Storage durable write + signed receipt → COC quorum append binding exact ref/digest → 双向回读 → 才 owner release；重试用同一 immutable identity |
| 最新裁决 / 证据 | R43：Storage normative protocol independently reviewed and accepted for limited architecture-contract scope; Commit `8e5e2d9f2d27f0d9d08c208798f3cd9ddd1598ae`, Blob `7ecd7f21724c4f6f46c1618a9d102e5d27ea35de`; #25 `7023314994`; #43 `7023315618` / A review `PENDING` |
| 范围限制 | 架构可行性 finding，非实现验证 |


R41（A-OWNER-INTEGRATION-R41-2026-11-19）：F-43-06A 维持 OPEN/BLOCKED，Storage Owner 派工定义规范性双持久化与崩溃恢复协议。规范写序必须是 Storage durable write → signed receipt → COC quorum append，且 append 明确绑定 exact immutable ref + digest → 双向回读 Storage 与 COC 的 exact identity/ref/digest/receipt → 全部一致后 owner release。所有重试/超时恢复必须复用同一 immutable identity/idempotency key；禁止生成新 identity 掩盖不确定提交。需定义 canonical-copy 唯一权威副本、复制方向、冲突处理、receipt 与 quorum proof 绑定、各崩溃窗口恢复判定及 UNKNOWN/BLOCKED fail-closed。交付到既有 #25 owner-decision 载体并回填本 ledger；不要求实现/运行时证明。本 finding 需 A 独立复审，不因派工或草案完成自动关闭。

R42（A-OWNER-INTEGRATION-R42-2026-11-19）：F-43-06A 继续 OPEN/BLOCKED。A 裁定 AID-2026-010 当前授权范围为 Integration Review；其 accountable_owner 为 NOT_ASSIGNED 的状态不能解释为授予 Storage Owner 规范决策权。Finding 上标注 Storage Owner 是技术责任分配，不等于 AI-EXEC Work Item 授权。A 不授权将 AID-2026-010 扩张解释为 Storage Owner 的规范决策授权，也不在配额冻结 ACTIVE 时自行创建/签发新的 AID 或独立 Work Item。解阻须由有权 Work Item issuer 建立独立 Storage Owner Work Item，明确独立 AID、accountable_owner、授权范围/交付载体及 AI-EXEC-001 v1.1 + AI-EXEC-002 v1.1（或正式更新版本）的适用提示词版本；随后 Storage 才能作出其自有规范决定。此裁定不妨碍 Storage Owner 在获授权前提供非约束性技术输入，但不得登记为 ACCEPT/REJECT 或权威规范决定。

R43（A-OWNER-INTEGRATION-R43-2026-11-20）：A 已在独立 Storage Work Item AID-2026-011 授权上下文下，回读 Storage Owner `STORAGE-OWNER-2026-11-20-001`。精确 Commit `8e5e2d9f2d27f0d9d08c208798f3cd9ddd1598ae`、文件 `reviews/storage-consistency/phase-3.8.3-storage-canonical-joinproof-dual-persistence-and-recovery-protocol.md`、Blob `7ecd7f21724c4f6f46c1618a9d102e5d27ea35de`；既有分支 `session-storage-consistency-forget-atomicity-2026-11-16` 回读同 Blob。核验 Storage durable write → signed durable receipt → COC quorum append exact binding → 双向权威回读 → owner release eligibility；Storage canonical JoinProof bytes 与 COC binding/commit authority 分离；10 类 crash/recovery matrix；exact replay 同 identity/digest；changed digest/immutable parameter conflict；UNKNOWN/BLOCKED 与 INTEGRITY_CONFLICT fail-closed；不以 timestamp/cache 覆盖；不声称 XA/2PC。Storage 与 COC 各自的 authority 边界、D/I/C 独立 release predicate 和生产实现非主张均明确。**裁定 F-43-06A CLOSED（仅限 Storage-owned 双持久化、canonical-copy、恢复与证据绑定架构规范交付）**。不代表生产实现、真实 receipt/quorum、CI、Runtime conformance 或生产授权。Storage #25 comment `7023314994`、#43 comment `7023315618`。

R43 对 F-43-07 Stage 2：A 回读同一 D Blob `05a24f7eab663f66a3153d79adfab699b275f1a6` 对应的 Storage `STORAGE-OWNER-2026-11-20-002` 决定，确认 `ACCEPT WITH LIMITATIONS`。限制被接受为 Storage 权威边界：D Storage PREPARED_HIDDEN prepare receipt 不等同 F-43-06A RecoveryJoinProof durable receipt；COC applicability、ParticipantIntent schema/cardinality、quorum algorithm/threshold 仍由 COC 自决；RecoveryJoinProof canonical bytes 归 Storage，COC 保存 quorum binding envelope；H consumer mapping/currentness 仍待 H。D §2.2/§3.1/§6.1 的 prepare receipt 应按独立记录/类型理解；§3.2/§5.3/§6/§8 的 COC 语义仅为条件提案，须 COC 自有权威接受；§6.5 canonical-copy 规则不得被解释为 COC 持有第二份可竞争 RecoveryJoinProof 内容副本。当前 D Blob 无需为满足 Storage Stage 2 决定而强制修改；若后续 D successor 改动上述边界，须 Storage 对新精确 Blob 重新决定。F-43-07 仍 OPEN/BLOCKED，等待 H Stage 3 及 COC 适用性/权威决定，再由 A 对同一精确版本集成复审。
## F-43-06B — BIH Registry §9 currentness / status-scope reconciliation

| 字段 | 内容 |
|---|---|
| ID | F-43-06B |
| 历史 ID / 别名 | `F-43-06`（历史别名，不得继续作主键） |
| 原始锚点 | Issue #43 comment `7016815868` |
| 问题定义 | BIH identity baseline currentness / status-scope 未完成对账。 |
| 状态 | CLOSED |
| 责任 Owner | BIH Registry Owner |
| 回流去向 | BIH Registry Owner 裁决 → A 集成复审 |
| 关闭条件 | §9 currentness 与 status-scope reconciliation 的权威证据（按该评论定义的关闭条件） |
| 最新裁决 / 证据 | #43 `7016815868`（F-43-06 P2 OPEN 原始登记） |
| 范围限制 | — |


R41（A-OWNER-INTEGRATION-R41-2026-11-19）：F-43-06B 维持 OPEN，派 BIH Registry Owner 提交 §9 currentness 与 status-scope reconciliation 权威证据。必须精确 pin 当前 Registry 源 commit/Blob，逐项说明 §9 Candidate addendum 与已决定语义的边界、identity currentness 状态及 status-scope 的权威枚举/适用范围、各 consumer acceptance 的效力边界、未决项与 owner/回流去向；不得把设计接受升级为 wire/schema freeze、governance approval 或 runtime conformance。更新 Registry 权威载体及既有 #43 锚点，提供 commit/Blob，供 A 集成复审。完成对账不自动意味着所有 BIH 消费者或治理项关闭。

R42（A-OWNER-INTEGRATION-R42-2026-11-19）：A 独立回读 #43 comment `7023107204`，确认 BIH Registry Owner Decision `B-OWNER-BIH-REGISTRY-2026-11-19-001`；Commit `840202a98cf40a0b3f194afb84bed4d5f3326658`，文件 `02-domain-model/typed-reference-registry.md`，Blob `25840cfea305dabc5725a07b4971d40132ffc811`。A 分别按 commit 与 `session-b-domain-model-phase3` 分支回读，Blob 一致。核验 §§15–16 的双语增补、currentness 与 lifecycle 区分、九类 identity 的类型化生命周期权威、失效/重验事件、fail-closed、status-scope 层次、Candidate/DECIDED/ACCEPTED/FROZEN/GOVERNANCE-BLOCKED/NOT VERIFIED 的效力边界、未决项 Owner/回流矩阵，以及历史 source pin 保留。满足本 Finding 的 §9 currentness/status-scope 权威对账关闭条件，裁定 F-43-06B **CLOSED（仅限 Registry §9 对账交付与规范边界澄清）**。不代表九类型 Candidate 整体 Accepted、不代表其他 consumer 接受、不代表 H wire/schema freeze、I governance approval 或 Runtime conformance；这些未决事项按各自 Owner/Gate 继续跟踪。#43 锚点 `7023107204`。
## F-43-07 — ParticipantRef 映射（PublicationParticipantRef / StorageVisibilityParticipantRef ↔ COC ParticipantIntentRef）

| 字段 | 内容 |
|---|---|
| ID | F-43-07 |
| 历史 ID / 别名 | — |
| 原始锚点 | Issue #43 comment `7013501942`（与 F-43-06A 同评论登记，子项 F-43-07）；交叉引用 #25 comment `7013493546` |
| 问题定义 | D PublicationParticipantRef / StorageVisibilityParticipantRef 未显式映射到（也未规范性排除于）COC ParticipantIntentRef。 |
| 状态 | CLOSED（限定于 ParticipantRef 映射/规范性排除、Owner identity binding、ordering/recovery 架构契约交付；非实现验证） |
| 责任 Owner | D Owner / Storage Owner / H Owner / COC Owner（仅限 COC applicability 决定） |
| 回流去向 | D/Storage/H 选定记账边界并定义 exact identity binding + ordering + recovery（或定义独立权威恢复枚举）→ A 集成复审 |
| 关闭条件 | 已满足：D/Storage/H 对同一精确 D Blob 独立接受；COC Owner 对精确 operation/scope/version 作出限定范围 NOT_REQUIRED 权威决定；契约给出认证负向适用性证明要求、D/Storage ref+digest 绑定、owner-local ordering/recovery、UNKNOWN/BLOCKED、同一 immutable identity 重试及重新进入 COC 范围的升级规则 |
| 最新裁决 / 证据 | R45：A-OWNER-INTEGRATION-R45-2026-11-20；D Blob `05a24f7eab663f66a3153d79adfab699b275f1a6`；Storage #43 `7023315618`；H #43 `7023562083` / H decision Blob `19e3dce92aa6d843d3d8d63b21f843eb30770b0f`；COC #43 `7023843575` / COC decision Blob `89c9e1c718195257c940fce69a2adbc81c01d034`；A 裁定 F-43-07 CLOSED（限定规范交付范围） |
| 范围限制 | 架构可行性 finding，非实现验证；编号治理不改变其技术含义 |


R41（A-OWNER-INTEGRATION-R41-2026-11-19）：F-43-07 维持 OPEN/BLOCKED。批准分阶段执行：D Owner 先在既有 D 会话/分支定义 `PublicationParticipantRef`、`StorageVisibilityParticipantRef` 与 COC `ParticipantIntentRef` 的候选映射边界或规范性排除；必须写明 nominal identity、authority/namespace、exact ref+digest、operation/idempotency identity、ordering/linearization point、receipt/quorum binding、retry/replay、crash/recovery、UNKNOWN/BLOCKED 及独立恢复枚举。D 草案不得单方面确定 Storage/COC 的物理或权威记账所有权。其后 Storage Owner 独立接受/拒绝 Storage visibility 与双持久化语义，H Owner 独立接受/拒绝消费侧映射及 status/currentness 语义；各自提供精确 artifact SHA 与限制项。D/Storage/H 三方均明确接受同一版本后，A 才做集成复审。若不能形成 ParticipantIntentRef 映射，必须明确规范性排除并定义等价的权威恢复枚举。不得把架构可行性结论当作实现验证。

R42（A-OWNER-INTEGRATION-R42-2026-11-19）：A 已独立回读 D Owner `D-OWNER-2026-11-19-008` 的精确草案：Commit `8fbef916785986fa1867ddf2eb3e3a5e4b366c5e`，文件 `08-bmcp-protocol/d-publication-storage-coc-participantref-mapping-boundary-1.0.md`，Blob `05a24f7eab663f66a3153d79adfab699b275f1a6`；在既有 remediation 分支再次读取得到同一 Blob。草案可作为阶段一 D-owned proposal；它明确三种 ref 为不同 nominal identity，采用部分跨域绑定而非身份合并，并将 Storage/COC/H 自有语义留待各自接受。F-43-07 维持 OPEN/BLOCKED；阶段二 Storage Owner 与阶段三 H Owner 对同一 Blob 的独立接受尚未取得，且 Storage 规范决策授权缺口须先解决。A 不把 D 草案视为三方共同基线。

R43（A-OWNER-INTEGRATION-R43-2026-11-20）：F-43-07 Stage 2 Storage Owner 已按独立 Work Item AID-2026-011 对 D Blob `05a24f7eab663f66a3153d79adfab699b275f1a6` 作 `ACCEPT WITH LIMITATIONS`（`STORAGE-OWNER-2026-11-20-002`，见 #25 comment `7023314994` / #43 comment `7023315618`）。A 独立复核五项限制：prepare receipt 与 RecoveryJoinProof durable receipt 分离；COC quorum algorithm/threshold 由 COC 自决；RecoveryJoinProof canonical bytes 归 Storage、COC 保存 binding envelope；COC applicability 尚待权威决定；H 消费侧尚待独立审查。该决定不等于 COC 接受，也不等于 H 接受。当前 D Blob 无需为满足 Storage 决定强制修改；若 D 后续修改 receipt 类型边界、COC applicability/ParticipantIntent/quorum、canonical-copy 或恢复语义，须重新取得受影响 Owner 对 successor Blob 的明确决定。F-43-07 继续 OPEN/BLOCKED，等待 H Stage 3 与 COC 自有适用性/权威边界决定，随后 A 对所有同版决定集成复审。
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


R44（A-OWNER-INTEGRATION-R44-2026-11-20）：A 完成 F-43-07 最终集成复审。审查基线为 D Owner `D-OWNER-2026-11-19-008` 的 Commit `8fbef916785986fa1867ddf2eb3e3a5e4b366c5e`、文件 `08-bmcp-protocol/d-publication-storage-coc-participantref-mapping-boundary-1.0.md`、Blob `05a24f7eab663f66a3153d79adfab699b275f1a6`。Storage Stage 2 `STORAGE-OWNER-2026-11-20-002`（#43 `7023315618) 与 H Stage 3 `H-OWNER-2026-11-20-001`（Commit `49e1b0f7dcd65bfde6759e633d867d00120927ae`，文件 `08-bmcp-protocol/phase-3.8.36-h-owner-decision-f43-07-stage-3-consumer-mapping.md`，Blob `19e3dce92aa6d843d3d8d63b21f843eb30770b0f`，#43 `7023562083`）均对同一 D Blob 作出 `ACCEPT WITH LIMITATIONS`；H 的精确决定原文及 #43 锚点已回读。三方同版接受已齐，但不满足当前 Finding 的完整关闭条件：D §3.2/§5.3/§6/§8.2 的 COC 分支仍是条件性提案，COC applicability、ParticipantIntent schema/cardinality、append/quorum 及 COC 相关 ordering/linearization 尚无 COC 权威决定；H 明确要求无精确 scope/version 的认证 `COC NOT_REQUIRED` 证明时，缺少 ParticipantIntentRef 必须保持 `UNKNOWN/BLOCKED`。不能把条件提案或 COC 缺席解释为已映射、已排除或已接受。原关闭条件要求映射或规范性排除文本、identity binding/ordering/recovery 定义及 D/Storage/H 三方接受；当前 COC 相关适用性及 ordering 仍未决。**A 裁定 F-43-07 维持 OPEN / BLOCKED，不裁定 CLOSED。** COC 是独立权威依赖，不得由 D/Storage/H 或 A 代替其决定；须由 COC authority 对精确 operation/scope/version 给出适用性决定，并在适用时接受/定义其 ParticipantIntent/ref+digest/member inclusion/quorum/ordering/recovery 语义，或给出认证的 NOT_REQUIRED disposition 及等价恢复边界。之后如改变 D Blob，受影响 Owner 须对 successor 精确 Blob 重新决定，再由 A 复审。此裁定不否定 D/Storage/H 已完成的同版接受；不构成 H wire/schema freeze、Runtime conformance、生产实现或生产授权。

R45（A-OWNER-INTEGRATION-R45-2026-11-20）：A 完成 F-43-07 四方最终集成复审。D 基线：`D-OWNER-2026-11-19-008`，Commit `8fbef916785986fa1867ddf2eb3e3a5e4b366c5e`，文件 `08-bmcp-protocol/d-publication-storage-coc-participantref-mapping-boundary-1.0.md`，Blob `05a24f7eab663f66a3153d79adfab699b275f1a6`，#43 `7022904207`。Storage Stage 2：`STORAGE-OWNER-2026-11-20-002`，ACCEPT WITH LIMITATIONS，#43 `7023315618`；A R43 已接受并保留其五项限制。H Stage 3：`H-OWNER-2026-11-20-001`，ACCEPT WITH LIMITATIONS，Commit `49e1b0f7dcd65bfde6759e633d867d00120927ae`，文件 `08-bmcp-protocol/phase-3.8.36-h-owner-decision-f43-07-stage-3-consumer-mapping.md`，Blob `19e3dce92aa6d843d3d8d63b21f843eb30770b0f`，#43 `7023562083`；H 的同版接受及限制已在 R44 精确回读。COC Owner 决定 `COC-OWNER-2026-11-19-001`，AID-2026-013，Disposition **NOT_REQUIRED（严格限定 operation/scope/version）**，分支 `recovery/c-owner-tree-2026-11-18`，Commit `ec59bacd2ac4d8695275578ef833db63ff29bd46`，文件 `reviews/causal-order-coordinator/phase-3.8.37-coc-f43-07-applicability-decision.md`，Blob `89c9e1c718195257c940fce69a2adbc81c01d034`，#43 `7023843575`；A 已回读全文与锚点。COC 决定仅排除 D PublicationParticipantRef / StorageVisibilityParticipantRef 的指定 PublicationOperationId 生命周期，且仅在不涉及受保护 C Provider Side Effect、不消费/终结 I Authorization Receipt、不是 JF-10 Prepared-Participant/XID Bridge 时成立；无法证明任一负向条件则 UNKNOWN/BLOCKED。每个具体操作仍须不可变、认证的 `COC_JOIN_NOT_REQUIRED` 证明，精确绑定 D/Storage ref+digest、operation/request/tuple digest、authority/namespace/incarnation 及负向适用性条件；证明缺失、过期、未认证、不匹配或不可解析时不得推断 NOT_REQUIRED。决定明确 Storage PREPARED_HIDDEN → D Admission → Storage Terminalization → D Closeout 的 owner-local 顺序、崩溃恢复、同一 immutable identity 精确重放/冲突规则，以及进入受保护 C/I 或 JF-10 范围时重新适用 COC 的升级规则。该 COC 决定是 COC 对其自有 applicability 的权威裁定，不要求 COC 对同一 NOT_REQUIRED 范围再作第二次接受。D/Storage/H 同版独立接受 + COC 限定范围权威排除，满足本 Finding 原定“映射或规范性排除 + identity binding/ordering/recovery + 三方独立接受”的规范交付关闭条件。**A 裁定 F-43-07 CLOSED（仅限 ParticipantRef 映射/规范性排除及 Owner identity binding、ordering/recovery 架构契约交付）**。不代表 `COC_JOIN_NOT_REQUIRED` 生产签发/验签机制已部署，不代表 endpoint、真实运行时 receipt、quorum、CI、Runtime conformance、H wire/schema freeze 或生产授权；任何超出 COC 精确 scope/version、负向条件不成立/不可证明或契约版本变化的操作均不受此关闭覆盖，必须按 COC 决定重新判定，受影响 Owner 对 successor Blob 重新接受并由 A 复审。