# A Independent B5 Source Audit — DOMAIN-REALITY-001-B

- Finding set: `A-B5-INDEP-001`
- Review date: 2026-11-18 (source snapshot read 2026-11-17 UTC / 2026-11-18 JST)
- Reviewer role: A integration evidence review; not B Owner approval and not an external independent auditor.
- Current main: `b3c666e67982cb3d3374e759cfb6552c7765aacb`
- Current main tree: `7096e0bc3fdc9a390fccff388f9261522fa424f2`
- B branch: `research/domain-reality-001-b`
- B branch HEAD and PR #55 head: `138be006ae6874ef44be47f2c8a1aebe96af4314`
- B PR #55: OPEN / DRAFT; base ref `main`; base SHA `052715487bd5e95aab8b9bb386c162cf2d6bf6d3`; compare against current main: DIVERGED, 145 ahead / 32 behind; GitHub metadata currently reports mergeable=true.
- B README Blob: `af10e810aaff96537afc731af07d322f2c050d1e`
- B currentness audit Blob: `4bc2d7339bdb7431393c449036fd374d2403f992`
- B bilingual parity audit Blob: `710df4a0170c3bb762297a81beacb80845719330`

## 1. Executive result

**B5 remains BLOCKED / NOT PASSED. B6 remains INDEPENDENT_REVIEW_PENDING. B0 remains PARTIAL / NOT PASSED.**

The B research branch exists and contains the 22-file DOMAIN-REALITY-001-B package, including its bilingual audit. The removal of the audit from main did not remove it from the B research branch. The live branch and PR were read directly.

This review did not approve the candidate canonical model, close Fact/Claim, accept any cross-owner contract, authorize schema freeze, or establish runtime/production readiness.

## 2. Confirmed findings

### A-B5-001 — Currentness metadata is stale in the B README and baseline audit

Severity: HIGH  
Blocking: B0 current-source closure and B5 evidence-readiness  
Owner: B (source correction); A (re-read and integration status)

Live facts:
- B branch HEAD / PR #55 head is `138be006ae6874ef44be47f2c8a1aebe96af4314`.
- Main HEAD is `b3c666e67982cb3d3374e759cfb6552c7765aacb`.
- README Blob `af10e810...` still records main `901e38...` and an earlier B branch HEAD `ec5bcc451554f6e7caf513e98427a6b7b7f13c81`.
- `baseline-currentness-and-owner-source-audit.md` Blob `4bc2d733...` records main `901e38...`, branch HEAD `5797ff44db7e3fdbc0820a08e91ff78f76c4faac`, and PR #55 head `dc05436aaa75a90c70aa3137dcdfadc49cf7e6dd`. All three are superseded by the live refs above.
- PR #55 compare against current main is DIVERGED, 145 ahead / 32 behind. The branch's historical merge base is `b372b62c640a2b656e54b6db62a4ee67d7d8c001`. GitHub currently reports mergeable=true, which is not a semantic or source-currentness acceptance.

Impact: readers cannot use the README/currentness audit as a current branch/PR snapshot. A branch being mergeable does not make the 32-commit divergence or old source ledger disappear.

Closure:
1. B refreshes the README and currentness audit with the same exact main HEAD, B branch HEAD, PR head/base SHA, compare status and counts.
2. B states whether it intends to rebase/retarget or retain the historical branch; A does not perform that Owner branch action.
3. A independently re-reads the corrected Blob and live PR/branch metadata.

### A-B5-002 — Three file-level Blob pins in the bilingual audit are stale

Severity: HIGH  
Blocking: B5 final exact readback and traceability  
Owner: B (audit maintainer); independent reviewer (verification)

The live file Blob values were fetched from `research/domain-reality-001-b` and compared to the corresponding exact Blob recorded in the bilingual audit's file table:

| File | Audit-recorded Blob | Live Blob | Result |
|---|---|---|---|
| `README.md` | `a77061e0032d771e704e04f1a3ea081c0368ab87` | `af10e810aaff96537afc731af07d322f2c050d1e` | MISMATCH |
| `baseline-currentness-and-owner-source-audit.md` | `6183923c6d90b3eaf0b471e6707b2e3e21659e36` | `4bc2d7339bdb7431393c449036fd374d2403f992` | MISMATCH |
| `evidence/official-reference-validation.md` | `610a4480b483bac668ab26bbb7ef0505029412e2` | `ef4a0cf448e474b08bf5ff6b80c32dbae705b002` | MISMATCH |

The remaining 18 core/supplemental file pins in the 21-file comparison sample matched the audit table. This is a bounded exact-pin check, not a full 22-file semantic parity audit. The parity audit's own Blob is separately pinned above.

Impact: the audit's file-level evidence index is not fully synchronized with the branch state. A reviewer following the three old pins will not inspect the current contents.

Closure:
1. Update the three rows to their exact live Blob SHAs, or explicitly mark them as historical and add current pins.
2. Re-fetch all 22 package files after the final write and compare every recorded Blob.
3. Publish a final source ledger that binds branch HEAD + path + Blob for every file.

### A-B5-003 — Bilingual audit contains conflicting self-status statements

Severity: HIGH  
Blocking: B5 status integrity  
Owner: B (audit maintainer); independent reviewer (status parity)

Observed in `bilingual-parity-audit.md` Blob `710df4a0...`:
- Section 2's row for `bilingual-parity-audit.md` says `PARTIAL`, with the file-by-file table and status/action cells English-only.
- Section 2A says the English audit table and per-file table have Chinese mirrors and marks the file `REMEDIATED — INDEPENDENT REVIEW PENDING`.
- Section 3 says Chinese peer text has been added to all 22 files, including the audit table.
- Section 5 still says B5 is blocked pending independent clause-by-clause review.

The final B5 disposition is consistently blocked, but the audit's file-level remediation state is not. It is unclear whether Section 2 is an obsolete snapshot, whether Section 2A supersedes it, or whether part of the audit table remains untranslated.

Impact: the audit cannot serve as a single authoritative file-level parity register until the conflicting rows are reconciled.

Closure:
1. Explicitly label superseded snapshots or remove/replace stale status rows.
2. Use one controlling per-file status and exact Blob per row.
3. Distinguish author-side translation, manual parity review, independent semantic acceptance and final readback as separate states.
4. Re-read the full audit after correction.

## 3. Current B gate interpretation

The live README and source audit support the following conservative interpretation:
- B0: PARTIAL / NOT PASSED.
- B1: IN PROGRESS.
- B2: IN PROGRESS; Fact/Claim identity remains a decision request.
- B3: NOT PASSED; owner acceptance and successor-pin reconciliation remain open.
- B4: NOT READY; specification only, no authorized executable schema/test result.
- B5: BLOCKED / NOT PASSED.
- B6: INDEPENDENT_REVIEW_PENDING.

The B Fact/Claim ADR is explicitly `CANDIDATE / DECISION REQUEST — NOT DECIDED, NOT ACCEPTED, NOT SCHEMA-FROZEN`. Its C2 + I1 recommendation must not be promoted to a B decision or consumer adoption. The current model's owner boundaries remain candidate semantics; D/E/F/G/H/I/Storage retain their local authority.

The research package explicitly states that schemas and executable tests have not been authorized/run, and that Issue #7 leaves the canonical runtime repository/accountable engineering owner unresolved. This report therefore makes no implementation or production claim.

## 4. Evidence boundary and limitations

- This review directly read B README, baseline currentness audit, bilingual parity audit, Fact/Claim ADR, decision register, conflict register, identity/state/temporal/relationship model files and the current PR/branch metadata.
- Exact Blob matching was performed for 21 listed package files; 3 mismatches were confirmed, 18 matched. The full package was not semantically compared clause by clause.
- No B Owner approval is inferred from the research branch or PR description.
- No CI pass, schema validation, executable conformance, merge, Gate passage or production authorization is claimed.
- The A reviewer's role is integration evidence assessment, not a substitute for a separate independent reviewer or B's decision authority.

## 5. Required next actions

1. B corrects A-B5-001 through A-B5-003 on its own branch and republishes exact readback evidence.
2. An independent reviewer performs clause/row-level semantic comparison across all 22 files, including the audit itself and all normative tables, IDs, fields, enums, statuses, examples and owner boundaries.
3. B publishes an explicit Fact/Claim ADR decision only after the required authority and consumer acceptance; otherwise it remains ADR-BLOCKED.
4. A re-reads the corrected B branch and updates G1/G6/G7 only against exact current evidence.

No calendar deadline is invented. These findings must close before B5 can pass or any B-dependent schema/contract freeze is considered.

## 6. Disposition

**B5 BLOCKED / NOT PASSED. B6 INDEPENDENT_REVIEW_PENDING. B0 PARTIAL / NOT PASSED.**

This is an A integration review artifact on the A review branch. It is not a B Owner decision, not an independent external audit, and not a canonical model freeze.
