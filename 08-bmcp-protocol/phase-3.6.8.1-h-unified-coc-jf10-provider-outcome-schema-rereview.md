# Phase 3.6.8.1 — H Exact-Version Re-review: Union Manifest + Provider Outcome Schema

- Owner perspective: H — BMCP Protocol & Adapter Authentication
- Status: **ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS — UNIFIED SCHEMA CANDIDATE, NOT FROZEN**
- Storage v3.2.1 Blob: `491e8e916cf9b1609c5220fb41fb766b8cddccf2`
- Companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- C exact Provider Outcome / union-manifest review Blob: `377c16531d5d8b43b353a09f61ebac9e999fc48d`
- C source contract Blob: `45a48249717c8cddb07ab96197730ef93d406c22`
- H source identity/protected-operation contract Blob: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- Prior unified schema v1.2.1 Blob: `746d66aa231af1ef2f7c3571dbc31c46e28b2547`
- Current unified schema v1.2.2 Blob: `6d4e6e4075fcec392dbc46c97f132a7ca08d8df1`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED

## 1. H exact-version decision

**H DECISION: ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS** for Storage v3.2.1 and companion COC §14 Blob 8ac178, limited to H wire representation, schema/versioning, transport integrity and protocol validation.

The owner-gate-before-prefix correction and complete union manifest are necessary. H accepts:
- S0a: I/D/C independently close their owner-local admission gates and freeze request/admission ledgers, high-waters, roots and anti-rollback anchors;
- S0b: after quorum restoration, COC enters RECOVERY_FENCED and freezes linearizable prefix P;
- S1: canonical Participant Manifest is the union of all COC ParticipantIntentRefs at/before P and all applicable I/D/C owner-local admissions through their frozen high-waters, including not-yet-COC-registered entries;
- S2: quorum-commit Batch binding P, owner snapshots and ManifestId/Digest/count;
- S3: quorum-commit separate Manifest Record binding the exact prior Batch position/digest and the exact union payload;
- S4: linearly read back both records and validate all bindings before participant recovery.

H rejects any interpretation that an absent COC ParticipantIntentRef means an owner-local admission is absent or that a missing Manifest Record represents an empty set.

## 2. Unified schema v1.2.2

H publishes:
- Path: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.2.schema.json`
- Blob: `6d4e6e4075fcec392dbc46c97f132a7ca08d8df1`
- Commit: `ffa4be5ddd4e000db46a01f8a285ddf6e1fad240`
- Schema ID/version: `bmcp.coc-jf10-unified/1.2.2`
- Protocol message variants: 11
- Manifest member variants: 2

Schema v1.2.2 supersedes v1.2.1 for the Storage v3.2.1 bundle. The two typed Manifest member variants are:
1. `COC_PARTICIPANT`: a committed ParticipantIntentRef with COC position/digest and immutable request/participant identity;
2. `OWNER_LOCAL_ADMISSION`: an I/D/C OwnerAdmissionRef with owner ledger ref/version, local sequence/high-water/root, operation digest, admission state and explicit COC ParticipantIntentRef null plus reason when not registered.

A member may bind both identities only when an authoritative typed cross-reference proves they represent the same immutable operation/attempt. TransactionId, timestamp or payload similarity cannot deduplicate entries.

The schema retains the other ten message families: Batch, Manifest Record, owner pending Gate, owner Gate release, RecoveryEpoch completion, the five JF-10 bridge records and C Provider Outcome. The exact set is 11 total variants; the two Manifest member variants are nested under the Manifest Record.

## 3. Batch/Manifest semantic validator requirements

JSON Schema is not sufficient to prove the v3.2.1 state machine. H requires a protocol semantic validator to enforce:
- S0a owner gates and high-waters close before S0b prefix P is frozen;
- S1 union equals every applicable COC prefix participant plus every I/D/C owner-ledger member through the captured high-waters;
- each union member occurs exactly once or has a valid owner-signed scope-specific exclusion proof;
- no deduplication without authoritative typed cross-reference;
- every owner-local admission with no COC intent carries explicit null and absence reason;
- explicit empty union is an empty array with count zero; missing array is invalid;
- Batch and Manifest Record bind identical RecoveryEpoch, P, ManifestId, ManifestDigest, count and enumeration high-water;
- Batch position precedes Manifest Record position in the same COC namespace;
- ManifestDigest is computed over the canonical union, P, RecoveryEpoch and frozen owner snapshot roots, excluding the later Batch back-reference;
- owner gate generations, request high-waters and anti-rollback anchors remain current at S4;
- no participant recovery, Storage resolution, provider invocation/retry, visibility publication, owner Gate release or protected serving before S4.

## 4. Provider Outcome mapping

H accepts C's independent Provider Outcome semantics and maps them to `C_PROVIDER_OUTCOME_RECORDED`. The message binds CSubmitOutcomeRef/digest, provider/adapter, stable provider idempotency-key reference, provider request/receipt, actual InferenceRequestId when supplied, FinalRequestBoundaryId, exact request digest, TransactionRef, ParticipantReservationRef, ParticipantIntentRef or OwnerAdmissionRef, exact Storage participant attempt/ledger/tuple where applicable, I/D/Storage evidence references and C owner signature.

Outcome-dependent evidence:
- `HANDOFF_ACCEPTED`: provider request identity, provider receipt and authoritative acceptance evidence required;
- `HANDOFF_REJECTED`: definitive no-handoff proof required;
- `NOT_INVOKED`: separate pre-provider proof; not a provider rejection;
- `UNKNOWN/IN_DOUBT`: explicit unresolved reason; nonterminal and non-expiring.

H prohibits promotion of Storage COMMITTED, I COMMIT_WON, COC commit, transport ACK or provider acceptance into another authority's result. Provider HANDOFF_ACCEPTED is not inference completion, content correctness, user delivery or G Applied.

## 5. Enumerated H limitations and required controls

1. **Cross-message validation remains mandatory.** Schema does not prove Batch/Manifest order, exact union completeness, count/member equality, owner role uniqueness, cross-record digest equality or S4 completion.
2. **Canonicalization remains a candidate.** Duplicate-key rejection, Unicode normalization/rejection, absent/null behavior, canonical JSON bytes, numeric/time encodings and signature preimage require a jointly approved I/H profile. No cryptographic algorithm or key custody is selected.
3. **Owner signatures and COC quorum proof are distinct.** H transports both but cannot create or validate authority absent I-approved trust policy and authoritative verifier/key-status inputs.
4. **Downgrade is forbidden.** v3.2.1 recovery and Provider Outcome messages require schema 1.2.2 or an explicitly compatible later version; no silent fallback to 1.1.0/1.2.0/1.2.1.
5. **Unknown critical types fail closed.** Unknown critical messages, fields or extensions cannot be interpreted as terminal evidence or permission to resume.
6. **No generated or interoperable artifact is evidenced.** Schema is documentation-derived; generated IDL/SDK, cross-language canonical-byte fixtures, parser hardening, signature verification and transport interoperability remain NOT VERIFIED.
7. **No runtime conformance claim.** H-COC and H-PO tests below are SPECIFIED / NOT RUN.

## 6. Required H conformance cases — specified, not executed

- H-COC-01: owner gate/high-water freeze after P is rejected.
- H-COC-02: owner-local admission without COC intent is represented as OWNER_LOCAL_ADMISSION.
- H-COC-03: missing owner admission or duplicate union member is rejected.
- H-COC-04: COC participant and owner admission are deduplicated only with exact typed cross-reference.
- H-COC-05: Batch without Manifest Record remains fenced.
- H-COC-06: Manifest without exact prior Batch is rejected.
- H-COC-07: reversed positions or mismatched P/RecoveryEpoch/ManifestId/Digest/count is rejected.
- H-COC-08: no participant recovery before S4.
- H-PO-01: HANDOFF_ACCEPTED without provider receipt/evidence is rejected.
- H-PO-02: HANDOFF_REJECTED without definitive no-handoff proof is rejected.
- H-PO-03: NOT_INVOKED is distinct from HANDOFF_REJECTED.
- H-PO-04: UNKNOWN/IN_DOUBT remains blocking across timeout/reconnect/lost ACK.
- H-PO-05: Storage COMMITTED, I COMMIT_WON or H ACK cannot synthesize C outcome.
- H-PO-06: same provider key/same tuple replay is idempotent; changed digest/key/tuple is CONFLICT.
- H-PO-07: schema downgrade cannot drop union-member or Provider Outcome fields.
- H-PO-08: missing historical key status, signature or canonicalization profile remains unverifiable/fail-closed.

**Disposition:** H accepts exact Storage v3.2.1 Batch/Manifest semantics and C Provider Outcome wire mapping with the enumerated validator/trust/canonicalization limitations. Schema 1.2.2 is the unified documentation-derived candidate for this bundle, not a frozen production protocol. H-COC/H-PO tests are SPECIFIED / NOT RUN.

## 7. Provenance

Assistant-authored role-based H exact-version re-review and schema proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human H Owner authorship or approval.
