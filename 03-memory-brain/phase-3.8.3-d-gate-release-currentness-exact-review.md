# Phase 3.8.3 — D Exact Review: Gate Release Currentness CAS and Producer Admission
# D 精确审查：Gate Release 当前性 CAS 与 Producer Admission

- Owner: D — Memory Brain / ForgetFence Authority
- Review mode: independent D-role semantic review at the user's direction
- Decision: **ACCEPT WITH CONDITIONS**
- Status: D semantic alignment accepted; Storage physical topology, cross-owner proof and conformance OPEN
- Exact reviewed file: gate-release-currentness-cas-and-producer-admission.md
- Exact reviewed Blob: 7f2861d9441b9be6c8e69f41fd0276636be483a8

## 1. D decision

D accepts the currentness and admission semantics only as an alignment supplement to the controlling D contracts in Phase 3.6.7, 3.6.8, 3.7 and 3.8. It does not create a second Forget Gate or replace DGateReleaseReceipt, DInFlightAdmissionSnapshot, DReconciliationTuple, Producer RegistrationReceipt or PublicationParticipantRef.

## 2. Accepted D invariants

1. RegisterProducerWork and InstallForgetFence share one D-authoritative linearizable ordering domain.
2. Fence-first rejects/quarantines affected admission; registration-first creates a durable receipt and is included in the immutable barrier snapshot.
3. D Gate Release final CAS compares D-owned Gate/Fence/high-water/barrier/registry/anti-rollback state only.
4. I ProducerDomainInventoryEpoch, IGateGeneration and PermissionEpoch remain I-owned opaque values. D binds exact signed I evidence in DReconciliationTuple and never compares owner-local counters.
5. Late-discovered pre-fence work or a newly discovered I registry mapping reopens the affected D barrier and invalidates the prior closure proof.
6. D outage release is OUTAGE_ADMISSION_RELEASE_ONLY. It neither clears the effective Forget Fence nor grants I authorization or C provider egress.
7. Canonical derivative visibility follows Storage PREPARED_HIDDEN → D PublicationParticipantRef → I single-use CommitAuthorizationReceipt → Storage final visibility transaction → D/I terminalization after authoritative outcome readback.
8. UNKNOWN/IN_DOUBT remains non-terminal; timeout, lease expiry, worker loss, queue deletion and missing COC row cannot release a barrier.

## 3. Conditions / dependencies

- Storage must resolve its ADR-blocked serialization topology and prove D fence/admission versus final visibility ordering, crash recovery, failover fencing, restore/PITR and read-path invisibility.
- I must provide exact current inventory and operation-bound authorization evidence. An I proof ref is not a D fence or D release.
- E/F/G/H must supply producer/recipient admission and terminal evidence for their own boundaries; D cannot infer their completion.
- H must encode typed D references and preserve issuer/scope/digest binding without changing D semantics.
- D's callable API, signing/key lifecycle and executable race suite remain to be specified and run.

## 4. Required exact tests

The ten cross-owner vectors in the controlling contract §11.4 are **SPECIFIED / NOT RUN**. D also requires the existing D Phase 3.6.7–3.8 vectors for EventRef-only admission, complete dependency registration, publication participant ordering, late discovery, terminal NO_PUBLICATION, restore replay and anti-rollback.

## 5. Explicit non-claims

This review does not claim:
- that D and Storage currently share one serializable transaction domain;
- that PostgreSQL 18.7 capability probes establish the project's deployment topology;
- that I PermissionEpoch is atomically updated by D;
- that DGateReleaseReceipt means Forget completion;
- that any provider request was submitted or any artifact was made visible.

**D disposition: ACCEPT WITH CONDITIONS.** Semantic alignment is accepted. Physical implementation, cross-owner exact-version acceptance and conformance remain OPEN.
