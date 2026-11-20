# REQ-08 portable exchange fixture (development baseline)

This isolated Python 3.11+ reference fixture implements `ai-memory-portable-exchange/1.0` with two materially different local adapters: canonical JSON documents (`JsonFileAdapter`) and relational SQLite (`SQLiteAdapter`). It is not BMCP, a production service, or production security certification.

## Run

```sh
python3 experiments/req08-portable-exchange-fixture/portable_exchange.py demo
python3 experiments/req08-portable-exchange-fixture/portable_exchange.py migration-demo
python3 -m unittest discover -s experiments/req08-portable-exchange-fixture -p 'test_*.py' -v
python3 -m py_compile experiments/req08-portable-exchange-fixture/portable_exchange.py experiments/req08-portable-exchange-fixture/test_portable_exchange.py
```

The local test authority signs canonical grant claims with HMAC-SHA256 and verifies them against a pinned local issuer key. Grants bind issuer, tenant, workspace, agent, audience, resource, actions, expiry and delegation parent/chain. Revocation is checked at each operation. The HMAC key and authority are fixtures only; no production credential or key-management claim is made.

Both adapters implement the same versioned contract. `read`, `write`, `export`, `import_record`, and `share` authorize at their own boundaries. Import verifies contract version and payload digest before authorizing both `import` and `write`. Records preserve record/resource identity, source agent/provider/model, lineage, lifecycle and provenance. Forgotten records cannot be read/exported/shared; retracted records remain portable as a distinct lifecycle state.

## Round-trip and migration semantics

The conformance fixture asserts byte-identical canonical envelopes for JSON → SQLite → JSON export/import. Equality covers contract/schema version, record and resource identity, tenant/workspace, content, lifecycle, version, source identity/provider/model, lineage, provenance and timestamps. Provider substitution changes the adapter/storage provider but deliberately does not rewrite source attribution.

Schema migration is an explicit local v1 → v2 transformation adding `retention_class=standard`. Rollback requires retaining the exact pre-migration v1 envelope as a backup and restores it byte-for-byte after validating backup digest and shape. This is a reversible fixture migration, not an in-place production database migration.

## Security and scope

Tests cover signature/issuer validation, tenant/workspace/agent/audience/resource/action checks, expiry, revocation, bounded delegation, parent revocation, read/write/import/export/share boundaries, tampering, cross-tenant import and confused-deputy attempts. This is development-baseline evidence only; human expert security review is `OUT-OF-SCOPE(dev-baseline)`. Do not infer production security from these tests.

No CI result is claimed unless a real workflow run completes successfully. No BMCP contract, Rust production crate, production service, credential, external provider API, or production data is modified or used.
