---
document_metadata:
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-25"
      last_verification_note: "Exact GitHub Issue comment IDs were read back; all 20 were found and all acceptance checklist boxes remained unchecked. Exact-head CI and semantic bilingual review are separate pending gates."
    usage_status: Active
    modification_status: Modified
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Evidence record for AID-2026-093"
    canonical_scope_id: null
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-093 — DECISION-ACCEPTANCE-03 Evidence

`RENUMBERED_AT_MERGE: 2026-11-26` — allocated from current main INDEX immediately before merge preparation.
`RENUMBERED_FROM: AID-2026-092` — provisional branch allocation relinquished because main assigned 092 to PR #1250.
`RENUMBERED_HISTORY: AID-2026-081 -> AID-2026-086 -> AID-2026-092 (provisional) -> AID-2026-093`.

## 1. Scope and authority

`RENUMBERED_FROM: AID-2026-081` — original ID relinquished after the GOV-DOC-001 collision.
`RENUMBERED_FROM: AID-2026-086` — the temporary 086 allocation was subsequently occupied by mainline AID-2026-089 / PR #1232; current ID is AID-2026-093.

Repository Work Item: `AID-2026-093`.

External workflow identifier `AID-2026-11-26-DECISION-ACCEPTANCE-03` is retained only as an external evidence reference; it is not the repository Work Item ID.

The confirmed scope is DEC-01..DEC-20 and the A–I / Storage matrix, representing 18 unique directions. Owner A coordinates. Content Owners are B, D, E, F, G, H and I. Acceptance requires Owner A jointly with the relevant content Owner(s). This evidence record does not itself accept any decision or authorize implementation, deployment or Issue closure; merge is separately authorized by the current user task only after all required checks succeed and branch protection permits it.

Carrier: [PR #1219](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1219). Stage 0 allocation source: [PR #1220](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/1220).

## 2. Exact source Issue comment readback

On 2026-11-25, all 20 expected Issue comments were fetched again by Issue number and exact comment ID. All 20 IDs were found in their corresponding Issue comment collections. Each returned comment body contained 10 unchecked checklist boxes and zero checked checklist boxes.

| DEC trace | Issue | Exact comment ID | Readback | Checklist |
|---|---:|---:|---|---|
| DEC-01 | #1191 | 7174847701 | FOUND | 10 unchecked; 0 checked |
| DEC-02 | #1128 | 7174848562 | FOUND | 10 unchecked; 0 checked |
| DEC-03 | #1103 | 7174849776 | FOUND | 10 unchecked; 0 checked |
| DEC-04 | #1104 | 7174851046 | FOUND | 10 unchecked; 0 checked |
| DEC-05 | #1170 | 7174851977 | FOUND | 10 unchecked; 0 checked |
| DEC-06 | #1174 | 7174852944 | FOUND | 10 unchecked; 0 checked |
| DEC-07 / DEC-09 | #1179 | 7174853922 | FOUND | 10 unchecked; 0 checked |
| DEC-08 | #1177 | 7174854969 | FOUND | 10 unchecked; 0 checked |
| DEC-08 / DEC-09 | #1184 | 7174856082 | FOUND | 10 unchecked; 0 checked |
| DEC-10 | #1209 | 7174856917 | FOUND | 10 unchecked; 0 checked |
| DEC-11 | #1180 | 7174865981 | FOUND | 10 unchecked; 0 checked |
| DEC-08 / DEC-12 | #1212 | 7174866924 | FOUND | 10 unchecked; 0 checked |
| DEC-13 | #1189 | 7174867715 | FOUND | 10 unchecked; 0 checked |
| DEC-14 | #1196 | 7174868513 | FOUND | 10 unchecked; 0 checked |
| DEC-15 | #1208 | 7174869624 | FOUND | 10 unchecked; 0 checked |
| DEC-16 | #1202 | 7174870329 | FOUND | 10 unchecked; 0 checked |
| DEC-17 | #1203 | 7174871193 | FOUND | 10 unchecked; 0 checked |
| DEC-18 | #1197 | 7174871890 | FOUND | 10 unchecked; 0 checked |
| DEC-19 | #1037 | 7174872690 | FOUND | 10 unchecked; 0 checked |
| DEC-20 | #1049 | 7174873458 | FOUND | 10 unchecked; 0 checked |

Result: **20/20 exact comment readbacks PASS; 200 unchecked boxes; 0 checked boxes.** This is evidence that the acceptance requests remain recorded and unaccepted, not evidence of Owner acceptance.

## 3. Unique-direction accounting

There are 20 separately traceable DEC rows and 18 unique directions:

- DEC-16 / DEC-17 are the I and H sub-registrations of one shared file-by-file normative-source restoration direction. Their domain evidence and Owner acceptance remain separately required.
- DEC-19 / DEC-20 are sequential Stage 1 and Stage 2 registrations of one binding-force governance direction. Stage 2 is dependent on Stage 1 and requires a separate explicit authorization.

All other DEC rows represent their own directions. Coverage is register coverage only; it is not implementation or acceptance.

## 4. Bilingual verification boundary

The prior GitHub readback found:
- EN body equality with the canonical body for both the decision register and system matrix.
- ZH-CN structural counts matching the expected 20 DEC rows and 24 invariant rows.
- Metadata counterpart paths present.

The prior readback did not establish complete ZH-CN semantic equivalence. Exact-head bilingual CI after this synchronization and semantic review remain separate checks. No complete bilingual PASS is claimed here.

## 5. Remaining acceptance and governance blockers

- **Historical snapshot before 2026-11-26:** Owner A and relevant content Owners had not recorded exact-version dispositions. The later delegated proxy record now covers all ten roles (3 ACCEPT / 7 CONDITIONAL / 0 REJECT), with explicit non-natural-person attribution; the seven conditions remain open.
- Historical intake snapshot: DEC-12 was PARTIAL before the explicit Owner C confirmation recorded below; current disposition is OWNER_CONFIRMED_GATE_A_PENDING.
- DEC-20 remains BLOCKED pending DEC-19 completion and a separate explicit authorization.
- I-01..I-24 are enumerated, but their per-invariant Authority Owner and Dependent Owners remain NOT_ESTABLISHED; those rows remain BLOCKED.
- Exact-head CI after this synchronization is pending.
- No implementation, normative effectiveness, production conformance, merge or deployment is authorized or claimed.

## 6. Change boundary

This Work Item synchronization changes governance documentation only. It does not modify product/runtime code, tests, schema, migrations, CI workflow definitions or validator logic. No Issue is closed and no acceptance checkbox is checked.


## 6. Exact-head CI results

The following GitHub Actions runs completed on exact PR Head `ca7d7146aa947373e8ac3971e6ac3a7ecd1ef9bf`. All eight workflow runs concluded `success`:

| Workflow | Run | Result |
|---|---:|---|
| Repository hygiene | [45712340510](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340510) | SUCCESS |
| Existing gates | [45712340486](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340486) | SUCCESS |
| Bilingual documentation gate | [45712340478](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340478) | SUCCESS |
| Architecture document management gate | [45712340407](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340407) | SUCCESS |
| Branch freshness | [45712340378](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340378) | SUCCESS |
| Session Evidence Gate | [45712340355](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340355) | SUCCESS — verdict `NOT_APPLICABLE`, because the linked Issues predate the configured effective date; this is not a `PRESENT` session-evidence verdict |
| Runner admission policy | [45712340345](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340345) | SUCCESS |
| Rust Phase 1 Workspace Tests | [45712340334](https://github.com/oahcom/AiMemoryBrainArchitecture/actions/runs/45712340334) | SUCCESS |

The manifest/evidence append itself creates a subsequent PR Head. A fresh CI run is therefore required for that new Head; the eight results above are historical exact-Head results and are not silently carried forward.

## 7. Verification limits

- Bilingual CI passed, but policy manual control M-05 (semantic parity) remains a human review item; CI success is not represented as semantic translation acceptance.
- The Session Evidence Gate returned `NOT_APPLICABLE`, not `PRESENT`; the Work Item's Issue-comment readback evidence is separately documented in §2.
- Local `git diff` commands and standalone local Python gate invocations were not run in this execution. GitHub Actions results above are the CI evidence.


## 8. DEC-12 staged-closure criteria made reviewable

Source direction and acceptance references:
- [Owner C staged-closure direction, #1212 comment 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311)
- [Current-main matrix and explicit do-not-close determination, #1212 comment 7174315211](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174315211)
- [DEC-12 acceptance checklist, #1212 comment 7174866924](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174866924)

The system matrix now defines two independent gates:
- **Gate A — Architecture Review closure:** exact-version review package; complete DEC trace and flow/invariant mapping; exact canonical source pins; bilingual semantic and stable-ID parity; Owner C acceptance of the review package; Owner A coordination; and authority-specific acceptance by every relevant domain Owner and Storage/Consistency. Implementation/production rows may remain explicitly BLOCKED / NOT VERIFIED and must remain so.
- **Gate B — Production Integration / Conformance:** separate integrated build identity; D/E/F/G/H/I contract conformance; Storage atomicity/durability/crash/restore evidence; positive and negative end-to-end tests; production environment identity where applicable; and separate acceptance by relevant domain Owners, Storage/Consistency and Owner A.

**Owner C confirmation recorded (2026-11-26; attribution: `user-authorized operator (delegated by account owner)`):** “I confirm that the Architecture Review workflow may be marked CLOSED once Gate A's exact-version review-artifact and cross-Owner acceptance criteria are met, even if implementation or Production Integration/Conformance rows remain BLOCKED / NOT VERIFIED; such review closure does not constitute, imply, or waive the separate Gate B production acceptance.”

Current disposition: **OWNER_CONFIRMED_GATE_A_PENDING**. The staged closure rule and ten proxy role dispositions are recorded, but the seven conditional reservations, exact-version composition artifact, source pins and full-package bilingual parity remain open. #1212 remains OPEN until Gate A is complete. Gate B production acceptance remains separate; no production acceptance or closure is claimed.

## 9. I-01..I-24 proposed Owner mapping

The system matrix now contains a row-by-row proposal for every invariant in the pinned source 00-governance/architecture-invariants.md blob 50566d16ee57c7ee34f8f089a1dea41260ee37b6.

- Proposed Authority Owner: 24/24 rows (100%).
- Proposed Dependent Owners: 24/24 rows (100%).
- One-sentence rationale: 24/24 rows (100%).
- **Historical snapshot (superseded 2026-11-26):** every mapping was labeled PROPOSED at initial intake. The current delegated adjudication and proxy dispositions are recorded in the matrix and decision register; the historical proposal remains preserved there.
- **Historical snapshot (superseded 2026-11-26):** all 24 invariant rows were BLOCKED while mappings were unresolved. Current row-level traceability is 24 VERIFIABLE; exact-version conditions and composition evidence remain open.

The ZH-CN mirror carries the same 24 IDs and proposed responsibility semantics. This synchronization does not close #1212, check any Issue acceptance box, authorize implementation, or claim production conformance.


## 9. 2026-11-26 delegated cross-Owner dispositions and Gate A reconciliation

Authority: `user-authorized operator (delegated by account owner)`; date: `2026-11-26`. The human Owner expressly authorized the same session to represent all listed Owner roles. The matrix and decision register now contain ten role-specific proxy dispositions: 3 ACCEPT, 7 CONDITIONAL, 0 REJECT. Each row explicitly says the disposition is proxy-recorded and not signed by a natural-person Owner. The natural-person/platform Owner acceptance count therefore remains 0; the proxy dispositions are not misrepresented as individual signatures.

The Gate A role-disposition artifact is recorded. The seven conditions remain open: Owner A composition/bilingual package; D/E/F/I source restoration and exact pins by IMPL2; H idempotency namespace/replay reconciliation; and Storage/Consistency physical transaction/durability/recovery evidence. Full composition review, full-package bilingual/source-revision parity and DEC-13 approval evidence also remain open. DEC-12 remains OWNER_CONFIRMED_GATE_A_PENDING; Gate A PARTIAL / OPEN; Gate B NOT VERIFIED; #1212 OPEN.

Source restoration ownership for missing normative roots/contracts is assigned to **IMPL2**. D/E/F/I validate their own domain semantics after IMPL2 supplies exact source pins; they do not duplicate-claim the restoration task. Storage/Consistency retains its own contract review responsibility.


## 10. 2026-11-26 latest-main reconciliation and matrix defect correction

**Attribution:** `user-authorized operator (delegated by account owner)`; date `2026-11-26`. All actions and proxy records in this section are agent-recorded, not signed by a natural-person Owner.

- PR #1221 is merged at `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706`; the current PR base and merge base both resolve to this main SHA. The PR #1219 pre-correction Head `2fc8ee702b0561f886e19f027d030cff3bef0e02` compared as **127 ahead / 0 behind** (not 1/0); no claim of 1/0 is made. Its ten-file PR diff does not overlap the 22 paths changed by #1221, so no path-level conflict exists.
- Current main `00-governance/architecture-invariants.md` Blob is `a5a51937133d43585d970cad02dcfd20925078d9`. The 24 invariant statement rows are text-identical to the prior pinned content `50566d16ee57c7ee34f8f089a1dea41260ee37b6`; the current blob includes #1221's metadata update. All canonical/EN/ZH-CN matrix source pins are updated to the current Blob.
- The current Invariants metadata is `decision_status: Under-Review`, approver/date `NOT_RECORDED`, `approval_applicability: Not-Applicable-To-Current-Version`, evidence `Unverified`, `usage_status: Active`, `modification_status: Pending-Reapproval`, `normative_status: Normative`. PR #1221 amended GOV-DOC-001 §4.3.1 to state that Normative content remains binding during Pending-Reapproval. The Invariants body still says CANDIDATE / NOT APPROVED and subject to a separate approval decision; DEC-13 records no formal approval. No formal approval is inferred. The body/metadata-policy binding-force tension is explicitly retained as an OPEN Gate A / DEC-13 item rather than silently adjudicated here.
- The canonical and EN matrices contained literal `undefined` values in the per-invariant proxy-disposition cells for I-01…I-24 (Authority Owner and first Dependent Owner). These were serialization defects, not unresolved decisions. The cells are corrected from the already recorded ten-role disposition register: B/C/G=ACCEPT; A/D/E/F/H/I/Storage-Consistency=CONDITIONAL. All 24 rows now show explicit values; no role disposition was changed. ZH-CN already contained the explicit values and is retained with the updated source pin and policy-status explanation.
- The old PROPOSED table remains explicitly historical; the later OWNER_CONFIRMED table is authoritative for current responsibility mapping. Current mapping state remains 24/24 OWNER_CONFIRMED, 24 VERIFIABLE, 0 BLOCKED_WITH_REASON. Exact-version domain Owner acceptance remains pending; proxy disposition is not natural-person signature.
- Historical identifier audit at the time of section 10 considered AID-2026-086 available. That allocation was later superseded when main registered AID-2026-089 from AID-2026-086 in PR #1232; the current allocation is recorded in section 14. Global branch-content uniqueness remains explicitly not exhaustively verified.
- Prior Head `2fc8ee702b0561f886e19f027d030cff3bef0e02` had all 16 required checks SUCCESS (the exact job-level results are reported in the PR description); the reconciliation commit creates a new Head and requires a fresh 16-check run. No prior-Head result is carried forward.
- #1212 remains OPEN. Gate A remains PARTIAL / OPEN; Gate B remains NOT VERIFIED. No Issue acceptance checkbox is checked, no implementation/deployment is authorized, and no runtime/validator semantics are changed.


## 11. 2026-11-26 concurrent-main refresh after PR #1240 and #1245

- After the matrix correction commit, main advanced from `dc826e4eae381d78a9fc4b1fcbb2cbc783ed2706` to `8d90843aec4583c3282a3b45da31c7d6fd734cf2` through PR #1240. That change updated the AID-2026-080 evidence/manifest and repaired its INDEX row. The branch merged it as second parent `8d90843aec4583c3282a3b45da31c7d6fd734cf2` in merge commit `df286ec19b48eda6a4f1338a1ef2aae5cfcbc1f7`. The INDEX was manually reconciled: current-main AID-2026-080 and AID-2026-081 rows retained; the branch's single AID-2026-086 row appended. The main AID-080 files were imported unchanged.
- Main then advanced once more to `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8` via PR #1245. Its only changed path is `14-ai-development/work-items/I-OWNER-DECISION-AUTHORIZATION-DECISION-001.md`, which does not overlap this PR. Immediately before this merge, the branch compared as 129 ahead / 1 behind, with merge base `8d90843aec4583c3282a3b45da31c7d6fd734cf2`. This commit imports the PR #1245 file unchanged and uses `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8` as its second parent; post-merge compare is to be read back.
- The latest main refresh changes no decision matrix semantics, invariant source, AID-2026-086 registration, or runtime/validator behavior. #1221's source reconciliation and the 24-row disposition correction remain intact.
- This latest-main merge creates a new exact PR Head; no prior-Head CI result is carried forward. The full 16-check suite must complete successfully on that resulting Head before merge.
- Attribution remains `user-authorized operator (delegated by account owner)`; proxy registration, not a natural-person Owner signature. #1212 remains OPEN; Gate A PARTIAL / OPEN; Gate B NOT VERIFIED.


## 12. 2026-11-26 branch-history normalization for one-ahead/zero-behind

- Before normalization, current main was `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`; PR head was `590ddcb5f2f3a78f74dee5d33f4b3c82888d8e10`; GitHub compare was 130 ahead / 0 behind, merge base exactly current main.
- The user explicitly requested a final `1 ahead / 0 behind` branch state. The complete PR tree (including latest main, AID-080/AID-081 records, AID-086 registration, three matrix languages, register translations, manifest and evidence) was retained; the branch was normalized to one net documentation commit directly on current main.
- **Force-with-lease ref update succeeded:** old Head `590ddcb5f2f3a78f74dee5d33f4b3c82888d8e10` → normalized Head `9b7f0fa843eddac3675c5f8374dc736e3af64098`, parent `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`. GitHub compare on that Head confirmed exactly **1 ahead / 0 behind**, merge base `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`. The evidence correction below is a new direct child of the same main SHA and preserves the same one-commit-ahead graph.
- The update used an expected-old-Head lease and did not bypass branch protection.
- The branch contains no runtime code or validator semantic changes. The final exact Head requires a fresh 16-check run; no earlier CI result is carried forward.


## 13. 2026-11-26 manifest authorization and identifier-marker consistency

- The manifest baseline fields `base_commit_sha` and `repository.baseline_commit` now point to current main `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`, replacing the original task-start baseline `6314a65bd8be48c1a4bb0768e9960c4c808110ab`; the historical baseline remains recorded in earlier evidence snapshots.
- The current user task explicitly authorizes merge after the 16 required checks pass and branch protection permits it. The manifest's `authority.merge_authorization` and lifecycle merge state now reflect that conditional authorization. Implementation, decision ratification, deployment and Issue closure remain unauthorized.
- The original renumbering marker appears exactly once at its original registration location; later references describe it without duplicating the marker.
- The prior normalized Head `9b7f0fa843eddac3675c5f8374dc736e3af64098` was confirmed by GitHub as 1 ahead / 0 behind. This correction commit is also a direct child of main `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8`; the resulting Head is re-read after the ref update.


## 14. 2026-11-26 latest-main refresh, second identifier collision and D/Storage boundary reconciliation

**Attribution:** `user-authorized operator (delegated by account owner)`; date `2026-11-26`. This is proxy registration, not a natural-person Owner signature.

- Main advanced from `515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8` to `d914e8a1f8a1ba24c21c41a9249489d544388185` (66 commits). Immediately before refresh, PR #1219 Head `6739452da77c809befd2a1b8dade4eaf94cc91e0` was 1 ahead / 66 behind; previous exact-Head 16/16 CI success is stale and is not carried forward.
- Main now contains AID-2026-089 / PR #1232, whose INDEX and PR body record a renumber from AID-086. The prior AID-086 allocation for this PR therefore collides with a mainline work item and is relinquished. AID-087/088 are occupied; AID-090 is allocated by PR #1220/#1241/#1248; AID-091 is allocated by PR #1242. Exact-token Issue/PR searches, branch-name searches and the current main tree/index show no AID-2026-093 allocation. This Work Item is now AID-2026-093. The original AID-081 renumber marker is preserved, and the second renumber from AID-086 is recorded above. Full content scanning of every branch is not exhaustive.
- Current main `01-system-architecture/forget-fence-and-completion-contract.md` is Blob `760a1d48011f2a66c23abcf825a3d067e79b8821`, metadata Draft / Unverified / Informative. It records D as sole logical ForgetOperation / ForgetFence authority and Storage-local fence rows as rebuildable D-derived projections; Storage retains physical durability, atomic visibility, backup/restore, recovery, replication and anti-rollback realization. This is a direction/source record, not normative approval, Owner acceptance or implementation evidence.
- Current main `01-system-architecture/system-boundaries.md` is Blob `c2aa6823b69313ba27c34625f87f29d2be356606`, metadata Draft / Unverified / Normative. It assigns D canonical Forget mechanics and the D-domain completion predicate; I retains global policy, target inventory and global completion criteria, with joint completion evidence from D and relevant execution Owners. No unilateral completion authority is created.
- The matrix's D Forget Fence flow and DEC-10 / DEC-15 source references are updated to pin both current-main documents and their actual metadata states. Storage is described as enforcing physical visibility through D-derived projections, without independent generation/cursor or publication authority. The former statement that the D Fence source was absent on main is removed. The D canonical-store normative source remains absent; E compiler contracts, F retrieval root, I security-governance root and Storage physical transaction/durability contract remain missing or unpinned. D/Storage exact-version acceptance and implementation remain pending.
- The current Invariants Blob remains `a5a51937133d43585d970cad02dcfd20925078d9`; all 24 invariant statements and the 24/24 OWNER_CONFIRMED responsibility mapping remain unchanged. The 10 role dispositions remain 3 ACCEPT / 7 CONDITIONAL / 0 REJECT, with zero natural-person Owner signatures.
- The INDEX row, manifest `work_item_id`, evidence record and manifest-schema registry now use AID-2026-093. The prior AID-086 directory is not carried into the new tree; the main AID-089 record and AID-081 record are preserved unchanged.
- The new branch commit is created directly on latest main `d914e8a1f8a1ba24c21c41a9249489d544388185`; the resulting ahead/behind state is read back after the ref update. Fresh exact-Head 16-check CI is required before merge. #1212 remains OPEN; Gate A PARTIAL / OPEN; Gate B NOT VERIFIED.


## 15. 2026-11-26 third identifier collision reconciliation

Current main after PR #1250 is `587d7ca9731e50c7a4c8c9df424798f555e0a2db` and assigns AID-2026-092 to PR #1250. The branch's provisional AID-2026-092 is relinquished before merge. Current Work Item ID is AID-2026-093. Earlier IDs AID-2026-081 and AID-2026-086 remain preserved as historical renumbering markers. This is proxy registration by `user-authorized operator (delegated by account owner)`; 代理登记，非自然人 Owner 签署.
