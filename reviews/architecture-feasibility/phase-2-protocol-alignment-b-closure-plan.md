# ARCH-CONSOL-002 — B: Cross-Owner Protocol Alignment Review
# ARCH-CONSOL-002 — B：跨 Owner 协议精确对齐审查

- Repository: \`oahcom/AiMemoryBrainArchitecture\`
- Scope: C / H / D / I / Storage exact Provider Outcome and owner-proof wire bindings
- Review mode: exact-Blob inspection and delegated role synthesis; not independent Owner approval
- Status: **PARTIAL ALIGNMENT EXISTS / EXACT BUNDLE NOT YET CLOSED**
- Branch: \`review/arch-consol-002-protocol-alignment-2026-11-17\`

## 1. Executive disposition / 总体裁决

**EN:** The earlier Phase 2 report overstated the C/H version gap. A current candidate alignment already exists: H has a 1.2.12 → CSubmitOutcome 1.0.1 exact consumer mapping; C has a 1.0.1 immutable sequence-namespace amendment; I has reviewed that required signed field; H's validator contract §§19–21 record the current 1.2.12 / 1.0.1 target and a 17-test candidate run. C reports a separate 19-test candidate run. These are meaningful architecture-level progress and must not be discarded.

However, the cross-owner *exact bundle* is still not closed. The Storage v3.2.4 successor manifest still pins CSubmitOutcome 1.0.0 and omits the new C 3.11.1 / I 3.8.8 / H exact mapping chain. The H mapping pins an older Blob of the 1.2.12 schema (a one-line descriptive revision-label mismatch versus the actual current H branch file). Several historical C semantic/projection artifacts still explicitly bind H 1.2.11, and the old H validator contract retains superseded 1.2.11 normative text in §§1–18. D/I adoption artifacts are candidates, not independent Owner approvals. Therefore B is **not complete**, but the remaining work is now precise and bounded.

**中文：** 上一轮 Phase 2 报告对 C/H 版本缺口的描述过重。当前已经存在一条候选对齐链：H 发布了 1.2.12 → CSubmitOutcome 1.0.1 精确消费映射；C 发布了 1.0.1 不可变 Sequence Namespace 修订；I 已审查该必需签名字段；H Validator 合同 §19–21 记录当前 1.2.12 / 1.0.1 目标及 17 项候选测试；C 另有 19 项候选测试。这些是实际架构进展，不应否定或重复实现。

但跨 Owner **精确版本包**尚未闭环。Storage v3.2.4 后继清单仍绑定 CSubmitOutcome 1.0.0，未纳入 C 3.11.1 / I 3.8.8 / H 精确 Mapping 链。H Mapping 仍绑定较早的 1.2.12 Schema Blob；与 H 当前分支文件相比，唯一内容差异是 Schema 描述中的 Artifact Revision 文案仍写 1.2.11。多个历史 C 语义/签名投影工件仍明确绑定 H 1.2.11；旧 H Validator 合同 §1–18 仍保留已被后续章节取代的 1.2.11 规范性文字。D/I 采纳文件仍是候选，不是独立 Owner 批准。因此 B **尚未完成**，但剩余工作已能精确界定。

## 2. Exact current source / consumer chain / 当前精确源—消费链

| Role | Exact artifact | Blob | Current disposition |
|---|---|---|---|
| H schema | BMCP Unified 1.2.12 on H branch | \`9aa366d857d0229687df7e44e8e70d2097a99237\` | Current branch file; wire family 1.3.0 |
| H RecoveryJoin | RecoveryJoin 1.0.2 | \`4b664e3bce465499bcdfd93796349a4ba7074002\` | Candidate structural proof carrier |
| H R1/R2 crosswalk | Phase 3.8.6 | \`8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c\` | Correctly identifies Unified 1.2.12 / RecoveryJoin 1.0.2 |
| C immutable object | CSubmitOutcome 1.0.1 schema | \`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda\` | Current proposed immutable object revision |
| C semantic amendment | Phase 3.11.1 | \`6fa67af110ebbc5ef57ed908bb4880d99c5e46fb\` | Explicit required signed sequence namespace; supersedes 1.0.0 for new records |
| I review | Phase 3.8.8 | \`0d78e5b2bfcf66cae6b757314cead84b9c942601\` | Accepts namespace as required/signed; no profile registration |
| H exact consumer mapping | Phase 3.8.7 | \`fad28f1b62f6a686669e209ebe30d69df6330d75\` | Accepts 1.2.12 / 1.0.1 mapping as proposal; not frozen |
| H validator core | Current core | \`1a92c0cf7146e2884bd38232005dd9a55d558a85\` | Requires C 1.0.1 and sequence namespace; callbacks not production-connected |
| H validator contract | Phase 3.8.5 current file | \`62b740696b4a5335f19f82e83fe4d4ce8b4e0f4e\` | §§19–21 current target; §§1–18 historical/superseded |
| Storage exact bundle | v3.2.4 successor manifest | \`6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7\` | Stale: C 1.0.0 and earlier C/H bindings remain pinned |

**Exact schema Blob correction:** H mapping Blob \`fad28f...\` and Storage manifest pin \`a54f669...\` bind an older copy of Unified 1.2.12. The current H branch file is Blob \`9aa366...\`. A line-by-line comparison found exactly one difference: the current file's schema description says artifact revision 1.2.12, while the older pinned Blob's description says 1.2.11. The schema's actual version fields remain 1.2.12 and wire family 1.3.0. This appears non-functional, but exact-Blob governance forbids treating the two blobs as interchangeable. H must re-pin the current Blob and rerun the exact mapping/conformance bundle; D/I/Storage must consume the same new pin.

**精确 Schema Blob 修正：** H Mapping Blob \`fad28f...\` 和 Storage 清单中的 \`a54f669...\` 绑定的是较早的 Unified 1.2.12 副本。H 当前分支文件 Blob 是 \`9aa366...\`。逐行比较发现唯一差异是 Schema description：当前文件写 Artifact Revision 1.2.12，旧 Blob 写 1.2.11。Schema 实际版本字段仍为 1.2.12，Wire Family 仍为 1.3.0。该差异看起来不影响运行语义，但精确 Blob 治理不允许将两个 Blob 视为相同。H 必须重新绑定当前 Blob 并重跑精确 Mapping/Conformance，D/I/Storage 随后消费同一新 pin。

## 3. What is already proven — and what is not / 已有证明与证明上限

### 3.1 Candidate structural and cross-language evidence

- C run \`44059935858\`, commit \`b49966361b4b3121a2ebf4105b4e0c57a612e945\`: SUCCESS, 19 tests. Covers CSubmitOutcome 1.0.1 schema, ten structural/semantic vectors, candidate Ed25519 cases, field-mutation rejection and Python/Node agreement.
- H run \`44060704553\`, commit \`8c377a7218b70621d2348b47341d4cf4755b3733\`: SUCCESS, 17 tests. Covers 1.0.1 namespace validation, five candidate crypto vectors, field-mutation rejection and H Python/Node agreement.
- I Phase 3.8.8 accepts the sequence namespace as a required signed field and explicitly does not register either profile.
- H exact mapping distinguishes C-authored Provider Outcome from external COC, I, D and Storage evidence; external proof refs are validated under their own issuers and authority callbacks.

### 3.2 Explicit evidence ceiling

These tests and documents do **not** prove:
- production registration of \`AIMBA-C-CRYPTO-1.0\` or \`AIMBA-I-KEY-GOVERNANCE-1.0\`;
- production trust roots, HSM/KMS, key custody, revocation or external anti-rollback;
- a deployed durable C sequencer or authenticated C key-status ledger;
- provider issuer truth, provider-specific idempotency, real adapter race/fault behavior;
- production COC quorum, Storage durable joins or end-to-end owner callback wiring;
- independent human C/H/D/I/Storage Owner approvals.

### 3.3 Authority rules that remain normative

1. C alone owns immutable Provider Outcome truth, final transport handoff boundary, C admission/attempt/gate and C signing sequence.
2. H owns BMCP wire structure, exact field mapping, schema/version checks and tri-state validation orchestration; it cannot manufacture C/I/D/Storage truth.
3. I owns profile registration, governance trust, key lifecycle and PermissionDomain decisions; accepting a signed field is not profile registration.
4. D owns Memory/ForgetFence and D lineage/participant semantics; it cannot delegate those semantics to H.
5. Storage owns durable transaction/visibility/physical recovery and exact version bundle binding; a Storage manifest is not an Owner approval.
6. COC records causal-order/recovery evidence; it is not the C Provider Outcome authority or the JF-10 coordinator.

## 4. Contradictions and migration debt / 矛盾与迁移债务

| ID | Severity | Exact issue | Required successor |
|---|---|---|---|
| B-01 | P1 | H exact mapping pins old Unified Blob \`a54f...\`; current H branch is \`9aa366...\` (one stale descriptive revision label). | H republishes mapping against exact current Blob; rerun H tests; D/I/Storage re-pin. |
| B-02 | P1 | Storage v3.2.4 manifest still lists C 1.0.0 schema/vectors and old Phase 3.8.6–3.8.9 C docs as current. | Storage publishes a successor manifest binding C 1.0.1, C Phase 3.11.1, I Phase 3.8.8, H exact mapping/core and current H schema. |
| B-03 | P1 | C Phase 3.8.6/3.8.7/3.8.8 and Phase 3.8.9 historical docs retain H 1.2.11 and/or C 1.0.0 pins. | C publishes one explicit successor applicability addendum (do not rewrite historical artifacts) binding H 1.2.12 exact current Blob and C 1.0.1, while preserving the 1.0.0 history. |
| B-04 | P1 | H validator contract title and §§1–18 still state 1.2.11 / C 1.0.0; §§19–21 later supersede them, creating two apparent normative targets. | H publishes a consolidated currentness amendment or clean successor contract making §§1–18 explicitly historical and pointing to exact current 1.2.12 / 1.0.1 mapping. |
| B-05 | P1 | D/I candidate membership adoption artifacts pin old H schema Blob \`a54f...\`; no fresh exact re-review against current H Blob \`9aa366...\`. | D and I each publish exact successor pin/review on their own branches; delegated simulation must remain labelled as such. |
| B-06 | P1 | Storage manifest has not yet composed the C/H/I exact source-consumer chain or received fresh C/H/D/I exact reviews against one identical manifest. | Storage publishes manifest first; C/H/D/I review that exact manifest; A integrates only after all exact dispositions. |
| B-07 | P1 | C/I crypto profiles remain PROPOSED_NOT_REGISTERED; H authority callbacks are not production-connected. | Keep activation blocked; registration and production trust are separate later gates, not papered over by schema alignment. |

## 5. Ordered closure plan / 按序闭环计划

### Step B1 — C source successor / C 源合同后继修订
C must publish a bilingual successor applicability amendment that:
- declares CSubmitOutcome 1.0.1 the current proposed immutable object revision for new records, with 1.0.0 retained as historical;
- binds C Phase 3.11.1 Blob \`6fa67af...\`, schema Blob \`a631bc...\`, vectors \`c447f8...\`, crypto manifest \`3a5fb...\`, expected vectors \`34e49a...\`;
- updates the applicability of the 3.8.6 semantic amendment and 3.8.8 projection to H Unified 1.2.12 exact current Blob \`9aa366...\`, without changing their historical source blobs;
- binds H mapping Blob \`fad28f...\` only as the current *candidate* mapping until H re-pins its corrected schema Blob;
- explicitly keeps the C profile NOT REGISTERED and provider/authority integration NOT PROVEN.

### Step B2 — H consumer successor / H 消费方后继修订
H must publish a clean current validator/mapping bundle that:
- pins exact Unified schema Blob \`9aa366...\`, wire version 1.3.0, artifact revision 1.2.12;
- pins RecoveryJoin 1.0.2 Blob \`4b664e...\` and RecoveryCutoff 1.0.5 exact current Blob after re-read;
- pins CSubmitOutcome 1.0.1 Blob \`a631bc...\`, C semantic amendment \`6fa67a...\`, I review \`0d78e5...\`;
- pins the current H validator core \`1a92c0...\` and the H exact mapping, with a new Blob after correction;
- records the 17-test run as candidate-only historical evidence and reruns tests against the exact successor Blob set;
- labels the old 1.2.11 sections historical, not a second active target.

### Step B3 — D/I exact successor reviews / D/I 精确后继复审
D and I must independently re-pin the corrected H Unified Blob and RecoveryJoin/RecoveryCutoff bundle, preserve their own authority boundaries, and review the same C/H source chain. Their prior Phase 3.8.5 candidate adoption artifacts are not upgraded by implication.

### Step B4 — Storage manifest successor / Storage 精确清单后继
Storage must publish a new successor manifest that:
- removes C 1.0.0 as the current binding and records it only as historical;
- pins C 1.0.1 source + amendment + vectors, I review, H mapping + validator core + corrected schema, D/I successor pins and Storage visibility contract;
- includes exact HEAD commits and exact Blob SHAs;
- records every Owner disposition and its provenance;
- preserves COC and JF-10 as separate protocols;
- does not declare the bundle frozen merely because all documents exist.

### Step B5 — Exact cross-owner review / 精确跨 Owner 复审
C/H/D/I each review the same Storage manifest SHA; Storage records exact review references; A performs the integration review only after all required Owner responses. No auto-approval, no inherited approval, no schema freeze and no production activation.

## 6. Acceptance criteria for B / B 阶段验收标准

B can be marked **CONDITIONALLY ALIGNED** only when:
1. one exact H schema Blob is consumed by H mapping, H validator, D, I and Storage;
2. one exact C object schema (1.0.1) is consumed by C contract, H mapping/validator, I review and Storage manifest;
3. C 1.0.0 is explicitly historical and never silently parsed as 1.0.1;
4. all source/consumer references are acyclic and exact;
5. C/H candidate CI reruns against the final exact blobs;
6. D/I/C/H/Storage dispositions are bound to the same successor manifest;
7. all evidence ceilings and unregistered production trust remain explicit.

B is **not** allowed to approve D/Storage transaction topology. That is Phase A and begins only after this protocol bundle is stable enough to serve as its input.

B 只有在同一个 H Schema Blob 被 H Mapping、H Validator、D、I、Storage 同时精确消费；同一个 C 1.0.1 对象 Schema 被 C 合同、H Mapping/Validator、I Review、Storage Manifest 同时绑定；1.0.0 明确降为历史；引用无环且精确；CI 对最终 Blob 重跑；D/I/C/H/Storage 对同一 Manifest 完成各自审查；证据上限和生产信任未注册状态仍明确时，才可标记 **CONDITIONALLY ALIGNED**。

B 不得批准 D/Storage 事务拓扑。该事项属于后续 A 阶段，必须以稳定的协议包作为输入。

## 7. Sources / 精确来源

- CSubmitOutcome 1.0.1 schema: \`a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda\`
- C Phase 3.11.1 amendment: \`6fa67af110ebbc5ef57ed908bb4880d99c5e46fb\`
- I Phase 3.8.8 review: \`0d78e5b2bfcf66cae6b757314cead84b9c942601\`
- H Unified current branch file: \`9aa366d857d0229687df7e44e8e70d2097a99237\`
- H Unified previously pinned Blob: \`a54f66914a819d77f00c6af04e76453ff9f654ee\`
- H Phase 3.8.7 exact mapping: \`fad28f1b62f6a686669e209ebe30d69df6330d75\`
- H validator contract current file: \`62b740696b4a5335f19f82e83fe4d4ce8b4e0f4e\`
- H validator core: \`1a92c0cf7146e2884bd38232005dd9a55d558a85\`
- Storage v3.2.4 successor manifest: \`6fc0bedaf5421d1be5a9ab5fb4d8cfab2871d7d7\`
- C CI: run \`44059935858\`, commit \`b49966361b4b3121a2ebf4105b4e0c57a612e945\`
- H CI: run \`44060704553\`, commit \`8c377a7218b70621d2348b47341d4cf4755b3733\`

All owner-branch files remain unchanged by this review branch.
