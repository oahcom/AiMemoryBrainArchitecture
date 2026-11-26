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
        - "AID-2026-193/manifest.yaml"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Counts in this record were produced by running the commands in section 2 on the committed tree: 84 absent paths, 300 fixed-string occurrences, 30 annotated lines in 19 files, 6 lines deferred with the gate output quoted. No CI result, merge SHA or Owner decision is claimed."
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
    canonical_status: Canonical
    canonical_scope: "AID-2026-193 annotation of the live citations of the 84 09-security-governance paths that are absent from main"
    canonical_scope_id: "ai-development/aid-2026-190-dangling-09-security-governance-citations"
    canonical_scope_keywords:
      - "security-governance"
      - "dangling-reference"
      - "aid-2026-107"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: "docs/en/14-ai-development/work-items/AID-2026-193/evidence.md"
    zh-CN: "docs/zh-CN/14-ai-development/work-items/AID-2026-193/evidence.md"
---


# AID-2026-193 — 84 `09-security-governance/` paths absent from main: live citations annotated, nothing restored

**Status: DRAFT — annotation only.** This work item edits 19 documents, 30 lines in
total, and defers 6 further lines with the gate evidence for why. It creates no file
under `09-security-governance/`, changes no normative body, deletes no reference and
promotes no reference to a clickable link. Each edited line keeps its original path text
verbatim and gains one parenthetical note: `(not restored on main; see AID-2026-107 §10)`.

## 1. Why this record exists

The dispatched contract reported "85 references to `09-security-governance/` documents
that do not exist". Re-measured at `0c752ee6ee186e494e35aa74447f263891ca4842`, the cited set is 91 distinct path strings,
of which 84 have no file anywhere in the tree. The 85th of the dispatch was produced by
testing existence at the root directory only: `09-security-governance/security-governance-guide.md`
is absent there but present under `docs/en/` and `docs/zh-CN/`, and no citation names it
root-relative, so it does not dangle. 91 = 84 absent + 7 present.

A path string that resolves to nothing is not by itself a defect. 252 of the 300
occurrences are rows of the AID-2026-107 section 10.4 adjudication register, whose whole
purpose is to record these paths as candidates that are *not* on main, each with the
Owner-branch blob it came from and a disposition. A further 12 are verbatim before/after
quotes inside AID-2026-170's evidence, where the surrounding text is a recorded diff.
The remaining 36 occurrences in 23 documents are live citations: a reader has no way to
tell that the path is a historical pin on an Owner branch rather than a file on main.
30 of those 36 are annotated here; the other 6 are deferred under section 5.3 because
annotating them requires a paired change to bilingual counterparts that do not exist.

The note is a pointer, not a disposition. It says the file is not on main and sends the
reader to the register that already adjudicated it. It does not assert that the document
is unnecessary, superseded or approved for restoration; for the 49 `UNDECIDED` rows that
remains the relevant Owner's call.

## 2. Measurement

All commands were run in this worktree with `PYTHONUTF8=1`. Base is `origin/main` =
`0c752ee6ee186e494e35aa74447f263891ca4842` (`Merge pull request #1340`).

```
refs   = git grep -oh "09-security-governance/[A-Za-z0-9._-]*\.md" origin/main -- "*.md" | sort -u
tree   = git ls-tree -r --name-only origin/main
absent = refs with no tree entry equal to it and no tree entry ending in "/" + it
occ    = git grep -n -F <path> -- "*.md"      # for each absent path
after  = git grep -F "not restored on main; see AID-2026-107" -- "*.md"
```

| Quantity | Before | After |
|---|---:|---:|
| Distinct `09-security-governance/*.md` strings cited | 91 | 91 |
| Of those, absent from the whole tree | 84 | 84 |
| Occurrences of the 84 absent paths (fixed-string, `*.md`) | 300 | 300 |
| Occurrences carrying the note | 0 | 30 |
| AID-2026-107 section 10.4 register rows (3 renditions) | 252 | 252 |
| AID-2026-170 verbatim diff quotes (3 renditions x 4 lines) | 12 | 12 |
| Live citations deferred with gate evidence | 6 | 6 |
| Files edited | 0 | 19 |
| Clickable markdown links among the 84 | 0 | 0 |
| Files created under `09-security-governance/` | 0 | 0 |

300 = 252 + 12 + 30 + 6. The split is stable because the note is appended after the path
text: all 300 path strings remain findable by fixed-string grep, which is what makes a
future restoration traceable back to its citations.

Reference forms: every one of the 36 live citations is backticked inline code, an
unbackticked table cell, or a bare bullet line. None is a markdown link, and the only two
link-form occurrences of a `09-security-governance/` path in the tree — the
`security-governance-guide.md` counterpart lines under `docs/{en,zh-CN}/09-security-governance/`
— point at files that exist. The contract's "demote a clickable link to plain text"
branch therefore has no instance; every edit is the first branch (keep the path text,
add the note).

## 3. Complete inventory: 84 absent paths and every site that cites them

Rows come from the fixed-string grep above, so a path cited twice in one document appears
twice in its site list. `annotated` = the note was added at that site; `deferred` = the
note was withheld for the reason in section 5.3; `register row` = a row of AID-2026-107
section 10.4 that already records the absence; `verbatim quote` = a quoted diff line in
AID-2026-170.

| # | Missing path | Citations | Referencing site(s) | Handling |
|---|---|---:|---|---|
| 1 | `09-security-governance/audit-and-exception-governance.md` | 6 | `14-ai-development/work-items/AID-2026-107/evidence.md:432`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:429`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:429`, `prompts/I/phase-3-remediation.md:49`, `reviews/integration/phase-3-cross-module-remediation-task-pack.md:352`, `reviews/integration/phase-3-session-kickoff-prompts.md:404` | annotated + register row |
| 2 | `09-security-governance/governance-decision-register.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:435`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:432`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:432` | register row |
| 3 | `09-security-governance/phase-3-global-forget-remediation-report.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:436`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:433`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:433` | register row |
| 4 | `09-security-governance/phase-3.5-global-identity-forget-governance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:437`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:434`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:434` | register row |
| 5 | `09-security-governance/phase-3.6-bih-joint-architecture-acceptance-addendum.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:438`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:435`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:435` | register row |
| 6 | `09-security-governance/phase-3.6-cgh-applied-1.0-i-authority-confirmation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:439`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:436`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:436` | register row |
| 7 | `09-security-governance/phase-3.6-cgh-applied-1.0-i-owner-authoritative-confirmation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:440`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:437`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:437` | register row |
| 8 | `09-security-governance/phase-3.6-governance-acceptance-execution-addendum.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:441`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:438`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:438` | register row |
| 9 | `09-security-governance/phase-3.6-governance-approval-and-consumer-acceptance-register.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:442`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:439`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:439` | register row |
| 10 | `09-security-governance/phase-3.6-i-commit-authorization-causal-order-contract.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:443`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:440`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:440` | register row |
| 11 | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | 10 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md:10`, `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md:29`, `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:79`, `14-ai-development/work-items/AID-2026-107/evidence.md:444`, `docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md:22`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:441`, `docs/governance/owner-branch-translation-inventory.md:111`, `docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md:22`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:441`, `reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md:19` | annotated + deferred + register row |
| 12 | `09-security-governance/phase-3.6-permission-epoch-and-authorization-formal-confirmation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:445`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:442`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:442` | register row |
| 13 | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | 5 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md:30`, `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:80`, `14-ai-development/work-items/AID-2026-107/evidence.md:446`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:443`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:443` | annotated + deferred + register row |
| 14 | `09-security-governance/phase-3.6-r1-r2-i-owner-gate-linearization-decision-candidate.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:447`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:444`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:444` | register row |
| 15 | `09-security-governance/phase-3.6-six-dimension-self-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:448`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:445`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:445` | register row |
| 16 | `09-security-governance/phase-3.6.10-i-exact-version-recovery-cutoff-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:449`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:446`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:446` | register row |
| 17 | `09-security-governance/phase-3.6.14-i-exact-review-storage-v3.2.4-successor-manifest.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:450`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:447`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:447` | register row |
| 18 | `09-security-governance/phase-3.6.2-i-coc-jf10-composition-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:451`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:448`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:448` | register row |
| 19 | `09-security-governance/phase-3.6.2-jf10-commit-authorization-recovery-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:452`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:449`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:449` | register row |
| 20 | `09-security-governance/phase-3.6.2-jf10-owner-gate-ordering-correction.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:453`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:450`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:450` | register row |
| 21 | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md` | 5 | `14-ai-development/work-items/AID-2026-107/evidence.md:454`, `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:124`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:451`, `docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:124`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:451` | annotated + register row |
| 22 | `09-security-governance/phase-3.6.3-i-coc-durable-protocol-authority-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:455`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:452`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:452` | register row |
| 23 | `09-security-governance/phase-3.6.4-global-forget-evidence-reconciliation.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:456`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:453`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:453` | register row |
| 24 | `09-security-governance/phase-3.6.4-global-forget-reference-model-evidence.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:457`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:454`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:454` | register row |
| 25 | `09-security-governance/phase-3.6.4-i-prepared-participant-gid-authorization-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:458`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:455`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:455` | register row |
| 26 | `09-security-governance/phase-3.6.5-i-restore-control-highwater-acceptance.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:459`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:456`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:456` | register row |
| 27 | `09-security-governance/phase-3.6.5-i36-governance-decision-proposal.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:460`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:457`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:457` | register row |
| 28 | `09-security-governance/phase-3.6.6-i-global-inventory-authority-addendum.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:461`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:458`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:458` | register row |
| 29 | `09-security-governance/phase-3.6.7-i-exact-version-owner-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:462`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:459`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:459` | register row |
| 30 | `09-security-governance/phase-3.6.7-i-owner-local-gate-admission-release-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:463`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:460`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:460` | register row |
| 31 | `09-security-governance/phase-3.6.8-i-exact-version-owner-rereview-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:464`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:461`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:461` | register row |
| 32 | `09-security-governance/phase-3.6.8-i-exact-version-r1-r4-rereview-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:465`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:462`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:462` | register row |
| 33 | `09-security-governance/phase-3.6.8-i-global-inventory-receipt-restore-currentness-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:466`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:463`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:463` | register row |
| 34 | `09-security-governance/phase-3.6.9-i-r1-r2-exact-version-delegated-disposition.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:467`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:464`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:464` | register row |
| 35 | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | 8 | `14-ai-development/work-items/AID-2026-107/evidence.md:468`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:465`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:465`, `reviews/architecture/SYS-RISK-001.en.md:427`, `reviews/architecture/SYS-RISK-001.zh-CN.md:426`, `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:9`, `reviews/integration/phase-3.8.2-callable-interface-convergence.en.md:24`, `reviews/integration/phase-3.8.2-callable-interface-convergence.zh-CN.md:24` | annotated + register row |
| 36 | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | 7 | `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md:43`, `14-ai-development/work-items/AID-2026-107/evidence.md:469`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:466`, `docs/research/product-first/PRODUCT-FIRST-001-SESSION-01-MEMORY-PRODUCTS.md:93`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:466`, `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:11`, `reviews/technology-reality/TECH-REALITY-001-A-independent-review-follow-up.md:58` | annotated + deferred + register row |
| 37 | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | 12 | `14-ai-development/work-items/AID-2026-107/evidence.md:470`, `14-ai-development/work-items/AID-2026-170/evidence.md:70`, `14-ai-development/work-items/AID-2026-170/evidence.md:82`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:467`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:70`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:82`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:467`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:70`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:82`, `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:67`, `reviews/architecture/SYS-RISK-001.en.md:297`, `reviews/architecture/SYS-RISK-001.zh-CN.md:296` | annotated + register row + verbatim quote |
| 38 | `09-security-governance/phase-3.8.10-i-scope-clarification-c-profile-identifier.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:471`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:468`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:468` | register row |
| 39 | `09-security-governance/phase-3.8.11-i-exact-review-unified-1.2.13-recoveryjoin-1.0.2-p0.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:472`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:469`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:469` | register row |
| 40 | `09-security-governance/phase-3.8.11-i-review-storage-serialization-anchor.md` | 4 | `14-ai-development/work-items/AID-2026-107/evidence.md:473`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:470`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:470`, `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:68` | annotated + register row |
| 41 | `09-security-governance/phase-3.8.12-i-exact-compatibility-h-unified-1.2.14-recoveryjoin-1.0.2.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:474`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:471`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:471` | register row |
| 42 | `09-security-governance/phase-3.8.12-i-exact-review-h-unified-1.2.14-current-schema-p0.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:475`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:472`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:472` | register row |
| 43 | `09-security-governance/phase-3.8.13-i-exact-review-h-authority-join-mapping-1.2.14.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:476`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:473`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:473` | register row |
| 44 | `09-security-governance/phase-3.8.13-i-review-h-1.2.14-authority-callback-contract.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:477`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:474`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:474` | register row |
| 45 | `09-security-governance/phase-3.8.13-i-review-h-terminal-authority-verifier-seam.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:478`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:475`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:475` | register row |
| 46 | `09-security-governance/phase-3.8.14-i-final-compatibility-h-1.2.14-callback-and-recoveryjoin.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:479`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:476`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:476` | register row |
| 47 | `09-security-governance/phase-3.8.14-i-review-h-full-path-terminal-callback-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:480`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:477`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:477` | register row |
| 48 | `09-security-governance/phase-3.8.15-i-exact-review-h-expanded-full-path-commit-won-callback.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:481`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:478`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:478` | register row |
| 49 | `09-security-governance/phase-3.8.15-i-review-h-expanded-full-path-terminal-and-envelope-auth-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:482`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:479`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:479` | register row |
| 50 | `09-security-governance/phase-3.8.16-i-exact-rereview-h-c-p0-projection-test-39-method-ci.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:483`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:480`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:480` | register row |
| 51 | `09-security-governance/phase-3.8.16-i-exact-review-h-42-test-commit-won-and-absence-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:484`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:481`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:481` | register row |
| 52 | `09-security-governance/phase-3.8.16-i-review-h-c-p0-nullable-coc-and-envelope-auth-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:485`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:482`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:482` | register row |
| 53 | `09-security-governance/phase-3.8.17-i-review-h-outer-envelope-authenticated-ingress-gate.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:486`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:483`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:483` | register row |
| 54 | `09-security-governance/phase-3.8.17-i-review-h-outer-envelope-authentication-trust-boundary.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:487`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:484`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:484` | register row |
| 55 | `09-security-governance/phase-3.8.18-i-exact-review-h-authenticated-ingress-envelope-trust-boundary.md` | 4 | `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:81`, `14-ai-development/work-items/AID-2026-107/evidence.md:488`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:485`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:485` | annotated + register row |
| 56 | `09-security-governance/phase-3.8.18-i-review-c-outer-envelope-signer-p0-trust-registration.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:489`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:486`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:486` | register row |
| 57 | `09-security-governance/phase-3.8.18-i-review-h-explicit-outer-signature-profile-requirement.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:490`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:487`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:487` | register row |
| 58 | `09-security-governance/phase-3.8.19-i-exact-review-c-outer-envelope-p0-correction.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:491`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:488`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:488` | register row |
| 59 | `09-security-governance/phase-3.8.19-i-review-c-separate-h-gateway-attestation-trust-model.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:492`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:489`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:489` | register row |
| 60 | `09-security-governance/phase-3.8.2-i-recovery-join-trust-currentness-exact-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:493`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:490`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:490` | register row |
| 61 | `09-security-governance/phase-3.8.20-i-exact-review-h-gateway-attestation-p0-candidate.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:494`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:491`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:491` | register row |
| 62 | `09-security-governance/phase-3.8.21-i-exact-rereview-h-gateway-attestation-p0-digest-encoding.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:495`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:492`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:492` | register row |
| 63 | `09-security-governance/phase-3.8.22-i-exact-review-h-unified-1.2.15-gateway-attestation-schema.md` | 5 | `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md:315`, `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md:344`, `14-ai-development/work-items/AID-2026-107/evidence.md:496`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:493`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:493` | deferred + register row |
| 64 | `09-security-governance/phase-3.8.23-i-rereview-h-gateway-attestation-replay-acceptance-order.md` | 4 | `14-ai-development/work-items/AID-2026-107/evidence.md:497`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:494`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:494`, `reviews/architecture-breakthrough/integration/evidence-source-ledger.md:126` | annotated + register row |
| 65 | `09-security-governance/phase-3.8.24-i-exact-review-h-applied-delivery-evidence-replay-authorization.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:498`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:495`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:495` | register row |
| 66 | `09-security-governance/phase-3.8.3-i-cryptographic-trust-profile-proposal.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:499`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:496`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:496` | register row |
| 67 | `09-security-governance/phase-3.8.3-i-exact-review-h-crypto-wire-mapping-r3.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:500`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:497`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:497` | register row |
| 68 | `09-security-governance/phase-3.8.3-i-exact-review-h-crypto-wire-mapping.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:501`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:498`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:498` | register row |
| 69 | `09-security-governance/phase-3.8.3-i-re-review-h-crypto-wire-mapping-r2.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:502`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:499`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:499` | register row |
| 70 | `09-security-governance/phase-3.8.4-i-c-provider-outcome-trust-boundary-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:503`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:500`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:500` | register row |
| 71 | `09-security-governance/phase-3.8.4-i-crypto-profile-artifact-revision-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:504`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:501`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:501` | register row |
| 72 | `09-security-governance/phase-3.8.4-i-exact-review-h-membership-proof-bundle.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:505`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:502`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:502` | register row |
| 73 | `09-security-governance/phase-3.8.4-i-exact-review-h-unified-manifest-1.2.11.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:506`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:503`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:503` | register row |
| 74 | `09-security-governance/phase-3.8.4-i-owner-snapshot-membership-proof-contract.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:507`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:504`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:504` | register row |
| 75 | `09-security-governance/phase-3.8.5-i-exact-review-h-unified-1.2.13-owner-proof-compatibility.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:508`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:505`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:505` | register row |
| 76 | `09-security-governance/phase-3.8.5-i-recoveryjoin-1.0.2-unified-1.2.12-wire-adoption-amendment.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:509`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:506`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:506` | register row |
| 77 | `09-security-governance/phase-3.8.5-i-storage-logical-serialization-topology-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:510`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:507`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:507` | register row |
| 78 | `09-security-governance/phase-3.8.6-i-c-outcome-crypto-profile-trust-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:511`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:508`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:508` | register row |
| 79 | `09-security-governance/phase-3.8.7-i-exact-signed-object-p0-allowlists.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:512`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:509`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:509` | register row |
| 80 | `09-security-governance/phase-3.8.7-i-h-owner-snapshot-attestation-schema-review.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:513`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:510`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:510` | register row |
| 81 | `09-security-governance/phase-3.8.8-i-crypto-profile-architecture-decision.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:514`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:511`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:511` | register row |
| 82 | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | 11 | `14-ai-development/work-items/AID-2026-107/evidence.md:515`, `14-ai-development/work-items/AID-2026-170/evidence.md:64`, `14-ai-development/work-items/AID-2026-170/evidence.md:76`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:512`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:64`, `docs/en/14-ai-development/work-items/AID-2026-170/evidence.md:76`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:512`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:64`, `docs/zh-CN/14-ai-development/work-items/AID-2026-170/evidence.md:76`, `reviews/architecture/SYS-RISK-001.en.md:77`, `reviews/architecture/SYS-RISK-001.zh-CN.md:77` | annotated + register row + verbatim quote |
| 83 | `09-security-governance/phase-3.9-i-d-forget-lifecycle-terminalization-authorization-proposal.md` | 3 | `14-ai-development/work-items/AID-2026-107/evidence.md:516`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:513`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:513` | register row |
| 84 | `09-security-governance/threat-model-and-adversarial-test-plan.md` | 6 | `14-ai-development/work-items/AID-2026-107/evidence.md:522`, `docs/en/14-ai-development/work-items/AID-2026-107/evidence.md:519`, `docs/zh-CN/14-ai-development/work-items/AID-2026-107/evidence.md:519`, `prompts/I/phase-3-remediation.md:48`, `reviews/integration/phase-3-cross-module-remediation-task-pack.md:351`, `reviews/integration/phase-3-session-kickoff-prompts.md:403` | annotated + register row |

## 4. The 30 live citations that were annotated

| # | Referencing site | Path cited | Form | Handling |
|---|---|---|---|---|
| 1 | `prompts/I/phase-3-remediation.md:49` | `09-security-governance/audit-and-exception-governance.md` | prose / bullet | note appended after the path text; path text unchanged |
| 2 | `reviews/integration/phase-3-cross-module-remediation-task-pack.md:352` | `09-security-governance/audit-and-exception-governance.md` | prose / bullet | note appended after the path text; path text unchanged |
| 3 | `reviews/integration/phase-3-session-kickoff-prompts.md:404` | `09-security-governance/audit-and-exception-governance.md` | prose / bullet | note appended after the path text; path text unchanged |
| 4 | `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:79` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | prose / bullet | note appended after the path text; path text unchanged |
| 5 | `docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md:22` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | table cell | note appended after the path text; path text unchanged |
| 6 | `docs/governance/owner-branch-translation-inventory.md:111` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | table cell | note appended after the path text; path text unchanged |
| 7 | `docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md:22` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | table cell | note appended after the path text; path text unchanged |
| 8 | `reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md:19` | `09-security-governance/phase-3.6-identity-trust-policy-joint-closure.md` | table cell | note appended after the path text; path text unchanged |
| 9 | `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:80` | `09-security-governance/phase-3.6-principal-trust-chain-authorization-revocation.md` | prose / bullet | note appended after the path text; path text unchanged |
| 10 | `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:124` | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md` | prose / bullet | note appended after the path text; path text unchanged |
| 11 | `docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md:124` | `09-security-governance/phase-3.6.2-jf10-v2-i-owner-disposition.md` | prose / bullet | note appended after the path text; path text unchanged |
| 12 | `reviews/architecture/SYS-RISK-001.en.md:427` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | table cell | note appended after the path text; path text unchanged |
| 13 | `reviews/architecture/SYS-RISK-001.zh-CN.md:426` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | table cell | note appended after the path text; path text unchanged |
| 14 | `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:9` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | prose / bullet | note appended after the path text; path text unchanged |
| 15 | `reviews/integration/phase-3.8.2-callable-interface-convergence.en.md:24` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | table cell | note appended after the path text; path text unchanged |
| 16 | `reviews/integration/phase-3.8.2-callable-interface-convergence.zh-CN.md:24` | `09-security-governance/phase-3.7-i-current-authorization-enforcement-and-restore-proof.md` | table cell | note appended after the path text; path text unchanged |
| 17 | `docs/research/product-first/PRODUCT-FIRST-001-SESSION-01-MEMORY-PRODUCTS.md:93` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | prose / bullet | note appended after the path text; path text unchanged |
| 18 | `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md:11` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | prose / bullet | note appended after the path text; path text unchanged |
| 19 | `reviews/technology-reality/TECH-REALITY-001-A-independent-review-follow-up.md:58` | `09-security-governance/phase-3.8-i-commit-authorization-receipt-and-revocation-sequencer-contract.md` | table cell | note appended after the path text; path text unchanged |
| 20 | `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:67` | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | table cell | note appended after the path text; path text unchanged |
| 21 | `reviews/architecture/SYS-RISK-001.en.md:297` | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | table cell | note appended after the path text; path text unchanged |
| 22 | `reviews/architecture/SYS-RISK-001.zh-CN.md:296` | `09-security-governance/phase-3.8.10-i-p0-allowlists-unified-1.2.14-recoveryjoin-1.0.2.md` | table cell | note appended after the path text; path text unchanged |
| 23 | `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md:68` | `09-security-governance/phase-3.8.11-i-review-storage-serialization-anchor.md` | table cell | note appended after the path text; path text unchanged |
| 24 | `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md:81` | `09-security-governance/phase-3.8.18-i-exact-review-h-authenticated-ingress-envelope-trust-boundary.md` | prose / bullet | note appended after the path text; path text unchanged |
| 25 | `reviews/architecture-breakthrough/integration/evidence-source-ledger.md:126` | `09-security-governance/phase-3.8.23-i-rereview-h-gateway-attestation-replay-acceptance-order.md` | prose / bullet | note appended after the path text; path text unchanged |
| 26 | `reviews/architecture/SYS-RISK-001.en.md:77` | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | prose / bullet | note appended after the path text; path text unchanged |
| 27 | `reviews/architecture/SYS-RISK-001.zh-CN.md:77` | `09-security-governance/phase-3.8.9-i-p0-allowlists-unified-1.2.13-recoveryjoin-1.0.2.md` | prose / bullet | note appended after the path text; path text unchanged |
| 28 | `prompts/I/phase-3-remediation.md:48` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | prose / bullet | note appended after the path text; path text unchanged |
| 29 | `reviews/integration/phase-3-cross-module-remediation-task-pack.md:351` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | prose / bullet | note appended after the path text; path text unchanged |
| 30 | `reviews/integration/phase-3-session-kickoff-prompts.md:403` | `09-security-governance/threat-model-and-adversarial-test-plan.md` | prose / bullet | note appended after the path text; path text unchanged |

## 5. The 270 occurrences that were not annotated

### 5.1 The register rows (252)

`14-ai-development/work-items/AID-2026-107/evidence.md` section 10.4 and its `docs/en`
and `docs/zh-CN` renditions list all 84 paths (84 x 3 = 252 rows). Each row already
carries the Owner-branch blob SHA, a classification (`NORMATIVE_ROOT`,
`HISTORICAL_PHASE_RECORD`, `UNDECIDED`) and a basis code, and section 10.1 states the
file-level scope as paths absent from main. Appending "not restored on main" to the body
of the register that exists to say exactly that adds no information, makes the table
harder to read, and would make this work item's pointer point at an annotated copy of
itself.

### 5.2 The verbatim quotes (12)

`14-ai-development/work-items/AID-2026-170/evidence.md` quotes four table rows twice —
before and after that work item's change — in three renditions. Those quotes are the
evidence that one specific cell changed and nothing else did. Editing the quoted text
would break the quote against the document it quotes
(`reviews/architecture/SYS-RISK-001.{en,zh-CN}.md`), so the quotes stay byte-identical and
the note went on the annotated original.

### 5.3 Deferred live citations (6 lines in 4 documents)

- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md`
- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md`
- `13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md`
- `13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md`

These four documents live under `13-engineering-decisions/`, a `NORMATIVE_ROOTS` entry.
`scripts/check_bilingual_docs.py` requires a change to such a document to be accompanied
by changes to all of its bilingual counterparts in the same PR. The counterparts do not
exist — they are among the 77 language pairs the repository already records as absent —
so the requirement can only be met by creating them, which is a document-creation
decision outside this unit. Annotating these four files was measured first, and the gate
rejected exactly that:

```
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/baseline-currentness-and-owner-source-audit.md
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/canonical-identity-semantics.md
::error::13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md requires all counterparts changed in this PR: 13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md, docs/en/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md, docs/zh-CN/13-engineering-decisions/domain-model-research/DOMAIN-REALITY-001-B/cross-owner-canonical-semantics-matrix.md
::error::13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md requires all counterparts changed in this PR: 13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md, docs/en/13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md, docs/zh-CN/13-engineering-decisions/technology-research/TECH-REALITY-001-A/owner-remediation/OWNER-REMEDIATION-001.md
Bilingual documentation gate: FAIL
```

The change was therefore reverted, not worked around: no exemption was claimed, no
counterpart was invented, and the bilingual gate was not edited. The 6 lines remain as
they were, still greppable, and are listed here so that a follow-up unit that owns the
13-engineering-decisions mirror set can annotate them in the same PR as their pairs.

## 6. Gate results

Local runs on the annotation commit `c1de9baa9af1e245f9ebe39e955a835dbb557910`, `PYTHONUTF8=1`:

```
$ python scripts/check_bilingual_docs.py
NOTE: 18 changed .md path(s) outside NORMATIVE_ROOTS were not pairing-checked
bilingual baseline: 77 frozen, 0 new gaps
exemptions: 21
Bilingual documentation and prompt-library gate: PASS (19 changed paths inspected).
This is a structural gate only; semantic parity requires independent review.

$ python scripts/check_document_management.py
INCOMPLETE: no rule violations in 496 classified documents, but 446 governed documents are still unclassified
GOV-DOC-002: 942 governed documents, 496 classified, 446 unclassified
DM-10 out-of-scope stale bindings: 0

$ python scripts/ci/check_line_endings.py
Line-ending check: 1629 files inspected, 0 binary skipped, 0 violations.

$ python scripts/ci/check_manifest_parse.py
Manifest parse: 94 manifests found, 94 parsed, 0 failed.

$ python scripts/ci/check_repository_hygiene.py --base <base> --head <head>
Work-item index membership version=2026-11-24.8 directories=105 linked=105
Work-item manifest consistency version=2026-11-24.8 manifests=93 in_scope=80 excluded_by_record_type=4 unrecognized=9 violations=0
Repository new-file admission passed: 0 new path(s) checked.

$ python scripts/check_session_evidence_workflow_shape.py
SESSION EVIDENCE WORKFLOW SHAPE: PASS

$ python scripts/check_traceability.py --index-only
PASS TRACEABILITY: 0 requirements / 93 work items / 0 errors / 105 warnings

$ python scripts/check_governance_operation_traceability.py
GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)
```

`check_document_management.py` exits 2 with `INCOMPLETE` because 446 governed documents
are still unclassified. That is the repository's standing state at this base — the same
line was produced on the unmodified tree before any edit — and it reports
`no rule violations`, which is what this change must not add to. It did not: the three
summary lines are identical before and after.

`check_bilingual_docs.py` needs `PR_BODY` on stdin-equivalent env to see the manifest
token; it reports `77 frozen, 0 new gaps` because no path was added, removed or renamed,
and it classifies the 18 changed paths outside `NORMATIVE_ROOTS` as not pairing-checked,
which is the documented behaviour for those paths.

## 7. What was not done

- No file was created under `09-security-governance/`, in any rendition. The 84 paths
  remain absent; restoring any of them is a separate, per-path Owner decision.
- No body text under `09-security-governance/` was edited; no normative statement,
  classification or disposition changed.
- No reference was deleted and no path text was reworded, abbreviated or aliased. The
  note is additive, so `git grep -F <path>` still finds all 300 occurrences.
- No path was converted to a markdown link, and no link was created.
- No bilingual counterpart was created and no `BILINGUAL-EXCEPTION` was claimed for the
  four deferred documents.
- No CI context result, merge SHA or post-merge readback is claimed; section 6 is a local
  run on the stated SHA.
- No Issue was closed, no acceptance decision asserted, and no branch protection,
  registry, metadata schema or baseline changed.
- The 49 `UNDECIDED` rows of AID-2026-107 section 10.4 are still undecided.

## 8. Changed paths

- `14-ai-development/work-items/AID-2026-001/i-pre-002-identity-binding-audit.md`
- `docs/en/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- `docs/en/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md`
- `docs/governance/owner-branch-translation-inventory.md`
- `docs/research/product-first/PRODUCT-FIRST-001-SESSION-01-MEMORY-PRODUCTS.md`
- `docs/zh-CN/07-agent-integration/phase-3.6-c-submit-cross-authority-causal-order-contract.md`
- `docs/zh-CN/08-bmcp-protocol/phase-3.6-identity-binding-consumer-conformance-status.md`
- `prompts/I/phase-3-remediation.md`
- `reviews/architecture-breakthrough/integration/evidence-source-ledger.md`
- `reviews/architecture-feasibility/phase-3-b-to-a-protocol-and-storage-topology-review.md`
- `reviews/architecture/SYS-RISK-001.en.md`
- `reviews/architecture/SYS-RISK-001.zh-CN.md`
- `reviews/integration/phase-3-cross-module-remediation-task-pack.md`
- `reviews/integration/phase-3-session-kickoff-prompts.md`
- `reviews/integration/phase-3.8-i-authorization-context-and-operation-identity-boundary.md`
- `reviews/integration/phase-3.8.2-callable-interface-convergence.en.md`
- `reviews/integration/phase-3.8.2-callable-interface-convergence.zh-CN.md`
- `reviews/technology-reality/TECH-REALITY-001-A-independent-review-follow-up.md`
- `reviews/translation/2026-11-17-phase36-identity-applied-storage-source-audit.md`

## 9. Attribution

Annotation worker inside a dispatched repair contract; executing model
`opencode-go/deepseek-v4.1-flash`. No independent review, Owner acceptance or human
sign-off is claimed.
