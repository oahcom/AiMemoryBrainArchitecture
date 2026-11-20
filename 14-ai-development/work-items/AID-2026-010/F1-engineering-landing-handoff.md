# F-43-01/F1 — Engineering-Phase Implementation Landing Handoff
# F-43-01/F1 — 工程阶段实现落地交接

- Work Item: `AID-2026-010`
- Finding: `F-43-01/F1`
- Severity: `P1`
- Disposition: `DEFERRED_TO_ENGINEERING_PHASE` — operational implementation is **NOT VERIFIED / NOT COMPLETE**
- Return carriers: Issue #7 (engineering entry), Issue #10 (JF-10/COC physical evidence), Issue #25 (D/Storage authority and receipt boundary), Issue #43 (finding ledger)
- Owner authority: D Domain Owner owns D semantics and operational authority; project authority / engineering leadership owns engineering-entry designation and runtime carrier; A Integration performs evidence reconciliation only.
- This document is a handoff/checklist, not implementation, not an authorization to start implementation, and not production acceptance.

## 1. Purpose and non-goals

This handoff converts the F1 residual into an executable engineering-entry package. It prevents the accepted D-002 normative proof from being mistaken for a working D authority runtime.

It does not:
- create or imply a canonical Runtime repository;
- authorize code in this architecture-definition repository or an unapproved repository;
- replace D Owner decisions, appoint engineering owners, or choose a persistence engine/topology;
- treat mocks, fixtures, TEST callbacks, static values, reference models, or documentation as operational proof;
- authorize merge to `main`, deployment, production activation, or global Forget completion.

The controlling entry decision remains Issue #7 comment [#7021990583](https://github.com/oahcom/AiMemoryBrainArchitecture/issues/7#issuecomment-7021990583): `IMPLEMENTATION_BINDING=DEFERRED_TO_ENGINEERING_PHASE`; engineering-phase entry is NOT AUTHORIZED / NOT READY. Owner ruling D-2026-1120-01 removes the former carrier quota freeze only; it does not supersede this engineering-entry decision.

## 2. Exact normative inputs

| Input | Exact identity | Evidentiary meaning |
|---|---|---|
| D-002 accepted proof pack | Blob `4c8672a68e4339e40b5d8cb98eb073af8c98c1a5` | Normative proof semantics accepted; not runtime evidence |
| D contract 1.3.1 | Blob `12b71e770f4e977c7f147694a644066bc2ce11b9` | Normative D contract |
| D authoritative query contract 1.0 | Blob `781e2e4306577448202ad84c987cbb2a0e5624f3` on PR #321 Head `3db969c04d08ec4b0d9aadd8f8efcea3ac0309b6` | Normative read-only query interface; endpoint explicitly NOT ESTABLISHED AS CALLABLE |
| D/H accepted mapping | Blob `004fc0261b447771e73a0f8cfdd34ec1f8b33e49` | Same-Blob D/H normative mapping acceptance; does not prove runtime implementation |
| Engineering entry ruling | Issue #7 comment #7021990583 | Explicit no-entry / defer disposition |

The D query contract itself states that no endpoint, transport, signing key, receipt instance, ledger proof, test, or Runtime implementation is thereby asserted to exist.

## 3. Entry package — required before implementation begins

All fields below must be evidenced in existing governance carriers before implementation work is treated as authorized.

| Gate | Required fact | Evidence required | Accountable supplier |
|---|---|---|---|
| E1 | Canonical Runtime repository and active branch | Repository URL, branch, exact HEAD, repository purpose and authority record | Project authority |
| E2 | Engineering responsibility | Named engineering lead and maintainers for D Runtime, Producer Registration Ledger, ForgetFence, Storage integration and CI | Engineering leadership |
| E3 | Write and custody authority | Explicit authorization for D Owner / implementers to write the designated repository and paths; maintainer permissions | Project authority + repository administrator |
| E4 | Persistence and serialization boundary | Authoritative Producer Registration Ledger/store, transaction domain, durability/WAL boundary, linearization point, recovery owner | D Owner + Storage Owner + engineering lead |
| E5 | Callable authority surface | Exact five D operational operations from the accepted D-002 proof pack, with request/response types, auth principal, error/UNKNOWN semantics and operation ownership | D Owner |
| E6 | Build and verification custody | Reproducible toolchain, build commands, test commands, CI workflow, artifact/build SHA source and log retention | Engineering leadership |
| E7 | Deployment and trust boundary | Service topology, principal/key registry, rotation/revocation, network/transport, replicas, backup/restore and operator boundary | Engineering leadership + D/Storage Owners |
| E8 | Traceability | Contract-to-code map from D-002 and D 1.3.1 clauses to implementation paths, tests, fault hooks and operational evidence | D Owner + engineering lead |

**Entry rule:** E1–E8 are conjunctive. Missing or inferred fields remain NOT ESTABLISHED. A repository search result, generic adapter, SQLite reference model, schema-only validator, or role-simulated approval cannot satisfy these gates.

## 4. Operational implementation deliverables

After E1–E8 are evidenced and implementation entry is authorized, the engineering work must produce all of the following in the designated runtime repository:

1. The five callable D authority operations enumerated verbatim from the accepted D-002 proof pack, each backed by the designated authoritative persistence boundary. No operation may be replaced by a fixture, callback returning a constant, or caller-supplied assertion.
2. Producer Registration Ledger and ForgetFence state with durable identity, namespace, sequence/generation, transaction and recovery semantics.
3. A real immutable authoritative Receipt with stable reference and content digest, persisted and independently readable after process restart.
4. Exact equality proof for the D-002 typed values, bound to the same operation, fence and snapshot identity; no cross-type comparison or inferred equality.
5. Linearization proof identifying the exact durable commit point and showing the behavior of concurrent producer admission, Forget fence installation, snapshot capture and visibility.
6. Fail-closed handling for missing, stale, contradictory, unauthenticated, revoked, unavailable or UNKNOWN evidence. UNKNOWN must not be converted to success, abort or terminality.
7. Reproducible build/test evidence pinned to the exact commit, with CI Run IDs, complete logs and artifact SHA values.

The five operation names and signatures MUST be copied from the exact accepted D-002 source at implementation entry. This handoff intentionally does not guess or rename them.

## 5. Ten-scenario operational evidence matrix

The ten scenarios are a required evidence set, not ten documentation checkboxes. At implementation entry, copy the canonical scenario IDs and exact expected outcomes from the accepted D-002 proof pack into this matrix. Preserve one-to-one mapping; do not invent substitute scenarios or collapse distinct races.

| Slot | Canonical D-002 scenario ID/title | Fault/race injection and ordering | Durable Receipt/Ledger observation | Expected terminal/UNKNOWN result | Exact test/report/CI evidence |
|---|---|---|---|---|---|
| S01 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S02 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S03 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S04 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S05 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S06 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S07 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S08 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S09 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| S10 | NOT RUN — populate from D-002 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

For every scenario, retain: exact runtime commit; exact test path and test ID; command and environment; injected ordering/fault; raw stdout/stderr or immutable CI log; durable before/after ledger and receipt readback; expected/actual result; CI Run ID; artifact digest. A summary count without the underlying evidence is insufficient.

## 6. Current evidence inventory — do not overstate

| Required proof | Current evidence | Current state |
|---|---|---|
| D-002 normative semantics | Accepted proof Blob `4c8672a68e4339e40b5d8cb98eb073af8c98c1a5` | ACCEPTED at normative level |
| Five operational D authority operations | Prior exact-source status records say NOT IMPLEMENTED | NOT VERIFIED / NOT IMPLEMENTED |
| Authoritative Producer Registration Ledger runtime | No authorized canonical runtime/persistence carrier evidenced | NOT ESTABLISHED |
| Real durable Receipt sample and readback | No real Receipt evidenced | NOT ESTABLISHED |
| Exact equality and linearization proof from running authority | No runtime trace or operational proof evidenced | NOT RUN |
| Ten operational scenarios | Prior exact-source status records say NOT RUN | NOT RUN |
| Reproducible exact-head runtime CI | No authorized runtime target/build custody evidenced | NOT ESTABLISHED |

No code tests are claimed by this handoff. No CI Run ID is claimed. This is a status-accurate engineering handoff, not an implementation PASS.

## 7. Closure rule and evidence return

F1 may move from DEFERRED/BLOCKED to implementation-verifiable only after:
- E1–E8 are recorded and implementation entry is authorized;
- all five D authority operations are implemented in the authorized runtime repository;
- a real durable Receipt and authoritative Ledger readback are attached;
- exact equality and linearization are demonstrated from the running authority;
- all ten D-002 scenarios have reproducible evidence;
- exact-head build/tests and CI are available;
- A Integration performs exact-source reconciliation without substituting for D Owner or engineering acceptance.

Return results to:
- Issue #7: E1–E8 engineering-entry package and authorization;
- Issue #10: JF-10/COC physical transaction and recovery evidence;
- Issue #25: D/Storage authoritative persistence, query, receipt and currentness evidence;
- Issue #43: F-43-01/F1 finding ledger and integration disposition.

## 8. Prompt and document provenance

- Owner ruling: D-2026-1120-01, supplied by the user in the current continuation chat (T2 instruction).
- Source conversation lineage: the continuation of the user's F1/F3 workstream; immutable platform conversation UUID/permalink and raw message bytes are not exposed to this execution context. Prompt SHA-256: `NOT_VERIFIED`; no digest is fabricated.
- Repository execution rules read from main: AI-EXEC-001 v1.1, Blob `58af59af266b81109269156ea667df1a15edfb7b`; AI-EXEC-002 v1.2, Blob `7f5928a5d16eb12da7621cfb8bd99ca463afd859`. AI-EXEC-002 v1.2 is PENDING ADOPTION; v1.1 remains the adopted predecessor.
- Normative sources are pinned in §2. Git Blob identifiers are not represented as file SHA-256.

---

# English operational summary

F-43-01/F1 is delivered here as an engineering-phase landing handoff with explicit entry gates, deliverables, ten-scenario evidence slots, closure rules and return destinations. It does not claim or create runtime implementation. The controlling Issue #7 ruling still defers implementation entry. The purpose of this PR is to make the deferred work actionable and auditable without violating the architecture-repository boundary.
