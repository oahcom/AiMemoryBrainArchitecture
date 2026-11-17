# H Owner — Exact Storage §14 Prepared-Participant Identity Wire Mapping Acceptance

- Exact Storage COC protocol Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- Exact A integration mapping Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- H schema candidate: `08-bmcp-protocol/schemas/bmcp.applied-ack-1.1.1-jf10-prepared-gid.schema.json`, Blob `c0bbfc7611a8d88a39cee209831db32b62601fde`
- Schema tests: `tests/schema/test_jf10_bridge_schema_1_1_1.py`, Blob `e92bbb16b85fe9727bcf0afa84868bbcc89c608c`
- Combined workflow: `.github/workflows/jf10-bridge-schema.yml`, Blob `01b93e7d5d7150cbeb0e39c46dfad2378be3ea10`
- CI run: `43964080044`; job `133638783610`; commit `576d86cef149110173f681a39cdc598e2ddafc4f`
- Result: **34/34 tests PASS** (1.1.0 schema + 1.1.1 schema + strict JSON parser)
- Decision: **ACCEPT WITH ENUMERATED H WIRE CONDITIONS — 1.1.1 CANDIDATE ONLY**
- Mode: delegated H-boundary review under user instruction; not independent human sign-off.

## 1. Canonical field mapping accepted

| H 1.1.1 field | Type / meaning | H constraint |
|---|---|---|
| `prepared_participant_ref` | PreparedParticipantRef | Stable opaque engine-neutral cross-service participant identity. |
| `prepared_transaction_gid` | PreparedTransactionGID | Client-chosen PostgreSQL GID; max 200 ASCII identifier chars; same value across intent, receipt, I terminal, resolution and reconciliation. |
| `engine_native_transaction_xid_ref` | EngineNativeTransactionXIDRef | Engine-assigned XID observed after PREPARE; opaque evidence, never preallocated or used as participant identity. |
| `postgres_system_identifier` | PostgreSQL cluster identity | Decimal string; bound to the canonical authority cluster. |
| `target_database_oid` | PostgreSQL database identity | Decimal string; bound to the target database. |
| `prepare_timeline` / `prepare_lsn` | Original prepare WAL location | Preserve original prepare timeline/LSN; recovery timeline/LSN is separate evidence. |
| `storage_signer_key_version` | Storage signer/key version | Required on Storage-signed prepared/resolution messages, alongside sender/audience/integrity/channel-binding evidence. |

H accepts the A mapping of legacy 1.1.0 fields as deprecated aliases only: `storage_participant_ref` → `prepared_participant_ref`; `storage_xid_ref` and `preallocated_storage_xid_ref` → `prepared_transaction_gid`; `storage_prepare_transaction_ref` → `engine_native_transaction_xid_ref`. If a legacy alias is present, the semantic verifier MUST require byte-identical equality with its canonical 1.1.1 field. New 1.1.1 producers SHOULD omit the deprecated aliases.

## 2. Message-family requirements

1. JF10_PREPARE_INTENT_REGISTERED requires PreparedParticipantRef + PreparedTransactionGID before Storage PREPARE; native XID is not yet available.
2. JF10_PREPARED_PARTICIPANT_REGISTERED requires the same stable pair, native XID observation, PostgreSQL system identifier, database OID, original prepare timeline/LSN and Storage signer key version.
3. I_JF10_TERMINAL_DECISION_OBSERVED binds the same stable pair and exact operation tuple; it does not treat native XID as I authorization.
4. STORAGE_JF10_PARTICIPANT_RESOLVED binds the same pair and native XID to same-GID COMMITTED/ROLLED_BACK proof and pointer/receipt or non-publication evidence.
5. JF10_BRIDGE_RECONCILIATION_RECORDED requires the stable pair; if Storage lookup state is PREPARED/COMMITTED/ROLLED_BACK, native XID and original prepare metadata are required.

## 3. Validation evidence

CI run `43964080044` succeeded on the exact schema/test branch revision. It reports 34 tests PASS across the previous 1.1.0 schema, the new 1.1.1 schema, and strict JSON parsing. The 1.1.1 suite verifies all five message variants, required stable identity fields, native-XID evidence, PostgreSQL metadata formats, GID constraints, legacy alias optionality and prepared-state reconciliation requirements.

## 4. H-owned limits and non-claims

- JSON Schema cannot enforce cross-message same-GID/same-participant consistency, GID uniqueness in a cluster/database, alias equality or Storage ledger lookup. Those require a semantic verifier and authoritative Storage state.
- No cryptographic signature algorithm, key custody, channel-binding implementation, issuer trust, replay-resistant transport or generated SDK is certified by these schema tests.
- H does not allocate PreparedParticipantRef/GID, decide Storage's reservation state, mint I authorization, establish D barrier membership or commit VisibilityPointer.
- PostgreSQL 18.7 is a candidate profile only. Other engines require their own stable prepared-handle and separately typed native transaction identity mapping.
- Schema 1.1.1 remains CANDIDATE / NOT PRODUCTION-FROZEN. Schema 1.1.0 remains available for its prior accepted message profile; 1.1.1 is an additive versioned candidate, not a silent in-place reinterpretation.

## 5. Decision

H accepts the exact Storage §14 field/type mapping and A integration mapping at the BMCP wire-schema boundary, with the conditions above. This does not constitute overall protocol acceptance by I/D/C/E/G/B/A/Storage or implementation conformance. JF-10 runtime P0 remains OPEN; no production activation is authorized.