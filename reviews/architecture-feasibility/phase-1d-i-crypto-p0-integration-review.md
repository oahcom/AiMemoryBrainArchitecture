# Phase 3.8.7–3.8.8 — A Integration Review: I Crypto Profile, P0 Allowlists and Snapshot Attestation
# Phase 3.8.7–3.8.8 — A 集成审查：I Crypto Profile、P0 白名单与 Snapshot Attestation

- Reviewer: A — Principal Integration Architect
- Branch: `session-a-integration-2026-11-16`
- I v1 crypto decision: Blob `56e956dca909af857469427378777705a5d1082a`
- I exact P0 addendum: Blob `739dc15e3cca33aef3f012f713b988e5528d4ad9`
- H owner snapshot attestation schema 1.0.0: Blob `ecf9971b089ca5fab9a92915663dc913c8ab1ba6`
- H P0/schema review: Blob `b03a99943b374103bae3e599c68cb2cd97a561ca`
- I snapshot schema review: Blob `1520d3fc8c36c57f87b0a75ff7cb6c432649a8e9`
- H v1 crypto architecture review: Blob `fe435d5a4cc39df76f2cbfd00e270962218cc051`
- H unified schema 1.2.8: Blob `70b892797d07489936300a26c0dedfafe1d6e746`
- Decision: **ACCEPT AS NORMATIVE I V1 CRYPTO ARCHITECTURE; L2 FIELD CONTRACT CLOSED; L3 FAMILY VECTORS OPEN**
- English and Chinese are normative peers.

## 1. Exact Owner review bundle / Owner 精确审查包

A re-read the exact I/H review artifacts from their respective branches. I has selected the v1 algorithm suite; H accepts it as the normative I wire/crypto architecture input. H and I have accepted the exact P0 field lists and the standalone owner snapshot attestation structure with enumerated conditions.

A 已从各 Owner 分支重新读取精确 I/H 审查工件。I 已选择 v1 算法套件；H 接受其作为规范 I Wire/Crypto 架构输入。H 与 I 已接受精确 P0 字段清单和独立 Owner Snapshot Attestation 结构，并保留明确条件。

## 2. Architecture decision / 架构决策

I v1 suite is:
- RFC 8785 JCS constrained by RFC 7493 I-JSON;
- SHA-256;
- Ed25519 / RFC 8032;
- canonical unpadded Base64url;
- separate profile bundle, canonicalization profile and signature profile IDs;
- exact message-family domain separation and P0 projections.

I's exact P0 projections now exist for:
- OWNER_LOCAL_PENDING_GATE (owner_kind=I);
- OWNER_LOCAL_GATE_RELEASE (owner_kind=I);
- JF10_I_TERMINAL_DECISION_OBSERVED;
- IOwnerSnapshotAttestation/1.0;
- ICompleteEmptyProof/1.0;
- IOutOfScopeProof/1.0;
- ICommitAuthorizationReceipt/1.0;
- ITerminalProof/1.0.

H's 1.2.8 outer ownerSnapshot remains a COC-carried summary. It must exactly join to the separate I-signed attestation ref/digest. Snapshot digest and attestation digest are distinct.

I v1 算法套件与精确 P0 已确定。H 1.2.8 外层 OwnerSnapshot 只是 COC 携带的摘要，必须与独立 I 签名 Attestation 的 Ref/Digest 精确 Join；Snapshot Digest 与 Attestation Digest 不同。

## 3. L2 disposition / L2 裁决

The previous generic P0 wording and missing I owner snapshot attestation shape are resolved at the architecture/contract level by the exact I addendum and H schema. The owner authority remains a typed opaque reference and must be resolved by I; it is not the literal string “I”.

The optional `owner_snapshot_attestation_digest` in the backward-compatible 1.2.8 structural schema is mandatory for protected I RecoveryCutoff records under semantic validation. Complete-empty refs must agree with exact count and pagination state. COC quorum remains an independent proof.

此前泛化 P0 表述和 I Owner Snapshot Attestation 结构缺失，已由精确 I 补充和 H Schema 在架构/合同层解决。Owner Authority 保持类型化不透明引用，由 I 解析，不能把字符串 “I” 当成身份权威。

1.2.8 为兼容性保留的可选 `owner_snapshot_attestation_digest`，在受保护 I RecoveryCutoff 记录的语义验证中必须强制要求。Complete-empty Ref 必须与 Count/Pagination 状态一致。COC Quorum 是独立证明。

## 4. L3 residuals / L3 遗留

The H 101/101 CI is bounded candidate evidence and does not prove every exact I P0 family. L3 remains OPEN for:
- two independent implementations for every listed I message/proof family;
- exact JCS bytes/digest/signature-preimage comparisons;
- nested I snapshot/empty/out-of-scope proof verification;
- key rotation/retirement/revocation/compromise and historical checkpoint vectors;
- anti-rollback and restore gap/fork vectors;
- owner snapshot summary mismatch and pagination/high-water counterexamples.

No production HSM/KMS, live key registry, sequencer deployment or database integration is required to complete these abstract reference-model vectors.

H 101/101 仅是有限候选证据，未证明每个 I P0 消息族。逐消息族双实现向量、Key Lifecycle、Historical Checkpoint、Anti-rollback、Restore、Snapshot Summary Mismatch 和 Pagination/High-water 反例仍属于 L3 OPEN。完成抽象参考向量不要求生产 HSM/KMS、实时 Key Registry、Sequencer 部署或数据库集成。

## 5. Final A disposition / A 最终结论

**ACCEPT AS NORMATIVE I V1 CRYPTO ARCHITECTURE; L2 FIELD CONTRACT CLOSED; L3 FAMILY VECTORS OPEN.**

I's v1 algorithm choice and exact P0 contract are no longer undecided architecture items. Production key custody, HSM/KMS, live registry, operational anti-rollback and regulatory suitability remain L4/governance. The full system architecture freeze remains pending other L1/L2/L3 domains.

**接受为规范 I v1 Crypto 架构；L2 字段合同已闭环；L3 逐消息族向量仍 OPEN。** I v1 算法选择和精确 P0 合同不再是未决架构事项。生产 Key Custody、HSM/KMS、实时 Registry、运维 Anti-rollback 和监管适用性属于 L4/治理。全系统架构冻结仍取决于其他 L1/L2/L3 领域。
