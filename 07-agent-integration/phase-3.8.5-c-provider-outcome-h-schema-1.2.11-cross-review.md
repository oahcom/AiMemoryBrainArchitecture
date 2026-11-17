# Phase 3.8.5 — C Exact Cross-Review of H Schema Artifact 1.2.11 / Provider Outcome

- Owner perspective: C — Agent Integration / Provider Outcome authority
- Disposition: **CONDITIONAL STRUCTURAL ACCEPTANCE; SEMANTIC AND WIRE FREEZE BLOCKED**
- Provenance: delegated C-role simulation authored at the user's direction; not an independent human C Owner signature or cryptographic signature.
- Scope: exact H schema 1.2.11 Provider Outcome record and C-owned provider boundary semantics.
- Project state: architecture design only; no provider implementation, production activation or executed adapter conformance is claimed.

## 1. Exact inputs

### C normative source set

| Artifact | Blob |
|---|---|
| Final Request Evidence Contract | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` |
| C-submit / I-authorization / D-ForgetFence causal-order contract | `45a48249717c8cddb07ab96197730ef93d406c22` |
| C owner-local admission / recovery-release amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| Provider Egress Gate Adapter contract | `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` |
| Prior C exact-owner decision (source-scoped) | `1353572f7d5655e3007b2fb5b3f10066f483e6bb` |

### H inputs

| Artifact | Blob |
|---|---|
| H schema `bmcp.coc-jf10-unified-1.2.11.schema.json` | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H semantic validator contract (Phase 3.6.10) | `4c5c3771575979061e674e40f1f5f3d9b4645bd9` |
| H prior semantic validator decision | `1de7d30f3ca81bc579b396acb0f05e2ead5fe9dd` |
| H/I crypto wire mapping (schema 1.2.8 candidate) | `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` |
| H wire interop Python test | `1a4e754ba9bfa57eb973c6d39731e9f89443b323` |
| H wire interop JS reference | `992585d3bc323dc0224d0075ef14abd992980f65` |
| H wire interop vectors | `cc7e98c729db8d9f615e17a9542b3cb63f459922` |

## 2. Structural alignment accepted

The exact 1.2.11 schema contains message type `C_PROVIDER_OUTCOME_RECORDED` and the exact outcome enum:

`HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`.

The message structurally binds:
- immutable C outcome ref and SHA-256-shaped outcome digest;
- provider, adapter and provider idempotency-key references;
- final request boundary and request digest;
- C transaction, participant intent/reservation and Storage prepare tuple references where supplied;
- provider request/receipt/evidence and same-key lookup proof references;
- C owner admission ref/digest, ledger ref/version, local sequence, high-water and ledger root;
- COC commit/record/position/digest and owner signature references;
- nullable COC ParticipantIntentRef, with an absence reason required when null and prohibited when non-null.

Outcome-dependent structural rules require:
- ACCEPTED: participant reservation, provider request, provider receipt and outcome evidence;
- REJECTED: participant reservation, provider-no-handoff proof and outcome evidence;
- NOT_INVOKED: not-invoked proof, and no provider receipt;
- UNKNOWN/IN_DOUBT: an unknown-reason reference.

This is a meaningful structural representation of C's outcome taxonomy and owner-local admission join. It is not by itself proof that referenced evidence is authentic, complete, same-attempt or semantically authoritative.

## 3. Blocking semantic gaps and required amendments

### C-PO-1 — attempt and gate-generation binding

The C adapter contract requires the final egress decision to bind the current `CGateGeneration`, immutable admission, provider attempt, exact request bytes/digest and the serialization point shared by gate close and egress commitment. The 1.2.11 outcome record has owner-local sequence/high-water and reservation/request references, but no explicit C gate-generation field or unambiguous provider-attempt identity/generation field in this message.

**Required:** add typed `c_gate_ref`, `c_gate_generation`, `provider_attempt_ref` and `provider_attempt_generation` (or publish a normative, immutable dereference contract proving these exact values are transitively bound by the referenced C admission/reservation and outcome digest). Validator must reject stale-generation, cross-attempt and request-digest mismatches.

### C-PO-2 — provider idempotency and lookup semantics

The schema carries `provider_idempotency_key_ref` and `provider_lookup_proof_ref`, but does not make the lookup proof conditionally mandatory for a resolved ambiguous attempt, nor define that it proves lookup in the same provider/account/namespace with the exact same key, attempt and immutable request digest.

**Required:** define provider/account/endpoint namespace and key retention; same-key lookup proof issuer/authenticity and lookup result; bind it to the same attempt and request digest. No retry-as-new-operation. If the provider cannot authoritatively resolve the ambiguity, retain UNKNOWN/IN_DOUBT indefinitely and keep affected gates/barriers blocking.

### C-PO-3 — outcome-specific semantic authority

The structural rules are directionally consistent but require semantic tightening:
- ACCEPTED must prove the exact immutable request crossed the actual transport/provider handoff boundary. It does not prove inference completion, Memory Brain visibility, user delivery or G Applied.
- REJECTED is valid only with authoritative rejection evidence for the exact attempt. If any external side effect may have occurred or no-handoff cannot be proven, classify UNKNOWN/IN_DOUBT, not safe rejection/retry.
- NOT_INVOKED requires authoritative proof that the exact attempt never crossed handoff; timeout, absent row, lost ACK, worker death or queue emptiness is insufficient.
- UNKNOWN/IN_DOUBT is nonterminal and must preserve the original request/attempt/key. A reason reference alone is not a terminal resolution.

### C-PO-4 — C signature profile and immutable projection

The schema requires `owner_signature_ref`; its description says protected owner-signed records require `signature_profile_id` semantically. However the fetched H/I mapping is explicitly an I-signed profile/mapping and references schema artifact 1.2.8, not a C signature projection for schema artifact 1.2.11.

**Required:** H/I/C publish an exact C owner-signature profile, key/trust authority, canonicalization, projection allowlist, domain separation, digest preimage, key version/status and anti-rollback semantics. Do not reuse I's P0 projection for C by analogy. C must sign the immutable C outcome payload and exact schema artifact revision under the agreed C profile.

### C-PO-5 — outcome record immutability and contradictory fields

The semantic validator must enforce append-only outcome identity, no mutation/overwrite by later timeout, no conflicting provider receipts, and no contradictory combinations of outcome enum, receipt, no-handoff proof, not-invoked proof, lookup proof and reservation. Corrections must be new superseding records and must preserve the original fact.

## 4. Cross-owner ordering retained

The existing C causal chain remains controlling:
1. C durable local admission and immutable final request;
2. COC ParticipantIntent registration before protected provider side effect;
3. exact I single-use authorization terminality and D lineage/ForgetFence clearance;
4. COC ParticipantReservation;
5. C transport-owning Adapter final durable CAS against current C gate generation immediately before handoff;
6. gate close and egress commitment serialize through the same durable authority;
7. C alone records immutable CSubmitOutcome from actual transport/provider observation;
8. during Recovery Cutoff, provider invocation/retry remains closed until exact S4 Batch/Manifest pair readback and semantic join.

Storage Prepared/COMMITTED, I authorization, D clearance, H ACK, COC quorum or manifest membership cannot synthesize provider truth. Storage does not release C's gate.

## 5. C disposition

**CONDITIONAL STRUCTURAL ACCEPTANCE ONLY.** H schema 1.2.11 contains the expected Provider Outcome vocabulary and the principal C/COC/owner-ledger references. C does not accept the schema as a complete semantic contract or frozen interoperable wire bundle until C-PO-1 through C-PO-5 are normatively resolved and the exact H validator/signature/fixture bundle is reviewed.

## 6. Evidence and implementation boundary

The fetched H Python/JavaScript/vector files identify themselves as HRC-TEST-v1 / recovery-cutoff 1.0.4 test-profile material. The Python helper uses sorted-key JSON serialization rather than demonstrating RFC 8785 JCS; the JS implementation is a bespoke test canonicalizer. The visible vectors cover three generic recovery/join examples, not C Provider Outcome semantics. These artifacts do not establish 1.2.11 C-provider interoperability.

No actual provider Adapter tests, crash/race tests, provider-specific idempotency proof, CI execution result for this exact 1.2.11/C-PO bundle, production deployment or universal exactly-once guarantee is claimed.

## 7. Freeze gate

C's acceptance of H 1.2.11 remains **OPEN / BLOCKED** pending:
- exact C gate-generation and provider-attempt binding;
- provider-specific same-key outcome/lookup contract;
- outcome-dependent semantic validator and contradiction vectors;
- C-specific signature/canonicalization profile aligned to schema 1.2.11;
- executed cross-language and real-Adapter conformance evidence;
- Storage manifest pin update and A final integration review.

This is a delegated architecture review record, not an independent Owner approval.
