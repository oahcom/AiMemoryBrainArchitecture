# Status migration tooling

Requires Python 3.10+ and PyYAML.

## Exact source vocabulary

The migrator accepts only the twelve exact AI-STD-001 work-item states:
`PROPOSED`, `ANALYZED`, `PROMPT_READY`, `READY`, `IN_PROGRESS`,
`IMPLEMENTED`, `VERIFIED`, `REVIEWED`, `INTEGRATION_READY`,
`ACCEPTED`, `MERGED`, and `CLOSED`.

Decorated values (for example, `IN_PROGRESS — explanation`), unknown values,
missing values and ambiguous values fail closed. `BLOCKED` and `REJECTED`
are orthogonal markers and are preserved separately; they are not phases or
source-state aliases. Architecture-decision records are out of scope.

## Commands

Dry-run is the default and does not write files:

```sh
find 14-ai-development/work-items -name manifest.yaml -print0 |
  xargs -0 python scripts/governance/status_migration/migrate_status.py
```

Apply only to an explicitly reviewed exact-path set. Each file receives a
byte-for-byte sibling backup before atomic replacement:

```sh
python scripts/governance/status_migration/migrate_status.py --apply path/to/manifest.yaml
```

Validate independent gates (a phase never implies a gate passed):

```sh
python scripts/governance/status_migration/check_status_gates.py path/to/manifest.yaml
```

Rollback restores the exact original bytes from the sibling backup:

```sh
python scripts/governance/status_migration/migrate_status.py --rollback path/to/manifest.yaml
```

The migration is additive and idempotent. It preserves the original `status`
field and adds `lifecycle.phase`, `lifecycle.source_status`,
`lifecycle.gates` and `lifecycle.markers`. All gates initialize to
`NOT_RECORDED`; the validator requires real evidence references and explicit
`PASS` dispositions for every gate implied by the source checkpoint.

Run a complete inventory and dry-run first. Review every candidate and every
blocked result. Do not apply unknown/decorated statuses or architecture-decision
records. Never infer review, acceptance, integration, merge or closeout evidence.
