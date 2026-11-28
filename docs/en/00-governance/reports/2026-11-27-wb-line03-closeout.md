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

# WB LINE 03 Closeout — Validator / Repository Governance / MCP / Local Environment

**Record type:** development-baseline audit record. Non-normative, informative. It changes no validator, gate, workflow, runtime, API, schema, wire semantic, work item, INDEX row, manifest or ledger entry.
**Status:** `PARTIAL` — every row carries a reproducible command and raw output; the items that could not be settled are enumerated in §6 and are not papered over.
**Base of this record:** `5670357db7a836d4f26838dbaf99494af41e2b65` (`Merge pull request #1423 from oahcom/governance/2026-11-27-merge-authorization-1325`). Branch `docs/wb-line03-closeout-final`, cut from that SHA.
**Written:** 2026-11-27T15:05 (+08), revised 2026-11-27T15:20. Per-row timestamps below are the moment the command in that row was executed.
**Host:** opencode 2.4.2 on Windows, PowerShell; `git` CLI; GitHub GraphQL. Authenticated REST core quota was `0/5000`, so no REST read is used for evidence except the unauthenticated probe bucket.

> **Evidence grades.** `VERIFIED` = the command and its raw output are in this record and the output settles the claim. `UNVERIFIED` = measured, but the measurement cannot settle the claim. `NOT_REPRODUCED` = the claim was tested and did not reproduce. `NOT_RECORDED` = no carrier exists anywhere. `NOT_VERIFIED` = not tested in this round.
>
> **Line-number validity.** Every line number and blob SHA is valid **only** at `5670357d`. `main` advanced at least four times during this audit (§1.2). Re-derive by running the row's command, never by trusting the number.

---

## 1. Baseline, drift and scope

### 1.1 The order's baseline was already stale when the audit started

| # | Claim | Source | Commit SHA | Blob SHA | Line | Command | Raw output | Timestamp (+08) | Grade | Disposition |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.1.1 | The order pinned `788fbc01…` as `main` | order text | `788fbc011877a14976fc0a974ffe2e013dd9991b` | — | — | — | `788fbc01…` | — | — | Superseded baseline; not used for any measurement in this record. |
| 1.1.2 | `main` advanced to `987d2602…` during phase 1 | `origin/main` | `987d26021affbb5ba6d651e0fb5985d6bd4026a5` | — | — | `git merge-base --is-ancestor 987d2602 5670357d` | `exit=0` | 2026-11-27T14:56:26 | VERIFIED | Ancestor of this record's base. |
| 1.1.3 | `main` then reached `6306a858…` | `origin/main` | `6306a858afc378f27448f8796c6b6604dfa240bb` | — | — | `git merge-base --is-ancestor 6306a858 5670357d` | `exit=0` | 2026-11-27T14:56:26 | VERIFIED | Ancestor of this record's base. |
| 1.1.4 | **This record's base** | `origin/main` at branch cut | `5670357db7a836d4f26838dbaf99494af41e2b65` | — | — | `git log -1 --format=%s 5670357d` | `Merge pull request #1423 from oahcom/governance/2026-11-27-merge-authorization-1325` | 2026-11-27T14:56:26 | VERIFIED | All blob SHAs and line numbers in this record are pinned here. |
| 1.1.5 | Distance from the order's baseline | `788fbc01..5670357d` | — | — | — | `git rev-list --count 788fbc01..5670357d` | `520` | 2026-11-27T14:56:26 | VERIFIED | The order's SHA is 520 commits behind. No order-supplied line number was reused without re-derivation. |
| 1.1.6 | `main` moved again **after** this branch was cut | GraphQL `repository.defaultBranchRef` | `7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19` | — | — | GraphQL `{repository{defaultBranchRef{target{...on Commit{oid}}}}}` | `main_oid 7fc4ddabe1ea3b216b4536c0f5cb0a0c84306f19` | 2026-11-27T14:58:25 | VERIFIED | Recorded as drift, not corrected for. This record deliberately does **not** chase `main`. |
| 1.1.7 | Repository visibility | GraphQL | — | — | — | GraphQL `{repository{isPrivate visibility}}` | `isPrivate=false`, `visibility=PUBLIC` | 2026-11-27T14:38 | VERIFIED | Public since 2026-11-25. This is why some historical CI facts are readable without a token; it is **not** used to infer anything about review. |
| 1.1.8 | Authenticated REST core quota | `GET /rate_limit` | — | — | — | (read at audit start) | `core 0/5000`; `graphql 4983/5000` | 2026-11-27T11:47 | VERIFIED | Consequence: every GitHub read below is GraphQL or unauthenticated. No REST-authenticated claim is made anywhere in this record. |

### 1.2 What this record is allowed to assert

`main` moved four times while this record was being written. Therefore:

- Every statement of the form "X is on `main`" means "X is in the tree at `5670357d`".
- Every PR state is the value returned at the timestamp printed in its row. `#1321` and `#1309` both changed state during the audit; both states are recorded with their timestamps.
- No claim is made about `main` after `2026-11-27T14:58:25` (+08).

---

## 2. Findings register

Each finding is a claim plus the exact command that settles it. Rows are ordered by identifier, not by importance.

### F-01 — PR #1329 is merged; its real merged head is `11fde79a`, and `2afe24cd` is an ancestor of it

| Field | Value |
|---|---|
| Source | GraphQL `repository.pullRequest(number:1329)` |
| `state` / `merged` | `MERGED` / `true` |
| `mergedAt` | `2026-11-26T18:48:41Z` |
| `mergeCommit.oid` | `76684cb28b132917b3f250e9bf6430713e61c362` |
| `headRefOid` | `11fde79a8f07fac5176f67a2fdc633411570e87e` |
| `baseRefOid` | `de9f6e9646c5140fe9c9767b1fd2fe15cc38b022` |
| `headRefName` | `docs/aid-151-retroactive-gate-gap` |
| `author` / `mergedBy` | `oahcom` / `oahcom` |
| Merge parents | `git log -1 --format=%P 76684cb2` → `de9f6e9646c5140fe9c9767b1fd2fe15cc38b022 11fde79a8f07fac5176f67a2fdc633411570e87e` |
| `2afe24cd` relation | `git merge-base --is-ancestor 2afe24cd 11fde79a` → `exit=0`; `git rev-parse 2afe24cd` → `2afe24cdb4d52ebed6f085f49b25ccec6ebda247` ≠ `11fde79a…`. **Ancestor, not head.** |
| `f8236828` relation | `git merge-base --is-ancestor f8236828 11fde79a` → `exit=1`. The 151-era commit is **not** in the merged head. |
| Merge reachable from base | `git merge-base --is-ancestor 76684cb2 5670357d` → `exit=0` |

Timestamp 2026-11-27T14:56:27 / 14:38 (+08). **Grade:** VERIFIED. **Disposition:** the order's "head `2afe24cd`" is corrected to `11fde79a`; `2afe24cd` is recorded as an ancestor that the branch merged past. Merged-ness is recorded as an integration fact only — no approval is inferred.

### F-02 — #1329 landed as `AID-2026-174`, and `AID-2026-151` never existed on `main`

| Observation | Value | Command | Timestamp (+08) | Grade |
|---|---|---|---|---|
| `AID-2026-151` anywhere in the tree at `5670357d` | absent | `git grep -n -I AID-2026-151 5670357d` → `exit=1` (no match) | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-151/` directory | absent | `git ls-tree 5670357d -- 14-ai-development/work-items/AID-2026-151/` → empty | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-151` INDEX row | absent | `git cat-file blob c14118f8` filtered for `AID-2026-151` → `0` hits | 2026-11-27T14:56:29 | VERIFIED |
| `AID-2026-174/manifest.yaml` | `3f3831e592f82b678ae4fdf5149213eed6e430a4` | `git ls-tree 5670357d -- …/AID-2026-174/` | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-174/prompt-v1.md` | `f11541445f5d36d46163fe30c5a07f8257f38693` | same | 2026-11-27T14:56:28 | VERIFIED |
| `AID-2026-174/session-evidence.md` | `a716146d9869580aeb7308d886d237796173117c` | same | 2026-11-27T14:56:28 | VERIFIED |
| `INDEX.md` | blob `c14118f854addbc59d9c12692b6b3f4ee9c8fe04`, 323 lines | `git ls-tree`; `cat-file blob … \| wc -l` | 2026-11-27T14:56:29 | VERIFIED |
| `AID-2026-174` INDEX row | **L58** | row scan for `AID-2026-174` | 2026-11-27T14:56:29 | VERIFIED |

**Grade:** VERIFIED. **Disposition:** "151" is a branch-only intermediate identifier; the canonical landed identifier is **174**. No renumbering performed, nothing renamed.

### F-03 — `AID-2026-112` is occupied by PR #1316 (merge `8722a37b`), while closed PR #1309 still claims it

| Field | Value |
|---|---|
| `AID-2026-112/` on `main` | `evidence.md` `ab6d63a79f73c22d773cf5ac864cb4b796ca3a51`; `manifest.yaml` `f246832b6da0db0b3a051c59050efbb114379265`; `prompt-v1.md` `f9cebc35f81ecf47f2530c65aff26bedc553bb5c`; `session-evidence.md` `275a1ef457ddc8eb75af112faa563a691baf8074` |
| INDEX row | **L293** (blob `c14118f8`) |
| Occupying PR | GraphQL `pullRequest(1316)`: `MERGED`, `mergedAt 2026-11-26T13:48:07Z`, `mergeCommit 8722a37b0cd72dc550d99c0eaebe9e7556ce2f95`, head `f9e399fc27c8914f6229c9fad50f938216cf0682` |
| Merge reachable from base | `git merge-base --is-ancestor 8722a37b 5670357d` → `exit=0` |
| Second claimant | GraphQL `pullRequest(1309)`: `CLOSED`, `merged=false`, `closedAt 2026-11-27T04:31:22Z`, head `df192ede5384227ab516ec19a49b2a9094cf224e`, ref `docs/2026-11-26-aid-112-e-canonical-restore-batch-1` |
| The closed PR's head still carries the directory | `git ls-tree df192ede -- 14-ai-development/work-items/` → `040000 tree 86bdcae69ea16dd406a8f41d6449a9de9018e4ad 14-ai-development/work-items/AID-2026-112` |

Timestamps 2026-11-27T14:38 (GraphQL) / 14:56:28 (+08). **Grade:** VERIFIED. **Disposition:** `112` on `main` belongs to #1316. #1309 was **closed unmerged** — it no longer asserts 112 against `main`, but its head tree still contains an `AID-2026-112/` and would add/add-conflict if it were ever reopened and rebased. Recorded; not acted on.

### F-04 — `AID-2026-116` is now merged into `main` via #1321; the INDEX row and the ledger both still say "open"

| Field | Value |
|---|---|
| `AID-2026-116/` on `main` | `evidence.md` `7804abe9b09c3bdd28b53eff4dc008fa87d89f39`; `manifest.yaml` `46ce54e62388a3306c3048c9738feddf23c495f2`; `prompt-v1.md` `c926c6ca9859f5c7fc8e548362af517f6cad2162`; `session-evidence.md` `75aa1261670279d4349a1ef807affda8807f999e` |
| INDEX row | **L72**, whose status cell still reads `PR_OPEN` |
| PR | GraphQL `pullRequest(1321)`: `MERGED`, head `e61e714a978cd9f298d9216e990b1d8466e4bf93`, ref `gov/aid-116-pin-and-attribution` |
| Ledger | `origin/aid-ledger` head `5592658f12f02ada111ccd338600ad2e17d7d2f4`, blob `9020f0a27945fcc3657d7fd35ab9cb699ee41855`, L150-153: `state: OCCUPIED_BY_OTHER`, `carrier: "PR #1321 (gov/aid-116-pin-and-attribution)"` |

Timestamps 2026-11-27T14:38 / 14:56:28 / 14:50 (+08). **Grade:** VERIFIED. **Disposition:** three carriers disagree with `main` — the directory is merged, the INDEX row says `PR_OPEN`, the ledger says another line occupied it. Correction text in §5, not applied.

### F-05 — `AID-2026-188` is merged via #1337, while branch `renumber/1329-188` still tries to create the same directory

| Field | Value |
|---|---|
| `AID-2026-188/` on `main` | `evidence.md` `bd8bee389c78307407ef6292c5d3d18669359a50`; `manifest.yaml` `038a2e2935123e5a0f035d6a781c73a5d2e6cde6`; `prompt-v1.md` `c03204b6bf272c058a077985e606aac6a0020231`; `session-evidence.md` `035c5f2026c0af714653ba937655273e5eead87c` |
| INDEX row | **L299**, status cell `MERGED — PR #1337; merge f6ef2545913754da7859abfaad5559fdc68074ce` |
| PR | GraphQL `pullRequest(1337)`: `MERGED`, `mergedAt 2026-11-26T15:34:46Z`, `mergeCommit f6ef2545913754da7859abfaad5559fdc68074ce`, head `c1a485cb23161fa38cd5fd71f4cea937ce1e6fee` |
| Merge reachable from base | `git merge-base --is-ancestor f6ef2545 5670357d` → `exit=0` |
| Competing branch | `origin/renumber/1329-188` head `452285b9366cd26dd5fd23a86d77b061b0c94d95` (`fix(index): drop stale AID-2026-115 row duplicated by the main merge`) |
| Divergence | `git rev-list --left-right --count 5670357d...origin/renumber/1329-188` → `868  5` |
| The branch's own `AID-2026-188/manifest.yaml` | `99cc3460489215a35e7b8c16c5f136139c93ce18` — **≠** `main`'s `038a2e29…` |
| Ledger | blob `9020f0a2` L181-183: `state: IN_FLIGHT`, `carrier: "PR #1337 (external)"` |

Timestamps 2026-11-27T14:38 / 14:56:28 (+08). **Grade:** VERIFIED. **Disposition:** #1337 is merged; the ledger's `IN_FLIGHT` is stale. The renumber branch would produce an **add/add conflict** on `AID-2026-188/manifest.yaml` if rebased and pushed. Recorded only; nothing renamed, no branch touched.

### F-06 — F-02 report: `v2.11` supersedes `v2.10` on `main`; the only residual live contradiction is AC-15

| Observation | Value | Command | Timestamp (+08) | Grade |
|---|---|---|---|---|
| Report blob | `8dd23ea35d1bce478073b7a122969f65c3e27e29` | `git ls-tree 5670357d -- 00-governance/reports/bilingual-baseline-remediation-report.md` | 2026-11-27T14:56:29 | VERIFIED |
| Line count | `1472` | `git cat-file blob 8dd23ea3 \| split('\n')` | 2026-11-27T14:56:29 | VERIFIED |
| Declared version | `v2.11` at **L50** | byte-exact line scan | 2026-11-27T14:56:29 | VERIFIED |
| `v2.10` as the declared version | `0` occurrences of `Report Version: v2.10` | same scan | 2026-11-27T14:56:29 | VERIFIED |
| `v2.11` revision note | **L1455-L1459**: "its sole reason for existing is a state that v2.10 left half-corrected … Ten further places were left asserting, in the present tense, that F-02 Requirement 2 is `NOT_VERIFIED` or that F-02 overall is `PARTIAL`" | same scan | 2026-11-27T14:56:29 | VERIFIED |
| `FAIL / BLOCKED` occurrences in the whole file | **1** | `d.count(b"FAIL / BLOCKED")` | 2026-11-27T14:56:29 | VERIFIED |
| That occurrence | **L869** `\| AC-15 \| Reproducible independent acceptance \| Review package and exact file SHAs recorded \| FAIL / BLOCKED — CI failure and outstanding findings \|` | byte-exact line scan | 2026-11-27T14:56:29 | VERIFIED |
| Counterpart assertions | L505 `F-02 overall status: COMPLETE / VERIFIED`; L640 `F-02 overall COMPLETE / VERIFIED`; L968 `F-02 overall: COMPLETE / VERIFIED`; L1023 `No F-02 blocker remains`; L1164 `Required-check enforcement is COMPLETE / VERIFIED as of 2026-11-25`; L1180 past-tense narrative; L1437-L1452 the v2.11 note itself | byte-exact line scan | 2026-11-27T14:56:29 | VERIFIED |

**The residual, stated precisely.** At `5670357d`, report L869 is the **only** line in the document that still asserts `FAIL / BLOCKED` for an F-02-related criterion, while six other places assert the opposite. AC-06 at L860 also reads `FAIL`, but that row rests on "v1.2 not adopted", an acknowledged and non-contradictory fact — it is not a self-contradiction. So AC-15 is the single live internal contradiction that v2.11 did not convert.

**Grade:** VERIFIED (blob, line, text, counts). **Disposition:** **recorded, not edited.** Correcting L869 requires the report's own §0 re-open procedure and its owner; editing it here would be a normative edit, which this record is forbidden to make. Correction proposal appears in §5 as C-06.

### F-07 — `192.168.1.108:20127` is a web console, not an MCP endpoint; the `502 ETIMEDOUT` classification is REFUTED

| # | Probe | Raw output | Timestamp (+08) | Grade |
|---|---|---|---|---|
| F-07.1 | TCP reachability | `Test-NetConnection 192.168.1.108 -Port 20127 -InformationLevel Quiet` → `True` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.2 | `GET /` | `http=307`, `redirect=http://192.168.1.108:20127/dashboard`, `t=0.274196s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.3 | `GET /` following redirects | `http=200`, `final=http://192.168.1.108:20127/login`, `t=0.025890s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.4 | `GET /login` | `http=200`, `t=0.009948s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.5 | `GET /mcp` | `http=404`, `t=0.016370s` | 2026-11-27T14:58:25 | VERIFIED |
| F-07.6 | Occurrences of the port in the governed tree | `git grep -n -I 20127 5670357d` → exactly 2 hits, both **prose**: `14-ai-development/work-items/AID-2026-078/session-evidence-1126.md:78` and `14-ai-development/work-items/AID-2026-241/evidence.md:73`, each inside a sentence about `ECONNREFUSED / ETIMEDOUT`. **Zero hits in `scripts/`, `.github/`, `crates/`, or any executable path.** | 2026-11-27T14:56:29 | VERIFIED |

**Grade:** NOT_REPRODUCED (for the `502`/`ETIMEDOUT` failure mode) and VERIFIED (for the observed behaviour). **Disposition:** the endpoint is a reachable HTTP console that exposes no MCP route. The earlier classification is withdrawn. This record makes **no claim** about the MCP contract itself beyond what §2.7 shows: the in-repo memory-adapter boundary is a local JSONL subprocess, so an HTTP console on a LAN address is not on that path.

### F-08 — opencode-purge: `continue_loop_on_deny` is an accepted `experimental` key in 2.4.2; `subagent_depth=4` is live with default 1

| Layer | Evidence | Timestamp (+08) | Grade |
|---|---|---|---|
| Live config | `%USERPROFILE%\.config\opencode\opencode.json` **L163-L164**: `"experimental": {` / `"subagent_depth": 4`. `continue_loop_on_deny` occurs **0** times in the file. | 2026-11-27T14:20 | VERIFIED |
| Installed binaries | 2 copies, **both** 278,504,840 B, mtime 2026-11-26 14:08, **identical** `sha256 420c04c36407134e01ade0cec681c91407e119a0a5f37da69f097f61cbc7beee`: `…\ai.opencode.desktop\resources\opencode-cli.exe` and `…\Roaming\ai.opencode.desktop\cli\2.4.2-x64\opencode-cli.exe` | 2026-11-27T14:22 | VERIFIED |
| Key presence in the binary | `subagent_depth` ×6, `continue_loop_on_deny` ×2 (raw byte count, both binaries) | 2026-11-27T14:22 | VERIFIED |
| Experimental allowlists in the binary | `KL=["logLevel","server","subagent_depth","layout"]`; `GI=["disable_paste_summary","batch_tool","openTelemetry","primary_tools","continue_loop_on_deny"]` | 2026-11-27T14:22 | VERIFIED |
| Field semantics in the binary | `Maximum subagent nesting depth. Defaults to 1.` ×2 (UTF-16 field description, adjacent to `subagent_depth`) | 2026-11-27T14:44 | VERIFIED |
| Published schema | `https://opencode.ai/config.json` → `http=200`, `75055` bytes; `experimental.additionalProperties = false`; `experimental.properties` contains **both** `subagent_depth` and `continue_loop_on_deny`; `subagent_depth = {type: integer, minimum: 0, maximum: 9007199254740991}`; `continue_loop_on_deny = {type: boolean, description: "Continue the agent loop when a tool call is denied", deprecated: true}` | 2026-11-27T14:20 | VERIFIED |
| purge's own claim | `D:\code\opencode-purge\lib\catalog.js` **L314-L317**, verbatim: `// Only subagent_depth is a live 2.4 field. \`continue_loop_on_deny\` used to be / // written here, but 2.4 lists it in GI and drops it as an unsupported legacy / // setting, so writing it only added noise to the config.` | 2026-11-27T14:18 | VERIFIED (text as written) |
| DP-01 patch state, both binaries | `DEEP_ANCHORS` = **9** entries. **8/9** verified patched by offset in **both** binaries: original `find` string absent, replacement `repl` string present. Offsets e.g. `DEEP-IDENTITY-HI @261477553`, `DEEP-REFUSAL-LINE @261478528`, `DEEP-LENGTH-CAP @261485022`, `DEEP-24-IDENTITY @233918530`. | 2026-11-27T14:24 | VERIFIED |
| The 9th anchor | `DEEP-IDENTITY-COMMON` → `orig_off=-1`, `repl_off=-1` (**ABSENT_BOTH**). Its `find` text is a strict substring of `DEEP-IDENTITY-HI`'s, so it was consumed by that anchor rather than patched at its own offset. | 2026-11-27T14:24 | UNVERIFIED (independently patched) |
| Runtime load of `subagent_depth` | `~/.local/share/opencode/log/opencode.log`: `subagent_depth` 0, `continue_loop_on_deny` 0, `Unrecognized` 0 → no rejection warning, but also no load line | 2026-11-27T13:00 | NOT_VERIFIED |
| Actual nesting behaviour at depth 4 | no nested-spawn probe executed this round | — | NOT_VERIFIED |

**Grade:** VERIFIED for config/schema/binary/DP-01-offsets; NOT_VERIFIED for runtime behaviour.
**Disposition:** the "legacy-dropped key" claim is **refuted** — `continue_loop_on_deny` is in the 2.4.2 experimental allowlist `GI` **and** is a live property of `experimental` in the published schema (`additionalProperties:false`). Citing an allowlist as proof of dropping inverts what an allowlist is. `subagent_depth` is a live field with documented default `1`, configured to `4`. Neither key's **behaviour** was exercised.

### F-09 — "200 acceptance boxes" does not exist in any file

Claim under test: the `AID-2026-093` INDEX row asserts "… 200 acceptance boxes remain unchecked".

| Target at `5670357d` | Blob | `- [ ]` | `- [x]` |
|---|---|---|---|
| `00-governance/implementation-evidence/2026-11-26-20-decision-acceptance-register.md` | `4810c6f8d3b5676a44288dea5782681e0745af6f` | **10** | 0 |
| `docs/en/…/2026-11-26-20-decision-acceptance-register.md` | `dcae8a7cb5c6e03bf220d1d681744cc68361e87d` | 10 | 0 |
| `docs/zh-CN/…/2026-11-26-20-decision-acceptance-register.md` | `49b3aff58991b77545ab143d12782b65e71a5a69` | 10 | 0 |
| `13-engineering-decisions/technology-architecture-blueprint.md` | `7b6f2d139217dbe13ab3a3af31bfbff525f20e71` | 10 | 0 |
| `00-governance/templates/bilingual-umbrella-requirement-template.md` | `9265098d739369522000ebc54b8c0275ee7e5b6d` | 4 | 0 |
| `14-ai-development/PR-GOVERNANCE-001.md` | `579ef2def33696c76eb636a46d6737eaee04edd5` | 0 | 0 |
| **Whole tree** | — | **333** across **28** files | **32** |

Command: for every path in `git ls-tree -r --name-only 5670357d`, read `git cat-file blob <sha>` and count the byte sequences `- [ ]` / `- [x]`. Timestamp 2026-11-27T14:44 (+08). **Grade:** VERIFIED.

**Disposition:** the three language copies hold **30** boxes (10 + 10 + 10); the register alone holds **10**; the whole tree holds **333**. `200 = 20 × 10` is an arithmetic projection of a ten-item template across twenty DEC rows, presented in an INDEX cell as an observation. **Not corrected here** (INDEX is off-limits); correction text in §5 C-07.

### F-10 — single-writer: author == mergedBy on 40/40 merged PRs; review independence is structurally unavailable

| # | Fact | Evidence | Timestamp (+08) | Grade |
|---|---|---|---|---|
| F-10.1 | `author == mergedBy` on the 40 most recently updated merged PRs | GraphQL `pullRequests(states:MERGED, first:40, orderBy:UPDATED_AT DESC)` → `author_ne_mergedBy = 0`; `authors = ['oahcom']`; `mergedBy = ['oahcom']`; repository `totalCount = 865` merged PRs | 2026-11-27T14:58:25 | VERIFIED |
| F-10.2 | All open PRs are authored by the same account | GraphQL `pullRequests(states:OPEN)` → `open_total = 16`, `open_authors = ['oahcom']` | 2026-11-27T14:58:25 | VERIFIED |
| F-10.3 | Repository is public | GraphQL `isPrivate=false`, `visibility=PUBLIC` | 2026-11-27T14:38 | VERIFIED |
| F-10.4 | `required_pull_request_reviews` is absent from branch protection | Report v2.11 L735 (EN) / L748 (ZH): "`GET /repos/…/branches/main/protection` returned HTTP 200: `required_status_checks.strict: true`; … **`required_pull_request_reviews` is absent**". L741: "It does not establish review enforcement: `required_pull_request_reviews` is absent, so a merge needs the checks but not an approving review." 13 independent occurrences in the file agree. | 2026-11-27T14:56:29 | VERIFIED (documentary) |
| F-10.5 | Live re-read of `/protection` | not performed — authenticated REST core quota `0/5000` | — | NOT_VERIFIED |

**Grade:** VERIFIED for F-10.1–F-10.4; NOT_VERIFIED for F-10.5.
**Disposition:** `OUT-OF-SCOPE(dev-baseline)`. Platform-level independent review is **structurally unavailable**: one account, no required reviews, so a second session or a second browser cannot manufacture an independent approver. This is recorded as a capability boundary and is **not** simulated anywhere in this record — no independent reviewer is claimed.

### F-11 — MCP integration surface: the in-repo contract is a local subprocess, not HTTP

| Carrier | Fact |
|---|---|
| `chatgpt-session-ops/src/session_ops/memory_adapter_client.py` | module docstring states a JSON Lines protocol, contract v0.1, "No shell, no retry, no network, no MCP, no third-party dependency"; `import subprocess` |
| `chatgpt-session-ops/references/memory-adapter-contract-v0.1.md` | "Preferred transport: JSON Lines over stdin/stdout"; MCP must never become a mandatory dependency of SO |
| This repository at `5670357d` | `git grep -n -I 20127` → 2 hits, both narrative prose in work-item evidence (F-07.6). No code path. |

**Grade:** VERIFIED for the port/code claim (F-07.6). **Disposition:** an HTTP console at `192.168.1.108:20127` is not part of any MCP code path in this repository. No MCP server was started, connected or exercised in this round; the runtime claim is **NOT_VERIFIED** (§6, N-04).

### F-12 — Prior closeout attempt on this line is superseded, and its CI result is evidence about this deliverable's shape

Draft PR **#1414** (`docs/wb-line03-closeout`, head `28b48f00654e03b872f2c1104ddc2c488858eaa6`, base `b12bfe8c`) was opened by an earlier attempt of this line. It is still open. Its own check rollup, read at 2026-11-27T14:40 (+08), was:

```
rollup FAILURE
  GOV-DOC-002 metadata checks  SUCCESS
  Repository hygiene (hard gate)  SUCCESS
  GOV-DOC-001 structural checks  FAILURE
  Bilingual docs coverage (ratchet)  FAILURE
  Branch freshness vs base  FAILURE
  Session Evidence  FAILURE
  (rust/clippy/fmt/doctest/BMCP/schema: SUCCESS)
```

**Grade:** VERIFIED (rollup read via GraphQL `statusCheckRollup`). **Disposition:** `Branch freshness` failed because its base moved during its life — the same structural hazard this record mitigates by pinning a base and refusing to chase `main` (§1.2). The three substantive failures are analysed against the local gate scripts in §3, and the ones this single-file deliverable cannot satisfy are stated as such rather than hidden.

---

## 3. Gates run against this commit

Each gate is the repository's own script, run from the branch worktree with the same arguments its workflow uses. "Workflow name" is the required check context the job publishes.

| # | Gate (workflow context) | Verdict |
|---|---|---|
| 3.1 | GOV-DOC-002 metadata checks (`document-management.yml`) | PASS |
| 3.2 | GOV-DOC-001 structural checks — traceability leg (`bilingual-docs.yml`) | PASS |
| 3.3 | Bilingual documentation gate (`bilingual-docs.yml` / `Bilingual docs coverage (ratchet)`) | **FAIL** — structural, explained |
| 3.4 | Repository hygiene (`repository-hygiene.yml`) | PASS |

**Raw output, as executed.** The four commands below were run from the branch worktree against commit `5417d49c` — the commit that introduces this file. The only difference between `5417d49c` and the file you are reading is the text of this section, which no gate reads; the same four commands re-run at the PR head give the same four exit codes (§3.5).

### 3.1 GOV-DOC-002 metadata checks — PASS

```
$ python scripts/check_document_management.py --require-changed 5670357db7a836d4f26838dbaf99494af41e2b65
…
manual controls (not machine-verified, policy 9.2): M-01 … M-10
PASS (incremental): no GOV-DOC-002 violations; 752 classified, 370 unclassified
  Incremental verdict only: files outside the changed set were not required to be classified.
exit=0
```

### 3.2 GOV-DOC-001 structural checks, traceability leg — PASS

```
$ python scripts/check_governance_operation_traceability.py --check
GOVERNANCE OPERATION TRACEABILITY: PASS (7 operations x 3 mirrors)
exit=0
```

The same workflow context also runs `check_owner_namespace_references.py --check` and `check_bilingual_docs.py`; the latter is 3.3.

### 3.3 Bilingual documentation gate — **FAIL (exit 2)**

```
$ BASE_SHA=5670357d HEAD_SHA=5417d49c PR_BODY=<the body of this PR> python scripts/check_bilingual_docs.py
::notice::reviews/bmcp-architecture-followup/BMCP-ARCH-001.en.md: 'HISTORICAL — not a gate input'; …
::notice::reviews/bmcp-architecture-followup/BMCP-ARCH-001.zh-CN.md: 'HISTORICAL — not a gate input'; …
::error::New bilingual gap outside frozen baseline: 00-governance/reports/2026-11-27-wb-line03-closeout.md
exit=2
```

**Why it fails, stated rather than worked around.** `00-governance` is a `NORMATIVE_ROOTS` entry (`scripts/check_bilingual_docs.py`), so a new `.md` there is a bilingual gap until it is either paired with `docs/en/…` + `docs/zh-CN/…` mirrors, registered in `EMBEDDED_BILINGUAL_SOURCES`, or covered by an Owner-approved `BILINGUAL-EXCEPTION` block in the PR body. This record is **one file by order**, and registration is a code edit to a validator — both out of bounds. Neither declaration is asserted in the PR body because neither would be true: there is no Chinese counterpart, and no Owner approval exists.

**Disposition:** `OUT-OF-SCOPE(order)` — the defect is a genuine conflict between the delivery shape and repo policy, not a defect this record may paper over. Remedy: a follow-up PR adding the two mirrors, or an Owner-approved time-bounded exception. This is also why draft #1414's `Bilingual docs coverage (ratchet)` check was red (§2 F-12).

### 3.4 Repository hygiene — PASS

```
$ python scripts/ci/check_repository_hygiene.py --base 5670357d --head 5417d49c
Work-item manifest consistency unrecognized shape: 14-ai-development/work-items/AID-2026-096/manifest.yaml
… (10 such lines, all pre-existing at the base commit)
Work-item index membership version=2026-11-27.2 directories=138 linked=138
Work-item manifest consistency version=2026-11-27.2 manifests=127 in_scope=112 excluded_by_record_type=5 unrecognized=10 violations=0
Repository new-file admission version=2026-11-27.2 base=5670357db7a836d4f26838dbaf99494af41e2b65 head=5417d49cdac7a303b5d388b5e55710e9a3c7fe20 merge_base=5670357db7a836d4f26838dbaf99494af41e2b65
Repository new-file admission passed: 1 new path(s) checked.
exit=0
```

`violations=0` and new-file admission passed on exactly one new path. The ten `unrecognized shape` lines are the base commit's own backlog (`unrecognized=10`), not introduced here.

### 3.5 Gate summary

| Gate | Context | Exit | Verdict |
|---|---|---|---|
| Document management | GOV-DOC-002 metadata checks | 0 | PASS |
| Traceability | GOV-DOC-001 structural checks | 0 | PASS |
| Repository hygiene | Repository hygiene (hard gate) | 0 | PASS |
| Bilingual | Bilingual docs coverage / GOV-DOC-001 structural checks | 2 | **FAIL — new gap outside frozen baseline, see 3.3** |

Three of four pass. The fourth fails for a structural reason the order created, and it is reported as a failure rather than converted into a passing run by asserting a declaration that is not true.

---

## 4. What this record did not do

- No edit to `INDEX.md`, any `manifest.yaml`, `aid-ledger.yaml`, `scripts/`, `.github/`, or any normative document — including the F-02 report whose L869 defect is recorded in §2 F-06.
- No merge, no force-push, no branch deletion, no Issue open/close/edit, no renumbering, no new work item, no ledger write.
- No write anywhere under `D:\code\chatgpt-session-ops`.
- One file added: this record. See §7.

---

## 5. Corrections needed in the ledger

Ledger baseline for every row below: `origin/aid-ledger` head `5592658f12f02ada111ccd338600ad2e17d7d2f4`, `aid-ledger.yaml` blob `9020f0a27945fcc3657d7fd35ab9cb699ee41855` (251 lines). **None of these corrections has been applied** — the ledger is outside this record's write boundary. The last column is the exact text an owner would need.

| # | Ledger row | What it says now | What is true at `5670357d` | Evidence | Exact correction for the ledger owner |
|---|---|---|---|---|---|
| C-01 | `AID-2026-112`, L134-L137 | `state: OCCUPIED_BY_OTHER`; note: "… The retroactive gate-coverage work item was reassigned to **AID-2026-151** by the external line (**PR #1329**) …" | The occupancy is right; the explanation is wrong twice. #1329 is **merged** (`76684cb2`, head `11fde79a`) and landed **AID-2026-174**, not 151. `AID-2026-151` never entered `main`. The occupant of 112 is **#1316** (`8722a37b`); #1309, the only other claimant, was **closed unmerged** (`2026-11-27T04:31:22Z`). | §2 F-01, F-02, F-03 | Keep `state: OCCUPIED_BY_OTHER`. Replace the note with: `note: "main carries a different AID-2026-112 from PR #1316 (merge 8722a37b). The retroactive gate-coverage record was renumbered 112 -> 151 -> 174 on the external branch and merged as AID-2026-174 in PR #1329 (merge 76684cb2, head 11fde79a). AID-2026-151 never entered main. PR #1309, the other claimant of 112, was closed unmerged (head df192ede)."` |
| C-02 | `AID-2026-116`, L150-L153 | `state: OCCUPIED_BY_OTHER`; `carrier: "PR #1321 (gov/aid-116-pin-and-attribution)"` | #1321 is **MERGED** (head `e61e714a`) and `AID-2026-116/` **is on `main`** (four blobs, §2 F-04). `OCCUPIED_BY_OTHER` describes a number held by someone else's landed work; here the work landed and the number is consumed. The INDEX row at L72 compounds it by still reading `PR_OPEN`. | §2 F-04 | Change to: `state: MERGED` / `carrier: "PR #1321 (gov/aid-116-pin-and-attribution), merge commit not recorded; head e61e714a"`. Separate defect, separate owner: INDEX L72's status cell should move off `PR_OPEN`. |
| C-03 | `AID-2026-117`, L240-L242 | `state: FREE`; note: "do not trust this row … the next plausibly free number is >= 189." | `FREE` holds — `117` is absent from the tree (`git grep` exit 1). But the note's floor is stale: `main` already carries AID-2026-241/253/260/261/279/280/290. A row instructing the reader not to trust itself is not a usable reservation record. | §2 F-02 evidence set; `git grep -n -I AID-2026-117 5670357d` → exit 1 | Keep `state: FREE`. Replace the note with: `note: "re-verified absent on main@5670357d. Do not reuse the 189 floor: main already carries 241/253/260/261/279/280/290. Re-scan the main work-items tree immediately before any reservation push."` |
| C-04 | `AID-2026-151`, L158-L161 | `state: IN_FLIGHT`; `carrier: "PR #1329 (external, head f8236828)"` | **Stale on all three fields.** #1329 is `MERGED` (`2026-11-26T18:48:41Z`, merge `76684cb2`); its merged head is `11fde79a`; the work item it landed is `AID-2026-174`. `f8236828` is **not** an ancestor of the merged head (`exit=1`). `AID-2026-151` is branch-only and absent from `main`. | §2 F-01, F-02 | Replace the block with: `- id: AID-2026-151` / `state: SUPERSEDED` / `carrier: "renumbered to AID-2026-174 before merge; landed by PR #1329 (merge 76684cb2, head 11fde79a)"` / `note: "branch-only identifier (commits c84a8191, f8236828). Never present on main. Do not reuse."` |
| C-05 | `AID-2026-188`, L181-L183 | `state: IN_FLIGHT`; `carrier: "PR #1337 (external): records that the 03-memory-brain normative root is already registered"` | #1337 is **MERGED** (`2026-11-26T15:34:46Z`, merge `f6ef2545`, head `c1a485cb`); `AID-2026-188/` is on `main` with four blobs; INDEX L299 says `MERGED`. The branch `renumber/1329-188` (`452285b9`, 868 behind / 5 ahead) still creates `AID-2026-188/` with a **different** `manifest.yaml` blob (`99cc3460` vs main's `038a2e29`) → add/add conflict on rebase. | §2 F-05 | Change to: `state: MERGED` / `carrier: "PR #1337, merge f6ef2545, 2026-11-26T15:34:46Z, head c1a485cb"` / append: `note: "branch renumber/1329-188 (452285b9) still carries a divergent AID-2026-188/manifest.yaml (99cc3460 vs main 038a2e29); it must be dropped or renumbered before it is rebased."` |
| C-06 | F-02 report **L869** (not a ledger row, but the same class of stale assertion) | `\| AC-15 \| Reproducible independent acceptance \| … \| FAIL / BLOCKED — CI failure and outstanding findings \|` | Every other F-02 assertion in the same document reads `COMPLETE / VERIFIED` (L505, L640, L968, L1023, L1164, L1180). L869 is the single residual. | §2 F-06 | Under the report's §0 re-open procedure only: reclassify AC-15 to state which of its two historical reasons still stands, or mark it `PARTIAL — historical CI failure run 44477435608 retained as a bound record`. **This record does not edit it.** |
| C-07 | `AID-2026-093` INDEX row (INDEX blob `c14118f8`) | "… **200** acceptance boxes remain unchecked" | No file and no issue carries 200 boxes. Register **10**; the three language copies **30**; the whole tree **333** across 28 files. | §2 F-09 | Replace the number with `333 open \`- [ ]\` across 28 tracked files at 5670357d (the register itself: 10)` and mark it as a tree-wide count, not a per-register count. **This record does not edit INDEX.** |

### 5.1 RESERVED self-errors

The ledger's own reservation rows contain method errors that make the reservations un-auditable, independent of whether the numbers are free. Recorded; not corrected.

| # | Row | The self-error | Evidence | What a correction would need |
|---|---|---|---|---|
| R-01 | `AID-2026-262` L196-L199 | `carrier` cites "local worktree wt-a262 (commit 2b63b8ba) + ref origin/work-item/aid-2026-262-merge-broker (commit 8908bb16)", and the note says the number was occupied by an unpublished local implementation, "AIDSCAN 判定其非权威占用". A reservation decision that rests on the contents of a local, unpublished worktree is not reproducible by any other party. | Ledger blob `9020f0a2` L196-L199 | Either publish the worktree ref and the commit, or replace `carrier` with the landed carrier and drop the local-worktree claim from the justification. |
| R-02 | `AID-2026-263` L224-L227 | The note justifies the reservation with "AIDSCAN 五范围零命中（main 全历史 2829 提交 / 2349 ref 去重 1317 唯一树 / ledger 21 版本 / 280 worktree / PR refs 无降级）". None of those five scans is a command, a script path, or an output file — the claim cannot be re-run from this record. | same blob, L224-L227 | Append `verification: "AIDSCAN command: <path>; raw output: <path>; reproducible=yes"`, or re-run the scan and cite it. |
| R-03 | `AID-2026-281` L200-L203 | The note asserts "main work-items tree occupies up to AID-2026-279; AID-2026-280 was consumed by PR #1384". The same ledger's R-04 note says main carries **AID-2026-290** above 279. Two reservation notes in one file disagree about the tree's high-water mark. | same blob, L200-L203 vs L243-L246 | Restate 281's premise against the actual high-water mark (`git ls-tree 5670357d -- 14-ai-development/work-items/`) instead of a remembered one. |
| R-04 | `AID-2026-284` L243-L246 | Premise "main work-items tree carries only AID-2026-280 and AID-2026-290 above 279" — checkable, and correct in shape, but stated without a command. | same blob, L243-L246 | Add the `git ls-tree` invocation and its output. |
| R-05 | `AID-2026-285` L247-L250 | Note says "285 scanned free on the main tree and on **all 18 open PR head trees**". At 2026-11-27T14:58:25 the repository had **16** open PRs; earlier in the audit it had **23**. A count of open PRs is a moving target, so "all N open PR head trees" is not a reproducible scope. | GraphQL `pullRequests(states:OPEN)` → `open_total` = 16 at 14:58:25, 23 at 14:38 | Restate as "scanned against the open-PR head set at `<timestamp>`, N=…; the set changes, re-scan before use". |

**Grade for all of §5:** VERIFIED (the quoted text and the counter-measurements). **Disposition:** corrections are proposals. Nothing in §5 has been written to the ledger, to `INDEX.md`, or to the F-02 report.

---

## 6. NOT_VERIFIED / UNVERIFIED register

| # | Item | Why it stays open | What would settle it |
|---|---|---|---|
| N-01 | `experimental.subagent_depth = 4` **runtime behaviour** | The key is present in the config and in the binary's allowlist, but `opencode.log` contains no load line and no rejection line, and no nested-spawn probe was run. | Spawn a subagent at depth 1 that itself spawns, and observe whether the 5th level is refused with `Increase "experimental.subagent_depth" to allow nested subagents.` |
| N-02 | `continue_loop_on_deny` **behaviour** | The key is absent from the live config, so there is nothing to exercise. Its *existence* in 2.4.2 and in the schema is verified; its effect is not. | Set the key on a scratch profile, deny a tool call, observe whether the loop continues. |
| N-03 | Live re-read of `branches/main/protection` | Authenticated REST core quota `0/5000`; unauthenticated returns `401`, not the payload. F-10.4 therefore rests on the report's 2026-11-25 readback, not on a fresh call. | `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` with a token after quota reset. |
| N-04 | MCP runtime: no server started, no session connected, no tool round-trip | Explicitly out of scope for a dev-baseline audit; the memory-adapter boundary is a local subprocess (F-11) and no MCP endpoint exists at the probed address (F-07). | A live MCP session against a named endpoint, with the handshake and one tool call recorded. |
| N-05 | `AID-2026-263`'s "AIDSCAN five-scope zero-hit" | Not reproducible from this record (R-02). | Publish the scan command and its raw output. |
| N-06 | `#1256`-class approver identity | No natural-person carrier exists; self-designation by the same account is not evidence. | An independent record naming a natural person, outside this repository. |
| N-07 | `DEEP-IDENTITY-COMMON` (DP-01 anchor 5 of 9) patched at its own offset | Its `find` string is a strict substring of `DEEP-IDENTITY-HI`'s, so it is `ABSENT_BOTH`: consumed by the neighbouring anchor rather than replaced in place. Its **original** text is gone (good), but it is not independently evidenced (unproven). | Byte-diff the region around `261477553` in an unpatched 2.4.2 build and show the common-string occurrence is the same bytes as the HI occurrence. |
| N-08 | Behaviour of every open PR's head tree | Only the specific PRs named in §2 were inspected. `AID-2026-285`'s "all N open PR head trees" claim (R-05) is not re-run here. | `git ls-tree` each open PR head for the identifier in question. |

---

## 7. Write boundary and self-audit

| Item | Value |
|---|---|
| Branch | `docs/wb-line03-closeout-final` |
| Base | `5670357db7a836d4f26838dbaf99494af41e2b65` — newest `origin/main` at branch-cut time (2026-11-27T14:5x +08) |
| Files added | 1 — `00-governance/reports/2026-11-27-wb-line03-closeout.md` |
| Files modified | 0 |
| Files deleted | 0 |
| Commit SHA / blob SHA | In the commit object and the Draft PR body. A file cannot contain its own blob SHA without changing it, so it is recorded there, not here. |
| Supersedes | Draft PR #1414 (same line, base `b12bfe8c`, head `28b48f00`), which was based on a `main` that has since moved 520 commits. #1414 is left untouched by this record. |

Verification that exactly one path differs from the base:

```
git diff --stat 5670357d...HEAD
```

---

## 8. Method notes (for reproduction)

- **Repository reads** used `git cat-file blob <sha>`, `git ls-tree <ref> -- <path>` and `git grep -n -I <pat> <ref>` against an explicitly pinned SHA. No working-tree read was used as evidence, because a working tree cannot be pinned.
- **Line numbers** were computed by splitting the blob's raw bytes on `\n`. PowerShell's `>` redirection re-encodes and re-wraps the stream and silently changes the line count (measured: 1222/2514 lines for a 1472-line blob), so no line number in this record comes from a redirected file.
- **Box counts** are `bytes.count(b"- [ ]")` over each blob, enumerated from `git ls-tree -r --name-only <ref>`.
- **Binary inspection** was raw byte search for ASCII and UTF-16 constants, plus `str.find` at the recorded offsets. No disassembly; no modified binary was executed.
- **GitHub reads** were GraphQL, or unauthenticated REST for the run-read endpoints. The token was read from the credential file and never printed. Authenticated REST core quota was 0, which is why no `/protection` re-read exists (N-03).
- **Network probes** were `Test-NetConnection -InformationLevel Quiet` and `curl.exe -m 5 -w` with explicit timeouts; every result is recorded with its `time_total`.
