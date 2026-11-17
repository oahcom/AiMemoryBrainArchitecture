# Phase 3.8.4 — H Unified Recovery Manifest and Owner-Evidence Contract
# Phase 3.8.4 — H 统一恢复清单与 Owner 证据合同

- Owner perspective: H — BMCP Protocol Architect
- Exact schema candidate: `bmcp.coc-jf10-unified/1.2.11`, Blob `4f1e103ab4b2ac961d77179dba0b65093532ea40`
- Wire family: `schema_version=1.3.0`
- Status: **PROPOSED / CANDIDATE ONLY — NOT FROZEN / NOT DEPLOYED**
- English and Chinese are normative peers.

## 1. Authority and exact inputs / Authority 与精确输入

| Artifact | Exact Blob |
|---|---|
| Storage COC protocol v3.2.3 | `5cee0d58575adc0fb3dd20a5c7ab68c2a2711792` |
| Storage Batch/Manifest order amendment | `1c8c0bc11798293293bcf47fa560f1699a5bcfe0` |
| H Unified Schema 1.2.11 | `4f1e103ab4b2ac961d77179dba0b65093532ea40` |
| H I crypto wire mapping 3.8.4 | `bf160288d7529b37ad1b56924c1583748922aa25` |
| I crypto profile proposal | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` |
| I crypto artifact-revision amendment | `9db3976ed9a891e9395d0e7edf949e75cb4422aa` |
| H RecoveryJoin schema 1.0.1 | `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c` |
| H semantic validator reference | `4a7c22ed15dff0a688559f79e4facbffca6527cd` |
| H unified manifest conformance tests | `cb4a619ac580f50c75bc6c9f7a8a6853a381ddb5` |
| I Python/Node P0 vector set | `4657f0c81e9c8692d29ac183380f3d7e074a4e4c` |
| I Python/Node crypto test | `7658edc6f51dac203742ecc1ecf00d41bd676908` |

Storage owns COC durability, exact Batch/Manifest append order, committed record identity and quorum evidence. I/D/C own their ledgers, snapshots, membership proofs, gates and releases. H owns wire grammar, schema, typed identity, digest field distinction, canonical serialization contract and interoperable message validation. H does not become the authority for another Owner's ledger or trust policy.

Storage 拥有 COC 持久性、Batch/Manifest 精确追加顺序、已提交 Record 身份与 Quorum Evidence。I/D/C 分别拥有自己的 Ledger、Snapshot、Membership Proof、Gate 与 Release。H 拥有 Wire Grammar、Schema、Typed Identity、Digest 字段区分、Canonical Serialization 合同与消息互操作验证。H 不成为其他 Owner 的 Ledger 或 Trust Policy Authority。

## 2. Exact schema and wire version / 精确 Schema 与 Wire Version

The schema artifact revision is `1.2.11`; the wire-family version is `1.3.0`. Both are required common-envelope fields:
- `schema_artifact_revision=1.2.11` selects the exact schema artifact;
- `schema_version=1.3.0` selects the protocol-family contract.

Both are included in protected I P0 projections for Unified Schema messages. A receiver rejects disagreement among the signed field, schema registry and resolved artifact. RecoveryJoin 1.0.1 remains a separate artifact and retains its own nested proof projections.

Schema Artifact Revision 为 `1.2.11`，Wire Family Version 为 `1.3.0`，两者都是必填 Common Envelope 字段：
- `schema_artifact_revision=1.2.11` 选择精确 Schema 工件；
- `schema_version=1.3.0` 选择协议族合同。

两者都纳入 Unified Schema 受保护 I P0 Projection。接收方必须拒绝签名字段、Schema Registry 与解析工件之间的不一致。RecoveryJoin 1.0.1 是独立工件，继续使用自己的嵌套 Proof Projection。

## 3. Canonical union Manifest / 规范化 Union Manifest

The Manifest is not merely the COC participant list. Its `manifest_members` is the canonical union of:

1. Every quorum-committed COC ParticipantIntent at or before the frozen COC prefix P.
2. Every applicable I/D/C owner-local admission at or below its own frozen owner high-water that has not been joined to a COC participant.

Each member has one explicit discriminator.

### 3.1 `COC_PARTICIPANT`

A COC member binds:
- exact ParticipantIntentRef and committed prefix position/digest;
- transaction/request identity and digest;
- owner boundary, PolicyDomain and participant tuple digest;
- zero or more exact `owner_admission_bindings`.

Each binding identifies the owner kind, OwnerAdmissionRef, OwnerEntryRef, owner ledger ref/version, owner-local sequence/high-water, owner entry digest, owner ledger root, immutable snapshot ref/digest, snapshot attestation ref/digest, membership proof ref/digest, operation/scope digest and the exact parent ParticipantIntentRef.

The binding array may be empty only when no applicable owner-local admission exists for that COC participant. If one or more applicable admissions exist in the frozen owner ledgers, every such row must appear exactly once; the semantic validator proves the complete set.

### 3.2 `OWNER_LOCAL_ADMISSION`

An admission not registered in the frozen COC prefix is represented as a separate union member. It MUST:
- identify I, D or C and the exact owner admission/ledger entry;
- bind owner ledger ref/version, owner-local sequence/high-water, entry digest and ledger root;
- bind immutable owner snapshot and snapshot-attestation refs/digests;
- bind an owner-signed snapshot membership-proof ref/digest;
- carry operation identity/digest, request digest, scope binding, admission state and effect boundary;
- set `coc_participant_intent_ref=null`;
- provide a non-empty `coc_absence_reason`.

A fabricated ParticipantIntentRef is invalid. Missing COC registration is not interpreted as an empty set and is never repaired by inventing a participant identity.

### 3.3 Counts and roots

The Manifest and preceding Recovery Cutoff Batch bind distinct values:
- `coc_participant_count`: COC members only;
- `owner_local_admission_count`: unregistered owner-local members only;
- `manifest_member_count`: total union member count;
- `member_set_root`: canonical root over all typed union members;
- `manifest_content_digest`: canonical content digest over epoch, frozen prefix, enumeration high-water, all counts, member-set root, owner snapshot roots and complete union members.

The registered owner admissions embedded in a COC member's `owner_admission_bindings` are evidence bindings, not additional top-level union members. Thus `manifest_member_count = coc_participant_count + owner_local_admission_count`.

### 3.4 Owner snapshot roots

The Manifest repeats an exact I/D/C `owner_snapshot_roots` map. Each root binds:
- owner snapshot ref and digest;
- owner snapshot attestation ref and digest;
- owner Gate ref/generation;
- request and admission high-waters;
- request, admission and owner-ledger roots;
- anti-rollback anchor;
- digest of the complete owner-specific high-water object.

The COC Batch carries the complete owner snapshots. The semantic validator must prove that the Manifest root map is byte-for-byte/equivalently bound to those exact snapshots; a locator without an immutable digest is insufficient.

## 4. Three different digest layers / 三种不同摘要层

These values are not aliases:

| Field | Meaning |
|---|---|
| `manifest_content_digest` | Canonical union Manifest content, prefix and frozen owner snapshot roots; excludes later Batch backlink and final COC record envelope |
| `member_set_root` | Canonical ordered root over the typed union members |
| `manifest_record_entry_digest` | Final committed COC Manifest Record entry digest, including exact Batch backlink |
| `batch_digest` | Recovery Cutoff Batch payload digest |
| `batch_entry_digest` | Final committed COC Batch Record entry digest |

The owner release and RecoveryEpochCompleted records MUST bind both Manifest content digest and final Manifest record-entry digest. Substituting one for the other is INVALID.

这些摘要不可互换：

| 字段 | 含义 |
|---|---|
| `manifest_content_digest` | Canonical Union Manifest 内容、Prefix 与冻结 Owner Snapshot Roots；不含后续 Batch Backlink 与最终 COC Record Envelope |
| `member_set_root` | Typed Union Members 的 Canonical Ordered Root |
| `manifest_record_entry_digest` | 包含精确 Batch Backlink 的最终已提交 COC Manifest Record Entry Digest |
| `batch_digest` | Recovery Cutoff Batch Payload Digest |
| `batch_entry_digest` | 最终已提交 COC Batch Record Entry Digest |

Owner Release 与 RecoveryEpochCompleted 必须同时绑定 Manifest Content Digest 和最终 Manifest Record Entry Digest。用其中一个替代另一个属于 INVALID。

## 5. Two-phase Batch/Manifest order / Batch/Manifest 两阶段顺序

1. COC quorum commits RecoveryCutoffBatch first. It binds RecoveryEpoch/round, exact frozen owner snapshots, COC prefix P, manifest identity/content digest, member counts/root and previous batch digest.
2. COC then appends ParticipantSetReconciliation as a separate committed record. It binds the exact prior Batch record ref, position and entry digest, repeats the same manifest content digest/counts/root and carries the complete canonical union members plus owner snapshot roots.
3. The Manifest record's final COC entry digest is distinct from its content digest.
4. A crash after Batch but before Manifest leaves the recovery epoch FENCED. Recovery must resume the same Batch/Manifest pair; it must not synthesize an empty Manifest or start owner release.
5. A crash after Manifest but before all owner releases leaves the epoch unreleased. Each owner independently revalidates its own currentness CAS before release.
6. RecoveryEpochCompleted is only a COC observation after exactly one current I, D and C release for the exact scope/generation and no unresolved member remains.

## 6. Owner Gate Release / Owner Gate 释放

The canonical release enum is `OUTAGE_ADMISSION_RELEASE_ONLY`. I/D/C may release only their own temporary outage admission gate. The release binds:
- exact Batch ref, payload digest, position and committed entry digest;
- exact Manifest record ref/position, content digest and committed entry digest;
- owner Gate ref/generation;
- owner request/admission high-waters, request/admission roots and owner reconciliation root;
- owner signature/profile and final owner-local currentness CAS.

It does NOT clear Forget effectiveness, grant new I permission, resolve Storage visibility, authorize C Provider Egress or prove Global Forget Completion. A stale high-water, scope generation, root, snapshot, key status or anti-rollback anchor invalidates the release candidate.

规范 Release 枚举为 `OUTAGE_ADMISSION_RELEASE_ONLY`。I/D/C 只能释放自己负责的临时 Outage Admission Gate。Release 必须绑定精确 Batch、Manifest Record、Content Digest、Record Entry Digest、Owner Gate Generation、Owner Request/Admission High-water、Roots、Owner Reconciliation Root、Owner Signature/Profile 与最终 Owner-local Currentness CAS。

该 Release 不会清除 Forget 生效状态、不授予新的 I Permission、不解决 Storage Visibility、不授权 C Provider Egress，也不证明 Global Forget Completion。任何 High-water、Scope Generation、Root、Snapshot、Key Status 或 Anti-rollback Anchor 过期都会使 Release Candidate 失效。

## 7. Semantic validation and fail-closed rules / 语义验证与 Fail-closed 规则

H semantic validation MUST establish:
1. complete COC prefix enumeration and complete I/D/C owner snapshot pagination;
2. unique typed union members and canonical order;
3. exact bidirectional COC Participant ↔ owner admission joins;
4. explicit null/no-registration reason for each unregistered owner admission;
5. exact membership proof ref/digest and snapshot-root inclusion for every owner row;
6. exact owner snapshot-root map equality between Batch and Manifest;
7. count, member root and content digest recomputation;
8. Batch-before-Manifest order and exact backlink/entry digest;
9. separate Manifest content and final record-entry digest;
10. protected owner signature profile resolution and owner-only release authority.

Missing source, incomplete page, unavailable owner, stale replica, unverifiable signature, missing proof, changed root, ambiguous field or unresolved anti-rollback state returns UNKNOWN/INVALID and keeps the relevant gate closed. JSON Schema validity alone never proves completeness or authorization.

H 语义验证必须证明：
1. COC Prefix 完整枚举及 I/D/C Owner Snapshot 完整分页；
2. Typed Union Members 唯一且 Canonical Order；
3. COC Participant 与 Owner Admission 双向精确 Join；
4. 每个未登记 Owner Admission 都有显式 Null 与未注册原因；
5. 每个 Owner Row 都有精确 Membership Proof Ref/Digest 与 Snapshot Root Inclusion；
6. Batch 与 Manifest 的 Owner Snapshot Root Map 完全一致；
7. Count、Member Root 与 Content Digest 可重算；
8. Batch 先于 Manifest，Backlink/Entry Digest 精确；
9. Manifest Content Digest 与最终 Record Entry Digest 分离；
10. 受保护 Owner Signature Profile 可解析，且 Release Authority 只能属于 Owner 自身。

Source 缺失、分页不完整、Owner 不可用、Replica 过期、签名无法验证、Proof 缺失、Root 变化、字段歧义或 Anti-rollback 不确定，均返回 UNKNOWN/INVALID 并保持相关 Gate 关闭。JSON Schema 有效本身不能证明完整性或授权。

## 8. Executable evidence boundary / 可执行证据边界

The H candidate reference validator uses a deterministic TEST-only digest profile and normalized evidence fixtures. It is not the production JCS/signature/quorum/ledger implementation. The Python/Node I crypto vectors use a deterministic TEST-only private seed. They prove independent test-stack agreement only.

The H CI run is recorded separately against its exact commit. Even a passing candidate suite does not establish:
- real COC quorum persistence or linearizable prefix reads;
- real I/D/C owner-ledger completeness and signed membership proofs;
- production JCS/Ed25519 trust/key registry and anti-rollback;
- C Provider Egress adapter linearization or provider same-key lookup;
- Storage database incarnation/XID/WAL/PITR deployment conformance;
- multi-PolicyDomain atomicity;
- production activation.

H 候选参考验证器使用确定性的 TEST-only Digest Profile 与归一化 Evidence Fixture，不是生产 JCS/Signature/Quorum/Ledger 实现。Python/Node I Crypto Vector 使用确定性的 TEST-only 私钥 Seed，只证明独立测试栈结果一致。

H CI 的精确 Run 与 Commit 必须单独记录。即使候选测试全部通过，也不能证明真实 COC Quorum 持久化/线性化 Prefix Read、I/D/C Owner Ledger 完整性与签名 Membership Proof、生产 JCS/Ed25519 Trust/Key Registry/Anti-rollback、C Provider Egress Adapter、Storage Database Incarnation/XID/WAL/PITR、多 PolicyDomain 原子性或生产激活。

## 9. H decision / H 决议

**ACCEPT WITH ENUMERATED AMENDMENTS** as a protocol/schema candidate only. This is a delegated H-role simulation in the coordinating session, not an independent human H Owner signature. I/D/C/Storage must review their respective authorities and evidence; A must perform a fresh exact-version integration review.

No schema/protocol/cryptographic freeze, deployment, implementation conformance PASS, JF-10 P0 closure or production activation is claimed.

**作为协议/Schema 候选有条件接受。** 本决议是协调会话中的 H 角色模拟，不是独立人工 H Owner 签署。I/D/C/Storage 必须审查各自 Authority 与 Evidence；A 必须进行新的精确版本集成审查。

不宣称 Schema/Protocol/Cryptographic Freeze、部署、实现 Conformance PASS、JF-10 P0 关闭或生产激活。
