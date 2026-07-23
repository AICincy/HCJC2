---
title: Testing and Quality
reference_namespace: V2
status: approved
authority: v2-quality
owner_repository: AICincy/HCJC2
document_family: quality
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-111
  relation: requires
  to: A-44
- from: V2-119
  relation: verifies
  to: A-16
---

# Testing and Quality

> **Authority:** Approved controlled HCJC2 quality specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 testing and quality requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-109 Formatting Gate

Controlled source and generated files pass deterministic formatting checks.

## V2-110 Linting and Static Typing

Production and test code pass pinned linting and static type-checking policies.

## V2-111 Unit Verification

Deterministic domain functions use focused unit tests with explicit assertions and controlled clocks, randomness, and inputs.

## V2-112 Contract Verification

Upstream source contracts, public schemas, compatibility behavior, and feed-registry documentation are tested.

## V2-113 Integration Verification

Stage boundaries, persistence, retries, locks, pointer conflicts, partial writes, and provider adapters are integration tested.

## V2-114 End-to-End and No-JavaScript Verification

Critical public routes, search, corrections, status, legal content, and no-JavaScript access are end-to-end verified.

## V2-115 Accessibility and Visual Regression

Automated and manual WCAG review, keyboard and screen-reader checks, responsive behavior, and approved visual baselines gate release.

## V2-116 Security and Privacy Verification

Dependencies, secrets, headers, route allowlists, public-field allowlists, preview exposure, retention, and deletion behavior are tested.

## V2-117 Data Quality Verification

Freshness, completeness, duplicates, null semantics, truncation, source status, schema conformance, and anomaly thresholds are verified.

## V2-118 Reproducible Artifacts

Identical approved inputs and versions produce byte-equivalent public artifacts and deterministic registries.

## V2-119 Resilience and Rollback Verification

Failure injection proves last-known-good preservation, fail-closed publication, promotion conflict handling, and application and data rollback.

## V2-120 Time-Limited Exceptions

Every exception records owner, rationale, affected rule, risk, compensating control, approval, expiration, and removal plan.

## Related decisions, contracts, schemas, tests, and evidence

Related controlled extensions and verification records are linked as they are approved.

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
