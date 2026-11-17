# Phase 3.8 — A Integration Decision: D/E/I/Storage Atomic Registration-to-Visibility

- Owner: A — Principal Integration Architect
- Status: **COHERENT PROPOSED COMPOSITION; exact independent Owner approval, implementation and conformance OPEN**
- Related issues: #21 (lifecycle reconciliation), #25 (atomic producer admission and derivative visibility)
- English and Chinese are normative peers.

## 1. Executive disposition

A has reconciled the final exact proposal blobs from D, E, I and Storage. The architecture is coherent as a proposed composition after two corrections:

1. EventRef-only work may be D-registered before Canonical MemoryRef exists when D's identity/class/Scope/digest/approved lineage requirements are met. It is barrier-counted; canonical refs/revisions must be linked before dependency registration/publication.
2. Storage must durably create the hidden StorageVisibilityParticipantRef before D admits PublicationParticipantRef. This closes the crash window where D could otherwise hold an in-flight barrier participant without a durable Storage recovery anchor.

A accepts the composition **WITH ENUMERATED CONDITIONS** as the next design baseline. This is an integration-session role decision, not independent approval by the D/E/I/Storage Owners. No implementation, test pass, database deployment, schema freeze, merge or production activation is claimed.

## 2. Exact final artifacts reviewed

| Role | Branch | Commit | Exact Blob | Artifact |
|---|---|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 69be7ae9a25d7235cdb12df556c067ea8335e48c | 206ead86103302d147c5e08a5c2ce93ec8c1d0c2 | 03-memory-brain/phase-3.7-d-producer-class-registry-eventref-ingress-and-participant-intent.md |
| E | session-e-memory-compiler-2026-11-16 | 12f8def9c2df1397a56e5b1c9d10e54604c808ea | bad04d2d8caa654ee4c0ffd65f32fd962a19f10f | 04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md |
| I | session-i-security-governance-2026-11-16 | 8a90c91c442c91543b82f085efb0886b745be4da | e3b1b5d99eb36ac0b395854d8c19287d2b64b752 | 09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | b97b6ccbf5d9d00b44debd08144d44e4cf396146 | 1ad895f191c2dbe2f450d0fab49e0f61f20a5a5a | reviews/storage-consistency/phase-3.7-storage-atomic-producer-registration-dependency-visibility-realization.md |

A re-fetched all four artifacts from their exact owner branches. Blob SHA equality and bilingual content are verified.

### Controlling source contracts

- D operation semantics: `forget-fence-operation-and-publication-gate.md`, Blob `4da0b61ba3656a768ea56b4a2a24e09da4e21cd5`.
- E producer admission: `compiler-state-and-producer-admission.md`, Blob `e59f517fff161ab882aa0ddc4a5bda513964ae1a`.
- E staging/derived registration: `forget-fence-and-derived-registration.md`, Blob `00e37ba56596e710513c8d0568acd79141d9101b`.
- I PermissionEpoch/final-boundary: Blob `bae6a24fe3a374bc816993979a8fa9af52517dea`.
- I CommitAuthorizationReceipt/sequencer: Blob `5a5304d48aa912dcf6f817099bd5659371d8cdc8`.
- Storage realization review: Blob `107d21bd2c604ee0b04feff2ee5580e1de9c7fce`.
- Storage prepared-participant design v3.1: Blob `d5bdc72f193fcdaa654e4f07f865b77c578673ca`. This is related JF-10 evidence only, not proof that producer visibility is implemented.
- C final-submit contract: Blob `45a48249717c8cddb07ab96197730ef93d406c22`.
- G Applied/Context contract: Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`.

## 3. Conflict resolution

### 3.1 EventRef-only ingress

The earlier Phase 3.7 quarantine-only wording conflicted with D's controlling §3.2, which permits registration before Canonical MemoryRef creation. The final D/E proposals correct this:

- D may register EventRef-only ProducerWork when authenticated producer, enabled ProducerClass/version, exact Scope, request digest and D-approved opaque lineage token/digest are present.
- The work receives D ProducerRegistrationSequence and is included in ForgetFence high-water.
- D registration is not I permission for protected payload dereference.
- E must link exact Canonical MemoryRef/MemoryVersionRef revisions before dependency registration/publication.
- Missing identity, Scope, lineage or authority remains quarantined; no implicit admission.

**A resolution:** D §3.2 controls; the corrected Phase 3.7 D/E addenda now align with it.

### 3.2 D/E/Storage register-before-work and fence race

D owns the semantics; Storage supplies the durable serialization; E consumes the receipt. RegisterProducerWork and InstallForgetFence must share one linearizable ordering domain:

- Registration first: its sequence is at/below the fence's captured high-water and remains barrier-accounted.
- Fence first: later registration is rejected/quarantined/cleanup-only and receives no execution capability.
- No third admitted-but-unaccounted state.

E may not enqueue, lease, dereference protected source content or execute derivative-capable work before durable D RegistrationReceipt resolution.

### 3.3 Complete dependency set

E stages bytes privately. D RegisterDerivedDependency must durably commit the immutable artifact identity and complete direct/transitive dependency set as one complete registration. Partial, unknown or conflicting lineage remains private and non-publishable. Exact canonical refs/revisions must be linked before this step for EventRef-only ingress.

### 3.4 Final visibility — conjunctive D and I barriers

The final corrected order is:

1. **Storage prepare first:** persist hidden StorageVisibilityParticipantRef bound to PublicationOperationId/digest, WorkItemId, artifact/version, attempt/lease, dependency digest and private stage.
2. **D publication admission:** D admits PublicationParticipantRef bound to that exact durable StorageVisibilityParticipantRef and records it as unresolved in the D fence/barrier.
3. **I authorization consumption:** I consumes a single-use CommitAuthorizationReceipt in its PolicyDomain sequencer, bound to the exact D and Storage participants, principal/workload, action/resource, Scope/Environment, PermissionEpoch and immutable publication digest.
4. **Storage final visibility commit:** validate exact D participant/current fence and I terminal proof; atomically commit visibility pointer, PublicationReceipt, Storage outcome and outbox in the D/Storage serialization domain.
5. **Independent closeout:** D and I independently consume the same authoritative Storage outcome. COMMITTED_VISIBLE closes the corresponding participant and records historical publication; authoritative NO_PUBLICATION closes it as safely aborted. UNKNOWN/IN_DOUBT keeps both barriers open and the artifact private.

D Fence-first rejects D publication admission. A D publication participant admitted first holds a later fence behind that unresolved participant until Storage terminality. I Revocation-first rejects receipt consumption. I COMMIT_WON first holds later revocation behind the exact participant until Storage terminality. The two namespaces are conjunctive; no scalar epoch/high-water or cross-authority numeric comparison is permitted.

### 3.5 Crash-window correction

Storage prepare must precede D publication admission. Therefore:
- Crash after Storage prepare but before D admission leaves an orphan hidden Storage participant with no D publication admission and no visibility capability.
- Crash after D admission means the exact Storage participant already exists and is recoverable by stable ID/digest.
- Missing Storage state after confirmed D admission is UNKNOWN/ledger inconsistency, never proof of abort.
- Crash after I COMMIT_WON keeps I revocation pending; D's barrier also remains held.
- Lost visibility ACK is resolved by the same PublicationOperationId/digest.
- Only authoritative Storage COMMITTED_VISIBLE or NO_PUBLICATION evidence closes D/I participants.

This corrects the earlier D-first sequence and is the required current order.

## 4. Nominal identity separation

The following are different types and cannot be aliased:

- D PublicationParticipantRef — in-flight derivative visibility barrier participant.
- C ParticipantIntentRef — pre-provider-side-effect participant.
- StorageVisibilityParticipantRef — hidden Storage visibility transaction participant.
- Storage PreparedParticipantRef / PreparedTransactionGID / PostgreSQLNativeXID — separate JF-10 prepared-transaction identity.
- ProducerWorkItemId, DerivationRunId, AttemptId, LeaseId, PublicationOperationId and CausalOrderTransactionRef — distinct work/run/attempt/operation identities.
- D ProducerRegistrationSequence, D ForgetFenceGeneration, D CanonicalCommitCursor, I PermissionEpoch and Storage visibility/transaction positions — separate namespaces.

A generic version/epoch/cursor field or a transport ACK cannot substitute for any of these.

## 5. Role dispositions

| Role | Integration-session disposition | Conditions |
|---|---|---|
| D | ACCEPT WITH ENUMERATED CONDITIONS | Exact operation/API schemas; durable PublicationParticipantRef lifecycle; fence hold/release; signed terminal proof; conformance |
| E | ACCEPT WITH ENUMERATED CONDITIONS | Exact compiler mapping; EventRef lineage completion; stable retry/recompile; private staging; output/terminal accounting |
| I | ACCEPT WITH ENUMERATED CONDITIONS | Exact derivative CommitAuthorizationReceipt/terminal proof; I sequencer/revocation hold; key/currentness policy and verifier conformance |
| Storage | ACCEPT WITH ENUMERATED CONDITIONS | Named shared serialization topology; durable visibility participant; atomic final visibility/outbox; recovery/failover/restore proof |
| A | ACCEPT COMPOSITION AS PROPOSED BASELINE | Exact independent Owner approvals and all physical evidence remain required |

These are role-played proposal positions in this integration session. They must not be represented as independent Owner signatures or approvals.

## 6. Remaining blockers

1. **D schema/API:** exact ProducerClass, RegistrationReceipt, DependencyRegistrationReceipt, PublicationParticipantRef, terminal proof and error/idempotency schemas.
2. **I gate protocol:** exact receipt and terminal proof schema for derivative publication; proof that revocation cannot pass an unresolved publication; verifier/key-status policy and anti-rollback.
3. **Storage topology:** select and document the actual transaction/serialization authority. The single serializable database per Canonical Memory authority is a recommendation, not a deployment decision. If separate stores are used, D/I/Storage must approve and prove the durable prepare/commit alternative.
4. **H wire:** exact schema, canonicalization, signatures, audience, replay/downgrade and interoperability vectors for the new D/I/Storage evidence families.
5. **Engineering:** deterministic race/crash/failover/restore tests for registration-vs-fence, dependency-set completeness, D fence-vs-publication participant, I revocation-vs-receipt consumption, visibility ACK loss, stale lease and restore quarantine.
6. **Restore:** independent D/I/Storage proof reconciliation and no serving before current control state is verified.
7. **C/G/H Applied:** remains a separate final-request/Applied workstream. This D/E/Storage visibility gate does not prove C provider submission, G Applied or Execution Started. C and G exact contracts remain unchanged; H wire remains NOT FROZEN.

### Required minimum race/fault cases

- registration commits immediately before fence install;
- fence install commits immediately before registration;
- EventRef-only admission with valid lineage token, then canonical-ref linking;
- EventRef-only admission with missing/invalid lineage token;
- partial dependency-set write and recovery;
- stale AttemptId/LeaseId after lease replacement;
- Storage prepare ACK loss before D admission;
- D admission ACK loss after Storage prepare;
- I revocation before receipt consumption;
- I COMMIT_WON followed by later revocation;
- D fence before/after PublicationParticipant admission;
- crash after I COMMIT_WON but before Storage visibility commit;
- Storage commit with lost ACK;
- authoritative NO_PUBLICATION and UNKNOWN distinction;
- restore with stale D ledger, I revocation state or Storage visibility pointer.

All are **SPECIFIED / NOT RUN** for this proposal.

## 7. Final A decision

**Phase 3.8 D/E/I/Storage architecture: ACCEPT AS A COHERENT PROPOSED COMPOSITION WITH ENUMERATED BLOCKERS.**

Not authorized:
- shared schema or wire freeze;
- database product selection/deployment;
- implementation or conformance PASS;
- branch merge;
- provider execution or G Applied promotion;
- production activation;
- Global Forget completion or physical-erasure claim.

Issue #25 remains OPEN pending independent exact-owner acceptance, physical topology and test evidence.

## 8. 中文规范

### 8.1 A 集成结论

A 已对 D、E、I、Storage 四份最终精确 Blob 完成集成复核。架构作为提案整体一致，但必须先解决两个冲突：

1. EventRef-only Work 在 Producer 身份、Class、Scope、摘要和 D 批准的 Lineage Token 完整时，可以在 Canonical MemoryRef 形成前由 D 正式注册并纳入 Barrier；Canonical Refs/Revisions 必须在 Dependency Registration/Publish 前补齐。
2. Storage 必须先持久化隐藏 StorageVisibilityParticipantRef，D 才能接受绑定它的 PublicationParticipantRef。否则会出现 D Barrier Participant 存在但 Storage 无恢复锚点的崩溃窗口。

A 对该组合给出“附明确条件接受”，仅作为本集成会话的提案基线，不代表 D/E/I/Storage 独立 Owner 签署，也不代表实现、测试、数据库部署或生产启用。

### 8.2 精确版本

| 角色 | Branch | Commit | Blob |
|---|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 69be7ae9a25d7235cdb12df556c067ea8335e48c | 206ead86103302d147c5e08a5c2ce93ec8c1d0c2 |
| E | session-e-memory-compiler-2026-11-16 | 12f8def9c2df1397a56e5b1c9d10e54604c808ea | bad04d2d8caa654ee4c0ffd65f32fd962a19f10f |
| I | session-i-security-governance-2026-11-16 | 8a90c91c442c91543b82f085efb0886b745be4da | e3b1b5d99eb36ac0b395854d8c19287d2b64b752 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | b97b6ccbf5d9d00b44debd08144d44e4cf396146 | 1ad895f191c2dbe2f450d0fab49e0f61f20a5a5a |

A 已从各自 Owner Branch 重新读取，Blob SHA 和中英双语内容均已验证。

### 8.3 冲突裁决与发布顺序

最终顺序为：

1. Storage 首先持久化隐藏 StorageVisibilityParticipantRef。
2. D 接受并绑定该精确 Storage Participant 的 PublicationParticipantRef，将其纳入 D Fence/Barrier。
3. I 在 PolicyDomain Sequencer 中消费绑定两个 Participant 和不可变 Publication Digest 的单次 CommitAuthorizationReceipt。
4. Storage 最终 Visibility Commit 同时验证 D 当前 Participant/Fence 和 I Terminal Proof，并原子提交 Visibility Pointer、PublicationReceipt、Storage Outcome 和 Outbox。
5. D/I 分别消费同一权威 Storage Outcome。COMMITTED_VISIBLE 或权威 NO_PUBLICATION 才能关闭各自 Participant；UNKNOWN/IN_DOUBT 保持 Barrier 开放且 Artifact Private。

D Fence-first 或 I Revocation-first 都阻断 Visibility。D PublicationParticipant 或 I COMMIT_WON 单独存在都不是发布许可。两个权威域独立且合取，不得合并成一个标量序列。

### 8.4 类型隔离

D PublicationParticipantRef、C ParticipantIntentRef、StorageVisibilityParticipantRef、Storage PreparedParticipantRef/GID/XID 必须保持不同类型。ProducerWorkItemId、DerivationRunId、AttemptId、LeaseId、PublicationOperationId 和 CausalOrderTransactionRef 也不得混用。

### 8.5 未决事项

仍须完成 D/I 精确 Schema/API、Storage 实际事务拓扑、H Wire Schema/Canonicalization/Signature/Interop、确定性 Race/Crash/Failover/Restore 测试，以及恢复后的独立 D/I/Storage 证明验证。C/G/H 的 Provider Submit/Applied 仍是独立工作流，本文件不替代其批准。

**最终状态：架构提案一致；独立 Owner 接受、物理实现和符合性仍 OPEN。**
