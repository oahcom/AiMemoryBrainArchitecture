# Phase 3.8.4 — D Owner Snapshot Membership Proof Contract
# Phase 3.8.4 — D Owner Snapshot Membership Proof 合同

- Owner: D — Memory Brain / ForgetFence Authority
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED OR FROZEN**
- Applies to D-owned work, attempt, producer-registration, derivative and barrier rows in H Unified Manifest 1.2.11 / wire 1.3.0.

## 1. Authority boundary

D alone attests D producer/work admission, WorkItem/Attempt/Derivative membership, ForgetFence generation, lineage and barrier membership. H may validate typed shape and join references but cannot attest D ledger completeness. I PermissionEpoch/InventoryEpoch and C provider counters remain opaque owner-owned values.

## 2. Proof required for each D row

Every D row represented in a COC participant binding or as an unregistered owner-local admission MUST carry one immutable `DAdmissionSnapshotMembershipProof` binding:

- `proof_ref`, `owner_kind=D`, D BrainAuthorityRef;
- exact D producer/work ledger ref and version, exact row/entry ref and digest;
- exact ProducerRegistrationRef / WorkItemRef / AttemptRef / DerivativeRef / admission ref as applicable;
- D-local sequence namespace/value and captured producer-registration, WorkItem and Attempt high-waters;
- immutable D owner snapshot ref/digest, snapshot-attestation ref/digest and complete D ledger root;
- ForgetOperationRef, target/source/ancestor scope binding digest, D Gate ref/generation and ForgetFenceGeneration;
- operation identity/digest, request digest, barrier generation/root/member identity;
- independent D anti-rollback anchor, key-status generation and D signature-profile/key/version/signature references.

A proof binds the exact D-local namespace and must not compare D counters with I, C or COC positions.

## 3. Membership and completeness

The proof attests exact inclusion of the identified row in the frozen D snapshot and that its D-local sequence is at or below the relevant captured D high-water. The signed snapshot must cover all producer registration, WorkItem, Attempt, derivative and barrier rows capable of affecting the target/source/ancestor lineage, including rows lacking COC registration.

Membership is not completeness. Completeness additionally requires D's authoritative query/projection identity, pagination completion, count, ordered set root, producer registry version/digest, dependency-inventory revision/digest, high-water vector and anti-rollback checkpoint. A late-discovered pre-fence row invalidates the old snapshot and reopens the affected barrier; the successor snapshot must include it. An empty D set requires a separate D-signed COMPLETE_EMPTY proof and cannot be inferred from count=0.

## 4. D signature projection and verification

D owns the proof canonical projection, digest preimage and signing profile. The signed projection includes all fields in §2 plus issuer/subject/audience/purpose, target lineage selector, applicability decision, Gate/Fence generation, snapshot roots and anti-rollback anchor. Only signature bytes/ref and explicitly derived digest fields are excluded.

Verification checks D key status, signature, scope, target lineage, exact snapshot and high-water inclusion. H must not interpret or re-sign D's proof. I/D cross-owner joins use exact typed refs and digests; they never compare numeric counters.

## 5. Gate/recovery semantics

D Gate Release validates every D membership proof in the canonical union Manifest and reconciles it against the same frozen D snapshot. A proof does not mean WorkItem terminality, publication, cancellation or Forget completion. UNKNOWN/IN_DOUBT, late discovery, incomplete dependency closure, changed barrier root, stale FenceGeneration or anti-rollback uncertainty keeps D's barrier/gate closed.

D outage admission release remains `OUTAGE_ADMISSION_RELEASE_ONLY`; it does not clear the effective Forget Fence or authorize C provider egress.

## 6. Decision boundary

This is a D-role proposal in the coordinating session, not independent human D Owner approval. The D proof signer/key lifecycle, durable ledger query, producer/queue/worker/restore reconciliation and executable race/fault tests remain unimplemented/unverified. No physical Storage acceptance or Forget completion is claimed.
