# Phase 1.G — A Exact Integration Re-review: Storage v3.2.7 / H 1.2.14 Full-Path CI
# Phase 1.G — A 精确集成复审：Storage v3.2.7 / H 1.2.14 Full-Path CI

- Reviewer perspective: A — Principal Integration Architect
- Review target: Storage v3.2.7 successor exact-version manifest
- Exact manifest Blob: fe1dcfcc4a40f70b6023f6c93cdf986d15583d29
- Storage manifest commit: 2658ce0065c07b59b154d31c95c38b0993db7419
- H Unified 1.2.14 schema Blob: 09fcd1fa29fe24255fbd87cae79dafb406594a59
- CSubmitOutcome 1.0.1 schema Blob: a631bc7a519be7ce93fcfd7c548fa2ca8e8c1cda
- H authority-join mapping Blob: 1cbe74eba69325510d6b1019d971661f965eabf8
- H validator Blob: eab961a08d41e871f38543b18ee60cf024977414
- H full-path test Blob: dccf8c099c18807ec072870d32604d0912209f01
- H full fixture Blob: c80247a6ecfbb4a29ff0993e8e2aea4829d00626
- H exact Provider Outcome CI run: 44069941327, commit ba2c9341fee4eb9ca9e665c74bdd37b4675dd251, job 133993324484, SUCCESS — 32 tests.
- Disposition: **ACCEPT AS A COHERENT ARCHITECTURE CANDIDATE WITH ENUMERATED BLOCKERS — DO NOT FREEZE**
- Provenance: delegated A-role integration simulation in the coordinating session; **not an independent human A Owner acceptance**.
- English and Chinese are normative peers.

## 1. Exact integration decision / 精确集成决议

The refreshed v3.2.7 manifest binds one coherent candidate set: H Unified 1.2.14 / wire 1.3.0, CSubmitOutcome 1.0.1, H C-object mapping, distinct I/D/Storage authority callback seams, RecoveryJoin 1.0.2, RecoveryCutoff 1.0.5, the actual H validator, full positive fixture and exact CI run 44069941327.

A verified the H CI job log. The run executed 32 tests: 26 H validator tests and six Python/Node C crypto interoperability tests. Tests 21–25 explicitly exercised the full H envelope + immutable C object path using actual H/C schemas, actual local semantic predicates and actual C-P0 digest recomputation, without patching those local functions. Negative cases cover one duplicate-field mismatch, digest mutation, missing I/D/Storage callbacks (UNKNOWN), and False I/D/Storage callbacks (INVALID).

This closes the earlier A concern that only callback orchestration was tested. It does **not** close complete per-field negative coverage or production authority integration. The current H branch head differs from the tested CI commit only by three documentation files; schema, validator, test and fixture Blobs are unchanged.

v3.2.7 records exact C/D/I/H delegated role reviews of the full-path fixture and authority boundaries. Their exact Blob scope is useful, but these are coordinating-session role artifacts, not independent human Owner signatures. No approval is transferred from an older Blob.

本次 v3.2.7 清单已绑定一致的候选版本集：H Unified 1.2.14 / Wire 1.3.0、CSubmitOutcome 1.0.1、H C Object Mapping、独立 I/D/Storage Authority Callback、RecoveryJoin 1.0.2、RecoveryCutoff 1.0.5、真实 H Validator、完整正向 Fixture 与精确 CI Run 44069941327。

A 已核验 H CI Job Log。Run 共执行 32 项：26 个 H Validator 测试和 6 个 Python/Node C Crypto Interoperability 测试。Test 21–25 显式执行完整 H Envelope + 不可变 C Object 路径，使用真实 H/C Schema、本地 Semantic Predicate 和 C-P0 Digest 重算，未 Patch 这些本地函数。负向用例覆盖一个重复字段不一致、Digest 变异、缺失 I/D/Storage Callback（UNKNOWN）以及 False Callback（INVALID）。

这关闭了此前仅验证 Callback 编排的缺口，但**未关闭每个字段的完整负向覆盖或生产权威集成**。当前 H Branch HEAD 相对测试 Commit 仅多三个文档文件；Schema、Validator、Test、Fixture Blob 未变。

v3.2.7 记录了 C/D/I/H 对 Full-Path Fixture 与 Authority Boundary 的精确角色复审。其 Blob 范围可核验，但这些仍是协调会话角色工件，不是真正独立人类 Owner 签署。不得将旧 Blob 的接受转移到新 Blob。

## 2. Blocking conditions / 阻断条件

### A1 — Independent Owner adoption remains required

C, D, I, H and Storage must obtain their own independent Owner decisions against the exact current bundle. Current C/D/I/H review documents are delegated role simulations. This A review is also delegated role simulation. No document authored in this coordinating session may be counted as independent Owner approval.

### A2 — H full-path negative coverage is partial

The full-path test proves a real local schema/semantic/digest execution, but currently exercises only:
- one duplicated wire field (provider_ref) mismatch;
- one payload-digest mutation;
- missing I/D/Storage callbacks → UNKNOWN;
- each I/D/Storage callback returning False → INVALID.

Still required: per-field mutation of every duplicated wire member; exact object identity/ref/digest mutation; C sequence namespace/key-status namespace mismatch and rollback/fork; duplicate raw JSON member and malformed UTF-8/constant cases through validate_raw_provider_outcome; stale key/currentness, rollback/fork and signature/preimage mismatch through full path. A single successful local fixture is not broad semantic conformance.

### A3 — I terminal authorization semantics

The H verify_i_terminal_decision slot is only an injected callback. Production I verifier must authenticate the exact I-signed terminal proof and bind operation, participant, PolicyDomain, admission, scope generation, I ledger entry, PermissionEpoch, key-status/history checkpoint, final I GateGeneration and currentness CAS. Provider invocation requires the exact applicable I COMMIT_WON; arbitrary terminal I outcome is not sufficient.

### A4 — D Forget clearance semantics

The H verify_d_clearance slot is only an injected callback. Production D verifier must bind exact Forget operation/scope, FenceGeneration, complete affected producer/work/attempt/derivative lineage, barrier generation/root/terminality, D owner-ledger high-water/root, snapshot attestation, late-discovery successor snapshot and final D-local currentness CAS. D lineage pagination and late-discovery fault proof remain OPEN.

### A5 — Storage same-GID proof semantics

The H verify_storage_resolution_proof slot is only an injected callback. Production Storage verifier must bind DB incarnation, GID, PrepareAttempt, participant ledger/version, authoritative terminal outcome, same-GID visibility and current database authority. The schema/reference alone does not prove a deployed Storage adapter or actual same-GID recovery.

### A6 — R1/R2, Gate A/B/C and deployment evidence

The bundle does not close Recovery Cutoff Batch completeness, owner-local gate linearization/release, COC quorum persistence, exact prefix/readback, deployed Storage recovery or executable distributed fault injection.

## 3. Gate and authorization statement / Gate 与授权状态

- JF-10 P0: **OPEN**.
- R1 Recovery Cutoff Batch completeness: **OPEN**.
- R2 owner-local Gate linearization/release: **OPEN**.
- Gate A Storage architecture: **PARTIAL PASS / OPEN**.
- Gate B COC persistence deployment: **BLOCKED**.
- Gate C executable end-to-end implementation fault injection: **DEFERRED TO ENGINEERING / NOT RUN**.
- Multi-PolicyDomain atomicity: **BLOCKED**.
- C/I production profile registration, trust roots, key custody, anti-rollback and historical verification: **NOT APPROVED / OPEN**.
- Provider issuer truth, same-key lookup, send-vs-close, lost-ACK/retry/failover and exactly-once: **NOT PROVEN**.
- Production activation/provider egress, Full Applied, Global Forget completion and physical Forget: **NOT AUTHORIZED / NOT PROVEN**.

## 4. Required next sequence / 后续执行顺序

1. Obtain independent human Owner decisions from C, D, I, H and Storage against the exact current artifacts; do not count delegated role documents as approvals.
2. Expand H full-path negative tests across every duplicated wire field, C identity/digest, sequence namespace/key-status relation and raw JSON parsing.
3. Implement I-authoritative terminal proof verification with COMMIT_WON semantics and final I currentness CAS.
4. Implement D-authoritative lineage/Forget clearance verification with complete pagination, late-discovery handling and final D currentness CAS.
5. Implement Storage-authoritative same-GID resolution proof verification bound to DB incarnation, prepare attempt, participant ledger and visibility.
6. Close C provider outcome evidence, same-key lookup and send-vs-close/retry/failover fault handling.
7. Close R1/R2, JF-10 P0 and Gate A/B/C only with their specified independent evidence; then A must re-review the resulting exact successor bundle.

## 5. Final A disposition / A 最终结论

**ACCEPT AS A COHERENT ARCHITECTURE CANDIDATE WITH ENUMERATED BLOCKERS — DO NOT FREEZE.**

The full local H/C schema/semantic/digest path is now demonstrated. The system remains in architecture-design phase; production trust, authority adapters, storage durability, owner-local gate linearization, fault injection and release authorization remain unproven or blocked.

**接受为具有明确阻断项的连贯架构候选——不得冻结。**

完整本地 H/C Schema/Semantic/Digest 路径已得到验证。系统仍处于架构设计阶段；生产 Trust、Authority Adapter、Storage Durability、Owner-local Gate Linearization、Fault Injection 与发布授权仍未证明或受阻。

---
**Provenance:** This is a delegated A-role review performed by the coordinating session, not an independent human A Owner acceptance or production gate approval.
