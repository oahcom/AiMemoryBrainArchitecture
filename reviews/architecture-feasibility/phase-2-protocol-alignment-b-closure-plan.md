# ARCH-CONSOL-002 — B: Cross-Owner Protocol Alignment Review
# ARCH-CONSOL-002 — B：跨 Owner 协议精确对齐审查

- Repository: oahcom/AiMemoryBrainArchitecture
- Scope: C / H / D / I / Storage exact Provider Outcome, RecoveryJoin and owner-proof bindings
- Snapshot: 2026-11-17
- Status: **L1/L2 CANDIDATE ALIGNMENT SUBSTANTIALLY EXISTS; SAME-BUNDLE REVIEW NOT CLOSED**
- Provenance: exact-Blob inspection and delegated role synthesis; not independent Owner approval
- Branch: review/arch-consol-002-protocol-alignment-2026-11-17

## 1. Executive disposition / 总体裁决

**EN:** The project has materially advanced beyond the earlier 1.2.12 snapshot. The current target is H Unified **1.2.14** (wire 1.3.0) + RecoveryJoin **1.0.2** + RecoveryCutoff **1.0.5**, with CSubmitOutcome **1.0.1**. C has accepted a current H 1.2.14 Provider Outcome mapping candidate; D has a corrected RecoveryJoin P0 crosswalk and D FenceGeneration high-water mapping; I has accepted H 1.2.14 / RecoveryJoin 1.0.2 compatibility; H has both a Provider Outcome mapping and an integrated authority-join mapping; Storage has published v3.2.7 and selected Option A at L1 in its separate topology ADR.

The remaining B problem is no longer "C/H have not migrated from 1.2.11". It is **same-bundle exactness and cross-owner closure**:

1. H has two different mapping artifacts: C Provider Outcome mapping Blob 7739d8159b32702024583669f40974a80801782b and integrated authority-join mapping Blob 1cbe74eba69325510d6b1019d971661f965eabf8. Storage v3.2.7 binds only the latter; C's latest review accepts the former, not the integrated mapping that adds I/D/Storage verifier seams.
2. C's latest review of the C mapping pins H schema Blob fee452efb99ab4fe0ceccb347c46eeef1521bd28, while the mapping itself and current H schema file pin 09fcd1fa29fe24255fbd87cae79dafb406594a59. The two schema Blobs differ only in descriptive text ("1.2.13" vs "1.2.14"), but exact-Blob governance still requires one identical pin and a fresh C readback.
3. Storage v3.2.7 is a candidate bundle, not joint acceptance. It predates the latest C/I review records and still routes fresh C/H/D/I reviews and A integration review as required.
4. H's 25-test callback-seam CI is bounded orchestration evidence: the new orchestration tests mock schema validation, semantic validation and candidate digest/preimage calculation. It is not an unmocked end-to-end proof of real I/D/Storage authority records.

**中文：** 项目已明显超越此前 1.2.12 快照。当前协议目标为 H Unified **1.2.14**（Wire 1.3.0）+ RecoveryJoin **1.0.2** + RecoveryCutoff **1.0.5**，CSubmitOutcome **1.0.1**。C 已接受 H 1.2.14 Provider Outcome Mapping 候选；D 已发布修正后的 RecoveryJoin P0 Crosswalk 和 D FenceGeneration High-Water 映射；I 已接受 H 1.2.14 / RecoveryJoin 1.0.2 兼容性；H 已发布 Provider Outcome Mapping 和集成 Authority-Join Mapping；Storage 已发布 v3.2.7，并在独立拓扑 ADR 中完成 Option A 的 L1 逻辑选择。

B 阶段剩余问题不再是“C/H 尚未从 1.2.11 迁移”，而是**同一 Bundle 的精确一致性和跨 Owner 闭环**：

1. H 有两种不同 Mapping：C Provider Outcome Mapping Blob 7739...，以及集成 Authority-Join Mapping Blob 1cbe...。Storage v3.2.7 只绑定后者；C 最新审查接受的是前者，没有审查包含 I/D/Storage Verifier Seam 的集成 Mapping。
2. C 最新审查绑定 H Schema Blob fee452...，而 Mapping 自身和 H 当前 Schema 文件绑定 09fcd...。两 Blob 仅在 Description 的 1.2.13/1.2.14 文案上不同，但精确 Blob 治理仍要求统一 SHA 并由 C 重新读回。
3. Storage v3.2.7 是候选 Bundle，不是联合接受；它早于 C/I 最新审查，仍要求 C/H/D/I 新审查及 A 集成审查。
4. H 的 25 项 Callback-Seam CI 仅是有限编排证据：新增测试对 Schema 校验、语义校验和候选 Digest/Preimage 计算使用 Mock，不能当作真实 I/D/Storage 权威记录的无 Mock 端到端证明。

## 2. Exact branch snapshot / 精确分支快照

| Owner | Branch HEAD at snapshot | Latest relevant evidence |
|---|---|---|
| C | 8d7298d7f56b1df48229799ff6462a8db634e7ed | Phase 3.8.16 accepts H Provider Outcome mapping candidate; its H schema pin is fee452... |
| H | a0e0944dc742ac89a71e00814f1d296155b622e5 | Provider Outcome mapping 7739...; integrated authority mapping 1cbe...; current H schema 09fcd... |
| D | 188f414fa2c080111325cb52c93f8cd1dc551388 | RecoveryJoin P0 crosswalk c4ad... pins H schema 09fcd... |
| I | 947553e77375a94671523931518e0d9673c4a766 | Phase 3.8.12 accepts H schema 09fcd... / RecoveryJoin 1.0.2 |
| Storage | 19eb636d364c87850afdcd1d87c04c7fe920f115 | v3.2.7 manifest Blob 4435fc0340a4fce10751679a95f3b4c821bdae4d; topology ADR Blob bb544... |

Branch heads are snapshot identifiers, not moving references. Re-read before any freeze or final sign-off.

## 3. Canonical source pins / 当前规范源 Pin

| Artifact | Exact Blob | Status |
|---|---|---|
| H Unified 1.2.14 / wire 1.3.0 | 09fcd1fa29fe24255fbd87cae79dafb406594a59 | Current H branch schema and H mapping pin |
| H RecoveryJoin 1.0.2 | 4b664e3bce465499bcdfd93796349a4ba7074002 | Current companion schema |
| H RecoveryCutoff 1.0.5 | 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7 | Current companion schema |
| H Provider Outcome mapping | 7739d8159b32702024583669f40974a80801782b | Exact C object / wire mapping candidate |
| H integrated authority-join mapping | 1cbe74eba69325510d6b1019d971661f965eabf8 | Separate I/D/Storage verifier seams; bound by Storage v3.2.7 |
| H validator core / tests | eab961a08d41e871f38543b18ee60cf024977414 / 53774aca0224fd9a727dfa625ba142825f1754b0 | Current callback-seam implementation/test pair in Storage v3.2.7 |
| CSubmitOutcome 1.0.1 | a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda | Current immutable C object schema |
| C Phase 3.11.1 sequence namespace amendment | 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb | New records use 1.0.1; 1.0.0 remains historical |
| C RecoveryJoin P0 crosswalk | df12af95e6859a389ba71eb1b7dba512b9feb8f6 | C row digest + immutable C object dereference |
| D RecoveryJoin P0 crosswalk | c4adf827dd62d44c43b8e871dec4835581508adf | D row digest + ForgetFence high-water |
| I P0 successor allowlist | 35e6843da8becbf3b152512a561b05cf5486819b | Exact I P0 fields; profile registration separate |
| I exact compatibility review | Commit 947553e77375a94671523931518e0d9673c4a766 | Accepts H 1.2.14 / RecoveryJoin 1.0.2; delegated review |
| C exact mapping review | Commit 8d7298d7f56b1df48229799ff6462a8db634e7ed | Accepts H mapping 7739...; schema pin mismatch noted above |
| Storage v3.2.7 manifest | 4435fc0340a4fce10751679a95f3b4c821bdae4d | Not jointly accepted / not frozen |

## 4. Exact-version contradictions / 精确版本矛盾

### B-01 — C review and H mapping do not use the same H schema Blob

H Provider Outcome mapping 7739... binds H Unified 1.2.14 Blob 09fcd.... C Phase 3.8.16 review binds the same mapping Blob but lists H schema Blob fee452.... Direct comparison shows the only textual difference is the schema description: fee452... says artifact revision 1.2.13, while 09fcd... says 1.2.14. The actual schema ID and required artifact revision are 1.2.14 in both.

**Required:** C republishes a one-line exact-pin correction against 09fcd... and re-reads H mapping 7739.... This is an exact-Blob provenance mismatch, not a demonstrated semantic incompatibility.

### B-02 — C has not reviewed the integrated H authority-join mapping

H has two separate mapping artifacts: Provider Outcome mapping 7739..., and integrated authority-join mapping 1cbe..., which includes distinct I terminal, D clearance and Storage resolution verifier seams and is the mapping pinned by Storage v3.2.7. C Phase 3.8.16 accepts 7739..., not 1cbe....

**Required:** C reviews exact 1cbe... with H schema 09fcd..., C schema a631..., validator eab961..., tests 53774..., and precise C/COC/I/D/Storage joins. H/Storage cannot infer C acceptance from the Provider Outcome-only review.

### B-03 — Storage v3.2.7 is a candidate manifest, not joint acceptance

Storage v3.2.7 Blob 4435... binds H schema 1.2.14, RecoveryJoin 1.0.2, RecoveryCutoff 1.0.5, integrated mapping 1cbe..., validator/test pair eab961... / 53774..., and C 1.0.1. It explicitly says fresh H/C/D/I reviews and A integration review are required.

**Required:** Storage publishes v3.2.8 binding C's review of 1cbe..., H's exact review of I P0 / D crosswalk, D's current crosswalk/review, I's compatibility review, exact H workflow evidence and unchanged Storage v3.2.3/COC source base. Then each Owner reviews the same v3.2.8 Blob and A reviews the joined evidence.

### B-04 — H 25-test CI is bounded, not end-to-end

Storage v3.2.7 §3.1 explains callback tests mock schema validation, semantic validation and candidate digest/preimage calculation for orchestration cases. They show separate I/D/Storage callback slots and UNKNOWN on missing callbacks. They do not prove real authority record validation or production adapters.

**Required:** Add unmocked end-to-end positive and negative fixtures exercising exact H envelope + CSubmitOutcome 1.0.1 + digest/signature + CKeyStatus namespace + provider evidence + C owner ledger + COC + I COMMIT_WON + D clearance + Storage same-GID proof. Keep production integration as a separate L4 gate.

### B-05 — Role simulation is not independent Owner acceptance

C/H/D/I/Storage artifacts label delegated-role provenance. No independent human Owner signature or governance approval is created by this review.

**Required:** Route the same exact manifest to authorized human Owners; no implicit/inherited approval or automatic merge.

## 5. Authority and semantic constraints / 权威与语义约束

1. C owns immutable Provider Outcome truth, provider handoff evidence, C gate/attempt/admission and C sequence namespace.
2. H owns wire schema, version identity, exact mapping and tri-state orchestration; H cannot issue C/I/D/Storage decisions.
3. I owns PolicyDomain, PermissionEpoch, COMMIT_WON/REVOCATION_WON and governance trust/key lifecycle.
4. D owns Canonical Memory, ForgetFenceGeneration, producer/work/attempt/derivative lineage, barrier and D clearance.
5. Storage owns physical serialization substrate, durable participants, visibility pointer/outcome, DB incarnation, outbox and physical recovery.
6. COC owns quorum causal-order prefix, Recovery Cutoff Batch/Manifest and participant log; it is neither C Provider Outcome authority nor JF-10 coordinator.
7. schema_artifact_revision, wire schema_version, C record_sequence/namespace, D Fence/Gate/Barrier generations, I PermissionEpoch/PolicyDomain position, COC quorum position and Storage serialization revision/GID/XID are distinct nominal types. No cross-domain numeric comparison or implicit ordering.
8. Missing verifier, stale key status, incomplete pagination, unavailable proof, unknown DB incarnation or anti-rollback uncertainty must remain UNKNOWN and block release/visibility.

## 6. B closure plan / B 阶段闭环计划

- **B1 — C exact integrated mapping review:** C reviews H integrated mapping 1cbe... against exact H/C schemas and current validator/test pair; corrects its schema Blob pin from fee452... to 09fcd....
- **B2 — H exact review of current I/D proof set:** H binds I P0 successor 35e..., D crosswalk c4ad..., C crosswalk df12..., RecoveryJoin 4b664..., Unified 09fcd..., and current validator mapping. H confirms required fields, digest domains, signature projections, D-only high-water separation and tri-state behavior.
- **B3 — D/I exact currentness:** D and I re-read the same exact H/C mapping bundle and publish their own current exact pins. Earlier H 1.2.13/1.2.12 decisions do not transfer.
- **B4 — Storage v3.2.8 manifest:** Storage publishes a successor binding the complete C/H/D/I source/consumer set, exact CI run/job/commit and evidence ceiling. It includes both H mapping artifacts, not one opaque reference.
- **B5 — Same-manifest review and A handoff:** C/H/D/I/Storage review the identical v3.2.8 Blob. A then reviews the exact joined set. No protocol freeze or production activation follows automatically.

## 7. B acceptance criteria / B 阶段验收条件

B may be marked **CONDITIONALLY ALIGNED (L1/L2)** only when one successor manifest binds H schema 09fcd..., both H mappings 7739... and 1cbe..., validator/test, C schema/amendment, C/D crosswalks, I P0 and all Owner reviews; C reviews the integrated mapping; H reviews current C/D/I sources; the C schema Blob pin is corrected; all Owners review the same manifest and A completes integration review.

B 只有在一个后继 Manifest 精确绑定 H Schema、两类 H Mapping、Validator/Test、C Schema/Amendment、C/D Crosswalk、I P0 和所有 Owner Review；C 审查集成 Mapping；H 审查当前 C/D/I 源集合；C 修正 Schema Blob Pin；所有 Owner 对同一 Manifest 审查且 A 完成集成复审后，才可标记 **CONDITIONALLY ALIGNED (L1/L2)**。

This does not mean protocol freeze, profile registration, provider activation, Global Forget completion, JF-10 closure or implementation PASS.

## 8. A handoff / A 阶段交接

Storage has already selected Option A as the L1 logical topology. Phase A must review, not reselect, that decision:
- per-BrainAuthority CanonicalAuthoritySerializationAnchor identity and append-only transition record;
- D Producer Admission, dependency registration, PublicationParticipant, ForgetFence and Storage visibility/NO_PUBLICATION all sharing one serializable transaction domain and anchor;
- same-transaction ownership and CAS semantics;
- I PolicyDomain sequencer remains independent;
- C Provider Outcome sequencer remains independent;
- COC quorum log remains independent and is not folded into XA;
- lost ACK, serialization retry, old-primary fencing, database incarnation and restore continuity;
- L1 logical correctness separated from L4 engine/deployment/operator/fault-campaign acceptance.

A must not treat the existence of the ADR as proof of physical feasibility or deployment readiness.
