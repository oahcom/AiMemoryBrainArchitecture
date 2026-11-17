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
| B | 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/fact-claim-identity-adr.md | research/domain-reality-001-b | 96a2ee7d595fcd4a214201a7c7b6b2a9c3deb961 | C2 + I1 recommended candidate; NOT DECIDED / NOT ACCEPTED / NOT SCHEMA-FROZEN |
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

## 2. Semantic matrix / 语义矩阵

| Concept | B canonical position | Owner-local position | Status / conflict |
|---|---|---|---|
| Memory identity/version | Stable Memory identity; immutable MemoryVersion identity; content change does not change Memory ID | D owns canonical Memory/revision/cursor and lifecycle; Storage persists | Compatible in principle; exact aggregate/transaction contract D/Storage-owned |
| Claim / Fact | Claim is proposition; epistemic status separate; Fact/Claim ADR remains blocked | E extracts/derives; D stores canonical Memory; F/G consume projections/context | **BLOCKING for schema freeze**: root overview's older DECIDED wording conflicts with I-04 conceptual distinction and bilingual guide ADR-BLOCKED. Provisional reconciliation: Fact remains a distinct concept; independent object identity/type vs qualified Claim representation is OPEN. A PR #53 closed unmerged with DEFERRED disposition. |
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
2. **XOWN-BLOCK-002 — Applied:** G owns Applied record, C actual submit proof, H wire, I authorization, D fence; issue #3 requests independent owner approvals. Gate B3.
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

## 6. B3 gate / B3 门禁

B3 is **NOT PASSED**. The matrix is based on exact fetched source Blobs and explicit issue acceptance requirements, but several owner acceptances are explicitly open, branch tip SHAs are not verified, and cross-owner contracts remain candidate/not frozen. B3 cannot be marked complete by this B session's role simulation or A's synthesis.

B3 **未通过**。矩阵基于精确读取的源 Blob 和 Issue 中明确的 Owner 验收要求，但多个 Owner 验收仍明确开放、分支 Tip SHA 未核验、跨 Owner 契约仍为候选/未冻结。本 B 会话角色扮演或 A 的综合意见不能代替 B3 完成。
