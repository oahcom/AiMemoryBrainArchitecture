# H Owner Review — COC Durable Log, Recovery Batch & JF-10 Wire Contract

- Reviewer: H — BMCP Protocol Architect
- Review target: `reviews/storage-consistency/phase-3.6-coc-durable-log-and-recovery-protocol-storage-design.md`
- Exact target: commit 9a975f665ee60f4551effe0104ea8f867716d9dd; blob cd5566b3d99b5204401ac713a5bb2dcf89a02726
- Decision: **NEEDS_REVISION**
- Scope: wire representation, schema evolution, canonicalization, typed evidence and transport semantics. No cryptographic governance or production schema freeze is implied.

## 1. Accepted protocol direction

The proposal correctly requires typed owner references, typed positions, immutable record identities, canonical payload digests, authenticated owner evidence, idempotent replay, hard conflict on same ID/different digest, and explicit UNKNOWN/IN_DOUBT semantics. It correctly forbids comparing COC epoch/index with I sequencer position, D generation/cursor or Storage XID/commit cursor.

The five JF-10 bridge message families are the right conceptual separation:
1. `JF10_PREPARE_INTENT_REGISTERED`
2. `JF10_PREPARED_PARTICIPANT_REGISTERED`
3. `I_JF10_TERMINAL_DECISION_OBSERVED`
4. `STORAGE_JF10_PARTICIPANT_RESOLVED`
5. `JF10_BRIDGE_RECONCILIATION_RECORDED`

## 2. Blocking findings

### H-COC-01 — Recovery Cutoff Batch wire mapping is not pinned by the target artifact (BLOCKING)

The H documentation contains a recovery-batch mapping addendum, but the current `bmcp.applied-ack/1.1.0` JSON Schema candidate is specifically a five-family JF-10 bridge schema. It does not itself define the recovery-batch message families and required fields from this proposal. The Storage proposal cannot claim a frozen wire contract from a documentation-only mapping.

Required amendment: publish a versioned schema addendum or new schema that explicitly models:
- `OWNER_LOCAL_PENDING_GATE`;
- `COC_RECOVERY_CUTOFF_BATCH`;
- `PARTICIPANT_SET_RECONCILIATION`;
- `OWNER_LOCAL_GATE_RELEASE`;
- `COC_RESTORE_FENCED`.
Bind exact field names, requiredness, null/empty semantics, canonical ordering, owner completeness attestations, pre-batch prefix/root, batch position/digest, participant manifest digest, and gate release owner signature. Keep these as separate message families; do not overload Applied ACK.

### H-COC-02 — Immutable batch/participant-manifest sequence has no unambiguous wire identity (BLOCKING)

The Storage proposal commits the batch before participant enumeration but also says the batch contains participant enumeration high-water. H needs an exact representation of whether the participant set is embedded in the batch or a separate immutable manifest. If separate, define `manifest_id`, `manifest_digest`, `batch_ref`, `batch_digest`, prefix P and owner high-water binding. A receiver must reject a manifest whose prefix or batch binding differs.

### H-COC-03 — Record envelope and owner proof reference types need schema-level definition (BLOCKING FOR FREEZE)

The proposal lists `LogRecordId`, `RecordType`, `SchemaVersion`, owner refs, idempotency key, canonical payload digest, term/index, previous digest, entry digest, ActorRef, KeyId and Signature, but does not define wire types, canonicalization profile, algorithm identifiers, domain separation, key-status proof, issuer/audience binding or unknown-critical-type behavior in a normative schema. These can remain open in a draft but block protocol freeze.

### H-COC-04 — Error and response semantics need exact encoding (BLOCKING)

Define typed response/error envelopes for quorum unavailable, stale/linearizable read unavailable, UNKNOWN, IN_DOUBT, CONFLICT, RESTORE_FENCED, owner unavailable and same-key lookup result. A timeout/lost ACK is transport UNKNOWN, not a transaction outcome. Retry identity must be stable and bound to canonical digest and message family.

## 3. JF-10 same-XID schema assessment

The existing JF-10 schema candidate includes fields for preallocated XID, DB identity, prepared receipt, I decision/sequence, Storage resolution, same-XID proof, PublicationReceipt, non-publication proof, visibility state and reconciliation lookups. This is useful candidate coverage, but the schema itself is documented as not production-frozen and requires runtime cross-field semantic validators.

Required semantic checks:
- all XID references are bound to the same DB identity, participant, operation digest and owner boundary;
- COMMITTED requires PublicationReceipt + VisibilityPointer transaction ref and forbids non-publication proof;
- ROLLED_BACK requires authoritative non-publication proof and forbids PublicationReceipt/visibility pointer;
- I decision must be owner-signed and bound to the exact prepared participant; COC observation is not I terminality;
- same message ID + same digest is idempotent; changed digest conflicts;
- UNKNOWN/PENDING cannot be coerced into terminal outcomes;
- COC/I/D/Storage positions remain typed opaque refs and cannot be compared.

## 4. Canonicalization and versioning conditions

1. Freeze a canonicalization profile ID and exact algorithm suite per schema version; include explicit domain separation for log record, batch, participant manifest and message envelope digests.
2. Define whether empty owner request sets are encoded as empty arrays or explicit null; do not allow both encodings to canonicalize ambiguously.
3. Define deterministic ordering for set-valued I/D refs and ParticipantIntentRefs using canonical opaque-reference bytes, never local time or arrival order.
4. Unknown critical record types must fail closed; unknown non-critical types may be retained only under explicit forward-compatibility rules.
5. Version negotiation must prevent an older receiver from silently dropping recovery-batch fields or treating a newer record as an older terminal family.
6. Integrity/signature profile and key lifecycle remain subject to I/Security approval; H does not approve cryptographic algorithms or key custody.

## 5. Owner-local Gate and typed-order assessment

H can transport an owner-issued pending-gate attestation and owner-issued gate-release attestation. It cannot issue either. The message must distinguish owner authority, gate ref, owner cursor/high-water, recovery epoch, batch digest and disposition. A COC restore-fenced message is only a COC state observation and must not clear I/D gates. H receiver sequence and message arrival order remain transport metadata only.

## 6. Required H tests

- H-COC-01: reject recovery batch with missing I/D completeness attestation.
- H-COC-02: reject batch with prefix/root mismatch or duplicate request refs.
- H-COC-03: reject participant manifest not bound to batch digest and prefix.
- H-COC-04: reject COC-issued I/D gate release.
- H-COC-05: reject cross-authority sequence comparison or timestamp ordering.
- H-COC-06: unknown critical RecordType fails closed.
- H-COC-07: same message ID/digest replay idempotent; changed digest conflict.
- H-COC-08: lost ACK remains transport UNKNOWN and resolves by same-key authoritative lookup.
- H-COC-09: schema-version downgrade cannot drop recovery-batch fields.
- H-COC-10: JF-10 COMMITTED/ROLLED_BACK cross-field invariants enforce exact same XID/DB/digest and publication/non-publication exclusivity.

**Conclusion:** H accepts the conceptual typed-evidence direction but does not accept this exact proposal as wire/schema complete. Publish a versioned schema for recovery-batch messages and resolve the batch/manifest identity before requesting a new exact-version review. No production schema freeze, generated-code interoperability, crypto approval or H conformance pass is claimed.
