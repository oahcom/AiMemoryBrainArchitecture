---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: {scheme: git, value: null}
      approval_scope: {type: Full-document, included_sections: [], included_assets: []}
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: ["AID-2026-082", "PR #1220", "delegated Owner authorization"]
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Source trees and blob pins enumerated; full body/frontmatter and semantic mirror review incomplete."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Candidate
    canonical_scope: "E/F/H/I source enumeration evidence"
    canonical_scope_id: "ai-development/source-restore-03"
    canonical_scope_keywords: [source-blob-pin, bilingual-mirror, owner-review]
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-cross-owner-source-restore-03.md"
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-cross-owner-source-restore-03.md"
---

# AID-2026-082 — E/F/H/I source inventory

- Carrier: PR #1220; branch `impl/2026-11-26-normative-source-restore`
- Inventory baseline Head: `7cf6b0adcd531c875e14bab0b6fa70ff75db08eb`
- Total enumerated Markdown files: **240** (tests excluded)
- Restored source files in this inventory commit: **0**
- Full body/frontmatter readback: **8 primary documents inspected; remaining listed bodies not yet read**
- Bilingual semantic parity: **NOT VERIFIED**
- All source documents remain Candidate/Informative or BLOCKED; none promoted.

## Source branches

| Owner | Branch | Source HEAD | Markdown count |
|---|---|---|---:|
| E | `session-e-memory-compiler-2026-11-16` | `ee098e14747d9915de5b3efb63b3a8dd77f670ed` | 25 |
| F | `session-f-memory-runtime` | `1908ce4d233b20f7cafd00cb679affd01bd15174` | 15 |
| H | `session-h-bmcp-protocol` | `3e8b33df18b9e6fc757ca84ff07a12faebc78e74` | 111 |
| I | `session-i-security-governance-2026-11-16` | `8abddf814467b271344a9814613a6b7ca6a446c6` | 89 |

## Per-file inventory

Mirror columns mean path exists in current main tree, not that content is semantically aligned with the pinned source.

| Owner | Source path | Source Blob | Root on main | EN path on main | ZH-CN path on main | Disposition |
|---|---|---|---|---|---|---|
| E | `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` | `5ca77a5b48e69afb3bc81429baf538be7dce4d46` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/compiler-overview.md` | `35a766fae29c0b8ddf692a6ec062762f0fca29d2` | yes | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/compiler-state-and-producer-admission.md` | `e59f517fff161ab882aa0ddc4a5bda513964ae1a` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/consolidation-and-conflict-resolution.md` | `d16f8e2e41a6cca81ad285e5f79f075d87e64edb` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/decision-change-log.md` | `a5a13c33c2096fc60086e18cd4f9bef59b0b2739` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/event-ingestion-engine.md` | `9fa3db53175452bf9e6f0fce8b1540765e46905f` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/evidence-and-provenance.md` | `38bcacafa89ebe7b3eedb6f38d174e0c6a1f3963` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/extraction-and-normalization.md` | `c18780403de2d1dbcf471bdb8abdaa009a4a78e1` | yes | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| E | `04-memory-compiler/forget-fence-and-derived-registration.md` | `00e37ba56596e710513c8d0568acd79141d9101b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/module-baseline-and-redlines.md` | `7f037a7684723fdbddd593b3d131c7c348e2ccbe` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6-bih-identity-consumer-acceptance.md` | `6f4100618695fcf971560fb784f7887a72798c96` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6-joint-producer-publication-decision.md` | `aaa15de9d6e3a6ce74b11fda376369d6a49659ab` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6-producer-publication-conformance.md` | `a17f065e69e809fceacb51873d6a36a8b0f5c235` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.1-joint-defect-closure-e-addendum.md` | `004bd48661a7657b88911ec40de79bde8fe35aa6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.2-e-jf10-coc-bridge-producer-acceptance.md` | `4503628cf6f6ea46696ab14e7decd3e408ced19a` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.2-jf10-cross-authority-recovery-protocol.md` | `94679897e84a6f58fd8b9467b5249e1a885cb0b0` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.2-jf10-reference-model-consumption.md` | `20770a84daea00ba9f38cc9a5bc43f153f09c3a7` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.3-e-coc-durable-protocol-acceptance.md` | `b9dd9af8c770a40b44849d02caac306e0a701100` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.4-e-prepared-participant-gid-producer-acceptance.md` | `057c1c2096e97798e60e07710f301ae7cc522bbc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.6.5-e-restore-reconciliation-consumer-acceptance.md` | `051a65c1c140f133ad06a73c649b27b1888e83ca` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.7-e-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `4fb9e58511941f59b4d777336f8f85ad88ecccf1` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.8-e-publication-orchestration-retry-recovery-contract.md` | `475fee41e5eea527af4edefbfe88c58c86967d0a` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.8.2-e-recovery-join-orchestration-exact-review.md` | `5479db78adfcc67d3c33e0bd9e2d8f9a0a734960` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.8.5-e-storage-logical-serialization-topology-review.md` | `14efd3d32930bec9740bfb4509e18ff6bf670090` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| E | `04-memory-compiler/phase-3.8.6-e-review-storage-serialization-anchor.md` | `19d708bc29b6115d7bccb7d320781f452ee28b78` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/activation-policy-engine.md` | `b7f5d85468f5262e472769a1991b812ac4a64f5b` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| F | `05-memory-runtime/module-baseline-and-redlines.md` | `d4756cabda3151999cbe1ddde0adb554458004a1` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.5-forget-suppression-and-cursor-consumption.md` | `99f950f9fabe97969b5ad580c9c80e52930a1423` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.5-reprocessing-change-log.md` | `69df00d94cd66789c84ad91d4948a26666965922` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.6-anti-resurrection-reference-model-evidence.md` | `15049d448ace5ad24a6c02eba3fc906fcac149f6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.6-runtime-forget-suppression-and-invalidation.md` | `ce59252dbbdc5d10d016704797e9ba12d5a941bd` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.6.4-f-prepared-participant-gid-index-boundary-acceptance.md` | `67e77f783a275727eb444cefca280a27a0f095ef` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.6.5-f-restore-reconciliation-consumer-acceptance.md` | `d630933a2aa70b9bc182fdeab47856dd8bbec386` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.7-f-local-lifecycle-producer-derivative-queue-recall-context-restore.md` | `29e9504c75d737c2dd200ebc3306eda555f0b0ac` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.8.5-f-storage-logical-serialization-topology-impact-review.md` | `9dae404993d3006e59d2dae88a0a97a3c0998d58` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/phase-3.8.6-f-review-storage-serialization-anchor.md` | `122238146830db6188f00a9788e018a82bfb3f90` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| F | `05-memory-runtime/retrieval-engine.md` | `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| F | `05-memory-runtime/runtime-overview.md` | `b7a948f014c3ad882a35a18bfc8ce025b26ab85a` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| F | `05-memory-runtime/runtime-scheduling.md` | `ca35d8cddd012c1ff067328ee22177f57c40ae36` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| F | `05-memory-runtime/working-set-and-cache.md` | `a934491950c876701e8ac592a0e6aaea983b44e3` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| H | `08-bmcp-protocol/adapter-capability-and-applied-attestation.md` | `74be8374a67da385a5f0f8e34c7aef2b38b72bcf` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| H | `08-bmcp-protocol/adapter-forget-ack-and-target-binding.md` | `5e2b33898cbc6a9c95e271ecd1d8a092d04c67f8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/context-delivery-and-acknowledgement.md` | `bf9732cc39d156853b507c3a3a4e573159978f49` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/forget-revocation-and-reconnect.md` | `695909360782987781e259187041618f495f1c8c` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/message-envelope-and-versioning.md` | `5547ecd78d118bd63e571e5daad87194d9b694e4` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3-5-identity-applied-ack-reconnect-contract.md` | `ceefd59fdf587fb7b4c01c7e5f9c5d6239d5b7bc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3-forget-ack-remediation-change-log.md` | `d118dfc825067e7f9cd038eb6e8af4effa68f0e3` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-a-package-exact-version-h-owner-acceptance.md` | `fe437a3d44790f249f613d1e6cafc0db40d45b10` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` | `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-bih-identity-trust-consumer-acceptance.md` | `21d799fbecc20eea02dc9f05863688e38165f04b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-bih-joint-architecture-acceptance-addendum.md` | `eb8f4108491c8aa78bcf1ea33f0c85a596bb40c8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-cgh-applied-contract-exact-version-h-owner-decision.md` | `c0e10966e8dd95a9d1f5b1dfa156cb4b098b26e0` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-h36-live-closure-addendum.md` | `e94d39b9977fca61af50bb697f29116d707b3439` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md` | `8afb914731a34d8ab44331f54f1f39bfd8ec37ce` | no | yes | yes | BLOCKED_BODY_FRONTMATTER_PARITY_READBACK |
| H | `08-bmcp-protocol/phase-3.6-jf10-bridge-schema-validation-evidence.md` | `318c433d5b96966ecd47e6d1b265a0b12b28e581` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-jf10-strict-parser-reference-evidence.md` | `d974ee1b166af4a94ab8ad7601744f40f32f98c6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6-six-dimension-self-review.md` | `9ef2d557cd872a11c96e8888004d4f7389d2081c` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.10-h-exact-version-semantic-validator-decision.md` | `1de7d30f3ca81bc579b396acb0f05e2ead5fe9dd` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.10-h-recovery-cutoff-semantic-validator-contract.md` | `4c5c3771575979061e674e40f1f5f3d9b4645bd9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.11-h-exact-version-r1-r4-bundle-rereview-decision.md` | `bf7964267e77ad024009026ee6a332fe2baa48bb` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.11-h-two-phase-recovery-batch-manifest-wire-validator-addendum.md` | `c216853412f654d92e2890ddcc2dffc12406cbe6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.12-h-exact-version-recovery-schema-review.md` | `86ee608007a4f9432eda8143e2a830afd3eece0c` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.14-h-cross-review-i-d-c-wire-adoption-amendments.md` | `712f7e5501b2f5a82aa1b9104d0bc1d525085cf5` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.14-h-exact-review-storage-v3.2.4-successor-manifest.md` | `e40a8fb32a71f4a3fc880c33cef9fa67298013f8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.15-h-provider-outcome-1.2.12-validator-pin-and-ci-evidence.md` | `383a89c474a32ae8eadc0571afeb09bc0c9ceacc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.3-h-coc-durable-protocol-wire-acceptance.md` | `5dfc7ae56b2ae7351d6c2c108f7be3249125f6c3` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.4-h-prepared-participant-identity-wire-acceptance.md` | `98321da4b93d39ada9d227f4e03f2e55ba45aa29` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.4-jf10-prepared-gid-schema-validation-evidence.md` | `d7652727e21c2f88d6cc2481deeeca96c2efd38f` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.5-h-restore-proof-transport-boundary-acceptance.md` | `5a4b9a768d7396eb4be58d0d1ed3c6c0021955ea` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.8-h-unified-coc-jf10-provider-outcome-schema-review.md` | `2a794d1bc544b9a7e82e1dbbc2fb859245d520b3` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.8.1-h-unified-coc-jf10-provider-outcome-schema-rereview.md` | `1079350927991032ca13e6af1ec3f84f1eabbc2b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.8.2-h-unified-coc-jf10-provider-outcome-schema-v1.2.3-rereview.md` | `36ed239019e34eaafff9e22b127a58e8e2557842` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.8.3-h-unified-coc-jf10-provider-outcome-schema-v1.2.4-decision.md` | `3aa617cd7066405d84a5bd027eaaad1f9c3bc9bc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.9-h-r1-r2-exact-version-delegated-disposition.md` | `3595221167cde69eaabf95fe7926440c4ca92822` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.6.9-h-recovery-cutoff-wire-contract.md` | `b4cae9c0c9121c27ea2933c029b83b3f4367672b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.7-h-lifecycle-handoff-envelope-semantics-not-frozen.md` | `b2a2648d5576511f68fdb9d87ce4388a1fedd5e9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.10-h-c-provider-outcome-unified-1.2.14-exact-mapping.md` | `579dd2a91edf47b86e744e897ba6668b839944bd` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.10-h-ci-and-c-owner-acceptance-closure.md` | `1dda43ef48787fc635be177e825d1b766178d962` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.10-h-exact-review-i-v1-crypto-p0-unified-1.2.13-recoveryjoin-1.0.2.md` | `0b6eeadb1cfac415e77ec1358b9fdf99fde11d41` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.10-h-review-i-p0-unified-1.2.14-recoveryjoin-1.0.2.md` | `68b2222419663674c6fcf4572377150e284a6dc0` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.10-h-unified-1.2.14-c-submit-outcome-1.0.1-authority-join-mapping.md` | `1cbe74eba69325510d6b1019d971661f965eabf8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.11-h-exact-mapping-unified-1.2.14-c-submit-outcome-1.0.1.md` | `c196fdc7a9d88e344d37ba2810a9bce1803f8b96` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.11-h-review-cdi-membership-p0-crosswalks.md` | `66a9cd8b43ec6185484e565da21df90d9a68042d` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.12-h-exact-ci-and-c-owner-acceptance-closure-1.2.14.md` | `d9c09f0eab9d0ca23e01627e2bd399363d20e2cd` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.12-h-exact-cross-review-cdi-membership-p0-1.2.14.md` | `90cdadd7d80676c1338965576c955a5f336ad0bc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.12-h-review-storage-serialization-anchor.md` | `c6ca09e9dd7b108f6dc2eff4d82e38e73c18d83f` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.13-h-exact-review-d-recoveryjoin-1.0.2-highwater.md` | `6d45398885a842b0e5effc860bc97d7ecd3a8435` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.13-h-provider-outcome-current-head-ci-and-authority-seam-closure.md` | `9083ad54581352c83be21ac981aea845cd307382` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.14-h-exact-review-i-p0-unified-1.2.14-recoveryjoin-1.0.2.md` | `7acafcdc38079cdc51965f7b416d547372083965` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.14-h-full-path-fixture-and-exact-head-ci-closure.md` | `cda025fb157815570b3280fa5ff168d5e62453b1` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.14-h-full-provider-outcome-local-validation-ci-evidence.md` | `b8bbac49ac99573911fe89f30f12325bbaa67b08` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.15-h-expanded-full-path-mutation-matrix-and-ci-closure.md` | `60e5eb98a07efcf87bc3f2be6fcf7fedb2196504` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.16-h-c-p0-mutation-nullable-coc-and-exact-ci-closure.md` | `431d049184ae4622e1dcac3f71176ab1cfc9aa8b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.16-h-exact-head-c-p0-projection-regression-ci-closure.md` | `f8aeae206b71f6a6bccd1c41300d40959a5221a8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.16-h-expanded-full-path-39-test-exact-head-closure.md` | `927fe9e8dafd5def6a5cb825e5968f5835d3c6bf` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.17-h-expanded-c-p0-nullable-intent-42-test-closure.md` | `82f06005e49505c7b33e72e65387dcd9f991dc01` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.18-h-outer-envelope-authentication-gap-and-owner-decision-contract.md` | `fbb7553b0bd0c7a9714304983882ca2cc1fa9cc1` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.19-h-outer-envelope-authenticated-ingress-reference-gate-and-60-test-closure.md` | `860c896a388597a4378eda5aa323f276390acf34` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.19-h-review-c-outer-envelope-signer-p0-wire-mapping-contract.md` | `2a3a995396ee7a56d8fbbb03ec53b5d1d15e1f82` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.20-h-exact-c-envelope-p0-correction-and-json-pointer-mapping.md` | `4ba7e1699215d02224f805a15484b1da2e40c03f` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.20-h-explicit-outer-signature-profile-requirement-63-test-closure.md` | `73543e8e7963f1442931c318542a4249d1c41790` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.20-h-gateway-attestation-p0-contract-candidate.md` | `93b83ac35114d20d64579d919c0699886940f0fa` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.21-h-candidate-outer-envelope-p0-allowlist-and-signer-role-matrix.md` | `e2eaa3efed8d0f3af79de550c850a21ef47cd72d` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.21-h-exact-schema-mapping-unified-1.2.15-gateway-attestation.md` | `2dc30f193d9c4f4bdc05ca4c137103687db28924` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.21-h-outer-envelope-p0-digest-reference-implementation.md` | `9b0e9fb5ad2ca49c121052763bd189d82547b413` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.23-h-exact-review-g-applied-delivery-evidence-mapping.md` | `be308261c3e000e712a3cdbd3dbf60507156127b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.23-h-exact-review-g-applied-delivery-evidence-mapping.zh-CN.md` | `641abd9b5a4ed271c3c4b561747c99d7cde79463` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.24-h-applied-delivery-evidence-1.0.0-schema-validator-candidate.md` | `f193113f142506b0d0848c7131f780db93a83aef` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.24-h-applied-delivery-evidence-1.0.0-schema-validator-candidate.zh-CN.md` | `2c612ff11f9e3da784eeb5a9033aceb5bf01b55f` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md` | `4c220e998fc6ba700157598b0384dc3134cf8575` | yes | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md` | `9ff4ac5b64b354f63add21a5d16d37da46835c07` | yes | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.27-h-applied-delivery-evidence-30-test-exact-head-verification.md` | `f2e4e850b3f82076aea8a91de000644bb91e8170` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.27-h-applied-delivery-evidence-30-test-exact-head-verification.zh-CN.md` | `c730bbd16b73e69263cfd414dd5dad3d14c6faaf` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.3-h-i-crypto-profile-wire-mapping.md` | `b132e6a01bcfe13f92020b9778ee3f7ddbf65753` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.3-h-independent-jcs-ed25519-candidate-conformance-result.md` | `02c488bf31f02208a8d6b3d394af13359c3799f9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.3-h-schema-1.2.7-candidate-ci-result.md` | `c7eb6d0af3fecc6583c71c4f237bfa93decdd054` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.3-h-schema-1.2.8-recovery-join-1.0.1-ci-result.md` | `3973156204d98c787589ffcaf744f17f467a0d48` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.30-h-recovery-join-288-test-exact-head-verification.md` | `2601c3051a0ab8544a421c117b72389fad8489d9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.30-h-recovery-join-288-test-exact-head-verification.zh-CN.md` | `e6539716b85b90f3236544c953e5b9b4f467f169` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.31-h-unified-1.2.15-structural-conformance.md` | `f7e548562f2c9c75822bf5467e2a9603ce784d42` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.31-h-unified-1.2.15-structural-conformance.zh-CN.md` | `5f8505b093a240b4953d82e869a3a7ffa2721b69` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.32-h-unified-1.2.16-owner-snapshot-completeness.md` | `cc40b50d99e329eafa6851049ad0e2cdbba5e955` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.32-h-unified-1.2.16-owner-snapshot-completeness.zh-CN.md` | `e312b47011a59876a77c89435ed3d8c2df61dbde` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.33-h-unified-1.2.17-owner-gate-release-completeness.md` | `4f39320c256cb994d768061f9644bf36aef3d5c9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.33-h-unified-1.2.17-owner-gate-release-completeness.zh-CN.md` | `e9263ffd47c4c3e2265405a6d5d799fe13e6db1a` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.33-h-unified-1.2.17-owner-gate-release-semantic-reference.md` | `fe4b8eea4df4b0cc392da64c08141157ba19693f` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.33-h-unified-1.2.17-owner-gate-release-semantic-reference.zh-CN.md` | `8e1ad25ee73ea6aca0e8d3cbf17acb31e6fe7248` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.34-h-owner-gate-release-semantic-reference.md` | `b27dbfe57a7b3a3312d3d8576a74b81e72ac86f7` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.34-h-owner-gate-release-semantic-reference.zh-CN.md` | `01109ba2a87c730c7c415b113d46401dbc25e1ee` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.34-h-unified-1.2.17-consumer-entry-scope.md` | `66a6dfa627ff6a6c382aca84258de347b0048ab5` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.35-h-owner-decision-f43-01-f3-d-1.3.1-mapping.md` | `004fc0261b447771e73a0f8cfdd34ec1f8b33e49` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.36-h-owner-decision-f43-07-stage-3-consumer-mapping.md` | `19e3dce92aa6d843d3d8d63b21f843eb30770b0f` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.4-h-c-provider-outcome-schema-exact-review.md` | `49583f71c3f2ac7d83c030792da1af8ac81edcc1` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.4-h-i-crypto-profile-wire-mapping.md` | `1a64a7be3ec4190643809897519afdf73ed69c1d` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.4-h-schema-1.2.11-provider-outcome-cross-review.md` | `aae5dcb1d0c1ad95c306e469e6fbd96aef67b309` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.4-h-unified-manifest-union-contract.md` | `e0f561df814c1539ee3b1e72ce7cfc2fd15dd175` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.5-h-owner-authority-membership-verifier-adapter-contract.md` | `5b462c79082a27b64a03f9c8b6da1d4e93075b89` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.5-h-schema-1.2.11-provider-outcome-semantic-validator-contract.md` | `62b740696b4a5335f19f82e83fe4d4ce8b4e0f4e` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.5-h-storage-logical-serialization-topology-review.md` | `b71e818379117514c4492138780fc80a9b2deba0` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.6-h-c-provider-outcome-crypto-profile-exact-review.md` | `c659485549da23927d5a190f6b16fc30086aa302` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.6-h-r1-r2-owner-gate-wire-crosswalk.md` | `8b5b2c37201f7ae821bb5ca71a5101f19e75cf5c` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.6-h-schema-1.2.11-c-provider-outcome-wire-mapping-and-vector-matrix.md` | `bd7dce6bf840af0ee7e4745d61c983818f6232c2` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.7-h-c-provider-outcome-unified-1.2.12-exact-mapping-amendment.md` | `c9a56ed1eaca6624daad68ff150744bd3be98092` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.7-h-i-p0-and-owner-snapshot-attestation-review.md` | `b03a99943b374103bae3e599c68cb2cd97a561ca` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.7-h-schema-1.2.12-c-provider-outcome-1.0.1-exact-mapping.md` | `fad28f1b62f6a686669e209ebe30d69df6330d75` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.8-h-c-provider-outcome-unified-1.2.13-exact-mapping.md` | `c4fd029d3f1258e3d5e0f56146ccc61eb8e90cdc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.8-h-i-v1-crypto-profile-architecture-review.md` | `fe435d5a4cc39df76f2cbfd00e270962218cc051` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.9-h-exact-mapping-unified-1.2.13-c-submit-outcome-1.0.1.md` | `32bf9b0fd42abe8b58749b858b1d5c9aef39c5fd` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/phase-3.8.9-h-review-i-p0-unified-1.2.13-recoveryjoin-1.0.2.md` | `c16063197766a495feb98776c7516ebcbe4b7441` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/protocol-conformance-matrix.md` | `075b2ac6ebe9bda4ec83de04fad07e8027e6a440` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| H | `08-bmcp-protocol/protocol-overview.md` | `b88ef3a6fd3be293e7c2e77d9652f386b169bc47` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/audit-and-exception-governance.md` | `0b5237f490066c7f95ebf4f5a5aa81edd8480bd4` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/forget-retention-backup-and-erasure-policy.md` | `f14cb2149ca3f817229533005ab89dbdc7f0b3a8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/global-forget-target-inventory-and-completion-evidence.md` | `9100061fa986fb6676656169de3fcf9fc1c72664` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/governance-decision-register.md` | `f5fd2558c657f4ef49396a7a00cdbcd0f226f853` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3-global-forget-remediation-report.md` | `6bc45a0aed5b5cb019149e4564d1eeb73e7c2512` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.5-global-identity-forget-governance.md` | `a8632931396125019d1afccff39ea266f52a4d3a` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-bih-joint-architecture-acceptance-addendum.md` | `475044ed4c6d468be26459e6201018dd57b3fc80` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-cgh-applied-1.0-i-authority-confirmation.md` | `8004b0f21e523b203ae36870fe88a25f977e70fa` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-cgh-applied-1.0-i-owner-authoritative-confirmation.md` | `9b09a31b786c0d49669bffb2c8cca332308c7098` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-governance-acceptance-execution-addendum.md` | `1f5d2e4aba7afa75c0696f3c8f025b0cb903e0ad` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-governance-approval-and-consumer-acceptance-register.md` | `22621fd6a9b26995b55288fee7e205f3a1ae7df5` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | `5a5304d48aa912dcf6f817099bd5659371d8cdc8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | `0cbf6bb7480db873790c454817593a9b1c5548ba` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md` | `bae6a24fe3a374bc816993979a8fa9af52517dea` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | `17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-r1-r2-i-owner-gate-linearization-decision-candidate.md` | `57ef6c4352d79577ae53a77895f73bce434c5fca` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6-six-dimension-self-review.md` | `6d1bb5c596902e8a02756e12f451fdd8b0958787` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.10-i-exact-version-recovery-cutoff-review.md` | `a0fee9ef41c52ea3948286e6ec9a348cc1b17168` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.14-i-exact-review-storage-v3.2.4-successor-manifest.md` | `58615abc9bc1d1ab2a71b2651fef12296bfcf92e` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.2-i-coc-jf10-composition-boundary.md` | `9e1f66ddbe0952f17068b1638feb8ab0094588c3` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.2-jf10-commit-authorization-recovery-acceptance.md` | `77ffa8f019ea7734e22d785953e54f65c05208ac` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.2-jf10-owner-gate-ordering-correction.md` | `57474cfb0c5da07a2cbcbeff1fc792ced36c5dd6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md` | `8069ff86988396442c8d9dc3fd58653683abe2f3` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.3-i-coc-durable-protocol-authority-acceptance.md` | `528945f82e3e25258052240a7a4ba43753ae6cf8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.4-global-forget-evidence-reconciliation.md` | `0289c5d79942358cbaf8d9686a25834773bfb944` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.4-global-forget-reference-model-evidence.md` | `206e65689d17c0fb1f57bc20aea72c6e7fd4752a` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.4-i-prepared-participant-gid-authorization-acceptance.md` | `20fc13bbfe7b93c0d6f6233fd714c57dadca1fda` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.5-i-restore-control-highwater-acceptance.md` | `85d62b8858fc86addacd3b83f49476e42f49b785` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.5-i36-governance-decision-proposal.md` | `33cc37eb19c1ce1e1125b7db68ad6c41f3200abf` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.6-i-global-inventory-authority-addendum.md` | `d7e34400738b7269929f48d125711ccf045b410b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.7-i-exact-version-owner-decision.md` | `325cd63164c217f8712964da58509f867d105740` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.7-i-owner-local-gate-admission-release-amendment.md` | `0d0b4fb0f5921e63b6ebfd70b62afa31d3d5fdf7` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.8-i-exact-version-owner-rereview-decision.md` | `0b9954d137a966c062a32424c69936a78ecc470c` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.8-i-exact-version-r1-r4-rereview-decision.md` | `f865ec592491cb251f35c07b562a2ca57db9bad8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md` | `cf4b76f151204fa47b156b5d807e7378c28fd268` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.6.9-i-r1-r2-exact-version-delegated-disposition.md` | `6bf56407721f1271f315d799f9bd57055393c176` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | `e3b1b5d99eb36ac0b395854d8c19287d2b64b752` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | `54bab0484bd232a5a258e65e34cc7425288b39a6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | `44986f5f864bcdc1a79d34978273644d381a68c0` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.10-i-scope-clarification-c-profile-identifier.md` | `1e86a1349d371a1cdb4a56d69f783e0f316c7203` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.11-i-exact-review-unified-1.2.13-recoveryjoin-1.0.2-p0.md` | `367a6002327134840b1d03d426bb4bcd864db4c9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.11-i-review-storage-serialization-anchor.md` | `f22d31dec3a95f094c2942ab816c830f007e830e` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.12-i-exact-compatibility-h-unified-1.2.14-recoveryjoin-1.0.2.md` | `c400b66639b810a9437c1b52993a2015473622d6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.12-i-exact-review-h-unified-1.2.14-current-schema-p0.md` | `fbd44d57bdb4fc15c4c254fcd9d8ac4c58d365fc` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.13-i-exact-review-h-authority-join-mapping-1.2.14.md` | `34b29f405d4e8ceb1a039666bfe84518f62355f8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.13-i-review-h-1.2.14-authority-callback-contract.md` | `04f80c9ca56621961bebb17b4e772ec9b0d15365` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.13-i-review-h-terminal-authority-verifier-seam.md` | `6bad2dcd7ac27598d3fd21c6f12c3c97888d3d95` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.14-i-final-compatibility-h-1.2.14-callback-and-recoveryjoin.md` | `a1c8c3cdedfb5ba6258e4db025b294d989a834e4` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.14-i-review-h-full-path-terminal-callback-boundary.md` | `eb35989ccba4d1039ce7e6e87d04f2f026e51b5b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.15-i-exact-review-h-expanded-full-path-commit-won-callback.md` | `44898fa686efc00d4b05aa0454755907d25fa3de` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.15-i-review-h-expanded-full-path-terminal-and-envelope-auth-boundary.md` | `df869ef90e6279602b4d46128a81b2dc6ba01d71` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.16-i-exact-rereview-h-c-p0-projection-test-39-method-ci.md` | `653841c9e7b4a48f7137118a1388a7634bdcd566` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.16-i-exact-review-h-42-test-commit-won-and-absence-boundary.md` | `2851d31e4f8caf48348944b885b493c607ca79e1` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.16-i-review-h-c-p0-nullable-coc-and-envelope-auth-boundary.md` | `1171f82f3d5bac58a6d105bcc18de649b7398385` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.17-i-review-h-outer-envelope-authenticated-ingress-gate.md` | `893f24036fa9ccf8e438f3312cec8cb9c7cfeff9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.17-i-review-h-outer-envelope-authentication-trust-boundary.md` | `a50fa73aa9cb5949a29e2ca39b0f4284c4a5a31b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.18-i-exact-review-h-authenticated-ingress-envelope-trust-boundary.md` | `73145f83df234ebb9e55cc07f0a82b0db9416b68` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.18-i-review-c-outer-envelope-signer-p0-trust-registration.md` | `b6d1ea45825a1c2090abfba42474814f02f073a3` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.18-i-review-h-explicit-outer-signature-profile-requirement.md` | `7785f7a8ab242816fb36d42e91fdd34e65aae4fb` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.19-i-exact-review-c-outer-envelope-p0-correction.md` | `63d7bfc4ad08bd75e8c0a16c34b3c4ca95e76d00` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.19-i-review-c-separate-h-gateway-attestation-trust-model.md` | `ba6ec4a573c0dcd48906ed1a2db26da60841e957` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.2-i-recovery-join-trust-currentness-exact-review.md` | `a6682c3d5ff6653f066aab17950950615e60ac10` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.20-i-exact-review-h-gateway-attestation-p0-candidate.md` | `c6d2d6809e5a45987a405924e031444ae9a2cd8b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.21-i-exact-rereview-h-gateway-attestation-p0-digest-encoding.md` | `a16ab74f2cb5cfc67c04073bfa49dfb076383c91` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.22-i-exact-review-h-unified-1.2.15-gateway-attestation-schema.md` | `6ba4ce3a93f2adf6f8961d4927d9b87deb9696bf` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.23-i-rereview-h-gateway-attestation-replay-acceptance-order.md` | `85cdbad04ae4b688338cdf2b667c21d2f02d8b96` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.24-i-exact-review-h-applied-delivery-evidence-replay-authorization.md` | `57dbfa5397abe9dd628df0eaf2257a8554ec560b` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.3-i-cryptographic-trust-profile-proposal.md` | `5eeb011032c53c2f7897d699d6f512b26f07d0a2` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.3-i-exact-review-h-crypto-wire-mapping-r3.md` | `93afe9c9e06d20de5ce1c2a0f676b4785123fbcf` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.3-i-exact-review-h-crypto-wire-mapping.md` | `446109f4867268fe7dca3c7e114346f3c1a74b61` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.3-i-re-review-h-crypto-wire-mapping-r2.md` | `64ed7495cd0b44248f240ba83d67951a6a3d43db` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.4-i-c-provider-outcome-trust-boundary-review.md` | `4b59c7a63bdb48db648ae26ac0bdc9f667b9d144` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.4-i-crypto-profile-artifact-revision-amendment.md` | `35c47cc56c9d5e7ab72fdddb7ef9032aa3661ff9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.4-i-exact-review-h-membership-proof-bundle.md` | `a9599742e80818be4053da382e750557b35dacef` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.4-i-exact-review-h-unified-manifest-1.2.11.md` | `7a9c447695fe34c0ac7bd941e805c3a2fe177d88` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.4-i-owner-snapshot-membership-proof-contract.md` | `0806a2be8e6a24d1a766ed58ccd7434a042d35e8` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.5-i-exact-review-h-unified-1.2.13-owner-proof-compatibility.md` | `5502e2d61cdab7b2833b55c16ef5dc4301988a57` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.5-i-recoveryjoin-1.0.2-unified-1.2.12-wire-adoption-amendment.md` | `b56b0c3690f1826f2fc965ec6af5d66a920004ae` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.5-i-storage-logical-serialization-topology-review.md` | `c63075aead9f0b18de9af4cf6fb0bc3c3a5a6d53` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.6-i-c-outcome-crypto-profile-trust-review.md` | `33704401bd80a8c95711d6240e5ce64028d5f356` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.7-i-exact-signed-object-p0-allowlists.md` | `739dc15e3cca33aef3f012f713b988e5528d4ad9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.7-i-h-owner-snapshot-attestation-schema-review.md` | `1520d3fc8c36c57f87b0a75ff7cb6c432649a8e9` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.8-i-crypto-profile-architecture-decision.md` | `56e956dca909af857469427378777705a5d1082a` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | `5c0e2049513d391dfc118f4f629a5ec95de456d6` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/phase-3.9-i-d-forget-lifecycle-terminalization-authorization-proposal.md` | `362307f6fff84cbe81fb71f37d6319e691db4f89` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/principal-actor-and-authorization-contract.md` | `03765efac4bb1153f303ce0030f9e277d602e81d` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/scope-and-revocation-policy.md` | `71df6aaf21bb1767cd9fe5c947581b871325e023` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/security-and-identity-overview.md` | `26a990e44709d8604ae515a2a63b510400fd8471` | no | no | no | BLOCKED_BILINGUAL_PAIR |
| I | `09-security-governance/threat-model-and-adversarial-test-plan.md` | `4227ac0e26228ca3504589efdee022b5d0802e12` | no | no | no | BLOCKED_BILINGUAL_PAIR |

## Inspected body/frontmatter excerpts

- E `04-memory-compiler/compiler-overview.md` Blob `35a766fae29c0b8ddf692a6ec062762f0fca29d2`: no source frontmatter; main already has a separately governed, newer root version. Do not overwrite with older branch copy.
- E `04-memory-compiler/accepted-receipt-and-idempotency-contract.md` Blob `5ca77a5b48e69afb3bc81429baf538be7dce4d46`: no source frontmatter in inspected excerpt.
- F `05-memory-runtime/runtime-overview.md` Blob `b7a948f014c3ad882a35a18bfc8ce025b26ab85a`: no source frontmatter in inspected excerpt.
- F `05-memory-runtime/retrieval-engine.md` Blob `1fbfc0ff07b66c0ff68c3cea5271261c9d7fc0af`: no source frontmatter in inspected excerpt.
- H `08-bmcp-protocol/message-envelope-and-versioning.md` Blob `5547ecd78d118bd63e571e5daad87194d9b694e4`: no source frontmatter in inspected excerpt; Principal/Actor/Permission fields remain ADR-blocked by I.
- H `08-bmcp-protocol/phase-3.6-authenticated-identity-protected-operation-binding.md` Blob `e7ca5ce4ece5d8fd77fe0760e49a85afa0133248`: no source frontmatter; governance and consumer acceptance OPEN.
- I `09-security-governance/security-and-identity-overview.md` Blob `26a990e44709d8604ae515a2a63b510400fd8471`: no source frontmatter; candidate policy, not approved production policy.
- I `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` Blob `17bbfcbe8f001c4ae1200cf1930ccc80059d7f9c`: CANDIDATE and GOVERNANCE-BLOCKED.
- I approval register Blob `22621fd6a9b26995b55288fee7e205f3a1ae7df5`: I36-GOV-01..10 remain GOVERNANCE-BLOCKED; approval evidence and effective version/time are None.

## Direction blockers and minimum release conditions

- **E (25 files):** most are absent from root on main. Per-file EN/ZH path state is above. Minimum: read every exact source blob body/frontmatter, reconcile source lineage against any existing main root, establish faithful EN/ZH mirrors and semantic parity, then obtain E Owner exact-version review. No overwrite of existing newer main root.
- **F (15 files):** all source paths are absent from main root. Minimum: exact body/frontmatter readback, bilingual pair creation/alignment, watermark coverage/scanned-through proof, and F Owner exact-version review.
- **H (112 files):** most paths absent from main; includes review/evidence documents, not all normative sources. Minimum: H authoritative core inventory, exact source readback, bilingual alignment, dependency-owner disposition and relevant ADR closure. No protocol freeze inferred.
- **I (89 files):** source paths absent from main root. Minimum: exact readback and bilingual alignment. I36-GOV-01..10 remain blocked until durable approvals name the approver, exact policy hash/version, authority, scope and effective time. This work cannot substitute for governance approval.
- Cross-owner source branches are not one coherent snapshot. Historical branch pins cited in I records differ from the live branch tips above.

No validator semantics or runtime/product code changed. No deployment, merge or Issue closure.
