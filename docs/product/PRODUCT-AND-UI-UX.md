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
relationships:
- from: V2-73
  relation: refines
  to: A-41
- from: V2-77
  relation: requires
  to: A-40
- from: V2-78
  relation: requires
  to: A-40
---

# Product and UI/UX

> **Authority:** Approved controlled HCJC2 product specification. It defines V2 requirements for this subject and delegates shared terminology to the canonical reference.

## Scope

This document controls the HCJC2 product and ui/ux requirements. Shared concepts are defined in the [HCJC Canonical Cross-Version Reference](../reference/HCJC-CANONICAL-REFERENCE.md).

## Controlled rules

## V2-67 Civic-Data Interface, Not a Mugshot Gallery

The product prioritizes custody lookup, source status, provenance, activity, methodology, corrections, and explainable evidence. Booking photographs are record content, not the primary browsing or hero device.

## V2-68 Public Route Hierarchy

The controlled route model includes home, people, custody episodes, activity, stable activity events, map, trends, data catalog, feed detail, methodology, corrections, legal, developers, accountability, and transparency.

## V2-69 Home Page Hierarchy

The home page leads with source status, primary custody search, current roster count, observation time, recent activity, feed health, and routes to methodology and corrections.

## V2-70 Search Behavior

Search supports approved names and identifiers, charge text, ORC citations, case numbers, activity IDs, and relationship IDs while distinguishing exact, approximate, unavailable, and stale results.

## V2-71 Result-Type Distinction

Current custody, prior activity, court, correlation, data-catalog, and methodology results are visually and semantically distinct.

## V2-72 Roster Presentation

Desktop may use an accessible data table; mobile transforms results into structured cards without compressing core facts or requiring horizontal scrolling.

## V2-73 Custody Episode Page

Current custody status, source time, booking data, observations, assessments, court and bond context, correlations, provenance, legal notice, and correction actions follow a controlled hierarchy.

## V2-74 Stable Activity Pages

Booking, release, material change, source correction, and eligible correlation updates use stable event identifiers and routes.

## V2-75 Public Data Catalog

Each feed page shows agency, description, status, source time, release time, schema, completeness, truncation, retention, fields, route, methodology, and limitations.

## V2-76 Maps and Trends

Maps provide list or table alternatives, location precision, uncertainty, filters, status, and date range. Trends disclose denominators, gaps, source changes, and avoid causal implication.

## V2-77 Progressive Enhancement

Essential status, search guidance, roster facts, activity facts, methodology, legal notices, corrections, and data catalog remain available without required client-side JavaScript.

## V2-78 WCAG 2.2 AA

Keyboard operation, visible focus, semantics, screen-reader status, contrast, zoom, reflow, reduced motion, touch targets, table structure, and map or chart alternatives are release requirements.

## V2-79 Data Status Communication

Every major view displays source status, source observation time, publication time, release ID, completeness, truncation, and degraded or stale conditions.

## V2-80 Explainable Correlation Presentation

Correlation components show inferred status, relationship type, confidence band, plain-language rationale, evidence for and against, missing evidence, source times, methodology, and dispute actions.

## V2-81 Controlling Visual Palette

The controlling palette uses civic red `#c2002c`, institutional navy `#122174`, white `#fefefe`, near black `#1a1a1a`, and accessible restrained grays. Gradients and off-brand accent colors are prohibited.

## V2-82 Typography and Visual Grammar

Helvetica Neue with documented system fallbacks, oversized bold headings, strong blocks, rounded sporty controls, clear rules, and dense but scannable civic-data layouts define the visual system.

## V2-83 Mobile-First Responsive Behavior

Mobile is a first-class layout with stacked status and search, card-based records, visible timestamps, touch-accessible actions, and no core horizontal scrolling.

## V2-84 Typed Component Boundaries

The application shell, status banner, search, roster, custody summary, observations, assessments, correlations, provenance, maps, charts, correction forms, legal notices, and failure states use independently testable typed components.

## Related decisions, contracts, schemas, tests, and evidence

Related controlled extensions and verification records are linked as they are approved.

## Supporting material

Supporting research, audits, and historical planning remain non-authoritative under `docs/supporting/`.
