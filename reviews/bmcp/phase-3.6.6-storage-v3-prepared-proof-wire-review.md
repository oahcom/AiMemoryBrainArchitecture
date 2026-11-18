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

**CI evidence:** initial run `43999897781` on commit `e0e4d97b65e6c6aaee5682278eac535a1c135b0b` failed with 7 schema-validation errors. The root cause was an authoring defect: a duplicate `allOf` object key overwrote the resolution payload's common/variant property schema with the conditional constraints. The corrected schema Blob is `6327d9d387bdc0d6610aba08ff3e51ca9da17f5d`, committed at `d26a40e2483e32a6afb1e8f9ccd456e8ae3c815c`. Follow-up run `44000078669`, job `133761649293`, completed **SUCCESS** on that exact commit. The workflow used Python 3.12 and pinned jsonschema 4.23.0; the compile step succeeded and `python -m unittest discover -s tests/schema -v` ran **47 tests, all PASS**. This includes 12 new Storage proof schema tests and the existing JF-10 schema/parser suites. The result is structural schema/parser reference evidence only; it is not cryptographic verification, canonical-byte interoperability, owner-authority proof, production transport or runtime conformance.

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


## 9. Cross-document and CGH wire-coverage addendum

### H-V3-06 — Storage companion §14 does not carry the complete v3 identity tuple

The exact companion protocol §14 Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7` was re-read. It carries PreparedParticipantRef, GID, native XID, canonical DB authority, cluster/database metadata, original prepare coordinates, operation/request digest, owner boundary, CausalOrderDomainRef/PolicyDomainRef and COC prepare-intent position/digest. It does not enumerate DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version or ParticipantTupleDigest as distinct required fields, while Storage v3 §§15.1–15.7 Blob `4a60420d457f359780c568dce42b8bef000026ca` does.

The new H schema implements the v3 fields, not the older §14-only tuple. Storage must amend §14 or explicitly supersede it for the v3 PostgreSQL profile. H will not treat a schema candidate as authority to silently change Storage's normative contract.

### H-V3-07 — Five H 1.1.0 JF-10 variants do not yet map every CGH-APPLIED-1.1 evidence family

A CGH-APPLIED-1.1 package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` §4 enumerates eight evidence families:
- CAUSAL_ORDER_INTENT and CAUSAL_ORDER_INTENT_RECEIPT;
- CAUSAL_ORDER_RESERVATION;
- I_AUTHORIZATION_TERMINAL;
- D_FENCE_TERMINAL;
- C_SUBMIT_OUTCOME;
- CAUSAL_ORDER_TERMINAL_PROOF;
- CAUSAL_ORDER_ACK.

The H schema candidate `bmcp.applied-ack/1.1.0` Blob `a8a945cc3623c2907003b93625e3c79742150944` has five variants only:
- JF10_PREPARE_INTENT_REGISTERED;
- JF10_PREPARED_PARTICIPANT_REGISTERED;
- I_JF10_TERMINAL_DECISION_OBSERVED;
- STORAGE_JF10_PARTICIPANT_RESOLVED;
- JF10_BRIDGE_RECONCILIATION_RECORDED.

The I terminal has a clear semantic counterpart. The current five-variant schema does not explicitly encode ParticipantReservation, DParticipantClearance/D fence terminal, CSubmitOutcome, CausalOrderTerminalProof or a distinct COC ACK. The first JF10 intent/prepared records are not automatically equivalent to the full CGH intent/reservation/terminal proof families. H must either add versioned message families or publish an exact mapping to another versioned schema/transport for every missing family. Until then, 1.1.0 is a JF-10 bridge candidate, not the complete CGH Applied wire contract.

### H-V3-08 — The Storage proof schema is a separate family, not a substitute for missing Applied messages

The new `bmcp.storage-prepared-participant-proof/1.0.0` Blob `6327d9d387bdc0d6610aba08ff3e51ca9da17f5d` defines only Storage.PreparedParticipantReceipt and Storage.StorageResolutionProof. It does not define the missing C/D/G/COC messages, and it is not referenced by the existing Applied ACK 1.1.0 schema. The exact integration must identify whether BMCP carries these proofs inline, by typed reference + digest, or as a separate proof family, and bind the selected representation to the same CausalOrderTransactionRef, ParticipantIntentRef, participant tuple, request digest and owner boundary.

The 47-test structural CI PASS remains valid for this schema's shape only. It does not close H36, CGH interoperability, signature/canonicalization, semantic joins or the complete Applied message registry.

## 10. Updated H disposition

H accepts the Storage v3 prepared-proof field shape with the enumerated amendments, and the structural schema/parser suite is 47/47 PASS. H does **not** accept the older companion §14 as equivalent to v3, does not freeze the full CGH-APPLIED-1.1 wire contract, and does not infer that the five JF-10 schema variants cover the eight CGH evidence families. Storage §14 reconciliation and a complete, version-pinned C/G/H message-family mapping remain required before G8 can close.


## 9. 2026-11-18 current Storage source and CGH wire-coverage reconciliation

### H-V3-06 — RESOLVED at current document level

The earlier H-V3-06 finding referenced companion §14 Blob `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`. The current Storage Owner branch HEAD at discovery is `268af57b099209b33835b663596e87d21bb9c22b`; its current companion §14 Blob is `dbc1dfd4c488c5d5e5a328388487d190984e8adc`. Current §14.1–14.4 explicitly carries DatabaseIncarnationRef, PrepareAttemptRef/Generation, ParticipantLedgerRef/Version and ParticipantTupleDigest, plus the exact pre-PREPARE, signed receipt, replay and recovery semantics. Storage v3.2.3 body Blob `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` §15.7 carries the matching I proof tuple. The old companion Blob is historical; no further §14 field amendment is required on the current source readback.

The Storage v3.3.2 manifest Blob `5c614375e10698e4931d83deb57d20321445e068` pins the v3.2.3 body but does not explicitly list current companion §14 Blob `dbc1dfd4c488c5d5e5a328388487d190984e8adc`. Storage/A must pin the exact companion source or a successor in the final bundle. This remains a version-binding action, not a semantic §14 gap.

### H-V3-07 — OPEN; exact Phase 3.6 message-family coverage

A's exact CGH-APPLIED-1.1 package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819` §4 requires eight causal-order evidence families. H's pinned `bmcp.applied-ack/1.1.0` schema Blob `a8a945cc3623c2907003b93625e3c79742150944` has five JF-10 variants. Current mapping assessment:

| A required family | H 1.1.0 candidate mapping | Disposition |
|---|---|---|
| CAUSAL_ORDER_INTENT | `JF10_PREPARE_INTENT_REGISTERED` contains related intent fields | Partial candidate only; not an exact distinct family mapping |
| CAUSAL_ORDER_INTENT_RECEIPT | No distinct receipt message; registration proof is only a field in the intent variant | OPEN |
| CAUSAL_ORDER_RESERVATION | No explicit reservation variant | OPEN |
| I_AUTHORIZATION_TERMINAL | `I_JF10_TERMINAL_DECISION_OBSERVED` | Direct semantic candidate; I authority/signature validation remains external to JSON Schema |
| D_FENCE_TERMINAL | No explicit D fence terminal variant | OPEN |
| C_SUBMIT_OUTCOME | C-owned `c-submit-outcome/1.0.1` schema exists (Blob `a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda`), but no H 1.1.0 transport family binds it | OPEN |
| CAUSAL_ORDER_TERMINAL_PROOF | No explicit terminal-proof variant | OPEN |
| CAUSAL_ORDER_ACK | No distinct COC ACK variant | OPEN |

The other H 1.1.0 variants—`JF10_PREPARED_PARTICIPANT_REGISTERED`, `STORAGE_JF10_PARTICIPANT_RESOLVED` and `JF10_BRIDGE_RECONCILIATION_RECORDED`—are Storage prepare/resolution and reconciliation observations; they are not substitutes for Reservation, D terminal, C submit outcome, CausalOrderTerminalProof or a distinct COC ACK.

H's later Phase 3.8 schemas `bmcp.coc-jf10-unified/1.2.17` Blob `1b8f44675f30919764481d33755c566ef5cf1ea8` and `bmcp.applied-delivery-evidence/1.0.0` Blob `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` are separate successor artifacts, not pins in A's Phase 3.6 package. They cannot be silently substituted for H 1.1.0 or transfer approvals. A must issue a successor package if it elects to adopt them, followed by exact C/G/H and D/I/B predicate re-acceptance.

### H structural test evidence and ceiling

- H branch HEAD at discovery: `0ec8be40b8fe1b8e4729334759d46da0be9b6b87`.
- Storage proof schema Blob: `6327d9d387bdc0d6610aba08ff3e51ca9da17f5d`.
- Test Blob: `f8de63379d4d411ff9c9831f25294e4c8b09f158`.
- Workflow Blob: `f9a8a403b4fd523a065c0aee6c51f3575c4270a2`.
- GitHub Actions run `44000078669`, job `133761649293`, tested commit `d26a40e2483e32a6afb1e8f9ccd456e8ae3c815c`: Python 3.12, jsonschema 4.23.0, compile succeeded, `python -m unittest discover -s tests/schema -v`: 47 tests, all PASS. The current H branch retains the same schema/test/workflow Blobs.

This is structural schema/parser evidence only. H36, CFG-01..20 and PI-01..08 remain NOT RUN. Signature verification, canonical-byte interoperability, live I/D/Storage authority callbacks, transport/channel binding and production replay durability remain unproven. H-V3-07/08 remain blockers to G8; no schema freeze is claimed.


## 10. Successor-schema reconnaissance — H Unified 1.2.17 is partial coverage, not Phase 3.6.1 adoption

A fresh read of the current H Owner branch finds `bmcp.coc-jf10-unified/1.2.17`, Blob `1b8f44675f30919764481d33755c566ef5cf1ea8`. Its exact message types are:

- `COC_RECOVERY_CUTOFF_BATCH`
- `PARTICIPANT_SET_RECONCILIATION`
- `OWNER_LOCAL_PENDING_GATE`
- `OWNER_LOCAL_GATE_RELEASE`
- `RECOVERY_EPOCH_COMPLETED`
- `JF10_PREPARE_INTENT_REGISTERED`
- `JF10_PREPARED_PARTICIPANT_REGISTERED`
- `JF10_I_TERMINAL_DECISION_OBSERVED`
- `JF10_STORAGE_PARTICIPANT_RESOLVED`
- `JF10_BRIDGE_RECONCILIATION_RECORDED`
- `C_PROVIDER_OUTCOME_RECORDED`

This successor contains useful candidate coverage absent from 1.1.0:
- `C_PROVIDER_OUTCOME_RECORDED` binds CSubmitOutcomeRef/digest, provider outcome/receipt, actual inference/final-boundary identity, request digest, transaction, participant reservation ref, I terminal, D clearance and Storage resolution proof refs.
- `OWNER_LOCAL_PENDING_GATE` / `OWNER_LOCAL_GATE_RELEASE` carry generic owner-kind gate evidence and owner-specific high-waters. They could support an I or D owner-local gate mapping only after the respective Owner confirms the exact `owner_kind`, generation, request/admission high-water and proof semantics.
- `JF10_PREPARE_INTENT_REGISTERED` carries the intent and COC commit-proof reference; `JF10_BRIDGE_RECONCILIATION_RECORDED` carries D barrier and C provider outcome references.

The successor still does not provide a distinct `CAUSAL_ORDER_INTENT_RECEIPT`, `CAUSAL_ORDER_RESERVATION`, explicit D fence terminal family, explicit `CAUSAL_ORDER_TERMINAL_PROOF` ref/family, or distinct `CAUSAL_ORDER_ACK` family. A field such as `participant_reservation_ref`, `d_barrier_evidence_ref`, `reconciliation_root` or `coc_commit_proof_ref` is not silently equivalent to a separately required message family.

H also has `bmcp.applied-delivery-evidence/1.0.0`, Blob `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608`, with one `APPLIED_DELIVERY_EVIDENCE_RECORDED` message. It is a separate Phase 3.8 evidence schema, not a replacement for the eight Phase 3.6 causal-order families.

**Disposition:** H 1.2.17 is a promising successor mapping source, but it is not pinned by A's CGH-APPLIED-1.1 package (which names H 1.1.0). A must publish a successor package/version decision before this schema can be considered for G8. C/G/H must accept the same successor digest; D/I/B must confirm their predicates; H must add explicit missing families or a signed/typed exact mapping. No prior acceptance transfers, and no contract freeze is claimed.
