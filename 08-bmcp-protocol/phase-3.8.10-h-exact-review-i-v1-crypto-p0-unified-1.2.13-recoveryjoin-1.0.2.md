# Phase 3.8.10 — H Exact Review of I Crypto Profile 1.0 and P0 Allowlist Successor
# Phase 3.8.10 — H 对 I Crypto Profile 1.0 与 P0 白名单后继版本的精确审查

- Reviewer: H — BMCP Protocol / Schema and Interoperability
- Status: **ACCEPT AS I V1 ARCHITECTURE INPUT AND P0 CANDIDATE; EXACT L3 VECTORS / TRUST INTEGRATION OPEN**
- Project phase: **ARCHITECTURE DESIGN**
- I crypto profile architecture decision: Blob 56e956dca909af857469427378777705a5d1082a
- I successor P0 allowlists for H Unified 1.2.13 / RecoveryJoin 1.0.2: Blob 5c0e2049513d391dfc118f4f629a5ec95de456d6
- H Unified schema 1.2.13: Blob 8e7f6a6c9663388863db88548f9c37d0fdb1bd97
- H RecoveryJoin schema 1.0.2: Blob 4b664e3bce465499bcdfd93796349a4ba7074002
- H RecoveryCutoff schema 1.0.5: Blob 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7
- I owner snapshot membership proof source: Blob 88209bbea0ab600880c5c630cfe83af31ee16dd7
- I 1.0.1 C sequence namespace review: Blob 0d78e5b2bfcf66cae6b757314cead84b9c942601
- H predecessor I profile review Phase 3.8.8: Blob fe435d5a4cc39df76f2cbfd00e270962218cc051
- Provenance: delegated H-role review; **not an independent human H Owner signature**.

## 1. Exact I v1 profile decision / I v1 Profile 精确决议

H accepts I's v1 architecture profile baseline for I-authored protected evidence:

| Concern | Exact I v1 choice |
|---|---|
| Profile bundle | AIMBA-I-CRYPTO-1.0 |
| Canonicalization | RFC 8785 JCS constrained by RFC 7493 I-JSON |
| Canonicalization profile | RFC8785-JCS-1.0 |
| Digest | SHA-256 |
| Signature | Ed25519 / RFC 8032 |
| Signature encoding | canonical unpadded Base64url |
| Signature profile | AIMBA-ED25519-SHA256-1.0 |
| Payload domain | AIMBA-I-PAYLOAD-v1 |
| Signature domain | AIMBA-I-SIGNATURE-v1 |

The profile is I-owned and applies only to I-authored protected evidence. H resolves it only after authenticating the I authority and resolving the exact I trust registry/profile/key-status evidence. Payload-supplied algorithm labels are never authoritative.

H 接受 I 为 I-authored Protected Evidence 选择的 v1 架构基线：RFC8785 JCS（受 I-JSON 约束）、SHA-256、Ed25519、无 Padding Base64url，以及独立 Bundle/Canonicalization/Signature Profile ID 和两个域分离标签。该配置只属于 I，不得被 C/D/H/Storage/COC 继承。

## 2. Exact I P0 scope / I P0 精确范围

The current I successor P0 addendum supersedes the earlier generic/1.2.8-era projection text for the exact H 1.2.13 / RecoveryJoin 1.0.2 bundle. H accepts the P0 structure as the current candidate for:

- BMCP common-envelope signed projection, including exact schema_artifact_revision distinct from wire schema_version;
- OWNER_LOCAL_PENDING_GATE with owner_kind=I;
- OWNER_LOCAL_GATE_RELEASE with owner_kind=I;
- JF10_I_TERMINAL_DECISION_OBSERVED;
- standalone IOwnerSnapshotAttestation/1.0;
- standalone ICompleteEmptyProof/1.0 and IOutOfScopeProof/1.0;
- standalone ICommitAuthorizationReceipt/1.0 and ITerminalProof/1.0;
- RecoveryJoin 1.0.2 I owner_snapshot_membership_proofs.

H accepts the key separation:
- the COC-carried H ownerSnapshot is a summary, not the I signature object;
- owner_snapshot_attestation_ref/digest dereference the standalone I-signed IOwnerSnapshotAttestation;
- I membership proof payloads are separately signed I objects and are not interchangeable with the attestation, CompleteEmptyProof or OutOfScopeProof;
- proof_digest and external signature_ref are excluded from the I proof P0 as defined by I, and signature_ref remains an external locator;
- snapshot_digest, attestation_digest, owner_specific_high_waters_digest, proof_digest and COC record/quorum digests are distinct domains.

当前 I 后继 P0 白名单取代旧通用/1.2.8 时代的投影描述，适用于 H 1.2.13 / RecoveryJoin 1.0.2 候选。H 接受其精确消息族及对象边界：COC 携带的 ownerSnapshot 只是摘要；独立 I 签名 Attestation、Membership Proof、CompleteEmptyProof、OutOfScopeProof、AuthorizationReceipt 和 TerminalProof 均是不同对象，不能互相替代。Snapshot/Attestation/High-Water/Proof/COC 摘要均属于不同摘要域。

## 3. H 1.2.13 and RecoveryJoin 1.0.2 structural joins / H 1.2.13 与 RecoveryJoin 1.0.2 结构 Join

H confirms the exact schema bundle contains the required carrier structures:
1. Unified 1.2.13 common envelope carries schema_artifact_revision separately from wire schema_version.
2. Unified 1.2.13 ownerSnapshot uses an owner-discriminated high-water union; for I, only I's typed request/admission/receipt/inventory/registry/PermissionEpoch/Gate values are accepted.
3. owner_snapshot_attestation_digest must equal the referenced I attestation digest; the summary fields must equal the signed attestation's corresponding fields.
4. RecoveryJoin 1.0.2 carries owner_snapshot_membership_proofs as a distinct proof-payload array; the I proof is not replaced by an ownerEvidence/ownerSnapshot summary.
5. Each proof reference/digest must match the exact RecoveryJoin admission row and the separately dereferenced I-signed proof object.
6. COC quorum/record fields are outside I P0 and must be independently authenticated as COC evidence.

H 确认精确 Schema Bundle 具备所需载体：Artifact Revision 独立于 Wire Version；ownerSnapshot 使用按 Owner 区分的 High-Water Union；I Attestation Digest 与摘要字段必须精确相等；RecoveryJoin 1.0.2 的 owner_snapshot_membership_proofs 是独立 Proof Payload 数组；每个 Proof Ref/Digest 必须与 Admission Row 及 I 签名对象精确 Join；COC Quorum/Record 证据不属于 I P0，必须独立认证。

## 4. I authority and tri-state requirements / I 权威与三态要求

H may parse, validate schema closure, reconstruct the exact I P0 and orchestrate typed joins. H cannot certify I ledger completeness or issue I authorization/release.

For every I proof:
- wrong owner, purpose, schema revision, profile, audience, scope, operation or request tuple is INVALID;
- mismatched proof ref/digest, ledger entry/digest, sequence/high-water, snapshot/attestation, owner-specific high-water or anti-rollback anchor is INVALID;
- missing I verifier, incomplete pagination, unavailable ledger/snapshot, unknown/revoked key status, unavailable historical checkpoint or unavailable anti-rollback service is UNKNOWN;
- COMPLETE_EMPTY requires the separately signed ICompleteEmptyProof; an empty array or count zero is never proof of an empty set;
- I release requires a final I-local currentness CAS; H/COC cannot release I's gate.

H 可以解析、校验 Schema Closure、重建精确 I P0 并编排 Typed Join，但不能认证 I Ledger 完整性，也不能签发 I Authorization/Release。错误身份/范围/摘要/High-Water 为 INVALID；Verifier、Ledger、Snapshot、Key Status、历史 Checkpoint 或 Anti-Rollback 不可用为 UNKNOWN。空数组/零计数不能替代 COMPLETE_EMPTY 证明。I Release 必须执行 I 自己的最终当前性 CAS。

## 5. Cross-owner profile isolation finding / 跨 Owner Profile 隔离发现

The I profile decision's §6 mentions a separate C candidate name, AIMBA-C-OUTCOME-CRYPTO-1.0. The exact C-owned CSubmitOutcome 1.0.1 schema and C signature projection currently declare AIMBA-C-CRYPTO-1.0. H does not treat the I decision's C-name mention as a C-owned profile registration or override.

**Required clarification:** C must confirm whether AIMBA-C-CRYPTO-1.0 remains the C-owned profile ID for schema 1.0.1 or publish an immutable C successor changing it. I's profile decision must not rename or select a C profile. Until C publishes a different exact source and I registers the applicable trust policy, H follows the exact C schema's declared profile ID and returns UNKNOWN for unregistered profile/trust checks.

I Profile 决议 §6 提及另一个 C 候选名称 AIMBA-C-OUTCOME-CRYPTO-1.0；但当前精确 CSubmitOutcome 1.0.1 Schema 与 C Signature Projection 声明的是 AIMBA-C-CRYPTO-1.0。H 不将 I 文件中的 C 名称视为 C Owner 注册，也不允许其覆盖 C 自有 Schema。

**必须澄清：** C 应确认 1.0.1 是否继续使用 AIMBA-C-CRYPTO-1.0，或发布新的不可变 C 后继版本。I 决议不得重命名或选择 C Profile。未注册时 H 对依赖 Profile/Trust 的判定仍为 UNKNOWN。

## 6. L3 and operational evidence boundary / L3 与运维证据边界

The earlier H 101/101 run is bounded generic I-profile candidate evidence. It does not prove all exact P0 families in the current I 3.8.9 addendum.

Required L3 work:
1. Two independent implementations produce byte-identical JCS(P0), digest and signature preimage for every exact message/proof family.
2. Negative mutations cover every signed field, excluded field, null/absent distinction, owner, audience, purpose, profile, key version, PolicyDomain, scope, participant tuple and COC quorum proof.
3. Historical key status, revocation/compromise, sequence rollback, stale checkpoint, restore and incomplete-pagination cases are tested.
4. H tests the exact 1.2.13 / RecoveryJoin 1.0.2 schema blobs and records workflow run + tested commit + source/test blobs.

No new full per-family P0 vector execution is claimed here. I profile architecture approval is not production activation, HSM/KMS custody, regulatory/FIPS approval, deployed trust registry or anti-rollback service.

此前 H 101/101 运行仅是通用 I Profile 候选证据，不证明当前 I 3.8.9 的每个精确 P0 消息/Proof Family。L3 仍需双实现逐族字节一致向量、全字段负向变异、历史 Key Status/Revocation/Rollback/Restore 测试，并绑定精确 1.2.13/RecoveryJoin1.0.2 的 CI。本文不声称新 P0 向量已执行，也不代表生产激活、HSM/KMS、监管/FIPS、Trust Registry 或 Anti-Rollback 已部署。

## 7. H disposition / H 侧决议

**Delegated H-role decision: ACCEPT AS NORMATIVE I V1 ARCHITECTURE INPUT AND CURRENT P0 MAPPING CANDIDATE; L3 / TRUST / PRODUCTION GATES REMAIN OPEN.**

The I profile and exact P0 allowlist are accepted as I-owned architecture inputs for H mapping. The cross-owner C profile naming discrepancy in §5 is referred to C/I for explicit disposition. No H production validator, I trust root, key registry, owner ledger verifier, COC quorum or deployment-grade RecoveryJoin is claimed.

**角色模拟 H 侧决议：接受为 I v1 架构输入及当前 P0 映射候选；L3/Trust/Production 门禁仍 OPEN。** 第 5 节 C Profile 名称差异交由 C/I 明确裁决。未声称 H 生产 Validator、I Trust Root/Key Registry、Owner Ledger Verifier、COC Quorum 或部署级 RecoveryJoin 已完成。
