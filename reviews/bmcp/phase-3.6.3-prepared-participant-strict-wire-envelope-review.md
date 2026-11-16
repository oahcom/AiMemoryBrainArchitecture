# H Review — Prepared Participant Strict Types, Canonical Wire & Signed Envelope

- Reviewer role: H — BMCP Protocol Architect (role-simulated in the coordinating ChatGPT session; not an independently authenticated H-session signature)
- Decision: **CANDIDATE / NO APPROVAL**
- Review class: architecture/wire-contract review; schema remains candidate
- Target 1: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design-v2.md`
  - Commit: `337fe8bffa178e64ad8e4750f1ede1d561424edc`
  - Blob: `4ed4234ce548a814a9496adf7a14c4459ea9f7ce`
  - Relevant: §§3–4, 7, 10–11
- Target 2: `reviews/storage-consistency/phase-3.6.3-coc-durable-log-and-recovery-protocol.md`
  - Commit: `71f0c745961cff7f75ef0ba2ac7bfd6f8aeccb66`
  - Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
  - Relevant: §14 and §§3.1–3.3, 5, 7–9, 13

## Decision summary

The semantic distinction among participant reference, PostgreSQL GID and native XID is correct. The wire contract is not yet interoperable: both targets list required concepts but do not provide a normative schema with exact field names, nominal type definitions, requiredness/nullability, canonical byte encoding, bounds, version negotiation and machine-testable vectors. Target 1 §10 explicitly delegates the JF-10 schema to H and says it remains candidate/non-frozen. Therefore H cannot approve a wire freeze.

## Blocking wire findings

### H-1 — Define nominal, non-coercible identity types

At minimum define separate nominal types:
- `PreparedParticipantRef`: opaque globally unique participant identity; never a GID or database transaction number.
- `PreparedTransactionGID`: PostgreSQL adapter-specific client-chosen prepared-transaction locator; bounded string with adapter-defined validation.
- `PostgreSQLNativeXID`: engine-assigned native transaction identifier; typed numeric/string representation per PostgreSQL adapter, never a GID.
- `CanonicalAuthorityDBRef`: opaque canonical Storage authority reference.
- `DatabaseIncarnationRef`: opaque governed non-reusable database incarnation identity.
- `PostgreSQLSystemIdentifier`: cluster system identifier, distinct from database OID and authority ref.
- `PostgreSQLDatabaseOID`: database-local engine identifier, not a globally stable DB identity.
- `PostgreSQLTimeline`, `PostgreSQLLSN`: separate types; LSN must not be accepted as an arbitrary integer or timeline.
- `PublicationOperationId`, `RequestDigest`, `ParticipantTupleDigest`, `COCPosition`, `IPolicyPosition`, `DForgetGeneration`: distinct nominal types.
- `PrepareAttemptRef`, `PrepareAttemptGeneration`, `ParticipantLedgerRef`, `ParticipantLedgerVersion`.

No field named generic `xid`. No implicit string/number conversion. Engine-neutral schema must use an explicitly tagged engine-specific locator/native-ID union rather than universalizing PostgreSQL's GID/XID.

### H-2 — Publish exact PreparedParticipantReceipt schema

Candidate field set (required unless explicitly marked optional):
- `message_type = "Storage.PreparedParticipantReceipt"`
- `schema_version`
- `issuer`, `subject`, `owner_authority`, `audience`, `purpose`
- `key_id`, `key_version`, `algorithm_profile`, `canonicalization_profile`, `digest_profile`
- `prepared_participant_ref`
- `prepared_transaction_gid`
- `postgresql_native_xid`
- `canonical_authority_db_ref`, `database_incarnation_ref`
- `postgresql_system_identifier`, `postgresql_database_oid`
- `original_prepare_timeline`, `original_prepare_lsn`
- `publication_operation_id`, `request_digest`, `participant_tuple_digest`
- `owner_boundary`, `causal_order_domain_ref`, `policy_domain_ref`
- `coc_prepare_intent_position`, `coc_prepare_intent_digest`
- `prepare_attempt_ref`, `prepare_attempt_generation`
- `participant_ledger_ref`, `participant_ledger_version`
- `prepared_state`, `prepared_observation_source`, `prepared_observed_at`
- `payload_digest`, `signature`

Do not encode a missing value as an empty string. Required fields cannot be null. Optional fields must have an explicit absent/null policy. Numeric identifiers and positions need specified decimal/hex encoding, range and normalization. Timestamp is audit metadata only and never causal order.

### H-3 — Define StorageResolutionProof and append-only recovery observations

Resolution proof must repeat/bind the immutable participant tuple and include:
- message type/schema version and same signed envelope fields;
- same participant/GID/native XID/DB authority/database incarnation/operation/request/tuple digest/owner boundary;
- original prepare timeline/LSN as immutable references;
- terminal outcome enum: COMMITTED, ROLLED_BACK, UNKNOWN;
- for COMMITTED: exact VisibilityPointer transaction identity and PublicationReceipt identity/digest;
- for ROLLED_BACK: authoritative non-publication evidence ref/digest;
- durable participant outcome-ledger identity/version;
- recovery observations as an append-only array, each with recovery epoch, timeline, LSN, source role and evidence ref;
- verification result/error class.

COMMITTED MUST NOT carry contradictory non-publication proof. ROLLED_BACK MUST NOT carry PublicationReceipt/VisibilityPointer. UNKNOWN cannot be coerced to either terminal outcome.

### H-4 — Specify canonical serialization and signed envelope

The wire spec must define:
- exact serialization format and canonicalization profile;
- deterministic field order or canonical map ordering;
- UTF-8 and Unicode normalization/rejection policy;
- duplicate-key rejection;
- integer/decimal/hex normalization and maximum lengths;
- absent versus null semantics;
- byte-string encoding;
- domain-separation prefix and exact signature preimage;
- digest and signature algorithm profile identifiers;
- protected header coverage and payload coverage;
- unknown critical field/type behavior;
- verification error taxonomy;
- downgrade/version-negotiation behavior.

The concrete cryptographic suite and trust policy are I-owned; H must implement only an I-approved profile and cannot unilaterally select or weaken it.

### H-5 — Replay, idempotency and cross-field semantic validation

Schema validators must enforce:
- one PreparedParticipantRef -> one immutable operation tuple and prepare-attempt lineage;
- same participant/GID/tuple exact retry is idempotent; changed tuple is CONFLICT;
- GID lookup is scoped by CanonicalAuthorityDBRef and DatabaseIncarnationRef;
- native XID is observed evidence and never used as participant identity;
- COC/I/D/Storage positions are typed and incomparable;
- COC prepare-intent digest and position match the receipt;
- I terminal proof references the exact same participant, GID, DB incarnation and tuple digest;
- recovery observations append and never overwrite original prepare coordinates;
- no COC or Storage proof can be interpreted as I authorization;
- unknown critical fields and downgrade that drops a required field fail closed.

## Required interoperability vectors

H must publish positive and negative fixtures for:
1. canonical receipt round-trip produces identical bytes/digest/signature input;
2. GID/native-XID field swap rejected by type validator;
3. wrong DB incarnation or system identifier rejected;
4. duplicate keys and absent/null ambiguity rejected;
5. reordered/noncanonical fields rejected or normalized deterministically per the frozen profile;
6. same identity/same tuple replay accepted as lookup, changed tuple rejected as CONFLICT;
7. receipt from old attempt/generation rejected;
8. original prepare timeline/LSN preserved when recovery timeline changes;
9. COMMITTED/ROLLED_BACK mutually exclusive evidence constraints enforced;
10. unknown critical field/schema downgrade rejected;
11. wrong issuer/subject/audience/purpose rejected;
12. invalid/revoked-key status handled according to I policy.

## Disposition

**CANDIDATE / NO APPROVAL.** The semantic type model is accepted as directionally correct, but no H wire schema, canonicalization profile or signed-envelope contract is approved. H-1 through H-5 and interoperability vectors are required before schema freeze or implementation conformance. No cryptographic algorithm is selected by H in this review.

## Review provenance

This is an H-role technical assessment authored by the coordinating session at the user's direction. It is not evidence that the separate H owner session independently reviewed or signed these targets.
