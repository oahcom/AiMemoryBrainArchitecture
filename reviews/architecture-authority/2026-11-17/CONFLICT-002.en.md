# Architecture Decision Conflict Register — CONFLICT-002

- Version: 1.0.0; historical assessment snapshot `6470f25ca23b8d35c06f60be2326867066418d18` (not current main).
- Status: A integration dispositions; Owner-owned normative decisions are not replaced.

| ID | Apparent conflict / ambiguity | A disposition | Authority / required action | Gate |
|---|---|---|---|---|
| AC-01 | Modular monolith recommendation vs. selected Storage L1 logical profile and open L4 deployment | No contradiction. Modular monolith is a deployment shape; Storage §8 has selected L1 Option A (one serializable transaction domain per Canonical Memory authority). L4 engine/deployment conformance remains Storage/D/I-owned and open | Storage + D + I prove L4 realization of Option A; A integrates | G3/G5; JF-10 |
| AC-02 | P0 durable vertical slice vs. unresolved P0 semantic/atomicity prerequisites | P0-07 is conditional and downstream of P0-02..05; only harness/fixture work may run earlier | F/D/P roadmap corrected by A; D/E/Storage own prerequisites | implementation entry |
| AC-03 | Delivery/transport ACK vs. Applied | Must remain separate facts; ACK cannot establish final-request crossing or provider outcome | C/G/H own final-request and Applied contract; I/D own authorization/fence inputs | G2/G4; Issue #3 |
| AC-04 | COC order vs. I commit decision vs. Storage visibility | Preserve separate authority: COC orders/records; I PolicyDomain sequencer decides JF-10 COMMIT/ABORT; Storage resolves same XID and owns visibility; D owns ForgetFence | A coordinates only; no synthesized authority | JF-10 A/B/C |
| AC-05 | Storage-first participant vs. D admission/lineage registration | Follow current crash-safe issue #25 proposal only as candidate: hidden durable Storage participant precedes D participant registration, then I authorization, then Storage visibility. Not a frozen contract absent exact Owner acceptance | D/E/I/Storage must independently accept exact current bundle | G2/G3/G4 |
| AC-06 | Gate A partial pass vs. older issue language saying blocked | Latest Issue #10 amendment governs: Gate A PARTIAL PASS / OPEN; Gate B BLOCKED pending all A conditions; Gate C BLOCKED pending B. Separately, Storage §8 closes L1 Option A; it does not close L4. | Storage supplies remaining A evidence; A tracks | JF-10 A/B/C |
| AC-07 | R Critical/High risk ratings vs. X ordinal complexity scores | Different models; do not sum or substitute. R measures risk; X scores complexity dimensions | A preserves both separate registers | G7 |
| AC-08 | F/D/P simulated roles vs. independent Owner approval | F/D/P are analytical roles in one session; not three independent Owner approvals | Actual B/C/D/E/F/G/H/I/Storage authority decisions remain required | G2 |
| AC-09 | Architecture repository vs. implementation ownership | README confirms architecture-only intent; Issue #7 remains open for canonical runtime repo/engineering lead | Project authority answers Issue #7; no code is added here as implementation | G5/G7 |
| AC-10 | Candidate schema/technology artifacts vs. freeze claims | Candidate and bounded CI status do not imply normative freeze or production conformance | Respective Owner/ADR authority decides; A requires exact-head evidence | G1/G2/G5 |

| AC-11 | Storage topology ADR retains pre-addendum prose saying no option is selected, while §8 explicitly supersedes it for L1 | §8 controls: Option A is selected at L1; historical §3 text is not a current blocker but should be explicitly marked/simplified to prevent ambiguity | Storage | Before G1/G5 freeze review | G1/G5 |

| AC-12 | Storage v3.2.9 manifest presented as current although later C/D/I review pins and H CI changed | Exact candidate semantics remain coherent, but manifest is stale; Storage must publish v3.3.0/equivalent, C/H/D/I review the identical Blob, then A re-reviews | Storage + C/H/D/I; A integrates | G1/G2/G6 |
| AC-13 | New B identity/entity artifacts could be mistaken for closed domain semantics | They are CANDIDATE/B1 IN PROGRESS; Fact/Claim remains ADR-BLOCKED; no dependent schema freeze | B; I/C/H consumers | G2/G3 |
| AC-14 | Option A logical selection could be mistaken for completed L1/L2 | Conditional L1 direction only; A-01..A-05 and exact D adoption remain open; L2/L3/L4 separate | Storage/D/I + A | G2/G3/G4/G5 |

## Explicit A boundary

A decides global sequencing, scope, cross-owner compatibility and Gate evidence sufficiency. A does not approve B domain semantics, I governance policy, D canonical lifecycle/fence semantics, C provider outcomes, G Applied semantics, H wire schema/cryptography, or Storage physical topology. No conflict is marked closed where an Owner decision or physical proof remains missing.


## Current main HEAD / 当前 Main HEAD

The current main HEAD independently observed for this publication is `8c0c5b11abf56a6f580fcf2a99c8043d3057da4f`. The earlier `6470f25...` / `b372b62...` values are historical assessment snapshots, not current main. This package has not completed a full source-by-source delta audit against current main; G1 remains PARTIAL and all Gate/freeze restrictions remain in force.
