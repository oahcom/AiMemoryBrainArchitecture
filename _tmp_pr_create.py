import json
import os
import re
import subprocess

creds = open(os.path.expanduser("~/.git-credentials"), encoding="utf-8").read()
token = re.search(r"gho_[A-Za-z0-9]+", creds).group(0)
body = open("_pr_body.md", encoding="utf-8").read()
payload = json.dumps({
    "title": "fix(session-evidence): exempt undeclared pre-effective PRs before enforcing the body contract",
    "head": "fix/1026-session-evidence-exemption",
    "base": "main",
    "body": body,
    "draft": False,
}).encode()

out = subprocess.run(
    ["curl", "-s", "-X", "POST",
     "-H", f"Authorization: Bearer {token}",
     "-H", "Accept: application/vnd.github+json",
     "-H", "Content-Type: application/json",
     "--data-binary", "@-",
     "https://api.github.com/repos/oahcom/AiMemoryBrainArchitecture/pulls"],
    input=payload, capture_output=True,
).stdout.decode()
data = json.loads(out)
print(data.get("number"), data.get("html_url"))
print(data.get("message") or "", data.get("errors") or "")
print((data.get("head") or {}).get("sha"))
