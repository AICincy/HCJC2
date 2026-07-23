# V1 Offense Taxonomy Audit

- Status: Complete for design disposition
- Snapshot: Sol-072026.zip, July 20, 2026
- Scope: `data/orc_offenses.json`, `scraper/orc.py`, `scraper/update_orc_offenses.py`, `web/classify.py`, build integration, tests, and current roster behavior
- Decision use: HCJC2 greenfield design

## Executive finding

V1 does not contain a controlled Ohio offense taxonomy. It contains a mixed lookup table that combines manually reviewed Ohio Revised Code sections, municipal provisions, source artifacts, booking holds, automatically extracted charge descriptions, and inferred degrees. The public build mutates this table before rendering. Missing degrees default to `MM`.

The lookup achieves high apparent coverage, but that coverage is inflated by automatic ingestion of unverified source text. HCJC2 must preserve raw observations and verified legal authority as separate data classes.

## Quantitative results

| Measure | Result |
|---|---:|
| Lookup entries | 1,888 |
| Entries labeled `MM` | 1,700, or 90.0 percent |
| Distinct leading code prefixes | 366 |
| Prefixes longer than four digits | 63 |
| Current roster inmates | 1,283 |
| Current roster charges | 5,036 |
| Current roster charges finding a lookup entry | 4,935, or 98.0 percent |
| Current criminal or traffic codes labeled `MM` | 42 |
| Common Pleas charges where lookup returns a misdemeanor degree and no explicit degree suffix exists | 268 charges across 33 codes |
| Explicit source-description degree conflicts with lookup degree | 3 charges across 2 codes |

High match coverage does not establish legal accuracy. The build can add entries from the same roster it later measures against.

## Findings

### F1. The public build mutates the legal lookup

`web/build.py` calls `update_orc_offenses()` before loading the lookup and rendering the site. `scraper/update_orc_offenses.py` reads the current roster and retained court-listing captures, extracts code and description pairs, and writes new entries into `data/orc_offenses.json`.

This violates reproducible-build and authority-review boundaries. Identical source code can produce different taxonomies depending on local retained files and the current roster.

Disposition: Replace.

### F2. Missing degree defaults to minor misdemeanor

`extract_degree()` returns `MM` when no degree suffix exists. Municipal entries are also forced to `MM`. This converts missing evidence into a positive legal classification.

Disposition: Prohibit in HCJC2. Missing degree must remain unknown.

### F3. The table combines incompatible jurisdictions and record types

The file contains:

- Ohio Revised Code sections
- Cincinnati and other municipal provisions
- traffic and regulatory provisions
- booking and juvenile hold placeholders
- codes explicitly marked as not found in the Ohio Revised Code
- malformed or source-concatenated identifiers
- code-description observations copied from source systems

Every entry has only `title` and `degree`. The schema has no jurisdiction, authority type, effective date, provenance, verification status, conditional-degree rule, or source-observation status.

Disposition: Split into separate registries and assessment artifacts.

### F4. Section-level degree is often conditional

A single base section can carry several degrees based on subsection facts, amount, prior record, victim characteristics, safe release, controlled substance, or other elements.

Examples verified against the current Ohio Laws site:

- ORC 2913.47 insurance fraud ranges from M1 through F3 based on claim amount.
- ORC 2921.32 obstructing justice can take the degree of an aided misdemeanor or range from F5 through F1 depending on the underlying offense.
- ORC 2923.123 courthouse weapon offenses are F5 by default and F4 for a qualifying prior conviction.
- ORC 2905.01 kidnapping is generally F1 but can be F2 when the victim is released safely and unharmed.
- ORC 2907.04 ranges from M1 through F2 based on age difference and prior convictions.
- ORC 2913.02 theft ranges from M1 through F1 based on value and other facts.
- ORC 2925.11 contains many degree paths based on substance, amount, and prior record.

The V1 `default degree` model cannot represent these statutes accurately.

Disposition: Replace with applicability rules and an explicit unresolved state.

### F5. Lookup priority can suppress stronger venue evidence

`_charge_tier()` uses this sequence:

1. explicit degree suffix in charge description
2. lookup degree
3. court venue inference

An automatically created misdemeanor lookup therefore prevents later Common Pleas venue evidence from being considered. The current snapshot contains 268 such charge instances.

Disposition: Replace with evidence aggregation and conflict reporting. Do not use first-match-wins classification.

### F6. ORC detection depends on polluted lookup content

`is_orc_code()` treats a titled lookup entry as ORC unless its title contains one of three exclusion phrases. It also builds a chapter whitelist from titled entries. Automatically extracted or malformed entries can therefore influence link eligibility and jurisdiction inference.

Disposition: Use an explicit authority registry keyed by jurisdiction and official identifier.

### F7. Normalization is permissive and context-free

`normalize_code()` extracts the first digit-and-dot pattern from arbitrary text. It does not validate the identifier against a jurisdiction-specific grammar or authority registry.

Disposition: Preserve raw code, parse through source-specific adapters, and validate against jurisdiction-specific identifier rules.

### F8. Tests validate shape, not authority

Current tests verify JSON validity, required keys, allowed degree tokens, a few known titles, and basic helper behavior. They do not verify:

- jurisdiction
- statutory currency
- effective date
- conditional degree logic
- source provenance
- malformed-code rejection
- build immutability
- conflict handling
- public-link correctness
- review status

Disposition: Replace with contract, authority, and regression tests.

## Legal currency examples

| Section | V1 stored degree | Current statutory reality | Status |
|---|---:|---|---|
| 2913.47 | MM | M1, F5, F4, or F3 based on amount | Incorrect simplification |
| 2921.32 | MM | Same-degree misdemeanor or F5, F3, F2, or F1 | Incorrect simplification |
| 2923.123 | MM | F5 or F4 | Incorrect |
| 2905.01 | F1 | F1 or F2, with additional sentencing rules | Incomplete |
| 2907.04 | F4 | M1, F4, F3, or F2 | Incomplete |
| 2913.02 | M1 | M1 through F1 | Incomplete |

These examples are enough to reject the single-value degree field as an authoritative legal model. They do not constitute a complete currency audit of all 1,888 V1 entries.

## V2 disposition

| V1 element | V2 disposition |
|---|---|
| Raw source code and description | Preserve as immutable observation |
| Verified official title | Preserve after authority verification |
| Single `degree` field | Replace |
| Build-time mutation | Retire |
| Municipal and ORC records in one map | Split |
| Hold and artifact codes in legal lookup | Isolate |
| Chapter display categories | Redesign as versioned analytical concepts |
| Explicit degree suffix parsing | Preserve as source evidence, not final truth |
| Venue inference | Preserve as evidence with conflict handling |
| ORC deep links | Preserve only from verified authority records |

## Required immediate HCJC2 rule

No build, scraper, frontend, or correlation process may create or modify a verified legal-authority record. Only a reviewed curation workflow may promote a source observation into the authority registry.
