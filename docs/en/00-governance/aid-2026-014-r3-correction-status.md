# AID-2026-014 — R3 Correction Status

## 1. Authority

Work Item: AID-2026-014

Tracking Issue: #265

ADR Carrier: #43, comment 7034237663

Disposition: CORR-APPLY-DISP-01

Correction Status: APPLIED_PENDING_INDEPENDENT_REVIEW

## 2. Decision status

OWNER DECISION = DECIDED FOR CONVERGENCE

B OPTION A = DECIDED FOR CONVERGENCE

D OPTION A = DECIDED FOR CONVERGENCE

R3 REVIEW DISPOSITION = REQUEST CHANGES (STRICTEST WINS)

FORMAL ACCEPTANCE = PENDING

SCHEMA FREEZE = NOT APPROVED

IMPLEMENTATION CONFORMANCE = NOT ESTABLISHED

DDL = NOT APPROVED

PUBLIC API = NOT APPROVED

H WIRE = NOT APPROVED

PRODUCTION ATTESTATION KEYS = NOT APPROVED

TRUST ROOT = NOT APPROVED

CRYPTOGRAPHIC PROFILE = NOT APPROVED

STORAGE L4 = OPEN / NOT APPROVED

TEST EXECUTION = SUSPENDED

## 3. Correction status by requirement

| Requirement | Application status | Independent review |
|---|---|---|
| R1 Claim identity | FIX_APPLIED_AWAITING_REREVIEW | PENDING |
| R2 Attestor authorization | FIX_APPLIED_AWAITING_REREVIEW | PENDING |
| R3 Shared Fact Forget | FIX_APPLIED_AWAITING_REREVIEW | PENDING |
| R4 Fact/Claim synchronization | FIX_APPLIED_AWAITING_REREVIEW | PENDING |
| R5 End-to-end publication | FIX_APPLIED_AWAITING_REREVIEW | PENDING |
| R5 Storage §8.8 | APPLIED_PENDING_INDEPENDENT_REVIEW | PENDING |
| PASS governance synchronization | FIX_APPLIED_AWAITING_REREVIEW | PENDING |

## 4. Application evidence requirements

Every applied target MUST record:

1. Exact repository commit HEAD before application.
2. Exact target path.
3. Original Blob SHA.
4. Exact pre-change content.
5. Resulting Blob SHA.
6. Resulting commit HEAD.
7. Actual line-count and diff statistics.
8. EN/ZH parity evidence.
9. Independent review reference.

The application record MUST use the actual HEAD and Blob values returned by the application and read-back process.

A source session's reported HEAD MUST NOT be used as application evidence.

## 5. Independent review procedure

The independent reviewer MUST inspect:

1. Exact applied R1 Blob.
2. Exact applied R2 Blob.
3. Exact applied R3 Blob.
4. Exact applied R4 Blobs and cross-synchronized consumers.
5. Exact applied R5 D/E/G Blobs.
6. Storage §8.8 carrier and Blob, if located.
7. EN/ZH semantic parity.
8. The seven-column R5 failure matrix.
9. The R5 reversible-order designation.
10. The PASS governance and evidence separation.

Each R1-R5 item requires an explicit PASS or REQUEST CHANGES decision.

No item may be marked CLOSED solely on author assertion.

## 6. Test execution gate

Test execution MUST remain suspended until R1-R5 have all passed independent review.

The existence of a specification does not establish test PASS.

The existence of a written test case does not establish test PASS.

An empty CI record, missing workflow execution, or unavailable execution output does not establish test PASS.

A review PASS is not Formal Acceptance.

An applied correction is not independently reviewed until its exact commit HEAD and Blob content have been read back and reviewed.

## 7. Final approval boundary

Formal Acceptance remains PENDING.

Schema Freeze remains NOT APPROVED.

Implementation Conformance remains NOT ESTABLISHED.

No production authorization is granted by this correction record.

## 8. Application evidence

Application baseline HEAD: 94cbb4dbffae9935373935f699ea74a7daee983b

Applied by: L0 registration channel (CORR-APPLY-DISP-01, finalize 6b002288) on the 43 server main tree.

All HEAD and Blob values below are returned by the application and read-back process. A source session's self-reported HEAD is not used as application evidence.

Read-back through commit fc17542d (main) and the AID-2026-014 carrier audit; see the correction note
at the end of this section for the three Blobs that changed after the original application round.

| File | Group | Commit SHA | Blob SHA | UTC |
|---|---|---|---|---|
| docs/en/02-domain-model/domain-model-overview.md | R1 §2.4 | d575ebc254ac | 47327d8a0f26 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R1 §2.4 | d575ebc254ac | 03843f8e1d98 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R1 §2.4 | d575ebc254ac | 47327d8a0f26 | 2026-11-20T19:53:40+08:00 |
| docs/en/09-security-governance/security-governance-guide.md | R2 §12 | 9420435f8eb7 | 60b2283fdf44 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/09-security-governance/security-governance-guide.md | R2 §12 | 9420435f8eb7 | 9fee318f2def | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | R2/R4 §3.15 | 74a531814cb2 | ec4a27099b29 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R2/R4 §3.15 | 74a531814cb2 | 0b2aa1c35553 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R2/R4 §3.15 | 74a531814cb2 | ec4a27099b29 | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | R3 §8.1 | 0e8ce367de8d | 364ce11587bc | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R3 §8.1 | 0e8ce367de8d | 28695a53a26a | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R3 §8.1 | 0e8ce367de8d | 364ce11587bc | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | R4 §1/§4/§11/§12 | 1cd36650f1d3 | 46fbdcacbe8a | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R4 §1/§4/§11/§12 | 1cd36650f1d3 | d80d0515f9e0 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/domain-model-overview.md | R4 §1/§4/§11/§12 | 1cd36650f1d3 | 46fbdcacbe8a | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/phase-1-domain-model-freeze.md | R4 phase-1-freeze | 5429eff46d76 | 80a159515717 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md | R4 phase-1-freeze | 5429eff46d76 | acf12e265b52 | 2026-11-20T19:53:40+08:00 |
| docs/en/00-governance/architecture-invariants.md | R4 arch-invariants | 088de92867fc | 4213ab67dc8a | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/00-governance/architecture-invariants.md | R4 arch-invariants | 088de92867fc | 909be080e7f5 | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/core-entities.md | R4 core-entities | 08630cf875d6 | 58fd178a7b46 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/core-entities.md | R4 core-entities | 08630cf875d6 | 998213221432 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/core-entities.md | R4 core-entities | 08630cf875d6 | 06a914699813 | 2026-11-20T19:53:40+08:00 |
| docs/en/02-domain-model/relationships-and-provenance.md | R4 relationships | 7873b5768f65 | cbacc2344310 | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/02-domain-model/relationships-and-provenance.md | R4 relationships | 7873b5768f65 | 684cb6b15242 | 2026-11-20T19:53:40+08:00 |
| 02-domain-model/relationships-and-provenance.md | R4 relationships | 7873b5768f65 | a674e21756cd | 2026-11-20T19:53:40+08:00 |
| docs/en/03-memory-brain/memory-versioning.md | R5 memory-versioning | e8078af592ea | d6694ba1409b | 2026-11-20T19:53:40+08:00 |
| docs/zh-CN/03-memory-brain/memory-versioning.md | R5 memory-versioning | e8078af592ea | dc652751d8c0 | 2026-11-20T19:53:40+08:00 |
| docs/en/04-memory-compiler/extraction-and-normalization.md | R5 extraction §19.1 | 5bf757863cd0 | 8d408328ed0d | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | R5 extraction §19.1 | 5bf757863cd0 | 6d67d73c5cca | 2026-11-20T19:53:41+08:00 |
| docs/en/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | R5 G addendum | bcf127f07078 | 28ab2832d5f2 | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | R5 G addendum | bcf127f07078 | d651005e5a87 | 2026-11-20T19:53:41+08:00 |
| docs/en/02-domain-model/domain-model-overview.md | PASS §13+CH | 961d2191bba6 | 443b35b288fc | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | PASS §13+CH | 961d2191bba6 | 736fc5865c54 | 2026-11-20T19:53:41+08:00 |
| 02-domain-model/domain-model-overview.md | PASS §13+CH | 961d2191bba6 | 443b35b288fc | 2026-11-20T19:53:41+08:00 |
| docs/en/00-governance/aid-2026-014-r3-correction-status.md | PASS status files | 1d9e2bd18771 | 8ad07e794f05 | 2026-11-20T19:53:41+08:00 |
| docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md | PASS status files | 1d9e2bd18771 | d6d7e00e03f9 | 2026-11-20T19:53:41+08:00 |

Not applied in this round (isolated, no repository write):

- G root §13.3 direct integration: APPLIED. Root file 06-memory-context/context-versioning.md was rebuilt as the canonical root-level normative source (commit 2606978e, Blob 8503a171922a27aca469042164b2e14f5f525910). Addendum Blobs 249fd8691707 (EN) and aed4f80857de (ZH) are merged into that section and no longer claim an independent competing protocol. §14.5 was subsequently aligned to §13.3 as its subordinate constraint (commit fc17542d, Blob dbce95485d02c8b25bfa2c13596c32d0d57b341d). Introduced legacy-open reads of Blob 05c0739d... are superseded.
- Storage ADR §8.8: APPLIED. Carrier branch session-storage-consistency-forget-atomicity-2026-11-16, path reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md. Applied at commit 9f63874ecf2c4d8292435c8c10d0b7b4fe9c620f; Blob bb544ba2f346bdc130d524bd5c7310d86f367988 -> edd81e2ba21c752fc88fa5e1c3cf2f2cca8cf603 (27834 -> 29945 bytes, 274 -> 333 lines). Section 8 now runs continuously 8.1 through 8.8. The bilingual 8.8 text is the Owner text from Issue #265 comment 7037252404, applied verbatim in the ADR's existing bilingual convention. The existing L1 decision and the Storage L4 OPEN boundary are preserved; 8.8 does not select a new topology. NOT_APPLIED_PENDING_LOCATE is withdrawn: the earlier recursive-tree search was scoped to main only while the prompt-pinned carrier lives on the Storage owner branch. F-265-STORAGE-01 / SD-08 close on this record. Cross-branch normative coexistence is recorded as a follow-up, not a blocker for this application.

This Application evidence section is added by the application-evidence commit itself; that commit SHA and the resulting status-file Blobs are recorded in the L0 application report and by the raw read-back.
