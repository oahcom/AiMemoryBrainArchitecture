# CI gates and ratchets

**Document:** GATE-CI-001
**Status:** ACTIVE — authored and locally verified; not yet observed running (see §1)
**Related:** GAP-10 Tier 2 item 2 (T2.2), GAP-08, GAP-09, DOC-OPS-001, AI-RUN-002-RUNBOOK

This document states which gates CI runs, which of them are hard gates and which
are ratchets, and what a ratchet baseline means. The workflow is
`.github/workflows/gates.yml`; the ratchet tool is `scripts/ci/gate_ratchet.py`.

## 1. These jobs have not run yet, and this document does not claim they have

Every job in `gates.yml` is pinned to `ubuntu-latest`. On this account,
GitHub-hosted minutes are blocked by a billing failure: branch protection on
`main` returns `403`, and every check run carries the annotation *"the job was
not started because recent account payments have failed"*. `rust-phase1.yml` has
therefore never executed a single test in this repository's history.

The status of this work is exactly: **the workflow file is correct and every
command it runs was executed locally with the output recorded.** Nothing here is
evidence that a check run went green. Do not read it as that.

The jobs are deliberately *not* moved to the self-hosted runner. Two binding
rules prevent it:

* **L1 (service layer):** the runner's job-started hook denies any job whose ref
  is not `refs/heads/main`. A `pull_request` job is denied with
  `ref_not_default_branch` before any step runs.
* **L2 (repository layer):** `scripts/ci/audit_runner_admission.py` rejects
  `pull_request` on any self-hosted job.

A gate that can only run after merge is not a gate. These jobs therefore stay on
the hosted runner, where they will start running when the billing block is
cleared.

## 2. Jobs

| Job | Gate | Command | Kind |
|---|---|---|---|
| `protocol-index` | BMCP message index vs schema `message_type` constraints | `python3 08-bmcp-protocol/scripts/check_protocol_index.py` | hard gate |
| `conformance` | BMCP conformance suite | `python3 -m unittest discover -s 08-bmcp-protocol/tests/conformance` | hard gate |
| `schema-nonempty` | schema non-empty constraint audit | `python3 08-bmcp-protocol/schemas/test_nonempty_audit.py` | ratchet |
| `bilingual` | GOV-DOC-001 full bilingual coverage scan | `python3 scripts/check_bilingual_docs_full.py` | ratchet |
| `rust` | formatting, lints, tests | `cargo fmt --all --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `cargo test --workspace` | hard gate |

### 2.1 Why `conformance` is a hard gate

The suite needs two dependency sets, and both are installed before it runs:

* `08-bmcp-protocol/tests/conformance/provider_outcome/requirements.txt`
  (`jsonschema`, `rfc8785`, `cryptography`).
* `npm ci` in `08-bmcp-protocol/tests/conformance` (`canonicalize@5.1.0`).

With both installed the suite is fully green on `main`: **585 tests, 27 skipped,
0 failures, 0 errors**. Without the Node install, three cross-language vector
tests error with `ERR_MODULE_NOT_FOUND`. That is a missing dependency, not a red
gate, which is why the install step is part of the job rather than a note.

Because the suite is green, it is a hard gate. Had it been red, it would have
been a ratchet.

## 3. What a ratchet is, and what it is not

`schema-nonempty` and `bilingual` are red on `main` today. GAP-09 and GAP-08
record how they got there: nothing ran them, so nothing noticed.

Turning them into hard gates immediately would paint every pull request red for
reasons no author caused. That does not produce compliance; it produces a check
everybody learns to ignore, which is the failure mode that let the gates reach
`main` red in the first place.

A ratchet instead pins the *exact set* of currently-failing items and fails when
that set changes in either direction:

1. **A failure appears that is not in the baseline** — a regression. Fails.
2. **A baseline item no longer fails** — the baseline is stale. Also fails.

The second rule is the one that keeps a ratchet honest. Without it the baseline
silently absorbs fixed items and becomes a permanent blanket exemption. With it,
fixing an item forces the author to lower the baseline in the same pull request.

**A ratchet is not a green exemption.** The gate is not "allowed to be red"; it
is "required to be no worse, and required to stay honest about it".

## 4. Baselines

Baselines are files under `scripts/ci/baselines/`, one failing item per line,
`#` starting a comment.

| File | Items | Meaning |
|---|---|---|
| `scripts/ci/baselines/schema-nonempty.txt` | 5506 | schema constraints absent from the bilingual audit inventory |
| `scripts/ci/baselines/bilingual-docs.txt` | 81 | normative paths with no `en` / `zh-CN` counterpart |

Regenerate a baseline only when the failure set legitimately changed:

```bash
python3 08-bmcp-protocol/schemas/test_nonempty_audit.py \
  | sort -u > scripts/ci/baselines/schema-nonempty.txt

python3 scripts/check_bilingual_docs_full.py \
  | grep -E '^[0-9]{3}\. ' | sed -E 's/^[0-9]{3}\. //' | sed -E 's/ -> .*$//' \
  | sort -u > scripts/ci/baselines/bilingual-docs.txt
```

Run a ratchet locally exactly as CI does:

```bash
python3 scripts/ci/gate_ratchet.py \
  --baseline scripts/ci/baselines/bilingual-docs.txt \
  --format paths \
  --command "python3 scripts/check_bilingual_docs_full.py"
```

Exit `0` means the failure set matches the baseline exactly. Exit `1` means a
regression or a stale baseline; the offending items are printed as
`::error::` annotations.

## 5. Known sharp edges

* **No `rust-toolchain.toml` and no `rustfmt.toml`.** The `rust` job uses
  `dtolnay/rust-toolchain@stable`, so a rustfmt release that changes formatting
  can turn `cargo fmt --all --check` red without any code change. This is
  recorded rather than hidden: formatting drift on `main` is itself a recurring
  regression in GAP-10, so the job is a hard gate. Pinning the toolchain would
  remove the sharp edge and is the obvious next step.
* **`cargo clippy` needs a C toolchain** for `libsqlite3-sys`. It builds on the
  hosted runner; a local Windows host without `cc1` cannot run it.
* **`check_bilingual_docs_full.py` reads the working tree**, not `git ls-files`.
  Untracked build output can change its answer locally. CI checks out clean, so
  the CI answer is reproducible; a local answer may not be.

## 6. Evidence

Recorded on `6de4e38c` (the commit this work is based on):

| Gate | Result |
|---|---|
| `check_protocol_index.py` | exit 0 — `missing=0 extra=0 duplicate_types=0 invalid_rows=0`, `PASS` |
| conformance with both dependency sets | exit 0 — `Ran 585 tests`, `OK (skipped=27)` |
| `test_nonempty_audit.py` | exit 1 — 5506 unregistered constraints (GAP-09) |
| `check_bilingual_docs_full.py` | exit 1 — 81 uncovered paths (GAP-08) |
| `cargo fmt --all --check` | exit 0 |
| `cargo clippy --workspace --all-targets -- -D warnings` | exit 0 |
| `cargo test --workspace` | exit 0 |
| `gate_ratchet.py` on both baselines | exit 0 — `regressions=0 fixed=0` |

This is local execution of the commands the workflow runs. It is not a green
check run. See §1.
