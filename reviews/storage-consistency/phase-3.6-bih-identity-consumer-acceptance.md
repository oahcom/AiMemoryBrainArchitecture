# Phase 3.6 — BIH Identity Trust Consumer Acceptance (Storage Owner-Side)

- Status: **DESIGN-LEVEL ACCEPTANCE RECORDED; RUNTIME CONFORMANCE NOT VERIFIED**
- Owner: Storage consistency / Forget Atomicity
- Branch: `session-storage-consistency-forget-atomicity-2026-11-16`
- This record accepts BIH semantics at Storage's durable publication/visibility boundary. It does not approve I governance policy, close JF-10, or claim cross-authority atomicity is implemented.
- B source Blob: `0a6b78a842e550b58533b797cdfcd2d954ed6826`.
- H source Blob: `9845c97ac43d7888732afafe12e28850ec02add8`.
- I source Blob: `0cbf6bb7480db873790c454817593a9b1c5548ba`; execution addendum Blob `1f5d2e4aba7afa75c0696f3c8f025b0cb903e0ad`.

## 1. Explicit design acceptance

Storage accepts the following semantics for protected durable publication:

1. Typed PrincipalRef, ActorRef, ProducerRef, AdapterRef, ScopeRef and EnvironmentRef remain distinct; identity fields in payloads are claims, never authentication.
2. Storage accepts authenticated operation context only from a trusted internal boundary established from H protected verifier context and I authoritative resolution. Storage must not infer Principal/Actor/workload identity from caller-supplied payload fields.
3. ActorRef is immutable, verifier-produced and operation-specific. Storage records it as attribution, not as a credential or grant.
4. ScopeBindingSet is canonical, non-empty and role-tagged whenever the operation profile is scoped. ScopeRef is not permission. Unresolved or unauthorized Scope/Environment bindings block protected publication.
5. Every protected publication binds the complete applicable authorization tuple, including PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, policy domain, PermissionEpoch and authenticated workload/session context.
6. I is the sole logical authority for PermissionEpoch. Storage validates currentness at the final visibility boundary. Stale, gapped, unknown, incomparable or unverifiable epochs block publication; offline/stale authorization leases and cached ALLOW without online currentness proof are prohibited.
7. PermissionEpoch and D ForgetFence/ForgetFenceGeneration are independent checks. Storage also validates D's owner-local fence/barrier state where required; neither check substitutes for the other.
8. Forged/mismatched payload identities, unknown issuer/workload, malformed refs, unsupported security-critical fields and ambiguous authorization outcomes fail closed. Unsupported capability or missing evidence is not success.
9. Storage accepts I's single-use `CommitAuthorizationReceipt` contract. The receipt binds policy domain, PermissionEpoch, PrincipalRef, ActorRef, action, ResourceRef, purpose, audience, ScopeBindingSet digest, EnvironmentRef, DelegationChainRef, operation ID, operation digest, owner boundary and decision ID. Receipt replay, changed digest/boundary, stale epoch, expiry or unknown status blocks visibility.
10. Storage's durable transaction records receipt ID, I decision ID, sequencer position, PermissionEpoch, operation digest, Storage transaction/commit cursor and terminal outcome alongside the VisibilityPointer, PublicationReceipt, idempotency outcome and same-transaction Outbox.
11. `COMMIT_WON` is the I authorization-ordering outcome, not proof of Storage visibility. Storage visibility occurs only when its own durable transaction commits the VisibilityPointer and PublicationReceipt. `REVOCATION_WON` forbids visibility. `INDETERMINATE_ABORTED` is never success and leaves staged data private.
12. The cross-authority relationship between I's sequencer and Storage's durable transaction remains JF-10 P0 OPEN until I formally accepts/revises the recovery protocol and executable crash/failover evidence proves forward recovery.

## 2. Consumer field mapping and boundary obligations

| Required field / behavior | Storage obligation | Fail-closed result |
|---|---|---|
| PrincipalRef | Persist exact authenticated subject binding in protected publication record | unresolved/mismatched/revoked => no visibility |
| ActorRef | Persist immutable verifier-attributed operation actor | caller-minted/stale/mismatched => reject |
| Producer/Adapter identity | Persist registered producer/workload and concrete instance binding where applicable | unknown/revoked/replaced => reject/quarantine |
| ScopeRef | Persist canonical role-tagged ScopeBindingSet and digest | missing/ambiguous/unauthorized => no visibility |
| EnvironmentRef | Persist resolved exact EnvironmentRef when required by operation profile | unresolved/unapproved cross-environment => deny |
| Authenticated transport binding | Accept only verified internal context; payload mirrors cannot override it | untrusted context => reject |
| PermissionEpoch | Verify current I policy-domain epoch at final visibility gate | stale/gap/offline/unknown => no visibility |
| Revocation | Honor I sequencer ordering and receipt terminal result | REVOCATION_WON/indeterminate => no visibility |
| Forged payload identity rejection | Compare claims with authenticated bindings and registry resolution | mismatch => reject and audit |
| Unknown/Unsupported | Preserve Unknown; no silent downgrade or inferred success | quarantine/private staging |

## 3. Transactional visibility semantics

Within the selected per-Canonical-Memory-Authority transactional database boundary, Storage's owner-side durable commit must atomically include:
- consumed single-use receipt identity and immutable operation digest;
- Storage idempotency/terminal outcome;
- VisibilityPointer update;
- PublicationReceipt;
- relevant durable publication metadata and commit cursor;
- Outbox record.

Large payloads remain private staged objects until the transaction commits. A pointer is the visibility authority. A Storage transaction rollback means no new visible pointer. This local atomicity does **not** by itself prove atomic ordering with I's sequencer; that is exactly the unresolved JF-10 cross-authority recovery problem.

## 4. Inventory Seal / Global Forget

Storage recognizes I's ProducerDomainInventoryEpoch and TargetInventorySeal as global inventory authority, distinct from Storage backup catalog, restore quarantine and local object/version accounting. Storage operators own backup/restore execution evidence, but cannot self-certify global inventory completeness or I's Global Forget terminal state. Restore remains quarantined until the current independent Forget/revocation control ledger is replayed and verified. Missing backup, replica, archive, recipient or physical-erasure evidence remains Unknown.

## 5. Outstanding evidence and gates

- I governance approval GOV-01..10 remains GOVERNANCE-BLOCKED.
- I-owned Storage consumer register remains OPEN until I records/recognizes this exact Storage Owner artifact.
- JF-10 remains P0 OPEN: I ACCEPT/REVISE/BLOCK, sequencer durability/lookup semantics, receipt consumption and crash/failover protocol are outstanding.
- No production database/vendor/version, migration, isolation proof, transaction trace, failover run or executable Storage integration test is claimed.
- Required tests: forged identity; stale/gapped epoch; receipt replay and changed-digest conflict; revocation-before/after ordering; Storage crash before transaction, after transaction before ACK, and during failover; duplicate retry; pointer/receipt/outbox atomicity; backup restore quarantine and control-ledger replay.

**Final state:** Storage design-level acceptance only. Runtime conformance NOT VERIFIED; JF-10 OPEN; no governance approval, runtime PASS or Phase 3.6 Gate passage is claimed.
