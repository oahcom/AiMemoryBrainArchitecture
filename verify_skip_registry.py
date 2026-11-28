"""Negative tests for skip registration, exact reasons, and harness diagnostics."""
import subprocess
import sys
from pathlib import Path

HARNESS_UNREGISTERED = r'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t

name = "T99 a case nobody registered"
why = "some reason"
t.skip(name, why)
expected = f"{name} ({why})"
assert any(expected in item for item in t.UNEXPECTED_SKIPS), t.UNEXPECTED_SKIPS
print("EXPECTED_DIAGNOSTIC: present")
code = t.main()
print("MAIN_EXIT:", code)
assert code == 1, f"expected main() == 1, got {code}"
'''

HARNESS_WRONG_REASON = r'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t

name = "T36 directory symlink is rejected as a governed root"
why = "a different reason"
t.skip(name, why)
assert any(name in item and why in item for item in t.UNEXPECTED_SKIPS), t.UNEXPECTED_SKIPS
print("EXPECTED_DIAGNOSTIC: present")
code = t.main()
print("MAIN_EXIT:", code)
assert code == 1, f"expected main() == 1, got {code}"
'''

HARNESS_WHITESPACE = r'''
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
import test_check_document_management as t

name = "T36 directory symlink is rejected as a governed root"
why = "\u00a0symlink creation unavailable on this platform\t"
t.skip(name, why)
assert any(name in item and repr(why) in item for item in t.UNEXPECTED_SKIPS), t.UNEXPECTED_SKIPS
print("EXPECTED_DIAGNOSTIC: present")
code = t.main()
print("MAIN_EXIT:", code)
assert code == 1, f"expected main() == 1, got {code}"
'''

failed = False
for label, harness in (
    ("unregistered-name", HARNESS_UNREGISTERED),
    ("wrong-reason", HARNESS_WRONG_REASON),
    ("whitespace-reason", HARNESS_WHITESPACE),
):
    r = subprocess.run(
        [sys.executable, "-c", harness],
        capture_output=True,
        text=True,
        cwd=str(Path.cwd()),
        encoding="utf-8",
        errors="replace",
    )
    lines = (r.stdout or "").splitlines()
    expected = "EXPECTED_DIAGNOSTIC: present" in lines
    main_exit = "MAIN_EXIT: 1" in lines
    ok = r.returncode == 0 and expected and main_exit
    print(label, "->", "PASS" if ok else "FAIL",
          [line for line in lines if line.startswith(("EXPECTED_DIAGNOSTIC", "MAIN_EXIT"))])
    if not ok:
        print("STDERR:", (r.stderr or "").splitlines()[-5:])
        failed = True

sys.exit(1 if failed else 0)
