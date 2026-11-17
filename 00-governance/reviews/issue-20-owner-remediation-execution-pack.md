# Issue #20 — Owner Remediation Execution Pack (Coordinator Proposal)

**Status:** COORDINATOR PROPOSAL / NON-NORMATIVE / NOT AN OWNER DECISION  
**Review target:** Storage commit `a65973093bb33c7c06ae503f421e096fadb5796b`, Blob `6f4b003b0a398c15b1f22a03c612f2c58afa3e7d`  
**Purpose:** Convert the six coordinator-simulated reviews into bounded, independently reviewable Owner deliverables. This document does not amend the Storage proposal and does not authorize implementation or interface freeze.

## 1. Execution order and dependency

1. **D + I semantic decisions (parallel, mutually cross-reviewed):** establish the two independent authorities before any lifecycle contract is frozen.
2. **F + E + G lifecycle decisions:** consume D/I semantics; each Owner defines its own local state, receipts, admission and restore release.
3. **H wire contract:** translate accepted semantic contracts into strict schemas; H must not invent or silently reinterpret Owner semantics.
4. **Storage amendment:** implement persistence/atomicity mapping only after semantic and wire contracts are pinned.
5. **A integration:** reconcile exact Owner artifacts and decide freeze readiness. A cannot waive an Owner blocker.

No phase is considered complete because a coordinator prompt, role simulation, issue comment, or branch file authored by a non-Owner exists.

## 2. D — canonical lineage and Forget Fence deliverable

D must publish an append-only decision artifact on D's branch, pinned to the exact Storage Blob above, covering:

- Normative classification of Archive-only, D-covered and mixed/unknown lineage. “No MemoryRef yet” is not proof of Archive-only.
- Stable ProducerWork identity and mandatory registration-before-execution for D-covered work.
- Exact atomic serialization point for admission/registration versus fence installation; define inclusive/exclusive high-water and assignment of racing work exactly once.
- Complete direct/transitive dependency registration before visibility; retries, leases, DLQ, replay and late-discovered descendants remain within the same logical work lineage.
- Late lineage discovery after barrier terminalization: quarantine object and all derivatives, reopen/invalidate the barrier under a new generation, reconcile before disclosure.
- D-owned terminal and release predicates. Storage may persist/serialize but cannot mint D receipts or decide D semantics.

**Required evidence:** state-transition table; identity tuple; linearization rule; race matrix; negative cases for fence/register, late descendant, retry-after-terminal, ambiguous commit and restore replay.

## 3. I — global inventory and authorization deliverable

I must publish an append-only decision artifact on I's branch, pinned to the exact Storage Blob above, covering:

- Authenticated ProducerClass/ProducerIdentity/instance/scope/capability and recipient/onward-copy identity.
- Authoritative enrollment and de-enrollment registry, independent completeness evidence, and discovery of unregistered instances/routes.
- ProducerDomainInventoryEpoch and TargetInventorySeal: canonical target-set encoding, snapshot boundary, signer, validity, invalidation, pagination/shard completeness and verifier.
- Positive evidence for empty categories and NotApplicable; unknown is deny/quarantine, never implicit exclusion.
- Exact join proof from each I-inventoried D-covered producer class/instance/scope to D registration semantics; no arithmetic comparison between I epochs and D cursors.
- PermissionEpoch/revocation, retention/legal-hold/crypto-erasure exception authority, and Global Forget governance boundary. Issue #4 approvals remain separate.

**Required evidence:** inventory source-of-truth map; seal preimage and signature envelope requirements; join matrix; invalidation matrix; unknown/empty-category negative vectors.

## 4. F — Archive and Recall local lifecycle deliverable

F must decide on F's branch:

- Separate object, immutable revision, manifest, locator, capture operation, Recall session and cursor identities.
- Idempotent capture/revision semantics and mixed-lineage treatment.
- D/I/F authorization recheck at cache hit, each Recall page, cursor resume, final handoff/export and downstream delivery.
- Cursor/session invalidation on fence, PermissionEpoch, inventory-seal or restore-generation change.
- F-local restore gate and release receipt bound to store/namespace/partitions/index/cache generation and Recall sessions; Storage SERVING is not F release.

**Required evidence:** local state machine; receipt fields; stale cursor/cache tests; partial capture and restore quarantine tests.

## 5. E — compiler producer lifecycle deliverable

E must decide on E's branch:

- Stable WorkItem/attempt/output identities across lease expiry, worker replacement, retry, DLQ and replay.
- Atomic handoff from D registration to E scheduling; no execution before required registration.
- Output binding to exact input revisions, dependency digest, compiler version/configuration and request digest.
- Private staged output until D/I final gates and visibility commit.
- Lost-ACK/ambiguous publication recovery by querying the same stable IDs; never mint a replacement ID to bypass uncertainty.
- Restore reconciliation of queued, leased, executing, DLQ, replay and staged output before E-local release.

**Required evidence:** state machine; identity tuple; crash-point table; duplicate/replay/fence-race tests.

## 6. G — Context and derivative lifecycle deliverable

G must decide on G's branch:

- Per-fragment provenance and union of all D-covered ancestors for mixed Context/TSS/ContextVersion.
- Lineage preservation through compaction, snapshot, delta, reuse, delivery and export.
- Current D/I validation at assembly, compaction, reuse, snapshot/delta application and delivery.
- Stale references remain suppressed after restore; restore does not make a stale snapshot valid.
- G-local restore release bound to restore generation, Context/TSS high-water, lineage reconciliation digest and invalidated snapshot/delta set.

**Required evidence:** typed lineage model; state machine; stale snapshot/delta and late-ancestor race vectors; local release receipt.

## 7. H — strict BMCP wire-contract deliverable

H must publish versioned schemas only after D/I/F/E/G semantic field ownership is pinned:

- ProducerClassificationReceipt, ArchiveManifestReceipt, D ProducerWork/Dependency receipts, TargetInventorySeal reference, RestoreReadinessManifest, owner-local release receipts and Storage restore receipt.
- Nominal types for I epoch, D registry/high-water/fence generation, G version, F object/revision/cursor, E work/attempt/output and Storage restore generation.
- Required/optional/nullability, canonical encoding, digest preimage, signature envelope (issuer/audience/purpose), replay protection, unknown-critical and downgrade rules.
- Strict rejection of duplicate keys, malformed opaque positions and cross-authority cursor/epoch coercion.

**Required evidence:** schema source + generated artifacts; compatibility matrix; positive/negative parser vectors; signature/canonicalization tests. A schema candidate is not accepted until the semantic Owners pin it.

## 8. Storage — persistence/atomicity amendment deliverable

After D/I/F/E/G/H exact decisions, Storage must:

- Map each Owner-owned receipt and state transition to durable records without taking semantic ownership.
- Define atomic persistence boundaries for admission/fence, dependency closure/publication, inventory-seal invalidation and restore serving CAS.
- Define hidden prepare, commit, rollback, same-operation recovery and ambiguous-ack behavior for the selected transaction profile.
- Preserve independent D and I control authorities and independent owner-local restore releases.
- Bind every artifact to exact schema/version and immutable source pins.

**Required evidence:** record-to-contract mapping; transaction/lock/recovery profile; crash matrix; exact DB/version/config evidence; conformance tests. No database selection or production proof is inferred by this pack.

## 9. A — integration decision

A may issue a formal integration decision only after all six Owner artifacts are independently attributable and exact-version pinned. The decision must enumerate resolved findings, accepted conditions, blockers and deferred engineering evidence, and explicitly state FREEZE APPROVED or FREEZE NOT APPROVED. A cannot convert missing Owner evidence into acceptance.

## 10. Required artifact attribution

Every Owner comment on Issue #20 must include:
- Owner and branch;
- artifact path;
- reviewed Storage commit + Blob;
- artifact commit SHA + Blob SHA;
- exact disposition;
- numbered findings with severity, section, required change and closure evidence;
- unresolved dependencies and whether they block interface freeze.

## 11. Current coordinator status and non-claims

At the latest Issue #20 comment fetch, the issue had three comments: the review protocol, coordinator-simulated six-role review, and coordinator review publication. No independently attributable D/I/F/E/G/H decision or A final integration decision was present in those comments.

This pack is an execution aid only. It does not claim Owner acceptance, implementation, CI/test pass, runtime conformance, Global Forget completion, physical deletion, restore safety, interface freeze, production activation or merge. Issue #20 remains OPEN.
