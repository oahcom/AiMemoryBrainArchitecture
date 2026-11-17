# Phase 3.6.19 — Storage v3.2.9 Exact Bundle Manifest: Full-Path H Fixture Evidence
# Phase 3.6.19 — Storage v3.2.9 精确 Bundle 清单：H Full-Path Fixture 证据

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **H 1.2.14 / C 1.0.1 FULL LOCAL PATH CANDIDATE BOUND; C/H/I/D ROLE REVIEWS RECORDED; EXACT H CI PASS; FRESH A REVIEW REQUIRED; NOT JOINTLY FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor bundle: Storage v3.2.8, Blob `b8a736e885a42d09f4776c34e8b6a93e6402b900`
- Normative Storage technical body: Storage v3.2.3, Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792`
- COC companion §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Provenance: delegated Storage-role successor manifest; **not an independent human Storage Owner signature**.
- English and Chinese are normative peers.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the H source/test/CI and C/H/I/D review pins in Storage v3.2.8. It does not rewrite Storage v3.2.3 S0a–S4, alter COC Batch-before-Manifest ordering, or upgrade any production gate. Storage v3.2.3 remains the normative technical body; v3.2.8 remains the immediate predecessor.

本清单仅替代 Storage v3.2.8 中 H Source/Test/CI 与 C/H/I/D 复审绑定，不改写 Storage v3.2.3 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不提升任何生产 Gate。Storage v3.2.3 仍为规范技术正文；v3.2.8 为直接前序。

Any changed Blob invalidates reviews that pin its predecessor. The current candidate pair remains H Unified 1.2.14 / wire 1.3.0 and immutable CSubmitOutcome 1.0.1. The full-path tests increase local evidence only; they do not make owner test doubles into production trust authorities.

任何 Blob 变化都会使绑定旧 Blob 的审查失效。当前候选版本对仍为 H Unified 1.2.14 / Wire 1.3.0 与不可变 CSubmitOutcome 1.0.1。Full-Path Test 仅增强本地证据，不会将 Owner Test Double 变成生产信任权威。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Durable log/recovery protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge and same-GID recovery |
| COC | Durable log/recovery companion §§15–17 | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | `0477f0329997e42a1cbf6ecb8127c5c01fa47051` | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.8 manifest | `b8a736e885a42d09f4776c34e8b6a93e6402b900` | Historical H source/test and owner-review candidate |

The normative S0a–S4 order remains unchanged:
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
| H | Authority-Join mapping Phase 3.8.10 | `1cbe74eba69325510d6b1019d971661f965eabf8` | C object/wire mapping plus independent I/D/Storage verifier seams |
| H | RecoveryJoin 1.0.2 / RecoveryCutoff 1.0.5 | `4b664e3bce465499bcdfd93796349a4ba7074002` / `75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7` | Closed generic membership proof and exact cutoff structure |
| H | C/D/I crosswalk review Phase 3.8.12 | `90cdadd7d80676c1338965576c955a5f336ad0bc` | Generic P0 and owner-digest dereference mapping |
| H | Validator core | `eab961a08d41e871f38543b18ee60cf024977414` | Fail-closed H 1.2.14 / C 1.0.1 validator with ten authority callback classes |
| H | Full-path validator tests | `dccf8c099c18807ec072870d32604d0912209f01` | 26 H validator unit/fixture test methods, including tests 21–25 full-path |
| H | Full positive H envelope + C object fixture | `c80247a6ecfbb4a29ff0993e8e2aea4829d00626` | Synthetic test-only fixture; owner callbacks are deterministic test doubles |
| H | C crypto interop test sources | `5559fb7a612c8dd92345ceae3a6aa62f4faae41a` / `a49d588ea6f840927fe21ad8c41cd8089dceac29` | Six Python/Node candidate crypto interop methods |
| H | Full-path source/CI closure Phase 3.8.14 | `804bfd3214b015c80340575c1eb467d756ad0699` | Exact fixture/source/test/run pins and evidence ceiling |
| H | Provider Outcome workflow | `4459d19f5b4eea058377d9819e48e81eed5c8c4b` | Python unittest discovery over all provider_outcome test_*.py files |
| H | Exact current CI | Run `44069777296`, commit `9eb06313e94e762f0fde4a606633a6dbe1bf8262`, job `133992753552` | completed/success; 32 test methods across three Python files; local full-path schema/semantic/digest and crypto interop only |
| C | CSubmitOutcome 1.0.1 schema | `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda` | Immutable C-owned provider outcome; signed sequence_namespace_ref |
| C | C sequence namespace amendment Phase 3.11.1 | `6fa67af110ebbc5ef57ed908bb4880d99c5e46fb` | C outcome and CKeyStatusEvent share durable C namespace |
| C | C RecoveryJoin P0 crosswalk | `df12af95e6859a389ba71eb1b7dba512b9feb8f6` | C row/digest indirection into generic RecoveryJoin P0 |
| C | C full-path review Phase 3.8.18 | `4be9c1cd8f116086bab58340f07e38ddfc223e21` | Accepts local H/C schema/semantic/digest path; production C trust remains open |
| I | I P0 allowlist for H 1.2.14 | `44986f5f864bcdc1a79d34978273644d381a68c0` | Exact I common-envelope/proof-family P0 candidate |
| I | I full-path/terminal callback review Phase 3.8.14 | `7c65650a37c8c0f270451fb0419e93259fc38151` | Accepts local path and specifies I terminal proof production boundary |
| D | D RecoveryJoin P0 crosswalk | `c4adf827dd62d44c43b8e871dec4835581508adf` | D owner row/operation/scope/fence/barrier/lineage digest indirection |
| D | D full-path/clearance callback review Phase 3.8.10 | `ccdae9b45affb23c6741b5cceb27004b35a8e03e` | Accepts local path and specifies D clearance production boundary |
| Storage | This v3.2.9 manifest | Self-reference omitted | Exact bundle/review routing, not independent Storage approval |

## 4. Exact CI and full-path evidence / 精确 CI 与 Full-Path 证据

H run `44069777296` completed successfully on exact commit `9eb06313e94e762f0fde4a606633a6dbe1bf8262`, job `133992753552`. The workflow runs unittest discovery over all test files in the provider_outcome directory. The current suite contains 32 test methods: 26 H validator unit/fixture methods and six Python/Node C crypto interoperability methods.

Tests 21–25 load the actual H 1.2.14 and C 1.0.1 schemas and the synthetic full positive fixture, then call the actual validator without mocking schema validation, semantic predicates or C-P0 digest/preimage calculation. They test:
- full local H envelope + C object schema/semantic/digest path;
- wire/object duplicate mismatch → INVALID;
- C payload digest mutation → INVALID after recomputation;
- missing I/D/Storage callbacks → UNKNOWN;
- contradictory I/D/Storage callback result → INVALID.

The ten authority callbacks in the positive fixture remain deterministic test doubles. The fixture signature is not authenticated by a production trust root, and the I/D/Storage proof payloads are not real issuer-signed production evidence. Thus this is **full local validation-path evidence**, not production authority integration.

H Run `44069777296` 在精确 Commit 上成功，Job `133992753552` 成功。Workflow 对 provider_outcome 目录所有测试文件执行 unittest discovery。当前套件共 32 个测试方法：26 个 H Validator Unit/Fixture 方法与 6 个 Python/Node C Crypto Interop 方法。

Test 21–25 加载真实 H 1.2.14/C 1.0.1 Schema 与合成正向 Fixture，调用真实 Validator，未 Mock Schema、Semantic 或 C-P0 Digest/Preimage 计算。覆盖完整本地 H Envelope + C Object 路径、Wire/Object 不一致、Digest 篡改、缺失 I/D/Storage Callback 与权威矛盾。

正向 Fixture 中十个 Authority Callback 仍为确定性 Test Double。Fixture Signature 未经生产 Trust Root 认证，I/D/Storage Proof 也不是真实生产 Issuer 签名证据。因此这属于**完整本地验证路径证据**，不是生产权威集成。

## 5. Owner review matrix / Owner 复审矩阵

| Owner | Exact review Blob | Decision and scope | Remaining conditions |
|---|---|---|---|
| H | Mapping `1cbe74...`; crosswalk review `90cdad...`; full-path closure `804bfd...` | Accepts L1/L2 mapping, generic P0 crosswalk and full local path | Independent human H adoption; production authority callbacks; L3 |
| C | Full-path review `4be9c1...` | Accepts local C object schema/semantic/digest path | Production C trust, provider evidence, same-key lookup, adapter race/fault, egress serialization |
| I | Full-path review `7c6565...` | Accepts local integration and specifies I terminal callback | Production I proof verifier, trust root, key custody, L3 P0 vectors, anti-rollback |
| D | Full-path review `ccdae9...` | Accepts local integration and specifies D clearance callback | Complete lineage, late-discovery, currentness CAS, production release |
| Storage | This manifest | Binds current exact bundle | Bidirectional COC joins, same-GID recovery, quorum durability and readback |
| A | No review of v3.2.9 yet | **PENDING** | Fresh exact A integration review required; v3.2.8 A decision does not transfer |

All C/H/I/D/A review artifacts are delegated role simulations in this coordinating workflow, not independent human Owner signatures or formal organizational approvals.

## 6. Storage join and gate obligations / Storage Join 与 Gate 义务

1. C `payload_digest` equals H `c_submit_outcome_digest`; digest domains remain distinct.
2. C `sequence_namespace_ref` equals authenticated CKeyStatusEvent namespace and durable C sequencer namespace.
3. I terminal authorization verifies the exact I-signed proof and applicable `COMMIT_WON`; generic terminality is insufficient.
4. D Forget clearance verifies FenceGeneration, complete affected lineage/barrier membership and final effect boundary.
5. Storage resolution verifies DB incarnation, GID, PrepareAttempt, participant ledger and same-GID terminal resolution/visibility.
6. Missing callback/evidence/currentness/anti-rollback is UNKNOWN; contradiction is INVALID.
7. Batch-before-Manifest, exact backlink, digest-domain separation, quorum and linearizable readback remain required.
8. Each Owner's release requires its own final currentness CAS and signed release; Storage/COC cannot release I/D/C gates.
9. Any source Blob change invalidates affected reviews and requires a new exact manifest/review.

## 7. Gate state and non-claims / Gate 状态与非声明

- Storage v3.2.3: normative design body unchanged.
- Storage v3.2.9: **EXACT CANDIDATE BUNDLE BOUND; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- H local full-path schema/semantic/digest conformance: **PASSED on exact CI run 44069777296**.
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

1. A performs fresh exact-version integration review of this v3.2.9 manifest and every pinned Blob.
2. Replace test doubles with independent owner-authoritative I/D/Storage proof verifiers and production trust/currentness sources.
3. Add complete negative full-path mutations for every duplicated wire field, every C-P0 field, sequence namespace, I COMMIT_WON, D fence/lineage and Storage same-GID tuple.
4. C executes provider adapter timeout/lost-ACK/partial-write/retry/failover and close-vs-send race evidence.
5. Storage executes bidirectional COC participant ↔ I/D/C owner admission joins, same-GID RecoveryJoin, quorum persistence and linearizable readback.
6. Only after independently verified evidence predicates close may the project consider Gate B/C, protocol freeze or production activation.

## 9. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Exact source Blobs and H workflow run/job were read from GitHub. This is a version-binding and review-routing artifact, not an independent Storage Owner signature, runtime deployment result or production conformance statement.

本清单由协调会话模拟 Storage 角色编写。所有源 Blob 与 H Workflow Run/Job 均从 GitHub 读回。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名、Runtime 部署结果或生产符合性声明。
