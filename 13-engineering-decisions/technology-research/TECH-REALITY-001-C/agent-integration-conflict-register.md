# Agent Integration Conflict Register / Agent 集成冲突登记

| ID | Level | Conflict / gap | Authority | Evidence | Closure condition | Gate |
|---|---|---|---|---|---|---|
| C-CON-001 | BLOCKING | Current main does not contain full Owner D/E/F/G/H/I contracts; branches are separate and exact currentness must be reconciled | A + each Owner | Main HEAD b3c666...; Owner branch pins in baseline | A-approved source pin manifest and each Owner exact-version adoption | C0/C5 |
| C-CON-002 | BLOCKING | H 1.2.15 candidate vs Storage v3.3.2 bundle pinned to H 1.2.14 | H/Storage/C/I/A | H schema Blob 860fc4...; Storage manifest 5c6143... | Successor manifest pins 1.2.15 exact schema, validator, CI and trust artifacts; all consumers review same bundle | C3/C5 |
| C-CON-003 | BLOCKING | C crypto profile and I governance signature profile not registered/deployed | I (trust policy), C (data signer), H (verification) | C Phase 3.11.0 Blob 9339b1... | I approval, key custody/rotation/revocation, anti-rollback checkpoints, H validator tests, operational evidence | C3/C5 |
| C-CON-004 | BLOCKING | G Applied freeze remains blocked and execution not verified | G; C/H/I/D supporting | G contract Blob aa3afa... | G-owned exact predicate, C final-request evidence, H wire/ACK, I authorization, D fence currentness and end-to-end tests | C5/C6 |
| C-CON-005 | HIGH | B Fact/Claim semantics ADR blocked; B research PR #55 is Draft and B0/B5 not passed | B + governance | PR #55 metadata; B domain overview Blob 4d1debc... | Formal B/governance ADR and downstream typed consumer mapping | C0/C5 |
| C-CON-006 | HIGH | Historical C branch diverges 167 ahead / 56 behind current main; its contracts cannot be treated as current main | C + A | Compare main...session-c; old C HEAD 71047... | Exact-source reconciliation and independent review; no blind merge | C0/C5 |
| C-CON-007 | HIGH | A research PR #45 is stale-base Draft; independent PR #56 says REVISE and A research remains NOT YET PROVEN | A | PR #45 base b372b... head 6c7c...; PR #56 | A remediates review findings and publishes current-main source pins; C consumes as candidate only | C0/C9 |
| C-CON-008 | HIGH | Provider capability parity not proven across OpenAI, Anthropic, Gemini, local and compatible endpoints | C | Official source evidence index; several provider docs not inspected | Per-provider versioned conformance matrix for stream/tool/error/cancel/usage/idempotency | C3/C6 |
| C-CON-009 | HIGH | Tool side-effect evidence and safe retry semantics are not standardized across arbitrary tools | I/tool runtime/C | Hermes and PydanticAI runtime docs; project contracts | I-approved capability/authorization model plus per-tool idempotency/effect evidence profile | C5/C6 |
| C-CON-010 | MEDIUM | Telemetry retention, attribute allowlist, data classification and export policy not approved | I/Observability | OTel context guidance; I governance register | I-approved classification/retention/export policy and redaction tests | C4/C6 |
| C-CON-011 | MEDIUM | Runtime/framework versions, licenses and Rust SDK/exporter compatibility not pinned | A/C | Official docs are moving; evidence index | Exact release/tag, license and dependency review | C6 |
| C-CON-012 | MEDIUM | No Brain end-to-end prototype or representative benchmarks executed | C/Testing/Runtime owner | Validation plan only | Reproducible test harness and measured outputs | C6 |

## Conflict handling / 冲突处理
BLOCKING items fail closed. C cannot resolve B/D/E/F/G/H/I/Storage authority conflicts by renaming fields, adding a parallel enum, or treating an author-side acceptance as Owner approval. Any change to exact Blob SHA invalidates reviews that pin the predecessor.
