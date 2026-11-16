# NVIDIA Context Optimization — Conflict and Blocker Register

- Owner: A — Principal Integration Architect
- Date: 2026-11-17
- Severity: P0 blocks interface freeze / implementation unless explicitly closed by required Owners

## 1. Cross-Owner conflict and blocker register

| ID | Owners | Object / field | Original basis / disagreement | Correctness impact | A disposition | Required evidence | Owner revision? | Blocks freeze? |
|---|---|---|---|---|---|---|---|---|
| X-01 | B/F/D/I | Observation, Evidence, Derived Summary, Canonical Memory; ProducerClass and lineage | B says Observation is not automatically proposition/canonical Memory; F owns runtime Archive; D says F producer and G derivative inventory incomplete; I requires closed-world producer/recipient/backup inventory | Blanket D inclusion overclaims canonical authority; blanket exclusion permits forgotten canonical derivatives to escape | D authority applies to classified D-covered lineage; Archive-only observations remain F runtime under I policy; no global inference without inventory | Complete producer/recipient/replica/export/backup/restore class matrix; exact lineage and policy mapping | YES: D/F/I with B semantics | YES |
| X-02 | F/G/B/H/I | ArchiveLocator vs ContextObservationReference; RecallIntent, RecallSession, ReadCursor, ReadReceipt | B/F/G/H/I agree conceptually on distinct types and receipt/cursor limits; F/G contract and H wire mapping remain conditional | Type confusion, cursor cross-context reuse, unauthorized read or false evidence | Separate owner-local identities; F cursor bound to one session/object/revision/selector/security checkpoint; G ref bound to ContextVersion; H transports opaque typed refs | Pinned F/G Recall contract, B semantics, H wire mapping, I/D revalidation proof | YES: F/G/B/H/I | YES |
| X-03 | D/F/G/I | ForgetFence, Producer Registration, Derived Registration; capture/recall/cache/compaction | D owns fence; F Archive; G Context; I policy. Complete inventory and local gate proof absent | Forgotten lineage may re-enter through Archive, cache, compaction, snapshot or replay | Independent D fence and I epoch; every owner checks its own boundary; unknown fails closed | Producer/derivative inventory; linearization points; race tests for admission, pages, cache fill/hit and CAS | YES: D/F/G/I | YES |
| X-04 | G/B/C/D/F/I | TSS fields, ContextVersion, CompactionLineage, LossLedger | G accepts Context projection; B requires typed epistemic/time meaning; C needs task/request evidence; D/I require transitive Forget and retention | Loss of rare constraints, epistemic upgrade, stale or forgotten source reintroduction | TSS remains G-owned non-canonical projection; hard fidelity vetoes and source-anchored lineage mandatory; no unmeasured fixed thresholds | G schema; B semantic review; D/I lineage/retention; C/F evidence mapping; stale/Forget CAS tests | YES: G/B/C/D/F/I | YES |
| X-05 | C/G/H/I/D/B | DeliveryIntent, ACK, AppliedAttestation, FinalRequestBoundaryId, managed-region digest | CGH-APPLIED-1.1 exact design matrix accepted with exceptions; H schema candidate, C provider idempotency and G persistence unverified; Issue #3 open | False Applied, duplicate application, stale context after reconnect or false historical ordering | ACK never means Applied; C Tier-1 proof is input; G predicate authoritative; causal ambiguity => UNKNOWN | Close Issue #3 residuals; versioned schema/IDL; provider digest tests; timeout, ACK-loss, supersession and Forget race tests | YES: C/G/H/I/D/B | YES |
| X-06 | E/D/Storage/I | Canonical Derived Registration, Publication Gate, VisibilityPointer, PublicationReceipt, prepared XID | E accepts authority separation; D/E/Storage atomic gate architecture accepted; JF-10 implementation and I sequencer integration remain open | Staged/derived data could become visible without atomic fence/permission/receipt ordering | VisibilityPointer is sole Storage publication authority; require exact I-approved owner-gate sequencer/2PC and same-XID recovery | I acceptance; D/E/Storage contract; prepared-XID and crash/ACK-loss/failover/restore evidence | YES: I/D/E/Storage | YES |
| X-07 | H/F/G/C/I/D | Recall/Delivery wire schemas, errors, cursor, idempotency, timeout, reconnect | H accepts message-family semantics and schema candidate; generated wire/IDL, parser and replay tests incomplete | Protocol ambiguity, stale cursor, duplicate side effect, ACK interpreted as success | Distinct Recall/Delivery lifecycles; typed cursor; stable logical IDs + attempt IDs; UNKNOWN/IN_DOUBT on ambiguity | H versioned schema/IDL; B type mapping; F/G/C/I/D exact acceptance; negative protocol suite | YES: H/F/G/C/I/D/B | YES |
| X-08 | I/D/F/G/H/C/Storage | Principal, PermissionEpoch, Retention, Revocation, inventory seal and Global Forget | I security boundary conditionally accepted; inventory/governance and external approvals remain blocked; Issue #4 open | Unregistered target, stale permission or untracked backup/external copy may be exposed or omitted from Forget | I retains security authority; D fence independent; unsupported target cannot be complete; fail closed | I append-only governance approvals, authoritative inventory/seal, exception authority, recipient/backup/restore coverage | YES: I | YES |
| X-09 | Storage/D/E/I | Recovery Cutoff Batch, Owner-local Gate, JF-10 same-XID bridge, WAL/PITR | JF-10/COC architecture design accepted with exceptions; JF-10 P0 and Gate C remain open; production deployment not designated | Split-brain between authorization and visibility; restore may roll back Forget/permission | Require I-sequenced durable participant protocol; exact XID only; independent D/I high-water; quarantine on any gap | Production deployment binding; prepared XID, sequencer, crash/recovery, WAL gap and PITR tests | YES: I/Storage/D/E | YES |
| X-10 | A/B–I/Storage | Interface freeze / version compatibility | Eight NVIDIA Owners all conditional; CGH-APPLIED and COC matrices design-level only; Issues #3/#4 and JF-10 P0 remain | Premature implementation cements incompatible ownership, state and recovery assumptions | Freeze denied; conditional architecture baseline only | All required Owners accept one immutable contract revision; P0 closure; schema compatibility and conformance evidence | YES: all relevant Owners | YES |

## 2. Required Owner remediation tasks

### B — Domain semantics
- Publish reusable Observation/Evidence/Derived Summary/Canonical Memory vocabulary and time/epistemic transitions.
- Review G TSS and lineage schema; maintain typed identity and Scope vs Permission distinction.
- Confirm H mapping preserves semantic discriminators without making refs credentials.

### C — Agent boundary
- Close Issue #3 residuals with exact final-request evidence profile, digest profile, provider capability and current D/I authority binding.
- Provide Tier-1 final request boundary evidence and protected-region negative tests.
- Correlate Recall, selection, compaction, DeliveryId/AttemptId, cache outcome and final request.

### D — Canonical Memory / Forget
- Publish exact F ProducerClass and G derivative/replica/backup classification.
- Define fence/barrier serialization against F admission/final Archive publication and G Context/compaction CAS.
- Provide authoritative fence/lineage high-water and stale Snapshot/Delta replay behavior.
- Supply D-owned negative test evidence; do not infer I Global Forget completion.

### E — Compiler / Publication
- Freeze complete producer identity, immutable dependency manifest and derived registration input only after D/I classification.
- Remain non-terminal until Storage PublicationReceipt is authoritative.
- Join D/E/Storage atomic gate and same-XID recovery; test duplicate key/digest conflict and post-Forget replay.

### F — Archive / Recall
- Publish one exact F/G Recall contract revision: locator, source revision/hash, selector coordinates, session/cursor binding, receipt, completeness and error terminality.
- Classify Archive-only vs D-covered producer work with D/I; define cache hit/fill final gates.
- Provide capture/Recall/cache race and Archive Restore evidence; retention policy remains I-owned.

### G — Context / TSS / Compaction
- Publish exact TSS, ContextObservationReference, ContextVersion, fidelity hard veto, CompactionLineage/LossLedger and invalidation schema.
- Obtain B semantic and D/I transitive Forget/retention decisions.
- Define CAS/abort behavior when source revision, permission, fence or inventory changes.
- Provide compaction/Forget/restore and stale Snapshot/Delta tests; do not claim Applied from delivery intent.

### H — BMCP
- Publish versioned Recall, Delivery, ACK, Applied evidence transport, Cancel/Supersede, Reconnect and Error schemas.
- Define capability negotiation, unknown-field behavior, cursor invalidation, idempotency retention and status reconciliation.
- Keep Forget clear ACK, transport ACK and Applied evidence distinct; execute ACK-loss/timeout/reconnect tests.

### I — Security / Governance
- Resolve Issue #4 with authoritative producer/recipient registry, inventory epoch/seal, late discovery, unsupported/offline defaults and approved exceptions.
- Record effective governance approvals for Global Forget completion and retention/backup/external recipient obligations.
- Accept/reject exact JF-10 owner-gate/sequencer participation and recovery evidence.
- Maintain independent PermissionEpoch and D ForgetFence authority.

### Storage — Durability / Recovery
- Complete JF-10 same-XID participant recovery and I-sequencer owner-gate integration.
- Designate actual project Canonical Authority deployment, database build/configuration, service owner/on-call, failure domains and recovery objectives.
- Execute prepared-XID, crash, coordinator/DB failover, WAL gap, PITR and restore quarantine tests with authoritative readback.
- Keep reference-model and capability CI labelled as bounded evidence, not production conformance.

## 3. Open GitHub coordination issues

- Issue #3 — Phase 3.6 C/G/H Applied Evidence & BMCP Wire Contract: OPEN.
- Issue #4 — I external dependency decisions: inventory, authorization and Global Forget completion: OPEN.

This register does not close, reassign or approve either issue.

## 4. Re-entry criteria

A blocker is eligible for re-review only when the responsible Owner publishes the revision on its own branch, records exact path/Blob SHA/commit SHA, states a decision on the exact A contract revision, supplies required negative/recovery evidence, and identifies downstream Owners. A then re-queries branch heads, reads exact files, compares semantic diffs and updates the decision register. No Owner branch is modified by this register.
