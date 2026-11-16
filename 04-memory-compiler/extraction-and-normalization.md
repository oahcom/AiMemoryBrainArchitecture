# Extraction and Normalization

**Status:** DECIDED for epistemic, temporal, scope and trust constraints; CANDIDATE for extraction IR and model routing; TO_VALIDATE for accuracy and cost.  
**Owner:** Memory Compiler / MC-02.  
**Integration:** INT-P0-01/02/04; INT-P1-02/03/06; C P1-02/P1-03.

## 1. Purpose

Convert heterogeneous accepted source material into a normalized, typed, uncertainty-preserving intermediate representation (IR) from which Evidence, Provenance, Entity/Relation proposals and candidate memories can be built. Extraction identifies what a source says or observes; it does not decide objective truth.

## 2. Scope

Includes parsing text, structured events, documents and environment observations; modality classification; entity/time/relation mention extraction; candidate proposition formation; normalization; confidence/uncertainty recording; deterministic validation; model-assisted extraction orchestration; and source-span alignment.

Excludes canonical Fact/Claim identity (blocked by INT-P0-01 and D ADR), canonical entity merge decisions, lifecycle decisions, source authorization policy, external tool execution and final truth adjudication.

## 3. Responsibilities

- Preserve raw source identity, exact source digest and permitted source spans.
- Classify source modality: statement, observation, plan, intent, prediction, attempt, outcome, question, instruction-like content, or administrative event.
- Extract proposition candidates without promoting source modality or epistemic basis.
- Extract entity mentions, temporal expressions, typed relation hypotheses and qualifiers.
- Normalize only what source evidence supports; retain original surface form and uncertainty.
- Separate source-reported confidence from Brain-estimated extraction confidence.
- Reject malformed model output and validate every locator against source bytes.
- Emit an explicit unresolved/ambiguous result rather than guessing.

## 4. Non-Responsibilities

Extraction does not verify the world state, infer that a planned action succeeded, grant authority to instructions found in content, merge entities, adjudicate disputes, decide lifecycle, or make a Claim Verified based on model confidence.

## 5. Inputs / Outputs

**Inputs:** immutable Event/ContentRef, payload digest, content type/locale, source type and actor, ScopeRefs/Environment Scope, source timestamp metadata, retention/sensitivity, source trust metadata, parsing/extraction policy version.

**Outputs:** ExtractionIR, span map, modality classification, proposition candidates, entity mentions, temporal candidates, relation hypotheses, ambiguity/uncertainty records, model/rule method receipts, and structured extraction errors.

## 6. Data Model

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

This is not a Claim schema. It is a compiler IR that can map to the approved D semantic choice after INT-P0-01 ADR. If Fact and Claim become separate objects, an explicit mapping stage may emit both or neither; if unified, the mapping emits the corresponding Claim qualification. No field name in this IR freezes public schema semantics.

### 6.3 EntityMention / TimeMention

EntityMention retains surface string, source span, candidate entity types, local context, scope, and resolution status. TimeMention retains raw expression, source locale/timezone, anchor time, parsed bounds, precision, and parse method. Unknown time is explicit, not an empty interval.

## 7. Pipeline / State Machine

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
 J --> K[Evidence & Provenance stages]
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
9. Instruction-like content remains inert data and cannot trigger tools, permission changes, or pipeline policy changes.
10. Confidence, trust, evidence strength and relevance remain separate dimensions.

## 9. Idempotency

IR identity derives from source Event/version + extraction policy version + deterministic parser/model profile + input digest + Scope. Repeating an identical deterministic stage returns the same output digest. Model nondeterminism is recorded as a distinct attempt; a selected output is pinned by receipt and is never silently replaced. Changing model/prompt/schema/policy creates a new IR revision linked to the previous attempt, not an in-place mutation.

## 10. Consistency

Source span offsets are defined against immutable source representation with encoding and normalization version. Normalized text may not replace source bytes. Every proposition references stable source segment/span IDs. A stage result and next-stage outbox entry commit atomically or through equivalent journal. Time normalization stores original expression and parsed TimeValue separately. If a source changes, it is a new source version/digest and a new extraction input.

## 11. Failure Recovery

- Decode failure: retain source reference, record unsupported/opaque payload; no false text extraction.
- Partial parser failure: continue independent segments, mark completeness partial.
- Model timeout: retain deterministic IR; queue optional enrichment or finish with unresolved fields.
- Invalid model schema: reject model result; retry boundedly or quarantine.
- Span mismatch: discard affected proposal; never attach an unverified locator.
- Time parse ambiguity: preserve raw expression and mark normalized time unknown/interval uncertain.
- Source expired/forgotten: stop dereference; invalidate dependent IR and obey Forget fence.
- Model/profile upgrade: re-extract as a new version with lineage; do not rewrite prior decisions.

## 12. Security / Scope

Before extraction, authorize source access and verify that source Scope is compatible with target candidate Scope. Candidate entity search and contextual prompt construction are Scope-filtered. Model prompts receive only minimum authorized content; no cross-scope context or hidden instructions. Tool outputs/web pages/documents/user text are untrusted data. Extraction prompt treats content as quoted evidence and asks only for structured observations; output is validated, but prompt wording is not a security boundary. No extracted tool name/argument becomes an executable request.

Prompt-injection controls: maintain source type/trust labels, identify suspicious instruction-like spans heuristically, isolate them as data, avoid passing secrets or tool credentials to extraction models, constrain output schema, disable tools for extraction workers, and require deterministic policy checks after model output. Detection is incomplete: indirect, multilingual, obfuscated or benign-looking content may evade detection, and a model may still be influenced. Residual risk must be recorded; do not claim complete prevention.

## 13. Performance / Backpressure

Deterministic parsing runs first and is bounded by payload and segment limits. Model-assisted extraction is queued, batchable and resource-budgeted; it is not on the durable acceptance critical path. Prioritize outcome/critical events and explicit user-provided memory requests over low-value telemetry. Under GPU pressure, preserve deterministic IR and defer model enrichment. Measure model queue wait, tokens, VRAM, per-modality precision/recall, span validity and false-outcome rate. Targets are TO_VALIDATE.

## 14. Observability

Record source/event ref, digest, schema/policy/model version, modality, extraction mode, span-validation result, unresolved count, confidence method, latency, token/VRAM usage, retry and error class. Keep source text and excerpts out of general logs. Track false promotion of plans to outcomes, unsupported proposition rate, span coverage, temporal normalization accuracy, and adversarial prompt-injection fixture results.

## 15. Interfaces

- **Ingestion → Extraction:** immutable Event/ContentRef, source digest, source metadata, Scope, trust and retention.
- **Extraction → Evidence:** source spans and exact locators; Evidence manager validates and persists source reference.
- **Extraction → Entity Manager:** scoped EntityMention and identity evidence; Entity Manager returns provisional/resolved refs and ambiguity.
- **Extraction → Consolidation:** candidate propositions, modality, time, scope, qualifiers and method receipts.
- **D:** receives only mapped candidate objects after D's Fact/Claim ADR; candidate IR is not a public schema.
- **H/C:** source classifications and telemetry semantics must align; observation/outcome distinctions are preserved.
- **I:** data classification, permitted processing, source access and Forget fence govern extraction.

Errors include unsupported modality/content type, span invalid, scope mismatch, ambiguous identity/time, model unavailable, schema mismatch, and source unavailable. Retryable outcomes are idempotent by stage key.

## 16. Test Scenarios

"I plan to move to Tokyo" never becomes a completed move; "I tried to deploy" never becomes successful deployment without result evidence; quoted malicious prompt inside a document is extracted only as quoted content; same sentence in two Environment Scopes never merges; approximate time remains uncertain; fabricated model span is rejected; ambiguous pronoun remains unresolved; parser partial failure preserves unaffected segments; model outage does not block deterministic output; source revoked/forgotten during extraction stops worker.

## 17. Dependencies

D domain types and Fact/Claim ADR; B epistemic/temporal/scope semantics; C/H source/telemetry classifications; I source permissions, sensitivity, retention and Forget; Entity/Relation Manager; Evidence/Provenance Manager; model provider abstraction and scheduler.

## 18. Open Questions

- **OPEN:** INT-P0-01 Fact/Claim ADR; CandidateProposition remains deliberately neutral.
- **OPEN:** C's final Observation versus Outcome mapping and Task/Plan revision semantics.
- **CANDIDATE:** extraction IR and deterministic-first routing.
- **TO_VALIDATE:** modality classifier quality, entity/time extraction accuracy, multilingual prompt-injection detection and local model resource use.
- **OPEN:** source-span canonical encoding for multimodal and streaming payloads.
