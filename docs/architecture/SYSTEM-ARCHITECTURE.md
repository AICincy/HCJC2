---
title: System Architecture
reference_namespace: V2
status: approved
authority: v2-architecture
owner_repository: AICincy/HCJC2
document_family: architecture
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

# System Architecture

> **Authority:** Approved controlled HCJC2 architecture specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 system architecture requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-4 Contract-First Architecture

Source, transformation, publication, and public-presentation behavior require explicit contracts before implementation.

## V2-5 Deterministic Domain Core

Normalization, identifier construction, taxonomy assessment, and correlation evidence logic remain deterministic and isolated from network, filesystem, clock, deployment, and alerting adapters.

## V2-6 Explicit State Transitions

Critical acquisition and publication stages expose typed states, decisions, evidence, and allowable transitions.

## V2-7 Application and Data Plane Separation

Application deployment and custody-data publication are independent release surfaces with independent rollback.

## V2-8 Netlify Application Plane

Netlify hosts the static application shell, documentation, redirects, headers, previews, and immutable application deployments. Custody refreshes do not trigger application deployments.

## V2-9 Private R2 and Worker Data Plane

Private Cloudflare R2 storage behind a Worker gateway is the planned public data plane, subject to proof of access control, cache behavior, rollback, deletion, and provider limits.

## V2-10 Repository Boundary

The source repository does not operate as a runtime database, active-photo store, evidence store, secret store, or generated deployment archive.

## Related decisions, contracts, schemas, tests, and evidence

Related controlled extensions and verification records are linked as they are approved.

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
