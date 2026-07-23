# Public Data-Plane Provider Evaluation

- Date: 2026-07-20
- Scope: public JSON datasets, active-roster photos, correlation outputs, release manifests, rollback, cache control, CORS, logging, retention, and deletion
- Excluded: application-shell hosting, long-term evidentiary storage, internal operational logs, and source acquisition compute

## Question

Which provider best supports frequent HCJC2 data publication without coupling each data refresh to a Netlify production deploy?

## Current workload profile

The July 20 V1 snapshot contains:

| Artifact class | Count | Size |
|---|---:|---:|
| Public JSON files | 16 | 32.23 MB |
| Public JSON excluding the improperly public WAF ledger | 15 | 15.32 MB |
| Active photo files | 1,180 | 10.43 MB |
| Intended refresh frequency | 96 runs/day | every 15 minutes |

The public WAF ledger must move to an internal evidence class and is excluded from the V2 public cost baseline.

## Required controls

1. Private origin storage.
2. Public custom domain.
3. Exact CORS allowlist.
4. Immutable release objects.
5. Atomic promotion through one small pointer.
6. API-controlled rollback.
7. Per-object cache policy.
8. Immediate explicit deletion path for released-person photos.
9. Cache purge and deletion verification.
10. Access and configuration audit logs.
11. Prefix-specific retention and lock rules.
12. No public access to prior roster releases.
13. Predictable cost at 96 publication decisions per day.

## Provider comparison

| Criterion | Cloudflare R2 + Worker | AWS S3 + CloudFront | Backblaze B2 + CDN | Netlify Blobs |
|---|---|---|---|---|
| Private object origin | Strong | Strong | Strong | Project-scoped |
| Custom public domain | Worker custom domain | CloudFront distribution | Requires CDN or custom-domain arrangement | Through Netlify project routes |
| Immutable-key model | Strong | Strong | Strong | Possible |
| Native object versions | No S3 bucket versioning; use immutable keys | Full S3 versioning | Native file versions | Not a release-version system |
| Retention lock | Cloudflare bucket locks | S3 Object Lock | B2 Object Lock | No comparable object-lock control identified |
| CORS | Bucket or gateway controlled | Bucket and distribution controlled | Bucket controlled | Route/application controlled |
| Cache control | Worker and Cloudflare Cache | CloudFront policies | CDN dependent | Edge cached |
| Deletion propagation | Explicit delete plus cache purge | Delete version plus invalidation | Hide/delete versions plus CDN purge | Updates/deletes propagate within 60 seconds |
| Access logs | Cloudflare HTTP logs and Worker telemetry, plan dependent | CloudFront, S3, CloudTrail, CloudWatch | Bucket access logs, best effort | Netlify project logs and usage controls |
| Egress economics | R2 egress free | Free tiers and plan options, then AWS pricing | 3x stored-data egress free, partner CDN options | Credit-metered bandwidth and requests |
| Operational complexity | Moderate, one provider | High | Moderate to high, often two providers | Low, but coupled to Netlify project and billing |
| Fit for urgent photo removal | Strong with separate unlocked photo prefix and purge | Strong if versioning and retention are carefully separated | More complex because hidden and prior versions can persist | Eventual edge propagation |
| Recommended role | Primary | Enterprise fallback | Cost fallback | Do not use as authoritative data plane |

## Cloudflare R2 findings

Cloudflare R2 provides S3-compatible object operations, Workers bindings, custom-domain delivery, CORS, object lifecycle rules, bucket locks, audit logs for configuration changes, and zero R2 egress charges. Standard storage is listed at $0.015 per GB-month, with 10 GB-month, one million Class A operations, and ten million Class B operations included monthly.

R2 does not implement S3 bucket versioning or S3 Object Lock through the compatibility API. Cloudflare provides its own bucket-lock API. HCJC2 does not require mutable-key versioning because releases will use immutable keys and a separate pointer.

R2 access through its APIs is strongly consistent, but a custom domain using Cloudflare Cache has relaxed consistency. Deleted or overwritten objects may remain cached until TTL expiration or purge. HCJC2 therefore requires explicit purge and verification for canonical pointers and deleted photos.

A directly public R2 bucket is insufficient because anyone who knows an old release key could retrieve that prior roster. The R2 bucket must remain private. A Worker gateway will permit only logical current paths and will reject direct release-prefix access.

## AWS findings

S3 provides native versioning, lifecycle policies, Object Lock, server access logging, CloudTrail, and mature IAM. CloudFront provides custom domains, caching, invalidations, origin restriction, logging, and broad operational controls.

AWS is the strongest alternative where formal versioning, multi-region replication, advanced identity controls, and organization-wide AWS governance are required. It also has the highest configuration surface. Versioning and Object Lock can conflict with urgent personal-data deletion if photos and public-current data are not isolated from retained records.

The current CloudFront pricing page offers flat-rate plans, including a free plan with 100 GB transfer, one million requests, and 5 GB S3 storage. AWS also documents a pay-as-you-go free tier of one TB transfer and ten million requests per month. Actual architecture cost depends on the selected pricing model and supporting services.

## Backblaze B2 findings

B2 provides native file versions, lifecycle rules, Object Lock, CORS, S3-compatible and native APIs, and bucket access logs. The published pay-as-you-go rate starts at $6.95 per TB-month, with free egress up to three times average monthly storage and broader free egress through listed CDN partners.

B2 is cost-effective storage, but the preferred public architecture generally adds a CDN or custom-domain layer. Its bucket access logs are best effort, may be delayed, incomplete, or duplicated, and should not be treated as a complete accounting. Native versions also require careful lifecycle design for removal requests.

## Netlify Blobs findings

Netlify Blobs is easy to integrate with a Netlify application, but it uses eventual consistency by default and guarantees update and deletion propagation to edge locations within 60 seconds. It also shares the Netlify account's credit and project-availability model. On credit-based plans, exhausted credits can pause all projects.

Netlify Blobs remains useful for application-specific state that is not the authoritative custody-data publication plane. It does not provide the desired operational separation between application releases and frequent data refreshes.

## Recommendation

Select Cloudflare R2 with a Cloudflare Worker gateway.

### Required topology

```text
GitHub Actions publisher
        |
        | signed API operations
        v
Private R2 buckets
  - release data
  - current photos
  - private rollback archive
        |
        | R2 bindings
        v
Cloudflare Worker gateway
        |
        | data.aretheyinjail.com
        v
Netlify-hosted application and public clients
```

### Why this topology wins

- Netlify deploy frequency remains low and tied to application releases.
- Data promotion is one pointer update, not a site deploy.
- Prior releases remain private.
- Rollback changes only the pointer.
- Photos can use a separate unlocked deletion policy.
- R2 and Workers share one control plane and API-token model.
- Egress charges are not imposed by R2 or Workers.
- Expected storage and operation volume is small relative to included usage.

## Uncertainty and required proof

Before production acceptance, HCJC2 must run a provider proof that verifies:

1. pointer update and rollback under cache,
2. exact CORS behavior,
3. removal of a photo from R2 and all cache paths,
4. direct denial of private release keys,
5. Worker fail-closed behavior,
6. access-log availability on the selected Cloudflare plan,
7. monthly cost alerts,
8. recovery with the Worker unavailable,
9. secret rotation,
10. DNS and certificate ownership.

## Primary sources

- Cloudflare R2 pricing: https://developers.cloudflare.com/r2/pricing/
- Cloudflare R2 S3 compatibility: https://developers.cloudflare.com/r2/api/s3/api/
- Cloudflare R2 consistency: https://developers.cloudflare.com/r2/reference/consistency/
- Cloudflare R2 bucket locks: https://developers.cloudflare.com/r2/buckets/bucket-locks/
- Cloudflare R2 lifecycle rules: https://developers.cloudflare.com/r2/buckets/object-lifecycles/
- Cloudflare R2 audit logs: https://developers.cloudflare.com/r2/platform/audit-logs/
- Cloudflare Workers pricing: https://developers.cloudflare.com/workers/platform/pricing/
- Cloudflare Workers custom domains: https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
- Amazon S3 Object Lock: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
- Amazon S3 security practices: https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
- Amazon CloudFront pricing: https://aws.amazon.com/cloudfront/pricing/
- Backblaze B2 pricing: https://www.backblaze.com/cloud-storage/pricing
- Backblaze file versions: https://www.backblaze.com/docs/cloud-storage-file-versions
- Backblaze bucket access logs: https://www.backblaze.com/docs/cloud-storage-bucket-access-logs
- Netlify Blobs: https://docs.netlify.com/build/data-and-storage/netlify-blobs/
- Netlify credit billing: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/
