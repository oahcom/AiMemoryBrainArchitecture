# AID-2026-001 — Owner D R3 Findings Resolution Proposal U-008 v1
# AID-2026-001 — Owner D R3 Finding 整改提案 U-008 v1

- Work Item: AID-2026-001
- Role: Owner D — Canonical Memory lifecycle / Forget domain semantics
- Prompt role reference: CHATGPT-OWNER-D-001 v2.0, source file blob 7005788694b4f89513c62a5d58adcfa74b6c14ec at main commit 6b5db2918cffc2281deb22fd9858a37dbaeec726
- Dispatch: relay-008, human Owner authorization “continue”; this fact package is not itself a frozen reusable prompt.
- Proposal status: CANDIDATE — NOT NORMATIVE; not an Owner D human approval, not an Owner I approval, not Storage approval, and not a joined D/I contract.
- Branch-only carrier: remediation/aid-2026-001-forget-contract-closure-2026-11-18
- Source baseline: main@6b5db2918cffc2281deb22fd9858a37dbaeec726
- Branch baseline before this proposal: e95d7cf7dcadd48475a6fceda52036ee01c6b48d
- Risk / class: ARCH / R3
- Tests: NOT RUN — this is a semantic proposal; no runtime or reference-model conformance is claimed.

> This artifact records an Owner-D-side proposed resolution for D-R3-D-001, D-R3-D-002 and D-R3-D-004. It intentionally does not amend the normative lifecycle documents or the joined contract. It preserves the unresolved D/I and Storage approval gates. The proposal is suitable for review and exact-version decision, not execution as an approved contract.

---

## 1. Live source pins and observed conflicts

All main source pins below were read from the same main snapshot, 6b5db2918cffc2281deb22fd9858a37dbaeec726.

| Source | Blob SHA | Relevant observation |
|---|---|---|
| 02-domain-model/lifecycle-model.md | 42b20fbdf81b574eb271f3db02503b615f414ab4 | English authority sentence assigns policy/execution/authorization/audit to Lifecycle Manager; appended lines 154–162 propose a different D/I split and Option-A-like suppression semantics. |
| docs/zh-CN/02-domain-model/lifecycle-model.md | 7809825a878745be4bb126c7345ea564622cbbeb | Chinese authority sentence has the same overbroad Lifecycle Manager assignment; it does not contain the English appended proposal block, so the two language files are not semantically/status aligned. |
| docs/en/03-memory-brain/memory-lifecycle-manager.md | f8562761483316bff1256775f06ff9446902072b | Lines 45, 64 and 169 say Forgotten follows required in-scope target/policy completion and an I-supplied governance criterion. |
| docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md | 6710e51561da3a7d10b7937fbdd461f95d9869de | Chinese counterpart carries the same later-trigger semantics. |
| 14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v1.md | 96882570d44f6a3c6d60a30b1edb0e405bde5efc | Proposal §3 maps SuppressionCommitted to atomic Memory→Forgotten; explicitly PROPOSED pending D/I approval. |
| 14-ai-development/work-items/AID-2026-001/owner-d-i-forget-authority-matrix.md | 6c6b3715f95f0aa9c29ad2fd42d15d8b2bae77b2 | Explicitly PROPOSED; assigns D domain semantics and I authorization/governance/evidence acceptance. |
| Phase 3.9 D proposal (PR #66 source branch) | 9c02b5680317f0092788ad0da66d621338b1c54c | Proposal requires D suppression proof plus a current I COMMIT_WON receipt for Forgotten CAS; not a main-branch approval or implementation proof. |

### Finding disposition

- D-R3-D-001 (P1): the Lifecycle Manager's stated ownership of policy/authorization/audit overlaps I-owned security/governance authority and conflicts with the proposed D/I matrix. D-owned lifecycle execution must be distinguished from I-owned authorization and policy.
- D-R3-D-002 (P1): the main joined proposal's fence-linearization trigger conflicts with the D Lifecycle Manager's later D-domain/policy-completion trigger. The exact trigger and its I authorization precondition must be decided explicitly; the two meanings cannot coexist under one Forgotten definition.
- D-R3-D-004 (P2): the joined proposal contains the beginnings of a multi-dimensional mapping, but the D Lifecycle Manager and bilingual Lifecycle Model do not consistently define the same types, mapping, per-target outcome and public projection.

## 2. D-R3-D-001 — proposed authority boundary

**Candidate rule: domain truth and policy authority are separate.**

1. Domain Model defines canonical lifecycle vocabulary, legal transitions and domain invariants.
2. Owner D owns canonical Memory lifecycle semantics, ForgetOperation domain semantics, the D-owned suppression/fence meaning, and the D-domain completion predicate.
3. Memory Lifecycle Manager is a D-domain executor/coordinator. It validates D transition guards, appends/reads canonical lifecycle events, operates the D-owned workflow and reports D-domain evidence. It does not own or invent authorization policy, revocation policy, retention/legal-hold policy, or cross-system evidence-acceptance policy.
4. Owner I owns authenticated-principal trust, authorization/delegation/revocation, PermissionEpoch/currentness, privacy/retention/legal-hold policy, cross-system inventory policy, exception authority, and governance evidence-acceptance/compliance assessment.
5. Storage owns the durable serialization/commit/visibility guarantee of its persistence boundary. D specifies the semantic atomicity requirement but cannot claim Storage implementation approval or physical durability evidence.
6. D emits domain events and immutable evidence references. I defines integrity, provenance, retention and acceptance requirements for governance evidence. “Audit” must not be a single undifferentiated ownership bucket.
7. Executors own only their local action and local evidence. They cannot authorize Forget, redefine Memory lifecycle, or claim another Owner's completion.

This boundary does not give I authority to rewrite D's canonical lifecycle state or D-domain completion predicate. It also does not allow D to authorize itself, waive I policy, or declare cross-system governance compliance.

## 3. D-R3-D-002 — recommended Forgotten trigger (D-side candidate)

**Recommendation: Option A — fence-linearization trigger, with I authorization as a precondition. CANDIDATE only; exact I receipt and Storage commit semantics remain subject to their Owners.**

The proposed canonical event is SuppressionCommitted. At the authoritative durable commit, the same atomic unit must bind:

- the canonical Memory identity and expected version;
- terminal Memory lifecycle state Forgotten and its immutable LifecycleEvent;
- the monotonically increasing applicable ForgetFence generation / tombstone;
- the ForgetOperation phase and idempotency identity;
- the outbox/publication record needed to make the committed suppression observable;
- typed references/digests for the current I authorization decision and D suppression proof.

The I authorization decision must be authenticated, applicable to the exact actor/action/target/scope/purpose, current under I's policy and PermissionEpoch rules, and not revoked at the commit serialization point. D consumes and validates the I-owned decision; D does not define I's trust, revocation or policy semantics. Storage must separately confirm that the required fields share one durable serialization/visibility boundary.

**Meaning of Forgotten:** the canonical Memory identity is terminal and ordinary read, derivation, activation, delivery and restore paths must deny or quarantine that identity under the current fence. Forgotten does not mean D-domain cleanup is complete, all cross-system targets are complete, governance is compliant, backups have expired, or physical erasure is evidenced.

**After SuppressionCommitted:** cancellation/rollback cannot remove or lower the fence, and the Memory cannot return to a non-Forgotten state. A later authorization revocation, target failure, unknown outcome or cleanup interruption may block/defer the operation and governance assessment; it must not resurrect the Memory or remove suppression.

**Before SuppressionCommitted:** denied, revoked, stale, scope-mismatched or UNKNOWN/IN_DOUBT authorization prevents the commit. The operation remains pending/blocked or is rejected under the I-owned decision. No Memory lifecycle transition to Forgotten is recorded.

**D-domain completion is later and separate:** D evaluates its own canonical target/producer/barrier predicate and records its own operation result. I separately evaluates cross-system governance compliance. Neither result retroactively defines when the canonical Memory identity became Forgotten.

Rationale for preferring A: the fence is the point at which canonical ordinary access and derivation become irrevocably suppressed. Keeping the Memory lifecycle non-terminal after that point would create a second “inaccessible but not Forgotten” state whose recovery/reactivation semantics are ambiguous. The separate D-domain and I-governance results preserve later completion work without weakening terminal suppression.

This recommendation does not adopt the exact COMMIT_WON / REVOCATION_WON / UNKNOWN receipt protocol from the Phase 3.9 proposal. Those are I-owned sequencer semantics and require Owner I's exact-version decision. It also does not assert that the proposed multi-record atomic commit is implemented; Storage must approve the exact commit boundary.

## 4. D-R3-D-004 — proposed typed state separation and mapping

These are separate aggregates/results. They must not be stored in one overloaded status field.

### 4.1 MemoryLifecycle (D-owned)

Candidate enum:

- Candidate
- Consolidated
- Active
- Superseded
- Archived
- Forgotten

There is no Memory lifecycle state named Forgetting. Forgotten is terminal for the same Memory identity.

### 4.2 ForgetOperationPhase (D-owned)

Candidate phase sequence:

Requested → AuthorizationPending → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → DomainCompletionEvaluated → Completed

Blocked / Failed are explicit non-success outcomes. Cancelled is permitted only before SuppressionCommitted. After SuppressionCommitted, a worker attempt may pause or fail, but the operation remains suppressed and resumable/reconcilable; it cannot become Cancelled in a way that implies rollback.

A phase is not a Memory lifecycle state. The phase records progress of the Forget workflow, not whether the canonical Memory identity remains accessible.

### 4.3 PerTargetResult (domain-specific; local result owned by each executor)

Candidate values:

- NotStarted
- InProgress
- Succeeded
- Failed
- Unknown
- Unsupported
- NotEvidenced
- ExceptionPending / ExceptionApproved (approval authority for a policy exception remains I)

Unknown, Unsupported, NotEvidenced, Failed and ExceptionPending are never success. Each target result is scoped to a typed target reference, action, attempt, evidence reference, observed fence generation and timestamp. A consumer cannot promote another executor's result to Succeeded.

### 4.4 DDomainCompletion (D-owned)

D evaluates only the D-owned canonical target/producer/barrier set and its evidence. Candidate result values: NotEvaluated, Incomplete, Blocked, Completed. Completed means only that D's explicit domain predicate is satisfied. It does not assert I governance compliance or physical erasure.

### 4.5 GovernanceAssessment (I-owned)

I owns the policy assessment and its result vocabulary, including any Compliant, NonCompliant, Deferred or CompliantWithException outcome. D stores/returns an opaque typed reference and does not calculate, approve or rewrite this result.

### 4.6 PublicResult (derived projection, not a new authority)

The public/API/UI projection must expose at least:
- request accepted/rejected;
- suppression committed/not committed;
- Memory lifecycle;
- ForgetOperation phase;
- D-domain completion;
- per-target results and unknowns;
- I governance assessment;
- physical-erasure evidence status.

It must not collapse SuppressionCommitted, Forgotten, DDomainCompletion.Completed, GovernanceAssessment.Compliant and PhysicalErasureConfirmed into one “deleted everywhere” or “Forget complete” claim.

### 4.7 Required lifecycle-to-operation mapping

| ForgetOperationPhase | MemoryLifecycle effect | Required interpretation |
|---|---|---|
| Requested / AuthorizationPending | No change | Request and authorization are not suppression. |
| Authorized | No change | I authorization alone does not make Memory Forgotten. |
| SuppressionCommitted | Atomically becomes Forgotten | The fence/tombstone/operation/outbox commit is the logical terminalization point. |
| InventorySealed / CleanupInProgress | Remains Forgotten | Target work continues; no rollback or ordinary access. |
| DomainCompletionEvaluated | Remains Forgotten | D evaluates only its own domain predicate. |
| Completed | Remains Forgotten | D-domain completion only; I governance and physical erasure remain separate. |
| Blocked / Failed after suppression | Remains Forgotten | Failure/unknown does not remove the fence; recovery is explicit. |
| Cancelled before suppression | Unchanged | No terminal lifecycle transition occurred. |
| Cancelled after suppression | Forbidden | Must not imply rollback or remove the fence. |

## 5. Minimum D/I/Storage decision and evidence gates

| Gate | Required decision/evidence | Accountable authority | Current status |
|---|---|---|---|
| D-R3-D-001 | Accept/amend the authority split in §2 against this exact proposal version | Owner D, with I concurrence on I-owned rows | CANDIDATE |
| D-R3-D-002 | Decide the D-side Forgotten trigger and exact D event/preconditions; I receipt semantics remain I-owned | Owner D + explicit Owner I approval of I-owned preconditions | CANDIDATE |
| D-R3-D-004 | Accept/amend the typed separation, mapping and D-domain completion semantics in §4 | Owner D; executor confirmation for local result semantics | CANDIDATE |
| Durable commit | Confirm atomic persistence, ordering, crash recovery and visibility behavior for the SuppressionCommitted tuple | Storage | PENDING |
| Joined contract | D and I approve the same exact bilingual content SHA; Storage approves its commit boundary | Owner D + Owner I + Storage | PENDING |
| Independent review | Fresh non-implementing review of exact frozen artifacts and diff | Independent reviewer | PENDING |
| R3 conformance | Reproducible race/fault/recovery/security tests on exact implementation/test commit | Relevant implementation owners | NOT RUN / NOT EVIDENCED |

## 6. Required regression scenarios (specifications only; NOT RUN)

- D001-T01: verify Lifecycle Manager cannot grant authorization, change I policy, waive retention/legal hold or declare cross-system compliance.
- D001-T02: verify I governance assessment cannot rewrite D MemoryLifecycle or DDomainCompletion.
- D002-T01: verify stale, denied, scope-mismatched or UNKNOWN I authorization prevents SuppressionCommitted.
- D002-T02: race authorization commit against revocation; prove the authoritative winner is deterministic and bound to the exact target/scope/policy/epoch tuple.
- D002-T03: after SuppressionCommitted, request cancellation, rollback, restore and replay; prove the fence remains effective and Memory remains Forgotten.
- D002-T04: inject crash at each persistence boundary; prove no partial state is misreported as committed and recovery does not expose the target.
- D004-T01: verify MemoryLifecycle and ForgetOperationPhase are distinct typed fields and never overwrite one another.
- D004-T02: verify Unknown / Unsupported / NotEvidenced / Failed per-target results cannot aggregate to success.
- D004-T03: verify Memory may remain Forgotten while cleanup and D-domain completion are incomplete.
- D004-T04: verify public status preserves D result, I assessment, per-target status and physical-erasure evidence separately.
- D004-T05: verify restore, cache rebuild, delayed publication and stale-worker replay cannot resurrect a Forgotten identity.

No test in this list has been executed by this session. Existing reference-model results remain model-only and are not evidence for production atomicity, concurrency, storage durability or R3 acceptance.

## 7. Explicit non-decisions and handoff

1. Owner I must decide the authenticated authorization receipt, PermissionEpoch/currentness, revocation ordering, policy/retention/legal-hold and governance evidence-acceptance semantics. This proposal does not author those semantics.
2. Storage must decide and evidence its durable serialization/commit/visibility boundary. D cannot approve Storage's implementation.
3. E/F/G/H/C and other execution owners must acknowledge only their own local enforcement and evidence boundaries.
4. D-R3-D-003 remains a bilateral D/I gate. This proposal does not close it.
5. The joined contract remains PROPOSED until D and I approve the same exact bilingual content SHA and Storage's relevant boundary is accepted.
6. A non-implementing Integration Reviewer and the required independent specialist reviews remain outstanding.
7. Overall AID-2026-001 remains REMEDIATION_IN_PROGRESS / BLOCKED for R3 acceptance. No production activation or acceptance is authorized by this artifact.

---

# 中文

## 1. 实时源文件与冲突

以下 main 源文件均来自同一快照：6b5db2918cffc2281deb22fd9858a37dbaeec726。

| 来源 | Blob SHA | 观察到的问题 |
|---|---|---|
| 02-domain-model/lifecycle-model.md | 42b20fbdf81b574eb271f3db02503b615f414ab4 | 英文权责句把策略/执行/授权/审计都归给 Lifecycle Manager；后附 154–162 行又提出不同的 D/I 分工和近似方案 A 的抑制语义。 |
| docs/zh-CN/02-domain-model/lifecycle-model.md | 7809825a878745be4bb126c7345ea564622cbbeb | 中文权责句有相同的 Lifecycle Manager 过宽授权问题；但缺少英文文件末尾新增的提案段落，中英文状态和语义未对齐。 |
| docs/en/03-memory-brain/memory-lifecycle-manager.md | f8562761483316bff1256775f06ff9446902072b | 第 45、64、169 行规定 Forgotten 要等必需目标/策略完成，并由 I 提供治理完成标准。 |
| docs/zh-CN/03-memory-brain/memory-lifecycle-manager.md | 6710e51561da3a7d10b7937fbdd461f95d9869de | 中文对应文件保留相同的延后触发语义。 |
| 14-ai-development/work-items/AID-2026-001/forget-lifecycle-joined-contract-proposal-v1.md | 96882570d44f6a3c6d60a30b1edb0e405bde5efc | 联合契约提案 §3 把 SuppressionCommitted 映射为 Memory 原子转为 Forgotten；状态仍为 PROPOSED，待 D/I 批准。 |
| 14-ai-development/work-items/AID-2026-001/owner-d-i-forget-authority-matrix.md | 6c6b3715f95f0aa9c29ad2fd42d15d8b2bae77b2 | 明确标为 PROPOSED；把领域语义归 D，把授权/治理/证据接受归 I。 |
| Phase 3.9 D 提案（PR #66 源分支） | 9c02b5680317f0092788ad0da66d621338b1c54c | 提案要求 D 抑制证明与当前 I COMMIT_WON 回执共同支持 Forgotten CAS；不是 main 分支批准或实现证明。 |

### Finding 处置

- D-R3-D-001（P1）：Lifecycle Manager 对策略/授权/审计的声明与 I 的安全治理职责重叠，并与 D/I 权责矩阵冲突。必须区分 D 生命周期执行与 I 授权/策略。
- D-R3-D-002（P1）：main 联合提案的 Fence 线性化触发点，与 D Lifecycle Manager 的延后 D 域/策略完成触发点冲突。必须明确唯一 Forgotten 语义及 I 授权前置条件。
- D-R3-D-004（P2）：联合提案已有多维映射雏形，但 D Lifecycle Manager 和双语 Lifecycle Model 尚未一致定义类型、映射、逐目标结果和公开投影。

## 2. D-R3-D-001 — 建议的权责边界

**候选规则：领域事实与治理策略分离。**

1. Domain Model 定义规范生命周期词汇、合法转换和领域不变量。
2. Owner D 拥有规范 Memory 生命周期语义、ForgetOperation 领域语义、D 侧抑制/Fence 含义及 D 领域完成判定条件。
3. Memory Lifecycle Manager 是 D 领域执行器/协调器，负责校验 D 转换前置条件、追加/读取规范生命周期事件、执行 D 所有的工作流并报告 D 领域证据。它不拥有或自行制定授权策略、撤权策略、Retention/Legal Hold 策略或跨系统证据接受策略。
4. Owner I 拥有已认证 Principal 信任、授权/Delegation/Revocation、PermissionEpoch/当前性、隐私/Retention/Legal Hold 策略、跨系统 Inventory 策略、例外授权以及治理证据接受/合规评估。
5. Storage 拥有自身持久化边界的持久排序/提交/可见性保证。D 可以规定语义原子性要求，但不能声称 Storage 已批准或已有物理持久性证据。
6. D 产生领域事件和不可变证据引用。I 定义治理证据的完整性、来源、保留和接受要求。“Audit”不得继续作为没有边界的单一职责桶。
7. 执行 Owner 只拥有本地动作和本地证据，不得授权 Forget、重定义 Memory 生命周期或宣称其他 Owner 已完成。

该边界不允许 I 重写 D 的规范生命周期状态或 D 领域完成判定；也不允许 D 自行授权、豁免 I 策略或宣布跨系统治理合规。

## 3. D-R3-D-002 — 建议的 Forgotten 触发点（D 侧候选）

**建议：方案 A — Fence 线性化触发，I 授权作为前置条件。当前仅为 CANDIDATE；I 回执及 Storage 提交语义仍由对应 Owner 决定。**

建议的规范事件为 SuppressionCommitted。在权威持久化提交点，同一原子提交单元必须绑定：

- 规范 Memory 身份及预期版本；
- 终态 Memory Lifecycle=Forgotten 及其不可变 LifecycleEvent；
- 单调递增的适用 ForgetFence Generation / Tombstone；
- ForgetOperation 阶段与幂等身份；
- 使已提交抑制可被观察的 Outbox/Publication 记录；
- 当前 I 授权决策与 D 抑制证明的类型化引用/摘要。

I 授权决策必须经过认证，适用于精确 Actor/Action/Target/Scope/Purpose，在 I 的策略和 PermissionEpoch 规则下仍然有效，并且在提交排序点尚未被撤销。D 消费并校验 I 所有的决策，但不定义 I 的信任、撤权或策略语义。Storage 必须另行确认这些字段共享一个持久化排序/可见性边界。

**Forgotten 的含义：** 规范 Memory 身份已终结；普通读取、派生、激活、交付和 Restore 路径必须依据当前 Fence 拒绝或隔离该身份。Forgotten 不表示 D 域清理完成、所有跨系统目标完成、治理合规、备份到期或物理擦除已有证据。

**SuppressionCommitted 之后：** Cancel/Rollback 不得移除或降低 Fence，Memory 也不得回到非 Forgotten 状态。之后发生授权撤销、目标失败、结果未知或清理中断时，可以阻塞/延期 Operation 和治理评估，但不得复活 Memory 或移除抑制。

**SuppressionCommitted 之前：** 授权被拒绝、撤销、过期、Scope 不匹配或结果为 UNKNOWN/IN_DOUBT 时，不得提交。Operation 保持 Pending/Blocked 或按 I 的决策被拒绝；不得记录 Forgotten 生命周期转换。

**D 领域完成发生在后续且独立：** D 评估自身规范目标/Producer/Barrier 判定条件并记录自己的 Operation 结果。I 独立评估跨系统治理合规。二者均不追溯定义规范 Memory 身份何时成为 Forgotten。

推荐方案 A 的理由：Fence 是规范普通访问和派生被不可逆抑制的时点。如果在此之后仍让 Memory 生命周期保持非终态，就会产生一个“不可访问但还不是 Forgotten”的第二状态，其恢复/重新激活语义模糊。把 D 域结果和 I 治理结果分开，可以保留后续完成工作，而不削弱终态抑制。

本建议不采纳 Phase 3.9 提案中精确的 COMMIT_WON / REVOCATION_WON / UNKNOWN 回执协议。这些属于 I 的排序器语义，必须由 Owner I 对精确版本作出决定。本建议也不声称上述多记录原子提交已经实现；Storage 必须批准精确提交边界。

## 4. D-R3-D-004 — 类型化状态分离与映射建议

这些是不同的聚合对象/结果，不得存储在一个过载的状态字段中。

### 4.1 MemoryLifecycle（D 所有）

候选枚举：

- Candidate
- Consolidated
- Active
- Superseded
- Archived
- Forgotten

不存在名为 Forgetting 的 Memory 生命周期状态。同一 Memory 身份的 Forgotten 为终态。

### 4.2 ForgetOperationPhase（D 所有）

候选阶段序列：

Requested → AuthorizationPending → Authorized → SuppressionCommitted → InventorySealed → CleanupInProgress → DomainCompletionEvaluated → Completed

Blocked / Failed 是明确的非成功结果。Cancelled 只允许发生在 SuppressionCommitted 之前。SuppressionCommitted 之后，Worker 尝试可以暂停或失败，但 Operation 必须保持抑制并可恢复/对账；不得进入暗示回滚的 Cancelled。

Phase 不是 Memory Lifecycle State。Phase 记录 Forget 工作流进度，不表示规范 Memory 身份是否仍可访问。

### 4.3 PerTargetResult（按领域划分；本地结果由各执行方拥有）

候选值：

- NotStarted
- InProgress
- Succeeded
- Failed
- Unknown
- Unsupported
- NotEvidenced
- ExceptionPending / ExceptionApproved（策略例外批准权仍归 I）

Unknown、Unsupported、NotEvidenced、Failed 和 ExceptionPending 永远不是成功。每个目标结果必须绑定类型化 Target Ref、Action、Attempt、Evidence Ref、观察到的 Fence Generation 和时间戳。消费者不得把其他执行方的结果提升为 Succeeded。

### 4.4 DDomainCompletion（D 所有）

D 只评估 D 所有的规范目标/Producer/Barrier 集合及其证据。候选结果值：NotEvaluated、Incomplete、Blocked、Completed。Completed 只表示 D 明确的领域判定条件已满足，不表示 I 治理合规或物理擦除。

### 4.5 GovernanceAssessment（I 所有）

I 拥有策略评估及其结果词汇，包括 Compliant、NonCompliant、Deferred 或 CompliantWithException 等结果。D 只保存/返回不透明类型化引用，不计算、批准或重写该结果。

### 4.6 PublicResult（派生投影，不是新的权威）

公开/API/UI 投影至少必须分别呈现：

- Request Accepted/Rejected；
- Suppression Committed/Not Committed；
- Memory Lifecycle；
- ForgetOperation Phase；
- D-domain Completion；
- Per-target Results 与 Unknown；
- I Governance Assessment；
- Physical-erasure Evidence Status。

不得把 SuppressionCommitted、Forgotten、DDomainCompletion.Completed、GovernanceAssessment.Compliant 和 PhysicalErasureConfirmed 合并为“已全域删除”或“Forget 已完成”。

### 4.7 Lifecycle 与 Operation 的必要映射

| ForgetOperationPhase | MemoryLifecycle 影响 | 必须保留的含义 |
|---|---|---|
| Requested / AuthorizationPending | 不改变 | 请求和授权不等于抑制。 |
| Authorized | 不改变 | I 授权本身不使 Memory 成为 Forgotten。 |
| SuppressionCommitted | 原子转为 Forgotten | Fence/Tombstone/Operation/Outbox 提交是逻辑终态化点。 |
| InventorySealed / CleanupInProgress | 保持 Forgotten | 目标工作继续；不得回滚或恢复普通访问。 |
| DomainCompletionEvaluated | 保持 Forgotten | D 只评估自己的领域判定条件。 |
| Completed | 保持 Forgotten | 仅代表 D 域完成；I 治理和物理擦除仍独立。 |
| SuppressionCommitted 后的 Blocked / Failed | 保持 Forgotten | 失败/未知不移除 Fence；恢复必须显式执行。 |
| SuppressionCommitted 前的 Cancelled | 不改变 | 未发生终态生命周期转换。 |
| SuppressionCommitted 后的 Cancelled | 禁止 | 不得暗示回滚或移除 Fence。 |

## 5. D/I/Storage 最低决议与证据门禁

| 门禁 | 必需决议/证据 | 责任权威 | 当前状态 |
|---|---|---|---|
| D-R3-D-001 | 对 §2 权责划分按本提案精确版本作出接受/修订 | Owner D；I 对 I 所有职责行会签 | CANDIDATE |
| D-R3-D-002 | 决定 D 侧 Forgotten 触发点及精确 D 事件/前置条件；I 回执语义仍归 I | Owner D + Owner I 对 I 所有前置条件明确批准 | CANDIDATE |
| D-R3-D-004 | 接受/修订 §4 类型分离、映射和 D 域完成语义 | Owner D；执行 Owner 确认本地结果语义 | CANDIDATE |
| 持久化提交 | 确认 SuppressionCommitted 元组的原子持久化、排序、崩溃恢复和可见性行为 | Storage | PENDING |
| 联合契约 | D/I 对同一精确双语内容 SHA 批准；Storage 批准其提交边界 | Owner D + Owner I + Storage | PENDING |
| 独立审查 | 对准确冻结工件和 Diff 进行新的非实现者审查 | 独立 Reviewer | PENDING |
| R3 符合性 | 在精确实现/测试 Commit 上执行可复现竞态/故障/恢复/安全测试 | 相关实现 Owner | NOT RUN / NOT EVIDENCED |

## 6. 必需回归场景（仅规格；NOT RUN）

- D001-T01：验证 Lifecycle Manager 不能授予授权、改变 I 策略、豁免 Retention/Legal Hold 或宣布跨系统合规。
- D001-T02：验证 I 治理评估不能重写 D MemoryLifecycle 或 DDomainCompletion。
- D002-T01：验证过期、拒绝、Scope 不匹配或 UNKNOWN 的 I 授权会阻止 SuppressionCommitted。
- D002-T02：让授权提交与撤权竞争；证明权威胜者确定且绑定精确 Target/Scope/Policy/Epoch 元组。
- D002-T03：在 SuppressionCommitted 后注入 Cancel、Rollback、Restore 和 Replay；证明 Fence 持续有效且 Memory 保持 Forgotten。
- D002-T04：在每个持久化边界注入 Crash；证明部分状态不会被误报为已提交，恢复后目标不会重新暴露。
- D004-T01：验证 MemoryLifecycle 和 ForgetOperationPhase 是独立类型字段，永不相互覆盖。
- D004-T02：验证 Unknown / Unsupported / NotEvidenced / Failed 的逐目标结果不能聚合为成功。
- D004-T03：验证 Memory 可在 Cleanup 和 D 域完成尚未完成时保持 Forgotten。
- D004-T04：验证公开状态分别保留 D 结果、I 评估、逐目标状态和物理擦除证据。
- D004-T05：验证 Restore、Cache Rebuild、延迟发布和陈旧 Worker Replay 不会复活 Forgotten 身份。

本会话没有执行上述任何测试。既有 Reference Model 结果仍仅为模型级证据，不证明生产原子性、并发、Storage 持久性或 R3 验收。

## 7. 明确未决事项与交接

1. Owner I 必须决定已认证授权回执、PermissionEpoch/当前性、撤权排序、Policy/Retention/Legal Hold 和治理证据接受语义。本提案不代写这些语义。
2. Storage 必须决定并提供其持久化排序/提交/可见性边界证据。D 不能批准 Storage 实现。
3. E/F/G/H/C 及其他执行 Owner 只确认各自本地强制执行与证据边界。
4. D-R3-D-003 仍是 D/I 双边门禁。本提案不关闭它。
5. 在 D/I 批准同一精确双语内容 SHA 且 Storage 相关边界获接受前，联合契约保持 PROPOSED。
6. 非实现者 Integration Reviewer 和必需的独立专业审查仍未完成。
7. AID-2026-001 整体仍为 REMEDIATION_IN_PROGRESS / R3 验收 BLOCKED。本制品不授权生产激活或验收。
