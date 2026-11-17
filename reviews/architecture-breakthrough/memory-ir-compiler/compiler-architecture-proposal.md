# Compiler Architecture Proposal

- Status: CANDIDATE / REQUIRES E OWNER + B OWNER REVIEW
- Recommendation: adopt a thin, layered, typed candidate IR at the compiler boundary; do not adopt LLVM/MLIR wholesale.

## 1. Proposed pipeline

```text
Durable Accepted Event / Source Ref
  -> L0 Source Envelope (stable digest, scope/admission refs)
  -> Parse / deterministic extraction + optional model proposal
  -> L1 Extraction IR (mentions, candidate assertions, evidence spans)
  -> Type + structural validation
  -> Scope-filtered Entity/Relation resolution proposal
  -> L2 Semantic IR (qualifications, lineage DAG, ConflictSets)
  -> deterministic policy/semantic passes
  -> D-contract-specific Commit Projection (L3)
  -> D Canonical Commit (existing authority; outside IR mutation)
  -> projection/index publication (existing downstream contract)
```

The diagram is a research proposal. It does not alter the current E stage ordering or grant a new commit path.

## 2. Why layered IR rather than one universal schema

One universal schema tends to collapse raw source, uncertain extraction, resolved semantics, and commit-ready canonical data into one shape. This makes optional fields proliferate and lets provisional model output look authoritative. A staged IR makes legal state transitions explicit and allows each pass to declare required information.

Use a compact core:
- envelope: schema version, stable node ID, source refs, scope, pass lineage;
- candidate payload: small tagged union;
- qualifications: epistemic, temporal, authority, confidence estimate;
- graph edges: evidence, derivation, entity mention/resolution, conflict;
- diagnostics: stable code, stage, node/source location, severity, remediation;
- extensions: namespaced, versioned optional data.

Do not introduce a standalone optimization framework in v1. A sequence of deterministic, pure passes with explicit inputs/outputs is sufficient.

## 3. Pass contract

Each pass declares:
- pass ID and implementation version;
- input IR versions and node kinds;
- output IR version and node kinds;
- preconditions and postconditions;
- determinism class (pure deterministic, deterministic with external snapshot, or nondeterministic/model-assisted);
- dependency keys and invalidation rules;
- diagnostics and retryability;
- resource budget and side-effect policy.

Pass categories:
1. Parse/extract: model-assisted and potentially nondeterministic; preserve raw response reference and generation metadata.
2. Validate: deterministic structural and semantic checks; no writes.
3. Normalize: deterministic canonicalization of dates, units, casing, aliases, and controlled vocabularies; never mutate evidence.
4. Resolve: scope-filtered identity proposals; deterministic only when resolver snapshot/index version is pinned; otherwise mark external dependency.
5. Analyze conflicts: conservative detection; produce proposals, never choose a winner by default.
6. Consolidate: propose grouping/dedup/summary with explicit parent lineage; never discard parents or supporting evidence.
7. Lower: map candidate representation into exact D-owned request schema; reject unknown required semantics.

## 4. Optimization is not truth optimization

Safe compiler optimizations include memoizing pure passes, avoiding repeated parsing for unchanged source digests, deduplicating identical *derivation work* by idempotency key, and pruning unreachable intermediate nodes only when retention policy allows and lineage remains reconstructible.

Unsafe transformations include deleting conflicting candidates, promoting inferred to verified, merging sources as independent corroboration, converting plan to outcome, dropping provenance for storage savings, or treating embedding similarity as identity.

## 5. Diagnostics

Diagnostics should be structured and stable:
`code`, `stage`, `node_id`, `source_ref`, `field_path`, `severity`, `message_key`, `retryability`, `related_nodes`, `pass_version`.
Messages can be localized separately. A diagnostic must not expose protected source content across Scope boundaries.

## 6. Incremental compilation

Build a dependency graph:
`source_digest -> extraction nodes -> validation nodes -> resolution nodes -> conflict/consolidation nodes -> commit projection`.
When a source changes, invalidate only descendants. When a resolver snapshot, model/prompt, ruleset, schema, or policy changes, invalidate only passes whose declared dependency set includes that version. Never reuse a cached result across a changed Scope, permission, Forget generation, retention, or authorization boundary without rechecking the live Owner contract.

For model-assisted passes, deterministic replay is not guaranteed merely by recording a model name. Persist the exact output or an immutable output reference plus provider/model revision, prompt/template digest, decoding parameters, tool results, input digests, and validation result. Re-run should either reuse the recorded output or be explicitly marked a new compilation attempt.

## 7. Canonical commit and governance boundary

IR is non-authoritative. It cannot own canonical IDs, lifecycle transitions, Forget state, permission decisions, or visibility. The L3 projection must target a pinned D contract. Canonical commit remains D-owned. Current Permission and Forget checks must be enforced at protected boundaries even if compilation was previously accepted.

## 8. Suggested implementation sequence (not authorized)

P0: schema-neutral prototype and conformance fixtures.
P1: E Owner review of IR envelope and stage ownership.
P2: B Owner mapping review, explicitly blocked on Fact/Claim ADR for affected mapping.
P3: bounded shadow-mode IR generation with no canonical write.
P4: compare diagnostics, lineage, replay and cost on real but access-approved data.
P5: only after approvals, migrate one narrow candidate path; preserve fallback and rollback.
No step here authorizes implementation in this architecture repository.
