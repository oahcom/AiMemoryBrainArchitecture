# Phase 3.6.16 — Storage v3.2.6 Successor Exact-Version Bundle Manifest
# Phase 3.6.16 — Storage v3.2.6 后继精确版本 Bundle 清单

- Owner perspective: Storage / COC Durable Log and Recovery
- Date: 2026-11-17
- Status: **SUCCESSOR BUNDLE BOUND / OWNER REVIEWS RECORDED / H 1.2.13 EXACT CI OPEN / NOT JOINTLY FROZEN**
- Project phase: **ARCHITECTURE DESIGN**
- Predecessor manifest: Storage v3.2.5, Blob bea90697e7a61d43bed00543d636a5cdf40cf5ca
- Normative Storage technical body: Storage v3.2.3, Blob 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792
- COC companion §§15–17: Blob 5b950a3a29bd7a5276b92a49a9114d700718b987
- Provenance: delegated Storage-role successor manifest authored in the coordinating session; **not an independent human Storage Owner signature**.

## 1. Scope and supersession / 范围与替代关系

This manifest supersedes only the C/H/I/D exact-version bundle in Storage v3.2.5 §14. It does not rewrite Storage v3.2.3 S0a–S4, change the COC companion's Batch-before-Manifest order, or silently upgrade any owner source. Storage v3.2.3 remains the normative technical body; Storage v3.2.5 remains the immediately preceding exact bundle.

本清单仅替代 Storage v3.2.5 §14 中的 C/H/I/D 精确版本绑定，不改写 Storage v3.2.3 的 S0a–S4，不改变 COC Batch-before-Manifest 顺序，也不静默升级任何 Owner 源。Storage v3.2.3 仍是规范技术正文；v3.2.5 是直接前序精确 Bundle。

A changed Blob invalidates every review that pins the old Blob. Branch names and paths are not version bindings. The exact H 1.2.13 and C 1.0.1 pair below is a successor candidate; it is not a production protocol freeze.

Blob 变化会使绑定旧 Blob 的审查失效。分支名和路径不是版本绑定。下列 H 1.2.13 / C 1.0.1 是后继候选，不是生产协议冻结。

## 2. Unchanged Storage / COC normative base / 不变的 Storage / COC 规范基线

| Authority | Artifact | Exact Blob | Binding |
|---|---|---|---|
| Storage | Storage durable log/recovery protocol v3.2.3 | 5cee0d58575adc0fb3dd20a5c7ab68c2a2711792 | Normative S0a–S4, RecoveryBatch, participant union, JF-10 bridge, same-GID recovery and evidence boundaries |
| COC | COC durable log/recovery companion §§15–17 | 5b950a3a29bd7a5276b92a49a9114d700718b987 | Dual-ledger union manifest, record order, digest chain and recovery joins |
| Storage | Batch-before-Manifest ordering amendment | 9704d110a06d0c2ee98be960054e0396d0b68546 | Batch committed before distinct Manifest with exact backlink |
| Storage | R1/R2 successor-round/release ordering addendum | 0477f0329997e42a1cbf6ecb8127c5c01fa47051 | Immutable RecoveryRound and owner-local release order |
| Predecessor | Storage v3.2.5 exact bundle manifest | bea90697e7a61d43bed00543d636a5cdf40cf5ca | Historical predecessor; §14 is superseded by this file |

The v3.2.3 S0a–S4 order remains unchanged:
1. I/D/C close their own gates and freeze their own request/admission/effect ledgers.
2. COC restores quorum and freezes exact committed prefix P.
3. Build the complete canonical union of COC participants through P and applicable I/D/C owner-local admissions through their independently frozen high-waters.
4. Commit immutable Recovery Cutoff Batch.
5. Commit the distinct Participant Manifest strictly after Batch, with exact backlink.
6. Linearly read back both records and verify prefix, roots, counts, member set, digests, quorum evidence and BatchPosition < ManifestPosition.
7. Only then reconcile participants; each Owner independently issues its own release.

## 3. Exact current C/H protocol bundle / 当前 C/H 协议精确 Bundle

| Role | Exact artifact | Blob | Required meaning |
|---|---|---|---|
| H | BMCP Unified schema artifact 1.2.13 / wire 1.3.0 | 8e7f6a6c9663388863db88548f9c37d0fdb1bd97 | Exact current C Provider Outcome wire branch and ownerSnapshot carrier |
| H | RecoveryJoin schema 1.0.2 | 4b664e3bce465499bcdfd93796349a4ba7074002 | Separate owner_snapshot_membership_proofs and bidirectional owner-admission joins |
| H | RecoveryCutoff schema 1.0.5 | 75cd1fedefd50a6ed570b5afaa2d1f9cc4c6a4c7 | Exact recovery cutoff structural family |
| H | Phase 3.8.9 C 1.0.1 / H 1.2.13 exact mapping | 32bf9b0fd42abe8b58749b858b1d5c9aef39c5fd | Exact C object-to-wire mapping, sequence namespace dereference and outcome predicates |
| H | Provider Outcome validator core | 0449090a0367576b8b4ac20b1b46897facf9233d | H 1.2.13 / C 1.0.1 schema identity and semantic validator source |
| H | Provider Outcome validator tests | 78d3c58ec0d56a95ef78c41ffbad9b21eb797556 | Current 15-test source; exact-head CI has not run |
| C | CSubmitOutcome schema 1.0.1 | a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda | Immutable C object schema; requires signed sequence_namespace_ref |
| C | Phase 3.11.1 sequence namespace amendment | 6fa67af110ebbc5ef57ed908bb4880d99c5e46fb | C record_sequence and CKeyStatusEvent event_sequence share the durable C namespace |
| C | C key-status event schema 1.0.0 | 908b293eba337e9fa75864cea3704e28a1a8d82e | C key-status event object schema; I trust verification remains separate |
| C | C key-status lifecycle contract | 9339b168165a7a3dd34def5236ad61cfd3163418 | C key-status event lifecycle and sequence semantics |
| C | C Phase 3.8.14 exact successor review | dd4fb61536bead57d5c8db0a58abae93b368b72e | Accepts exact H 1.2.13/C 1.0.1 mapping/validator candidate with enumerated blockers |
| C | C Phase 3.8.13 profile identifier decision | 5067dadb9c646a054d78f03c56e635facc36311a | AIMBA-C-CRYPTO-1.0 is sole C candidate ID for C schema 1.0.1 |
| C | C signature projection | 06d9264124d85896ccd44ef7789d9af245d8255b | C-P0 and C domain-separated signature construction candidate |

### 3.1 Cross-owner profile identifiers / 跨 Owner Profile ID

- I-owned evidence uses AIMBA-I-CRYPTO-1.0.
- CSubmitOutcome 1.0.1 uses C-owned AIMBA-C-CRYPTO-1.0.
- C has explicitly not adopted AIMBA-C-OUTCOME-CRYPTO-1.0; I has clarified that name was a non-normative example only.
- H must not alias, normalize or inherit across these profiles.
- C profile registration/trust status remains OPEN; exact schema/profile ID agreement does not mean I has registered the C profile.

### 3.2 C/H semantic contract / C/H 语义合同

- C payload_digest equals H c_submit_outcome_digest; BMCP envelope payload_digest and Provider Outcome Evidence Digest are separate digest domains.
- C ProviderAttemptRef/Generation, CGateRef/Generation, ProviderAccount, Endpoint, Region, API Operation, IdempotencyNamespace, Capability and final request details remain mandatory C-object dereference fields.
- C sequence_namespace_ref must join the authenticated CKeyStatusEvent and C signing sequencer namespace.
- H prepare_attempt_ref/generation is Storage's attempt, not C ProviderAttempt; H participant_ledger_ref/version is Storage's ledger, not C OwnerLedger.
- HANDOFF_REJECTED + PROVEN_NONE requires ProviderNoHandoffProofRef only; it does not require NotInvokedProofRef.
- NOT_INVOKED requires both ProviderNoHandoffProofRef and NotInvokedProofRef.
- HANDOFF_REJECTED + POSSIBLE_OR_UNKNOWN remains nonterminal/blocking; HANDOFF_REJECTED + PROVEN_OCCURRED must be reconciled as an occurred side effect.
- H validator checks loaded schema IDs/URIs, but the trusted schema loader/release manifest must additionally pin exact immutable Blob/content hashes.

## 4. I exact source and review set / I 精确源与复审集合

| Artifact | Blob | Status / scope |
|---|---|---|
| I v1 crypto profile architecture decision, AIMBA-I-CRYPTO-1.0 | 56e956dca909af857469427378777705a5d1082a | Approved as v1 architecture baseline; not production-active |
| I successor P0 allowlists for H 1.2.13 / RecoveryJoin 1.0.2 | 5c0e2049513d391dfc118f4f629a5ec95de456d6 | Exact per-family P0 candidate; L3 vectors remain OPEN |
| I C profile identifier scope clarification | 1e86a1349d371a1cdb4a56d69f783e0f316c7203 | Confirms C profile name is C-owned; I example is non-normative |
| I sequence namespace review for C 1.0.1 | 0d78e5b2bfcf66cae6b757314cead84b9c942601 | Accepts required signed sequence_namespace_ref; no C profile registration |
| I exact review of H 1.2.13 / RecoveryJoin 1.0.2 / P0 | 367a6002327134840b1d03d426bb4bcd864db4c9 | Accepts structural carriers and I P0 candidate; L3/trust/production OPEN |
| I owner snapshot membership proof contract | 88209bbea0ab600880c5c630cfe83af31ee16dd7 | I ledger/snapshot/attestation authority |
| I authorization sequencer contract | 54bab0484bd232a5a258e65e34cc7425288b39a6 | I authorization, receipt consumption, revocation and terminal order |

I remains sole authority for PermissionEpoch, PolicyDomain request/receipt ledgers, inventory/registry epochs, key status, revocation ordering, anti-rollback and I gate release. I profile architecture approval is not production trust registration, key custody, external anti-rollback deployment or L3 per-family vector completion.

## 5. D exact source and review set / D 精确源与复审集合

| Artifact | Blob | Status / scope |
|---|---|---|
| D owner snapshot membership proof contract | d80dabe7210e681bc4e2290355a38f8b67be9ddd | D-owned producer/work/attempt/derivative/barrier proof |
| D publication participant/terminal contract | 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 | D publication participant and terminality |
| D exact review of H 1.2.13 / RecoveryJoin 1.0.2 | 1f03f3a83dda3fc1cc364ae9d2d18a3f1b96b590 | Accepts structural carrier candidate; D lineage/release verification OPEN |
| D predecessor H 1.2.13 review | 84196906cad92367a60c79a74dd241fd80abb96c | Historical; pins earlier H 1.2.13 schema Blob and is superseded by the exact review above |

D remains sole authority for ForgetOperationRef, FenceGeneration, producer/work/attempt/derivative lineage, barrier terminality and D gate release. Late-discovered pre-fence work reopens the affected barrier. HANDOFF_REJECTED + POSSIBLE_OR_UNKNOWN cannot terminalize affected D lineage.

## 6. H/I exact review / H 对 I 精确复审

| Artifact | Blob | Status / scope |
|---|---|---|
| H exact review of I v1 crypto profile and P0 1.2.13 / RecoveryJoin 1.0.2 | 0b6eeadb1cfac415e77ec1358b9fdf99fde11d41 | Accepts I profile/P0 as architecture candidate; L3/trust/production OPEN |
| H exact C mapping | 32bf9b0fd42abe8b58749b858b1d5c9aef39c5fd | Accepts C 1.0.1 / H 1.2.13 mapping candidate; exact CI re-run required |
| H validator core and test source | 0449090a0367576b8b4ac20b1b46897facf9233d / 78d3c58ec0d56a95ef78c41ffbad9b21eb797556 | Source-level evidence only; exact CI has not run |

H confirms I P0 exact projections and the distinction between I OwnerSnapshot summary and separately signed I proof objects. H's current C outcome mapping pins the exact C profile ID and C sequence namespace, but production trust callbacks remain absent.

## 7. Executed versus unexecuted evidence / 已执行与未执行证据边界

| Evidence | Run / Blob | Result | Exact scope |
|---|---|---|---|
| C CSubmitOutcome 1.0.1 candidate CI | Run 44059935858; commit b49966361b4b3121a2ebf4105b4e0c57a612e945 | SUCCESS, 19 tests | C 1.0.1 schema/semantic vectors and candidate Python/Node crypto agreement; not H 1.2.13 wire |
| H predecessor candidate CI | Run 44060704553; commit 8c377a7218b70621d2348b47341d4cf4755b3733 | SUCCESS, 17 tests | H 1.2.12 / C 1.0.1; not H 1.2.13 |
| H current test source | Blob 78d3c58ec0d56a95ef78c41ffbad9b21eb797556 | NOT RUN on exact H 1.2.13 branch HEAD | 15-test source includes schema URI, namespace and outcome predicate cases; no full-envelope matrix yet |
| I generic profile vectors | I decision evidence | Bounded candidate evidence only | Does not close every Phase 3.8.9 P0 family |
| D lineage/barrier | D proof/review artifacts | DESIGN CANDIDATE | No complete real-world lineage enumeration or runtime release CAS |

No exact H 1.2.13 / C 1.0.1 GitHub Actions result is claimed. H workflow source exists only on the H owner branch and is not established here as an executed exact-head workflow. No local test run is claimed. The earlier H 1.2.12 result cannot transfer to H 1.2.13.

## 8. Owner decision matrix / Owner 决议矩阵

| Owner | Exact decision | Remaining conditions |
|---|---|---|
| Storage | Publishes this v3.2.6 successor binding | No joint freeze; exact H CI and A review remain |
| C | ACCEPT WITH ENUMERATED CONDITIONS for H 1.2.13 × C 1.0.1 mapping/validator | Exact H CI, full envelope vectors, key-status callback, provider adapter evidence, profile registration |
| H | ACCEPT AS MAPPING CANDIDATE for H 1.2.13 × C 1.0.1 and I P0 | Exact H CI, full envelope/mutation vectors, I trust integration |
| I | ACCEPT I v1 profile/P0 and H structural carriers as candidates | L3 vectors, production trust/key lifecycle, anti-rollback |
| D | ACCEPT H 1.2.13 / RecoveryJoin 1.0.2 as D proof carrier candidate | D ledger/lineage completeness, late-discovery tests, barrier/release CAS |
| A | **FRESH EXACT-VERSION REVIEW REQUIRED** | Must review this v3.2.6 manifest and all exact current blobs; prior A decisions do not transfer |

All Owner decisions above are delegated role simulations and source-level architecture reviews, not independent human Owner signatures. A must not treat them as independent approvals.

## 9. Storage join obligations / Storage Join 义务

Before a successor freeze recommendation:
1. Bind the C immutable SubmitOutcome ref/digest and C sequence namespace to the exact Storage participant admission and same-GID recovery tuple.
2. Bind H RecoveryJoin membership proof rows to the exact I/D/C owner-local admissions and COC participant union with bidirectional Join Proof.
3. Preserve separate I/D/C owner high-waters and roots; no arithmetic cross-owner comparison.
4. Verify Batch-before-Manifest, exact backlink, distinct digest domains, quorum and linearizable readback.
5. Require each owner-local release proof after its own final currentness CAS; Storage cannot release I/D/C gates.
6. Treat missing owner verifier, key status, provider evidence, currentness or anti-rollback as UNKNOWN and fail closed.
7. Any H schema, C object schema, owner proof or Storage source Blob change requires a new manifest and fresh affected-owner review.

## 10. Gate state and non-claims / Gate 状态与非声明

- Storage technical architecture v3.2.3: remains the normative candidate body.
- Successor protocol bundle v3.2.6: **BOUND FOR JOINT REVIEW; NOT JOINTLY ACCEPTED / NOT FROZEN**.
- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local gate linearization/release: **OPEN**.
- H 1.2.13 exact CI: **NOT RUN / OPEN**.
- C/I profile registration and production trust: **OPEN**.
- D lineage completeness and production release CAS: **OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- Production activation, Provider exactly-once, Global Forget completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

本清单不声称生产 Owner 签名、生产 Trust Root/Key Custody、真实 C/D/I Sequencer CAS、生产 Membership Verifier、Provider 认证、通用 exactly-once、分布式故障注入通过、物理 Forget/擦除、Global Forget Completion 或生产就绪。

## 11. Required next sequence / 后续执行顺序

1. H runs the exact 1.2.13 / C 1.0.1 test suite on the exact current H branch HEAD and records run ID, tested commit and test Blob; add full-envelope positive/negative and every-field mutation vectors.
2. C reviews any changed H validator/test Blob and confirms C object/P0/key-status namespace equality.
3. I completes independent P0 family vectors and production trust/key-status/anti-rollback gates.
4. D completes executable lineage membership, late-discovery and final release CAS evidence.
5. Storage proves the bidirectional COC participant ↔ I/D/C owner admission Join and same-GID RecoveryJoin.
6. A performs a fresh exact-version integration review of this v3.2.6 bundle and issues a DO NOT FREEZE / conditional disposition as appropriate.
7. Only after all actual evidence predicates close may the project consider Gate B/C or production activation.

## 12. Provenance / 来源说明

This manifest was authored in delegated Storage-role mode. Every listed Blob was obtained from the named branch/file readback during this session. This is a version-binding and review-routing artifact, not an independent Storage Owner signature. No runtime deployment or production test was performed.

本清单由协调会话模拟 Storage 角色编写。所有 Blob 均从本轮指定分支/文件读回获取。本文件仅是版本绑定与复审路由工件，不是独立 Storage Owner 签名。本轮未执行 Runtime 部署或生产测试。
