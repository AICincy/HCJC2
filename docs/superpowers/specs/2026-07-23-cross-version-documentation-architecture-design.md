---
title: Cross-Version Documentation Architecture
status: approved
authority: documentation-architecture-design
owner_repository: AICincy/HCJC2
document_family: governance
effective_date: 2026-07-23
supersedes: []
superseded_by: null
applies_to:
  - AICincy/HCJC
  - AICincy/HCJC2
canonical_reference:
  planned_version: 1.0.0
  planned_tag: reference-v1.0.0
---

# Cross-Version Documentation Architecture

> **Authority:** Approved design for structuring, referencing, validating, migrating, and governing the JCStream V1 and HCJC2 documentation systems. HCJC2 owns shared cross-version definitions. V1 controls descriptions of implemented V1 behavior. HCJC2 controls V2 requirements and planned behavior.

## 1. Purpose

This design establishes a documentation system for `AICincy/HCJC` and `AICincy/HCJC2` that is accurate, readable, stable under reorganization, and suitable for long-term cross-version traceability.

The system uses:

- one HCJC2-owned canonical cross-version reference
- concise master specifications for V1 and V2
- ten mirrored controlled document families
- short human-readable identifiers
- subject-specific authority
- explicit supersession metadata
- generated registries and traceability matrices
- a staged legacy-document migration process

## 2. Design objectives

The documentation architecture must:

1. preserve V1 as an accurate reference for implemented behavior
2. establish HCJC2 as the canonical owner of shared terminology and concepts
3. provide one authoritative home for each substantive rule or behavior
4. keep citations easy to read and easy to type
5. preserve reference identity when files or headings move
6. distinguish current, historical, superseded, retired, deprecated, and withdrawn material
7. connect shared concepts to V1 behavior, V2 requirements, decisions, schemas, tests, and evidence
8. preserve all legacy content until migration is verified
9. avoid V1's generated GitHub Pages `docs/` directory
10. remain understandable without running tooling

## 3. Authority model

Authority is subject-specific.

| Subject | Controlling source |
|---|---|
| Shared terminology and cross-version meaning | HCJC2 canonical reference |
| Implemented V1 behavior | V1 controlled modules |
| V2 requirements and planned behavior | V2 controlled modules |
| Architecture decisions | Approved ADRs |
| Machine-readable structure | Versioned schemas |
| Executable verification | Tests and checks |
| Recorded proof | Evidence records |
| Research, audits, and history | Supporting materials, non-authoritative |

Every controlled document must include YAML metadata and a visible authority statement.

## 4. Repository structure

### 4.1 HCJC2

```text
HCJC2/
  README.md
  docs/
    MASTER-SPEC.md
    reference/
      HCJC-CANONICAL-REFERENCE.md
      REFERENCE-REGISTRY.md
      TRACEABILITY-MATRIX.md
      REFERENCE-RELEASES.md
    architecture/SYSTEM-ARCHITECTURE.md
    data/DATA-AND-SCHEMAS.md
    pipeline/ACQUISITION-AND-PUBLICATION.md
    correlations/CORRELATIONS.md
    taxonomy/OFFENSE-TAXONOMY.md
    product/PRODUCT-AND-UI-UX.md
    governance/PRIVACY-AND-LEGAL.md
    operations/OPERATIONS-AND-SECURITY.md
    quality/TESTING-AND-QUALITY.md
    migration/
      MIGRATION-AND-TRACEABILITY.md
      LEGACY-DOCUMENT-MAPPING.md
    decisions/
    supporting/
      research/
      evidence/
      audits/
      historical/
    superpowers/specs/
```

### 4.2 HCJC V1

```text
HCJC/
  README.md
  docs-reference/
    MASTER-SPEC.md
    architecture/SYSTEM-ARCHITECTURE.md
    data/DATA-AND-SCHEMAS.md
    pipeline/ACQUISITION-AND-PUBLICATION.md
    correlations/CORRELATIONS.md
    taxonomy/OFFENSE-TAXONOMY.md
    product/PRODUCT-AND-UI-UX.md
    governance/PRIVACY-AND-LEGAL.md
    operations/OPERATIONS-AND-SECURITY.md
    quality/TESTING-AND-QUALITY.md
    migration/
      MIGRATION-AND-TRACEABILITY.md
      LEGACY-DOCUMENT-MAPPING.md
    reference/TRACEABILITY-MATRIX-SNAPSHOT.md
    supporting/
      research/
      evidence/
      audits/
      historical/
```

V1 uses `docs-reference/` because `docs/` is its generated production site.

## 5. Controlled document families

Both repositories use the same ten document families.

| Family | Controlled subject |
|---|---|
| System Architecture | boundaries, topology, components, dependencies, storage, runtime, architectural invariants |
| Data and Schemas | entities, identifiers, fields, records, serialization, artifacts, compatibility, unknown states |
| Acquisition and Publication | sources, adapters, schedules, retries, validation, build, promotion, freshness, rollback |
| Correlations | relationship types, candidates, evidence, scoring, competition, cardinality, review, disputes, evaluation |
| Offense Taxonomy | charge observations, legal authority, concepts, degree labels, assessments, unresolved states |
| Product and UI/UX | information architecture, routes, navigation, search, visual design, responsiveness, accessibility, content |
| Privacy and Legal | public-records posture, disclaimers, indexing, photos, corrections, removals, disputes, classifications |
| Operations and Security | credentials, automation, observability, incidents, deployment, rollback, evidence, secrets |
| Testing and Quality | test layers, quality gates, accessibility, privacy, security, reproducibility, resilience |
| Migration and Traceability | V1 inventory and evidence; V2 parity, cutover, rollback, stabilization, retirement |

Version-specific extensions may be added only when the core module links to them and states their authority.

## 6. Canonical reference

The canonical reference lives at:

```text
HCJC2/docs/reference/HCJC-CANONICAL-REFERENCE.md
```

It defines concepts that must retain the same meaning across versions. It is version-neutral and may include concise V1 and V2 interpretation notes.

Its structure is:

1. authority and usage
2. shared principles
3. terminology and record concepts
4. source systems
5. identity and identifier concepts
6. data lifecycle and release concepts
7. correlation terminology
8. offense and legal terminology
9. product and public-presentation concepts
10. operations, evidence, and quality concepts
11. concise V1/V2 traceability matrix
12. registry and release history

A canonical entry uses a visible reference heading:

```markdown
## A-12 Correlation

**Definition:** A documented relationship, association, or candidate association between two or more records.

**V1 interpretation:** Concise description and link to V1 behavior.

**V2 interpretation:** Concise description and link to V2 requirements.
```

## 7. Master specifications

Each repository has a concise `MASTER-SPEC.md`.

The master specification contains:

1. metadata and visible authority
2. system identity
3. purpose
4. scope and exclusions
5. governing principles
6. critical invariants
7. authority map
8. module index
9. decision index
10. canonical-reference relationship
11. supersession rules
12. maintenance ownership

It does not restate all module content.

## 8. README responsibilities

Each root README provides compact orientation:

- system purpose
- current production or development status
- concise architecture summary
- documentation authority notice
- links to the master specification and canonical reference
- links to all ten controlled modules
- essential contributor or operator commands
- support, correction, and security links

The README does not become a second master specification.

## 9. Reference identifiers

The documentation uses human-readable continuous namespaces.

| Namespace | Meaning |
|---|---|
| `A-` | Shared canonical concept |
| `V1-` | Implemented V1 behavior |
| `V2-` | V2 requirement or controlled rule |
| `D-` | Architecture decision |
| `S-` | Schema family |
| `T-` | Test or verification procedure |
| `E-` | Retained evidence |

Rules:

1. numbering is continuous within each namespace
2. identifiers are globally unique within their namespace
3. numbering does not restart by file
4. moved content keeps its identifier
5. retired identifiers are never reused
6. human authors assign identifiers
7. tooling validates but never automatically assigns or renumbers identifiers
8. only controlled sections and independently traceable rules receive identifiers
9. supporting subsections retain ordinary headings

Example:

```markdown
## V2-57 Correlation Assessments

### Supporting evidence

### Conflicting evidence

## V2-58 Evidence scores must not be described as probabilities without calibration
```

## 10. Citation format

Normal prose uses the linked identifier and title:

```markdown
See [A-12 Correlation](...).
See [V1-42 Candidate Dispatch Relationships](...).
See [V2-57 Correlation Assessments](...).
See [D-2 Canonical Correlation Engine](...).
See [S-8 Correlation Schema](...).
See [T-19 Correlation Competition Verification](...).
See [E-14 Correlation Evaluation Results](...).
```

Bare identifiers may be used in nearby tables after the full title has been introduced.

## 11. Duplication policy

> Define shared meaning once, summarize it locally, and document version-specific behavior only in the applicable version module.

The canonical reference contains the full shared definition.

A V1 module contains:

- concise shared-concept summary
- pinned canonical citation
- implemented V1 behavior
- implementation references
- tests and evidence

A V2 module contains:

- concise shared-concept summary
- current canonical citation
- binding requirements
- decisions
- schemas
- acceptance criteria
- tests and evidence

ADRs explain rationale. Continuing requirements remain in controlled modules.

## 12. Metadata and lifecycle

Controlled documents begin with YAML front matter:

```yaml
---
title: Product and UI/UX
reference_namespace: V2
status: approved
authority: v2-product
owner_repository: AICincy/HCJC2
document_family: product
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
reviewers: []
---
```

They then provide a visible authority statement.

Approved lifecycle values are:

- proposed
- draft
- in-review
- approved
- deprecated
- superseded
- retired
- withdrawn

Rules:

- superseded documents identify an approved replacement
- retired documents have no direct replacement
- withdrawn documents must not be relied upon
- deprecated documents remain temporarily valid while replacement is planned
- superseded and retired identifiers remain reserved
- historical documents remain accessible

## 13. Decisions, schemas, tests, and evidence

Existing ADR filenames remain intact. ADRs receive shorter `D-` codes for prose citations.

`S-` codes identify stable schema families. Semantic versions identify compatible or breaking schema revisions.

`T-` codes identify executable tests, checks, or verification procedures.

`E-` codes identify retained results, reviews, approvals, incident records, and operational proof.

## 14. Supporting materials

Non-authoritative material lives beneath a clear boundary:

```text
supporting/
  research/
  evidence/
  audits/
  historical/
```

Supporting material may be cited but cannot define or override requirements.

## 15. Registry and traceability

HCJC2 owns:

```text
docs/reference/REFERENCE-REGISTRY.md
docs/reference/TRACEABILITY-MATRIX.md
```

V1 keeps a pinned snapshot:

```text
docs-reference/reference/TRACEABILITY-MATRIX-SNAPSHOT.md
```

The registry records every controlled identifier, including:

- code
- title
- namespace
- repository
- file
- anchor
- status
- authority
- effective date
- supersession
- canonical-reference version

The traceability matrix connects:

- canonical concepts
- V1 behavior
- V2 requirements
- decisions
- schemas
- tests
- evidence
- migration status

Approved relationship labels include:

- defines
- implements
- requires
- refines
- replaces
- preserves
- verifies
- produces-evidence-for
- supersedes
- maps-to
- accepted-difference-from
- depends-on
- constrained-by

## 16. Generation and validation

Controlled documents are the source of truth. Generated registries and matrices are indexes, not independent authorities.

The generator must:

1. parse approved controlled-document locations
2. read front matter
3. identify controlled headings
4. derive anchors
5. collect relationships
6. detect duplicate or malformed identifiers
7. preserve retired references
8. generate registry and matrix files deterministically
9. compare generated output with committed output
10. fail CI when generated output is stale

The generator must not:

- assign or renumber identifiers
- modify controlled documents
- infer authority from path alone
- treat ordinary headings as controlled entries
- reuse retired identifiers

CI must reject:

- duplicate or malformed identifiers
- missing titles or anchors
- broken controlled links
- unknown references
- invalid lifecycle values
- approved documents without authority metadata
- supersession without replacement
- supersession cycles
- reused retired identifiers
- incompatible canonical major versions
- schema references without registered schema families
- requirements linked to absent tests
- evidence without date or provenance
- stale generated output
- inconsistent V1 snapshot metadata

Historical citations to superseded or retired entries must declare historical intent.

## 17. Canonical-reference releases

Canonical-reference releases use semantic versions and release dates.

Example:

```text
Tag: reference-v1.0.0
Released: 2026-07-23
```

| Release | Meaning | Approval |
|---|---|---|
| Patch | editorial or citation correction without changed meaning | documentation maintainer |
| Minor | additive compatible concepts or mappings | affected family owner and repository owner |
| Major | changed meaning, authority, identifier semantics, or compatibility | repository owner with explicit V1 and V2 impact review |

V1 records the exact canonical release and HCJC2 commit against which it was reviewed. V1 citations use the pinned release while also providing a convenience link to the current edition.

## 18. Legacy-document migration

Each repository contains:

```text
migration/LEGACY-DOCUMENT-MAPPING.md
```

Every substantive legacy section is assigned a destination or explicit disposition.

Migration states are:

- inventoried
- classified
- mapped
- migrated
- verified
- archived
- retired

The mapping records:

- legacy path
- original heading or range
- content classification
- destination reference
- action
- state
- review status
- preserved location
- rationale for consolidation, omission, or retirement

No substantive legacy content may disappear silently. It must be migrated, consolidated, preserved historically, retained as supporting evidence, intentionally retired with rationale, or identified as generated output.

When a legacy entry point stops controlling, it receives an archival notice linking to current authority and the preserved original.

## 19. Staged rollout

### Phase 1: foundations

Create directories, metadata, authority statements, placeholder modules, and README links. Remove nothing.

### Phase 2: canonical reference

Create the initial shared definitions and release `reference-v1.0.0`.

### Phase 3: V1 decomposition

Migrate V1 content by subject, verify it against the implementation, assign `V1-` codes, link evidence, and preserve originals.

### Phase 4: V2 decomposition

Convert V2 material into normative modules, decisions, schemas, tests, and migration criteria. Explicitly supersede contradictory earlier language.

### Phase 5: legacy mappings

Complete transition ledgers and archival notices.

### Phase 6: tooling

Implement deterministic validation, registry generation, traceability generation, and V1 snapshot generation.

Suggested command surface:

```text
docs validate
docs registry
docs traceability
docs snapshot-v1
docs check
```

### Phase 7: release and entry-point transition

Approve the first canonical release, generate current indexes, update both READMEs, pin the V1 snapshot, and mark replaced entry points as superseded.

## 20. Testing the documentation system

Tooling requires tests for:

- identifier parsing
- malformed identifier rejection
- duplicate detection
- heading recognition
- anchor generation
- local and cross-repository links
- lifecycle validation
- supersession chains and cycles
- retired-reference preservation
- canonical-version compatibility
- relationship validation
- deterministic registry generation
- deterministic matrix generation
- V1 snapshot generation
- legacy-mapping completeness

## 21. Human usability requirements

A reader must be able to:

- identify authority and current status immediately
- locate a replacement document
- cite a rule with a short code and title
- navigate from a shared concept to V1 and V2 behavior
- locate related decisions, schemas, tests, and evidence
- understand whether a V1/V2 difference is intentional
- distinguish current authority from historical material
- use the documentation without running tooling

Generated tables must prioritize readable Markdown. Machine-dense details may live in sidecar data.

## 22. Acceptance criteria

The documentation restructuring is complete when readers can answer, without ambiguity:

### Shared meaning

- Where is each shared concept defined?
- Which canonical-reference release applies?
- What distinguishes source observations, canonical records, assessments, correlations, releases, and evidence?

### V1

- How does V1 work?
- Which modules describe each behavior?
- Which tests and evidence support each description?
- Which V1 commit was reviewed?

### V2

- What must V2 preserve, refine, replace, or add?
- Which decisions and schemas govern it?
- Which tests verify critical requirements?
- Which evidence is required before cutover?

### Cross-version interpretation

- How does a V1 behavior map to a V2 requirement?
- Is the relationship preservation, refinement, replacement, or an accepted difference?
- What migration work remains incomplete?

### Authority and history

- Is a document approved?
- What does it control?
- Has it been superseded, retired, deprecated, or withdrawn?
- Is a citation current, pinned, or historical?
- Can the legacy source still be found?

## 23. Self-review

This design was reviewed for:

- unresolved placeholders
- contradictory authority rules
- identifier ambiguity
- duplicate document ownership
- V1 `docs/` path conflict
- missing legacy-preservation controls
- missing reference release policy
- missing validation rules
- missing human-readability requirements

Concrete commit hashes and final reference numbers are intentionally assigned during migration because they depend on repository state and the approved implementation sequence.

## 24. Implementation boundary

This design authorizes preparation of a detailed implementation plan. It does not authorize an uncontrolled one-step restructuring of both repositories.

Implementation must follow the staged rollout, preserve legacy material until verified, and require review before replacing existing documentation entry points.
