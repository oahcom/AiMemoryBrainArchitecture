# Phase 3 — Cross-Module Remediation Task Pack

- Date: 2026-11-16
- Repository: `oahcom/AiMemoryBrainArchitecture`
- Parent review: `reviews/integration/phase-2-defg-cross-session-reconciliation.md`
- D correction: `reviews/03-memory-brain/review-scope-correction-and-design-reassessment.md`
- Status: **TASK PACKAGE — READY FOR PARALLEL DESIGN WORK; NOT AN APPROVAL TO FREEZE CONTRACTS OR START PRODUCTION IMPLEMENTATION**
- Objective: close the cross-module architecture decisions and P1 design gaps without restarting or wholesale merging A–G.

---

## 0. Mandatory execution rules

Every session must follow these rules:

1. Read the governance baseline, the A/B/C documents on `main`, the Phase 1 and Phase 2 integration reviews, and the relevant D/E/F/G source documents from their exact branch refs listed below.
2. Do not treat a main-only missing-file report as proof that a branch design is defective. Review the actual branch and commit.
3. Preserve ownership boundaries. Do not redesign another session's subsystem or silently decide another owner's ADR.
4. Do not edit another session's files. Create or update only files explicitly assigned to your session. For existing module documents, only the owning session may update its own files on its own branch.
5. Do not modify `00-governance/*` unless the governance owner explicitly assigns that change. A decision proposal is not an approved invariant.
6. Every proposal must be labeled `DECIDED`, `CANDIDATE`, `ADR-BLOCKED`, `OPEN`, or `TO_VALIDATE`. Never turn an unresolved dependency into a decision by wording.
7. Every contract must define owner, producer, consumer, identity/scope, version/cursor semantics, failure behavior, retry/idempotency, revocation/Forget behavior, observability and conformance tests.
8. Separate logical suppression, asynchronous cleanup, and physical erasure. Do not claim physical deletion from a tombstone or local cache clear.
9. Separate design review, branch delivery, main integration, implementation conformance and performance sign-off.
10. Do not merge branches. Do not freeze wire/schema contracts. Do not claim implementation, security or performance passed without evidence.
11. Each session must submit: (a) its owned design artifacts, (b) a decision/change log, (c) an interface impact table, (d) testable acceptance criteria, and (e) unresolved issues with owner/dependency.
12. Keep IDs from Phase 2. Do not rename or close them without evidence and explicit owner approval.

### Source baselines

| Session | Branch | Baseline commit |
|---|---|---|
| A/B/C | `main` | Read current `main` at task start; record exact SHA |
| D | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` |
| E | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` |
| F | `session-f-memory-runtime` | `dad5deb6bfaa2df9956930d0b1372df354112567` |
| G | `session-g-memory-context` | `3d2c065be863bc1d349faaeece6f6eaa0047abae` |
| H/I | Not yet present in repository | Create separate task branches from the agreed current baseline; do not invent or assume existing H/I artifacts |

---

## 1. Workstream map and dependency order

| Workstream | Owner | Priority | Depends on | Output |
|---|---|---:|---|---|
| WS-0 Review/decision registry | Architecture coordinator (A) | P0 | Phase 2 reconciliation | Shared decision register and integration matrix |
| WS-1 Fact/Claim ADR | B + Architecture Governance; D consults | P0 | Existing domain model | Approved or explicitly rejected ADR |
| WS-2 Principal / ActorRef / Scope / permission epoch | I + H + B; C/D/E/F/G consult | P0 | WS-1 terminology alignment where needed | Security identity and authorization contract |
| WS-3 Forget fence and anti-resurrection | D + I; E/F/G/H implement their boundary contracts | P0 | WS-2 identity and scope | End-to-end Forget protocol and race matrix |
| WS-4 Typed cursor / watermark contract | A + D + E + F + G | P1 | Canonical commit semantics | Typed cursor and causal ordering specification |
| WS-5 BMCP and Applied attestation | H + C + G | P1 | WS-2 and G Context model | Wire protocol, delivery and Applied proof |
| WS-6 Durable Accepted / idempotency | E + H + I; A/storage consult | P1 | WS-2 identity | Durable ingestion and receipt contract |
| WS-7 Conformance suite | A coordinates; all module owners contribute | P1 | WS-1 through WS-6 candidate contracts | Cross-module test plan and evidence |
| WS-8 Performance validation plan | A + E/F/G + Engineering | P2 | Stable candidate interfaces | Reproducible benchmark protocol, not invented SLOs |

Parallel work is allowed for WS-1, WS-2, WS-4 and H/I first drafts. WS-3 must consume WS-2's identity/scope decision. WS-5 must consume WS-2 and G's delivery semantics. No dependent contract may be marked frozen before its dependencies close.

---

## 2. Session A — Integration Architecture and Contract Registry

**Role:** Integration Architect / cross-module coordinator.

**Owns:** System-wide contract map, dependency graph, typed cursor namespace proposal coordination, decision registry, conformance orchestration. A does not own canonical Memory, Compiler, Runtime, Context, Agent Adapter or global security policy.

### Tasks

1. Read A/B/C baseline and all D/E/F/G branches at the exact refs above.
2. Maintain one registry for INT-P0-01..04, INT-P1-01..06, D-REV-P1-001..003 and INT-X-01..08.
3. Coordinate WS-4 with D/E/F/G and storage engineering:
   - source Event cursor;
   - canonical commit cursor;
   - per-aggregate revision;
   - lifecycle event cursor;
   - per-index/per-partition publication watermark;
   - Forget fence/epoch;
   - Context version;
   - Delivery identifier/sequence;
   - Adapter capability epoch and inference request identifier.
4. Ensure each cursor has a typed name, namespace, owner, partition/scope, monotonicity, gap semantics, replay/resume rule and causal relation. Do not use one untyped integer for unrelated generations.
5. Build a cross-module interface matrix: producer, consumer, authoritative owner, immutable identifier, version, consistency, failure and retry.
6. Coordinate conformance scenarios; do not mark tests passed until evidence is attached.

### Outputs

- `reviews/integration/contract-registry.md`
- `reviews/integration/typed-cursor-and-watermark-contract.md`
- `reviews/integration/cross-module-conformance-plan.md`

### Acceptance

- Every INT and D-REV item has one accountable owner and an explicit state.
- Cursor/watermark names are unambiguous and consistent across D/E/F/G.
- No module claims ownership of another module's authoritative version.
- All open dependencies are visible; no silent closure.

---

## 3. Session B — Fact / Claim ADR and Domain Semantics

**Role:** Domain Model Principal Architect.

**Owns:** Canonical domain identity and semantics for Fact/Claim, typed references and domain-level Scope semantics. B does not own D's persistence mechanics or I's authorization policy.

### Tasks

1. Resolve INT-P0-01 against the existing governance terminology and B domain model.
2. Explicitly compare:
   - Fact as a canonical object versus Fact as an assertion/qualification of a Claim;
   - Claim identity and immutable ClaimRevision;
   - evidence attachment and provenance;
   - confidence, epistemic status, validity interval and lifecycle as separate axes;
   - contradiction and ConflictSet membership;
   - retraction, supersession and correction.
3. Decide one normative model through an ADR. If no decision can be made, state the exact missing decision authority and keep the ADR-BLOCKED.
4. Define typed domain references: MemoryRef, MemoryVersionRef, ClaimRef, ClaimRevisionRef, EntityRef, EvidenceRef, ScopeRef, ActorRef, EventRef and TimeValue/TimeInterval. Define whether each is globally unique, tenant-scoped or scope-bound.
5. Define domain Scope algebra and inheritance/containment semantics without deciding authorization grants. Keep Scope distinct from Permission.
6. Provide E's neutral extraction proposal mapping to the approved canonical model; provide D/F/G consumption semantics.

### Outputs

- `02-domain-model/adr/ADR-001-fact-claim-canonical-model.md`
- `02-domain-model/typed-reference-and-scope-semantics.md`
- `02-domain-model/fact-claim-consumer-mapping.md`

### Acceptance

- ADR has status APPROVED or explicitly ADR-BLOCKED with decision owner and alternatives.
- D/E/F/G use the same Claim identity/revision and ConflictSet semantics.
- No untyped or ambiguous reference is used in normative contracts.
- Scope semantics do not silently encode permissions.

---

## 4. Session C — Agent Telemetry and Inference Boundary

**Role:** Agent Integration Principal Architect.

**Owns:** Agent-side telemetry contract, inference boundary and Adapter capability requirements. C does not own BMCP wire serialization (H) or Context authority (G).

### Tasks

1. Reconcile telemetry with D/E/F/G needs without requiring full hidden CoT.
2. Define authenticated producer binding separately from payload fields.
3. Define Observation, Outcome, Intent, PlanSummary, PendingAction, ToolCall, EnvironmentDelta and Uncertainty as distinct event semantics; planned actions must not be recorded as completed facts.
4. Define event IDs, source sequence, timestamps, environment identity and correction/retraction semantics.
5. Define the final inference-request boundary at which H can attest Applied.
6. Specify Tier 1/2/3 capabilities and exactly when Full Applied is not attestable.
7. Preserve protected System/Developer/User regions and Agent authorization. Memory remains untrusted data, never elevated instructions.

### Outputs

- `07-agent-integration/telemetry-event-and-identity-contract.md`
- `07-agent-integration/final-inference-boundary-attestation.md`
- `07-agent-integration/adapter-conformance-cases.md`

### Acceptance

- No full CoT is required.
- Plan/intent cannot be mistaken for observed outcome.
- Applied proof binds to exact request/session/context version and capability epoch.
- Adapter cannot overwrite protected instruction/input regions or bypass tool authorization.

---

## 5. Session D — Memory Brain Corrections and Canonical Authority

**Role:** Memory Brain Principal Architect.

**Owns:** Canonical Memory identity, immutable revisions, lifecycle authority, Entity/Relation canonical assets and canonical ForgetOperation/fence semantics. D does not own ContextVersion, wire protocol, global authorization policy or physical-erasure policy.

### Tasks

1. Fix `D-REV-P1-001`: resolve Forgetting vocabulary contradiction. Recommended separation: Memory lifecycle states remain durable semantic lifecycle states; in-progress Forget is represented by ForgetOperation/fence, not a competing Memory lifecycle state. If effective visibility is exposed, name it separately.
2. Fix `D-REV-P1-002`: choose global canonical commit sequence, per-aggregate sequence, or both with distinct typed fields. Define transaction visibility, gaps, replay cursor and relation to LifecycleEvent.
3. Co-own `D-REV-P1-003`: define durable ForgetOperation ID and fence/generation, dependency inventory, producer registration, barrier/watermark, late derivative suppression, target acknowledgement and completion proof. I owns global completion policy; E/F/G/H implement their boundaries.
4. Finalize canonical Claim/ClaimRevision/ConflictSet only after B's ADR. Do not pre-empt the ADR.
5. Define Entity Merge/Split and Relation migration semantics with stable historical references.
6. Ensure canonical revisions, evidence/provenance references and lifecycle events remain auditable and recoverable.

### Outputs (on D branch only)

- Update only D-owned files under `03-memory-brain/`.
- Add `03-memory-brain/forget-fence-and-completion-contract.md` if needed.
- Add `03-memory-brain/commit-cursor-semantics.md` if needed.
- Add a D decision/change log in `03-memory-brain/`.

### Acceptance

- D-REV-P1-001 and D-REV-P1-002 resolved consistently across all D documents.
- D-REV-P1-003 specifies the race barrier and cannot allow late derivative resurrection.
- No D document claims G's Context authority, H's Adapter/wire authority or I's global policy authority.
- Fact/Claim remains ADR-BLOCKED until B/Governance approval.

---

## 6. Session E — Memory Compiler Durable Ingress and Derivative Registration

**Role:** Memory Compiler Principal Architect.

**Owns:** Event ingress durability, extraction/normalization proposals, provenance, consolidation and derivative production. E does not own canonical commit, Runtime indexes or Context versions.

### Tasks

1. Define Accepted as a durable receipt, distinct from Processed, Compiled, CanonicalCommitted and Indexed.
2. Define idempotency key scope, payload hash, same-key/same-payload replay, same-key/different-payload conflict, receipt replay and retention horizon.
3. Specify atomic/recoverable persistence for Event + payload reference + idempotency receipt + compile intent (transaction or equivalent outbox/WAL).
4. Define source event ordering and cursor separately from canonical commit and index publication cursors.
5. Consume D's Forget fence: every compiler worker, lease, retry, DLQ, replay, recompile and derived-output publication must check the fence before commit/publication.
6. Register derived dependencies before they become visible. Define how in-flight work participates in D/I's completion barrier.
7. Define provenance source lineage and deletion/suppression propagation without erasing required non-reconstructive audit tombstones.
8. Map neutral CandidateProposition/ExtractionIR to B's approved canonical Fact/Claim model after ADR.

### Outputs (on E branch only)

- Update only E-owned files under `04-memory-compiler/`.
- Add `04-memory-compiler/accepted-receipt-and-idempotency-contract.md`.
- Add `04-memory-compiler/forget-fence-and-derived-registration.md`.
- Add E decision/change log.

### Acceptance

- Crash/retry cannot lose an Accepted event or duplicate canonical effects.
- Compiler replay cannot resurrect forgotten derivatives.
- Every derived object has source lineage and a registered dependency.
- Event cursor, canonical cursor and index watermark are distinct typed concepts.

---

## 7. Session F — Memory Runtime Scope, Watermark and Forget Enforcement

**Role:** Memory Runtime Principal Architect.

**Owns:** Retrieval, candidate generation, fusion, freshness validation, Working Set/cache and activation recommendation. F does not own Canonical Memory or ContextVersion.

### Tasks

1. Define Scope enforcement before candidate emission in every retrieval backend: lexical, ANN, structured, temporal, graph, evidence and provenance.
2. Define per-index/per-partition publication watermark and its relationship to D canonical commit cursor and E outbox/publication cursor.
3. Specify stale index behavior: canonical revalidation, incomplete-result marker, bounded wait, fallback or fail-closed behavior according to risk.
4. Consume D/I Forget fence at candidate generation, in-flight result finalization, cache read/write, Working Set materialization and index rebuild.
5. Define cache keys and invalidation epochs so scope, principal, permission epoch, environment, canonical cursor and Forget fence cannot be accidentally crossed.
6. Define response completeness and uncertainty when channels lag or are unavailable.
7. Keep RetrievalResult and ActivationRecommendation immutable and separate from G's ContextEntry/ContextVersion.

### Outputs (on F branch only)

- Update only F-owned files under `05-memory-runtime/`.
- Add `05-memory-runtime/cursor-freshness-and-forget-enforcement.md`.
- Add F decision/change log.

### Acceptance

- No retrieval channel can emit cross-scope candidates before authorization.
- Stale/lagging channels cannot override canonical Forget state.
- Watermark gaps and channel lag are explicit in result completeness.
- F never writes or versions G Context entries.

---

## 8. Session G — Context Reconciliation, Delivery and Applied Semantics

**Role:** Memory Context Manager Principal Architect.

**Owns:** Desired Context membership/order/budget, ContextVersion, ContextChangeSet, reconciliation and delivery intent. G does not own canonical Memory or Adapter wire execution.

### Tasks

1. Consume D's exact MemoryVersion references and invalidation/fence events; never rewrite canonical Memory.
2. Consume F RetrievalResult/ActivationRecommendation; F does not create ContextEntry or ContextVersion.
3. Define atomic ChangeSet CAS, base/target version, idempotency, duplicate/replay, partial failure and full snapshot fallback.
4. Define Forget reconciliation: tombstone/remove entries, invalidate snapshots/deltas, cancel Prepared/Delivered work where possible, and prevent stale delivery from being marked Applied.
5. Define offline Adapter state as Pending/Unknown until a valid reconnect/reconciliation attestation is received.
6. Co-design Applied semantics with C/H: Full Applied requires complete managed-region materialization in the exact final inference request. Partial, Bypassed, Unknown and model attention are separate states.
7. Define budget and sufficiency metadata without claiming the model actually used the memory.

### Outputs (on G branch only)

- Update only G-owned files under `06-memory-context/`.
- Add `06-memory-context/forget-reconciliation-and-offline-adapter.md`.
- Add `06-memory-context/applied-attestation-consumer-contract.md`.
- Add G decision/change log.

### Acceptance

- ContextVersion and Delivery states remain separate state machines.
- ChangeSet is atomic/idempotent and base-version safe.
- No stale/late delivery can re-activate a forgotten entry.
- Applied is bound to exact ContextVersion, Delivery, session, capability epoch and inference request.

---

## 9. Session H — BMCP Protocol and Agent Context Adapter

**Role:** Protocol and Adapter Principal Architect. H is a new workstream; no H package was present in the inspected main tree.

**Owns:** BMCP wire envelope, serialization/version negotiation, transport semantics, Adapter SDK, delivery/application acknowledgement and final-request attestation. H does not own Brain memory semantics, Context membership or global security policy.

### Tasks

1. Define BMCP message families: Telemetry, Event Ingress, Context Snapshot/Delta, Delivery, Acknowledgement, Capability Negotiation, Forget/Revocation notification and Administrative governance envelope.
2. Define protocol versioning, required/optional fields, unknown enum handling, canonical serialization, integrity metadata, correlation/causation IDs and error taxonomy.
3. Define authenticated transport principal binding and consume I's Principal/ActorRef/permission epoch; never trust actor identity asserted only inside payload.
4. Define Adapter capabilities and Tier 1/2/3 conformance.
5. Define delivery state transitions Prepared, Delivered, Applied, Rejected, Expired, Superseded and Unknown; specify retry and idempotency.
6. Define exact Full/Partial/Bypassed/Unknown application attestations. Full Applied must bind to the final request actually submitted to the inference runtime, not merely an internal Adapter buffer.
7. Define Forget/revocation notification, managed-region clearing, offline reconnect, stale snapshot rejection and acknowledgement. Do not claim control over provider-side retained prompts or hidden model state.
8. Ensure Memory payload is data, not instructions, and cannot alter protected instruction regions or Agent tool authorization.

### Outputs (new H branch only)

- `08-bmcp-protocol/protocol-overview.md`
- `08-bmcp-protocol/message-envelope-and-versioning.md`
- `08-bmcp-protocol/context-delivery-and-acknowledgement.md`
- `08-bmcp-protocol/adapter-capability-and-applied-attestation.md`
- `08-bmcp-protocol/forget-revocation-and-reconnect.md`
- `08-bmcp-protocol/protocol-conformance-matrix.md`

### Acceptance

- Wire semantics match C telemetry, D canonical refs, E receipt, F retrieval response and G Context delivery.
- Full Applied has a verifiable final-request boundary; unsupported adapters cannot claim Tier 1.
- Duplicate, stale, superseded, expired, offline and late acknowledgement behavior is deterministic.
- H does not decide I's authorization policy or G's Context authority.

---

## 10. Session I — Security, Identity and Governance

**Role:** Security/Governance Principal Architect. I is a new workstream; no I package was present in the inspected main tree.

**Owns:** Global authorization policy, principal identity/delegation, revocation, retention, audit governance, backup/external-copy policy, Forget completion policy and physical-erasure requirements. I does not own local D/E/F/G mechanics or H wire encoding.

### Tasks

1. Define Principal, ActorRef, ProducerIdentity, issuer, delegation, tenant/user/project/environment scope binding, permission epoch and revocation semantics.
2. Define policy decision contract and fail-closed behavior. Separate authentication, authorization, ownership Scope and applicability Scope.
3. Define grants, revocation propagation, cache/lease invalidation and reauthorization at ingress, compile, canonical commit, retrieval, evidence dereference, Context delivery and inference boundary.
4. Define Forget governance: immediate logical suppression, asynchronous derivative cleanup, external recipient handling, backup/restore behavior, retention/legal hold exceptions and physical erasure policy.
5. Define global Forget completion: required target inventory, target states Pending/Confirmed/Failed/Unknown/PolicyException, barrier/watermark proof, exception approval and audit evidence.
6. Define threat model for prompt injection through Memory/Evidence/Provenance/Entity labels/summaries/compaction and cross-scope poisoning. Do not claim LLMs can be made perfectly immune.
7. Define audit retention while avoiding reconstruction of forgotten content. Specify non-reconstructive tombstones and evidence minimization.
8. Define security conformance and adversarial test matrix with H/C/D/E/F/G.

### Outputs (new I branch only)

- `09-security-governance/security-and-identity-overview.md`
- `09-security-governance/principal-actor-and-authorization-contract.md`
- `09-security-governance/scope-and-revocation-policy.md`
- `09-security-governance/forget-retention-backup-and-erasure-policy.md`
- `09-security-governance/threat-model-and-adversarial-test-plan.md` (not restored on main; see AID-2026-107 §10)
- `09-security-governance/audit-and-exception-governance.md` (not restored on main; see AID-2026-107 §10)

### Acceptance

- Identity is cryptographically/authentically bound, not payload-self-asserted.
- All boundaries reauthorize with defined revocation epoch semantics.
- Forget completion never counts unknown/offline targets as confirmed without an explicit policy exception.
- Logical suppression, cleanup and physical erasure are separate states and claims.
- Security residual risks and risk acceptance authority are explicit.

---

## 11. Shared conformance and fault-injection acceptance matrix

All owners must contribute concrete cases. The integration coordinator consolidates the evidence.

| Test ID | Scenario | Expected invariant | Required owners |
|---|---|---|---|
| CT-001 | Same idempotency key, same payload | Original durable receipt returned; no duplicate effect | E/H |
| CT-002 | Same idempotency key, different payload | Deterministic conflict; no overwrite | E/H |
| CT-003 | Crash before/after Accepted response | Durable state and receipt recover consistently | E/A |
| CT-004 | Compiler retry/DLQ replay after Forget fence | No forgotten derivative becomes visible | D/E/I |
| CT-005 | ANN/lexical/graph/temporal cross-scope candidate | Candidate rejected before emission | B/F/I |
| CT-006 | Unauthorized Evidence/Provenance dereference | Independent authorization denies access | D/E/F/I |
| CT-007 | Index lag or missing publication watermark | Result marks incomplete or applies declared fail-closed policy | D/E/F |
| CT-008 | Canonical revision changes during retrieval | Stale candidate revalidated or rejected | D/F |
| CT-009 | Forget concurrent with canonical write | Fence/barrier prevents post-completion resurrection | D/E/I |
| CT-010 | Forget while retrieval/cache fill is in flight | Response/cache cannot expose forgotten memory after suppression | F/I |
| CT-011 | Forget while Context ChangeSet/Delivery is pending | Stale delivery cannot become valid Applied | G/H/I |
| CT-012 | Late Applied ACK after superseding Forget/version | Rejected or recorded as stale; never reactivates state | G/H |
| CT-013 | Offline Adapter reconnects with stale snapshot | Must reconcile and clear/suppress before Full Applied | G/H/I |
| CT-014 | Backup restore after Forget | Forgotten content remains suppressed; restore policy is enforced | I + storage |
| CT-015 | ChangeSet base-version mismatch | No partial application; snapshot/reconcile path is deterministic | G/H |
| CT-016 | Applied claim without final-request evidence | Cannot be classified Full Applied | C/G/H |
| CT-017 | Prompt injection via retrieved/compacted Memory | Data remains untrusted; protected instructions and tool auth unchanged | C/H/I |
| CT-018 | Unknown enum/schema version | Explicit compatibility or fail-closed behavior; no silent reinterpretation | A/B/H |
| CT-019 | Provenance cycle/fan-out/source unavailable | Bounded, observable traversal; no unbounded recursion | D/E/F |
| CT-020 | Forget with legal hold/retention exception | Access suppression and retained-minimum policy are explicit and audited | I |

No test is marked PASS without a reproducible test artifact, test version, environment, expected/actual result and owner sign-off.

---

## 12. Global exit criteria

### Architecture decision gate

- INT-P0-01 Fact/Claim ADR approved or explicitly remains ADR-BLOCKED with no schema freeze.
- INT-P0-02 Principal/ActorRef/Scope/permission epoch semantics jointly approved.
- INT-P0-03 Forget fence, producer barrier, late derivative handling and global completion policy approved.
- INT-P0-04 threat model and residual risk owner accepted.
- INT-P1-01 Context/Delivery/Applied authority boundaries approved.
- INT-P1-02 Claim revision/ConflictSet/Merge/Split semantics aligned after ADR.
- INT-P1-03 authenticated telemetry identity and environment semantics approved.
- INT-P1-04 Accepted/idempotency/replay semantics approved.
- INT-P1-05 final-request Applied proof contract approved.
- INT-P1-06 typed references, provenance, lifecycle and watermark semantics aligned.

### Implementation readiness gate

- All required conformance cases have test evidence.
- No unresolved P0 or owner-local P1 blocks the intended implementation scope.
- Fail-closed behavior and degraded-mode behavior are explicit.
- Recovery, replay, revocation and Forget race tests pass.
- No unsupported performance claim appears in acceptance documentation.

### Main integration gate

- Branches are reviewed against exact commit SHAs.
- A/B/C baseline changes are not overwritten.
- D/E/F/G/H/I artifacts are integrated through controlled PRs only after cross-module review.
- Integration review verifies one coherent contract set, not merely file presence.

---

## 13. Copy-ready session kickoff prompt

Use this common preamble for each assigned session, then append only that session's role/tasks/outputs above:

> You are the Principal Architect for your assigned subsystem in AiMemoryBrainArchitecture. Execute only your assigned workstream in `reviews/integration/phase-3-cross-module-remediation-task-pack.md`. First read the full task pack, Phase 2 reconciliation, governance baseline, and all explicitly referenced upstream/downstream contracts at their exact branch refs. Do not assume main contains other sessions' unmerged work. Preserve all ownership boundaries. Do not edit other sessions' files or governance files. Create/update only your assigned files on your assigned branch. Keep every decision labeled DECIDED/CANDIDATE/ADR-BLOCKED/OPEN/TO_VALIDATE. For each change provide evidence, rationale, dependencies, failure behavior and acceptance tests. Do not merge branches, freeze contracts whose dependencies are open, or claim implementation/security/performance validation without test evidence. At completion report exact branch, base SHA, commit SHA, changed paths, resolved IDs, unresolved IDs, interface impacts and test evidence.

---

## 14. Recommended execution sequence

1. **Start A, B, H and I in parallel.** A opens the decision registry; B owns Fact/Claim ADR; H and I create protocol and security/governance foundations. They must coordinate identity and Applied semantics rather than independently inventing them.
2. **Start D and E in parallel after reading the task pack.** D resolves lifecycle/commit cursor and drafts Forget fence; E defines durable Accepted and producer registration against the proposed fence.
3. **Start F and G once D/E publish candidate cursor/fence contracts.** They may draft in parallel but must consume the same typed cursor and Forget semantics.
4. **C works with H/G** on final inference boundary and Applied proof while preserving Agent authority.
5. **A runs cross-module reconciliation** and updates the decision registry; owners resolve conflicts in their own documents.
6. **Run conformance review** against the shared matrix. Only then prepare controlled integration PRs.

If a dependency is not ready, the downstream session may produce a clearly labeled candidate mapping, but must not freeze or implement an assumed contract.

---

## 15. Final instruction

The goal is not to make every report say PASS. The goal is to make every subsystem agree on the same authoritative identities, scopes, cursors, versions, Forget fences, delivery states and evidence semantics.

Preserve the sound architecture. Fix the specific defects. Close shared contracts once, at their authoritative owner. Test the boundaries before merging.


## Mandatory bilingual architecture deliverables / 强制中英双语架构交付

This task MUST comply with [GOV-DOC-001 — Bilingual Architecture Documentation Policy](../../00-governance/bilingual-documentation-policy.md). Every architecture proposal, Owner review, interface/schema/state-machine change, ADR, integration decision, and acceptance report produced by this task MUST have Chinese and English counterparts updated in the same change set. Both versions must preserve identical scope, authority, normative force, decision status, findings, severity, evidence, caveats, and open issues. Stable identifiers and machine-readable values must remain unchanged. Update the repository-wide docs/translation-status.md register. Missing or stale counterparts block documentation acceptance unless a documented, time-bounded exception is approved under GOV-DOC-001.

本任务必须遵循 [GOV-DOC-001《架构双语文档规范》](../../00-governance/bilingual-documentation-policy.md)。本任务产生的每项架构提案、Owner 审查、接口/Schema/状态机变更、ADR、集成决议和验收报告，都必须在同一变更集中提供或更新中英文版本。两种语言必须保持相同的范围、权威性、规范效力、决策状态、发现、严重级别、证据、限制和未决事项。稳定标识和机器可读值不得改变。必须更新全仓库 docs/translation-status.md 登记表。除非依据 GOV-DOC-001 获得有记录、有期限的正式例外，否则缺失或过期的语言版本会阻止文档验收。
