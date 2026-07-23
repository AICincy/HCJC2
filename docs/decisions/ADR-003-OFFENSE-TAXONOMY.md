---
title: Separate Offense Record Classes
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

# D-3 Separate Offense Record Classes

- Status: Accepted
- Accepted: 2026-07-21
- Date: 2026-07-20

## Context

V1 stores 1,888 code entries in one `{title, degree}` map. The build automatically adds entries from current charge descriptions and retained court-listing captures. Missing degree text defaults to `MM`. The map mixes official statutes, municipal provisions, placeholders, malformed identifiers, and source artifacts.

Several Ohio statutes have conditional classifications that cannot be represented by one degree. The same base section can range across misdemeanor and felony degrees.

## Decision

HCJC2 will implement four versioned record classes:

1. immutable source observations
2. curated legal-authority records
3. curated analytical concept records
4. generated charge assessments

The build and ingestion pipeline may create observations and assessments. They may not create or modify authority or concept records.

A degree result requires an explicit applicability rule and sufficient facts. Otherwise the result is unknown. Missing degree never defaults to `MM`.

## Consequences

- Initial implementation is more explicit than a flat lookup.
- Legal and analytical changes become auditable.
- Correlation features can distinguish verified authority from weak text similarity.
- Public pages can explain uncertainty instead of displaying false precision.
- Unknown and conflict rates become visible operational metrics.
- A separate reviewed curation workflow is required.

## Rejected alternatives

### Copy V1 lookup

Rejected because it mixes jurisdictions, mutates during build, and stores unsupported degree defaults.

### Keep one section-level default degree

Rejected because many statutes require subsection facts, amounts, victim facts, prior records, or other elements.

### Infer degree only from court venue

Rejected because venue is useful evidence but not a complete statutory classification.

### Use NIBRS as the primary legal taxonomy

Rejected because NIBRS is an incident-reporting classification, not the legal authority governing an Ohio booking charge. It may be used as an approved analytical crosswalk.
