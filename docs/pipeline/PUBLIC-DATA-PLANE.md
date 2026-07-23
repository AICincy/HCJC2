---
title: Public Data Plane
reference_namespace: V2
status: approved
authority: v2-public-data-plane
owner_repository: AICincy/HCJC2
document_family: pipeline
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Approved controlled extension for the HCJC2 pipeline documentation family.

# Public Data-Plane Contract

## Purpose

Define the logical public interface, storage model, promotion rules, rollback behavior, caching, CORS, retention, deletion, and failure semantics for HCJC2 public data.

## Public routes

| Route family | Description | Cache policy |
|---|---|---|
| `/v1/status.json` | Current run, source, freshness, and publication status | `max-age=15, s-maxage=30` |
| `/v1/manifest.json` | Current approved artifact manifest | `max-age=30, s-maxage=60` |
| `/v1/roster.json` | Current normalized custody roster | `max-age=60, s-maxage=300` |
| `/v1/activity.json` | Current booking, release, and material-change activity | `max-age=60, s-maxage=300` |
| `/v1/correlations.json` | Current publishable correlation assessments | `max-age=60, s-maxage=300` |
| `/v1/feeds/{feed}.json` | Current approved supplemental feed | Feed-specific, maximum 15 minutes |
| `/v1/photos/{public_photo_id}` | Current active-roster photo | `max-age=60, s-maxage=300` |

The public interface must not expose internal bucket keys, source credentials, release prefixes, evidence logs, retained prior rosters, or review-only correlation data.

## Release layout

```text
releases/{release_id}/
  manifest.json
  status.json
  roster.json
  activity.json
  correlations.json
  feeds/*.json
```

Photos are excluded from release prefixes and live in a separate current-only bucket.

## Release identifier

`release_id` must be a sortable UTC timestamp plus a digest prefix:

```text
20260720T193000Z-4f8a1c92
```

## Pointer

The control pointer identifies exactly one approved release and its manifest digest. It must be small, schema validated, conditionally written, and independently readable by the Worker.

## Promotion invariants

1. Every release object is uploaded before promotion.
2. Every object digest matches the manifest.
3. The manifest digest matches the pointer.
4. The release passes data, privacy, schema, freshness, and correlation gates.
5. Pointer replacement is conditional on the expected prior ETag or version token.
6. Only one publisher may promote at a time.
7. Public verification occurs after pointer update.
8. A failed verification triggers hold or rollback, never silent continuation.

## Cache invariants

- Release objects are immutable and may use a one-year private-origin cache policy when addressed internally.
- Logical public routes use short browser TTLs.
- Worker cache keys include the approved release identifier.
- Pointer promotion purges logical routes, not immutable release objects.
- Photo deletion purges the exact photo URL.
- Cached 404 responses must not prevent newly approved files from appearing.

## CORS

- Allow only the production application origin and explicitly approved development origins.
- Permit `GET`, `HEAD`, and `OPTIONS` only.
- Do not use wildcard origins for production custody data.
- Expose `ETag`, `Last-Modified`, `Content-Length`, `X-HCJC2-Release`, and `X-HCJC2-Manifest`.
- Cache preflight responses for a bounded period.

## Integrity headers

Every successful data response must include:

- `ETag`
- `X-Content-Type-Options: nosniff`
- `X-HCJC2-Release`
- `X-HCJC2-Manifest`
- `X-HCJC2-Generated-At`
- `X-HCJC2-Source-Status`
- appropriate `Cache-Control`

## Failure behavior

| Failure | Public behavior | Operator action |
|---|---|---|
| Pointer missing or invalid | `503` with no roster body | Alert and restore last validated pointer |
| Manifest digest mismatch | `503` | Quarantine release and investigate |
| Requested artifact absent from manifest | `404` | No bucket fallback |
| Current release object missing | `503` | Roll back pointer |
| Source is stale but last-known-good remains valid | Serve approved release with stale status | Alert based on threshold |
| Photo object missing | `404` | Do not substitute another person's photo |
| Worker limit or runtime failure | Fail closed | Alert and use documented recovery path |

## Retention

- Public-current photos: retain only while the corresponding roster record remains active.
- Private release JSON: provisional seven-day operational rollback retention, subject to privacy and legal review.
- Public aggregate history: separate de-identified contract.
- Internal evidence: separate bucket, credentials, and retention schedule.
- No indefinite lock may apply to current photos or deletable personal-data releases.

## Observability

Each response and publication run must be traceable by:

- request or run identifier,
- release identifier,
- manifest digest,
- Worker version,
- publisher version,
- source status,
- cache status,
- HTTP status,
- latency,
- error class.
