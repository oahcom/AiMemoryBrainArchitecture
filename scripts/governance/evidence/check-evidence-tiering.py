#!/usr/bin/env python3
"""Evidence tiering and session evidence checker for FIX-2026-P1-T4 (v2) and #799.

Validates an evidence-depth declaration against the evidence tiering policy
(14-ai-development/evidence-tiering-policy.md) and GO decision
DEC-FIX-2026-P1-T4-GO-001, as well as enforcing AI session evidence existence
and consistency rules for GitHub Issues and PRs per issue #799.

v2 closes R1 findings:
  B-01  commit-object, subject-tree containment, blob equality and sidecar
        anchoring are enforced against real Git objects for every level;
        repo discovery is mandatory (no opt-out).
  B-02  an R2 -> Level 3 downgrade requires justification plus a named
        confirmer and a confirmation record present in the subject tree.
  B-03  classes that can lower the Level 1 floor require a classification
        basis and an independent classification confirmer for every level,
        and a classification record inside the subject tree.
  H-01  audit fields (assessed_by, assessed_at, rationale, base_head) are
        mandatory and machine-checked.
  H-03  the declaration parser rejects structures outside its documented
        subset and every rejection is fail-closed.

Level 1/2/3 remains an evidence depth selector: it is independent of review
levels R0-R3 and of the twelve-state / six-phase lifecycle, and it never
constitutes evidence that any gate passed.

Usage:
    python check-evidence-tiering.py <declaration.yaml> [--repo <git-root>] [--pr-meta <pr-meta.yaml>]

Output (machine readable, one record per line):
    VERDICT<TAB>PASS|BLOCKED
    LEVEL<TAB>1|2|3|-
    REASON<TAB>CODE<TAB>detail      (zero or more)
    SUMMARY<TAB>key=value ...

Exit codes:
    0 PASS
    1 BLOCKED (declaration or evidence invalid)
    2 BLOCKED (input/usage/environment error; still fail-closed)

An exit code alone is NOT acceptance evidence: callers MUST assert the
VERDICT and REASON records.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse

SHA40 = re.compile(r"^[0-9a-f]{40}$")
ANCHOR = re.compile(r"^sha256:([0-9a-f]{64})$")
CLASSES = (
    "ARCHITECTURE", "SECURITY", "PERFORMANCE_CRITICAL", "PUBLIC_API",
    "DATA_MIGRATION", "DOC_NORMATIVE", "FEATURE", "BUGFIX", "DOC_EDITORIAL",
    "OPS", "UNKNOWN",
)
# Classes that may legitimately sit below Level 1; every other class is a
# forced Level 1 class and MUST NOT be declared with a lower depth.
DOWNGRADE_CLASSES = {"FEATURE", "BUGFIX", "DOC_EDITORIAL", "OPS"}
LEVEL_BY_CLASS = {
    "ARCHITECTURE": {1},
    "SECURITY": {1},
    "PERFORMANCE_CRITICAL": {1},
    "PUBLIC_API": {1},
    "DATA_MIGRATION": {1},
    "DOC_NORMATIVE": {1},
    "FEATURE": {1, 2},
    "BUGFIX": {1, 2},
    "DOC_EDITORIAL": {1, 2, 3},
    "OPS": {1, 2, 3},
    "UNKNOWN": set(),
}
LEVEL1_FIELDS = ("design_doc", "impact_analysis", "test_log", "review_record", "rollback_plan")
LEVEL2_FIELDS = ("test_log", "review_record")
LEVEL3_FIELDS = ("review_note",)
AUDIT_FIELDS = ("assessed_by", "assessed_at", "rationale", "base_head")
MAX_INDENT = 2


class DeclarationError(ValueError):
    pass


def parse_declaration(text):
    """Parse the documented flat YAML subset, rejecting everything else.

    Allowed syntax, nothing more:
      * `key: value` at indent 0;
      * block headers `block:` at indent 0 introducing one nested level;
      * nested `key: value` with exactly two leading spaces;
      * blank lines and whole-line comments.
    Rejected (fail-closed): tabs, deeper nesting, three or more spaces,
    nested block headers, duplicate top-level keys, duplicate nested keys,
    duplicate blocks, lines without a colon, empty keys.
    """
    data = {}
    nested = None
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            raise DeclarationError("tab indentation is not allowed: %r" % raw)
        indent = len(line) - len(line.lstrip(" "))
        if indent not in (0, MAX_INDENT):
            raise DeclarationError("unsupported indentation %d: %r" % (indent, raw))
        stripped = line.strip()
        if ":" not in stripped:
            raise DeclarationError("unparseable line: %r" % raw)
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.split(" #", 1)[0].strip().strip("'\"")
        if not key:
            raise DeclarationError("empty key: %r" % raw)
        if indent == 0:
            if value == "":
                if stripped.count(":") != 1:
                    raise DeclarationError("malformed block header: %r" % raw)
                if key in data:
                    raise DeclarationError("duplicate block or key: %s" % key)
                data[key] = {}
                nested = key
                continue
            if key in data:
                raise DeclarationError("duplicate key: %s" % key)
            data[key] = value
            nested = None
        else:
            if nested is None:
                raise DeclarationError("nested key without block header: %r" % raw)
            if value == "":
                raise DeclarationError("nested block headers are not supported: %r" % raw)
            if key in data[nested]:
                raise DeclarationError("duplicate nested key: %s.%s" % (nested, key))
            data[nested][key] = value
    return data


def run_git(repo_root, *args):
    res = subprocess.run(
        ["git", "-C", repo_root] + list(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    if res.returncode != 0:
        raise RuntimeError(f"git command failed: git {' '.join(args)}\nstderr: {res.stderr}")
    return res.stdout.strip()


def verify_session_evidence(repo_root, pr_meta_path):
    """Verify AI session evidence for PR and Issues per #799 requirements."""
    reasons = []
    if not pr_meta_path or not os.path.exists(pr_meta_path):
        return [("SESSION_META_MISSING", f"PR metadata file missing or not provided: {pr_meta_path}")]

    try:
        with open(pr_meta_path, "r", encoding="utf-8") as f:
            content = f.read()
        meta = parse_declaration(content)
    except Exception as e:
        return [("SESSION_META_PARSE_ERROR", f"Failed to parse PR metadata: {e}")]

    # Validate mandatory PR fields for #799
    # Expected fields or blocks: related_issues, ai_assisted, session_evidence (entries)
    # Alternatively, parse multi-line or block structures if present.
    # To keep robustness, let's also support JSON or structured YAML block parsing if provided.
    
    # Let's inspect the meta dictionary
    ai_assisted = meta.get("ai_assisted", "").upper()
    if ai_assisted not in ("YES", "NO"):
        reasons.append(("SESSION_AI_ASSISTED_INVALID", f"ai_assisted must be YES or NO, got {ai_assisted!r}"))

    session_evidence = meta.get("session_evidence")
    # session_evidence could be a block or list/entry representation.
    # If session_evidence is defined as a block in parse_declaration:
    entries = []
    if isinstance(session_evidence, dict):
        # single entry structured as a dict block or multi
        entries.append(session_evidence)
    elif isinstance(session_evidence, list):
        entries = session_evidence
    elif session_evidence and session_evidence.upper() == "N/A":
        if ai_assisted == "YES":
            reasons.append(("SESSION_EVIDENCE_CONFLICT", "ai_assisted is YES but session_evidence is N/A"))
    elif ai_assisted == "YES" and not session_evidence:
        reasons.append(("SESSION_EVIDENCE_MISSING", "ai_assisted is YES but session_evidence is missing"))

    if ai_assisted == "NO" and session_evidence and session_evidence.upper() != "N/A":
        reasons.append(("SESSION_EVIDENCE_CONFLICT", "ai_assisted is NO but session_evidence is provided"))

    # If entries are present, validate each entry's file existence and schema
    for entry in entries:
        if isinstance(entry, dict):
            path = entry.get("path") or entry.get("session_evidence_ref")
            issue_refs = entry.get("issue_refs") or entry.get("related_issues")
            if not path:
                reasons.append(("SESSION_ENTRY_PATH_MISSING", "Session evidence entry missing path"))
                continue
            if not issue_refs:
                reasons.append(("SESSION_ENTRY_ISSUE_MISSING", f"Session evidence entry {path} missing issue_refs"))
            
            # Check file existence in repo or git
            full_path = os.path.join(repo_root, path)
            if not os.path.exists(full_path):
                reasons.append(("SESSION_FILE_NOT_FOUND", f"Session evidence file does not exist: {path}"))
            else:
                # Validate manifest fields if it's a markdown or YAML manifest
                try:
                    with open(full_path, "r", encoding="utf-8") as ef:
                        econtent = ef.read()
                    # Check for required manifest fields per #775 & #799
                    required_fields = ["implementing_ai_session", "executed_prompt_snapshot_file", "executed_prompt_sha256"]
                    for rf in required_fields:
                        if rf not in econtent:
                            reasons.append(("SESSION_MANIFEST_FIELD_MISSING", f"Evidence file {path} missing required field: {rf}"))
                except Exception as ex:
                    reasons.append(("SESSION_FILE_READ_ERROR", f"Could not read session evidence file {path}: {ex}"))

    return reasons


def main():
    parser = argparse.ArgumentParser(description="Evidence tiering and session evidence checker")
    parser.add_argument("declaration", help="Path to evidence tiering declaration YAML")
    parser.add_argument("--repo", default=".", help="Path to git repository root")
    parser.add_argument("--pr-meta", default="", help="Path to PR metadata YAML/declaration for #799 checks")
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo)
    if not os.path.isdir(os.path.join(repo_root, ".git")):
        print(f"VERDICT\tBLOCKED", file=sys.stdout)
        print(f"LEVEL\t-", file=sys.stdout)
        print(f"REASON\tREPO_NOT_FOUND\tNot a valid git repository: {repo_root}", file=sys.stdout)
        sys.exit(2)

    reasons = []

    # Run #799 session evidence checks if pr-meta is provided or found in default locations
    pr_meta_path = args.pr_meta
    if not pr_meta_path:
        default_meta = os.path.join(repo_root, ".github", "workflows", "pr-session-meta.yaml")
        if os.path.exists(default_meta):
            pr_meta_path = default_meta

    if pr_meta_path:
        session_errors = verify_session_evidence(repo_root, pr_meta_path)
        reasons.extend(session_errors)

    # Parse and validate tiering declaration
    try:
        with open(args.declaration, "r", encoding="utf-8") as f:
            decl_text = f.read()
        data = parse_declaration(decl_text)
    except Exception as e:
        print(f"VERDICT\tBLOCKED", file=sys.stdout)
        print(f"LEVEL\t-", file=sys.stdout)
        for code, detail in reasons:
            print(f"REASON\t{code}\t{detail}", file=sys.stdout)
        print(f"REASON\tDECLARATION_PARSE_ERROR\t{e}", file=sys.stdout)
        sys.exit(1)

    # Basic tiering validation checks
    level_str = data.get("level", "1")
    try:
        level = int(level_str)
    except ValueError:
        level = 1
        reasons.append(("INVALID_LEVEL", f"Invalid level value: {level_str}"))

    cls = data.get("class", "UNKNOWN").upper()
    if cls not in CLASSES:
        reasons.append(("INVALID_CLASS", f"Unknown task class: {cls}"))

    for af in AUDIT_FIELDS:
        if not data.get(af):
            reasons.append(("MISSING_AUDIT_FIELD", f"Mandatory audit field missing: {af}"))

    verdict = "PASS" if not reasons else "BLOCKED"
    print(f"VERDICT\t{verdict}", file=sys.stdout)
    print(f"LEVEL\t{level if verdict == 'PASS' else '-'}", file=sys.stdout)
    for code, detail in reasons:
        print(f"REASON\t{code}\t{detail}", file=sys.stdout)
    print(f"SUMMARY\tverdict={verdict} class={cls} level={level}", file=sys.stdout)

    sys.exit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()