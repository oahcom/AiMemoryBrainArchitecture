# Phase 3.6.12 — Storage / C / H Exact Version Binding Manifest

- Owner perspective: Storage coordination; C and H verification inputs are recorded as exact artifacts, not impersonated approvals.
- Status: PROPOSED INTEGRATION BINDING — A FINAL REVIEW REQUIRED
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT DEPLOYED
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`

## 1. Exact artifact pins

| Role | Artifact | Exact blob | Status |
|---|---|---|---|
| Storage | COC Durable Log, Participant Registry & Recovery Protocol (contains normative §§15–17) | `5b950a3a29bd7a5276b92a49a9114d700718b987` | Fetched from Storage branch and inspected |
| Storage companion | Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` | Referenced by COC §§15.0/15.1 and prior Storage canonical binding amendment; companion file was not independently re-fetched in this pass |
| H | `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.5.schema.json` | `164ec3c436558d5d93032edc51e127d15e03db4d` | Fetched from H branch and structurally inspected |
| C | Provider Outcome / CSubmitOutcome owner artifact | NOT PINNED | C owner artifact path/blob not recovered in this pass; no exact-owner acceptance claimed |
| Historical COC source | `8ac17816476f280ab6fb3afca0688aa03e37de1d` | historical source blob | Superseded by Storage protocol §§15–17 for ordering and digest semantics |

The Storage COC file fetched from the Storage branch is blob `5b950a3a29bd7a5276b92a49a9114d700718b987`. Do not substitute the historical `8ac178...` blob as the current ordering specification. The H schema artifact revision is 1.2.5 while its protocol-family `schema_version` remains 1.2.0; these are distinct version concepts.

## 2. Normative Batch / Manifest sequence

Storage COC §§15.1–15.2 require this order:

1. I/D/C close their respective gates and freeze owner-local snapshots/high-waters.
2. Establish the exact quorum-committed COC prefix P and anti-rollback anchor.
3. Enumerate and precompute the complete canonical Participant Manifest against P; independently re-read it. This is a staged immutable payload, not yet an authoritative committed record.
4. Commit `COC_RECOVERY_CUTOFF_BATCH`, binding the stable ManifestId, manifest content digest, count, enumeration high-water, prefix and owner snapshots.
5. Commit the separate Participant Manifest record, referencing the exact preceding Batch position/digest and repeating the exact epoch/prefix/ManifestId/content digest/count/high-water.
6. Linearizably read back both records and verify the complete pair before entering participant reconciliation.
7. Reconcile each member; each owner independently issues only its own Gate Release.
8. Append `RECOVERY_EPOCH_COMPLETED` only after all required owner releases and reconciliation evidence are durable.

The API contract rejects batch append without the already computed manifest identity/digest and complete frozen owner snapshots. Manifest append is idempotent on stable batch identity plus manifest identity/digest. Lost ACK recovery must use exact-key lookup and readback, not a second identity.

## 3. Digest dependency — no circular reference

Storage COC §§16.1–16.3 distinguish:

- `ParticipantManifestContentDigest`: precomputed over the canonical immutable manifest-content projection; excludes the future Batch reference and final record proof.
- `RecoveryBatchDigest`: covers the batch payload, including ManifestId and ParticipantManifestContentDigest.
- `ParticipantManifestRecordDigest`: covers the final committed Manifest record, including exact Batch reference/digest and content digest.

Required dependency:

`ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest`

The Batch MUST NOT bind the future Manifest Record digest. The Manifest Record MUST NOT precede its Batch. Owner release and epoch completion bind the exact committed Batch and Manifest record references, positions and entry digests, as well as the appropriate content/record digest values.

## 4. H schema 1.2.5 structural verification

The exact H schema was parsed and checked for these message contracts:

- `COC_RECOVERY_CUTOFF_BATCH` requires prefix, I/D/C owner snapshots, ManifestId/digest, participant count, enumeration high-water and quorum/COC record proof fields.
- `COC_PARTICIPANT_MANIFEST` requires exact Batch reference/position/entry digest, ManifestId/digest, count, enumeration high-water and participants.
- `OWNER_GATE_RELEASE_ATTESTATION` requires exact Batch and Manifest record references, positions and entry digests, owner gate generation, request/admission high-waters, set digests and ledger roots.
- `RECOVERY_EPOCH_COMPLETED` requires exact Batch/Manifest references and digests, reconciliation root and owner release references.
- Participant union uses distinct COC participant and owner-local admission variants; an owner admission may carry an explicit nullable COC ParticipantIntentRef plus absence reason.
- C Provider Outcome message requires CSubmitOutcome identity/digest, provider outcome and evidence references, provider/adapter/idempotency identity, final request boundary and request digest, owner-admission identity/digest, owner ledger/version/sequence/high-water/root, and COC participant/absence binding.

Structural schema validation alone does not establish digest recomputation, cross-record equality, quorum ordering, signature trust, completeness, or provider side-effect truth. Those remain semantic verification requirements.

## 5. C Provider Outcome verification requirements

The C Provider Outcome contract must preserve these mutually exclusive evidence meanings:

- `INVOKED_WITH_PROVIDER_RECEIPT`: proves the provider accepted/returned a receipt for the exact final request boundary and idempotency key; it does not by itself prove durable Memory Brain visibility.
- `INVOKED_WITHOUT_RECEIPT`: proves invocation/handoff occurred but receipt is absent; provider lookup/reconciliation is required and unresolved state remains UNKNOWN.
- `NOT_INVOKED`: requires authoritative `not_invoked_proof_ref` / `provider_no_handoff_proof_ref`; absence of a request record or timeout is insufficient.
- `UNKNOWN`: requires an explicit unknown reason and must never be coerced into success or safe retry.

Provider Outcome must bind exact Provider, Adapter, idempotency key, final request boundary, request digest, transaction/participant identity and applicable I/D/Storage terminal evidence. A CSubmitOutcome record is C-owned evidence; COC batch membership is not a provider outcome, and provider outcome does not itself mint I authorization, D clearance, Storage resolution, or global completion.

Retry must be outcome-aware: after any possible handoff, do not blindly invoke again; query by stable provider idempotency identity or preserve UNKNOWN. A new provider attempt requires an explicit new attempt identity and proof that retry is safe under the provider's idempotency contract.

## 6. Blocking conditions and review boundary

1. H schema 1.2.5 is structurally consistent with the Batch-before-Manifest-record order and distinct digest chain at the field-presence level. H owner semantic acceptance and interoperability-vector execution remain pending.
2. C Provider Outcome fields are present in H schema 1.2.5, and Storage COC §16.4 assigns C the gate across the Batch/Manifest interval. C owner artifact exact blob was not located in this pass; C exact-version approval is therefore pending.
3. The Storage v3.1 companion blob is cited by the current COC protocol but was not independently fetched in this pass. A must verify that pin before freezing the bundle.
4. Any schema or protocol change creates a new exact bundle and requires affected-owner re-review.

No implementation, conformance test execution, provider sandbox verification, production activation, physical erasure, or Global Forget Completion is claimed. This document records an architecture-level exact-version binding candidate only.
