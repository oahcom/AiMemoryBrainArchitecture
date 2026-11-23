---
document_metadata:
  domain: ai-development
  role: research

  lifecycle:
    approval:
      decision_status: Draft
      approver: null
    evidence_verification:
      verification_status: Verified
      last_verified_date: "2026-11-23"
      last_verification_note: "Read from the Actions API and the job logs, not from a summary. Run 45029496435 job 137229717562 log line 4: 'Runner is running behind proxy server http://127.0.0.1:17891 for all HTTPS requests.' Checkout timestamps per job from /actions/runs/{id}/jobs: run 45029496435 checkouts at 14:14:49, 14:15:58, 14:17:18, 14:19:20 all failure and 14:20:39 success; run 45032280121 at 14:25:24 success then 14:27:03, 14:28:12, 14:29:27 all failure. Disk run 45028386409 job 137226328804 printed 'free_disk_kb=2340276 free_disk_gb=2 refuse_below_gb=3'. AMENDED 2026-11-23 (section 1a): run 45104020193 jobs 137461070517 and 137461070552 failed at checkout with 'GnuTLS, handshake failed: The TLS connection was non-properly terminated' at 11:18:50Z, 11:19:39Z, 11:19:54Z while the proxy port was accepting connections; the later steps of both jobs are skipped, so neither job examined the commit."
    usage_status: Active
    modification_status: Unchanged
    supersession:
      supersedes: []
      supersession_reason: null

  authority:
    canonical_status: Non-Canonical
    canonical_conflict_status: None
    normative_status: Informative
---

# GAP-30 — the runner's proxy flaps, and takes every checkout with it

> **Amendment 2026-11-23.** §1 and §2 below were written from 11-22. The same runner produced a *different* error on the same port the next day, so the section after this block was added rather than the original rewritten. The original observation was correct; it was incomplete. See §1a.


**Status:** Open — not repaired here
**Area:** runner host, not repository code
**Found at:** `Existing gates` red on `main` for three consecutive commits
**Measured at:** `main` @ `84056315`, `1f045334`, `ec2d580e`

---

## 1. The failure, in the runner's own words

Run `45029496435` (`1f045334`), job `137229717562` (`Rust clippy (hard gate)`), printed this before doing anything:

```
Runner is running behind proxy server 'http://127.0.0.1:17891' for all HTTPS requests.
```

and then, at step 3, three times:

```
##[error]fatal: unable to access 'https://github.com/oahcom/AiMemoryBrainArchitecture/':
Failed to connect to github.com port 443 via 127.0.0.1 after 0 ms: Could not connect to server
The process '/usr/bin/git' failed with exit code 128
Waiting 12 seconds before trying again
... Waiting 19 seconds before trying again
```

`after 0 ms` is the load-bearing part. A refused connection, not a timeout: nothing was listening on the proxy port. The proxy process itself was gone, and GitHub was never contacted.

## 1a. The same port, a different failure, the next day

On `2026-11-23` the runner was still behind the same proxy and still failing checkouts, but with the opposite symptom. Run `45104020193` (push of `443b75a3`), job `137461070517` (`Rust clippy (hard gate)`):

```
Runner is running behind proxy server 'http://127.0.0.1:17891' for all HTTPS requests.
##[error]fatal: unable to access 'https://github.com/oahcom/AiMemoryBrainArchitecture/':
GnuTLS, handshake failed: The TLS connection was non-properly terminated.
... (three attempts, 11:18:50Z, 11:19:39Z, 11:19:54Z)
##[error]The process '/usr/bin/git' failed with exit code 128
```

Job `137461070552` (`Bilingual docs coverage (ratchet)`) failed identically, at the same step.

This is worth a separate section because it breaks the diagnosis that §1 invites. The two failures look like one problem and are not:

| | 11-22 (`after 0 ms`) | 11-23 (`GnuTLS handshake failed`) |
|---|---|---|
| proxy process | gone — nothing listening | present and accepting |
| TCP connect | refused | succeeded |
| TLS | never reached | started, then torn down mid-handshake |
| reading | the proxy is down | the proxy is up and mangling traffic |

An operator who saw only the 11-22 symptom would conclude "start the proxy". That action does nothing for the 11-23 symptom, in which the proxy is already running. The common factor is not the proxy's liveness but that **the runner's only egress path is a single local process whose failures surface as three unrelated error strings in front of a checkout step.**

Both are also indistinguishable, at check level, from a checkout that failed because the change broke something. `Rust clippy` reported `failure` on `443b75a3` while `cargo clippy` never ran; step 7 is `skipped`, and so are steps 4, 5 and 6. Nothing about the commit was examined.

## 2. It is a flap, not a direction

Job start times on this runner do not overlap — one job at a time, five gates in sequence. Reading the checkout outcome by time rather than by job name shows a window, not an ordering:

| run | commit | checkout outcomes, in time order |
|---|---|---|
| `45029496435` | `1f045334` | `14:14:49` fail · `14:15:58` fail · `14:17:18` fail · `14:19:20` fail · **`14:20:39` success** |
| `45032280121` | `ec2d580e` | **`14:25:24` success** · `14:27:03` fail · `14:28:12` fail · `14:29:27` fail |
| `45104020193` | `443b75a3` | `11:18:50Z` fail · `11:19:39Z` fail · `11:19:54Z` fail (GnuTLS, §1a) |

The proxy was down from before `14:14:49` until somewhere in `14:19:20`–`14:20:39`, came back, and went down again by `14:27:03`. That is two flaps inside eleven minutes. The next day, at `03:06:52Z`, every self-hosted checkout in that push run succeeded — and at `03:18:50Z` two of them failed again, with the TLS symptom rather than the refused-connection one. Whatever the proxy is doing, it is still doing it. "The first job always works" and "the last job always works" are both refuted by the two rows above, which is why the ordering explanation was tempting and wrong.

## 3. The retries cannot reach it

`actions/checkout` retries three times, waiting 12s then 19s — 31 seconds of coverage, and the three attempts are `14:15:58.997`, `14:16:11.011`, `14:16:30.026`. The flap outlasted them by minutes. Raising the retry count is the obvious move and the wrong one: covering a six-minute flap from inside one step means hanging a job for six minutes on an unrelated host, on a runner with 3.6G RAM and one worker.

**Bypassing the proxy is worse than the flap.** `no_proxy=github.com` would trade a diagnosed failure for an undiagnosed one on a network that very likely cannot reach GitHub directly — the port `17891` is a local forward proxy, and it exists for a reason. Nothing in this repository should encode a guess about that reason.

## 4. What is actually actionable

Two things, in this order, and the second is only worth doing after the first.

1. **Name the cause in the annotation.** Today a proxy flap reports as `Run actions/checkout@v4 failure`, which is byte-identical in shape to a checkout that failed because the diff broke something. It cost three separate investigations to establish that three red runs on `main` said nothing about `main`. A first step — before `actions/checkout`, since it needs no workspace — that checks the proxy and fails with `the runner's egress proxy 127.0.0.1:17891 is not usable; this run executed no check and says nothing about the code` converts a log dig into a sentence.

   §1a is why that check cannot be a TCP connect. On 11-23 the port accepted connections and the TLS handshake was torn down, so `nc -z 127.0.0.1 17891` would have declared the proxy healthy immediately before three failed checkouts. The probe has to be an actual HTTPS request through the proxy — `git ls-remote` against this repository is the cheapest one that exercises the same path `actions/checkout` is about to use.
2. **Wait for the proxy rather than fail on it**, bounded. The same probe can poll for up to a stated budget and proceed when the proxy answers. A flap then costs a delay instead of a red run.

Neither belongs in `gates.yml` alone. Every self-hosted job pays this cost at step 3, so the probe belongs wherever the jobs are defined together, or it will be added to one workflow and forgotten in the rest.

### Why waiting here is not the self-healing `#702` forbids

`runner-disk-reclaim.yml` (`ec2d580e`) refuses to reclaim automatically, and its reasoning is correct: *"A self-healing probe is not a probe."* The disk floor measures the repository's own trend, and healing it silently would erase the signal before anyone read it.

The proxy is the opposite case on the axis that matters. The disk number is a **measurement about this repository** — it is going to zero, and a human has to decide what to delete. The proxy is **transport**, it measures nothing about the repository, and the decision it needs was already made when the proxy was installed. Waiting for it is the same class of action as the 12-second and 19-second retries `actions/checkout` already performs; the only difference is that those are too short for the outage they meet. Nothing is hidden by waiting, because nothing was being reported.

## 5. The other cause, which is not this one

`84056315` was also red, and for a different reason. Four of five jobs passed; `Rust clippy` failed at `Check free disk before building`, not at checkout:

```
free_disk_kb=2340276 free_disk_gb=2 refuse_below_gb=3
##[error]only 2G free (2340276 KiB), below the 3G floor. A clippy build costs ~1.0-1.3G
and this is the repository's only runner. Reclaim space and re-run; do not lower
GATES_MIN_FREE_GB to get a green.
```

`#702` then added a manual reclaim tool, which keeps the floor honest but leaves the leak. Recorded here only so the three red runs are not described as one cause: two of them were the proxy, one was a 2 GiB disk, and **none of the three was about the code.**

## 6. Why this is worth a document rather than a re-run

The repository has already written the principle down twice. `gates.yml`'s header says a gate that fails on the image rather than the code "reports on the image, not on the code — and it reports that forever, on every run, which is precisely how a gate trains everyone to ignore it." `GAP-25` says a degraded check and a passing check produce the same output shape.

A flapping proxy is the same defect one layer down, and it is currently indistinguishable from a regression. The cost is not the failed run; it is every verification cycle spent deciding whether a red run meant anything.
