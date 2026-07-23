---
title: Canonical Public Data Contracts
reference_namespace: D
status: approved
authority: architecture-decision
owner_repository: AICincy/HCJC2
document_family: decisions
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Architecture decision governing the subject stated below.

# D-6 Canonical Public Data Contracts

- Status: Accepted
- Accepted: 2026-07-21
- Date: 2026-07-20

## Context

V1 publishes multiple useful JSON and RSS surfaces, but only the current roster has a schema version. The public formats use inconsistent envelopes, ambiguous source strings, opaque compact fields, and incomplete provenance. Several capped feeds do not declare truncation. One mixed changelog contains incompatible record shapes.

HCJC2 ingestion, correlations, the public data plane, and the frontend need one versioned contract system.

## Decision

HCJC2 will:

1. Preserve immutable source observations separately from normalized public records.
2. Use descriptive versioned JSON contracts for every artifact.
3. Identify custody episodes separately from source person identifiers.
4. Publish release, source-status, provenance, completeness, and result-window metadata.
5. Use typed normalized dates and money while retaining source text.
6. Use separate identified and anonymized activity artifacts.
7. Use GeoJSON for public map features.
8. Generate the public data catalog from the feed registry.
9. Reference versioned offense assessments and correlation assessments rather than embedding untraceable classifications.

## Rejected alternatives

### Copy V1 shapes and add fields later

Rejected because clients would inherit ambiguous identifiers and incompatible envelopes.

### One universal flat record

Rejected because custody records, open-data incidents, correlations, and aggregate history have different semantics and retention rules.

### Publish raw provider data only

Rejected because provider fields drift, source types remain ambiguous, and field-level publication controls cannot be enforced consistently.

## Consequences

The initial implementation requires schema validation, migration adapters, fixture generation, and consumer compatibility tests before frontend development. This cost reduces later coupling and prevents ingestion quirks from becoming permanent public API behavior.
