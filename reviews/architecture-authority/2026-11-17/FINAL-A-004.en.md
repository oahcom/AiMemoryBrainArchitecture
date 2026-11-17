# FINAL-A-004 — Current-main Baseline Correction and Independent Review Addendum

- Authority: A integration assessment; no Owner authority is substituted.
- Date: 2026-11-17
- Controlling main HEAD at this addendum: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Content tree: `7096e0bc3fdc9a390fccff388f9261522fa424f2` (identical to the tree at `901e38...`; subsequent add/delete cleanup commits changed history but restored the same tree).
- Previous baseline parent: `ca69d50d1fc6c19a930128de700b0f2328bf32fb`
- Change: `revert(domain): remove research-only bilingual audit from main`
- A review branch: `review/session-4-a-final-architecture-authority-current-2026-11-17`
- Supersedes: FINAL-A-003 only for current-main freshness and B-audit availability; it does not erase prior findings or Owner decisions.

## 1. Baseline correction

The previous FINAL-A-003 baseline `ca69d50d1fc6c19a930128de700b0f2328bf32fb` is no longer current. Main now points to `b3c666e67982cb3d3374e759cfb6552c7765aacb`.

The latest commit removes exactly:
`13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/bilingual-parity-audit.md`
(131 lines; commit file status: removed).

The removed audit Blob previously recorded as `a877ceff906da01e70e277a81b95978982af3ede` is historical evidence only. It is not a file in current main and must not be represented as a current-main source artifact or current B5 closure evidence.

## 2. B5 and G6 disposition

- B5 remains **BLOCKED / NOT PASSED**. The removal of the audit file does not establish that the underlying bilingual defects were corrected; it withdraws that audit file from the current-main evidence set.
- The former audit Blob may be consulted as historical context only after exact readback from its historical commit. It does not prove present source state, B Owner acceptance, consumer adoption, or independent semantic parity.
- Issue #43 G6 remains **PARTIAL / NOT PASSED**. The full A package semantic parity review is not complete, and no system-wide independent bilingual acceptance is inferred.
- B Fact/Claim remains ADR-BLOCKED unless and until B publishes a current authoritative decision and consumers accept its exact version.
- Do not equate B5 (B research-package gate) with Issue #43 G6 (system-wide bilingual gate).

## 3. A package currentness and review boundary

The ten paired A documents (20 files) in this PR retain their historical internal baseline pins. Their shared baseline must not be silently rewritten: the package was authored against its recorded baseline and FINAL-A-003 was the subsequent delta. FINAL-A-004 is now the controlling current-main delta for this review.

Independent review performed in this pass:
- Read back the live PR #60 metadata and all 22 changed-file entries.
- Read the EN/ZH SYS-RISK-002, ARCH-CX-002, DEV-FEAS-002, DEP-DAG-002, PRIORITY-002, READINESS-002, CONFLICT-002, GATE-002, DEFERRED-002 and FINAL-A-002 pairs from the exact A review branch.
- Confirmed that the ten pairs preserve matching document identity and broad decision structure.
- Identified currentness drift: all ten baseline documents and FINAL-A-002 still identify `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`; FINAL-A-003 identifies `ca69d50d1fc6c19a930128de700b0f2328bf32fb`; both are historical relative to current main `901e38...`.


### Finding A-PARITY-001 — PRIORITY-002 P0-05 under-translation (corrected)
The Chinese P0-05 row omitted the English requirements to close A-01..A-05 L1/L2 clarifications, obtain exact D adoption, and then complete L3/L4 physical proof. It had narrowed the action to L4 physical DB/COC/JF-10 proof. This could incorrectly imply that L1/L2 clarification and D acceptance were not part of the priority. The Chinese row has now been corrected on this branch to restore all three requirements. This is one confirmed semantic-parity defect; it does not establish that the remaining pairs are defect-free.

- Full sentence-by-sentence semantic parity, every table cell, and every cross-document status/owner/deadline alignment have **not** been completed. Equal structure is not proof of semantic equivalence.

## 4. R/X/F/D/P refresh dependency

PR #62 was authored against `ca69d50d1fc6c19a930128de700b0f2328bf32fb` and contains a delta that references the now-removed B audit artifact. It is no longer a complete current-main refresh for `901e38...`.

Required corrective action:
1. Reclassify PR #62's original ten files as a historical delta against ca69d50.
2. Publish a bilingual successor delta against main@901e38, explicitly recording the removal of the B audit artifact and the resulting B5 evidence limitation.
3. Keep R/X/F/D/P conclusions bounded to the exact source evidence actually re-read; do not claim the historical audit is current.
4. A re-reads the successor delta and updates G1/G6/G7 only after exact Blob readback.

## 5. Controlling disposition and gates

Overall decision remains **DEFERRED**; architecture state remains **ARCHITECTURE_NOT_READY**.

- G1: PARTIAL; current main is now identified, but all authority-owned source/consumer pins are not fully refreshed.
- G2–G5: BLOCKED.
- G6: PARTIAL / NOT PASSED.
- G7: candidate A integration disposition only; independent acceptance remains outstanding.
- G8: NOT READY.
- JF-10 Gate A: PARTIAL PASS / OPEN; Gate B and Gate C: BLOCKED.
- No Critical risk is accepted or waived.
- COND-NB-01 remains the sole accepted non-blocking capability deferral, limited to Vector/ANN production capability with F ownership and its recorded P2 closure criteria.
- No implementation freeze, schema/technology freeze, merge, Gate release, deployment or production activation is authorized.

## 6. Required next evidence

| Item | Accountable owner | Required evidence | Gate boundary |
|---|---|---|---|
| Current B research/domain source and B5 | B | Current branch HEAD, exact source Blobs, completed bilingual remediation, independent clause/row parity, B Owner decision | Before B-dependent normative freeze; B5 |
| R/X/F/D/P current-main successor | R/X/F/D/P authors; A integrates | Bilingual successor pinned to main@901e38 and all exact source Blobs | G1/G6/G7 |
| A package semantic parity | Independent reviewer | Clause/table/status/ID/owner/deadline parity matrix across all 20 files and FINAL-A-003/004 | G6 |
| Owner/consumer acceptance | Each domain Owner | Exact-version decision and consumer adoption evidence | G2 |
| Physical correctness and operations | D/I/Storage/C/G/H and project authority | Forget/publication, JF-10, Applied, recovery, topology and production operational proofs | G3–G5; JF-10 |

No artificial calendar deadline is assigned where no accountable Owner has accepted one. Closure is due before the dependent normative decision, schema freeze, implementation entry or Gate transition.

## 7. Authority boundary

This addendum is an integration review correction, not a B Owner decision, not a substitute for R/X/F/D/P source-owner approval, and not an independent external acceptance. It does not authorize changes to main or Owner branches.