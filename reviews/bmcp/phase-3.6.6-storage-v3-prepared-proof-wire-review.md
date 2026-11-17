# H — Exact Wire Review of Storage COC Protocol v3 / Prepared Participant Proofs

- Owner boundary: H — BMCP Protocol
- Branch: session-h-bmcp-protocol
- Exact Storage v3 target: commit db226387b0f2dede30a32a19a1478136b368cc1e, Blob 4a60420d457f359780c568dce42b8bef000026ca
- Companion Storage prepared-participant source: Blob 86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7
- B v3 type reconciliation: commit 5e8c0a3fc974bf08de5485925a94ebee31957068, registry Blob 4970a156aa33737d7e62cdaebbe2419d425438f2
- I v3 security review: commit 0323919be6938b0584d34b991fe185023d6a9e85, Blob 4645eb5de1732a1c78980d913a5d8d6326732923
- Prior H 1.1.1 candidate reviewed: Blob c0bbfc7611a8d88a39cee209831db32b62601fde
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS — PREPARED-PROOF SHAPE ONLY; NO FULL BMCP / CRYPTOGRAPHIC FREEZE**

## 1. H-owned artifacts added in this review

| Artifact | Blob | Purpose |
|---|---|---|
| 08-bmcp-protocol/schemas/bmcp.storage-prepared-participant-proof-1.0.0.schema.json | 6327d9d387bdc0d6610aba08ff3e51ca9da17f5d | Candidate strict schema for Storage.PreparedParticipantReceipt and Storage.StorageResolutionProof |
| tests/schema/test_storage_prepared_participant_proof_schema.py | f8de63379d4d411ff9c9831f25294e4c8b09f158 | Structural positive/negative JSON Schema tests |
| .github/workflows/jf10-bridge-schema.yml | f9a8a403b4fd523a065c0aee6c51f3575c4270a2 | Adds the candidate schema suite to the existing pinned jsonschema CI harness |

The new proof schema is separate from Applied ACK 1.1.1; it does not silently reinterpret the existing Applied wire version.

## 2. Exact type and field mapping

The candidate schema requires distinct fields for:
- PreparedParticipantRef;
- PreparedTransactionGID (PostgreSQL client-chosen ASCII GID, max 200 characters);
- PostgreSQLNativeXID (engine-assigned unsigned numeric evidence, observed after PREPARE);
- CanonicalAuthorityDBRef and DatabaseIncarnationRef;
- PostgreSQLSystemIdentifier and PostgreSQLDatabaseOID;
- immutable original prepare timeline/LSN;
- PublicationOperationId, RequestDigest and ParticipantTupleDigest;
- owner boundary, CausalOrderDomainRef and PolicyDomainRef;
- COC prepare-intent position/digest;
- PrepareAttemptRef and PrepareAttemptGeneration;
- ParticipantLedgerRef and ParticipantLedgerVersion.

H uses the full PostgreSQL-prefixed type names in the v3 wire candidate. It does not coerce PostgreSQLNativeXID into PreparedTransactionGID or the engine-neutral EngineNativeTransactionXIDRef. The B registry remains the semantic authority for these nominal distinctions.

## 3. PreparedParticipantReceipt wire boundary

The schema requires a signed-envelope shape with payload type/version, issuer principal, subject, owner authority, audience, target environment, purpose, key ID/version, algorithm/canonicalization/digest profile references, issued-at audit timestamp, trust-status evidence, payload digest and signature bytes.

The payload requires the complete Storage tuple and the PREPARED state plus authoritative writable-primary readback source. A driver/command ACK cannot satisfy the required observation-source value.

The schema does not verify the signature, key status, payload digest preimage, subject-to-participant equality or Storage registry authenticity. Those require the I-approved profile and semantic verifier.

## 4. StorageResolutionProof state mapping

The candidate keeps Storage outcome separate from I terminal outcome:

| Storage resolution | Permitted I terminal outcome | Required Storage evidence |
|---|---|---|
| COMMITTED | COMMIT_WON only | Same-GID resolution, VisibilityPointer transaction, PublicationReceipt and atomic publication transaction |
| ROLLED_BACK | REVOCATION_WON or INDETERMINATE_ABORTED | Same-GID resolution and authoritative non-publication proof |
| UNKNOWN | UNKNOWN or PENDING | NOT_VISIBLE, locks RETAINED, explicit unknown reason; no terminal visibility/non-publication assertion |

ABORT_WON is intentionally rejected because it is not in the current I terminal vocabulary. The schema also keeps original prepare coordinates distinct from append-only recovery observations.

## 5. H adversarial findings / remaining blockers

### H-V3-01 — Recovery Cutoff Batch and Participant Manifest wire families are not yet encoded

Storage v3 §5 requires owner request-set attestations, high-water/gate generations, exact COC prefix/root, immutable batch and manifest cross-binding, explicit empty-set proof, and RECOVERY_EPOCH_COMPLETED. The new schema covers only Storage prepared-participant receipts/resolution proofs. H must still publish exact schemas for:
- COC_RECOVERY_CUTOFF_BATCH;
- PARTICIPANT_SET_RECONCILIATION / immutable participant manifest;
- I/D owner pending and release attestations;
- per-fence D lineage membership/completeness proof;
- RECOVERY_EPOCH_COMPLETED.

Until these are version-pinned and semantically joined, H does not approve the complete v3 recovery wire protocol.

### H-V3-02 — Cross-field and cross-message validation remains required

JSON Schema cannot prove:
- signature input covers the exact canonical header and payload;
- signature issuer/subject/audience/purpose is authorized at signing time;
- envelope subject equals payload PreparedParticipantRef;
- payload_digest equals the exact canonical payload bytes;
- one participant/attempt/ledger tuple is immutable across Receipt, I terminal and ResolutionProof;
- same GID lookup is scoped to CanonicalAuthorityDBRef + DatabaseIncarnationRef;
- a later recovery observation appends without rewriting original prepare coordinates;
- I and Storage authoritative lookups agree on the exact immutable tuple.

A semantic validator must perform these checks against authenticated owner lookups. No such production validator is claimed here.

### H-V3-03 — I cryptographic profile is not approved

The schema carries profile identifiers but does not select an algorithm, canonicalization, key custody, issuer trust or historical verification rule. I must approve the security profile; H must then freeze the exact canonical bytes, domain-separated signature preimage and verification error taxonomy against that same profile. The I candidate proposal is not an effective governance approval.

### H-V3-04 — Requiredness and version boundary

The candidate uses non-null required fields and rejects unknown properties in version 1.0.0. Future non-critical extensions require an explicit versioned extension policy; unknown or unsupported security-critical fields and any downgrade that omits a required field fail closed. Existing Applied ACK 1.1.0/1.1.1 schemas remain separate candidate versions.

### H-V3-05 — A §11/§12 applicability and recovery mapping

The schema does not infer that the earlier H §12.9 recovery-batch mapping automatically applies to the current A §11/§12. A and H must pin one exact A package and explicitly bind each batch/manifest field to the current owner contract. No semantic-similarity inference is accepted.

## 6. CI / test evidence boundary

The new tests are wired into the existing H workflow with Python 3.12 and jsonschema 4.23.0. The expected assertions cover schema self-validation, valid Receipt and all three Storage outcomes, required identity/attempt/ledger fields, GID/native-XID separation, DB metadata formats, authoritative PREPARED observation, COMMIT_WON-only commit, rollback/non-publication, UNKNOWN lock retention, envelope requiredness, downgrade rejection and original-vs-recovery coordinates.

**Execution status at publication: NOT RUN.** A real GitHub Actions run must be fetched and reviewed before reporting PASS/FAIL. Even a passing structural suite is not cryptographic, interoperability, owner-authority or production conformance.

## 7. A G0–G10 disposition

- G4: supports H's technical wire-shape reconciliation only; does not alter BIH36-JD-01..17.
- G5: remains BLOCKED on external I36-GOV approvals.
- G6: remains BLOCKED/PARTIAL; this is not downstream C/D/E/F/G/Storage consumer acceptance.
- G7: H36 and I36 remain NOT RUN; the new schema suite is supplemental and cannot substitute.
- G8: remains BLOCKED; this is not the common C/G/H Applied contract or same-version owner/predicate acceptance.
- G9: remains NOT RUN.
- G10: remains BLOCKED.
- JF-10 P0 remains OPEN; no production activation or schema freeze is claimed.

## 8. Provenance

This is an H-role technical wire review prepared by the delegated B/I/H joint developer session at the user's direction. It is not an independently authenticated human signature. The schema and tests are candidates, not a production transport or cryptographic implementation.
