---
title: Feed Registry
reference_namespace: V2
status: approved
authority: v2-feed-registry
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

# Feed Registry Contract

The feed registry is the authoritative configuration and documentation source for every acquired or derived dataset.

## Required registry fields

| Group | Fields |
|---|---|
| Identity | `feed_id`, `label`, `owner`, `jurisdiction`, `source_type` |
| Source | canonical URL, dataset identifier, terms, access method |
| Acquisition | cadence, timeout, retry policy, query, order, limit, cache policy |
| Time | source timezone, source time fields, query window, freshness objective |
| Shape | source schema reference, normalized schema reference, primary key candidates |
| Publication | public artifact name, publication mode, retention, indexing policy |
| Classification | public, internal, sensitive, evidentiary, generated |
| Quality | completeness rules, row-drop thresholds, duplication checks, null thresholds |
| Status | current state, last success, last source observation, known pause or freeze |
| Ownership | operational owner, review owner, escalation route |

## Publication modes

| Mode | Meaning |
|---|---|
| `normalized_public` | HCJC2 publishes an allowlisted normalized view |
| `raw_public_reviewed` | HCJC2 publishes reviewed source rows with documented field classification |
| `internal_only` | Never enters the public release |
| `derived_public` | Generated from versioned public or approved internal inputs |
| `retired` | Retained only for historical documentation |

## Generated documentation

The public data catalog must render from the registry. Tests compare documented cadence, window, status, dataset ID, and limits to the runtime feed specification.

## Feed health rules

A feed at its configured limit must report `truncated`, `complete`, or `unknown`. It cannot report completeness implicitly.

A failed acquisition retains the prior validated artifact and changes `source_status.state` to `cached_after_fetch_failure`.

A paused or frozen source retains its last observed source time and does not imply current events.
