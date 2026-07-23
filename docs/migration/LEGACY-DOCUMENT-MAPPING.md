---
title: HCJC2 Legacy Document Mapping
reference_namespace: V2
status: approved
authority: v2-legacy-document-mapping
owner_repository: AICincy/HCJC2
document_family: migration
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

# HCJC2 Legacy Document Mapping

> **Authority:** Migration ledger mapping earlier HCJC2 documentation into controlled modules or explicitly classified supporting material.

| Legacy path | Section | Classification | Destination | Action | State | Verification |
|---|---|---|---|---|---|---|
| `docs/ARCHITECTURE-PRINCIPLES.md` | Entire document | controlled source | `docs/architecture/SYSTEM-ARCHITECTURE.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/MIGRATION-ACCEPTANCE.md` | Entire document | controlled source | `docs/migration/MIGRATION-AND-TRACEABILITY.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/PRIVACY-INVARIANTS.md` | Entire document | controlled source | `docs/governance/PRIVACY-AND-LEGAL.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/PROJECT-CHARTER.md` | Entire document | controlled source | `docs/MASTER-SPEC.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/QUALITY-GATES.md` | Entire document | controlled source | `docs/quality/TESTING-AND-QUALITY.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/TEST-STRATEGY.md` | Entire document | controlled source | `docs/quality/TESTING-AND-QUALITY.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/V1-DISPOSITION.md` | Entire document | controlled source | `docs/migration/MIGRATION-AND-TRACEABILITY.md` | consolidated | verified | Reviewed against approved architecture design |
| `docs/decisions/ADR-001-NETLIFY.md` | Entire document | controlled source | `docs/decisions/ADR-001-NETLIFY.md` | consolidated | verified | Reviewed against approved architecture design |
| `.gitattributes` | Entire document | project record | `docs/supporting/historical/.gitattributes` | preserved | verified | Source preserved and destination reviewed |
| `.gitignore` | Entire document | project record | `docs/supporting/historical/.gitignore` | preserved | verified | Source preserved and destination reviewed |
| `README.md` | Entire document | project record | `docs/supporting/historical/README.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/CONSOLIDATION-RECORD.md` | Entire document | historical record | `docs/supporting/historical/CONSOLIDATION-RECORD.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/PROJECT-RECORD.md` | Entire document | historical record | `docs/supporting/historical/PROJECT-RECORD.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/README.md` | Entire document | legacy controlled source | `docs/supporting/historical/README.md` | consolidated | verified | Source preserved and destination reviewed |
| `docs/audits/V1-ACQUISITION-PUBLICATION-AUDIT.md` | Entire document | non-authoritative audit | `docs/supporting/audits/V1-ACQUISITION-PUBLICATION-AUDIT.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/audits/V1-CORRELATION-AUDIT.md` | Entire document | non-authoritative audit | `docs/supporting/audits/V1-CORRELATION-AUDIT.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/audits/V1-OFFENSE-TAXONOMY-AUDIT.md` | Entire document | non-authoritative audit | `docs/supporting/audits/V1-OFFENSE-TAXONOMY-AUDIT.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/audits/V1-PUBLIC-DATA-CONTRACT-AUDIT.md` | Entire document | non-authoritative audit | `docs/supporting/audits/V1-PUBLIC-DATA-CONTRACT-AUDIT.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/contracts/ARTIFACT-CLASSIFICATION-RETENTION.md` | Entire document | approved contract | `docs/data/ARTIFACT-CLASSIFICATION-RETENTION.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/CANONICAL-PUBLIC-DATA-MODEL.md` | Entire document | approved contract | `docs/data/CANONICAL-PUBLIC-DATA-MODEL.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/CORRELATION-SYSTEM.md` | Entire document | approved contract | `docs/correlations/CORRELATION-SYSTEM.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/FEED-REGISTRY.md` | Entire document | approved contract | `docs/data/FEED-REGISTRY.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/LABELED-CORRELATION-FIXTURES.md` | Entire document | approved contract | `docs/correlations/LABELED-CORRELATION-FIXTURES.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/OFFENSE-TAXONOMY.md` | Entire document | approved contract | `docs/taxonomy/OFFENSE-TAXONOMY-CONTRACT.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/PIPELINE-STATE-MACHINE.md` | Entire document | approved contract | `docs/pipeline/PIPELINE-STATE-MACHINE.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/contracts/PUBLIC-DATA-PLANE.md` | Entire document | approved contract | `docs/pipeline/PUBLIC-DATA-PLANE.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/costs/DATA-PLANE-COST-MODEL.md` | Entire document | controlled extension | `docs/operations/costs/DATA-PLANE-COST-MODEL.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/decisions/ADR-002-CORRELATION-ENGINE.md` | Entire document | architecture decision | `docs/decisions/ADR-002-CORRELATION-ENGINE.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/decisions/ADR-003-OFFENSE-TAXONOMY.md` | Entire document | architecture decision | `docs/decisions/ADR-003-OFFENSE-TAXONOMY.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/decisions/ADR-004-NETLIFY-AND-DATA-PUBLICATION.md` | Entire document | architecture decision | `docs/decisions/ADR-004-NETLIFY-AND-DATA-PUBLICATION.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/decisions/ADR-005-R2-WORKER-DATA-PLANE.md` | Entire document | architecture decision | `docs/decisions/ADR-005-R2-WORKER-DATA-PLANE.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/decisions/ADR-006-CANONICAL-DATA-CONTRACTS.md` | Entire document | architecture decision | `docs/decisions/ADR-006-CANONICAL-DATA-CONTRACTS.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/migration/V1-TO-V2-DATA-MAPPING.md` | Entire document | migration source | `docs/migration/V1-TO-V2-DATA-MAPPING.md` | consolidated | verified | Source preserved and destination reviewed |
| `docs/research/CORRELATION-RESEARCH-NOTES.md` | Entire document | non-authoritative research | `docs/supporting/research/CORRELATION-RESEARCH-NOTES.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/research/DATA-PLANE-PROVIDER-EVALUATION-2026-07-20.md` | Entire document | non-authoritative research | `docs/supporting/research/DATA-PLANE-PROVIDER-EVALUATION-2026-07-20.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/research/NETLIFY-EVALUATION-2026-07-20.md` | Entire document | non-authoritative research | `docs/supporting/research/NETLIFY-EVALUATION-2026-07-20.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/research/OFFENSE-TAXONOMY-RESEARCH-NOTES.md` | Entire document | non-authoritative research | `docs/supporting/research/OFFENSE-TAXONOMY-RESEARCH-NOTES.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/runbooks/DATA-PROMOTION-ROLLBACK.md` | Entire document | controlled extension | `docs/operations/runbooks/DATA-PROMOTION-ROLLBACK.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/runbooks/DEPLOYMENT-CONTROL.md` | Entire document | controlled extension | `docs/operations/runbooks/DEPLOYMENT-CONTROL.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/security/DATA-PLANE-BOUNDARIES.md` | Entire document | controlled extension | `docs/operations/security/DATA-PLANE-BOUNDARIES.md` | migrated | verified | Source preserved and destination reviewed |
| `docs/tracks/01-foundation.md` | Entire document | historical planning | `docs/supporting/historical/tracks/01-foundation.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/tracks/02-correlation.md` | Entire document | historical planning | `docs/supporting/historical/tracks/02-correlation.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/tracks/03-offense-taxonomy.md` | Entire document | historical planning | `docs/supporting/historical/tracks/03-offense-taxonomy.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/tracks/04-pipeline-and-deployment.md` | Entire document | historical planning | `docs/supporting/historical/tracks/04-pipeline-and-deployment.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/tracks/05-data-plane.md` | Entire document | historical planning | `docs/supporting/historical/tracks/05-data-plane.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/tracks/06-canonical-data-model.md` | Entire document | historical planning | `docs/supporting/historical/tracks/06-canonical-data-model.md` | preserved | verified | Source preserved and destination reviewed |
| `docs/tracks/index.md` | Entire document | historical planning | `docs/supporting/historical/tracks/index.md` | preserved | verified | Source preserved and destination reviewed |
| `examples/activity-events.example.json` | Entire document | schema example | `examples/activity-events.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/artifact-manifest.example.json` | Entire document | schema example | `examples/artifact-manifest.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/correlation-fixture.example.json` | Entire document | schema example | `examples/correlation-fixture.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/map-feature-collection.example.json` | Entire document | schema example | `examples/map-feature-collection.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/offense-assessment.example.json` | Entire document | schema example | `examples/offense-assessment.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/offense-observation.example.json` | Entire document | schema example | `examples/offense-observation.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/roster-snapshot.example.json` | Entire document | schema example | `examples/roster-snapshot.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/run-manifest.example.json` | Entire document | schema example | `examples/run-manifest.example.json` | migrated | verified | Source preserved and destination reviewed |
| `examples/search-index.example.json` | Entire document | schema example | `examples/search-index.example.json` | migrated | verified | Source preserved and destination reviewed |
| `project-manifest.json` | Entire document | project record | `docs/supporting/historical/project-manifest.json` | preserved | verified | Source preserved and destination reviewed |
| `schemas/activity-events.schema.json` | Entire document | machine-readable schema | `schemas/activity-events.schema.json` | migrated | verified | Source preserved and destination reviewed |
| `schemas/common.schema.json` | Entire document | machine-readable schema | `schemas/common.schema.json` | migrated | verified | Source preserved and destination reviewed |
| `schemas/data-pointer.schema.json` | Entire document | machine-readable schema | `schemas/data-pointer.schema.json` | migrated | verified | Source preserved and destination reviewed |
| `schemas/map-feature-collection.schema.json` | Entire document | machine-readable schema | `schemas/map-feature-collection.schema.json` | migrated | verified | Source preserved and destination reviewed |
| `schemas/release-manifest.schema.json` | Entire document | machine-readable schema | `schemas/release-manifest.schema.json` | migrated | verified | Source preserved and destination reviewed |
| `schemas/roster-snapshot.schema.json` | Entire document | machine-readable schema | `schemas/roster-snapshot.schema.json` | migrated | verified | Source preserved and destination reviewed |
| `schemas/search-index.schema.json` | Entire document | machine-readable schema | `schemas/search-index.schema.json` | migrated | verified | Source preserved and destination reviewed |
