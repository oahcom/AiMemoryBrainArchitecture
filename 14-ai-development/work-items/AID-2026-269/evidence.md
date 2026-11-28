---
document_metadata:
  steward: "user-authorized operator (delegated by account owner)"
  domain: ai-development
  role: work-record
  lifecycle:
    approval:
      decision_status: Draft
    evidence_verification:
      verification_status: Unverified
      last_verified_date: "2026-11-27"
      last_verification_note: "Raw command log; no acceptance decision is asserted."
    usage_status: Active
    modification_status: Unchanged
  authority:
    canonical_status: Non-Canonical
    canonical_scope: "Raw command and digest evidence for AID-2026-269"
    canonical_scope_id: "ai-development/aid-2026-269-evidence"
    canonical_scope_keywords:
      - "exact-head-review"
      - "command-log"
      - "digest-recomputation"
    canonical_conflict_status: None
    normative_status: Informative
---

# Evidence appendix — review case #1278 (AID-2026-269, L2-B)

Raw command log. Shell: Windows PowerShell 5.1 on win32; Git
`git version 2.56.1.windows.1`; `Python 3.12.3`. All commands were run with the
working directory `D:\code\wt-aid268`. Exit codes are the PowerShell
`$LASTEXITCODE` of the preceding native command, recorded as observed.

Nothing below is reconstructed after the fact; the numbers in
[review-case-1278.md](review-case-1278.md) come from these outputs.

---

## E1. Worktree identity and locking

Command:

```
Set-Location D:\code\wt-aid268; "git_dir=$(git rev-parse --git-dir)"; "common_dir=$(git rev-parse --git-common-dir)"
```

Exit code: 0. Output:

```
git_dir=D:/code/AiMemoryBrainArchitecture/.git/worktrees/wt-aid268
common_dir=D:/code/AiMemoryBrainArchitecture/.git
```

Consequence recorded: the worktree shares its object database and refs with every
other worktree of the same repository, so refs can move under a running review.

## E2. Fetch and metadata (first lock)

Command:

```
Set-Location D:\code\wt-aid268; git fetch origin --prune 2>&1 | Out-String; "EXIT=$LASTEXITCODE"
```

Exit code: 0. Output (stderr rendered as a PowerShell error record; the fetch
itself succeeded):

```
git : From https://github.com/oahcom/AiMemoryBrainArchitecture
    f4e80641..bbae1f9c  fix/aid-268-manifest-blob-pins -> origin/fix/aid-268-manifest-blob-pins
    609bed88..99a6f9bb  s6a/aid-2026-279-work-item-uniqueness -> origin/s6a/aid-2026-279-work-item-uniqueness
    93a882b9..46e33a26  w10/aid-253-ac3-ac4-r2 -> origin/w10/aid-253-ac3-ac4-r2
EXIT=0
```

Command:

```
Set-Location D:\code\wt-aid268; git rev-parse origin/main; git rev-parse HEAD; git rev-parse "HEAD^{tree}"; git --version; python --version; (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
```

Exit code: 0. Output:

```
10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f
987d26021affbb5ba6d651e0fb5985d6bd4026a5
2a73559ebf1406ef3892c4c71dce33c20731e446
git version 2.56.1.windows.1
Python 3.12.3
2026-11-27T04:09:16Z
```

## E3. Declaration locations

Command:

```
Set-Location D:\code\wt-aid268; Select-String -Path "14-ai-development/work-items/AID-2026-092/manifest.yaml" -Pattern "prompt" | ForEach-Object { "$($_.LineNumber): $($_.Line)" }
```

Exit code: 0. Output:

```
25: prompt_id: AID-2026-083-PROMPT
26: prompt_version: 1
27: prompt_file: 14-ai-development/work-items/AID-2026-092/prompt-v1.md
28: prompt_status: RECORDED_NOT_FROZEN
29: prompt_sha256: a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3
30: prompt_bytes: 3772
31: prompt_digest_correction: >-
33:   at 2455 bytes. It matched no version of prompt-v1.md at any commit reachable from any ref:
34:   enumerating every distinct blob at this path and at AID-2026-083/prompt-v1.md across
40:   than relying on the diff. prompt_id is deliberately still AID-2026-083-PROMPT: the work item was
42: prompt_provenance: USER_AUTHORIZED_DELEGATED_REQUEST; snapshot assembled from the assigned scope, no independent source verification claimed
47:     GRANTED only for this work item's manifest, prompt snapshot, three evidence reports,
59:     - 14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

Command:

```
Set-Location D:\code\wt-aid268; git ls-tree -r HEAD -- "14-ai-development/work-items/AID-2026-092/"
```

Exit code: 0. Output:

```
100644 blob c5dd4d533ba3be3e4b6ee7b081c79691db57c94f	14-ai-development/work-items/AID-2026-092/ISSUE-1037-validator-and-metadata-verification.md
100644 blob fbaae7eb5a175944cb89d12fe8949aa1535c9d98	14-ai-development/work-items/AID-2026-092/ISSUE-1189-approval-provenance.md
100644 blob fc210be4fd0cf10d335009fcc1d4c17f41e27d0d	14-ai-development/work-items/AID-2026-092/ISSUE-1197-phase-freeze-audit.md
100644 blob 227c761d82984fb671ab3fa53f57b41c10bdd04c	14-ai-development/work-items/AID-2026-092/manifest.yaml
100644 blob 7adf342a51f924cb732129ba3052ca65a832ea75	14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

No `prompt_file_blob_sha` key is declared; the blob identity comes from
`ls-tree`.

## E4. Byte-exact recomputation from the blob (method 1: stdin pipe)

Command (binary pipe through `cmd`, Python reads `sys.stdin.buffer`):

```
Set-Location D:\code\wt-aid268; cmd /c "git cat-file blob 7adf342a51f924cb732129ba3052ca65a832ea75 | python -c ""import sys,hashlib; b=sys.stdin.buffer.read(); print('bytes',len(b)); print('sha256',hashlib.sha256(b).hexdigest())"""; "EXIT=$LASTEXITCODE"
```

Exit code: 0. Output:

```
bytes 3714
sha256 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
```

## E5. Byte-exact recomputation (method 2: redirect to file, independent read)

Commands:

```
Set-Location D:\code\wt-aid268; "cat-file -s: $(git cat-file -s 7adf342a51f924cb732129ba3052ca65a832ea75)"; "cat-file -s manifest: $(git cat-file -s 227c761d82984fb671ab3fa53f57b41c10bdd04c)"; git config --get core.autocrlf; "---worktree---"; (Get-Item "14-ai-development/work-items/AID-2026-092/prompt-v1.md").Length
cmd /c "git cat-file blob 7adf342a51f924cb732129ba3052ca65a832ea75 > %TEMP%\blob1278.bin"
cmd /c "python -c ""import hashlib;b=open(r'%TEMP%\blob1278.bin','rb').read();print('file_bytes',len(b));print('file_sha256',hashlib.sha256(b).hexdigest())"""
cmd /c "python -c ""import hashlib;b=open(r'14-ai-development/work-items/AID-2026-092/prompt-v1.md','rb').read();print('wt_bytes',len(b));print('wt_sha256',hashlib.sha256(b).hexdigest());print('crlf',b.count(b'\r\n'));print('lf',b.count(b'\n'))"""
```

Exit code: 0. Output:

```
cat-file -s: 3714
cat-file -s manifest: 7680
false
---worktree---
3714
file_bytes 3714
file_sha256 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
wt_bytes 3714
wt_sha256 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
crlf 0
lf 67
```

Both methods agree; the working tree copy equals the blob because
`core.autocrlf=false` and the object contains LF only.

## E6. Manifest blob recomputation

Command:

```
Set-Location D:\code\wt-aid268; cmd /c "git cat-file blob 227c761d82984fb671ab3fa53f57b41c10bdd04c | python -c ""import sys,hashlib;b=sys.stdin.buffer.read();print('manifest_blob_bytes',len(b));print('manifest_blob_sha256',hashlib.sha256(b).hexdigest())"""
```

Exit code: 0. Output:

```
manifest_blob_bytes 7680
manifest_blob_sha256 a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca
```

This sha256 equals the manifest blob at `e0d6a9920cee5fe0629af7daef2656d0bfb26acd`
(§E9), i.e. the candidate's manifest is exactly the AID-2026-102 correction
content.

## E7. History enumeration script

Script written to `C:\Users\Administrator\AppData\Local\Temp\opencode\hist1278.py`:

```python
import hashlib, subprocess, sys

REPO = r"D:\code\wt-aid268"
PATHS = [
    "14-ai-development/work-items/AID-2026-092/prompt-v1.md",
    "14-ai-development/work-items/AID-2026-083/prompt-v1.md",
    "14-ai-development/work-items/AID-2026-092/manifest.yaml",
]

def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True)

def gitb(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True).stdout

for path in PATHS:
    r = git("rev-list", "--all", "--", path)
    commits = r.stdout.decode().split()
    print("=== PATH", path)
    print("rev_list_exit", r.returncode, "commits", len(commits))
    print("commit_sha\tpath\tbyte_count\tsha256")
    seen = {}
    for c in commits:
        blob = gitb("show", "%s:%s" % (c, path))
        if not blob:
            print("%s\t%s\t%s\t%s" % (c, path, "ABSENT", "ABSENT"))
            continue
        h = hashlib.sha256(blob).hexdigest()
        print("%s\t%s\t%d\t%s" % (c, path, len(blob), h))
        seen.setdefault((len(blob), h), []).append(c)
    print("--- distinct (bytes,sha256) for this path:")
    for (n, h), cs in sorted(seen.items()):
        print("  %d bytes  %s  commits=%d  first=%s  last=%s" % (n, h, len(cs), cs[-1], cs[0]))
    print()

print("=== TARGET DIGESTS PRESENT ANYWHERE?")
targets = {
    "9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1": 2455,
    "a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3": 3772,
    "9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724": 3714,
}
print("target\tsha256_match_commits")
for t in targets:
    hits = []
    for path in PATHS[:2]:
        for c in git("rev-list", "--all", "--", path).stdout.decode().split():
            blob = gitb("show", "%s:%s" % (c, path))
            if blob and hashlib.sha256(blob).hexdigest() == t:
                hits.append((c, path, len(blob)))
    print(t, len(hits), hits)
```

Invocation:

```
Set-Location D:\code\wt-aid268; python C:\Users\Administrator\AppData\Local\Temp\opencode\hist1278.py 2>&1; "EXIT=$LASTEXITCODE"
```

Exit code: 0.

## E8. History enumeration output (first run, envelope 2452 refs / 9204 commits)

```
=== PATH 14-ai-development/work-items/AID-2026-092/prompt-v1.md
rev_list_exit 0 commits 2
commit_sha	path	byte_count	sha256
44b57170b86c7f3e56744da756ed24744b1c659c	14-ai-development/work-items/AID-2026-092/prompt-v1.md	3714	9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
f61dc15a7701702a57a7c0edcfc9d61591986bca	14-ai-development/work-items/AID-2026-092/prompt-v1.md	3772	a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3
--- distinct (bytes,sha256) for this path:
  3714 bytes  9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724  commits=1  first=44b57170b86c7f3e56744da756ed24744b1c659c  last=44b57170b86c7f3e56744da756ed24744b1c659c
  3772 bytes  a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3  commits=1  first=f61dc15a7701702a57a7c0edcfc9d61591986bca  last=f61dc15a7701702a57a7c0edcfc9d61591986bca

=== PATH 14-ai-development/work-items/AID-2026-083/prompt-v1.md
rev_list_exit 0 commits 4
commit_sha	path	byte_count	sha256
44c530a02e1c7f34f742f619449f13efd60ed4e0	14-ai-development/work-items/AID-2026-083/prompt-v1.md	7689	0c0ce002db720c6a46186a94a591bc13939768627910b447960cbbd4f5cfe640
45045ed319caa7049deacfc98de75f698db7a3d0	14-ai-development/work-items/AID-2026-083/prompt-v1.md	ABSENT	ABSENT
ecbb9bc743586edb3a116049c51ede9ddb324492	14-ai-development/work-items/AID-2026-083/prompt-v1.md	2915	9614ddf7013eaaa6f740842163f5f2f53d9475103d602fc0858bc62b3608166f
e5068b65c5f06857c4d21ba66b171b5e222f7cfc	14-ai-development/work-items/AID-2026-083/prompt-v1.md	4137	7ce260dfb8f1a959bce48ac3abcbfa2d53bbd0c984663013136fbcd3152b67ec
--- distinct (bytes,sha256) for this path:
  2915 bytes  9614ddf7013eaaa6f740842163f5f2f53d9475103d602fc0858bc62b3608166f  commits=1  first=ecbb9bc743586edb3a116049c51ede9ddb324492  last=ecbb9bc743586edb3a116049c51ede9ddb324492
  4137 bytes  7ce260dfb8f1a959bce48ac3abcbfa2d53bbd0c984663013136fbcd3152b67ec  commits=1  first=e5068b65c5f06857c4d21ba66b171b5e222f7cfc  last=e5068b65c5f06857c4d21ba66b171b5e222f7cfc
  7689 bytes  0c0ce002db720c6a46186a94a591bc13939768627910b447960cbbd4f5cfe640  commits=1  first=44c530a02e1c7f34f742f619449f13efd60ed4e0  last=44c530a02e1c7f34f742f619449f13efd60ed4e0

=== PATH 14-ai-development/work-items/AID-2026-092/manifest.yaml
rev_list_exit 0 commits 4
commit_sha	path	byte_count	sha256
27bfa597764281b3abdbe939843b45c14f25b388	14-ai-development/work-items/AID-2026-092/manifest.yaml	7680	11759f4c586af7654fb0c96d3d8b1783e59a293cc3a1dc7f0ea6eae70722c6c6
e0d6a9920cee5fe0629af7daef2656d0bfb26acd	14-ai-development/work-items/AID-2026-092/manifest.yaml	7680	a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca
3619502712b422f1149c5c37ab6e97679f8130ce	14-ai-development/work-items/AID-2026-092/manifest.yaml	6691	daec20c56161a691667f2d4ba453eef45fac1b784159971615c4e5dcd5b00c48
f61dc15a7701702a57a7c0edcfc9d61591986bca	14-ai-development/work-items/AID-2026-092/manifest.yaml	6677	64af89558212bce7b85e39b9af4c5bbea35429807f56b5cc66fee2fca8aaf326
--- distinct (bytes,sha256) for this path:
  6677 bytes  64af89558212bce7b85e39b9af4c5bbea35429807f56b5cc66fee2fca8aaf326  commits=1  first=f61dc15a7701702a57a7c0edcfc9d61591986bca  last=f61dc15a7701702a57a7c0edcfc9d61591986bca
  6691 bytes  daec20c56161a691667f2d4ba453eef45fac1b784159971615c4e5dcd5b00c48  commits=1  first=3619502712b422f1149c5c37ab6e97679f8130ce  last=3619502712b422f1149c5c37ab6e97679f8130ce
  7680 bytes  11759f4c586af7654fb0c96d3d8b1783e59a293cc3a1dc7f0ea6eae70722c6c6  commits=1  first=27bfa597764281b3abdbe939843b45c14f25b388  last=27bfa597764281b3abdbe939843b45c14f25b388
  7680 bytes  a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca  commits=1  first=e0d6a9920cee5fe0629af7daef2656d0bfb26acd  last=e0d6a9920cee5fe0629af7daef2656d0bfb26acd

=== TARGET DIGESTS PRESENT ANYWHERE?
target	sha256_match_commits
9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1 0 []
a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3 1 [('f61dc15a7701702a57a7c0edcfc9d61591986bca', '14-ai-development/work-items/AID-2026-092/prompt-v1.md', 3772)]
9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724 1 [('44b57170b86c7f3e56744da756ed24744b1c659c', '14-ai-development/work-items/AID-2026-092/prompt-v1.md', 3714)]
```

## E9. Envelope re-check and drift

Command:

```
Set-Location D:\code\wt-aid268; git fetch origin --prune 2>&1 | Out-String; "fetch_exit=$LASTEXITCODE"; "origin_main=$(git rev-parse origin/main)"; "head=$(git rev-parse HEAD)"; "tree=$(git rev-parse 'HEAD^{tree}')"; "all_count=$(git rev-list --count --all)"; "refs=$(git for-each-ref --format='%(refname)' | Measure-Object | ForEach-Object { $_.Count })"; "prompt_blob=$(git rev-parse 'HEAD:14-ai-development/work-items/AID-2026-092/prompt-v1.md')"; (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
```

Exit code: 0. Output:

```
fetch_exit=0
origin_main=386d8f57b02d8e3c511ff0e3980b9ce0af8b3028
head=987d26021affbb5ba6d651e0fb5985d6bd4026a5
tree=2a73559ebf1406ef3892c4c71dce33c20731e446
all_count=9211
refs=2454
prompt_blob=7adf342a51f924cb732129ba3052ca65a832ea75
2026-11-27T04:22:34Z
```

`origin/main` moved from `10d33b3f6c012e1c0d5649a5279cadb6d27b1a2f` (04:09:16Z) to
`386d8f57b02d8e3c511ff0e3980b9ce0af8b3028` (04:22:34Z); refs 2452 → 2454 and
reachable commits 9204 → 9211. The candidate SHA and the prompt blob did not
change.

History enumeration re-run at the wider envelope:

```
Set-Location D:\code\wt-aid268; python C:\Users\Administrator\AppData\Local\Temp\opencode\hist1278.py > $env:TEMP\hist1278.out 2>&1; "EXIT=$LASTEXITCODE"
```

Exit code: 0. Output (tail; per-path tables identical to §E8, `… 1 more` only for
repeated trailing lines):

```
f61dc15a7701702a57a7c0edcfc9d61591986bca	14-ai-development/work-items/AID-2026-092/manifest.yaml	6677	64af89558212bce7b85e39b9af4c5bbea35429807f56b5cc66fee2fca8aaf326
--- distinct (bytes,sha256) for this path:
  6677 bytes  64af89558212bce7b85e39b9af4c5bbea35429807f56b5cc66fee2fca8aaf326  commits=1  first=f61dc15a7701702a57a7c0edcfc9d61591986bca  last=f61dc15a7701702a57a7c0edcfc9d61591986bca
  6691 bytes  daec20c56161a691667f2d4ba453eef45fac1b784159971615c4e5dcd5b00c48  commits=1  first=3619502712b422f1149c5c37ab6e97679f8130ce  last=3619502712b422f1149c5c37ab6e97679f8130ce
  7680 bytes  11759f4c586af7654fb0c96d3d8b1783e59a293cc3a1dc7f0ea6eae70722c6c6  commits=1  first=27bfa597764281b3abdbe939843b45c14f25b388  last=27bfa597764281b3abdbe939843b45c14f25b388
  7680 bytes  a91b25f165766b7d7ee15f1a25269f98a4564dceeb4e6acf4e5db6b405a1f5ca  commits=1  first=e0d6a9920cee5fe0629af7daef2656d0bfb26acd  last=e0d6a9920cee5fe0629af7daef2656d0bfb26acd

=== TARGET DIGESTS PRESENT ANYWHERE?
target	sha256_match_commits
9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1 0 []
a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3 1 [('f61dc15a7701702a57a7c0edcfc9d61591986bca', '14-ai-development/work-items/AID-2026-092/prompt-v1.md', 3772)]
9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724 1 [('44b57170b86c7f3e56744da756ed24744b1c659c', '14-ai-development/work-items/AID-2026-092/prompt-v1.md', 3714)]
```

## E10. First-introduction commits

Command:

```
Set-Location D:\code\wt-aid268; git log --format="%H|%ad|%s" --date=iso -- "14-ai-development/work-items/AID-2026-092/prompt-v1.md" > $env:TEMP\g1.txt 2>&1; git log --format="%H|%ad|%s" --date=iso -- "14-ai-development/work-items/AID-2026-092/manifest.yaml" > $env:TEMP\g2.txt 2>&1; Get-Content $env:TEMP\g1.txt; Get-Content $env:TEMP\g2.txt
```

Exit code: 0. Output:

```
44b57170b86c7f3e56744da756ed24744b1c659c|2026-11-26 18:06:14 +0800|fix(gov): remove approval_scope's two permanently-empty keys from the schema and the corpus (#904)
f61dc15a7701702a57a7c0edcfc9d61591986bca|2026-11-26 15:04:18 +0800|docs(work-items): reallocate acceptance evidence as AID-2026-092 after main collision
e0d6a9920cee5fe0629af7daef2656d0bfb26acd|2026-11-26 17:31:59 +0800|docs(gov): correct the AID-2026-092 prompt digest, which matched no version
3619502712b422f1149c5c37ab6e97679f8130ce|2026-11-26 15:22:38 +0800|docs(registry): reconcile merged AID status 92
f61dc15a7701702a57a7c0edcfc9d61591986bca|2026-11-26 15:04:18 +0800|docs(work-items): reallocate acceptance evidence as AID-2026-092 after main collision
```

Note: `git log --all --no-renames --diff-filter=A -- <path>` returned nothing for
both 092 paths (empty output, exit 0) because `--diff-filter` under default merge
simplification does not report these paths; the introduction was therefore
established by diffing against the first parent instead:

Command:

```
Set-Location D:\code\wt-aid268; git diff-tree -r --name-status --no-commit-id 1e7f4d0a7baf06103dc3bd504293e25e53bd24c2 f61dc15a7701702a57a7c0edcfc9d61591986bca -- "14-ai-development/work-items/AID-2026-092/"; git diff-tree -r --name-status --no-commit-id 44b57170b86c7f3e56744da756ed24744b1c659c^ 44b57170b86c7f3e56744da756ed24744b1c659c -- "14-ai-development/work-items/AID-2026-092/prompt-v1.md"
```

Exit code: 0. Output:

```
A	14-ai-development/work-items/AID-2026-092/ISSUE-1037-validator-and-metadata-verification.md
A	14-ai-development/work-items/AID-2026-092/ISSUE-1189-approval-provenance.md
A	14-ai-development/work-items/AID-2026-092/ISSUE-1197-phase-freeze-audit.md
A	14-ai-development/work-items/AID-2026-092/manifest.yaml
A	14-ai-development/work-items/AID-2026-092/prompt-v1.md
M	14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

Ancestry checks:

```
Set-Location D:\code\wt-aid268; git merge-base --is-ancestor f61dc15a7701702a57a7c0edcfc9d61591986bca HEAD; "f61dc15a_ancestor_exit=$LASTEXITCODE"; git merge-base --is-ancestor 44b57170b86c7f3e56744da756ed24744b1c659c HEAD; "44b57170_ancestor_exit=$LASTEXITCODE"; git merge-base --is-ancestor 27bfa597764281b3abdbe939843b45c14f25b388 HEAD; "27bfa597_ancestor_exit=$LASTEXITCODE"
```

Exit code: 0 (last command's `$LASTEXITCODE` was 1 because `27bfa597…` is not an
ancestor). Output:

```
f61dc15a ancestor of HEAD: 0
44b57170 ancestor of HEAD: 0
--- ancestry 27bfa597:
is_ancestor_exit=1
```

## E11. The declaring commit (pre-rename) and its pinned file

Command:

```
Set-Location D:\code\wt-aid268; git show cac933cb9eb3e51b725dfaca0af47d5c05f8ad80:14-ai-development/work-items/AID-2026-083/manifest.yaml > $env:TEMP\m083.txt 2>&1; Select-String -Path $env:TEMP\m083.txt -Pattern "prompt_sha256|prompt_bytes|prompt_file" | ForEach-Object { "$($_.LineNumber): $($_.Line)" }; git rev-parse "cac933cb9eb3e51b725dfaca0af47d5c05f8ad80:14-ai-development/work-items/AID-2026-083/prompt-v1.md"; cmd /c "git cat-file blob $(git rev-parse cac933cb9eb3e51b725dfaca0af47d5c05f8ad80:14-ai-development/work-items/AID-2026-083/prompt-v1.md) | python -c ""import sys,hashlib;b=sys.stdin.buffer.read();print('bytes',len(b));print('sha256',hashlib.sha256(b).hexdigest())"""
```

Exit code: 0. Output:

```
23: prompt_file: 14-ai-development/work-items/AID-2026-083/prompt-v1.md
25: prompt_sha256: 9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1
26: prompt_bytes: 2455
ecdb9285c2c2c9975de35a002a7efbc47915346d
bytes 3772
sha256 a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3
```

Commit identity of the declaring commit:

```
git log -1 --format="%H|parents=%P|%ad|%s" --date=iso cac933cb9eb3e51b725dfaca0af47d5c05f8ad80
```

Output:

```
cac933cb9eb3e51b725dfaca0af47d5c05f8ad80|parents=515b7144320fd9fcc1e1a2c3d2d2744d979b4ca8|2026-11-26 14:37:01 +0800|docs: add delegated evidence package for #1189 #1197 #1037
```

`515b7144…` is the manifest's own `base_commit_sha` (manifest line 22).

## E12. Per-commit manifest declaration history

Commands:

```
git show e0d6a9920cee5fe0629af7daef2656d0bfb26acd:14-ai-development/work-items/AID-2026-092/manifest.yaml | Select-String -Pattern "prompt_sha256|prompt_bytes"
git show f61dc15a7701702a57a7c0edcfc9d61591986bca:14-ai-development/work-items/AID-2026-092/manifest.yaml | Select-String -Pattern "prompt_sha256|prompt_bytes"
git show 27bfa597764281b3abdbe939843b45c14f25b388:14-ai-development/work-items/AID-2026-092/manifest.yaml | Select-String -Pattern "prompt_sha256|prompt_bytes|prompt_file"
```

Exit code: 0. Output:

```
--- e0d6a992 manifest prompt lines:
prompt_sha256: a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3
prompt_bytes: 3772
--- f61dc15a manifest prompt lines:
prompt_sha256: 9be8aebf7d595f81cc062e5c03a67fd8317aeefaf69dd635fd9031f112dc25d1
prompt_bytes: 2455
--- 27bfa597 manifest prompt lines:
prompt_file: 14-ai-development/work-items/AID-2026-092/prompt-v1.md
prompt_sha256: 9de0895124032230b3418ff062ef2d590d27f37582d2847032a46b7116a53724
prompt_bytes: 3714
```

`27bfa597…` identity and ref containment:

```
git log -1 --format="%H|%ad|%s" --date=iso 27bfa597764281b3abdbe939843b45c14f25b388
git branch -a --contains 27bfa597764281b3abdbe939843b45c14f25b388
```

Output:

```
27bfa597764281b3abdbe939843b45c14f25b388|2026-11-26 21:32:35 +0800|fix(gov): repin 33 prompt digests PR #1281 invalidated, and repoint 3 misattributed corrections (AID-2026-116)
  pr1321
  pr1336
+ renumber/1321-187
  remotes/origin/gov/aid-116-pin-and-attribution
  remotes/origin/renumber/1321-187
  remotes/pr/1321
  … 1 more
```

## E13. What `44b57170…` changed in the prompt

Command:

```
git diff --numstat f61dc15a7701702a57a7c0edcfc9d61591986bca 44b57170b86c7f3e56744da756ed24744b1c659c -- "14-ai-development/work-items/AID-2026-092/prompt-v1.md"
```

Exit code: 0. Output:

```
0	2	14-ai-development/work-items/AID-2026-092/prompt-v1.md
```

Hunk (from `git show 44b57170… -- <path>`):

```
diff --git a/14-ai-development/work-items/AID-2026-092/prompt-v1.md b/14-ai-development/work-items/AID-2026-092/prompt-v1.md
index ecdb9285..7adf342a 100644
--- a/14-ai-development/work-items/AID-2026-092/prompt-v1.md
+++ b/14-ai-development/work-items/AID-2026-092/prompt-v1.md
@@ -12,8 +12,6 @@ document_metadata:
         value: null
       approval_scope:
         type: Full-document
-        included_sections: []
-        included_assets: []
       approval_applicability: Not-Applicable-To-Current-Version
       evidence_reference: []
       revocation: null
```

2 deleted lines, 0 added → 3772 − 3714 = 58 bytes, consistent with the measured
sizes.

## E14. INDEX cross-check

Command:

```
Set-Location D:\code\wt-aid268; cmd /c "git show HEAD:14-ai-development/work-items/INDEX.md | python -c ""import sys;t=sys.stdin.buffer.read().decode('utf-8'); lines=t.split('\n'); print('lines',len(lines)); [print(i+1,'|',l) for i,l in enumerate(lines) if 'a459d7e5' in l or '9be8aebf' in l]"""
```

Exit code: 0. Output (line 65 truncated here with an explicit marker; the full row
is quoted in review-case-1278.md §6):

```
lines 308
65 | | [AID-2026-092](AID-2026-092/manifest.yaml) | … `AID-2026-083-PROMPT` v1 — `14-ai-development/work-items/AID-2026-092/prompt-v1.md`, 3772 bytes, SHA-256 `a459d7e523fbba4ffb8c0f6ade8d3d8c1ec6ce45b95c3f48f65b192c0413edb3`. The digest recorded at registration was `9be8aebf…` at 2455 bytes, which matched no version of the file at any ref … |
```

INDEX blob identity:

```
git rev-parse "HEAD:14-ai-development/work-items/INDEX.md"
```

Output:

```
3e652348dc7df5286d4ba0408091a1f052968c07
```

Only one row carries the `AID-2026-092` prompt digest (line 65). Line 146 is the
`AID-2026-102` correction row and carries no `AID-2026-092` digest.

## E15. Blob endings / encoding sanity

Command:

```
cmd /c "git cat-file blob 7adf342a51f924cb732129ba3052ca65a832ea75 | python -c ""import sys;b=sys.stdin.buffer.read();print('bom',b[:3]);print('lines',b.count(b'\n'));print('crlf',b.count(b'\r\n'))"""
```

Exit code: 0. Output:

```
bom b'---'
lines 67
crlf 0
```

## E16. Post-write self-check

Command:

```
Set-Location D:\code\wt-aid268; python -c "import hashlib,sys"; "py_exit=$LASTEXITCODE"; Get-ChildItem "14-ai-development/work-items/AID-2026-269" | Select-Object Name,Length
```

See the final self-check block appended at the end of this file (§E17).

## E17. Self-check results

Command:

```
Set-Location D:\code\wt-aid268; python -c "import hashlib,sys"; "py_import_exit=$LASTEXITCODE"; Get-ChildItem "14-ai-development/work-items/AID-2026-269" | Select-Object Name,Length | Format-Table -AutoSize | Out-String; python -c "import json,re; t=open(r'14-ai-development/work-items/AID-2026-269/review-case-1278.md',encoding='utf-8').read(); m=re.search(r'```json\n(.*?)\n```',t,re.S); d=json.loads(m.group(1)); print('json_ok'); print('overall',d['overall_result']); print('checked',d['declarations_checked'],'verified',d['verified'],'failed',d['failed'],'unverifiable',d['unverifiable'],'findings',len(d['findings']))"; "json_exit=$LASTEXITCODE"
```

Exit code: 0. Output:

```
py_import_exit=0
--- files:

Name                             Length
----                             ------
evidence.md                       24995
exact-head-review-protocol-v1.md  17014
review-case-1278.md               16288

--- json parse:
json_ok
overall FAIL
checked 6 verified 2 failed 4 unverifiable 0 findings 5
json_exit=0
```

Both deliverable files exist and are non-empty; the JSON block parses and its
counts agree with the findings array (5 findings: 4 failed declarations plus the
E2 historical finding; `verified` counts the two E0 declarations D1 and D4a).

## E18. Commands deliberately not run / failures recorded

| command | exit | note |
|---|---|---|
| `git log --all --no-renames --diff-filter=A -- <092 path>` | 0, empty output | did not report the introduction commit; replaced by first-parent `git diff-tree` (§E10) |
| `git merge-base --is-ancestor 27bfa597764281b3abdbe939843b45c14f25b388 HEAD` | 1 | expected: the commit is reachable from `pr1321` / `pr1336` only, not from the candidate |

No command failed in a way that required substituting an expected value; the one
non-zero exit above is a measurement result, not an error.

---

## A. Adjudication appendix (Owner ruling, 2026-11-27)

Nothing above is revised by this appendix. Every command output in §E1–§E18 stands
as recorded; the ruling changes only the grades assigned to those measurements,
and the governing grade set is `review-case-1278.md` §9.1.

Ruling source: `D:\code\chatgpt-session-ops\scripts\accounts\acct3\replies\reply-6b08fa9b-124545.md`,
§1 (prompt `R3-L1-adjudicate.md`). The §1 table as adjudicated:

| checked declaration | final grade | basis |
|---|---|---|
| current `prompt_sha256` declaration | E1 DECLARATION_MISMATCH | declared value ≠ actual SHA-256 at the candidate head |
| current `prompt_bytes` declaration | E1 DECLARATION_MISMATCH | declares 3772 bytes, measured 3714 |
| INDEX same-row repeat | E1 DECLARATION_MISMATCH | the INDEX declaration does not match the reviewed content |
| "exactly four blob versions" | E4 INCOMPLETE_EVIDENCE | five exist; the two reviewers locked different candidate SHAs, which is not sufficient to call a single-review E5 drift |
| no fixed blob field, only the SHA-256 + bytes pair | E4 INCOMPLETE_EVIDENCE | no field binds the declaration to a specific blob; evidence structure incomplete |
| the correction claim "2455 bytes / 9be8aebf… never existed" | E0 VERIFIED | not found in the stated refs/commits/reachable-blob scope; the only 2455-byte object belongs to an unrelated file. The original manifest pin on that value is separately **E2 HISTORICAL_NONEXISTENCE** |
| "3772 bytes / a459d7e5… at first introduction" | E0 VERIFIED | manifest and prompt both first introduced with that byte count and digest |

Also ruled: the protocol classes "exactly four versions" as a `COUNT_ASSERTION`
(bound to candidate SHA, explicit scan envelope, itemised enumeration; E5 only if
the locked candidate itself changes during one review).

### A.1 Divergence items settled

| item | L2-B | L3-1 | ruling | why it diverged |
|---|---|---|---|---|
| current `prompt_sha256` | E1 | E1 | E1 | agreed; measurement from §E4/§E5 is unchanged |
| current `prompt_bytes` | E1 | E1 | E1 | agreed; 3772 declared vs 3714 measured (§E4, §E5) |
| INDEX same-row repeat | E1 | E1 | E1 | agreed; §E14 shows the row repeats the same pair |
| "exactly four versions" | E4 | E5 | **E4** | reviewers locked different candidates (`987d2602…` vs `10d33b3f…`); each candidate was stable inside its own review, so no single-review E5 exists. Five versions exist (§E8/§E9), so the count is incomplete |
| fixed blob field | (absent) | (absent) | **E4** | new row: the manifest declares only the digest+bytes pair, no blob pin (§E3) |
| "2455 / `9be8aebf…` never existed" | E0 | E0 | E0 | agreed; §E8/§E9 report 0 digest hits, §E11/§E12 show 3772/`a459d7e5…` at the declaring commit |
| "3772 / `a459d7e5…` at first introduction" | E0 | E0 | E0 | agreed; §E11, §E12 |
| registration pin `9be8aebf…`/2455 | E2 | E2 | **E2** | ruled separately from the negative claim: the pin asserts an existence that the envelope does not contain |
| `prompt_file` / `prompt_id` | E0 / E0 | E0 / E0 | not in ruling table | not adjudicated; retained as raw history only |
| H2 attribution | E0 | — | not in ruling table | not adjudicated; retained as raw history only |

Grade totals after adjudication (Head A `987d2602`, its own eight rows, retained
unchanged): E0 ×2, E1 ×3, E2 ×1, E4 ×2 — `verified 2 / failed 4 / unverifiable 0 /
incomplete 2 = 8`, `overall_result FAIL`.

Corrected bucket counts, at the submission head `c7d56bbe` over nine declarations:
E0 ×4 (F1, F2, F6, F7), E1 ×1 (F3), E2 ×1 (F8), E3 ×1 (F9), E4 ×2 (F4, F5) —
`verified 4 / failed 3 / unverifiable 0 / incomplete 2 = 9`, `overall_result FAIL`.
The total moved from 8 to 9 because one new finding was added — F9, the E3
attribution mismatch on `manifest.yaml:36-37` — not because a measurement was
replaced: the F4 enumeration was also corrected (five versions to seven non-empty
versions, `review-case-1278.md` §2.3.4) and stays in `incomplete`, so no bucket
moved on its account. At Head D `5e30d497` the counts are `5 / 2 / 0 / 2 = 9`,
with F3 closed by #1452; the per-head table is `review-case-1278.md` §7.3.

The bucketing convention used here (E1/E2/E3 → `failed`, E4/E5 → `incomplete`,
E6 → `unverifiable`) is the one carried by the case record's JSON block. The
superseded `unverifiable 2` line this appendix previously ended with counted E4 as
unverifiable; it no longer describes any head's counts.

The E4 row above and the divergence table in §A.1 are the adjudication record as
issued and are reproduced verbatim; the corrected enumeration changes the count
inside that row's rationale, not its grade.
