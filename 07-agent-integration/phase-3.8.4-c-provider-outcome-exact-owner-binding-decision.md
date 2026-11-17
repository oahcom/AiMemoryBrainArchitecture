# Phase 3.8.4 — C Provider Outcome Exact-Owner Binding Decision
# C Provider Outcome 精确 Owner 版本绑定裁决

- Owner perspective: C — Agent Integration / Actual Provider Submit Boundary
- Decision mode: delegated C-role exact-version review at the user's direction
- Decision: **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**
- Status: architecture/interface semantics accepted; implementation, provider conformance and production activation OPEN
- Branch snapshot reviewed: `session-c-agent-integration-2026-11-16`
- Reviewed branch HEAD: `afacd82a4bf03118f40cd010bff6060837132985`
- Provenance: assistant-authored role simulation; not an independent human C Owner signature.

## 1. Exact C-owned source bundle / C 所有规范源

The canonical C Provider Outcome authority is not a single standalone file. It is the following composable C-owned normative source set. The review artifacts below corroborate the composition but are not substituted for the source contracts.

| Role | Exact path | Blob SHA | Function |
|---|---|---|---|
| C final-request evidence | `07-agent-integration/phase-3.6-final-request-evidence-contract.md` | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | Immutable final request identity, boundary and submission evidence |
| C causal submit contract | `07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md` | `45a48249717c8cddb07ab96197730ef93d406c22` | CSubmitOutcome ownership, I/D/COC order and terminal evidence |
| C owner-local admission/recovery amendment | `07-agent-integration/phase-3.6.9-c-owner-local-admission-gate-recovery-release-amendment.md` | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` | C admission ledger, gate close, provider attempts and recovery release |
| C concrete Provider Egress Gate Adapter contract | `07-agent-integration/provider-egress-gate-adapter-contract.md` | `a8d1cfc4d2171c9b0a0ced10e53fc6b110479aca` | Final transport-owning Adapter CAS, gate/send race and physical egress rules |

Exact C review evidence:
- Phase 3.6.11 Provider Outcome × Recovery Batch/Manifest review: `07-agent-integration/phase-3.6.11-c-exact-version-provider-outcome-recovery-review.md`, Blob `19519a9dabe8aea66897c01493ab5b65ed8af4aa`.
- Phase 3.8.2 RecoveryJoin / provider-side-effect review: `07-agent-integration/phase-3.8.2-c-recovery-join-provider-side-effect-exact-review.md`, Blob `a7b57bd5531222559666f0f1d9df59a259cde61a`.
- Phase 3.8.3 exact review of the Adapter contract: `07-agent-integration/phase-3.8.3-c-provider-egress-gate-exact-review.md`, Blob `5a27f79087d3a5e01dd23e818d8c7ea0fdb61d1d`.

The source files and review files were located in the recursive Git tree of the exact C branch HEAD above and fetched by exact Blob SHA. The former “C source artifact not located” statement in the Storage manifest is superseded by this discovery.

## 2. C decision / C 裁决

**ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS** for the C Provider Outcome semantic source set and its composition with the C owner-local admission/recovery and concrete egress Adapter contracts.

C is the sole authority that creates immutable `CSubmitOutcome` from actual provider/runtime boundary observation. No I authorization receipt, D clearance, Storage prepared/committed result, COC intent/reservation/Batch/Manifest, H ACK/schema validity, or G Applied record can synthesize provider truth.

The accepted outcome semantics are:
- `HANDOFF_ACCEPTED`: exact final request handoff/acceptance is authoritatively established for the bound provider, adapter, idempotency key, request digest and final request boundary. It does not prove model execution, correctness, user delivery, durable Memory Brain visibility or G Applied.
- `HANDOFF_REJECTED`: authoritative rejection for the exact request. It is not interchangeable with `NOT_INVOKED`; if external side effect may have occurred, preserve `UNKNOWN/IN_DOUBT`.
- `NOT_INVOKED`: C-authoritative proof that the provider boundary was never crossed. Timeout, missing row, lost ACK, worker crash, queue emptiness or absence of receipt is insufficient.
- `UNKNOWN` / `IN_DOUBT`: nonterminal, durable and blocking. Preserve the same attempt, request digest and provider idempotency identity; do not retry as a new operation.

Every outcome must be bound to the exact C admission and provider attempt, Provider/Adapter identity, provider idempotency namespace/key, immutable final request boundary and digest, C ledger/version/sequence/high-water/root, applicable COC ParticipantIntent/Reservation or explicit null plus reason, actual provider receipt/lookup evidence, and applicable I/D/Storage/PreparedParticipant tuple. Late evidence is append-only enrichment of the same attempt lineage.

## 3. Gate and recovery composition / Gate 与恢复组合

The accepted order is:

1. C durable owner-local admission and exact immutable request binding.
2. COC ParticipantIntent registration before protected provider side effect.
3. Exact I single-use authorization terminality and D lineage/fence clearance.
4. COC ParticipantReservation bound to the same operation and digest.
5. The transport-owning C Adapter performs the final durable CAS against current `CGateGeneration`, admission/reservation/attempt and exact request digest immediately before transport handoff.
6. Gate close and final egress commitment serialize through the same durable authority: close-first means zero provider bytes; egress-first is captured as an in-flight attempt.
7. C records immutable CSubmitOutcome from actual provider observation and publishes the exact terminal evidence.
8. During Recovery Cutoff, C's provider invocation/retry gate remains closed through Batch and Manifest commit until S4 linearizable readback and semantic join succeed.

An ambiguous send may only be reconciled through authoritative same-key provider lookup on the same immutable request/attempt. A provider without authoritative same-key recovery may leave the operation IN_DOUBT indefinitely. Generic exactly-once is not assumed.

## 4. Cross-owner exact bundle boundary / 跨 Owner 精确版本边界

This C decision composes with, but does not replace, the following reviewed inputs:
- Storage ordering amendment v3.2.2: Blob `9704d110a06d0c2ee98be960054e0396d0b68546`.
- Integrated Storage COC protocol §§15–17: Blob `5b950a3a29bd7a5276b92a49a9114d700718b987`.
- H unified schema 1.2.5: Blob `164ec3c436558d5d93032edc51e127d15e03db4d` (structural mapping only; do not infer that this is the latest H schema revision).
- H schema 1.2.7 signature-profile amendment referenced in C review Blob `ce191163deb4fea2acf1ac53ebbe3b4fc90acabf`; its current schema/validator bundle must be separately pinned by A/H before a new cross-owner freeze.
- C Provider Egress Gate exact review Blob `5a27f79087d3a5e01dd23e818d8c7ea0fdb61d1d`.

C confirms the COC Batch/Manifest pair is ordering and membership evidence only. It does not prove provider handoff or provider outcome. C's own owner-local ledger must account for all protected admissions, including admissions with no COC ParticipantIntentRef, and must be joined without fabricating a COC participant.

## 5. Enumerated C-owned exceptions / C 自有例外

1. Provider-specific idempotency namespace, retention horizon, same-key lookup authority, receipt authenticity and definitive no-handoff semantics must be established per production provider.
2. Durable C Gate/ledger serialization across crash, process restart, multi-replica failover and restore remains unimplemented/unverified.
3. C-PO, C-RJ, C-CO and Provider Egress race/fault vectors remain specified evidence unless separately shown executed against the real transport/provider Adapter.
4. H semantic validator, canonical-byte fixtures, signature-profile trust and cross-language interoperability require exact current H artifacts and execution evidence.
5. I/D currentness, revocation and fence semantics remain I/D-owned; C validates exact operation-bound proofs and does not compare unrelated owner counters.
6. No provider integration, executable Adapter conformance, production activation, universal exactly-once, Full Applied, inference correctness or Global Forget Completion is claimed.

## 6. Final status / 最终状态

The C source contract set is now exactly located and pinned. The C semantic decision is **ACCEPT WITH ENUMERATED C-OWNED EXCEPTIONS**. The previous blocker “canonical C Provider Outcome source not located” is closed as a document-discovery issue, but provider-specific proof, implementation, H current-schema alignment and A final integration review remain open.

This is a delegated role-simulated architecture decision authored at the user's direction. It is not an independent human Owner signature, cryptographic signature, test result or production authorization.


## 7. Addendum — H current-head discovery after C decision / H 当前版本发现后的补充

A subsequent exact read of H branch `session-h-bmcp-protocol` resolved its current HEAD to `80ba6748f4c7442f162102a30cfefacefdec0db9`. Its current recursive tree contains schema artifact `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.11.schema.json`, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`. The schema declares artifact revision 1.2.11 and on-wire protocol-family version 1.3.0, retains the typed union of COC participants and I/D/C owner-local admissions, and retains Provider Outcome enum support.

C has not yet completed a semantic exact-version rereview of H schema 1.2.11 together with the matching H semantic validator, signature/canonicalization profile, canonical-byte fixtures and interoperability vectors. Therefore the ACCEPT decision above remains limited to the exact C-owned source set and the previously reviewed H mapping; it MUST NOT be read as C acceptance of H 1.2.11 or as a current cross-owner wire freeze. A new C/H exact-bundle review is required before freeze.

This addendum changes no C-owned outcome authority and does not relax any C exception or implementation gate.
