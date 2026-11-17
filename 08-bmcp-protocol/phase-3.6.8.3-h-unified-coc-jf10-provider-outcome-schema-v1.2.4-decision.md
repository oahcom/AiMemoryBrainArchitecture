# Phase 3.6.8.3 — H Exact-Version Decision: Unified COC / JF-10 / Provider Outcome Schema 1.2.4

- Owner perspective: H — BMCP Protocol & Adapter Authentication
- Status: **ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS — UNIFIED SCHEMA CANDIDATE, NOT FROZEN**
- Storage v3.2.2 Blob: `4039fd4c08aa0bb7da63fe5dab92e419487f48d1`
- Companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Current I Phase 3.6.8 Blob: `cf4b76f151204fa47b156b5d807e7378c28fd268`
- Current D Phase 3.6.8 Blob: `2d95099a2e19a8cbec325925b70da576f73d9899`
- C exact Provider Outcome review Blob: `535579cdfeedf705195bb4aa04cf1a85cb9b9a0f`
- H source identity/protected-operation contract Blob: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- Unified schema v1.2.3 predecessor Blob: `4ff62c587dac1566d95004a0fad95ca35d25f4e6`
- Unified schema v1.2.4 Blob: `1dc2d3a2675503c5ab97134d57d4c2b7bb80ca15`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED

## 1. H exact-version decision

**H DECISION: ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS** for Storage v3.2.2 + C Provider Outcome + current I/D evidence mapping, limited to BMCP wire representation, schema/versioning, transport integrity and protocol validation.

H accepts the S0a→S0b→S1→S2→S3→S4 order and the complete typed union manifest:
- owner-local I/D/C admission gates and ledgers freeze before COC prefix P;
- manifest contains every COC participant at/before P and every applicable owner-local admission through frozen high-waters;
- unregistered owner admissions are explicit `OWNER_LOCAL_ADMISSION` members, not omitted because COC ParticipantIntentRef is absent;
- Batch is quorum committed before the Manifest Record;
- Manifest Record references the exact prior Batch position/digest;
- both are linearly read back and validated before participant recovery.

## 2. Unified schema v1.2.4

H publishes:
- Path: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.4.schema.json`
- Blob: `1dc2d3a2675503c5ab97134d57d4c2b7bb80ca15`
- Commit: `9529437bb61a9ce1db1ee767d69f5352bbc92085`
- Schema ID/version: `bmcp.coc-jf10-unified/1.2.4`
- Protocol message variants: 11
- Manifest member variants: 2

Version 1.2.4 supersedes 1.2.3 for this exact bundle. It retains:
- `COC_PARTICIPANT` and `OWNER_LOCAL_ADMISSION` as distinct typed manifest member variants;
- C Provider Outcome OwnerAdmissionRef, owner ledger root/version/high-water, and nullable COC ParticipantIntentRef with absence reason;
- separate owner signature and COC quorum commit proof;
- outcome-dependent I terminal and Storage resolution evidence.

It corrects one overconstraint in v1.2.3: `participant_reservation_ref` is required for `HANDOFF_ACCEPTED` and `HANDOFF_REJECTED`, because those outcomes necessarily follow a finalized C reservation. It is not required for `NOT_INVOKED`, where the provider boundary was never crossed and no reservation may have been finalized. This prevents the schema from forcing a fabricated reservation solely to express authoritative non-invocation.

## 3. Provider Outcome semantic mapping

C alone authors and attests CSubmitOutcome. H transports it. The schema's conditional evidence rules are:
- `HANDOFF_ACCEPTED`: provider request, provider receipt, provider outcome evidence and finalized ParticipantReservationRef;
- `HANDOFF_REJECTED`: definitive no-handoff proof, provider outcome evidence and finalized ParticipantReservationRef;
- `NOT_INVOKED`: separate non-invocation proof; reservation may be absent;
- `UNKNOWN/IN_DOUBT`: explicit unresolved reason and nonterminal state.

Provider acceptance is not inference completion, content correctness, user delivery or G Applied. Storage COMMITTED/PublicationReceipt, I COMMIT_WON, D clearance, COC commit and H ACK cannot synthesize C Provider Outcome.

## 4. Batch/Manifest semantic validator

Schema 1.2.4 remains structural. A runtime validator MUST additionally enforce:
1. owner gate/high-water freeze precedes prefix P freeze;
2. complete union of COC participants and I/D/C owner-local admissions;
3. exact once-only membership or owner-signed scope-specific exclusion;
4. typed cross-reference for deduplication;
5. Batch precedes Manifest Record in the COC namespace;
6. exact P/RecoveryEpoch/ManifestId/Digest/count/high-water/owner-root equality;
7. canonical digest preimage and member-count equality;
8. exact I/D/C owner snapshot roles and current generations;
9. no participant recovery or provider invocation/retry before S4.

## 5. Enumerated H limitations

- Canonical bytes, duplicate-key rejection, Unicode normalization, absent/null semantics, numeric/time encoding and signature preimage remain unfrozen pending joint I/H trust and canonicalization approval.
- JSON Schema cannot prove quorum commitment, owner signatures, COC ordering, cross-record equality, complete inventory, or actual provider truth.
- Generated IDL/SDK, cross-language fixtures, parser hardening, cryptographic verification and transport interoperability are NOT VERIFIED.
- Unknown critical messages/fields fail closed; no silent downgrade to 1.2.3/1.2.2/1.2.1/1.1.0.
- H-COC/H-PO tests remain SPECIFIED / NOT RUN.

**Disposition:** H accepts exact Storage v3.2.2 and the current C Provider Outcome review with unified schema 1.2.4 as the current documentation-derived protocol candidate, subject to the above semantic validator, canonicalization and trust limitations. No production wire freeze or runtime/interoperability PASS is claimed.

## 6. Provenance

Assistant-authored role-based H exact-version decision and schema proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human H Owner authorship or approval.
