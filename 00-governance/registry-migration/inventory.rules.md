<escape>---</escape>
<escape>document_metadata:</escape>
<escape>  steward: "Architecture Governance"</escape>
<escape>  domain: architecture</escape>
<escape>  role: design-specification</escape>
<escape></escape>
<escape>  lifecycle:</escape>
<escape>    approval:</escape>
<escape>      decision_status: Draft</escape>
<escape>      approver: null</escape>
<escape>      decision_date: null</escape>
<escape>      approved_version:</escape>
<escape>        scheme: git</escape>
<escape>        value: null</escape>
<escape>      approval_scope:</escape>
<escape>        type: Full-document</escape>
<escape>      approval_applicability: Applicable-To-Current-Version</escape>
<escape>      evidence_reference: []</escape>
<escape>      revocation: null</escape>
<escape></escape>
<escape>    evidence_verification:</escape>
<escape>      verification_status: Unverified</escape>
<escape>      last_verified_date: null</escape>
<escape>      last_verification_note: null</escape>
<escape></escape>
<escape>    usage_status: Active</escape>
<escape>    modification_status: Unchanged</escape>
<escape></escape>
<escape>    supersession:</escape>
<escape>      supersedes: []</escape>
<escape>      supersession_reason: null</escape>
<escape>      effective_date: null</escape>
<escape></escape>
<escape>    archival:</escape>
<escape>      archived_date: null</escape>
<escape>      archival_reason: null</escape>
<escape>      archival_reference: null</escape>
<escape></escape>
<escape>  authority:</escape>
<escape>    canonical_status: Non-Canonical</escape>
<escape>    canonical_scope: null</escape>
<escape>    canonical_scope_id: null</escape>
<escape>    canonical_scope_keywords: []</escape>
<escape>    canonical_conflict_status: None</escape>
<escape>    canonical_conflict_resolution: null</escape>
<escape>    normative_status: Normative</escape>
<escape>---</escape>

# Work-item Registry Migration Inventory Rules

## 1. Purpose

`00-governance/registry-migration/inventory.yaml` is the migration coverage register. It records which work items were discovered, their source manifest, their migration state, and the registry destination when one exists.

It is not a source of truth for title, owner, class, risk, status, prompt metadata, implementation, review, or acceptance.

## 2. Required document shape

```yaml
inventory_version: 1
source_tree: "561e9f24"
source_prefix: "14-ai-development/work-items/"
entries:
  - work_item_id: AID-2026-001
    source_manifest: "14-ai-development/work-items/AID-2026-001/manifest.yaml"
    migration_state: NOT_MIGRATED
    registry_path: null
```

The document must contain:

- `inventory_version`: integer `1`.
- `source_tree`: a Git commit or tree identifier fixed when the inventory is generated.
- `source_prefix`: exactly `14-ai-development/work-items/`.
- `entries`: one entry for every resolvable work-item identity discovered in the fixed source tree.

Each entry must contain:

- `work_item_id`
- `source_manifest`
- `migration_state`
- `registry_path`

`registry_path` is `null` for `NOT_MIGRATED`. For migrated states it must point to the corresponding canonical registry file. An excluded item must retain its exclusion evidence in the inventory entry.

## 3. Discovery and identity

The canonical discovery population is direct manifest paths:

```text
14-ai-development/work-items/<AID-or-FIX-directory>/manifest.yaml
```

Do not discover records by searching arbitrary YAML files for identity-looking keys. Do not include `authorization-manifest.yaml`.

Identity extraction supports exactly:

1. top-level `work_item_id`;
2. top-level legacy `aid`;
3. nested `work_item.proposed_id`, but only when the same `work_item` mapping contains `identifier_status: coordinator_verified_unique_see_identifier_evidence`.

The accepted identity grammar is:

```regex
^(?:AID-[0-9]{4}-[0-9]{3}|FIX-[0-9]{4}-[A-Z0-9]+(?:-[A-Z0-9]+)*)$
```

The directory name is a consistency check only. It must not be used to manufacture an identity when the manifest does not declare one.

If multiple supported declarations disagree, if a declaration is malformed, or if the manifest cannot be read or parsed, the item is `INCOMPLETE`. Do not silently omit it.

## 4. Allowed migration states

The only allowed `migration_state` values are:

- `NOT_MIGRATED`
- `MIGRATED`
- `MIGRATED_WITH_UNCONFIRMED_FIELDS`
- `EXCLUDED_BY_AUTHORITY`

Do not use `IN_PROGRESS`, `BLOCKED`, or any other value in place of these states.

### 4.1 State meanings

| State | Meaning | Required registry condition |
|---|---|---|
| `NOT_MIGRATED` | Discovered in the source tree; registry record has not been created | Registry file must not exist; `registry_path: null` |
| `MIGRATED` | Registry record has been created and passes schema validation | Exactly one registry file exists and passes schema |
| `MIGRATED_WITH_UNCONFIRMED_FIELDS` | Registry record exists; one or more fields are explicitly `UNCONFIRMED` | Exactly one registry file exists and passes schema; unresolved fields must be marked `UNCONFIRMED` |
| `EXCLUDED_BY_AUTHORITY` | An authorized decision explicitly excludes the work item | Registry file must not be required; entry must carry an authorization source reference and reason |

## 5. Validator state matrix

The validator must apply this matrix:

| Inventory state / observed condition | Validator result | Required code or interpretation |
|---|---|---|
| `NOT_MIGRATED` and registry file absent | `PASS` | Migration is incomplete by design; report it in coverage |
| `NOT_MIGRATED` but registry file exists | `VIOLATION` | `INVENTORY_REGISTRY_STATE_MISMATCH` |
| `MIGRATED` but registry file absent | `VIOLATION` | `MIGRATED_RECORD_MISSING` |
| `MIGRATED` and file exists but required fields are absent | `VIOLATION` | `SCHEMA_REQUIRED_FIELD_MISSING` |
| `MIGRATED_WITH_UNCONFIRMED_FIELDS` and unresolved fields are correctly marked | `PASS` | The record is structurally migrated; uncertainty remains explicit |
| `EXCLUDED_BY_AUTHORITY` without authorization evidence | `VIOLATION` | `EXCLUSION_UNAUTHORIZED` |
| Manifest identity discovered in source tree but no inventory entry exists | `VIOLATION` | `INVENTORY_ENTRY_MISSING` |
| Inventory identity has no corresponding source manifest and no authorized exclusion | `VIOLATION` | `INVENTORY_SOURCE_MISSING` |
| Source manifest cannot be read or its identity cannot be resolved | `INCOMPLETE` | Do not classify it as a missing work item |
| Two source manifests resolve to the same identity | `VIOLATION` | Duplicate identity; both source paths must be reported |
| Inventory contains duplicate identity entries | `VIOLATION` | Duplicate inventory identity |
| Inventory source tree does not match the validator's selected source tree | `INCOMPLETE` | Inventory is not valid for this tree |

## 6. Coverage invariants

Let:

```python
inventory_ids = all_valid_ids_discovered_from_legacy_manifests
registry_ids = all_ids_with_registry_records
not_migrated_ids = IDs whose state is NOT_MIGRATED
migrated_ids = IDs whose state is MIGRATED
migrated_unconfirmed_ids = IDs whose state is MIGRATED_WITH_UNCONFIRMED_FIELDS
excluded_ids = IDs whose state is EXCLUDED_BY_AUTHORITY
```

The validator must enforce:

```python
assert registry_ids <= inventory_ids
assert registry_ids.isdisjoint(unaccounted_duplicate_ids)

assert inventory_ids == (
    migrated_ids
    | migrated_unconfirmed_ids
    | not_migrated_ids
    | excluded_ids
)
```

Every identity must occur exactly once in the inventory. Every registry file must correspond to exactly one inventory identity. No inventory record may be silently discarded because its manifest or registry file is malformed.

A source manifest whose identity cannot be resolved is not part of a guessed `inventory_ids` set; it must instead produce an `INCOMPLETE` finding with its source path.

## 7. Fixed source tree and new work items

The inventory records the source tree used for its creation. It is not a permanent discovery snapshot.

When validating a later candidate tree:

1. Re-discover the canonical manifest population from that candidate tree.
2. Resolve identities using the supported declarations in §3.
3. Require every newly discovered identity to have exactly one inventory entry.
4. Require every inventory entry to resolve to a source manifest, unless it has a valid authorized exclusion.
5. Validate registry presence against the state matrix in §5.

A new manifest absent from the inventory is `INVENTORY_ENTRY_MISSING`, not implicitly `NOT_MIGRATED`.

## 8. Exclusion evidence

`EXCLUDED_BY_AUTHORITY` requires both:

- a source reference to the authorization record; and
- a non-empty reason identifying the authority and the exclusion decision.

A prose note without a verifiable source reference is insufficient. Migration tooling must not create this state automatically.

## 9. Coverage reporting and strict inventory

During progressive migration, the validator must report at least:

- discovered manifest count;
- resolvable identity count;
- inventory entry count;
- `NOT_MIGRATED` count;
- `MIGRATED` count;
- `MIGRATED_WITH_UNCONFIRMED_FIELDS` count;
- `EXCLUDED_BY_AUTHORITY` count;
- duplicate identity count;
- missing inventory entry count;
- inventory entries with missing source manifests;
- unreadable or unidentifiable source manifests.

A coverage percentage below 100% is not itself a schema violation during progressive migration.

`--strict-inventory` enforces the full inventory/source/registry relationship and fails on any `INCOMPLETE` or `VIOLATION` condition. It does not mean that every record must already be migrated. A correctly inventoried `NOT_MIGRATED` record is permitted until the migration cutover criteria are met.

## 10. Cutover condition

INDEX may not switch to a registry-derived projection until all of the following hold:

```text
migrated_count + authorized_excluded_count = discovered_count
not_migrated_count = 0
schema_failures = 0
duplicate_ids = 0
incomplete = 0
```

INDEX generation and verification are Stage D responsibilities:

```text
scripts/ci/generate_work_item_index.py
scripts/ci/check_work_item_index.py
```

The inventory validator must not generate INDEX or treat INDEX contents as field authority.
