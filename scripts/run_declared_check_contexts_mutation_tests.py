#!/usr/bin/env python3
"""Execute two real source mutations and prove the targeted tests turn red."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_declared_check_contexts.py"
TESTS = HERE / "test_check_declared_check_contexts.py"


def execute(label, method, original_source, mutated_source):
    with tempfile.TemporaryDirectory(prefix="declared-context-mutation-") as tmp:
        scripts = Path(tmp) / "scripts"
        scripts.mkdir()
        shutil.copyfile(TESTS, scripts / TESTS.name)
        (scripts / CHECKER.name).write_text(original_source, encoding="utf-8")
        command = [
            sys.executable, "-m", "unittest", "-v",
            f"test_check_declared_check_contexts.DeclaredCheckContextsTest.{method}",
        ]
        before = subprocess.run(command, cwd=scripts, text=True, capture_output=True)
        print(f"=== {label}: ORIGINAL (must pass) ===")
        print(f"$ {' '.join(command)}")
        print(f"raw_rc={before.returncode}")
        print(before.stdout, end="")
        print(before.stderr, end="")
        if before.returncode != 0:
            raise SystemExit(f"{label}: baseline test did not pass")

        (scripts / CHECKER.name).write_text(mutated_source, encoding="utf-8")
        # Source mutations can preserve byte length and filesystem timestamp
        # granularity; remove the baseline bytecode so Python cannot reuse it.
        shutil.rmtree(scripts / "__pycache__", ignore_errors=True)
        after = subprocess.run(command, cwd=scripts, text=True, capture_output=True)
        print(f"=== {label}: MUTATED (must fail) ===")
        print(f"$ {' '.join(command)}")
        print(f"raw_rc={after.returncode}")
        print(after.stdout, end="")
        print(after.stderr, end="")
        if after.returncode == 0:
            raise SystemExit(f"{label}: mutation survived; test is ineffective")


source = CHECKER.read_text(encoding="utf-8")
mutation_one = "required_not_declared = sorted(set(protection) - set(contexts))"
if source.count(mutation_one) != 1:
    raise SystemExit("mutation 1 anchor not unique")
execute(
    "MUTATION-1 required-minus-declared forced empty",
    "test_violation_when_the_platform_requires_more_than_the_document",
    source,
    source.replace(mutation_one, "required_not_declared = []", 1),
)

mutation_two = '''                f"{type(error).__name__}: {error}",
                file=sys.stderr,
            )
            return 2
'''
if source.count(mutation_two) != 1:
    raise SystemExit("mutation 2 anchor not unique")
execute(
    "MUTATION-2 INCOMPLETE exception return 2 changed to 0",
    "test_incomplete_when_the_payload_cannot_be_read",
    source,
    source.replace(mutation_two, mutation_two.replace("return 2", "return 0"), 1),
)

print("MUTATION TESTS: PASS (both mutations detected)")
