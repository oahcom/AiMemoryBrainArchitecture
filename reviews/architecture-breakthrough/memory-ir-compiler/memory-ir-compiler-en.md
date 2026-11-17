# Memory IR and Memory Compiler Architecture Breakthrough Research

- Research ID: MB-IR-001
- Status: CANDIDATE / TO_VALIDATE; not a production architecture decision
- Repository baseline: `main` HEAD `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Isolated branch: `research/memory-ir-compiler-session-c-2026-11-18`
- Authority boundary: no B Owner domain-model edits, no removal of the Fact/Claim ADR block, and no production pipeline changes.

## 1. Executive summary

**Recommend a lightweight, layered, non-authoritative Memory IR candidate, but do not adopt it as a formal production architecture layer yet.**

The existing E Compiler already has a compiler-like pipeline: durable acceptance, persisted work items, Scope/Authorization checks, deterministic normalization, optional model extraction, Evidence/Provenance, Entity/Relation proposals, Conflict proposals, D-owned Canonical Commit, and downstream publication. Accepted, Compiled, Candidate Produced, Canonical Committed, Indexed, and Context Applied are explicitly distinct. This research is not an attempt to reinvent the Compiler.

The gap worth validating is narrower: whether stages need one shared, versioned, typed candidate representation with diagnostics and a dependency graph, instead of independently interpreting stage-local candidate structures.

Recommended layers:
- L0 Source Envelope: immutable source references, digests, acceptance and Scope metadata.
- L1 Extraction IR: EntityMention, AssertionCandidate, EventCandidate, EvidenceSpan and other unnormalized proposals.
- L2 Semantic IR: type/semantic-checked candidate graph, temporal/Scope qualifications, Provenance DAG and ConflictSets.
- L3 Commit Projection: mapping to the exact current D Owner contract, not a fourth canonical schema.

## 2. Current baseline and decision status

Issue #43 explicitly records the B Fact/Claim ADR as ADR-BLOCKED. Some older B Overview wording treats Claim as the canonical proposition object and Fact as a qualified interpretation; I-04/P-04 describe them as distinct concepts/objects. The bilingual B Domain Model Guide explicitly says older wording must not freeze downstream schemas while the ADR remains blocked.

Therefore:
- This research uses only the neutral `AssertionCandidate` term.
- It does not decide whether Fact and Claim are one object, separate objects, or a specialization relation.
- L3 lowering that depends on that mapping remains blocked.
- Domain objects, identity, lifecycle and canonical storage remain B/D Owner decisions.

Sources inspected: Issue #43; main README and documentation portal; B Domain Model Overview (branch/blob listed in Issue #43); bilingual B guides; bilingual E Compiler Guide. The full field-level E Owner branch contracts and tests were not individually inspected in this pass, so we cannot claim that no equivalent IR exists in those detailed contracts.

## 3. Why not one universal schema

A universal schema tends to mix raw source, model-extracted guesses, entity-resolution results and commit-ready canonical data in one structure. This encourages nullable-field sprawl and makes provisional model output look authoritative.

Layered Typed IR makes each stage's knowledge explicit:
- L1 EntityMention is not a Canonical Entity.
- AssertionCandidate is not a decided Fact/Claim.
- ConfidenceEstimate is not Truth, Trust or Evidence Strength.
- LifecycleHint is not a Canonical Lifecycle Transition.
- Entity Resolution is a Scope-filtered proposal, not permanent identity assignment during parsing.
- ConflictSet preserves incompatible candidates without selecting a winner.

## 4. Proposed pipeline

```text
Durable Accepted Event / Source Ref
  -> L0 Source Envelope
  -> Parse / deterministic extraction + optional model proposal
  -> L1 Extraction IR
  -> Type + structural validation
  -> Scope-filtered Entity/Relation resolution proposal
  -> L2 Semantic IR
  -> deterministic normalization / conflict / consolidation passes
  -> L3 D-contract-specific Commit Projection
  -> D Canonical Commit
  -> Index / Projection publication
```

IR is a non-authoritative compiler artifact. It does not own Canonical IDs, Lifecycle, Permission, Forget or visibility. Models propose candidates; they do not establish facts, approve lifecycle transitions or resolve authorization.

## 5. Recommended answers to key design questions

| Question | Research recommendation | Status |
|---|---|---|
| Introduce IR? | Shadow IR first; decide formal adoption after measurement | CANDIDATE |
| Universal or layered? | Three Typed IR layers plus separate Commit Projection | CANDIDATE |
| Distinguish Fact/Claim? | Neutral AssertionCandidate; no domain decision | ADR-BLOCKED |
| Entity resolution? | Extract mentions first; resolve later under Scope filtering | CANDIDATE |
| Provenance? | Required first-class graph edges for derived nodes | CANDIDATE |
| Conflict/expiry/speculation? | Separate epistemic, temporal, lifecycle and conflict dimensions | CANDIDATE |
| Reproducibility? | Record model output, prompt, rules, resolver snapshot and schema versions | CANDIDATE |
| Incremental compilation? | Precise invalidation using a pass dependency DAG | TO_VALIDATE |
| Historical interpretation? | Preserve old versions, explicit upgrade chain, fail closed on unknown major | CANDIDATE |
| Mature tools? | Reuse JSON Schema, Serde/Pydantic and migration tools | RECOMMENDED |

## 6. Provenance and reproducibility

Provenance must be a first-class IR graph, not a free-form string. Each derived node links to:
- EvidenceRef: source version, digest, span and availability;
- parent IR node(s);
- Pass Manifest: transformation ID/version and input/output digests;
- Model Manifest: provider/model revision, prompt digest, parameters, tool results and response reference;
- schema/rules/policy/resolver snapshot versions;
- redaction, deletion and unavailable reasons.

Replay classes:
- R0: pure deterministic pass; same inputs/config should be byte-identical.
- R1: repeatable when external dependency snapshots are pinned.
- R2: reuse recorded model output to reproduce downstream transformations.
- R3: fresh model invocation; a new compilation attempt, not deterministic replay.

Permission, PermissionEpoch, Forget Fence, Retention and final Visibility are live governance boundaries; a cache hit must not bypass them.

## 7. Synthetic prototype results and limits

A standard-library Python prototype and synthetic dataset have been added on the isolated branch:
- Direct Pipeline: one-pass mapping to a target-like shape.
- IR Pipeline: Parse → Typed IR → Semantic Validation → Lowering.
- Same five synthetic input rows, including one missing-source invalid row and overlapping contradictory assertions.
- Structured diagnostics, conflict proposals, lineage, deterministic replay summary and incremental node reuse count.

Reproduce:

```bash
python3 reviews/architecture-breakthrough/memory-ir-compiler/prototype/memory_ir_prototype.py
```

Expected: 5 input rows, 4 valid records; both paths propose one conflict set; repeated identical input yields stable IR output; changing one source leaves IDs for unchanged source nodes stable.

**Limit:** This is a synthetic deterministic fixture, not production-quality evidence. It does not test real NLP/LLM, Entity Resolution, persistent incremental caches, concurrency, crash recovery, Canonical Commit, Forget, Authorization or large-scale cost. The prototype does not prove production benefit.

## 8. Mature technology reuse boundary

- MLIR: borrow Dialect, Type, Pass, Verifier, Lowering, Diagnostics and IR Versioning concepts; do not embed the full MLIR runtime.
- LLVM IR: borrow strong typing and verification ideas only; abstraction level is too low.
- rustc: borrow dependency graph and incremental query invalidation.
- TypeScript Compiler: borrow AST and semantic-analysis staging.
- SQL AST/Query Planner: borrow separation of logical and execution plans, not truth semantics.
- JSON Schema: structural validation; cross-node invariants need custom validators.
- Protocol Buffers: consider only if Rust multi-service boundaries justify it.
- Avro: consider only if long-lived event streams and writer/reader schema resolution become real requirements.
- Pydantic / Serde: language-level validation and serialization tools, not the IR architecture itself.
- DB migration tools: manage physical schemas, not IR semantic version upgrades.

## 9. Complexity and migration risks

IR adds serialization, compatibility, pass manifests, diagnostics, cache invalidation and historical upgrade costs. If detailed E contracts already provide equivalent capabilities, a second IR may be duplicate abstraction.

Adoption sequence:
1. Do not change the production write path.
2. Select one source type for Shadow IR.
3. Compare candidate parity, provenance completeness, diagnostics, conflicts, replay and resource cost.
4. Have E/B/D/I and other affected Owners review their authority boundaries.
5. Only consider a narrow migration after measured benefit and approvals.
6. Retain the Direct Pipeline rollback path.

## 10. Final disposition

1. Does IR reduce transformation complexity? **Not proven.** It may reduce repeated interpretation but adds stages and version-governance cost.
2. Does it improve type safety and provenance? **Promising by design; the synthetic prototype only demonstrates diagnostic and lineage representation.**
3. Does it improve conflicts and incremental evolution? **It provides better structures; conflict algorithms do not improve automatically, and persistent incrementality is not implemented.**
4. Is it over-abstraction? **High risk if implemented as a general compiler framework or if every memory category becomes its own type.**
5. Adopt formally? **Recommend a Shadow Prototype, not a frozen production layer now.**
6. Can mature tools replace custom work? **They replace much serialization/validation infrastructure, not memory semantics, the provenance graph or pass contracts.**
7. Migration? **Shadow → compare → Owner review → one-type canary → expand/remove.**
8. Unresolved: Fact/Claim ADR, whether detailed E contracts already contain IR, real Entity Resolution cost, provenance/Forget retention boundaries, cross-service incremental and recovery semantics.

**Conclusion: RECOMMEND SHADOW IR / NOT READY FOR FORMAL ARCHITECTURE ADOPTION.**
