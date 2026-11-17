# IR Versioning and Provenance Strategy

- Status: CANDIDATE
- Scope: compiler-internal compatibility; canonical version/lifecycle remain Owner-controlled.

## 1. Version dimensions must be separate

Do not overload one `version` field. Track at least:
- `ir_schema_version`: shape and type semantics of the serialized IR.
- `extractor_version`: parser/model adapter implementation.
- `model_revision` + `prompt_digest` + generation parameters: model-assisted output provenance.
- `ruleset_version`: deterministic normalization and semantic rules.
- `resolver_snapshot`: entity catalogue/index snapshot used for matching.
- `policy_version`: scope, retention, admission and processing policy references.
- `target_contract_version`: exact D-owned commit request schema.
- `compiler_build`: code build/commit identity.

Each pass records the subset it actually depends on. A global version bump should not invalidate unrelated deterministic stages.

## 2. Reproducibility levels

| Class | Meaning | Replay expectation |
|---|---|---|
| R0 deterministic | Pure pass, fixed inputs and config | Byte-identical output |
| R1 snapshot deterministic | External data dependency pinned (resolver/catalogue) | Byte-identical given same snapshot |
| R2 recorded model output | Model call not deterministic; immutable response is replay input | Reproduce downstream output, not model generation |
| R3 fresh model run | New inference attempt | New candidate compilation; compare, do not claim deterministic replay |

Model name alone is insufficient. Record provider, model revision where available, request parameters, prompt/template digest, tool outputs, input digest, response reference/digest, timestamps, and validation diagnostics. Secrets and protected content must not be copied into logs; store references under the owning retention/access policy.

## 3. Provenance as a first-class graph

Every derived candidate must link to:
1. source EvidenceRef(s), including immutable source version/digest and selected span when available;
2. parent IR node(s);
3. transformation/pass identity and version;
4. output digest;
5. availability/redaction/unavailable reason;
6. scope/authority context needed to interpret the derivation, using Owner-defined references.

Evidence and Provenance are not synonyms. Evidence supports/refutes/qualifies a claim-like candidate. Provenance explains the derivation path. A model output can be provenance for a candidate but is not itself proof of truth.

## 4. Historical interpretation

Never reinterpret old bytes silently under a new schema. Persist schema ID/version and canonical serialization rules. Keep:
- original raw source reference/digest (subject to governance retention);
- original IR blob or immutable reference for accepted compilations;
- pass manifest and diagnostics;
- explicit upgrade chain `v0.1 -> v0.2 -> ...`;
- upgrade result digest and migration tool version.

A reader must support either the historical version or an explicit deterministic migration. Unknown major versions fail closed for canonical lowering. Do not discard old representations just because a new schema is available.

## 5. Compatibility policy

- Patch: documentation/validation bug fixes with no semantic change; same serialized shape.
- Minor: additive optional fields or node kinds; old readers may ignore only if declared safe.
- Major: changed meaning, required fields, enum semantics, identity, or graph edge meaning.
- Breaking changes require migration fixtures, dual-read/upgrade tests, and a rollback plan.
- Enum unknowns must be preserved or rejected explicitly; never map unknown to a plausible default.
- A target D contract change is independent of IR schema change and must be pinned separately.

## 6. Incremental invalidation

Cache key = stable source digest + pass ID/version + input node digests + relevant config/snapshot versions + scope partition. A dependency DAG determines descendants to invalidate. A changed prompt invalidates extraction descendants; a changed resolver snapshot invalidates resolution and later passes, not raw parsing. A changed target contract invalidates lowering/commit projection only.

Authorization, PermissionEpoch, Forget Fence, retention, and visibility are live guards, not cacheable truth. Cached work must re-check them before protected dereference or publication under current Owner contracts.

## 7. Provenance loss and deletion

When source data is redacted, expired, or forgotten, preserve only the minimal permitted tombstone/lineage required by governance. The IR design must not promise immutable source retention in violation of Forget or retention policy. Missing bytes remain unavailable; never reconstruct original evidence from a summary.
