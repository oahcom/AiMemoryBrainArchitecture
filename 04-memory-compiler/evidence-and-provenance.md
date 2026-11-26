---
document_metadata:
  domain: memory-compiler
  role: design-specification
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Applicable-To-Current-Version
      evidence_reference:
        - "AID-2026-082"
        - "source branch: session-e-memory-compiler-2026-11-16"
        - "source commit: ee098e14747d9915de5b3efb63b3a8dd77f670ed"
        - "original source blob: 38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact E source Blob pinned; Owner exact-version and dependency review pending."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Candidate
    canonical_scope: "Memory Compiler evidence and provenance obligations"
    canonical_scope_id: memory-compiler/evidence-and-provenance
    canonical_scope_keywords:
      - evidence
      - provenance
      - traceability
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/04-memory-compiler/evidence-and-provenance.md"
    zh-CN: "docs/zh-CN/04-memory-compiler/evidence-and-provenance.md"
---

# Evidence and Provenance

**Status:** DECIDED for traceability, authorization and Forget obligations; CANDIDATE for graph representation; OPEN for final DAG and reference contracts pending D/I.  
**Owner:** Memory Compiler / MC-03.  
**Integration:** INT-P0-02/03/04; INT-P1-02/06; DM-006/007/010/011.

## 1. Purpose

Create and maintain the verifiable source links and derivation lineage for every compiler-produced candidate and every canonical asset accepted from it. Evidence answers what source material supports, refutes or qualifies a proposition. Provenance answers how a target was derived. Neither is a truth score.

## 2. Scope

Includes Evidence identity proposals, source reference and locator validation, source-span preservation, Evidence-to-proposition role links, provenance nodes/edges, method and model lineage, source trust metadata propagation, access control checks, lineage traversal, dependency registration and Forget-aware invalidation.

Excludes D's final canonical Evidence/Claim schema, I's policy and physical deletion authority, canonical store transaction implementation, source truth adjudication and external provider erasure guarantees.

## 3. Responsibilities

Bind every Evidence item to a typed, versioned source reference where available; preserve locator, source digest, collector, recorded/observed time and Scope; distinguish support/refutation/qualification/context-only roles; record transformation method/version/input digest/parent provenance; preserve common ancestry; enforce independent Evidence authorization; register derivation dependencies for Forget; mark unavailable/restricted/expired/forgotten sources honestly.

## 4. Non-Responsibilities

Evidence manager does not determine that a proposition is true, convert source trust into Claim verification, decide Fact/Claim identity, assign final lifecycle, own canonical entity identity, or retain content against I's Forget policy.

## 5. Inputs / Outputs

**Inputs:** source Event/document/tool/environment reference, source digest/version, validated span/locator, CandidateProposition/RelationHypothesis, ScopeRefs, actor/collector, method receipt, trust metadata, retention/sensitivity, evidential role.

**Outputs:** EvidenceDraft/Canonical Evidence proposal, EvidenceLink, ProvenanceNode/Edge, dependency registration, lineage query result, structured access/unavailability result, and Forget impact references.

## 6. Data Model

### 6.1 Evidence (logical proposal aligned to B)

~~~text
Evidence {
  evidence_id: OpaqueId
  evidence_kind: source_span | user_statement | document | observation |
                 tool_result | attestation | derived_excerpt
  source_ref: TypedObjectRef
  source_version_ref: TypedObjectRef?
  locator: Locator?
  excerpt_ref: ContentRef?
  source_digest: Digest?
  observed_at: TimeValue?
  recorded_at: Instant
  collector_ref: ActorRef
  evidential_role: supports | refutes | qualifies | context_only
  source_reliability_ref: TypedObjectRef?
  scope_refs: ScopeRef[]
  availability_state: available | restricted | expired | forgotten | external_unavailable
  retention_class: RetentionClass
  sensitivity: Sensitivity
}
~~~

### 6.2 Locator and EvidenceLink

~~~text
Locator =
  MessageSpan(message_ref, byte_or_token_range, encoding_version)
  | DocumentLocation(document_ref, page, block_or_char_range)
  | JsonPath(source_ref, canonical_path)
  | MediaRange(source_ref, start_time, end_time, track_ref?)
  | EnvironmentTick(environment_ref, tick_or_frame, observation_ref)
  | StructuredField(source_ref, field_path)

EvidenceLink {
  target_ref: TypedObjectRef
  evidence_ref: TypedObjectRef
  role: supports | refutes | qualifies | context_only
  strength_assessment: MethodQualifiedScore?
  asserted_by: ActorRef
  scope_refs: ScopeRef[]
  created_at: Instant
}
~~~

Strength is specific to a target-evidence link, method-qualified and distinct from source trust or claim confidence. No numeric rubric is frozen here.

### 6.3 Provenance Node / Edge

~~~text
ProvenanceNode {
  provenance_id: OpaqueId
  target_ref: TypedObjectRef
  derivation_kind: direct_capture | extraction | normalization |
                   summarization | consolidation | inference |
                   human_correction | verification | migration
  method_ref: MethodRef
  derived_at: Instant
  input_digest_refs: DigestRef[]
  unavailable_reason: String?
  scope_refs: ScopeRef[]
  pipeline_version: Version
}
ProvenanceEdge {
  provenance_id: OpaqueId
  source_ref: TypedObjectRef
  source_role: primary | supporting | contradicting | context
  locator_ref: TypedObjectRef?
  parent_provenance_ref: TypedObjectRef?
}
~~~

A derivation has one target and one or more declared source edges, or an explicit unavailable reason permitted by policy. A method reference describes process; it does not prove correctness.

## 7. Pipeline / State Machine

~~~mermaid
flowchart TD
 S[Source Event / Document] --> L[Resolve source + immutable version]
 L --> A[Authorize source and Scope]
 A --> V[Validate locator / digest]
 V --> E[Create Evidence + role links]
 E --> P[Create Provenance node and parent edges]
 P --> D[Register dependency edges]
 D --> C[Attach to candidate / canonical transaction]
 C --> X[Publish lineage/change event]
~~~

Evidence state: DRAFT → VALIDATED → PERSISTED → RESTRICTED / EXPIRED / FORGOTTEN / EXTERNAL_UNAVAILABLE. Provenance state is append-only; corrections add nodes/edges or explicit superseding metadata, never rewrite history.

## 8. Invariants

Every derived Memory/Claim/Relation has traceable Evidence/Provenance or explicit unavailability reason; source and locator are validated against exact immutable source version/digest; mutable URL alone is not durable evidence; Evidence role is target-specific; common ancestry is preserved; Evidence authorization is independent; Provenance cannot traverse unauthorized Scope; model output cannot invent spans/digest/actor/lineage; Forget metadata cannot retain forbidden content; cycle policy must be declared before canonical use.

## 9. Idempotency

Evidence identity derives from source identity/version + locator + digest + Scope + evidence kind. Same identity/digest reuses record; changed digest is a new source version or integrity conflict, never overwrite. Provenance node identity derives from target proposal/version + derivation kind + method version + ordered input digests. Repeated stage execution returns prior node. Changed method/input creates a new node linked to prior lineage.

## 10. Consistency

Evidence records and target links commit atomically with candidate/canonical version or through an outbox protocol preventing a committed target from appearing without required lineage. Provenance dependency edges persist before derivation is declared complete. If canonical and provenance stores are separate, canonical transaction includes a durable pending-lineage marker; visibility is withheld until required provenance commits. Projection failure is repaired from canonical change log.

## 11. Failure Recovery

Missing source bytes preserve typed source ref/digest and mark unavailable; locator mismatch rejects link; Evidence persistence failure defers candidate; Provenance edge failure blocks completion/publication; changed external URL is not silently substituted; Forget fence suppresses dereference and cancels downstream jobs; replay reuses original source identity/digest where permitted; partial graph read returns explicit incomplete status.

## 12. Security / Scope

Before source fetch, locator resolution, lineage traversal or dependency expansion, authorize principal for each source and edge. Apply Scope filters before graph traversal and before aggregating counts. Derived summaries inherit no broader access than source policy unless I explicitly authorizes declassification. Locator paths, message IDs, page numbers and environment coordinates may be sensitive. Memory read does not imply evidence.read. Workers re-check permission and Forget fence before each protected dereference and commit.

Prompt-injection provenance retains source type, trust label, untrusted-content classification, extraction method and source span. This supports auditing but does not make content safe. Evidence is never executable instruction or tool authorization. Detection is heuristic and incomplete; downstream models may still be influenced.

## 13. Performance / Backpressure

Bound lineage depth, fan-out, page size and dependency traversal time. Use paginated traversal with continuation watermark and explicit partial result. Avoid eager loading source content when metadata suffices. Cache keys include principal/scope/policy epoch and source version; revocation/Forget invalidates cache. Measure provenance coverage, traversal depth/fan-out, dependency discovery duration, incomplete lineage, duplicate ancestry and Forget residual count. Numeric bounds are TO_VALIDATE.

## 14. Observability

Trace source_ref → evidence_id → provenance_id → candidate_id → canonical version. Record method/model/rule versions, digests, role, locator-validation result, availability state, authorization decision ref, graph generation, retry and error. Do not log excerpt contents or sensitive locator strings. Metrics include lineage completeness, evidence access denials, unavailable source rate, graph depth/fan-out, dependency queue age and deletion progress.

## 15. Interfaces

- **Extraction → Evidence:** source span/locator, source digest/version, proposition ref, role hypothesis, Scope and method receipt.
- **Evidence → D:** typed Evidence refs and source availability; D owns final object contract.
- **Evidence → Consolidation:** target-specific support/refute/qualify links, common ancestry, trust metadata and provenance.
- **D → F:** canonical evidence/provenance refs and generation; F must not expose unauthorized source.
- **E/D → I:** dependency registration and Forget-impact enumeration; I owns policy, access barrier and physical deletion.
- **G:** receive Forget/retraction/supersession notifications so Context references can be reconciled.
- **Storage/Consistency:** atomic target+lineage visibility and replayable outbox.

## 16. Test Scenarios

Source span exactness; same source duplicated does not count as independent; Evidence supports and refutes distinct Claims; source unavailable during replay; unauthorized Memory read but denied Evidence dereference; cross-scope lineage traversal; provenance cycle rejection; partial lineage response; crash between target proposal and lineage commit; Forget during lineage expansion; source digest changes; malicious content preserved as data.

## 17. Dependencies

B Domain Model reference/time/scope semantics; D canonical object and version contract; I policy/retention/Forget; H authenticated ActorRef; extraction IR; Entity/Relation Manager; storage/outbox; F projection and G context invalidation consumers.

## 18. Open Questions

- **OPEN:** INT-P1-06/DM-007 DAG versus restricted cycle semantics; proposed default is strict acyclic derivation graph, no cycle edges in lineage.
- **OPEN:** typed locator and ContentRef final schema with D.
- **CANDIDATE:** Evidence identity and Provenance node identity formulas.
- **TO_VALIDATE:** lineage depth/fan-out limits, traversal latency and dependency discovery completeness.
- **OPEN:** retention policy for digests and minimal tombstones when source content is forgotten.


## 19. Durable dependency registration and Forget addendum

- Every Evidence, EvidenceLink, ProvenanceNode/Edge, excerpt, normalized artifact and derived summary must retain transitive source lineage or an I-approved non-reversible dependency token.
- Dependency registration is a publication prerequisite, not eventual metadata enrichment. Persist staged output privately, persist provenance, register all source dependencies with the D-owned Forget inventory/barrier, revalidate the fence, and only then make the object visible.
- A provenance edge alone is not proof that D's completion barrier has accounted for an in-flight producer. E must register the producer/run and obtain durable dependency-registration acknowledgement.
- Source content, excerpt refs, raw payload hashes and reversible payload URIs must not be copied into Forget tombstones. Tombstones contain only minimum non-reconstructive suppression evidence permitted by I.
- On fence activation, block dereference and lineage expansion into forgotten sources; mark descendants suppressed/restricted and report incomplete/unreachable traversal as pending/unknown, never complete.
- See `forget-fence-and-derived-registration.md` for the visibility gate, race protocol and failure matrix. Physical erasure and global completion remain I-owned.


## 19. Phase 3 producer-registration, cursor and visibility alignment

This appendix consumes D `30dbffdc7d47af0888ecf7b42cfa686d2ec0c9d6` and does not freeze a cross-module schema.

- Every Evidence/Provenance node and edge produced by a compiler run is a derivative. It is first persisted in private staging and is not queryable or traversable by Runtime/other consumers until all direct and transitive dependencies have durable D DerivedRegistrationReceipt(s) and the final Publication Gate succeeds.
- The lineage record binds EventRef, source version refs, provenance parent refs, DerivationRunId, ProducerWorkItemId, exact ScopeRefs, lineage digest, observed ForgetFenceCursor and PermissionEpoch. The observed epochs are historical evidence, not authorization to publish later.
- SourceEventCursor remains E's ingress partition position. CanonicalCommitCursor is D's single globally ordered per-Brain-authority committed transaction position. AggregateRevision is per aggregate. LifecycleEventCursor is per Memory. IndexWatermark is F-owned and applied-through a CanonicalCommitCursor. ForgetFenceCursor and PermissionEpoch are separate namespaces. No provenance field named generic `cursor` or `generation` may carry one of these without its explicit type.
- When D confirms a canonical commit, Provenance records the returned CanonicalCommitCursor and exact AggregateRevision refs as separate fields. A LifecycleEventCursor is recorded only when a lifecycle event exists. Candidate-only extraction/provenance has none of these canonical fields.
- Provenance persistence alone is not dependency registration. A local edge is not a D registration receipt. Any missing/partial/unknown D registration leaves the complete derivative lineage private and non-visible.
- The atomic relationship between E Storage staging, D dependency inventory, D final gate and Storage visibility remains **OPEN / BLOCKING**. If these cannot be serialized in one transaction or a proven recoverable prepare/commit protocol, E must not expose the lineage or derivative.

Conformance scenarios (NOT RUN): partial provenance edge registration; duplicate registration ACK loss; Forget between lineage staging and gate; PermissionEpoch change during traversal; derivative-of-derivative ancestor suppression; cursor-type substitution rejection.
