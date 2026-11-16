# Phase 3 — D/E/H/I Cross-Module Contract Review

- Review date: 2026-11-16
- Review type: Branch-aware static contract review
- Status: **CONDITIONAL PASS FOR CONTINUED INTEGRATION; NOT READY FOR CONTRACT FREEZE OR IMPLEMENTATION SIGN-OFF**
- Scope: D Memory Brain, E Memory Compiler, H BMCP/Adapter, I Security & Governance; A Contract Registry and typed-cursor proposal inspected as coordination artifacts.
- No branch was merged or modified by this review. This report does not approve any module's internal authority model.

## 1. Exact reviewed branch heads

| Session | Branch | Reviewed head |
|---|---|---|
| A | session-a-integration-2026-11-16 | f76cc558273fbc1a27bb930a2f1e8d940b717c80 |
| B | session-b-domain-model-phase3 | ab19afbf92f67fe0a7679e9aa3a35b015fed89f4 |
| D | session-d-memory-brain-2026-11-16 | 30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6 |
| E | session-e-memory-compiler-2026-11-16 | 3dea6096eefa6779eb12e4e788bcf9429d2a3f83 |
| H | session-h-bmcp-protocol | fcc5103399b4c322e52d642cae5a2414969399a7 |
| I | session-i-security-governance-2026-11-16 | 8c91d99e450ab5e8862bd6a3301fa193e28e6cbb |

Key files inspected:
- A: reviews/integration/contract-registry.md; reviews/integration/typed-cursor-and-watermark-contract.md
- D: 03-memory-brain/forget-fence-and-completion-contract.md; 03-memory-brain/commit-cursor-semantics.md; D review
- E: 04-memory-compiler/forget-fence-and-derived-registration.md; 04-memory-compiler/accepted-receipt-and-idempotency-contract.md; 04-memory-compiler/decision-change-log.md; E review
- H: 08-bmcp-protocol/forget-revocation-and-reconnect.md; 08-bmcp-protocol/message-envelope-and-versioning.md
- I: 09-security-governance/forget-retention-backup-and-erasure-policy.md; 09-security-governance/principal-actor-and-authorization-contract.md; 09-security-governance/scope-and-revocation-policy.md

## 2. Executive assessment

D/E/H/I are now present as substantive candidate design packages. Their authority boundaries are broadly compatible:

- D owns canonical Memory identity/version, canonical ForgetOperation and ForgetFence semantics, and canonical commit ordering.
- E owns durable ingress/receipt, compiler work, derived lineage and producer-side enforcement.
- H owns BMCP wire/Adapter behavior, managed-region clear/reconnect and Adapter-local acknowledgements.
- I owns authenticated identity and authorization policy, revocation, retention, target inventory, global Forget completion and physical-erasure policy.

The packages correctly avoid collapsing Accepted receipt into compilation or canonical commit; canonical suppression into asynchronous cleanup or physical erasure; Adapter-local clear acknowledgement into global Forget completion; or permission epoch, Forget fence, canonical cursor, aggregate revision, lifecycle cursor and index watermark into one scalar.

Two cross-module contracts remain open: D/E producer-registration and publication linearization, and propagation of D's canonical cursor decision into A/E coordination artifacts. A's registry is materially stale.

## 3. Findings

### CR-P1-01 — D/E producer registration and publication gate are not yet an implementable closed contract

**Status: OPEN / BLOCKING FOR FORGET CONFORMANCE**

D's new Forget contract establishes strong normative invariants:
- each work item is durably registered before execution, lease, retry, DLQ replay or publication;
- fence installation atomically captures the producer-registration high-water mark;
- pre-fence work must reach a durable terminal disposition;
- every derivative and dependency edge must be durable before visibility;
- the final publish/commit gate rechecks the latest applicable fence;
- unknown producer classes, registry gaps, unresolved leases and late derivatives prevent barrier closure.

E's enforcement contract correctly requires staged invisible output, durable lineage, D dependency-registration acknowledgement, a current fence/authorization recheck and a publication gate. It explicitly says a local E check cannot close the race.

The remaining gap is not the safety principle; it is the cross-module operation/linearization contract. D describes required atomic behavior but does not yet expose a sufficiently precise operation contract that E/Storage can implement and test. E asks for an atomic or linearizable register-if-fence-open / producer-lease operation and a publication gate tied to the same fence epoch, or an equivalent protocol.

**Required D/E/Storage resolution:**
1. Define producer-class registration separately from per-work-item admission/registration.
2. Define the exact linearization order between work registration and fence installation. Every race must serialize to either “included in the barrier” or “rejected/quarantined”.
3. Define the atomicity boundary for dependency-edge registration and derivative visibility. A staged object must remain invisible if registration or the final fence check fails.
4. Define the final publish operation's required inputs and evidence: stable work/attempt ID, source refs/revisions, ScopeRefs, observed fence, permission epoch, registration receipt and target derivative identity.
5. Define retry, lease expiry, process crash and recovery behavior without allowing a queue item or lease to disappear from the barrier.
6. Provide conformance cases proving both race outcomes and no late publication after barrier closure.

Until resolved, classify D's semantics as specified but D/E/Storage enforcement as OPEN. Do not mark D-REV-P1-003 or INT-P0-03 closed.

### CR-P1-02 — D's canonical cursor decision conflicts with A's typed-cursor proposal and E's stale descriptions

**Status: OPEN / COORDINATION CORRECTION REQUIRED**

D's latest commit-cursor-semantics document makes an explicit owner decision:
- one globally ordered CanonicalCommitCursor per Canonical Memory authority;
- independent AggregateRevision per aggregate;
- LifecycleEventCursor per Memory;
- F-owned IndexWatermark per index/channel partition;
- ForgetFence generation is a separate fencing namespace, not a cursor.

A's current typed-cursor-and-watermark proposal still proposes a partitioned CanonicalCommitCursor and says D-REV-P1-002 is open pending D/Storage approval. E's decision-change-log also retains statements that D's cursor scope remains open. These are stale relative to D's latest owner decision.

**Required resolution:**
1. A must update its typed-cursor proposal to record D's selected per-authority global CanonicalCommitCursor, while keeping Storage/Consistency realization and durability/recovery validation open.
2. E must consume D's latest cursor contract and remove statements that cursor scope remains undecided. E must store D's typed cursor unchanged and must not confuse it with AggregateRevision, LifecycleEventCursor or F IndexWatermark.
3. F/G consumers must be checked against this decision before the cursor contract is declared integrated.
4. Storage/Consistency must validate the actual single-authority sequencing/transaction model. D's semantic decision is not evidence that a storage implementation exists or passes fault tests.

A's coordination proposal must not override D's cursor authority. D's semantic decision does not by itself settle multi-authority distribution or implementation topology.

### CR-P1-03 — A Contract Registry has stale source baselines and stale H/I presence status

**Status: OPEN / A UPDATE REQUIRED**

A's current registry still lists old D/E commit SHAs and says H/I are not present. The current branch inventory confirms all four packages exist. The registry therefore cannot serve as a reliable Phase 3 source-of-truth until updated.

A should:
- update exact D/E/H/I branch heads and reviewed artifact paths;
- record H/I as candidate packages, not approved contracts;
- preserve the distinction between package existence, owner decision, cross-module agreement and implementation evidence;
- update CR-P1-01/02 and related INT issue dispositions without declaring them closed prematurely.

The registry's warning that it is a coordination register rather than an ADR remains correct.

### CR-P1-04 — E's decision/change log contains superseded source-review statements

**Status: OPEN / E DOCUMENT HYGIENE REQUIRED**

E's decision-change-log includes earlier statements that D's fence/barrier was not closed, H/I branches were absent, and the D cursor scope remained open. Later sections partially correct these statements, but the document still presents multiple historical states without consistently marking earlier sections as superseded.

E should preserve audit history but add an explicit supersession notice and a current authoritative dependency disposition. At minimum:
- H/I are present candidate packages at the reviewed heads in this report;
- D's current cursor semantic decision is per-authority global;
- D's current Forget contract specifies a producer-registration barrier and register-before-visible invariants;
- the exact D/E/Storage atomic registration/publication operation remains open, which is narrower and more precise than saying the barrier is wholly undefined;
- B Fact/Claim mapping remains ADR-BLOCKED.

E's existing five-file review limitation and any incomplete self-review evidence must remain explicit until verified. Do not infer full review from the existence of the new contracts alone.

### CR-P1-05 — I's global Forget vector and D/H/E target semantics are directionally aligned, but status mapping remains open

**Status: CANDIDATE / NEEDS OWNER MAPPING**

I defines global Forget proof as a typed vector spanning:
- D canonical ForgetFence and producer/in-flight barrier;
- E source/compile and derivative-registration watermarks;
- F per-index/per-partition publication and suppression watermarks;
- G Context reconciliation/delivery watermarks;
- H Adapter capability/session/delivery clear attestations;
- external recipients and backup/restore evidence.

I requires a sealed target inventory, all derivative-capable producers crossing the barrier or being disabled/revoked, all pre-barrier work terminal, consumers advanced beyond the required fence, and no unresolved required Unknown/Failed targets. This is compatible with D's distinction between canonical suppression and I-owned global completion.

H correctly states that its local ACK is bounded to one Adapter instance and managed region, binds operation/fence/permission/context/delivery/capability evidence, and is not a global verdict. Offline reconnect authenticates, negotiates capabilities, obtains current permission epoch and Forget fence, clears affected state, reconciles deliveries, then applies only the current authorized Context.

Remaining owner mapping work:
1. Map each H ACK class (SUPPRESSED, LOCAL_BUFFER_CLEARED, LOCAL_CACHE_PURGED, QUEUED_DELIVERY_CANCELLED, FAILED, UNKNOWN, UNSUPPORTED) to I's per-target states and evidence requirements.
2. Specify how Adapter identity, capability epoch, session, scope and managed-region coverage identify the exact I inventory target.
3. Define how an offline/unsupported Adapter is represented as Unknown or as a narrowly scoped, explicitly approved PolicyException. It must never become implicit success.
4. Distinguish I's producer-domain registration epoch (closed-world inventory of producer/recipient classes) from D's per-work-item registration high-water/barrier. Both levels are needed; one cannot silently substitute for the other.
5. Define the typed relation between D's fence generation and I's policy/permission epoch without numeric comparison or token reinterpretation by H/E.

These are not evidence of a fundamental H/I contradiction; they are unresolved cross-owner mappings.

### CR-P0-01 — Fact/Claim remains ADR-BLOCKED

**Status: BLOCKING / CORRECTLY PRESERVED**

B's Fact/Claim ADR has not been verified as formally approved. E correctly keeps CandidateProposition/ExtractionIR mapping blocked from canonical Claim. D's review also prohibits schema/API freeze before the ADR.

No D/E/H/I document may convert a candidate option into an approved Fact/Claim canonical schema or wire field. A must continue to mark this issue ADR-BLOCKED.

### CR-P0-02 — Principal/ActorRef/ScopeRef and permission binding remain candidate

**Status: OPEN / BLOCKING FOR IDENTITY CONTRACT FREEZE**

I's identity model is directionally sound: authenticated issuer-bound Principal, ActorRef as a typed reference rather than a credential, payload ActorRef/producer IDs as claims only, current authorization at each protected boundary, and permission epochs scoped to a policy domain. H correctly requires authenticated transport binding and rejects payload identity as proof.

But B owns typed ActorRef/ScopeRef domain reference semantics, and the exact cross-module identity mapping remains open. H's envelope still marks exact identity/permission fields candidate or ADR-blocked. E's idempotency namespace depends on authenticated producer and security-domain binding.

Do not freeze BMCP identity fields, idempotency namespace serialization or public schemas until B/I/H and affected consumers reconcile exact typed references and issuer/delegation rules. Fail closed on identity mismatch, unknown issuer, stale permission epoch or inability to establish current authorization.

## 4. Cross-module contract matrix

| Contract | Current alignment | Remaining closure |
|---|---|---|
| D canonical Forget authority → E compiler | Directionally aligned | Atomic registration/fence/publication gate and executable race semantics |
| D canonical cursor → E receipt/publication | Owner decision now explicit | E/A updates; Storage validation; F/G consumer conformance |
| I identity/permission → H transport | Directionally aligned | B typed-reference approval; exact wire binding and negative tests |
| I identity/permission → E worker/replay | Candidate aligned | Exact Principal/ProducerIdentity/ScopeRef mapping and epoch checks |
| D ForgetFence → H Adapter | Directionally aligned | Typed token comparison contract and target inventory mapping |
| H Adapter ACK → I global completion | Compatible separation | Explicit ACK-to-target-state/evidence mapping |
| D/E producer barrier → I global completion | Compatible concepts, two levels | Domain registry epoch vs per-work-item barrier reconciliation |
| B Fact/Claim → D/E | Correctly blocked | Approved ADR and synchronized consumer mapping |

## 5. Gate disposition

| Gate / issue | Disposition |
|---|---|
| D/E delivery existence | PASS — files and branch heads verified |
| D/E/H/I authority boundaries | CONDITIONAL PASS |
| INT-P0-01 Fact/Claim | ADR-BLOCKED |
| INT-P0-02 Identity/Scope/Permission | OPEN |
| INT-P0-03 Forget end-to-end | OPEN — D/E/Storage atomic gate and F/G/H/I evidence required |
| INT-P0-04 Prompt injection | OPEN — separate threat-model and adversarial conformance gate |
| INT-X-01 typed cursors | OPEN — D decision exists; A/E and consumers not synchronized |
| INT-X-02 Forget barrier | OPEN — semantics advanced; cross-module atomic enforcement not proven |
| INT-X-03 identity binding | OPEN |
| INT-X-06 Accepted/idempotency/replay | CANDIDATE — storage, H/I identity and retention approval required |
| Implementation / fault-injection / security tests | NOT RUN / NOT EVIDENCED |

This review is static document analysis only. It does not establish code implementation, runtime behavior, penetration-test results, performance results, backup erasure or production readiness.

## 6. Required next actions and owners

1. **D + E + Storage/Consistency:** specify the atomic producer admission/fence installation/publication gate and its crash/race contract. Keep D-REV-P1-003 and INT-P0-03 open until conformance evidence exists.
2. **A:** update Contract Registry and typed-cursor proposal to current D/E/H/I branch heads and D's global per-authority CanonicalCommitCursor decision.
3. **E:** reconcile its change log and accepted-receipt cursor references with current D/H/I artifacts; explicitly preserve the remaining atomic-gate and storage dependencies.
4. **H + I + B:** finalize authenticated Principal/ActorRef/ScopeRef/ProducerIdentity binding, permission epoch semantics and Adapter ACK-to-target evidence mapping.
5. **I + D + E + H:** reconcile producer-domain inventory epoch with D's work-item barrier and I's global Forget completion vector.
6. **F + G:** after the above owner corrections, consume the same typed cursor and Forget contracts; demonstrate index/cache/Working Set suppression and Context/delivery invalidation before claiming end-to-end closure.
7. **A / integration governance:** run shared conformance and fault-injection tests only after relevant owner contracts are synchronized. Record test IDs, fixtures, environment, expected/actual results and reproducible evidence.

## 7. Final decision

**D/E/H/I are suitable to continue cross-module integration, but the four-way contract is not yet freeze-ready.**

The most important immediate blocker is no longer absence of D's Forget semantics; it is the missing implementable atomic boundary connecting D's producer barrier to E's staged derivative registration and publication. In parallel, A and E must synchronize on D's newly decided canonical cursor semantics. H/I's global policy and Adapter boundaries are compatible in principle but still require exact identity, target and acknowledgement mapping.

No branch merge is authorized or implied by this report.
