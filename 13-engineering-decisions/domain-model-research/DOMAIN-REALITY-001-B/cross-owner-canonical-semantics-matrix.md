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

## 2. Semantic matrix / 语义矩阵

| Concept | B canonical position | Owner-local position | Status / conflict |
|---|---|---|---|
| Memory identity/version | Stable Memory identity; immutable MemoryVersion identity; content change does not change Memory ID | D owns canonical Memory/revision/cursor and lifecycle; Storage persists | Compatible in principle; exact aggregate/transaction contract D/Storage-owned |
| Claim / Fact | Claim is proposition; epistemic status separate; Fact/Claim ADR remains blocked | E extracts/derives; D stores canonical Memory; F/G consume projections/context | **BLOCKING**: root overview's older DECIDED wording conflicts with bilingual guide ADR-BLOCKED and A #53 blocker |
| Entity / Relation | Entity has stable identity; Relation is typed, directed/symmetric, scoped, temporal, evidenced | E derives candidates; F graph/index projections; G consumes selected refs | No direct contradiction found; typed Relation must not collapse into co-occurrence |
| Source / Evidence / Provenance | Source origin, Evidence material, Provenance derivation trace | E emits source/derivation lineage; D tracks canonical dependencies; I controls access/retention | Compatible core; graph-cycle/retention/identity granularity OPEN |
| Principal / ActorRef / Domain Entity | Distinct typed identity; Ref is not authentication or permission | I resolves Principal/trust/delegation; H authenticates transport; B owns typed refs; C/D/E/G bind operation context | Strong joint technical baseline; C/F/G explicit consumer acceptance OPEN (#6); governance approvals blocked |
| Scope / Tenant / Workspace / Environment | ScopeRef is typed namespace/ownership/applicability boundary; Scope not Permission; EnvironmentRef distinct | I owns Scope isolation/policy; G binds context scope; C/H transport typed refs; B owns reference semantics | **HIGH**: exact Tenant/Workspace/Project/Environment taxonomy and registry authority incomplete |
| Session / Conversation / RuntimeSessionRef | RuntimeSessionRef is authenticated bounded runtime session, not necessarily Conversation or Session Scope | C/G/H define runtime/session/conversation use; H owns session binding | **HIGH**: terms must not alias; full canonical session/conversation relation unresolved |
| Context / ContextVersion / ChangeSet | Context is G-owned task-scoped desired view; ContextVersion separate from MemoryVersion; ChangeSet G-owned | G owns Context and Applied records; F Working Set; E compiler input bundle distinct | Compatible direction; G exact schema and state transitions require further pinning; no scalar version alias |
| Retrieval / Activation / Working Set | Runtime-derived view/process, not canonical Memory truth | F owns ranking, index/cache, Working Set and final gate; G selects membership | Compatible; must keep F Working Set distinct from G ContextVersion |
| Operation / Protocol Message / Receipt | Operation identity/state distinct from Request/Response/Command/ACK | H owns wire/ACK; C owns provider submit; D/I own fences/auth; Storage owns receipt | **HIGH**: operation identity and cross-authority participant references require exact contracts; ACK never upgrades to Applied |
| Applied | Historical per-request Context application fact committed only by G under full predicate; no attention/comprehension claim | C emits actual final-request evidence; H transports; I/D provide authorization/fence; G validates and commits | **BLOCKING**: C/G/H exact Applied contract not frozen; issue #3 explicitly shows Frozen NO, Tests NO, Implementation NO |
| Recorded / Committed / Visible / Published | Distinct typed outcome semantics; no universal total order | Owner records evidence; D canonical cursor; Storage authoritative pointer/receipt; E terminalizes after receipt | **BLOCKING** for JF-10 publication: I COMMIT_WON != Storage PUBLISHED; implementation/physical capability not verified |
| Forget / Forgotten / Deleted / Purged | Memory Forgotten is lifecycle state; ForgetOperation distinct; logical suppression not physical purge | D operation/fence/barrier; I global completion/retention; Storage/backup physical erasure; G/F/H local cleanup | **BLOCKING** for global completion/physical purge; no single owner can claim global success |
| Event Time / Observed At / Recorded At / Valid Time | Distinct temporal dimensions; valid-time and record-time history retained | C/E capture source times; D commit cursor; Storage transaction time | Compatible conceptually; exact Record vs Transaction Time field authority and fuzzy-time encoding OPEN |
| Provider Outcome / Final Request Submitted | Execution/provider boundary evidence is not a generic Event or protocol ACK | C alone emits actual provider submit outcome; H transports; G consumes | Compatible; provider outcome semantics and exact causal order remain C/I/D/Storage dependencies |
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
- Testing: executable invariant/conformance/fault-injection evidence; not found as an owner-authoritative acceptance for all above.

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

## 6. B3 gate / B3 门禁

B3 is **NOT PASSED**. The matrix is based on exact fetched source Blobs and explicit issue acceptance requirements, but several owner acceptances are explicitly open, branch tip SHAs are not verified, and cross-owner contracts remain candidate/not frozen. B3 cannot be marked complete by this B session's role simulation or A's synthesis.

B3 **未通过**。矩阵基于精确读取的源 Blob 和 Issue 中明确的 Owner 验收要求，但多个 Owner 验收仍明确开放、分支 Tip SHA 未核验、跨 Owner 契约仍为候选/未冻结。本 B 会话角色扮演或 A 的综合意见不能代替 B3 完成。
