#!/usr/bin/env python3
"""Build a legacy finding ledger from the baseline cohort and Git history."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CHECKER_PATH = ROOT / "scripts/ci/check_work_item_manifest_schema.py"

RULE_TEMPLATES = {
    "implementation.required_key": {
        "rationale": (
            "The implementation schema requires summary, files_changed, "
            "and tests. This finding originates from a manifest created "
            "before the current schema contract became effective. Retaining "
            "the missing implementation detail weakens traceability between "
            "the declared change, changed files, and verification evidence."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Populate every missing implementation key from the work-item "
            "README, implementation PR, committed diff, and verifiable test "
            "records. Completion requires all required keys to exist with "
            "the schema-defined types and the manifest to pass validation."
        ),
    },
    "top_level.documentation.required": {
        "rationale": (
            "The manifest schema requires a top-level documentation "
            "declaration. This finding predates enforcement of that "
            "requirement. Without documentation references, reviewers "
            "cannot reliably trace the work item's normative and design "
            "basis."
        ),
        "accountable_owner": "documentation-maintainer",
        "migration_plan": (
            "Identify existing authoritative documents and add repository-"
            "relative references with valid relationships. Completion "
            "requires the documentation field to satisfy the schema and "
            "every declared path to resolve in the Git tree."
        ),
    },
    "documentation.required": {
        "rationale": (
            "The AC4 contract requires documentation references. This "
            "finding belongs to the pre-enforcement historical cohort. "
            "Its retention weakens the ability to independently verify "
            "the documented basis and acceptance context of the work item."
        ),
        "accountable_owner": "documentation-maintainer",
        "migration_plan": (
            "Add at least the required authoritative documentation "
            "references using existing repository documents. Completion "
            "requires a non-empty valid documentation sequence and "
            "successful AC4 validation."
        ),
    },
    "top_level.evidence.required": {
        "rationale": (
            "The schema requires top-level evidence. This finding originates "
            "from a manifest predating the mandatory evidence contract. "
            "Missing evidence makes implementation and acceptance claims "
            "harder to independently reproduce."
        ),
        "accountable_owner": "evidence-maintainer",
        "migration_plan": (
            "Identify existing test reports, CI runs, or other verifiable "
            "artifacts and declare their repository references. Completion "
            "requires the evidence field to satisfy the schema and all "
            "referenced artifacts to exist."
        ),
    },
    "top_level.attribution.required": {
        "rationale": (
            "The schema requires attribution metadata. This finding "
            "predates mandatory attribution enforcement. Missing "
            "attribution weakens the audit trail for authorship and "
            "contributions."
        ),
        "accountable_owner": "governance-maintainer",
        "migration_plan": (
            "Recover attribution from explicit historical records and "
            "committed contribution metadata. Completion requires a "
            "schema-valid attribution declaration supported by verifiable "
            "source records."
        ),
    },
    "top_level.date.required": {
        "rationale": (
            "The schema requires a work-item date. This finding comes from "
            "a manifest created before the date requirement was enforced. "
            "Missing dates weaken chronological auditability and lifecycle "
            "reconstruction."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the declared work-item date from its original "
            "registration or authoritative issue history. Completion "
            "requires a valid date in the schema-defined representation."
        ),
    },
    "top_level.id_status.required": {
        "rationale": (
            "The schema requires id_status metadata. This historical "
            "finding predates enforcement of the identifier-status "
            "contract. Its absence weakens the ability to distinguish "
            "registered identifiers from unresolved or provisional ones."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Determine identifier status from the authoritative work-item "
            "registry and registration history. Completion requires a "
            "valid id_status value consistent with that record."
        ),
    },
    "top_level.acceptance_authority.required": {
        "rationale": (
            "The schema requires an explicit acceptance authority. This "
            "finding predates mandatory acceptance-authority declarations. "
            "Missing authority creates ambiguity about who can formally "
            "accept the work item's result."
        ),
        "accountable_owner": "governance-maintainer",
        "migration_plan": (
            "Recover the explicitly authorized acceptance authority from "
            "governance records or obtain a new explicit designation. "
            "Completion requires a verifiable authority declaration; "
            "the accountable owner must not be substituted automatically."
        ),
    },
    "top_level.session_evidence.required": {
        "rationale": (
            "The schema requires session evidence metadata. This finding "
            "originates from the historical pre-enforcement cohort. Missing "
            "session evidence weakens reconstruction of implementation "
            "decisions and verification activity."
        ),
        "accountable_owner": "evidence-maintainer",
        "migration_plan": (
            "Locate the original session evidence or produce a new "
            "verifiable evidence record without fabricating historical "
            "activity. Completion requires a schema-valid session_evidence "
            "declaration with resolvable references."
        ),
    },
    "session_evidence.required": {
        "rationale": (
            "The schema requires the session_evidence field. This finding "
            "predates its mandatory declaration. Its absence prevents "
            "reliable linkage between the work item and its recorded "
            "implementation sessions."
        ),
        "accountable_owner": "evidence-maintainer",
        "migration_plan": (
            "Locate an authentic session record or create a clearly dated "
            "replacement evidence record. Completion requires the required "
            "non-empty sequence and valid session references."
        ),
    },
    "implementation.status.enum": {
        "rationale": (
            "The schema restricts implementation.status to its declared "
            "enumeration. This finding comes from a pre-enforcement "
            "historical manifest. An unsupported value can cause different "
            "consumers to interpret implementation state inconsistently."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Map the existing status to a permitted value only when "
            "supported by the actual implementation state. Completion "
            "requires an allowed enum value and successful schema validation."
        ),
    },
    "top_level.base_commit_sha.required": {
        "rationale": (
            "The schema requires base_commit_sha. This finding predates "
            "mandatory baseline identification. Without a baseline commit, "
            "reviewers cannot reliably reconstruct the source state against "
            "which the work was developed."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the actual declared base commit from PR metadata or "
            "Git history. Completion requires a valid full commit SHA "
            "resolving to the intended historical baseline."
        ),
    },
    "top_level.risk_rationale.required": {
        "rationale": (
            "The schema requires an explanation supporting the declared "
            "risk level. This finding originates from the pre-enforcement "
            "cohort. Without justification, the risk classification cannot "
            "be independently evaluated."
        ),
        "accountable_owner": "governance-maintainer",
        "migration_plan": (
            "Obtain a documented risk assessment describing impact, "
            "likelihood, and relevant mitigations. Completion requires "
            "a substantive rationale consistent with the declared risk."
        ),
    },
    "top_level.base_branch.required": {
        "rationale": (
            "The schema requires base_branch. This finding predates "
            "mandatory branch-baseline declarations. Its absence weakens "
            "reproducibility of the work item's integration context."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the intended target branch from the original PR or "
            "authoritative work-item record. Completion requires a "
            "non-empty branch value consistent with the historical record."
        ),
    },
    "top_level.scope.required": {
        "rationale": (
            "The schema requires an explicit scope declaration. This "
            "finding originates from a manifest predating mandatory scope "
            "metadata. Missing scope makes it harder to establish which "
            "changes and responsibilities were actually covered."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the intended scope from the work-item specification "
            "and implementation record. Completion requires an explicit "
            "scope consistent with the recorded changes."
        ),
    },
    "top_level.implementation.required": {
        "rationale": (
            "The schema requires an implementation declaration. This "
            "finding predates mandatory implementation metadata. Its "
            "absence weakens traceability between the work-item objective "
            "and its implementation state."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Construct the implementation declaration from the actual "
            "work-item and implementation records. Completion requires "
            "a schema-valid implementation mapping."
        ),
    },
    "implementation.required": {
        "rationale": (
            "The implementation contract requires an implementation "
            "mapping. This historical finding predates enforcement of "
            "that contract. Without the mapping, implementation status "
            "and verification details cannot be consistently inspected."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Add the implementation mapping using verified implementation "
            "records. Completion requires a mapping containing every "
            "schema-required implementation key."
        ),
    },
    "top_level.repository.required": {
        "rationale": (
            "The schema requires repository metadata. This finding "
            "originates from the historical cohort before that field "
            "became mandatory. Missing repository identification weakens "
            "the ability to establish the authoritative source of changes."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the canonical repository identifier from the "
            "work-item registration and PR history. Completion requires "
            "a valid repository declaration matching the actual project."
        ),
    },
    "top_level.class.required": {
        "rationale": (
            "The schema requires a work-item class. This finding predates "
            "mandatory classification. Without classification, governance "
            "and review processes cannot reliably distinguish different "
            "kinds of work."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Classify the work item using its declared objective and "
            "the repository's classification policy. Completion requires "
            "a valid class value supported by the work-item content."
        ),
    },
    "top_level.sponsor.required": {
        "rationale": (
            "The schema requires sponsor metadata. This finding predates "
            "mandatory sponsor declarations. Missing sponsorship weakens "
            "traceability of the organizational mandate for the work."
        ),
        "accountable_owner": "governance-maintainer",
        "migration_plan": (
            "Recover an explicit sponsor designation from authoritative "
            "governance records or obtain a new designation. Completion "
            "requires a verifiable sponsor; authorship must not be used "
            "as a substitute."
        ),
    },
    "top_level.risk.required": {
        "rationale": (
            "The schema requires a risk classification. This finding "
            "originates from a manifest created before mandatory risk "
            "classification. Without it, reviewers cannot consistently "
            "assess the work item's exposure."
        ),
        "accountable_owner": "governance-maintainer",
        "migration_plan": (
            "Perform or recover a documented risk assessment and assign "
            "a permitted risk value. Completion requires consistency "
            "between the classification and its risk rationale."
        ),
    },
    "top_level.status.required": {
        "rationale": (
            "The schema requires lifecycle status. This finding predates "
            "mandatory lifecycle declarations. Missing status makes it "
            "difficult to determine whether the work item is proposed, "
            "active, completed, or otherwise governed."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the current lifecycle state from authoritative "
            "work-item and PR records. Completion requires a valid status "
            "consistent with the recorded lifecycle."
        ),
    },
    "top_level.accountable_owner.required": {
        "rationale": (
            "The schema requires an accountable owner. This finding "
            "predates mandatory ownership declarations. Missing ownership "
            "creates uncertainty about who is responsible for follow-up "
            "and maintenance."
        ),
        "accountable_owner": "governance-maintainer",
        "migration_plan": (
            "Obtain an explicit owner designation from the responsible "
            "governance authority. Completion requires a named or formally "
            "recognized accountable role supported by an ownership record."
        ),
    },
    "top_level.work_item_id.required": {
        "rationale": (
            "The schema requires work_item_id. This finding predates "
            "mandatory identifier declarations. Without an explicit "
            "identifier, the manifest cannot be reliably correlated with "
            "its registry and governance records."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the canonical identifier from the work-item directory "
            "and authoritative index. Completion requires exact agreement "
            "between work_item_id, directory identity, and registry entry."
        ),
    },
    "session_evidence.ref.pattern": {
        "rationale": (
            "The schema restricts session evidence references to an "
            "approved filename pattern or exact allowlist. This finding "
            "predates enforcement of that naming contract. Invalid "
            "references can prevent automated discovery of evidence."
        ),
        "accountable_owner": "evidence-maintainer",
        "migration_plan": (
            "Correct the reference to an existing evidence file whose "
            "basename satisfies the pinned pattern or exact allowlist. "
            "Completion requires successful path resolution and schema "
            "validation."
        ),
    },
    "session_evidence.kind.nonempty_sequence": {
        "rationale": (
            "The schema requires session_evidence to be a non-empty "
            "sequence. This finding predates mandatory sequence validation. "
            "An empty or incorrectly shaped value provides no usable "
            "session traceability."
        ),
        "accountable_owner": "evidence-maintainer",
        "migration_plan": (
            "Recover authentic session evidence and represent it as the "
            "required non-empty sequence of mappings. Completion requires "
            "all required record fields and references to validate."
        ),
    },
    "top_level.title.required": {
        "rationale": (
            "The schema requires a work-item title. This finding originates "
            "from the historical pre-enforcement cohort. Without a title, "
            "human reviewers and automated reports have reduced ability "
            "to identify the purpose of the work item."
        ),
        "accountable_owner": "work-item-maintainer",
        "migration_plan": (
            "Recover the original title from the authoritative issue or "
            "work-item README. Completion requires a non-empty title that "
            "accurately represents the declared objective."
        ),
    },
}


REQUIRED_RULE_IDS = frozenset({
    "documentation.required",
    "implementation.required",
    "implementation.required_key",
    "implementation.status.enum",
    "session_evidence.kind.nonempty_sequence",
    "session_evidence.ref.pattern",
    "session_evidence.required",
    "top_level.acceptance_authority.required",
    "top_level.accountable_owner.required",
    "top_level.attribution.required",
    "top_level.base_branch.required",
    "top_level.base_commit_sha.required",
    "top_level.class.required",
    "top_level.date.required",
    "top_level.documentation.required",
    "top_level.evidence.required",
    "top_level.id_status.required",
    "top_level.implementation.required",
    "top_level.repository.required",
    "top_level.risk.required",
    "top_level.risk_rationale.required",
    "top_level.scope.required",
    "top_level.session_evidence.required",
    "top_level.sponsor.required",
    "top_level.status.required",
    "top_level.title.required",
    "top_level.work_item_id.required",
})


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_work_item_manifest_schema", CHECKER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load checker: {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="strict",
    )
    return result.stdout.strip()


def load_cohort(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read cohort {path}: {exc}") from exc

    required = {"baseline_commit", "baseline_tree", "manifest_paths"}
    missing = sorted(required - payload.keys())
    if missing:
        raise ValueError(f"cohort missing required keys: {', '.join(missing)}")

    paths = payload["manifest_paths"]
    if not isinstance(paths, list) or not all(
        isinstance(item, str) and item for item in paths
    ):
        raise ValueError("cohort manifest_paths must be a list of paths")

    return payload


def validate_templates(required_rule_ids=None) -> None:
    checker = load_checker()

    # Validate against the actual rule IDs required by this build.
    # LEDGER_PLACEHOLDERS is a field-name -> draft-text mapping,
    # not a collection of rule IDs.
    if required_rule_ids is None:
        required_rule_ids = set(RULE_TEMPLATES)

    required = set(required_rule_ids)
    missing = sorted(required - set(RULE_TEMPLATES))
    if missing:
        raise ValueError(
            "missing RULE_TEMPLATES for rule_id(s): " + ", ".join(missing)
        )

    for rule_id in sorted(required):
        template = RULE_TEMPLATES[rule_id]
        for field in ("rationale", "accountable_owner", "migration_plan"):
            value = template.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"RULE_TEMPLATES[{rule_id!r}] "
                    f"missing non-empty {field}"
                )
            if value == checker.LEDGER_PLACEHOLDERS[field]:
                raise ValueError(
                    f"RULE_TEMPLATES[{rule_id!r}].{field} "
                    "uses the draft placeholder"
                )


def finding_key(checker, finding: dict[str, Any]) -> tuple[str, str, str]:
    identity = checker.finding_identity(finding)
    if not isinstance(identity, tuple) or len(identity) != 3:
        raise ValueError(f"invalid finding identity: {identity!r}")
    return identity


def finding_identities(checker, findings):
    if isinstance(findings, dict):
        return list(findings)
    return [finding_key(checker, finding) for finding in findings]


def collect_at_tree(checker, root, tree, manifest_path, schema):
    tree_paths = checker.git_tree_paths(root, tree)
    return checker.collect_findings(
        root, tree, [manifest_path], schema, tree_paths
    )


def find_resolution_commit(
    root: Path,
    baseline_commit: str,
    target_tree: str,
    manifest_path: str,
    rule_id: str,
    pointer: str,
):
    """
    Return the first chronological commit at which the finding is absent.

    A failed tree read, manifest parse, or finding collection is UNKNOWN,
    never proof of disappearance.
    """
    checker = load_checker()

    try:
        target_commit = git(root, "rev-parse", f"{target_tree}^{{commit}}")
        commits = git(
            root,
            "log",
            "--ancestry-path",
            "--reverse",
            "--format=%H",
            f"{baseline_commit}..{target_commit}",
            "--",
            manifest_path,
        ).splitlines()
        pinned_schema = checker.load_manifest_schema(root, target_tree)
    except Exception:
        return None

    wanted = (manifest_path, rule_id, pointer)

    for commit in commits:
        try:
            findings = collect_at_tree(
                checker, root, commit, manifest_path, pinned_schema
            )
            identities = set(findings)
        except Exception:
            # UNKNOWN: a failed read or parse is not evidence of absence.
            continue

        if wanted not in identities:
            return commit

    return None


def build_ledger(
    root: Path,
    target_tree: str,
    cohort_path: Path,
) -> dict[str, Any]:
    checker = load_checker()
    validate_templates(REQUIRED_RULE_IDS)
    cohort = load_cohort(cohort_path)

    baseline_commit = cohort["baseline_commit"]
    baseline_tree = cohort["baseline_tree"]
    manifest_paths = sorted(set(cohort["manifest_paths"]))

    if not manifest_paths:
        raise ValueError("cohort contains no manifest paths")

    schema = checker.load_manifest_schema(root, target_tree)
    baseline_tree_paths = checker.git_tree_paths(root, baseline_tree)
    target_tree_paths = checker.git_tree_paths(root, target_tree)

    baseline_findings = checker.collect_findings(
        root,
        baseline_tree,
        manifest_paths,
        schema,
        baseline_tree_paths,
    )
    # collect_findings returns {identity: finding}; identity[1] is rule_id.
    validate_templates(
        {
            identity[1]
            for identity in finding_identities(checker, baseline_findings)
        }
    )
    current_findings = checker.collect_findings(
        root,
        target_tree,
        manifest_paths,
        schema,
        target_tree_paths,
    )

    current_by_identity = (
        current_findings
        if isinstance(current_findings, dict)
        else {
            finding_key(checker, finding): finding
            for finding in current_findings
        }
    )

    entries = []
    for identity in finding_identities(checker, baseline_findings):
        manifest_path, rule_id, pointer = identity
        identity = (manifest_path, rule_id, pointer)
        canonical_id = checker.finding_id(identity)

        if identity in current_by_identity:
            template = RULE_TEMPLATES.get(rule_id)
            if template is None:
                raise ValueError(
                    f"missing RULE_TEMPLATES entry for rule_id={rule_id}"
                )

            entries.append(
                {
                    "finding_id": canonical_id,
                    "manifest_path": manifest_path,
                    "rule_id": rule_id,
                    "pointer": pointer,
                    "disposition": "OPEN",
                    "rationale": template["rationale"],
                    "accountable_owner": template["accountable_owner"],
                    "migration_plan": template["migration_plan"],
                    "resolution_commit": None,
                    "resolution_evidence": None,
                }
            )
            continue

        resolution_commit = find_resolution_commit(
            root,
            baseline_commit,
            target_tree,
            manifest_path,
            rule_id,
            pointer,
        )
        if not resolution_commit:
            raise RuntimeError(
                "cannot prove migrated finding: "
                f"manifest_path={manifest_path}, rule_id={rule_id}, "
                f"pointer={pointer}"
            )

        evidence = (
            f"Verified against Git tree at commit {resolution_commit}: "
            f"manifest {manifest_path} produces no finding with identity "
            f"(rule_id={rule_id}, pointer={pointer}) under the pinned "
            f"baseline schema."
        )

        entries.append(
            {
                "finding_id": canonical_id,
                "manifest_path": manifest_path,
                "rule_id": rule_id,
                "pointer": pointer,
                "disposition": "MIGRATED",
                "rationale": RULE_TEMPLATES[rule_id]["rationale"],
                "accountable_owner": RULE_TEMPLATES[rule_id]["accountable_owner"],
                "migration_plan": RULE_TEMPLATES[rule_id]["migration_plan"],
                "resolution_commit": resolution_commit,
                "resolution_evidence": evidence,
            }
        )

    payload = {
        "schema_version": 1,
        "baseline_commit": baseline_commit,
        "cohort": str(cohort_path.relative_to(root)).replace("\\", "/"),
        "generated_by": checker.LEDGER_GENERATED_BY,
        "entries": sorted(
            entries,
            key=lambda item: (
                item["manifest_path"],
                item["rule_id"],
                item["pointer"],
            ),
        ),
    }

    errors, _seen = checker.validate_ledger(
        payload,
        baseline_findings,
        current_findings,
        baseline_commit,
        payload["cohort"],
    )
    if errors:
        raise LedgerValidationError(errors)

    return payload


class LedgerValidationError(Exception):
    pass


def write_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(
                payload,
                stream,
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--tree", required=True)
    parser.add_argument(
        "--cohort",
        type=Path,
        default=ROOT
        / "14-ai-development/reports/work-item-legacy-cohort.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT
        / "14-ai-development/reports/work-item-legacy-ledger.json",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    root = args.root.resolve()
    cohort_path = args.cohort
    output_path = args.output

    if not cohort_path.is_absolute():
        cohort_path = root / cohort_path
    if not output_path.is_absolute():
        output_path = root / output_path

    if output_path.exists() and not args.force:
        print(
            f"ERROR: output already exists (use --force): {output_path}",
            file=sys.stderr,
        )
        return 2

    try:
        payload = build_ledger(root, args.tree, cohort_path)
    except LedgerValidationError as exc:
        print(f"LEDGER-VALIDATION-ERR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"BUILD-ERR: {exc}", file=sys.stderr)
        return 2

    try:
        write_atomic(output_path, payload)
    except OSError as exc:
        print(f"WRITE-ERR: {exc}", file=sys.stderr)
        return 1

    migrated = sum(
        entry["disposition"] == "MIGRATED" for entry in payload["entries"]
    )
    opened = sum(
        entry["disposition"] == "OPEN" for entry in payload["entries"]
    )
    accepted = sum(
        entry["disposition"] == "ACCEPTED_RISK"
        for entry in payload["entries"]
    )

    print(
        f"LEDGER-WRITTEN: {output_path} "
        f"(entries={len(payload['entries'])}, "
        f"MIGRATED={migrated}, OPEN={opened}, "
        f"ACCEPTED_RISK={accepted})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
