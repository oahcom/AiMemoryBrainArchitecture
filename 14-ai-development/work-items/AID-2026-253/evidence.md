---
document_metadata:
  domain: architecture-governance
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
        - "14-ai-development/work-items/AID-2026-253/evidence.md"
        - "docs/en/13-engineering-decisions/REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md"
      revocation: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-27"
      last_verification_note: "Live GitHub main and Owner branch refs were fetched; unresolved Owner acceptance and implementation evidence remain explicit."
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
    canonical_scope: "AID-2026-253 AC3/AC4 evidence and bounded delegated dispositions"
    canonical_scope_id: "architecture-governance/aid-2026-253"
    canonical_scope_keywords:
      - "conflict-register"
      - "mature-implementations"
      - "AC3"
      - "AC4"
      - "evidence"
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# AID-2026-253 — W10 AC3/AC4 evidence and bounded disposition

Repository: oahcom/AiMemoryBrainArchitecture  
Observed main: f18adc9fa1d06837433a09498f5297bf13b35756  
Attribution: user-authorized operator (delegated by account owner)  
Date: 2026-11-27  
Decision status: proxy ruling, not a natural-person Owner signature

## 1. Baseline and method

The supplied 788fbc01 prefix did not identify the live default-branch head at execution time. The live GitHub Branch API returned f18adc9fa1d06837433a09498f5297bf13b35756. All observations below use that fetched main head or explicitly named live Owner branch refs. Main recursive tree: 23620e7a8d4f7ddf7124d134471521c7c7b04778; truncated=false; 1,038 entries; 887 blobs.

Reproduction commands:

```bash
curl -fsSL https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/branches/main | jq -r '.commit.sha'
curl -fsSL 'https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/git/trees/23620e7a8d4f7ddf7124d134471521c7c7b04778?recursive=1' | jq -r '[.truncated, (.tree|length), ([.tree[]|select(.type=="blob")]|length)]'
```

Observed output:

```text
f18adc9fa1d06837433a09498f5297bf13b35756
[false, 1038, 887]
```

Main now contains roots 03-memory-brain, 04-memory-compiler, 05-memory-runtime, 06-memory-context, 08-bmcp-protocol, 09-security-governance and 10-storage-consistency. Directory presence is not itself Owner approval or a governed portal-map acceptance.

## 2. Per-conflict closure assessment

A status changes only where the row's own closure condition is supported. The old status is the live register value before this work.

| CF | Old status | New status | Assessment / missing evidence |
|---|---|---|---|
| CF-001 | OPEN | OPEN | Main now contains the subsystem roots, but exact A + affected-Owner approval of canonical path names and complete governed portal/source-link approval are absent. Missing: version-pinned path approvals and accepted links for every affected source. |
| CF-002 | OPEN | OPEN | The 2026-11-18 currentness addendum corrects the false claim that 02-domain-model was absent. PR #89 is now merged, not an Open/Draft historical PR as the closure condition says to preserve. Missing: explicit governance disposition reconciling the merged historical report with that condition; no PR history is rewritten. |
| CF-003 | OPEN | OPEN | Main has 08-bmcp-protocol, but docs/README.md does not link that root and no current H Owner canonical-path approval is pinned. Missing: H exact-path confirmation and A's governed portal-map update. |
| CF-004 | OPEN | OPEN | Main has 09-security-governance; its index remains Draft/Informative and does not disposition the alternate 10-security-and-governance path/copies. Missing: I canonical-directory decision and explicit alternate-path disposition. |
| CF-005 | OPEN | OPEN | Main has 10-storage-consistency, but no root README/index was found. ADR-RUN-001 remains PROPOSED and does not establish Storage L1/L4 authority. Missing: Storage canonical source index and exact accepted L1/L4 status. |
| CF-006 | ADR-BLOCKED | RECONCILED — SEMANTIC/IDENTITY DECISION ONLY | Main contains OWNER-DECISION-FACT-CLAIM-001.md, Blob 2225dcb469db37dbebe8d8bab202f3ea4f8b600b, metadata decision_status Approved, authority Project Owner delegate under Issue #305 comment 7042461592. It selects separate Fact attestation / Claim proposition and I1 stable Claim identity plus immutable revisions. It expressly does not freeze JSON Schema, DDL, public API, BMCP wire fields or Runtime implementation. Those downstream freezes remain outside this closure. |
| CF-007 | OPEN | OPEN | SQLite adapter code/tests exist, but ADR-RUN-001 remains PROPOSED and disclaims database deployment/recovery validation. Missing: accepted row ownership and L4 profile plus crash/failover/restore evidence. |
| CF-008 | P0 OPEN | P0 OPEN | I's source-root README says restored contracts remain Draft/Informative; G's package says global Applied/Forget and crash/restore are not frozen/verified. Missing: closed-world inventory, barriers, evidence joins and restore proof accepted by D/I/consumers. |
| CF-009 | OPEN | OPEN | Live H branch session-h-bmcp-protocol is 3e8b33df18b9e6fc757ca84ff07a12faebc78e74; tree a03964fc62dea1b7eb50dafdec6adc5d0795fa0e has 282 entries / 249 blobs, not truncated. Compare from intact baseline 0d36324457e39bd50ad56ae902d477c4ea765b61: ahead 80, behind 0. Compare from incident 0277a8b9ee63be850acc0b8b1b08625524aaa33: merge-base is the incident commit (ahead 79, behind 0), so the incident IS in current ancestry, contrary to PR #90's older narrative. Missing: current exact restoration/ancestry record explaining this ancestry and pinning the live tree digest. |
| CF-010 | RECONCILED FOR TREE CURRENTNESS | RECONCILED FOR TREE CURRENTNESS | Live C branch session-c-agent-integration-2026-11-16 is 3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c; tree db46a6d75cad94040cd5d5be236ce0c68e0964b8 has 160 entries / 138 blobs, not truncated. Compare from incident a5dff993e5c2928a28deb777c41023cfe923366f: ahead 11, behind 0. This remains only the bounded tree-currentness reconciliation, not C/Brain end-to-end proof. |
| CF-011 | P0 OPEN | P0 OPEN | Main G README says Phase 3.8.22 is a design draft, implementation NOT VERIFIED, crash/restart/restore tests NOT RUN and C/G/H Applied freeze NO. Missing: exact field mapping, identity, persistence and crash recovery acceptance by C/G/H/I/D/Storage. |
| CF-012 | OPEN | OPEN | PR #94 is merged; its body records successful schema-only trigger and restore runs. Missing: one exact compatible C/H/Storage bundle manifest and proof that pinned versions are compatible at current Owner heads. |
| CF-013 | CANDIDATE | CANDIDATE | New record DEFERs Cedar production PDP selection. Missing: wrapper conformance vectors, revocation tests and I/Security Owner approval. |
| CF-014 | OPEN | OPEN | New record DEFERs both final SQLite and PostgreSQL L4 profiles. Missing: representative Brain workload and complete comparative atomicity/HA/backup/restore/operations evidence. |
| CF-015 | OPEN | OPEN | Several roots have EN/ZH-CN companions, but E README still identifies detailed Owner sources whose full bilingual companions remain pending. Missing: per-contract semantic parity and exact Owner review. |
| CF-016 | OPEN | OPEN | PRs #74–#79 and #89 are merged research publications, not product approvals. Main README says product-level runtime has not started and production validation is not established. Missing: exact Owner ADR plus measured conformance for each recommendation. |

### Command/result anchors

```text
GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main
  commit.sha = f18adc9fa1d06837433a09498f5297bf13b35756

GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/89
  state=closed, merged=true, draft=false

GET /repos/oahcom/AiMemoryBrainArchitecture/pulls/94
  state=closed, merged=true
  schema-only trigger run 44151284885 SUCCESS
  restored-schema run 44151338457 SUCCESS

GET /repos/oahcom/AiMemoryBrainArchitecture/branches/session-h-bmcp-protocol
  head=3e8b33df18b9e6fc757ca84ff07a12faebc78e74
  tree=a03964fc62dea1b7eb50dafdec6adc5d0795fa0e
  recursive tree: 282 entries, 249 blobs, truncated=false

GET /repos/oahcom/AiMemoryBrainArchitecture/branches/session-c-agent-integration-2026-11-16
  head=3e7640cbe8a3d5c1dc95b6a0b887a1c41f62916c
  tree=db46a6d75cad94040cd5d5be236ce0c68e0964b8
  recursive tree: 160 entries, 138 blobs, truncated=false
```

## 3. Mature implementation decisions

Four bounded DEFER decisions are recorded in REQ04-MATURE-IMPLEMENTATION-DISPOSITIONS-001.md and its Chinese counterpart: SQLite local profile; PostgreSQL server profile; Cedar PDP; Tantivy. Each has reasons and concrete reopen triggers. Tantivy is explicitly DEFER, NOT REJECTED.

## 4. Register status

The register remains DRAFT / OPEN REGISTER / NON-NORMATIVE. Two of sixteen rows meet their stated bounded closure condition (CF-006 semantic/identity decision; CF-010 tree currentness): 2/16 = 12.5%. Fourteen remain OPEN, ADR-BLOCKED, P0 OPEN or CANDIDATE. No implementation or production activation is authorized.

## 5. AC recommendation

- AC3: retain PARTIAL. All 16 conflicts have evidence, but only 2/16 meet their own bounded closure conditions; 14 have named missing evidence/Owner actions.
- AC4: recommend SATISFIED for “mature implementations are considered”: four explicit DEFER dispositions exist, each with reasons and reopen triggers. This does not claim that any is selected for production.
