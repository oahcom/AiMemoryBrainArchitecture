# E Owner — JF-10 Executable Reference Model Consumption

- Status: **REFERENCE-MODEL MAPPING / OWNER REVIEW REQUIRED**
- Model source: Storage Owner branch, `reviews/storage-consistency/reference_model/jf10_linearization_model.py`
- Scope: logical stable identity and retry semantics only; not production E implementation.

## E-owned behavior represented

The reference model's `ProducerManifest` binds one WorkItemId to one immutable PublicationOperationId and manifest digest. Repeated execution attempts may vary AttemptId without changing publication identity. Rebinding a WorkItemId to another operation or changing its frozen manifest digest is rejected.

This is the logical behavior covered by JF10-E-16. The Storage participant model also carries the immutable operation and manifest digest into the visibility publication.

## Required production mapping

E implementation must identify the durable frozen output/lineage manifest, WorkItemId and PublicationOperationId generation, AttemptId/LeaseEpoch retry fencing, manifest digest canonicalization, and the exact handoff to Storage. E must not claim Published based on producer completion or staged object existence.

## Explicit non-claims

This model does not implement E's durable compiler ledger, artifact store, manifest canonicalization, retry scheduler, lease service, or Storage integration. It does not pass E36 or JF10-E-16. E owner review and production-equivalent evidence remain required.
