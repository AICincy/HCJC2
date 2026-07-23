---
title: HCJC2 Master Specification
reference_namespace: V2
status: approved
authority: v2-master
owner_repository: AICincy/HCJC2
document_family: master
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-3
  relation: refines
  to: A-42
---

# HCJC2 Master Specification

> **Authority:** Approved controlled HCJC2 master specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 hcjc2 master specification requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-1 Greenfield Successor

HCJC2 is implemented as a greenfield successor. Verified domain knowledge may be preserved, but V1 structure does not become the V2 architecture by default.

## V2-2 V1 Production Baseline

JCStream V1 remains the production, behavioral, fixture, and rollback reference during migration. V1 receives emergency, security, legal, and data-integrity fixes only.

## V2-3 Controlled Documentation Authority

The master specification controls scope, critical invariants, and document ownership. Detailed behavior is controlled by the ten linked modules and approved decisions.

## Related decisions, contracts, schemas, tests, and evidence

Related controlled extensions and verification records are linked as they are approved.

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
