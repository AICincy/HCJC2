---
title: Pipeline State Machine
reference_namespace: V2
status: approved
authority: v2-pipeline-state-machine
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

# Pipeline State Machine Contract

## Purpose

This contract governs every HCJC2 acquisition and publication run. No stage may infer success from process exit alone. Every stage records status, inputs, outputs, checksums, timing, warnings, and failure reasons in one run manifest.

## Run states

| State | Meaning | Allowed next states |
|---|---|---|
| `created` | Run identifier and immutable configuration captured | `preflight_passed`, `failed` |
| `preflight_passed` | Lock, credentials, storage, clock, schemas, and prior canonical pointers validated | `acquiring`, `failed` |
| `acquiring` | Source adapters are retrieving candidate source snapshots | `acquired`, `degraded`, `failed` |
| `acquired` | Required candidate inputs exist | `validating`, `failed` |
| `degraded` | One or more non-required sources failed; last-known-good candidates remain available | `validating`, `held`, `failed` |
| `validating` | Schema, completeness, freshness, consistency, and privacy gates are running | `validated`, `held`, `failed` |
| `validated` | Candidate inputs satisfy all required gates | `transforming`, `failed` |
| `transforming` | Canonical records, correlations, and public projections are produced in staging | `transformed`, `failed` |
| `transformed` | Candidate artifacts and manifests are complete | `publishing_data`, `failed` |
| `publishing_data` | Versioned public-data objects are uploaded but not yet canonical | `data_verified`, `failed` |
| `data_verified` | Uploaded data is readable and hash-equivalent to the manifest | `promoting_data`, `failed` |
| `promoting_data` | The canonical data pointer is atomically changed | `data_published`, `failed` |
| `data_published` | Public data pointer references the verified version | `deploying_app`, `complete`, `failed` |
| `deploying_app` | A new application release is being created when application code changed | `app_verified`, `failed` |
| `app_verified` | Immutable deploy URL passes health, security, and integrity checks | `promoting_app`, `failed` |
| `promoting_app` | Production alias is moved to the verified deploy | `complete`, `rollback` |
| `held` | Candidate state was rejected; prior canonical state remains active | `complete` |
| `rollback` | Prior canonical pointer or application deploy is restored | `complete`, `failed` |
| `failed` | Run did not achieve a safe terminal state | `rollback`, `complete` |
| `complete` | Manifest is finalized and alerts are delivered or recorded | none |

## Mandatory promotion invariant

A candidate roster may become canonical only when all conditions hold:

1. The list phase completed.
2. Required detail acquisition completed or an approved carry-forward policy filled every required record.
3. Candidate record count and identifier set pass completeness gates.
4. Required fields pass quality thresholds.
5. Takedown and retention filters execute successfully.
6. Candidate schema validates.
7. Candidate checksum is recorded.
8. The run manifest reaches `validated`.
9. Canonical promotion is one atomic pointer or object-version operation.

An exception, cancellation, timeout, process termination, or alert failure must never promote the in-memory partial candidate.

## Source independence

Each source adapter returns one of:

- `fresh`
- `cached_valid`
- `source_paused`
- `source_frozen`
- `failed_optional`
- `failed_required`
- `invalid`

Optional-source failure may allow publication only when the public output explicitly carries the source status and freshness. Required-source failure must hold the canonical pointer.

## Run manifest requirements

The manifest must include:

- run ID
- trigger and actor
- source commit and configuration hash
- stage transitions with UTC timestamps
- source results
- candidate and canonical versions
- schema versions
- artifact checksums and sizes
- validation results
- publication decision
- deploy ID when applicable
- health-check results
- rollback action
- alert-delivery results
- unresolved warnings

## Idempotency

Re-running a stage with the same immutable inputs and configuration must produce the same semantic artifacts. Timestamps belong in manifests or metadata, not inside content whose hash is expected to be reproducible, unless the timestamp is an explicit contract field.

## Concurrency

- Only one canonical roster promotion may execute at a time.
- Source acquisition may run concurrently when adapters do not share mutable state.
- Evidence writers may append to separate immutable segments without serializing unrelated event types.
- A stale run may not overwrite a canonical version promoted by a newer run.
- Promotion uses compare-and-swap against the prior canonical version recorded at preflight.
