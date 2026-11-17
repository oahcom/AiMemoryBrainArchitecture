# Phase 3.8.25 — H Applied Delivery Evidence 1.0.0 Hardening Addendum
# Phase 3.8.25 — H Applied Delivery Evidence 1.0.0 加固补充

- Parent candidate: Phase 3.8.24, schema Blob \`2ce8776ca5ee5e014b234dc3eb34a7cb7961e608\`.
- Scope: H-ADE-001 duplicate JSON member rejection and H-ADE-003 current authorization before replay-result disclosure.
- Status: **CANDIDATE REMEDIATION BRANCH; EXACT CI AND H/I/D OWNER ACCEPTANCE PENDING**.
- This addendum does not amend CSubmitOutcome semantics, G Applied acceptance, I authorization policy, or D ForgetFence authority.

## 1. Duplicate-key parsing

The reference validator now parses with an \`object_pairs_hook\` that rejects duplicate member names at every JSON object depth before schema validation, P0 construction, digest comparison or signature callback invocation. This prevents the default decoder's last-value-wins behavior from hiding conflicting signed fields.

The candidate test suite adds top-level and nested duplicate-member negative vectors. The schema's \`additionalProperties: false\` remains necessary but is not a substitute for duplicate-aware raw JSON parsing.

## 2. Replay disclosure authorization

The validator contract now requires two separate callbacks for SAME_DIGEST_REPLAY: verify_current_i_replay_authorization(envelope, original_result_ref) and verify_current_d_forget_fence(envelope, original_result_ref). Each runs in its own authority domain and is tri-state:
- Both True: the original result reference may be returned.
- Either False: INVALID; do not disclose the result reference.
- Either None or exception: UNKNOWN; do not disclose the result reference.

The I callback rechecks current I authorization/PermissionEpoch, issuer/key status, principal/delegation, audience and scope. The D callback independently rechecks the applicable ForgetOperation/Fence/lineage currentness. Neither authority may substitute for the other. A historical signature and same digest do not confer perpetual disclosure authorization.

Candidate tests cover denial, UNKNOWN and callback exception; all assert that \`original_result_ref\` is absent.

## 3. Remaining blockers

- H-ADE-002 / C/G mapping is now implemented as a reference-code candidate in Phase 3.8.26: injected C resolver/verifier, immutable C identity requirements and exact H/C record ref, sequence, payload digest and final-boundary equality, with negative fixture mutations. Real C Owner Ledger/signature verification remains OPEN.
- H production trust roots, H key/profile registration, production canonicalization/signature, durable replay ledger, crash-safe reservation and runtime Adapter integration remain OPEN.
- The new callback is an adapter seam. This branch does not implement I or D authority ledgers and cannot claim their production checks.
- G has issued Phase 3.8.23 as a delegated candidate consumer decision for this H 1.0.0 family; it is not an independent human G Owner signature or production acceptance.
- No C/G/H Full Applied freeze or production activation is implied.

## 4. Verification required

Run the H Applied Delivery Evidence conformance workflow against the exact final head; read back validator, tests and workflow pins; obtain H review of this addendum and exact I/D review of the replay authorization callback contract. The branch remains a candidate until those steps complete.

**Disposition: H-ADE-001 duplicate-key rejection, H-ADE-002 CSubmitOutcome reference join, and H-ADE-003 separate I/D replay rechecks have candidate reference-code/test coverage. The current 29-test suite must run on the exact current Head; production/Owner closure remains NOT VERIFIED.**


## 5. Current exact-head validation boundary — 2026-11-18

The current H Owner branch Head is `b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9`. The current validator/test Blobs are `8febb915ec321cc37cf159b2f5b917a3f945726c` and `77cb66b895c5293a2f4883b1d5cb69775e71d00c` respectively; the suite contains 29 tests. The cited 26/26 run `44180835412` belongs to earlier H Head `9fb2097905ef653b3a2048ac5f6804fc94178d8d`, not the current Head. The current-mainline integration PR adds a PR-triggered workflow so the exact 29-test suite can be run before candidate merge. No test pass is claimed until that run completes.

当前 H Owner 分支 Head 为 `b14e388e9e8ecc19f9c51fed67818e9cc69ef4d9`。当前 Validator/Test Blob 分别为 `8febb915ec321cc37cf159b2f5b917a3f945726c` 和 `77cb66b895c5293a2f4883b1d5cb69775e71d00c`，套件共 29 项测试。引用的 26/26 Run `44180835412` 属于较早 H Head `9fb2097905ef653b3a2048ac5f6804fc94178d8d`，不是当前 Head。当前主线集成 PR 使用 PR 触发工作流，以便在候选合并前运行精确 29 项测试。运行完成前不宣称测试通过。
