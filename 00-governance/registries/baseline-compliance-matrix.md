# Existing Design — Project Baseline Compliance Matrix

- Review version: 0.1.0
- Status: **INITIAL STATIC REVIEW; NOT A COMPLIANCE CERTIFICATION**
- Baseline under review: proposed PB-2026-11-16 v0.1.0
- Source baseline: main @ `8a6414158c9c056c1638222534e1993d1bbc99d2`; cross-branch artifacts cited by exact branch and blob SHA where fetched.

## Status meanings
COMPLIANT = evidence supports the criterion at the stated review scope; PARTIALLY_COMPLIANT = some requirements supported, gaps remain; NON_COMPLIANT = direct conflict evidenced; NOT_REVIEWED = no adequate artifact review; BLOCKED_BY_OPEN_DECISION = cannot determine/freeze until named ADR or authority decision. Static review cannot prove runtime behavior.

| PB / criterion | Existing evidence and scope | Status | Gap / required owner action |
|---|---|---|---|
| PB-01 Mission | main README; system-overview.md states independent durable Brain across Agents/models/sessions | COMPLIANT (document-level) | PGA ratification pending; no product validation implied |
| PB-02 Scope | README + system overview + component map | COMPLIANT (logical design) | Module capability conformance and owner baseline still required |
| PB-03 Non-goals | system overview explicitly excludes planning, tool execution, guardrails and framework-specific ownership | COMPLIANT (document-level) | Check all module APIs/implementation during G1/G3 |
| PB-04 Architecture | component-map.md and responsibility-matrix.md define Brain/Compiler/Runtime and cross-cutting roles | PARTIALLY_COMPLIANT | Need all module baselines, exact authority reconciliation and Context/Integration/BMCP/Security placement acceptance |
| PB-05 Domain distinctions | README lists distinct objects; Phase 2 and Phase 3 reviews preserve Fact/Claim blocker | BLOCKED_BY_OPEN_DECISION | B Fact/Claim ADR and typed-reference semantics unresolved; no schema freeze |
| PB-06 Context operations | G responsibility is represented in component map; Phase 2/3 review recognizes G Context authority | PARTIALLY_COMPLIANT | Need explicit owner acceptance for full operation list, version/delivery/applied evidence and protected region |
| PB-07 Agent independence | README/system overview model-/Agent-independent; H envelope remains candidate | COMPLIANT (design intent) | Adapter interoperability and portability tests absent |
| PB-08 Security/governance | I Principal/ActorRef proposal; H identity fields candidate; Phase 3 review flags B/I/H binding | BLOCKED_BY_OPEN_DECISION | Authenticated identity, typed references, permission epoch, revocation and target mapping not jointly approved |
| PB-09 Engineering | README and system overview describe local-first/resource-aware; Rust/modular-monolith/technology selection not verified in reviewed excerpts | NOT_REVIEWED | Engineering decision inventory and representative benchmarks required; no tech choice promoted |
| PB-10 Quality | Phase 2/3 reviews explicitly disclaim implementation/security/performance certification; no run evidence reviewed | NOT_REVIEWED | Build test, conformance, threat, race, fault, restore and performance evidence required |
| PR-01 Brain Independence | README/system overview | COMPLIANT (design intent) | Runtime/framework coupling inspection required |
| PR-02 Model Independence | README/system overview | COMPLIANT (design intent) | Multi-model/no-model portability test absent |
| PR-03 Responsibility Boundary | system overview non-goals | COMPLIANT (document-level) | API/implementation scan required |
| PR-04 Canonical Memory Authority | responsibility matrix and D contract | PARTIALLY_COMPLIANT | D authority documented; enforce all bypass/write paths and atomic publication in implementation |
| PR-05 Memory Context Management | component map names G MCM and sync | PARTIALLY_COMPLIANT | Need owner baseline and end-to-end operation conformance |
| PR-06 Managed Region Ownership | README says memory data never elevated; C/G/H boundary evidence incomplete | PARTIALLY_COMPLIANT | Protected region ownership and Adapter negative tests required |
| PR-07 Untrusted Memory | README principle; Phase 3 review notes design consistency but threat testing open | PARTIALLY_COMPLIANT | C/E/F/G/H/I threat model and adversarial conformance not evidenced |
| PR-08 Identity/Authorization | I candidate contract; H envelope candidate; B typed refs open | BLOCKED_BY_OPEN_DECISION | B/I/H joint decision and negative tests |
| PR-09 Evidence Integrity | README principle; E candidate lineage contract; B domain schema open | PARTIALLY_COMPLIANT | Schema decision, end-to-end lineage and conflict tests required |
| PR-10 Forget Completeness | D/E contracts and Phase 3 CR-P1-01; F/G/H/I mapping open | BLOCKED_BY_OPEN_DECISION | D/E/Storage atomic gate plus F/G/H/I global proof and restore tests |
| PR-11 State Integrity | Phase 3 review distinguishes Accepted/Committed, suppression/cleanup/erasure, local/global ACK | PARTIALLY_COMPLIANT | Implemented state machines and cross-module negative tests absent |
| PR-12 Verification Integrity | Phase 2/3 reviews explicitly disclaim runtime, security and performance proof | COMPLIANT (reporting discipline only) | Must maintain in future acceptance reports |

## Evidence and limitations

- `main@8a6414158c9c056c1638222534e1993d1bbc99d2`: README blob `dfb5bf8a91f4a3ba29b14d623fbd2083f0273508`; system overview blob `995a1c5a3815d7e7b81b8d7f2ccc546c91d4c256`; component map blob `ddb7a1571463cadce83d89f62b03526c4f9693e8`; responsibility matrix blob `fbeb6935fe874e6c843c25c3a891d6b3242cbfd3`.
- `session-a-integration-2026-11-16`: contract registry blob `b15a87e9e259de74df600defbdd449772b9b3daa` (candidate coordination register).
- `session-d-memory-brain-2026-11-16`: Forget contract blob `1f0391bc49d007c44ec74165bd33d37412cc7990`; cursor semantics blob `4688a0ca487bf4d853c7f0220408abe8d743d159`.
- `session-e-memory-compiler-2026-11-16`: producer admission/publication contract blob `00e37ba56596e710513c8d0568acd79141d9101b`.
- `session-h-bmcp-protocol`: envelope/versioning blob `5547ecd78d118bd63e571e5daad87194d9b694e4`.
- `session-i-security-governance-2026-11-16`: Principal/ActorRef blob `03765efac4bb1153f303ce0030f9e277d602e81d`.
- Main Phase 2 review blob `3cd31abeac88703de5b9a0b29bea5d82cd5fdee7`; Phase 3 D/E/H/I review blob `edaccb802e0425f2d47bd4b613fab4dfde107144`.

A–C and F/G module-specific source documents were not all successfully retrieved by exact path in this pass. Their status is not inferred from absence; rows above are scoped to available project-level evidence and cross-module review. A complete branch-aware artifact inventory remains an OPEN follow-up before any final G0/G1 approval.
