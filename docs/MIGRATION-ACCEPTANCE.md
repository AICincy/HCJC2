# Migration Acceptance Criteria

Production cutover from V1 to HCJC2 requires all criteria below.

## Data parity

- No unexplained active-roster omissions or additions.
- Charge, custody, court, bond, and photo fields meet approved parity contracts.
- Booking, release, and material-change semantics are verified.
- Supplemental feeds publish with documented status and freshness.

## Safety

- Last-known-good preservation passes forced-failure tests.
- Public/private boundary tests pass.
- Retention and photo-removal tests pass.
- Legal notices and correction routes are present.

## User experience

- Required routes work at mobile and desktop widths.
- Search, filtering, and record views work without required JavaScript.
- WCAG AA review passes.
- Performance budgets pass on representative devices and networks.

## Operations

- Netlify deployment is reproducible from the repository.
- Preview exposure controls are verified.
- Production health checks run after deployment.
- Rollback is tested against an actual prior deploy.
- Alert ownership and incident runbooks are documented.
- V1 remains available as a rollback target through the stabilization period.

## Approval record

Cutover requires a dated decision record listing evidence for each criterion, unresolved risks, rollback authority, and stabilization duration.
