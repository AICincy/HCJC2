---
title: Netlify Application Hosting
reference_namespace: D
status: deprecated
authority: architecture-decision
owner_repository: AICincy/HCJC2
document_family: decisions
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Architecture decision governing the subject stated below.

# D-1 Netlify Application Hosting

- Status: Superseded in part by ADR-004 and ADR-005
- Date: 2026-07-20
- Superseded: 2026-07-21

## Context

V1 publishes a static site through GitHub Pages after GitHub Actions acquires data, validates it, builds `docs/`, and commits generated output. HCJC2 requires atomic deployment, preview verification, rollback, security headers, custom-domain support, and repository-owned configuration.

## Decision

This initial decision required a complete Netlify evaluation. ADR-004 accepted Netlify for the application plane and separated frequent data publication. ADR-005 accepted a private R2 origin with a Worker gateway for the data plane. The original provisional target was:

- GitHub Actions controls acquisition, validation, transformation, and authoritative static build.
- Netlify hosts immutable static artifacts.
- Repository configuration controls build context, publish directory, redirects, headers, cache policy, and environment contracts.
- Production promotion follows health and integrity checks.
- Deploy previews must not expose prohibited personal or internal data.
- Netlify Functions and Scheduled Functions remain out of scope unless a later decision proves they improve reliability without weakening auditability or privacy.

## Required validation before acceptance

- current Netlify limits and pricing
- deploy API and rollback behavior
- immutable deploy and production-alias workflow
- cache invalidation and response headers
- preview access controls
- custom domain and TLS behavior
- secret scope and rotation
- log and notification retention
- large artifact and deploy-frequency limits
- integration with GitHub Actions and post-deploy health checks

## Consequences

Netlify replaces hosting and deployment behavior, not the custody-data acquisition authority. The final architecture may revise this decision if official documentation or testing identifies a material control, privacy, reliability, or cost deficiency.
