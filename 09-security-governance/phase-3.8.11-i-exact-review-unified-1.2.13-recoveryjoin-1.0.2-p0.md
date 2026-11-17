# Phase 3.8.11 — I Exact Review: Unified 1.2.13 / RecoveryJoin 1.0.2 / Successor P0
# Phase 3.8.11 — I 对 Unified 1.2.13 / RecoveryJoin 1.0.2 / 后继 P0 的精确复审

- Owner perspective: I — Security, Identity and Governance
- Status: **ACCEPT AS I-OWNED ARCHITECTURE / P0 CANDIDATE; L3 / TRUST / PRODUCTION GATES OPEN**
- Project phase: **ARCHITECTURE DESIGN**
- I v1 crypto profile decision: Blob 56e956dca909af857469427378777705a5d1082a
- I successor P0 allowlists: Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6
- I C profile naming clarification: Blob 1e86a1349d371a1cdb4a56d69f783e0f316c7203
- H Unified schema 1.2.13: Blob 8e7f6a6c9663388863db88548f9c37d0fdb1bd97
- H RecoveryJoin schema 1.0.2: Blob 4b664e3bce465499bcdfd93796349a4ba7074002
- H Phase 3.8.10 review of I profile/P0: Blob 0b6eeadb1cfac415e77ec1358b9fdf99fde11d41
- H Phase 3.8.9 C outcome mapping: Blob a09980b168f14ef41f84567d28267387d9a98377
- C Phase 3.8.14 successor review of H/C mapping and validator: Blob dd4fb61536bead57d5c8db0a58abae93b368b72e
- C Phase 3.8.13 profile identifier decision: Blob 5067dadb9c646a054d78f03c56e635facc36311a
- I owner snapshot membership proof contract: Blob 88209bbea0ab600880c5c630cfe83af31ee16dd7
- Provenance: delegated I-role review; **not an independent human I Owner signature or external governance approval**.

## 1. Exact version decision / 精确版本决议

I confirms the current candidate pair:
- H Unified schema artifact revision 1.2.13, wire family 1.3.0;
- H RecoveryJoin schema 1.0.2;
- I P0 successor addendum Phase 3.8.9.

The current I P0 addendum supersedes the earlier 1.2.8/1.2.11-specific applicability language for the named message/proof families. The H 1.2.13 common envelope includes schema_artifact_revision as a signed field distinct from schema_version. H 1.2.13 ownerSnapshot and RecoveryJoin 1.0.2 membership proof carriers match the I successor P0 projection candidate.

I 确认当前候选版本对：H Unified 1.2.13（Wire 1.3.0）、RecoveryJoin 1.0.2、I Phase 3.8.9 后继 P0 附录。该 P0 附录取代指定消息/Proof Family 的旧 1.2.8/1.2.11 适用性声明。H 1.2.13 Common Envelope 将 schema_artifact_revision 作为独立签名字段；ownerSnapshot 与 RecoveryJoin 1.0.2 Proof Carrier 与 I 后继 P0 候选相匹配。

## 2. I profile and P0 ownership / I Profile 与 P0 权属

I confirms:
- AIMBA-I-CRYPTO-1.0 is the normative v1 architecture profile for I-authored protected evidence.
- Exact I P0 allowlists in Phase 3.8.9 apply to the named I message/proof families only.
- I ownerSnapshotAttestation, ICompleteEmptyProof, IOutOfScopeProof, ICommitAuthorizationReceipt, ITerminalProof and RecoveryJoin owner_snapshot_membership_proofs are distinct signed object families with separate P0s.
- The H ownerSnapshot summary is not the I signature object. H must dereference and verify the I-signed attestation and each membership proof separately.
- C's profile remains C-owned. C Phase 3.8.13 confirms AIMBA-C-CRYPTO-1.0 for CSubmitOutcome 1.0.1; I Phase 3.8.10 clarifies that AIMBA-C-OUTCOME-CRYPTO-1.0 was a non-normative example only. I's profile is not inherited by C.

I 确认 AIMBA-I-CRYPTO-1.0 是 I 自有保护证据的 v1 架构配置；Phase 3.8.9 P0 白名单只适用于指定 I 消息/证明族。I Attestation、CompleteEmpty、OutOfScope、AuthorizationReceipt、TerminalProof 与 RecoveryJoin Membership Proof 是不同签名对象，分别拥有独立 P0。H ownerSnapshot 不是 I 签名对象，必须解引用并分别验证。C Profile 由 C 独占；C 已确认 AIMBA-C-CRYPTO-1.0，I 的 Profile 不得被 C 继承。

## 3. I proof invariants / I 证明不变量

Every I proof must continue to bind exact owner kind, PolicyDomain, I ledger and entry identity/digest, admission ref, local sequence, captured high-water/root, snapshot/attestation, PermissionEpoch, inventory/registry epoch, scope/generation, operation/request, owner gate generation, key ID/version/status, historical checkpoint and anti-rollback anchor.

I/D/C/COC sequence spaces are distinct. No arithmetic comparison or ordering inference across those namespaces is permitted. I release requires a final I-local currentness CAS against the latest request/admission roots, PermissionEpoch, inventory/registry epoch, scope, GateGeneration and key status.

每个 I Proof 继续绑定精确 Owner Kind、PolicyDomain、I Ledger/Entry/Admission、Local Sequence、High-Water/Root、Snapshot/Attestation、PermissionEpoch、Inventory/Registry Epoch、Scope/Generation、Operation/Request、Gate Generation、Key ID/Version/Status、Historical Checkpoint 与 Anti-Rollback。I/D/C/COC 序列空间互相独立，不得跨 Namespace 作算术比较或顺序推断。I Release 必须执行 I 自己的最终 Currentness CAS。

## 4. Tri-state and authority boundary / 三态与权威边界

- Wrong owner/purpose/schema revision/profile/audience/scope/operation, duplicate or unknown critical field, digest mismatch, high-water mismatch, incomplete signed P0 or stale snapshot is INVALID.
- Missing I verifier, unavailable ledger/snapshot, incomplete pagination, unknown/revoked/compromised key status, unavailable historical checkpoint or unavailable anti-rollback service is UNKNOWN.
- COMPLETE_EMPTY requires the separately signed ICompleteEmptyProof; empty array/count zero is insufficient.
- H can validate transport/schema/P0 reconstruction and orchestrate joins; only I can authenticate I ledger completeness, authorization, key status, revocation/compromise ordering and I gate release.
- C provider outcome, D ForgetFence, Storage persistence/visibility and COC quorum remain independent owner facts.

## 5. Enumerated conditions / 明确保留条件

1. I v1 profile is an architecture baseline, not production-active. Production trust roots, KMS/HSM custody, key ceremonies, rotation/revocation/compromise operations and external anti-rollback remain OPEN.
2. L3 exact P0 vectors for every Phase 3.8.9 message/proof family remain OPEN until two independent implementations pass byte-identical JCS(P0), digest and signature-preimage vectors.
3. H's 101/101 generic I-profile run is bounded evidence and does not close per-family P0 coverage.
4. H owner-verifier callbacks remain TEST-ONLY; missing authority returns UNKNOWN.
5. I36-GOV-01..10 remain GOVERNANCE-BLOCKED; this review does not authorize Multi-PolicyDomain, Global Forget completeness, physical erasure or production activation.
6. The C profile identifier is not an I decision. C owns it; I only governs trust registration/status within I's authority.

## 6. I disposition / I 侧决议

**Delegated I-role decision: ACCEPT the exact H 1.2.13 / RecoveryJoin 1.0.2 structural carriers and I Phase 3.8.9 P0 candidate, with L3/trust/production conditions OPEN.**

This does not claim independent human approval, production keys, deployed trust registry, historical verification, anti-rollback service, runtime currentness CAS or production conformance.

**角色模拟 I 侧决议：接受 H 1.2.13 / RecoveryJoin 1.0.2 结构载体与 I Phase 3.8.9 P0 候选；L3/Trust/Production 条件仍 OPEN。** 不声称独立人类批准、生产密钥、Trust Registry、历史验证、Anti-Rollback、Runtime Currentness CAS 或生产符合性已完成。
