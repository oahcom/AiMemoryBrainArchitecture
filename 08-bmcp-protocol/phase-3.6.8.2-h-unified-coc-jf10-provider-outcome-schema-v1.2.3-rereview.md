# Phase 3.6.8.2 — H Exact-Version Review: Unified Schema 1.2.3 + Storage v3.2.2

- Owner perspective: H — BMCP Protocol & Adapter Authentication
- Status: **ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS — UNIFIED SCHEMA CANDIDATE, NOT FROZEN**
- Storage v3.2.2 Blob: `4039fd4c08aa0bb7da63fe5dab92e419487f48d1`
- Companion COC/PostgreSQL §14 Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- Current I Phase 3.6.8 Blob: `cf4b76f151204fa47b156b5d807e7378c28fd268`
- Current D Phase 3.6.8 Blob: `2d95099a2e19a8cbec325925b70da576f73d9899`
- C exact Provider Outcome review Blob: `535579cdfeedf705195bb4aa04cf1a85cb9b9a0f`
- H source identity/protected-operation contract Blob: `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`
- Unified schema v1.2.2 predecessor Blob: `6d4e6e4075fcec392dbc46c97f132a7ca08d8df1`
- Unified schema v1.2.3 Blob: `4ff62c587dac1566d95004a0fad95ca35d25f4e6`
- Project phase: ARCHITECTURE DESIGN; NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED

## 1. H exact-version decision

**H DECISION: ACCEPT WITH ENUMERATED PROTOCOL AMENDMENTS** for Storage v3.2.2 + companion COC §14 + current I/D cross-owner inputs + C Provider Outcome, limited to H's BMCP wire and protocol-validation authority.

H accepts the exact Storage order:
1. I/D/C owner-local Gate closure and high-water/ledger freeze (S0a);
2. COC quorum recovery and linearizable prefix P freeze (S0b);
3. canonical union manifest construction (S1);
4. quorum Recovery Cutoff Batch commit binding P, owner snapshots and ManifestId/Digest/count (S2);
5. separate quorum Manifest Record commit binding the exact Batch position/digest and complete union (S3);
6. linearizable read-back of both records and cross-binding/currentness checks (S4);
7. participant recovery/reconciliation only after S4.

The manifest union contains both `COC_PARTICIPANT` and `OWNER_LOCAL_ADMISSION` variants. Owner-local admissions without a COC ParticipantIntentRef are represented explicitly with null plus an absence reason; they are not omitted or treated as an empty COC participant set.

## 2. Unified schema 1.2.3

H publishes:
- Path: `08-bmcp-protocol/schemas/bmcp.coc-jf10-unified-1.2.3.schema.json`
- Blob: `4ff62c587dac1566d95004a0fad95ca35d25f4e6`
- Commit: `bc3b5f65c1c0abdce057a0fb8b2d1289dc7b21c7`
- Schema ID/version: `bmcp.coc-jf10-unified/1.2.3`
- Protocol message variants: 11
- Participant Manifest member variants: 2

Version 1.2.3 supersedes 1.2.2 for this exact v3.2.2 bundle. In addition to the two typed Manifest member variants, C Provider Outcome now directly binds:
- OwnerAdmissionRef and owner admission digest;
- C owner-ledger ref/version/root, local sequence and frozen high-water;
- COC ParticipantIntentRef as an explicit nullable field, with a mandatory absence reason when null;
- provider idempotency-key reference, provider request/receipt and outcome evidence;
- exact request/final-boundary and applicable I/D/Storage participant tuple refs.

This closes the prior schema gap where the Manifest could carry a pre-COC owner admission but the C Provider Outcome message still required a COC ParticipantIntentRef.

## 3. Cross-message semantic validation requirements

The JSON Schema is structural. A separate protocol validator MUST enforce:
- S0a happens before S0b; owner snapshots are independently signed and monotonic;
- the union contains every applicable COC participant at/before P and every I/D/C owner-ledger member through frozen high-waters;
- each union member is represented exactly once or has a valid owner-signed scope-specific exclusion proof;
- COC ParticipantIntentRef and OwnerAdmissionRef are joined only by exact typed immutable cross-reference;
- Batch precedes Manifest Record in the same COC position namespace;
- P, RecoveryEpoch, ManifestId/Digest/count/enumeration high-water and owner ledger roots match across the pair;
- ManifestDigest covers the canonical union/P/RecoveryEpoch/owner snapshot roots and excludes the later Batch back-reference;
- count equals the canonical union length; explicit empty array is not the same as missing;
- exactly one I, D and C owner snapshot is present and current;
- no participant recovery, Storage resolution, provider invocation/retry, visibility publication, owner Gate release or serving before S4.

## 4. C Provider Outcome protocol mapping

H accepts C's exact Provider Outcome contract in Blob `535579cdfeedf705195bb4aa04cf1a85cb9b9a0f`. C alone determines and signs `CSubmitOutcome`; H only serializes and transports it.

The 1.2.3 schema supports:
- `HANDOFF_ACCEPTED`: provider request + provider receipt + authoritative evidence;
- `HANDOFF_REJECTED`: definitive no-handoff proof;
- `NOT_INVOKED`: separate pre-provider proof;
- `UNKNOWN/IN_DOUBT`: explicit unresolved reason, nonterminal.

No I COMMIT_WON, D clearance, Storage COMMITTED/PublicationReceipt, COC commit, H ACK or G Applied state can be promoted to C provider outcome. HANDOFF_ACCEPTED does not mean inference completion, output correctness, user delivery or Applied.

## 5. Current I/D cross-owner alignment

H verifies that the current I/D proposal references are carried as opaque typed owner evidence, not collapsed into BMCP's own sequence:
- I: IGateGeneration, PermissionEpoch, I request high-water, ProducerDomainInventoryEpoch/registry currentness, signer/key-status generation and Restore tuple;
- D: FenceGeneration, fence installation cursor, publication-boundary fencing, barrier root/closure, current I proof and C provider outcome reference for crossed side-effect members;
- C: CSubmitOutcomeRef/digest, provider idempotency-key namespace and exact request/attempt lineage;
- COC: RecoveryEpoch/prefix/batch/manifest record positions and commit proofs.

H does not decide any of these owner outcomes or compare their owner-local counters.

## 6. Enumerated H limitations and tests

1. Canonical JSON bytes, duplicate-key rejection, Unicode normalization/rejection, absent/null behavior, numeric/time encodings and signature preimage remain unfrozen pending I/H profile approval.
2. Owner signatures, COC quorum proofs and protected channel binding are separate; schema presence does not prove cryptographic verification or current key status.
3. JSON Schema cannot prove quorum commitment, cross-record ordering, owner set completeness, exact digest preimage, authoritative currentness or provider outcome truth.
4. Generated IDL/SDK, cross-language canonical-byte fixtures, parser hardening, cryptographic verification and transport interoperability remain NOT VERIFIED.
5. Unknown critical message/field types fail closed. No silent downgrade from 1.2.3 to 1.2.2/1.2.1/1.1.0 for this bundle.
6. H-COC and H-PO conformance cases are SPECIFIED / NOT RUN.

Required tests include owner Gate close racing prefix freeze; pre-COC admission union membership; duplicate/missing union members; Batch/Manifest order and digest mismatch; crash after Batch; no recovery before S4; provider accepted/rejected/not-invoked/unknown evidence; same-key replay; and downgrade rejection.

**Disposition:** H accepts exact Storage v3.2.2 + C Provider Outcome + current I/D evidence mapping with the enumerated protocol limitations. Schema 1.2.3 is a unified documentation-derived candidate, not a frozen production wire profile. No runtime or interoperability PASS is claimed.

## 7. Provenance

Assistant-authored role-based H exact-version review and schema proposal committed at the user's direction. It is not a cryptographic signature and does not prove independent human H Owner authorship or approval.
