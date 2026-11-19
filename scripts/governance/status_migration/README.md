# Status migration tooling

Requires Python 3.10+ and PyYAML (install in an isolated environment with: python -m pip install PyYAML).

## Commands

Dry-run (default; no writes):
```sh
find 14-ai-development/work-items -name manifest.yaml -print0 | xargs -0 python scripts/governance/status_migration/migrate_status.py
```

Apply (creates a byte-for-byte sibling backup before writing):
```sh
python scripts/governance/status_migration/migrate_status.py --apply path/to/manifest.yaml
```

Validate sequential independent gates:
```sh
python scripts/governance/status_migration/check_status_gates.py path/to/manifest.yaml
```

Rollback to exact pre-migration bytes:
```sh
python scripts/governance/status_migration/migrate_status.py --rollback path/to/manifest.yaml
```

The migrator is intentionally conservative: unknown states, conflicting lifecycle metadata, missing status, and pre-existing backups block writes. The source status is retained verbatim. Gate records are initialized to NOT_RECORDED; the validator does not treat those placeholders as evidence. Fill a gate only with a real evidence reference and explicit PASS disposition. No repository-wide apply is authorized by this PR; run the dry-run inventory first, review every candidate, then apply only to an explicitly approved manifest set. Architecture decision records are excluded.

