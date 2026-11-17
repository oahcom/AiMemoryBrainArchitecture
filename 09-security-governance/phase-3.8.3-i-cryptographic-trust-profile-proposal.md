# Phase 3.8.3 — I Cryptographic, Canonicalization and Key-Lifecycle Profile Proposal
# Phase 3.8.3 — I 密码学、规范化与密钥生命周期配置提案

- Owner: I — Security, Identity and Governance
- Status: **PROPOSED / CANDIDATE ONLY — NOT APPROVED, NOT FROZEN, NOT IMPLEMENTED**
- Profile ID: `AIMBA-I-CRYPTO-1.0`
- Applies to: I-signed authorization receipts, I terminal proofs, owner-signed I snapshots, empty-set proofs, out-of-scope proofs and I-owned RecoveryJoin evidence.
- Does not define: H wire grammar, C provider outcomes, D fence semantics, Storage visibility semantics or COC quorum semantics.
- Normative language: English and Chinese are equal-authority peers. If wording appears inconsistent, raise a versioned clarification; do not silently choose one language.

## 1. Executive decision / 执行结论

This proposal establishes one explicit candidate cryptographic profile so H can map a deterministic wire projection and independent implementations can build conformance vectors. It does **not** claim an approved trust root, deployed key registry, production PolicyDomain sequencer, H interoperability or owner/governance approval.

本提案建立一个明确的候选密码学配置，供 H 映射确定性 Wire Projection，并供独立实现建立一致性测试向量。它**不代表**信任根已批准、密钥注册表已部署、生产 PolicyDomain Sequencer 已运行、H 互操作已验证或 Owner/治理审批已完成。

### 1.1 Candidate suite / 候选算法套件

| Concern | Candidate normative choice | Constraint |
|---|---|---|
| Canonical JSON | RFC 8785 JSON Canonicalization Scheme (JCS), constrained by RFC 7493 I-JSON | Reject duplicate keys before object materialization; UTF-8 only; no implicit Unicode normalization |
| Digest | SHA-256 | Lowercase hexadecimal 64-character representation on wire |
| Signature | Ed25519, RFC 8032 | 64-byte signature; public key 32 bytes; no algorithm negotiation or downgrade within this profile |
| Signature encoding | Base64url without padding | Decode strictly; reject non-canonical encodings |
| Profile identity | `AIMBA-I-CRYPTO-1.0` | Exact, case-sensitive, immutable profile identifier |
| Domain separation | Profile- and message-type-specific ASCII domain tag | A signature for one message family cannot be replayed as another family |

This is a candidate profile, not a claim that Ed25519 satisfies every deployment's regulatory/FIPS requirements. A deployment requiring a different approved cryptographic module or algorithm suite MUST define a separately versioned profile and obtain I/H/Storage approval; silent fallback is forbidden.

这是候选配置，不代表 Ed25519 满足所有部署的监管/FIPS 要求。若部署要求其他经批准的密码模块或算法套件，必须定义独立版本配置并取得 I/H/Storage 审批；禁止静默降级或回退。

## 2. Canonicalization contract / 规范化合同

### 2.1 Input admissibility / 输入准入

Before canonicalization, every implementation MUST:

1. Decode UTF-8 strictly; reject BOM, invalid byte sequences and invalid Unicode scalar values.
2. Parse JSON with duplicate-member detection. Duplicate keys are rejected even if a conventional parser would keep only the first or last value.
3. Reject NaN, positive/negative Infinity, non-I-JSON values and numbers outside the interoperable IEEE-754 safe integer range when used as integers.
4. Reject unpaired surrogates and invalid Unicode. Do not silently repair malformed text.
5. Apply message-type semantic validation before signing or accepting a signature.
6. Treat absent, explicit null, empty string, empty array and empty object as distinct values. No defaulting or null/absence coercion is permitted unless the exact H schema says so.
7. Enforce RFC 8785 JCS serialization exactly. Do not add whitespace, reorder arrays, normalize Unicode, or apply locale-dependent formatting.

规范化前，所有实现必须严格解码 UTF-8；在对象构造前检测并拒绝重复 JSON Key；拒绝 NaN/Infinity、非法 Unicode、非 I-JSON 值及不安全整数；不得修复或归一化输入；必须先做消息语义校验；Absent、Null、空字符串、空数组、空对象必须区分；最后严格使用 RFC 8785 JCS，不得自行增加空白、重排数组、Unicode 归一化或依赖 Locale 格式化。

### 2.2 Numeric and time semantics / 数字与时间语义

- JCS number serialization is normative. Implementations MUST NOT sign language-native floating-point renderings.
- Identifiers, generations, owner-local sequence values and database/XID identities SHOULD be represented using their schema-defined string or integer types; never convert opaque typed identifiers into floating-point numbers.
- Time values used for policy validity are semantically validated as RFC 3339 timestamps with an explicit UTC offset. The signed value is the exact canonical string selected by the owner; a verifier MUST NOT rewrite it before signature verification.
- Wall-clock timestamps are audit/validity metadata only. They never replace I sequencer position, key-status generation, PermissionEpoch or anti-rollback anchors.

JCS 数字序列化规则具有规范性。禁止签署语言运行时自行生成的浮点字符串。Opaque ID、Generation、Owner-local Sequence 和 DB/XID 必须按 Schema 定义类型表达，不能转成浮点数。策略时间必须是带明确 UTC Offset 的 RFC 3339 时间；签名前选定的字符串就是被签署值，验证方不得先改写再验签。墙上时钟仅作审计/有效期元数据，不能替代 I Sequencer Position、Key Status Generation、PermissionEpoch 或 Anti-rollback Anchor。

## 3. Owner-signed projection and signature preimage / Owner 签名投影与签名原文

### 3.1 Projection ownership / 投影归属

H MUST publish an exact per-message-type field projection. The owner signature covers the complete immutable owner-authored semantic record, including:

- schema ID and on-wire schema-family version;
- message type, stable message ID and replay nonce;
- owner authority, owner record reference and owner subject/issuer identity;
- audience, purpose, PolicyDomain and OwnerBoundary where applicable;
- canonicalization/signature profile IDs;
- all message-specific semantic payload fields, typed refs, generations, high-waters, roots, counts, digests and terminal enums;
- key ID/version and owner-authored creation/validity fields.

The projection MUST exclude only fields that are not owner-authored and are added by another authority after signing, such as COC quorum position/commit proof and transport-session channel-binding evidence. Exclusions MUST be an explicit H field allowlist per message family; wildcard exclusions and implementation-defined omission are forbidden.

H 必须按消息类型发布精确字段投影。Owner 签名覆盖完整、不可变且由 Owner 撰写的语义记录，包括 Schema 标识与 Wire 版本、消息类型/稳定 ID/Replay Nonce、Owner Authority/Record Ref/Issuer/Subject、Audience/Purpose/PolicyDomain/OwnerBoundary、Profile ID、所有消息专属字段、Typed Ref、Generation、High-water、Root、Count、Digest、Terminal Enum、Key ID/Version 及 Owner 创建/有效期字段。

仅可排除签名后由其他 Authority 添加、且并非 Owner 撰写的字段，例如 COC Quorum Position/Commit Proof 和 Transport Session Channel-binding Evidence。每类消息的排除项必须由 H 明确列出；禁止通配符排除或实现自行省略。

### 3.2 Signature construction / 签名构造

Let `P` be the exact H-defined owner-signed projection and `JCS(P)` its RFC 8785 canonical UTF-8 bytes.

- Payload digest:
  `payload_digest = SHA-256(ASCII("AIMBA-I-PAYLOAD-v1") || 0x00 || JCS(P))`
- Signature preimage:
  `signature_preimage = ASCII("AIMBA-I-SIGNATURE-v1") || 0x00 || ASCII("AIMBA-I-CRYPTO-1.0") || 0x00 || ASCII(message_type) || 0x00 || JCS(P)`
- Signature:
  `signature = Ed25519.Sign(private_key, signature_preimage)`

The signature field itself, signature verification result, transport channel-binding proof and post-append COC commit attestation are not members of P. The exact projection MUST include `payload_digest` only if H defines it as a field inside P; if included, the digest is recomputed over the projection with the digest field omitted, and this omission rule must be explicit in the H mapping. No circular digest is permitted.

`P` 是 H 定义的精确 Owner-signed Projection，`JCS(P)` 是 RFC 8785 规范 UTF-8 字节。

- Payload Digest：`SHA-256("AIMBA-I-PAYLOAD-v1" || 0x00 || JCS(P))`
- Signature Preimage：`"AIMBA-I-SIGNATURE-v1" || 0x00 || "AIMBA-I-CRYPTO-1.0" || 0x00 || message_type || 0x00 || JCS(P)`
- Signature：`Ed25519.Sign(private_key, signature_preimage)`

Signature 字段本身、验签结果、Transport Channel-binding Proof 及签名后追加的 COC Commit Attestation 不属于 P。若 H 将 `payload_digest` 纳入 P，必须明确其计算时排除该字段并防止循环摘要；否则不得自行推断。

### 3.3 Separate authority attestations / Authority Attestation 分离

- Owner signature proves the named owner authored the exact projected record; it does not prove COC quorum commitment.
- COC quorum attestation proves the exact record position/configuration/prefix commitment; it does not prove owner authorization or business outcome.
- H transport/channel binding proves the authenticated transport/session boundary; it does not replace either durable owner signature or COC quorum proof.
- A RecoveryJoinProof digest is a later typed link in the evidence chain, not a replacement signature over earlier owner records.

Owner Signature 只证明指定 Owner 撰写了精确投影记录，不证明 COC Quorum Commit。COC Quorum Attestation 只证明记录位置/配置/Prefix 已提交，不证明 Owner 授权或业务结果。H Transport/Channel Binding 只证明认证传输会话，不替代 Owner Signature 或 COC Quorum Proof。RecoveryJoinProof Digest 是后续证据链链接，不替代对早期 Owner Record 的签名。

## 4. Key identity, custody and lifecycle / Key 身份、保管与生命周期

### 4.1 Key identity / Key 身份

Every signing key is identified by the tuple:

`(IssuerRef, OwnerAuthority, KeyIdRef, KeyVersion, Algorithm, ProfileId, Purpose, Audience)`

A key ID is never reused for different key material. Key version is immutable. Public-key material is distributed through an authenticated I trust registry; payload-supplied public keys are never trusted.

每把签名密钥以 `(IssuerRef, OwnerAuthority, KeyIdRef, KeyVersion, Algorithm, ProfileId, Purpose, Audience)` 唯一标识。Key ID 不得复用到不同 Key Material；Key Version 不可变。公钥只能通过经认证的 I Trust Registry 分发，禁止信任 Payload 自带公钥。

### 4.2 Custody / 保管

- Production private keys MUST be generated and used in an approved HSM/KMS boundary with non-exportable key material, access logging and least-privilege signing authorization.
- Key administration, signing authorization and audit review MUST be separated. High-impact I root/trust changes require two-person approval and immutable audit evidence.
- Development/test keys MUST be cryptographically and operationally isolated from production keys and MUST NOT be accepted by production trust roots.
- Private-key backup/export is prohibited unless an explicitly approved HSM recovery design requires it; any such exception needs a separate threat-model and governance decision.

生产私钥必须在经批准的 HSM/KMS 边界内生成和使用，密钥材料不可导出，具备访问日志和最小权限签名授权。Key 管理、签名授权与审计复核必须分离；高影响 I Root/Trust 变更必须双人批准并保留不可变审计证据。开发/测试密钥必须与生产隔离，生产 Trust Root 不得接受测试密钥。除非独立批准的 HSM 恢复设计确有需要，否则禁止私钥备份/导出。

### 4.3 Lifecycle states / 生命周期状态

The authoritative I key-status ledger MUST represent at least:

- `PENDING`: generated/registered but not usable;
- `ACTIVE`: may sign for the exact profile/purpose/audience and validity interval;
- `RETIRED`: cannot create new signatures; historical verification may remain possible;
- `REVOKED`: no new signatures; verification follows the recorded effective revocation boundary;
- `COMPROMISED`: signatures are untrusted from the recorded compromise boundary unless a separately approved, independently anchored pre-compromise proof establishes prior existence;
- `DESTROYED`: private key material destroyed; public verification metadata and status history retained as policy requires.

Every transition is append-only and signed by the I key-status authority. A transition binds previous status digest, new status, key identity, effective I sequencer position, status generation, reason code, approver identities and audit reference. A timestamp alone MUST NOT establish the effective boundary.

I 权威 Key Status Ledger 至少支持 PENDING、ACTIVE、RETIRED、REVOKED、COMPROMISED、DESTROYED。状态转换只追加、不覆盖，并由 I Key Status Authority 签名。每次转换绑定前序状态 Digest、新状态、Key Identity、生效 I Sequencer Position、Status Generation、Reason Code、审批人及审计引用。禁止仅凭时间戳确定生效边界。

### 4.4 Rotation, revocation and compromise / 轮换、撤销与泄露

1. Rotation creates a new KeyVersion; it never mutates an existing key record or reuses an old KeyIdRef.
2. New signatures require ACTIVE status at the exact I sequencer position at signing/consumption.
3. RETIRED keys may verify historical signatures only when the historical trust proof is complete and the key was not compromised for the relevant interval.
4. REVOKED/COMPROMISED status is evaluated using the I-authoritative effective sequencer position, not a sender timestamp or cache TTL.
5. On compromise, I closes affected gates, marks the key status, identifies all records signed by the key/version, revalidates dependent receipts/proofs and requires explicit disposition. Unknown exposure interval means affected evidence is UNKNOWN.
6. Verifiers fail closed when current key status or historical status checkpoint is unavailable, stale, forked or cannot be anchored after restore.

轮换必须创建新 KeyVersion，不得修改旧 Key Record 或复用旧 KeyIdRef。新签名必须在签发/消费时的精确 I Sequencer Position 上处于 ACTIVE。RETIRED 仅在历史信任链完整且相关期间未泄露时可用于历史验签。撤销/泄露边界以 I Sequencer Position 为准，不依赖发送方时间戳或 Cache TTL。发生泄露时 I 关闭受影响 Gate，标记 Key Status，枚举该 KeyVersion 签署的全部记录并重新裁定依赖证明；泄露区间未知则相关证据为 UNKNOWN。恢复后无法锚定历史 Status Checkpoint 时必须 Fail-closed。

## 5. Replay, nonce and retention / Replay、Nonce 与保留期

- Nonce uniqueness is enforced by the I sequencer within the tuple `(IssuerRef, PolicyDomainRef, message_type, nonce)`.
- Same tuple + same immutable payload digest is idempotent and returns the original durable result; same tuple + different digest is CONFLICT.
- A consumed CommitAuthorizationReceipt is single-use for its exact PublicationOperationId, PublicationTupleDigest, D participant, Storage participant, artifact/version, Scope, Purpose and Audience.
- Replays with changed participant, attempt, artifact version, scope, audience, policy domain or tuple digest are rejected even if the caller reuses a valid signature.
- Nonce/receipt tombstones MUST be retained beyond the maximum retry, delayed-message, backup, restore, dispute and audit horizons. The concrete retention period is a separate I policy decision and cannot be shorter than any dependent evidence-retention requirement.
- Unknown, missing or rolled-back nonce state is UNKNOWN; never infer unused from absence after restore.

I Sequencer 必须在 `(IssuerRef, PolicyDomainRef, message_type, nonce)` 范围内保证 Nonce 唯一。同一 Tuple + 同一不可变 Payload Digest 幂等返回原始结果；同一 Tuple + 不同 Digest 返回 CONFLICT。已消费 CommitAuthorizationReceipt 仅对精确 PublicationOperationId/TupleDigest、D/Storage Participant、Artifact/Version、Scope、Purpose、Audience 单次有效。变更 Participant/Attempt/Artifact/Scope/Audience/PolicyDomain/Tuple 的重放必须拒绝。Nonce/Receipt Tombstone 保留时间必须超过最大 Retry、延迟消息、Backup、Restore、争议和审计期限；具体时长由 I 独立制定，且不得短于依赖证据的保留要求。Restore 后 Nonce 状态缺失/回滚/未知时一律 UNKNOWN，不得推断为未消费。

## 6. Historical verification and anti-rollback / 历史验签与防回滚

Historical verification MUST use a verifiable checkpoint chain containing at least:

- I PolicyDomainRef and PermissionEpoch history;
- I key-status ledger generation and append-only status digest chain;
- I sequencer epoch/position and continuity proof;
- trust-registry version and issuer/delegation status at the relevant sequencer position;
- receipt nonce-consumption record and exact operation/participant tuple;
- independently stored anti-rollback anchor/checkpoint.

A restore MUST compare restored state against a checkpoint held outside the restored failure domain. If the external anchor is unavailable, older, forked or inconsistent, the authority remains quarantined. Wall-clock time, database sequence numbers restored from backup, COC position, D FenceGeneration and Storage XID MUST NOT substitute for the I anchor.

历史验签必须验证 I PolicyDomain/PermissionEpoch 历史、Key Status Ledger Generation/追加链、I Sequencer Epoch/Position 连续性、对应位置的 Trust Registry/Issuer/Delegation 状态、Receipt Nonce Consumption 记录、精确 Operation/Participant Tuple，以及独立存储的 Anti-rollback Anchor。Restore 必须与恢复域之外保存的 Checkpoint 比对；外部 Anchor 不可用、过旧、分叉或不一致时，Authority 保持隔离。禁止使用墙上时钟、备份恢复的 DB Sequence、COC Position、D FenceGeneration 或 Storage XID 替代 I Anchor。

## 7. Verification algorithm / 验证算法

A verifier MUST execute in this order:

1. Strictly parse JSON and reject duplicate keys/invalid UTF-8/invalid Unicode.
2. Resolve the exact schema artifact and on-wire family version; reject unknown critical fields and unsupported profile IDs.
3. Resolve issuer, owner, key ID/version, purpose and audience from authenticated trust context; never from an untrusted key supplied in the message.
4. Fetch current and historical I key-status/trust checkpoints and verify anti-rollback continuity.
5. Reconstruct the exact H-defined owner-signed projection; reject missing, extra, reordered-array or ambiguous fields.
6. Recompute JCS bytes and SHA-256 payload digest; constant-time compare digest values.
7. Verify Ed25519 signature over the exact domain-separated preimage.
8. Validate nonce/replay state and exact operation/participant tuple in the authoritative I sequencer.
9. For CommitAuthorizationReceipt, atomically consume once and order against revocation/policy changes in the same PolicyDomain sequencer.
10. Any unavailable authority, stale generation, unknown status, signature mismatch, schema downgrade, replay conflict or anti-rollback failure returns DENY/UNKNOWN and keeps the relevant gate closed.

验证顺序必须严格执行：严格解析并拒绝重复 Key/非法 UTF-8/Unicode；解析精确 Schema Artifact 与 Wire Version；从认证 Trust Context 获取 Issuer/Owner/Key/Purpose/Audience；获取当前与历史 Key Status 并验证 Anti-rollback；重建 H 定义的 Owner Projection；计算 JCS 与 SHA-256；验证 Ed25519；验证 Nonce/Replay 和精确 Operation/Participant Tuple；CommitAuthorizationReceipt 必须在同一 PolicyDomain Sequencer 中单次消费并与 Revocation 排序。任何 Authority 不可用、Generation 过期、Status 未知、签名不符、Schema 降级、Replay Conflict 或 Anti-rollback 失败，都返回 DENY/UNKNOWN 并保持相关 Gate 关闭。

## 8. Required conformance vectors / 强制一致性向量

I and H MUST jointly publish positive and negative vectors for:

| ID | Vector | Expected |
|---|---|---|
| CRYPTO-01 | Same owner projection in two independent implementations | Identical JCS bytes and SHA-256 digest |
| CRYPTO-02 | Same projection signed and verified by independent Ed25519 implementations | Signature verifies byte-for-byte |
| CRYPTO-03 | Duplicate JSON member at any nesting level | REJECT |
| CRYPTO-04 | Absent vs null vs empty string/array/object | Distinct canonical bytes and semantics |
| CRYPTO-05 | Unicode composed/decomposed forms | Distinct strings unless the application explicitly defines a prior semantic normalization; JCS itself does not normalize |
| CRYPTO-06 | Reordered object members | Same JCS bytes |
| CRYPTO-07 | Reordered array elements | Different JCS bytes |
| CRYPTO-08 | NaN/Infinity/unpaired surrogate/invalid UTF-8 | REJECT |
| CRYPTO-09 | Integer beyond safe interoperable range | REJECT unless represented as schema-defined string |
| CRYPTO-10 | Wrong message type/profile/purpose/audience | REJECT |
| CRYPTO-11 | Signature field or COC commit attestation modified | Owner signature behavior follows exact projection; COC attestation must independently fail its own proof check |
| CRYPTO-12 | Same nonce + same digest | IDEMPOTENT original result |
| CRYPTO-13 | Same nonce + different digest | CONFLICT |
| CRYPTO-14 | Retired key with valid historical checkpoint | Historical verification only |
| CRYPTO-15 | Compromised key with no independently anchored pre-compromise proof | UNKNOWN / REJECT |
| CRYPTO-16 | Key-status ledger rollback/fork or missing external anchor | QUARANTINE |
| CRYPTO-17 | Stale key cache / unavailable key-status service | UNKNOWN; no gate release |
| CRYPTO-18 | Duplicate/replayed CommitAuthorizationReceipt consumption | Original result only; no second effect |
| CRYPTO-19 | Profile downgrade or algorithm substitution | REJECT |
| CRYPTO-20 | Restore with missing nonce tombstone or sequencer gap | QUARANTINE |

These vectors are specified, **not executed**. H must bind each vector to exact schema projections and at least two independently implemented canonicalization/signature stacks. I must approve the trust/key-status test authority and expected security disposition.

以上向量目前仅定义、尚未执行。H 必须将每个向量绑定到精确 Schema Projection，并由至少两套独立实现执行规范化/签名；I 必须批准 Trust/Key Status 测试 Authority 及安全预期结果。

## 9. Open decisions / 待决事项

The following remain explicitly OPEN and MUST NOT be inferred from this proposal:

1. I Owner approval of the algorithm suite and the production regulatory/FIPS suitability decision.
2. Exact H per-message signed-field projections, signature-envelope mapping and schema artifact revision.
3. I trust-root ceremony, HSM/KMS vendor/profile, two-person recovery and operator separation.
4. Concrete key rotation interval, overlap window, nonce/receipt retention duration and revocation propagation SLO.
5. External anti-rollback anchor implementation and restore drill.
6. Real PolicyDomain sequencer, durable single-use nonce consumption and revocation-vs-commit race proof.
7. Two independent language implementations, byte-for-byte canonicalization/signature vectors and live key-status verification.
8. Independent human Owner and governance approval.

## 10. Exact acceptance boundary / 精确接受边界

This document is an I-owned **candidate proposal**. It does not authorize H to claim schema approval, does not authorize Storage to accept signatures, does not authorize production key provisioning, and does not close FR-P0-01, I-FR-01, I-RJ-05 or TAB-001.

本文件是 I Owner 的**候选提案**。它不授权 H 宣称 Schema 已获批准，不授权 Storage 接受生产签名，不授权生产密钥配置，也不关闭 FR-P0-01、I-FR-01、I-RJ-05 或 TAB-001。
