# Netlify Evaluation

- Evaluation date: 2026-07-20
- Source policy: official Netlify documentation only

## Capability assessment

| Capability | Current finding | HCJC2 use |
|---|---|---|
| Atomic deploys | Netlify documents whole-site atomic deploys rather than individual-file mutation. | Strong fit for application releases. |
| Immutable URLs | Each deploy has a deploy-ID permalink whose contents do not change. | Use for pre-promotion verification and evidence. |
| Rollback | A retained prior successful deploy can be republished immediately. | Strong, but retain independent artifacts because deploys expire. |
| Deploy retention | Default deletion after 30 days on free plans or 90 days on paid plans; Enterprise can configure up to 365 days. | Insufficient as sole rollback archive. |
| Deploy Previews | Generated for pull requests and shareable by URL by default. | Use synthetic fixtures. |
| Preview protection | Password and team-login options exist; non-production-only protection is documented as Enterprise-only. | Do not place real roster data in ordinary previews. |
| Headers | `_headers` or `netlify.toml` can define response headers; header rules are global unless copied per context during build. | Suitable for CSP, HSTS, nosniff, frame, referrer, permissions, COOP, CORP, cache, and CORS policy. |
| Redirects | `_redirects` and `netlify.toml` are repository-controlled. | Suitable for legacy routes and canonical-domain control. |
| Manual/API deploys | API supports digest or ZIP deploys; CLI supports manual production deploys. | Supports external CI-controlled application releases. |
| API limits | Most API calls allow 500 per minute; deploys are limited to 3 per minute and 100 per day. | Per-sweep deployment at 15-minute cadence is too close to the daily limit. |
| Production-deploy billing | Credit plans charge 15 credits per successful production deploy. | Frequent data deployment is economically inefficient. |
| Bandwidth and requests | Credit plans meter bandwidth and web requests. | Model costs before final provider commitment. |
| Audit log | Project audit log is documented for Pro and Enterprise. | Useful supplemental control, not the project system of record. |
| Notifications | Deploy event notifications can target email, pull requests, web services, or Slack. | Integrate as secondary delivery channels. |

## Cadence calculation

| Cadence | Deploys per day | 30-day production-deploy credits |
|---|---:|---:|
| 15 minutes | 96 | 43,200 |
| 30 minutes | 48 | 21,600 |
| 45 minutes | 32 | 14,400 |

These totals exclude bandwidth, web requests, functions, and other metered features.

## Recommendation

Netlify is a good HCJC2 application host but a poor mechanism for publishing every data refresh under the documented 2026 pricing and API model. Separate the application release cadence from the public-data refresh cadence.

## Official sources

- https://docs.netlify.com/api-and-cli-guides/api-guides/get-started-with-api/
- https://docs.netlify.com/deploy/create-deploys/
- https://docs.netlify.com/deploy/deploy-overview/
- https://docs.netlify.com/deploy/deploy-types/deploy-previews/
- https://docs.netlify.com/deploy/manage-deploys/manage-deploys-overview/
- https://docs.netlify.com/manage/security/secure-access-to-sites/password-protection/
- https://docs.netlify.com/manage/routing/headers/
- https://docs.netlify.com/manage/routing/redirects/overview/
- https://docs.netlify.com/build/configure-builds/file-based-configuration/
- https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/
- https://docs.netlify.com/manage/projects/monitor-project-activity/
