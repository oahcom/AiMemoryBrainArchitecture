# L2-02-C-H-G-APPLIED-PROTOCOL — 启动核验记录

**LOADED 声明核验结果：`LOADED-PARTIAL`（现行版本差异已识别，正在核对指定 ADOPTED 版本）。**

已从 `oahcom/AiMemoryBrainArchitecture` 的 `main` 实际读取：

| 文件 | 实际读取版本 | Blob SHA | 状态 |
|---|---|---|---|
| `14-ai-development/AI-EXEC-001.md` | v1.1 | `58af59af266b81109269156ea667df1a15edfb7b` | ADOPTED |
| `14-ai-development/AI-EXEC-002.md` | v1.2 | `7f5928a5d16eb12da7621cfb8bd99ca463afd859` | PENDING ADOPTION |

因此，**不能声称已经从 main 加载了 AI-EXEC-002 v1.1**。v1.2 明确记载 v1.1 经 PR #256、合并提交 `48a556491506d25e78be47957276bf3821797a0a` 采纳。本轮将以该采纳提交中的 v1.1 为执行依据，v1.2 仅披露版本差异，不把它当成已采纳规则。

- 仓库：`oahcom/AiMemoryBrainArchitecture`
- 声明的 main tip：`d61f813cac6780b6bcc5c09536a8e9bee96cc362`
- 声明的 remediation tip：`745c768deca0a5826d436744213bed3beb65cd85`
- 本轮权限：只读；不创建 PR/Issue，不写 Git，不修改任何载体状态。
- 角色边界：L2 对齐与证据核验，不代替 C/H/G/I/D/Storage Owner 批准。

## 一、治理规则与证据边界

进一步核对后，确认本轮能够读取 v1.1 的具体内容：

| 规范 | 实际采用的内容来源 | Blob SHA |
|---|---|---|
| AI-EXEC-001 v1.1 | main 当前 ADOPTED 文件 | `58af59af266b81109269156ea667df1a15edfb7b` |
| AI-EXEC-002 v1.1 | PR #256 对应的 v1.1 文件 | `f58ac86d446664c07e571a960bcd63dfd1f50f6a` |

**状态披露：** AI-EXEC-002 v1.1 的文件头在所读取的合并提交中仍写 `PROPOSED`，而 main 上 v1.2 的历史记录明确称 v1.1 已经由 PR #256 采纳。这是版本状态记录不一致，不能隐去。本轮按 v1.1 内容执行，不采用 v1.2 新增的规范要求。

执行原则：

1. C、G、H、I、D、Storage 各自只决定自己的领域。
2. A 的综合意见不是领域 Owner 批准。
3. 委派角色审查、同身份角色模拟、reference-model PASS 均不能冒充独立 Owner 签名。
4. `UNKNOWN`、`IN_DOUBT`、`NOT RUN` 不得转成成功。
5. Applied 是可验证的执行结果事实，不表示模型理解、注意或记住了内容。
6. Delivery ACK 和 Forget ACK 都不能代替 Applied。
7. 测试签名、生产签名及其信任链必须分开。

本轮只读取既有 GitHub 载体。未运行测试、未修改源文件、未创建决策或改变任何 Issue/PR 状态。

## 二、逐 Issue 对齐报告

<box border radius="lg" gap={3} padding={3}>
  **Issue #3 — Phase 3.6 C/G/H Applied Evidence & BMCP Wire Contract**

  <row align="center" wrap="wrap" gap={2}>
    <badge color="danger">HOLD</badge>
    <badge color="warning">Applied Contract Frozen: NO</badge>
    <badge>OPEN</badge>
  </row>
  **主责与协同**

  - C：FinalRequestBoundary、InferenceRequestId、Provider Side Effect、ProviderIdempotencyKey。
  - G：Applied predicate、ContextVersion、持久化、幂等、Supersession、历史结果与当前使用资格。
  - H：BMCP Delivery、Applied evidence、ACK、wire schema、capability、integrity/replay。
  - I：PermissionEpoch、授权有效性及撤销顺序。
  - D：ForgetFence、lineage、barrier。
  - B：ActorRef、ScopeRef、EnvironmentRef 类型边界。
  - A：集成协调，不拥有上述领域的批准权。

  A 的初分 `#3 → C/G/H` 得到 Issue 定义支持，但不能理解成只有这三个 Owner 有责任。I、D、B 的授权与类型语义是必要依赖。

  **Decision_ID：** `NOT_CREATED`（本会话未创建新决策）。

  **已有明确批准与其适用范围**

  1. B 已发布 ActorRef/ScopeRef/EnvironmentRef 的领域语义决定；不包含 H wire encoding 或 I 授权。
  2. C/G/H 曾对旧版 CGH-APPLIED-1.0 发布 `APPROVE WITH ENUMERATED EXCEPTIONS`，记录于 Issue #3 评论 `6919554401`。
  3. I 曾对旧版精确包发布 `APPROVE`，记录于评论 `6919760476`。
  4. D/I/B 的后续权威边界确认记录于 `6919769731`。

  这些决定不能自动转移到后续 CGH-APPLIED-1.1、修订后的 A package 或当前 H schema。尤其不能把早期 1.0 的批准当作当前统一合同冻结。

  **角色模拟与独立批准**

  - Issue 中存在正式 Owner 决策文本和 delegated role review。
  - 但当前审查不能仅凭评论由 `oahcom` 发布，就证明不同领域的真人独立签署。
  - 所有模拟性质的 C/G/H、I/D/Storage 技术审查均按角色模拟处理。
  - 未找到可证明当前精确统一包已由 C、G、H 分别独立批准的完整证据链。

  **精确来源**

  | 文件 | Commit SHA | Blob SHA |
  |---|---|---|
  | A CGH 决策包 `reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md` | 当前分支精确引入提交未核实 | `122b164bcc0760b83bf555072a36fc55631623e1` |
  | C `phase-3.6-final-request-evidence-contract.md` | `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` |
  | C `schemas/c-submit-outcome-1.0.1.schema.json` | `3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c` | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` |
  | H `schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json` | 当前分支精确 HEAD 未核实 | `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` |
  | H `validators/applied_delivery_evidence_validator.py` | 当前分支精确 HEAD 未核实 | `43f402e4a09034da197ac24856cddbd496c9c75f` |
  | G `phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md` | `0f77ffbe956c5f93df295c436fcb0a750629d595` | `a8efd1aa9696783035e157131fa9751666a4182d` |

  **发现及阻塞**

  <badge color="danger">APP-C-001 · P0 · OPEN</badge>

  C 的 `ActualInferenceRequestId` 是 schema property，但不在顶层 `required` 中；C 语义合同却要求成功的 Final Request Submitted evidence 具有实际 runtime/provider 分配的 request identity。

  - Evidence：C schema Blob `a631bc7...`；C 语义合同 Blob `fd2f47...`。
  - Owner：C。
  - 关闭条件：版本化 schema 将其设为必需并提供正负 conformance vectors；或者发布明确、有限的例外，并保证缺字段时 Full Applied 不可成立。
  - Feedback：Issue #3，评论 `6985079267`。
  - 测试：本轮 NOT RUN；既有记录称 final-request matrix SPECIFIED / NOT RUN。

  <badge color="danger">A03-01 · P1 · OPEN</badge>

  H/C 对齐存在边界类型匹配缺口。已有记录指出 H validator 对 `FinalRequestBoundaryRef` 做精确关联，但没有证明 `FinalRequestBoundaryType` 与 C 的类型完全相等。

  - Owner：H（wire/validator）、C（边界语义）、G（Full Applied 强制消费）。
  - 关闭条件：精确类型比较、错误类型负向向量、精确 Head CI。
  - Feedback：Issue #3。

  <badge color="warning">A03-02 · P1 · OPEN</badge>

  CapabilityEpoch 虽存在于 H 数据结构，但当前验证依赖注入回调，不能证明它真实解析到签名 capability attestation、Adapter build、runtime hook 与 Tier-1 observability feature set。

  - Owner：H；G 负责 Applied 接受边界。
  - 关闭条件：权威 epoch→attestation/profile 解析、签名与 currentness 验证、负向向量。
  - Feedback：Issue #3。

  <badge color="warning">G-CO-X04 · P1 · OPEN</badge>

  Compaction 产生新 ContextVersion 时，不得继承父版本的 Applied/current-use 资格。

  - Owner：G；H/C/I/D 提供相应证据边界。
  - 关闭条件：新 ContextVersion 身份、旧 DeliveryAttempt 失效、历史 Applied 仅作审计、新版本必须重新满足完整证据链。
  - Feedback：Issue #3，评论 `6979611133`。

  **当前测试证据**

  - G 的 SQLite reference model：PR #139、#143 已合并，既有 8 项测试 PASS。
  - H Applied Delivery Evidence：历史 30/30 reference candidate PASS。
  - 这些测试不证明生产 G 多副本线性化、真实 C/H/COC/I/D/Storage resolver、生产密码学、真实 Provider Side Effect 或完整 Full Applied。
  - A 的 15 项负向场景曾记录为 NOT RUN，不能视为完成。

  **尚未验证的生产行为**

  - C close-vs-send 原子序列化与 ProviderIdempotencyKey 恢复。
  - G durable Applied、crash/restart、multi-replica 与 restore fencing。
  - H 实际 Adapter/Runtime capability、签名、重放和持久化。
  - I PermissionEpoch 实时 currentness。
  - D ForgetFence/lineage 实时 barrier。
  - 跨服务 causal ordering 与 historical Applied 的 current-use eligibility。

  **当前下一步**

  C 先对 APP-C-001 作精确版本正式处置；H 更新对应 schema/validator；随后由 G 验证完整 Full Applied predicate。A 再进行 exact-Blob 集成审查。不得跳过 C 的前置决策启动 A03-01。
</box>

<box border radius="lg" gap={3} padding={3}>
  **Issue #29 — Phase 3.8.2 HRC / RecoveryJoin / Storage Topology**

  <row align="center" wrap="wrap" gap={2}>
    <badge color="danger">HOLD</badge>
    <badge color="warning">H↔Storage: CONDITIONAL / BLOCKED</badge>
    <badge>OPEN</badge>
  </row>
  **主责与协同核验**

  原映射 `#29 → H/C` 不够完整。

  - **H：主要协议责任**，负责 RecoveryCutoff、RecoveryJoin、BMCP schema、wire adapter、semantic validator。
  - **Storage：不可缺少的共同领域责任**，负责 JoinProof 持久化、COC/Storage participant 关系、JF-10 物理解析、序列化拓扑。
  - **C：必要协同 Owner**，提供 C admission、ProviderIdempotencyKey、ProviderOutcome、PreparedParticipant 等权威证据。
  - I/D：提供各自的请求/准入 ledger、签名证明、currentness 和 gate release。
  - E：提供恢复队列、restore dispatch、publication gate。
  - A：跨领域冲突整合及最终 exact-Blob review。

  因此建议 A 将责任矩阵调整为：

  `H = 协议主责；Storage = JoinProof/物理拓扑共同主责；C/I/D/E = 领域证据 Owner；A = 集成协调。`

  这是 L2 建议，不是对正式 Accountable Owner 的重新指派。

  **Decision_ID：** `NOT_CREATED`。

  **精确来源及测试证据**

  <text color="secondary" size="xs">当前 H 分支最后可核实 HEAD：`36703686e3b40a07322a4d7855554b18b60237aa`。它比已测试 HEAD `654d4449fd491cdda37d9761fe63a3efca55dc9d` 前进一个文档提交；该提交仅修改 BIH acceptance report。</text>

  | H Artifact | Commit SHA | Blob SHA |
  |---|---|---|
  | `phase-3.6.10-h-recovery-cutoff-semantic-validator-contract.md` | `36703686e3b40a07322a4d7855554b18b60237aa` | `4c5c3771575979061e674e40f1f5f3d9b4645bd9` |
  | `tests/conformance/recovery_cutoff/test_hrc_semantics.py` | 同上 | `60a2f4db4bd12f2131ecd147db9bbe328da6db50` |
  | `schemas/bmcp.recovery-join-1.0.2.schema.json` | 同上 | `4b664e3bce465499bcdfd93796349a4ba7074002` |
  | `tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py` | 同上 | `3c61cc8c9d973a27f890e1452305e3fb0ad09f1a` |
  | `schemas/bmcp.coc-jf10-unified-1.2.17.schema.json` | 同上 | `1b8f44675f30919764481d33755c566ef5cf1ea8` |
  | `tests/conformance/recovery_cutoff/test_i_crypto_profile.py` | 同上 | `01239e06e8f4464f49acd34241dc00899befe424` |

  Storage 侧：

  - JoinProof contract：Blob `eac350ed5cb53094bdd5626f49e6f82ebea1f78c`
  - Exact review：Blob `a92f56da78bef63ed28128c319eb277b5a7b7aa7`
  - Topology ADR：Blob `080433f8e13a500522bc2754da64057edb0ae9d8`
  - 上述三个文件的具体路径和引入 Commit SHA，本轮未能独立核实，故不补造。

  A 的物理测试矩阵：Blob `d9d4c44ec63c019463c26eacfe5b74aa223e4fc0`。

  **已有明确批准**

  - D/E/I/Storage 的既有角色审查处置：`ACCEPT WITH AMENDMENTS`。
  - C：`ACCEPT WITH C-OWNED PROVIDER-SIDE-EFFECT AMENDMENTS`。
  - H：候选 schema/reference suite 有 CI PASS。
  - Storage JoinProof：逻辑设计已有条件性技术接受。

  上述都是委派角色审查或受限技术接受，不能当作独立人类 Owner 签名，也不能推导物理拓扑已经选定。

  **当前测试证据**

  <badge color="success">368 executed PASS</badge>

  H workflow [44215993536](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44215993536)，job `134505846435`：

  - 390 tests collected。
  - 368 executed and passed。
  - 22 skipped。
  - 22 项全部为 `test_unified_manifest_1_2_10.py` 的历史 UNION-01..22 vectors。
  - 跳过不等于通过。

  当前分支 HEAD `367036...` 只比该 CI 测试 HEAD `654d444...` 多一个 BIH 文档更新提交。因此现有结果对测试代码具有较强的延续性，但严格 exact-Head CI 仍应在 `367036...` 上重新取得证据，不能把旧 run 直接称为当前 HEAD 的 CI PASS。

  另外，101 项候选测试清单已被后续 390 项测试记录取代，不能继续用 101 项作为当前 H 套件总数。

  **发现及阻塞**

  <badge color="danger">H-JOIN-001 · P1 · OPEN</badge>

  **冻结 Owner Admission enumeration 未绑定实际传入的 admission rows。**

  证据：

  - `08-bmcp-protocol/runtime_reference/unified_manifest_semantics.py`，Blob `e26379d38825ee13d15f652d3bd019c4091da37d`。
  - Unified 1.2.12 tests，Blob `5b444aa11ffb86c145ec745752204e623c1c2b41`。
  - Owner Snapshot 1.2.17 validator/tests，Blobs `17275eebd0013f8ad8765670a7faaa40866d99d8` / `165e52c068b08eff7b5c9aa833ce49c97a55129d`。

  `validate_union()` 检查调用者传入的 admission rows，但未证明这些 rows 与签名冻结 snapshot 中的 authoritative entries、count、set digest/root 完全相等。

  独立 Owner Snapshot validator 存在，但没有完整组合进该 Join 路径。

  - Owner：H；Storage、A 复审。
  - 关闭条件：六套 I/D/C request/admission 集合分别与冻结 snapshot 证明精确相等；验证 count、root、cursor、attestation；补充截断、替换、重复、重排的对抗测试。
  - 预期：缺失完整枚举 → UNKNOWN；集合或 digest 不一致 → INVALID。
  - Feedback：Issue #29，评论 `6978565518`。

  <badge color="danger">JF-10 P0 / Gate B-C · OPEN</badge>

  **物理同一 GID / DB incarnation 恢复仍未证明。**

  - Owner：Storage、D、I。
  - 关闭条件：同一 PreparedParticipantRef、GID、DB incarnation 的真实物理解析；提交/回滚一致性；HA/failover/restore 和旧 primary fencing。
  - Feedback：Issue #29；现有 Storage ADR。

  <badge color="danger">Topology · ADR-BLOCKED</badge>

  **D/Storage 实际序列化拓扑尚未选择。**

  现有 ADR `080433...` 仅保留两种条件候选：

  - A：每个 Canonical Memory authority 一个 serializable transaction domain，必须证明实际 D/Storage runtime 共用。
  - B：独立服务加具名 durable linearizable coordinator，并通过 failover 证明。

  Check-then-write、进程锁、队列顺序、eventual replica、outbox-only coordination 均不满足要求。

  - Owner：Storage + D。
  - 关闭条件：明确选择并记录真实部署拓扑、线性化点、HA/failover/restore、read-path enforcement 和旧 primary fencing。
  - Feedback：Issue #29。

  **其余必要阻塞**

  | 项目 | Owner | 状态 |
  |---|---|---|
  | 六类 Recovery Cutoff wire-to-normalized adapter | H | OPEN |
  | 生产 canonicalization/signature/key lifecycle | I/H | OPEN |
  | 两种独立语言的生产 profile interoperability | H/I | OPEN |
  | 实际 COC quorum prefix enumeration 与 durable readback | Storage/H | OPEN |
  | 六套 Owner ledger 的真实枚举与 currentness CAS | I/D/C | OPEN |
  | E restore queue、protected dereference 和 publication 前硬门禁 | E | OPEN |
  | C close-vs-send、zero-byte close-first、同 Key 恢复 | C | OPEN |
  | 36 项 race/crash/failover/restore 物理矩阵 | A/各 Owner | NOT EXECUTED |

  **下一步工作**

  1. H 修复 H-JOIN-001，并将 1.2.17 snapshot validator 组合进实际 Join 验证路径。
  2. Storage 提供可执行的双向 JoinProof 持久化/readback 与 JF-10 物理证据。
  3. C/I/D 分别提供自己的权威 ledger 和 owner-local gate/currentness 证据。
  4. H/I 完成生产签名 profile 和双实现验证；测试 Seed 继续严格 TEST-ONLY。
  5. E 提供恢复执行入口的硬门禁证明。
  6. A 重新核对所有精确 Blob，取得独立 Owner 决策后再作集成处置。

  **停止条件：** 真实 Provider 行为、Owner ledger、生产签名、物理拓扑任何一项无法验证时，保持 OPEN，不以候选 schema 或 reference model 代替。
</box>

## 三、跨 Issue 领域语义裁定核验

以下是 L2 对齐结论，不是 Owner 批准。

### 3.1 Applied 必须拆成两个独立问题

<box border radius="lg" padding={3} gap={2}>
  **A. 历史 Applied 事实**

  某次提交是否真正跨过 C 的 FinalRequestBoundary？

  必须绑定：
  - InferenceRequestId / ActualInferenceRequestId
  - FinalRequestBoundaryId / FinalRequestBoundaryRef
  - 完整 Managed Region digest
  - C ProviderOutcome 和 SideEffectStatus
  - H Adapter、DeliveryAttempt、Runtime、Capability
  - G ContextVersion 和不可变 EvidenceSetDigest

  <divider color="subtle"/>
  **B. 当前使用资格**

  即使历史 Applied 成立，现在是否仍允许使用？

  必须重新考虑：
  - I PermissionEpoch/currentness
  - D ForgetFence、Lineage、Barrier
  - G 当前 ContextVersion 和 Supersession
  - C/H 证据是否仍绑定正确请求与运行实例
  - Storage 恢复及 anti-rollback 状态
</box>

**关键结论：历史 Applied ≠ 当前可使用。**

如果 C submission 与 Forget/revocation 的因果顺序不能证明：

`Unknown → protected memory suppressed`

不能利用独立 wall-clock timestamps 排序，也不能利用 Delivery ACK、Forget ACK 或事后观察推断成功。

### 3.2 强制消息族区分

| 消息/事实 | 能证明什么 | 不能证明什么 |
|---|---|---|
| Delivery ACK | 传输或交付阶段的确认 | Applied |
| Forget ACK | Forget 操作的确认 | Applied 或物理擦除 |
| Applied evidence | 满足对应执行事实的证据 | 模型理解、记住内容 |
| C SubmitOutcome | C 所拥有的提交及 Provider Side Effect 事实 | G 已接受 Applied |
| G Applied commit | G 接受并持久化其 Applied 状态 | I/D 当前授权仍有效 |
| RecoveryJoin | 恢复参与者与 Owner 证据的对应关系 | 自动释放 Owner gate |

### 3.3 生产签名边界

H 当前 Python/Node 候选测试覆盖 RFC 8785 JCS、Ed25519、digest 和 signature preimage 的有限差分。

但：

- 测试 Seed 是 TEST-ONLY，严禁生产复用。
- I Profile `AIMBA-I-CRYPTO-1.0` 仍为候选。
- Trust Root、key lifecycle、historical verification、anti-rollback 未完成正式授权。
- 两套测试实现通过固定向量，不等于两套生产 SDK 完成互操作。

**不得宣布生产密码学通过。**

## 四、跨 Issue Findings 登记表

以下全部沿用既有 Issue，不创建新 Finding 载体。

| Finding | Severity | Owner | 当前状态 | 回流 |
|---|---|---|---|---|
| APP-C-001 | P0 | C | OPEN | #3 |
| A03-01 | P1 | C/H/G | OPEN | #3 |
| A03-02 | P1 | H/G | OPEN | #3 |
| G-CO-X04 | P1 | G | OPEN | #3 |
| CFG-G8-HMAP-01 | P1 | H/C/G/I/D/B/A | BLOCKED | #3 |
| H-JOIN-001 | P1 | H | OPEN | #29 |
| JF-10 P0 | P0 | D/I/Storage | OPEN | #29 |
| D/Storage topology | BLOCKER | D/Storage | ADR-BLOCKED | #29 |

每项关闭条件如下：

1. **APP-C-001**：C 发布明确 schema 必需性修订或有界语义例外，并提供精确测试证据。
2. **A03-01**：H/C 精确 boundary type 相等性验证，G 强制消费。
3. **A03-02**：H 提供真实 capability attestation 解析与 currentness 验证。
4. **G-CO-X04**：Compaction 新版本不得继承旧 Applied/current-use 资格。
5. **CFG-G8-HMAP-01**：八类消息逐一对应同一版本的 schema、字段、validator 和 Owner 决定。
6. **H-JOIN-001**：冻结 snapshot 与实际输入行精确集合相等。
7. **JF-10 P0**：真实同一 GID/DB incarnation 的提交、回滚、恢复证明。
8. **D/Storage topology**：选定实际序列化拓扑，完成故障切换、恢复和旧 primary fencing 证明。

## 五、Phase 3.8 D/E/I/C/Storage 合同协调结果

<box border radius="lg" padding={3} gap={2}>
  <title size="lg">领域对齐矩阵</title>
  | 领域 | 必须保留的权威边界 | 当前结论 |
  |---|---|---|
  | D | ForgetFence、lineage、barrier、恢复顺序 | OPEN |
  | E | Restore dispatch 前硬门禁及 publication gate | OPEN |
  | I | PermissionEpoch、签名证明、currentness CAS | OPEN |
  | C | Provider Side Effect、Final Request、Idempotency | OPEN |
  | Storage | JoinProof、durability、JF-10、序列化拓扑 | OPEN |
  | H | wire schema、semantic validator、crypto mapping | CANDIDATE |
  | G | Applied predicate、幂等、持久化、Supersession | DESIGN DRAFT |
</box>

需要特别防止四种跨领域错误：

- Storage 可以持久化 JoinProof，但不能释放 I/D/C 的 gate。
- I 的 COMMIT_WON 不等于 C 的 Provider Side Effect 成功。
- D 的 ForgetFence 完成不自动证明历史 Applied 无效，也不自动证明物理擦除。
- E 不得在 Recovery gate 未通过时启动 restore queue、protected dereference、lease execution、retry replay 或 publication。

### RecoveryJoin 双向证明

必须同时满足：

**方向 A：Owner Admission → COC ParticipantManifest**

每一条 I/D/C admission 都必须对应：
- 精确 COC participant；
- 或明确的 no-effect/out-of-scope disposition。

**方向 B：COC ParticipantManifest → Owner Evidence**

每一条 COC participant 必须能够反向找到：
- 主 C admission；
- 相关 I/D/C Owner Evidence；
- 必要 Storage/JF-10 证据。

六套集合不得合并成一个状态：

- I Request
- I Admission
- D Request
- D Admission
- C Request
- C Admission

并且：

`OwnerAdmissionRef ≠ OwnerEntryRef`

`OwnerRequestDigest ≠ OwnerEntryDigest`

两组引用必须分别验证，不能因为字段值看起来相似就认为身份相同。

## 六、最终逐 Issue 处置

| 项目 | #3 | #29 |
|---|---|---|
| Delta_Scope | C/G/H Applied 与 BMCP 契约 | HRC/RecoveryJoin/Storage |
| Decision_ID | NOT_CREATED | NOT_CREATED |
| 已有技术证据 | 有，存在历史受限批准 | 有，候选测试及角色审查 |
| 独立 Owner 批准 | 当前统一版本未证明 | 未证明 |
| 生产行为验证 | 未完成 | 未完成 |
| 主要阻塞 | C Owner 决定、八类消息统一、Applied predicate | H-JOIN-001、JF-10、实际拓扑 |
| 当前状态 | HOLD | HOLD |

**Unresolved_Findings：**

1. C 对 APP-C-001 的正式处置仍缺失。
2. H 的八类 Applied 消息族尚未形成统一版本的完整映射。
3. G 的 Applied 生产持久化及 current-use 资格尚未验证。
4. Storage JoinProof 仍缺真实 Owner Ledger 与 COC quorum 证据。
5. D/Storage 拓扑尚未选定。
6. JF-10 生产物理恢复尚未通过。
7. 36 项物理 race/crash/failover 案例尚未完成。
8. 各领域精确版本的独立 Owner 决策尚未全部取得。

## 七、提交给 Owner A 的集成建议

<badge color="warning">RECOMMENDATION — KEEP BOTH ISSUES OPEN</badge>

建议按以下依赖顺序推进，而不是同时宣布两项集成完成：

1. **先解决 #3 的 C 权威缺口。** 没有 C 的实际 request identity 与 Provider Side Effect 语义，就不能建立可信 Full Applied。
2. **H 完成八类 Applied wire mapping。** 不把 Applied Delivery Evidence 或 JF-10 五类消息误算为八类协议覆盖。
3. **G 明确 Applied 历史事实与 current-use 的分离。**
4. **#29 继续推进双向 JoinProof。** 重点解决 H-JOIN-001，组合 Owner Snapshot 1.2.17 验证器。
5. **Storage/D/I 解决物理序列化和 JF-10。**
6. **E 补齐恢复路径硬门禁。**
7. **A 在所有 Owner 新决定之后刷新精确 Blob，并重新执行集成审查。**

本次不替 A 选择架构、不替 C/G/H 批准合同，也不替 D/Storage 选择拓扑。

**最终 L2 结论：**

- #3：`HOLD — Applied Contract NOT FROZEN`
- #29：`HOLD — RecoveryJoin / Physical Conformance NOT PROVEN`
- H 现有候选测试：局部 PASS，不等于生产协议通过。
- Storage JoinProof：逻辑结构已有实质进展，但端到端仍未证明。
- Global Forget、生产激活、物理擦除：均不得宣称完成。

**登记义务最终状态**

| 字段 | #3 | #29 |
|---|---|---|
| Decision_ID | NOT_CREATED | NOT_CREATED |
| Delta_Scope | 已界定 | 已界定 |
| Relevant_Artifacts | 已列可核实路径/Blob；缺失 Commit 明示 | 已列可核实路径/Blob；缺失 Commit 明示 |
| Evidence | Issue #3 及 Owner 分支读取、历史 CI | Issue #29、H exact-head CI、Storage review |
| Unresolved_Findings | APP-C-001、A03-01/02、G-CO-X04、G8 | H-JOIN-001、JF-10、Topology |

未写 Git、未创建 PR/Issue、未关闭载体、未改变 assignee 或现有 PR 状态。

报告交付对象：**Owner A — Cross-owner integration review**。

