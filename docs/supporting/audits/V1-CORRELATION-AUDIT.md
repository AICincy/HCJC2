# V1 Correlation Audit

- Status: Complete for the July 20, 2026 snapshot
- V1 repository: `AICincy/HCJC`
- Snapshot times:
  - custody roster: `2026-07-20T18:34:22Z`
  - current CFS feed: `2026-07-20T18:34:23Z`
  - PDI CFS feed: `2026-07-20T18:34:26Z`
- V2 disposition: Preserve and enhance the capability. Replace both V1 implementations.

## Executive conclusion

V1 does not contain one correlation system. It contains two independent matchers with conflicting policies, different candidate rules, different outputs, and contradictory publication assumptions.

The public matcher is not a calibrated correlation engine. It is a time-window candidate selector. On the audited snapshot it returned exactly four candidates for every matched person because four is the hard cap. The stricter private matcher agreed with only 29 of the public matcher's 1,752 pairs.

V2 must not copy either implementation. It must preserve the intended capability and build one canonical, governed, explainable event-linkage system.

## Quantitative findings

The measurements below were produced by executing both V1 matchers against the same repository snapshot.

| Metric | Public matcher | Private matcher |
|---|---:|---:|
| Active custody records | 1,283 | 1,283 |
| Deduplicated CFS rows available to public build | 2,769 | N/A |
| People with at least one candidate | 438 | 92 |
| Candidate pairs | 1,752 | 517 |
| Candidate count per matched person | Exactly 4 for all 438 | Variable |
| Pair overlap between engines | 29 | 29 |
| Pairs unique to this engine | 1,723 | 468 |
| Dispatch events assigned to multiple people | 116 | 148 |
| Maximum people assigned to one event | 31 | 5 |

These figures do not establish which pairs are correct. They establish that the two engines implement materially different definitions of correlation and that the public output has severe candidate saturation.

## F1. Duplicate implementations

### Public matcher

`scraper/match.py`:

- anchors a date-only booking at midnight
- accepts calls from 12 hours before through 36 hours after that anchor
- requires CPD agency
- accepts disposition prefixes `ARR`, `CIT`, and `301`
- sorts only by temporal distance from midnight
- returns the nearest four rows
- does not compare charges or incident type
- does not produce a score or rationale

Source: `scraper/match.py`, lines 1-88.

### Private matcher

`scraper/correlate.py`:

- uses a separate time-window implementation
- compares only the first listed charge description
- uses substring-based token overlap
- combines temporal and textual scores with fixed equal weights
- adds a fixed arrest-disposition boost
- labels the result `confidence` without calibration
- identifies source rows by list index
- writes a separate researcher-mode artifact

Source: `scraper/correlate.py`, lines 23-330.

### Disposition

**Replace.** V2 will have one canonical engine used by all outputs.

## F2. Public candidate saturation

The public matcher returns at most four rows. In the audited snapshot, every matched person reached that cap. The cap therefore hides the size of the underlying candidate pool and makes four unrelated rows appear like a curated result.

A selection rule based only on date, agency, and broad disposition cannot distinguish among people booked on the same date. One dispatch event was reused across 31 custody records.

### Disposition

**Replace.** Candidate counts, competition, and ambiguity must remain visible to the engine. The public interface must not imply that a hard-capped nearest-neighbor list is a ranked relationship assessment.

## F3. Arbitrary confidence values

The private matcher calculates:

- 50 percent temporal score
- 50 percent token overlap
- plus 0.15 for an arrest disposition

The weights are hand-selected. No labeled evaluation set, calibration curve, holdout test, or error bound supports interpreting the result as probability or confidence.

### Disposition

**Redesign.** V2 will call uncalibrated output an `evidence_score`. It may use `match_probability` only after validation demonstrates probability calibration on held-out labeled examples.

## F4. Incorrect and ambiguous time handling

V1 treats date-only HCSO booking dates as midnight. The public matcher uses naive datetimes. The private matcher attaches UTC to naive source values. Cincinnati source timestamps do not carry an explicit offset in the stored rows.

This creates several risks:

- local time can be mislabeled as UTC
- daylight-saving transitions are not modeled
- temporal distance from midnight is not distance from the actual booking
- first observation time is ignored as an upper bound
- source time uncertainty is not represented

### Disposition

**Redesign.** V2 will represent source timestamps as intervals with an explicit source timezone and uncertainty.

## F5. Unstable source references

The private artifact identifies a CFS row by its list index. Feed refreshes can reorder, insert, or remove rows. The same index can therefore identify a different event later.

The public build deduplicates by `event_number` but falls back to Python object identity when that field is absent. Object identity is process-local and non-reproducible.

Sources:

- `scraper/correlate.py`, lines 34-38 and 316-323
- `web/build.py`, lines 143-155

### Disposition

**Replace.** V2 requires stable source keys formed from dataset ID, agency record ID, and source snapshot hash.

## F6. Weak text comparison

The private matcher:

- uses only the first charge
- splits on whitespace
- ignores punctuation and statutory structure
- uses substring containment instead of token equality
- has a short fixed stop-word list
- does not normalize synonyms
- does not use ORC code compatibility
- does not model contradictory charges

### Disposition

**Replace.** V2 will use a versioned offense taxonomy with exact mappings, aliases, ORC relationships, and explicit incompatible pairs.

## F7. No relationship cardinality model

A dispatch can lead to multiple arrests, and one booking can be associated with multiple source events. V1 treats every pair independently. It has no event-level competition penalty, group-arrest representation, or relationship capacity rule.

### Disposition

**Redesign.** V2 will define cardinality by relationship type and model group events explicitly.

## F8. Contradictory publication architecture

The private module states that correlations do not reach the public site. The public build separately runs `attach_candidates` and renders candidates on individual pages.

Sources:

- `scraper/correlate.py`, lines 1-20 and 302-314
- `web/build.py`, lines 143-155
- `web/templates/inmate.html`, lines 387-404

The workflow runs the private correlator with `continue-on-error`, then the public build independently computes different candidates.

Source: `.github/workflows/sweep.yml`, lines 126-134.

### Disposition

**Replace.** Correlation generation becomes an explicit pipeline stage. The public build consumes the versioned correlation artifact and never recomputes relationships.

## F9. Incomplete provenance

V1 does not persist:

- source snapshot checksums
- source retrieval times per pair
- engine commit
- ruleset version
- taxonomy version
- candidate-generation policy
- rejected alternatives
- competition context
- stable relationship ID
- reviewer history

### Disposition

**Redesign.** V2 will retain complete provenance for every assessment.

## F10. Insufficient tests

Current tests verify parsing, simple time inclusion, simple text overlap, and basic output writing. They do not test:

- timezones or daylight-saving transitions
- candidate saturation
- event reuse
- one-to-many group arrests
- multiple charges
- ORC compatibility
- conflicting evidence
- source reordering
- stable identifiers
- calibration
- reviewer overrides
- publication thresholds
- corrections and removal
- sealed or takedown records
- stale source artifacts
- cross-version reproducibility

### Disposition

**Replace.** V2 requires labeled evaluation, contract tests, property tests, resilience tests, and public-output tests.

## V2 requirements extracted from V1

| Requirement | Disposition |
|---|---|
| Show possible relationships between bookings and dispatches | Preserve and enhance |
| Avoid presenting inference as confirmed fact | Preserve |
| Explain why a pair was nominated | Preserve and expand |
| Use source-level identifiers | Preserve, but replace unstable indexes |
| Support research and public presentation | Preserve through one governed artifact |
| Use date and disposition as signals | Preserve as partial evidence only |
| Limit misleading noise | Redesign through calibrated thresholds and ambiguity display |
| Retain current-roster lifecycle | Preserve |
| Provide correction and review | Add |
| Support additional relationship families | Add |

## Immediate implementation boundary

No V2 correlation code should be written until:

1. the canonical source-event schema is approved
2. relationship types and cardinality rules are approved
3. the labeling protocol is approved
4. the public presentation policy is approved
5. the initial evaluation fixture set exists
