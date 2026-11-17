# I Owner Decision — Gate Release Currentness CAS and Admission Proof
# I Owner Gate Release 当前性 CAS 与 Admission 证明裁决

- Owner: I — Security & Governance
- Review mode: independent I-role semantic review at the user's direction
- Decision: **ACCEPT WITH CONDITIONS**
- Status: semantic contract accepted within I authority; implementation, inventory closure and conformance OPEN
- Controlling contract: gate-release-currentness-cas-and-admission-proof.md, including §11

## 1. I decision

I accepts the I-local Currentness CAS and cross-owner release barrier semantics in the exact current contract. The earlier broad wording that could imply a single transaction over I/D/C/H/Storage/COC is explicitly controlled by §11: I's sequencer atomically orders I-owned state only. Cross-owner release is a staged, recoverable barrier, not a fictitious global ACID transaction.

I retains exclusive authority over Principal/authorization policy, PermissionEpoch, IGateGeneration, global producer/recipient/backup/export/restore inventory, policy exceptions, revocation semantics and global completion. D, C, H and Storage remain independent evidence authorities.

## 2. Accepted invariants

1. I Gate Release CAS compares I-owned gate revision, PermissionEpoch, policy revision, I inventory epochs/digests, proposal nonce/expiry and I evidence manifest.
2. Foreign owner evidence is bound by exact typed refs, signed digests, issuer/key, scope, target mapping and owner-local generation. No cross-owner counter arithmetic is permitted.
3. Global release is not effective after I's local commit alone. Every mandatory owner must complete its own local release CAS and return durable acknowledgement; offline/unknown owners keep global state PENDING.
4. A global release token is one-use, bound to one exact prepared owner set and cannot reopen a stale owner gate.
5. Per-operation authorization is separate from global Gate Release.
6. For C provider submit, I's PolicyDomain Sequencer orders single-use authorization consumption against revocation: REVOCATION_WON blocks provider invocation; COMMIT_WON creates an exact in-flight participant that later revocation cannot pass until C terminalizes it; UNKNOWN remains blocked.
7. I receipt never proves D admission, C egress, Storage visibility, provider execution, Adapter Applied or global Forget completion.

## 3. Conditions and required owner inputs

- D must confirm D-local gate/fence and exact participant semantics; D outage release remains OUTAGE_ADMISSION_RELEASE_ONLY.
- C must consume exact I authorization terminality and retain C-owned provider outcome.
- H must define the canonical wire schemas, signatures, empty-set representation, replay behavior and ACK mapping; H cannot mint I decisions.
- Storage must validate the exact I CommitAuthorizationReceipt at the final visibility transaction; Storage cannot issue or reinterpret I authorization.
- The I global inventory must enumerate all mandatory enforcement and recipient targets, including offline, backup, export, restore and provider-side targets where policy requires them.
- Cryptographic profile, key rotation/revocation, issuer/audience binding and evidence retention must be finalized before freeze.

## 4. Rejected interpretations

I rejects:
- one synthetic global epoch/counter combining PermissionEpoch, ForgetFenceGeneration, CGateGeneration, COC RecoveryEpoch, H CapabilityEpoch or Storage transaction position;
- describing independent local reads followed by writes as cross-service atomic CAS;
- treating transport ACK, owner release proposal, cached ALLOW or signed stale token as currentness;
- marking global release EFFECTIVE while any mandatory owner acknowledgement is absent or UNKNOWN;
- treating D/C owner-local release as I global authorization or Forget completion.

## 5. Conformance gate

Required tests are enumerated in the controlling contract §11.5. They are **SPECIFIED / NOT RUN**. No production I sequencer, complete inventory, multi-owner barrier execution, cryptographic verification or global Forget completion is claimed.

**I disposition: ACCEPT WITH CONDITIONS.** Gate semantics may be used as a candidate cross-owner contract. No schema freeze, implementation sign-off or global release authorization is granted.
