# Memory Compiler Stage Contract

- **Status:** PROPOSED — contract-level reference; not production authorization
- **Owner:** E — Memory Compiler and derived-memory production
- **Work Item:** GAP-BASELINE-001 / GAP-01
- **Baseline:** 1ad6c2cf67a228f597fcbe1c7149c328ecbf38e9

## 1. Purpose and authority

This document defines the compiler transformation boundary from accepted source events/memories to derived-memory candidates with explicit lineage. It does not redefine the Event Store custody contract. Event Store acceptance is not compilation, verification, indexing, publication, or canonicalization.

Owner E owns the stage transformations and lineage production only. This contract does not decide Owner I's permission/retention/security policy or Owner D's canonical authority and publication rules.

## 2. Types

- `SourceEvent`: accepted event envelope reference containing `event_id`, `producer_actor_ref`, `scope_ref`, `payload_ref`, `payload_digest`, `idempotency_key`, and `accepted_at`.
- `SourceMemory`: source memory materialized from an accepted event; `memory_id`, `source_event_id`, `scope_ref`, `content`, `content_digest`, `created_at`.
- `NormalizedMemory`: validated, normalized representation; `memory_id`, `scope_ref`, `normalized_content`, `normalization_version`, `source_digest`.
- `DerivationRequest`: immutable input set of source memory IDs, transformation ID/version, and deterministic parameters.
- `DerivedMemoryCandidate`: derived content plus required lineage metadata; not inherently canonical or publishable.
- `ProvenanceRecord`: immutable mapping from a derived candidate to its immediate sources and transitive roots.
- `StageFailure`: typed failure with stage, stable error code, retryability, and input identity. Error payloads must not expose protected content.

All IDs and references are opaque non-empty strings. Digests are lowercase hexadecimal SHA-256 strings (64 characters). Timestamps are RFC 3339 UTC instants. Content is treated as untrusted data, never as executable instructions.

## 3. Stage enumeration and contract

| Stage | Input → output | Failure semantics | Idempotency |
|---|---|---|---|
| Ingest | `SourceEvent` → `SourceMemory` (zero or more, each retaining event identity) | **FAIL-CLOSED**: malformed envelope, missing required custody fields, or digest mismatch rejects the event from compilation; no partial acceptance | Same event ID + same digest yields the same logical source identity; same event ID + different digest is a conflict |
| Validate | `SourceMemory` → `ValidatedSourceMemory` | **FAIL-CLOSED**: missing identity/scope/content or invalid digest stops the item | Pure validation; same bytes and rules produce same result |
| Normalize | `ValidatedSourceMemory` → `NormalizedMemory` | **FAIL-CLOSED**: unsupported encoding, ambiguous required structure, or normalizer error produces no normalized output | Keyed by source memory ID + source digest + normalizer ID/version; repeat returns equivalent output |
| Derive | ordered `NormalizedMemory[]` + `DerivationRequest` → `DerivedMemoryCandidate` | **FAIL-CLOSED**: insufficient inputs, transformation error, or invalid output yields no candidate; no silent partial derivation | Keyed by ordered source IDs/digests + transformation ID/version + canonical parameter digest |
| Provenance | candidate + immediate source lineage → `ProvenanceRecord` | **FAIL-CLOSED**: missing source, cycle, broken link, or unresolved root prevents candidate from advancing | Same candidate identity and lineage inputs produce the same record; duplicate writes must be logically equivalent |
| Publish gate | candidate + provenance + policy decisions → publication request | **FAIL-CLOSED** until all required policy/authority decisions are available; this contract defines no publication side effect | A future publisher must use a stable candidate/idempotency identity; semantics are pending Owner D/I decisions |

No stage may convert a failure into an apparently successful empty result. Retryable failures may be retried with the same idempotency identity. Non-retryable failures require corrected input or a new transformation version.

## 4. Required provenance fields

Every derived candidate MUST carry the following fields. “Optional: no” means omission invalidates the candidate.

| Field | Type | Optional? | Meaning |
|---|---|---:|---|
| `derived_memory_id` | string | No | Stable identity of this derived memory |
| `derivation_id` | string | No | Stable identity of this derivation execution/logical operation |
| `transformation_id` | string | No | Named derivation algorithm |
| `transformation_version` | string | No | Immutable algorithm version |
| `immediate_source_memory_ids` | string[] (non-empty) | No | Direct source memory IDs |
| `root_source_memory_ids` | string[] (non-empty) | No | Deduplicated terminal source memory IDs |
| `source_event_ids` | string[] (non-empty) | No | Event identities anchoring the source memories |
| `source_digests` | string[] (SHA-256) | No | Content digests aligned to immediate sources |
| `scope_ref` | string | No | Scope label copied as data; permission inheritance is not implied |
| `created_at` | RFC3339 UTC | No | Candidate creation instant |
| `compiler_contract_version` | string | No | Contract version used to produce the candidate |
| `parameter_digest` | SHA-256 | No | Digest of canonical derivation parameters |
| `parent_derived_memory_ids` | string[] | Yes | Immediate parents that are themselves derived memories |

Array ordering for immediate sources is significant and stable. Root IDs are unique and sorted lexicographically for deterministic comparison. Source digests and event IDs are aligned to immediate source order. The source-event identity is retained through each source memory; if an upstream source memory has multiple event anchors, all anchors are preserved.

### Traceback termination

A lineage walk terminates only at a source memory explicitly classified as a non-derived root, with a non-empty `source_event_id` and verifiable source digest. A derived node must have at least one immediate parent and every parent must resolve. Missing nodes, cycles, empty roots, missing event anchors, or digest mismatch are errors; the walk must never silently truncate. Root source IDs are the set of all reachable non-derived roots.

## 5. Cross-owner decisions — unresolved

- **PENDING CROSS-OWNER DECISION — Owner I:** What exact permission, principal, scope, revocation, retention, and Forget constraints (if any) must be inherited or re-evaluated when a source memory produces a derived memory? Which source-policy changes invalidate or suppress existing derivatives? **This contract does not decide; pending explicit Owner I ruling.**
- **PENDING CROSS-OWNER DECISION — Owner D:** Which authority defines canonical status, and what validation/acceptance barrier must a derived candidate pass before any canonical registration or publication? Can derived memories ever become canonical, and under what authority? **This contract does not decide; pending explicit Owner D ruling.**

Until these rulings exist, the reference model stops at a non-canonical candidate plus provenance. It does not authorize publication, canonical registration, permission inheritance, or policy bypass.

## 6. Reference model and verification boundary

The Python reference model under `reference-model/` demonstrates only deterministic contract invariants: required identity/digest checks, deterministic normalization/derivation identities, complete lineage resolution, cycle/missing-parent rejection, and fail-closed behavior.

It is not a production implementation. It does not provide storage, transactionality, WAL, fsync, crash recovery, queueing, worker leases, distributed coordination, cryptographic verification of payload bytes, authorization, retention/Forget enforcement, canonical registration, publication, indexing, retrieval, or performance/security qualification. No production durability or runtime behavior is claimed.

Run from repository root:

```sh
python3 -m unittest discover -s 04-memory-compiler/reference-model -p 'test_*.py' -v
```

The test suite reports its actual count at execution time. A passing reference-model test is not architecture acceptance or independent review.
