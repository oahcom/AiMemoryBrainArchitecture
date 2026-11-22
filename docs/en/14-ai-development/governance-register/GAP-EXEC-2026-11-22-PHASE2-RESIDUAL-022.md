# GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022

**Register**: GAP-EXEC-2026-11-22-PHASE2-RESIDUAL-022
**Nature**: MEASUREMENT_ONLY / NO_IMPLEMENTATION / REQUIRES_INDEPENDENT_REVIEW
**Measured at**: `main = b093b59f` (2026-11-22 12:29 +08:00)
**Date**: 2026-11-22
**Author**: coordination session (not an independent reviewer)
**Supersedes**: the rejected PR #589 (originally numbered 021, renumbered because `GOV-NC-2026-11-22-ENUM-BOUNDARY-021` had taken that number)

---

## 0. Why a rewrite rather than a revision

PR #589 was rejected by the Owner on two grounds, both correct:

1. **The denominator was stale.** It described `main` with a `dba34a35` measurement
   (9 ignores), when `main` actually had 2. Five of the APIs in its table existed.
2. **The reproduce command does not run.** The header said `AR=zigar`; that binary
   does not exist.

The second is the more serious: a register's entire value is "here is the command I
ran". A command that errors is worse than no command.

This file therefore puts the **current table first** and the historical one after it,
labelled `superseded`. That is what the #589 review asked for, and it is the right way
to read.

---

## 1. Current state (`main = b093b59f`, 2026-11-22 12:29 +08:00)

```
$ CC=zigcc AR=zigar cargo test --workspace --all-targets
binaries: 30
passed=503  failed=0  ignored=1
```

Platform: Windows 10, Git Bash, `cargo 1.100.0`. `zigcc` / `zigar` are local `.bat`
wrappers (`%LOCALAPPDATA%\Temp\opencode\zigcc.bat`) because the local gcc lacks `cc1`:

```
gcc.exe: fatal error: cannot execute 'cc1': CreateProcess: No such file or directory
```

On WSL2 the equivalent is `CC=zigcc AR="zig ar"` (`zig` is on PATH, no `.bat`
wrapper). **The two forms are not interchangeable.** That is the second reason #589
was rejected.

Exactly **1** ignore remains in `crates/memory-domain/tests/phase2_acceptance.rs`:

| line | test | blocked by |
|---:|---|---|
| 605 | `dm2_06_missing_authorization_ref_blocks_fact_publication` | authority I |

Phase 2 acceptance has 20 tests: **19 passing / 1 ignored**.

### 1.1 The one remaining gap: `dm2_06`

The reason, verbatim:

> `FactRevision::initial` requires an `AuthorizationDecisionRef`, but the only public
> constructor is `AuthorizationDecisionRef::pending_i()`; the type has no
> absent / validated-I-issued state, so a missing authorization cannot be proven to be
> refused. Round 4's `fact_with_placeholder_attestor_validates_today` pins the fact
> that the current placeholder passes.

Measurement confirms this reason **still holds**:

```rust
// memory-domain/src/lib.rs — the doc comment on pending_i()
/// NOT DEFINED: awaiting I. Placeholder only; security identity semantics are not inferred.
/// `pending_i()` is public and any caller can create this placeholder. It is not proof of
/// an attestor identity. This known temporary construction window closes only when I
/// defines the contract and the placeholder is replaced by a validated, non-forgeable ref.
```

This is the **only** Phase 2 entry hard-blocked by an external decision. What it needs
is not code but I issuing the `AuthorizationDecisionRef` contract (at least three
states `Absent` / `Pending` / `Validated`, with `FactRevision::validate` returning
`Err` on the first two).

**A known conflict must be handled with it**: `fact_with_placeholder_attestor_validates_today`
pins "the current placeholder passes". The new criterion and that test are mutually
exclusive, so both must change together; changing either alone turns the suite red.

---

## 2. Historical table (`dba34a35`, **superseded**, for traceability only)

This is the table #589 used as "current". It accurately describes `dba34a35` and
**accurately describes no later commit**. It is kept because it records the original
reason text for all 9 ignores, and 8 of those no longer exist in the code — the reason
text can only be recovered from here.

| test | reason at `dba34a35` | closed by |
|---|---|---|
| `dm2_01` | no `ClaimRevisionRegistry` / `register_revision` | #570 `5c50b910` |
| `dm2_02` | no `AcceptedRevisionState` | #570 `5c50b910` |
| `dm2_03` | no `classify_claim_change` | `classify()` added by #545 `444deef1`; body rewritten by #567 `caa37a7e` |
| `dm2_04` | no `ClaimRevisionResolver` / `resolve_claim_head` | #570 `5c50b910` |
| `dm2_06` | see §1.1 | **not closed** |
| `dm2_08` | no `RelationTypeRegistry` | #574 `241e385c` (+ #581 `a0d4f7d7` distinguishing failure modes) |
| `dm2_09` | `RelationExtension` has no `scope_refs` | #574 `241e385c` |
| `dm2_11` | `Provenance` has no `validate` / `parent_provenance_refs` / `unavailable_reason` | #583 (`Provenance` now carries `source_version_refs`, `parent_provenance_refs`, `unavailable_reason`, `method_version` + `validate`) |
| `dm2_12` | no `ProvenanceGraph` / `DerivationEdge` / `validate_independent` | #582 `fe9e25a5` |

### 2.1 `dm2_03` is the only methodological evidence in this series

`dm2_03`'s ignore reason was already false at `dba34a35` — `classify()` landed with
#545, and 19 tests cover the 10 reachable CIs out of CI-01..CI-13. It was found by
running, not by reading:

```sh
grep -rc "classify" --include=*.rs crates/memory-domain/src/
cargo test -p memory-domain --lib claim_identity   # 19 passed
```

That is precisely why the Owner kept this section: "you checked it against the code
instead of against the previous document". But #567 then rewrote and merged it, so this
section is historical too.

---

## 3. Final correction to "Phase 2/3 domain model: 100% not started"

The claim is false at all three measurement points, and increasingly so:

| measured at | passing acceptance dimensions | remaining ignores |
|---|---:|---:|
| `dba34a35` | 11 | 9 |
| `fe9e25a5` | 18 | 2 |
| `b093b59f` | **19** | **1** |

The real state of Phase 2: **19 acceptance dimensions pass, 1 waits on authority I**.
Not "not started" — "one closing item left, held by an external decision".

The value of this correction is not the number but the **disposition**, which is
completely different:

- Believing "not started" leads to dispatching work that writes specs and
  implementations for 20 dimensions, 19 of which already exist — duplicate labour.
  (#573 was closed for exactly this: it re-implemented four APIs #570 had landed.)
- Seeing "19 pass, 1 blocked" makes the only correct action **wait for I's decision**,
  and dispatch nothing.

---

## 4. What I learned from these two rejections

Both rejections point at the same defect: **describing a new state with an old
measurement**.

The first (register 021 v1 → v2) made me add "is a parallel PR doing this". The second
(#589 rejected) shows that is not enough — I added "check open PRs" but **did not check
merged PRs**, and did not re-run before writing.

The corrected pre-publication checklist:

1. `git fetch && git reset --hard origin/main`, record the actual HEAD;
2. run the reproduce command on that HEAD and paste its output into the document;
   do not cite the previous round's output;
3. the reproduce command must **actually execute on this host** before it goes into
   the document (#589's `AR=zigar` did not);
4. check open PRs **and recently merged** PRs — both;
5. the first row of any table must be the current measurement point; history goes
   after it and is labelled `superseded`.

Item 3 is new. Items 1 and 2 were already in place for 021 v2, but I never verified the
command itself.

---

## 5. What this register does not do

- does not modify `phase2_acceptance.rs`;
- does not add production code;
- does not claim `dm2_06` is doable — it waits on I;
- does not claim to be an independent review (the author is a coordination session);
- does not touch `INDEX.md` (this is a register entry, not a new work item);
- does not reuse number 021 (taken by `GOV-NC-2026-11-22-ENUM-BOUNDARY-021`).

## 6. Re-verification checklist

```sh
# Platform: Windows Git Bash; the local gcc lacks cc1, hence the .bat wrappers
export CC="$LOCALAPPDATA/Temp/opencode/zigcc.bat"
export AR="$LOCALAPPDATA/Temp/opencode/zigar.bat"

git fetch && git reset --hard origin/main && git clean -fd
git log -1 --format='%h %ci %s'

cargo test --workspace --all-targets
grep -n "#\[ignore" crates/memory-domain/tests/phase2_acceptance.rs
```

Expected at `b093b59f`: `passed=503 failed=0 ignored=1`, the only ignore at line 605.
If the ignore count differs, §1 and §3 must be re-measured; do not carry them forward.
