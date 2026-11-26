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
      approval_applicability: Not-Applicable-To-Current-Version
      evidence_reference:
        - "14-ai-development/work-items/AID-2026-105/evidence.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-26"
      last_verification_note: "Evidence inventory based on GitHub readbacks at main 533d8646a3fb32b0a1c9d3ed40c01bce33a76b17; it records gaps and does not claim acceptance."
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
    canonical_scope: "English mirror of Issue #1189 acceptance evidence inventory"
    canonical_scope_id: "ai-development/issue-1189-acceptance-evidence"
    canonical_scope_keywords:
      - approval-provenance
      - owner-acceptance
      - joint-acceptance
      - evidence-gap
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: "14-ai-development/work-items/AID-2026-105/evidence.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-105/evidence.md"
---

# Issue #1189 — acceptance evidence inventory

- Work Item: `AID-2026-105`
- ID status: `PROVISIONAL`
- Initial evidence readback: `main` at `533d8646a3fb32b0a1c9d3ed40c01bce33a76b17`; synchronized base after PR creation: `main` at `df54ed60321e2958c50e9649963608cb3cb3f3b1`; latest synchronization: `main` at `2d52b0c81dc1b779e49516fceb69d89cdc1d9c31`.
- Baseline date: 2026-11-26
- Attribution: `user-authorized operator (delegated by account owner)`
- Attribution note: delegated operator record; **代理登记，非自然人 Owner 签署**
- Nature: documentation-only evidence inventory. This is not a new approval, Owner acceptance, joint acceptance, governance approval, or Issue-closure decision.

## 1. Finding

Issue #1189 is not simply waiting for an approval record. A new, attributable approval event was recorded on 2026-11-26 and carried by PR #1256, merged as `64bce1321a33e8f0d70949f7bb5869c5f250522a`. The remaining acceptance gap is the absence of the required accountable/dependent Owner and governance-approver acceptance against the exact current versions, together with unresolved version/mirror and governance-check evidence.

The evidence does **not** support closing #1189. It remains OPEN.

## 2. Issue acceptance requirements and evidence disposition

The requirements below are transcribed from Issue #1189's acceptance criteria and later DEC-13 acceptance checklist. “Documented” means a record exists; it does not turn a proxy disposition into a natural-person signature or convert an unexecuted check into PASS.

| # | Acceptance requirement | Evidence currently present | Disposition |
|---|---|---|---|
| 1 | Current approval status is supported by attributable, version-pinned evidence, or an authorized decision corrects the status. | AID-2026-096 approval record; PR #1256 merge `64bce1321a33e8f0d70949f7bb5869c5f250522a`; original six approved Git blob pins and six body content-hash pins are in §3. Current six Git blobs are different after the metadata-only schema migration in commit `44b57170b86c7f3e56744da756ed24744b1c659c`, included in main merge `533d8646a3fb32b0a1c9d3ed40c01bce33a76b17`. | **EVIDENCE_REQUIRED** — reconcile the AID-096 statement that any metadata change requires a new approval event with the later removal of the two obsolete empty metadata keys. Obtain an explicit authorized disposition or re-pin/re-approve the current six blobs. |
| 2 | No approver identity or date is invented or inferred. | AID-2026-096 records `user-authorized operator (delegated by account owner)`, designation source “account owner statement, 2026-11-26”, event date 2026-11-26 and `NEW_APPROVAL`; Issue comment #7185429832 records the same. | **DOCUMENTED_WITH_LIMIT** — proxy attribution and event date are recorded; this is not a natural-person Owner signature and does not satisfy the separate Owner-acceptance checklist. |
| 3 | Approval scope is explicit separately for P-01–P-16 and the Architecture Invariants set. | AID-2026-096 approval evidence identifies the full-document scope for the Design Principles and Architecture Invariants roots and their EN/ZH-CN mirrors, with six exact path/blob pairs. It expressly excludes P-01–P-16 implementation conformity. | **DOCUMENTED_WITH_LIMIT** — document-level scope is recorded; no implementation-conformity claim is made. Current-blob reconciliation remains open under item 1. |
| 4 | Both canonical documents have attributable, version-pinned approval evidence or an authorized status correction. | Canonical Design Principles and Architecture Invariants have `Approved`, approver/date and content-hash values matching the AID-096 recorded body-hash values. The six current Git blob IDs do not equal the six Git blob IDs in the approval record. | **PARTIAL / EVIDENCE_REQUIRED** — body-hash values remain recorded, but the exact current Git blobs are not the exact blobs listed in the approval record. No new approval is inferred. |
| 5 | EN/ZH-CN mirrors carry the same verified status and source pin as the canonical documents. | All six current documents show `decision_status: Approved`, the same proxy attribution/date and `normative_status: Normative`. However, all six show `evidence_verification.verification_status: Unverified`; canonical root verification notes still say no formal approval record exists; the Architecture Invariants root and EN body still describe the invariants as proposed and subject to a separate approval. | **EVIDENCE_REQUIRED** — reconcile stale statements and verify semantic parity and source-revision pins across all six exact current blobs. Metadata equality alone is not semantic parity. |
| 6 | Governance checks detect an Approved decision that lacks required approval provenance, including missing approver/date evidence and an unverified state. | Current `scripts/check_document_management.py` DM-03 requires an Approved document's version, scope type and applicability. The checker validates the verification-status enum but does not require a non-empty approver/date or require `Verified`. Policy M-02 and M-03 explicitly classify the reality/support of approval evidence as reviewer controls. | **EVIDENCE_REQUIRED** — the current checker does not enforce the specific acceptance condition. This work item does not change validator semantics; a separately authorized checker/test change and raw CI output are required. |

## 3. Approval record versus current exact versions

### 3.1 Approval record carried by PR #1256

The merged approval evidence is `14-ai-development/work-items/AID-2026-096/approval-evidence.md` (current-main blob `bff9a63ad88e027e92529bcc4001250840dade8d`). It records:

- Approval event: `NEW_APPROVAL`, 2026-11-26.
- Approver attribution: `user-authorized operator (delegated by account owner)`.
- Designation source: account owner statement, 2026-11-26.
- Scope: full-document approval for Design Principles and Architecture Invariants, each with EN/ZH-CN mirrors.
- Exclusion: implementation conformity with P-01–P-16, runtime, validator, deployment and production conformance.
- Carrier merge: PR #1256, merge commit `64bce1321a33e8f0d70949f7bb5869c5f250522a`.

Original approved Git blob SHA-1 values:

| Path | Blob recorded by AID-2026-096 |
|---|---|
| `00-governance/design-principles.md` | `352b969fa8c07ad1f2848797f06404293242db13` |
| `00-governance/architecture-invariants.md` | `3c64217fde34fe67f463856b648a3e8a935a1654` |
| `docs/en/00-governance/design-principles.md` | `50d1d1d0907f25e2104414ba9bb48a31fb470b1d` |
| `docs/en/00-governance/architecture-invariants.md` | `ca7052afa486ce124e180c63812e082a6def5ebc` |
| `docs/zh-CN/00-governance/design-principles.md` | `cf6ce6c08970dea58e3a93514cea1f801e55a666` |
| `docs/zh-CN/00-governance/architecture-invariants.md` | `de534192ce8c343318d7da4add21daf0bbf1e04b` |

The same record lists the following approved body content hashes (the values also remain in the current documents' `approved_version.scheme: content-hash` fields): Design Principles root `273f048d8dd3401ec62e2c177fa00787ab6f6cb855e190b471b3a0c7f3b81523`; Invariants root `6df99f23052dd5475d22d397cdee160436464dc3a95946fe6d6e12f93aea1071`; EN Design Principles `e467d7cf3e8feb0457843b5f4f0fd038b01608c32a9fbe35e585cc41e49c665a`; EN Invariants `6b818d9b1884530bdf208507d6a7913699c8598d4c0f351f238cfaff449c0a3a`; ZH-CN Design Principles `7cd923872a16ec0b01174798614d6ccf867b20fa18edfe9c3c08b4f3e31e3e00`; ZH-CN Invariants `88bbebd033e0b5669bafc83c71afa2831cebb4a2e3a6cfa47573cf6b3259b293`.

### 3.2 Current main exact Git blobs

Each current blob below was re-read from `main` at `2d52b0c81dc1b779e49516fceb69d89cdc1d9c31`. Main advanced from `df54ed60321e2958c50e9649963608cb3cb3f3b1` via PR #1291 (AID-2026-106); all six blob IDs remained unchanged.

| Path | Current main blob SHA-1 | Matches AID-096 Git blob pin? |
|---|---|---|
| `00-governance/design-principles.md` | `9fb729a4bd6ebcfa9576e5318804a65e2a95abe2` | NO |
| `00-governance/architecture-invariants.md` | `15daf882febb71e4cda9317bdd7f0538fbae2404` | NO |
| `docs/en/00-governance/design-principles.md` | `214b8f376497cc3c3c04e2d6bce2951427a84f2c` | NO |
| `docs/en/00-governance/architecture-invariants.md` | `a223001bece95bcdb1d41407910d5df7e1ffd313` | NO |
| `docs/zh-CN/00-governance/design-principles.md` | `40b5984eeae38795efe51da25bb2a3708a6d1135` | NO |
| `docs/zh-CN/00-governance/architecture-invariants.md` | `97c652b9d30a53a10036a2030419432ddd41c144` | NO |

The current-main merge commit `533d8646a3fb32b0a1c9d3ed40c01bce33a76b17` has `44b57170b86c7f3e56744da756ed24744b1c659c` as a parent. That commit removes the obsolete, empty `approval_scope.included_sections` and `approval_scope.included_assets` keys from the schema and corpus. Its diff for the six approved documents changes frontmatter only; it does not show body-line changes in those six documents. The GOV-DOC-002 body-hash algorithm strips frontmatter, so this explains why the stored body hashes can remain unchanged while Git blob IDs change. It does **not** decide whether AID-096's stricter statement (“any content or metadata change creates a new blob and requires a new approval event”) permits this schema migration without a new approval. That decision is not supplied by this evidence inventory.

## 4. Other main evidence and unresolved contradictions

| Evidence | Current main path and blob | What it establishes / limitation |
|---|---|---|
| Prior Issue audit | `14-ai-development/work-items/AID-2026-092/ISSUE-1189-approval-provenance.md`, `fbaae7eb5a175944cb89d12fe8949aa1535c9d98` | Historical no-approval finding at its stated baseline. Its disposition predates and is superseded by the new approval event in AID-096; do not reuse its old blob pins as current. |
| DEC-13 evidence | `14-ai-development/work-items/AID-2026-093/evidence.md`, `69ce490157adb1e018e5608e7405c6ef4d233de3` | Records DEC-13 comment #7174867715 as 10 unchecked / 0 checked and 20/20 comment readbacks; this proves the checklist was recorded, not accepted. |
| DEC-13 register | `00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md`, `4810c6f8d3b5676a44288dea5782681e0745af6f` | Evidence register explicitly distinguishes direction approval from Owner acceptance, normative effectiveness, implementation authorization, verification and production conformance. |
| A–I / Storage matrix | `00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md`, `a180459fa70f713de9232f372b94c8feb2c0c90d` | Records role dispositions as proxy-recorded; 3 ACCEPT / 7 CONDITIONAL / 0 REJECT. It states natural-person Owner acceptance count is 0 and DEC-13 / Gate A acceptance remains open. |
| EN / ZH-CN DEC-13 register mirrors | `docs/en/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md`, `dcae8a7cb5c6e03bf220d1d681744cc68361e87d`; `docs/zh-CN/00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md`, `49b3aff58991b77545ab143d12782b65e71a5a69` | Mirror artifacts; their presence does not prove semantic parity or Owner acceptance. |
| EN / ZH-CN A–I / Storage matrix mirrors | `docs/en/00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md`, `5e6a388be1e55a0acaa49e67006f8ad3404a1a72`; `docs/zh-CN/00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md`, `149f3657e980826b1b44d560b83e71f837c8ffab` | Mirror artifacts; their presence does not prove semantic parity or Owner acceptance. |
| AID-096 manifest | `14-ai-development/work-items/AID-2026-096/manifest.yaml`, `df16f4ad6d563f3f2a9a4596ee94a855b8431e19` | Records `APPROVAL_RECORDED_OWNER_ACCEPTANCE_PENDING`; no Owner/joint acceptance is claimed. |
| AID-096 session evidence | `14-ai-development/work-items/AID-2026-096/session-evidence.md`, `45a1c1aebb54a93b28c2446c9ade96d6abc84654` | Records proxy attribution, prompt/session provenance limits and the no-natural-person-signature boundary. |
| AID-096 prompt snapshot | `14-ai-development/work-items/AID-2026-096/prompt-v1.md`, `042f0f21e7d2410f01d5aeca4cbb2d4597422f11` | Records the delegated approval task and its explicit scope/exclusions. |
| Issue #1189 decision / acceptance comments | Comments `7174316473`, `7174519803`, `7174867715`, `7185367827`, `7185429832` and `7186346059` | Record the non-approval direction, D-12, DEC-13 unchecked checklist, keep-open audit, AID-096 new approval event and post-merge status. The latest approval comment expressly leaves Owner/joint acceptance pending. |
| Work-item index | `14-ai-development/work-items/INDEX.md`, `02bacd620ea147bd9b2fb63868648d8b7dd55474` | AID-096 Acceptance cell says pending; AID-093 records proxy dispositions and zero natural-person acceptance. |

### 4.1 DEC-13 accountable and joint acceptance

Issue comment #7174867715 identifies Accountable decision Owner C and required dependent/joint Owners A and governance approver. Its checklist has separate unchecked items for canonical source update, EN mirror verification, ZH-CN mirror verification, cross-references/dependency ADRs, independent criteria checks, verification method/raw output, Accountable Owner acceptance, each required dependent/joint Owner acceptance, governance approval and limitations/failure/recovery documentation.

The AID-2026-093 evidence readback records 10 unchecked boxes and 0 checked for DEC-13. The A–I / Storage matrix's 10 role dispositions are explicitly proxy-recorded and not natural-person signatures; its natural-person Owner acceptance count is 0. Therefore the specific acceptance from Owner C, joint Owner A and the governance approver is **EVIDENCE_REQUIRED** against the exact current versions. Proxy disposition does not close those boxes.

### 4.2 Current-document consistency observations

- The canonical Design Principles and Architecture Invariants frontmatter still says `evidence_verification.verification_status: Unverified`.
- The two canonical root documents' `last_verification_note` still says no formal approval record / approver / date exists, which conflicts with the later AID-096 new-approval record.
- The Architecture Invariants root and EN body still call the invariants “proposed” and subject to a separate approval decision, despite the current Approved / Normative metadata. This is a body-level contradiction, not just a blob-ID difference.
- The EN Design Principles mirror retains a source revision string `9792e189d63fbbc3694ab891fc4aeba5143b3b1c`; the ZH-CN counterpart also carries a source revision string. These source pins and all six bodies require a fresh semantic/source-revision parity readback at one exact commit.

These observations are not corrected by this work item. Changing the canonical approval metadata or normative prose requires the relevant authorized decision and a separately reviewed change.

## 5. GOV-DOC-002 checker coverage

Current main source pins:

- `scripts/check_document_management.py`: blob `4221de3cdf59c4985b19fd258163780866271167`.
- `00-governance/architecture-document-metadata.schema.yaml`: blob `a3ce83d6afc38eb960c39b5636704798cbd299cd`.
- `00-governance/architecture-document-management-policy.md`: blob `3f800279708bf6c101ee5295158b62ef137e0758`.

The checker’s DM-03 block requires an Approved document to bind `approved_version.value`, `approval_scope.type` and `approval_applicability`. The schema declares `approver` and `decision_date` as nullable strings, not non-empty required fields. The checker validates `evidence_verification.verification_status` against the enum but accepts `Unverified`; it does not require `Verified` for `Approved`. Policy manual controls M-02 and M-03 explicitly leave the reality of approval and evidentiary support to an approver/reviewer. Thus the current implementation does not satisfy Issue #1189 criterion 6 as written.

**Minimum path:** a separately authorized governance change must define the exact rule for Approved + missing approver/date and Approved + Unverified, add positive and negative fixtures (including mutation controls), and demonstrate the required CI job on the exact resulting commit. This AID-2026-105 evidence-only change does not modify checker, schema, tests, workflow, runtime or validator semantics.

## 6. Minimum closure path

1. Accountable Owner C records acceptance or rejection of the exact current Design Principles and Architecture Invariants versions, separately naming P-01–P-16 and I-01–I-24 scope.
2. Required joint Owner A and governance approver record their authority-specific acceptance against the same exact six current path/blob pairs and the exact evidence package. Each record must preserve its true attribution; proxy registration is not a natural-person signature.
3. The authorized decision-maker resolves whether the #904 metadata-only schema migration is approval-neutral under the AID-096 exact-blob statement, or supplies a new approval event / updated exact blob scope. No inference is made here.
4. Reconcile the contradictory verification notes and proposed-status prose, then read back Canonical/EN/ZH-CN semantic parity and source revision pins at one commit. Do not change normative content without authorization.
5. Separately authorize and implement the GOV-DOC-002 enforcement gap for missing approver/date and unverified Approved status; attach raw test and CI output.
6. Independently verify all DEC-13 checklist items, attach the exact-head verification output, and only then consider #1189 closure. Production or P-01–P-16 implementation conformance is not claimed by this evidence record.

## 7. Explicit non-claims

- No historical approver is identified or inferred.
- No natural-person Owner or governance-approver acceptance is claimed.
- No proxy role disposition is relabelled as a human signature.
- No current Git blob is claimed to equal an AID-096 original approved blob.
- No semantic parity or governance-check criterion is marked PASS without evidence.
- No runtime, validator, schema, test, workflow, canonical source or production state is changed by this work item.
- Issue #1189 remains OPEN.
