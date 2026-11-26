#!/usr/bin/env python3
"""Regression tests for bilingual governance scripts (stdlib only)."""
import os,subprocess,sys,tempfile,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent
TIERING=HERE/"check-bilingual-tiering.sh"; SYNC=HERE/"check-bilingual-sync.sh"; TRANSLATOR=HERE/"translate-document.py"
# On Windows, plain BASH may resolve to the WSL launcher; BASH_BIN lets
# callers point at a real POSIX bash (e.g. Git Bash) explicitly.
BASH=os.environ.get("BASH_BIN","bash")
class Tests(unittest.TestCase):
    def run_cmd(self,cmd,**kw):
        # MSYS bash eats backslash escapes in Windows-style paths; pass POSIX
        # style paths and decode robustly on any platform.
        cmd=[c.as_posix() if isinstance(c,Path) else c for c in cmd]
        return subprocess.run(cmd,text=True,capture_output=True,check=False,
                              encoding="utf-8",errors="replace",**kw)
    def test_unknown_is_reported_not_pass(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); subprocess.run(["git","init","-q",str(root)],check=True)
            subprocess.run(["git","-C",str(root),"config","user.email","test@example.invalid"],check=True)
            subprocess.run(["git","-C",str(root),"config","user.name","Test"],check=True)
            (root/"docs").mkdir(); (root/"docs"/"new.md").write_text("# new\n",encoding="utf-8")
            (root/"known.md").write_text("# known\n",encoding="utf-8")
            known_sha=subprocess.run(["git","-C",str(root),"hash-object",str((root/"known.md").as_posix())],capture_output=True,encoding="utf-8",errors="replace").stdout.strip()
            mapping=root/"mapping.yaml"; mapping.write_text("tier1:\n  files:\n    - path: known.md\n      blob_sha: %s\ntier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules:\n    - directory: docs/\n      tier: UNKNOWN\n"%known_sha,encoding="utf-8")
            subprocess.run(["git","-C",str(root),"add","."],check=True); subprocess.run(["git","-C",str(root),"commit","-qm","fixture"],check=True)
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,2,r.stdout+r.stderr); self.assertIn("UNKNOWN\tdocs/new.md",r.stdout); self.assertIn("NEEDS_CONFIRMATION",r.stderr)
    def test_sync_failure_exit_propagates(self):
        with tempfile.TemporaryDirectory() as d:
            stub=Path(d)/"python-fails"; stub.write_text("#!/bin/sh\nexit 23\n",encoding="utf-8"); stub.chmod(0o755)
            r=self.run_cmd([BASH,SYNC,"--source","s.md","--counterpart","t.md"],env={**os.environ,"PYTHON_BIN":str(stub.as_posix())})
            self.assertEqual(r.returncode,23,r.stdout+r.stderr)
    def test_sync_source_revision_and_pairing(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s,t=root/"s.md",root/"t.md"
            s.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: t.md -->\n",encoding="utf-8")
            t.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: s.md -->\n",encoding="utf-8")
            r=self.run_cmd([BASH,SYNC,"--source",s,"--counterpart",t])
            self.assertEqual(r.returncode,0,r.stdout+r.stderr); self.assertIn("PASS",r.stdout)
    def test_translation_diff_work_order(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s,t,o=root/"zh.md",root/"en.md",root/"work.md"
            s.write_text("# 标题\nMUST 保留。\n",encoding="utf-8"); t.write_text("# Title\nMUST preserve.\n",encoding="utf-8")
            r=self.run_cmd([sys.executable,TRANSLATOR,"--source",s,"--target",t,"--output",o])
            self.assertEqual(r.returncode,0,r.stdout+r.stderr); body=o.read_text(encoding="utf-8")
            self.assertIn("status: PENDING_TRANSLATION",body); self.assertIn("Human translator/reviewer",body); self.assertIn("no model/API invocation",body)
    def test_translation_failure_status_registered(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); o=root/"failed.md"
            r=self.run_cmd([sys.executable,TRANSLATOR,"--source",root/"missing.md","--target",root/"t.md","--output",o])
            self.assertEqual(r.returncode,1,r.stdout+r.stderr); self.assertTrue(o.is_file()); body=o.read_text(encoding="utf-8")
            self.assertIn("status: FAILED",body); self.assertIn("failure:",body)
    def make_repo(self,root,files):
        root=Path(root); subprocess.run(["git","init","-q",str(root)],check=True)
        subprocess.run(["git","-C",str(root),"config","user.email","test@example.invalid"],check=True)
        subprocess.run(["git","-C",str(root),"config","user.name","Test"],check=True)
        for name,content in files.items():
            p=root/name; p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text(content,encoding="utf-8",newline="\n")
        subprocess.run(["git","-C",str(root),"add","."],check=True)
        subprocess.run(["git","-C",str(root),"commit","-qm","fixture"],check=True)
        return subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],capture_output=True,encoding="utf-8",errors="replace").stdout.strip()
    def blob_sha(self,root,path):
        return subprocess.run(["git","-C",str(root),"rev-parse",f"HEAD:{path}"],capture_output=True,encoding="utf-8",errors="replace").stdout.strip()
    def test_tiering_blob_sha_drift_fails(self):
        # A registered blob_sha that no longer matches the file content at the
        # declared baseline MUST fail the check (exit 1), not pass silently.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=self.make_repo(root,{"docs/a.md":"# real content\n"})
            sha=self.blob_sha(root,"docs/a.md")
            mapping=root/"mapping.yaml"
            mapping.write_text(
                f"baseline_commit: {head}\ntier1:\n  files:\n    - path: docs/a.md\n      blob_sha: {'0'*40}\n"
                "tier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules: []\n",
                encoding="utf-8",newline="\n")
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,1,r.stdout+r.stderr)
            self.assertIn("STALE_BLOB_SHA\tdocs/a.md",r.stdout)
            self.assertIn("BASELINE_DRIFT",r.stderr)
    def test_tiering_valid_baseline_sha_passes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); head=self.make_repo(root,{"docs/a.md":"# real content\n"})
            sha=self.blob_sha(root,"docs/a.md")
            mapping=root/"mapping.yaml"
            mapping.write_text(
                f"baseline_commit: {head}\ntier1:\n  files:\n    - path: docs/a.md\n      blob_sha: {sha}\n"
                "tier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules: []\n",
                encoding="utf-8",newline="\n")
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertIn("TIER1\tdocs/a.md",r.stdout)
    def test_tiering_non_commit_baseline_rejected(self):
        # A declared baseline_commit that is not a commit object MUST be
        # rejected before any classification is reported (evidence-binding v3).
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.make_repo(root,{"docs/a.md":"# x\n"})
            tree=self.run_cmd(["git","-C",str(root),"rev-parse","HEAD^{tree}"]).stdout.strip()
            mapping=root/"mapping.yaml"
            mapping.write_text(
                f"baseline_commit: {tree}\ntier1:\n  files:\n    - path: docs/a.md\n"
                "tier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules: []\n",
                encoding="utf-8",newline="\n")
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,1,r.stdout+r.stderr)
            self.assertIn("not a commit object",r.stderr)
    def test_tiering_registered_missing_path_fails(self):
        # A per-file entry registered in the mapping but absent from the tree
        # MUST be reported as MISSING_IN_BASELINE and fail the check.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.make_repo(root,{"docs/a.md":"# present\n"})
            mapping=root/"mapping.yaml"
            mapping.write_text(
                "tier1:\n  files:\n    - path: docs/gone.md\n      blob_sha: %s\n"
                "tier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules: []\n"%("e"*40),
                encoding="utf-8",newline="\n")
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,1,r.stdout+r.stderr)
            self.assertIn("MISSING_IN_BASELINE\tdocs/gone.md",r.stderr)
    def test_tiering_path_in_worktree_but_absent_from_baseline_fails(self):
        # R2 F1: a file that exists in the current worktree/index but NOT in
        # the declared baseline tree MUST fail (cat-file -e binding), even
        # though ls-files would enumerate it.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            self.make_repo(root,{"docs/a.md":"# a\n"})
            base=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],capture_output=True,encoding="utf-8",errors="replace").stdout.strip()
            (root/"docs"/"b.md").write_text("# added later\n",encoding="utf-8",newline="\n")
            subprocess.run(["git","-C",str(root),"add","."],check=True)
            subprocess.run(["git","-C",str(root),"commit","-qm","add b"],check=True)
            sha_a=self.blob_sha(root,"docs/a.md")  # rev-parse at HEAD == at base for a.md
            mapping=root/"mapping.yaml"
            mapping.write_text(
                f"baseline_commit: {base}\ntier1:\n  files:\n    - path: docs/a.md\n      blob_sha: {sha_a}\n"
                "tier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules: []\n",
                encoding="utf-8",newline="\n")
            # Register docs/b.md (exists in index) against the older baseline.
            text=mapping.read_text(encoding="utf-8")
            text=text.replace("    - path: docs/a.md\n      blob_sha: %s\n"%sha_a,
                              "    - path: docs/a.md\n      blob_sha: %s\n    - path: docs/b.md\n      blob_sha: %s\n"%(sha_a,self.blob_sha(root,"docs/b.md")))
            mapping.write_text(text,encoding="utf-8",newline="\n")
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,1,r.stdout+r.stderr)
            self.assertIn("MISSING_IN_BASELINE\tdocs/b.md",r.stderr)
    def test_tiering_entry_without_blob_sha_fails(self):
        # R2 F1: every per-file registration MUST carry a valid blob_sha.
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); self.make_repo(root,{"docs/a.md":"# a\n"})
            mapping=root/"mapping.yaml"
            mapping.write_text(
                "tier1:\n  files:\n    - path: docs/a.md\n"
                "tier2:\n  files: []\ntier3_per_file:\n  files: []\ndirectory_rules:\n  rules: []\n",
                encoding="utf-8",newline="\n")
            r=self.run_cmd([BASH,TIERING,mapping],env={**os.environ,"REPO_ROOT":str(root)})
            self.assertEqual(r.returncode,1,r.stdout+r.stderr)
            self.assertIn("NO_BLOB_SHA\tdocs/a.md",r.stderr)
    def test_sync_bilingual_pair_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s,t=root/"s.md",root/"t.md"
            s.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: t.md -->\n",encoding="utf-8")
            # Counterpart points back at the wrong file.
            t.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: other.md -->\n",encoding="utf-8")
            r=self.run_cmd([BASH,SYNC,"--source",s,"--counterpart",t])
            self.assertNotEqual(r.returncode,0,r.stdout+r.stderr)
    def test_sync_source_revision_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); s,t=root/"s.md",root/"t.md"
            s.write_text("<!-- source-revision: abcdef1234567 -->\n<!-- bilingual-pair: t.md -->\n",encoding="utf-8")
            t.write_text("<!-- source-revision: 9999999999999 -->\n<!-- bilingual-pair: s.md -->\n",encoding="utf-8")
            r=self.run_cmd([BASH,SYNC,"--source",s,"--counterpart",t])
            self.assertNotEqual(r.returncode,0,r.stdout+r.stderr)
if __name__=="__main__": unittest.main(verbosity=2)
