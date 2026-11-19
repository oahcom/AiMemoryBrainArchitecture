#!/usr/bin/env python3
"""Evidence tiering checker for FIX-2026-P1-T4.

Validates an evidence-depth declaration against the evidence tiering policy
(14-ai-development/evidence-tiering-policy.md) and the GO decision
DEC-FIX-2026-P1-T4-GO-001.

Design constraints (GO Section 3):
  * Level 1/2/3 is an evidence depth selector, NOT a status axis.
  * Level 1 is mandatory for R3, security, authorization, data integrity,
    migration, public API and architecture-semantic changes.
  * R2 MUST NOT be auto-downgraded for small size.
  * Documentation changes that alter normative semantics MUST be escalated.
  * Every level keeps a full 40-hex SHA and a change summary.
  * UNKNOWN is always BLOCKED.
  * Evidence binding protocol v3 fields and authenticity checks are preserved.

Usage:
    python check-evidence-tiering.py <declaration.yaml> [--repo <git-root>]

Output (machine readable, one record per line):
    VERDICT<TAB>PASS|BLOCKED
    LEVEL<TAB>1|2|3|-
    REASON<TAB>CODE<TAB>detail      (zero or more)
    SUMMARY<TAB>key=value ...

Exit codes:
    0 PASS
    1 BLOCKED (declaration invalid, incomplete, or fails closed)
    2 BLOCKED (input unreadable / usage error; still fail-closed)

The exit code alone is NOT sufficient evidence: callers MUST assert the
VERDICT and REASON records, per GO Section 3 acceptance gates.
"""
import argparse
import os
import re
import subprocess
import sys

SHA40 = re.compile(r"^[0-9a-f]{40}$")

LEVEL1_CLASSES = {
    "ARCHITECTURE",
    "SECURITY",
    "PERFORMANCE_CRITICAL",
    "PUBLIC_API",
    "DATA_MIGRATION",
    "DOC_NORMATIVE",
}
CLASS_ALLOWED_LEVELS = {
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


def parse_declaration(text):
    """Parse the flat YAML subset used by evidence declarations.

    Supports `key: value`, quoted values, comments, and a single nested block
    introduced by `evidence:`. Nested keys are returned as `evidence.<key>`.
    Raises ValueError on structurally ambiguous input (fail-closed).
    """
    data = {}
    nested = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if stripped.endswith(":") and indent == 0:
            nested = stripped[:-1].strip()
            if nested in data:
                raise ValueError("duplicate block: %s" % nested)
            data[nested] = {}
            continue
        if ":" not in stripped:
            raise ValueError("unparseable line: %r" % raw)
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.split("#", 1)[0].strip().strip("'\"")
        if not key:
            raise ValueError("empty key: %r" % raw)
        if indent > 0:
            if nested is None:
                raise ValueError("indented key without block: %r" % raw)
            flat = "%s.%s" % (nested, key)
            if flat in data[nested]:
                raise ValueError("duplicate key: %s" % flat)
            data[nested][key] = value
        else:
            if key in data:
                raise ValueError("duplicate key: %s" % key)
            data[key] = value
    return data


def flatten(decl):
    flat = {}
    for key, value in decl.items():
        if isinstance(value, dict):
            for sub, subval in value.items():
                flat["%s.%s" % (key, sub)] = subval
        else:
            flat[key] = value
    return flat


def check(decl, repo=None):
    """Return (verdict, level, reasons, summary)."""
    reasons = []
    flat = flatten(decl)

    def block(code, detail):
        reasons.append((code, detail))

    change_class = flat.get("change_class", "").strip().upper()
    review_level = flat.get("review_level", "").strip().upper()
    raw_level = flat.get("evidence_level", "").strip()
    subject_head = flat.get("subject_head", "").strip()
    summary_text = flat.get("change_summary", "").strip()
    authenticity = flat.get("source_authenticity", "").strip().upper()

    # (1) Missing evidence level declaration.
    if not raw_level:
        block("CE_NO_LEVEL", "evidence_level is absent; every change MUST declare depth")
    if raw_level and raw_level not in ("1", "2", "3"):
        block("CE_BAD_LEVEL", "evidence_level=%r is not one of 1/2/3" % raw_level)

    # (4) UNKNOWN classification must never receive a level.
    if not change_class:
        block("CE_NO_CLASS", "change_class is absent")
    elif change_class == "UNKNOWN":
        block("CE_UNKNOWN_CLASS", "UNKNOWN classification is BLOCKED; no level may be assigned")
    elif change_class not in CLASS_ALLOWED_LEVELS:
        block("CE_BAD_CLASS", "change_class=%r is not a recognized class" % change_class)

    # (2) Level/risk conflicts.
    if raw_level in ("1", "2", "3") and change_class in CLASS_ALLOWED_LEVELS:
        allowed = CLASS_ALLOWED_LEVELS[change_class]
        if allowed and int(raw_level) not in allowed:
            block("CE_LEVEL_CLASS_CONFLICT",
                  "%s requires evidence level %s, declaration says %s"
                  % (change_class, sorted(allowed), raw_level))
    if review_level == "R3" and raw_level in ("2", "3"):
        block("CE_R3_DOWNGRADE", "R3 changes are always Level 1 (declaration says %s)" % raw_level)
    if review_level == "R2" and raw_level == "3":
        if not flat.get("downgrade_justification", "").strip():
            block("CE_R2_AUTO_DOWNGRADE",
                  "R2 MUST NOT be auto-downgraded to Level 3 without an explicit justification")
    if not review_level:
        block("CE_NO_REVIEW_LEVEL", "review_level is absent")
    elif review_level not in ("R0", "R1", "R2", "R3"):
        block("CE_BAD_REVIEW_LEVEL", "review_level=%r is not one of R0/R1/R2/R3" % review_level)

    # (6) SHA format/length.
    if not subject_head:
        block("CE_NO_SUBJECT_HEAD", "subject_head (40-hex commit) is required at every level")
    elif not SHA40.match(subject_head):
        block("CE_BAD_SHA", "subject_head=%r is not a 40-character lowercase hex SHA" % subject_head)
    elif repo:
        kind = subprocess.run(["git", "-C", repo, "cat-file", "-t", subject_head],
                              capture_output=True, text=True)
        if kind.returncode or kind.stdout.strip() != "commit":
            block("CE_BAD_SUBJECT", "subject_head %s is not a commit object in %s" % (subject_head, repo))
    if not summary_text:
        block("CE_NO_SUMMARY", "change_summary is required at every level")

    # (3) Required fields per level.
    if raw_level == "1":
        for field in LEVEL1_FIELDS:
            if not flat.get("evidence.%s" % field, "").strip():
                block("CE_L1_MISSING_FIELD", "Level 1 requires evidence.%s" % field)
    elif raw_level == "2":
        for field in LEVEL2_FIELDS:
            if not flat.get("evidence.%s" % field, "").strip():
                block("CE_L2_MISSING_FIELD", "Level 2 requires evidence.%s" % field)
    elif raw_level == "3":
        for field in LEVEL3_FIELDS:
            if not flat.get("evidence.%s" % field, "").strip():
                block("CE_L3_MISSING_FIELD", "Level 3 requires evidence.%s" % field)

    # (5) v3 binding fields preserved for Level 1 and Level 2.
    if raw_level in ("1", "2"):
        if not flat.get("binding.protocol", "").strip():
            block("CE_NO_BINDING_PROTOCOL", "evidence binding protocol version (v3) is required")
        elif flat.get("binding.protocol", "").strip().lower() not in ("v3", "3"):
            block("CE_BAD_BINDING_PROTOCOL",
                  "binding.protocol=%r does not declare v3" % flat.get("binding.protocol"))
        if not flat.get("binding.subject_tree_contains_evidence", "").strip():
            block("CE_NO_BINDING_TREE", "binding.subject_tree_contains_evidence is required (v3)")
    if raw_level == "1" and not flat.get("binding.sidecar_anchor", "").strip():
        block("CE_NO_SIDECAR_ANCHOR", "Level 1 requires binding.sidecar_anchor per v3")

    # (7) Authenticity must never be passed silently as NOT_VERIFIED.
    if not authenticity:
        block("CE_NO_AUTHENTICITY", "source_authenticity is required")
    elif authenticity not in ("NOT_VERIFIED", "VERIFIED"):
        block("CE_BAD_AUTHENTICITY", "source_authenticity=%r is not NOT_VERIFIED/VERIFIED" % authenticity)
    elif authenticity == "VERIFIED":
        if not flat.get("authenticity.verification_record", "").strip():
            block("CE_UNFOUNDED_VERIFIED",
                  "VERIFIED claim without authenticity.verification_record is not acceptable")
    elif authenticity == "NOT_VERIFIED":
        if raw_level == "1" and flat.get("authenticity.acknowledged", "").strip().lower() not in ("true", "yes"):
            block("CE_AUTH_NOT_ACK",
                  "Level 1 with NOT_VERIFIED authenticity requires authenticity.acknowledged: true")

    level = raw_level if raw_level in ("1", "2", "3") else "-"
    summary = {
        "change_class": change_class or "-",
        "review_level": review_level or "-",
        "evidence_level": level,
        "subject_head": subject_head[:12] or "-",
        "reasons": str(len(reasons)),
    }
    return ("BLOCKED" if reasons else "PASS"), level, reasons, summary


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("declaration")
    parser.add_argument("--repo", default=None)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        print("VERDICT\tBLOCKED")
        print("REASON\tCE_USAGE\tinvalid arguments; fail-closed")
        return 2

    path = args.declaration
    if not os.path.isfile(path):
        print("VERDICT\tBLOCKED")
        print("REASON\tCE_INPUT_MISSING\tdeclaration not found: %s" % path)
        return 2
    try:
        with open(path, encoding="utf-8") as handle:
            decl = parse_declaration(handle.read())
        verdict, level, reasons, summary = check(decl, repo=args.repo)
    except ValueError as exc:
        print("VERDICT\tBLOCKED")
        print("REASON\tCE_UNPARSABLE\t%s" % exc)
        return 1
    except Exception as exc:  # defensive: any unexpected failure is fail-closed
        print("VERDICT\tBLOCKED")
        print("REASON\tCE_INTERNAL_ERROR\t%s: %s" % (type(exc).__name__, exc))
        return 2

    print("VERDICT\t%s" % verdict)
    print("LEVEL\t%s" % level)
    for code, detail in reasons:
        print("REASON\t%s\t%s" % (code, detail))
    print("SUMMARY\t" + "\t".join("%s=%s" % (k, v) for k, v in summary.items()))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
