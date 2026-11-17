# Architecture Decision Conflict Register — CONFLICT-002

- Version: 1.0.0; baseline `b372b62c640a2b656e54b6db62a4ee67d7d8c001`.
- Status: A integration dispositions; Owner-owned normative decisions are not replaced.

| ID | Apparent conflict / ambiguity | A disposition | Authority / required action | Gate |
|---|---|---|---|---|
| AC-01 | Modular monolith recommendation vs. unresolved Storage physical topology | No contradiction. Modular monolith is a deployment shape; Storage §8 has selected L1 Option A (one serializable transaction domain per Canonical Memory authority). L4 engine/deployment conformance remains Storage/D/I-owned and open | Storage + D + I select/prove topology; A integrates | G3/G5; JF-10 |
| AC-02 | P0 durable vertical slice vs. unresolved P0 semantic/atomicity prerequisites | P0-07 is conditional and downstream of P0-02..05; only harness/fixture work may run earlier | F/D/P roadmap corrected by A; D/E/Storage own prerequisites | implementation entry |
| AC-03 | Delivery/transport ACK vs. Applied | Must remain separate facts; ACK cannot establish final-request crossing or provider outcome | C/G/H own final-request and Applied contract; I/D own authorization/fence inputs | G2/G4; Issue #3 |
| AC-04 | COC order vs. I commit decision vs. Storage visibility | Preserve separate authority: COC orders/records; I PolicyDomain sequencer decides JF-10 COMMIT/ABORT; Storage resolves same XID and owns visibility; D owns ForgetFence | A coordinates only; no synthesized authority | JF-10 A/B/C |
| AC-05 | Storage-first participant vs. D admission/lineage registration | Follow current crash-safe issue #25 proposal only as candidate: hidden durable Storage participant precedes D participant registration, then I authorization, then Storage visibility. Not a frozen contract absent exact Owner acceptance | D/E/I/Storage must independently accept exact current bundle | G2/G3/G4 |
| AC-06 | Gate A partial pass vs. older issue language saying blocked | Latest Issue #10 amendment governs: Gate A PARTIAL PASS / OPEN; Gate B BLOCKED pending all A conditions; Gate C BLOCKED pending B. Separately, Storage §8 closes L1 Option A; it does not close L4. | Storage supplies remaining A evidence; A tracks | JF-10 A/B/C |
| AC-07 | R Critical/High risk ratings vs. X ordinal complexity scores | Different models; do not sum or substitute. R measures risk; X scores complexity dimensions | A preserves both separate registers | G7 |
| AC-08 | F/D/P simulated roles vs. independent Owner approval | F/D/P are analytical roles in one session; not three independent Owner approvals | Actual B/C/D/E/F/G/H/I/Storage authority decisions remain required | G2 |
| AC-09 | Architecture repository vs. implementation ownership | README confirms architecture-only intent; Issue #7 remains open for canonical runtime repo/engineering lead | Project authority answers Issue #7; no code is added here as implementation | G5/G7 |
| AC-10 | Candidate schema/technology artifacts vs. freeze claims | Candidate and bounded CI status do not imply normative freeze or production conformance | Respective Owner/ADR authority decides; A requires exact-head evidence | G1/G2/G5 |

## Explicit A boundary

A decides global sequencing, scope, cross-owner compatibility and Gate evidence sufficiency. A does not approve B domain semantics, I governance policy, D canonical lifecycle/fence semantics, C provider outcomes, G Applied semantics, H wire schema/cryptography, or Storage physical topology. No conflict is marked closed where an Owner decision or physical proof remains missing.
