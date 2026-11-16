# H Phase 3.6.4 — PreparedParticipantRef / PreparedTransactionGID Schema 1.1.1 Evidence

- Storage protocol §14 Blob: `86ff3b247d7565a0dcd1f2e4ed21b5ba70a6b0d7`
- A identity mapping addendum Blob: `a71251704851cacd15f67faa985a5bd50057e92a`
- H schema 1.1.1 Blob: `c0bbfc7611a8d88a39cee209831db32b62601fde`
- H 1.1.1 test Blob: `e92bbb16b85fe9727bcf0afa84868bbcc89c608c`
- Strict parser Blob: `3b9b3da645448c773c95a9dcd3c57c8c109bb2da`
- CI run `43964080044`, job `133638783610`, commit `576d86cef149110173f681a39cdc598e2ddafc4f`
- Result: **34/34 tests PASS**

Schema 1.1.1 separates stable PreparedParticipantRef, client-chosen PreparedTransactionGID and engine-assigned native transaction XID. It requires PostgreSQL cluster/database identity, original prepare timeline/LSN and Storage signer key version on prepared/resolved evidence. Legacy 1.1.0 aliases are optional/deprecated.

The combined suite validates 1.1.0 and 1.1.1 schemas, all five message families, required fields, conditional D/I/Storage proof shapes, GID format, native XID separation, PostgreSQL metadata formats, old-version rejection, duplicate-key rejection, invalid UTF-8, non-finite values, message size/depth limits and unknown critical extension handling.

Limits: schema/reference-parser tests do not prove same-GID consistency across actual messages, GID uniqueness in the DB, alias equality at runtime, cryptographic signatures, channel binding, issuer trust, replay-resistant transport, generated SDK interoperability or live owner-service integration. No production freeze.