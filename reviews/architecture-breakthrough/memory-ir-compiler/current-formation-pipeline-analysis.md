# Current Memory Formation Pipeline Analysis

- Research ID: MB-IR-001
- Status: RESEARCH / CANDIDATE; no production change
- Repository baseline: `main` HEAD `b3c666e67982cb3d3374e759cfb6552c7765aacb` (2026-11-18 session baseline)
- B source pin referenced by Issue #43: branch `session-b-domain-model-phase3`, HEAD `2faf8ec38f14dba49e7263d7a60804dae1a74ee2`; `02-domain-model/domain-model-overview.md` Blob `4d1debc0ec19b3917f9e76d04bb66da4df4cd346`
- Main guide pins: E compiler guide ZH Blob `84af043e306c54114e1129141ebe128f153c74e6`; B domain guide ZH Blob `a9f53a453aec25c47c58c4aea75adc43c83028d3`
- System integration authority: Issue #43, live read on 2026-11-18.

## 1. Executive finding

The repository already describes a compiler-like, recoverable semantic transformation pipeline. It is not a blank slate. The current architecture separates durable acceptance, compile work, candidate production, canonical commit, indexing, and context application. It also already requires source lineage, versioned model/prompt/policy information, idempotent replay, current authorization/Forget re-checks, and explicit conflict proposals.

The gap this research can responsibly identify is narrower: the inspected high-level guides describe stage outputs and obligations, but do not establish one shared, explicitly versioned, typed *inter-stage candidate representation* with uniform diagnostics and transformation contracts. This is a documentation/evidence gap in the inspected baseline, not proof that detailed E-owner contracts lack such a representation. The detailed E branch was referenced by the guide but was not fully read in this pass; therefore claims about its absence remain NOT VERIFIED.

## 2. Current flow reconstructed from live guides

```text
Durable Event + Idempotency + Accepted Receipt
  -> Recoverable Compile Intent / Work Item
  -> Scope and authorization checks
  -> Deterministic normalization and classification
  -> Optional model-assisted extraction
  -> Evidence / Provenance / Candidate Memory & Claim
  -> Entity and Relation resolution proposals
  -> Conflict proposal + Canonical Write Request
  -> D-owned Canonical Commit
  -> Index / Projection publication request
  -> downstream Runtime / Context / Adapter boundaries
```

The E guide explicitly distinguishes Accepted, Compiled, Candidate Produced, Canonical Committed, Indexed, and Context Applied. A successful earlier milestone is not evidence for a later one. Model-assisted extraction is optional; deterministic work must continue when inference is unavailable. Scope filtering precedes source dereference and entity matching. A replay must not bypass current Permission or Forget Fence.

## 3. Domain baseline: decided versus blocked

### Decided in the inspected B source wording

The B Domain Model Overview says Event, Memory, Claim, Entity, Relation, Evidence, Provenance, Memory Version, Memory Source, Memory Context, Context Entry, Agent Scope, and Environment Scope are distinct concepts. It also says:
- Event is captured/submitted material, not necessarily objective truth.
- Memory is a retained, addressable asset, not a truth guarantee.
- Memory can contain multiple Claims; Claims have epistemic and temporal qualifications.
- Evidence supports, refutes, or qualifies Claims; Provenance records origin and derivation.
- Epistemic status, lifecycle, temporal qualification, confidence, relevance, trust, and evidence strength are orthogonal.
- Immutable versions, conflict preservation, explicit Scope, and deterministic side-effect-free domain validation are required.

### Explicitly not available for this research to decide

Issue #43 records Fact/Claim as ADR-BLOCKED. It reports competing descriptions across B Overview and I-04/P-04. The Chinese Domain Model Guide itself warns that older wording treating Fact as a qualified Claim interpretation must not freeze downstream schemas while the ADR is blocked. Therefore this research uses neutral `AssertionCandidate` / `PropositionCandidate` labels and does not define canonical Fact/Claim types.

Other open points in the B Overview include Claim identity across Memory versions, uncertain timestamp representation, and whether an attestation domain needs a distinct immutable Fact object.

## 4. Current pipeline strengths and unresolved questions

| Area | Observed baseline | Research question |
|---|---|---|
| Acceptance durability | Separate Accepted receipt and durable work item | What is the compiler's stable source-to-node identity? |
| Extraction | Optional, bounded, versioned model assistance | How are model proposals represented without giving them authority? |
| Normalization | Deterministic stage named | Are input/output schemas and pass contracts shared and versioned? |
| Evidence | Evidence/Provenance creation is explicit | Can every derived node carry exact evidence edges and unavailable/redacted reasons? |
| Entity resolution | Candidate proposals; Scope first | How to preserve mention identity separately from canonical Entity identity? |
| Conflict | Conflict proposals, no silent overwrite | Can conflict sets be first-class diagnostics rather than ad hoc output? |
| Replay | Stable IDs, digest, idempotency, current fence re-check | Is reprocessing deterministic across model/rule/schema revisions? |
| Commit | D owns canonical commit | Can IR be lowered into D requests without becoming a competing domain model? |
| Versioning | Schema/policy/model versions required | Is there a compatibility and historical interpretation policy? |

## 5. Compiler analogy: useful and not useful

Useful: a stable boundary between parsing/extraction and downstream semantic passes; typed nodes; pass-specific preconditions/postconditions; deterministic validation; diagnostics with source locations; explicit pass/config versions; dependency tracking; and incremental invalidation.

Not useful: pretending memory formation is a pure compiler. LLM output is probabilistic, external sources may be unavailable, authorization/Forget are live governance checks, Entity resolution may require human review, and canonical commit is a separately owned durable side effect. Optimization must never discard evidence, merge disputed claims, promote plans to outcomes, or rewrite history.

## 6. Evidence limitations

This pass read Issue #43, main README and documentation portal, the B Domain Model Overview on its named branch, and bilingual B/E architecture guides. It did not read every field-level B artifact, every E Owner contract, all tests, or every consumer mapping. The B branch head and source pins above are recorded as supplied by Issue #43, not independently refreshed from branch metadata in this pass. These gaps remain explicit; no completeness claim is made.

## 7. Disposition

Recommend a bounded, non-authoritative candidate IR at the compiler boundary, subject to E Owner and B Owner review. Do not add it to the canonical domain model or production pipeline yet. First prove that it improves traceability, diagnostics, and repeatability enough to justify its maintenance cost.
