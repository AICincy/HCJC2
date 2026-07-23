---
title: Acquisition and Publication
reference_namespace: V2
status: approved
authority: v2-pipeline
owner_repository: AICincy/HCJC2
document_family: pipeline
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-25
  relation: constrained-by
  to: D-4
- from: V2-26
  relation: requires
  to: A-2
- from: V2-29
  relation: requires
  to: A-16
- from: V2-30
  relation: constrained-by
  to: D-5
- from: V2-30
  relation: requires
  to: A-14
- from: V2-34
  relation: refines
  to: A-18
---

# Acquisition and Publication

> **Authority:** Approved controlled HCJC2 pipeline specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 acquisition and publication requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-25 Explicit Pipeline State Machine

Runs advance through scheduled, locked, acquiring, validating, normalizing, assessing, building, verifying, staging, promotion, post-verification, and completion states.

## V2-26 Run-Scoped Acquisition

Source adapters write only immutable run-scoped observations and never mutate the approved public release.

## V2-27 Validation Gates

Source schema, count, freshness, completeness, parsing quality, privacy, integrity, and reproducibility checks gate advancement.

## V2-28 Partial Acquisition Never Advances

A failed, interrupted, anomalously small, or incomplete acquisition may be retained as diagnostic candidate state but never replaces the approved roster.

## V2-29 Last-Known-Good Preservation

Failure preserves the most recent approved release and may update only an explicitly permitted source-status surface.

## V2-30 Immutable Candidate Releases

Generated candidate releases are immutable once verification begins and remain private until promotion.

## V2-31 Conditional Pointer Promotion

Publication changes one approved-release pointer through a conditional write rather than mutating all public objects.

## V2-32 Independent Data Rollback

Data rollback selects a previously verified release without rebuilding or redeploying the application.

## V2-33 Separate Release Cadences

Application changes deploy through Netlify. Custody-data refreshes publish through the data plane without a Netlify production deployment.

## V2-34 Source Degradation Policy

Delayed, paused, frozen, cached-after-failure, degraded, unavailable, derived, and retired source states have explicit publication behavior.

## V2-35 Active Photo Lifecycle

When current-roster eligibility ends, the public manifest and origin object are removed, the exact route is purged, and deletion evidence is retained privately.

## V2-36 Worker Route Allowlist

The public gateway exposes only stable approved logical routes and denies direct immutable release-prefix access.

## V2-37 Manifest and Hash Verification

Candidate and public artifacts are verified against a release manifest before and after promotion.

## V2-38 Post-Promotion Verification

Stable public routes, hashes, headers, cache isolation, CORS, and release metadata are checked after promotion; failure triggers rollback.

## Related decisions, contracts, schemas, tests, and evidence

- [Pipeline State Machine](PIPELINE-STATE-MACHINE.md)
- [Public Data Plane](PUBLIC-DATA-PLANE.md)
- [D-4 Separate Application and Data Publication](../decisions/ADR-004-NETLIFY-AND-DATA-PUBLICATION.md)
- [D-5 Private R2 Origin with Worker Gateway](../decisions/ADR-005-R2-WORKER-DATA-PLANE.md)

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
