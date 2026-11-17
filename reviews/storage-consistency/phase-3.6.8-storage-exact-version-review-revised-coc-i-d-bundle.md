# Phase 3.6.8 — Storage Exact-Version Review of Revised COC / I / D Bundle

- Reviewer role: Storage / Consistency (delegated role simulation)
- Decision date: 2026-11-17
- Decision: **ACCEPT — RECOVERY BATCH / MANIFEST ORDERING ALIGNED; JOINT FREEZE STILL BLOCKED**
- Storage Design v3.1 exact Blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- Revised COC protocol exact Blob: `a07a8d352f31d5406786e1cd8ecddd4065ec384a`
- Storage ordering amendment exact Blob: `9704d110a06d0c2ee98be960054e0396d0b68546`
- Storage canonical-version / participant identity correction: `dd1b30eca08cea16f2d3ef1556ffb1a61d0f181f`
- I revised source Blob: `cf4b76f151204fa47b156b5d807e7378c28fd268`
- D revised source Blob: `2d95099a2e19a8cbec325925b70da576f73d9899`
- C provider outcome contract: `f538d921d06c92dfaba13fbe326a80d6550fe1b7`
- H revised two-phase addendum: `c216853412f654d92e2890ddcc2dffc12406cbe6`
- H Recovery Cutoff schema 1.0.5: `3d451778b9867c3b54779c5cd478522993719025`

## 1. Decision summary

Storage confirms that COC §15–16 now resolves the exact ordering conflict previously identified between Storage v3.1 §§5.2–5.6 and COC base §6.2.

**Storage ACCEPTS the revised COC ordering and digest contract as semantically aligned with Storage Design v3.1.** No further Storage-local amendment is required for the Recovery Cutoff Batch / Participant Manifest ordering defect.

## 2. Exact ordering review

| Required property | Storage v3.1 | Revised COC | Result |
|---|---|---|---|
| Owner-local gate close and high-water capture before recovery set freeze | §5.2 | §15.1 step 1 | ALIGNED |
| Exact quorum-confirmed prefix P | §5.3 | §15.1 step 2 | ALIGNED |
| Complete participant enumeration and manifest precomputation before Batch | §5.3–5.4 step 1 | §15.1 step 3 / §15.4 | ALIGNED |
| Batch binds ManifestId, content digest, count and enumeration high-water | §5.4 step 2 | §15.1 step 4 / §16.2 | ALIGNED |
| Separate Manifest Record commits after Batch and back-references exact Batch | §5.4 step 3 | §15.1 step 5 / §16.2–16.3 | ALIGNED |
| Linearizable readback of both records before participant reconciliation | §5.4 step 4 | §15.1 step 6 / §16.3 | ALIGNED |
| Three distinct digest projections | implied by exact batch/manifest cross-binding | §16.1–16.2 | ALIGNED / EXPLICIT |
| Crash after Batch but before Manifest leaves system fenced and resumes same identity | §5.4 | §15.3 | ALIGNED |
| Late owner request requires next batch or authoritative out-of-scope proof | §5.6 | §15.3 | ALIGNED |
| UNKNOWN/mismatch prevents release and serving | §§5.4–5.5 | §§15.3, 16.3 | ALIGNED |

The key distinction is explicit: immutable manifest content is prepared before Batch; the quorum-committed Manifest Record is appended after Batch; the pair is linearly read back before reconciliation/release. "Manifest before Batch" must never be interpreted as committing the final manifest record before its batch back-reference exists.

## 3. Digest and wire consistency

COC §16 and H schema 1.0.5 correctly separate:
- ParticipantManifestContentDigest: precomputed canonical content projection;
- RecoveryBatchDigest: committed batch payload including ManifestId/content digest;
- ParticipantManifestRecordDigest: final committed manifest record including BatchId/BatchDigest backlink.

The required dependency is ContentDigest → BatchDigest → ManifestRecordDigest. No circular dependency is introduced. Owner release and RecoveryEpoch completion bind both manifest digests; the Batch does not contain the future record digest.

H owns exact wire spelling/schema/canonicalization. I owns cryptographic trust policy. Storage does not select either.

## 4. Cross-owner observations

- I revised source cf4b76f... now binds the exact batch/manifest refs and shared reconciliation attempt identity.
- D revised source 2d95099... binds the same attempt identity, I currentness and C-owned provider outcome references.
- C contract f538d9... correctly blocks provider invocation until exact Batch/Manifest pair readback and requires C-owned provider evidence.
- H addendum c216853... and schema 1.0.5 encode the two-phase digest and semantic join rules.
- Storage canonical-version correction dd1b30... remains part of the exact participant identity provenance bundle.

## 5. Remaining blockers — not waived

1. I cryptographic/key lifecycle profile remains separately versioned and unapproved.
2. H semantic validators and cross-implementation canonical-byte fixtures are specified but not demonstrated as passing.
3. C provider-specific same-key lookup/idempotency, durable outcome recovery and adapter crash/failover conformance remain unproven.
4. The full exact I/D/Storage/COC/C/H bundle still requires A final integration acceptance.
5. JF-10 runtime P0 remains open; Multi-PolicyDomain atomicity remains blocked; no production activation is authorized.

## 6. Conformance boundary

This is an architecture-level exact-version review. It does not claim that the crash/retry, batch/manifest, provider or cross-owner vectors have been executed. The two-record protocol and its conformance cases remain **SPECIFIED / NOT EXECUTED**.

## 7. Final disposition

**ACCEPT — Storage v3.1 §5.2–5.6 and revised COC §15–16 are aligned for the Recovery Cutoff Batch / Participant Manifest sequence.**

This closes the previously identified Storage/COC drafting-order conflict at the specification level. It does not grant joint freeze, implementation PASS, deployment or production activation.

## 8. Provenance

Assistant-authored delegated Storage role review at the user's direction. It is not an independent human Storage Owner signature or approval.