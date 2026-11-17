# Phase 3.8.4 — I Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — I Owner Snapshot Membership Proof 合同

- Owner: I — Security, Identity and Governance
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED OR FROZEN**
- Applies to: I-owned rows represented in H Unified Manifest 1.2.11 / wire 1.3.0.
- Normative language: MUST / MUST NOT / UNKNOWN.

## 1. Authority boundary

I is the sole authority for I PolicyDomain request/admission ledgers, I receipt issue/consume events, I owner snapshots, I membership proofs, I issuer/key status and I anti-rollback anchors. H transports and structurally validates the proof; H does not decide I ledger completeness or key trust. D/C proofs remain D/C-owned.

## 2. Proof identity and exact binding

Every I row represented as either an `owner_admission_binding` within a `COC_PARTICIPANT` or an `OWNER_LOCAL_ADMISSION` MUST have one immutable `IAdmissionSnapshotMembershipProof`. The proof MUST bind, without aliases:

- `proof_ref`, `owner_kind=I`, I PolicyDomain authority ref;
- exact I ledger ref/version, exact entry ref and entry digest;
- exact I OwnerAdmissionRef, owner-local sequence namespace and sequence;
- captured I admission high-water and admission ledger root;
- immutable I snapshot ref/digest and signed snapshot-attestation ref/digest;
- exact I Gate ref/generation and PolicyDomain/scope binding digest;
- operation identity ref/digest and request digest;
- independent I anti-rollback anchor ref and key-status generation;
- issuer, subject, audience, purpose, signature profile, key ID/version and signature ref.

The sequence is compared only inside its I-owned namespace. No comparison to D/C sequence or COC index is permitted.

## 3. Membership and completeness semantics

The I proof attests that the exact ledger row is included in the exact immutable signed snapshot, that the row sequence is at or below the captured I admission high-water, and that the snapshot root/count/set digest were computed over the complete applicable I admission query for the declared PolicyDomain and scope.

A valid row-membership proof does not by itself prove the entire I set is complete. Completeness additionally requires the signed snapshot attestation, exact query identity, pagination-complete evidence, count, canonical set digest/root and high-water. Empty I sets require the separate RecoveryJoin COMPLETE_EMPTY proof; zero count or empty array alone is not proof.

## 4. Signature projection

I defines and owns the canonical proof P0, digest preimage and signature profile. The P0 MUST include every identity, ledger, entry, sequence/high-water, snapshot, attestation, root, scope, operation, request, gate-generation, anti-rollback, key-status, issuer/subject/audience/purpose field listed above. It excludes only the signature bytes/ref and derived digest fields explicitly enumerated by the I profile. No H or Storage field may be silently added or removed from the I projection.

The proof digest is SHA-256 over the I-approved canonical proof payload. Signature verification checks the exact I key version and key-status generation, issuer authorization, audience, purpose, scope and anti-rollback anchor. Revoked, unknown, stale, rolled-back or unverifiable key state yields UNKNOWN and blocks I Gate Release.

## 5. Release use

I Gate Release MUST validate every I membership proof referenced by the canonical union Manifest and reconcile it against the exact frozen I snapshot. Any missing row, duplicate, unexpected row, root mismatch, high-water mismatch, incomplete page, stale key status or changed currentness CAS blocks release. I may not attest D/C rows.

## 6. Failure semantics and retention

Proofs are immutable and append-only. Late evidence creates a successor proof or reconciliation record; it never rewrites an old proof. Missing ledger, partial query, stale replica, unavailable anti-rollback checkpoint, uncertain ordering or failed signature returns UNKNOWN. No timeout, absent COC participant or zero count may be converted into an empty-set proof.

## 7. Decision boundary

This contract is an I-role proposal in the coordinating session, not independent human I Owner approval. Production algorithm/regulatory suitability, trust-root ceremony, HSM/KMS, key rotation, compromise response, external anti-rollback and durable PolicyDomain sequencer conformance remain open. I exact review of H 1.2.11 is limited to the wire fields and semantic obligations above; it does not freeze production cryptography.
