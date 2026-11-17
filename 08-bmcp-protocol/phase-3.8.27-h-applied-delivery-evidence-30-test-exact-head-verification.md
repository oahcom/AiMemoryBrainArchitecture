# Phase 3.8.27 — H Applied Delivery Evidence 1.0.0 Exact-Head Sync and 30-Test Verification
# Phase 3.8.27 — H Applied Delivery Evidence 1.0.0 精确 Head 同步与 30 项测试验证

- Date: 2026-11-18
- Owner branch: `session-h-bmcp-protocol`
- Exact branch Head: `4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`
- Related issue: #3
- Parent: H Phase 3.8.24 / 3.8.25 / 3.8.26

## 1. Exact source pins

The H owner branch was updated with the exact current-main resolver-reference equality fix and the corresponding negative test. The branch retains the separate Applied Delivery Evidence 1.0.0 family; Unified 1.2.15 remains unchanged.

| Artifact | Exact Blob |
|---|---|
| Applied Delivery Evidence 1.0.0 schema | `2ce8776ca5ee5e014b234dc3eb34a7cb7961e608` |
| Reference validator | `43f402e4a09034da197ac24856cddbd496c9c75f` |
| Conformance tests | `98242cc193a77b27d58b39353ccc031201992614` |
| H workflow | `c029a0b1beb6f24916163169873b856fb16d5214` |
| CSubmitOutcome join addendum | `9ff4ac5b64b354f63add21a5d16d37da46835c07` |

## 2. Exact-head CI

GitHub Actions run [#44187702465](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/44187702465) was triggered by push and checked out exact Head `4c16410f8b20b8fc2bc8c7609eb7bf07d83f317e`.

- Workflow: H Applied Delivery Evidence Conformance
- Job: `applied-delivery-evidence` — SUCCESS
- Test step: `Run Applied Delivery Evidence schema and semantic conformance tests` — SUCCESS
- Decoded job log: `Ran 30 tests ... OK`
- Negative test `test_27_resolver_record_ref_must_equal_h_c_submit_outcome_ref` executed successfully.

This is a verified 30/30 pass for the H Python reference/conformance candidate on the exact H Owner branch Head.

## 3. Correctness effect

Before this sync, H's resolver callback could return a different valid CSubmitOutcome record than the opaque `c_submit_outcome_ref` named in the H envelope. The validator now requires the resolver-returned C `record_ref` to equal the exact requested reference; mismatch is INVALID before H accepts the observation.

This prevents a resolver substitution from silently binding H evidence to another valid C record. The existing exact equality checks for record sequence, payload digest, final request boundary and optional ActualInferenceRequestId remain in force.

## 4. Strict scope and remaining blockers

The 30/30 result proves only the bounded Python reference/conformance suite. It does not prove:
- a live authenticated C Owner Ledger resolver or C signature/trust-root verification;
- production JCS/canonicalization, Ed25519/HSM/KMS key lifecycle or external anti-rollback;
- durable H replay/observation storage, crash recovery or deployed Adapter/Runtime integration;
- real I PermissionEpoch and D ForgetFence ledger adapters;
- G durable Applied persistence/restore, multi-replica idempotency or end-to-end Full Applied;
- independent human C/H/G Owner acceptance.

**Disposition:** H candidate reference suite — **PASS (30/30, exact Head)**. H production service — **NOT VERIFIED**. Cross-owner wire freeze — **NO**. Production activation — **NOT AUTHORIZED**.
