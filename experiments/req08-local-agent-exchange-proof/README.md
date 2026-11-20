# REQ-08 local cross-agent exchange proof (experimental)

**Status: experimental evidence only; not a normative contract.** This fixture is isolated from BMCP, the Rust workspace, and product runtime. It does not freeze a portable exchange format or establish production authentication/authorization.

## What runs

The exchange_demo.py program starts a sender process and a receiver process. The sender identifies itself as agent.alpha on provider-a/model-alpha; the receiver is agent.beta on provider-b/model-beta. A JSON payload crosses the process boundary through standard input/output. The receiver checks an explicit fixture grant before accepting the memory and reports preserved source-agent/provider/model/record provenance.

The fixture grant is test data, not a cryptographic credential. The human.fixture.owner principal is not a real authenticated identity. No live model inference or external provider API is called: provider/model labels demonstrate heterogeneous adapter metadata only. The experiment does not prove cross-model semantic equivalence.

## Run

```sh
python3 experiments/req08-local-agent-exchange-proof/exchange_demo.py
python3 -m unittest discover -s experiments/req08-local-agent-exchange-proof -p 'test_*.py' -v
```

The tests cover successful cross-agent transfer, tenant mismatch, wrong grantee/audience, revoked grant, payload tampering, transport-source spoofing, resource substitution, an ungranted action, and a missing delegation chain.

## Deliberate limits

- No BMCP changes, production adapters, real credentials, external model calls, or deployment.
- The experiment envelope is local fixture plumbing only; it is not a schema proposal or exchange-format freeze.
- Authorization semantics are illustrative test predicates pending Stage A architecture stabilization and competent authority review.
- Passing tests prove only these fixture behaviors, not absence of vulnerabilities or production security conformance.
