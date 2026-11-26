---
document_metadata:
  domain: architecture
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version: null
      approval_scope:
        type: Full-document
        included_sections: []
        included_assets: []
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Evidence-tracking artifact; not an Owner acceptance or normative approval."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Canonical
    canonical_scope: "Decision acceptance evidence register"
    canonical_scope_id: "architecture/decision-acceptance-register"
    canonical_scope_keywords:
      - decision-acceptance
      - evidence
      - governance
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md"
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md"
---

# 20-Decision Acceptance Register — AID-2026-11-26-DECISION-ACCEPTANCE-03

> Evidence register only. Directional decisions are not Owner acceptance, normative effectiveness, implementation authorization, implementation verification, or production conformance.
>
> Authority attribution: `user-authorized operator (delegated by account owner)` (delegated operator; not a natural-person signature).
> Owner-specified decision date: 2026-11-26. GitHub registration timestamps may precede that date; preserve the supplied decision date and actual platform timestamp separately.
> Baseline observed: `main` latest commit search result `6314a65bd8be48c1a4bb0768e9960c4c808110ab` (2026-11-25 session observation; recheck before merge).

## Counting and status rules

There are **20 DEC registration records** representing **18 unique directions**. DEC-16 and DEC-17 are the I/H sub-registrations of one shared direction: governed, file-by-file normative-source restoration. DEC-19 and DEC-20 are two ordered stages of one binding-force governance direction. DEC-01…20 remain independently traceable; both pairs retain separate evidence and prerequisite tracking.

Statuses: OPEN = decision recorded, acceptance evidence incomplete; PARTIAL = some composition/document evidence exists but at least one required acceptance gate is absent; BLOCKED = a named prerequisite/authority/evidence gate prevents progress; VERIFIED requires every criterion and every required Owner acceptance. None of these records is marked VERIFIED by this register.

State axes MUST remain separate: Direction Approved; Owner Accepted; Normative Source Effective; Implementation Authorized; Implementation Verified; Production Conformant.

## Decision inventory

| ID | Direction / selected option | Source record | Accountable Owner / dependent Owners | Canonical source / evidence anchor | Independent acceptance criteria | Verification method | Status |
|---|---|---|---|---|---|---|---|
| DEC-01 | MemoryVersion canonical reference manifest — C, hybrid: explicit refs equal canonical derivation; reject mismatch; recompute digest | [#1191 comment 7174300340](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1191#issuecomment-7174300340); [Owner detail 7174521705](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1191#issuecomment-7174521705) | C; B and D dependent | `02-domain-model/core-entities.md`; `02-domain-model/relationships-and-provenance.md`; #1191 | Claim revision refs authoritative; entity/relation/source/provenance/evidence refs deterministic derived projections; commit rejects mismatch; digest recomputed over canonical result; immutable revision refs exact | Exact blob review; derive-vs-supplied positive/negative cases; commit rejection and digest recomputation evidence | OPEN |
| DEC-02 | Partial-Scope MemoryVersion disclosure — B, safe projection | [#1128 comment 7174029131](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1128#issuecomment-7174029131) | B; C, D, I dependent | #1128; MemoryVersion read/disclosure contract (canonical path to be pinned) | Filter Claims and all dependent refs; projection digest distinct from canonical digest; no hidden identifiers or full digest leakage; canonical snapshot immutable | Mixed-scope fixtures; inspect returned refs/digest; positive/negative disclosure tests | OPEN |
| DEC-03 | Claim–Evidence relationship model — C, versioned association object | [#1103 comment 7174030149](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1103#issuecomment-7174030149) | C; B, D dependent | `02-domain-model/relationships-and-provenance.md`; `02-domain-model/epistemic-and-temporal-semantics.md`; #1103 | Canonical independently versioned association carries role/assessment; ClaimRevision pins exact association revision; lifecycle/scope/provenance validated | Type and revision review; exact-pin positive/negative tests | OPEN |
| DEC-04 | Provenance completeness — C, tiered authoritative vs explanatory records | [#1104 comment 7174031071](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1104#issuecomment-7174031071) | C; B, D, E dependent | `02-domain-model/core-entities.md`; `02-domain-model/epistemic-and-temporal-semantics.md`; #1104 | Verifiable canonical record requires target, typed source refs, exact versions, input digests, actor and lineage; incomplete notes explicitly non-authoritative | Field/type review; canonical publication rejection tests; lineage validation | OPEN |
| DEC-05 | Evidence attachability / authorization / retention / Forget — C, orthogonal layered dimensions | [#1170 comment 7174032150](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1170#issuecomment-7174032150); [Owner detail 7174508996](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1170#issuecomment-7174508996) | C; B, D, I dependent | #1170; Evidence and permission/retention/Forget contracts | Availability, authorization, retention and Forget remain independent; combined attach/read decision rules; forgotten/revoked precedence; EvidenceRef remains resolvable after payload erasure | Decision-table review; combination and precedence tests; historical ref resolution | OPEN |
| DEC-06 | Sub-object Forget / immutable history — A history semantics + C dependency-closure execution | [#1174 comment 7174032987](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1174#issuecomment-7174032987); [Owner detail 7174512700](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1174#issuecomment-7174512700) | A (history); C (dependency closure); B, D, I, F/G/Storage dependent as applicable | #1174; #1164 DAG; #1191 manifest; Forget/Fence sources | Historical snapshots immutable and read-time suppressed; governed successor version for surviving current view; dependency closure includes derived objects/caches/indexes/projections; suppression distinguishable from absence; audit evidence | Dependency graph and read-surface inventory; historical/current read tests; derivative cleanup/fence and audit evidence | OPEN |
| DEC-07 | F formal normative source processing — A | [#1179 comment 7174052619](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1179#issuecomment-7174052619); [combined record 7174288361](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1179#issuecomment-7174288361) | A; F, D, E, I, Storage dependent | `05-memory-runtime/` normative root currently absent per #1179 | Candidate design, F Owner acceptance and effective normative source separately recorded; resolve open items; exact per-file source/mirror pins and boundary reconciliation | File inventory; exact blobs; Owner review; governance approval; mainline per-file verification | OPEN |
| DEC-08 | D→E→F Canonical Commit and consumer event — A | [#1177 comment 7174287587](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1177#issuecomment-7174287587); [#1184 comment 7174053488](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1184#issuecomment-7174053488); [#1212 comment 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311) | A; D, E, F, Storage/Consistency joint acceptance | D canonical store source; E producer contract; #1177/#1184/#1212 | Canonical commit and authoritative change event/outbox/receipt share one atomic boundary; auditable linearization point; E projection request references already committed D revision/cursor and creates no canonical truth | Exact contract review; transaction/crash/recovery/replay/idempotency evidence; Storage/Consistency acceptance | OPEN |
| DEC-09 | F watermark and scan coverage proof — A | [#1179 comment 7174060184](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1179#issuecomment-7174060184); [#1184 comment 7174286863](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1184#issuecomment-7174286863) | A; F, D, Storage dependent | F consumer/watermark contract; #1179/#1184 | scanned_through or equivalent contiguous coverage proof; visible/irrelevant/filtered/gap distinct; gap stalls advancement; replay from watermark; last-visible cursor not coverage | Gap/replay/duplicate/out-of-order fixtures; contiguous-prefix proof; exact source pins | OPEN |
| DEC-10 | Forget Fence and derived publication boundary — A | [#1209 comment 7174055125](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1209#issuecomment-7174055125); [#1212 comment 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311) | A; D, E, F, G, I, H where transport involved, Storage/Consistency | D-FORGET-CONTRACT-001 @ `760a1d48011f2a66c23abcf825a3d067e79b8821` (Draft/Unverified/Informative; Owner acceptance pending); System Boundaries @ `c2aa6823b69313ba27c34625f87f29d2be356606` (Draft/Unverified/Normative); #1125/#1211/#1209/#1212 | D-authoritative Fence proof; publication/visibility gate; stale-Fence derivatives cannot publish or re-enter visible paths; each transition has issuer, token, linearization, idempotency and unknown/failure behavior | Transition/race table; stale result, retry, queue/cache/replay/restore and crash tests; per-Owner row acceptance | OPEN |
| DEC-11 | G Delivery and C/H Accepted evidence mapping — B | [#1180 comment 7174054303](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1180#issuecomment-7174054303); [detail 7174289110](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1180#issuecomment-7174289110) | B; C, H, G joint acceptance; D/I inputs as required | ContextVersion Immutability Decision @ `27e9e5f092b17cf4013a533d07949eb73ac6ef4c` (Draft/Unverified/Informative; G acceptance pending); Applied Evidence Contract @ `273efdd1b02bd9302fc968f07c6d094da2582a6e` (Draft/Unverified/Informative; C/G/H acceptance pending); existing `06-memory-context/context-versioning.md`; `07-agent-integration/inference-boundary-model.md`; H BMCP contract; #1144/#1151/#1124/#1135/#1180 | G adds no Accepted state; durable auditable reference to authoritative C/H Accepted evidence bound to stable Attempt; Accepted != Applied; retry/late ACK/Unknown/supersession defined | Exact transition/evidence mapping; durable-link and replay tests; C/H/G acceptance | OPEN |
| DEC-12 | Workflow CLOSED acceptance staged — C (confirmed; Gate A pending) | [#1212 comment 7174051311](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174051311); [matrix 7174315211](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1212#issuecomment-7174315211); acceptance checklist 7174866924 | C; A and every domain Owner; Storage/Consistency | #1212 and focused Issues | Architecture Review Gate A requires exact-version review package, complete flow/invariant traceability, Owner A + relevant Owner acceptances and bilingual/source-revision parity; implementation/production rows may remain explicitly BLOCKED/NOT VERIFIED. Gate B separately requires integrated build, D/E/F/G/H/I conformance, Storage fault/recovery evidence, end-to-end tests and production Owner acceptance. No Gate A closure implies Gate B acceptance. | Owner C confirmation recorded 2026-11-26 (attribution: user-authorized operator (delegated by account owner)): “I confirm that the Architecture Review workflow may be marked CLOSED once Gate A's exact-version review-artifact and cross-Owner acceptance criteria are met, even if implementation or Production Integration/Conformance rows remain BLOCKED / NOT VERIFIED; such review closure does not constitute, imply, or waive the separate Gate B production acceptance.” The ten required Owner-role dispositions are now proxy-recorded on this branch (3 ACCEPT / 7 CONDITIONAL / 0 REJECT); each entry explicitly states that it is proxy-recorded and not signed by a natural-person Owner. The conditional evidence remains OPEN: full exact-version composition review, source restoration/pins, Storage/Consistency physical contract, H idempotency/replay reconciliation, full-package bilingual/source-revision parity and DEC-13 approval evidence. Gate A is PARTIAL / OPEN; #1212 stays OPEN. Gate B production acceptance remains separate and mandatory. | OWNER_CONFIRMED_GATE_A_PENDING |
| DEC-13 | Principles / Invariants normative approval effectiveness — NEW_APPROVAL 2026-11-26; exact six-blob scope | [#1189 new approval evidence 7185429832](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7185429832); [AID-2026-096 approval evidence](../../14-ai-development/work-items/AID-2026-096/approval-evidence.md) | C; A and governance approver | Design Principles; Architecture Invariants; exact six blob pins in AID-2026-096 | New approval only; root is canonical normative source; EN/ZH mirrors retain separately marked non-normative supplemental material; no retroactive approval; changes require re-approval; P-01–P-16 implementation conformity excluded | Read back six blob SHAs, frontmatter and historical note; mirror-only supplements remain in place; implementation conformity separately excluded | RECORDED — new approval evidence committed in Draft PR #1256; #1189 state unchanged |
| DEC-14 | Owner A–I vs subsystem/capability namespace — A, non-colliding SYS-* names | [#1196 comment 7174317289](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1196#issuecomment-7174317289) | A; all A–I Owners for own capability/authority rows | System Component Map; Responsibility Matrix; #1196 | Subsystem labels distinct from Owner roles; complete capability→Owner crosswalk; primary/supporting/joint responsibility and authority boundaries; no ambiguous A–I subsystem labels | Table/diagram audit; complete mapping census; bilingual diff; individual Owner acceptance | OPEN |
| DEC-15 | D/I Forget, Retention and global completion authority — B, joint decision | [#1208 comment 7174318079](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1208#issuecomment-7174318079) | B (direction); I global policy; D canonical mechanics; relevant execution Owners jointly accept | System Boundaries @ `c2aa6823b69313ba27c34625f87f29d2be356606` (Draft/Unverified/Normative); D-FORGET-CONTRACT-001 @ `760a1d48011f2a66c23abcf825a3d067e79b8821` (Draft/Unverified/Informative); I security-governance source root remains absent; #1208 | I owns global authorization/retention/legal-hold/external-copy policy/inventory/completion criteria; D owns canonical Forget lifecycle/Fence/D-domain predicate; global completion requires D + each relevant execution Owner acceptance | Authority wording diff; exact evidence contract; joint Owner acceptance and end-to-end proof | OPEN |
| DEC-16 | I normative source file-by-file restoration — A | [#1202 comment 7174318902](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1202#issuecomment-7174318902) | A; I; required joint/dependency Owners per file | `09-security-governance/` absent on observed main; #1202 | Each candidate file has path/blob/role/dependencies/reviewers/mirror/eligibility; dependency ADRs and governance approvals before individual restoration; no whole-branch merge; Candidate/Accepted/Effective distinct | Per-file eligibility matrix; blob equality; approvals; main tree verification | OPEN |
| DEC-17 | H BMCP normative source file-by-file restoration — A | [#1203 comment 7174319680](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1203#issuecomment-7174319680) | A; H; C/G and other protocol-dependent Owners | `08-bmcp-protocol/`; #1203 | H exact inventory and contract coverage; per-file dependency/joint review/governance approval; no whole-branch merge; restoration != protocol freeze or conformance | Per-file inventory/blob/mirror/approval; main verification; exact-head conformance separately | OPEN |
| DEC-18 | Phase 1 semantic freeze vs engineering authorization — A, retain DEFERRED | [#1197 comment 7174320446](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1197#issuecomment-7174320446) | A; Phase 1 domain Owners; engineering authority separate | `02-domain-model/phase-1-domain-model-freeze.md`; controlling implementation binding; #1197 | `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; Phase 1 is semantic freeze only; historical Rust work distinguished from new authorization; remove implication of current Runtime/Storage/production start | Exact wording review; search all implementation-next-step references; EN/ZH parity | OPEN |
| DEC-19 | Governance binding-force rule — Stage 1 — A | [#1037 ruling 7153761392](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1037#issuecomment-7153761392); sequencing #1037 comment 7154085008 | A; C governance review | `00-governance/architecture-document-management-policy.md` (single inline-bilingual source); #1037 | `normative_status` determines binding force; Informative authoritative only as record of what happened, never requirement source; `usage_status: Active` does not elevate Informative; Pending-Reapproval does not change classification; changelog/EN-ZH inline wording consistent | Exact clause diff; inline bilingual semantic comparison; policy and changelog review; confirm no checker/schema scope expansion | OPEN |
| DEC-20 | Schema/checker/migration/test authorization — Stage 2, deferred pending Stage 1 — A | [#1049 comment 7174322035](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1049#issuecomment-7174322035) | A; governance Owner and separately assigned implementation/acceptance Owner | #1049; depends on #1037 | No Stage 2 work until #1037 complete and a separate explicit AID names schema, checker, migration, tests, accountable Owner and acceptance authority; this direction itself authorizes none | Verify #1037 completion; inspect separate AID scope and authority; no code/checker/schema edits in this workflow | BLOCKED |

## Duplicate-direction and sequencing map

- DEC-08 is one direction recorded across #1177, #1184 and #1212; count once in unique-direction coverage.
- DEC-09 is the watermark direction recorded in #1179/#1184 and cross-referenced by #1212.
- DEC-10 is the Fence direction recorded in #1209/#1212 (with #1177 as supporting D-source evidence).
- DEC-16 and DEC-17 are the I/H sub-registrations of one shared direction: governed, per-file normative-source restoration. Keep both domain tracks independently evidenced while counting the shared direction once.
- DEC-19 → DEC-20 is a strict prerequisite sequence. Stage 2 is BLOCKED until Stage 1 and a separate AID.
- The 20 IDs are the user-supplied register; source comments are linked individually above. A matching comment records a direction only, not acceptance.

## Required Issue evidence checklist template

Append (do not replace historical text) to each focused Issue:
- [ ] canonical source and exact blob/commit recorded
- [ ] EN mirror verified
- [ ] ZH-CN mirror verified
- [ ] cross-references and dependency ADRs verified
- [ ] required verification method/output attached
- [ ] accountable Owner accepted the exact version
- [ ] every dependent/joint Owner accepted their authority row
- [ ] governance approval recorded where required
- [ ] remaining limitations and unknown/recovery behavior documented
- [ ] implementation authorization, implementation verification and production conformance separately recorded (only if in scope)

All boxes remain unchecked until evidence is attached. This register does not close any Issue.


## I-01…I-24 delegated authority-mapping adjudication (2026-11-26)

**Attribution:** `user-authorized operator (delegated by account owner)` (delegated operator; not a natural-person signature).  
**Disposition:** the 24 Authority Owner / Dependent Owner assignments in the linked A–I + Storage matrix are **OWNER_CONFIRMED** as the delegated operator's final responsibility-mapping decision. The earlier PROPOSED rows remain preserved in that matrix as the historical proposal snapshot. This adjudication does not impersonate any listed Owner and is not their acceptance of an exact contract version.

**Counts:** 24/24 mappings adjudicated; 2 Authority Owner assignments revised from the prior proposal (I-05 D→E; I-14 D→B); 3 dependent-owner sets revised (I-02 adds C/I/Storage; I-13 and I-21 remove A because A coordinates but does not enforce those domain boundaries); all other assignments confirmed or retained with the rationale in the matrix. Row-level Gate A traceability: 24 VERIFIABLE, 0 BLOCKED_WITH_REASON. Exact-version role dispositions: 10 proxy records cover Owner A, Owners B–I and Storage/Consistency; 3 ACCEPT / 7 CONDITIONAL / 0 REJECT. Every entry says it is proxy-recorded, not a natural-person Owner signature; all seven substantive conditions remain OPEN.

**DEC-12 / Gate A status:** `OWNER_CONFIRMED_GATE_A_PENDING`; Gate A remains **PARTIAL / OPEN**, not CLOSED. The delegated mapping decision completes the responsibility-assignment task only. It does not satisfy the required exact-version cross-Owner dispositions or the complete A–I + Storage/Consistency end-to-end composition package. Outstanding Gate A items are: (1) discharge the seven explicit role-level CONDITIONAL reservations and read back the resulting exact-version evidence; the proxy dispositions themselves are recorded (3 ACCEPT / 7 CONDITIONAL / 0 REJECT); (2) current-main source/version pins and complete boundary contracts for all end-to-end flows, including issuer, request/response, identity/cursor/idempotency scope, linearization, durable receipt, failure/Unknown, replay/recovery and visibility; (3) resolution or explicit disposition of the missing D/E/F/I normative roots/contracts and Storage/Consistency source/acceptance pins; and (4) one read-back-verified exact-version review package with EN/ZH-CN semantic and source-revision parity. The current Invariants source also remains unapproved under DEC-13; no approval is inferred here.

**Gate B:** remains NOT VERIFIED and separate. Production integration, fault/recovery tests, end-to-end conformance and production Owner acceptance are not inferred from this Gate A traceability decision. #1212 remains OPEN.


## 2026-11-26 cross-Owner dispositions — delegated proxy record

**Authority and attribution:** `user-authorized operator (delegated by account owner)`; decision date `2026-11-26`. The human Owner has expressly authorized one session to represent all listed Owner roles for this record. Each disposition below is nevertheless a proxy record, not a natural-person Owner signature, platform-authenticated Owner review, or evidence that another individual personally signed. The dispositions apply to the exact responsibility mapping and Gate A review criteria in this matrix at the current PR head; they do not grant implementation authorization, normative approval, production acceptance, or Gate A closure.

**Disposition rule:** `ACCEPT` accepts the role's assigned responsibility mapping and row-level review criteria. `CONDITIONAL` accepts that mapping subject to the explicit evidence/contract condition in the row. No role issued `REJECT`. A conditional record is a recorded disposition, but its condition remains an open Gate A item until evidence is read back.

| Role | Authority rows | Dependent rows | Disposition | Condition / reservation | Attribution / date |
|---|---|---|---|---|---|
| Owner A | I-22, I-23, I-24 (Authority); I-01…I-24 (coordination) | — | **CONDITIONAL** | Accepts I-22..I-24 responsibility and the review criteria; Gate A closure is conditional on a complete exact-version A–I + Storage/Consistency composition package and bilingual/source-revision parity. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner B | I-02, I-03, I-04, I-06, I-14, I-15, I-21 | I-01, I-05, I-12, I-13, I-22, I-23, I-24 | **ACCEPT** | Accepts its assigned authority/dependency responsibilities and row-level review criteria; no B-specific reservation is recorded against the mapping. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner C | I-11, I-12 | I-02, I-03, I-04, I-06, I-09, I-10, I-13, I-17, I-18, I-21, I-22, I-23, I-24 | **ACCEPT** | Accepts its assigned authority/dependency responsibilities and row-level review criteria; no C-specific reservation is recorded against the mapping. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner D | I-01, I-07 | I-02, I-03, I-04, I-05, I-06, I-08, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The current-main canonical store normative source is absent. IMPL2 must restore or formally disposition and pin that source; D then verifies the exact canonical-authority and lifecycle contract. D is not re-assigned the source-restoration task. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner E | I-05 | I-01, I-02, I-03, I-04, I-06, I-07, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The compiler receipt/idempotency and producer/stage normative contracts are absent or not pinned on current main. IMPL2 must restore or formally disposition and pin those sources; E then verifies compiler provenance and derived-memory semantics. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner F | — | I-01, I-02, I-03, I-04, I-05, I-13, I-14, I-15, I-16, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The F-domain normative source root/contract is not present as a complete current-main review pin. IMPL2 must restore or formally disposition and pin the missing source; F then verifies the exact retrieval/derived-record boundary. F is not re-assigned source restoration. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner G | I-08, I-09, I-10, I-17, I-19 | I-01, I-02, I-03, I-04, I-05, I-06, I-07, I-11, I-12, I-13, I-14, I-15, I-16, I-18, I-20, I-21, I-22, I-23, I-24 | **ACCEPT** | Accepts its assigned context-versioning, delivery and compaction responsibilities and row-level review criteria; no G-specific reservation is recorded against the mapping. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner H | I-16, I-18 | I-01, I-02, I-03, I-04, I-06, I-09, I-10, I-11, I-12, I-13, I-17, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The exact idempotency namespace, linearization and durable replay/Unknown contract still needs one reconciled source pin across H, E and Storage/Consistency. H accepts its protocol authority subject to that exact contract being recorded. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Owner I | I-13, I-20 | I-01, I-02, I-03, I-04, I-05, I-08, I-12, I-14, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The current-main security-governance normative root is absent and DEC-13 approval metadata remains unverified. IMPL2 must restore or formally disposition and pin the source; I's policy acceptance remains conditional on exact-source and approval evidence. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |
| Storage/Consistency | — | I-01, I-02, I-03, I-04, I-05, I-07, I-08, I-09, I-10, I-13, I-14, I-15, I-16, I-17, I-19, I-20, I-21, I-22, I-23, I-24 | **CONDITIONAL** | The exact physical transaction, durability, crash/restart, restore and visibility contract is not pinned in the review package. The exact source and evidence must be recorded and Storage/Consistency's own review disposition read back. | 该处置由代理登记，非自然人 Owner 签署; date: 2026-11-26 |

**Counts:** 10 role dispositions; 3 ACCEPT; 7 CONDITIONAL; 0 REJECT. Roles covered: Owner A, B, C, D, E, F, G, H, I, and Storage/Consistency. The Authority/Dependent row coverage is derived from the 24 adjudicated invariant rows above; it is not an independent human signature.

## Gate A closeout checklist — current disposition

| Gate A item | Status | Minimum condition to close / accountable party |
|---|---|---|
| Branch synchronized with current main | SATISFIED | Merge base equals current main; merge base equals current main and the branch is not behind it. The ahead count is volatile as review commits accumulate and is reported from current PR metadata, not frozen here. Recheck if main advances again. |
| Cross-Owner role dispositions recorded | SATISFIED | All 10 roles have a dated proxy disposition; 3 ACCEPT / 7 CONDITIONAL / 0 REJECT. The seven conditions below remain OPEN and must be discharged before Gate A can close. |
| Exact-head CI | OPEN_PENDING_FINAL_HEAD | Run all applicable pull_request workflows on the final documentation head and read back the exact SHA and conclusions; do not reuse earlier-head results. |
| Complete A–I + Storage/Consistency composition review artifact | OPEN | Owner A coordinates one exact-version package; each relevant Owner pins the canonical source and documents issuer/authority, request/response, identity/cursor/idempotency namespace, linearization point, durable receipt, failure/Unknown, replay/recovery and visibility for each end-to-end boundary. |
| Missing normative source roots/contracts (D/E/F/I) | OPEN — IMPL2 | **IMPL2 owns source restoration or explicit disposition and exact source pins.** Minimum: restore/publish the missing current-main normative roots/contracts or record a governed non-restoration disposition with exact replacement source pins. Domain Owners validate their contracts after restoration; they do not duplicate-claim IMPL2's source-restoration task. |
| Storage/Consistency physical contract and evidence | OPEN — IMPL2 + Storage/Consistency | IMPL2 supplies/restores the canonical physical transaction/durability/recovery source and exact blob pin; Storage/Consistency reviews and records the corresponding proxy disposition condition as satisfied against crash/restart, restore and visibility evidence. |
| H idempotency namespace / replay boundary | OPEN — Owner H with E and Storage/Consistency | Record one reconciled exact-version namespace/scope, linearization, durable receipt and Unknown/replay contract across the participating boundaries. |
| Full-package bilingual semantic and source-revision parity | OPEN — Owner A / documentation Owners | Read back the complete exact-head Canonical/EN/ZH-CN review package; verify semantic parity, stable IDs, decision states and every source revision pin. Matrix-only parity is insufficient. |
| DEC-13 normative approval evidence | RECORDED — AID-2026-096 new approval event, 2026-11-26 | https://github.com/oahcom/AiMemoryBrainArchitecture/issues/1189#issuecomment-7185429832; exact six path/blob pairs in AID-2026-096/approval-evidence.md; implementation conformity remains separate |

**DEC-12:** remains `OWNER_CONFIRMED_GATE_A_PENDING`. Gate A is **PARTIAL / OPEN**, not CLOSED. The cross-Owner disposition record is now present, but conditional evidence and composition/source/parity items remain OPEN. **Gate B remains NOT VERIFIED** and separate. #1212 remains OPEN.
