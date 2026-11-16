# ADR-001 — Canonical Fact / Claim Model

- **Status: ADR-BLOCKED**
- **Decision domain:** Fact/Claim domain semantics and canonical identity
- **Accountable decision owners:** Memory Domain Model (B) + Architecture Governance
- **Consulted owners:** D (Canonical Memory), E (Memory Compiler), F (Memory Runtime), G (Memory Context)
- **Related issues:** INT-P0-01, INT-P1-02, DM-001, DM-003, DM-004, DM-006
- **Prepared on:** 2026-11-16
- **Branch:** `session-b-domain-model-phase3`
- **Base:** `main@8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2`

## 1. Decision statement

**ADR-BLOCKED — no canonical Fact/Claim model is approved by this ADR.**

This document compares viable domain models and records a preferred candidate. It does not authorize schema, DDL, API, or wire-contract freeze. Phase 2 and the Phase 3 task pack assign this decision jointly to B and Architecture Governance. The inspected governance baseline contains normative statements that conflict with the current B model, and no Architecture Governance approval or named individual decision-maker is recorded in the inspected sources. B can recommend domain semantics but cannot unilaterally amend `00-governance/*`.

Until the blocking authority provides an explicit decision:
- E MUST retain neutral CandidateProposition / ExtractionIR and MUST NOT assign canonical Fact or Claim identity.
- D MUST retain its neutral proposition envelope and MUST NOT freeze Fact/Claim persistence identities or schema.
- F and G MAY consume candidate-neutral references and existing immutable MemoryVersion references, but MUST NOT assume a Fact/Claim identity model.
- H MUST NOT publish Fact/Claim wire fields as normative.
- No module may treat this candidate recommendation as approval.

## 2. Decision context and baseline conflict

The inspected sources establish:

1. `00-governance/architecture-invariants.md`, I-04: Event, Memory, Fact, Entity, Relation, and Evidence are distinct domain concepts.
2. `00-governance/design-principles.md`, P-04: Event, Memory, Fact, Entity, Relation, and Evidence are different objects; a source event may support a memory claim.
3. `00-governance/terminology.md`: “Fact / Claim” is currently defined together as a proposition with epistemic and temporal qualifications, leaving the object distinction unresolved.
4. `02-domain-model/domain-model-overview.md`, §5: Claim is the canonical proposition object and Fact is a qualified interpretation of Claim, not a separate object type.
5. `02-domain-model/core-entities.md`, §5: Claim is modeled as a proposition with epistemic status, evidence refs, confidence, validity, scope and retraction metadata; Claim identity across versions remains OPEN.
6. D's Canonical Memory Store explicitly marks Claim and Fact persistence **ADR-BLOCKED**. D's candidate versioning model recommends stable Claim identity plus immutable ClaimRevision, but explicitly defers to this ADR.
7. E's ExtractionIR/CandidateProposition is deliberately pre-canonical and neutral. E's consolidation layer proposes revision/conflict proposals but assigns final identity and ConflictSet shape to D after this ADR.

The contradiction is semantic, not merely naming: whether a Fact has its own identity and lifecycle changes evidence attachment, revision history, conflict membership, references, and consumer behavior.

## 3. Alternatives considered

### Option A — Fact and Claim are distinct canonical domain objects

**Definition**

- **Claim** is an attributable proposition asserted, observed, reported, inferred, questioned, disputed, corrected or withdrawn by an actor/source/process. It captures what is being claimed, by whom/what, with what epistemic basis, scope and asserted validity.
- **Fact** is a separately identified, evidence-backed canonical attestation/accepted proposition produced by an explicit verification or adjudication process. “Fact” does not mean metaphysical certainty or objective infallibility. It means the Brain has recorded a governed fact-level determination under a named method/authority and evidence set.
- A Fact MUST reference the exact ClaimRevision(s) it affirms, qualifies, narrows, or supersedes, and its supporting/refuting Evidence and Provenance. A Fact is not a copy of a raw source statement.
- A Claim may exist without a Fact. A Fact requires a traceable attestation basis and an explicit verification method/authority. Confidence alone cannot create a Fact.
- Fact and Claim have separate stable identities and immutable revision histories. A Fact revision records the precise ClaimRevision refs and evidence/method basis used at that time.

**Identity and revision**

- Claim identity denotes a proposition thread within the Brain authority namespace and applicable scope; ClaimRevision denotes one immutable assertion state.
- Fact identity denotes a fact-attestation thread; FactRevision denotes one immutable attestation result and its exact supporting ClaimRevision/Evidence/Provenance set.
- A correction to a Claim creates a new ClaimRevision. A change to the fact-level determination creates a new FactRevision, not an in-place edit. A Fact may be withdrawn/revoked by a later FactRevision or explicit append-only attestation event; prior history remains addressable subject to Forget policy.
- Claim and Fact are related by typed, directional, version-pinned links such as `attests_to`, `affirms`, `qualifies`, `contradicts`, or `supersedes`. The controlled vocabulary and exact link ownership require D/B alignment.

**Assessment**

- Preserves I-04/P-04 as written and gives a real semantic distinction.
- Strong auditability: a source assertion is not confused with a Brain verification outcome.
- Supports multiple Claims feeding one Fact, one Claim being rejected/qualified, and a Fact being revised when new evidence arrives.
- Adds object/revision/link complexity and requires explicit attestation authority and verification policy. That authority/policy cannot be invented by B; it requires governance and I coordination.
- Requires D to persist the canonical identities and immutable revision references after approval.

### Option B — Claim is the only canonical proposition object; Fact is a qualification/view of Claim

**Definition**

- Claim is the sole canonical proposition identity and immutable revision stream.
- “Fact” is a derived label/view for a Claim revision meeting an explicit epistemic qualification, for example Verified under a named method and evidence threshold.
- No independent Fact ID, FactRevision, or Fact lifecycle exists. Any “fact” reference resolves to a ClaimRevision plus its qualification metadata.

**Identity and revision**

- Claim identity denotes a stable proposition thread; ClaimRevision denotes an immutable exact assertion/epistemic state.
- A ClaimRevision may be described as fact-qualified only when the required verification method, authority, evidence and scope conditions are satisfied.
- Re-verification or correction appends a new ClaimRevision. Historical views resolve to the old revision and its old evidence/method basis.
- Evidence attaches to exact ClaimRevision(s), with target-specific support/refutation/qualification roles. A view does not own independent evidence links.

**Assessment**

- Smaller canonical object graph and simpler reference model.
- Avoids duplicate proposition records and keeps query/revision logic centralized.
- Makes it harder to represent an independently governed fact attestation with its own identity, provenance, lifecycle, and consumers.
- Does not satisfy the literal “Fact and Claim are distinct domain concepts” language in I-04/P-04 unless Architecture Governance explicitly redefines those invariants and terminology.
- The current B overview is closest to this option, but its current text does not resolve Claim identity/revision or ConflictSet gaps.

## 4. Comparative evaluation

| Dimension | Option A: separate Fact + Claim | Option B: Claim with fact qualification |
|---|---|---|
| Identity stability | Separate stable Fact and Claim identities; revisions pin exact cross-links | One stable Claim identity; fact label is revision-local |
| Versioning | Independent immutable ClaimRevision and FactRevision streams | One immutable ClaimRevision stream |
| Evidence attachment | Claim evidence attaches to exact ClaimRevision; Fact attestation references exact ClaimRevision and evidence set | Evidence attaches to exact ClaimRevision; fact qualification references same evidence |
| Provenance | Separate lineage for assertion and verification/attestation | One lineage with verification derivation metadata |
| Conflicts | ConflictSet can include ClaimRevision participants and FactRevision adjudication outcomes | ConflictSet includes ClaimRevision participants; “fact” is a qualification |
| Retraction | Claim withdrawal and Fact attestation withdrawal are distinct events/revisions | Append a ClaimRevision with Retracted or changed epistemic status; fact view changes accordingly |
| Correction | New ClaimRevision; FactRevision remains historically tied to old ClaimRevision until re-attested | New ClaimRevision; fact qualification recalculated/appended |
| Validity time | Claim valid interval and Fact attestation's asserted/effective interval are separate, explicit values | ClaimRevision valid interval; fact view inherits it |
| Historical traceability | Strong separation of source assertion from adjudicated fact result; more joins | Simpler history but less explicit separation of assertion and adjudication |
| Complexity | Higher object, reference, policy and query complexity | Lower object count and simpler consumers |
| Governance fit | Preserves current I-04/P-04 literal distinction | Requires explicit governance amendment/reinterpretation |

## 5. Preferred candidate (NOT APPROVED)

**B's preferred candidate is Option A, distinct Fact and Claim objects, subject to Architecture Governance approval and a concrete attestation authority contract.**

Rationale:
1. It preserves the explicit distinction already mandated by I-04 and P-04 instead of silently weakening a normative invariant.
2. It prevents source assertions, model inferences and user reports from becoming “facts” merely because they have high confidence or a Verified-looking enum.
3. It makes the verification/adjudication act independently auditable and revision-addressable.
4. It allows a fact-level determination to cite exact ClaimRevision inputs and evidence, without rewriting the underlying assertions.

This recommendation is not a decision. The Fact definition must not imply certainty, and the attestation authority, acceptable methods, evidence sufficiency, and revocation semantics must be approved by the relevant governance owners. If Architecture Governance chooses Option B, it must explicitly amend the conflicting governance baseline before downstream schema freeze.

## 6. Cross-cutting canonical semantics

### 6.1 Claim identity and ClaimRevision

Candidate model, pending ADR approval:

- `ClaimRef` identifies a stable Claim thread.
- `ClaimRevisionRef` identifies one immutable revision within that Claim.
- Claim identity is not derived from proposition text, embedding, display label, or normalized sentence hash. Semantic similarity is candidate generation only.
- A Claim identity is scoped to one Brain authority namespace; ownership/applicability Scope is explicit metadata and a reference constraint, not a substitute for identity.
- ClaimRevision contains the exact proposition payload, subject/predicate/object, polarity, qualifiers, epistemic status, valid interval, evidence links, provenance refs, Scope refs, author/actor, recorded time, method refs, parent revision and content digest.
- One revision is genesis; every later committed revision has one parent. Competing proposals do not create multiple canonical heads. CAS/reconciliation is D's persistence responsibility.
- A correction/refinement/retraction creates a new immutable revision. Prior revisions remain immutable and historically addressable subject to governed Forget restrictions.

### 6.2 Evidence and Provenance

- **Evidence** is source material/observation or a typed source locator, not a score and not a proposition.
- Evidence has stable identity under a declared source/version + locator + digest + Scope + kind identity policy. It can support, refute, qualify, or be context-only for an exact ClaimRevision or FactRevision.
- Evidence links are target-specific and independently addressable when role/strength/actor/scope/time has its own semantics.
- **Provenance** records how a ClaimRevision or FactRevision was produced: derivation kind, method/model/rule version, input digest refs, parent provenance refs, actor, time and Scope.
- Evidence identity and Provenance identity are distinct. One Evidence can support multiple revisions; one revision can have multiple Evidence links. A method reference describes process and does not prove correctness.
- Source availability, authorization, retention and Forget are independent from the existence of a historical reference. An unavailable/forgotten source must not be fabricated or silently substituted.

### 6.3 ConflictSet

Candidate canonical semantics, subject to D's canonical persistence shape:

- ConflictSet is a durable domain concept grouping two or more incompatible exact ClaimRevisionRefs within a compatible comparison domain.
- It is not a boolean flag on one Claim, not a similarity cluster, and not a replacement for the participating claims.
- ConflictSet identity denotes a continuing conflict thread; each membership/status/resolution change is an immutable ConflictSetRevision or append-only resolution event.
- Membership records exact ClaimRevisionRef, stance/role, relevant dimensions and Scope. The set records conflict dimensions, relevant valid-time intersection (if any), evidence refs, common ancestry refs, opened/updated times, and status: unresolved, review_required, resolved, accepted_coexistence.
- A conflict requires semantic incompatibility over an overlapping valid-time interval in a compatible Scope/environment and modality. Non-overlapping validity, incompatible environment scopes, distinct modality (e.g. plan vs outcome), or mere paraphrase are not conflicts.
- Resolution never deletes participant revisions or source evidence. It records an authorized outcome such as retain_both, select_successor, retract, narrow_validity, mark_disputed, or no_conflict, with actor, reason, method, evidence, time and references to prior set revision.
- ConflictSet does not adjudicate truth itself. It preserves the disagreement and resolution history.

### 6.4 Orthogonal dimensions (never one overloaded status)

| Dimension | Question answered | Candidate values / semantics |
|---|---|---|
| Confidence | How strongly does a declared method estimate support? | Optional method-qualified score with scale, calibration/population, method/version, assessed_at; not truth and not permission |
| Epistemic status | What is the asserted basis/standing of this ClaimRevision? | observed, reported, inferred, verified, disputed, retracted; exact vocabulary governed/versioned |
| Validity interval | During what real-world interval is the proposition asserted to hold? | TimeInterval; unknown is explicit and is not unbounded or timeless |
| Lifecycle | What management stage is the canonical asset in? | Memory lifecycle is D-owned; Fact/Claim lifecycle, if any, must be separately named and approved; never reuse epistemic status as lifecycle |
| Relevance | How useful is it for a task now? | F-owned/task-time-dependent retrieval or activation signal, not truth |
| Source trust | How trustworthy is the source/producer? | Separate source/principal/process assessment; not evidence strength or confidence |

Confidence cannot promote a Claim to Verified or create a Fact. Verified requires a declared verification method and qualifying Evidence/attestation; the exact authority and criteria remain OPEN pending governance.

### 6.5 Retraction, correction and temporal history

- Retraction is a new revision or append-only status event that withdraws a prior assertion from current endorsement; it does not erase the old revision or source.
- Correction creates a new revision with explicit relation to the corrected revision and a reason. It may correct content, entity resolution, temporal interval, epistemic basis or scope; it does not silently rewrite historical valid time.
- Supersession is an explicit relation between revisions/claims and is not equivalent to deletion.
- Valid Time describes when the proposition is asserted to hold. Recorded/transaction time describes when the Brain knew/committed it. Event Time describes when the source occurrence happened. They are not interchangeable.
- “Valid at T, known by T2” must return the exact ClaimRevisionRef (and, if Option A is approved, the exact FactRevisionRef) that was authoritative under that temporal query.

## 7. Required approval and remaining questions

### Decision authority required

1. **Architecture Governance decision owner:** must be identified by the project governance process; no named individual or explicit approval record was present in the inspected baseline. This owner must decide whether I-04/P-04 are preserved with Option A or formally amended for Option B.
2. **B Domain Model Principal Architect:** provides domain recommendation and updates B-owned semantics after the joint decision.
3. **D Memory Brain Principal Architect:** confirms canonical identity/revision/ConflictSet storage contract after ADR; D does not decide the Fact/Claim semantic choice.
4. **E/F/G owners:** confirm mappings and consumer semantics; they are not approval authorities for this ADR.
5. **I Security/Governance owner:** consulted for attestation authority, identity/scope and revocation/Forget constraints; I owns authorization policy, not Fact/Claim semantics.

### Questions that must be answered to unblock

- Is Fact a separately identified canonical attestation object (Option A), or a derived qualification/view of ClaimRevision (Option B)?
- Who/what is an authorized attestor, and which method/authority can create or withdraw a Fact-level attestation?
- What minimum Evidence and provenance are mandatory for Verified/Fact qualification, and what remains merely candidate or reported?
- Does a Fact-level attestation have its own validity interval distinct from the Claim's asserted valid interval?
- What is the approved correction/revocation relation between a FactRevision and the ClaimRevision(s) it references?
- Which governance owner approves any amendment to I-04, P-04 and the terminology/README baseline?
- Does D accept the candidate stable ClaimRef + immutable ClaimRevisionRef + ConflictSet thread model after the ADR is approved?

## 8. Consequences while blocked

- No canonical Fact/Claim schema, storage layout, DDL, API or wire field is frozen.
- D's stable Claim identity + immutable ClaimRevision remains a candidate only.
- ConflictSet semantics in this ADR are candidate domain semantics; D owns canonical persistence shape and lifecycle/commit mechanics.
- E continues producing neutral CandidateProposition/ExtractionIR and proposals only.
- F may preserve candidate proposition/revision references internally but may not mint canonical Claim identity or infer fact status.
- G pins exact MemoryVersionRef as its canonical memory dependency; any exposed Claim references must be exact and version-pinned, without G owning Claim or Context mutation beyond its own Context authority.
- Any cross-module test must label Fact/Claim mapping as blocked until governance approval.

## 9. Source baseline and provenance

All source refs below identify the branch/ref actually inspected. No unmerged D/E branch content is represented as main.

| Source | Branch/ref | Commit SHA | Blob SHA | Use |
|---|---|---|---|---|
| `00-governance/architecture-invariants.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `66266667bdbb1cf15a2644fa98db5ecaaf3bb23b` | I-04, I-05, I-14, I-15 |
| `00-governance/design-principles.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `192e6ba6e9287792a02b679dda0d391844270228` | P-04, P-05, P-06, P-14 |
| `00-governance/terminology.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `9b287ebe027ae01128baf164952ce15aad050638` | Fact/Claim and epistemic/lifecycle definitions |
| `02-domain-model/core-entities.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `8cb5a674eec8eac1f3c4d83c400dc08d00166f23` | Existing Claim, Evidence, Provenance fields |
| `02-domain-model/domain-model-overview.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `4d1debc0ec19b3917f9e76d04bb66da4df4cd346` | Current Fact/Claim conflation |
| `02-domain-model/epistemic-and-temporal-semantics.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `8c03a20db1ed54c90db1d5c4c64f5ea7b1324ed7` | Epistemic/time axes |
| `02-domain-model/lifecycle-model.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `81c48c928cb5f9c76ca29d493fbd9479079e62f7` | Lifecycle separation |
| `02-domain-model/relationships-and-provenance.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `e762f84c59f69de7a44baad2123aed46e1ffea16` | Evidence and provenance semantics |
| `02-domain-model/scope-and-permission-model.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `b5215ae27bd65a6c89c185b496f730b6cd52efa9` | Scope baseline |
| `reviews/integration/phase-2-defg-cross-session-reconciliation.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7` | Joint ADR ownership and blockers |
| `reviews/integration/phase-3-cross-module-remediation-task-pack.md` | `main` | `8e57f38e1f81a26280f0d56d6a40d6b98c5c6ac2` | `7abe73e5209ee985c9807b95d99616069911a6b7` | B workstream and outputs |
| `03-memory-brain/canonical-memory-store.md` | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `4e4db0ed8847d060d235a1dedb394dfd4bda317d` | D canonical authority and ADR block |
| `03-memory-brain/memory-lifecycle-manager.md` | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `6eeeb862fa9a65587877951630e03860f105c186` | Lifecycle and candidate ConflictSet |
| `03-memory-brain/memory-versioning.md` | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `c32e58f7a845a9b075e68eb1c93f63649996d580` | ClaimRevision candidate and history |
| `03-memory-brain/entity-and-relationship-manager.md` | `session-d-memory-brain-2026-11-16` | `9dc08c63f6912320e290a963c634748ec44a81c8` | `5688ef4fa682bc3e81aad5a9939e19ffc41ddf57` | Typed refs and relation semantics |
| `04-memory-compiler/extraction-and-normalization.md` | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `438f0c795fbcf8ed2c5e05615f1b96aa448efe85` | Neutral CandidateProposition/IR |
| `04-memory-compiler/consolidation-and-conflict-resolution.md` | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `bac3123d02e726ecffd8eb73ada515dea566e7e6` | Revision and ConflictSet proposals |
| `04-memory-compiler/evidence-and-provenance.md` | `session-e-memory-compiler-2026-11-16` | `54df136d1e410af834461950e3c61c5c80abd6ad` | `e001be08b2ea4329f12f44a12edda200fb62b1ec` | Evidence and lineage |

**Branch-awareness note:** D and E files above were fetched from their own branches at the commit SHAs shown, not from main. The main tree did not contain these subsystem documents at the inspected baseline.

## 10. Review and approval checklist

- [ ] Architecture Governance names the decision owner/approver.
- [ ] Architecture Governance explicitly chooses Option A or Option B.
- [ ] If Option B, governance updates I-04/P-04 and terminology/README through its authorized change process.
- [ ] B updates its domain model to match the approved choice.
- [ ] D confirms Claim identity/revision and canonical ConflictSet shape.
- [ ] E confirms IR mapping.
- [ ] F confirms retrieval/index consumer semantics.
- [ ] G confirms Context consumer semantics.
- [ ] Cross-module conformance tests cover revisions, evidence, conflict, correction, retraction, temporal as-of and scope isolation.

**No approval is inferred from review, silence, merge, or downstream implementation.**
