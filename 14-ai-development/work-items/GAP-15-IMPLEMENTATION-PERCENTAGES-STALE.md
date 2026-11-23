---
document_metadata:
  domain: ai-development
  role: work-record

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Every figure in §1 was produced by a command in §6, executed on the stated commit in this session. No figure is quoted from an earlier document."
    usage_status: Active
    modification_status: Unchanged

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative

  bilingual_counterpart:
    source: null
    en: null
    zh-CN: null
---

# GAP-15 — the six implementation percentages are fossils, and two of them invert the dispatch decision

**Status:** measurement only · **Severity:** Tier 1 (misroutes work) · **Owner:** none required to read; the one dispatchable gap is named in §4
**Measured at:** `4ce12cc7` (2026-11-23, re-verified after `fb37a44b`) · **Supersedes:** §9.2 and §10.2 of `GAP-10-IMPLEMENTATION-FRONTIER`, both now stale
**Related:** GAP-10, GAP-12, GAP-13, GAP-14, `D-OWNER-DECISION-CANONICAL-COMMIT-001`, `D-OWNER-DECISION-PARTICIPANT-ADMISSION-001`, `D-OWNER-DECISION-PROTECTED-VISIBILITY-001`

## 1. What I measured, and what it says about the six numbers

| stated | measured at `4ce12cc7` | verdict |
|---|---|---|
| Memory Compiler **85% unimplemented** | `compile` reachable from `brain-cli` through a production adapter; `canonical_commit_confirmed` now resolved from the durable `canonical_commits` row (`publication_authority.rs:123`); whole workspace green | **wrong, and the residue is not code** |
| Memory Context **80% unimplemented** | crate present, budget/sufficiency/observability modules landed, tests green | **wrong** |
| Agent Integration **90% unimplemented** | crate consumed by `brain-cli`; `context_snapshot_reaches_agent_adapter_and_preserves_compiler_contract` passes across the crate boundary | **wrong** |
| BMCP **60% unimplemented** | 22 message types indexed, `PASS`; 3 recognised in Rust, 2 public parsers, **19 unparsed** | **right in spirit, wrong by 2** — and **the row itself has since expired; see `GAP-16`** |
| Phase 2 domain **100% not started** | `#[ignore]` in the whole workspace: **0**. `dm2_06` exists and is not ignored. `CanonicalCommitRefState { Pending, Issued }` is implemented | **wrong, and it inverts the dispatch** |
| E2E **100% not started** | full chain passes; 8 test binaries under `crates/brain-cli/tests/`, including `e2e_full_chain` and `e2e_full_pipeline` | **wrong, and it inverts the dispatch** |

Workspace total at this commit:

```
$ cargo test --workspace --all-targets --no-fail-fast
PASSED=718  FAILED=0  IGNORED=0
```

`todo!()` count across `crates/`: **0**. `#[ignore]` count: **0**.

## 2. Why two of these matter more than a percentage being wrong

"Phase 2 not started" and "E2E not started" do not just understate. They point at the wrong action.

- Believing "Phase 2 not started" dispatches 20 acceptance dimensions of implementation. **19 of the 20 already pass**, and the 20th stopped being `#[ignore]` when `OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` landed the three-state ref. A dispatch based on that number re-does merged work — which is exactly how PR #573 died, re-implementing four APIs that PR #570 had already merged.
- Believing "E2E not started" dispatches an integration harness. **The harness exists and passes.** What is absent is a *successful `Published` disposition*, which is a different thing: the chain runs end to end and is *observably blocked* at the publication gate, by design.

The second distinction is the one worth spending words on, because the two facts look identical from a percentage and are opposites operationally.

## 3. The frontier, stated as three items rather than six percentages

Everything else in the six rows is code that exists.

1. **A successful `Published` disposition.** Not missing code. Missing *external issuers* — see §5. Not dispatchable by anyone inside this repository.
2. **BMCP: 19 unparsed message types.** Dispatchable, but **frozen** — see §4. Dispatch it now and the work is unmergeable by construction.
3. ~~`dm2_06`'s authorization type state.~~ **Closed.** The three-state ref exists; the ignore is gone. GAP-10 §9.3 still lists this as blocked, and that listing is stale as of this measurement.

## 4. The one dispatchable gap, and why I did not dispatch it

> **This section expired at `main` `021f5a3f`.** `parse_dispatch` now exists in `crates/bmcp-protocol/src/lib.rs` with all 22 arms; the figures below were measured at `fb37a44b`, which is an ancestor of `main` but not an ancestor of the commit that added dispatch (`6007782b`), so it could not see it. The current state is in `GAP-16`. This section is kept unedited because the reasoning about *why* dispatching parsers against an unfrozen mapping is a bet still holds, and because deleting a wrong measurement is how the same measurement gets made again.

The BMCP residue is precise, and worth recording even though it cannot proceed:

| measured element | value | command |
|---|---|---|
| unique `message_type` in schemas | 22 | `python 08-bmcp-protocol/scripts/check_protocol_index.py` → `PASS` |
| recognised anywhere in `crates/` | **3** | `git grep -l <TYPE> -- crates/` per type |
| public parsers in `bmcp-protocol` | **2** | `grep -rn '^pub fn parse_'` → `parse_and_validate`, `parse_storage_receipt` |
| message types with no Rust recognition | **19** | §6 |

The 19: `COC_PARTICIPANT_MANIFEST`, `COC_RECOVERY_CUTOFF_BATCH`, `C_PROVIDER_OUTCOME_RECORDED`,
`I_JF10_TERMINAL_DECISION_OBSERVED`, `JF10_BRIDGE_RECONCILIATION_RECORDED`,
`JF10_I_TERMINAL_DECISION_OBSERVED`, `JF10_PREPARED_PARTICIPANT_REGISTERED`,
`JF10_PREPARE_INTENT_REGISTERED`, `JF10_STORAGE_PARTICIPANT_RESOLVED`, `OWNER_ADMISSION_ENTRY`,
`OWNER_ADMISSION_SNAPSHOT_ATTESTATION`, `OWNER_GATE_RELEASE_ATTESTATION`, `OWNER_LOCAL_GATE_RELEASE`,
`OWNER_LOCAL_PENDING_GATE`, `PARTICIPANT_SET_RECONCILIATION`, `RECOVERY_CUTOFF_BATCH`,
`RECOVERY_EPOCH_COMPLETED`, `RECOVERY_JOIN_PROOF`, `STORAGE_JF10_PARTICIPANT_RESOLVED`.

**Why this is not dispatched, in one line:** `TECH-REALITY-001-C/README.md:70` records that
*"H wire mapping remains NOT FROZEN"*. A parser is a binding of wire bytes to a Rust type. Write
19 of them against an unfrozen mapping and every one of them is a bet that the mapping does not
change — and the repository already has a rule against exactly this shape of work (§9.3: "Frozen
by H, so dispatching it produces unmergeable work").

This is not me refusing a task. It is the difference between a gap that a session can close and a
gap that a session can only *describe accurately*, and the description is the deliverable in the
second case.

I also record the alternative I rejected: generating 19 parsers directly from the 22 JSON Schemas.
It looks attractive — the schemas are present, the pointers are indexed — but it would manufacture
19 artifacts whose conformance criterion is the schema's current text, which is the very thing not
yet frozen, and it would do so without any call site that consumes them. `bmcp-server` reaches no
parser at all today (`describe()` in `lib.rs:718-723` is `#[allow(dead_code)]` with zero call sites).
Producing parsers with no consumer, against an unfrozen mapping, is not progress; it is inventory.

## 5. Why `Published` is not a code gap, and cannot be made one from here

All three blocking flags now have an authoritative ruling, and two of those rulings say **permanently
`false` for this baseline**:

| flag | ruling | what it decides |
|---|---|---|
| `canonical_commit_confirmed` | `D-OWNER-DECISION-CANONICAL-COMMIT-001` | content-bearing ref, durable row, record-backed validator — **landed** |
| `publication_participant_admitted` | `D-OWNER-DECISION-PARTICIPANT-ADMISSION-001` §1 | permanently `false`: no D-side issuer can lawfully establish COC-quorum, Storage-signature and I-terminal evidence |
| `protected_visibility_authorized` | `D-OWNER-DECISION-PROTECTED-VISIBILITY-001` §1 | permanently `false`: joint Storage + D/I boundary; no local component may substitute |

`publication_authority.rs:135-139` reports the last two as `false` **because the rulings say so**, not
because an issuer is missing by oversight. The comment there is explicit that they "must not be
inferred, defaulted or copied from the test-only authorities that hardcode `true`".

So the honest statement is: **`Published` is unreachable because three external bodies do not exist in
this repository** — a COC quorum, a Storage signing authority, an I terminal-decision authority. No
session, acting as any owner, can conjure a signature it does not hold. Writing code here would either
produce an unmergeable PR or forge authority, and both are worse than an accurate register.

That is the boundary of what "act as every owner" means, and it is worth stating plainly: an owner
session can *decide* contracts (and three owners did, which is why two flags are now resolved and one
is landed). It cannot *be* an external counterparty.

## 6. Reproduction

Platform: Windows, Git Bash, `cargo 1.100.0`. Local gcc lacks `cc1`, so the zig wrappers from
`GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022` §1 are required — the same workaround, recorded here
because a command that does not run is worse than no command.

```sh
export CC="$LOCALAPPDATA/Temp/opencode/zigcc.bat"
export AR="$LOCALAPPDATA/Temp/opencode/zigar.bat"
git log -1 --format='%h %ci %s'          # 4ce12cc7
```

```sh
cargo test --workspace --all-targets --no-fail-fast   # PASSED=718 FAILED=0 IGNORED=0
grep -rn '^#\[ignore' --include=*.rs crates/ | wc -l  # 0
grep -rn 'todo!\|unimplemented!' --include=*.rs crates/ | wc -l  # 0
python 08-bmcp-protocol/scripts/check_protocol_index.py          # unique_message_types=22 ... PASS
grep -rn '^pub fn parse_' crates/bmcp-protocol/src/*.rs          # 2
grep -rn 'canonical_commit_confirmed' crates/memory-compiler/src/publication_authority.rs | head
grep -n 'enum CanonicalCommitRefState' -A 3 crates/memory-domain/src/canonical_commit.rs
```

The BMCP coverage count per type:

```sh
for t in COC_PARTICIPANT_MANIFEST JF10_PREPARE_INTENT_REGISTERED OWNER_ADMISSION_ENTRY ...; do
  git grep -l "$t" -- crates/ || echo "ABSENT $t"
done
```

## 7. What this register does not do

- Does not edit GAP-10. §9.2 and §10.2 are stale; the correct fix is an errata section in GAP-10 by
  someone who can run the measurement themselves, and this document names the numbers so that errata
  can be written without re-deriving them.
- Does not dispatch the BMCP parsers, for the reason in §4.
- Does not claim the E2E chain reaches `Published`. It does not, and §5 is why.
- Does not assert independent review. I wrote this from the same session that measured it.
