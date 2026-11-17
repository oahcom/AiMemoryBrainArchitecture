# Cross-Owner Canonical Semantics Matrix
# 跨 Owner 规范语义矩阵

- ID: B-XOWN-001
- Status: FIRST-PASS RECONCILIATION; B3 OPEN
- Baseline main HEAD: b372b62c640a2b656e54b6db62a4ee67d7d8c001
- Scope: A/C/D/E/F/G/H/I/Storage/Testing; source artifacts pinned below by exact Blob SHA where fetched.

## 1. Source evidence ledger / 来源证据登记

| Owner | Artifact | Branch | Blob SHA | Observed status |
|---|---|---|---|---|
| B | 02-domain-model/phase-3.6-typed-identity-trust-closure.md | session-b-domain-model-phase3 | 0a6b78a842e550b58533b797cdfcd2d954ed6826 | Joint technical baseline; consumer/governance/implementation gates open |
| B | 02-domain-model/phase-3.8.6-b-storage-serialization-anchor-nominal-types.md | session-b-domain-model-phase3 | e2bc4c8dde9706bfbe443269b702f1b5aa6965f6 | B delegated technical approval of per-authority nominal type boundary only |
| B | B Owner ADRs on `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` (summary `a1024938ff5baba069cf128c69496a44e143330c`; detailed `df77e4a93cb8fef689ae7c828888d960cbf381d6`) | research reconciliation ADR Blob `958e7f3a3a909ee5b6d9fb38ebf3a72b3a9bd593` | Option A preferred candidate; ADR-BLOCKED / NOT APPROVED / NOT SCHEMA-FROZEN; stable ClaimRef + ClaimRevisionRef candidate |
| C | 07-agent-integration/phase-3.6-final-request-evidence-contract.md | session-c-agent-integration-2026-11-16 | fd2f47ba6c89bb270e9f2bec956873cb7ae3592b | C semantic decisions; C/G/H freeze blocked |
| C | 07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md | session-c-agent-integration-2026-11-16 | 45a48249717c8cddb07ab96197730ef93d406c22 | C amendment specified; coordinator and cross-owner acceptance open |
| D | 03-memory-brain/forget-fence-operation-and-publication-gate.md | session-d-memory-brain-2026-11-16 | 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5 | D operation semantics decided; interface/Storage realization open |
| D | 03-memory-brain/forget-fence-and-completion-contract.md | session-d-memory-brain-2026-11-16 | 1f0391bc49d007c44ec74165bd33d37412cc7990 | D canonical semantics decided; global completion I-owned |
| D | 03-memory-brain/commit-cursor-semantics.md | session-d-memory-brain-2026-11-16 | 4688a0ca487bf4d853c7f0220408abe8d743d159 | Canonical cursor semantics decided; engine/conformance open |
| E | 04-memory-compiler/compiler-state-and-producer-admission.md | session-e-memory-compiler-2026-11-16 | e59f517fff161ab882aa0ddc4a5bda513964ae1a | Candidate E lifecycle; D semantics decided; Storage realization open |
| E | 04-memory-compiler/forget-fence-and-derived-registration.md | session-e-memory-compiler-2026-11-16 | 00e37ba56596e710513c8d0568acd79141d9101b | Candidate enforcement; publication gate blocking |
| E | 04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md | session-e-memory-compiler-2026-11-16 | 4fb9e58511941f59b4d777336f8f85ad88ecccf1 | E-local proposal; cross-owner schemas open |
| F | 05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md | session-f-memory-runtime | 29e9504c75d737c2dd200ebc3306eda555f0b0ac | F-local proposal; interfaces/implementation open |
| G | 06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md | session-g-memory-context | aa3afa73d8a76cc6f025839c52bfbff6a983046a | G semantics recorded; C/G/H freeze blocked |
| G | 06-memory-context/phase-3.7-g-local-lifecycle-producer-derivative-queue-recall-context-restore.md | session-g-memory-context | c1de241ec69834377d9b0e24aa4770a809796d4b | G-local proposal; interfaces open |
| H | 08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md | session-h-bmcp-protocol | e7ca5ce4ece5d8fd77fe0760e49a85afa0133248 | Joint technical baseline; governance/consumer acceptance open |
| H | 08-bmcp-protocol/adapter-capability-and-applied-attestation.md | session-h-bmcp-protocol | 74be8374a67da385a5f0f8e34c7aef2b38b72bcf | Candidate; final proof and authorization binding open |
| I | 09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md | session-i-security-governance-2026-11-16 | 0cbf6bb7480db873790c454817593a9b1c5548ba | Technical baseline joint-decided; governance blocked |
| I | 09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md | session-i-security-governance-2026-11-16 | 17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c | Candidate policy contract; governance blocked |
| I | 09-security-governance/global-forget-target-inventory-and-completion-evidence.md | session-i-security-governance-2026-11-16 | 9100061fa986fb6676656169de3fcf9fc1c72664 | Candidate; cross-owner conformance open |
| Storage | reviews/storage-consistency/forget-atomicity-storage-realization-review.md | session-storage-consistency-forget-atomicity-2026-11-16 | 107d21bd2c604ee0b04feff2ee5580e1de9c7fce | Proposed realization; not implemented/verified |
| Storage | reviews/storage-consistency/phase-3.6.2-jf10-cross-authority-recovery-protocol.md | session-storage-consistency-forget-atomicity-2026-11-16 | 94679897e84a6f58fd8b9467b5249e1a885cb0b0 | DE-S proposal; I acceptance required; JF-10 P0 open |
| A | reviews/integration/phase-3.6-cgh-applied-contract-decision-package.md | session-a-integration-2026-11-16 | 122b164bcc0760b83bf555072a36fc55631623e1 | Decision request; C/G/H approvals not recorded |
| A | reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md | session-a-integration-2026-11-16 | 4961ffefc0f9920efb8425a9b2a7af42d8f64819 | Candidate package; owner review required; not frozen |

Branch tips/commit SHAs are NOT VERIFIED for the live owner branches in this matrix; only the exact fetched Blob SHAs are asserted. Issue #21's G phase 3.7 pin is an older Blob (d6d18684ba8a31a538e2e719be3f6e1b715cadf8); the current fetched branch file is c1de241ec69834377d9b0e24aa4770a809796d4b. Do not carry older acceptance/pins forward.


## 1A. Current branch heads and latest Phase 3.8 source pins / 当前分支 HEAD 与最新 Phase 3.8 来源 Pin

| Owner | Current branch HEAD | Latest exact review artifact | Blob SHA | Finding |
|---|---|---|---|---|
| B | 2faf8ec38f14dba49e7263d7a60804dae1a74ee2 | phase-3.8.6-b-storage-serialization-anchor-nominal-types.md | e2bc4c8dde9706bfbe443269b702f1b5aa6965f6 | Approves per-authority nominal type boundary with clarifications; delegated role review, not independent human signature; L1/L2 only |
| C | 2e8414f361b0b5d7de959be8a971aadc9e62d6a9 | phase-3.8.22-c-exact-review-h-authenticated-ingress-1.2.14-60-tests.md | 8fd6052cabf58a78962cc2e776398b2a40604bcd | Accepts H reference gate/test boundary; signer/attestation open; not crypto-frozen; 60 tests are deterministic callback orchestration evidence |
| D | 76fcc92225666a11893b7241825261319edb621e | phase-3.8.13-d-review-h-outer-envelope-authenticated-ingress-gate.md | 152627e00b96355e2ff370acd643a51168c4c78c | Accepts H as upstream interface only; D Forget/RecoveryJoin authority unchanged |
| E | ee098e14747d9915de5b3efb63b3a8dd77f670ed | phase-3.8.6-e-review-storage-serialization-anchor.md | 19d708bc29b6115d7bccb7d320781f452ee28b78 | Accepts anchor with E lifecycle conditions; implementation L4 open |
| F | 1908ce4d233b20f7cafd00cb679affd01bd15174 | phase-3.8.6-f-review-storage-serialization-anchor.md | 122238146830db6188f00a9788e018a82bfb3f90 | Accepts anchor with read-path/cache conditions; implementation L4 open |
| G | 3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe | phase-3.8.18-g-exact-review-h-unified-1.2.14-csubmitoutcome-1.0.1-fullpath.md | 1894860c76336f8739d354b72beed3992cffd17e | Accepts bounded L1/L2 C/H consumer mapping with G-owned Applied conditions; NOT FROZEN; 38-method full-path fixture still uses ten deterministic authority test doubles |
| H | 8e24342048d29ef29195b153b8b9ec53ba7c75d9 | phase-3.8.20-h-exact-c-envelope-p0-correction-and-json-pointer-mapping.md | 4ba7e1699215d02224f805a15484b1da2e40c03f | Corrects C P0 proof-locator omission; mapping candidate; executable authentication still open |
| I | 2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9 | phase-3.8.18-i-review-c-outer-envelope-signer-p0-trust-registration.md | b6d1ea45825a1c2090abfba42474814f02f073a3 | Accepts separation/signer ownership as candidate; crypto suite and trust registration not approved |
| Storage | 431138e7c7af8bee716f3d8dcbc20114c046bd36 | phase-3.6.21-storage-v3.2.11-exact-version-bundle-manifest.md | 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57 | Exact candidate bundle bound; C/H/I/D reviews recorded; fresh A review required; not jointly accepted/frozen |
| A | 9bdf938b980413f592a4db9fe94f4bf2c299fb01 | phase-3.8.19-a-review-h-outer-envelope-authentication-c-i-boundary.md | e12cd7b5c79e2234178014243fd51f2e7d51272e | Accepts outer-envelope auth as a blocking architecture gap; do not freeze |

## 1B. New cross-owner identity and ingress boundaries / 新的跨 Owner 身份与入口边界

- B's per-authority serialization anchor review approves distinct physical nominal types, but the anchor is an implementation primitive, not a canonical domain entity or global counter.
- C owns origin-signed message semantics and exact C envelope P0; H owns wire extraction/verification; I owns trust profile, issuer/key registration, revocation, anti-rollback and authorization; Storage owns durable authenticated ingress/replay persistence. H does not become C signer; I does not rewrite C P0; a gateway attestation is distinct from C origin signature.
- The H 1.2.14 / CSubmitOutcome 1.0.1 reference ingress path is not production authentication. H 60-test CI uses deterministic callback doubles; G's 38-method full-path fixture also uses deterministic authority doubles. H P0 extraction/signature verification, production trust registry, durable replay, C envelope signer profile and Storage durable ingress are still open.
- A's current Phase 3.8.19 review explicitly marks this as a blocking architecture gap. This issue supersedes older summaries that described only a 42-test local validator gap; the 42-test scope remains valid only for its original limited C-object/local-validation claim.

- B 的 per-authority Serialization Anchor 复审批准不同物理名义类型，但 Anchor 属于实现原语，不是规范领域实体或全局计数器。
- C 负责 Origin-signed Message 语义和精确 C Envelope P0；H 负责 Wire 提取/验证；I 负责 Trust Profile、Issuer/Key 注册、撤销、Anti-rollback 和授权；Storage 负责认证后持久 Ingress/Replay。H 不成为 C Signer；I 不得改写 C P0；Gateway Attestation 与 C Origin Signature 不同。
- H 1.2.14 / CSubmitOutcome 1.0.1 Reference Ingress 路径不是生产认证。H 60 项 CI 使用确定性 Callback Double；G 的 38 项 Full-path Fixture 也使用确定性 Authority Double。H P0 提取/签名验证、生产 Trust Registry、持久 Replay、C Envelope Signer Profile 和 Storage Durable Ingress 仍未完成。
- A 当前 Phase 3.8.19 复审明确将其列为阻塞性架构缺口。这一问题更新了旧摘要：42 项本地 Validator 测试仅在其原始 C-object/本地校验范围内有效。

## 1C. Chinese current-owner source-pin ledger / 中文当前 Owner 来源 Pin 台账

| Owner | Branch HEAD | Exact review artifact and Blob / 精确复审工件与 Blob | 中文发现 / Chinese finding |
|---|---|---|---|
| B | 2faf8ec38f14dba49e7263d7a60804dae1a74ee2 | phase-3.8.6 B serialization anchor; e2bc4c8dde9706bfbe443269b702f1b5aa6965f6 | B 仅批准 Per-authority 名义类型边界；Anchor 是物理实现细节，不是规范实体/全局计数器。 |
| C | 2e8414f361b0b5d7de959be8a971aadc9e62d6a9 | phase-3.8.22 C H authenticated ingress review; 8fd6052cabf58a78962cc2e776398b2a40604bcd | C 接受 H Reference Gate/测试边界；Signer/Attestation 和 Crypto Profile 仍未关闭；60 项测试使用确定性 Callback Double。 |
| D | 76fcc92225666a11893b7241825261319edb621e | phase-3.8.13 D outer-envelope review; 152627e00b96355e2ff370acd643a51168c4c78c | D 只接受 H 作为上游接口；D Forget/RecoveryJoin 权威不变。 |
| E | ee098e14747d9915de5b3efb63b3a8dd77f670ed | phase-3.8.6 E serialization review; 19d708bc29b6115d7bccb7d320781f452ee28b78 | E 在自身生命周期条件下接受 Anchor；L4 实现仍开放。 |
| F | 1908ce4d233b20f7cafd00cb679affd01bd15174 | phase-3.8.6 F serialization review; 122238146830db6188f00a9788e018a82bfb3f90 | F 在读路径/Cache 条件下接受 Anchor；L4 实现仍开放。 |
| G | 3367438f7b6ba5fa1b7d7540a0fd03a72bbebdbe | phase-3.8.18 G H/CSubmitOutcome full-path review; 1894860c76336f8739d354b72beed3992cffd17e | G 接受有限 L1/L2 C/H 消费者映射并保留 G Applied 谓词；NOT FROZEN；38 项测试使用 10 个确定性 Authority Double。 |
| H | 8e24342048d29ef29195b153b8b9ec53ba7c75d9 | phase-3.8.20 H C-envelope P0 correction; 4ba7e1699215d02224f805a15484b1da2e40c03f | H 修正 C P0 Proof Locator 缺失并记录 JSON Pointer；可执行认证仍开放。 |
| I | 2afe0e17f8c0929d9e642ccbe2cad112b5fd43a9 | phase-3.8.18 I C origin-signer review; b6d1ea45825a1c2090abfba42474814f02f073a3 | I 接受 Signer Ownership 分离为候选；Crypto Suite/Trust 注册未批准。 |
| Storage | 431138e7c7af8bee716f3d8dcbc20114c046bd36 | Storage v3.2.11 exact manifest; 54a4f0dab7ab24f1f6fb01f8cc5c7da292f02c57 | 精确候选包已绑定 C/H/I/D 复审；仍未联合接受/冻结，需 A 新审查。 |
| A | 9bdf938b980413f592a4db9fe94f4bf2c299fb01 | phase-3.8.19 A outer-envelope auth review; e12cd7b5c79e2234178014243fd51f2e7d51272e | A 将外层 Envelope Authentication 明确标记为阻塞架构缺口，要求不得冻结。 |

## 1D. Chinese historical contract evidence summary / 中文历史契约证据摘要

- **B：** Phase 3.6 Typed Identity Trust Closure（Blob 0a6b78...）建立类型化身份技术基线；当前 Formal Actor/Scope/Environment Type Mapping Blob 3a1e77889cd9a90cd5822d9f0cb3437880868706 已正式批准对应类型语义。当前 B Owner ADR 推荐 Option A 作为候选（摘要 Blob a1024938...；详细 Blob df77e4...）；研究包旧 C2 建议已被取代。Option A 仍 ADR-BLOCKED，不构成最终决策。
- **C：** Final Request Evidence Contract（Blob fd2f47...）区分真实 Final Request 与传输 ACK；CSubmit Cross-authority Causal Order Contract（Blob 45a482...）仍需跨 Owner 因果顺序和 Storage 接受。
- **D：** Forget Fence/Completion Contract（Blob 1f0391...）规定 D 规范抑制和完成证明；Commit Cursor Semantics（Blob 4688a0...）由 D 拥有，不能与其他 Owner Epoch/Cursor 混用。
- **E：** Compiler State/Producer Admission（Blob e59f51...）和 Forget Fence/Derived Registration（Blob 00e37b...）定义 Compiler 侧准入/派生登记；Storage Publication Gate 仍阻塞。
- **F：** Phase 3.7 Local Lifecycle/Queue/Recall/Context Restore（Blob 29e950...）是 F 局部提案，不能替代 G ContextVersion 或规范 Memory。
- **G：** Applied Forget Reconciliation Contract（Blob aa3afa...）由 G 拥有 Applied 记录；ContextVersion/ChangeSet 与 MemoryVersion 不同。
- **H：** Protected Operation Binding（Blob e7ca5c...）和 Adapter Capability/Applied Attestation（Blob 74be83...）是候选协议边界；ACK 仅证明其声明的有限后置条件。
- **I：** Identity Trust Policy Joint Closure（Blob 0cbf6b...）技术基线已共同决定，但 I36 外部治理仍阻塞；Global Forget Target Inventory（Blob 910006...）仍候选。
- **Storage：** Forget Atomicity Realization Review（Blob 107d21...）和 JF-10 DE-S Proposal（Blob 946798...）仍是提案/未实现证据，不能宣称物理擦除或跨权威原子性已证明。
- **A：** CGH Applied Decision Package（Blob 122b16...）和 CGH-APPLIED-1.1 Causal Order Package（Blob 4961ff...）记录集成裁决/候选包；必须以各 Owner 精确版本批准为准。

## 2. Semantic matrix / 语义矩阵

| Concept | B canonical position | Owner-local position | Status / conflict |
|---|---|---|---|
| Memory identity/version | Stable Memory identity; immutable MemoryVersion identity; content change does not change Memory ID | D owns canonical Memory/revision/cursor and lifecycle; Storage persists | Compatible in principle; exact aggregate/transaction contract D/Storage-owned |
| Claim / Fact | Claim is an attributable proposition; Fact is a candidate independent attestation object under current B recommendation; epistemic status remains orthogonal | E extracts/derives; D owns canonical identity/commit after approval; F/G consume exact version-pinned refs | **BLOCKING for schema freeze**: B currently prefers Option A only as CANDIDATE; formal Architecture Governance approval is absent. I-04/P-04, overview and terminology still conflict; bilingual guides retain ADR-BLOCKED. Option B would require explicit governance amendment. |
| Entity / Relation | Entity has stable identity; Relation is typed, directed/symmetric, scoped, temporal, evidenced | E derives candidates; F graph/index projections; G consumes selected refs | No direct contradiction found; typed Relation must not collapse into co-occurrence |
| Source / Evidence / Provenance | Source origin, Evidence material, Provenance derivation trace | E emits source/derivation lineage; D tracks canonical dependencies; I controls access/retention | Compatible core; graph-cycle/retention/identity granularity OPEN |
| Principal / ActorRef / Domain Entity | Distinct typed identity; Ref is not authentication or permission | I resolves Principal/trust/delegation; H authenticates transport; B owns typed refs; C/D/E/G bind operation context | B formally APPROVED its semantic mapping; C/F/G BIH consumer decisions ACCEPT WITH ENUMERATED EXCEPTIONS and H ACCEPTED exact BIH package (Issue #6 closed, exact package Blob a45ae90b318a79bf009d14f4d917611881e9e214); I36 governance remains blocked |
| Scope / Tenant / Workspace / Environment | ScopeRef is typed namespace/ownership/applicability boundary; Scope not Permission; EnvironmentRef distinct | I owns Scope isolation/policy; G binds context scope; C/H transport typed refs; B owns reference semantics | **HIGH**: exact Tenant/Workspace/Project/Environment taxonomy and registry authority incomplete |
| Session / Conversation / RuntimeSessionRef | RuntimeSessionRef is authenticated bounded runtime session, not necessarily Conversation or Session Scope | C/G/H define runtime/session/conversation use; H owns session binding | **HIGH**: terms must not alias; full canonical session/conversation relation unresolved |
| Context / ContextVersion / ChangeSet | Context is G-owned task-scoped desired view; ContextVersion separate from MemoryVersion; ChangeSet G-owned | G owns Context and Applied records; F Working Set; E compiler input bundle distinct | Compatible direction; G exact schema and state transitions require further pinning; no scalar version alias |
| Retrieval / Activation / Working Set | Runtime-derived view/process, not canonical Memory truth | F owns ranking, index/cache, Working Set and final gate; G selects membership | Compatible; must keep F Working Set distinct from G ContextVersion |
| Operation / Protocol Message / Receipt | Operation identity/state distinct from Request/Response/Command/ACK | H owns wire/ACK; C owns provider submit; D/I own fences/auth; Storage owns receipt | **HIGH**: operation identity and cross-authority participant references require exact contracts; ACK never upgrades to Applied |
| Applied | Historical per-request Context application fact committed only by G under full predicate; no attention/comprehension claim | C emits actual final-request evidence; H transports; I/D provide authorization/fence; G validates and commits | **BLOCKING**: exact CGH-APPLIED-1.1 recovery-batch decisions are recorded by C/D/G/H/I/B with enumerated exceptions and Storage confirmed interface with changes (Issue #3 comments 6920620910 / 6929521979); Applied Contract Frozen remains NO. G 38-method full-path fixture and H 60-test CI are bounded local evidence using deterministic authority callbacks/test doubles; production trust, provider truth/idempotency, COC quorum durability, Storage same-GID recovery, G Applied persistence and end-to-end L3/L4 remain NOT VERIFIED / NOT RUN. A I-10 wording should be clarified as Adapter ACK necessary but insufficient. |
| Recorded / Committed / Visible / Published | Distinct typed outcome semantics; no universal total order | Owner records evidence; D canonical cursor; Storage authoritative pointer/receipt; E terminalizes after receipt | **BLOCKING** for JF-10 publication: I COMMIT_WON != Storage PUBLISHED; implementation/physical capability not verified |
| Forget / Forgotten / Deleted / Purged | Memory Forgotten is lifecycle state; ForgetOperation distinct; logical suppression not physical purge | D operation/fence/barrier; I global completion/retention; Storage/backup physical erasure; G/F/H local cleanup | **BLOCKING** for global completion/physical purge; no single owner can claim global success |
| Event Time / Observed At / Recorded At / Valid Time | Distinct temporal dimensions; valid-time and record-time history retained | C/E capture source times; D commit cursor; Storage transaction time | Compatible conceptually; exact Record vs Transaction Time field authority and fuzzy-time encoding OPEN |
| Provider Outcome / Final Request Submitted | Execution/provider boundary evidence is not a generic Event or protocol ACK | C alone emits actual provider submit outcome; H transports; G consumes | Compatible; provider outcome semantics and exact causal order remain C/I/D/Storage dependencies |
| Outer Envelope Authentication / C Origin Signature | Authentication proof and origin-signed message semantics are separate from ActorRef/PrincipalRef payload references | C owns origin signer/P0; H extracts/verifies wire; I owns profile/trust/key lifecycle; Storage owns durable authenticated ingress/replay | **BLOCKING**: H reference gate only; C signer/P0 candidate; I crypto suite/trust registration not approved; A says do not freeze |
| Serialization Anchor / SerializationRevision | Physical per-authority serialization primitive, not a canonical domain identity or global clock | B approves nominal type boundaries; Storage owns physical anchor; E/F accept with conditions; D/I/C/COC counters remain distinct | HIGH: Storage v3.2.11 exact candidate bundle not jointly accepted/frozen; fresh A review and L4 DB/HA/recovery proof open |
| Audit / Governance Decision / Consent / Forget Request | Distinct records, not Memory lifecycle flags | I owns policy, approvals, audit and global Forget | B must not absorb these into generic state; I36 external approvals still blocked |

## 3. Exact owner boundaries / Owner 权威边界

- A: cross-module integration, contract registry and system-level dependency; cannot approve another Owner's semantic decisions.
- B: canonical domain vocabulary, typed references and domain relationship/time/evidence meaning.
- C: actual final request/provider submit boundary and immutable CSubmitOutcome.
- D: canonical Memory lifecycle, ForgetOperation/Fence, producer registration/barrier, canonical commit cursor and dependency lineage.
- E: compiler ingress/work/derivation/attempt and output staging; cannot declare artifact Published.
- F: retrieval/index/cache/Working Set and runtime final suppression; cannot mutate canonical Memory or G Applied.
- G: desired Context, ContextVersion, ChangeSet, Delivery, Applied record and current-use projection; cannot claim provider submit or global Forget.
- H: BMCP wire, transport authentication integration, ACK, capability and reconnect; ACK only proves declared bounded postcondition.
- I: issuer trust, Principal, authorization, delegation, revocation, PermissionEpoch, retention and global Forget policy/completion.
- Storage: durable transaction/visibility pointer/receipt and physical storage capability; current package is proposal, not implementation evidence.
- Testing/QA: cross-cutting conformance and fault-injection execution coordinated by A; B owns TC-01 Domain Identity and References and TC-10 Provenance/Lifecycle/Temporal test semantics. No dedicated Testing/Quality branch or independent accountable Owner was found. Independent test executor/reviewer still must be appointed.

## 4. Conflict severity / 冲突等级

- BLOCKING: prevents a cross-owner canonical contract or architecture freeze.
- HIGH: affects identity/scope/security or correctness but may be locally isolated with fail-closed gate.
- MEDIUM: ambiguity/complexity needing resolution before affected implementation.
- LOW: terminology/documentation issue with no immediate invariant break.
- INFORMATIONAL: compatible variation or documented boundary.

## 5. Current conflict summary / 当前冲突摘要

1. **XOWN-BLOCK-001 — Fact/Claim:** main overview and guide disagree on decision status; preserve ADR-BLOCKED. Owners B/D/E; A registry; Gate B2/B3.
2. **XOWN-BLOCK-002 — Applied:** G owns Applied record, C actual submit proof, H wire, I authorization, D fence. Exact CGH-APPLIED-1.1 recovery-batch decisions are recorded by C/D/G/H/I/B with enumerated exceptions and Storage confirmed interface with changes; Applied Contract Frozen remains NO and production proof is NOT VERIFIED. Gate B3.
3. **XOWN-BLOCK-003 — JF-10 publication:** I COMMIT_WON, Storage owner commit and Published receipt are separate; current DE-S protocol is proposal and JF-10 P0 remains open. Gate B3/B4 and A system gate.
4. **XOWN-BLOCK-004 — Global Forget:** D canonical suppression proof is not I global completion or Storage physical purge. I inventory seal/governance approvals are missing; Gate B3.
5. **XOWN-HIGH-001 — Scope taxonomy:** Tenant/Workspace/Project/Environment/ownership/applicability scope need I/A registry decision; fail closed for ambiguous cross-scope references.
6. **XOWN-HIGH-002 — Claim identity:** Claim ID vs version-local ClaimSnapshot not settled; do not freeze Schema.
7. **XOWN-HIGH-003 — Temporal axes:** Record Time vs Transaction Time and uncertain-time encoding need B/D/Storage agreement.
8. **XOWN-HIGH-004 — Context identity/state:** ContextVersion, F Working Set, E compiler input bundle, MemoryVersion and Applied are distinct; exact G schemas/predicates still require consumer acceptance.
9. **XOWN-MED-001 — Provenance identity/cycles:** edge record vs provenance object granularity and graph cycle policy remain open.
10. **XOWN-MED-002 — Source/Observation/Evidence:** confirm whether Source is first-class entity or typed origin ref; Evidence has its own identity.
11. **XOWN-BLOCK-005 — Outer-envelope authenticated ingress:** C origin signer/P0, H extraction/verification, I trust/profile/key lifecycle and Storage durable replay must close as one exact-version boundary; current H reference gate and local test doubles are insufficient. Owner authority C/H/I/Storage; A integration; blocks Gate A/B and production ingress.
12. **XOWN-HIGH-005 — Per-authority serialization anchor:** B-approved nominal type distinctions are not a physical implementation decision; Storage v3.2.11 is not jointly accepted/frozen, and fresh A review plus L4 proof are required.

## 2A. Chinese semantic matrix mirror / 中文语义矩阵对照

| Concept / 概念 | B 规范立场 / B Canonical Position | Owner 局部权威 / Owner-local Authority | Status and conflict / 状态与冲突 |
|---|---|---|---|
| Memory identity/version / Memory 身份与版本 | Memory 身份稳定；MemoryVersion 不可变；内容变化不改变 Memory ID。 | D 拥有规范 Memory/Revision/Cursor 和生命周期；Storage 持久化。 | 原则兼容；精确 Aggregate/Transaction 契约由 D/Storage 决定。 |
| Claim / Fact / Claim 与 Fact | Claim 是命题，认知状态独立；Fact 是不同概念，但其独立对象身份/类型还是限定 Claim 表示仍 ADR-BLOCKED。 | E 抽取/派生；D 存储规范 Memory；F/G 消费投影/Context。 | **Schema 冻结 BLOCKING**：保留 I-04 概念区分；Fact/Claim 身份与表示未决；A PR #53 已关闭但未合并，结论 DEFERRED。 |
| Entity / Relation / 实体与关系 | Entity 具有稳定身份；Relation 必须类型化、有方向/Scope/时间/Evidence。 | E 派生候选；F 建立图/索引投影；G 消费选定引用。 | 未发现直接矛盾；类型化 Relation 不得退化为共现边。 |
| Source / Evidence / Provenance / 来源、证据与溯源 | Source 是来源起点；Evidence 是支持材料；Provenance 是派生轨迹。 | E 生产来源/派生谱系；D 跟踪规范依赖；I 控制访问/保留。 | 核心兼容；图循环、保留和身份粒度仍 OPEN。 |
| Principal / ActorRef / Domain Entity / Principal、ActorRef 与领域实体 | 身份类型不同；Ref 不等于认证或权限。 | I 解析 Principal/Trust/Delegation；H 认证传输；B 定义类型化引用；C/D/E/G 绑定操作上下文。 | B 类型映射已正式批准；C/F/G 的 BIH 消费者设计 ACCEPT WITH EXCEPTIONS，H 接受精确包（Issue #6 已关闭）；I36 治理仍阻塞。 |
| Scope / Tenant / Workspace / Environment / 作用域与隔离域 | ScopeRef 是类型化命名空间/所有权/适用边界；Scope 不等于 Permission；EnvironmentRef 独立。 | I 管理隔离/策略；G 绑定 Context Scope；C/H 传输类型化引用；B 定义引用语义。 | **HIGH**：Tenant/Workspace/Project/Environment 精确分类和 Registry 权威未完成。 |
| Session / Conversation / RuntimeSessionRef / 会话与对话 | RuntimeSessionRef 是认证后的有界 Runtime Session，不必然等于 Conversation 或 Session Scope。 | C/G/H 定义 Runtime/Session/Conversation 用法；H 拥有 Session 绑定。 | **HIGH**：术语不得别名化；规范 Session/Conversation 关系未决。 |
| Context / ContextVersion / ChangeSet / 上下文与变更集 | Context 是 G 拥有的任务级期望视图；ContextVersion 与 MemoryVersion 分离；ChangeSet 由 G 拥有。 | G 管理 Context 和 Applied；F 管 Working Set；E 的 Compiler Input Bundle 独立。 | 方向兼容；G 精确 Schema/状态转换仍需 Pin；不得复用标量版本号。 |
| Retrieval / Activation / Working Set / 检索、激活与工作集 | Runtime 派生视图/过程，不是规范 Memory 真值。 | F 管 Ranking、Index/Cache、Working Set 和最终 Gate；G 选择 Context 成员。 | 兼容；F Working Set 必须与 G ContextVersion 分离。 |
| Operation / Protocol Message / Receipt / 操作、协议消息与回执 | Operation 身份/状态与 Request/Response/Command/ACK 分离。 | H 管 Wire/ACK；C 管 Provider Submit；D/I 管 Fence/Auth；Storage 管 Receipt。 | **HIGH**：操作身份和跨权威参与方引用需精确契约；ACK 永不自动升级为 Applied。 |
| Applied / 已应用 | G 在完整谓词满足后，对精确 ContextVersion 进入精确提交请求的历史证明；不声称模型注意或理解。 | C 提供真实 Final Request 证据；H 传输；I/D 提供授权/Fence；G 验证并提交。 | **BLOCKING**：CGH-APPLIED-1.1 设计决策已有例外记录，但 Frozen=NO；38/60 项本地测试使用确定性 Authority Double，生产信任、Provider 真值、COC、Storage same-GID、G Applied 持久化和 L3/L4 未验证。 |
| Recorded / Committed / Visible / Published / 已记录、已提交、可见、已发布 | 四者语义不同，不存在默认全局总序。 | Owner 记录证据；D 规范 Cursor；Storage 拥有 Pointer/Receipt；E 在 Receipt 后终态化。 | **BLOCKING**：I COMMIT_WON 不等于 Storage PUBLISHED；JF-10 物理能力/实现未验证。 |
| Forget / Forgotten / Deleted / Purged / 遗忘、已遗忘、删除、清除 | Forgotten 是 Memory 生命周期状态；ForgetOperation 独立；逻辑抑制不等于物理 Purge。 | D Operation/Fence/Barrier；I 全局完成/保留；Storage/备份物理擦除；G/F/H 局部清理。 | **BLOCKING**：全局完成/物理擦除无单一 Owner 可宣称成功。 |
| Event Time / Observed At / Recorded At / Valid Time / 事件、观察、记录、有效时间 | 时间维度必须区分；保留 Valid Time 和 Record Time 历史。 | C/E 捕获来源时间；D 管 Commit Cursor；Storage 管 Transaction Time。 | 概念兼容；Record vs Transaction Time 字段权威及模糊时间编码仍 OPEN。 |
| Provider Outcome / Final Request Submitted / Provider 结果与最终请求提交 | 执行/Provider 边界证据不等于通用 Event 或 Protocol ACK。 | 只有 C 发出真实 Provider Submit Outcome；H 传输；G 消费。 | 兼容；精确因果顺序仍依赖 C/I/D/Storage。 |
| Outer Envelope Authentication / C Origin Signature / 外层认证与 C 来源签名 | 认证证明和来源签名语义与 ActorRef/PrincipalRef 载荷引用分离。 | C 拥有 Origin Signer/P0；H 提取/验证 Wire；I 拥有 Profile/Trust/Key 生命周期；Storage 持久化认证入口/Replay。 | **BLOCKING**：H 仅有 Reference Gate；C Signer/P0 候选；I Crypto Suite/Trust 注册未批准；A 要求不得冻结。 |
| Serialization Anchor / SerializationRevision / 序列化锚点与修订号 | 每 Authority 物理序列化原语，不是规范领域身份或全局时钟。 | B 批准名义类型边界；Storage 拥有物理 Anchor；E/F 有条件接受；D/I/C/COC 计数器保持独立。 | **HIGH**：Storage v3.2.11 候选包未联合接受/冻结；需 A 新审查及 L4 DB/HA/恢复证明。 |
| Audit / Governance Decision / Consent / Forget Request / 审计、治理决定、同意与遗忘请求 | 是不同记录，不是 Memory 生命周期标志。 | I 拥有策略、批准、审计和全局 Forget。 | B 不得将其吸收到通用 State；I36 外部治理批准仍阻塞。 |

## 3A. Chinese owner boundaries / 中文 Owner 权威边界

- **A：** 负责跨模块集成、契约注册和系统级依赖；不能批准其他 Owner 的语义决定。
- **B：** 负责规范领域词汇、类型化引用以及领域关系/时间/Evidence 语义。
- **C：** 负责真实 Final Request/Provider Submit 边界及不可变 CSubmitOutcome。
- **D：** 负责规范 Memory 生命周期、ForgetOperation/Fence、Producer Registration/Barrier、规范 Commit Cursor 和依赖谱系。
- **E：** 负责 Compiler Ingress/Work/Derivation/Attempt 和 Output Staging；不能宣称 Artifact Published。
- **F：** 负责 Retrieval/Index/Cache/Working Set 和 Runtime 最终抑制；不能修改规范 Memory 或 G Applied。
- **G：** 负责期望 Context、ContextVersion、ChangeSet、Delivery、Applied Record 和当前使用投影；不能宣称 Provider Submit 或全局 Forget。
- **H：** 负责 BMCP Wire、传输认证集成、ACK、Capability 和 Reconnect；ACK 只证明其声明的有界后置条件。
- **I：** 负责 Issuer Trust、Principal、Authorization、Delegation、Revocation、PermissionEpoch、Retention 和全局 Forget 策略/完成。
- **Storage：** 负责持久事务、Visibility Pointer/Receipt 和物理存储能力；当前包仍是提案，不是实现证据。
- **Testing/QA：** 属于 A 协调的横切一致性/故障注入执行方；B 负责 TC-01 和 TC-10 测试语义。尚未找到独立 Testing/Quality 分支或独立负责 Owner，仍需指定独立执行/审查人员。

## 4A. 中文冲突严重级别

- **BLOCKING：** 阻止跨 Owner 规范契约冻结或架构 Gate。
- **HIGH：** 影响身份、Scope、安全或正确性；在隔离路径上可 Fail Closed。
- **MEDIUM：** 在相关实现开始前必须解决的歧义/复杂度。
- **LOW：** 不立即破坏不变量的局部术语/文档问题。
- **INFORMATIONAL：** 已记录的兼容差异或边界。

## 5A. 中文当前冲突摘要

1. **XOWN-BLOCK-001 — Fact/Claim：** I-04 要求 Fact 与 Claim 保持概念区分；Fact 是否独立对象或限定 Claim 表示仍 ADR-BLOCKED。Owner：B/D/E；A 维护 Registry；阻塞 B2/B3。
2. **XOWN-BLOCK-002 — Applied：** G 拥有 Applied Record；C 提供真实 Submit 证明；H 管 Wire；I 管授权；D 管 Fence。精确设计决策已有列明例外，但 Frozen=NO，生产证明未验证。阻塞 B3。
3. **XOWN-BLOCK-003 — JF-10 Publication：** I COMMIT_WON、Storage Owner Commit 和 Published Receipt 是不同事实；DE-S 仍是提案，JF-10 P0 未关闭。阻塞 B3/B4 和 A 系统 Gate。
4. **XOWN-BLOCK-004 — Global Forget：** D Canonical Suppression 证明不等于 I Global Completion 或 Storage Physical Purge；I Inventory Seal/治理批准仍缺。阻塞 B3。
5. **XOWN-HIGH-001 — Scope 分类：** Tenant/Workspace/Project/Environment/Ownership/Applicability Scope 需要 I/A Registry 决策；跨 Scope 歧义时 Fail Closed。
6. **XOWN-HIGH-002 — Claim 身份：** Claim ID 与版本局部 ClaimSnapshot 的关系未定；不得冻结 Schema。
7. **XOWN-HIGH-003 — 时间轴：** Record Time 与 Transaction Time 及不确定时间编码需 B/D/Storage 协调。
8. **XOWN-HIGH-004 — Context 身份/状态：** ContextVersion、F Working Set、E Compiler Input Bundle、MemoryVersion 和 Applied 均不同；G 精确 Schema/谓词仍需消费者验收。
9. **XOWN-MED-001 — Provenance 身份/循环：** 边记录还是 Provenance 对象、图循环策略仍 OPEN。
10. **XOWN-MED-002 — Source/Observation/Evidence：** 需确认 Source 是否为一等实体还是类型化来源引用；Evidence 自身具有身份。
11. **XOWN-BLOCK-005 — 外层认证 Ingress：** C Origin Signer/P0、H 提取/验证、I Trust/Profile/Key 生命周期和 Storage Durable Replay 必须形成一个精确版本边界；当前 H Reference Gate 和本地 Test Double 不足。Owner：C/H/I/Storage；A 集成；阻塞生产入口。
12. **XOWN-HIGH-005 — Per-authority Serialization Anchor：** B 批准的名义类型差异不代表物理实现批准；Storage v3.2.11 未联合接受/冻结，需要 A 新审查和 L4 证明。

## 6. B3 gate / B3 门禁

B3 is **NOT PASSED**. The matrix is based on exact fetched source Blobs, current branch HEAD snapshots and explicit issue acceptance requirements, but several owner acceptances remain conditional, branch HEADs may move and must be re-read, and cross-owner contracts remain candidate/not frozen. B3 cannot be marked complete by this B session's role simulation or A's synthesis.

B3 **未通过**。矩阵基于精确读取的源 Blob 和 Issue 中明确的 Owner 验收要求，但多个 Owner 验收仍明确开放、分支 Tip SHA 未核验、跨 Owner 契约仍为候选/未冻结。本 B 会话角色扮演或 A 的综合意见不能代替 B3 完成。


## 7. Live successor reconciliation — Storage topology and authenticated ingress / 实时后继协调 — Storage 拓扑与认证入口

| Semantic area / 语义领域 | Exact source evidence / 精确来源证据 | Owner authority / Owner 权威 | Current cross-owner disposition / 当前跨 Owner 结论 |
|---|---|---|---|
| Option A logical topology vs L4 physical realization / Option A 逻辑拓扑与 L4 物理实现 | ADR Blob `bb544ba2f346bdc130d524bd5c7310d86f367988`; Storage v3.3.1 Blob `f6e61691ecdcfcbf1fb423cc45242868676ca925`; corrected Storage v3.3.2 Blob `5c614375e10698e4931d83deb57d20321445e068`; A Phase 3.12.1 Blob `d3d4e6f4b6d7e82f90e3eee3427c8ace3b4160c8`; A Phase 3.12.2 Blob `eb3c946065aff4fbc6d76f384402fb9f75fa32dc` | Storage owns topology ADR/manifest; A owns integration review; B owns shared semantic consistency only. | **B-CONFLICT-017 CLOSED at manifest-consistency level.** v3.3.2 corrects Option A to selected normative v1 logical architecture and removes unsupported A-01–A-05. A Phase 3.12.2 accepts it as a consistent exact-version candidate with enumerated release blockers. Not independently human-approved, jointly accepted or frozen; L4 remains OPEN. |
| H authenticated-ingress schema successor / H 认证入口 Schema 后继版本 | H Unified 1.2.15 mapping Blob `2dc30f193d9c4f4bdc05ca4c137103687db28924`; H schema Blob `860fc4cec658db7d2703cd6adf72aa31a2723f6d`; I review Blob `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf`; Storage v3.3.2 Blob `5c614375e10698e4931d83deb57d20321445e068`; A review Blob `eb3c946065aff4fbc6d76f384402fb9f75fa32dc` | H owns wire/schema; I owns trust registration; C owns provider outcome and C-object P0; Storage owns durable ingress bundle; A integrates. | H/I 1.2.15 is a structural trust-carrier candidate only. Storage v3.3.2 and A 3.12.2 still bind H 1.2.14 / C 1.0.1 and predecessor C/I reviews. 1.2.15 is not retroactively accepted. Exact successor bundle, H P0/validator, I registration and fresh A review remain required. |
| Applied / Forget / current-use / Applied、Forget 与当前使用资格 | G current contract Blob `aa3afa73d8a76cc6f025839c52bfbff6a983046a`; D Phase 3.8.13 review Blob `152627e00b96355e2ff370acd643a51168c4c78c` | G owns Applied predicate/record; D owns ForgetFence/lineage/barrier; I owns authorization/PermissionEpoch; C owns final provider submit evidence; H owns transport. | **BLOCKING remains:** G Applied freeze and execution remain blocked/not verified; D clearance/lineage/barrier/release remain open; H ACK is insufficient; no Global Forget or physical purge claim. |
| C origin and outer-envelope signer separation / C 来源与外层 Envelope Signer 分离 | C Phase 3.8.22 review Blob `8fd6052cabf58a78962cc2e776398b2a40604bcd`; I Phase 3.8.22 review Blob `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` | C owns CSubmitOutcome object P0/provider truth; H owns outer wire/P0; I owns signer trust/profile/key registration. | C recommends but does not approve a distinct H gateway attestation. I accepts 1.2.15 schema shape only; exact P0, trust registry, signer approval and executable verifier remain OPEN. No implicit reuse of C-object signature. |

### 7.1 Owner-authority boundary / Owner 权威边界

A Phase 3.12.2 is a delegated A-role exact re-review of Storage v3.3.2, not an independent human A Owner signature. It directly verifies that the Option A wording and unsupported A-01–A-05 reference were corrected and accepts v3.3.2 as a consistent candidate manifest with enumerated blockers. Storage v3.3.2 itself is a delegated Storage-role coordination artifact, not an independent human Storage Owner signature. Therefore B-CONFLICT-017 is closed only at manifest-consistency level; it is not a global or governance acceptance.

A Phase 3.12.2 是对 Storage v3.3.2 的委派 A 角色精确复审，不是独立人类 A Owner 签名。它直接核验 Option A 措辞及无依据 A-01–A-05 引用已修正，并接受 v3.3.2 作为带列明阻塞项的一致候选 Manifest。Storage v3.3.2 本身也是委派 Storage 角色协调工件，不是独立人类 Storage Owner 签名。因此 B-CONFLICT-017 仅在 Manifest 一致性层面关闭，不构成全局或治理验收。

The v3.3.2 / A 3.12.2 exact-version pair binds H 1.2.14 and C 1.0.1. H 1.2.15 and I's 1.2.15 structural review are later candidate artifacts, not part of that accepted pair. A successor Storage manifest must bind exact H/C/I successor artifacts and receive fresh A review. All authority decisions remain local; no cross-owner global PASS is inferred.

v3.3.2 / A 3.12.2 精确版本配对绑定 H 1.2.14 和 C 1.0.1。H 1.2.15 与 I 对 1.2.15 的结构复审属于较新的候选工件，不属于该已接受配对。Storage 后继 Manifest 必须绑定精确 H/C/I 后继工件并取得 A 新复审。所有权威决定仍局限于各 Owner；不得推断跨 Owner 全局 PASS。

### 7.2 Gate / 门禁

B3 remains **NOT PASSED**. B-CONFLICT-017 is closed at manifest-consistency level only. Authenticated ingress, H 1.2.15 successor binding, I trust/profile/key registration, durable replay, G Applied freeze, D Forget completion and Storage L4 implementation remain open. No independent QA result, production authentication or physical purge is claimed.

B3 仍为 **NOT PASSED**。B-CONFLICT-017 仅在 Manifest 一致性层面关闭。Authenticated Ingress、H 1.2.15 后继绑定、I Trust/Profile/Key 注册、Durable Replay、G Applied 冻结、D Forget 完成和 Storage L4 实现仍开放。不宣称独立 QA 结果、生产认证或物理清除。


## 8. Current B2/B3 owner-source reconciliation — 2026-11-18 / 当前 B2/B3 Owner 来源协调 — 2026-11-18

### 8.1 Fact / Claim and Claim identity / Fact、Claim 与 Claim 身份

| Item / 项目 | Current authoritative evidence / 当前权威证据 | Disposition / 处置 |
|---|---|---|
| Fact vs Claim / Fact 与 Claim | B Owner summary ADR Blob `a1024938ff5baba069cf128c69496a44e143330c`; detailed ADR Blob `df77e4a93cb8fef689ae7c828888d960cbf381d6`; consumer map Blob `dd45a37199c9b69ab6b68f65e051a484a04691d4`; B branch `session-b-domain-model-phase3` @ `2faf8ec38f14dba49e7263d7a60804dae1a74ee2` | B's current preferred candidate is **Option A: separate Claim proposition thread and independently addressable Fact attestation object**. This supersedes the earlier C2/Option B preference in the B research ADR. It remains CANDIDATE / ADR-BLOCKED; Architecture Governance authority and approval are not recorded. |
| Claim identity / Claim 身份 | Detailed B ADR above; consumer map above | Stable ClaimRef + immutable ClaimRevisionRef is candidate only. D owns canonical ID allocation, persistence, revision commit and ConflictSet lifecycle/commit shape after ADR approval. No Claim identity/schema freeze. |
| Evidence / Provenance / ConflictSet | Detailed B ADR §6; consumer map §4 | Evidence is exact-revision-targeted; Provenance describes derivation, not truth; ConflictSet groups incompatible exact ClaimRevisionRefs and remains candidate pending D canonical commit approval. |
| E / F / G consumers | Consumer map Blob `dd45a37199c9b69ab6b68f65e051a484a04691d4` | E retains neutral CandidateProposition/ExtractionIR and may not mint canonical IDs; F preserves exact revision/currentness and cannot adjudicate truth; G pins MemoryVersionRef and only exposes exact ClaimRevisionRef when directly represented. These are candidate mappings, not consumer approvals. |
| Governance baseline / 治理基线 | Main I-04 Blob `33b037318e459ebb73bea33b3186f31a41d5dcfe`; P-04 Blob `192e6ba6e9287792a02b679dda0d391844270228`; Domain Overview Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`; EN/ZH guides Blobs `8a19cebacf5aefb0aded5fdbfeaff406291a5cf1` / `a9f53a453aec25c47c58c4aea75adc43c83028d3` | I-04/P-04 distinguish Fact and Claim; overview still describes Fact as qualified Claim; both guides retain ADR-BLOCKED. The normative baseline remains internally inconsistent. Option B would require explicit governance amendment; no option is approved. |

### 8.2 H 1.2.15 ingress correction / H 1.2.15 入口状态纠偏

A Phase 8 B-02 integration reconciliation Blob `8a0a428ebf9cd8c8fe00562d2267ff490d5c3205` corrects two overbroad statements in the preceding A report:
- I has reviewed the H 1.2.15 schema, P0 encoding and corrected replay/acceptance order as a trust-carrier/reference contract **ACCEPT WITH CONDITIONS**; I has **not** registered a production profile, issuer, trust root, keys, revocation, anti-rollback or production transport identity.
- C has reviewed the corrected issuance/receiver/replay order as a reference contract **ACCEPT WITH CONDITIONS**; that is not an exact review of the current H receiver validator/CI or an executable H issuer.
- D's prior review is limited to the 1.2.14 outer-auth boundary; exact H 1.2.15 currentness/Forget/lineage review remains OPEN.
- H receiver validator and tests exist, but A found no distinct issuer/signing-pipeline implementation entrypoint. H issuer pre-sign execution chain and integrated authority-join successor remain OPEN / NOT FOUND.
- Storage v3.3.2 remains a historical bundle pinned to H 1.2.14 / C 1.0.1. A new Storage successor must bind exact H/C/I/D artifacts and receive fresh A review.

A Phase 8 B-02 集成协调 Blob `8a0a428ebf9cd8c8fe00562d2267ff490d5c3205` 修正了前一份 A 报告中两项过度概括：
- I 已对 H 1.2.15 Schema、P0 编码和修正后的 Replay/Acceptance 顺序作了 Trust-Carrier/Reference 契约级 **ACCEPT WITH CONDITIONS** 审查；但 I **尚未**注册生产 Profile、Issuer、Trust Root、Keys、Revocation、Anti-Rollback 或生产 Transport Identity。
- C 已对修正后的 Issuance/Receiver/Replay 顺序作了 Reference 契约级 **ACCEPT WITH CONDITIONS** 审查；这不等于对当前 H Receiver Validator/CI 或可执行 H Issuer 的精确复审。
- D 先前的复审仅限 1.2.14 Outer-Auth 边界；H 1.2.15 的 Currentness/Forget/Lineage 精确复审仍 OPEN。
- H Receiver Validator 和测试已经存在，但 A 未发现独立 Issuer/Signing-Pipeline 实现入口。H Issuer Pre-sign 执行链和 Integrated Authority-Join 后继版本仍 OPEN / NOT FOUND。
- Storage v3.3.2 仍是绑定 H 1.2.14 / C 1.0.1 的历史 Bundle。新的 Storage 后继版本必须绑定精确 H/C/I/D 工件并取得 A 新复审。

The separate A exact review Blob `582ed576f73d9096dcc77b3a559df8c3b997b895` reports local H 1.2.15 validator/CI evidence (Provider Outcome workflow 91 tests, 0 failures; Recovery Cutoff workflow 288 tests, 22 skipped, 0 failures) on H commit `0d36324457e39bd50ad56ae902d477c4ea765b61`. Its evidence ceiling is deterministic callback orchestration and local reference conformance; it does not prove production cryptographic trust, issuer signing order, I registration, durable replay, or end-to-end deployment. A's overall disposition remains DEFERRED.

独立 A 精确复审 Blob `582ed576f73d9096dcc77b3a559df8c3b997b895` 报告了 H 1.2.15 本地 Validator/CI 证据（Provider Outcome Workflow 91 项测试、0 失败；Recovery Cutoff Workflow 288 项测试、22 项跳过、0 失败），测试 Commit 为 H Commit `0d36324457e39bd50ad56ae902d477c4ea765b61`。其证据上限是确定性 Callback 编排和本地 Reference Conformance；不能证明生产密码学信任、Issuer 签名顺序、I 注册、Durable Replay 或端到端部署。A 的总体处置仍为 DEFERRED。

### 8.3 Research maturity and non-promotion / 研究成熟度与禁止提升为规范

PRODUCT-FIRST-001 integration review Blob `3e7f0fc604761533ddd521924ff69d2039a63282` is explicitly NON-NORMATIVE / DRAFT and confirms the Fact/Claim ADR remains blocked; it authorizes no ADR, technology freeze or implementation. Memory Operating System research Blob `00e09d91ad3e7f08a9b7f7a26e30ebc98160d9c5` and Memory IR research Blob `084fc03bc5f09393bdd1ea6e8af3d8a6b703d3fc` state that their baselines are pinned but design/prototype work is not yet complete. They are research inputs only and cannot change B canonical identity, Scope, Evidence or lifecycle semantics.

PRODUCT-FIRST-001 集成审查 Blob `3e7f0fc604761533ddd521924ff69d2039a63282` 明确为 NON-NORMATIVE / DRAFT，并确认 Fact/Claim ADR 仍阻塞；它不批准 ADR、技术冻结或实现。Memory Operating System 研究 Blob `00e09d91ad3e7f08a9b7f7a26e30ebc98160d9c5` 和 Memory IR 研究 Blob `084fc03bc5f09393bdd1ea6e8af3d8a6b703d3fc` 均声明基线已 Pin，但设计/原型工作尚未完成。它们仅是研究输入，不能改变 B 规范身份、Scope、Evidence 或生命周期语义。

### 8.4 B2/B3 disposition / B2/B3 结论

B2 remains **IN PROGRESS / NOT PASSED**. The current preferred Fact/Claim candidate is Option A, but formal Architecture Governance approval is missing; ClaimRef/ClaimRevisionRef, FactRevision and ConflictSet schemas remain unfrozen. B3 remains **NOT PASSED**: H issuer implementation, integrated H/C/I/D authority join, I production trust registration, D 1.2.15 review, Storage successor manifest, durable replay, Applied and Forget evidence remain open.

B2 仍为 **IN PROGRESS / NOT PASSED**。当前优先 Fact/Claim 候选是 Option A，但缺少正式 Architecture Governance 批准；ClaimRef/ClaimRevisionRef、FactRevision 和 ConflictSet Schema 均未冻结。B3 仍 **NOT PASSED**：H Issuer 实现、H/C/I/D 集成权威联结、I 生产信任注册、D 1.2.15 复审、Storage 后继 Manifest、Durable Replay、Applied 和 Forget 证据仍开放。
