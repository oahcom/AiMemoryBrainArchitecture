# Phase 3.6.9 — H Exact-Version R1/R2 Wire Contract Disposition

- Role: H — BMCP Protocol Architect
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Scope: Recovery Cutoff Batch, owner snapshots/admission entries, COC ParticipantManifest, owner gate release and A §11/§12 schema mapping
- Provenance: **delegated role simulation authored in the coordinating ChatGPT session at the user's direction; not an independent human Owner signature or cryptographic attestation**
- Status: schema/documentation candidate only; NOT FROZEN / NOT INTEROPERABILITY-VERIFIED

## Exact review bundle

| Source | Blob |
|---|---|
| A Phase 3.6 architecture §§11–12 | `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d` |
| Storage Design v3.1 | `d5bdc72f193fcdaa654e4f07f865b77c578673ca` |
| COC protocol | `8ac17816476f280ab6fb3afca0688aa03e37de1d` |
| I Phase 3.6.8 amendment | `929b30ba10ac627927d3959e0777b467846b268d` |
| D Phase 3.6.8 amendment | `0668667daeb936bf223ab049277ea2a4117c3b09` |
| C Phase 3.6.9 amendment | `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb` |
| H recovery wire contract | `707ed85642ba4b0275c4ec851d599fde28ec6cae` |
| H recovery schema 1.0.3 | `9c3b98abab0c04a241a93c5e6f02e9424059b07b` |
| H JF-10 bridge schema 1.1.0 | `a8a945cc3623c2907003b93625e3c79742150944` |


## R1 — Recovery Cutoff wire model

H accepts the conceptual split in schema 1.0.3:
- separate request and admission member arrays, statuses, counts and roots;
- explicit COMPLETE_EMPTY distinct from NOT_ENUMERATED/PARTIAL/UNAVAILABLE/UNKNOWN;
- owner-specific secondary high-waters for I, D and C;
- exact quorum-confirmed COC prefix and typed participant entries;
- RecoveryCutoffBatch binding I/D/C owner snapshot refs/digests and ParticipantManifest;
- repeated immutable rounds for post-high-water changes.

H confirms the new recovery-cutoff schema supplements, and does not replace, the existing bmcp.applied-ack/1.1.0 JF-10 bridge schema. A §11 maps to recovery-cutoff; A §12 maps to JF-10 bridge. Cross-schema validation must bind the exact same participant tuple and terminal proofs.

## R2 — Owner gate release wire model

H accepts owner-signed gate-release attestations that bind owner kind, gate generation, RecoveryEpoch/round/batch, ParticipantManifest digest, snapshot digest, request/admission high-waters and roots, scope generation, anti-rollback anchor and final owner-local CAS proof reference.

COC may record the receipt but cannot issue, infer or substitute for an I/D/C owner release.

## Enumerated amendments / conditions

1. Schema 1.0.3 is structural only. Semantic validators must prove count equals array length, canonical member ordering/root, empty-set digest, uniqueness of owner entry and ParticipantIntentRef, exact prefix completeness and exact bidirectional join between owner entries and COC participant manifest.
2. RecoveryEpochCompleted must verify exactly the required I, D and C releases once each; a minItems constraint alone is insufficient.
3. Every owner-specific secondary high-water must be sourced from the named authoritative ledger and have a corresponding member-set/root or an explicit proof that the ledger is not applicable.
4. H must freeze deterministic canonical bytes, absent/null rules, duplicate-key handling, Unicode behavior, digest preimage and signature envelope only after I approves the security/cryptographic profile.
5. Cross-schema validator must enforce I COMMIT_WON → same participant/same-XID Storage COMMITTED, and I REVOCATION_WON / INDETERMINATE_ABORTED → same participant/same-XID Storage ROLLED_BACK; UNKNOWN/IN_DOUBT blocks release.
6. Positive/negative interoperability fixtures must cover stale schema, downgrade, wrong issuer/subject/audience/purpose, changed digest, replay, missing owner, empty-set substitution, missing prefix participant and mismatched participant tuple.

## H disposition

H's current schema and wire mapping are conditionally acceptable as a candidate with these amendments. This is not a schema freeze, cryptographic profile selection, canonical-byte interoperability PASS, runtime conformance or production activation.
