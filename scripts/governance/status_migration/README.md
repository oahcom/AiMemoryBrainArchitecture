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

## Evidence schema and rollback integrity

A successful gate record must contain a structured `evidence` mapping, not
merely a non-empty reference. Required fields are:

- `verified`: `commands`, `environment`, `tested_head`,
  `expected_result`, `actual_result`, `logs`. The tested Head must equal
  the manifest's full `subject_head`.
- `independent_review`: `reviewer`, `implementer`, `reviewed_head`,
  `report`, `findings_disposition`. Reviewer and implementer must be
  different identities and the reviewed Head must equal `subject_head`.
- `integration`: `compatibility_result`, `registry_updates`,
  `integration_report`.
- `owner_acceptance`: `authority`, `decision`, `decision_record`.
- `merge`: `target_branch`, `merge_commit`, `merge_record`.
- `closeout`: `index_update`, `closeout_record`.

Empty values, placeholders, and fabricated `fake://`, `test://` or
placeholder references are rejected. The validator continues to require
sequential PASS dispositions through the source checkpoint; no phase
automatically passes a gate. YAML duplicate mapping keys are rejected.

The migrator preserves the original YAML text and comments by appending only
the new `lifecycle` block. It records the post-migration file SHA-256 in the
sibling `.post-status-migration.sha256` file. Rollback is refused unless the
current file hash exactly matches that recorded hash; edits made after
migration must be reviewed rather than overwritten by rollback.

## Evidence binding protocol (v3)

Path evidence fields (`logs`, `report`, `integration_report`,
`decision_record`, `merge_record`, `closeout_record`) are bound to the
attested subject through three checks, all fail-closed:

1. `subject_head` must resolve to a git **commit** object (`git cat-file -t`).
2. The evidence file must be a member of the subject commit's tree.
3. The working-tree bytes must equal the subject blob (`git show subject_head:path`).
   The git blob SHA-1 identity is therefore the cryptographic binding of
   evidence content to the attested subject.

Evidence files must additionally carry meaningful content: placeholder or
near-empty artifacts (shorter than 32 bytes, or matching known placeholder
strings) cannot satisfy a PASS gate.

Optionally, a manifest may record an independent content digest alongside a
path field as `<field>_sha256` (64-hex). When present, it must exactly match
the SHA-256 of the evidence bytes. This digest is advisory redundancy: the
authoritative binding remains the subject-tree blob identity.

## Sidecar trust boundary

`PR272-evidence-hardening.sha256` records git blob SHA-1s of the validator's
own protected source files. The most recent commit touching the sidecar must
embed the SHA-256 of the sidecar bytes in its commit message; the validator
re-verifies both on every run and fails closed on mismatch.

Threat model: this is an **auditable tamper-detection mechanism**, not a
digital signature or non-repudiation scheme. Silent local edits to protected
sources or the sidecar are detected. A bypass requires a fresh, visible
commit carrying a matching anchor, which remains in git history for audit.
It does not protect against an attacker who rewrites history and controls
the anchor, nor does it authenticate the committer's identity.

## Content integrity vs source authenticity (distinct concepts)

This validator proves **content integrity**: evidence bytes are exactly the
ones committed in the subject tree, bound by git object identity and optional
SHA-256 digests, and are not placeholder artifacts.

This validator does **not** prove **source authenticity**: whether the
evidence was genuinely produced by a trusted executor. Textual evidence
(even plausible-looking reports) cannot be authenticated without a signing
or trusted-CI infrastructure, which is out of scope for this tool.

Consequently, every manifest with a PASS gate must declare
`source_authenticity: NOT_VERIFIED`. Any other value — including a
self-declared `VERIFIED` — is rejected. The validator's PASS report always
carries `content_integrity: PASS` alongside
`source_authenticity: NOT_VERIFIED`; the two must never be conflated.
Upgrading authenticity requires a separately reviewed trust chain (trusted
CI identity binding or cryptographic signatures).
