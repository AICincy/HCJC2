---
title: Artifact Classification and Retention
reference_namespace: V2
status: approved
authority: v2-artifact-classification
owner_repository: AICincy/HCJC2
document_family: data
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

> **Authority:** Approved controlled extension for the HCJC2 data documentation family.

# Artifact Classification and Retention Contract

## Classes

| Class | Examples | Public | Mutable | Retention |
|---|---|---:|---:|---|
| Source capture | Raw HCSO or Socrata response, headers, retrieval metadata | No by default | No | Source-specific, documented |
| Candidate input | Parsed but unapproved source snapshot | No | No | Short operational window |
| Canonical internal state | Approved normalized roster and feed versions | No direct listing | Pointer only | Version window plus audit requirements |
| Public data projection | Approved current roster, feeds, correlations, checksums | Yes | No; versioned | Current plus explicit public-history policy |
| Application artifact | HTML, CSS, JavaScript, fonts, documentation | Yes | No; versioned | Release retention policy |
| Photo working set | Current-roster booking photos | Controlled public | No; versioned | Remove when source no longer lists person, subject to legal hold policy |
| Operational telemetry | Metrics, timing, status, non-sensitive error summaries | No or aggregated | Append-only | Defined operational period |
| Evidentiary record | Access denials, preserved source samples, attestations | No by default | Append-only segments | Matter-specific legal retention |
| Public transparency aggregate | Counts and durations derived from evidence | Yes | No; versioned | Long-term aggregate |
| Correction/takedown record | Request, authority, action, verification | No | Append-only status history | Legal and governance policy |

## Public-data allowlist

Publication is deny-by-default. Every public artifact must appear in a versioned allowlist with:

- artifact name
- schema ID and version
- field classifications
- source and derivation
- retention rule
- cache policy
- indexing policy
- correction process
- owner

A build may not copy directories recursively into the public artifact unless every descendant is generated from the allowlist.

## Evidence rules

1. Separate evidence streams by purpose and schema.
2. Do not mix access-denial evidence, photo observations, pipeline telemetry, and correction records.
3. Identity-bearing evidence is private unless a specific reviewed publication decision exists.
4. Public transparency outputs should normally contain aggregates and redacted samples.
5. Evidence storage must support append without rewriting the entire history.
6. Each segment carries a checksum and previous-segment hash.
7. A signed or independently anchored manifest periodically commits the segment chain head.
8. Deletion, sealing, legal hold, and retention exceptions are recorded as governance events.

## Retention enforcement

Retention is executable, not descriptive. Scheduled controls must:

- identify expired artifacts
- verify no legal hold applies
- delete or anonymize the artifact
- verify public and preview copies are removed
- record the action and affected versions
- detect retention failures

## Preview rule

No preview deployment may contain real custody identities, real booking photos, correction records, private evidence, secrets, or internal logs unless the environment is explicitly authorized and access-controlled. Default previews use synthetic fixtures.
