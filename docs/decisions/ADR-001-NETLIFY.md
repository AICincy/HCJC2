# ADR-001: Netlify as the V2 Hosting Target

- Status: Provisional
- Date: 2026-07-20

## Context

V1 publishes a static site through GitHub Pages after GitHub Actions acquires data, validates it, builds `docs/`, and commits generated output. HCJC2 requires atomic deployment, preview verification, rollback, security headers, custom-domain support, and repository-owned configuration.

## Decision

Netlify must be evaluated and included in HCJC2 documentation. The provisional target is:

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
