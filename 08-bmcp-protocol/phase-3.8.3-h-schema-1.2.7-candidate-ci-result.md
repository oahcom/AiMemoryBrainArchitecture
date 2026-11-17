# Phase 3.8.3 — H Schema 1.2.7 Candidate CI Result
# Phase 3.8.3 — H Schema 1.2.7 候选 CI 结果

- Owner: H — BMCP Protocol
- Workflow: H Recovery Cutoff Conformance
- Run: [44042401245](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44042401245)
- Job: `semantic-and-wire-tests`, job ID `133899868784`
- Checked-out commit: `a39c87a62b5cbe911c096b010146685d779eecae`
- Result: **95 tests PASS / 0 failures / 0 skipped**
- Exact schema 1.2.7 Blob: `e9748a5b904d2b975e47a32a0cbb31de31636854`
- Exact schema test Blob: `fa4fc9f7d3bf64a90bc992453b13fc1fb3c11879`
- Exact H mapping Blob reviewed separately: `77d0bb31196c722cb2cdda8c2ff55d8ade201db5`
- Exact I review of H mapping: `64ed7495cd0b44248f240ba83d67951a6a3d43db`

## 1. What passed / 通过范围

The run executed the checked-in H semantic, JoinProof, two-phase recovery, wire and schema candidate tests. It includes the new assertions that:
- the schema artifact is revision 1.2.7;
- the on-wire family version remains 1.2.0;
- `signature_profile_id` is an explicit common-envelope property;
- the field remains structurally optional for compatibility;
- SHA-256 remains the schema digest algorithm.

The same run also includes the existing Python/Node fixed UTF-8 and digest differential vector.

本次运行执行了已提交的 H Semantic、JoinProof、Two-phase Recovery、Wire 与 Schema 候选测试，并包含 Schema 1.2.7 / Wire 1.2.0 版本区分、`signature_profile_id` 字段存在且结构可选、SHA-256 算法声明，以及既有 Python/Node 固定 UTF-8 与 Digest 差分向量。

## 2. What this PASS does not prove / 不证明事项

This 95/95 result does **not** execute or prove:
- RFC 8785 JCS conformance for the I P0 projections;
- Ed25519 signing/verification against the I profile;
- exact per-message P0 allowlists against real serialized I records;
- I key-status, issuer/audience/purpose trust, historical verification or anti-rollback;
- independent Python/Node Ed25519/JCS implementations for all I message families;
- real I PolicyDomain nonce consumption or revocation-vs-commit ordering;
- Storage verification at the actual visibility linearization point.

The existing Python/Node differential test is limited to its fixed UTF-8/digest fixture; it is not the two-independent-implementation proof required by I-H-CRYPTO-04.

95/95 仅证明当前候选测试套件通过，不证明 I P0 Projection 的 RFC 8785 JCS、Ed25519、真实 I Key Status/Trust/Anti-rollback、PolicyDomain Sequencer 或 Storage 最终 Visibility Boundary。既有 Python/Node 差分测试仅覆盖固定 UTF-8/Digest 夹具，不满足 I-H-CRYPTO-04 要求的完整双实现密码学互操作证明。

## 3. H disposition / H 结论

**STRUCTURAL SCHEMA CANDIDATE PASS. CRYPTOGRAPHIC PROFILE CONFORMANCE OPEN.**

The run is a useful schema/candidate regression result. It does not close H-FR-04/H-FR-06, I-FR-01, I-RJ-05, FR-P0-01 or TAB-001.

**结构 Schema 候选测试通过；密码学配置一致性仍 OPEN。** 本结果不关闭 H-FR-04/H-FR-06、I-FR-01、I-RJ-05、FR-P0-01 或 TAB-001。
