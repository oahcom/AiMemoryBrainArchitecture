# D Forget Normative Index — Phase 3.9 Proposal
# D Forget 规范索引 — Phase 3.9 提案

**Status / 状态:** PROPOSAL — NOT A NORMATIVE FREEZE / 提案 — 非规范冻结  
**Owner / 责任方:** D — Memory Brain / Forget Authority  
**Baseline branch / 基线分支:** `session-d-memory-brain-2026-11-16`  
**Baseline commit / 基线提交:** `194c4c8d64972547cdbcf3fe64bd806c4d1d6a2f`  
**Purpose / 目的:** Establish an auditable precedence and evidence map for D Forget contracts, amendments and delegated reviews. / 为 D Forget 契约、修订和委派审查建立可审计的优先级与证据映射。

> This index classifies the exact artifacts read at the stated baseline. It does not retroactively upgrade proposals or delegated role decisions into independent Owner approval, implementation acceptance or production freeze. A later commit must refresh this index before it is treated as current.
>
> 本索引对指定基线中读取的精确制品进行分类。它不会追溯性地把提案或委派角色决议升级为独立 Owner 批准、实现验收或生产冻结。后续提交必须刷新本索引，才能视为当前版本。

---

## 1. Precedence rules / 优先级规则

When D Forget artifacts conflict, apply these rules in order:

D Forget 制品发生冲突时，按以下规则处理：

1. **Owner authority boundary:** D controls canonical Memory lifecycle, ForgetOperation, ForgetFence, producer/dependency ledger, D barrier and D clearance. I controls authorization, PermissionEpoch/revocation, global target inventory, retention/legal hold, external copies, exceptions and Global Forget completion. Storage controls its durable serialization and visibility outcome. H transports/consumes typed evidence and cannot mint D/I facts.
2. **Exact accepted successor:** an explicitly accepted exact-version amendment supersedes only the clauses it names. It does not silently replace an entire earlier contract.
3. **Explicit supersession:** only an artifact that names the superseded exact file/Blob/clauses and has the authority to supersede them can do so.
4. **Supplemental review:** an exact review or addendum supplements the referenced controlling contract only within its stated scope and disposition.
5. **Proposal / candidate:** proposals, candidates, conditional decisions and delegated role reviews do not override a controlling contract until required Owner approvals are recorded.
6. **Implementation evidence:** implementation, tests and CI evidence prove only the exact code/build/test scope they actually exercised. They do not silently change semantic authority.
7. **Unknown conflict:** if exact precedence cannot be established, fail closed and hold the affected Gate. Do not infer authority from filename chronology or the highest phase number.

1. **Owner 权威边界：** D 控制规范 Memory 生命周期、ForgetOperation、ForgetFence、Producer/Dependency Ledger、D Barrier 和 D Clearance。I 控制授权、PermissionEpoch/撤权、全局目标 Inventory、Retention/Legal Hold、外部副本、例外和 Global Forget 完成。Storage 控制自身持久化排序和可见性结果。H 只传输/消费类型化证据，不得制造 D/I 事实。
2. **精确接受的后继版本：** 明确接受的精确版本修订仅替代其明确列出的条款，不得暗中替换整个旧契约。
3. **明确废止：** 只有明确指出被替代的精确文件/Blob/条款且具备对应权威的制品，才可废止旧条款。
4. **补充审查：** 精确审查或 Addendum 仅在其声明的范围和处置内补充所引用的控制性契约。
5. **提案/候选：** 提案、候选、有条件决议和委派角色审查，在必需 Owner 批准被记录前不得覆盖控制性契约。
6. **实现证据：** 实现、测试和 CI 仅证明其实际执行的精确代码/构建/测试范围，不会暗中改变语义权威。
7. **冲突未知：** 无法确定精确优先级时，必须 fail closed 并保持受影响 Gate，不得根据文件名时间顺序或最高 Phase 编号推断权威。

---

## 2. Exact artifact register / 精确制品登记表

All Blob SHAs below were read from the D source branch at the baseline commit. Status is limited to the artifact's own declared decision/provenance.

以下所有 Blob SHA 均从基线 Commit 的 D 源分支读取。状态仅限于制品自身声明的决议/来源。

| Artifact / 制品 | Exact Blob SHA | Classification / 分类 | Precedence / 优先级 |
|---|---|---|---|
| `forget-fence-and-completion-contract.md` | `1f0391bc49d007c44ec74165bd33d37412cc7990` | D canonical Forget contract; D semantics decided, cross-module/global policy open. / D 规范 Forget 契约；D 语义已决定，跨模块/全局策略开放。 | **D base semantic contract**; remains controlling subject to exact accepted amendments. / D 基础语义契约；受精确接受修订约束。 |
| `memory-lifecycle-manager.md` | `8b972035b449e1eab546aedc9cc5b30581600c65` | Lifecycle/Operation domain contract; its own header says some thresholds/transitions OPEN. / Lifecycle/Operation 域契约；文件头明确部分阈值/迁移仍 OPEN。 | **D lifecycle base**; read jointly with Forget Fence contract. / D 生命周期基础规范；须与 Fence 契约共同阅读。 |
| `forget-fence-operation-and-publication-gate.md` | `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5` | D operation/publication gate contract. / D Operation/Publication Gate 契约。 | **D operation/publication base**; no claim of implementation freeze. / D Operation/Publication 基础规范；不代表实现冻结。 |
| `phase-3.6-joint-forget-linearization-decision.md` | `1b6a312ecffd3947bbb4df59f902242482c98a40` | Joint architecture decision recorded; implementation explicitly not verified; role delegation provenance. / 联合架构决议已记录；实现明确未验证；委派角色来源。 | **Architecture decision supplement** for its enumerated semantics; not implementation acceptance or independent Owner approval. / 对列明语义构成架构决议补充；非实现验收或独立 Owner 批准。 |
| `phase-3.6.6-d-forget-semantic-authority-addendum.md` | `a384ffb4fff7de9b35ba6b3011d2779ad529573d` | D semantic proposal; explicitly says supersedes none and implementation/conformance OPEN. / D 语义提案；明确不废止任何文件，实施/符合性开放。 | **Supplemental proposal**, not a superseding normative decision. / 补充提案，非替代性规范决议。 |
| `phase-3.6.7-d-owner-local-gate-admission-release-amendment.md` | `84f6875ce382fb37f35b01140c19a482fcfa9fab` | Owner-branch semantic amendment candidate; independent D review required; not implemented/verified. / Owner 分支语义修订候选；需独立 D 复审；未实现/验证。 | **Candidate amendment**; not normative freeze. / 候选修订；非规范冻结。 |
| `phase-3.6.7-d-exact-version-owner-decision.md` | `3603aff5881dd8a375f22aad67b90ade312bbfad` | Exact-version role decision: ACCEPT WITH ENUMERATED AMENDMENTS; no semantic freeze until amendments incorporated/re-reviewed; delegated role provenance. / 精确版本角色决议：接受但列有修订；修订纳入并复审前不冻结；委派角色来源。 | **Conditional exact-version decision** for Blob `84f6875...`; does not supersede base contracts wholesale. / 对 Blob `84f6875...` 的有条件精确版本决议；不整体替代基础契约。 |
| `phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md` | `4c01713bc8793a8926ef18b625b72d132572173d` | D semantic boundary proposal; callable schema and implementation OPEN. / D 语义边界提案；可调用 Schema 和实现开放。 | **Supplemental proposal**; §8 replaces earlier wording only inside this artifact. / 补充提案；§8 仅在本文件内部替代早期措辞。 |
| `phase-3.8-d-publication-participant-and-terminal-contract.md` | `17e53890dd6cce9bea9eacc1be2e64b0ef55ac78` | D-role proposal; exact Owner approval, callable API and conformance OPEN. / D 角色提案；精确 Owner 批准、Callable API 和符合性开放。 | **Supplemental proposal** for publication participant semantics; not frozen. / Publication Participant 语义补充提案；未冻结。 |
| `phase-3.8.2-d-recovery-join-and-visibility-exact-review.md` | `6f39475784458d34b347d8566824fa22b308b477` | Delegated D-role review ACCEPT WITH AMENDMENTS; implementation/conformance not verified. / 委派 D 角色审查：接受但需修订；实现/符合性未验证。 | **Conditional review supplement**; does not prove D ledger completeness. / 有条件审查补充；不证明 D Ledger 完整性。 |
| `phase-3.8.3-d-gate-release-currentness-exact-review.md` | `7d45e663b471b7d82a0af8ca5b2e1f14c88f2315` | ACCEPT WITH CONDITIONS; semantics aligned, Storage topology/cross-owner proof/conformance OPEN. / 有条件接受；语义对齐，Storage 拓扑/跨 Owner 证明/符合性开放。 | **Conditional semantic supplement**; test vectors specified, not run. / 有条件语义补充；测试向量已规格化但未运行。 |
| `phase-3.8.8-d-review-storage-serialization-anchor.md` | `cb1e71730c6fd1fe5eed5c643d2fd59eceba008a` | ACCEPT as L1/L2 D/Storage ordering substrate; D row schema, dependency pagination, late discovery, failover and independent D approval OPEN. / 接受为 L1/L2 D/Storage 排序基础；D Row Schema、依赖分页、迟发现、Failover 和独立 D 批准开放。 | **L1/L2 substrate acceptance only**; not D semantic release or Forget completion. / 仅接受 L1/L2 基础设施；非 D 语义 Release 或 Forget 完成。 |
| `phase-3.8.9-d-review-h-forget-clearance-verifier-seam.md` | `53613f383d064d25ac9f34a00e457f86730f16bf` | ACCEPT H verifier seam as fail-closed interface only; D lineage/release proof OPEN. / 仅接受 H Verifier Fail-Closed 接口；D Lineage/Release 证明开放。 | **Consumer interface acceptance only**; no full D clearance. / 仅消费接口接受；非完整 D Clearance。 |
| `phase-3.8.9-d-exact-review-h-authority-join-mapping-1.2.14.md` | `40fee15d7e42d68da231ea161896f85df2921669` | Accept L1/L2 D-clearance carrier candidate; L3 lineage/currentness/production release OPEN; delegated D-role review. / 接受 L1/L2 D Clearance 载体候选；L3 Lineage/Currentness/Production Release 开放；委派 D 角色审查。 | **L1/L2 candidate only**; not full release proof or independent human D signature. / 仅 L1/L2 候选；非完整 Release Proof 或独立人类 D 签名。 |
| `phase-3.9-d-forget-terminal-semantics-and-linearization-closure-proposal.md` | `9c02b5680317f0092788ad0da66d621338b1c54c` | New proposal in PR #66; D-001..003 closure proposal. / PR #66 新提案；D-001..003 闭合提案。 | **Proposal only**; becomes successor only after exact D/Storage/I acceptance and independent review. / 仅提案；须 D/Storage/I 精确接受并经独立审查后才能成为后继。 |
| `tests/test_phase_3_9_forget_reference_model.py` | `b712f15bdb3770a3075070f8f3fce573c70defcf` | 19-case logical reference-model suite; locally executed in ChatGPT Python runtime, 19/19 PASS; no CI run and no production conformance. / 19 项逻辑 Reference Model 测试；在 ChatGPT Python 运行环境本地执行，19/19 PASS；无 CI 运行且非生产符合性。 | **Bounded semantic test evidence only.** / 仅有限语义测试证据。 |

---

## 3. Controlling interpretation / 当前控制性解释

Until the required exact-version approvals are recorded, use the following conservative interpretation:

在必需精确版本批准被记录前，采用以下保守解释：

1. D base contracts define D's semantic authority, target/lineage scope, producer registration, monotonic Fence and canonical suppression proof.
2. Phase 3.6.6 clarifies three outcomes and a D terminal state machine, but its header says it is a proposal and supersedes nothing.
3. Phase 3.6.7's exact-version decision is ACCEPT WITH ENUMERATED AMENDMENTS, not a freeze; its reviewed amendment still requires independent D review and conformance.
4. Phase 3.7/3.8 refine producer and publication participant semantics but remain proposals with callable schema/implementation or exact Owner approval open.
5. Phase 3.8.8 accepts the physical ordering substrate only. It explicitly leaves D row schema, complete dependency pagination, late-discovery fault campaign, database failover and independent human D approval open.
6. Phase 3.8.9 accepts H's D-clearance verifier seam only. It explicitly leaves D lineage completeness, barrier terminality and production release CAS open.
7. No D artifact in this register proves implementation PASS, Global Forget completion or physical erasure.

1. D 基础契约定义 D 的语义权威、目标/Lineage 范围、Producer 注册、单调 Fence 和规范抑制证明。
2. Phase 3.6.6 澄清三种结果和 D 终态机，但其文件头表明它是提案且不废止任何文件。
3. Phase 3.6.7 精确版本决议是 ACCEPT WITH ENUMERATED AMENDMENTS，不是冻结；被审修订仍需独立 D 复审和符合性证据。
4. Phase 3.7/3.8 细化 Producer 和 Publication Participant 语义，但仍是提案，可调用 Schema/实现或精确 Owner 批准仍开放。
5. Phase 3.8.8 仅接受物理排序基础；明确保留 D Row Schema、完整依赖分页、迟发现故障战役、数据库 Failover 和独立人类 D 批准为 OPEN。
6. Phase 3.8.9 仅接受 H 的 D-Clearance Verifier 接口；明确保留 D Lineage 完整性、Barrier 终态和生产 Release CAS 为 OPEN。
7. 本登记表中没有任何 D 制品证明实现 PASS、Global Forget 完成或物理擦除。

---

## 4. Open decision/evidence ledger / 未决决策与证据台账

| ID | Required closure / 必需闭合 | Owner(s) | Current state / 当前状态 |
|---|---|---|---|
| D-NI-01 | Approve one terminal vocabulary and state/field mapping. / 批准唯一终态词汇及状态/字段映射。 | D + I | OPEN — PR #66 proposal. |
| D-NI-02 | Approve immediate read suppression vs barrier-drain ordering. / 批准立即读抑制与 Barrier Drain 排序语义。 | D + Storage | OPEN — PR #66 proposal. |
| D-NI-03 | Approve exact I authorization currentness for Forgotten LifecycleEvent. / 批准 Forgotten LifecycleEvent 的 I 授权当前性。 | I + D + Storage | OPEN — PR #68 proposal. |
| D-NI-04 | Publish exact bilateral D/I acceptance against one Blob. / 针对同一 Blob 发布精确 D/I 双边接受。 | D + I | OPEN. |
| D-NI-05 | Complete D row schema, dependency pagination and late-discovery/failover evidence. / 完成 D Row Schema、依赖分页及迟发现/Failover 证据。 | D + Storage | OPEN. |
| D-NI-06 | Prove D Barrier terminality and final Release CAS with executable tests. / 用可执行测试证明 D Barrier 终态与最终 Release CAS。 | D + H + Storage | OPEN. |
| D-NI-07 | Execute D R3 and D/I cross-owner test matrix on identified commits. / 在明确 Commit 上执行 D R3 和 D/I 跨 Owner 测试矩阵。 | D + I + Storage + H | NOT RUN / NOT EVIDENCED. |
| D-NI-08 | Obtain independent non-implementing integration review. / 取得不参与实现的独立集成审查。 | A/governance-appointed reviewer | PENDING. |
| D-NI-09 | Add D/I/Storage logical reference tests, then separately execute production-boundary and fault-injection tests. / 增加 D/I/Storage 逻辑 Reference 测试，并单独执行生产边界与故障注入测试。 | D + I + Storage | 19 D logical tests PASS in ChatGPT Python runtime; CI/production conformance NOT RUN. / ChatGPT Python 运行环境 19 项 D 逻辑测试 PASS；CI/生产符合性未运行。 |

---

## 5. Refresh and closure rules / 刷新与闭合规则

- Refresh this index whenever a listed source file changes, a new amendment is accepted, a proposal is superseded, or a new test result is attached.
- Every row must carry full 40-character Blob SHA, branch/commit identity, declared status, decision authority and evidence boundary.
- Do not infer "latest" from Phase numbering. The latest file can still be a proposal; a lower-numbered exact accepted amendment can remain controlling.
- A delegated role simulation must be labelled as such. It cannot be upgraded to independent human Owner approval.
- D-001..D-007 remain open until their individual closure evidence is linked; PR creation alone does not close a finding.

- 每当列出的源文件变化、新修订被接受、提案被替代或新测试结果附加时，必须刷新本索引。
- 每一行必须记录完整 40 位 Blob SHA、分支/提交身份、声明状态、决策权威和证据边界。
- 不得根据 Phase 编号推断“最新”。最新文件仍可能是提案；较低编号的精确接受修订仍可能具有控制效力。
- 委派角色模拟必须明确标注，不得升级为独立人类 Owner 批准。
- D-001..D-007 必须分别关联关闭证据后才能关闭；创建 PR 本身不能关闭发现。

---

## 6. Non-claims / 不作出的声明

This index does not claim a normative freeze, D Owner independent signature, Storage production topology, full lineage completeness, R3 test execution, global Forget completion, physical erasure, production activation, or merge authorization.

本索引不声称规范冻结、D Owner 独立签名、Storage 生产拓扑、完整 Lineage、R3 测试执行、Global Forget 完成、物理擦除、生产激活或合并授权。
