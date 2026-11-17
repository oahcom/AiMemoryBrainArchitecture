# Phase 3.8.3 — H Independent JCS / Ed25519 Candidate Conformance Result
# Phase 3.8.3 — H 独立 JCS / Ed25519 候选一致性结果

- Workflow: H Recovery Cutoff Conformance
- Run: [44044050598](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44044050598)
- Job: `semantic-and-wire-tests`, job ID `133905263073`
- Checked-out commit: `f85c6c0c38cf629b553abb35e5611e89d552942b`
- Result: **101 tests PASS / 0 failures / 0 skipped**
- I profile proposal: `5eeb011032c53c2f7897d699d6f512b26f07d0a2`
- H mapping: `b132e6a01bcfe13f92020b9778ee3f7ddbf65753`
- Unified schema 1.2.8: `70b892797d07489936300a26c0dedfafe1d6e746`
- RecoveryJoin schema 1.0.1: `f94e01cf30b4c59fca24cb4ccd8b76a0db8ca95c`
- Python JCS/Ed25519 test: `73a8c27bb8ec63fc1f0e6cf605c0ad4c67dd366a`
- Node JCS/Ed25519 oracle: `232f0e427be57fe22ff614e9a017589064be659d`
- Five fixed projection vectors: `2b6857aab1b8cc5e4f8f05a8b7ca57cafe0181d4`
- Workflow definition: `2a6d875c69006bcc37dcc65ce6954e3cd4f135db`

## 1. Independent implementations / 独立实现

The candidate run uses:
- Python `rfc8785==0.1.4` for RFC 8785 JCS;
- Python `cryptography==44.0.2` Ed25519 implementation;
- Node.js 22 package `canonicalize@2.1.0` for an independent JCS implementation;
- Node.js built-in `crypto` Ed25519 signing implementation.

The Python and Node implementations independently compute and compare exact P0 canonical UTF-8 bytes, payload/proof digest, final signed projection bytes, domain-separated signature preimage, raw public key and Base64url signature.

本次候选运行采用 Python `rfc8785==0.1.4` + `cryptography==44.0.2`，以及 Node.js 22 `canonicalize@2.1.0` + Node 内置 `crypto`。两套独立实现分别计算并逐字节比较 P0 Canonical UTF-8、Payload/Proof Digest、最终签名投影、域分离 Signature Preimage、公钥及 Base64url Signature。

## 2. Covered I projection families / 覆盖的 I 投影类型

The differential vector set covers five exact candidate object classes:
1. `OWNER_LOCAL_PENDING_GATE`;
2. `OWNER_LOCAL_GATE_RELEASE`;
3. `JF10_I_TERMINAL_DECISION_OBSERVED`;
4. `I_COMPLETE_EMPTY_PROOF`;
5. `I_OUT_OF_SCOPE_PROOF`.

Additional tests verify object-member order invariance, array-order sensitivity, no implicit Unicode normalization and rejection of non-finite numbers.

差分向量覆盖五类候选对象：I Pending Gate、I Gate Release、I JF10 Terminal Decision、I COMPLETE_EMPTY Proof、I OUT_OF_SCOPE Proof；另验证对象成员顺序、数组顺序、Unicode 不自动归一化及拒绝非有限数字。

## 3. Exact meaning and limitations / 证据边界

**This is a meaningful independent-implementation candidate pass, but it is not production trust acceptance.**

The deterministic private seed is test-only. The vectors exercise the pinned candidate projections and test profile; they do not prove:
- production I issuer/key registry, HSM/KMS custody or key-status distribution;
- historical key verification, compromise cut-off adjudication or external anti-rollback checkpoint;
- actual I PolicyDomain sequencer, durable nonce consumption or revocation-vs-commit race;
- live I ledger snapshots, COC quorum records or owner-local release CAS;
- Storage's verification at the actual final visibility linearization point;
- a production runtime's exact serialized records beyond the five pinned test projections.

该结果是有价值的独立实现候选通过，但不是生产 Trust Acceptance。测试私钥不可用于生产。测试不证明生产 Issuer/Key Registry、HSM/KMS、历史验签、泄露裁定、外部 Anti-rollback、真实 PolicyDomain Sequencer/Nonce Consumption/Revocation Race、Live Ledger/COC/Owner CAS 或 Storage 最终 Visibility Boundary。

## 4. Disposition / 结论

**I/H CRYPTOGRAPHIC BYTE-LEVEL CANDIDATE VECTORS: PASS FOR THE FIVE PINNED PROJECTIONS.**

**PRODUCTION CRYPTOGRAPHIC PROFILE: NOT APPROVED.**

This result satisfies the first two-implementation byte-equality milestone for the five named projection classes. H and I must still close exact schema-to-P0 extraction tests, signature-reference allocation, key lifecycle/operational trust and live authority verification before freeze.

**五类固定 Projection 的 I/H 密码学字节级候选向量通过；生产密码学配置仍未批准。** 下一步仍须闭合 Schema→P0 自动提取、Signature Ref 分配、Key Lifecycle/Trust 运营及真实 Authority 验证。
