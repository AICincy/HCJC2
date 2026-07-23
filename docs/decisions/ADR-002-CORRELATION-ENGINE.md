---
title: Canonical Correlation Engine
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

# D-2 Canonical Correlation Engine

- Status: Accepted
- Accepted: 2026-07-21
- Date: 2026-07-20

## Context

V1 contains two independent booking-to-dispatch matchers. The public matcher selects up to four temporally adjacent arrest-like calls. The private matcher applies a separate time and text scoring formula. Their outputs overlap minimally and use different publication policies.

HCJC2 requires correlations as a first-class capability and must improve their accuracy, explainability, extensibility, and governance.

## Decision

HCJC2 will implement one canonical correlation engine with:

- typed relationship definitions
- normalized source-event contracts
- stable source identifiers
- explicit time uncertainty and source timezone
- versioned feature extraction
- positive, negative, missing, and conflicting evidence
- relationship-specific cardinality
- competition analysis
- deterministic evidence scoring first
- calibrated probabilities only after validation
- complete provenance
- review and correction states
- one versioned artifact consumed by the public build

The public frontend will never calculate correlations.

## Rejected options

### Copy `scraper/match.py`

Rejected because it ranks only by distance from a midnight booking-date anchor and saturates the four-result cap.

### Copy `scraper/correlate.py`

Rejected because it uses arbitrary confidence weights, unstable row indexes, one charge, weak text overlap, and no cardinality model.

### Keep public and researcher engines separate

Rejected because two definitions create contradictory results, testing, documentation, and public claims.

### Start with an opaque machine-learning model

Rejected because no labeled dataset currently supports training, calibration, or error analysis.

## Consequences

- Initial implementation will be slower to design but safer to evolve.
- V2 needs a labeling and review workflow before probability claims.
- Correlation publication can degrade independently from roster publication.
- Additional relationship families can reuse the platform while retaining separate policies.
- Engine versions and source snapshots will increase artifact size, but make results reproducible and auditable.

## Follow-up decisions

- source-event schema
- offense taxonomy
- labeling protocol
- reviewer workflow
- public correction process
- relationship-specific publication thresholds
- optional learned scorer
