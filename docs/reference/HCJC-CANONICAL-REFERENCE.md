---
title: HCJC Canonical Cross-Version Reference
reference_namespace: A
status: approved
authority: canonical-reference
owner_repository: AICincy/HCJC2
document_family: reference
effective_date: 2026-07-23
canonical_reference:
  version: 1.0.0
  tag: reference-v1.0.0
supersedes: []
superseded_by: null
relationships: []
---

# HCJC Canonical Cross-Version Reference

> **Authority:** Approved source of shared terminology, lifecycle concepts, identifier meaning, and cross-version interpretation for JCStream V1 and HCJC2.

## Authority and usage

Shared definitions appear here once. V1 and V2 modules summarize them and define version-specific behavior.

## Terminology and record concepts

## A-1 Source System

**Definition:** A public or approved private system from which HCJC or HCJC2 obtains an observation, reference, or operational signal.

**V1 interpretation:** V1 acquires the HCSO roster and approved public feeds through implemented source-specific clients.

**V2 interpretation:** V2 requires every source system to be registered with an explicit owner, contract, freshness policy, and public-data classification.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-2 Source Observation

**Definition:** An immutable representation of what a source reported at a specific observation time, before project interpretation changes its meaning.

**V1 interpretation:** V1 preserves roster and public-feed values in generated JSON snapshots and event records.

**V2 interpretation:** V2 formalizes immutable run-scoped observations before normalization or assessment.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-3 Canonical Record

**Definition:** A normalized project record derived from one or more source observations under a versioned transformation contract.

**V1 interpretation:** V1 uses validated inmate, charge, activity, and feed structures as its normalized project records.

**V2 interpretation:** V2 requires explicit canonical record types with versioned provenance and transformation semantics.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-4 Current Roster

**Definition:** The latest approved collection of custody records representing individuals listed by the authoritative roster source at its observation time.

**V1 interpretation:** V1 publishes the latest successful HCSO roster snapshot in current.json and generated pages.

**V2 interpretation:** V2 publishes only an approved release selected through the release pointer and last-known-good policy.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-5 Person Reference

**Definition:** A project-scoped reference used to associate records with a person without asserting that a source identifier is universally unique.

**V1 interpretation:** V1 primarily associates current records through HCSO inmate identifiers and names.

**V2 interpretation:** V2 separates person references from source identifiers, bookings, and custody episodes.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-6 Custody Record

**Definition:** A record describing a source-reported state of custody, booking, charge, court, bond, holder, or release information.

**V1 interpretation:** V1 represents custody information through validated inmate records and nested charges.

**V2 interpretation:** V2 preserves source observations while creating typed canonical custody records.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-7 Custody Episode

**Definition:** A continuous period of custody associated with one person reference and one or more source observations.

**V1 interpretation:** V1 expresses the concept through current roster presence, first-seen and last-seen values, and booking or release events.

**V2 interpretation:** V2 introduces a deterministic versioned custody episode identifier and explicit episode lifecycle.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-8 Booking Event

**Definition:** A dated event representing entry into a custody episode or the first approved observation of that entry.

**V1 interpretation:** V1 creates booked change events when a source identifier appears in the new roster.

**V2 interpretation:** V2 distinguishes source observation time, inferred event time, and approved activity publication.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-9 Release Event

**Definition:** A dated event representing departure from a custody episode or the first approved observation of that departure.

**V1 interpretation:** V1 creates released change events when a prior roster record is absent from the new approved snapshot.

**V2 interpretation:** V2 ties release events to custody episodes and stable activity routes under explicit uncertainty semantics.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-10 Material Change Event

**Definition:** A dated event representing a significant approved change to a custody record that is neither a booking nor a release.

**V1 interpretation:** V1 creates updated events for selected differences in continuing roster records.

**V2 interpretation:** V2 requires typed material-change categories and versioned activity contracts.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-11 Source Identifier

**Definition:** An identifier assigned by a source system and interpreted only within the scope documented for that source.

**V1 interpretation:** V1 uses HCSO inmate numbers, booking numbers, case numbers, and feed row identifiers in their source contexts.

**V2 interpretation:** V2 records source scope, source system, and identifier semantics explicitly.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-12 Project Identifier

**Definition:** A versioned identifier assigned by the project for a defined record type, lifecycle, and collision domain.

**V1 interpretation:** V1 generates route, event, and output identifiers through implemented build conventions.

**V2 interpretation:** V2 requires deterministic project identifiers with documented recipes and collision testing.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## Data lifecycle, release, and provenance concepts

## A-13 Public Artifact

**Definition:** A file or route intentionally approved for public access under a documented schema, retention rule, and release.

**V1 interpretation:** V1 publishes generated HTML, JSON, XML, images, and policy files through GitHub Pages.

**V2 interpretation:** V2 publishes allowlisted artifacts through separate application and data release surfaces.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-14 Candidate Release

**Definition:** An immutable collection of generated artifacts that has not yet received publication approval.

**V1 interpretation:** V1 builds a candidate site and data tree during each workflow run before repository publication.

**V2 interpretation:** V2 formalizes immutable candidate releases and prohibits public selection before verification.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-15 Approved Release

**Definition:** A candidate release that passed required validation and became the publicly selected release.

**V1 interpretation:** V1 approval is expressed through successful workflow completion, commit, and Pages publication.

**V2 interpretation:** V2 uses explicit verification and conditional pointer promotion.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-16 Last-Known-Good Release

**Definition:** The most recent approved release retained as the public fallback when a later run fails or is withheld.

**V1 interpretation:** V1 retains the previously committed and deployed state when guarded acquisition or publication does not complete.

**V2 interpretation:** V2 makes last-known-good preservation an explicit release invariant.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-17 Release Manifest

**Definition:** A versioned record listing a release's artifacts, hashes, schemas, provenance, and verification state.

**V1 interpretation:** V1 publishes checksums and generated timestamps across its distribution artifacts.

**V2 interpretation:** V2 requires one manifest that binds all public artifacts to a release and run.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-18 Source Status

**Definition:** A controlled statement describing a source's current availability, freshness, delay, degradation, pause, or retirement.

**V1 interpretation:** V1 communicates roster freshness, source access, interruptions, and recovery through pages and metrics.

**V2 interpretation:** V2 standardizes source-status vocabulary across APIs and interface components.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-19 Completeness

**Definition:** A controlled statement describing whether an artifact contains all records expected under its source and selection contract.

**V1 interpretation:** V1 applies roster health heuristics and publishes feed-specific result windows.

**V2 interpretation:** V2 requires completeness metadata and explicit partial or degraded states.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-20 Truncation

**Definition:** An explicit condition in which a bounded artifact returns fewer records than are known or potentially available.

**V1 interpretation:** V1 uses configured feed and history limits in generated artifacts.

**V2 interpretation:** V2 requires every bounded artifact to disclose limits, ordering, and truncation.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-21 Provenance

**Definition:** The recorded origin, observation time, transformation path, software version, and release context of a record or artifact.

**V1 interpretation:** V1 exposes source attribution, generated timestamps, repository history, and checksums.

**V2 interpretation:** V2 requires structured provenance on records, assessments, and releases.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-22 Public Field Allowlist

**Definition:** The explicit set of fields approved for publication from a record or feed.

**V1 interpretation:** V1 publishes selected fields through builder-specific shaping and feed queries.

**V2 interpretation:** V2 centralizes reviewed public field allowlists in contracts and the feed registry.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-23 Retained Evidence

**Definition:** A preserved result, review, approval, incident record, or operational proof used to demonstrate compliance or behavior.

**V1 interpretation:** V1 retains access ledgers, audit records, workflow history, and verification outputs.

**V2 interpretation:** V2 classifies evidence separately from public data and requires attributable retention.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-24 Supporting Material

**Definition:** Research, audit, history, or analysis that informs controlled documentation but does not itself define authority.

**V1 interpretation:** V1 preserves extensive audit, wiki, and operational reference material.

**V2 interpretation:** V2 stores non-authoritative research, audits, evidence, and historical material under a visibly separate boundary.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## Correlation and offense concepts

## A-25 Correlation

**Definition:** A documented relationship, association, or candidate association between two or more records.

**V1 interpretation:** V1 publishes candidate dispatch relationships and a separate research-oriented correlation output.

**V2 interpretation:** V2 requires typed, explainable, versioned, reviewable, and correctable relationship assessments.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-26 Candidate Relationship

**Definition:** A possible relationship retained for assessment because it satisfies a relationship family's candidate-generation rules.

**V1 interpretation:** V1 retains dispatch candidates that satisfy implemented time, agency, disposition, or text conditions.

**V2 interpretation:** V2 generates candidates broadly, then applies explicit disqualifying, competition, and cardinality rules.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-27 Supporting Evidence

**Definition:** A signal that increases support for a candidate relationship or assessment under a documented ruleset.

**V1 interpretation:** V1 uses temporal, agency, disposition, and text signals in its matchers.

**V2 interpretation:** V2 records every supporting signal and its source provenance.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-28 Conflicting Evidence

**Definition:** A signal that decreases support or creates ambiguity without automatically disqualifying a candidate.

**V1 interpretation:** V1 represents reduced support primarily through lower match confidence or candidate ordering.

**V2 interpretation:** V2 publishes material conflicts explicitly in the assessment explanation.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-29 Missing Evidence

**Definition:** An expected signal that is unavailable, omitted, unresolved, or not observable.

**V1 interpretation:** V1 proceeds with the fields available from the current source records.

**V2 interpretation:** V2 distinguishes missing evidence from negative evidence and may abstain.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-30 Disqualifying Evidence

**Definition:** A signal that makes a candidate relationship or assessment ineligible under a documented rule.

**V1 interpretation:** V1 applies eligibility conditions within matcher logic.

**V2 interpretation:** V2 records disqualifying rules and rejected candidates as governed review data.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-31 Evidence Score

**Definition:** A deterministic or statistical summary of evidence that is not a probability unless separately calibrated and validated.

**V1 interpretation:** V1 research correlations use an implemented confidence value to rank candidate relationships.

**V2 interpretation:** V2 uses an explainable evidence score and prohibits probability terminology without calibration.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-32 Confidence Band

**Definition:** A controlled qualitative interpretation of an assessment's evidence and uncertainty.

**V1 interpretation:** V1 presents candidate status and research confidence in the context of investigatory relationships.

**V2 interpretation:** V2 standardizes strong, probable, possible, conflicted, unresolved, and rejected bands.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-33 Charge Observation

**Definition:** A source observation preserving raw charge text, code, degree, jurisdiction, and source context.

**V1 interpretation:** V1 stores source-reported charge rows within each inmate record.

**V2 interpretation:** V2 separates immutable charge observations from authority records and assessments.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-34 Authority Record

**Definition:** A reviewed statute, ordinance, rule, or legal reference with currency, jurisdiction, and source provenance.

**V1 interpretation:** V1 maintains ORC title and degree references used for classification and statute pages.

**V2 interpretation:** V2 requires reviewed, dated, jurisdiction-specific authority records with amendment status.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-35 Offense Concept

**Definition:** An analytical category used to group related charge observations without replacing legal authority.

**V1 interpretation:** V1 groups charges into public analytical categories such as violence, weapons, property, theft, drugs, family, and other.

**V2 interpretation:** V2 retains analytical concepts as distinct records rather than legal classifications.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-36 Charge Assessment

**Definition:** A versioned interpretation connecting a charge observation to possible authority records, concepts, classifications, and unresolved facts.

**V1 interpretation:** V1 derives statute, category, and severity context during processing and build generation.

**V2 interpretation:** V2 records each interpretation as a provenance-bearing assessment with explicit unresolved facts.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## Product, correction, evidence, and governance concepts

## A-37 Correction

**Definition:** A documented process and resulting record used to amend inaccurate, incomplete, or misleading published information.

**V1 interpretation:** V1 provides no-fee correction routes and updates current generated outputs when corrections are accepted.

**V2 interpretation:** V2 requires correction records, disposition states, provenance, and publication effects.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-38 Removal

**Definition:** A documented process and resulting state used to stop public availability of an eligible record or artifact.

**V1 interpretation:** V1 removes current roster entries and associated active photos after source departure and supports sealing or removal requests.

**V2 interpretation:** V2 requires typed removal decisions, exact public-object deletion, cache purge, and private evidence.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-39 Dispute

**Definition:** A documented challenge to a correlation, assessment, or publication decision that requires review and disposition.

**V1 interpretation:** V1 provides public correction and project-reporting channels applicable to published information.

**V2 interpretation:** V2 adds explicit correlation dispute lifecycle states and stable relationship identifiers.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-40 Progressive Enhancement

**Definition:** A presentation model in which essential content and actions remain available without required client-side JavaScript.

**V1 interpretation:** V1 generates complete static HTML and uses JavaScript for optional search, filtering, maps, tooltips, and lightboxes.

**V2 interpretation:** V2 requires essential status, records, legal notices, corrections, and methodology to remain available without required client-side JavaScript.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-41 Current Custody Status

**Definition:** A presentation statement identifying whether the latest approved roster lists a person as currently in custody.

**V1 interpretation:** V1 individual pages and roster views derive current status from the latest successful snapshot.

**V2 interpretation:** V2 makes current custody status the primary state distinction and separates it from historical activity.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-42 Controlled Document

**Definition:** A document with declared authority, lifecycle, ownership, effective date, and stable references.

**V1 interpretation:** V1 controlled reference modules describe implemented behavior against a pinned canonical edition.

**V2 interpretation:** V2 controlled modules define requirements, decisions, and migration criteria.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-43 Supersession

**Definition:** The formal replacement of one controlled document or entry by another approved authority.

**V1 interpretation:** V1 preserves superseded documentation for historical interpretation while linking to current controlling references.

**V2 interpretation:** V2 records explicit replacement chains and validates them for completeness and cycles.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-44 Verification Procedure

**Definition:** An executable test, check, or review method identified by a `T-` reference.

**V1 interpretation:** V1 tests and operational verification commands demonstrate implemented behavior.

**V2 interpretation:** V2 links critical requirements to explicit verification procedures.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-45 Evidence Record

**Definition:** A dated and attributable result, approval, review, or incident record identified by an `E-` reference.

**V1 interpretation:** V1 retains workflow, audit, access, and test evidence in repository records and ledgers.

**V2 interpretation:** V2 requires evidence for release gates, migration acceptance, and operational decisions.

**Related references:** Version-specific links are added when their controlled entries are assigned.

## A-46 Accepted Difference

**Definition:** A reviewed V1-to-V2 difference that is intentional, documented, and not a migration defect.

**V1 interpretation:** V1 serves as the behavioral baseline from which differences are measured.

**V2 interpretation:** V2 records intentional redesigns and their approval rather than treating all non-parity as failure.

**Related references:** Version-specific links are added when their controlled entries are assigned.
