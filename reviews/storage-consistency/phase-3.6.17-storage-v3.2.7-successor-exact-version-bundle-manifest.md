# Phase 3.6.17 — Storage v3.2.7 Successor Exact-Version Bundle Manifest
# Phase 3.6.17 — Storage v3.2.7 后继精确版本 Bundle 清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 CANDIDATE BUNDLE BOUND; FRESH OWNER REVIEWS AND A REVIEW REQUIRED; NOT JOINTLY ACCEPTED / NOT FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor exact bundle: Storage v3.2.6, Blob `dbfa37617d109d5891a067769e858085e2ce547a`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role coordination artifact; **not an independent human Storage Owner signature**.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the C/H exact-version candidate pins in Storage v3.2.6 §3 and its H evidence status. It does not rewrite Storage v3.2.3 S0a–S4, alter the COC Batch-before-Manifest order, or transfer earlier Owner decisions to changed Blobs. Storage v3.2.3 remains the normative technical body; v3.2.6 remains the historical predecessor bundle.

本清单仅替代 Storage v3.2.6 §3 中 C/H 精确版本候选绑定及其 H 证据状态。不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不将旧 Owner 决议转移到新 Blob。Storage v3.2.3 仍是规范技术正文；v3.2.6 是历史前序 Bundle。

A changed Blob invalidates every review that pins the old Blob. Branch names and paths are not version bindings. No 1.2.13 review transfers to 1.2.14. No C/I/D/H role simulation is an independent human Owner signature.

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Storage durable log/recovery protocol v3.2.3 | 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge, same-GID recovery and evidence boundaries |
| COC | COC durable log/recovery companion §§15–17 | 5b950a3a29bd7a5276b92a49a9114d700718b987 | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest ordering amendment | 9704d110a06d0c2ee98be960054e0396d0b68546 | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | 0477f0329997e42a1cbf6ecb8127c5c01fa47051 | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.6 successor bundle | dbfa37617d109d5891a067769e858085e2ce547a | Historical H 1.2.13 / C 1.0.1 candidate bundle |

The v3.2.3 S0a–S4 order remains unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through their independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit the distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current C/H candidate pair / 当前 C/H 精确候选组合

| Role | Artifact | Exact Blob / run | Meaning and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current structural schema; D ForgetFenceGeneration and owner gate generation carriers |
| H | RecoveryJoin schema 1.0.2 | `4b664e3bce465499bcdfd93796349a4ba7074002` | Owner snapshot membership proof and bidirectional owner-admission join carrier |
| H | RecoveryCutoff schema 1.0.5 | `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Recovery cutoff structural family |
| H | Authority-join mapping | `1cbe74eba69325510d6b1019d971661f965eabf8` | Separate I terminal, D Forget clearance and Storage resolution verifier seams |
| H | Exact C object-wire mapping | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` | Unified 1.2.14 ↔ CSubmitOutcome 1.0.1 mapping |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Actual schema, object identity/equality, local semantic and C-P0 digest validation; injected authority callbacks |
| H | Expanded full-path fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Complete synthetic H envelope + immutable C object, with test-only I/D/Storage proof refs |
| H | Expanded validator tests | `c37c5e2621ebd7bae138f135c5066aa8be7f9926` | 33 H validator methods; Tests 21–32 include full path, 22-field duplicate mutation and owner callback predicates |
| H | C crypto interop tests | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a`; `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate JCS/Ed25519 interoperability methods |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Exact workflow path filters include current schema, validator and test/fixture directory |
| H | Exact current-head Provider Outcome CI | Run `44071354162`; commit `6dda3c8f82c2f25118d5bdcfe24015cec678895a`; job `133998097779` | SUCCESS; raw log: 39 tests, 0 failures (33 H validator + 6 C crypto interop) |
| H | Expanded full-path closure | Phase 3.8.16 Blob `927fe9e8dafd5def6a5cb825e5968f5835d3c6bf` | Delegated H-role exact source/CI closure; authority callbacks TEST-ONLY |
| H | Exact-head C-P0 projection regression closure | Phase 3.8.16 Blob `f8aeae206b71f6a6bccd1c41300d40959a5221a8` | Confirms Test 32 C-P0 projection completeness; exact 39/39 CI |
| C | CSubmitOutcome immutable schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | C-owned immutable provider outcome; signed sequence_namespace_ref required |
| C | Sequence namespace amendment | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome record and CKeyStatusEvent share C-owned namespace |
| C | Expanded 22-field full-path exact review | Phase 3.8.19 Blob `da5dd66ef6514f4b66c27e7d8549d17004e8fcac` | Delegated C-role acceptance of local C object/wire matrix; production C trust/egress OPEN |
| D | Expanded D Fence/Storage callback exact review | Phase 3.8.11 Blob `7a9ed2bcf7fd34edc576a4a1be7f4388ee551b43` | Delegated D-role acceptance of local D callback boundary; lineage/release OPEN |
| I | Expanded COMMIT_WON callback exact review | Phase 3.8.15 Blob `44898fa686efc00d4b05aa0454755907d25fa3de` | Delegated I-role acceptance of local COMMIT_WON predicate; trust/L3/currentness OPEN |

### 3.1 Exact CI and evidence ceiling / 精确 CI 与证据上限

H Provider Outcome CI run `44071354162` executed on exact commit `6dda3c8f82c2f25118d5bdcfe24015cec678895a`, job `133998097779`, and completed SUCCESS. The raw job log explicitly records Tests 21–32 and `Ran 39 tests in 9.319s; OK`. The 39 methods comprise 33 H validator methods and six Python/Node C crypto interoperability methods.

Tests 21–32 use actual H Unified 1.2.14 and CSubmitOutcome 1.0.1 schemas, actual local C semantic predicates and actual C-P0 digest/preimage calculation. They cover a full positive envelope/object path; 22 present duplicated wire fields individually mutated; synchronized C-P0/wire mutation; C sequence namespace mismatch; I COMMIT_WON predicate; D exact operation/Fence binding; Storage DB-incarnation/GID/PrepareAttempt/participant-ledger binding; and complete C-P0 projection membership. The test suite does not patch the local schema, semantic or digest functions.

The current H branch HEAD after the two Phase 3.8.16 evidence documents is `1ad9391cfcb94c2434da919b78804217a3a609ef`. Comparing tested commit `6dda3c8...` to current HEAD shows only two added documentation files; schema, validator, test, fixture and workflow Blobs remain byte-identical to the exact CI inputs.

**Evidence ceiling:** all I/D/Storage authority callbacks in the full-path fixture are deterministic test doubles. The C crypto interop methods verify candidate JCS/Ed25519 vectors but do not register production trust profiles. This is strong bounded local L1/L2 source evidence, not production authority authentication, production outer H envelope authentication, provider exactly-once, COC quorum durability or Storage same-GID deployment.

H Provider Outcome CI Run `44071354162` 在精确 Commit `6dda3c8...`、Job `133998097779` 上 SUCCESS。Raw Job Log 明确记录 Test 21–32 执行，并显示 `Ran 39 tests in 9.319s; OK`。39 项由 33 个 H Validator 方法和 6 个 Python/Node C Crypto Interoperability 方法组成。

Test 21–32 使用真实 H Unified 1.2.14 与 CSubmitOutcome 1.0.1 Schema、真实本地 C Semantic Predicate 和 C-P0 Digest/Preimage 计算，覆盖完整正向 Envelope/Object 路径、22 个现存重复 Wire 字段逐项变异、同步 C-P0/Wire 变异、C Sequence Namespace 不一致、I COMMIT_WON Predicate、D 精确 Operation/Fence 绑定、Storage DB Incarnation/GID/PrepareAttempt/Participant Ledger 绑定，以及 C-P0 Projection 成员完整性。测试没有 Patch 本地 Schema/Semantic/Digest 函数。

H 分支加入两份 Phase 3.8.16 证据文档后的当前 HEAD 为 `1ad9391...`。与测试 Commit `6dda3c8...` 比较，仅新增两份文档；Schema、Validator、Test、Fixture 与 Workflow Blob 均与 CI 输入字节一致。

**证据上限：** Full-Path Fixture 中所有 I/D/Storage Authority Callback 均为确定性 Test Double。C Crypto Interop 方法验证候选 JCS/Ed25519 向量，但不注册生产 Trust Profile。这是强有力的有限本地 L1/L2 源级证据，不是生产 Authority Authentication、生产外层 H Envelope Authentication、Provider Exactly-once、COC Quorum Durability 或 Storage Same-GID 部署证明。

## 4. Owner review/adoption matrix / Owner 精确审查与采纳矩阵

| Owner | Exact review artifact / Blob | Exact scope actually reviewed | Current bundle disposition |
|---|---|---|---|
| C | Phase 3.8.19 expanded full-path review, Blob `da5dd66ef6514f4b66c27e7d8549d17004e8fcac` | Exact H schema, C schema, mapping, validator, 22-field test source and full fixture; H CI 44071354162 | Delegated C-role acceptance of local C object/wire and digest/namespace checks as L1/L2 candidate; production C trust, provider evidence and egress OPEN |
| D | Phase 3.8.11 expanded D review, Blob `7a9ed2bcf7fd34edc576a4a1be7f4388ee551b43` | Exact H test/fixture, Test 30 D operation/Fence callback boundary and Test 31 Storage callback distinction | Delegated D-role acceptance of local D callback boundary only; D lineage completeness, late discovery, pagination, currentness CAS and release OPEN |
| I | Phase 3.8.15 expanded I review, Blob `44898fa686efc00d4b05aa0454755907d25fa3de` | Exact H test/fixture, Test 29 COMMIT_WON callback predicate | Delegated I-role acceptance of local predicate only; production I proof, trust roots, key custody, historical verification, anti-rollback and final CAS OPEN |
| H | Phase 3.8.16 expanded full-path closure, Blob `927fe9e8dafd5def6a5cb825e5968f5835d3c6bf`; C-P0 regression closure Blob `f8aeae206b71f6a6bccd1c41300d40959a5221a8` | Exact H HEAD 6dda3c8..., current test/fixture Blobs and CI 44071354162 | Delegated H-role local L1/L2 closure; callbacks TEST-ONLY; outer envelope authentication OPEN |
| A | Prior Phase 1.G review Blob `86b3d4e7d6615b9a5cd915616d7c12f4ecd0a1b3` | Pins previous manifest Blob `fe1dcf...`, old test `dccf8...`, fixture `c80247...`, CI 44069941327 | **SUPERSEDED / NOT CURRENT** by H 39-test/22-field expansion; fresh A exact re-review required |
| Storage | This v3.2.7 manifest | Exact-version bundle binding and review routing | Delegated Storage-role artifact, not independent Storage Owner signature |

C/D/I/H review documents are exact delegated role artifacts, not independent human Owner signatures. They confirm bounded domain review of the current H 39-test set; they do not certify production authority adapters or transfer earlier approvals. A's Phase 1.G review is stale because H's test source and fixture have changed after its pinned manifest and CI set.

C/D/I/H 审查文档是精确的角色审查工件，不是真正独立人类 Owner 签署。它们确认了当前 H 39 项测试集的有限领域审查，但不认证生产 Authority Adapter，也不转移此前批准。A 的 Phase 1.G Review 因 H Test Source 与 Fixture 在其绑定的 Manifest/CI 集之后发生变化而过期。

## 5. Required semantic and operational joins / 必需语义与运行 Join

1. C `payload_digest` equals H `c_submit_outcome_digest`; BMCP envelope digest and Provider Outcome Evidence digest remain distinct domains.
2. C `sequence_namespace_ref` must match authenticated CKeyStatusEvent namespace and the durable C signing sequencer.
3. I terminal decision is independently verified; provider invocation authorization requires the applicable I `COMMIT_WON` proof, not merely any I terminal outcome.
4. D Forget clearance independently verifies FenceGeneration, barrier/lineage membership and final effect boundary.
5. Storage resolution independently verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing authority callback/evidence/currentness/anti-rollback is UNKNOWN; proven contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Owner-local release requires each Owner's fresh final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Any H/C/I/D/Storage Blob change invalidates the affected review and requires a new exact manifest/review.

## 6. Gate state and non-claims / Gate 状态与非声明

- Storage technical architecture v3.2.3: normative candidate body unchanged.
- Storage v3.2.7: **CURRENT EXACT CANDIDATE BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H Unified 1.2.14 / CSubmitOutcome 1.0.1 full local validator CI: **SUCCESS, 39 tests; 22-field duplicate mutation, local semantic/C-P0 digest and bounded I/D/Storage callback predicates PASS with TEST-ONLY authority callbacks**.
- Full local H envelope + C object schema/semantic/digest path: **PASS**.
- Full mutation coverage of all present duplicated fields in the fixture: **PASS (22 fields)**; complete schema-wide optional/conditional mutation and outer H envelope authentication: **OPEN**.
- Production I/D/Storage authority callback adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C/I profiles, production trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- Production activation, production provider egress, Provider exactly-once, Full Applied, Global Forget Completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

本清单不声称生产 Owner 签名、生产 Trust Root/Key Custody、真实 I/D/C Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 7. Required next sequence / 后续执行顺序

1. A must issue a fresh exact integration review against the final read-back Blob of this v3.2.7 manifest; Phase 1.G is stale.
2. H must add outer H envelope payload_digest/signature and authenticated transport-principal verification through the H gateway boundary; the C object validator must not be treated as outer-envelope authentication.
3. H/C must expand schema-wide conditional/optional field mutation, raw JSON strict parsing through validate_raw_provider_outcome, signature/preimage mismatch and C key-status/currentness/rollback vectors.
4. I must connect COMMIT_WON verification to I-authoritative terminal proofs, request/admission ledger, key status/history, PermissionEpoch and final currentness CAS.
5. D must connect Fence/lineage/Barrier proof to complete D-authoritative pagination, late-discovery successor snapshot and final D-local CAS.
6. Storage must connect same-GID resolution to DB incarnation, GID, PrepareAttempt, participant ledger, terminal outcome and visibility marker.
7. C must close production provider issuer truth, same-key lookup, adapter send-vs-close, lost ACK/retry/failover and egress linearization.
8. Storage must prove COC quorum persistence, bidirectional RecoveryJoin, exact prefix/readback and owner-local release ordering. No Gate status changes from CI alone.

1. A 必须针对本 v3.2.7 Manifest 最终读回 Blob 发布全新精确集成审查；Phase 1.G 已过期。
2. H 必须在 H Gateway 边界增加外层 H Envelope payload_digest/signature 与认证 Transport Principal 验证；不得将 C Object Validator 误当成外层 Envelope Authentication。
3. H/C 必须扩展 Schema-wide 条件/可选字段变异、经 validate_raw_provider_outcome 的 Raw JSON 严格解析、Signature/Preimage 不匹配及 C Key Status/Currentness/Rollback 向量。
4. I 必须将 COMMIT_WON 验证连接 I 权威 Terminal Proof、Request/Admission Ledger、Key Status/History、PermissionEpoch 与最终 Currentness CAS。
5. D 必须将 Fence/Lineage/Barrier Proof 连接 D 权威完整分页、Late-Discovery Successor Snapshot 与最终 D-local CAS。
6. Storage 必须将 Same-GID Resolution 连接 DB Incarnation、GID、PrepareAttempt、Participant Ledger、Terminal Outcome 与 Visibility Marker。
7. C 必须关闭生产 Provider Issuer Truth、Same-Key Lookup、Adapter Send-vs-Close、Lost ACK/Retry/Failover 与 Egress Linearization。
8. Storage 必须证明 COC Quorum Persistence、双向 RecoveryJoin、Exact Prefix/Readback 与 Owner-local Release Ordering。CI 本身不改变任何 Gate 状态。

## 8. Provenance / 来源说明

This manifest was authored in delegated Storage-role coordination mode. Exact file Blobs were fetched from their named owner branches and the H workflow run/job logs were read directly. This is a candidate version-binding and review-routing artifact, not an independent Storage Owner signature or runtime deployment result.

本清单由协调会话模拟 Storage 角色编写。精确文件 Blob 来自对应 Owner 分支读取，H Workflow Run/Job Log 已直接核验。本文件仅为候选版本绑定与复审路由工件，不是独立 Storage Owner 签名，也不是 Runtime 部署结果。
