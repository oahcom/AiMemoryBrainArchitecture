# Phase 3.6.8 — H Exact-Version Review: Unified COC / JF-10 / Provider Outcome Schema

- Owner perspective: H — BMCP Protocol & Adapter Authentication
- Status: **ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS — SCHEMA CANDIDATE, NOT FROZEN**
- Storage v3.2 Blob: `e7ab80cdf8af5e0d50c407b06a5deb618d1e2ae6`
- Companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- C exact Provider Outcome review Blob: `f538d921d06c92dfaba13fbe326a80d6550fe1b7`
- C source contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- H source identity/protected-operation contract Blob: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- Prior five-family JF-10 schema candidate Blob: `a8a945cc3623c2907003b93625e3c79742150944`
- Unified schema v1.2.0 predecessor Blob: `8eb2d28701483b1e49cfb55c954ec4adfa54f3b4`
- Unified schema v1.2.1 Blob: `746d66aa231af1ef2f7c3571dbc31c46e28b2547`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED

## 1. H authority and exact-version disposition

H owns BMCP message envelope, wire schema/version, serialization/canonicalization contract, Adapter transport/authentication binding, ACK transport and reconnect framing. H does not mint I authorization, D Forget clearance, Storage resolution, C Provider Outcome or G Applied.

**H DECISION: ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS** for the Storage v3.2 + companion COC §14 + C Provider Outcome contract, limited to H's wire representation and protocol validation responsibilities.

H publishes the unified Draft 2020-12 schema candidate:
- Path: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.1.schema.json`
- Blob: `746d66aa231af1ef2f7c3571dbc31c46e28b2547`
- Commit: `3cf911dd33a098c06d895935652e2ba91655ced7`
- Schema ID/version: `bmcp.coc-jf10-unified/1.2.1`
- Message variants: 11.

Schema 1.2.1 supersedes H's 1.2.0 candidate for this combined COC/Provider Outcome bundle. The earlier `bmcp.applied-ack/1.1.0` schema remains historical evidence for its five JF-10 message families only; it is not the complete unified schema for the v3.2 recovery protocol.

## 2. Unified message-family coverage

The v1.2.1 schema contains these 11 discriminated message variants:

1. `COC_RECOVERY_CUTOFF_BATCH`
2. `PARTICIPANT_SET_RECONCILIATION` (the separately committed Participant Manifest Record)
3. `OWNER_LOCAL_PENDING_GATE`
4. `OWNER_LOCAL_GATE_RELEASE`
5. `RECOVERY_EPOCH_COMPLETED`
6. `JF10_PREPARE_INTENT_REGISTERED`
7. `JF10_PREPARED_PARTICIPANT_REGISTERED`
8. `JF10_I_TERMINAL_DECISION_OBSERVED`
9. `JF10_STORAGE_PARTICIPANT_RESOLVED`
10. `JF10_BRIDGE_RECONCILIATION_RECORDED`
11. `C_PROVIDER_OUTCOME_RECORDED`

The schema supplies a shared authenticated envelope and typed fields for COC position/digests, RecoveryEpoch, prefix P, owner snapshot attestations, ManifestId/Digest/count, PreparedParticipant GID/DB incarnation/attempt/ledger tuple, I terminal decision, Storage resolution and C Provider Outcome. COC commit proof and owner signature are separate fields; neither substitutes for the other.

## 3. H validation of Storage v3.2 Batch/Manifest ordering

H accepts the S0–S4 sequence as the normative protocol order:

- S0: close/freeze owner gates and capture owner snapshots; freeze quorum prefix P.
- S1: construct the immutable canonical Participant Manifest payload and digest. Staging is not a COC commit.
- S2: quorum-commit `COC_RECOVERY_CUTOFF_BATCH`, binding exact P, RecoveryEpoch, I/D/C owner snapshots and ManifestId/Digest/count.
- S3: quorum-commit the separate `PARTICIPANT_SET_RECONCILIATION` Manifest Record, referencing the exact preceding Batch position/digest and carrying the exact canonical member payload.
- S4: linearly read back both records and validate all cross-bindings before participant recovery/reconciliation.

The non-circular digest rule is accepted: ManifestDigest covers the canonical manifest payload + P + RecoveryEpoch, but excludes the later Batch record back-reference; the Manifest Record envelope carries the exact Batch position/digest. BatchPosition and ManifestRecordPosition are compared only inside the single COC log namespace.

H requires a semantic validator in addition to JSON Schema to enforce:
1. BatchPosition < ManifestRecordPosition and both quorum proofs valid;
2. RecoveryEpoch and prefix P equality across the pair;
3. ManifestId/Digest/count/enumeration-high-water equality;
4. canonical payload digest equality, unique ParticipantIntentRef membership, deterministic ordering, explicit empty array, and count == member-array length;
5. exactly one authenticated I, D and C owner snapshot attestation, with no duplicate owner role;
6. each owner gate generation/high-water remains current and no post-freeze admission crossed the closed gate;
7. no participant recovery, Storage resolution, provider invocation/retry, visibility publication, owner Gate release or serving before S4 succeeds.

JSON Schema cannot prove quorum commitment, cross-record equality, array length against a separate count, owner snapshot uniqueness by semantic role, canonical digest preimage, or ordering between records. Those checks are mandatory runtime protocol-validator responsibilities, not optional documentation.

## 4. C Provider Outcome wire validation

H accepts C's separation of actual provider handoff from I, D, Storage, COC, H and G facts. The `C_PROVIDER_OUTCOME_RECORDED` message carries CSubmitOutcomeRef/digest, provider identity/adapter, stable provider idempotency-key reference, provider request/receipt references, actual InferenceRequestId when supplied, FinalRequestBoundaryId, exact request digest, transaction/reservation/participant references, PreparedParticipant attempt/ledger/tuple fields where JF-10 applies, I/D/Storage evidence references and C owner signature.

The wire contract preserves these outcome distinctions:
- `HANDOFF_ACCEPTED`: requires authoritative provider acceptance evidence, provider request identity and provider receipt;
- `HANDOFF_REJECTED`: requires definitive no-handoff proof; a local pre-invocation error is not a provider rejection;
- `NOT_INVOKED`: a distinct pre-provider disposition with its own proof;
- `UNKNOWN` / `IN_DOUBT`: requires an explicit unresolved reason and remains nonterminal.

H forbids the following semantic promotions:
- Storage `COMMITTED` or PublicationReceipt → provider `HANDOFF_ACCEPTED`;
- I `COMMIT_WON` → provider `HANDOFF_ACCEPTED`;
- H transport ACK / COC quorum commit → provider outcome;
- provider `HANDOFF_ACCEPTED` → inference completion, content correctness or G Applied;
- timeout, absent receipt, lost ACK or process death → `HANDOFF_REJECTED`.

The same provider idempotency-key and immutable request/participant tuple must survive retries and reconnect. H transports the references and digest; C alone determines provider outcome.

## 5. Enumerated H amendments / limitations

1. **Cross-message semantic validation is mandatory.** The schema is structural. A validator must enforce S0–S4 order, batch/manifest tuple equality, participant count, owner snapshot exact set, canonical digest rules, replay/conflict identity and no recovery before S4.
2. **Outcome-dependent evidence is mandatory.** v1.2.1 adds conditional requiredness for C provider outcomes, I terminal receipt-consumption evidence, and Storage COMMITTED versus ROLLED_BACK evidence. Validators must also reject contradictory extra evidence and malformed state combinations.
3. **Authenticated provenance is separate from payload claims.** `owner_signature_ref`, COC quorum proof and protected channel binding are separate. H cannot validate an owner signature or key status without I-approved trust policy and authoritative verifier inputs.
4. **Canonical bytes remain unfrozen.** Duplicate-key rejection, Unicode normalization/rejection, absent-vs-null, number/hex/timestamp encoding, canonical JSON bytes and signature preimage remain pending a joint I/H profile decision. The schema does not select a cryptographic algorithm or key custody model.
5. **Downgrade control is required.** A peer that receives any v3.2 recovery or C Provider Outcome family must negotiate/require unified schema 1.2.1 or a later explicitly compatible profile. It MUST NOT silently fall back to 1.1.0 and drop Batch/Manifest/C Provider Outcome fields.
6. **Generated artifacts and interoperability remain open.** No generated IDL/SDK, cross-language canonical-byte fixtures, real signature verification, parser hardening or transport interoperability run is evidenced.
7. **Unknown critical fields/types fail closed.** Extension handling must preserve forward compatibility only for explicitly non-critical fields; unknown critical record/message families cannot be interpreted as terminal or safe.
8. **Owner boundaries remain unchanged.** H transports C Provider Outcome but cannot author it; H transports I/D/Storage proofs but cannot create them; H cannot release any owner gate or mark G Applied.

## 6. Required H conformance cases — specified, not executed

- H-COC-01: Batch without Manifest Record remains incomplete/fenced.
- H-COC-02: Manifest Record without exact prior Batch is rejected.
- H-COC-03: reversed Batch/Manifest positions are rejected.
- H-COC-04: mismatched P, RecoveryEpoch, ManifestId/Digest/count/high-water is rejected.
- H-COC-05: duplicate participant or owner snapshot role is rejected.
- H-COC-06: absent member array differs from explicit empty array.
- H-COC-07: any participant recovery action before S4 is rejected.
- H-PO-01: HANDOFF_ACCEPTED without provider receipt/evidence is rejected.
- H-PO-02: HANDOFF_REJECTED without definitive no-handoff proof is rejected.
- H-PO-03: NOT_INVOKED is not conflated with provider rejection.
- H-PO-04: UNKNOWN/IN_DOUBT remains nonterminal across timeout/reconnect/lost ACK.
- H-PO-05: Storage COMMITTED, I COMMIT_WON or H ACK cannot synthesize provider outcome.
- H-PO-06: same-key/same-tuple replay is idempotent; changed digest/key/tuple is CONFLICT.
- H-PO-07: schema downgrade to 1.1.0 cannot omit required v3.2 message fields.
- H-PO-08: signature/key-status/canonicalization unknown remains unverifiable/fail-closed.

**Disposition:** H accepts the exact v3.2 Batch/Manifest order and C Provider Outcome semantics at the protocol contract level with the listed validator, canonicalization, trust and interoperability limitations. Schema 1.2.1 is a unified documentation-derived candidate, not a frozen production wire profile. H-COC/H-PO cases are SPECIFIED / NOT RUN.

## 7. Provenance

Assistant-authored role-based H review and schema proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human H Owner authorship or approval.
