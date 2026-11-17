# Phase 3.6.12 — H Exact-Version Review: Unified Recovery Schema and Batch/Manifest Binding

- Role: H — BMCP Protocol Architect
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: assistant-authored delegated H role review at the user's direction; not an independent human H Owner signature.
- Status: candidate wire/schema review only; NOT FROZEN / NOT IMPLEMENTED / NOT INTEROPERABILITY-VERIFIED

## 0. Exact review bundle

| Artifact | Blob |
|---|---|
| A COC architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| Storage Phase 3.6.12 ordering/bundle amendment | `1c8c0bc11798293293bcf47fa560f1699a5bcfe0` |
| COC base protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| Storage/COC ordering amendment | `9704d110a06d0c2ee98be960054e0396d0b68546` |
| I Phase 3.6.8 | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 provider gate amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| C Phase 3.6.11 provider outcome review | Pending exact readback at decision authoring |
| H Recovery Cutoff schema 1.0.4 predecessor | `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1` |
| H Recovery Cutoff schema 1.0.5 | `3d451778b9867c3b54779c5cd478522993719025` |
| H two-phase wire/validator addendum | `5a3def4f7e84ed489993681455b6840b93ecc282` |
| H semantic validator predecessor | `7e6f67518e476fe9798f23a87798c7a3eb352f3c` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |

## 1. H schema ruling

H accepts the Recovery Cutoff 1.0.5 candidate as the correct structural direction for the two-phase Batch/Manifest contract. It improves on 1.0.4 by separating:
- `participant_manifest_content_digest` — computed before Batch commit;
- `participant_manifest_record_digest` — final committed Manifest record payload digest, consumed by releases/completion;
- `recovery_batch_digest` — committed Batch payload digest.

The Manifest now carries `recovery_batch_ref` + `recovery_batch_digest`, while the Batch carries stable `participant_manifest_ref` + `participant_manifest_content_digest`. This is the required reverse binding without a circular digest.

H confirms the 1.0.5 schema's strict structural shape includes the new required fields on ParticipantManifest, RecoveryCutoffBatch, OwnerGateRelease and RecoveryEpochCompleted. JSON Schema alone cannot prove prefix completeness, digest projection, quorum order or cross-message equality.

## 2. H-M1 — Normative content-digest projection

The wire contract MUST publish one canonical definition of the ParticipantManifestContentDigest preimage:
- exact included fields;
- exact excluded fields;
- canonical ordering and empty-set representation;
- domain-separation label;
- digest profile identifier;
- absent/null behavior;
- encoding and Unicode rules.

The projection must include the stable ManifestId, RecoveryEpoch, exact prefix P, previous-prefix digest, enumeration status, participant entries, count and participant-set root. It excludes future batch backlink, quorum proof and envelope/signature fields. No implementation may invent a different projection.

## 3. H-M2 — Bidirectional cross-message and COC log-order validator

The semantic validator MUST enforce:
- Batch.participant_manifest_ref == Manifest.message_id;
- Batch.participant_manifest_content_digest == Manifest.participant_manifest_content_digest;
- Manifest.recovery_batch_ref == Batch.message_id;
- Manifest.recovery_batch_digest == Batch.batch_digest;
- same RecoveryEpoch/round and exact prefix term/index/root;
- same count, participant-set root, enumeration status and canonical entries;
- Batch log position strictly before Manifest log position;
- ManifestRecordDigest equals the committed manifest envelope payload digest;
- release/completion references both ManifestContentDigest and ManifestRecordDigest.

The validator must obtain linearizable quorum-backed reads and complete pagination. Stale follower reads, missing pages, partial prefix enumeration or unavailable source return UNKNOWN.

## 4. H-M3 — Crash and immutable replay semantics

The semantic validator and state machine must preserve:
- no Batch before prefix and manifest content enumeration are complete;
- no Manifest commit before its exact Batch is quorum committed;
- crash after Batch but before Manifest leaves the system fenced and resumes with the same BatchId, ManifestId and content digest;
- missing or changed staged manifest after Batch commit enters RESTORE_FENCED; no replacement manifest is silently minted;
- crash after Manifest commit requires exact pair readback, not replacement;
- each later cutoff round has new immutable identities and an append-only previous-batch chain.

## 5. H-M4 — Owner snapshot and participant accountability

The schema and validators retain separate request and admission sets/high-waters for I/D/C, explicit COMPLETE_EMPTY semantics, C's reservation/provider-attempt high-waters and mandatory owner admission reference on each participant entry.

For every C-owned participant, H must resolve the exact C owner entry and compare operation identity, request digest, scope, CAdmissionRef, ParticipantIntentRef, prefix position and participant digest. Storage-owned entries must join the exact JF-10 PreparedParticipant tuple. No owner-local counters are compared across authorities.

## 6. H-M5 — Provider Outcome is a separate message family

The reviewed Recovery Cutoff schema 1.0.5 and JF-10 bridge schema 1.1.0 do not define a dedicated `C_SUBMIT_OUTCOME_RECORDED` / `CSubmitOutcome` wire message family.

This is not a reason to place provider outcome fields into the Recovery Cutoff Manifest or to overload the Storage PreparedParticipantReceipt. H requires a separate versioned provider-outcome schema/message family, based on C's owner contract, with at least:
- CAdmissionRef, CProviderAttemptRef/Generation;
- provider identity and idempotency key reference;
- exact final request digest and FinalRequestBoundaryId;
- reservation/ParticipantIntent refs and COC position where registered;
- current CGateGeneration and exact I/D proof references;
- egress disposition NOT_SENT / SENT_OR_AMBIGUOUS / OUTCOME_KNOWN;
- provider outcome ACCEPTED / REJECTED_NO_HANDOFF / UNKNOWN;
- actual provider receipt / InferenceRequestId / same-key lookup evidence where available;
- issuer, subject, audience, purpose, schema version and integrity envelope.

C remains the semantic authority for this message. H owns its wire encoding and validators. Until that separate schema exists and C/H accept the same exact bundle, provider-outcome wire freeze remains OPEN.

## 7. H-M6 — Schema artifact revision versus message schema_version

The file is named Recovery Cutoff schema 1.0.5, while individual message objects currently constrain `schema_version` to `1.0.0`. H must explicitly document whether:
- 1.0.5 is the revision of the schema artifact while 1.0.0 is the stable message-family wire version; or
- message instances must advertise 1.0.5.

No implementation may infer this distinction. The schema artifact revision and on-wire message version must be separately named and unambiguous. If a message wire version changes, downgrade rejection and compatibility policy must be explicit.

## 8. H-M7 — Cryptographic and canonical-byte freeze remains separate

Schema 1.0.5 does not select I's signature algorithm, key lifecycle, trust root, historical verification or anti-rollback policy. H can specify canonical serialization and digest preimages only against approved profile identifiers. No cryptographic or canonical-byte interoperability PASS is claimed.

## 9. H decision

**ACCEPT WITH ENUMERATED AMENDMENTS H-M1 through H-M7.**

H accepts Recovery Cutoff schema 1.0.5 and the two-phase Batch/Manifest direction as a structural candidate. H does not accept the bundle as frozen until the content-digest preimage, cross-message validators, schema-version semantics, provider-outcome message family and I-approved trust profile are closed by exact versions.

This decision is limited to H wire/schema authority. It does not approve C provider semantics, I policy, D Forget semantics, Storage prepared participant outcome, COC deployment or A integration.

## 10. Required evidence — specified, not run

- JSON Schema positive/negative validation for each message family.
- Canonical ContentDigest fixtures across at least two independent implementations.
- Batch/Manifest cross-link and log-position ordering vectors.
- Crash between Batch and Manifest, staged payload loss and replay vectors.
- Empty/non-empty manifest and complete-pagination vectors.
- Owner request/admission count/root/high-water and bidirectional participant join vectors.
- CSubmitOutcome strict schema vectors including NOT_SENT, SENT_OR_AMBIGUOUS, UNKNOWN, ACCEPTED and REJECTED_NO_HANDOFF.
- Downgrade, absent/null, duplicate-key, unknown-critical and wrong-audience rejection vectors.

All vectors remain SPECIFIED / NOT RUN.

## 11. Status and provenance

This is an assistant-authored delegated H role review. It is not an independent human H Owner signature. No schema freeze, cryptographic approval, canonical-byte interoperability, runtime validator PASS, deployment or production activation is claimed.
