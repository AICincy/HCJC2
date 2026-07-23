---
title: Correlation System Contract
reference_namespace: V2
status: approved
authority: v2-correlations-contract
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

# Correlation System Contract

- Status: Proposed
- Capability: Required
- Implementation posture: Greenfield
- Initial relationship: booking to dispatch
- Future relationships: court case, incident, use of force, complaint, judge, and statute relationships

## 1. Purpose

The correlation system identifies and explains possible relationships among records from independent public sources. It does not convert inference into fact. It preserves uncertainty, source provenance, conflicting evidence, and correction history.

## 2. Governing rules

1. One canonical engine produces every correlation artifact.
2. Public pages consume correlation artifacts. They do not calculate relationships.
3. Every relationship type has its own source rules, features, cardinality, thresholds, and limitations.
4. Candidate generation favors recall. Publication rules control precision and presentation.
5. Uncalibrated scores are called `evidence_score`, not confidence or probability.
6. A `match_probability` field is prohibited until a held-out evaluation demonstrates calibration.
7. Every assessment records supporting, conflicting, missing, and disqualifying evidence.
8. Every public relationship provides a correction or dispute route.
9. Relationships follow the lifecycle of the underlying public custody record unless a separate approved retention rule applies.
10. A failed correlation stage must not block publication of the verified custody roster. The site must expose correlation freshness and failure status.

## 3. Pipeline

```text
Normalize source records
        |
Create stable source-event identifiers
        |
Generate broad candidates with source-specific blocking
        |
Extract positive, negative, missing, and conflict features
        |
Score candidates with a versioned ruleset or calibrated model
        |
Apply relationship cardinality and competition analysis
        |
Assign evidence band and review status
        |
Write versioned correlation artifact with provenance
        |
Validate public-policy and lifecycle rules
        |
Render public explanations
```

## 4. Canonical source-event contract

Each normalized source event must contain:

```json
{
  "schema_version": "1.0.0",
  "source": {
    "agency": "CPD",
    "dataset_id": "source-dataset-id",
    "record_id": "stable-agency-record-id",
    "snapshot_sha256": "sha256",
    "retrieved_at": "RFC3339 timestamp"
  },
  "event": {
    "type": "dispatch",
    "occurred_interval": {
      "start": "RFC3339 timestamp",
      "end": "RFC3339 timestamp",
      "timezone": "America/New_York",
      "precision": "second"
    },
    "agency": "CPD",
    "disposition": "ARR: ARREST",
    "offense_terms": [],
    "statute_codes": [],
    "location": {
      "precision": "block",
      "public_value": "2XX EXAMPLE ST",
      "latitude": null,
      "longitude": null
    }
  }
}
```

A date-only value must be represented as a full-day interval, not midnight.

## 5. Relationship identity

V2 uses two identifiers:

- `relationship_id`: stable hash of relationship type and stable source record identifiers
- `assessment_id`: stable hash of relationship ID, engine version, ruleset version, taxonomy version, and source snapshot hashes

This permits the relationship to persist while assessments evolve.

## 6. Booking-to-dispatch candidate generation

Candidate generation may use:

- booking date interval in `America/New_York`
- first-observed timestamp as an upper-bound signal
- source event time interval
- agency and disposition eligibility
- source freshness
- exact source identifiers

Candidate generation must not use a hard result cap before scoring. It may use indexed blocking to control computation, but the blocking policy and excluded population must be recorded.

## 7. Evidence features

### Supporting evidence

- compatible temporal intervals
- arrest or citation disposition
- offense taxonomy compatibility
- ORC-to-incident mapping compatibility
- compatible agency
- common case or incident identifier
- related group-arrest pattern
- source records that independently support the same relationship

### Conflicting evidence

- impossible event ordering
- incompatible agency
- incompatible charge and incident taxonomy
- event linked strongly to a competing booking
- source record outside the validated temporal envelope
- source record marked canceled, unfounded, or non-arrest when applicable
- event reuse beyond an approved group-arrest model

### Missing evidence

Missing data must be recorded separately. Missing evidence is not automatically negative evidence.

## 8. Cardinality

Each relationship type declares a cardinality policy.

For booking to dispatch:

- one dispatch may relate to multiple bookings when group-arrest evidence exists
- one booking may relate to multiple dispatch events
- unconstrained many-to-many assignment is prohibited
- event reuse triggers a competition penalty and review flag
- group relationships must be represented as a group object, not duplicated unexplained pairs

## 9. Scoring stages

### Stage A: deterministic evidence model

The first production implementation uses versioned, reviewable rules. It outputs an `evidence_score` and evidence components. The score is ordinal only.

### Stage B: calibration

After a sufficient labeled dataset exists, V2 may calibrate scores against observed match frequency. Calibration must use held-out data and reliability diagrams. The evaluation must be segmented by relationship type and important source conditions.

### Stage C: learned ranking, optional

A learned model requires a separate decision record, model documentation, drift monitoring, fairness analysis, and rollback to the deterministic model.

## 10. Evidence bands

| Band | Meaning | Public treatment |
|---|---|---|
| Strong | Evidence meets the validated high-precision threshold | May be prominently ranked with limitations |
| Probable | Evidence supports the relationship but material uncertainty remains | May be shown with uncertainty statement |
| Possible | Candidate has limited supporting evidence | Shown only as a candidate, not likely match |
| Conflicted | Material supporting and contradicting evidence coexist | Show conflict explanation or withhold |
| Rejected | Disqualifying evidence or reviewer rejection | Not shown as a positive relationship |
| Unassessed | Candidate generated but not scored or evaluation unavailable | Withhold from normal public display |

Until calibration is validated, these bands derive from rules and must not be described as probabilities.

## 11. Assessment artifact

```json
{
  "schema_version": "1.0.0",
  "relationship_id": "rel_...",
  "assessment_id": "assess_...",
  "relationship_type": "booking_to_dispatch",
  "subject_refs": [
    {"dataset_id": "hcso_current", "record_id": "booking-id"},
    {"dataset_id": "cincinnati_cfs", "record_id": "event-number"}
  ],
  "engine": {
    "version": "2.0.0",
    "commit": "git-sha",
    "ruleset_version": "booking-dispatch-1.0.0",
    "taxonomy_version": "offense-taxonomy-1.0.0"
  },
  "assessment": {
    "evidence_score": 74,
    "match_probability": null,
    "evidence_band": "probable",
    "supporting": [],
    "conflicting": [],
    "missing": [],
    "disqualifying": [],
    "competition": {
      "competing_booking_count": 2,
      "competing_event_count": 0,
      "group_relationship_id": null
    }
  },
  "review": {
    "status": "machine_generated",
    "history": []
  },
  "provenance": {
    "generated_at": "RFC3339 timestamp",
    "source_snapshot_sha256": [],
    "feature_record_sha256": "sha256"
  },
  "lifecycle": {
    "public": true,
    "expires_when_subject_leaves_roster": true,
    "correction_status": "none"
  }
}
```

## 12. Review states

- `machine_generated`
- `needs_review`
- `reviewed_supported`
- `reviewed_rejected`
- `disputed`
- `corrected`
- `withdrawn`
- `expired`

Every transition records timestamp, actor type, reason code, and prior state.

## 13. Public presentation

Every displayed relationship must show:

- relationship type
- evidence band
- plain-language rationale
- supporting and conflicting signals
- source agency and event identifier
- source timestamp and data freshness
- engine and ruleset version through a details view
- a statement that the relationship is inferred
- a correction or dispute route

The interface must not display an unexplained decimal score as certainty.

## 14. Evaluation and release gates

### Required labeled sets

- confirmed positive pairs
- confirmed negative pairs
- unresolved pairs
- group-arrest cases
- date-only booking cases
- midnight and daylight-saving cases
- stale-feed cases
- duplicate and reordered source rows
- multi-charge cases
- incompatible offense cases
- high-competition events
- prior false-positive regressions

### Required metrics

- precision by evidence band
- recall on reviewable positives
- false discovery rate
- unresolved rate
- event reuse distribution
- reviewer override rate
- calibration error when probability is enabled
- performance by source condition and relationship type
- drift in feature and score distributions

### Provisional publication targets

- Strong band: lower bound of the 95 percent precision interval at or above 0.95
- Probable band: lower bound of the 95 percent precision interval at or above 0.85
- Possible band: no probability claim
- Insufficient sample size: no calibrated label

These targets are provisional until the evaluation protocol is approved.

## 15. Failure behavior

| Failure | Required behavior |
|---|---|
| Source unavailable | Preserve last-known-good assessment with stale status and age |
| Engine failure | Publish roster without new correlations and expose correlation failure status |
| Taxonomy failure | Stop correlation publication for affected relationship type |
| Provenance mismatch | Reject artifact |
| Public-policy validation failure | Reject deploy |
| Excess event reuse | Flag drift and demote affected assessments |
| Calibration drift | Remove probability language and fall back to evidence bands |
| Correction accepted | Withdraw or amend relationship on next publication cycle |

## 16. Observability

Each run records:

- candidate count before and after blocking
- scored, published, rejected, conflicted, and unresolved counts
- score and band distributions
- source freshness and null rates
- event reuse distribution
- top rejection and conflict reasons
- reviewer overrides
- runtime and memory
- artifact checksum

## 17. Security and privacy

- Correlation artifacts must pass the public-path allowlist.
- Sealed, removed, or takedown custody records must be excluded before candidate generation.
- Internal reviewer identity and notes remain outside the public artifact unless explicitly approved.
- Public location precision must follow the source and approved publication policy.
- Preview deployments must apply the same data lifecycle and access rules as production.
