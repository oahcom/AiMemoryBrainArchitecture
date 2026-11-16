# Phase 2 — D/E/F/G Cross-Session Review Reconciliation

- Date: 2026-11-16
- Repository: oahcom/AiMemoryBrainArchitecture
- Review type: branch-aware cross-session architecture reconciliation
- Scope: A/B/C specialist reviews and Phase 1 integration review; D/E/F/G branch design documents and branch-local review reports; D main-branch scope correction.
- This is a static document review. It is not implementation, security certification, performance benchmarking, or three separately staffed external reviewers.
- Status: **CONDITIONAL PASS FOR CONTINUED ARCHITECTURE INTEGRATION; NOT READY FOR CONTRACT FREEZE OR IMPLEMENTATION SIGN-OFF.**

---

## 1. Executive decision

The reports cannot be compared by their PASS/FAIL labels alone. The decisive issue is the review baseline.

A/B/C design documents and their specialist reports were present on main and were reviewed against that shared baseline. D/E/F/G used independent delivery branches. Their main-branch review reports therefore assessed an incomplete main tree and marked the missing subsystem documents FAIL / NOT REVIEWABLE. Branch-aware inspection confirms the design documents and branch-local self-review reports exist on their respective branches.

The correct interpretation is:

1. A/B/C and the Phase 1 integration review remain valid reviews of the shared baseline.
2. The main-only D/E/F/G FAIL reports remain valid evidence that those documents were not visible in main at the time of those reviews.
3. Those FAIL labels are not valid design-quality verdicts for the D/E/F/G branch content.
4. D has a separate branch-aware reassessment already recorded at reviews/03-memory-brain/review-scope-correction-and-design-reassessment.md.
5. E/F/G branch-local reports conclude Conditional Pass, but explicitly describe themselves as static self-reviews using simulated architecture, engineering and security lenses. They are not independent external sign-offs.
6. The branch designs are suitable for a coordinated integration review. They are not frozen schemas, wire contracts or implementation-ready security guarantees.

**Overall project disposition: proceed with controlled cross-module contract closure; do not merge all branches blindly and do not start implementation against unresolved P0/P1 contracts.**

## 2. Repositories, branches and review evidence

### 2.1 Shared baseline and A/B/C

The following review artifacts are present on main:

- reviews/architecture/2026-11-16-three-party-six-dimension-review.md
- reviews/architecture/2026-11-16-memory-domain-model-three-party-six-dimension-review.md
- reviews/07-agent-integration/three-party-six-dimension-review.md
- reviews/integration/phase-1-abc-cross-document-integration-review.md

A/B/C design documents are also present on main. The Phase 1 report concludes Conditional Pass: the overall architecture direction is accepted for controlled subsystem deepening, but core domain schema, BMCP wire contract, security and Forget guarantees must not be frozen.

### 2.2 D/E/F/G branch evidence

| Session | Branch | Design commit | Design documents confirmed |
|---|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 9dc08c63f6912320e290a963c634748ec44a81c8 | Five D documents |
| E | session-e-memory-compiler-2026-11-16 | 54df136d1e410af834461950e3c61c5c80abd6ad | Five E documents |
| F | session-f-memory-runtime | dad5deb6bfaa2df9956930d0b1372df354112567 | Five F documents |
| G | session-g-memory-context | 3d2c065be863bc1d349faaeece6f6eaa0047abae | Six G documents |

Each branch also contains a branch-local review report. The E/F/G branch-local reports conclude Conditional Pass. D's branch-local report also concludes conditional acceptance as a candidate specification. All explicitly disclaim implementation/security/performance certification; D/E/F/G reports also disclose simulated review lenses rather than three independent external signatories.

### 2.3 Review-baseline correction

The following main-branch reports were generated while the corresponding subsystem documents were absent from main:

- reviews/03-memory-brain/three-party-six-dimension-review.md
- reviews/04-memory-compiler/three-party-six-dimension-review.md
- reviews/05-memory-runtime/three-party-six-dimension-review.md
- reviews/06-memory-context/three-party-six-dimension-review.md

Their missing-document findings are accurate for the declared main-only baseline. Their subsystem-level FAIL conclusions must be reclassified as **REVIEW_SCOPE_ERROR / NOT REVIEWABLE ON MAIN**, not as proof of a defective D/E/F/G design.

The original reports should be retained as historical evidence. Do not silently overwrite or delete them. The D correction report establishes the required precedent: separate design quality from main-branch integration readiness. Apply the same distinction to E/F/G.

### 2.4 H/I status

The current repository tree contains no H BMCP/protocol design package or I Security/Governance design package and no corresponding H/I specialist review reports. Their responsibilities appear as dependencies in D/E/F/G, but dependency references do not constitute H/I approval.

H/I are therefore explicit integration blockers for final wire, identity, authorization, revocation, retention, backup and physical-erasure contracts.

---

## 3. Reconciled session verdicts

| Session | Main-only review verdict | Branch-aware design evidence | Correct current verdict |
|---|---|---|---|
| A | Conditional Pass | A docs and report on main | Conditional Pass; P0 gates remain open |
| B | P0 domain conflict; schema freeze blocked | B docs and report on main | Conditional / blocked for Fact-Claim freeze |
| C | Conditional Pass | C docs and report on main | Conditional Pass; six P1 interface items remain |
| D | Fail / Not Reviewable | Five docs and branch-local review exist; separate correction review completed | Conditional Pass as candidate design; three D-owned/cross-module P1 corrections remain |
| E | Fail / Not Reviewable | Five docs and branch-local review exist; branch self-review says Conditional Pass | Conditional Pass as candidate design; Accepted/Idempotency, D commit, F watermark and I governance remain open |
| F | Review Blocked / Not Passed | Five docs and branch-local review exist; branch self-review says Conditional Pass | Conditional Pass as candidate design; watermark, revocation and D/E/G/I contracts remain open |
| G | Fail / Not Reviewable | Six docs and branch-local review exist; branch self-review says Conditional Pass | Conditional Pass as candidate design; H Applied proof and I Forget/Scope contracts remain open |

This table does not mark any INT issue CLOSED. It corrects only the status of the subsystem design review based on the actual branch artifacts.

---

## 4. Cross-session consistency findings

### 4.1 Architecture ownership is broadly consistent

The following boundaries agree across D/E/F/G and the A/B/C baseline:

- D owns canonical Memory identity, immutable Memory versions, lifecycle authority, canonical entity/relation assets and canonical Forget state.
- E accepts durable source Events and compiles them into candidate proposals; it does not own canonical truth or lifecycle decisions.
- F performs retrieval, candidate generation, fusion, freshness handling and activation recommendations; it does not own canonical Memory or Context versions.
- G owns desired Memory Context membership, ordering, eligibility, budget and Context version sequence; it does not mutate Canonical Memory.
- H must own BMCP wire encoding, transport, Adapter execution and Adapter-side application attestation.
- I must own global identity/authorization policy, grants/revocation, retention, audit governance, backup/external-copy policy and physical-erasure rules.
- C defines the Agent-side telemetry and inference-boundary semantics; Agent retains reasoning, planning, tool authorization and action authority.

No design should move these responsibilities merely to simplify an implementation.

### 4.2 INT-P0-01 — Fact / Claim canonical model

**Status: OPEN / ADR-BLOCKED.**

B's domain model conflicts with the governance baseline that lists Fact and Claim as distinct concepts. D proposes a FactRecord-style qualification/attestation object and stable Claim revisions, but explicitly labels this candidate. E correctly uses neutral CandidateProposition / ExtractionIR rather than freezing canonical Fact/Claim identity. F preserves Claim revisions and conflicts without adjudicating. G pins exact canonical Memory versions and preserves epistemic/conflict metadata.

Required action:
- Architecture Governance + B own the ADR.
- D defines the approved canonical representation after the ADR.
- E supplies an explicit mapping from neutral Candidate IR to the approved canonical model.
- F/G consume the approved IDs and revision semantics.
- No canonical Fact/Claim schema, API or wire contract may be frozen before the ADR is approved and all references are synchronized.

### 4.3 INT-P0-02 — Scope isolation

**Status: DESIGN COVERAGE EXISTS; POLICY AND END-TO-END PROOF OPEN.**

D defines object-level Scope and pre-candidate constraints. E carries Scope through ingress, source dereference, entity search, consolidation, write, replay and reauthorization. F specifies Scope-before-Candidate inside every candidate-producing backend, graph edge/target reauthorization, scoped caches and response-boundary revalidation. G binds Context and Delivery to Scope and reauthorizes before materialization, delivery and application.

The missing authority is not another local filter. H/I must define authenticated Principal/ActorRef, issuer/delegation, permission epoch and revocation semantics. I must own the policy and cross-system negative-test matrix.

Required action:
- B/I/H close the common Principal, ActorRef, ScopeRef and permission-epoch semantics.
- D/E/F/G/H implement the same authorization context and fail-closed rules at their boundaries.
- Test ANN, lexical, structured, temporal, graph, evidence, provenance, cache, replay, Context delivery and offline reconnect paths.
- Do not mark INT-P0-02 closed because each subsystem describes a local check.

### 4.4 INT-P0-03 — Forget, revocation and anti-resurrection

**Status: PARTIALLY DESIGNED ACROSS D/E/F/G; GLOBAL COMPLETION CONTRACT OPEN.**

The module responsibilities are complementary:

- D owns canonical ForgetOperation, canonical suppression fence and dependency inventory.
- E must suppress queued, leased, retrying, dead-letter and replayed compiler work, and register derived dependencies.
- F must suppress candidate generation, in-flight responses, caches and Working Sets; canonical Forget state overrides stale index state and rebuild.
- G must tombstone Context entries, invalidate snapshots/deltas, cancel pending deliveries, block new Applied confirmations and keep offline Adapter state pending/unknown until safe reconnect and attestation.
- H must define Adapter clear/reconnect behavior and trustworthy acknowledgement.
- I owns retention, backup, external recipient and global completion policy.

Three problems remain:

1. D-REV-P1-003: D has not fully closed the late-derivative race. A compiler job, replay, projection rebuild or delayed delivery must not publish a newly visible derivative after Forget completion.
2. E/F/G refer to fences, epochs, watermarks and tombstones, but their exact shared identity, scope, ordering and retention are not yet one normative contract.
3. Global completion must distinguish immediate access suppression from asynchronous cleanup and physical erasure. Unknown/offline/unreachable targets cannot be silently counted as confirmed.

Required action:
- Define one durable ForgetOperation ID and monotonically ordered fence/generation with explicit scope and affected canonical references.
- Every producer checks the fence before committing or publishing; every consumer checks it before candidate exposure, cache return, Context delivery and final inference application.
- Define producer registration/acknowledgement or a closed watermark barrier so no earlier in-flight work can register a late derivative invisibly.
- Define per-target states pending/confirmed/failed/unknown and policy-approved residual exceptions.
- Completion requires the barrier to be crossed and all required targets either confirmed or explicitly excepted by I; a tombstone alone is not proof of physical erasure.
- Run a race matrix covering concurrent canonical writes, delayed compiler jobs, outbox replay, index rebuild, retrieval in flight, Context ChangeSet, Prepared/Delivered delivery, late Applied ACK, offline Adapter reconnect and backup restore.

This is the highest-priority cross-session workstream.

### 4.5 INT-P0-04 — Memory prompt injection

**Status: DESIGN BOUNDARY CONSISTENT; RESIDUAL RISK AND END-TO-END TESTING OPEN.**

D/E/F/G consistently treat Memory, Evidence, summaries, entity labels and relation qualifiers as untrusted data, not instructions or tool authority. C protects System/Developer/User regions and Agent policy. This is the correct boundary.

No document can guarantee that an LLM will ignore malicious content once it is included in an inference request. I must own the threat model and risk acceptance; H/C must prove that managed Memory cannot overwrite protected regions or bypass the Agent's authorization boundary. Test retrieval poisoning, indirect instructions, provenance laundering, summary/compaction laundering and cross-scope injection.

### 4.6 INT-P1-01 — Context Version / Change Set authority

**Status: OWNERSHIP AGREED; WIRE AND INTEGRATION CONTRACT OPEN.**

D supplies immutable Memory ID + exact MemoryVersion references and canonical invalidation signals. F returns immutable RetrievalResult and ActivationRecommendation, not ContextEntry or ContextVersion. G owns ContextVersion, ContextChangeSet, atomic edit semantics, CAS and reconciliation. H owns wire encoding and Adapter application.

This is one of the strongest areas of agreement. Preserve it. Do not let F create Context entries or D own Context versions.

### 4.7 INT-P1-02 — Claim identity, revision, Conflict Set and Entity Merge/Split

**Status: OPEN / CANDIDATE.**

B's Fact/Claim baseline conflict blocks canonical identity. D proposes stable Claim ID + immutable ClaimRevision, ConflictSet and explicit Entity Merge/Split migration records. E emits revision/conflict proposals but does not adjudicate. F preserves competing claims and evidence. G pins exact Memory versions and reconciles changed references.

Required action:
- Resolve Fact/Claim ADR first.
- D/B finalize Claim identity, revision and ConflictSet semantics.
- D finalizes Entity Merge/Split and relation migration records.
- E maps proposals to the approved model.
- F/G consume exact version and invalidation events without inventing identity rules.

### 4.8 INT-P1-03 — Telemetry identity, Scope and event semantics

**Status: OPEN WITH C/B/H/I.**

C identifies producer/Agent/instance/session/task/environment and Observation/Outcome distinctions. E requires authenticated producer binding and reauthorization at processing time. D uses typed ActorRef/ScopeRef candidates. F/G require trusted identity and environment binding.

Required action:
- H/I define authenticated Principal, producer identity, issuer/delegation and revocation epoch.
- B defines typed identity/reference semantics.
- C defines telemetry event/revision/ordering semantics.
- E must reject payload self-assertions that do not match authenticated identity.
- Environment identity must be mandatory where memories are environment-dependent.

### 4.9 INT-P1-04 — Accepted / durable ingestion / idempotency

**Status: E DESIGN ADDRESSED; H/I/STORAGE DETAILS OPEN.**

E correctly distinguishes Accepted, Processed/Compiled, Canonical Commit and Indexed. It requires Event + payload reference + idempotency record + receipt + compile intent to become durable atomically or through an equivalent recoverable protocol. Same key/same payload returns the original receipt; same key/different payload conflicts. Model outage does not revoke Accepted durability.

Required action:
- H finalizes wire envelope and receipt.
- I finalizes identity binding and retention/tombstone horizon.
- Storage/Consistency chooses the concrete transaction/outbox or WAL implementation.
- C/E agree on source ordering, late event and per-source sequence semantics.
- Do not confuse Event acceptance with canonical Memory commit or index visibility.

### 4.10 INT-P1-05 — Applied proof

**Status: SEMANTIC REQUIREMENT AGREED; H/C PROOF ENCODING OPEN.**

C and G agree that Applied is not an Adapter's internal insertion success. Full Applied requires the exact target Context version to be completely materialized in the controlled managed region and that region to belong to the final request actually submitted to the inference runtime. Partial, Bypassed and Unknown are not Full Applied. Applied does not prove model attention or use.

Required action:
- C/H define final-request boundary observability, attestation/digest privacy and capability epoch.
- G binds attestation to Context, Delivery, session and target version.
- H must not claim Tier 1/Full when it cannot observe the final request boundary.
- Conformance tests must include partial application, retry, timeout, late ACK and superseded version.

### 4.11 INT-P1-06 — Provenance, Lifecycle, typed references and freshness watermarks

**Status: PARTIALLY DESIGNED; CROSS-MODULE CURSOR SEMANTICS OPEN.**

D proposes immutable canonical versions and a LifecycleEvent authority; E persists Evidence/Provenance lineage and dependency registrations; F requires per-channel index watermarks and canonical revalidation; G reconciles canonical changes and retrieval completeness.

The design documents currently use several distinct ordering concepts that must not be conflated:
- source Event sequence / durable ingestion cursor;
- canonical commit sequence;
- per-aggregate Memory/Claim revision;
- LifecycleEvent sequence;
- per-index or per-partition publication watermark;
- Forget fence/epoch;
- Context version;
- Delivery sequence/ID;
- Adapter capability epoch and inference request ID.

D-REV-P1-002 already identifies ambiguity about global versus per-aggregate canonical sequence. E/F/G need a shared cursor contract with typed namespaces, partition/scope, monotonicity, gap meaning, replay rules and causal relation. A single untyped integer called generation/watermark is insufficient.

Required action:
- D + Storage/Consistency define canonical commit cursor and lifecycle authority.
- E defines durable Event cursor and canonical publication/outbox cursor.
- F defines per-channel/per-partition index watermark and required-fence behavior.
- G defines the exact reconciliation watermark tuple it consumes.
- H/C define request/delivery correlation identifiers separately.
- B/D/I close TypedObjectRef, ScopeRef, ActorRef, ContentRef, TimeValue and TimeInterval semantics.

---

## 5. Confirmed D-local findings from branch-aware reassessment

These are not inherited from the main-only missing-file report:

| ID | Severity | Finding | Owner | Exit condition |
|---|---|---|---|---|
| D-REV-P1-001 | P1 | Forgetting is described inconsistently as a Memory lifecycle state versus a ForgetOperation state | D | One normative lifecycle table; in-progress Forget suppression belongs to ForgetOperation, not a competing Memory lifecycle state |
| D-REV-P1-002 | P1 | Canonical commit sequence scope is unclear: global stream, per-aggregate sequence or both | D + Storage/Consistency | Store, Versioning, E, F and G use typed and consistent cursor semantics |
| D-REV-P1-003 | P1 | Forget completion lacks a fully closed late-derivative barrier | D + I; E/F/G/H enforce | Durable fence plus producer barrier/watermark; race matrix proves no late re-exposure |

The Fact/Claim ADR, generic Scope algebra, ActorRef authentication and global Forget physical-erasure policy are not D-only defects. They remain owned by Governance/B/I/H with D as a contributor.

---

## 6. Additional integration work items

These are cross-module contract gaps, not findings that the subsystem documents are absent.

| ID | Priority | Work item | Owners | Dependency |
|---|---|---|---|---|
| INT-X-01 | P1 | Define typed cursor/watermark namespaces and causal ordering | D/E/F/G + Storage/Consistency | D-REV-P1-002 |
| INT-X-02 | P1 | Define one Forget fence, producer barrier, derivative registration and global completion protocol | D/E/F/G/H/I | INT-P0-03 |
| INT-X-03 | P1 | Finalize Principal/ActorRef/ScopeRef/permission epoch and environment binding | B/C/H/I + D/E/F/G | INT-P0-02, INT-P1-03 |
| INT-X-04 | P1 | Finalize Context delivery, final-request Applied attestation and clear/reconnect contract | C/G/H + I | INT-P1-01, INT-P1-05, INT-P0-03 |
| INT-X-05 | P1 | Finalize canonical lifecycle authority, Claim revision and ConflictSet after ADR | B/D + E/F/G | INT-P0-01, INT-P1-02, INT-P1-06 |
| INT-X-06 | P1 | Define Accepted receipt, idempotency scope, replay ordering and retention | C/E/H/I + Storage/Consistency | INT-P1-03, INT-P1-04 |
| INT-X-07 | P2 | Shared conformance and fault-injection suite across all boundaries | C/D/E/F/G/H/I + Testing | INT-X-01 through INT-X-06 |
| INT-X-08 | P2 | Representative workload benchmarks and local resource budgets | D/E/F/G + Engineering | Stable candidate interfaces |

---

## 7. Recommended remediation sequence

### Gate 0 — Correct review bookkeeping

1. Retain the original main-only D/E/F/G reports as historical records.
2. Mark their conclusions as main-branch delivery visibility failures, not design-quality verdicts.
3. Link each report to the exact branch and commit reviewed.
4. Do not mark any INT issue closed by this bookkeeping correction.
5. Keep design review, main integration readiness and implementation verification as separate statuses.

### Gate 1 — Governance and identity baseline

1. Approve INT-P0-01 Fact/Claim ADR.
2. Finalize Principal/ActorRef/producer binding, ScopeRef and permission epoch.
3. Finalize typed references and temporal value contracts.
4. Decide the canonical lifecycle authority and canonical commit cursor semantics.

No Fact/Claim schema or final wire contract freeze before this gate exits.

### Gate 2 — Forget and revocation protocol

1. Define the durable Forget fence/generation and its scope.
2. Define producer registration and the barrier that accounts for in-flight compilation/replay/publication.
3. Define F cache/index suppression and rebuild rules.
4. Define G Context/delivery cancellation and offline Adapter reconnect behavior.
5. Define H clear attestation and I global completion/backup/external-copy policy.
6. Pass the full race and anti-resurrection matrix.

This gate blocks security-sensitive implementation and any deletion guarantee.

### Gate 3 — Cross-module data and version contracts

1. Event Accepted receipt and idempotency contract.
2. Canonical Commit, LifecycleEvent and outbox publication.
3. Index generation/watermark and canonical consistency fence.
4. RetrievalResult and ActivationRecommendation.
5. ContextChangeSet, ContextVersion, Delivery and Applied attestation.
6. Typed cursor namespaces and replay/resume behavior.

### Gate 4 — Conformance before implementation sign-off

Required tests:
- duplicate Event same key/same payload and same key/different payload;
- crash before/after Accepted response and outbox dispatch;
- compiler retry, DLQ replay and revocation during processing;
- Scope filtering before ANN/lexical/structured/temporal candidate emission;
- graph edge/target and Evidence/Provenance independent authorization;
- index lag, missing publication, rebuild and stale canonical versions;
- Forget during concurrent write, compile, retrieval, cache fill, Context update, delivery, late ACK, offline reconnect and backup restore;
- ChangeSet CAS races, duplicate Delta, base mismatch and all-or-nothing failure;
- Applied proof against the actual final inference request;
- provenance lineage cycle, fan-out, source unavailable and Forget dependency traversal.

Only after correctness conformance should performance thresholds be set. No P95/P99, throughput, VRAM or latency claim is accepted without a reproducible benchmark declaration.

---

## 8. Current release gate

| Gate | Status | Reason |
|---|---|---|
| A/B/C architecture direction | Conditional Pass | A/B/C integration permits controlled deepening; P0/P1 semantics remain open |
| D design review | Conditional Pass | Branch-aware review completed; three P1 corrections required |
| E design review | Conditional Pass | Branch-local documents exist; H/I/D/F integration details open |
| F design review | Conditional Pass | Branch-local documents exist; D/E/G/I cursor, fence and policy contracts open |
| G design review | Conditional Pass | Branch-local documents exist; H Applied proof and I global governance open |
| H protocol/wire review | Not started / no artifacts found | Wire, authentication and Adapter proof contract absent |
| I security/governance review | Not started / no artifacts found | Global policy, revocation, retention, backup and erasure authority absent |
| Cross-module contract freeze | BLOCKED | INT-P0-01..04 and INT-P1-01..06 not closed |
| Rust implementation sign-off | BLOCKED | No integrated conformance evidence or H/I contracts |
| Performance sign-off | NOT ASSESSABLE | No reproducible workload benchmark |

---

## 9. Final verdict

**The architecture direction is coherent enough to continue. The reports do not justify restarting D/E/F/G. They justify a controlled integration and correction phase.**

The immediate work is not to rewrite all four subsystems. It is to:
1. correct the branch-baseline error in D/E/F/G review bookkeeping;
2. fix D's three P1 issues;
3. close the shared Fact/Claim, Scope/Identity and Forget decisions;
4. define typed cursor/watermark and Applied proof contracts across D/E/F/G/H/I;
5. perform a true cross-module review after H/I provide their owned specifications.

Until those conditions are met, keep D/E/F/G branches separate, do not merge them wholesale, do not freeze wire/schema contracts, and do not describe static Conditional Pass as implementation/security approval.
