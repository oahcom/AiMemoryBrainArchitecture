# Phase 3.8.2 — A HRC / RecoveryJoin / Phase 3.8 Cross-Owner Integration Review

- Reviewer perspective: A — Principal Integration Architect
- Review mode: **integration-session role simulation; not independent Owner signatures**
- Decision: **ACCEPT AS A COHERENT PROPOSED COMPOSITION WITH BLOCKING AMENDMENTS**
- Status: **PROPOSED / NOT FROZEN / TEST CANDIDATES NOT RUN**
- Language: English and Chinese are normative peers.

## 1. Exact source bundle

### Phase 3.8 contracts

| Role | Branch | Path | Blob |
|---|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 03-memory-brain/phase-3.8-d-publication-participant-and-terminal-contract.md | 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 |
| E | session-e-memory-compiler-2026-11-16 | 04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md | 475fee41e5eea527af4edefbfe88c58c86967d0a |
| I | session-i-security-governance-2026-11-16 | 09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md | 54bab0484bd232a5a258e65e34cc7425288b39a6 |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | reviews/storage-consistency/phase-3.8-storage-visibility-participant-and-atomic-outcome-contract.md | 175ee7b1349cfdb79a19898b311a88391ed88010 |

### H / Storage RecoveryJoin and tests

| Artifact | Branch | Blob |
|---|---|---|
| H RecoveryCutoff schema 1.0.4 | session-h-bmcp-protocol | d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1 |
| H RecoveryJoin schema 1.0.0 candidate | session-h-bmcp-protocol | dd3234aa1c74caf6d0e335875cd96e0b2b64082f |
| H semantic validator contract | session-h-bmcp-protocol | 9a2c3b856d1319e780932d75d2b0165021faf816 |
| HRC/JPF executable semantic suite | session-h-bmcp-protocol | f28834d73e055be411060f0c1093bd3dc0d865b9 |
| Wire interop candidate suite | session-h-bmcp-protocol | 1a4e754ba9bfa57eb973c6d39731e9f89443b323 |
| Schema integrity suite | session-h-bmcp-protocol | 5292d56661e938c905c61455e9ed53c4ff674c54 |
| H branch test workflow | session-h-bmcp-protocol | ea7a3d9c365b84352d3bac69da94fe0d510e46a4 |
| Storage bidirectional JoinProof contract | session-storage-consistency-forget-atomicity-2026-11-16 | 2882fa8eb4d5e7faca035866572cbe48ac5eeae0 |
| Storage serialization topology ADR | session-storage-consistency-forget-atomicity-2026-11-16 | 080433f8e13a500522bc2754da64057edb0ae9d8 |
| A deterministic conformance matrix | session-a-integration-2026-11-16 | c556125b279271c1cc57fca0b49584b5b1f302b2 |

### Role review artifacts

| Role | Artifact | Branch | Exact Blob | Simulated disposition |
|---|---|---|---|---|
| D | phase-3.8.2-d-recovery-join-and-visibility-exact-review.md | D branch | 1ef3a736cdbf59b27a017d6dd4aee9fe7be0b940 | ACCEPT WITH AMENDMENTS |
| E | phase-3.8.2-e-recovery-join-orchestration-exact-review.md | E branch | c2beb133de40e7c8281933dfa175ac7fa289bd5f | ACCEPT WITH AMENDMENTS |
| I | phase-3.8.2-i-recovery-join-trust-currentness-exact-review.md | I branch | 83cacf7575c2800593104ddb9a6e72f521a9576b | ACCEPT WITH AMENDMENTS |
| Storage | phase-3.8.2-storage-exact-review-and-topology-disposition.md | Storage branch | 7c09cfad1ca77ed51cf282dc0826c62d91eea4dd | ACCEPT WITH AMENDMENTS; ADR BLOCKED |

These are assistant-authored role simulations at the user's direction. They are not independently attributable repository Owner signatures or cryptographic attestations.

## 2. H disposition — HRC-01..25 executable candidate

H has converted the existing 25 semantic scenarios into named unittest methods and added:
- JPF-01..17: bidirectional request/admission/participant joins, owner row identity, no-effect/out-of-scope dispositions, cardinality, currentness and JF-10 same-participant terminal mapping;
- WIRE-01..10: strict duplicate-key parsing, absent/null distinction, deterministic test bytes, counter representation, unknown critical field, GID typing and domain separation;
- SCHEMA-01..09: six recovery message families, strict object boundaries, RecoveryJoin required edge sets, JF-10 tuple and owner request/admission completeness.

Total committed candidate suite: **64 unittest methods** (25 HRC + 17 JPF + 10 WIRE + 9 SCHEMA).

The RecoveryJoin schema now has:
- six separate owner request/admission completeness states (I/D/C request and I/D/C admission);
- owner_request_dispositions for every request row;
- OwnerAdmissionRef separated from OwnerEntryRef;
- C primary admission anchor plus distinct I/D/C/Storage evidence edges;
- explicit no-effect/out-of-scope proof conditions;
- exact JF-10 prepared participant / GID / DB incarnation / attempt / ledger / I/Storage terminal fields.

**Execution boundary:** the tests are committed but no CI workflow run is available for the current candidate. The semantic suite uses a TEST-ONLY digest helper; production canonicalization, signatures, key trust and cross-language byte interoperability remain OPEN. No PASS is claimed.

## 3. Storage disposition — bidirectional JoinProof

Storage has defined the acyclic record chain:

ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest → RecoveryJoinProofDigest → Owner Gate Release / RecoveryEpochCompleted.

The JoinProof has two required directions:

1. Owner request/admission ledger rows → exact COC participant or explicit no-effect/out-of-scope disposition.
2. Every COC participant → exact primary C admission plus all applicable I receipt/terminal, D barrier/lineage, C reservation/provider outcome and Storage JF-10 evidence.

The proof also binds exact COC prefix P, batch/manifest digests, I/D/C snapshot refs and digests, owner roots/high-waters/generations and anti-rollback anchors. Storage may persist/commit the JoinProof; it cannot issue I/D/C release. Each owner must revalidate and perform its own release CAS.

This closes the conceptual one-way-join gap, but semantic validators, owner ledgers, live COC enumeration and owner currentness CAS are not implemented or evidenced.

## 4. Cross-owner reconciliation

### 4.1 Compatible elements

- D PublicationParticipantRef, C ParticipantIntentRef, StorageVisibilityParticipantRef and Storage PreparedParticipantRef/GID remain distinct nominal types.
- Storage durable hidden prepare precedes D publication admission.
- I's consumed CommitAuthorizationReceipt / ICommitAuthorizationProof is pre-commit evidence; ITerminalProof is post-Storage-outcome closeout evidence. No circular proof dependency remains.
- D Fence, I revocation, C provider-egress gate and Storage visibility are independent authorities.
- Request rows, admission rows and COC participant rows are separately enumerated and then joined; none is inferred from another.
- NOT_REGISTERED cannot carry participant identity and requires no-effect proof or remains a release blocker.
- RecoveryEpochCompleted is a COC observation, not an owner release or business outcome.

### 4.2 Blocking amendments by Owner

| Owner | Blocking amendment | Why it blocks freeze |
|---|---|---|
| D | Add exact D per-Fence ForgetOperationRef/FenceGeneration/lineage manifest/barrier-member/terminal proof binding or a strict signed-proof dereference contract | Generic evidence refs alone do not expose D scope/lineage semantics |
| E | Gate restore, queue dispatch, protected dereference, retry replay and publication on current RecoveryJoin + owner release + restore reconciliation | E local lifecycle must not resume before recovery gate is complete |
| I | Approve signature/trust/key/historical verification and exact currentness CAS for OwnerAdmissionRef + OwnerEntryRef, inventory epoch and receipt issue/consume | Structural validity is not cryptographic or current authorization proof |
| Storage | Select and prove actual D/Storage serialization topology, read-path enforcement, atomic pointer/outcome/outbox, HA/failover/restore | Logical composition is not physical linearizability |
| H | Implement wire-to-normalized adapters and six validators; approve exact canonical bytes/field mapping; run differential cross-language vectors | Current tests are candidates over normalized models, not complete interoperable implementation |

## 5. Physical topology decision

Storage's topology ADR is **ADR-BLOCKED / NO TOPOLOGY SELECTED**:
- Option A: one serializable transaction domain per Canonical Memory authority, conditional preference only if actual D/Storage runtime shares it and preserves semantic ownership.
- Option B: separate D/Storage services with a named durable linearizable coordinator and executable failover proof.
- Check-then-write, process mutex, queue order, eventual replica and outbox-only coordination are rejected.

Issue #10's PostgreSQL 18.7 CI probes are candidate-engine capability evidence, not proof of the actual deployed Canonical Authority runtime or D/Storage shared transaction domain. Gate B/C and JF-10 P0 remain open under Issue #10.

## 6. Required deterministic test campaign

A's matrix includes:
- 12 two-order race cases;
- 12 crash / ACK-loss cases;
- 12 failover / restore cases;
- mapping to HRC-01..25, JPF-01..17, WIRE-01..10 and SCHEMA-01..09.

Tests must assert actual authoritative ledgers, owner-local high-waters, participant identity, DB incarnation/GID, visibility pointer, private staging, outbox/provider side effects and exact proof digests. Unknown remains UNKNOWN; timeout/missing row/lease expiry/process death never infers terminality.

No test campaign has been run. H's current candidate workflow has no reported run.

## 7. A integration decision

**ACCEPT AS A COHERENT PROPOSED COMPOSITION WITH BLOCKING AMENDMENTS.**

The HRC/JoinProof work materially advances the recovery contract: it now has explicit request-side and admission-side completeness, both directional joins, row identity binding, JF-10 sub-join and 61 executable candidate test methods. Storage's digest chain avoids a circular batch/manifest/JoinProof dependency.

The remaining blockers are substantive, not editorial:
1. D per-Fence evidence typing;
2. E recovery-gate integration;
3. I trust/key/currentness approval;
4. H wire adapter, canonicalization, cryptographic and differential interoperability;
5. Storage physical serialization topology and read-path/HA/restore evidence;
6. actual CI and deterministic fault-injection results;
7. independent Owner decisions on these exact latest blobs.

No schema freeze, implementation/conformance PASS, merge, production activation, Global Forget completion or physical-erasure claim is authorized.

## 8. 中文集成裁决

A 认为 HRC-01..25 与 RecoveryJoin 的逻辑组合方向成立。当前 JoinProof 已同时覆盖 COC ParticipantManifest、I/D/C Request Ledger、I/D/C Admission Ledger，并区分 OwnerAdmissionRef 与 OwnerEntryRef，明确 C Primary Admission Anchor、I/D/C 证据边、NOT_REGISTERED 无副作用证明及 JF-10 同一 Prepared Participant 终态映射。61 个 unittest 候选已提交，但尚无 CI 执行结果。

四方精确版本角色审查均为 ACCEPT WITH AMENDMENTS 的模拟结论，不是独立 Owner 签名。D 的 per-Fence Lineage Proof、E 的 Restore/Dispatch Gate、I 的 Cryptographic Trust/Currentness、Storage 的真实事务拓扑和 HA/Restore、H 的 Wire Adapter/Canonicalization/跨语言互操作仍为阻塞项。

最终裁决：**接受为逻辑一致的提案组合，但保留阻塞项；不冻结、不合并、不启用生产。**


## 9. Follow-up schema refinement

H has added row-digest and typed owner-evidence requirements to RecoveryJoin 1.0.0:
- request disposition now binds both OwnerRequestDigest and OwnerEntryDigest;
- NOT_REGISTERED admission disposition binds operation identity/digest, scope and gate/scope generations;
- D lineage/barrier evidence requires ForgetOperationRef, FenceGeneration, LineageManifestRef/Digest and BarrierMemberRef;
- I receipt/terminal evidence requires PolicyDomain, PermissionEpoch, inventory epoch, issuer key and authorization receipt;
- C provider and Storage prepared/resolution evidence carry their owner-specific tuple fields.

The latest H schema Blob is dd3234aa1c74caf6d0e335875cd96e0b2b64082f. The latest HRC suite Blob is f28834d73e055be411060f0c1093bd3dc0d865b9. The Storage JoinProof contract is now Blob 2882fa8eb4d5e7faca035866572cbe48ac5eeae0.

These are schema and test-candidate refinements only. No CI run, cross-language interop PASS or owner signature is claimed.
