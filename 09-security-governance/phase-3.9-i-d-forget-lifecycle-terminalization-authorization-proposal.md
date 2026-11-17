# Phase 3.9-I — D/I Forget Lifecycle Terminalization Authorization Contract Proposal
# Phase 3.9-I — D/I Forget 生命周期终态化授权契约提案

**Status / 状态:** PROPOSAL — NOT NORMATIVE / 提案 — 尚非规范  
**Owner / 责任方:** I owns authorization and governance; D owns canonical LifecycleEvent and ForgetFence / I 拥有授权与治理；D 拥有规范 LifecycleEvent 与 ForgetFence  
**I baseline / I 基线:** `session-i-security-governance-2026-11-16` @ `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`  
**Companion proposal / 配套提案:** D Phase 3.9 proposal, PR #66, commit `c3c1ac7b802f96075de98af788ef969052f10e21`

> This proposal does not claim I Owner approval, external governance approval, D acceptance, implementation, or test execution. It must be accepted by D and I against this exact blob before becoming normative.
>
> 本提案不声称已取得 I Owner 批准、外部治理批准、D 接受、实现或测试执行。必须由 D 与 I 针对本文件精确 Blob 接受后，方可成为规范。

---

## 1. Problem statement / 问题定义

D owns the canonical Memory lifecycle and is the only authority that appends the `LifecycleEvent` changing a Memory to `Forgotten`. I owns the authorization, PermissionEpoch, revocation ordering, retention/legal-hold policy, global Forget completion criteria and physical-erasure governance.

D 拥有规范 Memory 生命周期，并且是唯一可以追加将 Memory 变更为 `Forgotten` 的 `LifecycleEvent` 的权威。I 拥有授权、PermissionEpoch、撤权排序、Retention/Legal Hold 策略、Global Forget 完成标准及物理擦除治理。

The current artifacts correctly separate these responsibilities, but they do not yet provide one exact bilateral protocol for the authorization/revocation race at D's irreversible lifecycle-terminalization commit. A historical I authorization decision or a cached ALLOW is not sufficient. Conversely, revoking the requester must not roll back an already committed D ForgetFence.

现有文档正确区分了双方职责，但尚未形成一套精确的双边协议，用于处理 D 不可逆生命周期终态化提交时的授权/撤权竞争。历史 I 授权决策或缓存 ALLOW 均不足。另一方面，撤销请求者权限也不得回滚已经提交的 D ForgetFence。

This proposal defines a dedicated, single-use I authorization participant for the exact D lifecycle-terminalization event. It is distinct from derivative-publication authorization and from I global Forget completion.

本提案为精确的 D 生命周期终态事件定义专用、单次消费的 I 授权 Participant。它与 Derivative Publication 授权以及 I Global Forget 完成相互独立。

---

## 2. Non-interchangeable authority and outcome vocabulary / 不可互换的权威与结果词汇

| Fact / 事实 | Authority / 权威 | Meaning / 含义 |
|---|---|---|
| `CanonicalSuppressionComplete` | D | D proves its canonical producer/derivative barrier and required canonical targets are suppressed. / D 证明其规范 Producer/Derivative Barrier 和必需规范目标已抑制。 |
| `Forgotten` LifecycleEvent | D | Canonical Memory identity is logically terminalized by an immutable D event. / 通过不可变 D 事件将规范 Memory 身份逻辑终态化。 |
| `GlobalForgetCompleted` | I | I's global target inventory/evidence evaluator confirms governance obligations are satisfied or covered by approved scoped exceptions. / I 的全局目标 Inventory/证据评估器确认治理义务已满足或由批准的范围化例外覆盖。 |
| `PhysicalErasureConfirmed` | Each responsible storage/copy authority under I policy | Physical erasure evidence for that authority's controlled copies. / 各责任方对其控制副本提供的物理擦除证据。 |

D's `Forgotten` event MUST NOT set I's global state to Completed, CompletedWithPolicyException, or any physical-erasure state. I MUST NOT manufacture or append D's canonical LifecycleEvent. A local D proof is an input to I's global evaluator, not a substitute for I's inventory seal or evidence vector.

D 的 `Forgotten` 事件不得将 I 全局状态设为 Completed、CompletedWithPolicyException 或任何物理擦除状态。I 不得制造或追加 D 的规范 LifecycleEvent。D 本地证明是 I 全局评估器的输入，不得替代 I Inventory Seal 或 Evidence Vector。

---

## 3. Proposed I authorization object / I 授权对象提案

Introduce a dedicated logical operation:

建议引入专用逻辑操作：

`ConsumeForgetTerminalizationAuthorization`

It is an I PolicyDomain sequencer operation. It is not a general-purpose authorization token, not a detached ALLOW snapshot and not a global completion receipt.

该操作由 I PolicyDomain Sequencer 执行。它不是通用授权 Token、Detached ALLOW Snapshot，也不是 Global Completion Receipt。

### 3.1 Immutable request binding / 不可变请求绑定

The request MUST bind all of the following:

请求必须绑定以下全部内容：

- exact `ForgetOperationId`;
- exact canonical `MemoryId`, expected `MemoryVersion` and target/lineage digest;
- exact `ScopeRef` and scope digest;
- D `ForgetFenceGeneration` and D `CanonicalSuppressionProofRef` plus proof digest;
- exact proposed `LifecycleEventDigest`, expected lifecycle sequence/version and terminal transition `to=Forgotten`;
- authenticated requester/continuity PrincipalRef, ActorRef, delegation and purpose;
- I `PolicyDomainRef`, policy version and I-local `PermissionEpoch`;
- issuer key ID/version/status and I-local revocation/sequencer position;
- unique nonce, request digest, timestamp and approved canonicalization/signature profile.

- 精确的 `ForgetOperationId`；
- 精确规范 `MemoryId`、预期 `MemoryVersion` 和目标/Lineage 摘要；
- 精确 `ScopeRef` 及 Scope 摘要；
- D `ForgetFenceGeneration`、D `CanonicalSuppressionProofRef` 及证明摘要；
- 精确拟提交的 `LifecycleEventDigest`、预期生命周期 Sequence/Version，以及 `to=Forgotten` 终态迁移；
- 经认证的请求者/连续性 PrincipalRef、ActorRef、Delegation 和 Purpose；
- I `PolicyDomainRef`、策略版本及 I 本地 `PermissionEpoch`；
- Issuer Key ID/Version/Status 与 I 本地 Revocation/Sequencer Position；
- 唯一 Nonce、请求摘要、时间戳和批准的 Canonicalization/Signature Profile。

The PermissionEpoch remains an opaque I-local value. It MUST NOT be numerically compared with D ForgetFenceGeneration, D LifecycleEvent sequence, Storage SerializationRevision or any other owner's cursor.

PermissionEpoch 始终是 I 本地不透明值。不得与 D ForgetFenceGeneration、D LifecycleEvent Sequence、Storage SerializationRevision 或其他 Owner 的 Cursor 进行数值比较。

### 3.2 Receipt and sequencer outcomes / Receipt 与 Sequencer 结果

I issues/consumes one `ForgetTerminalizationAuthorizationReceipt` with exactly one sequencer result:

I 签发/消费一个 `ForgetTerminalizationAuthorizationReceipt`，Sequencer 结果只能是以下之一：

- `COMMIT_WON`: this exact lifecycle-terminalization request won the I authorization/revocation ordering race. I persists an unresolved, single-use authorization participant bound to the tuple above.
- `REVOCATION_WON`: applicable revocation, policy change, scope change, hold or authorization invalidation linearized first; D MUST NOT commit the `Forgotten` event using this request.
- `UNKNOWN / IN_DOUBT`: ordering, currentness, issuer/key status, sequencer continuity or receipt outcome cannot be proven; D MUST NOT commit the `Forgotten` event.

- `COMMIT_WON`：该精确生命周期终态化请求赢得 I 授权/撤权排序竞争。I 持久化一个绑定上述元组、未解决且单次使用的授权 Participant。
- `REVOCATION_WON`：适用撤权、策略变更、Scope 变更、Hold 或授权失效先行线性化；D 不得使用该请求提交 `Forgotten` 事件。
- `UNKNOWN / IN_DOUBT`：无法证明排序、当前性、Issuer/Key Status、Sequencer 连续性或 Receipt 结果；D 不得提交 `Forgotten` 事件。

The caller cannot select the result. A `COMMIT_WON` receipt is bound only to the exact event digest and cannot authorize a different Memory, version, scope, operation, fence generation, proof digest or LifecycleEvent sequence.

调用方不得选择结果。`COMMIT_WON` Receipt 仅绑定精确事件摘要，不得授权其他 Memory、Version、Scope、Operation、Fence Generation、Proof Digest 或 LifecycleEvent Sequence。

---

## 4. Required cross-owner commit/closeout protocol / 必需的跨 Owner 提交与关闭协议

The proposed protocol has five steps:

建议协议包含五个步骤：

1. **D prepares the exact terminal event.** D verifies its active fence, current canonical suppression proof, Memory version, operation identity, scope and expected LifecycleEvent sequence. D computes the immutable LifecycleEvent digest but does not append it yet.
2. **I consumes authorization.** I verifies the full current authorization tuple and atomically orders the single-use request against applicable revocation/policy/hold changes in its PolicyDomain sequencer.
3. **D commits or refuses.** With `COMMIT_WON`, D attempts an atomic compare-and-set append of the exact LifecycleEvent using the exact receipt. D rechecks its own fence/proof/version/sequence currentness in its authoritative transaction. It cannot use the receipt for a modified event.
4. **I closes the authorization participant.** If D returns an authenticated exact `D_TERMINALIZED` outcome, I records the receipt as consumed/closed. If D returns an authoritative `D_NO_TERMINALIZATION` outcome, I closes without a Forgotten event. Missing/contradictory D outcome remains `UNKNOWN / IN_DOUBT`.
5. **Global Forget remains separate.** I's global evaluator consumes D's event/proof only as one typed component of the global evidence vector. It independently checks the I Target Inventory Seal, per-target evidence, exceptions, retention/backup/recipient requirements and all other mandatory components.

1. **D 准备精确终态事件。** D 验证活动 Fence、当前规范抑制证明、Memory Version、Operation 身份、Scope 和预期 LifecycleEvent Sequence。D 计算不可变 LifecycleEvent 摘要，但暂不追加。
2. **I 消费授权。** I 验证完整当前授权元组，并在 PolicyDomain Sequencer 中将单次请求与适用撤权/策略/Hold 变更原子排序。
3. **D 提交或拒绝。** 收到 `COMMIT_WON` 后，D 使用精确 Receipt 对精确 LifecycleEvent 执行原子 Compare-and-Set 追加。D 必须在自身权威事务中重新验证 Fence/Proof/Version/Sequence 当前性。Receipt 不得用于已修改事件。
4. **I 关闭授权 Participant。** 若 D 返回经认证的精确 `D_TERMINALIZED` 结果，I 将 Receipt 记录为已消费/关闭。若 D 返回权威 `D_NO_TERMINALIZATION`，I 关闭该 Participant，但不产生 Forgotten 事件。缺失/矛盾的 D 结果保持 `UNKNOWN / IN_DOUBT`。
5. **Global Forget 仍然独立。** I 全局评估器仅将 D 事件/证明作为全局 Evidence Vector 中的一个类型化组成部分。I 仍须独立检查 Target Inventory Seal、逐目标证据、例外、Retention/Backup/Recipient 要求及其他必需组件。

### 4.1 Revocation race semantics / 撤权竞争语义

| Ordering / 排序 | Required behavior / 必须行为 |
|---|---|
| Revocation/policy/hold change wins before I consumption / I 消费前撤权/策略/Hold 变更先行 | I returns `REVOCATION_WON`; D does not append `Forgotten`. The already committed D Fence remains active and the Forget operation remains resumable under an authorized continuity principal. / I 返回 `REVOCATION_WON`；D 不追加 `Forgotten`。已提交 D Fence 继续有效；Forget Operation 在有权连续性主体下保持可恢复。 |
| I consumption returns `COMMIT_WON` before later revocation / 后续撤权前 I 消费返回 `COMMIT_WON` | I holds the applicable later revocation transition pending the exact D terminalization/no-terminalization outcome. This is an ordering hold for one exact event, not a reusable grant. / I 将适用的后续撤权转换保持 Pending，等待精确 D 终态化/未终态化结果。这是针对单一精确事件的排序 Hold，不是可复用授权。 |
| D event commit fails after `COMMIT_WON` / `COMMIT_WON` 后 D 事件提交失败 | D must return a durable no-terminalization outcome or UNKNOWN. I closes only on authenticated no-terminalization proof; otherwise remains IN_DOUBT and does not infer success. / D 必须返回持久化未终态化结果或 UNKNOWN。I 仅在取得经认证的未终态化证明后关闭；否则保持 IN_DOUBT，不得推断成功。 |
| D proof/fence becomes stale before D CAS / D CAS 前 D Proof/Fence 过期 | D CAS fails. No Forgotten event. The Fence is not lowered. A new D proof/authorization cycle is required. / D CAS 失败，不产生 Forgotten 事件。Fence 不降低，必须重新取得 D Proof/Authorization。 |
| Sequencer/key/epoch state UNKNOWN / Sequencer/Key/Epoch 状态未知 | No `COMMIT_WON`; D fails closed. / 不得产生 `COMMIT_WON`；D fail closed。 |

### 4.2 No rollback of committed Forget Fence / 已提交 Forget Fence 不回滚

Revocation of the requester after Fence installation MUST NOT remove, lower, expire or weaken the Fence, cancel the operation, restore canonical visibility or erase already recorded target obligations. A currently authorized continuity principal may resume the operation, but cannot change its target/scope/digest without a new authorized operation and explicit lineage linkage.

Fence 安装后撤销请求者权限，不得移除、降低、使 Fence 过期或削弱 Fence，不得取消 Operation、恢复规范可见性或抹除已记录目标义务。当前有权的连续性主体可以恢复 Operation，但不得在没有新授权 Operation 和明确 Lineage 关联的情况下改变目标/Scope/摘要。

---

## 5. I Global Forget completion boundary / I Global Forget 完成边界

I global completion remains an I-only evaluation. At minimum it requires:

I 全局完成仍是 I 独占评估。至少需要：

- current, gap-free I ProducerDomainInventoryEpoch and valid TargetInventorySeal;
- D's exact current CanonicalSuppressionComplete proof and closed D work-item barrier;
- each required E/F/G/H/Storage/external recipient target Confirmed or covered by an exact, approved, unexpired PolicyException;
- no unresolved required Unknown/Failed target;
- backup/restore anti-resurrection proof and retention/legal-hold evaluation;
- authentic, scope-bound evidence vector and complete audit references;
- any required physical-erasure evidence from the responsible storage/copy authorities.

- 当前、无缺口的 I ProducerDomainInventoryEpoch 和有效 TargetInventorySeal；
- D 精确、当前有效的 CanonicalSuppressionComplete 证明及已闭合 D Work Item Barrier；
- 每个必需 E/F/G/H/Storage/External Recipient 目标均已 Confirmed，或由精确、批准且未过期的 PolicyException 覆盖；
- 不存在未解决的必需 Unknown/Failed 目标；
- Backup/Restore 防复活证明及 Retention/Legal Hold 评估；
- 真实、Scope 绑定的 Evidence Vector 和完整审计引用；
- 责任存储/副本方提供的任何必需物理擦除证据。

The I global evaluator MUST preserve separate output states for suppression, cleanup, global completion with/without policy exception, and physical-erasure evidence. A logical D `Forgotten` event is never enough by itself.

I 全局评估器必须分别保留抑制、清理、带/不带策略例外的全局完成以及物理擦除证据状态。D 的逻辑 `Forgotten` 事件本身永远不足以证明全局完成。

---

## 6. Required schema and evidence / 必需 Schema 与证据

Logical receipt model (not wire encoding):

逻辑 Receipt 模型（非 Wire 编码）：

```text
ForgetTerminalizationAuthorizationReceipt {
  receipt_ref
  nonce
  forget_operation_id
  memory_id
  expected_memory_version
  scope_digest
  target_lineage_digest
  forget_fence_generation_ref       // opaque D value
  d_canonical_suppression_proof_ref
  d_canonical_suppression_proof_digest
  lifecycle_event_digest
  expected_lifecycle_sequence
  policy_domain_ref
  policy_version
  permission_epoch                  // opaque I-local value
  issuer_key_id
  issuer_key_version
  issuer_key_status_ref
  i_revocation_watermark
  i_sequencer_position
  consumption_result               // COMMIT_WON | REVOCATION_WON | UNKNOWN
  issued_at
  consumed_at
  signature_profile
  signature
}
```

I terminal closeout model:

I 终态关闭模型：

```text
ForgetTerminalizationAuthorizationCloseout {
  receipt_ref
  lifecycle_event_ref?              // present only for D_TERMINALIZED
  lifecycle_event_digest?
  d_outcome                          // D_TERMINALIZED | D_NO_TERMINALIZATION | UNKNOWN
  d_authority_ref
  d_outcome_digest
  i_closeout_position
  i_terminal_status                  // CLOSED | IN_DOUBT
  integrity_proof
}
```

The wire schema, signature suite, key lifecycle, receipt retention, canonical serialization and sequencer durability are separate implementation decisions. This proposal does not freeze them.

Wire Schema、签名套件、Key Lifecycle、Receipt 保留期、Canonical Serialization 和 Sequencer 持久化属于独立实现决策。本提案不冻结这些内容。

---

## 7. Required tests / 必需测试

| Test ID | Race/failure / 竞争或故障 | Required result / 必须结果 |
|---|---|---|
| I-D-FT-001 | Authorization valid, D CAS succeeds / 授权有效且 D CAS 成功 | Exact event commits; I closes exact participant; no global completion implied. / 精确事件提交；I 关闭精确 Participant；不暗示 Global Completion。 |
| I-D-FT-002 | Revocation wins before I consumption / I 消费前撤权先行 | `REVOCATION_WON`; no Forgotten event; Fence remains active. / `REVOCATION_WON`；不产生 Forgotten 事件；Fence 继续有效。 |
| I-D-FT-003 | COMMIT_WON then revocation / COMMIT_WON 后撤权 | Revocation is held for exact event until D outcome; no other event can reuse receipt. / 撤权针对精确事件等待 D 结果；其他事件不能重用 Receipt。 |
| I-D-FT-004 | D proof stale before CAS / CAS 前 D Proof 过期 | D CAS rejects; I closes only with D no-terminalization proof. / D CAS 拒绝；I 仅凭 D 未终态化证明关闭。 |
| I-D-FT-005 | I PermissionEpoch stale/gapped/unknown / I PermissionEpoch 过期/有缺口/未知 | No COMMIT_WON; D fails closed. / 不产生 COMMIT_WON；D fail closed。 |
| I-D-FT-006 | Wrong Memory/version/scope/operation/digest / Memory/Version/Scope/Operation/摘要错误 | Receipt rejected; no event. / Receipt 拒绝；不产生事件。 |
| I-D-FT-007 | Duplicate nonce / Nonce 重复 | Same exact idempotent request returns same outcome; altered tuple is conflict. / 完全相同幂等请求返回同一结果；修改元组为 Conflict。 |
| I-D-FT-008 | Lost response after COMMIT_WON / COMMIT_WON 后响应丢失 | Recovery queries exact sequencer participant; no re-consumption or inferred success. / 恢复查询精确 Sequencer Participant；不重复消费、不推断成功。 |
| I-D-FT-009 | D outcome missing/contradictory / D 结果缺失或矛盾 | I remains IN_DOUBT; no revocation release or global completion inference. / I 保持 IN_DOUBT；不释放撤权、不推断全局完成。 |
| I-D-FT-010 | Requester revoked after Fence commit / Fence 提交后请求者撤权 | Fence and outstanding obligations persist; only current continuity principal may resume. / Fence 与未完成义务持续存在；仅当前连续性主体可恢复。 |
| I-D-FT-011 | D Forgotten event without I receipt / 无 I Receipt 的 D Forgotten 事件 | Contract violation; event rejected or quarantined by conformance verifier. / 契约违规；一致性验证器拒绝或隔离事件。 |
| I-D-FT-012 | D Forgotten event followed by incomplete global inventory / D Forgotten 后全局 Inventory 不完整 | D event remains historical fact; I global state remains pending/blocked. / D 事件保留为历史事实；I 全局状态保持 Pending/Blocked。 |

These are new D/I cross-owner tests. Existing I reference-model tests do not prove these tests have run.

以上为新增 D/I 跨 Owner 测试。现有 I Reference Model 测试不证明这些测试已经执行。

---

## 8. Exact approval and exit criteria / 精确批准与退出条件

| Party / 责任方 | Required decision / 必需决策 |
|---|---|
| I | Approve the I-owned receipt semantics, revocation ordering, PermissionEpoch/currentness, key status, exception and global-evaluator boundaries against this exact Blob. / 针对本精确 Blob 批准 I Receipt 语义、撤权排序、PermissionEpoch/当前性、Key Status、例外和全局评估边界。 |
| D | Accept the exact event binding, D CAS, proof/fence currentness and no-rollback semantics; publish D Owner decision in D's own branch. / 接受精确事件绑定、D CAS、Proof/Fence 当前性和不回滚语义；在 D 自己的分支发布 Owner 决定。 |
| Storage | Confirm that D LifecycleEvent commit can validate/consume the I receipt at the authoritative commit point or provide an approved equivalent linearizable protocol; no detached stale ALLOW. / 确认 D LifecycleEvent 提交可在权威提交点验证/消费 I Receipt，或提供获批准的等价线性一致协议；不得使用 Detached Stale ALLOW。 |
| A / Independent Integration Reviewer | Verify exact version join, cross-namespace type safety, race behavior, bilateral acceptance and reproducible tests. The reviewer must not be the proposal author or implementer. / 核验精确版本 Join、跨命名空间类型安全、竞争行为、双边接受和可复现测试。审查者不得是提案作者或实现者。 |

The proposal is not normative until all required Owner decisions reference the exact Blob SHA. External Privacy/Legal/Security Governance approvals remain a separate governance gate and cannot be supplied by an architect or by this ChatGPT session.

所有必需 Owner 决策引用精确 Blob SHA 后，本提案才可成为规范。外部 Privacy/Legal/Security Governance 批准仍是独立治理 Gate，架构师或本 ChatGPT 会话均不能代为批准。

---

## 9. Source documents / 来源文档

I baseline branch: `session-i-security-governance-2026-11-16` @ `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`.

I 基线分支：`session-i-security-governance-2026-11-16` @ `0d071bf1ee7cc71912398c6ae57e4496e08f44ab`。

- `09-security-governance/forget-retention-backup-and-erasure-policy.md` — blob `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` (CANDIDATE; external proof open).
- `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` — blob `9100061fa986fb6676656169de3fcf9fc1c72664` (CANDIDATE; consumer conformance open).
- `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md` — blob `bae6a24fe3a374bc816993979a8fa9af52517dea` (I technical baseline confirmed; external governance approval blocked).
- `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` — blob `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` (semantic proposal; token schema/conformance open).
- `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` — blob `54bab0484bd232a5a258e65e34cc7425288b39a6` (I-role proposal; exact approval/crypto/conformance open).
- `09-security-governance/phase-3.6-governance-approval-and-consumer-acceptance-register.md` — blob `f8cfab7100e161ec4b8d0d9791a66337ab7a69de` (governance approvals blocked; consumer acceptance and execution gaps recorded).
- `09-security-governance/tests/global_forget_model.py` — blob `5233da028e409ec3f41848582dad73a923e7155b`.
- `09-security-governance/tests/test_global_forget_model.py` — blob `428e15c6263b5b2d730b93ce5412d55e782a449b`.

