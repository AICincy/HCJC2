---
title: Separate Application and Data Publication
reference_namespace: D
status: approved
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

# D-4 Separate Application and Data Publication

- Status: Accepted
- Accepted: 2026-07-21
- Date: 2026-07-20

## Context

HCJC2 requires frequent custody-data refreshes, atomic publication, rollback, explicit health checks, security headers, preview controls, and repository-owned configuration.

V1 couples each data refresh to a full generated-site commit. Repeating that model on Netlify would create a production deploy for each refresh.

As of 2026-07-20, Netlify documents:

- atomic deploys and immutable deploy permalinks
- instantaneous rollback by publishing a prior retained deploy
- automatic deploy deletion after 30 days on free plans or 90 days on paid plans, with longer configurable retention limited to Enterprise
- Deploy Preview URLs accessible to anyone with the link unless protection is configured
- non-production-only password protection limited to Enterprise
- API deployment limits of three deploys per minute and 100 deploys per day
- credit-based billing of 15 credits per successful production deploy

At a 15-minute schedule, 96 successful production deploys per day would consume 43,200 production-deploy credits in a 30-day month and operate close to the documented 100-deploy daily API limit.

## Decision

Use Netlify for:

- the HCJC2 application shell
- static documentation
- infrequent production application releases
- immutable preview and release verification
- custom headers and redirects
- custom domain and TLS management

Do not use a Netlify production deploy as the publication mechanism for every custody-data refresh.

Create a separate public data plane with:

- versioned immutable objects
- atomic canonical-pointer promotion
- independent cache controls
- checksums and manifests
- rollback by pointer
- direct health and freshness verification
- a documented provider decision in a later ADR

The application reads the canonical data manifest at runtime and progressively loads approved public artifacts. Server-side functions are not required for the initial design.

## Application release flow

1. Build the application from a pinned source commit.
2. Run unit, integration, accessibility, security, and privacy tests using synthetic data.
3. Create an unpublished immutable Netlify deploy.
4. Verify the deploy permalink.
5. Validate headers, redirects, CSP, robots behavior, and asset hashes.
6. Promote the verified deploy to production.
7. Record the deploy ID in the release manifest.
8. Roll back by publishing a retained prior deploy or redeploying a retained artifact bundle.

## Preview policy

Because preview URLs are shareable by default and selective non-production protection may require Enterprise, HCJC2 previews must use synthetic fixtures unless an approved protected environment is available. Real roster data is not included in ordinary Deploy Previews.

## Retention consequence

Netlify deploy retention is not the sole rollback archive. HCJC2 retains signed application artifact bundles and release manifests outside Netlify for the project-defined rollback period. A deleted Netlify deploy can then be recreated from its retained bundle.

## Rejected alternatives

### Full Netlify production deploy every sweep

Rejected because it couples data freshness to application deployment, consumes production-deploy credits at high frequency, approaches the API daily deployment limit, and expands the blast radius of source-data changes.

### Netlify Functions as the initial data API

Rejected for the initial release because the public surface is read-heavy static data, and functions add runtime compute, operational complexity, and another failure domain without a proven need.

### Continue committing generated state to `main`

Rejected because repository history is not an operational database, retention engine, or atomic data publication service.

## Required follow-up

- Select and document the public data-plane provider.
- Validate CORS, cache, custom-domain, object-versioning, and deletion controls.
- Measure expected bandwidth and request volume.
- Test Netlify deploy creation, verification, promotion, rollback, and artifact rehydration.
- Reconfirm current Netlify pricing and limits immediately before production commitment.
