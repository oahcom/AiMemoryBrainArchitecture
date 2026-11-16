# I — Security & Governance Technology Architecture Review

- Document: TAR-I-001
- Owner perspective: I — Security, Identity & Governance Architect
- Execution mode: centralized delegated review by the project integration assistant; not an independent human-owner attestation.
- Branch: `session-i-security-governance-2026-11-16`
- Reviewed branch HEAD: `1fc3b3293ebf2077edfd6ad253647d382173d9fa`
- TAB-001 blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- Global Forget inventory blob: `9100061fa986fb6676656169de3fcf9fc1c72664`
- Phase 3 remediation blob: `6bc45a0aed5b5cb019149e4564d1eeb73e7c2512`
- Phase 3.5 governance blob: `a8632931396125019d1afccff39ea266f52a4d3a`
- Date: 2026-11-17
- Verdict: **CONDITIONAL PASS — policy boundaries are directionally sound; security controls and global Forget remain unproven.**

## 1. Executive verdict

TAB-001 correctly treats security as a cross-cutting authority boundary and does not invent cryptographic algorithms or claim physical erasure from tombstones. Its current language is not sufficient to approve a deployable security posture. Key custody, authenticated principal binding, revocation freshness, remote inference policy, audit integrity, backup encryption, restore quarantine and target completeness require concrete policy-to-control mapping.

I's global Forget contract is a candidate closed-world governance model. It is not satisfied by D's local barrier alone. The global ProducerDomainInventoryEpoch, D's per-operation producer-registration high-water and ForgetFenceGeneration are different namespaces and cannot substitute for one another.

## 2. R1–R6 assessment

| Dimension | Verdict | Evidence and gap | Impact |
|---|---|---|---|
| R1 Requirements/threat model | CONDITIONAL | TAB enumerates identity, authorization, key management, audit and redaction, but no complete asset/attacker/trust-boundary/control matrix is demonstrated. | Security posture cannot be accepted from technology names alone. |
| R2 Boundaries/dependencies | CONDITIONAL | I owns authorization, revocation, PermissionEpoch, target inventory and global completion; D/E/F/G/H/C/Storage own local enforcement/evidence. | Requires explicit evidence contracts at each boundary. |
| R3 Technology selection | OPEN | OS key store, encryption-at-rest, authenticated IPC, remote inference and audit mechanism are capability requirements, not selected implementations. | No security technology should be frozen yet. |
| R4 Resources | NOT MEASURED | Encryption, indexing, audit retention, backup copies and model provider traffic have unquantified CPU/disk/network/storage impact. | Capacity and retention costs unknown. |
| R5 Recovery | BLOCKED for global completion | Restore must replay current governance control state and quarantine stale content before serving. No restore drill or deletion proof is attached. | Stale backups/replicas can resurrect suppressed content. |
| R6 Compatibility | CONDITIONAL | Typed PermissionEpoch, ProducerDomainInventoryEpoch, ForgetFenceGeneration, D producer high-water and owner-specific receipts remain distinct. | Numeric coercion or incomplete target registration invalidates proof. |

## 3. Findings

### TAR-I-P0-001 — Global Forget evidence cannot be complete without closed-world target inventory and per-domain receipts

- Evidence: I inventory blob `9100061fa986fb6676656169de3fcf9fc1c72664`; Phase 3 remediation blob `6bc45a0aed5b5cb019149e4564d1eeb73e7c2512`; Phase 3.5 governance blob `a8632931396125019d1afccff39ea266f52a4d3a`.
- Consequence: an unregistered producer, external recipient, stale index, offline Adapter or retained backup can remain outside the completion proof.
- Recommendation: seal a versioned closed-world producer/recipient inventory; require typed evidence for each registered target; unknown, unsupported, offline, stale, exception and missing evidence remain non-success states. Reconcile inventory epoch changes during an operation and reopen/recompute completion when the target universe changes.
- Owners: I/A plus D/E/F/G/H/C and Storage/external recipient operators.
- Closure: inventory completeness audit, target-by-target evidence vector, exception approval semantics, and adversarial omission tests.

### TAR-I-P0-002 — Permission freshness must be checked at each protected commit/visibility boundary

- Evidence: Phase 3.5 policy distinguishes I PermissionEpoch from D fence generation and requires current authorization at final boundary.
- Consequence: stale cached authorization or payload-supplied ActorRef/ProducerId can create a confused-deputy or revocation race.
- Recommendation: bind authenticated transport principal to the typed domain Actor/Producer identity; payload IDs are claims only. Revalidate current policy decision/epoch at canonical commit, producer admission, derived publication, Context delivery/Applied acceptance, and external action boundary as applicable. Define freshness, revocation propagation, and unknown-policy fail-closed semantics.
- Owners: I with H, D, E, G and C.
- Closure: forged-identity, stale-epoch, revocation-race and replay tests.

### TAR-I-P1-001 — Key custody and encryption lifecycle are not operationally specified

Define key hierarchy, OS-backed storage support, local fallback permissions, rotation, backup wrapping, recovery, compromise response and cryptographic-erasure semantics. Never imply deletion of a data key proves all replicas/backups/external copies are erased without key-scope proof.

### TAR-I-P1-002 — Audit tamper evidence and privacy retention need a decision

Separate security audit from diagnostic logs. Define append-only/tamper-evident properties, signing/key custody, event minimization, redaction, retention, legal hold, access review and export controls. Audit must not become a covert indefinite copy of forgotten content.

### TAR-I-P1-003 — Remote model/provider data policy is incomplete

Remote inference is optional and disabled unless configured/authorized. Define data classification, permitted Scope, residency, provider retention/training policy, credential isolation, egress logging, timeout and provider compromise response. Model worker must not become an alternate authority or receive unapproved raw memory.

### TAR-I-P1-004 — Backup/restore quarantine is a correctness boundary

Restore must quarantine all restored canonical/derived/index/cache/context/delivery artifacts until current Forget, authorization, retention and target inventory control state has been replayed and verified. Backup catalog coverage and external recipient acknowledgements are separate from local database success.

## 4. Technology disposition

| Capability | Disposition | Conditions |
|---|---|---|
| Authenticated local IPC / remote mTLS | RECOMMEND as capability | H/I define binding and protocol; platform-specific implementation remains open. |
| OS-backed key store | RECOMMEND | Provide documented secure fallback and recovery/rotation. |
| Encryption at rest | NEEDS POLICY/THREAT-MODEL DECISION | Define threat model, keys, backups and cryptographic erasure. |
| Vetted cryptographic libraries | DECIDED constraint | No custom cryptography. Specific crate/algorithm requires review. |
| Append-only/tamper-evident audit | RECOMMEND | Retention/privacy design and key custody required. |
| Remote inference | DEFER / OPT-IN ONLY | I policy, residency and provider contract required. |
| Global Forget target inventory | CANDIDATE GOVERNANCE CONTRACT | Closed-world completeness and executable consumer evidence remain open. |

## 5. Resource and recovery matrix

Sizing must measure encrypted bytes, audit events/day, retention period, backup generations, blob duplication, key rotation overhead, restore throughput, revocation propagation delay and provider egress. No capacity or latency numbers are claimed.

| Failure | Required behavior | Test |
|---|---|---|
| Forged payload ActorRef | Reject; bind to authenticated transport principal | I-AUTH-01 |
| Stale PermissionEpoch | Fail closed at protected boundary | I-AUTH-02 |
| Revocation races publish | One serialized current decision; no stale visible artifact | I-RACE-01 |
| Restore stale backup | Quarantine, replay latest Forget/control ledger, verify before serving | I-RESTORE-01 |
| Missing target/recipient | Global completion remains UNKNOWN/INCOMPLETE | I-GLOBAL-01 |
| Key loss/rotation | Recover only through documented key ceremony; otherwise declared data-loss state | I-KEY-01 |
| Audit log tampering | Detect and alert; preserve evidence without leaking payload | I-AUDIT-01 |
| Remote provider outage/policy drift | Stop/degrade optional inference; no durable ingress loss | I-PROVIDER-01 |

## 6. Required sequence

1. Reconcile I ProducerDomainInventoryEpoch with D ProducerRegistryVersion/high-water and A/module ownership registry.
2. Define current authorization decision freshness and authenticated identity binding with H/D/E/G/C.
3. Define key custody, encryption, audit and backup/restore policies against explicit threat model.
4. Build restore-after-Forget, permission-revocation and target-omission fault suites.
5. Only then consider security acceptance of a deployment profile.

## 7. Final recommendation and non-claims

Conditionally accept TAB-001's security capability architecture as a candidate. Do not approve a concrete cryptographic stack, claim Global Forget completion, or claim physical erasure. No penetration test, key ceremony, restore drill, backup deletion, external recipient deletion, revocation race test or security certification was run.