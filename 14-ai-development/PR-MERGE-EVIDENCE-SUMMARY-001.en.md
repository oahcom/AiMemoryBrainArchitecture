# PR Merge Evidence Summary (PR-MERGE-EVIDENCE-SUMMARY-001)

- Baseline snapshot: `main@6b5db2918cffc2281deb22fd9858a37dbaeec726`
- Recorded: 2026-11-18
- Scope: Phase 1 Domain Model / Rust Workspace / SQLite Storage PRs, plus currently open governance and SQLite validation PRs.
- This document is an evidence index, not a substitute for PR review, Owner decisions, or platform branch-protection controls. Merge state follows GitHub PR metadata. CI evidence must match the PR's exact Head SHA. Closed/unmerged PRs have merge SHA N/A and are not counted as integrated.
- This documentation change is submitted from a separate branch; it does not directly modify `main`.

## 1. Executive summary

| Area | State | Supported conclusion | Explicit non-claim |
|---|---|---|---|
| Phase 1 canonical Domain Model | DECIDED (bounded scope) | #189 established the normative baseline; #193/#194 corrected it and reaffirmed Claim identity across Memory Versions as OPEN | Not every domain policy is decided |
| Rust Phase 1 Workspace gate | DECIDED (executable gate) | Exact-head Workspace CI passed on #221, #234, and #240; the gate covers `crates/**` | Not production runtime/deployment acceptance |
| SQLite idempotency identity binding | DECIDED (tested boundary) | #234 exact-head Workspace CI passed; replay identity is bound to Memory | Not all cross-process/distributed idempotency semantics |
| SQLite scope-filtered pagination | DECIDED (tested boundary) | #241 exact-head Workspace CI passed; pagination limits apply to authorized visible records | Not a complete authorization model |
| SQLite WAL/FULL + reopen/process-exit rollback | DECIDED (local file-backed test boundary) | #242 exact-head tests verify close/reopen persistence and rollback of an uncommitted transaction in a terminated child process | No proof of power loss, kernel crash, media corruption, backup/restore, or production topology |
| SQLite independent-connection CAS/idempotency race | DECIDED (same-process independent-connection boundary) | #243 exact-head Workspace CI passed; competing writes and identical-key replay across two independent connections are covered | No cross-process linearizability or distributed coordination proof |
| Additional SQLite rollback/locking/savepoint tests | CANDIDATE / pending validation | #249 test implementation is submitted and the bilingual gate passed | Rust Workspace run was still in progress at capture time |
| PR governance / branch protection | OPEN | #248 proposal passed the bilingual structural gate | Platform-level protection, required-check enforcement, and a negative blocking test for #134 remain outstanding |
| Phase 3.7 D/E/I/Storage publication protocol | OPEN | Issue #25 retains unresolved Owner decisions, real implementation, and production evidence gaps | Phase 1 SQLite tests do not establish a production Forget/Publication closure |

## 2. PR-by-PR evidence

### 2.1 Domain Model and Rust Workspace

| PR | Goal / scope | Exact Head / gates | Merge commit SHA | Decision relation and disposition |
|---|---|---|---|---|
| [#189](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/189) | Freeze the Phase 1 Domain Model contract: canonical objects, identity, time, scope, etc. | Head `42368891ed21f5c7e47867475ee620054b774637`; Bilingual runs `44247363131`, `44253844020`, `44254167924` all FAILURE | `f9f4e7975de58c60b724d5fcb9a72ae76f81e52b` | Merged, but the current normative interpretation must include corrections in #193/#194; do not describe #189's failed gate as passing |
| [#190](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/190) | Duplicate Domain Model freeze; incorrectly marked Claim identity across Memory Versions DECIDED | Head `ddad9d5333fbb4c2ba21318ea075582171cd62ee`; Bilingual `44254039968` SUCCESS (also failure `44252052239`) | N/A (closed, unmerged) | Superseded by #189 and later #193/#194; retained as historical evidence. Its Claim identity conclusion is not authoritative |
| [#193](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/193) | Correct the Domain Model and keep Claim identity across Memory Versions OPEN | Head `b6dcb5c432398b1f413adbec777ee6dd4ea954cd`; Bilingual `44254205801` SUCCESS | `a9f6d9431ef1f4918b025a23a69463008e92b3c2` | Supports the current normative state: Claim identity across Memory Versions = OPEN |
| [#194](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/194) | Reaffirm Claim identity as OPEN and correct the normative source | Head `2ca3de62a6b31a60304385982ecdca28bec5c33e`; Bilingual `44254223209` SUCCESS | `87a2199a0b6f89c14858f475e10e86cb7d6a452f` | Supports keeping Claim identity OPEN; this was a documentation gate, not a Rust test |
| [#191](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/191) | Rust Workspace skeleton, pure domain crate, and DM-01..DM-10 unit tests | Head `a6c44b35ca8f326ddd52825cd5283b8b00380ab0`; Bilingual `44254025064` SUCCESS; no applicable Rust CI existed at merge time | `2bedbcf8c0cdf4a4ff434049c973389c526a75ad` | Implements the Phase 1 pure domain layer; does not decide Claim identity and contains no Storage/SQLite |
| [#217](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/217) | Enable Rust Workspace CI and add the SQLite serde dependency | Head `7db2d3c4d27f043c02cda8f46b0beea42912e0fd`; Rust `44255133793` FAILURE; Bilingual `44255133773` SUCCESS | `5447db7d0316e1725e0288cfad081cd7db74fe6c` | Gate-enablement change; its own Rust failure is not a passing test record. #221 subsequently repaired the integration |
| [#219](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/219) | Duplicate Workspace CI / SQLite serde change | No separate admissible exact-head acceptance record found | N/A (closed, superseded) | Superseded by merged #217; not independent implementation or decision evidence |
| [#221](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/221) | Fix Event Store ScopeRef fixture and ensure Rust CI covers Workspace crates | Head `7f546bf2c9414788a168089d248438f5e0e057b0`; Rust `44255671837` SUCCESS; Bilingual `44255671757` SUCCESS | `7b8eef64390ed31cb92bdf7b29c98623d79a31fe` | Establishes an executable Workspace gate; recorded at the time as 21 tests passed / 0 failed |
| [#222](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/222) | Attempted Event Store fixture, SQLite serde dependency, and Workspace workflow-trigger repairs | Head `d3ade61f1d015e5c63ad1985d8a19753edf82acf`; no CI run found for this exact Head | N/A (closed, superseded) | Replaced by the consolidated #221 repair; no claim that this PR itself passed |
| [#224](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/224) | Attempted ScopeRef fixture and Rust workflow repair | Head `092e708a1b9f8db501eabd41cdf062e11e3ae675`; no CI run found for this exact Head | N/A (closed, superseded) | Replaced by #221; its duplicate workflow was not retained |
| [#225](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/225) | Align serde derives and SQLite/Event Store ScopeRef fixtures | Final PR Head `17c6ca786a08b31103b4f0b7fcd07a38902fd573`; intermediate Head `604e843432c5aa0dffef142af67cc948d8027db5` had Rust run `44255722412` FAILURE; do not attribute that failure to the final Head or claim the final Head passed | N/A (closed, superseded) | Replaced by #221 and later integration repairs; stale branch was not merged |
| [#234](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/234) | Fix SQLite idempotency replay not being bound to Memory identity | Head `c4c02d0dcb44dc1089e8ebed61a211520992c9ea`; Rust `44256767166` SUCCESS; Bilingual `44256767193` SUCCESS | `e68a5d66f11383c5252a00bc9547073ff9f911d7` | Supports the tested implementation boundary for Memory-identity-bound idempotency replay |
| [#240](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/240) | Restore serde serialization derives on canonical domain/storage records; minimal two-file repair | Head `d5c7c41298118182a295d39fee3223beebfb5f77`; Rust Workspace `44258489811` SUCCESS; Bilingual `44258489883` SUCCESS | `715878ef3f5ce1331bc9caf771dd20481da1145e` | Supports Workspace + SQLite serialization compile/test integration; does not prove production durability or crash recovery |

### 2.2 SQLite Storage verification

| PR | Goal / scope | Exact Head / gates | Merge commit SHA | Decision relation and disposition |
|---|---|---|---|---|
| [#241](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/241) | Fix change-record pagination after scope filtering: count authorized visible records and advance the cursor correctly | Head `fa8de8442ae9ff4311f2c0f42cfa4983df1737c1`; Rust `44258500677` SUCCESS; Bilingual `44258500686` SUCCESS | `6691bfba44cbebce6c4d3556e1c1cf9bbb3b16c8` | Supports the local implementation claim for scope-filtered visible pagination |
| [#242](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/242) | File-backed SQLite WAL, synchronous=FULL, foreign_keys, busy timeout; close/reopen persistence and child-process uncommitted-transaction rollback tests | Head `92d4910057a6f5b48e627a393b7bc7005bb73b20`; Rust `44258883510` SUCCESS; Bilingual `44258883432` SUCCESS | `aa711289785395d2efa202e34def64c393ee0ac7` | Supports file-backed reopen persistence and rollback on process termination; explicitly does not prove power-loss/kernel-crash/media-corruption/restore behavior |
| [#244](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/244) | CAS test for competing first commits through two independent SQLite connections | Head `09ab26963293ee460237c6f27c5b95ed3b401730`; Rust `44259233587` SUCCESS; Bilingual `44259233358` SUCCESS | N/A (closed, superseded) | Had its own exact-head passing evidence, but was superseded by the enhanced merged #243; not evidence of code merged from #244 |
| [#243](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/243) | Consolidate independent-connection CAS race and concurrent identical-idempotency-key replay tests | Head `179059a5be1973e2e188fd648ee57d1db7b004fe`; Rust Workspace `44259219033` SUCCESS; Bilingual `44259218907` SUCCESS | `4a3e06fd263e9dbd1056179dceb3cb21b17e330f` | Supports bounded same-process independent-connection competing-write correctness; not cross-process linearizability or distributed coordination |

### 2.3 Currently open PRs

| PR | Goal / scope | Exact Head / gate snapshot | Merge commit SHA | Current state / decision |
|---|---|---|---|---|
| [#248](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/248) | Bilingual PR-GOVERNANCE-001 enforcement addendum: exact-head CI, independent approval, prompt/evidence traceability, Issue #130/#134 runbooks | Head `b887e9518977dca985776bf8715de9cd7597beb2`; Bilingual `44264271033` SUCCESS; Rust not applicable | N/A (OPEN) | Governance proposal; CANDIDATE. GitHub platform branch protection and negative enforcement test for #134 remain OPEN |
| [#249](https://github.com/oahcom/AiMemoryBrainArchitecture/pull/249) | SQLite SAVEPOINT rollback, busy-timeout/retry, injected commit failure, panic/unwind rollback tests | Head `be1eb17334864b1d74aa70612a09033f09b40d36`; Bilingual `44264275487` SUCCESS; Rust Workspace `44264277063` FAILURE (job `134664822288`; 14 passed / 1 failed; `file_db_busy_timeout_bounds_wait_for_long_immediate_transaction` referenced a nonexistent `updated_at` column) | N/A (OPEN) | CANDIDATE / TO_VALIDATE; do not accept before the exact-head Rust result completes |

## 3. State classification and evidence boundaries

### DECIDED (only the specific propositions supported by evidence)

1. The bounded Phase 1 canonical Domain Model was integrated through #189 and corrected by #193/#194. Claim identity across Memory Versions explicitly remains OPEN. Evidence: #189 merge `f9f4e7975de58c60b724d5fcb9a72ae76f81e52b`; correction merge #193 `a9f6d9431ef1f4918b025a23a69463008e92b3c2` / run `44254205801`; #194 `87a2199a0b6f89c14858f475e10e86cb7d6a452f` / run `44254223209`.
2. The Rust Workspace test gate is executable and has passed on exact Heads. Evidence: #221 merge `7b8eef64390ed31cb92bdf7b29c98623d79a31fe` / run `44255671837`; #240 merge `715878ef3f5ce1331bc9caf771dd20481da1145e` / run `44258489811`.
3. SQLite idempotency identity binding, scope-filtered pagination, WAL/FULL reopen/process-exit rollback, and same-process independent-connection CAS race are DECIDED only within their respective tested boundaries. Evidence: #234 run `44256767166`, #241 run `44258500677`, #242 run `44258883510`, and #243 run `44259219033`; exact Heads and merge SHAs are in the tables above.

### CANDIDATE

- PR #248 governance enforcement addendum: bilingual gate passed, but the PR is not merged and cannot substitute for GitHub platform configuration.
- PR #249 SQLite rollback/locking/savepoint tests: implementation is submitted; the exact-head Rust result is still pending.
- WAL/FULL may be treated as the current adapter configuration, not as a final production durability policy.

### OPEN

- Claim identity across Memory Versions.
- Issue #25 D/E/I/Storage exact-owner decisions, real publication participants/sequencer, production authorization, crash/failover/restore, and production evidence.
- Issue #134 main branch protection / required-check enforcement, independent approval, and negative test proving a failing gate blocks merge.
- Issue #130 complete prompt/session traceability audit.

### TO_VALIDATE

- Cross-process linearizability and cross-host/distributed concurrency or coordination.
- Power loss, kernel crash, write-cache behavior, media corruption, backup/restore, and real production deployment topology.
- SQLite connection-pool lifecycle and abnormal pooled-connection reclamation; #249 explicitly has no connection-pool abstraction.
- A complete Scope/Permission algebra and integration with a production authorization service.

## 4. Merge discipline

- Only CI for the exact PR Head SHA is admissible as that PR's gate evidence. A run on an older Head, a similarly named workflow, or a later unrelated commit is not a substitute.
- Closed but unmerged PRs (#190, #222, #224, #225, #244) must retain merge SHA N/A and be labelled superseded/failed/closed; they must not be counted as merged into main.
- CANDIDATE → DECIDED requires both an implementation Commit SHA and an exact-head CI Run ID, with the conclusion bounded to what the test actually establishes.
- The bilingual gate proves documentation structure/manifest checks only; it does not replace semantic review, Rust tests, or production evidence.
- This record is pinned to the observed `main@6b5db2918cffc2281deb22fd9858a37dbaeec726`. When main advances, update this record incrementally from a new snapshot without overwriting historical evidence.
