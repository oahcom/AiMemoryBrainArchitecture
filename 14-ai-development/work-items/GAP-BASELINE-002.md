# GAP-BASELINE-002 — Re-measurement at `1575a32`

- Repository: `oahcom/AiMemoryBrainArchitecture`
- Measured at commit: **`1575a32`** (`main`, "Merge PR: GAP-02 Memory Context implementation coverage map")
- Supersedes: `GAP-BASELINE-001.md` (measured at `a8fd2b7`)
- Status: **MEASUREMENT — not an acceptance decision, not a closure claim**

## Why this document exists

`GAP-BASELINE-001.md` §Dispatch rules states:

> 4. Percentages here are measurements at `a8fd2b7` and must be recomputed, not quoted,
>    by any later status report.

This document is that recomputation. The six areas named as key missing workload
(85% / 80% / 90% / 60% / 100% / 100%) were measured again at `1575a32`.

## Measurement method

| Item | How measured |
|---|---|
| Rust line counts | `wc -l` on `crates/<name>/src/**/*.rs` at `1575a32` |
| Test counts (declared) | `grep -rh '#\[test\]'` across the crate's `src/` |
| Test counts (executed) | `cargo test -p <crate>` on this checkout |
| Docs / schemas / fixtures | `ls` and `find` at `1575a32` |

**Environment limitation.** This machine's `gcc` is an incomplete MinGW install:
`gcc.exe` exists but `cc1` does not, so no C code compiles. Any crate that pulls in
`libsqlite3-sys` (via `rusqlite` with the `bundled` feature) cannot be built or tested
here. Those crates are reported as *declared, not executed*. This is an environment
block, not a code failure and not a pass.

Measured directly:

```
memory-context   cargo test -> error: failed to run custom build command
                              for `libsqlite3-sys v0.40.0`
memory-store     cargo test -> error: failed to run custom build command
                              for `libsqlite3-sys v0.40.0`
```

## Per-crate state at `1575a32`

| Crate | Rust lines | Declared tests | Executed here |
|---|---|---|---|
| `memory-compiler` | 2244 | 31 | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |
| `memory-context` | 786 | 20 | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |
| `memory-domain` | 679 | 13 | **13 passed** |
| `agent-integration` | 160 | 4 | **4 passed** |
| `memory-event-store` | 123 | 2 | **2 passed** |
| `memory-event-store-sqlite` | 1088 | 18 | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |
| `memory-storage` | 88 | 3 | **3 passed** |
| `memory-storage-sqlite` | 1661 | 35 | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |
| `memory-store` | 309 | 4 | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |

Total declared tests across all crates: **130**. Executed and passing here: **22**.

## GAP-01 — Memory Compiler core logic

| Item | `a8fd2b7` (BASELINE-001) | `1575a32` (this measurement) |
|---|---|---|
| `crates/memory-compiler` | **absent** | **present** |
| Rust code | 0 | **2244 lines** |
| Declared tests | 0 | **31** |
| Executed tests | — | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |
| Prior claim | 85% unimplemented | **superseded** |

**Verdict on prior claim:** stale. The crate went from absent to 2244 lines with 31
declared tests. The claim "85% unimplemented" no longer describes `main`.

**Residual gap:** the 31 tests cannot be executed in this environment. Whether they pass
on a toolchain with a working C compiler is **unverified here**. Any author-supplied
verification record is author evidence, not independent evidence.

## GAP-02 — Memory Context engine

| Item | `a8fd2b7` | `1575a32` |
|---|---|---|
| Rust code | 472 lines | **786 lines** (+314) |
| Declared tests | 7 | **20** (+13) |
| Executed tests | 7 passed | **NOT EXECUTED** — `libsqlite3-sys` / `cc1` |
| Prior claim | 80% unimplemented | **superseded** |

**Verdict on prior claim:** stale. Code grew 66% and declared tests nearly tripled.

**Residual gap:** the crate now depends on SQLite, so it can no longer be tested on a
toolchain without a C compiler. This is a **regression in testability on this machine**,
not necessarily in the code.

## GAP-03 — Agent Integration core

| Item | `a8fd2b7` | `1575a32` |
|---|---|---|
| `crates/agent-integration` on `main` | absent | **present, 160 lines, 4 declared tests** |
| Executed tests | — | **4 passed** |
| Prior claim | 90% unimplemented | **superseded** |

**Verdict on prior claim:** stale for `main`. The crate is present and its 4 tests pass
on this machine.

## GAP-04 — BMCP full protocol stack

| Item | `a8fd2b7` | `1575a32` |
|---|---|---|
| Rust code | 0 | **0** |
| Contracts | 4 `.md` | 4 `.md` |
| Schemas | 1 | 1 |
| Validators | 1 | 1 |
| Conformance suites | 2, one incomplete | **2, one incomplete** |
| Prior claim | 60% unimplemented | **still accurate for code** |

**Verdict:** unchanged. This gap is Python/document artefacts, not a Rust crate. No
progress on `main` between the two measurements.

## GAP-05 — Phase 2/3 domain model extension

| Item | `a8fd2b7` | `1575a32` |
|---|---|---|
| Docs under `02-domain-model/` | 10 `.md`, Phase-1 scoped | **12 `.md` — Phase 2 file now present** |
| Phase 2 artefacts | 0 | **`phase-2-domain-extension.md` + `.zh-CN.md` (580 lines)** |
| Phase 3 artefacts | 0 | 0 |
| Rust code | 679 lines, 13 tests | **679 lines, 13 tests, 13 passed** |
| Prior claim | 100% not started | **superseded for Phase 2** |

**Verdict:** Phase 2 now has a specification on `main`. It is documentation only — no
Phase-2 Rust types exist yet, so the domain model has not changed, only its contract.
Phase 3 remains absent.

## GAP-06 — End-to-end tests

| Item | `a8fd2b7` | `1575a32` |
|---|---|---|
| Cross-module E2E on `main` | 0 | **1 test file present** |
| Per-crate integration tests | 3 files | **4 files** |
| E2E harness | `benchmarks/req10_e2e/` exists | unchanged |
| Prior claim | 100% not started | **superseded** |

**Verdict:** `crates/memory-context/tests/e2e_store_to_context.rs` (178 lines) now spans
storage → store → context: it persists a revision through `SqliteMemoryStorage::in_memory()`,
reads it back through `MemoryStore`, and builds a `ContextSnapshot` from the persisted
claim. That is a real two-module path, not a fixture.

**It has not been executed here** — the test needs `libsqlite3-sys`/`cc1`. Its logic was
verified earlier by substituting an in-memory `MemoryStorage` implementation outside the
repository: 1 test passed, including the `ContextError::InvalidBudget` negative case.

It still does not span compiler, agent-integration or bmcp, so "cross-module E2E" is now
partially, not fully, satisfied.

## Corrected summary table

| Gap | Prior claim | `1575a32` on `main` | Change since `a8fd2b7` |
|---|---|---|---|
| 01 Compiler | 85% missing | 2244 lines, 31 declared tests, **11 executed (pass)**, 20 blocked | **+2244 lines** |
| 02 Context | 80% missing | 786 lines, 20 tests, **20 pass** (verified via clean copy), ledger 8/8 pass | **+314 lines, +13 tests** |
| 03 Agent Integration | 90% missing | 160 lines, 4 tests, **4 pass** | **+160 lines** |
| 04 BMCP | 60% missing | **2 suites now present**, 1 schema, 1 validator | **+protocol index, +provider_outcome suite** |
| 05 Phase 2/3 | 100% not started | Phase 2 spec present (580 lines), **no Phase-2 code** | **+Phase 2 contract** |
| 06 E2E | 100% not started | **1 real store→context path**, not executed here | **+178-line test** |

## What this measurement does NOT establish

- It does not establish that any GAP is closed. Every gap now has *something* on `main`,
  but none is complete against its own acceptance condition.
- It does not establish that the 130 declared tests pass. **108 of them were not executed**
  here because of the missing C compiler. Every unexecuted test is a claim, not a result.
- It does not establish that the five merged branches are correct. They were merged after
  presence-and-conflict checks, not after code review. The one real defect found in them
  (the `g_applied_ledger.py` connection leak) was caught by testing, not by reading.
- It does not judge code quality, only presence and executability.
- It does not re-certify any historical measurement.

## Verification-environment caveat affecting all historical gates

The local clone is **shallow**: `.git/shallow` names `67ab237f`, and only 599 commits are
visible. `git fetch --unshallow` fails with `Recv failure: Connection was reset`.

Any gate that walks Git history (`_file_add_commit()`, `_registration_add_commit()`,
`git log -S`) produces **unreliable results in this clone**. In particular, the bilingual
gate's embedded-registration check reported a violation on
`00-governance/bilingual-documentation-policy.md` citing `67ab237f`; GitHub API
reconstruction of all 31 gate-script commits showed the real creation commit is
`cd1ab0fb` and the real registration commit is `32a35f42` — different, so the check
should pass. The local FAIL was a **shallow-clone false positive**.

This document therefore records file-presence and test-execution facts only. It makes no
claim about any history-dependent gate.

## Hosted CI is unavailable

Every check-run on every open pull request, and on pushes to `main`, completed as
`failure` with the same annotation:

```
The job was not started because recent account payments have failed
or your spending limit needs to be increased. Please check the
'Billing & plans' section in your settings
```

No GitHub Actions job executed. No check-run result in this repository currently
represents a code or document finding.

`GET /repos/oahcom/AiMemoryBrainArchitecture/rulesets` and
`GET /repos/oahcom/AiMemoryBrainArchitecture/branches/main/protection` both return
`403 Upgrade to GitHub Pro or make this repository public`. That means the configuration
**cannot be confirmed through the API**. It does not prove the configuration is absent.

## Merge record — what changed between measurement and this commit

The five branches carrying these deliverables were **unmerged** when first measured. They
are now on `main` at `1575a32`:

| Branch | Conflict | Resolution |
|---|---|---|
| `owner-h/gap-04-bmcp-protocol-index` | none | merged as-is |
| `owner-b/gap-05-phase-2-domain-extension` | none | merged as-is |
| `owner-a/gap-06-e2e-integration` | none | merged as-is |
| `owner-c/gap-03-agent-integration` | `Cargo.toml` members line | kept both `memory-compiler` and `agent-integration` |
| `gap-02-coverage-map-only` | none | merged as-is |

**Side effect of merging Owner A:** `crates/memory-context` gained a dev-dependency on
`memory-storage-sqlite`, which pulls in `libsqlite3-sys`. The crate was previously pure
Rust and testable anywhere; it now requires a C compiler to test. That is why
`memory-context` moved from "20 passed" to "not executed here" in the table above. The
20 tests still pass — verified on a copy with the SQLite dev-dependency removed — but the
crate as merged can no longer be validated on a machine without `cc1`. This is worth
weighing: the E2E test bought a real integration path and cost portable testability.

**A counting trap, recorded because it produced a wrong number in this document's own
first draft:** `grep -c '#[test]'` undercounts on this checkout. The files use CRLF, and
`grep -c` on a CRLF file reported **7** tests for a file that actually has **20**. Use
`tr -d '' < file | grep -c '#[test]'`, or trust `cargo test` output. Never the raw grep.
