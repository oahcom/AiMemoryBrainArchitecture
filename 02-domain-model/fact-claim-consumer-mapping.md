# Fact / Claim Consumer Mapping

- **Status:** CANDIDATE mapping; canonical Fact/Claim portions ADR-BLOCKED
- **Owner:** Memory Domain Model (B)
- **Related issues:** INT-P0-01, INT-P1-02, INT-P1-06, DM-003, DM-004, DM-006
- **Branch:** `session-b-domain-model-phase3`
- **Base:** `main@8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`

## 1. Purpose and non-goals

Define the semantic mapping boundary from E's neutral CandidateProposition/ExtractionIR to a future approved canonical model, and specify how D/F/G consume the resulting references consistently.

This document does not approve Fact/Claim identity, define D's storage mechanism, define I's authorization policy, define H's wire protocol, or define G's Context version authority. All Fact/Claim canonical identity fields remain blocked until ADR-001 is approved.

## 2. Shared vocabulary

- **CandidateProposition:** E-owned extraction hypothesis tied to an immutable source span/locator. It is not a canonical Claim or Fact.
- **Claim:** if approved, an attributable proposition thread with stable identity and immutable revisions.
- **ClaimRevision:** if approved, one immutable exact assertion state under a Claim.
- **Fact / FactRevision:** exists only if Option A is approved; a separate attestation identity/revision, not a confidence label.
- **Evidence:** source material or observation supporting/refuting/qualifying a specific target revision.
- **Provenance:** derivation lineage for a target, recording source refs, method/version, input digests and derivation time.
- **ConflictSet:** durable grouping of incompatible exact ClaimRevisionRefs and resolution history; final canonical shape/commit mechanics belong to D.
- **MemoryVersion:** immutable snapshot committed by D; may contain/pin exact ClaimRevision refs according to approved mapping.
- **Scope:** domain namespace/applicability context; not Permission.

## 3. E mapping: CandidateProposition / ExtractionIR to canonical semantics

### 3.1 Preserve the neutral input

E's ExtractionIR remains source- and method-pinned:
- source EventRef/ContentRef and digest/version;
- exact SourceSpan/Locator and encoding/normalization version;
- source ScopeRefs and Environment Scope from trusted ingress metadata;
- modality, source epistemic basis and uncertainty;
- normalized subject/predicate/object hypotheses, polarity and qualifiers;
- extraction confidence with method/version;
- evidence span reference, ambiguity refs and unresolved fields;
- extraction method receipts and Provenance inputs.

No canonical identity is assigned at this stage. A model-generated proposition ID or text hash is not a Claim ID.

### 3.2 Common mapping preconditions

Before canonical mapping:
1. Resolve authenticated ActorRef and trusted ScopeRefs; payload text cannot self-assert identity or scope.
2. Validate source EventRef, exact source digest and locator/span against immutable source bytes.
3. Preserve modality: planned/intended/predicted/attempted/questioned/quoted do not become completed outcomes.
4. Preserve uncertainty and unresolved fields; do not fill unknown values by plausibility.
5. Create/validate Evidence and Provenance proposals with target-specific roles and exact source lineage.
6. Resolve Entity mentions through D's Entity authority; ambiguity remains explicit.
7. Apply domain Scope compatibility checks. I separately authorizes all protected operations and Evidence dereferences.
8. Compare against canonical candidates only after Scope/permission filtering and with the current canonical snapshot/version supplied by D.

### 3.3 Conditional mapping if Option A is approved

1. Emit a Claim proposal for each attributable proposition candidate that passes semantic validation.
2. Assign/resolve Claim identity only through D's canonical identity authority; E submits a candidate key/relationship proposal, never self-mints canonical ClaimRef.
3. Submit an immutable ClaimRevision proposal containing normalized proposition, polarity, qualifiers, epistemic status, valid interval, Scope, ActorRef, source/method metadata and parent ClaimRevisionRef where revising.
4. Attach EvidenceLinks to the exact proposed ClaimRevisionRef with supports/refutes/qualifies/context_only roles. E supplies source evidence; D validates canonical references and commit atomicity.
5. Submit Provenance node/edges for extraction, normalization, inference or correction, with input digests and method versions.
6. A separate Fact proposal may be emitted only when an explicit verification/adjudication operation exists with authorized attestor, method, qualifying evidence and declared validity semantics. It references exact ClaimRevisionRef(s); extraction confidence alone MUST NOT produce Fact or Verified status.
7. If Fact adjudication is unavailable, the Claim remains reported/observed/inferred/candidate as supported; no synthetic Fact is created.

### 3.4 Conditional mapping if Option B is approved

1. Emit a Claim proposal and immutable ClaimRevision proposal as above.
2. Fact is not assigned an identity or persisted separately.
3. A ClaimRevision may carry a fact-qualified/Verified epistemic qualification only when the approved verification method, authority and evidence conditions are met.
4. EvidenceLinks and Provenance attach to the exact ClaimRevision; “fact” is a derived view/qualification of that revision, not a second object.
5. Historical fact views resolve to the exact ClaimRevision and method/evidence basis that supported the qualification at that time.

### 3.5 Mapping outcomes

| Outcome | Meaning | Canonical effect |
|---|---|---|
| Candidate only | Insufficient identity, evidence, scope or temporal precision | No canonical Claim/Fact identity |
| Claim proposal | Attributable proposition with traceable source/method | D may accept/defer/reject after ADR |
| Revision proposal | Explicit correction/refinement/retraction against exact prior revision | D validates expected parent and commits/rejects |
| Conflict proposal | Incompatible exact proposition revisions in comparable Scope/time/modality | D owns canonical ConflictSet decision |
| Fact proposal (Option A only) | Explicit authorized verification/attestation over exact ClaimRevision(s) | D may commit separate Fact revision only after governance approval |
| Deferred/ambiguous | Unresolved entity/time/source or high-impact dispute | Preserve candidate and lineage; no guessed identity |

## 4. Canonical identity, revision and conflict semantics

### 4.1 Claim identity

**Candidate pending ADR:** stable ClaimRef denotes a proposition thread; it is not content hash, display label, memory identity, source event identity, or a mutable “latest value” record. One Claim may have multiple immutable ClaimRevisionRefs.

### 4.2 ClaimRevision

Each committed ClaimRevision is immutable and exact. It contains or resolves:
- ClaimRef and revision sequence;
- one parent revision except genesis;
- proposition payload and vocabulary/schema versions;
- subject EntityRef/EventRef/typed subject ref, predicate, object, polarity and qualifiers;
- epistemic status and method-qualified confidence (optional);
- valid TimeInterval (unknown explicitly represented);
- EvidenceLink refs and Provenance refs;
- owner/applicability ScopeRefs;
- ActorRef, asserted/recorded/commit time and change reason;
- content digest and explicit correction/supersession/retraction relation.

Correction, refinement, epistemic reassessment, valid-time correction and retraction append a new revision. No consumer mutates a revision in place.

### 4.3 Evidence and Provenance

Evidence is independently addressable and access-controlled. ClaimRevisionRef is the exact assertion target. Evidence role is target-specific; copied excerpts or repeated ingestion of the same source do not automatically count as independent corroboration.

Provenance identifies the derivation process, not truth. It records source/version refs, locators, input digests, derivation kind, method/model/rule version, ActorRef, time, Scope and parent provenance refs. Incomplete lineage must be explicitly marked; it is never fabricated.

### 4.4 ConflictSet

**Candidate pending D approval:** ConflictSet groups two or more incompatible ClaimRevisionRefs, not whole mutable Claim identities. It records conflict dimensions, Scope/environment comparison domain, overlapping valid interval, supporting/refuting evidence refs, common ancestry, status and append-only resolution history.

- Disjoint valid intervals or incompatible environments are not contradictory claims.
- Similarity clusters and duplicate candidates are not ConflictSets.
- ConflictSet membership changes must be historically visible.
- Resolution may retain both, select a successor, retract, narrow validity, mark disputed or declare no conflict; the resolution is a proposal until D commits under its authority.
- A Fact/FactRevision under Option A may record an adjudication outcome but does not delete the conflicting ClaimRevision participants.

## 5. Consumer contract

### 5.1 D — Canonical Memory / Lifecycle / Entity authority

D consumes proposals, not compiler-issued canonical identities.

D MUST:
- allocate and own canonical IDs for Memory, Claim, ClaimRevision, Evidence and ConflictSet objects as approved;
- validate typed reference existence, Scope compatibility, Evidence and Provenance completeness, parent revision and expected canonical version;
- commit immutable revisions and MemoryVersion references under its own transaction/CAS/outbox design;
- preserve exact ClaimRevision and ConflictSet history; never silently overwrite;
- own canonical ConflictSet lifecycle/commit decisions and Memory lifecycle transitions;
- expose canonical current/exact/as-of reads with explicit unavailable/forgotten outcomes.

B defines semantic meaning; D chooses physical storage and commit mechanics. Neither E nor F/G may bypass D to mint canonical identities.

### 5.2 E — Compiler

E MUST:
- keep CandidateProposition/ExtractionIR neutral until ADR approval;
- map proposals under the approved branch only and preserve exact source spans, modality, uncertainty, Evidence and Provenance;
- submit expected parent/version, idempotency, Scope, ActorRef and method/policy refs;
- emit revision/conflict/fact-attestation proposals, not canonical decisions;
- query D after unknown commit outcomes; never infer commit from timeout;
- stop/reconcile work under Forget fence and current authorization.

### 5.3 F — Runtime retrieval and activation

F MUST:
- consume D's canonical ClaimRef/ClaimRevisionRef and ConflictSet refs only after approval;
- index immutable revision identity separately from mutable/current projections;
- preserve competing revisions and ConflictSet status; never adjudicate truth or turn high confidence into Verified;
- retrieve exact revisions and report freshness/watermark/completeness; revalidate canonical currentness and Forget suppression before emission;
- return RetrievalResult/ActivationRecommendation, not ContextEntry or ContextVersion;
- apply Scope/authorization filters before candidate generation and Evidence dereference, with I's policy authority.

A ClaimRef alone is insufficient when exact content, historical state, conflict membership, evidence or as-of semantics matter; use ClaimRevisionRef.

### 5.4 G — Memory Context Manager

G MUST:
- pin D-issued MemoryVersionRef in every canonical Memory Context entry;
- when Claim details are directly represented, retain exact ClaimRevisionRef (and FactRevisionRef only if Option A approved), not a floating ClaimRef;
- preserve epistemic status, validity interval, conflict marker and source/provenance refs in the rendered/expandable context representation where applicable;
- treat ConflictSet as a signal for qualification or competing views, not a command to choose a winner;
- own ContextEntry membership, ordering, budget and ContextVersion; it does not own Claim identity, Claim revision, ConflictSet adjudication or canonical lifecycle;
- revalidate current Scope/Permission and Forget/revocation state before materialization/delivery under I/H boundaries.

G does not write or revise Canonical Memory. Context removal is not Claim retraction or Forget.

### 5.5 H / I boundaries

- H serializes approved typed refs and status fields; H owns wire format, compatibility and transport. This document does not define wire field names as frozen.
- I owns authentication/authorization policy, grants, revocation, retention and Forget completion. ScopeRef is not a grant; ActorRef is not proof of current permission.
- Evidence dereference may require stricter authorization than Memory/Claim metadata access.

## 6. Failure, retry and temporal behavior

- Unknown or incompatible ref type: reject as typed validation error; never reinterpret as another object type.
- Missing exact revision: return not-found/not-visible or history-unavailable according to I's disclosure and retention rules.
- Stale expected parent: reject with stale-version semantics; caller reloads and reconciles; no last-write-wins.
- Same idempotency key/same payload: return original result; same key/different payload: deterministic conflict.
- Evidence unavailable/restricted/forgotten: preserve reference and availability state; do not fabricate excerpt or substitute a new source.
- Conflict detector incomplete or timed out: retain candidate/defer; do not claim no conflict.
- Temporal uncertainty: preserve original expression, precision and bounds; unknown is not timeless.
- Forget/revocation: suppress reads and queued work according to D/E/F/G/I boundaries; no replay may resurrect forgotten derivatives.

## 7. Conformance scenarios

1. Same proposition from two sources creates two Evidence links, not two independent truths by default.
2. Same Claim corrected later creates a new ClaimRevisionRef; the old revision remains unchanged.
3. A retraction appends a new revision/event and does not erase the previous assertion/evidence.
4. Two incompatible claims with overlapping validity and compatible Scope create a ConflictSet proposal.
5. Same predicate with disjoint validity intervals is temporal succession/coexistence, not contradiction.
6. Same wording in different Environment Scopes is not merged into one Claim or ConflictSet.
7. High extraction confidence without verification evidence never creates Verified or a Fact.
8. A Fact proposal under Option A must point to exact ClaimRevisionRef(s), attestor, method and evidence; absent any, defer.
9. F returns stale/incomplete when its index watermark lags canonical commit or Forget fence.
10. G pins exact MemoryVersionRef and exact ClaimRevisionRef where claim detail is rendered.
11. A Context Remove does not change ClaimRevision or ConflictSet state.
12. Evidence read denied while Claim metadata read allowed does not leak evidence content.
13. Unknown time remains explicit and does not create false overlap/conflict.
14. Duplicate retry does not create a second ClaimRevision or ConflictSet revision.
15. Late replay after Forget suppression cannot re-expose a Claim/Evidence/Fact derivative.

## 8. Decision/change log

| Item | State | Owner | Note |
|---|---|---|---|
| CandidateProposition remains pre-canonical | DECIDED for current integration | E | Retain neutral IR until ADR approval |
| Stable ClaimRef + immutable ClaimRevisionRef | CANDIDATE | B proposes; D confirms canonical authority | Not frozen |
| ConflictSet groups exact ClaimRevisionRefs | CANDIDATE | B semantics; D canonical lifecycle/commit | Not frozen |
| Fact separate attestation object | ADR-BLOCKED | B + Architecture Governance | Preferred candidate Option A only |
| Confidence/epistemic/validity/lifecycle separation | DECIDED semantic principle | B | Exact enums/method vocabularies remain versioned |
| F/G consumer mapping | CANDIDATE | B proposes; F/G confirm | No schema freeze |

## 9. Source baseline and provenance

| Source | Branch/ref | Commit SHA | Blob SHA |
|---|---|---|---|
| Phase 3 task pack | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `7abe73e5209ee985c9807b95d99616069911a6b7` |
| Phase 2 reconciliation | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7` |
| D canonical store | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `4e4db0ed8847d060d235a1dedb394dfd4bda317d` |
| D memory versioning | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `c32e58f7a845a9b075e68eb1c93f63649996d580` |
| E extraction/normalization | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `438f0c795fbcf8ed2c5e05615f1b96aa448efe85` |
| E consolidation/conflict | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `bac3123d02e726ecffd8eb73ada515dea566e7e6` |
| E evidence/provenance | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `e001be08b2ea4329f12f44a12edda200fb62b1ec` |

D/E content above is sourced from their exact unmerged branches, not main.
