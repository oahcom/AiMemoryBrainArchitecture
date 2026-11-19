# D-002 六条件操作级证明包 / Six-Condition Operational Proof

- Decision ID: D-OWNER-2026-11-19-003
- Owner: D Domain Contract Owner（D Owner）
- Scope: AID-2026-010 / Issue #43；F-43-01/F1 的 D 侧操作证明；F-43-02 的 D 契约 §5 与 Unicode 版本阻塞整改
- Normative successor: D contract 1.3.1，见 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract-1.3.1.md
- Superseded candidate: 1.3.0 main commit 4f82e3a48a35e9fd73e7920f0c6a559b77aaf0dc, Blob d83cde77e98db2e74cf6827d874b0babb4157304
- D-002 source: Issue #25 comment 7015682819; Issue #43 comment 7015684625
- D operation baseline: 03-memory-brain/forget-fence-operation-and-publication-gate.md, D branch session-d-memory-brain-2026-11-16 @ b525e1f8fee2471a131e4a38efda99804045e424, Blob 4da0b61ba3656a768ea56b4a2a24e09da4e21cd5

## 1. Authority and proof boundary

This package formalizes the six conjunctive conditions accepted by D Owner Decision D-OWNER-2026-11-19-002. It does not infer protocol correctness from field names, numeric magnitude, schema presence, a single successful call, or an unverified implementation.

The proof is over one immutable ForgetOperation/fence snapshot. InstallForgetFence establishes the cutoff at its linearization point. CaptureProducerRegistrationHighWater only retrieves and verifies that already-established cutoff; Capture MUST NOT create, move, reset, or advance it.

The two nominal high-waters remain disjoint:

- ProducerRegistrationHighWater / ProducerRegistrationSequence: D ProducerWork Registration Ledger namespace; source is the D producer-work registration ledger and immutable BarrierSnapshotReceipt.
- ForgetFenceGeneration: D ForgetFence namespace; source is D ForgetFence generation state/ledger.

H producer_registration_high_water maps only to the first type. H forget_fence_generation_high_water maps only to the second. They have different units, sequences, and authority sources. They MUST NOT be compared, cast, substituted, or used to derive one another. The equality in Condition 4 below is between two representations of the same ProducerRegistrationHighWater cutoff, not between the two H fields.

## 2. Six-condition operational proof

The Condition IDs below are local trace labels only. The condition wording and ordering preserve the six separate conjuncts in D-002; none is merged or omitted.

| Condition ID | 规范定义 | 操作主体 | 前置状态 | 持久化后状态 | 成功判据 | 失败/恢复行为 | 对应字段及名义类型 | 证据位置 |
|---|---|---|---|---|---|---|---|---|
| D002-C1 | Same BrainAuthorityId, Producer Registration Ledger identity/namespace, and ProducerRegistryVersion. | D authority executes InstallForgetFence; D snapshot authority issues BarrierSnapshotReceipt; verifier checks both receipts. | Authority and ledger are identified; registry version is committed and complete; request is authenticated/authorized; no unresolved registry gap. | Fence receipt and snapshot receipt persist the same authority, ledger namespace, and registry version. | Exact identity equality across the install receipt and snapshot receipt; registry version is the captured immutable version. | Any mismatch => INVALID; missing/unavailable registry or ledger state => UNKNOWN/BLOCKED. Retry reads the same operation; never substitute another namespace or registry version. | BrainAuthorityId; Producer Registration Ledger identity/namespace; ProducerRegistryVersion. These are nominal identities/version, not watermarks. | This file §2 D002-C1; D operation contract §§2, 3.2–3.4. |
| D002-C2 | Same ForgetOperationId, idempotency identity, canonical request digest, and exact target-set digest. | D ForgetOperation authority validates the request and owns idempotency record; caller supplies stable identity and digest. | Operation identity/key/digests are canonicalized; no prior record exists, or an exact prior record is found. | A durable idempotency record binds the operation ID, key, request digest, target digest, and resulting fence receipt. | Exact identity and digest match; same request resolves to the original operation result. | Same identity with changed request or target digest => IDEMPOTENCY_CONFLICT. Lost ACK => lookup/retry same identity. Never mint a new cutoff/generation for uncertain outcome. | ForgetOperationId, idempotency key/identity, canonical request digest, target-set digest. IDs/digests are opaque typed identities, not counters. | This file §2 D002-C2; D operation contract §§3.3, 3.8. |
| D002-C3 | Same ForgetFenceCursor / ForgetFenceGeneration and installation CanonicalCommitCursor. | D ForgetFence authority commits the fence and returns the cursor; D snapshot authority binds it into the BarrierSnapshotReceipt. | C2 is satisfied; fence has not been replaced between install and snapshot binding; install transaction is durable. | The same typed FenceCursor (including ForgetFenceGeneration) and install CanonicalCommitCursor are durably bound to the snapshot receipt. | Exact typed identity equality for cursor/generation and installation commit cursor. | Any changed generation/cursor/commit cursor => INVALID or STALE according to authoritative state-version result; unavailable state => UNKNOWN. Recovery resolves the original fence receipt, not a new generation. | ForgetFenceCursor; ForgetFenceGeneration; installation CanonicalCommitCursor. Distinct nominal types; no cross-domain arithmetic. | This file §2 D002-C3; D operation contract §§2, 3.3–3.4, 6. |
| D002-C4 | The InstallForgetFence durable receipt's captured_producer_registration_high_water equals the CaptureProducerRegistrationHighWater BarrierSnapshotReceipt's producer_registration_high_water as the same nominal type and same immutable snapshot. Equality is required; greater-than or less-than is never VALID. | D Install authority writes the cutoff; D Capture authority retrieves/verifies it; verifier compares only these two same-typed cutoff values after C1–C3 binding. | Fence install is durable; the same operation/fence/snapshot identity is known; Capture is not permitted to run as a new admission operation. | Install receipt and BarrierSnapshotReceipt retain the identical immutable ProducerRegistrationHighWater value and snapshot reference. | Exact typed equality under the same operation/fence/snapshot identity. | Any inequality => INVALID if explicit mismatch; UNKNOWN if the source or binding cannot be established. Capture MUST NOT repair mismatch by recapturing a later high-water. | captured_producer_registration_high_water and producer_registration_high_water: both ProducerRegistrationHighWater. Neither is ForgetFenceGeneration. | This file §2 D002-C4; D operation contract §§2, 3.3–3.4. |
| D002-C5 | The BarrierSnapshotReceipt binds the identities above plus a D-authoritative ledger consistency proof/reference. | D ledger/snapshot authority constructs and durably issues the receipt; verifier validates every binding and the consistency proof/reference. | C1–C4 bindings are available; D ledger snapshot is consistent; no unresolved ledger gap or registry incompleteness. | Immutable receipt includes authority, ledger identity, registry version, operation, target digest, fence cursor/generation, install commit cursor, cutoff, and ledger consistency proof/reference. | All bindings resolve to one immutable snapshot and D consistency evidence establishes a complete, gap-free snapshot. | Missing/malformed proof or explicit mismatch => INVALID; unavailable/incomplete ledger evidence => UNKNOWN/BLOCKED. Reconciliation may append evidence but cannot rewrite the old receipt or erase unresolved entries. | BarrierSnapshotReceipt; D ledger consistency proof/reference; identity fields and ProducerRegistrationHighWater already named above. | This file §2 D002-C5; D operation contract §§3.4, 3.8–3.9. |
| D002-C6 | The D serialization proof establishes that every accepted registration ordered before the fence linearization point has sequence <= H and is included in the barrier; ordinary covered registrations ordered after the fence are rejected/quarantined or explicitly cleanup-only and cannot publish. | D registration ledger and ForgetFence authority share one linearizable serialization domain per affected Brain Authority/source lineage; D barrier reconciler verifies inclusion/terminality. | C1–C5 are satisfied; registration and fence writes use the same authoritative ordering domain; registry and lineage inventory are complete. | The committed order, registration rows, fence snapshot, inclusion set, and post-fence dispositions are durable and auditable. | Every accepted pre-fence registration is included at/below H; every post-fence covered ordinary registration is rejected/quarantined/cleanup-only and has no ordinary publication path; no admitted-but-unaccounted publishable work exists. | If order/inclusion cannot be proven, barrier remains OPEN/UNKNOWN/BLOCKED. Partial inventory, split-brain ordering, or an unaccounted accepted registration MUST NOT produce VALID/DRAINED. Recover by same IDs and append-only reconciliation. | ProducerRegistrationSequence / ProducerRegistrationHighWater (same D registration domain); ForgetFenceCursor; CanonicalCommitCursor; work/registration/dependency receipts. No comparison to FenceGeneration or PermissionEpoch. | This file §2 D002-C6; D operation contract §§1, 3.2–3.4, 3.9, 4. |

### Why the six conditions form one proof

The result is VALID only if C1 AND C2 AND C3 AND C4 AND C5 AND C6 hold for the same immutable operation and snapshot. C1–C3 establish which authority, ledger, operation, fence, and commit the evidence concerns. C4 establishes that Install and Capture refer to the same immutable cutoff. C5 proves that the receipt is a complete D-authoritative snapshot rather than a bag of matching fields. C6 proves the ordering/completeness property that gives the cutoff its operational meaning. If any conjunct is false, the proof is INVALID/STALE as specified; if a required authority fact cannot be obtained, the result is UNKNOWN/BLOCKED. No subset of the six is sufficient.

## 3. State transition and durable-operation requirements

1. RegisterProducerWork and InstallForgetFence share one D-authoritative linearizable ordering domain per affected Brain Authority and source lineage.
2. The fence linearization point atomically makes the fence effective, allocates its ForgetFenceGeneration, captures the ProducerRegistryVersion and ProducerRegistrationHighWater, persists target binding/inventory snapshot and durable receipt/outbox intent. The install receipt is not successful before this commit.
3. Capture is a read/verification of the fence-bound immutable snapshot. It is not an admission write, a second cutoff, a reset, or a new high-water allocation.
4. A registration ordered before the fence point is included at or below H. A covered ordinary registration ordered after the fence point is rejected/quarantined or cleanup-only and cannot publish.
5. The barrier can be DRAINED only against immutable, explicit reconciliation checkpoints. Later-discovered pre-fence work or late derivatives reopen reconciliation; history is append-only.
6. Fence currentness/state-version and revocation are independent of C1–C6 high-water identity checks. They are evaluated from one authoritative state snapshot: mismatch => STALE; explicit revocation => INVALID; unavailable authority state => UNKNOWN. No TTL, local clock, or cached VALID substitutes.
7. No successful proof may be emitted from a partially committed receipt set. If the implementation cannot provide an atomic install receipt and snapshot binding, it must remain UNKNOWN/BLOCKED until reconciliation proves the exact durable outcome.

## 4. Required adversarial scenario proofs

### S1 — Two or more namespaces advance concurrently

- **Initial state:** Namespace N1 and N2 each have distinct authority/ledger namespace identity and committed registry version. Their existing fence/registration state is known. If they share a Brain Authority and source lineage, the D ordering domain is shared; otherwise their ordering domains are independent.
- **Operation sequence:** N1 and N2 each submit RegisterProducerWork and InstallForgetFence concurrently; each install binds its own operation ID, idempotency identity, target digest, registry version, FenceCursor, commit cursor and captured ProducerRegistrationHighWater. Capture then reads each fence's own immutable snapshot.
- **Possible interleaving:** N1 registration-before-fence while N2 fence-before-registration; or both registrations win; or both fences win. Same-authority/lineage events serialize at the common D linearization point; unrelated domains may progress independently.
- **Allowed result:** Each namespace independently satisfies all six conditions against its own immutable tuple. N1 may include its pre-fence registration while N2 rejects/quarantines its post-fence registration. Aggregate completion is permitted only when every required namespace has its own valid proof.
- **Must reject:** Comparing N1 installed/captured values with N2 values; cross-namespace equality/substitution; using one namespace's receipt or generation for the other; treating partial namespace success as global completion.
- **Crash point:** After N1 durable install but before N2 install, or after one Capture response but before the other.
- **Recovery state:** Resolve each operation by its own stable identity/digest. Preserve completed namespace receipt; retry the incomplete namespace with the same identity. Aggregate result remains OPEN/UNKNOWN until both required proofs are independently complete.
- **Evidence:** C1–C6; D operation contract §§2, 3.2–3.4, 3.8–3.9. No runtime race test is claimed by this document.

### S2 — Capture interleaves with install, replacement, or later publication

- **Initial state:** ForgetOperation is known; install may be pending, committed, or replaced by a newer fence. No Capture-created cutoff exists.
- **Operation sequence:** InstallForgetFence commits receipt and immutable cutoff H; Capture requests the receipt; independently, a new fence/revocation or publication attempt may race.
- **Possible interleaving:** Capture before install commit; Capture after install commit; fence replacement/state-version advance between issuance and verification; PublishDerivedIfFenceCurrent competes with fence install at the same serialization boundary.
- **Allowed result:** Capture before durable install => FENCE_NOT_INSTALLED/UNKNOWN. After install => returns the exact installed snapshot. Publish wins serialization first => artifact visibility is committed before fence and included in inventory/barrier. Fence wins first => covered publication is rejected. Currentness is evaluated from one authoritative version read.
- **Must reject:** Capture setting or advancing H; Capture returning a later ledger tip as a new cutoff; split currentness reads; retrying reads until a matching version appears; publishing from an earlier fence check after a later fence has won.
- **Crash point:** After fence commit but before Capture response; or after a fence/publication race has one durable winner but the caller sees no response.
- **Recovery state:** Resolve the original fence receipt; Capture replays the same snapshot. Resolve publication by original PublicationOperationId. A durable fence winner rejects publication; a durable publication winner remains in inventory. Unknown winner => private/UNKNOWN, not visible.
- **Evidence:** C3–C6; D operation contract §§3.3–3.6, 3.8.

### S3 — Same request replay and changed-payload replay

- **Initial state:** A request has stable ForgetOperationId, idempotency identity, canonical request digest and target-set digest.
- **Operation sequence:** Submit InstallForgetFence; replay the exact request; then separately attempt same identity with changed request digest or target digest.
- **Possible interleaving:** Replay arrives while first request is in flight, after durable commit, or after response loss.
- **Allowed result:** Exact replay returns or resolves to the same durable receipt, FenceGeneration, commit cursor and cutoff. Concurrent exact duplicates converge on the one idempotent result.
- **Must reject:** Changed digest under same operation identity => IDEMPOTENCY_CONFLICT; allocating a second generation/cutoff because ACK was lost; treating changed target as a replay.
- **Crash point:** Immediately before durable commit, immediately after commit, and after commit before response delivery.
- **Recovery state:** Before commit, retry same identity and allow one commit. After commit, lookup/replay returns original receipt. Changed digest remains rejected. No second cutoff is created.
- **Evidence:** C2–C4; D operation contract §§3.3–3.4, 3.8.

### S4 — Crash during operation (before/within/after durable commit)

- **Initial state:** Request identity is fixed; no successful receipt has yet been observed.
- **Operation sequence:** D validates request, enters serialization, writes fence/cutoff/registry/target/inventory/outbox state, commits, then emits response.
- **Possible interleaving:** Process or node crashes before commit; transaction aborts; crash occurs after commit but before receipt delivery; or a non-atomic implementation leaves partial durable rows.
- **Allowed result:** Pre-commit crash leaves no successful fence receipt and retry may commit once. Post-commit crash leaves the exact durable receipt recoverable. If atomicity cannot be established, result remains UNKNOWN/BLOCKED and target remains suppressed/private as applicable.
- **Must reject:** A receipt for uncommitted state; a partial row set interpreted as installed; minting a new operation/generation to escape uncertainty; publication from an ambiguous fence outcome.
- **Crash point:** Every write boundary, transaction commit boundary, and response boundary must be injected in conformance testing.
- **Recovery state:** Read authoritative durable state by original operation ID/digest. Recover exact receipt if committed; otherwise retry same request. Partial/inconsistent state enters reconciliation and cannot be VALID.
- **Evidence:** C2–C6; D operation contract §§3.3, 3.8–3.9. Crash-injection tests are NOT RUN here.

### S5 — Durable persistence succeeded but response was lost

- **Initial state:** InstallForgetFence has committed all atomic effects and receipt; client timed out before receiving response.
- **Operation sequence:** Client retries or calls ResolveProducerWork using the same operation ID and digest; Capture re-requests the same fence-bound snapshot.
- **Possible interleaving:** Retry arrives before the original response would have been delivered, or multiple identical retries race.
- **Allowed result:** All callers resolve to the same persisted receipt, generation, commit cursor and cutoff; Capture returns the same immutable snapshot.
- **Must reject:** Treating timeout as abort; new idempotency key/new generation; recapturing a later cutoff; accepting two different receipts for one operation identity.
- **Crash point:** Response lost after durable commit; server restart before retry.
- **Recovery state:** Original committed state is authoritative; return its exact receipt. If authoritative lookup is unavailable, UNKNOWN/BLOCKED until lookup succeeds.
- **Evidence:** C2–C5; D operation contract §§3.3–3.4, 3.8.

### S6 — Recovery repeats an operation after restart/restore

- **Initial state:** Durable operation may or may not exist; restored system may have replayed an older snapshot.
- **Operation sequence:** Reconcile operation ID/digest, fence generation/state version, ledger continuity and receipt; replay Install/Capture only with original identity.
- **Possible interleaving:** Retry races with background recovery; restore has stale local cache; old state version is observed before authoritative anti-rollback check.
- **Allowed result:** Exact committed receipt is reused; proven not-committed operation may be executed once; unprovable continuity or anti-rollback yields UNKNOWN/BLOCKED. Fence generation/state version cannot regress.
- **Must reject:** Reusing a prior VALID cache; restoring lower fence generation/state version as current; generating a fresh cutoff for an old operation; declaring absence from one stale replica to be proof of abort.
- **Crash point:** During recovery reconciliation, between authoritative read and durable repair, or after repair before ACK.
- **Recovery state:** Retry reconciliation with same identity and authoritative source; append evidence only. Do not reverse completed Forget effects or resurrect previously valid proof.
- **Evidence:** C2–C6; D operation contract §§3.8–3.9 and contract 1.3.1 §5.4.

### S7 — Partial success and partial failure across namespaces or sub-operations

- **Initial state:** A multi-namespace request has required namespace set {N1, N2, …}; each namespace has independent receipts and proof state.
- **Operation sequence:** Commit N1 install and snapshot; N2 fails or becomes unavailable; attempt aggregate barrier evaluation.
- **Possible interleaving:** One namespace commits while another returns registry gap, timeout, ledger unavailable, or explicit mismatch.
- **Allowed result:** N1's local proof remains valid for N1; aggregate barrier remains OPEN/UNKNOWN/BLOCKED until every required namespace independently satisfies all six conditions. Retry only failed/incomplete namespace using its original identity.
- **Must reject:** Rollback or invalidate a valid independent N1 receipt solely because N2 failed; conversely, treating N1 success as aggregate success; silently dropping N2; cross-namespace watermark arithmetic.
- **Crash point:** Between namespace commits or between sub-operation commits and aggregate response.
- **Recovery state:** Preserve durable successful namespace state; append reconciliation for failed namespace. Aggregate remains non-success until complete. If one namespace cannot be proven, no global VALID/DRAINED.
- **Evidence:** C1–C6; D operation contract §§3.3–3.4, 3.9. No cross-namespace transactional atomicity is claimed.

## 5. §5 conflict disposition against D-OWNER-2026-11-19-002

| 1.3.0 原规则 | 阻塞原因 | 1.3.1 修改后规则 | 精确规范位置 | 与 D-002 一致性 |
|---|---|---|---|---|
| captured 是 CaptureProducerRegistrationHighWater 结果；installed 是安装的 ForgetFence High Water。 | installed 可能指 ForgetFenceGeneration，与 ProducerRegistrationHighWater 不同名义类型。 | 明确为 Install receipt 的 captured_producer_registration_high_water 与 Capture receipt 的 producer_registration_high_water；两者同为 ProducerRegistrationHighWater。 | successor §5.1 | 一致；禁止跨命名空间/类型比较。 |
| installed = captured => VALID。 | 单独相等仍未证明 authority、operation、fence、cursor、snapshot 和 ledger 完整性。 | 仅作为 C4，且须先满足 C1–C3，并同时满足 C5–C6。 | successor §§5.1–5.3 | 一致；六条件合取，不是标量捷径。 |
| installed > captured => VALID。 | 更大值不可能是同一不可变 cutoff，意味着快照不一致或类型错误。 | 删除此成功规则；任何不相等均 fail-closed。 | successor §5.2 | 直接落实 D-002。 |
| installed < captured => INVALID。 | 标量大小关系不是证明模型，不能确定绑定/currentness。 | 删除数值关系表；明确不匹配 INVALID，证据不可得 UNKNOWN/BLOCKED。 | successor §5.2 | 直接落实 D-002。 |
| 两值按数值比较，接受前导零并按数值归一化。 | 不能靠表示规范化修复名义类型冲突。 | 各字段独立校验规范十进制表示；禁止跨字段算术/排序；只对同一 typed cutoff 作相等验证。 | successor §5.2 | 一致；不以字段名称/数值推断。 |
| §8 英文/中文决策表分别重复 installed = captured、installed > captured、installed < captured 三行。 | 即使 §5 改正，重复标量行仍会恢复旧规则或被误读为独立充分条件。 | 两种语言表均删除全部三条标量比较行，替换为同一 typed cutoff + 六条件合取；不匹配/不可用均 fail-closed。 | predecessor EN lines 259–261 / ZH lines 546–548; successor §6 | 一致；无规范性重复冲突。 |

### 5.1 Exact source line mapping\n\n- Predecessor 1.3.0 English §5: lines 151–178; the conflicting scalar result rows are lines 162–164.\n- Predecessor 1.3.0 English §8: lines 241–263; the scalar result rows are lines 259–261.\n- Predecessor 1.3.0 Chinese §5: lines 438–465; the conflicting scalar result rows are lines 449–451.\n- Predecessor 1.3.0 Chinese §8: lines 528–550; the scalar result rows are lines 546–548.\n- Successor 1.3.1 §5 contains the six conjuncts and comparison semantics; successor §6 removes the old scalar table rows in both language peers. Exact successor line ranges are pinned in the commit readback record on Issue #43.\n\n## 6. Unicode version and reproducible canonicalization

- **Pinned data version:** Unicode 15.1.0.
- **Normative source:** Unicode Standard Annex #15, Unicode Normalization Forms; Unicode Character Database 15.1.0 files CaseFolding.txt, DerivedNormalizationProps.txt, PropList.txt, and NormalizationTest.txt. Obtain only from the versioned Unicode 15.1.0 UCD distribution, not an unversioned “latest” endpoint.
- **Bound behavior:** first three namespace segments: NFKC → Default Case Folding (statuses C/F; Turkic T mappings excluded) → NFKC → trim using Unicode 15.1.0 White_Space. Fourth version segment: NFKC and trim per existing rule, no case folding. Existing decode-once, UTF-8, slash-injection, canonical re-encoding and idempotence rules remain unchanged.
- **Implementation binding:** implementation MUST expose/build-record unicode_data_version = 15.1.0; runtime/library-reported Unicode version MUST equal 15.1.0. A mismatch MUST fail closed at startup/validation, not silently use host defaults. Conformance build MUST pin the UCD package/data artifacts and record SHA-256 for each vendored data file in its lock manifest. Hash values are intentionally NOT asserted here because the files are not vendored or independently hashed in this commit.
- **Upgrade rule:** a Unicode data upgrade is a new normative contract revision, never a transparent dependency bump. D must publish a versioned migration plan, compare old/new canonical outputs over the full corpus and adversarial vectors, identify collisions/splits, preserve old canonical identifiers as immutable historical identities, and require explicit namespace migration with continuity proof. No mixed-version comparison or implicit recanonicalization is allowed. If continuity/collision behavior is not proven, result is UNKNOWN and migration is blocked.
- **Validator rule:** validator MUST compare actual UCD/runtime version to the contract pin and verify locked data artifact hashes before accepting a canonicalization proof. It MUST run Unicode 15.1.0 NormalizationTest corpus plus D-specific vectors (fullwidth A, U+FF0F slash, U+3000 whitespace, percent-encoded UTF-8, malformed UTF-8, double-decode and idempotence). Merely printing “15.1” or using a default runtime is insufficient.
- **Evidence status:** normative version and binding rule are fixed. No production validator was changed or run in this commit; no UCD files/hash lock was vendored; cross-runtime conformance remains NOT RUN.

## 7. Scope and non-scope

**Changed by this delivery:** D normative successor contract 1.3.1; D-002 operational proof package; §5 replacement; Unicode version pin and implementation-binding requirement.

**Not changed:** D operation implementation, H schema/validator, Storage engine/topology, D/H query transport, cryptographic algorithm/key registry implementation, I revocation mechanism, runtime database, CI configuration, and production activation. No tests or validator source were changed. No D/H joint acceptance is made.

**Evidence classification:** the six-condition operational argument is a normative protocol proof and adversarial scenario analysis. It is not a runtime execution trace or proof of an existing deployed implementation. CI NOT RUN; implementation conformance NOT VERIFIED.

## 8. Decision and return

**Decision ID:** D-OWNER-2026-11-19-003

**Decision:** ACCEPT the normative successor text 1.3.1 and the six-condition D proof rule within D Owner authority. This supersedes the conflicting §5 scalar predicate of 1.3.0. It does not retroactively accept the 1.3.0 Blob, does not authorize H to consume 1.3.1, and does not claim implementation/conformance/production readiness.

**Finding boundary:**
- F-43-01/F1 remains OPEN pending exact implementation, deterministic race/replay/crash/restore conformance, and A Integration verification.
- F-43-01/F3 remains OPEN; this is D-side evidence only. H Owner must independently accept the exact D/H mapping.
- F-43-02 is submitted to A Integration for independent exact-source verification and status decision; D Owner does not close A's ledger finding.
- No PR, Issue, or branch was created. This return is for existing Issue #43 only.
