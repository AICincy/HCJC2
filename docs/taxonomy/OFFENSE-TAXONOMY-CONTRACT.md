---
title: Offense Taxonomy Contract
reference_namespace: V2
status: approved
authority: v2-taxonomy-contract
owner_repository: AICincy/HCJC2
document_family: taxonomy
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Approved controlled extension for the HCJC2 taxonomy documentation family.

# Offense Taxonomy Contract

- Status: Proposed
- Capability: Required
- Implementation posture: Greenfield
- Applies to: charge display, search, analytics, correlation, provenance, review, and public explanations

## 1. Purpose

The taxonomy represents what a source reported, what legal authority exists, what concepts can be inferred, and what remains unknown. It must not convert absent subsection facts into a definite offense degree.

## 2. Core separation

HCJC2 uses four distinct record classes.

| Class | Purpose | Mutability |
|---|---|---|
| Source observation | Preserve raw agency code and description | Append-only by source snapshot |
| Authority record | Represent a verified statute or ordinance | Curated and versioned |
| Concept record | Represent analytical categories and crosswalks | Curated and versioned |
| Charge assessment | Apply available evidence to one reported charge | Regenerated and reviewable |

A source observation must never become an authority record automatically.

## 3. Source observation

Required fields:

```json
{
  "schema_version": "1.0.0",
  "observation_id": "obs_...",
  "source": {
    "agency": "HCSO",
    "dataset_id": "hcso_current",
    "snapshot_sha256": "sha256",
    "record_id": "source charge identifier or stable derived identifier",
    "retrieved_at": "RFC3339"
  },
  "reported": {
    "code_raw": "2913.02",
    "description_raw": "THEFT",
    "degree_raw": null,
    "case_numbers": [],
    "court_raw": null
  }
}
```

Raw values remain unchanged. Normalized values belong in assessments.

## 4. Authority registry

Each authority record must include:

- authority ID
- jurisdiction
- authority type
- official identifier
- official title
- official source URL
- effective start date
- effective end date when known
- verification date
- verification status
- verifying method
- source snapshot or content hash when legally and technically permitted
- offense classification possibilities
- applicability rules
- supersession or amendment links
- review history

### Authority types

- Ohio Revised Code
- Ohio Administrative Code
- Cincinnati Municipal Code
- other municipal ordinance
- court rule
- source-system placeholder
- source-system artifact
- unknown

Placeholders and artifacts are not legal authorities.

## 5. Identifier handling

1. Preserve `code_raw` exactly.
2. Apply a source-specific parser.
3. Produce zero or more identifier candidates.
4. Validate each candidate against the correct authority registry.
5. Record rejected parsing paths and reasons.
6. Never infer jurisdiction from digit length alone.
7. Never deep-link an unverified identifier.

## 6. Degree model

The authority record must not use one unconditional `degree` field unless the section truly has one possible classification.

Use:

```json
{
  "classification_rules": [
    {
      "rule_id": "orc-2913.47-c-base",
      "conditions": [{"fact": "claim_amount", "operator": "lt", "value": 1000}],
      "result": {"class": "misdemeanor", "degree": "M1"},
      "authority_locator": "division (C)"
    }
  ],
  "unresolved_result": {
    "class": "unknown",
    "degree": null,
    "reason": "required statutory facts unavailable"
  }
}
```

### Rules

- Missing facts remain missing.
- A default may be recorded only when the statute expressly supplies a default.
- A default does not override conflicting source or venue evidence.
- Derived degree must identify the exact rule and inputs used.
- Venue is evidence about case handling, not proof of statutory degree.
- A source description suffix is evidence, not legal verification.

## 7. Concept taxonomy

Legal authority and analytical concepts remain separate.

A charge may map to multiple concepts, for example:

- violence
- property
- fraud
- drug possession
- drug trafficking
- weapon
- obstruction
- family or domestic
- traffic safety
- public order

Concept mappings include:

- mapping version
- supporting authority or source text
- mapping strength
- inclusion and exclusion terms
- parent and child concepts
- external crosswalks when approved

NIBRS may serve as an optional analytical crosswalk. It must not replace the local legal authority or imply that a booking charge is a NIBRS-coded incident.

## 8. Charge assessment

Each charge assessment combines evidence without first-match-wins logic.

```json
{
  "assessment_id": "charge_assess_...",
  "observation_id": "obs_...",
  "taxonomy_version": "offense-taxonomy-1.0.0",
  "authority_candidates": [],
  "selected_authority_id": null,
  "classification": {
    "class": "unknown",
    "degree": null,
    "rule_id": null
  },
  "concepts": [],
  "evidence": {
    "supporting": [],
    "conflicting": [],
    "missing": [],
    "disqualifying": []
  },
  "review_status": "machine_generated"
}
```

## 9. Review states

- machine_generated
- needs_authority_review
- needs_source_review
- reviewed_supported
- reviewed_corrected
- reviewed_rejected
- superseded
- expired

Every transition records actor type, timestamp, reason, and prior state.

## 10. Correlation interface

The correlation engine consumes concept and authority assessments, not raw text alone.

Permitted features include:

- verified authority compatibility
- concept overlap
- source-description token overlap
- incompatible concept evidence
- degree compatibility when resolved
- source and taxonomy freshness

An unresolved offense assessment may still support correlation through lower-weight concepts and text evidence. It must not be silently treated as a confirmed legal classification.

## 11. Versioning

Every published assessment records:

- source snapshot hash
- parser version
- authority-registry version
- concept-taxonomy version
- classification-rules version
- assessment engine version

A taxonomy update must not rewrite historical evidence. It creates a new assessment.

## 12. Failure behavior

| Failure | Required behavior |
|---|---|
| Authority registry unavailable | Preserve raw observation and publish unknown classification |
| Source code unparseable | Preserve raw code and record parse failure |
| Required statutory fact missing | Return unresolved classification |
| Conflicting source and authority evidence | Mark conflict and require review for prominent display |
| Taxonomy validation failure | Block new taxonomy publication |
| Current build sees unknown code | Add to curation queue only |
| Authority becomes amended | Create new version and reassess affected charges |

## 13. Release gates

- Build does not mutate authority or concept registries.
- Every authority record has jurisdiction and provenance.
- Every code-list release has a version and checksum.
- Every degree result is supported by a rule or is explicitly unresolved.
- Malformed and placeholder codes cannot produce official deep links.
- Contract tests cover known variable-degree statutes.
- Current-roster unknown and conflict rates are reported.
- Correlation tests pin the taxonomy version used.
