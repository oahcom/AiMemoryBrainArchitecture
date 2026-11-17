# Phase 3.8.4 — I Amendment: Signed Schema Artifact Revision and Manifest Digest Semantics
# Phase 3.8.4 — I 修订：签名 Schema Artifact Revision 与 Manifest Digest 语义

- Owner: I — Security, Identity and Governance
- Parent proposal: `AIMBA-I-CRYPTO-1.0`, Blob `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- Status: **PROPOSED AMENDMENT / CANDIDATE ONLY — NOT APPROVED / NOT FROZEN**
- English and Chinese are normative peers.

## 1. Exact reviewed inputs / 精确输入

| Artifact | Exact Blob |
|---|---|
| H Unified Schema 1.2.11, wire 1.3.0 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H crypto wire mapping 3.8.4 | `bf160288d7529b37ad1b56924c1583748922aa25` |
| I P0 vector set | `4657f0c81e9c8692d29ac183380f3d7e074a4e4c` |
| I Python/Node vector test | `7658edc6f51dac203742ecc1ecf00d41bd676908` |
| H unified manifest semantic test file | `1eb90da6bea5e6bba062fa59f7b22f79105f46c7` |
| H semantic union validator module | `4a7c22ed15dff0a688559f79e4facbffca6527cd` |

## 2. Signed schema version binding / 签名 Schema 版本绑定

For all I-signed message families carried by the H Unified Schema, I requires:

- `schema_artifact_revision = 1.2.11`;
- `schema_version = 1.3.0`;
- both fields are required by the common envelope and included in P0;
- the receiver resolves the exact schema artifact from the signed artifact revision and rejects a mismatch between the field, schema registry entry and resolved schema;
- no downgrade from wire 1.3.0 to 1.2.0 is permitted for these protected records.

对于由 H Unified Schema 承载的所有 I 签名消息族，I 要求：

- `schema_artifact_revision = 1.2.11`；
- `schema_version = 1.3.0`；
- 两个字段均为 Common Envelope 必填项并纳入 P0；
- 接收方必须按已签名的 Artifact Revision 解析精确 Schema，并拒绝字段、Schema Registry 与实际解析工件之间的不一致；
- 受保护记录不得从 Wire 1.3.0 降级到 1.2.0。

RecoveryJoin 1.0.1 remains a separate schema artifact. Its nested `completeEmptyProof` and `outOfScopeProof` keep their own exact field projections and do not inherit the Unified Schema artifact revision. A future RecoveryJoin artifact change must independently specify whether its artifact revision is carried in the proof P0.

RecoveryJoin 1.0.1 是独立 Schema 工件。其嵌套 `completeEmptyProof` 与 `outOfScopeProof` 继续使用各自精确字段投影，不继承 Unified Schema Artifact Revision。未来 RecoveryJoin 工件升级必须单独规定是否将 Artifact Revision 纳入 Proof P0。

## 3. Manifest digest fields / Manifest 摘要字段

I requires the following distinctions in `OWNER_LOCAL_GATE_RELEASE` and its exact P0:

- `manifest_content_digest`: digest of the canonical union Manifest content, including the typed COC participant and unregistered owner-local admission members, frozen owner snapshot roots and prefix binding;
- `manifest_record_entry_digest`: digest of the final committed COC Manifest Record entry, including the exact Batch backlink;
- `batch_digest`: exact Recovery Cutoff Batch payload digest;
- `batch_entry_digest`: exact committed COC Batch Record entry digest.

These values are not aliases and MUST NOT be copied into one another. I's P0 includes all four owner-authored references/digests. COC-added record position/entry fields remain excluded from owner P0 only where the exact H mapping enumerates them as coordinator-added fields.

I 要求 `OWNER_LOCAL_GATE_RELEASE` 及其精确 P0 区分：

- `manifest_content_digest`：规范化 Union Manifest 内容摘要，覆盖类型化 COC Participant、未登记 Owner-local Admission、冻结 Owner Snapshot Roots 与 Prefix 绑定；
- `manifest_record_entry_digest`：最终已提交 COC Manifest Record Entry 摘要，包含精确 Batch Backlink；
- `batch_digest`：Recovery Cutoff Batch Payload 摘要；
- `batch_entry_digest`：已提交 COC Batch Record Entry 摘要。

这些值不能互换，也不能互相复制。I 的 P0 必须包含四项 Owner-authored 引用/摘要。只有 H 精确 Mapping 明确列为 Coordinator-added 的 COC Position/Entry 字段，才可按其规则排除在 Owner P0 之外。

## 4. Owner snapshot membership proof / Owner Snapshot 成员证明

The H schema now requires immutable membership-proof reference and digest for each owner-admission binding and each unregistered owner-local admission. I accepts this as the correct wire-level requirement, subject to I's proof authority:

1. I defines the proof payload, canonical projection, digest preimage, issuer/subject/audience/purpose and trust profile for I-owned admission membership proofs.
2. The proof MUST bind the exact owner ledger ref/version, entry ref/digest, owner-local sequence namespace/value, captured admission high-water, owner snapshot ref/digest/attestation digest, ledger root, operation digest and scope binding.
3. Verification MUST establish inclusion in the exact signed frozen snapshot and prove the row is at/below that snapshot's owner-local high-water. H must not numerically compare or order I, D and C counters.
4. Missing proof, incomplete page, unavailable ledger, changed root, stale snapshot or anti-rollback uncertainty returns UNKNOWN and blocks I Gate Release.
5. D and C must independently define their corresponding membership-proof semantics; I does not attest D/C ledger rows.

H Schema 现在要求每个 Owner Admission Binding 与未登记 Owner-local Admission 都携带不可变 Membership Proof Ref 与 Digest。I 接受这一 Wire 要求，但证明 Authority 仍由各 Owner 掌握：

1. I 定义 I-owned Admission Membership Proof 的 Payload、Canonical Projection、Digest Preimage、Issuer/Subject/Audience/Purpose 与 Trust Profile。
2. Proof 必须绑定精确 Owner Ledger Ref/Version、Entry Ref/Digest、Owner-local Sequence Namespace/Value、捕获的 Admission High-water、Owner Snapshot Ref/Digest/Attestation Digest、Ledger Root、Operation Digest 与 Scope Binding。
3. 验证必须证明该行属于精确签名冻结 Snapshot，并证明其不超过该 Snapshot 的 Owner-local High-water。H 不得对 I/D/C 计数器做跨 Owner 数值比较或排序。
4. Proof 缺失、分页不完整、Ledger 不可用、Root 变化、Snapshot 过期或 Anti-rollback 不确定时返回 UNKNOWN，阻断 I Gate Release。
5. D 与 C 必须独立定义自己的 Membership Proof 语义；I 不为 D/C Ledger 行背书。

## 5. Vector disposition / 向量处理

The I vector set updates the three unified-schema I P0 families to include the exact artifact and wire versions. The I Gate Release vector now signs `manifest_content_digest` and `manifest_record_entry_digest` separately. The two RecoveryJoin nested proof vectors remain on their own schema projection.

The Python RFC 8785 + Ed25519 implementation and Node JCS + Ed25519 oracle are independent test implementations using a deterministic TEST-ONLY seed. Their success establishes cross-language test-vector agreement only; it does not approve production Ed25519 use, trust roots, HSM/KMS, key lifecycle or historical trust.

I 向量集已更新三个 Unified Schema I P0 消息族，纳入精确 Artifact 与 Wire Version。I Gate Release 向量分别签署 `manifest_content_digest` 与 `manifest_record_entry_digest`。两个 RecoveryJoin 嵌套 Proof 向量仍使用各自 Schema Projection。

Python RFC 8785 + Ed25519 实现与 Node JCS + Ed25519 Oracle 是独立测试实现，使用确定性的 TEST-ONLY Seed。测试成功只证明跨语言测试向量一致，不批准生产 Ed25519 使用、Trust Root、HSM/KMS、Key Lifecycle 或历史信任。

## 6. I decision boundary / I 决议边界

This amendment is proposed. I will issue a separate exact-version review after the H schema, H mapping, vector set and CI run are all pinned to one immutable bundle. It does not approve production cryptographic activation, owner ledger deployment, COC quorum persistence, Storage visibility acceptance, JF-10 P0 closure or production activation.

本修订仍为提案。待 H Schema、H Mapping、Vector Set 与 CI Run 全部绑定到同一不可变版本后，I 将另行出具精确版本审查。本修订不批准生产密码学启用、Owner Ledger 部署、COC Quorum 持久化、Storage Visibility 接受、JF-10 P0 关闭或生产激活。
