# AID-2026-099 — H Idempotency Namespace and Replay Boundary Candidate

Date: 2026-11-26
Requested scope: documentation-only candidate contract in canonical H protocol root plus EN and ZH-CN mirrors.
Required topics: per-authority/scope/operation idempotency namespace; producer-generated stable key; distinct Attempt ID per retry; deduplication horizon and durable receipt; H admission and Storage domain-effect linearization points; Unknown/Pending/Failed/Duplicate/Conflict semantics; crash recovery; C/G Applied join under AID-2026-091; D ForgetFence and I current authorization replay checks; Storage atomicity delegated to AID-2026-098 without duplication.
Every checkpoint must state PASS/FAIL and DOCUMENTED_ONLY or EVIDENCE_REQUIRED.
Keep status Draft/Candidate/Informative. Record unavailable exact AID-2026-098 source as unresolved, not invented.
Create AID-2026-099 as PROVISIONAL, Draft PR, and comments on #1212, #1208, #1135.
No runtime, validator, schema, test, workflow or deployment changes. Do not merge or close Issues. Do not claim Owner acceptance or implementation evidence.
