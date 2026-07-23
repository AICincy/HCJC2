---
title: Migration and Traceability
reference_namespace: V2
status: approved
authority: v2-migration
owner_repository: AICincy/HCJC2
document_family: migration
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-121
  relation: refines
  to: V1-116
- from: V2-124
  relation: requires
  to: A-46
- from: V2-130
  relation: requires
  to: A-42
- from: V2-132
  relation: requires
  to: A-45
- from: V2-134
  relation: requires
  to: A-43
- from: V2-135
  relation: requires
  to: A-42
---

# Migration and Traceability

> **Authority:** Approved controlled HCJC2 migration specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 migration and traceability requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-121 Staged Migration Strategy

Migration proceeds through governance, domain contracts, frontend architecture, acquisition, taxonomy, correlation, data-plane proof, shadow operation, dual publication, cutover, and stabilization.

## V2-122 V1 Implementation Inventory

Every relevant V1 behavior, data artifact, public route, workflow, legal control, UI behavior, test, and evidence source receives a preservation, redesign, replacement, retirement, verification, or isolation disposition.

## V2-123 Parity Measurement

Shadow comparison measures roster, identity, episode, charge, bond, court, photo, activity, feed, correlation, taxonomy, schema, and failure behavior.

## V2-124 Accepted Differences

Intentional redesigns are reviewed and recorded as accepted differences rather than unexplained parity failures.

## V2-125 Shadow Operation

V1 and V2 run concurrently while V1 remains authoritative and every unexplained variance blocks advancement.

## V2-126 Dual Publication

V2 publishes under a non-production domain using production-like data flow while V1 remains authoritative.

## V2-127 Controlled Cutover

Cutover requires dated approval, complete acceptance evidence, named rollback authority, approved releases, successful public verification, and active monitoring.

## V2-128 Stabilization

The stabilization period uses elevated monitoring, defect response, correction and deletion verification, rollback proof, and continued parity review.

## V2-129 V1 Retirement

V1 retirement requires formal approval after stabilization and preservation of the implementation, documentation, evidence, and rollback history.

## V2-130 Cross-Version Traceability

Shared concepts, V1 behavior, V2 requirements, decisions, schemas, tests, evidence, and migration states use explicit typed relationships.

## V2-131 Pinned Canonical Interpretation

V1 records the exact canonical reference version, tag, commit, V1 commit, generation date, and tooling version used for interpretation.

## V2-132 Acceptance Evidence

Data, safety, UX, accessibility, privacy, security, deployment, rollback, and operational criteria require dated retained evidence.

## V2-133 Legacy Documentation Mapping

Every substantive legacy section receives a destination or explicit historical, supporting, generated, consolidated, or retired disposition.

## V2-134 Controlled Document Lifecycle

Proposed, draft, in-review, approved, deprecated, superseded, retired, and withdrawn states have explicit authority and replacement semantics.

## V2-135 Generated Registry and Matrix

Controlled Markdown is authoritative; deterministic human-readable and JSON indexes are generated and checked for staleness.

## V2-136 Production Cutover Requires Documented Evidence

Production cutover remains prohibited until every applicable acceptance criterion has attributable verification evidence.

## Related decisions, contracts, schemas, tests, and evidence

Related controlled extensions and verification records are linked as they are approved.

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
