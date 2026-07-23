---
title: Operations and Security
reference_namespace: V2
status: approved
authority: v2-operations
owner_repository: AICincy/HCJC2
document_family: operations
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships:
- from: V2-102
  relation: refines
  to: A-23
---

# Operations and Security

> **Authority:** Approved controlled HCJC2 operations specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 operations and security requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-97 Least-Privilege Credentials

Acquisition, publication, deployment, review, and administrative actions use separate least-privilege identities.

## V2-98 Secret and Environment Management

Secrets remain in managed stores and never enter source, generated public artifacts, logs, previews, or evidence packages.

## V2-99 Run-Level Observability

Every run records trigger, versions, source outcomes, counts, freshness, decisions, hashes, promotion state, rollback target, alerts, and final status.

## V2-100 Operational Alerts

Alerts cover frozen or empty sources, count and schema anomalies, privacy failure, partial-state attempts, promotion conflicts, hash mismatch, stale releases, deletion failure, correlation regression, and rollback.

## V2-101 Versioned Run Manifests

Run manifests provide the authoritative operational chronology and bind source observations, candidate artifacts, decisions, and release outcomes.

## V2-102 Evidence Separation

Operational diagnostics, source captures, review notes, and legal evidence remain private and separate from public data.

## V2-103 Cache and CORS Control

The gateway applies explicit cache keys, release isolation, invalidation behavior, CORS allowlists, and fail-closed pointer handling.

## V2-104 Application Deployment Control

Application changes pass tests, synthetic previews, accessibility and security verification, controlled production promotion, and application rollback.

## V2-105 Incident Response and Rollback Authority

Runbooks identify incident ownership, escalation, rollback authority, evidence preservation, public status communication, and recovery verification.

## V2-106 Artifact Retention and Disposal

Each artifact class has an owner, purpose, storage location, retention period, deletion behavior, backup policy, public-access rule, and disposal evidence.

## V2-107 Release Ownership

Application and data releases have named approvers, promotion evidence, rollback targets, and post-release verification.

## V2-108 Provider Cost and Limit Review

Netlify, R2, Worker, logging, bandwidth, object-operation, cache, and retention costs and limits are verified before production approval.

## Related decisions, contracts, schemas, tests, and evidence

- [Cost Model](costs/DATA-PLANE-COST-MODEL.md)
- [Deployment Control](runbooks/DEPLOYMENT-CONTROL.md)
- [Data Promotion and Rollback](runbooks/DATA-PROMOTION-ROLLBACK.md)
- [Data Plane Boundaries](security/DATA-PLANE-BOUNDARIES.md)

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
