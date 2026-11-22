# GAP-EXEC-2026-11-22-MEASUREMENT-REPRODUCIBILITY-023 — the recorded commands do not run, and the two test counts measure different things

**Status:** measurement-integrity register, not an acceptance decision
**Measured at:** `f3ddeb76` (main), local runs on 2026-11-22
**Corrects:** the reproduce block in `GAP-10-IMPLEMENTATION-FRONTIER.md` §9.1, and by extension §8.3
**Related:** register 022 (rejected for this exact defect), GAP-10 §7.1, PR #598, PR #600

## 0. What this document is, after a correction to itself

My first draft of this register re-measured the six workload percentages. That was wrong,
and I am recording why rather than quietly deleting it.

`GAP-10-IMPLEMENTATION-FRONTIER.md` §9 (merged as `f3ddeb76`, PR #598) had already done
that re-measurement at `d89fd5fa8`, one hour before I started. Its §9.2 table is correct
and its conclusion — "one decision-gated disposition, one transport-frozen binary, one
owner-gated type state, not six percentages" — is better than what I had written. Producing
a second copy would have been the same duplicated labour this repository already paid for
once when #573 rewrote four APIs that #570 had landed.

So this document keeps only what §9 does not have, and what §9 gets wrong.

## 1. The defect: §9.1's reproduce command cannot be executed on this host

`GAP-10` §9.1 records:

```
$ CC=<zigcc> AR=<zigar> cargo test --workspace --all-targets --offline
TOTAL passed=503 failed=0 ignored=1
```

`AR=<zigar>` is a placeholder for a binary that does not exist here:

```
$ which zigar
(not found)
```

This is not a cosmetic complaint. Register 022 was **rejected** for writing
`AR=zigar` without testing it — the reviewer's words were that it "fails: `error occurred
in cc-rs: failed to find tool \"zigar\": program not found`". §9.1 was merged with the same
defect, three hours later, by a different session. The numbers in it happen to be right;
the command that claims to produce them is not runnable.

**What actually works on Windows, verified by building the workspace with it:**

```
CC = <...>/zigcc.bat      # wraps `zig cc`
AR = <...>/llvm-ar.bat    # wraps llvm-ar
```

`llvm-ar.exe` ships with the rust toolchain at
`~/.rustup/toolchains/stable-x86_64-pc-windows-gnu/lib/rustlib/x86_64-pc-windows-gnu/bin/`.
The obvious alternative does not work either: `zig ar` rejects `cq`, so `libsqlite3-sys`
cannot use zig as its archiver:

```
$ <...>/zigcc.exe ar rcs liba.a a.o
error: ar: unrecognized file extension
```

WSL2 uses a third form (`CC=zigcc AR='zig ar'` with `zig` on PATH). Three platforms, three
pairs, none interchangeable. A register that names one and implies it is universal is
wrong on the other two.

## 2. The second defect: 503 and 508 are both correct, and they are not the same measurement

`GAP-10` §8.3 records `476 / 0 / 3`; §9.1 records `503 / 0 / 1`. A later session running
the same workspace without `--all-targets` gets `508 / 0 / 1`. Neither is a regression, and
neither is a miscount. They are different target sets:

| command | test targets executed | passed | failed | ignored |
|---|---|---|---|---|
| `cargo test --workspace --all-targets` | 32 | **503** | 0 | 1 |
| `cargo test --workspace` | 41 | **508** | 0 | 1 |

The 9-target difference is doc-tests. `--all-targets` excludes them; the default run
includes them, and 5 of the 9 doc-test targets contain tests (the `memory-domain` compile-fail
examples), which is exactly the 5-test gap.

`GAP-10` §7.1 already recorded this class of error once:

> 438/0/9 vs §6.1's 385/0/10; `--all-targets` and `--lib` count different target sets

It is now the third time a test count in this repository has been ambiguous about its target
set. The fix is not a better count. It is that **a test count without its target set is not
a measurement**, and every future register should write the command, not the number.

## 3. What §9 gets right, and one thing it understates

§9.2's six-row correction is accurate against the tree I measured at `f3ddeb76`. The two
claims worth confirming independently, because they are the ones that change dispatch:

**Agent Integration is not 90% unimplemented.** `crates/agent-integration/src/lib.rs` is
1399 lines with two integration suites (`context_snapshot_delivery.rs`,
`delivery_lifecycle.rs`, 444 lines), and `brain-cli` depends on it. §9.2 says this.

**BMCP is not 60% unimplemented.** §9.2 says "protocol artifacts substantial … transport
still absent — a binary, not a percentage." That is right, and `GAP-16` (PR #606) measures
it more precisely than I did: 22 unique `message_type` values across 32 schemas, and exactly
one has a Rust parser.

**A correction to my own first draft, because I made the counting error I am criticising.**
I wrote that `bmcp-protocol` "has 52 public functions and zero consumers". The 52 came from
`grep -c "pub fn "`, which counts every field getter inside `evidence::AppliedDeliveryEvidence`.
The actual crate surface is:

```
$ grep -c "^pub fn " crates/bmcp-protocol/src/lib.rs
1
```

One top-level public function: `parse_and_validate`, whose return type names the single
message it can produce. That is a different artifact from "a protocol stack 60% complete",
and it is a different claim from mine. My number was arithmetically correct and
semantically wrong — the same defect as writing `503` without saying `--all-targets`.

What survives from my observation, and it is worth keeping: **no crate depends on
`bmcp-protocol`** (`grep bmcp crates/*/Cargo.toml` returns only its own name), and
`agent-integration` imports nothing from it. So the parser that exists is unreachable from
the product path. That is a wiring fact, not a percentage, and `GAP-16` reaches the same
conclusion by counting message types instead.

## 4. The blocker §9.1 records — and my own first correction of it was also wrong

§9.1 says of `dm2_06`:

> this one is decision-blocked, not code-blocked — the same category §1.2 put it in, now
> the only member of that category.

My first draft of this section said that framing had expired because I had frozen the
authorization contract in `c9a6394d` (#595), and that `dm2_06` had therefore become
implementation-blocked and E-owned. **That correction was itself wrong**, and
`OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001` (PR #603) shows why. I am recording the
mistake rather than replacing it silently, because the mistake is the more useful artifact.

### The conflation

Two questions had been filed as one:

- **`B-P2-XO-01`: is this authorization genuine?** That needs I's cryptographic contract,
  key custody, quorum and a validator. It is genuinely blocked, and stays blocked.
- **`dm2_06`: is an authorization present at all?** That needs a type able to represent
  absence. It needs nothing from I.

`dm2_06`'s own acceptance sentence picks the second: *"missing or invalid I authorization
reference prevents Fact publication"*. "Prevents" is a property of the gate; "missing" is a
property of the value.

So freezing I's contract in #595 did **not** unblock `dm2_06`. I read "I has decided
something about authorization" and concluded "the authorization blocker is gone". Those are
different blockers that share a noun — the same error as reading `52 pub fn` as 52
capabilities because they share a keyword.

### The actual defect, which is stronger than the missing test

`crates/memory-domain/src/lib.rs:837` — `initial` takes authorization as a **required,
non-`Option`** parameter (the struct field is at `:819`), and the type is a unit struct with
one constructor:

```rust
pub struct AuthorizationDecisionRef(());
impl AuthorizationDecisionRef {
    pub const fn pending_i() -> Self { Self(()) }
}
```

`Self(())` carries no state, so **no value of this type means "absent"**. Every
`FactRevision` that exists asserts an I authorization nobody issued, and the type system
prevents anyone from saying otherwise. The missing test is a symptom; the unrepresentable
absence is the defect.

### What the decision requires, and it is not I's contract

| state | meaning |
|---|---|
| `Absent` | no authorization decision recorded |
| `Placeholder` | a value exists, known unvalidated (`pending_i()`) |
| `Issued(..)` | a reference *claimed* I-issued; authenticity not asserted |

Only `Absent` blocks. `dm2_06` becomes two assertions: absent+attested fails `validate()`;
placeholder+attested validates. The second is what keeps the decision honest — without it a
reader sees only "absent is rejected" and assumes "present is verified".

The naming rule is part of the contract: `Issued`, not `Valid` or `Verified`. A name that
reads as proof converts an open question into a false answer.

### What this means for the category

`dm2_06` is **not** decision-blocked in the sense §9.1 meant (waiting on I), and it is not
implementation-blocked in the sense my first draft meant (E implementing #595). It is
blocked on a type-state decision that has now been recorded in PR #603 and is
unimplemented. Three descriptions, three different owners — which is exactly why the
category label matters more than the count.

Verified unchanged at `d1250877`, after #603 was opened:

```
$ grep -n "pub struct AuthorizationDecisionRef" crates/memory-domain/src/lib.rs
531:pub struct AuthorizationDecisionRef(());
```

The type still cannot represent absence. PR #603 is documentation; the change it authorizes
is a separate act.

## 5. What is still true and still unowned

1. **CI has never executed a test.** Re-verified this session on three separate heads: every
   check run is `completed / failure` with one annotation —
   *"The job was not started because recent account payments have failed..."* Re-running the
   failed jobs returned `201 Accepted` and reproduced the identical annotation.
2. **A non-billed path exists and is narrower than it looks.** The self-hosted runner
   `zesu-x64` is online and completed a job at `04:41:52Z`. But its job-started hook denies
   any job whose `GITHUB_REF` is not exactly `refs/heads/main`
   (`ubuntu-self-hosted-runner-bootstrap.en.md` §4.1), observed directly as
   `DENY reason=ref_not_default_branch` on run `44988094101`. So the runner **cannot gate a
   PR**; it can only produce a post-merge result on `main`. PR #600 carries that workflow,
   restricted to `push: branches: [main]` and `workflow_dispatch`, and states the limitation
   instead of implying a gate.
3. **Independent review `NOT_ASSIGNED`.** No register in this series has been independently
   reviewed.
4. **Implementation authorisation `NOT_AUTHORISED`.** **Sponsor / accountable_owner
   `NOT_ASSIGNED`.**

## 6. Pre-publication checklist

Carried forward from register 022 §4, which caught two real defects there, plus one new item
because §9.1 shows the checklist was not applied repository-wide.

1. Every commit sha was re-read from the API this session, not quoted.
2. Every count came from a command executed this session.
3. **Every reproduce command was executed on this host before being written down.** The
   `CC`/`AR` pair in §1 is the pair that built the workspace; `AR=zigar` was tested and does
   not exist; `zig ar` was tested and rejects `cq`.
4. Numbers not re-measured are labelled with their measurement commit.
5. **New: a test count is written together with its target set.** `503` means
   `--all-targets`; `508` means default. Neither is "the" number.
6. **New: a symbol count is written together with its scope.** `52 pub fn` counts field
   getters inside a module; `1` counts the crate's top-level surface. I got this wrong in
   this document's own first draft and corrected it in §3 — which is why the rule is here
   and not only in the abstract.

## 7. What this document does not claim

- It does not claim §9's numbers are wrong. They reproduce. Its command is wrong.
- It does not claim any gap is closed. Presence of code is not acceptance.
- It does not re-litigate the six percentages. §9.2 settled that and this document defers
  to it.
- It does not authorise implementation. §8 item 12 of the frozen I contract assigns
  `dm2_06` to E; this records the assignment, it does not make it.
