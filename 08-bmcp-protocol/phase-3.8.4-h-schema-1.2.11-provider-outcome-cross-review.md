# Phase 3.8.4 — H Exact Review of Schema Artifact 1.2.11 / C Provider Outcome

- Owner perspective: H — BMCP Protocol / Interoperability Architect
- Disposition: **STRUCTURAL SCHEMA ACCEPTED AS A CANDIDATE; SEMANTIC/WIRE FREEZE BLOCKED**
- Provenance: delegated H-role simulation authored at the user's direction; not an independent human H Owner signature.
- Status: PROPOSED review record; NOT FROZEN / NOT IMPLEMENTED.

## 1. Exact reviewed artifacts

| Artifact | Exact Blob |
|---|---|
| H unified schema artifact 1.2.11 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H semantic validator contract, Phase 3.6.10 | `4c5c3771575979061e674e40f1f5f3d9b4645bd9` |
| H prior semantic validator decision | `1de7d30f3ca81bc579b396acb0f05e2ead5fe9dd` |
| H/I crypto wire mapping (schema 1.2.8 candidate) | `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` |
| H Python interop test | `1a4e754ba9bfa57eb973c6d39731e9f89443b323` |
| H JS reference | `992585d3bc323dc0224d0075ef14abd992980f65` |
| H interop vectors | `cc7e98c729db8d9f615e17a9542b3cb63f459922` |
| C Provider Outcome source set | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b`, `45a48249717c8cddb07ab96197730ef93d406c22`, `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb`, `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` |

## 2. Structural schema review

Schema 1.2.11 identifies artifact revision 1.2.11 and wire protocol-family version 1.3.0. It adds `schema_artifact_revision` to the common envelope description so protected signatures can bind the exact artifact revision as well as the wire family version. The schema retains typed COC participant / owner-local admission union members and the distinct manifest digest model.

The `C_PROVIDER_OUTCOME_RECORDED` message contains:
- CSubmitOutcome ref and 64-hex digest;
- five exact provider outcomes: HANDOFF_ACCEPTED, HANDOFF_REJECTED, NOT_INVOKED, UNKNOWN, IN_DOUBT;
- provider, adapter, idempotency-key, request and receipt references;
- final request boundary and request digest;
- transaction, participant intent/reservation and optional Storage prepare tuple references;
- provider outcome, same-key lookup, no-handoff, not-invoked and unknown-reason evidence references;
- C owner admission ref/digest, ledger/version/local sequence/high-water/root;
- COC commit/record/position/digest, owner signature and nullable ParticipantIntentRef with conditional absence reason.

The schema has useful conditional required-field rules for all five outcome classes. This is a structural candidate, not semantic proof of referenced evidence, issuer authority, signature correctness, completeness or external provider truth.

## 3. Blocking H-owned semantic and interoperability gaps

### H-1 — exact validator contract is not yet version-aligned

The fetched Phase 3.6.10 validator contract is a proposed validation contract whose source table and examples are anchored to earlier recovery schema/COC revisions. The fetched H exact-version decision accepts the 1.0.4 recovery schema direction and explicitly says it does not freeze the schema, select cryptography or prove interoperability. Neither artifact is an exact semantic acceptance of schema artifact 1.2.11 / wire family 1.3.0.

**Required:** publish a 1.2.11-specific semantic validator contract and decision. It must define C Provider Outcome validation, all cross-record joins, exact schema artifact revision binding, canonical bytes, signatures, authority, anti-rollback, and INVALID versus UNKNOWN behavior.

### H-2 — cryptographic mapping mismatch

The fetched H/I mapping explicitly names H schema artifact 1.2.8 and wire family `schema_version=1.2.0`; it specifies I's projection and I profile only. It is not a C owner-signature mapping and is not pinned to 1.2.11 / wire family 1.3.0.

**Required:** publish a current H envelope/canonicalization mapping for 1.2.11 and an owner-specific C signature projection/profile. I remains owner of I's algorithm/trust decisions; H must not infer C's signing profile from I's profile.

### H-3 — test profile is not production JCS or C Provider Outcome conformance

The fetched Python and JS artifacts explicitly call themselves test-profile material for recovery-cutoff 1.0.4 / HRC-TEST-v1. Python uses sorted-key `json.dumps`; JS implements a bespoke recursive canonicalizer. Neither demonstrates RFC 8785 JCS or the exact signature projection. The three visible vectors cover generic UTF-8/recovery join, empty-versus-absent and opaque-GID examples; they do not exercise C Provider Outcome proof rules, gate-generation races, same-key lookup or outcome contradictions.

**Required:** add 1.2.11 canonical-byte and signature fixtures plus positive/negative C Provider Outcome vectors, run independent Python/JavaScript (or other declared language) implementations, and publish reproducible execution/CI evidence pinned to exact blobs.

### H-4 — schema-level gaps remain semantic obligations

The schema exposes a provider lookup proof reference but does not itself establish same provider/account/key namespace, same attempt and same request digest. It cannot prove provider receipt authenticity or no-handoff semantics. It also does not, by structure alone, prove C gate generation or provider-attempt generation is bound to the outcome. H semantic validation must dereference the C-owned admission/reservation/attempt evidence and compare all typed identities and digests.

### H-5 — envelope and owner signature requirements

The schema description says protected owner-signed records semantically require `signature_profile_id`. H must define exact behavior for 1.2.11 artifact revision 1.2.11 and wire family 1.3.0, reject downgrade/missing profile for protected records, and pin canonicalization, digest domain separation, key ID/version/status, signature projection and anti-rollback. C's signature projection is C-owned and cannot be substituted with I's P0 projection.

## 4. H disposition

**STRUCTURAL SCHEMA ACCEPTED AS A CANDIDATE; SEMANTIC/WIRE FREEZE BLOCKED.** The current schema contains a coherent typed Provider Outcome envelope, but the fetched validator, crypto mapping and visible interop fixtures are not a matching exact 1.2.11/C-PO bundle. H therefore does not declare a current cross-owner wire freeze or interoperability acceptance.

## 5. Required next H deliverables

1. H semantic validator contract and decision pinned to schema 1.2.11 / wire family 1.3.0.
2. C Provider Outcome conditional validation, evidence dereference, cross-ledger joins, stale/currentness and INVALID/UNKNOWN semantics.
3. Exact H envelope profile plus C-specific owner signature profile/projection and key/trust binding.
4. Canonical-byte, digest, signature and C outcome fixtures; duplicate-key, null/absent, unknown critical fields and downgrade tests.
5. Cross-language conformance and real C Adapter fault/race execution reports, each tied to exact commit/blob and test environment.

No test execution, production readiness, provider-specific exactly-once, deployment or Full Applied/Forget Completion is claimed.
