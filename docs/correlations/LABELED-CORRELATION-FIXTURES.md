---
title: Labeled Correlation Fixtures
reference_namespace: V2
status: approved
authority: v2-correlation-fixtures
owner_repository: AICincy/HCJC2
document_family: correlations
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Approved controlled extension for the HCJC2 correlations documentation family.

# Labeled Correlation Fixture Protocol

- Status: Proposed
- Applies to: booking-to-dispatch and future HCJC2 relationship types
- Dependency: Correlation System Contract and Offense Taxonomy Contract

## 1. Purpose

The fixture system provides reproducible evidence for correlation accuracy without turning model output into its own ground truth. Fixtures must preserve ambiguity, source limitations, group events, and negative evidence.

## 2. Label unit

The primary label unit is a proposed relationship between stable source records under a named relationship type.

Each fixture contains:

- source snapshots or minimal normalized extracts
- stable source identifiers
- taxonomy and ruleset versions
- candidate relationship
- label
- label basis
- evidence inventory
- reviewer metadata separated from public output

## 3. Allowed labels

| Label | Meaning |
|---|---|
| link | Evidence establishes the records refer to the approved relationship |
| non_link | Evidence establishes they do not |
| possible_link | Evidence is insufficient to resolve |
| conflicted | Material evidence supports and contradicts the relationship |
| group_link | Relationship exists through an identified multi-record group event |
| invalid_fixture | Source or labeling defect prevents use |

`possible_link` and `conflicted` are valid outcomes. Reviewers must not force a binary label.

## 4. Label authority levels

| Level | Basis | Permitted use |
|---|---|---|
| A | Shared official incident, arrest, booking, or case identifier | Gold evaluation and release gates |
| B | Independent official records plus specific compatible facts | Gold after two-reviewer agreement |
| C | Strong circumstantial public-record evidence | Ranking research, not sole high-confidence calibration |
| D | Reviewer judgment from ambiguous text and time alone | Error analysis only |
| E | Existing V1 matcher output | Candidate generation only, never ground truth |

## 5. Required evidence fields

- source record identifiers
- source agencies and datasets
- source retrieval timestamps
- event and booking time intervals with timezone and precision
- raw and normalized offense observations
- authority and concept assessments
- disposition
- location precision when permitted
- shared case or incident identifiers
- competing candidates
- group-event evidence
- missing fields
- conflicting fields
- source freshness

## 6. Reviewer workflow

1. Generate candidate without exposing engine score to the initial reviewer.
2. Reviewer A assigns label, authority level, evidence, and rationale.
3. Reviewer B independently reviews Level B, C, conflicted, and group cases.
4. Resolve disagreements through adjudication.
5. Record each prior label and reason. Do not overwrite history.
6. Lock the fixture before it enters a held-out set.

Reviewer identity remains private. Public artifacts expose only approved rationale and review status.

## 7. Dataset partitions

- development set
- validation set
- held-out test set
- temporal holdout from later source periods
- regression set for previously observed defects
- challenge set for rare or adversarial conditions

No source record, booking group, dispatch group, or near-duplicate may span partitions.

## 8. Required strata

The fixture inventory must cover:

- exact shared identifiers
- same-day unrelated events
- date-only booking times
- midnight boundaries
- daylight-saving transitions
- delayed booking after incident
- group arrests
- one dispatch competing with many bookings
- one booking with multiple plausible dispatches
- multiple charges
- variable-degree statutes
- missing or malformed charge codes
- incompatible offense concepts
- canceled, unfounded, report-only, citation, and arrest dispositions
- stale or partially missing source feeds
- duplicate and reordered source records
- source corrections
- removed custody subjects
- prior V1 false positives and false negatives

## 9. Fixture format

```json
{
  "fixture_version": "1.0.0",
  "fixture_id": "fx_...",
  "relationship_type": "booking_to_dispatch",
  "partition": "held_out_test",
  "subjects": [],
  "taxonomy_version": "offense-taxonomy-1.0.0",
  "label": {
    "value": "possible_link",
    "authority_level": "C",
    "rationale_codes": [],
    "evidence_refs": [],
    "adjudication_status": "agreed"
  },
  "conditions": [],
  "privacy": {
    "contains_real_personal_data": false,
    "handling_class": "synthetic"
  }
}
```

## 10. Personal-data rules

Prefer synthetic or structurally transformed fixtures. Real public records may be used only when necessary to preserve a failure mode that cannot be represented otherwise.

Real-record fixtures require:

- purpose statement
- minimum necessary fields
- restricted access classification
- retention rule
- prohibition on public test logs and screenshots
- removal and sealing synchronization
- replacement with synthetic fixture when feasible

## 11. Metrics

Report by relationship type and important stratum:

- precision
- recall
- false discovery rate
- unresolved rate
- conflicted rate
- group-link accuracy
- event reuse distribution
- reviewer agreement
- override rate
- calibration error when probabilities exist
- performance by taxonomy certainty
- performance by time precision
- performance under source staleness

Do not publish one aggregate score without stratum results.

## 12. Release requirements

- No test-set labels are created from engine output alone.
- Held-out fixtures remain inaccessible to tuning code and prompts.
- Every fixture pins source, taxonomy, and ruleset versions.
- Reviewers can reproduce the evidence from stored fixture inputs.
- Strong and Probable public bands meet their approved precision gates.
- Group-link behavior has separate tests.
- Event saturation and uncontrolled many-to-many reuse fail the release gate.
- Prior V1 saturation behavior is included as a regression fixture.
