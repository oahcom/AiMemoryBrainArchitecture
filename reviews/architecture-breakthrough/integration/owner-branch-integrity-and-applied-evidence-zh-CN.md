# Owner 分支完整性与 Applied Delivery Evidence 实时复核（2026-11-18）

- Review ID: ABR-INTEGRATION-002
- 关联集成：ABR-INTEGRATION-001 / Draft PR #93
- 治理跟踪：Issue #43
- 当前 main：`e52594f181d2edb77448adcfed64a0fbdffaf3aa`
- 当前 main tree：`7096e0bc3fdc9a390fccff388f9261522fa424f2`
- 范围：Owner B/C/D/E/F/G/H/I/Storage 当前分支快照、H/C 树完整性事故恢复、Applied Delivery Evidence 1.0.0 候选与消费者接受边界。
- 结论级别：精确树/文件核验 + CI 元数据核验；不是全模块语义审计或 Owner 独立批准。

## 1. 当前状态摘要

本轮确认了一个重要状态变化：此前 A 的 H/C 分支树完整性事故报告记录的损坏 HEAD 已不再是当前 Owner 分支 HEAD。H 与 C 均已有后续恢复提交，且恢复后相对事故前基线只增加少量文件，没有继续删除原有完整树。

| 项目 | 当前证据 | 集成判定 |
|---|---|---|
| H 树完整性 | H 已从损坏 HEAD 恢复完整树；相对事故前 HEAD 仅增加 8 个文件 | **恢复已核实；事故仍须留档** |
| C 树完整性 | C 已从损坏 HEAD 恢复完整树；相对事故前 HEAD 仅增加 2 个文件 | **恢复已核实；事故仍须留档** |
| H Applied Delivery Evidence 1.0.0 | Schema、参考 Validator、11 项测试、Workflow 均存在；CI SUCCESS | **TEST/CONFORMANCE CANDIDATE** |
| CSubmitOutcome 1.0.1 | 当前 C Owner HEAD 有 Schema、测试和工作流；CI SUCCESS | **有限 CI 证据存在** |
| C workflow 1.0.1 触发路径 | 当前 workflow 只列 1.0.0 Schema；PR #94 增加 1.0.1 路径 | **触发缺陷已识别；PR #94 待审** |
| H 1.0.0 Applied 消费者接受 | H 文档明确要求 C/G/I 接受；当前未发现 C/G 对 H 1.0.0 精确 Blob 的接受决议 | **OPEN / NOT FROZEN** |
| Global Applied | G 合同是规范设计草案；实现、跨 Owner 接受未验证 | **NOT FROZEN / NOT PROVEN** |

## 2. 当前 main 与 Owner HEAD 快照

当前 `main` 分支实时读取为 `e52594f181d2edb77448adcfed64a0fbdffaf3aa`。main tree 为 `7096e0bc3fdc9a390fccff388f9261522fa424f2`。此前 PR #87 的临时默认分支文件写入已由删除提交补偿；当前 main tree 与记录的基线一致，但 Git 历史指针已前进。不得把“tree 相同”说成“commit 历史未变”。

以下 HEAD 是本轮递归树实时读取结果：

| Owner | Branch | HEAD | Blob 文件数 | 精确关键源文件 / Blob |
|---|---|---|---:|---|
| B | `session-b-domain-model-phase3` | `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | 58 | ADR-001 Fact/Claim `df77e4a93cb8fef689ae7c828888d960cbf381d6` |
| C | `session-c-agent-integration-2026-11-16` | `88992da30331121b81cf2773acab11d921daf281` | 136 | CSubmitOutcome 1.0.1 `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`; C/G Phase 3.8.23 `4860c627b4d7e84e23fb39ad83411674f3b88c7b` |
| D | `session-d-memory-brain-2026-11-16` | `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f` | 86 | Forget Fence / Publication Gate `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` |
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | 54 | Forget Fence / Derived Registration `00e37ba56596e710513c8d0568acd79141d9101b` |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | 49 | Runtime Forget suppression `ce59252dbbdc5d10d016704797e9ba12d5a941bd` |
| G | `session-g-memory-context` | `763b3d31e910db8fd29c6e4dbaff9273b7fb66b8` | 50 | Applied persistence contract EN `bd297873bc1e593280484a43cb44b56058d9c4ff`; ZH `82553a47fae2d5e796e0742b46231afe465e75b2` |
| H | `session-h-bmcp-protocol` | `6608cde89d959257db612d8ff8080f631333f3f3` | 216 | Unified 1.2.15 Schema `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; Applied 1.0.0 Schema `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`; Validator `2f6de24eea737cf75a16ead7495bea4627bb1bb4` |
| I | `session-i-security-governance-2026-11-16` | `0d071bf1ee7cc71912398c6ae57e4496e08f44ab` | 161 | Global Forget inventory `9100061fa986fb6676656169de3fcf9fc1c72664`; PermissionEpoch confirmation `bae6a24fe3a374bc816993979a8fa9af52517dea` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `830a559bd2f4ec72608f5a51e1a0b43779f2b989` | 122 | Producer/Dependency/Visibility `2ab899ee37a18ae6c8f2f64dbb82ad6499842060`; topology ADR `bb544ba2f346bdc130d524bd5c7310d86f367988`; Restore high-water `4f656163aeba532a441eaed1d293a48e2363cb4a` |

**Freshness limitation:** 上表证明本轮读取到这些分支 HEAD 与指定 Blob；不证明每份 Owner 文档内部引用的其他 Owner Blob 都是最新，也不替代对全部 9 个 Owner 完整文件包的逐行审查。Issue #43 G1 仍只能判为 PARTIAL。

## 3. H 树完整性事故：恢复核验

### 3.1 事故链

- 事故前最后审查 HEAD：`0d36324457e39bd50ad56ae902d477c4ea765b61`。
- 破坏性提交：`0277a8b9ee63be850acc0b8b1b08625524aaa33b`，其父提交正是事故前 HEAD。
- 破坏性提交统计：160 additions / 92,969 deletions；compare 显示 205 个文件 removed、3 个 workflow rename；递归树只有 5 个文件（A 报告记录为 7 个 entries，含目录节点）。
- H 恢复提交：`1ca07ed575be1fb2a690e3c2e110a89880ea6454`，明确提交信息为 “Restore complete branch tree and retain Phase 3.8.23 owner decisions”。
- 当前 H HEAD：`6608cde89d959257db612d8ff8080f631333f3f3`。

### 3.2 恢复证据

直接比较事故前 HEAD `0d363244...` 与当前 H HEAD `6608cde...`：
- ahead 7 commits / behind 0；
- 8 files added；
- 0 files removed；
- 0 files modified；
- 0 files renamed。

因此当前 H 树完整性恢复不是仅凭 Owner 声明，而是通过 Git compare 证明：原事故前文件树保留，后续新增 8 个文件。当前递归树有 216 个 Blob 文件。

### 3.3 H CI 精确范围

- H Applied Delivery Evidence Conformance run `44130722532`：SUCCESS；精确测试提交 `4e65a2ee0c6ac1c52a36f5d830ec7685dc4967e6`；H 报告列明 11 项测试通过。
- H Recovery Cutoff Conformance run `44130905292`：SUCCESS；精确 HEAD 为当前 H `6608cde...`。
- H Provider Outcome Conformance run `44129938964`：SUCCESS；精确提交 `1ca07ed...`。
- H Applied 1.0.0 workflow run 对应的测试提交 `4e65a2...` 是当前 H HEAD 的祖先；其后到 `6608cde...` 的最终提交记录双语 CI 结果。不能把 Applied run 的 SHA 错写成当前 HEAD。

### 3.4 当前 H 仍未完成的事情

H Phase 3.8.24 将 Applied Delivery Evidence 1.0.0 明确标为 **TEST/CONFORMANCE CANDIDATE**，不是生产密码学或持久化 replay 服务：
- 本地 canonicalizer 是测试用 sorted-key JSON，不是生产 JCS/profile；
- 签名、key status、profile registration、C final boundary、G binding、capability epoch 与 durable observation 均通过注入 callback；生产 callback/service 未实现；
- SDK、跨语言向量、Runtime Adapter 接入、持久化观察账本、生产信任根/密钥状态和 crash/restore 验证未完成；
- H Phase 3.8.23 的历史结论是身份语义 ACCEPT WITH EXCEPTIONS、wire mapping NOT FROZEN。Phase 3.8.24 增加候选实现，不自动把旧决议提升为 Owner 接受。

## 4. C 树完整性事故：恢复核验

### 4.1 事故链

- 事故前 C HEAD：`71047cdb51139ca4080ac67f451e38a48698859d`。
- 破坏性提交：`a5dff993e5c2928a28deb777c41023cfe923366f`，父提交为事故前 HEAD。
- 破坏性提交统计：144 additions / 21,673 deletions；compare 显示 133 files removed、2 added、1 renamed；递归树仅 3 个文件。
- C 恢复提交：`88992da30331121b81cf2773acab11d921daf281`，提交信息为 “Restore complete branch tree and retain Phase 3.8.23 owner decisions”。

### 4.2 恢复证据

直接比较事故前 C HEAD `71047c...` 与当前 C HEAD `88992d...`：
- ahead 2 commits / behind 0；
- 2 files added；
- 0 files removed；
- 0 files modified；
- 0 files renamed。

当前 C 递归树有 136 个 Blob 文件。C Phase 3.8.23 双语身份决议和 CSubmitOutcome 1.0.1 Schema 均存在。

### 4.3 C CI 与触发器缺陷

- C Provider Outcome Conformance run `44129914790`：SUCCESS；精确测试提交是当前 C HEAD `88992da...`。
- 当前 C workflow Blob `a1f0b8f884f0f294fb3ec96da7c4f11e294e5142` 的 push.paths 仅包含 CSubmitOutcome 1.0.0 Schema，没有包含 1.0.1 Schema。
- C PR #94 只增加 `07-agent-integration/schemas/c-submit-outcome-1.0.1.schema.json` 到 workflow paths，变更范围准确且没有改 Schema 语义。
- PR #94 仍为 Draft；本轮未将其视为已合并，也未声称该新增触发路径已通过独立 push 触发测试。C 现有 workflow 对 1.0.1 schema-only commit 的触发可靠性仍待该 PR 验证。

## 5. Applied Delivery Evidence 1.0.0 跨 Owner 接受矩阵

### 5.1 当前可确认

| 责任方 | 精确决议/证据 | 当前状态 |
|---|---|---|
| G | Phase 3.8.22 Applied persistence contract，EN/中文 Blobs 如上 | G-owned normative design draft；implementation NOT VERIFIED；新 H 1.0.0 wire mapping 尚需精确 consumer review |
| H | Phase 3.8.23 identity review Blob `be308261...`；Phase 3.8.24 candidate report Blob `f193113f...` | H identity semantics ACCEPT WITH EXCEPTIONS；1.0.0 candidate schema/validator CI PASS；不等于 G/C/I acceptance |
| C | Phase 3.8.23 C/G identity review Blob `4860c627...` | 仅接受 G 3.8.22 中 C-owned identity semantics；明确未接受 H wire mapping |
| I | PermissionEpoch formal confirmation Blob `bae6a24...`；I 3.8 Commit Authorization proposal Blob `54bab048...` | PermissionEpoch 技术基线已确认；Applied 1.0.0 signer/profile/key registration、crypto profile、canonicalization 与生产 trust 仍未形成完整接受 |
| D | Forget Fence / Publication Gate Blob `4da0b61...` | D operation semantics DECIDED；D/E interface schema、Storage realization、cross-owner conformance OPEN |
| Storage | Option A topology ADR Blob `bb544ba...`；atomic producer/dependency/visibility review Blob `2ab899...` | L1 logical topology selected；D adoption、L3 adversarial proof、L4 physical realization/conformance仍 OPEN |

### 5.2 不能越过的边界

- H Applied Delivery Evidence 1.0.0 是独立消息族，不得扩展或污染 Unified 1.2.15 Gateway Attestation 的 P0 allowlist。
- H Gateway ingress replay、H Adapter observation replay、G Applied uniqueness 是三个不同幂等域。
- C 的 ProviderAttempt/OutcomeRecord 身份与 H DeliveryBinding/Evidence/Observation 身份不可互换。
- G 是唯一 Applied 决策权威；H Validator 的 VALID 或 C 的 HANDOFF_ACCEPTED 都不能单独生成 Full Applied。
- I PermissionEpoch、D ForgetFenceGeneration、Storage cursor、G ContextVersion、H CapabilityEpoch 是不同命名空间；禁止数值比较、转换或互相代替。
- Applied 1.0.0 validator 的注入回调未知必须保持 UNKNOWN；本地测试用 canonicalizer 不能被当作生产密码学配置。

### 5.3 当前阻断项

1. G 对 H Applied 1.0.0 schema/validator 的 exact-version consumer review 尚未在 G 当前 HEAD 找到。
2. C 对 H Applied 1.0.0 schema/validator 的 exact-version review 尚未找到；C Phase 3.8.23 只接受 G 的 C-owned identity tuple。
3. I 的生产 issuer/key/profile/canonicalization/trust registration 与 anti-rollback 仍开放。
4. H durable observation ledger、生产 Adapter integration、SDK/跨语言 vectors、生产 crypto 未实现。
5. G Applied persistence implementation、同一事务的 D/I/COC/Storage final currentness validation 与 restore behavior 未物理验证。
6. Storage JF-10 同 GID terminal proof 与 D/I/Storage visibility ordering 仍需真实拓扑和 crash campaign。

**因此：H Applied Delivery Evidence 1.0.0 = candidate implementation + bounded CI PASS；Global Applied = NOT FROZEN / NOT PROVEN。**

## 6. Forget P0：Owner 现行合同的状态重述

本轮读取的 Owner 文件支持下列边界：
- D `forget-fence-operation-and-publication-gate.md`：D operation semantics DECIDED；D/E interface schema、Storage/Consistency realization、cross-owner conformance OPEN。D 要求 ProducerWork registration 与 Fence installation 在同一线性化排序域；最终 visibility commit 必须在同一域重验 Fence、Dependency Registration 与 I authorization。
- E `forget-fence-and-derived-registration.md`：E enforcement contract 仍 CANDIDATE；所有 derivative 在 durable D dependency registration、当前 PermissionEpoch/Fence 和最终 Publication Gate 成功前必须 private/non-queryable。
- I `global-forget-target-inventory-and-completion-evidence.md`：Global inventory/completion 仍 CANDIDATE；D/E/F/G/H/Storage conformance OPEN。I PermissionEpoch 技术确认是 normative baseline，但外部治理 profile approval 仍 BLOCKED。
- I `phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md`：仍是 I-role proposal；exact Owner approval、crypto profile、conformance OPEN。
- Storage `phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md`：提供候选原子实现设计；不等于物理拓扑部署证明。Storage L1 Option A ADR 已选，不代表 L3/L4。
- Storage Restore high-water contract与 reference model 仍需结合真实数据库备份、PITR、failover、rejoin、restore 的物理证据。

因此 ABR-INTEGRATION-001 对 Forget 的 P0 / NOT READY 判断维持不变，但 P0 需要更精确地表述为“逻辑 Owner 合同部分已存在；跨 Owner 原子组合、精确接口采纳、物理实现和故障证明仍未闭合”，不能简单说所有原子顺序都没有合同。

## 7. Issue #43 Gate 更新建议

| Gate | 本轮影响 | 建议状态 |
|---|---|---|
| G1 exact current pins | B/C/D/E/F/G/H/I/Storage HEAD 与核心 Blob 已刷新；完整文件级源账本/所有引用 freshness 未完成 | PARTIAL |
| G2 Owner authority/consumer acceptance | H/C 恢复不等于 Applied 1.0.0 C/G/I 接受；B ADR blocked | BLOCKED |
| G3 end-to-end state/causal model | Forget 逻辑合同已读；尚未对所有 Owner 做全序列与交叉 race/crash 证明 | BLOCKED |
| G4 P0/P1 proof | H/C tree restored; JF-10/Forget/Applied/Restore P0/P1 仍开放 | BLOCKED |
| G5 technology feasibility | Storage L1 Option A 已选；L3/L4 与 JF-10 物理证据不足 | BLOCKED |
| G6 bilingual parity | 本轮未做所有 Owner 双语逐条语义 parity | PARTIAL |
| G7 A integration disposition | 两份集成报告已提交研究 Draft PR；Owner 决议仍须各自授权方确认 | PARTIAL |
| G8 freeze recommendation | 当前仍不具备架构冻结条件 | NOT READY |

## 8. 下一步执行顺序

1. H：发布恢复后精确 current-head manifest，明确恢复提交的意图、恢复树与新加 8 个文件；将 Applied 1.0.0 candidate 独立列为非生产。
2. C：完成 PR #94 的 1.0.1 workflow path review，并证明 schema-only push 能触发 conformance；同时针对 H Applied 1.0.0 作 exact-version consumer review。
3. G：对 H Applied 1.0.0 Schema/Validator/P0 projection/identity/replay tuple 做逐字段 exact review；不得仅引用 H 3.8.23 的旧候选映射。
4. I/H：明确生产 signer/profile/key-status/canonicalization/anti-rollback authority、版本、向量与未知状态规则。
5. D/E/Storage/I：将 D operation semantics、E producer/derived registration、Storage atomic visibility、I CommitAuthorization sequencer 映射成一个同 GID/同 publication operation 的可验证顺序；分别证明两种竞争顺序与每个 durable boundary 前后 crash。
6. A：完成所有 Owner 文件的 source-pin freshness 与 bilingual parity，再更新 Issue #43 G1–G8；不把本轮树恢复或 CI 成功误判为 Gate 通过。

## 9. 最终判定

- H/C branch tree integrity: **RECOVERED AT CURRENT OWNER HEADS; incident retained; independent Owner intent/acknowledgment still required where applicable.**
- H Applied Delivery Evidence 1.0.0: **CANDIDATE / BOUNDED CI PASS / NOT PRODUCTION READY.**
- CSubmitOutcome 1.0.1: **CURRENT C HEAD CI PASS; schema-only workflow trigger fix remains PR #94 pending.**
- Global Applied: **NOT FROZEN / NOT PROVEN.**
- Forget/Producer/Derived Publication/Storage/JF-10: **P0 remains open; some logical Owner semantics are decided, but cross-owner and physical closure are not proven.**
- Issue #43: **G1 PARTIAL; G2–G5 BLOCKED; G6 PARTIAL; G7 PARTIAL; G8 NOT READY.**

本报告只记录集成复核，不替代 H/C/G/I/D/E/Storage Owner 决议，不授权实现、合并、Gate release、部署或生产激活。
