"""Regression: the complete self-check must finish under Windows symlink denial.

Both symlink entry points are patched in the child process. The child runs
main(), so this verifies the section-level failure boundary, all registered
symlink skips, the final summary, and the process exit status.
"""
import re
import subprocess
import sys
from pathlib import Path

HARNESS = r'''
import os
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t

def deny(*args, **kwargs):
    raise OSError(1314, "A required privilege is not held by the client")

with mock.patch.object(os, "symlink", side_effect=deny):
    with mock.patch.object(Path, "symlink_to", side_effect=deny):
        sys.exit(t.main())
'''

r = subprocess.run(
    [sys.executable, "-c", HARNESS],
    cwd=str(Path.cwd()),
    capture_output=True,
    text=True,
    encoding="utf-8",
    errors="replace",
)

lines = (r.stdout or "").splitlines()
summaries = [line for line in lines if re.fullmatch(r"\d+/\d+ passed", line)]
skip_summaries = [
    line for line in lines
    if line.startswith("13 skipped, 13 registered of 13 allowed:")
]

expected_skips = (
    "T36 directory symlink is rejected as a governed root",
    "T37 governed_files does not descend into a symlinked root",
    "T41 symlinked governed file is rejected",
    "T42 governed file reached through a symlinked parent is rejected",
    "T49 symlinked backlog root is named in the diagnostic",
    "T50 symlinked directory inside a backlog root is reported",
    "T51 symlinked markdown file inside a backlog root is reported",
    "T51b symlinked bilingual mirror directory is refused by name",
    "T58 symlinked subdirectory in a normative root is reported",
    "T59 top-level symlink is reported and does not satisfy the registry",
    "T60 declared directory that is only a symlink is reported",
    "T128 DM-14 a symlinked mirror directory is named",
)

summary_ok = summaries == ["359/359 passed"]
skip_summary_ok = (
    len(skip_summaries) == 1
    and all(name in skip_summaries[0] for name in expected_skips)
    and "T68c a real 0o000 directory is reported by path (integration)"
    in skip_summaries[0]
)

ok = (
    r.returncode == 0
    and summary_ok
    and skip_summary_ok
)

print("FULL_SUITE_EXIT:", r.returncode)
print("FULL_SUITE_SUMMARIES:", summaries)
print("FULL_SUITE_SKIP_SUMMARY_COUNT:", len(skip_summaries))
print("FULL_SUITE_ALL_12_SYMLINK_SKIPS:", all(
    name in (skip_summaries[0] if skip_summaries else "")
    for name in expected_skips
))
print("FULL_SUITE_VERDICT:", "PASS" if ok else "FAIL")

if not ok:
    print("--- child stdout tail ---")
    print("\n".join(lines[-50:]))
    print("--- child stderr tail ---")
    print("\n".join((r.stderr or "").splitlines()[-30:]))

sys.exit(0 if ok else 1)
