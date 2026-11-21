# G Owner — 精确 JF-10 Prepared Participant Identity / GID Applied-Evidence 验收

- Storage protocol §14 Blob：`86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A integration mapping Blob：`a71251704851cacd15f67faa985a5bd50057e92a`
- B typed-reference registry Blob：`b5a169a1f2c2e6db4b7c8f96b127af971ff53f1f`
- H BMCP schema 1.1.1 candidate Blob：`c0bbfc7611a8d88a39cee209831db32b62601fde`
- 决策：**ACCEPT WITH G-OWNED FULL APPLIED / CURRENT-USE CONDITIONS**
- 模式：按照用户指示进行的委派式 G 边界评审；不是独立的人类签署。

G 接受精确的 participant identity tuple，作为 Full Applied proof 所消费的 Storage 证据：

1. Full Applied 绑定 `PreparedParticipantRef` + `PreparedTransactionGID` + `EngineNativeTransactionXIDRef` + CanonicalAuthorityDBRef + PostgreSQL system/database identity + original prepare timeline/LSN + participant digest + PublicationOperationId/RequestDigest + owner boundary + COC intent position/digest + Storage signer/key version/audience。
2. PreparedParticipantRef/GID 是稳定的 identity/handle；native XID 只是观察到的证据。两者均不能单独证明 publication 或 Applied。
3. Full Applied 仍要求 CSubmitOutcome、有效的 H envelope/ACK、I terminal authorization/receipt consumption、D complete-lineage barrier/clearance、Storage same-GID terminal resolution，以及 atomic VisibilityPointer/PublicationReceipt proof；所有这些都必须绑定到同一不可变 tuple。
4. COMMITTED Storage proof 必须标识精确的 VisibilityPointer 和 PublicationReceipt transaction/digest。ROLLED_BACK proof 必须确立 non-publication。Prepared-but-unresolved、GID absent without durable outcome、missing WAL、conflicting native XID 或 stale database identity 均仍为 UNKNOWN/IN_DOUBT。
5. COC commit position 和 PreparedTransactionGID/native XID 不可与 I sequencer position、D fence generation、G ContextVersion 或 delivery cursor 互换。
6. 只有当原始完整 proof 有效时，历史 Applied 才不可变。Current-use 仍须单独受当前 Context head、I PermissionEpoch、D ForgetFence、Scope/Environment、session 和 capability 控制。

例外：G Applied validator/persistence 和集成的 COC/Storage proof lookup 尚未实现/验证；G-CO race suites 仍为 NOT RUN。这只是设计验收，不代表 Global Forget completion。
