# HCJC2 Consolidation Record

- Consolidated: 2026-07-21
- Source packages: 6
- Substantive source files: 50
- Packaging indexes excluded: 6
- Repository destination: internal HCJC2 workspace

## Integrated packages

| Package | Integrated content |
|---|---|
| HCJC2 bootstrap | Project charter, principles, privacy, quality, testing, migration, and ADR-001 |
| Correlation design | V1 audit, system contract, ADR-002, and research notes |
| Offense taxonomy | V1 audit, taxonomy and fixture contracts, ADR-003, research notes, and examples |
| Pipeline audit | V1 audit, state machine, artifact policy, ADR-004, runbook, research, and examples |
| Data plane | Provider evaluation, ADR-005, public contract, runbook, security, cost model, and schemas |
| Canonical data model | V1 audit, canonical and feed contracts, ADR-006, migration map, schemas, and examples |

## Reconciliations

1. Replaced the original blanket prohibition on public correlations with the approved governed-correlation mandate.
2. Marked ADR-002 through ADR-006 according to the user's approvals.
3. Marked ADR-001 as superseded in part by ADR-004 and ADR-005.
4. Updated the hosting summary to separate the Netlify application plane from the R2 and Worker data plane.
5. Moved JSON examples out of the schema directory.
6. Added repository ignore rules for logs, ZIP archives, runtime data, photos, evidence, caches, and environment files.
7. Replaced six package README files with one documentation index and one approved project record.

## Validation

- All ZIP source packages passed archive integrity tests.
- All JSON files parsed successfully.
- All Draft 2020-12 JSON Schemas passed schema validation.
- All four schema-backed canonical examples passed validation.
- All local Markdown links resolved.
- No ZIP package or Malwarebytes log exists in the consolidated repository tree.
- No em dash or en dash characters exist in the consolidated Markdown or JSON files.

## Retained source artifacts

The original ZIP packages remain outside the consolidated repository as historical source artifacts. They are superseded for active project work and are not part of the HCJC2 repository tree.
