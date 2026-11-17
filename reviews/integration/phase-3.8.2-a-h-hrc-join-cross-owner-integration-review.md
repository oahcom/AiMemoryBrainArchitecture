# Phase 3.8.2 — A HRC / RecoveryJoin / Phase 3.8 Cross-Owner Integration Review

- Reviewer perspective: A — Principal Integration Architect
- Review mode: integration-session role simulation; **not independent Owner signatures**
- Decision: **ACCEPT AS A COHERENT PROPOSED COMPOSITION WITH BLOCKING AMENDMENTS**
- Status: **H CANDIDATE TEST SUITE PASS; PHYSICAL / PRODUCTION CONFORMANCE OPEN**
- Language: English and Chinese are normative peers.

## 1. Exact source bundle

### Phase 3.8 owner contracts

| Role | Branch | Blob |
|---|---|---|
| D — Publication Participant and Terminal Contract | session-d-memory-brain-2026-11-16 | 17e53890dd6cce9bea9eacc1be2e64b0ef55ac78 |
| E — Publication Orchestration, Retry and Recovery Contract | session-e-memory-compiler-2026-11-16 | 475fee41e5eea527af4edefbfe88c58c86967d0a |
| I — Commit Authorization Receipt and Revocation Sequencer Contract | session-i-security-governance-2026-11-16 | 54bab0484bd232a5a258e65e34cc7425288b39a6 |
| Storage — Visibility Participant and Atomic Outcome Contract | session-storage-consistency-forget-atomicity-2026-11-16 | 175ee7b1349cfdb79a19898b311a88391ed88010 |

### H / Storage RecoveryJoin and test bundle

| Artifact | Branch | Blob |
|---|---|---|
| H RecoveryCutoff schema 1.0.4 | session-h-bmcp-protocol | d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1 |
| H RecoveryJoin schema 1.0.0 candidate | session-h-bmcp-protocol | dd3234aa1c74caf6d0e335875cd96e0b2b64082f |
| H semantic validator contract | session-h-bmcp-protocol | 6f66a72a2d0aa43af338ff9e22d650d47aa2bd80 |
| HRC/JPF semantic suite | session-h-bmcp-protocol | 60a2f4db4bd12f2131ecd147db9bbe328da6db50 |
| Wire interop candidate suite | session-h-bmcp-protocol | 1a4e754ba9bfa57eb973c6d39731e9f89443b323 |
| Schema integrity suite | session-h-bmcp-protocol | 67aba74c120f2916d768e7b01c45408ee2624f3a |
| H branch workflow | session-h-bmcp-protocol | ea7a3d9c365b84352d3bac69da94fe0d510e46a4 |
| Storage bidirectional COC/Owner Admission JoinProof | session-storage-consistency-forget-atomicity-2026-11-16 | 668faeb20e3e9cb907a8d1061635b12162f3dbe2 |
| Storage serialization topology ADR | session-storage-consistency-forget-atomicity-2026-11-16 | 080433f8e13a500522bc2754da64057edb0ae9d8 |
| A deterministic race/crash/failover matrix | session-a-integration-2026-11-16 | b53fe265cd5477a99e8b52e181e34d2a90c2dcf9 |

### Role review artifacts

| Role | Branch | Review Blob | Simulated disposition |
|---|---|---|---|
| D | session-d-memory-brain-2026-11-16 | 6f39475784458d34b347d8566824fa22b308b477 | ACCEPT WITH AMENDMENTS |
| E | session-e-memory-compiler-2026-11-16 | 5479db78adfcc67d3c33e0bd9e2d8f9a0a734960 | ACCEPT WITH AMENDMENTS |
| I | session-i-security-governance-2026-11-16 | 01d4514c1c0979ea878a89f36213a7db3c3c1003 | ACCEPT WITH AMENDMENTS |
| C | session-c-agent-integration-2026-11-16 | a7b57bd5531222559666f0f1d9df59a259cde61a | ACCEPT WITH C-OWNED PROVIDER-SIDE-EFFECT AMENDMENTS |
| Storage | session-storage-consistency-forget-atomicity-2026-11-16 | 2726f0a2a5168f126d25eb48b857d8921a09031e | ACCEPT WITH AMENDMENTS; ADR BLOCKED |

All role reviews above are assistant-authored role simulations at the user's direction. They are not independent human Owner signatures, cryptographic approvals or proof of deployed behavior.

## 2. HRC / JPF / WIRE / SCHEMA candidate execution

The checked-in test inventory is **66 unittest methods**:
- HRC-01..25: 25 recovery-cutoff semantic cases;
- JPF-01..19: 19 bidirectional request/admission/participant JoinProof cases;
- WIRE-01..10: 10 strict parsing and deterministic test-wire cases;
- SCHEMA-01..12: 12 schema-candidate integrity cases.

### 2.1 First run — failure retained as evidence

GitHub Actions run 44039825581 checked out H commit 78f90a51384b4ca3fdd202e5b308d0d40559f340. It ran 64 tests and failed only JPF-08. The fixture intended to test duplicate C primary admission but inherited required I/D evidence while supplying only C evidence, so the validator correctly returned UNKNOWN before reaching the duplicate-C assertion. This was a test-fixture defect, not a validator defect.

The fixture was narrowed to the C-only invariant. During the same correction pass, JPF-18/JPF-19 were moved into the unittest class so the OwnerAdmissionRef/OwnerEntryRef substitution negatives were actually discovered by unittest.

### 2.2 Corrected run — verified candidate PASS

<badge color="success">66 / 66 PASS</badge>

- GitHub Actions run: [44039990464](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44039990464)
- Job: semantic-and-wire-tests, job ID 133891944149
- Checked-out H commit: da94bcc1796cb350eed12845e49cbc3663faab9c
- Runner: Ubuntu 26.04 / CPython 3.12.16
- Result: 66 run, 66 passed, 0 failed, 0 skipped.

The exact checked-out test/schema blobs were:
- HRC/JPF suite: 60a2f4db4bd12f2131ecd147db9bbe328da6db50;
- RecoveryJoin schema: dd3234aa1c74caf6d0e335875cd96e0b2b64082f;
- Wire suite: 1a4e754ba9bfa57eb973c6d39731e9f89443b323;
- Schema suite: 67aba74c120f2916d768e7b01c45408ee2624f3a.

The raw job log enumerates all 66 cases as OK and ends with “Ran 66 tests” / “OK”.

### 2.3 Exact meaning of this PASS

This is a verified pass of the checked-in Python reference-candidate suite on the named runner. It is useful evidence for the modeled semantic invariants, schema shape and strict-parser negative vectors.

It does NOT prove:
- production canonicalization or signature bytes;
- I issuer/key status, historical trust or PolicyDomain sequencer implementation;
- two independent language implementations producing identical canonical bytes/digests/signature inputs;
- live COC quorum-prefix enumeration or RecoveryJoin quorum persistence;
- real I/D/C owner-ledger adapters or owner-local release CAS;
- real C provider adapter, same-key outcome lookup or final send gate;
- JF-10 prepared transaction behavior in the deployed Canonical Authority;
- D/Storage physical linearization, visibility read-path enforcement, HA/failover or restore.

The digest helper in the test suite is explicitly TEST-ONLY and is not a production H/I cryptographic profile.

## 3. Storage bidirectional JoinProof

Storage's logical digest chain is acyclic:

ParticipantManifestContentDigest → RecoveryBatchDigest → ParticipantManifestRecordDigest → RecoveryJoinProofDigest → owner-local Gate Release / RecoveryEpochCompleted.

The JoinProof contains both directions:

1. **Owner → COC:** every I/D/C request row and admission row is represented by an exact disposition or exact ParticipantIntent join. REGISTERED admission maps to one participant; NOT_REGISTERED has no participant locator and requires NO_EFFECT_PROVEN or remains pending; out-of-scope request requires owner-signed proof.
2. **COC → Owner:** every ParticipantManifest entry resolves to its primary C admission and every required I/D/C/Storage evidence edge, including JF-10 PreparedParticipantRef/GID/DB incarnation/attempt/ledger/outcome.

It explicitly preserves:
- six independent I/D/C request/admission completeness states;
- OwnerAdmissionRef (stable admission identity) vs OwnerEntryRef (exact owner snapshot row);
- OwnerRequestRef / OwnerRequestDigest vs OwnerEntryRef / OwnerEntryDigest;
- C primary admission anchor vs separate I/D/C/Storage evidence edges;
- D per-Fence lineage/barrier, I policy/receipt, C provider and Storage prepared/resolution typed evidence;
- owner-local high-waters, GateGeneration, ScopeGeneration and anti-rollback anchors without cross-domain numeric comparison.

Storage may persist and quorum-commit JoinProof after exact authoritative readback. Storage cannot issue I/D/C Gate Release. Each owner must re-read its own current roots/high-waters and perform its own release CAS. RecoveryEpochCompleted is a COC observation, not an owner release or business outcome.

The H schema now carries the structural fields, but live COC/owner enumeration, signature verification, evidence dereference and owner CAS remain unimplemented/unverified.

## 4. Cross-owner reconciliation

### 4.1 Compatible composition

- D PublicationParticipantRef, C ParticipantIntentRef, StorageVisibilityParticipantRef and Storage PreparedParticipantRef/GID/XID remain distinct nominal types.
- Storage durable PREPARED_HIDDEN precedes D PublicationParticipant admission.
- I's consumed CommitAuthorizationReceipt / ICommitAuthorizationProof is pre-commit evidence; ITerminalProof is post-Storage-outcome closeout evidence. No circular proof dependency remains.
- D ForgetFence, I revocation, C provider-egress gate and Storage visibility remain independent authorities.
- Owner request rows, owner admission rows and COC participant rows are separately enumerated and then joined; none is inferred from another.
- NOT_REGISTERED cannot carry participant identity and requires owner-signed no-effect proof or remains a release blocker.
- C ProviderIdempotencyKey is a C-owned namespace and MUST NOT be derived from or reused as Storage PreparedTransactionGID / native XID.
- RecoveryEpochCompleted does not imply Forget completion, provider success, Applied, visibility or physical erasure.

### 4.2 Remaining owner amendments

| Owner | Remaining blocker |
|---|---|
| D | Runtime verification of exact per-Fence ForgetOperationRef/FenceGeneration/LineageManifest/BarrierMember evidence, signed by D and read from the authoritative D ledger |
| E | Integrate RecoveryJoin + current owner releases + restore proofs as a hard gate before queue dispatch, protected dereference, lease execution, retry replay or publication after restore |
| I | Approve and implement signature/trust/key/historical verification, empty/out-of-scope proof policy and exact currentness CAS in I PolicyDomain sequencer |
| C | Implement provider adapter close-vs-send serialization, zero-byte close-first, same ProviderIdempotencyKey recovery, immutable CSubmitOutcome and final Agent submit hook |
| Storage | Prove actual D/Storage serialization topology, read-path enforcement, atomic pointer/receipt/outcome/outbox, HA/failover/restore and old-primary fencing |
| H | Implement wire-to-normalized adapters and production semantic validators; approve production canonicalization/signature profile and cross-language differential vectors |

## 5. Physical topology decision

Storage's topology ADR remains **ADR-BLOCKED / NO TOPOLOGY SELECTED**:
- Option A: one serializable transaction domain per Canonical Memory authority, conditional preference only if actual D/Storage runtime shares it and preserves semantic owner boundaries.
- Option B: separate D/Storage services with a named durable linearizable coordinator and executable failover proof.
- Check-then-write, process mutex, queue order, eventual replica and outbox-only coordination are rejected.

Issue #10 PostgreSQL 18.7 candidate CI probes are engine-capability evidence only. They do not identify the actual deployed Canonical Authority runtime or prove D/Storage share one serializable transaction domain. JF-10 P0 and Issue #10 Gate B/C remain open.

## 6. Deterministic physical test campaign

A's matrix contains:
- 12 two-order race cases;
- 12 crash / ACK-loss cases;
- 12 failover / restore cases;
- explicit mapping to HRC-01..25, JPF-01..19, WIRE-01..10 and SCHEMA-01..12.

The 66 H Python candidate tests passed. The broader physical race/crash/failover/restore campaign has NOT been run. A physical test PASS requires authoritative owner-ledger readback, actual COC quorum behavior, real DB/transaction evidence, pointer/read-path assertions, provider side-effect evidence and exact proof digests.

## 7. A integration decision

**ACCEPT AS A COHERENT PROPOSED COMPOSITION WITH BLOCKING AMENDMENTS.**

The HRC/RecoveryJoin/Storage JoinProof logical composition is coherent and the 66-case Python reference-candidate suite has a verified CI PASS. The first JPF-08 failure was a fixture issue: unrelated required I/D evidence was absent while testing a C-only duplicate-primary invariant. The fixture was narrowed without weakening validator behavior; JPF-18/JPF-19 are now actually discovered unittest methods.

The remaining blockers are substantive:
1. D per-Fence signed evidence verification;
2. E restore/dispatch gate integration;
3. I cryptographic trust and currentness implementation;
4. C real provider side-effect adapter and same-key recovery;
5. H production wire adapters/canonicalization and two-language interoperability;
6. Storage physical serialization topology, read-path, HA and restore proof;
7. actual physical deterministic test campaign and independent Owner approvals.

No schema/crypto freeze, production implementation/conformance PASS, branch merge, production activation, Global Forget completion or physical-erasure claim is authorized.

## 8. 中文集成裁决

H 已将 HRC-01..25 扩展为可执行 Python 候选测试，并增加 JPF-01..19、WIRE-01..10、SCHEMA-01..12，共 66 项。GitHub Actions 的修正后运行 44039990464 在精确 H Commit 上 66/66 通过。首次运行 44039825581 的 JPF-08 失败来自测试夹具：测试只提供 C 证据，却沿用了要求 I/D 证据的默认配置；修正后将该用例限定为 C 主 Admission 唯一性检查，同时把 JPF-18/19 正确注册为 unittest 方法，没有放宽 Validator。

Storage 已明确 COC ParticipantManifest 与 I/D/C Request/Admission Ledger 的双向 JoinProof，区分 OwnerAdmissionRef 与 OwnerEntryRef、OwnerRequestDigest 与 OwnerEntryDigest，并保留 D/I/C/Storage 各自的类型化证据。Storage 只能持久化 JoinProof，I/D/C 必须在自己的权威域执行 Currentness CAS 和 Gate Release。

66/66 仅证明 Python 候选语义/结构测试通过，不证明生产密码学、跨语言 Canonical Bytes、真实 COC Quorum、Owner Ledger Adapter、C Provider Side Effect、JF-10 生产物理行为或 D/Storage 事务拓扑。

最终裁决：**接受为逻辑一致的提案组合，且 H 候选测试通过；保留所有生产与物理实现阻塞项。Storage 拓扑 ADR 仍 BLOCKED，不冻结、不合并、不启用生产。**
