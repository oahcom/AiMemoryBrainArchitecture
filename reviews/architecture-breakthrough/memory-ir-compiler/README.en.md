# Memory IR / Memory Compiler Independent Research

**Status:** Baseline pinned; domain mapping and prototype not yet completed.  
**Baseline:** `main@b3c666e67982cb3d3374e759cfb6552c7765aacb` (2026-11-18)  
**Tracking:** [Issue #43](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/43)

## Objective

Determine whether memory formation benefits from a Typed Intermediate Representation (Memory IR) that reduces repeated interpretation between stages and improves type/semantic validation, provenance, conflict diagnostics, deterministic reprocessing, and incremental evolution.

## Known critical constraint

Issue #43 still records the B Fact/Claim ADR as ADR-BLOCKED and notes unresolved convergence between consumer concept distinctions and canonical object identity. This research must not decide canonical Fact/Claim identity or present a candidate type system as the current domain model.

## Baseline readback

Read exact current B Domain Model, ADR, I-04/P-04 consumer mappings, Compiler/Ingestion/Extraction/Normalization, Entity Resolution, Provenance, Consolidation, Canonical Commit, and related tests. Record branch HEAD, path, Blob SHA, normative status, and read timestamp for each source.

## Candidate pipeline

Raw Experience → Parsing → Extraction → Memory IR → Type/Semantic Validation → Entity Resolution → Conflict Analysis → Optimization/Consolidation → Canonical Commit.

Test each stage ordering rather than assuming this pipeline is correct. Evaluate candidate representations such as Fact/Claim/Assertion/Event/Entity/Relationship/Procedure plus Source Evidence, Confidence, Authority, Provenance, Scope, and Temporal Semantics. Do not turn every useful term into a separate entity merely for completeness.

## Key questions

1. One IR or multiple IR layers?
2. What is the boundary between IR and the canonical domain model?
3. At what stage should Fact/Claim distinctions occur, and which decisions must remain with B/governance authority?
4. Is provenance immutable and carried through every compiler pass?
5. How are contradictions, expiry, hypotheses, uncertainty, and temporal validity represented?
6. How are IR, compiler passes, model/rule versions, and outputs versioned?
7. How are deterministic reprocessing and incremental compilation achieved?
8. How are schema evolution, historical IR interpretation, and migration handled?
9. Does IR reduce complexity, or add another abstraction and duplicate model?

## Prototype

Use identical deterministic synthetic inputs to implement:
- Direct Pipeline: extract directly into target structures;
- IR Pipeline: generate IR, then run type/semantic validation and normalization.

Compare Provenance Completeness, Type Validation, Conflict Detection, Determinism, Incremental Processing, Schema Evolution, Error Localization, Processing Cost, and Data Loss. Publish code, data, commands, and results; synthetic results are not production-quality proof.

## Technology reuse

Compare LLVM/MLIR IR concepts, JSON Schema, Protobuf, Avro, ASTs, Serde/Pydantic, and database migration tooling. Compare real adoption costs against building custom components.

## Deliverables and boundaries

Deliver pipeline complexity analysis, candidate IR model, compiler proposal, version/provenance strategy, Direct-vs-IR prototype, technology reuse matrix, migration risks, and bilingual report. Modify only this research branch; do not modify B/I authority contracts, freeze schemas, merge, or enter production implementation. Classify all conclusions as DECIDED / CANDIDATE / TO_VALIDATE / UNRESOLVED / REJECTED.
