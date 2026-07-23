# V1 Public Data Contract Audit

- Audit snapshot: `Sol-072026.zip`
- Snapshot roster time: `2026-07-20T18:34:22Z`
- Scope: public JSON, RSS, search, map data, model definitions, output generators, and public data documentation
- Method: static source inspection plus direct shape and count analysis of the supplied snapshot

## Inventory

| Surface | V1 shape | Records in snapshot |
|---|---|---:|
| Current roster | `data/current.json` | 1,283 people, 5,036 charges |
| Identified changelog | `data/changelog.json` | 10,000 events |
| Anonymizing changelog | `data/anon_changelog.json` | 4,092 rows |
| Daily history | `data/history.json` | 70 rows |
| Public search | `docs/search.json` | 1,283 rows |
| Public map | `docs/dispatches.json` | 600 points |
| Supplemental feeds | 11 `*recent.json` files | 19,900 published rows |
| RSS | `feed.xml`, `booked.xml`, `released.xml` | Up to 50 items each |

## Findings

| ID | Severity | Finding | Evidence | V2 disposition |
|---|---|---|---|---|
| F13 | High | Only `current.json` carries a schema version. All other public JSON surfaces can change shape without a machine-readable compatibility signal. | `Snapshot.schema_version` exists in `scraper/models.py`; the other inspected payloads omit it. | Replace with versioned schemas for every public artifact. |
| F14 | High | Public datasets use incompatible envelopes and count names. | Roster uses `inmate_count`; search and map use `count`; supplemental feeds use `row_count`; changelogs and history are bare arrays. | Standardize release metadata, record counts, status, provenance, and truncation fields. |
| F15 | High | Dates, money, unknown values, and source sentinels remain ambiguous strings. | HCSO dates accept source strings and sentinels such as `NA`, `TBD`, and `1/1/70`; bond amounts remain strings. | Preserve raw observations, add typed normalized values, precision, timezone, and explicit unknown reasons. |
| F16 | High | The model does not identify custody episodes explicitly. | `inmate_number` serves as the person key, page key, changelog key, and photo key. `booking_number` is optional and two active rows lacked it. | Introduce source subject references and deterministic custody episode identifiers. |
| F17 | High | Three supplemental feeds contain exactly the configured 5,000-row limit without a truncation flag. | `use_of_force_pdi_recent`, `traffic_stops_drivers_recent`, and `pedestrian_stops_recent` each contain 5,000 rows. | Publish query window, order, limit, returned count, truncation state, and continuation strategy. |
| F18 | Medium | Public documentation does not match the traffic-stop and pedestrian-stop implementation. | The template says about 30 days and 12-hour refresh. `open_data_feeds.py` performs unfiltered latest-5,000 pulls and uses 24-hour caching. | Generate documentation from the feed registry and test it against runtime configuration. |
| F19 | High | `anon_changelog.json` places two incompatible record shapes in one unversioned array. | 2,961 rows have `{event,date,tier,category}` and 1,131 have identity-bearing timestamped fields. | Separate identified, anonymized, and aggregated event contracts or use a discriminated union. |
| F20 | Medium | Search and map formats use opaque compact field names and omit source provenance. | Search uses `n,c,t,b,id`; map uses `la,lo,k,d,a,n,t`. | Use descriptive names and source record references. Compression belongs at the transport layer. |
| F21 | High | The map artifact silently drops records and cannot explain which records were omitted. | `_dispatch_points` appends CFS rows before shooting rows, then returns `pts[:600]` without a declared sort or source IDs. | Publish a deterministic ordered GeoJSON view with inclusion policy, source IDs, total candidate count, and truncation metadata. |
| F22 | High | The public supplemental files mirror raw provider fields without field-level classification. | Published fields include precise coordinates, demographic attributes, `citizen_id`, and `unique_officer_id`. | Maintain immutable internal source observations, then publish reviewed normalized views through explicit allowlists. |
| F23 | Medium | One site build combines artifacts observed or generated at different times without a common release identifier. | Current roster, open-data feeds, search, and map have different `generated_utc` values. Some retained feeds are months old. | Add a release ID and preserve separate acquisition, source-observed, normalization, and publication times. |
| F24 | Medium | RSS release items link to custody pages that are removed when the subject leaves the active roster. | The feed template always links to `/inmate/<inmate_number>/`, while released people are removed from the generated roster pages. | Link activity items to stable event pages or a non-identifying activity route with defined retention. |
| F25 | Medium | Derived classifications appear in search output without ruleset provenance or uncertainty. | Search emits a single primary category and tier from mutable classification helpers. | Reference versioned offense assessments and expose unresolved status rather than silently choosing a category. |

## Required V2 boundaries

1. Source observations and public normalized records remain separate.
2. Every public artifact declares a schema URI, schema version, release ID, generation time, source status, provenance, record count, and integrity hash through the release manifest.
3. Every identity-bearing record has an explicit retention and deletion rule.
4. No build step mutates legal authority data or source observations.
5. Derived values reference the ruleset and taxonomy versions that produced them.
6. A capped or partial result cannot present itself as complete.
7. Public documentation is generated from the same registry that controls acquisition and publication.

## Conclusion

V1 exposes useful data, but it does not provide a stable public API contract. HCJC2 should preserve the underlying observations and useful views while replacing every public envelope and identifier rule.
