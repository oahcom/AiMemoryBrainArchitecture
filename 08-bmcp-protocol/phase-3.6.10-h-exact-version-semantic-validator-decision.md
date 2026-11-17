# Phase 3.6.10 — H Exact-Version Semantic Validator Decision

- Role: H — BMCP Protocol Architect
- Decision: **ACCEPT WITH ENUMERATED AMENDMENTS**
- Provenance: **delegated role simulation authored in the coordinating ChatGPT session at the user's direction; not an independent human H Owner signature**
- Status: candidate wire/schema/validator specification only; NOT FROZEN / NOT IMPLEMENTED

## Exact bundle

- A §§11–12 Blob: `a3c51ec18f61dda46bb5e57d1155d1bcb2c7cc4d`
- Storage v3.1 Blob: `d5bdc72f193fcdaa654e4f07f865b77c578673ca`
- COC protocol Blob: `8ac17816476f280ab6fb3afca0688aa03e37de1d`
- I 3.6.8 Blob: `929b30ba10ac627927d3959e0777b467846b268d`
- D 3.6.8 Blob: `0668667daeb936bf223ab049277ea2a4117c3b09`
- C 3.6.9 Blob: `9609b252fc38fd5ba7b2f8c0992b7bd33a13c5bb`
- H recovery wire contract Blob: `b4cae9c0c9121c27ea2933c029b83b3f4367672b`
- H recovery schema 1.0.4 Blob: `d18b9ae1e2ed5e43ee5a78ac43b873b7d42230f1`
- H semantic validator contract Blob: `7e6f67518e476fe9798f23a87798c7a3eb352f3c`
- H JF-10 bridge schema 1.1.0 Blob: `a8a945cc3623c2907003b93625e3c79742150944`


## Accepted design

H accepts the 1.0.4 Recovery Cutoff schema direction and semantic validator contract:
- distinct owner request and admission sets, roots and high-waters;
- explicit COMPLETE_EMPTY separate from missing/partial/unavailable/unknown;
- I/D/C owner-specific high-water requirements;
- COC ParticipantManifest entries bound to an owner admission identity;
- immutable RecoveryCutoffBatch and repeated rounds;
- owner-only I/D/C outage-gate releases;
- RecoveryEpochCompleted as a COC observation only;
- A §11 recovery cutoff mapped separately from A §12 JF-10 bridge schema;
- same-participant/same-XID I terminal to Storage outcome mapping.

## Enumerated amendments / conditions

1. Implement the six semantic validators and RecoveryJoin composition described in the exact validator contract; JSON Schema parsing alone is not sufficient.
2. Prove array count equality, canonical ordering/root, empty-set root, uniqueness and complete pagination against authoritative owner/COC ledgers.
3. Prove bidirectional exact participant/owner-admission joins and ensure every affected participant has accountable I/D/C/Storage evidence.
4. Require exactly one current I, D and C release for the applicable scope before RecoveryEpochCompleted; reject duplicate or cross-scope releases.
5. Resolve the `OTHER` participant owner class through an explicit trusted owner registry; unknown/unregistered owner classes fail closed.
6. Freeze canonical bytes, digest preimage and signature envelope only after I approves the trust/cryptographic policy; no algorithm or key profile is selected by this H disposition.
7. Cross-schema vectors must prove I COMMIT_WON → same-XID Storage COMMITTED and I REVOCATION_WON/INDETERMINATE_ABORTED → same-XID Storage ROLLED_BACK; UNKNOWN/IN_DOUBT remains blocking.

## H disposition

H accepts the design as a candidate with these amendments. This does not freeze schema 1.0.4, select cryptography, prove interoperability, implement validators, close R1/R2 or authorize deployment/production activation.
