# HCJC2 Approved Project Record

- Consolidated: 2026-07-21
- Production baseline: `AICincy/HCJC`
- V2 repository: `AICincy/HCJC2`
- Current phase: architecture foundation and V1 contract extraction

## Approved work tracks

| Track | Decision | Status | Primary records |
|---|---|---|---|
| Governance foundation | Greenfield V2 with V1 as operational reference and rollback baseline | Approved | Project charter, principles, quality gates, migration criteria |
| Correlations | Preserve, redesign, and materially enhance correlations through one canonical engine | Approved | ADR-002 and Correlation System Contract |
| Offense taxonomy | Separate observations, authorities, concepts, and assessments | Approved | ADR-003 and Offense Taxonomy Contract |
| Acquisition and publication | Replace V1 orchestration with an explicit state machine and last-known-good protection | Approved | ADR-004 and Pipeline State Machine Contract |
| Application hosting | Use Netlify for application releases and documentation, not every data refresh | Approved | ADR-004 |
| Public data plane | Use a private R2 origin behind a Worker gateway, subject to proof implementation | Approved | ADR-005 and Public Data Plane Contract |
| Canonical data model | Use versioned common contracts across ingestion, correlation, publication, and frontend | Approved | ADR-006 and Canonical Public Data Model |

## Binding corrections

1. Correlations are a required public capability. Earlier blanket prohibitions were superseded.
2. Public correlations must remain explainable, versioned, correctable, and separated from review-only evidence.
3. Missing offense facts must remain unresolved. They must never default to a legal degree.
4. Failed or partial acquisition must never replace the current approved roster.
5. Application deployment and data publication remain separate release surfaces.
6. The source repository must not act as a runtime database, evidence store, or photo store.

## Next design gate

The next controlled track is the frontend product architecture. It covers route hierarchy, search, correlation presentation, data status, progressive enhancement, accessibility, component boundaries, and the approved visual system.
