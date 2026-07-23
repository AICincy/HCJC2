---
title: Private R2 Origin with Worker Gateway
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

# D-5 Private R2 Origin with Worker Gateway

- Status: Accepted for proof implementation
- Accepted: 2026-07-21
- Date: 2026-07-20

## Context

HCJC2 must refresh public data every 15 minutes without triggering a Netlify production deploy. It must support atomic promotion, rollback, cache control, CORS, active-photo deletion, correlation outputs, and strict denial of prior roster releases.

A directly public object bucket would expose old immutable release keys to anyone who obtained or guessed them. Stable mutable paths would make multi-file promotion non-atomic. The data plane therefore requires a private origin and a controlled gateway.

## Decision

Use Cloudflare R2 as private object storage and a Cloudflare Worker as the only public data gateway.

Use Netlify for the application shell and documentation.

## Bucket classes

| Bucket | Visibility | Purpose | Lock policy |
|---|---|---|---|
| `hcjc2-data-releases` | Private | Versioned JSON and manifests | Short operational retention only |
| `hcjc2-current-photos` | Private | Photos for active roster records | Never locked |
| `hcjc2-control` | Private | Current pointer, promotion receipts, rollback state | No indefinite lock |
| `hcjc2-internal-evidence` | Private, separate credentials | Internal evidence and audit records | Governed by separate retention policy |

The exact bucket names are placeholders until infrastructure implementation.

## Public gateway rules

The Worker must:

1. expose only documented logical routes,
2. reject direct `/releases/` and internal-key access,
3. load the approved pointer from the control bucket,
4. resolve the logical route into the current release prefix,
5. verify object digest and manifest membership,
6. apply exact CORS and security headers,
7. apply route-specific cache policy,
8. emit structured request and failure telemetry,
9. fail closed when the pointer or manifest is invalid,
10. never enumerate bucket contents.

## Promotion

The publisher uploads and validates all immutable release objects first. It then updates the small current pointer using a conditional write. After pointer verification, it purges only logical current URLs that may contain stale responses.

## Rollback

Rollback replaces the current pointer with a previously validated release identifier and purges the same logical URLs. It does not copy, rebuild, or overwrite the prior release.

## Privacy deletion

Photos are not included in immutable release archives. When a person leaves the active roster:

1. delete the photo object,
2. remove the photo reference from the next approved manifest,
3. purge the exact public photo URL,
4. verify origin absence and public 404 behavior,
5. record a deletion receipt without retaining the image.

## Consequences

### Positive

- Atomic logical release promotion.
- Old releases remain private.
- Rollback is fast and API controlled.
- Netlify deploys are decoupled from data refreshes.
- Cache and CORS behavior are centralized.
- Photos receive a stricter deletion path than release JSON.

### Negative

- Adds a Worker runtime to the public data path.
- Requires Cloudflare DNS zone control.
- Requires monitoring of Worker request limits and failures.
- Requires a proof that purge and deletion behavior satisfy the removal policy.

## Rejected alternatives

- Netlify production deploy for each data refresh.
- Public R2 bucket with discoverable immutable release paths.
- Git repository as runtime database and rollback store.
- Netlify Blobs as the authoritative data plane.
- Copying prior release objects to stable paths during promotion.
