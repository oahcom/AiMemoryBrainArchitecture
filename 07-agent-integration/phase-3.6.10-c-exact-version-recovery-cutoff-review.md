# Phase 3.6.10 — C Exact-Version Re-review of Recovery Cutoff Semantics

- Role: C — Agent Integration / provider submit boundary
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: delegated role simulation in the coordinating ChatGPT session; not independent human Owner approval.
- Status: architecture only; NOT IMPLEMENTED / NOT CONFORMANCE-VERIFIED

## Exact review bundle

- A §§11–12: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Storage v3.1: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- COC protocol: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- I 3.6.8: `929b30ba10ac627927d3959e0777b467846b268d`
- D 3.6.8: `0668667daeb936bf223ab049277ea2a4117c3b09`
- C 3.6.9: `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb`
- H wire contract: `b4cae9c0c9121c27ea2933c029b83b3f4367672b`
- H schema 1.0.4: `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1`
- H semantic validator contract: `7e6f67518e476fe9798f23a87798c7a3eb352f3c`
- H JF-10 bridge schema 1.1.0: `a8a945cc3623c2907003b93625e3c79742150944`


C reaffirms its durable pre-COC admission ledger, C-local Gate and provider egress serialization in C 3.6.9. C accepts H schema 1.0.4 and the semantic validator contract as the correct recovery evidence model.

Conditions:
1. C owner snapshots must separately enumerate request and admission/reservation/provider-attempt sets with exact high-waters and COMPLETE_EMPTY evidence.
2. Every COC participant manifest entry must bind the exact C owner admission identity, operation/request digest, scope and prefix position.
3. The egress adapter must serialize the final send boundary against current CGateGeneration, I COMMIT_WON, D clearance, exact reservation and one-use attempt identity.
4. A reserved/queued/NOT_DISPATCHED attempt cannot send after gate close. A pre-close SENT_OR_AMBIGUOUS attempt is reconciled by the same provider idempotency key; lost ACK never authorizes retry-as-new.
5. Provider-specific same-key outcome lookup must be proven before activation. Generic exactly-once semantics are not assumed.
6. H semantic validators must bind owner entries bidirectionally to the exact COC prefix and JF-10 participant tuple; UNKNOWN blocks C release.

Disposition: C accepts the current design direction with these conditions. No C independent signature, provider adapter conformance, R1/R2 closure or production activation is claimed.
