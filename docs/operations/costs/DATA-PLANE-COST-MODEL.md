# Data-Plane Cost Model

- Date: 2026-07-20
- Purpose: planning estimate, not a provider quote

## Baseline

| Input | Value |
|---|---:|
| Publication decisions | 96/day |
| Days modeled | 30 |
| JSON artifacts per release | 15 |
| Manifest, status, and pointer writes | 3 |
| Approximate non-WAF JSON size | 15.32 MB/release |
| Current photos | 10.43 MB |

## Naive full-release retention

Seven days of full JSON releases:

```text
15.32 MB x 96 x 7 = approximately 10.3 GB
```

This is a conservative upper bound. Content-addressed reuse and feed-specific update frequency should reduce actual storage.

## R2 operations

Approximate writes:

```text
18 writes/run x 96 runs/day x 30 days = 51,840 Class A operations/month
```

This remains below the published R2 monthly inclusion of one million Class A operations.

Reads depend on public traffic and Worker cache efficiency. The published inclusion is ten million Class B operations monthly. R2 egress is listed as free.

## Worker gateway

The Workers Free plan permits 100,000 requests per day and has a hard daily limit. HCJC2 should use the Workers Paid plan before production so a traffic spike does not disable the data gateway. The published paid minimum is $5/month and includes ten million requests monthly, with additional requests priced per million.

## Expected order of magnitude

| Component | Expected early-stage cost |
|---|---|
| Workers Paid minimum | $5/month |
| R2 storage | Near free tier to low single digits |
| R2 operations | Likely included at baseline |
| R2 egress | $0 from R2 |
| Cloudflare DNS and basic cache | Plan dependent; validate account configuration |
| Logpush or advanced logs | Plan dependent |

## Cost controls

1. Alert at 50, 75, and 90 percent of request and storage budgets.
2. Do not write unchanged feed objects.
3. Use content-addressed objects where privacy retention permits.
4. Keep the WAF and evidence ledger outside the public data plane.
5. Expire private release objects after the approved rollback window.
6. Do not snapshot photos into each release.
7. Cache public logical routes and use ETags.
8. Record cost per successful promotion.

## Provider-source rates

- R2 Standard storage: $0.015/GB-month.
- R2 Class A: $4.50/million after included usage.
- R2 Class B: $0.36/million after included usage.
- Workers Paid minimum: $5/month.
- Workers Paid requests: ten million included, then $0.30/additional million.

Rates must be rechecked before procurement or production launch.
