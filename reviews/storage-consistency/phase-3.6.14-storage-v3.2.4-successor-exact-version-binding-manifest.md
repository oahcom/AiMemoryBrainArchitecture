# Phase 3.6.14 — Storage v3.2.4 Successor Exact-Version Binding Manifest
# Phase 3.6.14 — Storage v3.2.4 后继精确版本绑定清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **SUCCESSOR REVIEW BUNDLE PUBLISHED / NOT JOINTLY ACCEPTED / NOT FROZEN**
- Purpose: supersede stale cross-owner pins in Storage v3.2.3 §§21.1–21.5 without silently changing its normative S0a–S4 protocol.
- Normative Storage base: reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.3.md, Blob 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792.
- Predecessor audit: reviews/storage-consistency/phase-3.6.9-storage-v3.2.3-currentness-and-exact-review-gate-audit.md, Blob 15fd59b306a20e65aaafca156ca60736f6bc1b00.
- Provenance: delegated Storage-role coordination artifact authored in this ChatGPT session; NOT an independent Storage Owner signature.

## 1. Decision and scope / 决议与范围

This file is the successor v3.2.4 exact-version binding manifest. It is not a claim that the entire Storage technical design has been rewritten as a new normative v3.2.4 protocol. Storage v3.2.3 remains the normative technical body. This manifest supersedes only its stale exact-version review pins and adds the latest owner-owned source and review artifacts required for a common successor review bundle.

本文件是 v3.2.4 后继精确版本绑定清单，并不声称 Storage 技术设计正文已整体改写为新的规范协议。Storage v3.2.3 仍是规范技术正文。本清单只替换过时的精确版本审查绑定，并补充共同复审所需的最新 Owner 源文件与审查工件。

A referenced Blob is an immutable source identity. A path or branch name alone is not a binding. A changed Blob invalidates the affected review and requires a new exact-version decision. No earlier decision transfers automatically to a changed Storage, C, H, I or D Blob.

引用的 Blob 是不可变源身份。仅有路径或分支名不构成绑定。Blob 变化会使受影响的审查失效，必须重新进行精确版本决议。任何旧版本决议均不得自动转移到变更后的 Storage、C、H、I 或 D Blob。

## 2. Normative Storage and COC base / Storage 与 COC 规范基线

| Authority | Path | Exact Blob | Binding role |
|---|---|---|---|
| Storage | reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.2.3.md | 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 | Normative Storage body; S0a–S4, participant union, JF-10 bridge and Storage evidence boundary |
| COC | reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v3.md | 5b950a3a29bd7a5276b92a49a9114d700718b987 | COC §§15–17 companion: two-record order, digest chain and union manifest |
| Storage | reviews/storage-consistency/phase-3.6.4-storage-two-phase-batch-manifest-ordering-amendment.md | 9704d110a06d0c2ee98be960054e0396d0b68546 | Digest separation and Batch-before-Manifest ordering |
| Storage | reviews/storage-consistency/phase-3.6.13-storage-r1-r2-batch-round-and-owner-release-ordering-addendum.md | 0477f0329997e42a1cbf6ecb8127c5c01fa47051 | Immutable RecoveryRound, successor-round handling and owner-local release order |
| Storage | reviews/storage-consistency/phase-3.6.9-storage-v3.2.3-currentness-and-exact-review-gate-audit.md | 15fd59b306a20e65aaafca156ca60736f6bc1b00 | Predecessor audit motivating this successor binding |

The v3.2.3 S0a–S4 ordering is preserved:
1. I/D/C close their own gates and freeze their own request and admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Construct the complete canonical union of COC participants at/before P and applicable I/D/C owner-local admissions through their own frozen high-waters.
4. Commit the immutable Recovery Cutoff Batch.
5. Commit the distinct Participant Manifest record strictly after the Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then begin participant reconciliation. Owner release remains independently owner-authoritative.

S0a–S4 的语义与顺序不因本清单改变。Batch 与 Manifest 仍是两个独立、不可变、按序提交的记录；COC 不得代替 I/D/C 签发 Owner Gate Release。

## 3. I — Security and Governance exact source set / I 安全与治理精确源集合

| Artifact | Path | Exact Blob | Status and scope |
|---|---|---|---|
| I R1/R2 disposition | 09-security-governance/phase-3.6.9-i-r1-r2-exact-version-delegated-disposition.md | 6bf56407721f1271f315d799f9bd57055393c176 | ACCEPT WITH ENUMERATED AMENDMENTS; delegated simulation, not independent signature |
| I recovery-cutoff rereview | 09-security-governance/phase-3.6.10-i-exact-version-recovery-cutoff-review.md | a0fee9ef41c52ea3948286e6ec9a348cc1b17168 | ACCEPT WITH ENUMERATED AMENDMENTS; older bundle, not approval of this successor |
| I owner-local gate amendment | 09-security-governance/phase-3.6.7-i-owner-local-gate-admission-release-amendment.md | 0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7 | I-owned gate close, request capture, high-water and independent release |
| I global inventory/currentness amendment | 09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md | cf4b76f151204fa47b156b5d807e7378c28fd268 | Inventory epoch, registry digest, TargetInventorySeal and restore currentness |
| I authorization sequencer contract | 09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md | 54bab0484bd232a5a258e65e34cc7425288b39a6 | Authorization receipt, revocation order and one-time consumption |
| I membership proof contract | 09-security-governance/phase-3.8.4-i-owner-snapshot-membership-proof-contract.md | 88209bbea0ab600880c5c630cfe83af31ee16dd7 | Candidate I proof P0 and owner-ledger/snapshot membership |
| I R1/R2 candidate | 09-security-governance/phase-3.6-r1-r2-i-owner-gate-linearization-decision-candidate.md | 57ef6c4352d79577ae53a77895f73bce434c5fca | Owner-local candidate source; not independent approval |

I owns PermissionEpoch, PolicyDomain request/receipt issue/consume ledgers, revocation ordering, ProducerDomainInventoryEpoch, registry snapshot/digest, relevant entry generations, TargetInventorySeal, I GateGeneration and I release. I request completeness and global inventory completeness are distinct proof domains. I release requires a fresh I-local currentness CAS against the exact frozen Batch/Manifest, I high-waters/roots, scope, key status and anti-rollback anchor. I counters are never compared numerically with D/C/COC counters.

I 的权限、撤销、Receipt 签发/消费、全局 Producer Inventory、TargetInventorySeal 和 Gate Release 均由 I 自己负责。请求账本完整性与全局 Inventory 完整性是两个独立证明域。I Release 必须在最终线性化点重新验证当前性；不得跨 Owner 比较计数器。

I status: the listed decisions are delegated simulations and the proof/profile contracts are candidates. They are not independent Owner approval, production cryptographic profile registration, durable sequencer proof or conformance. The I proof contract's historical H Unified 1.2.11 reference is superseded as a wire binding by §6; I must confirm mapping to H 1.2.12 without changing I's P0 authority.

## 4. D — Memory Brain / Forget exact source set / D 记忆大脑与 Forget 精确源集合

| Artifact | Path | Exact Blob | Status and scope |
|---|---|---|---|
| D R1/R2 disposition | 03-memory-brain/phase-3.6.9-d-r1-r2-exact-version-delegated-disposition.md | 7ab4f53c497bce597e422a6df9a85b31a2352602 | ACCEPT WITH ENUMERATED AMENDMENTS; delegated simulation, not independent signature |
| D recovery-cutoff rereview | 03-memory-brain/phase-3.6.10-d-exact-version-recovery-cutoff-review.md | e03ca0db209fc8ac5b985e114a31c21fbb136859 | ACCEPT WITH ENUMERATED AMENDMENTS; older bundle, not approval of this successor |
| D owner-local gate amendment | 03-memory-brain/phase-3.6.7-d-owner-local-gate-admission-release-amendment.md | 84f6875ce382fb37f35b01140c19a482fcfa9fab | Fence close, admission inventory, post-high-water suppression and release |
| D fencing/terminalization amendment | 03-memory-brain/phase-3.6.8-d-cross-boundary-fencing-terminalization-amendment.md | 2d95099a2e19a8cbec325925b70da576f73d9899 | D lineage/barrier/fencing source |
| D publication participant contract | 03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md | 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 | D publication participant and terminal evidence |
| D membership proof contract | 03-memory-brain/phase-3.8.4-d-owner-snapshot-membership-proof-contract.md | d80dabe7210e681bc4e2290355a38f8b67be9ddd | Candidate D proof for producer/work/attempt/derivative/barrier rows |
| D R1/R2 candidate | 03-memory-brain/phase-3.6-r1-r2-d-owner-gate-linearization-decision-candidate.md | a7cba2c72720bb7873d77f1a9d151df974605a9e | Owner-local candidate source; not independent approval |

D owns ForgetOperationRef, ForgetFenceGeneration, producer registration, WorkItem/Attempt/Derivative membership, lineage closure, barrier terminalization and D Gate Release. D snapshots bind distinct request and admission/work/attempt high-waters and roots, exact scope/lineage, and the relevant I inventory projection. Every effect boundary—including producer registration, queue/lease, worker/retry/replay, derivative creation, restore replay and final publication—must check current D FenceGeneration. A late-discovered pre-fence item reopens the barrier; post-fence work cannot publish and must be rejected or quarantined.

D 的 Fence、Producer/Work/Attempt/Derivative、Lineage、Barrier 与 Release 均由 D 自己负责。所有实际效果边界必须检查当前 FenceGeneration。迟发现的 Fence 前工作必须重新打开 Barrier；Fence 后工作不得发布。

D status: prior dispositions are delegated simulations against earlier bundle versions. D proof and publication contracts remain proposals pending independent D approval and executable conformance. The D proof contract's historical H Unified 1.2.11 reference is superseded as a wire binding by §6; D must confirm mapping to H 1.2.12 without transferring D ledger authority to H.

## 5. C — Agent Integration / Provider Egress exact source set / C Agent 集成与 Provider Egress 精确源集合

| Artifact | Path | Exact Blob | Status and scope |
|---|---|---|---|
| C exact review of Storage v3.2.3 | 07-agent-integration/phase-3.6.8.3-c-provider-outcome-storage-v3.2.3-union-manifest-exact-review.md | ef324fe5484f72adf17cc00f9c443e944f8a5c48 | ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS; delegated simulation, limited to then-bound bundle |
| C Provider Outcome owner-binding decision | 07-agent-integration/phase-3.8.4-c-provider-outcome-exact-owner-binding-decision.md | 1353572f7d5655e3007b2fb5b3f10066f483e6bb | C semantic authority and canonical source composition; delegated role decision |
| C final-request evidence | 07-agent-integration/phase-3.6-final-request-evidence-contract.md | fd2f47ba6c89bb270e9f2bec956873cb7ae3592b | Immutable final request identity and boundary |
| C causal submit contract | 07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md | 45a48249717c8cddb07ab96197730ef93d406c22 | CSubmitOutcome ownership and I/D/COC ordering |
| C owner-local admission/recovery amendment | 07-agent-integration/phase-3.6.9-c-owner-local-admission-gate-recovery-release-amendment.md | 9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb | C admission ledger, gate close, attempt and recovery release |
| C transport-owning egress adapter | 07-agent-integration/provider-egress-gate-adapter-contract.md | a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca | Final durable CAS immediately before transport handoff |
| CSubmitOutcome schema/conformance contract | 07-agent-integration/phase-3.8.9-c-submit-outcome-1.0.0-schema-and-conformance-contract.md | 2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac | Current contract text; contains stale H 1.2.11 references that block 1.2.12 compatibility acceptance |
| C R1/R2 candidate | 07-agent-integration/phase-3.6-r1-r2-c-owner-gate-linearization-decision-candidate.md | 5c37ebea98436fc985a94f17063b50b4df7ad7a6 | Owner-local candidate source; not independent approval |
| C Provider Egress exact review | 07-agent-integration/phase-3.8.3-c-provider-egress-gate-exact-review.md | 5a27f79087d3a5e01dd23e818d8c7ea0fdb61d1d | Exact review of C Adapter contract; delegated review |
| C Provider Outcome recovery review | 07-agent-integration/phase-3.6.11-c-exact-version-provider-outcome-recovery-review.md | 19519a9dabe8aea66897c01493ab5b65ed8af4aa | Recovery/Provider Outcome review; scoped to older H schema and older Storage bundle |
| C RecoveryJoin/provider side-effect review | 07-agent-integration/phase-3.8.2-c-recovery-join-provider-side-effect-exact-review.md | a7b57bd5531222559666f0f1d9df59a259cde61a | C-owned provider-side-effect boundary; amendments remain open |
| C membership proof contract | 07-agent-integration/phase-3.8.4-c-owner-snapshot-membership-proof-contract.md | 5e37185610869951c3b392c9ad143a72b4c702ac | Candidate C-owned admission/attempt/outcome snapshot proof |
| C review of H membership proof | 07-agent-integration/phase-3.8.4-c-exact-review-h-owner-membership-proof.md | ea2e11519646225679eadc8b33af0d755998d92e | Conditional C-role review against H 1.2.11-era bundle |
| C gate/attempt/idempotency amendment | 07-agent-integration/phase-3.8.6-c-provider-outcome-gate-attempt-idempotency-amendment.md | 392a3fd43790db59cb8aa5b3c919ca98e4bcddb4 | Immutable attempt tuple and shared gate/send serialization; references H 1.2.11 |
| C crypto profile review | 07-agent-integration/phase-3.8.7-c-review-of-i-c-crypto-profile-proposal.md | 794d1dc49f034152407e3a42ba5ac937ea3539f8 | Candidate construction accepted only; profile registration/trust/wire freeze OPEN |
| C signature projection | 07-agent-integration/phase-3.8.8-c-provider-outcome-signature-projection.md | 06d9264124d85896ccd44ef7789d9af245d8255b | C-owned P0 projection; requires exact H mapping and I profile registration |
| C SubmitOutcome JSON Schema | 07-agent-integration/schemas/c-submit-outcome-1.0.0.schema.json | b5e87fa8df8463cf4cdc1ebc6867e643dcf5924c | Immutable C object structural schema |
| C outcome vectors | 07-agent-integration/tests/conformance/provider_outcome/c_submit_outcome_1_0_0_vectors.json | b4c32dc8cd7072a04843c2db74c7f96c6de001a4 | Synthetic fixtures; signatures are placeholders |
| C structural/semantic test | 07-agent-integration/tests/conformance/provider_outcome/test_c_submit_outcome_1_0_0.py | 92e8e9e607566eafa6ad89110202dbeed0fc43cb | Bounded schema/semantic test; not provider or crypto certification |
| C crypto vector manifest | 07-agent-integration/tests/conformance/provider_outcome/c_crypto_profile_vector.json | 88a16f0d9aaa8a5e46af857c2cd34c2bcedd07ae | TEST-ONLY candidate vectors; public deterministic seed must never be reused |
| C expected crypto vectors | 07-agent-integration/tests/conformance/provider_outcome/c_crypto_profile_expected_vectors.json | a4bfe0b431d5e710ac99d604e7b1bce49c044d23 | TEST-ONLY expected fingerprints/signatures |
| C Python crypto tests | 07-agent-integration/tests/conformance/provider_outcome/test_c_crypto_profile.py | 2e1f572facc644c378ee1880a553c27a72ed2cc4 | Candidate Ed25519/JCS test implementation |
| C Node crypto oracle | 07-agent-integration/tests/conformance/provider_outcome/c_crypto_profile_reference.mjs | 31c8ac889766f9574725357ae6134a901bfb5f33 | Independent TEST-ONLY Node oracle |
| C test dependency pins | 07-agent-integration/tests/conformance/provider_outcome/requirements.txt | 305d9bf5ae883a16e22dde83d97005f2b0be902e | Test dependencies only |

C mandatory rule: the transport-owning C Adapter is the final side-effect boundary. C final egress CAS must validate current CGateGeneration, exact C admission/request digest, COC reservation, I COMMIT_WON for the exact operation, D clearance/current Fence, and one-use ProviderAttemptRef. Only that CAS winner may invoke the bound transport. UNKNOWN/IN_DOUBT remains blocking; ambiguous handoff requires same-key provider lookup. No COC or H record may synthesize C provider truth.

C 的强制规则：最终发送边界由实际持有 Provider Transport 的 Adapter 控制。最终 CAS 必须验证当前 C Gate、精确请求摘要、COC Reservation、同一操作的 I COMMIT_WON、D Clearance/当前 Fence 及一次性 ProviderAttempt。只有 CAS 胜者可调用 Transport。UNKNOWN/IN_DOUBT 必须阻塞。

C status: the delegated v3.2.3 review is bounded evidence but predates the complete current C source composition and H 1.2.12 wire binding. It does not approve this successor bundle. Provider-specific idempotency, actual adapter implementation, multi-replica serialization and race/fault execution remain OPEN.

## 6. H — BMCP Protocol / exact wire and schema set / H 协议与 Schema 精确集合

| Artifact | Path | Exact Blob | Binding role |
|---|---|---|---|
| H Unified COC/JF-10/Provider schema 1.2.12 | 08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.12.schema.json | a54f66914a819d77f00c6af04e76453ff9f654ee | Current unified structural schema; artifact revision 1.2.12, declared wire family version 1.3.0 |
| H RecoveryJoin schema 1.0.2 | 08-bmcp-protocol/schemas/bmcp.recovery-join-1.0.2.schema.json | 4b664e3bce465499bcdfd93796349a4ba7074002 | Owner snapshot membership proof envelope and join structure |
| H RecoveryCutoff schema 1.0.5 | 08-bmcp-protocol/schemas/bmcp.recovery-cutoff-1.0.5.schema.json | 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7 | Recovery cutoff companion structural family |
| H R1/R2 wire crosswalk | 08-bmcp-protocol/phase-3.8.6-h-r1-r2-owner-gate-wire-crosswalk.md | 8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c | Record-family mapping to Unified 1.2.12 / RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 |
| H owner-authority verifier adapter contract | 08-bmcp-protocol/phase-3.8.5-h-owner-authority-membership-verifier-adapter-contract.md | 5b462c79082a27b64a03f9c8b6da1d4e93075b89 | H structural/tri-state interface; I/D/C retain authority |
| H semantic reference helper | 08-bmcp-protocol/runtime_reference/unified_manifest_semantics.py | e26379d38825ee13d15f652d3bd019c4091da37d | TEST-ONLY helper; injected owner verifier callback is not production trust |
| H RecoveryJoin 1.0.2 tests | 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_recovery_join_1_0_2.py | 3c61cc8c9d973a27f890e1452305e3fb0ad09f1a | Bounded tests for VALID/INVALID/UNKNOWN mapping |
| H I cross-language vector | 08-bmcp-protocol/tests/conformance/recovery_cutoff/i_admission_snapshot_membership_proof_vectors.json | 9210219a85afe1f48da0ea253a073aba8b2e138c | TEST-ONLY Python/Node vector |
| H I cross-language test source | 08-bmcp-protocol/tests/conformance/recovery_cutoff/test_i_admission_snapshot_membership_proof_cross_language.py | 01239e06e8f4464f49acd34241dc00899befe424 | TEST-ONLY Python/Node vector harness |

H exact-head workflow evidence: run 44051851164 on commit ba99eea9334d77c2a014ed45d9287ef514a4d895; 288 total, 266 passed, 22 skipped, 0 failed. The 22 skipped are superseded historical 1.2.10 semantic fixtures and are not counted as passed. This is bounded H branch CI evidence only; it does not prove production owner verifiers, production signatures, complete owner-ledger enumeration, quorum durability or gate linearization.

H owns wire shape, exact typed joins, canonical field mapping, versioning and interoperability. I/D/C own their proof P0, signing profile, key status, ledger completeness and anti-rollback. The current H verifier is only an interface/reference helper. Missing verifier, timeout, incomplete pagination, unavailable key status or unknown profile MUST map to UNKNOWN, never VALID.

H 负责 Wire、Typed Join、字段映射、版本与互操作；I/D/C 分别负责自己的证明 P0、签名配置、Key Status、账本完整性和 Anti-Rollback。当前 H Verifier 仍只是接口/参考实现，不能冒充生产验证器。证据缺失必须返回 UNKNOWN。

## 7. C/H compatibility blocker / C/H 兼容性阻断项

The current C Provider Outcome contract set (Phase 3.8.6 amendment Blob 392a3fd43790db59cb8aa5b3c919ca98e4bcddb4, Phase 3.8.7 review Blob 794d1dc49f034152407e3a42ba5ac937ea3539f8, Phase 3.8.8 projection Blob 06d9264124d85896ccd44ef7789d9af245d8255b, and Phase 3.8.9 contract Blob 2ecdf44cae1bf71e9611dd5367c8f7bcf25dd7ac) explicitly references H Unified 1.2.11. C's Phase 3.8.5 cross-review also accepted only structural elements of H 1.2.11 and explicitly left semantic/wire freeze blocked. H 1.2.12 must not be treated as a compatible drop-in until C publishes an exact amendment covering the actual schema fields, CSubmitOutcome dereference, duplicated-field equality, C GateGeneration/ProviderAttempt identity, signature projection/profile and negative vectors, and H publishes matching schema/validator cross-review. The prior H 1.2.11 cross-review does not satisfy this requirement.

当前 C Provider Outcome 合同仍明确引用 H Unified 1.2.11；C 对 H 1.2.11 的旧交叉审查也只作结构性条件接受，并明确语义与 Wire Freeze 尚未通过。不得将 H 1.2.12 默认为兼容替代版本。C 必须发布精确修订，覆盖字段、CSubmitOutcome 解引用、重复字段一致性、GateGeneration/ProviderAttempt、签名投影/配置和负向向量；H 必须对修订后的精确 Schema/Validator 再审。旧版 1.2.11 审查不能替代该工作。

## 8. Currentness correction and superseded pins / 当前性纠正与废止绑定

The following pins in Storage v3.2.3 §§21.1–21.5 are superseded for the successor review bundle:

| Old v3.2.3 pin | Successor binding |
|---|---|
| H Unified schema 1.2.5, Blob 164ec3c436558d5d93032edc51e127d15e03db4 | H Unified schema 1.2.12, Blob a54f66914a819d77f00c6af04e76453ff9f654ee |
| Older recovery schema references | RecoveryCutoff 1.0.5 Blob 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7 and RecoveryJoin 1.0.2 Blob 4b664e3bce465499bcdfd93796349a4ba7074002 |
| C Provider Outcome v3.2-era source only, Blob f538d921d06c92dfaba13fbe326a80d6550fe1b7 | Complete C source set in §5, including C local admission/recovery, concrete egress Adapter and CSubmitOutcome object schema |
| I/D Phase 3.6.8 sources as sole owner binding | Current I/D source sets in §§3–4; earlier decisions remain scoped to their old bundle |

No superseded Blob is deleted or rewritten. It remains historical review evidence only.

## 9. Cross-owner semantic joins required for review / 跨 Owner 语义 Join 审查要求

C, H, I and D must review these exact joins:

1. Union membership: every applicable I/D/C admission through its owner-specific frozen high-water appears exactly once, either joined to a COC participant or as an owner-local admission. No fabricated ParticipantIntentRef; no empty-by-omission.
2. Distinct owner proof: each row carries the issuing owner's exact membership proof; proof identity, ledger/version/entry, sequence/high-water, root, snapshot/attestation, gate generation, scope, operation/request digest and anti-rollback/key-status bind to the frozen owner snapshot.
3. Tri-state semantics: H maps owner authority result to VALID/INVALID/UNKNOWN. Missing production verifier remains UNKNOWN. Schema-valid is not a completeness proof.
4. I/C authorization join: C provider egress requires I's exact COMMIT_WON terminal proof for the same operation/digest and valid single-use consumption; revocation-won, indeterminate, missing or mismatched proof blocks send.
5. D/C fence join: C final egress and D publication validate exact D participant/clearance and current FenceGeneration; D and I counters are not compared.
6. Storage ordering: immutable RecoveryRound; Batch quorum commit before Manifest quorum commit; exact Batch backlink; linearizable readback; post-snapshot advances require a successor round; owner release is signed and issued only by that owner.
7. Restore: start fenced; replay current I/D/C controls independently; verify anti-rollback and owner snapshots; reconcile COC participants and owner-local admissions; no serving or provider invocation before all required owner releases and COC completion predicates.

## 10. Exact review and adoption matrix / 精确复审与采纳矩阵

| Owner | Current evidence | Required action on this exact manifest |
|---|---|---|
| Storage | This manifest + v3.2.3 technical body | Confirm bundle completeness; issue successor only if a pinned Blob changes |
| I | R1/R2 disposition, cutoff review, gate/authority/proof sources | Fresh I exact-version review; confirm H 1.2.12 mapping and preserve I currentness/crypto boundaries |
| D | R1/R2 disposition, cutoff review, gate/publication/proof sources | Fresh D exact-version review; confirm H 1.2.12 mapping and preserve D barrier/lineage/fence boundaries |
| C | v3.2.3 exact review, Provider Outcome decision and complete C source set | Fresh C exact-version review; confirm final egress CAS and CSubmitOutcome wire/object mapping |
| H | Unified 1.2.12, RecoveryJoin 1.0.2, RecoveryCutoff 1.0.5, crosswalk and verifier contract | Fresh H exact-version review; confirm requiredness, joins, semantic mapping and UNKNOWN behavior |
| A | Prior R1/R2 candidate integration simulation | Fresh A integration review after I/D/C/H publish exact decisions against this same manifest |

Existing I/D/C/A review artifacts are delegated role simulations, not independent human Owner signatures. This manifest does not impersonate such signatures. Any amended source must be pinned by a new manifest revision and reviewed again by affected Owners.

现有 I/D/C/A 审查工件均为协调会话中的角色模拟，不是真正独立 Owner 签署。本清单不冒充独立批准。任何源文件发生变化，都必须更新精确绑定并由受影响 Owner 重新审查。

## 11. Gate state and non-claims / Gate 状态与非声明

- Storage Gate A architecture: CONDITIONAL PASS within documented design scope; deployment, operations and production durability remain separate evidence gates.
- Gate B COC persistence: BLOCKED pending Gate A acceptance and actual deployment binding.
- Gate C executable end-to-end implementation fault injection: DEFERRED_TO_ENGINEERING_PHASE / NOT RUN.
- R1 Recovery Cutoff Batch completeness: OPEN.
- R2 owner-local gate linearization/release: OPEN.
- JF-10 P0: OPEN.
- Multi-PolicyDomain atomicity: BLOCKED.
- Production activation: NOT AUTHORIZED.

本清单不声称存在生产 Owner 签名、已部署 COC quorum、真实 I/D/C sequencer CAS、生产 Membership Verifier、Provider 认证、通用 exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 12. Required next sequence / 后续执行顺序

1. I and D independently review this exact manifest and publish their own exact-Blob decisions on their own branches.
2. C reviews the exact C source set and H 1.2.12 mapping, then publishes its exact-Blob decision.
3. H reviews the same manifest and all H schemas/semantic references in §6, then publishes its exact-Blob decision.
4. Storage updates only this manifest if any source Blob changes; never silently float a branch ref.
5. A reviews the exact same manifest plus all four fresh I/D/C/H decisions and publishes a new integration disposition.
6. Keep Issue #14 R1/R2 and JF-10 P0 open until acceptance predicates and implementation/deployment gates are actually met.

## 13. Provenance / 来源说明

This manifest was authored by the coordinating session in delegated Storage-role mode. All listed Blob IDs were read from the named owner branches or exact file readbacks during this run. It is a version-binding and review-routing artifact, not an independent Storage Owner signature. No implementation files, schemas or runtime code were changed by this manifest.

本清单由协调会话模拟 Storage 角色编写。所有 Blob 均在本轮从指定 Owner 分支或精确文件读回中核验。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名。本轮未修改实现文件、Schema 或 Runtime 代码。
