# Phase 3.8 Integration Addendum — I Authorization Context and Operation Identity Boundary
# Phase 3.8 集成补充 — I 授权上下文与 Operation 身份边界

**Status / 状态:** CANDIDATE REFERENCE-MODEL ADDENDUM — NOT NORMATIVE / 候选参考模型补充 — 非规范  
**Tracking / 跟踪:** Issue #25  
**Integration PR / 集成 PR:** #179  
**Current I source branch / 当前 I 来源分支:** `session-i-security-governance-2026-11-16`  
**Current I source HEAD / 当前 I 来源 HEAD:** `029ae8f8f48992532d5c0a9397816e4d8a9220a2`  
**Exact I source / 精确 I 来源:** `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` (not restored on main; see AID-2026-107 §10)  
**Exact I source Blob / 精确 I 来源 Blob:** `e3b1b5d99eb36ac0b395854d8c19287d2b64b752`  
**Additional controlling I source / 额外控制性 I 来源:** `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` (not restored on main; see AID-2026-107 §10)  
**Exact Phase 3.8 Blob / Phase 3.8 精确 Blob:** `54bab0484bd232a5a258e65e34cc7425288b39a6`

## 1. Why this addendum exists / 补充原因

PR #172 established a provisional one-`COMMIT_WON`-winner-per-`PublicationParticipantRef` invariant. The subsequent review identified two additional reference-model gaps: the authorization context was not fully bound to the participant decision, and the same operation identity was not carried consistently across D, I and Storage participant records.

PR #172 建立了临时的“每个 `PublicationParticipantRef` 仅允许一个 `COMMIT_WON` winner”不变量。后续审查又发现两个参考模型缺口：授权上下文未完整绑定到 Participant 决策；同一个 Operation 身份未在 D、I、Storage Participant 记录之间保持一致。

This addendum records the bounded model correction. It does not amend I's normative contract or approve the exact cross-owner protocol.

本补充记录有限范围的模型修正，不修改 I 规范契约，也不批准精确的跨 Owner 协议。

## 2. Exact model change / 精确模型变更

PR #179 carries both dimensions in one reference-model change:

PR #179 在同一参考模型变更中覆盖两个维度：

1. The immutable authorization-context tuple is bound to authorization identity, I `COMMIT_WON` proof, operation binding, Storage commit validation and UNKNOWN reconciliation.
2. The exact `operation_id` is bound across Storage hidden participant, D publication participant/admission proof, I authorization/COMMIT_WON proof, Storage commit and UNKNOWN/NO_PUBLICATION reconciliation.
3. A `PublicationParticipantRef` has at most one `COMMIT_WON` winner in this provisional model.
4. Substitution of operation ID, participant IDs, request digest, Owner Boundary, Final Visibility Gate identity, dependency digest, D proof, I proof or authorization context is rejected.
5. UNKNOWN remains private and requires exact reconciliation; it is not converted to success by local inference.

1. 不可变授权上下文元组绑定到授权身份、I `COMMIT_WON` 证明、Operation Binding、Storage Commit 验证及 UNKNOWN 核对。
2. 精确 `operation_id` 在 Storage Hidden Participant、D Publication Participant/Admission Proof、I Authorization/COMMIT_WON Proof、Storage Commit 和 UNKNOWN/NO_PUBLICATION 核对中保持绑定。
3. 在该临时模型中，一个 `PublicationParticipantRef` 最多只有一个 `COMMIT_WON` winner。
4. 替换 Operation ID、Participant ID、Request Digest、Owner Boundary、Final Visibility Gate 身份、Dependency Digest、D Proof、I Proof 或授权上下文均会被拒绝。
5. UNKNOWN 保持私有并要求精确核对，不得通过本地推断转换为成功。

## 3. Authorization context coverage / 授权上下文覆盖范围

The model currently binds these 25 context values:

当前模型绑定以下 15 个上下文值：

- `principal_ref`
- `actor_ref`
- `scope_binding_digest`
- `environment_ref`
- `action`
- `resource_ref`
- `purpose`
- `audience`
- `delegation_chain_ref`
- `policy_domain_id`
- `permission_epoch`
- `runtime_session_ref`
- `workload_binding_ref`
- `policy_version_digest`
- `decision_id`
- `tenant_security_domain_ref`
- `ownership_scope_ref`
- `applicability_scope_set_digest`
- `obligations_digest`
- `expiry`
- `producer_binding_ref`
- `adapter_binding_ref`
- `authenticated_transport_binding_ref`
- `authentication_strength`
- `operation_payload_digest`

These 25 values are immutable within the model's authorization identity and are carried into the I decision proof and subsequent Storage/UNKNOWN checks. The exact PublicationOperationId and D/Storage participant IDs are separately bound by the participant/operation tuple, not treated as free context metadata.

这些值在模型授权身份内保持不可变，并进入 I 决策证明及后续 Storage/UNKNOWN 检查。

### 3.1 Explicitly not covered / 明确尚未覆盖

The 25-value tuple is **not** the complete protected-boundary authorization mechanism. The following remain unimplemented or unproven:

该 15 值元组**不等于**完整的受保护边界授权机制。以下内容仍未实现或未证明：

- authenticated issuer identity, issuer credential validation, and issuer key ID/version/status at issuance and verification;
- live I policy/revocation/registry state and authoritative PolicyDomain sequencer continuity;
- exact DerivedArtifactRef/version/content digest, AttemptId/LeaseId/LeaseEpoch, dependency receipt and complete dependency-set digest as separate authoritative bindings (the model currently covers only a subset of these through generic IDs/digests);
- issuer key ID/version/status, key revocation and trust-root validation;
- live PolicyDomain policy-version currentness;
- live PermissionEpoch/revocation/registry currentness and sequencer continuity;
- cryptographic signature, canonicalization and authenticated evidence provenance;
- authenticated Principal/Actor/Workload/Delegation resolution;
- real scope isolation and cross-PolicyDomain enforcement.

- 经认证的 Issuer 身份及 Issuer 凭据验证；
- Issuer Key ID/Version/Status、密钥撤销及信任根验证；
- PolicyDomain 实时策略版本当前性；
- PermissionEpoch/撤权/注册表实时当前性及 Sequencer 连续性；
- 加密签名、规范化及经认证的证据来源；
- 经认证的 Principal/Actor/Workload/Delegation 解析；
- 真实 Scope 隔离和跨 PolicyDomain 执行。

`permission_epoch` remains opaque and I-local. The follow-up model now includes an explicit in-memory `current_permission_epochs` test seam: I COMMIT_WON is rejected if the current epoch is unavailable or differs from the authorization context; a later epoch advance does not rewrite a previously won COMMIT_WON. This models equality/fail-closed ordering only. It does not prove a live I sequencer, authenticated current-state source, issuer-key status, policy/revocation/registry currentness, or comparability with any D/Storage high-water.

`permission_epoch` 在模型中仅作为不透明的 I 本地值和精确绑定字段。该模型不证明真实 I Sequencer、实时新鲜度、撤权排序，也不证明它可与任何 D/Storage High-water 比较。

## 4. Exact-head verification / 精确 Head 验证

- Consolidated code PR: #179.
- Exact tested Head before this documentation-only addition: `5d8b1cc1d3b87e8a1238410688ae434e238987c2`.
- Publication Protocol run #44242418467: **52 tests / OK**.
- GOV-DOC-001 run #44242418382: **SUCCESS**.

- 集成代码 PR：#179。
- 本次仅文档追加前的精确测试 Head：`5d8b1cc1d3b87e8a1238410688ae434e238987c2`。
- Publication Protocol run #44242418467：**52 项测试 / OK**。
- GOV-DOC-001 run #44242418382：**SUCCESS**。

The follow-up PermissionEpoch currentness candidate adds an explicit unavailable/stale fail-closed test and tests that a later epoch advance does not cancel an earlier COMMIT_WON. Its current code/test Head before this documentation update is `0c55e4fd9ca7ae9c889498bf173b5888e11ca204` with 58 tests; exact-head CI is pending. The field-substitution test now checks all 25 tuple positions; the earlier index-16-only loop is not used as acceptance evidence. Any subsequent documentation change also requires a fresh exact-head run.

本次仅文档追加会改变 PR Head，因此合并前必须对新精确 Head 重新运行 CI。上述 52/52 仅证明前一代码 Head，不自动证明后续 Head。

## 5. Required owner decisions / 必需 Owner 决策

- I must confirm the required authorization fields, their cardinality/optionality and live currentness semantics against its controlling contract.
- D must confirm the exact operation identity and D participant/admission proof binding.
- Storage must confirm the same operation identity is durable and atomic across its participant and final visibility commit.
- D/I/Storage must explicitly decide whether one `PublicationParticipantRef` has one terminal authorization winner or whether operation-scoped accounting is required.
- Any successor normative contract must be accepted by the responsible Owners against one exact Blob SHA.

- I 必须依据控制性契约确认必需授权字段、基数/可选性及实时当前性语义。
- D 必须确认精确 Operation 身份及 D Participant/Admission Proof 绑定。
- Storage 必须确认相同 Operation 身份在其 Participant 和最终 Visibility Commit 中具备持久化原子保证。
- D/I/Storage 必须明确决定一个 `PublicationParticipantRef` 是否只有一个终态授权 Winner，还是需要按 Operation 进行核算。
- 任何后继规范契约都必须由责任 Owner 针对同一个精确 Blob SHA 明确接受。

## 6.1 Dependency digest consistency / Dependency Digest 一致性

PR #183 restores equality checks between the dependency-set digest persisted by the Storage hidden participant and the digest carried by the D publication participant at three boundaries: first I COMMIT_WON consumption, final Storage commit, and UNKNOWN/NO_PUBLICATION reconciliation. PR #186 adds negative tests for both Storage-side and D-side substitutions at the final-commit and UNKNOWN-reconciliation boundaries.

PR #183 恢复了三个边界上的一致性检查：首次 I COMMIT_WON 消费、Storage 最终 Commit、UNKNOWN/NO_PUBLICATION 核对时，Storage Hidden Participant 持久化的 Dependency Set Digest 必须与 D Publication Participant 携带的摘要一致。PR #186 增加了在最终 Commit 和 UNKNOWN 核对阶段分别替换 Storage 侧与 D 侧摘要的负向测试。

The test seam verifies tuple equality only. It does not prove canonical dependency-set digest derivation, authenticated dependency receipts, durable Storage atomicity, or production isolation.

测试接口仅验证元组相等，不证明规范 Dependency Set Digest 派生、Dependency Receipt 认证、Storage 持久化原子性或生产隔离。

## 6. Evidence ceiling / 证据上限

PR #179 is a deterministic in-memory reference model. Passing tests prove only the tested abstract transitions and substitution guards. They do not prove production authorization, signed/authenticated evidence, database durability or isolation, distributed races, multi-process fencing, crash/failover/restore, live D/I/Storage adapters, end-to-end conformance, or production readiness.

PR #179 是确定性的内存参考模型。测试通过仅证明被测试的抽象迁移和替换防护，不证明生产授权、签名/认证证据、数据库持久化或隔离、分布式竞态、多进程 Fencing、Crash/Failover/Restore、真实 D/I/Storage Adapter、端到端符合性或生产就绪。

**Disposition / 处置:** CANDIDATE MODEL EVIDENCE ONLY — Issue #25 remains OPEN; no Owner approval, architecture freeze, production authorization or activation is inferred.

**处置：** 仅为候选模型证据——Issue #25 仍 OPEN；不得推断已获 Owner 批准、架构冻结、生产授权或激活。
