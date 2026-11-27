#!/usr/bin/env python3
"""Evidence tiering checker for FIX-2026-P1-T4 (v2).

Validates an evidence-depth declaration against the evidence tiering policy
(14-ai-development/evidence-tiering-policy.md) and GO decision
DEC-FIX-2026-P1-T4-GO-001.

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
    python check-evidence-tiering.py <declaration.yaml> [--repo <git-root>]

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
                raise DeclarationError("indented key without block: %r" % raw)
            if value == "":
                raise DeclarationError("nested block header is not supported: %r" % raw)
            if key in data[nested]:
                raise DeclarationError("duplicate nested key: %s.%s" % (nested, key))
            data[nested][key] = value
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


def git(repo, *args):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")


def discover_repo(start):
    probe = start
    while True:
        root = git(probe, "rev-parse", "--show-toplevel")
        if root.returncode == 0 and root.stdout.strip():
            return root.stdout.strip()
        parent = os.path.dirname(probe)
        if parent == probe:
            return None
        probe = parent


def repo_slug(repo):
    """Return owner/name from the origin remote, or None if not allowlisted.

    Accepted origin forms, and nothing else:
      https://github.com/owner/repo[.git]   (no username, no port/query/fragment)
      ssh://git@github.com/owner/repo[.git] (username must be exactly git)
      git@github.com:owner/repo[.git]       (scp form, username must be git)

    The host is compared exactly after parsing; matching "github.com" anywhere
    in the URL string would let a path segment pass as GitHub.
    """
    url = git(repo, "config", "--get", "remote.origin.url").stdout.strip()
    if not url:
        return None
    slug = None
    scp = re.match(r"^([A-Za-z0-9._-]+)@([A-Za-z0-9.-]+):(.+)$", url)
    if scp and "://" not in url:
        if scp.group(1) == "git" and scp.group(2).lower() == "github.com":
            slug = scp.group(3)
    else:
        # A bare "?" or "#" parses to an empty query/fragment, so the raw URL
        # is inspected rather than the parsed fields alone.
        if "?" in url or "#" in url:
            return None
        try:
            parsed = urllib.parse.urlparse(url)
            scheme = parsed.scheme.lower()
            netloc = parsed.netloc
            # The authority is compared verbatim: an explicit empty port
            # ("github.com:"), any userinfo on HTTPS, or an empty password
            # separator on SSH is not the declared form even though urlparse
            # reports port/password as None.
            if (scheme == "https" and netloc.lower() == "github.com"
                    and not parsed.query and not parsed.fragment):
                slug = parsed.path
            elif (scheme == "ssh" and netloc.lower() == "git@github.com"
                    and not parsed.query and not parsed.fragment):
                slug = parsed.path
        except ValueError:
            # e.g. a non-numeric port; fail closed rather than raise.
            return None
    if not slug:
        return None
    path = slug.strip()
    if path.startswith("/"):
        path = path[1:]
    # Exactly owner/repo, optionally with a single .git suffix. Repeated or
    # empty segments and traversal are rejected rather than normalised away.
    if not re.match(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+?(?:\.git)?$", path):
        return None
    if ".." in path:
        return None
    if path.endswith(".git"):
        path = path[:-4]
    return path


def verify_path(repo, subject, path, label, block, codes):
    """Verify a declared path against the subject tree, worktree and blob."""
    not_in_subject, missing_worktree, blob_mismatch = codes
    if not SHA40.match(subject or ""):
        return
    in_tree = git(repo, "cat-file", "-e", "%s:%s" % (subject, path))
    if in_tree.returncode:
        block(not_in_subject, "%s=%s is not in the subject tree of %s"
              % (label, path, subject[:12]))
        return
    worktree_path = os.path.join(repo, path)
    if not os.path.isfile(worktree_path):
        block(missing_worktree, "%s=%s is not present in the working tree" % (label, path))
        return
    worktree_blob = git(repo, "hash-object", worktree_path)
    subject_blob = git(repo, "rev-parse", "%s:%s" % (subject, path))
    if (worktree_blob.returncode or subject_blob.returncode
            or worktree_blob.stdout.strip() != subject_blob.stdout.strip()):
        block(blob_mismatch, "%s working-tree bytes differ from subject blob" % label)


def check(decl, repo):
    reasons = []
    flat = flatten(decl)

    def block(code, detail):
        reasons.append((code, detail))

    change_class = flat.get("change_class", "").strip().upper()
    review_level = flat.get("review_level", "").strip().upper()
    raw_level = flat.get("evidence_level", "").strip()
    subject_head = flat.get("subject_head", "").strip()
    base_head = flat.get("base_head", "").strip()
    summary_text = flat.get("change_summary", "").strip()
    authenticity = flat.get("source_authenticity", "").strip().upper()

    # ---- level declaration -------------------------------------------------
    if not raw_level:
        block("CE_NO_LEVEL", "evidence_level is absent; every change MUST declare depth")
    elif raw_level not in ("1", "2", "3"):
        block("CE_BAD_LEVEL", "evidence_level=%r is not one of 1/2/3" % raw_level)
    level = raw_level if raw_level in ("1", "2", "3") else None

    # ---- classification ----------------------------------------------------
    if not change_class:
        block("CE_NO_CLASS", "change_class is absent")
    elif change_class == "UNKNOWN":
        block("CE_UNKNOWN_CLASS", "UNKNOWN is BLOCKED; no level may be assigned")
    elif change_class not in CLASSES:
        block("CE_BAD_CLASS", "change_class=%r is not a recognized class" % change_class)
    if not flat.get("classification_basis", "").strip():
        block("CE_NO_CLASSIFICATION_BASIS",
              "classification_basis is required: why this risk class applies")
    if change_class in DOWNGRADE_CLASSES:
        confirmer = flat.get("classification_confirmed_by", "").strip()
        record = flat.get("classification_record", "").strip()
        if not confirmer:
            block("CE_CLASS_UNCONFIRMED",
                  "%s lowers the Level 1 floor; classification_confirmed_by is required"
                  % change_class)
        elif confirmer == flat.get("assessed_by", "").strip():
            block("CE_CLASS_SELF_CONFIRMED",
                  "classification_confirmed_by MUST differ from assessed_by")
        if not record:
            block("CE_NO_CLASSIFICATION_RECORD",
                  "%s requires classification_record anchored in the subject tree"
                  % change_class)

    # ---- review level ------------------------------------------------------
    if not review_level:
        block("CE_NO_REVIEW_LEVEL", "review_level is absent")
    elif review_level not in ("R0", "R1", "R2", "R3"):
        block("CE_BAD_REVIEW_LEVEL", "review_level=%r is not one of R0/R1/R2/R3" % review_level)

    # ---- level / risk consistency -----------------------------------------
    if level and change_class in LEVEL_BY_CLASS:
        allowed = LEVEL_BY_CLASS[change_class]
        if allowed and int(level) not in allowed:
            block("CE_LEVEL_CLASS_CONFLICT",
                  "%s requires evidence level %s, declaration says %s"
                  % (change_class, sorted(allowed), level))
    if review_level == "R3" and level in ("2", "3"):
        block("CE_R3_DOWNGRADE", "R3 changes are always Level 1 (declaration says %s)" % level)
    if review_level == "R2" and level == "3":
        justification = flat.get("downgrade_justification", "").strip()
        confirmer = flat.get("downgrade_confirmed_by", "").strip()
        record = flat.get("downgrade_confirmation_record", "").strip()
        if not justification:
            block("CE_R2_AUTO_DOWNGRADE",
                  "R2 MUST NOT be auto-downgraded to Level 3 without an explicit justification")
        if not confirmer:
            block("CE_R2_DOWNGRADE_UNCONFIRMED",
                  "R2 -> Level 3 requires downgrade_confirmed_by")
        elif confirmer == flat.get("assessed_by", "").strip():
            block("CE_R2_DOWNGRADE_SELF_CONFIRMED",
                  "downgrade_confirmed_by MUST differ from assessed_by")
        if not record:
            block("CE_R2_DOWNGRADE_NO_RECORD",
                  "R2 -> Level 3 requires downgrade_confirmation_record in the subject tree")

    # ---- audit trail (H-01) ------------------------------------------------
    for field in AUDIT_FIELDS:
        if not flat.get(field, "").strip():
            block("CE_NO_AUDIT_FIELD", "audit field %s is required" % field)

    # ---- SHA fields --------------------------------------------------------
    if not subject_head:
        block("CE_NO_SUBJECT_HEAD", "subject_head (40-hex commit) is required at every level")
    elif not SHA40.match(subject_head):
        block("CE_BAD_SHA", "subject_head=%r is not a 40-character lowercase hex SHA" % subject_head)
    if base_head:
        if not SHA40.match(base_head):
            block("CE_BAD_BASE_HEAD", "base_head=%r is not a 40-character lowercase hex SHA" % base_head)
    if not summary_text:
        block("CE_NO_SUMMARY", "change_summary is required at every level")

    # ---- mandatory evidence fields per level -------------------------------
    required = ()
    if level == "1":
        required = LEVEL1_FIELDS
    elif level == "2":
        required = LEVEL2_FIELDS
    elif level == "3":
        required = LEVEL3_FIELDS
    for field in required:
        if not flat.get("evidence.%s" % field, "").strip():
            block("CE_L%s_MISSING_FIELD" % level, "Level %s requires evidence.%s" % (level, field))

    # ---- real Git verification (B-01) --------------------------------------
    if not repo:
        block("CE_NO_REPO",
              "a Git repository is required to verify evidence binding; none was found")
        return finish(reasons, level, change_class, review_level, subject_head)

    if subject_head and SHA40.match(subject_head):
        kind = git(repo, "cat-file", "-t", subject_head)
        if kind.returncode or kind.stdout.strip() != "commit":
            block("CE_BAD_SUBJECT", "subject_head %s is not a commit object in %s"
                  % (subject_head, repo))
        else:
            if base_head and SHA40.match(base_head):
                ancestor = git(repo, "merge-base", "--is-ancestor", base_head, subject_head)
                if ancestor.returncode != 0:
                    block("CE_BASE_NOT_ANCESTOR",
                          "base_head %s is not an ancestor of subject_head" % base_head)

    # Repository identity: the declaration MUST name the repository it was
    # assessed against, and that name MUST match the clone's origin remote.
    declared_repo = flat.get("repository", "").strip()
    if not declared_repo:
        block("CE_NO_REPOSITORY", "repository (owner/name) is required")
    else:
        slug = repo_slug(repo)
        if not slug:
            block("CE_REPO_IDENTITY_UNVERIFIED",
                  "origin remote is missing or not a GitHub URL; cannot verify %s" % declared_repo)
        elif slug.lower() != declared_repo.lower():
            block("CE_REPO_IDENTITY_MISMATCH",
                  "declared repository %s does not match origin %s" % (declared_repo, slug))

    protocol = flat.get("binding.protocol", "").strip().lower()
    if not protocol:
        block("CE_NO_BINDING_PROTOCOL", "binding.protocol is required at every level (v3)")
    elif protocol not in ("v3", "3"):
        block("CE_BAD_BINDING_PROTOCOL", "binding.protocol=%r does not declare v3" % protocol)

    # Every declared evidence path must exist in the subject tree and the
    # working-tree bytes must equal the subject blob. Governance confirmation
    # records are held to the same standard: a path string is not evidence.
    evidence_paths = dict((k.split(".", 1)[1], v) for k, v in flat.items()
                          if k.startswith("evidence.") and v)
    if level and not evidence_paths:
        block("CE_NO_EVIDENCE_PATHS", "no evidence paths declared for Level %s" % level)
    for name, path in sorted(evidence_paths.items()):
        verify_path(repo, subject_head, path, "evidence.%s" % name, block,
                    ("CE_EVIDENCE_NOT_IN_SUBJECT", "CE_EVIDENCE_MISSING_WORKTREE",
                     "CE_BLOB_MISMATCH"))

    for field, missing_code, codes in (
        ("classification_record", "CE_NO_CLASSIFICATION_RECORD",
         ("CE_CLASS_RECORD_NOT_IN_SUBJECT", "CE_CLASS_RECORD_MISSING_WORKTREE",
          "CE_CLASS_RECORD_BLOB_MISMATCH")),
        ("downgrade_confirmation_record", "CE_R2_DOWNGRADE_NO_RECORD",
         ("CE_DOWNGRADE_RECORD_NOT_IN_SUBJECT", "CE_DOWNGRADE_RECORD_MISSING_WORKTREE",
          "CE_DOWNGRADE_RECORD_BLOB_MISMATCH")),
    ):
        record = flat.get(field, "").strip()
        if record:
            verify_path(repo, subject_head, record, field, block, codes)
        elif field == "classification_record" and change_class in DOWNGRADE_CLASSES:
            block(missing_code, "%s requires %s anchored in the subject tree"
                  % (change_class, field))
        elif field == "downgrade_confirmation_record" and review_level == "R2" and level == "3":
            block(missing_code, "R2 -> Level 3 requires %s anchored in the subject tree" % field)

    # Level 1 additionally anchors a sidecar digests to the commit message.
    if level == "1":
        sidecar_path = flat.get("binding.sidecar_path", "").strip()
        anchor = flat.get("binding.sidecar_anchor", "").strip()
        if not sidecar_path:
            block("CE_NO_SIDECAR_PATH", "Level 1 requires binding.sidecar_path")
        if not anchor:
            block("CE_NO_SIDECAR_ANCHOR", "Level 1 requires binding.sidecar_anchor")
        elif not ANCHOR.match(anchor):
            block("CE_BAD_SIDECAR_ANCHOR",
                  "binding.sidecar_anchor=%r is not sha256:<64 hex>" % anchor)
        if sidecar_path and anchor and ANCHOR.match(anchor) and SHA40.match(subject_head):
            blob = git(repo, "show", "%s:%s" % (subject_head, sidecar_path))
            if blob.returncode:
                block("CE_SIDECAR_MISSING", "sidecar %s is not in the subject tree" % sidecar_path)
            else:
                digest = hashlib.sha256(blob.stdout.encode("utf-8", "surrogateescape")).hexdigest()
                if digest != ANCHOR.match(anchor).group(1):
                    block("CE_SIDECAR_MISMATCH",
                          "declared sidecar anchor %s does not match actual digest %s"
                          % (ANCHOR.match(anchor).group(1)[:12], digest[:12]))
                last = git(repo, "log", "-1", "--format=%H", subject_head, "--", sidecar_path)
                touched = last.stdout.strip()
                if last.returncode or not touched:
                    block("CE_SIDECAR_UNANCHORED",
                          "no commit touching %s found at %s" % (sidecar_path, subject_head[:12]))
                else:
                    message = git(repo, "log", "-1", "--format=%B", touched).stdout
                    if digest not in message:
                        block("CE_SIDECAR_UNANCHORED",
                              "commit %s does not carry the sidecar digest in its message"
                              % touched[:12])

    # ---- authenticity (unchanged boundary) --------------------------------
    if not authenticity:
        block("CE_NO_AUTHENTICITY", "source_authenticity is required")
    elif authenticity not in ("NOT_VERIFIED", "VERIFIED"):
        block("CE_BAD_AUTHENTICITY",
              "source_authenticity=%r is not NOT_VERIFIED/VERIFIED" % authenticity)
    elif authenticity == "VERIFIED":
        if not flat.get("authenticity.verification_record", "").strip():
            block("CE_UNFOUNDED_VERIFIED",
                  "VERIFIED claim without authenticity.verification_record is not acceptable")
    elif authenticity == "NOT_VERIFIED":
        if level == "1" and flat.get("authenticity.acknowledged", "").strip().lower() not in ("true", "yes"):
            block("CE_AUTH_NOT_ACK",
                  "Level 1 with NOT_VERIFIED authenticity requires authenticity.acknowledged: true")
    return finish(reasons, level, change_class, review_level, subject_head)


def finish(reasons, level, change_class, review_level, subject_head):
    summary = {
        "change_class": change_class or "-",
        "review_level": review_level or "-",
        "evidence_level": level or "-",
        "subject_head": subject_head[:12] or "-",
        "reasons": str(len(reasons)),
    }
    return ("BLOCKED" if reasons else "PASS"), level or "-", reasons, summary


def emit(verdict, level, reasons, summary):
    print("VERDICT\t%s" % verdict)
    print("LEVEL\t%s" % level)
    for code, detail in reasons:
        print("REASON\t%s\t%s" % (code, detail))
    print("SUMMARY\t" + "\t".join("%s=%s" % (k, v) for k, v in summary.items()))


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("declaration")
    parser.add_argument("--repo", default=None)
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        emit("BLOCKED", "-", [("CE_USAGE", "invalid arguments; fail-closed")],
             {"change_class": "-", "review_level": "-", "evidence_level": "-",
              "subject_head": "-", "reasons": "1"})
        return 2

    path = args.declaration
    if not os.path.isfile(path):
        emit("BLOCKED", "-", [("CE_INPUT_MISSING", "declaration not found: %s" % path)],
             {"change_class": "-", "review_level": "-", "evidence_level": "-",
              "subject_head": "-", "reasons": "1"})
        return 2
    repo = args.repo or discover_repo(os.path.dirname(os.path.abspath(path)))
    try:
        with open(path, encoding="utf-8") as handle:
            decl = parse_declaration(handle.read())
        verdict, level, reasons, summary = check(decl, repo)
    except DeclarationError as exc:
        emit("BLOCKED", "-", [("CE_UNPARSABLE", str(exc))],
             {"change_class": "-", "review_level": "-", "evidence_level": "-",
              "subject_head": "-", "reasons": "1"})
        return 1
    except Exception as exc:  # defensive: any unexpected failure is fail-closed
        emit("BLOCKED", "-", [("CE_INTERNAL_ERROR", "%s: %s" % (type(exc).__name__, exc))],
             {"change_class": "-", "review_level": "-", "evidence_level": "-",
              "subject_head": "-", "reasons": "1"})
        return 2
    emit(verdict, level, reasons, summary)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
