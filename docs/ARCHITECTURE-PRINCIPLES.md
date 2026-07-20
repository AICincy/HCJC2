# Architecture Principles

1. **Contracts before implementation.** Every source, transformation, output, and failure mode must have an explicit contract.
2. **Pure core, controlled edges.** Domain rules remain deterministic. Network, filesystem, alerts, and deployment remain replaceable adapters.
3. **Single responsibility.** Critical functions must not combine acquisition, validation, persistence, alerting, and publication.
4. **Explicit state transitions.** Each pipeline run records preflight, acquisition, validation, transformation, build, deploy, verification, and rollback states.
5. **Last-known-good preservation.** Failed or degraded inputs must not replace validated public data.
6. **Idempotency.** Repeating a successful stage with the same inputs must not create divergent outputs.
7. **Schema versioning.** Public and internal artifacts carry schema versions and migration rules.
8. **Provenance by default.** Published datasets identify source, generation time, transformation, status, and checksum.
9. **Static public surface.** The public site should remain static unless a reviewed requirement proves a runtime service is necessary.
10. **No hidden correlation.** Custody identities and unrelated geographic activity remain separate unless a lawful, documented, reviewed purpose is approved.
11. **Operational control through supported APIs.** External services are observed and controlled only through documented, testable integrations.
12. **Documentation is part of the system.** Architecture, contracts, runbooks, and decisions must change with the code they govern.
