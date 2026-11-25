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
      verification_status: Verified
      last_verified_date: "2026-11-24"
      last_verification_note: "Every count in this register came from a script run in this session against main aae8b25b8: the 33-register list came from git ls-tree; the status tokens from a regex sweep of each root file; the README coverage from substring matching each register id against README.md; the three behavioural measurements ran scripts/check_bilingual_docs.py in a throwaway worktree on real commits; the PR #869 review count came from the GitHub REST API. No figure is carried over from another register."
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
  bilingual_counterpart:
    source: "14-ai-development/governance-register/GOV-NC-2026-11-24-REGISTER-INDEX-031.md"
    en: null
    zh-CN: "docs/zh-CN/14-ai-development/governance-register/GOV-NC-2026-11-24-REGISTER-INDEX-031.md"
---

# GOV-NC-2026-11-24-REGISTER-INDEX-031

**Status:** `OPEN` / `MEASUREMENT_ONLY` / `NO_IMPLEMENTATION`
**Nature:** `REGISTER_ONLY / NO_GATE_CHANGE / REQUIRES_INDEPENDENT_REVIEW`
**Measured at:** `main = aae8b25b8`
**Register author:** orchestrator session acting as owner-proxy. **Not** an independent reviewer, **not** the accountable owner.

---

## 1. Conclusion first

The register centre holds 33 registers. The README's "register list" names **11** of them; the other **22** do not exist in the only index. The status field is free text: **10 of the 33 have no status line at all**, and the ones that do use **14 mutually incompatible status words**, plus one register that puts an identifier into the status field.

The consequence is measured, not inferred: **three registers carried a wrong status for two days and nothing could have noticed**, because

1. none of them is in the index (`011`, `021` and `007` are all outside those 11);
2. even if seen, the status column is prose with no value set to compare against;
3. no gate reads register status — neither `check_bilingual_docs.py` nor `check_document_management.py` touches it.

This file contributes two things: a table covering **all 33**, and measured corrections to three registers. It proposes no implementation and authorises no merge.

---

## 2. The coverage gap (measured)

| Quantity | Value | Source |
|---|---|---|
| Registers at the root of `governance-register/` | **33** | `git ls-tree` @ `aae8b25b8` |
| Named in the README register list | **11** | substring match of each id against `README.md` |
| **Absent from the index** | **22** | set difference |
| README table rows | 12 | `^\| \`ID\`` match |
| README row with no register file | **1** | `OWNER-DECISION-REVIEW-INDEPENDENCE-001` |

The 22 include the most load-bearing registers in the series:

```
GOV-NC-2026-11-21-REGRESSION-009      GOV-NC-2026-11-21-SPLIT-DOMAIN-011
GOV-NC-2026-11-21-SELF-REVIEW-007     GOV-NC-2026-11-22-ENUM-BOUNDARY-021
GOV-NC-2026-11-21-GATE-DEADLOCK-006   GOV-REV-2026-11-21-PARTIAL-SCOPE-019
GOV-NC-2026-11-21-PAIRING-RESIDUAL-013 GOV-NC-2026-11-21-EMBEDDED-ROOT-015
GOV-NC-2026-11-21-SUFFIX-SCOPE-017    GOV-NC-2026-11-21-CWD-SPLIT-014
GOV-REV-2026-11-21-GATE-MUTANTS-016   GOV-NC-2026-11-20-CI-NOT-EXECUTED-005
   … 22 in total; the full list is in §5
```

The index is not "approximate". It is **one third**.

---

## 3. One field serving three meanings

Taking each of the 33 status lines verbatim yields 14 status words. They do not belong to one axis:

**Axis A — lifecycle state (migrates)**

| Token | Count | Meaning |
|---|---|---|
| `OPEN` | 13 | not disposed of |
| `RULED` | 1 | decided, implementation pending |
| `DISPATCHED` | 1 | work order issued |
| `FIXED-UNGUARDED` | 1 | fixed, no regression test |
| `FIXED-CLOSED-BY-OTHER` | 1 | fixed by another route |
| `RESOLVED_ON_MAIN` | 1 | measured resolved on main |
| `ACCEPTED` | 2 | acknowledged, not fixed |

**Axis B — register nature (does not migrate)**

`MEASUREMENT_ONLY` (2), `NO_IMPLEMENTATION` (1), `SELF_REVIEW_IDENTIFIED` (1)

**Axis C — residual condition (hangs off A)**

`NOT_REMEDIATED` (4), `NOT_ASSIGNED` (4), `CI_NOT_EXECUTED` (1), `ACTIVE` (2)

**And a third kind: identifiers written into the status field.**

`AID-2026-054` (2), `OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025` (1), `GAP-18-AUTHORIZATION-VALIDATOR-REMAINDER` (1)

**This is the root of the whole mechanism problem**: one field carries three axes, so no two registers' status strings are comparable. `OPEN / NOT_REMEDIATED` and bare `OPEN` say the same thing but look different; `MEASUREMENT_ONLY` is not a state at all yet occupies the state slot. No gate can validate the field without a value set, so no gate validates it, so its errors go unseen.

`ENUM-BOUNDARY-021` has enum in its name — it records the bilingual gate's enumeration boundary. The register centre has no enumeration of its own. That juxtaposition needs no embellishment.

---

## 4. Measured corrections to three registers

All three were written at a moment when the defect did not yet exist, or had not yet been found. They are not products of fabrication; they are products of **having no recheck trigger**.

### 4.1 `SPLIT-DOMAIN-011` — correct when written, void 1 h 42 min later

| Item | Value |
|---|---|
| Register measurement point | `main = cb04524`, 2026-11-21 **18:48:20** +0800 |
| `check_normative_pairing()` body at that point | **30 lines**, no `side_by_side_partner` |
| Fixing commit | `5f109308d`, 2026-11-21 **20:30:42** +0800 |
| Function body after that commit | **51 lines**, contains `side_by_side_partner` |

So §1's claim — "`14-ai-development` passes, the other eight roots fail" — was **true at `cb04524`**. Today's measurement:

| Case (real PR-diff shape, `BASE_SHA = HEAD~1`) | `EXIT` |
|---|---|
| `02-domain-model/….zh-CN.md`, one side edited | **1** |
| `02-domain-model/….zh-CN.md` + `….md`, both sides edited | **0** |
| `14-ai-development/AI-EXEC-INDEPENDENCE-RULING-001.en.md`, one side edited | **1** |
| the same pair, both sides edited | **0** |

**The two roots behave identically.** §1's asymmetry is gone. §2's "the deadlock has no legal exit" falls with it — the exit is "edit both sides", and it does not require forging a seven-field exception.

§4's mirror regression is also gone. Constructing "Chinese source + `docs/en` mirror, no `docs/zh-CN`":

| Root | `EXIT` | Verdict |
|---|---|---|
| `02-domain-model/hm.md` | **2** | `New bilingual gap outside frozen baseline` — correctly a gap |
| `14-ai-development/hm.md` | **0** | Shape 3 legal shape — correctly accepted |

The Shape 3 branch is confined to `14-ai-development/` again.

**This file draws no inference about whether the author of `5f109308d` knew `011` existed.** It records only the timing: the register was written at 18:48, the fix landed at 20:30, and the register was not touched again.

### 4.2 `ENUM-BOUNDARY-021` — the register and its fix are one commit

| Item | Value |
|---|---|
| Status line | `OPEN — Awaiting implementation and independent verification` |
| Commit that introduced the register file | `8ab40fb4f`, 2026-11-22 10:37:32 +0800 |
| Same commit also changed | `scripts/check_bilingual_docs.py` (+186/−46) |

The register and the implementation it asks for **landed together**. The status line was never updated.

Both defects, measured (`main = aae8b25b8`, throwaway worktree):

| Claim | Measurement | Verdict |
|---|---|---|
| `current_bilingual_gaps()` walks the filesystem, so it collects untracked files | wrote an untracked `00-governance/PHANTOM-UNTRACKED-PROBE.md`; the scan **did not** include it; the gap set stayed at **77** | fixed: `git ls-files` is the sole enumeration authority |
| `write_baseline()` does not validate the worktree | with an untracked file present it returned **2** and printed `working tree is not clean; ?? 00-governance/DIRTY-PROBE.md` | fixed: a dirty tree is refused |

"Implementation complete, independent verification outstanding" is the real residual. "Awaiting implementation" is not.

### 4.3 `SELF-REVIEW-007` — not stale, re-confirmed by me

The status `ACCEPTED / SELF_REVIEW_IDENTIFIED / S-2 APPROVED_IN_PRINCIPLE / IDENTITY_NOT_ASSIGNED` is accurate. Measuring my own merge with the register's own instrument:

| Field | PR #869 |
|---|---|
| author | `oahcom` |
| merged_by | `oahcom` |
| reviews | **0** |
| APPROVED | **0** |
| last commit → merge | **115 seconds** |

007's table measured 13 s and 40 s. 115 s is longer, but no structural condition changed: **one writable identity, author equals merger, zero approvals**.

> **〔Added 2026-11-25〕** The sentence lists "one writable identity" and "author equals merger" — two account-layer facts — as the "structural conditions" for judging that merge's independence, and infers from their being unchanged that "no structural condition changed". Section 5 was amended on 2026-11-24 by `2eb4e352` (PR #935) to a session-level test (see `GOV-REV-2026-11-24-INDEPENDENCE-IS-SESSION-LEVEL-036`): a different session under the same GitHub identity is an independent review. `/pulls/{n}/reviews` returns only `user.login`, not the session, so the step "same identity ⇒ same session" cannot be verified from that payload. This should be read as **"account layer not independent; session layer not verified"**. **What survives is "zero approvals"**: it is an `APPROVED` count and does not depend on the version of section 5 — no version of section 5 turns a `COMMENTED` review into an approval, so `APPROVED = 0` for #869 holds independently, and on its own it already shows that merge obtained no approval. **Also surviving is** the 115-second interval measurement. **What does not survive is** treating "one writable identity / author equals merger" as structural conditions of the independence test — equal identity no longer implies equal session, so "no condition changed" does not cover independence.

So 007 is not a register awaiting correction. It is a register **awaiting disposition and externally blocked**. The README's "a boundary that must be recorded" section already measured `PUT /branches/main/protection` returning 403 (private repository, plan does not support it), so "prevent it technically" does not exist in this repository's current state. That still holds; this file does not re-measure it.

---

## 5. The full list (33 registers, two booleans measured per row)

"Status line" = the file contains a `状态:` / `Status:` field. "In index" = the README names it.

| # | Register | Status line | In index |
|---|---|---|---|
| 1 | `GOV-NC-2026-11-20-DIRECT-MAIN-001` | yes | yes |
| 2 | `GOV-NC-2026-11-20-SELF-AUTH-002` | yes | yes |
| 3 | `GOV-NC-2026-11-20-MERGE-AFTER-RULING-003` | yes | yes |
| 4 | `GOV-NC-2026-11-20-AC-UNMET-CLOSURE-004` | yes | **no** |
| 5 | `GOV-NC-2026-11-20-CI-NOT-EXECUTED-005` | yes | **no** |
| 6 | `GOV-NC-2026-11-21-GATE-DEADLOCK-006` | yes | **no** |
| 7 | `GOV-NC-2026-11-21-SELF-REVIEW-007` | yes | **no** |
| 8 | `GOV-NC-2026-11-21-ZERO-REVIEW-GATE-008` | yes | **no** |
| 9 | `GOV-NC-2026-11-21-REGRESSION-009` | yes | **no** |
| 10 | `GOV-NC-2026-11-21-DEV-PR-GATE-010` | **no** | **no** |
| 11 | `GOV-NC-2026-11-21-SPLIT-DOMAIN-011` | **no** | **no** |
| 12 | `GAP-EXEC-2026-11-21-012` | **no** | **no** |
| 13 | `GOV-NC-2026-11-21-PAIRING-RESIDUAL-013` | yes | **no** |
| 14 | `GOV-NC-2026-11-21-CWD-SPLIT-014` | yes | **no** |
| 15 | `GOV-NC-2026-11-21-EMBEDDED-ROOT-015` | yes | **no** |
| 16 | `GOV-REV-2026-11-21-GATE-MUTANTS-016` | yes | **no** |
| 17 | `GOV-NC-2026-11-21-SUFFIX-SCOPE-017` | yes | **no** |
| 18 | `GAP-EXEC-2026-11-21-018` | yes | **no** |
| 19 | `GOV-REV-2026-11-21-PARTIAL-SCOPE-019` | yes | **no** |
| 20 | `GOV-NC-2026-11-21-GATE-CLOSURE-020` | **no** | **no** |
| 21 | `GOV-NC-2026-11-22-ENUM-BOUNDARY-021` | yes | **no** |
| 22 | `GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022` | **no** | **no** |
| 23 | `GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023` | yes | **no** |
| 24 | `GAP-EXEC-2026-11-22-AUTHORIZATION-GATE-CONTRADICTION-024` | yes | **no** |
| 25 | `GOV-NC-2026-11-22-EVIDENCE-CONTRACT-026` | yes | yes |
| 26 | `GOV-NC-2026-11-22-PROVENANCE-REFERENCE-REVALIDATION-027` | **no** | yes |
| 27 | `GOV-NC-2026-11-23-PROVENANCE-GRAPH-ADD-SIGNATURE-028` | **no** | yes |
| 28 | `GOV-NC-2026-11-23-EXECUTION-RESTORED-029` | yes | yes |
| 29 | `GOV-NC-2026-11-23-UNREACHABLE-GUARD-030` | yes | yes |
| 30 | `GOV-NC-CONVERGENCE-2026-11-20` | yes | yes |
| 31 | `GOV-REV-2026-11-21-PR425-001` | **no** | **no** |
| 32 | `TEST-DRAFT-2026-11-21-PR425-M3` | **no** | **no** |
| 33 | `EX-20261123-01` | **no** | yes |

The ten without a status line: `DEV-PR-GATE-010`, `SPLIT-DOMAIN-011`, `GAP-EXEC-012`, `GATE-CLOSURE-020`, `GAP-EXEC-022`, `PROVENANCE-REFERENCE-REVALIDATION-027`, `PROVENANCE-GRAPH-ADD-SIGNATURE-028`, `PR425-001`, `PR425-M3`, `EX-20261123-01`.

---

## 6. A suggested minimal value set (proposal, not authorisation)

Split §3's three axes into three fields with finite domains:

```
lifecycle:  OPEN | RULED | DISPATCHED | FIXED | RESOLVED | CLOSED
nature:     DEFECT | MEASUREMENT | DECISION | EXCEPTION
residual:   NONE | NOT_REMEDIATED | NOT_ASSIGNED | UNGUARDED | UNVERIFIED
```

`MEASUREMENT_ONLY` and `NO_IMPLEMENTATION` move into `nature`; `NOT_REMEDIATED` and `NOT_ASSIGNED` move into `residual`; identifier references leave the status field for a `dispatch:` field.

**This file does not self-authorise that scheme.** It needs an Owner ruling or a separate work order; the issuing authority is not in this session. It is recorded here only so the next reader does not have to rebuild the value set out of 33 pieces of prose.

---

## 7. What this file does not do

- It does not change the status lines of `011`, `021` or `007`. They still carry the literal values §4 judged stale or confirmed. Changing them means editing 3 files across 3 language copies, and this file already states the truth; whether to patch status lines first or adopt the value set first is the Owner's choice, not mine.
- It does not add README rows for the 22 missing registers. Adding 22 rows requires judging severity and scale for each, which is rewriting the index, not completing it.
- It does not test whether the technical claims of the 30 registers outside §4 still hold. Their "status line / in index" bits are mechanically testable and are measured here; their technical conclusions are not, and are not written up here in any form of verdict.
- It does not claim any gate changes behaviour because of this file. Neither `check_bilingual_docs.py` nor `check_document_management.py` reads register status, and this file does not change that.
