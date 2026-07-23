---
title: Offense Taxonomy
reference_namespace: V2
status: approved
authority: v2-taxonomy
owner_repository: AICincy/HCJC2
document_family: taxonomy
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-55
  relation: constrained-by
  to: D-3
- from: V2-55
  relation: refines
  to: A-33
- from: V2-56
  relation: refines
  to: A-34
- from: V2-57
  relation: refines
  to: A-35
- from: V2-58
  relation: refines
  to: A-36
---

# Offense Taxonomy

> **Authority:** Approved controlled HCJC2 taxonomy specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 offense taxonomy requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-55 Separate Charge Observations

Raw source charge text, code, degree, jurisdiction, record ID, observation time, and parse status are preserved.

## V2-56 Reviewed Authority Records

Statutes, ordinances, rules, holds, and other authority types use separate reviewed records with official sources and effective dates.

## V2-57 Analytical Offense Concepts

Analytical concepts group related observations but do not replace legal authority or determine guilt.

## V2-58 Versioned Charge Assessments

Assessments connect observations to possible authorities, concepts, classifications, evidence, conflicts, and unresolved facts.

## V2-59 No Build-Time Authority Mutation

Public builds and live source observations never create or modify reviewed authority records.

## V2-60 Missing Degree Never Defaults to MM

A missing or ambiguous source degree remains unresolved and never defaults to `MM` or any other classification.

## V2-61 Unresolved Legal Facts Remain Unresolved

Insufficient facts, conditional statutory elements, uncertain jurisdiction, or ambiguous source codes produce an unresolved assessment.

## V2-62 Jurisdiction-Specific Interpretation

Authority matching considers jurisdiction, venue, source context, and effective date.

## V2-63 Authority Currency

Authority records identify current, amended, superseded, repealed, expired-review, or unresolved status.

## V2-64 Conditional Degree Logic

A base section with fact-dependent degrees cannot be reduced to one unconditional classification.

## V2-65 Correlation Integration

The correlation engine may use raw text, concept, authority, degree, and jurisdiction compatibility as separate evidence signals.

## V2-66 Public Assessment Provenance

Public offense labels identify the source observation, assessment status, authority source, ruleset, and unresolved limitations.

## Related decisions, contracts, schemas, tests, and evidence

- [Offense Taxonomy Contract](OFFENSE-TAXONOMY-CONTRACT.md)
- [D-3 Separate Offense Record Classes](../decisions/ADR-003-OFFENSE-TAXONOMY.md)

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
