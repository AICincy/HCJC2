# Test Strategy

## Test layers

| Layer | Purpose |
|---|---|
| Unit | Verify deterministic domain logic without network or filesystem access |
| Contract | Verify upstream adapters and public schemas against versioned expectations |
| Integration | Verify stage boundaries, persistence, retries, and failure behavior |
| End-to-end | Verify public routes, search, accessibility, and deployment behavior |
| Resilience | Simulate source failures, stale data, partial data, rate limits, and rollback |
| Privacy | Detect prohibited publication, retention failures, and indexing regressions |
| Migration parity | Compare V1 and V2 outputs during shadow operation |

## Rules

- Tests must cover failure paths, not only successful examples.
- Time, network, random values, and external services must be controllable in tests.
- Production behavior must not depend on test-only branches.
- Test fixtures must avoid unnecessary real personal data.
- Generated snapshots require semantic assertions, not blind acceptance.
- Coverage percentages support review but do not replace risk-based path analysis.
