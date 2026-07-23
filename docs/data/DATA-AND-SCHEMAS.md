---
title: Data and Schemas
reference_namespace: V2
status: approved
authority: v2-data
owner_repository: AICincy/HCJC2
document_family: data
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-11
  relation: constrained-by
  to: D-6
- from: V2-11
  relation: refines
  to: A-3
- from: V2-12
  relation: requires
  to: A-17
- from: V2-13
  relation: refines
  to: A-2
- from: V2-14
  relation: refines
  to: A-7
- from: V2-18
  relation: refines
  to: A-12
- from: V2-19
  relation: refines
  to: A-19
- from: V2-19
  relation: refines
  to: A-20
- from: V2-22
  relation: requires
  to: A-22
- from: V2-24
  relation: requires
  to: A-21
---

# Data and Schemas

> **Authority:** Approved controlled HCJC2 data specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 data and schemas requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-11 Canonical Public Contracts

Every public artifact uses a versioned schema family and common release metadata. See [D-6 Canonical Public Data Contracts](../decisions/ADR-006-CANONICAL-DATA-CONTRACTS.md#d-6-canonical-public-data-contracts).

## V2-12 Common Release Metadata

Artifacts identify schema version, release ID, generation time, source observation time, source status, completeness, truncation, record count, and manifest route.

## V2-13 Immutable Source Observations

Raw source values, identifiers, wording, and observation times are preserved before normalization or assessment.

## V2-14 Versioned Custody Episodes

A custody episode receives a deterministic, versioned project identifier that is stable across repeated observations and collision-tested.

## V2-15 Typed Date and Time Values

Normalized time values retain source text, timezone, precision, and uncertainty. Date-only values are not represented as exact midnight events.

## V2-16 Explicit Unknown States

Known, omitted, source-unknown, not-applicable, parse-failed, pending-review, withheld, and unresolved states remain distinguishable.

## V2-17 Typed Monetary Values

Money retains source text, normalized amount, currency, and interpretation status.

## V2-18 Identifier Scope

Person references, source inmate identifiers, bookings, custody episodes, court cases, incidents, dispatch events, relationships, and activity events remain distinct.

## V2-19 Completeness and Truncation

Bounded artifacts disclose ordering, known total, returned count, configured limit, time window, and truncation.

## V2-20 GeoJSON Map Contract

Map output uses GeoJSON with stable source identifiers, event type, time, agency, location precision, uncertainty, inclusion reason, and release ID.

## V2-21 Versioned Feed Registry

Runtime acquisition configuration and public feed documentation derive from one versioned feed registry.

## V2-22 Public Field Allowlists

Every public record and feed is restricted to an explicitly reviewed public field allowlist.

## V2-23 Separated Activity Surfaces

Identified current activity, anonymized history, and aggregate trends use separate artifacts and schemas.

## V2-24 Assessment Provenance

Derived offense labels, correlations, and normalized values identify the ruleset, source observations, and assessment versions that produced them.

## Related decisions, contracts, schemas, tests, and evidence

- [Canonical Public Data Model](CANONICAL-PUBLIC-DATA-MODEL.md)
- [Feed Registry](FEED-REGISTRY.md)
- [Artifact Classification and Retention](ARTIFACT-CLASSIFICATION-RETENTION.md)
- [D-6 Canonical Public Data Contracts](../decisions/ADR-006-CANONICAL-DATA-CONTRACTS.md)

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
