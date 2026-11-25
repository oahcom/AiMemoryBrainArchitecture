---
document_metadata:
  domain: ai-development
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
      evidence_reference: []
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Metadata added on 2026-11-24 so that this file can be edited without tripping DM-01. No content claim in this file is verified by this block."
    usage_status: Active
    modification_status: Modified
    supersession:
      supersedes: []
      supersession_reason: null
      effective_date: null
    archival:
      archived_date: null
      archival_reason: null
      archival_reference: null
  authority:
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AI-EXEC-INDEPENDENCE-RULING-001
# Session Independence, Platform Identity and R3 Expert Review

- Document ID: AI-EXEC-INDEPENDENCE-RULING-001
- Source: [Canonical bilingual source](AI-EXEC-INDEPENDENCE-RULING-001.md)
- Source Blob: `48bc8b6082abf3455272f384cbd940711879b353`
- Translation status: DRAFT — not adopted; the bilingual source remains authoritative
- Version: 1.0
- Status: PROPOSED — pending explicit Project Owner adoption; this session does not claim Owner adoption
- Ruling date: 2026-11-18 (execution date; coordinator observations also cite 2026-11-19)
- Authority: L4 governance adjudication session; Project Owner adoption remains required for repository-wide normative policy
- Tracking: Issue #130; AID-2026-005; related PRs #249/#251/#252/#253/#258 and Issue #264
- Relationship: COMPLEMENT — narrow interpretation; no source clause is amended or waived
- Review-by: 2026-12-02
- Language authority: English and Chinese provisions are intended to be semantically equivalent; independent bilingual review NOT RECORDED

## Status path

PROPOSED → ADOPTED only after the Project Owner, or a delegate with explicit documented authority to adopt repository-wide governance policy, records an affirmative attributable decision in an existing governance carrier. The record must identify this document/version, adopting authority, effective date, relationship, rationale, boundary and review date. An author-identity COMMENT, AI role simulation, commit, merge, silence or this session's own ruling is not adoption. Until then this remains a proposal, not an effective amendment to ADOPTED standards.

Basis: AI-EXEC-001 v1.1 and AI-EXEC-002 v1.1 are ADOPTED via PR #256 merge 48a556491506d25e78be47957276bf3821797a0a; PR-GOVERNANCE-001 is ADOPTED via Issue #130 comment #6962523529; AI-EXEC-UNIFICATION-RULING-001 is the binding precedent. This proposal is COMPLEMENT, not SUPERSEDE.

---

## RULING-04 — Two non-substitutable independence dimensions

**Conflict.** NR-001 / OPTION A permits a genuinely new independent ChatGPT conversation to satisfy the independent-session requirement subject to controls. PR-GOVERNANCE-001 §5 as amended 2026-11-24 makes independence a property of the reviewing session: a review through the same connected GitHub identity as the author **is** independent when the reviewing session is not the authoring session. Before that amendment §5 required a distinct GitHub actor, which NR-001 / OPTION A could not supply. AI-EXEC-001 v1.1 §6 and AI-EXEC-002 §5 preserve both requirements; the amendment removes the conflict rather than choosing a side.

**Ruling.**
1. Session/review-behavior independence (S-independence) means a genuinely new conversation distinct from authoring/implementation, supplied with frozen inputs, independently reading repository sources, performing adversarial review and recording findings, with NR-001 disclosure that conversation isolation is not model/provider/statistical independence.
2. Platform-identity/review-event independence (P-independence) — **retired 2026-11-24.** Was defined as: the review event is attributable to a GitHub identity distinct from the author's connected GitHub identity. Item 5 records why it no longer stands as a bar; it is kept here so that rulings written against it remain readable.
3. S-independence satisfies the independence requirement of `PR-GOVERNANCE-001` §5 in full, as amended 2026-11-24 to make independence a property of the reviewing session. It does not create a second GitHub actor and does not produce Owner approval; neither is required for independence.
4. Under the repository's stated ChatGPT-native model where sessions share oahcom, a fresh session satisfies §5 independence. The shared GitHub actor is the carrier of the review event, not the measure of its independence; what §5 now asks is whether the reviewing context is the authoring context, and for a fresh session it is not.
5. AI-EXEC-001 R2 maps independent ChatGPT session to S-independence, which is now the §5 requirement itself. Affected Owner explicit contract approval is separate and still required. R3 additionally requires security/domain expert review, reproducible tests and explicit Acceptance Authority approval. Those remain non-substitutable; P-independence no longer exists as a separate bar.
6. For §5-covered changes (security, identity, authorization, Forget, lifecycle, canonical persistence, recovery, cross-owner contracts, production operations), a qualifying independent session is sufficient for the independence element of MERGE. High-risk changes additionally require the affected Owner's explicit approval, which no session supplies. Absent that approval, disposition remains HOLD, or REMEDIATE/REJECT as justified.

**Boundaries.** No model independence, multi-model consensus, human expertise, platform enforcement or independent GitHub actor is claimed. Role separation is not actor separation. Role simulation inside the authoring session must never be relabeled independent; a **separate session** under the same identity already is independent and needs no relabeling.

**Effective scope.** Prospective interpretation after adoption. Review by 2026-12-02.

---

## RULING-05 — Five-disposition authorization chain

**Conflict.** NR-001 review + Owner comments + an exception + exact-Head checks could be misread as enough to merge despite §5, converting exception recording into waiver.

**Ruling.** Preserve exactly MERGE / HOLD / REMEDIATE / SUPERSEDED / REJECT:

- MERGE only if every applicable exact-Head check passes; an independent-session §5 review exists where applicable; NR-001 review exists where required; every affected authority Owner explicitly approves the exact normative contract boundary; R3 additionally has qualified independent expert review, reproducible test evidence and Acceptance Authority approval; dependencies are satisfied; no blocking finding remains; and the PR is mergeable.
- HOLD if any required review, Owner approval, expert review, exact-Head check, reproducible evidence or dependency is missing, pending, NOT RUN, NOT VERIFIED or attributable only to the shared identity〔added 2026-11-25: read this as "attributable only to the **authoring/implementing session**". After the `PR-GOVERNANCE-001` §5 amendment of 2026-11-24 (commit `2eb4e352`, PR #935) independence is a property of the reviewing session; a review carried by the shared identity but produced by another session is independent and does not trigger HOLD〕.
- REMEDIATE for a concrete defect/evidence gap repairable on the same coherent carrier; re-review the changed exact Head.
- SUPERSEDED only when an actual replacement fully supersedes the carrier; preserve unique evidence. It is not a shortcut around missing approval.
- REJECT when the proposal is invalid or conflicts with accepted authority; preserve rationale and evidence.

**Owner approval protocol.** The actual accountable Owner (or a delegate with documented authority) must issue a direct, attributable, explicit written decision identifying PR/Work Item, exact Head or immutable contract version/blob, clauses/fields, ACCEPT / REJECT / ACCEPT WITH AMENDMENTS, conditions, identity/role and timestamp. Use an existing Issue/PR comment or link a verifiable Owner-authored artifact. If GitHub actor is shared oahcom, disclose it; do not represent it as a distinct platform identity or GitHub APPROVE. Verify attribution through an authorized Owner channel. If attribution cannot be verified, Owner gate remains OPEN.

Never issue or claim GitHub APPROVE as a workaround for the platform's self-approval prohibition. Owner written decision may satisfy only the Owner contract-approval gate when attribution and scope are verified; it is not §5 independence and cannot substitute for it. Independence is supplied by a separate reviewing session, which this repository can always open; where even that is unavailable, HOLD and escalate to Project Owner/repository administrator.

**Boundaries.** No combination of authoring-session COMMENT, role simulation, Owner narrative, exception entry or green CI manufactures an independent reviewer. Exception alone never changes HOLD to MERGE.

> **Added 2026-11-25 (citation currency).** This sentence read "same-identity COMMENT" — the pre-2026-11-24 §5 criterion, under which the same identity was never independent. `PR-GOVERNANCE-001` §5 as amended 2026-11-24 (commit `2eb4e352`, PR #935; `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`) keys independence on the reviewing **session**: a COMMENT from another session that shares the author's GitHub identity, did not write or implement the change and takes its conclusion from the artifact **can** be an independent review, and what cannot manufacture one is a COMMENT inside the authoring session. The sentence above has therefore been replaced with "authoring-session COMMENT", word-for-word identical to the same sentence in `AI-EXEC-INDEPENDENCE-RULING-001.md:128`. COMMENT is still not APPROVE, and platform `required_pull_request_reviews` still counts users. The other four items are unchanged.

**Effective scope.** All five-state decisions after adoption. Review by 2026-12-02.

---

## RULING-06 — Explicit §5 exception protocol

**Conflict.** PR-GOVERNANCE-001 §5 requires explicit exception recording but does not enumerate fields/counting/carriers. AI-EXEC-001 v1.1 §6 restricts exceptions to escalation/HOLD/REMEDIATE/REJECT and caps them at two per iteration.

**Ruling.** An exception is a time-bounded record of an unavailable control/resource, never a waiver. Register one per distinct blocked Work Item/PR plus missing mandatory control/resource.

| Field | Required content |
|---|---|
| Exception ID | EX-YYYYMMDD-NN, unique within iteration |
| Work Item/carrier | AID, Issue, PR, repository |
| Rule/control | Exact clause and missing review/evidence |
| Risk/scope | R0–R3 and affected boundary |
| Request time | Timezone timestamp + source link |
| Missing resource | an independent reviewing session (any GitHub account, including the authoring one), an expert, an Owner decision or a test〔added 2026-11-25: replaces "Independent GitHub reviewer"; that account-level wording was retired by the §5 amendment of 2026-11-24〕 |
| Attempts/source order | Recipients, requests, timestamps, responses; NR-001 first where applicable |
| Reason | Factual unavailability; distinguish not-requested from no-response |
| Disposition | HOLD / REMEDIATE / REJECT only |
| Escalation owner/time | Named accountable Owner/admin and timestamp |
| Open evidence | Exact missing items; retain NOT RUN / NOT VERIFIED |
| Next review | Timestamp |
| Deadline | 24-hour escalation and 3-business-day disposition where §6 applies |
| Decision | Continue HOLD / REMEDIATE / REJECT; authority and timestamp |
| Closure evidence | Actual control obtained or remediation/rejection; exact link/SHA |
| Iteration/count | Iteration key, ordinal 1 or 2, over-quota marker |
| Disclosure | Shared GitHub identity, AI simulation and provenance limits |

**Counting.**
- Count each distinct blocked Work Item/PR plus missing mandatory control/resource once per iteration. Same control and continuous blocked interval for one PR counts once; separate controls (for example §5 reviewer and R3 expert) count separately.
- New iteration, renewed request after recorded deadline, materially different missing control or new PR/Work Item is a new exception. Do not split one event to inflate counts or merge distinct controls to hide counts.
- Limit remains no more than two per iteration. A third is over-quota, must be recorded and escalated to daily governance window; omission does not make it compliant.
- Keep the countable register in the existing owning Issue/PR thread and link it from manifest/Closeout. Issue #130 is cross-PR index; details remain on each affected existing PR/Issue. If no PR exists, use existing Issue or Closeout. Never create an Issue solely for an exception.
- Close only when missing control is actually obtained or an authorized REMEDIATE/REJECT decision is recorded. Expiry, silence or elapsed time does not close it.

**Boundaries.** Exceptions do not satisfy missing review/approval/expert/test, turn NOT RUN into PASS, authorize downgrade or permit MERGE. Clock triggers escalation/disposition only.

**Effective scope.** New exception records after adoption; no fabricated historical evidence. Review by 2026-12-02.

---

## RULING-07 — R3 expert source and escalation clock

**Conflict.** AI-EXEC-001 v1.1 requires R3 independent security/domain expert review, reproducible tests and explicit Acceptance Authority approval. NR-001 does not waive these gates.

**Ruling.** A qualifying expert must be a real, identifiable human with competence relevant to the particular risk, evidenced by professional role/experience, relevant work, qualification or a documented accountable-Owner assessment. The person must be independent of author/implementation, disclose conflicts, and review exact Head or immutable artifact. The report must identify reviewer, expertise/basis, independence/conflict disclosure, exact SHA, scope, methods/evidence, findings/severity, conclusion, limitations and timestamp. A platform expert resource may qualify only if it is a verifiable human expert and all independence requirements are met; no such resource is asserted to exist here. ChatGPT conversations, model personas, prompt roles, AI panels or vendor/model labels never qualify.

**Clock**
- Start at the evidenced request timestamp. If no qualifying resource/evidence is obtained within 24 hours, escalate to accountable Owner and keep HOLD/BLOCKED; record request, attempts, missing resource, escalation recipient and next review.
- If still unavailable at 3 business days, accountable Owner records continue HOLD, REMEDIATE with concrete acquisition plan, or REJECT. Timeout never authorizes MERGE, ACCEPTED, risk downgrade or waiver.
- If historical request time is absent, mark NOT RECORDED and start a new prospective clock from a newly evidenced request; never invent/backdate.
- PR #249: RV-249-2 is BLOCKER and says NR-001 session review cannot satisfy the R3 expert gate. Keep BLOCKED/HOLD until qualified expert report and reproducible exact-Head evidence exist, in addition to §5 and Owner gates. Apply clock from verifiable request time; if unavailable, mark NOT RECORDED and initiate a fresh request.
- PR #258: F-PR258-REVIEW-02 is BLOCKER; F-PR258-RESILIENCE-01 is P1. Exact-Head Rust/GOV-DOC checks are recorded SUCCESS, but subprocess crash/recovery, concurrent append, restart receipt stability, payload-tamper detection and WAL recovery remain NOT VERIFIED/NOT RUN; independent persistence/security-domain review remains required. Keep HOLD/BLOCKED. Green CI does not close missing tests or expert review. Apply same request-clock rule.
- Reproducible evidence identifies exact source SHA, command, environment/dependencies, fixtures, expected/actual results, logs/artifact links and independent reproduction instructions. Any required test not run remains NOT RUN.

**Boundaries.** This ChatGPT session is not a security/domain expert. No R3 evidence is waived.

**Effective scope.** R3 qualification and clock records after adoption. Review by 2026-12-02.

---

## RULING-08 — Phase B application to PRs #251/#252/#253

Rules-only application. No PR state, branch or metadata is changed.

| PR | Present rule conclusion | Required gates before MERGE |
|---|---|---|
| #251 RFC-IDE-001 | Cross-owner identity/Scope/idempotency contract; §5 applies. Exact Head/CI not recorded in INDEX; required Owner decisions not evidenced complete. **HOLD.** | Fresh NR-001 review; independent-session §5 review; attributable Domain Model/Producer Identity, Scope/Security and Event Store Owner decisions against exact contract version; exact-Head checks; resolve or explicitly exclude TTL, cleanup, ProducerIdentity composition and digest CANDIDATE/TO_VALIDATE items; no BLOCKER. |
| #252 D/E/I/Storage convergence | Cross-owner normative interfaces and security/authorization/recovery boundaries; §5 applies. Successor pins recorded, but exact-Head checks and all D/E/I/Storage Owner decisions not evidenced complete. **HOLD.** | Fresh NR-001 review; independent-session §5 review; D, E, I and Storage decisions against exact successor Blobs; close D-HW-01/H-RJ-HW-01 or keep outside accepted scope; applicable exact-Head checks; physical conformance and production authorization remain separate. |
| #253 acceptance matrix | Cross-owner acceptance authority/evidence boundary; §5 applies. Exact Head/CI and Owner adoption/approval not recorded complete. **HOLD.** | Fresh NR-001 review; independent-session §5 review; Project Owner/authorized governance adoption and affected Owner approvals for normative responsibility boundaries; exact-Head GOV-DOC/bilingual checks; no logical acceptance represented as physical conformance or production approval. |

All three retain their existing platform state; no GitHub APPROVE is issued or inferred. New findings must be recorded in existing Issue/PR comments with ID + severity + return destination. No new Issue is opened.

**Boundaries.** Not an implementation review or fresh CI run; refresh exact Head, checks and Owner decisions at any later merge decision.

**Effective scope.** Rules-only application to #251/#252/#253. Review by 2026-12-02.

---

## Terminology

| Term | Definition |
|---|---|
| S-independence | NR-001 fresh-session review; not model/provider/statistical independence. |
| P-independence | **Retired 2026-11-24.** Was: review event attributed to a GitHub identity different from the author's. No longer an independence bar; see `INDEPENDENCE-IS-SESSION-LEVEL-036`. |
| Owner approval | Explicit attributable approval by actual accountable authority for its normative boundary. |
| Expert review | Additional review by verifiable competent independent human; never a ChatGPT role. |
| Exception | Time-bounded unavailability record for escalation/HOLD/REMEDIATE/REJECT; never waiver. |
| Exact-Head | Evidence tied to precise current commit SHA. |
| NOT RUN | Required check not executed; never PASS. |
| Five dispositions | MERGE, HOLD, REMEDIATE, SUPERSEDED, REJECT. |

## Bilingual semantic parity self-check

The authoring session checked both languages for the same independence axes, non-substitution rules, five dispositions, Owner attribution protocol, exception fields/counting, R3 qualification/clock and Phase B HOLD conclusions. Author self-check only; independent bilingual semantic review NOT RECORDED. GOV-DOC-001 PASS is not claimed.

## Evidence and provenance

- Readback Blob SHAs: AI-EXEC-001 `cb95815627f895e2cf46c4e801b91153b2713f0b`; AI-EXEC-002 `64a85bc8763ba22a88dc791daddae548b93e4f5d`; PR-GOVERNANCE-001 `4a28fa8181af0da06f52d31a6dca5d30fbf6458a`; UNIFICATION-RULING `94939179ce592cd82e1a34ab8c5bd9fb6bad0283`; INDEX `981bd6d3720fc8fb8d8de0a6942b85f1d4022eed`.
- Prompt provenance: T2 chat instruction; coordinator session + this session's task prompt (independence interpretation ruling). Stable conversation ID/permalink, raw bytes and SHA-256 unavailable; SHA-256 NOT_VERIFIED. No fictional repository prompt file/hash.
- Baseline: main@`6b5db2918cffc2281deb22fd9858a37dbaeec726` as stated in PR #258 quota-closeout evidence; direct branch-ref HEAD query unavailable, not represented as a fresh HEAD response.
- Verification: policy/documentation only; runtime tests NOT RUN / NOT APPLICABLE; independent GOV-DOC-001 check NOT RUN.
- Findings: F-AID005-01 [BLOCKER] → Issue #130; F-AID005-02 [P1] → Issue #130.
---

## Amendment record / 修订记录（2026-11-24）

**本文件的 RULING-04 第 3、4、5、6 项已按所有者基线修改**，术语表的 P-independence 条目标记为退役。

原因：`PR-GOVERNANCE-001` §5 于 2026-11-24 修订，独立性改为**会话级**属性。RULING-04 原判定
「S 独立性不能替代 P 独立性、§5 要求 P 独立性」因此失去依据——它所解释的那条文本已不存在。

**保留不变**：S 独立性仍然不是模型/服务商/统计独立；同会话内角色模拟仍然不构成独立审查；
受影响 Owner 的明确批准仍然独立必需；五态处置、例外字段、R3 专家审查要求均不变。

**这不是本文件自我采用。** 本文件状态仍为 `PROPOSED`。本次修改的是它与现行 §5 不一致的部分，
若不改，它会持续引用一条已被替换的条款。采用与否仍由所有者决定。

Revision of this file's RULING-04 items 3–6 follows the owner baseline and the §5 amendment of
2026-11-24. What is preserved: S-independence is still not model/provider/statistical independence;
role simulation within the authoring session still does not count; affected Owner approval is still
separately required; the five dispositions, exception fields and R3 expert-review requirements are
untouched. This file remains `PROPOSED`; the change only removes its reference to a clause that no
longer exists.

