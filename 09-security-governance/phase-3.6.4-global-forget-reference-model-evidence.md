# I Phase 3.6.4 — Global Forget Inventory/Completion Reference Model Evidence

- Branch HEAD: `73a0bff13b531b5b9feaeeec1887db31d6266589`
- Model: `09-security-governance/tests/global_forget_model.py`, Blob `5233da028e409ec3f41848582dad73a923e7155b`
- Tests: `09-security-governance/tests/test_global_forget_model.py`, Blob `091f9450adf49a2a9f9ec8a2fa4470918023f765`
- Workflow: `.github/workflows/i-global-forget-reference-model.yml`, Blob `2c16ef5381dd271789912e9b1c1e5c12941d2826`
- CI run: `43962873109`; job `133634616584`; commit `73a0bff13b531b5b9feaeeec1887db31d6266589`
- Result: **25/25 TESTS PASS**

## 1. Covered logical invariants

1. Only I inventory authority can seal; registry gaps and empty/unproven inventory are rejected.
2. Every target requires owner, exact ScopeRef coverage, capability profile and required action.
3. Inventory epoch changes/new target registration invalidate the prior seal and reopen the operation.
4. Evidence binds exact operation, current seal, inventory epoch, target, owner, scope, action, capability and integrity.
5. Adapter request receipt is not delete ACK; unsupported/offline/timeout remains Unknown.
6. D barrier, suppression, backup restore safety, every target and every CEV component are mandatory for completion.
7. Backup restore requires quarantine, current control-ledger replay and suppression revalidation.
8. Physical erasure requires an explicit PHYSICAL_ERASURE action; ordinary suppression is insufficient.
9. PolicyException requires an authorized independent approver, exact scope, reason, signed evidence and unexpired time; expired exceptions reopen.
10. NotApplicable requires positive absence proof and independent reviewer.
11. A prior failure cannot be overwritten by a later ACK without owner resolution.
12. F/owner-local evidence cannot claim global completion.

## 2. Exact CI result

Workflow run `43962873109` concluded SUCCESS. The raw job log reports 25 tests in 0.002 seconds and `OK`.

## 3. Limits

This is an in-memory logical reference model. It does not populate or authenticate a production ProducerDomainInventoryEpoch registry, create a real TargetInventorySeal, execute D/E/F/G/H/Storage APIs, verify real external recipient deletion, run a production backup restore, authorize I36-GOV-01..10, approve PolicyException, or prove physical erasure. Global Forget remains OPEN / NOT COMPLETED.
## 4. Expanded terminal-state and reopening coverage — 2026-11-17

The suite was extended with five additional cases: empty inventory cannot be sealed; a valid approved exception yields CompletedWithPolicyException; a positively evidenced NotApplicable target can satisfy only its own target slot; Failed target blocks completion; and a newly discovered target after a previously Completed operation forces Reopened. The updated test Blob is `428e15c6263b5b2d730b93ce5412d55e782a449b`.

Latest exact CI: run `43963450717`, job `133636592112`, commit `8a6a6e67696c496e265b3d87f1a550fe5e8bb2a0`; **30/30 tests PASS**.