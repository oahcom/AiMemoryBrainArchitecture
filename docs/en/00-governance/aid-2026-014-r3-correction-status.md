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

## 9. Correction note — read-back after the R5 application round

The round recorded in §8 above was written before three Blobs changed. This note is the
read-back that supersedes the corresponding rows, per the requirement in §4 that application
records carry the actual HEAD and Blob values.

| Target | Superseded value | Current value | Commit | Note |
|---|---|---|---|---|
| 06-memory-context/context-versioning.md | 05c0739d0c22 | dbce95485d02 | fc17542d | §13.3 rebuilt as canonical root source (2606978e, 8503a171), then §14.5 aligned to §13.3 as its subordinate constraint. EN-only root file; no ZH counterpart exists for this root path before or after. |
| docs/en/00-governance/aid-2026-014-r3-correction-status.md | 8ad07e794f05 | d9b3a9141c71 | 8b9cb119 | Status table flipped to FIX_APPLIED_AWAITING_REREVIEW / APPLIED_PENDING_INDEPENDENT_REVIEW. |
| docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md | d6d7e00e03f9 | 706c4da352e5 | 8b9cb119 | Restored to its paired location by 25c61283 after 927eadcb renamed it alone into docs/governance/archive/; the orphaned archive copy was removed. |

Storage §8.8 is **not** in this repository's `main` tree. Its applied state lives on the carrier
branch `session-storage-consistency-forget-atomicity-2026-11-16` at commit `9f63874e`, Blob
`edd81e2ba21c`. That branch is the Storage owner branch whose tip `281fd1ed` and L1-topology Blob
`bb544ba2` are pinned by AID-2026-014-PROMPT v1. Application on that branch is the correct
disposition; copying the ADR into `main` would create a second normative copy and was not done.

Open follow-up (not a blocker for R5): cross-branch normative coexistence has no Owner ruling yet.
Until one exists, the ADR is authoritative on its own branch and MUST NOT be mirrored.

R3 review disposition, formal acceptance, schema freeze, and implementation conformance are
unchanged by this note. All seven rows still carry `PENDING` for independent review.

### 9.1 Pinned read-back of the R1 and R4 correction round

Read-back baseline HEAD: `dd4ecf167c4af4ccb911f18dcfca2ca849f0b650`. Every Blob below was read at that exact commit, not at a moving
branch head. That is deliberate: `main` advanced from `92459e0f` through `1733c3bf` to `dd4ecf16`
while this note was being written, and `memory-versioning.md` changed twice inside that window. A
read-back that names no baseline is not evidence, so §4 is satisfied here by pinning.

| Group | What the round changed |
|---|---|
| R1/R4 | Canonical Claim identity semantics confirmed DECIDED; stale `OPEN` clauses removed from the domain-model Overview and the phase-1 Freeze (6 clauses, EN/ZH/root). |
| R1 consumer | Downstream text aligned to the decided Claim identity semantics. |
| R4/R5 consumer | Extraction separates Claim identity, Fact-specific modeling, and physical Schema. |
| G | §13.3 established as canonical root source; §14.5 aligned to it as subordinate. |

| Target | Group | Value this round supersedes | Blob at baseline HEAD | Producing commit |
|---|---|---|---|---|
| docs/en/02-domain-model/domain-model-overview.md | R1/R4 | 46fbdcacbe8a | 5b86fe23ab7c670b4ae13331b56572aee35f5d00 | bc114263 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R1/R4 | d80d0515f9e0 | 03129ded6e9532048240aea3a18414370cbcb73d | bc114263 |
| 02-domain-model/domain-model-overview.md | R1/R4 | 46fbdcacbe8a | 5b86fe23ab7c670b4ae13331b56572aee35f5d00 | 778d1bee |
| docs/en/02-domain-model/phase-1-domain-model-freeze.md | R4 | 80a159515717 | 1a18c6b8424c939dd90986527a24807c8f74d552 | bc114263 |
| docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md | R4 | acf12e265b52 | 408a606c44fcf271f265508bc9d3029f8fc889cb | bc114263 |
| 02-domain-model/phase-1-domain-model-freeze.md | R4 | not in §8 | d1102a0adf32e3f7b3eb9091758823f990a2a37c | ae5a886f |
| docs/en/03-memory-brain/memory-versioning.md | R1 consumer | d6694ba1409b | 7e63b9b397c3bdff1567dab421f658af86ee1a48 | 5ed9669d |
| docs/zh-CN/03-memory-brain/memory-versioning.md | R1 consumer | dc652751d8c0 | 89d9eb4786615cc43f7098b206c1ccd446536fa2 | 9c94b3c4 |
| docs/en/04-memory-compiler/extraction-and-normalization.md | R4/R5 consumer | 8d408328ed0d | 10c46fd79c53c54a77f8bd2c91107a4b2aeaabda | 39553c25 |
| docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | R4/R5 consumer | 6d67d73c5cca | cec9cf3185659b8d9ba1dd916674f71dd4fce808 | 39553c25 |
| docs/en/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | G | 28ab2832d5f2 | 190bd11d8226d6e6e3c97ad37b700d43b8b70720 | ae5a886f |
| docs/zh-CN/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md | G | d651005e5a87 | 47d9fe9b7387c843f09f519519b14e998a1a65c7 | ae5a886f |
| 06-memory-context/context-versioning.md | G root | 05c0739d0c22 (§8 bullet) | 847c9578b4404c1a034fe62ee9bbffa598f7ab2e | ae5a886f |

Two rows need a word of caution. The root-level `02-domain-model/phase-1-domain-model-freeze.md`
has no row in §8 at all, so there is no superseded value to cite; `not in §8` is literal, not a
placeholder. The root-level `06-memory-context/context-versioning.md` appears in §8 not as a table
row but inside the "Not applied in this round" bullet, hence the `(§8 bullet)` qualifier.

The R4 closure is substantive, not clerical. `10c46fd7` splits three questions that the earlier
text ran together: canonical Claim identity semantics are `DECIDED FOR CONVERGENCE` and governed
by D; Fact-specific modeling and Fact approval remain `OPEN` under INT-P0-01; physical Schema and
DDL remain `NOT APPROVED`. `ADR-BLOCKED` no longer describes Claim identity mapping. The
independent-review finding on this point was read from `2717fadb`, which is superseded.

Two status values appear in §3: `FIX_APPLIED_AWAITING_REREVIEW` and
`APPLIED_PENDING_INDEPENDENT_REVIEW`. They are one certainty level, not two grades. Both mean the
application happened and independent review has not; they differ only in which round produced the
application. Recorded here so the difference is not read as a ranking.

The two status files carry no row above, because this section ships inside them: their pre-commit
Blobs were `db3e9f394c61c247ae9dde51c92d190f194ee11a` (EN) and `87c00ade741ebc0837c2f6903b820741f2887e4a` (ZH), superseded by the commit that adds this section.
