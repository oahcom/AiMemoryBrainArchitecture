# AID-2026-001 — Owner D R3 Findings Resolution U-010 v1
# AID-2026-001 — Owner D R3 Finding 整改裁决 U-010 v1

- Work Item: AID-2026-001
- Role: Owner D — Canonical Memory lifecycle / Forget domain semantics
- Dispatch: relay-010; human Owner authorized continuous progression to convergence on 2026-11-18 22:08 +08:00.
- Dispatch source: current ChatGPT user instruction relay-010, received 2026-11-18 22:15 +08:00; platform conversation ID is not exposed to this executing session and is therefore not fabricated.
- Role prompt: CHATGPT-OWNER-D-001 v2.0; source `14-ai-development/prompts/owners/D/owner-session-v2.md`, main@6b5db2918cffc2281deb22fd9858a37dbaeec726, Blob `7005788694b4f89513c62a5d58adcfa74b6c14ec`; source status PROPOSED (not represented as ADOPTED).
- Process contracts loaded: AI-EXEC-001 v1.0 ADOPTED Blob `d9fbdca4542ded8977c9092e6b8276cc4fdbed6a`; AI-EXEC-002 v1.0 ADOPTED Blob `c1d1e5bffe0a92af701e59c7f2627350b1d9fddf`.
- Source baseline: main@6b5db2918cffc2281deb22fd9858a37dbaeec726.
- Working branch baseline: `remediation/aid-2026-001-forget-contract-closure-2026-11-18` @ `5a5ebcce34b7d26936678a8ccc5a730c2acba383`.
- Risk / class: ARCH / R3.
- Status: D-SIDE CANDIDATE — NOT NORMATIVE; D/I same-SHA approval, Storage approval, independent review and R3 evidence remain pending.
- Tests: NOT RUN by this session. This is a domain-contract decision proposal and documentation alignment, not implementation or runtime evidence.

> This artifact defines the D-side domain trigger and typed lifecycle meaning only. It does not author I's authorization receipt, PermissionEpoch, revocation ordering, retention/legal-hold policy, cross-system target policy, governance evidence acceptance, or exceptions. It does not approve Storage's persistence implementation. The joined D/I contract remains PROPOSED until both Owners approve the same exact content SHA.

---

## 1. Decision summary / 决议摘要

**D-side decision: `Forgotten` is entered at the successful durable `SuppressionCommitted` linearization point, not after D-domain cleanup completion and not after I governance completion.**

I's authorization decision is a mandatory precondition to that commit. The authorization decision's authenticity, applicability, currentness, revocation race semantics and policy meaning are I-owned and must be supplied by I. They are not the domain trigger and are not defined by this D proposal.

Storage must separately approve and prove that the lifecycle event, fence/tombstone, operation transition, idempotency identity and publication/outbox evidence share the required durable atomic serialization/visibility boundary. D's semantic decision is not Storage implementation approval.

**D 侧裁决：只有在 `SuppressionCommitted` 成功持久化并达到线性化点时，Memory 才进入 `Forgotten`；不得等到 D 领域清理完成，也不得等到 I 治理完成。**

I 的授权决策是该提交的强制前置条件。授权决策的真实性、适用性、当前性、撤权竞态语义和策略含义由 I 负责并提供。它们不是领域触发点，也不由本 D 提案定义。

Storage 必须另行批准并证明 Lifecycle Event、Fence/Tombstone、Operation 转换、幂等身份和 Publication/Outbox 证据共享所要求的持久化原子排序/可见性边界。D 的语义裁决不等于 Storage 实现批准。

## 2. D-R3-D-001 — authority boundary / 权责边界

### English

1. **Owner D** owns canonical Memory lifecycle vocabulary, legal lifecycle transitions, ForgetOperation domain semantics, ForgetFence meaning and monotonicity, the D-owned suppression predicate, and D-domain completion predicate.
2. **Memory Lifecycle Manager (MCM)** is a D-domain executor/coordinator. It validates D transition invariants, persists/reads canonical domain events through the approved Storage contract, coordinates D-owned dependency/producer work, and reports D-domain evidence. It does not own or invent identity trust, authorization, delegation, revocation, PermissionEpoch, privacy/retention/legal-hold policy, cross-system target policy, governance evidence acceptance, or policy exceptions.
3. **Owner I** owns authenticated-principal trust, authorization/delegation/revocation, PermissionEpoch/currentness, privacy/retention/legal-hold policy, global required-target policy, governance evidence acceptance/compliance assessment and policy-exception authority. I may deny/defer a commit under I policy; I may not redefine D's canonical Memory state or D-domain completion predicate.
4. **Storage** owns and must evidence its durable serialization, atomic commit, crash recovery and visibility guarantees. D specifies the semantic tuple that must be atomic but cannot approve Storage's implementation or claim durability evidence.
5. **Each executor** owns only its local action, capability boundary and local evidence. Its ACK cannot establish another executor's success or physical erasure beyond its proven scope.
6. **Audit is split by responsibility:** D emits canonical domain events and immutable evidence references; I defines governance integrity, provenance, access, retention and acceptance requirements. “Audit” is not one undifferentiated authority.

This boundary does not allow D to authorize itself, waive I policy or declare cross-system governance compliance. It does not allow I to rewrite D lifecycle truth.

### 中文

1. **Owner D** 拥有规范 Memory 生命周期词汇、合法生命周期转换、ForgetOperation 领域语义、ForgetFence 含义与单调性、D 所有的抑制判定条件及 D 领域完成判定条件。
2. **Memory Lifecycle Manager（MCM）** 是 D 领域执行器/协调器。它校验 D 转换不变量，依据已批准的 Storage 契约持久化/读取规范领域事件，协调 D 所有的依赖/Producer 工作并报告 D 领域证据。它不拥有或自行制定身份信任、授权、Delegation、Revocation、PermissionEpoch、隐私/Retention/Legal Hold 策略、跨系统目标策略、治理证据接受规则或策略例外。
3. **Owner I** 拥有已认证 Principal 信任、授权/Delegation/Revocation、PermissionEpoch/当前性、隐私/Retention/Legal Hold 策略、全局必需目标策略、治理证据接受/合规评估及策略例外授权。I 可以依据 I 策略拒绝/延期提交，但不得重定义 D 的规范 Memory 状态或 D 领域完成判定条件。
4. **Storage** 拥有并必须证明自身持久化排序、原子提交、崩溃恢复和可见性保证。D 规定必须原子提交的语义元组，但不能批准 Storage 实现或声称已有持久性证据。
5. **每个执行方** 只拥有自己的本地动作、能力边界和本地证据。其 ACK 不能证明其他执行方成功，也不能证明超出其已证明范围的物理擦除。
6. **Audit 按职责拆分：** D 产生规范领域事件和不可变证据引用；I 定义治理完整性、来源、访问、保留和接受要求。“Audit”不是一个不区分边界的单一权责。

该边界不允许 D 自行授权、豁免 I 策略或声明跨系统治理合规；也不允许 I 改写 D 的生命周期事实。

## 3. D-R3-D-002 — canonical Forgotten trigger / Forgotten 规范触发点

### 3.1 Normative domain meaning proposed by D

The canonical D-domain event is **`SuppressionCommitted`**. At the successful authoritative durable serialization point, the canonical Memory identity transitions atomically to `Forgotten`.

The semantic commit tuple MUST bind, under one Storage-approved atomic durable boundary:

- canonical Memory identity and expected lifecycle/version;
- terminal `MemoryLifecycle=Forgotten` and its immutable LifecycleEvent;
- monotonically increasing applicable ForgetFence generation / tombstone;
- ForgetOperation identity, idempotency identity and phase `SuppressionCommitted`;
- the outbox/publication record needed to make committed suppression observable;
- typed immutable references/digests for the I authorization decision and D suppression proof.

This list specifies the required domain semantics, not a claim that the current Storage implementation provides this atomicity.

### 3.1 D 提议的规范领域含义

D 侧规范事件为 **`SuppressionCommitted`**。在权威持久化排序点成功提交时，规范 Memory 身份原子转为 `Forgotten`。

在 Storage 批准的单一持久化原子边界内，语义提交元组 MUST 绑定：

- 规范 Memory 身份及预期 Lifecycle/Version；
- 终态 `MemoryLifecycle=Forgotten` 及其不可变 LifecycleEvent；
- 单调递增的适用 ForgetFence Generation / Tombstone；
- ForgetOperation 身份、幂等身份及 `SuppressionCommitted` 阶段；
- 使已提交抑制可被观察的 Outbox/Publication 记录；
- I 授权决策与 D 抑制证明的不可变类型化引用/摘要。

此清单规定必需的领域语义，不代表当前 Storage 实现已经提供该原子性。

### 3.2 I authorization is a precondition, not the trigger

Before `SuppressionCommitted`, D MUST consume an I-owned authorization decision that is authenticated, applicable to the exact actor/action/Memory/Scope/purpose, current under I's policy and not revoked according to I's authoritative ordering rule at the commit serialization point. Denied, stale, expired, revoked, scope-mismatched or UNKNOWN/IN_DOUBT authorization MUST fail closed: no `SuppressionCommitted`, no `Forgotten` transition.

D does not define the receipt envelope, trusted issuer, delegation chain, PermissionEpoch comparison, revocation winner algorithm, replay protection or policy decision. Those are I-owned and remain OPEN pending U-011. D MUST NOT invent a fallback or treat absence of an I decision as approval.

The I authorization precondition is evaluated at the commit boundary. It is not a requirement that I first declare all required targets cleaned, all governance evidence complete, or global policy compliance. Such a requirement would conflate authorization with post-commit governance assessment and recreate I-U009-002.

### 3.2 I 授权是前置条件，不是触发点

在 `SuppressionCommitted` 之前，D MUST 消费 I 所有的授权决策。该决策必须经过认证，适用于精确的 Actor/Action/Memory/Scope/Purpose，并且依据 I 的策略，在提交排序点仍然有效且未按 I 的权威排序规则撤销。授权被拒绝、过期、失效、已撤销、Scope 不匹配或结果为 UNKNOWN/IN_DOUBT 时，MUST fail closed：不得发生 `SuppressionCommitted`，也不得转为 `Forgotten`。

D 不定义回执信封、可信签发者、Delegation 链、PermissionEpoch 比较、撤权胜者算法、重放保护或策略决策。这些归 I 所有，并留待 U-011 决定。D MUST NOT 发明替代协议，也不得把缺少 I 决策视为批准。

I 授权前置条件在提交边界进行判定。它不要求 I 先声明所有必需目标均已清理、所有治理证据均已完成或全局策略已合规。此类要求会混淆授权与提交后的治理评估，并重新造成 I-U009-002 所指出的冲突。

### 3.3 Before / at / after transition rules

| Point | MemoryLifecycle | ForgetOperation | Rule |
|---|---|---|---|
| Request / authorization pending | unchanged | Requested / AuthorizationPending | No suppression; ordinary lifecycle rules continue. |
| Authorization valid, before commit | unchanged | Authorized | Authorization alone does not make Memory Forgotten. |
| Successful `SuppressionCommitted` | atomically becomes `Forgotten` | SuppressionCommitted | Canonical terminalization and fence linearization point. |
| After commit: inventory / cleanup / D completion pending | remains `Forgotten` | InventorySealed / CleanupInProgress / DomainCompletionEvaluated | Continue/reconcile; no rollback or ordinary access. |
| Failure / unknown after commit | remains `Forgotten` | Blocked / Failed / resumable | Failure never removes or lowers the fence and never resurrects identity. |
| Cancel before commit | unchanged | Cancelled if otherwise permitted by I policy | No Forgotten transition occurred. |
| Cancel after commit | remains `Forgotten` | cancellation rejected; attempt may pause | No rollback, restore or fence removal. |

### 3.3 转换前、中、后的规则

| 时点 | MemoryLifecycle | ForgetOperation | 规则 |
|---|---|---|---|
| Request / 授权待处理 | 不变 | Requested / AuthorizationPending | 尚未抑制；继续遵循普通生命周期规则。 |
| 授权有效但尚未提交 | 不变 | Authorized | 仅有授权不会使 Memory 成为 Forgotten。 |
| 成功执行 `SuppressionCommitted` | 原子转为 `Forgotten` | SuppressionCommitted | 规范终态化与 Fence 线性化点。 |
| 提交后：Inventory / Cleanup / D 完成仍待处理 | 保持 `Forgotten` | InventorySealed / CleanupInProgress / DomainCompletionEvaluated | 继续/对账；不得回滚或恢复普通访问。 |
| 提交后失败/未知 | 保持 `Forgotten` | Blocked / Failed / 可恢复 | 失败绝不移除/降低 Fence，也绝不复活身份。 |
| 提交前取消 | 不变 | 在 I 策略允许时可为 Cancelled | 未发生 Forgotten 转换。 |
| 提交后取消 | 保持 `Forgotten` | 拒绝取消；可暂停尝试 | 不得回滚、Restore 或移除 Fence。 |

### 3.4 Meaning and non-meaning of Forgotten

`Forgotten` means the canonical Memory identity is terminal and ordinary read, retrieval, derivation, activation, delivery and restore paths MUST reject or quarantine that identity under the current fence.

It does NOT mean: D-domain completion; all cross-system targets completed; I governance compliant; backup expiry; remote recipient compliance; cleanup completion; or physical erasure. Those are distinct results/evidence and MUST NOT be collapsed into the Memory lifecycle state.

After the commit, later revocation, policy change, target failure, unknown result or cleanup interruption may block/defer remaining work or I governance assessment. None can reverse the committed domain transition. If I policy requires a pre-commit deny/defer, the commit does not occur; if a post-commit obligation arises, it is handled as a separate policy/operation outcome without resurrection.

### 3.4 Forgotten 的含义与非含义

`Forgotten` 表示规范 Memory 身份已经终结；普通读取、检索、派生、激活、交付和 Restore 路径 MUST 依据当前 Fence 拒绝或隔离该身份。

它不表示：D 领域完成；所有跨系统目标均已完成；I 治理合规；备份到期；远端接收方已履行删除；清理完成；或物理擦除。上述均为独立结果/证据，MUST NOT 合并进 Memory 生命周期状态。

提交后发生的撤权、策略变化、目标失败、结果未知或清理中断，可以阻塞/延期剩余工作或 I 治理评估，但均不能逆转已提交的领域转换。如果 I 策略要求提交前拒绝/延期，则不得发生提交；如果提交后产生义务，则作为独立策略/Operation 结果处理，不得复活 Memory。

## 4. D-R3-D-004 — typed state separation / 类型化状态分离

These dimensions MUST remain separately typed and separately attributable:

1. **MemoryLifecycle (D):** Candidate, Consolidated, Active, Superseded, Archived, Forgotten. Forgotten is terminal for the same identity.
2. **ForgetOperationPhase (D):** Requested, AuthorizationPending, Authorized, SuppressionCommitted, InventorySealed, CleanupInProgress, DomainCompletionEvaluated, Completed, Blocked, Failed, Cancelled. Cancelled is only valid before SuppressionCommitted.
3. **PerTargetResult (each executor):** NotStarted, InProgress, Succeeded, Failed, Unknown, Unsupported, NotEvidenced. A policy exception is not an executor success result; its approval/reference is I-owned and separately typed.
4. **DDomainCompletion (D):** NotEvaluated, Incomplete, Blocked, Completed. Completed means only that D's declared canonical producer/barrier/target predicate is met.
5. **GovernanceAssessment (I):** I defines its own vocabulary and policy semantics (e.g. Pending, Compliant, NonCompliant, Deferred, CompliantWithException). D stores only an opaque typed decision/reference and does not calculate or approve it.
6. **PhysicalErasureEvidence (target/storage owner):** target-specific evidence status; it cannot be inferred from Forgotten, a tombstone, suppression ACK or governance status.

A public projection MUST expose these dimensions separately. In particular, `SuppressionCommitted`, `Forgotten`, `DDomainCompletion.Completed`, `GovernanceAssessment.Compliant` and physical-erasure confirmation MUST NOT be collapsed into “deleted everywhere” or a single “Forget complete” boolean.

以上维度 MUST 保持类型独立、责任归属独立：

1. **MemoryLifecycle（D）：** Candidate、Consolidated、Active、Superseded、Archived、Forgotten。同一身份的 Forgotten 为终态。
2. **ForgetOperationPhase（D）：** Requested、AuthorizationPending、Authorized、SuppressionCommitted、InventorySealed、CleanupInProgress、DomainCompletionEvaluated、Completed、Blocked、Failed、Cancelled。Cancelled 只允许在 SuppressionCommitted 之前。
3. **PerTargetResult（各执行方）：** NotStarted、InProgress、Succeeded、Failed、Unknown、Unsupported、NotEvidenced。策略例外不是执行方成功结果；其批准/引用由 I 所有并单独类型化。
4. **DDomainCompletion（D）：** NotEvaluated、Incomplete、Blocked、Completed。Completed 仅表示 D 声明的规范 Producer/Barrier/Target 判定条件满足。
5. **GovernanceAssessment（I）：** I 定义自己的词汇和策略语义（例如 Pending、Compliant、NonCompliant、Deferred、CompliantWithException）。D 只保存不透明的类型化决策/引用，不计算或批准该结果。
6. **PhysicalErasureEvidence（目标/存储 Owner）：** 目标级证据状态；不得从 Forgotten、Tombstone、Suppression ACK 或治理状态推断。

公开投影 MUST 分别呈现这些维度。特别是 `SuppressionCommitted`、`Forgotten`、`DDomainCompletion.Completed`、`GovernanceAssessment.Compliant` 和物理擦除确认 MUST NOT 合并为“全域删除”或单一“Forget 完成”布尔值。

## 5. Findings disposition / Finding 处置

| Finding | Severity | D-side disposition | Remaining gate / 回流去向 |
|---|---|---|---|
| D-R3-D-001 | P1 | D/I authority boundary clarified as §2; MCM no longer claims I policy/authorization ownership | Owner I confirms I-owned boundary rows; Issue #41 |
| D-R3-D-002 | P1 | D chooses `SuppressionCommitted` as the sole D-domain trigger; I authorization is a precondition, not a later governance-completion trigger | Owner I defines authorization/currentness/revocation semantics in U-011; Storage approves atomic commit boundary; Issue #41 |
| D-R3-D-004 | P2 | lifecycle, operation, target result, D completion, I governance and physical-erasure evidence separated as §4 | executor/storage conformance and bilingual independent review; Issue #41 |
| I-U009-002 | P1 | D-side semantic conflict resolved by this candidate; no claim that I-side prerequisites are approved | U-011 I authorization precondition contract + D/I same-SHA approval; Issue #41 |

## 6. Approval and evidence gates / 批准与证据门禁

- This U-010 artifact and the aligned D-owned lifecycle documents remain **CANDIDATE / PROPOSED**, not ADOPTED and not normative.
- Owner D's domain decision is recorded here; it is not a substitute for a separately recorded Owner D approval if the project's approval mechanism requires one.
- Owner I must author/approve the I-owned authorization receipt, PermissionEpoch/currentness, revocation ordering, retention/legal-hold, target-policy and governance-evidence rules in U-011.
- Owner D and Owner I must approve the **same exact joined bilingual content SHA**. Approval of different commits, blobs, excerpts or summaries is not same-SHA approval.
- Storage durable serialization/commit/visibility approval remains PENDING.
- E/F/G/H/C and other executor acknowledgements remain bounded to their own contracts.
- Independent integration review remains PENDING.
- Production/runtime R3 tests remain NOT RUN / NOT EVIDENCED. Existing in-memory reference-model tests are model-only and do not prove Storage atomicity, concurrency, production conformance or R3 acceptance.
- D-R3-D-003 remains a bilateral gate and is not closed by U-010.
- Overall AID-2026-001 remains BLOCKED_PENDING_R3_EVIDENCE. No production activation, acceptance or merge-to-main is authorized by this artifact.

- 本 U-010 制品及已对齐的 D 所有生命周期文件仍为 **CANDIDATE / PROPOSED**，不是 ADOPTED，也不具规范效力。
- 本文记录 D 的领域决策，不替代项目审批机制可能要求的单独 Owner D 正式批准。
- Owner I 必须在 U-011 中编写/批准 I 所有的授权回执、PermissionEpoch/当前性、撤权排序、Retention/Legal Hold、目标策略和治理证据规则。
- Owner D 与 Owner I 必须批准**同一份精确的联合双语内容 SHA**。批准不同 Commit、Blob、摘录或摘要不构成同 SHA 双边批准。
- Storage 持久化排序/提交/可见性批准仍为 PENDING。
- E/F/G/H/C 和其他执行方的确认仍限于各自职责契约。
- 独立集成审查仍为 PENDING。
- 生产/运行时 R3 测试仍为 NOT RUN / NOT EVIDENCED。既有内存 Reference Model 测试仅为模型级证据，不能证明 Storage 原子性、并发、生产符合性或 R3 验收。
- D-R3-D-003 仍是双边门禁，U-010 不予关闭。
- AID-2026-001 整体仍为 BLOCKED_PENDING_R3_EVIDENCE。本制品不授权生产激活、验收或合并至 main。

## 7. Bilingual change manifest / 双语变更清单

D-owned source counterparts updated in the same branch change set:
- `02-domain-model/lifecycle-model.md`
- `docs/zh-CN/02-domain-model/lifecycle-model.md`
- `docs/en/03-memory-brain/memory-lifecycle-manager.md`
- `docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md`

The joined D/I proposal remains proposal-only and must be re-frozen after I's U-011 changes before any same-SHA bilateral approval. GOV-DOC-001 parity, identifiers, status and reciprocal links must be independently checked against the final frozen joined revision.

同一分支变更集更新的 D 所有源文件双语对应件：
- `02-domain-model/lifecycle-model.md`
- `docs/zh-CN/02-domain-model/lifecycle-model.md`
- `docs/en/03-memory-brain/memory-lifecycle-manager.md`
- `docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md`

D/I 联合提案仍仅为提案；必须在 I 完成 U-011 修改后重新冻结版本，才能进行同 SHA 双边批准。必须依据最终冻结的联合版本独立检查 GOV-DOC-001 语义、标识、状态和双向链接一致性。

---

## 8. Explicit non-claims / 明确不作出的声明

No I authorization receipt protocol was approved here. No PermissionEpoch or revocation race winner rule was invented. No retention/legal-hold exception was approved. No global target inventory or governance assessment was performed. No Storage implementation or atomicity was approved. No production tests were run. No finding is marked fully closed solely by this author-side candidate.

本次未批准任何 I 授权回执协议；未发明 PermissionEpoch 或撤权竞态胜者规则；未批准 Retention/Legal Hold 例外；未执行全局目标清单或治理评估；未批准 Storage 实现或原子性；未运行生产测试。不得仅凭本作者侧候选提案将任何 Finding 标记为完全关闭。
