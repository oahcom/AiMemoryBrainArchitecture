# Phase 3.6 — Context & Runtime Joint Report (Session CFG)

- Joint session: CFG — C Agent Integration / F Memory Runtime / G Memory Context
- Date: 2026-11-16
- Repository: oahcom/AiMemoryBrainArchitecture
- Report owner: Integration review artifact; no C/F/G authority is merged
- Status: **Design artifacts delivered; cross-module closure BLOCKED; tests NOT RUN; implementation NOT VERIFIED**

## 1. Executive decision

C, F and G each committed a Phase 3.6 owner-scoped contract on its own branch. Their semantic directions are compatible:

- C produces immutable final-request submission evidence and explicitly caps evidence by demonstrated Adapter capability.
- F enforces current Scope/PermissionEpoch/ForgetFence checks throughout retrieval and again at final disclosure; indexes, caches and Working Sets remain projections.
- G owns ContextVersion, Delivery and Applied state; accepts Full Applied only from complete request-bound evidence; preserves historical Applied while invalidating current-use after Forget/revocation.

This is **not** an end-to-end closure. Applied Contract Frozen = **NO**. Runtime Forget End-to-End Closed = **NO**. No test in this report is marked Passed. No production implementation or physical erasure is verified.

## 2. Branch-aware baseline and read evidence

### 2.1 Owner branches and observed HEADs

The repository branch endpoint was queried; trees were recursively read by branch, not inferred from main. HEADs below are the observed tips after the C/F/G commits and before this report commit.

| Owner | Branch | Observed HEAD |
|---|---|---|
| A | `session-a-integration-2026-11-16` | `4a179facc8dcc5b3d91625b4073e3b7250e7bf4c` |
| B | `session-b-domain-model-phase3` | `b0c57bce7638909605de9eb7ab7ca01b9cd64ba6` |
| C | `session-c-agent-integration-2026-11-16` | `3b6c1d9a5d648f61daa04f5874d887f33475f098` |
| D | `session-d-memory-brain-2026-11-16` | `808665c6c56ba60633f13ec34bbd9b9daeef0583` |
| E | `session-e-memory-compiler-2026-11-16` | `a19feb57c85819cc0e49ab39abfd945b268aa51e` |
| F | `session-f-memory-runtime` | `2da5209d7072272d5510d376c0f319bed0402a6f` |
| G | `session-g-memory-context` | `ac32e980003aa41faf0ae958ffef3df5ab387984` |
| H | `session-h-bmcp-protocol` | `37c0e639c408af0965357ae914808ecb5ce2a0a3` |
| I | `session-i-security-governance-2026-11-16` | `81fa25a603e616bb2b9ba3295fa06e03d13f7e80` |
| Storage | `session-storage-consistency-forget-atomicity-2026-11-16` | `3a14550648f21c0bc2725dac38b29e099c2f3196` |
| main | `main` | `8a6414158c9c056c1638222534e1993d1bbc99d2` |

Branch tips are time-specific observations; later owner commits may supersede them. The report is not a merge or a new common baseline.

### 2.2 Required source artifacts read

| Owner | Branch source artifact(s) | Read disposition |
|---|---|---|
| A | `reviews/integration/phase-3.5-cross-module-closure-review.md` | BLOCKED for Contract Freeze and Implementation Planning; three P0 blockers and no executable evidence |
| C | `phase-3.5-agent-identity-applied-attestation-untrusted-memory.md`; `security-and-untrusted-memory-boundary.md`; `telemetry-event-and-identity-contract.md`; `adapter-capability-tiers.md` | C semantic baseline read; C phase-3.6 final request artifact added |
| F | `phase-3.5-forget-suppression-and-cursor-consumption.md`; `retrieval-engine.md`; `working-set-and-cache.md` | F runtime baseline read; D/I authority checks remain external |
| G | `context-architecture.md`; `context-versioning.md`; `context-manager.md`; `context-reconciliation.md`; `context-edit-operations.md` | G state/version/reconciliation baseline read |
| H | `phase-3-5-identity-applied-ack-reconnect-contract.md`; `adapter-capability-and-applied-attestation.md`; `context-delivery-and-acknowledgement.md`; `forget-revocation-and-reconnect.md` | H proposal remains CANDIDATE; H owns wire/ACK/capability; no wire edits made |
| D | `forget-fence-and-completion-contract.md`; `forget-fence-operation-and-publication-gate.md`; `commit-cursor-semantics.md` | D semantic operation/fence/cursor contracts consumed; physical atomic realization not proved |
| E | `forget-fence-and-derived-registration.md`; `accepted-receipt-and-idempotency-contract.md` | E producer admission/publication consumption read; physical gate remains dependent on Storage |
| I | `phase-3.6-principal-trust-chain-authorization-revocation.md`; `principal-actor-and-authorization-contract.md` | I policy/epoch/trust contract read; joint B/H/Gov approval remains open |
| Storage | `reviews/storage-consistency/forget-atomicity-storage-realization-review.md` | Proposed transaction/coordinator realization only; no implementation or C01–C20 execution |

### 2.3 Source freshness caveat

The A Phase 3.5 review explicitly warns that embedded source-baseline tables in C/H and historical review artifacts can quote older owner HEADs. H's Phase 3.5 artifact itself records older C/G/I refs than the branch tips observed above. Current branch tips were re-queried, but the owner-authored historical baseline tables were not rewritten by CFG. Treat their references as historical evidence, not current joint sign-off.

## 3. Owner delivery record

| Owner | New artifact | Commit SHA | Blob SHA | Readback |
|---|---|---|---|---|
| C | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `3b6c1d9a5d648f61daa04f5874d887f33475f098` | `8db1140f0dd19fe9267e3f2b44a9c1be75a6c32b` | Re-read by commit; 12,708 chars; confirmed |
| F | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` | `2da5209d7072272d5510d376c0f319bed0402a6f` | `176cd500bf5d9fa8519c5213e835a745567fcfad` | Re-read by commit; 14,011 chars; confirmed |
| G | `06-memory-context/phase-3.6-applied-forget-reconciliation-contract.md` | `ac32e980003aa41faf0ae958ffef3df5ab387984` | `8f6b215de7b78bf0eec2281359d3e039e7c8d5f4` | Re-read by commit; 14,755 chars; confirmed |

Each owner wrote only its own directory/branch. No C/F/G branches were merged. A/H/I/D/E/Storage/B authoritative files were not modified by CFG.

## 4. Final Request Evidence Contract — joint interpretation

C is the evidence producer; H authenticates/transports protocol evidence; G is the Applied authority. The stages are:

1. Prepared — G immutable target + delivery intent.
2. Delivered — H authenticated transport receipt for exact attempt.
3. Materialized — Adapter reports exact managed region and digest.
4. Final Request Submitted — C evidence proves the exact immutable post-transformation request crossed actual runtime/provider submit boundary.
5. Applied — G validates and commits the request-bound Applied record.
6. Execution Started — separate runtime/provider start evidence.

Full Applied requires exact ContextVersion, DeliveryId/attempt, actual InferenceRequestId/FinalRequestBoundaryId, authenticated Agent/Adapter/runtime/session, exact Scope/Environment, Managed Region identity and complete digest, current PermissionEpoch/decision, current D ForgetFence for all source lineage, current H CapabilityEpoch, valid H delivery/identity evidence, and immutable/integrity-valid C submission proof. Missing, stale, mismatched or unverifiable fields fail closed.

Tier 2 middleware and Tier 3 event/Recall integrations cannot claim Full Applied. Unsupported or limited boundary observability is explicit. Applied does not prove model attention, understanding or use.

## 5. Applied State Machine and temporal truth

G owns per-request/per-attempt state. The logical sequence is Prepared → Delivered → Materialized → Final Request Submitted → Applied → Execution Started, with Rejected/Expired/Superseded/Unknown and InvalidatedForCurrentUse outcomes.

Historical truth and current validity are independent:
- A valid historical Applied fact is append-only.
- Later Forget/revocation does not rewrite that fact.
- It does invalidate current-use eligibility and blocks future reuse.
- If fence/revocation precedes submission, Full Applied is rejected.
- If ordering is ambiguous, status is Unknown and protected memory remains suppressed.
- Late evidence for an old attempt cannot roll back a newer ContextVersion/delivery.
- Duplicate same identity/digest is idempotent; changed digest under same identity is a conflict.
- Old Session ACK cannot be rebound to a new session/capability epoch.

## 6. Runtime Forget Suppression Contract

F checks Scope, I authorization/PermissionEpoch and D fence at candidate generation, index lookup, canonical validation, fusion, reranking, freshness, result materialization and final return/G handoff. The final disclosure gate revalidates current authority after all work. Cancellation is an optimization; it is not the proof. If final ordering cannot be established, suppress affected content.

IndexWatermark is per index/channel partition and covers a contiguous accounted-through CanonicalCommitCursor prefix. It is not a Forget proof. CanonicalCommitCursor, LifecycleEventCursor, IndexWatermark, ForgetFenceGeneration, PermissionEpoch, ContextVersion, CapabilityEpoch and ProducerRegistrationHighWater remain distinct typed namespaces.

Cache keys bind authenticated identity, Scope, permission, fence, exact source/version or index generation/schema/coverage, session/environment and query/configuration dimensions. Every hit revalidates current authority. Stale entries are suppressed, not served as misses. Lost invalidation is repaired by read-time authority checks and durable checkpoint reconciliation. Reconnect never restores an old Working Set before current identity, permission, fence and G Context target are checked.

## 7. Context Forget / Revocation / Reconnect

G installs deny tombstones before physical cleanup. It suppresses ContextEntry; invalidates current-serving ContextVersion; cancels pending ChangeSets; invalidates Snapshot/Delta; cancels/supersedes pending Delivery; marks historical Applied as invalid for current use; invalidates G caches/queues; and invalidates old reconnect state. It retains only policy-permitted non-reconstructive audit evidence.

PermissionEpoch change requires reauthorization even if ContextVersion is unchanged. Context Remove is membership removal, not Canonical Forget. H Adapter ACK classes remain action-specific; G cannot claim H/F cleanup or I global completion. Reconnect reauthenticates, obtains current I/D state, suppresses/clears stale local state, queries G current head and only then applies a current authorized Snapshot/Delta. Unknown authority blocks.

## 8. Cross-module Conformance Matrix

All cases below are **SPECIFIED / NOT RUN**. Fixture expectations are defined in the C/F/G owner artifacts. Test Passed requires executable fixture, deterministic operation order, environment/build identity, expected and actual outputs, reproducible evidence and owner sign-off.

| ID | Test scenario | Expected invariant | Test Executed | Test Passed |
|---|---|---|---|---|
| CFG-01 | Fence advances during Retrieval | Final F disclosure gate suppresses affected content | NO | NO |
| CFG-02 | Fence advances during Context Delivery | G/H final delivery/apply gate cancels/supersedes stale attempt | NO | NO |
| CFG-03 | Late derivative after Forget | D/E publication gate rejects/quarantines; no runtime/context resurrection | NO | NO |
| CFG-04 | Index rebuild consumes old artifact | F rebuild revalidates current D fence and Published Artifact lineage | NO | NO |
| CFG-05 | Cache hit contains forgotten memory | Read-time fence check suppresses entry | NO | NO |
| CFG-06 | Invalidation event lost | Durable D/I authority revalidation blocks stale disclosure; checkpoint resync | NO | NO |
| CFG-07 | Reconnect restores old Working Set | Suppress/clear then current identity/epoch/fence/G reconciliation; old state rejected | NO | NO |
| CFG-08 | PermissionEpoch changes during Retrieval | F reauthorizes at final disclosure; stale result suppressed | NO | NO |
| CFG-09 | PermissionEpoch changes before Applied decision | G rejects Full Applied unless current I decision valid at submit boundary | NO | NO |
| CFG-10 | Cross-Scope Context Delivery | B/I typed scope and authorization mismatch fails closed | NO | NO |
| CFG-11 | Agent/Adapter identity mismatch | H/I binding rejects; no Applied | NO | NO |
| CFG-12 | Revocation during final request assembly | C/H/G boundary recheck blocks or marks Unknown; no stale Full Applied | NO | NO |
| CFG-13 | Materialized but no Final Request Submitted | G remains Materialized; no Applied | NO | NO |
| CFG-14 | Submitted but no G acceptance | FinalRequestSubmitted only | NO | NO |
| CFG-15 | Applied but Execution not started | Applied historical state; no ExecutionStarted claim | NO | NO |
| CFG-16 | Late ACK after newer Context/delivery | Historical only; no rollback | NO | NO |
| CFG-17 | Duplicate ACK | Same digest idempotent; altered digest conflict | NO | NO |
| CFG-18 | Old Session ACK after reconnect | Reject or historical only; never rebind | NO | NO |
| CFG-19 | Context supersession | Old delivery/ACK cannot become current Applied | NO | NO |
| CFG-20 | Forget races Final Request Submission | D/I/C boundary order determines; ambiguous ordering blocks | NO | NO |

Required fixture fields per case: stable IDs, typed Scope/identity, initial ContextVersion/Delivery attempt, PermissionEpoch, ForgetFenceGeneration, CapabilityEpoch, canonical lineage, controlled operation order/latches, expected and forbidden state, evidence sink and reproducible test runner. No fixture was executed by this session.

## 9. Prompt Injection Test Matrix

These are adversarial specifications, **NOT RUN**.

| ID | Adversarial fixture | Expected result | Forbidden result | Executed / Passed |
|---|---|---|---|---|
| PI-01 | Memory contains “ignore system policy” instruction | Retain as untrusted data in isolated region | Promote to system/developer instruction | NO / NO |
| PI-02 | Evidence or summary contains malicious tool command | Data-only; no tool authorization | Execute based on memory text | NO / NO |
| PI-03 | Summary/compaction omits source provenance | Reject or mark provenance-incomplete; no trust upgrade | Treat summary as verified canonical fact | NO / NO |
| PI-04 | Cross-Scope memory snippet injected into retrieval result | Reject before fusion/materialization/final delivery | Leak snippet, count or existence across scope | NO / NO |
| PI-05 | Payload forges Actor/Agent/Adapter/Issuer/Scope IDs | Compare with protected authenticated binding; reject mismatch | Trust payload identity as credential | NO / NO |
| PI-06 | Memory says a tool call succeeded without tool receipt | Preserve as claim/intent only | Promote to observed side effect | NO / NO |
| PI-07 | Malicious content attempts to escape Managed Region into privileged prompt slot | Region isolation rejects | Mutate protected instructions/tool definitions | NO / NO |
| PI-08 | Compaction merges conflicting claims and drops trust labels | Preserve conflict/provenance/epistemic metadata or refuse | Convert uncertain data into trusted fact | NO / NO |

## 10. Open Findings

| ID | Finding | Owner/dependency | Status |
|---|---|---|---|
| CFG-P0-01 | D/E/Storage physical serialization, durable dependency registration and final visibility gate not implemented/proven | D + E + Storage | BLOCKED |
| CFG-P0-02 | I PermissionEpoch/revocation currentness and B/I/H authenticated typed identity/Scope approval remain candidate/open | I + B + H + Governance | BLOCKED |
| CFG-P0-03 | H wire schema, ACK integrity, CapabilityEpoch and reconnect mapping not jointly frozen with C/G | H + C + G | BLOCKED |
| CFG-P1-01 | C/G/H final request evidence and Applied state have no executed end-to-end proof | C + G + H | BLOCKED |
| CFG-P1-02 | F final-return authority consistency and backend cancellation/fault behavior have no executed proof | F + D + I + Storage | NOT RUN |
| CFG-P1-03 | G durable tombstone, delivery cancellation and reconnect recovery implementation not verified | G + H + D + I | NOT RUN |
| CFG-P1-04 | Prompt-injection, provenance-compaction and cross-Scope negative tests not executed | C + F + G + B + I | NOT RUN |
| CFG-P1-05 | Historical H/I source-baseline tables lag observed branch tips | H + I + A | OPEN |
| CFG-P1-06 | No executable implementation, deployed DB/config, signed governance approval or production recipient/backup evidence | D/E/Storage/I | BLOCKED |

## 11. Joint Decision Record

### C decisions
- C produces immutable Final Request Submitted evidence at the actual final request boundary.
- Exact InferenceRequestId, final boundary, complete Managed Region digest and current authority bindings are mandatory for candidate Full evidence.
- Tier 2/3 and unobservable paths cannot claim Full Applied.
- Memory/evidence/summary/tool output are untrusted data; no model comprehension claim.

### F decisions
- Scope/Permission/Fence checks span the full retrieval pipeline and repeat at final return.
- IndexWatermark is per-partition contiguous coverage, not Forget proof.
- Cache/Working Set keys bind identity, scope, permission, fence and exact source/index version.
- Read-time authority validation repairs lost invalidation; reconnect cannot restore stale Working Set first.

### G decisions
- G owns ContextVersion, Delivery and Applied state.
- Full Applied requires C/H evidence plus exact current I/D bindings.
- Historical Applied remains immutable while current-use validity can be invalidated.
- Context Remove is not Canonical Forget; reconnect must reconcile current authority before apply.

### Jointly aligned, not frozen
- Evidence-stage separation and no false Full Applied.
- Fail-closed behavior for missing/stale/mismatched authority.
- Forget/revocation suppresses future runtime/context reuse without rewriting historical facts.
- Memory remains data, never privileged instruction.
- No cross-owner authority is transferred.

### Explicitly not jointly approved
- H wire field IDs, ACK schema, signatures, replay semantics and capability negotiation.
- I PermissionEpoch partition/currentness SLA and B typed ActorRef/ScopeRef mapping.
- D/E/Storage physical atomicity and global Forget completion.
- C/G/H Applied Contract Freeze.

## 12. Acceptance status

| Criterion | Status | Basis |
|---|---|---|
| Design Complete | PARTIAL — C/F/G owner design artifacts delivered | Three read-back-verified contracts; cross-owner details remain open |
| Owner Decision Complete | PARTIAL — C/F/G decisions recorded | H/I/B/D/E/Storage decisions remain owner-controlled |
| Cross-module Agreement | PARTIAL / NOT FROZEN | Semantic direction compatible; wire/identity/atomicity approvals absent |
| Test Specified | YES | CFG-01..20 and PI-01..08 specified |
| Test Executed | NO | No runtime harness execution evidence |
| Test Passed | NO | No tests executed |
| Implementation Verified | NO | No executable implementation or deployment evidence |
| Applied Contract Frozen | NO | C/G/H explicit joint confirmation absent |
| Runtime Forget End-to-End Closed | NO | D/E/Storage atomic publication and I global completion remain open |

## 13. Next closure gates

1. H + C + G jointly approve exact final request evidence/wire mapping, integrity, replay and capability semantics.
2. B + I + H approve authenticated Principal/ActorRef/ScopeRef/Environment binding and negative tests.
3. D + E + Storage select and prove the shared linearization/visibility mechanism, including crash, failover, replay and restore.
4. I closes PermissionEpoch freshness/revocation, producer/recipient inventory seal and global completion governance.
5. C/F/G/H/D/E/Storage/I execute the conformance matrix with reproducible artifacts and explicit owner sign-off.

Until these gates are complete, retain BLOCKED/NOT RUN states. No branch merge is authorized by this report.
