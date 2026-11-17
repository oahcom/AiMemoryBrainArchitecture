# Phase 3.6.20 — Storage v3.3.0 Successor Exact-Version Bundle Manifest
# Phase 3.6.20 — Storage v3.3.0 后继精确版本 Bundle 清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 42-TEST CANDIDATE BUNDLE CONSOLIDATED; A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor exact manifest: Storage v3.2.9, Blob bf323a1682f2bfadc3ff41ea4f86883d678a77e3
- Additional evidence source: Storage v3.2.7 manifest, Blob f7a3acc1845f4322b2b38264eb0d4bae92623bac (latest 42-test source/review set; its own predecessor is v3.2.6)
- Intermediate manifest: Storage v3.2.8, Blob b8a736e885a42d09f4776c34e8b6a93e6402b900
- Normative Storage technical body: Storage v3.2.3, Blob 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792
- COC companion §§15–17: Blob 5b950a3a29bd7a5276b92a49a9114d700718b987
- Option A topology ADR: Blob bb544ba2f346bdc130d524bd5c7310d86f367988
- Provenance: delegated Storage-role coordination artifact; **not an independent human Storage Owner signature**
- English and Chinese are normative peers

## 1. Scope and supersession / 范围与替代关系

This v3.3.0 manifest consolidates the current exact H/C/D/I source and review set and resolves the divergent evidence lineage between v3.2.7 (later 42-test evidence was written into this earlier-numbered manifest) and v3.2.9 (later version number but stale 32-test and Owner-review pins). It supersedes v3.2.7, v3.2.8 and v3.2.9 **for current exact candidate bundle binding only**. It does not rewrite Storage v3.2.3 S0a–S4, alter COC Batch-before-Manifest ordering, transfer old Owner decisions to changed Blobs, or close production gates.

The v3.2.7 manifest remains a source of 42-test evidence but is not treated as a monotonic successor to v3.2.9. v3.2.9 remains historical and its A review requirement does not transfer. This v3.3.0 bundle requires a fresh A review.

本 v3.3.0 清单整合当前 H/C/D/I 精确源与审查集合，并解决 v3.2.7（后续 42-test 证据被写入较早编号 Manifest）与 v3.2.9（版本号较高但 32-test/Owner Review Pin 已过期）之间的证据谱系分叉。它仅就当前精确候选 Bundle 绑定目的替代 v3.2.7、v3.2.8 和 v3.2.9；不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，不将旧 Owner 决议转移到新 Blob，也不关闭生产 Gate。

v3.2.7 保留为 42-test 证据来源，但不视为 v3.2.9 的单调后继。v3.2.9 保留为历史版本，其 A Review 要求不自动转移。本 v3.3.0 必须取得新的 A 精确审查。

Any changed Blob invalidates reviews that pin the predecessor. Branch names and paths are not version bindings. C/H/D/I role reviews remain delegated technical reviews, not independent human Owner signatures.

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge, same-GID recovery and evidence boundaries |
| COC | Durable log/recovery companion §§15–17 | 5b950a3a29bd7a5276b92a49a9114d700718b987 | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | 9704d110a06d0c2ee98be960054e0396d0b68546 | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | 0477f0329997e42a1cbf6ecb8127c5c01fa47051 | Immutable RecoveryRound and owner-local release order |
| Storage/D | Option A per-BrainAuthority topology ADR | bb544ba2f346bdc130d524bd5c7310d86f367988 | L1 logical candidate only; A-01–A-05 clarifications remain open |

The normative S0a–S4 order remains unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact H/C protocol source set / H/C 精确协议源集合

| Owner | Artifact | Exact Blob | Binding |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | 09fcd1fa29fe24255fbd87cae79dafb406594a59 | Current structural schema and D ForgetFenceGeneration high-water carrier |
| H | RecoveryJoin schema 1.0.2 | 4b664e3bce465499bcdfd93796349a4ba7074002 | Generic owner membership proof carrier |
| H | RecoveryCutoff schema 1.0.5 | 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7 | Exact Recovery Cutoff structure |
| H | Authority-Join mapping | 1cbe74eba69325510d6b1019d971661f965eabf8 | C object/wire mapping plus separate I/D/Storage verifier seams |
| H | Validator core | eab961a08d41e871f38543b18ee60cf024977414 | H 1.2.14 / C 1.0.1 schema, object identity/equality, local semantic and C-P0 digest validation; authority callbacks injected |
| H | Validator test source | da1454ed985c84160c4cb6a0462df9d1225fab7f | 36 H validator methods; tests 21–34 include full path, 22 duplicate wire fields, 64 C-P0 members and nullable COC intent |
| H | Positive full-path fixture | f911027c848d21dd36fb87ba64a201a1455787a7 | Synthetic H envelope + immutable C object; authority callbacks are test-only |
| H | C crypto interop tests | 5559fb7a612c8dd92345ceae3a6aa62f4faae41a; a49d588ea6f840927fe21ad8c41cd8089dceac29 | Six Python/Node candidate JCS/Ed25519 interoperability methods |
| H | Provider Outcome workflow | 4459d19f5b4eea058377d9819e48e81eed5c8c4b | Exact workflow path filters include schema, validator and test/fixture directories |
| H | Exact current-head CI | Run 44072037563; commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7; job 134000402978 | SUCCESS; 42 tests, 0 failures (36 H validator + 6 C crypto interop) |
| H | Phase 3.8.17 exact closure | 82f06005e49505c7b33e72e65387dcd9f991dc01 | 42-test closure, full C-P0 mutation and nullable COC intent |
| H | Phase 3.8.16 CI closure | 431d049184ae4622e1dcac3f71176ab1cfc9aa8b | Exact 42-test run/source binding |
| C | CSubmitOutcome immutable schema 1.0.1 | a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda | C-owned immutable provider outcome; signed sequence_namespace_ref |
| C | Sequence namespace amendment | 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb | C record_sequence and CKeyStatusEvent event_sequence share C-owned namespace |
| C | RecoveryJoin P0 crosswalk | df12af95e6859a389ba71eb1b7dba512b9feb8f6 | C owner row/digest indirection |
| C | Exact 42-test review | 61ff3716c9c3d3101a0058963c58f089aa1448b0 | Delegated C acceptance of P0 projection/full mutation and nullable COC semantics; production C authority OPEN |
| D | RecoveryJoin P0 crosswalk | c4adf827dd62d44c43b8e871dec4835581508adf | D row/operation/scope/fence/barrier/lineage digest indirection |
| D | Exact 42-test review | 2bf4514fe7972b72f6c1f904e461f86488d04cda | Delegated D acceptance of local callback boundary only; lineage/currentness/release OPEN |
| I | P0 allowlist successor | 44986f5f864bcdc1a79d34978273644d381a68c0 | Exact I common-envelope/proof-family P0 candidate |
| I | Exact 42-test review | 2851d31e4f8caf48348944b885b493c607ca79e1 | Delegated I acceptance of local COMMIT_WON predicate only; trust/L3/currentness OPEN |

## 4. Exact CI and evidence ceiling / 精确 CI 与证据上限

H Provider Outcome CI run 44072037563 executed on exact H commit c6faee294e503f32a802ba51f3f3b3eb4bee2cd7, job 134000402978, and completed SUCCESS. The raw job log records Tests 21–34 and Ran 42 tests; OK. The 42 methods comprise 36 H validator methods and six Python/Node C crypto interoperability methods.

The suite proves at bounded local L1/L2 source level:
- actual H/C schema loading and full synthetic envelope/object schema validation;
- exact equality and mutation rejection for all 22 duplicated wire fields present in the fixture;
- local C semantic predicates and C-P0 digest/preimage recomputation;
- C-P0 projection includes every present object member except derived payload_digest and signature;
- mutation rejection across all 64 present C-P0 members;
- C sequence namespace mismatch rejection;
- local I COMMIT_WON, D exact operation/Fence and Storage DB-incarnation/GID/PrepareAttempt/participant-ledger callback predicates;
- valid NOT_INVOKED + PROVEN_NONE with null COC intent/reservation only when explicit COCAbsenceReason and distinct no-handoff/not-invoked proofs exist;
- absent COCAbsenceReason is not equivalent to explicit null;
- fail-closed UNKNOWN for missing authority callbacks and INVALID for explicit contradictions;
- candidate Python/Node JCS/Ed25519 interoperability.

**Evidence ceiling:** the I/D/Storage authority callbacks are deterministic test doubles. The suite does not authenticate production issuer-signed I/D/Storage proof payloads or connect production authority stores. It does not prove production C profile/trust roots/key custody/key-status ledger, provider issuer truth, same-key lookup, adapter send-vs-close/lost-ACK/retry/failover, outer H envelope signature/payload_digest authentication, COC quorum durability, same-GID physical recovery, JF-10, Global Forget, Full Applied or production activation.

中文：H Run 44072037563 在精确 Commit c6faee... / Job 134000402978 上 SUCCESS，共 42 项（36 H Validator + 6 Python/Node C Crypto Interop）。本地 L1/L2 证据覆盖真实 H/C Schema、完整合成 Envelope/Object、22 个重复 Wire 字段变异、64 个 C-P0 字段变异、C Sequence Namespace、Nullable COC Intent、I/D/Storage Callback Predicate 及 fail-closed UNKNOWN/INVALID。**证据上限：** I/D/Storage Callback 仍为确定性 Test Double；不认证生产 Owner 签名 Proof，也不连接生产权威存储。生产 C Trust/Provider Truth、H 外层 Envelope Auth、COC Quorum、Same-GID 物理恢复、JF-10、Global Forget、Full Applied 和生产激活均未证明。

## 5. Owner review status / Owner 复审状态

| Owner | Exact review Blob | Accepted scope | Still open |
|---|---|---|---|
| C | 61ff3716c9c3d3101a0058963c58f089aa1448b0 | C-P0 projection, 64-field mutation, nullable COC intent; local L1/L2 candidate | Production C trust, provider issuer, same-key lookup, adapter race/fault and egress |
| D | 2bf4514fe7972b72f6c1f904e461f86488d04cda | Local D callback boundary and exact operation/Fence mismatch behavior | Complete lineage, late discovery, pagination, currentness CAS, barrier terminality and release |
| I | 2851d31e4f8caf48348944b885b493c607ca79e1 | Local I COMMIT_WON predicate and fail-closed mismatch behavior | I proof authentication, trust roots, key custody, historical verification, anti-rollback, revocation ordering and final CAS |
| H | 82f06005e49505c7b33e72e65387dcd9f991dc01 / 431d049184ae4622e1dcac3f71176ab1cfc9aa8b | Exact 42-test local H/C conformance and CI binding | Outer H envelope authentication, production callbacks and independent human H adoption |
| A | PENDING for this exact v3.3.0 Blob | Must review v3.3.0 and Option A topology ADR | No v3.2.8/v3.2.9 A review transfers |

These are delegated role reviews. They are not independent human Owner signatures or formal governance approvals. Each Owner's authority remains local; the manifest cannot synthesize a global PASS.

## 6. Gate state and non-claims / Gate 状态与非声明

- Storage v3.2.3: normative design body unchanged.
- H 1.2.14 / C 1.0.1 local conformance: **42 tests PASS; bounded local L1/L2 only**.
- Storage v3.3.0: **candidate exact bundle consolidated; fresh A review required; not jointly accepted / not frozen**.
- Option A topology: **conditional L1 candidate; A-01–A-05 clarifications remain open**.
- JF-10 P0: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C distributed end-to-end fault injection: **DEFERRED / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C/I production profiles, trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- D lineage completeness, late-discovery, barrier terminality and release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin, same-GID recovery, quorum durability and linearizable readback: **OPEN**.
- Production activation, provider egress, Provider exactly-once, Full Applied, Global Forget completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

## 7. Required next sequence / 后续执行顺序

1. A issues a fresh exact integration review against the final read-back Blob of this v3.3.0 manifest and Option A topology ADR.
2. Storage/D resolve Option A A-01–A-05 and publish a successor topology ADR; affected Owners re-review exact changed Blobs.
3. H implements/validates outer-envelope payload_digest/signature and authenticated transport-principal checks at the gateway boundary.
4. I connects COMMIT_WON verification to I-authoritative terminal proofs, request/admission ledger, key status/history, PermissionEpoch and final currentness CAS.
5. D connects Fence/lineage/barrier proof to complete D-authoritative pagination, late-discovery successor snapshot and final D-local CAS.
6. Storage connects same-GID resolution to DB incarnation, GID, PrepareAttempt, participant ledger, terminal outcome and visibility marker.
7. C closes provider issuer truth, same-key lookup, adapter send-vs-close, lost ACK/retry/failover and egress linearization.
8. Storage proves COC quorum persistence, bidirectional RecoveryJoin, exact prefix/readback and owner-local release ordering. CI alone does not change any Gate status.

## 8. Provenance / 来源说明

This manifest was authored in delegated Storage-role coordination mode. Exact source Blobs and the H workflow run/job were read from GitHub. This is a version-binding and review-routing artifact, not an independent Storage Owner signature, runtime deployment result or production conformance statement.

本清单由协调会话模拟 Storage 角色编写。精确源 Blob 与 H Workflow Run/Job 已从 GitHub 读回。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名、Runtime 部署结果或生产符合性声明。
