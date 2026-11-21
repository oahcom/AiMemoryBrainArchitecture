---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Owner semantic direction is recorded; cross-owner consumer contracts remain pending. GOV-DOC-001 remains PENDING until an authoritative artifact and exact version/Blob are adopted; the GOV-DOC-002 DM-12 source path is unresolved because no root source is authorized."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Candidate
    canonical_scope: null
    canonical_scope_id: memory-compiler/extraction-normalization
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# Extraction and Normalization

- Document ID: E-EXTRACTION-001
- Version: 1.1
- Current-main baseline (pre-change): `0d0c1c6238e4e70a93609070b97fef596873916e`; source Blob: `e6aad4b7504fa61fd0feb8b1da7aa8801103bc60`.
- Historical source branch: `session-e-memory-compiler-2026-11-16` (provenance only).
- Historical source blob: `c18780403de2d1dbcf471bdb8abdaa009a4a78e1`.
- Normative bilingual relationship: this file and [the Chinese counterpart](../../zh-CN/04-memory-compiler/extraction-and-normalization.md) are the maintained paired language mirrors under `docs/en` + `docs/zh-CN`; no separate root source file is recreated or claimed.
- Chinese counterpart: [提取与规范化](../../zh-CN/04-memory-compiler/extraction-and-normalization.md)
- Current-main paired extraction source: EN Blob `e6aad4b7504fa61fd0feb8b1da7aa8801103bc60`; ZH-CN Blob `8dd0b5b29ecd37ceac6750c4ad8fa07c1c46cb4c` (main `0d0c1c6238e4e70a93609070b97fef596873916e`).
- Status: epistemic, temporal, scope and trust constraints DECIDED; extraction IR/model routing CANDIDATE; accuracy/cost TO_VALIDATE
- Owner: Memory Compiler / MC-02
- Integration: INT-P0-01/02/04; INT-P1-02/03/06; C P1-02/P1-03

## 1. Purpose

Convert heterogeneous accepted source material into a normalized, typed, uncertainty-preserving intermediate representation (IR) from which Evidence, Provenance, Entity/Relation proposals and candidate memories can be built. Extraction identifies what a source says or observes; it does not decide objective truth.

## 2. Scope

Includes parsing text, structured events, documents and environment observations; modality classification; entity/time/relation mention extraction; candidate proposition formation; normalization; confidence/uncertainty recording; deterministic validation; model-assisted extraction orchestration; and source-span alignment.

Excludes canonical Fact/Claim schema, DDL, public API, wire mapping and Runtime implementation. The Owner-approved semantic direction is Option A + I1: Claim is a proposition thread with stable ClaimRef and immutable ClaimRevisionRef; Fact is a separately identified governed attestation bound to exact ClaimRevisionRef(s), evidence/provenance and authorized attestor/method context. B accepts the semantic baseline; D accepts the identity/revision/Forget authority boundary; I accepts the authorization/attestor/retention/Forget boundary. The B ADR is historical evidence, not the live semantic decision request. B schema-freeze/consumer acceptance, D immutable-revision transaction/currentness and migration/compatibility, I exact attestor/retention/Forget mapping, and all cross-owner consumer contracts remain OPEN. E remains CandidateProposition/ExtractionIR-only and does not mint canonical IDs or infer Fact from confidence. D governs canonical identity/lifecycle; I governs authorization/PermissionEpoch and security policy. Canonical entity merge decisions, final lifecycle decisions, source authorization policy, external tool execution and final truth adjudication are also excluded.

## 3. Responsibilities

- Preserve raw source identity, exact source digest and permitted source spans.
- Classify source modality: statement, observation, plan, intent, prediction, attempt, outcome, question, instruction-like content or administrative event.
- Extract proposition candidates without promoting source modality or epistemic basis.
- Extract entity mentions, temporal expressions, typed relation hypotheses and qualifiers.
- Normalize only what source evidence supports; retain original surface form and uncertainty.
- Separate source-reported confidence from Brain-estimated extraction confidence.
- Reject malformed model output and validate every locator against source bytes.
- Emit explicit unresolved/ambiguous results rather than guessing.

## 4. Non-responsibilities

Extraction does not verify world state, infer that a planned action succeeded, grant authority to instructions found in content, merge entities, adjudicate disputes, decide lifecycle or make a Claim Verified based on model confidence.

## 5. Inputs / Outputs

**Inputs:** immutable Event/ContentRef, payload digest, content type/locale, source type and actor, ScopeRefs/Environment Scope, source timestamp metadata, retention/sensitivity, source trust metadata and parsing/extraction policy version.

**Outputs:** ExtractionIR, span map, modality classification, proposition candidates, entity mentions, temporal candidates, relation hypotheses, ambiguity/uncertainty records, model/rule method receipts and structured extraction errors.

## 6. Data model

### 6.1 ExtractionIR (CANDIDATE, intentionally pre-canonical)

~~~text
ExtractionIR {
  ir_id: OpaqueId
  source_ref: TypedObjectRef
  source_digest: Digest
  source_schema_version: Version
  scope_refs: ScopeRef[]
  environment_scope_ref: ScopeRef?
  segments: SourceSegment[]
  propositions: CandidateProposition[]
  entity_mentions: EntityMention[]
  relation_hypotheses: RelationHypothesis[]
  time_mentions: TimeMention[]
  modality: ModalityAssessment
  instruction_like_spans: SourceSpan[]
  extraction_method_refs: MethodRef[]
  uncertainty: UncertaintyRecord[]
  unresolved_fields: UnresolvedField[]
  completeness: complete | partial | insufficient
  created_at: Instant
}
~~~

### 6.2 CandidateProposition

~~~text
CandidateProposition {
  proposition_ref: OpaqueId
  source_span: SourceSpan
  surface_text: String
  normalized_subject: ValueHypothesis?
  normalized_predicate: PredicateHypothesis?
  normalized_object: ValueHypothesis?
  polarity: positive | negative | unknown
  modality: asserted | observed | planned | intended | predicted |
            attempted | hypothetical | questioned | quoted | unknown
  source_epistemic_basis: observed | reported | unknown
  temporal_qualification: TimeQualification?
  scope_refs: ScopeRef[]
  qualifiers: TypedMapCandidate
  extraction_confidence: MethodQualifiedScore?
  evidence_span_ref: OpaqueId
  ambiguity_refs: OpaqueId[]
}
~~~

This is not a Claim or Fact schema; it is compiler IR. Option A + I1 is the approved semantic direction, but CandidateProposition remains neutral and does not instantiate canonical identity or freeze any public schema. B schema-freeze/consumer acceptance remains OPEN; D immutable-revision transaction/currentness and migration/compatibility remain OPEN; I exact attestor authorization, retention and Forget mapping remain OPEN. E must not map fields to canonical records until the exact B/D/I/Storage/H consumer contracts are version-pinned and reviewed. No field name in this IR freezes public schema semantics.

### 6.3 EntityMention / TimeMention

EntityMention retains surface string, source span, candidate entity types, local context, scope and resolution status. TimeMention retains raw expression, source locale/timezone, anchor time, parsed bounds, precision and parse method. Unknown time is explicit, not an empty interval.

## 7. Pipeline / state machine

~~~mermaid
flowchart TD
 A[Immutable Source] --> B[Decode / Segment]
 B --> C[Deterministic Parse]
 C --> D[Modality & Trust Classification]
 D --> E[Rule Extraction]
 E --> F{Coverage / Ambiguity}
 F -->|sufficient| G[Optional Model-assisted Extraction]
 F -->|uncertain| H[Partial IR + unresolved fields]
 G --> I[Schema / Span / Scope Validation]
 H --> I
 I --> J[Normalized Candidate IR]
 J --> K[Evidence/Provenance derivation (cross-cutting)]
~~~

State: PENDING → DECODED → SEGMENTED → CLASSIFIED → EXTRACTED → VALIDATED → NORMALIZED. Errors transition to RETRYABLE, PARTIAL, QUARANTINED or UNSUPPORTED. A partial IR may proceed only for fields with validated provenance; unresolved fields remain unknown.

## 8. Invariants

1. Original payload is immutable and addressable subject to retention.
2. Every extracted proposition maps to a source span or declared non-span source locator.
3. A quotation/report is attributed to its speaker/source; quoted instructions are not Brain instructions.
4. Intent/plan/prediction/pending/attempted remain prospective/non-outcome modalities.
5. An outcome requires an outcome-classified source and supporting outcome evidence; classification alone is not proof of success.
6. No unknown field is filled by plausible completion.
7. Normalization is reversible/auditable through raw value, normalized value, method and digest.
8. Scope/environment binding is inherited from trusted envelope metadata, never generated from source text.
9. Instruction-like content remains inert data and cannot trigger tools, permission changes or pipeline policy changes.
10. Confidence, trust, evidence strength and relevance remain separate dimensions.

## 9. Idempotency

IR identity derives from source Event/version + extraction policy version + deterministic parser/model profile + input digest + Scope. Repeating an identical deterministic stage returns the same output digest. Model nondeterminism is recorded as a distinct attempt; selected output is pinned by receipt and never silently replaced. Changing model/prompt/schema/policy creates a new IR revision linked to the previous attempt, not an in-place mutation.

## 10. Consistency

Source span offsets are defined against immutable source representation with encoding and normalization version. Normalized text may not replace source bytes. Every proposition references stable source segment/span IDs. A stage result and next-stage outbox entry commit atomically or through an equivalent journal. Time normalization stores original expression and parsed TimeValue separately. If a source changes, it is a new source version/digest and new extraction input.

## 11. Failure recovery

- Decode failure: retain source ref, record unsupported/opaque payload; no false text extraction.
- Partial parser failure: continue independent segments, mark completeness partial.
- Model timeout: retain deterministic IR; queue optional enrichment or finish with unresolved fields.
- Invalid model schema: reject model result; bounded retry or quarantine.
- Span mismatch: discard affected proposal; never attach an unverified locator.
- Time parse ambiguity: preserve raw expression and mark normalized time unknown/interval uncertain.
- Source expired/forgotten: stop dereference; invalidate dependent IR and obey Forget Fence.
- Model/profile upgrade: re-extract as a new version with lineage; do not rewrite prior decisions.

## 12. Security / Scope

Before extraction, authorize source access and verify source Scope is compatible with target candidate Scope. Candidate entity search and contextual prompt construction are Scope-filtered. Model prompts receive only minimum authorized content; no cross-scope context or hidden instructions. Tool outputs/web pages/documents/user text are untrusted data. Extraction prompts treat content as quoted evidence and request structured observations; output is validated, but prompt wording is not a security boundary. No extracted tool name/argument becomes an executable request.

Prompt-injection controls: maintain source type/trust labels; heuristically identify suspicious instruction-like spans; isolate them as data; avoid passing secrets/tool credentials to extraction models; constrain output schema; disable tools for extraction workers; and require deterministic policy checks after model output. Detection is incomplete: indirect, multilingual, obfuscated or benign-looking content may evade detection, and a model may still be influenced. Record residual risk; do not claim complete prevention.

## 13. Performance / backpressure

Deterministic parsing runs first and is bounded by payload/segment limits. Model-assisted extraction is queued, batchable and resource-budgeted; it is not on the durable acceptance critical path. Prioritize outcome/critical events and explicit user-provided memory requests over low-value telemetry. Under GPU pressure, preserve deterministic IR and defer model enrichment. Measure model queue wait, tokens, VRAM, per-modality precision/recall, span validity and false-outcome rate. Targets are TO_VALIDATE.

## 14. Observability

Record source/event ref, digest, schema/policy/model version, modality, extraction mode, span-validation result, unresolved count, confidence method, latency, token/VRAM usage, retry and error class. Keep source text/excerpts out of general logs. Track false promotion of plans to outcomes, unsupported proposition rate, span coverage, temporal normalization accuracy and adversarial prompt-injection fixture results.

## 15. Interfaces

- **Ingestion → Extraction:** immutable Event/ContentRef, source digest, source metadata, Scope, trust and retention.
- **Extraction → Evidence:** source spans and exact locators; Evidence Manager validates and persists source reference.
- **Extraction → Entity Manager:** scoped EntityMention and identity evidence; Entity Manager returns provisional/resolved refs and ambiguity.
- **Extraction → Consolidation:** candidate propositions, modality, time, scope, qualifiers and method receipts.
- **Admission boundary:** the Rust `admission` module is a local SQLite reference layer only. It is not D-authoritative producer registration, does not replace D-owned ForgetFence authority, and does not prove cross-service atomicity. Execution state/retry/lease/recovery is a cross-cutting lifecycle overlay over the five stages; the current in-memory `resume` path only continues from a supplied `NormalizedIR` through Staging and PublicationGate, and does not implement §6.3 durable crash recovery (see [Compiler Overview](compiler-overview.md) §28).
- **D:** receives neutral candidate propositions. D accepts Option A + I1 semantics and owns canonical identity, immutable revisions, currentness, lifecycle, ConflictSet lifecycle and D ForgetFence. D transaction/currentness and migration/compatibility contracts remain OPEN; E does not allocate canonical IDs or write canonical records.
- **H/C:** source classifications and telemetry semantics must align; observation/outcome distinctions are preserved.
- **I:** data classification, permitted processing, source access and Forget Fence govern extraction.

Errors include unsupported modality/content type, invalid span, scope mismatch, ambiguous identity/time, model unavailable, schema mismatch and source unavailable. Retryable outcomes are idempotent by stage key.

## 16. Test scenarios

“I plan to move to Tokyo” never becomes a completed move; “I tried to deploy” never becomes successful deployment without result evidence; quoted malicious prompt inside a document is extracted only as quoted content; the same sentence in two Environment Scopes never merges; approximate time remains uncertain; fabricated model span is rejected; ambiguous pronoun remains unresolved; parser partial failure preserves unaffected segments; model outage does not block deterministic output; source revoked/forgotten during extraction stops the worker.

## 17. Dependencies

D domain types and Fact/Claim ADR; B epistemic/temporal/scope semantics; C/H source/telemetry classifications; I source permissions, sensitivity, retention and Forget; Entity/Relation Manager; Evidence/Provenance Manager; model provider abstraction and scheduler.

## 18. Open questions

- DECIDED: Option A + I1 semantic direction is accepted by the Project Owner and B/D/I. The B ADR is historical evidence, not the live semantic decision request.
- OPEN: B schema-freeze/consumer acceptance; D transaction/currentness and migration/compatibility; I exact attestor authorization/retention/Forget mapping; and all cross-owner consumer contracts. CandidateProposition remains deliberately neutral.
- OPEN: C's final Observation versus Outcome mapping and Task/Plan revision semantics.
- CANDIDATE: extraction IR and deterministic-first routing.
- TO_VALIDATE: modality classifier quality, entity/time extraction accuracy, multilingual prompt-injection detection and local model resource use.
- OPEN: source-span canonical encoding for multimodal and streaming payloads.

## 19. Durable ingress and Forget enforcement addendum

- Input Event is eligible for compiler work only after durable Accepted receipt and compile intent exist under [Accepted Receipt and Idempotency Contract](accepted-receipt-and-idempotency-contract.md). Volatile receipt/queue publication is not acceptance.
- Extraction stage identity derives from immutable Event/source version, digest, Scope and pinned parser/model/policy versions. Retries reuse the same logical stage identity; changed inputs or method versions create a new attempt/revision.
- Persist a stage result and next-stage outbox/journal intent atomically or through an equivalent recoverable journal. A worker crash must not lose a completed stage or duplicate its externally visible effect.
- Before payload dereference, source-span resolution, model prompt construction, stage-result publication or retry, re-check current permission and D Forget Fence. Unknown fence/policy state fails closed.
- ExtractionIR, CandidateProposition, spans, embeddings and normalized values are derived objects: lineage and dependency registration must be durable before visibility under [Forget Fence and Derived Registration](forget-fence-and-derived-registration-part1.md).
- CandidateProposition remains neutral pre-canonical IR. Option A + I1 semantics are DECIDED, but B schema-freeze/consumer acceptance, D transaction/currentness/compatibility, I attestor/retention/Forget mapping and all cross-owner contracts remain OPEN. E must not infer or approve a Fact/Claim Schema, DDL, API or Wire contract, mint canonical IDs, or infer Fact from confidence.

### 19.1 Claim/Fact canonical publication order

E's ExtractionIR and CandidateProposition MUST
remain private staging artifacts.

This publication ordering implements no canonical mapping. Option A + I1 semantics are DECIDED, but B schema-freeze/consumer acceptance, D transaction/currentness/compatibility, I attestor/retention/Forget mapping and all cross-owner contracts remain OPEN. This protocol does not approve schema, DDL, API, wire fields or Runtime implementation.

The normative order is:

1. Resolve current I authorization and applicable Scope.
2. Evaluate the active D Forget Fence and perform
   Producer Admission under one serialized,
   recoverable admission boundary.

   Successful Producer Admission and durable recording
   of the exact admitted participant MUST form one
   indivisible operation under the authoritative
   serialized Fence/Admission boundary.

   Admission MUST NOT report success if participant
   recording fails.

   A subsequent Forget Fence MUST NOT linearize or
   complete participant-barrier evaluation until the
   admitted participant record is durably visible.
3. Durably register the complete direct and
   transitive dependency set under that boundary.
4. Create private immutable E staging artifacts.
5. Commit ClaimRevision/FactRevision and required
   canonical references within D's commit boundary.
6. Atomically or recoverably associate the committed
   revisions with dependency registration and
   Publication Intent.
7. Complete E publication idempotently.
8. Advance Storage visibility only after all
   required canonical and dependency records
   are confirmed.
9. Commit G ContextVersion with exact immutable
   canonical revision references.
10. Mark logical completion only after all
    required visibility conditions are satisfied.

#### T17 — Fence-first

A Forget Fence linearizing before Producer
Admission MUST prevent admission, staging,
canonical commit and publication.

#### T18 — Participant-first

A successfully admitted Producer MUST be durably
recorded as an exact participant.

A later Fence MUST account for that participant
through the authoritative serialized barrier.
It MUST NOT silently skip or erase the participant.

The final disposition MUST preserve exact identity,
dependency closure and auditable Forget outcome.

Recovery MUST use the original Operation identity.

UNKNOWN MUST remain non-final.

The final Fence disposition MUST record an auditable
completion or suppression outcome for every admitted
participant.

The six-component protected publication failure
matrix in D memory-versioning.md §16.1 is normative.

E MUST preserve the D Fence/Admission participant
barrier and MUST NOT introduce an independent
publication ordering.

UNKNOWN remains non-final until resolved.

E MUST NOT expose canonical-looking Claims/Facts,
index events, public artifacts or serving references
before the applicable protected publication
conditions are satisfied.

Staging does not imply canonical acceptance.

E does not own canonical Claim/Fact identity
or I governance authorization.

### 19.2 Producer Admission and PublicationParticipant Admission

Producer Admission and PublicationParticipant Admission are
two distinct, ordered admission stages in the same protected
production and publication lifecycle.

They MUST NOT be treated as aliases, equivalent operations,
or interchangeable admission decisions.

Producer Admission admits the exact Producer/ProducerWork
identity into the canonical production lifecycle.

It MUST occur before dependency-set registration and
canonical revision commit, as specified in §19.1.

PublicationParticipant Admission admits the exact
PublicationParticipant bound to the corresponding
StorageVisibilityParticipantRef and publication tuple digest.

It MUST occur only after D has committed the applicable
canonical revisions and Storage has durably persisted the
exact publication tuple as PREPARED_HIDDEN.

Successful Producer Admission MUST NOT be interpreted as
successful PublicationParticipant Admission.

The two admissions MUST preserve the following order:

1. Producer Admission and durable recording of the exact
   admitted Producer participant.
2. Durable registration of the complete direct and
   transitive dependency set.
3. Canonical ClaimRevision/FactRevision commit and
   required canonical references.
4. Durable persistence of the exact Storage publication
   tuple as PREPARED_HIDDEN.
5. PublicationParticipant Admission against the current
   ForgetFence.
6. Subsequent protected visibility processing.

PublicationParticipant Admission MUST bind to the exact
committed publication identity and MUST NOT create,
replace, narrow, or independently redefine the dependency
closure established during Producer Admission and
dependency-set registration.

Both admission stages MUST be serialized against the
authoritative ForgetFence/Admission ordering anchor. The
"ForgetFence/Admission ordering anchor" and the
"per-BrainAuthorityRef serialization anchor" MUST denote
the same authoritative ordering anchor; neither name may
be interpreted as a separate lock or transaction domain.

For each admitted Producer participant P, the complete
direct and transitive dependency closure established by
Producer Admission MUST be durably persisted before the
corresponding participant barrier may be resolved or
completed. A Fence MUST NOT mark that participant barrier
resolved or complete while any member of that complete
dependency closure remains unpersisted.

The observable completion predicate is:
DependencyClosurePersisted(P) = TRUE if and only if the
authoritative durable dependency-registration record for
P identifies the complete direct and transitive dependency
set, its completeness state is COMPLETE, its persisted
closure digest matches that exact set, and an authoritative
read-after-commit confirms that record. A participant
barrier MUST be resolved or completed only when this
predicate is TRUE.

An UNKNOWN dependency, a missing dependency record, an
incomplete closure record, an unavailable authoritative
read, or any dependency-persistence failure MUST NOT be
treated as successful dependency persistence or successful
barrier completion. UNKNOWN MUST remain unresolved.

The dependency closure MUST NOT be narrowed, truncated,
or otherwise reduced to make a participant barrier resolve
or complete earlier. PublicationParticipant Admission
MUST preserve the complete closure established by Producer
Admission; it MUST NOT redefine or reduce the set used by
the completion predicate.

For each admission stage, successful admission and durable
recording of the exact admitted participant MUST form one
indivisible operation within the authoritative serialized
Transaction Domain.

Admission MUST NOT report success if the corresponding
participant recording fails or is not durably visible.

A subsequent Forget Fence MUST NOT pass the corresponding
unresolved admitted-participant barrier.

A later Fence MUST account for every successfully admitted
participant through the authoritative serialized barrier.

It MUST NOT silently skip, erase, or substitute either
participant identity.

The implementation MUST preserve the distinction between
Producer Admission and PublicationParticipant Admission,
including their respective participant identities,
durable records, ordering, dependency closure and terminal
Forget outcomes.

This is an implementation-conformance gate, not an
unresolved normative ordering choice.

#### T17-PUB / T18-PUB — Second-stage Admission rejected by Forget Fence

When Producer Admission has successfully linearized, but the corresponding PublicationParticipant Admission is rejected by a Forget Fence, the rejection MUST produce an explicit terminal disposition for the exact publication identity. Successful Producer Admission MUST NOT authorize publication visibility or substitute for successful PublicationParticipant Admission.

The following requirements are normative:

1. **Canonical Revision terminal state.** Any Canonical ClaimRevision/FactRevision already committed for the operation MUST remain committed as a canonical historical record, but MUST remain permanently non-public. It MUST NOT become publicly visible through the rejected publication. A subsequent independent operation MAY establish a new authorized publication outcome, subject to all applicable admission, dependency-closure and ForgetFence requirements. Retrying, replaying or resuming the same rejected operation MUST NOT constitute independent authorization.

2. **E Publication disposition.** Any E Publication already produced for the rejected publication identity MUST have its public visibility revoked or MUST be isolated from all public visibility paths. It MUST NOT be replayed, restored or treated as a successful visible effect of the rejected publication. Its existence MUST NOT establish successful PublicationParticipant Admission.

3. **Storage tuple disposition.** The exact Storage publication tuple persisted as PREPARED_HIDDEN MUST be cancelled or isolated. In either case, it MUST remain non-visible and MUST NOT advance through protected visibility processing under the rejected publication identity. Cancellation or isolation MUST have an auditable terminal outcome. An unresolved tuple MUST NOT be treated as cancelled, successfully published or eligible for visibility advancement.

4. **First-stage participant disposition.** The successfully admitted Producer participant MUST receive an auditable suppression disposition for the rejected publication. That disposition MUST explicitly identify and bind to the exact rejected PublicationParticipant identity, its corresponding StorageVisibilityParticipantRef, and the exact publication tuple identity. A generic operation-level suppression disposition MUST NOT satisfy this requirement. The Fence MUST preserve the original Producer participant identity and MUST NOT substitute a PublicationParticipant that was never successfully admitted.

5. **Recovery, retry and alternative publication paths.** Recovery MUST preserve the non-visible terminal disposition of the rejected publication. Retry MUST NOT convert the rejected second-stage Admission into successful Admission. An alternative publication path MUST NOT expose the same tuple or reproduce its rejected visibility outcome. Every recovery, retry and alternative publication path MUST verify authoritative evidence of successful second-stage Admission and an independently authorized visibility outcome before any visibility advancement. Missing, conflicting or UNKNOWN evidence MUST fail closed. A tuple without proven successful second-stage Admission and an authorized visibility outcome MUST remain non-visible.

These requirements apply to the exact publication identity and its associated Canonical Revision, E Publication, Storage tuple and admitted Producer participant. The implementation MUST maintain an auditable association across all corresponding terminal dispositions.

This is an implementation-conformance gate. It does not change the ten-step ordering specified in §19.1 or the six-step ordering specified in §19.2. Neither ordering MAY be reordered, shortened or reinterpreted by these terminal-disposition requirements.

#### Storage boundary

The existing Storage L1 decision remains unchanged.

This protocol does not approve Storage L4.
