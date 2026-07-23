# Offense Taxonomy Research Notes

## Question

What offense-data model allows HCJC2 to improve correlations while avoiding V1's unsupported legal classifications?

## V1 sources examined

- `data/orc_offenses.json`
- `scraper/orc.py`
- `scraper/update_orc_offenses.py`
- `web/classify.py`
- `web/build.py`
- `tests/test_orc.py`
- `tests/test_classify.py`
- `tests/test_match.py`
- `tests/test_correlate.py`
- `audit/22a_orc_offenses_currency_audit.md`
- July 20 `data/current.json`

## Primary authority reviewed

- Ohio Revised Code 2901.02, classification of crimes
- Ohio Revised Code 2905.01, kidnapping
- Ohio Revised Code 2907.04, unlawful sexual conduct with minor
- Ohio Revised Code 2913.02, theft
- Ohio Revised Code 2913.47, insurance fraud
- Ohio Revised Code 2921.32, obstructing justice
- Ohio Revised Code 2923.123, courthouse weapon offenses
- Ohio Revised Code 2925.11, possession of controlled substances

Official source: Ohio Laws, `codes.ohio.gov`, reviewed July 20, 2026.

## Technical references

- FBI UCR current NIBRS technical specifications and user manual identify a versioned incident-reporting code system with business-rule validation. NIBRS is appropriate as an optional analytical crosswalk, not as a substitute for Ohio legal authority.
- NIEM code-list specifications treat code lists as versioned artifacts with definitions and independent lifecycles. HCJC2 adopts the versioning and provenance principle without requiring NIEM XML.

## Key reasoning

1. A raw agency code is an observation, not proof that the identifier is valid or current.
2. A statute title can often be verified at section level.
3. A degree often requires facts not available in the booking roster.
4. Correlation benefits from broader analytical concepts than legal titles alone.
5. Legal authority, analytical concepts, and source text must remain separately attributable.
6. Evaluation fixtures must pin taxonomy versions because mapping changes alter correlation features.

## Limits

This work did not perform a complete currency audit of all 1,888 V1 entries. The reviewed examples establish that the V1 schema is incapable of representing current law accurately. Full authority migration requires a separate item-by-item curation and verification process.
