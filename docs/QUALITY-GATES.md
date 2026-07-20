# Quality Gates

No change reaches production unless all applicable gates pass.

## Required gates

| Gate | Minimum requirement |
|---|---|
| Formatting and lint | Zero unresolved errors |
| Static typing | Production and test code pass the configured type checker |
| Unit tests | All pass with meaningful assertions |
| Contract tests | Source and public-output contracts pass |
| Integration tests | Pipeline stages pass against controlled fixtures |
| End-to-end tests | Critical public journeys pass with and without JavaScript |
| Accessibility | WCAG AA automated checks and manual keyboard review pass |
| Security | Dependency, secret, header, and public-file scans pass |
| Privacy | No prohibited field, file, correlation, or preview exposure |
| Data quality | Freshness, completeness, duplicate, null, and schema checks pass |
| Build reproducibility | Same inputs produce the same public artifact hashes |
| Deployment | Immutable preview deploy passes health checks before promotion |
| Rollback | Previous validated deploy can be restored and verified |
| Documentation | Contracts, decisions, and runbooks reflect the change |

## Exceptions

Exceptions require a written decision record with owner, rationale, duration, affected risk, compensating control, and removal date.
