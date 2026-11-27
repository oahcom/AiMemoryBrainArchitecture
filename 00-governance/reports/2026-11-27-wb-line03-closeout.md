---
document_metadata:
  steward: "Architecture Governance"
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
      decision_date: null
      approved_version:
        scheme: git
        value: null
      approval_scope:
        type: Full-document
      approval_applicability: Applicable-To-Current-Version
      evidence_reference: []
      revocation: null

    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: null

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
    canonical_status: Non-Canonical
    canonical_scope: null
    canonical_scope_id: null
    canonical_scope_keywords: []
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
---

# WB LINE 03 Closeout — Validator / Repository / MCP / Local Environment

**Status:** `PARTIAL` — every item carries direct evidence; six items remain `UNVERIFIED`, `NOT_REPRODUCED` or `NOT_VERIFIED` and are listed explicitly in §5.
**Record type:** development-baseline audit record. Non-normative. It changes no validator, gate, runtime, API, schema, wire semantics, work item, index row or ledger entry.
**Owner order:** `chatgpt-session-ops/scripts/accounts/acct6/replies/reply-6b08f751-112543.md`, section `### PROMPT-03`.
**Executing session:** LINE 03 executor subagent (this session); order target session `ses_migkoSVr1n3YBkwCfqs1AltZrM`; host opencode v2.4.2.
**Record written:** 2026-11-27T13:07 (+08) — see §1 for the exact timestamp of every measurement.
**Base of this record:** `652aeaaea9cc77db959e6241f65184b4bf21c9c8` (branch `docs/wb-line03-closeout`). The branch was re-based onto this SHA at 2026-11-27T13:07:53 (+08) because `main` advanced twice while the record was being written; the body of measurements was taken against `242cf101`, which is 5 commits behind and is cited explicitly wherever it matters.

> Evidence grades used below: **VERIFIED** (raw output reproduced in this record), **UNVERIFIED** (measured, but the measurement cannot settle the claim), **NOT_REPRODUCED** (the claim was tested and did not reproduce), **NOT_RECORDED** (no carrier exists), **NOT_VERIFIED** (not tested in this round).

---

## 1. Baseline and drift

The Owner order pinned `788fbc011877a14976fc0a974ffe2e013dd9991b` as the main baseline. That value was already stale when the audit began, and main kept moving throughout the audit. This record therefore pins its own base and reports the drift rather than inheriting a SHA.

| # | Observation | Value | Command / source | Timestamp (+08) | Grade |
|---|---|---|---|---|---|
| 1.1 | Order baseline | `788fbc011877a14976fc0a974ffe2e013dd9991b` | order text | — | — |
| 1.2 | main at first measurement | `f18adc9fa1d06837433a09498f5297bf13b35756` | `git ls-remote origin refs/heads/main` | 2026-11-27T11:36:29 | VERIFIED |
| 1.3 | main at second measurement | `bc741bdce7b47d3695d85fa9649fe9506f23c595` | `git ls-remote` | 2026-11-27T11:46:33 | VERIFIED |
| 1.4 | main pinned for phase-1 evidence | `987d26021affbb5ba6d651e0fb5985d6bd4026a5` | GraphQL `repository.defaultBranchRef.target.oid` | 2026-11-27T12:01:36 | VERIFIED |
| 1.5 | main pinned for the body of measurements | `242cf101c8b79007ad2fb8d9c89681224577188d` | `git ls-remote origin refs/heads/main`; `git fetch origin --prune` | 2026-11-27T12:53:59 | VERIFIED |
| 1.5b | **final branch base** | **`652aeaaea9cc77db959e6241f65184b4bf21c9c8`** | `git fetch origin main`; `git checkout -B docs/wb-line03-closeout 652aeaa` | 2026-11-27T13:07:53 | VERIFIED |
| 1.6 | Distance from order baseline | **>206 commits** (`788fbc01..242cf101` = 206; more by `652aeaa`) | `git rev-list --count 788fbc01..242cf101` | 2026-11-27T12:56 | VERIFIED |
| 1.7 | Cause of drift | concurrent merges by other lines during the audit (`#1334 #1360 #1361 #1364 #1367 #1383` …) | `git log --first-parent --oneline` | — | VERIFIED |
| 1.8 | Repository visibility | `isPrivate=false`, `visibility=PUBLIC` | GraphQL | 2026-11-27T12:01 | VERIFIED |
| 1.9 | REST core quota at audit start | `0 / 5000` (exhausted by concurrent lines); GraphQL `4983 / 5000` | `GET /rate_limit` | 2026-11-27T11:47 | VERIFIED |

**Consequence for readers:** every line number and blob SHA in this record is valid **only** at `242cf101` (or at the explicitly named older blob where the record is describing a superseded state). Re-deriving them against a later `main` will fail; re-run the command in the row instead.

**PR states are pinned to a timestamp, not to "now".** During the audit, `#1325` merged (2026-11-27T04:38:43Z, merge `3daebd2c`), `#1309` was closed unmerged (head `df192ede`), `#1321`'s head moved `65b50760` → `20f1d468`, and `#1335`'s head moved `75ef044c` → `ae0ef728`. Every PR state in this record is the value measured at the timestamp printed in its row; none is asserted as current.

---

## 2. Findings register

### F-01 — `#1329` is merged; its real merged head is `11fde79a`, not `2afe24cd`

| Field | Value |
|---|---|
| Source | `GET https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls/1329` |
| state / merged | `closed` / `true` |
| merged_at | `2026-11-26T18:48:41Z` |
| merge_commit_sha | `76684cb28b132917b3f250e9bf6430713e61c362` |
| head.sha (at merge) | `11fde79a8f07fac5176f67a2fdc633411570e87e` |
| base.sha | `de9f6e9646c5140fe9c9767b1fd2fe15cc38b022` |
| head.ref | `docs/aid-151-retroactive-gate-gap` |
| author / merged_by | `oahcom` / `oahcom` |
| created_at | `2026-11-26T14:17:15Z` |
| Merge commit parents | `de9f6e96…` + `11fde79a…` (`git log -1 --pretty=%P 76684cb2`) |
| `2afe24cd` relation | `2afe24cd` is an **ancestor** of `11fde79a` (the branch merged main once more before merging); it is **not** the merged head |
| Ancestry of merge commit | `76684cb2` is an ancestor of `242cf101` — `git merge-base --is-ancestor 76684cb2 242cf101` → exit `0` |
| Merge diff | 4 files, +334: `AID-2026-174/{manifest,prompt-v1,session-evidence}` + `INDEX.md` (`git show --stat 76684cb2`) |

**Grade:** VERIFIED. **Disposition:** merged fact recorded separately from the authorization history; the order's "head `2afe24cd`" is corrected to `11fde79a`, and `2afe24cd` is recorded as an ancestor.

### F-02 — `AID-2026-174` is the work item that landed; its carriers at `242cf101`

| Path | blob | Notes |
|---|---|---|
| `14-ai-development/work-items/AID-2026-174/manifest.yaml` | `3f3831e592f82b678ae4fdf5149213eed6e430a4` | `work_item_id: AID-2026-174` (L1), `status: DISPATCHED` (L12), `acceptance_authority: NOT_ASSIGNED` (L16) |
| `14-ai-development/work-items/AID-2026-174/prompt-v1.md` | `f11541445f5d36d46163fe30c5a07f8257f38693` | — |
| `14-ai-development/work-items/AID-2026-174/session-evidence.md` | `a716146d9869580aeb7308d886d237796173117c` | — |
| `14-ai-development/work-items/INDEX.md` | `2e4d5552ad204bfee2515debf96322a20325f53a` (313 lines) | AID-2026-174 row at **L55** |

Command: `git ls-tree 242cf101 -- 14-ai-development/work-items/AID-2026-174/`; `git show 242cf101:…/manifest.yaml`.
**Grade:** VERIFIED. **Disposition:** recorded. `acceptance_authority: NOT_ASSIGNED` is retained as written; no approval is inferred from the merge.

### F-03 — `AID-2026-151` never existed on `main`

| Observation | Value | Command | Grade |
|---|---|---|---|
| `AID-2026-151` in main tree | absent (`git ls-tree` + `git grep` both empty) | `git grep -n -I AID-2026-151 242cf101` → no match | VERIFIED |
| `AID-2026-151` INDEX row | absent | `git show 242cf101:…/INDEX.md \| grep AID-2026-151` → no match | VERIFIED |
| Where it does exist | only in branch history: `f8236828` "docs(ai-development): record the historical Session Evidence coverage gap (AID-2026-151)" and its reservation `c84a8191` | `git log --all --diff-filter=A -- '14-ai-development/work-items/AID-2026-151/*'` | VERIFIED |
| Branch containment | `docs/aid-151-retroactive-gate-gap`, `renumber/1329-188` | `git branch -a --contains f8236828` | VERIFIED |
| Is `f8236828` an ancestor of the merged head `11fde79a`? | **No** (exit 1) — the record was renumbered before merge | `git merge-base --is-ancestor f8236828 11fde79a` | VERIFIED |
| Tree at `f8236828` | contains `AID-2026-151/` | `git ls-tree f8236828 -- 14-ai-development/work-items/` | VERIFIED |
| Tree at merged head `11fde79a` | contains `AID-2026-174/` (no 151) | same | VERIFIED |
| Numbering chain | `8d89d125` (21:22) "reserve AID-2026-112 for the retroactive gate-gap record" → `c84a8191` (22:05) reserve **151** → `f8236828` (22:08) write as 151 → merged as **174** | `git log --all --diff-filter=A` + commit subjects | VERIFIED |

**Grade:** VERIFIED. **Disposition:** recorded as "151 is a branch-only intermediate number; the canonical landed identifier is 174". No renumbering performed.

### F-04 — F-02 report: `v2.10` is superseded by `v2.11` on `main`; one live assertion remains

Document located: `00-governance/reports/bilingual-baseline-remediation-report.md` (this is the F-02 report; `14-ai-development/PR-GOVERNANCE-001.md` is a different, 205-line document with 0 checkboxes).

| State | Ref | blob | lines |
|---|---|---|---|
| v2.10 (the version the order's line numbers refer to) | `c6b7d987b959c42af5072932963dae9ed55721e4` (PR #1195 merge) | `a047b72d1f9681c2c58d9b5e62ed940f819fcaa3` | 1448 |
| current main | `242cf101` | `8dd23ea35d1bce478073b7a122969f65c3e27e29` | 1472 |

Line-level contradiction table (order lines → v2.10 text → conflicting counterpart → current main state):

| Order line (v2.10) | v2.10 text (truncated) | Conflicting counterpart | At `242cf101` |
|---|---|---|---|
| L861 AC-05 | `PARTIAL — … platform required-check enforcement is unverified (F-02 R2)` | L501 "Requirement 2 … COMPLETE / VERIFIED" | **corrected** → L859 now points at §7.2.2 |
| L862 AC-06 | `FAIL — F-02 Requirement 2 NOT_VERIFIED (platform-limited); v1.2 not adopted` | L501 / L642 | **corrected** → L860 "FAIL — v1.2 not adopted … no longer on platform enforcement" |
| **L871 AC-15** | **`FAIL / BLOCKED — CI failure and outstanding findings`** | L642 "F-02 overall COMPLETE / VERIFIED" | **NOT corrected — main L869 is byte-identical** |
| L883 / L894 | §8 supplementary table, F-02 = `PARTIAL` (EN / ZH) | L642 / L507 | **corrected** → L881 / L892 `COMPLETE / VERIFIED` |
| L997 | §9 F-09 boundary: `F-02 Requirement 2 stays NOT_VERIFIED because the platform setting is unavailable` | L642 / L969 | **corrected** → L995 past tense + separate 2026-11-25 closure |
| L1021 / L1085 | §9 CI blocker: `The only remaining F-02 blocker is … Retain NOT_VERIFIED` (EN / ZH) | L507 / L642 | **corrected** → L1021 / L1089 "No F-02 blocker remains" |
| L1152 / L1158 | §10 ledger row `PARTIAL`; Structural CI row `Required-check enforcement remains NOT_VERIFIED` | L642 / L969-970 | **corrected** → L1158 / L1164 both COMPLETE |
| L1174 / L1191 | §11 honest declaration: `Required-check enforcement is not verified … F-02 therefore remains PARTIAL` | L642 | **corrected** → L1180 past tense |
| L501-507 | `Requirement 2 … COMPLETE / VERIFIED` + `F-02 overall status: COMPLETE / VERIFIED` | the stale rows above | unchanged (correct side) |
| L642 | `**Status:** R1 COMPLETE … R2 COMPLETE … F-02 overall COMPLETE` | L871 / L997 / L1152 | unchanged |
| L684 | §6.4 gate-behaviour paragraph; 403 marked historical, "no longer `NOT_VERIFIED`" | `D7 v2.2` note (L1249) still says `NOT_VERIFIED` | unchanged; L1249 is inside a **bound snapshot** revision note (§0), not a live assertion |
| L742 | §7.2.2 negative control (`PUT /pulls/1038/merge` → 405) | — | unchanged |
| L914 | §9 finding row F-02 = `COMPLETE / VERIFIED (2026-11-25)` | L997 / L1021 | unchanged |
| L969-970 | §9 P1 block, both requirements COMPLETE | L997 / L1152 | unchanged |

**Single residual (recorded, not edited):** `242cf101:00-governance/reports/bilingual-baseline-remediation-report.md` **L869** still reads `FAIL / BLOCKED — CI failure and outstanding findings` while §7.2 L642, §9 L912, §10 L1158 and §11 L1180 all assert `COMPLETE / VERIFIED`. This is the only enumerated line from the order that v2.11 did not convert. **This record does not edit the normative document**; the correction requires the report's own revision-note procedure and its owner.

**"EN three / ZH two" claim:** NOT_REPRODUCED. Measured on blob `a047b72d`, live-assertion conflicts are EN 7 (L861, L883, L997, L1021, L1152, L1158, L1174) and ZH 3 (L894, L1085, L1191).

**Grade:** VERIFIED (locations, blobs, line numbers, texts). **Disposition:** residual registered as an open defect of the report, not of this record.

### F-05 — `#1195` §7.1: the three historical runs are accessible

§7.1 of the report (v2.10, L630-640) names three successful runs and one retained failure:

| run id | unauthenticated `GET /repos/oahcom/AiMemoryBrainArchitecture/actions/runs/<id>` | conclusion | head_sha | workflow |
|---|---|---|---|---|
| `44542512889` | **HTTP 200** | `success` | `702197314850…` | Bilingual documentation gate |
| `44546301573` | **HTTP 200** | `success` | `47369925ace9…` | Bilingual documentation gate |
| `44559550224` | **HTTP 200** | `success` | `bbfe046b9307…` | Bilingual documentation gate |
| `44477435608` (control) | **HTTP 200** | `failure` | `a77219fa2834…` | Bilingual documentation gate |

Command: `curl -s -o run.json -w "%{http_code}" https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/actions/runs/44542512889` (unauthenticated requests use a separate 60/h bucket, so the exhausted token quota does not confound this test).
`/branches/main/protection` unauthenticated returns **401** (not 403), so the historical 403 reading **cannot be retested without credentials** — see §11.

**Grade:** VERIFIED for run existence/conclusion/head. **Disposition:** the three runs are accessible today because the repository became public; the 403 era is recorded as historical, not re-asserted.

### F-06 — `#262` AC2: `7157542128` supersedes `7156638485`

| Comment | Author | Created (UTC) | Opening line |
|---|---|---|---|
| `7156638485` | `oahcom` | `2026-11-25T08:07:39Z` | `## REQ-01 / AC2 — 裁定：SATISFIED（条款已入 main）` … "落点 `14-ai-development/PR-GOVERNANCE-001.md` §5 … PR #1073 合入 `edbc363`" |
| `7157542128` | `oahcom` | `2026-11-25T08:50:41Z` | `## Correction — 7156638485 is wrong on two counts: AC2 is not SATISFIED, and the clause is not Owner text` |

Later comments `7161380329`, `7167242401`, `7170740216`, `7192867653`, `7194113764` all keep **AC2 = PARTIAL**.
`#262` body measured: 346 lines, `- [ ]` = **1**, `- [x]` = 7; body L296 `ASSESSMENT_COMPLETE_AC2_PARTIAL_CARRIER_AID_2026_075`, L304 Chinese status marks AC2 PARTIAL.

**Grade:** VERIFIED. **Disposition:** reference chain recorded; AC2 domain semantics untouched; no AC completion claimed.

### F-07 — `#1256` approver: no natural-person carrier → `NOT_RECORDED`

| Item | Value |
|---|---|
| Object type | **pull request** (`#1256`), not an issue |
| state / merged_at | `MERGED` / `2026-11-26T08:13:20Z` |
| author / merged_by | `oahcom` / `oahcom` |
| Recorded approver string | `user-authorized operator (delegated by account owner)` |
| Designation evidence (PR comment `7186340337`) | `designation_evidence: account owner direct instruction, 2026-11-26, verbatim: "你就是批准人"`; `designation_channel: operator session instruction` |
| Blocking reviews before merge | `7185706860`, `7185865670`, `7186114803` all state the approval-attribution defect blocks merge |
| Self-confirmation | `7186084178` — the same `oahcom` account confirms the designation |

**Grade:** NOT_RECORDED (no natural-person identity carrier exists). **Disposition:** recorded as `NOT_RECORDED`; no substitution with a session or account identity; `OUT-OF-SCOPE(dev-baseline)` for obtaining one.

### F-08 — 200 boxes: the number does not exist in any target file

Claim under test: `INDEX.md` AID-2026-093 row — "`20 DEC rows / 18 unique directions; … 200 acceptance boxes remain unchecked`" (`242cf101:…/INDEX.md` **L64**, blob `2e4d5552`).

| Target file (`242cf101`) | blob | `- [ ]` | line numbers |
|---|---|---|---|
| `00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md` | `4810c6f8d3b5676a44288dea5782681e0745af6f` | **10** | L100-L109 |
| `docs/en/…/2026-11-26-20-decision-acceptance-register.md` | `dcae8a7cb5c6e03bf220d1d681744cc68361e87d` | 10 | L99-L108 |
| `docs/zh-CN/…/2026-11-26-20-decision-acceptance-register.md` | `49b3aff58991b77545ab143d12782b65e71a5a69` | 10 | L99-L108 |
| `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | 10 | L719-L728 |
| `00-governance/templates/bilingual-umbrella-requirement-template.md` | `9265098d739369522000ebc54b8c0275ee7e5b6d` | 4 | L90, L91, L94, L95 |
| `14-ai-development/PR-GOVERNANCE-001.md` | `579ef2def33696c76eb636a46d6737eaee04edd5` | 0 | — |

Whole tree at `242cf101`: **27 files, 331 open `- [ ]`, 32 `- [x]`** (`python boxes.py 242cf101`; each file read as `git show <ref>:<path>` then `bytes.count(b"- [ ]")`).
`200 = 20 × 10` is an arithmetic projection of the ten-item checklist template across twenty DEC rows; no file and no issue carries 200 boxes.

**Grade:** VERIFIED (counts, blobs, lines). **Disposition:** recorded; the INDEX cell's "200" is a derived figure presented as an observation. **Not corrected by this record** (INDEX is off-limits); correction text proposed in §10.

### F-09 — numbering and ledger state for the thirteen identifiers

Ledger under test: `origin/aid-ledger:aid-ledger.yaml`, blob **`b95563a662b3397237a0dca364d7e183e98e0909`**, branch head `384a3057dc48b512e2973db6e0f0aac52ffb19d2` (2026-11-27T12:52:10, "chore(aid): cancel 262, reserve 263 for #1341, record 261 conflict and 7 missing rows"). The ledger is **not on `main`** — it lives only on branch `aid-ledger`.

| ID | dir on `main`? | INDEX line (`2e4d5552`) | manifest title | ledger state |
|---|---|---|---|---|
| 097 | yes | L72 | Remove the live assertions that still said F-02 Requirement 2 was NOT_VERIFIED | MERGED / PR #1270 |
| 102 | yes | L149 | Correct the AID-2026-092 prompt digest, which matched no version of its own file | MERGED / PR #1279 |
| 104 | yes | L142 | Remove approval_scope's two permanently-empty keys from the schema and the corpus | MERGED / PR #1281 |
| 106 | yes | L59 | Complete Phase 1/2 phase-freeze audit and exact-version acceptance evidence for #1197 | MERGED (PR not recorded) |
| 110 | yes | L285 | Restore two review-named E Memory Compiler canonical roots | MERGED / PR #1304 |
| 111 | yes | L286 | SQLite backend implementation evidence mapping to SC/HIR and Gate A predicates | MERGED (receipt `591bbcd8`) |
| **112** | yes | **L289** | Rejudge SC/HIR implementation predicates against 552 local test passes | **OCCUPIED_BY_OTHER** |
| **116** | **no** | **absent** | — (only in `#1321` head tree) | OCCUPIED_BY_OTHER / PR #1321 |
| 117 | no | absent | — | **FREE** + self-distrusting note |
| 140 | yes | L288 | Restore five F Memory Runtime Canonical roots | — |
| **149** | **no** | **absent** | — | **no ledger row at all** |
| 150 | yes | L292 | Restore three D Memory Brain normative roots | MERGED (PR not recorded) |
| **151** | **no** | **absent** | — | **IN_FLIGHT / "PR #1329 head f8236828"** (stale on all three fields) |
| 174 | yes | L55 | Record the historical Session Evidence coverage gap … | (no row) |
| 188 | yes | L295 | Verify that the 03-memory-brain normative root … already registered | **IN_FLIGHT / PR #1337** (stale) |

**Grade:** VERIFIED. **Disposition:** per-ID facts registered; corrections proposed in §10, none applied.

### F-10 — MCP: `ai-memory-adapter × chatgpt-session-ops` contract as it exists in code

| Carrier | Symbols / facts |
|---|---|
| `chatgpt-session-ops:src/session_ops/memory_adapter_client.py` (10,597 B) | `MemoryAdapterClient.{store, retrieve, _invoke}`, `MemoryProvenance`, `StoredMemory`, `RetrievedMemory`, `RetrieveResult`, `MemoryAdapterError`, `CONTRACT_VERSION = "0.1"` |
| same file, module docstring | "JSON Lines protocol, contract v0.1 … **No shell, no retry, no network, no MCP, no third-party dependency**" |
| same file, implementation | `import subprocess` ×3; occurrences of `http` = 0, `url` = 0, `20127` = 0 |
| `chatgpt-session-ops:src/session_ops/mcp_server.py` (35,093 B) | `MCPToolService.dispatch`, `build_mcp_server`, `_DeadlineExceeded`, `_ResourceExhausted`; references `MemoryAdapter` ×5, `memory_adapter` ×12 |
| `chatgpt-session-ops:references/memory-adapter-contract-v0.1.md` (583 lines, introduced by `05ffbbdf`, 2026-11-24) | "Preferred transport: JSON Lines over stdin/stdout"; "MCP must never become a mandatory dependency of SO"; SO owns WorkItem identity (`wi_<UUIDv4>`), MA owns persistence/retrieval/scope |

**Grade:** VERIFIED. **Disposition:** the contract is a **local subprocess** boundary; there is no HTTP or MCP transport in the code path.

### F-11 — `192.168.1.108:20127` is a web console, not an MCP endpoint → the `502 ETIMEDOUT` classification is REFUTED

| Probe | Raw result |
|---|---|
| `Test-NetConnection 192.168.1.108 -Port 20127` | `TcpTestSucceeded=True`, `PingSucceeded=False` |
| `curl -m 5 http://192.168.1.108:20127/` | `HTTP/1.1 307 Temporary Redirect`; `location: /dashboard`; `time_total=0.010618` |
| `curl -m 5 -L http://192.168.1.108:20127/` | `final=http://192.168.1.108:20127/login  http=200` |
| `curl -m 5 http://192.168.1.108:20127/mcp` | `404` |
| `20127` in ops code | 0 occurrences (only in `prompts/` and `scripts/**/replies/`) |

**Grade:** NOT_REPRODUCED (the 502/ETIMEDOUT failure mode). **Disposition:** classified as "reachable HTTP console with no MCP endpoint", **not** as a code defect and **not** as network unreachability.

### F-12 — RMC: TCP reachability vs SSH authentication success

| Check | Raw result |
|---|---|
| TCP 22 | `TcpTestSucceeded=True`, `PingSucceeded=False` |
| SSH auth | `ssh -o BatchMode=yes -o ConnectTimeout=5 ubuntu@43.138.133.238 "id -un; sudo -n true && echo SUDO_NOPASS_OK"` → `ubuntu` / `SUDO_NOPASS_OK` |
| Secrets | none read, printed, or stored |

**Grade:** VERIFIED. **Disposition:** TCP reachability and authentication success recorded as **separate** facts; neither implies MCP is logged in or working. `so-mcp:8791`, `so-sender:8792`, Keycloak `:8180` were **not** exercised this round.

### F-13 — opencode-purge: configuration present, schema real, runtime load unobserved

| Layer | Evidence | Grade |
|---|---|---|
| Config presence | `C:\Users\Administrator\.config\opencode\opencode.json` **L163-165**: `"experimental": { "subagent_depth": 4 }`; `continue_loop_on_deny` occurs **0** times in the file | VERIFIED |
| Published schema | `https://opencode.ai/config.json` (75,055 B): `experimental.additionalProperties=false`; `experimental.properties` contains **both** `subagent_depth` and `continue_loop_on_deny`; `subagent_depth` = `{type: integer, minimum: 0}` | VERIFIED |
| Installed binaries | `…\ai.opencode.desktop\resources\opencode-cli.exe` and `…\Roaming\ai.opencode.desktop\cli\2.4.2-x64\opencode-cli.exe`; both `opencode v2.4.2`, 278,504,840 B, mtime 2026-11-26 14:08 | VERIFIED |
| Keys inside 2.4.2 | `subagent_depth` ×6, `continue_loop_on_deny` ×2 (raw byte search) | VERIFIED |
| Allowlists inside 2.4.2 | `KI=["logLevel","server","subagent_depth","layout"]`; `GI=["disable_paste_summary","batch_tool","openTelemetry","primary_tools","continue_loop_on_deny"]` | VERIFIED |
| Field semantics inside 2.4.2 | annotation `subagent_depth: … "Maximum subagent nesting depth. Defaults to 1."`; error string `Increase "experimental.subagent_depth" to allow nested subagents.` | VERIFIED |
| purge's own claim | `purge/app/lib/catalog.js` L314-317: "Only subagent_depth is a live 2.4 field … 2.4 lists it in GI and drops it as an unsupported legacy setting" | — |
| Runtime load | `~/.local/share/opencode/log/opencode.log` (24,959 lines): `subagent_depth` 0, `continue_loop_on_deny` 0, `Unrecognized` 0 → no rejection warning, but no load line | NOT_OBSERVED |
| Actual behaviour | no nested-spawn probe executed | NOT_VERIFIED |
| DP-01 re-verified independently | 2 binaries × 10 patches: every `patched_match=True`, every `orig_present=False` (e.g. `DEEP-IDENTITY-HI` @261,477,553; `DEEP-REFUSAL-LINE` @261,478,528; `DEEP-LENGTH-CAP` @261,485,022) | VERIFIED |
| `deep.json` "2.4.1 dead record" | `deep.json` (`at=2026-11-26T06:09:37Z`, `version=2`, `targets=2`) names only `…\cli\2.4.2-x64\opencode-cli.exe` and the desktop copy; `2.4.1` occurs **0** times | NOT_REPRODUCED |

**Grade:** VERIFIED for config/schema/binary/DP-01; NOT_VERIFIED for runtime behaviour. **Disposition:** the "legacy-dropped key" claim is refuted; `subagent_depth=4` is a live field whose default is 1.

### F-14 — Single-writer identity

| Fact | Evidence |
|---|---|
| author == merged_by == `oahcom` | **40 / 40** most recently merged PRs, differing set = `none` (GraphQL `pullRequests(states:MERGED, first:40){nodes{author{login} mergedBy{login}}}`) |
| Spot checks | `#1329`, `#1334`, `#1361`, `#1337`, `#1316`, `#1220` — all `oahcom` / `oahcom` |
| Open PRs | **13** at 2026-11-27T13:02 (+08), all authored by `oahcom` (`#1404 #1402 #1401 #1398 #1397 #1393 #1388 #1380 #1366 #1336 #1335 #1321 #1305`) |
| Review enforcement | `required_pull_request_reviews` is **absent** from branch protection (report v2.10 §7.2.2 states it explicitly; the 16 required contexts are status checks only) |
| Platform consequence | a merge needs green checks, **not** an approving review; a second GitHub account or a second session cannot manufacture platform-level independence |

**Grade:** VERIFIED. **Disposition:** `OUT-OF-SCOPE(dev-baseline)`. This is a **capability boundary**, never a blocker for the convergence, and it is not simulated: no independent reviewer is claimed anywhere in this record.

---

## 3. What this record did not do

- No edit to `INDEX.md`, any manifest, `aid-ledger.yaml`, or any normative document (including the F-02 report).
- No merge, no issue close/reopen, no renumbering, no force-push, no new work item.
- No access to the other line's worktree (`D:\code\chatgpt-session-ops`) beyond read-only inspection; nothing there was written.
- No path under `14-ai-development/reports/` and no `ATTRIBUTION.md` (owned by LINE 01).
- One file added: this record. See §6 for `git show --stat`.

---

## 4. Corrections to the ledger and to earlier conclusions

Ledger baseline for every row below: `origin/aid-ledger:aid-ledger.yaml` blob `b95563a662b3397237a0dca364d7e183e98e0909` (head `384a3057`, 2026-11-27T12:52:10). **None of these corrections has been applied.** The exact text an owner would need is given in the last column.

| # | Row / claim | What was claimed | What is true | Evidence | Exact correction for the ledger owner |
|---|---|---|---|---|---|
| C-01 | `AID-2026-112` (L134-137) | `state: OCCUPIED_BY_OTHER`; note: "the retroactive gate-coverage work item was reassigned to **AID-2026-151** by the external line (**PR #1329**)" | `112` on main is PR **#1316** (merge `8722a37b`, 2026-11-26T21:48:06+08). PR #1329 landed as **AID-2026-174**, head `11fde79a`, merge `76684cb2`. **AID-2026-151 never existed on main.** The second claimant of 112, PR **#1309, was CLOSED unmerged** (head still `df192ede`) — so no open PR asserts 112 any more. | `git log --first-parent -5 242cf101 -- …/AID-2026-112/`; `GET /pulls/1329`; `git grep AID-2026-151 242cf101` (no match); GraphQL `pullRequest(1309)` → `state=CLOSED, merged=false, headRefOid=df192ede` | Replace the note with: `note: "main carried a different AID-2026-112 from PR #1316 (merge 8722a37b). The retroactive gate-coverage record was renumbered 112 -> 151 -> 174 on the external branch and merged as AID-2026-174 in PR #1329 (merge 76684cb2, head 11fde79a). AID-2026-151 never entered main; PR #1309, the only other claimant of 112, was closed unmerged."` Keep `state: OCCUPIED_BY_OTHER`. |
| C-02 | `AID-2026-116` (L150-153) | `state: OCCUPIED_BY_OTHER`; carrier `PR #1321` | `#1321` is **still OPEN** (head moved `65b50760` → `20f1d468` during the audit); `main@242cf101` has **no** `14-ai-development/work-items/AID-2026-116/` and no INDEX row. `OCCUPIED_BY_OTHER` asserts occupancy of main, which is false. | GraphQL `pullRequest(1321)`; `git ls-tree 242cf101 -- …/AID-2026-116/` → empty; `git ls-tree 65b50760 -- …/` → `AID-2026-116` present | Change `state` to `IN_FLIGHT`; keep `carrier: "PR #1321 (gov/aid-116-pin-and-attribution), open, head 20f1d468"`. |
| C-03 | `AID-2026-117` (L240-242) | `state: FREE` with note "do not trust this row … the next plausibly free number is >= 189" | `117` is indeed absent from `main@242cf101`, so `FREE` holds — but the note's floor is stale: main now carries `AID-2026-241`, `253`, `260`, `261`, `279`. A row that instructs the reader not to trust itself is not a usable reservation record. | `git grep AID-2026-117 242cf101` (no match); INDEX rows for 241/253/260/261/279 present | Keep `state: FREE`; replace the note with: `note: "re-verified absent on main@242cf101 and in all open PR heads; do not reuse the 189 floor — main already carries 241/253/260/261/279; re-scan immediately before any reservation push."` |
| C-04 | `AID-2026-151` (L158-161) | `state: IN_FLIGHT`; carrier "PR #1329 (external, head `f8236828`)" | Three independent errors: PR #1329 is **MERGED** (2026-11-26T18:48:41Z), its merged head is **`11fde79a`**, and the work item it landed is **AID-2026-174**. `f8236828` is not an ancestor of the merged head; `AID-2026-151` is branch-only and absent from main. | `GET /pulls/1329`; `git merge-base --is-ancestor f8236828 11fde79a` → 1; `git ls-tree 11fde79a -- …/` → `AID-2026-174` | Replace the whole block with: `- id: AID-2026-151` / `state: SUPERSEDED` / `carrier: "renumbered to AID-2026-174 before merge; landed by PR #1329 (merge 76684cb2, head 11fde79a)"` / `note: "branch-only identifier (commits c84a8191, f8236828). Never present on main. No action required; do not reuse."` |
| C-05 | `AID-2026-188` (L181-183) | `state: IN_FLIGHT`; carrier "PR #1337 (external)" | PR **#1337 is MERGED** at `2026-11-26T15:34:46Z`, merge `f6ef2545913754da7859abfaad5559fdc68074ce`; `main@242cf101` carries `AID-2026-188/{evidence,manifest,prompt-v1,session-evidence}` and INDEX **L295**. | GraphQL `pullRequest(1337)`; `git log --first-parent -1 f6ef2545`; `git ls-tree 242cf101 -- …/AID-2026-188/` | `state: MERGED` / `carrier: "PR #1337, merge f6ef2545, 2026-11-26T15:34:46Z"`. Also note the live collision: branch `renumber/1329-188` (`5d5b0aa9`, 22:54) still tries to create `AID-2026-188/` and would add/add-conflict with the merged copy. |
| C-06 | RESERVED self-errors | `AID-2026-262: RESERVED` (Issue #1341) with a note that excluded `261` because it lived in an "unpushed local worktree" | Already superseded by ledger commit `384a3057`: `262` is now `OCCUPIED_BY_OTHER` and `263` is `RESERVED`; `261` is `OCCUPIED_BY_OTHER` because `#1383` merged it into main at `242cf101`. **The remaining defect is the method, not the row:** the earlier exclusion of 261 rested on an unverifiable local-worktree claim, and the replacement reservation's note asserts "AIDSCAN five-scope zero-hit (2829 commits / 1317 unique trees / 21 ledger versions / 280 worktrees)" — that scan is not reproducible from this record. | `git log -1 origin/aid-ledger` = `384a3057`; ledger L196-199 (`262`), L220-223 (`261`), L224-227 (`263`) | No row change needed. Add to the reservation note: `verification: "AIDSCAN claim NOT_VERIFIED by an independent party; re-scan before use"` — or reproduce the scan and cite its command. |
| C-07 | `AID-2026-149` | No ledger row exists at all; no directory, no INDEX row on main | Absence confirmed; the identifier is unregistered rather than free-by-record. | `git ls-tree 242cf101 -- …/AID-2026-149/` → empty; INDEX grep → no match; ledger grep → no match | Add an explicit row: `- id: AID-2026-149` / `state: UNREGISTERED` / `note: "no carrier on main, in open PRs, or in this ledger; treat as free only after a fresh scan"`. |
| C-08 | Technical claim: `192.168.1.108:20127` = MCP endpoint returning `502 ETIMEDOUT` | The MCP integration was "blocked on 502 ETIMEDOUT at 192.168.1.108:20127" | The port answers HTTP `307 → /dashboard`, `/login` returns `200`, `/mcp` returns `404`, in 10.6 ms. It is a **web console**, not an MCP server. No ops code references the port; the in-repo contract is a local JSONL subprocess. | §F-11 raw output | Restate as: "`192.168.1.108:20127` is reachable and serves an HTTP console; it exposes no MCP endpoint (`/mcp` → 404). The ops memory-adapter contract does not use HTTP. The earlier 502/ETIMEDOUT classification is withdrawn as NOT_REPRODUCED." |
| C-09 | Technical claim: `continue_loop_on_deny` is a legacy-dropped key | `purge/app/lib/catalog.js` L314-317: 2.4 "lists it in GI and drops it as an unsupported legacy setting" | In 2.4.2 the key is present in the binary (×2) **and** in the experimental allowlist `GI`, and it is still a property of `experimental` in the published schema (`additionalProperties:false`). Citing GI as proof of dropping inverts the meaning of an allowlist. | §F-13 raw output | Restate as: "`continue_loop_on_deny` is an accepted `experimental` key in 2.4.2 and in the published schema; purge no longer writes it because `subagent_depth` is the field the purge depends on, not because 2.4 drops it. Behaviour of the key was not exercised." |

---

## 5. NOT_VERIFIED / UNVERIFIED register

| # | Item | Why it stays open | What would settle it |
|---|---|---|---|
| N-01 | `experimental.subagent_depth` **runtime behaviour** (does depth 4 actually permit 4 levels?) | No load line in `opencode.log`; no nested-spawn probe executed | spawn a subagent at depth 1 that spawns at depth 2, then 3, 4, and observe the `Increase "experimental.subagent_depth" …` error at the boundary |
| N-02 | `continue_loop_on_deny` **behaviour** | key is absent from config; nothing to exercise | set the key on a scratch profile and deny a tool, then observe loop continuation |
| N-03 | `#1195` §7.1 historical **403** retest | unauthenticated `/protection` returns **401**, authenticated REST core quota is **0** | retest with a token after quota reset: `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` |
| N-04 | `AID-2026-263` reservation's "AIDSCAN five-scope zero-hit" | not reproducible from this record | publish the AIDSCAN command and its raw output |
| N-05 | MCP `so-mcp:8791` / `so-sender:8792` / Keycloak `:8180` behaviour | not exercised this round (RMC production login is `OUT-OF-SCOPE(dev-baseline)`) | — (explicitly excluded) |
| N-06 | `#1256` approver's natural-person identity | no carrier exists; self-designation by the same account is not evidence | an independent record naming a natural person, outside this repository |

---

## 6. Write boundary and self-audit

| Item | Value |
|---|---|
| Branch | `docs/wb-line03-closeout` |
| Base | `652aeaaea9cc77db959e6241f65184b4bf21c9c8` (newest `origin/main` at branch creation; the record body was measured at `242cf101`, 5 commits behind) |
| Fetch time | 2026-11-27T12:53:59+08:00 (bulk) / 2026-11-27T13:07:53+08:00 (final base) |
| Files added | 1 — `00-governance/reports/2026-11-27-wb-line03-closeout.md` |
| Files modified | 0 |
| Files deleted | 0 |
| Commit SHA / blob SHA | recorded in the Draft PR body and in the commit object — a file cannot contain its own blob SHA without changing it |

Verification command and raw output are recorded in §6 of this record and repeated in the Draft PR body:

```
git show --stat <commit>
```

---

## 7. Method notes (for reproduction)

- All repository reads used `git show <sha>:<path>` / `git ls-tree <sha>` against an explicitly pinned SHA; no working-tree read was used for evidence.
- All GitHub reads used GraphQL (`POST /graphql`) or unauthenticated REST because the authenticated REST core quota was exhausted; the token was read from disk and never printed.
- Box counting: `git show <sha>:<path>` → `bytes.count(b"- [ ]")`, per file, over `git ls-tree -r --name-only <sha>`.
- Binary inspection: raw byte search for ASCII keys and hex-decoded patch comparison at recorded offsets; no disassembly, no execution of modified binaries.
- Network probes: `Test-NetConnection`, `curl -m 5` with explicit timeouts; `ssh -o BatchMode=yes -o ConnectTimeout=5`.
