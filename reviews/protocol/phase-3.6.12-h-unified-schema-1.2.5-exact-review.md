# H — Exact-Version Structural Schema Review: COC / JF-10 Unified 1.2.5

- Owner perspective: H — Protocol & Schema
- Status: **CONDITIONAL ACCEPTANCE — SEMANTIC / INTEROPERABILITY GATES OPEN**
- Reviewed schema path: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.5.schema.json`
- Exact schema blob: `164ec3c436558d5d93032edc51e127d15e03db4d`
- Companion Storage COC protocol blob: `5b950a3a29bd7a5276b92a49a9114d700718b987`
- Storage Recovery Cutoff amendment referenced by COC: `9704d110a06d0c2ee98be960054e0396d0b68546`

## 1. Decision

**ACCEPT WITH ENUMERATED AMENDMENTS** for the structural schema mapping only. This is not a protocol freeze, signature-profile approval, semantic-validator acceptance or interoperability pass.

## 2. Verified structural coverage

The schema has distinct message shapes for:
- `COC_RECOVERY_CUTOFF_BATCH`: exact prefix, I/D/C owner snapshots, ManifestId/digest, count, enumeration high-water and quorum/COC record proof references.
- `COC_PARTICIPANT_MANIFEST`: exact preceding Batch ref/position/entry digest, ManifestId/digest, count, enumeration high-water and participant list.
- `OWNER_GATE_RELEASE_ATTESTATION`: exact Batch and Manifest record references, positions and entry digests, current owner Gate generation, separate request/admission high-waters, counts, digests and roots.
- `RECOVERY_EPOCH_COMPLETED`: exact Batch/Manifest references and digests, reconciliation root and owner release references.
- Participant membership uses two distinct variants: COC participant and owner-local admission. An unregistered owner admission can explicitly carry nullable COC ParticipantIntentRef and a non-empty absence reason.

The schema artifact revision is 1.2.5; its protocol-family `schema_version` remains 1.2.0. These must remain distinct in documentation, version pinning and compatibility checks.

## 3. Required H amendments before freeze

1. Publish semantic validators for S0a owner dual-ledger snapshot freeze before S0b prefix freeze; JSON Schema cannot enforce cross-message temporal order.
2. Validate canonical union completeness, uniqueness, exact owner-ledger roots/high-waters and scope-specific exclusions. Require every applicable COC participant and every applicable I/D/C owner admission exactly once.
3. Validate `ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest` with separate canonical projections; forbid future Manifest Record digest in Batch.
4. Validate exact Batch-before-Manifest COC positions, quorum proofs, prefix equality and linearizable S4 readback.
5. Validate outcome-dependent C Provider Outcome evidence; structural presence of proof-reference fields does not prove that a referenced proof exists, is signed by C, or matches the final request boundary.
6. Publish canonical-byte fixtures, positive/negative vectors, duplicate/replay tests, unknown-field policy and cross-language serialization vectors.
7. Clarify null-vs-absent semantics for `coc_participant_intent_ref` and `coc_absence_reason` in each participant variant; reject contradictory pairs.

## 4. Provider Outcome schema observation

The exact enum is `HANDOFF_ACCEPTED | HANDOFF_REJECTED | NOT_INVOKED | UNKNOWN | IN_DOUBT`. The C Provider Outcome message includes CSubmitOutcome identity/digest, provider and adapter identity, idempotency key, final request boundary, request digest, outcome evidence refs, owner-admission identity/digest and COC participant/absence binding. H must not redefine C's outcome semantics; C remains the semantic authority.

## 5. Non-claims

No executable validator or interoperability vector was run in this review. No cryptographic profile, schema freeze, provider exactly-once behavior, implementation conformance or production activation is accepted. The review is a role-simulated H assessment, not an independent human Owner signature.
