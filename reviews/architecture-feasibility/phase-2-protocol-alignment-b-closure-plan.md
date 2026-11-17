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


## 9. Superseding B snapshot — Storage v3.2.9 / 更新后的 B 快照

This section supersedes the earlier v3.2.7 / v3.2.8 candidate snapshot. Current successor: Storage **v3.2.9**, manifest Blob **bf323a1682f2bfadc3ff41ea4f86883d678a77e3**.

### 9.1 Current Owner branch HEADs / 当前 Owner 分支 HEAD

| Owner | Current branch HEAD | Latest action |
|---|---|---|
| A | 0bb77a3df8023ef0a5e27d79a0a9c49509a5b3f7 | Exact integration review of Storage v3.2.8; v3.2.9 still requires fresh A review |
| C | 81f1e81307315a31c3bbeae17eb801e8a4f47e10 | Corrected exact H schema pin in Phase 3.8.18 review |
| H | 362cc113cfb5b595a4002a6f6e980d19ae2d2d15 | Full local H/C path fixture and exact CI binding; 32 test methods |
| D | 7d01732521a8b9db202f10cde2c2547e50071d58 | Corrected exact H schema pin in D full-path/clearance review |
| I | a68bb3587fe88aa72398e2dc8d136f94cee9a63f | Corrected exact H schema pin in I full-path/terminal review |
| Storage | 39a1e0429f6b4b08c6c437c8e3f5ace582a7315f | Storage v3.2.9 exact bundle manifest |

### 9.2 What is now aligned at L1/L2 candidate level / 已完成的 L1/L2 候选收敛

- H Unified 1.2.14 Blob `09fcd1fa29fe24255fbd87cae79dafb406594a59` is now the exact common pin across H mapping, C review, D review, I review and Storage v3.2.9.
- H integrated Authority-Join mapping Blob `1cbe74eba69325510d6b1019d971661f965eabf8` is reviewed by C, H, D and I role artifacts.
- CSubmitOutcome 1.0.1 remains the exact immutable C source; 1.0.0 is historical for new records.
- RecoveryJoin 1.0.2 and RecoveryCutoff 1.0.5 remain separately pinned.
- Storage v3.2.9 binds the exact C/H/I/D source and review set and H full-path test evidence.

### 9.3 Full local path CI — improved evidence, not production authority / 本地完整路径 CI

Storage v3.2.9 binds:
- H Unified schema 1.2.14: `09fcd1fa29fe24255fbd87cae79dafb406594a59`
- H integrated mapping: `1cbe74eba69325510d6b1019d971661f965eabf8`
- H validator core: `eab961a08d41e871f38543b18ee60cf024977414`
- H full-path test source: `dccf8c099c18807ec072870d32604d0912209f01`
- H full positive fixture: `c80247a6ecfbb4a29ff0993e8e2aea4829d00626`
- H full-path source/CI closure: `804bfd3214b015c80340575c1eb467d756ad0699`
- H CI run `44069777296`, tested commit `9eb06313e94e762f0fde4a606633a6dbe1bf8262`, job `133992753552`: 32 test methods, success.

Tests 21–25 execute the actual local H envelope + CSubmitOutcome 1.0.1 schema/semantic/digest path without mocking those local primitives. They cover a positive fixture, wire/object mismatch, C payload digest mutation, missing authority callbacks → UNKNOWN and contradictory callback → INVALID.

**Evidence ceiling:** the ten C/I/D/Storage authority callbacks in the positive fixture remain deterministic test doubles. They are not production issuer-signed proof payloads or connected authority stores. This is full local validation-path evidence, not production trust/authority integration or distributed fault proof.

### 9.4 B disposition / B 阶段裁决

**B is now CONDITIONALLY ALIGNED at L1/L2 candidate level against Storage v3.2.9.** The earlier exact-pin and missing C integrated-mapping review discrepancies are corrected by the latest C/H/D/I source set and v3.2.9 manifest.

B is handed to Phase A for exact review of (a) Storage v3.2.9 and (b) the separate Option A per-BrainAuthority serialization topology ADR. A's earlier review of v3.2.8 does not transfer to v3.2.9 or to the topology ADR.

Still open: independent human Owner/governance signatures; production C/I trust/key-status and D/Storage proof adapters; full D lineage and release CAS; bidirectional COC↔I/D/C joins; same-GID recovery; R1/R2; JF-10; Gate B/C; production activation.

**B 现可在 L1/L2 候选层标记为 CONDITIONALLY ALIGNED，基线为 Storage v3.2.9。** 早期精确 Pin 与 C 集成 Mapping 审查缺口，已由最新 C/H/D/I 源文件和 v3.2.9 Manifest 修正。现交由 A 对 (a) Storage v3.2.9 和 (b) 独立的 Option A per-BrainAuthority Serialization Topology ADR 做精确审查。A 对 v3.2.8 的旧审查不自动转移到 v3.2.9，也不等于拓扑 ADR 审查。

仍未关闭：独立人类 Owner/治理签署；生产 C/I Trust/Key Status 与 D/Storage Proof Adapter；完整 D Lineage/Release CAS；双向 COC↔I/D/C Join；Same-GID Recovery；R1/R2；JF-10；Gate B/C；生产激活。


## 10. Exact-currentness invalidation after Owner pin corrections / Owner Pin 修正后的精确当前性失效

The latest live Owner branches advanced after Storage v3.2.9 was published:

- C HEAD 81f1e81307315a31c3bbeae17eb801e8a4f47e10 corrected the H schema Blob pin in its Phase 3.8.18 full-path review.
- D HEAD 7d01732521a8b9db202f10cde2c2547e50071d58 corrected the same pin in its full-path/clearance review.
- I HEAD a68bb3587fe88aa72398e2dc8d136f94cee9a63f corrected the same pin in its full-path/terminal review.
- H HEAD 362cc113cfb5b595a4002a6f6e980d19ae2d2d15 updated exact CI binding to run 44069941327, tested commit ba2c9341fee4eb9ca9e665c74bdd37b4675dd251, job 133993324484.
- Storage HEAD remains 39a1e0429f6b4b08c6c437c8e3f5ace582a7315f, with v3.2.9 as its latest manifest.

Storage v3.2.9 Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3 still binds the earlier C/D/I review Blobs 4be9c1cd8f116086bab58340f07e38ddfc223e21 / ccdae9b45affb23c6741b5cceb27004b35a8e03e / 7c65650a37c8c0f270451fb0419e93259fc38151 and H CI run 44069777296 / commit 9eb06313e94e762f0fde4a606633a6dbe1bf8262. The latest Owner branches have changed those exact review/CI pins.

**Correction to Section 9:** B is aligned at the semantic/source candidate level, but the v3.2.9 manifest is no longer the current exact review bundle. B cannot be called fully conditionally aligned against a current same-manifest baseline until Storage publishes a successor (v3.3.0 or equivalent) binding the corrected C/D/I review Blobs and current H CI run/commit/job; C/H/D/I review that identical successor; and A reviews the successor.

This is exact-currentness/provenance drift, not a demonstrated schema or semantic regression. The H 1.2.14 / C 1.0.1 source target remains unchanged.

**中文修正：** 最新 C/D/I 分支分别修正了 Full-Path Review 中的 H Schema Pin；H 将 CI 绑定更新到 Run 44069941327 / Commit ba2c934... / Job 133993324484。Storage v3.2.9 仍绑定旧 C/D/I Review Blob 和旧 H CI Run。因此 B 在语义/源文件候选层已对齐，但 v3.2.9 不再是当前精确 Review Bundle。必须由 Storage 发布后继 v3.3.0（或等效版本），绑定修正后的 C/D/I Review Blob 和当前 H CI Run/Commit/Job；C/H/D/I 对同一 Manifest 复审，再由 A 精确复审。该问题属于精确当前性/来源漂移，不是已证明的 Schema/Semantic 回退。
