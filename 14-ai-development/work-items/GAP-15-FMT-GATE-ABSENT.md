# GAP-15 — nothing runs `cargo fmt --check` before a merge, so it breaks twice an hour

**Status:** Open — measured, not hypothesised
**Area:** CI / engineering gate
**Severity:** low per occurrence, high by frequency
**Measured at:** `main @ caa37a7e`, 2026-11-22 03:30 UTC

## 1. The observation

Two fmt regressions reached `main` within fifteen minutes of each other, from two different commits, in two different crates:

| commit | file | caught by | fixed by |
|---|---|---|---|
| `c1e0dcdb` | `crates/memory-event-store-sqlite/src/lib.rs` (lines 277, 479) | me, running `--check` for an unrelated PR | #572 (`78985c6c`) |
| `#566` | `crates/brain-cli/tests/e2e_full_chain.rs` (lines 12, 43) | me, again, for an unrelated PR | #577 |

Neither was caught before merge. Both were found only because someone happened to run `cargo fmt --all -- --check` while validating something else.

## 2. Why the existing workflow does not catch it

`.github/workflows/rust-phase1.yml` is the only workflow that runs on `pull_request` for `crates/**`, and it runs exactly one command:

```yaml
- run: cargo test --workspace --all-targets
```

`cargo test` does not check formatting. A crate that compiles and tests green is fmt-red and the workflow still passes.

## 3. And it would not run anyway

All four check runs on the relevant heads carry the same annotation, verbatim:

> The job was not started because recent account payments have failed or your spending limit needs to be increased.

So even the one workflow that could catch a regression is not executing. `GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` returns `403 — Upgrade to GitHub Pro or make this repository public`, so no required-status-check can be configured either.

**The gate is therefore missing twice over**: the command is not in the workflow, and the workflow is not running.

## 4. What would actually fix it

Two independent layers, cheapest first.

**Layer 1 — one line in the existing workflow.**

```yaml
- run: cargo fmt --all -- --check
```

Placed before `cargo test`, this fails the job in ~5 seconds on a formatting diff. It costs nothing and requires no new file. It becomes effective the moment Actions billing is restored.

**Layer 2 — a pre-merge check that does not depend on Actions.**

The repository already has this pattern: `scripts/precheck_delivery.py` is a stdlib-only checker run manually against Rust sources. A sibling `scripts/check_fmt.py` that shells out to `cargo fmt --all -- --check` and exits non-zero would let the merger run one command before `PUT /pulls/{n}/merge`.

This matters more than Layer 1 in the current state, because Layer 1 cannot execute.

## 5. What I am not doing

I am not adding either layer in this work item. Both are CI/governance changes, and the repository's own rule is that a session must not create a new mandatory gate on its own authority (see the `#305` precedent: a session-level ruling cannot override an adopted governance tool, and a tool cannot expand beyond its declared scope). Registering the defect with measurements is within scope; deciding that every merge now requires a new check is not.

What I can say without any authority: **as of `caa37a7e`, `main` is fmt-red, and I fixed it twice by hand rather than by gate.**

## 6. Reproduce

```sh
curl -sL https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/tarball/caa37a7e | tar xz
cd oahcom-AiMemoryBrainArchitecture-*/
cargo fmt --all -- --check     # exits 1, two diffs in crates/brain-cli/tests/e2e_full_chain.rs
```

## 7. Closure criteria

1. `cargo fmt --all -- --check` is a step in `rust-phase1.yml` before `cargo test`.
2. A non-Actions path exists that a merger can run in one command, and the merge procedure names it.
3. A commit that is fmt-red cannot reach `main` for one full week.
