# Project Charter

## Mission

HCJC2 will provide a reliable, accessible, privacy-conscious, and auditable public interface to the Hamilton County, Ohio Justice Center custody roster and approved contextual public datasets.

## Problem

The current JCStream implementation contains valuable domain knowledge and operational safeguards, but its architecture combines acquisition, transformation, publication, generated output, legal operations, and historical evidence in ways that increase change risk. HCJC2 will preserve verified behavior while replacing brittle implementation patterns.

## Scope

HCJC2 includes:

- custody roster acquisition and normalization
- approved supplemental public feeds
- public static publication
- search, filtering, data exploration, and provenance
- accessibility and progressive enhancement
- operational monitoring, rollback, and evidence
- correction and removal workflows
- Netlify hosting evaluation and implementation

## Exclusions until separately approved

- consumer reporting or background screening
- identity correlation between custody records and unrelated geographic feeds
- permanent public archives of released individuals
- unreviewed publication of internal or evidentiary data
- runtime features that require undisclosed tracking

## Success

HCJC2 succeeds when it can replace V1 without reducing data integrity, privacy, accessibility, legal safeguards, freshness, recoverability, or public usefulness.
