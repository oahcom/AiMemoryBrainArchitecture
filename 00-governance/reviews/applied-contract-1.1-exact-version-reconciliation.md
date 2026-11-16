# CGH-APPLIED-1.1 Exact-Version Reconciliation

- Assessment ID: P-APPLIED-1.1-EXACT-RECON-001
- Date: 2026-11-17
- Prepared by: Session P coordinator
- Status: **FREEZE BLOCKED — EXACT OWNER DECISIONS INCOMPLETE**
- Scope: Reconciliation of current A package and C/G/H Owner artifacts; no Owner decision is created or substituted.

## 1. Executive result

The current successor contract is `CGH-APPLIED-1.1`, not the older `CGH-APPLIED-1.0`.

The current A package is:
- `reviews/integration/phase-3.6-cgh-applied-1.1-causal-order-decision-package.md`
- Blob SHA: `4961ffefc0f9920efb8425a9b2a7af42d8f64819`
- Companion COC deployment/recovery architecture:
  `reviews/integration/phase-3.6-causal-order-coordinator-deployment-architecture.md`
- Companion Blob SHA: `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`
- Profile: `CausalOrderProfile/1.0`
- H schema target: `bmcp.applied-ack/1.1.0`

**Current exact-version decision vector:**
- G: **ACCEPT WITH ENUMERATED EXCEPTIONS** for exact A package Blob `4961...` plus companion COC Blob `fc3...`.
- C: has published C-side 1.1 causal-order specification, but its formal exact-package decision remains **PENDING**. C's recorded formal Applied decision is for CGH-APPLIED-1.0 / A package Blob `122b...`, not the current 1.1 package.
- H: has a concrete 1.1.0 JF10 bridge schema candidate, but no exact H Owner acceptance of current A package Blob `4961...` was found. H's recorded exact Applied decision is for CGH-APPLIED-1.0 / Blob `122b...`; the schema candidate is explicitly not production-frozen.
- B/D/I: their component semantics/specifications exist, but no exact decision against current 1.1 package and companion pair was found in the inspected current Owner artifacts.
- Coordinator/Storage operator: no named/deployed operator or production durable coordinator acceptance is evidenced.

Therefore **Applied Contract Frozen = NO**. The current package itself says A CANDIDATE / OWNER REVIEW REQUIRED / NOT FROZEN. G's acceptance does not bind C or H.

## 2. Exact source pins

| Role | Branch | Current HEAD | Artifact | Blob SHA | Finding |
|---|---|---|---|---|---|
| A | `session-a-integration-2026-11-16` | `cf98cdb8fb3ee99d7b9aed54a14dc8888cf04175` | CGH-APPLIED-1.1 decision package | `4961ffefc0f9920efb8425a9b2a7af42d8f64819` | Candidate, exact Owner review required |
| A | same | same | COC deployment/recovery companion | `fc3bac39ec64fda68b8cba5e1aada4e719e5acea` | Companion candidate, exact Owner review required |
| C | `session-c-agent-integration-2026-11-16` | `2e5776029bc4271c33525f04c7d0f0708e4bbae8` | C-submit cross-authority causal-order contract | `45a48249717c8cddb07ab96197730ef93d406c22` | C-side specification; cross-owner acceptance OPEN |
| C | same | same | Final Request Evidence Contract | `fd2f47ba6c89bb270e9f2bec956873cb7ae3592b` | C exact formal decision remains on 1.0 |
| G | `session-g-memory-context` | `72a8066b4401f9586fe10775d545384b82736f07` | Applied/Forget reconciliation contract | `aa3afa73d8a76cc6f025839c52bfbff6a983046a` | Explicit acceptance of 1.1 recovery-batch amendment |
| H | `session-h-bmcp-protocol` | `242d8ab5da890181e762561bb3d3a662287fb63c` | Exact H decision for A 1.0 package | `c0e10966e8dd95a9d1f5b1dfa156cb4b098b26e0` | Does not accept current 1.1 package |
| H | same | same | BMCP Applied ACK 1.1.0 JF10 bridge schema | `a8a945cc3623c2907003b93625e3c79742150944` | Schema candidate, not production-frozen |

## 3. Owner decision ledger

### C — exact 1.1 decision pending

C's `phase-3.6-c-submit-cross-authority-causal-order-contract.md` targets `CGH-APPLIED-1.1`, `CausalOrderProfile/1.0`, and `bmcp.applied-ack/1.1.0`. It specifies:
- stable ParticipantIntentRef bound to request digest, boundary, identity/session, context/delivery and capability;
- I single-use CommitAuthorizationReceipt consumption and terminal proof;
- D exact ForgetFence/complete lineage binding and cutoff/effective positions;
- provider invocation only after exact I/D owner proofs and final reservation;
- CSubmitOutcome and determinate CausalOrderTerminalProof;
- UNKNOWN/IN_DOUBT with no Full Applied when provider outcome or owner order is uncertain.

But its status says C-side contract amendment specified and coordinator deployment/cross-owner acceptance open. C's separate formal decision record only accepts `CGH-APPLIED-1.0` against A Blob `122b...`. No exact C decision for current Blob `4961...` and companion `fc3...` was found.

### G — exact 1.1 package pair accepted with exceptions

G's current contract records:
- Exact A package Blob `4961ffefc0f9920efb8425a9b2a7af42d8f64819`.
- Exact COC companion Blob `fc3bac39ec64fda68b8cba5e1aada4e719e5acea`.
- Decision: **ACCEPT WITH ENUMERATED EXCEPTIONS**.

G requires recovery-cutoff batch and pre-batch participant reconciliation before any new Full Applied promotion. Missing/unknown COC order, owner-local pending-gate reconciliation, participant enumeration, I terminal outcome, D complete-lineage barrier or owner high-water proof prevents Full Applied and suppresses protected current use.

G's exceptions remain substantive:
1. G validator/Applied persistence has not been shown consuming the full recovery-batch evidence.
2. Same-identity/digest replay, conflict quarantine and restore behavior need executable tests.
3. G-CO/Applied race suites remain SPECIFIED / NOT RUN.
4. No implementation or production pass is claimed.

### H — 1.1 schema candidate exists; exact package acceptance pending

H's exact C/G/H Applied decision artifact approves with exceptions only the prior A package Blob `122b...` (CGH-APPLIED-1.0). It explicitly does not freeze a concrete Applied wire schema.

The H branch now contains schema candidate `bmcp.applied-ack/1.1.0-jf10-bridge.schema.json`, Blob `a8a945cc3623c2907003b93625e3c79742150944`. Its title/description identifies it as a JF-10 COC bridge candidate and explicitly says it is not production-frozen; authority signatures, canonicalization and cross-field semantic checks require runtime validators.

The existence of this schema file is not H acceptance of A's current package. H must decide the exact pair `4961...` + `fc3...`, identify whether the 1.1.0 schema is the intended wire contract for the complete Applied flow or only the JF10 bridge, and close H-EX-01 requirements for field requiredness, canonicalization, crypto, replay, compatibility and conformance.

## 4. Critical semantic/technical observations

1. **Do not conflate Applied and JF-10 bridge schema.** The JSON schema is titled `BMCP Applied ACK 1.1.0 — JF-10 COC bridge candidate`; it defines five JF-10 COC bridge message families. A 1.1.0 schema version string alone does not prove the entire C/G/H Applied lifecycle wire schema is complete.
2. **Coordinator outage semantics are material amendments.** The current A package includes owner-local pending gates and a recovery batch for I/D requests during COC outage. Prior approvals against `9808...` or `d4eef...` do not cover the current package pair.
3. **G's acceptance is bounded.** G accepted the current exact package and companion within G's Applied predicate authority, with implementation and test exceptions. It cannot approve C provider evidence, H wire schema, I authorization or D fence semantics.
4. **The exact current C and H decisions are the remaining central C/G/H blockers.** C has not adopted the current 1.1 pair; H has not adopted it either. B/D/I and Storage/operator confirmations also remain prerequisites in the A package.
5. **Implementation is still separate.** All relevant documents keep coordinator deployment, runtime validator, Applied persistence, and G-CO/race tests open or not run.

## 5. Required closure actions

1. C Owner: record an explicit decision against exact A package Blob `4961...` and COC companion `fc3...`; list exceptions and compatibility/migration impact.
2. H Owner: record an explicit decision against the same exact pair; state whether schema Blob `a8a945...` covers all required Applied messages or only the JF10 bridge; publish any missing schema amendments and pin the final schema Blob.
3. D and I Owners: record exact-version acceptance/exception for their own fence/authorization clauses, including request cutoff versus effective positions, single-use receipt, pending gates and recovery-batch semantics.
4. B Owner: confirm typed reference/role-tagged ScopeBindingSet and identity semantics against the exact current package without reopening unrelated B semantics.
5. Storage/coordinator operator: identify actual runtime implementation and accountable operator, durable service, recovery/failover profile, and the real C/D/I/G/H evidence paths.
6. A: re-fetch all exact Owner artifacts and package blobs, then update the freeze vector. Do not mark Frozen until all required Owner decisions and schema compatibility evidence are exact-version pinned.
7. After contract closure, run schema validation, C/G/H integration and G-CO/race tests on a pinned build. Do not promote design acceptance to implementation pass.

## 6. Final verdict

- Current package: `CGH-APPLIED-1.1`, Blob `4961...`, companion `fc3...`.
- G: exact-version ACCEPT WITH ENUMERATED EXCEPTIONS.
- C: exact-version decision pending.
- H: exact-version decision pending; 1.1.0 JF10 bridge schema candidate exists but is not production-frozen.
- B/D/I/Storage operator: exact current package confirmations and implementation evidence remain incomplete.
- Applied Contract Frozen: **NO**.
- Implementation verified: **NO**.
- Conformance tests: **NOT RUN / NOT VERIFIED**.
