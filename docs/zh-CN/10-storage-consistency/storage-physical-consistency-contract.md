---
document_metadata:
  domain: consistency-recovery
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-098/manifest.yaml"
        - "14-ai-development/work-items/AID-2026-098/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Candidate contract text only; no backend conformance, crash-recovery, power-loss, restore or production durability evidence is claimed."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Storage/Consistency physical transaction, durability, visibility and recovery contract candidate"
    canonical_scope_id: "consistency-recovery/storage-physical-consistency"
    canonical_scope_keywords:
      - storage-atomicity
      - durability
      - crash-recovery
      - visibility
      - forget-fence-projection
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "10-storage-consistency/storage-physical-consistency-contract.md"
    en: "docs/en/10-storage-consistency/storage-physical-consistency-contract.md"
    zh-CN: null
---
# Storage 物理一致性合同——候选规范

- 工作项：AID-2026-098（PROVISIONAL）
- 版本：0.1.0-draft
- 日期：2026-11-26
- 状态：**Draft / Candidate / Informative（草案 / 候选 / 参考性）**
- 归属：user-authorized operator (delegated by account owner)；代理登记，非自然人 Owner 签署
- Canonical 源文件：[10-storage-consistency/storage-physical-consistency-contract.md](../../../10-storage-consistency/storage-physical-consistency-contract.md)
- English mirror：[EN](../../en/10-storage-consistency/storage-physical-consistency-contract.md)


## 1. 目的、状态与术语

本候选规范补齐 AID-2026-095 所识别 F8 Storage Atomicity 缺口的**文档合同形状**，并不关闭 F8。其目的在于把物理事务、持久性、可见性、恢复与防回滚义务写成可证伪的检查条件。

术语：

- **Owner 事实**：由相应责任 Owner 签发的领域事实，例如 D CanonicalCommit/Fence、E Accepted/Compiler 状态、G ContextVersion/Applied、I 授权/Global Forget Completion。
- **Storage 事实**：关于物理事务、参与者、日志位置、持久性级别、回执、副本应用或恢复激活的物理事实。
- **GID**：协调多参与者操作的稳定全局事务标识。GID 不等于 D commit cursor、E receipt ID、F watermark、G Applied ID 或 I PermissionEpoch。
- **可见性指针（Visibility pointer）**：消费者解析已准备写入时使用的已提交物理指针/版本。它是 Storage 机制，不是领域权威。
- **Unknown**：调用方无法确定物理提交是否到达终态。Unknown 既不是提交，也不是中止。

后端配置档必须声明实际事务范围、隔离级别、日志模式、同步持久化设置、副本策略、备份模型及恢复限制。本候选规范不选择 SQLite、PostgreSQL、分布式数据库、WAL、共识或 COC 拓扑。

## 2. 权威边界与事务边界

### 2.1 单资源原子提交

对持久化在单一事务资源中的每个 Owner 逻辑操作，使该操作可见所需的全部物理记录必须一起提交或一起中止。具体写集合由 Owner 合同决定，适用时包括：

- 不可变对象/版本载荷及其 provenance/lineage 引用；
- 由 Owner 的 expected-version CAS 保护的 current-version 指针更新；
- Owner 签发的 commit sequence/cursor 引用（Storage 只持久化，不得签发）；
- 幂等键、规范化请求摘要及持久结果/回执；
- Owner 的持久 outbox/change-intent 行；
- 防止 prepared 数据提前可读所需的参与者/可见性元数据；
- 用于授权操作的当前 D Fence / I authorization 观察值，或对其权威版本进行事务性验证的引用。

不得有任何子集单独对外可见。CAS 或校验失败必须不留下部分对象、指针、幂等结果、outbox 事件或成功回执。相同幂等身份与摘要的重复请求解析为原始结果；摘要不同则冲突。

### 2.2 各 Owner 的必要写集合

- **D canonical commit：** D 拥有 canonical identity、version/lifecycle 语义、canonical commit cursor 和 canonical change identity。物理事务必须原子持久化不可变 canonical version、current pointer/CAS、D sequence/cursor 引用、D 幂等结果、D commit receipt 及 D canonical-change outbox。Storage 只提供物理原子性，不得创造或重新分配 D 标识。
- **E compiler/admission：** E 拥有 Accepted receipt、compiler state、producer admission 和 compile-intent 语义。E 的 accepted envelope/digest/receipt/state 与 E compile-intent outbox 必须在 E 选择的事务边界内原子提交。这不是 D canonical-change outbox，也不会使事件成为 canonical。除非存在明确获接受的跨 Owner 协议，E 与 D 提交属于不同 Owner 事务。
- **G context/delivery：** G 拥有 ContextVersion、delivery intent 及其 delivery-state 投影；G 根据自身合同独占 Applied 决策权。G 自身的 version/intent/ledger 记录及 G receipt 必须具有可恢复的物理边界。Storage receipt 不等于 Delivered、Accepted-by-Adapter 或 Applied。
- **I authorization：** I 拥有 authorization decision、PermissionEpoch、retention/global Forget policy 和 Global Forget Completion。Storage 持久化或验证其引用，不签发 I 决策。

### 2.3 跨资源操作与线性化

本地数据库事务只在该数据库内部具有原子性。两个独立数据库、队列、对象存储、索引或副本不得仅因使用相同请求标识就被描述为一个原子事务。

当一个逻辑操作跨越多个资源时，协议必须规定参与者身份、prepare 记录、持久化投票、唯一终态决策权威、commit/abort 恢复、参与者幂等重放及可见性门控。在所有必要参与者达到持久终态且获接受的协调协议确认提交之前，prepared 写入必须保持隐藏。未来 COC/GID 协议目前仅是候选机制；其密码学、quorum、成员配置和防回滚冻结阻塞项仍按 #1211 保持开放。

单资源操作的物理线性化点是该后端配置档认可的持久数据库 commit record/终态提交。协调操作的线性化点是获接受协调器的持久终态 commit decision，且必须满足参与者持久性谓词。Prepare、enqueue、本地写入、发送 ACK 或构造响应均不是线性化点。

## 3. WAL、检查点与崩溃恢复

### 3.1 先日志后数据

若后端使用 WAL 或等效 redo log：

1. 每条事务记录必须包含事务身份、有序日志位置、记录类型/长度及完整性校验。
2. 所有已提交变更所需的 redo 信息必须先到达配置要求的持久日志，才可确认 commit record。
3. commit record 及所需日志前缀必须越过后端声明的持久化屏障（例如 fsync 或等效机制），之后才能返回持久成功回执。
4. 只有在恢复可从保留日志重建已提交状态时，数据页才可延后刷盘。
5. 日志截断/回收不得越过恢复、副本、备份或未决参与者所需的最早检查点。

仅有 WAL 标签或同步标志配置，不能证明存储设备、文件系统、虚拟化卷或云服务商兑现了刷盘承诺。

### 3.2 检查点与重放顺序

检查点必须标识其代表的精确持久日志位置，并且必须具备崩溃原子性或可恢复暂存机制。后端必须：

1. 验证数据库身份、格式/版本及检查点完整性；
2. 定位最后一个有效检查点及其后的连续有效日志前缀；
3. 验证日志帧、校验和、事务边界及 commit marker；
4. 按日志顺序 redo 完整且已提交的事务；
5. 丢弃/undo 不完整或未提交的事务；
6. 在暴露恢复状态前持久化恢复结果和 recovery high-water mark；
7. 保留/重放副本、备份或未决参与者仍需的日志尾部。

检查点不构成跳过缺失日志段的许可。日志缺口、序列不一致、校验和无效或事务结果未知，都必须停止相关可见性，并要求从权威源修复/重建。

### 3.3 部分写入与崩溃切点

只有完整 commit record 及其所需前置日志记录满足后端持久化顺序规则时，事务才算提交。部分记录、撕裂页、截断日志尾或缺失 commit marker 均不构成成功提交。若完整性检查无法区分已提交与未提交状态，则结果为 Unknown，相关记录必须保持隐藏并等待对账。不得把损坏转换成空数据库、虚假的成功回滚声明或推定提交。

恢复必须先暂存备份、验证 schema 和完整性、应用所有强制权威投影与恢复记录，再原子激活暂存镜像。激活前失败必须保留原 live 镜像；激活期间失败或结果不确定时，必须停止服务，直到确定性恢复路径建立唯一有效镜像。

## 4. 持久回执

### 4.1 含义

**Storage Durable Commit Receipt（Storage 持久提交回执）**仅证明指定物理参与者达到其后端配置档声明的终态持久性。它不证明语义有效性、授权、canonical commit、compiler acceptance、索引覆盖、交付、应用、Forget 完成或物理擦除。

结果词汇：

- `COMMITTED`：已证明终态提交及声明的持久化屏障；
- `ABORTED`：已证明终态中止，且事务中的任何写入均不可见；
- `UNKNOWN`：尚不能证明终态。它是查询/对账结果，不是持久终态回执。

### 4.2 最小字段

终态回执至少必须包含：

| 字段 | 含义 |
|---|---|
| `receipt_id` | 稳定物理回执标识 |
| `gid` | 全局事务标识，或明确的单资源事务标识 |
| `participant_id` | 稳定参与者/资源标识 |
| `owner_operation_ref` | 发起 Owner 操作的不透明引用；Storage 不重新签发 |
| `request_digest` | 不可变参与者请求/写集合摘要 |
| `terminal_state` | COMMITTED 或 ABORTED |
| `storage_commit_ref` | 后端提交标识 |
| `durable_log_position` | WAL LSN 或后端等效持久位置 |
| `durability_profile` | 实际使用的、具名且带版本的刷盘/复制保证 |
| `visibility_pointer` | 操作发布数据时的已提交物理版本/指针 |
| `authority_observations` | 适用时所检查的精确 D Fence cursor/generation 与 I PermissionEpoch 引用 |
| `backend_epoch` | 足以检测过期回执的后端实例/term/配置引用 |
| `integrity_digest` | 绑定回执字段的完整性摘要 |
| `committed_at` | 用于审计的后端时间戳；不是排序权威 |

回执不得伪造 D commit cursor、D ForgetFence generation、E AcceptedReceipt ID、F IndexWatermark、G ContextVersion/Applied ID、H ACK 或 I PermissionEpoch。某操作要求的字段缺失时，该回执对该操作不可用。

相同 GID + participant + request digest 必须返回相同终态回执。相同 GID/participant 但摘要不同必须冲突。Unknown 后重试必须查询/对账同一 GID，不得创建新 GID 来绕过未决结果。

## 5. 可见性、隔离与读己之写

1. 未提交和 PreparedHidden 数据不得对普通读取、索引、缓存、Context 快照或交付可见。
2. 写入只有在物理线性化点、持久回执及全部必要 Owner 谓词成立后，才具备可见资格。
3. 后端配置档必须声明隔离级别。对同一 canonical pointer、GID participant 或 Fence projection 的冲突写入必须串行化或产生确定性冲突。若 Snapshot Isolation 仍允许违反声明不变量的 write skew 或谓词竞态，则不足以满足要求；配置档必须增加显式锁或 serializable 验证。
4. 返回 COMMITTED 后，提交会话必须满足 read-your-writes。任何被路由到其他连接、副本或缓存的读取，必须至少观察到回执的 commit position；否则必须明确标记 stale/unknown，并排除在权威决策之外。
5. 副本只有在 applied position 达到所需 commit position 且 D Fence/I epoch 观察值为最新时，才可提供权威读取。滞后、位置缺失或重放不确定时，对受影响数据 fail closed。
6. 提交前开始的读取可按声明的 snapshot 返回先前提交版本。权威路径上成功提交后才开始的读取，不得返回旧版本却声称具备 current/linearizable 可见性。

## 6. Forget Fence 投影与防回滚

### 6.1 单一权威

AID-2026-089 / 已合并 PR #1232 是本边界的治理方向依据：

- D 是 ForgetOperation identity/state、typed canonical targets 与 transitive lineage coverage、Scope coverage、单调 ForgetFence generation/cursor、canonical suppression 和 D-domain proof 的唯一逻辑签发者。
- Storage 本地 Fence 行是派生、可重建的投影。不得分配独立 sequence/generation/cursor，不得定义 target/lineage coverage，不得授权读取/发布，也不得声明 Forget 完成。
- I 独占 authorization、global policy 和 Global Forget Completion。物理擦除与逻辑抑制仍是不同事实。

本候选规范不创建第二个 Fence 权威。Storage 投影存储 D 签发的精确 generation/cursor 及执行所需的 typed target/Scope/lineage 数据；不得自行推进逻辑 generation。

### 6.2 投影新鲜度与服务门控

在服务或发布受影响数据前，Storage 必须证明其投影覆盖该 target 及 source lineage 适用的最新 D Fence snapshot/cursor。缺失、过期、损坏、回滚、不完整或 Scope 不足的投影必须 fail closed。投影可以从 D 权威源重建，但不得从本地行顺序或 namespace 猜测重建。

Namespace 是 partition/scope 属性，不能替代 typed target identity、source identity、ScopeRefs 或 transitive lineage。namespace 级记录不能悄然充当 D target/lineage Fence。

### 6.3 恢复与防回滚顺序

恢复或故障切换不得仅因本地数据库备份内部一致，就暴露 Fence 之前的镜像。在任何受影响读取、索引切换、Context 物化、队列重放、交付或发布之前：

1. 恢复物理数据库并验证 checkpoint/log 链；
2. 获取并验证最新 D-authoritative Fence snapshot/cursor 及 I-authoritative PermissionEpoch/policy state；
3. 将投影覆盖范围与这些权威状态比较，并重建或隔离过期投影；
4. 验证 replica/backup/backend epoch，以及已接受部署配置档要求的独立防回滚锚点；
5. 仅在所有必要门控均为最新时开放可见性；否则对受影响数据保持不可用。

独立防回滚锚点、信任根、密钥生命周期及多节点 quorum 的精确定义尚未由本候选规范冻结。它们的缺失是阻塞项，不能成为依赖备份自身单调计数器的理由。

## 7. Owner 边界与跨域关联

| 域 | 拥有 | Storage 可以做 | Storage 不得做 |
|---|---|---|---|
| D — canonical commit 与 Forget | Canonical identity/version/lifecycle、D commit cursor/outbox identity、ForgetOperation/Fence generation 和 D-domain proof | 原子持久化 D 提供的值；执行经验证的 D Fence 投影；返回物理回执 | 签发 canonical identity/cursor/Fence generation；重定义 lineage；签发 canonical 或 Forget proof |
| E — compiler | Accepted receipt、compiler state、producer admission/work lifecycle 和 compile intent | 在 E 事务中原子持久化 E 提供的状态/回执/outbox | 把 E acceptance 当作 D canonical commit；签发 E receipt 语义；代表 E 发布 |
| F — retrieval/index | Index generation、scan watermark、coverage 和 retrieval result | 持久化索引/检查点数据并执行可见性门控 | 推进 F watermark，或从 Storage commit receipt 推断扫描覆盖 |
| G — context/delivery | ContextVersion、delivery intent/projection 和 Applied decision | 持久化 G 记录/回执；隐藏 prepared 或过期版本；提供可恢复读取 | 签发 Delivered、Accepted-by-Adapter 或 Applied；从 Storage durability 推断 Applied |
| H — protocol | Wire/transport/ACK evidence | 持久化提供的证据引用 | 签发 H ACK 或协议状态 |
| I — security/governance | Authorization、PermissionEpoch、retention/global Forget policy 和 Global Forget Completion | 持久化/验证提供的决策及 epoch 引用 | 授权、豁免策略或签发全局完成 |
| Storage/Consistency | Physical transaction、durability、log/recovery、replica/backup/restore 和 physical visibility | 提供物理事实及执行机制 | 成为竞争性的领域权威 |

跨域回执必须通过稳定引用和摘要关联，不得复用同一个命名空间表达不同事实。物理 COMMITTED 回执只证明物理参与者。崩溃后相关 Owner 必须独立解析自身语义状态。Unknown GID 在参与者回执与协调器决策完成对账前必须保持隐藏。

## 8. 审查检查点与证据分类

**解释：** `DOCUMENTED_ONLY` 行的 PASS 仅表示候选规范写出了可证伪条款，不代表 Owner 接受或 Gate A 符合性。`EVIDENCE_REQUIRED` 行的 FAIL 表示当前仓库缺少所需物理证明；未来 PASS 必须提供可复现、精确版本的证据及受影响 Owner 接受。

| ID | PASS / FAIL 检查点 | 分类 | 候选结果 |
|---|---|---|---|
| SC-01 | PASS：单资源写集合在一个事务内包含不可变载荷/版本、CAS 指针、Owner cursor 引用、幂等结果、Owner outbox 和回执；若任一必要项可独立提交则 FAIL。 | DOCUMENTED_ONLY | PASS — 已写入条款；后端尚未证明 |
| SC-02 | PASS：冲突/校验/中止不会留下部分可见写入或成功回执；若有任何子集泄漏则 FAIL。 | DOCUMENTED_ONLY | PASS — 已写入条款；后端尚未证明 |
| SC-03 | PASS：物理线性化点是持久提交（或获接受协调器的终态决策）；若把 prepare、enqueue 或响应构造当作提交则 FAIL。 | DOCUMENTED_ONLY | PASS — 已写入条款；后端尚未证明 |
| SC-04 | PASS：在声明后端配置档下证明 WAL/log framing、先日志后数据、commit marker 和持久刷盘；若回执早于必要持久化屏障则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少故障注入/设备刷盘证明 |
| SC-05 | PASS：证明 checkpoint position、检查点原子性及连续有效已提交日志前缀的重放；若截断会丢失恢复所需数据或跳过缺口则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少 checkpoint/replay 证明 |
| SC-06 | PASS：撕裂/部分记录及未完成事务被丢弃或隔离，损坏时 fail closed，恢复激活具备崩溃安全性；若暴露不确定状态则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少 crash-cut/torn-write/restore 证明 |
| SC-07 | PASS：回执包含所有适用最小字段，并区分 COMMITTED、ABORTED、UNKNOWN；若回执越权声明 Owner 事实或缺少必要绑定则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义回执形状；无实际回执证据 |
| SC-08 | PASS：相同 GID/participant/digest 重放返回相同回执，摘要变化时冲突；若重试产生重复或冲突终态则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义幂等规则；无多进程证据 |
| SC-09 | PASS：后端隔离配置明确，冲突操作串行化或确定性冲突；若声明不变量仍允许 write skew/竞态则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义要求；配置档尚未选择 |
| SC-10 | PASS：读己之写及提交后权威路径可见性成立，副本在服务前证明 applied position/Fence 最新；若旧数据被报告为当前则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少副本/可见性证明 |
| SC-11 | PASS：D 始终是唯一逻辑 Fence 签发者，Storage 投影保存 D 的精确 cursor/generation 且无本地序列；若 Storage 分配或推进 Fence 权威则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义权威规则；当前实现差异仍存在 |
| SC-12 | PASS：缺失/过期/损坏/Scope 不足的投影阻断相关读取/发布，重建使用 D 权威；若本地 namespace/sequence 被视为充分则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少端到端 fail-closed 证明 |
| SC-13 | PASS：恢复在暴露前验证最新 D Fence、I PermissionEpoch 及必要独立防回滚锚点；若 Fence 前备份可导致数据复活则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少防回滚/恢复证明 |
| SC-14 | PASS：D 拥有 canonical identity/cursor/outbox 语义，Storage 只持久化所提供的值；若 Storage 创造 D 事实则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义边界；D/Storage 精确版本接受待定 |
| SC-15 | PASS：E Accepted/compiler state/compile intent 仍由 E 拥有，并仅在 E 声明的事务边界内物理原子化；若 E acceptance 与 D commit 混淆则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义边界；E 接受待定 |
| SC-16 | PASS：G ContextVersion/delivery/Applied 仍由 G 拥有，Storage receipt 不被当作 Delivered/Accepted/Applied；若物理提交推进 G 状态则 FAIL。 | DOCUMENTED_ONLY | PASS — 已定义边界；G 接受待定 |
| SC-17 | PASS：跨资源 GID participant 具备稳定身份、持久 prepare/terminal 记录、确定性重放及唯一获接受终态决策权威；若假定独立存储天然原子则 FAIL。 | EVIDENCE_REQUIRED | FAIL — COC/GID 协议尚未冻结或证明 |
| SC-18 | PASS：备份、副本回滚、故障切换与恢复满足声明的 RPO/RTO 配置档并有可重复证据；若从单元测试或 WAL 配置推断生产持久性则 FAIL。 | EVIDENCE_REQUIRED | FAIL — 缺少工作负载/生产恢复证据 |

**计数：** 18 个检查点；10 个 `DOCUMENTED_ONLY`；8 个 `EVIDENCE_REQUIRED`。本候选基线有意将 8 个证据必需项标为 FAIL。没有任何一项构成 Gate A PASS。

## 9. 明确不主张的事项与关闭证据

本文不主张：已选定后端；COC 或 JF-10 已冻结；签发者/签名/密钥生命周期已定；共识成员或 quorum 已定；跨数据库原子性已实现；断电持久性已证明；多进程线性化已证明；生产备份/恢复已证明；RPO/RTO 已承诺；或 Owner 已接受。

要把证据必需项改为 PASS，证据包必须固定精确代码/配置/后端和测试环境；提供 prepare、commit、flush、checkpoint、副本应用和恢复激活前/中/后的可复现崩溃切点；包含重复/并发请求及摘要不匹配；验证读取路径和副本滞后；恢复 Fence 前备份并证明不复活；保留原始日志/结果；并记录 D/E/F/G/I 与 Storage 对各自受影响边界的接受。

### 当前源代码差异，必须显式处置

当前 main 快照中的 `crates/memory-storage-sqlite/src/lib.rs` 存在 Storage 本地 `canonical_forget_fences` 表及本地序列生成代码；独立的 `crates/memory-event-store-sqlite/src/forget_fence.rs` 也存在 namespace-keyed `forget_fence` 表及 `next_seq` 权威。这些只是实现观察，不是已接受架构。它们不符合 AID-2026-089 所述的单一权威方向。物理合同要求 D 派生投影，且不得存在 Storage 自有 Fence 序列。精确迁移、代码路径归属和运行时整改不属于本次纯文档 Work Item，必须由 D/Storage 审查并另行授权实施。

### 审查处置

- 候选源文档完整性：提交审查。
- D / Storage / A 语义接受：PENDING。
- E / G 消费方接受：其事务和可见性边界受影响时 PENDING。
- Normative approval：NOT CLAIMED。
- Runtime/validator 变更：NONE。
- 本文不授权合并、Issue 关闭、实现或生产启用。
