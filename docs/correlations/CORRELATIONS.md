---
title: Correlations
reference_namespace: V2
status: approved
authority: v2-correlations
owner_repository: AICincy/HCJC2
document_family: correlations
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-39
  relation: constrained-by
  to: D-2
- from: V2-39
  relation: refines
  to: A-25
- from: V2-41
  relation: refines
  to: A-26
- from: V2-43
  relation: requires
  to: A-27
- from: V2-44
  relation: requires
  to: A-28
- from: V2-45
  relation: requires
  to: A-29
- from: V2-46
  relation: requires
  to: A-30
- from: V2-47
  relation: refines
  to: A-31
- from: V2-49
  relation: requires
  to: A-32
- from: V2-53
  relation: requires
  to: A-39
---

# Correlations

> **Authority:** Approved controlled HCJC2 correlations specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 correlations requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-39 Correlations Are Required and Enhanced

Correlations remain a first-class public capability and must materially improve accuracy, explanation, governance, extensibility, correction, and evaluation.

## V2-40 One Canonical Engine

One canonical engine replaces parallel incompatible matchers. See [D-2 Canonical Correlation Engine](../decisions/ADR-002-CORRELATION-ENGINE.md#d-2-canonical-correlation-engine).

## V2-41 Typed Relationship Families

Each relationship family defines endpoints, candidate rules, evidence, disqualifiers, cardinality, retention, explanation, and publication thresholds.

## V2-42 Broad Candidate Generation

Candidate generation maximizes appropriate recall before disqualifying rules, evidence scoring, competition, and abstention.

## V2-43 Supporting Evidence

Every assessment records signals that increase support, their values, provenance, and rule interpretations.

## V2-44 Conflicting Evidence

Material contradictory signals remain explicit rather than disappearing into an aggregate score.

## V2-45 Missing Evidence

Unavailable or unresolved expected signals are distinguished from negative evidence.

## V2-46 Disqualifying Evidence

Impossible timing, incompatible jurisdiction, authoritative identifier conflict, and other family-specific exclusions make candidates ineligible.

## V2-47 Deterministic Evidence Scoring

The initial engine uses deterministic, explainable scoring and documented thresholds.

## V2-48 Scores Are Not Probabilities Without Calibration

Evidence scores must not be described as probability, certainty percentage, likelihood percentage, or statistical confidence until held-out calibration supports that interpretation.

## V2-49 Qualitative Confidence Bands

Strong, probable, possible, conflicted, unresolved, and rejected bands communicate evidence and uncertainty.

## V2-50 Relationship Cardinality

Each family defines allowed one-to-one, one-to-many, many-to-one, or grouped-event behavior.

## V2-51 Candidate Competition

Stronger alternatives, event reuse, duplicate source rows, temporal clusters, and person-to-event competition affect assessments.

## V2-52 Group Incident Modeling

Group arrests and shared incidents are represented explicitly rather than treated as unrestricted event reuse.

## V2-53 Review, Dispute, and Correction Lifecycle

Machine-generated, pending-review, reviewed, confirmed, rejected, disputed, corrected, withdrawn, and expired states are auditable.

## V2-54 Versioning and Evaluation

Public records identify engine, ruleset, taxonomy, and generation versions. Evaluation reports precision, recall, false-positive rate, abstention, reviewer disagreement, and calibration by relevant strata.

## Related decisions, contracts, schemas, tests, and evidence

- [Correlation System Contract](CORRELATION-SYSTEM.md)
- [Labeled Correlation Fixtures](LABELED-CORRELATION-FIXTURES.md)
- [D-2 Canonical Correlation Engine](../decisions/ADR-002-CORRELATION-ENGINE.md)

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
