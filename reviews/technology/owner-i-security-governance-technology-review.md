# I — Security & Governance Technology Architecture Review

- Document: TAR-I-001
- Review date: 2026-11-17
- Owner boundary: I — Security, Identity & Governance
- Execution: centralized delegated static architecture review; not an independent human-owner attestation.
- Branch: `session-i-security-governance-2026-11-16`
- **Reviewed branch HEAD (refreshed):** `0abd1a26008d90c15cbb7d6ebae0f7325f7c1c1b`
- TAB-001 main HEAD: `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f`; blueprint blob: `7b6f2d139217dbe13ab3a3af31bfbff525f20e71`
- TAR-AI-001 task blob: `5a813edeccf7190d66dfd71a96ca581c48f8a4cb`
- I Principal/Actor/Authorization blob: `03765efac4bb1153f303ce0030f9e277d602e81d`
- I global Forget inventory blob: `9100061fa986fb6676656169de3fcf9fc1c72664`
- I Forget/retention/backup/erasure policy blob: `f14cb2149ca3f817229533005ab89dbdc7f0b3a8`
- I threat model blob: `4227ac0e26228ca3504589efdee022b5d0802e12`
- I PermissionEpoch formal confirmation blob: `bae6a24fe3a374bc816993979a8fa9af52517dea`
- I JF-10 v2 disposition blob: `8069ff86988396442c8d9dc3fd58653683abe2f3`
- I COC durable-protocol acceptance blob: `528945f82e3e25258052240a7a4ba43753ae6cf8`
- Phase 3 D/E/H/I review main blob: `edaccb802e0425f2d47bd4b613fab4dfde107144`
- Existing report blob replaced: `3558856fcc109efc6ed1cda3a53ac7900a89fd31`

## Executive Summary

**Verdict: CONDITIONAL PASS for the security architecture direction; BLOCKED for deployable security acceptance and Global Forget completion.** TAB-001's cross-cutting security boundary is directionally correct, but naming OS key stores, encryption, authenticated IPC or audit mechanisms does not constitute a security design. The latest I contracts materially strengthen the identity and JF-10 boundary: PermissionEpoch is I-owned, opaque and policy-domain scoped; protected final operations require current I sequencer evidence; the accepted JF-10 v2 profile is single-policy-domain only. These are design decisions, not a deployed sequencer, key-management system, global inventory seal or restore-tested erasure workflow.

B has formally approved ActorRef/ScopeRef/EnvironmentRef semantic mapping. This closes the B semantic type mapping dependency, but does not freeze H wire representation or authorize I policy deployment. I's ProducerDomainInventoryEpoch and target seal remain candidate governance contracts; D's per-operation barrier and ForgetFence remain separate.

## Review Scope

Reviewed TAB-001 security, model-provider, transport and backup/restore sections against I's Principal/Actor/Authorization, global target inventory, Forget/retention/erasure, threat model, PermissionEpoch formal confirmation, JF-10 v2 disposition and COC boundary acceptance. Cross-checked D/E owner artifacts and Phase 3 cross-module review. Static document review only; no penetration test, key ceremony, restore drill, revocation race, external-recipient deletion or implementation inspection was performed.

## Six-Dimension Review Conclusions

| Dimension | Verdict | Assessment |
|---|---|---|
| 1. Technical requirements & workload fit | CONDITIONAL | Complete authenticated tuple, deny/indeterminate behavior, per-boundary reauthorization and global Forget evidence vector are specified. Threat coverage, policy SLOs, data classification and jurisdiction-specific controls need deployment profile and validation. |
| 2. Component dependencies & boundaries | CONDITIONAL | I owns identity trust, authorization, PermissionEpoch, ProducerDomainInventoryEpoch, inventory seal, retention and global completion. B owns reference semantics; H transport binding; D canonical fence/barrier; E/F/G/C local execution/evidence; Storage backup/restore. |
| 3. Candidate technology selection | OPEN | Cryptographic library, OS key custody, encryption-at-rest, audit integrity, IPC/mTLS and policy sequencer implementation are not selected. Capability requirements must precede crate/algorithm selection. |
| 4. Resource constraints | NOT MEASURED | Encryption throughput, audit growth, retention/backup bytes, restore rate, key rotation and sequencer latency/availability are unmeasured. |
| 5. Failure recovery & operational safety | BLOCKED for security acceptance | I specifies fail-closed and JF-10 recovery semantics; no coordinator/participant deployment, key recovery, restore quarantine or global inventory audit is evidenced. |
| 6. Interface & compatibility | CONDITIONAL / GLOBAL FORGET OPEN | B's ActorRef/ScopeRef semantics are approved; H wire mapping and I policy activation remain open. PermissionEpoch, ProducerDomainInventoryEpoch, ForgetFenceGeneration, D work high-water, COC positions and Storage XID must remain distinct. |

## Component Dependency Analysis

- **B ↔ I:** B owns typed meaning for ActorRef, ScopeRef and EnvironmentRef; I owns issuer trust, Principal resolution, delegation, policy and revocation. B's formal semantic approval is not a permission grant.
- **H ↔ I:** H authenticates/binds transport and carries security context unchanged. I decides authorization. Payload ActorRef/ProducerId/AdapterId are claims, never credentials.
- **D/E ↔ I:** D owns ForgetFence and work/dependency barrier; E owns compiler producer lifecycle. I owns PermissionEpoch and single-policy-domain CommitAuthorizationReceipt sequencing. Both D and I gates apply; neither token substitutes for the other.
- **F/G/H/C:** every retrieval, Context delivery, Adapter apply/reconnect and final inference boundary must consume current authorization and exact Forget evidence as applicable.
- **Storage/COC:** Storage owns XID, prepared participant and reader-visible VisibilityPointer; COC records causal order/participant accounting only. I's COC acceptance does not transfer I's sequencer authority to COC.
- **Global inventory:** enumerate producers, derivatives, indexes, caches, Context, Adapters, providers, backups, replicas, logs and human exports. An inventory seal proves enumeration at a point in time, not cleanup.

## Candidate Technology Comparison

| Concern | Candidate | Alternative | Trade-offs / recommendation |
|---|---|---|---|
| Credential/key custody | OS-backed key store (platform credential vault/keychain/TPM where available) | Encrypted local key file / user passphrase | OS vault improves access control and lifecycle integration but varies by platform and backup behavior. File-based fallback is portable but raises permissions, unlock and recovery risks. Require threat-modelled fallback; never store raw keys in config/logs. |
| Encryption at rest | Vetted AEAD/storage encryption with envelope-managed data keys | Filesystem-only encryption | Application-level envelope encryption supports per-scope/key rotation and cryptographic erasure but adds key lifecycle and backup complexity. Filesystem encryption is simpler but does not protect exported backups or copied blobs. Decide after threat model; no custom crypto. |
| Authenticated IPC | OS peer credentials + local socket ACL; mTLS for remote | Loopback HTTP without mutual auth | Peer credentials reduce local token handling but need platform-specific verification; mTLS works across hosts but adds certificate lifecycle. Plain loopback is not identity proof. H/I must specify binding and replay protections. |
| Authorization freshness | I online policy-domain sequencer + opaque PermissionEpoch + single-use CommitAuthorizationReceipt | Cached ALLOW / TTL / asynchronous invalidation only | Online sequencer preserves revocation ordering at cost of latency/availability. Cached ALLOW improves availability but violates current I Phase 3.6 profile for protected irreversible operations. Fail closed on unavailable/unknown state. |
| Audit | Append-only, integrity-protected event ledger with separated security audit | Ordinary application logs | Dedicated ledger supports evidence verification but costs storage and retention operations. Logs are easier but mutable/noisy and risk payload leakage. Keep security evidence separate, minimized and tamper-evident. |
| Global Forget inventory | Versioned registry + sealed digest + per-target evidence vector | Best-effort broadcast/delete | Closed-world inventory can expose omissions and unknowns; requires owner/recipient registration and reconciliation. Broadcast-only cannot prove no missed target. |
| Remote inference | Explicit opt-in provider adapter with classification/residency/retention controls | Local isolated inference only | Remote may reduce local VRAM but adds egress, provider retention and jurisdiction risks. Default off until provider policy/contract approved. |

## Resource Budget Analysis

No measured capacity is available. Estimate:
- encrypted storage = canonical + blobs + indexes + audit + backup generations + rotation overlap;
- audit volume = protected operations/day × evidence bytes × retention period;
- restore capacity = backup bytes / verified restore throughput, plus replay of fence, inventory, permission and participant ledgers;
- key operations = encrypted objects/rotations and per-scope key count;
- authorization latency = I sequencer round trip + durable decision commit + owner participant transaction.

Measure CPU overhead for encryption/decryption, p95/p99 policy-sequencer latency, audit write amplification, disk growth, backup overlap, restore throughput and outage backlog. The 12–16 GB VRAM envelope is not an I-owned budget; remote/local model data policy must ensure model choice does not bypass authorization.

## Failure & Recovery Matrix

| Failure | Required behavior | Required evidence |
|---|---|---|
| Forged payload identity / unknown issuer | Reject and audit; verifier-bound Principal/Actor only | Adversarial identity tests |
| Permission revocation races final gate | I sequencer yields COMMIT_WON or REVOCATION_WON for exact operation; unknown remains blocked | Deterministic revocation interleaving |
| I sequencer/COC outage | Affected operations enter PENDING_COC_CUTOFF/UNKNOWN; no stale cached ALLOW | Crash/recovery and cutoff reconciliation |
| JF-10 participant in doubt | Keep bytes private; retain XID/locks; recover same XID from durable I decision | Crash after I decision / before Storage commit |
| Missing or changed inventory target | Invalidate seal/reopen; global completion UNKNOWN | Inventory omission/epoch-change tests |
| Offline/unsupported Adapter or recipient | UNKNOWN unless narrowly approved scoped PolicyException | Target-state evidence tests |
| Restore from stale backup | Quarantine all content; replay current fence, permission, retention and inventory control state before serving | Restore-after-Forget drill |
| Key loss/rotation/compromise | Execute documented ceremony or declare controlled data-loss state; no silent plaintext fallback | Key rotation/recovery exercise |
| Audit tampering | Detect, alert and preserve minimal evidence without payload leakage | Integrity verification/tamper test |
| Provider policy drift/outage | Stop remote inference; retain accepted data locally; do not relax policy | Provider contract/egress tests |

## Interface Compatibility Findings

1. B's formal ActorRef/ScopeRef/EnvironmentRef semantic mapping is approved at B blob `3a1e77889cd9a90cd5822d9f0cb3437880868706`; H still owns wire encoding and I owns policy interpretation.
2. PermissionEpoch is opaque and monotonic only within one I PolicyDomainRef. Cross-domain epochs are incomparable. The I Phase 3.6 profile prohibits offline authorization leases or stale-epoch grace for protected irreversible operations.
3. ProducerDomainInventoryEpoch is I's global producer/recipient catalogue version; D ProducerRegistrationHighWater/WorkItemBarrier tracks concrete work in one Forget operation. Both are required.
4. ForgetFenceGeneration is D-owned; it must be checked independently from PermissionEpoch. IndexWatermark, ContextVersion, AdapterCapabilityEpoch, Storage XID and COC positions are separate.
5. JF-10 v2 is accepted by I for one PolicyDomainRef only. Multi-policy-domain atomicity remains BLOCKED / NOT ACCEPTED. I COMMIT_WON is authorization ordering, not Storage publication; only Storage same-XID commit/readback of PublicationReceipt proves visibility.
6. COC records order and participant observations; it cannot mint I authorization, decide I revocation, or substitute for I's durable sequencer and receipt-consumption ledger.

## Blocking Findings

- **P0 — TAR-I-P0-001:** Global Forget target inventory completeness, inventory seal and target evidence mapping are not implemented/verified; global completion cannot be inferred from D local barrier.
- **P0 — TAR-I-P0-002:** JF-10 single-domain sequencer/receipt-consumption and prepared participant recovery are design-accepted but not implemented/tested; multi-domain profile remains blocked.
- **P1 — TAR-I-P1-001:** Key custody, encryption hierarchy, rotation, recovery and cryptographic-erasure scope are not operationally specified.
- **P1 — TAR-I-P1-002:** Security audit integrity, minimization, retention, legal hold and export controls require an ADR/profile.
- **P1 — TAR-I-P1-003:** Remote provider classification, residency, retention/training, credential isolation and egress controls remain OPEN.
- **P1 — TAR-I-P1-004:** Restore quarantine and replay ordering across canonical, derived, indexes, Context, Adapters, backups and external recipients have no drill evidence.
- **P1 — TAR-I-P1-005:** I registry/epoch sequencer availability, failover and authoritative lookup durability are not validated.

## Required ADRs

1. Security key custody and envelope-encryption/backup-key lifecycle ADR.
2. Local IPC and remote authentication profile ADR with H transport binding.
3. Audit evidence integrity, retention, minimization and legal-hold ADR.
4. Remote inference/provider data processing and residency policy ADR.
5. Global Forget inventory/evidence and restore-quarantine operational profile.
6. I sequencer durability/failover/retention ADR for JF-10 single-policy-domain profile.

## Required Prototypes and Tests

- Forged ActorRef/ProducerId, issuer/key/audience/delegation mismatch and scope-confusion tests.
- PermissionEpoch gap, revocation-before/after-owner-gate and same-operation replay/digest-conflict tests.
- JF-10 crash matrix: I decision durable before Storage commit; Storage commit before ACK; I/COC outage; same-XID recovery; stale replica rejection.
- Inventory seal omission, epoch mutation, late target discovery and unknown/offline target tests.
- Restore-after-Forget with stale index/cache/Context/Adapter and backup/WAL/object-store artifacts.
- Key rotation/loss/backup recovery, audit tamper detection, remote egress/policy drift tests.
- All tests above remain NOT RUN unless a reproducible execution artifact is separately attached.

## Verdict

**CONDITIONAL PASS** for the candidate security architecture direction; **BLOCKED** for security deployment acceptance and Global Forget completion. I's JF-10 and COC acceptances are technical design-boundary decisions only.

## Evidence and Exact SHAs

| Source | Commit SHA | Blob SHA |
|---|---|---|
| TAB-001 main | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` |
| TAR-AI-001 tasks main | `3799616bea65bf5ffd1cd0bdb321cd4c6f591b7f` | `5a813edeccf7190d66dfd71a96ca581c48f8a4cb` |
| I Principal/Actor/Authorization | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `03765efac4bb1153f303ce0030f9e277d602e81d` |
| I Global Forget inventory | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `9100061fa986fb6676656169de3fcf9fc1c72664` |
| I Forget/retention/backup policy | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` |
| I threat model | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `4227ac0e26228ca3504589efdee022b5d0802e12` |
| I PermissionEpoch confirmation | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `bae6a24fe3a374bc816993979a8fa9af52517dea` |
| I JF-10 v2 disposition | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `8069ff86988396442c8d9dc3fd58653683abe2f3` |
| I COC durable protocol acceptance | `4b1ef1c607089db1c886ae9af82e8cab5d9c6af3` | `528945f82e3e25258052240a7a4ba43753ae6cf8` |

This report does not approve TAB-001, declare global Forget complete, or claim implementation/security-test evidence.

## 8. Reassessment — Global Forget target inventory reference model (2026-11-17)

I added an in-memory Global Forget target-inventory/CEV reference model. Evidence: `09-security-governance/phase-3.6.4-global-forget-reference-model-evidence.md`, commit `674b9496bcb866fdaf725108104ce55f6d127528`; model Blob `5233da028e409ec3f41848582dad73a923e7155b`; tests Blob `091f9450adf49a2a9f9ec8a2fa4470918023f765`; CI run `43962873109`, job `133634616584`, commit `73a0bff13b531b5b9feaeeec1887db31d6266589`.

**Result: 25/25 logical reference-model tests PASS.** Covered inventory seal authority/gaps, epoch invalidation, target discovery, evidence binding, ACK-vs-delete distinction, Unknown/Unsupported, D barrier, backup restore quarantine/control replay, physical-erasure action, independent PolicyException approval/expiry, NotApplicable proof and owner-local evidence limits.

Limit: no production inventory registry/seal, actual target API, external recipient evidence, production restore, formal I36 governance approval, PolicyException approval or physical-erasure proof is claimed. Global Forget remains OPEN / NOT COMPLETED.

## 9. TAR-AI-001 reassessment — PreparedParticipantReceipt signature trust boundary (2026-11-17)

The I branch advanced after the original technology review. This addendum consumes the current branch's security review:
- Source: `reviews/security-governance/phase-3.6.3-prepared-participant-signature-trust-review.md`
- Source commit: `0abd1a26008d90c15cbb7d6ebae0f7325f7c1c1b`
- Source blob: `7545dc1f74e6cfda17701b9c053fe342a8b01d44`
- Disposition: **CANDIDATE / NO APPROVAL**; role-simulated assessment, not an independently authenticated I-session signature.

### Additional blocking findings

1. **I-1 — Signed-byte contract is incomplete.** The PreparedParticipantReceipt/COC protocol does not yet define a normative complete signed envelope and exact signature preimage. The protected envelope must bind payload type/schema, issuer, subject, owner authority, audience, purpose, key identity/version, algorithm/canonicalization/digest profiles, payload digest and issue time. The signature must cover a domain-separated canonical representation of the protected header and complete payload. Duplicate keys, absent-vs-null, Unicode normalization, numeric encoding, field ordering and unknown critical fields require explicit rules.
2. **I-2 — Trust context binding is incomplete.** Issuer, signing service, owner authority, exact Storage participant, target environment, audience, message purpose/type and protocol version must be bound. A valid signature alone does not establish authority to attest a particular participant or operation.
3. **I-3 — Key lifecycle and historical verification are OPEN.** Generation/custody, activation, rotation, suspension, revocation, compromise, retirement, destruction, recovery, dual control, audit and historical key-status verification need normative policy.
4. **I-4 — Revocation and verification-time semantics need closure.** Verification must distinguish signing-time validity from current trust, preserve verifiable key-status evidence and fail closed when trust history is unavailable or ambiguous.
5. **I-5 — Receipt replay and cross-purpose substitution must be rejected.** Receipts must be bound to exact participant/GID/XID, operation, environment and single-use consumption state. A cloned/restored consumed-receipt snapshot must not authorize a second consumption.
6. **I-6 — Authority types must remain non-substitutable.** Storage PREPARED evidence cannot be promoted into I COMMIT_WON authorization; a COC statement cannot be treated as I authorization; I terminal proof must bind the exact Storage participant and GID.

### Updated technology and compatibility disposition

- I owns authorization receipt issuance/consumption, PermissionEpoch, revocation ordering, terminal decision, I key policy and gate release.
- Storage owns its prepared participant, GID/native XID mapping, database identity and visibility resolution.
- H owns wire schema and canonical serialization implementation under I-approved policy.
- COC stores references/proofs and orders events; it cannot mint or reinterpret I authority.
- No cryptographic algorithm suite, canonicalization profile, key custody implementation or historical verification policy is approved by this addendum.
- JF-10 single-PolicyDomain scope remains the accepted design profile; multi-PolicyDomain atomicity remains blocked.

### Additional required ADRs and tests

- Signed envelope, domain separation, canonicalization and digest-profile ADR jointly owned by I/H within their authority boundaries.
- Key custody, lifecycle, revocation and historical verification ADR owned by I.
- Participant/GID/XID binding and single-use receipt-consumption contract with Storage/COC.
- Golden signed-byte vectors; duplicate-key and Unicode/numeric canonicalization tests; wrong issuer/audience/purpose/environment substitution tests; key rotation/revocation/compromise historical-verification tests; receipt replay after backup/restore; and same-XID prepared-participant recovery tests.

### Updated verdict

**CONDITIONAL PASS** for candidate security architecture direction; **BLOCKED** for deployable security acceptance, signed-receipt trust approval, JF-10 application recovery and Global Forget completion. This addendum does not approve the signature profile or claim implementation/security-test evidence.

