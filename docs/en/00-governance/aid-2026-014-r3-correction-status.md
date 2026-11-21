# AID-2026-014 — R3 Correction Status

## 1. Authority

Work Item: AID-2026-014

Tracking Issue: #265

ADR Carrier: #43, comment 7034237663

Disposition: CORR-APPLY-DISP-01

Correction Status: APPLIED

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
TEST EXECUTION DISPATCH GATE = UNLOCKED-WITH-CONDITIONS (REQ-04 STEP 5 DISPATCH SPEC ONLY)

## 3. Correction status by requirement

| Requirement | Application status | Independent review |
|---|---|---|
| R1 Claim identity | APPLIED | REQUEST CHANGES (R1-01, R1-02; §9.9) |
| R2 Attestor authorization | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R3 Shared Fact Forget | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R4 Fact/Claim synchronization | APPLIED | PASS (M19: 7050001430; M20: 7050002020) |
| R5 End-to-end publication | APPLIED | PASS (M19: 7050001430; M20: 7050002020; M27: 7057332489; M28: 7057332846) |
| R5 Storage §8.8 | APPLIED | PASS (M22: 7056912025; M27: 7057332489; M28: 7057332846) |
| R5 Admission stage relation | APPLIED | PASS (M25: 7057203158; M26: 7057203517; M27: 7057332489; M28: 7057332846) |
| PASS governance synchronization | APPLIED | PASS (M19: 7050001430; M20: 7050002020; M27: 7057332489; M28: 7057332846) |

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
| docs/en/02-domain-model/domain-model-overview.md | R1/R4 | 443b35b288fc | 5b86fe23ab7c670b4ae13331b56572aee35f5d00 | bc114263 |
| docs/zh-CN/02-domain-model/domain-model-overview.md | R1/R4 | d80d0515f9e0 | 03129ded6e9532048240aea3a18414370cbcb73d | bc114263 |
| 02-domain-model/domain-model-overview.md | R1/R4 | 443b35b288fc | 5b86fe23ab7c670b4ae13331b56572aee35f5d00 | 778d1bee |
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

Earlier versions of §3 used two status values, `FIX_APPLIED_AWAITING_REREVIEW` and
`APPLIED_PENDING_INDEPENDENT_REVIEW`. At that time both denoted one certainty level, not two
grades: the application happened and independent review had not, differing only in which round
produced the application. These are historical values. They no longer describe the current §3
rows, which record `APPLIED` together with the independent-review result.

The two status files carry no row above, because this section ships inside them: their pre-commit
Blobs were `db3e9f394c61c247ae9dde51c92d190f194ee11a` (EN) and `87c00ade741ebc0837c2f6903b820741f2887e4a` (ZH), superseded by the commit that adds this section.

### 9.2 Read-back of the admission stage relation round

Read-back baseline HEAD: `da378340b0c7adb0ad3c1f128878bc96804c78d9`. Two commits closed the last substantive item from independent
review.

| Target | Commit | Blob before | Blob after | Size |
|---|---|---|---|---|
| docs/en/04-memory-compiler/extraction-and-normalization.md | da378340 | 10c46fd79c53 | 03c8a6f32113d54cac097c792b896a4ec3f873b1 | 18070 -> 20841 B |
| docs/zh-CN/04-memory-compiler/extraction-and-normalization.md | da378340 | cec9cf318565 | ac484c860b9b8eb9da19801acd9a985f2a8b4b3a | 17662 -> 20233 B |
| reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md (carrier branch) | a5a13d63 | edd81e2ba21c | 8d4ac845f409c2cb64831c850219fdb84a113cf0 | 29945 -> 32954 B |

The gap was that the two admission names never met. Extraction named only `Producer Admission`,
required before D canonical commit; the Storage ADR §8.8 named only `PublicationParticipant
Admission`, required after D canonical commit and after Storage persisted the exact publication
tuple as `PREPARED_HIDDEN`. In the files as they stood, the same-named act carried two
contradictory positions and nothing said they were different acts.

The applied text rules them two distinct ordered stages, not aliases and not interchangeable
decisions. Producer Admission admits the exact Producer/ProducerWork identity before dependency-set
registration and canonical commit. PublicationParticipant Admission admits the exact
PublicationParticipant bound to the corresponding StorageVisibilityParticipantRef and publication
tuple digest, after canonical commit and after PREPARED_HIDDEN persistence. Success in the first is
explicitly not success in the second. Both MUST be atomic with their own participant recording.
Both serialize against the same authoritative ordering anchor. The dependency closure established
during Producer Admission and dependency-set registration MUST NOT be created, replaced, narrowed
or independently redefined at publication.

Extraction carries this as a new §19.2, inserted before that file's existing `#### Storage
boundary` block. The two boundary sentences in that block are unchanged and are not restated in
§19.2. The ADR carries it as a clarification inside §8.8, placed after the seven-step order and
before the per-BrainAuthorityRef serialization-anchor statement. The seven steps, the anchor, the
L1 decision and the L4 OPEN boundary are untouched.

Both insertions state this is an implementation-conformance gate, not an unresolved normative
ordering choice, so the fix reopens nothing that is already DECIDED FOR CONVERGENCE.

R3 disposition, formal acceptance, schema freeze and implementation conformance are unchanged.

### 9.3 Independent review disposition of the correction round

Reviewer: independent session `6b00a00c-3ad0-83ee-bda0-f6dcdef2fbd9` (read-only, no repository
write, no comment posted by the reviewer). Verdict returned 2026-11-21: `PASS` on the three items
that were still blocked, superseding the earlier `REQUEST CHANGES` on those three.

The reviewer read the files themselves, not the L0 summary. Blobs it cites, verified against the
repository after the fact:

```
docs/en/04-memory-compiler/extraction-and-normalization.md   03c8a6f32113d54cac097c792b896a4ec3f873b1
docs/zh-CN/04-memory-compiler/extraction-and-normalization.md   ac484c860b9b8eb9da19801acd9a985f2a8b4b3a
reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md (carrier branch)   8d4ac845f409c2cb64831c850219fdb84a113cf0   32954 B
```

| Item reviewed | Earlier | Now | What the reviewer says it checked |
|---|---|---|---|
| R5 Admission stage relation | REQUEST CHANGES | PASS | Two distinct ordered stages; `MUST NOT be treated as aliases`; success in stage 1 explicitly not success in stage 2; both on one ordering anchor; dependency closure created at Producer Admission and not narrowable at publication. |
| R4 Claim identity / Fact modeling | REQUEST CHANGES | PASS | Re-read the current Blobs instead of carrying over the old `2717fadb` finding. `OPEN` now bounds only Fact-specific modeling and Fact approval. No unresolved item is repackaged as closed. |
| Application evidence §9.1 + §9.2 | REQUEST CHANGES | PASS | Continuous correction record: targets, Blobs before and after, commits, sizes, reasons. All review states still `PENDING` at the time of review, so no review outcome was claimed in advance. |
| Storage §8.8 alignment | PASS | PASS | Seven-step order not rewritten; §8.8 clarification only states that a distinct Producer Admission precedes it. |
| Bilingual synchronization | PASS | PASS | EN/ZH carry the same normative content. |

What `PASS` does not mean, stated by the reviewer and preserved here:

- Not formal acceptance. `FORMAL ACCEPTANCE = PENDING` is unchanged.
- Not schema freeze. `SCHEMA FREEZE = NOT APPROVED` is unchanged.
- Not implementation conformance. `IMPLEMENTATION CONFORMANCE = NOT ESTABLISHED` is unchanged,
  and `DDL`, `PUBLIC API`, `H WIRE`, `PRODUCTION ATTESTATION KEYS`, `TRUST ROOT`,
  `CRYPTOGRAPHIC PROFILE` all remain `NOT APPROVED`. `STORAGE L4` remains `OPEN`.
- Not a reopening of anything `DECIDED FOR CONVERGENCE`.

One implementation gate the reviewer keeps open, on its own initiative: a concurrent-interleaving
test MUST demonstrate that a Forget Fence does not complete disposition while the dependency
closure has not fully entered the participant barrier. This is implementation conformance, not an
unresolved ordering choice, and it is not satisfied by the existence of the text.

`R1`, `R2`, `R3`, `R5 End-to-end publication` and `PASS governance synchronization` were not
re-adjudicated in this round and keep `PENDING`. The overall disposition is therefore narrower than
the round's `PASS`: three rows moved, five did not, and the acceptance gates did not move at all.
### 9.4 Second independent review — changes required

Reviewer: independent session `6b0112a2-7b64-83ee-a29b-da285ff8d589` (read-only, no repository
write, no comment posted by the reviewer). Verdict returned 2026-11-21. Read-back pin:
`8dc92c3debde36929d34808bead0a62ffc4f64fa`. Twelve Blobs were read at that exact commit.

This is not a re-run of §9.3. §9.3 covered the three items that were blocked then; this review
covers the four that §9.3 left `PENDING`. It supersedes the closing paragraph of §9.3 and the
sentence in §9 that all rows still carry `PENDING`: both described the state before this verdict,
and §3 carries the current state.

Blob identities the reviewer verified, all MATCH against the pin:
```
docs/en/09-security-governance/security-governance-guide.md        60b2283fdf44d116fa59fe84eaab217b435fbe70  15171 B
docs/zh-CN/09-security-governance/security-governance-guide.md     9fee318f2def690b3db9386d938df790292fb05f  13359 B
docs/en/03-memory-brain/memory-versioning.md                       7e63b9b397c3bdff1567dab421f658af86ee1a48  33424 B
docs/zh-CN/03-memory-brain/memory-versioning.md                    89d9eb4786615cc43f7098b206c1ccd446536fa2  31768 B
docs/en/02-domain-model/domain-model-overview.md                   5b86fe23ab7c670b4ae13331b56572aee35f5d00  26974 B
docs/en/04-memory-compiler/extraction-and-normalization.md         03c8a6f32113d54cac097c792b896a4ec3f873b1  20841 B
docs/zh-CN/04-memory-compiler/extraction-and-normalization.md      ac484c860b9b8eb9da19801acd9a985f2a8b4b3a  20233 B
docs/en/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md   190bd11d8226d6e6e3c97ad37b700d43b8b70720  2822 B
docs/zh-CN/06-memory-context/phase-3.8.27-g-claim-fact-visibility-addendum.md   47d9fe9b7387c843f09f519519b14e998a1a65c7  2626 B
06-memory-context/context-versioning.md                            847c9578b4404c1a034fe62ee9bbffa598f7ab2e  32435 B
docs/en/00-governance/aid-2026-014-r3-correction-status.md         0047e6fc83b50eb561ebfc5f7b5440448435d79a  22544 B
docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md      4b41c177f1707be1b24334df60ca85c95974c612  21054 B
```

| Item | Verdict | Blocking finding |
|---|---|---|
| R2 Attestor authorization | REQUEST CHANGES | R2-01 |
| R3 Shared Fact Forget | REQUEST CHANGES | R3-01 |
| R5 End-to-end publication | REQUEST CHANGES | R5-01, R5-02 |
| PASS governance synchronization | PASS | — |
| R4 Fact/Claim synchronization | PASS, inherited | not re-adjudicated |
| R5 Storage §8.8 | PASS, inherited | not re-adjudicated |
| R5 Admission stage relation | PASS, inherited | not re-adjudicated |

**R2-01 — the authorization decision is not bound to a single attestation operation.** The I/D
split itself passes: §1 gives I the global identity and authorization policy, Delegation and
Revocation; §12.1 makes I the sole governance decision authority for Attestor authorization and
forbids D from judging eligibility or reinterpreting the decision; D only verifies. Revocation is
also adequate: §12.3 requires PrincipalRef, exact ScopeRef, Method and immutable Version, validity
window and authorization epoch, revocation identity and currentness, explicit Delegation
`ALLOWED`/`PROHIBITED`, an immutable `AuthorizationDecisionRef`, and policy provenance; §12.4 fails
closed; §12.5 forbids silently rewriting history. The gap is single-use binding. §12.2 stores an
authorization decision reference on the FactRevision, but the §12.3 field list does not require
binding it to a unique `AttestationOperationRef`, to the exact target `FactRef`/`FactRevisionRef`,
to the exact `ClaimRevisionRef` set of that operation, to the exact `EvidenceRef` set, or to a
one-time-consumption or anti-replay state. §12.6's D verification list likewise never requires
checking that the decision is bound to the current unique attestation operation. The concrete
replay reading: one decision, cited by a second FactRevision, satisfies every explicitly listed
Scope, Method and validity check; nothing in the current text forbids it, and two FactRevisions
each holding a reference does not prove the decision was used once. The fix is asked for as a
semantic contract only — no Schema, DDL or Public API approval is requested.

**R3-01 — the six-component matrix has no Forget terminal-state mapping.** The shared-closure rules
pass. `§8.1` requires Forget to act on the complete dependency closure: exact Claim/Fact revision
references, Evidence with its own governance and source payload, reconstructable Provenance,
derived MemoryVersion and ContextVersion, Index and Cache clearing plus read-path suppression,
Snapshot/Staging in the dependency list, Replay/Retry/Recovery history checks, Export under
authorization and Forget checks, Backup retention, and Restore re-checks before query or delivery.
Its three constraints are the substantive part: a shared Fact does not give multiple ClaimRevisions
one shared disposition; if the remaining lawful content cannot be safely isolated the whole
affected FactRevision must be suppressed; and an unknown or incomplete dependency set forbids
declaring Forget complete. §19.1 also leaves no lawful publish-then-register path, since step 3
persists the full direct and transitive dependency set before step 5 permits canonical commit and
step 7 permits E publication. What is missing is a different artefact: I Security Guide §7 defines
four operation terminal states — `Completed`, `CompletedWithPolicyException`, `Failed`,
`Cancelled` — and §16.1 builds no disposition mapping from those states onto its six components.
The reviewer names four questions the matrix cannot answer today: whether `Cancelled` permits a
committed canonical revision to remain; how `Failed` terminates when E publication happened but
Storage visibility did not; whether `CompletedWithPolicyException` permits a G ContextVersion commit
or only a hidden state; and which terminal states must complete all six components versus end on a
suppression disposition. Behaviour is currently inferable only from the declared
completion/suppression policy, not checkable against the matrix. This is a request for one
terminal-state × component disposition table, not for a duplicated failure matrix per fault.

**R5-01 — the second-stage Fence-first outcome is undefined.** A race window that the original
T17 does not cover: Producer Admission succeeds and the participant record is durable; dependency
registration and canonical commit succeed; E publication produces the object and Storage persists
the exact tuple as `PREPARED_HIDDEN`; then the Forget Fence and PublicationParticipant Admission
race and the Fence linearizes first, so the second admission cannot succeed. §19.2 settles the
ordering anchor, the inseparability of second-stage success from its participant record, the bar on
crossing an unresolved admitted-participant barrier, and the bar on replacing participant identity.
It does not say what happens to objects that already exist. Five questions are left open: whether
the committed canonical revision stays permanently unpublishable; what happens to an E publication
that already exists; whether the `PREPARED_HIDDEN` tuple must be cancelled, quarantined, or held in
a pending-disposition state; how the first-stage participant disposition reaches a
PublicationParticipant that never successfully admitted; and how it is proven that the hidden tuple
cannot become visible through recovery, retry, or another publication path.

**R5-02 — the six-component matrix still has one `Admission` column.** §16.1 still reads
`D Fence → Admission → D Canonical Commit → E Publication → Storage Visibility → G Context Commit`,
while §19.2 now defines two admissions. A Fence that linearizes before Producer Admission, between
the two admissions, or after PublicationParticipant Admission succeeds leaves different durable
records, different visibility states and different final dispositions, and only the first of the
three timings is named by T17/T18.

What this verdict does not do, stated by the reviewer and preserved here:

- It does not reopen the `DECIDED FOR CONVERGENCE` publication order, the two-admission
  distinction, the R4 three-layer split, or the applied Storage §8.8 position.
- It does not allege production data leakage. R3's finding is about normative checkability; the
  reviewer records that no published-but-unregistered production instance is known.
- It does not change any acceptance gate. §2 is unchanged in every line.
- It does not authorize testing. `TEST EXECUTION = SUSPENDED` stands, and the reviewer lists
  preconditions rather than execution.

The reviewer also re-read the Storage ADR §8.8 Blob on its carrier branch
(`8d4ac845f409c2cb64831c850219fdb84a113cf0`) and states its seven-step order and two admission
definitions agree with Extraction §19.2, without re-adjudicating the ADR body.

SYNC items handed to the correction round (EN and ZH both, not English alone):

| Id | Target | Change |
|---|---|---|
| SYNC-01 | Security Guide §12.3 | Bind the decision to a unique attestation operation and its targets; forbid cross-operation replay |
| SYNC-02 | Security Guide §12.6 | Require D to verify operation identity, target set and consumption state |
| SYNC-03 | Domain Model §8.1 | Keep the closure rules; add their correspondence to Forget terminal states |
| SYNC-04 | Memory Versioning §16.1 | Add the Forget terminal-state × six-component disposition matrix |
| SYNC-05 | Extraction §19.1 / §19.2 | Complete the second-stage Fence-first and Participant-first dispositions |
| SYNC-06 | Memory Versioning §16.1 | Separate Producer Admission from PublicationParticipant Admission |
| SYNC-07 | G §13.3 | State the no-publish and recovery constraints when the second stage is refused |

Test preconditions named by the reviewer, to be satisfied before execution is reconsidered: unique
attestation-operation binding and a cross-FactRevision reuse rejection test (R2); multi-ClaimRevision
shared-Fact Forget, Evidence and Provenance dependencies, Export/Backup/Restore paths, the four
terminal states across six components, and commit blocked on incomplete dependency registration
(R3); `T17-P`, `T18-P`, `T17-PUB`, `T18-PUB`, two-admission concurrent interleaving, Fence versus
`PREPARED_HIDDEN`, crash, lost ACK, retry and recovery, no duplicate visible revision, publication or
ContextVersion, and no Fence completing over an unresolved participant barrier (R5). Admission
success plus durable participant record must hold in both stages, not only the first.

The Application status column in §3 is left as it stands: the previous application is still in the
tree. The Independent review column now carries this verdict, which is why four rows changed and
none of the acceptance gates did.

### 9.5 Application of the seven SYNC items

Read-back baseline HEAD: `836dc1055547f1dd9fba2081a5280ef22cbb94c5`. Every Blob below was read at that exact commit.

Seven items were applied in three commits, then one defect was found and removed in a fourth.
The table records what the tree holds now, not what an earlier commit held.

| Target | Item | Blob before | Blob after | Size | Commit |
|---|---|---|---|---|---|
| `docs/en/09-security-governance/security-governance-guide.md` | R2 / SYNC-01+02 | `60b2283fdf44` | `061c5847b3df` | 15171 -> 20714 B | `782c4c8d` |
| `docs/zh-CN/09-security-governance/security-governance-guide.md` | R2 / SYNC-01+02 | `9fee318f2def` | `372d27c79dc7` | 13359 -> 18224 B | `782c4c8d` |
| `docs/en/03-memory-brain/memory-versioning.md` | R3+R5 / SYNC-04+06 | `7e63b9b397c3` | `84aabc25bb07` | 33424 -> 48474 B | `9eca5eda` |
| `docs/zh-CN/03-memory-brain/memory-versioning.md` | R3+R5 / SYNC-04+06 | `89d9eb478661` | `aa2fc775c786` | 31768 -> 44569 B | `9eca5eda` |
| `docs/en/02-domain-model/domain-model-overview.md` | R3 / SYNC-03 | `5b86fe23ab7c` | `1a1a10b24d68` | 26974 -> 28507 B | `9eca5eda` |
| `docs/zh-CN/02-domain-model/domain-model-overview.md` | R3 / SYNC-03 | `03129ded6e95` | `8ef976789af6` | 24417 -> 25636 B | `9eca5eda` |
| `docs/en/04-memory-compiler/extraction-and-normalization.md` | R5 / SYNC-05 | `c87860706313` | `e6aad4b7504f` | 22484 -> 26256 B | `d36c27c9` |
| `docs/zh-CN/04-memory-compiler/extraction-and-normalization.md` | R5 / SYNC-05 | `9657949af482` | `8dd0b5b29ecd` | 21781 -> 25185 B | `d36c27c9` |
| `06-memory-context/context-versioning.md` | R5 / SYNC-07 | `847c9578b440` | `ce952ba3eca3` | 32435 -> 34566 B | `d36c27c9` |

**SYNC-01 and SYNC-02 — the authorization decision is now single-use.** `§12.3` gains three
numbered fields after the original seven: a unique `AttestationOperationRef` binding that names
the exact `FactRef`/`FactRevisionRef` targeted by that operation; exact `ClaimRevisionRef`,
`EvidenceRef` and, where provenance is attested input, `ProvenanceRef` set binding, with an
explicit bar on an unspecified, subsequently expanded, substituted or implicitly resolved set; and
a single-use consumption and replay-protection state that separates an unused decision from one
consumed by its uniquely bound operation, after which the decision MUST NOT authorize another
operation, FactRevision, target, claim set or evidence set. `§12.6` gains the matching D duties:
verify that the `AuthorizationDecisionRef` is bound to the current unique operation, verify the
exact target and exact input sets, and verify consumption state. The closing paragraph states the
whole thing is a semantic contract and an implementation-conformance boundary, not a Schema, DDL
or Public API approval.

**SYNC-03 — closure rules now meet terminal states.** `§8.1` keeps every closure rule unchanged and
adds their correspondence to the Forget terminal states: no terminal state may be declared on an
incomplete closure, and `Failed`/`Cancelled` must dispose of every registered dependency rather
than only the initiating object. The shared-Fact, whole-FactRevision-suppression and
unknown-closure-blocks rules are untouched.

**SYNC-04 and SYNC-06 — the matrix now names two admissions and maps four terminal states.**
`§16.1` no longer says `Admission`. The seven logical components are `D Fence`, `Producer
Admission`, `D Canonical Commit`, `E Publication`, `PublicationParticipant Admission`, `Storage
Visibility`, `G Context Commit`, with an explicit statement that the two admissions MUST remain
distinct and MUST NOT be treated as aliases or interchangeable operations. The nine-step
execution order places Producer Admission at step 2 and PublicationParticipant Admission at step 7,
after the `PREPARED_HIDDEN` persistence at step 6. A new `Forget terminal-state × component
disposition` matrix gives all seven components a disposition for each of `Completed`,
`CompletedWithPolicyException`, `Failed` and `Cancelled`, plus a last-permitted-visible-component
rule, the disposition of an already committed canonical revision, of an existing E Artifact, of a
`PREPARED_HIDDEN` tuple, the required audit evidence, and the UNKNOWN bar per state. Four
classification rules make the states mutually exclusive, including that `Failed` MUST NOT be
declared where an authoritative cancellation outcome supersedes it and that an execution failure
MUST NOT be relabelled `Cancelled`.

**The existing scenario table keeps its rows.** Only its `Admission` column is renamed to
`Producer Admission`. `Fence before Admission (T17)`, `Fence after Admission (T18)`, the crash,
lost-ACK, retry and post-visibility rows keep their meanings. A separate
`Second-stage Admission race matrix` adds `T17-P`, `T18-P`, `T17-PUB` and `T18-PUB`, which are
explicitly stated not to reinterpret or replace the first-stage scenarios.

**SYNC-05 — the second-stage rejection now has terminal dispositions.** Extraction `§19.2` gains a
`T17-PUB`/`T18-PUB` block between the existing body and `#### Storage boundary`, whose two
boundary sentences are unchanged. It closes the five open questions one by one: the committed
canonical revision stays committed but permanently non-public and a retry of the same rejected
operation does not constitute independent authorization; an existing E Publication has its public
visibility revoked or is isolated and cannot be replayed as a successful visible effect; the
`PREPARED_HIDDEN` tuple is cancelled or isolated with an auditable terminal outcome and an
unresolved tuple is not treated as cancelled or publishable; the first-stage Producer participant
gets an auditable suppression disposition that must bind the exact rejected
`PublicationParticipant` identity, its `StorageVisibilityParticipantRef` and the exact tuple
identity, with a generic operation-level suppression explicitly insufficient; and recovery, retry
and alternative publication paths must all verify proven second-stage admission and an
independently authorized visibility outcome before any advancement, failing closed on missing,
conflicting or UNKNOWN evidence. The block states it changes neither the ten-step `§19.1` order nor
the six-step `§19.2` order.

**SYNC-07 — G now refuses without the second stage.** `06-memory-context/context-versioning.md`
`§13.3` gains a block at the end of `#### 4. T18 — Participant-first`: no `ContextVersion` commit or
publication without successful second-stage admission; first-stage success is not evidence of
second-stage success; an already committed `ContextVersion` that references a publication object
without successful second-stage admission takes the `§16.1` terminal disposition; recovery and
replay re-evaluate at every read so a historical commit confers no permanent visibility; and the
publication identity, participants, closure and terminal Forget disposition must be preserved
throughout. `#### 5. G protected commit requirements` and `#### 6. Historical visibility` are
unchanged.

**A defect that was introduced and then removed.** The R2 delivery carried three HTML comments per
language that were drafting instructions to the author rather than normative text: two
`insert after` markers inside `§12.3` and `§12.6` and one `append to the end of §12.6` marker. They
shipped in `782c4c8d`. Commit `836dc105` removes the three comment lines and the blank line that
followed each, so paragraph spacing is unchanged; item numbering, the twelve D verification duties
and the semantic-contract paragraph are byte-identical. This is recorded because an application
record that shows only the final Blob would hide that the tree briefly carried non-normative
markup.

All nine targets were re-read at `836dc1055547f1dd9fba2081a5280ef22cbb94c5` after the cleanup, and none contains an HTML comment.

R3 review disposition remains `REQUEST CHANGES`; the three blocking items are applied but not
re-reviewed. `TEST EXECUTION = SUSPENDED` stands. No acceptance gate changed: `§2` is
byte-identical across all four commits.

### 9.6 Third independent review and closure of its two blocking findings

Reviewer: independent session `6b012e23-5ff0-83ee-95e1-1bea41ad85cf` (read-only, no repository
write, no comment posted by the reviewer). Verdict returned 2026-11-21. Read-back pin:
`7d2233a5bee2369fbb6358374ec5c2f049de88df`.

Five of seven items passed: R2-01 single-use binding, R3-01 terminal-state mapping, R5-01
second-stage convergence, bilingual equivalence, and the application-record audit. Two blocking
findings remained, both closed by `3b452dbe`.

| Item reviewed | Verdict | Blocking finding |
|---|---|---|
| R2-01 single-use authorization binding | PASS | — |
| R3-01 Forget terminal-state mapping | PASS | — |
| R5-02 two admission stages | REQUEST CHANGES | R5-02-01 |
| R5-01 second-stage convergence | PASS | — |
| SYNC-07 G-side constraint | REQUEST CHANGES | SYNC-07-01 |
| Bilingual equivalence | PASS | — |
| Application-record truthfulness (9.5) | PASS | — |

**R5-02-01 — the second admission had no indivisibility clause.** `§16.1` required that successful
Producer Admission and durable recording of the exact admitted Producer participant form one
indivisible operation. The second admission stated which identity it binds and forbade narrowing
the closure, but never forbade the state where second-stage admission has succeeded while its
exact participant record is not yet durable. A Fence could therefore observe the admission
without the record. The fix adds the symmetric requirement: successful
`PublicationParticipant` Admission and durable recording of the exact admitted
`PublicationParticipant` identity, its `StorageVisibilityParticipantRef` and the exact publication
tuple identity bound to the committed publication identity form one indivisible operation; the
intermediate state MUST NOT exist; and a Fence MUST NOT observe successful second-stage Admission
without simultaneously observing the complete durable participant record for that exact Admission.

**SYNC-07-01 — G pointed at the wrong matrix.** `§13.3` said a committed `ContextVersion` receives
the terminal disposition of the `six-component` protected publication failure matrix. That name
still describes the old scenario table, which was kept for T17/T18 row meanings and is not the new
terminal-disposition artefact. The fix repoints the sentence at the Forget terminal-state by
component disposition matrix, states its dimensions (four terminal states across seven logical
components), and ties the `G Context Commit` disposition to the applicable terminal state: no
commit under `Failed` and `Cancelled`; commit under `CompletedWithPolicyException` only when the
exception has received named approval and all preconditions hold; complete-completion
requirements under `Completed`. The existing prohibition on preserving a `ContextVersion` as a
successful visible publication merely because its canonical commit succeeded is retained.

The `six-component` phrase survives exactly once in the file, in `§13.3`'s pre-existing sentence
that the six-component matrix is normative for G `ContextVersion` commits derived from protected
Claim/Fact content. That sentence was correct before this round and is still correct: the old
table really does have six component columns. Only the new block's reference was wrong.

| Target | Blob before | Blob after | Size |
|---|---|---|---|
| `docs/en/03-memory-brain/memory-versioning.md` | `84aabc25bb07` | `4efbd26db958` | 48474 -> 49348 B |
| `docs/zh-CN/03-memory-brain/memory-versioning.md` | `aa2fc775c786` | `5ff17ab6cb56` | 44569 -> 45301 B |
| `06-memory-context/context-versioning.md` | `ce952ba3eca3` | `1bfe7f1891e1` | 34566 -> 35100 B |

One inconsistency in the reviewer's own output is recorded rather than smoothed over: its opening
summary table marks R5-02 as `PASS`, while its body adjudicates `REQUEST CHANGES` with blocking
finding R5-02-01 and the closing disposition is `REQUEST CHANGES`. The body governs. Reading the
summary row as the verdict would have closed a gap the same review opened three paragraphs later.

What the review confirms, in its own words, and what it does not do:

- The reviewer independently compared the pre-fix and post-fix Blobs and states that
  `#### 5. G protected commit requirements` and `#### 6. Historical visibility` are byte-identical,
  so the new G block did not rewrite either existing normative paragraph.
- It independently verified the nine pre-change Blobs and nine post-change Blobs in `§9.5` as
  MATCH, and independently re-read `782c4c8d` and `836dc105` to confirm the three-then-zero HTML
  comment counts.
- It re-checked the T17/T18 rows rather than accepting the column rename at face value, and states
  that only the `Admission` column name changed and row contents did not.
- It does not reopen any `DECIDED FOR CONVERGENCE` decision.
- It does not constitute `FORMAL ACCEPTANCE`, does not establish `IMPLEMENTATION CONFORMANT`, and
  does not lift `TEST EXECUTION = SUSPENDED`.

R3 review disposition after this round is still `REQUEST CHANGES`: the two findings are applied
but not yet re-reviewed. `§2` is unchanged in every line across all five commits of this round.

### 9.7 Fourth independent review — PASS on both closures

Reviewer: independent session `6b0133e2-3ce0-83ee-aa0c-8a994b9ea682` (read-only, no repository
write, no comment posted by the reviewer). Verdict returned 2026-11-21. Read-back pin:
`2fab32dea01310eb50f74aded3fa06e261e8e356`.

`PASS` on all five items: R5-02-01, SYNC-07-01, no newly introduced defect, bilingual equivalence
of the new `§16.1` paragraph, and the `§9.6` record. The reviewer states it checked the actual
`G Context Commit` column of the terminal-state matrix against the new G paragraph row by row and
found the four dispositions consistent, rather than accepting the pointer as sufficient.

It also settled the one point `§9.6` argued in prose: the old scenario matrix really does have six
component columns, so the surviving `six-component` sentence is correct and is not a blocking
finding.

It confirms the `3b452dbe` diff changed only the three target files, and that the nine-step
execution order, the existing T17/T18 rows, and the Schema / DDL / Public API / wire-format
exclusions are untouched.

Boundary, stated by the reviewer and preserved: no `DECIDED FOR CONVERGENCE` decision was reopened;
`FORMAL ACCEPTANCE` is not granted; `IMPLEMENTATION CONFORMANT` is not established; test execution
is not authorized and `TEST EXECUTION = SUSPENDED` stands.

### 9.8 R1 has no independent review, and that is the only thing left

`§3` carries `PENDING` on exactly one row: R1 Claim identity. Every other row is either `PASS` or
has an applied fix whose blocking findings are now closed. R1's application was recorded in `§9.1`
and its consumer text was never challenged — but "never challenged" is not `PASS`, and §5 requires
an independent reviewer to check the applied Blob. So the disposition cannot become `PASS` on the
strength of the other seven rows.

The R1 targets, read at the pin above:

```
docs/en/02-domain-model/domain-model-overview.md  1a1a10b24d68dbc2de20cbe4cd6419a7ca037bed  28507 B
docs/zh-CN/02-domain-model/domain-model-overview.md  8ef976789af64afc5e02e8dbdeb2b5f7e1f3df58  25636 B
02-domain-model/domain-model-overview.md  5b86fe23ab7c670b4ae13331b56572aee35f5d00  26974 B
docs/en/02-domain-model/phase-1-domain-model-freeze.md  1a18c6b8424c939dd90986527a24807c8f74d552  5946 B
docs/zh-CN/02-domain-model/phase-1-domain-model-freeze.md  408a606c44fcf271f265508bc9d3029f8fc889cb  5553 B
02-domain-model/phase-1-domain-model-freeze.md  d1102a0adf32e3f7b3eb9091758823f990a2a37c  10457 B
docs/en/03-memory-brain/memory-versioning.md  4efbd26db9586f6fcf1897f42ffba287d625b903  49348 B
docs/zh-CN/03-memory-brain/memory-versioning.md  5ff17ab6cb561407806fe63e1b5aa18f399cbed1  45301 B
docs/en/04-memory-compiler/extraction-and-normalization.md  e6aad4b7504fa61fd0feb8b1da7aa8801103bc60  26256 B
docs/zh-CN/04-memory-compiler/extraction-and-normalization.md  8dd0b5b29ecd37ceac6750c4ad8fa07c1c46cb4c  25185 B
```

Note the third row. `02-domain-model/domain-model-overview.md` exists at repository root alongside
`docs/en` and `docs/zh-CN`. Its Blob is `5b86fe23ab7c`, which is the value `§9.1` records as the
result of the R1 correction on that path, produced by `778d1bee`. The root copy is therefore not
stale on Claim identity: it was corrected in the same round, and the value it superseded was
`443b35b288fc`, produced by `961d2191bb`. What differs is that the root copy has not moved since,
while `docs/en` advanced to `1a1a10b24d68` in a later round.

Whether the root copy is a legitimate third authoritative copy, a mirror, or dead weight remains a
question `§9.1` recorded but did not resolve: it noted the root-level freeze file has no row in
`§8` at all and that the root-level `context-versioning.md` appears only as a "not applied" bullet.
That is a governance question about which copies are authoritative, and an application round may
not decide it alone.

### 9.9 R1 first independent review, and a factual error this round made

Reviewer: independent session `6b01353c-6468-83e8-8158-9aa8750e05c2` (read-only, no repository
write, no comment posted by the reviewer). Verdict returned 2026-11-21. Read-back pin:
`b752aad0fc0f5cd1525c35515b01d2acd990c438`. Verdict: `REQUEST CHANGES`, two findings.

| Item reviewed | Verdict | Blocking finding |
|---|---|---|
| R1 open-clause removal completeness | REQUEST CHANGES | R1-01 |
| No over-deletion of items that must stay `OPEN` | PASS | — |
| Three-copy consistency | PASS on Claim identity | — |
| Claim identity semantic self-consistency | PASS | — |
| Bilingual equivalence | PASS | — |
| `§9.1` R1 row truthfulness | REQUEST CHANGES | R1-02 |

**R1-01 — the root-level freeze still treats Claim identity as unverified.** In
`02-domain-model/phase-1-domain-model-freeze.md`, `§2.6` states that the Claim identity semantic
classification is `DECIDED FOR CONVERGENCE` and that only the ID generation algorithm remains
`CANDIDATE`; `§7` lists `ID generation: CANDIDATE` and six other open items. But `§6`'s DM-10
acceptance row read `未验证的 ID/Claim identity 等不被实现偷偷冻结` — putting the decided Claim
identity back into the unverified set alongside the undecided ID generation. An implementer reading
only the acceptance table cannot tell whether Claim identity must still be kept open. This is the
root-level freeze only; the EN and ZH copies do not carry the row in that form.

The fix scopes the unverified set to the still-open items and states that the decided Claim
identity and ClaimRevision semantics must not be treated as unverified. `§2.6` and `§7` are
untouched, so the three statements in that file now agree.

**R1-02 — `§9.8` misdescribed the root Overview Blob, and that error was mine.** `§9.8` said the
root-level `02-domain-model/domain-model-overview.md` "still carries Blob `5b86fe23ab7c` — the
pre-R1-correction value". That is false. `§9.1` records `5b86fe23ab7c` as the *result* of the R1
correction on that path, produced by `778d1bee`, and the value it superseded was `443b35b288fc`.
The reviewer verified this by reading the `778d1bee` diff, which replaces the old
`ClaimId identity policy across Memory versions remains OPEN` sentence with the decided
`ClaimRef is stable across Memory versions` formulation.

What actually differs between the copies is that the root copy has not advanced since that
correction, while `docs/en` moved to `1a1a10b24d68` in a later round. This round's L0 read
"different Blob" as "not yet corrected" and wrote a claim `§9.1` already contradicted two sections
earlier. `§9.8` now states the correct provenance and keeps the separate governance question —
which copies are authoritative — as unresolved.

The reviewer also checked, independently and at the `§9.1` baseline `dd4ecf16`, that all eleven
Blobs `§9.1` registers match, and that the six producing commits it names do touch the files it
says they touch. It further accepted the two qualifiers `§9.1` uses (`not in §8` for the root
freeze, `(§8 bullet)` for the root context-versioning) as honest descriptions of where those
files were or were not registered, not as cover for omissions.

On the question this round specifically asked: the reviewer's answer is that the root copy is not
stale on Claim identity, so three-copy consistency passes on that content, and that whether the
root copy carries independent normative authority stays an owner decision. R1-01 is a different
matter — a real residue in a different root-level file, and therefore a genuine R1 blocker.

| Target | Blob before | Blob after | Size |
|---|---|---|---|
| `02-domain-model/phase-1-domain-model-freeze.md` | `d1102a0adf32` | `5e30c5b6c68f` | 10457 -> 10595 B |
| `docs/en/00-governance/aid-2026-014-r3-correction-status.md` | `f2ef0f80b707` | `9a757ffc14e7` | 50375 -> 50493 B |
| `docs/zh-CN/00-governance/aid-2026-014-r3-correction-status.md` | `319409a40cf3` | `5fcac6d7c60f` | 45786 -> 45878 B |

R1 therefore moves from `FIX_APPLIED_AWAITING_REREVIEW` to
`APPLIED_PENDING_INDEPENDENT_REVIEW`, with the independent-review column still `REQUEST CHANGES`
until the two findings are re-reviewed. `§2` is unchanged.

### 9.10 Read-back of the predicate-equivalence round

This section records the post-merge read-back for the R7 predicate-equivalence correction reviewed in REREVIEW-8.

It records repository state and content identity only. REREVIEW-8 = PASS is not FORMAL ACCEPTANCE and does not establish implementation conformance.

#### 9.10.1 Exact correction heads

| Target | Reviewed correction HEAD | Correction |
|---|---|---|
| PR #410 — Extraction EN | `a685aa9d868b56afb0a335a691d1e758d1fff05a` | `TRUE if and only if` |
| PR #411 — Storage ADR EN | `79a4d7df475c03ccb318712ccef6e6d78fedebba` | `TRUE if and only if` |

The two correction commits each replace the predicate connector in one existing English definition. The Chinese definitions already use `当且仅当`.

#### 9.10.2 Exact merge targets

| Target branch | Merge commit |
|---|---|
| `main` — PR #410 | `f1a6028d8192` |
| Storage carrier branch — PR #411 | `356e2f051def` |

These are separate Git histories and must not be represented as one common atomic Git snapshot.

The Extraction files are read from the specified `main` merge result. The Storage ADR is read from its separate carrier branch merge result.

#### 9.10.3 Post-merge Blob read-back

The Blob values below are pinned to the R7 merge result (`main` `f1a6028d`).
They are historical read-back values and do not describe the current `main` HEAD,
which has since been advanced by later governance rounds.

| Normative carrier | Path | Blob SHA | Size |
|---|---|---|---:|
| Extraction EN | `docs/en/04-memory-compiler/extraction-and-normalization.md` | `c87860706313` | 22,484 bytes |
| Extraction ZH | `docs/zh-CN/04-memory-compiler/extraction-and-normalization.md` | `9657949af482` | 21,781 bytes |
| Storage ADR (EN/ZH) | `reviews/storage-consistency/phase-3.8.2-storage-serialization-topology-adr.md` | `62ae6e878657` | 35,544 bytes |

The complete Blob identifiers are recorded by the post-merge read-back:

- Extraction EN: `c87860706313`
- Extraction ZH: `9657949af482`
- Storage ADR: `62ae6e878657`

#### 9.10.4 Predicate-equivalence read-back

The four normative definitions are:

1. Extraction EN §19.2.
2. Extraction ZH §19.2.
3. Storage ADR EN §8.8.
4. Storage ADR ZH §8.8.

The read-back confirms the following correspondence:

| Predicate element | English | Chinese |
|---|---|---|
| Predicate identity | `DependencyClosurePersisted(P)` | `DependencyClosurePersisted(P)` |
| Logical connector | `if and only if` | `当且仅当` |
| Dependency set | Complete direct and transitive set | 完整 direct 和 transitive 集合 |
| Completeness | `COMPLETE` | `COMPLETE` |
| Digest | Matches the exact dependency set | 与准确依赖集合匹配 |
| Confirmation | Authoritative read-after-commit | 权威 read-after-commit |

The English and Chinese definitions express the same necessary-and-sufficient conditions.

The participant barrier MUST be resolved or completed only when the predicate is TRUE.

#### 9.10.5 Review and governance disposition

```text
REREVIEW-8 = PASS

FOUR-WAY PREDICATE CONSISTENCY = PASS
LOGICAL EQUIVALENCE = PASS
SCOPE VIOLATION = NONE
REGRESSION = NONE
RESIDUAL REVIEW BLOCKER = NONE

R1-R5 = PASS / NOT REOPENED

FORMAL ACCEPTANCE = PENDING
IMPLEMENTATION CONFORMANCE = NOT ESTABLISHED

TEST EXECUTION = SUSPENDED
TEST EXECUTION DISPATCH GATE = UNLOCKED-WITH-CONDITIONS
UNLOCKED SCOPE = REQ-04 STEP 5 DISPATCH SPEC ONLY
```

The `R1-R5 = PASS / NOT REOPENED` line above is M27's verdict at the REREVIEW-8 point in time.
R1 was subsequently reviewed on its own in `§9.9` and returned `REQUEST CHANGES` (R1-01, R1-02).
For R1, `§9.9` governs.

The PASS decision is an independent review disposition. It is not an acceptance decision.

The read-back does not demonstrate that the underlying storage implementation provides atomicity, transaction isolation, durable dependency registration, or any other implementation property.

No Schema, DDL, public API, H Wire, production key, Trust Root, Crypto Profile, or Storage L4 approval is granted by this section.

This section records a completed normative read-back, not a completed implementation test.
