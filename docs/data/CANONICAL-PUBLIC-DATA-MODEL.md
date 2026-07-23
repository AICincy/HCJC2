---
title: Canonical Public Data Model
reference_namespace: V2
status: approved
authority: v2-canonical-data-model
owner_repository: AICincy/HCJC2
document_family: data
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Approved controlled extension for the HCJC2 data documentation family.

# Canonical Public Data Model

## Contract objectives

The canonical model provides one vocabulary for ingestion, correlation, public data, and frontend use. It does not force every source into one flat record.

## Common artifact metadata

Every public JSON artifact must include:

| Field | Requirement |
|---|---|
| `schema_uri` | Stable URI for the JSON Schema |
| `schema_version` | Semantic version of the artifact contract |
| `dataset_id` | Stable HCJC2 dataset identifier |
| `release_id` | Immutable release identifier from the data plane |
| `generated_at` | UTC time when HCJC2 generated the artifact |
| `source_status` | Structured source condition and freshness |
| `provenance` | Source, acquisition, transformation, and ruleset references |
| `record_count` | Number of records included |
| `result_window` | Query bounds, limits, returned count, and truncation state |

The release manifest carries object hashes, sizes, media types, and paths.

## Identity model

### Source subject reference

A source subject reference preserves the official identifier without claiming that it is a universal person identity.

```json
{
  "namespace": "hcso.inmate_number",
  "value": "1234567"
}
```

### Custody episode identifier

A custody episode represents one continuous custody occurrence.

Preferred deterministic input:

```text
source system + inmate number + booking number
```

Fallback input when the booking number is unavailable:

```text
source system + inmate number + normalized booking date + first observation identifier
```

The record must declare the derivation method. A later official booking number may become an alias without changing previously published event identifiers.

## Roster snapshot

A roster snapshot contains only active source-reported custody episodes approved for publication.

Each episode separates:

- official source identifiers
- source-reported identity fields
- custody dates
- current charges
- current holder status
- photo availability
- observation timestamps
- normalized assessments
- provenance

The public model preserves source strings under `source_observation` and provides typed values under `normalized`.

## Dates and times

Every normalized temporal value uses:

- ISO 8601
- an explicit timezone or `date` precision
- `precision`: `instant`, `minute`, `date`, `month`, or `unknown`
- `source_text`
- `unknown_reason` when no normalized value exists

The model never converts `NA`, `TBD`, `NONE`, or `1/1/70` into a real date.

## Money

A bond amount uses integer minor units:

```json
{
  "amount_minor": 250000,
  "currency": "USD",
  "source_text": "$2,500.00",
  "status": "reported"
}
```

Unknown, nonmonetary, percentage, and conditional bond values use explicit status values instead of zero.

## Charges

A charge record contains:

- stable charge record ID
- source case references by court system
- source offense code and description
- source bond and disposition text
- normalized offense observation
- optional reviewed authority reference
- optional offense assessment
- court event dates with precision
- provenance

A charge assessment remains separate from the source observation and references the taxonomy and ruleset version.

## Activity events

Activity events use immutable event IDs and a discriminated event type. Supported initial types:

- `custody.booked`
- `custody.released`
- `custody.updated`
- `source.degraded`
- `source.recovered`
- `correlation.published`
- `correlation.withdrawn`
- `record.corrected`

Identity-bearing events and anonymized aggregate events use separate artifacts and retention policies.

## Source status

Every dataset reports:

- operational state
- source-observed time
- last successful acquisition
- freshness age
- expected refresh interval
- completeness state
- degradation reason
- cached artifact use

Allowed initial operational states:

- `current`
- `delayed_upstream`
- `source_paused`
- `source_frozen`
- `cached_after_fetch_failure`
- `conditional_empty`
- `derived`
- `retired`

## Search view

The search artifact is a derived projection, not an authority record. It includes descriptive names, custody episode IDs, booking dates, primary assessment references, photo availability, and the release ID.

The search view must not contain a legal classification unless a versioned assessment supports it.

## Map view

The map artifact uses GeoJSON. Each feature includes:

- stable feature ID
- relationship to a source record
- event type
- event time with precision
- location precision
- public display fields
- source status
- provenance reference

The artifact declares the candidate count, included count, sort policy, cap, and truncation state.

## Compatibility rules

1. Additive optional fields require a minor schema version.
2. Removed fields, renamed fields, changed meaning, or stricter required fields require a major version.
3. Producers validate artifacts before upload.
4. Consumers reject unsupported major versions.
5. Old schemas remain available while any retained release references them.
6. Every schema change includes migration notes and contract fixtures.
