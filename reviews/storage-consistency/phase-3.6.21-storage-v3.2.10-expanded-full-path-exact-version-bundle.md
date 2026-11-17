# Phase 3.6.20 — Storage v3.2.10 Exact Bundle Manifest: Expanded Full-Path Mutation Evidence
# Phase 3.6.20 — Storage v3.2.10 精确 Bundle 清单：扩展 Full-Path Mutation 证据

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 EXPANDED LOCAL PATH CANDIDATE BOUND; C/H/I/D REVIEWS REFRESHED; EXACT H CI PASS; FRESH A REVIEW REQUIRED; NOT JOINTLY FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor bundle: Storage v3.2.9, Blob `bf323a1682f2bfadc3ff41ea4f86883d678a77e3`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role successor manifest; **not an independent human Storage Owner signature**.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the H test/fixture/CI and C/H/I/D review pins in Storage v3.2.9. It does not rewrite Storage v3.2.3 S0a–S4, change the COC Batch-before-Manifest order, or upgrade any production gate. Storage v3.2.3 remains the normative recovery body; v3.2.9 remains the immediate predecessor.

本清单仅替代 Storage v3.2.9 中 H Test/Fixture/CI 与 C/H/I/D 复审绑定，不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不提升任何生产 Gate。Storage v3.2.3 仍是规范恢复正文；v3.2.9 为直接前序。

The current candidate pair remains H Unified 1.2.14 / wire 1.3.0 and immutable CSubmitOutcome 1.0.1. Expanded local mutation coverage strengthens L1/L2 evidence but does not turn deterministic authority test doubles into production trust, nor does C-object signature validation authenticate the outer H envelope.

当前候选版本对仍为 H Unified 1.2.14 / Wire 1.3.0 与不可变 CSubmitOutcome 1.0.1。扩展本地 Mutation Coverage 增强 L1/L2 证据，但不会将确定性 Authority Test Double 变成生产 Trust；C Object Signature Validation 也不等于外层 H Envelope 已认证。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge and same-GID recovery |
| COC | Durable log/recovery companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.9 exact bundle manifest | `bf323a1682f2bfadc3ff41ea4f86883d678a77e3` | Historical local full-path candidate and review matrix |

The normative S0a–S4 order is unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current protocol and source bundle / 当前协议与源文件精确 Bundle

| Authority | Artifact | Exact Blob / Run | Meaning and evidence ceiling |
|---|---|---|---|
| H | BMCP Unified schema 1.2.14 / wire 1.3.0 | `09fcd1fa29fe24255fbd87cae79dafb406594a59` | Current exact wire schema and D ForgetFenceGeneration high-water carrier |
| H | Authority-Join mapping Phase 3.8.10 | `1cbe74eba69325510d6b1019d971661f965eabf8` | C object/wire mapping and separate I/D/Storage verifier seams |
| H | RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 | `4b664e3bce465499bcdfd93796349a4ba7074002` / `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Closed generic membership proof and exact cutoff structure |
| H | C/D/I crosswalk review Phase 3.8.12 | `90cdadd7d80676c1338965576c955a5f336ad0bc` | Generic P0 and owner-digest dereference mapping |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | H 1.2.14 / C 1.0.1 validator; local C object digest/equality and ten callback seams |
| H | Expanded validator test source | `540056d7c4f290c31290b17c264c69cfd76b1cb2` | 32 H validator unit/full-path methods; tests 26–31 add expanded mutations |
| H | Full positive H envelope + C object fixture | `f911027c848d21dd36fb87ba64a201a1455787a7` | Synthetic test-only fixture with I/D/Storage proof refs and tuple members |
| H | C crypto interop test sources | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate crypto interoperability methods |
| H | Expanded full-path closure Phase 3.8.15 | `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504` | Exact source/fixture/CI pins and explicit outer-envelope auth non-claim |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Python unittest discovery over all provider_outcome test files |
| H | Exact expanded CI | Run `44070924346`, commit `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`, job `133996627914` | completed/success; 38 test methods across three files; local full-path and mutation evidence only |
| C | CSubmitOutcome schema 1.0.1 | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C-owned provider outcome; signed sequence_namespace_ref |
| C | C sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome and CKeyStatusEvent share durable C namespace |
| C | C RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C row/digest indirection into generic RecoveryJoin P0 |
| C | C expanded full-path review Phase 3.8.18 | `8433ce8d99410229924b026f87d71c46b79c24ef` | Accepts local C object path and 22-field duplicate mutation evidence; production C trust remains open |
| I | I P0 allowlist for H 1.2.14 | `44986f5f864bcdc1a79d34978273644d381a68c0` | Exact I common-envelope/proof-family P0 candidate |
| I | I expanded full-path/terminal callback review Phase 3.8.14 | `eb35989ccba4d1039ce7e6e87d04f2f026e51b5b` | Accepts local path; production I terminal proof verifier remains open |
| D | D RecoveryJoin P0 crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D owner row/operation/scope/fence/barrier/lineage digest indirection |
| D | D expanded full-path/clearance callback review Phase 3.8.10 | `fd576d05a6dbf18ce4920b6a1ce44b957f9f1850` | Accepts local path; production D clearance verifier remains open |
| Storage | This v3.2.10 manifest | Self-reference omitted | Exact bundle/review routing, not independent Storage approval |

## 4. Exact CI and expanded mutation evidence / 精确 CI 与扩展 Mutation 证据

H run `44070924346` completed successfully on exact commit `77a9d5e2e716ba33387f0beb1195f864ed8ac54f`, job `133996627914`. The suite has 38 methods: 32 H validator unit/full-path methods and six Python/Node C crypto interop methods.

Tests 21–31 load the actual H/C schemas and the synthetic positive fixture and call the real validator without mocking schema, semantic or C-P0 digest/preimage primitives. Expanded tests add:
- 22 present duplicated wire-field mutations, each required to return INVALID;
- mutate a C-P0 member and its matching wire field together, then require digest-recomputation INVALID;
- C sequence namespace mismatch after digest recomputation → key-status contradiction INVALID;
- I terminal must be exact COMMIT_WON for provider invocation;
- D clearance must bind the exact ForgetOperation/Fence tuple;
- Storage resolution must bind DB incarnation, GID, PrepareAttempt and participant-ledger tuple.

All ten authority callbacks in the positive fixture remain deterministic test doubles. The local H validator verifies C object digest and H/C wire mapping, but **does not authenticate the outer H envelope's own payload_digest/signature or transport identity**. H gateway/authentication integration remains a separate OPEN obligation.

H Run `44070924346` 在精确 Commit 上成功，Job `133996627914` 成功。套件共 38 个方法：32 个 H Validator Unit/Full-Path 方法与 6 个 Python/Node C Crypto Interop 方法。

Test 21–31 加载真实 H/C Schema 与合成正向 Fixture，调用真实 Validator，不 Mock Schema、Semantic 或 C-P0 Digest/Preimage 基础函数。扩展测试新增：
- 22 个当前存在的重复 Wire 字段逐项篡改，均要求 INVALID；
- 同时篡改 C-P0 成员与匹配 Wire 字段，再要求 Digest 重算后 INVALID；
- 重算 Digest 后篡改 C Sequence Namespace，要求 Key Status Contradiction 为 INVALID；
- I Terminal 必须精确为 Provider Invocation 所需的 COMMIT_WON；
- D Clearance 必须绑定精确 ForgetOperation/Fence；
- Storage Resolution 必须绑定 DB Incarnation、GID、PrepareAttempt 与 Participant Ledger。

正向 Fixture 的十个 Authority Callback 仍为确定性 Test Double。本地 H Validator 验证 C Object Digest 与 H/C Wire Mapping，但**不认证外层 H Envelope 自身的 payload_digest/signature 或 Transport Identity**。H Gateway/Authentication 集成仍是独立 OPEN 义务。

## 5. Owner review matrix / Owner 复审矩阵

| Owner | Exact review Blob | Decision and scope | Remaining conditions |
|---|---|---|---|
| H | Mapping `1cbe74...`; crosswalk review `90cdad...`; expanded closure `60e5eb...` | Accepts L1/L2 mapping, generic P0 and expanded local full-path mutation suite | Independent human H adoption; outer-envelope authentication; production callbacks; L3 |
| C | Phase 3.8.18 review `8433ce...` | Accepts C object local full-path and 22-field duplicate mutation evidence | Production C trust, provider issuer, same-key lookup, adapter race/fault and egress serialization |
| I | Phase 3.8.14 review `eb3598...` | Accepts local path and I terminal callback boundary | Production I proof verifier, trust root, key custody, L3 P0 vectors, anti-rollback |
| D | Phase 3.8.10 review `fd576d...` | Accepts local path and D clearance callback boundary | Complete lineage, late-discovery, currentness CAS and production release |
| Storage | This manifest | Binds exact bundle | Bidirectional COC joins, same-GID recovery, quorum durability and readback |
| A | No review of v3.2.10 yet | **PENDING** | Fresh exact A integration review required; v3.2.9 A decision does not transfer |

All C/H/I/D/Storage decisions above are delegated role simulations and source-level architecture reviews, not independent human Owner signatures or formal organizational approvals.

## 6. Storage join and gate obligations / Storage Join 与 Gate 义务

1. C `payload_digest` equals H `c_submit_outcome_digest`; digest domains remain distinct.
2. C `sequence_namespace_ref` equals authenticated CKeyStatusEvent namespace and durable C sequencer namespace.
3. I terminal authorization verifies exact I-signed proof and applicable `COMMIT_WON`; generic terminality is insufficient.
4. D Forget clearance verifies FenceGeneration, complete affected lineage/barrier membership and final effect boundary.
5. Storage resolution verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing callback/evidence/currentness/anti-rollback is UNKNOWN; contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Each Owner's release requires its own final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Outer H envelope digest/signature/transport identity must be authenticated by the H gateway/authentication layer; C object signature validation is not a substitute.
10. Any source Blob change invalidates affected reviews and requires a new exact manifest/review.

## 7. Gate state and non-claims / Gate 状态与非声明

- Storage v3.2.10: **EXACT CANDIDATE BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H local full-path schema/semantic/C-P0 digest and expanded mutation conformance: **PASSED on exact CI run 44070924346**.
- Outer H envelope payload_digest/signature/transport authentication: **OPEN**.
- Real production C signature/key-status, provider evidence and same-key lookup: **OPEN**.
- Real I/D/Storage proof authentication and production callback adapters: **NOT IMPLEMENTED / NOT VERIFIED**.
- Complete owner-ledger pagination, D lineage/late-discovery and final release CAS: **OPEN**.
- Storage bidirectional RecoveryJoin, same-GID recovery, quorum durability and linearizable readback: **OPEN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C distributed end-to-end fault injection: **DEFERRED / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C/I production profiles, trust roots, key custody and anti-rollback: **NOT APPROVED / OPEN**.
- Production activation, provider egress, Provider exactly-once, Full Applied, Global Forget completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

## 8. Required next sequence / 后续执行顺序

1. A performs fresh exact-version integration review of this v3.2.10 manifest and every pinned Blob.
2. Implement outer H envelope authentication (payload digest, signature, transport identity) at the H gateway and add full-path positive/negative tests.
3. Replace test doubles with owner-authoritative I/D/Storage proof verifiers and production trust/currentness sources.
4. Complete negative full-path mutations for every C-P0 member, null/absent distinctions, stale key status and anti-rollback checkpoints.
5. C executes provider adapter timeout/lost-ACK/partial-write/retry/failover and close-vs-send race evidence.
6. Storage executes bidirectional COC participant ↔ I/D/C owner admission joins, same-GID RecoveryJoin, quorum persistence and linearizable readback.
7. Only after independently verified evidence predicates close may the project consider Gate B/C, protocol freeze or production activation.

## 9. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Exact source Blobs and H workflow run/job were read from GitHub. This is a version-binding and review-routing artifact, not an independent Storage Owner signature, runtime deployment result or production conformance statement.

本清单由协调会话模拟 Storage 角色编写。所有源 Blob 与 H Workflow Run/Job 均从 GitHub 读回。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名、Runtime 部署结果或生产符合性声明。
