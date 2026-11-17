# Phase 3.8.5 — I Exact Review of Storage Logical Serialization Topology
# Phase 3.8.5 — I 对 Storage 逻辑序列化拓扑的精确审查

- Reviewer: I — Security, Identity and Governance
- Branch: `session-i-security-governance-2026-11-16`
- Exact Storage ADR reviewed: `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md`
- ADR Blob: `1ef47d4e5711c7db73a24d249adf1992be1f6aa4`
- I Phase 3.8 Commit Authorization / Revocation Sequencer contract: Blob `54bab0484bd232a5a258e65e34cc7425288b39a6`
- Decision: **ACCEPT WITH ENUMERATED I-OWNED CONDITIONS — L1 LOGICAL COMPOSITION**
- English and Chinese are normative peers.

## 1. I decision / I 决议

I accepts Option A as a feasible logical topology for D/Storage publication serialization, provided that I's PolicyDomain sequencer remains a separate authority and that the exact consumed CommitAuthorizationReceipt is bound to the same D PublicationParticipantRef and StorageVisibilityParticipantRef.

I's sequencer is not folded into the Storage transaction domain. The shared D/Storage transaction domain does not become an I policy sequencer and cannot mint I decisions. I remains the only authority that orders receipt consumption against revocation and policy/issuer changes.

I 接受 Option A 作为 D/Storage Publication Serialization 的可行逻辑拓扑，前提是 I PolicyDomain Sequencer 保持独立权威，且精确消费的 CommitAuthorizationReceipt 绑定同一个 D PublicationParticipantRef 与 StorageVisibilityParticipantRef。

I Sequencer 不并入 Storage Transaction Domain。D/Storage 共享事务域不能成为 I Policy Sequencer，也不能签发 I 决策。I 仍是唯一负责将 Receipt Consumption 与 Revocation/Policy/Issuer Change 排序的权威。

## 2. Binding I conditions / I 约束条件

1. I consumes the exact single-use receipt in the I PolicyDomain sequencer after exact D and Storage participant identities are established.
2. Only COMMIT_WON permits the Storage final visibility transaction to proceed. REVOCATION_WON forbids visibility. UNKNOWN/IN_DOUBT keeps the I participant unresolved and affected gates closed.
3. The receipt binds PolicyDomainRef, PermissionEpoch, authenticated subject/actor/workload/delegation, action/resource/purpose/audience/Scope/Environment, OwnerBoundary, PublicationOperationId/digest, exact D and Storage participant refs, I sequencer position and key/profile references.
4. Storage validates the consumed pre-commit ICommitAuthorizationProof at the visibility linearization point. I's ITerminalProof is post-outcome evidence and MUST NOT be required before Storage commits.
5. After Storage COMMITTED_VISIBLE or authoritative NO_PUBLICATION, I independently verifies the exact outcome and closes its participant. If Storage is UNKNOWN/unavailable, I does not release the held revocation.
6. Scope remains one I PolicyDomain for v1. Multi-PolicyDomain atomicity is NOT ACCEPTED / BLOCKED.

## 3. No cross-log atomicity claim / 不声明跨日志原子性

The architecture has three distinct ordering authorities:
- D/Storage serializable transaction domain for canonical admission/fence/dependency and visibility;
- I PolicyDomain sequencer for authorization receipt consumption/revocation order;
- COC quorum log for cross-owner causal order and recovery-cutoff evidence.

There is no global scalar position and no claim that one log's commit atomically commits the other two. The safety protocol is conjunctive: exact participant refs, durable owner outcomes, held unresolved participants and recovery reconciliation. Unknown remains blocked.

架构包含三个独立顺序权威：D/Storage Serializable Transaction Domain、I PolicyDomain Sequencer、COC Quorum Log。不存在全局标量位置，也不声称一个 Log Commit 会原子提交另外两个。安全协议依靠精确 Participant Ref、持久化 Owner Outcome、未解决 Participant Hold 与恢复协调。UNKNOWN 必须阻断。

## 4. Final I disposition / I 最终结论

**ACCEPT WITH ENUMERATED I-OWNED CONDITIONS — L1 LOGICAL COMPOSITION.**

I accepts ADR Blob `1ef47d4e5711c7db73a24d249adf1992be1f6aa4` as a feasible logical topology. The actual I sequencer, trust registry, key custody, historical verification, anti-rollback anchor and deployment remain L4/operational obligations. The I crypto profile is not approved by this topology decision.

**有条件接受 — L1 逻辑组合。** I 接受该 ADR 作为可行逻辑拓扑。实际 I Sequencer、Trust Registry、Key Custody、历史验证、Anti-rollback Anchor 与部署属于后续 L4/运维义务。本拓扑决策不批准 I Crypto Profile。
