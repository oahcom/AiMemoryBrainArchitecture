---
document_metadata:
  domain: architecture
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
      evidence_reference:
        - "00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
      revocation: null
    evidence_verification:
      verification_status: Unverified
      last_verified_date: null
      last_verification_note: "Exact-version source inventory and gap analysis only; no end-to-end conformance or Owner acceptance inferred."
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
    canonical_status: Canonical
    canonical_scope: "Exact-version A-I + Storage/Consistency end-to-end composition review"
    canonical_scope_id: "architecture/a-i-storage-e2e-composition-review"
    canonical_scope_keywords:
      - end-to-end
      - composition
      - storage-consistency
      - gate-a
    canonical_conflict_status: None
    canonical_conflict_resolution: null
    normative_status: Informative
  bilingual_counterpart:
    en: "docs/en/00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
    zh-CN: "docs/zh-CN/00-governance/implementation-evidence/2026-11-26-a-i-storage-e2e-composition-review.md"
---

# A-I + Storage/Consistency End-to-End Composition Review

- Work item: AID-2026-095
- ID status: PROVISIONAL; temporary numeric reservation; recheck main and renumber at merge time if occupied.
- Exact source baseline: main @ 81906cfc8d3cd477d26657520aa04d81466e7ce2
- Attribution: user-authorized operator (delegated by account owner), date 2026-11-26. Any proxy disposition is 代理登记，非自然人 Owner 签署. No new Owner acceptance is recorded.
- Purpose: falsifiable Gate A composition checklist, not implementation or production conformance.

## 1. Reading rules and verdicts

Only files present on the exact main baseline are pinned. NOT_FOUND_ON_MAIN is a negative tree finding. A mirror, reference model, schema, test, implementation file or work-record is not promoted into a normative Owner contract.

- VERIFIED_BY_DOCUMENT means the exact current-main document fully defines the proposition, has applicable authority/status and no unresolved cross-owner dependency. It is not a runtime test result.
- BLOCKED_WITH_REASON means incomplete, contradictory, candidate-only, unaccepted, missing normative source or missing evidence; identify exact missing item and provider.
- Each checkpoint is PASS, FAIL or NOT EVIDENCED. NOT EVIDENCED is not a Gate A pass. One missing required checkpoint keeps the flow blocked.
- All eight flows below are BLOCKED_WITH_REASON; no local clause promotes a whole flow to verified.
- No runtime, validator, schema, test, policy or Owner decision is changed.

## 2. Exact source inventory

Blob SHA values were read from the Git tree/content API at the exact baseline. Missing paths are explicit negative findings.

| Exact path | Blob SHA | Source class / limitation |
|---|---|---|
| 00-governance/implementation-evidence/2026-11-26-a-i-storage-acceptance-matrix.md | 9c802777e9bafc421c77f8f68fcb035cdee4167d | Canonical work-record; traceability only; embedded baseline is stale. |
| 04-memory-compiler/compiler-overview.md | 24c2fc69a8a69176071d46aac871ae16588702b7 | Canonical Normative Draft/Unverified; orchestration candidate and explicit exclusions. |
| 04-memory-compiler/phase-1-event-store-contract.md | 17b14591d76160a7c125903b41e7dae014c3c5df | DECIDED semantics / CANDIDATE seam; dispatcher, leases and production durability excluded. |
| 04-memory-compiler/README.md | 88f1a451830b4c7b455462edd6453543778793e4 | Canonical Informative reading guide. |
| 14-ai-development/work-items/D-OWNER-DECISION-PARTICIPANT-ADMISSION-001.md | 2cff53b2133e26115e2d3808ae9738092602c4d3 | Owner-proxy decision; participant_admitted remains false. |
| 14-ai-development/work-items/D-OWNER-DECISION-CANONICAL-COMMIT-001.md | 2fba6536e95e55e55617bfddefc26a11e269c5b5 | D decision; canonical store normative root absent. |
| 01-system-architecture/forget-fence-and-completion-contract.md | 760a1d48011f2a66c23abcf825a3d067e79b8821 | Canonical Draft/Unverified/Informative; global policy and cross-module execution open. |
| 06-memory-context/context-versioning.md | 57ea7e7298f79d769d6931b1d355c9d3b4f956d6 | G semantics; encoding/serialization candidate. |
| 06-memory-context/context-version-immutability-decision.md | 27e9e5f092b17cf4013a533d07949eb73ac6ef4c | Draft/Unverified/Informative; G acceptance pending. |
| 06-memory-context/phase-3.8.22-g-applied-persistence-idempotency-crash-restore-contract.md | 833815e37ac8d7505d93a0a115421dafe3eb08ad | G Normative Design Draft; implementation unverified; cross-owner acceptance required. |
| 07-agent-integration/applied-evidence-contract.md | 273efdd1b02bd9302fc968f07c6d094da2582a6e | Draft/Unverified/Informative; C/G/H acceptance pending. |
| 07-agent-integration/inference-boundary-model.md | e2d5cb6abd9ec40da6e3680531de5944fc8b14df | Candidate boundary model; no cross-owner freeze. |
| 08-bmcp-protocol/owner-snapshot-namespace-and-fence-currentness-contract.md | d83cde77e98db2e74cf6827d874b0babb4157304 | H candidate; must reconcile with E/G/Storage. |
| 08-bmcp-protocol/phase-3.8-h-rj-hw-01-typed-watermark-and-fence-binding-contract.md | e583ac2fb888aa5184eaa6525d9cc564f343785f | H phase contract; not F normative retrieval root. |
| 08-bmcp-protocol/phase-3.8.25-h-applied-delivery-evidence-hardening-addendum.md | afa294bc42a8488e4569e6a8bdf5437c7a90e247 | H addendum; shared consumer acceptance pending. |
| 08-bmcp-protocol/phase-3.8.26-h-applied-delivery-evidence-csubmitoutcome-join-addendum.md | 7b73491c765091728af6f5306b9efd502cf7f30a | H addendum; shared consumer acceptance pending. |
| 02-domain-model/phase-1-storage-trait-contract.md | 22ca7cd3777e0132e25f084084610f1e90b60d21 | Candidate seam; no backend selected; no backend atomicity/durability proof. |
| 02-domain-model/scope-and-permission-model.md | b5215ae27bd65a6c89c185b496f730b6cd52efa9 | Scope separation decided; policy and inheritance edge cases open. |
| 14-ai-development/adr/OWNER-DECISION-AUTHORIZATION-TYPE-STATE-001.md | 8ad9bbfa4906a6f9c30a437fd144c6c62c37577d | Proxy decision; does not establish I issuance authenticity. |
| 14-ai-development/adr/OWNER-RULING-AUTHORIZATION-PRESENCE-GATE-025.md | 75e338aa0dbe0161fbc890977c5f4a8234a8c815 | Proxy ruling; presence gate is not authorization authenticity. |
| crates/memory-event-store-sqlite/src/lib.rs | c68e036e5f8deb7968babc6703a4cf9341d5db40 | Implementation evidence only. |
| crates/memory-storage-sqlite/src/lib.rs | b7eecd3ec0ec4c3ef3c27bc43fe24c29c91fb11f | Implementation evidence only. |
| crates/memory-event-store-sqlite/src/forget_fence.rs | 5b71a25b8be24fd0f1d9cf9e22582705d646cf64 | Implementation evidence only. |
| 06-memory-context/reference-model/g_applied_ledger.py | be24fea19ee72a1fc01350b79d5359e7820848b9 | Reference model only. |
| 08-bmcp-protocol/schemas/bmcp.applied-delivery-evidence-1.0.0.schema.json | 0700f2077052bd153f9baa86850d9aab89491016 | Schema presence is not end-to-end acceptance. |
| 09-security-governance/README.md | NOT_FOUND_ON_MAIN | IMPL2/I restore or disposition; I accepts policy. |
| 03-memory-brain/canonical-memory-store.md | NOT_FOUND_ON_MAIN | IMPL2/D restore or disposition; D accepts canonical semantics. |
| 05-memory-runtime/README.md | NOT_FOUND_ON_MAIN | IMPL2/F restore or disposition; F accepts retrieval semantics. |
| 04-memory-compiler/accepted-receipt-and-idempotency-contract.md | NOT_FOUND_ON_MAIN | IMPL2/E restore or disposition; E supplies receipt contract. |
| 04-memory-compiler/compiler-state-and-producer-admission.md | NOT_FOUND_ON_MAIN | IMPL2/E restore or disposition; E supplies admission contract. |

### Missing current-main normative roots

| Expected path | Result | Required provider |
|---|---|---|
| 03-memory-brain/canonical-memory-store.md | NOT_FOUND_ON_MAIN | IMPL2/D restore or formally disposition; D accepts canonical semantics. |
| 05-memory-runtime/README.md | NOT_FOUND_ON_MAIN | IMPL2/F restore or formally disposition; F accepts retrieval semantics. |
| 09-security-governance/README.md | NOT_FOUND_ON_MAIN | IMPL2/I restore or formally disposition; I accepts policy semantics. |
| 04-memory-compiler/accepted-receipt-and-idempotency-contract.md | NOT_FOUND_ON_MAIN | IMPL2/E restore or formally disposition; E supplies receipt contract. |
| 04-memory-compiler/compiler-state-and-producer-admission.md | NOT_FOUND_ON_MAIN | IMPL2/E restore or formally disposition; E supplies admission contract. |

A docs/en mirror under 03-memory-brain or 05-memory-runtime does not fill a missing canonical root without an explicit source-hierarchy decision.

## 3. Eight required end-to-end flows

Each flow has the same nine checkpoints: issuer; request/response; identity and cursor namespace; idempotency scope; linearization point; durable receipt; failure/Unknown; replay/recovery; visibility.

### F1 — Event ingress → durable acceptance → Compiler admission

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** E ingress/Compiler; I authorization; D authority boundary; Storage persistence
- **Reason:** E Event Store is only a candidate seam; accepted-receipt and producer-admission roots are absent. Compiler overview excludes final canonical authority and production dispatch. D's decision says E AdmissionStore is not D-authoritative and publication_participant_admitted remains false.
- **Missing / provider:** IMPL2/E restore or disposition the missing receipt/admission roots; E supplies dispatch/lease/retry contract; I supplies authorization issuer/epoch; D/Storage supply durable acceptance boundary.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | E accepts producer envelope; I is authorization authority; E AdmissionStore cannot assert D authority. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | Producer actor, Scope refs, payload ref+digest, idempotency key, correlation/causation; return durable Accepted receipt or explicit conflict/rejection. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | Event/receipt IDs stable; candidate idempotency tuple is (producer_actor_ref,idempotency_key); separate from D commit, F watermark and H cursors. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Same producer+key+digest returns original receipt; same key/different digest conflicts; Scope authorization precedes replay. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | Candidate transaction stores envelope, digest, receipt, Pending state and compile-intent outbox row together. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | Receipt and compile intent persist together; replay returns original receipt without duplicate intent. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Dispatcher/worker delivery and post-commit Unknown resolution are not fully specified. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Startup backfills missing intent; dispatcher, leases, retries and DLQ are outside adapter. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | Accepted is not canonical/indexed; private staging until D/I gates. | NOT EVIDENCED — FAIL for Gate A closure |

### F2 — D Canonical Commit → atomic outbox / receipt → F consumer

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** D canonical authority; Storage physical transaction; F consumes authoritative feed
- **Reason:** D canonical store root is absent. Storage trait is candidate-only and disclaims backend/distributed atomicity. E compile-intent outbox is not D canonical-change outbox.
- **Missing / provider:** IMPL2/D restores/dispositions canonical store root; D pins commit/result/cursor/outbox; Storage supplies same-transaction commit/outbox and crash evidence; F supplies consumer dedupe/ack.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | Only D issues canonical identity/version/lifecycle/commit result; Storage cannot mint domain authority. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | CanonicalWriteRequest binds expected version, immutable new version, Scope, authorization/Fence and idempotency; response distinguishes commit/conflict/reject/Unknown. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | D commit cursor and D outbox event ID are bound; F scan watermark is separately F-owned. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Key+request digest resolves one D receipt; changed digest conflicts; Scope checked before receipt lookup. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | Expected one Storage transaction: immutable version, current-version CAS, idempotency record, D sequence, outbox and receipt. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | D receipt/outbox durable and queryable after restart; E compile-intent row is not this receipt. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | CAS conflict determinate; rollback means no commit; lost response during commit remains Unknown until receipt lookup. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | F replays durable D cursor; dedupes at-least-once delivery; gaps cannot be skipped. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | Canonical state visible only after commit and D/I/Fence checks; F projection is derivative. | NOT EVIDENCED — FAIL for Gate A closure |

### F3 — F Retrieval / Index / Watermark / Scan Coverage

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** D owns canonical feed; F owns retrieval/index/watermark
- **Reason:** F normative root 05-memory-runtime/README.md is absent; retrieval-engine material exists only as docs mirror. D canonical feed root also absent; no source defines contiguous watermark proof.
- **Missing / provider:** IMPL2/F restores/dispositions F root; D pins feed cursor; F specifies watermark/gap/tombstone/coverage; Storage pins durable index checkpoint.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | D issues canonical sequence; F alone issues per-index scan watermark and retrieval metadata. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | Request binds actor, resolved Scope, query/filter, consistency and Fence/permission epochs; response separates visible/filtered/irrelevant/gap/unknown. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | D cursor, F per-index watermark, shard cursor and continuation token typed and distinct. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Index dedupe by D event/commit identity + index generation; retrieval retries do not advance scan watermark. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | No F source fixes atomic index mutation + contiguous watermark + coverage proof. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | Per-index scan-through proof with exact D cursor and gaps must persist; shape not pinned. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Gap, malformed event, permission failure, stale Fence or failed shard cannot count as scanned. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Rebuild from D cursor; contiguous prefix advances only after all prior events accounted. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | D Fence and I authorization checked at retrieval/publication; stale index/cache suppressed. | NOT EVIDENCED — FAIL for Gate A closure |

### F4 — Forget Fence → E/F/G/H/Storage visibility and cleanup

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** D canonical Fence issuer; I policy/completion; each derivative Owner executes; Storage projection-only
- **Reason:** D Fence source is Draft/Unverified/Informative and not a wire schema; I global policy root absent. Cross-domain receipt schemas, linearization and production evidence not accepted.
- **Missing / provider:** IMPL2/I restores/dispositions policy root; D pins Fence operation/inventory source; I defines auth/retention/residual policy; E/F/G/H/Storage provide per-target durable ack/replay/visibility evidence.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | D issues ForgetOperation/Fence; I issues policy/global completion; E/F/G/H own derivative acknowledgements. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | Operation ID, target inventory/version, policy authority and expected Fence; each target returns typed per-target ack including unknown/exception. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | D operation/Fence cursor; I PermissionEpoch; E/F/G/H target ack; Storage derived projection cursor are distinct. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Stable operation ID + immutable target/policy digest; per-target ack scoped by operation+target+generation. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | D durable monotonic Fence commit is logical suppression point; cleanup later; I global completion separate. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | D operation/Fence and per-target acks persist; only I may issue global completion receipt. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Unknown target, timeout, offline adapter, backup/external copy or missing inventory blocks completion; fail closed. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Retry rechecks current Fence; restore applies Fence before exposing data; stale publication cannot re-enter. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | D Fence suppresses canonical refs immediately; all derivative paths enforce; physical erasure is I policy. | NOT EVIDENCED — FAIL for Gate A closure |

### F5 — C/H Applied evidence → G Applied decision

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** C owns inference facts; H protocol evidence; G sole Applied issuer; I/D/Storage supply predicates
- **Reason:** G persistence contract is Normative Design Draft with implementation unverified and cross-owner acceptance required. C Applied contract is Draft/Unverified/Informative; H schema/addenda do not prove complete same-request/same-GID predicate join.
- **Missing / provider:** C/H/G/Storage/D/I reconcile exact join contract; G proves ledger crash/restore; Storage proves same-GID terminal; all relevant Owners accept same version.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | C issues immutable CSubmitOutcome; H issues authenticated delivery evidence; G alone issues/mutates Applied; D/I/Storage issue independent proofs. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | G evaluates immutable Applied identity and complete evidence revision for same request/causal transaction; returns Full Applied or explicit non-applied/Unknown. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | Applied ID, request ID, CSubmitOutcome, H evidence revision, COC GID/participant, I decision/epoch, D Fence and Storage receipt are distinct but joined. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Same immutable Applied identity+evidence revision same result; changed evidence revision is explicit supersession/re-evaluation. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | G ledger commit is Applied decision; where JF-10 applies Storage same-GID VisibilityPointer/Receipt must be terminal first. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | G decision and evidence joins persist; Storage same-GID receipt and C/H evidence resolve after crash. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Unknown from C/H/COC/I/D/Storage remains non-Applied; invalidated attempt cannot apply. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Replay uses same request/evidence revision; recovery resolves GID and high-water marks; stale attempts cannot reuse authority. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | Applied is not model comprehension; Accepted/Delivered/ACK alone cannot expose downstream result. | NOT EVIDENCED — FAIL for Gate A closure |

### F6 — I Authorization / PermissionEpoch / revocation

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** I sole policy/authorization authority; every subsystem enforces
- **Reason:** I normative root absent. Scope/Permission model leaves policy and cache/revocation guarantees open. Authorization ADRs concern type/presence and do not establish genuine I issuance, cryptographic trust, key custody or quorum.
- **Missing / provider:** IMPL2/I restores/dispositions policy root; I supplies issuer, signed decision/attestor, PermissionEpoch, revocation/cache freshness and verifier; all domains supply negative enforcement tests.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | I alone issues authorization/attestation and policy/epoch transitions; consumers validate but cannot mint. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | Bind actor, action, resource, Scope, purpose/context and policy version; return decision ID, issuer, subject digest, issue time and epoch. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | Principal, Scope, policy version, PermissionEpoch, decision ID, attestation ID and revocation cursor are distinct. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Decision binds immutable subject digest+policy version; changed subject/policy requires new decision. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | Policy/grant/epoch mutation commit is currentness point; protected operation validates current epoch at its own boundary. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | Decision and revocation/epoch history durable and auditable; full I ledger absent. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Unavailable policy service, unknown issuer, stale epoch or ambiguous decision fails closed. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Retries re-evaluate current authorization; stale queued work cannot execute after revoke. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | All read/write/publication/retrieval/Forget/restore boundaries enforce current I policy and Scope. | NOT EVIDENCED — FAIL for Gate A closure |

### F7 — Global Forget inventory → per-target evidence → I completion

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** I owns global policy/completion; D canonical Fence; each execution Owner owns local evidence
- **Reason:** D explicitly leaves global completion and physical erasure to I. I root absent. D Fence is Draft/Unverified/Informative; inventory, backup/external-copy and exception policy not accepted.
- **Missing / provider:** IMPL2/I restores/dispositions I root; I defines inventory, completion predicate, residual exceptions/backups and receipt; D/E/F/G/H/Storage supply per-target evidence.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | I defines inventory/completion and sole global completion issuer; D issues Fence; each domain issues local ack. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | Global operation binds immutable inventory version/digest and policy; responses list every target's typed state/evidence. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | I operation/policy epoch, D Fence cursor, per-owner ack IDs, Storage projection cursor and backup/external IDs distinct. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | Global op ID+inventory digest+policy version; per-target ack scoped by op+target+Fence generation. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | D Fence commit = logical suppression; I durable completion decision later after all target evidence/exception policy. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | D Fence, per-target receipts and I completion receipt survive restart; I receipt contract absent. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Missing target, unknown executor, offline backup or unverified external copy blocks completion absent explicit I exception. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Reconcile by stable operation IDs; restore reapplies Fence then cleanup; inventory changes require reevaluation. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | Suppression immediate at D Fence; global completion does not gate initial suppression; physical copies remain I policy. | NOT EVIDENCED — FAIL for Gate A closure |

### F8 — Storage atomicity / durability / crash / restore

- **Overall state:** BLOCKED_WITH_REASON
- **Authority / owners:** Storage/Consistency physical guarantees; D/E/F/G/I retain logical authority
- **Reason:** Storage trait is candidate-only, no backend selected; tests are contract-shape only and explicitly do not prove backend atomicity, crash recovery, serialization, multiprocess concurrency or durability. SQLite code is implementation evidence, not accepted proof.
- **Missing / provider:** IMPL2 pins physical contract; Storage/Consistency specifies transaction/isolation/durability/recovery/restore and same-GID; D/E/F/G/I accept boundaries; reproducible fault-injection/crash evidence required.

| Checkpoint | Expected contract and PASS/FAIL rule | Current result |
|---|---|---|
| **Issuer** | Storage attests physical commit/rollback/Unknown only; D issues canonical commit/Fence, E Accepted, G Applied, I policy/completion. | NOT EVIDENCED — FAIL for Gate A closure |
| **Request / response** | Typed transaction request binds participants, GID, immutable writes, CAS, receipts/outbox and Fence/epoch guards; response committed/aborted/Unknown plus proof. | NOT EVIDENCED — FAIL for Gate A closure |
| **Identity / cursor namespace** | Storage GID/participant, D cursor, E receipt, F watermark, G Applied ID and I epoch distinct; same-GID joins explicit. | NOT EVIDENCED — FAIL for Gate A closure |
| **Idempotency scope** | GID+immutable participant/request digest; duplicate prepare/commit same terminal proof; digest mismatch conflicts. | NOT EVIDENCED — FAIL for Gate A closure |
| **Linearization point** | Physical transaction commit (or agreed COC terminal commit); VisibilityPointer/Receipt commits atomically; logical Owner decisions remain distinct. | NOT EVIDENCED — FAIL for Gate A closure |
| **Durable receipt** | Prepared/terminal participant records, commit receipt, visibility pointer, outbox and recovery high-water durable. | NOT EVIDENCED — FAIL for Gate A closure |
| **Failure / Unknown** | Crash precommit aborts; crash during commit queries GID; Unknown stays hidden until resolved; heuristic outcomes explicit. | NOT EVIDENCED — FAIL for Gate A closure |
| **Replay / recovery** | Resolve prepared GIDs and high-water marks before publication; restore Fence/PermissionEpoch/watermarks before reads. | NOT EVIDENCED — FAIL for Gate A closure |
| **Visibility** | Only atomic VisibilityPointer/PublicationReceipt after authority predicates; D Fence projection rebuildable and non-authoritative. | NOT EVIDENCED — FAIL for Gate A closure |

## 4. Cross-flow invariants

1. Authority separation: E Accepted, D CanonicalCommit/Fence, F watermark, G Applied, H protocol evidence, I authorization/completion and Storage physical commit are distinct facts. No subsystem mints another Owner's fact.
2. Namespace separation: producer idempotency key, D commit cursor, D ForgetFence cursor, F watermark, G ContextVersion/Applied identity, H delivery/evidence revision, I PermissionEpoch and Storage GID/participant/receipt are not interchangeable.
3. Unknown is not success: possible durable commit with lost response is reconciled through the corresponding Owner's durable receipt/ledger; never blind-retry with a new identity.
4. Visibility is stricter than acceptance: Accepted, Delivered, ACK, canonical commit, indexed, Applied, logical suppression, physical erasure and global Forget are distinct.
5. Recovery ordering: recover D Fence and I authorization currentness before exposing Storage projections, F indexes, G Context/Applied state, H reconnect output or E queued work.
6. Source presence is not acceptance: Draft/Unverified/Informative documents or passing unit tests do not establish exact-version Owner acceptance or end-to-end evidence.

## 5. Gate A disposition and providers

| Item | Status | Provider / next evidence |
|---|---|---|
| E ingress receipt + producer lifecycle | OPEN | IMPL2/E restore/disposition missing roots; E pins receipt, dispatch, lease and retry; I/D/Storage confirm boundaries. |
| D canonical commit + outbox | OPEN | IMPL2/D restores canonical store root; D+Storage provide atomic commit/outbox/receipt and crash evidence; F accepts feed. |
| F retrieval and scan coverage | OPEN | IMPL2/F restores root; D pins feed; F supplies contiguous watermark and gap/rebuild proof. |
| D Forget Fence and derivative visibility | OPEN | D/I/E/F/G/H/Storage provide exact per-target contract and acceptance; IMPL2/I supplies policy root. |
| C/H/G Applied | OPEN | C/H/G/Storage/D/I reconcile exact join contract; G proves ledger recovery; each Owner accepts own evidence. |
| I authorization/revocation | OPEN | IMPL2/I supplies root; I supplies issuer/epoch/revocation/verifier; all domains supply negative enforcement tests. |
| Global Forget completion | OPEN | I defines inventory, exceptions, backup/external-copy policy and completion receipt; D/executors provide per-target evidence. |
| Storage atomicity/durability/restore | OPEN | IMPL2 pins physical contract; Storage provides transaction/same-GID/fault-injection/crash/restore evidence; logical Owners accept boundaries. |
| Owner A complete review coordination | OPEN | Owner A reads all eight flows, source pins and bilingual parity. |
| Seven CONDITIONAL role reservations from prior matrix | OPEN | Each role discharges its condition against exact source version; proxy disposition is not natural-person signature. |

Gate A remains PARTIAL / OPEN. Gate B remains NOT VERIFIED. Issue #1212 remains OPEN. No implementation, merge, deployment or Issue closure is authorized.

## 6. Review procedure

For every checkpoint, cite exact source path+blob SHA, name issuer and consumer, and attach concrete test/evidence before PASS/FAIL. If prerequisite is absent, ambiguous, candidate-only or unaccepted, record NOT EVIDENCED and keep BLOCKED_WITH_REASON. Never convert a missing source into an assumed contract.

This package is ready for domain-owner review, not Gate A closure. Any material source change requires a new baseline and regenerated blob pins.
